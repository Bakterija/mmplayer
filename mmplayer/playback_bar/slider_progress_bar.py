from kivy.properties import NumericProperty, ListProperty, BooleanProperty
from kivy_soil.hover_behavior import HoverBehavior
from kivy.uix.progressbar import ProgressBar
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.metrics import cm
from kivy.clock import Clock

class SliderProgressBar(HoverBehavior, ProgressBar):
    '''Progress bar for playback bar'''
    callback = None
    do_callback_on_move = False
    source_circle = 'data/circle.png'
    circle_size = ListProperty([int(cm(0.3)), int(cm(0.3))])
    circle_color = ListProperty([1, 1, 1, 0.2])
    touching = BooleanProperty(False)
    value2 = NumericProperty(50.0)

    def __init__(self, **kwargs):
        super(SliderProgressBar, self).__init__(**kwargs)
        self.circle = Image(
            source=self.source_circle, opacity=0, size=self.circle_size)
        Clock.schedule_once(self.add_circle, 0)

    def add_circle(self, *args):
        self.add_widget(self.circle)
        Window.bind(mouse_pos=self.on_mouse_move)

    def on_mouse_move(self, _, pos):
        if self.circle.opacity:
            self.move_circle_to_progress()

    def on_hovering(self, _, value):
        if value:
            self.circle.opacity = 1
        elif not self.touching:
            self.circle.opacity = 0

    def on_touching(self, _, value):
        if not value and not self.hovering:
            self.circle.opacity = 0

    def move_circle_to_progress(self, *args):
        '''Moves circle to progress bar current value'''
        chalf = self.circle_size[0] * 0.5
        if not self.value:
            x_new = self.x - chalf
        else:
            x_new = self.x + (self.width / self.max * self.value) - chalf
        self.circle.pos = (x_new, self.y + self.height * 0.5 - chalf)

    def on_value(self, _, value):
        self.move_circle_to_progress()

    def on_value2(self, _, value):
        '''Calls self.move_circle_to_progress if it is not being dragged by
        touch already, otherwise sets value from touch position'''
        if not self.touching:
            self.value = value

    def update_value_from_touch(self, touch):
        tx = touch.pos[0]
        if self.touching:
            val = ((tx - self.x) / self.width) * self.max
            if val < 0.0:
                val = 0.0
            elif val > self.max:
                val = self.max
            self.value = val

    def on_touch_down(self, touch):
        '''Starts dragging bar value with touch'''
        if touch.button in ('scrollup', 'scrolldown', 'right'):
            return False
        if self.collide_point(*touch.pos):
            touch.grab(self)
            self.touching = True
            self.update_value_from_touch(touch)
            return True

    def on_touch_up(self, touch):
        '''Stops dragging bar value with touch and calls self.on_seeking()
        with new value argument'''
        if touch.button in ('scrollup', 'scrolldown', 'right'):
            return False
        if self.touching:
            self.update_value_from_touch(touch)
            self.touching = False
            touch.ungrab(self)
            if self.callback:
                self.callback(self.value)
            return True

    def on_touch_move(self, touch):
        '''Updates progress value from touch position'''
        if self.touching:
            self.update_value_from_touch(touch)
            if self.callback and self.do_callback_on_move:
                self.callback(self.value)
            return True
