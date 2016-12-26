from __future__ import print_function
from kivy.clock import Clock
from kivy.logger import Logger
from time import sleep
import default_providers
import traceback
from kivy.utils import platform

class Playlist(object):
    def __init__(self,*args,**kwargs):
        self.list = []
        self.current = 0

    def get_next(self):
        self.current +=1
        if self.list != []:
            try:
                return self.current, self.list[self.current]
            except:
                self.current = 0
                return self.current, self.list[self.current]
        Logger.warning('[Media Player] Playlist is empty')
        return None, (None, None)

    def get_previous(self):
        self.current -= 1
        if self.list != []:
            try:
                return self.current, self.list[self.current]
            except:
                self.current = len(self.list) - 1
                return self.current, self.list[self.current]
        Logger.warning('[Media Player] Playlist is empty')
        return None, (None, None)

    def get_current(self):
        if self.list:
            name = self.list[self.current]['name']
            path = self.list[self.current]['path']
            return self.current, (name, path)
        else:
            return None

    def set_current(self,value):
        self.current = int(value)

    def add(self, name, path, **kwargs):
        # print(name, path)
        appending = {'name': name, 'path': path}
        for key, value in kwargs.iteritems():
            self.appending['key'] = value
        self.list.append(appending)

    def insert(self, index, name, path, **kwargs):
        appending = {'name': name, 'path': path}
        for key, value in kwargs.iteritems():
            self.appending['key'] = value
        self.list.insert(index, appending)
        # print(name, path)

    def reset(self):
        self.current = 0
        self.list = []


class Dummy(object):
    ''' Will be removed later'''
    class Sound(object):
        def __init__(self):
            self.sound, self.state = 'Dummy', 'Dummy'
        def seek(self):
            return 0
        def unload(self):
            pass
    def __init__(self):
        self.state = 'stop'
        self.length, self.source, name_name, self.sound = 0, False, False, self.Sound()
        self.paused = False
    def unload(self,*arg):
        return 'Dummy'
    def play(self,*arg):
        return 'Dummy'
    def stop(self,*arg):
        return 'Dummy'
    def get_pos(self,*arg):
        return 0
    def seek(self,*arg):
        return 'Dummy'


