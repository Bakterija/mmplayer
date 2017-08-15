'''A system that combines global bindable hotkeys with a widget focus behavior
Manages kivy Window key_up, key_down events and calls methods, callbacks
where necessary'''

from . import focus as focus_behavior
from kivy.core.window import Window
from kivy.core.window import Keyboard
from kivy.logger import Logger
from kivy.clock import Clock
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

waiting_press = False
waiting_release = False
'''All hotkeys can have a waiting time which will temporarily freeze all input
events'''

disabled_categories = set()
'''Storage set for disabled global hotkey categories'''

ignore_warnings = False
last_key = ''
last_modifier = []
last_time = time()
time_alt_press = {}

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

def add(name, key, state, callback, modifier=None, wait=0, category='n/a'):
    '''Add a global hotkey'''
    if name in keybinds:
        log_warning('key_binder: key {} in {} was added to keybinds before,'
                    'replacing with {}'.format(
                        name, keybinds[name], _make_kb_dict(
                            name, key, state, callback,
                            modifier=modifier, wait=wait,
                            category=category))
                    )
    keybinds[name] = _make_kb_dict(
        name, key, state, callback, modifier=modifier,
        wait=wait, category=category)

def _make_kb_dict(name, key, state, callback, modifier=None, wait=0,
                  category=''):
    return {
        'callback': callback,
        'key': int(key),
        'state': state,
        'modifier': modifier,
        'wait': wait,
        'category': category,
        }

def remove(name):
    '''Remove a global hotkey'''
    try:
        del keybinds[name]
    except KeyError as e:
        Logger.error('key_binder: key "%s" is not in keybinds' % (name))
        raise e

def on_key_down(window, key, scan, text, modifier):
    '''Detects pressed keys, modifiers and calls on_key_event'''
    global last_key, last_modifier, last_time, time_alt_press, waiting_press
    global log_keys
    modifier = _update_modifier(key, True)
    if waiting_press:
        if log_keys:
            Logger.info('kb_dispatcher: on_key_down: waiting')
    else:
        time_now = time()
        if last_time + 0.02 > time_now:
            if key == last_key and modifier == last_modifier:
                return

        if 'alt' in modifier:
            keytime = time_alt_press.get(key, 0)
            if keytime:
                if keytime > time_now - 0.3:
                    return
            time_alt_press[key] = time_now

        last_key = key
        last_modifier = modifier
        last_time = time_now

        on_key_event(key, modifier, True, text=text)

def on_key_up(window, key, *args):
    '''Detects released keys, modifiers and calls on_key_event'''
    global waiting_release, log_keys
    modifier = _update_modifier(key, False)
    if waiting_release:
        if log_keys:
            Logger.info('kb_dispatcher: on_key_down: waiting')
    else:
        on_key_event(key, modifier, False)

def on_key_event(key, modifier, is_down, text=None):
    '''Logs keys(if log_keys is True),
    updates global modifiers,
    does global hotkey callbacks, calls focused widget
    on_key_down or on_key_up method when there is a focused widget
    and key is not used by global callback already or key is grabbed by widget
    '''
    global held_ctrl, held_alt, held_shift, waiting_press, waiting_release
    global log_keys, ignored_keys
    if not active:
        return

    if is_down:
        kstate = 'down'
    else:
        kstate = 'up'

    if log_keys:
        Logger.info('kb_dispatcher: on_key_{}: {} - {}'.format(
            kstate, key, modifier))

    disp_global = True
    cur_focus = focus_behavior.current_focus
    if text and cur_focus and cur_focus.receive_textinput:
        return
    if cur_focus and key in cur_focus.grab_keys:
        disp_global = dispatch_to_focused(key, modifier, is_down)
    if disp_global:
        found = False
        for k, v in keybinds.items():
            if v['category'] in disabled_categories:
                continue
            if v['key'] == key:
                if v['state'] in (kstate, 'any', 'all'):
                    if modifier and v['modifier']:
                        found = True
                        for mod in v['modifier']:
                            if mod not in modifier:
                                found = False
                        if found:
                            v['callback']()
                    else:
                        if v['modifier'] == ['none'] or not v['modifier']:
                            v['callback']()
                            found = True
                if v['wait']:
                    if is_down and not waiting_press:
                        waiting_press = True
                        Clock.schedule_once(remove_wait_press, v['wait'])
                    elif not is_down and not waiting_release:
                        waiting_release = True
                        Clock.schedule_once(remove_wait_release, v['wait'])
        if not found:
            dispatch_to_focused(key, modifier, is_down)

def remove_wait_press(*args):
    global waiting_press
    waiting_press = False

def remove_wait_release(*args):
    global waiting_release
    waiting_release = False

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

def on_textinput(window, text):
    global log_keys
    if log_keys:
        Logger.info('kb_dispatcher: on_textinput: %s' % (text))
    cf = focus_behavior.current_focus
    if cf:
        try:
            retval = cf.dispatch('on_focus_textinput', text)
        except:
            e = traceback.format_exc()
            Logger.error('kb_system: on_textinput: %s' % (e))

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
Window.bind(on_textinput=on_textinput)
