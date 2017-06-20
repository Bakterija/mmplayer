from kivy.properties import NumericProperty, StringProperty
from kivy.properties import BooleanProperty, ListProperty
from kivy_soil.hover_behavior import HoverBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.metrics import sp, cm
from kivy.lang import Builder
from kivy.clock import Clock
from time import time

Builder.load_string('''
<InfoWidget>:
    orientation: 'vertical'
    size_hint: None, None
    height: self.minimum_size[1]
    spacing: dp(10)

<InfoLabel>:
    font_size: dp(22)
    canvas.before:
        Color:
            rgba: self.col_bg[0], self.col_bg[1], self.col_bg[2], self.col_transp
        Rectangle:
            size: self.width + dp(6), self.height + dp(6)
            pos: self.pos[0] - dp(3), self.pos[1] - dp(3)
''')

class InfoLabel(HoverBehavior, Label):
    '''Notification display widget'''
    ttl = NumericProperty(2)
    tp = StringProperty('info')
    col_bg = ListProperty([0.2, 0.2, 0.2])
    col_transp = NumericProperty(0.8)
    hover_height = 200

    def __init__(self, **kwargs):
        super(InfoLabel, self).__init__(**kwargs)
        # self.markup = True
        self.text_size = self.size
        self.bind(size= self.on_size)
        self.bind(text= self.on_text_changed)
        self.size_hint_y = None # Not needed here

    def on_size(self, widget, size):
        self.text_size = size[0], None
        self.texture_update()
        if self.size_hint_y == None and self.size_hint_x != None:
            self.height = max(self.texture_size[1], self.line_height) + sp(5)
        elif self.size_hint_x == None and self.size_hint_y != None:
            self.width  = self.texture_size[0]

    def on_text_changed(self, widget, text):
        self.on_size(self, self.size)

    def on_parent(self, _, parent):
        if parent:
            self.col_bg = parent.colors[self.tp]
            self.col_transp = parent.transparency
            self.font_size = parent.font_size
            Clock.schedule_once(self.fade_out_clock, self.ttl)

    def fade_out_clock(self, *args):
        if not self.hovering:
            timm = 0.7
            anim = Animation(col_transp=0.0, d=timm)
            anim.start(self)
            cl = Clock.schedule_once(self.remove_self, timm)
            self.clock = cl
        self.ttl = 0

    def remove_self(self, *args):
        if self.parent:
            self.parent.remove_widget(self)
        else:
            print ('NO PARENT ', self)

    def on_enter(self):
        self.bold = True

    def on_leave(self):
        self.bold = False
        if self.ttl <= 0:
            self.fade_out_clock()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.remove_self()
            return True


class InfoWidget(BoxLayout):
    '''Notification display layout'''
    colors = {
        'error': [0.7, 0.3, 0.3],
        'warning': [0.6, 0.6, 0.3],
        'info': [0.4, 0.4, 0.4]
    }
    transparency = NumericProperty(0.9)
    msg_log = []
    default_ttl = 7
    font_size = sp(16)
    last_label = {'time': 0.0, 'ttl': 0.0}

    def _add_label(self, **kwargs):
        kwargs['text'] = str(kwargs['text'])
        timenow = int(time())
        self.msg_log.append(
            {'time':timenow, 'type':kwargs['tp'], 'message':kwargs['text']})
        if self.last_label['time'] + self.last_label['ttl'] > timenow:
            kwargs['ttl'] = (timenow - self.last_label['time'] +
                             self.last_label['ttl'] + kwargs['ttl'])
        self.add_widget(InfoLabel(**kwargs), index=len(self.children))
        self.last_label['time'] = timenow
        self.last_label['ttl'] = kwargs['ttl']

    def error(self, message, ttl=default_ttl):
        self._add_label(ttl=ttl, tp='error', text=message)

    def warning(self, message, ttl=default_ttl):
        self._add_label(ttl=ttl, tp='warning', text=message)

    def info(self, message, ttl=default_ttl):
        self._add_label(ttl=ttl, tp='info', text=message)
