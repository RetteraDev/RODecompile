#Embedded file name: I:/bag/tmp/tw2/res/entities\common\Lib/leakHunter.o
import datetime
import gc
import inspect
import json
import os
import re
import threading
import time
_stopEvent = None
_workingThread = None

def start():
    global _workingThread
    global _stopEvent
    if _stopEvent == None:
        _stopEvent = threading.Event()
        _workingThread = threading.Thread(target=_hunter)
        _workingThread.start()
    else:
        raise Exception, 'LeakHunter already started'


def stop():
    global _stopEvent
    if _stopEvent != None:
        _stopEvent.set()
        _workingThread.join()
        _stopEvent = None
    else:
        raise Exception, 'LeakHunter not started'


def _hunter():
    while not _stopEvent.is_set():
        hunt()
        time.sleep(1)


def hunt():
    oldGCFlag = gc.get_debug()
    gc.set_debug(gc.DEBUG_SAVEALL)
    if gc.collect() > 0:
        dumpFileName = _saveGarbages()
        _freeGargages()
    else:
        dumpFileName = None
    gc.set_debug(oldGCFlag)
    if dumpFileName != None:
        print 'Possible circular references detected and dumped. File: ' + dumpFileName
    else:
        print 'Congratulations, no circular references detected.'


def _saveGarbages():
    dump = {}
    dump['version'] = 1
    objs = []
    for pyObj in gc.garbage:
        obj = {}
        obj['id'] = id(pyObj)
        obj['className'] = _getClassName(pyObj)
        obj['repr'] = repr(pyObj)
        try:
            srcObj = pyObj
            if inspect.isclass(pyObj) or inspect.ismodule(pyObj) or inspect.isfunction(pyObj) or inspect.iscode(pyObj) or inspect.ismethod(pyObj) or inspect.istraceback(pyObj) or inspect.isframe(pyObj):
                srcObj = pyObj
            else:
                srcObj = pyObj.__class__
            obj['sourceFile'] = inspect.getsourcefile(srcObj)
            try:
                _, obj['sourceLine'] = inspect.getsourcelines(srcObj)
            except IOError:
                obj['sourceLine'] = '<unknown>'

        except:
            obj['sourceFile'] = '<built-in>'
            obj['sourceLine'] = '<unknown>'

        referents = []
        for referent in gc.get_referents(pyObj):
            referents.append(id(referent))

        obj['referents'] = referents
        objs.append(obj)

    dump['objs'] = objs
    dumpFileName = datetime.datetime.today().strftime('%Y%m%d_%H%M%S') + '.leakdump'
    dumpFile = os.open(dumpFileName, os.O_CREAT | os.O_WRONLY)
    os.write(dumpFile, json.dumps(dump))
    os.close(dumpFile)
    return dumpFileName


def _freeGargages():
    gc.set_debug(0)
    del gc.garbage[:]
    gc.collect()


def _getClassName(obj):
    try:
        className = obj.__class__.__name__
        try:
            if obj.__module__ != None:
                return obj.__module__ + '.' + className
            return className
        except AttributeError:
            return className

    except AttributeError:
        m = re.match('\\<(\\S+).*\\>', repr(obj))
        if m != None:
            return m.group(1)
        else:
            return repr(obj)


def leak():
    s = 'a0 = {}\n'
    for i in xrange(1, 100):
        s += 'a' + str(i) + " = {\'o\' : a" + str(i - 1) + '}\n'

    s += "a0[\'o\'] = a99\n"
    exec s
