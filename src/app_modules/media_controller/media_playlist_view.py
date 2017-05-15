from .media_view_base import MediaButton
from .media_view_base import MediaRecycleviewBase
from kivy.logger import Logger


class PlaylistViewClass(MediaButton):
    queue_view = False

    def start_media(self, *args):
        if self.mtype == 'media':
            self.rv.mcontrol.start_playlist(
                self.name, self.path, self.index, self.id, self)
        elif self.mtype == 'folder':
            self.rv.mcontrol.open_playlist(self.dictio)


class MediaPlaylistView(MediaRecycleviewBase):
    def __init__(self, **kwargs):
        super(MediaPlaylistView, self).__init__(**kwargs)
        self.viewclass = 'PlaylistViewClass'

    def set_viewed_playlist(self, mcontrol, new_playlist):
        self.playlist_instance = new_playlist
        self.set_data(new_playlist.media)

    def update_data(self):
        self.set_data(self.playlist_instance.media)
