#Embedded file name: /WORKSPACE/data/entities/client/hijack.o
import random
import cPickle
import zlib
import BigWorld
import C_ui
import formula
import const
import gameglobal
import utils
import keys
import gamelog
from callbackHelper import Functor
from guis import uiConst
from guis import ui
from gameclass import Singleton
from data import dll_md5_data as DMD
ClientComModule = None

def getClientComModule():
    global ClientComModule
    if ClientComModule == None:
        import clientcom
        ClientComModule = clientcom
    return ClientComModule


HOTFIX_PROCESS = []
CHECK_PROCESS = DMD.data

def on_md5_hotfix(md5data):
    global HOTFIX_PROCESS
    if len(md5data) == 0:
        HOTFIX_PROCESS = []
        return
    HOTFIX_PROCESS = md5data


def hotfix_md5(md5s):
    for i in md5s:
        i = i.strip()
        if len(i) > 0 and i not in CHECK_PROCESS:
            CHECK_PROCESS.append(i)


_checking = False
_dll_checking = False
_window_checking = False
CHECK_SERVERS = []

def on_proc_check(lst, found):
    global _checking
    global _hijack_checking
    if not _checking:
        return
    _hijack_checking = False
    p = BigWorld.player()
    if p == None or p.__class__.__name__ != 'PlayerAvatar' or p.base == None:
        return
    if found:
        key = found[1]
        md5 = found[2]
        path = found[3]
        mac = ''
        try:
            mac = gameglobal.rds.macaddrs[0]
        except:
            mac = ''

        serial, model = BigWorld.get_machine_serial()
        serial = serial.strip().replace(' ', '-')
        model = model.strip().replace(' ', '-')
        hd = serial + model
        extra = {}
        if key:
            extra['key'] = key
        p.base.onScanHackProcess(path, md5, mac, hd, str(extra))


def check_by_proc():
    global _checking
    if gameglobal.gDisableHiJack:
        return
    if _checking:
        return
    _checking = True
    return BigWorld.schedule_proc_code(on_proc_code2)


def check_by_key(keyName):
    global _checking
    if gameglobal.gDisableHiJack:
        return
    if _checking:
        return
    _checking = True
    return BigWorld.schedule_proc_code(Functor(on_proc_code1, keyName))


def on_proc_code1(keyName, lst):
    keyName = keyName.lower()
    keyName = keyName.split('#')
    p = BigWorld.player()
    if p == None or p.__class__.__name__ != 'PlayerAvatar' or p.base == None:
        return
    res = []
    check_proc_keyName(lst, keyName, 0, res)


def check_proc_keyName(lst, keyName, idx, res):
    global _checking
    if not _checking:
        return
    if idx >= len(lst):
        if res:
            send_proc_info(lst, res, 0)
        else:
            on_proc_check(lst, None)
            _checking = False
        return
    mypath, mymd5 = lst[idx]
    for key in keyName:
        mypath = mypath.lower()
        if mypath.find(key) != -1:
            res.append((key, mymd5, mypath))
            break

    BigWorld.callback(0.1, Functor(check_proc_keyName, lst, keyName, idx + 1, res))


def on_proc_code2(lst):
    p = BigWorld.player()
    if p == None or p.__class__.__name__ != 'PlayerAvatar' or p.base == None:
        return
    res = []
    check_proc_info(lst, CHECK_PROCESS + HOTFIX_PROCESS, 0, res)


def check_proc_info(lst, md5list, idx, res):
    global _checking
    if not _checking:
        return
    if idx >= len(lst):
        if res:
            send_proc_info(lst, res, 0)
        else:
            on_proc_check(lst, None)
            _checking = False
        return
    mypath, mymd5 = lst[idx]
    for md5 in md5list:
        mypath = mypath.lower()
        if md5 == mymd5:
            res.append(('', mymd5, mypath))
            break
        elif mypath.find(md5) != -1:
            res.append((md5, mymd5, mypath))
            break

    BigWorld.callback(0.1, Functor(check_proc_info, lst, md5list, idx + 1, res))


def send_proc_info(lst, infolist, idx):
    global _checking
    if not _checking:
        return
    if idx >= len(infolist):
        _checking = False
        return
    key, mypath, mymd5 = infolist[idx]
    on_proc_check(lst, ('',
     key,
     mypath,
     mymd5))
    BigWorld.callback(0.1, Functor(send_proc_info, lst, infolist, idx + 1))


def on_proc_code(uid, lst):
    global _checking
    global _hijack_checking
    _checking = False
    _hijack_checking = False
    code = ''
    for i in lst:
        code += ';' + i[0] + ':' + i[1]

    mac = ''
    try:
        for i in gameglobal.rds.macaddrs:
            mac += i + ';'

    except:
        mac = ''

    info = {}
    info['mac'] = mac
    info['process'] = code
    info['hd'] = gameglobal.rds.clientInfo.harddisk
    blob = zlib.compress(cPickle.dumps(info, -1))
    sendInfoBySection(uid, blob)


