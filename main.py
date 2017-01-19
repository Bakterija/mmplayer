#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Version: Beta 9
from __future__ import print_function
from time import time
starttime = time()
from kivy.logger import Logger, LoggerHistory
from kivy.compat import PY2
if not PY2:
    Logger.error('App: Python3 is not supported yet, exiting')
    quit()
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
from app_modules.service_com import serviceCom
from app_modules.media_player.media_player_client import \
Media_Player_Client as Media_Player
from app_modules.media_controller.controller import MediaController
from app_modules.media_controller.media_playlist_view import MediaPlaylistView
from app_modules.media_controller.media_queue_view import MediaQueueView
from app_configs import AppConfigHandler
from kivy.config import Config as KivyConfig
from kivy.lib import osc
import traceback
import sys
print ('DONE IMPORTS', time() - starttime)

if platform in ('windows','win', 'linux'):
    # Disabled for now
    # from multiprocessing import Process
    # from service import main as PCservice
    from app_modules.layouts.pc_layout_methods import LayoutMethods
    KivyConfig.set( 'input', 'mouse', 'mouse,disable_multitouch')
    sys.dont_write_bytecode = True


class Jotube(LayoutMethods, FloatLayout):
    sidebar_items = ListProperty()

    def __init__(self, **kwargs):
        super(Jotube, self).__init__(**kwargs)
        self.data_list = []
        self.service = None
        Window.bind(on_dropfile=self.on_dropfile)
        self.app_configurator = AppConfigHandler(self)
        self.app_configurator.load_before()
        Clock.schedule_once(self.init_widgets, 0)

    def switch_screen(self, screen_name):
        self.manager.current = screen_name
        self.media_control.current_screen = screen_name
        if screen_name == 'video':
            self.media_control.videoframe_is_visible = True
        elif self.media_control.videoframe_is_visible:
            self.media_control.videoframe_is_visible = False

    def reset_sidebar_widgets(self, media_controller, playlists):
        self.app_configurator.load_with_args(
            'sidebar_loader', media_controller, playlists)

    def on_dropfile(self, win, val):
        '''Runs when a file is dropped on the window'''
        self.media_control.on_dropfile(val)

    def mgui_add_playlist(self, *args):
        '''For adding playlists in MediaController from GUI buttons'''
        self.media_control.create_playlist_popup()

    def mgui_add_local_files(self, *args):
        '''For adding files to playlists in MediaController from GUI buttons'''
        self.media_control.add_local_files_popup()

    def on_video_screen(self, *args):
        '''Runs when video screen is entered and left.
        Moves small video in or out, among other things'''
        super(Jotube, self).on_video_screen(*args)

    def on_error(self, error):
        '''For showing errors in GUI'''
        self.ids.info_widget.error(error)

    def init_widgets(self, *args):
        self.manager = Jotube_SM()
        # self.manager = Jotube_SM(transition=NoTransition())
        self.manager.screen_switch_modified = self.switch_screen
        self.ids.sm_area.add_widget(self.manager)

        self.manager.current = 'media'
        self.service = serviceCom(self)

        ## FIRST SCREEN MEDIA PLAYER - sc-media
        self.mPlayer = Media_Player()
        self.mPlayer.modes['on_error'].append(self.on_error)
        self.mPlayer.set_osc_sender(self.service.send_message)
        self.media_control = MediaController(self.mPlayer)
        self.media_control.videoframe = self.manager.ids.video_screen
        self.media_control.videoframe_small = self.ids.video_small
        self.media_control.bind(
            videoframe_is_visible=lambda obj, val:self.on_video_screen(
                val, self.media_control.playing_video))
        self.ids.sm_area.bind(
            size=lambda ob,v: self.media_control.on_video_resize(v))

        playlistview = MediaPlaylistView(self.media_control)
        queueview = MediaQueueView(self.media_control)
        self.manager.ids.media_stack.add_widget(playlistview)
        self.manager.ids.queue_stack.add_widget(queueview)

        self.media_control.bind_on_playlists(self.reset_sidebar_widgets)
        self.media_control.reset_playlists()
        self.media_control.bind(
            playing_seek_value=self.ids.playback_bar.on_media_progress_val)
        self.media_control.bind(
            playing_seek_max=self.ids.playback_bar.on_media_progress_max)

        self.ids.playback_bar.on_seeking = self.mPlayer.seek
        self.ids.playback_bar.on_playbtn = self.media_control.play_pause
        self.ids.playback_bar.on_prevbtn = self.media_control.play_previous
        self.ids.playback_bar.on_nextbtn = self.media_control.play_next

        self.mPlayer.modes['on_pause'].append(self.ids.playback_bar.on_pause)
        self.mPlayer.modes['on_play'].append(self.ids.playback_bar.on_play)
        self.mPlayer.modes['on_start'].append(self.ids.playback_bar.on_play)

        self.ids.playback_bar.bind(
            media_volume=lambda obj, val: self.mPlayer.set_volume(val))

        self.ids.video_small.on_video_touch = (
            lambda: self.switch_screen('video'))
        self.ids.video_small.on_video_scroll_down = (
            self.ids.playback_bar.volume_increase)
        self.ids.video_small.on_video_scroll_up = (
            self.ids.playback_bar.volume_decrease)

        super(Jotube, self).init_widgets()
        self.app_configurator.load_after()
        self.ids.playback_bar.media_volume = self.mPlayer.volume * 100

class Jotube_SM(ScreenManager):

    def screen_switch_modified(self):
        pass


class JotubeApp(App):
    root_widget = None

    def build(self):
        self.root_widget = Jotube()
        return self.root_widget

    def on_start(self):
        pass

    def on_pause(self):
        self.root_widget.service.SERVICEdisconnect()
        self.root_widget.mPlayer.background_switch()
        return True

    def on_resume(self):
        self.root_widget.service.SERVICEconnect()

    def on_stop(self):
        settings = {'volume': self.root_widget.mPlayer.volume}
        self.root_widget.app_configurator.load_with_args(
            'user_settings', 'save', settings)

        self.root_widget.mPlayer.stop()
        self.stop_static(self)

    @staticmethod
    def stop_static(self):
        try:
            self.root_widget.service.stop()
        except Exception as e:
            try:
                service = serviceCom(object)
                service.stop()
            except Exception as e:
                print(e)
        try:
            osc.dontListen()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    try:
        Builder.load_file('app_modules/layouts/pc_layout.kv')
        Builder.load_file('app_modules/layouts/screen_manager.kv')
        app = JotubeApp()
        app.run()
    except Exception as e:
        traceback.print_exc()
        Logger.error('[App         ] Crashed, stopping processes')
        try:
            app.on_stop()
        except:
            JotubeApp.stop_static(None)
