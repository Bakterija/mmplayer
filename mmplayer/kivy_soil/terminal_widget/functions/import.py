from ._base import FunctionBase

class Function(FunctionBase):
    name = 'import'
    doc = 'Imports arg[0] module as arg[1] name'
    methods_subclass = {}

    def do_import(self, tglobals, elocal, import_module, import_as):
        text_mod = 'import %s as %s' % (import_module, import_as)
        try:
            exec(text_mod, globals(), elocal)
            ret = 'Imported %s as %s' % (import_module, import_as)
        except Exception as e:
            ret = 'Failed to import %s\n%s' % (import_module, str(e))
        return ret

    def handle_input(self, term_system, term_globals, exec_locals, text):
        args = text.split(' ')[1:]

        return self.do_import(term_globals, exec_locals, *args)
