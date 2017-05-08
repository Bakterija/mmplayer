from __future__ import print_function
from kivy.uix.video import Video as Video
from kivy.properties import NumericProperty
from kivy.resources import resource_find
from kivy.compat import PY2
from kivy.logger import Logger


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

    def on_texture(self, _, value):
        if value:
            self.mplayer.on_video(True)
        else:
            self.mplayer.on_video(False)

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

    def unload(self):
        self.mplayer.on_video(False)
        super(AppVideoPlayer, self).unload()

    def texture_update(self, *largs):
        if not self.source:
            self.texture = None
        else:
            filename = resource_find(self.source)
            self._loops = 0
            if filename is None:
                return Logger.error('Image: Error reading file {filename}'.
                                    format(filename=self.source))
            mipmap = self.mipmap
            if self._coreimage is not None:
                self._coreimage.unbind(on_texture=self._on_tex_change)
            try:
                if PY2 and isinstance(filename, str):
                    filename = filename.decode('utf-8')
                self._coreimage = ci = CoreImage(filename, mipmap=mipmap,
                                                 anim_delay=self.anim_delay,
                                                 keep_data=self.keep_data,
                                                 nocache=self.nocache)
            except:
                self._coreimage = ci = None

            if ci:
                ci.bind(on_texture=self._on_tex_change)
                self.texture = ci.texture

    @staticmethod
    def try_loading(mplayer, path):
        if path[-4:] in ('.mp4', '.mkv', '.flv'):
            return AppVideoPlayer(mplayer)
        else:
            return None
