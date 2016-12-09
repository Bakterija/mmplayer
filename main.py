#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Version: Beta 4
from __future__ import print_function
from kivy import require as kivy_require
kivy_require('1.9.2')
from time import strftime, time, sleep
from app_modules.ptimer import PTimer
ptimer = PTimer()
from kivy.app import App
from app_modules.terminal_app.terminalapp import TerminalApp
from threading import Thread
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.clipboard import Clipboard
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock, mainthread
from kivy.utils import platform
from kivy.properties import StringProperty, ListProperty, ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.metrics import cm, dp
from kivy.graphics import *
from sys import path
from kivy import kivy_home_dir
from kivy.logger import Logger, LoggerHistory
from app_modules.service_com import serviceCom
from app_modules.setting_handler import Setting_handler
from app_modules.my_scrollview import My_ScrollView as ScrollView2
from app_modules.my_scrollview import My_ScrollView_y as ScrollView2y
from app_modules.media_player.media_player_client import \
Media_Player_Client as Media_Player
from app_modules.youtube_view import Youtube_View
from app_modules.media_gui.media_gui import Media_GUI
from app_modules.media_gui.media_playlist_view import MediaPlaylistView
from app_modules.media_gui.media_queue_view import MediaQueueView
import app_modules.accurate_seeker_buttons as Accurate_Seeker
# from app_modules.youtube import yt_loader as YT_Loader
# from app_modules.youtube.youtube_dl_kivy_browser.browser import YDL_Browser
from app_modules.key_binder.key_binder import KeyBinder
from kivy.config import Config as KivyConfig
from urllib2 import urlopen
from kivy.lib import osc
import json
import traceback
import sys
import os
ptimer.add('imports')
if platform == 'android':
    import android
    # from android.runnable import run_on_ui_thread
elif platform in ('windows','win', 'linux'):
    from multiprocessing import Process
    from service import main as PCservice
    from app_modules.layouts.pc_layout_methods import LayoutMethods

    def pcservice():
        PCservice.main_loop()

    sys.dont_write_bytecode = True
    KivyConfig.set( 'input', 'mouse', 'mouse,disable_multitouch')
    service_process = Process(target=pcservice)
    service_process.start()


def return_path():
    if platform == 'android':
        return '/storage/emulated/0/github_bakterija/jotube/'
    return path[0]+'/'


def return_audio_path():
    if platform == 'android':
        return '/storage/emulated/0/github_bakterija/jotube/audio/'
    return path[0]+'/service/media/'


def make_dirs():
    if platform == 'android':
        d = os.path.dirname('/storage/emulated/0/github_bakterija/')
        if not os.path.exists(d):
            os.makedirs(d)
        d = os.path.dirname('/storage/emulated/0/github_bakterija/jotube/')
        if not os.path.exists(d):
            os.makedirs(d)
        d = os.path.dirname('/storage/emulated/0/github_bakterija/jotube/audio/')
        if not os.path.exists(d):
            os.makedirs(d)
        d = os.path.dirname('/storage/emulated/0/github_bakterija/jotube/audio/thumbnails/')
        if not os.path.exists(d):
            os.makedirs(d)
        d = os.path.dirname('/storage/emulated/0/github_bakterija/jotube/audio/')
    else:
        d = os.path.dirname('media/thumbnails/')
        if not os.path.exists(d):
            os.makedirs(d)
        d = os.path.dirname('media/playlists/')
        if not os.path.exists(d):
            os.makedirs(d)


def readf(filename):
    file = filename
    try:
        f = open(file, 'rU')
    except:
        savef('',filename)
        f = open(file, 'rU')
    a = f.read()
    a = str.splitlines(a)
    f.close()
    return a


def savef(text,file):
    f = open(file, 'w')
    f.write(text)
    f.close()


def edit_settings(text,text_find,new_value):
    count = 0
    newlist = []
    for lines in text:
        b = lines.find(text_find)
        if b is not -1:
            c = text_find + '=' + str(new_value)
            newlist.append(c)
        else:
            newlist.append(lines)
        count+=1
    count = 1
    return newlist


def get_settings(text,text_find,default_value):
    for lines in text:
        b = lines.find(text_find)
        if b is not -1:
            c = lines[len(text_find):]
    ## Checks if it exists and appends something, if not
    try:
        if c == '':
            c = default_value
            if default_value != '':
                write_settings(text_find[:-1],'\n'+c)
    except:
        path = return_path()
        c = default_value
        fh = open(path+'settings.ini', 'a')
        fh.write('\n'+str(text_find)+str(c))
        fh.close()
    return c


