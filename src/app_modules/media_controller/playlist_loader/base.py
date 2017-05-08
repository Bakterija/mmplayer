from kivy.event import EventDispatcher
from kivy.properties import StringProperty, ListProperty
from kivy.compat import PY2
from kivy.logger import Logger
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
        if os.path.isfile(path):
            return [self.get_default_media_dict(path)]

        for dirname, dirnames, filenames in os.walk(path):
            for file_name in filenames:
                file_path = os.path.join(dirname, file_name)
                templist.append(
                    self.get_default_media_dict(file_path))
        # if sort == 'abc':
        #     templist
        return templist

    def get_default_media_dict(self, file_path):
        file_name = os.path.basename(file_path)
        _fp, file_ext = os.path.splitext(file_path)
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
