from kivy.properties import BooleanProperty, ListProperty
from kivy.event import EventDispatcher
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.logger import Logger
from kivy.clock import Clock
from time import time
import weakref

active = True

focusable_widgets = []
'''Storage list for references to FocusBehavior widgets without focus grab'''

focus_grab_widgets = []
'''Storage list for references to FocusBehavior widgets with focus grab'''

prev_focused_widgets = []
'''Storage list of references to previously focused widgets,
duplicates are not inserted'''

max_previous_widgets = 10
'''Int number of max widgets, defaults to 10'''

current_focus = None
'''Reference to currently focused widget'''

def on_mouse_move(window, pos):
    '''Removes focus from widgets with
    self.remove_focus_on_touch_move set to True
    '''
    if current_focus and current_focus.remove_focus_on_touch_move:
        remove_focus()

def on_parent(self, parent):
    '''Adds widget with parent to focusable_widgets or focus_grab_widgets
    and removes widget without parent'''
    global focusable_widgets, focus_grab_widgets
    if self.grab_focus:
        fc_list = focus_grab_widgets
    else:
        fc_list = focusable_widgets
    if parent:
        fc_list.append(self)
    else:
        if self in fc_list:
            fc_list.remove(self)
        else:
            Logger.error('focus: on_parent: %s not in fc_list' % (self))

def find_next_focusable(widget_list):
    '''Searches a list, finds currently focused widget
    and next widget with self.is_focusable set to. Returns both
    '''
    len_widgets = len(widget_list)
    previous = (-1, None)
    new = (-1, None)
    for i, widget in enumerate(widget_list):
        if widget.focus:
            previous = (i, widget)
            if len_widgets - 1 > i:
                for i2, x in enumerate(widget_list[i+1:]):
                    if x.is_focusable:
                        new = (i + i2, x)
                        break
            if new[0] != -1:
                break
    return previous, new

def focus_next():
    '''Focuses next focusable widget in focusable_widgets list
    or first widget in focus_grab_widgets list, if it is not empty.
    If focus_grab_widgets list is not empty and focus widget has widgets
    in self.subfocus_widgets list, cycles focus between itself and those'''
    global prev_focused_widgets, focus_grab_widgets, focus_grab_widgets
    global current_focus
    new_focus = None
    if focus_grab_widgets:
        fwidget = focus_grab_widgets[0]
        if fwidget.subfocus_widgets:
            if fwidget.focus:
                new_focus = fwidget.subfocus_widgets[0]
            else:
                fprev, fnext = find_next_focusable(fwidget.subfocus_widgets)
                if fnext[0] != -1:
                    new_focus = fnext[1]
                else:
                    new_focus = fwidget
        elif not fwidget.focus:
            new_focus = fwidget

    elif focusable_widgets:
        if not current_focus:
            for x in prev_focused_widgets:
                widget = x()
                if widget in focusable_widgets:
                    new_focus = widget

        if not new_focus:
            prev, new = find_next_focusable(focusable_widgets)
            if new[0] == -1:
                new_focus = focusable_widgets[0]
            else:
                new_focus = new[1]
    if new_focus:
        set_focus(new_focus)
        # Logger.info('focus: focus_next: %s' % (current_focus))

def remove_focus(*args):
    '''Remove focus from current_focus widget'''
    global current_focus
    # Logger.info('focus: removing focus %s' % (current_focus))
    if current_focus:
        current_focus.focus = False
        current_focus = None

def set_focus_previous(*args):
    '''Set focus to last widget in prev_focused_widgets list'''
    global focus_grab_widgets, focusable_widgets, prev_focused_widgets
    if not focus_grab_widgets:
        if prev_focused_widgets:
            last = prev_focused_widgets[-1]
            # Logger.info('focus: focusing previous %s' % (last()))
            set_focus(last(), change_previous=False)

