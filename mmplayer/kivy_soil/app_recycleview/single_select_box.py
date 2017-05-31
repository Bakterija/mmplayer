from .recyclebox import AppRecycleBoxLayout


class SingleSelectRecycleBox(AppRecycleBoxLayout):
    def on_arrow_up(self):
        '''Modified AppRecycleBoxLayout single select method'''
        data = self.parent.data
        for i in reversed(range(self.sel_last)):
            if self.parent.data[i]['selectable']:
                self.update_selected_widgets_and_scroll(i)
                break
        self.update_selected()
        self.scroll_to_selected()

    def on_arrow_down(self):
        '''Modified AppRecycleBoxLayout single select method'''
        data = self.parent.data
        len_data = len(data)
        for i in range(self.sel_last + 1, len_data):
            if data[i]['selectable']:
                self.update_selected_widgets_and_scroll(i)
                break

    def update_selected_widgets_and_scroll(self, new_selected):
        self.sel_last, self.sel_first = new_selected, new_selected
        self.selected_widgets = {new_selected}
        self.update_selected()
        self.scroll_to_selected()