def sendInfoBySection(uid, blob):
    p = BigWorld.player()
    if p == None or p.__class__.__name__ != 'PlayerAvatar' or p.base == None or not p.inWorld:
        return
    if len(blob) <= 512:
        p.base.onSendInfoBySection(uid, blob, 1, 1)
    else:
        size = len(blob)
        section = size // 512 + 1
        nowsec = 1
        BigWorld.callback(0.5, Functor(_sendInfoBySection, blob[512:], nowsec, section, uid))
        p.base.onSendInfoBySection(uid, blob[:512], nowsec, section)


def _sendInfoBySection(buff, sec, allsec, uid):
    p = BigWorld.player()
    if p == None or p.__class__.__name__ != 'PlayerAvatar' or p.base == None or not p.inWorld:
        return
    sec += 1
    if sec < allsec:
        BigWorld.callback(0.5, Functor(_sendInfoBySection, buff[512:], sec, allsec, uid))
        p.base.onSendInfoBySection(uid, buff[:512], sec, allsec)
    else:
        p.base.onSendInfoBySection(uid, buff[:512], sec, allsec)


def get_proc_code(op_nuid):
    global _checking
    if gameglobal.gDisableHiJack:
        return
    _checking = True
    return BigWorld.schedule_proc_code(Functor(on_proc_code, op_nuid))


def do_check():
    check_by_proc()


_hijack_checking = False
_hijack_counter = 0
CHECK_INTEVAL = 1800

def hijack_check(stage):
    global _hijack_counter
    global _hijack_checking
    if gameglobal.gDisableHiJack:
        return
    if _hijack_checking:
        return
    _hijack_checking = True
    _hijack_counter += 1
    _checktime = random.uniform(1, 5) * 30
    BigWorld.callback(_checktime, Functor(_hijack_real_check, _hijack_counter))
    _next_time = random.uniform(1, 10) * 30 + CHECK_INTEVAL
    BigWorld.callback(_next_time, Functor(hijack_check, stage + 1))


VK_TAB = 9
VK_F1 = 112
VK_F2 = 113
VK_F3 = 114
VK_F4 = 115
VK_F5 = 116
VK_F6 = 117
VK_F7 = 118
VK_F8 = 119
VK_F9 = 120
VK_F10 = 121
VK_F11 = 122
VK_F12 = 123
VK_F13 = 124
VK_F14 = 125
VK_F15 = 126
VK_F16 = 127
VK_F17 = 128
VK_F18 = 129
VK_F19 = 130
VK_F20 = 131
VK_F21 = 132
VK_F22 = 133
VK_F23 = 134
VK_F24 = 135
VK_1 = 49
VK_2 = 50
VK_3 = 51
VK_4 = 52
VK_5 = 53
VK_6 = 54
VK_7 = 55
VK_8 = 56
VK_9 = 57
VK_0 = 64
CHAR_DICT = {VK_TAB: 'VK_TAB',
 VK_F1: 'VK_F1',
 VK_F2: 'VK_F2',
 VK_F3: 'VK_F3',
 VK_F4: 'VK_F4',
 VK_F5: 'VK_F5',
 VK_F6: 'VK_F6',
 VK_F7: 'VK_F7',
 VK_F8: 'VK_F8',
 VK_F9: 'VK_F9',
 VK_F10: 'VK_F10',
 VK_F11: 'VK_F11',
 VK_F12: 'VK_F12',
 VK_F13: 'VK_F13',
 VK_F14: 'VK_F14',
 VK_F15: 'VK_F15',
 VK_F16: 'VK_F16',
 VK_F17: 'VK_F17',
 VK_F18: 'VK_F18',
 VK_F19: 'VK_F19',
 VK_F20: 'VK_F20',
 VK_F21: 'VK_F21',
 VK_F22: 'VK_F22',
 VK_F23: 'VK_F23',
 VK_F24: 'VK_F24',
 VK_1: 'VK_1',
 VK_2: 'VK_2',
 VK_3: 'VK_3',
 VK_4: 'VK_4',
 VK_5: 'VK_5',
 VK_6: 'VK_6',
 VK_7: 'VK_7',
 VK_8: 'VK_8',
 VK_9: 'VK_9',
 VK_0: 'VK_0'}
WM_KEYDOWN = 256
WM_LBUTTONDOWN = 513
WM_RBUTTONDOWN = 516
WM_CHAR = 258
REPORT_WM = frozenset([WM_KEYDOWN, WM_LBUTTONDOWN, WM_RBUTTONDOWN])
REPORT_INTERVAL = 300
NEXT_REPORT_TIME = 0
CHECK_BGMSG_VER = 0
BG_MSG_DICT = {}

