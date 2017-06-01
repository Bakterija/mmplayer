from utils import get_containing_directory, open_directory
from utils import seconds_to_minutes_hours
from kivy_soil.kb_system.canvas import FocusBehaviorCanvas
from media_info import cache as media_cache
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy_soil.kb_system import keys
from widgets.app_popup import AppPopup
from kivy.uix.popup import Popup
from kivy.metrics import dp, cm
from kivy.uix.label import Label
from kivy.lang import Builder
import global_vars as gvars

Builder.load_string('''
#: import ConditionLayout widgets.condition_layout.ConditionLayout
#: import FocusButtonScroller widgets.focus_button.FocusButtonScroller
#: import Clipboard kivy.core.clipboard.Clipboard

<MediaPropertiesDialogText>:
    orientation: 'horizontal'
    size_hint: 1, None
    height: tinput.height
    Label:
        id: label
        size_hint_x: None
        width: int(root.width * 0.2)
        valign: 'top'
        height: tinput.height
        text_size: self.size
        text: root.t_key

    CompatTextInputScroller:
        id: tinput
        size_hint: None, None
        width: int(root.width * 0.8)
        text_size: self.width, None
        height: self.minimum_height
        text_size: self.width, None
        text: root.t_value
        multiline: True
        foreground_color: app.mtheme.col_text
        background_active: ''
        background_normal: ''
        background_disabled_normal: ''
        background_color: (0.3, 0.3, 0.8, 0.15)

<MediaPropertiesDialog>:
    size_hint: 0.8, 0.7
    title: 'Media properties dialog'
    ScrollView:
        id: scroller
        do_scroll_x: False
        BoxLayout:
            size_hint: 1, None
            height: self.minimum_height
            orientation: 'vertical'
            spacing: app.mlayout.button_height
            GridLayout:
                id: grid
                size_hint: 0.9, None
                pos_hint: {'center_x': 0.5}
                size_hint_y: None
                height: self.minimum_height
                cols: 1
                spacing: int(cm(0.3))
            ConditionLayout:
                size_hint: 0.9, None
                pos_hint: {'center_x': 0.5}
                height: app.mlayout.button_height
                condition: True if root.containing_directory else False
                spacing: app.mlayout.spacing * 4
                FocusButtonScroller:
                    id: open_fld_button
                    scroll_when_focused: scroller
                    is_subfocus: True
                    text: 'Open containing directory'
                    on_release: root.open_cont_dir()
                FocusButtonScroller:
                    id: copy_path_button
                    scroll_when_focused: scroller
                    is_subfocus: True
                    text: 'Copy path'
                    on_release: Clipboard.copy(root.mpath)
''')


class MediaPropertiesDialogText(BoxLayout):
    t_key = StringProperty()
    t_value = StringProperty()

    def __init__(self, key, value, **kwargs):
        super(MediaPropertiesDialogText, self).__init__(**kwargs)
        self.t_key = str(key)
        self.t_value = str(value)


class MediaPropertiesDialog(FocusBehaviorCanvas, AppPopup):
    '''Takes a dictionary as first __init__ argument and adds
    Label widget pairs in boxlayouts to display, has handling for
    media data'''

    containing_directory = StringProperty()
    '''Stores directory path which contains media file when a path is found
    in media_dict argument'''

    mpath = StringProperty()
    '''Stores media file path when a path is found in media_dict argument'''

    ignored_properties = ['id', 'state']

    def __init__(self, media_dict, **kwargs):
        super(MediaPropertiesDialog, self).__init__(**kwargs)
        self.remove_focus_on_touch_move = False
        self.grab_focus = True
        self.subfocus_widgets = [
            self.ids.open_fld_button, self.ids.copy_path_button]

    def add_content_widgets(self, media_dict):
        '''Find all important information in media_dict and add widgets to self
        '''
        grid = self.ids.grid
        # Adds key and value pairs from media_dict argument
        button_list = []
        for k, v in media_dict.items():
            if k in self.ignored_properties:
                continue
            button_list.append((k, v))

        # Attempts to get and add file tags
        # and other important information from global media cache
        mpath = media_dict.get('path', '')
        if mpath:
            self.containing_directory = get_containing_directory(mpath)
            self.mpath = mpath

            mc = media_cache.get(mpath, None)
            if mc:
                duration = mc.get('duration', None)
                if duration:
                    duration = seconds_to_minutes_hours(duration)
                    button_list.append(('duration', duration))
                mc_format = mc.get('format', None)
                if mc_format:
                    for k, v in mc_format.items():
                        if k[:4] == 'TAG:':
                            k = k[4:]
                            button_list.append((k, v))
        for k, v in button_list:
            btn = MediaPropertiesDialogText(k, v)
            tinput = btn.ids.tinput
            tinput.is_subfocus = True
            tinput.scroll_when_focused = self.ids.scroller
            self.subfocus_widgets.insert(-2, tinput)
            grid.add_widget(btn)

    def open_cont_dir(self):
        '''Open directory that contains file'''
        open_directory(self.containing_directory)

    def dismiss(self):
        super(MediaPropertiesDialog, self).dismiss()
        self.remove_from_focus(prev_focus=True)
        # self.parent.remove_widget(self)

    @staticmethod
    def open_diag(media_dict):
        '''Method for creating and opening dialog'''
        dialog = MediaPropertiesDialog(media_dict)
        dialog.add_content_widgets(media_dict)

        dialog.open()
        return dialog
