from kivy.core.window import Window
from kivy.logger import Logger
from time import time
from . import focus as focus_behavior
from . import keys

keybinds = {}
held_ctrl = False
held_alt = False
held_shift = False
log_keys = False
active = True
disabled_categories = set()
ignore_warnings = False
last_key = ''
last_modifier = []
last_time = time()

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
    global last_key, last_modifier, last_time
    modifier = update_modifier(key, True)
    time_now = time()
    if last_time + 0.02 > time_now:
        if key == last_key and modifier == last_modifier:
            return

    last_key = key
    last_modifier = modifier
    last_time = time_now

    on_key_event(key, modifier, True)

def on_key_up(win, key, *args):
    modifier = update_modifier(key, False)
    on_key_event(key, modifier, False)

def on_key_event(key, modifier, is_down):
    global held_ctrl, held_alt, held_shift
    if not active:
        return
    if is_down:
        kstate = 'down'
    else:
        kstate = 'up'

    if log_keys:
        Logger.info('kb_dispatcher: on_key_{}: {} - {}'.format(
            kstate, key, modifier))

    dispatch_global = True
    cur_focus = focus_behavior.current_focus
    if cur_focus and key in cur_focus.grab_keys:
        dispatch_global = dispatch_to_focused(key, modifier, is_down)
    if dispatch_global:
        found = False
        for k, v in keybinds.items():
            if v['category'] in disabled_categories:
                continue
            if v['key'] == key:
                if v['state'] in (kstate, 'any', 'all'):
                    if not v['modifier'] or v['modifier'] == modifier:
                        v['callback']()
                        found = True
        if not found:
            dispatch_to_focused(key, modifier, is_down)

def dispatch_to_focused(key, modifier, is_down):
    cf = focus_behavior.current_focus
    retval = None
    if cf:
        if is_down:
            retval = cf.on_key_down(key, modifier)
        else:
            retval = cf.on_key_up(key, modifier)
        return retval

def update_modifier(key, is_down):
    global held_alt, held_ctrl, held_shift
    if key in (keys.ALT_L, keys.ALT_R):
        held_alt = is_down
    elif key in (keys.CTRL_L, keys.CTRL_R):
        held_ctrl = is_down
    elif key in (keys.SHIFT_L, keys.SHIFT_R):
        held_shift = is_down
    modifier = []
    if held_alt:
        modifier.append('alt')
    if held_ctrl:
        modifier.append('ctrl')
    if held_shift:
        modifier.append('shift')
    return modifier

def log_warning(text):
    if not ignore_warnings:
        Logger.warning(text)


Window.bind(on_key_down=on_key_down)
Window.bind(on_key_up=on_key_up)
