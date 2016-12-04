from app_modules.behaviors.resizable.resize import ResizableBehavior
from kivy.uix.boxlayout import BoxLayout


class ResizableBoxLayout(ResizableBehavior, BoxLayout):
    def __init__(self, **kwargs):
        super(ResizableBoxLayout, self).__init__(**kwargs)
