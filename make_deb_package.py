from __future__ import print_function
from kivy.config import Config
from kivy.logger import Logger
from zipfile import ZipFile
import subprocess
import shutil
import sys
import os

# Avoid kivy log spam when importing main
Config.set('kivy', 'log_level', 'error')
try:
    os.chdir('mmplayer/')
    sys.path.append(os.getcwd())
    from mmplayer.app import __version__, __author__, __author_email__
    from mmplayer.app import __description__, __url__, __icon_path__
except Exception as e:
    Logger.exception('make_deb_package: %s' % (e))
    raise Exception(e)
Config.set('kivy', 'log_level', 'info')
os.chdir('..')

Logger.info('Running setup.py')
subprocess.check_call(['python', 'setup.py', 'bdist', '--format=zip'])
Logger.info('Done setup.py')

APP_NAME = 'mmplayer'
APP_VERSION = str(__version__)
DIR_ROOT = '{}_{}'.format(APP_NAME, APP_VERSION)
DIR_APP = '{}/'.format(DIR_ROOT)
DIR_APP_INSTALL = '/usr/local/share/{}'.format(APP_NAME)
DIR_BIN0 = '/usr/local/bin'
DIR_BIN = '{}{}'.format(DIR_ROOT, DIR_BIN0)
DIR_SHARE = '{}/usr/local/share'.format(DIR_ROOT)
DIR_APPS = '{}/usr/share/applications'.format(DIR_ROOT)
DIR_DEBIAN = '{}/DEBIAN'.format(DIR_ROOT)
PATH_DESKTOP_FILE = '{}/{}.desktop'.format(DIR_APPS, APP_NAME)
PATH_BIN_LAUNCHER = '{}/{}'.format(DIR_BIN, APP_NAME)
PATH_DEBIAN_CONTROL = '{}/control'.format(DIR_DEBIAN)
PATH_DEBIAN_POSTINST = '{}/postinst'.format(DIR_DEBIAN)
PATH_EXEC = '/usr/local/bin/mmplayer'
PATH_ICON = '{}/{}'.format(DIR_APP, __icon_path__)
MAKEDIRS = (DIR_BIN, DIR_SHARE, DIR_APPS, DIR_DEBIAN)

if os.path.exists(DIR_ROOT):
    shutil.rmtree(DIR_ROOT)

for d in MAKEDIRS:
    if not os.path.exists(d):
        os.makedirs(d)
        Logger.info('Made missing dir {}'.format(d))

fzip = 'mmplayer-11.0.linux-x86_64.zip'
path_fzip = 'dist/%s' % (fzip)
Logger.info('Extracting {} into {}'.format(path_fzip, DIR_APP))
fzip = ZipFile(path_fzip)
fzip.extractall(path=DIR_APP)
Logger.info('Extracting done')

class TextFile(object):
    path_open = ''
    path_save = ''
    chmod = 0
    replacables = (
        ('%APP_NAME%', APP_NAME), ('%DESCRIPTION%', __description__),
        ('%AUTHOR%', __author__), ('%AUTHOR_EMAIL%', __author_email__),
        ('%PATH_ICON%', PATH_ICON),
        ('%APP_VERSION%', APP_VERSION), ('%VERSION%', APP_VERSION),
        ('%PATH_BIN_LAUNCHER%', PATH_BIN_LAUNCHER),
        ('%PATH_EXEC%', PATH_EXEC)
    )

    def __init__(self, path_open, path_save, chmod=0):
        self.path_open = path_open
        self.path_save = path_save
        self.chmod = chmod

    def do_it(self):
        with open(self.path_open, 'r') as f:
            text = f.read()
        for a, b in self.replacables:
            text = text.replace(a, b)
        with open(self.path_save, 'w') as f:
            f.write(text)
        text_lines = text.splitlines()
        for i, x in enumerate(text_lines):
            if x.find('%') != -1:
                Logger.warning(''.join(
                    'TextFile: % character still remains in line '
                    '{} of file {}: "{}"'.format(i, self.path_open, x)
                    ))
        if self.chmod:
            cmd = ('chmod', str(self.chmod), self.path_save)
            Logger.info('TextFile: subprocess {}'.format(' '.join(cmd)))
            subprocess.call(cmd)

Logger.info('Parsing and saving launchers, text files')
res_linux = 'resources/linux/'
TEXT_LAUNCHER = TextFile(
    '%s/launcher.in' % (res_linux), PATH_BIN_LAUNCHER).do_it()
TEXT_DESKTOP_FILE = TextFile(
    '%s/mmplayer.desktop.in' % (res_linux), PATH_DESKTOP_FILE).do_it()
TEXT_DEBIAN = TextFile(
    '%s/debian_control.in' % (res_linux), PATH_DEBIAN_CONTROL).do_it()
TEXT_POSTINST = TextFile(
    '%s/postinst.in' % (res_linux), PATH_DEBIAN_POSTINST, chmod=555).do_it()
Logger.info('Done')

cmd_dpkg = ('dpkg-deb', '--build', DIR_ROOT)
Logger.info('Running {}'.format(' '.join(cmd_dpkg)))
subprocess.call(cmd_dpkg)

Logger.info('Cleaning up')
for x in ('build', DIR_ROOT, APP_NAME + '.egg-info'):
    if os.path.exists(x):
        shutil.rmtree(x)

deb_name = '%s_%s.deb' % (APP_NAME, APP_VERSION)
shutil.move(deb_name, 'dist/' + deb_name)
Logger.info('Done')
