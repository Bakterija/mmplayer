from ._base import FunctionBase

class Function(FunctionBase):
    name = 'help'
    doc = 'Returns help text'
    methods_subclass = {}

    def handle_input(self, term_system, term_globals, exec_locals, text):
        fname, method, args = self.get_method_args(text)
        if method:
            ret = '%s function doc: %s' % (
                method, term_system.functions[method].doc)
        else:
            fnct = 'Currently loaded plugin functions:\n'
            for k, v in term_system.functions.items():
                fnct = '%s - %s: %s\n' % (fnct, k, v.doc)

            fnct = '%s\n%s' % (
                fnct, (
                'You can get more information about functions by typing '
                '"help [function name]" or "[function name] help" and more '
                'help about function methods by typing '
                '"[function name] get_methods" or'
                '"[function name] help [method name]"'
                ))

            ret = '# Help text\n%s\n%s' % (term_system.doc, fnct)

        return ret
