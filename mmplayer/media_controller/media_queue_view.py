from utils.not_implemented import show_error as show_not_implemented
from .media_view_base import MediaRecycleviewBase
from .media_view_base import MediaButton
from kivy.logger import Logger


class QueueViewClass(MediaButton):
    '''Playlists and media player queue have some differences, this
    works with media player queue'''

    queue_view = True

    def start_media(self, *args):
        '''Starts playing at selected index in queue'''
        if self.mtype == 'media':
            self.rv.mcontrol.start_queue(self.index)


class MediaQueueView(MediaRecycleviewBase):
    queue_view = True

    def __init__(self, **kwargs):
        super(MediaQueueView, self).__init__(**kwargs)
        self.viewclass = 'QueueViewClass'

    def set_queue(self, obj, data):
        self.set_data(data)

    def remove_selected(self):
        '''Removes selected indexes from media player queue'''
        remlist = sorted(list(self.children[0].selected_widgets))
        self.mcontrol.queue_remove_indexes(remlist)
