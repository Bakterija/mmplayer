from behaviors.resizable.resize import ResizableBehavior
from kivy.uix.boxlayout import BoxLayout
##from kivy.garden.resizable_behavior import ResizableBehavior


class ResizableBoxLayout(ResizableBehavior, BoxLayout):
    def __init__(self, **kwargs):
        super(ResizableBoxLayout, self).__init__(**kwargs)
