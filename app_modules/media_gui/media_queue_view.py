from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from media_gui import Media_Button
from media_gui import MRV_Base


class QueueViewClass(Media_Button):
    def __init__(self, **kwargs):
        super(QueueViewClass, self).__init__(**kwargs)
        self.children[0].bind(on_release=self.on_release)

    def on_release(self, *args):
        if self.mtype == 'media':
            self.mgui.start_queue(self.index)


class MediaQueueView(MRV_Base):
    def __init__(self, media_gui, **kwargs):
        super(MediaQueueView, self).__init__(**kwargs)
        self.mgui = media_gui
        self.viewclass = 'QueueViewClass'
        self.mgui.rv_queue = self
        media_gui.bind(queue=self.on_queue)

    def on_queue(self, obj, data):
        self.data = data
