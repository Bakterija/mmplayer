from .base import BasePlaylist


class FileLoaderPlaylist(BasePlaylist):

    def load(self, path, data):
        super(FileLoaderPlaylist, self).load(path, data)
        self.update()

    def update(self):
        pass

    @staticmethod
    def create(name, path, load_path):
        playlist = FileLoaderPlaylist()
        playlist.load_path = load_path
        playlist.name = name
        playlist.path = path
        playlist.save_json({
            'name': name,
            'playlist_type': 'file_loader'
        })
        return playlist
