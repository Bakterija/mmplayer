class FunctionBase(object):
    name = ''
    doc = {
        'class': 'doc about this function class',
        'help': 'doc about help method',
        'methods': 'doc about methods method'
    }

    def methods():
        return [key for key in this.doc]

    def help():
        pass

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

        return fname, method, args

    def handle_input(term_system, term_globals, exec_locals, text):
        fname, method, args = this.get_method_args(text)

this = FunctionBase
