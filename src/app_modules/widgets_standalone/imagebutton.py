from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.lang import Builder

Builder.load_string('''
<ImageButton>:
''')

class ImageButton(ButtonBehavior, Image):
    pass
