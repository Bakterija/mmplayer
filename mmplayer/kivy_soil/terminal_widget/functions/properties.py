from ._base import FunctionBase

class Function(FunctionBase):
    name_upper = 'Properties'
    name = 'properties'
    doc = 'Returns all properties of TerminalWidgetSystem'
    methods_subclass = {}

    def handle_input(term_system, term_globals, exec_locals, text):
        fname, method, args = Function.get_method_args(text)

        ret = list(term_system.properties())

        return ret
