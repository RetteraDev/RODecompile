#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/pushMessageV2Proxy.o
import BigWorld
import gameglobal
import gametypes
import utils
import keys
from appSetting import Obj as AppSettings
from guis import uiConst
from guis.uiProxy import UIProxy
from sfx import birdEffect
from sfx import keyboardEffect
from callbackHelper import Functor
from guis import teamInviteV2Proxy
from guis import tipUtils
from guis import events
from guis.asObject import ASUtils
from guis.asObject import TipManager
from guis.asObject import ASObject
from data import push_data as PMD
from data import sys_config_data as SCD
RES_PATH = 'push/%s.dds'
DEFAULT_MSG_ICON_PATH = ['push/bg0.dds', 'push/bg1.dds', 'push/bg2.dds']
PUSH_TYPE_CNT = 3
MAX_MSG_SHOW_CNT = 5
APP_SETTING_PUSHMSG_PATH = keys.SET_UI_INFO + '/pushMessage/'
ASPUSHBAR_TYPE = APP_SETTING_PUSHMSG_PATH + 'type'
HORIZONTAL = 0
VERTICAL = 1
MSG_ICON_W = 40
MSG_ICON_H = 40
LINE_BG_X = 30
LINE_BG_Y = 1
LINE_BG_H = 33
MSG_ITEM_W = 32
MSG_ITEM_OFFSET = 4
TEMP_MSGITEM_SHOW_TEXT_TIME = 3
TEMP_MSGITEM_MOVE_TWEEN_TIME = 1
TEMP_MSGITEM_HOLD_TIME = 3
TEMP_MSGITEM_ENTERIN_TWEEN_TIME = 0.5
TWEEN_SHOWICON = 1
TWEEN_HIDEICON = 2

def getEndTime(param):
    if param and param.has_key('totalTime'):
        return param['totalTime'] + param['startTime']


def showBird(func):

    def wrapper(parent, msgType, data = None):
        if gameglobal.rds.GameState == gametypes.GS_PLAYGAME and msgType in (uiConst.MESSAGE_TYPE_GET_REWARD, uiConst.MESSAGE_TYPE_GET_ACHIEVE_REWARD):
            birdEffect.showBirdEffect(Functor(func, parent, msgType, data))
        else:
            func(parent, msgType, data)

    return wrapper


