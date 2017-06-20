from kivy.properties import ObjectProperty
from kivy.uix.textinput import TextInput
from kivy.base import EventLoop
from time import time

class TextInput2(TextInput):
    scroller = ObjectProperty()

    def on_scroller(self, _, value):
        if value:
            value.bind(on_touch_down=self.testmethod)

    def testmethod(self, _, touch):
        x, y = self.to_widget(touch.x, touch.y)
        if self.collide_point(x, y):
            self.scroller.dont_do_scrolling = True

    def on_touch_up(self, touch):
        if self.scroller:
            if self.scroller.dont_do_scrolling:
                self.scroller.dont_do_scrolling = False
        return super(TextInput2, self).on_touch_up(touch)
