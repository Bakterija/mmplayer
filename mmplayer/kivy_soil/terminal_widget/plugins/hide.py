from ._base import PluginBase


class Plugin(PluginBase):
    name = 'hide'
    doc = 'Hides this widget'

    def handle_input(self, term_system, term_globals, exec_locals, text):
        term_system.term_widget.animate_out()
