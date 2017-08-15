from kivy.properties import ListProperty, NumericProperty
from kivy_soil.app_recycleview import AppRecycleViewClass
from kivy.utils import get_hex_from_color
from kivy.utils import escape_markup
from kivy.uix.label import Label
import copy


class TerminalWidgetLabel(AppRecycleViewClass, Label):
    markup = True
    important_word_color = get_hex_from_color((0.7, 0.3, 0.55, 1.0))
    text_colors = {
        'hash':      get_hex_from_color((0.7, 0.7, 0.3, 1.0)),
        'info':      get_hex_from_color((0.3, 0.7, 0.3, 1.0)),
        'warning':   get_hex_from_color((0.7, 0.5, 0.2, 1.0)),
        'error':     get_hex_from_color((0.7, 0.2, 0.2, 1.0)),
        'exception': get_hex_from_color((0.7, 0.2, 0.2, 1.0))
    }
    _lvlreplace = [
        ('[INFO', text_colors['info']),
        ('[WARNING', text_colors['warning']),
        ('[EXCEPTION', text_colors['exception']),
        ('[ERROR', text_colors['error'])
    ]
    important_words = {
        'self', 'object', 'def', 'abs', 'divmod', 'input', 'open',
        'staticmethod', 'all', 'enumerate', 'int', 'ord', 'str',
        'any', 'eval', 'isinstance', 'pow', 'sum', 'basestring',
        'execfile', 'issubclass', 'print', 'super', 'bin', 'file',
        'iter', 'property', 'tuple', 'bool', 'filter', 'len',
        'range', 'type', 'bytearray', 'float', 'list', 'raw_input',
        'unichr', 'callable', 'format', 'locals', 'reduce', 'unicode',
        'chr', 'frozenset', 'long', 'reload', 'vars', 'classmethod',
        'getattr', 'map', 'repr', 'xrange', 'cmp', 'globals', 'max',
        'reversed', 'zip', 'compile', 'hasattr', 'memoryview', 'round',
        '__import__', 'complex', 'hash', 'min', 'set', 'delattr',
        'help', 'next', 'setattr', 'dict', 'hex', 'object', 'slice',
        'dir', 'id', 'oct', 'sorted', 'class'
    }

    def __init__(self, **kwargs):
        super(TerminalWidgetLabel, self).__init__(**kwargs)
        self.fbind('width', self.update_text_width)
        self.max_lines = 1
        self.shorten = True

    def markup_log_level(self, text):
        for lvltext, lvlcolor in self._lvlreplace:
            start = text.find(lvltext)
            if start != -1:
                end = text[start:].find(']') + start + 1
                text = '%s[color=%s]%s[/color]%s' % (
                    text[:start], lvlcolor, text[start:end], text[end:])
                break
        return text

    def markup_important_words(self, text, len_text):
        for word in self.important_words:
            start = 0
            for i in range(len_text):
                start = text[start:].find(word) + start
                if start == -1:
                    break
                else:
                    end = start + len(word)
                    if start == 0 or text[start-1] == ' ':
                        if end == len(text) or text[end] == ' ':
                            text = '%s[color=%s]%s[/color]%s' % (
                                text[:start], self.important_word_color,
                                text[start:end], text[end:])
        return text

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.font_name = rv.font_name
        self.font_size = rv.font_size

        text = data['text']
        if text:
            len_text = len(text)
            opening = 0
            for i in range(len_text):
                opening = text[opening:].find('[') + opening
                if opening == -1:
                    break
                else:
                    is_closing = text[opening:].find(']')
                    if is_closing == -1:
                        text = '%s%s%s' % (
                            text[:opening],
                            escape_markup(text[opening:opening+2]),
                            text[opening+2:])
                    opening += 2

            if text[0] == '#':
                col = get_hex_from_color((0.7, 0.7, 0.3, 1.0))
                text = '[color=%s]%s[/color]' % (col, text)
            else:
                text = self.markup_log_level(text)
                text = self.markup_important_words(text, len_text)
        for attr, value in data.items():
            if attr != 'text':
                setattr(self, attr, value)
        self.text = text

    def update_text_width(self, _, value):
        self.text_size = (value, None)
