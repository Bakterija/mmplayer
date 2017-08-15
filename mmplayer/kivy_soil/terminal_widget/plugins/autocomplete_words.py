from ._base import PluginBase

class Plugin(PluginBase):
    name = 'autocomplete_words'
    doc = 'Returns all current autocomplete words'
    methods_subclass = {}

    def handle_input(self, term_system, term_globals, exec_locals, text):
        fname, method, args = self.get_method_args(text)

        ret = list(term_system.autocomplete_words)

        return ret
