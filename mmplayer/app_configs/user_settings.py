from .config_base import ConfigBase
from utils import logs, settings
from kivy.utils import platform
from kivy.logger import Logger
from kivy.app import App


class Config(ConfigBase):
    name = 'UserConfig', 'user_settings'

    def load_before(self, root):
        self.app = App.get_running_app()
        settings.update_callbacks.append(self.update_defaults)
        self.defaults = {
            'volume': ('media_controller', 100, root.media_control.set_volume)
        }
        if settings.store:
            self.update_defaults(settings.store)

    def update_defaults(self, new_dict):
        self.defaults.update(new_dict)

    def load_after(self, root):
        store = self.app.store
        if not store:
            Logger.warning('user_settings: load_after: app.store is None, '
                           'skipping load settings')
            return
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
                    if section[:3] == 'ED_':
                        call(None, value)
                    else:
                        call(value)
                    success = True
                except KeyError:
                    pass
            if not success:
                missing.append((section, attr, value_default))
                if section[:3] == 'ED_':
                    call(None, value_default)
                else:
                    call(value_default)

        if missing:
            for section, attr, value in missing:
                self.update_store(section, attr, value)
            logs.info(('UserConfig: found {} missing settings,'
                'saved to file').format(len(missing)))

    def update_store(self, section, attr, value):
        store = self.app.store
        if store.exists(section):
            new = store.get(section)
            new.update({attr:value})
        else:
            new = {attr:value}
        store.put(section, **new)

    # def save_defaults(self):
    #     self.save_defaults(self.defaults.items())

    def _save_settings(self, setting_list):
        Logger.info('UserConfig: saving settings for %s')
        for attr, value in setting_list:
            section = self.defaults[attr][0]
            self.update_store(section, attr, value)

    def load_with_args(self, *args, **kwargs):
        if not self.app.store:
            Logger.warning('user_settings: load_with_args: app.store is None, '
                            'returning')
            return
        if args[0] == 'save':
            self._save_settings(args[1])
