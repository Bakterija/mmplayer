from __future__ import print_function
from time import time

class PTimer(object):
    starttime = time()
    time_log = []

    def add(self, name, ):
        try:
            b = time() - self.starttime - self.time_log[-1][1]
        except:
            b = time() - self.starttime
        a = [
            name,
            time() - self.starttime, # time after init
            b # time after last add()
        ]
        self.time_log.append(a)

    def get(self, rounded=0):
        log = list(self.time_log)
        if rounded:
            for i, x in enumerate(self.time_log):
                log[i][1] = round(x[1], rounded)
                log[i][2] = round(x[2], rounded)
        return log

    def printer(self):
        for x in self.time_log:
            print(x)
