from kivy.properties import NumericProperty, StringProperty
from kivy_soil.app_recycleview import SingleSelectRecycleBox
from kivy_soil.app_recycleview.behaviors.quickfind import AppRecycleViewQuickFind
from kivy_soil.app_recycleview import AppRecycleView
from kivy_soil.kb_system.canvas import FocusBehaviorCanvas
from .ctx_menu import open_sidebar_ctx_menu
from .viewclass import SideBarViewClass
from kivy.lang import Builder
from kivy.clock import Clock
from kivy_soil.kb_system import keys
from . import view_widgets
from kivy.app import App


Builder.load_string('''
<SideBarRecycleView>:
    viewclass: 'SideBarViewClass'
    SideBarRecycleRecycleBox:
        orientation: 'vertical'
        size_hint: None, None
        height: self.minimum_height
        width: root.width - root.bar_width
        default_size_hint: 1, None
        default_size: None, None
        spacing: app.mlayout.spacing
''')


class SideBarRecycleView(FocusBehaviorCanvas, AppRecycleViewQuickFind,
                         AppRecycleView):
    grab_keys = [keys.TAB, keys.ESC]

    def __init__(self, **kwargs):
        super(SideBarRecycleView, self).__init__(**kwargs)
        self.bind(focus=self.on_focus_update_selected)

    def on_focus_update_selected(self, _, value):
        box = self.children[0]
        if value:
            box.select_with_touch(box.desel_index)

    def on_key_down(self, key, modifier):
        box = self.children[0]
        if key in (keys.UP, keys.DOWN):
            for x in box.children:
                if x.hovering:
                    x.hovering = False
                    x.on_leave()
            if key == keys.UP:
                box.on_arrow_up()
            elif key == keys.DOWN:
                box.on_arrow_down()
        elif key in (keys.ENTER, keys.RETURN):
            selected = box.get_selected_widget()
            if selected:
                selected.on_left_click()
        elif key == keys.PAGE_UP:
            self.page_up()
        elif key == keys.PAGE_DOWN:
            self.page_down()
        elif key in (keys.MENU, keys.MENU_WIN):
            box.open_context_menu()
        elif key == keys.TAB:
            box.deselect_all()
            return True
        elif key == keys.ESC:
            box.deselect_all()
            return True


class SideBarRecycleRecycleBox(SingleSelectRecycleBox):

    def context_menu_function(self, child, index, pos):
        open_sidebar_ctx_menu(child)
