from kivy_soil.kb_system.compat_widgets.popup import AppPopup
from utils import get_containing_directory, open_directory
from media_info import cache as media_cache
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.metrics import dp, cm
from kivy.lang import Builder
from kivy.clock import Clock
import global_vars as gvars
from kivy.app import App

Builder.load_string('''
#: import ConditionLayout widgets.condition_layout.ConditionLayout
#: import FocusButton widgets.focus_button.FocusButton
<CreatePlaylistPopup>:
    size_hint: 0.6, None
    height: self.content.height + int(app.mlayout.button_height * 2)
    title: 'Type playlist name'
    subfocus_widgets: [inp, btn1, btn2]
    StackLayout:
        id: stack0
        size_hint: 1, None
        height: self.minimum_height
        spacing: app.mlayout.spacing * 4
        CompatTextInput:
            id: inp
            size_hint: 1, None
            height: app.mlayout.button_height
            is_subfocus: True
            multiline: False
            on_text_validate: root.on_text_validate(self.text)
        FocusButton:
            id: btn1
            size_hint: 0.5, None
            height: app.mlayout.button_height
            is_subfocus: True
            text: 'Create'
            on_release: root.on_text_validate(inp.text)
        FocusButton:
            id: btn2
            size_hint: 0.5, None
            height: app.mlayout.button_height
            is_subfocus: True
            text: 'Cancel'
            on_release: root.dismiss()
''')


class CreatePlaylistPopup(AppPopup):
    grab_focus = True

    def on_text_validate(self, text):
        '''Calls MediaController.create_playlist()
        with input widget text argument'''
        mcontrol = App.get_running_app().root.media_control
        mcontrol.create_playlist(text)
        self.dismiss()

    def open(self, *args):
        '''Opens popup and schedules self.focus_input()
        to be called on next frame with Clock '''
        Clock.schedule_once(self.focus_input, 0)
        super(CreatePlaylistPopup, self).open(*args)

    def focus_input(self, *a):
        '''Focuses playlist name input widget'''
        self.ids.inp.focus_widget()

    def dismiss(self):
        super(CreatePlaylistPopup, self).dismiss()
        self.remove_from_focus(prev_focus=True)
        self.parent.remove_widget(self)
