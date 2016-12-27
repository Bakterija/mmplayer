from __future__ import print_function
from kivy.core.audio import SoundLoader
from video_player_modified import VideoPlayerModified
from audio_gstplayer_modified import SoundGstplayerModified
from kivy.utils import platform
from threading import Thread
from time import sleep
import traceback
if platform == 'android':
    from android_intents import android_fileExt_activity
    from android_native_player import Android_Native_Player


def start_audio_kivy(self, place):
    ID, (name, path) = self.playlist.get_current()
    if type(path) == unicode:
        path = path.encode('utf-8')
    self.sound = SoundLoader.load(path)
    if self.sound:
        self.sound.play()
        self.sound.bind(on_stop=self.on_stop)
        return name

def start_audio_external(self, place):
    ID, (name, path) = self.playlist.get_current()
    if type(path) == unicode:
        path = path.encode('utf-8')
    self.player = 'external'
    android_fileExt_activity("audio/*",path+name)
    return 'External player'

def start_video_kivy(self, place):
    ID, (name, path) = self.playlist.get_current()
    if type(path) == unicode:
        path = path.encode('utf-8')
    self.pauseSupported = True
    self.sound = VideoPlayerModified(source=path, state='play', async=False, options={'allow_stretch': True})
    self.sound.bind(on_stop= self.on_stop)
    return name

def start_video_external(self,place):
    ID, (name, path) = self.playlist.get_current()
    if type(path) == unicode:
        path = path.encode('utf-8')
    self.player = 'external'
    android_fileExt_activity("video/*",path)
    return 'External player'

def start_video_no_video(self, place):
    ID, (name, path) = self.playlist.get_current()
    if type(path) == unicode:
        path = path.encode('utf-8')
    self.sound = VideoPlayerModified(source=path, state='play', options={'allow_stretch': True})
    return name

def start_android_audio(self, place):
    ID, (name, path) = self.playlist.get_current()
    if type(path) == unicode:
        path = path.encode('utf-8')
    self.player = 'audio'
    self.sound = Android_Native_Player()
    self.sound.load(path)
    self.sound.play()
    self.sound.bind(on_stop= self.on_stop)
    self.stream = False
    self.pauseSupported = True
    return name

def start_android_video(self, place):
    ID, (name, path) = self.playlist.get_current()
    if type(path) == unicode:
        path = path.encode('utf-8')
    self.player = 'video2'
    self.sound = Android_Native_Player()
    self.sound.load(path)
    self.sound.play()
    self.sound.bind(on_stop= self.on_stop)
    self.stream = False
    self.pauseSupported = True
    return name

def start_stream_kivy(self,place):
    ID, (name, path) = self.playlist.get_current()
    if platform == 'linux':
        import testplayer
        class Gst_Stream_Timer:
            def __init__(self,parent,player):
                self.parent,self.player,self.looping = parent,player,True
                Thread(target=self.start_thread).start()
                # Window.bind(on_close=self.stop_thread)

            def get_pos(self):
                return self.pos

            def stop_thread(self,*arg,**kwarg):
                kwarg.setdefault('reason','n/a')
                self.looping = False
                if kwarg['reason'] == 'error': Logger.info('GstStreamTimer: Player crashed.')
                else: Logger.info('GstStreamTimer: Thread was stopped.')
                self.stream = False

            def seek(self,pos,length):
                self.player.seek(int(pos))
                self.startTime = self.curTime - pos

            def start_thread(self):
                self.startTime,self.pos  = time(),0
                while self.looping:
                    if self.player == self.parent.sound and self.player.length != -1:
                        self.curTime = time()
                        self.pos = int(self.curTime - self.startTime)
                        sleep(1)
                    else:
                        if self.player.length == -1: self.stop_thread(reason='error')
                        else: self.stop_thread()

        self.sound = testplayer.SoundGstplayer()
        self.player = 'audio'
        self.sound.source = path
        self.sound.load()
        self.sound.play()
        self.streamTimer = Gst_Stream_Timer(self,self.sound)
        self.sound.bind(on_stop= self.on_stop())
        self.stream = stream
        return name
    elif platform == 'android':
        if self.providers['stream'] == 'Kivy':
            start_android_audio(self,path,'',stream=True)
            return name
        else:
            self.player = 'external'
            android_fileExt_activity("video/*",path)
            return 'External player'

def start_audio_other_gst(self, place):
    ID, (name, path) = self.playlist.get_current()
    if type(path) == unicode:
        path = path.encode('utf-8')
    self.sound = SoundGstplayerModified().load(path)
    if self.sound:
        self.sound.play()
        self.sound.bind(on_stop=self.on_stop)
        return name
