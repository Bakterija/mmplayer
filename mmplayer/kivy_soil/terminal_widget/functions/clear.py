from ._base import FunctionBase

class Function(FunctionBase):
    name = 'clear'
    doc = 'Clears TerminalWidgetSystem data'
    methods_subclass = {}

    def handle_input(self, term_system, term_globals, exec_locals, text):
        term_system.data = []
