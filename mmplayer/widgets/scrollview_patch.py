from kivy.uix.scrollview import ScrollView
from kivy.properties import ListProperty
from kivy.logger import Logger

ScrollView.bar_background_color = ListProperty([0.3, 0.3, 0.3, 0.7])

Logger.warning('scrollview_patch: added bar_background_color property')
