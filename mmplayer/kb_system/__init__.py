'''A system that combines global bindable hotkeys with a widget focus behavior
Manages kivy Window key_up, key_down events and calls methods, callbacks
wehre necessary'''

from . import focus as focus_behavior
from kivy.core.window import Window
from kivy.logger import Logger
from time import time
from . import keys
import traceback

keybinds = {}
'''Storage for all global hotkeys and callbacks'''
held_ctrl = False
held_alt = False
held_shift = False
log_keys = False
'''Key events will be logged when True, default is False'''

active = True
'''Key events will be managed when True, default is True'''

disabled_categories = set()
'''Storage set for disabled global hotkey categories'''

ignore_warnings = False
last_key = ''
last_modifier = []
last_time = time()

def start():
    '''Start managing key events'''
    global active
    active = True

def stop():
    '''Stop managing key events'''
    global active
    active = False

def start_categories(categories):
    '''Start managing key events for global hotkey categories'''
    global disabled_categories
    if type(categories) == str:
        categories = [categories]
    for x in categories:
        if x in disabled_categories:
            disabled_categories.remove(x)

def stop_categories(categories):
    '''Stop managing key events for global hotkey categories'''
    global disabled_categories
    if type(categories) == str:
        categories = [categories]
    for x in categories:
        disabled_categories.add(x)

def add(name, key, state, callback, modifier=None, category='n/a'):
    '''Add a global hotkey'''
    if name in keybinds:
        log_warning('key_binder: key {} in {} was added to keybinds before,'
                    'replacing with {}'.format(
                        name, keybinds[name], _make_kb_dict(
                            name, key, state, callback,
                            modifier=modifier, category=category)))
    keybinds[name] = _make_kb_dict(
        name, key, state, callback, modifier=modifier, category=category)

def _make_kb_dict(name, key, state, callback, modifier=None, category=''):
    return {
        'callback': callback,
        'key': int(key),
        'state': state,
        'modifier': modifier,
        'category': category,
        }

def remove(name):
    '''Remove a global hotkey'''
    try:
        del keybinds[name]
    except KeyError as e:
        Logger.error('key_binder: key "%s" is not in keybinds' % (name))
        raise e

def on_key_down(win, key, *args):
    '''Detects pressed keys, modifiers and calls on_key_event'''
    global last_key, last_modifier, last_time
    modifier = _update_modifier(key, True)
    time_now = time()
    if last_time + 0.02 > time_now:
        if key == last_key and modifier == last_modifier:
            return

    last_key = key
    last_modifier = modifier
    last_time = time_now

    on_key_event(key, modifier, True)

def on_key_up(win, key, *args):
    '''Detects released keys, modifiers and calls on_key_event'''
    modifier = _update_modifier(key, False)
    on_key_event(key, modifier, False)

def on_key_event(key, modifier, is_down):
    '''Logs keys(if log_keys is True),
    updates global modifiers,
    does global hotkey callbacks, calls focused widget
    on_key_down or on_key_up method when there is a focused widget
    and key is not used by global callback already or key is grabbed by widget
    '''
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
        try:
            if is_down:
                retval = cf.on_key_down(key, modifier)
            else:
                retval = cf.on_key_up(key, modifier)
            return retval
        except:
            e = traceback.format_exc()
            Logger.error('kb_system: dispatch_to_focused: %s' % (e))

def _update_modifier(key, is_down):
    '''Saves modifier hold state to module globals
    (held_alt, held_ctrl, held_shift).
    Returns list with modifier strings for on_key_event'''
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
