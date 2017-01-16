from config_base import ConfigBase
from kivy.utils import platform
import os


class Config(ConfigBase):

    @staticmethod
    def load_before(root_widget):
        if platform == 'android':
            d = os.path.dirname('/storage/emulated/0/github_bakterija/')
            if not os.path.exists(d):
                os.makedirs(d)
            d = os.path.dirname('/storage/emulated/0/github_bakterija/jotube/')
            if not os.path.exists(d):
                os.makedirs(d)
            d = os.path.dirname(
                '/storage/emulated/0/github_bakterija/jotube/audio/')
            if not os.path.exists(d):
                os.makedirs(d)
            d = os.path.dirname(
                '/storage/emulated/0/github_bakterija/jotube/audio/thumbnails/')
            if not os.path.exists(d):
                os.makedirs(d)
            d = os.path.dirname(
                '/storage/emulated/0/github_bakterija/jotube/audio/')
        else:
            d = os.path.dirname('media/thumbnails/')
            if not os.path.exists(d):
                os.makedirs(d)
            d = os.path.dirname('media/playlists/')
            if not os.path.exists(d):
                os.makedirs(d)

    @staticmethod
    def load_after(root_widget):
        import sys
