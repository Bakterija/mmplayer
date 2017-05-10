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
# from app_modules import appworker
# appworker.start_workers(1)
from kivy.config import Config
Config.set('kivy', 'exit_on_escape', 0)
from kivy.logger import Logger, LoggerHistory
from kivy.compat import PY2
from kivy import require as kivy_require
kivy_require('1.9.2')
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
from kivy.clock import Clock, mainthread
from kivy.utils import platform
from kivy.properties import StringProperty, ListProperty, ObjectProperty
from app_modules.media_player import mplayer
from app_modules.media_controller.controller import MediaController
from app_modules.media_controller.media_playlist_view import MediaPlaylistView
from app_modules.media_controller.media_queue_view import MediaQueueView
from app_configs import AppConfigHandler
from kivy.config import Config as KivyConfig
from app_modules.behaviors.focus import focus
from utils import get_unicode
import traceback
import sys

if platform in ('windows','win', 'linux'):
    from app_modules.layouts.pc_layout_methods import LayoutMethods
    KivyConfig.set( 'input', 'mouse', 'mouse,disable_multitouch')
    sys.dont_write_bytecode = True


class Jotube(LayoutMethods, FloatLayout):
    sidebar_items = ListProperty()
    media_control = ObjectProperty()

    def __init__(self, **kwargs):
        super(Jotube, self).__init__(**kwargs)
        self.data_list = []
        Window.bind(on_dropfile=self.on_dropfile)
        self.app_configurator = AppConfigHandler(self)
        self.app_configurator.load_before()
        Clock.schedule_once(self.init_widgets, 0)

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
        Clock.schedule_once(lambda *a: self.on_dropfile_after(path), 0.5)

    def on_dropfile_after(self, path):
        self.media_control.on_dropfile(path)

    def mgui_add_playlist(self, *args):
        '''For adding playlists in MediaController from GUI buttons'''
        self.media_control.create_playlist_popup()

    def on_video_screen(self, *args):
        '''Runs when video screen is entered and left.
        Moves small video in or out, among other things'''
        super(Jotube, self).on_video_screen(*args)

    def display_info(self, text):
        self.ids.info_widget.info(text)

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

    def init_widgets(self, *args):
        self.manager = Jotube_SM()
        self.manager = Jotube_SM(transition=NoTransition())
        self.manager.bind(current=self.on_screen_current)
        self.manager.screen_switch_modified = self.switch_screen
        self.ids.sm_area.add_widget(self.manager)

        self.manager.current = 'main'

        ## FIRST SCREEN MEDIA PLAYER - sc-media
        mplayer.error_callback = self.on_error
        self.media_control = MediaController(mplayer)
        self.media_control.videoframe = self.manager.ids.video_screen
        self.media_control.videoframe_small = self.ids.video_small
        self.media_control.bind(cur_viewed_playlist=self.on_viewed_playlist)
        self.media_control.bind(
            videoframe_is_visible=lambda obj, val:self.on_video_screen(
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

        # For testing
        def testfunc(*a):
            self.media_control.open_playlist_by_id(8)
        # Clock.schedule_once(testfunc, 0.2)

class Jotube_SM(ScreenManager):

    def screen_switch_modified(self):
        pass


class JotubeApp(App):
    root_widget = None

    def build(self):
        self.root_widget = Jotube()
        self.icon = 'data/icon.png'
        return self.root_widget

    def on_start(self):
        Logger.info('App: on_start: %s' % (time() - TIME0))
        Clock.schedule_once(self.on_first_frame, 0)
        pass

    def on_first_frame(self, *args):
        Logger.info('App: on_first_frame: %s' % (time() - TIME0))

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
    # appworker.stop()

if __name__ == "__main__":
    main_loop()
