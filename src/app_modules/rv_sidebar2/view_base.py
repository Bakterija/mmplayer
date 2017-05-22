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
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from app_modules.behaviors.hover_behavior import HoverBehavior
from app_modules.kb_system import keys
from app_modules.widgets_standalone.app_recycleview import AppRecycleViewClass


class SideBarViewBase(HoverBehavior, AppRecycleViewClass, ButtonBehavior):
    text = StringProperty()
    index = None
    func = None
    func2 = None

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
