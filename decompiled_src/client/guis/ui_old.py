#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/ui_old.o
from gamestrings import gameStrings
import BigWorld
import C_ui
import cursor
import decorator
import gameglobal
import gamelog
import const
import utils
import time
import gametypes
from callbackHelper import Functor
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD
from data import item_synthesize_data as ISD
from cdata import item_synthesize_set_data as ISSD
ui_path = 'gui'
callList = []
callTimeList = {}
scenarioFuncCache = []
widEvent = {}
calledMethodMap = {}
callIntervalMethodMap = {}
checkWidFuncDict = {}

def checkItemMixNeedHint(pg, pp):

    def func(method, *args):
        page = args[pg]
        pos = args[pp]
        p = BigWorld.player()
        it = p.inv.getQuickVal(page, pos)
        if it:
            if it.bindType != 1:
                if checkMaterialNeedBind(it):
                    txtShow = GMD.data.get(GMDD.data.ITEM_MIX_NEED_HINT, {}).get('text', gameStrings.TEXT_UI_42)
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(txtShow, Functor(method, *args), msgType='mixHintBind', isShowCheckBox=True)
                else:
                    method(*args)
            else:
                method(*args)

    return decorator.decorator(func)


def checkMaterialNeedBind(item):
    synthesizeData = ISD.data.get(item.getParentId(), None)
    if synthesizeData:
        results = synthesizeData.get('result')
        if results:
            for result in results:
                _, itemConsume, itemCunsumeSetId, res, resSetId = result
                if itemConsume:
                    for itemSearchType, itemId, num in itemConsume:
                        if itemId:
                            if checkItemHasBind(itemId, itemSearchType):
                                return True

                if itemCunsumeSetId:
                    sd = ISSD.data.get(itemCunsumeSetId, None)
                    for d in sd:
                        itemId = d.get('itemId', 0)
                        if itemId == 0:
                            continue
                        itemSearchType = d.get('itemSearchType', gametypes.ITEM_MIX_TYPE_NO_PARENT)
                        if checkItemHasBind(itemId, itemSearchType):
                            return True

            return False
        else:
            return False
    else:
        return False


def checkItemHasBind(itemId, searchType):
    if searchType == gametypes.ITEM_MIX_TYPE_NO_PARENT:
        enableParentCheck = False
    else:
        enableParentCheck = True
    p = BigWorld.player()
    if p.inv.countItemInPages(itemId, enableParentCheck=enableParentCheck, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_ONLY):
        return True
    return False


def checkEquipCanReturn(itemParamPos = 0, showMsgID = GMDD.data.LIFE_SKILL_SOC_PROP2):

    def func(method, *args):
        if itemParamPos == const.LAST_PARAMS:
            length = len(args)
            pos = length - 1
        else:
            pos = itemParamPos
        equip = args[pos]
        if not equip:
            return None
        canReturn = equip.canReturnToShop()
        if canReturn:
            txt = GMD.data.get(showMsgID, {}).get('text', gameStrings.TEXT_ACTIVITY_976_1)
            txt2 = GMD.data.get(GMDD.data.CAN_CHECK_RETURN_BASE, {}).get('text', gameStrings.TEXT_UI_101)
            txtShow = txt2 % (txt, txt)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(txtShow, Functor(method, *args))
            return None
        method(*args)

    return decorator.decorator(func)


