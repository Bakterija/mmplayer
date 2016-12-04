from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from media_gui import Media_Button
from media_gui import MRV_Base
import traceback

class PlaylistViewClass(Media_Button):
    def __init__(self, **kwargs):
        super(PlaylistViewClass, self).__init__(**kwargs)
        self.children[0].bind(on_release=self.on_release)

    def on_release(self, *args):
        if self.mtype == 'media':
            self.mgui.start_playlist(self.name, self.path, self.index, self)
        elif self.mtype == 'folder':
            self.mgui.open_playlist(self.dictio)


class MediaPlaylistView(MRV_Base):
    def __init__(self, media_gui, **kwargs):
        super(MediaPlaylistView, self).__init__(**kwargs)
        self.mgui = media_gui
        self.viewclass = 'PlaylistViewClass'
        self.data = []
        self.mgui.rv_playlist = self

    def on_playlist(self, active_playlist):
        self.data = active_playlist['files']
