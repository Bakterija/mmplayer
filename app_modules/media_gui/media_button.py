from multi_line_button import MultiLineButton
from kivy.properties import BooleanProperty
from kivy.properties import StringProperty
from kivy.properties import StringProperty

from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.metrics import cm


class Media_Button(RecycleDataViewBehavior, Label):
    def __init__(self,*args, **kwargs):
        super(Media_Button, self).__init__(**kwargs)
        self.colors = {'default': (0.5, 0.5, 1, 1),
                       'playing': (0.7,0.3,0.5,1),
                       'disabled': (0.3,0.3,0.3,1)}
        self.height = cm(1)
        index = None  # stores our index
        selected = BooleanProperty(False)
        selectable = BooleanProperty(False)
        name = StringProperty()

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super(Media_Button, self).refresh_view_attrs(rv, index, data)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected

    def on_touch_down(self, touch):
        if super(Media_Button, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)


class Media_Button_Playlist(Media_Button):
    # def __init__(self,*args, **kwargs):
    #     super(Media_Button_Playlist, self).__init__(**kwargs)
        # self.background_color = self.colors['default']
        # self.bind(on_release= self.play)
        # self.playing = False
    index = None  # stores our index
    selected = BooleanProperty(False)
    selectable = BooleanProperty(False)
    name = StringProperty()

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super(Media_Button_Playlist, self).refresh_view_attrs(rv, index, data)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected

    def on_touch_down(self, touch):
        if super(Media_Button_Playlist, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def play(self,*arg):
        self.mgui.start(self)


class Media_Button_Queue(Media_Button):
    def __init__(self,*args, **kwargs):
        super(Media_Button_Queue, self).__init__(**kwargs)
        self.background_color = self.colors['default']
        self.bind(on_release=lambda x: self.mgui.start(self))
