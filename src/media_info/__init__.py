from app_modules.compat_queue import Queue
from threading import Thread
from . import info_ffprobe
from time import time, sleep
from app_modules import appworker
from kivy.clock import Clock
from kivy.logger import Logger

cache = {}
worker_state = {}
remaining_tasks = 0
scheduled_paths = []
info_update_callback = None
detected_ffprobe = None

def get_info(media_list):
    t0 = time()
    info_list = [info_ffprobe.get_info(items['path']) for items in media_list]
    return info_list

def get_info_async(media_path):
    global cache, scheduled_paths, worker_state
    if not media_path in cache:
        cache[media_path] = {}
        worker_state[media_path] = 'waiting'
        scheduled_paths.append(media_path)

def get_info_async_done(media_path, info):
    global cache, info_update_callback, remaining_tasks, worker_state
    global detected_ffprobe
    cache[media_path] = info
    worker_state[media_path] = 'done'
    remaining_tasks -= 1
    if info_update_callback:
        info_update_callback(media_path, info)

def add_priority_path(media_path):
    global scheduled_paths
    scheduled_paths.append(media_path)

def update_schedule(dt):
    t0 = time()
    global scheduled_paths, qu, remaining_tasks
    if remaining_tasks < 4:
        t_paths = []
        remlist = []
        for i, x in enumerate(reversed(scheduled_paths)):
            if x not in t_paths:
                t_paths.append(x)
                worker_state[x] = 'working'
            if len(t_paths) == 10:
                break
            remlist.append(i)

        for x in remlist:
            del scheduled_paths[-1]

        for x in reversed(t_paths):
            qu.put(x)
            remaining_tasks += 1
    # print (time() - t0, remaining_tasks, len(scheduled_paths))

def worker_thread(ind, queue):
    if info_ffprobe.find_ffprobe():
        while True:
            sleep (0.1)
            tt = qu.get()
            result = info_ffprobe.get_info(tt)
            Clock.schedule_once(lambda *a: get_info_async_done(tt, result))
    else:
        Clock.schedule_once(on_ffprobe_not_found, 0)


qu = Queue()
def start_workers(count):
    Clock.schedule_interval(update_schedule, 0.3)
    for i in range(count):
        t = Thread(target=worker_thread, args=(i, qu,))
        t.daemon = True
        t.start()

def on_ffprobe_not_found(*args):
    global detected_ffprobe
    detected_ffprobe = False
    Clock.unschedule(update_schedule)
    Logger.warning('media_info: ffprobe was not found, '
                   'media information will not be added')
