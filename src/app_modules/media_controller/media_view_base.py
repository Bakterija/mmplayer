from kivy.properties import (
    StringProperty, DictProperty, ListProperty, NumericProperty)
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from app_modules.widgets_standalone.app_recycleview import AppRecycleView
from app_modules.widgets_standalone.app_recycleview import AppRecycleBoxLayout
from app_modules.widgets_standalone.app_recycleview import AppRecycleViewClass
from app_modules.behaviors.hover_behavior import HoverBehavior
from app_modules.behaviors.focus import FocusBehaviorCanvas
from kivy.uix.recycleview import RecycleView
from kivy.uix.behaviors import ButtonBehavior
from app_modules.behaviors.button2 import ButtonBehavior2
from kivy.uix.stacklayout import StackLayout
from kivy.lang import Builder
from kivy.utils import platform
from kivy.logger import Logger
from kivy.metrics import cm
from app_modules import keys
from kivy.clock import Clock
from utils import not_implemented


class MediaButton(ButtonBehavior2, HoverBehavior, AppRecycleViewClass,
                  RecycleDataViewBehavior, StackLayout):
    index = NumericProperty(-1)
    id = NumericProperty(-1)
    rv = None
    bg_colors = DictProperty()
    state = StringProperty('default')
    mtype = StringProperty('media')
    name = StringProperty()
    path = StringProperty()
    bg_color = ListProperty()

    def refresh_view_attrs(self, rv, index, data):
        super(MediaButton, self).refresh_view_attrs(rv, index, data)
        self.index = index
        self.hovering = False
        self.set_bg_color()
        if not self.rv:
            self.rv = rv

    def on_press(self, button, double_tap):
        if button == 'left':
            if double_tap:
                self.start_media()
            else:
                self.parent.select_with_touch(self.index)
        elif button == 'right':
            if not self.index in self.parent.selected_widgets:
                Clock.schedule_once(
                    lambda *a: self.parent.select_with_touch(self.index))
            self.open_context_menu()

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

    def open_context_menu(self, *args):
        not_implemented.show_error()


class MediaRecycleviewBase(FocusBehaviorCanvas, AppRecycleView):
    mcontrol = None

    def __init__(self, **kwargs):
        super(MediaRecycleviewBase, self).__init__(**kwargs)
        self.filter_keys = ['name']
        self.children[0].context_menu_function = self.open_ctx

    def get_selected_data(self):
        return [self.data[i] for i in self.children[0].selected_widgets]

    def open_ctx(self, widget, index, pos):
        widget.open_context_menu()

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
        if modifier == ['shift']:
            if key == keys.UP:
                box.on_arrow_up()
            elif key == keys.DOWN:
                box.on_arrow_down()
        if not modifier:
            if key == keys.UP:
                box.on_arrow_up()
            elif key == keys.DOWN:
                box.on_arrow_down()
            elif key == keys.RETURN:
                self.on_kb_return()
            elif key == keys.ENTER:
                self.on_kb_return()
            elif key == keys.MENU:
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
            if key == 97:
                box.select_all()
            elif key == 32:
                box.deselect_all()

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


if platform == 'android':
    Builder.load_file('app_modules/media_controller/controller.kv')
else:
    Builder.load_file('app_modules/media_controller/controller.kv')
