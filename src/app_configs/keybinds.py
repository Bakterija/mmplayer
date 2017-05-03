from app_modules.behaviors.focus import focus as focus_behavior
from app_modules import key_binder as kbinder
from .config_base import ConfigBase
from kivy.app import App

class Config(ConfigBase):

    @staticmethod
    def load_before(root):
        pass

    @staticmethod
    def load_after(root):
        app = App.get_running_app()
        # kbinder.log_keys = True

        kbinder.add('quit', 27, 'down', app.kb_esc)
        kbinder.add('focus_next', 9, 'down', focus_behavior.focus_next)

        kbinder.add(
            'vol_increase', '273', 'down',
            root.ids.playback_bar.volume_increase, modifier=['ctrl'])
        kbinder.add(
            'vol_decrease', '274', 'down',
            root.ids.playback_bar.volume_decrease, modifier=['ctrl'])
        kbinder.add(
            'seek_4_sec_back', '276', 'down',
            lambda: root.mplayer.seek_relative(-4), modifier=['shift'])
        kbinder.add(
            'seek_4_sec_forward', '275', 'down',
            lambda: root.mplayer.seek_relative(4), modifier=['shift'])
        kbinder.add(
            'seek_60_sec_back', '276', 'down',
            lambda: root.mplayer.seek_relative(-60), modifier=['ctrl'])
        kbinder.add(
            'seek_60_sec_forward', '275', 'down',
            lambda: root.mplayer.seek_relative(60), modifier=['ctrl'])
        kbinder.add(
            'play_pause_toggle', '32', 'down', root.media_control.play_pause)

        kbinder.add('toggle_terminal', '96', 'down',
                           root.ids.terminal_widget.toggle_pos_multiplier)
        kbinder.add('terminal_scroll_up', '280', 'down',
                          root.ids.terminal_widget.scroll_up)
        kbinder.add('terminal_scroll_down', '281', 'down',
                        root.ids.terminal_widget.scroll_down)
