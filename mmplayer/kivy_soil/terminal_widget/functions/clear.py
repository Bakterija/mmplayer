from ._base import FunctionBase

class Function(FunctionBase):
    name = 'clear'
    doc = {}

    def handle_input(term_system, term_globals, exec_locals, text):
        term_system.data = []
