from kivy.compat import PY2
import os, webbrowser

def get_containing_directory(file_path):
    '''Returns directory path which contains file_path'''
    return os.path.abspath(os.path.join(file_path, os.pardir))

def open_directory(path):
    '''Calls webbrowser.open(path)'''
    webbrowser.open(path)

def get_unicode(string):
    '''Takes any bytes or str objects, then returns a unicode utf-8 string '''
    if PY2:
        try:
            string = string.encode('utf-8')
        except:
            pass
        string = unicode(string, 'utf-8')
    else:
        if isinstance(string, bytes):
            string = string.decode('utf-8')
    return string

def get_files(self, path, sort='abc'):
    '''Finds and returns list of all files in path and sub directories in it'''
    templist = []
    time0 = time()
    if os.path.isfile(path):
        return [get_default_media_dict(path)]

    for dirname, dirnames, filenames in os.walk(path):
        for file_name in filenames:
            file_path = os.path.join(dirname, file_name)
            new_file = get_default_media_dict(file_path)
            if new_file:
                templist.append(new_file)
    # if sort == 'abc':
    #     templist
    if time() - time0 > 1.0:
        Logger.info('get_files: found {} files in {} seconds'.format(
            len(templist), time() - time0))
    return templist

def is_exe(fpath):
    '''Checks if file is exe, then returns bool'''
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

def which(program):
    '''Checks if program string name is in path.
    If found, returns path where it is, otherwise returns nothing'''
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None

def seconds_to_minutes_hours(seconds, div_hours=True):
    '''Divmods seconds argument into hours:minutes:seconds format, then
    returns it'''
    s = int(seconds)
    m, s = divmod(s, 60)
    if m > 59 and div_hours:
        h, m = divmod(m, 60)
        result = ''.join((
            str(h).zfill(2), ':', str(m).zfill(2), ':', str(s).zfill(2)))
    else:
        result = ''.join((str(m).zfill(2),':', str(s).zfill(2)))
    return result
