from .folder_loader import FolderLoaderPlaylist
from .file_loader import FileLoaderPlaylist
from kivy.properties import DictProperty
from kivy.event import EventDispatcher
from kivy.logger import Logger
import global_vars as gvars
from utils import logs
import appworker
from appworker import async_tasks
import json
import os


class PlaylistLoader(EventDispatcher):
    playlists = DictProperty()
    '''All loaded playlist objects in sections'''

    loader_switch = {
        'file_loader': FileLoaderPlaylist,
        'folder_loader': FolderLoaderPlaylist
    }

    def __init__(self, **kwargs):
        self.register_event_type('on_playlists')
        super(PlaylistLoader, self).__init__(**kwargs)

    def on_playlists(self, *args):
        pass

    def get_playlist_by_path(self, path):
        for section, playlist_list in self.playlists.items():
            for pl in playlist_list:
                if pl.path == path:
                    return pl

    def get_playlist_by_name(self, name):
        for section, playlist_list in self.playlists.items():
            for pl in playlist_list:
                if pl.name == name:
                    return pl

    def update_from_directories_async(self, directories):
        Logger.info('playlist_loader: update_from_directories_async')
        ret = async_tasks.find_playlists(directories, self._async_call0)
        appworker.add_task(*ret)

    def _async_call0(self, result):
        files = result['args']
        path_section_list = []
        for section in files:
            for fpath, name in files[section]:
                pl = self.get_playlist_by_path(fpath)
                if pl:
                    pl.update()
                else:
                    path_section_list.append((fpath, section))
        ret = async_tasks.load_playlists(path_section_list, self._async_call1)
        appworker.add_task(*ret)

    def _async_call1(self, result):
        lists = result['args']
        for pld in lists:
            section = pld['section']
            if section not in self.playlists:
                self.playlists[section] = []
            new_pl = self.loader_switch[pld['playlist_type']]()
            for attr, value in pld.items():
                setattr(new_pl, attr, value)
            self.playlists[section].append(new_pl)
            
        self.dispatch('on_playlists', self.playlists)

    def update_from_directories(self, directories):
        Logger.info('playlist_loader: update_from_directories')
        '''Load new playlists from directories, call playlist update() when
        playlist is already in global playlists, then return playlist dict'''
        playlists = self.playlists
        for directory in directories:
            dir_list = os.listdir(directory)

            for section in dir_list:
                if not section in playlists:
                    playlists[section] = []
                file_list = os.listdir('{}{}/'.format(directory, section))

                for f in file_list:
                    found = False
                    fpath = '{}{}/{}'.format(directory, section, f)
                    for k, v in playlists.items():
                        for pl in v:
                            if fpath == pl.path:
                                pl.update()
                                found = True
                                break
                            if found:
                                break

                    if not found:
                        pl = self.load_playlist(
                            '{}{}/{}'.format(directory, section, f), section)
                        if pl:
                            playlists[section].append(pl)

        # Removes playlists which have been deleted
        remlist = []
        for k, v in playlists.items():
            for pl in v:
                if not os.path.exists(pl.path):
                    remlist.append((section, pl))
        for section, pl in remlist:
            playlists[section].remove(pl)
        return playlists

    def load_playlist(self, path, section):
        '''Load new playlist object from path and return it'''
        playlist = None
        try:
            with open(path) as data_file:
                data = json.load(data_file)

            if data['playlist_type'] == 'folder_loader':
                playlist = FolderLoaderPlaylist()
            elif data['playlist_type'] == 'file_loader':
                playlist = FileLoaderPlaylist()

            playlist.load(path, data)
            playlist.section = section
        except:
            logs.error('playlist_loader: failed to load playlist \n', trace=True)

        return playlist

    def create_playlist(self, name):
        '''Create new FileLoaderPlaylist with arg[0] name at default path'''
        category = 'playlists'
        load_path = ''
        path = '{}{}/{}.json'.format(gvars.DIR_PLAYLISTS, category, name)
        if os.path.exists(path):
            logs.error(
                'create_playlist: Playlist "{}" already exists, skipping'.format(
                    name))
        else:
            playlist = FileLoaderPlaylist.create(name, path, load_path)

loader = PlaylistLoader()
