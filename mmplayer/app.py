#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

__version__ = 11.0
__url__ = 'https://github.com/Bakterija/mmplayer'
__description__ = 'A Kivy media player'
__author_email__ ='atiskrp@gmail.com'
__author__ = 'Atis K.'
__icon_path__ = 'data/icon.png'

from time import time, sleep
TIME0 = time()
import sys
from kivy.utils import platform
from kivy.config import Config
Config.set('kivy', 'exit_on_escape', 0)
# Config.set('kivy', 'log_level', 'debug')
from kivy import require as kivy_require
kivy_require('1.9.2')
import global_vars
from kivy.logger import Logger, LoggerHistory
from kivy.properties import StringProperty, ListProperty, ObjectProperty
from popups_and_dialogs.create_playlist import CreatePlaylistPopup
from popups_and_dialogs.remove_playlist import RemovePlaylistPopup
from kivy.uix.screenmanager import ScreenManager, NoTransition
from media_controller.media_playlist_view import MediaPlaylistView
from media_controller.media_queue_view import MediaQueueView
from media_controller.controller import MediaController
from kivy_soil.kb_system import focus_behavior
from kivy.uix.floatlayout import FloatLayout
from kivy.storage.jsonstore import JsonStore
from kivy.core.clipboard import Clipboard
from kivy.clock import Clock, mainthread
from app_configs import AppConfigHandler
from kivy.core.window import Window
from utils import get_unicode, logs
from media_player import mplayer
from kivy_soil import kb_system
from kivy.lang import Builder
from kivy.compat import PY2
from kivy.app import App
import traceback
import sys

if platform in ('windows','win', 'linux'):
    from layouts.pc_layout_methods import LayoutMethods
    Config.set( 'input', 'mouse', 'mouse,disable_multitouch')


