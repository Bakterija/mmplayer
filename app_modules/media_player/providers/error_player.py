

class ErrorPlayer(object):
    length = -1
    volume = 1.
    loop = False
    is_video = False
    is_seeking = False
    seek_pos = 0
    state = 'error'

    def play(self):
        pass

    def pause(self):
        pass

    def on_stop(self, *args):
        pass

    def stop(self):
        pass

    def seek(self, position):
        pass

    def get_pos(self):
        return -1

    def load(self, path):
        pass

    def unload(self):
        pass

    def bind(self, **kwargs):
        pass

    @staticmethod
    def try_loading(mplayer, path):
        return None
