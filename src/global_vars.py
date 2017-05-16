from kivy.metrics import cm, dp
from kivy.lang import Builder
from kivy.utils import platform
from kivy.event import EventDispatcher
from kivy.properties import NumericProperty, ListProperty
import os

DIR_HOME = os.path.expanduser("~")+'/'
if platform == 'linux':
    DIR_PLAYLISTS = '%s.config/github_bakterija/mmplayer/playlists/' % (
        DIR_HOME)
else:
    DIR_PLAYLISTS = '%sgithub_bakterija/mmplayer/playlists/' % (DIR_HOME)


def __set_app_globals__():
    col_grey = (0.4, 0.4, 0.4, 1)
    col_dgrey = (0.25, 0.25, 0.25, 1)
    col_ddgrey = (0.17, 0.17, 0.17, 1)
    col_bgrey = (0.83, 0.83, 0.83, 1)

    col_blue = (0.3, 0.4, 0.5, 1)
    col_bblue = (0.35, 0.45, 0.55, 1)
    col_bblue_transp06 = (0.35, 0.45, 0.55, 0.6)
    col_bbblue = (0.5, 0.6, 0.7, 1)
    col_dblue = (0.25, 0.35, 0.45, 1)
    col_dblue2 = (0.15, 0.25, 0.35, 1)
    col_satblue = (0.15, 0.25, 0.60, 1)

    col_green = (0.3, 0.5, 0.4, 1)
    col_bgreen = (0.35, 0.55, 0.45, 1)
    col_satgreen = (0.15, 0.60, 0.25, 1)

    col_white = (0.9, 0.9, 0.9, 1)
    col_black = (0.1, 0.1, 0.1, 1)
    col_red = (0.8, 0.2, 0.2, 1)

    col_ncolbg = (0.09, 0.09, 0.1, 1)

    button_height = int(cm(0.7))
    button_height20 = int(button_height * 2.0)
    button_height15 = int(button_height * 1.5)
    button_height05 = int(button_height * 0.5)
    lower_bar_height = int(button_height * 1.6)
    rv_default_height = button_height
    sidebar_section_height = int(button_height * 0.8)
    default_spacing = 1
    scroll_wheel_distance = (rv_default_height + default_spacing) * 2

    app_background = (0.10, 0.10, 0.10, 1)
    border_color0 = (0.32, 0.32, 0.32)
    side_bar_color = app_background
    scrollbar_width = int(cm(0.5))
    scrollbar_color = (0.4, 0.4, 0.4, 1)
    scrollbar_inactive_color = (.4, .4, .4, .7)
    scrollbar_background = col_ncolbg

    globals().update(locals())
    for attr, value in locals().items():
        Builder.load_string('#: set %s %s' % (attr, value))

__set_app_globals__()


class ThemeManager(EventDispatcher):
    btn_height = NumericProperty(button_height)
    btn_height05 = NumericProperty(button_height05)
    background2 = ListProperty(col_dgrey)
    col_text = ListProperty([0.9, 0.9, 0.9, 1])
    col_text_disabled = ListProperty([0.5, 0.5, 0.5, 1])

theme_manager = ThemeManager()
