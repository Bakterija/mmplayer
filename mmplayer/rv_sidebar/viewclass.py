from widgets_standalone.app_recycleview import AppRecycleViewClass
from behaviors.hover_behavior import HoverBehavior
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.label import Label
from . import view_widgets


subview_classes = {
    'SideBarScreenButton': view_widgets.SideBarScreenButton,
    'SideBarPlaylistButton': view_widgets.SideBarPlaylistButton,
    'SideBarSeparator': view_widgets.SideBarSeparator,
    'SideBarSection': view_widgets.SideBarSection
}


class SideBarViewClass(HoverBehavior, AppRecycleViewClass, BoxLayout):
    sub_viewclass = StringProperty()
    path = StringProperty()
    orientation = 'horizontal'
    size_hint = None, None
    vchild = None

    def refresh_view_attrs(self, rv, index, data):
        super(SideBarViewClass, self).refresh_view_attrs(rv, index, data)
        self.update_vchild(data['viewclass'])

    def on_selected(self, _, value):
        if self.vchild.selectable:
            self.vchild.selected = value

    def on_hovering(self, _, value):
        if self.vchild:
            self.vchild.hovering = value

    def update_vchild(self, value):
        if value != self.sub_viewclass:
            if self.vchild:
                self.remove_widget(self.vchild)
            self.vchild = subview_classes[value]()
            self.add_widget(self.vchild)
            self.sub_viewclass = value

        self.vchild.refresh_attrs(self)
        self.selectable = self.vchild.selectable

    def on_left_click(self):
        self.vchild.on_left_click()

    def on_right_click(self):
        self.vchild.on_right_click()

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            if touch.device == 'mouse':
                if touch.button == 'left':
                    self.on_left_click()
                elif touch.button == 'right':
                    self.on_right_click()
            else:
                self.do_func()
            return True
