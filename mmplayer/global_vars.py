from kivy.properties import NumericProperty, ListProperty
from kivy.event import EventDispatcher
from kivy.utils import platform
from kivy.metrics import cm, dp
from kivy.logger import Logger
from kivy.lang import Builder
from random import randrange
import os

DIR_HOME = os.path.expanduser("~")+'/'
if platform == 'linux':
    DIR_PLAYLISTS = '%s.config/github_bakterija/mmplayer/playlists/' % (
        DIR_HOME)
else:
    DIR_PLAYLISTS = '%sgithub_bakterija/mmplayer/playlists/' % (DIR_HOME)


def __set_app_globals__():
    col_grey = (0.4, 0.4, 0.4, 1)
    col_dgrey = (0.22, 0.22, 0.22, 1)
    col_ddgrey = (0.17, 0.17, 0.17, 1)
    col_bgrey = (0.83, 0.83, 0.83, 1)

    col_blue = (0.3, 0.4, 0.5, 1)
    col_bblue = (0.35, 0.45, 0.55, 1)
    col_bblue_transp06 = (0.35, 0.45, 0.55, 0.6)
    col_bbblue = (0.5, 0.6, 0.7, 1)
    col_bbbblue = (0.55, 0.65, 0.8, 1)
    col_dblue = (0.25, 0.35, 0.45, 1)
    col_dblue2 = (0.15, 0.25, 0.35, 1)
    col_satblue = (0.15, 0.25, 0.60, 1)
    col_satblue2 = (0.50, 0.50, 1, 1)
    col_satblue_dark = (0.22, 0.28, 0.50, 1)

    col_green = (0.3, 0.5, 0.4, 1)
    col_bgreen = (0.35, 0.55, 0.45, 1)
    col_satgreen = (0.15, 0.60, 0.25, 1)

    col_white = (0.9, 0.9, 0.9, 1)
    col_black = (0.1, 0.1, 0.1, 1)
    col_red = (0.8, 0.2, 0.2, 1)
    col_orange = (0.9, 0.6, 0.3, 1)

    col_ncolbg = (0.09, 0.09, 0.1, 1)

    button_height = int(cm(0.75))
    button_height20 = int(button_height * 2.0)
    button_height15 = int(button_height * 1.5)
    button_height12 = int(button_height * 1.2)
    button_height07 = int(button_height * 0.7)
    button_height05 = int(button_height * 0.5)

    playback_bar_height = int(button_height * 1.6)

    rv_default_height = button_height
    sidebar_section_height = int(button_height * 0.8)
    default_spacing = 1
    scroll_wheel_distance = (rv_default_height + default_spacing) * 2

    app_background = (0.10, 0.10, 0.10, 1)
    border_color = (0.20, 0.20, 0.20, 1)
    side_bar_color = app_background
    scrollbar_width = int(cm(0.5))
    scrollbar_color = (0.4, 0.4, 0.4, 1)
    scrollbar_inactive_color = (.4, .4, .4, .7)
    scrollbar_background = col_ncolbg

    globals().update(locals())
    for attr, value in locals().items():
        Builder.load_string('#: set %s %s' % (attr, value))

__set_app_globals__()


class LayoutManager(EventDispatcher):
    '''Global EventDispatcher for layout size values,
    almost all widgets bind on it's properties'''

    button_height = NumericProperty()
    button_height12 = NumericProperty()
    button_height05 = NumericProperty()
    button_height07 = NumericProperty()
    scrollbar_width = NumericProperty()
    playback_bar_height = NumericProperty()
    font_size = NumericProperty()
    spacing = NumericProperty()
    scale = NumericProperty()

    def __init__(self, **kwargs):
        super(LayoutManager, self).__init__(**kwargs)
        self.default_values = {
            'button_height': button_height,
            'button_height12': button_height12,
            'button_height05': button_height05,
            'button_height07': button_height07,
            'scrollbar_width': scrollbar_width,
            'font_size': button_height05,
            'playback_bar_height': playback_bar_height,
            'spacing': 1
        }
        self.scale = 1.0
        self.set_defaults()

    def set_defaults(self):
        for k, v in self.default_values.items():
            setattr(self, k , v)
        # self.button_height = button_height
        # self.button_height12 = button_height12
        # self.button_height05 = button_height05
        # self.button_height07 = button_height07
        # self.scrollbar_width = scrollbar_width
        # self.font_size = self.button_height05
        # self.playback_bar_height = playback_bar_height
        # self.spacing = 1

    def increase_scale(self):
        self.scale += 0.1

    def decrease_scale(self):
        self.scale -= 0.1

    def on_scale(self, _, value):
        Logger.info('LayoutManager: set scale to %s' % (value))
        self.set_defaults()
        for x in self.properties():
            if x != 'scale':
                def_val = self.default_values[x]
                new_val = int(def_val * self.scale)
                setattr(self, x, new_val)


class ThemeManager(EventDispatcher):
    '''Global EventDispatcher for theme color values,
    almost all widgets bind on it's properties'''
    
    col_btn_normal = ListProperty(col_dgrey)
    col_btn_down = ListProperty(col_satblue2)

    background0 = ListProperty((0, 0, 0, 1))
    # background1 = ListProperty(app_background)
    background2 = ListProperty((0.15, 0.15, 0.15, 1)) # context menu
    bar_color = ListProperty(app_background)
    bar_border = ListProperty(border_color)

    focus_border = ListProperty(col_bbbblue)
    col_theme0 = ListProperty(col_satblue2)
    col_theme1 = ListProperty(col_bbblue)
    col_theme2 = ListProperty(col_orange)
    col_text = ListProperty([0.9, 0.9, 0.9, 1])
    col_text_disabled = ListProperty([0.5, 0.5, 0.5, 1])
    scrollbar = ListProperty(scrollbar_color)
    scrollbar_background = ListProperty(col_ncolbg)

    def randomize(self):
        for x in self.properties():
            nc = self.get_random_color()
            setattr(self, x, nc)

    def randomize2(self):
        for x in self.properties():
            nc = self.get_random_color()
            setattr(self, x, nc)
        self.background0 = (1, 1, 1, 1)
        self.background2 = (1, 1, 1, 1)
        self.bar_color = (0.9, 0.9, 0.9, 1)
        self.bar_border = (0.3, 0.3, 0.3, 1)


    def get_random_color(self):
        rgb = [float(randrange(0, 255, 1)) / 255.0 for i in range(3)]
        rgb.append(1)
        return rgb


layout_manager = LayoutManager()
theme_manager = ThemeManager()
