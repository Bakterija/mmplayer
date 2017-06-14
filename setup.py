#!/usr/bin/env python
from kivy.config import Config
# Avoid kivy log spam when importing main
Config.set('kivy', 'log_level', 'error')
from mmplayer.main import __version__, __author__, __author_email__
from mmplayer.main import __description__, __url__, __icon_path__
from mmplayer.utils import get_files
Config.set('kivy', 'log_level', 'debug')
from setuptools import setup, find_packages
from distutils.core import setup
import os
os.chdir('..')

packages = find_packages()

setup(
    name='mmplayer',
    version=__version__,
    description=__description__,
    author=__author__,
    author_email=__author_email__,
    url=__url__,
    packages=packages,
    install_requires=['kivy'],
    package_data={'': ['data/*.png', 'data/*.wav', '*.kv', 'data/4/*',
                       'data/volume/*', 'data/material/*']},
    entry_points={
        'console_scripts': [
            'mmplayer = %s.main.main_loop' % ('mmplayer'),
        ]
})
