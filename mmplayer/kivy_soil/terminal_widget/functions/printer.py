from ._base import FunctionBase

class Function(FunctionBase):
    name = 'printer'
    doc = 'Gets values of argument references and returns for printing'
    methods_subclass = {}

    def handle_input(self, term_system, term_globals, exec_locals, text):
        fname, text = self.slice_fname(text)

        return eval(text, term_globals, exec_locals)
