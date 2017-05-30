from kivy_soil.hover_behavior import HoverBehavior
from kivy.uix.modalview import ModalView
from kivy.uix.popup import Popup
from kivy.lang import Builder


class AppPopup(HoverBehavior, Popup):
    hover_height = 20

    def open(self):
        hover_behavior.min_hover_height = self.hover_height
        super(AppPopup, self).open()

    def dismiss(self):
        hover_behavior.min_hover_height = 0
        super(AppPopup, self).dismiss()
