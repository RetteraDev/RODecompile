#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\helpers/taboo.o
if __name__ == '__main__':
    import sys
    sys.path.append('../../common')
import re
import cPickle
import regexPkl
import cStringIO
import gzip
import tabooPatternData
import utils
from guis import ui
from tabooData import originWordsA
from tabooData import originWordsB
from tabooData import originWordsBWorld
from tabooData import originWordsBSingle
from tabooData import originWordsBNewbie
from tabooData import originWordsBAllLv
from tabooData import originWordsC
from tabooData import originWordsName
from tabooData import checkPathWaiguaList
from tabooData import autoPushSystemWords
TABOO_PINGBI = 'PB'
TABOO_TIHUAN = 'TH'
TABOO_TIANXIA = 'TX'
TABOO_MIYU = 'MY'
TABOO_DIDENGJI = 'NB'
TABOO_SANLEI = 'SL'
TABOO_QUANDENGJI = 'AB'
TABOO_MINGMING = 'MM'
TABOO_CHECKPATHWG = 'CPWG'
TABOO_TUISONG = 'TS'
TABOO_ALL = (TABOO_PINGBI,
 TABOO_TIHUAN,
 TABOO_TIANXIA,
 TABOO_MIYU,
 TABOO_DIDENGJI,
 TABOO_SANLEI,
 TABOO_QUANDENGJI,
 TABOO_MINGMING,
 TABOO_CHECKPATHWG,
 TABOO_TUISONG)
TS_HELP = 1
TS_MINLV = 2
TS_MAXLV = 3
TS_VIP = 4
TS_SCHOOL = 5
TS_SCENE = 6
TS_MIN_SCORE = 7
TS_MAX_SCORE = 8
TS_SHOW = 9
TS_TYPE = 10
TS_LINK = 11
compileReady = False
allKeywords = []
addKeywords = []
delKeywords = []

@ui.callNoUrgent()
def keywordToCheck(keywords):
    global compileReady
    global allKeywords
    if not keywords:
        clearKeywords()
        return
    allKeywords = []
    for kw in keywords:
        try:
            posType = kw.find(':')
            type = kw[:posType]
            kw = kw[posType + 1:]
            posOp = kw.find(':')
            op = kw[:posOp]
            kw = kw[posOp + 1:]
            posExtra = kw.find('extra:')
            if posExtra != -1:
                tt = kw[:posExtra]
                extra = kw[posExtra + 6:]
            else:
                tt = kw
                extra = ''
            tt = tt.decode(utils.defaultEncoding()).encode('utf8').replace('\\xe4\\xb8\\x80-\\xe9\\xbe\\xa5', '一-龥')
            extra = extra.decode(utils.defaultEncoding()).encode('utf8').replace('\\xe4\\xb8\\x80-\\xe9\\xbe\\xa5', '一-龥')
            keyword = unicode(tt, 'utf8', 'replace')
            allKeywords.append((type,
             op,
             keyword,
             extra))
        except:
            continue

    if compileReady:
        updateKeywords()


def updateKeywords():
    global delKeywords
    global addKeywords
    global tabooDataDict
    for type, op, keyword, extra in allKeywords:
        try:
            if type not in tabooDataDict and type not in TABOO_ALL:
                continue
            data = tabooDataDict.setdefault(type, {})
            if op == 'add':
                if keyword in data:
                    data[keyword][0] = 1
                else:
                    if type == TABOO_TUISONG:
                        data[keyword] = [1, re.compile(keyword, re.U), createExtraInfo(extra)]
                    else:
                        data[keyword] = [1, re.compile(keyword, re.U)]
                    addKeywords.append((type, op, keyword))
            elif keyword in data:
                data[keyword][0] = 0
                delKeywords.append((type, op, keyword))
        except:
            continue


def clearKeywords():
    global delKeywords
    global addKeywords
    for type, op, keyword in delKeywords:
        data = tabooDataDict.setdefault(type, {})
        if not data:
            continue
        if keyword in data:
            data[keyword][0] = 1

    delKeywords = []
    for type, op, keyword in addKeywords:
        data = tabooDataDict.setdefault(type, {})
        if not data:
            continue
        if keyword in data:
            data[keyword][0] = 0

    addKeywords = []


