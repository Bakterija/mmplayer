from ._base import FunctionBase

class Function(FunctionBase):
    name = 'autocomplete_words'
    doc = {}

    def handle_input(term_system, term_globals, exec_locals, text):
        fname, method, args = Function.get_method_args(text)

        ret = list(term_system.autocomplete_words)

        return ret
