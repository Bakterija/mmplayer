from ._base import FunctionBase

class Function(FunctionBase):
    name = 'autocomplete_words'
    doc = 'Returns all current autocomplete words'
    methods_subclass = {}

    def handle_input(self, term_system, term_globals, exec_locals, text):
        fname, method, args = self.get_method_args(text)

        ret = list(term_system.autocomplete_words)

        return ret
