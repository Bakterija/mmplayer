from config_base import ConfigBase
import ConfigParser as configparser
from kivy.utils import platform
from kivy.logger import Logger


class Config(ConfigBase):
    name = 'UserConfig', 'user_settings'
    config = configparser.ConfigParser()
    confpath = 'app_configs/settings.ini'

    def __init__(self):
        loaded_files = self.config.read(self.confpath)
        if loaded_files:
            Logger.info('{}: loaded settings.ini'.format(self.name[0]) )
        else:
            Logger.error('{}: did not load settings.ini'.format(self.name[0]) )

    def load_before(self, root):
        self.loader_switch = {
            'volume': lambda val: root.mPlayer.set_volume(float(val) * 100.0)
        }

    def load_after(self, root):
        if platform in ('linux', 'win', 'windows'):
            from kivy.core.window import Window
            Window.set_icon('data/icon.png')

        self.load_configs(root)

    def load_configs(self, root):
        for key, value in self.config.items('MAIN'):
            self.loader_switch[key](value)

    def load_with_args(self, *args, **kwargs):
        if args[0] == 'save':
            for key, value in args[1].iteritems():
                self.config.set('MAIN', key, value)

            with open(self.confpath, 'wb') as configfile:
                self.config.write(configfile)
