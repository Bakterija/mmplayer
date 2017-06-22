from kivy.properties import ListProperty, NumericProperty
from kivy_soil.app_recycleview import AppRecycleViewClass
from kivy.uix.label import Label


class TerminalWidgetLabel(AppRecycleViewClass, Label):
    def __init__(self, **kwargs):
        super(TerminalWidgetLabel, self).__init__(**kwargs)
        self.fbind('width', self.update_text_width)
        self.max_lines = 1
        self.shorten = True

    def update_text_width(self, _, value):
        self.text_size = (value, None)
