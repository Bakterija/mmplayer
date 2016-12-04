from __future__ import print_function
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import ListProperty
from kivy.metrics import dp, cm
from kivy.lang import Builder
from kivy.properties import BooleanProperty, NumericProperty


kv22 = """
<rvLabelButton>:
    hovercolors: [1, 1, 1, 0], [0.5, 0.2, 0.2, 1], [0.6, 1, 0.6, 0.3], [0.7, 0.2, 0.2, 1]
    text_size: self.size
    height: cm(0.8)
    font_size: dp(16)
    canvas.before:
        Color:
            rgba: self.hovercolors[self.hovering]
        Rectangle:
            pos: self.pos
            size: self.width*1, self.height

<rvSection>:
    height: cm(0.6)
    font_size: dp(14)
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
    hovering = NumericProperty(0)
    selected = NumericProperty(0)
    def __init__(self, **kwargs):
        super(rvLabelButton, self).__init__(**kwargs)
        self.size_hint_y = None
        default_setter(self)

    def on_mouse_move(self, posx, posy):
        if self.collide_point_window(posx, posy):
            self.hovering = self.selected + 1
        else:
            self.hovering = self.selected + 0

    def on_select(self, *args):
        try:
            if self.selected:
                self.selected = 0
                self.hovering = self.selected + 0
            else:
                self.selected = 2
                self.hovering = self.selected + 1
        except Exception as e:
            print(e)

    def collide_point_window(self, x, y):
        sx, sy = self.to_window(self.x, self.y)
        return sx <= x <= sx + self.width and sy <= y <= sy + self.height


class rvSection(ButtonBehavior, Label):
    background_color = ListProperty([1,1,1])
    def __init__(self, **kwargs):
        super(rvSection, self).__init__(**kwargs)
        self.size_hint_y = None
        default_setter(self)


Builder.load_string(kv22)
