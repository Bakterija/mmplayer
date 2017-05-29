from kivy.utils import platform
from utils import get_unicode
from os.path import exists as path_exists
import subprocess
import utils

cmd_ffprobe = None


def find_ffprobe():
    global cmd_ffprobe
    found = False
    cmd = ('ffprobe')
    found = utils.which(cmd)
    if found:
        cmd_ffprobe = [found, '-v', 'error', '-show_format', '-show_streams']
    else:
        if platform == 'win':
            fp = 'bin/ffprobe.exe'
            if path_exists(fp):
                cmd_ffprobe = [
                    fp, '-v', 'error', '-show_format', '-show_streams']
            found = True
    return found

def get_info(path):
    global cmd_ffprobe
    cmd = cmd_ffprobe + [path]
    popen = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
        stderr=subprocess.PIPE)
    info = popen.communicate()[0]
    info = parse_output(info)
    return info

def parse_output(info):
    info_dict = {}
    info = get_unicode(info)
    lines = info.splitlines()
    is_video = False
    duration = -1
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
                    try:
                        duration = float(value)
                    except Exception as e:
                        Logger.error('info_ffprobe: %s' % (e))
                elif key == 'codec_type' and value == 'video':
                    is_video = True
    info_dict['is_video'] = is_video
    info_dict['duration'] = duration
    return info_dict
