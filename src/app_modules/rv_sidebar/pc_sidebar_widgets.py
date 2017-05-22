from __future__ import print_function
from kivy.properties import BooleanProperty, NumericProperty, ListProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label


class SideBarButton(ButtonBehavior, Label):
    col_canvas_hover_selected = ListProperty([0.7, 0.2, 0.2, 1])
    col_canvas_selected = ListProperty([0.6, 1, 0.6, 0.3])
    col_canvas_hover = ListProperty([0.5, 0.2, 0.2, 1])
    col_canvas_default = ListProperty([1, 1, 1, 0])
    background_color = ListProperty([0.2, 0.2, 0.2, 1])
    hovering = BooleanProperty()
    selected = BooleanProperty()
    shorten = True
    shorten_from = 'right'

    def on_hovering(self, _, new_hovering):
        if new_hovering:
            if self.selected:
                self.background_color = self.col_canvas_hover_selected
            else:
                self.background_color = self.col_canvas_hover
        elif self.selected:
            self.background_color = self.col_canvas_selected
        else:
            self.background_color = self.col_canvas_default

    def on_selected(self, _, new_selected):
        if new_selected:
            if self.hovering:
                self.background_color = self.col_canvas_hover_selected
            else:
                self.background_color = self.col_canvas_selected
        elif self.hovering:
            self.background_color = self.col_canvas_hover
        else:
            self.background_color = self.col_canvas_default

    def collide_point_window(self, x, y):
        sx, sy = self.to_window(self.x, self.y)
        return sx <= x <= sx + self.width and sy <= y <= sy + self.height


class SideBarSection(ButtonBehavior, Label):
    markup = True
    def on_text(self, _, value):
        if value[:3] != '[b]':
            self.text = '[b]%s[/b]' % (value)
