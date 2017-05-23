from kivy.properties import BooleanProperty
from kivy.uix.recycleview.views import RecycleDataViewBehavior

class AppRecycleViewClass(RecycleDataViewBehavior):
    selected_last = BooleanProperty()
    selectable = BooleanProperty()
    selected = BooleanProperty()
    index = None

    def refresh_view_attrs(self, rv, index, data):
        super(AppRecycleViewClass, self).refresh_view_attrs(rv, index, data)
        self.index = index
        self.rv = rv

    def apply_selection(self, value):
        if value:
            self.selected = True
        else:
            self.selected = False
