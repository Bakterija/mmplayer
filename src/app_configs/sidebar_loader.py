from .config_base import ConfigBase
from kivy.metrics import cm

WIDTH_SECTION = cm(0.6)
WIDTH_SEPARATOR = cm(0.8)
WIDTH_TEXT = cm(0.8)


class Config(ConfigBase):
    root = None

    def set_defaults(self, root):
        self.default_list = [
            self.get_section('SCREENS'),
            self.get_button(
                'Main', lambda: root.switch_screen('media'), None),
            self.get_button(
                'Queue', lambda: root.switch_screen('queue'), None),
            self.get_button(
                'Video', lambda: root.switch_screen('video'), None),
            self.get_button(
                'Browser', lambda: root.switch_screen('browser'), None),
        ]

    def load_before(self, root_widget):
        self.root = root_widget
        self.set_defaults(root_widget)

    def load_after(self, root_widget):
        pass

    def get_button(self, name, left_click, right_click):
        return {
            'text': name, 'wtype': 'text', 'can_select': True,
            'func': left_click, 'func2': right_click, 'height': WIDTH_TEXT
        }

    def get_section(self, name):
        return {'text': name, 'wtype': 'section', 'height': WIDTH_SECTION}

    def get_separator(self):
        return {'text': '', 'wtype': 'separator', 'height': WIDTH_SEPARATOR}

    def get_playlist_button(self, item):
        return self.get_button(
            item['name'],
            lambda item=item: {
                self.root.media_control.open_playlist(item),
                self.root.switch_screen("media")
            },
            lambda item=item: {
                self.root.media_control.playlist_cmenu_popup(item)
            })

    def load_with_args(self, *args, **kwargs):
        mgui_widget = args[0]
        playlist_dict = args[1]

        new_list = self.default_list
        nm = ''

        item = {}

        for section, playlists in  sorted(playlist_dict.items()):
            for plist in sorted(playlists, key=lambda x: x.name):
                # If section was added already, add playlist buttons
                # else add new section
                item['name'] = plist.name
                if nm == section:
                    new_list.append(self.get_playlist_button(item))
                else:
                    nm = section
                    new_list.append(self.get_separator())

                    new_list.append(self.get_section(section.upper()))

                    new_list.append(self.get_playlist_button(item))

        new_list.append(self.get_separator())

        self.root.sidebar_items = new_list
