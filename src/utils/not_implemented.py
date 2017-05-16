from kivy.app import App
from kivy.logger import Logger


def show_error():
    app = App.get_running_app()
    root = app.root_widget
    Logger.error('Not implemented')
    root.on_error('Not implemented')
