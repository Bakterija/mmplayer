from kivy.properties import StringProperty, DictProperty, ListProperty
from kivy.properties import NumericProperty, BooleanProperty
from kivy_soil.app_recycleview import AppRecycleView, AppRecycleBoxLayout
from kivy_soil.app_recycleview import AppRecycleViewClass
from kivy_soil.kb_system.canvas import FocusBehaviorCanvas
from kivy_soil.hover_behavior import HoverBehavior
from utils import not_implemented, seconds_to_minutes_hours
from popups_and_dialogs.media_properties import MediaPropertiesDialog
from popups_and_dialogs import media_context_menu
from kivy.uix.behaviors import ButtonBehavior
from behaviors.button2 import ButtonBehavior2
from kivy.uix.stacklayout import StackLayout
from kivy.clock import Clock, mainthread
from kivy_soil.kb_system import keys
from kivy.utils import platform
from kivy.logger import Logger
from kivy.lang import Builder
from kivy.metrics import cm
import media_info


class MediaButton(ButtonBehavior2, HoverBehavior, AppRecycleViewClass,
                  StackLayout):
    '''Base view class of media buttons'''
    id = NumericProperty(-1)
    background_color = ListProperty([0.2, 0.2, 0.2, 1])
    state = StringProperty('normal')
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

    def __init__(self, **kwargs):
        super(MediaButton, self).__init__(**kwargs)
        for x in ('state', 'hovering', 'background_normal'
                  'background_playing', 'background_hover',
                  'background_selected', 'background_error',
                  'background_disabled',):
            self.fbind(x, self.update_bg_color)
        self.update_bg_color()

    def refresh_view_attrs(self, rv, index, data):
        super(MediaButton, self).refresh_view_attrs(rv, index, data)
        if self.path not in media_info.cache:
            media_info.get_info_async(self.path)
            self.update_media_info(None)
        else:
            self.update_media_info(media_info.cache[self.path])

    def on_duration(self, _, value):
        self.duration_readable = seconds_to_minutes_hours(value)

    def update_media_info(self, info):
        '''Sets self.is_video, duration, tags from info dict'''
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

    def update_bg_color(self, *args):
        if self.hovering and self.state != 'playing':
            self.background_color = self.background_hover
        else:
            cl = getattr(self, 'background_%s' % (self.state))
            self.background_color = cl

    def open_properties_dialog(self, *args):
        '''Opens MediaPropertiesDialog with own media information'''
        dialog = MediaPropertiesDialog.open_diag(self.rv.data[self.index])


class MediaRecycleviewBase(FocusBehaviorCanvas, AppRecycleView):
    '''Base recycleview of queue and playlist recycleview'''
    grab_keys = [keys.SPACE]
    mcontrol = None

    def __init__(self, **kwargs):
        super(MediaRecycleviewBase, self).__init__(**kwargs)
        self.ids.box.context_menu_function = self.context_menu_function
        self.filter_keys = ['name']

    def context_menu_function(self, widget, index, pos):
        media_context_menu.open_menu(self, widget, index, pos)

    def get_selected_data(self):
        '''Returns list with data dicts that contain selected data'''
        return [self.data[i] for i in self.children[0].selected_widgets]

    def update_data_from_filter(self, *args):
        '''Schedules self.log_data_update on next frame,
        then calls super method'''
        Clock.schedule_once(self.log_data_update, 0)
        super(MediaRecycleviewBase, self).update_data_from_filter()

    def log_data_update(self, dt):
        '''Logs performance of data update'''
        Logger.info('{}: loaded {} item playlist in {} sec'.format(
            self.__class__.__name__, len(self.data), round(dt, 3)))

    def remove_selected(self):
        '''Stub method, updated in subclasses'''
        pass

    def on_kb_return(self):
        '''Starts selected media'''
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
        '''Finds dict in list where state == 'playing',
        returns -1 if not found'''
        for i, x in enumerate(self.data):
            if x['state'] == 'playing':
                return i
        return -1

    def find_view_with_path(self, path):
        '''Finds child that has path from argument,
        returns nothing if not found'''
        for x in self.children[0].children:
            if x.path == path:
                return x


if platform == 'android':
    Builder.load_file('media_controller/controller.kv')
else:
    Builder.load_file('media_controller/controller.kv')
