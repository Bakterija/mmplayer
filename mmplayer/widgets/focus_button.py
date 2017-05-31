'''Module with buttons that integrate into kivy_soil kb_system'''

from kivy_soil.kb_system.canvas import FocusBehaviorCanvas
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty
from kivy_soil.kb_system import keys
from kivy.uix.button import Button
from kivy.uix.widget import Widget


class FocusButton(FocusBehaviorCanvas, Button):
    '''A FocusBehaviorCanvas Button which dispatches
    on_press and on_release when it has focus
    and enter or return key is pressed/released
    '''
    # def __init__(self, **kwargs):
    #     super(FocusButton, self).__init__(**kwargs)

    def on_key_down(self, key, *args):
        if key in (keys.ENTER, keys.RETURN):
            self.dispatch('on_press')

    def on_key_up(self, key, *args):
        if key in (keys.ENTER, keys.RETURN):
            self.dispatch('on_release')


class FocusButtonEmpty(FocusBehaviorCanvas, ButtonBehavior, Widget):
    '''A FocusBehaviorCanvas button which is an empty widget'''

    def on_key_down(self, key, *args):
        self.state = 'down'
        if key in (keys.ENTER, keys.RETURN):
            self.dispatch('on_press')

    def on_key_up(self, key, *args):
        self.state = 'normal'
        if key in (keys.ENTER, keys.RETURN):
            self.dispatch('on_release')
