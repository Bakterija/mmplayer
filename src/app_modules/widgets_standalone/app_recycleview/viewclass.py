from kivy.properties import BooleanProperty


class AppRecycleViewClass(object):
    selected = BooleanProperty()
    selected_last = BooleanProperty()
    index = None

    def apply_selection(self, value):
        if value:
            self.selected = True
        else:
            self.selected = False