def stop_check_bgmessage():
    global CHECK_BGMSG_VER
    CHECK_BGMSG_VER += 1


last_md5_check_time = 0
MD5_INTV = 3600

def report_bgmessage(message, wParam):
    global BG_MSG_DICT
    opname = ''
    if message in REPORT_WM:
        if message == WM_LBUTTONDOWN:
            opname = '鼠标左键按下'
        elif message == WM_RBUTTONDOWN:
            opname = '鼠标右键按下'
        elif message in (WM_KEYDOWN, WM_CHAR):
            if wParam in CHAR_DICT:
                opname = '%s键按下' % CHAR_DICT.get(wParam, '')
    if opname:
        if opname in BG_MSG_DICT:
            BG_MSG_DICT[opname] += 1
        else:
            BG_MSG_DICT[opname] = 1


def report_bgmsg_dict():
    global BG_MSG_DICT
    if not BG_MSG_DICT:
        return
    p = getClientComModule().getPlayerAvatar()
    if not p:
        return
    bg_msg_report = ''
    for k, v in BG_MSG_DICT.iteritems():
        bg_msg_report += '%s %d次|' % (k, v)

    BG_MSG_DICT = {}
    try:
        mac = gameglobal.rds.macaddrs[0]
    except:
        mac = ''

    serial, model = BigWorld.get_machine_serial()
    serial = serial.strip().replace(' ', '-')
    model = model.strip().replace(' ', '-')
    hd = serial + model
    print '后台发送检测',
    print ('%s %s' % (gameglobal.gServerName, gameglobal.rds.loginUserName),
     '%s %s' % (bg_msg_report, formula.toYearDesc(p.getServerTime())),
     '%s %d %d' % (p.realRoleName, p.lv, p.school),
     '%s %s' % (mac, hd),
     '场景编号%d 坐标%s' % (getattr(p, 'spaceNo', 0), str(p.position)))


def hijack_uncheck():
    global _hijack_counter
    global _hijack_checking
    _hijack_checking = False
    _hijack_counter += 1


_check_count = 0

def _hijack_real_check(counter):
    if not _hijack_checking:
        return
    if counter != _hijack_counter:
        return
    do_check()
    BigWorld.callback(300, sendDllAndMd5)


def sendDllAndMd5():
    global _dll_checking
    return
    if _dll_checking:
        return
    _dll_checking = True
    BigWorld.getProcessModulesMd5(onDllScanFinished)


def onDllScanFinished(lst):
    global DllMd5Counter
    global _dll_checking
    _dll_checking = False
    DllMd5Counter += 1
    unkonwDll = []
    for dllName, dllMd5 in lst:
        dllInfo = '%s-%s' % (dllName, dllMd5)
        unkonwDll.append(dllInfo)

    if not unkonwDll:
        return
    mac = ''
    try:
        for i in gameglobal.rds.macaddrs:
            mac += i + ';'

    except:
        mac = ''

    info = {}
    info['mac'] = mac
    info['dll'] = str(unkonwDll)
    blob = zlib.compress(cPickle.dumps(info, -1))
    sendInfoBySection(const.HIJACK_DLL_MD5 + DllMd5Counter, blob)


WILD_MONSTER_KILLED = 0
LX_MONSTER_KILLED = 0

def add_monster_kill_record():
    pass


def send_monster_kill_record():
    pass


def clear_moster_kill_record():
    global LX_MONSTER_KILLED
    global WILD_MONSTER_KILLED
    WILD_MONSTER_KILLED = 0
    LX_MONSTER_KILLED = 0


MouseChecking = False
MouseCheckingCounter = 0

def checkMousePos(interval, totalTime):
    global MouseCheckingCounter
    global MouseChecking
    if MouseChecking:
        return
    MouseChecking = True
    MouseCheckingCounter += 1
    res = []
    count = int(totalTime / interval) + 1
    startTime = BigWorld.player().getServerTime()
    _checkMousePos(res, 0, count, interval, startTime)


def _checkMousePos(res, index, total, interval, startTime):
    global MouseChecking
    if index >= total:
        MouseChecking = False
        info = {}
        info['startTime'] = startTime
        info['interval'] = interval
        info['array'] = res
        info['screenState'] = BigWorld.getScreenState()
        info['screenSize'] = BigWorld.getScreenSize()
        blob = zlib.compress(cPickle.dumps(info, -1))
        sendInfoBySection(const.HIJACK_MOUSE_POS_GAP + MouseCheckingCounter, blob)
    else:
        pos = C_ui.get_cursor_pos()
        isDown = BigWorld.getKeyDownState(keys.KEY_MOUSE0, 0)
        res.append((pos[0], pos[1], isDown))
        BigWorld.callback(interval, Functor(_checkMousePos, res, index + 1, total, interval, startTime))


