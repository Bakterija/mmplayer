from .config_base import ConfigBase
from kivy.utils import platform
from kivy.logger import Logger
from kivy.app import App
from utils import logs


class Config(ConfigBase):
    name = 'UserConfig', 'user_settings'

    def load_before(self, root):
        self.app = App.get_running_app()
        self.defaults = {
            'volume': ('media_controller', 100, root.media_control.set_volume)
        }

    def load_after(self, root):
        store = self.app.store
        missing = []
        for attr, items in self.defaults.items():
            success = False
            section = items[0]
            value_default = items[1]
            call = items[2]
            if store.exists(section):
                ldict = store[section]
                try:
                    value = ldict[attr]
                    call(value)
                    success = True
                except KeyError:
                    pass
            if not success:
                missing.append((section, attr, value_default))
                call(value_default)

        for section, attr, value in missing:
            self.update_store(section, attr, value)
            logs.info(('UserConfig: setting {} did not exist, '
                'loaded and stored with default value {}').format(attr, value))

    def update_store(self, section, attr, value):
        store = self.app.store
        if store.exists(section):
            new = store.get(section)
            new.update({attr:value})
        else:
            new = {attr:value}
        store.put(section, **new)

    def save_settings(self, setting_list):
        Logger.info('UserConfig: saving settings')
        for attr, value in setting_list:
            section = self.defaults[attr][0]
            self.update_store(section, attr, value)

    def load_with_args(self, *args, **kwargs):
        if args[0] == 'save':
            self.save_settings(args[1])
