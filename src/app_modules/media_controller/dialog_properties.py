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

Builder.load_string('''
#: import ConditionLayout app_modules.widgets_standalone.condition_layout.ConditionLayout
#: import FocusButton app_modules.widgets_integrated.focus_button.FocusButton

<MediaPropertiesDialogText>:
    orientation: 'horizontal'
    size_hint: 1, None
    height: lbl2.height
    AppLabel:
        id: lbl1
        size_hint_x: 0.2
        valign: 'top'
        height: lbl2.height
        text_size: self.size
        text: root.t_key

    AppLabel:
        id: lbl2
        size_hint: 0.7, None
        valign: 'top'
        text_size: self.width, None
        height: self.texture_size[1]
        text: root.t_value

<MediaPropertiesDialog>:
    size_hint: 0.8, 0.7
    title: 'Media properties dialog'
    ScrollView:
        BoxLayout:
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'
            GridLayout:
                id: grid
                size_hint_y: None
                height: self.minimum_height
                cols: 1
                spacing: cm(0.3)
            ConditionLayout:
                size_hint_y: None
                height: app.mtheme.btn_height
                condition: True if root.containing_directory else False
                FocusButton:
                    id: open_fld_button
                    is_subfocus: True
                    text: 'Open containing directory'
                    on_release: root.open_cont_dir()
''')


class MediaPropertiesDialogText(BoxLayout):
    t_key = StringProperty()
    t_value = StringProperty()

    def __init__(self, key, value, **kwargs):
        super(MediaPropertiesDialogText, self).__init__(**kwargs)
        self.t_key = str(key)
        self.t_value = str(value)


class MediaPropertiesDialog(FocusBehaviorCanvas, AppPopup):
    containing_directory = StringProperty()
    remove_focus_on_touch_move = False
    grab_focus = True

    def __init__(self, media_dict, **kwargs):
        super(MediaPropertiesDialog, self).__init__(**kwargs)
        self.subfocus_widgets = [self.ids.open_fld_button]

    def add_content_widgets(self, media_dict):
        for k, v in media_dict.items():
            btn = MediaPropertiesDialogText(k, v)
            self.ids.grid.add_widget(btn)
            if k == 'path':
                self.containing_directory = get_containing_directory(v)

                if v in media_cache and media_cache[v]:
                    mc = media_cache[v]
                    if 'duration' in mc:
                        btn = MediaPropertiesDialogText('duration', mc['duration'])
                        self.ids.grid.add_widget(btn)
                    if mc['format']:
                        for x in ('artist', 'title', 'album', 'genre', 'date'):
                            tagtext = ''.join(('TAG:', x))
                            if tagtext in mc['format']:
                                btn = MediaPropertiesDialogText(
                                    x, mc['format'][tagtext])
                                self.ids.grid.add_widget(btn)

    def open_cont_dir(self):
        open_directory(self.containing_directory)

    def dismiss(self):
        super(MediaPropertiesDialog, self).dismiss()
        self.remove_from_focus(prev_focus=True)

    @staticmethod
    def open_diag(media_dict):
        dialog = MediaPropertiesDialog(media_dict)
        dialog.add_content_widgets(media_dict)

        dialog.open()
        return dialog
