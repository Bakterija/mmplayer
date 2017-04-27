from .config_base import ConfigBase
from kivy.utils import platform
from kivy.logger import Logger
from kivy.compat import PY2
if PY2:
    import ConfigParser as configparser
else:
    import configparser as configparser


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
        try:
            for key, value in self.config.items('MAIN'):
                self.loader_switch[key](value)
        except configparser.NoSectionError:
            return

    def load_with_args(self, *args, **kwargs):
        if args[0] == 'save':
            try:
                for key, value in args[1].items():
                    self.config.set('MAIN', key, value)
            except configparser.NoSectionError:
                self.config.add_section('MAIN')
                self.load_with_args(*args)

            with open(self.confpath, 'w') as configfile:
                self.config.write(configfile)
