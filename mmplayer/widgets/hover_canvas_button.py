from kivy.properties import StringProperty, ListProperty
from kivy_soil.hover_behavior import HoverBehavior
from kivy.uix.behaviors import ButtonBehavior
from global_vars import theme_manager
from kivy.uix.widget import Widget
from kivy.lang import Builder

class HoverCanvasButton(HoverBehavior, ButtonBehavior, Widget):
    source = StringProperty()
    color = ListProperty([0.8, 0.8, 0.8, 1])


Builder.load_string('''
<HoverCanvasButton>:
    canvas:
        Color:
            rgba: self.color
        Rectangle:
            source: self.source
            size: self.size
            pos: self.pos
''')
