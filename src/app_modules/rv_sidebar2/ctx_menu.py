from kivymd_modified.menu import MDDropdownMenu, MDMenuItem

def open_sidebar_ctx_menu(widget):
    ci = [
        {
            'text': 'Remove playlist', 'disabled': False}
        ]

    for i, x in enumerate(ci):
        x['viewclass'] = 'MDMenuItem'
        x['index'] = i

    drop = MDDropdownMenu(items=ci, width_mult=7)
    drop.open(widget)
