from widgets.compat_textinput import CompatTextInput
from kivy_soil.kb_system.canvas import FocusBehaviorCanvas
from kivy.properties import StringProperty, BooleanProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.clock import Clock


Builder.load_string('''
<FilterInputBox>:
    CompatTextInput:
        id: filter_input
        size_hint: 1, 1
        background_color: root.background_color
        background_active: ''
        background_normal: ''
        background_disabled_normal: ''
        border: 0, 0, 0, 0
        markup: True
        foreground_color: root.text_color
        font_size: int(self.height * 0.45)
        multiline: False
        on_text_validate: root.filter_text = self.text
        hint_text: '' if self.focus else 'Filter'
''')


class FilterInputBox(BoxLayout):
    filter_text = StringProperty()
    is_focusable = BooleanProperty()
    background_color = ListProperty([0.2, 0.2, 0.2, 1])
    text_color = ListProperty([0.9, 0.9, 0.9, 1])

    def on_ids(self, _, value):
        value.filter_input.bind(text=self.on_input_text)

    def on_input_text(self, _, value):
        Clock.unschedule(self.update_filter_text)
        Clock.schedule_once(self.update_filter_text, 0.5)

    def update_filter_text(self, *args):
        self.filter_text = self.ids.filter_input.text

    def on_is_focusable(self, _, value):
        if value:
            self.ids.filter_input.is_focusable = True
        else:
            self.ids.filter_input.is_focusable = False

    def focus_input(self, *args):
        input_widget = self.ids.filter_input
        input_widget.focus = True
        input_widget.select_all()
