from app_modules.widgets_standalone.app_recycleview import AppRecycleViewClass
from app_modules.behaviors.hover_behavior import HoverBehavior
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock


class SideBarViewBase(HoverBehavior, AppRecycleViewClass, ButtonBehavior):
    text = StringProperty()
    wtype = StringProperty()
    hovering = BooleanProperty(False)
    index = None
    func = None
    func2 = None

    def do_func(self):
        if self.func:
            self.func()
            if not self.selected:
                self.parent.select_with_touch(self.index)

    def on_left_click(self):
        pass

    def on_right_click(self):
        pass

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            if touch.device == 'mouse':
                if touch.button == 'left':
                    self.on_left_click()
                elif touch.button == 'right':
                    self.on_right_click()
            else:
                self.do_func()
            return True
