from .base import BasePlaylist


class FolderLoaderPlaylist(BasePlaylist):
    load_path = ''

    def load(self, path, data):
        super(FolderLoaderPlaylist, self).load(path, data)
        self.load_path = self.strreplace(data['path'])
        self.update()

    def update(self):
        folder_files = self.get_files(self.load_path)
        for i, x in enumerate(folder_files):
            folder_files[i]['index'] = i
        self.media = folder_files

    @staticmethod
    def create(name, path, load_path):
        playlist = FolderLoaderPlaylist()
        playlist.load_path = load_path
        playlist.name = name
        playlist.path = path
        playlist.save_json({
            'name': name,
            'path': load_path,
            'playlist_type': 'folder_loader'
        })
        return playlist
