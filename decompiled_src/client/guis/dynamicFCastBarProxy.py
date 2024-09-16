#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/dynamicFCastBarProxy.o
import BigWorld
import gameglobal
import uiConst
import const
from uiProxy import UIProxy
from guis import uiUtils
from data import quest_marker_data as QMD
PROGRESS_BAR_WIDTH = 307

class DynamicFCastBarProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(DynamicFCastBarProxy, self).__init__(uiAdapter)
        self.widget = None
        self.totalTime = 0
        self.startTime = 0
        self.prePTime = 0
        self.currPTime = 0
        self.upTime = 0
        self.markerId = 0
        self.callback = None
        self.barType = ''
        self.indirect = 1
        uiAdapter.registerEscFunc(uiConst.WIDGET_DYNAMIC_F_CAST_BAR, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_DYNAMIC_F_CAST_BAR:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def show(self):
        if self.widget:
            self.refreshInfo()
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_DYNAMIC_F_CAST_BAR)

    def clearWidget(self):
        if self.uiAdapter.isHideAllUI():
            self.uiAdapter.setVisRecord(uiConst.WIDGET_DYNAMIC_F_CAST_BAR, False)
        self.widget = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_DYNAMIC_F_CAST_BAR)

    def reset(self):
        self.totalTime = 0
        self.startTime = 0
        self.prePTime = 0
        self.currPTime = 0
        self.upTime = 0
        self.markerId = 0
        self.callback = None
        self.barType = ''
        self.indirect = 1

    def initUI(self):
        pass

    def refreshInfo(self):
        if not self.widget:
            return
        if self.barType == 'indirect':
            self.updateIconAndDesc()
            self.updateIndirectPressInfo()
        elif self.barType == 'hold':
            self.updateIconAndDesc()
            self.updateHoldPressInfo()

    def updateIndirectPressInfo(self):
        if not self.widget:
            self.stopCallback()
            return
        p = BigWorld.player()
        diff = max(self.currPTime - self.prePTime, p.getServerTime() - self.prePTime)
        if diff >= 0 and diff <= self.indirect or p.checkInAutoQuest():
            self.updateCastBar()
        else:
            self.widget.castBar.barMask.width = 0.1
            self.startTime = 0
            self.totalTime = 0
            self.prePTime = 0
            self.currPTime = 0
            self.stopAction()
            self.stopCallback()

    def updateCastBar(self):
        p = BigWorld.player()
        pastTime = p.getServerTime() - self.startTime
        if self.totalTime < pastTime:
            p.useMarkerNpc(self.markerId)
            self.stopAction()
            self.stopCallback()
            return
        currBarW = PROGRESS_BAR_WIDTH * pastTime / self.totalTime
        self.widget.castBar.barMask.width = currBarW
        self.callback = BigWorld.callback(0, self.updateIndirectPressInfo)

    def startIndirectPress(self, time, indirectTime, markerId):
        if not self.checkQuestMarker(markerId):
            if self.widget:
                self.hide()
            return
        self.barType = 'indirect'
        if not self.startTime:
            self.startTime = time
            self.totalTime = indirectTime[0]
            self.indirect = indirectTime[1]
            self.prePTime = time
            self.markerId = markerId
            self.playAction()
        if self.currPTime:
            self.prePTime = self.currPTime
        self.currPTime = time
        self.show()

    def stopCallback(self):
        if self.callback:
            BigWorld.cancelCallback(self.callback)
            self.callback = None

    def updateIconAndDesc(self):
        fKey = QMD.data.get(self.markerId, {}).get('fKey', 0)
        path, desc = uiUtils.getFKeyPathDesc(fKey)
        self.widget.castBar.iconShell.iconMc.loadImage(path)
        self.widget.castBar.midText.text = desc

    def playAction(self):
        p = BigWorld.player()
        qmd = QMD.data.get(self.markerId, {})
        triggerType = qmd.get('triggerType', 0)
        if triggerType in (const.EMOTION_TRIGGER, const.BIGEMOTION_TRIGGER):
            otherActionId = qmd.get('otherActionId', None)
            if otherActionId:
                p._startActionProgress(None, otherActionId, None, None, None)

    def stopAction(self):
        p = BigWorld.player()
        otherActionId = QMD.data.get(self.markerId, {}).get('otherActionId', None)
        if otherActionId:
            p._endActionProgress(False, otherActionId)

    def startHoldPress(self, time, holdTime, markerId):
        if not self.checkQuestMarker(markerId):
            if self.widget:
                self.hide()
            return
        self.barType = 'hold'
        if not self.startTime:
            self.startTime = time
            self.totalTime = holdTime
            self.markerId = markerId
            self.playAction()
        self.show()

    def updateHoldPressInfo(self):
        if not self.widget:
            self.stopCallback()
            return
        p = BigWorld.player()
        pastTime = p.getServerTime() - self.startTime
        diff = max(self.upTime - self.startTime, 0)
        if diff > 0 and diff < self.totalTime and not p.checkInAutoQuest():
            self.widget.castBar.barMask.width = 0.1
            self.startTime = 0
            self.totalTime = 0
            self.upTime = 0
            self.stopAction()
            self.stopCallback()
        elif self.totalTime < pastTime:
            p.useMarkerNpc(self.markerId)
            self.stopAction()
            self.stopCallback()
        else:
            currBarW = PROGRESS_BAR_WIDTH * pastTime / self.totalTime
            self.widget.castBar.barMask.width = currBarW
            self.callback = BigWorld.callback(0, self.updateHoldPressInfo)

    def recordHoldPressUpTime(self, isDown, time):
        if self.barType != 'hold':
            return
        if not isDown:
            self.upTime = time

    def checkQuestMarker(self, markerId):
        p = BigWorld.player()
        qmd = QMD.data[markerId]
        if qmd.has_key('quest'):
            questId = qmd['quest']
            if questId not in p.quests:
                return False
        if qmd.has_key('notFailQuest'):
            if any([ p.getQuestData(qid, const.QD_FAIL, False) for qid in qmd['notFailQuest'] ]):
                return False
        return True
