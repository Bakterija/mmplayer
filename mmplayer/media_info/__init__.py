'''Looks for ffprobe. If ffprobe is found, workers can be started that will
load media information into cache asynchronously and store it in cache
gloal dict'''

from utils.compat_queue import Queue
from kivy.logger import Logger
from threading import Thread
from kivy.clock import Clock
from time import time, sleep
from . import info_ffprobe
from kivy.app import App
import appworker

cache = {}
'''Dict stores all loaded media information in dicts with media path keys'''

_qu_worker = []
_qu_worker_current_index = 0
_qu_results = Queue()

update_timer = 0.1

worker_state = {}
'''Dict stores media path key and state string pares,
state can be "waiting", "working", "done"
'''

remaining_tasks = 0
'''Integer count of tasks that haven't yet been finished by workers'''

scheduled_paths = []
'''List of paths that are waiting to be added into worker queues'''

info_update_callback = None
'''Callback function to call with media_path and info dict arguments
when a worker has loaded information for one file'''

detected_ffprobe = None
'''Default value is None, changes to True when ffprobe is found or
to False when it couldn't be found '''

def get_info(media_path):
    '''Run subprocess and get back media information for one path'''
    return info_ffprobe.get_info(media_path)

def get_info_async(media_path):
    '''Put media path into worker schedule and update state'''
    global cache, scheduled_paths, worker_state
    if not media_path in cache:
        cache[media_path] = {}
        worker_state[media_path] = 'waiting'
        scheduled_paths.append(media_path)

def get_info_async_done(media_path, info):
    '''Called when a worker finishes working on one media path'''
    global cache, info_update_callback, remaining_tasks, worker_state
    cache[media_path] = info
    worker_state[media_path] = 'done'
    remaining_tasks -= 1
    if info_update_callback:
        info_update_callback(media_path, info)

def add_priority_path(media_path):
    '''Puts media_path at end of scheduled_paths to be loaded soon'''
    global scheduled_paths
    scheduled_paths.append(media_path)

def _update(dt):
    '''Mainthread scheduled update fnction.
    Gets results from result queue, calls get_info_async_done.
    Then puts new tasks into worker queue, if remaining_tasks is low'''
    t0 = time()
    global scheduled_paths, _qu_worker, _qu_results, remaining_tasks
    global worker_state, _qu_worker_current_index, update_timer
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
            if x in worker_state and worker_state[x] == 'done':
                pass
            else:
                if x not in t_paths:
                    t_paths.append(x)
                    worker_state[x] = 'working'
                if len(t_paths) == 10:
                    break
            remlist.append(i)

        for x in remlist:
            del scheduled_paths[-1]

        len_worker_queue = len(_qu_worker) - 1
        for x in reversed(t_paths):
            _qu_worker[_qu_worker_current_index].put(x)
            _qu_worker_current_index += 1
            if _qu_worker_current_index > len_worker_queue:
                _qu_worker_current_index = 0
            remaining_tasks += 1

    if update_timer != -1:
        Clock.schedule_once(_update, update_timer)
    # print (time() - t0, remaining_tasks, len(scheduled_paths))

def worker_thread(ind, qwork, qresults):
    '''Gets work from worker queue, runs ffprobe subprocess,
    puts results in result queue'''
    while True:
        sleep (0.01)
        mpath = qwork.get()
        info = info_ffprobe.get_info(mpath)
        qresults.put((mpath, info))

def start_workers(count):
    '''Starts workers and schedules _update function with interval'''
    global _qu_worker, _qu_results, update_timer
    if info_ffprobe.find_ffprobe():
        Clock.schedule_once(_update, update_timer)
        for i in range(count):
            new_queue = Queue()
            _qu_worker.append(new_queue)
            t = Thread(target=worker_thread, args=(i, new_queue, _qu_results))
            t.daemon = True
            t.start()
    else:
        on_ffprobe_not_found()

def on_ffprobe_not_found(*args):
    '''Sets detected_ffprobe global to False and logs failure'''
    global detected_ffprobe
    detected_ffprobe = False
    Clock.unschedule(_update)
    app = App.get_running_app()
    wtext = ('media_info: ffprobe was not found, '
             'media information will not be added')
    app.root.display_warning(wtext)
    Logger.warning(wtext)