def createExtraInfo(extra):
    extralist = []
    extralist.append((TS_HELP, extra.find('help:'), len('help:')))
    extralist.append((TS_MINLV, extra.find('minLv:'), len('minLv:')))
    extralist.append((TS_MAXLV, extra.find('maxLv:'), len('maxLv:')))
    extralist.append((TS_VIP, extra.find('vip:'), len('vip:')))
    extralist.append((TS_SCHOOL, extra.find('school:'), len('school:')))
    extralist.append((TS_SCENE, extra.find('scene:'), len('scene:')))
    extralist.append((TS_MIN_SCORE, extra.find('minScore:'), len('minScore:')))
    extralist.append((TS_MAX_SCORE, extra.find('maxScore:'), len('maxScore:')))
    extralist.append((TS_SHOW, extra.find('show:'), len('show:')))
    extralist.append((TS_TYPE, extra.find('type:'), len('type:')))
    extralist.append((TS_LINK, extra.find('link:'), len('link:')))
    extralist.sort(key=lambda x: x[1], reverse=False)
    info = {}
    extralistLen = len(extralist)
    for i in xrange(extralistLen):
        if extralist[i][1] == -1:
            continue
        if i + 1 >= extralistLen:
            value = extra[extralist[i][1] + extralist[i][2]:]
        else:
            value = extra[extralist[i][1] + extralist[i][2]:extralist[i + 1][1]]
        if extralist[i][0] == TS_HELP:
            info['helpStr'] = value
        elif extralist[i][0] == TS_MINLV:
            info['minLv'] = int(value)
        elif extralist[i][0] == TS_MAXLV:
            info['maxLv'] = int(value)
        elif extralist[i][0] == TS_VIP:
            info['vip'] = int(value)
        elif extralist[i][0] == TS_SCHOOL:
            info['school'] = int(value)
        elif extralist[i][0] == TS_SCENE:
            info['scene'] = value
        elif extralist[i][0] == TS_MIN_SCORE:
            info['minScore'] = int(value)
        elif extralist[i][0] == TS_MAX_SCORE:
            info['maxScore'] = int(value)
        elif extralist[i][0] == TS_SHOW:
            info['showStr'] = value
        elif extralist[i][0] == TS_TYPE:
            info['type'] = int(value)
        elif extralist[i][0] == TS_LINK:
            info['link'] = value

    return info


tabooDataDict = {}
disWordsA = []
disWordsB = []
disWordsC = []
disWordsBWorld = []
disWordsBSingle = []
disWordsBNewbie = []
itemFilter = None
codeFilter = None
emoteFilter = None
disturbFilter = None
tabooFilter = None
rplStr = None