TitleCheckingCounter = 0
DllMd5Counter = 0

def unicode2gbk(str):
    try:
        str.decode('utf-8').encode(utils.defaultEncoding())
    except:
        return str

    return str


def checkWindowTitle():
    global TitleCheckingCounter
    global _window_checking
    if _window_checking:
        return
    _window_checking = True
    TitleCheckingCounter += 1
    BigWorld.get_window_titles(afterCheckWindows)


def afterCheckWindows(windows):
    _windows = []
    for item in windows:
        if item not in _windows:
            _windows.append(unicode2gbk(item))

    BigWorld.callback(1, Functor(checkWindowCaption, _windows))


def checkWindowCaption(_windows):
    BigWorld.schedule_proc_captions(Functor(afterCheckWindowCaption, _windows))


def afterCheckWindowCaption(windows, windowCaptions):
    global _window_checking
    _windowCaptions = []
    for caption in windowCaptions:
        _caption = []
        pid, exeName = caption[0]
        exeName = unicode2gbk(exeName)
        _caption.append((pid, exeName))
        for windowName in caption[1:]:
            _caption.append(unicode2gbk(windowName))

        _windowCaptions.append(_caption)

    ret = {'windows': windows,
     'windowCaptions': _windowCaptions}
    blob = zlib.compress(cPickle.dumps(ret, -1))
    sendInfoBySection(const.HIJACK_WINDOW_TITLE_GAP + TitleCheckingCounter, blob)
    _window_checking = False


class UILogRecorder(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.logs = []
        self.statisticsLog = {}

    def clear(self):
        self.logs = []
        self.statisticsLog = {}

    @ui.callFilter(0.5, False)
    def addLog(self, type, *arg):
        self.addLogNoFilter(type, *arg)

    def addLogNoFilter(self, type, *arg):
        t = utils.getNow()
        self.logs.append((t, type) + arg)
        if len(self.logs) + len(self.statisticsLog) >= 1000:
            self.sendLogs()

    def addOpenLog(self, *arg):
        return
        self.addLog(uiConst.LOG_UI_OPEN, *arg)

    def addCloseLog(self, *arg):
        return
        self.addLog(uiConst.LOG_UI_CLOSE, *arg)

    def addItemLog(self, *arg):
        return
        self.addLog(uiConst.LOG_UI_ITEM, *arg)

    def addPathLog(self, *arg):
        return
        self.addLog(uiConst.LOG_UI_PATHFINDING, *arg)

    def addFlyLog(self, *arg):
        return
        self.addLog(uiConst.LOG_UI_FLY, *arg)

    def addClickLog(self, *arg):
        return
        self.addLog(uiConst.LOG_UI_CLICK, *arg)

    def addWidgetClickLog(self, *arg):
        return
        self.addLog(uiConst.LOG_UI_WIDGET_CLICK, *arg)

    def addUIOpenCntLog(self, wid):
        openCntStat = self.statisticsLog.setdefault(uiConst.LOG_UI_OPEN_CNT, {})
        openCntStat[str(wid)] = openCntStat.get(str(wid), 0) + 1

    def addWidgetShowTimeLog(self, *arg):
        return
        self.addLog(uiConst.LOG_UI_WIDGET_SHOW_TIME, *arg)

    def addWidgetOpenCntLog(self, wid):
        return
        openCntStat = self.statisticsLog.setdefault(uiConst.LOG_UI_WIDGET_OPEN_CNT, {})
        openCntStat[str(wid)] = openCntStat.get(str(wid), 0) + 1

    def addModelCntLog(self, modelMark):
        openCntStat = self.statisticsLog.setdefault(uiConst.LOG_UI_MODEL_LOAD_CNT, {})
        openCntStat[modelMark[0]][modelMark[1]] = openCntStat.setdefault(modelMark[0], {}).get(modelMark[1], 0) + 1

    def addEffectCntLog(self, effectId):
        openCntStat = self.statisticsLog.setdefault(uiConst.LOG_UI_EFFECT_LOAD_CNT, {})
        openCntStat[str(effectId)] = openCntStat.get(str(effectId), 0) + 1

    def addMapCntLog(self, mapId):
        openCntStat = self.statisticsLog.setdefault(uiConst.LOG_UI_MAP_LOAD_CNT, {})
        openCntStat[str(mapId)] = openCntStat.get(str(mapId), 0) + 1

    def sendLogs(self):
        if self.statisticsLog:
            for k, v in self.statisticsLog.iteritems():
                self.addLogNoFilter(k, str(v))

            self.statisticsLog = {}
        if self.logs:
            blob = zlib.compress(cPickle.dumps(self.logs, -1))
            sendInfoBySection(const.HIJACK_UI_CLICK, blob)
            self.logs = []

    def getRecord(self):
        return self.logs


global _check_count ## Warning: Unused global
