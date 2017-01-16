#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Version: Beta 7.1
from __future__ import print_function
from kivy import require as kivy_require
kivy_require('1.9.2')
from app_modules.ptimer import PTimer
ptimer = PTimer()
from kivy.app import App
from app_modules.terminal_app.terminalapp import TerminalApp
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
from kivy.clock import Clock, mainthread
from kivy.utils import platform
from kivy.properties import StringProperty, ListProperty, ObjectProperty
from kivy.logger import Logger, LoggerHistory
from app_modules.service_com import serviceCom
from app_modules.media_player.media_player_client import \
Media_Player_Client as Media_Player
from app_modules.media_gui.media_gui import Media_GUI
from app_modules.media_gui.media_playlist_view import MediaPlaylistView
from app_modules.media_gui.media_queue_view import MediaQueueView
from app_modules.key_binder.key_binder import KeyBinder
from kivy.config import Config as KivyConfig
from kivy.lib import osc
import traceback
import sys
import os
ptimer.add('imports')

if platform in ('windows','win', 'linux'):
    # Disabled for now
    # from multiprocessing import Process
    # from service import main as PCservice
    from app_modules.layouts.pc_layout_methods import LayoutMethods
    KivyConfig.set( 'input', 'mouse', 'mouse,disable_multitouch')
    sys.dont_write_bytecode = True


def make_dirs():
    if platform == 'android':
        d = os.path.dirname('/storage/emulated/0/github_bakterija/')
        if not os.path.exists(d):
            os.makedirs(d)
        d = os.path.dirname('/storage/emulated/0/github_bakterija/jotube/')
        if not os.path.exists(d):
            os.makedirs(d)
        d = os.path.dirname(
            '/storage/emulated/0/github_bakterija/jotube/audio/')
        if not os.path.exists(d):
            os.makedirs(d)
        d = os.path.dirname(
            '/storage/emulated/0/github_bakterija/jotube/audio/thumbnails/')
        if not os.path.exists(d):
            os.makedirs(d)
        d = os.path.dirname(
            '/storage/emulated/0/github_bakterija/jotube/audio/')
    else:
        d = os.path.dirname('media/thumbnails/')
        if not os.path.exists(d):
            os.makedirs(d)
        d = os.path.dirname('media/playlists/')
        if not os.path.exists(d):
            os.makedirs(d)


