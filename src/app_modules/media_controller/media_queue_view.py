from .media_view_base import MediaButton
from .media_view_base import MediaRecycleviewBase


class QueueViewClass(MediaButton):
    queue_view = True

    def start_media(self, *args):
        if self.mtype == 'media':
            self.rv.mcontrol.start_queue(self.index)


class MediaQueueView(MediaRecycleviewBase):
    def __init__(self, **kwargs):
        super(MediaQueueView, self).__init__(**kwargs)
        self.viewclass = 'QueueViewClass'

    def set_queue(self, obj, data):
        self.data = data
