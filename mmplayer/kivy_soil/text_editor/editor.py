from kivy.properties import StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.clock import Clock, mainthread


Builder.load_string('''
<TextEditor>:
    orientation: 'horizontal'
    ScrollView:
        id: scroller
        CompatTextInput:
            id: input
            grab_focus: True
            size_hint: 1, None
            height: self.minimum_height if root.height < self.minimum_height else root.height
            multiline: True
            on_cursor: root.on_cursor(args[1])
            on_cursor_row: root.on_cursor_row(args[1])
            cursor_width: cm(0.07)
            cursor_color: 0.2, 0.4, 0.7, 1.0
''')


class TextEditor(BoxLayout):

    def __init__(self, **kwargs):
        super(TextEditor, self).__init__(**kwargs)

    def on_cursor(self, value):
        pass

    def on_cursor_row(self, row):
        scroll_y = self.ids.scroller.scroll_y
        negscroll_y = 1.0 - self.ids.scroller.scroll_y

        inp_height = self.ids.input.height
        scrl_height = self.ids.scroller.height
        size1 = inp_height - scrl_height

        line_height = self.ids.input.line_height
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


class TextEditorPopup(Popup):
    text = StringProperty()
    title = 'Text editor'

    def __init__(self, **kwargs):
        super(TextEditorPopup, self).__init__(**kwargs)
        self.content = TextEditor()
        self.size_hint = (0.9, 0.9)

    def open(self, *args):
        super(TextEditorPopup, self).open(*args)
        self.content.ids.input.text = self.text
        Clock.schedule_once(self.focus_textinput, 0)

    def focus_textinput(self, *args):
        winput = self.content.ids.input
        winput.focus = True
        winput.cursor = (0, 0)
