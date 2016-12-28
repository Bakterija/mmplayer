from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivy.lang import Builder
from kivy.clock import Clock
from time import time
from kivy.metrics import sp, cm
from kivy.properties import BooleanProperty
from kivy.uix.widget import Widget
from kivy.core.window import Window

class HoverBehavior(Widget):
    hovering = BooleanProperty(False)
    def __init__(self, **kwargs):
        super(HoverBehavior, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouse_move)

    def on_mouse_move(self, win, (posx, posy)):
        if self.hovering == False:
            if self.collide_point_window(posx, posy):
                self.hovering = True
                self.on_enter()
        else:
            if self.collide_point_window(posx, posy) == False:
                self.hovering = False
                self.on_leave()

    def on_enter(self, *args):
        pass

    def on_leave(self, *args):
        pass

    def collide_point_window(self, x, y):
        sx, sy = self.to_window(self.x, self.y)
        return sx <= x <= sx + self.width and sy <= y <= sy + self.height

kv = '''
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
'''

class InfoLabel(HoverBehavior, Label):
    ttl = NumericProperty(2)
    tp = StringProperty('info')
    col_bg = ListProperty([0.2, 0.2, 0.2])
    col_transp = NumericProperty(0.8)

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
            print 'NO PARENT ', self

    def on_enter(self):
        self.bold = True

    def on_leave(self):
        self.bold = False
        if self.ttl <= 0:
            self.fade_out_clock()


class InfoWidget(BoxLayout):
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
    # width = NumericProperty200.0

    def add_label(self, **kwargs):
        timenow = int(time())
        self.msg_log.append(
            {'time':timenow, 'type':kwargs['tp'], 'message':kwargs['text']})
        if self.last_label['time'] + self.last_label['ttl'] > timenow:
            kwargs['ttl'] = (timenow - self.last_label['time'] +
                             self.last_label['ttl'] + kwargs['ttl'])
        self.add_widget(InfoLabel(**kwargs))
        self.last_label['time'] = timenow
        self.last_label['ttl'] = kwargs['ttl']

    def error(self, message, ttl=default_ttl):
        self.add_label(ttl=ttl, tp='error', text=message)

    def warning(self, message, ttl=default_ttl):
        self.add_label(ttl=ttl, tp='warning', text=message)

    def info(self, message, ttl=default_ttl):
        self.add_label(ttl=ttl, tp='info', text=message)


Builder.load_string(kv)
