from kivy.properties import ListProperty, NumericProperty
from .focus import FocusBehavior
# from kivy.uix.behaviors import FocusBehavior
from kivy.lang import Builder


class FocusBehaviorCanvas(FocusBehavior):
    border_color = ListProperty([0.2, 0.3, 0.7, 1])
    border_width = NumericProperty(2)


class FocusBehaviorCanvasLight(FocusBehaviorCanvas):
    border_color = ListProperty([0.3, 0.4, 0.8, 1])
    border_width = NumericProperty(1)


Builder.load_string('''
<FocusBehaviorCanvas>:
    canvas.after:
        Color:
            rgba: self.border_color if self.focus else [0, 0, 0, 0]
        Line:
            points: self.x + 1, self.y + 1, self.x + 1, self.top - 1, self.right - 1, self.top - 1, self.right - 1, self.y + 1, self.x + 1, self.y + 1
            width: self.border_width
''')
