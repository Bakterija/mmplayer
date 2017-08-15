from ._base import PluginBase

class Plugin(PluginBase):
    name = 'plugins'
    doc = 'Reuturns list of all loaded plugins'
    methods_subclass = {}

    def handle_input(self, term_system, term_globals, exec_locals, text):
        fname, method, args = self.get_method_args(text)

        ret = list(term_system.plugins)

        return ret
