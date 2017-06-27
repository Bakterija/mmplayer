from kivy.properties import NumericProperty, ListProperty, StringProperty
from time import time
import copy


class LineSplitBehavior(object):
    split_text_key = StringProperty('text')
    split_text_indent = NumericProperty(4)
    chars_per_line = NumericProperty(100)
    _unsplit_data = ListProperty()

    def __init__(self, **kwargs):
        super(LineSplitBehavior, self).__init__(**kwargs)
        self.fbind('chars_per_line', self.line_split_reload)

    def set_data(self, data_full, update_unsplitted=True):
        if update_unsplitted:
            if data_full:
                key = self.split_text_key
                self._unsplit_data = [copy.copy(x) for x in data_full]
            else:
                self._unsplited_text = []
        if data_full:
            data_full = self.get_line_split_data(data_full)

        try:
            super(LineSplitBehavior, self).set_data(data_full)
        except AttributeError:
            self.data = data_full

    def get_line_split_data(self, data_full):
        new_data0 = []
        new_data = []
        cpl = self.chars_per_line
        key = self.split_text_key

        # Do fast splitting with new line characters before doing word
        # length calculations
        for x in data_full:
            split_text = x[key].splitlines()
            if len(split_text) > 1:
                for text in split_text:
                    new_dict = copy.copy(x)
                    new_dict[key] = text
                    new_data0.append(new_dict)
            else:
                new_data0.append(x)

        for x in new_data0:
            # If text does not fit in one line, start splitting it
            if len(x[key]) > cpl:
                words = x[key].split(' ')

                new_lines = []
                new_line = ''
                for word in words:
                    len_line = len(new_line)
                    len_word = len(word)

                    # When word fits in line character limit,
                    # add it to current line
                    if len_word + len_line < cpl:
                        if new_line:
                            new_line = '%s %s' % (new_line, word)
                        else:
                            new_line = word

                    # When word does not fit in line character limit
                    # append current line and start a new line
                    else:
                        new_lines.append(new_line)
                        new_line = ''

                        # When word fits in the new empty line, add it
                        if len_word < cpl:
                            if new_line:
                                new_line = '%s %s' % (new_line, word)
                            else:
                                new_line = word

                        # When word is longer then character limit,
                        # split it and add multiple lines
                        else:
                            # Calculate line count
                            split_parts = float(len_word) / float(cpl)
                            split_remain = split_parts % int(split_parts)
                            if split_remain:
                                split_parts = int(split_parts) + 1
                            else:
                                split_parts = int(split_parts)

                            # Split word into calculated line count
                            word_split = [
                                word[cpl*i:cpl*(i+1)] for i in range(
                                    split_parts)
                            ]

                            # Add parts of split word to new_lines
                            if split_remain:
                                for word in word_split[:-1]:
                                    new_lines.append(word)
                                new_line = word
                            else:
                                for word in word_split:
                                    new_lines.append(word)

                # Add any remaining text
                if new_line:
                    new_lines.append(new_line)

                # Make data copies and put in text for each line
                for new_line in new_lines:
                    new_dict = copy.copy(x)
                    new_dict[key] = new_line
                    new_data.append(new_dict)
            else:
                # Skip splitting for short text and append the data
                new_data.append(x)

        return new_data

    def line_split_reload(self, _, chars_per_line):
        self.set_data(self._unsplit_data)
