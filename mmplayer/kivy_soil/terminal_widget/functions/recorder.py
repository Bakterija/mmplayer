from ._base import FunctionBase

class Function(FunctionBase):
    name_upper = 'Recorder'
    name = 'recorder'
    methods2 = {
        'run': 'd',
        'list': 'd',
        'read': 'd',
        'save': 'd',
        'delete': 'd',
        'record': 'd'
    }
    def __init__(self, **kwargs):
        self.methods.update(self.methods2)

    def run(self, file_name):
        fpath = '%s/%s' % (DIR_APP, file_name)
        if os.path.exists(fpath):
            with open(fpath, 'r') as fp:
                text = fp.read()
                self.handle_input(text)
        else:
            self.add_text('# %s does not exist' % fpath)

    def list(self, *args):
        files = os.listdir(DIR_APP)
        if files:
            adt = '# Recorded files in %s\n%s' % (DIR_APP, files)
        else:
            adt = '# No files recorded'
        self.add_text(adt)

    def read(self, file_name):
        fpath = '%s/%s' % (DIR_APP, file_name)
        if os.path.exists(fpath):
            with open(fpath, 'r') as fp:
                text = fp.read().splitlines()
                self.add_text(text)
        else:
            self.add_text('# %s does not exist' % fpath)

    def delete(self, file_name):
        fpath = '%s/%s' % (DIR_APP, file_name)
        if os.path.exists(fpath):
            os.remove(fpath)
            self.add_text('# Deleted %s' % (fpath))
        else:
            self.add_text('# %s does not exist' % fpath)

    def record(self, file_name):
        fpath = '%s/%s' % (DIR_APP, file_name)
        if os.path.exists(fpath):
            self.add_text('# %s already exists' % fpath)
        else:
            self.add_text(
                '# Recording input for %s, type "save" to save' % (file_name))
            self._record_starts_at = self.input_log_index + 1
            self._record_file_name = file_name

    def save(self, *args):
        addt = ''
        if not hasattr(self, '_record_starts_at'):
            addt = '# Nothing to save'
        elif self._record_starts_at == -1:
            addt = '# Nothing to save'
        else:
            fpath = '%s/%s' % (DIR_APP, self._record_file_name)
            try:
                with open(fpath, 'w') as fp:
                    fp.write('')
                    lines = self.input_log[self._record_starts_at+1:]
                    len_lines = len(lines)
                    joined_text = lines[0]
                    for line in lines[1:]:
                        joined_text = '%s\n%s' % (joined_text, line)
                    fp.write(joined_text)
                addt = '# Saved recorded in %s' % (fpath)
            except Exception as e:
                self.add_text(str(e), level='exception')
        self._record_starts_at = -1
        if addt:
            self.add_text(addt)

    # def handle_input(term_system, term_globals, exec_locals, text):
    #     fname, method, args = Function.get_method_args(text)
    #
    #
    #
    #     return ret

Function = Function()
