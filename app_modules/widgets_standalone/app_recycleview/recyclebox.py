from kivy.uix.recycleboxlayout import RecycleBoxLayout
from app_modules import key_binder
from kivy.clock import Clock


class AppRecycleBox(RecycleBoxLayout):
    selected_widgets = None
    sel_first = -1
    sel_last = -1
    desel_index = 0

    def __init__(self, **kwargs):
        super(AppRecycleBox, self).__init__(**kwargs)
        key_binder.add('arrow_up', 273, 'down', self.on_arrow_up)
        key_binder.add('arrow_down', 274, 'down', self.on_arrow_down)
        key_binder.add(
            'select_all', 97, 'down', self.select_all, modifier=['ctrl'])
        key_binder.add(
            'deselect_all', 32, 'down', self.deselect_all, modifier=['ctrl'])
        key_binder.add(
            'context_menu', 1073741942, 'down', self.open_context_menu)
        self.selected_widgets = set()

    def on_data_update_sel(self, len_old, len_new):
        def next_frame_task(*a):
            if self.sel_last > len_new:
                if len_new < len_old:
                    self.sel_last = len_new - 1
                    if self.sel_first > len_new - 1:
                        self.sel_first = self.sel_last
                    self.selected_widgets.add(self.sel_last)
                    for i in list(self.selected_widgets):
                        if i > len_new - 1:
                            self.selected_widgets.remove(i)
                    self._update_selected()
                    self._scroll_to_selected()
        Clock.schedule_once(next_frame_task, 0)

    def get_modifier_mode(self):
        mode = ''
        if key_binder.ctrl_held and key_binder.shift_held:
            mode = ''
        elif key_binder.ctrl_held:
            mode = 'ctrl'
        elif key_binder.shift_held:
            mode = 'shift'
        return mode

    def on_arrow_up(self):
        if self.desel_index and self.sel_last == -1:
            self.sel_last = self.desel_index
            self.desel_index = 0

        if self.sel_last is 0:
            return

        mode = self.get_modifier_mode()
        if self.children:
            if mode in ('', 'ctrl'):
                self.sel_first = self.sel_last - 1
                self.sel_last = self.sel_first
                self.selected_widgets = {self.sel_first}
            elif mode == 'shift':
                new_last = self.sel_last
                new_last -= 1
                if new_last >= self.sel_first:
                    self.add_remove_selected_set(self.sel_last)
                elif new_last not in self.selected_widgets:
                    self.add_remove_selected_set(new_last)
                self.sel_last = new_last

        self._update_selected()
        self._scroll_to_selected()

    def on_arrow_down(self):
        if self.desel_index and self.sel_last == -1:
            self.sel_last = self.desel_index
            self.desel_index = 0

        sel_max = len(self.parent.data) - 1
        mode = self.get_modifier_mode()

        if self.children:
            if mode in ('', 'ctrl'):
                self.sel_first = min(self.sel_last + 1, sel_max)
                self.sel_last = self.sel_first
                self.selected_widgets = {self.sel_first}
            elif mode == 'shift':
                new_last = min(self.sel_last, sel_max)
                if new_last != sel_max:
                    new_last += 1
                    if new_last <= self.sel_first:
                        self.add_remove_selected_set(self.sel_last)
                    elif new_last not in self.selected_widgets:
                        self.add_remove_selected_set(new_last)
                    self.sel_last = new_last
        self._update_selected()
        self._scroll_to_selected()

    def select_with_touch(self, index):
        mode = self.get_modifier_mode()
        if self.sel_first == -1:
            self.sel_first = 0

        if mode in ('', 'ctrl'):
            self.sel_first = index
            self.sel_last = self.sel_first
            if not mode:
                self.selected_widgets = {self.sel_first}
            else:
                self.add_remove_selected_set(index)
        elif mode == 'shift':
            self.sel_last = index
            if self.sel_first < index:
                start, end = self.sel_first, index
            else:
                start, end = index, self.sel_first

            self.selected_widgets = set()
            for x in range(start, end+1):
                self.selected_widgets.add(x)
        self.parent.refresh_from_layout()

    def select_all(self):
        for i in range(len(self.parent.data)):
            self.selected_widgets.add(i)
        self._update_selected()


    def deselect_all(self):
        self.selected_widgets = set()
        self.desel_index = self.sel_last
        self.sel_first, self.sel_last = -1, -1
        self._update_selected()

    def add_remove_selected_set(self, index, index2=None):
        if index in self.selected_widgets:
            self.selected_widgets.remove(index)
            if index2 and index2 in self.selected_widgets:
                self.selected_widgets.remove(index2)
        else:
            self.selected_widgets.add(index)

    def open_context_menu(self, pos=None):
        if not pos:
            for x in self.children:
                if x.index == self.sel_last:
                    pos = x.to_window(x.right, x.y)
                    break
        if not pos:
            return
        self.context_menu_function(pos)

    def context_menu_function(self, pos):
        pass

    def get_widget_from_index(self, index):
        for x in self.children:
            if x.index == index:
                return x
        return None

    def _scroll_to_selected(self):
        self.parent.scroll_to_index(self.sel_last)

    def _update_selected(self):
        for x in self.children:
            if x.index in self.selected_widgets:
                if not x.selected:
                    x.apply_selection(True)
            else:
                if x.selected:
                    x.apply_selection(False)
            if x.selected_last and x.index != self.sel_last:
                x.selected_last = False
            elif x.index == self.sel_last:
                x.selected_last = True

    def on_children(self, _, __):
        self._update_selected()
