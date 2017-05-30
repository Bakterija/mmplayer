from kivy.properties import StringProperty, DictProperty, ListProperty
from kivy.properties import NumericProperty, BooleanProperty
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from widgets_standalone.app_recycleview import AppRecycleView
from widgets_standalone.app_recycleview import AppRecycleBoxLayout
from widgets_standalone.app_recycleview import AppRecycleViewClass
from behaviors.hover_behavior import HoverBehavior
from kb_system.canvas import FocusBehaviorCanvas
from kivy.uix.recycleview import RecycleView
from kivy.uix.behaviors import ButtonBehavior
from behaviors.button2 import ButtonBehavior2
from kivy.uix.stacklayout import StackLayout
from kivy.lang import Builder
from kivy.utils import platform
from kivy.logger import Logger
from kivy.metrics import cm
from kb_system import keys
from kivy.clock import Clock
from utils import not_implemented, seconds_to_minutes_hours
import media_info
from popups_and_dialogs import media_context_menu


class MediaButton(ButtonBehavior2, HoverBehavior, AppRecycleViewClass,
                  StackLayout):
    index = NumericProperty(-1)
    id = NumericProperty(-1)
    rv = None
    bg_colors = DictProperty()
    state = StringProperty('default')
    mtype = StringProperty('media')
    name = StringProperty()
    text = StringProperty()
    path = StringProperty()
    bg_color = ListProperty()
    in_mi = BooleanProperty(False)
    duration = NumericProperty(-1)
    duration_readable = StringProperty('')
    is_video = BooleanProperty(False)
    artist = StringProperty()
    title = StringProperty()
    album = StringProperty()
    genre = StringProperty()
    date = StringProperty()

    def refresh_view_attrs(self, rv, index, data):
        super(MediaButton, self).refresh_view_attrs(rv, index, data)
        self.hovering = False
        self.set_bg_color()
        if self.path not in media_info.cache:
            media_info.get_info_async(self.path)
            self.update_media_info(None)
        else:
            self.update_media_info(media_info.cache[self.path])

    def on_duration(self, _, value):
        self.duration_readable = seconds_to_minutes_hours(value)

    def update_media_info(self, info):
        if info:
            self.in_mi = True
            self.is_video = info['is_video']
            self.duration = info['duration']
            if 'format' in info:
                self.artist = info['format'].get('TAG:artist', '')
                self.title = info['format'].get('TAG:title', '')
                self.album = info['format'].get('TAG:album', '')
                self.genre = info['format'].get('TAG:genre', '')
                self.date = info['format'].get('TAG:date', '')
        else:
            if media_info.worker_state[self.path] == 'waiting':
                media_info.add_priority_path(self.path)
            self.in_mi = False
            self.is_video = False
            self.duration = -1
            self.artist = ''
            self.title = ''
            self.album = ''
            self.genre = ''
            self.date = ''
        if self.title and self.artist:
            self.text = ' - '.join((self.artist, self.title))
        elif self.title:
            self.text = self.title
        else:
            self.text = self.name

    def on_press(self, button, double_tap):
        if button == 'left':
            if double_tap:
                self.start_media()
            else:
                self.parent.select_with_touch(self.index)
        elif button == 'right':
            if not self.index in self.parent.selected_widgets:
                self.parent.select_with_touch(self.index)
            self.rv.ids.box.open_context_menu()

    def set_bg_color(self, *args):
        if self.hovering and self.state != 'playing':
            self.bg_color = self.bg_colors['hover']
        else:
            if self.mtype == 'media':
                self.bg_color = self.bg_colors[self.state]
            elif self.mtype == 'folder':
                self.bg_color = self.bg_colors['folder']
            elif self.mtype == 'disabled':
                self.bg_color = self.bg_colors['folder']

    def on_enter(self, *args):
        if self.state != 'playing':
            self.set_bg_color()

    def on_leave(self, *args):
        if self.state != 'playing':
            self.set_bg_color()

    def on_selected(self, _, value):
        self.set_bg_color()


class MediaRecycleviewBase(FocusBehaviorCanvas, AppRecycleView):
    grab_keys = [keys.SPACE]
    mcontrol = None

    def __init__(self, **kwargs):
        super(MediaRecycleviewBase, self).__init__(**kwargs)
        self.ids.box.context_menu_function = self.context_menu_function
        self.filter_keys = ['name']

    def context_menu_function(self, widget, index, pos):
        media_context_menu.open_menu(self, widget, index, pos)

    def get_selected_data(self):
        return [self.data[i] for i in self.children[0].selected_widgets]

    def update_data_from_filter(self, *args):
        Clock.schedule_once(self.log_data_update, 0)
        super(MediaRecycleviewBase, self).update_data_from_filter()

    def log_data_update(self, dt):
        Logger.info('{}: loaded {} item playlist in {} sec'.format(
            self.__class__.__name__, len(self.data), round(dt, 3)))

    def remove_selected(self):
        pass

    def on_kb_return(self):
        box = self.children[0]
        if box.sel_first != -1:
            for x in box.children:
                if x.index == box.sel_first:
                    x.start_media()

    def on_key_down(self, key, modifier):
        box = self.children[0]
        res = True
        if modifier == ['shift']:
            if key == keys.UP:
                box.on_arrow_up()
            elif key == keys.DOWN:
                box.on_arrow_down()
        elif not modifier:
            if key == keys.UP:
                box.on_arrow_up()
            elif key == keys.DOWN:
                box.on_arrow_down()
            elif key in (keys.ENTER, keys.RETURN):
                self.on_kb_return()
            elif key in (keys.MENU, keys.MENU_WIN):
                box.open_context_menu()
            elif key == keys.PAGE_UP:
                self.page_up()
            elif key == keys.PAGE_DOWN:
                self.page_down()
            elif key == keys.HOME:
                self.scroll_to_start()
            elif key == keys.END:
                self.scroll_to_end()
            elif key == keys.DEL:
                self.remove_selected()
        elif modifier == ['ctrl']:
            if key == keys.A:
                box.select_all()
            elif key == keys.SPACE:
                box.deselect_all()
                res = False
        return res
        # Clock.schedule_once(self.int_scroll_test, 0.1)

    def int_scroll_test(self, a):
        box = self.children[0]
        skrol0 = 1.0 - self.scroll_y
        wheight = box.default_size[1] + box.spacing
        dist = int((len(self.data) * wheight) * skrol0)

        skrol = 1.0 - self.convert_distance_to_scroll(0, dist)[1]
        self.scroll_y = skrol

    def find_playing(self):
        for i, x in enumerate(self.data):
            if x['state'] == 'playing':
                return i
        return -1

    def find_view_with_path(self, path):
        for x in self.children[0].children:
            if x.path == path:
                return x

if platform == 'android':
    Builder.load_file('media_controller/controller.kv')
else:
    Builder.load_file('media_controller/controller.kv')
