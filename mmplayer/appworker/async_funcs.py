from media_controller import playlist_loader
from media_controller.playlist_loader import FileLoaderPlaylist
from media_controller.playlist_loader import FolderLoaderPlaylist
import json
import os

def do_find_playlists(directories, **kwargs):
    new = {}
    for directory in directories:
        dir_list = os.listdir(directory)

        for section in dir_list:
            new[section] = []
            files = os.listdir('{}{}/'.format(directory, section))
            for f in files:
                fpath = '%s%s/%s' % (directory, section, f)
                new[section].append((fpath, f))
    return (new), {}

def do_load_playlists(path_section_list, *args):
    new_playlists = []
    for path, section in path_section_list:
        pl = playlist_loader.loader.load_playlist(path, section)
        pl_dict = {
            'section': str(pl.section), 'playlist_type': str(pl.playlist_type),
            'type': str(pl.playlist_type), 'name': str(pl.name),
            'path': str(pl.path), 'media': list(pl.media)
        }
        new_playlists.append(pl_dict)

    return (new_playlists), {}


task_switch = {
    'do_find_playlists': do_find_playlists,
    'do_load_playlists': do_load_playlists
}
