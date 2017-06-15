from os import chdir
from os.path import dirname
import sys

try:
    chdir(dirname(__file__))
    sys.path.append(dirname(__file__))
except:
    pass


def main_loop():
    import app
    import appworker
    appworker.start_workers(1)
    app.main_loop()
    appworker.stop()


if __name__ == '__main__':
    from multiprocessing import freeze_support
    freeze_support()
    main_loop()
