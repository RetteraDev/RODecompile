#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/LZYDPushProxy.o
import BigWorld
import uiConst
import events
import utils
import gamelog
import gameglobal
import formula
from gamestrings import gameStrings
from uiProxy import UIProxy
ACTIVITY_PREPARE = 1
ACTIVITY_COMPETITION = [2,
 3,
 4,
 5,
 6,
 7]
ACTIVITY_END = 8
ACTIVITY_CLOSE = 0
MAX_ROUND = 6
from data import arena_mode_data as AMD

class LZYDPushProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(LZYDPushProxy, self).__init__(uiAdapter)
        self.reset()

    def reset(self):
        self.timer = 0
        self.widget = None
        self.arenaMode = None
        self.activityState = 0
        self.round = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_LZYD_PUSH:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_LZYD_PUSH)

    def show(self):
        if not gameglobal.rds.configData.get('enableLunZhanYunDian', False):
            return
        p = BigWorld.player()
        self.arenaMode = gameglobal.rds.ui.lunZhanYunDian.getArenaMode()
        if not self.arenaMode:
            return
        minLv, maxLv = formula.getArenaLvByMode(self.arenaMode)
        if p.lv < minLv or p.lv > maxLv:
            return
        if not self.widget:
            self.timer = 0
            self.uiAdapter.loadWidget(uiConst.WIDGET_LZYD_PUSH)
        self.refreshInfo()

    def initUI(self):
        self.widget.button.addEventListener(events.BUTTON_CLICK, self.handleBtnClick, False, 0, True)

    def handleBtnClick(self, *args):
        gameglobal.rds.ui.lunZhanYunDian.show()

    def getData(self):
        timeDesc, roundDesc = (0, 0)
        now = utils.getNow()
        startTime, endTime, duration = self.getTime()
        arenaData = AMD.data.get(self.arenaMode, {})
        matchTimes = arenaData.get('matchTimes', [])
        if not matchTimes:
            return (timeDesc, roundDesc)
        if self.activityState == ACTIVITY_PREPARE:
            if now >= startTime or not gameglobal.rds.configData.get('enableDuelTimeCheck', False):
                timeStr = utils.formatCustomTime(int(utils.getNextCrontabTime(matchTimes[0])), '%H:%M')
                timeDesc = gameStrings.LZYD_PUSH_NEXT_ROUND_DESC % timeStr
                roundDesc = gameStrings.LZYD_ROUND_NOT_OPEN
        elif self.activityState in ACTIVITY_COMPETITION:
            if now < endTime or not gameglobal.rds.configData.get('enableDuelTimeCheck', False):
                round = self.activityState - 1
                roundDesc = gameStrings.LZYD_PUSH_ROUND_DESC % round
                if round == MAX_ROUND:
                    timeDesc = ''
                else:
                    timeStr = utils.formatCustomTime(int(utils.getNextCrontabTime(matchTimes[round])), '%H:%M')
                    timeDesc = gameStrings.LZYD_PUSH_NEXT_ROUND_DESC % timeStr
                self.round = round
        return (timeDesc, roundDesc)

    def refreshInfo(self):
        if not self.widget:
            return
        timeStr, round = self.getData()
        if not timeStr and not round:
            self.widget.tipsText.visible = False
            return
        self.widget.tipsText.visible = True
        self.widget.tipsText.txtName0.htmlText = round
        self.widget.tipsText.txtName1.htmlText = timeStr

    def getTime(self):
        self.arenaMode = gameglobal.rds.ui.lunZhanYunDian.getArenaMode()
        arenaData = AMD.data.get(self.arenaMode, {})
        startCron = arenaData.get('startTimes', (utils.CRON_ANY,))[0]
        endCron = arenaData.get('endTimes', (utils.CRON_ANY,))[0]
        startTime = utils.getNextCrontabTime(startCron)
        endTime = utils.getNextCrontabTime(endCron)
        if not utils.isSameWeek(startTime, utils.getNow()):
            startTime = utils.getPreCrontabTime(startCron)
        if not utils.isSameWeek(endTime, utils.getNow()):
            endTime = utils.getPreCrontabTime(endCron)
        closeDelayTime = arenaData.get('closeDelayTime', 1800)
        return (startTime, endTime, closeDelayTime)

    def onChangeLZYDState(self, state):
        startTime, endTime, closeDelayTime = self.getTime()
        closeTime = endTime + closeDelayTime
        now = utils.getNow()
        if state == ACTIVITY_CLOSE:
            if now > closeTime or now < startTime:
                self.activityState = state
                self.hide()
                return
            self.activityState = ACTIVITY_END
            self.show()
        if state > 0 and state >= self.activityState:
            self.activityState = state
            if not gameglobal.rds.configData.get('enableDuelTimeCheck', False):
                self.show()
            elif utils.isSameDay(startTime, now):
                if now < startTime:
                    if self.timer:
                        BigWorld.cancelCallback(self.timer)
                        self.timer = 0
                    self.timer = BigWorld.callback(startTime - now, self.show)
                elif now > endTime:
                    self.hide()
                else:
                    self.show()
