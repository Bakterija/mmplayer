from .base import BasePlaylist
from kivy.logger import Logger


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
