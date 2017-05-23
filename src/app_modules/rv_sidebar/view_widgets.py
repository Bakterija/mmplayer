from __future__ import print_function
from kivy.properties import (
    BooleanProperty, NumericProperty, ListProperty, StringProperty)
from kivy.uix.behaviors import ButtonBehavior
from .view_base import SideBarViewBase, SideBarButton
from app_modules.behaviors.hover_behavior import HoverBehavior
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.app import App


class SideBarPlaylistButton(SideBarButton):
    path = StringProperty()
    def refresh_attrs(self, parent):
        self.text = parent.text
        self.selected = self.parent.selected
        self.path = self.parent.path

    def on_left_click(self):
        root = App.get_running_app().root
        if root.manager.current != 'media':
            root.switch_screen('media')
        self.parent.parent.select_with_touch(self.parent.index)
        root.media_control.open_playlist({'path': self.path})

    def on_right_click(self):
        self.parent.parent.select_with_touch(self.parent.index)
        self.parent.parent.open_context_menu()


class SideBarScreenButton(SideBarButton):
    opened = BooleanProperty()

    def refresh_attrs(self, parent):
        self.text = parent.text
        self.selected = self.parent.selected
        manager = App.get_running_app().root.manager
        if manager.current == self.text.lower():
            self.opened = True
        else:
            self.opened = False

    def on_left_click(self):
        self.parent.parent.select_with_touch(self.parent.index)
        root = App.get_running_app().root
        root.switch_screen(self.text.lower())

    def on_right_click(self):
        pass


class SideBarSection(SideBarViewBase, Label):
    markup = True

    def refresh_attrs(self, parent):
        self.text = parent.text

    def on_text(self, _, value):
        if value[:3] != '[b]':
            self.text = '[b]%s[/b]' % (value)


class SideBarSeparator(SideBarViewBase, Widget):
    pass
