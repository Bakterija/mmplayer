from kivy.uix.stacklayout import StackLayout
from kivy.properties import ListProperty
from kivy.graphics import InstructionGroup, Color, Rectangle


class BackgroundStackLayout(StackLayout):
    background_color = ListProperty()
    def __init__(self, **kwargs):
        super(BackgroundStackLayout, self).__init__(**kwargs)
        self.background = Rectangle(size=self.size, pos=self.pos)
        self.bg_color = Color(*self.background_color)
        self.instr = InstructionGroup()
        self.instr.add(self.bg_color)
        self.instr.add(self.background)
        self.canvas.before.add(self.instr)

        self.bind(background_color=self.on_background_color)
        self.bind(size=lambda obj, val: setattr(self.background, 'size', val))
        self.bind(pos=lambda obj, val: setattr(self.background, 'pos', val))

    def on_background_color(self, obj, val):
        if self.canvas:
            for i in self.instr.get_group(None):
                if type(i) is Color:
                    i.r, i.g, i.b, i.a = val[0], val[1], val[2], val[3]
                    return
