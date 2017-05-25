from kivy.lang import Builder
from app_modules.kb_system import keys
from app_modules.widgets_standalone.app_recycleview import (
    AppRecycleView, AppRecycleBoxLayout)
from app_modules.kb_system.canvas import FocusBehaviorCanvas
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from . import view_widgets
from kivy.properties import NumericProperty, StringProperty
from .ctx_menu import open_sidebar_ctx_menu
from kivy.app import App
from kivy.clock import Clock
from .viewclass import SideBarViewClass
from app_modules.widgets_standalone.app_recycleview import (
    SingleSelectRecycleBox)


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


class SideBarRecycleView(FocusBehaviorCanvas, AppRecycleView):
    grab_keys = [keys.TAB]

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


class SideBarRecycleRecycleBox(SingleSelectRecycleBox):

    def context_menu_function(self, child, index, pos):
        open_sidebar_ctx_menu(child)
