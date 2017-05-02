from app_modules.behaviors.focus import FocusBehaviorCanvas
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

kv = '''
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
        font_size: self.height * 0.5
        width: self.font_size * 4
    TextInput:
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
        font_size: self.height * 0.5
        multiline: False
        on_text_validate: app.set_filter_text(self.text)
        canvas.before:
            Color:
                rgba: col_white
            Line:
                points: self.x, self.y + (self.height * 0.2), self.right - (self.width * 0.05), self.y + (self.height * 0.2)
'''


class FilterInputBox(FocusBehaviorCanvas, BoxLayout):
    pass


Builder.load_string(kv)
