from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.modalview import ModalView
from app_modules.behaviors import hover_behavior


class AppPopup(hover_behavior.HoverBehavior, Popup):
    hover_height = 20

    def open(self):
        hover_behavior.min_hover_height = self.hover_height
        super(AppPopup, self).open()

    def dismiss(self):
        hover_behavior.min_hover_height = 0
        super(AppPopup, self).dismiss()
