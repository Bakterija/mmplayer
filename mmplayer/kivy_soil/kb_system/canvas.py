from kivy.properties import ListProperty, NumericProperty, ObjectProperty
from .focus import FocusBehavior
from kivy.lang import Builder


class FocusBehaviorCanvas(FocusBehavior):
    '''FocusBehavior subclass with a line border
    that is visible when self.focus is True
    '''
    border_color = ListProperty([0.2, 0.3, 0.7, 1])
    '''RGBA border line color'''

    border_width = NumericProperty(2)
    '''Border width in pixels'''


class FocusBehaviorCanvasScroller(FocusBehaviorCanvas):
    '''FocusBehavior subclass with a line border
    that is visible when self.focus is True
    and a scroll_when_focused ObjectProperty of a ScrollView object
    which will be scrolled when inheriting widget receives focus
    '''

    scroll_when_focused = ObjectProperty()
    '''ObjectProperty of the ScrollView object which will be scrolled when
    FocusBehaviorCanvasScroller receives focus'''

    def __init__(self, **kwargs):
        super(FocusBehaviorCanvasScroller, self).__init__(**kwargs)
        self.fbind('focus', self.on_focus_do_scroll)

    def on_focus_do_scroll(self, _, value):
        if not self.scroll_when_focused:
            return
        if value:
            self.scroll_when_focused.scroll_to(self, padding=self.height * 3)


Builder.load_string('''
<FocusBehaviorCanvas>:
    canvas.after:
        Color:
            rgba: self.border_color if self.focus else [0, 0, 0, 0]
        Line:
            points: self.x + 1, self.y + 1, self.x + 1, self.top - 1, self.right - 1, self.top - 1, self.right - 1, self.y + 1, self.x + 1, self.y + 1
            width: self.border_width
''')
