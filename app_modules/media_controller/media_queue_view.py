from media_view_base import MediaButton
from media_view_base import MediaRecycleviewBase


class QueueViewClass(MediaButton):

    def __init__(self, **kwargs):
        super(QueueViewClass, self).__init__(**kwargs)
        self.children[0].bind(on_release=self.on_release)

    def on_release(self, *args):
        if self.mtype == 'media':
            self.rv.controller.start_queue(self.index)


class MediaQueueView(MediaRecycleviewBase):
    def __init__(self, controller, **kwargs):
        super(MediaQueueView, self).__init__(**kwargs)
        self.controller = controller
        self.viewclass = 'QueueViewClass'
        self.controller.rv_queue = self
        controller.bind(queue=self.on_queue)

    def on_queue(self, obj, data):
        self.data = data
