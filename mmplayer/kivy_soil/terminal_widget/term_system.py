from __future__ import print_function, unicode_literals
from kivy.properties import ListProperty, NumericProperty, ObjectProperty
from kivy.properties import BooleanProperty, DictProperty, StringProperty
from kivy_soil.utils.autocomplete import Autocompleter
from kivy.event import EventDispatcher
from time import time, strftime, gmtime
from kivy_soil.utils import get_unicode
from kivy.logger import Logger
from kivy.clock import Clock
from functools import partial
from kivy.compat import PY2
from . import shared_globals
from kivy.app import App
import traceback
import importlib
import random
import re
import os


class TerminalWidgetSystem(EventDispatcher):
    doc = (
    "TerminalWidgetSystem is a system that is meant to\n"
    "simplify various tasks with evaling and execing python code.\n"
    "It supports:\n"
    " - autocomplete,\n"
    " - dynamic plugin loading\n"
    " - recording and replaying inputs\n\n"
    "It's properties are:\n\n"
    " - data: list property that stores all displayed data with time stamps "
    "and raw text\n"
    " - plugins: dict property that stores name, object ref pairs of loaded "
    "plugins\n"
    " - input_log: list property that stores all input text\n"
    " - input_log_index: numeric property that stores log index of current "
    "input, default way to switch is to press up/down arrow\n"
    " - term_widget: object property of parent TerminalWidget\n"
    " - time_stamp_mode: numeric property, 0 is disabled, (1, 2, 3) "
    "are different time stamps\n"
    " - typed_multilines: list property that stores all typed lines "
    "while self.handling_multiline_input is True, after that it is cleared\n"
    )

    autocompleter = Autocompleter()
    handling_multiline_input = BooleanProperty(False)
    log_path = '%s/input_log.txt' % shared_globals.DIR_CONF
    typed_multilines = ListProperty()
    time_stamp_mode = NumericProperty(0)
    input_log_index = NumericProperty(0)
    term_widget = ObjectProperty()
    plugins = DictProperty()
    input_log = ListProperty()
    write_input_log_to_file = True
    data = ListProperty()
    use_logger = False
    grab_input = None
    exec_locals = {}
    _time0 = time()
    _next_id = 0

    def __init__(self, term_widget,**kwargs):
        self.register_event_type('on_data')
        self.register_event_type('on_data_append')
        self.register_event_type('on_input')
        super(TerminalWidgetSystem, self).__init__(**kwargs)
        self.term_widget = term_widget
        self.id = self._next_id
        self.add_text(
            'TerminalWidgetSystem: id:%s initialised' % self._next_id)
        self._next_id += 1
        Clock.schedule_interval(self.on_every_second, 1)
        self.fbind('time_stamp_mode', self.on_time_stamp_mode_reload_data)

        app = App.get_running_app()
        self.exec_locals = {
            'app': app, 'self': self, 'add_text': self.add_text,
            'term_widget': self.term_widget,
            'hide': self.term_widget.animate_out}
        for x in self.exec_locals:
            self.autocompleter.add_word(x)
        for item in self.plugins:
            self.autocompleter.add_word(item)
        for item in self.properties():
            self.autocompleter.add_word(item)

        shared_globals.set_app_name(app.name)
        self._import_built_in_plugins()
        self._load_input_log()

    def on_data_append(self, *args):
        pass

    def _load_input_log(self):
        _write_true_after = False
        if self.write_input_log_to_file:
            self.write_input_log_to_file = False
            _write_true_after = True
        try:
            if os.path.exists(self.log_path):
                with open(self.log_path, 'r') as f:
                    text = f.read()
                    for x in text.splitlines():
                        self.add_to_input_log(x)
            else:
                with open(self.log_path, 'w') as f:
                    f.write('')
        except:
            Logger.error('TerminalWidgetSystem: %s' % (traceback.format_exc()))
        if _write_true_after:
            self.write_input_log_to_file = True
        for x in self.input_log:
            self.add_autocomplete_words_from_text(x)

    def _import_built_in_plugins(self):
        funcpath = os.path.split(os.path.realpath(__file__))[0] + '/plugins/'
        files = os.listdir(funcpath)
        modules = []
        for x in files:
            if not x[-4:] == '.pyc' and not x[0] == '_':
                dot = x[::-1].find('.')
                if dot == -1:
                    modules.append(x)
                else:
                    modules.append(x[:-dot-1])

        for x in modules:
            func_package = 'kivy_soil.terminal_widget.plugins.'
            func_module = '%s%s' % (func_package, x)
            try:
                new_module = importlib.import_module(func_module)
                new_func = new_module.Plugin()
                new_func.on_import(self)
                self.plugins[new_func.name] = new_func
            except:
                Logger.error(
                    'TerminalWidgetSystem: failed to import %s\n %s' % (
                        func_module, traceback.format_exc()))
        Logger.info('TerminalWidgetSystem: imported %s plugins' % (
            len(modules)))

    def on_input(self, *args):
        pass

    def on_data(self, *args):
        pass

    def on_time_stamp_mode_reload_data(self, _, tsmode):
        if tsmode == 1:
            uinfo = "%H:%M:%S"
        elif tsmode == 2:
            uinfo = "%M:%S"
        elif tsmode == 3:
            uinfo = "[%S]"
        for x in self.data:
            x['text'] = self.format_text(x['text_raw'], x['time'], x['level'])
        self.dispatch('on_data', self.data)
        if tsmode in (1, 2, 3):
            self.add_text('TerminalWidgetSystem: tsmode %s: %s' % (
                tsmode, uinfo))
        else:
            self.add_text(
                'TerminalWidgetSystem: tsmode %s: disabled time stamps' % (
                    tsmode))

    def on_every_second(self, *a):
        pass

    def add_text(self, text, text_time=None, level=None,
                 add_autocomplete=True):
        text = str(text)
        if PY2:
            text = get_unicode(text)
        if add_autocomplete:
            self.add_autocomplete_words_from_text(text)
        if not text_time:
            text_time = round(time() - self._time0, 2)
        form_first = self.first_time_text_format(text, text_time, level)
        text_formatted = self.format_text(form_first, text_time, level)
        new = {
            'time': text_time, 'text_raw': form_first, 'text': text_formatted,
            'level': level}
        self.data.append(new)
        self.dispatch('on_data_append', new)

    def add_autocomplete_words_from_text(self, text):
        self.autocompleter.add_words_from_text(text)

    def first_time_text_format(self, text, time, level):
        if level:
            b = text.find(':')
            if b != -1:
                plusspace = ''
                if b < 12:
                    plusspace = ' ' * (12 - b)
                text = '[%s%s]%s' % (text[:b], plusspace, text[b+1:])
        return text

    def format_text(self, text, time, level):
        if level:
            text = '[{:<8}] {}'.format(level.upper(), text)
        tsmode = self.time_stamp_mode
        if tsmode == 1:
            time_formatted = strftime("%H:%M:%S", gmtime(time))
            ret =  '[%s] %s' % (time_formatted, text)
        elif tsmode == 2:
            time_formatted = strftime("%M:%S", gmtime(time))
            ret = '[%s] %s' % (time_formatted, text)
        elif tsmode == 3:
            time = round(time, ndigits=1)
            time_formatted = str(time).zfill(5)
            ret =  '[%s] %s' % (time_formatted, text)
        else:
            ret = text
        return ret

    def try_autocomplete(self, text, cursor_index):
        ret = ''
        try:
            for key in self.exec_locals:
                self.autocompleter.add_word(key)
            found, ret = self.autocompleter.autocomplete(text, cursor_index)
            if len(found) > 1:
                self.add_text(str(found))
        except:
            if self.use_logger:
                Logger.error('TerminalWidgetSystem: \n%s' % (
                    traceback.format_exc()))
            self.add_text('TerminalWidgetSystem: \n%s' % (
                    traceback.format_exc()),level='exception')
        return ret

    def get_log_previous(self, *a):
        ret = ''
        if self.input_log:
            if self.input_log_index != 0:
                self.input_log_index -= 1
            ret = self.input_log[self.input_log_index]
        return ret

    def get_log_next(self, *a):
        ret = ''
        if self.input_log:
            len_input_log = len(self.input_log)
            new_index = self.input_log_index
            if len(self.input_log) - 1 > self.input_log_index:
                new_index = self.input_log_index + 1
            if new_index > len_input_log - 1:
                new_index = len_input_log - 1
            self.input_log_index = new_index
            ret = self.input_log[self.input_log_index]
        return ret

    def get_globals(self):
        return globals()

    def handle_input(self, text, add_to_input_log=True):
        try:
            self.dispatch('on_input', text)
            text = text.rstrip()
            if self.grab_input:
                self.grab_input.handle_input(
                    self, globals(), self.exec_locals, text)
                return
            self.exec_locals['__ret_value__'] = {}
            if self.handling_multiline_input or text and text[-1] == ':':
                self.handle_input_multiline(text)
            else:
                if not text:
                    self.add_text('\n')
                    return
                if text:
                    if text[0] == '.':
                        func_name = text.split(' ')[0]
                        func = self.plugins.get(func_name[1:], None)
                        if func:
                            ret = func.handle_input(
                                self, globals(), self.exec_locals, text)
                            self.exec_locals['__ret_value__'] = ret
                        else:
                            self.add_text('# Did not find plugin: "%s"' % (
                                func_name))
                            self.add_text('# Available plugins are: %s' % (
                                [x for x in self.plugins]))

                    else:
                        try:
                            exec('__ret_value__ = %s' % (
                                text), globals(), self.exec_locals)
                        except SyntaxError:
                            exec(text, globals(), self.exec_locals)
                    self.handle_return(self.exec_locals)
        except Exception as e:
            if self.use_logger:
                Logger.error('TerminalWidgetSystem: %s\n%s' % (
                    e, traceback.format_exc()))
            self.add_text('TerminalWidgetSystem: %s\n%s' % (
                    e, traceback.format_exc()),level='exception')
        if not self.typed_multilines and add_to_input_log:
            self.add_to_input_log(text)

    def add_to_input_log(self, text):
        len_input_log = len(self.input_log)
        can_append = True
        try:
            self.input_log.remove(text)
        except:
            pass

        if can_append:
            self.input_log.append(text)
            if self.write_input_log_to_file:
                try:
                    if PY2 and isinstance(text, unicode):
                        text = text.encode('utf-8')
                    with open(self.log_path, 'a') as f:
                        f.write(text + '\n')
                except:
                    Logger.error('TerminalWidgetSystem: %s' % (
                        traceback.format_exc()))
        self.input_log_index = len(self.input_log)

    def clear_input_log(self, *args):
        self.input_log = []
        log_path = '%s/input_log.txt' % shared_globals.DIR_CONF
        try:
            with open(self.log_path, 'w') as f:
                f.write('')
        except:
            Logger.error('TerminalWidgetSystem: %s' % (
                traceback.format_exc()))
        self.input_log_index = 0

    def handle_input_multiline(self, text):
        if text:
            if not self.handling_multiline_input:
                self.handling_multiline_input = True
            self.typed_multilines.append(text)
            self.add_to_input_log(text)
            self.add_text(text)
        else:
            self.handling_multiline_input = False
            if len(self.typed_multilines) > 1:
                joined_multilines = '\n'.join(self.typed_multilines)
                self.handle_input(joined_multilines)
                self.typed_multilines = []
            else:
                self.typed_multilines = []

    def handle_return(self, new_locals):
        ret = new_locals.get('__ret_value__', None)
        if ret:
            self.add_text(ret)

    def on_handling_multiline_input(self, _, value):
        if value:
            text = '# Multi line input start'
        else:
            text = '# Multi line input stop'
        self.add_text(text)

    def keyboard_interrupt(self):
        if self.handling_multiline_input:
            self.handling_multiline_input = False
            self.typed_multilines = []
        self.add_text('# KeyboardInterrupt')
