from __future__ import print_function
from kivy.core.window import Window
from kivy.logger import Logger


class KeyBinder(object):
    keybinds = {}
    use_logger = False

    def __init__(self):
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
        try:
            modifier = args[2]
        except:
            modifier = []
        if self.use_logger:
            Logger.info('KeyBinder: on_key_down: {} - {}'.format(key, modifier))
        for k, v in self.keybinds.iteritems():
            if v['key'] == str(key):
                if v['state'] in ('down', 'any', 'all'):
                    if not v['modifier'] or v['modifier'] == modifier:
                        v['callback']()

    def on_key_up(self, win, key, *args):
        if self.use_logger:
            Logger.info('KeyBinder: on_key___up: {} - {}'.format(key, args))
        for k, v in self.keybinds.iteritems():
            if v['key'] == str(key):
                if v['state'] in ('up', 'any', 'all'):
                    v['callback']()
