from __future__ import print_function
from kivy.properties import NumericProperty, BooleanProperty
from kivy.properties import StringProperty, ListProperty
from widgets.hover_canvas_button import HoverCanvasButton
from kivy_soil.hover_behavior import HoverBehavior
from .slider_progress_bar import SliderProgressBar
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.stacklayout import StackLayout
from widgets.imagebutton import ImageButton
from utils import seconds_to_minutes_hours
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.metrics import cm, dp
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.clock import Clock
from time import time
from sys import path

class PlayBackButton(HoverCanvasButton):
    img_pause = StringProperty('data/4/play4')
    '''Path of "Pause" button image'''

    img_prev = StringProperty('data/4/play1')
    '''Path of "Previous" button image'''

    img_play = StringProperty('data/4/play2')
    '''Path of "Play" button image'''

    img_next = StringProperty('data/4/play3')
    '''Path of "Next" button image'''

    text = StringProperty()
    '''Text of button, not displayed, but used to switch images from paths'''

    def on_text(self, _, text):
        '''Updates source image path from text'''
        if text == 'Previous':
            self.source = ''.join((self.img_prev, '.png'))
        elif text == 'Play':
            self.source = ''.join((self.img_play, '.png'))
        elif text == 'Next':
            self.source = ''.join((self.img_next, '.png'))
        elif text == 'Pause':
            self.source = ''.join((self.img_pause, '.png'))


class PlayBackBar(BoxLayout):
    orientation = 'horizontal'
    background_color = ListProperty([0.1, 0.1, 0.1])
    path = path[0]+'/playback_bar/'
    '''Path of module'''

    media_progress_max = NumericProperty(0)
    '''NumericProperty of current media length in seconds'''

    media_progress_val = NumericProperty(0)
    '''NumericProperty of media player positon in seconds'''

    media_volume = NumericProperty(50.0)
    '''NumericProperty on which volume slider is binded'''

    media_progress_val_readable = StringProperty('00:00')
    '''StringProperty of media player position,
    divmoded and filled into hours:minutes:seconds
    '''

    media_progress_max_readable = StringProperty('00:00')
    '''StringProperty of current media length,
    divmoded and filled into hours:minutes:seconds
    '''

    shuffle = BooleanProperty(False)
    muted = BooleanProperty(False)

    def __init__(self, **kwargs):
        self.register_event_type('on_set_seek')
        self.register_event_type('on_set_volume')
        self.register_event_type('on_toggle_mute')
        self.register_event_type('on_toggle_shuffle')
        super(PlayBackBar, self).__init__(**kwargs)
        Clock.schedule_once(self.do_bindings, 0)

    def do_bindings(self, *args):
        self.ids.btn_volume.bind(on_press=self._dispatch_mute_toggle)
        self.ids.btn_shuffle.bind(on_press=self._dispatch_shuffle_toggle)
        self.ids.slider_volume.do_callback_on_move = True
        self.ids.slider_volume.callback = self._dispatch_volume_update
        self.ids.slider_seek.callback = self._dispatch_seek_update
        self.ids.slider_seek.bind(value=self.update_media_progress)

    def _dispatch_seek_update(self, value):
        self.dispatch('on_set_seek', value)

    def _dispatch_volume_update(self, value):
        self.dispatch('on_set_volume', value)

    def _dispatch_mute_toggle(self, *args):
        self.dispatch('on_toggle_mute')

    def _dispatch_shuffle_toggle(self, *args):
        self.dispatch('on_toggle_shuffle')

    def on_set_seek(self, value):
        pass

    def on_set_volume(self, value):
        pass

    def on_toggle_mute(self):
        pass

    def on_toggle_shuffle(self):
        pass

    def update_media_progress(self, _, value):
        s = seconds_to_minutes_hours(value)
        self.media_progress_val_readable = s

    def on_media_progress_val(self, _, value):
        if not self.ids.slider_seek.touching:
            self.update_media_progress(None, value)

    def on_media_progress_max(self, _, value):
        s = seconds_to_minutes_hours(value)
        self.media_progress_max_readable = s

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


Builder.load_file('playback_bar/bar.kv')
