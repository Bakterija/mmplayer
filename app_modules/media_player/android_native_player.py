from jnius import autoclass
MediaPlayer = autoclass('android.media.MediaPlayer')


class Android_Native_Player:
    def __init__(self,*arg,**kwarg):
        self.enabled = False
        self.state = 'init'
        self.length = -1
        self.stopCallback = False

    def load(self,path,stream=False):
        self.player = MediaPlayer()
        if stream:
            AudioManager = autoclass('android.media.AudioManager')
            self.player.setAudioStreamType(AudioManager.STREAM_MUSIC)
        self.player.setDataSource(path)
        self.state = 'prepare'
        self.player.prepare()
        self.length = self.player.getDuration()/1000
        self.enabled = True

    def play(self,*arg):
        if self.enabled:
            self.player.start()
            self.state = 'play'

    def seek(self,value):
        if self.enabled:
            value = value*1000.0
            self.player.seekTo(int(value))

    def stop(self,*arg):
        if self.enabled:
            self.player.pause()
            self.state = 'stop'

    def unload(self,*arg):
        if self.enabled:
            self.player.release()
            self.enabled = False

    def get_pos(self,*arg):
        if self.enabled:
            # self.length = self.player.getDuration()/1000
            pos = self.player.getCurrentPosition()/1000
            if pos == self.length:
                self.state = 'stop'
                self.stopCallback()
            return pos
        else:
            return 0

    def bind(self,*arg,**kwarg):
        kwarg.setdefault('on_stop',False)
        if kwarg['on_stop'] != False: self.stopCallback = kwarg['on_stop']
