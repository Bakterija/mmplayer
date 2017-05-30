from app_modules.compat_queue import Queue
from app_modules import appworker
from kivy.logger import Logger
from threading import Thread
from kivy.clock import Clock
from time import time, sleep
from . import info_ffprobe
from kivy.app import App

cache = {}
worker_state = {}
remaining_tasks = 0
scheduled_paths = []
info_update_callback = None
detected_ffprobe = None

def get_info(media_path):
    return info_ffprobe.get_info(media_path)

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
    # print ('VISSS', media_path[-50:], info['duration'])
    if info_update_callback:
        info_update_callback(media_path, info)

def add_priority_path(media_path):
    global scheduled_paths
    scheduled_paths.append(media_path)

def _update(dt):
    t0 = time()
    global scheduled_paths, _qu_worker, _qu_results, remaining_tasks
    for i in range(20):
        try:
            result = _qu_results.get_nowait()
            if result:
                get_info_async_done(result[0], result[1])
        except:
            pass
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
            _qu_worker.put(x)
            remaining_tasks += 1
    # print (time() - t0, remaining_tasks, len(scheduled_paths))

def worker_thread(ind, qwork, qresults):
    while True:
        sleep (0.01)
        mpath = _qu_worker.get()
        info = info_ffprobe.get_info(mpath)
        # print ('CLOCK', mpath[-50:], info['duration'])
        # Clock.schedule_once(lambda *a: get_info_async_done())
        qresults.put((mpath, info))

_qu_worker = Queue()
_qu_results = Queue()
def start_workers(count):
    global _qu_worker, _qu_results
    if info_ffprobe.find_ffprobe():
        Clock.schedule_interval(_update, 0.2)
        for i in range(count):
            t = Thread(target=worker_thread, args=(i, _qu_worker, _qu_results))
            t.daemon = True
            t.start()
    else:
        on_ffprobe_not_found()

def on_ffprobe_not_found(*args):
    global detected_ffprobe
    detected_ffprobe = False
    Clock.unschedule(_update)
    app = App.get_running_app()
    wtext = ('media_info: ffprobe was not found, '
             'media information will not be added')
    app.root.display_warning(wtext)
    Logger.warning(wtext)
