from kivy.metrics import cm, dp
from kivy.compat import PY2

def intcm(number):
    return int(cm(number))

def intdp(number):
    return int(dp(number))

def get_unicode(string):
    '''Takes any bytes or str objects, then returns a unicode utf-8 string '''
    if PY2:
        try:
            string = string.encode('utf-8')
        except:
            pass
        string = unicode(string, 'utf-8')
    else:
        if isinstance(string, bytes):
            string = string.decode('utf-8')
    return string