def looseGroupTradeConfirm(itemPos = 0, operMsgId = GMDD.data.ACTIVE_STAR_LV):

    def func(method, *args):
        item = None
        item2 = None
        if type(itemPos) == list or type(itemPos) == tuple:
            if len(itemPos) < 2:
                return
            if len(itemPos) >= 2:
                page = args[itemPos[0]]
                pos = args[itemPos[1]]
                item = BigWorld.player().inv.getQuickVal(page, pos)
            if len(itemPos) >= 4:
                page = args[itemPos[2]]
                pos = args[itemPos[3]]
                item2 = BigWorld.player().inv.getQuickVal(page, pos)
        else:
            pos = len(args) - 1 if itemPos == const.LAST_PARAMS else itemPos
            item = args[pos]
        if not item:
            return
        enable = gameglobal.rds.configData.get('enableLooseGroupTradeConfirm', False)
        flag1 = item and hasattr(item, 'canGroupTrade') and item.canGroupTrade()
        flag2 = item2 and hasattr(item2, 'canGroupTrade') and item2.canGroupTrade()
        flag = flag1 or flag2
        if enable and flag:
            operStr = GMD.data.get(operMsgId, {}).get('text', gameStrings.TEXT_ACTIVITY_976_1)
            warn = GMD.data.get(GMDD.data.BIND_ITEM_CHECK_WARNING, {}).get('text', gameStrings.TEXT_UI_143)
            strShow = warn % (operStr, operStr)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(strShow, Functor(method, *args))
        else:
            method(*args)

    return decorator.decorator(func)


def checkEquipCanReturnByPos(itemPosParamPos = [0, 1], showMsgID = GMDD.data.LIFE_SKILL_SOC_PROP2):

    def func(method, *args):
        equip = None
        if type(itemPosParamPos) == list or type(itemPosParamPos) == tuple:
            page = args[itemPosParamPos[0]]
            pos = args[itemPosParamPos[1]]
            equip = BigWorld.player().inv.getQuickVal(page, pos)
        else:
            pos = len(args) - 1 if itemPosParamPos == const.LAST_PARAMS else itemPosParamPos
            equip = args[pos]
        if not equip:
            return
        canReturn = equip.canReturnToShop()
        if canReturn:
            txt = GMD.data.get(showMsgID, {}).get('text', gameStrings.TEXT_ACTIVITY_976_1)
            txt2 = GMD.data.get(GMDD.data.CAN_CHECK_RETURN_BASE, {}).get('text', gameStrings.TEXT_UI_101)
            txtShow = txt2 % (txt, txt)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(txtShow, Functor(method, *args))
            return
        method(*args)

    return decorator.decorator(func)


def callFilter(time = 0, showMsg = True):

    def func(method, *args):
        if method not in callList:
            callList.append(method)
            BigWorld.callback(time, Functor(delFuncFromList, method))
            return method(*args)
        else:
            showMsg and gameglobal.rds.ui.systemTips.show(gameStrings.TEXT_CLIENTUTILS_90)
            return None

    return decorator.decorator(func)


def checkItemIsLock(itemPosParamPos = [0, 1]):

    def func(method, *args):
        page = args[itemPosParamPos[0]]
        pos = args[itemPosParamPos[1]]
        item = BigWorld.player().inv.getQuickVal(page, pos)
        if item:
            if item.hasLatch():
                BigWorld.player().showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
                return
        else:
            return
        return method(*args)

    return decorator.decorator(func)


def checkInventoryLock():

    def func(method, *args):
        if gameglobal.rds.configData.get('enableInventoryLock', False):
            params = [method]
            for v in args:
                params.append(v)

            BigWorld.player().getCipher(onGetCipherCallBack, tuple(params))
        else:
            method(*args)

    return decorator.decorator(func)


def checkWidgetLoaded(wid):

    def func(method, *args):
        if gameglobal.rds.ui.isWidgetLoaded(wid):
            return method(*args)
        checkWidFuncDict.setdefault(wid, []).append((method, args))
        if not gameglobal.rds.ui.isWidgetLoading(wid):
            gameglobal.rds.ui.loadWidget(wid)

    return decorator.decorator(func)


def onWidgetLoaded(wid):
    if wid in checkWidFuncDict.keys():
        for func, args in checkWidFuncDict[wid]:
            func(*args)

        checkWidFuncDict.pop(wid)


def onGetCipherCallBack(cipher, callback, *args):
    callback(*args)


