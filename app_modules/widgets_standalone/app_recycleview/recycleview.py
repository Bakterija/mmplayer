from kivy.uix.recycleview import RecycleView
from app_modules import key_binder
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.animation import Animation


class AppRecycleView(RecycleView):

    def set_data(self, value):
        if self.children:
            self.children[0].on_data_update_sel(len(self.data), len(value))
        self.data = value

    def page_down(self):
        scroll = self.convert_distance_to_scroll(0, self.height)[1] * 0.9
        self.scroll_y = max(self.scroll_y - scroll, 0.0)
        self._update_effect_bounds()

    def page_up(self):
        scroll = self.convert_distance_to_scroll(0, self.height)[1] * 0.9
        self.scroll_y = min(self.scroll_y + scroll, 1.0)
        self._update_effect_bounds()

    def scroll_to_index(self, index):
        box = self.children[0]
        if not box.default_size[1]:
            return
        pos_index = (box.default_size[1] + box.spacing) * index
        scroll = self.convert_distance_to_scroll(
            0, pos_index - (self.height * 0.5))[1]
        if scroll > 1.0:
            scroll = 1.0
        elif scroll < 0.0:
            scroll = 0.0
        self.scroll_y = 1.0 - scroll

    def convert_distance_to_scroll(self, dx, dy):
        box = self.children[0]
        wheight = box.default_size[1] + box.spacing

        if not self._viewport:
            return 0, 0
        vp = self._viewport
        vp_height = len(self.data) * wheight
        if vp.width > self.width:
            sw = vp.width - self.width
            sx = dx / float(sw)
        else:
            sx = 0
        if vp_height > self.height:
            sh = vp_height - self.height
            sy = dy / float(sh)
        else:
            sy = 1
        return sx, sy
