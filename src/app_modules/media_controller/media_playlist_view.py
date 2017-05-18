from .media_view_base import MediaButton
from .media_view_base import MediaRecycleviewBase
from kivymd_modified.menu import MDDropdownMenu, MDMenuItem
from kivy.logger import Logger
from utils.not_implemented import show_error as show_not_implemented
from kivy.clock import Clock, mainthread
from .dialog_properties import MediaPropertiesDialog


class PlaylistViewClass(MediaButton):
    queue_view = False

    def __init__(self, **kwargs):
        super(PlaylistViewClass, self).__init__(**kwargs)

    def get_ctx_items(self):
        selected = self.rv.get_selected_data()
        count_selected = len(selected)
        jump_index = self.rv.find_playing()
        if jump_index != -1:
            can_jump = False
        else:
            can_jump = True
        cant_remove = True
        if self.rv.playlist_instance:
            if self.rv.playlist_instance.can_remove:
                cant_remove = False

        ci = [
            {
                'text': 'Play', 'disabled': False,
                'on_press': self.start_media},
            {
                'text': 'Play selection', 'disabled': False,
                'on_press': lambda *a: self.rv.mcontrol.start_selection(
                    selected)},
            {
                'text': 'Add to queue', 'disabled': False,
                'on_press': self.add_to_queue},
            {
                'text': 'Remove from playlist', 'disabled': cant_remove,
                'on_press': self.rv.remove_selected},
            {
                'text': 'Jump to current played', 'disabled': can_jump,
                'on_press': lambda *a: self.rv.scroll_to_index(jump_index)},
            {
                'text': 'Select all', 'disabled': False,
                'on_press': self.rv.ids.box.select_all},
            {
                'text': 'Deselect all', 'disabled': False,
                'on_press': self.rv.ids.box.deselect_all},
            # Decided not to include it for now
            #
            # {
            #     'text': 'Delete files', 'disabled': False,
            #     'on_press': show_not_implemented},
            {
                'text': 'Properties', 'disabled': False,
                'on_press': self.open_prop_dialog
            }
        ]
        for i, x in enumerate(ci):
            x['viewclass'] = 'MDMenuItem'
            x['index'] = i
        return ci

    def add_to_queue(self, *a):
        self.rv.mcontrol.add_to_queue(self.rv.get_selected_data())

    def start_media(self, *args):
        if self.mtype == 'media':
            self.rv.mcontrol.start_playlist_from_index(
                self.name, self.path, self.index, self.id, self)
        elif self.mtype == 'folder':
            self.rv.mcontrol.open_playlist(self.dictio)

    def open_context_menu(self):
        drop = MDDropdownMenu(items=self.get_ctx_items(), width_mult=7)
        drop.open(self)

    def open_prop_dialog(self):
        dialog = MediaPropertiesDialog.open_diag(self.rv.data[self.index])


class MediaPlaylistView(MediaRecycleviewBase):
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
