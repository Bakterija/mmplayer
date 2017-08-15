from kivy.app import App
from time import time
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from random import randrange
from kivy.metrics import cm
from kivy.lang import Builder
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.logger import Logger
from kivy.properties import NumericProperty
Window.system_size = 500, 400


kv = '''
<RootScroller>:

    RecycleView:
        id: data_box
        scroll_type: ['bars', 'content']
        bar_width: self.width * 0.07
        bar_color: 0.2, 0.2, 0.2, 1
        bar_inactive_color: 0.2, 0.2, 0.2, 1

        viewclass: 'DataButton'
        canvas.before:
            Color:
                rgb: 0.9, 0.9, 0.9
            Rectangle:
                size: self.size
                pos: self.pos

        canvas:
            Color:
                rgb: 0.7, 0.7, 0.7
            Rectangle:
                size: self.width * 0.07, self.height
                pos: self.width * 0.93, 0

        RecycleBoxLayout:
            orientation: 'vertical'
            default_size: None, dp(56)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            multiselect: True
            touch_multiselect: True

    FloatLayout:
        size_hint: None, None
        size: 0, 0
        Button:
            size_hint: None, None
            size: self.texture_size
            text: 'FPS: {}'.format(root.fps)


<DataButton>:
    canvas.before:
        Color:
            rgb: 0.2, 0.3, 0.6, 1
        Rectangle:
            size: self.width, self.height * 0.94
            pos: self.x, self.y + self.height * 0.03
'''

full_string = '''Had denoting properly jointure you occasion directly raillery. In said to of poor full be post face snug. Introduced imprudence see say unpleasing devonshire acceptance son. Exeter longer wisdom gay nor design age. Am weather to entered norland no in showing service. Nor repeated speaking shy appetite. Excited it hastily an pasture it observe. Snug hand how dare here too.

He unaffected sympathize discovered at no am conviction principles. Girl ham very how yet hill four show. Meet lain on he only size. Branched learning so subjects mistress do appetite jennings be in. Esteems up lasting no village morning do offices. Settled wishing ability musical may another set age. Diminution my apartments he attachment is entreaties announcing estimating. And total least her two whose great has which. Neat pain form eat sent sex good week. Led instrument sentiments she simplicity.

Advice me cousin an spring of needed. Tell use paid law ever yet new. Meant to learn of vexed if style allow he there. Tiled man stand tears ten joy there terms any widen. Procuring continued suspicion its ten. Pursuit brother are had fifteen distant has. Early had add equal china quiet visit. Appear an manner as no limits either praise in. In in written on charmed justice is amiable farther besides. Law insensible middletons unsatiable for apartments boy delightful unreserved.'''

class RootScroller(BoxLayout):
    fps = NumericProperty()


class DataButton(RecycleDataViewBehavior, Label):

    def __init__(self, **kwargs):
        super(DataButton, self).__init__(**kwargs)
        self.size_hint_y = None
        self.markup = True

    def refresh_view_attrs(self, rv, index, data):
        super(DataButton, self).refresh_view_attrs(rv, index, data)
        self.rv = rv

    def on_width(self, i , value):
        if value > 30:
            self.text_size = self.width, None

    def on_texture_size(self, i , value):
        self.height = value[1]

    def on_release(self, *args):
        print('on_release:', self.text)


class RecycleviewExample(App):
    starttime = time()
    frametimes = []

    def build(self):
        self.root = RootScroller()

        ndata = []
        for i in range(0, 10160):
            # ndata.append( {'text': 't {}'.format(i)})
            ndata.append( {'text': '[color=#FE2E2E]{}[/color] \n {}'.format(
                i, full_string[randrange(0, len(full_string), 1):]
            )})
        self.root.ids.data_box.data = ndata

        Clock.schedule_interval(self.test_interval, 0)
        Clock.schedule_once(self.test_once, 1)
        return self.root

    def on_start(self, *args):
        Logger.info('BUILD TIME: {}'.format(time() - self.starttime))

    def test_once(self, *args):
        pass

    def test_interval(self, *args):
        if len(self.frametimes) == 10:
            self.frametimes.append(time() - self.last_time)
            del self.frametimes[0]

            alltime = 0.0
            for x in self.frametimes:
                alltime += x
            alltime = alltime / 10
            # Logger.info('FRAME TIME: {}'.format(1.0 / alltime))
            self.root.fps = 1.0 / alltime

        elif 0 < len(self.frametimes) < 10:
            self.frametimes.append(time() - self.last_time)

        else:
            self.frametimes.append(time() - self.starttime)
        self.last_time = time()

Builder.load_string(kv)
app = RecycleviewExample()
app.run()
