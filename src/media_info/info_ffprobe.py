from kivy.utils import platform
from utils import get_unicode
import subprocess
from os.path import exists as path_exists

cmd_ffprobe = None

def find_ffprobe():
    global cmd_ffprobe
    found = False
    if platform == 'linux':
        try:
            cmd = ('ffprobe', '-h')
            cmd_ffprobe = (
                'ffprobe', '-v', 'error', '-show_format', '-show_streams')
            found = True
        except:
            pass
    elif platform == 'win':
        if path_exists('bin/ffprobe.exe'):
            cmd_ffprobe = (
                'bin\\ffprobe.exe', '-v', 'error', '-show_format',
                '-show_streams')
            found = True
    return found

def get_info(path):
    global cmd_ffprobe
    cmd = (*cmd_ffprobe, path)
    popen = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
        stderr=subprocess.PIPE)
    info = popen.communicate()[0]
    info = parse_output(info)
    return info

def parse_output(info):
    info = get_unicode(info)
    lines = info.splitlines()
    info_dict = {'is_video': False}
    stream_cnt = 0
    sub_dict = ''
    for x in lines:
        if x == '[FORMAT]':
            sub_dict = 'format'
            info_dict[sub_dict] = {}
        elif x == '[STREAM]':
            sub_dict = 'stream{}'.format(stream_cnt)
            info_dict[sub_dict] = {}
            stream_cnt += 1
        elif x[:2] == '[/':
            sub_dict = ''
        if sub_dict:
            b = x.find('=')
            if b != -1:
                key = x[:b]
                value = x[b+1:]
                info_dict[sub_dict][key] = value
                if key == 'duration':
                    info_dict['duration'] = value
                elif key == 'codec_type' and value == 'video':
                    info_dict['is_video'] = True
    return info_dict
