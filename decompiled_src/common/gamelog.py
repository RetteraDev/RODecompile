#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\common/gamelog.o
import sys, os, BigWorld
DEBUG = 10
INFO = 20
WARNING = 30
ERROR = 40
CRITICAL = 50
if BigWorld.component in ('base', 'cell'):
    import syslog, Netease, gameconfig, logconst
    LOG_LEVEL = gameconfig.scriptLogLevel()
    print '[%s] %s' % ('INFO', 'gamelog init')
    if gameconfig.logType() == logconst.LOG_TYPE_SYSLOG:
        syslog.openlog('%s' % gameconfig.getHostId(), syslog.LOG_NOWAIT, syslog.LOG_LOCAL0)
elif BigWorld.component in ('client',):
    if not getattr(BigWorld, 'isBot', False) and BigWorld.isPublishedVersion():
        LOG_LEVEL = CRITICAL
    else:
        LOG_LEVEL = DEBUG

def _lvlStack():
    """
    try:
        raise ZeroDivisionError
    except ZeroDivisionError:
        f = sys.exc_info()[2].tb_frame.f_back
    """
    f = sys._getframe().f_back
    n = 1
    while f != None and n < 2:
        f = f.f_back
        n = n + 1

    if f and n == 2:
        filename = f.f_code.co_filename
        funcname = f.f_code.co_name
        lineno = f.f_lineno
        path, filename = os.path.split(filename)
        filename, ext = os.path.splitext(filename)
        return '%s.%s:%d' % (filename, funcname, lineno)
    else:
        return 'GLOBAL'


def _enableLogFilter():
    if BigWorld.component in ('base', 'cell') and Netease.logFilter:
        return True
    return False


def _getForceLogInfo():
    f = sys._getframe().f_back
    n = 1
    while f != None and n < 2:
        f = f.f_back
        n = n + 1

    eid, ename = (0, '')
    iterDepth = 10
    while n < iterDepth and f:
        f = f.f_back
        n = n + 1
        if f:
            lvars = f.f_locals
            if lvars.has_key('self'):
                s = lvars['self']
                if hasattr(s, 'id') and s.__class__.__name__ in Netease.entityReloadInfo:
                    eid = s.id
                    ename = s.__class__.__name__
                    break
        else:
            break

    if not Netease.logFilter:
        return 'id: %d, e: %s' % (eid, ename)
    mname = ''
    if Netease.logFilter.get('mname'):
        mname = _shouldFilterByMethodName()
        if not mname:
            return
    tgtename = Netease.logFilter.get('ename', ())
    tgteid = Netease.logFilter.get('eid', ())
    if tgteid and eid not in tgteid:
        return
    elif tgtename and ename not in tgtename:
        return
    elif mname:
        return 'id: %d, e: %s, m: %s' % (eid, ename, mname)
    else:
        return 'id: %d, e: %s' % (eid, ename)


def _shouldFilterByMethodName():
    methodNames = Netease.logFilter['mname']
    f = sys._getframe().f_back
    n = 1
    while f != None and n < 3:
        f = f.f_back
        n = n + 1

    iterDepth = 10
    while n < iterDepth and f:
        f = f.f_back
        n = n + 1
        if not f:
            break
        if f.f_code.co_name in methodNames:
            return f.f_code.co_name

    return ''


def _lvlPrint(title, stack, msg, args, owner = None):
    msg = str(msg) + ' ' + ' '.join([ str(a) for a in args ])
    if owner:
        if stack:
            print '[%s][%s][%s] %s' % (title,
             stack,
             owner,
             msg)
        else:
            print '[%s][%s] %s' % (title, owner, msg)
    elif stack:
        print '[%s][%s] %s' % (title, stack, msg)
    else:
        print '[%s] %s' % (title, msg)


def debug(msg, *args):
    _logWithFilterCheck('DEBUG', DEBUG, msg, args)


def info(msg, *args):
    _logWithFilterCheck('INFO', INFO, msg, args)


def _logWithFilterCheck(levelstr, level, msg, args):
    if BigWorld.component in ('base', 'cell'):
        if LOG_LEVEL > level and not _enableLogFilter():
            return
        forceInfo = _getForceLogInfo()
        if forceInfo:
            _lvlPrint(levelstr, '', msg, args, forceInfo)
    else:
        if LOG_LEVEL > level:
            return
        _lvlPrint(levelstr, '', msg, args)


def warning(msg, *args, **kw):
    if LOG_LEVEL > WARNING:
        return
    st = _lvlStack()
    _lvlPrint('WARNING', st, msg, args)


def error(msg, *args, **kw):
    if LOG_LEVEL > ERROR:
        return
    st = _lvlStack()
    _lvlPrint('ERROR', st, msg, args)


def critical(msg, *args, **kw):
    if LOG_LEVEL > CRITICAL:
        return
    st = _lvlStack()
    _lvlPrint('CRITICAL', st, msg, args)


def isDebugLevel():
    return LOG_LEVEL <= DEBUG


UPLOAD_HOST = 'in-appdump.nie.netease.com'
UPLOAD_URL = '/upload'