def compileTask():
    global tabooDataDict
    global originWordsBNewbie
    global originWordsBSingle
    global itemFilter
    global checkPathWaiguaList
    global originWordsBWorld
    global rplStr
    global originWordsC
    global originWordsB
    global originWordsA
    global originWordsName
    global emoteFilter
    global disturbFilter
    global compileReady
    global originWordsBAllLv
    global codeFilter
    global autoPushSystemWords
    itemFilter = re.compile('(#\\[.{8}\\])(.+?)(#\\[0\\])', re.DOTALL)
    codeFilter = re.compile('(#c\\([0-9]+?\\))(.+?)(#c\\(0\\))', re.DOTALL)
    emoteFilter = re.compile(unicode('#[rzkbwng]|#c[0-9a-f]{0,6}|#[0-9]{0,3}', 'mbcs', 'replace'), re.U)
    disturbFilter = re.compile(unicode('\\W', 'mbcs', 'replace'), re.U)
    rplStr = unicode('#78', 'mbcs', 'replace')
    tabooDataDict = {}
    tdict = tabooDataDict.setdefault(TABOO_TIANXIA, {})
    for item in originWordsBWorld:
        item = unicode(item, 'utf8', 'replace')
        tdict[item] = [1, regexPkl.compileHalfAndPkl(item, re.U)]

    originWordsBWorld = []
    tdict = tabooDataDict.setdefault(TABOO_MIYU, {})
    for item in originWordsBSingle:
        item = unicode(item, 'utf8', 'replace')
        tdict[item] = [1, regexPkl.compileHalfAndPkl(item, re.U)]

    originWordsBSingle = []
    tdict = tabooDataDict.setdefault(TABOO_DIDENGJI, {})
    for item in originWordsBNewbie:
        item = unicode(item, 'utf8', 'replace')
        tdict[item] = [1, regexPkl.compileHalfAndPkl(item, re.U)]

    originWordsBNewbie = []
    tdict = tabooDataDict.setdefault(TABOO_QUANDENGJI, {})
    for item in originWordsBAllLv:
        item = unicode(item, 'utf8', 'replace')
        tdict[item] = [1, regexPkl.compileHalfAndPkl(item, re.U)]

    originWordsBAllLv = []
    tdict = tabooDataDict.setdefault(TABOO_PINGBI, {})
    for item in originWordsA:
        item = unicode(item, 'utf8', 'replace')
        tdict[item] = [1, regexPkl.compileHalfAndPkl(item, re.U)]

    originWordsA = []
    tdict = tabooDataDict.setdefault(TABOO_TIHUAN, {})
    for item in originWordsB:
        item = unicode(item, 'utf8', 'replace')
        tdict[item] = [1, regexPkl.compileHalfAndPkl(item, re.U)]

    originWordsB = []
    tdict = tabooDataDict.setdefault(TABOO_SANLEI, {})
    for item in originWordsC:
        item = unicode(item, 'utf8', 'replace')
        tdict[item] = [1, regexPkl.compileHalfAndPkl(item, re.U)]

    originWordsC = []
    tdict = tabooDataDict.setdefault(TABOO_MINGMING, {})
    for item in originWordsName:
        item = unicode(item, 'utf8', 'replace')
        tdict[item] = [1, regexPkl.compileHalfAndPkl(item, re.U)]

    originWordsName = []
    tdict = tabooDataDict.setdefault(TABOO_CHECKPATHWG, {})
    for item in checkPathWaiguaList:
        item = unicode(item, 'utf8', 'replace')
        tdict[item] = [1, regexPkl.compileHalfAndPkl(item, re.U)]

    checkPathWaiguaList = []
    tdict = tabooDataDict.setdefault(TABOO_TUISONG, {})
    for item in autoPushSystemWords:
        posExtra = item.find('extra:')
        if posExtra != -1:
            extra = item[posExtra + 6:]
            item = item[:posExtra]
        else:
            extra = ''
        item = unicode(item, 'utf8', 'replace')
        tdict[item] = [1, regexPkl.compileHalfAndPkl(item, re.U), createExtraInfo(extra)]

    autoPushSystemWords = []
    compileReady = True
    dumpstr = cPickle.dumps(tabooDataDict, 2)
    sio = cStringIO.StringIO()
    gzfile = gzip.GzipFile(fileobj=sio, mode='wb')
    gzfile.write(dumpstr)
    gzfile.close()
    f = open('tabooPatternData_new.py', 'wb')
    f.write('# -*-coding: utf-8 -*-\n\n')
    write_str = 'PATTERN_DATA_DICT = {\"tabooDataDict\":' + sio.getvalue().__repr__() + '}'
    f.write(write_str)
    sio.close()
    f.close()
    updateKeywords()
    print 'compileTask done'


def loadCompiledPattern():
    global originWordsC
    global originWordsB
    global originWordsA
    global originWordsName
    global tabooPatternData
    global emoteFilter
    global tabooDataDict
    global tabooFilter
    global compileReady
    global originWordsBNewbie
    global originWordsBSingle
    global itemFilter
    global originWordsBAllLv
    global checkPathWaiguaList
    global disturbFilter
    global originWordsBWorld
    global codeFilter
    global rplStr
    global autoPushSystemWords
    itemFilter = re.compile('(#\\[.{8}\\])(.+?)(#\\[0\\])', re.DOTALL)
    codeFilter = re.compile('(#c\\([0-9]+?\\))(.+?)(#c\\(0\\))', re.DOTALL)
    emoteFilter = re.compile(unicode('#[rzkbwng]|#c[0-9a-f]{0,6}|#[0-9]{0,3}', 'utf8', 'replace'), re.U)
    disturbFilter = re.compile(unicode('\\W', 'utf8', 'replace'), re.U)
    tabooFilter = re.compile(unicode('<FONT COLOR=\"#.{6}\">|</FONT>|<A HREF=\"event:(item|ret|achvid|task)\\d+\">|</[AU]>|<[AU]>|\"><[AU]>|<A HREF=\"event:achvid\\d+:time\\d+/\\d+/\\d+:|\\$\\d{2,3}|&lt;FONT COLOR=&quot;#.{6}&quot;&gt;|&lt;A HREF=&quot;event:achvid\\d+:time\\d+/\\d+/\\d+:|&quot;&gt;&lt;U&gt;|&lt;/U&gt;&lt;/A&gt;|&lt;/FONT&gt;', 'mbcs', 'replace'), re.U)
    rplStr = unicode('#78', 'utf8', 'replace')
    tabooDataDict = {}
    sio = cStringIO.StringIO(tabooPatternData.PATTERN_DATA_DICT['tabooDataDict'])
    gzfile = gzip.GzipFile(fileobj=sio)
    deflate_data = gzfile.read()
    gzfile.close()
    sio.close()
    tabooDataDict = cPickle.loads(deflate_data)
    for taboo_name, taboo_dict in tabooDataDict.iteritems():
        for item, item_lst in taboo_dict.iteritems():
            item_lst[1] = regexPkl.unpklAndFulfillOtherHalfCompile(item_lst[1])

    originWordsBWorld = []
    originWordsBSingle = []
    originWordsBNewbie = []
    originWordsBAllLv = []
    originWordsA = []
    originWordsB = []
    originWordsC = []
    originWordsName = []
    checkPathWaiguaList = []
    autoPushSystemWords = []
    compileReady = True
    updateKeywords()
    import sys
    del tabooPatternData
    delModules = ['helpers.tabooPatternData', 'helpers.tabooData']
    for m in delModules:
        if m in sys.modules:
            del sys.modules[m]


