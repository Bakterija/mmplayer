from kivy.properties import BooleanProperty, NumericProperty
from kivy.uix.widget import Widget
from kivy.core.window import Window
from time import time
import weakref

_hover_widgets = []
active = True
min_hover_height = 0

def on_mouse_move(win, pos):
    global _hover_widgets, active, min_hover_height
    if not active:
        return
    hovered = []
    t0 = time()
    for ref in _hover_widgets:
        self = ref()
        if self:
            if self.collide_point_window(*pos):
                hovered.append(self)
            elif self.hovering:
                self.hovering = False
                self.on_leave()

        if hovered:
            highest = hovered[0]
            for self in hovered:
        #         # print ('HVR', self, self.hover_height, self.parent)
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
    hovering = BooleanProperty(False)
    hover_resize_x = NumericProperty()
    hover_resize_y = NumericProperty()
    hover_height = 0

    def __init__(self, **kwargs):
        super(HoverBehavior, self).__init__(**kwargs)
        self.bind(parent=self.on_parent_update_hover)

    def on_parent_update_hover(self, _, parent):
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
        global _hover_widgets
        _hover_widgets.remove(self)

    @staticmethod
    def force_update_hover(*a):
        on_mouse_move(None, Window.mouse_pos)

    def on_enter(self, *args):
        pass

    def on_leave(self, *args):
        pass

    def collide_point_window(self, x, y):
        sx, sy = self.to_window(self.x, self.y)
        sx += self.hover_resize_x
        sy += self.hover_resize_y
        width = self.width - self.hover_resize_x
        height = self.height - self.hover_resize_y
        return sx <= x <= sx + width and sy <= y <= sy + height
