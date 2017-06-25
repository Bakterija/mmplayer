from kivy.properties import ListProperty
from kivy.event import EventDispatcher
from kivy.logger import Logger
from time import time

class LoggerHistoryProper(EventDispatcher):
    data = ListProperty()

    def __init__(self, **kwargs):
        self.register_event_type('on_add_data')
        super(self.__class__, self).__init__(**kwargs)

    def on_add_data(self, data):
        pass

    def add_data(self, text, level):
        new = {'time': time(), 'level': level, 'text': text}
        self.data.append(new)
        self.dispatch('on_add_data', new)

LoggerHistoryProper = LoggerHistoryProper()

def exception(msg, *args):
    Logger._exception(msg)
    LoggerHistoryProper.add_data(msg, 'exception')

def warning(msg, *args):
    Logger._warning(msg)
    LoggerHistoryProper.add_data(msg, 'warning')

def error(msg, *args):
    Logger._error(msg)
    LoggerHistoryProper.add_data(msg, 'error')

def info(msg, *args):
    Logger._info(msg)
    LoggerHistoryProper.add_data(msg, 'info')

Logger._exception = Logger.exception
Logger.exception = exception
Logger._warning = Logger.warning
Logger.warning = warning
Logger._error = Logger.error
Logger.error = error
Logger._info = Logger.info
Logger.info = info

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

def not_implemented(feature=None, toast=True):
    if feature:
        text = '%s not implemented' % (feature)
    else:
        text = 'Not implemented'
    display_toast(text, 'error')
    if toast:
        Logger.error(text)

def error(text, trace=False, toast=True):
    if trace:
        text = ''.join((text, traceback.format_exc()))
    if toast:
        Clock.schedule_once(lambda dt: display_toast(text, 'error'), 0)
    Logger.error(text)

def warning(text, toast=True):
    if toast:
        display_toast(text, 'warning')
    Logger.warning(text)

def info(text, toast=True):
    if toast:
        display_toast(text, 'info')
    Logger.info(text)
