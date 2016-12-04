from __future__ import print_function
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import ListProperty

class LabelButton(Label, ButtonBehavior):
    pass


bgkv = """
<LabelButtonBackground>
    canvas.before:
        Color:
            rgba: self.background_color
        Rectangle:
            pos: self.pos
            size: self.size
"""

class LabelButtonBackground(ButtonBehavior, Label):
    background_color = ListProperty([1,1,1,1])
    def __init__(self, **kwargs):
        super(LabelButtonBackground, self).__init__(**kwargs)



Builder.load_string(bgkv)
