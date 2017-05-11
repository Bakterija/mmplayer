from __future__ import print_function
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.progressbar import ProgressBar
from kivy.uix.button import Button
from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import cm, dp
from kivy.lang import Builder
from kivy.graphics import *
from app_modules.behaviors.hover_behavior import HoverBehavior
from kivy.clock import Clock
from sys import path


kv = '''
<PlayBackBar>:
    playb_width: int(cm(3))
    playb_width_small: int(cm(2))
    spacing: 0
    canvas.before:
        Color:
            rgb: self.background_color
        Rectangle:
            size: self.size
            pos: self.pos

    PlayBackButton:
        id: btn1
        size_hint_x: None
        width: root.playb_width_small
        text: 'Previous'
        on_release: root.on_prevbtn()

    PlayBackButton:
        id: btn2
        size_hint_x: None
        width: root.playb_width
        text: 'Play'
        on_release: root.on_playbtn()

    PlayBackButton:
        id: btn3
        size_hint_x: None
        width: root.playb_width_small
        text: 'Next'
        on_release: root.on_nextbtn()

    Widget:
        id: sep1
        size_hint_x: None
        width: cm(0.5)

    Label:
        id: progress_label1
        size_hint_x: None
        width: self.texture_size[0] + cm(0.5)
        text: root.media_progress_val_readable
    SliderProgressBar:
        id: progress1
        size_hint_x: None
        width: root.width - btn1.width - btn2.width - btn3.width - sep1.width - sep2.width - progress2.width - cm(0.5) - progress_label1.width - progress_label2.width
        max: root.media_progress_max
    Label:
        id: progress_label2
        size_hint_x: None
        width: self.texture_size[0] + cm(0.5)
        text: root.media_progress_max_readable

    Widget:
        id: sep2
        size_hint_x: None
        width: cm(0.5)

    SliderProgressBar:
        id: progress2
        size_hint_x: None
        width: cm(2.5)
        max: 100.0
        value: int(self.seeking_touch_value) if self.seeking_touch else int(root.media_volume)
'''


class SliderProgressBar(ProgressBar):
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
        circlesource = 'data/circle.png'
        self.circle = Image(source=circlesource, pos=(-999,-999), size=(
            self.circle_size, self.circle_size))
        self.add_widget(self.circle)

    def on_mouse_move(self, win, pos):
        chalf = self.circle_size * 0.5
        if self.collide_point_window(*pos) or self.seeking_touch:
            self.move_circle_to_progress()
        else:
            self.hide_circle()

    def hide_circle(self, *args):
        chalf = self.circle_size * 0.5
        self.circle.pos = (-999 - chalf, -999 - chalf)

    def move_circle_to_progress(self, *args):
        chalf = self.circle_size * 0.5
        if not self.value:
            x_new = self.x - chalf
        else:
            x_new = self.x + (self.width / self.max * self.value) - chalf
        self.circle.pos = (x_new, self.y + self.height * 0.5 - chalf)

    def on_value_update(self, widget, value):
        if self.value != value:
            if self.seeking_touch:
                self.value = self.seeking_touch_value
            else:
                self.value = value
                if self.hovering:
                    self.move_circle_to_progress()

    def on_touch_down(self, touch):
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
        if touch.button in ('scrollup', 'scrolldown', 'right'):
            return False
        if self.seeking_touch:
            self.seeking_touch = False
            touch.ungrab(self)
            self.on_seeking(self.value)
            return True

    def on_touch_move(self, touch):
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


class PlayBackButton(HoverBehavior, Button):
    hovercolors = [[0.7, 0.7, 0.7, 1], [0.6, 0.8, 0.6, 1]]
    def __init__(self, **kwargs):
        super(PlayBackButton, self).__init__(**kwargs)
        self.hovercolors[0] = self.background_color

    def on_enter(self, *args):
        self.background_color = self.hovercolors[1]

    def on_leave(self, *args):
        self.background_color = self.hovercolors[0]


class ButtonImage(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(ButtonImage, self).__init__(**kwargs)


class PlayBackBar(BoxLayout):
    orientation = 'horizontal'
    background_color = ListProperty([0.1, 0.1, 0.1])
    path = path[0]+'/app_modules/playback_bar/'
    media_progress_max = NumericProperty(0)
    media_progress_val = NumericProperty(0)
    media_volume = NumericProperty(50.0)
    media_progress_val_readable = StringProperty('00:00')
    media_progress_max_readable = StringProperty('00:00')
    dont_update_progress = False
    skip_progress2 = False
    progress_clock = None

    def __init__(self, **kwargs):
        super(PlayBackBar, self).__init__(**kwargs)
        self.on_media_progress_val()
        self.on_media_progress_max()
        Clock.schedule_once(self.bind_children_clock, 0)

    def bind_children_clock(self, *args):
        self.ids.progress1.on_seeking = lambda *args: self.on_seeking(*args)
        self.bind(media_progress_val=self.ids.progress1.on_value_update)
        self.ids.progress1.bind(on_touch_down=self.toggle_progress_update)
        self.ids.progress1.bind(on_touch_up=self.toggle_progress_update)
        self.ids.progress1.bind(on_touch_up=lambda obj, val: setattr(
            self, 'media_progress_val', self.ids.progress1.value))
        self.ids.progress1.bind(on_touch_move=lambda obj, val: setattr(
            self, 'media_progress_val', self.ids.progress1.value))
        self.ids.progress2.bind(on_touch_move=lambda obj, val: setattr(
            self, 'media_volume', self.ids.progress2.value))
        self.ids.progress2.bind(on_touch_up=lambda obj, val: setattr(
            self, 'media_volume', self.ids.progress2.value))

    def get_readable_from_int(self, seconds):
        seconds = int(seconds)
        m, s = divmod(seconds, 60)
        s = str(m).zfill(2)+':'+str(s).zfill(2)
        return s

    def toggle_progress_update(self, *args):
        if self.dont_update_progress:
            self.dont_update_progress = False
            self.skip_progress2 = True
            if self.skip_progress2:
                Clock.unschedule(self.progress_clock)
            self.progress_clock = Clock.schedule_once(
                lambda *a: setattr(self, 'skip_progress2', False), 0.6)
        else:
            self.dont_update_progress = True

    def on_media_progress_val(self, *args):
        if self.skip_progress2:
            return
        if args:
            if self.dont_update_progress == False:
                self.media_progress_val = args[1]
            s = self.get_readable_from_int(self.media_progress_val)
            self.media_progress_val_readable = s

    def on_media_progress_max(self, *args):
        if args:
            if self.dont_update_progress == False:
                self.media_progress_max = args[1]
            s = self.get_readable_from_int(self.media_progress_max)
            self.media_progress_max_readable = s

    def volume_increase(self, *args):
        if self.media_volume < 100:
            self.media_volume += 10

    def volume_decrease(self, *args):
        if self.media_volume > 0:
            self.media_volume -= 10

    def on_playbtn(self, *args):
        pass

    def on_prevbtn(self, *args):
        pass

    def on_nextbtn(self, *args):
        pass

    def on_play(self, *args):
        self.ids.btn2.text = 'Pause'

    def on_pause(self, *args):
        self.ids.btn2.text = 'Play'

    def on_seeking(self, value):
        if self.on_seeking_function:
            self.on_seeking_function(self.value)
            s = self.get_readable_from_int(self.ids.progress1.value)
            self.media_progress_val_readable = s


Builder.load_string(kv)
