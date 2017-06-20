from kivy.properties import NumericProperty, ListProperty
from utils.settings import SettingHandler
from kivy.event import EventDispatcher
from kivy.utils import platform
from kivy.metrics import cm, dp
from kivy.logger import Logger
from kivy.lang import Builder
from random import randrange
import os

DIR_HOME = os.path.expanduser("~")+'/'
if platform == 'linux':
    DIR_CONF = '%s.config/github_bakterija' % (DIR_HOME)
    DIR_PLAYLISTS = '%s/mmplayer/playlists/' % (DIR_CONF)
else:
    DIR_CONF = '%sgithub_bakterija' % (DIR_HOME)
    DIR_PLAYLISTS = '%s/mmplayer/playlists/' % (DIR_CONF)


def __set_app_globals__():
    col_grey =           (0.40, 0.40, 0.40, 1)
    col_dgrey =          (0.22, 0.22, 0.22, 1)
    col_ddgrey =         (0.17, 0.17, 0.17, 1)
    col_bgrey =          (0.83, 0.83, 0.83, 1)

    col_blue =           (0.30, 0.40, 0.50, 1)
    col_bblue =          (0.35, 0.45, 0.55, 1)
    col_bblue_transp06 = (0.35, 0.45, 0.55, 0.6)
    col_bbblue =         (0.50, 0.60, 0.70, 1)
    col_bbbblue =        (0.55, 0.65, 0.80, 1)
    col_dblue =          (0.25, 0.35, 0.45, 1)
    col_dblue2 =         (0.15, 0.25, 0.35, 1)
    col_satblue =        (0.15, 0.25, 0.60, 1)
    col_satblue2 =       (0.50, 0.50, 1.00, 1)
    col_satblue3 =       (0.00, 0.66, 1.00, 1)
    col_satblue_dark =   (0.22, 0.28, 0.50, 1)

    col_green =          (0.30, 0.50, 0.40, 1)
    col_bgreen =         (0.35, 0.55, 0.45, 1)
    col_satgreen =       (0.15, 0.60, 0.25, 1)

    col_white =          (0.90, 0.90, 0.90, 1)
    col_black =          (0.10, 0.10, 0.10, 1)
    col_red =            (0.80, 0.20, 0.20, 1)
    col_orange =         (0.90, 0.60, 0.30, 1)

    col_ncolbg =         (0.09, 0.09, 0.1, 1)

    col_media_normal =   (0.20, 0.20, 0.40, 1)
    col_media_playing =  (0.50, 0.15, 0.30, 1)
    col_media_hover =    (0.40, 0.45, 0.40, 1)
    col_media_selected = (0.2, 0.4, 0.7, 0.45)
    col_media_disabled = (0.20, 0.20, 0.20, 1)
    col_media_error =    (0.10, 0.05, 0.05, 1)
    col_media_folder =   (0.20, 0.20, 0.20, 1)

    app_background =     (0.10, 0.10, 0.10, 1)
    border_color =       (0.20, 0.20, 0.20, 1)
    side_bar_color =     app_background
    scrollbar_color =    (0.4, 0.4, 0.4, 1)
    scrollbar_inactive_color = (.4, .4, .4, .7)
    scrollbar_background = col_ncolbg

    scrollbar_width =    int(cm(0.5))
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


    globals().update(locals())
    lc = locals().items()
    bstring = '\n'.join(['#: set %s %s' % (attr, value) for attr, value in lc])
    Builder.load_string(bstring)

__set_app_globals__()


class LayoutManager(SettingHandler, EventDispatcher):
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
    sidebar_width = NumericProperty()
    scale = NumericProperty()

    def __init__(self, **kwargs):
        super(LayoutManager, self).__init__(**kwargs)
        self.defaults = {
            'button_height': button_height,
            'button_height12': button_height12,
            'button_height05': button_height05,
            'button_height07': button_height07,
            'scrollbar_width': scrollbar_width,
            'font_size': button_height05,
            'playback_bar_height': playback_bar_height,
            'sidebar_width': int(cm(4)),
            'spacing': 1,
            'scale': 1.0
        }
        self.set_defaults()
        self.store_properties = self.defaults.items()
        self.store_name = 'LayoutManager'
        self.update_store_properties()

    def set_defaults(self):
        for k, v in self.defaults.items():
            setattr(self, k , v)

    def increase_scale(self):
        self.scale += 0.1

    def decrease_scale(self):
        self.scale -= 0.1

    def on_scale(self, _, value):
        Logger.info('LayoutManager: set scale to %s' % (value))
        for k, v in self.defaults.items():
            if k != 'scale':
                setattr(self, k , v)
        for x in self.properties():
            if x != 'scale':
                def_val = self.defaults[x]
                new_val = int(def_val * self.scale)
                setattr(self, x, new_val)


class ThemeManager(SettingHandler, EventDispatcher):
    '''Global EventDispatcher for theme color values,
    almost all widgets bind on it's properties'''

    button_normal = ListProperty(col_dgrey)
    button_down = ListProperty(col_satblue3)
    button_hover = ListProperty((0.38, 0.99, 1.00, 1))

    background0 = ListProperty((0, 0, 0, 1))
    # background1 = ListProperty(app_background)
    background2 = ListProperty((0.15, 0.15, 0.15, 1)) # context menu
    bar_color = ListProperty(app_background)
    bar_border = ListProperty(border_color)

    focus_border = ListProperty(col_bbbblue)
    col_theme0 = ListProperty(col_satblue2)
    col_theme1 = ListProperty(col_bbblue)
    col_theme2 = ListProperty(col_orange)
    text = ListProperty([0.9, 0.9, 0.9, 1])
    text_disabled = ListProperty([0.5, 0.5, 0.5, 1])

    media_normal = ListProperty(col_media_normal)
    media_playing = ListProperty(col_media_playing)
    media_hover = ListProperty(col_media_hover)
    media_selected = ListProperty(col_media_selected)
    media_disabled = ListProperty(col_media_disabled)
    media_error = ListProperty(col_media_error)

    scrollbar = ListProperty(scrollbar_color)
    scrollbar_inactive = ListProperty(scrollbar_inactive_color)
    scrollbar_background = ListProperty(col_ncolbg)

    def __init__(self, **kwargs):
        super(ThemeManager, self).__init__(**kwargs)
        self.store_properties = [
            ('button_normal', col_dgrey),
            ('button_down', col_satblue3),
            ('button_hover', (0.38, 0.99, 1.00, 1)),
            ('background0', (0, 0, 0, 1)),
            ('background2', (0.15, 0.15, 0.15, 1)),
            ('bar_color', app_background),
            ('bar_border', border_color),
            ('focus_border', col_bbbblue),
            ('col_theme0', col_satblue2),
            ('col_theme1', col_bbblue),
            ('col_theme2', col_orange),
            ('text', (0.9, 0.9, 0.9, 1)),
            ('text_disabled', (0.5, 0.5, 0.5, 1)),
            ('media_normal', col_media_normal),
            ('media_playing', col_media_playing),
            ('media_hover', col_media_hover),
            ('media_selected', col_media_selected),
            ('media_disabled', col_media_disabled),
            ('media_error', col_media_error),
            ('scrollbar', scrollbar_color),
            ('scrollbar_inactive', scrollbar_inactive_color),
            ('scrollbar_background', col_ncolbg)
        ]
        self.store_name = 'ThemeManager'
        self.update_store_properties()

    def set_defaults(self):
        for attr, value in self.store_properties:
            setattr(self, attr, value)

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
