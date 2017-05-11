from kivy.properties import BooleanProperty
from kivy.event import EventDispatcher
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.logger import Logger

focusable_widgets = []
current_focus = None
ctrl_held = False
alt_held = False
shift_held = False
modifier = []

def update_modifier():
    global ctrl_held, alt_held, shift_held, modifier
    modifier = []
    if ctrl_held:
        modifier.append('ctrl')
    if alt_held:
        modifier.append('alt')
    if shift_held:
        modifier.append('shift')

def on_key_up(window, key, *args):
    global ctrl_held, alt_held, shift_held
    if key == 9:
        return

    if key in (308, 1073741824):
        alt_held = False
    elif key in (305, 306):
        ctrl_held = False
    elif key in (304, 303):
        shift_held = False

    if current_focus:
        update_modifier()
        current_focus.on_key_up(key, modifier)

def on_key_down(window, key, *args):
    global ctrl_held, alt_held, shift_held
    if key == 9:
        return

    if key in (308, 1073741824):
        alt_held = True
    elif key in (305, 306):
        ctrl_held = True
    elif key in (304, 303):
        shift_held = True

    if current_focus:
        update_modifier()
        current_focus.on_key_down(key, modifier)

def on_mouse_move(window, pos):
    if current_focus and current_focus.remove_focus_on_touch_move:
        remove_focus()

Window.bind(on_key_up=on_key_up)
Window.bind(on_key_down=on_key_down)
Window.bind(mouse_pos=on_mouse_move)

def on_parent(self, parent):
    global focusable_widgets
    if parent:
        focusable_widgets.append(self)
    else:
        focusable_widgets.remove(self)

def focus_next():
    if not focusable_widgets:
        return

    len_focusable_widgets = len(focusable_widgets)
    found = False
    for i, widget in enumerate(focusable_widgets):
        if widget.focus:
            widget.focus = False
            found = True
            if len_focusable_widgets - 1 > i:
                set_focus(focusable_widgets[i+1])
            else:
                set_focus(focusable_widgets[0])
            break

    if not found:
        set_focus(focusable_widgets[0])
    # Logger.info('focus: focus_next: %s' % (current_focus))

def remove_focus():
    global current_focus
    if current_focus:
        current_focus.focus = False
        current_focus = None

def set_focus(widget):
    global current_focus
    widget.focus = True
    current_focus = widget

class FocusBehavior(Widget):
    focus = BooleanProperty(False)
    remove_focus_on_touch_move = True

    def __init__(self, **kwargs):
        super(FocusBehavior, self).__init__(**kwargs)
        self.bind(parent=on_parent)
        self.bind(focus=self.remove_other_focused)

    def remove_other_focused(self, _, value):
        global current_focus
        if value:
            if current_focus != self:
                remove_focus()
                set_focus(self)

    def on_key_down(self, key, *args):
        pass

    def on_key_up(self, key, *args):
        pass
