from kivy_soil.kb_system.canvas import FocusBehaviorCanvas
from kivy_soil.kb_system.canvas import FocusBehaviorCanvasScroller
from kivy.uix.textinput import TextInput

__all__ = ('CompatTextInput', 'CompatTextInputScroller')


class CompatTextInputBase(TextInput):
    ignored_keys = [9,]
    ignored_text = '`'

    def __init__(self, **kwargs):
        super(CompatTextInputBase, self).__init__(**kwargs)
        self.remove_focus_on_touch_move = False

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if keycode[0] in self.ignored_keys:
            return
        super(CompatTextInputBase, self).keyboard_on_key_down(
            window, keycode, text, modifiers)

    def keyboard_on_key_up(self, window, keycode):
        if keycode[0] in self.ignored_keys:
            return
        super(CompatTextInputBase, self).keyboard_on_key_up(
            window, keycode)

    def insert_text(self, s, from_undo=False):
        if s in self.ignored_text:
            return
        return super(
            CompatTextInputBase, self).insert_text(s, from_undo=from_undo)


class CompatTextInput(FocusBehaviorCanvas, CompatTextInputBase):
    '''TextInput widget which is compatible with kivy_soil focus behavior'''
    pass

class CompatTextInputScroller(FocusBehaviorCanvasScroller,
                              CompatTextInputBase):
    '''TextInput widget which is compatible with kivy_soil focus behavior.
    Inherits from FocusBehaviorCanvasScroller instead of FocusBehaviorCanvas
    '''
    pass
