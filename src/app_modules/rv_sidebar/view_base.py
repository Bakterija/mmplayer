from app_modules.widgets_standalone.app_recycleview import AppRecycleViewClass
from app_modules.behaviors.hover_behavior import HoverBehavior
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.uix.label import Label


class SideBarViewBase(AppRecycleViewClass):
    hovering = BooleanProperty(False)
    selectable = False

    def refresh_attrs(self, parent):
        pass

    def on_left_click(self):
        pass

    def on_right_click(self):
        pass


class SideBarButton(SideBarViewBase, Label):
    selected = BooleanProperty(False)
    text = StringProperty()
    shorten = True
    shorten_from = 'right'
    selectable = True
