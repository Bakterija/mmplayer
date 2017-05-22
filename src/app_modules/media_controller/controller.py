from __future__ import print_function
from kivy.uix.widget import Widget
from kivy.uix.stacklayout import StackLayout
# from kivy.utils import platform
# from kivy.lang import Builder
from app_modules.widgets_standalone.background_stacklayout import BackgroundStackLayout
from kivy.uix.textinput import TextInput
from kivy.metrics import cm, dp
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import (
    BooleanProperty, StringProperty, DictProperty,
    ListProperty, NumericProperty, ObjectProperty)
from kivy.clock import Clock
from kivy.core.window import Window
# import kivy.uix.filechooser as filechooser
##from plyer.facades import FileChooser as FileChooser2
##from plyer.platforms.linux.filechooser import instance as FileChooser3
# from .fileadder_dialog import FileAdderDialog
from app_modules.widgets_integrated.section import rvSection
# from . import various_functions as various
from . import playlist_loader
from .playlist_loader.base import BasePlaylist
from kivy.logger import Logger
import traceback
import global_vars as gvars
from time import time
import media_info
# from app_modules.rv_sidebar.ctx_menu import open_sidebar_ctx_menu


class MediaController(Widget):
    playlists = DictProperty()
    cur_played_playlist = ObjectProperty()
    cur_viewed_playlist = ObjectProperty()
    # cur_queue = ListProperty()

    playing_name = StringProperty()
    playing_path = StringProperty()
    playing_seek_value = NumericProperty(0)
    playing_seek_max = NumericProperty(0)
    playing_id = NumericProperty()
    playing_state = StringProperty()
    last_media = None

    windowpopup = None
    videoframe = None
    videoframe_is_visible = BooleanProperty(False)
    videoframe_small = None
    playing_video = BooleanProperty(False)

    def __init__(self, mplayer, **kwargs):
        super(MediaController, self).__init__(**kwargs)
        self.mplayer = mplayer
        self.mplayer.bind(on_start=self.on_mplayer_start)
        self.mplayer.bind(on_video=self.on_mplayer_video)
        self.skip_seek, self.seek_lock = 0, 0
        # self.reset_playlists()
        Clock.schedule_interval(self.update_seek, 0.1)
        media_info.info_update_callback = self.on_media_info_update
        Clock.schedule_once(lambda *a: media_info.start_workers(2), 1)

    def on_mplayer_start(self):
        state = self.mplayer.get_state_all()
        media = state['cur_media']
        if self.last_media:
            if self.last_media['state'] == 'playing':
                self.last_media['state'] = 'default'

        if 'id' in media:
            index = media['id']
            self.playing_id = index
            if self.cur_played_playlist:
                self.cur_played_playlist.set_playing(index)
            else:
                media['state'] = 'playing'
        else:
            self.playing_id = -9
            if self.cur_played_playlist:
                self.cur_played_playlist.remove_playing()
            media['state'] = 'playing'

        self.playing_name = media['name']
        self.playing_path = media['path']
        self.last_media = media
        self.refresh_playlist_view()
        self.refresh_queue_view()

    def on_mplayer_video(self, value, player=None):
        if value:
            self.playing_video = True
        else:
            self.playing_video = False

    def on_playlist_media(self, playlist, media):
        if playlist.path == self.cur_viewed_playlist.path:
            self.view_playlist.update_data()

    def attach_playlist_view(self, widget):
        self.view_playlist = widget
        widget.mcontrol = self
        self.bind(cur_viewed_playlist=widget.set_viewed_playlist)

    def attach_queue_view(self, widget):
        self.view_queue = widget
        widget.mcontrol = self

    def start_playlist_from_index(self, name, path, index, id, btn):
        '''Triggered when user touches a MediaButton in playlist'''
        self.mplayer.reset()
        self.cur_played_playlist = self.cur_viewed_playlist
        new_queue = list(self.view_playlist.data[index:])
        self.mplayer.queue = new_queue
        self.view_queue.set_data(new_queue)
        stat = self.mplayer.start(0)

    def start_queue(self, index):
        '''Triggered when user touches a MediaButton in queue'''
        stat = self.mplayer.start(index)

    def start_selection(self, new_queue, cur_playlist=None):
        self.mplayer.reset()
        if cur_playlist:
            self.cur_played_playlist = cur_playlist
        self.mplayer.queue = new_queue
        self.view_queue.set_data(new_queue)
        self.start_queue(0)

    def add_to_queue(self, new_media):
        new_queue = self.mplayer.queue + new_media
        self.mplayer.queue = new_queue
        self.view_queue.set_data(new_queue)

    def queue_remove_indexes(self, index_list):
        for x in reversed(index_list):
            del self.mplayer.queue[x]
        self.view_queue.set_data(self.mplayer.queue)
        Logger.info('MediaController: removed %s files from queue' % (
            len(index_list)))

    def clear_queue(self, *args):
        self.mplayer.reset()
        self.view_queue.clear_data()

    def play_pause(self):
        state = self.mplayer.get_state()
        if state in ('pause', 'stop'):
            self.mplayer.play()
        else:
            self.mplayer.pause()

    def play_next(self):
        self.mplayer.next()

    def play_previous(self):
        self.mplayer.previous()

    def jump_to_current_index(self, screen):
        Logger.info('MediaController: jump_to_current_index(%s)' % (screen))
        if screen == 'playlist':
            pl = self.view_playlist
        elif screen == 'queue':
            pl = self.view_queue

        index = self.find_playing(pl.data)
        if index is not None:
            pl.scroll_to_index(index)
            pl.children[0].select_with_touch(index)
            Logger.info('MediaController: jumping to index %s' % (index))
        else:
            Logger.info('MediaController: played index is not in view')

    @staticmethod
    def find_playing(playlist):
        for i, x in enumerate(playlist):
            if x['state'] == 'playing':
                return i

    def refresh_playlist_view(self):
        self.view_playlist.refresh_from_data()

    def refresh_queue_view(self):
        self.view_queue.refresh_from_data()

    def update_seek(self, *arg):
        pos = self.mplayer.get_mediaPos()
        dur = self.mplayer.get_mediaDur()
        self.playing_state = self.mplayer.get_state()
        if pos == -1:
            self.playing_seek_value = 0
        else:
            self.playing_seek_value = pos
        if dur == -1:
            self.playing_seek_max = 0
        else:
            self.playing_seek_max = dur

    def on_video_resize(self, size):
        if self.playing_video:
            if self.videoframe and self.videoframe_is_visible:
                self.videoframe.children[0].size = size

    def on_playing_video(self, _, value):
        if not self.videoframe_small:
            Logger.error(''.join((
                'MediaController: on_playing_video:',
                'videoframe_small is None')))
        else:
            if value:
                self.video_show(self.mplayer.video_widget)
            else:
                self.video_hide()

    def video_show(self, widget):
        if self.videoframe and self.videoframe_is_visible:
            self.videoframe.add_widget(widget)
        else:
            self.videoframe_small.add_widget(widget)
            self.videoframe_small.animate_in()

    def video_hide(self):
        if self.videoframe:
            self.videoframe.clear_widgets()
        if self.videoframe_small:
            self.videoframe_small.clear_widgets()
            self.videoframe_small.animate_out()

    def on_videoframe_is_visible(self, obj, val):
        if val:
            if self.videoframe_small.children:
                temp = self.videoframe_small.children[0]
                self.videoframe_small.remove_widget(temp)
                self.videoframe.add_widget(temp)
                self.videoframe_small.animate_out()
                temp.pos = (0, 0)
        elif self.videoframe.children and self.playing_video:
            temp = self.videoframe.children[0]
            self.videoframe.remove_widget(temp)
            self.videoframe_small.add_widget(temp)
            self.videoframe_small.animate_in()

    def create_playlist_popup(self, *arg):
        def validate(button):
            if inp.text:
                self.create_playlist(inp.text)
            frame.dismiss()
        try:
            frame = Popup(
                title='Type playlist name', size_hint=(1,None),
                height=cm(4), content=StackLayout())
            inp = TextInput(
                multiline=False, on_text_validate= validate,
                size_hint=(1, None), height=gvars.button_height)
            cancel = Button(
                text='Cancel', on_press=frame.dismiss,
                size_hint=(0.5, None), height=gvars.button_height)
            ok = Button(
                text='Create', on_press=validate,
                size_hint=(0.5, None), height=gvars.button_height)
            inp.focus = True
            for x in (inp, cancel, ok):
                frame.content.add_widget(x)
            frame.open()
        except:
            traceback.print_exc()

    def on_dropfile(self, path, mouse_pos=None, playlist=None):
        Logger.info(
            '{}: on_dropfile: path:{} mouse_pos:{} playlist:{}'.format(
                self.__class__.__name__, path, mouse_pos, playlist))

        found = False
        if playlist:
            if playlist == 'playlist':
                if self.cur_viewed_playlist:
                    self.cur_viewed_playlist.add_path(path)
                    found = True
            elif playlist == 'queue':
                pl = BasePlaylist()
                new_media = pl.get_files(path)
                self.add_to_queue(new_media)
                found = True

        if not found:
            Logger.warning('{}: no playlist selected'.format(
                self.__class__.__name__))

    def playlist_cmenu_popup(self, widget, dictio):
        open_sidebar_ctx_menu(widget)
        # def validate(button):
        #     section = dictio['section']
        #     name = dictio['name']
        #     self.remove_playlist(name, section)
        #     remove_windowpopup()
        # def remove_windowpopup(*args):
        #     if self.windowpopup:
        #         Window.remove_widget(self.windowpopup)
        #         self.windowpopup = None
        # remove_windowpopup()
        #
        # frame = BackgroundStackLayout(size_hint=(None, None), width=cm(3),
        #                               background_color=(0.1, 0.1, 0.1, 0.9),
        #                               height=cm(4), pos=(Window.mouse_pos))
        # Window.add_widget(frame)
        # Clock.schedule_once(lambda x: setattr(frame, 'pos', self.to_window(
        #     Window.mouse_pos[0], Window.mouse_pos[1])), 0)
        #
        # section = rvSection(text='CMENU')
        # remove = Button(
        #     text='Remove playlist', on_press=lambda x: validate(x),
        #     size_hint=(1, None), height=gvars.button_height)
        # for x in (section, remove):
        #     frame.add_widget(x)
        # frame.bind(on_touch_up=lambda *args: remove_windowpopup())
        # self.windowpopup = frame

    def create_playlist(self, name):
        playlist_loader.create_playlist(name)
        self.reset_playlists()

    def remove_playlist(self, name, section):
        for x in self.playlists[section]:
            if x.name == name:
                x.remove()
        self.reset_playlists()

    def reset_playlists(self, *args):
        time0 = time()
        self.playlist_ids = {}
        pl = playlist_loader.load_from_directories((
            'media/playlists/', gvars.DIR_PLAYLISTS))
        self.playlists = pl
        for section, playlists in self.playlists.items():
            for x in playlists:
                x.bind(media=self.on_playlist_media)
                self.playlist_ids[x.id] = x
        Logger.info(
            'MediaController: reset_playlists: %s sec' % (time() - time0))

    def open_playlist(self, target):
        for section, playlists in self.playlists.items():
            for instance in playlists:
                if target['path'] == instance.path:
                    self.cur_viewed_playlist = instance
                    # TODO Disable for now, add config setting later
                    # Clock.schedule_once(self.view_playlist.focus_widget, 0.2)
                    return

        Logger.warning('MediaController: playlist not found')

    def open_playlist_by_id(self, id):
        if id in self.playlist_ids:
            print('open ids playlist', id)
            pl = self.playlist_ids[id]
            target = {'name': pl.name, 'path': pl.path}
            self.open_playlist(target)
        else:
            print('playlist not in ids', id, self.playlist_ids)

    def on_media_info_update(self, path, info):
        pl = self.view_playlist.find_view_with_path(path)
        que = self.view_queue.find_view_with_path(path)
        if pl:
            pl.update_media_info(info)
        if que:
            que.update_media_info(info)