class Media_Player(object):
    '''The audio/video player class of the application.
    Does not use any kivy GUI widgets on purpose, to make it possible to
    us it inside another GUI, in a terminal or as a service'''

    seeking = False
    paused = False
    pauseSupported = False
    sound = False
    state = 'stop'
    gui_update = None
    starting = False
    volume = 1.0
    pauseSeek = 0

    def __init__(self):
        self.playlist = Playlist()
        self.mediaName = ''
        self.sound = Dummy()
        self.player = 'audio'
        self.stream = False
        self.modes = {
            'next_on_stop': True,
            'on_video': [],
            'on_start': [],
            'on_next': [],
            'on_previous': [],
            'on_pause': [],
            'on_resume': [],
            'on_error': []
        }
        self.providers_active = {
            'video':'Kivy',
            'audio':'Kivy',
            'stream':'Kivy'
        }
        self.providers = {
            'video':[
                ['Kivy', default_providers.start_video_kivy],
                ['External', default_providers.start_video_external],
                ['No video', default_providers.start_video_no_video]
            ],
            'audio':[
                ['Kivy', default_providers.start_audio_kivy],
                ['External', default_providers.start_audio_kivy]
            ],
            'stream-audio':[
                ['Kivy', default_providers.start_stream_kivy],
            ],
            'stream-video':[
                ['Kivy', default_providers.start_stream_kivy],
            ]
        }

    def set_video_provider(self, value):
        self.providers_active['video'] = value

    def set_audio_provider(self, value):
        self.providers_active['audio'] = value

    def set_stream_provider(self, value):
        self.providers_active['stream'] = value

    def set_gui_update_callback(self, callback):
        self.gui_update = callback

    def set_modes(self,dictio):
        self.modes.update(dictio)

    def add_provider(self, mType, provider):
        self.providers[mType].append(provider)

    def set_volume(self, value):
        self.volume = float(value) / 100
        if self.sound:
            self.sound.volume = self.volume

    def start(self, place, seek=0.0):
        try:
            self.trying_seek = False
            place = int(place)
            self.playlist.set_current(place)
            ID, (name, path) = self.playlist.get_current()
            self.starting = True
            self.state = 'stop'
            self.paused = False
            self.pauseSupported = False
            if self.stream:
                self.stream = False
                try:
                    self.streamTimer.stop_thread(reason='Start media')
                except:
                    pass
                self.streamTimer = None
            stream = False
            try:
                self.stop()
            except Exception as e:
                pass
            self.player = ''

            if path[:7] == 'http://' or  path[:8] == 'https://':
                self.player = 'stream-audio'
            if not self.player:
                for x in '.wav','.mp3','.ogg','.m4a':
                   if path[-4:] == x:
                       self.player = 'audio'
                for x in '.mp4','.mkv':
                   if path[-4:] == x:
                       self.player = 'video'

            if not self.player:
                e = '''[MediaPlayer error] Could not detect format of file:
                    {}\n\n{}'''.format(path, name)
                for x in self.modes['on_error']:
                    x(str(e))
                return None

            found = False
            for provider, callback in self.providers[self.player]:
                if self.providers_active[self.player] == provider:
                    found = True
                    self.mediaName = callback(self, place)
                    if self.mediaName:
                        if self.gui_update:
                            kwargs = {'name': name, 'path': path}
                            self.gui_update(**kwargs)
                        for x in self.modes['on_start']:
                            x()
                        if self.player in ('video', 'video2'):
                            for x in self.modes['on_video']:
                                x(self.sound)
                        self.starting = False
                        if seek:
                            self.seek(seek)
                        self.sound.volume = self.volume
                        return self.mediaName
                    found = False
            if not found:
                self.sound = Dummy()
                self.starting = False
                return False
        except Exception as e:
            traceback.print_exc()

    def on_stop(self,*arg):
        if not self.starting:
            if self.paused == False:
                self.pauseSeek = 0
                if self.modes['next_on_stop']:
                    self.next()

    def play(self,*arg):
        try:
            if self.player == 'video':
                self.sound.state = 'play'
            else:
                self.sound.play()
            Clock.schedule_once(self.resume, 0.2)
            self.state = 'play'
        except Exception as e:
            print(e)

    def next(self,*arg):
        ID,(name,path) = self.playlist.get_next()
        if ID:
            self.start(str(ID))
            for x in self.modes['on_next']:
                x()
        else:
            for x in self.modes['on_error']:
                x('playlist is empty')

    def previous(self,*arg):
        ID,(name,path) = self.playlist.get_previous()
        if ID:
            name = self.start(str(ID))
            for x in self.modes['on_previous']:
                x()
        else:
            for x in self.modes['on_error']:
                x('playlist is empty')

    def seek(self, value):
        if value < 0.0:
            value = 0.0
        elif value > self.get_mediaDur():
            value = self.get_mediaDur() - 0.2
        self.seeking = True
        if self.paused:
            self.pauseSeek = float(value)
        else:
            if self.stream and platform == 'linux':
                self.streamTimer.seek(int(value),self.get_mediaDur())
            elif self.player in ('audio', 'video2'):
                self.sound.seek(float(value))
            elif self.player == 'video':
                val = float(value)
                getDur = float(self.get_mediaDur())
                fn = val / getDur
                self.sound.seek(fn)
        self.seeking = False

    def seek_relative(self, value):
        value = self.get_mediaPos() + value
        self.seek(value)

    def resume(self,*arg):
        if self.sound and type(self.sound) != Dummy:
            self.paused = False
            if self.pauseSupported == False:
                try:
                    self.sound.seek(self.pauseSeek)
                except:
                    pass
            self.state = 'play'
            for x in self.modes['on_resume']:
                x(self, self.pauseSeek)

    def stop(self,*arg):
        if self.player in ('audio', 'video2') and self.sound:
            self.sound.stop()
            self.sound.unload()
        elif self.player == 'video' and self.sound:
            self.sound.state = 'stop'
            self.sound.source = ''
        self.state = 'stop'

    def pause(self, *arg):
        if self.sound and type(self.sound) != Dummy:
            self.pauseSeek = self.get_mediaPos()
            self.paused = True
            if self.player in ('audio', 'video2'):
                self.sound.stop()
            elif self.player == 'video':
                self.sound.state = 'pause'
            for x in self.modes['on_pause']:
                x(self, self.pauseSeek)

    def get_mediaPos(self, *arg):
        pos = 0
        if self.paused:
            pos = self.pauseSeek
        if self.seeking:
            pos = -9
        else:
            if self.stream:
                pos = self.streamTimer.get_pos()
            elif self.player in ('audio', 'video2'):
                pos = self.sound.get_pos()
            elif self.player == 'video':
                pos = self.sound.position
        print (pos)
        return pos

    def get_mediaDur(self,*arg):
        dur = 0
        if self.player in ('audio', 'video2'):
            dur = self.sound.length
        elif self.player == 'video':
            dur = self.sound.duration
        return dur

    def return_pos(self):
        if self.sound != None and self.player != 'external':
            seconds = self.get_mediaPos()
            soundlen = self.get_mediaDur()
            intseconds = int(seconds)
            m, s = divmod(intseconds, 60)
            m2, s2 = divmod(int(soundlen), 60)
            s = str(m).zfill(2)+':'+str(s).zfill(2)+'/'+str(m2).zfill(2)+':'+str(s2).zfill(2)
            return s, (seconds, soundlen)
