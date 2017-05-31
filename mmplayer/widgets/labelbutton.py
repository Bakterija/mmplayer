from widgets.multi_line_label import MultiLineLabel
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import ListProperty
from kivy.uix.label import Label
from kivy.lang import Builder


class LabelButton(ButtonBehavior, MultiLineLabel):
    pass


kv = """
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



Builder.load_string(kv)
