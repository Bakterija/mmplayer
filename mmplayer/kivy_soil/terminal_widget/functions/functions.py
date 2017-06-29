from ._base import FunctionBase

class Function(FunctionBase):
    name_upper = 'Funcions'
    name = 'functions'
    doc = 'Reuturns list of all loaded plugin functions'
    methods_subclass = {}

    def handle_input(term_system, term_globals, exec_locals, text):
        fname, method, args = Function.get_method_args(text)

        ret = list(term_system.functions)

        return ret