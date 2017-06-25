from __future__ import print_function
from kivy.properties import ListProperty, NumericProperty, ObjectProperty
from kivy.event import EventDispatcher
from time import time, strftime, gmtime
from kivy.logger import Logger
from kivy.clock import Clock
from functools import partial
from kivy.app import App
import traceback
import random
import re


class TerminalWidgetSystem(EventDispatcher):
    time_stamp_mode = NumericProperty(0)
    input_log_index = NumericProperty(0)
    term_widget = ObjectProperty()
    _empty_try_autocompletes = 0
    input_log = ListProperty()
    autocomplete_words = {'self', 'app', 'term_widget'}
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
            'autocomplete_words': self.get_autocomplete_words,
            'fromimport': self.do_from_import,
            'functions': self.get_functions,
            'properties': self.properties,
            'setprop': self.set_property,
            'import': self.do_import,
            'printer': self.printer,
            'help': self.print_help,
        }
        for item in self.functions:
            self.autocomplete_words.add(item)
        for item in self.properties():
            self.autocomplete_words.add(item)
        self.exec_locals = {'app': App.get_running_app(), 'self': self}

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

    def do_import(self, import_module, import_as):
        text_mod = 'import %s as %s' % (import_module, import_as)
        try:
            exec(text_mod, globals())
            self.add_text('Imported %s as %s' % (import_module, import_as))
        except Exception as e:
            self.add_text('Failed to import %s\n%s' % (import_module, str(e)))

    def do_from_import(self, from_text, import_text, import_as):
        text_mod = 'from %s import %s as %s' % (
            from_text, import_text, import_as)
        try:
            exec(text_mod, globals())
            self.add_text('Imported %s as %s' % (import_text, import_as))
        except Exception as e:
            self.add_text('Failed to import %s\n%s' % (import_text, str(e)))

    def print_help(self):
        ret = ('# Help text\n'
        'properties:\n{}\n'
        'autocomplete_words:\n{}\n'
        'functions:\n{}\n'
        ).format(
            str([v for v in self.properties()]), str(self.autocomplete_words),
            str([v for v in self.functions])
        )
        self.add_text(ret)

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
                  '-', '_', '=', '+', '{', '}', '[', ']', '\\', '|', '?',
                  ';', ':', '<', '>', ',', '.', '/', '1', '2', '3', '4', '5',
                  '6', '7', '8', '9', '`', '~'):
            text2 = text2.replace(x, '0')
        text2 = text2.replace("'", '0')
        text2 = text2.replace('"', '0')
        text2 = text2.replace('"', '0')
        words = text2.split('0')
        for word in words:
            if word:
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
                Clock.schedule_once(self.reset_empty_autocompletes)
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
                        if x[:len(word)] == word:
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
                                if x[match_index] != char:
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
        if not text:
            return
        args = text.split(' ')
        if text[-1] == ' ':
            text = text[:-1]
        text_mod = args[0]
        args = args[1:]
        try:
            func = self.functions.get(text_mod, None)
            if func:
                if args:
                    ret = func(*args)
                else:
                    ret = func()
                if ret:
                    self.handle_return({'__ret_value__': ret})
            else:
                self.exec_locals['__ret_value__'] = {}

                try:
                    exec('__ret_value__ = %s' % (
                        text), globals(), self.exec_locals)
                except SyntaxError:
                    exec(text, globals(), self.exec_locals)
                except AttributeError:
                    exec(text, globals(), self.exec_locals)
                self.handle_return(self.exec_locals)
        except Exception as e:
            if self.use_logger:
                Logger.error('TerminalWidgetSystem: %s\n%s' % (
                    e, traceback.format_exc()))
            self.add_text('TerminalWidgetSystem: %s\n%s' % (
                    e, traceback.format_exc()),level='exception')

        len_input_log = len(self.input_log)
        if len_input_log == self.input_log_index:
            self.input_log.append(text)
        elif self.input_log[self.input_log_index] != text:
            self.input_log.append(text)
        self.input_log_index = len(self.input_log)

    def handle_return(self, new_locals):
        ret = new_locals.get('__ret_value__', None)
        if ret:
            if isinstance(ret, dict):
                self.add_text('#Dict result')
                for k, v in ret.items():
                    self.add_text('%s: %s' % (k, v))
                self.add_text('#Dict result end')
            elif isinstance(ret, list):
                self.add_text('#List result')
                for x in iter(ret):
                    self.add_text(x)
                self.add_text('#List result end')
            else:
                self.add_text(ret)
