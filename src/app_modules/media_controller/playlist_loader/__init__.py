from .file_loader import FileLoaderPlaylist
from .folder_loader import FolderLoaderPlaylist
from os import listdir
import json

loaded_paths = set()

def load_from_directory(directory):
    playlists = {}
    dir_list = listdir(directory)

    for section in dir_list:
        playlists[section] = []
        file_list = listdir('{}{}/'.format(directory, section))

        for f in file_list:
            playlists[section].append(
                load_playlist('{}{}/{}'.format(directory, section, f),
                section))
    return playlists

def load_playlist(path, section):
    playlist = None
    with open(path) as data_file:
        data = json.load(data_file)

    if data['playlist_type'] == 'folder_loader':
        playlist = FolderLoaderPlaylist()
    elif data['playlist_type'] == 'file_loader':
        playlist = FileLoaderPlaylist()

    playlist.load(path, data)
    playlist.section = section

    return playlist
