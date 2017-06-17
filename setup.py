#!/usr/bin/env python
from setuptools import setup, find_packages
from distutils.core import setup
from kivy.config import Config
from kivy.logger import Logger
import sys
import os
# Avoid kivy log spam when importing main
# Config.set('kivy', 'log_level', 'error')
try:
    os.chdir('mmplayer/')
    sys.path.append(os.getcwd())
    from mmplayer.app import __version__, __author__, __author_email__
    from mmplayer.app import __description__, __url__, __icon_path__
    from mmplayer.utils import get_files
except Exception as e:
    Logger.exception('setup: %s' % (e))
    raise Exception(e)
Config.set('kivy', 'log_level', 'info')
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
