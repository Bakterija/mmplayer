from config_base import ConfigBase


class Config(ConfigBase):
    root = None
    default_list = []

    def set_defaults(self, root):
        self.default_list = [
            {'text': 'SCREENS', 'wtype': 'section'},
            self.get_button(
                'Main', lambda: root.switch_screen('media'), None),
            self.get_button(
                'Queue', lambda: root.switch_screen('queue'), None),
            self.get_button(
                'Video', lambda: root.switch_screen('video'), None),
            self.get_button(
                'Browser', lambda: root.switch_screen('browser'), None),
            {'text': '', 'wtype': 'separator'}
        ]

    def load_before(self, root_widget):
        self.root = root_widget
        self.set_defaults(root_widget)

    def load_after(self, root_widget):
        pass

    def get_button(self, name, left_click, right_click):
        return {
            'text': name, 'wtype': 'text', 'can_select': True,
            'func': left_click, 'func2': right_click
        }

    def get_playlist_button(self, item):
        return {
            'text': item['name'],
            'wtype': 'text',
            'can_select': True,
            'func': lambda item=item: {
                self.root.media_control.open_playlist(item),
                self.root.switch_screen("media")
            },
            'func2': lambda item=item: {
                self.root.media_control.playlist_cmenu_popup(item)
            }
        }

    def load_with_args(self, *args, **kwargs):
        mgui_widget = args[0]
        playlists = args[1]

        new_list = self.default_list

        new_list.append({'text': 'PLACES', 'wtype': 'section'})
        nm = 'places'

        for section in iter(playlists):
            for item in iter(section):
                # If section was added already, add playlist buttons
                # else add new section
                if nm == item['section']:
                    new_list.append(self.get_playlist_button(item))
                else:
                    nm = item['section']
                    new_list.append(
                        {'text': '', 'wtype': 'separator'})

                    new_list.append(
                        {'text': item['section'].upper(), 'wtype': 'section'})

                    new_list.append(self.get_playlist_button(item))

        new_list.append({'text': '', 'wtype': 'separator'})

        self.root.sidebar_items = new_list
