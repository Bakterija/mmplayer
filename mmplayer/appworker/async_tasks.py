def find_playlists(directories, callback):
    task = {'method': 'do_find_playlists', 'args': (directories), 'kwargs': {}}
    return (task, callback)

def load_playlists(path_section_list, callback):
    task = {
        'method': 'do_load_playlists', 'args': (path_section_list),
        'kwargs': {}}
    return (task, callback)
