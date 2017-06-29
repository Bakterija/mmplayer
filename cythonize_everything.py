'''Was useful for finding some mistakes and testing, but does not
improve performance of app at all, at least not noticably,
.pyx files some time in future should do that'''

from distutils.core import setup
from Cython.Build import cythonize
from mmplayer.utils import get_files
from threading import Thread
from logging import Logger
from queue import Queue
import subprocess
import shutil
import time
import sys
import os

PY_VERSION = '3.5m'
REMOVE_C = True

DIR = 'mmplayer/'
dirname = os.path.dirname(__file__)
if dirname:
    DIR = '%s/%s' % (dirname, Dir)
DIR_DEST = 'mmplayer_cythonized/'

ignore = ['garden', 'main.py', 'loader', 'global_vars', 'focus', 'android',
          'default_providers', '__init__.py'
]

if os.path.exists(DIR_DEST):
    shutil.rmtree(DIR_DEST)
shutil.copytree(DIR, DIR_DEST)

cython_files = get_files(DIR_DEST, filter_ext=('.py', ))
for i, x in enumerate(cython_files):
    cython_files[i] = x[len(DIR_DEST):]

rem_files = get_files(DIR_DEST, filter_ext=('.pyc', ))
for x in rem_files:
    os.remove(x)

os.chdir(DIR_DEST)

rem_indexes = []
for i, x in enumerate(cython_files):
    for x2 in ignore:
        if x2 in x:
            rem_indexes.append(i)

for x in reversed(rem_indexes):
    del cython_files[x]


len_cython_files = len(cython_files)

def worker_loop(id, work_list):
    global REMOVE_C
    len_list = len(work_list)
    try:
        for i, x in enumerate(work_list):
            fname = x[:-3]

            cmd = ['cython', x]
            print('%s [%s/%s] Cythoning: %s' % (id, i, len_list, x))
            # print('%s [%s/%s] %s' % (id, i, len_list, cmd))
            subprocess.check_call(cmd)

            cmd = ['gcc', '-shared', '-pthread', '-fPIC', '-fwrapv',
                   '-O2', '-Wall', '-fno-strict-aliasing',
                   '-I/usr/include/python%s' % (PY_VERSION), '-o',
                   '%s.so' % (fname),  '%s.c' % (fname)]
            # print('%s [%s/%s] %s' % (id, i, len_list, cmd))
            subprocess.check_call(cmd)

            if REMOVE_C:
                os.remove('%s.c' % (fname))
            if x[-11:] != '__init__.py':
                os.remove(x)

        print('Worker: %s completed work' % id)

    except KeyboardInterrupt:
        pass

worker_count = 4
splitlen = int((len_cython_files + 4) / worker_count)
workers = []
for i in range(worker_count):
    wlist = cython_files[splitlen*i:splitlen*(i+1)]
    t = Thread(target=worker_loop, args=(i, wlist,))
    workers.append(t)
    t.daemon = True
    t.start()

try:
    for x in workers:
        x.join()
except KeyboardInterrupt:
    pass
