from .file_loader import FileLoaderPlaylist
from .folder_loader import FolderLoaderPlaylist
from os import listdir
import json


def load_from_directory(directory):
    playlists = {}
    dir_list = listdir(directory)

    for category in dir_list:
        playlists[category] = []
        file_list = listdir('{}{}/'.format(directory, category))

        for f in file_list:
            playlists[category].append(
                load_playlist('{}{}/{}'.format(directory, category, f)))
    return playlists

def load_playlist(path):
    with open(path) as data_file:
        data = json.load(data_file)

    if data['playlist_type'] == 'folder_loader':
        playlist = FolderLoaderPlaylist()
    elif data['playlist_type'] == 'file_loader':
        playlist = FileLoaderPlaylist()

    playlist.load(path, data)
    return playlist
