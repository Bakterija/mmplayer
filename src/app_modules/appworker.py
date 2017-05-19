# from app_modules.media_controller.playlist_loader.base import BasePlaylist
from time import time, sleep
from kivy.logger import Logger
import multiprocessing
import threading
try:
    from Queue import Queue
except:
    from queue import Queue

workers = {}
next_id = 0


class Worker(object):
    id = None
    task_thread = None

    def start(self, recv, send):
        active = True
        self.q_recv = recv
        self.q_send = send
        self.tasks = Queue()
        self.tasks_done = Queue()
        self.task_thread = threading.Thread(target=self.do_tasks)
        self.task_thread.daemon = True
        self.task_thread.start()
        while active:
            if not recv.empty():
                task = recv.get_nowait()
                if task:
                    if task['method'] == 'stop':
                        active = False
                    else:
                        self.tasks.put(task)
            if not self.tasks_done.empty():
                task = self.tasks_done.get_nowait()
                self.q_send.put(task)
            sleep(0.01)

    def do_tasks(self):
        while True:
            if not self.tasks.empty():
                task = self.tasks.get_nowait()
                self.tasks_done.put({
                    'method': 'Logger_info',
                    'text': 'Worker: task started: %s-%s' % (
                        task['task_id'], task['method'])})
                if task['method'] == 'playlist_from_path':
                    plbase = BasePlaylist()
                    files = plbase.get_files(task['path'])
                    index = task['start_index']
                    for i, f in enumerate(files):
                        f['index'] = index + i
                    result = {
                        'method': 'task_done', 'task_id': task['task_id'],
                        'playlist': files}
                    self.tasks_done.put({
                        'method': 'Logger_info',
                        'text': 'Worker: task done: %s-%s' % (
                            task['task_id'], task['method'])})
                    self.tasks_done.put(result)
            sleep(0.01)


class WorkerInterface(object):
    process = None
    next_task_id = 0

    def __init__(self):
        global next_id
        self.id = next_id
        next_id += 1
        self.recv = multiprocessing.Queue()
        self.send = multiprocessing.Queue()
        self.task_callbacks = {}

    def add_task(self, task, callback):
        task['task_id'] = self.next_task_id
        self.task_callbacks[self.next_task_id] = callback
        self.next_task_id += 1
        self.send.put(task)

    def update(self):
        for i in range(50):
            if not self.recv.empty():
                task = self.recv.get_nowait()
                if task['method'] == 'task_done':
                    self.task_callbacks[task['task_id']](task)
                elif task['method'] == 'Logger_info':
                    Logger.info(task['text'])

    def start_process(self):
        if not self.process:
            w = Worker()
            self.process = multiprocessing.Process(
                target=w.start, args=(self.send, self.recv,))
            self.process.daemon = True
            self.process.start()

    def stop(self):
        self.send.put({'method': 'stop'})
        self.process.join()


def start_workers(count):
    from kivy.clock import Clock
    global workers
    for i in range(count):
        w_interface = WorkerInterface()
        w_interface.start_process()
        workers[w_interface.id] = w_interface
    Clock.schedule_interval(__update, 0.1)

def __update(dt):
    global workers
    for k, worker in workers.items():
        worker.update()

def add_task(task, callback):
    global workers
    workers[0].add_task(task, callback)

def stop():
    global workers
    for k, worker in workers.items():
        worker.stop()
