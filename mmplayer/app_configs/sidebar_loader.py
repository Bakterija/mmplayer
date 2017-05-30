from .config_base import ConfigBase
from kivy.metrics import cm
import global_vars as gvars

WIDTH_SECTION = gvars.sidebar_section_height
WIDTH_SEPARATOR = gvars.rv_default_height
WIDTH_TEXT = gvars.rv_default_height


class Config(ConfigBase):
    root = None

    def set_defaults(self, root):
        wtype = 'screen_button'
        self.default_list = [
            self.get_section('SCREENS'),
            self.get_button(
                wtype, 'Main', lambda: root.switch_screen('main'), None),
            self.get_button(
                wtype, 'Queue', lambda: root.switch_screen('queue'), None),
            self.get_button(
                wtype, 'Video', lambda: root.switch_screen('video'), None),
        ]
        for x in self.default_list:
            if x['viewclass'] == 'SideBarButton':
                x['viewclass'] = 'SideBarScreenButton'

    def load_before(self, root_widget):
        self.root = root_widget
        self.set_defaults(root_widget)

    def load_after(self, root_widget):
        pass

    def get_button(self, wtype, name, left_click, right_click):
        return {
            'text': name, 'wtype': wtype, 'hovering': False, 'opened': False,
            'func': left_click, 'func2': right_click, 'height': WIDTH_TEXT,
            'viewclass': 'SideBarButton', 'selectable': True}

    def get_section(self, name):
        return {'text': name, 'wtype': 'section', 'height': WIDTH_SECTION,
                'viewclass': 'SideBarSection', 'selectable': False,
                'hovering': False, 'opened': False}

    def get_separator(self):
        return {'text': '', 'wtype': 'separator', 'height': WIDTH_SEPARATOR,
                'viewclass': 'SideBarSeparator', 'selectable': False,
                'hovering': False, 'opened': False}

    def get_playlist_button(self, item):
        btn = self.get_button(
            'playlist_button',
            item['name'],
            lambda : {
                self.root.media_control.open_playlist(item),
                self.root.switch_screen("media"),},
            None)
        btn['path'] = item['path']
        btn['viewclass'] = 'SideBarPlaylistButton'
        return btn

    def load_with_args(self, *args, **kwargs):
        mgui_widget = args[0]
        playlist_dict = args[1]

        new_list = list(self.default_list)
        cur_section = ''

        for section, playlists in  sorted(playlist_dict.items()):
            sorted_playlists = sorted(playlists, key=lambda x: x.name)
            for plist in sorted_playlists:
                # If section was added already, add playlist buttons
                # else add new section
                item = {
                    'name': plist.name, 'section': section, 'path': plist.path}

                if cur_section == section:
                    new_list.append(self.get_playlist_button(item))
                else:
                    cur_section = section
                    new_list.append(self.get_separator())

                    new_list.append(self.get_section(section.upper()))

                    new_list.append(self.get_playlist_button(item))

        new_list.append(self.get_separator())

        self.root.sidebar_items = new_list