class MMplayer(LayoutMethods, FloatLayout):
    sidebar_items = ListProperty()
    media_control = MediaController(mplayer)
    dropped_files = ListProperty()
    '''holds dropped file paths before media_control.on_dropfile is called'''

    def __init__(self, app, **kwargs):
        super(MMplayer, self).__init__(**kwargs)
        self.app = app

    def switch_screen(self, screen_name):
        if screen_name != self.manager.current:
            self.manager.current = screen_name
            self.media_control.current_screen = screen_name
            if screen_name == 'video':
                self.media_control.videoframe_is_visible = True
            elif self.media_control.videoframe_is_visible:
                self.media_control.videoframe_is_visible = False

    def reset_sidebar_widgets(self, media_controller, playlists):
        self.app_configurator.load_with_args(
            'sidebar_loader', media_controller, playlists)

    def on_dropfile(self, win, path):
        '''Appends dropped file to self.dropped_files
        and schedules _on_dropfile_after() for next frame.
        App is blocking and nothing else is done
        before this method is called for all dropped files'''
        self.dropped_files.append(get_unicode(path))
        Clock.unschedule(self._on_dropfile_after)
        Clock.schedule_once(self._on_dropfile_after, 0)

    def _on_dropfile_after(self, *args):
        '''Is called from Clock schedule when all dropped files have been
        appended to self.dropped_files. Creates a file drop notification
        and calls self.add_dropped_files()'''
        len_dropped_files = len(self.dropped_files)
        if len_dropped_files > 1:
            droptext = 'Dropped %s files' % (len_dropped_files)
        else:
            droptext = 'Dropped one file'
        self.display_info(droptext)
        Clock.schedule_once(self.add_dropped_files, 0)

    def add_dropped_files(self, *args):
        '''Gets mouse position and selected playlist, then
        calls self.media_control.on_dropfile() to add new file to playlist'''
        screen = self.manager.current
        if screen in ('media', 'queue'):
            if screen == 'queue':
                playlist = 'queue'
            else:
                playlist = 'playlist'
            for mpath in self.dropped_files:
                self.media_control.on_dropfile(
                    mpath, mouse_pos=Window.mouse_pos, playlist=playlist)
        self.dropped_files = []

    def mgui_open_settings(self, *args):
        logs.not_implemented(feature='App settings')

    def mgui_add_playlist(self, *args):
        '''For adding playlists in MediaController from GUI buttons'''
        popup = CreatePlaylistPopup()
        popup.open()

    def mgui_remove_playlist(self, playlist_path):
        '''For adding playlists in MediaController from GUI buttons'''
        popup = RemovePlaylistPopup(playlist_path)
        popup.open()

    def on_video_screen(self, *args):
        '''Runs when video screen is entered and left.
        Moves small video in or out, among other things'''
        super(MMplayer, self).on_video_screen(*args)

    def display_info(self, text):
        '''Displays info notification'''
        self.ids.info_widget.info(text)

    def display_warning(self, text):
        '''Displays warning notification'''
        self.ids.info_widget.warning(text)

    def display_error(self, error):
        '''Displays error notification'''
        self.ids.info_widget.error(error)

    def set_mplayer_volume(self, value):
        self.media_control.set_volume(value)

    def mplayer_seek_relative(self, value):
        mplayer.seek_relative(value)

    def mplayer_next(self):
        mplayer.next()

    def mplayer_previous(self):
        mplayer.previous()

    def on_viewed_playlist(self, mcontrol, playlist, screen='media'):
        self.set_playhint_text(self.manager.current, playlist=playlist)

    def on_screen_current(self, _, value):
        self.set_playhint_text(value, playlist=None)
        self.update_focusable_widgets(value)

    def update_focusable_widgets(self, screen):
        for k, v in self.sc_focusable_switch.items():
            if screen in v:
                k.is_focusable = True
            else:
                k.is_focusable = False

    def set_playhint_text(self, screen, playlist=None):
        mcontrol = self.media_control
        ntext = ''
        if screen == 'queue':
            if not mplayer.queue:
                ntext = '\n'.join((
                    'Queue is empty', 'drop a file/folder here',
                    'or select a playlist'))
        elif screen == 'media':
            if playlist and not playlist.media:
                if playlist.can_add:
                    ntext = 'Playlist is empty\ndrop a file/folder here'
                else:
                    ntext = '{} directory is empty'.format(playlist.name)
        elif screen == 'video' and not mcontrol.playing_video:
            ntext = 'No video is playing'
        self.ids.playlisthint.text = ntext

    def set_media_filter_text(self, text):
        if self.media_control.view_playlist:
            self.media_control.view_playlist.filter_text = text

    def jump_to_current(self):
        '''Calls media_control.jump_to_current_index()'''
        screen = self.manager.current
        if screen in 'media':
            self.media_control.jump_to_current_index('playlist')
        elif screen == 'queue':
            self.media_control.jump_to_current_index('queue')

    def init_widgets(self, *args):
        mcontrol = self.media_control
        playback_bar = self.ids.playback_bar
        Window.bind(on_dropfile=self.on_dropfile)
        self.app_configurator = AppConfigHandler(self)
        self.app_configurator.load_before()
        self.manager = MMplayer_SM(transition=NoTransition())
        self.manager.bind(current=self.on_screen_current)
        self.ids.sm_area.add_widget(self.manager)

        self.manager.current = 'main'

        ## FIRST SCREEN MEDIA PLAYER - sc-media
        mplayer.bind(on_error=self.display_error)
        mcontrol.videoframe = self.manager.ids.video_screen
        mcontrol.videoframe_small = self.ids.video_small
        mcontrol.bind(cur_viewed_playlist=self.on_viewed_playlist)
        mcontrol.bind(
            videoframe_is_visible=lambda ob, v: self.on_video_screen(
                v, mcontrol.playing_video))
        self.ids.sm_area.bind(size=lambda ob, v: mcontrol.on_video_resize(v))

        playlistview = MediaPlaylistView()
        queueview = MediaQueueView()

        self.manager.ids.media_stack.add_widget(playlistview)
        self.manager.ids.queue_stack.add_widget(queueview)

        mcontrol.attach_playlist_view(playlistview)
        mcontrol.attach_queue_view(queueview)

        mcontrol.bind(on_playlist_update=self.reset_sidebar_widgets)
        mcontrol.bind(
            playing_seek_value=playback_bar.setter('media_progress_val'))
        mcontrol.bind(
            playing_seek_max=playback_bar.setter('media_progress_max'))
        mcontrol.bind(shuffle=playback_bar.setter('shuffle'))
        mcontrol.bind(muted=playback_bar.setter('muted'))
        mcontrol.bind(volume=playback_bar.setter('media_volume'))
        mcontrol.reset_playlists()

        playback_bar.on_playbtn = mcontrol.play_pause
        playback_bar.on_prevbtn = mcontrol.play_previous
        playback_bar.on_nextbtn = mcontrol.play_next
        playback_bar.bind(on_set_volume=lambda ob, v: mcontrol.set_volume(v))
        playback_bar.bind(on_set_seek=lambda ob, v: mplayer.seek(v))
        playback_bar.bind(on_toggle_shuffle=lambda *a: setattr(
            mcontrol, 'shuffle', not mcontrol.shuffle))
        playback_bar.bind(on_toggle_mute=lambda *a: setattr(
            mcontrol, 'muted', not mcontrol.muted))

        mplayer.bind(on_pause=playback_bar.on_pause)
        mplayer.bind(on_play=playback_bar.on_play)
        mplayer.bind(on_start=playback_bar.on_play)

        self.ids.sidebar.bind(width=self.app.mlayout.setter('sidebar_width'))

        self.ids.video_small.on_video_touch = (
            lambda: self.switch_screen('video'))
        self.ids.video_small.on_video_scroll_down = (
            mcontrol.volume_increase)
        self.ids.video_small.on_video_scroll_up = (
            mcontrol.volume_decrease)

        super(MMplayer, self).init_widgets()
        self.app_configurator.load_after()

        self.sc_focusable_switch = {
            mcontrol.view_playlist: ('media'),
            mcontrol.view_queue: ('queue'),
            self.manager.ids.media_filter_widget: ('media'),
            self.manager.ids.plugin_manager: ('main')
        }

        # For testing
        def testfunc(*a):
            self.media_control.open_playlist_by_id(3)
            self.switch_screen('media')
        Clock.schedule_once(testfunc, 1)


