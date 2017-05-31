from __future__ import print_function
from kivy.clock import Clock
from kivy.logger import Logger
from time import sleep
from .providers import provider_list as providers
from .providers.error_player import ErrorPlayer
from kivy.event import EventDispatcher
import traceback


class MediaPlayer(object):
    cur_index = -1
    player = None
    queue = []
    is_video = False
    video_widget = None
    volume = 1.0
    volume_real = 1.0
    pos = -1
    length = -1
    cur_media = {'name': '', 'path': ''}

    def __init__(self):
        self.callbacks = {
            'next_on_stop': True,
            'loop': '',
            'on_video': [],
            'on_start': [],
            'on_next': [],
            'on_previous': [],
            'on_pause': [],
            'on_play': [],
            'on_error': []
        }

    def reset(self):
        self.unload()
        self.queue = []

    def unload(self):
        if self.player:
            try:
                self.player.unload()
            except Exception as e:
                print (e)

    def set_volume(self, value):
        self.volume = float(value) / 100
        self.volume_real = (float(value) * float(value)) / 10000
        if self.player:
            self.player.volume = self.volume_real

    def start(self, index, seek=0.0):
        self.starting = True
        index = int(index)
        self.unload()
        try:
            self.cur_index = index
            self.cur_media = self.queue[index]

            for x in providers:
                player = x.try_loading(self, self.cur_media['path'])
                if player:
                    self.player = player
                    self.player.load(self.cur_media['path'])
                    self.player.volume = self.volume_real
                    self.play()

                    if seek:
                        self.seek(seek)

                    self.on_start(index)
                    self.starting = False
                    return True

        except Exception as e:
            traceback.print_exc()
            return
        self.starting = False
        # self.player = ErrorPlayer()

    def on_stop(self,*arg):
        if not self.starting:
            Logger.info('%s: %s' % (self.__class__.__name__, 'on_stop'))
            if self.callbacks['next_on_stop']:
                self.next()

    def play(self, *arg):
        if self.player:
            self.player.play()
            for x in self.callbacks['on_play']:
                x(self, self.get_mediaPos())

    def next(self, *arg):
        if not self.queue:
            return self.on_error('Empty playlist')

        new_index = self.cur_index + 1
        if new_index < len(self.queue):
            self.start(new_index)
            self.on_next()
        else:
            self.on_error('Done playing')

    def previous(self, *arg):
        if not self.queue:
            return self.on_error('Empty playlist')

        new_index = self.cur_index - 1
        if new_index != -1:
            self.start(new_index)
            self.on_previous()

    def seek(self, value):
        if self.player:
            if value < 0.0:
                value = 0.0
            elif value > self.get_mediaDur():
                value = self.get_mediaDur() - 0.2
            self.player.seek(value)

    def seek_relative(self, value):
        value = self.get_mediaPos() + value
        self.seek(value)

    def stop(self, *arg):
        if self.player:
            self.player.stop()
            self.player.unload()

    def pause(self, *arg):
        if self.player:
            self.player.pause()
            for x in self.callbacks['on_pause']:
                x(self, self.get_mediaPos())

    def get_mediaPos(self, *arg):
        if self.player:
            return self.player.get_pos()
        return -1

    def get_mediaDur(self, *arg):
        if self.player:
            return self.player.length
        return -1

    def get_state(self):
        if self.player:
            return self.player.state
        return 'stop'

    def get_state_all(self):
        is_video = False
        if self.player:
            is_video = self.player.is_video
        return {
            'is_video': is_video, 'state': self.get_state(),
            'volume': self.volume, 'pos': self.get_mediaPos(),
            'cur_index': self.cur_index, 'length': self.get_mediaDur(),
            'cur_media': self.cur_media}

    def on_start(self, index):
        Logger.info('%s: %s(%s)' % (
            self.__class__.__name__, 'on_start', index))
        for x in self.callbacks['on_start']:
            x()

    def on_next(self):
        Logger.info('%s: %s' % (self.__class__.__name__, 'on_next'))
        for x in self.callbacks['on_next']:
            x()

    def on_previous(self):
        Logger.info('%s: %s' % (self.__class__.__name__, 'on_previous'))
        for x in self.callbacks['on_previous']:
            x()

    def on_error(self, reason):
        Logger.info('%s: %s' % (self.__class__.__name__, 'on_error'))
        for x in self.callbacks['on_error']:
            x(reason)

    def on_video(self, value):
        self.is_video = value
        if value:
            self.video_widget = self.player
        else:
            self.video_widget = None
        for x in self.callbacks['on_video']:
            x(value, player=self.player)


    def bind(self, **kwargs):
        for k, v in kwargs.items():
            self.callbacks[k].append(v)

    def unbind(self, **kwargs):
        for k, v in kwargs.items():
            self.callbacks[k].remove(v)

mplayer = MediaPlayer()