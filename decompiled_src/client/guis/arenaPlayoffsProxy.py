#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/arenaPlayoffsProxy.o
from gamestrings import gameStrings
import BigWorld
import const
import gametypes
import utils
import copy
import gameglobal
import datetime
import formula
import gamelog
from guis import uiConst
from uiProxy import UIProxy
from guis import uiUtils
from pvPPanelProxy import PvPPanelProxy
from gameStrings import gameStrings
from helpers import taboo
from callbackHelper import Functor
from data import duel_config_data as DCD
from data import arena_playoffs_group_duel_data as APGDD
from cdata import game_msg_def_data as GMDD
from data import arena_playoffs_schedule_desc_data as APSDD
TYPE_GROUP_DUEL = 1
TYPE_FINAL_DUEL = 2

class ArenaPlayoffsProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ArenaPlayoffsProxy, self).__init__(uiAdapter)
        self.modelMap = {'selelctGroupResult': self.onSelelctGroupResult,
         'selectFinalResult': self.onSelectFinalResult,
         'showTeamInfo': self.onShowTeamInfo,
         'enterArenaWithLive': self.onEnterArenaWithLive}
        self.createTeamId = 0
        self.selectTeamInfo = (0, 0, '', 0)
        uiAdapter.registerEscFunc(uiConst.WIDGET_ARENA_PLAYOFFS_GROUP_MATCH, self.hideGroupView)
        uiAdapter.registerEscFunc(uiConst.WIDGET_ARENA_PLAYOFFS_FINIAL_DUAL, self.hideFinalView)
        uiAdapter.registerEscFunc(uiConst.WIDGET_VIEW_PLAYOFFS_TEAM_INFO, self.hideTeamInfo)
        self.groupMatchMed = None
        self.groupTeamInfos = {}
        self.groupDuleResults = {}
        self.selGroupIdx = 0
        self.selGroupLvKey = const.ARENA_PLAYOFFS_TEIM_KEY_1_59
        self.finalDuelResults = {}
        self.finalMed = None
        self.selFinalLvKey = const.ARENA_PLAYOFFS_TEIM_KEY_1_59
        self.teamDetails = {}
        self.teamDetailMed = None
        self.curArenaPlayoffsSeason = {}
        self.isNeedOpen = False
        self.reset()

    def _registerMediator(self, widgetId, mediator):
        p = BigWorld.player()
        if widgetId == uiConst.WIDGET_ARENA_PLAYOFFS_GROUP_MATCH:
            self.groupMatchMed = mediator
            initData = {'matchInfo': self.getGroupMatchInfo(),
             'hideLvKey': p.isBalancePlayoffs(),
             'isPlayoffs5V5': p.isPlayoffs5V5(),
             'keyIndexs': self.getKeyIndexs(),
             'groups': [ {'label': x} for x in DCD.data.get('arenaPlayoffsGroups', [0] * 8) ],
             'lvKeyIdx': self.getPlayerLvKeyIdx()}
            return uiUtils.dict2GfxDict(initData, True)
        if widgetId == uiConst.WIDGET_ARENA_PLAYOFFS_FINIAL_DUAL:
            self.finalMed = mediator
            dayLabels = []
            if p.isBalancePlayoffs():
                dayLabels = gameglobal.rds.ui.balanceArenaPlayoffs.getPlayoffsDayLabel()
            elif p.isPlayoffs5V5():
                dayLabels = gameglobal.rds.ui.arenaPlayoffs5v5Final.getPlayoffs5v5DayLabel()
            else:
                for key in sorted(APGDD.data.keys()):
                    val = APGDD.data[key]
                    lvKey = utils.lv2ArenaPlayoffsTeamkey(BigWorld.player().lv)
                    if val.get('type') == TYPE_FINAL_DUEL and lvKey == key[1]:
                        dayLabels.append({'week': val.get('week', ''),
                         'date': val.get('date', ''),
                         'state': self.getTimeState(val.get('startTime'), val.get('endTime'))})

            initData = {'lvKeyIdx': self.getPlayerLvKeyIdx(),
             'hideLvKey': p.isBalancePlayoffs(),
             'isPlayoffs5V5': p.isPlayoffs5V5(),
             'keyIndexs': self.getKeyIndexs(),
             'dayLabels': dayLabels}
            return uiUtils.dict2GfxDict(initData, True)
        if widgetId == uiConst.WIDGET_VIEW_PLAYOFFS_TEAM_INFO:
            self.teamDetailMed = mediator
            return uiUtils.dict2GfxDict(self.getGfxTeamDetail(), True)

    def getKeyIndexs(self):
        p = BigWorld.player()
        if p.isBalancePlayoffs():
            return [3, 3, const.ALL_ARENA_PLAYOFFS_TEAM_LV_KEYS.index(const.ARENA_PLAYOFFS_TEIM_KEY_BALANCE)]
        elif p.isPlayoffs5V5():
            return [4, 4, 5]
        else:
            return [0, 1, 2]

    def _asWidgetClose(self, widgetId, multiID):
        if widgetId == uiConst.WIDGET_ARENA_PLAYOFFS_GROUP_MATCH:
            self.hideGroupView()
        elif widgetId == uiConst.WIDGET_ARENA_PLAYOFFS_FINIAL_DUAL:
            self.hideFinalView()
        elif widgetId == uiConst.WIDGET_VIEW_PLAYOFFS_TEAM_INFO:
            self.hideTeamInfo()

    def reset(self):
        pass

    def showPlayoffsReport(self):
        p = BigWorld.player()
        self.isNeedOpen = False
        state = self.getCurrentPlayoffsState()
        if state == gametypes.CROSS_ARENA_PLAYOFFS_TEAM_STATE_GROUP_DUEL:
            self.uiAdapter.loadWidget(uiConst.WIDGET_ARENA_PLAYOFFS_GROUP_MATCH)
        elif state == gametypes.CROSS_ARENA_PLAYOFFS_TEAM_STATE_FINAL_DUEL:
            self.uiAdapter.loadWidget(uiConst.WIDGET_ARENA_PLAYOFFS_FINIAL_DUAL)
        else:
            p.showGameMsg(GMDD.data.ARENA_PLAYOFFS_NO_REPORT, ())

    def hideGroupView(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ARENA_PLAYOFFS_GROUP_MATCH)
        self.groupMatchMed = None
        self.selGroupIdx = 0
        self.selGroupLvKey = const.ARENA_PLAYOFFS_TEIM_KEY_1_59

    def hideFinalView(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ARENA_PLAYOFFS_FINIAL_DUAL)
        self.finalMed = None

    def showArenaPlayoffsTeamInfo(self, nuid, hostId, score, rank, lvKey):
        self.selectTeamInfo = (nuid,
         hostId,
         score,
         rank)
        if self.teamDetailMed:
            self.refreshTeamDetail()
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_VIEW_PLAYOFFS_TEAM_INFO)
        if not self.teamDetails.has_key(nuid):
            BigWorld.player().cell.queryArenaPlayoffsTeamDetail(hostId, lvKey, nuid)

    def hideTeamInfo(self):
        self.selectTeamInfo = (0, 0, '', 0)
        self.teamDetailMed = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_VIEW_PLAYOFFS_TEAM_INFO)

    def showCreateTeam(self):
        if self.getCurrentPlayoffsState() != 0:
            BigWorld.player().showGameMsg(GMDD.data.ARENA_PLAYOFFS_CREATE_TEAM_OUT_TIME_MSG, ())
            return
        self.hideCreateTeam()
        self.createTeamId = self.uiAdapter.messageBox.showYesNoInput(msg=gameStrings.TEXT_ARENAPLAYOFFSPROXY_161, yesCallback=self.onCreateTeam, title=gameStrings.TEXT_ARENAPLAYOFFSPROXY_163, inputMax=const.ARENA_PLAYOFFS_TEAM_NAME_MAX_LENGTH, style=uiConst.MSG_BOX_INPUT_STRING, dismissOnClick=False)

    def showCreateScoreTeam(self):
        p = BigWorld.player()
        if self.getCurrentPlayoffsState() != 0:
            BigWorld.player().showGameMsg(GMDD.data.ARENA_PLAYOFFS_CREATE_TEAM_OUT_TIME_MSG, ())
            return
        self.hideCreateTeam()
        self.createTeamId = self.uiAdapter.messageBox.showYesNoInput(msg=gameStrings.TEXT_ARENAPLAYOFFSPROXY_161, yesCallback=self.onCreateScoreTeam, title=gameStrings.TEXT_ARENAPLAYOFFSPROXY_163, inputMax=const.ARENA_PLAYOFFS_TEAM_NAME_MAX_LENGTH, style=uiConst.MSG_BOX_INPUT_STRING, dismissOnClick=False)

    def hideCreateTeam(self):
        if self.createTeamId:
            self.uiAdapter.messageBox.dismiss(self.createTeamId)
        self.createTeamId = 0

    def onCreateScoreTeam(self, inputStr):
        p = BigWorld.player()
        if len(inputStr):
            retval, _ = taboo.checkNameDisWord(inputStr)
            if not retval:
                p.showGameMsg(GMDD.data.ARENA_PLAYOFFS_TEAM_NAME_INVALID, ())
                return
            p.cell.buildArenaScoreTeam(const.ARENA_SCORE_TYPE_1, inputStr)
        else:
            p.showGameMsg(GMDD.data.ARENA_PLAYOFFS_TEAM_NAME_EMPTY, ())

    def onCreateTeam(self, inputStr):
        p = BigWorld.player()
        if len(inputStr):
            retval, _ = taboo.checkNameDisWord(inputStr)
            if not retval:
                p.showGameMsg(GMDD.data.ARENA_PLAYOFFS_TEAM_NAME_INVALID, ())
                return
            if p.isPlayoffs5V5():
                p.cell.buildArenaPlayoffsTeam(gametypes.ARENA_PLAYOFFS_TYPE_5V5, inputStr)
            else:
                p.cell.buildArenaPlayoffsTeam(gametypes.ARENA_PLAYOFFS_TYPE_3V3, inputStr)
        else:
            p.showGameMsg(GMDD.data.ARENA_PLAYOFFS_TEAM_NAME_EMPTY, ())

    def onArenaPlayoffsTeamInfoChanged(self):
        p = BigWorld.player()
        if p.getArenaPlayoffsTeamNUID():
            self.hideCreateTeam()
            if p.isBalancePlayoffs():
                self.uiAdapter.balanceArenaPlayoffs.refreshPlayoffsPanel()
            elif p.arenaPlayoffsTeamHeader and p.arenaPlayoffsTeamLvKey:
                if p.isPlayoffs5V5():
                    self.uiAdapter.pvpPlayoffs5V5.refreshPlayoffsPanel()
                else:
                    self.uiAdapter.pvpPlayoffsV2.refreshPlayoffsPanel()
        elif p.isBalancePlayoffs():
            self.uiAdapter.balanceArenaPlayoffs.refreshPlayoffsPanel()
        elif p.isPlayoffs5V5():
            self.uiAdapter.pvpPlayoffs5V5.refreshPlayoffsPanel()
        else:
            self.uiAdapter.pvpPlayoffsV2.refreshPlayoffsPanel()

    def onSelelctGroupResult(self, *args):
        selLvInx = args[3][0].GetNumber()
        selGroupIdx = args[3][1].GetNumber()
        lvKey = const.ALL_ARENA_PLAYOFFS_TEAM_LV_KEYS[selLvInx]
        self.selGroupIdx = selGroupIdx
        self.selGroupLvKey = lvKey
        gamelog.debug('dxk@arenaPlayoffs onSelelctGroupResult', self.selGroupLvKey, self.selGroupIdx, selLvInx)
        self.fetchTeamInfo(self.selGroupLvKey, self.selGroupIdx)
        self.fetchGroupDuleResult(self.selGroupLvKey, self.selGroupIdx)
        obj = self.getGroupMatchInfo()
        if self.groupMatchMed:
            self.groupMatchMed.Invoke('refreshMathces', uiUtils.dict2GfxDict(obj, True))

    def onSelectFinalResult(self, *args):
        selLvInx = args[3][0].GetNumber()
        self.selFinalLvKey = const.ALL_ARENA_PLAYOFFS_TEAM_LV_KEYS[selLvInx]
        self.fetchFinalResult(self.selFinalLvKey)
        self.refreshFinalDuelResultView()

    def select5V5FinalResult(self, selLvInx):
        self.selFinalLvKey = const.ALL_ARENA_PLAYOFFS_TEAM_LV_KEYS[selLvInx]
        self.fetchFinalResult(self.selFinalLvKey)
        p = BigWorld.player()
        if p.isPlayoffs5V5():
            self.refreshFinalDuelResultView()
            return

    def onShowTeamInfo(self, *args):
        nuid = int(args[3][0].GetString())
        hostId = int(args[3][1].GetNumber())
        score = args[3][2].GetString()
        rank = args[3][3].GetNumber()
        self.showArenaPlayoffsTeamInfo(nuid, hostId, score, rank, self.getCurSelLvKey())

    def refreshGroupDuleResultView(self):
        if self.groupMatchMed:
            self.groupMatchMed.Invoke('refreshMathces', uiUtils.dict2GfxDict(self.getGroupMatchInfo(), True))

    def refreshFinalDuelResultView(self):
        p = BigWorld.player()
        if p.isPlayoffs5V5():
            gameglobal.rds.ui.arenaPlayoffs5v5Final.refreshInfo()
        if self.finalMed:
            self.finalMed.Invoke('refreshFinalResult', uiUtils.dict2GfxDict(self.getFinalDuelResult(), True))

    def getMatchesSchedule(self):
        p = BigWorld.player()
        matchesSchedule = []
        schedule = self.getCurPlayoffsSchedule()
        firstRound = schedule['applyEndTime'] + datetime.timedelta(days=1)
        dayOffset = 0
        for i in xrange(0, 7):
            matchRound = firstRound + datetime.timedelta(days=dayOffset)
            mathchRoundDesc = {}
            now = utils.getNow()
            currentYear = datetime.datetime.fromtimestamp(now).year
            if not i % 2:
                matchRoundCrontab = '30 19 %d %d * %d' % (matchRound.day, matchRound.month, currentYear)
                matchRoundEnterCrontab = '20 19 %d %d * %d' % (matchRound.day, matchRound.month, currentYear)
            else:
                matchRoundCrontab = '40 20 %d %d * %d' % (matchRound.day, matchRound.month, currentYear)
                matchRoundEnterCrontab = '30 20 %d %d * %d' % (matchRound.day, matchRound.month, currentYear)
                dayOffset += 2
            mathchRoundDesc['startStage'] = 0
            if utils.inTimeRange(matchRoundEnterCrontab, matchRoundCrontab):
                if i % 2:
                    mathchRoundDesc['startStage'] = 1
                else:
                    mathchRoundDesc['startStage'] = 2
            matchTime = utils.getDisposableCronTabTimeStamp(matchRoundCrontab)
            macthDateTime = datetime.datetime.fromtimestamp(matchTime)
            matchEnterTime = utils.getDisposableCronTabTimeStamp(matchRoundEnterCrontab)
            matchDataEnterTime = datetime.datetime.fromtimestamp(matchEnterTime)
            mathchRoundDesc['week'] = gameStrings.ARENA_GROUP_MATCH_WEEK_TXT % gameStrings.NUM_TO_CN_WEEK[macthDateTime.weekday()]
            mathchRoundDesc['date'] = '%d.%d' % (macthDateTime.month, macthDateTime.day)
            mathchRoundDesc['time'] = gameStrings.ARENA_GROUP_MATCH_TIME_TXT % (macthDateTime.hour, macthDateTime.minute)
            mathchRoundDesc['startTime'] = '%d.%d.%d.19.0.0' % (macthDateTime.year, macthDateTime.month, macthDateTime.day)
            if i != 6:
                mathchRoundDesc['endTime'] = '%d.%d.%d.21.30.0' % (macthDateTime.year, macthDateTime.month, macthDateTime.day)
            else:
                mathchRoundDesc['endTime'] = '%d.%d.%d.20.20.0' % (macthDateTime.year, macthDateTime.month, macthDateTime.day)
            mathchRoundDesc['name'] = gameStrings.ARENA_GROUP_MATCH_ENTER_TIME_TXT % (matchDataEnterTime.hour, matchDataEnterTime.minute)
            matchesSchedule.append(mathchRoundDesc)

        return matchesSchedule

    def teamListSortFunc(self, groupDuelData, val1, val2):
        cmpReuslt = cmp(val1['score'], val2['score'])
        if cmpReuslt != 0:
            return cmpReuslt
        else:
            return self.cmpTeamWinAndScore(groupDuelData, val1['nuid'], val2['nuid'])

    def cmpTeamWinAndScore(self, groupDuelData, nuid0, nuid1):
        for idx in sorted(groupDuelData.keys()):
            matches = groupDuelData.get(idx)
            if not matches:
                continue
            for nuids, result in matches.items():
                if nuid0 == str(nuids[0]) and nuid1 == str(nuids[1]) and result.get('matchScore', ()):
                    team0 = self.getTeamInfoByNUID(nuids[0], self.selGroupLvKey, self.selGroupIdx)
                    team1 = self.getTeamInfoByNUID(nuids[1], self.selGroupLvKey, self.selGroupIdx)
                    matchScore = result.get('matchScore')
                    if matchScore[0] == matchScore[1]:
                        return cmp(team0.get('teamArenaScore', 0), team1.get('teamArenaScore'))
                    return cmp(matchScore[0], matchScore[1])
                if nuid1 == str(nuids[0]) and nuid0 == str(nuids[1]) and result.get('matchScore', ()):
                    team0 = self.getTeamInfoByNUID(nuids[0], self.selGroupLvKey, self.selGroupIdx)
                    team1 = self.getTeamInfoByNUID(nuids[1], self.selGroupLvKey, self.selGroupIdx)
                    matchScore = result.get('matchScore')
                    if matchScore[0] == matchScore[1]:
                        return cmp(team1.get('teamArenaScore', 0), team0.get('teamArenaScore'))
                    return cmp(matchScore[1], matchScore[0])

        return 0

    def getGroupMatchInfo(self):
        teamList = []
        p = BigWorld.player()
        teamInfo = self.getSelTeamInfo()
        for teamId, teamVal in teamInfo.get('data', {}).items():
            teamName = teamVal.get('teamName', '')
            teamList.append({'teamName': uiUtils.toHtml(teamName, '#77dd4b') if teamId == p.arenaPlayoffsTeamNUID else teamName,
             'score': teamVal.get('score', ''),
             'nuid': str(teamId),
             'serverName': utils.getServerName(teamVal.get('hostId', 0)),
             'hostId': teamVal.get('hostId', 0)})

        groupDuleResult = self.getGroupDuleResult()
        groupDuelData = groupDuleResult.get('data', {})
        teamList.sort(cmp=Functor(self.teamListSortFunc, groupDuelData), reverse=True)
        rankIds = {}
        for val in teamList:
            rankIds[int(val.get('nuid'))] = teamList.index(val) + 1

        allMatches = []
        dayMatches = {}
        twoGroupMatch = []
        if p.isBalancePlayoffs():
            matchesSchedule = gameglobal.rds.ui.balanceArenaPlayoffs.getMatchesSchedule()
        elif p.isPlayoffs5V5():
            matchesSchedule = gameglobal.rds.ui.pvpPlayoffs5V5.getMatchesSchedule()
        else:
            matchesSchedule = self.getMatchesSchedule()
        for idx in sorted(groupDuelData.keys()):
            matches = groupDuelData.get(idx)
            if not matches:
                continue
            for nuids, result in matches.items():
                team0 = self.getTeamInfoByNUID(nuids[0], self.selGroupLvKey, self.selGroupIdx)
                team1 = self.getTeamInfoByNUID(nuids[1], self.selGroupLvKey, self.selGroupIdx)
                team0['rank'] = rankIds.get(nuids[0], 0)
                team1['rank'] = rankIds.get(nuids[1], 0)
                if result.get('matchScore', ()):
                    state = 1
                    matchScore = result.get('matchScore')
                    team0['matchScore'] = matchScore[0]
                    team1['matchScore'] = matchScore[1]
                else:
                    team0['matchScore'] = ''
                    team1['matchScore'] = ''
                    state = 0
                twoGroupMatch.append({'teams': [team0, team1],
                 'nuid': nuids[0] if nuids[0] else nuids[1],
                 'state': state,
                 'idx': idx})

            desc = matchesSchedule[idx - 1]
            if idx % 2 == 1:
                dayMatches['state'] = self.getTimeState(desc.get('startTime'), desc.get('endTime'))
                dayMatches['matches'] = twoGroupMatch
                dayMatches['startStage'] = desc.get('startStage', 0) if utils.canInLiveOfArenaPlayoffs(BigWorld.player()) else 0
                dayMatches['canView'] = utils.canInLiveOfArenaPlayoffs(BigWorld.player())
                dayMatches['weekDayTxt'] = desc.get('week', '')
                if p.isPlayoffs5V5():
                    dayMatches['weekDayTxt'] = gameStrings.ARENA_5v5_GROUP_TITLE % str(idx)
                dayMatches['dateTxt'] = desc.get('date', '')
                dayMatches['stage1Txt'] = desc.get('name', '')
                dayMatches['time1Txt'] = desc.get('time', '')
                dayMatches['stage2Txt'] = ''
                dayMatches['time2Txt'] = ''
                dayMatches['weekDay2Txt'] = ''
                dayMatches['date2Txt'] = ''
                allMatches.append(dayMatches)
            elif idx % 2 == 0:
                dayMatches['state2'] = self.getTimeState(desc.get('startTime'), desc.get('endTime'))
                if p.isPlayoffs5V5():
                    dayMatches['weekDay2Txt'] = gameStrings.ARENA_5v5_GROUP_TITLE % str(idx)
                dayMatches['date2Txt'] = desc.get('date', '')
                dayMatches['stage2Txt'] = desc.get('name', '')
                dayMatches['time2Txt'] = desc.get('time', '')
                dayMatches = {}
                twoGroupMatch = []

        return {'teamList': teamList,
         'allMatches': allMatches}

    def onGetTeamInfo(self, lvKey, groupId, info):
        if lvKey and groupId >= 0:
            if not self.groupTeamInfos.has_key(lvKey):
                self.groupTeamInfos[lvKey] = [{}] * const.CROSS_ARENA_PLAYOFFS_GROUP_NUM
            self.groupTeamInfos[lvKey][groupId] = info
        else:
            return
        if self.getSelTeamInfo() and self.getGroupDuleResult():
            self.refreshGroupDuleResultView()

    def onGetGroupDuleResult(self, lvKey, groupId, result):
        if lvKey and groupId >= 0:
            if not self.groupDuleResults.has_key(lvKey):
                self.groupDuleResults[lvKey] = [{}] * const.CROSS_ARENA_PLAYOFFS_GROUP_NUM
            self.groupDuleResults[lvKey][groupId] = result
        else:
            return
        if self.getSelTeamInfo() and self.getGroupDuleResult():
            self.refreshGroupDuleResultView()

    def onGetFinalDuleResult(self, lvKey, result):
        self.finalDuelResults[lvKey] = result
        self.refreshFinalDuelResultView()

    def onQueryArenaPlayoffsTeamDetail(self, nuid, teamInfo, result):
        if teamInfo:
            teamInfo['members'] = result
            self.teamDetails[nuid] = teamInfo
            self.refreshTeamDetail()

    def getFinalDuelResult(self):
        dayLabels = []
        p = BigWorld.player()
        if p.isBalancePlayoffs():
            dayLabels = gameglobal.rds.ui.balanceArenaPlayoffs.getPlayoffsDayLabel()
        elif p.isPlayoffs5V5:
            dayLabels = gameglobal.rds.ui.arenaPlayoffs5v5Final.getPlayoffs5v5DayLabel()
        else:
            schedule = self.getCurPlayoffsSchedule()
            firstKickOutTime = schedule['kickOutStartTime']
            dayOffset = 0
            for i in xrange(0, 4):
                kickOutTime = firstKickOutTime + datetime.timedelta(days=dayOffset)
                dayOffset += 2
                week = gameStrings.ARENA_FINAL_MATCH_WEEK_TXT % (kickOutTime.month, kickOutTime.day)
                date = gameStrings.ARENA_FINAL_MATCH_DATA_TXT
                startTime = '%d.%d.%d.19.0.0' % (kickOutTime.year, kickOutTime.month, kickOutTime.day)
                endTime = '%d.%d.%d.22.0.0' % (kickOutTime.year, kickOutTime.month, kickOutTime.day)
                dayLabels.append({'week': week,
                 'date': date,
                 'state': self.getTimeState(startTime, endTime)})

        teams = []
        finalResult = self.finalDuelResults.get(self.selFinalLvKey)
        duelNeedWinCnt = DCD.data.get('ARENA_PLAYOFFS_FINAL_DUEL_NEED_WIN_CNT', 2)
        if p.isPlayoffs5V5():
            duelNeedWinCnt = DCD.data.get('ARENA_PLAYOFFS_5V5_FINAL_DUEL_NEED_WIN_CNT', 1)
        if finalResult:
            data = finalResult.get('data', {})
            for idx in sorted(data.keys()):
                teamsPerDay = []
                for team1, team2 in data[idx]:
                    duelDone = team1.get('winCnt', 0) >= duelNeedWinCnt or team2.get('winCnt', 0) >= duelNeedWinCnt
                    if team1:
                        teamsPerDay.append({'teamName': team1.get('teamName'),
                         'win': team1.get('winCnt', 0) >= duelNeedWinCnt,
                         'duelDone': duelDone,
                         'winCnt': team1.get('winCnt', 0),
                         'nuid': str(team1.get('nuid', 0)),
                         'hostId': team1.get('hostId', 0),
                         'canView': utils.canInLiveOfArenaPlayoffs(BigWorld.player())})
                    if team2:
                        teamsPerDay.append({'teamName': team2.get('teamName'),
                         'win': team2.get('winCnt', 0) >= duelNeedWinCnt,
                         'duelDone': duelDone,
                         'winCnt': team2.get('winCnt', 0),
                         'nuid': str(team2.get('nuid', 0)),
                         'hostId': team2.get('hostId', 0)})

                teams.append(teamsPerDay)

            finalRoundNum = utils.getCrossArenaPlayoffsFinalRoundNum(self.selFinalLvKey)
            if len(data) >= finalRoundNum and len(data[finalRoundNum]) > 0:
                if len(data[finalRoundNum][0]) == 2:
                    team1, team2 = data[finalRoundNum][0]
                    winTeam = None
                    if team1.get('winCnt', 0) >= duelNeedWinCnt:
                        winTeam = team1
                    if team2.get('winCnt', 0) >= duelNeedWinCnt:
                        winTeam = team2
                    if winTeam:
                        teams.append([{'teamName': winTeam.get('teamName'),
                          'win': True,
                          'duelDone': True,
                          'winCnt': winTeam.get('winCnt', 0),
                          'nuid': str(winTeam.get('nuid', 0)),
                          'hostId': winTeam.get('hostId', 0)}])
        return {'teams': teams,
         'dayLabels': dayLabels}

    def getSelTeamInfo(self, lvKey = '', idx = -1):
        if lvKey == '':
            lvKey = self.selGroupLvKey
        if idx == -1:
            idx = self.selGroupIdx
        teams = self.groupTeamInfos.get(lvKey)
        if teams and len(teams) > idx:
            return teams[idx]
        return {}

    def getGroupDuleResult(self, lvKey = '', idx = -1):
        if lvKey == '':
            lvKey = self.selGroupLvKey
        if idx == -1:
            idx = self.selGroupIdx
        results = self.groupDuleResults.get(lvKey)
        if results and len(results) > idx:
            return results[idx]
        return {}

    def fetchTeamInfo(self, lvKey, idx):
        teamInfo = self.getSelTeamInfo(lvKey, idx)
        BigWorld.player().cell.queryArenaPlayoffsGroupTeamResult(teamInfo.get('version', 0), idx, lvKey)

    def fetchGroupDuleResult(self, lvKey, idx):
        result = self.getGroupDuleResult(lvKey, idx)
        BigWorld.player().cell.queryArenaPlayoffsGroupDuelResult(result.get('version', 0), idx, lvKey)

    def fetchFinalResult(self, lvKey):
        result = self.finalDuelResults.get(lvKey, {})
        BigWorld.player().cell.queryArenaPlayoffsFinalDuelResult(result.get('version', 0), lvKey)

    def getTeamInfoByNUID(self, nuid, lvKey, idx):
        val = {'teamName': gameStrings.TEXT_ARENAPLAYOFFSPROXY_565,
         'nuid': '0'}
        if not nuid:
            return copy.deepcopy(val)
        teamInfos = self.getSelTeamInfo(lvKey, idx)
        if teamInfos:
            val = teamInfos.get('data', {}).get(nuid, {})
            val['nuid'] = str(nuid)
        return copy.deepcopy(val)

    def getTimeState(self, startTime, endTime, startOffset = 0):
        sTime = utils.getTimeSecondFromStr(startTime) - startOffset
        eTime = utils.getTimeSecondFromStr(endTime)
        if eTime < utils.getNow():
            return uiConst.ARENA_PLAYOFFS_END_STATE
        if utils.getNow() < sTime:
            return uiConst.ARENA_PLAYOFFS_PRE_STATE
        return uiConst.ARENA_PLAYOFFS_PLAYING_STATE

    def onClickPlayoffsPush(self, msgType):
        self.uiAdapter.pushMessage.removePushMsg(msgType)
        p = BigWorld.player()
        if msgType in (uiConst.MESSAGE_TYPE_AREANA_PLAYOFFS_GROUP_DUEL_START,
         uiConst.MESSAGE_TYPE_AREANA_PLAYOFFS_FINAL_DUEL_START,
         uiConst.MESSAGE_TYPE_AREANA_SCORE_PLAYOFFS_GROUP_DUEL_START,
         uiConst.MESSAGE_TYPE_AREANA_SCORE_PLAYOFFS_FINAL_DUEL_START):
            if p.isBalancePlayoffs():
                self.uiAdapter.pvPPanel.pvpPanelShow(uiConst.PVP_BG_V2_TAB_BALANCE_PLAYOFFS)
            elif p.isPlayoffs5V5():
                self.uiAdapter.pvPPanel.pvpPanelShow(uiConst.PVP_BG_V2_TAB_5V5_PLAYOFFS)
            else:
                self.uiAdapter.pvPPanel.show(uiConst.PVP_BG_V2_TAB_PLAYOFFS)
        elif msgType in (uiConst.MESSAGE_TYPE_AREANA_PLAYOFFS_GROUP_DUEL_END,
         uiConst.MESSAGE_TYPE_AREANA_PLAYOFFS_FINAL_DUEL_END,
         uiConst.MESSAGE_TYPE_AREANA_SCORE_PLAYOFFS_GROUP_DUEL_END,
         uiConst.MESSAGE_TYPE_AREANA_SCORE_PLAYOFFS_FINAL_DUEL_END):
            self.showPlayoffsReport()

    def isNeedPushGroupEndMsg(self):
        schedule = self.getCurPlayoffsSchedule()
        kickOutStartTime = schedule['kickOutStartTime']
        kickOutStartCrontab = '0 0 %d %d *' % (kickOutStartTime.day, kickOutStartTime.month)
        return utils.inCrontabRange(schedule['groupStartCrontab'], kickOutStartCrontab)

    def getCurrentPlayoffsState(self):
        p = BigWorld.player()
        if p.isBalancePlayoffs():
            val = gameglobal.rds.ui.balanceArenaPlayoffs.getCurPlayoffsSchedule()
            return val.get('type', 0)
        elif p.isPlayoffs5V5():
            val = gameglobal.rds.ui.pvpPlayoffs5V5.getCurPlayoffsSchedule()
            return val.get('type', 0)
        else:
            val = gameglobal.rds.ui.pvpPlayoffsV2.getCurPlayoffsSchedule()
            return val.get('type', 0)

    def getCurPlayoffsSchedule(self):
        p = BigWorld.player()
        if p.isBalancePlayoffs():
            return gameglobal.rds.ui.balanceArenaPlayoffs.getArenaPlayOffSchedule()
        elif p.isPlayoffs5V5():
            return gameglobal.rds.ui.pvpPlayoffs5V5.getArenaPlayOffSchedule()
        else:
            return gameglobal.rds.ui.pvpPlayoffsV2.getArenaPlayOffSchedule()

    def getPlayerLvKeyIdx(self):
        p = BigWorld.player()
        if p.isBalancePlayoffs():
            return const.ALL_ARENA_PLAYOFFS_TEAM_LV_KEYS.index(const.ARENA_PLAYOFFS_TEIM_KEY_BALANCE)
        if p.isPlayoffs5V5():
            lvKey = utils.lv2ArenaPlayoffs5v5Teamkey(BigWorld.player().lv)
        else:
            lvKey = utils.lv2ArenaPlayoffsTeamkey(BigWorld.player().lv)
        if lvKey in const.ALL_ARENA_PLAYOFFS_TEAM_LV_KEYS:
            lvKeyIdx = const.ALL_ARENA_PLAYOFFS_TEAM_LV_KEYS.index(lvKey)
        else:
            lvKeyIdx = 0
        return lvKeyIdx

    def refreshTeamDetail(self):
        if self.teamDetailMed:
            self.teamDetailMed.Invoke('refreshView', uiUtils.dict2GfxDict(self.getGfxTeamDetail(), True))

    def getCurSelLvKey(self):
        if self.finalMed or gameglobal.rds.ui.arenaPlayoffs5v5Final.widget:
            return self.selFinalLvKey
        if self.groupMatchMed:
            return self.selGroupLvKey
        return const.ARENA_PLAYOFFS_TEIM_KEY_1_59

    def getGfxTeamDetail(self):
        ret = {}
        if self.selectTeamInfo:
            detail = self.teamDetails.get(self.selectTeamInfo[0], {})
            ret['teamName'] = detail.get('teamName', '')
            ret['serverName'] = utils.getServerName(detail.get('hostId', 0))
            ret['score'] = self.selectTeamInfo[2]
            ret['rank'] = int(self.selectTeamInfo[3])
            members = []
            for gbId, val in detail.get('members', {}).iteritems():
                members.append({'gbId': str(gbId),
                 'hostId': self.selectTeamInfo[1],
                 'roleName': val.get('roleName', ''),
                 'isHeader': val.get('isHeader', False),
                 'schoolFrame': uiConst.SCHOOL_FRAME_DESC.get(val.get('school', 0))})

            ret['members'] = members
        return ret

    def onEnterArenaWithLive(self, *args):
        nuid = int(args[3][0].GetString())
        isGroupDuel = args[3][1].GetBool()
        gamelog.debug('dxk @onEnterArenaWithLive', nuid, isGroupDuel)
        selLvKey = self.selFinalLvKey
        if isGroupDuel:
            selLvKey = self.selGroupLvKey
        BigWorld.player().cell.enterPlayoffsArenaWithLive(selLvKey, nuid, isGroupDuel)

    def enterArena5v5WithLive(self, nuid, isGroupDuel):
        gamelog.debug('dxk @onEnterArenaWithLive', nuid, isGroupDuel)
        selLvKey = self.selFinalLvKey
        if isGroupDuel:
            selLvKey = self.selGroupLvKey
        BigWorld.player().cell.enterPlayoffsArenaWithLive(selLvKey, nuid, isGroupDuel)
