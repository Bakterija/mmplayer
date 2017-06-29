from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from widgets.compat_textinput import CompatTextInput
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.logger import Logger
from kivy.clock import Clock


class AppRecycleViewQuickFind(object):
    '''Mixin for AppRecycleView. Searches, scrolls, selects widgets
    when text input is received in it's do_quickfind method'''

    receive_textinput = True
    quickfind_reset_time = 1.0
    quickfind_key = StringProperty('text')
    _quickfind_text = StringProperty('')
    quickfind_font_size = NumericProperty(12)
    _quickfind_label = None

    def __init__(self, **kwargs):
        super(AppRecycleViewQuickFind, self).__init__(**kwargs)
        self.fbind('on_focus_textinput', self.do_quickfind)
        self.fbind('_quickfind_text', self._update_quickfind_label)

    def _update_quickfind_label(self, _, value):
        qlabel = self._quickfind_label
        if value:
            if qlabel:
                qlabel.text = value
            else:
                self._quickfind_label = CompatTextInput(
                    text=value, size_hint=(None, None), pos=self.pos,
                    font_size=self.quickfind_font_size,
                    size=(self.width, int(self.quickfind_font_size * 2.3)))
                Window.add_widget(self._quickfind_label)
        else:
            if qlabel:
                Window.remove_widget(qlabel)
                self._quickfind_label = None

    def do_quickfind(self, _, text):
        Clock.unschedule(self._reset_quickfind_text)
        text = self._quickfind_text + text
        self._quickfind_text = text
        result = self.find_index_by_text(self.quickfind_key, text, match=True)
        index = None
        selectable = False
        data_text = ''

        if result:
            index = result[0]
            selectable = True
            data = self.data[index]
            data_text = data[self.quickfind_key]
            if 'selectable' in data and not data['selectable']:
                selectable = False

            if selectable:
                self.scroll_to_index(index)
                delayed = lambda dt: self.children[0].select_with_touch(index)
                Clock.schedule_once(delayed, 0)
        if not selectable:
            self.children[0].deselect_all()

        Logger.info(
            ('AppRecycleViewQuickFind: do_quickfind: '
             'text="{}" index="{}" selectable="{}" data_text={}').format(
                 text, index, selectable, data_text))
        Clock.schedule_once(
            self._reset_quickfind_text, self.quickfind_reset_time)

    def _reset_quickfind_text(self, *args):
        self._quickfind_text = ''
