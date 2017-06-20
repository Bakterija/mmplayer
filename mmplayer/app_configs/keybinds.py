from kivy_soil.kb_system import focus as focus_behavior
from .config_base import ConfigBase
from kivy_soil.kb_system import keys
from kivy.app import App
from kivy_soil import kb_system

class Config(ConfigBase):

    @staticmethod
    def load_before(root):
        pass

    @staticmethod
    def load_after(root):
        app = App.get_running_app()
        # kb_system.log_keys = True

        kb_system.add(
            'theme_randomize', keys.NUM_MULTIPLY, 'down', app.mtheme.randomize,
            modifier=['none'])
        kb_system.add(
            'theme_reset', keys.NUM_MULTIPLY, 'down', app.mtheme.set_defaults,
            modifier=['ctrl'])

        kb_system.add(
            'gui_scale+', keys.NUM_PLUS, 'down', app.mlayout.increase_scale,
            modifier=['ctrl'])
        kb_system.add(
            'gui_scale-', keys.NUM_MINUS, 'down', app.mlayout.decrease_scale,
            modifier=['ctrl'])

        kb_system.add('add_playlist', keys.N, 'down',
                      root.mgui_add_playlist, modifier=['ctrl'])

        kb_system.add('quit', keys.ESC, 'down', app.kb_esc)
        kb_system.add(
            'focus_next', keys.TAB, 'down', focus_behavior.focus_next)

        kb_system.add(
            'focus_filter', keys.L, 'down',
            root.manager.ids.media_filter_widget.focus_input,
            modifier=['ctrl'])

        screenbinds = (
            (keys.N1, 'main'), (keys.N2, 'queue'),
            (keys.N3, 'media'), (keys.N4, 'video'))
        for key, name in screenbinds:
            kb_system.add(
                'screen_switch_%s' % (name), key, 'down',
                lambda key=key, name=name: root.switch_screen(name),
                modifier=['alt'])

        kb_system.add(
            'jump_to_current', keys.J, 'down',
            root.jump_to_current, modifier=['ctrl'])

        kb_system.add(
            'vol_increase', keys.UP, 'down',
            root.media_control.volume_increase, modifier=['ctrl'])
        kb_system.add(
            'vol_decrease', keys.DOWN, 'down',
            root.media_control.volume_decrease, modifier=['ctrl'])
        kb_system.add(
            'mplayer_previous', keys.LEFT, 'down',
            root.mplayer_previous, modifier=['alt'])
        kb_system.add(
            'mplayer_next', keys.RIGHT, 'down',
            root.mplayer_next, modifier=['alt'])
        kb_system.add(
            'seek_4_sec_back', keys.LEFT, 'down',
            lambda: root.mplayer_seek_relative(-4), modifier=['shift'])
        kb_system.add(
            'seek_4_sec_forward', keys.RIGHT, 'down',
            lambda: root.mplayer_seek_relative(4), modifier=['shift'])
        kb_system.add(
            'seek_60_sec_back', keys.LEFT, 'down',
            lambda: root.mplayer_seek_relative(-60), modifier=['ctrl'])
        kb_system.add(
            'seek_60_sec_forward', keys.RIGHT, 'down',
            lambda: root.mplayer_seek_relative(60), modifier=['ctrl'])
        kb_system.add(
            'play_pause_toggle', keys.SPACE, 'down',
            root.media_control.play_pause)

        kb_system.add(
            'toggle_terminal', keys.TILDE, 'down',
            root.ids.terminal_widget.toggle_pos_multiplier)
