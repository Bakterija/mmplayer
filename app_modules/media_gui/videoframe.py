from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
if platform in ('linux', 'win'):
    from kivy.core.window import Window


class VideoFrame(BoxLayout):
    orientation = 'vertical'
    full_screen_check = None
    maximized = False
    maximizer_mode = 0

    def __init__(self, **kwargs):
        super(VideoFrame, self).__init__(**kwargs)
        if platform in ('linux', 'win'):
            Window.bind(on_maximize=self.on_maximize)
            Window.bind(on_restore=self.on_restore)

    def on_touch_down(self, touch):
        if platform in ('linux', 'win'):
            if touch.is_double_tap:
                if self.full_screen_check:
                    if self.full_screen_check():
                        if self.maximizer_mode == 0:
                            self.maximize_borderless_toggle()
                        elif self.maximizer_mode == 1:
                            self.maximize_full_screen()

    def maximize_borderless_toggle(self):
        if self.maximized:
            Window.restore()
            self.maximized = False
        else:
            Window.maximize()
            self.maximized = True

    def maximize_full_screen(self):
        if self.maximized:
            Window.fullscreen = False
            self.maximized = False
        else:
            Window.fullscreen = True
            self.maximized = True

    def on_maximize(self, *args):
        self.maximized = True

    def on_restore(self, *args):
        self.maximized = False
