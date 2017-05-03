from kivy.event import EventDispatcher
from kivy.properties import StringProperty, ListProperty
from kivy.compat import PY2
import os

HOME_DIR = os.path.expanduser("~")+'/'


class BasePlaylist(EventDispatcher):
    name = StringProperty()
    path = StringProperty()
    playlist_type = StringProperty()
    media = ListProperty()

    def update(self):
        pass

    def load(self, path, data):
        self.path = path
        self.name = data['name']
        self.playlist_type = data['playlist_type']

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
        for dirname, dirnames, filenames in os.walk(path):
            for filename in filenames:
                file_path = os.path.join(dirname, filename)
                file_name, file_ext = os.path.splitext(file_path)
                templist.append((
                    self.py2decode(file_name),
                    self.py2decode(file_ext),
                    self.py2decode(file_path)
                    ))
        if sort == 'abc':
            templist.sort()
        return templist

    def py2decode(self, string):
        if PY2:
            string = string.decode('utf-8')
        return string

    @staticmethod
    def strreplace(string):
        replacables = [('%USER-HOME%/', HOME_DIR)]

        for start, end in replacables:
            string = string.replace(start, end)
        return string
