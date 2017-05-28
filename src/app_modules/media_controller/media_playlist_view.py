from .media_view_base import MediaButton
from .media_view_base import MediaRecycleviewBase
from kivy.logger import Logger
from utils.not_implemented import show_error as show_not_implemented
from kivy.clock import Clock, mainthread
from .dialog_properties import MediaPropertiesDialog
from random import randrange


class PlaylistViewClass(MediaButton):
    queue_view = False

    def __init__(self, **kwargs):
        super(PlaylistViewClass, self).__init__(**kwargs)

    def start_media(self, *args):
        if self.mtype == 'media':
            self.rv.mcontrol.start_playlist_from_index(
                self.name, self.path, self.index, self.id, self)
        elif self.mtype == 'folder':
            self.rv.mcontrol.open_playlist(self.dictio)

    def open_prop_dialog(self):
        dialog = MediaPropertiesDialog.open_diag(self.rv.data[self.index])


class MediaPlaylistView(MediaRecycleviewBase):
    queue_view = False

    def __init__(self, **kwargs):
        super(MediaPlaylistView, self).__init__(**kwargs)
        self.viewclass = 'PlaylistViewClass'

    def set_viewed_playlist(self, mcontrol, new_playlist):
        self.playlist_instance = new_playlist
        self.set_data(new_playlist.media)

    def update_data(self):
        self.set_data(self.playlist_instance.media)

    def remove_selected(self):
        remlist = [x['id'] for x in self.get_selected_data()]
        self.playlist_instance.remove_indexes(remlist)

    def add_selected_to_queue(self, *args):
        self.mcontrol.add_to_queue(self.get_selected_data())
