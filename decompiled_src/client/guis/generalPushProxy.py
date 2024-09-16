#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/generalPushProxy.o
import BigWorld
import gameglobal
import utils
import gamelog
from guis import events
from guis import uiConst
from guis import generalPushMappings
from guis.asObject import ASUtils
from data import general_push_icon_data as GPID
from uiProxy import UIProxy
from helpers import tickManager
from callbackHelper import Functor
from crontab import CronTab, defaultTimezone
PUSH_ITEM_WIDTH = 80
PUSH_ITEM_HEIGHT = 80

class GeneralPushItemProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GeneralPushItemProxy, self).__init__(uiAdapter)
        self.widget = None
        self.pushState = 0
        self.parent = None
        self.pushId = 0
        self.pushEndTime = 0
        self.isCountOver = False
        self.isPrepare = False

    def countOver(self):
        self.isCountOver = True
        return self.onEndPushTime()

    def inShowState(self):
        return False

    def isShowHintEff(self):
        return True

    def onEndPushTime(self):
        return True

    def isPushItemEnabled(self, state):
        return True

    def onInitPushItem(self, widget):
        pass

    def onPushStateUpdate(self, state):
        pass

    def onClickItem(self, *args):
        pass

    def onPushTimeUpdated(self, time):
        pass

    def refreshItem(self):
        if not self.widget:
            return
        pushData = GPID.data.get((self.pushId, self.pushState), {})
        labels = [pushData.get('name', ''), pushData.get('subTitle', '')]
        if self.isPrepare:
            labels = [pushData.get('name', ''), pushData.get('prepareTitle', '')]
        self.widget.gotoAndPlay('notifyAnim' if self.isShowHintEff() else 'noEff')
        self.widget.mainBtn.labels = labels

    def updatePushTime(self, time):
        if self.widget:
            if time <= 3600:
                self.setTimeMcVisible(True)
                self.widget.countdown.textField.text = self.formateTime(time)
            else:
                self.setTimeMcVisible(False)
        self.onPushTimeUpdated(time)

    def setTimeMcVisible(self, visible):
        if self.widget:
            self.widget.countdown.visible = visible

    def formateTime(self, time):
        minute = int(time / 60)
        sec = time - minute * 60
        return '%02d:%02d' % (minute, sec)

    def prepareStateUpdate(self, isPrepare):
        if self.isPrepare != isPrepare:
            self.isPrepare = isPrepare
            self.refreshItem()

    def pushStateUpdate(self, state, pushEndTime = 0):
        self.isCountOver = False
        self.pushState = state
        self.pushEndTime = pushEndTime
        self.refreshItem()
        self.onPushStateUpdate(state)

    def initPushItem(self, widget, parent, pushId):
        self.parent = parent
        self.pushId = pushId
        self.widget = widget
        self.refreshItem()
        self.widget.mainBtn.addEventListener(events.MOUSE_CLICK, self.onClickItem)
        self.onInitPushItem(widget)

    def hideItem(self):
        self.parent.hidePushItem(self)
        self.widget.visible = False
        self.parent = None
        self.clearWidget()

    def clearWidget(self):
        pass


class GeneralPushProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GeneralPushProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        self.tickId = 0
        self.pushItems = {}
        self.callBackParams = []
        self.crontabCache = {}
        self.addEvent(event=events.EVENT_GENERAL_PUSH_STATECHANGE, call=self.onGeneralPushStateChange, priority=0, isGlobal=True)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_GENERAL_PUSH:
            self.widget = widget
            self.initUI()
            self.refreshInfo()
            if self.callBackParams:
                for params in self.callBackParams:
                    self.onGeneralPushStateChange(params)

                self.callBackParams = []

    def clearWidget(self):
        self.widget = None
        if self.tickId:
            tickManager.stopTick(self.tickId)
        self.tickId = 0
        self.pushItems = {}
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_GENERAL_PUSH)

    def show(self):
        if self.tickId:
            tickManager.stopTick(self.tickId)
        self.tickId = 0
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_GENERAL_PUSH)
        self.tickId = tickManager.addTick(1, self.timeTick)

    def timeTick(self):
        self.refreshInfo()

    def initUI(self):
        pass

    def getRenderClassName(self, pushId, state):
        pushType = GPID.data.get((pushId, state), {}).get('type', 0)
        if pushType == 1:
            return 'GeneralPush_FightPushItem'
        elif pushType == 3:
            return 'GeneralPush_Common'
        else:
            return 'GeneralPush_XiuXianPushItem'

    def hasPushStateData(self, pushId, state):
        return GPID.data.has_key((pushId, state))

    def addCacheParams(self, params):
        for i, val in enumerate(self.callBackParams):
            if params.data[0] == val.data[0]:
                self.callBackParams[i] = params
                return

        self.callBackParams.append(params)

    def onGeneralPushStateChange(self, params):
        data = params.data
        gamelog.debug('dxk@generalPushProxy onGeneralPushStateChange:', data)
        if not self.widget:
            self.show()
            self.addCacheParams(params)
            return
        if len(data) == 3:
            pushId, state, endTime = data
        else:
            pushId, state = data
            endTime = 0
        if not self.hasPushStateData(pushId, state):
            return
        self.tryAddPushItem(pushId, state)
        if pushId in self.pushItems:
            pushItem = self.pushItems[pushId]
            pushItem.pushStateUpdate(state, endTime)
            self.refreshInfo()

    def GetCrontabTime(self, str):
        currTime = utils.getNow()
        if self.crontabCache.has_key(str):
            croTime = self.crontabCache[str]
            if croTime > currTime:
                return croTime
        cacheTime = CronTab(str).next(utils.getNow()) + currTime
        self.crontabCache[str] = cacheTime
        return cacheTime

    def calcShowRange(self, pushId, state):
        pushData = GPID.data.get((pushId, state), {})
        pushStartTimes = pushData.get('startTimes', [])
        pushEndTimes = pushData.get('endTimes', [])
        if not (pushEndTimes and pushStartTimes):
            return (True, 0, 0)
        nextStartTime = min([ self.GetCrontabTime(s) for s in pushStartTimes ])
        nextEndTime = min([ self.GetCrontabTime(s) for s in pushEndTimes ])
        if nextStartTime < nextEndTime:
            return (False, nextStartTime, nextEndTime)
        return (True, nextStartTime, nextEndTime)

    def isInPrepareRange(self, pushId, state, startTime):
        pushData = GPID.data.get((pushId, state), {})
        prepTime = pushData.get('prepareTime', 0)
        if prepTime and startTime:
            if utils.getNow() + prepTime >= startTime:
                return True
        return False

    def refreshInfo(self):
        if not self.widget:
            return
        if not gameglobal.rds.configData.get('enableGeneralPush', False):
            self.widget.visible = False
        for pushId in self.pushItems:
            pushItem = self.pushItems[pushId]
            itemMc = self.widget.getChildByName('pushItem%s' % str(pushId))
            if not itemMc:
                if not self.hasPushStateData(pushId, pushItem.pushState):
                    continue
                self.tryAddPushItem(pushId, pushItem.pushState)
                itemMc = self.widget.getChildByName('pushItem%s' % str(pushId))
            if not itemMc:
                gamelog.error('dxk@generalPushProxy cannot add the pusItem:[pushId]:', pushId, pushItem)
                continue
            if not self.hasPushStateData(pushId, pushItem.pushState) or not pushItem.isPushItemEnabled(pushItem.pushState):
                self.setPushItemVisible(pushId, False)
                continue
            isInshowRange, startTime, endTime = self.calcShowRange(pushId, pushItem.pushState)
            isInPrepareRange = False
            if not isInshowRange:
                isInPrepareRange = self.isInPrepareRange(pushId, pushItem.pushState, startTime)
            inShowState = pushItem.inShowState()
            if isInPrepareRange:
                self.setPushItemVisible(pushId, True)
                pushItem.prepareStateUpdate(True)
                leftTime = startTime - utils.getNow()
                if leftTime <= 0:
                    leftTime = 0
                pushItem.updatePushTime(leftTime)
            elif isInshowRange or inShowState:
                self.setPushItemVisible(pushId, True)
                pushItem.prepareStateUpdate(False)
                if endTime:
                    leftTime = endTime - utils.getNow()
                    if leftTime <= 0:
                        leftTime = 0
                    pushItem.updatePushTime(leftTime)
                    if leftTime == 0:
                        pushItem.hideItem()
                elif pushItem.pushEndTime and not pushItem.isCountOver:
                    leftTime = pushItem.pushEndTime - utils.getNow()
                    if leftTime <= 0:
                        leftTime = 0
                    pushItem.updatePushTime(leftTime)
                    if leftTime == 0:
                        if pushItem.countOver():
                            pushItem.hideItem()
                else:
                    pushItem.setTimeMcVisible(False)
            else:
                self.setPushItemVisible(pushId, False)

    def tryAddPushItem(self, pushId, state):
        if pushId in self.pushItems:
            itemMc = self.widget.getChildByName('pushItem%s' % str(pushId))
            if itemMc:
                return
        pushItem = generalPushMappings.getGeneralPushProxy(pushId)
        if pushItem:
            pushMc = self.widget.getInstByClsName(self.getRenderClassName(pushId, state))
            pushMc.name = 'pushItem%s' % str(pushId)
            self.widget.addChild(pushMc)
            pushItem.initPushItem(pushMc, self, pushId)
            self.pushItems[pushId] = pushItem
            self.relayOutItems()
        else:
            gamelog.error('dxk@generalPushProxy cannot get proxy by generalPushMappings.getGeneralPushProxy, pushId:', pushId)

    def setPushItemVisible(self, pushId, visible):
        if pushId not in self.pushItems:
            gamelog.debug("dxk@generalPush hidePushItem:can\'t find The PushItem")
            return
        itemMc = self.widget.getChildByName('pushItem%s' % str(pushId))
        if itemMc.visible != visible:
            itemMc.visible = visible
            self.relayOutItems()

    def relayOutItems(self):
        initX = -86
        initY = -86
        for pushId in self.pushItems:
            pushMc = self.widget.getChildByName('pushItem%s' % str(pushId))
            if pushMc.visible:
                pushMc.x = initX
                pushMc.y = initY
                initX += PUSH_ITEM_WIDTH

    def removePushItem(self, pushId):
        if pushId not in self.pushItems:
            gamelog.debug("dxk@generalPush removePushItem:can\'t find The PushItem")
            return
        itemMc = self.widget.getChildByName('pushItem%s' % str(pushId))
        self.widget.removeChild(itemMc)
        del self.pushItems[pushId]
