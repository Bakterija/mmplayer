from kivy.properties import ListProperty, StringProperty, BooleanProperty
from kivy.uix.recycleview import RecycleView
from kivy_soil.kb_system import keys
from kivy.animation import Animation
from operator import itemgetter
from kivy.logger import Logger
from kivy.clock import Clock
from kivy.metrics import dp


class AppRecycleView(RecycleView):
    reverse_sorting = BooleanProperty(False)
    filter_text = StringProperty()
    '''StringProperty that is used to filter text,
    self.update_data_from_filter() is called when it changes'''

    filter_keys = ListProperty()
    '''ListProperty with update_data_from_filter method data keys'''

    sorting_key = StringProperty()
    '''StringProperty is used in update_data_from_filter method for sorting'''

    data_full = ListProperty()
    '''ListProperty that stores all widget data unsorted'''

    filters = ListProperty()

    def __init__(self, **kwargs):
        super(AppRecycleView, self).__init__(**kwargs)
        self.fbind('reverse_sorting', self.update_data_from_filter)
        self.fbind('filter_text', self.update_data_from_filter)
        self.fbind('filter_keys', self.update_data_from_filter)
        self.fbind('sorting_key', self.update_data_from_filter)

    def on_key_down(self, key, modifier):
        '''Default keys for kivy_soil focus behavior'''
        if key == keys.UP:
            self.children[0].on_arrow_up()
        elif key == keys.DOWN:
            self.children[0].on_arrow_down()
        elif key == keys.PAGE_UP:
            self.page_up()
        elif key == keys.PAGE_DOWN:
            self.page_down()
        elif key == keys.HOME:
            self.scroll_to_start()
        elif key == keys.END:
            self.scroll_to_end()
        elif key in (keys.MENU, keys.MENU_WIN):
            drop = self.children[0].open_context_menu()
        elif key == keys.ESC:
            self.remove_focus()

    def set_data(self, data_full):
        '''Sets self.data_full, call updates data from filter, then sorts.
        Use this for updating data'''
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
        data = self.sort_data(data, self.reverse_sorting, self.sorting_key)
        if self.children:
            self.children[0].on_data_update_sel(len(self.data), len(data))
        for x in self.filters:
            data = x(data)
        self.data = data
        self.refresh_from_data()

    @staticmethod
    def get_filtered_data(data, filter_keys, find_text):
        '''Filters a data list with dict items and returns it'''
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

    @staticmethod
    def sort_data(data, reverse_sorting, sorting_key):
        '''Sorts a data list with dict items and returns it'''
        if sorting_key:
            data = sorted(data, key=itemgetter(sorting_key))
            if reverse_sorting:
                data = list(reversed(data))
        return data

    def scroll_to_start(self):
        self.scroll_y = 1.0
        self._update_effect_bounds()

    def scroll_to_end(self):
        self.scroll_y = 0.0
        self._update_effect_bounds()

    def page_down(self):
        '''Scrolls viewport down by it's height * 0.9'''
        scroll = RecycleView.convert_distance_to_scroll(
            self, 0, self.height)[1] * 0.9
        self.scroll_y = max(self.scroll_y - scroll, 0.0)
        self._update_effect_bounds()

    def page_up(self):
        '''Scrolls viewport up by it's height * 0.9'''
        scroll = RecycleView.convert_distance_to_scroll(
            self, 0, self.height)[1] * 0.9
        self.scroll_y = min(self.scroll_y + scroll, 1.0)
        self._update_effect_bounds()

    def scroll_to_index(self, index):
        '''Scrolls viewport to place where a widget with index argument is'''
        box = self.children[0]
        if box.default_size[1]:
            pos_index = (box.default_size[1] + box.spacing) * index
        else:
            pos_index = 0
            try:
                for x in self.data[:index]:
                    pos_index += x['height'] + box.spacing
            except KeyError:
                pos_index = -1
                self._log_height_key_warning('scroll_to_index')
        if not pos_index == -1:
            scroll = self.convert_distance_to_scroll(
                0, pos_index - (self.height * 0.5))[1]
            if scroll > 1.0:
                scroll = 1.0
            elif scroll < 0.0:
                scroll = 0.0
            self.scroll_y = 1.0 - scroll

    def _log_height_key_warning(self, funcname):
        Logger.warning((
            'AppRecycleView: {}: '
            'no default height has been set and data dictionaries '
            'do not have a height value, scrolling to selected index '
            'will not work').format(funcname))

    def convert_distance_to_scroll(self, dx, dy):
        '''Modified convert_distance_to_scroll method for better reliability'''
        box = self.children[0]
        if box.default_size[1]:
            wheight = box.default_size[1] + box.spacing
            vp_height = len(self.data) * wheight
        else:
            try:
                vp_height = 0
                for x in self.data:
                    vp_height += x['height']
            except KeyError:
                self._log_height_key_warning('convert_distance_to_scroll')
                return 0, 0

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

    def find_index_by_text(
        self, key, value, multiple=False, match=False, case_sensitive=False):
        '''Looks for text in data. If match is True, compares first letters to
        value. Returns list with found index number or numbers'''
        templist = []
        if not case_sensitive:
            value = value.lower()
        for i, item in enumerate(self.data):
            v = item.get(key, None)
            if v:
                if not case_sensitive:
                    v = v.lower()
                found = False
                if match:
                    if v[:len(value)] == value:
                        found = True
                else:
                    if v.find(value) != -1:
                        found = True
                if found:
                    templist.append(i)
                    if not multiple:
                        break
        return templist
