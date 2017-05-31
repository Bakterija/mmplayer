from kivy_soil.kb_system.canvas import FocusBehaviorCanvas
from kivy.uix.textinput import TextInput


class CompatTextInput(FocusBehaviorCanvas, TextInput):
    '''TextInput widget which is compatible with kivy_soil focus behavior'''

    remove_focus_on_touch_move = False

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
