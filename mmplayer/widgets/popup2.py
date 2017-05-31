from kivy.uix.modalview import ModalView
from kivy_soil import hover_behavior
from kivy_soil.kb_system import keys
from kivy.uix.popup import Popup
from kivy.lang import Builder


class AppPopup(hover_behavior.HoverBehavior, Popup):
    hover_height = 20
    grab_keys = [keys.ESC]

    def open(self):
        hover_behavior.min_hover_height = self.hover_height
        super(AppPopup, self).open()

    def dismiss(self):
        hover_behavior.min_hover_height = 0
        super(AppPopup, self).dismiss()