def checkDisbWord(msg):
    what = msg
    what = unicode(what, utils.defaultEncoding(), 'replace')
    what = re.sub(tabooFilter, '', what)
    bwhat = what
    for index, (flag, pattern) in enumerate(tabooDataDict.get(TABOO_PINGBI, {}).itervalues()):
        if not flag:
            continue
        if re.search(pattern, what):
            return (False, msg)

    for index, (_str, (flag, pattern)) in enumerate(tabooDataDict.get(TABOO_TIHUAN, {}).iteritems()):
        if not flag:
            continue
        for g in re.finditer(pattern, bwhat):
            msg = msg.replace(g.group(0).encode(utils.defaultEncoding()), '*')

    return (True, msg)


def checkDisbWordEx(msg):
    what = msg
    what = unicode(what, utils.defaultEncoding(), 'replace')
    what = re.sub(tabooFilter, '', what)
    bwhat = what
    bReplace = False
    for index, (flag, pattern) in enumerate(tabooDataDict.get(TABOO_PINGBI, {}).itervalues()):
        if not flag:
            continue
        if re.search(pattern, what):
            return (False, msg, bReplace)

    for index, (_str, (flag, pattern)) in enumerate(tabooDataDict.get(TABOO_TIHUAN, {}).iteritems()):
        if not flag:
            continue
        for g in re.finditer(pattern, bwhat):
            msg = msg.replace(g.group(0).encode(utils.defaultEncoding()), '*')
            bReplace = True

    return (True, msg, bReplace)


def checkDisbWordNoReplace(msg):
    what = msg
    what = unicode(what, utils.defaultEncoding(), 'replace')
    what = re.sub(tabooFilter, '', what)
    for index, (flag, pattern) in enumerate(tabooDataDict.get(TABOO_PINGBI, {}).itervalues()):
        if not flag:
            continue
        if re.search(pattern, what):
            return False

    for index, (_str, (flag, pattern)) in enumerate(tabooDataDict.get(TABOO_TIHUAN, {}).iteritems()):
        if not flag:
            continue
        if re.search(pattern, what):
            return False

    return True


def checkMonitorWord(msg):
    what = msg
    what = unicode(what, utils.defaultEncoding(), 'replace')
    what = re.sub(tabooFilter, '', what)
    for index, (flag, pattern) in enumerate(tabooDataDict.get(TABOO_SANLEI, {}).itervalues()):
        if not flag:
            continue
        if re.search(pattern, what):
            return True

    return False


def checkBWorld(msg):
    what = msg
    what = unicode(what, utils.defaultEncoding(), 'replace')
    what = re.sub(tabooFilter, '', what)
    for index, (_str, (flag, pattern)) in enumerate(tabooDataDict.get(TABOO_TIANXIA, {}).iteritems()):
        if not flag:
            continue
        if re.search(pattern, what):
            return (False, msg)

    return (True, msg)


def checkBSingle(msg):
    what = msg
    what = unicode(what, utils.defaultEncoding(), 'replace')
    what = re.sub(tabooFilter, '', what)
    for index, (_str, (flag, pattern)) in enumerate(tabooDataDict.get(TABOO_MIYU, {}).iteritems()):
        if not flag:
            continue
        if re.search(pattern, what):
            return (False, msg)

    return (True, msg)


def checkBNewbie(msg):
    what = msg
    what = unicode(what, utils.defaultEncoding(), 'replace')
    what = re.sub(tabooFilter, '', what)
    for index, (_str, (flag, pattern)) in enumerate(tabooDataDict.get(TABOO_DIDENGJI, {}).iteritems()):
        if not flag:
            continue
        if re.search(pattern, what):
            return (False, msg)

    return (True, msg)


def checkAllLvDisWorld(msg):
    what = msg
    what = unicode(what, utils.defaultEncoding(), 'replace')
    what = re.sub(tabooFilter, '', what)
    for index, (_str, (flag, pattern)) in enumerate(tabooDataDict.get(TABOO_QUANDENGJI, {}).iteritems()):
        if not flag:
            continue
        if re.search(pattern, what):
            return (False, msg)

    return (True, msg)


