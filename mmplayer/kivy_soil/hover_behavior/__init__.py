__all__ = ('HoverBehavior', )

from kivy.properties import BooleanProperty, NumericProperty, ObjectProperty
from kivy.weakproxy import WeakProxy
from kivy.core.window import Window


class HoverBehavior(object):
    '''
    The HoverBehavior `mixin <https://en.wikipedia.org/wiki/Mixin>`_ provides
    Hover behavior. When combined with a widget, hovering mouse cursor
    above it's position will call it's on_hovering event.
    '''

    _hover_grab_widget = None
    '''WeakProxy of widget which has grabbed focus or None'''

    _hover_widgets = []
    '''List of hover widget WeakProxy references'''

    min_hover_height = 0
    '''Numeric class attribute of minimum height where "hovering" property
    will be updated'''

    hovering = BooleanProperty(False)
    '''Hover state, is True when mouse enters it's position

    :attr:`hovering` is a :class:`~kivy.properties.BooleanProperty` and
    defaults to `False`.
    '''

    hover_height = NumericProperty(0)
    '''Number that is compared to min_hover_height.

    :attr:`hover_height` is a :class:`~kivy.properties.NumericProperty` and
    defaults to `0`.
    '''

    def _on_hover_mouse_move(win, pos):
        '''Internal method that is binded on Window.mouse_pos.
        Compares mouse position with widget positions,
        ignoring disabled widgets and widgets with hover_height below
        HoverBehavior.min_hover_height,
        then sets widget hovering property to False or True'''

        collided = [] # widget weak proxies that collide with mouse pos

        if HoverBehavior._hover_grab_widget:
            HoverBehavior.hover_widget_refs = [HoverBehavior._hover_grab_widget]
        else:
            HoverBehavior.hover_widget_refs = HoverBehavior._hover_widgets
        for ref in HoverBehavior.hover_widget_refs:
            if not ref.disabled and ref._collide_point_window(*pos):
                # Get all widgets that are at mouse pos
                collided.append(ref)
            # Remove hover from all widgets that are not at mouse pos
            elif ref.hovering:
                ref.hovering = False

            if collided:
                # Find the highest widget and set it's hover to True
                # Set hover to False for other widgets
                highest = collided[0]
                if len(collided) > 1:
                    for ref in collided:
                        if ref.hover_height > highest.hover_height:
                            if highest.hovering:
                                highest.hovering = False
                            highest = ref
                        elif ref.hovering:
                            ref.hovering = False

                if HoverBehavior._hover_grab_widget:
                    if not highest.hovering:
                        highest.hovering = True

                elif highest.hover_height >= HoverBehavior.min_hover_height:
                    if not highest.hovering:
                        highest.hovering = True

    @staticmethod
    def force_update_hover():
        '''Gets window mouse position and updates hover state for all widgets'''
        HoverBehavior._on_hover_mouse_move(Window, Window.mouse_pos)

    @staticmethod
    def set_min_hover_height(number):
        '''Sets min_hover_height for HoverBehavior class'''
        HoverBehavior.min_hover_height = number

    @staticmethod
    def get_min_hover_height():
        '''Gets min_hover_height from HoverBehavior class'''
        return HoverBehavior.min_hover_height

    def __init__(self, **kwargs):
        super(HoverBehavior, self).__init__(**kwargs)
        self.bind(parent=self._on_parent_update_hover)

    def _on_parent_update_hover(self, _, parent):
        '''Adds self to hover system when has a parent,
        otherwise removes self from hover system'''
        if parent:
            self.hoverable_add()
        else:
            self.hoverable_remove()

    def hoverable_add(self):
        '''Add widget in hover system. By default, is called when widget
        is added to a parent'''
        HoverBehavior._hover_widgets.append(WeakProxy(self))

    def hoverable_remove(self):
        '''Remove widget from hover system. By default is called when widget
        is removed from a parent'''
        HoverBehavior._hover_widgets.remove(self)

    def grab_hover(self):
        '''Prevents other widgets from receiving hover'''
        HoverBehavior._hover_grab_widget = WeakProxy(self)

    @staticmethod
    def get_hover_grab_widget():
        '''Returns widget which has grabbed hover currently or None'''
        return HoverBehavior._hover_grab_widget

    @staticmethod
    def remove_hover_grab():
        '''Removes widget WeakProxy from hover system'''
        HoverBehavior._hover_grab_widget = None

    def _collide_point_window(self, x, y):
        '''Widget collide point method that compares arguments to
        "self.to_window(self.x, self.y)" instead of "self.x, self.y"'''
        sx, sy = self.to_window(self.x, self.y)
        return sx <= x <= sx + self.width and sy <= y <= sy + self.height


Window.bind(mouse_pos=HoverBehavior._on_hover_mouse_move)
