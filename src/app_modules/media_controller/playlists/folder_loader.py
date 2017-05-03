from .base import BasePlaylist


class FolderLoaderPlaylist(BasePlaylist):
    load_path = ''

    def load(self, path, data):
        super(FolderLoaderPlaylist, self).load(path, data)
        self.load_path = self.strreplace(data['path'])
        self.update()

    def update(self):
        folder_files = self.get_files(self.load_path)
        self.media = folder_files
