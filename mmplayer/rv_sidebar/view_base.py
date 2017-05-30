from kivy.properties import StringProperty, BooleanProperty
from kivy_soil.app_recycleview import AppRecycleViewClass
from kivy_soil.hover_behavior import HoverBehavior
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.clock import Clock


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
