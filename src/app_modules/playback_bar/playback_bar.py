from __future__ import print_function
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.properties import (
    NumericProperty, StringProperty, ListProperty, BooleanProperty)
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import cm, dp
from kivy.lang import Builder
from kivy.graphics import *
from app_modules.behaviors.hover_behavior import HoverBehavior
from kivy.clock import Clock
from sys import path
from app_modules.widgets_standalone.imagebutton import ImageButton
from .slider_progress_bar import SliderProgressBar
from kivy.uix.label import Label


class PlayBackButton(ImageButton, HoverBehavior):
    background_normal = ListProperty([0.3, 0.3, 0.3, 0])
    background_down = ListProperty([0, 0.4, 0.5, 0.5])
    background_hover = ListProperty([0, 0, 1, 0.5])
    background_current = ListProperty([0.1, 0.1, 1, 1])
    pressing = BooleanProperty(False)
    text = StringProperty()

    def __init__(self, **kwargs):
        super(PlayBackButton, self).__init__(**kwargs)
        self.background_current = self.background_normal
        self.bind(on_press=self.update_bg_on_press)
        self.bind(on_release=self.update_bg_on_release)

    def update_bg_on_press(self, p):
        self.background_current = self.background_down
        self.pressing = True

    def update_bg_on_release(self, p):
        if self.hovering:
            self.background_current = self.background_hover
        else:
            self.background_current = self.background_normal
        self.pressing = True

    def on_text(self, _, text):
        if text == 'Previous':
            self.source = self.parent.img_prev
        elif text == 'Play':
            self.source = self.parent.img_play
        elif text == 'Next':
            self.source = self.parent.img_next
        elif text == 'Pause':
            self.source = self.parent.img_pause

    def on_enter(self):
        self.background_current = self.background_hover

    def on_leave(self):
        self.background_current = self.background_normal


class PlayBackBar(BoxLayout):
    orientation = 'horizontal'
    img_pause = StringProperty('data/4/play4.png')
    img_prev = StringProperty('data/4/play1.png')
    img_play = StringProperty('data/4/play2.png')
    img_next = StringProperty('data/4/play3.png')
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


Builder.load_file('app_modules/playback_bar/bar.kv')
