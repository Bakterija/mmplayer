from kivy.core.window import Window
from kivy.logger import Logger

keybinds = {}
ctrl_held = False
alt_held = False
shift_held = False
log_keys = False
active = True
disabled_categories = set()
ignore_warnings = False

def start():
    global active
    active = True

def stop():
    global active
    active = False

def start_categories(categories):
    global disabled_categories
    if type(categories) == str:
        categories = [categories]
    for x in categories:
        if x in disabled_categories:
            disabled_categories.remove(x)

def stop_categories(categories):
    global disabled_categories
    if type(categories) == str:
        categories = [categories]
    for x in categories:
        disabled_categories.add(x)

def add(name, key, state, callback, modifier=None, category='n/a'):
    if name in keybinds:
        log_warning('key_binder: key {} in {} was added to keybinds before,'
                    'replacing with {}'.format(
                        name, keybinds[name], make_kb_dict(
                            name, key, state, callback,
                            modifier=modifier, category=category)))
    keybinds[name] = make_kb_dict(
        name, key, state, callback, modifier=modifier, category=category)

def make_kb_dict(name, key, state, callback, modifier=None, category=''):
    return {
        'callback': callback,
        'key': int(key),
        'state': state,
        'modifier': modifier,
        'category': category,
        }

def remove(name):
    try:
        del keybinds[name]
    except KeyError as e:
        Logger.error('key_binder: key "%s" is not in keybinds' % (name))
        raise e

def on_key_down(win, key, *args):
    global ctrl_held, alt_held, shift_held
    if not active:
        return

    try:
        modifier = args[2]
    except:
        modifier = []

    if key in (308, 1073741824):
        alt_held = True
    elif key in (305, 306):
        ctrl_held = True
    elif key in (304, 303):
        shift_held = True

    if log_keys:
        Logger.info('KeyBinder: on_key_down: {} - {}'.format(key, modifier))

    for k, v in keybinds.items():
        if v['category'] in disabled_categories:
            continue
        if v['key'] == key:
            if v['state'] in ('down', 'any', 'all'):
                if not v['modifier'] or v['modifier'] == modifier:
                    v['callback']()

def on_key_up(win, key, *args):
    global ctrl_held, alt_held, shift_held
    if not active:
        return

    if log_keys:
        Logger.info('KeyBinder: on_key___up: {} - {}'.format(key, args))

    if key in (308, 1073741824):
        alt_held = False
    elif key in (305, 306):
        ctrl_held = False
    elif key in (304, 303):
        shift_held = False

    for k, v in keybinds.items():
        if v['category'] in disabled_categories:
            continue
        if v['key'] == key:
            if v['state'] in ('up', 'any', 'all'):
                v['callback']()

def log_warning(text):
    if not ignore_warnings:
        Logger.warning(text)


Window.bind(on_key_down=on_key_down)
Window.bind(on_key_up=on_key_up)
Logger.info('key_binder: initialised')
