from kivy.app import App
from time import time
from kivy.uix.widget import Widget
from app_modules.widgets.multi_line_label import MultiLineLabel
from kivy.uix.recycleview import RecycleView
from kivy.properties import ListProperty
from kivy.lang import Builder
defaultcolor = 'e6e6e6'

def tapp_add(self, text):
    app = App.get_running_app()
    if app:
        app.tapp_log.append(tapp_formater(text, color=defaultcolor))

def tapp_formater(text, color=defaultcolor):
    text0 = str(rounder(time() - starttime))
    if len(text0) < 8:
        text0 = text0.zfill(8)
    text1 = '[color=b3b3b3]%s[/color] ' % (text0)
    text2 = '[color=%s]%s[/color]' % (color, text)
    return {'text': text1 + text2}

def rounder(num):
    return round(num, 2)


starttime = rounder(time())
class TerminalApp(Widget):
    tapp_log = ListProperty()

    def tapp_add(self, text, color=defaultcolor):
        self.tapp_log.append(tapp_formater(text, color=defaultcolor))

    def tapp_get_gui(self, **kwargs):
        rv = TerminalRecycleView(**kwargs)
        self.bind(tapp_log=lambda obj, val: setattr(rv, 'data', val))
        return rv

kv = '''
<TerminalViewClass>:
    padding: dp(3), 0

<TerminalRecycleView>:
    scroll_type: ['bars', 'content']
    scroll_wheel_distance: dp(114)
    bar_width: dp(10)
    viewclass: 'TerminalViewClass'
    canvas.before:
        Color:
            rgb: 0.1, 0.1, 0.1
        Rectangle:
            pos: self.pos
            size: self.size
    RecycleBoxLayout:
        id: rv_box
        orientation: 'vertical'
        size_hint: None, None
        height: self.minimum_height
        width: self.parent.width
        default_size: None, None
        default_size_hint: 1, None
        spacing: '2dp'
'''

class TerminalViewClass(MultiLineLabel):
    def __init__(self, **kwargs):
        super(TerminalViewClass, self).__init__()


class TerminalRecycleView(RecycleView):
    def __init__(self, **kwargs):
        super(TerminalRecycleView, self).__init__(**kwargs)



Builder.load_string(kv)
