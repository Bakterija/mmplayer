from kivy.properties import BooleanProperty, NumericProperty
from kivy.uix.recycleview.views import RecycleDataViewBehavior

class AppRecycleViewClass(RecycleDataViewBehavior):
    '''The base ViewClass for AppRecycleView
    includes mandatory selection properties, index attribute and
    methods to make those work'''

    selected = BooleanProperty(False)
    selected_last = BooleanProperty()
    selectable = BooleanProperty()
    index = NumericProperty()

    def refresh_view_attrs(self, rv, index, data):
        super(AppRecycleViewClass, self).refresh_view_attrs(rv, index, data)
        self.index = index
        self.rv = rv

    def apply_selection(self, value):
        if self.selectable:
            self.selected = value
        elif self.selected:
            self.selected = False
