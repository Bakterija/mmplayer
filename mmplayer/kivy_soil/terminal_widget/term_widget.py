from __future__ import print_function
from kivy.properties import ListProperty, NumericProperty, ObjectProperty
from kivy.properties import StringProperty
from kivy_soil.kb_system.canvas import FocusBehaviorCanvas
from kivy_soil.kb_system import keys
from kivy_soil.app_recycleview.behaviors.line_split import LineSplitBehavior
from kivy_soil.app_recycleview import AppRecycleViewClass
from kivy_soil.app_recycleview import AppRecycleView
from .term_system import TerminalWidgetSystem
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.metrics import cm
from kivy.app import App

kv = '''
<TerminalWidget>:
    orientation: 'vertical'
    size_hint: None, None
    input_height: int(cm(0.8))
    anim_speed: 0.2
    canvas:
        Color:
            rgba: self.background_color
        Rectangle:
            size: self.size
            pos: self.pos

    TerminalWidgetScroller:
        id: rv
        viewclass: 'TerminalWidgetLabel'
        SingleSelectRecycleBox:
            id: rv_box
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
        font_name: root.font_name
        ignored_keys: [9, 96]
        border_width: 1
        height: root.input_height
        font_size: int(root.input_height * 0.5)
        multiline: False
        on_text_validate: root.on_input(self, self.text)
'''

class TerminalWidgetScroller(FocusBehaviorCanvas, LineSplitBehavior,
                             AppRecycleView):
    is_focusable = False

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
    font_name = StringProperty('RobotoMono-Regular.ttf')
    background_color = ListProperty([0.2, 0.2, 0.2, 0.9])
    small_size = ListProperty([100, 100])
    big_size = ListProperty([100, 100])
    selected_size = StringProperty('')
    pos_multiplier = NumericProperty()
    term_system = ObjectProperty()
    font_size = NumericProperty()
    global_objects = {
        'app': App.get_running_app(),
    }

    def __init__(self, **kwargs):
        super(TerminalWidget, self).__init__(**kwargs)
        Clock.schedule_once(self.init_widgets, 0)
        self.is_focusable = False
        self._temp_init_data = []

    def on_small_size(self, _, value):
        if self.selected_size == 'small':
            self.size = value

    def on_big_size(self, _, value):
        if self.selected_size == 'big':
            self.size = value

    def on_selected_size(self, _, value):
        if value == 'big':
            self.on_big_size(None, self.big_size)
        elif value == 'small':
            self.on_big_size(None, self.small_size)

    def add_data(self, text, level=None):
        if self.term_system:
            self.term_system.add_text(text, level=level)
        else:
            self._temp_init_data.append((text, level))

    def update_chars_per_line(self, _, font_size):
        self.ids.rv.chars_per_line = int((self.width / font_size) * 90)

    def update_rv_box_font_name(self, _, value):
        for child in self.ids.rv_box.children:
            child.font_name = self.font_name

    def init_widgets(self, dt):
        rv = self.ids.rv
        inputw = self.ids.input
        inputw.is_focusable = False
        inputw.grab_focus = True
        rv_box = self.ids.rv_box
        self.fbind('font_size', self.update_chars_per_line)
        self.fbind('font_name', self.update_rv_box_font_name)
        rv_box.bind(children=self.update_rv_box_font_name)

        self.term_system = TerminalWidgetSystem(self)
        self.term_system.bind(data=lambda obj, val: self.ids.rv.set_data(val))
        self.term_system.bind(
            on_data=lambda obj, val: self.ids.rv.set_data(val))

        rv.bind(width=self.update_chars_per_line)
        rv.set_data(self.term_system.data)
        rv.input_widget = inputw
        self.update_chars_per_line(None, self.font_size)
        inputw.keyboard_on_key_down = self.on_input_key_down
        for text, level in self._temp_init_data:
            self.add_data(text, level=level)
        del self._temp_init_data

    def on_input_key_down(self, _, key, text, modifiers):
        inputw = self.ids.input
        if key[0] in (keys.PAGE_UP, keys.PAGE_DOWN):
            self.ids.rv.on_key_down(key[0], modifiers)
        elif key[0] == keys.TAB:
            text = self.term_system.try_autocomplete(
                inputw.text, inputw.cursor_index())
            inputw.insert_text(text)
        elif key[0] == keys.UP:
            text = self.term_system.get_log_previous()
            inputw.text = text
        elif key[0] == keys.DOWN:
            text = self.term_system.get_log_next()
            inputw.text = text
        elif key[0] == keys.C and modifiers == ['ctrl']:
            self.term_system.keyboard_interrupt()
            inputw.text = ''
        else:
            inputw.__class__.keyboard_on_key_down(
                inputw, _, key, text, modifiers)

    def animate_in_small(self, *args):
        self.size = self.small_size
        anim = Animation(pos_multiplier=1.0, d=self.anim_speed, t='out_quad')
        Clock.schedule_once(self.focus_input, 0)
        self.ids.input.is_focusable = True
        self.ids.rv.scroll_to_end()
        anim.start(self)
        self.selected_size = 'small'

    def animate_in_big(self, *args):
        self.size = self.big_size
        anim = Animation(pos_multiplier=1.0, d=self.anim_speed, t='out_quad')
        Clock.schedule_once(self.focus_input, 0)
        self.ids.input.is_focusable = True
        self.ids.rv.scroll_to_end()
        anim.start(self)
        self.selected_size = 'big'

    def animate_out(self, *args):
        anim = Animation(pos_multiplier=0.0, d=self.anim_speed, t='in_quad')
        self.ids.input.focus = False
        self.ids.input.is_focusable = False
        anim.start(self)
        self.selected_size = ''

    def animate_big(self, *args):
        if self.pos_multiplier == 0.0 or self.size == self.small_size:
            self.animate_in_big()
        elif self.pos_multiplier == 1.0:
            self.animate_out()

    def animate_small(self, *args):
        if self.pos_multiplier == 1.0:
            self.animate_out()
        elif self.pos_multiplier == 0.0:
            self.animate_in_small()

    def on_input(self, widget, text):
        Clock.schedule_once(self.focus_input, 0)
        self.term_system.handle_input(text)
        widget.text = ''

    def focus_input(self, text):
        if self.ids.input.is_focusable:
            self.ids.input.focus = True


Builder.load_string(kv)
