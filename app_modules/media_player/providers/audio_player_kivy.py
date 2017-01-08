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
        self.sound.stop()
        self.state = 'pause'

    def stop(self):
        self.sound.stop()
        self.state = 'stop'

    def seek(self, position):
        self.sound.seek(position)

    def get_pos(self):
        if self.state == 'stop':
            return -1
        if self.state == 'pause':
            return self.pause_seek
        return self.sound.get_pos()

    def load(self, path):
        self.sound = SoundLoader.load(path)
        self.length = self.sound.length
        self.sound.bind(on_length=self.setter('length'))
        self.sound.bind(on_stop = self.mplayer.on_stop)
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
