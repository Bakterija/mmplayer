from .file_loader import FileLoaderPlaylist
from .folder_loader import FolderLoaderPlaylist
from kivy.logger import Logger
import global_vars as gvars
import traceback
import json
import os

playlists = {}

def load_from_directories(directories):
    global playlists

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
                    pl = load_playlist(
                        '{}{}/{}'.format(directory, section, f), section)
                    if pl:
                        playlists[section].append(pl)

    remlist = []
    for k, v in playlists.items():
        for pl in v:
            if not os.path.exists(pl.path):
                remlist.append((section, pl))
    for section, pl in remlist:
        playlists[section].remove(pl)
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
