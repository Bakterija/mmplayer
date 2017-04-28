from kivy.properties import StringProperty, DictProperty, ListProperty
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from app_modules.behaviors.hover_behavior import HoverBehavior
from app_modules.behaviors.focus import FocusBehaviorCanvas
from kivy.uix.recycleview import RecycleView
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.stacklayout import StackLayout
from kivy.lang import Builder
from kivy.utils import platform
from kivy.metrics import cm


class MediaButton(HoverBehavior, RecycleDataViewBehavior,
                  ButtonBehavior, StackLayout):
    index = None
    rv = None
    bg_colors = DictProperty()
    pstate = StringProperty()
    mtype = StringProperty()
    text = StringProperty()
    name = StringProperty()
    path = StringProperty()
    bg_color = ListProperty()

    def __init__(self, **kwargs):
        super(MediaButton, self).__init__(**kwargs)

    def refresh_view_attrs(self, rv, index, data):
        super(MediaButton, self).refresh_view_attrs(rv, index, data)
        self.index = index
        self.hovering = False
        self.set_bg_color()
        if not self.rv:
            self.rv = rv

    def set_bg_color(self, *args):
        if self.hovering == True and self.pstate != 'playing':
            self.bg_color = self.bg_colors['hover']
        else:
            if self.mtype == 'media':
                self.bg_color = self.bg_colors[self.pstate]
            elif self.mtype == 'folder':
                self.bg_color = self.bg_colors['folder']
            elif self.mtype == 'disabled':
                self.bg_color = self.bg_colors['folder']

    def on_enter(self, *args):
        if self.pstate != 'playing':
            self.set_bg_color()

    def on_leave(self, *args):
        if self.pstate != 'playing':
            self.set_bg_color()


class MediaRecycleviewBase(FocusBehaviorCanvas, RecycleView):
    pass


if platform == 'android':
    Builder.load_file('app_modules/media_controller/controller.kv')
else:
    Builder.load_file('app_modules/media_controller/controller.kv')
