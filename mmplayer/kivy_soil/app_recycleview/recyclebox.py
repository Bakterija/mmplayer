from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.clock import Clock
from kivy_soil import kb_system


class AppRecycleBoxLayout(RecycleBoxLayout):
    selected_widgets = None
    '''Set with indexes of selected widgets'''

    sel_first = -1
    '''Index of first selected widget of current multiselect'''

    sel_last = -1
    '''Index of last selected widget of current multiselect'''

    desel_index = 0
    '''Index of last deselected widget'''

    def __init__(self, **kwargs):
        super(AppRecycleBoxLayout, self).__init__(**kwargs)
        self.fbind('children', self.update_selected)
        self.selected_widgets = set()

    def on_data_update_sel(self, len_old, len_new):
        '''Triggers selection update when data is changed'''
        Clock.schedule_once(
            lambda *a: self.on_data_next_frame_task(len_old, len_new), 0)

    def on_data_next_frame_task(self, len_old, len_new):
        '''Updates selection when data is changed'''
        if self.sel_last > len_new:
            if len_new < len_old:
                self.sel_last = len_new - 1
                if self.sel_first > len_new - 1:
                    self.sel_first = self.sel_last
                self.selected_widgets.add(self.sel_last)
                for i in list(self.selected_widgets):
                    if i > len_new - 1:
                        self.selected_widgets.remove(i)
                self.update_selected()
                self.scroll_to_selected()

    def _get_modifier_mode(self):
        mode = ''
        if kb_system.held_ctrl and kb_system.held_shift:
            mode = ''
        elif kb_system.held_ctrl:
            mode = 'ctrl'
        elif kb_system.held_shift:
            mode = 'shift'
        return mode

    def on_arrow_up(self):
        '''Call this when up selection button is pressed,
        Selects previous widget, supports multiselect with shift modifier'''
        if self.desel_index and self.sel_last == -1:
            self.sel_last = self.desel_index
            self.desel_index = 0

        if self.sel_last is 0:
            return

        mode = self._get_modifier_mode()
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
        self.update_selected()
        self.scroll_to_selected()

    def on_arrow_down(self):
        '''Call this when down selection button is pressed,
        Selects next widget, supports multiselect with shift modifier'''
        if self.desel_index and self.sel_last == -1:
            self.sel_last = self.desel_index
            self.desel_index = 0

        sel_max = len(self.parent.data) - 1
        mode = self._get_modifier_mode()

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
        self.update_selected()
        self.scroll_to_selected()

    def select_with_touch(self, index):
        '''Call to select with touch, supports single and multiple
        multiselect modes with ctrl and shift modifiers'''
        mode = self._get_modifier_mode()
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
        self.update_selected()

    def select_all(self):
        for i in range(len(self.parent.data)):
            self.selected_widgets.add(i)
        self.update_selected()

    def deselect_all(self):
        self.selected_widgets = set()
        self.desel_index = self.sel_last
        self.sel_first, self.sel_last = -1, -1
        self.update_selected()

    def add_remove_selected_set(self, index, index2=None):
        '''Toggles index numbers in self.selected_widgets'''
        if index in self.selected_widgets:
            self.selected_widgets.remove(index)
            if index2 and index2 in self.selected_widgets:
                self.selected_widgets.remove(index2)
        else:
            self.selected_widgets.add(index)

    def open_context_menu(self, pos=None):
        widget = None
        if self.sel_last != -1:
            for x in self.children:
                if x.index == self.sel_last:
                    pos = x.to_window(x.right, x.y)
                    widget, widget_index = x, x.index
                    break
        if widget:
            self.context_menu_function(widget, widget_index, pos)
        else:
            self.context_menu_function(self, None, self.pos)

    def context_menu_function(self, child, index, pos):
        '''Stub method for context menu'''
        pass

    def get_widget_from_index(self, index):
        '''Returns child with argument index when it is in view,
        otherwise returns nothing'''
        for x in self.children:
            if x.index == index:
                return x

    def get_selected_widget(self, *args):
        '''Returns child selected child when it is in view,
        otherwise returns nothing'''
        for x in self.children:
            if x.selected:
                return x

    def scroll_to_selected(self, *args):
        '''Scrolls view to self.sel_last index'''
        self.parent.scroll_to_index(self.sel_last)

    def update_selected(self, *args):
        '''Calls apply_selection() on newly selected and deselected widgets'''
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
