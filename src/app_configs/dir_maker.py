from .config_base import ConfigBase
from kivy.utils import platform
import global_vars
import os


class Config(ConfigBase):

    @staticmethod
    def load_before(root_widget):
        directories = []
        if platform == 'android':
            directories = (
                '/storage/emulated/0/github_bakterija/'
            )

        else:
            directories = (
                'media/thumbnails/',
                'media/playlists/',
                global_vars.DIR_PLAYLISTS
            )

        for x in directories:
            d = os.path.dirname(x)
            if not os.path.exists(d):
                os.makedirs(d)

    @staticmethod
    def load_after(root_widget):
        pass
