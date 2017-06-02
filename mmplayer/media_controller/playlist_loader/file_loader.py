from .base import BasePlaylist
from kivy.logger import Logger
from utils import get_unicode
from copy import deepcopy


class FileLoaderPlaylist(BasePlaylist):
    '''Playlist that can add all files from a path and it's sub-paths,
    files can also later be removed.
    Useful when a playlist has to have specific files, folders'''
    can_add = True
    file_modif_time = 0
    adding_files = False

    def load(self, path, data):
        super(FileLoaderPlaylist, self).load(path, data)
        self.media = data['media']
        self.update()

    def update(self):
        pass

    def add_path(self, path):
        path = get_unicode(path)
        new_files = self.get_files(path)
        self.media = self.media + new_files
        self.refresh_media_id()
        self.save()

    def add_path_async(self, path):
        path = get_unicode(path)
        start_index = 0
        if self.media:
            start_index = self.media[-1]['index']
        task = {
            'method': 'playlist_from_path', 'path': path,
            'start_index': start_inde}
        appworker.add_task(task, self.add_path_async_done)
        Logger.info('Playlist-{}: add_path_async: {}'.format(self.name, path))

    def add_path_async_done(self, result):
        Logger.info('Playlist-{}: add_path_async_done:'.format(self.name))
        self.media = self.media + result['playlist']
        self.refresh_media_id()
        self.save()

    def remove_indexes(self, index_list):
        '''Delete self.media items by indexes in index_list argument'''
        for x in reversed(index_list):
            del self.media[x]
        self.refresh_media_id()
        Logger.info('FileLoaderPlaylist: removed %s files' % (len(index_list)))
        self.save()

    def save(self):
        '''Save playlist'''
        save_list = []
        for i, mdict in enumerate(self.media):
            new_dict = {}
            for k, v in mdict.items():
                if k in self.saved_media_keys:
                    new_dict[k] = v
            save_list.append(new_dict)
        self.save_json({
            'name': self.name,
            'playlist_type': 'file_loader',
            'media': save_list
        })

    @staticmethod
    def create(name, path, load_path):
        playlist = FileLoaderPlaylist()
        playlist.load_path = load_path
        playlist.name = name
        playlist.path = path
        playlist.save()
        return playlist
