from .media_view_base import MediaButton
from .media_view_base import MediaRecycleviewBase


class QueueViewClass(MediaButton):

    def __init__(self, **kwargs):
        super(QueueViewClass, self).__init__(**kwargs)
        self.children[0].bind(on_release=self.on_release)

    def on_release(self, *args):
        if self.mtype == 'media':
            self.rv.mcontrol.start_queue(self.index)


class MediaQueueView(MediaRecycleviewBase):
    def __init__(self, **kwargs):
        super(MediaQueueView, self).__init__(**kwargs)
        self.viewclass = 'QueueViewClass'

    def set_queue(self, obj, data):
        self.data = data
