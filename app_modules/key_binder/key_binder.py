from __future__ import print_function
from kivy.core.window import Window


class KeyBinder(object):
    def __init__(self):
        self.keybinds = {}
        Window.bind(on_key_down=self.on_key_down)
        Window.bind(on_key_up=self.on_key_up)

    def add(self, name, key, state, callback, modifier=None):
        self.keybinds[name] = {
            'callback': callback,
            'key': key,
            'state': state,
            'modifier': modifier
        }

    def remove(self, name):
        del self.keybinds[name]

    def on_key_down(self, win, key, *args):
        # print('DOWN', key, args[2])
        try:
            modifier = args[2]
        except:
            modifier = []
        for k, v in self.keybinds.iteritems():
            if v['key'] == str(key):
                if v['state'] in ('down', 'any', 'all'):
                    if not v['modifier'] or v['modifier'] == modifier:
                        v['callback']()

    def on_key_up(self, win, key, *args):
        # print('__UP', key, args)
        for k, v in self.keybinds.iteritems():
            if v['key'] == str(key):
                if v['state'] in ('up', 'any', 'all'):
                    v['callback']()
