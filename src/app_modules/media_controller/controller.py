from __future__ import print_function
from kivy.uix.widget import Widget
from kivy.uix.stacklayout import StackLayout
from kivy.utils import platform
from kivy.lang import Builder
from app_modules.widgets_standalone.background_stacklayout import BackgroundStackLayout
from kivy.uix.textinput import TextInput
from kivy.metrics import cm, dp
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import (BooleanProperty, StringProperty, DictProperty,
                             ListProperty, NumericProperty)
from kivy.clock import Clock
from kivy.core.window import Window
import kivy.uix.filechooser as filechooser
##from plyer.facades import FileChooser as FileChooser2
##from plyer.platforms.linux.filechooser import instance as FileChooser3
from .fileadder_dialog import FileAdderDialog
from app_modules.widgets_integrated.section import rvSection
from . import various_functions as various
from . import playlist_loader
import traceback
import global_vars as gvars


class MediaController(Widget):
    playlists = DictProperty()

    cur_played_playlist = ListProperty(['', '', None])
    '''ListProperty of [section, name, instance]'''

    cur_viewed_playlist = ListProperty(['', '', None])
    '''ListProperty of [section, name, instance]'''

    cur_queue = ListProperty()

    playing_name = StringProperty()
    playing_path = StringProperty()
    playing_seek_value = NumericProperty(0)
    playing_seek_max = NumericProperty(0)

    adding_files = False
    current_screen = ''
    windowpopup = None
    videoframe = None
    videoframe_is_visible = BooleanProperty(False)
    videoframe_small = None
    playing_video = BooleanProperty(False)

    def __init__(self, mplayer, **kwargs):
        super(MediaController, self).__init__(**kwargs)
        self.mplayer = mplayer
        self.mplayer.bind(on_start=self.on_mplayer_start)
        self.mplayer.bind(on_video=self.video_show)
        self.skip_seek, self.seek_lock = 0, 0
        self.reset_playlists()
        Clock.schedule_interval(self.update_seek, 0.1)

    def on_mplayer_start(self):
        state = self.mplayer.get_state_all()
        index = state['cur_media']['index']
        self.cur_played_playlist[2].set_playing(index)
        self.cur_queue = self.cur_played_playlist[2].media
        self.view_queue.set_data(self.cur_queue)
        self.refresh_playlist_view()
        self.refresh_queue_view()

    def attach_playlist_view(self, widget):
        self.view_playlist = widget
        widget.mcontrol = self
        self.bind(cur_viewed_playlist=widget.set_viewed_playlist)

    def attach_queue_view(self, widget):
        self.view_queue = widget
        widget.mcontrol = self

    def start_playlist(self, name, path, index, btn):
        '''Triggered when user touches a MediaButton in playlist'''
        self.mplayer.reset()
        self.cur_played_playlist = self.cur_viewed_playlist
        self.mplayer.queue = self.cur_played_playlist[2].media
        self.view_queue.set_data(self.mplayer.queue)
        self.refresh_queue_view()
        stat = self.mplayer.start(index)

    def start_queue(self, index):
        '''Triggered when user touches a MediaButton in queue'''
        stat = self.mplayer.start(str(index))

    def insert_queue(self, name, path, index):
        current = self.mplayer.playlist.get_current()
        if index == 'Next':
            if current is None:
                index = 0
            else:
                index = current[0] + 1
        elif index == 'End':
            index = len(self.mplayer.playlist.list) + 1
        elif index == 'Beginning':
            index = 0
        self.mplayer.playlist.insert(index, name, path)
        self.queue.insert(index, {
            'text': name, 'name': name, 'path': path,
            'mtype': 'media', 'pstate': 'default'
        })

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

    def set_media_labels(self, string):
        def resizer_clock(*arg):
            label = lbl
            ratio = float(label.size[0]) / float(label.texture_size[0])
            if ratio < 1:
                lentext = len(label.text)
                will_remove = lentext-int(float(lentext) * float(ratio)) + 4
                templist = list(label.text)
                while will_remove:
                    del templist[int(len(templist) * 0.8)]
                    will_remove -= 1
                templist.insert(int(len(templist) * 0.8) , '...')
                label.text = ''.join(templist)

        lbl = self.ids.media_label
        lbl.text = string
        Clock.schedule_once(resizer_clock, 0)

    def refresh_playlist_view(self):
        self.view_playlist.refresh_from_data()

    def refresh_queue_view(self):
        self.view_queue.refresh_from_data()

    def update_seek(self, *arg):
        pos = self.mplayer.get_mediaPos()
        dur = self.mplayer.get_mediaDur()
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

    def video_show(self, widget):
        if self.videoframe and self.videoframe_is_visible:
            self.videoframe.add_widget(widget)
        else:
            self.videoframe_small.add_widget(widget)
            self.videoframe_small.animate_in()
        self.mplayer.bind(on_start=self.video_hide)
        self.playing_video = True

    def video_hide(self):
        if self.videoframe:
            self.videoframe.clear_widgets()
        if self.videoframe_small:
            self.videoframe_small.clear_widgets()
            self.videoframe_small.animate_out()
        self.mplayer.unbind(on_start=self.video_hide)
        self.playing_video = False

    def on_videoframe_is_visible(self, obj, val):
        if val:
            if self.videoframe_small.children:
                temp = self.videoframe_small.children[0]
                self.videoframe_small.remove_widget(temp)
                self.videoframe.add_widget(temp)
                self.videoframe_small.animate_out()
                temp.pos = (0, 0)
        elif self.videoframe.children and self.playing_video:
            # if self.videoframe.children[0].children:
            temp = self.videoframe.children[0]
            self.videoframe.remove_widget(temp)
            self.videoframe_small.add_widget(temp)
            self.videoframe_small.animate_in()

    def create_playlist_popup(self, *arg):
        def validate(button):
            if inp.text:
                playlist_loader.create_playlist(inp.text)
            frame.dismiss()
            self.reset_playlists()
        try:
            frame = Popup(
                title='Type playlist name', size_hint=(1,None), height=cm(4),
                content=StackLayout())
            inp = TextInput(multiline=False, on_text_validate= validate, size_hint=(1, None), height=gvars.button_height)
            cancel = Button(text='Cancel', on_press=frame.dismiss, size_hint=(0.5, None), height=gvars.button_height)
            ok = Button(text='Create', on_press=validate, size_hint=(0.5, None), height=gvars.button_height)
            inp.focus = True
            for x in (inp, cancel, ok):
                frame.content.add_widget(x)
            frame.open()
        except:
            traceback.print_exc()

    def on_dropfile(self, path):
        paths = various.get_files(path)
        if paths:
            for path in paths:
                if self.adding_files:
                    self.fdiag.add_file(path[1])
                else:
                    self.add_local_files_popup(path[1])
        else:
            if self.adding_files:
                self.fdiag.add_file(path)
            else:
                self.add_local_files_popup(path)

    def add_files(self, target, index, plist):
        target2 = target
        found = False
        if index == 'Beginning':
            index = 0
        if target[:7] == 'Current':
            if self.current_screen == 'sc-queue':
                for item in plist:
                    self.insert_queue(item['text'], item['path'], index)
                return
        for i, x in enumerate(self.playlists[1]):
            if target[:7] == 'Current':
                if x['name'] == self.active_playlist['name']:
                    if x['path'] == self.active_playlist['path']:
                        target = self.playlists[1][i]
                        found = True
                        break
            else:
                if x['name'] == target:
                    target = self.playlists[1][i]
                    found = True
                    break
        if found:
            if index == 'Next':
                index = len(target['files'])
                for i, x in enumerate(target['files']):
                    if x['pstate'] == 'playing':
                        index = i
            elif index == 'End':
                index = len(target['files'])
            if target2 == 'Current':
                for item in plist:
                    target['files'].insert(index, {
                        'text': item['text'], 'name': item['text'],
                        'path': item['path'],
                        'mtype': 'media', 'pstate': 'default'
                    })
            else:
                for item in plist:
                    target['files'].insert(index, {
                        'text': item['text'], 'name': item['text'],
                        'path': item['path'],
                        'mtype': 'media', 'pstate': 'default'
                    })
            if target['name'] == self.active_playlist['name']:
                if target['path'] == self.active_playlist['path']:
                    if self.rv_playlist:
                        self.rv_playlist.on_playlist(target)
            various.save_playlist(target['path'], target['files'])

    def add_local_files_popup(self, path):
        self.adding_files = True
        plist_arg = [i['name'] for i in self.playlists[1]]
        plist_arg.insert(0, 'Current ' + self.current_screen)
        plist_arg.insert(1, 'Queue')
        self.fdiag = FileAdderDialog(plist_arg, self.add_files)
        self.fdiag.bind(on_dismiss=lambda *args: setattr(self, 'adding_files', False))
        self.fdiag.open()
        self.fdiag.add_file(path)

    def add_local_files_popup2(self, *args):
        from app_modules import filechooser22
        try:
            # self.eemo = FileChooser3()
            # aa = self.eemo.open_file()
            self.ee = filechooser22.instance()
            aa = self.ee._file_selection_dialog(mode = 'filename')
        except Exception as e:
            traceback.print_exc()

    def playlist_cmenu_popup(self, dictio):
        def validate(button):
            self.remove_playlist(
            dictio['name'], dictio['path'], dictio['section'])
            remove_windowpopup()
        def remove_windowpopup(*args):
            if self.windowpopup:
                Window.remove_widget(self.windowpopup)
                self.windowpopup = None
        remove_windowpopup()

        frame = BackgroundStackLayout(size_hint=(None, None), width=cm(3),
                                      background_color=(0.1, 0.1, 0.1, 0.9),
                                      height=cm(4), pos=(Window.mouse_pos))
        Window.add_widget(frame)
        Clock.schedule_once(lambda x: setattr(frame, 'pos', self.to_window(
            Window.mouse_pos[0], Window.mouse_pos[1])), 0)

        section = rvSection(text='CMENU')
        remove = Button(
            text='Remove playlist', on_press=lambda x: validate(x),
            size_hint=(1, None), height=gvars.button_height)
        for x in (section, remove):
            frame.add_widget(x)
        frame.bind(on_touch_up=lambda *args: remove_windowpopup())
        self.windowpopup = frame

    def create_playlist(self, name):
        various.create_playlist(name)
        self.reset_playlists()

    def remove_playlist(self, name, path, section):
        various.remove_playlist(name, path, section)
        if path == self.active_playlist['path']:
            self.reset_playlists()

    def reset_playlists(self):
        self.playlist_ids = {}
        pl = playlist_loader.load_from_directories((
            'media/playlists/', gvars.DIR_PLAYLISTS))
        self.playlists = pl
        for section, playlists in self.playlists.items():
            for x in playlists:
                self.playlist_ids[x.id] = x

    def open_playlist(self, target):
        for section, playlists in self.playlists.items():
            for instance in playlists:
                if target['name'] == instance.name:
                    self.cur_viewed_playlist = [
                        section, instance.name, instance]
                    return

        Logger.warning('MediaController: playlist not found')

    def open_playlist_by_id(self, id):
        if id in self.playlist_ids:
            pl = self.playlist_ids[id]
            target = {'name': pl.name}
            self.open_playlist(target)
