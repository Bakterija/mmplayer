from __future__ import print_function
from kivy.properties import (
    BooleanProperty, NumericProperty, ListProperty, StringProperty)
from kivy.uix.behaviors import ButtonBehavior
from .view_base import SideBarViewBase
from app_modules.behaviors.hover_behavior import HoverBehavior
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.app import App


class SideBarButton(SideBarViewBase, Label):
    col_canvas_hover_selected = ListProperty([0.7, 0.2, 0.2, 1])
    col_canvas_selected = ListProperty([0.6, 1, 0.6, 0.3])
    col_canvas_hover = ListProperty([0.5, 0.2, 0.2, 1])
    col_canvas_default = ListProperty([1, 1, 1, 0])
    background_color = ListProperty([0.2, 0.2, 0.2, 1])
    opened = BooleanProperty(False)
    played = BooleanProperty(False)
    path = StringProperty()
    shorten = True
    shorten_from = 'right'

    def __init__(self, **kwargs):
        super(SideBarButton, self).__init__(**kwargs)
        self.bind(selected=self.on_selected_update_canvas)

    def update_opened_path(self, value):
        if self.path == value:
            self.rv.data[self.index]['opened'] = True
            self.opened = True
        else:
            self.rv.data[self.index]['opened'] = False
            self.opened = False

    def update_played_path(self, value):
        if self.path == value:
            self.rv.data[self.index]['played'] = True
            self.played = True
        else:
            self.rv.data[self.index]['played'] = False
            self.played = False

    def on_left_click(self):
        self.parent.select_with_touch(self.index)
        self.do_func()

    def on_right_click(self):
        self.parent.select_with_touch(self.index)
        self.parent.open_context_menu()

    def refresh_view_attrs(self, rv, index, data):
        super(SideBarButton, self).refresh_view_attrs(rv, index, data)
        if not data['wtype'] == 'playlist_button':
            self.opened = False
            self.played = False

    def on_enter(self):
        self.rv.data[self.index]['hovering'] = True

    def on_leave(self):
        self.rv.data[self.index]['hovering'] = False

    def on_hovering(self, _, value):
        if value:
            if self.selected:
                self.background_color = self.col_canvas_hover_selected
            else:
                self.background_color = self.col_canvas_hover
        elif self.selected:
            self.background_color = self.col_canvas_selected
        else:
            self.background_color = self.col_canvas_default

    def on_selected_update_canvas(self, _, value):
        if value:
            if self.hovering:
                self.background_color = self.col_canvas_hover_selected
            else:
                self.background_color = self.col_canvas_selected
        elif self.hovering:
            self.background_color = self.col_canvas_hover
        else:
            self.background_color = self.col_canvas_default


class SideBarSection(SideBarViewBase, Label):
    selectable = False
    markup = True
    def on_text(self, _, value):
        if value[:3] != '[b]':
            self.text = '[b]%s[/b]' % (value)


class SideBarSeparator(SideBarViewBase, Widget):
    selectable = False