class MMplayer_SM(ScreenManager):
    pass


class MMplayerApp(App):
    mlayout = global_vars.layout_manager
    '''Global layout manager'''

    mtheme = global_vars.theme_manager
    '''Global theme manager'''

    escape_presses = 0
    '''Tracks escape press counts for kb_quit method'''

    root_widget = None

    store_path = global_vars.DIR_CONF + '/mmplayer.json'
    store = JsonStore(store_path, indent=4, sort_keys=True)

    def build(self):
        self.root_widget = MMplayer(self)
        self.icon = __icon_path__
        return self.root_widget

    def on_start(self):
        self.root_widget.init_widgets()
        self.last_frame_time = time() - TIME0
        Logger.info('App: on_start: %s' % (self.last_frame_time))
        Clock.schedule_once(lambda dt: self.on_some_frame(1, 8), 0)

    def on_some_frame(self, current, fmax):
        this_time = time() - TIME0
        fps = 1 / (this_time - self.last_frame_time)
        Logger.info('App: on_frame {0: >2}: {1: >5} - {2: >3}'.format(
            current, round(this_time, 3), str(int(fps))))
        current += 1
        self.last_frame_time = this_time
        if current != fmax:
            Clock.schedule_once(
                lambda dt: self.on_some_frame(current, fmax), 0)

    def on_pause(self):
        return True

    def on_resume(self):
        pass

    def kb_esc(self):
        '''Updates self.escape_presses, quits app when reached target value'''
        cfocus = focus_behavior.current_focus
        if cfocus:
            focus_behavior.remove_focus()
        else:
            if self.escape_presses == 1:
                self.stop()
            else:
                self.root_widget.display_info('Double press escape to quit')
            self.escape_presses += 1
            Clock.unschedule(self.reset_escape_presses)
            Clock.schedule_once(self.reset_escape_presses, 0.7)

    def reset_escape_presses(self, *args):
        self.escape_presses = 0

    def on_stop(self):
        if not hasattr(self, 'app_is_stopping_now'):
            self.app_is_stopping_now = True
            root = self.root_widget
            new_settings = [('volume', root.media_control.volume)]
            self.root_widget.app_configurator.load_with_args(
                'user_settings', 'save', new_settings)

def main_loop():
    try:
        Builder.load_file('layouts/pc_layout.kv')
        Builder.load_file('layouts/screen_manager.kv')
        app = MMplayerApp()
        app.run()
    except Exception as e:
        traceback.print_exc()


if __name__ == "__main__":
    main_loop()
