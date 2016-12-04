from __future__ import print_function
from kivy.core.window import Window

class KeyBinder(object):
    def __init__(self):
        self.keybinds = {}
        Window.bind(on_key_down=self.on_key_down)
        Window.bind(on_key_up=self.on_key_up)

    def add(self, name, key, state, callback):
        self.keybinds[name] = {
            'callback': callback,
            'key': key,
            'state': state
        }

    def remove(self, name):
        del self.keybinds[name]

    def on_key_down(self, win, key, *arg):
        #print('DOWN', key)
        for k, v in self.keybinds.iteritems():
            if v['key'] == str(key):
                if v['state'] in ('down', 'any', 'all'):
                    v['callback']()

    def on_key_up(self, win, key, *args):
        #print('__UP', key)
        for k, v in self.keybinds.iteritems():
            if v['key'] == str(key):
                if v['state'] in ('up', 'any', 'all'):
                    v['callback']()
