from app_modules.behaviors.focus import FocusBehaviorCanvas
from kivy.uix.textinput import TextInput
from kivy.lang import Builder


class CompatTextInput(TextInput):
    '''TextInput widget which is compatible with this apps behaviors'''

    def __init__(self, **kwargs):
        super(CompatTextInput, self).__init__(**kwargs)

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if keycode[0] == 9:
            return
        super(CompatTextInput, self).keyboard_on_key_down(
            window, keycode, text, modifiers)

    def keyboard_on_key_up(self, window, keycode):
        if keycode[0] == 9:
            return
        super(CompatTextInput, self).keyboard_on_key_up(
            window, keycode)


Builder.load_string('''
<CompatTextInput>
''')
