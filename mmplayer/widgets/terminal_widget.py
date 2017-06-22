from kivy.properties import ListProperty, NumericProperty
from kivy_soil.kb_system.canvas import FocusBehaviorCanvas
from kivy_soil.kb_system import keys
from kivy_soil.app_recycleview import AppRecycleView
from kivy_soil.app_recycleview import AppRecycleViewClass
from kivy.logger import Logger, LoggerHistory
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.metrics import cm


kv = '''
#: import TerminalWidgetLabel widgets.terminal_widget_label.TerminalWidgetLabel
<TerminalWidget>:
    orientation: 'vertical'
    size_hint: None, None
    input_height: int(cm(0.8))
    anim_speed: 0.2
    canvas:
        Color:
            rgba: 0.2, 0.2, 0.2, 0.9
        Rectangle:
            size: self.size
            pos: self.pos

    TerminalWidgetScroller:
        id: rv
        grab_focus: True
        subfocus_widgets: [input]
        viewclass: 'TerminalWidgetLabel'
        SingleSelectRecycleBox:
            orientation: 'vertical'
            size_hint: None, None
            height: self.minimum_height
            width: self.parent.width - self.parent.bar_width
            default_size_hint: 1, None
            default_size: None, app.mlayout.button_height07
            spacing: app.mlayout.spacing

    CompatTextInput:
        id: input
        size_hint_y: None
        is_subfocus: True
        ignored_keys: [9, 96]
        height: root.input_height
        font_size: self.height * 0.5
        multiline: False
        background_active: ''
        background_normal: ''
        background_disabled_normal: ''
        # foreground_color: 1, 1, 1, 1
        # cursor_color: 1, 1, 1, 1
        background_color: (0.3, 0.3, 0.8, 0.15)
        on_text_validate: root.on_input(self, self.text)
'''

class TerminalWidgetScroller(FocusBehaviorCanvas, AppRecycleView):
    def on_key_down(self, key, modifier):
        box = self.children[0]
        if key == keys.PAGE_UP:
            self.page_up()
        elif key == keys.PAGE_DOWN:
            self.page_down()
        elif key == keys.HOME:
            self.scroll_to_start()
        elif key == keys.END:
            self.scroll_to_end()


class TerminalWidget(BoxLayout):
    data = ListProperty()
    pos_multiplier = NumericProperty()
    input_callback = None

    def __init__(self, **kwargs):
        super(TerminalWidget, self).__init__(**kwargs)
        Clock.schedule_once(self.after_init, 0.5)
        self.is_focusable = False

    def after_init(self, *args):
        self.fbind('data', self.ids.rv.setter('data'))
        histo = LoggerHistory()
        for x in histo.history:
            self.data.append({'text': str(x.msg)})

    def enter(self, *args):
        self.ids.rv.is_focusable = True
        anim = Animation(pos_multiplier=1.0, d=self.anim_speed, t='out_quad')
        self.ids.rv.scroll_to_end()
        Clock.schedule_once(self.focus_input, 0)
        anim.start(self)

    def leave(self, *args):
        self.ids.rv.is_focusable = False
        anim = Animation(pos_multiplier=0.0, d=self.anim_speed, t='in_quad')
        anim.start(self)
        self.ids.input.focus = False

    def toggle_pos_multiplier(self, *args):
        if self.pos_multiplier == 1.0:
            self.leave()
        elif self.pos_multiplier == 0.0:
            self.enter()

    def on_input(self, widget, text):
        if self.input_callback:
            self.input_callback(self, widget, text)
        widget.text = ''
        Clock.schedule_once(self.focus_input, 0)

    def focus_input(self, text):
        self.ids.input.focus = True


Builder.load_string(kv)
