from ._base import PluginBase

class Plugin(PluginBase):
    name = 'help'
    doc = 'Returns help text'
    methods_subclass = {}

    def handle_input(self, term_system, term_globals, exec_locals, text):
        fname, method, args = self.get_method_args(text)
        if method:
            ret = '%s plugin doc: %s' % (
                method, term_system.plugins[method].doc)
        else:
            fnct = 'Currently loaded plugins:\n'
            for k, v in term_system.plugins.items():
                fnct = '%s - %s: %s\n' % (fnct, k, v.doc)

            fnct = '%s\n%s' % (
                fnct, (
                'You can get more information about plugins by typing '
                '"help [plugin name]" or "[plugin name] help" and more '
                'help about plugin methods by typing '
                '"[plugin name] get_methods" or'
                '"[plugin name] help [method name]"'
                ))

            ret = '# Help text\n%s\n%s' % (term_system.doc, fnct)

        return ret
