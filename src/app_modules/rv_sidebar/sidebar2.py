from kivy.uix.stacklayout import StackLayout
from kivy.utils import platform
from kivy.metrics import dp, cm
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import BooleanProperty, StringProperty, DictProperty
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from app_modules.kb_system.canvas import FocusBehaviorCanvas
from app_modules.widgets_standalone.app_recycleview import (
    AppRecycleBoxLayout, AppRecycleView, AppRecycleViewClass)
from kivy.uix.behaviors import ButtonBehavior
from .pc_sidebar_widgets import SideBarButton, SideBarSection
from kivy.clock import Clock
from app_modules.behaviors.hover_behavior import HoverBehavior
from app_modules.kb_system import keys as kb
import traceback
from time import time


kv = '''
<SideBarRecycleView>:
    viewclass: 'SideBarViewClass'
    SingleSelectBox:
        id: box
        orientation: 'vertical'
        size_hint: None, None
        height: self.minimum_height
        width: root.width - root.bar_width
        default_size_hint: 1, None
        default_size: None, None
        spacing: default_spacing
'''

class SideBarViewClass(HoverBehavior, AppRecycleViewClass,
                       ButtonBehavior, StackLayout):
    index = None
    text = StringProperty()
    wtype = StringProperty()
    children_initialised = False
    func = None
    func2 = None

    def __init__(self, **kwargs):
        super(SideBarViewClass, self).__init__(**kwargs)
        size_hint_y = None

    def on_selected(self, _, a):
        print (self.index, a)

    def init_children(self, *args):
        if self.wtype == 'text':
            self.lbl = SideBarButton(text=self.text)
            self.add_widget(self.lbl)
        elif self.wtype == 'section':
            self.lbl = SideBarSection(text=self.text)
            self.add_widget(self.lbl)
        elif self.wtype == 'separator':
            self.lbl = Label(text=self.text)
            self.add_widget(self.lbl)
        setattr(self, 'height', self.lbl.height)

    def update_kbhover(self, new_index):
        if self.index == new_index:
            self.lbl.hovering = True
        else:
            self.lbl.hovering = False

    def update_selection(self, new_index):
        if self.index == new_index:
            self.lbl.selected = True
        else:
            self.lbl.selected = False

    def on_text(self, *args):
        if self.children_initialised:
            self.lbl.text = self.text

    def on_enter(self):
        if self.wtype == 'text':
            self.lbl.hovering = True

    def on_leave(self):
        if self.wtype == 'text':
            self.lbl.hovering = False

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        try:
            replace = False
            if self.wtype != data['wtype']:
                replace = True
            for x in data:
                setattr(self, x, data[x])
            if not self.children_initialised:
                self.init_children()
                self.rv = rv
                self.bind(text=self.on_text)
                self.children_initialised = True
            elif replace == True:
                self.remove_widget(self.lbl)
                self.init_children()
            self.update_kbhover(rv.kbhover_index)
            self.update_selection(rv.selected_index)
            super(SideBarViewClass, self).refresh_view_attrs(rv, index, data)
        except Exception as e:
            traceback.print_exc()

    def do_func(self):
        if self.func:
            self.func()
            if self.can_select:
                self.rv.selected_index = self.index
                self.lbl.selected = True

    def on_left_click(self):
        self.do_func()

    def on_right_click(self):
        if self.func2:
            self.func2()

    def on_touch_down(self, touch):
        if self.wtype == 'text':
            if self.collide_point(touch.x, touch.y):
                if touch.device == 'mouse':
                    if touch.button == 'left':
                        self.on_left_click()
                    elif touch.button == 'right':
                        self.on_right_click()
                else:
                    self.do_func()
                return True


class SideBarRecycleView(FocusBehaviorCanvas, AppRecycleView):
    kbhover_index = NumericProperty()
    selected_index = NumericProperty()

    def __init__(self, **kwargs):
        super(SideBarRecycleView, self).__init__(**kwargs)
        self.bind(focus=self.on_focus_update_kbhover)

    def on_children(self, _, value):
        box = value[0]
        self.kb_switch = {
            kb.DOWN: box.on_arrow_down,
            kb.UP: box.on_arrow_up,
            kb.RETURN: self.kb_func_visible_hover,
            kb.PAGE_UP: self.page_up,
            kb.PAGE_DOWN: self.page_down,
            kb.MENU: self.kb_ctx_menu
        }

    def on_focus_update_kbhover(self, _, has_focus):
        if has_focus:
            self.kbhover_index = self.selected_index
        else:
            self.kbhover_index = -1

    def on_key_down(self, key, *args):
        if key in self.kb_switch:
            self.kb_switch[key]()

    def set_kbhover_previous(self):
        for i in reversed(range(self.kbhover_index)):
            if self.data[i]['wtype'] == 'text':
                self.kbhover_index = i
                break

    def set_kbhover_next(self):
        len_data = len(self.data)
        for i in range(self.kbhover_index + 1, len_data):
            if self.data[i]['wtype'] == 'text':
                self.kbhover_index = i
                break

    def on_kbhover_index(self, _, new_index):
        for x in self.children[0].children:
            x.update_kbhover(new_index)
        self.scroll_to_index(new_index)

    def on_selected_index(self, _, new_index):
        for x in self.children[0].children:
            x.update_selection(new_index)

    def kb_func_visible_hover(self):
        for x in self.children[0].children:
            if x.index == self.kbhover_index:
                x.do_func()

    def kb_ctx_menu(self):
        for x in self.children[0].children:
            if x.index == self.kbhover_index:
                x.on_right_click()

class SingleSelectBox(AppRecycleBoxLayout):
    def get_modifier_mode(self):
        return ''

Builder.load_string(kv)
