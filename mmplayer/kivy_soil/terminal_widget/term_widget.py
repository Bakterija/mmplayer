from __future__ import print_function
from kivy.properties import ListProperty, NumericProperty, ObjectProperty
from kivy.properties import StringProperty, BooleanProperty
from kivy_soil.kb_system.canvas import FocusBehaviorCanvas
from kivy_soil.kb_system import keys
from kivy_soil.app_recycleview.behaviors.line_split import LineSplitBehavior
from kivy_soil.app_recycleview import AppRecycleViewClass
from kivy_soil.app_recycleview import AppRecycleView
from .term_system import TerminalWidgetSystem
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.core.window import Window
from kivy_soil.utils import intdp, intcm
from kivy.uix.label import Label
from kivy.utils import platform
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.app import App

Builder.load_file('kivy_soil/terminal_widget/term_layout.kv')

class TermButton(Label):
    is_held = BooleanProperty(False)

    def __init__(self, **kwargs):
        self.register_event_type('on_press')
        super(TermButton, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            FocusBehavior.ignored_touch.append(touch)
            self.is_held = True
            return True

    def on_is_held(self, _, value):
        if value:
            self.dispatch('on_press')
            Clock.schedule_once(self.dispatch_held, 0.7)

    def dispatch_held(self, *args):
        if self.is_held:
            self.dispatch('on_press')
            Clock.schedule_once(self.dispatch_held, 0.1)

    def on_touch_up(self, touch):
        self.is_held = False
        if self.collide_point(*touch.pos):
            FocusBehavior.ignored_touch.append(touch)
            return True

    def on_press(self, *args):
        pass


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
    background_color = ListProperty([0.2, 0.2, 0.3, 0.9])
    small_size = ListProperty([100, 100])
    big_size = ListProperty([100, 100])
    selected_size = StringProperty('')
    pos_multiplier = NumericProperty(0.0)
    term_system = ObjectProperty()
    font_size = NumericProperty(intdp(14))
    is_being_pulled = BooleanProperty(False)
    pull_area_pos = ListProperty([0, 0])
    pull_area_size = ListProperty([0, 0])
    movable_with_touch = BooleanProperty(True)
    global_objects = {
        'app': App.get_running_app(),
    }

    def __init__(self, **kwargs):
        super(TerminalWidget, self).__init__(**kwargs)
        Clock.schedule_once(self.init_widgets, 0)
        self.is_focusable = False
        self._temp_init_data = []
        self.size = self.small_size

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

    def _update_chars_per_line(self, *args):
        self.ids.rv.chars_per_line = int(
            ((self.width - intcm(0.5)) / self.font_size) * 1.6)

    def schedule_line_split_update(self, *args):
        Clock.unschedule(self._update_chars_per_line)
        Clock.schedule_once(self._update_chars_per_line, 0.3)

    def update_rv_box_font_name(self, _, value):
        for child in self.ids.rv_box.children:
            child.font_name = self.font_name

    def init_widgets(self, dt):
        rv = self.ids.rv
        inputw = self.ids.inputw
        inputw.is_focusable = False
        inputw.grab_focus = True
        rv_box = self.ids.rv_box
        self.fbind('font_size', self.schedule_line_split_update)
        self.fbind('size', self.schedule_line_split_update)
        self.schedule_line_split_update()

        self.fbind('font_name', self.update_rv_box_font_name)
        rv_box.bind(children=self.update_rv_box_font_name)

        self.term_system = TerminalWidgetSystem(self)
        self.term_system.bind(data=lambda obj, val: self.ids.rv.set_data(val))
        self.term_system.bind(
            on_data=lambda obj, val: self.ids.rv.set_data(val))

        rv.set_data(self.term_system.data)
        rv.input_widget = inputw
        inputw.keyboard_on_key_down = self.on_input_key_down
        for text, level in self._temp_init_data:
            self.add_data(text, level=level)
        del self._temp_init_data

    def on_input_key_down(self, _, key, text, modifiers):
        inputw = self.ids.inputw
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
        else:
            inputw.__class__.keyboard_on_key_down(
                inputw, _, key, text, modifiers)

    def animate_in_small(self, focus_input=True):
        self.size = self.small_size
        self.selected_size = 'small'
        if self.pos_multiplier < 1.0:
            if self.pos_multiplier:
                d = self.anim_speed * (1.0 - (self.pos_multiplier))
            else:
                d = self.anim_speed
            anim = Animation(pos_multiplier=1.0, d=d, t='out_quad')
            anim.start(self)
            self.ids.rv.scroll_to_end()
        else:
            d = 0.05
        self.ids.inputw.is_focusable = True
        if focus_input:
            Clock.schedule_once(self.focus_input, d * 3.0)

    def animate_in_big(self, focus_input=True):
        self.size = self.big_size
        self.selected_size = 'big'
        if self.pos_multiplier < 1.0:
            if self.pos_multiplier:
                d = self.anim_speed * (1.0 - (self.pos_multiplier))
            else:
                d = self.anim_speed
            anim = Animation(pos_multiplier=1.0, d=d, t='out_quad')
            anim.start(self)
            self.ids.rv.scroll_to_end()
        else:
            d = 0.05
        self.ids.inputw.is_focusable = True
        if focus_input:
            Clock.schedule_once(self.focus_input, d * 3.0)

    def animate_out(self, *args):
        self.ids.inputw.focus = False
        self.ids.inputw.is_focusable = False
        anim = Animation(pos_multiplier=0.0, d=self.anim_speed, t='in_quad')
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
        if self.ids.inputw.is_focusable:
            self.ids.inputw.focus = True

    def on_touch_down(self, touch):
        if 0 not in self.pull_area_size:
            ppos = self.pull_area_pos
            psize = self.pull_area_size
            tpos = self.to_local(*touch.pos)
            if self.movable_with_touch and self.pos_multiplier in (0.0, 1.0):
                if ppos[0] < tpos[0] < ppos[0] + psize[0]:
                    if ppos[1] < tpos[1] < ppos[1] + psize[1]:
                        if self.ids.inputw.focus:
                            self.ids.inputw.focus = False
                        self.is_being_pulled = True
                        return True
        return super(TerminalWidget, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.is_being_pulled:
            res = 1.0 - (float(touch.pos[1]) / float(Window.system_size[1]))
            if res > 0.8:
                if self.selected_size != 'big':
                    self.size = self.big_size
                    self.selected_size = 'big'
            elif self.selected_size != 'small':
                self.size = self.small_size
                self.selected_size = 'small'
            self.pos_multiplier = res
        else:
            return super(TerminalWidget, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.is_being_pulled:
            self.is_being_pulled = False
            if self.pos_multiplier >= 0.44:
                if self.selected_size == 'small':
                    self.animate_in_small(focus_input=False)
                elif self.selected_size == 'big':
                    self.animate_in_big(focus_input=False)
            else:
                self.animate_out()
        return super(TerminalWidget, self).on_touch_up(touch)