def checkEquipChangeOpen():

    def func(method, *args):
        if gameglobal.rds.ui.equipChange.mediator:
            BigWorld.player().showGameMsg(GMDD.data.FORBIDDEN_BY_EQUIP_CHANGE_PANEL_OPEN, ())
            return None
        if gameglobal.rds.ui.manualEquipLvUp.widget:
            BigWorld.player().showGameMsg(GMDD.data.FORBIDEN_BY_MANUAL_EQUIP_LV_UP_OPEN, ())
            return None
        return method(*args)

    return decorator.decorator(func)


def callAfterTime(time = 0.1):

    def func(method, *args):
        if method not in callList:
            callList.append(method)
            BigWorld.callback(time, Functor(delFuncFromListAndCall, method, args))

    return decorator.decorator(func)


def callInCD(time = 1):

    def func(method, *args):
        delta = 0.1
        totalTime = time + delta
        currentTiem = BigWorld.time()
        if method not in callTimeList.keys():
            nextCallBackId = BigWorld.callback(totalTime, Functor(delFuncFromCallTimeList, method))
            callTimeList[method] = (currentTiem, nextCallBackId)
            return method(*args)
        else:
            lastTime = callTimeList[method][0]
            nextCallBackId = callTimeList[method][1]
            if currentTiem - lastTime > totalTime:
                nextCallBackId = BigWorld.callback(totalTime, Functor(delFuncFromCallTimeList, method))
                callTimeList[method] = (currentTiem, nextCallBackId)
                return method(*args)
            if nextCallBackId:
                BigWorld.cancelCallback(nextCallBackId)
            nextCallBackId = BigWorld.callback(lastTime + totalTime - currentTiem, Functor(callCDMethod, method, args, totalTime))
            callTimeList[method] = (lastTime, nextCallBackId)
            return None

    return decorator.decorator(func)


def callNoUrgent(time = 0.1):

    def func(method, *args):
        frameNum = BigWorld.getCurFrameNum()
        if frameNum not in calledMethodMap.keys():
            method(*args)
            calledMethodMap[frameNum] = method
            BigWorld.callback(0, Functor(delFromCalled, frameNum))
        else:
            BigWorld.callback(time, Functor(func, method, *args))

    return decorator.decorator(func)


def delFromCalled(frame):
    if calledMethodMap.has_key(frame):
        calledMethodMap.pop(frame)


def callInterval(interval = 0, callCnt = 1, expireTime = 0):

    def func(method, *args):
        if interval < 0 or callCnt <= 0:
            return method(*args)
        methodKey = method.__module__ + method.__name__
        if callIntervalMethodMap.has_key(methodKey):
            callIntervalMethodMap[methodKey].append((method, args, time.time()))
        else:
            callIntervalMethodMap[methodKey] = [(method, args, time.time())]
            BigWorld.callback(interval, Functor(_callMethodInterval, interval, callCnt, methodKey, expireTime))

    return decorator.decorator(func)


def _callMethodInterval(interval, callCnt, methodKey, expireTime):
    methods = callIntervalMethodMap.get(methodKey, [])
    if methods:
        expireIdx = 0
        if expireTime > 0:
            timeCheck = time.time() - expireTime
            for idx, methodInfo in enumerate(methods):
                if methodInfo[2] > timeCheck:
                    expireIdx = idx
                    break

        methodLen = len(methods) - expireIdx
        if methodLen > callCnt:
            BigWorld.callback(interval, Functor(_callMethodInterval, interval, callCnt, methodKey, expireTime))
            for i in xrange(callCnt):
                method, args, _ = methods[expireIdx + i]
                method(*args)

            methods = methods[expireIdx + callCnt:]
            callIntervalMethodMap[methodKey] = methods
        else:
            callIntervalMethodMap.pop(methodKey)
            for i in xrange(methodLen):
                method, args, _ = methods[expireIdx + i]
                method(*args)


