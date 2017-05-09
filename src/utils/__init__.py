from kivy.compat import PY2

def get_unicode(string):
    if PY2:
        string = string.encode('utf-8')
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
