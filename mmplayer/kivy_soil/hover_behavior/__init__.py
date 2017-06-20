from kivy.properties import BooleanProperty, NumericProperty
from kivy.uix.widget import Widget
from kivy.core.window import Window
from time import time
import weakref

_hover_grab_widget = None
'''Weak reference to widget which has grabbed hover'''

_hover_widgets = []
'''Weak references to all HoverBehavior instances'''

min_hover_height = 0
'''Minimum widget hover_height where widget hover will be set to True'''

def on_mouse_move(win, pos):
    '''Compares mouse position with widget positions
    and sets hover to false or true'''
    global _hover_widgets, min_hover_height, _hover_grab_widget
    hovered = []
    if _hover_grab_widget:
        hover_widget_refs = [_hover_grab_widget]
    else:
        hover_widget_refs = _hover_widgets
    t0 = time()
    for ref in hover_widget_refs:
        self = ref()
        if self:
            if self.collide_point_window(*pos):
                # Get all widgets that are at mouse pos
                hovered.append(self)
            # Remove hover from all widgets that are not at mouse pos
            elif self.hovering:
                self.hovering = False
                self.on_leave()

        if hovered:
            # Find the highest widget and set it's hover to True
            # Set hover to False for other widgets
            highest = hovered[0]
            if len(hovered) > 1:
                for self in hovered:
                    if self.hover_height > highest.hover_height:
                        if highest.hovering:
                            highest.hovering = False
                            highest.on_leave()
                        highest = self
                    elif self.hovering:
                        self.hovering = False
                        self.on_leave()

                if highest.hover_height < min_hover_height:
                    return

            if not highest.hovering:
                highest.hovering = True
                highest.on_enter()

Window.bind(mouse_pos=on_mouse_move)


class HoverBehavior(Widget):
    '''Widget behavior with hovering property that is set
    to True when mouse is hovering over the widget and to False when not.
    Also has on_enter and on_leave methods that get called when
    hover state changes'''

    hovering = BooleanProperty(False)
    '''Hover state, is True when mouse enters it's position'''

    hover_height = 0
    '''Z axis height, heighest widgets take priority in hover system'''

    def __init__(self, **kwargs):
        super(HoverBehavior, self).__init__(**kwargs)
        self.bind(parent=self._on_parent_update_hover)

    def _on_parent_update_hover(self, _, parent):
        '''Adds self to hover system when has a parent,
        otherwise removes self from hover system'''
        global _hover_widgets
        if parent:
            _hover_widgets.append(weakref.ref(self))
        else:
            d = -1
            for i, x in enumerate(_hover_widgets):
                if x() == self:
                    d = i
                    break
            if d != -1:
                del _hover_widgets[d]

    def remove_from_hover_behavior(self):
        '''Remove widget from hover system'''
        global _hover_widgets
        _hover_widgets.remove(self)

    @staticmethod
    def force_update_hover(*a):
        on_mouse_move(None, Window.mouse_pos)

    def on_enter(self, *args):
        '''Is called when mouse enters widget position'''
        pass

    def on_leave(self, *args):
        '''Is called when mouse leaves widget position'''
        pass

    def grab_hover(self, *args):
        global _hover_grab_widget
        _hover_grab_widget = weakref.ref(self)

    def ungrab_hover(self, *args):
        global _hover_grab_widget
        if _hover_grab_widget() == self:
            _hover_grab_widget = None

    def collide_point_window(self, x, y):
        sx, sy = self.to_window(self.x, self.y)
        return sx <= x <= sx + self.width and sy <= y <= sy + self.height
