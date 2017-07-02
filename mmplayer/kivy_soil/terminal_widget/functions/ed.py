from kivy_soil.text_editor import TextEditorPopup
from ._base import FunctionBase
from kivy.clock import Clock


class Function(FunctionBase):
    name = 'ed'
    doc = 'text editor'
    methods_subclass = {'empty': ''}

    def empty(self):
        a = TextEditorPopup()
        a.open()
