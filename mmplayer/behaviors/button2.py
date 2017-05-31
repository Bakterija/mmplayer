class ButtonBehavior2(object):
    '''A differet ButtonBehavior implementation
    Passes touch.button and touch.is_double_tap as
    on_press and on_release method arguments'''

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.on_press(touch.button, touch.is_double_tap)
            return True
        return False

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self.on_release(touch.button, touch.is_double_tap)
            return True
        return False

    def on_press(self, button, double_tap):
        pass

    def on_release(self, button, double_tap):
        pass
