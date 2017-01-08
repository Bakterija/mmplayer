from __future__ import print_function
from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.utils import platform
from kivy.lang import Builder
from kivy.metrics import dp, cm
from app_modules.multi_line_button import MultiLineButton
from app_modules.widgets.background_stacklayout import BackgroundStackLayout
from kivy.uix.filechooser import FileSystemLocal
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import (BooleanProperty, StringProperty, DictProperty,
                             ListProperty, NumericProperty)
from kivy.uix.recycleview import RecycleView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.behaviors.focus import FocusBehavior
from kivy.animation import Animation
from app_modules.behaviors.hover_behavior import HoverBehavior
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.modalview import ModalView
import kivy.uix.filechooser as filechooser
##from plyer.facades import FileChooser as FileChooser2
##from plyer.platforms.linux.filechooser import instance as FileChooser3
from fileadder_dialog import FileAdderDialog
from app_modules.widgets.section import rvSection
from sys import path
from time import time
import various_functions as various
import traceback
import os


class ProjectsRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    pass


class Media_Button(HoverBehavior, RecycleDataViewBehavior, ButtonBehavior, StackLayout):
    index = None  # stores our index
    bg_colors = DictProperty()
    pstate = StringProperty()
    mtype = StringProperty()
    text = StringProperty()
    name = StringProperty()
    path = StringProperty()
    bg_color = ListProperty()
    def __init__(self, **kwargs):
        super(Media_Button, self).__init__(**kwargs)

    def refresh_view_attrs(self, rv, index, data):
        super(Media_Button, self).refresh_view_attrs(rv, index, data)
        self.index = index
        self.hovering = False
        self.set_bg_color()

    def set_bg_color(self, *args):
        if self.hovering == True and self.pstate != 'playing':
            self.bg_color = self.bg_colors['hover']
        else:
            if self.mtype == 'media':
                self.bg_color = self.bg_colors[self.pstate]
            elif self.mtype == 'folder':
                self.bg_color = self.bg_colors['folder']
            elif self.mtype == 'disabled':
                self.bg_color = self.bg_colors['folder']

    def on_enter(self, *args):
        if self.pstate != 'playing':
            self.set_bg_color()

    def on_leave(self, *args):
        if self.pstate != 'playing':
            self.set_bg_color()


class MRV_Base(RecycleView):
    pass


