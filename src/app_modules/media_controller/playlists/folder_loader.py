from .base import BasePlaylist


class FolderLoaderPlaylist(BasePlaylist):
    load_path = ''

    def load(self, path, data):
        super(FolderLoaderPlaylist, self).load(path, data)
        self.load_path = self.strreplace(data['path'])
        folder_files = self.get_files(self.load_path)

        # print(self.load_path, folder_files)

    def update(self):
        pass
