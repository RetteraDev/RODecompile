#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/balanceArena2PersonInfoProxy.o
import BigWorld
import gametypes
import gameglobal
import uiConst
import utils
from guis.asObject import ASObject
from guis import events
from gamestrings import gameStrings
from uiProxy import UIProxy
from guis.asObject import TipManager
from data import duel_config_data as DCD
ZHENYINGCLOLR = ['',
 'bai',
 'huang',
 'lv',
 'lan']
ARENA_16_TEAM_NUM = [16,
 8,
 4,
 2,
 1]
ROUND_NUM = 4

class BalanceArena2PersonInfoProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BalanceArena2PersonInfoProxy, self).__init__(uiAdapter)
        self.widget = None
        self.cacahe = None
        self.version = 0
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_BALANCE_ARENA_2PERSON_INFO, self.hide)

    def reset(self):
        pass

    def getCurrentRound(self):
        champion = self.cacahe.stage.get(5, {}).get(1, [0])[0]
        if champion:
            return 4
        return getattr(self.cacahe, 'roundNum', 0) - 1

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_BALANCE_ARENA_2PERSON_INFO:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BALANCE_ARENA_2PERSON_INFO)

    def show(self):
        p = BigWorld.player()
        p.base.dArenaQueryTopSixteen(self.version)
        if not self.cacahe:
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_BALANCE_ARENA_2PERSON_INFO)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        zhenyingInfos = DCD.data.get('doubleArenaZhenYingInfo', {})
        for i in xrange(len(zhenyingInfos)):
            self.widget.getChildByName('camp%d' % i).text = zhenyingInfos.get(i + 1, {}).get('name', '')

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshState()
        self.refreshTeamInfos()

    def refreshTeamInfos(self):
        currRound = self.getCurrentRound()
        for round in xrange(ROUND_NUM):
            teamNum = ARENA_16_TEAM_NUM[round]
            for j in xrange(teamNum):
                teamMc = self.widget.getChildByName('team%d%d' % (round, j + 1))
                lineMc = self.widget.getChildByName('line%d%d' % (round, int(j / 2)))
                cameraMc = self.widget.getChildByName('camera%d%d' % (round, int(j / 2)))
                self.setTeamInfo(teamMc, lineMc, cameraMc, round, j)

        champion = self.cacahe.stage.get(5, {}).get(1, [0])[0]
        teamMc = self.widget.team41
        if champion:
            teamInfo = self.cacahe.teamList[champion]
            teamMc.unknownIcon.visible = False
            teamMc.teamName.text = teamInfo.teamName
            teamMc.teamColor.gotoAndStop(ZHENYINGCLOLR[teamInfo.camp])
        else:
            teamMc.unknownIcon.visible = True
            teamMc.teamColor.visible = False

    def canWatchLive(self):
        return utils.canInLiveOfArenaPlayoffs(BigWorld.player())

    def onWatchBtnClick(self, *args):
        e = ASObject(args[3][0])
        leaderGbId = long(e.currentTarget.leaderGbId)
        p = BigWorld.player()
        p.cell.dArenaStartObserve(leaderGbId)

    def setTeamInfo(self, teamMc, lineMc, cameraMc, round, teamIndex):
        if cameraMc:
            cameraMc.visible = False
        stageIndex = int(teamIndex / 2)
        roundInfo = self.cacahe.stage.get(round + 1, {})
        stageInfo = roundInfo.get(stageIndex + 1, [0, 0])
        nextRoundInfo = self.cacahe.stage.get(round + 2, {})
        nextStage = nextRoundInfo.get(int(stageIndex / 2) + 1, [])
        for i in xrange(2 - len(stageInfo)):
            stageInfo.append(0)

        isodd = teamIndex % 2 == 1
        teamId = 0
        emermyId = 0
        if round == 0:
            teamId = stageInfo[1] if isodd else stageInfo[0]
            emermyId = stageInfo[0] if isodd else stageInfo[1]
        else:
            lastRoundInfo = self.cacahe.stage.get(round, {})
            if not isodd:
                for id in stageInfo:
                    if id and id in lastRoundInfo.get((stageIndex + 1) * 2 - 1, [0, 0]):
                        teamId = id

                for id in stageInfo:
                    if id and id in lastRoundInfo.get((stageIndex + 1) * 2, [0, 0]):
                        emermyId = id

            else:
                for id in stageInfo:
                    if id and id in lastRoundInfo.get((stageIndex + 1) * 2 - 1, [0, 0]):
                        emermyId = id

                for id in stageInfo:
                    if id and id in lastRoundInfo.get((stageIndex + 1) * 2, [0, 0]):
                        teamId = id

        if isodd:
            if not self.isRoundOver(stageInfo, nextStage):
                lineMc.visible = False
            else:
                lineMc.visible = True
                if teamId and teamId in nextStage:
                    lineMc.gotoAndStop('state0')
                else:
                    lineMc.gotoAndStop('state1')
        if self.canWatchLive() and gameglobal.rds.configData.get('enableDoubleArenaAnnal', False):
            if self.isRoundOver(stageInfo, nextStage):
                cameraMc.visible = False
            elif emermyId and teamId:
                teamInfo = self.cacahe.teamList.get(teamId, None)
                emermyInfo = self.cacahe.teamList.get(emermyId, None)
                if teamInfo and emermyInfo:
                    cameraMc.visible = True
                    cameraMc.leaderGbId = teamInfo.gbId
                    cameraMc.addEventListener(events.MOUSE_CLICK, self.onWatchBtnClick, False, 0, True)
        if teamId:
            teamInfo = self.cacahe.teamList.get(teamId, None)
            if not teamInfo:
                teamMc.teamName.text = ''
                teamMc.unknownIcon.visible = True
                teamMc.loseIcon.visible = False
                teamMc.teamColor.visible = False
                p = BigWorld.player()
                msg = "Double Arena teamId Error,TeamList don\'t have key %s" % str(teamId)
                p.reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_SCRIPT, [msg], 0, {})
                return
            teamMc.teamName.text = teamInfo.teamName
            teamMc.teamColor.visible = True
            teamMc.teamColor.gotoAndStop(ZHENYINGCLOLR[teamInfo.camp])
            teamMc.unknownIcon.visible = False
            TipManager.addTip(teamMc, '%s\n%s' % (teamInfo.leaderName, teamInfo.mateName))
            if self.isRoundOver(stageInfo, nextStage):
                teamMc.loseIcon.visible = teamId not in nextStage
            else:
                teamMc.loseIcon.visible = False
        else:
            teamMc.teamName.text = ''
            teamMc.unknownIcon.visible = True
            teamMc.loseIcon.visible = False
            teamMc.teamColor.visible = False

    def isRoundOver(self, stageInfo, nexStage):
        for teamId in stageInfo:
            if teamId and teamId in nexStage:
                return True

        return False

    def refreshState(self):
        currentState = self.getCurrentRound()
        states = gameStrings.BALANCEARENA_16_STATES
        for i in xrange(len(states)):
            stateMc = self.widget.getChildByName('day%s' % str(i))
            if i < currentState:
                stateMc.gotoAndPlay('state3')
            elif i == currentState:
                stateMc.gotoAndPlay('state2')
            else:
                stateMc.gotoAndPlay('state1')
            stateMc.week.text = states[i]

    def onGetServerData(self, data):
        if data:
            self.cacahe = data
            self.version = data.version
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_BALANCE_ARENA_2PERSON_INFO)
        else:
            self.refreshInfo()

    def generateTestCase(self):
        testTeam1 = type('Team', (object,), {'mateName': 'ddd',
         'leaderName': 'dddx',
         'camp': 2,
         'teamName': 'XXX',
         'annalUUID': 11})
        testTeam2 = type('Team', (object,), {'mateName': 'dddd',
         'leaderName': 'ddddx',
         'camp': 1,
         'teamName': 'XXX2',
         'annalUUID': 11})
        testClass = type('DataTest', (object,), {'roundNum': 1,
         'version': 1,
         'stage': {1: {1: [1],
                       2: [3, 4]},
                   2: {1: [1]}},
         'teamList': {1: testTeam1,
                      2: testTeam2,
                      3: testTeam1,
                      4: testTeam2}})
        self.onGetServerData(testClass)
