from kivy.properties import ListProperty, NumericProperty
from .focus import FocusBehavior
from kivy.lang import Builder


class FocusBehaviorCanvas(FocusBehavior):
    border_color = ListProperty([0.2, 0.3, 0.7, 1])


class FocusBehaviorCanvasKB(FocusBehavior):
    border_color = ListProperty([0.2, 0.3, 0.7, 1])
    kb_hover = NumericProperty()


Builder.load_string('''
<FocusBehaviorCanvas>:
    canvas.before:
        Color:
            rgba: self.border_color if self.focus else [0, 0, 0, 0]
        Line:
            points: self.x + 1, self.y + 1, self.x + 1, self.top - 1, self.right - 1, self.top - 1, self.right - 1, self.y + 1, self.x + 1, self.y + 1

<FocusBehaviorCanvasKB>:
    canvas.after:
        Color:
            rgba: [0, 0, 0, 0] if self.kb_hover else self.border_color if self.focus else [0, 0, 0, 0]
        Line:
            points: self.x + 1, self.y + 1, self.x + 1, self.top - 1, self.right - 1, self.top - 1, self.right - 1, self.y + 1, self.x + 1, self.y + 1
''')
