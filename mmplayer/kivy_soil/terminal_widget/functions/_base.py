class FunctionBase(object):
    name = ''
    doc = 'doc about this class'
    methods = {
        'help': 'doc about help method',
        'get_methods': 'doc about get_methods method'
    }
    methods_subclass = {}

    def __init__(self, **kwargs):
        self.methods.update(self.methods_subclass)

    def on_import(self, term_system):
        pass

    def get_methods(self):
        return [key for key in self.methods]

    def help(self, method_name):
        doc = self.methods.get(method_name[0], None)
        if doc:
            ret = doc
        else:
            ret = '# %s: %s: %s not found' % (
                self.name, 'help', method_name)
        return ret

    @staticmethod
    def slice_fname(text):
        fname = ''
        text2 = ''
        args = ''
        if text:
            b = text.find(' ')
            if b != -1:
                text2 = text[b+1:]
                fname = text[:b]
            else:
                fname = text
        return fname, text2

    @staticmethod
    def get_method_args(text):
        fname = ''
        method = ''
        args = []
        if text:
            aspl = text.split(' ')
            fname = aspl[0]
            if len(aspl) > 1:
                method = aspl[1]
            if len(aspl) > 2:
                args = tuple(aspl[2:])

        return fname, method, args

    def handle_input(self, term_system, term_globals, exec_locals, text):
        fname, method, args = self.get_method_args(text)
        found = False

        if method in self.methods:
            m = getattr(self, method, None)
            if m:
                found = True
                if args:
                    result = m(*args)
                else:
                    result = m()

        if not found:
            result = (
                '# %s: Method "%s" not found\n'
                '# Available methods are %s\n'
                '# Type "help [method_name]" for help') % (
                    self.name, method, self.get_methods())

        return result