def uiEvent(wid, event):

    def _addEvent(srcFunc):
        if isinstance(wid, tuple) or isinstance(wid, list):
            wids = wid
        elif isinstance(wid, int):
            wids = (wid,)
        if isinstance(event, tuple) or isinstance(event, list):
            events = event
        elif isinstance(event, str):
            events = (event,)
        for id in wids:
            for e in events:
                if isinstance(e, tuple) and len(e) == 2:
                    eventName, priority = e
                else:
                    eventName = e
                    priority = 0
                item = (eventName,
                 srcFunc.__module__,
                 srcFunc.__name__,
                 priority)
                if item not in widEvent.get(id, []):
                    widEvent.setdefault(id, []).append(item)

        return srcFunc

    return _addEvent


def delFuncFromListAndCall(method, args):
    callList.remove(method)
    method(*args)


def delFuncFromList(method):
    callList.remove(method)


def delFuncFromCallTimeList(method):
    if method in callTimeList.keys():
        del callTimeList[method]


def callCDMethod(method, args, cd):
    method(*args)
    nextCallbackId = BigWorld.callback(cd, Functor(delFuncFromCallTimeList, method))
    callTimeList[method] = (BigWorld.time(), nextCallbackId)


def scenarioCallFilter():

    def func(method, *args):
        global scenarioFuncCache
        if gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_PLAYING_TRACK_CAMERA:
            scenarioFuncCache.append((method, args))
            return None
        else:
            return method(*args)

    return decorator.decorator(func)


def clearScenarioFuncCache():
    global scenarioFuncCache
    for i, (method, args) in enumerate(scenarioFuncCache):
        BigWorld.callback(i * 1, Functor(method, *args))

    scenarioFuncCache = []


def gbk2unicode(str, default = ''):
    try:
        gamelog.error('#Fedor@UI_ENCODING_PROBLEM_TRY_CASE_str', str)
        return str.decode(utils.defaultEncoding()).encode('utf-8')
    except Exception as e:
        try:
            gamelog.error('#Fedor@UI_exception_error', e)
            gamelog.error('gbk2unicode error_fix_try_gbk', str.decode('gbk').encode('utf-8'))
            gamelog.error('gbk2unicode error', str)
            return str.decode('gbk').encode('utf-8')
        except Exception as e2:
            gamelog.error('#Fedor@UI_exception_error_level2', e2)
            gamelog.error('gbk2unicode error_level2', str)
            return 'Fedor UI test -- exception 2 found! -- None str input!'


def unicode2gbk(str, default = ''):
    try:
        return str.decode('utf-8').encode(utils.defaultEncoding())
    except:
        gamelog.error('unicode2gbk error', str)
        return default


INPUT_RANGE_1_99 = (1, 99, GMDD.data.SET_AMOUNT)
INPUT_RANGE_1_99_TRADENUM = (1, 99, GMDD.data.ITEM_TRADE_NUM)
INPUT_RANGE_1_100 = (1, 100, GMDD.data.SET_LEVEL)
INPUT_RANGE_0_4200000000 = (0, 4200000000L, GMDD.data.MAX_MONEY_VALUE)

def inputRangeJudge(rangeType, num, option = ()):
    if num < rangeType[0] or num > rangeType[1]:
        BigWorld.player().showGameMsg(rangeType[2], option)
        return False
    return True


fontName0 = gameStrings.TEXT_SCENARIO_2800
openedDlg = []
entityClickTime = 0
entityClicked = None

class FontParam(object):

    def __init__(self, fontName = gameStrings.TEXT_SCENARIO_2800, fontSize = 16, weight = -400, shadow = 1, edge = 0, charSpace = 0, lineSpace = 2):
        self.fontName = fontName
        self.fontSize = fontSize
        self.weight = weight
        self.shadow = int(shadow)
        self.edge = int(edge)
        self.charSpace = charSpace
        self.lineSpace = lineSpace

    def getCopy(self):
        return FontParam(self.fontName, self.fontSize, self.weight, self.shadow, self.edge, self.charSpace, self.lineSpace)

    def getString(self):
        return '%s %d %d %d %d' % (self.fontName,
         self.fontSize,
         self.weight,
         self.edge,
         self.shadow)

    def getFont(self):
        if abs(self.weight) > 400:
            multiply = 1.0
        else:
            multiply = 1.4
        name = self.fontName
        if name in (gameStrings.TEXT_UI_463,):
            name = gameStrings.TEXT_UI_464
        if self.edge == 2:
            return C_ui.font(name, self.fontSize, self.weight, 0, 0, self.shadow, multiply, 1)
        else:
            return C_ui.font(name, self.fontSize, self.weight, self.edge, 0, self.shadow, multiply)


