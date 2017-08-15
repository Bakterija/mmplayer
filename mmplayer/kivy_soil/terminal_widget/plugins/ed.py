from kivy_soil.text_editor import TextEditorPopup
from ._base import PluginBase
from kivy.clock import Clock


class Plugin(PluginBase):
    name = 'ed'
    doc = 'text editor'
    methods_subclass = {'empty': ''}

    def empty(self):
        a = TextEditorPopup()
        a.open()
