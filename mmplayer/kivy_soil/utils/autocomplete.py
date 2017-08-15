from copy import copy

DEFAULT_SPECIAL_CHARS = [
    ' ', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '=', '+',
    '{', '}', '[', ']', '\\', '|', ':', ';', "'", '"', '/', ',', '<', '.',
    '>', '/', '?'
]

class Autocompleter(object):
    autocomplete_words = set()
    '''Set with autocomplete words'''

    special_chars = DEFAULT_SPECIAL_CHARS

    def __init__(self):
        self.autocomplete_words = copy(self.autocomplete_words)
        self.special_chars = copy(self.special_chars)

    def add_word(self, word):
        self.autocomplete_words.add(word)

    def add_words_from_text(self, text):
        text2 = text
        for x in (' ', '!', '@', '$', '#', '%', '^', '&', '*', '(', ')',
                  '-', '=', '+', '{', '}', '[', ']', '\\', '|', '?',
                  ';', ':', '<', '>', ',', '.', '/', '1', '2', '3',
                  '4', '5', '6', '7', '8', '9', '`', '~'):
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

    def find_nearest_special(self, text, cursor_index):
        text = text[:cursor_index]
        rev_text = text[::-1]
        nearest = -1
        for x in self.special_chars:
            b = rev_text.find(x)
            if b != -1:
                if nearest == -1:
                    nearest = b
                elif nearest > b:
                    nearest = b

        if nearest == -1:
            nearest = 0
        else:
            nearest = len(text) - nearest
        return nearest

    def autocomplete(self, text, cursor_index):
        found_words, insert_text = [], ''
        if not text:
            return found_words, insert_text

        len_text = len(text)
        insert_text = ''

        # looks for a special characters before cursor,
        # then sets word start slice number
        start = self.find_nearest_special(text, cursor_index)

        if start != -1:
            word = text[start:cursor_index]
            # Does nothing when word is empty
            if word:
                len_word = len(word)
                # Looks for matching strings in autocomplete_words
                # Appends all results to found list
                for x in self.autocomplete_words:
                    if x[:len(word)].lower() == word.lower():
                        found_words.append(x)

            len_found_words = len(found_words)
            # If only one word found, insert text from it
            if len_found_words:
                if len_found_words == 1:
                    insert_text = found_words[0][len_word:]
                    if len_text == cursor_index:
                        insert_text = insert_text + ' '
                else:
                    # If multiple words found, looks for and adds
                    # matching characters untill word_min_len index
                    # is reached, then stops and returns character string
                    # for inserting
                    found_lens = [len(x) for x in found_words]
                    word_min_len = min(found_lens)
                    len_word = len(word)
                    match_index = len_word
                    for char in found_words[0][match_index:word_min_len]:
                        are_matching = True
                        for x in found_words[1:word_min_len]:
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
        return found_words, insert_text
