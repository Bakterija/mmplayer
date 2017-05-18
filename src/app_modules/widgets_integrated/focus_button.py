from app_modules.kb_system.canvas import FocusBehaviorCanvas
from kivy.uix.button import Button
from app_modules.kb_system import keys


class FocusButton(FocusBehaviorCanvas, Button):

    def __init__(self, **kwargs):
        super(FocusButton, self).__init__(**kwargs)

    def on_key_down(self, key, *args):
        if key in (keys.ENTER, keys.RETURN):
            self.dispatch('on_press')

    def on_key_up(self, key, *args):
        if key in (keys.ENTER, keys.RETURN):
            self.dispatch('on_release')
