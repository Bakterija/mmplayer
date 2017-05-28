from .media_view_base import MediaButton
from .media_view_base import MediaRecycleviewBase
from kivy.logger import Logger
from utils.not_implemented import show_error as show_not_implemented
from kivymd_modified.menu import MDDropdownMenu, MDMenuItem
from .dialog_properties import MediaPropertiesDialog


class QueueViewClass(MediaButton):
    queue_view = True

    def start_media(self, *args):
        if self.mtype == 'media':
            self.rv.mcontrol.start_queue(self.index)

    def open_prop_dialog(self):
        dialog = MediaPropertiesDialog.open_diag(self.rv.data[self.index])

class MediaQueueView(MediaRecycleviewBase):
    queue_view = True

    def __init__(self, **kwargs):
        super(MediaQueueView, self).__init__(**kwargs)
        self.viewclass = 'QueueViewClass'

    def set_queue(self, obj, data):
        self.data = data

    def remove_selected(self):
        remlist = sorted(list(self.children[0].selected_widgets))
        self.mcontrol.queue_remove_indexes(remlist)
