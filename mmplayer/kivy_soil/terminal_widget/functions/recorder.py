from kivy_soil.terminal_widget.shared_globals import DIR_APP, DIR_CONF
from ._base import FunctionBase
from kivy.clock import Clock
import os

PATH_AUTORUN = DIR_APP + '/autorun_files.txt'
if not os.path.exists(PATH_AUTORUN):
    with open(PATH_AUTORUN, 'w') as f:
        f.write('')


class Function(FunctionBase):
    _record_starts_at = -1
    name = 'recorder'
    doc = ('Records and saves input for running later, '
           'can also list, read and delete saved files')
    methods_subclass = {
        'run': 'run saved log',
        'list': 'show list of saved recordings',
        'read': 'print contents of a recording',
        'save': 'save current recording',
        'delete': 'delete saved recording',
        'record': 'start recording input',
        'stop_recording': 'stops current recording',
        'autorun': '',
        'autorun_list': ''
    }
    autorun_files = set()

    def on_import(self, term_system):
        self.term_system = term_system
        self._load_autorun_files()
        Clock.schedule_once(self._run_autorun_files, 0)

    def _load_autorun_files(self, *args):
        text = ''
        with open(PATH_AUTORUN, 'r') as f:
            text = f.read()
        if text:
            autolist = text.splitlines()
            for x in autolist:
                self.autorun_files.add(x)

    def _run_autorun_files(self, *args):
        for x in list(self.autorun_files):
            self.term_system.add_text('# Autorun "%s"' % (x))
            self.run(x)

    def autorun(self, file_name, *args):
        on = True
        if args:
            on = args[0]
        else:
            if file_name in self.autorun_files:
                on = False
        if on and not file_name in self.autorun_files:
            self.autorun_files.add(file_name)
        elif not on and file_name in self.autorun_files:
            self.autorun_files.remove(file_name)
        with open(PATH_AUTORUN, 'w') as fp:
            autolist = list(self.autorun_files)
            if autolist:
                string = autolist[0]
                if len(autolist) > 1:
                    for x in autolist[1:]:
                        '\n'.join((string, x))
            else:
                string = ''
            fp.write(string)

    def run(self, file_name):
        fpath = '%s/%s' % (DIR_APP, file_name)
        if os.path.exists(fpath):
            with open(fpath, 'r') as fp:
                for x in fp.read().splitlines():
                    self.term_system.handle_input(x)
        else:
            return '# %s does not exist' % fpath

    def autorun_list(self, *args):
        autolist = list(self.autorun_files)
        if autolist:
            ret = autolist
        else:
            ret = '# Autorun is empty'
        return ret

    def list(self, *args):
        files = os.listdir(DIR_APP)
        if files:
            ret = '# Recorded files in %s\n%s' % (DIR_APP, files)
        else:
            ret = '# No files recorded'
        return ret

    def read(self, file_name):
        fpath = '%s/%s' % (DIR_APP, file_name)
        if os.path.exists(fpath):
            with open(fpath, 'r') as fp:
                text = fp.read().splitlines()
                ret = text
        else:
            ret = '# %s does not exist' % fpath
        return ret

    def delete(self, file_name):
        fpath = '%s/%s' % (DIR_APP, file_name)
        if os.path.exists(fpath):
            os.remove(fpath)
            ret = '# Deleted %s' % (fpath)
        else:
            ret = '# %s does not exist' % fpath
        return ret

    def record(self, file_name):
        fpath = '%s/%s' % (DIR_APP, file_name)
        if os.path.exists(fpath):
            ret = '# %s already exists' % fpath
        else:
            ret = '# Recording input for %s, type "save" to save' % (file_name)
            self._record_starts_at = self.term_system.input_log_index + 1
            self._record_file_name = file_name
        return ret

    def stop_recording(self, *args):
        if self._record_starts_at != -1:
            self._record_starts_at = -1
            ret = '# Stopped recording'
        else:
            ret = '# Nothing to stop'
        return ret

    def save(self, *args):
        ret = ''
        if self._record_starts_at == -1:
            ret = '# Nothing to save'
        else:
            fpath = '%s/%s' % (DIR_APP, self._record_file_name)
            try:
                with open(fpath, 'w') as fp:
                    fp.write('')
                    ln = self.term_system.input_log[self._record_starts_at+1:]
                    len_lines = len(ln)
                    joined_text = ln[0]
                    for line in ln[1:]:
                        joined_text = '%s\n%s' % (joined_text, line)
                    fp.write(joined_text)
                ret = '# Saved in %s' % (fpath)
            except Exception as e:
                raise e
            finally:
                self._record_starts_at = -1
        return ret
