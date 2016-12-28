from __future__ import print_function
from kivy.uix.popup import Popup
from kivy.uix.stacklayout import StackLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from app_modules.widgets.multi_line_label import MultiLineLabel
from app_modules.widgets.background_label import BackgroundLabel
from kivy.uix.spinner import Spinner
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.properties import StringProperty
from kivy.metrics import cm
from kivy.lang import Builder
import os


kv = '''
#: import aa1 app_modules.widgets.background_label.BackgroundLabel
<FileAdderDialog>:
    title: 'File adder dialog'
    size_hint: 0.9, 0.7
    StackLayout:
        id: content
        BackgroundLabel:
            id: filecounter
            size_hint_y: None
            height: cm(0.5)
            background_color: 0.2, 0.2, 0.3, 1
            text: 'Adding files'

        FileAdderRecycleView:
            id: file_list
            size_hint_y: None
            height: content.height - (cm(1) + cm(2) + cm(0.5) + cm(1))
            canvas.before:
                Color:
                    rgb: 0.22, 0.22, 0.22
                Rectangle:
                    pos: self.pos
                    size: self.size

        Widget:
            size_hint_y: None
            height: cm(0.5)

        Label:
            id: spinlabel
            size_hint: None, None
            height: cm(1)
            width: cm(3)
            text_size: self.size[0], None
            text: 'Select playlist'
        Spinner:
            id: playlist_spinner
            size_hint: None, None
            width: content.width - spinlabel.width
            height: cm(1)
            text: 'Current'

        Label:
            id: spinlabel2
            size_hint: None, None
            height: cm(1)
            width: cm(3)
            text_size: self.size[0], None
            text: 'Select index'
        Spinner:
            id: playlist_spinner2
            size_hint: None, None
            width: content.width - spinlabel2.width
            height: cm(1)
            text: 'Next'
            values: 'Beginning', 'Next', 'End'

        Widget:
            size_hint_y: None
            height: cm(0.5)

        Button:
            size_hint: 0.5, None
            height: cm(1)
            text: 'Cancel'
            on_release: root.dismiss()
        Button:
            id: addbtn
            size_hint: 0.5, None
            height: cm(1)
            text: 'Add'
'''


class FileAdderDialog(Popup):
    def __init__(self, playlists, on_add, **kwargs):
        super(FileAdderDialog, self).__init__(**kwargs)
        self.ids.playlist_spinner.values = [i for i in playlists]
        self.ids.addbtn.bind(on_release=lambda *args: self.accept_files(on_add))

    def add_file(self, path):
        name = os.path.split(path)[1]
        self.ids.file_list.data.append({'text':name, 'path':path})
        self.ids.filecounter.text = '%s files' % (len(self.ids.file_list.data))

    def accept_files(self, func):
        templist = []
        for i in self.ids.file_list.data:
            try:
                templist.append(
                    {'text':unicode(i['text'].decode('utf-8')),
                    'path':unicode(i['path'].decode('utf-8')) })
            except:
                templist.append(
                    {'text':unicode(i['text']),
                    'path':unicode(i['path']) })
        func(
            self.ids.playlist_spinner.text,
            self.ids.playlist_spinner2.text,
            templist
        )
        self.dismiss()


class FileViewClass(RecycleDataViewBehavior, Label):
    def __init__(self, **kwargs):
        super(FileViewClass, self).__init__(**kwargs)

    def refresh_view_attrs(self, rv, index, data):
        super(FileViewClass, self).refresh_view_attrs(rv, index, data)
        self.index = index
        self.text_size[0] = rv.width


class FileAdderRecycleView(RecycleView):
    def __init__(self, **kwargs):
        super(FileAdderRecycleView, self).__init__(**kwargs)
        self.scroll_type = ['bars', 'content']
        self.layout = RecycleBoxLayout(
            orientation = 'vertical', size_hint_y = None,
            default_size = (None, cm(0.5)), default_size_hint = (1, None))
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.bind(width=self.layout.setter('width'))
        self.add_widget(self.layout)
        self.viewclass = 'FileViewClass'


Builder.load_string(kv)
