from kivy.event import EventDispatcher
from kivy.properties import StringProperty, ListProperty
from kivy.compat import PY2
from kivy.logger import Logger
from time import time
import os
import json

HOME_DIR = os.path.expanduser("~")+'/'
next_id = 0


class BasePlaylist(EventDispatcher):
    id = None
    name = StringProperty()
    path = StringProperty()
    playlist_type = StringProperty()
    media = ListProperty()
    cur_playing = -1
    can_add = True
    allowed_extensions = {
        '.flac', '.midi', '.webm', '.vob', '.ogv', '.apun', '.mp3', '.ogg',
        '.m4a', '.mp4', '.mkv', '.dmf', '.dsm', '.far', '.j2b', '.mdl',
        '.med', '.mod', '.dbm', '.mpg', '.mp2', '.mpeg', '.mpe', '.mpv'
        '.avi', '.flv', '.wav', '.mid',  '.669', '.abc', '.amf', '.ams',
        '.mv2', '.mt2', '.mtm', '.okt', '.pat', '.psm', '.ptm', '.s3m',
        '.stm', '.m4v', '.ult', '.umx', '.far', '.gdm', '.gt2', '.okt',
        '.f4v', '.f4p', '.f4a', '.f4b', '.stx', '.ult', '.umx', '.uni',
        '.xm', '.it', '.xm'
        }

    def __init__(self, **kwargs):
        global next_id
        super(BasePlaylist, self).__init__(**kwargs)
        self.id = next_id
        next_id += 1

    def set_playing(self, index):
        self.remove_playing()
        self.cur_playing = index
        self.media[index]['state'] = 'playing'

    def remove_playing(self):
        if self.cur_playing != -1:
            self.media[self.cur_playing]['state'] = 'default'
            self.cur_playing = -1

    def update(self):
        pass

    def load(self, path, data):
        self.path = path
        self.name = data['name']
        self.playlist_type = data['playlist_type']

    def add_path(self, path):
        Logger.error('{}: add_path: can not add to this playlist'.format(
            self.name))

    def add_path_async(self, path):
        Logger.error('{}: add_path: can not add to this playlist'.format(
            self.name))

    @staticmethod
    def create():
        pass

    def save_json(self, playlist_dict):
        with open(self.path, 'w') as outfile:
            json.dump(playlist_dict, outfile, indent=4, sort_keys=True, separators=(
                ',', ':'))

    def remove(self):
        os.remove(self.path)

    @staticmethod
    def get_folders(path, sort='abc'):
        templist = []
        for dirname, dirnames, filenames in os.walk(path):
            for subdirname in dirnames:
                dirpath = os.path.join(dirname, subdirname)
                templist.append([subdirname, dirpath])
        if sort == 'abc':
            templist.sort()
        return templist

    def get_files(self, path, sort='abc'):
        templist = []
        time0 = time()
        if os.path.isfile(path):
            return [self.get_default_media_dict(path)]

        for dirname, dirnames, filenames in os.walk(path):
            for file_name in filenames:
                file_path = os.path.join(dirname, file_name)
                new_file = self.get_default_media_dict(file_path)
                if new_file:
                    templist.append(new_file)
        # if sort == 'abc':
        #     templist
        if time() - time0 > 1.0:
            Logger.info('{}-playlist: found {} files in {} seconds'.format(
                self.name, len(templist), time() - time0))
        return templist

    def get_default_media_dict(self, file_path):
        file_name = os.path.basename(file_path)
        _fp, file_ext = os.path.splitext(file_path)
        if file_ext not in self.allowed_extensions:
            return None
        return {
            'name': self.get_unicode(file_name),
            'ext': self.get_unicode(file_ext),
            'path': self.get_unicode(file_path),
            'state': 'default'}

    def get_unicode(self, string):
        if PY2:
            string = string.encode('utf-8')
            string = unicode(string, 'utf-8')
        else:
            if isinstance(string, bytes):
                string = string.decode('utf-8')
        return string

    @staticmethod
    def strreplace(string):
        replacables = [('%USER-HOME%/', HOME_DIR)]

        for start, end in replacables:
            string = string.replace(start, end)
        return string
