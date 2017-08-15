from kivy_soil.kb_system.canvas import FocusBehaviorCanvas
from kivy_soil.kb_system import keys
from kivy.uix.button import Button


class FocusButton(FocusBehaviorCanvas, Button):
    def on_key_down(self, key, *args):
        if key in (keys.ENTER, keys.RETURN):
            self.dispatch('on_press')

    def on_key_up(self, key, *args):
        if key in (keys.ENTER, keys.RETURN):
            self.dispatch('on_release')
