from __future__ import print_function
from kivy.properties import ListProperty, NumericProperty, ObjectProperty
from kivy.properties import BooleanProperty
from kivy.event import EventDispatcher
from time import time, strftime, gmtime
from kivy.logger import Logger
from kivy.clock import Clock
from functools import partial
from . import shared_globals
from kivy.app import App
import traceback
import importlib
import random
import re
import os


class TerminalWidgetSystem(EventDispatcher):
    autocomplete_words = {'self', 'app', 'term_widget'}
    handling_multiline_input = BooleanProperty(False)
    typed_multilines = ListProperty()
    time_stamp_mode = NumericProperty(0)
    input_log_index = NumericProperty(0)
    app_name = ''
    term_widget = ObjectProperty()
    _empty_try_autocompletes = 0
    input_log = ListProperty()
    data = ListProperty()
    use_logger = False
    exec_locals = {}
    _time0 = time()
    _next_id = 0

    def __init__(self, term_widget,**kwargs):
        self.register_event_type('on_data')
        super(TerminalWidgetSystem, self).__init__(**kwargs)
        self.term_widget = term_widget
        self.id = self._next_id
        self.add_text(
            'TerminalWidgetSystem: id:%s initialised' % self._next_id)
        self._next_id += 1
        Clock.schedule_interval(self.on_every_second, 1)
        self.fbind('time_stamp_mode', self.on_time_stamp_mode_reload_data)
        self.functions = {
            # 'autocomplete_words': self.get_autocomplete_words,
            # 'functions': self.get_functions,
            # 'properties': self.properties,
            # 'setprop': self.set_property,
            # 'printer': self.printer,
            # 'clear': lambda: setattr(self, 'data', []),
            # 'record': self.record_input_start,
            # 'record_list': self.record_list_app,
            # 'record_delete': self.record_delete,
            # 'record_exec': self.record_exec,
            # 'record_print': self.record_print,
            # 'save': self.record_input_save
        }
        for item in self.functions:
            self.autocomplete_words.add(item)
        for item in self.properties():
            self.autocomplete_words.add(item)
        app = App.get_running_app()
        self.exec_locals = {'app': app, 'self': self}
        shared_globals.set_app_name(app.name)
        self._import_built_in_functions()

    def _import_built_in_functions(self):
        funcpath = os.path.split(os.path.realpath(__file__))[0] + '/functions/'
        files = os.listdir(funcpath)
        del_list = reversed([i for i, x in enumerate(files) if x[0] == '_'])
        for i in del_list:
            del files[i]

        for x in files:
            x = x[:-3]
            func_package = 'kivy_soil.terminal_widget.functions.'
            new_module = importlib.import_module('%s%s' % (func_package, x))
            new_func = new_module.Function
            self.functions[new_func.name] = new_func
            Logger.info('TerminalWidgetSystem: imported function "%s"' % (
                new_func.name))

    def record_exec(self, file_name):
        fpath = '%s/%s' % (DIR_APP, file_name)
        if os.path.exists(fpath):
            with open(fpath, 'r') as fp:
                text = fp.read()
                self.handle_input(text)
        else:
            self.add_text('# %s does not exist' % fpath)

    def record_list_app(self, *args):
        files = os.listdir(DIR_APP)
        if files:
            adt = '# Recorded files in %s\n%s' % (DIR_APP, files)
        else:
            adt = '# No files recorded'
        self.add_text(adt)

    def record_print(self, file_name):
        fpath = '%s/%s' % (DIR_APP, file_name)
        if os.path.exists(fpath):
            with open(fpath, 'r') as fp:
                text = fp.read().splitlines()
                self.add_text(text)
        else:
            self.add_text('# %s does not exist' % fpath)

    def record_delete(self, file_name):
        fpath = '%s/%s' % (DIR_APP, file_name)
        if os.path.exists(fpath):
            os.remove(fpath)
            self.add_text('# Deleted %s' % (fpath))
        else:
            self.add_text('# %s does not exist' % fpath)

    def record_input_start(self, file_name):
        fpath = '%s/%s' % (DIR_APP, file_name)
        if os.path.exists(fpath):
            self.add_text('# %s already exists' % fpath)
        else:
            self.add_text(
                '# Recording input for %s, type "save" to save' % (file_name))
            self._record_starts_at = self.input_log_index + 1
            self._record_file_name = file_name

    def record_input_save(self, *args):
        addt = ''
        if not hasattr(self, '_record_starts_at'):
            addt = '# Nothing to save'
        elif self._record_starts_at == -1:
            addt = '# Nothing to save'
        else:
            fpath = '%s/%s' % (DIR_APP, self._record_file_name)
            try:
                with open(fpath, 'w') as fp:
                    fp.write('')
                    lines = self.input_log[self._record_starts_at+1:]
                    len_lines = len(lines)
                    joined_text = lines[0]
                    for line in lines[1:]:
                        joined_text = '%s\n%s' % (joined_text, line)
                    fp.write(joined_text)
                addt = '# Saved recorded in %s' % (fpath)
            except Exception as e:
                self.add_text(str(e), level='exception')
        self._record_starts_at = -1
        if addt:
            self.add_text(addt)

    def printer(self, *args):
        new_args = []
        for x in args:
            gget = None
            lget = self.exec_locals.get(x, None)
            if lget:
                new_args.append(str(lget))
            if not lget:
                gget = globals().get(x, None)
                if gget:
                    new_args.append(str(gget))
            if not lget and not gget:
                exec('__ret_value__ = %s' % (x), globals(), self.exec_locals)
                if self.exec_locals['__ret_value__']:
                    new_args.append(str(self.exec_locals['__ret_value__']))
                else:
                    raise NameError('name %s is not defined' % (x))
        exec_text = '%s(%s)' % ('self.add_text', new_args)
        try:
            exec(exec_text, globals(), self.exec_locals)
        except:
            traceback.print_exc()

    def get_autocomplete_words(self):
        auto = list(self.autocomplete_words)
        return auto

    def get_functions(self):
        return self.functions

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

    def set_property(self, property, value):
        exec('self.%s = %s' % (property, value))

    def on_every_second(self, *a):
        pass

    def add_text(self,text, text_time=None, level=None,
                 add_autocomplete=True):
        text = str(text)
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

    def add_autocomplete_words_from_text(self, text):
        text2 = text
        for x in (' ', '!', '@', '$', '#', '%', '^', '&', '*', '(', ')',
                  '-', '=', '+', '{', '}', '[', ']', '\\', '|', '?',
                  ';', ':', '<', '>', ',', '.', '/', '1', '2', '3', '4', '5',
                  '6', '7', '8', '9', '`', '~'):
            text2 = text2.replace(x, '0')
        text2 = text2.replace("'", '0')
        text2 = text2.replace('"', '0')
        text2 = text2.replace('"', '0')
        words = text2.split('0')
        for word in words:
            word = word.strip()
            if word:
                word = word.lower()
                if word not in self.autocomplete_words:
                    self.autocomplete_words.add(word)

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

    def reset_empty_autocompletes(self, *args):
        self._empty_try_autocompletes = 0

    def try_autocomplete(self, text, cursor_index):
        if not text:
            self._empty_try_autocompletes += 1
            if self._empty_try_autocompletes > 1:
                self.add_text(self.get_autocomplete_words())
            Clock.unschedule(self.reset_empty_autocompletes)
            Clock.schedule_once(self.reset_empty_autocompletes, 0.5)
            return ''
        insert_text = ''
        start = -1
        end = cursor_index
        try:
            len_text = len(text)
            rev_text = text[::-1]
            # If cursor is at end, looks for a space character
            # before it, then sets word start slice number
            if len_text == cursor_index:
                start = rev_text.find(' ')
                if start == -1:
                    start = 0
                else:
                    start = len_text - start
            else:
                # If cursor is at end of a word, looks for a space character
                # before it, then sets start slice number
                if text[cursor_index] == ' ' and text[cursor_index-1] != ' ':
                    end = cursor_index
                    start = rev_text[len_text-end:].find(' ')
                    if start == -1:
                        start = 0
                    else:
                        start = end - start
            # Skips if no word found
            if start != -1:
                word = text[start:cursor_index]
                found = []
                # Does nothing when word is empty
                if word:
                    len_word = len(word)
                    # Looks for matching strings in autocomplete_words
                    # Appends all results to found list
                    for x in self.autocomplete_words:
                        if x[:len(word)].lower() == word.lower():
                            found.append(x)

                len_found = len(found)
                # If only one result found, new characters for inserting
                if len_found:
                    if len_found == 1:
                        insert_text = found[0][len_word:]
                        if len_text == cursor_index:
                            insert_text = insert_text + ' '
                    else:
                        # If multiple words found, looks for and adds
                        # matching characters untill word_min_len index
                        # is reached, then stops and returns character string
                        # for inserting
                        found_lens = [len(x) for x in found]
                        word_min_len = min(found_lens)
                        len_word = len(word)
                        match_index = len_word
                        for char in found[0][match_index:]:
                            are_matching = True
                            for x in found[1:]:
                                if x[match_index].lower() != char.lower():
                                    are_matching = False
                                    break
                            match_index += 1
                            if are_matching:
                                insert_text += char
                            else:
                                break
                            if word_min_len - 1 < match_index:
                                break
                        self.add_text(found)
        except Exception as e:
            if self.use_logger:
                Logger.error('TerminalWidgetSystem: %s\n%s' % (
                    e, traceback.format_exc()))
            self.add_text('TerminalWidgetSystem: %s\n%s' % (
                    e, traceback.format_exc()),level='exception')
        return insert_text

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
            if len(self.input_log) - 1 > self.input_log_index:
                self.input_log_index += 1
            ret = self.input_log[self.input_log_index]
        return ret

    def handle_input(self, text):
        text = text.rstrip()
        self.exec_locals['__ret_value__'] = {}
        if self.handling_multiline_input or text and text[-1] == ':':
            self.handle_input_multiline(text)
        else:
            try:
                if not text:
                    self.add_text('\n')
                    return
                func_name = text.split(' ')[0]
                func = self.functions.get(func_name, None)
                if func:
                    ret = func.handle_input(
                        self, globals(), self.exec_locals, text)
                    if ret:
                        self.handle_return({'__ret_value__': ret})
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
            if not self.typed_multilines:
                self.add_to_input_log(text)

    def add_to_input_log(self, text):
        len_input_log = len(self.input_log)
        if len_input_log == self.input_log_index:
            self.input_log.append(text)
        elif self.input_log[self.input_log_index] != text:
            self.input_log.append(text)
        self.input_log_index = len(self.input_log)

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
