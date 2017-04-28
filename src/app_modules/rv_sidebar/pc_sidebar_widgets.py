from __future__ import print_function
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import ListProperty
from kivy.metrics import dp, cm
from kivy.lang import Builder
from kivy.properties import BooleanProperty, NumericProperty


kv22 = """
<rvLabelButton>:
    col_canvas_default: [1, 1, 1, 0]
    col_canvas_hover: [0.5, 0.2, 0.2, 1]
    col_canvas_selected: [0.6, 1, 0.6, 0.3]
    col_canvas_hover_selected: [0.7, 0.2, 0.2, 1]
    text_size: self.size
    height: int(cm(0.8))
    font_size: int(self.height * 0.5)
    canvas.before:
        Color:
            rgba: self.background_color
        Rectangle:
            pos: self.pos
            size: self.width, self.height

<rvSection>:
    height: int(cm(0.6))
    font_size: int(self.height * 0.6)
    background_color: 0.2, 0.2, 0.2
    text_size: self.size
    canvas.before:
        Color:
            rgb: self.background_color
        Rectangle:
            pos: self.pos
            size: self.size
"""

rv_sidebar_default_values = [
    ['padding', (int(dp(10)), int(dp(2)))]
]
def default_setter(widget):
    for x in rv_sidebar_default_values:
        setattr(widget, x[0], x[1])

class rvLabelButton(ButtonBehavior, Label):
    background_color = ListProperty([0.2, 0.2, 0.2, 1])
    hovering = BooleanProperty()
    selected = BooleanProperty()

    def __init__(self, **kwargs):
        super(rvLabelButton, self).__init__(**kwargs)
        self.size_hint_y = None
        default_setter(self)

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

    def on_mouse_move(self, posx, posy):
        if self.collide_point_window(posx, posy):
            self.hovering = True
        else:
            self.hovering = False

    def collide_point_window(self, x, y):
        sx, sy = self.to_window(self.x, self.y)
        return sx <= x <= sx + self.width and sy <= y <= sy + self.height


class rvSection(ButtonBehavior, Label):

    def __init__(self, **kwargs):
        super(rvSection, self).__init__(**kwargs)
        self.size_hint_y = None
        default_setter(self)


Builder.load_string(kv22)
