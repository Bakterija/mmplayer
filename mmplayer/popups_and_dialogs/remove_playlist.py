from utils import get_containing_directory, open_directory
from kivy_soil.kb_system.canvas import FocusBehaviorCanvas
from media_info import cache as media_cache
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from widgets.popup2 import AppPopup
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.metrics import dp, cm
from kivy.lang import Builder
import global_vars as gvars
from kivy.app import App

Builder.load_string('''
#: import ConditionLayout widgets.condition_layout.ConditionLayout
#: import FocusButton widgets.focus_button.FocusButton
<RemovePlaylistPopup>:
    size_hint: 0.7, None
    height: self.content.height + int(app.mlayout.button_height * 2)
    title: 'Are you sure?'
    subfocus_widgets: [btn1, btn2]
    StackLayout:
        size_hint: 1, None
        height: self.minimum_height
        FocusButton:
            id: btn1
            size_hint: 0.5, None
            height: app.mlayout.button_height
            is_subfocus: True
            text: 'Yes'
            on_release: root.remove_playlist()
        Widget:
            size_hint_y: None
            height: app.mlayout.button_height
        FocusButton:
            id: btn2
            size_hint: 0.5, None
            height: app.mlayout.button_height
            is_subfocus: True
            text: 'No'
            on_release: root.dismiss()
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
