from .media_view_base import MediaButton
from .media_view_base import MediaRecycleviewBase
from kivy.logger import Logger
from utils.not_implemented import show_error as show_not_implemented
from kivymd_modified.menu import MDDropdownMenu, MDMenuItem
from .dialog_properties import MediaPropertiesDialog


class QueueViewClass(MediaButton):
    queue_view = True

    def get_ctx_items(self):
        selected = self.rv.get_selected_data()
        count_selected = len(selected)
        jump_index = self.rv.find_playing()
        if jump_index != -1:
            can_jump = False
        else:
            can_jump = True

        ci = [
            {
                'text': 'Play', 'disabled': False,
                'on_press': self.start_media},
            {
                'text': 'Clear queue', 'disabled': False,
                'on_press': self.rv.mcontrol.clear_queue},
            {
                'text': 'Jump to current played', 'disabled': can_jump,
                'on_press': lambda *a: self.rv.scroll_to_index(jump_index)},
            {
                'text': 'Properties', 'disabled': False,
                'on_press': self.open_prop_dialog
            }
        ]
        for i, x in enumerate(ci):
            x['viewclass'] = 'MDMenuItem'
            x['index'] = i
        return ci

    def start_media(self, *args):
        if self.mtype == 'media':
            self.rv.mcontrol.start_queue(self.index)

    def open_context_menu(self):
        drop = MDDropdownMenu(items=self.get_ctx_items(), width_mult=7)
        drop.open(self)

    def open_prop_dialog(self):
        dialog = MediaPropertiesDialog.open_diag(self.rv.data[self.index])

class MediaQueueView(MediaRecycleviewBase):
    def __init__(self, **kwargs):
        super(MediaQueueView, self).__init__(**kwargs)
        self.viewclass = 'QueueViewClass'

    def set_queue(self, obj, data):
        self.data = data
