'''Python 2.x and Python 3.x have different queue module name,
this imports the correct one
'''

from kivy.compat import PY2
if PY2:
    from Queue import Queue, Empty
else:
    from queue import Queue, Empty
