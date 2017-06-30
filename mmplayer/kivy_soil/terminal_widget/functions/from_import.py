from ._base import FunctionBase

class Function(FunctionBase):
    name = 'fromimport'
    doc = 'Imports arg[0] module or object from arg[1] module as arg[2] name'
    methods_subclass = {}

    def do_from_import(self, tglobals, elocal, from_text,
                       import_text, import_as):
        text_mod = 'from %s import %s as %s' % (
            from_text, import_text, import_as)

        try:
            exec(text_mod, tglobals, elocal)
            ret = 'Imported %s as %s' % (import_text, import_as)
        except Exception as e:
            ret = 'Failed to import %s\n%s' % (import_text, str(e))
        return ret

    def handle_input(self, term_system, term_globals, exec_locals, text):
        args = text.split(' ')[1:]

        return self.do_from_import(term_globals, exec_locals, *args)
