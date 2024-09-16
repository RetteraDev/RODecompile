#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/pushMessageProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gametypes
import utils
from ui import gbk2unicode
from guis import uiConst, uiUtils
from guis.uiProxy import UIProxy
from sfx import birdEffect
from sfx import keyboardEffect
from callbackHelper import Functor
from guis import teamInviteV2Proxy
from data import push_data as PMD
from data import sys_config_data as SCD
RES_PATH = 'push/'

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


class PushMessageProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PushMessageProxy, self).__init__(uiAdapter)
        self.mediator = None
        self.modelMap = {'messageItemClick': self.onHandleMsg,
         'getAllMessage': self.onGetAllMsg,
         'getDynamicTip': self.onGetDynamicTip}
        self.msgs = {}
        self.showBirdMsg = []
        self.callBackMap = {}
        self.destroyOnHide = False
        self.isTimerStart = False
        self.msgInfoDict = {}
        self.onceMessage = []
        self.crossMsgs = {}
        self.allMsgDict = {}
        self.stopTimeCallBackMap = {}
        self.isSoulBack = False

    def _registerMediator(self, widgetId, mediator):
        if widgetId in (uiConst.WIDGET_PUSH_MESSSAGES, uiConst.WIDGET_EXTEND_PUSH_MESSSAGES):
            self.mediator = mediator
            if gameglobal.CURRENT_WINDOW_STYLE == gameglobal.WINDOW_STYLE_CHAT:
                gameglobal.rds.ui.extendChatBox.registerPushMsg(self.mediator)
            return uiUtils.dict2GfxDict({'pushShowPos': SCD.data.get('pushShowPos', (0.5, 0.3))})

    def show(self, *args):
        self.uiAdapter.loadWidget(uiConst.WIDGET_PUSH_MESSSAGES)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_PUSH_MESSSAGES)

    def reset(self):
        super(self.__class__, self).reset()
        self.callBackMap = {}
        self.msgInfoDict = {}
        if self.msgs:
            self.crossMsgs = self.msgs
        if self.isSoulBack:
            self.isSoulBack = False
        else:
            self.msgs = {}

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

    def onHandleMsg(self, *args):
        msgType = args[3][0].GetNumber()
        pushData = self.msgs.get(msgType, None)
        if gameglobal.CURRENT_WINDOW_STYLE == gameglobal.WINDOW_STYLE_CHAT:
            p = BigWorld.player()
            p.setWindowStyle(gameglobal.WINDOW_STYLE_NORMAL)
        if pushData:
            self.callBackByType(msgType, 'click')

    def onGetAllMsg(self, *args):
        msgs = []
        for msgType in self.msgs:
            msgs.append(self._getASMsgByType(msgType))

        return uiUtils.array2GfxAarry(msgs)

    def setCallBack(self, msgType, callBackDict):
        self.callBackMap[msgType] = callBackDict

    def callBackByType(self, msgType, callBackType, args = None):
        if callBackType == 'click' and (gameglobal.rds.ui.quest.isShow or gameglobal.rds.ui.npcV2.isShow) and not PMD.data.get(msgType, {}).get('canUse', 0):
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
        stopTime = PMD.data.get(msgType, {}).get('stopTime', None)
        if stopTime != None:
            callBackId = self.stopTimeCallBackMap.get(msgType, None)
            if callBackId != None:
                BigWorld.cancelCallback(callBackId)
            callBackId = BigWorld.callback(utils.getNextCrontabTime(stopTime) - utils.getNow(), Functor(self.vanishCallBack, msgType))
            self.stopTimeCallBackMap[msgType] = callBackId
        enablePushMessageOnceFlag = gameglobal.rds.configData.get('enablePushMessageOnceFlag', True)
        if enablePushMessageOnceFlag:
            once = PMD.data.get(msgType, {}).get('once')
            if isSoulBackMsg and once:
                self.onceMessage.remove(msgType)
            if once and msgType not in self.onceMessage:
                self.onceMessage.append(msgType)
            elif once:
                return
        if not self._checkMsgTypeEnable(msgType, msgInfo):
            return
        elif isSoulBackMsg and not PMD.data.get(msgType, {}).get('crossEnable', 0):
            return
        else:
            if gameglobal.rds.GameState == gametypes.GS_PLAYGAME and msgType in (uiConst.MESSAGE_TYPE_GET_REWARD, uiConst.MESSAGE_TYPE_GET_ACHIEVE_REWARD):
                self.showBirdMsg.append((msgType, data))
                birdEffect.showBirdEffect(Functor(self.realAddPushMsg, msgType, data))
            else:
                self.realAddPushMsg(msgType, data, msgInfo)
            return

    def saveAllMsg(self, messageId, messageData, messageInfo):
        self.allMsgDict[messageId] = {'data': messageData,
         'msgInfo': messageInfo}

    def realAddPushMsg(self, msgType, data = None, msgInfo = None):
        if not self._checkMsgTypeEnable(msgType, msgInfo):
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
            msgData = self._getASMsgByType(msgType)
            if self.mediator:
                self.mediator.Invoke('addMsg', msgData)
            keyboardEffect.addPushMsgEffect(msgType)
        self.callBackByType(msgType, 'refresh')
        self.refreshTimer()
        soundIdx = self.msgInfoDict.get(msgType, {}).get('soundIdx', 0)
        if not soundIdx:
            soundIdx = PMD.data.get(msgType, {}).get('soundIdx', 0)
        gameglobal.rds.sound.playSound(soundIdx)
        if gameglobal.CURRENT_WINDOW_STYLE == gameglobal.WINDOW_STYLE_CHAT:
            gameglobal.rds.ui.extendChatBox.flashWindow()

    def removePushMsg(self, msgType):
        callBackId = self.stopTimeCallBackMap.get(msgType, None)
        if callBackId != None:
            BigWorld.cancelCallback(callBackId)
            self.stopTimeCallBackMap.pop(msgType)
        if not self.msgs.has_key(msgType):
            return
        else:
            del self.msgs[msgType]
            if self.mediator:
                self.mediator.Invoke('removeMsg', GfxValue(msgType))
            self.refreshTimer()
            keyboardEffect.removePushMsgEffect(msgType)
            return

    def removeTeamPushMsg(self):
        pushData = self.msgs.pop(uiConst.MESSAGE_TYPE_INVITE_TEAM, None)
        if pushData:
            if self.mediator:
                self.mediator.Invoke('removeMsg', GfxValue(uiConst.MESSAGE_TYPE_INVITE_TEAM))
            self.refreshTimer()
            for data in pushData.dataList:
                srcGbId = long(data['data'][teamInviteV2Proxy.SRC_GBID_IDX])
                BigWorld.player().cell.cancelInviteByGroup(srcGbId)

        pushData = self.msgs.pop(uiConst.MESSAGE_TYPE_RECOMMEND_TEAM, None)
        if pushData:
            if self.mediator:
                self.mediator.Invoke('removeMsg', GfxValue(uiConst.MESSAGE_TYPE_RECOMMEND_TEAM))
            self.refreshTimer()
            for data in pushData.dataList:
                srcGbId = long(data['data'][teamInviteV2Proxy.SRC_GBID_IDX])
                BigWorld.player().cell.cancelRecommendByGroup(srcGbId)

    def updatePushMsg(self, msgType):
        if not self.msgs.has_key(msgType):
            return
        msgData = self._getASMsgByType(msgType)
        if self.mediator:
            self.mediator.Invoke('updateMsg', msgData)
        self.refreshTimer()

    def setHitTestDisable(self, disable):
        if self.mediator:
            self.mediator.Invoke('setHitTestDisable', GfxValue(disable))

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

        if self.mediator:
            self.mediator.Invoke('setTime', GfxValue(currentTime))
        if self.isTimerStart:
            BigWorld.callback(1, self._refreshTime)

    def _startTimer(self):
        if not self.isTimerStart:
            self.isTimerStart = True
            self._refreshTime()

    def _stopTime(self):
        if self.isTimerStart:
            self.isTimerStart = False

    def _getASMsgByType(self, msgType):
        pushMsgdata = self.msgs[msgType]
        if msgType in self.msgInfoDict.keys():
            pushDataInfo = self.msgInfoDict.get(msgType, {})
        else:
            pushDataInfo = PMD.data.get(msgType, {})
        msgData = self.uiAdapter.movie.CreateObject()
        msgData.SetMember('iconPath', GfxValue(RES_PATH + str(pushDataInfo.get('iconId', 'notFound')) + '.dds'))
        msgData.SetMember('type', GfxValue(msgType))
        msgData.SetMember('shine', GfxValue(False))
        msgData.SetMember('tipDesc', GfxValue(gbk2unicode(pushDataInfo.get('tooltip', ''))))
        currentTime = utils.getNow()
        showEndTime = None
        for data in pushMsgdata.dataList:
            endTime = getEndTime(data)
            if endTime and endTime > currentTime:
                if showEndTime == None or showEndTime > endTime:
                    showEndTime = endTime

        showCountDown = PMD.data.get(msgType, {}).get('showTime', 0)
        if showCountDown and showEndTime:
            msgData.SetMember('endTime', GfxValue(showEndTime))
        if pushMsgdata.num > 1:
            msgData.SetMember('num', GfxValue(pushMsgdata.num))
        return msgData

    def onGetDynamicTip(self, *arg):
        msgType = int(arg[3][0].GetNumber())
        if msgType == uiConst.MESSAGE_TYPE_PUSH_XINMO_RECORD:
            return GfxValue(gbk2unicode(gameglobal.rds.ui.xinmoRecord._getPushMsgTip()))
        if msgType == uiConst.MESSAGE_TYPE_CRYSTAL_DEFENCE_UPDATE:
            return GfxValue(gbk2unicode(gameglobal.rds.ui.crystalDefenceMain.getPushMsgTip()))

    def _checkMsgTypeEnable(self, msgType, msgInfo):
        if msgInfo and msgInfo.get('iconId', 0) == '11601':
            return True
        if BigWorld.player()._isSoul():
            return PMD.data.get(msgType, {}).get('crossEnable', 0)
        return True

    def vanishCallBack(self, msgType):
        self.removePushMsg(msgType)


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
        endTime = 0
        currentEndTime = None
        for data in self.dataList:
            endTime = getEndTime(data)
            if endTime:
                if currentEndTime == None or endTime < currentEndTime:
                    currentEndTime = endTime

        return endTime
