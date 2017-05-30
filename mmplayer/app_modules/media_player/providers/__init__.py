from kivy.utils import platform
from .audio_player_kivy import AudioPlayer
from .video_player_kivy import AppVideoPlayer


if platform == 'android':
    from android_player import AndroidPlayer
    provider_list = [
        AppVideoPlayer,
        AndroidPlayer
    ]

else:
    provider_list = [
        AppVideoPlayer,
        AudioPlayer
    ]
