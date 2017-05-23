from kivy.uix.stacklayout import StackLayout
from kivy.lang import Builder
from app_modules.kb_system import keys
from app_modules.kb_system.canvas import FocusBehaviorCanvas
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.properties import NumericProperty, StringProperty
from kivy.properties import ListProperty
from kivy.app import App
from kivy.clock import Clock
from app_modules.widgets_standalone.app_recycleview import (
AppRecycleView, AppRecycleBoxLayout, AppRecycleViewClass)
from kivy.logger import Logger
import traceback
import importlib
import os
from kivy.uix.button import Button


Builder.load_string('''
<PluginManager>:
    viewclass: 'PluginButton'
    SingleSelectRecycleBox:
        orientation: 'vertical'
        size_hint: None, None
        height: self.minimum_height
        width: root.width - root.bar_width
        default_size_hint: 1, None
        default_size: None, None
        spacing: default_spacing

<PluginButton>:
''')


class PluginButton(AppRecycleViewClass, Button):
    name = StringProperty()

    def __init__(self, **kwargs):
        super(PluginButton, self).__init__(**kwargs)
        self.bind(name=self.setter('text'))


class PluginManager(FocusBehaviorCanvas, AppRecycleView):
    plugins = ListProperty()

    def __init__(self, **kwargs):
        super(PluginManager, self).__init__(**kwargs)
        pl_files = os.listdir('plugins/')
        new_plugins = []
        for x in pl_files:
            if x[0] == '_':
                continue
            try:
                module_name = x[:-3]
                Logger.info('PluginManager: importing %s' % (module_name))
                new = importlib.import_module('plugins.' +module_name)
                new_plugins.append({'name': module_name, 'plugin': new})
            except Exception as e:
                Logger.error(
                    'PluginManager: failed to import %s\n%s' % (
                        module_name, traceback.format_exc()))
        self.plugins = new_plugins

    def on_plugins(self, _, value):
        print ('ON_PLUGINS', len(value))
        new_data = []
        for items in value:
            plg = items['plugin']
            new_data.append({
                'name': plg.NAME,
                'background_normal': plg.IMAGE})
        self.data = new_data
