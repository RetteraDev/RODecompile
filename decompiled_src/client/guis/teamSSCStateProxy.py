#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/teamSSCStateProxy.o
import BigWorld
import gameglobal
import uiConst
import utils
import gametypes
from uiProxy import UIProxy
from data import duel_config_data as DCD
from gamestrings import gameStrings
ROUND_IN_TYPE = 0
ROUND_END_TYPE = 1
ROUND_END_WAIT_NEXT_TYPE = 2

class TeamSSCStateProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(TeamSSCStateProxy, self).__init__(uiAdapter)
        self.widget = None
        self.handler = None
        self.reset()

    def reset(self):
        self.topText = None
        self.bottomText = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_TEAM_SSC_STATE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_TEAM_SSC_STATE)
        self.handler and BigWorld.cancelCallback(self.handler)
        self.handler = None

    def show(self, topText, bottomText):
        self.topText = topText
        self.bottomText = bottomText
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_TEAM_SSC_STATE)
        else:
            self.refreshInfo()

    def initUI(self):
        self.refreshInfo()

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.content.topLineTf.htmlText = self.topText
        self.widget.content.bottomLineTf.htmlText = self.bottomText

    def onRefreshStateText(self):
        topText, bottomText = self.getText()
        if not topText or not bottomText:
            self.hide()
        else:
            self.show(topText, bottomText)

    def getText(self):
        p = BigWorld.player()
        state = p.teamShengSiChangStatus
        topLineText = ''
        bottomLineText = ''
        if state in [gametypes.TEAM_SHENG_SI_CHANG_STATUS_IN_SSC, gametypes.TEAM_SHENG_SI_CHANG_STATUS_START]:
            if hasattr(p, 'sscStatsInfo'):
                topLineText = DCD.data.get('roundIn_upgradeText', 'win %d') % p.sscStatsInfo.get('winNum', 0)
                bottomLineText = DCD.data.get('roundIn_aliveText', 'live %d') % p.sscStatsInfo.get('aliveMen', 0)
        elif state in [gametypes.TEAM_SHENG_SI_CHANG_STATUS_CONFIRMING, gametypes.TEAM_SHENG_SI_CHANG_STATUS_CONFIRMED]:
            countDownInfo = getattr(p, 'teamSSCCountDownData', None)
            if countDownInfo and not countDownInfo.get('isFirst', False) and self.getStartRemainTime(countDownInfo) > 0:
                topLineText = DCD.data.get('roundWaitNext_hintText', 'wait1')
                bottomLineText = DCD.data.get('roundWaitNext_startRemainTime', 'wait2 %d') % self.getStartRemainTime(countDownInfo)
        elif state in (gametypes.TEAM_SHENG_SI_CHANG_STATUS_WIN_STANDBY, gametypes.TEAM_SHENG_SI_CHANG_STATUS_NEW_RULE_SPECIAL) and not p.isTeamSSCFinalRound():
            if gameglobal.rds.configData.get('enableNewMatchRuleSSC', False) and getattr(p, 'sscStageLv', 0):
                currRankLv = getattr(p, 'sscRankLv', '1')
                topLineText = gameStrings.SSC_STAND_BY_LV_TITLE % (currRankLv, p.sscStageLv)
            else:
                topLineText = DCD.data.get('roundEnd_hintText', 'wait other')
            bottomLineText = DCD.data.get('roundEnd_notEndText', 'not end %d') % getattr(p, 'teamSSCRoundNotFinishCnt', 0)
        return (topLineText, bottomLineText)

    def getStartRemainTime(self, msgData):
        totalTime = msgData.get('totalTime', 45)
        startTime = msgData.get('startTime', utils.getNow())
        return int(max(totalTime - (utils.getNow() - startTime), 0))

    def onUpdateStateText(self):
        self.onRefreshStateText()
        status = BigWorld.player().teamShengSiChangStatus
        if status in [gametypes.TEAM_SHENG_SI_CHANG_STATUS_CONFIRMING, gametypes.TEAM_SHENG_SI_CHANG_STATUS_CONFIRMED]:
            self.startRefresh()
        else:
            self.stopRefresh()

    def startRefresh(self):
        self.handler and BigWorld.cancelCallback(self.handler)
        if not BigWorld.player():
            self.handler = None
            return
        else:
            self.onRefreshStateText()
            self.handler = BigWorld.callback(0.5, self.startRefresh)
            return

    def stopRefresh(self):
        self.handler and BigWorld.cancelCallback(self.handler)
        self.handler = None
