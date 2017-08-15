from kivy_soil.kb_system.compat_widgets.scrollview import AppScrollView
from kivy_soil.kb_system.compat_widgets.popup import AppPopup
from kivy.properties import StringProperty
from kivy.uix.label import Label


class PopupLabel(AppPopup):
    text = StringProperty()

    def __init__(self, **kwargs):
        super(PopupLabel, self).__init__(**kwargs)
        scroller = AppScrollView()
        lbl = Label(
            size_hint_y=None, text_size=(scroller.width, None), text=self.text)
        scroller.bind(size=self._update_text_size)
        lbl.bind(texture_size=self._update_text_widget_size)
        scroller.add_widget(lbl)
        self.content, self.lbl = scroller, lbl

    def on_key_down(self, key, modifier):
        self.content.on_key_down(key, modifier)

    def _update_text_size(self, _, value):
        self.lbl.text_size = (value[0], None)

    def _update_text_widget_size(self, _, value):
        self.lbl.size = value

    @staticmethod
    def quick_open(text, title):
        new = PopupLabel(text=text, title=title)
        new.open()
        return new
