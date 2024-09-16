#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/voidLunHuiBarProxy.o
import BigWorld
import gameglobal
import uiConst
import utils
import math
import formula
from uiProxy import UIProxy
from gameStrings import gameStrings
from guis import uiUtils
from helpers import tickManager
from guis.asObject import ASUtils
from guis.asObject import ASObject
from guis.asObject import TipManager
from data import sys_config_data as SCD
from cdata import team_endless_progress_data as TEPD
from data import fb_data as FD
COUNT_DOWN_SHOW = 60
PROGRESS_BAR_WIDTH = 248
SUB_BOSS_NUM = 5
SUB_BOSS_START_X = 2

class VoidLunHuiBarProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(VoidLunHuiBarProxy, self).__init__(uiAdapter)
        self.widget = None
        self.timer = None
        self.currentProgress = 0
        self.totalTime = 0
        self.orchinProgress = 0
        self.bossState = {}
        self.fbId = 0
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_VOID_LUNHUI_BAR, self.hide)

    def reset(self):
        self.flyEffect = None
        self.currTimePre = ''
        self.totalTime = 0
        self.currSkilledPre = ''
        self.endTime = 0
        self.currentProgress = 0
        self.bossState = {}

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_VOID_LUNHUI_BAR:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.reset()
        if self.timer:
            tickManager.stopTick(self.timer)
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_VOID_LUNHUI_BAR)

    def show(self):
        p = BigWorld.player()
        self.fbId = formula.getFubenNo(p.spaceNo)
        self.totalTime = FD.data.get(self.fbId, {}).get('teamEndlessDuration', 0)
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_VOID_LUNHUI_BAR)
        else:
            self.refreshInfo()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        ASUtils.setHitTestDisable(self.widget.countDown, True)
        if self.timer:
            tickManager.stopTick(self.timer)
        self.timer = tickManager.addTick(1, self.refreshTime)
        self.initBar()
        self.widget.bossMc.bossIcon.gotoAndStop('gray')

    def refreshTime(self):
        if not self.endTime:
            self.widget.countDown.countDown.text = ''
            self.widget.processBar.bar.timeBarMask.width = 0
            self.widget.processBar.bar.purpleCursor.x = SUB_BOSS_START_X
            return
        if len(self.bossesData) == len(self.bossState):
            self.widget.countDown.text = ''
            return
        remainTime = self.endTime - utils.getNow()
        if remainTime < 0:
            remainTime = 0
        if remainTime <= 60:
            self.widget.countDown.countDown.htmlText = "<font color = \'#FF0000\'>%s</font>" % self.formateTime(remainTime)
        else:
            self.widget.countDown.countDown.htmlText = self.formateTime(remainTime)
        if self.totalTime <= 0:
            timeLen = 0
        else:
            timeLen = (1 - remainTime * 1.0 / self.totalTime) * PROGRESS_BAR_WIDTH
            timeLen = min(PROGRESS_BAR_WIDTH, timeLen)
        self.widget.processBar.bar.timeBarMask.width = timeLen
        self.widget.processBar.bar.purpleCursor.x = SUB_BOSS_START_X + timeLen
        if remainTime < 0:
            self.widget.processBar.bar.purpleCursor.gotoAndStop('special')
        else:
            self.widget.processBar.bar.purpleCursor.gotoAndStop('normal')

    def formateTime(self, time):
        minute = int(time / 60)
        sec = int(time - minute * 60)
        return '%02d:%02d' % (minute, sec)

    def refreshInfo(self):
        if not self.widget:
            return
        self.updateProgress()
        self.updateGoals()

    def initBar(self):
        self.bossesData = self.getAllBossData(self.fbId)
        self.bossesData.sort()
        tempProgress = 0
        for i, order in enumerate(self.bossesData):
            goal = self.widget.getChildByName('goal%s' % i)
            bossData = TEPD.data.get((self.fbId, order), {})
            if goal:
                goal.visible = True
                goal.order = order
                goal.bossName = bossData.get('bossName', '')
                self.updateGoalTextField(i, 'accept')
            bossIcon = self.widget.processBar.bar.getChildByName('subBoss%d' % i)
            tempProgress = bossData.get('progressAdd', 0) * 1.0 / 1000
            if bossIcon:
                bossIcon.visible = True
                bossIcon.gotoAndStop('weijisha')
                bossIcon.order = order
                bossIcon.x = SUB_BOSS_START_X + tempProgress * PROGRESS_BAR_WIDTH

        if len(self.bossesData) <= SUB_BOSS_NUM:
            for i in xrange(len(self.bossesData) - 1, SUB_BOSS_NUM):
                bossIcon = self.widget.processBar.bar.getChildByName('subBoss%d' % i)
                if bossIcon:
                    bossIcon.visible = False

            for i in xrange(len(self.bossesData), SUB_BOSS_NUM):
                goal = self.widget.getChildByName('goal%s' % i)
                if goal:
                    goal.visible = False

        self.updateProgress()

    def updateEndTime(self, endTime):
        self.endTime = endTime

    def onBossFinished(self, bossOrder, orchinProgress = 0):
        self.orchinProgress = orchinProgress
        if bossOrder and not self.bossState.has_key(bossOrder):
            self.bossState[bossOrder] = 1
            self.refreshInfo()
        else:
            self.updateProgress()

    def onGetBossOrders(self, bossOrderList, orchinProgress = 0):
        self.orchinProgress = orchinProgress
        for bossOrder in bossOrderList:
            self.bossState[bossOrder] = 1

        self.refreshInfo()

    def updateGoals(self):
        for i, order in enumerate(self.bossesData):
            if order in self.bossState:
                self.updateGoalTextField(i, 'complete')

    def updateProgress(self):
        if not self.widget:
            return
        self.currentProgress = self.getCurrentProgress()
        for i in xrange(len(self.bossState)):
            if i == len(self.bossesData) - 1:
                self.widget.bossMc.bossIcon.gotoAndStop('killed')
            else:
                bossIcon = self.widget.processBar.bar.getChildByName('subBoss%d' % i)
                bossIcon.gotoAndStop('jisha')

        maxWidth = PROGRESS_BAR_WIDTH
        width = maxWidth * self.currentProgress
        self.widget.processBar.bar.skilledBarMask.width = width

    def getAllBossData(self, fbId):
        bossesData = []
        for key in TEPD.data:
            if key[0] == fbId:
                bossesData.append(key[1])

        return bossesData

    def getCurrentProgress(self):
        progress = 0
        for order in self.bossState:
            progress = max(progress, TEPD.data.get((self.fbId, order), {}).get('progressAdd', 0) * 1.0 / 1000)

        progress += self.orchinProgress * 1.0 / 1000
        return min(progress, 1)

    def updateGoalTextField(self, szStr, state):
        goal = self.widget.getChildByName('goal%s' % szStr)
        if goal:
            bossName = goal.bossName
            goal.gotoAndStop('danhang')
            goalAction = goal.singleLine
            goalAction.gotoAndPlay(state)
            if state == 'complete':
                goalItem = goalAction.goalCompleteMc
            else:
                goalItem = goalAction.goalMc
            goalItem.goalIcon.gotoAndStop('boss')
            goalItem.goalText.text = gameStrings.LUNHUI_TARGET_GOAL % bossName
