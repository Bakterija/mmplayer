from utils.not_implemented import show_error as show_not_implemented
from .media_view_base import MediaRecycleviewBase
from .media_view_base import MediaButton
from kivy.clock import Clock, mainthread
from kivy.logger import Logger


class PlaylistViewClass(MediaButton):
    '''Playlists and media player queue have some differences, this
    works with normal playlists'''

    queue_view = False

    def __init__(self, **kwargs):
        super(PlaylistViewClass, self).__init__(**kwargs)

    def start_media(self, *args):
        '''Adds selected media to queue and starts playing'''
        if self.mtype == 'media':
            self.rv.mcontrol.start_playlist_from_index(
                self.name, self.path, self.index, self.id, self)
        elif self.mtype == 'folder':
            self.rv.mcontrol.open_playlist(self.dictio)


class MediaPlaylistView(MediaRecycleviewBase):
    queue_view = False

    def __init__(self, **kwargs):
        super(MediaPlaylistView, self).__init__(**kwargs)
        self.viewclass = 'PlaylistViewClass'

    def set_viewed_playlist(self, mcontrol, new_playlist):
        '''Updates self.playlist_instance and refreshes view when user
        selects a new playlist'''
        self.playlist_instance = new_playlist
        self.set_data(new_playlist.media)

    def update_data(self):
        '''Updates data from self.playlist_instance.media list'''
        self.set_data(self.playlist_instance.media)

    def remove_selected(self):
        '''Removes selected media from view and self.playlist_instance '''
        remlist = [x['id'] for x in self.get_selected_data()]
        self.playlist_instance.remove_indexes(remlist)

    def add_selected_to_queue(self, *args):
        '''Adds selected to end of media player queue'''
        self.mcontrol.add_to_queue(self.get_selected_data())
