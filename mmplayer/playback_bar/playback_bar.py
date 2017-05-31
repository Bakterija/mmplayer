from __future__ import print_function
from kivy.properties import NumericProperty, BooleanProperty
from kivy.properties import StringProperty, ListProperty
from kivy_soil.hover_behavior import HoverBehavior
from .slider_progress_bar import SliderProgressBar
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.stacklayout import StackLayout
from widgets.imagebutton import ImageButton
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.metrics import cm, dp
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.clock import Clock
from sys import path


class PlayBackButton(HoverBehavior, ImageButton):
    img_pause = StringProperty('data/4/play4')
    img_prev = StringProperty('data/4/play1')
    img_play = StringProperty('data/4/play2')
    img_next = StringProperty('data/4/play3')
    text = StringProperty()

    def __init__(self, **kwargs):
        super(PlayBackButton, self).__init__(**kwargs)
        self.update_source_bg(self.text, self.hovering, self.state)

    def on_state(self, _, value):
        '''Updates images when player state changes'''
        self.update_source_bg(self.text, self.hovering, value)

    def update_source_bg(self, text, hover, press):
        '''Updates playback button image paths'''
        mod = ''
        if press == 'down':
            mod = '_d'
        elif hover:
            mod = '_h'
        if text == 'Previous':
            self.source = ''.join((self.img_prev, mod, '.png'))
        elif text == 'Play':
            self.source = ''.join((self.img_play, mod, '.png'))
        elif text == 'Next':
            self.source = ''.join((self.img_next, mod, '.png'))
        elif text == 'Pause':
            self.source = ''.join((self.img_pause, mod, '.png'))

    def on_text(self, _, text):
        '''Calls self.update_source_bg()'''
        self.update_source_bg(text, self.hovering, self.state)

    def on_enter(self):
        '''Calls self.update_source_bg()'''
        self.update_source_bg(self.text, self.hovering, self.state)

    def on_leave(self):
        '''Calls self.update_source_bg()'''
        self.update_source_bg(self.text, self.hovering, self.state)


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

    dont_update_progress = False
    '''media_progress_val updates are skipped when this is True,
    default is False'''

    skip_progress2 = False
    '''media_progress_val updates are skipped when this is True,
    default is False'''

    progress_clock = None
    '''References last clock that was or will be used to reenable
    media_progress_val updates'''


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
        self.ids.progress1.bind(on_touch_up=self.update_media_progress)
        self.ids.progress1.bind(on_touch_move=self.update_media_progress)
        self.ids.progress2.bind(on_touch_move=self.update_media_volume)
        self.ids.progress2.bind(on_touch_up=self.update_media_volume)

    def update_media_progress(self, widget, value):
        self.media_progress_val = widget.value

    def update_media_volume(self, widget, value):
        self.media_volume = widget.value

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


Builder.load_file('playback_bar/bar.kv')
