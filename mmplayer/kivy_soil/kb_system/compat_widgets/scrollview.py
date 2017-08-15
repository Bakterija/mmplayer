from kivy.uix.scrollview import ScrollView
from kivy_soil.kb_system import keys


class AppScrollView(ScrollView):
    def on_key_down(self, key, modifier):
        if key == keys.UP:
            self.scroll_up_slightly()
        elif key == keys.DOWN:
            self.scroll_down_slightly()
        elif key == keys.PAGE_UP:
            self.page_up()
        elif key == keys.PAGE_DOWN:
            self.page_down()
        elif key == keys.HOME:
            self.scroll_to_start()
        elif key == keys.END:
            self.scroll_to_end()

    def scroll_to_start(self):
        self.scroll_y = 1.0
        self._update_effect_bounds()

    def scroll_to_end(self):
        self.scroll_y = 0.0
        self._update_effect_bounds()

    def scroll_up_slightly(self):
        '''Scrolls viewport down by it's height * 0.1'''
        scroll = ScrollView.convert_distance_to_scroll(
            self, 0, self.height)[1] * 0.1
        self.scroll_y = min(self.scroll_y + scroll, 1.0)
        self._update_effect_bounds()

    def scroll_down_slightly(self):
        '''Scrolls viewport down by it's height * 0.1'''
        scroll = ScrollView.convert_distance_to_scroll(
            self, 0, self.height)[1] * 0.1
        self.scroll_y = max(self.scroll_y - scroll, 0.0)
        self._update_effect_bounds()

    def page_down(self):
        '''Scrolls viewport down by it's height * 0.9'''
        scroll = ScrollView.convert_distance_to_scroll(
            self, 0, self.height)[1] * 0.9
        self.scroll_y = max(self.scroll_y - scroll, 0.0)
        self._update_effect_bounds()

    def page_up(self):
        '''Scrolls viewport up by it's height * 0.9'''
        scroll = ScrollView.convert_distance_to_scroll(
            self, 0, self.height)[1] * 0.9
        self.scroll_y = min(self.scroll_y + scroll, 1.0)
        self._update_effect_bounds()
