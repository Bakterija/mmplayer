from kivy.uix.recycleview import RecycleView
from kivy.uix.stacklayout import StackLayout
from kivy.utils import platform
from kivy.metrics import dp, cm
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import BooleanProperty
from kivy.properties import StringProperty, DictProperty
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import ButtonBehavior
from pc_sidebar_widgets import rvLabelButton, rvSection
from kivy.clock import Clock
from kivy.core.window import Window
import traceback


kv = '''
<SideBarRecycleView>:
    id: rv
    size_hint: 1, None
    height: self.parent.height
    scroll_type: ['bars', 'content']
    scroll_wheel_distance: dp(114)
    bar_width: dp(10)
    viewclass: 'SideBarViewClass'
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

class SideBarViewClass(RecycleDataViewBehavior, ButtonBehavior, StackLayout):
    index = None  # stores our index
    bg_colors = DictProperty()
    text = StringProperty()
    func = None
    func2 = None
    fsize = NumericProperty(int(dp(16)))
    wtype = StringProperty()
    children_initialised = False
    def __init__(self, **kwargs):
        super(SideBarViewClass, self).__init__(**kwargs)
        size_hint_y = None

    def init_children(self, *args):
        if self.wtype == 'text':
            self.lbl = rvLabelButton(text=self.text)
            self.add_widget(self.lbl)
            # self.lbl.bind(on_touch_down=self.try_pressing)
        elif self.wtype == 'section':
            self.lbl = rvSection(text=self.text)
            self.add_widget(self.lbl)
        elif self.wtype == 'separator':
            self.lbl = Label(text=self.text, size_hint=(1, None), height=cm(1))
            self.add_widget(self.lbl)
        setattr(self, 'height', self.lbl.height)

    def on_text(self, *args):
        if self.children_initialised:
            self.lbl.text = self.text

    def on_mouse_move(self, win, pos):
        if self.wtype == 'text':
            self.lbl.on_mouse_move(int(pos[0]), int(pos[1]))

    def on_touch_move(self, *args):
        if self.wtype == 'text':
            self.lbl.on_touch_move(*args)

    def refresh_view_attrs(self, rv, index, data):
        try:
            replace = False
            if self.wtype != data['wtype']:
                replace = True
            for x in data:
                setattr(self, x, data[x])
            if self.children_initialised == False:
                self.init_children()
                self.rv = rv
                self.bind(text=self.on_text)
                Window.bind(mouse_pos=self.on_mouse_move)
                # Window.bind(on_touch_move=self.on_touch_move)
                self.children_initialised = True
            elif replace == True:
                self.remove_widget(self.lbl)
                self.init_children()
            super(SideBarViewClass, self).refresh_view_attrs(rv, index, data)
        except Exception as e:
            traceback.print_exc()

    def apply_selection(self, rv, index, is_selected):
        pass

    def do_func(self):
        self.func()
        if self.can_select:
            if self.rv.selected_child_sb:
                self.rv.selected_child_sb.on_select()
            self.rv.selected_child_sb = self.lbl
            self.lbl.on_select()

    def on_left_click(self):
        self.do_func()

    def on_right_click(self):
        if self.func2:
            self.func2()

    def on_touch_up(self, touch):
        if self.wtype == 'text':
            if self.collide_point(touch.x, touch.y):
                if touch.device == 'mouse':
                    if touch.button == 'left':
                        self.on_left_click()
                    elif touch.button == 'right':
                        self.on_right_click()
                else:
                    self.do_func()
                return True


class SideBarRecycleView(RecycleView):
    selected_child_sb = None
    def __init__(self, **kwargs):
        super(SideBarRecycleView, self).__init__(**kwargs)
        Clock.schedule_once(self.init_hovercolor, 0)

    def init_hovercolor(self, *args):
        def on_next_frame(*args):
            for x in self.children[0].children:
                if x.text == 'Main':
                    x.try_pressing()
        # Clock.schedule_once(on_next_frame, 0)


Builder.load_string(kv)
