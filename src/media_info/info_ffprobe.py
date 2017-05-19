from utils import get_unicode
import subprocess

def get_info(path):
    cmd = ('ffprobe', '-v', 'error', '-show_format', '-show_streams', path)
    popen = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
        stderr=subprocess.PIPE, universal_newlines=True)
    info = popen.communicate()[0]
    info = parse_output(info)
    return info

def parse_output(info):
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
                key = get_unicode(x[:b])
                value = get_unicode(x[b+1:])
                info_dict[sub_dict][key] = value
                if key == 'duration':
                    info_dict['duration'] = value
                elif key == 'codec_type' and value == 'video':
                    info_dict['is_video'] = True
    return info_dict