def checkNameDisWord(msg):
    what = msg
    what = unicode(what, utils.defaultEncoding(), 'replace')
    what = re.sub(tabooFilter, '', what)
    for index, (flag, pattern) in enumerate(tabooDataDict.get(TABOO_MINGMING, {}).itervalues()):
        if not flag:
            continue
        if re.search(pattern, what):
            return (False, msg)

    return (True, msg)


def checkNameDisWordWithReplace(msg):
    what = msg
    what = re.sub(itemFilter, '', what)
    what = re.sub(codeFilter, '', what)
    what = unicode(what, utils.defaultEncoding(), 'replace')
    bwhat = what
    findDis = False
    for index, (flag, pattern) in enumerate(tabooDataDict.get(TABOO_MINGMING, {}).itervalues()):
        if not flag:
            continue
        for g in re.finditer(pattern, bwhat):
            msg = msg.replace(g.group(0).encode(utils.defaultEncoding()), '*')
            findDis = True

    return (findDis, msg)


def checkPathWaigua(msg):
    what = msg
    what = unicode(what, utils.defaultEncoding(), 'replace')
    for index, (flag, pattern) in enumerate(tabooDataDict.get(TABOO_CHECKPATHWG, {}).itervalues()):
        if not flag:
            continue
        if re.search(pattern, what):
            return (False, msg)

    return (True, msg)


def checkPingBiWord(msg, isReplace = True):
    what = msg
    what = unicode(what, utils.defaultEncoding(), 'replace')
    what = re.sub(tabooFilter, '', what)
    bwhat = what
    for index, (_str, (flag, pattern)) in enumerate(tabooDataDict.get(TABOO_TIHUAN, {}).iteritems()):
        if not flag:
            continue
        if not isReplace:
            if re.search(pattern, what):
                return (False, msg)
        else:
            for g in re.finditer(pattern, bwhat):
                msg = msg.replace(g.group(0).encode(utils.defaultEncoding()), '*')

    return (True, msg)


def checkTiHuanWord(msg, isReplace = True):
    what = msg
    what = unicode(what, utils.defaultEncoding(), 'replace')
    what = re.sub(tabooFilter, '', what)
    bwhat = what
    for index, (flag, pattern) in enumerate(tabooDataDict.get(TABOO_PINGBI, {}).itervalues()):
        if not flag:
            continue
        if not isReplace:
            if re.search(pattern, what):
                return (False, msg)
        else:
            for g in re.finditer(pattern, bwhat):
                msg = msg.replace(g.group(0).encode(utils.defaultEncoding()), '*')

    return (True, msg)


def checkAutoPushSystemWords(msg, p):
    import utils
    import const
    from helpers import navigator
    what = msg
    what = unicode(what, utils.defaultEncoding(), 'replace')
    what = re.sub(tabooFilter, '', what)
    for index, (flag, pattern, extra) in enumerate(tabooDataDict.get(TABOO_TUISONG, {}).itervalues()):
        if not flag:
            continue
        if p.realLv < extra.get('minLv', 0):
            continue
        if p.realLv > extra.get('maxLv', 1000):
            continue
        if utils.getVipGrade(p) < extra.get('vip', 0):
            continue
        school = extra.get('school', 0)
        if school and school != p.school:
            continue
        scene = extra.get('scene', '')
        if scene and scene != navigator.getPhaseMappingNameBySpaceNo(p.spaceNo):
            continue
        allScore = p.combatScoreList[const.COMBAT_SCORE]
        if allScore < extra.get('minScore', 0):
            continue
        if allScore > extra.get('maxScore', 100000000):
            continue
        if re.search(pattern, what):
            helpStr = extra.get('helpStr', '').decode('utf8').encode(utils.defaultEncoding())
            showStr = extra.get('showStr', '').decode('utf8').encode(utils.defaultEncoding())
            type = extra.get('type', 0)
            link = extra.get('link', '').decode('utf8').encode(utils.defaultEncoding())
            return (True,
             helpStr,
             showStr,
             type,
             link)

    return (False,
     '',
     '',
     0,
     '')


if __name__ == '__main__':
    from tabooTool import processTabooData
    processTabooData()
else:
    loadCompiledPattern()
global disWordsBNewbie ## Warning: Unused global
global disWordsBSingle ## Warning: Unused global
global disWordsBWorld ## Warning: Unused global
global disWordsA ## Warning: Unused global
global disWordsB ## Warning: Unused global
global disWordsC ## Warning: Unused global
