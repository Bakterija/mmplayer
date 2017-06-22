from utils.compat_queue import Queue
from .async_funcs import task_switch
from time import time, sleep
import threading


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

                method = task['method']
                args, kwargs = task['args'], task['kwargs']

                rargs, rkwargs = task_switch[method](args, **kwargs)
                ret = {
                    'method': 'task_done', 'task_id': task['task_id'],
                    'args': rargs, 'kwargs': rkwargs}

                self.tasks_done.put({
                    'method': 'Logger_info',
                    'text': 'Worker: task    done: %s-%s' % (
                        task['task_id'], task['method'])})

                self.tasks_done.put(ret)
            sleep(0.01)
