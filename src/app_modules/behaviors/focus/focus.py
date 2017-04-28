from kivy.properties import BooleanProperty
from kivy.event import EventDispatcher
from kivy.uix.widget import Widget
from kivy.core.window import Window

focusable_widgets = []
current_focus = None

def on_key_up(window, key, *args):
    if current_focus:
        current_focus.on_key_up(key, *args)

def on_key_down(window, key, *args):
    if current_focus:
        current_focus.on_key_down(key, *args)

def on_mouse_move(window, pos):
    if current_focus and current_focus.remove_focus_on_touch:
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

def remove_focus():
    global current_focus
    current_focus.focus = False
    current_focus = None

def set_focus(widget):
    global current_focus
    widget.focus = True
    current_focus = widget

class FocusBehavior(Widget):
    focus = BooleanProperty(False)
    remove_focus_on_touch = True

    def __init__(self, **kwargs):
        super(FocusBehavior, self).__init__(**kwargs)
        self.bind(parent=on_parent)

    def on_key_down(self, key, *args):
        pass

    def on_key_up(self, key, *args):
        pass
