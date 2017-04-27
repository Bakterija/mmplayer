from kivy.properties import ListProperty, NumericProperty
from kivy.logger import Logger, LoggerHistory
from kivy.animation import Animation
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.metrics import cm


kv = '''
<TerminalWidget>:
    orientation: 'vertical'
    size_hint: None, None
    input_height: cm(0.8)
    anim_speed: 0.2
    canvas:
        Color:
            rgba: 0.2, 0.2, 0.2, 0.9
        Rectangle:
            size: self.size
            pos: self.pos

    ScrollView:
        id: scroller
        size_hint_y: None
        height: root.height - root.input_height

        BoxLayout:
            id: dbview
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height

    TextInput:
        id: input
        size_hint_y: None
        height: root.input_height
        font_size: self.height * 0.5
        background_color: 0.12, 0.12, 0.18, 1
        foreground_color: 1, 1, 1, 1
        cursor_color: 1, 1, 1, 1
        multiline: False
        text_color: 1, 1, 1, 1
        on_text_validate: root.on_input(self, self.text)
'''


class TerminalView(Label):
    def __init__(self, **kwargs):
        super(TerminalView, self).__init__( **kwargs)
        self.markup = True
        self.text_size = self.size
        self.bind(size= self.on_size)
        self.bind(text= self.on_text_changed)
        self.size_hint_y = None # Not needed here

    def on_size(self, widget, size):
        self.text_size = size[0], None
        self.texture_update()
        if self.size_hint_y == None and self.size_hint_x != None:
            self.height = max(self.texture_size[1], self.line_height)
        elif self.size_hint_x == None and self.size_hint_y != None:
            self.width  = self.texture_size[0]

    def on_text_changed(self, widget, text):
        self.on_size(self, self.size)

    def refresh_view_attrs(self, terminal, index, data):
        for k, v in data.items():
            setattr(self, k, v)


class TerminalWidget(BoxLayout):
    data = ListProperty()
    pos_multiplier = NumericProperty()
    input_callback = None

    def __init__(self, **kwargs):
        super(TerminalWidget, self).__init__(**kwargs)
        Clock.schedule_once(self.after_init, 0.5)

    def after_init(self, *args):
        histo = LoggerHistory()
        for x in histo.history:
            self.data.append({'text': str(x.msg)})

    def on_data(self, instance, value):
        view = self.ids.dbview
        children_count = len(view.children)
        value_count = len(value)
        if children_count != value_count:
            if children_count < value_count:
                for count in range(0, value_count - children_count):
                    view.add_widget(TerminalView())
            else:
                for count in range(0, children_count - value_count):
                    view.remove_widget(view.children[-1])

        if view.children:
            for i, child in enumerate(reversed(view.children)):
                child.refresh_view_attrs(self, i, value[i])
        self.animate_scroll_bottom()

    def enter(self, *args):
        anim = Animation(pos_multiplier=1.0, d=self.anim_speed, t='out_quad')
        anim.start(self)
        self.ids.input.focus = True

    def leave(self, *args):
        anim = Animation(pos_multiplier=0.0, d=self.anim_speed, t='in_quad')
        anim.start(self)
        if self.ids.input.focus:
            self.ids.input.focus = False

    def scroll_up(self, *args):
        distance = self.ids.scroller.convert_distance_to_scroll(0, cm(1))[1]
        self.ids.scroller.scroll_y += distance
        if self.ids.scroller.scroll_y > 1:
            self.ids.scroller.scroll_y = 1

    def scroll_down(self, *args):
        distance = self.ids.scroller.convert_distance_to_scroll(0, cm(1))[1]
        self.ids.scroller.scroll_y -= distance
        if self.ids.scroller.scroll_y < 0:
            self.ids.scroller.scroll_y = 0

    def animate_scroll_bottom(self, force=False, *args, **kwargs):
        if self.ids.scroller.scroll_y != 0.0 or force:
            anim = Animation(scroll_y=0, d=self.anim_speed)
            anim.start(self.ids.scroller)

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