class PushMessageV2Proxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PushMessageV2Proxy, self).__init__(uiAdapter)
        self.msgs = {}
        self.pushMsgs = PushTypeMsgs()
        self.showBirdMsg = []
        self.callBackMap = {}
        self.destroyOnHide = False
        self.isTimerStart = False
        self.msgInfoDict = {}
        self.onceMessage = []
        self.crossMsgs = {}
        self.allMsgDict = {}
        self.isSoulBack = False
        self.itemBarShowType = AppSettings.get(ASPUSHBAR_TYPE, 1)
        self.tempMsgItems = []
        self.holdTempMsgItems = []
        self.expandLines = {}
        self.relayoutHandle = None
        self.effectShowHandles = [None, None, None]
        self.effectHideHandles = [None, None, None]
        self.widget = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_PUSH_MESSAGES_V2:
            self.widget = widget
            self.initUI()

    def initUI(self):
        self.resetDragBg(False)
        self.widget.addEventListener(events.EVENT_WIDGET_DRAG_LOCK_CHANGED, self.handleLockChanged)
        self.addCanvasListener()
        self.relayoutCanvas()
        for i in xrange(PUSH_TYPE_CNT):
            self.refreshLineCanvas(i)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_PUSH_MESSAGES_V2)

    def reset(self):
        self.holdTempMsgItems = []
        self.removeAllTempMsgItem()
        self.relayoutHandle and BigWorld.cancelCallback(self.relayoutHandle)
        self.relayoutHandle = None
        for handle in self.effectShowHandles:
            handle and BigWorld.cancelCallback(handle)

        self.effectShowHandles = [None, None, None]
        for handle in self.effectHideHandles:
            handle and BigWorld.cancelCallback(handle)

        self.effectHideHandles = [None, None, None]

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_PUSH_MESSAGES_V2)

    def clearAll(self):
        self.callBackMap = {}
        self.msgInfoDict = {}
        if self.msgs:
            self.crossMsgs = self.msgs
        if self.isSoulBack:
            self.isSoulBack = False
        else:
            self.msgs = {}
            self.pushMsgs.reset()
        self.reset()
        for i in xrange(PUSH_TYPE_CNT):
            self.refreshLineCanvas(i)

        self.relayoutCanvas()

    def addCanvasListener(self):
        for pushType in xrange(PUSH_TYPE_CNT):
            canvas = getattr(self.widget, 'canvas%d' % pushType)
            canvas.pushType = pushType
            canvas.addEventListener(events.MOUSE_ROLL_OVER, self.onCanvasRollOver, False, 0, True)
            canvas.addEventListener(events.MOUSE_ROLL_OUT, self.onCanvasRollOut, False, 0, True)

    def onCanvasRollOver(self, *args):
        e = ASObject(args[3][0])
        pushType = e.currentTarget.pushType
        self.expandLines[pushType] = True
        self.resetLineCanvas(pushType, TWEEN_SHOWICON)
        self.relayoutCanvas()
        self.removeAllTempMsgItem()
        self.hideEffect(pushType)

    def onCanvasRollOut(self, *args):
        e = ASObject(args[3][0])
        pushType = e.currentTarget.pushType
        del self.expandLines[pushType]
        self.resetLineCanvas(pushType, TWEEN_HIDEICON)
        self.relayoutCanvas()
        self.removeAllTempMsgItem()
        self.hideEffect(pushType)
        self.holdTempMsgItems and self.handleAllHoldMsgItem()

    def removeAllTempMsgItem(self):
        for tempMsgItem in self.tempMsgItems:
            tempMsgItem.parent and tempMsgItem.parent.removeChild(tempMsgItem)

        self.tempMsgItems = []

    def removeTempMsgItem(self, msgItem):
        msgItem.parent and msgItem.parent.removeChild(msgItem)
        if msgItem in self.tempMsgItems:
            self.tempMsgItems.remove(msgItem)

    def relayoutCanvas(self):
        self.relayoutHandle and BigWorld.cancelCallback(self.relayoutHandle)
        self.relayoutHandle = None
        if self.expandLines:
            self.relayoutHandle = BigWorld.callback(1, self.relayoutCanvas)
            return
        else:
            if self.itemBarShowType == HORIZONTAL:
                lastCanvasX = 0
                for pushType in xrange(PUSH_TYPE_CNT):
                    canvas = getattr(self.widget, 'canvas%d' % pushType)
                    canvas.x, canvas.y = lastCanvasX, 0
                    if self.pushMsgs.getMsgsByPushType(pushType):
                        lastCanvasX += MSG_ICON_W

            else:
                lastCanvasY = (PUSH_TYPE_CNT - 1) * MSG_ICON_H
                for pushType in xrange(PUSH_TYPE_CNT):
                    canvas = getattr(self.widget, 'canvas%d' % pushType)
                    canvas.x, canvas.y = 0, lastCanvasY
                    if self.pushMsgs.getMsgsByPushType(pushType):
                        lastCanvasY -= MSG_ICON_W

            return

    def resetLineCanvas(self, pushType, resetType):
        canvas = getattr(self.widget, 'canvas%d' % pushType)
        lineMsgs = self.pushMsgs.getMsgsByPushType(pushType)
        showCnt = min(len(lineMsgs), MAX_MSG_SHOW_CNT)
        self.resetLineCanvasBg(canvas, resetType, showCnt)
        for i in xrange(showCnt):
            msgItem = getattr(canvas, 'msgItem%d' % i)
            msgType = lineMsgs[i]
            if msgItem is None:
                msgData = self.uiGetMsgByType(msgType)
                msgItem = self.widget.getInstByClsName('PushMessageV2_MsgItem')
                msgItem.msgData = msgData
                msgItem.addEventListener(events.MOUSE_CLICK, self.onMsgItemClick, False, 0, True)
                self.addMsgItemTip(msgItem, msgData)
            if resetType == TWEEN_SHOWICON:
                msgItem.startShow(canvas, i)
            elif i == 0 and showCnt != 1:
                msgItem.refreshByExtraData(canvas, 0, pushType, len(lineMsgs))
            else:
                msgItem.startHide(i)

    def resetLineCanvasBg(self, canvas, resetType, showCnt = 1):
        lineBg = getattr(canvas, 'lineBg')
        if resetType == TWEEN_SHOWICON and showCnt > 1:
            if lineBg is None:
                lineBg = self.widget.getInstByClsName('PushMessageV2_LineBg')
                canvas.addChildAt(lineBg, 0)
                setattr(canvas, 'lineBg', lineBg)
            lineBg.x = LINE_BG_X
            lineBg.y = LINE_BG_Y
            lineBg.width = (MSG_ITEM_W + MSG_ITEM_OFFSET) * showCnt
            lineBg.height = LINE_BG_H
        else:
            lineBg and canvas.removeChild(lineBg)
            canvas.lineBg = None

    def refreshLineCanvas(self, pushType):
        canvas = getattr(self.widget, 'canvas%d' % pushType)
        lineMsgs = self.pushMsgs.getMsgsByPushType(pushType)
        if self.expandLines.get(pushType):
            self.refreshExpandLineCanvas(canvas, lineMsgs)
        else:
            self.refreshShrinkLineCanvas(canvas, lineMsgs, pushType)

    def refreshExpandLineCanvas(self, canvas, lineMsgs):
        if not lineMsgs:
            for i in xrange(MAX_MSG_SHOW_CNT):
                msgItem = getattr(canvas, 'msgItem%d' % i)
                msgItem and msgItem.hideComplete()

            self.resetLineCanvasBg(canvas, TWEEN_HIDEICON, 0)
        else:
            showCnt = min(len(lineMsgs), MAX_MSG_SHOW_CNT)
            for i in xrange(MAX_MSG_SHOW_CNT):
                msgItem = getattr(canvas, 'msgItem%d' % i)
                if showCnt <= i:
                    msgItem and msgItem.hideComplete()
                else:
                    msgType = lineMsgs[i]
                    if msgItem is None:
                        msgItem = self.widget.getInstByClsName('PushMessageV2_MsgItem')
                        msgItem.addEventListener(events.MOUSE_CLICK, self.onMsgItemClick, False, 0, True)
                    msgData = self.uiGetMsgByType(msgType)
                    msgItem.msgData = msgData
                    msgItem.refresh(canvas, i)
                    self.addMsgItemTip(msgItem, msgData)

            self.resetLineCanvasBg(canvas, TWEEN_SHOWICON, showCnt)

    def refreshShrinkLineCanvas(self, canvas, lineMsgs, pushType):
        if not lineMsgs:
            for i in xrange(MAX_MSG_SHOW_CNT):
                msgItem = getattr(canvas, 'msgItem%d' % i)
                msgItem and msgItem.hideComplete()

        else:
            msgCnt = len(lineMsgs)
            for i in xrange(MAX_MSG_SHOW_CNT):
                msgItem = getattr(canvas, 'msgItem%d' % i)
                if i == 0:
                    msgType = lineMsgs[i]
                    if msgItem is None:
                        msgItem = self.widget.getInstByClsName('PushMessageV2_MsgItem')
                        msgItem.addEventListener(events.MOUSE_CLICK, self.onMsgItemClick, False, 0, True)
                    msgData = self.uiGetMsgByType(msgType)
                    msgItem.msgData = msgData
                    self.addMsgItemTip(msgItem, msgData)
                    if msgCnt == 1:
                        msgItem.refresh(canvas, i)
                    else:
                        msgItem.refreshByExtraData(canvas, 0, pushType, msgCnt)
                else:
                    msgItem and msgItem.hideComplete()

        self.resetLineCanvasBg(canvas, TWEEN_HIDEICON, 0)

    def onMsgItemClick(self, *args):
        e = ASObject(args[3][0])
        msgType = e.currentTarget.msgType
        pushData = self.msgs.get(msgType)
        pushData and self.callBackByType(msgType, 'click')

    def addMsgItemTip(self, msgItem, msgData):
        tipDesc = msgData.get('tipDesc')
        if not tipDesc:
            TipManager.addTipByFunc(msgItem, self.getDynamicTip, msgItem, False)
        else:
            TipManager.addTip(msgItem, tipDesc, tipUtils.TYPE_DEFAULT_BLACK)

    def getDynamicTip(self, *args):
        msgItem = ASObject(args[3][0])
        msgType = msgItem.msgType
        if msgType == uiConst.MESSAGE_TYPE_PUSH_XINMO_RECORD:
            tipStr = gameglobal.rds.ui.xinmoRecord._getPushMsgTip()
            tip = TipManager.getInstance().getDefaultTipMc(tipStr, tipUtils.TYPE_DEFAULT_BLACK)
            TipManager.showImediateTip(msgItem, tip, 'upCenter')
        if msgType == uiConst.MESSAGE_TYPE_CRYSTAL_DEFENCE_UPDATE:
            tipStr = gameglobal.rds.ui.crystalDefenceMain.getPushMsgTip()
            tip = TipManager.getInstance().getDefaultTipMc(tipStr, tipUtils.TYPE_DEFAULT_BLACK)
            TipManager.showImediateTip(msgItem, tip, 'upCenter')

    def showEffect(self, pushType):
        self.effectShowHandles[pushType] and BigWorld.cancelCallback(self.effectShowHandles[pushType])
        self.effectShowHandles[pushType] = None
        hintEffectMc = getattr(self.widget, 'hintEffect%d' % pushType)
        if not hintEffectMc:
            hintEffectMc = self.widget.getInstByClsName('PushMessageV2_HintEffect')
            self.widget.addChild(hintEffectMc)
            canvas = getattr(self.widget, 'canvas%d' % pushType)
            hintEffectMc.x, hintEffectMc.y = canvas.x, canvas.y
            setattr(self.widget, 'hintEffect%d' % pushType, hintEffectMc)
            ASUtils.setHitTestDisable(hintEffectMc, True)
        self.effectHideHandles[pushType] and BigWorld.cancelCallback(self.effectHideHandles[pushType])
        self.effectHideHandles[pushType] = BigWorld.callback(SCD.data.get('EffectShowTime', 5), Functor(self.hideEffect, pushType))

    def hideEffect(self, pushType):
        self.effectHideHandles[pushType] and BigWorld.cancelCallback(self.effectHideHandles[pushType])
        self.effectHideHandles[pushType] = None
        hintEffectMc = getattr(self.widget, 'hintEffect%d' % pushType)
        if hintEffectMc:
            setattr(self.widget, 'hintEffect%d' % pushType, None)
            self.widget.removeChild(hintEffectMc)
        self.effectShowHandles[pushType] and BigWorld.cancelCallback(self.effectShowHandles[pushType])
        self.effectShowHandles[pushType] = BigWorld.callback(SCD.data.get('EffectShowIntervalTime', 300), Functor(self.showEffect, pushType))

    def uiGetAllMsg(self):
        return [ self.uiGetMsgByType(msgType) for msgType in self.msgs ]

    def getMsgPushType(self, msgType):
        if msgType in self.msgInfoDict.keys():
            pushDataInfo = self.msgInfoDict.get(msgType, {})
        else:
            pushDataInfo = PMD.data.get(msgType, {})
        return pushDataInfo.get('pushType', 0)

    def getShowTime(self, pushMsgdata, msgType):
        showCountDown = PMD.data.get(msgType, {}).get('showTime', 0)
        showEndTime = None
        currentTime = utils.getNow()
        for data in pushMsgdata.dataList:
            endTime = getEndTime(data)
            if endTime and endTime > currentTime:
                if showEndTime is None or showEndTime > endTime:
                    showEndTime = endTime

        return (showCountDown, showEndTime)

    def addMsgItem(self, msgData):
        msgItem = self.widget.getInstByClsName('PushMessageV2_AddAnimation')
        self.widget.addChild(msgItem)
        self.tempMsgItems.append(msgItem)
        msgItem.x, msgItem.y = self.getMoveAnimStartPos()
        msgItem.msgData = msgData
        msgItem.addEventListener(events.MOUSE_CLICK, self.onTempMsgItemClick, False, 0, True)
        msgItem.gotoAndPlay('start')
        msgItem.scaleX = msgItem.scaleY = 1
        msgItem.iconMc.icon.fitSize = True
        msgItem.iconMc.icon.loadImage(msgData['iconPath'])
        msgItem.textMc.textField.text = msgData['name']
        self.setMsgItemBg(msgItem, msgData['pushType'])
        self.addMsgItemTip(msgItem, msgData)
        return msgItem

    def setMsgItemBg(self, msgItem, pushType):
        for i in xrange(0, PUSH_TYPE_CNT):
            bgMc = getattr(msgItem.iconMc, 'bg%d' % i)
            bgMc.visible = bool(i == pushType)

    def onTempMsgItemClick(self, *args):
        e = ASObject(args[3][0])
        msgItem = e.currentTarget
        msgType = msgItem.msgData.msgType
        pushType = msgItem.msgData.pushType
        pushData = self.msgs.get(msgType)
        pushData and self.callBackByType(msgType, 'click')
        self.removeTempMsgItem(msgItem)
        self.refreshLineCanvas(pushType)
        self.relayoutCanvas()

    def uiAddMsg(self, msgType):
        msgData = self.uiGetMsgByType(msgType)
        pushType = msgData['pushType']
        msgItem = self.addMsgItem(msgData)
        endPos = self.getMoveAnimEndPos(pushType)
        if self.expandLines:
            self.holdTempMsgItems.append((msgItem, endPos))
        else:
            self.addMoveTweener(msgItem, endPos)

    def addMoveTweener(self, msgItem, endPos, delayTime = 10):
        endX, endY = endPos
        msgItem.needUpdate = True
        param = {'delay': delayTime,
         'onStart': self.moveTweenStart,
         'onStartParams': (msgItem,),
         'onUpdate': self.moveTweenUpdate,
         'onUpdateParams': (msgItem,),
         'onComplete': self.moveTweenComplete,
         'onCompleteParams': (msgItem,),
         'time': TEMP_MSGITEM_MOVE_TWEEN_TIME,
         'x': endX,
         'y': endY,
         'scaleX': 0.8,
         'scaleY': 0.8}
        ASUtils.addTweener(msgItem, param)

    def handleAllHoldMsgItem(self):
        for msgItem, endPos in self.holdTempMsgItems:
            self.addMoveTweener(msgItem, endPos, 0)

        self.holdTempMsgItems = []

    def moveTweenStart(self, *args):
        msgItem = ASObject(args[3][0])
        msgItem.gotoAndPlay('hold')

    def moveTweenComplete(self, *args):
        msgItem = ASObject(args[3][0])
        self.enterInTween(msgItem)

    def moveTweenUpdate(self, *args):
        msgItem = ASObject(args[3][0])
        if msgItem.x < MSG_ICON_W and msgItem.needUpdate:
            self.relayoutCanvas()
            msgItem.needUpdate = False

    def enterInTween(self, msgItem):
        msgData = msgItem.msgData
        pushType = msgData.pushType
        canvas = getattr(self.widget, 'canvas%d' % pushType)
        xGlobal, yGlobal = ASUtils.local2Global(canvas, 0, 0)
        xWidget, yWidget = ASUtils.global2Local(self.widget, xGlobal, yGlobal)
        param = {'delay': TEMP_MSGITEM_HOLD_TIME,
         'onComplete': self.enterInTweenComplete,
         'onCompleteParams': (msgItem,),
         'time': TEMP_MSGITEM_ENTERIN_TWEEN_TIME,
         'x': xWidget,
         'y': yWidget}
        ASUtils.addTweener(msgItem, param)

    def enterInTweenComplete(self, *args):
        msgItem = ASObject(args[3][0])
        pushType = msgItem.msgData.pushType
        self.refreshLineCanvas(pushType)
        self.removeTempMsgItem(msgItem)

    def getMoveAnimStartPos(self):
        xRatio, yRatio = SCD.data.get('pushShowPos', (0.5, 0.3))
        xGlobal = xRatio * self.widget.stage.stageWidth
        yGlobal = yRatio * self.widget.stage.stageHeight
        xWidget, yWidget = ASUtils.global2Local(self.widget, xGlobal, yGlobal)
        y = self.getLastYPos(yWidget)
        y -= MSG_ICON_H + 2
        return (xWidget, y)

    def getLastYPos(self, minYPos):
        for tempMsgItem in self.tempMsgItems:
            if tempMsgItem.currentFrameLabel != 'hold':
                minYPos = min(tempMsgItem.y, minYPos)

        return minYPos

    def getMoveAnimEndPos(self, pushType):
        lineMsgs = self.pushMsgs.getMsgsByPushType(pushType)
        offset = len(lineMsgs) > 1
        x, y = MSG_ICON_W * int(offset), 0
        canvas = getattr(self.widget, 'canvas%d' % pushType)
        xGlobal, yGlobal = ASUtils.local2Global(canvas, x, y)
        xWidget, yWidget = ASUtils.global2Local(self.widget, xGlobal, yGlobal)
        return (xWidget, yWidget)

    def uiRemoveMsg(self, msgType):
        pushType = self.getMsgPushType(msgType)
        index = self.pushMsgs.getMsgIndex(msgType, pushType)
        if index > MAX_MSG_SHOW_CNT:
            return
        self.refreshLineCanvas(pushType)
        self.relayoutCanvas()

    def uiUpdateMsg(self, msgType):
        pushType = self.getMsgPushType(msgType)
        index = self.pushMsgs.getMsgIndex(msgType, pushType)
        if index > MAX_MSG_SHOW_CNT:
            return
        self.refreshLineCanvas(pushType)
        self.relayoutCanvas()

    def uiGetMsgByType(self, msgType):
        pushMsgdata = self.msgs[msgType]
        if msgType in self.msgInfoDict.keys():
            pushDataInfo = self.msgInfoDict.get(msgType, {})
        else:
            pushDataInfo = PMD.data.get(msgType, {})
        msgData = {'name': pushDataInfo.get('name', 'new Message'),
         'pushType': pushDataInfo.get('pushType', 0),
         'iconPath': RES_PATH % pushDataInfo.get('iconId', 'notFound'),
         'msgType': msgType,
         'tipDesc': pushDataInfo.get('tooltip', '')}
        showCountDown, showEndTime = self.getShowTime(pushMsgdata, msgType)
        if showCountDown and showEndTime:
            msgData['endTime'] = showEndTime
        if pushMsgdata.num > 1:
            msgData['num'] = pushMsgdata.num
        return msgData

    def setCrossMsg(self):
        self.crossMsgs = self.msgs
        self.msgs = {}
        self.isSoulBack = True
        for messageId in self.allMsgDict.keys():
            if messageId in self.crossMsgs.keys() and PMD.data.get(messageId, {}).get('soulBackPush', 0):
                data = self.allMsgDict[messageId]['data']
                msgInfo = self.allMsgDict[messageId]['msgInfo']
                self.addPushMsg(messageId, data, msgInfo, isSoulBackMsg=True)

        self.crossMsgs = {}

    def handleMsg(self, msgType):
        pushData = self.msgs.get(msgType, None)
        if pushData:
            self.callBackByType(msgType, 'click')

    def setCallBack(self, msgType, callBackDict):
        self.callBackMap[msgType] = callBackDict

    def callBackByType(self, msgType, callBackType, args = None):
        if callBackType == 'click' and gameglobal.rds.ui.quest.isShow and not PMD.data.get(msgType, {}).get('canUse', 0):
            return
        if self.callBackMap.has_key(msgType):
            if self.callBackMap[msgType].has_key(callBackType):
                if args:
                    self.callBackMap[msgType][callBackType](args)
                else:
                    self.callBackMap[msgType][callBackType]()
        if callBackType == 'click' and PMD.data.get(msgType, {}).get('clickOnce', 0):
            self.removePushMsg(msgType)

    def addPushMsg(self, msgType, data = None, msgInfo = None, isSoulBackMsg = False):
        self.saveAllMsg(msgType, data, msgInfo)
        enablePushMessageOnceFlag = gameglobal.rds.configData.get('enablePushMessageOnceFlag', True)
        if enablePushMessageOnceFlag:
            once = PMD.data.get(msgType, {}).get('once')
            if isSoulBackMsg and once:
                self.onceMessage.remove(msgType)
            if once and msgType not in self.onceMessage:
                self.onceMessage.append(msgType)
            elif once:
                return
        if not self._checkMsgTypeEnable(msgType):
            return
        if isSoulBackMsg and not PMD.data.get(msgType, {}).get('crossEnable', 0):
            return
        if gameglobal.rds.GameState == gametypes.GS_PLAYGAME and msgType in (uiConst.MESSAGE_TYPE_GET_REWARD, uiConst.MESSAGE_TYPE_GET_ACHIEVE_REWARD):
            self.showBirdMsg.append((msgType, data))
            birdEffect.showBirdEffect(Functor(self.realAddPushMsg, msgType, data))
        else:
            self.realAddPushMsg(msgType, data, msgInfo)

    def saveAllMsg(self, messageId, messageData, messageInfo):
        self.allMsgDict[messageId] = {'data': messageData,
         'msgInfo': messageInfo}

    def realAddPushMsg(self, msgType, data = None, msgInfo = None):
        if not self._checkMsgTypeEnable(msgType):
            return
        if msgType in (uiConst.MESSAGE_TYPE_GET_REWARD,):
            erefType, detailId = data['data']
            p = BigWorld.player()
            if erefType == uiConst.ACT_STAT and p.statsTargets.has_key(detailId) and p.statsTargets[detailId].rewardApplied:
                return
            if erefType == uiConst.ACT_SPECIAL_AWD and p.isSpAwdRewarded(detailId):
                return
        if msgInfo:
            self.msgInfoDict[msgType] = msgInfo
        if (msgType, data) in self.showBirdMsg:
            self.showBirdMsg.remove((msgType, data))
        if msgType in self.msgs.keys():
            pushData = self.msgs[msgType]
            pushData.addData(data)
            self.updatePushMsg(msgType)
        else:
            pushData = PushMsgData(msgType, data)
            self.msgs[msgType] = pushData
            self.pushMsgs.add(msgType, self.getMsgPushType(msgType))
            self.widget and self.uiAddMsg(msgType)
            keyboardEffect.addPushMsgEffect(msgType)
        self.callBackByType(msgType, 'refresh')
        self.refreshTimer()
        soundIdx = self.msgInfoDict.get(msgType, {}).get('soundIdx', 0)
        if not soundIdx:
            soundIdx = PMD.data.get(msgType, {}).get('soundIdx', 0)
        gameglobal.rds.sound.playSound(soundIdx)

    def removePushMsg(self, msgType):
        if not self.msgs.has_key(msgType):
            return
        del self.msgs[msgType]
        self.pushMsgs.remove(msgType, self.getMsgPushType(msgType))
        self.widget and self.uiRemoveMsg(msgType)
        self.refreshTimer()
        keyboardEffect.removePushMsgEffect(msgType)

    def removeTeamPushMsg(self):
        pushData = self.msgs.pop(uiConst.MESSAGE_TYPE_INVITE_TEAM, None)
        self.pushMsgs.remove(uiConst.MESSAGE_TYPE_INVITE_TEAM, self.getMsgPushType(uiConst.MESSAGE_TYPE_INVITE_TEAM))
        if pushData:
            self.widget and self.uiRemoveMsg(uiConst.MESSAGE_TYPE_INVITE_TEAM)
            self.refreshTimer()
            for data in pushData.dataList:
                srcGbId = long(data['data'][teamInviteV2Proxy.SRC_GBID_IDX])
                BigWorld.player().cell.cancelInviteByGroup(srcGbId)

        pushData = self.msgs.pop(uiConst.MESSAGE_TYPE_RECOMMEND_TEAM, None)
        self.pushMsgs.remove(uiConst.MESSAGE_TYPE_RECOMMEND_TEAM, self.getMsgPushType(uiConst.MESSAGE_TYPE_RECOMMEND_TEAM))
        if pushData:
            self.widget and self.uiRemoveMsg(uiConst.MESSAGE_TYPE_RECOMMEND_TEAM)
            self.refreshTimer()
            for data in pushData.dataList:
                srcGbId = long(data['data'][teamInviteV2Proxy.SRC_GBID_IDX])
                BigWorld.player().cell.cancelRecommendByGroup(srcGbId)

    def updatePushMsg(self, msgType):
        if not self.msgs.has_key(msgType):
            return
        self.widget and self.uiUpdateMsg(msgType)
        self.refreshTimer()

    def removeData(self, msgType, data):
        if not self.msgs.has_key(msgType):
            return
        elif data is None:
            return
        else:
            pushData = self.msgs[msgType]
            if pushData:
                pushData.removeData(data)
                self.updatePushMsg(msgType)
            if len(pushData.dataList) == 0:
                self.removePushMsg(msgType)
            self.callBackByType(msgType, 'refresh')
            self.refreshTimer()
            return

    def getDataList(self, msgType):
        pushData = self.msgs.get(msgType, None)
        if pushData:
            return pushData.dataList
        else:
            return {}

    def getLastData(self, msgType):
        pushData = self.msgs.get(msgType, None)
        if pushData:
            return pushData.getLastData()
        else:
            return {}

    def getFirstData(self, msgType):
        pushData = self.msgs.get(msgType, None)
        if pushData:
            return pushData.getFirstData()
        else:
            return {}

    def removeLastData(self, msgType):
        self.removeData(msgType, self.getLastData(msgType))

    def hasMsgType(self, msgType):
        if self.msgs.has_key(msgType):
            return True
        else:
            return False

    def hasMsgInMsgList(self, msgList):
        for msg in msgList:
            if msg in self.msgs:
                return msg

    def hasPushData(self, msgType, pushData):
        curPush = self.getDataList(msgType)
        if curPush:
            for val in curPush:
                if val == pushData:
                    return True

        return False

    def refreshTimer(self):
        needStart = False
        for pushMsgData in self.msgs.values():
            if needStart:
                break
            for data in pushMsgData.dataList:
                if getEndTime(data):
                    needStart = True
                    break

        if needStart:
            self._startTimer()
        else:
            self._stopTime()

    def _refreshTime(self):
        currentTime = utils.getNow()
        for msgType in self.msgs.keys():
            pushData = self.msgs[msgType]
            for msgData in pushData.dataList:
                endTime = getEndTime(msgData)
                if endTime and endTime < currentTime:
                    self.callBackByType(msgType, 'timeout', msgData)
                    self.removeData(msgType, msgData)
                    self.updatePushMsg(msgType)

        if self.isTimerStart:
            BigWorld.callback(1, self._refreshTime)

    def _startTimer(self):
        if not self.isTimerStart:
            self.isTimerStart = True
            self._refreshTime()

    def _stopTime(self):
        if self.isTimerStart:
            self.isTimerStart = False

    def _checkMsgTypeEnable(self, msgType):
        if BigWorld.player()._isSoul():
            return PMD.data.get(msgType, {}).get('crossEnable', 0)
        return True

    def _onVBtnClick(self, e):
        self.itemBarShowType = HORIZONTAL
        self.resetDragBg(True)
        self.dragDataChanged()
        self.relayoutCanvas()

    def _onHBtnClick(self, e):
        self.itemBarShowType = VERTICAL
        self.resetDragBg(True)
        self.dragDataChanged()
        self.relayoutCanvas()

    def handleLockChanged(self, *args):
        e = ASObject(args[3][0])
        editMode = bool(e.data)
        self.resetDragBg(editMode)
        for pushType in xrange(PUSH_TYPE_CNT):
            canvas = getattr(self.widget, 'canvas%d' % pushType)
            canvas.visible = not editMode

        if not editMode:
            AppSettings[ASPUSHBAR_TYPE] = self.itemBarShowType
            AppSettings.save()

    def resetDragBg(self, editMode):
        self.widget.hBg.visible = False
        self.widget.hBtn.visible = False
        self.widget.vBg.visible = editMode and self.itemBarShowType == VERTICAL
        self.widget.vBtn.visible = False

    def dragDataChanged(self):
        if self.itemBarShowType == HORIZONTAL:
            rect = (0,
             0,
             self.widget.hBg.width,
             self.widget.hBg.height)
        else:
            rect = (0,
             0,
             self.widget.vBg.width,
             self.widget.vBg.height)
        event = ASUtils.getDragDataEvent(self.widget, uiConst.WIDGET_PUSH_MESSAGES_V2, rect)
        self.widget.dispatchEvent(event)

    def setHitTestDisable(self, disable):
        if self.widget:
            ASUtils.setHitTestDisable(self.widget, disable)


