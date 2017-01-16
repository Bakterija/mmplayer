from controller import Media_Button
from controller import MRV_Base


class PlaylistViewClass(Media_Button):

    def __init__(self, **kwargs):
        super(PlaylistViewClass, self).__init__(**kwargs)
        self.children[0].bind(on_release=self.on_release)

    def on_release(self, *args):
        if self.mtype == 'media':
            self.rv.controller.start_playlist(
                self.name, self.path, self.index, self)
        elif self.mtype == 'folder':
            self.rv.controller.open_playlist(self.dictio)


class MediaPlaylistView(MRV_Base):
    def __init__(self, controller, **kwargs):
        super(MediaPlaylistView, self).__init__(**kwargs)
        self.controller = controller
        self.viewclass = 'PlaylistViewClass'
        self.data = []
        self.controller.rv_playlist = self

    def on_playlist(self, active_playlist):
        self.data = active_playlist['files']
