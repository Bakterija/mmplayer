from __future__ import print_function
from kivy.properties import BooleanProperty, StringProperty, DictProperty
from kivy.properties import ListProperty, NumericProperty, ObjectProperty
from .playlist_loader import loader as playlist_loader
from .playlist_loader.base import BasePlaylist
from utils.settings import SettingHandler
from kivy.event import EventDispatcher
from kivy.uix.widget import Widget
from kivy.utils import platform
from kivy.logger import Logger
from kivy.clock import Clock
import global_vars as gvars
from time import time
import traceback
import media_info


class MediaController(SettingHandler, EventDispatcher):
    playlist_ids = DictProperty()

    playlists = DictProperty()
    '''DictProperty with sections with lists of playlist objects'''

    cur_played_playlist = ObjectProperty()
    '''ObjectProperty of currently played playlist'''

    cur_viewed_playlist = ObjectProperty()
    '''ObjectProperty of last opened playlist, ignores mplayer queue'''

    playing_name = StringProperty()
    '''StringProperty file name of current played media'''

    playing_path = StringProperty()
    '''StringProperty file path of current played media'''

    playing_seek_value = NumericProperty(0)
    '''NumericProperty seek seconds of current played media'''

    playing_seek_max = NumericProperty(0)
    '''NumericProperty length of current played media in seconds'''

    playing_id = NumericProperty()
    playing_state = StringProperty()
    last_media = None
    '''dict of currently played media file'''

    volume = NumericProperty(-1)
    shuffle = BooleanProperty(False)
    muted = BooleanProperty(False)
    _volume_before_muted = 0

    videoframe = None
    videoframe_is_visible = BooleanProperty(False)
    playing_video = BooleanProperty(False)
    videoframe_small = None

    default_relative_volume = 10

    store_properties = (('volume', 100), ('shuffle', False))
    store_name = 'MediaController'

    def __init__(self, mplayer, **kwargs):
        self.register_event_type('on_playlist_update')
        super(MediaController, self).__init__(**kwargs)
        self.mplayer = mplayer
        self.mplayer.bind(on_start=self._on_mplayer_start)
        self.mplayer.bind(on_video=self.on_mplayer_video)
        self.fbind('volume', self._set_mplayer_volume)
        Clock.schedule_interval(self.update_seek, 0.1)
        media_info.info_update_callback = self.on_media_info_update
        media_info.update_timer = 0.05
        playlist_loader.bind(on_playlists=self._on_reset_playlists_done)
        Clock.schedule_once(lambda *a: media_info.start_workers(2), 1)

    def _set_mplayer_volume(self, _, value):
        self.mplayer.set_volume(value)

    def set_volume(self, value):
        value = int(value)
        if value < 0:
            value = 0
        elif value > 100:
            value = 100
        if self.muted and value > 0:
            self.muted = False
        self.volume = value
        Logger.info('MediaController: set_volume: %s' % (value))

    def set_volume_relative(self, value):
        value = int(value)
        if self.muted:
            self.set_volume(self._volume_before_muted + value)
        else:
            self.set_volume(self.volume + value)

    def volume_increase(self, *args):
        self.set_volume_relative(self.default_relative_volume)

    def volume_decrease(self, *args):
        self.set_volume_relative(-self.default_relative_volume)

    def on_muted(self, _, value):
        if value:
            self._volume_before_muted = self.volume
            self.set_volume(0)
            Logger.info('MediaController: muted')
        else:
            self.set_volume(self._volume_before_muted)
            Logger.info('MediaController: unmuted')

    def toggle_shuffle(self):
        self.shuffle = not self.shuffle

    def toggle_mute(self):
        self.muted = not self.muted

    def on_shuffle(self, _, value):
        self.mplayer.shuffle = value
        Logger.info(
            'MediaController: on_shuffle: set mplayer shuffle to %s' % value)

    def on_playlist_update(self, *args):
        '''Event fired when playlist DictProperty is updated'''
        pass

    def _on_mplayer_start(self):
        '''Updates attributes when mplayer starts media'''
        state = self.mplayer.get_state_all()
        media = state['cur_media']

        if self.last_media:
            last_id = self.last_media['id']
            plname = self.last_media.get('playlist_name', None)
            playlist = playlist_loader.get_playlist_by_name(plname)
            if playlist.media[last_id]['state'] == 'playing':
                playlist.media[last_id]['state'] = 'normal'
                self.last_media = 'normal'

        self.playing_id = media.get('id')
        plname = media.get('playlist_name', None)
        media_playlist = playlist_loader.get_playlist_by_name(plname)
        media_playlist.media[self.playing_id]['state'] = 'playing'
        # if 'id' in media:
        #     index = media['id']
            # self.playing_id = index
            # if self.cur_played_playlist:
            #     self.cur_played_playlist.set_playing(index)
            # else:
        #     media['state'] = 'playing'
        # else:
        #     self.playing_id = -9
        #     if self.cur_played_playlist:
        #         self.cur_played_playlist.remove_playing()
        # media['state'] = 'playing'

        self.playing_name = media['name']
        self.playing_path = media['path']
        self.last_media = media
        self.refresh_playlist_view()
        self.refresh_queue_view()

    def on_mplayer_video(self, value, player=None):
        '''Updates self.playing_video property when video starts/stops'''
        if value:
            self.playing_video = True
        else:
            self.playing_video = False

    def on_playlist_media(self, playlist, media):
        '''Updates playlist view when playlist changes'''
        if self.cur_viewed_playlist:
            if playlist.path == self.cur_viewed_playlist.path:
                self.view_playlist.update_data()

    def attach_playlist_view(self, widget):
        self.view_playlist = widget
        widget.mcontrol = self
        self.bind(cur_viewed_playlist=widget.set_viewed_playlist)

    def attach_queue_view(self, widget):
        self.view_queue = widget
        widget.mcontrol = self

    def start_playlist_from_index(self, name, path, index, id, btn):
        '''Add selected index and all indexes after it into queue,
        then start playing'''
        self.mplayer.reset()
        self.cur_played_playlist = self.cur_viewed_playlist
        new_queue = list(self.view_playlist.data[index:])
        self.mplayer.queue = new_queue
        self.view_queue.set_data(new_queue)
        stat = self.mplayer.start(0)

    def start_queue(self, index):
        '''Start playing queue at index argument'''
        stat = self.mplayer.start(index)

    def start_selection(self, new_queue, cur_playlist=None):
        '''Add list of dicts into queue and start playing at index 0'''
        self.mplayer.reset()
        if cur_playlist:
            self.cur_played_playlist = cur_playlist
        self.mplayer.queue = new_queue
        self.view_queue.set_data(new_queue)
        self.start_queue(0)

    def add_to_queue(self, new_media):
        '''Add media dicts at end of queue'''
        new_queue = self.mplayer.queue + new_media
        self.mplayer.queue = new_queue
        self.view_queue.set_data(new_queue)

    def queue_remove_indexes(self, index_list):
        '''Remove media dicts from queue with index_list indexes'''
        for x in reversed(index_list):
            del self.mplayer.queue[x]
        self.view_queue.set_data(self.mplayer.queue)
        Logger.info('MediaController: removed %s files from queue' % (
            len(index_list)))

    def clear_queue(self, *args):
        '''Clear queue and it's view'''
        self.mplayer.reset()
        self.view_queue.clear_data()

    def play_pause(self):
        '''Toggle play and pause'''
        state = self.mplayer.get_state()
        if state in ('pause', 'stop'):
            self.mplayer.play()
        else:
            self.mplayer.pause()

    def play_next(self):
        '''Play next in mplayer queue'''
        self.mplayer.next()

    def play_previous(self):
        '''Play previous in mplayer queue'''
        self.mplayer.previous()

    def jump_to_current_index(self, screen):
        '''Move view to currently played media'''
        Logger.info('MediaController: jump_to_current_index(%s)' % (screen))
        if screen == 'playlist':
            pl = self.view_playlist
        elif screen == 'queue':
            pl = self.view_queue

        index = self.find_playing(pl.data)
        if index is not None:
            pl.scroll_to_index(index)
            pl.children[0].select_with_touch(index)
            Logger.info('MediaController: jumping to index %s' % (index))
        else:
            Logger.info('MediaController: played index is not in view')

    @staticmethod
    def find_playing(playlist):
        '''Finds dict in list where state == 'playing',
        returns -1 nothing if not found'''
        for i, x in enumerate(playlist):
            if x['state'] == 'playing':
                return i

    def refresh_playlist_view(self):
        self.view_playlist.refresh_from_data()

    def refresh_queue_view(self):
        self.view_queue.refresh_from_data()

    def update_seek(self, *arg):
        '''Updates playing_seek_value, playing_seek_max properties and
        playing_state'''
        pos = self.mplayer.get_mediaPos()
        dur = self.mplayer.get_mediaDur()
        self.playing_state = self.mplayer.get_state()
        if pos == -1:
            self.playing_seek_value = 0
        else:
            self.playing_seek_value = pos
        if dur == -1:
            self.playing_seek_max = 0
        else:
            self.playing_seek_max = dur

    def on_video_resize(self, size):
        '''Updates videoframe size when video size changes'''
        if self.playing_video:
            if self.videoframe and self.videoframe_is_visible:
                self.videoframe.children[0].size = size

    def on_playing_video(self, _, value):
        '''Adds/removes small video widget when video starts/stops'''
        if not self.videoframe_small:
            Logger.error(''.join((
                'MediaController: on_playing_video:',
                'videoframe_small is None')))
        else:
            if value:
                self.video_show(self.mplayer.video_widget)
            else:
                self.video_hide()

    def video_show(self, widget):
        '''Adds video to small or big layout'''
        if self.videoframe and self.videoframe_is_visible:
            self.videoframe.add_widget(widget)
        else:
            self.videoframe_small.add_widget(widget)
            self.videoframe_small.animate_in()

    def video_hide(self):
        '''Removes video from layout'''
        if self.videoframe:
            self.videoframe.clear_widgets()
        if self.videoframe_small:
            self.videoframe_small.clear_widgets()
            self.videoframe_small.animate_out()

    def on_videoframe_is_visible(self, obj, val):
        '''Moves video from small videoframe and video screen'''
        if val:
            if self.videoframe_small.children:
                temp = self.videoframe_small.children[0]
                self.videoframe_small.remove_widget(temp)
                self.videoframe.add_widget(temp)
                self.videoframe_small.animate_out()
                temp.pos = (0, 0)
        elif self.videoframe.children and self.playing_video:
            temp = self.videoframe.children[0]
            self.videoframe.remove_widget(temp)
            self.videoframe_small.add_widget(temp)
            self.videoframe_small.animate_in()

    def on_dropfile(self, path, mouse_pos=None, playlist=None):
        '''Adds dropped files into playlists'''
        Logger.info(
            '{}: on_dropfile: path:{} mouse_pos:{} playlist:{}'.format(
                self.__class__.__name__, path, mouse_pos, playlist))

        found = False
        if playlist:
            if playlist == 'playlist':
                if self.cur_viewed_playlist:
                    self.cur_viewed_playlist.add_path(path)
                    found = True
            elif playlist == 'queue':
                pl = BasePlaylist()
                new_media = pl.get_files(path)
                self.add_to_queue(new_media)
                found = True

        if not found:
            Logger.warning('{}: no playlist selected'.format(
                self.__class__.__name__))

    def create_playlist(self, name):
        playlist_loader.create_playlist(name)
        self.reset_playlists()

    def remove_playlist(self, playlist_path):
        for section in self.playlists:
            for x in self.playlists[section]:
                if x.path == playlist_path:
                    x.remove()
                    self.reset_playlists()
                    break

    def reset_playlists(self, *args):
        self.time_reset = time()
        playlist_loader.update_from_directories_async((
            'media/playlists/', gvars.DIR_PLAYLISTS))

    def _on_reset_playlists_done(self, _, pl):
        self.playlists = pl
        self.dispatch('on_playlist_update', self.playlists)
        for section, playlists in self.playlists.items():
            for x in playlists:
                x.bind(media=self.on_playlist_media)
                self.playlist_ids[x.id] = x
        Logger.info(
            'MediaController: reset_playlists: %s sec' % (
                round(time() - self.time_reset, 2)))

    def open_playlist(self, target):
        for section, playlists in self.playlists.items():
            for instance in playlists:
                if target['path'] == instance.path:
                    self.cur_viewed_playlist = instance
                    # TODO Disable for now, add config setting later
                    # Clock.schedule_once(self.view_playlist.focus_widget, 0.2)
                    return

        Logger.warning('MediaController: playlist not found')

    def open_playlist_by_id(self, id):
        if id in self.playlist_ids:
            print('open ids playlist', id)
            pl = self.playlist_ids[id]
            target = {'name': pl.name, 'path': pl.path}
            self.open_playlist(target)
        else:
            print('playlist not in ids', id, self.playlist_ids)

    def on_media_info_update(self, path, info):
        '''Updates widget media info when media_info package loads new info'''
        pl = self.view_playlist.find_view_with_path(path)
        que = self.view_queue.find_view_with_path(path)
        if pl:
            pl.update_media_info(info)
        if que:
            que.update_media_info(info)
