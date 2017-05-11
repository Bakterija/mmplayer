from .file_loader import FileLoaderPlaylist
from .folder_loader import FolderLoaderPlaylist
from kivy.logger import Logger
from os import listdir
import global_vars as gvars
import json
import traceback

loaded_paths = set()

def load_from_directories(directories):
    playlists = {}

    for directory in directories:
        dir_list = listdir(directory)

        for section in dir_list:
            if not section in playlists:
                playlists[section] = []
            file_list = listdir('{}{}/'.format(directory, section))

            for f in file_list:
                pl = load_playlist(
                    '{}{}/{}'.format(directory, section, f), section)
                if pl:
                    playlists[section].append(pl)
    return playlists

def load_playlist(path, section):
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
        Logger.error('playlist_loader: failed to load playlist: %s' % (
            traceback.format_exc()))

    return playlist

def create_playlist(name):
    category = 'playlists'
    load_path = ''
    path = '{}{}/{}.json'.format(gvars.DIR_PLAYLISTS, category, name)
    playlist = FileLoaderPlaylist.create(name, path, load_path)
