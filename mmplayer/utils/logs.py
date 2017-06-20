from kivy.logger import Logger
from functools import partial
from kivy.clock import Clock
from kivy.app import App
import traceback

def display_toast(text, level):
    app = App.get_running_app()
    root = app.root_widget
    if level == 'warning':
        root.display_warning(text)
    elif level == 'error':
        root.display_error(text)
    else:
        root.display_info(text)

def not_implemented(feature=None):
    if feature:
        text = '%s not implemented' % (feature)
    else:
        text = 'Not implemented'
    display_toast(text, 'error')
    Logger.error(text)

def error(text, trace=False):
    if trace:
        text = ''.join((text, traceback.format_exc()))
    Clock.schedule_once(lambda dt: display_toast(text, 'error'), 0)
    Logger.error(text)

def warning(text):
    display_toast(text, 'warning')
    Logger.warning(text)

def info(text):
    display_toast(text, 'info')
    Logger.info(text)
