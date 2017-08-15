class PluginBase(object):
    name = ''
    doc = 'doc about this class'
    methods_subclass = {}

    def __init__(self, **kwargs):
        self.methods = {
            'help': 'doc about help method',
            'get_methods': 'doc about get_methods method'
        }
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
    def get_args_kwargs_from_text(text):
        start_str = (None, -1)
        strings_found = []
        kwargs_found = {}
        args_found = []

        for i, char in enumerate(text):
            if char in ("'", '"'):
                if start_str[0]:
                    if char == start_str[0]:
                        rev = text[:i+1][::-1]
                        b = rev[i+1 - start_str[1]:].find(' ')

                        if b != -1:
                            strings_found.append((start_str[1] - b, i+1))
                        else:
                            strings_found.append((start_str[1], i+1))
                        start_str = (None, -1)
                else:
                    start_str = (char, i)

        if strings_found:
            last_end = 0
            for start, end in strings_found:
                before = text[last_end:start]
                for x in before.split(' '):
                    if x:
                        args_found.append(x)
                args_found.append(text[start:end])
                last_end = end
            for x in text[end:].split(' '):
                if x:
                    args_found.append(x)
        else:
            args_found = text.split(' ')

        remlist = []
        for i, x in enumerate(args_found):
            a = x.find('=')
            if a != -1:
                yes = False
                c = x.find("'")
                b = x.find('"')
                if b == -1 and c == -1:
                    yes = True
                else:
                    start = b
                    if c != -1 and c < b:
                        start = c
                    a = x[:start].find('=')
                    if a != -1:
                        yes = True
                if yes:
                    kwargs_found[x[:a]] = x[a+1:]
                    remlist.append(i)
        for x in reversed(remlist):
            del args_found[x]

        return args_found, kwargs_found

    @staticmethod
    def get_from_locals_globals(term_system, text):
        ret = term_system.exec_locals.get(text, None)
        if not ret:
            ret = term_system.get_globals().get(text, None)
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
                args = aspl[2:]
        return fname, method, tuple(args)

    @staticmethod
    def get_method_args_kwargs(text):
        fname, method, args, kwargs = '', '', [], {}
        if text:
            aspl = text.split(' ')
            fname = aspl[0]
            if len(aspl) > 1:
                method = aspl[1]
            if len(aspl) > 2:
                args, kwargs = PluginBase.get_args_kwargs_from_text(
                    ' '.join(aspl[2:]))
        return fname, method, tuple(args), kwargs

    def handle_input(self, term_system, term_globals, exec_locals, text):
        fname, method, args, kwargs = self.get_method_args_kwargs(text)
        found = False

        if method in self.methods:
            m = getattr(self, method, None)
            if m:
                found = True
                if args and kwargs:
                    result = m(*args, **kwargs)
                elif args:
                    result = m(*args)
                elif kwargs:
                    result = m(**kwargs)
                else:
                    result = m()

        if not found:
            result = (
                '# %s: Method "%s" not found\n'
                '# Available methods are %s\n'
                '# Type "help [method_name]" for help') % (
                    self.name, method, self.get_methods())

        return result
