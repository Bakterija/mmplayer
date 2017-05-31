from kivy.properties import NumericProperty, ListProperty
from kivy.uix.progressbar import ProgressBar
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.metrics import cm
from kivy.clock import Clock


class SliderProgressBar(ProgressBar):
    '''Progress bar for playback bar'''
    hovering = NumericProperty(0)
    seeking_touch = False
    seeking_touch_value = NumericProperty(0)
    on_seeking_function = None
    circle_size = NumericProperty(int(cm(0.3)))
    circle_color = ListProperty([1, 1, 1, 0.2])

    def __init__(self, **kwargs):
        super(SliderProgressBar, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouse_move)
        Window.bind(on_cursor_leave=self.hide_circle)
        Clock.schedule_once(self.after_init, 0)

    def after_init(self, *args):
        '''Loads circle image widget and adds it to self'''
        circlesource = 'data/circle.png'
        self.circle = Image(source=circlesource, pos=(-999,-999), size=(
            self.circle_size, self.circle_size))
        self.add_widget(self.circle)

    def on_mouse_move(self, win, pos):
        '''Moves circle to mouse position when near SliderProgressBar'''
        chalf = self.circle_size * 0.5
        if self.collide_point_window(*pos) or self.seeking_touch:
            self.move_circle_to_progress()
        else:
            self.hide_circle()

    def hide_circle(self, *args):
        '''Moves circle off screen'''
        chalf = self.circle_size * 0.5
        self.circle.pos = (-999 - chalf, -999 - chalf)

    def move_circle_to_progress(self, *args):
        '''Moves circle to progress bar current value'''
        chalf = self.circle_size * 0.5
        if not self.value:
            x_new = self.x - chalf
        else:
            x_new = self.x + (self.width / self.max * self.value) - chalf
        self.circle.pos = (x_new, self.y + self.height * 0.5 - chalf)

    def on_value_update(self, widget, value):
        '''Calls move_circle_to_progress if it is not being dragged by
        touch already, otherwise sets value from touch position'''
        if self.value != value:
            if self.seeking_touch:
                self.value = self.seeking_touch_value
            else:
                self.value = value
                if self.hovering:
                    self.move_circle_to_progress()

    def on_touch_down(self, touch):
        '''Starts dragging bar value with touch'''
        if touch.button in ('scrollup', 'scrolldown', 'right'):
            return False
        if self.collide_point(touch.pos[0], touch.pos[1]):
            touch.grab(self)
            self.seeking_touch = True
            self.on_touch_move(touch)
            if self.max:
                self.move_circle_to_progress()
            return True

    def on_touch_up(self, touch):
        '''Stops dragging bar value with touch and calls self.on_seeking()
        with new value argument'''
        if touch.button in ('scrollup', 'scrolldown', 'right'):
            return False
        if self.seeking_touch:
            self.seeking_touch = False
            touch.ungrab(self)
            self.on_seeking(self.value)
            return True

    def on_touch_move(self, touch):
        '''Updates progress value from touch position'''
        tx = touch.pos[0]
        if self.seeking_touch:
            val = ((tx - self.x) / self.width) * self.max
            if val < 0.0:
                val = 0.0
            elif val > self.max:
                val = self.max
            self.seeking_touch_value = val
            self.value = self.seeking_touch_value

    def on_seeking(self, *args):
        pass

    def collide_point_window(self, x, y):
        sx, sy = self.to_window(self.x, self.y)
        return sx <= x <= sx + self.width and sy <= y <= sy + self.height
