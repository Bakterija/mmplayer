from utils.logs import not_implemented as show_not_implemented
from kivymd_modified.menu import MDDropdownMenu
from kivy.logger import Logger
from random import randrange


def open_menu(self, widget, index, pos):
    '''Builds a media list view context menu for queue or playlist,
    then opens and returns it'''
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

    # All available button values
    # with callbacks, names, values adding, disabling buttons after init
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
         getattr(widget, 'open_properties_dialog', None)),
    ]
    # Parses all_items and adds button data for items where item[0] is True,
    # sets disabled value, because some functions will not work
    # or are not available at specific times
    items = []
    for i, (condition, text, disabled, func) in enumerate(all_items):
        if condition:
            items.append({
                'index': i, 'text': text, 'disabled': disabled,
                'on_press': func, 'viewclass': 'MDMenuItem'})

    drop = MDDropdownMenu(
        items=items, width_mult=7)

    # If no viewclass instance is selected, puts it on the recycleview,
    # otherwise context menu appears on selected viewclass instance
    if selected_rv:
        drop.open(self)
    else:
        drop.open(widget)
    return drop