class PushTypeMsgs(object):

    def __init__(self):
        self.value = ([], [], [])

    def reset(self):
        self.value = ([], [], [])

    def add(self, msgType, pushType):
        self.value[pushType].append(msgType)

    def remove(self, msgType, pushType):
        if msgType in self.value[pushType]:
            self.value[pushType].remove(msgType)

    def getMsgIndex(self, msgType, pushType):
        if msgType in self.value[pushType]:
            return self.value[pushType].index(msgType)
        else:
            return -1

    def getMsgsByPushType(self, pushType):
        return self.value[pushType]


class PushMsgData(object):

    def __init__(self, msgType, param):
        super(PushMsgData, self).__init__()
        self.type = msgType
        self.dataList = []
        self.num = 0
        self.addData(param)

    def getLastData(self):
        return self.dataList[len(self.dataList) - 1]

    def getFirstData(self):
        return self.dataList[0]

    def removeData(self, value):
        for item in self.dataList:
            if value['data'] == item['data']:
                self.dataList.remove(item)
                self.num = len(self.dataList)
                return

    def addData(self, param):
        if param:
            self.dataList.append(param)
            self.num = len(self.dataList)

    def getEndTime(self):
        currentEndTime = None
        for data in self.dataList:
            endTime = getEndTime(data)
            if endTime:
                if currentEndTime == None or endTime < currentEndTime:
                    currentEndTime = endTime

        return endTime
