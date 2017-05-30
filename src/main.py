#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from time import time
TIME0 = time()
__VERSION__ = 11
from os import chdir
from os.path import dirname
import sys
try:
    chdir(dirname(__file__))
    sys.path.append(dirname(__file__))
except:
    pass
import global_vars
from kivy.config import Config
Config.set('kivy', 'exit_on_escape', 0)
from kivy import require as kivy_require
kivy_require('1.9.2')
from kivy.properties import StringProperty, ListProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from app_modules.media_controller.media_playlist_view import MediaPlaylistView
from app_modules.media_controller.media_queue_view import MediaQueueView
from app_modules.media_controller.controller import MediaController
from app_modules.popups_and_dialogs.create_playlist import CreatePlaylistPopup
from app_modules.popups_and_dialogs.remove_playlist import RemovePlaylistPopup
from kivy.logger import Logger, LoggerHistory
from app_modules.media_player import mplayer
from kivy.uix.floatlayout import FloatLayout
from kivy.core.clipboard import Clipboard
from kivy.clock import Clock, mainthread
from app_configs import AppConfigHandler
from app_modules.kb_system import focus
from kivy.core.window import Window
from app_modules import appworker
from utils import not_implemented
from kivy.utils import platform
from utils import get_unicode
from kivy.lang import Builder
from kivy.compat import PY2
from kivy.app import App
import traceback
import sys

if platform in ('windows','win', 'linux'):
    from app_modules.layouts.pc_layout_methods import LayoutMethods
    Config.set( 'input', 'mouse', 'mouse,disable_multitouch')


class Jotube(LayoutMethods, FloatLayout):
    sidebar_items = ListProperty()
    media_control = MediaController(mplayer)

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
        '''Runs when a file is dropped on the window'''
        self.display_info('DROPPED FILES: %s' % (get_unicode(path)))
        screen = self.manager.current
        path = get_unicode(path)
        if screen in ('media', 'queue'):
            pl = 'playlist'
            if screen == 'queue':
                pl = 'queue'
            Clock.schedule_once(lambda *a: self.on_dropfile_after(
                path, mouse_pos=Window.mouse_pos, playlist=pl),
                0.2)

    def on_dropfile_after(self, path, mouse_pos=None, playlist=None):
        self.media_control.on_dropfile(
            path, mouse_pos=mouse_pos, playlist=playlist)

    def mgui_open_settings(self, *args):
        not_implemented.show_error(feature='App settings')

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
        super(Jotube, self).on_video_screen(*args)

    def display_info(self, text):
        self.ids.info_widget.info(text)

    def display_warning(self, text):
        self.ids.info_widget.warning(text)

    def on_error(self, error):
        '''For showing errors in GUI'''
        self.ids.info_widget.error(error)

    def set_mplayer_volume(self, value):
        mplayer.set_volume(value)

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
        screen = self.manager.current
        if screen in 'media':
            self.media_control.jump_to_current_index('playlist')
        elif screen == 'queue':
            self.media_control.jump_to_current_index('queue')

    def init_widgets(self, *args):
        Window.bind(on_dropfile=self.on_dropfile)
        self.app_configurator = AppConfigHandler(self)
        self.app_configurator.load_before()
        self.manager = Jotube_SM(transition=NoTransition())
        self.manager.bind(current=self.on_screen_current)
        self.ids.sm_area.add_widget(self.manager)

        self.manager.current = 'main'

        ## FIRST SCREEN MEDIA PLAYER - sc-media
        mplayer.bind(on_error=self.on_error)
        self.media_control.videoframe = self.manager.ids.video_screen
        self.media_control.videoframe_small = self.ids.video_small
        self.media_control.bind(cur_viewed_playlist=self.on_viewed_playlist)
        self.media_control.bind(
            videoframe_is_visible=lambda obj, val: self.on_video_screen(
                val, self.media_control.playing_video))
        self.ids.sm_area.bind(
            size=lambda ob,v: self.media_control.on_video_resize(v))

        playlistview = MediaPlaylistView()
        queueview = MediaQueueView()

        self.manager.ids.media_stack.add_widget(playlistview)
        self.manager.ids.queue_stack.add_widget(queueview)

        self.media_control.attach_playlist_view(playlistview)
        self.media_control.attach_queue_view(queueview)

        self.media_control.bind(playlists=self.reset_sidebar_widgets)
        self.media_control.reset_playlists()
        self.media_control.bind(
            playing_seek_value=self.ids.playback_bar.on_media_progress_val)
        self.media_control.bind(
            playing_seek_max=self.ids.playback_bar.on_media_progress_max)

        self.ids.playback_bar.on_seeking = mplayer.seek
        self.ids.playback_bar.on_playbtn = self.media_control.play_pause
        self.ids.playback_bar.on_prevbtn = self.media_control.play_previous
        self.ids.playback_bar.on_nextbtn = self.media_control.play_next

        mplayer.bind(on_pause=self.ids.playback_bar.on_pause)
        mplayer.bind(on_play=self.ids.playback_bar.on_play)
        mplayer.bind(on_start=self.ids.playback_bar.on_play)

        self.ids.playback_bar.bind(
            media_volume=lambda obj, val: mplayer.set_volume(val))

        self.ids.video_small.on_video_touch = (
            lambda: self.switch_screen('video'))
        self.ids.video_small.on_video_scroll_down = (
            self.ids.playback_bar.volume_increase)
        self.ids.video_small.on_video_scroll_up = (
            self.ids.playback_bar.volume_decrease)

        super(Jotube, self).init_widgets()
        self.app_configurator.load_after()
        self.ids.playback_bar.media_volume = mplayer.volume * 100

        self.sc_focusable_switch = {
            self.media_control.view_playlist: ('media'),
            self.media_control.view_queue: ('queue'),
            self.manager.ids.media_filter_widget: ('media'),
            self.manager.ids.plugin_manager: ('main')
        }

        # For testing
        def testfunc(*a):
            self.media_control.open_playlist_by_id(3)
            self.switch_screen('media')
        Clock.schedule_once(testfunc, 1)


class Jotube_SM(ScreenManager):
    pass


class JotubeApp(App):
    mlayout = global_vars.layout_manager
    mtheme = global_vars.theme_manager
    root_widget = None

    def build(self):
        self.root_widget = Jotube()
        self.icon = 'data/icon.png'
        return self.root_widget

    def on_start(self):
        self.root_widget.init_widgets()
        self.last_frame_time = time() - TIME0
        Logger.info('App: on_start: %s' % (self.last_frame_time))
        Clock.schedule_once(lambda dt: self.on_some_frame(1, 6), 0)

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
        if focus.focusable_widgets and focus.current_focus:
            focus.remove_focus()
        else:
            self.stop()

    def on_stop(self):
        if not hasattr(self, 'app_is_stopping_now'):
            self.app_is_stopping_now = True
            settings = {'volume': str(mplayer.volume)}
            self.root_widget.app_configurator.load_with_args(
                'user_settings', 'save', settings)

def main_loop():
    try:
        Builder.load_file('app_modules/layouts/pc_layout.kv')
        Builder.load_file('app_modules/layouts/screen_manager.kv')
        app = JotubeApp()
        app.run()
    except Exception as e:
        traceback.print_exc()
    appworker.stop()


if __name__ == "__main__":
    from multiprocessing import freeze_support
    freeze_support()
    appworker.start_workers(1)
    main_loop()