defaultNameFontParam = FontParam(gameStrings.TEXT_SCENARIO_2800, 18, -800)
font11 = C_ui.font(fontName0, 11, -400, 0, 0, 1, 1.7)
font12 = C_ui.font(fontName0, 12, -400, 0, 0, 1, 1.7)
font12ns = C_ui.font(fontName0, 12, -400, 0, 0, 0, 1.7)
font13 = C_ui.font(fontName0, 13, -400, 0, 0, 1, 1.7)
font13ns = C_ui.font(fontName0, 13, -400, 0, 0, 0, 1.7)
font14 = C_ui.font(fontName0, 14, -400, 0, 0, 1, 1.7)
font14ns = C_ui.font(fontName0, 14, -400, 0, 0, 0, 1.7)
font16 = C_ui.font(fontName0, 16, -400, 0, 0, 1, 1.4)
font16ns = C_ui.font(fontName0, 16, -400, 0, 0, 0, 1.4)
font18 = C_ui.font(fontName0, 18, -400, 0, 0, 1, 1.4)
font18ns = C_ui.font(fontName0, 18, -400, 0, 0, 0, 1.4)
font20 = C_ui.font(fontName0, 20, -800, 0, 0, 1, 1.4)
font20ns = C_ui.font(fontName0, 20, -800, 0, 0, 0, 1.4)
font22 = C_ui.font(fontName0, 22, -800, 0, 0, 1, 1.4)
font25 = C_ui.font(fontName0, 25, -800, 0, 0, 1, 1.4)
font30 = C_ui.font(fontName0, 30, -800, 0, 0, 0, 1.0)
font48 = C_ui.font(fontName0, 48, -800, 0, 0, 0, 1.0)
font60 = C_ui.font(fontName0, 60, -800, 0, 0, 0, 1.0)
NORMAL_STATE = 0
TAKEITEM_STATE = 1
REPAIR_STATE = 2
EXTRACT_STATE = 3
TARGET_STATE = 4
SYSTEM_REPAIR_STATE = 5
FORCE_REPAIR_STATE = 6
FEED_FOOD_STATE = 7
FEED_EQUIP_STATE = 8
FEED_SBALL_STATE = 9
ENHANCE_STATE = 10
ITEM_CODE_LOCK_STATE = 11
ITEM_TIME_LOCK_STATE = 12
TOUCH_VIEW_BEAST = 13
BINDEXCHG_STATE = 14
WASHSOULBALL_STATE = 15
WASHSBSKILL_STATE = 16
INLAYSTONE_STATE = 17
WASHHBSKILL_STATE = 18
SUBMIT_STATE = 19
ITEM_TIME_RELOCK_STATE = 20
EXCHANGE_STATE = 21
IDENTIFY_STATE = 22
CLEAR_IDENT_STATE = 23
FEED_GROWTHNPC_STATE = 24
RANDOM_EXCHANGE_STATE = 25
FISHHOOK_STATE = 26
DISMANTLE_STATE = 27
DISMANTLE_STATE2 = 28
ITEMMARK_STATE = 29
RENEW_STATE = 30
ITEM_SPLIT_STATE = 31
ITEM_ABSTRACTE_STATE = 32
REMOVERS_STATE = 33
ITEM_LOOKREPAIR_STATE = 34
IDENTIFY_KEYIN_STATE = 35
ASSEMBLY_STATE = 36
ITEM_JHSFORGET_STATE = 37
ITEM_JHSCLEAN_STATE = 38
TMPIDT_STATE = 39
SPLIT_STATE = 40
SYNTHESIZE_STATE = 41
ZAIJU_STATE = 42
LITTLE_MAP_SEND_POS = 43
DYE_STATE = 44
DISAS_STATE = 45
RUNE_CHONGXI_STATE = 46
MARK_MAP_STATE = 47
LATCH_CIPHER_STATE = 48
LATCH_TIME_STATE = 49
UNLATCH_STATE = 50
CHOOSE_STATE = 51
MAPMARK_STATE = 52
SIGNEQUIP_STATE = 53
RENEWAL_STATE = 54
IDENTIFY_ITEM_STATE = 55
CHANGE_OWNER_STATE = 56
CANCEL_ABILITY_STATE = 57
CANCEL_ABILITY_NODE_STATE = 58
CHANGE_BIND_STATE = 59
RENEWAL_STATE2 = 60
RESET_FASHION_PROP = 61
IDENTIFY_MANUAL_EQUIP_STATE = 62
ITEM_SEARCH_STATE = 63
DISASSEMBLE_STATE = 64
ADD_STAR_EXP_STATE = 65
WING_WORLD_MARK0 = 66
WING_WORLD_MARK1 = 67
WING_WORLD_MARK2 = 68
WING_WORLD_MARK3 = 69
CLICKABLE_STATE = 1000

