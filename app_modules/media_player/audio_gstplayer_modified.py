from app_modules.other.kivy_core_gstplayer.audio_gstplayer import SoundGstplayer
from kivy.logger import Logger
from kivy.compat import PY2
from os.path import realpath
from kivy.lib.gstplayer import GstPlayer, get_gst_version
if PY2:
    from urllib import pathname2url
else:
    from urllib.request import pathname2url


def _on_gstplayer_message(mtype, message):
    if mtype == 'error':
        Logger.error('AudioGstplayer: {}'.format(message))
    elif mtype == 'warning':
        Logger.warning('AudioGstplayer: {}'.format(message))
    elif mtype == 'info':
        Logger.info('AudioGstplayer: {}'.format(message))


class SoundGstplayerModified(SoundGstplayer):
    '''This is a modified SoundGstplayer that works'''

    def load(self, uri):
        self.unload()
        uri = 'file:' + pathname2url(realpath(uri))
        self.player = GstPlayer(uri, None, self._on_gst_eos_sync,
                                _on_gstplayer_message)
        self.player.load()
        return self
