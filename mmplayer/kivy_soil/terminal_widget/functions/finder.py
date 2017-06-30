from ._base import FunctionBase

class Function(FunctionBase):
    name = 'finder'
    doc = 'Finds and returns text from TerminalWidgetSystem data'
    methods_subclass = {}

    def handle_input(self, term_system, term_globals, exec_locals, text):
        fname, method, args = self.get_method_args(text)
        if args:
            find = ' '.join(text).lower()
        else:
            find = str(method).lower()
            method = 'term_data'

        results = ['%s: %s' % (i, x['text']) for i, x in enumerate(
            term_system.data) if find in x['text'].lower()]

        if results:
            str1, str2 = '# Finder: results start', '# Finder: results end'
            results = [str1] + results + [str2]
            ret = '\n'.join(results)
        else:
            ret = '# Finder: "%s" was not found' % (find)

        return ret