class Jotube(TerminalApp, LayoutMethods, FloatLayout):
    sidebar_items = ListProperty()

    def __init__(self, **kwargs):
        super(Jotube, self).__init__(**kwargs)
        global data_list, serviceConnected , serviceStarted
        self.data_list = []
        data_list = self.data_list
        self.settings = {}
        # Window.clearcolor = (0.1, 0.1, 0.1, 0.1)
        if platform in ('linux', 'win', 'windows'):
            Window.set_icon('data/icon.png')
            # Window.system_size = (480,960)
            # Window.system_size = (1000,650)
            # Window.system_size = (700,420)
        self.service = None
        Builder.load_file('app_modules/layouts/screen_manager.kv')
        self.keybinder = KeyBinder()
        # self.keybinder.use_logger = True
        Window.bind(on_dropfile=self.on_dropfile)
        Clock.schedule_once(self.init_widgets, 0)

    def add_file(self, text, dlFormat):
        '''Used to get audio/video files to play from youtue linkes
        GUI parts were removed at some point'''
        if self.service.connected:
            if dlFormat == 'Video':
                sett = 'dl-video'
            else:
                sett = 'dl-audio'
            sendmsg = 'DOWNLOAD::'+sett+':'+text
            self.service.send_message(sendmsg.encode('utf_8'))

    def receive_data(self,*arg):
        '''Parses data from the app service and executes funtions'''
        for data in self.data_list:
            if data[:8] == 'audioSV:':
                # MediaPlayer server commands
                self.mPlayer.osc_callback(data[8:])
            elif data[:15] == 'DL::Downloader-':
                # Removed youtube loader commands
                self.mGUI.downloader_task(data[15:])
                self.ins_text(data)
            else:
                self.ins_text(data)
            del self.data_list[0]

    def ins_text(self,text):
        self.terminal.add_tdata(unicode(text))

    def switch_screen(self, screen_name):
        self.manager.current = screen_name
        self.mGUI.current_screen = screen_name
        if screen_name == 'sc-video':
            self.mGUI.videoframe_is_visible = True
        elif self.mGUI.videoframe_is_visible:
            self.mGUI.videoframe_is_visible = False

    def reset_sidebar_widgets(self, mgui_widget, playlists):
        app_to_side = [
            {'text': 'SCREENS', 'wtype': 'section'},
            {
                'text': 'Main', 'wtype': 'text', 'can_select': True,
                'func': lambda: self.switch_screen("sc-media"),
                'func2':None},
            {
                'text': 'Queue', 'wtype': 'text', 'can_select': True,
                'func': lambda: self.switch_screen("sc-queue"),
                'func2':None},
            {
                'text': 'Video', 'wtype': 'text', 'can_select': True,
                'func': lambda: self.switch_screen("sc-video"),
                'func2':None},
            {
                'text': 'Terminal', 'wtype': 'text', 'can_select': True,
                'func': lambda: self.switch_screen("sc-terminal"),
                'func2':None},
            {
                'text': 'Browser', 'wtype': 'text', 'can_select': True,
                'func': lambda: self.switch_screen("sc-browser"),
                'func2':None},
            {'text': '', 'wtype': 'separator'}
        ]
        self.sidebar_items = []
        for x in app_to_side:
            self.sidebar_items.append(x)
        self.sidebar_items.append({'text': 'PLACES', 'wtype': 'section'})
        nm = 'places'
        def append_item(item):
            self.sidebar_items.append({
                'text': item['name'],
                'wtype': 'text',
                'can_select': True,
                'func': lambda item=item: {
                    self.mGUI.open_playlist(item),
                    self.switch_screen("sc-media")
                },
                'func2': lambda item=item: {
                    self.mGUI.playlist_cmenu_popup(item)
                }
            })

        for section in playlists:
            for item in section:
                if nm == item['section']:
                    append_item(item)
                else:
                    nm = item['section']
                    self.sidebar_items.append(
                        {'text': '', 'wtype': 'separator'})
                    self.sidebar_items.append(
                        {'text': item['section'].upper(), 'wtype': 'section'})
                    append_item(item)
        self.sidebar_items.append({'text': '', 'wtype': 'separator'})

    def on_dropfile(self, win, val):
        '''Runs when a file is dropped on the window'''
        self.mGUI.on_dropfile(val)

    def mgui_add_playlist(self, *args):
        '''For adding playlists in mGUI from GUI buttons'''
        self.mGUI.create_playlist_popup()

    def mgui_add_local_files(self, *args):
        '''For adding files to playlists in mGUI from GUI buttons'''
        self.mGUI.add_local_files_popup()

    def on_video_screen(self, *args):
        '''Runs when video screen is entered and left.
        Moves small video in or out, among other things'''
        super(Jotube, self).on_video_screen(*args)

    def on_error(self, error):
        '''For showing errors in GUI'''
        self.ids.info_widget.error(error)

    def init_widgets(self, *args):
        make_dirs()
        self.manager = Jotube_SM()
        # self.manager = Jotube_SM(transition=NoTransition())
        self.manager.screen_switch_modified = self.switch_screen
        self.ids.sm_area.add_widget(self.manager)

        self.manager.current = 'sc-media'
        self.service = serviceCom(self)
        serviceConnected = self.service.connected
        serviceStarted = self.service.serviceSTARTED

        ## TERMINAL
        try:
            self.terminal = self.tapp_get_gui()
            self.tapp_add('Init terminal', color='ff3333')
            self.manager.ids.sc3_stack1.add_widget(self.terminal)
            Clock.schedule_interval(self.receive_data, 0.2)
        except Exception as e:
            traceback.print_exc()

        ## FIRST SCREEN MEDIA PLAYER - sc-media
        try:
            self.mPlayer = Media_Player()
            self.mPlayer.modes['on_error'].append(self.on_error)
            self.mPlayer.set_osc_sender(self.service.send_message)
            self.mGUI = Media_GUI(self.mPlayer)
            self.mGUI.videoframe = self.manager.ids.sc4
            self.mGUI.videoframe_small = self.ids.video_small
            self.mGUI.bind(videoframe_is_visible=lambda obj, val:
                           self.on_video_screen(val, self.mGUI.playing_video))
            self.ids.sm_area.bind(
                size=lambda ob,v: self.mGUI.on_video_resize(v))

            playlistview = MediaPlaylistView(self.mGUI)
            queueview = MediaQueueView(self.mGUI)
            self.manager.ids.sc2_stack1.add_widget(playlistview)
            self.manager.ids.sc55_stack1.add_widget(queueview)
            self.mGUI.bind_on_playlists(self.reset_sidebar_widgets)
            self.mGUI.reset_playlists()
            self.mGUI.bind(
                playing_seek_value=self.ids.playback_bar.on_media_progress_val)
            self.mGUI.bind(
                playing_seek_max=self.ids.playback_bar.on_media_progress_max)
            self.ids.playback_bar.on_seeking = self.mPlayer.seek
            self.ids.playback_bar.on_playbtn = self.mGUI.play_pause
            self.ids.playback_bar.on_prevbtn = self.mGUI.play_previous
            self.ids.playback_bar.on_nextbtn = self.mGUI.play_next
            self.ids.playback_bar.media_volume = self.mPlayer.volume * 100
            self.mPlayer.modes['on_pause'].append(self.ids.playback_bar.on_pause)
            self.mPlayer.modes['on_resume'].append(self.ids.playback_bar.on_play)
            self.mPlayer.modes['on_start'].append(self.ids.playback_bar.on_play)
            self.ids.playback_bar.bind(
                media_volume=lambda obj, val: self.mPlayer.set_volume(val))
            self.ids.video_small.on_video_touch = (
                lambda: self.switch_screen('sc-video'))
            self.ids.video_small.on_video_scroll_down = (
                self.ids.playback_bar.volume_increase)
            self.ids.video_small.on_video_scroll_up = (
                self.ids.playback_bar.volume_decrease)

            self.keybinder.add(
                'vol_increase', '273', 'down',
                self.ids.playback_bar.volume_increase, modifier=['ctrl'])
            self.keybinder.add(
                'vol_decrease', '274', 'down',
                self.ids.playback_bar.volume_decrease, modifier=['ctrl'])
            self.keybinder.add(
                'seek_4_sec_back', '276', 'down',
                lambda: self.mPlayer.seek_relative(-4), modifier=['shift'])
            self.keybinder.add(
                'seek_4_sec_forward', '275', 'down',
                lambda: self.mPlayer.seek_relative(4), modifier=['shift'])
            self.keybinder.add(
                'seek_60_sec_back', '276', 'down',
                lambda: self.mPlayer.seek_relative(-60), modifier=['ctrl'])
            self.keybinder.add(
                'seek_60_sec_forward', '275', 'down',
                lambda: self.mPlayer.seek_relative(60), modifier=['ctrl'])
            self.keybinder.add(
                'play_pause_toggle', '32', 'down', self.mGUI.play_pause)
        except Exception as e:
            traceback.print_exc()

        self.mPlayer.set_modes({'screen_on':False})

        ptimer.add('app init')
        for x in ptimer.get():
            self.tapp_add('[PTimer] %s %s %s' % (x[1], x[2], x[0]))

        try:
            # Run LayoutMethods init_widgets method when this is done
            super(Jotube, self).init_widgets()
        except Exception as e:
            self.ids.info_widget.error(traceback.format_exc())
            traceback.print_exc()

class Jotube_SM(ScreenManager):

    def screen_switch_modified(self):
        pass


class JotubeApp(App):
    def build(self):
        self.app_rt = Jotube()
        return self.app_rt

    def on_pause(self):
        self.app_rt.service.SERVICEdisconnect()
        self.app_rt.mPlayer.background_switch()
        return True

    def on_resume(self):
        self.app_rt.service.SERVICEconnect()

    def on_stop(self):
        try:
            self.app_rt.mPlayer.stop()
        except Exception as e:
            print(e)
        self.stop_static(self)

    @staticmethod
    def stop_static(self):
        try:
            self.app_rt.service.stop()
        except Exception as e:
            service = serviceCom(object)
            service.stop()
        osc.dontListen()


if __name__ == "__main__":
    try:
        Builder.load_file('app_modules/layouts/pc_layout.kv')
        ptimer.add('kv load')
        app = JotubeApp()
        ptimer.add('app load')
        app.run()
    except Exception as e:
        traceback.print_exc()
        Logger.error('[App         ] Crashed, stopping processes')
        try:
            app.on_stop()
        except:
            JotubeApp.stop_static(None)
