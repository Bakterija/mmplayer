from utils import get_unicode
import subprocess

def get_info(path):
    cmd = ('ffprobe', '-v', 'error', '-show_format', '-show_streams', path)
    popen = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
        stderr=subprocess.PIPE, universal_newlines=True)
    info = popen.communicate()[0]

    return info