def read_settings(*arg):
    path = return_path()
    a = readf(path+'settings.ini')
    a = get_settings(a,arg[0],arg[1])
    return a


def write_settings(text_find,new_value):
    path = return_path()
    a = readf(path+'settings.ini')
    a = edit_settings(a,text_find,new_value)
    text = a = '\n'.join(str(e) for e in a)
    savef(text,path+'settings.ini')


def get_time():
    return strftime("[%H:%M]")


def get_time_sec():
    return strftime("[%H:%M:%S]")


def timestring_from_int(seconds):
    seconds = int(seconds)
    m, s = divmod(seconds, 60)
    s = str(m).zfill(2)+':'+str(s).zfill(2)
    return s


def focus_widget(widget):
    widget.focus = True


def return_true(*arg):
    return True


class Global_Callbacks(object):
    def __init__(self,*arg):
        self.dict = {
            'on_resize': [],
            'on_pause': [],
            'on_resume': [],
            'on_screen': [],
        }
        Window.bind(on_size= self.on_resize)

    def add(self, dictio,func):
        self.dict[dictio].append(func)
    def remove(self,dictio,func):
        for i,x in enumerate(self.dict[dictio]):
            if x == func:
                del self.dict[dictio][i]

    def on_resize(self,*arg):
        for x in self.dict['on_resize']:
            x()

    def on_pause(self,*arg):
        for x in self.dict['on_pause']:
            x()

    def on_resume(self,*arg):
        for x in self.dict['on_resume']:
            x()

    def on_screen(self,*arg):
        for x in self.dict['on_screen']:
            x()


