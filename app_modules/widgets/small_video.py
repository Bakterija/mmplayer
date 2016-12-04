from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, BooleanProperty
from kivy.animation import Animation
from app_modules.behaviors.resizable.resize import ResizableBehavior


class SmallVideo(ResizableBehavior, BoxLayout):
    offset_x_in = NumericProperty()
    offset_x_out = NumericProperty()
    offset_y_in = NumericProperty()
    offset_y_out = NumericProperty()
    offset_x = NumericProperty()
    offset_y = NumericProperty()
    inside_window = BooleanProperty(False)
    resizable_up = True
    resizable_left = True
    can_move_resize = True

    def animate_in(self, *args):
        anim = Animation(
            offset_x = self.offset_x_in, offset_y = self.offset_y_in,
            d=0.4, t='in_quad')
        anim.start(self)
        self.inside_window = True

    def animate_out(self, *args):
        anim = Animation(
            offset_x = self.offset_x_out, offset_y = self.offset_y_out,
            d=0.4, t='in_quad')
        anim.start(self)
        self.inside_window = False
