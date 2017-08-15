from ._base import FunctionBase

class Function(FunctionBase):
    name = 'finder'
    doc = 'Finds and returns text from TerminalWidgetSystem data'
    methods_subclass = {'in_log': '', 'in_string': '', 'in_list': ''}

    def on_import(self, term_system):
        self.term_system = term_system

    def in_log(self, *text):
        text = ' '.join(text)
        results = ['%s: %s' % (i, x['text']) for i, x in enumerate(
            self.term_system.data) if text in x['text'].lower()]
        return self.handle_results(results, text)

    def in_string(self, source, text):
        source = self.get_from_locals_globals(self.term_system, source)
        source = source.splitlines()
        results = [
            '%s: %s' % (i, x) for i, x in enumerate(source) if text in x]
        return self.handle_results(results, text)

    def in_list(self, source, text):
        source = self.get_from_locals_globals(self.term_system, source)
        results = [
            '%s: %s' % (i, x) for i, x in enumerate(source) if text in x]
        return self.handle_results(results, text)

    def handle_results(self, results, text):
        if results:
            str1, str2 = '# Finder: results start', '# Finder: results end'
            results = [str1] + results + [str2]
            ret = '\n'.join(results)
        else:
            ret = '# Finder: "%s" was not found' % (text)
        return ret
