from kivy.properties import BooleanProperty, NumericProperty
from kivy.uix.widget import Widget
from kivy.core.window import Window

class HoverBehavior(Widget):
    hovering = BooleanProperty(False)
    hover_resize_x = NumericProperty()
    hover_resize_y = NumericProperty()

    def __init__(self, **kwargs):
        super(HoverBehavior, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouse_move)

    def on_mouse_move(self, win, (posx, posy)):
        if self.hovering == False:
            if self.collide_point_window(posx, posy):
                self.hovering = True
                self.on_enter()
        else:
            if self.collide_point_window(posx, posy) == False:
                self.hovering = False
                self.on_leave()

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
