from behaviors.resizable.resize import ResizableBehavior
from kivy.uix.boxlayout import BoxLayout


class ResizableBoxLayout(ResizableBehavior, BoxLayout):
    '''A BoxLayout which inherits from resizable_behavior'''