class Jotube(TerminalApp, LayoutMethods, FloatLayout):
    sidebar_items = ListProperty()

    def __init__(self, **kwargs):
        super(Jotube, self).__init__(**kwargs)
        global data_list, serviceConnected , serviceStarted
        self.data_list = []
        data_list = self.data_list
        self.settings = {}
        # Window.clearcolor = (0.1, 0.1, 0.1, 0.1)
        if platform == 'linux' or platform == 'windows':
            Window.set_icon(return_path()+'data/icon.png')
            # Window.system_size = (480,960)
            # Window.system_size = (1000,650)
            # Window.system_size = (700,420)
        self.service = None
        Builder.load_file('app_modules/layouts/screen_manager.kv')
        self.keybinder = KeyBinder()
        Window.bind(on_dropfile=self.on_dropfile)
        Clock.schedule_once(self.init_widgets, 0)

    def add_file(self,text,dlFormat):
        if self.service.connected:
            if dlFormat == 'Video': sett = 'dl-video'
            else: sett = 'dl-audio'
            sendmsg = 'DOWNLOAD::'+sett+':'+text
            self.service.send_message(sendmsg.encode('utf_8'))

    def receive_data(self,*arg):
        for data in self.data_list:
            if data[:8] == 'audioSV:':
                self.mPlayer.osc_callback(data[8:])
            elif data[:15] == 'DL::Downloader-':
                self.mGUI.downloader_task(data[15:])
                self.ins_text(data)
            else:
                self.ins_text(data)
            del self.data_list[0]

    def ins_text(self,text):
        self.terminal.add_tdata(unicode(text))

    def switch_screen(self, screen_name):
        # if screen_name == 'sc-video':
        #     Window.clearcolor = (0, 0, 0, 0)
        # else:
        #     Window.clearcolor = (0.1, 0.1, 0.1, 0.1)
        # if screen_name == 'sc-terminal':
        #     self.terminal.tcan_refresh = True
        #     self.terminal.scroll_y = 0.0
        # else:
        #     self.terminal.tcan_refresh = False
        #     self.terminal.scroll_y = 1.0
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
            {
                'text': 'Options', 'wtype': 'text', 'can_select': True,
                'func': lambda: self.switch_screen("sc-options"),
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
        self.mGUI.on_dropfile(val)

    def mgui_add_playlist(self, *args):
        self.mGUI.create_playlist_popup()

    def mgui_add_local_files(self, *args):
        self.mGUI.add_local_files_popup()

    def on_video_screen(self, *args):
        super(Jotube, self).on_video_screen(*args)

    def on_error(self, error):
        self.ids.info_widget.error(error)

    def init_widgets(self, *args):
        make_dirs()
        self.manager = Jotube_SM(size_hint=(1,1))
        self.manager.screen_switch_modified = self.switch_screen
        self.ids.sm_area.add_widget(self.manager)

        self.manager.current = 'sc-media'
        self.settings['download_mode'] = str(
            read_settings('download_mode=','Sequential'))
        self.settings['download_format'] = str(
            read_settings('download_format=','Audio'))
        self.settings['video_provider'] = str(
            read_settings('video_provider=','Kivy'))
        self.settings['audio_provider'] = str(
            read_settings('audio_provider=','Kivy'))
        self.settings['stream_provider'] = str(
            read_settings('stream_provider=','Kivy'))
        self.settings['startup_mode'] = str(
            read_settings('startup_mode=','Yes'))

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
            global_callbacks.add('on_pause', self.mPlayer.background_switch)
            self.mGUI = Media_GUI(self.mPlayer)
            self.mGUI.videoframe = self.manager.ids.sc4
            self.mGUI.videoframe_small = self.ids.video_small
            self.mGUI.bind(videoframe_is_visible=lambda obj, val:
                           self.on_video_screen(val, self.mGUI.playing_video))
            self.ids.sm_area.bind(
                size=lambda ob,v:self.mGUI.on_video_resize(v))

            playlistview = MediaPlaylistView(self.mGUI, size_hint_y=1)
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
        ## OPTIONS sc-options
        optionlayout = self.manager.ids.sc1_stack1

        option_scroll = ScrollView2y(
            size_hint=(1,0.85), scroll_distance=50, do_scroll_x=False)
        option_grid = option_scroll.children[0]
        optionlayout.add_widget(option_scroll)

        testing = True
        if platform == 'android' or testing:
            videoset = Setting_handler(
                option_grid, self.settings, 'video_provider',
                'Video provider', ('Kivy','External','No video'))
            audioset = Setting_handler(
                option_grid, self.settings, 'audio_provider',
                'Audio provider', ('Kivy','Kivy-Server','External'))
            streamset = Setting_handler(
                option_grid,self.settings, 'stream_provider',
                'Stream provider', ('Kivy','External'))
            audioset.bind_click(self.mPlayer.set_audio_provider, run=True)
            streamset.bind_click(self.mPlayer.set_stream_provider, run=True)
        else:
            videoset = Setting_handler(
                option_grid, self.settings, 'video_provider',
                'Video provider' , ('Kivy','No video'))
        dlfset = Setting_handler(
            option_grid, self.settings, 'download_format',
            'Download format' , ('Audio','Video'))
        startupset = Setting_handler(
            option_grid , self.settings , 'startup_mode',
            'Startup service' , ('Yes','No'))
        videoset.bind_click(self.mPlayer.set_video_provider, run=True)
        if platform == 'android' and self.settings['startup_mode'] == 'Yes':
            self.service.toggle_service()
        self.mPlayer.set_modes({'screen_on':False})

        # self.manager.current = 'sc-browser'
        # self.ydl_test = YDL_Browser()
        # self.manager.ids.sc5_stack1.add_widget(self.ydl_test)
        #
        # self.ydl_test.set_title('Titls')
        # self.ydl_test.set_thumbnail('')
        # self.ydl_test.set_uploader('Uploader')
        # self.ydl_test.set_view_count('view_c 200')
        # self.ydl_test.set_like_count('like_c 300')
        # self.ydl_test.set_duration('dur 3:20')
        # self.ydl_test.set_dislike_count('disl_c 400')
        # self.ydl_test.set_description(
            # "Imagine that you add some code to the end of the client")
        ptimer.add('app init')
        for x in ptimer.get():
            self.tapp_add('[PTimer] %s %s %s' % (x[1], x[2], x[0]))

        self.ids.sidebar.set_cursor_icons(
            'app_modules/behaviors/resizable/resize_horizontal.png',
            'app_modules/behaviors/resizable/resize2.png',
            'app_modules/behaviors/resizable/resize_vertical.png',
            'app_modules/behaviors/resizable/resize1.png',)
        try:
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
        global_callbacks.on_pause()
        return True

    def on_resume(self):
        self.app_rt.service.SERVICEconnect()
        global_callbacks.on_resume()

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
        sleep(0.1)
        osc.dontListen()


global_callbacks = Global_Callbacks()
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
            JotubeApp.stop_static('')
