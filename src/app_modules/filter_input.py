from app_modules.widgets_standalone.compat_textinput import CompatTextInput
from app_modules.behaviors.focus import FocusBehaviorCanvas
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder


Builder.load_string('''
<FilterInputBox>:
    orientation: 'horizontal'
    canvas.before:
        Color:
            rgba: col_dgrey
        Rectangle:
            pos: self.pos
            size: self.size
    Label:
        size_hint: None, 1
        text: 'Filter'
        font_size: int(self.height * 0.4)
        width: self.font_size * 4
    CompatTextInput:
        id: filter_input
        size_hint: 1, 1
        background_color: col_dgrey
        background_active: ''
        background_normal: ''
        background_disabled_normal: ''
        text_color: col_white
        border: 0, 0, 0, 0
        cursor_color: col_white
        markup: True
        foreground_color: col_white
        font_size: int(self.height * 0.4)
        multiline: False
        on_text_validate: root.filter_text = self.text
        canvas.before:
            Color:
                rgba: col_white
            Line:
                points: self.x, self.y + (self.height * 0.2), self.right - (self.width * 0.05), self.y + (self.height * 0.2)
''')


class FilterInputBox(BoxLayout):
    filter_text = StringProperty()
    is_focusable = BooleanProperty()

    def on_is_focusable(self, _, value):
        if value:
            self.ids.filter_input.is_focusable = True
        else:
            self.ids.filter_input.is_focusable = False

    # def enable_focusable(self):
    #
    # def disable_focusable(self):

    def focus_input(self, *args):
        input_widget = self.ids.filter_input
        input_widget.focus = True
        input_widget.select_all()
