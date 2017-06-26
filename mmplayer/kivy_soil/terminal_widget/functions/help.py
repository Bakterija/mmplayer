from ._base import FunctionBase

class Function(FunctionBase):
    name = 'help'
    doc = {}

    def handle_input(term_system, term_globals, exec_locals, text):
        fname, method, args = Function.get_method_args(text)

        ret = (
            '# Help text\n'
            'properties:\n{}\n'
            'functions:\n{}\n'
            ).format(
                str([v for v in term_system.properties()]),
                str([v for v in term_system.functions])
                )

        return ret
