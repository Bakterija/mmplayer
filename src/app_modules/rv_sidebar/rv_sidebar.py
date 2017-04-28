from kivy.uix.recycleview import RecycleView
from kivy.uix.stacklayout import StackLayout
from kivy.utils import platform
from kivy.metrics import dp, cm
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import BooleanProperty
from kivy.properties import StringProperty, DictProperty
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from app_modules.behaviors.focus import FocusBehaviorCanvasKB
from app_modules.behaviors.focus import FocusBehaviorCanvas
from app_modules.widgets_standalone.app_recycleview import (
    AppRecycleBox, AppRecycleView)
from kivy.uix.behaviors import ButtonBehavior
from .pc_sidebar_widgets import rvLabelButton, rvSection
from kivy.clock import Clock
from kivy.core.window import Window
from app_modules import keys as kb
import traceback


kv = '''
<SideBarRecycleView>:
    viewclass: 'SideBarViewClass'
    SelectableRecycleBox:
        orientation: 'vertical'
        size_hint: None, None
        height: self.minimum_height
        width: root.width - root.bar_width
        default_size_hint: 1, None
        default_size: None, None
'''

class SideBarViewClass(RecycleDataViewBehavior, ButtonBehavior, StackLayout):
    index = None
    text = StringProperty()
    func = None
    func2 = None
    fsize = NumericProperty(int(dp(16)))
    wtype = StringProperty()
    children_initialised = False

    def __init__(self, **kwargs):
        super(SideBarViewClass, self).__init__(**kwargs)
        size_hint_y = None

    def init_children(self, *args):
        if self.wtype == 'text':
            self.lbl = rvLabelButton(text=self.text)
            self.add_widget(self.lbl)
        elif self.wtype == 'section':
            self.lbl = rvSection(text=self.text)
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

    def on_mouse_move(self, win, pos):
        if self.wtype == 'text':
            self.lbl.on_mouse_move(int(pos[0]), int(pos[1]))

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
                Window.bind(mouse_pos=self.on_mouse_move)
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
        self.kb_switch = {
            kb.DOWN: self.set_kbhover_next,
            kb.UP: self.set_kbhover_previous,
            kb.RETURN: self.kb_func_visible_hover,
            kb.PAGE_UP: self.page_up,
            kb.PAGE_DOWN: self.page_down,
        }

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


class SelectableRecycleBox(RecycleBoxLayout):
    pass


Builder.load_string(kv)
