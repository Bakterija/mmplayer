from utils.not_implemented import show_error as show_not_implemented
from kivymd_modified.menu import MDDropdownMenu
from random import randrange
from kivy.logger import Logger

# def get_ctx_items(self):
#     selected = self.rv.get_selected_data()
#     count_selected = len(selected)
#     jump_index = self.rv.find_playing()
#     if jump_index != -1:
#         can_jump = False
#     else:
#         can_jump = True
#     if count_selected:
#         cant_remove = False
#     else:
#         cant_remove = True
#
#     ci = [
#         {
#             'text': 'Play', 'disabled': False,
#             'on_press': self.start_media},
#         {
#             'text': 'Remove from playlist', 'disabled': cant_remove,
#             'on_press': self.rv.remove_selected},
#         {
#             'text': 'Clear queue', 'disabled': False,
#             'on_press': self.rv.mcontrol.clear_queue},
#         {
#             'text': 'Jump to current played', 'disabled': can_jump,
#             'on_press': lambda *a: self.rv.scroll_to_index(jump_index)},

def open_menu(self, widget, index, pos):
    is_queue, is_playlist = False, False
    if self.queue_view:
        is_queue = True
    else:
        is_playlist = True

    len_data = len(self.data)
    random_jump = randrange(0, len_data, 1)

    selected_media = False
    selected = self.get_selected_data()
    if selected:
        selected_media = True

    selected_rv = False
    if index is None:
        selected_rv = True

    jump_index = self.find_playing()
    if jump_index == -1:
        can_jump = False
    else:
        can_jump = True

    can_remove = False
    if is_playlist:
        if self.playlist_instance:
            can_remove = self.playlist_instance.can_remove
            if selected_rv:
                can_remove  = False
    else:
        can_remove = True

    all_items = [
        (True, 'Play', selected_rv, getattr(widget, 'start_media', None)),
        (is_playlist, 'Play selection', not selected_media,
         lambda *a: self.mcontrol.start_selection(selected)),
        (is_playlist, 'Add to queue', not selected_media,
         getattr(self, 'add_selected_to_queue', None)),
        (True, 'Remove selected',
         all((not can_remove, not selected_media)), self.remove_selected),
        (True, 'Jump to index ..', False, show_not_implemented),
        (True, 'Jump to random', False,
         lambda *a: self.scroll_to_index(random_jump)),
        (True, 'Jump to current played', not can_jump,
         lambda *a: self.scroll_to_index(jump_index)),
        (True, 'Select all', False, self.ids.box.select_all),
        (True, 'Deselect all', False, self.ids.box.deselect_all),
        (True, 'Properties', selected_rv,
         getattr(widget, 'open_prop_dialog', None)),
    ]
    items = []
    for i, (condition, text, disabled, func) in enumerate(all_items):
        if condition:
            items.append({
                'index': i, 'text': text, 'disabled': disabled,
                'on_press': func, 'viewclass': 'MDMenuItem'})

    drop = MDDropdownMenu(
        items=items, width_mult=7)

    if selected_rv:
        drop.open(self)
    else:
        drop.open(widget)
