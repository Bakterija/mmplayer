from .dir_maker import Config as Directories
from .user_settings import Config as UserConfig
from .keybinds import Config as KeybindConfig
from .sidebar_loader import Config as SidebarLoader
from utils import logs
import importlib

class AppConfigHandler(object):
    root_widget = None
    app = None # Unused for now
    config_instances = {
        'directories': Directories(),
        'user_settings': UserConfig(),
        'keybinder': KeybindConfig(),
        'sidebar_loader': SidebarLoader(),
    }

    def __init__(self, root_widget):
        self.root_widget = root_widget

    def load_before(self):
        for name in self.config_instances:
            try:
                self.config_instances[name].load_before(self.root_widget)
            except Exception as e:
                if self.config_instances[name].critical:
                    raise e
                else:
                    logs.error('AppConfigHandler: load_before \n', trace=True)

    def load_after(self):
        for name in self.config_instances:
            try:
                self.config_instances[name].load_after(self.root_widget)
            except Exception as e:
                if self.config_instances[name].critical:
                    raise e
                else:
                    logs.error('AppConfigHandler: load_after \n', trace=True)

    def load_with_args(self, name, *args, **kwargs):
        try:
            self.config_instances[name].load_with_args(*args, **kwargs)
        except Exception as e:
            if self.config_instances[name].critical:
                raise e
            else:
                logs.error('AppConfigHandler: load_with_args \n', trace=True)
