from kivy.core.window.window_sdl2 import WindowSDL
from kivy.core.window import Window
from kivy.logger import Logger


def new_release_keyboard(self, *largs):
    super(WindowSDL, self).release_keyboard(*largs)
    if self._system_keyboard.widget:
        self._win.hide_keyboard()
    self._sdl_keyboard = None
    return True


WindowSDL.release_keyboard = new_release_keyboard
Logger.warning('window_patch: patched kivy Window.release_keyboard')