class Media_GUI(StackLayout):
    rv_playlist = None
    rv_queue = None
    playlists = {}
    on_playlists = []
    places = ListProperty([])
    queue = ListProperty([])
    playing_name = StringProperty('')
    playing_path = StringProperty('')
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
        try:
            super(Media_GUI, self).__init__(**kwargs)
            self.mPlayer = mplayer
            self.mPlayer.set_gui_update_callback(self.gui_update)
            self.mPlayer.modes['on_video'].append(self.video_show)
            self.skip_seek, self.seek_lock = 0, 0
            self.recicler = self.rv_playlist
            self.recicler_queue = self.rv_queue
            self.reset_playlists()
            Clock.schedule_interval(self.update_seek, 0.2)
            # def testinj(*a):
            #     print(self.mPlayer.get_state_all())
            # Clock.schedule_interval(testinj, 1)
        except:
            traceback.print_exc()

    def start_playlist(self, name, path, index, btn):
        self.mPlayer.playlist.reset()
        self.queue = []
        self.mPlayer.playlist.add(name, path)
        x = self.rv_playlist.data[index]
        self.queue.append({
            'text': x['name'], 'name': x['name'], 'path': x['path'], 'mgui': self,
            'mtype': x['mtype'], 'pstate': x['pstate']
        })
        stat = self.mPlayer.start(0)
        if stat:
            for x in self.rv_playlist.data[index+1:]:
                self.mPlayer.playlist.add(x['name'],x['path'])
                nm = {
                    'text': x['name'], 'name': x['name'], 'path': x['path'], 'mgui': self,
                    'mtype': x['mtype'], 'pstate': x['pstate']
                }
                self.queue.append(nm)

    def start_queue(self, index):
        stat = self.mPlayer.start(str(index))

    def insert_queue(self, name, path, index):
        current = self.mPlayer.playlist.get_current()
        if index == 'Next':
            if current is None:
                index = 0
            else:
                index = current[0] + 1
        elif index == 'End':
            index = len(self.mPlayer.playlist.list) + 1
        elif index == 'Beginning':
            index = 0
        self.mPlayer.playlist.insert(index, name, path)
        self.queue.insert(index, {
            'text': name, 'name': name, 'path': path, 'mgui': self,
            'mtype': 'media', 'pstate': 'default'
        })

    def play_pause(self):
        state = self.mPlayer.get_state()
        if state in ('pause', 'stop'):
            self.mPlayer.play()
        else:
            self.mPlayer.pause()

    def play_next(self):
        self.mPlayer.next()

    def play_previous(self):
        self.mPlayer.previous()

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

    def refresh_rview_playlist(self):
        self.rv_playlist.refresh_from_data()

    def refresh_rview_queue(self):
        self.rv_queue.refresh_from_data()

    def gui_update(self, *args, **kwargs):
        if kwargs:
            name = kwargs['name']
            path = kwargs['path']
            for i, x in enumerate(self.rv_playlist.data):
                if x['name'] == name and x['path'] == path:
                    self.rv_playlist.data[i]['pstate'] = 'playing'
                elif x['pstate'] == 'playing':
                    self.rv_playlist.data[i]['pstate'] = 'default'
            for i, x in enumerate(self.rv_queue.data):
                if x['name'] == name and x['path'] == path:
                    self.rv_queue.data[i]['pstate'] = 'playing'
                elif x['pstate'] == 'playing':
                    self.rv_queue.data[i]['pstate'] = 'default'
            self.refresh_rview_playlist()
            self.refresh_rview_queue()

    def update_seek(self,*arg):
        self.playing_seek_value = self.mPlayer.get_mediaPos()
        self.playing_seek_max = self.mPlayer.get_mediaDur()

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
        self.mPlayer.modes['on_start'].append(self.video_hide)
        self.playing_video = True

    def video_hide(self):
        if self.videoframe:
            self.videoframe.clear_widgets()
        if self.videoframe_small:
            self.videoframe_small.clear_widgets()
            self.videoframe_small.animate_out()
        self.mPlayer.modes['on_start'].remove(self.video_hide)
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
            self.create_playlist(inp.text)
            frame.dismiss()
        try:
            frame = Popup(title='Type playlist name', size_hint=(1,None),height=cm(4),
                          content=StackLayout(size_hint=(1,1)))
            inp = TextInput(multiline=False, on_text_validate= validate, size_hint=(1, None), height=cm(1))
            cancel = Button(text='Cancel', on_press=frame.dismiss, size_hint=(0.5, None), height=cm(1))
            ok = Button(text='Create', on_press=validate, size_hint=(0.5, None), height=cm(1))
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
                        'path': item['path'], 'mgui': self,
                        'mtype': 'media', 'pstate': 'default'
                    })
            else:
                for item in plist:
                    target['files'].insert(index, {
                        'text': item['text'], 'name': item['text'],
                        'path': item['path'], 'mgui': self,
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
            size_hint=(1, None), height=cm(1))
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
        files = []
        self.playlists = various.get_playlists()
        for section in self.playlists:
            for item in section:
                nm = {
                    'text': item['name'], 'name': item['name'],
                    'path': item['path'], 'mgui': self,
                    'mtype': 'folder', 'pstate': 'default',
                    'dictio': item, 'section': item['section'],
                }
                files.append(nm)
        self.active_playlist = {
            'section': '',
            'files': files,
            'name': '',
            'path': ''
        }

        if self.rv_playlist:
            self.rv_playlist.on_playlist(self.active_playlist)
        for x in self.on_playlists:
            x(self, self.playlists)

    def open_playlist(self, target):
        try:
            files = []
            if target['method'] == 'folder_loader':
                files2 = various.get_files(target['path'])
                for name, path in files2:
                    files.append({
                        'text': name, 'name': name,
                        'path': path, 'mgui': self,
                        'mtype': 'media', 'pstate': 'default'
                    })
            elif target['method'] == 'json_loader':
                files2 = various.json_loader(target['path'])
                if files2:
                    for v in files2['items']:
                        files.append({
                            'text': v['name'], 'name': v['name'],
                            'path': v['path'], 'mgui': self,
                            'mtype': 'media', 'pstate': 'default'
                        })

            #Empty
            if not files2:
                files.append({
                    'text': 'Playlist is empty', 'name': '',
                    'path': '', 'mgui': self,
                    'mtype': 'disabled', 'pstate': 'default'
                })

            self.active_playlist = {
                'section': target['section'],
                'files': files,
                'name': target['name'],
                'path': target['path']
            }

            self.refresh_rview_playlist()
            if self.rv_playlist:
                self.rv_playlist.on_playlist(self.active_playlist)
            self.mPlayer._gui_update()
        except IOError:
            self.reset_playlists()
        except Exception as e:
            traceback.print_exc()

    def bind_on_playlists(self, func):
        self.on_playlists.append(func)


if platform == 'android':
    Builder.load_file(path[0]+'/app_modules/media_gui/media_gui.kv')
else:
    Builder.load_file(path[0]+'/app_modules/media_gui/media_gui.kv')
