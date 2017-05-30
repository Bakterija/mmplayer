from app_modules.kb_system.canvas import FocusBehaviorCanvas
from kivy.uix.textinput import TextInput
# from kivy.lang import Builder


class CompatTextInput(FocusBehaviorCanvas, TextInput):
    '''TextInput widget which is compatible with this apps behaviors'''
    remove_focus_on_touch_move = False

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


# Builder.load_string('''
# <CompatTextInput>
# ''')