def get_cursor_state():
    return cursor.Obj.get_state()


def set_bindItemPos(kind, page, pos):
    cursor.Obj.set_bindItemPos(kind, page, pos)


def get_bindItemPos():
    return cursor.Obj.get_bindItemPos()


def lock_cursor(lock = True):
    if lock:
        cursor.Obj.lock()
    else:
        cursor.Obj.release()


def cursor_islock():
    return cursor.Obj.isLock()


def set_cursor(up, down = ''):
    if cursor.Obj.isLock() or cursor.Obj.isWap():
        return
    if down != '':
        cursor.Obj.setUpDown(up, down)
        cursor.Obj.downCursor()
    else:
        cursor.Obj.setCursor(up)


def setCursorImage(filename, filedown = ''):
    set_cursor(filename, filedown)


def reset_cursor():
    cursor.Obj.reset()


def restore_cursor():
    cursor.Obj.setCursor('')


def getCursorImage():
    return cursor.Obj.tag()


def setStockCursor(x, y):
    cursor.oldCursorPos = [x, y]


def getStockCursor():
    if cursor.oldCursorPos:
        return cursor.oldCursorPos
    else:
        return [0, 0]


def set_cursor_state(state):
    old_state = get_cursor_state()
    if old_state == state:
        return
    cursor.Obj.set_state(state)


def turnUnicodeDict2Gbk(uDict):
    if type(uDict) != dict:
        return uDict
    gDict = {}
    for key, value in uDict.iteritems():
        gKey, gValue = key, value
        if type(gKey) == unicode:
            gKey = gKey.encode(utils.defaultEncoding())
        if type(gValue) == unicode:
            gValue = gValue.encode(utils.defaultEncoding())
        elif type(gValue) == dict:
            gValue = turnUnicodeDict2Gbk(gValue)
        elif type(gValue) == list or type(gValue) == tuple:
            gValue = turnUnicodeListTuple2Gbk(gValue)
        gDict[gKey] = gValue

    return gDict


def turnUnicodeListTuple2Gbk(uList):
    if type(uList) != list and type(uList) != tuple:
        return uList
    gList = []
    for item in uList:
        gValue = item
        if type(gValue) == unicode:
            gValue = gValue.encode(utils.defaultEncoding())
        elif type(gValue) == dict:
            gValue = turnUnicodeDict2Gbk(gValue)
        elif type(gValue) == list or type(gValue) == tuple:
            gValue = turnUnicodeListTuple2Gbk(gValue)
        gList.append(gValue)

    if type(uList) == tuple:
        return tuple(gList)
    return gList
