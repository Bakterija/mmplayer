from __future__ import print_function
from media_player import Media_Player
from kivy.utils import platform
from time import sleep
import traceback
import default_providers


class Media_Player_Server(Media_Player):
    def __init__(self):
        super(Media_Player_Server, self).__init__()
        self.osc_sender = None
        self.server_active = True
        self.mstring = 'audioSV:'
        self.modes['on_start'].append(self.update_playlist_current)
        self.modes['on_video'].append(self.gui_video_start)
        if platform == 'android':
            self.add_provider('audio',['android', default_providers.start_android_audio])
            self.add_provider('video',['android', default_providers.start_android_video])
            self.providers_active = {'video':'android','audio':'android','stream':'Kivy'}

    def set_osc_sender(self,value):
        self.osc_sender = value
        self.sender_enabled = True

    def enable_sender(self):
        self.sender_enabled = True
        if self.playlist.list != []:
            self.update_playlist_current()
        try:
            if self.sound:
                if self.player in ('video', 'video2'):
                    if self.sound.state == 'play':
                        self.gui_video_start()
        except Exception as e:
            traceback.print_exc()

    def disable_sender(self):
        self.sender_enabled = False
        self.modes['next_on_stop'] = True

    def osc_callback(self,message):
        try:
            msg = message.split(':')
            if msg[0] == 'Load':
                self.start(msg[1])
            elif msg[0] == 'Play':
                self.modes['next_on_stop'] = True
                self.play()
            elif msg[0] == 'Pause':
                self.pause()
            elif msg[0] == 'Stop':
                self.modes['next_on_stop'] = False
                try:
                    self.sound.stop()
                except AttributeError:
                    pass
            elif msg[0] == 'Unload':
                self.stop()
            elif msg[0] == 'Next':
                self.next()
            elif msg[0] == 'Previous':
                self.previous
            elif msg[0] == 'addPlaylist':
                self.playlist.add(msg[1], msg[2])
            elif msg[0] == 'insertPlaylist':
                self.playlist.insert(int(msg[1]), msg[2], msg[3])
            elif msg[0] == 'resetPlaylist':
                self.playlist.reset()
            elif msg[0] == 'Seek':
                self.seek(msg[1])
                sleep(1)
            elif msg[0] == 'background_switch':
                self.start(msg[1],seek=msg[4])
        except Exception as e:
            traceback.print_exc()

    def update(self,cl_connected):
        try:
            if self.paused == False:
                string = self.mstring+'return_pos:'+self.return_pos2()
                if self.sender_enabled:
                    self.osc_sender(string)
        except Exception as e:
            traceback.print_exc()
            self.server_active = False

    def gui_video_start(self,*arg):
        try:
            if self.sender_enabled:
                ID, (name, path) =  self.playlist.get_current()
                seektime = self.return_pos()[1][0]
                string = self.mstring+'start_video:'+'%s:%s:%s:%s' % (ID, name, path, seektime)
                self.osc_sender(string)
                self.osc_sender(string)
                self.stop()
        except Exception as e:
            traceback.print_exc()

    def update_playlist_current(self,*arg):
        ID, (name, path) =  self.playlist.get_current()
        string = self.mstring+'update_media:'+'%s:%s:%s' % (ID, name, path)
        self.osc_sender(string)

    def return_pos2(self):
        if self.seeking:
            seconds = -9
            soundlen = self.get_mediaDur()
            s = str(-9).zfill(2)+'-'+str(-9).zfill(2)+'/'+str(-9).zfill(2)+'-'+str(-9).zfill(2)
            return '%s:%s:%s' % (s,seconds,soundlen)
        else:
            if self.sound and self.player != 'external':
                seconds = self.get_mediaPos()
                soundlen = self.get_mediaDur()
                intseconds = int(seconds)
                m, s = divmod(intseconds, 60)
                m2, s2 = divmod(int(soundlen), 60)
                s = str(m).zfill(2)+'-'+str(s).zfill(2)+'/'+str(m2).zfill(2)+'-'+str(s2).zfill(2)
                return '%s:%s:%s' % (s,seconds,soundlen)
