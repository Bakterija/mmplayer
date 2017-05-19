from . import info_ffprobe
from time import time

info_cache = {}

def get_info(media_list):
    t0 = time()
    info_list = [info_ffprobe.get_info(items['path']) for items in media_list]
    print (len(info_list))
    print(time() - t0)
    return info_list
