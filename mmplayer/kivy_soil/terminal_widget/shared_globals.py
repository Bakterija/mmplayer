from kivy.utils import platform
import os

DIR_HOME = os.path.expanduser("~")
APP_NAME = 'UNNAMED_APP'
if platform == 'linux':
    DIR_CONF = '%s/.config/github_bakterija/terminal_widget' % (DIR_HOME)
else:
    DIR_CONF = '%s/github_bakterija/terminal_widget' % (DIR_HOME)
DIR_FUNCTIONS = '%s/_functions/' % (DIR_CONF)
DIR_APP = '%s/%s/' % (DIR_CONF, APP_NAME)
for x in (DIR_CONF, DIR_FUNCTIONS, DIR_APP):
    if not os.path.exists(x):
        os.makedirs(x)


def set_app_name(name):
    global DIR_APP, APP_NAME
    APP_NAME = name
    DIR_APP = '%s/%s' % (DIR_CONF, APP_NAME)
    if not os.path.exists(DIR_APP):
        os.makedirs(DIR_APP)
