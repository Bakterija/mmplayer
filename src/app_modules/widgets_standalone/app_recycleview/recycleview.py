from kivy.properties import ListProperty, StringProperty, BooleanProperty
from kivy.uix.recycleview import RecycleView
from app_modules import key_binder
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.animation import Animation


class AppRecycleView(RecycleView):
    reverse_sorting = BooleanProperty(False)
    filter_text = StringProperty()
    sorting_key = StringProperty()
    data_full = ListProperty()
    filter_keys = None

    def __init__(self, **kwargs):
        super(AppRecycleView, self).__init__(**kwargs)
        self.fbind('reverse_sorting', self.update_data_from_filter)
        self.fbind('filter_text', self.update_data_from_filter)

    def set_data(self, data_full):
        self.data_full = data_full
        self.update_data_from_filter()

    def clear_data(self):
        self.data_full = []
        self.update_data_from_filter()

    def update_data_from_filter(self, *args):
        if not self.filter_text:
            data = self.data_full
        else:
            data = self.get_filtered_data(
                self.data_full, self.filter_keys, self.filter_text)
        if self.children:
            self.children[0].on_data_update_sel(len(self.data), len(data))
        self.data = data

    @staticmethod
    def get_filtered_data(data, filter_keys, find_text):
        templist = []
        find_text = find_text.lower()
        if filter_keys:
            for item in data:
                for key, value in item.items():
                    if key in filter_keys:
                        if isinstance(value, int) or isinstance(value, float):
                            continue
                        if value.lower().find(find_text) != -1:
                            templist.append(item)
                            break
        else:
            for item in data:
                for key, value in item.items():
                    if isinstance(value, int) or isinstance(value, float):
                        continue
                    if value.lower().find(find_text) != -1:
                        templist.append(item)
                        break
        return templist

    def scroll_to_start(self):
        self.scroll_y = 1.0
        self._update_effect_bounds()

    def scroll_to_end(self):
        self.scroll_y = 0.0
        self._update_effect_bounds()

    def page_down(self):
        scroll = RecycleView.convert_distance_to_scroll(
            self, 0, self.height)[1] * 0.9
        self.scroll_y = max(self.scroll_y - scroll, 0.0)
        self._update_effect_bounds()

    def page_up(self):
        scroll = RecycleView.convert_distance_to_scroll(
            self, 0, self.height)[1] * 0.9
        self.scroll_y = min(self.scroll_y + scroll, 1.0)
        self._update_effect_bounds()

    def scroll_to_index(self, index):
        box = self.children[0]
        if box.default_size[1]:
            pos_index = (box.default_size[1] + box.spacing) * index
        else:
            pos_index = 0
            for x in self.data[:index]:
                pos_index += x['height'] + box.spacing
        scroll = self.convert_distance_to_scroll(
            0, pos_index - (self.height * 0.5))[1]
        if scroll > 1.0:
            scroll = 1.0
        elif scroll < 0.0:
            scroll = 0.0
        self.scroll_y = 1.0 - scroll

    def convert_distance_to_scroll(self, dx, dy):
        box = self.children[0]
        if box.default_size[1]:
            wheight = box.default_size[1] + box.spacing
            vp_height = len(self.data) * wheight
        else:
            vp_height = 0
            for x in self.data:
                vp_height += x['height']

        if not self._viewport:
            return 0, 0
        vp = self._viewport

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
