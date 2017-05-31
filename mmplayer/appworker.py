'''Module that runs extra process and thread workers
to offload cpu usage from main thread.
Also has a interface class and queues, methods, attributes
for handling the data, functions, callbacks
'''

from utils.compat_queue import Queue
from kivy.logger import Logger
from time import time, sleep
import multiprocessing
import threading

workers = {}
next_id = 0


class Worker(object):
    '''A worker that interprets json tasks,
    runs them in a separate thread and sends back results.
    Continually looks in recv queue for a stop message
    to be able to stop quickly
    '''

    id = None
    task_thread = None
    '''Thread which runs tasks'''

    q_recv = None
    '''Queue which receives tasks'''

    q_send = None
    '''Queue where responses are put'''

    def start(self, recv, send):
        self.task_thread = threading.Thread(target=self.do_tasks)
        self.task_thread.daemon = True
        self.tasks_done = Queue()
        self.tasks = Queue()
        self.q_recv = recv
        self.q_send = send
        self.task_thread.start()
        active = True
        while active:
            if not recv.empty():
                task = recv.get_nowait()
                # If task is stop, stop process,
                # else tell task thread to work on it
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
        '''Loop method for task thread.
        Gets taks from it's own self.tasks queue
        puts results into self.task_done queue'''
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
    '''Interface for Worker processes '''
    task_callbacks = None
    '''Dict with task callback id numbers and callback functions'''

    process = None
    '''Process object'''

    next_task_id = 0
    '''Task counter, used as task_callbacks dict key for every new task'''

    def __init__(self):
        global next_id
        self.id = next_id
        next_id += 1
        self.recv = multiprocessing.Queue()
        self.send = multiprocessing.Queue()
        self.task_callbacks = {}

    def add_task(self, task, callback):
        '''Puts task in worker queue and stores callback for later use'''
        task['task_id'] = self.next_task_id
        self.task_callbacks[self.next_task_id] = callback
        self.next_task_id += 1
        self.send.put(task)

    def update(self):
        '''Gets results from self.recv queue and calls task callbacks'''
        for i in range(50):
            if not self.recv.empty():
                task = self.recv.get_nowait()
                if task['method'] == 'task_done':
                    self.task_callbacks[task['task_id']](task)
                elif task['method'] == 'Logger_info':
                    Logger.info(task['text'])

    def start_process(self):
        '''Starts daemon process with
        self.send and self.recv queues as arguments.
        Stores it in self.process'''
        if not self.process:
            w = Worker()
            self.process = multiprocessing.Process(
                target=w.start, args=(self.send, self.recv,))
            self.process.daemon = True
            self.process.start()

    def stop(self):
        '''Tells self.process to stop'''
        self.send.put({'method': 'stop'})
        self.process.join()


def start_workers(count):
    '''Creates WorkerInterface instances and starts Worker processes,
    then schedules __update with Clock interval'''
    from kivy.clock import Clock
    global workers
    for i in range(count):
        w_interface = WorkerInterface()
        w_interface.start_process()
        workers[w_interface.id] = w_interface
    Clock.schedule_interval(__update, 0.1)

def __update(dt):
    '''Calls WorkerInterface update method
    to check task results and call callbacks '''
    global workers
    for k, worker in workers.items():
        worker.update()

def add_task(task, callback):
    '''Calls WorkerInterface instance add_task method.
    It puts tasks into worker queue'''
    global workers
    workers[0].add_task(task, callback)

def stop():
    '''Tells workers to stop'''
    global workers
    for k, worker in workers.items():
        worker.stop()
