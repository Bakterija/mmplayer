from __future__ import print_function
from .video_player_kivy import AppVideoPlayer
from .audio_player_kivy import AudioPlayer
from kivy.utils import platform
import traceback
if platform == 'android':
    from android_intents import android_fileExt_activity
    from android_player import AndroidPlayer


def start_audio_kivy(self, place):
    ID, (name, path) = self.playlist.get_current()
    if type(path) == unicode:
        path = path.encode('utf-8')
    self.sound = AudioPlayer(path)
    if self.sound:
        self.sound.play()
        self.sound.bind(on_stop=self.on_stop)
        return name

def start_audio_external(self, place):
    ID, (name, path) = self.playlist.get_current()
    if type(path) == unicode:
        path = path.encode('utf-8')
    self.player = 'external'
    android_fileExt_activity("audio/*", path + name)
    return 'External player'

def start_video_kivy(self, place):
    ID, (name, path) = self.playlist.get_current()
    if type(path) == unicode:
        path = path.encode('utf-8')
    self.pauseSupported = True
    self.sound = VideoPlayerModified(
        source=path, state='play', async=False, options={'allow_stretch': True})
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
    self.sound = VideoPlayerModified(
        source=path, state='play', options={'allow_stretch': True})
    return name

def start_android_audio(self, place):
    ID, (name, path) = self.playlist.get_current()
    if type(path) == unicode:
        path = path.encode('utf-8')
    self.player = 'audio'
    self.sound = AndroidPlayer()
    self.sound.load(path)
    self.sound.play()
    self.sound.bind(on_stop= self.on_stop)
    return name

def start_android_video(self, place):
    ID, (name, path) = self.playlist.get_current()
    if type(path) == unicode:
        path = path.encode('utf-8')
    self.player = 'video2'
    self.sound = AndroidPlayer()
    self.sound.load(path)
    self.sound.play()
    self.sound.bind(on_stop= self.on_stop)
    return name
