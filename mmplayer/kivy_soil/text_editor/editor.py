from __future__ import division
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy_soil.kb_system.canvas import FocusBehaviorCanvas
from kivy.properties import BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock, mainthread
from kivy.uix.popup import Popup
from kivy.lang import Builder


Builder.load_string('''
#: import CompatTextInput kivy_soil.kb_system.compat_widgets.textinput.CompatTextInput
#: import DampedScrollEffect kivy.effects.dampedscroll.DampedScrollEffect

<TextEditor>:
    border_color: inputw.border_color
    border_width: inputw.border_width
    focus: inputw.focus
    inputw: inputw
    orientation: 'horizontal'
    canvas.after:
        Color:
            rgba:
                [self.border_color[0], self.border_color[1],
                self.border_color[2], 1] if self.focus else [0, 0, 0, 0]
        Line:
            width: self.border_width
            points:
                [self.x + 1, self.y + 1, self.x + 1,
                self.top - self.border_width, self.right - self.border_width,
                self.top - self.border_width, self.right - self.border_width,
                self.y + 1, self.x + 1, self.y + 1]
    ScrollView:
        id: scroller
        effect_cls: DampedScrollEffect
        CompatTextInput:
            id: inputw
            size_hint: 1, None
            height: self.minimum_height if root.height < self.minimum_height else root.height
            is_focusable: root.is_focusable
            border_width: 1
            border_color:
                [self.border_color[0], self.border_color[1],
                self.border_color[2], 0]
            multiline: True
            on_cursor: root.on_cursor(args[1])
            on_cursor_row: root.on_cursor_row(args[1])
            cursor_width: cm(0.07)
            cursor_color: 0.2, 0.4, 0.7, 1.0
''')


class TextEditor(BoxLayout):
    is_focusable = BooleanProperty(True)
    border_width = NumericProperty(1)
    focus = BooleanProperty(False)
    inputw = ObjectProperty()
    text = StringProperty()

    def __init__(self, **kwargs):
        super(TextEditor, self).__init__(**kwargs)

    def on_inputw(self, _, value):
        value.bind(text=self.on_inputw_text)

    def on_inputw_text(self, _, value):
        if self.text != value:
            self.text = value

    def on_text(self, _, value):
        if self.inputw.text != self.text:
            self.inputw.text = value

    def on_cursor(self, value):
        pass

    def on_cursor_row(self, row):
        scroll_y = self.ids.scroller.scroll_y
        negscroll_y = 1.0 - self.ids.scroller.scroll_y

        inp_height = self.ids.inputw.height
        scrl_height = self.ids.scroller.height
        size1 = inp_height - scrl_height

        line_height = self.ids.inputw.line_height
        max_lines = int(inp_height / line_height) - 1
        rem_lines = int(size1 / line_height)
        mrem_lines = (max_lines - (max_lines - rem_lines))

        visible_first = int(mrem_lines * negscroll_y)
        visible_last = int(visible_first + scrl_height / line_height)
        if visible_last > max_lines:
            visible_last = max_lines

        prc = 0.0
        if row > 0.0 and mrem_lines > 0.0:
            prc = row / mrem_lines

        conv_lh = self.ids.scroller.convert_distance_to_scroll(
            0, scrl_height - line_height * 1.2)
        if row < visible_first or row == 0:
            self.ids.scroller.scroll_y = 1.0 - prc
        elif row > visible_last or row == max_lines:
            self.ids.scroller.scroll_y = 1.0 - prc + conv_lh[1]


class TextEditorPopup(Popup, FocusBehaviorCanvas):
    text = StringProperty()
    title = 'Text editor'
    grab_focus = True

    def __init__(self, **kwargs):
        super(TextEditorPopup, self).__init__(**kwargs)
        self.size_hint = (0.9, 0.9)
        self.content = TextEditor(is_focusable=True)
        if self.content.inputw:
            self.on_inputw(None, self.content.inputw)
        else:
            self.content.bind(inputw=self.on_inputw)

    def on_inputw(self, _, widget):
        widget.bind(border_width=self.setter('border_width'))
        self.border_width = widget.border_width
        widget.is_subfocus = True
        self.subfocus_widgets = [widget]

    def open(self, focus=False, *args):
        super(TextEditorPopup, self).open(*args)
        self.content.ids.inputw.text = self.text
        self.content.ids.inputw.cursor = (0, 0)
        if focus:
            Clock.schedule_once(self.focus_textinput, 0)

    def focus_textinput(self, *args):
        winput = self.content.ids.inputw
        winput.focus = True

    @staticmethod
    def quick_open(text, focus=False):
        '''Static method that creates a new popup with argument text
        and opens it, then returns the new widget'''
        new = TextEditorPopup(text=text)
        new.open(focus=focus)
        return new