def set_focus(widget, change_previous=True):
    '''Focus a widget and update prev_focused_widgets'''
    global current_focus, prev_focused_widgets, max_previous_widgets, active
    if not active:
        return
    widget.focus = True
    if current_focus and change_previous:
        if not widget.is_subfocus:
            if prev_focused_widgets and widget == prev_focused_widgets[-1]():
                return
            prev_focused_widgets.append(weakref.ref(current_focus))
            if len(prev_focused_widgets) > max_previous_widgets:
                del prev_focused_widgets[0]
    current_focus = widget
    # Logger.info('focus: set_focus: %s - %s' % (
    #     time(), current_focus.__class__.__name__))

def activate(*args):
    global active
    active = True

def on_window_focus(_, value):
    global active
    if value:
        Clock.schedule_once(activate, 0.1)
    else:
        active = False
        remove_focus()

Window.bind(mouse_pos=on_mouse_move)
Window.bind(focus=on_window_focus)


class FocusBehavior(Widget):
    focus = BooleanProperty(False)
    '''Focus state, default is False'''

    remove_focus_on_touch_move = True

    subfocus_widgets = ListProperty()
    '''Subfocus widgets for focus grab widgets'''

    is_subfocus = BooleanProperty(False)
    '''Subfocus widgets don't cycle normally,
    have to be in a subfocus_widgets list of a widget with
    grab_focus set to True'''

    grab_keys = ListProperty()
    '''List with integer key codes of keys that will be grabbed before
    kb_system searches and calls a global hotkey callback.
    Return True from on_key_dow or on_key_up method
    to allow calling global hotkeys'''

    grab_focus = BooleanProperty(False)
    '''Add widget to focus_grab_widgets or focusable_widgets,
    default is False'''

    is_focusable = BooleanProperty(False)

    receive_textinput = False

    def __init__(self, **kwargs):
        self.register_event_type('on_focus_textinput')
        super(FocusBehavior, self).__init__(**kwargs)
        self.fbind('focus', self.remove_other_focused)
        self.fbind('is_focusable', self.update_is_focusable)
        if not self.is_subfocus:
            self.bind(parent=on_parent)
            if self.grab_focus:
                self.focus_widget(self)

    def update_is_focusable(self, _, value):
        global focus_grab_widgets, focusable_widgets
        if value:
            if self.grab_focus and not self in focus_grab_widgets:
                self.on_grab_focus(None, True)
            elif not self.grab_focus and not self in focusable_widgets:
                on_parent(self, self.parent)
        else:
            self.remove_from_focus()

    def on_grab_focus(self, _, value):
        self.remove_from_focus()
        if self.parent:
            on_parent(self, self.parent)
            if value:
                self.focus_widget(self)

    def on_is_subfocus(self, _, value):
        if value:
            self.funbind('parent', on_parent)
            self.remove_from_focus()
        else:
            self.bind(parent=on_parent)

    def remove_from_focus(self, prev_focus=False):
        '''Remove widget from focusable_widgets or focus_grab_widgets list'''
        global current_focus, prev_focused_widgets, focus_grab_widgets
        global prev_focused_widgets
        if current_focus == self:
            remove_focus()
        if self.grab_focus and self in focus_grab_widgets:
            focus_grab_widgets.remove(self)
        elif self in focusable_widgets:
            focusable_widgets.remove(self)
        remlist = [
            i for i, x in enumerate(prev_focused_widgets) if x() == self]
        for x in reversed(remlist):
            del prev_focused_widgets[x]
        if prev_focus:
            Clock.schedule_once(set_focus_previous, 0)

    def remove_other_focused(self, _, value):
        '''Sets current_focus.focus to False if current_focus is not self,
        Then calls set_focus(self)'''
        global current_focus
        if value:
            if current_focus != self:
                remove_focus()
                set_focus(self)

    def focus_widget(self, *args):
        '''Focus this widget'''
        set_focus(self)

    def on_key_down(self, key, *args):
        pass

    def on_key_up(self, key, *args):
        pass

    def on_focus_textinput(self, text):
        pass
