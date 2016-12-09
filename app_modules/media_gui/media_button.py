from app_modules.wodgets.multi_line_label import MultiLineLabel
from multi_line_button import MultiLineButton
from kivy.properties import BooleanProperty
from kivy.properties import StringProperty
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.metrics import cm


class Media_Button(RecycleDataViewBehavior, Label):
    index = None  # stores our index
    selected = BooleanProperty(False)
    selectable = BooleanProperty(False)
    name = StringProperty()
    
    def __init__(self,*args, **kwargs):
        super(Media_Button, self).__init__(**kwargs)

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
