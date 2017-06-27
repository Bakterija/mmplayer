from kivy.properties import ListProperty
from kivy.event import EventDispatcher
from kivy.uix.widget import Widget
from kivy.logger import Logger
from kivy.clock import Clock
from kivy.app import App

update_callbacks = []
store = {}

class SettingHandler(object):
    store_properties = []
    store_name = ''

    def __init__(self, **kwargs):
        super(SettingHandler, self).__init__(**kwargs)
        if self.store_name and self.store_properties:
            self.update_store_properties()
        Clock.schedule_once(self.bind_on_stop, 0)
        self.is_stopping_now = False

    def bind_on_stop(self, *args):
        app = App.get_running_app()
        app.bind(on_stop=self.on_stop)

    def update_store_properties(self):
        global update_callbacks, store
        name = ''.join(('ED_', self.store_name))
        if name:
            for attr, default_value in self.store_properties:
                setter = self.setter(attr)
                store[attr] = (name, default_value, setter)
            for x in update_callbacks:
                x(store)

        else:
            Logger.warning(('SettingHandler: store_name for object {} '
                           'has not been set').format(self))

    def on_stop(self, app):
        if not self.is_stopping_now:
            self.is_stopping_now = True
            new_settings = []
            for attr, value in self.store_properties:
                new_settings.append((attr, getattr(self, attr)))

            app.root_widget.app_configurator.load_with_args(
               'user_settings', 'save', new_settings)
