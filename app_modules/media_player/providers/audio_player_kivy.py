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
        self.state = 'play'
        if self.pause_seek:
            self.seek(self.pause_seek)

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
        if self.length > 0:
            if self.state in ('pause', 'stop'):
                self.pause_seek = position
            else:
                self.sound.seek(position)

    def get_pos(self):
        if self.state == 'stop':
            return -1
        if self.state == 'pause':
            return self.pause_seek
        if self.length == -1:
            self.length = self.sound.length
        return self.sound.get_pos()

    def load(self, path):
        if type(path) == unicode:
            path = path.encode('utf-8')
        self.sound = SoundLoader.load(path)
        self.sound.bind(on_stop= self.on_stop)
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
