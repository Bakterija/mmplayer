from . import logs
from kivy.config import Config
Config.set('kivy', 'exit_on_escape', 0)
from kivy.app import App
from kivy.core.window import Window
from kivy_soil.terminal_widget import TerminalWidget
from kivy_soil.info_widget import InfoWidget
from kivy_soil import kb_system
from kivy_soil.kb_system import keys, focus
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty
from kivy.logger import Logger
from kivy.clock import Clock
from kivy.utils import platform


class TemplateApp(App):
    term_widget = ObjectProperty()
    info_widget = ObjectProperty()
    escape_presses = NumericProperty(0)
    '''Tracks escape press counts for kb_quit method'''

    use_template_theme = BooleanProperty(True)
    use_template_widgets = BooleanProperty(True)
    use_template_keybinds = BooleanProperty(True)
    _keybinds_were_inited = False

    def __init__(self, **kwargs):
        super(TemplateApp, self).__init__(**kwargs)
        if self.use_template_theme:
            Logger.info('TemplateApp: loading template app_style.kv')
            self.load_kv('kivy_soil/template_app/themes_layouts/app_style.kv')
        if self.use_template_widgets:
            Clock.schedule_once(self.init_template_widgets, 0)
        elif self.use_template_keybinds:
            self.init_keybinds()

    def init_template_widgets(self, *args):
        Logger.info('TemplateApp: initialising template widgets')
        self.load_kv('kivy_soil/template_app/themes_layouts/term_and_toast.kv')
        self.info_widget = InfoWidget()
        self.term_widget = TerminalWidget()
        for data in logs.LoggerHistoryProper.data:
            self.term_widget.add_data(data['text'], data['level'])
        logs.LoggerHistoryProper.bind(
            on_add_data=lambda obj, data: self.term_widget.add_data(
                data['text'], data['level']))

        Window.add_widget(self.term_widget)
        Window.add_widget(self.info_widget)
        self.init_keybinds()

    def init_keybinds(self):
        if not self._keybinds_were_inited:
            Logger.info('TemplateApp: initialising template keybinds')
            self._keybinds_were_inited = True
            kb_system.add(
                'quit', keys.ESC, 'down', self.kb_esc, modifier=['none'])
            kb_system.add('focus_next', keys.TAB, 'down', focus.focus_next,
                          modifier=['none'])

            if self.use_template_widgets:
                kb_system.add(
                    'toggle_terminal_small', keys.TILDE, 'down',
                    self.term_widget.animate_small, modifier=['none'])
                kb_system.add(
                    'toggle_terminal_big', keys.TILDE, 'down',
                    self.term_widget.animate_big, modifier=['ctrl'])
        else:
            Logger.info(('TemplateApp: init_keybinds:'
                         'were already initialised, skipping'))

    def display_info_toast(self, text):
        self.info_widget.info(text)

    def display_warning_toast(self, text):
        self.info_widget.warning(text)

    def display_error_toast(self, text):
        self.info_widget.error(text)

    def kb_esc(self):
        '''Updates self.escape_presses, quits app when reached target value'''
        cfocus = focus.current_focus
        if cfocus:
            focus.remove_focus()
        else:
            if self.escape_presses == 1:
                self.stop()
            else:
                self.display_info_toast('Double press escape to quit')
                self.escape_presses += 1
                Clock.unschedule(self.reset_escape_presses)
                Clock.schedule_once(self.reset_escape_presses, 0.8)

    def reset_escape_presses(self, *args):
        self.escape_presses = 0
