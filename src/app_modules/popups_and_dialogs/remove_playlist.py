from app_modules.kb_system.canvas import FocusBehaviorCanvas
from kivy.uix.popup import Popup
from kivy.metrics import dp, cm
from kivy.uix.label import Label
import global_vars as gvars
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.lang import Builder
from utils import get_containing_directory, open_directory
from media_info import cache as media_cache
from app_modules.widgets_integrated.popup2 import AppPopup
from kivy.app import App

Builder.load_string('''
#: import ConditionLayout app_modules.widgets_standalone.condition_layout.ConditionLayout
#: import FocusButton app_modules.widgets_integrated.focus_button.FocusButton
<RemovePlaylistPopup>:
    size_hint: 0.7, None
    height: self.content.height + (button_height * 2)
    title: 'Are you sure?'
    subfocus_widgets: [btn1, btn2]
    spacing: default_spacing * 4
    StackLayout:
        size_hint: 1, None
        height: self.minimum_height
        FocusButton:
            id: btn1
            size_hint: 0.5, None
            height: button_height
            is_subfocus: True
            text: 'Yes'
            on_press: root.remove_playlist()
        FocusButton:
            id: btn2
            size_hint: 0.5, None
            height: button_height
            is_subfocus: True
            text: 'No'
            on_press: root.dismiss()
''')


class RemovePlaylistPopup(FocusBehaviorCanvas, AppPopup):
    grab_focus = True
    pl_path = StringProperty()

    def __init__(self, playlist_path, **kwargs):
        super(RemovePlaylistPopup, self).__init__(**kwargs)
        self.pl_path = playlist_path

    def remove_playlist(self):
        mcontrol = App.get_running_app().root.media_control
        mcontrol.remove_playlist(self.pl_path)
        self.dismiss()

    def dismiss(self):
        super(RemovePlaylistPopup, self).dismiss()
        self.remove_from_focus(prev_focus=True)
        self.parent.remove_widget(self)
