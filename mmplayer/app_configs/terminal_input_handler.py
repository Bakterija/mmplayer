from .config_base import ConfigBase


class Config(ConfigBase):
    root = None

    def __init__(self):
        self.input_switch = {
            'play': self.handle_play,
            'screen': self.handle_screen,
            'help': self.handle_help
        }

    def load_before(self, root_widget):
        self.root = root_widget

    def load_after(self, root_widget):
        root_widget.ids.terminal_widget.input_callback = self.handle_input

    def handle_input(self, terminal, widget, text):
        if text:
            nt = text.split(' ')
            nlen = len(nt)
            try:
                self.input_switch[nt[0]](nt, nlen)
                terminal.data.append({'text': text})
            except KeyError as e:
                terminal.data.append(
                    {'text': 'Key {} does not exist'.format(e)})
            except Exception as e:
                terminal.data.append({'text': str(e)})

    def handle_play(self, nt, len):
        path = ' '.join(nt[1:])
        self.root.media_control.insert_queue(path, path, 'End')
        self.root.mplayer.start(-1)

    def handle_screen(self, nt, len):
        self.root.switch_screen(nt[1])

    def handle_help(self, text, len):
        pass

    def load_with_args(self, *args, **kwargs):
        pass
