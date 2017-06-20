from kivy.properties import StringProperty, ListProperty, DictProperty
from kivy.event import EventDispatcher
from kivy.logger import Logger
from utils import get_unicode
from kivy.compat import PY2
from utils import logs
from time import time
import json
import os

HOME_DIR = os.path.expanduser("~")+'/'
next_id = 0


class BasePlaylist(EventDispatcher):
    '''Base class of application playlists'''

    id = None
    '''id number of playlist, default is 0'''

    name = StringProperty()
    '''Name of playlist'''

    path = StringProperty()
    '''Path where playlist .json file is saved'''

    playlist_type = StringProperty()
    '''StringProperty class name of loaded playlist'''

    media_paths = DictProperty()
    '''DictProperty with media path keys and media list index number values
    for fast path searching'''

    media = ListProperty()
    '''ListProperty of all media file dictionaries,
    stories names, paths, exts and maybe also media info like
    duration, artist, title (if ffprobe is available and file has been probed)
    '''

    cur_playing = -1
    can_add = True
    '''True when files can be added to playlist'''

    can_remove = True
    '''True when files can be removed from playlist'''

    allowed_extensions = {
        '.flac', '.midi', '.webm', '.vob', '.ogv', '.mp3', '.ogg',
        '.m4a', '.mp4', '.mkv', '.mdl', '.mpg', '.mp2', '.mpeg',
        '.mpe', '.mpv', '.avi', '.flv', '.wav', '.mid', '.mv2', '.m4v'
        }
    saved_media_keys = {
        'ext', 'name', 'path', 'duration'
        }

    def __init__(self, **kwargs):
        global next_id
        super(BasePlaylist, self).__init__(**kwargs)
        self.id = next_id
        next_id += 1
        self.bind(media=self.refresh_media_id)

    # def set_playing(self, index):
    #     self.remove_playing()
    #     self.cur_playing = index
    #     self.media[index]['state'] = 'playing'

    # def remove_playing(self):
    #     if self.cur_playing != -1:
    #         self.media[self.cur_playing]['state'] = 'normal'
    #         self.cur_playing = -1

    def update(self):
        pass

    def load(self, path, data):
        '''Load playlist from file'''
        self.path = path
        self.name = data['name']
        self.playlist_type = data['playlist_type']
        for x in iter(self.media):
            x['playlist_name'] = self.name

    def add_path(self, path):
        '''Add file path to playlist'''
        Logger.error('{}: add_path: can not add to this playlist'.format(
            self.name))

    def add_path_async(self, path):
        Logger.error('{}: add_path: can not add to this playlist'.format(
            self.name))

    @staticmethod
    def create():
        '''Create playlist file'''
        Logger.error('{} has an empty create method'.format(self))

    def save_json(self, playlist_dict):
        try:
            with open(self.path, 'w') as outfile:
                json.dump(
                    playlist_dict, outfile, indent=4,
                    sort_keys=True, separators=(',', ':'))
        except:
            logs.error('Playlist: failed to save "%s"\n' % self.name, trace=True)

    def remove(self):
        '''Delete playlist'''
        os.remove(self.path)

    def save(self):
        '''Save playlist file'''
        Logger.error('{} has an empty save method'.format(self))

    @staticmethod
    def get_folders(path, sort='abc'):
        '''Get all folders and subfolders from path argument'''
        templist = []
        for dirname, dirnames, filenames in os.walk(path):
            for subdirname in dirnames:
                dirpath = os.path.join(dirname, subdirname)
                templist.append([subdirname, dirpath])
        if sort == 'abc':
            templist.sort()
        return templist

    def get_files(self, path, sort='abc'):
        '''Get all files from path argument'''
        templist = []
        time0 = time()
        if os.path.isfile(path):
            media_dict = self.get_default_media_dict(path)
            if media_dict:
                templist = [media_dict]
        else:
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
        '''Returns a media dict with unicode values,
        if file extension is in self.allowed_extensions,
        otherwise returns nothing'''
        file_name = os.path.basename(file_path)
        _fp, file_ext = os.path.splitext(file_path)
        if file_ext not in self.allowed_extensions:
            return None
        return {
            'name': get_unicode(file_name),
            'ext': get_unicode(file_ext),
            'path': get_unicode(file_path),
            'state': 'normal',
            'playlist_name': self.name}

    def refresh_media_id(self, *args):
        '''Updates id numbers for all files in self.media ListProperty'''
        mp = {}
        for i, x in enumerate(self.media):
            x['id'] = i
            mpath = x['path']
            if mpath in mp:
                mp[x['path']].append(i)
            else:
                mp[x['path']] = [i]
            x['playlist_name'] = self.name
            if not 'state' in x:
                x['state'] = 'normal'
        self.media_paths = mp

    @staticmethod
    def strreplace(string):
        replacables = [('%USER-HOME%/', HOME_DIR)]

        for start, end in replacables:
            string = string.replace(start, end)
        return string
