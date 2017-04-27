from __future__ import print_function
from kivy.uix.video import Video as Video
from kivy.properties import NumericProperty
from kivy.compat import PY2


class AppVideoPlayer(Video):
    modified_stop_callback = None
    length = NumericProperty(-1)
    is_video = True

    def __init__(self, mplayer, **kwargs):
        super(AppVideoPlayer, self).__init__(**kwargs)
        self.length = self.duration
        self.bind(duration=self.setter('length'))
        self.allow_stretch = True
        self.mplayer = mplayer
        self.bind(on_stop = mplayer.on_stop)

    def load(self, path):
        if PY2 and type(path) == unicode:
            path = path.encode('utf-8')
        self.source = path
        self.state = 'play'
        self.async = False
        self.options = {'allow_stretch': True}

    def play(self):
        self.state = 'play'

    def pause(self):
        self.state = 'pause'

    def stop(self):
        self.state = 'stop'

    def set_texture_si(self, *args):
        self.texture_size = self.size

    def on_state(self, instance, value):
        super(AppVideoPlayer, self).on_state(instance, value)
        if value == 'stop' and self.modified_stop_callback:
            self.modified_stop_callback()

    def seek(self, value):
        value = float(value)
        length =  float(self.length)
        fn = value / length
        super(AppVideoPlayer, self).seek(fn)

    def get_pos(self):
        return self.position

    def bind(self, **kwargs):
        super(AppVideoPlayer, self).bind(**kwargs)
        if 'on_stop' in kwargs:
            self.modified_stop_callback = kwargs['on_stop']

    def _play_started(self, instance, value):
        self.container.clear_widgets()
        self.container.add_widget(self._video)

    @staticmethod
    def try_loading(mplayer, path):
        if path[-4:] in ('.mp4', '.mkv'):
            return AppVideoPlayer(mplayer)
        else:
            return None
