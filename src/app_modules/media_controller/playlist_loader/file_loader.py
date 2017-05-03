from .base import BasePlaylist


class FileLoaderPlaylist(BasePlaylist):

    def load(self, path, data):
        super(FileLoaderPlaylist, self).load(path, data)
