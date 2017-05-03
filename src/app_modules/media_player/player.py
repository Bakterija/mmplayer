from __future__ import print_function
from kivy.clock import Clock
from kivy.logger import Logger
from time import sleep
from .providers import provider_list as providers
from .providers.error_player import ErrorPlayer
import traceback


class MediaPlayer(object):
    cur_index = -1
    player = None
    queue = []
    video = None
    volume = 1.0
    pos = -1
    length = -1

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
        self.stop()
        self.queue = []

    def set_gui_update_callback(self, callback):
        self.gui_update = callback

    def set_volume(self, value):
        self.volume = float(value) / 100
        if self.player:
            self.player.volume = self.volume

    def do_gui_update(self, *args):
        if self.gui_update:
            self.gui_update(**self.get_state_all())

    def start(self, index, seek=0.0):
        self.on_start(index)
        index = int(index)
        if self.player:
            try:
                self.player.unload()
            except Exception as e:
                print (e)
        try:
            self.cur_index = index
            self.cur_media = self.queue[index]
            self.starting = True

            for x in providers:
                player = x.try_loading(self, self.cur_media['path'])
                if player:
                    self.player = player
                    self.player.load(self.cur_media['path'])
                    self.player.volume = self.volume
                    self.play()

                    if seek:
                        self.seek(seek)

                    if self.gui_update:
                        # self.gui_update(**self.get_state_all())

                        if player.is_video:
                            for x in self.callbacks['on_video']:
                                x(self.player)
                    self.starting = False
                    return True

        except Exception as e:
            traceback.print_exc()
            return
        self.starting = False

        self.player = ErrorPlayer()
        self.cur_media = {'name': name, 'path': path}
        if self.gui_update:
            self.gui_update(**self.get_state_all())
        for x in self.callbacks['on_error']:
            x('MediaPlayer: Could not play file {}'.format(name))
        return False

    def on_stop(self,*arg):
        if not self.starting:
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
            new_media = self.queue[new_index]
            self.start(new_index)
            self.on_next()
        else:
            self.on_error('Done playing')

    def previous(self, *arg):
        if not self.queue:
            return self.on_error('Empty playlist')

        if self.cur_index > 0:
            new_index -= 1
            new_media = self.queue[new_index]
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
            'length': self.get_mediaDur(), 'name': self.cur_media['name'],
            'path': self.cur_media['path']}

    # def get_pos(self):
    #     '''Unused currently'''
    #     if self.player != None and self.player != 'external':
    #         seconds = self.get_mediaPos()
    #         soundlen = self.get_mediaDur()
    #         intseconds = int(seconds)
    #         m, s = divmod(intseconds, 60)
    #         m2, s2 = divmod(int(soundlen), 60)
    #         s = str(m).zfill(2)+':'+str(s).zfill(2)+'/'+str(m2).zfill(2)+':'+str(s2).zfill(2)
    #         return s, seconds, soundlen

    def on_start(self, index):
        for x in self.callbacks['on_start']:
            x()
        print("ONSTART", index)

    def on_next(self):
        for x in self.callbacks['on_next']:
            x()

    def on_previous(self):
        for x in self.callbacks['on_previous']:
            x()

    def on_error(self, reason):
        for x in self.callbacks['on_error']:
            x(reason)

    def bind(self, **kwargs):
        for k, v in kwargs.items():
            self.callbacks[k].append(v)

    def unbind(self, **kwargs):
        for k, v in kwargs.items():
            self.callbacks[k].remove(v)

mplayer = MediaPlayer()
