from __future__ import print_function
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import ListProperty
from kivy.metrics import dp, cm
from kivy.lang import Builder
from kivy.properties import BooleanProperty, NumericProperty


kv22 = """
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

class rvSection(ButtonBehavior, Label):
    background_color = ListProperty([1,1,1])
    def __init__(self, **kwargs):
        super(rvSection, self).__init__(**kwargs)
        self.size_hint_y = None

Builder.load_string(kv22)
