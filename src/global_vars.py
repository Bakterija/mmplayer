from kivy.metrics import cm, dp
from kivy.lang import Builder

def __set_app_globals__():
    col_grey = (0.4, 0.4, 0.4, 1)
    col_dgrey = (0.25, 0.25, 0.25, 1)
    col_ddgrey = (0.17, 0.17, 0.17, 1)
    col_bgrey = (0.83, 0.83, 0.83, 1)

    col_blue = (0.3, 0.4, 0.5, 1)
    col_bblue = (0.35, 0.45, 0.55, 1)
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

    logview_font_size = int(cm(0.4))
    logview_height = int(cm(2.2))
    scrollview_bar_width = int(cm(0.6))

    side_bar_color = (0.1, 0.1, 0.1, 1)

    globals().update(locals())
    for attr, value in locals().items():
        Builder.load_string('#: set %s %s' % (attr, value))

__set_app_globals__()
