from kivy.properties import NumericProperty, ListProperty
import copy


class LineSplitBehavior(object):
    split_text_keys = ListProperty(['text',])
    split_text_indent = NumericProperty(4)
    chars_per_line = NumericProperty(100)

    def __init__(self, **kwargs):
        super(LineSplitBehavior, self).__init__(**kwargs)
        self.fbind('chars_per_line', self.line_split_reload)

    def set_data(self, data_full):
        if data_full:
            data_full = self.get_line_split_data(data_full)
        super(LineSplitBehavior, self).set_data(data_full)

    def get_line_split_data(self, data_full):
        new_data0 = []
        new_data = []
        cpl = self.chars_per_line
        for x in data_full:
            for key in self.split_text_keys:
                split_text = x[key].splitlines()
                if len(split_text) > 1:
                    for text in split_text:
                        new_dict = copy.copy(x)
                        new_dict[key] = text
                        new_data0.append(new_dict)
                else:
                    new_data0.append(x)

        for x in new_data0:
            added_to_data = False
            for key in self.split_text_keys:
                len_key_text = len(x[key])
                if len_key_text > cpl:
                    words = x[key].split(' ')

                    new_lines = []
                    new_line = ''
                    was_split = False
                    # print('JAUNS!___________-', words)
                    for word in words:
                        len_line = len(new_line)
                        len_word = len(word)
                        # print([word], [new_line])
                        if len_word > cpl:
                            if len_line:
                                new_lines.append(new_line)
                            len_splitted_word = []
                            for i in range(int(len_word / cpl) + 1):
                                len_splitted_word.append(word[:cpl])
                                word = word[cpl:]
                            # print('LENSPLIT!', len_splitted_word)
                            for word in len_splitted_word:
                                new_lines.append(word)
                            new_line = ''
                            was_split = True
                        elif len_line + len_word <= cpl:
                            new_line = '%s %s' % (new_line, word)
                        elif len_line + len_word > cpl:
                            new_lines.append(new_line)
                            new_line = word
                            was_split = True
                        else:
                            new_lines.append(new_line)
                            new_line = ''
                        if new_lines and new_lines[-1][0] == ' ':
                            new_lines[-1] = new_lines[-1][1:]
                        # print([word], [new_line])
                    # print(new_lines)
                    for new_line in new_lines:
                        new_dict = copy.copy(x)
                        new_dict[key] = new_line
                        new_data.append(new_dict)
                    added_to_data = True
            if not added_to_data:
                new_data.append(x)

        return new_data

    def line_split_reload(self, _, chars_per_line):
        self.set_data(self.data_full)
