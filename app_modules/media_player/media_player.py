from __future__ import print_function
from kivy.clock import Clock
from kivy.logger import Logger
from time import sleep
from providers import provider_list as providers
from providers.error_player import ErrorPlayer
from kivy.utils import platform
import traceback


class Playlist(object):
    def __init__(self,*args,**kwargs):
        self.list = []
        self.current = 0

    def get_next(self):
        self.current +=1
        if self.list:
            try:
                name = self.list[self.current]['name']
                path = self.list[self.current]['path']
                return self.current, name, path
            except:
                return None, None, None

    def get_previous(self):
        self.current -= 1
        if self.list:
            try:
                name = self.list[self.current]['name']
                path = self.list[self.current]['path']
                return self.current, name, path
            except:
                return None, None, None

    def get_current(self):
        if self.list:
            name = self.list[self.current]['name']
            path = self.list[self.current]['path']
            return self.current, name, path
        else:
            return None, None, None

    def set_current(self,value):
        self.current = int(value)

    def add(self, name, path, **kwargs):
        appending = {'name': name, 'path': path}
        for key, value in kwargs.iteritems():
            self.appending['key'] = value
        self.list.append(appending)

    def insert(self, index, name, path, **kwargs):
        appending = {'name': name, 'path': path}
        for key, value in kwargs.iteritems():
            self.appending['key'] = value
        self.list.insert(index, appending)

    def reset(self):
        self.current = 0
        self.list = []


class Media_Player(object):
    '''The audio/video player class of the application.
    Does not use any kivy GUI widgets on purpose, to make it possible to
    us it inside another GUI, in a terminal or as a service'''

    sound = None
    playlist = Playlist()
    cur_media = {'name': '', 'path': ''}
    player = 'audio'
    gui_update = None
    starting = False
    volume = 1.0

    def __init__(self):
        self.modes = {
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

    def set_gui_update_callback(self, callback):
        self.gui_update = callback

    def set_modes(self,dictio):
        self.modes.update(dictio)

    def set_volume(self, value):
        self.volume = float(value) / 100
        if self.sound:
            self.sound.volume = self.volume

    def do_gui_update(self, *args):
        if self.gui_update:
            self.gui_update(**self.get_state_all())

    def start(self, place, seek=0.0):
        if self.sound:
            try:
                self.sound.unload()
            except Exception as e:
                print (e)
        try:
            place = int(place)
            self.playlist.set_current(place)
            index, name, path = self.playlist.get_current()
            self.starting = True


            for x in providers:
                player = x.try_loading(self, path)
                if player:
                    self.sound = player
                    self.sound.load(path)
                    self.sound.volume = self.volume
                    self.sound.play()
                    self.cur_media = {'name': name, 'path': path}

                    if seek:
                        self.seek(seek)

                    if self.gui_update:
                        self.gui_update(**self.get_state_all())
                        for x in self.modes['on_start']:
                            x()

                        if player.is_video:
                            for x in self.modes['on_video']:
                                x(self.sound)
                    self.starting = False
                    return True

        except Exception as e:
            traceback.print_exc()
        self.starting = False

        self.sound = ErrorPlayer()
        self.cur_media = {'name': name, 'path': path}
        if self.gui_update:
            self.gui_update(**self.get_state_all())
        for x in self.modes['on_error']:
            x('MediaPlayer: Could not play file {}'.format(name))
        return False

    def on_stop(self,*arg):
        if not self.starting:
            if self.modes['next_on_stop']:
                self.next()

    def play(self, *arg):
        if self.sound:
            self.sound.play()
            for x in self.modes['on_play']:
                x(self, self.get_mediaPos())

    def next(self, *arg):
        index, name, path = self.playlist.get_next()
        if index:
            self.start(str(index))
            for x in self.modes['on_next']:
                x()
        else:
            if self.playlist.list:
                if self.modes['loop'] == 'playlist':
                    self.playlist.current = 0
                    self.start('0')
                else:
                    for x in self.modes['on_error']:
                        x('Done playing')
            else:
                for x in self.modes['on_error']:
                    x('Playlist is empty')

    def previous(self, *arg):
        index, name, path = self.playlist.get_previous()
        if index:
            name = self.start(str(index))
            for x in self.modes['on_previous']:
                x()
        else:
            for x in self.modes['on_error']:
                x('Playlist is empty')

    def seek(self, value):
        if self.sound:
            if value < 0.0:
                value = 0.0
            elif value > self.get_mediaDur():
                value = self.get_mediaDur() - 0.2
            self.sound.seek(value)

    def seek_relative(self, value):
        value = self.get_mediaPos() + value
        self.seek(value)

    def stop(self, *arg):
        if self.sound:
            self.sound.stop()
            self.sound.unload()

    def pause(self, *arg):
        if self.sound:
            self.sound.pause()
            for x in self.modes['on_pause']:
                x(self, self.get_mediaPos())

    def get_mediaPos(self, *arg):
        if self.sound:
            return self.sound.get_pos()
        return -1

    def get_mediaDur(self, *arg):
        if self.sound:
            return self.sound.length
        return -1

    def get_state(self):
        if self.sound:
            return self.sound.state
        return 'stop'

    def get_state_all(self):
        is_video = False
        if self.sound:
            is_video = self.sound.is_video
        return {
            'is_video': is_video, 'state': self.get_state(),
            'volume': self.volume, 'pos': self.get_mediaPos(),
            'length': self.get_mediaDur(), 'name': self.cur_media['name'],
            'path': self.cur_media['path']}

    def get_pos(self):
        '''Unused currently'''
        if self.sound != None and self.player != 'external':
            seconds = self.get_mediaPos()
            soundlen = self.get_mediaDur()
            intseconds = int(seconds)
            m, s = divmod(intseconds, 60)
            m2, s2 = divmod(int(soundlen), 60)
            s = str(m).zfill(2)+':'+str(s).zfill(2)+'/'+str(m2).zfill(2)+':'+str(s2).zfill(2)
            return s, seconds, soundlen
