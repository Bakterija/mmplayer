# -*- coding: utf-8 -*-
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import NumericProperty, ListProperty, OptionProperty, \
    StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from app_modules.kb_system.focus import FocusBehavior
from app_modules.widgets_standalone.app_recycleview import AppRecycleView
from app_modules.widgets_standalone.app_recycleview import AppRecycleViewClass
from app_modules.behaviors.hover_behavior import HoverBehavior
from app_modules.kb_system import keys
from global_vars import theme_manager



Builder.load_string('''
<MDMenuItem>
    size_hint_y: None
    padding: int(cm(0.2)), 0
    height: app.mtheme.btn_height
    on_release: root.parent.parent.dismiss_ctx_menu()
    canvas.before:
        Color:
            rgba: col_bblue_transp06 if self.selected else [0, 0, 0, 0]
        Rectangle:
            size: self.size
            pos: self.pos
        Color:
            rgba: col_bblue_transp06 if self.hovering else [0, 0, 0, 0]
        Rectangle:
            size: self.size
            pos: self.pos
    AppLabel:
        text_size: self.width, None
        text: root.text

<MDMenu>
    size_hint: 1, None
    key_viewclass: 'viewclass'
    AppRecycleBoxLayout:
        default_size: None, app.mtheme.btn_height
        default_size_hint: 1, None
        orientation: 'vertical'

<MDDropdownMenu>
    FloatLayout:
        id: fl
        MDMenu:
            id: md_menu
            data: root.items
            width_mult: root.width_mult
            size_hint: None, None
            size: 0, 0
            canvas.before:
                Color:
                    rgba: app.mtheme.background2
                Rectangle:
                    size: self.size
                    pos: self.pos
''')


class MDMenuItem(HoverBehavior, ButtonBehavior, BoxLayout,
                 AppRecycleViewClass):
    text = StringProperty()
    hover_height = 10

    def __init__(self, **kwargs):
        super(MDMenuItem, self).__init__(**kwargs)


class MDMenu(AppRecycleView, FocusBehavior):
    width_mult = NumericProperty(1)
    remove_focus_on_touch_move = False
    grab_focus = True
    nremoving = False
    grab_keys = [keys.ESC]

    def on_key_down(self, key, *args):
        box = self.children[0]
        if key == keys.UP:
            box.on_arrow_up()
            self.remove_hover()
        elif key == keys.DOWN:
            box.on_arrow_down()
            self.remove_hover()
        elif key in (keys.RETURN, keys.ENTER):
            for x in box.children:
                if x.selected:
                    x.on_press()
                    self.dismiss_ctx_menu()
                    break
        elif key == keys.ESC:
            self.dismiss_ctx_menu()

    def on_ctx_dismiss(self):
        self.remove_from_focus(prev_focus=True)
        self.clear_widgets()

    def dismiss_ctx_menu(self):
        if not self.nremoving:
            self.remove_from_focus(prev_focus=True)
            self.parent.parent.dismiss()
            self.nremoving = True

    def remove_hover(self):
        for x in self.children[0].children:
            if x.hovering:
                x.hovering = False


class MDDropdownMenu(BoxLayout):
    items = ListProperty()
    '''See :attr:`~kivy.uix.recycleview.RecycleView.data`
    '''

    width_mult = NumericProperty(1)
    '''This number multiplied by the standard increment (56dp on mobile,
    64dp on desktop, determines the width of the menu items.

    If the resulting number were to be too big for the application Window,
    the multiplier will be adjusted for the biggest possible one.
    '''

    max_height = NumericProperty()
    '''The menu will grow no bigger than this number.

    Set to 0 for no limit. Defaults to 0.
    '''

    border_margin = NumericProperty(dp(4))
    '''Margin between Window border and menu
    '''

    ver_growth = OptionProperty(None, allownone=True,
                                options=['up', 'down'])
    '''Where the menu will grow vertically to when opening

    Set to None to let the widget pick for you. Defaults to None.
    '''

    hor_growth = OptionProperty(None, allownone=True,
                                options=['left', 'right'])
    '''Where the menu will grow horizontally to when opening

    Set to None to let the widget pick for you. Defaults to None.
    '''

    def open(self, *largs):
        Window.add_widget(self)
        # Clock.schedule_once(lambda x: self.display_menu(largs[0]), -1)
        self.display_menu(largs[0])
        
    def display_menu(self, caller):
        # We need to pick a starting point, see how big we need to be,
        # and where to grow to.
        c = caller.to_window(caller.center_x,
                             caller.center_y)  # Starting coords

        # ---ESTABLISH INITIAL TARGET SIZE ESTIMATE---
        target_width = int(self.width_mult * theme_manager.btn_height)
        # If we're wider than the Window...
        if target_width > Window.width:
            # ...reduce our multiplier to max allowed.
            target_width = int(
                Window.width / theme_manager.btn_height) * theme_manager.btn_height

        target_height = theme_manager.btn_height * len(self.items)
        # If we're over max_height...
        if 0 < self.max_height < target_height:
            target_height = self.max_height

        # ---ESTABLISH VERTICAL GROWTH DIRECTION---
        if self.ver_growth is not None:
            ver_growth = self.ver_growth
        else:
            # If there's enough space below us:
            if target_height <= c[1] - self.border_margin:
                ver_growth = 'down'
            # if there's enough space above us:
            elif target_height < Window.height - c[1] - self.border_margin:
                ver_growth = 'up'
            # otherwise, let's pick the one with more space and adjust ourselves
            else:
                # if there's more space below us:
                if c[1] >= Window.height - c[1]:
                    ver_growth = 'down'
                    target_height = c[1] - self.border_margin
                # if there's more space above us:
                else:
                    ver_growth = 'up'
                    target_height = Window.height - c[1] - self.border_margin

        if self.hor_growth is not None:
            hor_growth = self.hor_growth
        else:
            # If there's enough space to the right:
            if target_width <= Window.width - c[0] - self.border_margin:
                hor_growth = 'right'
            # if there's enough space to the left:
            elif target_width < c[0] - self.border_margin:
                hor_growth = 'left'
            # otherwise, let's pick the one with more space and adjust ourselves
            else:
                # if there's more space to the right:
                if Window.width - c[0] >= c[0]:
                    hor_growth = 'right'
                    target_width = Window.width - c[0] - self.border_margin
                # if there's more space to the left:
                else:
                    hor_growth = 'left'
                    target_width = c[0] - self.border_margin

        if ver_growth == 'down':
            tar_y = c[1] - target_height
        else:  # should always be 'up'
            tar_y = c[1]

        if hor_growth == 'right':
            tar_x = c[0]
        else:  # should always be 'left'
            tar_x = c[0] - target_width
        anim = Animation(x=tar_x, y=tar_y,
                         width=target_width, height=target_height,
                         duration=.3, transition='out_quint')
        menu = self.ids['md_menu']
        menu.pos = c
        anim.start(menu)

    def on_touch_down(self, touch):
        if not self.ids['md_menu'].collide_point(*touch.pos):
            self.dismiss()
            return True
        super(MDDropdownMenu, self).on_touch_down(touch)
        return True

    def on_touch_move(self, touch):
        super(MDDropdownMenu, self).on_touch_move(touch)
        return True

    def on_touch_up(self, touch):
        super(MDDropdownMenu, self).on_touch_up(touch)
        return True

    def dismiss(self):
        self.children[0].children[0].on_ctx_dismiss()
        Window.remove_widget(self)
