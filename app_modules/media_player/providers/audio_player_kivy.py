from kivy.core.audio import SoundLoader
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from kivy.event import EventDispatcher


class AudioPlayer(EventDispatcher):
    source = StringProperty()
    length = NumericProperty(-1)
    pause_seek = NumericProperty()
    volume = NumericProperty(1.)
    loop = BooleanProperty(False)
    is_video = False
    is_seeking = False
    seek_pos = 0
    state = 'stop'

    def __init__(self, mplayer, **kwargs):
        super(AudioPlayer, self).__init__(**kwargs)
        self.mplayer = mplayer

    def on_volume(self, instance, value):
        self.sound.volume = value

    def play(self):
        self.sound.play()
        if self.pause_seek:
            self.seek(self.pause_seek)
        self.state = 'play'

    def pause(self):
        self.pause_seek = self.get_pos()
        self.state = 'pause'
        self.sound.stop()

    def on_stop(self, *args):
        if self.state != 'pause':
            self.mplayer.on_stop()

    def stop(self):
        self.sound.stop()
        self.state = 'stop'

    def seek(self, position):
        self.is_seeking = True
        self.seek_pos = position
        self.sound.seek(position)

    def get_pos(self):
        if self.state == 'stop':
            return -1
        if self.state == 'pause':
            return self.pause_seek
        if self.is_seeking:
            if not self.sound.get_pos():
                return self.seek_pos
            else:
                self.is_seeking = False
        return self.sound.get_pos()

    def load(self, path):
        self.sound = SoundLoader.load(path)
        self.length = self.sound.length
        self.sound.bind(on_length=self.setter('length'))
        self.sound.bind(on_stop = self.on_stop)
        self.bind(volume=self.on_volume)

    def unload(self):
        self.sound.unload()

    def bind(self, **kwargs):
        super(AudioPlayer, self).bind(**kwargs)

    @staticmethod
    def try_loading(mplayer, path):
        if path[-4:] in ('.wav', '.mp3', '.ogg', '.m4a'):
            return AudioPlayer(mplayer)
        else:
            return None
