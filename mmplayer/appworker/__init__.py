'''Module that runs extra process and thread workers
to offload cpu usage from main thread.
Also has a interface class and queues, methods, attributes
for handling the data, functions, callbacks
'''

from utils.compat_queue import Queue, Empty
from kivy.utils import platform
from kivy.logger import Logger
from time import time, sleep
from .worker import Worker
from .async_funcs import *
import multiprocessing
import threading

workers = {}

class WorkerInterface(object):
    '''Interface for Worker processes '''
    task_callbacks = None
    '''Dict with task callback id numbers and callback functions'''

    process = None
    '''Process object'''

    _next_worker_id = 0

    _next_task_id = 0
    '''Task counter, used as task_callbacks dict key for every new task'''


    if platform == 'win':
        use_multiprocess = False
    else:
        use_multiprocess = True

    def __init__(self):
        self.id = WorkerInterface._next_worker_id
        WorkerInterface._next_worker_id += 1
        if self.use_multiprocess:
            self.recv = multiprocessing.Queue()
            self.send = multiprocessing.Queue()
        else:
            self.recv, self.send = Queue(), Queue()
        self.task_callbacks = {}

    def add_task(self, task, callback):
        '''Puts task in worker queue and stores callback for later use'''
        task['task_id'] = self._next_task_id
        self.task_callbacks[self._next_task_id] = callback
        self._next_task_id += 1
        self.send.put(task)

    def update(self):
        '''Gets results from self.recv queue and calls task callbacks'''
        try:
            for i in range(5):
                task = self.recv.get_nowait()
                if task['method'] == 'task_done':
                    self.task_callbacks[task['task_id']](task)
                elif task['method'] == 'Logger_info':
                    Logger.info(task['text'])
        except Empty:
            pass

    def start_process(self):
        '''Starts daemon process with
        self.send and self.recv queues as arguments.
        Stores it in self.process'''
        if not self.process:
            w = Worker()
            if self.use_multiprocess:
                self.process = multiprocessing.Process(
                    target=w.start, args=(self.send, self.recv,))
            else:
                self.process = threading.Thread(
                    target=w.start, args=(self.send, self.recv,))
            self.process.daemon = True
            self.process.start()

    def stop(self):
        '''Tells self.process to stop'''
        self.send.put({'method': 'stop'})
        self.process.join()


def start_workers(count):
    '''Creates WorkerInterface instances and starts Worker processes,
    then schedules _update with Clock interval'''
    from kivy.clock import Clock
    global workers
    for i in range(count):
        w_interface = WorkerInterface()
        w_interface.start_process()
        workers[w_interface.id] = w_interface
    Clock.schedule_interval(_update, 0.1)

def _update(dt):
    '''Calls WorkerInterface update method
    to check task results and call callbacks '''
    global workers
    for k, worker in workers.items():
        worker.update()

def add_task(task, callback):
    '''Calls WorkerInterface instance add_task method.
    It puts tasks into worker queue'''
    global workers
    if workers:
        workers[0].add_task(task, callback)

def stop():
    '''Tells workers to stop'''
    global workers
    for k, worker in workers.items():
        worker.stop()
