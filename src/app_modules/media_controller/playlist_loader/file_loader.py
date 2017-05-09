from .base import BasePlaylist
from kivy.logger import Logger
from app_modules import appworker


class FileLoaderPlaylist(BasePlaylist):
    can_add = True
    file_modif_time = 0
    adding_files = False

    def load(self, path, data):
        super(FileLoaderPlaylist, self).load(path, data)
        self.media = data['media']
        self.update()

    def update(self):
        pass
        # folder_files = self.get_files(self.load_path)
        # for i, x in enumerate(folder_files):
        #     folder_files[i]['index'] = i
        # self.media = folder_files

    def add_path(self, path):
        path = self.get_unicode(path)
        for new_file in self.get_files(path):
            new_file['index'] = len(self.media)
            self.media.append(new_file)
        self.save()

    def add_path_async(self, path):
        path = self.get_unicode(path)
        start_index = 0
        if self.media:
            start_index = self.media[-1]['index']
        task = {
            'method': 'playlist_from_path', 'path': path,
            'start_index': start_index}
        appworker.add_task(task, self.add_path_async_done)
        Logger.info('Playlist-{}: add_path_async: {}'.format(self.name, path))

    def add_path_async_done(self, result):
        Logger.info('Playlist-{}: add_path_async_done:'.format(self.name))
        self.media = self.media + result['playlist']
        self.save()

    def save(self):
        self.save_json({
            'name': self.name,
            'playlist_type': 'file_loader',
            'media': self.media
        })

    @staticmethod
    def create(name, path, load_path):
        playlist = FileLoaderPlaylist()
        playlist.load_path = load_path
        playlist.name = name
        playlist.path = path
        playlist.save()
        return playlist
