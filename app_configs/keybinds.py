from config_base import ConfigBase
from app_modules.key_binder.key_binder import KeyBinder


class Config(ConfigBase):

    @staticmethod
    def load_before(root):
        root.keybinder = KeyBinder()
        # root.keybinder.log_keys = True

    @staticmethod
    def load_after(root):
        root.keybinder.add(
            'vol_increase', '273', 'down',
            root.ids.playback_bar.volume_increase, modifier=['ctrl'])
        root.keybinder.add(
            'vol_decrease', '274', 'down',
            root.ids.playback_bar.volume_decrease, modifier=['ctrl'])
        root.keybinder.add(
            'seek_4_sec_back', '276', 'down',
            lambda: root.mPlayer.seek_relative(-4), modifier=['shift'])
        root.keybinder.add(
            'seek_4_sec_forward', '275', 'down',
            lambda: root.mPlayer.seek_relative(4), modifier=['shift'])
        root.keybinder.add(
            'seek_60_sec_back', '276', 'down',
            lambda: root.mPlayer.seek_relative(-60), modifier=['ctrl'])
        root.keybinder.add(
            'seek_60_sec_forward', '275', 'down',
            lambda: root.mPlayer.seek_relative(60), modifier=['ctrl'])
        root.keybinder.add(
            'play_pause_toggle', '32', 'down', root.media_control.play_pause)

        root.keybinder.add('toggle_terminal', '96', 'down',
                           root.ids.terminal_widget.toggle_pos_multiplier)
        root.keybinder.add('terminal_scroll_up', '280', 'down',
                          root.ids.terminal_widget.scroll_up)
        root.keybinder.add('terminal_scroll_down', '281', 'down',
                        root.ids.terminal_widget.scroll_down)
