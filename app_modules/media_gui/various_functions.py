from sys import path
from kivy.utils import platform
import json
import os


ignored_dirs = []
home_dir = os.path.expanduser("~")+'/'
platformfolders = {}
if platform == 'android':
    audio_path = '/storage/emulated/0/github_bakterija/jotube/audio/'
    syspath = path[4]
    platformfolders = [
        ['Movies', '/storage/emulated/0/Movies'],
        ['Music', '/storage/emulated/0/Music']]
else:
    syspath = path[0]
    if platform in ('linux', 'win'):
        audio_path = syspath+'/media/'
        platformfolders = [
            ['Downloads', home_dir+'Downloads/'],
            ['Music', home_dir+'Music/'],
            ['Videos', home_dir+'Videos/']]


def load_json(path):
    with open(path) as data_file:
        data = json.load(data_file)
        return data


def save_json(path, dictio):
    with open(path, 'w') as outfile:
        json.dump(dictio, outfile, indent=4, sort_keys=True, separators=(',', ':'))


def save_playlists(dictio):
    save_json('%splaylist.json' % (audio_path), dictio)


def save_playlist(path, dictio):
    dictio2 = load_json(path)
    dictio2['items'] = []
    for item in dictio:
        if item['path']:
            dictio2['items'].append({
                'name':item['name'],
                'path':item['path']
            })
    save_json(path, dictio2)


def create_playlist(name):
    dictio = {'items':[]}
    save_json('%s/playlists/%s.json' % (audio_path, name), dictio)


def remove_playlist(name, path, section):
    if section == 'playlists':
        os.remove(path)


def get_folders(path, sort='abc'):
    templist = []
    for dirname, dirnames, filenames in os.walk(path):
        for subdirname in dirnames:
            dirpath = os.path.join(dirname, subdirname)
            if os.path.exists(dirpath+'/__ignore__.ydl') == False:
                templist.append([subdirname, dirpath])
    if sort == 'abc':
        templist.sort()
    return templist


def json_loader(path):
    dictio = load_json(path)
    return dictio


def get_playlists(sort='abc', platform_defaults=True):
    places, playlists = [], []
    if platform_defaults:
        for name, path in platformfolders:
            d = path
            if os.path.exists(d):
                places.append({
                    'name':name,
                    'path':path,
                    'method':'folder_loader',
                    'section':'places'
                })
    for name, path in get_files(audio_path+'/playlists/', sort):
        if name[-5:] == '.json':
            name = name[:-5]
        playlists.append({
            'name':name,
            'path':path,
            'method':'json_loader',
            'section':'playlists',
            'files':[]
        })
    return [places, playlists]


def get_files(path, sort='abc'):
    templist = []
    for dirname, dirnames, filenames in os.walk(path):
        for filename in filenames:
            templist.append([
                filename.decode('utf-8'),
                os.path.join(dirname, filename).decode('utf-8')
                ])
    if sort == 'abc':
        templist.sort()
    return templist
