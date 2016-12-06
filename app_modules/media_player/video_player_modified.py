from __future__ import print_function
from kivy.uix.video import Video as VideoPlayer


class VideoPlayerModified(VideoPlayer):
    def __init__(self, **kwargs):
        super(VideoPlayerModified, self).__init__(**kwargs)
        self.modified_stop_callback = None
        self.allow_stretch = True

    def set_texture_si(self, *args):
        self.texture_size = self.size

    def on_state(self, instance, value):
        super(VideoPlayerModified, self).on_state(instance, value)
        if value == 'stop' and self.modified_stop_callback:
            self.modified_stop_callback()

    def seek(self, value):
        super(VideoPlayerModified, self).seek(value)

    def bind(self, **kwargs):
        super(VideoPlayerModified, self).bind(**kwargs)
        if 'on_stop' in kwargs:
            self.modified_stop_callback = kwargs['on_stop']

    def _play_started(self, instance, value):
        self.container.clear_widgets()
        self.container.add_widget(self._video)
