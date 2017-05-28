from kivy.compat import PY2
import os, webbrowser

def get_containing_directory(file_path):
    return os.path.abspath(os.path.join(file_path, os.pardir))

def open_directory(path):
    webbrowser.open(path)

def get_unicode(string):
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
