from ._base import PluginBase
from kivy.clock import Clock


class Plugin(PluginBase):
    name = 'wait'
    doc = 'stops term system input handling for arg[0] seconds'
    methods_subclass = {}
    _grabbed_input = None

    def __init__(self, **kwargs):
        self._grabbed_input = []

    def on_import(self, term_system):
        self.term_system = term_system

    def ungrab_input(self, dt):
        if self.term_system.grab_input == self:
            self.term_system.grab_input = None
            self.term_system.add_text('# Done waiting')
        for x in self._grabbed_input:
            self.term_system.handle_input(x)

    def handle_input(self, term_system, term_globals, exec_locals, text):
        if term_system.grab_input == self:
            self._grabbed_input.append(text)
        else:
            grabtime = float(self.slice_fname(text)[1])
            term_system.grab_input = self
            Clock.schedule_once(self.ungrab_input, grabtime)
            return '# Waiting %s seconds' % (grabtime)
