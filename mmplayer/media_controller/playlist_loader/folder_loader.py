from kivy.properties import StringProperty
from .base import BasePlaylist
from kivy.logger import Logger

class FolderLoaderPlaylist(BasePlaylist):
    '''Playlist that doesn't save files,
    instead it displays all files that that are in it's target path.
    Useful for adding folders that will be changing often'''

    load_path = StringProperty()
    '''StringProperty path where the playlist will be looking for files'''

    can_add = False
    '''Files can not be added to this playlist,
    it only displays what was found in it's load path'''

    can_remove = False
    '''Files can not be removed from this playlist,
    it only displays what was found in it's load path'''

    def load(self, path, data):
        super(FolderLoaderPlaylist, self).load(path, data)
        self.load_path = self.strreplace(data['path'])
        self.update()

    def update(self):
        '''Find files in self.load_path and refresh self.media'''
        folder_files = self.get_files(self.load_path)
        for i, x in enumerate(folder_files):
            folder_files[i]['index'] = i
        self.media = folder_files
        self.refresh_media_id()

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
