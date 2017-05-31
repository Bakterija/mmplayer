from kivy.app import App
from kivy.logger import Logger


def show_error(feature=None):
    '''Displays error notification in app and logs error'''
    app = App.get_running_app()
    root = app.root_widget
    if feature:
        text = '%s not implemented' % (feature)
    else:
        text = 'Not implemented'
    Logger.error(text)
    root.on_error(text)
