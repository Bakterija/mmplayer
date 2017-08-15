from ._base import PluginBase
from kivy.clock import Clock
from kivy.app import App


class Plugin(PluginBase):
    name = 'press_button'
    doc = 'Presses kivy buttons '
    methods_subclass = {
        'by_text': 'Searches button by text, presses when found',
        'print_button_text': 'Walks widget tree and prints text from buttons'}

    def print_button_text(self, *args):
        root = App.get_running_app().root
        ret = []
        for widget in root.walk():
            if hasattr(widget, 'on_press'):
                if hasattr(widget, 'text') and widget.text:
                    ret.append(widget.text)
        return ret

    def by_text(self, text):
        root = App.get_running_app().root
        found = False

        for widget in root.walk():
            if hasattr(widget, 'text') and text in widget.text:
                if hasattr(widget, 'on_press'):
                    found = True
                    widget.on_press()
                    Clock.schedule_once(widget.on_release, 0.2)
                    ret = '# Pressed button %s' % (widget)
                    break
                elif hasattr(widget, 'on_left_click'):
                    found = True
                    widget.on_left_click()
                    ret = '# Pressed button %s' % (widget)
                    break
        if not found:
            ret = '# Did not find button'

        return ret
