from ._base import PluginBase

class Plugin(PluginBase):
    name = 'clear'
    doc = 'Clears TerminalWidgetSystem data'
    methods_subclass = {}

    def handle_input(self, term_system, term_globals, exec_locals, text):
        term_system.data = []
