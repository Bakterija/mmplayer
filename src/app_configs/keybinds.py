from app_modules.behaviors.focus import focus as focus_behavior
from app_modules import key_binder as kbinder
from .config_base import ConfigBase
from app_modules import keys
from kivy.app import App

class Config(ConfigBase):

    @staticmethod
    def load_before(root):
        pass

    @staticmethod
    def load_after(root):
        app = App.get_running_app()
        # kbinder.log_keys = True

        kbinder.add('quit', keys.ESC, 'down', app.kb_esc)
        kbinder.add('focus_next', keys.TAB, 'down', focus_behavior.focus_next)

        kbinder.add(
            'focus_filter', keys.L, 'down',
            root.manager.ids.media_filter_widget.focus_input,
            modifier=['ctrl'])

        screenbinds = (
            (keys.N1, 'main'), (keys.N2, 'queue'),
            (keys.N3, 'media'), (keys.N4, 'video'))
        for key, name in screenbinds:
            kbinder.add(
                'screen_switch_%s' % (name), key, 'down',
                lambda key=key, name=name: root.switch_screen(name),
                modifier=['alt'])

        kbinder.add(
            'jump_to_current', keys.J, 'down',
            root.jump_to_current, modifier=['ctrl'])

        kbinder.add(
            'vol_increase', keys.UP, 'down',
            root.ids.playback_bar.volume_increase, modifier=['ctrl'])
        kbinder.add(
            'vol_decrease', keys.DOWN, 'down',
            root.ids.playback_bar.volume_decrease, modifier=['ctrl'])
        kbinder.add(
            'mplayer_previous', keys.LEFT, 'down',
            root.mplayer_previous, modifier=['alt'])
        kbinder.add(
            'mplayer_next', keys.RIGHT, 'down',
            root.mplayer_next, modifier=['alt'])
        kbinder.add(
            'seek_4_sec_back', keys.LEFT, 'down',
            lambda: root.mplayer_seek_relative(-4), modifier=['shift'])
        kbinder.add(
            'seek_4_sec_forward', keys.RIGHT, 'down',
            lambda: root.mplayer_seek_relative(4), modifier=['shift'])
        kbinder.add(
            'seek_60_sec_back', keys.LEFT, 'down',
            lambda: root.mplayer_seek_relative(-60), modifier=['ctrl'])
        kbinder.add(
            'seek_60_sec_forward', keys.RIGHT, 'down',
            lambda: root.mplayer_seek_relative(60), modifier=['ctrl'])
        kbinder.add(
            'play_pause_toggle', keys.SPACE, 'down', root.media_control.play_pause)

        kbinder.add('toggle_terminal', keys.TILDE, 'down',
                           root.ids.terminal_widget.toggle_pos_multiplier)
        kbinder.add('terminal_scroll_up', keys.PAGE_UP, 'down',
                          root.ids.terminal_widget.scroll_up)
        kbinder.add('terminal_scroll_down', keys.PAGE_DOWN, 'down',
                        root.ids.terminal_widget.scroll_down)
