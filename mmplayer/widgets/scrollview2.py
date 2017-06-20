from kivy.uix.scrollview import ScrollView

class ScrollView2(ScrollView):
    dont_do_scrolling = False

    def on_touch_down(self, touch):
        if self.dont_do_scrolling:
            self.simulate_touch_down(touch)
            return True

        elif self.dispatch('on_scroll_start', touch):
            self._touch = touch
            touch.grab(self)
            return True
