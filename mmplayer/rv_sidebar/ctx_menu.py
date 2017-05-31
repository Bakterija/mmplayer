from kivymd_modified.menu import MDDropdownMenu, MDMenuItem
from kivy.app import App

def open_sidebar_ctx_menu(widget):
    root = App.get_running_app().root

    if widget.sub_viewclass == 'SideBarPlaylistButton':
        pl_remove_path = widget.path
    else:
        pl_remove_path = ''

    ci = [
        {'text': 'Add playlist', 'disabled': False,
         'on_press': root.mgui_add_playlist},
        {'text': 'Remove playlist',
         'disabled': False if pl_remove_path else True,
         'on_press': lambda *a: root.mgui_remove_playlist(pl_remove_path)}
        ]

    for i, x in enumerate(ci):
        x['viewclass'] = 'MDMenuItem'
        x['index'] = i

    drop = MDDropdownMenu(items=ci, width_mult=7)
    drop.open(widget)
