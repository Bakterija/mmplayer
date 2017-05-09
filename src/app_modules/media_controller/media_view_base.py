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
from kivy.uix.stacklayout import StackLayout
from kivy.lang import Builder
from kivy.utils import platform
from kivy.metrics import cm
from app_modules import keys
from kivy.clock import Clock


class MediaButton(HoverBehavior, AppRecycleViewClass, RecycleDataViewBehavior,
                  ButtonBehavior, StackLayout):
    index = NumericProperty(-1)
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
        if value:
            self.hovering = True
        else:
            self.hovering = False
        self.set_bg_color()

class MediaRecycleviewBase(FocusBehaviorCanvas, AppRecycleView):
    def on_kb_return(self):
        box = self.children[0]
        if box.sel_first != -1:
            for x in box.children:
                if x.index == box.sel_first:
                    x.on_release()

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
            elif key == 1073741942:
                box.open_context_menu()
            elif key == keys.PAGE_UP:
                self.page_up()
            elif key == keys.PAGE_DOWN:
                self.page_down()
        elif modifier == ['ctrl']:
            if key == 97:
                self.select_all()
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


if platform == 'android':
    Builder.load_file('app_modules/media_controller/controller.kv')
else:
    Builder.load_file('app_modules/media_controller/controller.kv')
