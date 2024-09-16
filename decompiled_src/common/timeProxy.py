#Embedded file name: I:/bag/tmp/tw2/res/entities\common/timeProxy.o


def toProxy(still, tWant):
    import sys
    import BigWorld
    timeNow = sys.modules.pop('time', None)
    import time as timeReal
    if timeNow:
        sys.modules['time'] = timeNow
    TIME_STILL = still
    TIME_BASE = tWant
    TIME_DIFF = tWant - timeReal.time()
    BigWorld.timeProxy = 1
    if TIME_STILL:
        BigWorld.timeStill = 1
    else:
        BigWorld.timeStill = 0

    def bwtime():
        if TIME_STILL:
            return TIME_BASE - (timeReal.time() - BigWorld.timeOrigin())
        else:
            return BigWorld.timeOrigin() + TIME_DIFF

    BigWorld.time = bwtime

    def bwgetlastinputtime():
        if TIME_STILL:
            return TIME_BASE - (timeReal.time() - BigWorld.get_last_input_time_origin())
        else:
            return BigWorld.get_last_input_time_origin() + TIME_DIFF

    BigWorld.get_last_input_time = bwgetlastinputtime
    import new
    timePseudo = new.module('TimePseudo', timeReal.__doc__)

    def time():
        if TIME_STILL:
            return TIME_BASE
        return timeReal.time() + TIME_DIFF

    timePseudo.time = time

    def asctime(t = None):
        if t is None:
            return timeReal.asctime(timeReal.localtime(time()))
        return timeReal.asctime(t)

    timePseudo.asctime = asctime

    def ctime(secs = None):
        if secs is None:
            return timeReal.ctime(time())
        return timeReal.ctime(secs)

    timePseudo.ctime = ctime

    def gmtime(secs = None):
        if secs is None:
            return timeReal.gmtime(time())
        return timeReal.gmtime(secs)

    timePseudo.gmtime = gmtime

    def localtime(secs = None):
        if secs is None:
            return timeReal.localtime(time())
        return timeReal.localtime(secs)

    timePseudo.localtime = localtime

    def mktime(t = None):
        if t is None:
            return timeReal.mktime(timeReal.localtime(time()))
        return timeReal.mktime(t)

    timePseudo.mktime = mktime

    def strftime(format, t = None):
        if t is None:
            return timeReal.strftime(format, timeReal.localtime(time()))
        return timeReal.strftime(format, t)

    timePseudo.strftime = strftime
    for k, v in timeReal.__dict__.iteritems():
        if k in ('__file__', '__name__', '__doc__'):
            continue
        if hasattr(timePseudo, k):
            continue
        setattr(timePseudo, k, v)

    for m in sys.modules.itervalues():
        if hasattr(m, 'time') and type(getattr(m, 'time')) == type(sys):
            m.time = timePseudo

    sys.modules['time'] = timePseudo


def toOrigin():
    import sys
    import BigWorld
    sys.modules.pop('time', None)
    import time as timeReal
    for m in sys.modules.itervalues():
        if hasattr(m, 'time') and type(getattr(m, 'time')) == type(sys):
            m.time = timeReal

    sys.modules['time'] = timeReal
    BigWorld.time = BigWorld.timeOrigin
    if BigWorld.component == 'client':
        BigWorld.get_last_input_time = BigWorld.get_last_input_time_origin
    BigWorld.timeProxy = 0
    BigWorld.timeStill = 0
