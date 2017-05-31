from kivy.properties import NumericProperty, BooleanProperty
from behaviors.resizable.resize import ResizableBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation


class SmallVideo(ResizableBehavior, BoxLayout):
    '''BoxLayout with ResizableBehavior that holds media player video widget
    when video screen is not in view'''

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

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if touch.button == 'left':
                if self.check_resizable_side(*touch.pos):
                    super(SmallVideo, self).on_touch_down(touch)
                else:
                    self.on_video_touch()
            return True

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            if touch.button == 'scrolldown':
                self.on_video_scroll_down()
            elif touch.button == 'scrollup':
                self.on_video_scroll_up()
            else:
                super(SmallVideo, self).on_touch_up(touch)
            return True

    def on_video_scroll_up(self, *args):
        pass

    def on_video_scroll_down(self, *args):
        pass

    def on_video_touch(self, *args):
        pass
