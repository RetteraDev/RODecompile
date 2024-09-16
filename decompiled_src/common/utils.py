#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\common/utils.o
from gamestrings import gameStrings
import zlib
import copy
import uuid
import encodings
import codecs
import binascii
import cPickle
import copy
import json
from collections import OrderedDict
unicode(gameStrings.TEXT_UTILS_22, 'gbk')
unicode(gameStrings.TEXT_UTILS_22, 'gb18030')
unicode(gameStrings.TEXT_UTILS_22, 'gbk').encode('utf8')
unicode(gameStrings.TEXT_UTILS_22, 'gbk').encode('utf-8')
unicode('1', 'gbk').encode('latin-1')
unicode('abc', 'ascii')
unicode('abc', 'gbk').encode('ascii')
'7061756c'.decode('hex')
'asdf'.decode('utf-8')
import traceback
import time
import sys
import math
import Math
import datetime
import random
import re
import struct
import md5
from cPickle import loads
from random import randint
import hashlib
from socket import inet_aton
from pytz import timezone
import BigWorld
import ResMgr
try:
    import MemoryDB
except:
    pass

import const
import gametypes
import gamelog
from data import datarevision
from crontab import CronTab, defaultTimezone
from gamestrings import serverLanguage
from collections import Iterable
if BigWorld.component in ('base', 'cell'):
    import Netease
    import memprofiler
    import gameconfig
    import gameconfigCommon
    import gameconst
elif BigWorld.component == 'client':
    import gameglobal
    import gameconfigCommon
EQUIP_TYPR_MISMATCH = 4
from miniUtils import *
if BigWorld.component == 'client' and hasattr(BigWorld, 'isPublishedVersion'):

    class roDict(dict):

        def __init__(self):
            raise Exception('Error: roDict is __init__!')

        def __setitem__(self, name, value):
            raise Exception('Error: roDict is read only! name: %s, value: %s' % (name, str(value)))

        def __delitem__(self, name):
            raise Exception('Error: roDict is read only! name: %s' % (name,))

        def pop(self, key):
            raise Exception('Error: roDict is read only! key: %s' % (key,))

        def popitem(self):
            raise Exception('Error: roDict is read only!')

        def clear(self):
            raise Exception('Error: roDict is read only!')

        def update(self, d):
            raise Exception('Error: roDict is read only! d: %s' % (str(d),))


class Faker(object):

    def __getattribute__(self, name):
        if name not in ('__dict__', '__iter__'):
            return object.__getattribute__(self, 'caller')
        raise AttributeError()

    def caller(self, *args, **kw):
        pass


class Swallower(object):

    def __getattribute__(self, name):
        return self

    def __call__(self, *args, **kw):
        pass


if BigWorld.component != 'cell':

    def getGameTimeFromCell(spaceID):
        return None


else:

    def getGameTimeFromCell(spaceID):
        timeNow = int(BigWorld.timeOfDay(spaceID))
        if timeNow:
            timeHour = timeNow / 3600
            timeMin = (timeNow - timeHour * 3600) / 60
            timeSec = timeNow - timeHour * 3600 - timeMin * 60
            return [timeHour % 24, timeMin % 60, timeSec]
        else:
            return None


def getNowMillisecond():
    Millisecond = int(round(getNow(False) * 1000))
    return Millisecond


def _covertToTimestampFromExpireDate(expireData):
    if not expireData:
        return 0
    timeStamp = time.mktime(time.strptime(expireData, '%Y%m%d'))
    return int(timeStamp + const.TIME_INTERVAL_DAY)


def getTimeStampDaysAgo(days):
    t = datetime.date.today() - datetime.timedelta(days)
    return int(t.strftime('%s'))


def getTimeSecondFromStr(ts, tz = None):
    s = ts.split('.')
    if len(s) != 6:
        return 0
    if BigWorld.component in ('cell', 'base'):
        t = time.mktime(time.strptime(ts, '%Y.%m.%d.%H.%M.%S'))
    elif BigWorld.component in 'client':
        for i, k in enumerate(s):
            s[i] = int(k)

        dt = datetime.datetime(s[0], s[1], s[2], s[3], s[4], s[5])
        tDst = 0
        if tz:
            tt = tz.localize(dt).timetuple()
            tNow = datetime.datetime.now(tz).timetuple()
            tDst = tNow[8] - tt[8]
        t = int(time.mktime(dt.timetuple()))
        t += (getTimeZone() - gameglobal.SERVER_TIME_ZONE + tDst) * 3600
    return int(t)


def getCrontabFromStr(ts):
    s = ts.split('.')
    if len(s) != 6:
        return ''
    contabArr = [s[4],
     s[3],
     s[2],
     s[1],
     '*',
     s[0]]
    return ' '.join(contabArr)


def getDateStrFromStr(ts):
    s = ts.split('.')[0:3]
    return '.'.join(s)


def getDayEndSecondFromStr(ts):
    t = getTimeSecondFromStr(ts)
    return getDaySecond(t) + const.TIME_INTERVAL_DAY - 1


def convertDaysFrom1970(timeStamp = None):
    n = timeStamp if timeStamp else getNow()
    offset = time.timezone if time.localtime().tm_isdst == 0 else time.altzone
    return int((n - offset) / 86400)


def localtimeEx(srcSec, isLocalTime = True):
    sec = srcSec
    if isLocalTime and BigWorld.component == 'client':
        sec -= (getTimeZone() - gameglobal.SERVER_TIME_ZONE) * 3600
    if sec < 0:
        sec = max(0, srcSec)
    return getTimeTuple(sec)


def getWeekSecond(sec = None, isLocalTime = True):
    if sec is None:
        sec = getNow()
        isLocalTime = False
    tplSec = localtimeEx(sec, isLocalTime)
    diff = tplSec[3] * 60 * 60 + tplSec[4] * 60 + tplSec[5] + tplSec[6] * 3600 * 24
    t = sec - diff
    if t > 0:
        t = t + 3600 * (tplSec[8] - localtimeEx(t, isLocalTime)[8])
    return sec - diff


def getYearInt(sec = None):
    if sec is None:
        sec = getNow()
    tplSec = time.localtime(sec)
    return tplSec[0]


def getMonthInt(sec = None):
    if sec is None:
        sec = getNow()
    tplSec = time.localtime(sec)
    return tplSec[1]


def getMonthDayInt(sec = None):
    if sec is None:
        sec = getNow()
    tplSec = time.localtime(sec)
    return tplSec[2]


def getHourMinuteInt(sec = None):
    if sec is None:
        sec = getNow()
    tplSec = time.localtime(sec)
    return (tplSec[3], tplSec[4])


def getHourInt(sec = None):
    if sec is None:
        sec = getNow()
    tplSec = time.localtime(sec)
    return tplSec[3]


def getMinuteInt(sec = None):
    if sec is None:
        sec = getNow()
    tplSec = time.localtime(sec)
    return tplSec[4]


def getSecondInt(sec = None):
    if sec is None:
        sec = getNow()
    tplSec = time.localtime(sec)
    return tplSec[5]


def getMinIntegral(sec = None, det = 0):
    if sec is None:
        sec = getNow()
    tplSec = time.localtime(sec)
    integral = 60 + det - tplSec[5]
    return integral


def getWeekInt(sec = None):
    if sec is None:
        sec = getNow()
    tplSec = time.localtime(sec)
    return tplSec[6]


def getDaySecond(sec = None):
    if sec is None:
        sec = getNow()
    else:
        sec = int(sec)
    tplSec = getTimeTuple(sec)
    diff = tplSec[3] * 60 * 60 + tplSec[4] * 60 + tplSec[5]
    wee = sec - diff
    if wee > 0:
        wee = wee + 3600 * (tplSec[8] - getTimeTuple(wee)[8])
    return wee


def getSecondToday(sec = None):
    if sec is None:
        sec = getNow()
    else:
        sec = int(sec)
    tplSec = getTimeTuple(sec)
    return tplSec[3] * 60 * 60 + tplSec[4] * 60 + tplSec[5]


def getMonthSecond(sec = None):
    if sec is None:
        sec = getNow()
    else:
        sec = int(sec)
    tplSec = getTimeTuple(sec)
    diff = (tplSec[2] - 1) * 86400 + tplSec[3] * 60 * 60 + tplSec[4] * 60 + tplSec[5]
    t = sec - diff
    if t > 0:
        t = t + 3600 * (tplSec[8] - getTimeTuple(t)[8])
    return t


def getQuarterSecond(sec = None):
    if sec is None:
        sec = time.time()
    else:
        sec = int(sec)
    tplSec = time.localtime(sec)
    tplMonth = tplSec[1]
    if tplMonth in (1, 2, 3):
        dateC = datetime.datetime(tplSec[0], 1, 1, 0, 0, 0)
        return time.mktime(dateC.timetuple())
    elif tplMonth in (4, 5, 6):
        dateC = datetime.datetime(tplSec[0], 4, 1, 0, 0, 0)
        return time.mktime(dateC.timetuple())
    elif tplMonth in (7, 8, 9):
        dateC = datetime.datetime(tplSec[0], 7, 1, 0, 0, 0)
        return time.mktime(dateC.timetuple())
    elif tplMonth in (10, 11, 12):
        dateC = datetime.datetime(tplSec[0], 10, 1, 0, 0, 0)
        return time.mktime(dateC.timetuple())
    else:
        return


def getQuarterSecondRange(sec = None):
    if sec is None:
        sec = time.time()
    else:
        sec = int(sec)
    tplSec = time.localtime(sec)
    tplMonth = tplSec[1]
    if tplMonth in (1, 2, 3):
        dateC = datetime.datetime(tplSec[0], 1, 1, 0, 0, 0)
        dateEnd = datetime.datetime(tplSec[0], 3, 31, 0, 0, 0)
        return (time.mktime(dateC.timetuple()), time.mktime(dateEnd.timetuple()))
    elif tplMonth in (4, 5, 6):
        dateC = datetime.datetime(tplSec[0], 4, 1, 0, 0, 0)
        dateEnd = datetime.datetime(tplSec[0], 6, 30, 0, 0, 0)
        return (time.mktime(dateC.timetuple()), time.mktime(dateEnd.timetuple()))
    elif tplMonth in (7, 8, 9):
        dateC = datetime.datetime(tplSec[0], 7, 1, 0, 0, 0)
        dateEnd = datetime.datetime(tplSec[0], 9, 30, 0, 0, 0)
        return (time.mktime(dateC.timetuple()), time.mktime(dateEnd.timetuple()))
    elif tplMonth in (10, 11, 12):
        dateC = datetime.datetime(tplSec[0], 10, 1, 0, 0, 0)
        dateEnd = datetime.datetime(tplSec[0], 12, 31, 0, 0, 0)
        return (time.mktime(dateC.timetuple()), time.mktime(dateEnd.timetuple()))
    else:
        return (None, None)


def getTodaySecond(sec = None):
    if sec is None:
        sec = getNow()
    tplSec = time.localtime(sec)
    return tplSec[3] * 3600 + tplSec[4] * 60 + tplSec[5]


def getToTomorrowSecond(sec = None):
    if sec is None:
        sec = getNow()
    tplSec = time.localtime(sec)
    return 86400 - (tplSec[3] * 3600 + tplSec[4] * 60 + tplSec[5]) % 86400


def getToNextWeekSecond(sec = None):
    if sec is None:
        sec = getNow()
    tplSec = time.localtime(sec)
    return 604800 - (tplSec[6] * 86400 + tplSec[3] * 3600 + tplSec[4] * 60 + tplSec[5]) % 604800


def getNextWeekTimeStamp(sec = None):
    if sec is None:
        sec = getNow()
    return sec + getToNextWeekSecond(sec)


def getNextDayTimeStamp(sec = None):
    if sec is None:
        sec = getNow()
    return sec + getToTomorrowSecond(sec)


def getLastDayOfMonth(year, month):
    nextMonth = month + 1 if 0 < month < 12 else 1
    t = time.mktime((year,
     nextMonth,
     1,
     0,
     0,
     0,
     0,
     0,
     0))
    tplSec = time.localtime(t - 86400)
    return tplSec[2]


def isWeekReq(timeStr, sec = None):
    timeStr = timeStr.split('|')
    if len(timeStr) < 3:
        return False
    curWeekday = getWeekInt(sec)
    weekdays = timeStr[2]
    if weekdays == '*':
        return True
    weekdays = [ int(day) for day in weekdays.split(',') ]
    if curWeekday not in weekdays:
        return False
    else:
        return True


def isDateReq(timeStr, sec = None):
    timeStr = timeStr.split('|')
    if len(timeStr) < 3:
        return False
    curMonth = getMonthInt(sec)
    curMonthDay = getMonthDayInt(sec)
    dates = timeStr[1]
    if dates == '*':
        return True
    duringDates = False
    for d in dates.split('^'):
        m = re.match('\\(([0-9]+),([0-9]+|\\*)\\)\\-\\(([0-9]+),([0-9]+|\\*)\\)', d)
        mm = re.match('\\(([0-9]+),([0-9]+|\\*)\\)', d)
        if m:
            beginMonth, beginDay, endMonth, endDay = (m.group(1),
             m.group(2),
             m.group(3),
             m.group(4))
            if curMonth >= int(beginMonth) and (beginDay == '*' or curMonthDay >= int(beginDay)) and curMonth <= int(endMonth) and (endDay == '*' or curMonthDay <= int(endDay)):
                duringDates = True
                break
        elif mm:
            beginMonth, beginDay = mm.group(1), mm.group(2)
            if curMonth == int(beginMonth) and (beginDay == '*' or curMonthDay == int(beginDay)):
                duringDates = True
                break

    if not duringDates:
        return False
    else:
        return True


def isTimeReq(timeStr, sec = None):
    curHour = getHourInt(sec)
    curMinute = getMinuteInt(sec)
    timeStr = timeStr.split('|')
    if len(timeStr) < 3:
        return False
    times = timeStr[0]
    if times == '*':
        return True
    for r in times.split('^'):
        m = re.match('\\(([0-9]+),([0-9]+)\\)\\-\\(([0-9]+),([0-9]+)\\)', r)
        if m == None:
            continue
        beginHour, beginMin, endHour, endMin = (int(m.group(1)),
         int(m.group(2)),
         int(m.group(3)),
         int(m.group(4)))
        if (curHour, curMinute) >= (beginHour, beginMin) and (curHour, curMinute) <= (endHour, endMin):
            return True
        return False


def isSameDay(src, dst = None):
    if dst == None:
        return getDaySecond(src) == getDaySecond()
    else:
        return getDaySecond(src) == getDaySecond(dst)


def isSameWeek(t1, t2 = None):
    if t2 is None:
        t2 = getNow()
    tplSec1 = localtimeEx(t1)
    tplSec2 = localtimeEx(t2)
    return isSameDay(t1 - tplSec1[6] * 24 * 60 * 60, t2 - tplSec2[6] * 24 * 60 * 60)


def isSameHour(t1, t2 = None):
    if t2 is None:
        t2 = getNow()
    tplSec1 = localtimeEx(t1)
    tplSec2 = localtimeEx(t2)
    return tplSec1[3] == tplSec2[3]


def isSameHalfWeek(t1, t2 = None):
    if t2 is None:
        t2 = getNow()
    if not isSameWeek(t1, t2):
        return False
    tplWeek1 = localtimeEx(t1)[6]
    tplWeek2 = localtimeEx(t2)[6]
    if tplWeek2 in (5, 6) and tplWeek1 < 5 or tplWeek2 in (2, 3, 4) and tplWeek1 < 2:
        return False
    return True


def isNthWeek(t1, loopNum, N, t2 = None):
    if t2 is None:
        t2 = getNow()
    t1 = getWeekSecond(t1, isLocalTime=False)
    t2 = getWeekSecond(t2, isLocalTime=False)
    return round((t2 - t1) / 604800.0) % loopNum == (N - 1) % loopNum


def canResetBianShen(src, dst):
    if dst - src >= 86400:
        return True
    else:
        return False


def getResetBianShenTimes(src, dst):
    return (dst - src) // 86400


def getDayMode(hour):
    if hour >= 6 and hour <= 18:
        return const.DAY
    else:
        return const.NIGHT


def isSameEndlessChallengeSeason(lastBuyTime):
    from cdata import endless_challenge_season_list_data as ecsld
    nowSeason = -1
    for season in sorted(ecsld.data.keys(), reverse=True):
        sData = ecsld.data.get(season, {})
        beginTime, endTime = sData.get('beginTime', ''), sData.get('endTime', '')
        if not beginTime or not endTime:
            continue
        if inCrontabRangeWithYear(beginTime, endTime):
            nowSeason = season
            break

    if nowSeason == -1:
        return True
    sData = ecsld.data.get(nowSeason, {})
    beginTime, endTime = sData.get('beginTime', ''), sData.get('endTime', '')
    if inCrontabRangeWithYear(beginTime, endTime, lastBuyTime):
        return True
    return False


def isSameSpriteChallengeSeason(lastBuyTime):
    from cdata import sprite_challenge_season_list_data as scsld
    nowSeason = -1
    for season in sorted(scsld.data.keys(), reverse=True):
        sData = scsld.data.get(season, {})
        beginTime, endTime = sData.get('beginTime', ''), sData.get('endTime', '')
        if not beginTime or not endTime:
            continue
        if inCrontabRangeWithYear(beginTime, endTime):
            nowSeason = season
            break

    if nowSeason == -1:
        return True
    sData = scsld.data.get(nowSeason, {})
    beginTime, endTime = sData.get('beginTime', ''), sData.get('endTime', '')
    if inCrontabRangeWithYear(beginTime, endTime, lastBuyTime):
        return True
    return False


def inCurrentFamousGeneralSeason(lastBuyTime):
    from data import famous_general_config_data as FGCD
    year = getYearInt()
    famousGenralSeasonStartCrontab = FGCD.data['famousGenralSeasonStartCrontab']
    args = famousGenralSeasonStartCrontab.split(' ')
    if len(args) == 5:
        famousGenralSeasonStartCrontab += ' %d' % year
    famousGenralSeasonEndCrontab = FGCD.data['famousGenralSeasonEndCrontab']
    args = famousGenralSeasonEndCrontab.split(' ')
    if len(args) == 5:
        famousGenralSeasonEndCrontab += ' %d' % year
    if inCrontabRangeWithYear(famousGenralSeasonStartCrontab, famousGenralSeasonEndCrontab, lastBuyTime):
        return True
    else:
        return False


def isSameMonth(t1, t2 = None):
    if t2 is None:
        t2 = getNow()
    tplSec1 = localtimeEx(t1)
    tplSec2 = localtimeEx(t2)
    return tplSec1[0] == tplSec2[0] and tplSec1[1] == tplSec2[1]


def getIntervalDay(t1, t2):
    t1 = getDaySecond(t1)
    t2 = getDaySecond(t2)
    return abs(t1 - t2) / const.TIME_INTERVAL_DAY


def getIntervalWeek(t1, t2):
    t1 = getWeekSecond(t1)
    t2 = getWeekSecond(t2)
    return int(abs(t1 - t2) / const.TIME_INTERVAL_WEEK)


def getDayTimeSecondsFromHMS(hsm):
    hour, mint, sec = hsm.split('.')
    hour, mint, sec = int(hour), int(mint), int(sec)
    return getDaySecond() + hour * const.SECONDS_PER_HOUR + mint * const.SECONDS_PER_MIN + sec


if BigWorld.component == 'base' or BigWorld.component == 'cell':
    import Netease
    if not hasattr(Netease, 'roDict'):

        class roDict(dict):

            def __setitem__(self, name, value):
                raise Exception('Error: roDict is read only! name: %s, value: %s' % (name, str(value)))

            def __delitem__(self, name):
                raise Exception('Error: roDict is read only! name: %s' % (name,))

            def pop(self, key):
                raise Exception('Error: roDict is read only! key: %s' % (key,))

            def popitem(self):
                raise Exception('Error: roDict is read only!')

            def clear(self):
                raise Exception('Error: roDict is read only!')

            def update(self, d):
                raise Exception('Error: roDict is read only! d: %s' % (str(d),))


        Netease.roDict = roDict
    else:
        roDict = Netease.roDict
enableBDB = False
isBot = False
filePath = '../planb.txt'
if BigWorld.component == 'client':
    try:
        if BigWorld.isWow64():
            enableBDB = False
        else:
            with open(filePath, 'r') as f:
                line = f.read()
                if line:
                    args = line.split(',')
                    if len(args) >= 6:
                        if random.randint(0, 99) < int(args[5]):
                            enableBDB = True
                    else:
                        enableBDB = False
                else:
                    enableBDB = False
    except:
        enableBDB = False

    isBot = getattr(BigWorld, 'isBot', False)
    if isBot:
        try:
            enableBDB = ResMgr.root['server']['bw.xml']['bots']['enableBDB'].asBool
        except:
            enableBDB = False

    if enableBDB:
        import cacheBDB
        cacheBDB.OpenCache(datarevision.REVISION)

def convertToConst(data, force = False, name = '', ktype = '', vtype = ''):
    if BigWorld.component == 'client':
        if enableBDB and name:
            threshold = 500 if isBot else 0
            return cacheBDB.convert_to_BDB_dict(data, name, ktype, vtype, threshold)
        else:
            return data
    if force:
        pass
    if BigWorld.component == 'database':
        return data
    import gameconfig
    if gameconfig.publicServer():
        import Netease
        if getattr(Netease, 'cntReload', 0) > 0:
            return data
    return convertToRodict(data)


def calcFamousGeneralWeekRatio():
    from data import famous_general_config_data as FGCD
    famousGenralSeasonStartCrontab = FGCD.data.get('famousGenralSeasonStartCrontab')
    if famousGenralSeasonStartCrontab is None:
        return 1.0
    famousGenralSeasonStartTimestamp = getPreCrontabTime(famousGenralSeasonStartCrontab)
    weekCnt = getIntervalWeek(getNow(), famousGenralSeasonStartTimestamp)
    weekCntRatioMap = FGCD.data.get('weekCntRatioMap', {})
    return weekCntRatioMap.get(weekCnt, 1.0)


def needEnableMDB():
    if BigWorld.component not in ('client',):
        return False
    if enableBDB:
        return False
    if not hasattr(BigWorld, 'isPublishedVersion'):
        return False
    if True:
        return True
    enableMDB = False
    filePath = '../planb.txt'
    try:
        with open(filePath, 'r') as f:
            line = f.read()
            if line:
                args = line.split(',')
                if len(args) >= 3:
                    if random.randint(1, 100) < int(args[2]):
                        enableMDB = True
                    return enableMDB
    except:
        enableMDB = False

    return enableMDB


enableMemoryDB = needEnableMDB()
try:
    if not hasattr(MemoryDB, 'initMDB'):
        enableMemoryDB = False
except:
    enableMemoryDB = False

MDB_MODULES = set([])

def needEnableNewMDB():
    doubleOpen = False
    if hasattr(BigWorld, 'hasTianyuRunning'):
        doubleOpen = BigWorld.hasTianyuRunning()
    if doubleOpen:
        return False
    if BigWorld.component not in ('client',):
        return False
    if enableBDB:
        return False
    if not hasattr(BigWorld, 'isPublishedVersion'):
        return False
    try:
        import NewMemoryDB
    except:
        return False

    if True:
        return True
    enableMDB = False
    filePath = '../planb.txt'
    try:
        with open(filePath, 'r') as f:
            line = f.read()
            if line:
                args = line.split(',')
                if len(args) >= 7:
                    if random.randint(1, 100) < int(args[6]):
                        enableMDB = True
                    return enableMDB
    except:
        enableMDB = False

    return enableMDB


newMDB = needEnableNewMDB()
if newMDB:
    enableMemoryDB = False

def convertFromRodict(data):
    if isinstance(data, dict):
        res = {}
        for k, v in data.iteritems():
            res[k] = convertFromRodict(v)

        return res
    if isinstance(data, tuple):
        return tuple([ convertFromRodict(x) for x in data ])
    if isinstance(data, list):
        return [ convertFromRodict(x) for x in data ]
    return data


def convertToRodict(data):
    if type(data) is dict:
        res = {}
        for k, v in data.iteritems():
            if type(v) is dict:
                res1 = {}
                for k1, v1 in v.iteritems():
                    if type(v1) is dict:
                        res2 = {}
                        for k2, v2 in v1.iteritems():
                            if type(v2) is dict:
                                res2[k2] = convertToRodict(v2)
                            else:
                                res2[k2] = v2

                        res1[k1] = roDict(res2)
                    elif type(v1) is list:
                        res2 = []
                        for v2 in v1:
                            if type(v2) is dict:
                                res2.append(convertToRodict(v2))
                            else:
                                res2.append(v2)

                        res1[k1] = res2
                    elif type(v1) is tuple:
                        res2 = []
                        for v2 in v1:
                            if type(v2) is dict:
                                res2.append(convertToRodict(v2))
                            else:
                                res2.append(v2)

                        res1[k1] = tuple(res2)
                    else:
                        res1[k1] = v1

                res[k] = roDict(res1)
            elif type(v) is list:
                res1 = []
                for v1 in v:
                    if type(v1) is dict:
                        res2 = {}
                        for k2, v2 in v1.iteritems():
                            if type(v2) is dict:
                                res2[k2] = convertToRodict(v2)
                            else:
                                res2[k2] = v2

                        res1.append(roDict(res2))
                    elif type(v1) is list:
                        res2 = []
                        for v2 in v1:
                            if type(v2) is dict:
                                res2.append(convertToRodict(v2))
                            else:
                                res2.append(v2)

                        res1.append(res2)
                    elif type(v1) is tuple:
                        res2 = []
                        for v2 in v1:
                            if type(v2) is dict:
                                res2.append(convertToRodict(v2))
                            else:
                                res2.append(v2)

                        res1.append(tuple(res2))
                    else:
                        res1.append(v1)

                res[k] = res1
            elif type(v) is tuple:
                res1 = []
                for v1 in v:
                    if type(v1) is dict:
                        res2 = {}
                        for k2, v2 in v1.iteritems():
                            if type(v2) is dict:
                                res2[k2] = convertToRodict(v2)
                            else:
                                res2[k2] = v2

                        res1.append(roDict(res2))
                    elif type(v1) is list:
                        res2 = []
                        for v2 in v1:
                            if type(v2) is dict:
                                res2.append(convertToRodict(v2))
                            else:
                                res2.append(v2)

                        res1.append(res2)
                    elif type(v1) is tuple:
                        res2 = []
                        for v2 in v1:
                            if type(v2) is dict:
                                res2.append(convertToRodict(v2))
                            else:
                                res2.append(v2)

                        res1.append(tuple(res2))
                    else:
                        res1.append(v1)

                res[k] = tuple(res1)
            else:
                res[k] = v

        return roDict(res)
    return data


def convertToConstDict(data, force = False):
    res = {}
    for k, v in data.iteritems():
        res[convertToConst(k, force)] = convertToConst(v, force)

    return roDict(res)


def convertToConstList(data, force = False):
    res = []
    for x in data:
        res.append(convertToConst(x, force))

    return res


def convertToConstTuple(data, force = False):
    res = []
    for x in data:
        res.append(convertToConst(x, force))

    return tuple(res)


def convertFromConst(data):
    if isinstance(data, dict):
        return convertFromConstDict(data)
    if isinstance(data, list):
        return convertFromConstTuple(data)
    if isinstance(data, tuple):
        return convertFromConstTuple(data)
    return data


def convertFromConstDict(data):
    res = {}
    for k, v in data.iteritems():
        res[k] = convertFromConst(v)

    return res


def convertFromConstTuple(data):
    res = []
    for x in data:
        res.append(convertFromConst(x))

    return res


def resetCls(obj):
    oldCls = obj.__class__
    clsName = oldCls.__name__
    mod = __import__(oldCls.__module__, fromlist=[clsName])
    newCls = getattr(mod, clsName)
    obj.__class__ = newCls


def reportExcept():
    sys.excepthook(*sys.exc_info())


class FakeNone(object):
    __slots__ = []

    def __eq__(self, a):
        return a == None

    def __ne__(self, a):
        return a != None

    def __nonzero__(self):
        return False

    def default_func(self, *args, **kw):
        pass

    def __getattribute__(self, name):
        return object.__getattribute__(self, 'default_func')


MyNone = FakeNone()
logList = []

def recusionLog(num):
    if len(logList) > 50:
        return
    logList.append(num)


def clearLog():
    logList = []


if BigWorld.component in ('base', 'cell'):
    from Netease import uuid_generate_time

    def getUUID():
        return uuid_generate_time()


elif BigWorld.component == 'client':

    def getUUID():
        return ''


def instanceof(ent, entType):
    return ent.__class__.__name__ == entType


def instanceofTypes(ent, entTypes):
    return ent.__class__.__name__ in entTypes


def getEntity(entityClass):
    module = __import__(entityClass)
    clazz = getattr(module, entityClass)
    for k, v in BigWorld.entities.items():
        if type(v).__name__ == clazz.__name__:
            return v


def getEntityList(entityClass):
    module = __import__(entityClass)
    clazz = getattr(module, entityClass)
    res = []
    for k, v in BigWorld.entities.items():
        if type(v).__name__ == clazz.__name__:
            res.append(v)

    return res


def getAvatar():
    return getEntity('Avatar')


def getSprite():
    return getEntity('SummonedSprite')


def lsEntities():
    return BigWorld.entities.values()


def set_gafunc(im_class, rlist):

    def __getattr__(im_self, attrib):
        if attrib[:4] == 'get_':
            atr_name = '_%s__%s' % (im_class.__name__, attrib[4:])
            attr = '__' + attrib[4:]
            if hasattr(im_self, atr_name) and attr in rlist:

                def getfun(obj):
                    return getattr(obj, atr_name)

                getfun.__name__ = attrib
                setattr(im_class, attrib, getfun)
                return getattr(im_self, attrib)
        elif attrib[:4] == 'set_':
            atr_name = '_%s__%s' % (im_class.__name__, attrib[4:])
            attr = '__' + attrib[4:]
            if hasattr(im_self, atr_name) and attr in rlist:

                def setfun(obj, arg):
                    setattr(obj, atr_name, arg)

                setfun.__name__ = attrib
                setattr(im_class, attrib, setfun)
                return getattr(im_self, attrib)
        raise AttributeError, "\'%s\' object has no attribute \'%s\'" % (im_self.__class__.__name__, attrib)

    setattr(im_class, '__getattr__', __getattr__)


def buildAvatarName(pre, post):
    return pre + '-' + post


def isRenameAvatar(name):
    indexR = name.rfind('-')
    if indexR == -1:
        return False
    return True


def genPassword(rang = '23456789qwertyupasdfghjkzxcvbnm', size = 8):
    return ''.join(random.sample(rang, size)).replace(' ', '')


def chooseWithProps(sequence, props, base = const.RANDOM_RATE_BASE_10K):
    if len(sequence) != len(props):
        if len(props):
            gamelog.warning('invalid props, return uniform choice instead', sequence, props)
        return random.choice(sequence)
    rnd = random.random() * base
    for idx, p in enumerate(props):
        rnd -= p
        if rnd <= 0:
            return sequence[idx]


def chooseIdxWithProps(sequence, props, base = const.RANDOM_RATE_BASE_10K):
    if len(sequence) != len(props):
        gamelog.warning('invalid props, return uniform choice inx instead', sequence, props)
        return random.randint(0, len(sequence))
    rnd = random.random() * base
    for idx, p in enumerate(props):
        rnd -= p
        if rnd <= 0:
            return idx


def getObjectSize(obj):
    if obj.__class__.__name__ in ('dict', 'roDict'):
        size = 0
        for k, v in obj.iteritems():
            size += getObjectSize(k) + getObjectSize(v)

        return size + sys.getsizeof(obj)
    elif obj.__class__.__name__ in ('tuple', 'list', 'set', 'frozenset', 'deque'):
        size = 0
        for it in obj:
            size += getObjectSize(it)

        return size + sys.getsizeof(obj)
    else:
        return sys.getsizeof(obj)


def getEntitySize(e, printTopStatistic = False, printNum = 50, type = 1):
    if type:
        propertyList = Netease.propertiesInClass(e.classname())
    else:
        propertyList = BigWorld.propertiesInClass(e.classname())
    count = memprofiler.asizeof(e)
    d = {}
    for property in propertyList:
        if hasattr(e, property):
            count += memprofiler.asizeof(getattr(e, property))
            d[property] = memprofiler.asizeof(getattr(e, property))

    if printTopStatistic:
        gamelog.debug('@zf:profile:  ', e.classname())
        for key, value in sorted(d.iteritems(), key=lambda (k, v): (v, k), reverse=True)[:50]:
            gamelog.debug('@zf:profile:%s: %s' % (key, value))

    gamelog.debug('@zf:profile:total size of entity %s: %s' % (e.classname(), count))
    return count


def memClientProfiler():
    ens = BigWorld.entities.values()
    for en in ens:
        getEntitySize(en, False, 100, 0)


def transformSuitToItems(suitId, school, suitData, equipData = None):
    hasKey = suitData.data.has_key(suitId)
    if hasKey:
        schReq = suitData.data[suitId].get('schReq', ())
        if schReq and school not in schReq:
            hasKey = False
    body = suitData.data[suitId].get('body', 0) if hasKey else 0
    parts = getFashionAspectSlots(body) if body else []
    head = suitData.data[suitId].get('head', 0) if hasKey else 0
    hand = suitData.data[suitId].get('hand', 0) if hasKey else 0
    shoe = suitData.data[suitId].get('shoe', 0) if hasKey else 0
    leg = suitData.data[suitId].get('leg', 0) if hasKey else 0
    cape = suitData.data[suitId].get('cape', 0) if hasKey else 0
    if gametypes.EQU_PART_FASHION_HEAD in parts:
        head = body
    fashion = suitData.data[suitId].get('fashion', 0) if hasKey else 0
    headDye = []
    bodyDye = []
    handDye = []
    shoeDye = []
    legDye = []
    capeDye = []
    if equipData:
        headDye = getEquipDyeList(head)
        bodyDye = getEquipDyeList(body)
        handDye = getEquipDyeList(hand)
        shoeDye = getEquipDyeList(shoe)
        legDye = getEquipDyeList(leg)
        capeDye = getEquipDyeList(cape)
    return (head,
     body,
     hand,
     shoe,
     leg,
     cape,
     fashion,
     headDye,
     bodyDye,
     handDye,
     shoeDye,
     legDye,
     capeDye)


def getEquipId(valueStr):
    try:
        if valueStr == '' or valueStr == None:
            return 0
        return eval(valueStr)[0]
    except:
        raise Exception('eval error in utils getEquipId' + str(valueStr))


def getDyeList(valueStr):
    try:
        if valueStr == '' or valueStr == None:
            return []
        return eval(valueStr)[1]
    except:
        return []


def getEnhLv(valueStr):
    try:
        if valueStr == '' or valueStr == None:
            return 0
        return eval(valueStr)[2]
    except:
        return 0


def setDefaultSuit(suitId, school, aspect, suitData, equipData = None):
    head, body, hand, shoe, leg, cape, fashion, headDye, bodyDye, handDye, shoeDye, legDye, capeDye = transformSuitToItems(suitId, school, suitData, equipData)
    gamelog.debug('b.e.: utils.setDefaultSuit, get part: ', head, body, hand, shoe, leg, fashion)
    aspect.set(gametypes.EQU_PART_FASHION_HEAD, 0)
    if fashion:
        aspect.set(gametypes.EQU_PART_FASHION_HEAD, head, headDye)
        aspect.set(gametypes.EQU_PART_FASHION_BODY, body, bodyDye)
        aspect.set(gametypes.EQU_PART_FASHION_HAND, hand, handDye)
        aspect.set(gametypes.EQU_PART_FASHION_SHOE, shoe, shoeDye)
        aspect.set(gametypes.EQU_PART_FASHION_LEG, leg, legDye)
        aspect.set(gametypes.EQU_PART_FASHION_CAPE, cape, capeDye)
        return True
    else:
        aspect.set(gametypes.EQU_PART_HEAD, head, headDye)
        aspect.set(gametypes.EQU_PART_BODY, body, bodyDye)
        aspect.set(gametypes.EQU_PART_HAND, hand, handDye)
        aspect.set(gametypes.EQU_PART_SHOE, shoe, shoeDye)
        aspect.set(gametypes.EQU_PART_LEG, leg, legDye)
        return False


def buildGroupMessage():
    pass


LANGUAGE = serverLanguage()
if LANGUAGE == 'zh_CN':
    validChar = re.compile('[A-Za-z0-9\\xB0-\\xF7\\x81-\\xA0\\xAA-\\xFE\\xA1-\\xA9]')
    invalidChar = re.compile('\\xA1[\\xA2-\\xB5]|\\xA3[\\xA1-\\xAF\\xBA-\\xC0]|\\xA9[\\x6F-\\x88]|[\\s|]')

    def isValidChName(text):
        try:
            unicodeText = unicode(text, defaultEncoding())
            if len(unicodeText) == 0:
                return False
            for uCh in unicodeText:
                gbkText = uCh.encode(defaultEncoding())
                if validChar.match(gbkText[0]) and not invalidChar.match(gbkText):
                    continue
                else:
                    return False

            return True
        except:
            return False


    def isValidGuildName(name):
        from cdata import game_msg_def_data as GMDD
        if not name or len(name) < const.GUILD_NAME_MIN_LEN or len(name) > const.GUILD_NAME_MAX_LEN:
            return (GMDD.data.GUILD_INVALID_NAME, (const.GUILD_NAME_MIN_LEN / 2, const.GUILD_NAME_MAX_LEN / 2))
        return (-1, ())


elif LANGUAGE == 'ru':
    validCharUpper = re.compile('[A-ZА-Я]')
    enChars = re.compile('[A-Za-z]')
    ruChars = re.compile('[А-я]')

    def isValidChName(text):
        try:
            unicodeText = unicode(text, defaultEncoding())
            if len(unicodeText) < 2 or len(unicodeText) > 14:
                return False
            pt = enChars if enChars.match(unicodeText[0]) else ruChars
            upperCnt = 0
            for uCh in unicodeText:
                if validCharUpper.match(uCh) and pt.match(uCh):
                    upperCnt += 1
                    continue
                if pt.match(uCh):
                    continue
                return False

            return upperCnt <= 2
        except:
            return False


    def isValidGuildName(name):
        from cdata import game_msg_def_data as GMDD
        if not name:
            return (GMDD.data.GUILD_INVALID_NAME, (const.GUILD_NAME_MIN_LEN, const.GUILD_NAME_MAX_LEN))
        name = unicode(name, defaultEncoding())
        if len(name) < const.GUILD_NAME_MIN_LEN or len(name) > const.GUILD_NAME_MAX_LEN:
            return (GMDD.data.GUILD_INVALID_NAME, (const.GUILD_NAME_MIN_LEN, const.GUILD_NAME_MAX_LEN))
        if '__' in name:
            return (GMDD.data.GUILD_INVALID_NAME_UNDERSCORE, ())
        if name.count('_') > 2:
            return (GMDD.data.GUILD_INVALID_NAME_UNDERSCORE, ())
        if name.startswith('_') or name.endswith('_'):
            return (GMDD.data.GUILD_INVALID_NAME_UNDERSCORE, ())
        pt = enChars if enChars.match(name[0]) else ruChars
        for uCh in name:
            if uCh == '_':
                continue
            if pt.match(uCh):
                continue
            return (GMDD.data.GUILD_INVALID_NAME_INVALID_CHAR, ())

        return (-1, ())


elif LANGUAGE == 'en':
    validCharUpper = re.compile('[A-ZÀ-ÖØ-ÝĀĂĄĆĈĊČĎ' + 'ĐĒĔĖĘĚĜĞ' + 'ĠĢĤĦĨĪĬĮ' + 'İĲĴĶĹĻĽĿ' + 'ŁŃŅŇŊŌŎ' + 'ŐŒŔŖŘŚŜŞ' + 'ŠŢŤŦŨŪŬŮ' + 'ŰŲŴŶŸŹŻŽ]')
    validChar = re.compile('[A-Za-zÀ-ÖØ-öø-ÿĀ-ſ]')
    vowels = re.compile('[%s]' % (gameStrings.TEXT_UTILS_1419.decode('utf-8'),))
    consonants = re.compile('[%s]' % ('BCDFGHJKLMNPQRSTVWXZbcdfghjklmnpqrstvwxz?D?T??e?t'.decode('utf-8'),))

    def isValidChName(text):
        try:
            unicodeText = unicode(text, defaultEncoding())
            if len(unicodeText) < 2 or len(unicodeText) > 14:
                return False
            upperCnt = 0
            for uCh in unicodeText:
                if not validChar.match(uCh):
                    return False
                if validCharUpper.match(uCh):
                    upperCnt += 1
                    if upperCnt > 2:
                        return False

            return True
        except:
            return False


    def isValidGuildName(name):
        from cdata import game_msg_def_data as GMDD
        if not name:
            return (GMDD.data.GUILD_INVALID_NAME, (const.GUILD_NAME_MIN_LEN, const.GUILD_NAME_MAX_LEN))
        name = unicode(name, defaultEncoding())
        if len(name) < const.GUILD_NAME_MIN_LEN or len(name) > const.GUILD_NAME_MAX_LEN:
            return (GMDD.data.GUILD_INVALID_NAME, (const.GUILD_NAME_MIN_LEN, const.GUILD_NAME_MAX_LEN))
        upperCnt = 0
        for uCh in name:
            if not validChar.match(uCh):
                return (GMDD.data.GUILD_INVALID_NAME_INVALID_CHAR, ())
            if validCharUpper.match(uCh):
                upperCnt += 1
                if upperCnt > 2:
                    return (GMDD.data.GUILD_INVALID_NAME_UPPER_CNT, ())

        return (-1, ())


def uint64ToStr(intx):
    return struct.pack('Q', intx)


def strToUint64(ustr):
    return struct.unpack('Q', ustr)[0]


def bytesToUuidstring(bytes):
    if bytes is not None and len(bytes) > 0:
        if len(bytes) != 16:
            raise ValueError('bytes is not a 16-char string')
        int = long('%02x' * 16 % tuple(map(ord, bytes)), 16)
        hex = '%032x' % int
        return '%s-%s-%s-%s-%s' % (hex[:8],
         hex[8:12],
         hex[12:16],
         hex[16:20],
         hex[20:])
    return ''


def immutableMeta(name, bases, dct):

    class MetaServer(type):

        def __init__(cls, name, bases, dct):
            type.__init__(cls, name, bases, dct)

        def __setattr__(cls, attr, value):
            raise AttributeError('Cannot assign attributes to this class')

        def __getattr__(cls, name):
            try:
                return cls.__dict__[name]
            except:
                gamelog.error('%s is not defined, return 0 instead.' % name)
                return 0

    class MetaClient(type):

        def __init__(cls, name, bases, dct):
            type.__init__(cls, name, bases, dct)

        def __getattr__(cls, name):
            try:
                return cls.__dict__[name]
            except:
                gamelog.error('%s is not defined, return 0 instead.' % name)
                return 0

    if BigWorld.component == 'client':
        return MetaClient(name, bases, dct)
    else:
        return MetaServer(name, bases, dct)


def isEntitiyInRange2D(entityA, entityB, scope):
    entityA = BigWorld.entities.get(entityA.id)
    entityB = BigWorld.entities.get(entityB.id)
    if entityA is None or entityB is None:
        return False
    elif abs(entityA.position[0] - entityB.position[0]) <= scope and abs(entityA.position[2] - entityB.position[2]) <= scope:
        return True
    else:
        return False


def isOccupied(tgt):
    if hasattr(tgt, 'visibleGbId') and tgt.visibleGbId > 0:
        return True
    if hasattr(tgt, 'visibleGroupNUID') and tgt.visibleGroupNUID > 0:
        return True
    return False


def isOccupiedBySingle(tgt):
    if hasattr(tgt, 'visibleGroupNUID') and tgt.visibleGroupNUID > 0:
        return False
    if hasattr(tgt, 'visibleGbId') and tgt.visibleGbId > 0:
        return True
    return False


def hasOccupiedRelation(src, target):
    if src.IsAvatar is False and target.IsAvatar is False:
        return False
    if src.IsAvatar is True and target.IsAvatar is True:
        return False
    if target.IsAvatar is True:
        src, target = target, src
    visibleGbId = getattr(target, 'visibleGbId', 0)
    if visibleGbId > 0 and visibleGbId == src.gbId:
        return True
    visibleGroupNUID = getattr(target, 'visibleGroupNUID', 0)
    if visibleGroupNUID > 0 and visibleGroupNUID == src.groupNUID:
        return True
    return False


def occupiedSame(src, tgt):
    if not src.IsAvatar and not tgt.IsAvatar:
        if hasattr(src, 'visibleGbId') and hasattr(tgt, 'visibleGbId'):
            if src.visibleGbId == tgt.visibleGbId and src.visibleGbId > 0:
                return True
        if hasattr(src, 'visibleGroupNUID') and hasattr(tgt, 'visibleGroupNUID'):
            if src.visibleGroupNUID == tgt.visibleGroupNUID and src.visibleGroupNUID > 0:
                return True
    return False


def getMarkExceptionWeekCnt():
    now = datetime.datetime.now()
    weekCnt = int(now.strftime('%W'))
    weekDay = getWeekInt()
    if weekDay <= 2:
        return weekCnt - 1
    return weekCnt


def calcExceptionDigest(content):
    curYear = getYearInt()
    curWeek = getMarkExceptionWeekCnt()
    content += str(curYear) + str(curWeek)
    digest = md5.new(content).hexdigest()
    return digest


def normaliseAccountName(name):
    lw = name.lower()
    if lw.endswith('@163.com'):
        return lw[:-8]
    return lw


def unnormaliseAccountName(name):
    n = name.lower()
    if n.find('@') < 0:
        return n + '@163.com'
    return n


def calcTeamAvgCombatPower(members):
    combatPower = 0
    cnt = 0
    for mem in members.itervalues():
        cnt += 1
        combatPower += mem.get('combatPower', 0)

    if cnt > 0:
        return combatPower / cnt
    else:
        return 0


def calcTeamMaxCombatPower(members):
    maxCombatPower = 0
    for mem in members.itervalues():
        combatPower = mem.get('combatPower', 0)
        if combatPower > maxCombatPower:
            maxCombatPower = combatPower
        return maxCombatPower


BUILTIN_OBJS = frozenset(['int',
 'long',
 'str',
 'float',
 'dict',
 'list',
 'bool',
 'tuple',
 'set',
 'frozenset',
 'deque'])

def checkCls(obj):
    oldCls = obj.__class__
    clsName = oldCls.__name__
    if clsName in BUILTIN_OBJS or oldCls.__module__ == '__builtin__':
        return True
    mod = __import__(oldCls.__module__)
    if '.' in oldCls.__module__:
        mod = sys.modules[oldCls.__module__]
    newCls = getattr(mod, clsName, None)
    if newCls is None:
        return True
    return oldCls is newCls


def checkObjCls(name, checked, obj, res, su = None):
    if obj is None:
        return
    if id(obj) in checked:
        return
    checked.add(id(obj))
    if not hasattr(obj, '__class__'):
        return
    cls = obj.__class__
    if cls is None:
        msg = 'checkObjCls: ' + name + ' is old.'
        print msg
        res.append(name)
        return
    if not checkCls(obj):
        msg = 'checkObjCls1: ' + name + ' is old.'
        print msg
        res.append(name)
        return
    if hasattr(obj, '__dict__'):
        for k, v in obj.__dict__.iteritems():
            checkObjCls(name + '.' + str(k), checked, v, res, su)

    if isinstance(obj, dict):
        for k, v in obj.iteritems():
            checkObjCls(name + '[' + repr(k) + ']', checked, v, res, su)

    elif hasattr(obj, '__iter__'):
        for i, v in enumerate(obj):
            checkObjCls(name + '[' + repr(i) + ']', checked, v, res, su)

    elif cls.__name__ == 'PyArrayDataInstance':
        for i, v in enumerate(obj):
            checkObjCls(name + '[' + repr(i) + ']', checked, v, res, su)

    elif cls.__name__ == 'PyFixedDictDataInstance':
        for k, v in obj.items():
            checkObjCls(name + '[' + repr(k) + ']', checked, v, res, su)


def whereAmI():
    lst = traceback.format_list(traceback.extract_stack())
    return '\n'.join([ l.strip() for l in lst[-10:] ])


def isEmpty(s):
    return not s or re.match('^[\\s]+$', s)


def getPlayerDir(skillSrc):
    yaw = BigWorld.dcursor().yaw
    from guis import hotkey as HK
    yaw = skillSrc.yaw
    if HK.HKM[HK.KEY_MOVELEFT].isAnyDown():
        if HK.HKM[HK.KEY_FORWARD].isAnyDown():
            yaw = yaw - math.pi / 4
        elif HK.HKM[HK.KEY_BACKWARD].isAnyDown():
            yaw = yaw - math.pi * 3 / 4
        else:
            yaw = yaw - math.pi / 2
    elif HK.HKM[HK.KEY_MOVERIGHT].isAnyDown():
        if HK.HKM[HK.KEY_FORWARD].isAnyDown():
            yaw = yaw + math.pi / 4
        elif HK.HKM[HK.KEY_BACKWARD].isAnyDown():
            yaw = yaw + math.pi * 3 / 4
        else:
            yaw = yaw + math.pi / 2
    elif HK.HKM[HK.KEY_BACKWARD].isAnyDown():
        yaw = yaw - math.pi
    return yaw


def __getDstPos(md, skillSrc, skillTgt, src, forcePosition, distFix = None):
    gamelog.debug('@__getDstPos', forcePosition, md)
    ignoreTypes = md.get('ignoreTypes')
    if ignoreTypes and skillTgt:
        if getattr(skillTgt, 'IsAvatar', False):
            if gametypes.MOVEMENT_IGNORE_TYPE_AVATAR in ignoreTypes:
                return
        elif getattr(skillTgt, 'IsMonster', False):
            if gametypes.MOVEMENT_IGNORE_TYPE_MONSTER in ignoreTypes:
                return
        elif getattr(skillTgt, 'IsSummonedSprite', False):
            if gametypes.MOVEMENT_IGNORE_TYPE_SPRITE in ignoreTypes:
                return
    tgtUnit = md.get('tgtUnit')
    if tgtUnit == gametypes.MOVEMENT_SKILL_REF_SELF:
        tgt = skillSrc
        if not md.get('forceUsePos'):
            forcePosition = None
    elif tgtUnit == gametypes.MOVEMENT_SKILL_REF_TGT:
        tgt = skillTgt
        if not md.get('forceUsePos'):
            forcePosition = None
    else:
        if not forcePosition:
            return
        tgt = src
    gamelog.debug('111111', forcePosition)
    if not forcePosition:
        angleType = md.get('angleType')
        if md.has_key('distance'):
            dist = md.get('distance')
        elif md.has_key('relativeDist'):
            dist = md.get('relativeDist')
        elif md.has_key('moveTime') and md.has_key('speed'):
            dist = md.get('moveTime') * md.get('speed')
        else:
            dist = 0
        if distFix:
            fixType, fixValue = distFix
            dist = pskillFixValue(dist, fixType, fixValue)
        if src == tgt and src == skillSrc:
            if BigWorld.component in 'client':
                yaw = BigWorld.dcursor().yaw
                if angleType == gametypes.MOVEMENT_SKILL_SRC_WASD:
                    yaw = getPlayerDir(skillSrc)
            else:
                yaw = src.yaw
        elif angleType == gametypes.MOVEMENT_SKILL_ABSOLUTE_ANGLE:
            if tgt == None:
                return
            yaw = tgt.yaw
        elif angleType == gametypes.MOVEMENT_SKILL_SRC_ANGLE:
            yaw = skillSrc.yaw
        elif src == tgt and src == skillTgt:
            if skillSrc == None or tgt == None:
                gamelog.error('flyeffect error, skillSrc or tgt can not be None', md)
                return
            yaw = (skillSrc.position - tgt.position).yaw
        else:
            if tgt == None or src == None:
                gamelog.error('flyeffect error, src or tgt can not be None', md)
                return
            yaw = (tgt.position - src.position).yaw
        theta = getMovementAngle(md)
        if tgt == None:
            return
        dstPos = getRelativePosition(tgt.position, yaw, theta, dist)
        if md.get('angle', 0) == gametypes.MOVEMENT_SKILL_ANGLE_UP:
            dstPos = getRelativePositionWithY(md, tgt.position, dist)
        else:
            getRelativePosition(tgt.position, yaw, theta, dist)
    elif md.has_key('distance'):
        dist = md.get('distance')
        if distFix:
            fixType, fixValue = distFix
            dist = pskillFixValue(dist, fixType, fixValue)
        if tgt == None:
            gamelog.error('flyeffect error, src or tgt can not be None', md)
            return
        yaw = math.atan2(forcePosition[0] - tgt.position[0], forcePosition[2] - tgt.position[2])
        theta = getMovementAngle(md)
        gamelog.debug('2222', forcePosition, tgt.position, tgt.id, yaw, theta)
        if md.get('angle', 0) == gametypes.MOVEMENT_SKILL_ANGLE_UP:
            dstPos = getRelativePositionWithY(md, tgt.position, dist)
        else:
            dstPos = getRelativePosition(tgt.position, yaw, theta, dist)
    else:
        dstPos = forcePosition
    if dstPos:
        dstPos = Math.Vector3(dstPos)
    return dstPos


def pskillFixValue(baseValue, fixType, fixValue):
    if fixType == gametypes.PSKILL_AFFECT_SKILL_CALC_TYPE_ADD:
        return baseValue + fixValue
    if fixType == gametypes.PSKILL_AFFECT_SKILL_CALC_TYPE_REDUCE:
        return baseValue - fixValue
    if fixType == gametypes.PSKILL_AFFECT_SKILL_CALC_TYPE_MULTIPLY:
        return baseValue * fixValue
    if fixType == gametypes.PSKILL_AFFECT_SKILL_CALC_TYPE_DIVIDE:
        return baseValue / fixValue
    if fixType == gametypes.PSKILL_AFFECT_SKILL_CALC_TYPE_SET:
        return fixValue


def getRelativePosition(selfPos, selfYaw, theta, dist):
    x = selfPos[0] + dist * math.sin(selfYaw + theta * math.pi / 180)
    z = selfPos[2] + dist * math.cos(selfYaw + theta * math.pi / 180)
    return (x, selfPos[1], z)


def getRelativePositionWithY(md, position, dist):
    if md.get('angle', None) == gametypes.MOVEMENT_SKILL_ANGLE_UP:
        return (position[0], position[1] + dist, position[2])
    return position


def getMovementAngle(md):
    angle = md.get('angle')
    if angle == gametypes.MOVEMENT_SKILL_ANGLE_FRONT:
        theta = 0
    elif angle == gametypes.MOVEMENT_SKILL_ANGLE_BACK:
        theta = 180
    elif angle == gametypes.MOVEMENT_SKILL_ANGLE_LEFT:
        theta = 270
    elif angle == gametypes.MOVEMENT_SKILL_ANGLE_RIGHT:
        theta = 90
    else:
        theta = 0
    return theta


def isOldGuildFlag(flag):
    if type(flag) != type(''):
        flag = str(flag)
    if flag.find(const.SYMBOL_GUILD_FLAG_SPLIT) == -1:
        return True
    else:
        return False


def isDownloadImage(val):
    if type(val) == str and val.startswith(const.IMAGES_DOWNLOAD_PREFIX):
        return True
    return False


def getGuildFlagKey(flag):
    pass


def isResultCrit(resultSet):
    if resultSet and resultSet.results:
        for pair in resultSet.results:
            if pair.ars == gametypes.DMGPOWER_CRIT:
                return True

    return False


emailVarify = re.compile('\\S*@\\w+([-.]\\w+)*\\.\\w+([-.]\\w+)*')

def isValidEmail(email):
    global emailVarify
    if emailVarify.match(email.strip()):
        return True
    else:
        return False


def normalisePrintAccountName(name):
    n = name.lower()
    if n.find('@') < 0:
        return n + '@163.com'
    return n


def formatRoleNameLink(name):
    return "<font color=\'#ffe566\'><a href = \'event:%s\'><u>%s</u></a></font>" % ('role' + name + '$', name)


def getRangeIndex(val, rangeList):
    for idx, (start, end) in enumerate(rangeList):
        if start <= val <= end:
            return idx

    return -1


def getListIndex(val, l):
    for idx, v in enumerate(l):
        if val < v:
            return idx

    return len(l)


def getListIndexInclude(val, l):
    for idx, v in enumerate(l):
        if val <= v:
            return idx

    return len(l)


def quote(v):
    return gameStrings.TEXT_UTILS_1935 % v


def getFormatDurationList(dura):
    days = int(dura / 86400)
    dura = dura % 86400
    hours = int(dura / 3600)
    dura = dura % 3600
    minutes = int(dura / 60)
    dura = dura % 60
    seconds = int(dura)
    return [days,
     hours,
     minutes,
     seconds]


def formatDurationShortVersion(dura):
    days = int(dura / 86400)
    s = ''
    if days > 0:
        s += gameStrings.TEXT_GUILDRESIDENTPROXY_185 % days
    t = dura % 86400
    hours = int(t / 3600)
    t = t % 3600
    minutes = int(t / 60)
    t = t % 60
    seconds = int(t)
    if hours > 0:
        s += gameStrings.TEXT_CONSIGNPROXY_577 % hours
    if minutes > 0:
        if days <= 0:
            s += gameStrings.TEXT_CONSIGNPROXY_580 % minutes
    if seconds > 0:
        if days <= 0:
            s += gameStrings.TEXT_UTILS_1965 % seconds
    return s


def formatDurationV2(dura, showNums = None):
    if not showNums:
        return formatDuration(dura)
    duraTimeStrList = [gameStrings.TEXT_GUILDRESIDENTPROXY_185,
     gameStrings.TEXT_CONSIGNPROXY_577,
     gameStrings.TEXT_CONSIGNPROXY_580,
     gameStrings.TEXT_UTILS_1965]
    duraTimeList = getFormatDurationList(dura)
    s = ''
    curShowNums = 0
    for idx, curTime in enumerate(duraTimeList):
        if curTime > 0:
            curShowNums += 1
            s += duraTimeStrList[idx] % str(curTime)
            if curShowNums >= showNums:
                return s

    return s


def formatDuration(dura):
    days = int(dura / 86400)
    s = ''
    if days > 0:
        s += gameStrings.TEXT_GUILDRESIDENTPROXY_185 % days
    dura = dura % 86400
    s += formatTime(dura)
    return s


def formatDurationForShort(dura):
    hours = int(dura / 3600)
    t = dura % 3600
    minutes = int(t / 60)
    t = t % 60
    seconds = int(round(t, 1))
    s = ''
    if hours > 0:
        s += '%s:' % hours
    if minutes > 0:
        s += '%s:' % minutes
    if seconds > 0:
        s += '%s' % seconds
    return s


def formatTime(t):
    hours = int(t / 3600)
    t = t % 3600
    minutes = int(t / 60)
    t = t % 60
    seconds = int(t)
    s = ''
    if hours > 0:
        s += gameStrings.TEXT_CONSIGNPROXY_577 % hours
    if minutes > 0:
        s += gameStrings.TEXT_CONSIGNPROXY_580 % minutes
    if seconds > 0:
        s += gameStrings.TEXT_UTILS_1965 % seconds
    return s


def formatDurationLeftDay(sec):
    return int(sec / const.TIME_INTERVAL_DAY)


def formatDurationLeftHour(sec):
    sec = sec % const.TIME_INTERVAL_DAY
    return int(sec / const.TIME_INTERVAL_HOUR)


def formatDurationLeftMin(sec):
    sec = sec % const.TIME_INTERVAL_HOUR
    return int(sec / const.TIME_INTERVAL_MINUTE)


def formatTimeEx(t):
    return datetime.datetime.fromtimestamp(t).strftime('%H:%M:%S')


def formatMonth(t):
    return datetime.datetime.fromtimestamp(t).strftime('%Y-%m')


def formatDate(t, delimiter = '-'):
    return datetime.datetime.fromtimestamp(t).strftime('%%Y%s%%m%s%%d' % (delimiter, delimiter))


def formatDatetime(t):
    return datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M')


def formatDatetimeWithoutHour(t):
    return datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d')


def formatCustomTime(t, formatStr):
    return datetime.datetime.fromtimestamp(t).strftime(formatStr)


def formatTimeAgo(t, fuzzyTime = 0):
    if not t:
        return ''
    from gamestrings import gameStrings
    now = getNow()
    diffTime = now - t
    if diffTime <= fuzzyTime:
        return gameStrings.TIME_AGO_JUST_NOW_TXT
    elif diffTime > const.SECONDS_PER_YEAR:
        return ''.join((str(diffTime / const.SECONDS_PER_YEAR), gameStrings.TIME_AGO_YEAR_TXT, gameStrings.TIME_AGO_TXT))
    elif diffTime > const.SECONDS_PER_MONTH:
        return ''.join((str(diffTime / const.SECONDS_PER_MONTH), gameStrings.TIME_AGO_MONTH_TXT, gameStrings.TIME_AGO_TXT))
    elif diffTime > const.SECONDS_PER_DAY:
        return ''.join((str(diffTime / const.SECONDS_PER_DAY), gameStrings.TIME_AGO_DAY_TXT, gameStrings.TIME_AGO_TXT))
    elif diffTime > const.SECONDS_PER_HOUR:
        return ''.join((str(diffTime / const.SECONDS_PER_HOUR), gameStrings.TIME_AGO_HOUR_TXT, gameStrings.TIME_AGO_TXT))
    elif diffTime > const.SECONDS_PER_MIN:
        return ''.join((str(diffTime / const.SECONDS_PER_MIN), gameStrings.TIME_AGO_MIN_TXT, gameStrings.TIME_AGO_TXT))
    else:
        return ''.join((str(diffTime), gameStrings.TIME_AGO_SEC_TXT, gameStrings.TIME_AGO_TXT))
    return ''


def isGroupPick(picker, itemBox):
    now = getNow()
    if now - itemBox.dropTime > const.DROPPED_ITEM_FREE_PICK_INTERVAL:
        return False
    if itemBox.ownerGroupNUID == 0:
        return False
    if not itemBox.ownerGbIdList:
        return False
    from data import item_data as ID
    if ID.data.get(itemBox.itemId, {}).get('freePickFlag', False):
        return False
    if itemBox.groupAssignWay in (const.GROUP_ASSIGN_HEADER,
     const.GROUP_ASSIGN_DICE,
     const.GROUP_ASSIGN_DICE_JOB,
     const.GROUP_ASSIGN_AUCTION):
        if itemBox.quality >= itemBox.groupAssignQuality:
            return True
        else:
            return False
    return False


def getUseLimitByLv(itemId, playerLv, limitType, limitMax):
    from data import consumable_item_data as CID
    cid = CID.data.get(itemId, {})
    limitDict = cid.get('useLimitByLv', {})
    limityByLv = limitDict.get(limitType)
    if not limityByLv:
        return limitMax
    limitExtraVal = 0
    limitExtraDict = cid.get('useLimitServerProgressExtra', {})
    for type2msgId, lv2AddValue in limitExtraDict.iteritems():
        lType, msgId = type2msgId
        isFinished = False
        if BigWorld.component == 'client':
            p = BigWorld.player()
            isFinished = p.isServerProgressFinished(msgId)
        else:
            import serverProgress
            isFinished = serverProgress.isMileStoneFinished(msgId)
        if lType == limitType and isFinished:
            for lv, addVal in sorted(lv2AddValue, reverse=True):
                if playerLv >= lv:
                    limitExtraVal += int(addVal)
                    break

    for lv, useLimit in sorted(limityByLv, reverse=True):
        if playerLv >= lv:
            return int(useLimit) + limitExtraVal

    return 0


def inRange(rangeTuple, val):
    if rangeTuple[0] <= val < rangeTuple[1]:
        return True
    return False


def inRangeList(rangeTupleList, val):
    for rangeTuple in rangeTupleList:
        if rangeTuple[0] <= val < rangeTuple[1]:
            return True

    return False


def parseCrontabPattern(express, tz = None):
    ct = CronTab(express, tz)
    return [ sorted(list(c.allowed)) for c in ct.matchers[:5] ]


def parseCrontabPatternWithYear(express, tz = None):
    ct = CronTab(express, tz)
    return [ sorted(list(c.allowed)) for c in ct.matchers[:6] ]


def crontabArg2Str(timeArgs):
    s = ''
    for item in timeArgs:
        if len(item) == 0:
            s += ' *'
        else:
            s += ' ' + str(list(item)[0])

    return s[1:]


def crontabArg2Desc(timeArgs):
    val = ''
    if len(timeArgs) == 6 and len(timeArgs[5]) > 0:
        val = val + str(list(timeArgs[5])[0]) + gameStrings.TEXT_GUILDPROXY_497
    if len(timeArgs[4]) > 0:
        val = gameStrings.TEXT_GAMETYPES_10547
        for week in timeArgs[4]:
            val = val + str(week) + ','

    if len(timeArgs[3]) > 0:
        val = val + str(list(timeArgs[3])[0]) + gameStrings.TEXT_GUILDPROXY_497_1
    if len(timeArgs[2]) > 0:
        val = val + str(list(timeArgs[2])[0]) + gameStrings.TEXT_PLAYRECOMMPROXY_848_6
    if len(timeArgs[1]) > 0:
        val = val + str(list(timeArgs[1])[0]) + gameStrings.TEXT_UTILS_2196
    if len(timeArgs[0]) > 0:
        val = val + str(list(timeArgs[0])[0]) + gameStrings.TEXT_FORMULA_1553
    return val


MINUTE = 0
HOUR = 1
DAY = 2
MONTH = 3
WEEKEND = 4
YEAR = 5
TRANS_TAB = {MINUTE: 4,
 HOUR: 3,
 DAY: 2,
 MONTH: 1,
 WEEKEND: 6,
 YEAR: 0}
ALIGN_TAB = {MONTH: 12,
 DAY: 31,
 WEEKEND: 7,
 HOUR: 24,
 MINUTE: 60}
CRON_ANY = '* * * * *'

def checkCrontabs(current, crontabs):
    timeWrap = time.localtime(current)
    if crontabs is None:
        return False
    match = True
    for index, tick in enumerate(crontabs):
        if len(tick) == 0:
            continue
        if timeWrap[TRANS_TAB[index]] not in tick:
            match = False
            break

    return match


def checkXingJiCrontabs(hour, minute, crontabs):
    timeWrap = ['@',
     '@',
     '@',
     hour,
     minute,
     '@',
     '@']
    if crontabs is None:
        return False
    match = True
    for index, tick in enumerate(crontabs):
        if len(tick) == 0:
            continue
        if timeWrap[TRANS_TAB[index]] not in tick:
            match = False
            break

    return match


allMinutes = range(60)
allHours = range(24)
allMonths = range(1, 13)
allWeekdays = range(7)
allTimeRanges = (allMinutes,
 allHours,
 [],
 allMonths,
 allWeekdays)

def nextByTimeTuple(tp, now = None, weekSet = 0, tz = None):
    tpLen = len(tp)
    if tpLen == 5:
        return nextByTimeTupleWithoutYear(tp, now, weekSet, tz)
    else:
        return nextByTimeTupleWithYear(tp, now, weekSet, tz)


def nextByTimeTupleWithoutYear(tp, now = None, weekSet = 0, tz = None):
    if len(tp) != 5:
        return sys.maxint
    now = now or (BigWorld.player().getServerTime() if BigWorld.component == 'client' else time.time())
    tz = tz or defaultTimezone()
    nowDatetime = datetime.datetime.fromtimestamp(now, tz)
    tplSec = nowDatetime.timetuple()
    curYear, curMonth, curDay, curHour, curMin, curSec, curWeekDay = tplSec[0:7]
    minutes, hours, days, months, weekdays = tp
    if days and weekdays:
        return sys.maxint
    minutes = minutes or allMinutes
    hours = hours or allHours
    months = months or allMonths
    weekdays = weekdays or allWeekdays
    dayInterval = 0
    if days and type(days[0]) == tuple and days[0][0] == -1:
        dayInterval = days[0][1]
        days = []
    for month in months:
        if month < curMonth:
            continue
        allDays = range(1, getLastDayOfMonth(curYear, month) + 1)
        mDays = days or allDays
        if dayInterval:
            mDays = [ iDay for iDay in mDays if not (iDay - 1) % dayInterval ]
        for day in mDays:
            if day > allDays[-1]:
                continue
            if month == curMonth and day < curDay:
                continue
            t = tz.localize(datetime.datetime(curYear, month, day))
            if t.weekday() not in weekdays:
                continue
            if isInvalidWeek(weekSet, time.mktime(t.timetuple())):
                continue
            for hour in hours:
                if month == curMonth and day == curDay and hour < curHour:
                    continue
                for minute in minutes:
                    t = tz.localize(datetime.datetime(curYear, month, day, hour, minute))
                    if t > nowDatetime:
                        return (t - nowDatetime).total_seconds()

    for month in months:
        allDays = range(1, getLastDayOfMonth(curYear, month) + 1)
        mDays = days or allDays
        if dayInterval:
            mDays = [ iDay for iDay in mDays if not (iDay - 1) % dayInterval ]
        for day in mDays:
            if day > allDays[-1]:
                continue
            t = tz.localize(datetime.datetime(curYear + 1, month, day))
            if t.weekday() not in weekdays:
                continue
            if isInvalidWeek(weekSet, time.mktime(t.timetuple())):
                continue
            t = tz.localize(datetime.datetime(curYear + 1, month, day, hours[0], minutes[0]))
            return (t - nowDatetime).total_seconds()

    return sys.maxint


def prevByTimeTuple(tp, now = None, weekSet = 0, tz = None):
    if len(tp) == 5:
        return prevByTimeTupleWithoutYear(tp, now, weekSet, tz)
    else:
        return prevByTimeTupleWithYear(tp, now, weekSet, tz)


def prevByTimeTupleWithoutYear(tp, now = None, weekSet = 0, tz = None):
    if len(tp) != 5:
        return 0
    now = now or (BigWorld.player().getServerTime() if BigWorld.component == 'client' else time.time())
    tz = tz or defaultTimezone()
    nowDatetime = datetime.datetime.fromtimestamp(now, tz)
    tplSec = nowDatetime.timetuple()
    curYear, curMonth, curDay, curHour, curMin, curSec, curWeekDay = tplSec[0:7]
    minutes, hours, days, months, weekdays = tp
    if days and weekdays:
        return 0
    minutes = minutes or allMinutes
    hours = hours or allHours
    months = months or allMonths
    weekdays = weekdays or allWeekdays
    minutes = minutes[::-1]
    hours = hours[::-1]
    months = months[::-1]
    weekdays = weekdays[::-1]
    dayInterval = 0
    if days and type(days[0]) == tuple and days[0][0] == -1:
        dayInterval = days[0][1]
        days = []
    for month in months:
        if month > curMonth:
            continue
        allDays = range(1, getLastDayOfMonth(curYear, month) + 1)
        mDays = days or allDays
        if dayInterval:
            mDays = [ iDay for iDay in mDays if not (iDay - 1) % dayInterval ]
        mDays = mDays[::-1]
        for day in mDays:
            if day > allDays[-1]:
                continue
            if month == curMonth and day > curDay:
                continue
            t = tz.localize(datetime.datetime(curYear, month, day))
            if t.weekday() not in weekdays:
                continue
            if isInvalidWeek(weekSet, time.mktime(t.timetuple())):
                continue
            for hour in hours:
                if month == curMonth and day == curDay and hour > curHour:
                    continue
                for minute in minutes:
                    t = tz.localize(datetime.datetime(curYear, month, day, hour, minute))
                    if t <= nowDatetime:
                        return (t - nowDatetime).total_seconds()

    for month in months:
        allDays = range(1, getLastDayOfMonth(curYear, month) + 1)
        mDays = days or allDays
        if dayInterval:
            mDays = [ iDay for iDay in mDays if not (iDay - 1) % dayInterval ]
        mDays = mDays[::-1]
        for day in mDays:
            t = tz.localize(datetime.datetime(curYear - 1, month, day))
            if t.weekday() not in weekdays:
                continue
            if isInvalidWeek(weekSet, time.mktime(t.timetuple())):
                continue
            t = tz.localize(datetime.datetime(curYear - 1, month, day, hours[-1], minutes[-1]))
            return (t - nowDatetime).total_seconds()

    return 0


def prevByTimeTupleWithYear(tp, now = None, weekSet = 0, tz = None):
    if len(tp) != 6:
        return 0
    now = now or (BigWorld.player().getServerTime() if BigWorld.component == 'client' else time.time())
    tz = tz or defaultTimezone()
    nowDatetime = datetime.datetime.fromtimestamp(now, tz)
    tplSec = nowDatetime.timetuple()
    curYear, curMonth, curDay, curHour, curMin, curSec, curWeekDay = tplSec[0:7]
    minutes, hours, days, months, weekdays, years = tp
    if days and weekdays:
        return 0
    minutes = minutes or allMinutes
    hours = hours or allHours
    months = months or allMonths
    weekdays = weekdays or allWeekdays
    years = years or allYears
    minutes = minutes[::-1]
    hours = hours[::-1]
    months = months[::-1]
    weekdays = weekdays[::-1]
    years = years[::-1]
    dayInterval = 0
    if days and type(days[0]) == tuple and days[0][0] == -1:
        dayInterval = days[0][1]
        days = []
    for year in years:
        if year > curYear:
            continue
        for month in months:
            if year == curYear and month > curMonth:
                continue
            allDays = range(1, getLastDayOfMonth(year, month) + 1)
            mDays = days or allDays
            if dayInterval:
                mDays = [ iDay for iDay in mDays if not (iDay - 1) % dayInterval ]
            mDays = mDays[::-1]
            for day in mDays:
                if day > allDays[-1]:
                    continue
                if year == curYear and month == curMonth and day > curDay:
                    continue
                t = tz.localize(datetime.datetime(year, month, day))
                if t.weekday() not in weekdays:
                    continue
                if isInvalidWeek(weekSet, time.mktime(t.timetuple())):
                    continue
                for hour in hours:
                    if year == curYear and month == curMonth and day == curDay and hour > curHour:
                        continue
                    for minute in minutes:
                        t = tz.localize(datetime.datetime(year, month, day, hour, minute))
                        if t <= nowDatetime:
                            return (t - nowDatetime).total_seconds()

    return 0


allYears = range(2016, 2025)

def nextByTimeTupleWithYear(tp, now = None, weekSet = 0, tz = None):
    if len(tp) != 6:
        return sys.maxint
    now = now or (BigWorld.player().getServerTime() if BigWorld.component == 'client' else time.time())
    tz = tz or defaultTimezone()
    nowDatetime = datetime.datetime.fromtimestamp(now, tz)
    tplSec = nowDatetime.timetuple()
    curYear, curMonth, curDay, curHour, curMin, curSec, curWeekDay = tplSec[0:7]
    minutes, hours, days, months, weekdays, years = tp
    if days and weekdays:
        return sys.maxint
    minutes = minutes or allMinutes
    hours = hours or allHours
    months = months or allMonths
    weekdays = weekdays or allWeekdays
    years = years or allYears
    dayInterval = 0
    if days and type(days[0]) == tuple and days[0][0] == -1:
        dayInterval = days[0][1]
        days = []
    if years:
        for year in years:
            if year < curYear:
                continue
            for month in months:
                if year == curYear and month < curMonth:
                    continue
                allDays = range(1, getLastDayOfMonth(year, month) + 1)
                mDays = days or allDays
                if dayInterval:
                    mDays = [ iDay for iDay in mDays if not (iDay - 1) % dayInterval ]
                for day in mDays:
                    if day > allDays[-1]:
                        continue
                    if year == curYear and month == curMonth and day < curDay:
                        continue
                    t = tz.localize(datetime.datetime(year, month, day))
                    if t.weekday() not in weekdays:
                        continue
                    if isInvalidWeek(weekSet, time.mktime(t.timetuple())):
                        continue
                    for hour in hours:
                        if year == curYear and month == curMonth and day == curDay and hour < curHour:
                            continue
                        for minute in minutes:
                            t = tz.localize(datetime.datetime(year, month, day, hour, minute))
                            if t > nowDatetime:
                                return (t - nowDatetime).total_seconds()

        return sys.maxint
    return sys.maxint


def reportWarning(msg):
    if BigWorld.component not in ('base', 'cell'):
        return
    import gameengine
    gameengine.reportSevereCritical(msg)


def inSimpleTimeRange(start, end, now = None, tz = None):
    now = now or getNow()
    if len(start) != 3 or len(end) != 3:
        reportWarning('inSimpleTimeRange warning length not correct, start:%d, end:%d' % (len(start), len(end)))
        return False
    startMin, startHour, startWeek = start
    endMin, endHour, endWeek = end
    tz = tz or defaultTimezone()
    nowDatetime = datetime.datetime.fromtimestamp(now, tz)
    tplSec = nowDatetime.timetuple()
    curYear, curMonth, curDay, curHour, curMin, curSec, curWeekDay = tplSec[0:7]
    if startMin == '*' and endMin == '*' and startHour == '*' and endHour == '*' and startWeek == '*' and endWeek == '*':
        return True
    if (startWeek == '*' or int(startWeek) == curWeekDay) and (startHour == '*' or endHour == '*' or curHour >= int(startHour) and curHour <= int(endHour)):
        if int(startHour) < int(endHour):
            if curHour == int(endHour):
                if endMin == '*' or curMin <= int(endMin):
                    return True
                else:
                    return False
            elif curHour == int(startHour):
                if startMin == '*' or curMin >= int(startMin):
                    return True
            else:
                return True
        elif int(startHour) == int(endHour):
            if endMin == '*' or startMin == '*' or int(startMin) <= curMin <= int(endMin):
                return True
            else:
                return False
        else:
            reportWarning('inSimpleTimeRange warning startHour more than endHour, startHour:%s, endHour:%s' % (startHour, endHour))
            return False
    return False


def inTimeTupleRange(start, end, now = None, weekSet = 0, tz = None):
    if nextByTimeTuple(start, now, weekSet=weekSet, tz=tz) < nextByTimeTuple(end, now, weekSet=weekSet, tz=tz):
        return False
    if nextByTimeTuple(end, now, weekSet=weekSet, tz=tz) == sys.maxint:
        return False
    return True


def inTimeTupleRangeWithYear(start, end, now = None, weekSet = 0, tz = None):
    """
    \xe6\x8e\xa5\xe5\x8f\xa3\xe8\xbf\x98\xe5\x9c\xa8\xe6\xb5\x8b\xe8\xaf\x95\xe4\xb8\xad,\xe6\x9a\x82\xe6\x97\xb6\xe5\x85\x88\xe4\xb8\x8d\xe8\xa6\x81\xe4\xbd\xbf\xe7\x94\xa8
    :param start:
    :param end:
    :param now:
    :param weekSet:
    :param tz:
    :return:
    """
    now = now or getNow()
    nextStartTime = nextByTimeTupleWithYear(start, now, weekSet=weekSet, tz=tz) + now
    nextEndTime = nextByTimeTupleWithYear(end, now, weekSet=weekSet, tz=tz) + now
    if nextStartTime == sys.maxint and nextEndTime != sys.maxint and getNow() <= nextEndTime:
        return True
    if nextStartTime != sys.maxint and nextStartTime > nextEndTime and getNow() <= nextEndTime:
        return True
    return False


def inTimeTuplesRange(starts, ends, sec = None):
    sec = sec or getNow()
    nextStartTime = min([ nextByTimeTuple(s, sec) for s in starts ])
    nextEndTime = min([ nextByTimeTuple(e, sec) for e in ends ])
    if nextStartTime < nextEndTime:
        return False
    return True


def inCrontabRangeEx(start, end, sec = None, startSec = None, endSec = None, weekSet = 0, tz = None):
    sec = sec or getNow()
    startSec = startSec or getNow()
    endSec = endSec or getNow()
    if enableCronStr2List():
        nextStart = nextByTimeTuple(parseCrontabStr2List(start), startSec, weekSet=weekSet, tz=tz)
        nextEnd = nextByTimeTuple(parseCrontabStr2List(end), endSec, weekSet=weekSet, tz=tz)
        if nextEnd == sys.maxint:
            return False
        if nextStart == sys.maxint and nextEnd != sys.maxint:
            return True
        if nextStart < nextEnd:
            return False
        return True
    startCT = CronTab(start, tz)
    endCT = CronTab(end, tz)
    if not endCT.next():
        return False
    if not startCT.next() and endCT.next():
        return True
    if calcCrontabNextEx(startCT, startSec, weekSet) < calcCrontabNextEx(endCT, endSec, weekSet):
        return False
    if isInvalidWeek(weekSet, sec):
        return False
    return True


def inCrontabRange(start, end, sec = None, weekSet = 0, tz = None):
    sec = sec or getNow()
    startTimeStamp = calcFixedTimeStr(start)
    endTimeStamp = calcFixedTimeStr(end)
    if startTimeStamp and endTimeStamp and weekSet == 0:
        return startTimeStamp <= sec <= endTimeStamp
    if enableCronStr2List():
        nextStart = nextByTimeTuple(parseCrontabStr2List(start), sec, weekSet=weekSet, tz=tz)
        nextEnd = nextByTimeTuple(parseCrontabStr2List(end), sec, weekSet=weekSet, tz=tz)
        if nextEnd == sys.maxint:
            return False
        if nextStart == sys.maxint and nextEnd != sys.maxint:
            return True
        if nextStart < nextEnd:
            return False
        return True
    startCT = CronTab(start, tz)
    endCT = CronTab(end, tz)
    if not endCT.next():
        return False
    if not startCT.next() and endCT.next():
        return True
    if calcCrontabNextEx(startCT, sec, weekSet) < calcCrontabNextEx(endCT, sec, weekSet):
        return False
    if calcCrontabNextEx(startCT, sec, weekSet) == calcCrontabNextEx(endCT, sec, weekSet) == sys.maxint:
        return False
    if isInvalidWeek(weekSet, sec):
        return False
    return True


def inCrontabsRange(starts, ends, sec = None):
    sec = sec or getNow()
    if enableCronStr2List():
        return inTimeTuplesRange([ parseCrontabStr2List(startCront) for startCront in starts ], [ parseCrontabStr2List(endCront) for endCront in ends ], sec)
    nextStartTime = min([ CronTab(s).next(sec) for s in starts ])
    nextEndTime = min([ CronTab(s).next(sec) for s in ends ])
    if nextStartTime < nextEndTime:
        return False
    return True


def getFamousGeneralLvDesc(lv):
    from data import famous_general_lv_data as FGLD
    if FGLD.data.has_key(lv):
        return FGLD.data[lv]['name']
    else:
        return ''


def inCrontabRangeWithYear(start, end, sec = None):
    """
    \xe5\x88\xa4\xe6\x96\xadsec\xe6\x97\xb6\xe9\x97\xb4\xe6\x88\xb3\xe6\x98\xaf\xe5\x90\xa6\xe5\x9c\xa8start\xe5\x92\x8cend\xe4\xb8\xad\xef\xbc\x8c\xe6\xb3\xa8\xe6\x84\x8f\xe8\xbf\x99\xe4\xb8\xaa\xe5\x8f\xaa\xe6\x98\xaf\xe9\x92\x88\xe5\xaf\xb9\xe4\xb8\xa4\xe4\xb8\xaa\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9\xe7\x9a\x84\xe5\x88\xa4\xe6\x96\xad\xef\xbc\x8c\xe5\xa6\x82\xe6\x9e\x9cstart\xe6\x88\x96end\xe6\x9c\x89\xe5\xa4\x9a\xe4\xb8\xaa\xe6\x97\xb6\xe9\x97\xb4\xe7\x82\xb9\xef\xbc\x8c\xe5\x88\x99\xe7\xa6\x81\xe6\xad\xa2\xe4\xbd\xbf\xe7\x94\xa8\xe6\x9c\xac\xe5\x87\xbd\xe6\x95\xb0
    :param start: \xe5\xbc\x80\xe5\xa7\x8b\xe6\x97\xb6\xe9\x97\xb4*\xe7\x82\xb9* 
    :param end: \xe7\xbb\x93\xe6\x9d\x9f\xe6\x97\xb6\xe9\x97\xb4*\xe7\x82\xb9*
    :param sec: \xe7\x9b\xae\xe6\xa0\x87\xe6\x97\xb6\xe9\x97\xb4\xe6\x88\xb3
    :return:
    """
    sec = sec or getNow()
    return getDisposableCronTabTimeStamp(start) <= sec and sec <= getDisposableCronTabTimeStamp(end)


def transformCrontabRangeWithYearToWithOutYear(cron):
    fields = cron.split(' ')
    if len(fields) == 5:
        return cron
    if len(fields) == 6:
        return ' '.join(fields[:5])
    return cron


def inDateRange(startCron, endCron, sec = None, weekSet = 0):
    if startCron == CRON_ANY and endCron == CRON_ANY:
        return True
    sec = sec or getNow()
    startCron = '0 0 %s %s %s' % tuple(startCron.split()[2:])
    endCron = '59 23 %s %s %s' % tuple(endCron.split()[2:])
    return inCrontabRange(startCron, endCron, sec, weekSet)


def inTimeRange(startCron, endCron, sec = None, weekSet = 0):
    sec = sec or getNow()
    startCron = '%s %s ' % tuple(startCron.split()[:2]) + '* * *'
    endCron = '%s %s ' % tuple(endCron.split()[:2]) + '* * *'
    return inCrontabRange(startCron, endCron, sec, weekSet)


def isExpireCrontab(cron, sec = None):
    ct = CronTab(cron)
    sec = sec or getNow()
    if not ct.next(sec):
        return True
    return False


def getNextCrontabTime(cron, sec = None, weekSet = 0):
    sec = sec or getNow()
    if enableCronStr2List():
        return sec + nextByTimeTuple(parseCrontabStr2List(cron), sec, weekSet)
    else:
        ct = CronTab(cron)
        return sec + calcCrontabNextEx(ct, sec, weekSet)


def getPreCrontabTime(cron, sec = None, weekSet = 0):
    now = sec or getNow()
    if enableCronStr2List():
        return now + prevByTimeTuple(parseCrontabStr2List(cron), now, weekSet)
    else:
        ct = CronTab(cron)
        pre = calcCrontabPreviousEx(ct, now, weekSet)
        return now - pre


def getTimeDesc(startCron, endCron, tz = None):
    start = parseCrontabPattern(startCron, tz=tz)
    end = parseCrontabPattern(endCron, tz=tz)
    return '%02d:%02d-%02d:%02d' % (start[HOUR][0],
     start[MINUTE][0],
     end[HOUR][0],
     end[MINUTE][0])


def getTimeStampDesc(cron, tz = None):
    start = parseCrontabPattern(cron, tz=tz)
    return '%02d:%02d' % (start[HOUR][0], start[MINUTE][0])


def getRandomValue(v):
    if isinstance(v, tuple):
        if len(v) == 0:
            return None
        if len(v) == 1:
            v = v[0]
        else:
            v = random.uniform(v[0], v[1])
    return v


def isLingXiSkill(skillId):
    return skillId == const.LING_XI_SKILL_ID


def needCalcExtraSkillCD(skillId):
    return skillId in (const.SKILL_ID_1613,)


def isMonsterSkill(skillId):
    if const.MONSTER_SKILL_ID_LOWER <= skillId <= const.MONSTER_SKILL_ID_UPPER:
        return True
    if const.MONSTER_SKILL_ID_LOWER_2 <= skillId <= const.MONSTER_SKILL_ID_UPPER_2:
        if const.SPRITE_SKILL_ID_LOWER <= skillId <= const.SPRITE_SKILL_ID_UPPER:
            return False
        return True
    return False


def isMonsterPSkill(pskillId):
    return const.MONSTER_PSKILL_ID_UPPER >= pskillId >= const.MONSTER_PSKILL_ID_LOWER


def getActivateTitles(owner):
    titles = []
    if owner.activeTitleType == const.ACTIVE_TITLE_TYPE_COMMON:
        for tType in const.COMMON_TTILE_TYPE_SET:
            titles.append(owner.currTitle[tType])

    elif owner.activeTitleType == const.ACTIVE_TITLE_TYPE_WORLD:
        titles.append(owner.currTitle[const.TITLE_TYPE_WORLD])
    titles = [ tId for tId in titles if tId > 0 ]
    return titles


def genDefaultNameByGroupType(groupType):
    if groupType == gametypes.GROUP_TYPE_RAID_GROUP:
        return gameStrings.TEXT_IMPCHAT_41
    if groupType == gametypes.GROUP_TYPE_TEAM_GROUP:
        return gameStrings.TEXT_IMPCHAT_40


def getFbGroupGoal(fbNo):
    from data import fb_data as FD
    isEnableGroupMatch = FD.data[fbNo].get('isEnableGroupMatch', 0)
    if fbNo in const.GUILD_FUBEN_NOS:
        return const.GROUP_GOAL_GUILD_FB
    elif isEnableGroupMatch:
        return const.GROUP_GOAL_FB
    else:
        return const.GROUP_GOAL_DEFAULT


def getAddYaoliPointByJingjie(owner):
    from data import jingjie_data as JD
    addPoint = 0
    for lv, val in JD.data.iteritems():
        if lv <= owner.jingJie:
            addPoint += val.get('addMaxYaoliPoint', 0)

    return addPoint


def jingJie2Name(jingJie):
    from data import jingjie_data as JD
    jName = JD.data.get(jingJie, {}).get('name', '')
    return jName


def getLifeSubType(skillId, cId):
    from data import life_skill_data as LSD
    from data import life_skill_collection_data as LSCD
    from data import life_skill_manufacture_data as LSMD
    skType = LSD.data.get((skillId, 0), {}).get('type', 0)
    subType = 0
    if skType == gametypes.LIFE_SKILL_TYPE_COLLECTION:
        subType = LSCD.data.get(cId, {}).get('subType', 0)
    elif skType == gametypes.LIFE_SKILL_TYPE_MANUFACTURE:
        subType = LSMD.data.get(cId, {}).get('subType', 0)
    return subType


def getLifeRepairData(lv):
    from data import life_equip_repair_data as LERD
    for key, val in LERD.data.iteritems():
        lvMin, lvMax = key
        if lv >= lvMin and lv <= lvMax:
            return val


def getLifeRepairItemAmount(owner, subType, eItem):
    from data import life_skill_subtype_data as LSSD
    toolFixReduceIndex = LSSD.data.get(subType, {}).get('toolFixReduceIndex', -1)
    delta = eItem.initMaxDura - eItem.cdura
    if toolFixReduceIndex == -1 or toolFixReduceIndex > len(owner.lifeEquipFixReduce):
        return 0
    gamelog.info('@hjx getLifeRepairItemAmount:', subType, eItem.id, delta, owner.lifeEquipFixReduce[toolFixReduceIndex - 1])
    return abs(int(math.ceil(delta / 100.0 * (1 - owner.lifeEquipFixReduce[toolFixReduceIndex - 1] / 10000))))


def getSpecialLifeRepairItemAmount(eItem):
    delta = eItem.initMaxDura - eItem.cdura
    amount = int(math.ceil(delta / 100.0))
    return amount


def calcLabourConsume(owner, skillId, rData, props):
    consume = rData.get('consumeLabour')
    tgtLv = rData.get('lv', 1)
    propA = props.get('propA', 0)
    resPropA = props.get('resPropA', 0)
    delta = max(propA - resPropA, 0)
    level = owner.getLiefSkillAttr(skillId, 'level')
    if tgtLv > level:
        delta = 0
    t = (100 - (delta / 1.8 - tgtLv * 0.3) / (int(tgtLv / 50) + 1)) / 100
    t = min(max(round(t, 1), 0.66), 1.1)
    res = consume * t
    res *= owner.getLifeEquipEffect((const.LIFE_EQUIP_EFFECT_LABOUR_CONSUME, skillId), 1)
    return max(0, int(res))


def calcMentalConsume(owner, skillId, rData, props):
    consume = rData.get('consumeMental')
    tgtLv = rData.get('lv', 1)
    propA = props.get('propA', 0)
    resPropA = props.get('resPropA', 0)
    delta = max(propA - resPropA, 0)
    level = owner.getLiefSkillAttr(skillId, 'level')
    if tgtLv > level:
        delta = 0
    t = (100 - (delta / 1.8 - tgtLv * 0.3) / (int(tgtLv / 50) + 1)) / 100
    t = min(max(round(t, 1), 0.66), 1.1)
    res = consume * t
    res *= owner.getLifeEquipEffect((const.LIFE_EQUIP_EFFECT_MENTAL_CONSUME, skillId), 1)
    return max(0, int(res))


def getLifeCanEquipCnt(owner, skillId):
    if BigWorld.component == 'client':
        if not owner.lifeSkill.has_key(skillId):
            return 0
    elif not owner.lifeSkills.has_key(skillId):
        return 0
    from data import life_skill_config_data as LSCD
    toolPartsCount = LSCD.data.get('toolPartsCount', {})
    level = owner.getLiefSkillAttr(skillId, 'level')
    for key, val in toolPartsCount.iteritems():
        lvMin, lvMax = key
        if level >= lvMin and level <= lvMax:
            return val

    return 0


def getLifeEquipCntBySubType(owner, subType):
    cnt = 0
    for key, val in owner.lifeEquipment.iteritems():
        if not val:
            continue
        srcSubType, _ = key
        if srcSubType == subType:
            cnt += 1

    return cnt


def getLifeSkillIdBySubType(subType):
    from data import life_skill_subtype_data as LSSD
    sData = LSSD.data.get(subType)
    if not sData:
        return 0
    return sData['lifeSkillId']


def getLifeFixVal(diffLv):
    from data import life_skill_exp_fix_data as LSEFD
    minDiff = min(LSEFD.data.keys())
    maxDiff = max(LSEFD.data.keys())
    if diffLv < minDiff:
        key = minDiff
    elif diffLv > maxDiff:
        key = maxDiff
    else:
        key = diffLv
    return LSEFD.data[key]


def isSameDirection(p1, p2, p3, p4):
    v1 = Math.Vector3(p1) - Math.Vector3(p2)
    v2 = Math.Vector3(p3) - Math.Vector3(p4)
    theta = math.acos(v1.dot(v2) / (v1.length * v2.length))
    return theta <= math.pi / 2


def isSameTeam(srcIndex, tgtIndex):
    if srcIndex / const.TEAM_MAX_NUMBER == tgtIndex / const.TEAM_MAX_NUMBER:
        return True
    else:
        return False


def isValidIpAddress(address):
    return re.match('^[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}$', address)


def convertAToN(address):
    if not isValidIpAddress(address):
        return None
    l = map(int, address.split('.'))
    return (l[3] << 24) + (l[2] << 16) + (l[1] << 8) + l[0]


def createItemObjFromDict(dict):
    from pickledItem import PickledItem
    if BigWorld.component == 'client':
        return doCreateItemObjFromDict(dict)
    it = PickledItem(dict['id'], dict['cwrap'], dict['uuid'], dict['uutime'], dict['minutia'])
    return it


def createItemObjFromStream(stream):
    from pickledItem import PickledItem
    it = PickledItem(*stream)
    return it


def createSingleWrapItemObjFromDict(itemDict):
    from pickledItem import PickledItem
    it = PickledItem(itemDict['id'], 1, itemDict['uuid'], itemDict['uutime'], itemDict['minutia'])
    return it


def getItemStreamData(it):
    from item import Item
    if not it:
        return ()
    try:
        if it.__dict__.has_key('yangSlots'):
            yangSlotsBak = list(it.yangSlots)
            for idx, sVal in enumerate(yangSlotsBak):
                it.yangSlots[idx] = sVal.getGemData(Item.GEM_TYPE_YANG)

        if it.__dict__.has_key('yinSlots'):
            yinSlotsBak = list(it.yinSlots)
            for idx, sVal in enumerate(yinSlotsBak):
                it.yinSlots[idx] = sVal.getGemData(Item.GEM_TYPE_YIN)

        res = (it.id,
         it.cwrap,
         it.uuid,
         it.uutime,
         it.dumpProp())
        if it.__dict__.has_key('yangSlots'):
            for idx, sVal in enumerate(yangSlotsBak):
                it.yangSlots[idx] = yangSlotsBak[idx]

        if it.__dict__.has_key('yinSlots'):
            for idx, sVal in enumerate(yinSlotsBak):
                it.yinSlots[idx] = yinSlotsBak[idx]

    except Exception as e:
        gamelog.error('getItemSaveData', getattr(it, 'id', 0), getattr(it, 'uuid', ''), e.message)
        return ()

    return res


def getItemSaveData_L(subType, part, it):
    if not it:
        return {}
    itData = getItemSaveData(it)
    if not itData:
        return {}
    res = {'subType': subType,
     'part': part}
    res.update(itData)
    return res


def getItemStreamData_L(subType, part, it):
    if not it:
        return {}
    itData = getItemStreamData(it)
    if not itData:
        return {}
    res = (itData, subType, part)
    return res


def getItemStreamData_X(part, it):
    if not it:
        return ()
    itData = getItemStreamData(it)
    if not itData:
        return ()
    res = (itData, part)
    return res


def getItemSaveData_XY(page, pos, it):
    if not it:
        return {}
    itData = getItemSaveData(it)
    if not itData:
        return {}
    res = {'page': page,
     'pos': pos}
    res.update(itData)
    return res


def getItemStreamData_XY(page, pos, it):
    if not it:
        return ()
    itData = getItemStreamData(it)
    if not itData:
        return ()
    res = (itData, page, pos)
    return res


def buildRenameString(pre, post):
    if type(pre) != type(''):
        pre = str(pre)
    if type(post) != type(''):
        post = str(post)
    return pre + const.SYMBOL_RENAME_SPLIT + post


def isRenameString(name):
    indexR = name.rfind(const.SYMBOL_RENAME_SPLIT)
    if indexR == -1:
        return False
    return True


def isMigrateRename(name):
    idx = name.rfind(const.SYMBOL_MIGRATE_SPLIT)
    if idx == -1:
        return False
    return True


def parseMigrateName(name):
    tl = name.split(const.SYMBOL_RENAME_SPLIT)
    return tl[0] + '-' + tl[1][:len(tl[1]) - len(const.SYMBOL_MIGRATE_SPLIT)]


def preRenameString(name):
    if isRenameString(name):
        indexR = name.rfind(const.SYMBOL_RENAME_SPLIT)
        return name[:indexR]
    return ''


def postRenameString(name):
    if isRenameString(name):
        indexR = name.rfind(const.SYMBOL_RENAME_SPLIT)
        return name[indexR:]
    return ''


def getDisplayName(name):
    prename = preRenameString(name)
    if prename:
        if prename[-1] == const.SYMBOL_DELETE_SPLIT:
            prename = prename[0:-1]
        return prename
    return name


def bytes_to_char(bytes):
    return binascii.hexlify(bytes).upper()


def getRealDye(equip, item, dye, data):
    if data:
        for value in data.values():
            if value[0] == item.id:
                dye = value[1:]

    if len(dye) == 1:
        dye = [dye[0], '255,255,255,255']
    return dye


def hasStateAttrs(stateInfo, attrs = None):
    if attrs == None:
        return False
    for attrId in stateInfo.getStateData('allAttrIds', []):
        if attrId in attrs:
            return True

    return False


def getFbDesc(fbNo):
    from data import fb_data as FD
    if not FD.data.has_key(fbNo):
        return ''
    else:
        return FD.data[fbNo]['name'] + '-' + FD.data[fbNo]['primaryLevelName'] + '-' + FD.data[fbNo]['modeName']


def getFbGroupNo(fbNo):
    fbNo = str(fbNo)
    return int(fbNo[0:3])


def getModifiedStates(oldSt, newSt):
    oldTmp = {sid:(sum([ sVal[gametypes.STATE_INDEX_LAYER] for sVal in slst ]), sVal[gametypes.STATE_INDEX_SRCID], sVal[gametypes.STATE_INDEX_STARTTIME] + sVal[gametypes.STATE_INDEX_LASTTIME] if sVal[gametypes.STATE_INDEX_LASTTIME] != -1 else -1) for sid, slst in oldSt.iteritems()}
    oldStates = {(sid, srcId):(layer, endTime) for sid, (layer, srcId, endTime) in oldTmp.iteritems()}
    newTmp = {sid:(sum([ sVal[gametypes.STATE_INDEX_LAYER] for sVal in slst ]), sVal[gametypes.STATE_INDEX_SRCID], sVal[gametypes.STATE_INDEX_STARTTIME] + sVal[gametypes.STATE_INDEX_LASTTIME] if sVal[gametypes.STATE_INDEX_LASTTIME] != -1 else -1) for sid, slst in newSt.iteritems()}
    newStates = {(sid, srcId):(layer, endTime) for sid, (layer, srcId, endTime) in newTmp.iteritems()}
    return (set([ sid for (sid, srcId), (layer, endTime) in newStates.iteritems() if (sid, srcId) not in oldStates or layer > oldStates[sid, srcId][0] or endTime > oldStates[sid, srcId][1] + 0.3 and endTime > 0 ]), set([ sid for (sid, srcId), (layer, endTime) in oldStates.iteritems() if (sid, srcId) not in newStates or layer < newStates[sid, srcId][0] or endTime > oldStates[sid, srcId][1] + 0.3 and endTime > 0 ]))


def getModifiedStatesByStartTime(oldSt, newSt):
    oldTmp = {sid:(sum([ sVal[gametypes.STATE_INDEX_LAYER] for sVal in slst ]), sVal[gametypes.STATE_INDEX_SRCID], sVal[gametypes.STATE_INDEX_STARTTIME]) for sid, slst in oldSt.iteritems()}
    oldStates = {(sid, srcId):(layer, startTime) for sid, (layer, srcId, startTime) in oldTmp.iteritems()}
    newTmp = {sid:(sum([ sVal[gametypes.STATE_INDEX_LAYER] for sVal in slst ]), sVal[gametypes.STATE_INDEX_SRCID], sVal[gametypes.STATE_INDEX_STARTTIME]) for sid, slst in newSt.iteritems()}
    newStates = {(sid, srcId):(layer, startTime) for sid, (layer, srcId, startTime) in newTmp.iteritems()}
    return (set([ sid for (sid, srcId), (layer, startTime) in newStates.iteritems() if (sid, srcId) not in oldStates or layer > oldStates[sid, srcId][0] or startTime > oldStates[sid, srcId][1] + 1 ]), set([ sid for (sid, srcId), (layer, startTime) in oldStates.iteritems() if (sid, srcId) not in newStates or layer < newStates[sid, srcId][0] or startTime > oldStates[sid, srcId][1] + 1 ]))


def isInteger(s):
    try:
        long(s)
    except:
        return False

    return True


def isEntityId(s):
    if isInteger(s) and long(s) < const.GBID_BASE:
        return True
    return False


def isGbId(s):
    if isInteger(s) and long(s) > const.GBID_BASE:
        return True
    return False


def isRoleName(player):
    return not isInteger(player) and type(player) is str


def getStateSpecialEffectParam(owner, seId, default = 0):
    if hasattr(owner, 'statesSpecialEffectCache'):
        return owner.getStateSpecialEffectParam(seId, default)
    return default


def getAbilityKey(key1, key2):
    if not key2:
        key = str(key1)
    else:
        key = '%d_%d' % (key1, key2)
    return key


def getAbilityTypeAndId(key):
    if not key:
        return (0, 0)
    keys = key.split('_')
    if keys:
        if len(keys) == 2:
            return (int(keys[0]), int(keys[1]))
        if len(keys) == 1:
            return (int(keys[0]), 0)
    return (0, 0)


def getAllAbilityKeysAffectProp():
    res = set()
    from cdata import prop_def_data as PDD
    from gametypes import ABILITY_LS_PROP_ADD, ABILITY_LIFE_EQUIP_DURA
    from data import life_equip_ability_prop_data as LEAPD
    for pid in PDD.data.SOCIAL_PRIMARY_PROPERTIES:
        res.add(getAbilityKey(ABILITY_LS_PROP_ADD, pid))

    propFromAbility = LEAPD.data.get(ABILITY_LIFE_EQUIP_DURA, [])
    for propId, _, val in propFromAbility:
        res.add(getAbilityKey(ABILITY_LIFE_EQUIP_DURA, propId))

    return res


def getAbilityTypeFromKey(key):
    if not key:
        return
    keys = key.split('_')
    if keys and keys[0]:
        return int(keys[0])


def getServerOpenTime():
    serverOpenTime = 0
    if BigWorld.component == 'client':
        import gameglobal
        serverOpenTime = gameglobal.rds.configData.get('serverOpenTime', 0)
    else:
        serverOpenTime = gameconfig.serverOpenTime()
    return serverOpenTime


def getEnableIgnoreTgtGroup():
    enableIgnoreTgtGroup = False
    if BigWorld.component == 'client':
        import gameglobal
        enableIgnoreTgtGroup = gameglobal.rds.configData.get('enableIgnoreTgtGroup', False)
    else:
        enableIgnoreTgtGroup = gameconfig.enableIgnoreTgtGroup()
    return enableIgnoreTgtGroup


def getServerOpenWeeks(tNow = 0):
    tNow = tNow or getNow()
    return getIntervalWeek(tNow, getServerOpenTime())


def getServerOpenDays():
    return (getDaySecond() - getDaySecond(sec=getServerOpenTime())) / const.TIME_INTERVAL_DAY


def getDaysByTime(timeStamp):
    return (getDaySecond() - getDaySecond(sec=timeStamp)) / const.TIME_INTERVAL_DAY


def getLeftSecondByServerOpenDay(dayLimit):
    return getDaySecond(sec=getServerOpenTime()) + const.TIME_INTERVAL_DAY * dayLimit - getNow()


def getServerOpenWeeksInCache():
    if BigWorld.component == 'cell':
        return getattr(Netease, 'serverOpenWeeks', getServerOpenWeeks())
    return getServerOpenWeeks()


def isAbilityOn():
    return True


def enableReliveAutoWithLvLess():
    flag = False
    if BigWorld.component == 'client':
        import gameglobal
        flag = gameglobal.rds.configData.get('enableReliveAutoWithLvLess', False)
    else:
        flag = gameconfig.enableReliveAutoWithLvLess()
    return flag


def enableGroupDetailForcely():
    flag = False
    if BigWorld.component == 'client':
        import gameglobal
        flag = gameglobal.rds.configData.get('enableGroupDetailForcely', False)
    else:
        flag = gameconfig.enableGroupDetailForcely()
    return flag


def isEnableFortBf():
    enableFortBf = False
    if BigWorld.component == 'client':
        import gameglobal
        enableFortBf = gameglobal.rds.configData.get('enableFortBf', False)
    else:
        enableFortBf = gameconfig.enableFortBf()
    return enableFortBf


def isEnableHookBf():
    enableHookBf = False
    if BigWorld.component == 'client':
        import gameglobal
        enableHookBf = gameglobal.rds.configData.get('enableHookBf', False)
    else:
        enableHookBf = gameconfig.enableHookBf()
    return enableHookBf


def isJingJieOn():
    enableJingJie = False
    if BigWorld.component == 'client':
        import gameglobal
        enableJingJie = gameglobal.rds.configData.get('enableJingJie', False)
    else:
        enableJingJie = gameconfig.enableJingJie()
    if not enableJingJie:
        return False
    return True


def isRideWingShareSpeedEnabled():
    enableShareSpeed = False
    if BigWorld.component == 'client':
        enableShareSpeed = gameglobal.rds.configData.get('enableRideWingShareSpeed', False)
    else:
        enableShareSpeed = gameconfig.enableRideWingShareSpeed()
    return bool(enableShareSpeed)


def isRideWingShareEpRegenEnabled():
    if BigWorld.component == 'client':
        return gameglobal.rds.configData.get('enableRideWingShareEpRegen', False)
    else:
        return gameconfig.enableRideWingShareEpRegen()


def isGroupPrepareEnabled():
    enableGroupPrepare = True
    if BigWorld.component == 'client':
        enableGroupPrepare = gameglobal.rds.configData.get('enableGroupPrepare', True)
    else:
        enableGroupPrepare = gameconfig.enableGroupPrepare()
    return bool(enableGroupPrepare)


def isSellNormalToCompositeShopOn():
    enableSellNormalToCompositeShop = False
    if BigWorld.component == 'client':
        import gameglobal
        enableSellNormalToCompositeShop = gameglobal.rds.configData.get('enableSellNormalToCompositeShop', False)
    else:
        enableSellNormalToCompositeShop = gameconfig.enableSellNormalToCompositeShop()
    return bool(enableSellNormalToCompositeShop)


def genArenaWeeklyAward(owner, arenaModeType = 0):
    from cdata import arena_level_data as ALD
    if arenaModeType == const.ARENA_MODE_TYPE_BALANCE:
        from data import balance_arena_score_desc_data as ASDD
        arenaInfo = owner.arenaInfoEx
        curLevel = getArenaLevelForReward(owner and owner.lv or 0)
    else:
        from data import arena_score_desc_data as ASDD
        arenaInfo = owner.arenaInfo
        curLevel = arenaInfo.curLevel
    weeklyAwardName = ALD.data.get(curLevel, {}).get('weeklyAwardName', '')
    awardId = 0
    for key, val in ASDD.data.iteritems():
        minScore, maxScore = key
        if arenaInfo.arenaScore >= minScore and arenaInfo.arenaScore <= maxScore:
            awardId = val.get(weeklyAwardName, 0)
            break

    return awardId


def getDisturbRatioByType(owner, dType):
    if BigWorld.component == 'client':
        if not gameglobal.rds.configData.get('enableDisturb', False):
            return 1.0
        else:
            return owner.disturb.get(dType, 1.0)
    elif BigWorld.component == 'cell':
        if not gameconfig.enableDisturb():
            return 1.0
        else:
            return owner.disturb.getDisturbRatio(owner, dType)
    else:
        return 1.0


def getAwardScoreByArenaType(arenaScore, arenaType, awardType, arenaModeType = 0, arenaMode = 0):
    if arenaModeType == const.ARENA_MODE_TYPE_BALANCE:
        from data import balance_arena_score_desc_data as ASDD
    else:
        from data import arena_score_desc_data as ASDD
    arenaData = {}
    for key, val in ASDD.data.iteritems():
        minScore, maxScore = key
        if arenaScore >= minScore and arenaScore <= maxScore:
            arenaData = val
            break

    if not arenaData:
        return 0
    specialRatio = 1
    if arenaMode in const.CROSS_DOUBLE_ARENA:
        from data import duel_config_data as DCD
        specialRatio = DCD.data.get('dArenaSpecialRatio', 2)
    if arenaType == gametypes.ARENA_TYPE_DUAN_WEI:
        if awardType == gametypes.DUEL_AWARD_TYPE_ZHAN_XUN:
            return arenaData.get('duanWeiAwardZhanXun', 0) * specialRatio
        if awardType == gametypes.DUEL_AWARD_TYPE_JUN_ZI:
            return arenaData.get('duanWeiAwardJunZi', 0) * specialRatio
    elif arenaType == gametypes.ARENA_TYPE_LIAN_XI:
        if awardType == gametypes.DUEL_AWARD_TYPE_ZHAN_XUN:
            return arenaData.get('lianXiAwardZhanXun', 0) * specialRatio
        if awardType == gametypes.DUEL_AWARD_TYPE_JUN_ZI:
            return arenaData.get('lianXiAwardJunZi', 0) * specialRatio
    else:
        return 0


def calcArenaCombatPower(arenaInfo):
    rankScore = arenaInfo.arenaScore * 1.2 * math.pow(1 + 1.0 * (arenaInfo.arenaScore - 1000) / 2000, 1.6)
    winRatio = arenaInfo.calcWinRatio()
    if winRatio >= 0.7:
        winRatio = 0.7
        winRatioScore = 750 + 100 * math.pow(winRatio * 100 - 50, 0.7)
    elif winRatio >= 0.5 and winRatio < 0.7:
        winRatioScore = 750 + 100 * math.pow(winRatio * 100 - 50, 0.7)
    else:
        winRatioScore = 750 - 100 * math.pow(50 - winRatio * 100, 0.7)
    winCnt = arenaInfo.getWinCnt()
    if winCnt < 20:
        winRatioScore = winRatioScore * winCnt / 20
    elif winCnt > 50 and winCnt <= 100:
        winRatioScore *= 1.1
    elif winCnt > 100 and winCnt <= 150:
        winRatioScore *= 1.15
    elif winCnt > 150 and winCnt <= 300:
        winRatioScore *= 1.2
    elif winCnt > 300 and winCnt <= 500:
        winRatioScore *= 1.25
    elif winCnt > 500:
        winRatioScore *= 1.3
    winRankRatio = 0.65 * math.pow(1.0 * arenaInfo.arenaScore / 1000, 1.1)
    if winRankRatio > 1:
        winRatioScore *= winRankRatio
    winScore = min(3500, winCnt * 2)
    return max(0, int(rankScore) + int(winRatioScore) + winScore)


def calcArenaCombatPowerEx(arenaScore, winMatch, duelMatch, loseMatch):
    rankScore = arenaScore * 1.2 * math.pow(1 + 1.0 * (arenaScore - 1000) / 2000, 1.6)
    totalCount = sum(winMatch) + sum(duelMatch) + sum(loseMatch)
    if totalCount > 0:
        winRatio = sum(winMatch) * 1.0 / totalCount
    else:
        winRatio = 0
    if winRatio >= 0.7:
        winRatio = 0.7
        winRatioScore = 750 + 100 * math.pow(winRatio * 100 - 50, 0.7)
    elif winRatio >= 0.5 and winRatio < 0.7:
        winRatioScore = 750 + 100 * math.pow(winRatio * 100 - 50, 0.7)
    else:
        winRatioScore = 750 - 100 * math.pow(50 - winRatio * 100, 0.7)
    winCnt = sum(winMatch)
    if winCnt < 20:
        winRatioScore = winRatioScore * winCnt / 20
    elif winCnt > 50 and winCnt <= 100:
        winRatioScore *= 1.1
    elif winCnt > 100 and winCnt <= 150:
        winRatioScore *= 1.15
    elif winCnt > 150 and winCnt <= 300:
        winRatioScore *= 1.2
    elif winCnt > 300 and winCnt <= 500:
        winRatioScore *= 1.25
    elif winCnt > 500:
        winRatioScore *= 1.3
    winRankRatio = 0.65 * math.pow(1.0 * arenaScore / 1000, 1.1)
    if winRankRatio > 1:
        winRatioScore *= winRankRatio
    winScore = min(3500, winCnt * 2)
    return max(0, int(rankScore) + int(winRatioScore) + winScore)


def calcBuyPriceInMarket(buyCnt, curCnt, cntStep, price, priceStep, priceHighest):
    res = 0
    mod = curCnt % cntStep
    dstPrice = price
    if buyCnt <= mod:
        res = buyCnt * price
    else:
        k = math.ceil(1.0 * (buyCnt - mod) / cntStep)
        if price + k * priceStep <= priceHighest:
            res = price * (mod + 1) + (price + k * priceStep) * (buyCnt - 1 - (k - 1) * cntStep - mod) + (price + priceStep * k / 2) * (k - 1) * cntStep
            dstPrice = int(price + k * priceStep)
        else:
            k = math.ceil(1.0 * (priceHighest - price) / priceStep)
            res = price * (mod + 1) + priceHighest * (buyCnt - 1 - (k - 1) * cntStep - mod) + (price + priceStep * k / 2) * (k - 1) * cntStep
            dstPrice = priceHighest
    return (res, dstPrice)


def calcSellPriceInMarket(sellCnt, curCnt, cntStep, price, priceStep, priceLowest):
    res = 0
    dstPrice = price
    mod = cntStep - curCnt % cntStep
    if sellCnt < mod:
        res = sellCnt * price
    else:
        k = math.ceil(1.0 * (sellCnt - mod + 1) / cntStep)
        if price - k * priceStep >= priceLowest:
            res = price * mod + (price - k * priceStep) * (sellCnt - (k - 1) * cntStep - mod) + (price - priceStep * k / 2) * (k - 1) * cntStep
            dstPrice = int(price - k * priceStep)
        else:
            k = math.ceil(1.0 * (price - priceLowest) / priceStep)
            res = price * mod + priceLowest * (sellCnt - (k - 1) * cntStep - mod) + (price + priceStep * k / 2) * (k - 1) * cntStep
            dstPrice = priceLowest
    return (res, dstPrice)


def getStateIdFromStateNUID(stateNUID):
    return stateNUID >> const.STATE_NUID_SHIFT


def getDamageExtra(src, tgt):
    """
    :param src: \xe4\xbc\xa4\xe5\xae\xb3\xe4\xba\xa7\xe7\x94\x9f\xe7\x9d\x80
    :param tgt: \xe4\xbc\xa4\xe5\xae\xb3\xe6\x89\xbf\xe5\x8f\x97\xe7\x9d\x80
    :return: \xe4\xb8\x80\xe4\xba\x9b\xe9\x99\x84\xe5\x8a\xa0\xe7\x8a\xb6\xe6\x80\x81\xe4\xbf\xa1\xe6\x81\xaf
    """
    extra = {}
    if src.IsAvatar:
        zaijuNoSrc = src._getZaijuNo()
        weakProtectSrc = src._getWeakProtectNum()
        if zaijuNoSrc:
            extra[const.DAMAGE_EXTRA_ZAIJU_SRC] = zaijuNoSrc
        if weakProtectSrc:
            extra[const.DAMAGE_EXTRA_WEAKPROTECT_SRC] = weakProtectSrc
    if tgt.IsAvatar:
        zaijuNoTgt = tgt._getZaijuNo()
        weakProtectTgt = tgt._getWeakProtectNum()
        if zaijuNoTgt:
            extra[const.DAMAGE_EXTRA_ZAIJU_TGT] = zaijuNoTgt
        if weakProtectTgt:
            extra[const.DAMAGE_EXTRA_WEAKPROTECT_TGT] = weakProtectTgt
    return extra


def getCrossGuildTournamentJoinTeam(mode, regionId, groupId):
    if mode == gametypes.CROSS_GUILD_TOURNAMENT_GROUP:
        return const.CROSS_GTN_CANDIDATE_NUM
    if mode == gametypes.CROSS_GUILD_TOURNAMENT_CIRCULAR:
        from data import region_server_config_data as RSCD
        realNum = 0
        for r in RSCD.data.itervalues():
            gtnRegionId = r.get('gtnRegionId', [])
            gtnGuildNum = r.get('gtnGuildNum', [])
            if not gtnRegionId or not gtnGuildNum:
                continue
            gamelog.debug('@ct getCrossGuildTournamentJoinTeam', gtnRegionId, gtnGuildNum)
            if groupId == gametypes.GUILD_TOURNAMENT_GROUP_QL:
                if gtnRegionId[0] == regionId:
                    realNum += gtnGuildNum[0]
            elif groupId == gametypes.GUILD_TOURNAMENT_GROUP_BH:
                if gtnRegionId[1] == regionId:
                    realNum += gtnGuildNum[1]

        if realNum < const.CROSS_GTN_CANDIDATE_NUM:
            gamelog.info('@ct  getCrossGuildTournamentJoinTeam num lack', realNum)
            realNum = const.CROSS_GTN_CANDIDATE_NUM
        return realNum
    return const.CROSS_GTN_CANDIDATE_NUM


def you2SSCName(zaijuNo = 0, weakProtectLv = 0):
    from data import zaiju_data as ZD
    roleName = const.YOU
    if zaijuNo and ZD.data.has_key(zaijuNo):
        roleName = '%s(%s)' % (roleName, ZD.data.get(zaijuNo, {}).get('name', ''))
    if weakProtectLv:
        roleName = gameStrings.TEXT_UTILS_3766 % (roleName, weakProtectLv)
    return roleName


def findChatAnonymity(chatAnonymity):
    from cdata import anonymous_name_manager_data as ANMD
    for cId, val in chatAnonymity.iteritems():
        charName = ANMD.data.get(cId, {}).get('anonymousName', '')
        return '%s%s' % (charName, ''.join(val))


def roleName2SSCName(ent, zaijuNo = 0, weakProtectLv = 0):
    from data import zaiju_data as ZD
    roleName = ent.roleName
    if zaijuNo:
        roleName = '%s(%s)' % (roleName, ZD.data.get(zaijuNo, {}).get('name', ''))
    if weakProtectLv:
        roleName = gameStrings.TEXT_UTILS_3766 % (roleName, weakProtectLv)
    if hasattr(ent, 'IsAvatar') and ent.IsAvatar or hasattr(ent, 'IsSummonedAvatarMonster') and ent.IsSummonedAvatarMonster:
        if BigWorld.component in 'client':
            p = BigWorld.player()
            import gameconfigCommon
            if p.inFubenType(const.FB_TYPE_SHENGSICHANG) or p.inFubenType(const.FB_TYPE_TEAM_SHENGSICHANG):
                return const.SSC_ROLENAME
            elif p.inFubenType(const.FB_TYPE_FIGHT_FOR_LOVE):
                return const.FFL_ROLENAME
            elif p.inClanCourier() and getattr(ent, 'jctSeq', False):
                return ent.getJCTRoleName()
            else:
                roleName = p.anonymNameMgr.checkNeedAnonymousName(ent, roleName)
                return roleName
        elif ent.inFubenType(const.FB_TYPE_SHENGSICHANG) or ent.inFubenType(const.FB_TYPE_TEAM_SHENGSICHANG):
            return const.SSC_ROLENAME
        elif ent.inFubenType(const.FB_TYPE_FIGHT_FOR_LOVE):
            return const.FFL_ROLENAME
        elif gameconfig.enableAssassination() and getattr(ent, 'assassinationKillTargetGbId', 0):
            return const.ASSASSINATION_KILLER_NAME
        elif gameconfig.enablePUBG() and (ent.inFubenType(const.FB_TYPE_BATTLE_FIELD_PUBG) or ent.inFubenType(const.FB_TYPE_BATTLE_FIELD_TIMING_PUBG)):
            gamelog.debug('@hqx_pubg_roleName2SSCName_avatar', ent.id)
            return const.PUBG_ANONYMOUS_NAME
        elif hasattr(ent, 'inClanCourier') and ent.inClanCourier() and getattr(ent, 'isJct', False):
            return const.CLAN_COURIER_JCT_KILLEER_NAME
        elif getattr(ent, 'chatAnonymity', ''):
            return findChatAnonymity(ent.chatAnonymity)
        else:
            return roleName
    else:
        if BigWorld.component == 'cell' and gameconfig.enableClanWarCourier() and hasattr(ent, 'IsSummonedSprite') and ent.IsSummonedSprite and getattr(BigWorld.entities.get(ent.ownerId), 'jctSeq', 0):
            from data import summon_sprite_info_data as SSID
            return SSID.data.get(ent.spriteId, {}).get('name', gameStrings.TEXT_CONST_11070)
        if BigWorld.component == 'cell' and gameconfig.enableAssassination() and hasattr(ent, 'ownerId') and getattr(BigWorld.entities.get(ent.ownerId), 'assassinationKillTargetGbId', 0):
            return const.ASSASSINATION_KILLER_SPRITE_NAME
        return roleName


def getSocSchoolStatus(owner, school, status):
    curSchool = owner.curSocSchool
    if not school:
        if status == 0:
            if not curSchool:
                return True
            return False
        elif curSchool:
            return True
        else:
            return False
    else:
        if status == 2:
            if curSchool != school and owner.socSchools.has_key(school):
                return True
            return False
        if status == 1:
            if curSchool == school:
                return True
            return False
        if owner.socSchools.has_key(school):
            return False
        return True


def getStrFromEffectDict(effectDict):
    strValue = ''
    if not effectDict:
        return strValue
    for key in effectDict.keys():
        strValue = strValue + '_' + str(key) + '&' + '@'.join([ str(i) for i in effectDict.get(key, []) ])

    return strValue


def getEffectDictFromStr(strValue):
    effectDict = {}
    if not strValue:
        return effectDict
    for value in strValue.split('_'):
        if value:
            array = value.split('&')
            effId = int(array[0])
            ids = [ int(i) for i in array[1].split('@') ]
            effectDict[effId] = ids

    return effectDict


SKILL_POINT_LV_DICT = {}

def getCurSkillPoint(lv):
    global SKILL_POINT_LV_DICT
    if SKILL_POINT_LV_DICT.has_key(lv):
        return SKILL_POINT_LV_DICT[lv]
    from data import avatar_lv_data as ALD
    ret = 0
    for key, value in ALD.data.items():
        if lv < key:
            break
        ret += value.get('skillPoint', 0)
        SKILL_POINT_LV_DICT[lv] = ret

    return ret


SKILL_ENHANCE_POINT_LV_DICT = {}

def getCurSkillEnhancePoint(lv):
    global SKILL_ENHANCE_POINT_LV_DICT
    if SKILL_ENHANCE_POINT_LV_DICT.has_key(lv):
        return SKILL_ENHANCE_POINT_LV_DICT[lv]
    from cdata import skill_enhance_cost_data as SECD
    point = 0
    for key, value in SECD.data.items():
        if lv >= value['needLv']:
            point = key

    SKILL_ENHANCE_POINT_LV_DICT[lv] = point
    return point


def checkUpgradeJingJie(owner):
    from data import jingjie_data as JJD
    import jingJieUtils
    if owner.jingJie + 1 not in JJD.data:
        return False
    checkJingJie = JJD.data.get(owner.jingJie + 1, {}).get('checkJingJie', [])
    for checkData in checkJingJie:
        cType, cond = checkData
        checkFunc = getattr(jingJieUtils, jingJieUtils.jingJieCondCheckMap[cType], None)
        if checkFunc == None:
            continue
        isFinish, _ = checkFunc(owner, cond)
        if not isFinish:
            return False

    return True


def getTotalSkillEnhancePoint(owner):
    totalPoint = owner.skillEnhancePoint
    for sVal in owner.skills.itervalues():
        totalPoint += sum([ eVal.enhancePoint for eVal in sVal.enhanceData.itervalues() ])

    return totalPoint


def getSkillEnhanceLv(owner):
    totalPoint = getTotalSkillEnhancePoint(owner)
    enhanceLv = getSkillEnhanceLvByTotalPoint(totalPoint)
    return enhanceLv


def getSkillEnhanceLvByTotalPoint(totalPoint):
    from cdata import skill_enhance_lv_data as SELD
    enhLvList = sorted(SELD.data.keys(), reverse=True)
    if totalPoint == 0:
        return enhLvList[-1]
    for skillEnhLv in enhLvList:
        jData = SELD.data[skillEnhLv]
        minPoint, maxPoint = jData['minEnhancePoint'], jData['maxEnhancePoint']
        if minPoint <= totalPoint <= maxPoint:
            return skillEnhLv

    return enhLvList[0]


def getSkillEnhanceCntByPart(owner, partLv):
    cnt = 0
    for skillId in owner.skills.keys():
        sVal = owner.skills[skillId]
        for part in sVal.enhanceData.keys():
            if part // 10 == partLv and sVal.enhanceData[part].enhancePoint > 0:
                cnt += 1

    return cnt


def isSkillEnhanced(owner, skillId, part):
    if owner.skills.has_key(skillId):
        sVal = owner.skills[skillId]
        if sVal.enhanceData.has_key(part) and sVal.enhanceData[part].enhancePoint > 0:
            return True
        else:
            return False
    else:
        return False


def getRuneFullCnt(owner):
    cnt = 0
    for runeType in const.ALL_RUNE_TYPE:
        cnt += const.RUNE_EQUIP_SLOTS_MAP[owner.runeBoard.runeEquip.runeEquipOrder, runeType]

    return cnt


def getMallItemType(item):
    if item._mallExpireTime <= 0:
        return const.MALL_ITEM_TYPE_PERMANENT
    from data import mall_item_data as MID
    md = MID.data.get(item._mallId)
    if not md:
        return const.MALL_ITEM_TYPE_FINITE_TIME
    mallItemType = md.get('mallItemType', const.MALL_ITEM_TYPE_FINITE_TIME)
    if mallItemType == const.MALL_ITEM_TYPE_ONE and item.cwrap > 1:
        mallItemType = const.MALL_ITEM_TYPE_MULTI
    return mallItemType


def chunkName2MapAreaId(owner):
    from data import chunk_mapping_data as CMD
    if BigWorld.component == 'cell':
        chunkName = owner.ChunkInfoAt(owner.position)
    elif BigWorld.component == 'client':
        chunkName = BigWorld.ChunkInfoAt(owner.position)
    else:
        chunkName = ''
    return CMD.data.get(chunkName, {}).get('mapAreaId', 999)


def calcBFMemScore(fbNo, bfStats, memValStats, flagStats = {}):
    import formula
    from data import sys_config_data as SCD
    from data import battle_field_flag_data as BFFD
    UNIT_QUANTITY_KILL = SCD.data.get('UNIT_QUANTITY_KILL', 5)
    UNIT_QUANTITY_ASSIST = SCD.data.get('UNIT_QUANTITY_ASSIST', 2)
    UNIT_QUANTITY_DEATH = SCD.data.get('UNIT_QUANTITY_DEATH', -3)
    score = 0
    score += memValStats['killNum'] * UNIT_QUANTITY_KILL + memValStats['assistNum'] * UNIT_QUANTITY_ASSIST + memValStats['deathNum'] * UNIT_QUANTITY_DEATH + getBFCureScore(bfStats, memValStats['cure']) + getBFDamageScore(bfStats, memValStats['damage'])
    mode = formula.fbNo2BattleFieldMode(fbNo)
    if mode == const.BATTLE_FIELD_MODE_FLAG:
        flagScore = 0
        for flagId, cnt in flagStats.iteritems():
            UNIT_QUANTITY_FLAG = BFFD.data.get(flagId, {}).get('UNIT_QUANTITY_FLAG', 0)
            flagScore += UNIT_QUANTITY_FLAG * cnt

        score += flagScore
    return score


def isCrossArenaPlayoffsFb(fbNo):
    return fbNo in const.FB_NO_CROSS_APD


def isCrossArenaChallenge(fbNo):
    return fbNo in const.FB_NO_CROSS_ROUND_CHALLENGE


def isDoubleArenaPlayoffFb(fbNo):
    return fbNo in const.FB_NO_CROSS_2V2_ROUND_DOUBLE_ARENA_PLAYOFF


def getCrossArenaPlayoffsFinalRoundNum(lvKey):
    if arenaPlayoffsKey2playoffsType(lvKey) == gametypes.ARENA_PLAYOFFS_TYPE_5V5:
        return int(math.log(const.CROSS_ARENA_PLAYOFFS_GROUP_NUM * 2, 2))
    else:
        return int(math.log(const.CROSS_ARENA_PLAYOFFS_GROUP_NUM * 2, 2))


def getFightObserverFlySpeed(owner):
    maxVelocity = 20
    import formula
    from data import sys_config_data as SCD
    fbNo = formula.getFubenNo(owner.spaceNo)
    if inLiveOfArenaPlayoffs(owner) and isCrossArenaPlayoffsFb(fbNo):
        maxVelocity = SCD.data.get('arenaPlayoffsObserverFlySpeed', maxVelocity)
    else:
        maxVelocity = SCD.data.get('observerFlySpeed', gametypes.FLY_OBSERVER_SPEED)
    return maxVelocity


def checkArenaPlayoffsType(playoffsType):
    import formula
    return formula.getPlayoffsType() == playoffsType


def lv2ArenaPlayoffs5v5Teamkey(lv):
    if lv >= 1 and lv <= 69:
        return '5v5_60_69'
    if lv >= 70 and lv <= 89:
        return '5v5_70_79'
    return '5v5_60_69'


def lv2ArenaPlayoffsTeamkey(lv, playoffsType = gametypes.ARENA_PLAYOFFS_TYPE_3V3):
    if playoffsType == gametypes.ARENA_PLAYOFFS_TYPE_3V3:
        if lv >= 1 and lv <= 59:
            return '1_59'
        if lv >= 60 and lv <= 69:
            return '60_69'
        if lv >= 70 and lv <= 89:
            return '70_79'
    elif playoffsType == gametypes.ARENA_PLAYOFFS_TYPE_5V5:
        if lv >= 60 and lv <= 69:
            return '5v5_60_69'
        if lv >= 70 and lv <= 89:
            return '5v5_70_79'
        if lv <= 59:
            return ''
    elif playoffsType == gametypes.ARENA_PLAYOFFS_TYPE_BALANCE:
        return 'balance'
    if BigWorld.component in ('cell', 'base'):
        import gameengine
        gameengine.reportSevereCritical('warning lv2ArenaPlayoffsTeamkey:%d' % lv)
    return ''


def arenaPlayoffsKey2playoffsType(lvKey):
    for playoffsType, lvKeys in gametypes.ARENA_PLAYOFFS_OPEN_LV_KEYS.iteritems():
        if lvKey in lvKeys:
            return playoffsType

    return 0


def inLiveOfArenaPlayoffs(owner):
    if not hasattr(owner, 'inLiveArenaPlayoffs'):
        return False
    return owner.inLiveArenaPlayoffs


def canInLiveOfArenaPlayoffs(owner):
    return owner.gmMode == const.GM_MODE_OBSERVER


def hasRunningArenaChallenge(owner):
    from data import arena_mode_data as AMD
    readyTime = AMD.data.get(const.ARENA_MODE_CROSS_MS_ROUND_1V1_CHALLENGE, {}).get('challengeReadyTime', 300)
    timestamp = owner.arenaChallengeNotifyEnterTimestamp
    if timestamp == 0:
        return False
    elif getNow() - timestamp > readyTime:
        return False
    else:
        return True


def getArenaReadyTime(fbNo, arenaPlayoffsCurRoundNum, roundNum):
    gamelog.info('@hjx arenaChallenge#getArenaReadyTime:', fbNo, arenaPlayoffsCurRoundNum, roundNum)
    import formula
    from data import arena_mode_data as AMD
    if enableArenaPlayoffsQuickReady():
        return const.ARENA_START_DELAY
    if isCrossArenaPlayoffsFb(fbNo):
        if roundNum > 1:
            return const.ARENA_START_DELAY
        else:
            arenaMode = formula.fbNo2ArenaMode(fbNo)
            return AMD.data.get(arenaMode, {}).get('readyTimes', {}).get(arenaPlayoffsCurRoundNum, 600)
    elif fbNo in const.FB_NO_CROSS_ROUND_CHALLENGE:
        if roundNum > 1:
            return const.ARENA_START_DELAY
        else:
            arenaMode = formula.fbNo2ArenaMode(fbNo)
            return AMD.data.get(arenaMode, {}).get('challengeReadyTime', 300)
    else:
        if fbNo == const.FB_NO_WING_WORLD_XINMO_ARENA:
            from data import wing_world_config_data as WWCD
            return WWCD.data.get('xinmoArenaPrepareTime', const.ARENA_START_DELAY)
        if fbNo in const.FB_NO_CROSS_2V2_ROUND_DOUBLE_ARENA_PLAYOFF:
            if roundNum > 1:
                return const.ARENA_START_DELAY
            else:
                from data import duel_config_data as DCD
                return DCD.data.get('dArenaPrepareTime', 60)
        else:
            if fbNo in const.FB_NO_CLAN_WAR_CHALLENGE:
                from data import clan_war_challenge_config_data as CWCCD
                return CWCCD.data.get('combatReadyTime', 180)
            if fbNo in const.FB_NO_LUN_ZHAN_YUN_DIAN:
                return const.ARENA_LZYD_DELAY
            return const.ARENA_START_DELAY


def checkArenaPlayoffsCandidateValid(owner, playoffsType = gametypes.ARENA_PLAYOFFS_TYPE_3V3):
    from data import duel_config_data as DCD
    if owner.arenaPlayoffsCandidateState == gametypes.ARENA_PLAYOFFS_CANDIDATE_STATE_DEFAULT:
        if playoffsType == gametypes.ARENA_PLAYOFFS_TYPE_3V3:
            score = DCD.data.get('playOffsCandidateScore', 0)
            return owner.lastSeasonArenaScore >= score
        if playoffsType == gametypes.ARENA_PLAYOFFS_TYPE_5V5:
            needLevel = DCD.data.get('playoffs5v5MinLevel', const.ARENA_PLAYOFFS_5V5_MIN_LEVEL)
            return owner.lv >= needLevel
    else:
        if owner.arenaPlayoffsCandidateState == gametypes.ARENA_PLAYOFFS_CANDIDATE_STATE_SUCC:
            return True
        if owner.arenaPlayoffsCandidateState == gametypes.ARENA_PLAYOFFS_CANDIDATE_STATE_FAILED:
            return False
    return False


def checkArenaScoreCandidateValid(owner):
    from data import duel_config_data as DCD
    if owner.lv >= DCD.data.get('ArenaScoreTeamFounderLevel', 40):
        return True
    return False


def getBFDamageScore(bfStats, myDamage):
    from data import sys_config_data as SCD
    UNIT_QUANTITY_DAMAGE_1 = SCD.data.get('UNIT_QUANTITY_DAMAGE_1', 60)
    UNIT_QUANTITY_DAMAGE_2 = SCD.data.get('UNIT_QUANTITY_DAMAGE_2', 50)
    UNIT_QUANTITY_DAMAGE_3 = SCD.data.get('UNIT_QUANTITY_DAMAGE_3', 40)
    index = 0
    UNIT_QUANTITY_DAMAGE = (UNIT_QUANTITY_DAMAGE_1, UNIT_QUANTITY_DAMAGE_2, UNIT_QUANTITY_DAMAGE_3)
    for value in bfStats:
        if value['damage'] > myDamage:
            index += 1

    if index < len(UNIT_QUANTITY_DAMAGE):
        return UNIT_QUANTITY_DAMAGE[index]
    else:
        return 0


def getBFCureScore(bfStats, myCure):
    from data import sys_config_data as SCD
    UNIT_QUANTITY_CURE_1 = SCD.data.get('UNIT_QUANTITY_CURE_1', 30)
    UNIT_QUANTITY_CURE_2 = SCD.data.get('UNIT_QUANTITY_CURE_2', 20)
    UNIT_QUANTITY_CURE_3 = SCD.data.get('UNIT_QUANTITY_CURE_3', 10)
    index = 0
    UNIT_QUANTITY_CURE = (UNIT_QUANTITY_CURE_1, UNIT_QUANTITY_CURE_2, UNIT_QUANTITY_CURE_3)
    for value in bfStats:
        if value['cure'] > myCure:
            index += 1

    if index < len(UNIT_QUANTITY_CURE):
        return UNIT_QUANTITY_CURE[index]
    else:
        return 0


def validSchemeNo(part):
    isGeneralScheme = 0 <= part < const.SKILL_POINT_SCHEME_NUM
    isArenaScheme = part == const.SKILL_SCHEME_ARENA
    isEquipSoulScheme = 0 < part <= const.EQUIP_SOUL_SCHEME_NUM
    isWingWorldSchemo = part == const.SKILL_SCHEME_WINGWORLD
    isCrossBfSchememe = part == const.SKILL_SCHEME_CROSS_BF
    isOneKeyConfigScheme = const.ONEKEYCONFIG_SCHEME_ID_DEFAULT <= part <= const.ONEKEYCONFIG_SCHEME_ID_EXTRA4
    return isGeneralScheme or isArenaScheme or isEquipSoulScheme or isWingWorldSchemo or isOneKeyConfigScheme or isCrossBfSchememe


def checkFbConditionInvalid(owner, fbNo, roleName):
    from data import fb_data as FD
    from data import fame_data as FMD
    from cdata import fb_unlock_data as FUD
    from cdata import game_msg_def_data as GMDD
    unlockFame = FUD.data.get(fbNo, {}).get('unlockFame', ())
    if unlockFame:
        fameId, needFameVal = unlockFame
        curFameVal = owner.fame.getFame(fameId)
        fameName = FMD.data.get(fameId, {}).get('name', '')
        if curFameVal < needFameVal:
            return (GMDD.data.FB_NOT_ENOUGH_XIU_WEI_ON_APPLY_FB_GROUP_MATCH, (roleName, fameName))
    fame = FD.data.get(fbNo, {}).get('fame', ())
    if fame:
        fameId, needFameVal = fame
        curFameVal = owner.fame.getFame(fameId)
        fameName = FMD.data.get(fameId, {}).get('name', '')
        if curFameVal < needFameVal:
            return (GMDD.data.FB_NOT_ENOUGH_FAME_ON_APPLY_FB_GROUP_MATCH, (roleName, fameName))
    return (None, None)


def isPrintableString(text):
    for c in text:
        if not 32 <= ord(c) <= 126:
            return False

    return True


def getRelativeTimeFromServerBootTime(endTime):
    serverBootTime = time.time() - BigWorld.time()
    return int((endTime - serverBootTime) * 10)


def getRealTimeFromServerBootTime(relativeTime):
    if BigWorld.component == 'client':
        serverBootTime = BigWorld.player().serverBootTime
        return relativeTime / 10.0 + serverBootTime
    else:
        serverBootTime = time.time() - BigWorld.time()
        return relativeTime / 10.0 + serverBootTime


MAX_STATE_END_TIME = 33554431
STATE_SHIFT_LAYER = 7
STATE_SHIFT_ENDTIME = 25

def encodeStateValue(stateId, stateSrcId, layer, endTime):
    temp = ((stateSrcId << STATE_SHIFT_LAYER) + layer << STATE_SHIFT_ENDTIME) + endTime
    return [temp & 65535,
     temp >> 16 & 65535,
     temp >> 32 & 65535,
     temp >> 48 & 65535,
     stateId]


STATE_MASK_SRC_ID = 4294967295L
STATE_MASK_LAYER = 2 ** STATE_SHIFT_LAYER - 1
STATE_MASK_ENDTIME = 2 ** STATE_SHIFT_ENDTIME - 1

def loadStateValue(data):
    temp = (((data[3] << 16) + data[2] << 16) + data[1] << 16) + data[0]
    return (data[4],
     temp >> 32 & STATE_MASK_SRC_ID,
     temp >> 25 & STATE_MASK_LAYER,
     temp & STATE_MASK_ENDTIME)


phoneVerify = re.compile('^0\\d{9,11}$|^1\\d{10}$|^\\+\\d{1,3}-\\d{5,20}$')

def isValidPhoneNum(phoneNum):
    global phoneVerify
    return phoneVerify.match(phoneNum)


def extractPhoneNum(phoneNum):
    if phoneNum.find('|') != -1:
        return ('86', phoneNum)
    if phoneNum.isdigit():
        return ('86', phoneNum)
    try:
        ctCode, phone = phoneNum.split('-')
        return (ctCode[1:], phone)
    except:
        return ('86', phoneNum)


def isMainlandPhoneNumber(phoneNum):
    ctCode = extractPhoneNum(phoneNum)[0]
    return ctCode is None or ctCode == '86'


def ip2long(ip):
    return struct.unpack('L', inet_aton(ip))[0]


if BigWorld.component in ('base', 'cell'):
    from data import log_src_def_data as LSDD

    def updateExpireTime(owner, it, renewalType, expireTime, resKind):
        if it == const.CONT_EMPTY_VAL:
            return
        if not it.canRenewalCommon() or it.getCommonRenewalType() != renewalType:
            return
        oldExpireTime = getattr(it, 'commonExpireTime', const.EXPIRE_TIME_NOT_SET)
        it.commonExpireTime = expireTime
        logSrc = LSDD.data.LOG_SRC_RENEWAL_USE_ITEM
        owner.logItem(it, 0, Netease.getNUID(), logSrc, [it.guid()], [it.guid()], '%d-%d' % (oldExpireTime, it.commonExpireTime), resKind)
        return it


def getEquipDyeList(equipId):
    from data import equip_data as ED
    data = ED.data.get(equipId, {})
    dyeMaterials = data.get('dyeMaterials', [])
    if dyeMaterials:
        return calcDyeListFromMaterial(dyeMaterials)
    else:
        return data.get('dyeList', [])


def calcDyeListFromMaterial(materialIds):
    if not materialIds:
        return []
    from cdata import material_dye_data as MDD
    dyeList = []
    for i, itemId in enumerate(materialIds):
        color = []
        if itemId in MDD.data:
            color = MDD.data[itemId].get('color', [])
        else:
            color = const.DEFAULT_DYES[:const.DYES_INDEX_TEXTURE]
        tColor = []
        for val in color:
            if isinstance(val, tuple) or isinstance(val, list):
                tColor.extend(val)
            else:
                tColor.append(val)

        dyeList.extend(tColor)
        if i == 0 and len(materialIds) == 2:
            dyeList.extend(const.DEFAULT_DYES[const.DYES_INDEX_TEXTURE:const.DYES_INDEX_DUAL_COLOR])

    return dyeList


def calcFullDyeListFromMaterials(materialIds, assignTexture = None):
    if not materialIds:
        return
    from cdata import material_dye_data as MDD
    dyeList = copy.deepcopy(const.DEFAULT_DYES)
    for i, itemId in enumerate(materialIds):
        if itemId not in MDD.data:
            return
        pbrcolor = MDD.data[itemId].get('pbrColor', [])
        if isinstance(pbrcolor, list):
            pbrcolor = pbrcolor[0]
        if i + 1 == const.DYE_CHANNEL_1:
            dyeList[const.DYES_INDEX_COLOR:const.DYES_INDEX_TEXTURE] = pbrcolor
            if assignTexture is not None:
                dyeList[const.DYES_INDEX_TEXTURE:const.DYES_INDEX_DUAL_COLOR] = assignTexture
        elif i + 1 == const.DYE_CHANNEL_2:
            dyeList[const.DYES_INDEX_DUAL_COLOR:const.DYES_INDEX_PBR_TEXTURE_DEGREE] = pbrcolor
        else:
            return

    return dyeList


def genRandomDyeList():
    return ['%d,%d,%d,%d' % (randint(0, 255),
      randint(0, 255),
      randint(0, 255),
      randint(0, 2000)), '%d,%d,%d,%d' % (randint(0, 255),
      randint(0, 255),
      randint(0, 255),
      randint(0, 2000))]


def genRandomNormalDyeMaterial():
    from cdata import material_dye_data as MDD
    keys = MDD.data.keys()
    random.shuffle(keys)
    for materialId in keys:
        if MDD.data[materialId].get('dyeQuality') == 1:
            return materialId

    return 0


def findItemCost(equip):
    from data import shihun_cost_data as SHCD
    from data import sys_config_data as SCD
    p = BigWorld.player()
    itemCost = []
    costData = None
    matchItem = None
    matchItemUUID = getattr(equip, 'shihunItemUUID', '')
    if matchItemUUID:
        matchItem, mpage, mpos = p.inv.findItemByUUID(matchItemUUID)
    if matchItem and not matchItem.isExpireTTL():
        itemCost.append((matchItem.id, 1))
        return itemCost
    for data in SHCD.data.itervalues():
        enhLvRange = data.get('enhLvRange')
        if enhLvRange:
            enhLv = getattr(equip, 'enhLv', 0)
            if enhLv < enhLvRange[0] or enhLv > enhLvRange[1]:
                continue
        lvRange = data.get('lvRange')
        if lvRange and (equip.lvReq < lvRange[0] or equip.lvReq > lvRange[1]):
            continue
        qualityRange = data.get('qualityRange')
        if qualityRange and (equip.quality < qualityRange[0] or equip.quality > qualityRange[1]):
            continue
        costData = data
        break

    if costData:
        itemCost = costData.get('itemCost')
    else:
        itemCost = SCD.data.get('shihunItemCost')
    realItemCost = []
    now = getNow()
    for itemId, num in itemCost:
        num = int(math.ceil(num * (equip.getShihunExpireTime() - now) * 1.0 / SCD.data.get('shihunTTL', const.SHIHUN_TTL)))
        realItemCost.append((itemId, num))

    return realItemCost


from data import zaiju_data as ZJD
from data import horsewing_data as HWD
from data import horsewing_speed_data as HWSD
from data import physics_config_data as PCD

def getWingSpeedData(owner):
    dataKey = None
    speedData = {}
    aspect = owner.aspect
    wingId = aspect.wingFly
    if owner.inCombat:
        keyName = 'combatSpeedId'
    else:
        keyName = 'speedId'
    wing = owner.equipment[gametypes.EQU_PART_WINGFLY]
    if wing:
        if wing.id == wingId:
            if isRideWingShareSpeedEnabled() and owner.hasSharedWingMaxSpeed():
                dataKey = owner.getCompoundWingSpeedSubId(owner.inCombat)
            else:
                dataKey = owner.equipment[gametypes.EQU_PART_WINGFLY].getRideWingSpeedId(owner.inCombat)
        else:
            dataKey = HWD.data.get(ED.data.get(wingId, {}).get('subId', [0])[0], {})[0].get(keyName)
    if dataKey:
        speedData = HWSD.data.get(dataKey, {})
    return speedData


def getHorseSpeedData(owner):
    dataKey = None
    speedData = {}
    ride = owner.equipment[gametypes.EQU_PART_RIDE]
    if ride:
        if isRideWingShareSpeedEnabled() and owner.hasSharedRideMaxSpeed:
            dataKey = owner.getCompoundRideSpeedSubId(owner.inCombat)
        else:
            dataKey = owner.equipment[gametypes.EQU_PART_RIDE].getRideWingSpeedId(owner.inCombat)
    if dataKey:
        speedData = HWSD.data.get(dataKey, {})
    return speedData


def getAvatarSpeedData(owner):
    dataKey = None
    speedData = {}
    if owner.inCombat:
        keyName = 'combatSpeedId'
    else:
        keyName = 'speedId'
    if owner.bianshen[0] == gametypes.BIANSHEN_ZAIJU or owner.bianshen[0] == gametypes.BIANSHEN_BIANYAO:
        key = owner.bianshen[1]
        data = ZJD.data.get(key, {})
        dataKey = data.get('subId', 0)
        horseData = HWD.data.get(dataKey, {})
        if horseData:
            dataKey = horseData[0].get('speedId', None)
    elif owner.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
        rideId = owner.bianshen[1]
        ride = owner.equipment[gametypes.EQU_PART_RIDE]
        if ride:
            if getRealRideId(ride) == rideId:
                if isRideWingShareSpeedEnabled() and owner.hasSharedRideMaxSpeed:
                    dataKey = owner.getCompoundRideSpeedSubId(owner.inCombat)
                else:
                    dataKey = owner.equipment[gametypes.EQU_PART_RIDE].getRideWingSpeedId(owner.inCombat)
            else:
                dataKey = HWD.data.get(ED.data.get(rideId, {}).get('subId', [0])[0], {})[0].get(keyName)
    elif owner.inFly:
        aspect = owner.aspect
        wingId = aspect.wingFly
        wing = owner.equipment[gametypes.EQU_PART_WINGFLY]
        if wing:
            if wing.id == wingId:
                if isRideWingShareSpeedEnabled() and owner.hasSharedWingMaxSpeed():
                    dataKey = owner.getCompoundWingSpeedSubId(owner.inCombat)
                else:
                    dataKey = owner.equipment[gametypes.EQU_PART_WINGFLY].getRideWingSpeedId(owner.inCombat)
            else:
                dataKey = HWD.data.get(ED.data.get(wingId, {}).get('subId', [0])[0], {})[0].get(keyName)
    if dataKey:
        speedData = HWSD.data.get(dataKey, {})
    return speedData


def getFlySpeed(owner):
    resSpeed = 0
    if len(owner.speed) > 3:
        resSpeed = owner.speed[gametypes.SPEED_FLY] / 60.0
    else:
        resSpeed = gametypes.FLY_H_SPEED_BASE
    if owner.bianshen[0] == gametypes.BIANSHEN_ZAIJU:
        if ZJD.data.get(owner.bianshen[1], {}).get('replaceProperty', False):
            resSpeed = owner.speed[gametypes.SPEED_RIDE] / 60.0
    if owner.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
        equipRide = owner.equipment.get(gametypes.EQU_PART_RIDE)
        if equipRide:
            resSpeed = resSpeed * equipRide.getVelocityDuraFactor() * equipRide.getVelocityFactorByVip(owner)
    else:
        equipWingFly = owner.equipment.get(gametypes.EQU_PART_WINGFLY)
        if equipWingFly:
            resSpeed = resSpeed * equipWingFly.getVelocityDuraFactor() * equipWingFly.getVelocityFactorByVip(owner)
            if owner.coupleEmote and owner.coupleEmote[1] == owner.id:
                resSpeed = resSpeed * equipWingFly.getCoupleEmoteVelocityFactor()
    return resSpeed


def getFlyMaxSpeed(owner):
    speedData = getAvatarSpeedData(owner)
    return getFlySpeed(owner) * speedData.get('flyMaxFactor', gametypes.FLY_MAX_SPEED_FACTOR)


def getFlyHorizonSpeed(owner):
    speedData = getAvatarSpeedData(owner)
    return getFlySpeed(owner) * speedData.get('flyHorizonFactor', gametypes.FLY_HORIZON_SPEED_FACTOR)


def getFlyVerticalSpeed(owner):
    speedData = getAvatarSpeedData(owner)
    return getFlySpeed(owner) * speedData.get('flyVerticalFactor', gametypes.FLY_VERTICAL_SPEED_FACTOR)


def getFlyRushMaxSpeed(owner):
    speedData = getAvatarSpeedData(owner)
    return getFlySpeed(owner) * speedData.get('flyRushMaxFactor', gametypes.FLY_RUSH_SPEED_FACTOR)


def getHorseSpeedBase(owner):
    resSpeed = 0
    if len(owner.speed) > 5:
        resSpeed = owner.speed[gametypes.SPEED_RIDE] / 60.0
    else:
        resSpeed = gametypes.HORSE_H_SPEED_BASE
    if owner.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
        equipRide = owner.equipment.get(gametypes.EQU_PART_RIDE)
        if equipRide:
            return resSpeed * equipRide.getVelocityDuraFactor() * equipRide.getVelocityFactorByVip(owner)
    return resSpeed


def getSwimSpeed(owner):
    if len(owner.speed) > 4:
        return owner.speed[gametypes.SPEED_SWIM] / 60.0
    return gametypes.SWIM_H_SPEED_BASE


def getDashRushTopSpeed(owner):
    speedData = getAvatarSpeedData(owner)
    return PCD.data.get('dashRushTopSpeed', gametypes.DASHRUSHTOP_SPEED) * speedData.get('flyDashFactor', 1.0)


def getDashRushTopWeaponInHandSpeed(owner):
    speedData = getAvatarSpeedData(owner)
    return PCD.data.get('dashRushTopWeaponInHandSpeed', gametypes.DASHRUSHTOP_WEAPON_IN_HAND_SPEED) * speedData.get('flyDashFactor', 1.0)


def getMoveSpeedBase(owner):
    runFwdSpeed = owner.speed[gametypes.SPEED_MOVE] / 60.0 if owner.speed[gametypes.SPEED_MOVE] else 5.0
    if hasattr(owner, 'bianshen') and getattr(owner, 'bianshen', (0, 0))[0]:
        runFwdSpeed = getHorseSpeedBase(owner)
    return runFwdSpeed


def getDashFactor(owner):
    speedData = getAvatarSpeedData(owner)
    return speedData.get('dashFactor', 1.0)


def getSwimDashFactor(owner):
    speedData = getAvatarSpeedData(owner)
    return speedData.get('swimDashFactor', 1.0)


def getDashUpForwardSpeed(owner):
    speed = PCD.data.get('dashUpForwardSpeed', gametypes.DASHUP_FORWARD_SPEED) * getDashFactor(owner)
    return speed * owner.getQingGongData(gametypes.QINGGONG_FAST_RUN_JUMP).get('speedFactor', 1)


def getDashUpForwardSpeed1(owner):
    speed = PCD.data.get('dashUpForwardSpeed1', gametypes.DASHUP_FORWARD_SPEED1) * getDashFactor(owner)
    return speed * owner.getQingGongData(gametypes.QINGGONG_FAST_RUN_BIG_JUMP).get('speedFactor', 1)


def getHorseDashUpForwardSpeed(owner):
    speed = PCD.data.get('horseDashUpForwardSpeed', gametypes.DASHUP_FORWARD_SPEED) * getDashFactor(owner)
    return speed * owner.getQingGongData(gametypes.QINGGONG_MOUNT_JUMP).get('speedFactor', 1)


def getDashNormalSpeed(owner):
    speed = PCD.data.get('dashForwardSpeed', gametypes.DASHFORWARD_SPEED) * getDashFactor(owner)
    return speed * owner.getQingGongData(gametypes.QINGGONG_STATE_FAST_RUN).get('speedFactor', 1) * getHorseDuraFactor(owner) * getHorseVelocityFactorByVip(owner)


def getHorseDuraFactor(owner):
    if owner.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
        equipRide = owner.equipment.get(gametypes.EQU_PART_RIDE)
        if equipRide:
            return equipRide.getVelocityDuraFactor()
    return 1


def getHorseVelocityFactorByVip(owner):
    if owner.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
        equipRide = owner.equipment.get(gametypes.EQU_PART_RIDE)
        if equipRide:
            return equipRide.getVelocityFactorByVip(owner)
    return 1


def getHorseDashNormalSpeed(owner):
    speed = PCD.data.get('dashForwardSpeed', gametypes.DASHFORWARD_SPEED) * getDashFactor(owner)
    return speed * owner.getQingGongData(gametypes.QINGGONG_STATE_MOUNT_DASH).get('speedFactor', 1) * getHorseDuraFactor(owner) * getHorseVelocityFactorByVip(owner)


def getRideSwimDashSpeed(owner):
    speed = PCD.data.get('dashForwardSpeed', gametypes.DASHFORWARD_SPEED) * getSwimDashFactor(owner)
    return speed * getHorseDuraFactor(owner) * getHorseVelocityFactorByVip(owner)


def getDashFlySpeedBase(owner):
    return PCD.data.get('dashRushSpeed', gametypes.DASHRUSH_SPEED) * getSlideFactor(owner)


def getDashFlySpeedLvUp(owner):
    return getDashFlySpeedBase(owner) * owner.getQingGongData(gametypes.QINGGONG_FAST_RUN_DOUBLE_JUMP).get('speedFactor', 1)


def getRushDownFwdSpeed(owner):
    speed = PCD.data.get('rushDownFwdSpeed', gametypes.RUSH_DOWN_FWD_SPEED) * getSlideFactor(owner)
    return speed * owner.getQingGongData(gametypes.QINGGONG_RUSH_DOWN).get('speedFactor', 1)


def getRushDownWeaponInHandFwdSpeed(owner):
    speed = PCD.data.get('rushDownWeaponInHandFwdSpeed', gametypes.RUSH_DOWN_WEAPON_IN_HAND_FWD_SPEED) * getSlideFactor(owner)
    return speed * owner.getQingGongData(gametypes.QINGGONG_RUSH_DOWN_WEAPON_IN_HAND).get('speedFactor', 1)


def getSlideFactor(owner):
    speedData = getAvatarSpeedData(owner)
    return speedData.get('slideFactor', 1.0)


def getAutoJumpForwardSpeedBase(owner):
    speed = PCD.data.get('autoJumpForwardSpeed', gametypes.AUTO_JUMP_FORWARD_SPEED)
    return speed * owner.getQingGongData(gametypes.QINGGONG_AUTO_JUMP).get('speedFactor', 1)


def getDashAutoJumpForwardSpeedBase(owner):
    speed = PCD.data.get('dashAutoJumpForwardSpeed', gametypes.DASH_AUTO_JUMP_FORWARD_SPEED)
    return speed * owner.getQingGongData(gametypes.QINGGONG_DASH_AUTO_JUMP).get('speedFactor', 1)


def lvUpRideWingFilter(it, eData):
    if eData.has_key('stageRequire'):
        if not hasattr(it, 'rideWingStage'):
            return False
        if it.rideWingStage < eData.get('stageRequire'):
            return False
        if eData.get('maxExpRequire', 0) and it.rideWingStage == eData.get('stageRequire') and it.starExp < it.getRideWingMaxUpgradeExp():
            return False
    return True


def getEquipGemData(gemId):
    from item import Item
    from data import equip_gem_data as EGD
    pid = Item.parentId(gemId)
    return EGD.data.get(pid, {})


from cdata import life_skill_quality_reverse_data as LSQRD

def getLifeSkillRelatedId(itemId):
    pid = LSQRD.data.get(itemId, 0)
    if pid:
        return pid
    return itemId


def getRealConsumeLifeSkillItems(consumeItems, userSpecifiedItems):
    tDict = copy.copy(consumeItems)
    if userSpecifiedItems:
        for itemId in userSpecifiedItems:
            if not itemId:
                continue
            relatedId = getLifeSkillRelatedId(itemId)
            if tDict.has_key(relatedId):
                tDict[itemId] = tDict[relatedId]
                del tDict[relatedId]
            else:
                return None

    return tDict


if BigWorld.component in ('cell', 'base'):
    from cdata import life_skill_quality_data as LSQD

    def getLifeSkillFineItemId(itemId):
        subId = LSQD.data.get(itemId, {}).get('fineItemId', 0)
        return subId


    def getFinalLifeSkillByQuality(itemId, quality):
        if quality == 0:
            return itemId
        subId = LSQD.data.get(itemId, {}).get('fineItemId')
        if not subId:
            return itemId
        elif randint(0, 100) <= quality:
            return subId
        else:
            return itemId


    def bytearrayToDbString(data):
        ret = data
        ret.rstrip(' ')
        return zlib.compress(str(ret))


    def dbStringToBytearrayToDbString(data):
        try:
            return bytearray(zlib.decompress(data))
        except:
            return bytearray('')


from data import horsewing_upgrade_data as HWUD
from data import equip_data as ED

def getRideWingProps(item):
    if not item.isWingOrRide():
        return []
    props = HWUD.data.get((item.quality, item.getVehicleType(), item.rideWingStage), {}).get('props', [])
    return props


def getHorseQinggongAdjustEx(itemId, quality, vehicleType, rideWingStage):
    if itemId == 0:
        return 1.0
    adjust = HWUD.data.get((quality, vehicleType, rideWingStage), {}).get('horseQingGongAdjust', 0)
    if not adjust:
        adjust = ED.data.get(itemId, {}).get('horseQingGongAdjust', 1.0)
    return adjust


def getHorseQinggongAdjust(item):
    if not item.isWingOrRide():
        return 1
    adjust = None
    if hasattr(item, 'rideWingStage'):
        adjust = HWUD.data.get((item.quality, item.getVehicleType(), item.rideWingStage), {}).get('horseQingGongAdjust', 0)
    if not adjust:
        adjust = ED.data.get(item.id, {}).get('horseQingGongAdjust', 1.0)
    return adjust


def getWingQinggongAdjustEx(itemId, quality, vehicleType, rideWingStage):
    if itemId == 0:
        return 1.0
    adjust = HWUD.data.get((quality, vehicleType, rideWingStage), {}).get('wingQingGongAdjust', 0)
    if not adjust:
        adjust = ED.data.get(itemId, {}).get('wingQingGongAdjust', 1.0)
    return adjust


def getWingQinggongAdjust(item):
    if not item.isWingOrRide():
        return 1
    adjust = None
    if hasattr(item, 'rideWingStage'):
        adjust = HWUD.data.get((item.quality, item.getVehicleType(), item.rideWingStage), {}).get('wingQingGongAdjust', 0)
    if not adjust:
        adjust = ED.data.get(item.id, {}).get('wingQingGongAdjust', 1.0)
    return adjust


def getUniqueList(dataList):
    alreadySeen = set()
    return [ x for x in dataList if not (x in alreadySeen or alreadySeen.add(x)) ]


def getIsolateBails(player, isolateBailsTypeInfo, isolateLvInterval):
    if not isolateBailsTypeInfo.has_key(player.isolateType):
        return 0
    lvIndex = 0
    for i, (lvStart, lvEnd) in enumerate(isolateLvInterval):
        if player.lv >= lvStart and player.lv <= lvEnd:
            lvIndex = i
            break

    isolateCnt = player.isolateInfo.get(player.isolateType, 1)
    isolateBailsInfo = isolateBailsTypeInfo[player.isolateType][lvIndex]
    if isolateCnt > max(isolateBailsInfo.keys()):
        coinCnt = isolateBailsInfo[max(isolateBailsInfo.keys())]
    else:
        coinCnt = isolateBailsInfo.get(isolateCnt, 0)
    return coinCnt


def getResetWudaoRes(skillId, wudaoCntDict, wudaoItemId):
    from data import ws_skill_config_data as WSCD
    res = {}
    configData = WSCD.data.get(skillId)
    if not configData:
        return res
    lingliCost = configData.get('wudaoLingliCost', ())
    returnRatio = configData['defaultReturnRatio'] * 0.01
    resetWudaoItems = dict(configData.get('resetWudaoItems', ()))
    if wudaoItemId and wudaoItemId not in resetWudaoItems:
        gamelog.error('zt: invalid wudao item', wudaoItemId, resetWudaoItems)
        return res
    if wudaoItemId:
        returnRatio = resetWudaoItems[wudaoItemId] * 0.01
    for gemTp, wudaoLv in wudaoCntDict.iteritems():
        for lv in xrange(1, wudaoLv + 1):
            lingliType, lingliCostVal = lingliCost[lv - 1]
            res[lingliType] = res.get(lingliType, 0) + lingliCostVal

    for lingliType, lingliVal in res.iteritems():
        res[lingliType] = int(lingliVal * returnRatio)

    return res


def countWudaoLingli(skillId, wudaoCntDict):
    from data import ws_skill_config_data as WSCD
    res = {}
    configData = WSCD.data.get(skillId)
    if not configData:
        return res
    lingliCost = configData.get('wudaoLingliCost', ())
    for gemTp, wudaoLv in wudaoCntDict.iteritems():
        for lv in xrange(1, wudaoLv + 1):
            lingliType, lingliCostVal = lingliCost[lv - 1]
            res[lingliType] = res.get(lingliType, 0) + lingliCostVal

    return res


def limitSprintByZaiju(player):
    if player.bianshen[0] == gametypes.BIANSHEN_ZAIJU:
        zaijuData = ZJD.data.get(player.bianshen[1], {})
        if zaijuData.get('limitSprint'):
            return True
    return False


def getRandomCnt(count, rate):
    total = 0
    for _ in xrange(count):
        if rate >= random.random():
            total += 1

    return total


def getRoundTableSeatNodeName(bindIdx):
    from data import sys_config_data as SCD
    roundTableSeatNodes = SCD.data.get('roundTableSeatNodes', ['HP_chair1',
     'HP_chair2',
     'HP_chair3',
     'HP_chair4',
     'HP_chair5',
     'HP_chair6'])
    return roundTableSeatNodes[bindIdx]


def getInteractiveNodeName(bindIdx):
    return 'HP_jiaohu_' + str(bindIdx + 1)


def getCarrierNodeName(bindIdx):
    if bindIdx < 10:
        return 'HP_ride0' + str(bindIdx)
    else:
        return 'HP_ride' + str(bindIdx)


def selectUseItemProperMessage(messageBuf):
    if not messageBuf:
        return
    from cdata import game_msg_def_data as GMDD
    messageSorted = [GMDD.data.ITEM_USE_CANNOT_APPLY_SELF,
     GMDD.data.ITEM_USE_ONLY_ENEMY,
     GMDD.data.ITEM_USE_ONLY_FRIEND,
     GMDD.data.ITEM_USE_FORBIDDEN_BY_QUEST,
     GMDD.data.ITEM_USE_FORBIDDEN_WRONG_MAP,
     GMDD.data.ITEM_USE_BODYTYPE_ERROR,
     GMDD.data.ITEM_TTL_EXPIRE,
     GMDD.data.ITEM_FORBIDDEN_WRONG_SEX,
     GMDD.data.ITEM_FORBIDDEN_WRONG_SCHOOL,
     GMDD.data.ITEM_FORBIDDEN_LEVEL_LOWER,
     GMDD.data.ITEM_FORBIDDEN_LEVEL_UPPER,
     GMDD.data.ITEM_FORBIDDEN_SPECIAL_PERIOD,
     GMDD.data.ITEM_FORBIDDEN_IN_COMBAT,
     GMDD.data.USE_ITEM_FORBIDDEN_ZAIJU,
     GMDD.data.ITEM_FORBIDDEN_WRONG_FISHINGLV,
     GMDD.data.CON_FAME_FAILED_LV,
     GMDD.data.CON_SOCSCHOOL_FAILED,
     GMDD.data.CON_LIFE_SKILL_FAILED_LV,
     GMDD.data.CON_PROP_FAILED,
     GMDD.data.CON_BUFF_FAILED,
     GMDD.data.CON_NO_BUFF_FAILED,
     GMDD.data.CON_QUEST_FAILED,
     GMDD.data.CON_SOCLV_FAILED,
     GMDD.data.ITEM_RELIVE_SINGLE_LIMITED,
     GMDD.data.ITEM_USE_OUT_OF_LIMIT_COUNT,
     GMDD.data.JING_JIE_LIMIT,
     GMDD.data.ITEM_FORBIDDEN_LATCH,
     GMDD.data.ITEM_NOT_READY,
     GMDD.data.ITEM_FORBID_IN_FLY]
    for x in messageSorted:
        if x in messageBuf:
            return (x, messageBuf[x])


def getIntfmtSec(sec = None):
    if sec is None:
        sec = getNow()
    tplSec = time.localtime(sec)
    return '%02d%02d%02d%02d%02d%02d' % tplSec[:6]


def getYearMonthDayfmtSec(sec = None):
    if sec is None:
        sec = getNow()
    tplSec = time.localtime(sec)
    return '%02d%02d%02d' % tplSec[:3]


def encodeLottery(lotteryId, issueTime, nuid):
    return '%03d%s%s' % (lotteryId, issueTime, nuid)


def decodeLottery(lotteryNo):
    if not lotteryNo:
        return (0, 0, 0)
    lotteryId = int(lotteryNo[:3])
    issueTime = int(lotteryNo[3:13])
    nuid = int(lotteryNo[13:])
    return (lotteryId, issueTime, nuid)


def getLotteryNextTime(now, lotteryTime, lotteryInterval):
    if lotteryTime > now:
        nextTime = lotteryTime
    else:
        nextTime = int(math.ceil(float(now - lotteryTime) / lotteryInterval)) * lotteryInterval + lotteryTime
    return nextTime


def getDisplayLotteryNo(nuid):
    if not nuid:
        return ''
    ip = nuid & 255
    pid = nuid >> 8 & 65535
    x256 = nuid >> 24 & 255
    tm = nuid >> 32 & 4294967295L
    n = (ip << 56) + (pid << 40) + (x256 << 32) + tm
    return hex(n).upper()[2:-1]


def checkValuableTradeItem(item):
    if item.isValuable():
        valuableLatchOfTime = getattr(item, 'valuableLatchOfTime', 0)
        if valuableLatchOfTime:
            if getNow() >= valuableLatchOfTime:
                return True
            else:
                return False
    return True


def addMotorsChild(motors, am):
    if not motors or not am:
        return
    for motor in motors:
        if motor.__class__.__name__ == 'ActionMatcher':
            motor.addChild(am)
            break


def formatTimeStr(sec, formatStr = gameStrings.TEXT_WINGWORLDINFOPROXY_90, zeroShow = False, sNum = 1, mNum = 0, hNum = 0, replaceOnce = False):
    if formatStr.find('d') != -1:
        d = sec / const.TIME_INTERVAL_DAY
        sec = sec % const.TIME_INTERVAL_DAY
        formatStr = formatStr.replace('d', str(d))
    else:
        d = 0
    h = sec / const.TIME_INTERVAL_HOUR
    m = sec % const.TIME_INTERVAL_HOUR / const.TIME_INTERVAL_MINUTE
    s = sec % const.TIME_INTERVAL_MINUTE
    if not zeroShow:
        if d == 0 and formatStr.find('h') != -1:
            formatStr = formatStr[formatStr.index('h'):]
        if d == 0 and h == 0 and formatStr.find('m') != -1:
            formatStr = formatStr[formatStr.index('m'):]
        if d == 0 and h == 0 and m == 0 and formatStr.find('s') != -1:
            formatStr = formatStr[formatStr.index('s'):]
    hStr = str(h)
    while hNum > len(hStr):
        hStr = '0%s' % hStr

    mStr = str(m)
    while mNum > len(mStr):
        mStr = '0%s' % mStr

    sStr = str(s)
    while sNum > len(sStr):
        sStr = '0%s' % sStr

    if replaceOnce:
        formatStr = formatStr.replace('h', str(hStr), 1)
        formatStr = formatStr.replace('m', str(mStr), 1)
        formatStr = formatStr.replace('s', str(sStr), 1)
    else:
        formatStr = formatStr.replace('h', str(hStr))
        formatStr = formatStr.replace('m', str(mStr))
        formatStr = formatStr.replace('s', str(sStr))
    return formatStr


def matchesFbKeyAndFbNo(key, fbNo):
    if str(key) == str(fbNo):
        return True
    try:
        return key.split('_')[0] == str(fbNo)
    except:
        return False


def _getTopRankSimpleKey2(lv, school):
    if 1 <= lv <= 69:
        return '1_69_' + str(school)
    if 70 <= lv <= 89:
        return '70_79_' + str(school)


def _getTopRankSimpleKey3(lv, school):
    if 1 <= lv <= 59:
        return '1_59_' + str(school)
    if 60 <= lv <= 69:
        return '60_69_' + str(school)
    if 70 <= lv <= 89:
        return '70_79_' + str(school)


def _getTopRankSimpleKeyEx3(lv, school, lvMin):
    if lvMin <= lv <= 59:
        return str(lvMin) + '_59_' + str(school)
    if 60 <= lv <= 69:
        return '60_69_' + str(school)
    if 70 <= lv <= 89:
        return '70_79_' + str(school)


def getTopRankKey(topType, lv, school = 0, fbNo = 0):
    if topType == gametypes.TOP_TYPE_FB:
        from cdata import fb_top_server_data as FTD
        if FTD.data.get(fbNo, {}).get('isByClass'):
            return str(fbNo) + '_' + str(school)
        else:
            return str(fbNo)
    if topType == gametypes.TOP_TYPE_COMBAT_SCORE:
        if fbNo == gametypes.ALL_LV_TOP_RANK_KEY:
            return gametypes.ALL_LV_TOP_RANK_KEY
        if fbNo:
            school = 0
        return _getTopRankSimpleKey3(lv, school)
    if topType == gametypes.TOP_TYPE_ARENA_SCORES or topType == gametypes.TOP_TYPE_GLOBAL_ARENA_SCORE:
        if fbNo == gametypes.ALL_LV_TOP_RANK_KEY:
            return gametypes.ALL_LV_TOP_RANK_KEY
        if fbNo:
            school = 0
        return _getTopRankSimpleKey3(lv, school)
    if topType in (gametypes.TOP_TYPE_ARENA_SCORES_BALANCE, gametypes.TOP_TYPE_ARENA_SCORES_GLOBAL_BALANCE):
        if fbNo == gametypes.NORMAL_TOP_RANK_KEY:
            return gametypes.NORMAL_TOP_RANK_KEY
        return str(school)
    if topType == gametypes.TOP_TYPE_ZHAN_XUN or topType == gametypes.TOP_TYPE_FAMOUS_GENERAL_LV:
        if fbNo == gametypes.ALL_LV_TOP_RANK_KEY:
            return gametypes.ALL_LV_TOP_RANK_KEY
        if fbNo:
            school = 0
        return _getTopRankSimpleKey3(lv, school)
    if topType == gametypes.TOP_TYPE_YUNCHUI_GUILD_SCORE:
        return str(fbNo)
    if topType == gametypes.TOP_TYPE_ENDLESS_CHALLENGE:
        if fbNo == gametypes.ALL_LV_TOP_RANK_KEY:
            return gametypes.ALL_LV_TOP_RANK_KEY
        return _getTopRankSimpleKeyEx3(lv, school, 50)
    if topType == gametypes.TOP_TYPE_SPRITE_CHALLENGE:
        if fbNo == gametypes.ALL_LV_TOP_RANK_KEY:
            return gametypes.ALL_LV_TOP_RANK_KEY
        school = 0
        if 60 <= lv <= 69:
            return '60_69_' + str(school)
        if 70 <= lv <= 89:
            return '70_79_' + str(school)
    if topType == gametypes.TOP_TYPE_MONSTER_CLAN_WAR:
        if 40 <= lv <= 69:
            return '40_69_' + str(school)
        if 70 <= lv <= 89:
            return '70_79_' + str(school)
    if topType == gametypes.TOP_TYPE_HALL_OF_FAME_XIUWEI:
        if fbNo == gametypes.ALL_LV_TOP_RANK_KEY:
            return gametypes.ALL_LV_TOP_RANK_KEY
        school = 0
        if 1 <= lv <= 69:
            return '1_69_' + str(school)
        if 70 <= lv <= 89:
            return '70_79_' + str(school)
    if topType == gametypes.TOP_TYPE_HALL_OF_FAME_SHENBING:
        if fbNo == gametypes.ALL_LV_TOP_RANK_KEY:
            return gametypes.ALL_LV_TOP_RANK_KEY
        if fbNo:
            school = 0
        return _getTopRankSimpleKey2(lv, school)
    if topType == gametypes.TOP_TYPE_SKY_WING_CHALLENGE:
        if fbNo == gametypes.ALL_LV_TOP_RANK_KEY:
            return gametypes.ALL_LV_TOP_RANK_KEY
        return _getTopRankSimpleKey2(lv, school)
    if topType == gametypes.TOP_TYPE_SPRITE_COMBAT_SCORE:
        if isinstance(fbNo, dict) and fbNo.get('topKey') == gametypes.ALL_LV_TOP_RANK_KEY:
            return gametypes.ALL_LV_TOP_RANK_KEY
        school = 0
        return _getTopRankSimpleKey3(lv, school)
    if topType == gametypes.TOP_TYPE_CARD_COMBAT_SCORE:
        if fbNo == gametypes.ALL_LV_TOP_RANK_KEY:
            return gametypes.ALL_LV_TOP_RANK_KEY
        school = 0
        return _getTopRankSimpleKey3(lv, school)
    if topType in gametypes.LV_DEPENDENT_TOP_RANK_LIST:
        if fbNo == gametypes.ALL_LV_TOP_RANK_KEY:
            return gametypes.ALL_LV_TOP_RANK_KEY
        return _getTopRankSimpleKey3(lv, school)
    if topType == gametypes.TOP_TYPE_WW_KILL_AVATAR or topType == gametypes.TOP_TYPE_WW_KILL_AVATAR_TOTAL or topType == gametypes.TOP_TYPE_CHAR_TEMP_HEAT_RANK:
        if school:
            return str(school)
    if topType == gametypes.TOP_TYPE_WW_ROB_SCORE or topType == gametypes.TOP_TYPE_WB_SCORE:
        if isinstance(fbNo, Iterable):
            if len(fbNo) >= 1:
                return str(school) + '_' + str(fbNo[0])
            gamelog.warning('cgy#wwrobOrBattleTopRankArgsError: ', fbNo)
    if topType == gametypes.TOP_TYPE_WING_WORLD_BOSS_DAMAGE_RANK:
        return _getTopRankSimpleKey3(lv, school)
    if topType == gametypes.TOP_TYPE_WING_WORLD_XINMO_FB and isinstance(fbNo, dict):
        fromHostId = fbNo.get('extra', {}).get(const.WING_WORLD_XINMO_FB_RANK_EXTRA_INDEX_HOSTID, 0)
        if fromHostId:
            groupId = getWingWorldGroupId(fromHostId)
            if groupId:
                return str(groupId)
    if topType == gametypes.TOP_TYPE_DOUBLE_ARENA_SCORE:
        return str(fbNo)
    if topType in gametypes.SCHOOL_DEPENDENT_TOP_RANK_LIST:
        return str(school)
    if topType == gametypes.TOP_TYPE_GUILD_BOSS_FOR_ELITE:
        return str(fbNo)
    if topType == gametypes.TOP_TYPE_TEAM_ENDLESS:
        return str(fbNo)
    if topType == gametypes.TOP_TYPE_WING_WORLD_CAMP_CONTRI_PERSON:
        return str(lv) + '_' + str(fbNo) + '_' + str(school)
    if topType == gametypes.TOP_TYPE_WING_WORLD_CAMP_CONTRI_GUILD:
        return str(lv) + '_' + str(fbNo)
    if topType == gametypes.TOP_TYPE_NPC_FAVOR:
        if isinstance(fbNo, dict):
            return str(fbNo.get('key', 0))
    if topType == gametypes.TOP_TYPE_WING_WORLD_SEASON_CONTRI:
        return str(lv) + '_' + str(fbNo) + '_' + str(school)
    if topType == gametypes.TOP_TYPE_WING_WORLD_GUILD_SEASON_CONTRI:
        return str(lv) + '_' + str(fbNo)
    return '0'


def getYunChuiRankType(key):
    if key in ('1', '2', '3'):
        return const.YUNCHUI_TOP_TYPE_MONTH
    elif key in ('0',):
        return const.YUNCHUI_TOP_TYPE_QUARTER
    else:
        return const.YUNCHUI_TOP_TYPE_HISTORY


def needRefreshTopStubOnLevelUp(lv, oldLv = None):
    oldLv = lv - 1 if oldLv == None else oldLv
    if oldLv <= 59 and lv >= 60 or oldLv <= 69 and lv >= 70 or oldLv <= 79 and lv >= 80:
        return True
    return False


def getJuexingDataStep(item, enhLv, juexingData, juexingConfigData):
    matchNumber = 0
    nowData = juexingConfigData.get((item.equipType,
     item.equipSType,
     enhLv,
     item.enhanceType), [])
    for singleData in nowData:
        if type(singleData) == str:
            raise Exception('error!!!!, wrong eejd data, key:%d,%d,%d,%d', item.equipType, item.equipSType, enhLv, item.enhanceType)
            continue
        enhanceJuexingProps = singleData.get('enhanceJuexingProps', ())
        for enhanceJuexingProp in enhanceJuexingProps:
            if enhanceJuexingProp[0] == juexingData[0]:
                matchNumber += 1
                minValue = enhanceJuexingProp[2]
                maxValue = enhanceJuexingProp[3]
                step = enhanceJuexingProp[4]
                currentValue = juexingData[2]
                diff = currentValue - minValue
                if maxValue == minValue:
                    nowStep = step
                else:
                    nowStep = int(round(float(diff) * step / (maxValue - minValue)))
                return nowStep

    if matchNumber == 0:
        return EQUIP_TYPR_MISMATCH
    return 0


def isValidCrontabString(string):
    pass


def getIndulgeStateOfTime(onlineTime):
    if onlineTime < const.INDULGE_ONLINE_HALF_TIRED_TIME:
        return const.INDULGE_PROFIT_HEALTHY
    elif onlineTime < const.INDULGE_ONLINE_TIRED_TIME:
        return const.INDULGE_PROFIT_HALF_TIRED
    else:
        return const.INDULGE_PROFIT_TIRED


def calcBattleFieldWaitRewardJunzi(tApply, tJoin):
    from data import duel_config_data as DCD
    interval = tJoin - tApply
    baseSecond = DCD.data.get('WAIT_REWARD_BASE_SECOND', 10)
    baseJunzi = DCD.data.get('WAIT_REWARD_BASE_JUNZI', 5)
    maxWaitRewardJunzi = DCD.data.get('WAIT_REWARD_MAX_JUNZI', 50)
    return min(max(interval / baseSecond * baseJunzi, 0), maxWaitRewardJunzi)


def checkCanChangeSex(player):
    from cdata import game_msg_def_data as GMDD
    from data import item_data as ID
    fbox = player
    if BigWorld.component != 'client':
        fbox = player.client
        enableHomosexualIntimacy = gameconfig.enableHomosexualIntimacy()
    else:
        enableHomosexualIntimacy = gameglobal.rds.configData.get('enableHomosexualIntimacy', False)
    if player.curSocSchool:
        fbox.showGameMsg(GMDD.data.CANNOT_CHANGE_SEX, gameStrings.TEXT_UTILS_5317)
        return False
    if BigWorld.component != 'client' and isInternationalVersion():
        intimacyTgt = 0
        if BigWorld.component == 'cell':
            intimacyTgt = player.cellOfIntimacyTgt
        elif hasattr(player, 'friend'):
            intimacyTgt = player.friend.intimacyTgt
        if intimacyTgt:
            fbox.showGameMsg(GMDD.data.CANNOT_CHANGE_SEX, gameStrings.TEXT_UTILS_5327)
            return False
    if not enableHomosexualIntimacy:
        intimacyTgt = 0
        if BigWorld.component == 'cell':
            intimacyTgt = player.cellOfIntimacyTgt
        elif hasattr(player, 'friend'):
            intimacyTgt = player.friend.intimacyTgt
        if intimacyTgt:
            fbox.showGameMsg(GMDD.data.CANNOT_CHANGE_SEX, gameStrings.TEXT_UTILS_5327)
            return False
    for equip in player.equipment:
        if equip and ID.data.get(equip.id, {}).get('sexReq', 0):
            fbox.showGameMsg(GMDD.data.TAKE_OFF_EQUIP_SEXREQ, ())
            return False

    return True


def checkCanChangeBodyType(player):
    from cdata import game_msg_def_data as GMDD
    from data import item_data as ID
    fbox = player
    if BigWorld.component != 'client':
        fbox = player.client
    if player.curSocSchool:
        fbox.showGameMsg(GMDD.data.CANNOT_CHANGE_SEX, gameStrings.TEXT_UTILS_5317)
        return False
    for equip in player.equipment:
        if equip and ID.data.get(equip.id, {}).get('allowBodyType', 0):
            fbox.showGameMsg(GMDD.data.TAKE_OFF_EQUIP_BODYREQ, ())
            return False

    return True


def checkCanChangeBodyTypeByAppearance(appearance):
    from cdata import game_msg_def_data as GMDD
    from data import item_data as ID
    from helpers import charRes
    if not appearance:
        return False
    for key in charRes.PARTS_ASPECT + charRes.PARTS_ASPECT_FASHION:
        itemId = getattr(appearance, key, 0)
        if itemId and ID.data.get(itemId, {}).get('allowBodyType', 0):
            BigWorld.player().showGameMsg(GMDD.data.TAKE_OFF_EQUIP_BODYREQ, ())
            return False

    return True


def checkCanChangeSexByAppearance(appearance):
    from cdata import game_msg_def_data as GMDD
    from data import item_data as ID
    from helpers import charRes
    if not appearance:
        return False
    for key in charRes.PARTS_ASPECT + charRes.PARTS_ASPECT_FASHION:
        itemId = getattr(appearance, key, 0)
        if itemId and ID.data.get(itemId, {}).get('sexReq', 0):
            BigWorld.player().showGameMsg(GMDD.data.TAKE_OFF_EQUIP_BODYREQ, ())
            return False

    return True


def addDyeLists(dyeList, index, color):
    dyeList = list(dyeList)
    if not isinstance(color, tuple) and not isinstance(color, list):
        color = [color]
    if index in const.DYES_INDEXS:
        i = const.DYES_INDEXS.index(index)
        nextIndex = const.DYES_INDEXS[i + 1]
        if nextIndex - index == len(color):
            l = len(dyeList)
            if nextIndex >= l:
                dyeList.extend(const.DEFAULT_DYES[l:nextIndex])
            dyeList[index:nextIndex] = color
    return dyeList


def isPinyinAndHanzi(string):
    if isInternationalVersion():
        return const.STR_ONLY_HANZI
    pinyin = False
    hanzi = False
    for i in string:
        p = ord(i)
        if p > 128:
            hanzi = True
        else:
            pinyin = True

    if pinyin and hanzi:
        return const.STR_HANZI_PINYIN
    elif pinyin:
        return const.STR_ONLY_PINYIN
    else:
        return const.STR_ONLY_HANZI


def getCountryName(hostId):
    if BigWorld.component == 'client':
        if hostId in gametypes.WING_WORLD_CAMPS:
            return getWingCampName(hostId)
        else:
            from data import region_server_config_data as RSCD
            return RSCD.data.get(hostId, {}).get('serverName', '')
    elif BigWorld.component in ('base', 'cell'):
        if hostId in gametypes.WING_WORLD_CAMPS:
            return getWingCampName(hostId)
        else:
            return getServerName(hostId)
    return ''


def getWingCampName(campId = 0):
    if BigWorld.component == 'client':
        from gamestrings import gameStrings
        from data import wing_world_config_data as WWCFGD
        return WWCFGD.data.get('wingCampNames', gameStrings.WING_WORLD_CAMP_NAMES).get(campId, '')
    if BigWorld.component in ('base', 'cell'):
        from data import wing_world_config_data as WWCFGD
        return WWCFGD.data.get('wingCampNames', {}).get(campId)
    return ''


def getServerName(hostId = 0):
    from data import region_server_config_data as RSCD
    from cdata import region_server_name_data as RSND
    defaultName = ''
    if BigWorld.component in ('base', 'cell'):
        localHostId = int(gameconfig.getHostId())
        hostId = hostId or localHostId
        defaultName = gameconfig.getServerName() if hostId == localHostId else ''
    serverName = RSCD.data.get(hostId, {}).get('serverName', '')
    if not serverName:
        serverName = RSND.data.get(hostId, {}).get('serverName', '')
    if not serverName:
        serverName = defaultName
    return serverName


def regionServerHostId(hostId = 0):
    from data import region_server_config_data as RSCD
    if BigWorld.component in ('base', 'cell'):
        hostId = hostId or int(gameconfig.getHostId())
    regionData = RSCD.data.get(hostId)
    if not regionData:
        return 0
    return regionData.get('regionHostId', 0)


def regionServerName(hostId = 0):
    regionHostId = regionServerHostId(hostId)
    return getServerName(regionHostId)


def lzydRegionServerName(hostId = 0):
    regionHostId = lzydRegionServerHostId(hostId)
    return getServerName(regionHostId)


def lzydRegionServerHostId(hostId = 0):
    from data import region_server_config_data as RSCD
    if BigWorld.component in ('base', 'cell'):
        hostId = hostId or int(gameconfig.getHostId())
    regionData = RSCD.data.get(hostId)
    if not regionData:
        return 0
    return regionData.get('lzydRegionHostId', 0)


def isBattleFieldRegionServer(hostId = 0):
    if BigWorld.component in ('base', 'cell'):
        hostId = hostId or int(gameconfig.getHostId())
    else:
        return False
    return hostId == bfRegionServerHostId(hostId)


def isRegionServer(hostId = 0):
    from data import region_server_config_data as RSCD
    if BigWorld.component in ('base', 'cell'):
        hostId = hostId or int(gameconfig.getHostId())
    elif BigWorld.component == 'client':
        hostId = hostId or gameglobal.rds.g_serverid
    regionData = RSCD.data.get(hostId)
    if not regionData:
        return False
    serverTypes = regionData.get('serverType', ())
    for st in serverTypes:
        if st in gametypes.CROSS_SERVER_TYPES:
            return True

    return False


def arenaChallengeRegionServerName(hostId):
    from data import region_server_config_data as RSCD
    regionData = RSCD.data.get(hostId)
    if not regionData:
        return ''
    return getServerName(regionData.get('arenaChallengeRegionServer', 0))


def bfRegionServerHostId(hostId = 0):
    from data import region_server_config_data as RSCD
    if BigWorld.component in ('base', 'cell'):
        hostId = hostId or int(gameconfig.getHostId())
    regionData = RSCD.data.get(hostId)
    if not regionData:
        return 0
    return regionData.get('bfRegionHostId', 0)


def mlRegionHostId(mlgNo, hostId = 0, playerHostId = 0):
    from data import region_server_config_data as RSCD
    if BigWorld.component in ('base', 'cell'):
        hostId = hostId or int(gameconfig.getHostId())
        if gameconfig.eveDeployServer():
            return getHostId()
    regionData = RSCD.data.get(hostId)
    if not regionData:
        return 0
    if mlgNo == const.ML_GROUP_NO_WING_WORLD_XINMO and playerHostId:
        return getWingWorldXinMoRegionHostId(playerHostId)
    return regionData.get('mlRegionHost', {}).get(mlgNo, 0)


def isCrossGuildTournamentRegionServer():
    from data import cross_guild_tournament_region_data as CGTRD
    return CGTRD.data.has_key(getHostId())


def isNewGuildTournamentRegionServer():
    from data import region_server_config_data as RSCD
    if RSCD.data.has_key(getHostId()):
        if RSCD.data[getHostId()].has_key('rankGTNRegionHostId'):
            if RSCD.data[getHostId()]['rankGTNRegionHostId'] == getHostId():
                return True
    return False


def getCrossGuildTournamentRegionServerHostId():
    from data import region_server_config_data as RSCD
    return RSCD.data.get(getHostId(), {}).get('gtnRegionHostId', 0)


def getCrossGuildTournamentRegionServerName():
    from data import region_server_config_data as RSCD
    regionData = RSCD.data.get(getCrossGuildTournamentRegionServerHostId())
    if regionData:
        return regionData.get('serverName')


def getNewGuildTournamentRegionServerHostId():
    from data import region_server_config_data as RSCD
    return RSCD.data.get(getHostId(), {}).get('rankGTNRegionHostId', 0)


def getNewGuildTournamentRegionServerName():
    from data import region_server_config_data as RSCD
    regionData = RSCD.data.get(getNewGuildTournamentRegionServerHostId())
    if regionData:
        return regionData.get('serverName')


def getCrossGuildTournamentRegionId(groupId, hostId = 0):
    if BigWorld.component in ('base', 'cell'):
        hostId = hostId or int(gameconfig.getHostId())
    from data import region_server_config_data as RSCD
    regionData = RSCD.data.get(hostId)
    if not regionData:
        return 0
    regionIds = regionData.get('gtnRegionId')
    if not regionIds:
        return 0
    if groupId > len(regionIds):
        return 0
    return regionIds[groupId - 1]


def isWorldWarRegionServer():
    from data import world_war_region_data as WWRD
    hostId = getHostId()
    return WWRD.data.has_key(hostId)


def getWorldWarRegionServerHostId(hostId = 0):
    from data import region_server_config_data as RSCD
    hostId = hostId or getHostId()
    return RSCD.data.get(hostId, {}).get('wwRegionHostId', 0)


def getWorldWarRegionServerName():
    from data import region_server_config_data as RSCD
    regionData = RSCD.data.get(getWorldWarRegionServerHostId())
    if regionData:
        return regionData.get('serverName')


def getWorldWarSpaceNo():
    if BigWorld.component == 'cell' or BigWorld.component == 'base':
        if gameconfig.enableWorldWarNewMap():
            return const.SPACE_NO_WORLD_WAR_NEW
        else:
            return const.SPACE_NO_WORLD_WAR
    else:
        if gameglobal.rds.configData.get('enableWorldWarNewMap', False):
            return const.SPACE_NO_WORLD_WAR_NEW
        return const.SPACE_NO_WORLD_WAR


def getProfileIconSuffix():
    enablePNGProfileIcon = gameglobal.rds.configData.get('enablePNGProfileIcon', False)
    if enablePNGProfileIcon:
        return '.png'
    return '.dds'


def getServerProgressRegionServerHostId(hostId = 0):
    """
    \xe8\x8e\xb7\xe5\x8f\x96\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xe4\xba\x8b\xe4\xbb\xb6\xe8\xb7\xa8\xe6\x9c\x8d\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8hostId
    Args:
        hostId: \xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8hostId\xef\xbc\x8c\xe9\xbb\x98\xe8\xae\xa4\xe4\xb8\xba0\xef\xbc\x8c\xe5\x8d\xb3\xe6\x9c\xac\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8hostId
    
    Returns:
        \xe5\xaf\xb9\xe5\xba\x94\xe7\x9a\x84\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8\xe4\xba\x8b\xe4\xbb\xb6\xe8\xb7\xa8\xe6\x9c\x8d\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x99\xa8hostId
    """
    from data import region_server_config_data as RSCD
    hostId = hostId or getHostId()
    return RSCD.data.get(hostId, {}).get('spRegionHostId', 0)


def getCrossServerGlobalDataRegionHostId(hostId = 0):
    from data import region_server_config_data as RSCD
    hostId = hostId or getHostId()
    return RSCD.data.get(hostId, {}).get('csgdRegionHostId', 0)


def getHallOfFameRegionHostId(hostId = 0):
    from data import region_server_config_data as RSCD
    hostId = hostId or getHostId()
    return RSCD.data.get(hostId, {}).get('hofRegionHostId', 0)


def getDoubleArenaRegionHostId(hostId = 0):
    from data import region_server_config_data as RSCD
    hostId = hostId or getHostId()
    return RSCD.data.get(hostId, {}).get('daRegionHostId', 0)


def enableArenaPlayoffsQuickReady():
    if BigWorld.component == 'cell' or BigWorld.component == 'base':
        if gameconfig.enableArenaPlayoffsQuickReady():
            return True
        else:
            return False
    else:
        if gameglobal.rds.configData.get('enableArenaPlayoffsQuickReady', False):
            return True
        return False


def enableBindReward():
    if BigWorld.component == 'cell' or BigWorld.component == 'base':
        if gameconfig.enableBindReward():
            return True
        else:
            return False
    else:
        if gameglobal.rds.configData.get('enableBindReward', False):
            return True
        return False


def getInterfacesMethods(interface):
    path = 'entities/defs/interfaces/%s.def' % (interface,)
    sec = ResMgr.openSection(path)
    if BigWorld.component == 'cell':
        s = sec.openSection('CellMethods')
    elif BigWorld.component == 'base':
        s = sec.openSection('BaseMethods')
    elif BigWorld.component == 'client':
        s = sec.openSection('ClientMethods')
    m = []
    if s != None:
        m = s.values()
    implements = sec.openSection('Implements')
    if implements != None:
        for interface in implements.values():
            m += getInterfacesMethods(interface.asString)

    return m


def genGuildChallengeName(fbNo):
    from data import guild_challenge_data as GCLD
    gData = GCLD.data.get(fbNo, {})
    numLimit = gData.get('numLimit', 100)
    gName = gData.get('name', gameStrings.TEXT_UTILS_5731)
    fbName = '%dVS%d' % (numLimit / 2, numLimit / 2)
    return gName % fbName


def getInterfacesMembers(interface):
    path = 'entities/defs/interfaces/%s.def' % (interface,)
    sec = ResMgr.openSection(path)
    s = sec.openSection('Properties')
    cellMembers = []
    baseMembers = []
    m = []
    if s != None:
        m = s.values()
    for tagProp in m:
        indexOfType = [ k for k, n in enumerate(tagProp.values()) if n.name == 'Flags' ][0]
        flag = tagProp.values()[indexOfType].asString
        if flag in ('CELL', 'ALL_CLIENTS', 'ALL_CLIENT', 'OWN_CLIENT', 'OTHER_CLIENTS', 'CELL_PRIVATE', 'CELL_PUBLIC', 'CELL_PUBLIC_AND_OWN'):
            cellMembers.append(tagProp.name)
        if flag in ('BASE', 'BASE_AND_CLIENT'):
            baseMembers.append(tagProp.name)

    implements = sec.openSection('Implements')
    if implements != None:
        for interface in implements.values():
            cells, bases = getInterfacesMembers(interface.asString)
            cellMembers += cells
            baseMembers += bases

    return (cellMembers, baseMembers)


def getEntityMembers(entName):
    path = 'entities/defs/%s.def' % (entName,)
    sec = ResMgr.openSection(path)
    s = sec.openSection('Properties')
    cellMembers = []
    baseMembers = []
    m = []
    if s != None:
        m = s.values()
    for tagProp in m:
        indexOfType = [ k for k, n in enumerate(tagProp.values()) if n.name == 'Flags' ][0]
        flag = tagProp.values()[indexOfType].asString
        if flag in ('CELL', 'ALL_CLIENTS', 'ALL_CLIENT', 'OWN_CLIENT', 'OTHER_CLIENTS', 'CELL_PRIVATE', 'CELL_PUBLIC', 'CELL_PUBLIC_AND_OWN'):
            cellMembers.append(tagProp.name)
        if flag in ('BASE', 'BASE_AND_CLIENT'):
            baseMembers.append(tagProp.name)

    implements = sec.openSection('Implements')
    if implements != None:
        for interface in implements.values():
            cells, bases = getInterfacesMembers(interface.asString)
            cellMembers += cells
            baseMembers += bases

    return (set(cellMembers), set(baseMembers))


def getEntityMethods(entName):
    path = 'entities/defs/%s.def' % (entName,)
    sec = ResMgr.openSection(path)
    if BigWorld.component == 'cell':
        s = sec.openSection('CellMethods')
    elif BigWorld.component == 'base':
        s = sec.openSection('BaseMethods')
    elif BigWorld.component == 'client':
        s = sec.openSection('ClientMethods')
    m = []
    if s != None:
        m = s.values()
    implements = sec.openSection('Implements')
    if implements != None:
        for interface in implements.values():
            m += getInterfacesMethods(interface.asString)

    return m


def checkInCorrectServer(cId):
    from cdata import server_config_data as SCD
    if BigWorld.component in ('base', 'cell'):
        serverHost = gameconfig.getHostId()
    elif BigWorld.component == 'client':
        serverHost = gameglobal.rds.g_serverid
    else:
        return False
    serverData = SCD.data.get(cId, {})
    if serverData:
        if serverData.get('include', ()) and serverData.get('exclude', ()):
            if serverHost in serverData['include']:
                return True
            elif serverHost in serverData['exclude']:
                return False
            else:
                return True
        elif serverData.get('include', ()) and not serverData.get('exclude', ()):
            if serverHost in serverData['include']:
                return True
            else:
                return False
        elif not serverData.get('include', ()) and serverData.get('exclude', ()):
            if serverHost in serverData['exclude']:
                return False
            else:
                return True
        else:
            return True
    else:
        if BigWorld.component in ('base', 'cell'):
            reportWarning('checkInCorrectServer: %d not in server_config_data' % cId)
        return False


def getEnableCheckServerConfig():
    enableCheckServerConfig = False
    if BigWorld.component == 'client':
        import gameglobal
        enableCheckServerConfig = gameglobal.rds.configData.get('enableCheckServerConfig', False)
    else:
        enableCheckServerConfig = gameconfig.enableCheckServerConfig()
    return enableCheckServerConfig


def rgb2hex(rgbcolor):
    if not rgbcolor:
        return 0
    r, g, b = rgbcolor
    return (int(r) << 16) + (int(g) << 8) + int(b)


def transformGuidIntoBytes(guid):
    serverId = int(guid[:guid.index('-')])
    uid = guid[guid.index('-') + 1:]
    return transformUUID(serverId, uuid.UUID(uid).bytes)


def transformUUID(serverId, bytes):
    high = serverId >> 8 & 255
    low = serverId & 255
    return chr(high) + chr(low) + bytes[6:8] + bytes[4:6] + bytes[:4] + bytes[8:]


def transfromFromUUID(bytes):
    high = ord(bytes[0])
    low = ord(bytes[1])
    bytes = bytes[2:]
    return str((high << 8) + low) + '-' + str(uuid.UUID(bytes=bytes[4:8] + bytes[2:4] + bytes[:2] + bytes[8:]))


def extractTimeFromUUID(uid):
    hex_str = uid[15:18] + uid[9:13] + uid[0:8]
    dec_num = int(hex_str, 16)
    seconds = dec_num / 10 / 1000 / 1000
    timestamp = seconds - 12219292800L
    x = time.localtime(timestamp)
    localtime = time.strftime('%Y-%m-%d %H:%M:%S', x)
    return localtime


def findByUnicode(s, v, vIsGBK = True):
    s = unicode(s, defaultEncoding())
    if vIsGBK:
        return s.find(unicode(v, defaultEncoding()))
    else:
        return s.find(v)


def _getUUIDFromGUID(guid):
    try:
        return uuid.UUID(guid[len(guid) - 36:])
    except:
        return uuid.UUID(guid)


def cmpItemAndGUID(item, guid):
    return item.uuid == _getUUIDFromGUID(guid).bytes


validVerifyCodeChar = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'

def genVerifyCode(length):
    return ''.join([ random.choice(validVerifyCodeChar) for x in xrange(length) ])


def getCanonicalCrossServerRoleName(serverName, roleName):
    return serverName + ':' + roleName


def parseCanonicalCrossServerRoleName(name):
    return name.split(':', 1)


def isBaseMailBox(ent):
    return type(ent).__name__ in ('BaseViaCellMailBox', 'BaseEntityMailBox')


def isCellMailBox(ent):
    return type(ent).__name__ in ('CellEntityMailBox', 'CellViaBaseMailBox')


def isServerMailBox(ent):
    return isBaseMailBox(ent) or isCellMailBox(ent)


def isGlobalMailBox(ent):
    return type(ent).__name__ == 'GlobalMailBox'


def getMigrateServerName(hostId):
    from cdata import migrate_server_data as MSD
    return MSD.data.get(hostId, {}).get('serverName', '')


def canMigrateOut(hostId):
    from cdata import migrate_server_data as MSD
    return MSD.data.get(hostId, {}).get('migrateOut', 0)


def canMigrateIn(hostId):
    from cdata import migrate_server_data as MSD
    return MSD.data.get(hostId, {}).get('migrateIn', 0)


def canMigrate(fromServer, toServer):
    from cdata import migrate_server_data as MSD
    fromData = MSD.data.get(fromServer, {})
    toData = MSD.data.get(toServer, {})
    if not fromData or not toData:
        return False
    if not fromData.get('migrateOut', 0):
        return False
    if not toData.get('migrateIn', 0):
        return False
    if toServer in fromData.get('mutex', ()):
        return False
    from cdata import migrate_server_group_data as MSGD
    mGroup = fromData.get('group', 0)
    gData = MSGD.data.get(mGroup, {})
    if not gData:
        return False
    if toServer not in gData['group']:
        return False
    return True


def calcFixedTimeStr(cronStr):
    if not gameconfigCommon.enableCheckCrontabStrIsFixedTimeStamp():
        return 0
    weeksIndex = 4
    token = cronStr.split(' ')
    if len(token) == 6:
        token.pop(weeksIndex)
    elif len(token) == 5:
        token.pop(weeksIndex)
        token.append(str(getYearInt()))
    else:
        return 0
    for field in token:
        if field == '*':
            return 0

    timestamp = time.mktime(time.strptime('.'.join(token), '%M.%H.%d.%m.%Y'))
    return int(timestamp)


def getDisposableCronTabTimeStamp(startCronStr, now = None):
    t = calcFixedTimeStr(startCronStr)
    if t:
        return t
    else:
        now = now or getNow()
        if enableCronStr2List():
            cronList = parseCrontabStr2List(startCronStr)
            nextOffset = nextByTimeTuple(cronList, now)
            if nextOffset != sys.maxint:
                return int(now + nextOffset)
            prevOffset = prevByTimeTuple(cronList, now)
            return now + prevOffset
        startCron = CronTab(startCronStr)
        nextOffset = startCron.next(now)
        if nextOffset:
            return int(now + nextOffset)
        prevOffset = startCron.previous(now)
        if not prevOffset:
            prevOffset = 0
        return int(prevOffset + now)


def isInBusinessZaiju(ent):
    if not hasattr(ent, '_getZaijuNo'):
        return False
    zaijuNo = ent._getZaijuNo()
    return isBussinessZaiju(zaijuNo)


def isBussinessZaiju(zaijuNo):
    zjd = ZJD.data.get(zaijuNo, {})
    return zjd.has_key('bagSlotCount') and zjd.has_key('bagWidth') and zjd.has_key('bagHeight')


ITEM_CONBINE_FLAG_NO_SELL = 0
ITEM_CONBINE_FLAG_NO_TRADE = 1
ITEM_CONBINE_FLAG_NO_DROP = 2
ITEM_CONBINE_FLAG_NO_MAIL = 3
ITEM_CONBINE_FLAG_NO_CONSIGN = 4
ITEM_CONBINE_FLAG_NOT_SHOW_CONSIGN = 5
ITEM_CONBINE_FLAG_COIN_CONSIGN = 6
ITEM_CONBINE_FLAG_NO_BOOTH = 7
ITEM_CONBINE_FLAG_NO_BOOTH_BUY = 8
ITEM_CONBINE_FLAG_NO_STORAGE = 9
ITEM_CONBINE_FLAG_NO_REPAIRE = 10
ITEM_CONBINE_FLAG_NO_LATCH = 11
ITEM_CONBINE_FLAG_NO_RETURN = 12
ITEM_CONBINE_FLAG_APPRENTICE_ONLY = 13
ITEM_CONBINE_FLAG_MENTOR_ONLY = 14
ITEM_CONBINE_FLAG_CROSS_CONSIGN = 15
ITEM_CAN_SELL = 0
ITEM_SELL_FORBIDDEN_ALL = 1
ITEM_SELL_FORBIDDEN_PRICE = 2
ITEM_SELL_FORBIDDEN_FAME_PRICE = 3

def getBitDword(x, index):
    return x & 1 << index != 0


def getItemNoSell(data):
    return data.get('noSellType')


def getItemNoSellForPrice(data):
    return data.get('noSellType') in (ITEM_SELL_FORBIDDEN_ALL, ITEM_SELL_FORBIDDEN_PRICE)


def getItemNoSellForFamePrice(data):
    return data.get('noSellType') in (ITEM_SELL_FORBIDDEN_ALL, ITEM_SELL_FORBIDDEN_FAME_PRICE)


def getItemNoTrade(data):
    if data.has_key('itemFlags'):
        itemFlags = data.get('itemFlags', 0)
        return getBitDword(itemFlags, ITEM_CONBINE_FLAG_NO_TRADE)
    else:
        return data.get('noTrade', 0)


def getItemNoDrop(data):
    if data.has_key('itemFlags'):
        itemFlags = data.get('itemFlags', 0)
        return getBitDword(itemFlags, ITEM_CONBINE_FLAG_NO_DROP)
    else:
        return data.get('noDrop', 0)


def getItemNoMail(data):
    if data.has_key('itemFlags'):
        itemFlags = data.get('itemFlags', 0)
        return getBitDword(itemFlags, ITEM_CONBINE_FLAG_NO_MAIL)
    else:
        return data.get('noMail', 0)


def getItemNoConsign(data):
    if data.has_key('itemFlags'):
        itemFlags = data.get('itemFlags', 0)
        return getBitDword(itemFlags, ITEM_CONBINE_FLAG_NO_CONSIGN)
    else:
        return data.get('noConsign', 0)


def getItemNotShowConsign(data):
    if data.has_key('itemFlags'):
        itemFlags = data.get('itemFlags', 0)
        return getBitDword(itemFlags, ITEM_CONBINE_FLAG_NOT_SHOW_CONSIGN)
    else:
        return data.get('notShowConsign', 0)


def getItemCoinConsign(data):
    if data.has_key('itemFlags'):
        itemFlags = data.get('itemFlags', 0)
        return getBitDword(itemFlags, ITEM_CONBINE_FLAG_COIN_CONSIGN)
    else:
        return data.get('coinConsign', 0)


def getItemCrossConsign(data):
    if data.has_key('itemFlags'):
        itemFlags = data.get('itemFlags', 0)
        return getBitDword(itemFlags, ITEM_CONBINE_FLAG_CROSS_CONSIGN)
    else:
        return data.get('crossConsign', 0)


def getItemCoinPayMailLimit(data):
    return data.get('coinPayMailLimit', 0)


def getItemNoBooth(data):
    if data.has_key('itemFlags'):
        itemFlags = data.get('itemFlags', 0)
        return getBitDword(itemFlags, ITEM_CONBINE_FLAG_NO_BOOTH)
    else:
        return data.get('noBooth', 0)


def getItemNoBoothBuy(data):
    if data.has_key('itemFlags'):
        itemFlags = data.get('itemFlags', 0)
        return getBitDword(itemFlags, ITEM_CONBINE_FLAG_NO_BOOTH_BUY)
    else:
        return data.get('noBoothBuy', 0)


def getItemNoStorage(data):
    if data.has_key('itemFlags'):
        itemFlags = data.get('itemFlags', 0)
        return getBitDword(itemFlags, ITEM_CONBINE_FLAG_NO_STORAGE)
    else:
        return data.get('noStorage', 0)


def getItemNoRepair(data):
    if data.has_key('itemFlags'):
        itemFlags = data.get('itemFlags', 0)
        return getBitDword(itemFlags, ITEM_CONBINE_FLAG_NO_REPAIRE)
    else:
        return data.get('noRepair', 0)


def getItemNoLatch(data):
    if data.has_key('itemFlags'):
        itemFlags = data.get('itemFlags', 0)
        return getBitDword(itemFlags, ITEM_CONBINE_FLAG_NO_LATCH)
    else:
        return data.get('noLatch', 0)


def getItemNoReturn(data):
    if data.has_key('itemFlags'):
        itemFlags = data.get('itemFlags', 0)
        return getBitDword(itemFlags, ITEM_CONBINE_FLAG_NO_RETURN)
    else:
        return data.get('noReturn', 0)


def getItemApprenticeOnly(data):
    if data.has_key('itemFlags'):
        itemFlags = data.get('itemFlags', 0)
        return getBitDword(itemFlags, ITEM_CONBINE_FLAG_APPRENTICE_ONLY)
    else:
        return data.get('apprenticeOnly', 0)


def getItemMentorOnly(data):
    if data.has_key('itemFlags'):
        itemFlags = data.get('itemFlags', 0)
        return getBitDword(itemFlags, ITEM_CONBINE_FLAG_MENTOR_ONLY)
    else:
        return data.get('mentorOnly', 0)


def getItemName(itemId):
    from data import item_data as ID
    return ID.data.get(itemId, {}).get('name', '')


def getYearMonthDayInt(t = None):
    if t is None:
        t = getNow()
    lt = time.localtime(t)
    return int('%04d%02d%02d' % (lt[0], lt[1], lt[2]))


def extractYearMonthDayInt(monthDayInt):
    return (int(monthDayInt / 10000), int(monthDayInt % 10000 / 100), int(monthDayInt % 100))


def getVipGrade(avatar):
    if BigWorld.component == 'base':
        tCoin = avatar.account.ursChargeCoin
    else:
        tCoin = avatar.accountTotalCoin
    return calcVipGrade(tCoin)


def calcVipGrade(coin):
    money = int(coin / 10)
    vlist = [30000,
     10000,
     5000,
     3000,
     2000,
     1000,
     500,
     0]
    idx = 0
    for i, v in enumerate(vlist):
        if money >= v:
            idx = i
            break

    return len(vlist) - idx - 1


def shiftYearMonthDayInt(monthDayInt, days):
    year, month, day = extractYearMonthDayInt(monthDayInt)
    date = datetime.datetime(year, month, day)
    date += datetime.timedelta(days=days)
    lt = date.timetuple()
    return int('%04d%02d%02d' % (lt[0], lt[1], lt[2]))


def diffYearMonthDayInt(dayInt1, dayInt2):
    d1 = datetime.date(*extractYearMonthDayInt(dayInt1))
    d2 = datetime.date(*extractYearMonthDayInt(dayInt2))
    delta = d1 - d2
    return delta.days


itemLinkRegExp = re.compile('<a href=\"event:ret(\\d+)\">', re.IGNORECASE)

def extractCodeFromhyperlink(link):
    return [ int(x) for x in itemLinkRegExp.findall(link) if x.isdigit() ]


def isCipherBinding(owner):
    if BigWorld.component == 'cell':
        if not owner.cipherOfCell:
            return False
    elif BigWorld.component == 'client':
        if not owner.hasInvPassword:
            return False
    return True


def genNOSServiceMD5(content):
    current = getNow()
    serviceSalt = gameconfig.nosServiceSalt()
    plainText = serviceSalt + str(content) + str(current)
    myMd5 = hashlib.md5()
    myMd5.update(plainText)
    md5Text = myMd5.hexdigest()
    return (md5Text, current)


def getHostId():
    if BigWorld.component in ('base', 'cell'):
        return int(gameconfig.getHostId())
    if BigWorld.component in ('client',):
        return int(gameglobal.rds.g_serverid)


def getCurrHostId():
    if BigWorld.component in ('base', 'cell'):
        return int(gameconfig.getHostId())
    if BigWorld.component in ('client',):
        p = BigWorld.player()
        if p:
            if p._isSoul() or p._isReturn():
                return BigWorld.player().crossToHostId
            else:
                return int(gameglobal.rds.g_serverid)
        else:
            return int(gameglobal.rds.g_serverid)


def calcArenaPlayoffsBetRewardTotalCash(bType, bId, lastSeasonRestCash, lastDuelRestCash, betFailedCash, betSuccNum, lvKey):
    from data import arena_playoffs_bet_time_data as APBTD
    from data import arena_playoffs_5v5_bet_time_data as APBTD5
    from data import duel_config_data as DCD
    if lvKey in (gametypes.CROSS_ARENA_PLAYOFFS_5V5_LV_KEY_60_69, gametypes.CROSS_ARENA_PLAYOFFS_5V5_LV_KEY_70_79):
        PLAYOFFS_BET_TBL = APBTD5
    else:
        PLAYOFFS_BET_TBL = APBTD
    if not PLAYOFFS_BET_TBL.data.has_key((bType, bId)):
        if BigWorld.component in ('cell', 'base'):
            import gameengine
            gameengine.reportSevereCritical('warnning:_calcArenaPlayoffsBetRewardTotalCash failed:', bType, bId, lastSeasonRestCash, betFailedCash, betSuccNum, lvKey)
        return 0
    bData = PLAYOFFS_BET_TBL.data[bType, bId]
    cashOfsys = bData['cashOfsys']
    lastSeasonRestCashRatio = bData['lastSeasonRestCashRatio']
    ratio = DCD.data.get('ARENA_PLAYOFFS_USE_BET_FAILED_CASH_RATIO', 0.6)
    lastRatio = DCD.data.get('ARENA_PLAYOFFS_LAST_SEASON_REST_CASH_DUEL_BET_RATIO', 0.8)
    return int(lastSeasonRestCash * lastRatio * lastSeasonRestCashRatio + lastDuelRestCash + cashOfsys + betFailedCash * ratio)


def calcArenaPlayoffsBetRewardCash(bType, bId, lastSeasonRestCash, lastDuelRestCash, betFailedCash, betSuccNum, lvKey = None):
    total = calcArenaPlayoffsBetRewardTotalCash(bType, bId, lastSeasonRestCash, lastDuelRestCash, betFailedCash, betSuccNum, lvKey)
    return int(total / betSuccNum)


def calcArenaPlayoffsTopRewardCash(lvKey, rank, lastSeasonRestCash, betFailedAccumulateCash):
    from data import duel_config_data as DCD
    topCashOfSysDict = DCD.data.get('ARENA_PLAYOFFS_TOP_REWARD_CASH_FROM_SYS', {})
    lastRatio = DCD.data.get('ARENA_PLAYOFFS_LAST_SEASON_REST_CASH_DUEL_BET_RATIO', 0.8)
    rankRatioDict = DCD.data.get('ARENA_PLAYOFFS_TOP_REWARD_RATIO', {})
    total = topCashOfSysDict.get(lvKey, 1000) + (lastSeasonRestCash + betFailedAccumulateCash) * (1 - lastRatio)
    if not rankRatioDict.has_key(rank) and BigWorld.component in ('cell', 'base'):
        import gameengine
        gameengine.reportSevereCritical('calcArenaPlayoffsTopRewardCash warnning: rank not in data:', rank, rankRatioDict)
        return 0
    return int(total * rankRatioDict[rank])


def getLvLimit(avatar):
    import formula
    if not avatar:
        return const.PK_PROTECT_LV_LOWER_LIMIT
    if formula.getMLGNo(avatar.spaceNo) in const.ML_SPACE_NO_LINGZHU:
        lvLowerLimit = const.PK_PROTECT_LV_LOWER_LIMIT_IN_DIGONG
    else:
        lvLowerLimit = const.PK_PROTECT_LV_LOWER_LIMIT
    return lvLowerLimit


def getMLPvpReliveState(cnt):
    from cdata import ymf_relive_state_data as YRSD
    for numRange, stateData in YRSD.data.iteritems():
        if numRange[0] <= cnt <= numRange[1]:
            return (stateData['stateId'], 1, 0)

    return (0, 0, 0)


def getArenaSkillSchemeData(lv):
    from cdata import arena_skill_scheme_data as ASSD
    for lvRange, data in ASSD.data.iteritems():
        if lvRange[0] <= lv <= lvRange[1]:
            return data

    return {}


def getArenaSkillSchemeLvRange(lv):
    from cdata import arena_skill_scheme_data as ASSD
    for lvRange, data in ASSD.data.iteritems():
        if lvRange[0] <= lv <= lvRange[1]:
            return lvRange


def getWingWorldSkillSchemaData(groupId):
    from data import wing_world_skill_scheme_template_data as WWSSTD
    from data import wing_world_data as WWD
    modeId = WWD.data.get(groupId, {}).get('skillSchemeModeId', 0)
    return WWSSTD.data.get(modeId, {})


def getCrossBFSkillSchemaData(lv):
    from cdata import battle_field_skill_scheme_data as BFSSD
    for lvRange, data in BFSSD.data.iteritems():
        if lvRange[0] <= lv <= lvRange[1]:
            return data

    return {}


def getCrossBFSkillSchemaLvRange(lv):
    from cdata import battle_field_skill_scheme_data as BFSSD
    for lvRange, data in BFSSD.data.iteritems():
        if lvRange[0] <= lv <= lvRange[1]:
            return lvRange

    return (0, 0)


def pyStrToAsStr(str):
    strList = str.split('%s')
    retStr = strList[0]
    for i in xrange(len(strList) - 1):
        retStr += '{%d}' % i + strList[i + 1]

    return retStr


def randomAnswers(puzzleId):
    from data import puzzle_data as PD
    pd = PD.data[puzzleId]
    reduceCond = []
    initAnswer = pd.get('initAnswer', 4)
    aRandom = pd['aRandom']
    wrongAnswers = range(initAnswer)
    if pd.has_key('rightAnswer'):
        wrongAnswers.remove(pd['rightAnswer'])
    reduceAnswers = random.sample(wrongAnswers, len(reduceCond))
    answers = []
    for i in xrange(initAnswer):
        if i in reduceAnswers:
            answers.append((i, (1, reduceCond[reduceAnswers.index(i)])))
        else:
            answers.append((i, 0))

    if aRandom:
        random.shuffle(answers)
        return answers


def getStoryIdByMapId(fbNo):
    from cdata import story_fb_reverse_data as SFRD
    return SFRD.data.get(fbNo, {}).get('storyId', 0)


def parseCrossServerAccount(accountRole):
    return accountRole[:accountRole.rfind('@')]


def getDailyFameLimit(player, fameId):
    from data import fame_data as FD
    if BigWorld.component == 'client':
        fameLv = player.getFameLv(fameId)
    elif BigWorld.component == 'cell':
        fameLv = player.fame.getFameLv(fameId)
    purchaseLimit = FD.data.get(fameId, {}).get('purchaseLimit', {})
    if not purchaseLimit:
        return const.MAX_PURCHASE_LIMIT
    sum = 0
    for lv in xrange(fameLv):
        sum += purchaseLimit.get(lv + 1, 0)

    return sum


def getFameInitVal(fameId, school):
    from data import fame_data as FD
    fd = FD.data.get(fameId, None)
    if not fd:
        return 0
    else:
        schoolFame = fd.get('schoolFame', 0)
        if schoolFame:
            return fd.get('schoolInitVal', {}).get(school, 0)
        return fd.get('initVal', 0)


def genIntimacyEventKey(sec = None):
    return (getYearInt(sec), getMonthInt(sec), getMonthDayInt(sec))


def getDefaultWhere(className):
    if className in gametypes.BASE_ONLY_EVE_ENTTYPE:
        return 'base'
    else:
        return 'cell'


def getFashionAspectSlots(itemId):
    from data import equip_data as ED
    ed = ED.data.get(itemId, {})
    equipType = ed.get('equipType', 0)
    from item import Item
    if equipType == Item.EQUIP_BASETYPE_FASHION:
        from equipment import Equipment
        equipSType = ed.get('fashionSType', 0)
        mainPart = Item.EQUIP_PART_TABLE[equipType][equipSType][0]
        slotParts = ed.get('slotParts', [])
        parts = ed.get('parts', [])
        autoParts = [ p for p in slotParts if p not in parts ]
        autoParts = [ Equipment.FASHION_PARTS_MAP[i] for i in autoParts ]
        autoParts.append(mainPart)
        return autoParts
    return []


def getInteractiveObjectType(objectId):
    from data import interactive_data as ID
    return ID.data.get(objectId, {}).get('type', 0)


def getFashionEquipSlots(itemId):
    from data import equip_data as ED
    ed = ED.data.get(itemId, {})
    equipType = ed.get('equipType', 0)
    from item import Item
    if equipType == Item.EQUIP_BASETYPE_FASHION:
        from equipment import Equipment
        equipSType = ed.get('fashionSType', 0)
        mainPart = Item.EQUIP_PART_TABLE[equipType][equipSType][0]
        slotParts = ed.get('slotParts', [])
        slotParts = [ Equipment.FASHION_PARTS_MAP[i] for i in slotParts ]
        slotParts.append(mainPart)
        return slotParts
    return []


def crossServerAccount(accountRole):
    if BigWorld.component in ('base', 'cell'):
        hostId = gameconfig.getHostId()
    else:
        import gameglobal
        hostId = gameglobal.rds.g_serverid
    return accountRole + '@' + hostId


def getRealServerAccount(accountRole, hostId):
    suffix = '@%s' % hostId
    if suffix in accountRole:
        pos = accountRole.index(suffix)
        if len(accountRole) - pos == len(suffix):
            return accountRole[:pos]
    return accountRole


battleFieldRegionIDSet = set()

def getBattleFieldRegionIDSet():
    global battleFieldRegionIDSet
    if battleFieldRegionIDSet:
        return battleFieldRegionIDSet
    from cdata import battlefield_region_config_data as BRCD
    from cdata import new_battlefield_region_config_data as NBRCD
    for vData in (BRCD.data.itervalues(), NBRCD.data.itervalues()):
        for v in vData:
            for _, _, regionId in v.get('regionConfig', []):
                if regionId:
                    battleFieldRegionIDSet.add(regionId)

    return battleFieldRegionIDSet


def getBattleFieldRegionInfo(fbNo, needUpRegion = False, hostId = 0):
    from cdata import battlefield_region_config_data as BRCD
    from data import battle_field_data as BFD
    from cdata import new_battlefield_region_config_data as NBRCD
    if not hostId:
        hostId = getHostId()
    lvRange = BFD.data.get(fbNo, {}).get('lv')
    if (hostId, lvRange, fbNo) in NBRCD.data:
        regionConfigData = NBRCD.data.get((hostId, lvRange, fbNo))
    else:
        regionConfigData = BRCD.data.get((hostId, lvRange), {})
    if needUpRegion:
        upConfigData = regionConfigData.get('upRegionConfig')
        if not upConfigData or not hostId:
            return (0, 0, 0)
        serverProgressId, toHostId, regionId = upConfigData
        if BigWorld.component in ('base', 'cell'):
            import gameutils
            serverProgressFinished = gameutils.checkExistServerProgressCross(hostId, [serverProgressId])
        else:
            p = BigWorld.player()
            serverProgressFinished = p.inWorld and p.checkServerProgress(serverProgressId, False)
        if serverProgressFinished:
            return (serverProgressId, toHostId, regionId)
        else:
            return (0, 0, 0)
    configData = regionConfigData.get('regionConfig')
    if not configData:
        return (0, 0, 0)
    for serverProgressId, toHostId, regionId in reversed(configData):
        if BigWorld.component in ('base', 'cell'):
            import serverProgress
            serverProgressFinished = serverProgress.isMileStoneFinished(serverProgressId)
        else:
            p = BigWorld.player()
            serverProgressFinished = p.inWorld and p.isServerProgressFinished(serverProgressId)
        if serverProgressFinished:
            return (serverProgressId, toHostId, regionId)

    return (0, 0, 0)


def crossServerArenaEnabled(mode, lv):
    from cdata import cross_server_arena_config_data as CSACD
    configData = CSACD.data.get(getHostId(), {}).get('enableCrossServerArena')
    if not configData:
        return False
    for lvRange, serverProgressId in configData:
        if lvRange[0] <= lv <= lvRange[1]:
            if BigWorld.component in ('base', 'cell'):
                import serverProgress
                return serverProgress.isMileStoneFinished(serverProgressId)
            else:
                p = BigWorld.player()
                return p.inWorld and p.isServerProgressFinished(serverProgressId)

    return False


def isVipQueueMember(owner):
    if BigWorld.component == 'base':
        if not gameconfig.enableVipQueue():
            return False
    elif BigWorld.component == 'client':
        if not gameglobal.rds.configData.get('enableVipQueue', 0):
            return False
    if not owner or not hasattr(owner, 'prePayGbId'):
        return False
    return owner.prePayGbId > 0


def isCrossRoleName(name):
    return findByUnicode(name, '-') >= 0


def getRealRoleName(name):
    if isCrossRoleName(name):
        return parseRoleNameFromCrossName(name)
    else:
        return name


def parseRoleNameFromCrossName(globalName):
    if isCrossRoleName(globalName):
        return globalName[:globalName.rfind('-')]
    return globalName


def getRealServerName(name):
    if isCrossRoleName(name):
        return parseServerNameFromCrossName(name)
    else:
        return ''


def parseServerNameFromCrossName(globalName):
    if isCrossRoleName(globalName):
        return globalName[globalName.rfind('-') + 1:]
    return ''


def parseHostIdFromCrossName(globalName):
    if isCrossRoleName(globalName):
        from cdata import region_server_name_to_hostId as RSNTD
        return RSNTD.data.get(globalName[globalName.rfind('-') + 1:])
    return 0


def getHostIdFromServerName(serverName):
    from cdata import region_server_name_to_hostId as RSNTD
    return RSNTD.data.get(serverName, 0)


def getCurHostIdAfterServerMerge(hostId):
    from cdata import region_server_name_data as RSND
    return RSND.data.get(hostId, {}).get('currentHostId', 0)


def getNameWithHostIdStr(name, hostId):
    joinList = [name, str(hostId)]
    return '-'.join(joinList)


def getNameWithHostNameStr(name, hostId):
    joinList = [name, getServerName(hostId)]
    return '-'.join(joinList)


def getRoleNameFromNameWithHostIdStr(nameWithHostIdStr):
    return nameWithHostIdStr[:nameWithHostIdStr.rfind('-')]


def getHostIdFromNameWithHostIdStr(nameWithHostIdStr):
    if isCrossRoleName(nameWithHostIdStr):
        hostId = nameWithHostIdStr[nameWithHostIdStr.rfind('-') + 1:]
        if isInteger(hostId):
            return int(hostId)
    return 0


def fromSameServerByName(name1, name2):
    localServerName = getServerName()
    serverName1 = parseServerNameFromCrossName(name1) or localServerName
    serverName2 = parseServerNameFromCrossName(name2) or localServerName
    return serverName1 == serverName2


def getVPosByResKind(resKind, page, pos):
    if resKind == const.RES_KIND_INV:
        return (page, pos)
    if resKind == const.RES_KIND_CROSS_INV:
        return (const.CROSS_INV_VIRTUAL_PAGE_NO + page, pos)
    if resKind == const.RES_KIND_BATTLE_FIELD_BAG:
        return (const.BATTLE_FIELD_INV_VIRTUAL_PAGE_NO + page, pos)


def genWorldWarGroupGoalType(owner):
    goal = 0
    if owner.inWorldWar():
        if owner._isSoul():
            goal = const.GROUP_GOAL_WW_SOUL
        else:
            goal = const.GROUP_GOAL_WW_RAW
    elif owner.inWorldWarBattle():
        if owner._isSoul():
            goal = const.GROUP_GOAL_WW_BATTLE_SOUL
        else:
            goal = const.GROUP_GOAL_WW_BATTLE_RAW
    return goal


def genWorldWarOnlyGroupGoalType(owner):
    if owner.inWorldWar():
        if owner._isSoul():
            goal = const.GROUP_GOAL_WW_SOUL
        else:
            goal = const.GROUP_GOAL_WW_RAW
        return goal
    else:
        return 0


def weighted_choice(weights):
    if not weights:
        return None
    sumf = sum(weights)
    if sumf <= 0:
        return 0
    rnd = random.random() * sumf
    for i, w in enumerate(weights):
        rnd -= w
        if rnd < 0:
            return i


def getRealPos(owner, page, pos):
    if page >= const.CROSS_INV_VIRTUAL_PAGE_NO and page < const.BATTLE_FIELD_INV_VIRTUAL_PAGE_NO:
        return (owner.crossInv, page - const.CROSS_INV_VIRTUAL_PAGE_NO, pos)
    if page >= const.BATTLE_FIELD_INV_VIRTUAL_PAGE_NO:
        return (owner.battleFieldBag, page - const.BATTLE_FIELD_INV_VIRTUAL_PAGE_NO, pos)
    return (owner.realInv, page, pos)


def calcCrontabNextEx(crontab, now = 0, weekSet = 0):
    now = now or getNow()
    baseTime = now
    for i in xrange(1, 100):
        delta = crontab.next(baseTime)
        if delta == None:
            break
        baseTime = delta + baseTime
        if not isInvalidWeek(weekSet, baseTime):
            return baseTime - now

    return sys.maxint


def calcCrontabPreviousEx(crontab, now = 0, weekSet = 0):
    now = now or getNow()
    baseTime = now
    for i in xrange(1, 100):
        delta = crontab.previous(now=now + 60)
        if delta == None:
            break
        baseTime = baseTime + delta + 60
        if not isInvalidWeek(weekSet, baseTime):
            return now - baseTime

    return sys.maxint


def getTimeTuple(sec, tz = None):
    tz = tz or defaultTimezone()
    d = datetime.datetime.fromtimestamp(sec, tz)
    return d.timetuple()


def isInvalidWeek(weekSet, t = 0):
    from cdata import activity_loop_data as ALD
    if not t:
        t = getNow()
    loopData = ALD.data.get(weekSet, None)
    if not loopData:
        return False
    weekType = loopData.get('type')
    startDay = loopData.get('startDay', '')
    step = loopData.get('step', 1)
    num = loopData.get('num', 0)
    if weekType == const.ACT_LOOP_TYPE_MONTH:
        baseTime = getMonthSecond(t)
        tplSec = getTimeTuple(t)
        tplSec1 = getTimeTuple(baseTime)
        if tplSec[6] < tplSec1[6]:
            num += 1
    else:
        s = startDay.split('.')
        if len(s) > 6:
            return False
        for i in range(len(s), 6):
            startDay += '.0'

        baseTime = getTimeSecondFromStr(startDay, tz=defaultTimezone())
    return not isNthWeek(baseTime, step, num, t)


def checkPlayRecommWeekInValid(recommId):
    from data import play_recomm_item_data as PRID
    rData = PRID.data.get(recommId, None)
    if rData is None:
        return True
    weekSet = rData.get('weekSet', -1)
    if weekSet == -1:
        return False
    return isInvalidWeek(weekSet)


def getRedPacketRichText(sn, pType, msg, roleName, money, cnt, photo, time):
    from data import sys_config_data as SCD
    splitStr = SCD.data.get('redPacketSplit', const.RED_PACKET_SPLIT)
    return '[redpacket%s]' % splitStr.join((str(sn),
     str(pType),
     str(msg),
     photo,
     roleName,
     str(money),
     str(cnt),
     str(time)))


def isGroupMatchLvLimitAct(itemId):
    from data import activity_basic_data as ABD
    groupMatchLvs = ABD.data.get(itemId, {}).get('groupMatchLvs', ())
    if len(groupMatchLvs) == 0:
        return False
    else:
        return True


def parsePacketRichText(msg):
    from data import sys_config_data as SCD
    splitStr = SCD.data.get('redPacketSplit', const.RED_PACKET_SPLIT)
    try:
        sn, pType, msg, photo, roleName, money, cnt, time = msg.split(splitStr)
    except:
        try:
            msg = unicode(msg, defaultEncoding())
            sc = unicode(splitStr, defaultEncoding())
            sn, pType, msg, photo, roleName, money, cnt, time = msg.split(sc)
            return (sn.encode(defaultEncoding()),
             int(pType.encode(defaultEncoding())),
             msg.encode(defaultEncoding()),
             photo.encode(defaultEncoding()),
             roleName.encode(defaultEncoding()),
             int(money.encode(defaultEncoding())),
             int(cnt.encode(defaultEncoding())),
             int(time.encode(defaultEncoding())))
        except:
            sn, pType, msg, photo, roleName, money, cnt, time = ('', 0, '', '', '', 0, 0, 0)

    return (sn,
     int(pType),
     msg,
     photo,
     roleName,
     int(money),
     int(cnt),
     int(time))


def isRedPacket(msg):
    if msg:
        if re.search('\\[redPacket.*?\\]', msg, re.DOTALL | re.IGNORECASE | re.VERBOSE):
            return True
    return False


def getWWItemCommiteRewardRate(owner, lastScore, enemyLastScore):
    from data import item_commit_config_data as ICCD
    if enemyLastScore == 0:
        scoreRate = 1
    else:
        scoreRate = float(lastScore) / float(enemyLastScore)
    if owner._isSoul() and BigWorld.component in ('base', 'cell'):
        if lastScore == 0:
            scoreRate = 1.0
        else:
            scoreRate = 1.0 / scoreRate
    tmpRewardRate = 1
    for minRate, maxRate, rewardRate in ICCD.data['rewardRates']:
        if minRate <= scoreRate < maxRate:
            tmpRewardRate = rewardRate
            break

    return tmpRewardRate


def getTimeZone():
    offset = time.timezone if time.localtime().tm_isdst == 0 else time.altzone
    return offset / 60 / 60 * -1


def getInfoFromTMD(itemId, key = 'color', default = None):
    from cdata import tuzhuang_material_data as TMD
    return TMD.data.get(itemId, {}).get(key, default)


def setPartTuZhuangDyeList(dyeListDict, channel, part, value):
    values = dyeListDict.get(channel, [])
    if len(values) > part:
        values[part] = str(value)
    else:
        values += const.DEFAULT_TZ_PART_DYES[len(values):part]
        values.append(str(value))


def getTuZhuangDyeListInfo(dyeList):
    ret = {}
    for channel, indexs in const.TZ_CHANNEL_MAP.iteritems():
        ret[channel] = []

    if type(dyeList) is str:
        ret[const.DYE_CHANNEL_TEXTURE] = dyeList
        return ret
    ret[const.DYE_CHANNEL_TEXTURE] = 0
    for channel, indexs in const.TZ_CHANNEL_MAP.iteritems():
        if indexs:
            for index in indexs:
                if index - 1 < len(dyeList):
                    ret[channel].append(dyeList[index - 1])

    return ret


def createTuZhuangDyeList(oldDyeList, dyeArray):
    if not dyeArray:
        return oldDyeList
    if dyeArray[0][0] == const.DYE_CHANNEL_TEXTURE:
        tint = getInfoFromTMD(dyeArray[0][1][0], 'texture')
        if tint:
            return tint
    oldDyeListDict = getTuZhuangDyeListInfo(oldDyeList)
    for channel, dyeItems in dyeArray:
        if channel in (const.DYE_CHANNEL_1, const.DYE_CHANNEL_2, const.DYE_CHANNEL_3):
            colorId, caizhiId, gaoguangValue = dyeItems
            if colorId:
                color = getInfoFromTMD(colorId, 'color')
                setPartTuZhuangDyeList(oldDyeListDict, channel, 0, color)
            if caizhiId:
                material = getInfoFromTMD(caizhiId, 'material')
                setPartTuZhuangDyeList(oldDyeListDict, channel, 1, material)
            if gaoguangValue:
                setPartTuZhuangDyeList(oldDyeListDict, channel, 2, gaoguangValue)
        elif channel == const.DYE_CHANNEL_LIGHT:
            lightId = dyeItems[0]
            if lightId:
                light = getInfoFromTMD(lightId, 'light')
                setPartTuZhuangDyeList(oldDyeListDict, channel, 0, light)

    ret = []
    for channel in (const.DYE_CHANNEL_1, const.DYE_CHANNEL_2, const.DYE_CHANNEL_3):
        value = oldDyeListDict[channel]
        if len(value) < len(const.DEFAULT_TZ_PART_DYES):
            value += const.DEFAULT_TZ_PART_DYES[len(value):]
        ret += value

    if oldDyeListDict[const.DYE_CHANNEL_LIGHT] and oldDyeListDict[const.DYE_CHANNEL_LIGHT][0]:
        ret.append(oldDyeListDict[const.DYE_CHANNEL_LIGHT][0])
    return ret


def getFubenGuideLvs(owner, fbNo, validPlayerIds = []):
    from formula import calcFormulaById
    from data import fb_data as FD
    fd = FD.data[fbNo]
    if not fd.has_key('guideMode'):
        return (0, 0)
    guideMode = fd['guideMode']
    if guideMode == gametypes.FB_GUIDE_MODE_NORMAL:
        return (fd['guideLowLv'], fd['guideUpLv'])
    if guideMode == gametypes.FB_GUIDE_MODE_AVE_LV:
        guideLowLvFId = fd.get('guideLowLvFId', 0)
        guideUpLvFId = fd.get('guideUpLvFId', 0)
        guideLowLv = calcFormulaById(guideLowLvFId, {'mlLv': owner.fbAvgLv})
        guideUpLv = calcFormulaById(guideUpLvFId, {'mlLv': owner.fbAvgLv})
        return (guideLowLv, guideUpLv)
    if guideMode == gametypes.FB_GUIDE_MODE_RANK_DIFF and owner:
        isMinLevel = True
        from data import sys_config_data as SCD
        guideModeLevelDiff = SCD.data.get('guideModeLevelDiff', 1)
        lv = owner.lv
        if BigWorld.component == 'client':
            ownerMac = owner.members.get(owner.gbId, {}).get('macAddress', '')
            validLevels = [ pInfo.get('level') for gbId, pInfo in owner.members.iteritems() if owner.gbId != gbId and ownerMac != pInfo.get('macAddress', '') ]
        else:
            validLevels = [ x.level for x in owner.team.values() if x.box and x.box.id != owner.id and x.macAddress != owner.macAddress and x.box.id in validPlayerIds ]
        if not len(validLevels):
            return (lv - 1, lv + 1)
        else:
            for level in validLevels:
                if lv >= level + guideModeLevelDiff:
                    isMinLevel = False
                    break

            if isMinLevel:
                return (lv, lv + guideModeLevelDiff)
            return (lv - guideModeLevelDiff, lv)
    else:
        return (0, 0)


def isInRookie(owner, fbNo, teamers, isTeam = True):
    """
    \xe5\x89\xaf\xe6\x9c\xac\xe6\x8c\x87\xe5\xaf\xbc\xe5\xa2\x9e\xe5\x8a\xa0\xe6\xa8\xa1\xe5\xbc\x8f3\xe7\xad\x89\xe7\xba\xa7\xe5\xb7\xae\xe7\x9a\x84\xe5\x88\xa4\xe6\x96\xad\xef\xbc\x8c\xe7\x8e\xa9\xe5\xae\xb6\xe5\x8f\xaf\xe4\xbb\xa5\xe5\x90\x8c\xe6\x97\xb6\xe5\xb1\x9e\xe4\xba\x8e\xe6\x8c\x87\xe5\xaf\xbc\xe4\xb8\x8e\xe8\xa2\xab\xe6\x8c\x87\xe5\xaf\xbc\xe4\xb8\xa4\xe7\xa7\x8d\xe7\x8a\xb6\xe6\x80\x81\xef\xbc\x8c\xe5\xbd\x93\xe7\x8e\xa9\xe5\xae\xb6\xe5\xa4\x84\xe4\xba\x8e\xe6\x8c\x87\xe5\xaf\xbc\xe7\x8a\xb6\xe6\x80\x81\xe6\x97\xb6\xef\xbc\x8c\xe9\x9c\x80\xe8\xa6\x81\xe5\x88\xa4\xe6\x96\xad\xe5\x85\xb6\xe6\x98\xaf\xe5\x90\xa6\xe4\xb9\x9f\xe5\xa4\x84\xe4\xba\x8e\xe8\xa2\xab\xe6\x8c\x87\xe5\xaf\xbc\xe7\x8a\xb6\xe6\x80\x81
    \xe5\x90\x8c\xe6\x97\xb6\xe5\xa4\x84\xe4\xba\x8e\xe6\x8c\x87\xe5\xaf\xbc\xe4\xb8\x8e\xe8\xa2\xab\xe6\x8c\x87\xe5\xaf\xbc\xe7\x8a\xb6\xe6\x80\x81\xe6\x97\xb6\xef\xbc\x8c\xe7\xbb\x8f\xe9\xaa\x8c\xe5\x8a\xa0\xe6\x88\x90\xe7\xb3\xbb\xe6\x95\xb0\xe5\x8f\x962\xe7\xa7\x8d\xe7\x8a\xb6\xe6\x80\x81\xe4\xb8\xad\xe7\x9a\x84\xe6\x9c\x80\xe5\xa4\xa7\xe5\x80\xbc
    :param owner: \xe7\x8e\xa9\xe5\xae\xb6\xe8\x87\xaa\xe5\xb7\xb1
    :param fbNo:  \xe7\x8e\xa9\xe5\xae\xb6\xe6\x89\x80\xe5\x9c\xa8\xe5\x89\xaf\xe6\x9c\xac
    :param teamers: \xe7\x8e\xa9\xe5\xae\xb6\xe9\x98\x9f\xe4\xbc\x8d\xe6\x88\x90\xe5\x91\x98/\xe5\x87\xbb\xe6\x9d\x80\xe6\x80\xaa\xe7\x89\xa9\xe5\x91\xa8\xe5\x9b\xb4\xe6\x9c\x89\xe6\x95\x88\xe7\x8e\xa9\xe5\xae\xb6
    :param isTeam: \xe6\x98\xaf\xe5\x90\xa6\xe6\x98\xaf\xe9\x98\x9f\xe4\xbc\x8d\xe6\x88\x90\xe5\x91\x98
    :return: True\xe8\xa1\xa8\xe7\xa4\xba\xe7\x8e\xa9\xe5\xae\xb6\xe5\x90\x8c\xe6\x97\xb6\xe5\xa4\x84\xe4\xba\x8e\xe6\x8c\x87\xe5\xaf\xbc\xe4\xb8\x8e\xe8\xa2\xab\xe6\x8c\x87\xe5\xaf\xbc\xe7\x8a\xb6\xe6\x80\x81\xef\xbc\x8c\xe7\xbb\x8f\xe9\xaa\x8c\xe5\x8a\xa0\xe6\x88\x90\xe5\x8f\x96\xe4\xb8\xa4\xe7\xa7\x8d\xe7\x8a\xb6\xe6\x80\x81\xe7\x9a\x84\xe6\x9c\x80\xe5\xa4\xa7\xe5\x80\xbc\xef\xbc\x9b False\xef\xbc\x9a\xe7\x8e\xa9\xe5\xae\xb6\xe4\xbb\x85\xe5\xa4\x84\xe4\xba\x8e\xe6\x8c\x87\xe5\xaf\xbc\xe7\x8a\xb6\xe6\x80\x81\xef\xbc\x8c\xe5\x8e\xbb\xe6\x8c\x87\xe5\xaf\xbc\xe7\x8a\xb6\xe6\x80\x81\xe4\xb8\x8b\xe7\x9a\x84\xe7\xbb\x8f\xe9\xaa\x8c\xe5\x8a\xa0\xe6\x88\x90
    """
    if not owner:
        return False
    from data import fb_data as FD
    fd = FD.data.get(fbNo, None)
    if not fd:
        return False
    if not fd.has_key('guideMode'):
        return False
    guideMode = fd['guideMode']
    if guideMode == gametypes.FB_GUIDE_MODE_RANK_DIFF:
        from data import sys_config_data as SCD
        guideModeLevelDiff = SCD.data.get('guideModeLevelDiff', 1)
        lv = owner.lv
        if not isTeam:
            team = [ x for x in teamers if x.macAddress != owner.macAddress and x.id != owner.id ]
        else:
            team = [ x for x in teamers if x.box and x.box.id != owner.id and x.macAddress != owner.macAddress and x.spaceNo == owner.spaceNo ]
        if not len(team):
            return False
        for mate in team:
            if isTeam:
                if lv + guideModeLevelDiff <= mate.level:
                    return True
            elif lv + guideModeLevelDiff <= mate.lv:
                return True

        return False


def getServerDaySecond(sec = None, isServerTime = False):
    if not sec:
        sec = getNow()
        isServerTime = True
    tplSec = time.localtime(sec)
    if isServerTime and BigWorld.component == 'client':
        hours = tplSec[3] - (getTimeZone() - gameglobal.SERVER_TIME_ZONE)
        diff = hours % 24 * 3600 + tplSec[4] * 60 + tplSec[5]
    else:
        diff = tplSec[3] * 60 * 60 + tplSec[4] * 60 + tplSec[5]
    return sec - diff


def calcDaysAfterEnterWorld(owner):
    nowDaySec = getServerDaySecond(getNow(), True)
    cnt = int(round((nowDaySec - getServerDaySecond(owner.enterWorldTime, True)) / 86400.0))
    if nowDaySec != getNow():
        cnt += 1
    return max(0, cnt)


def encodeMsgHeader(msg, properties):
    if not properties:
        return msg
    oldProperties, msg = decodeMsgHeader(msg)
    if oldProperties:
        properties.update(oldProperties)
    return '%s%s%s%s' % (const.CHAT_MSG_HEADER_SPLIT_START,
     str(properties),
     const.CHAT_MSG_HEADER_SPLIT_END,
     msg)


def decodeMsgHeader(msg):
    if msg and msg[0] == '$' and msg.find(const.CHAT_MSG_HEADER_SPLIT_START) == 0:
        end = msg.find(const.CHAT_MSG_HEADER_SPLIT_END)
        if end > 0:
            header = msg[len(const.CHAT_MSG_HEADER_SPLIT_START):end]
            if end < len(msg) - len(const.CHAT_MSG_HEADER_SPLIT_END):
                msg = msg[end + len(const.CHAT_MSG_HEADER_SPLIT_END):]
            else:
                msg = ''
            return (eval(header), msg)
        else:
            return (None, msg)
    else:
        return (None, msg)


def calcMakeManualMaterialDiKou(owner, itemDict):
    from cdata import equip_make_manual_dikou_data as EMMDD
    gamelog.debug('@ct calcMakeManualMaterialDiKou start', itemDict)
    totalYunChui = 0
    totalCoin = 0
    itemConsumeDict = {}
    enableManualDiKou = False
    if BigWorld.component == 'client':
        import gameglobal
        enableManualDiKou = gameglobal.rds.configData.get('enableManualDiKou', False)
    else:
        enableManualDiKou = gameconfig.enableManualDiKou()
    if not enableManualDiKou:
        for itemId, itemInfo in itemDict.iteritems():
            if owner.inv.countItemInPages(itemId, enableParentCheck=True) < itemInfo['itemNum']:
                return (False,
                 0,
                 0,
                 {})

        return (True,
         0,
         0,
         itemDict)
    for itemId, itemInfo in itemDict.iteritems():
        invCnt = owner.inv.countItemInPages(itemId, enableParentCheck=True)
        if invCnt < itemInfo['itemNum']:
            delta = itemInfo['itemNum'] - invCnt
            dkData = EMMDD.data.get(itemId)
            if not dkData:
                return (False,
                 0,
                 0,
                 {})
            totalYunChui += dkData.get('yunChuiScore', 0) * delta
            totalCoin += dkData.get('coin', 0) * delta
        itemConsumeDict[itemId] = {'itemNum': min(invCnt, itemInfo['itemNum']),
         'enableParentCheck': itemInfo['enableParentCheck'],
         'bindingType': itemInfo['bindingType']}

    return (True,
     totalYunChui,
     totalCoin,
     itemConsumeDict)


def calcEquipMaterialDiKou(owner, itemDict):
    from cdata import equip_transform_dikou_data as ETDD
    totalYunChui = 0
    totalCoin = 0
    itemConsumeDict = {}
    enableEquipDiKou = False
    if BigWorld.component == 'client':
        import gameglobal
        enableEquipDiKou = gameglobal.rds.configData.get('enableEquipDiKou', False)
    else:
        enableEquipDiKou = gameconfig.enableEquipDiKou()
    if not enableEquipDiKou:
        for itemId, itemNum in itemDict.iteritems():
            if owner.inv.countItemInPages(itemId, enableParentCheck=True) < itemNum:
                return (False,
                 0,
                 0,
                 {})

        return (True,
         0,
         0,
         itemDict)
    owner.tempEquipDiKouItemID = 0
    for itemId, itemNum in itemDict.iteritems():
        invCnt = owner.inv.countItemInPages(itemId, enableParentCheck=True)
        if invCnt < itemNum:
            delta = itemNum - invCnt
            dkData = ETDD.data.get(itemId)
            if not dkData:
                return (False,
                 0,
                 0,
                 {})
            totalYunChui += dkData.get('yunChuiScore', 0) * delta
            totalCoin += dkData.get('coin', 0) * delta
            owner.tempEquipDiKouItemID = itemId
        itemConsumeDict[itemId] = min(invCnt, itemNum)

    return (True,
     totalYunChui,
     totalCoin,
     itemConsumeDict)


def isSchoolCaps(cap):
    return cap > 1 and cap < 10 or cap > 100


def isSchoolAndNormalCaps(cap):
    return cap >= 1 and cap < 10 or cap > 100


def calcEquipSoulUsedEnergy(spid, realNum, simulationNum):
    from cdata import equip_soul_consume_data as ESCD
    usedEnergy = 0
    for i in xrange(realNum + 1, realNum + simulationNum + 1):
        usedEnergy += ESCD.data.get((spid, i), {}).get('energyCon', 0)

    return usedEnergy


def getEquipSoulOffsetPos(x, y):
    offsetList = const.EQUIP_SOUL_POS_OFFSET_LIST1 if y % 2 else const.EQUIP_SOUL_POS_OFFSET_LIST2
    offsetPosList = [ (x + offset[0], y + offset[1]) for offset in offsetList ]
    return offsetPosList


def checkEquipSoulStoneCanActive(schreq, x, y, spid, totalList):
    from data import equip_soul_prop_data as ESPRD
    if ESPRD.data.get((schreq,
     x,
     y,
     spid), {}).get('firstStone', 0):
        return True
    offsetPosList = getEquipSoulOffsetPos(x, y)
    for offsetPos in offsetPosList:
        if offsetPos in totalList:
            return True

    return False


def getLifeSkillEquipIdsBySubType(owner, dstSubType):
    equipIds = []
    if dstSubType is None:
        return []
    for key, val in owner.lifeEquipment.iteritems():
        if not val:
            continue
        srcSubType, _ = key
        if srcSubType != dstSubType:
            continue
        if val.cdura == 0:
            continue
        equipIds.append(val.id)

    return equipIds


def calcLifeSkillEquipLvUps(equipIds):
    from data import life_skill_equip_data as LSEPD
    addLv = 0
    for eId in equipIds:
        addLv += LSEPD.data.get(eId, {}).get('lvUp', 0)

    return addLv


def inAllowBodyType(itemId, bodyType, ID = None):
    if not ID:
        from data import item_data as ID
    data = ID.data.get(itemId, {})
    allowBodyType = data.get('allowBodyType', 0)
    if allowBodyType:
        if isinstance(allowBodyType, int):
            allowBodyType = (allowBodyType,)
        if bodyType not in allowBodyType:
            return False
    return True


def inAllowSex(itemId, sex, ID = None):
    if not ID:
        from data import item_data as ID
    data = ID.data.get(itemId, {})
    sexReq = data.get('sexReq', 0)
    if sexReq:
        if isinstance(sexReq, int):
            sexReq = (sexReq,)
        if sex not in sexReq:
            return False
    return True


def getConfigVal(configName):
    if BigWorld.component == 'client':
        serverOpenTime = gameglobal.rds.configData.get(configName, 0)
    else:
        config = getattr(gameconfig, configName, None)
        if config:
            return config()
        return False


def getRefreshAvatarInfoInterval(owner):
    import formula
    if owner.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
        if BigWorld.component == 'client':
            battlefieldPosRefreshInterval = gameglobal.rds.configData.get('battlefieldPosRefreshInterval', const.REFRESH_AVATAR_INFO_BATTLEFIELD_INTERVAL)
        else:
            battlefieldPosRefreshInterval = gameconfig.battlefieldPosRefreshInterval()
        if formula.inPUBGSpace(owner.spaceNo):
            from data import duel_config_data as DCD
            battlefieldPosRefreshInterval = DCD.data.get('pubgTeammateRefreshInterval', battlefieldPosRefreshInterval)
            return battlefieldPosRefreshInterval
        elif battlefieldPosRefreshInterval < 1.0:
            return const.REFRESH_AVATAR_INFO_BATTLEFIELD_INTERVAL
        else:
            return battlefieldPosRefreshInterval
    else:
        return const.REFRESH_AVATAR_INFO_INTERVAL


def filtItemByConfig(data, getItem):
    from data import item_data as ID
    if type(data) in const.TYPE_TUPLE_AND_LIST:
        result = []
        for e in data:
            itemId = getItem(e)
            if not itemId:
                result.append(e)
                continue
            itemData = ID.data.get(itemId)
            if not itemData:
                continue
            configName = itemData.get('configName')
            if not configName:
                result.append(e)
                continue
            if getConfigVal(configName):
                result.append(e)

        return type(data)(result)
    if type(data) == dict:
        result = {}
        for k, v in data.iteritems():
            itemId = getItem(k, v)
            if not itemId:
                result[k] = v
                continue
            itemData = ID.data.get(itemId)
            if not itemData:
                continue
            configName = itemData.get('configName')
            if not configName:
                result[k] = v
                continue
            if getConfigVal(configName):
                result[k] = v

        return result
    if type(data) == int:
        itemId = data
        itemData = ID.data.get(itemId)
        if not itemData:
            return 0
        configName = itemData.get('configName')
        if not configName:
            return data
        if getConfigVal(configName):
            return data
        return 0


def adjustDir(yaw):
    if yaw > math.pi:
        yaw = yaw - 2 * math.pi
    if yaw < -math.pi:
        yaw = yaw + 2 * math.pi
    return yaw


def randomYaw():
    return random.randint(int(-math.pi * 100), int(math.pi * 100)) / 100.0


def defaultEncoding():
    from BWAutoImport import DEFAULT_ENCODING
    return DEFAULT_ENCODING


def getFurnitureName(itemId):
    from data import item_furniture_data as IFD
    return IFD.data.get(itemId, {}).get('name', '')


def getModelShareLinkMsg(roleName, nuid, furnitureName):
    return gameStrings.TEXT_UTILS_7323 % (roleName, nuid, furnitureName)


def isInternationalVersion():
    from gamestrings import DEFAULT_LANGUAGE
    return serverLanguage() != DEFAULT_LANGUAGE


def getGameLanuage():
    from gamestrings import serverLanguage
    return serverLanguage()


def getCrossServerActivityTimeZone():
    if serverLanguage() in ('en',):
        from data import sys_config_data as SCD
        if SCD.data.get('crossServerActivityTimeZone'):
            return timezone(SCD.data['crossServerActivityTimeZone'])
    return defaultTimezone()


def roundInt(n):
    return math.floor(n + 0.5)


def isNormalAttack(skillInfo):
    return skillInfo.getSkillData('skillCategory') == const.SKILL_CATEGORY_BF_DOTA_NORMAL


def isTalentSkill(skillId):
    from data import duel_config_data as DCD
    allTalentSkillIdList = DCD.data.get('BATTLE_FIELD_DOTA_TALENT_SKILL_LIST', [])
    if skillId in allTalentSkillIdList:
        return True
    return False


def isCDStorageSkill(skillId, levle):
    from data import skill_general_data as SGD
    return SGD.data.get((skillId, levle), {}).get('cdstorage', 0) > 0


def isDotaBfOpen():
    enableDotaBf = False
    if BigWorld.component == 'client':
        import gameglobal
        enableDotaBf = gameglobal.rds.configData.get('enableDotaBf', False)
    else:
        enableDotaBf = gameconfig.enableDotaBf()
    return bool(enableDotaBf)


def getTalentSkillByIndex(index):
    from data import duel_config_data as DCD
    skillList = DCD.data.get('BATTLE_FIELD_DOTA_TALENT_SKILL_LIST', [])
    if index >= len(skillList):
        raise Exception('@jbx: talentSkill index error', index, skillList)
    return (skillList[index], 1)


def getAmmoMsgID(school):
    from cdata import game_msg_def_data as GMDD
    if school == const.SCHOOL_YUXU:
        return GMDD.data.SKILL_FORBIDDEN_NO_YUAN_LING
    if school == const.SCHOOL_YECHA:
        return GMDD.data.SKILL_FORBIDDEN_NO_XUE_DU
    return 0


def getRealRideId(item):
    if getattr(item, 'realDyeId', None):
        return item.realDyeId
    return item.id


def getRealWingId(item):
    if getattr(item, 'realDyeId', None):
        return item.realDyeId
    return item.id


def needShowScopeDebug(src, viewType):
    """
    \xe6\x98\xaf\xe5\x90\xa6\xe5\x85\x81\xe8\xae\xb8\xe6\x98\xbe\xe7\xa4\xba\xe6\xa1\x86\xe7\xba\xbf
    1. \xe6\x8a\x80\xe8\x83\xbd\xe7\xbb\x93\xe7\xae\x97\xe5\x8f\xaf\xe5\x9c\xa8client\xe3\x80\x81base\xe3\x80\x81cell\xe4\xb8\x8a\xe8\xbf\x90\xe8\xa1\x8c
    2. \xe5\x85\xb6\xe4\xbb\x96\xe5\x9d\x87\xe5\x8f\xaa\xe8\x83\xbd\xe5\x9c\xa8base\xe3\x80\x81cell\xe4\xb8\x8a\xe8\xbf\x90\xe8\xa1\x8c
    :param src:
    :param viewType: \xe7\xb1\xbb\xe5\x9e\x8b(\xe8\xae\xa1\xe7\xae\x97\xe8\x8c\x83\xe5\x9b\xb4\xe6\xa1\x86\xe7\xba\xbf:1, \xe6\x80\xaa\xe7\x89\xa9\xe8\xa7\x86\xe9\x87\x8e:2, \xe6\x80\xaa\xe7\x89\xa9\xe5\xb7\xa1\xe9\x80\xbb\xe8\x8c\x83\xe5\x9b\xb4:3, \xe6\x80\xaa\xe7\x89\xa9\xe8\xbf\xbd\xe5\x87\xbb\xe8\x8c\x83\xe5\x9b\xb4:4,\xe9\x99\xb7\xe8\xbf\x9b\xe8\xa7\xa6\xe5\x8f\x91\xe8\x8c\x83\xe5\x9b\xb4:5)
    :return:
    """
    if BigWorld.component == 'client':
        publicServer = gameglobal.rds.configData.get('publicServer', False)
        showScopeViewIds = {}
        if hasattr(gameglobal.rds, 'showScopeViewIds'):
            showScopeViewIds = gameglobal.rds.showScopeViewIds
        if gametypes.NO_SHOW_SCOPE:
            return False
    else:
        publicServer = gameconfig.publicServer()
        showScopeViewIds = Netease.showScopeViewIds
    if publicServer:
        return False
    if viewType == gametypes.SCOPCE_TYPE_CALC_DEBUG:
        if gametypes.ENABLE_SHOW_GLOBAL_CALC_SCOPE:
            return True
    if src and viewType in showScopeViewIds.get(src.id, []):
        return True
    return False


def isValidGuildGroupId(groupId, subGroupId):
    if groupId not in gametypes.GUILD_TOURNAMENT_GROUP:
        return False
    if subGroupId not in gametypes.GUILD_TOURNAMENT_GUILD_SUBGROUP:
        return False
    if subGroupId and groupId != gametypes.GUILD_TOURNAMENT_GROUP_BH:
        return False
    return True


def getRealGtnGuildGroupId(groupId, subGroupId):
    groupId = gametypes.GUILD_TOURNAMENT_GUILD_GROUP_DATA.get(groupId, groupId)
    if groupId == gametypes.GUILD_TOURNAMENT_GUILD_GROUP_QL:
        return groupId
    elif subGroupId:
        return gametypes.GUILD_TOURNAMENT_GUILD_GROUP_BH_2
    else:
        return gametypes.GUILD_TOURNAMENT_GUILD_GROUP_BH


def decoratorStatic(method):

    def newStaticFunc(*args, **kws):
        keyWatcher = args[0]
        funcName = method.func_name
        if funcName == '__calcSkillEffectData':
            if not (_preCheckStaticDecorator(args[0].owner) or _preCheckStaticDecorator(args[1].owner)):
                return method(*args, **kws)
            keyWatcher = args[4]
        elif funcName == 'useSkill':
            if not (_preCheckStaticDecorator(args[0]) or _preCheckStaticDecorator(args[1])):
                return method(*args, **kws)
            keyWatcher = args[2].num
        else:
            return method(*args, **kws)
        startTime = time.time()
        returnSult = method(*args, **kws)
        endTime = time.time()
        gamelog.debug('@lhb skill decorator funcName = {0}, skillId = {1}, startTime = {2}, endTime = {3}'.format(method.func_name, keyWatcher, startTime, endTime))
        if funcName == 'useSkill':
            if keyWatcher not in Netease.skillUseWatch:
                Netease.skillUseWatch[keyWatcher] = []
            Netease.skillUseWatch[keyWatcher].append(endTime - startTime)
        elif funcName == '__calcSkillEffectData':
            if keyWatcher not in Netease.skillSpecialEffWatch:
                Netease.skillSpecialEffWatch[keyWatcher] = {}
            skillEffectId = args[2].num
            if skillEffectId not in Netease.skillSpecialEffWatch[keyWatcher]:
                Netease.skillSpecialEffWatch[keyWatcher][skillEffectId] = []
            Netease.skillSpecialEffWatch[keyWatcher][skillEffectId].append(endTime - startTime)
        return returnSult

    return newStaticFunc


def _preCheckStaticDecorator(obj):
    if not obj:
        return False
    if not obj.IsAvatar and not obj.IsAvatarRobot:
        return False
    return True


def decoratorNonStatic(method):

    def newNonStaticFunc(self, *args, **kws):
        print 'start'
        print 'Arg{0}'.format(args)
        print 'Kws{0}'.format(kws)
        returnSult = method(self, *args, **kws)
        print 'end'
        return returnSult

    return newNonStaticFunc


def getRedPacketChatChannel(pType, channel):
    if pType == const.RED_PACKET_TYPE_SNOWBALL:
        return const.CHAT_CHANNEL_GUILD
    if pType in (const.RED_PACKET_TYPE_COMMON, const.RED_PACKET_TYPE_LUCKY):
        if channel == const.CHAT_FRIEND:
            return const.CHAT_FRIEND
        elif channel == const.CHAT_CHANNEL_CLAN:
            return const.CHAT_CHANNEL_CLAN
        elif channel == const.CHAT_CHANNEL_TEAM:
            return const.CHAT_CHANNEL_TEAM
        elif channel == const.CHAT_CHANNEL_GROUP:
            return const.CHAT_CHANNEL_GROUP
        else:
            return const.CHAT_CHANNEL_GUILD
    elif pType in (const.RED_PACKET_TYPE_MARRIAGE_HALL_CASH, const.RED_PACKET_TYPE_MARRIAGE_HALL_COIN):
        return const.CHAT_CHANNEL_MARRIAGE_HALL
    return const.CHAT_CHANNEL_WORLD_EX


def flakes(input, **kw):
    PyCF_ONLY_AST = 1024
    import textwrap
    from pyflakes import checker
    tree = compile(textwrap.dedent(input), '<test>', 'exec', PyCF_ONLY_AST)
    w = checker.Checker(tree, **kw)
    return w


def checkFile(content):
    from pyflakes import reporter
    import StringIO
    from pyflakes.messages import UnusedImport, RedefinedWhileUnused
    warningStream = StringIO.StringIO()
    errorStream = StringIO.StringIO()
    report = reporter.Reporter(warningStream, errorStream)
    res = flakes(content)
    warnings = filter(lambda message: type(message) != UnusedImport and type(message) != RedefinedWhileUnused, res.messages)
    warnings.sort(key=lambda m: m.lineno)
    if not warnings:
        return
    for warning in warnings:
        report.flake(warning)

    warningContent = warningStream.getvalue()
    errorContent = errorStream.getvalue()
    ret = 'pyflakes check fail! quit. \n'
    if warningContent:
        ret += 'warnings: \n'
        ret += warningContent
        ret += '\n'
    if errorContent:
        ret += 'errors: \n'
        ret += errorContent
        ret += '\n'
    return ret


def checkRunscriptFileError():
    import os
    dir = 'entities/common_server'
    filename = os.path.join(dir, 'run_script.py')
    with open(filename, 'rb') as ff:
        content = ff.read()
    res = checkFile(content)
    return res


def checkHotFixFileError():
    import os
    dir = 'entities/common_server/hotfix'
    filename = os.path.join(dir, 'hotfix.txt')
    with open(filename, 'rb') as ff:
        content = ff.read()
    res = checkFile(content)
    return res


def needRebalanceDataWSWD(modeID):
    from cdata import balance_method_data as BMD
    methodList = BMD.data.get(gametypes.REBALANCE_SUBSYS_ID_WSWD, {}).get('method', [])
    if modeID <= 0 or modeID > len(methodList):
        return False
    else:
        methodID = methodList[modeID - 1]
        if methodID == const.REBALANCE_METHOD_3_USERDEF:
            return True
        return False


def enableCalcRarityMiracle():
    if BigWorld.component in ('base', 'cell'):
        return gameconfig.enableCalcRarityMiracle()
    elif BigWorld.component in ('client',):
        return gameglobal.rds.configData.get('enableCalcRarityMiracle', False)
    else:
        return False


def getAptitudeMax(spriteId, aptitudeName):
    from data import summon_sprite_info_data as SSID
    infoData = SSID.data.get(spriteId, {})
    return getAptitudeMaxFromInfo(infoData, aptitudeName)


def getAptitudeMin(spriteId, aptitudeName):
    from data import summon_sprite_info_data as SSID
    infoData = SSID.data.get(spriteId, {})
    return getAptitudeMinFromInfo(infoData, aptitudeName)


def getAptitudeMaxFromInfo(infoData, aptitudeName):
    rule = infoData.get(aptitudeName + 'RandomRule', {})
    if rule:
        return max([ max(i) for i in rule.keys() ])
    return 0


def getAptitudeMinFromInfo(infoData, aptitudeName):
    rule = infoData.get(aptitudeName + 'RandomRule', {})
    if rule:
        return min([ min(i) for i in rule.keys() ])
    return 0


APTITUDE_NAME_LIST = ['aptitudePw',
 'aptitudeAgi',
 'aptitudeSpr',
 'aptitudePhy',
 'aptitudeInt']
APTITUDE_ORI_NAME_LIST = ['oriAptitudePw',
 'oriAptitudeAgi',
 'oriAptitudeSpr',
 'oriAptitudePhy',
 'oriAptitudeInt']
APTITUDE_NAME_MAP = {'aptitudePw': 'oriAptitudePw',
 'aptitudeAgi': 'oriAptitudeAgi',
 'aptitudeSpr': 'oriAptitudeSpr',
 'aptitudePhy': 'oriAptitudePhy',
 'aptitudeInt': 'oriAptitudeInt'}
APTITUDE_TALENT_RANGE_NAME_LIST = ['growthRatio',
 'aptitudePw',
 'aptitudeAgi',
 'aptitudeSpr',
 'aptitudePhy',
 'aptitudeInt']

def getSpriteAptSumByFunc(infoData, function, originProps):
    global APTITUDE_NAME_LIST
    if BigWorld.component == 'client':
        from data import formula_client_data as FCD
    else:
        from data import formula_server_data as FCD
    props = {}
    for name in APTITUDE_NAME_LIST:
        rule = infoData.get(name + 'RandomRule', {})
        if function:
            props[name] = function([ function(i) for i in rule.keys() ]) if rule else 0
        else:
            props[name] = originProps[name]

    return sum(props.values())


def getSpriteScoreInfo(spriteId, props):
    global APTITUDE_ORI_NAME_LIST
    try:
        from data import summon_sprite_info_data as SSID
        if BigWorld.component == 'client':
            from data import formula_client_data as FORD
        else:
            from data import formula_server_data as FORD
        from data import sys_config_data as SYSCD
        err = 0
        infoData = SSID.data.get(spriteId, {})
        if not infoData:
            err += 1
            return (0,
             0,
             '',
             err)
        score = 0
        maxApt = getSpriteAptSumByFunc(infoData, max, props)
        minApt = getSpriteAptSumByFunc(infoData, min, props)
        currentApt = sum([ props[name] for name in APTITUDE_ORI_NAME_LIST ])
        if 'baseGrowthRatio' not in props:
            err += 4000
        star = getSpriteGrowthRatioStar(spriteId, props.get('baseGrowthRatio', 0))
        if 'spriteScoreLv' not in SYSCD.data:
            err += 50000
        spriteLvTxts = SYSCD.data.get('spriteScoreLv', ['lv'] * 4)
        if 'spriteScorePecents' not in SYSCD.data:
            err += 600000
        spriteScorePecents = SYSCD.data.get('spriteScorePecents', [0.5, 0.75, 0.9])
        percent = (currentApt - minApt) * 1.0 / (maxApt - minApt)
        percentIndex = 0
        for index, value in enumerate(spriteScorePecents):
            if percent > value:
                percentIndex = index + 1

        if 'spriteLvs' not in SYSCD.data:
            err += 7000000
        scoreLv = SYSCD.data.get('spriteLvs', {}).get((star, percentIndex), 0)
        title = spriteLvTxts[scoreLv]
        return (int(score),
         scoreLv,
         title,
         err)
    except Exception as e:
        if BigWorld.component in ('base', 'cell'):
            import gameengine
            gameengine.reportCritical('@smj getSpriteScoreInfo Error', spriteId, e)
        else:
            gamelog.error('@zhp getSpriteScoreInfo Error', spriteId, e)
        return (0, 0, '', 9)


def getSpriteAptitudeMinMax(spriteId, name):
    try:
        from data import summon_sprite_info_data as SSID
        if BigWorld.component == 'client':
            from data import formula_client_data as FORD
        else:
            from data import formula_server_data as FORD
        infoData = SSID.data.get(spriteId, {})
        rule = infoData.get(name + 'RandomRule', {})
        minApt = min([ min(i) for i in rule.keys() ]) if rule else 0
        maxApt = max([ max(i) for i in rule.keys() ]) if rule else 0
        return (minApt, maxApt)
    except Exception as e:
        gamelog.error('getSpriteAptitudeMinMax Error', spriteId, e)
        return (0, 0)


def getSpriteGrowthRatioStar(spriteId, growthRatio):
    from data import summon_sprite_info_data as SSID
    infoData = SSID.data.get(spriteId, {})
    star = 0
    starsNum = sorted((x[0] for x in infoData.get('growthRatioRandomRule', {}).keys()))
    for index, val in enumerate(starsNum):
        if growthRatio >= val:
            star = index

    return star


def getAwakeSkillBySpriteInfo(spriteInfo):
    if spriteInfo:
        return spriteInfo.get('skills', {}).get('awake', 0)
    return 0


def getAwakeSkillBonusBySpriteInfo(spriteInfo):
    if spriteInfo:
        return spriteInfo.get('skills', {}).get('bonus', [])
    return []


def getAwakeSkillBySprite():
    p = BigWorld.player()
    index = getattr(p, 'spriteBattleIndex', None)
    if index:
        info = p.summonSpriteList.get(index, {})
        sid = getAwakeSkillBySpriteInfo(info)
        from data import summon_sprite_skill_data as SSSD
        return SSSD.data.get(sid, {}).get('manualSkill', 0)
    return 0


def getEffLvBySpriteFamiEffLv(famiEffLv, srcName, default):
    from data import summon_sprite_familiar_data as SSFD
    lv = SSFD.data.get(famiEffLv, {}).get(srcName, default)
    return max(1, min(lv, const.MAX_SKILL_LV_SPRITE_FAMILIAR))


def getAwakeSkillLvBySpriteIdx(spriteIdx):
    p = BigWorld.player()
    spriteInfo = p.summonSpriteList.get(spriteIdx, {})
    if not spriteInfo:
        return const.DEFAULT_SKILL_LV_SPRITE
    _, _, famiEfflv = getSpriteFamiByIdx(spriteIdx)
    effLv = getEffLvBySpriteFamiEffLv(famiEfflv, 'awake', const.DEFAULT_SKILL_LV_SPRITE)
    addLv = 0
    awakeSkillId = getAwakeSkillBySpriteInfo(spriteInfo)
    from data import summon_sprite_skill_data as SSSD
    awakeSkillInfo = SSSD.data.get(awakeSkillId, {})
    awakeSkillAddSkillId, awakeSkillLvAdd = awakeSkillInfo.get('skillAddVirtualLv', (0, 0))
    awakeSkillBonus = getAwakeSkillBonusBySpriteInfo(spriteInfo)
    if awakeSkillAddSkillId in awakeSkillBonus:
        addLv = awakeSkillLvAdd
    return effLv + addLv


def enableEndlessLoopMode():
    if BigWorld.component in 'cell':
        return gameconfig.enableEndlessLoopMode()
    elif BigWorld.component in ('client',):
        return gameglobal.rds.configData.get('enableEndlessLoopMode', False)
    else:
        return False


def getStrLen(str):
    try:
        uStr = unicode(str, defaultEncoding())
        return len(uStr)
    except:
        return 0


def is_Chinese(str):
    try:
        uCh = unicode(str, defaultEncoding())
    except:
        return False

    if uCh >= '一' and uCh <= '龥':
        return True
    return False


def is_Number(str):
    try:
        return str.isdigit()
    except:
        return False


def isChineseAndNumber(string):
    try:
        string = unicode(string, defaultEncoding())
    except:
        return False

    comp = '([^0-9一-龥]+)'
    pattern = re.compile(comp)
    results = pattern.findall(string)
    if results:
        return False
    else:
        return True


def getNextEarlyMorningTime():
    tplSec = time.localtime()
    if const.EARLY_MORNING_HOUR - tplSec[3] > 0:
        return getDaySecond() + const.EARLY_MORNING_HOUR * const.TIME_INTERVAL_HOUR
    else:
        return getDaySecond() + const.TIME_INTERVAL_DAY + const.EARLY_MORNING_HOUR * const.TIME_INTERVAL_HOUR


def getDaySecondByEarlyMorning():
    return getDaySecond(getNow() - const.EARLY_MORNING_HOUR * const.TIME_INTERVAL_HOUR)


def soundRecordRichText(id, duration):
    if id:
        return '[sound%s@%.f]' % (id, duration)
    return ''


def getAccountType(urs):
    idx = urs.rfind('@')
    if idx != -1:
        suffix = urs[idx:]
        return gametypes.ACCOUNT_TYPE_SUFFIX_DICT.get(suffix, gametypes.ACCOUNT_TYPE_URS)
    else:
        return gametypes.ACCOUNT_TYPE_URS


def getGroupGoalActivationId(secondKey):
    from data import group_label_data as GLD
    if not secondKey:
        return 0
    gldd = GLD.data
    id = gldd.get(secondKey, 0).get('activateId', 0)
    return id


def allowExistItemInMap(item, mapId):
    from data import map_config_data as MCD
    from data import item_data as ID
    if not item:
        return True
    if not MCD.data.has_key(mapId):
        return True
    mapType = MCD.data[mapId].get('type', 1)
    allowExistMapTypes = ID.data.get(item.id, {}).get('allowExistMapTypes', ())
    allowExistMapIds = ID.data.get(item.id, {}).get('allowExistMaps', ())
    if allowExistMapTypes and mapType not in allowExistMapTypes or allowExistMapIds and mapId not in allowExistMapIds:
        return False
    return True


def getGroupGoalFbId(firstKey, secondKey, thirdKey):
    from cdata import group_fb_menu_data as GFMD
    if not firstKey:
        return 0
    elif secondKey == 0:
        treeData = GFMD.data[firstKey]
        fbNo = treeData.values()[0].values()[0].values()[0]
        return fbNo
    else:
        treeData = GFMD.data[firstKey][secondKey]
        fbNo = treeData.values()[0].values()[0]
        if thirdKey != const.GROUP_MATCH_FB_SECOND_LEVEL_MODE_ALL:
            fbNo = treeData[thirdKey].values()[0]
        return fbNo


def getTeamName():
    from gamestrings import gameStrings
    p = BigWorld.player()
    teamName = ''
    if hasattr(p, 'detailInfo') and len(p.detailInfo) > 0:
        teamName = p.detailInfo.get('teamName')
    if not teamName:
        if p.groupType == gametypes.GROUP_TYPE_RAID_GROUP:
            teamName = gameStrings.TEAM_DEFAULT_GROUP_NAME % p.realRoleName
        else:
            teamName = gameStrings.TEAM_DEFAULT_TEAM_NAME % p.realRoleName
    return teamName


def isActivitySaleNewPlayer():
    return True


def getStateAttrValueTypeStr(attrNo):
    if attrNo == 1:
        return 'attrValueType'
    elif attrNo > 1:
        return 'attrValueType{0}'.format(attrNo)
    else:
        return ''


def getStateAttrFstValueStr(attrNo):
    if attrNo == 1:
        return 'attrFstValue'
    elif attrNo > 1:
        return 'attrFstValue{0}'.format(attrNo)
    else:
        return ''


def getStateAttrContiValueStr(attrNo):
    if attrNo == 1:
        return 'attrContiValue'
    elif attrNo > 1:
        return 'attrContiValue{0}'.format(attrNo)
    else:
        return ''


def calcSpriteGrowthRatio(baseRatio, isJuexing, boneLv, boneBonusRatio):
    """
    :param baseRatio: 'props' -> 'baseGrowthRatio' / propReRand -> baseGrowthRatio
    :param isJuexing: 'props' -> 'juexing'
    :param boneLv:    'props' -> 'boneLv'
    :param boneBonusRatio: \xe6\x88\x98\xe7\x81\xb5\xe4\xbf\xa1\xe6\x81\xaf\xe8\xa1\xa8 spriteBoneGrowth
    :return: \xe6\x88\x98\xe7\x81\xb5\xe7\x9a\x84\xe6\x9c\x80\xe7\xbb\x88\xe6\x88\x90\xe9\x95\xbf\xe7\x8e\x87
    """
    from data import sys_config_data as SCD
    juexingBonusRatio = SCD.data.get('juexingBonusRatio', 0.1) if isJuexing else 0
    return baseRatio * (1 + juexingBonusRatio) + boneLv * boneBonusRatio


def calcDiscountedNum(num, oriDiscountRule):
    """
    :param num: \xe6\x8a\x98\xe7\xae\x97\xe5\x89\x8d\xe6\x95\xb0\xe9\x87\x8f
    :param discountRule: \xe6\x8a\x98\xe7\xae\x97\xe8\xa7\x84\xe5\x88\x99\xe5\x8f\x82\xe6\x95\xb0 \xe5\xa6\x82 ((0, 1), (20, 0.5), (40, 0.1), (100, 0))
    :return: \xe6\x8a\x98\xe7\xae\x97\xe5\x90\x8e\xe6\x95\xb0\xe9\x87\x8f\xef\xbc\x88\xe5\x90\x91\xe4\xb8\x8b\xe5\x8f\x96\xe6\x95\xb4\xef\xbc\x89\xef\xbc\x8c\xe5\xa6\x82\xe6\x9e\x9c\xe6\x9c\x89\xe9\x94\x99\xe5\x88\x99\xe8\xbf\x94\xe5\x9b\x9e 0
    """
    if not oriDiscountRule:
        return 0
    if num <= 0:
        return 0
    discountRule = sorted(oriDiscountRule, key=lambda r: r[0], reverse=True)
    if discountRule[-1][0] != 0:
        return 0
    numLeft = num
    res = 0
    for threshold, discountRatio in discountRule:
        if threshold > numLeft:
            continue
        enrolledNum = numLeft - threshold
        if enrolledNum > 0:
            res += enrolledNum * discountRatio
            numLeft -= enrolledNum

    return int(res)


def getSpriteBattleState(warSpriteIndex):
    return getattr(BigWorld.player(), 'spriteBattleIndex', None) == warSpriteIndex


def getSpriteAccessoryState(warSpriteIndex):
    bSpriteAccessory = False
    p = BigWorld.player()
    for k, v in enumerate(p.summonedSpriteAccessory):
        tInfo = p.summonedSpriteAccessory[v]
        if 'spriteIndex' in tInfo and tInfo['spriteIndex'] == warSpriteIndex:
            bSpriteAccessory = True

    return bSpriteAccessory


def checkTgtUnitType(tgt, tgtUnitType):
    if tgtUnitType == gametypes.SKILL_TGT_UNIT_TYPE_MONSTER:
        if not tgt.IsMonster or tgt.IsMonster and tgt.monsterStrengthType in gametypes.MONSTER_BOSS_TYPE:
            return False
    elif tgtUnitType == gametypes.SKILL_TGT_UNIT_TYPE_BOSS:
        if not tgt.IsMonster or tgt.IsMonster and tgt.monsterStrengthType not in gametypes.MONSTER_BOSS_TYPE:
            return False
    elif tgtUnitType == gametypes.SKILL_TGT_UNIT_TYPE_AVATAR:
        if not tgt.IsAvatar:
            return False
    elif tgtUnitType == gametypes.SKILL_TGT_UNIT_TYPE_MONSTER_ALL:
        if not tgt.IsMonster:
            return False
    elif tgtUnitType == gametypes.SKILL_TGT_UNIT_TYPE_NOT_AVATAR:
        if tgt.IsAvatar:
            return False
    elif tgtUnitType == gametypes.SKILL_TGT_UNIT_TYPE_SPRITE:
        if not tgt.IsSummonedSprite:
            return False
    elif tgtUnitType == gametypes.SKILL_TGT_UNIT_TYPE_SUMMONED_BEAST:
        if not tgt.IsSummonedBeast:
            return False
    elif tgtUnitType == gametypes.SKILL_TGT_UNIT_TYPE_WING_WORLD_BUILDING:
        if not tgt.IsWingCityWarBuilding:
            return False
    elif tgtUnitType == gametypes.SKILL_TGT_UNIT_TYPE_CLAN_WAR_UNIT:
        if not tgt.IsClanWarUnit:
            return False
    return True


def getGuildRedPacketOnlineCoef(onlineNum):
    from data import guild_config_data as GCD
    redPacketOnlineCoef = GCD.data.get('redPacketOnlineCoef')
    if redPacketOnlineCoef:
        onlineNums, params = redPacketOnlineCoef
        return params[min(getListIndexInclude(onlineNum, onlineNums), len(params) - 1)]
    return 0


def transferItemsToBinded(tempDict):
    from data import item_data as ID
    from cdata import item_parentId_data as IPD
    res = {}
    for iid, inum in tempDict.iteritems():
        newId = iid
        idBindType = ID.data.get(iid, {}).get('bindType', 0)
        if idBindType == gametypes.ITEM_BIND_TYPE_FOREVER:
            newId = iid
        else:
            for pid in IPD.data.get(iid, []):
                idBindType = ID.data.get(pid, {}).get('bindType', 0)
                if idBindType == gametypes.ITEM_BIND_TYPE_FOREVER:
                    newId = pid
                    break

        res[newId] = res.setdefault(newId, 0) + inum

    return res


def splitItemDictToMWrap(itemNumDict, autoSplitWrap):
    from data import item_data as ID
    res = []
    for iid, inum in itemNumDict.iteritems():
        inumLeft = inum
        if autoSplitWrap:
            while inumLeft > 0:
                mwrap = ID.data.get(iid, {}).get('mwrap', 1)
                if inumLeft > mwrap:
                    res.append((iid, mwrap))
                    inumLeft -= mwrap
                else:
                    res.append((iid, inumLeft))
                    inumLeft = 0

        else:
            res.append((iid, inumLeft))

    return tuple(res)


def splitItemListToMWrap(items):
    if not items:
        return []
    from data import item_data as ITEM_DATA
    itemBonus = []
    for itemId, itemNum in items:
        if itemNum <= 0:
            continue
        mwrap = ITEM_DATA.data.get(itemId, {}).get('mwrap', 999)
        if itemNum > mwrap:
            count = int(itemNum) / mwrap
            remain = int(itemNum) % mwrap
            for i in xrange(count):
                itemBonus.append((itemId, mwrap))

            if remain > 0:
                itemBonus.append((itemId, remain))
        else:
            itemBonus.append((itemId, itemNum))

    return itemBonus


def getSpriteTrainLimit(mlv, slv):
    from data import sys_config_data as SCD
    totalLimitPerDay = SCD.data.get('spriteTrainTotalTimes', 0)
    singleLimitPerDay = SCD.data.get('spriteTrainSingleTimes', 0)
    return (totalLimitPerDay, singleLimitPerDay)


def getSpriteTrainCost(mlv, slv):
    from data import sys_config_data as SCD
    import formula
    args = {'mlv': mlv,
     'slv': slv}
    moneyCost = formula.calcFormulaWithPArg(SCD.data.get('spriteTrainMoney', (0, 0)), args, default=0)
    timeCost = SCD.data.get('spriteTrainDuration', 0)
    return (moneyCost, timeCost)


def getSpriteTrainReward(mlv, slv):
    from data import sys_config_data as SCD
    import formula
    args = {'mlv': mlv,
     'slv': slv}
    expReward = formula.calcFormulaWithPArg(SCD.data.get('spriteTrainExp', (0, 0)), args, default=0)
    famiReward = formula.calcFormulaWithPArg(SCD.data.get('spriteTrainFami', (0, 0)), args, default=0)
    return (expReward, famiReward)


def getSpriteTrainLimitSameTime():
    from data import sys_config_data as SCD
    import formula
    limitSameTime = formula.calcFormulaWithPArg(SCD.data.get('spriteTrainLimitSameTime', (0, 0)), {}, default=1)
    return limitSameTime


def getSpriteAllFamiExp(spriteFamiLv, currentFamiLvExp):
    from data import summon_sprite_familiar_data as SSFD
    totalFamiExp = currentFamiLvExp
    for lv in xrange(1, spriteFamiLv):
        totalFamiExp += SSFD.data.get(lv, {}).get('upExp', 0)

    return totalFamiExp


def getSpriteFamiTransfer(totalFamiExp):
    from data import sys_config_data as SCD
    return round(totalFamiExp * SCD.data.get('spriteFamiCoverCoef', 0))


def getSpriteFamiTransferV2(totalFamiExpOut):
    from data import sys_config_data as SCD
    coef = SCD.data.get('spriteFamiCoverCoef', 0)
    minVal = SCD.data.get('spriteFamiCoverMinValue', 0)
    enableInFestival = False
    if BigWorld.component in ('base', 'cell'):
        enableInFestival = gameconfig.enableSpriteFamiTransferInFestival()
    elif BigWorld.component in ('client',):
        enableInFestival = gameglobal.rds.configData.get('enableSpriteFamiTransferInFestival', False)
    if enableInFestival:
        minVal = SCD.data.get('newSpriteFamiCoverMinValue', 0)
    return int(totalFamiExpOut - min(totalFamiExpOut * (1.0 - coef), minVal))


def getSpriteTotalFamiExpToLv(totalFamiExp):
    from data import summon_sprite_familiar_data as SSFD
    curFamiExp = 0
    famiLv = 0
    for lv in SSFD.data:
        curFamiExp += SSFD.data.get(lv, {}).get('upExp', 0)
        if curFamiExp > totalFamiExp:
            famiLv = lv
            break

    return famiLv


def getSpriteCoverCost(totalFamiExp):
    from data import sys_config_data as SCD
    import formula
    enableInFestival = False
    if BigWorld.component in ('base', 'cell'):
        enableInFestival = gameconfig.enableSpriteFamiTransferInFestival()
    elif BigWorld.component in ('client',):
        enableInFestival = gameglobal.rds.configData.get('enableSpriteFamiTransferInFestival', False)
    argDict = {'totalFamiExp': totalFamiExp}
    if enableInFestival:
        yunchuiCost = formula.calcFormulaWithPArg(SCD.data.get('newSpriteFamiCoverCostFormula', (0, 0)), argDict, default=0)
    else:
        yunchuiCost = formula.calcFormulaWithPArg(SCD.data.get('spriteFamiCoverCostFormula', (0, 0)), argDict, default=0)
    return int(round(yunchuiCost))


def getSpriteFamiByIdx(index):
    p = BigWorld.player()
    spriteInfo = p.summonSpriteList.get(index, {})
    props = spriteInfo.get('props', {})
    familiar = props.get('familiar', 1)
    famiEffAdd = props.get('famiEffAdd', 0)
    famiEffLv = props.get('famiEffLv', 1)
    return (familiar, famiEffAdd, famiEffLv)


def getSpriteTotalFamiExp(spriteIdx):
    p = BigWorld.player()
    spriteInfo = p.summonSpriteList.get(spriteIdx, {})
    props = spriteInfo.get('props', {})
    familiar = props.get('familiar', 0)
    famiExp = props.get('famiExp', 0)
    totalFamiExp = getSpriteAllFamiExp(familiar, famiExp)
    return totalFamiExp


def getSpriteFamiTransferPercentStr(spriteIdx):
    totalFamiExpOut = getSpriteTotalFamiExp(spriteIdx)
    if gameglobal.rds.configData.get('enableSpriteFamiV2', False):
        getTurnFamiOut = getSpriteFamiTransferV2(totalFamiExpOut)
        if totalFamiExpOut == 0:
            turnFamiOutStr = '0.000000%'
        else:
            turnFamiOutStr = '%.2f%%' % round(getTurnFamiOut * 1.0 / totalFamiExpOut * 100, 2)
    else:
        from data import sys_config_data as SCD
        per = SCD.data.get('spriteFamiCoverCoef', 0)
        getTurnFamiOut = totalFamiExpOut
        turnFamiOutStr = '%d%%' % int(per * 100)
    return (turnFamiOutStr, getTurnFamiOut)


def getStrNameAndGuildName(name, guildName):
    return '{0}-{1}'.format(name, guildName)


def getNameAndGuildNameFromStr(srcStr):
    return srcStr.split('-', 1)


def getRewardRecoveryServerOpTime():
    if BigWorld.component == 'client':
        import gameglobal
        if not gameglobal.rds.configData.get('enableRewardRecoveryForServerOpTime', False):
            return 0
    elif not gameconfig.enableRewardRecoveryForServerOpTime():
        return 0
    from data import sys_config_data as SCD
    rewardRecoveryServerOpTime = SCD.data.get('rewardRecoveryServerOpTime', [])
    serverOpTime = 0
    if not rewardRecoveryServerOpTime:
        return serverOpTime
    hostId = int(getHostId())
    if len(rewardRecoveryServerOpTime) == 2 and len(rewardRecoveryServerOpTime[0]) == 2:
        firstOpHostIds = rewardRecoveryServerOpTime[0][1]
        if hostId in firstOpHostIds:
            serverOpTime = rewardRecoveryServerOpTime[0][0]
        else:
            serverOpTime = rewardRecoveryServerOpTime[1][0]
    elif len(rewardRecoveryServerOpTime) == 1 and len(rewardRecoveryServerOpTime[0]) == 2:
        firstOpHostIds = rewardRecoveryServerOpTime[0][1]
        if hostId in firstOpHostIds:
            serverOpTime = rewardRecoveryServerOpTime[0][0]
        else:
            return serverOpTime
    else:
        return serverOpTime
    return getDisposableCronTabTimeStamp(serverOpTime)


def calcTimeDuration(periodType, serverOpenTime, nOffset, nLast):
    if periodType == 'day':
        tFrom = getDaySecond(serverOpenTime)
        tStart = tFrom + 86400 * (nOffset - 1)
        tEnd = tStart + 86400 * nLast
    elif periodType == 'week':
        tFrom = getWeekSecond(serverOpenTime)
        tStart = tFrom + 604800 * (nOffset - 1)
        tEnd = tStart + 604800 * nLast
    elif periodType == 'data':
        tStart = getTimeSecondFromStr(nOffset)
        tEnd = getTimeSecondFromStr(nLast) - const.SECONDS_PER_DAY
    else:
        return (sys.maxint, sys.maxint)
    return (tStart, tEnd)


def getNSPrestigeActivityConfigData():
    from data import ns_guild_prestige_act_data as GPAD
    if BigWorld.component == 'client':
        import gameglobal
        mergeTime = gameglobal.rds.configData.get('serverLatestMergeTime', 0)
    else:
        mergeTime = gameconfig.serverLatestMergeTime()
    hostId = getHostId()
    for configData in GPAD.data.values():
        if mergeTime and not configData.get('fromMergeTime'):
            continue
        if not mergeTime and configData.get('fromMergeTime'):
            continue
        if hostId not in configData.get('hostWhiteList', (hostId,)):
            continue
        if hostId in configData.get('hostBlackList', ()):
            continue
        return configData

    return {}


def getGuildPrestigeEnableStage(tFrom):
    configData = getNSPrestigeActivityConfigData()
    for i in range(1, 10):
        enableTime = configData.get('enableTime%s' % i)
        if not enableTime:
            return -1
        periodType, nWeeksOffset, nLastWeeks = enableTime
        tStart, tEnd = calcTimeDuration(periodType, tFrom, nWeeksOffset, nLastWeeks)
        if tStart <= getNow() <= tEnd:
            return i

    return -1


def getGuildPrestigeEnableStageAndOneDay(tFrom):
    stage = getGuildPrestigeEnableStage(tFrom)
    if stage == -1:
        PRIVIEGE_DAY_TO_SECOND = 86400
        configData = getNSPrestigeActivityConfigData()
        lastStage = getGuildPrestigeLastStage()
        enableTime = configData.get('enableTime%s' % lastStage)
        periodType, nWeeksOffset, nLastWeeks = enableTime
        tStart, tEnd = calcTimeDuration(periodType, getServerOpenTime(), nWeeksOffset, nLastWeeks)
        if getNow() <= tEnd + PRIVIEGE_DAY_TO_SECOND:
            stage = lastStage
    return stage


def getGuildPrestigeNearestStage(tFrom):
    configData = getNSPrestigeActivityConfigData()
    curTime = getNow()
    for i in range(1, 10):
        enableTime = configData.get('enableTime%s' % i)
        if not enableTime:
            return (-1, 0)
        periodType, nWeeksOffset, nLastWeeks = enableTime
        tStart, tEnd = calcTimeDuration(periodType, tFrom, nWeeksOffset, nLastWeeks)
        if tStart <= curTime <= tEnd:
            return (i, 0)
        if curTime < tStart:
            return (i, tStart - curTime)

    return (-1, 0)


def getGuildPrestigeNextStageTime(tFrom, curStage):
    configData = getNSPrestigeActivityConfigData()
    enableTime = configData.get('enableTime%s' % (curStage + 1))
    if not enableTime:
        return 0
    periodType, nWeeksOffset, nLastWeeks = enableTime
    tStart, tEnd = calcTimeDuration(periodType, tFrom, nWeeksOffset, nLastWeeks)
    return tStart


def getGuildPrestigeStageEndTime(tFrom, curStage):
    configData = getNSPrestigeActivityConfigData()
    enableTime = configData.get('enableTime%s' % curStage)
    if not enableTime:
        return 0
    periodType, nWeeksOffset, nLastWeeks = enableTime
    tStart, tEnd = calcTimeDuration(periodType, tFrom, nWeeksOffset, nLastWeeks)
    return tEnd


def getGuildPrestigeLastStage():
    configData = getNSPrestigeActivityConfigData()
    for i in range(10, 0, -1):
        enableTime = configData.get('enableTime%s' % i)
        if not enableTime:
            continue
        return i

    return 0


def getGuildPrestigeStageReduce(enterStage):
    configData = getNSPrestigeActivityConfigData()
    reduce = configData.get('reduce%s' % enterStage, 0)
    if reduce > 1:
        reduce = 1
    elif reduce < 0:
        reduce = 0
    return reduce


def getNewServerPropertyRankActStage(topType, val):
    configDataList = getNSPropertyRankActData(topType)
    if not configDataList:
        return -1
    hostId = getHostId()
    nStage = len(configDataList)
    nowTime = getNow()
    openTime = getServerOpenTime()
    for stage in range(nStage - 1, -1, -1):
        configData = configDataList[stage]
        if not configData.has_key('propertyTarget'):
            continue
        if configData.has_key('hostWhiteList') and hostId not in configData['hostWhiteList']:
            continue
        if hostId in configData.get('hostBlackList', ()):
            continue
        if configData.has_key('enableTime'):
            periodType, offset, last = configData['enableTime']
            tStart, tEnd = calcTimeDuration(periodType, openTime, offset, last)
            if not tStart <= nowTime < tEnd:
                continue
        if configData.has_key('needServerProgress'):
            msId = configData['needServerProgress']
            if BigWorld.component == 'client':
                p = BigWorld.player()
                finished = p.isServerProgressFinished(msId)
                if not finished:
                    continue
            else:
                import serverProgress
                finished = serverProgress.isMileStoneFinished(msId)
                tFinished = serverProgress.getProgressStatus(gameconst.SP_PROP_MILE_STONE, msId)
                if not finished or getDaySecond(tFinished) == getDaySecond():
                    continue
        targetVal = configData['propertyTarget']
        if type(val) in (tuple, list):
            if all([ iv >= tv for iv, tv in zip(val, targetVal) ]):
                return stage
        elif val >= targetVal:
            return stage

    return -1


def getNewServerPropertyRankActStageClient(topType, val):
    configDataList = getNSPropertyRankActData(topType)
    if not configDataList:
        return -1
    hostId = getHostId()
    nStage = len(configDataList)
    nowTime = getNow()
    openTime = getServerOpenTime()
    enableStages = []
    for stage in range(nStage - 1, -1, -1):
        configData = configDataList[stage]
        if not configData.has_key('propertyTarget'):
            continue
        if configData.has_key('hostWhiteList') and hostId not in configData['hostWhiteList']:
            gamelog.debug('@hxm act is invalid: whiteList', topType, hostId, configData['hostWhiteList'])
            continue
        if hostId in configData.get('hostBlackList', ()):
            gamelog.debug('@hxm act is invalid: blackList', topType, hostId, configData['hostBlackList'])
            continue
        if configData.has_key('enableTime'):
            periodType, offset, last = configData['enableTime']
            tStart, tEnd = calcTimeDuration(periodType, openTime, offset, last)
            if not tStart <= nowTime < tEnd + const.SECONDS_PER_DAY:
                gamelog.debug('@hxm act is invalid: enableTime', topType, tStart, tEnd, stage, configData['enableTime'])
                continue
        if configData.has_key('needServerProgress'):
            msId = configData['needServerProgress']
            if BigWorld.component == 'client':
                p = BigWorld.player()
                finished = p.isServerProgressFinished(msId)
                if not finished:
                    gamelog.debug('@hxm act is invalid: needServerProgress', topType, stage, msId, finished)
                    continue
            else:
                import serverProgress
                finished = serverProgress.isMileStoneFinished(msId)
                tFinished = serverProgress.getProgressStatus(gameconst.SP_PROP_MILE_STONE, msId)
                if not finished or getDaySecond(tFinished) == getDaySecond():
                    gamelog.debug('@hxm act is invalid: needServerProgress', topType, stage, msId, finished, tFinished)
                    continue
        enableStages.append(stage)
        targetVal = configData['propertyTarget']
        if type(val) in (tuple, list):
            if all([ iv > tv for iv, tv in zip(val, targetVal) ]):
                return min(stage + 1, nStage - 1)
        elif val > targetVal:
            return min(stage + 1, nStage - 1)

    enableStages = enableStages if enableStages else [0]
    return min(enableStages)


def getEnableNewServerPropertyRankActStages(topType):
    import const
    enableStages = []
    configDataList = getNSPropertyRankActData(topType)
    if not configDataList:
        return []
    hostId = getHostId()
    nStage = len(configDataList)
    nowTime = getNow()
    openTime = getServerOpenTime()
    for stage in range(nStage - 1, -1, -1):
        configData = configDataList[stage]
        if not configData.has_key('propertyTarget'):
            continue
        if configData.has_key('hostWhiteList') and hostId not in configData['hostWhiteList']:
            gamelog.debug('@hxm act is invalid: whiteList', topType, hostId, configData['hostWhiteList'])
            continue
        if hostId in configData.get('hostBlackList', ()):
            gamelog.debug('@hxm act is invalid: blackList', topType, hostId, configData['hostBlackList'])
            continue
        if configData.has_key('enableTime'):
            periodType, offset, last = configData['enableTime']
            tStart, tEnd = calcTimeDuration(periodType, openTime, offset, last)
            if not tStart <= nowTime < tEnd + const.SECONDS_PER_DAY:
                gamelog.debug('@hxm act is invalid: enableTime', topType, tStart, tEnd, stage, configData['enableTime'])
                continue
        if configData.has_key('needServerProgress'):
            msId = configData['needServerProgress']
            if BigWorld.component == 'client':
                p = BigWorld.player()
                finished = p.isServerProgressFinished(msId)
                if not finished:
                    gamelog.debug('@hxm act is invalid: needServerProgress', topType, stage, msId, finished)
                    continue
            else:
                import serverProgress
                finished = serverProgress.isMileStoneFinished(msId)
                tFinished = serverProgress.getProgressStatus(gameconst.SP_PROP_MILE_STONE, msId)
                if not finished or getDaySecond(tFinished) == getDaySecond():
                    gamelog.debug('@hxm act is invalid: needServerProgress', topType, stage, msId, finished, tFinished)
                    continue
        enableStages.append(stage)

    return enableStages


def updateDict(d, updateDict):
    if d is None:
        return updateDict
    else:
        d.update(updateDict)
        return d


def selectByKeyRange(sList, key):
    for kRange, val in sList:
        left, right = kRange
        if key >= left and key <= right:
            return val


def getDefaultPhoto(school, sex):
    return 'headIcon/%s.dds' % str(school * 10 + sex)


def convertObjectToHexStr(data):
    return binascii.hexlify(cPickle.dumps(data, -1))


def convertHexStrToObject(hexStr):
    return cPickle.loads(binascii.unhexlify(hexStr))


def getDistanceToLine(ent, lineEntL, lineEntR):
    vecL = lineEntL.position - ent.position
    vecR = lineEntR.position - ent.position
    vecH = lineEntR.position - lineEntL.position
    xMultiple = sum((lp * rp for lp, rp in zip(vecL, vecR)))
    if not vecL.length or not vecR.length:
        return 0
    interCos = xMultiple / (vecL.length * vecR.length)
    interSin = pow(1 - pow(interCos, 2), 0.5)
    if not vecH.length:
        return vecL.length
    distToFootLine = interSin * vecL.length * vecR.length / vecH.length
    return distToFootLine


def faceIdToString(faceId):
    if faceId < 10:
        return '#00%d' % faceId
    elif faceId < 100:
        return '#0%d' % faceId
    else:
        return '#%d' % faceId


def isInRectangle(p1, p2, p3, p4, p):
    if crossProduct(p, p1, p2) * crossProduct(p, p4, p3) <= 0 and crossProduct(p, p4, p1) * crossProduct(p, p3, p2) <= 0:
        return True
    return False


def crossProduct(p1, p2, p0):
    return (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p2[0] - p0[0]) * (p1[1] - p0[1])


def isLineSegmentJudge(a, b, c, d):
    if not (min(a.x, b.x) <= max(c.x, d.x) and min(c.y, d.y) <= max(a.y, b.y) and min(c.x, d.x) <= max(a.x, b.x) and min(a.y, b.y) <= max(c.y, d.y)):
        return False
    u = (c.x - a.x) * (b.y - a.y) - (b.x - a.x) * (c.y - a.y)
    v = (d.x - a.x) * (b.y - a.y) - (b.x - a.x) * (d.y - a.y)
    w = (a.x - c.x) * (d.y - c.y) - (d.x - c.x) * (a.y - c.y)
    z = (b.x - c.x) * (d.y - c.y) - (d.x - c.x) * (b.y - c.y)
    return u * v < 0 and w * z < 0


def getWingWorldXinMoRegionHostId(hostId = 0):
    from data import region_server_config_data as RSCD
    from cdata import wing_world_xinmo_host_data as WWXHD
    hostId = hostId or getHostId()
    RSCData = RSCD.data.get(hostId, {})
    wingGlobalHostId = RSCData.get('wingWorldGlobalHostId', 0)
    groupId = RSCData.get('wingWorldGroupId', 0)
    return WWXHD.data.get(wingGlobalHostId, {}).get(groupId, 0)


def getWingWorldGroupId(hostId = 0):
    from data import region_server_config_data as RSCD
    hostId = hostId or getHostId()
    groupId = RSCD.data.get(hostId, {}).get('wingWorldGroupId', 0)
    return groupId


def getQuizzesCenterHostId(hostId = 0):
    from data import region_server_config_data as RSCD
    hostId = hostId or getHostId()
    return RSCD.data.get(hostId, {}).get('quizzesCenterHostId', 0)


def isYaojingqitanStartQuest(questId):
    """
    \xe5\x88\xa4\xe6\x96\xad\xe6\x98\xaf\xe5\x90\xa6\xe6\x98\xaf\xe5\xa6\x96\xe7\xb2\xbe\xe5\xa5\x87\xe8\xb0\xad\xe7\xac\xac\xe4\xb8\x80\xe7\x8e\xaf\xe4\xbb\xbb\xe5\x8a\xa1
    :param questId:
    :return:
    """
    if BigWorld.component in ('base', 'cell') and not gameconfig.enableYaojingqitanCustomCost():
        return False
    if BigWorld.component == 'client' and not gameglobal.rds.configData.get('enableYaojingqitanCustomCost', False):
        return False
    from data import sys_config_data as SCD
    if questId in SCD.data.get('yaojingqitanStartQuestIds', ()):
        return True
    return False


def isYaojingqitanEndQuest(questId):
    """
    \xe5\x88\xa4\xe6\x96\xad\xe6\x98\xaf\xe5\x90\xa6\xe6\x98\xaf\xe5\xa6\x96\xe7\xb2\xbe\xe5\xa5\x87\xe8\xb0\xad\xe6\x9c\x80\xe5\x90\x8e\xe4\xb8\x80\xe7\x8e\xaf\xe4\xbb\xbb\xe5\x8a\xa1
    :param questId:
    :return:
    """
    if BigWorld.component in ('base', 'cell') and not gameconfig.enableYaojingqitanCustomCost():
        return False
    if BigWorld.component == 'client' and not gameglobal.rds.configData.get('enableYaojingqitanCustomCost', False):
        return False
    from data import sys_config_data as SCD
    if questId in SCD.data.get('yaojingqitanEndQuestIds', ()):
        return True
    return False


def randomByDictUniform(randomDict, default = 0):
    valueList = randomDict.values()
    if -1 in valueList:
        for k, v in randomDict.iteritems():
            if -1 == v:
                return k

    totalValue = sum(valueList)
    randomNum = random.uniform(0, totalValue)
    for k, v in randomDict.iteritems():
        if randomNum > v:
            randomNum -= v
            continue
        return k

    return default


def getValueByRangeKey(rangeDict, key, default = 0):
    for rang, val in rangeDict.iteritems():
        low, high = rang
        if low <= key <= high:
            return val

    return default


def getValueByRangeKeyContainLeft(rangeDict, key, default = 0):
    for rang, val in rangeDict.iteritems():
        low, high = rang
        if low <= key < high:
            return val

    return default


def getRegionHostId(arenaMode = 0, hostId = 0, tgtHostId = 0):
    if arenaMode in const.ARENA_MODE_CLAN_WAR_CHALLENGE:
        return tgtHostId or getHostId()
    if arenaMode == const.ARENA_MODE_CROSS_WING_WORLD_XINMO:
        return getWingWorldXinMoRegionHostId(hostId)
    if arenaMode == const.ARENA_MODE_CROSS_LUN_ZHAN_YUN_DIAN:
        return lzydRegionServerHostId(hostId)
    return regionServerHostId(hostId)


def getRegionServerName(arenaMode = 0, hostId = 0, tgtHostId = 0):
    if arenaMode in const.ARENA_MODE_CLAN_WAR_CHALLENGE:
        return getServerName(tgtHostId)
    if arenaMode == const.ARENA_MODE_CROSS_WING_WORLD_XINMO:
        return getServerName(getWingWorldXinMoRegionHostId(hostId))
    if arenaMode == const.ARENA_MODE_CROSS_LUN_ZHAN_YUN_DIAN:
        return lzydRegionServerName(hostId)
    return regionServerName(hostId)


def getGuildRoleIdPriority(roleId):
    pdata = gametypes.GUILD_PRIVILEGES.get(roleId)
    return pdata['priority']


def _usePtrDataForEquipEnhJuexing():
    if BigWorld.component == 'client':
        import gameglobal
        return gameglobal.rds.configData.get('enableEquipJuexingServerConfig', 0)
    else:
        import gameconfig
        return gameconfig.enableEquipJuexingServerConfig()


def getEquipEnhJuexingData(eType, eSubType, enhLv, enhType):
    if _usePtrDataForEquipEnhJuexing():
        from data import equip_enhance_juexing_ptr_data as EEJDPTR
        return EEJDPTR.data.get((eType,
         eSubType,
         enhLv,
         enhType), [])
    else:
        from data import equip_enhance_juexing_data as EEJD
        return EEJD.data.get((eType,
         eSubType,
         enhLv,
         enhType), [])


def getEquipEnhJuexingPyData():
    if _usePtrDataForEquipEnhJuexing():
        from data import equip_enhance_juexing_ptr_data as EEJDPTR
        return EEJDPTR.data
    else:
        from data import equip_enhance_juexing_data as EEJD
        return EEJD.data


def getEquipEnhJuexingPropData(eType, eSubType, enhLv, enhType):
    if _usePtrDataForEquipEnhJuexing():
        from cdata import equip_enhance_juexing_prop_ptr_data as EEJPDPTR
        return EEJPDPTR.data.get((eType,
         eSubType,
         enhLv,
         enhType), [])
    else:
        from cdata import equip_enhance_juexing_prop_data as EEJPD
        return EEJPD.data.get((eType,
         eSubType,
         enhLv,
         enhType), [])


def showDebugMsg(owner, data):
    if BigWorld.component == 'client':
        return
    if gameconfig.publicServer():
        return
    if not getattr(owner, 'client'):
        return
    from cdata import game_msg_def_data as GMDD
    owner.client.showGameMsg(GMDD.data.COMMON_MSG, 'DebugMsg:' + data)


def getCbgRoleType(sex, school):
    """
    \xe8\x97\x8f\xe5\xae\x9d\xe9\x98\x81equip_type
    \xe7\xba\xa6\xe5\xae\x9a\xe4\xb8\xbaSEX*100+SCHOOL
    :param sex: \xe6\x80\xa7\xe5\x88\xab
    :param school: \xe8\x81\x8c\xe4\xb8\x9a
    :return: 
    """
    return sex * 100 + school


def isCbgRoleType(t):
    return const.CBG_ITEM_TYPE_ROLE_MIN <= t <= const.CBG_ITEM_TYPE_ROLE_MAX


def getSchoolByCbgRoleType(t):
    return t % 100


def isCbgRoleSameWhiteGbId(gbId):
    from cdata import cbg_role_sale_white_data as CRSWD
    return gbId in CRSWD.data.get(gbId % 1000, [])


def convertToUTF8String(originString):
    return originString.decode(defaultEncoding()).encode('UTF-8')


def spriteGrowthUpLimitInit(entryId):
    """
    \xe8\x8b\xb1\xe7\x81\xb5\xe4\xbf\xae\xe7\x82\xbc\xe6\x9d\xa1\xe7\x9b\xae\xe7\x9a\x84\xe5\x88\x9d\xe5\xa7\x8b\xe5\x8f\xaf\xe4\xbf\xae\xe7\x82\xbc\xe7\xad\x89\xe7\xba\xa7\xe4\xb8\x8a\xe9\x99\x90
    :param entryId: \xe6\x9d\xa1\xe7\x9b\xaeID
    """
    from cdata import sprite_growth_entry_post_data as SGEPD
    defaultVal = getSpriteGrowthEntryLvLimit(entryId)
    return SGEPD.data.get(entryId, {}).get(0, defaultVal)


def spriteGrowthUpLimitDelta(entryId, curUpLimit):
    """
    \xe8\x8b\xb1\xe7\x81\xb5\xe4\xbf\xae\xe7\x82\xbc\xe6\x9d\xa1\xe7\x9b\xae\xe5\xbd\x93\xe5\x89\x8d\xe7\xad\x89\xe7\xba\xa7\xe7\xaa\x81\xe7\xa0\xb4\xe4\xb8\x8a\xe9\x99\x90\xe7\x9a\x84\xe5\xa2\x9e\xe9\x87\x8f
    :param entryId: \xe6\x9d\xa1\xe7\x9b\xaeID
    :param curUpLimit: \xe5\xbd\x93\xe5\x89\x8d\xe5\xb7\xb2\xe7\xaa\x81\xe7\xa0\xb4\xe4\xb8\x8a\xe9\x99\x90
    """
    from cdata import sprite_growth_entry_post_data as SGEPD
    return SGEPD.data.get(entryId, {}).get(curUpLimit, curUpLimit) - curUpLimit


def isLvByPlayerLvSkill(skillId):
    from data import skill_general_data as SGD
    return SGD.data.get((skillId, 1), {}).get('skLvByPlayerLv')


def getConsumedGrowthExpItems(entryId, lv):
    """\xe8\xbf\x94\xe5\x9b\x9e\xe5\xbd\x93\xe5\x89\x8d\xe4\xbf\xae\xe7\x82\xbc\xe7\xad\x89\xe7\xba\xa7\xe5\xb7\xb2\xe6\xb6\x88\xe8\x80\x97\xe7\x9a\x84\xe7\xbb\x8f\xe9\xaa\x8c\xe9\x81\x93\xe5\x85\xb7"""
    from data import sys_config_data as SCD
    from data import sprite_growth_entry_data as SGED
    from cdata import item_parentId_data as IPD
    returnItems = SCD.data.get('returnSpriteGrowthItems', {})
    result = dict()
    if lv <= 0:
        return result
    for i in xrange(1, lv + 1):
        items = SGED.data.get((entryId, i), {}).get('expItems')
        if not items:
            continue
        for itemId, num in items:
            if not returnItems.get(itemId):
                subItemIds = IPD.data.get(itemId)
                if itemId in subItemIds:
                    subItemIds.remove(itemId)
                if not subItemIds:
                    continue
                itemId = min(subItemIds)
            else:
                itemId = returnItems.get(itemId)
            if result.has_key(itemId):
                result[itemId] += num
            else:
                result[itemId] = num

    return result


def getConsumedGrowthExceedItems(entryId, lv):
    """\xe8\xbf\x94\xe5\x9b\x9e\xe5\xbd\x93\xe5\x89\x8d\xe4\xbf\xae\xe7\x82\xbc\xe7\xad\x89\xe7\xba\xa7\xe5\xb7\xb2\xe6\xb6\x88\xe8\x80\x97\xe7\x9a\x84\xe7\xaa\x81\xe7\xa0\xb4\xe9\x81\x93\xe5\x85\xb7"""
    from data import sys_config_data as SCD
    from data import sprite_growth_entry_data as SGED
    from cdata import item_parentId_data as IPD
    returnItems = SCD.data.get('returnSpriteGrowthItems', {})
    result = dict()
    if lv <= 0:
        return result
    for i in xrange(1, lv + 1):
        items = SGED.data.get((entryId, i), {}).get('exceedItem')
        if not items:
            continue
        for itemId, num in items:
            if not returnItems.get(itemId):
                subItemIds = IPD.data.get(itemId)
                if itemId in subItemIds:
                    subItemIds.remove(itemId)
                if not subItemIds:
                    continue
                itemId = min(subItemIds)
            else:
                itemId = returnItems.get(itemId)
            if result.has_key(itemId):
                result[itemId] += num
            else:
                result[itemId] = num

    return result


def getNSPropertyRankActData(topType):
    from cdata import ns_property_rank_act_data as NPRAD
    hostId = getHostId()
    targetData = NPRAD.data.get((topType, hostId), [])
    defaultData = NPRAD.data.get((topType, 0), [])
    if targetData:
        return targetData
    return defaultData


def getHistoryConsumedCenterHostId(hostId = 0):
    from data import region_server_config_data as RSCD
    hostId = hostId or getHostId()
    return RSCD.data.get(hostId, {}).get('historyConsumedCenterHostId', 0)


def getHistoryConsumedActId():
    from data import history_consumed_config_data as HCCD
    now = getNow()
    curHost = getHostId()
    for actId, mVal in HCCD.data.iteritems():
        if curHost not in mVal.get('includeHosts', ()):
            continue
        startDay = mVal.get('startDay', '2018.1.1.0.0.0')
        endDay = mVal.get('endDay', '2018.1.1.0.0.0')
        if getTimeSecondFromStr(startDay) <= now < getTimeSecondFromStr(endDay):
            return actId

    return 0


def checkHistoryConsumedActId(mActId):
    from data import history_consumed_config_data as HCCD
    now = getNow()
    curHost = getHostId()
    for actId, mVal in HCCD.data.iteritems():
        startDay = mVal.get('startDay', '2018.1.1.0.0.0')
        endDay = mVal.get('endDay', '2018.1.1.0.0.0')
        if getTimeSecondFromStr(startDay) <= now < getTimeSecondFromStr(endDay) and actId == mActId:
            return True

    return False


def parseCrontabStr2List(crontabStr):
    result = []
    try:
        for index, str in enumerate(crontabStr.split(' ')):
            if str == '*':
                result.append([])
            elif str.find(',') >= 0:
                timeList = [ int(timeStr) for timeStr in str.split(',') ]
                result.append(timeList)
            elif str.find('-') >= 0:
                startStr, endStr = str.split('-')
                timeList = range(int(startStr), int(endStr) + 1)
                result.append(timeList)
            elif str.find('/') >= 0:
                rangeList = allTimeRanges[index]
                denominator = int(str.split('/')[-1])
                if index == 2:
                    resultList = [(-1, denominator)]
                else:
                    resultList = [ time for time in rangeList if not time % denominator ]
                result.append(resultList)
            else:
                result.append([int(str)])

    except Exception as e:
        gamelog.error('parseContabStr2Tuple Error', crontabStr)

    return result


def enableCronStr2List():
    if BigWorld.component == 'client':
        return gameglobal.rds.configData.get('enableParseCronStr2List', False)
    return False


def convertNum(num):
    from gamestrings import gameStrings
    if type(num) == str:
        return num
    elif num > 100000000:
        return gameStrings.BF_HISTORY_YI % ('%.3f' % (num * 1.0 / 100000000))
    elif num > 10000:
        return gameStrings.BF_HISTORY_WAN % int(num / 10000)
    else:
        return str(int(num))


def getCommonGameConfig(name):
    val = None
    if BigWorld.component in ('base', 'cell'):
        try:
            val = BigWorld.globalData['CONFIG'][name]
        except Exception as e:
            reportWarning('@xjw getCommonGameConfig exception! %s, %s' % (name, str(e)))

    elif BigWorld.component in ('client',):
        val = gameglobal.rds.configData.get(name)
    return val


def slimDict(d):
    rmKeys = []
    for key in d.iterkeys():
        if len(d[key]) == 0:
            rmKeys.append(key)

    for key in rmKeys:
        d.pop(key, None)


def getFTBCenterHostId(hostId = 0):
    from data import region_server_config_data as RSCD
    hostId = hostId or getHostId()
    return RSCD.data.get(hostId, {}).get('ftbCenterHostId', 0)


def isRealOnlineServer(hostId = 0):
    if not hostId:
        hostId = getHostId()
    return hostId / 10000 == 1


def whatDayFromCrontabStr(cron):
    """
    \xe4\xbb\x8ecrontab\xe5\xad\x97\xe7\xac\xa6\xe4\xb8\xb2\xe4\xb8\xad\xe8\x8e\xb7\xe5\x8f\x96\xe6\x98\x9f\xe6\x9c\x9f\xe5\x87\xa0
    1-7\xe8\xa1\xa8\xe7\xa4\xba\xe6\x98\x9f\xe6\x9c\x9f\xe4\xb8\x80\xe5\x88\xb0\xe6\x98\x9f\xe6\x9c\x9f\xe6\x97\xa5\xef\xbc\x8c
    0\xe8\xa1\xa8\xe7\xa4\xba\xe4\xb8\x8d\xe5\x90\x88\xe6\xb3\x95\xe6\x88\x96\xe6\xb2\xa1\xe6\x9c\x89\xe6\x8c\x87\xe5\xae\x9a\xe6\x98\x9f\xe6\x9c\x9f
    """
    li = parseCrontabPattern(cron)
    return li[WEEKEND][0] + 1


def whatDayToday(timestamp = 0):
    """
    \xe8\x8e\xb7\xe5\x8f\x96\xe4\xbb\x8a\xe5\xa4\xa9\xe6\x98\xaf\xe6\x98\x9f\xe6\x9c\x9f\xe5\x87\xa0
    1-7\xe8\xa1\xa8\xe7\xa4\xba\xe6\x98\x9f\xe6\x9c\x9f\xe4\xb8\x80\xe5\x88\xb0\xe6\x98\x9f\xe6\x9c\x9f\xe6\x97\xa5
    """
    from datetime import datetime
    t = getNow() if not timestamp else timestamp
    return datetime.fromtimestamp(t).weekday() + 1


def getBaseAngleSize(entityCnt):
    from data import sys_config_data as SCD
    data = SCD.data.get('selectDirAngleSize', {(0, 15): 1,
     (16, 30): 3,
     (31, 60): 5,
     (61, 120): 7,
     (121, 360): 9})
    for tup, baseAngle in data.iteritems():
        if tup[0] <= entityCnt <= tup[1]:
            return baseAngle

    return max(data.values())


def getAngleOfMaxCnt(angleList, angleSlice):
    """
    \xe8\x8e\xb7\xe5\x8f\x96\xe6\x8c\x87\xe5\xae\x9a\xe8\xa7\x92\xe5\xba\xa6\xe8\x8c\x83\xe5\x9b\xb4\xe5\x86\x85\xef\xbc\x8c\xe5\xae\x9e\xe4\xbd\x93\xe6\x95\xb0\xe6\x9c\x80\xe5\xa4\x9a\xe7\x9a\x84\xe8\xa7\x92\xe5\xba\xa6
    :param angleList: \xe8\xa7\x92\xe5\xba\xa6\xe5\x88\x97\xe8\xa1\xa8
    :param angleSlice: \xe8\xa7\x92\xe5\xba\xa6\xe5\x88\x87\xe7\x89\x87
    :return:
    """
    if angleSlice <= 0:
        return 0
    if not angleList:
        return 0
    if len(angleList) == 1:
        return angleList[0]
    angleSlice = angleSlice % 360
    angleList.sort()
    angleDict = OrderedDict()
    baseAngle = getBaseAngleSize(len(angleList))
    f = lambda x: x / baseAngle * baseAngle + baseAngle / 2
    for v in angleList:
        key = f(v)
        angleDict[key] = angleDict.get(key, 0) + 1

    length = len(angleDict)
    for angle in angleList:
        if angle > angleSlice:
            break
        key = f(angle)
        angleDict[key + 360] = angleDict.get(key + 360, 0) + 1

    angles = angleDict.keys()
    maxEntityCnt, leftAngle, rightAngle = angleDict[angles[0]], angles[0], angles[0]
    for i in xrange(length):
        entityCnt = 0
        for j in xrange(i, len(angles)):
            if angles[j] - angles[i] > angleSlice:
                break
            entityCnt += angleDict.get(angles[j])
            if entityCnt > maxEntityCnt:
                leftAngle, rightAngle, maxEntityCnt = angles[i], angles[j], entityCnt

    result = (leftAngle + rightAngle) / 2 % 360
    return result


def json_loads_byteified(json_text, encoding = 'gkb'):
    return _byteify(json.loads(json_text, object_hook=_byteify), ignore_dicts=True, encoding=encoding)


def _byteify(data, ignore_dicts = False, encoding = 'gbk'):
    if isinstance(data, unicode):
        return data.encode(encoding)
    if isinstance(data, list):
        return [ _byteify(item, ignore_dicts=True, encoding=encoding) for item in data ]
    if isinstance(data, dict) and not ignore_dicts:
        return {_byteify(key, ignore_dicts=True, encoding=encoding):_byteify(value, ignore_dicts=True, encoding=encoding) for key, value in data.iteritems()}
    return data


def enableFlyUp():
    import gameconfigCommon
    if not gameconfigCommon.enableFlyUp():
        return False
    if gameconfigCommon.enableIgnoreFlyUpGroupCheck():
        return True
    from cdata import fly_up_config_data as fucd
    groupId = getWingWorldGroupId(getHostId())
    if groupId == gametypes.FLY_UP_GROUP_ONE:
        return True
    if groupId == gametypes.FLY_UP_GROUP_TWO and getServerOpenDays() >= fucd.data.get('flyUpServerOpenDays', 0):
        return True
    return False


def crontabTimeArgsToStr(timeArgs):
    ret = ''
    try:
        for i, s in enumerate(timeArgs):
            if not s:
                ret += '* '
            else:
                val = ''
                for v in s:
                    val += str(v) + ','

                if val.endswith(','):
                    val = val[:-1]
                ret += val + ' '

        if ret.endswith(' '):
            ret = ret[:-1]
    except Exception as e:
        ret = '* * * * *'
        print 'crontabTimeArgsToStr ERROR, exception %s' % (e.message,)
    finally:
        return ret


def getSchoolTopOpenTime():
    """\xe6\x96\xb0\xe6\x9c\x8d\xe9\x97\xa8\xe6\xb4\xbe\xe9\xa6\x96\xe5\xb8\xad\xe5\xae\x9a\xe6\x97\xb6\xe5\xbc\x80\xe5\x85\xb3\xe6\x97\xb6\xe9\x97\xb4"""
    import calendar
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    m1 = calendar.MONDAY
    m7 = calendar.SUNDAY
    nextMon = copy.deepcopy(today)
    nextSun = copy.deepcopy(today)
    while nextMon.weekday() != m1:
        nextMon += oneday

    while nextSun.weekday() != m7:
        nextSun += oneday

    nextMon = '{}.{}.{}.0.3.0'.format(nextMon.year, nextMon.month, nextMon.day)
    nextSun = '{}.{}.{}.23.58.0'.format(nextSun.year, nextSun.month, nextSun.day)
    return (nextSun, nextMon)


def generateNewDyeMaterials(oldDyeMaterials, dyeMaterials):
    newDyeMaterials = list(oldDyeMaterials)
    if oldDyeMaterials:
        for newMaterial in dyeMaterials:
            hasFound = False
            for i, oldMaterail in enumerate(oldDyeMaterials):
                if oldMaterail[0] == newMaterial[0]:
                    newDyeMaterials[i] = newMaterial
                    hasFound = True
                    break

            if not hasFound:
                newDyeMaterials.append(newMaterial)

    else:
        newDyeMaterials = dyeMaterials
    return newDyeMaterials


def generateDyeMaterialsPriorityList():
    from cdata import material_dye_data as MAD
    from item import Item

    def dyeMaterialsCmp(x1, x2):
        data1 = MAD.data.get(x1, {})
        data2 = MAD.data.get(x2, {})
        dyeType1 = data1.get('dyeType', 0)
        dyeType2 = data2.get('dyeType', 0)
        ret = cmp(dyeType1, dyeType2)
        if ret == 0:
            if data1.has_key('dyeQuality') and data2.has_key('dyeQuality'):
                dyeQuality1 = data1['dyeQuality']
                dyeQuality2 = data2['dyeQuality']
                ret = cmp(dyeQuality1, dyeQuality2)
                if ret == 0:
                    return cmp(x1, x2)
                return ret
            return cmp(x1, x2)
        return ret

    items = MAD.data.keys()
    items.sort(dyeMaterialsCmp)
    color_normal = []
    color_high = []
    color_rare = []
    for itemId in items:
        if MAD.data.get(itemId, {}).get('dyeType') == Item.CONSUME_DYE_NORMAL:
            if MAD.data.get(itemId, {}).get('dyeQuality') == 1:
                color_normal.append(itemId)
            elif MAD.data.get(itemId, {}).get('dyeQuality') == 2:
                color_high.append(itemId)
            elif MAD.data.get(itemId, {}).get('dyeQuality') == 3:
                color_rare.append(itemId)

    return (color_normal, color_high, color_rare)


def checkSamePropTypes(propsA, propsB):
    propTypesA = sorted([ x[0] for x in propsA ])
    propTypesB = sorted([ x[0] for x in propsB ])
    return propTypesA == propTypesB


def randSchools(n = 1):
    """\xe9\x9a\x8f\xe6\x9c\xban\xe4\xb8\xaa\xe8\x81\x8c\xe4\xb8\x9a"""
    return [ random.choice(const.SCHOOL_SET) for i in xrange(n) ]


def getSpriteGrowthEntryLvLimit(entryId):
    from cdata import sprite_growth_entry_lvLimit_post_data as SGELPD
    return SGELPD.data.get(entryId, const.SPRITE_GROWTH_LV_LIMIT)


def getCellContainerName(resKind):
    if resKind in const.ALL_CELL_PAGE_POS_BAG_KINDS.iterkeys():
        return const.ALL_CELL_PAGE_POS_BAG_KINDS.get(resKind)
    return ''


def getBaseContainerName(resKind):
    if resKind in const.ALL_BASE_PAGE_POS_BAG_KINDS.iterkeys():
        return const.ALL_BASE_PAGE_POS_BAG_KINDS.get(resKind)
    return ''


def getPageAndPosByIt(bag, item):
    try:
        for pg, page in enumerate(bag.pages):
            for ps, it in enumerate(page):
                if it == item:
                    return (pg, ps)

    except Exception as e:
        gamelog.error('xjw## getPageAndPosByIt exception! %s' % (str(e),))
        return (None, None)

    return (None, None)


def isWithinToday(startSec):
    daySec = getDaySecond()
    dayEndSec = getDaySecond() + const.TIME_INTERVAL_DAY
    if daySec < startSec < dayEndSec:
        return True
    return False


def getArenaLevelForReward(playerLv):
    from cdata import arena_level_data as ALD
    curLevel = 0
    for lId, val in ALD.data.iteritems():
        minLv = val.get('minLv', 0)
        maxLv = val.get('maxLv', 0)
        if minLv == 0 or maxLv == 0:
            continue
        if playerLv >= minLv and playerLv <= maxLv:
            curLevel = lId
            break

    return curLevel


def getTeamEndlessLvType(fbNo):
    from data import team_endless_config_data as TECD
    data = TECD.data.get('fbNos', {})
    for (lvMin, lvMax), fbNos in data.iteritems():
        if fbNo not in fbNos:
            continue
        if lvMax == 79:
            return gametypes.TEAM_ENDLESS_LV_79
        return gametypes.TEAM_ENDLESS_LV_69

    return gametypes.TEAM_ENDLESS_LV_69


def getTeamEndlessLvRange(lvType):
    if lvType == gametypes.TEAM_ENDLESS_LV_79:
        return (70, 89)
    return (69, 69)


def getTeamEndlessFbNoByType(lvType, lv1, lv2):
    from data import team_endless_config_data as TECD
    for fbNo in TECD.data.get('fbTypes', {}).get(lvType, ()):
        if fbNo in TECD.data.get('fbNos', {}).get((lv1, lv2), ()):
            return fbNo

    return 0


def getPlayerMaxXiuweiLv():
    if BigWorld.component in ('base', 'cell'):
        return Netease.playerMaxXiuweiLv
    if BigWorld.component == 'client':
        return getattr(BigWorld.player(), 'playerMaxXiuweiLv', 0)
    return 0


def isFreezeBattleField(fbNo):
    if fbNo in const.FB_NO_BATTLE_FIELD_RACE:
        return False
    if fbNo in const.FB_NO_BATTLE_FIELD_LZS:
        return False
    return True


def checkLearnSkillEnhForQumoJunJie(skillID, part, owner):
    if BigWorld.component == 'client':
        import gameglobal
        if not gameglobal.rds.configData.get('enableSkillXiuLianScore', False):
            return True
    elif not gameconfig.enableSkillXiuLianScore():
        return True
    from data import skill_enhance_data as SKILL_ENH_DATA
    eData = SKILL_ENH_DATA.data.get((skillID, part), {})
    reqJunJie = eData.get('requireJunJieLevel', 0)
    if owner.junJieLv < reqJunJie:
        return False
    reqQumo = eData.get('requireQuMoLevel', 0)
    if owner.qumoLv < reqQumo:
        return False
    return True


def getPrefixName(name, prefixLen):
    if name:
        name = name.decode(defaultEncoding())
        if len(name) > prefixLen:
            name = name[:prefixLen]
        name = name.encode(defaultEncoding())
    return name


def getSkillDelayCastStatParams():
    import gameconfigCommon
    paramsStr = gameconfigCommon.skillDelayCastStatParams()
    paramsList = [ float(x) for x in paramsStr.split(',') ]
    return paramsList


def needDisableUGC():
    import gameconfigCommon
    from data import sys_config_data as SCD
    if gameconfigCommon.enableUGCForceLimit():
        return True
    if gameconfigCommon.enableUGCLimit():
        timeRange = SCD.data.get('ugcLimitTime', ())
        if timeRange and inRange(timeRange, getNow()):
            return True
    return False


def getLessLvWenYinGemId(order, gemData):
    from data import equip_gem_data as EGD
    from cdata import equip_gem_desc_reverse_data as EGDRD
    gemId = 0
    gemType = gemData.get('type', 0)
    gemSubType = gemData.get('subType', 0)
    gemKeys = EGDRD.data.get((gemType, gemSubType), [])
    for gId in gemKeys:
        tmpData = EGD.data.get(gId, {})
        if tmpData and order >= tmpData.get('orderLimit', 0):
            gemId = gId
            break

    return gemId


def isValidIdentification(id):
    if not id or type(id) != str or len(id) != 18:
        return False
    try:
        val = sum((int(id[i]) * const.ID_CARD_WEIGHTS[i] for i in xrange(17))) % 11
        if val == 0:
            checkCode = 1
        elif val == 1:
            checkCode = 0
        elif val == 2:
            checkCode = 'x'
        else:
            checkCode = 12 - val
        if checkCode == 'x':
            if id[17].lower() == checkCode:
                return True
            else:
                return False
        else:
            if int(id[17]) == checkCode:
                return True
            return False
    except Exception as e:
        if BigWorld.component in ('base', 'cell'):
            import gameengine
            gameengine.reportCritical('@xjw isValidIdentification exception %d' % (e,))
        return False

    return False


def getIdentificationCheckCode(ids):
    if not ids or type(ids) != str or len(ids) != 17:
        return None
    try:
        val = sum((int(ids[i]) * const.ID_CARD_WEIGHTS[i] for i in xrange(17))) % 11
        if val == 0:
            checkCode = 1
        elif val == 1:
            checkCode = 0
        elif val == 2:
            checkCode = 'x'
        else:
            checkCode = 12 - val
        return checkCode
    except Exception as e:
        return None


def parseBirthDayFromId(id):
    if not isValidIdentification(id):
        return 0
    return int(id[6:14])


def getFullAge(birthDay, tNow = None):
    if tNow is None:
        tNow = getNow()
    st = time.localtime(tNow)
    year = int(birthDay / 10000)
    month = int(birthDay % 10000 / 100)
    day = birthDay % 100
    age = st.tm_year - year - 1
    if st.tm_mon > month or st.tm_mon == month and st.tm_mday >= day:
        age += 1
    return max(age, 0)


def isHoliday(tNow = None):
    if tNow is None:
        tNow = getNow()
    st = time.localtime(tNow)
    if st.tm_wday in (5, 6):
        return True
    from data import sys_config_data as SCD
    holidays = SCD.data.get('HOLIDAY_DEFINE', ())
    for dStart, dEnd in holidays:
        startArr = dStart.split('-')
        endArr = dEnd.split('-')
        if len(startArr) != len(endArr) or len(startArr) not in (2, 3):
            continue
        if len(startArr) == 3:
            startYear = startArr[0]
            endYear = endArr[0]
        else:
            startYear = str(st.tm_year)
            endYear = str(st.tm_year)
        tStart = getTimeSecondFromStr('.'.join([startYear,
         startArr[-2],
         startArr[-1],
         '0',
         '0',
         '0']))
        tEnd = getTimeSecondFromStr('.'.join([endYear,
         endArr[-2],
         endArr[-1],
         '23',
         '59',
         '59']))
        if tStart < tNow < tEnd:
            return True

    return False


def getTeenTime(tNow = None):
    from data import sys_config_data as SCD
    if isHoliday(tNow):
        return SCD.data.get('PUPIL_DAILY_TIME_HOLIDAY', const.SECONDS_PER_DAY)
    else:
        return SCD.data.get('PUPIL_DAILY_TIME_NORMAL', const.SECONDS_PER_DAY)


def getVisitorTime():
    from data import sys_config_data as SCD
    return SCD.data.get('VISITOR_TOTAL_TIME', 0)


def canEnterPvP():
    if BigWorld.component != 'client':
        return True
    if hasattr(BigWorld, 'getTianyuRunningNum') and gameglobal.rds.configData.get('enableFubenMultiLimit', 0):
        if BigWorld.getTianyuRunningNum() > 2:
            from cdata import game_msg_def_data as GMDD
            BigWorld.player().showGameMsg(GMDD.data.FB_APPLY_MULTI_TIANYU, ())
            return False
    return True


def isCustomeBet(betId):
    import bet
    return betId < bet.AUTOMATIC_BET_ID_MIN


def getRealConsignType(consignType):
    if consignType in gametypes.GUILD_AND_WORLD_CONSIGN_SOURCE_RANGE_EXTRA:
        for cType, rangeVal in gametypes.GUILD_CONSIGN_EXTEND_MAP.iteritems():
            if consignType in xrange(rangeVal[0], rangeVal[1]):
                return cType

        return consignType
    else:
        return consignType


def inRankRange(rankRange, myRank, myRankPct):
    if not rankRange or len(rankRange) != 2:
        return False
    if type(rankRange[0]) == int:
        if myRank < rankRange[0]:
            return False
    elif type(rankRange[0]) == float:
        if myRankPct < rankRange[0]:
            return False
    if type(rankRange[1]) == int:
        if myRank > rankRange[1]:
            return False
    if type(rankRange[1]) == float:
        if myRankPct > rankRange[1]:
            return False
    return True


def getBoundDetailedData(bounds):
    result = []
    if not bounds:
        return []
    minX, minZ, maxX, maxZ = bounds
    result.append([(minX, maxZ), maxX - minX])
    result.append([(maxX, maxZ), maxZ - minZ])
    result.append([(maxX, minZ), maxX - minX])
    result.append([(minX, minZ), maxZ - minZ])
    return result


def getBoundCenterData(bounds):
    if not bounds:
        return []
    minX, minZ, maxX, maxZ = bounds
    centerX = (maxX + minX) / 2.0
    centerZ = (maxZ + minZ) / 2.0
    width = maxX - minX
    height = maxZ - minZ
    return [centerX,
     centerZ,
     width,
     height]


def getBoundCenterDataReverse(bounds):
    if not bounds:
        return []
    minX, minZ, maxX, maxZ = bounds
    centerX = (maxX + minX) / 2.0
    centerZ = (maxZ + minZ) / 2.0
    width = maxX - minX
    height = minZ - maxZ
    return [centerX,
     centerZ,
     width,
     height]


def unescapeHtml(info):
    info = info.replace('&quot;', '\"')
    info = info.replace('&apos;', "\'")
    info = info.replace('&nbsp;', ' ')
    info = info.replace('&nbsp;', ' ')
    info = info.replace('&amp;', '&')
    info = info.replace('&lt;', '<')
    info = info.replace('&gt;', '>')
    return info


def parseNUID(nuid):
    hexStr = hex(nuid)[2:]
    timeStamp = int(hexStr[:8], 16)
    x256 = int(hexStr[8:10], 16)
    pid = int(hexStr[10:14], 16)
    ip = int(hexStr[14:16], 16)
    return (timeStamp,
     ip,
     pid,
     x256)


def parseTimeFromNUID(nuid):
    return int(hex(nuid)[2:10], 16)


def equipSuitIgnoreSuits(suitsCache):
    from cdata import equip_suits_data as EQSD
    ignoreSuitIds = set()
    if not gameconfigCommon.enableEquipSuitReplace():
        return ignoreSuitIds
    for suitId in suitsCache.iterkeys():
        eqsd = EQSD.data.get(suitId, {})
        if not eqsd:
            continue
        parentSuitIds = eqsd.values()[0].get('parentSuitId', [])
        for parentSuitId in parentSuitIds:
            if parentSuitId == suitId or parentSuitId not in suitsCache:
                continue
            checkIgnore = False
            for pNum in EQSD.data.get(parentSuitId, {}).iterkeys():
                if pNum <= suitsCache[parentSuitId]:
                    ignoreSuitIds.add(suitId)
                    checkIgnore = True
                    break

            if checkIgnore:
                break

    return ignoreSuitIds


def getHostName(hostId):
    from data import region_server_config_data as RSCD
    return RSCD.data.get(hostId, {}).get('serverName', '')


def AddInArray(oldArray, data):
    if type(oldArray) is tuple:
        if data not in oldArray:
            tempList = list(oldArray)
            tempList.append(data)
            return tuple(tempList)
    if type(oldArray) is list:
        if data not in oldArray:
            oldArray.append(data)
            return oldArray
    return oldArray


def DelInArray(oldArray, data):
    if type(oldArray) is tuple:
        if data in oldArray:
            tempList = list(oldArray)
            tempList.remove(data)
            return tuple(tempList)
    if type(oldArray) is list:
        if data in oldArray:
            oldArray.remove(data)
            return oldArray
    return oldArray


def genSchoolTransferItemCost(tSchool, schoolTransferInfo):
    from data import school_transfer_config_data as STCD
    if not gameconfigCommon.enableSchoolTransferConditionItemCost():
        return STCD.data.get('schoolTransferItemCost', {}).get(tSchool, None)
    now = getNow()
    lastTransferTime = schoolTransferInfo[2] if schoolTransferInfo else 0
    itemCost = []
    lastDay = (now - lastTransferTime) / const.SECONDS_PER_DAY
    specialCost = STCD.data.get('schoolTransferSpecialItemCost', {}).get(tSchool, None)
    commonCost = None
    for days, cost in sorted(STCD.data.get('schoolTransferCommonItemCost', [])):
        if lastDay >= days:
            commonCost = cost

    if commonCost and specialCost:
        itemCost.append(commonCost)
        itemCost.append(specialCost)
    return itemCost
