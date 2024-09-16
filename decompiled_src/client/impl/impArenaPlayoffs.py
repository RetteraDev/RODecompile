#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impArenaPlayoffs.o
from gamestrings import gameStrings
import cPickle
import zlib
import gameglobal
import gametypes
import gamelog
import utils
import formula
from guis import ui
from guis import uiConst
from guis import uiUtils
from callbackHelper import Functor
from cdata import game_msg_def_data as GMDD
from gamestrings import gameStrings

class ImpArenaPlayoffs(object):

    def arenaPlayoffsTeamQuery(self, teamInfo, memberInfo):
        gamelog.debug('@hjx playoffs#arenaPlayoffsTeamQuery:', self.roleName, teamInfo, memberInfo)
        self.arenaPlayoffsTeam = teamInfo
        self.arenaPlayoffsMember = memberInfo
        if self.isBalancePlayoffs():
            gameglobal.rds.ui.balanceArenaPlayoffs.refreshPlayoffsPanel()
        elif self.isPlayoffs5V5():
            gameglobal.rds.ui.pvpPlayoffs5V5.refreshPlayoffsPanel()
        else:
            gameglobal.rds.ui.pvpPlayoffsV2.refreshPlayoffsPanel()

    def syncArenaPlayoffsMemberInfo(self, mType, mGbId, info):
        gamelog.debug('@hjx playoffs#syncArenaPlayoffsMemberInfo:', self.roleName, mGbId, mType, info)
        if mType in (gametypes.DUEL_MEM_PUSH, gametypes.DUEL_MEM_UPDATE):
            self.arenaPlayoffsMember[mGbId] = info
        elif mType == gametypes.DUEL_MEM_POP:
            self.arenaPlayoffsMember.pop(mGbId, None)
        if self.isBalancePlayoffs():
            gameglobal.rds.ui.balanceArenaPlayoffs.refreshPlayoffsPanel()
        elif self.isPlayoffs5V5():
            gameglobal.rds.ui.pvpPlayoffs5V5.refreshPlayoffsPanel()
        else:
            gameglobal.rds.ui.pvpPlayoffsV2.refreshPlayoffsPanel()

    def syncArenaPlayoffsTeamInfo(self, teamInfo):
        gamelog.debug('@hjx playoffs#syncArenaPlayoffsTeamInfo:', teamInfo)
        self.arenaPlayoffsTeam = teamInfo
        if self.isBalancePlayoffs():
            gameglobal.rds.ui.balanceArenaPlayoffs.refreshPlayoffsPanel()
        elif self.isPlayoffs5V5():
            gameglobal.rds.ui.pvpPlayoffs5V5.refreshPlayoffsPanel()
        else:
            gameglobal.rds.ui.pvpPlayoffsV2.refreshPlayoffsPanel()

    def onInviteByArenaPlayoffsTeam(self, key, nuid, srcGbId, srcName, srcLv, srcSchool):
        gamelog.debug('@hjx playoffs#onInviteByArenaPlayoffsTeam:', key, nuid, srcGbId, srcName, srcLv, srcSchool)
        msg = uiUtils.getTextFromGMD(GMDD.data.INVITE_ARENA_PLAYOFFS_MEMEBER_MSG, '%s') % srcName
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.cell.acceptArenaPlayoffsTeamInvite, key, nuid, srcGbId, srcName), noCallback=Functor(self.cell.rejectArenaPlayoffsTeamInvite, key, nuid, srcGbId), noBtnText=gameStrings.TEXT_IMPFRIEND_963)

    def onAskArenaPlayoffsTeamForPrepare(self):
        gamelog.debug('@hjx playoffs#onAskArenaPlayoffsTeamForPrepare:')
        msg = uiUtils.getTextFromGMD(GMDD.data.APPLY_ARENA_PLAYOFFS_TEAM_MSG, '%s')
        gameglobal.rds.ui.doubleCheckWithInput.show(msg, 'YES', confirmCallback=self.answerArenaPlayoffsTeamPrepare)

    @ui.checkInventoryLock()
    def answerArenaPlayoffsTeamPrepare(self):
        self.cell.answerArenaPlayoffsTeamPrepare()

    def notifyArenaPlayoffsTeamMemberLogon(self, extra):
        self.notifyArenaPlayoffsTeamState(extra['state'])
        if extra['needRename']:
            pass

    def notifyArenaPlayoffsTeamState(self, state):
        gamelog.debug('@hjx playoffs#notifyArenaPlayoffsTeamState:', state)
        self.arenaPlayoffsTeamState = state
        if self.isBalancePlayoffs():
            gameglobal.rds.ui.balanceArenaPlayoffs.refreshPlayoffsPanel()
            if self.arenaPlayoffsTeamState == gametypes.CROSS_ARENA_PLAYOFFS_TEAM_STATE_GROUP_DUEL:
                gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_AREANA_SCORE_PLAYOFFS_GROUP_DUEL_START)
            elif self.arenaPlayoffsTeamState == gametypes.CROSS_ARENA_PLAYOFFS_TEAM_STATE_GROUP_END:
                if gameglobal.rds.ui.arenaPlayoffs.isNeedPushGroupEndMsg():
                    gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_AREANA_SCORE_PLAYOFFS_GROUP_DUEL_END)
            elif self.arenaPlayoffsTeamState == gametypes.CROSS_ARENA_PLAYOFFS_TEAM_STATE_FINAL_DUEL:
                gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_AREANA_SCORE_PLAYOFFS_FINAL_DUEL_START)
            elif self.arenaPlayoffsTeamState == gametypes.CROSS_ARENA_PLAYOFFS_TEAM_STATE_FINAL_END:
                gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_AREANA_SCORE_PLAYOFFS_FINAL_DUEL_END)
        else:
            if self.isPlayoffs5V5():
                gameglobal.rds.ui.pvpPlayoffs5V5.refreshPlayoffsPanel()
            else:
                gameglobal.rds.ui.pvpPlayoffsV2.refreshPlayoffsPanel()
            if self.arenaPlayoffsTeamState == gametypes.CROSS_ARENA_PLAYOFFS_TEAM_STATE_GROUP_DUEL:
                gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_AREANA_PLAYOFFS_GROUP_DUEL_START)
            elif self.arenaPlayoffsTeamState == gametypes.CROSS_ARENA_PLAYOFFS_TEAM_STATE_GROUP_END:
                if gameglobal.rds.ui.arenaPlayoffs.isNeedPushGroupEndMsg():
                    gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_AREANA_PLAYOFFS_GROUP_DUEL_END)
            elif self.arenaPlayoffsTeamState == gametypes.CROSS_ARENA_PLAYOFFS_TEAM_STATE_FINAL_DUEL:
                gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_AREANA_PLAYOFFS_FINAL_DUEL_START)
            elif self.arenaPlayoffsTeamState == gametypes.CROSS_ARENA_PLAYOFFS_TEAM_STATE_FINAL_END:
                gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_AREANA_PLAYOFFS_FINAL_DUEL_END)

    def onQueryCurArenaPlayoffsSeason(self, lvKey, index):
        """
        \xe5\xbd\x93\xe5\x89\x8dlvKey\xe7\xad\x89\xe7\xba\xa7\xe6\xae\xb5\xe6\x89\x80\xe5\xa4\x84\xe7\x9a\x84\xe8\xb5\x9b\xe5\xad\xa3index(\xe4\xbb\x8e1\xe5\xbc\x80\xe5\xa7\x8b)
        Args:
            lvKey:
            index:
        
        Returns:
        
        """
        gamelog.debug('@hjx playoffs#onQueryCurArenaPlayoffsSeason:', lvKey, index)
        gameglobal.rds.ui.arenaPlayoffs.curArenaPlayoffsSeason[lvKey] = index
        if gameglobal.rds.ui.arenaPlayoffs.finalMed:
            gameglobal.rds.ui.arenaPlayoffs.refreshFinalDuelResultView()
        elif gameglobal.rds.ui.arenaPlayoffs.groupMatchMed:
            gameglobal.rds.ui.arenaPlayoffs.refreshGroupDuleResultView()
        elif gameglobal.rds.ui.arenaPlayoffs.isNeedOpen:
            gameglobal.rds.ui.arenaPlayoffs.showPlayoffsReport()
        if self.isPlayoffs5V5():
            gameglobal.rds.ui.pvpPlayoffs5V5.refreshPlayoffsPanel()
        else:
            gameglobal.rds.ui.pvpPlayoffsV2.refreshPlayoffsPanel()

    def onQueryArenaPlayoffsGroupDuelResult(self, lvKey, groupId, info):
        gamelog.debug('@hjx playoffs#onQueryArenaPlayoffsGroupDuelResult:', cPickle.loads(zlib.decompress(info)))
        info = cPickle.loads(zlib.decompress(info))
        gameglobal.rds.ui.arenaPlayoffs.onGetGroupDuleResult(lvKey, groupId, info)

    def onQueryArenaPlayoffsGroupTeamResult(self, lvKey, groupId, info):
        gamelog.debug('@hjx playoffs#onQueryArenaPlayoffsGroupTeamResult:', cPickle.loads(zlib.decompress(info)))
        info = cPickle.loads(zlib.decompress(info))
        gameglobal.rds.ui.arenaPlayoffs.onGetTeamInfo(lvKey, groupId, info)

    def onQueryArenaPlayoffsFinalDuelResult(self, lvKey, info):
        gamelog.debug('@hjx playoffs#onQueryArenaPlayoffsFinalDuelResult:', cPickle.loads(zlib.decompress(info)))
        info = cPickle.loads(zlib.decompress(info))
        gameglobal.rds.ui.arenaPlayoffs.onGetFinalDuleResult(lvKey, info)
        gameglobal.rds.ui.arenaPlayoffsBet.updateFinalDuelResult(lvKey, info)

    def onQueryArenaPlayoffsTeamDetail(self, lvKey, nuid, teamInfo, info):
        gamelog.debug('@hjx playoffs#onQueryArenaPlayoffsTeamDetail:', lvKey, nuid, cPickle.loads(zlib.decompress(info)))
        info = cPickle.loads(zlib.decompress(info))
        gameglobal.rds.ui.arenaPlayoffs.onQueryArenaPlayoffsTeamDetail(nuid, teamInfo, info)

    def onArenaChallengeStageNotify(self, stage):
        gamelog.debug('@hjx arenaChallenge#onArenaChallengeStart:', stage)

    def notifyEnterArenaChallenge(self):
        gamelog.debug('@hjx arenaChallenge#notifyEnterArenaChallenge')
        gameglobal.rds.ui.arenaChallengeDeclartion.addPushMsg(uiConst.MESSAGE_TYPE_ARENA_CHALLENGE_ENTER)

    def getPlayoffs5V5UIState(self, isDone = True):
        if not self.isPlayoffs5V5():
            return uiConst.ARENA_PLAYOFFS_STATE_NOT_OPEN
        if not utils.checkArenaPlayoffsCandidateValid(self, gametypes.ARENA_PLAYOFFS_TYPE_5V5):
            return uiConst.ARENA_PLAYOFFS_STATE_NO_REQUIEMENT
        if isDone and self.arenaPlayoffsTeam.get('isDone'):
            return uiConst.ARENA_PLAYOFFS_STATE_NORMAL
        if self.arenaPlayoffsTeamNUID:
            if self.arenaPlayoffsTeamHeader == self.gbId:
                return uiConst.ARENA_PLAYOFFS_STATE_LEADER
            else:
                return uiConst.ARENA_PLAYOFFS_STATE_TEAMER
        return uiConst.ARENA_PLAYOFFS_STATE_NO_TEAM

    def getPlayoffsUIState(self, isDone = True):
        if self.isBalancePlayoffs() or self.isPlayoffs5V5():
            return uiConst.ARENA_PLAYOFFS_STATE_NOT_OPEN
        if not utils.checkArenaPlayoffsCandidateValid(self):
            return uiConst.ARENA_PLAYOFFS_STATE_NO_REQUIEMENT
        if isDone and self.arenaPlayoffsTeam.get('isDone'):
            return uiConst.ARENA_PLAYOFFS_STATE_NORMAL
        if self.arenaPlayoffsTeamNUID:
            if self.arenaPlayoffsTeamHeader == self.gbId:
                return uiConst.ARENA_PLAYOFFS_STATE_LEADER
            else:
                return uiConst.ARENA_PLAYOFFS_STATE_TEAMER
        return uiConst.ARENA_PLAYOFFS_STATE_NO_TEAM

    def onRewardArenaPlayoffsBet(self, lvKey, bType, betId, cash):
        gamelog.debug('@hjx bet#onRewardArenaPlayoffsBet:', lvKey, bType, betId, cash)
        gameglobal.rds.ui.arenaPlayoffsBet.notifyBetRewardPushMsg(lvKey, bType, betId)

    def onQueryArenaPlayoffsDuelBetResult(self, lvKey, bType, betId, betDuelInfo, lastSeasonRestCash):
        gamelog.debug('@hjx bet#onQueryArenaPlayoffsDuelBetResult:', lvKey, bType, betId, betDuelInfo, lastSeasonRestCash)
        gameglobal.rds.ui.arenaPlayoffsBet.updateBetResult(lvKey, bType, betId, betDuelInfo, lastSeasonRestCash)

    def onQueryArenaPlayoffsBetCalcInfo(self, version, lastSeasonRestCashInfo, betFailedAccumulateCashInfo, lastDuelRestCashDict):
        gamelog.debug('@hjx bet#onQueryArenaPlayoffsBetCalcInfo:', version, lastSeasonRestCashInfo, betFailedAccumulateCashInfo, lastDuelRestCashDict)
        gameglobal.rds.ui.arenaPlayoffsBet.updateBetFailedCash(version, lastSeasonRestCashInfo, betFailedAccumulateCashInfo, lastDuelRestCashDict)

    def onQueryArenaPlayoffsMyBet(self, version, info):
        gamelog.debug('@hjx bet#onQueryArenaPlayoffsMyBet:', version, cPickle.loads(zlib.decompress(info)))
        info = cPickle.loads(zlib.decompress(info))
        gameglobal.rds.ui.arenaPlayoffsBet.updateMyBet(version, info)

    def onQueryArenaPlayoffsTeamsOfLvKey(self, lvKey, version, info):
        gamelog.debug('@hjx bet#onQueryArenaPlayoffsTeamsOfLvKey:', lvKey, version, cPickle.loads(zlib.decompress(info)))
        info = cPickle.loads(zlib.decompress(info))
        gameglobal.rds.ui.arenaPlayoffsBet.updateTeams(lvKey, version, info)

    def onQueryArenaPlayoffsBetCandidate(self, lvKey, bType, betId, betDuelInfo):
        gamelog.debug('@hjx bet#onQueryArenaPlayoffsBetCandidate:', lvKey, bType, betId, cPickle.loads(zlib.decompress(betDuelInfo)))
        betDuelInfo = cPickle.loads(zlib.decompress(betDuelInfo))
        gameglobal.rds.ui.arenaPlayoffsBet.updateCandidate(lvKey, bType, betId, betDuelInfo)

    def onArenaPlayoffsBetLogon(self, betIdDict):
        gamelog.debug('@hjx bet#onArenaPlayoffsBetLogon:', betIdDict)
        gameglobal.rds.ui.arenaPlayoffsBet.initBetIdDict(betIdDict)

    def onArenaPlayoffsBetIdDictQuery(self, lvKey, info):
        gamelog.debug('@hjx bet#onArenaPlayoffsBetIdDictQuery:', lvKey, info)
        gameglobal.rds.ui.arenaPlayoffsBet.updateBetIdDict(lvKey, info)

    def onQueryArenaPlayoffsDailyBet(self, lvKey, bType, betId, resultList, index):
        gamelog.debug('@hjx bet#onQueryArenaPlayoffsDailyBet:', lvKey, bType, betId, resultList, index)
        gameglobal.rds.ui.arenaPlayoffsBet.updateTipResultDict(lvKey, bType, betId, index, resultList)

    def onQueryArenaPlayoffsFinalBetResult(self, lvKey, bType, betId, resultList, index):
        gamelog.debug('@hjx bet#onQueryArenaPlayoffsFinalBetResult:', lvKey, bType, betId, resultList, index)
        gameglobal.rds.ui.arenaPlayoffsBet.updateTipResultDict(lvKey, bType, betId, index, resultList)

    def notifyArenaChallengeLogon(self, status, srcHostId, srcRoleName, tgtHostId, tgtRoleName, challengeMode, msg):
        gamelog.debug('@hjx arenaChallenge#notifyArenaChallengeLogon:', status)
        declartionDict = {'srcHostId': srcHostId,
         'srcRoleName': srcRoleName,
         'tgtHostId': tgtHostId,
         'tgtRoleName': tgtRoleName,
         'challengeMode': challengeMode,
         'msg': msg}
        if status == gametypes.CROSS_ARENA_CHALLENGE_STATUS_APPLY_SUCC:
            gameglobal.rds.ui.arenaChallengeDeclartion.addPushMsg(uiConst.MESSAGE_TYPE_ARENA_CHALLENGE_ACCEPT, declartionDict)
        elif status == gametypes.CROSS_ARENA_CHALLENGE_STATUS_APPLY_BY:
            gameglobal.rds.ui.arenaChallengeDeclartion.addPushMsg(uiConst.MESSAGE_TYPE_ARENA_CHALLENGE_APPLY, declartionDict)

    def onArenaChallengeInfoQuery(self, qType, version, info):
        gamelog.debug('@hjx arenaChallenge#onArenaChallengeInfoQuery:', qType, version, cPickle.loads(zlib.decompress(info)))
        info = cPickle.loads(zlib.decompress(info))
        gameglobal.rds.ui.arenaChallengeReview.onArenaChallengeInfoQuery(qType, version, info)

    def getArenaPlayoffs5V5State(self):
        if hasattr(self, 'arenaPlayoffsStatesInfo'):
            state69 = self.arenaPlayoffsStatesInfo.get(gametypes.CROSS_ARENA_PLAYOFFS_5V5_LV_KEY_60_69, gametypes.CROSS_ARENA_PLAYOFFS_STATE_DEFAULT)
            state79 = self.arenaPlayoffsStatesInfo.get(gametypes.CROSS_ARENA_PLAYOFFS_5V5_LV_KEY_70_79, gametypes.CROSS_ARENA_PLAYOFFS_STATE_DEFAULT)
            if state79 == gametypes.CROSS_ARENA_PLAYOFFS_STATE_START_VOTE or state69 == gametypes.CROSS_ARENA_PLAYOFFS_STATE_START_VOTE:
                return gametypes.CROSS_ARENA_PLAYOFFS_STATE_START_VOTE
            return max(state69, state79)
        return gametypes.CROSS_ARENA_PLAYOFFS_STATE_DEFAULT

    def getArenaPlayoffs3V3State(self):
        if hasattr(self, 'arenaPlayoffsStatesInfo'):
            state59 = self.arenaPlayoffsStatesInfo.get(gametypes.CROSS_ARENA_PLAYOFFS_LV_KEY_1_59, gametypes.CROSS_ARENA_PLAYOFFS_STATE_DEFAULT)
            state69 = self.arenaPlayoffsStatesInfo.get(gametypes.CROSS_ARENA_PLAYOFFS_LV_KEY_60_69, gametypes.CROSS_ARENA_PLAYOFFS_STATE_DEFAULT)
            state79 = self.arenaPlayoffsStatesInfo.get(gametypes.CROSS_ARENA_PLAYOFFS_LV_KEY_70_79, gametypes.CROSS_ARENA_PLAYOFFS_STATE_DEFAULT)
            return max(state59, state69, state79)
        return gametypes.CROSS_ARENA_PLAYOFFS_STATE_DEFAULT

    def getArenaScoreState(self):
        if hasattr(self, 'arenaPlayoffsStatesInfo'):
            return self.arenaPlayoffsStatesInfo.get(gametypes.CROSS_ARENA_PLAYOFFS_LV_KEY_BALANCE, gametypes.CROSS_ARENA_PLAYOFFS_STATE_DEFAULT)
        return gametypes.CROSS_ARENA_PLAYOFFS_STATE_DEFAULT

    def isPlayoffs5V5(self):
        return gameglobal.rds.configData.get('enablePlayoffs5V5', False)

    def onArenaPlayoffsScheduleUpdated(self, lvKey, state):
        gamelog.debug('xjw##### onArenaPlayoffsScheduleUpdated', lvKey, state)
        if not hasattr(self, 'arenaPlayoffsStatesInfo'):
            self.arenaPlayoffsStatesInfo = {}
        self.arenaPlayoffsStatesInfo[lvKey] = state
        if formula.getPlayoffsTypeByLvKey(lvKey) == gametypes.ARENA_PLAYOFFS_TYPE_5V5:
            gameglobal.rds.ui.pvpPlayoffs5V5.refreshPlayoffsPanel()
            gameglobal.rds.ui.pvpPlayoffs5V5.addPlayoffsPushMsg(lvKey, state)
        elif formula.getPlayoffsTypeByLvKey(lvKey) == gametypes.ARENA_PLAYOFFS_TYPE_BALANCE:
            gameglobal.rds.ui.balanceArenaPlayoffs.refreshPlayoffsPanel()
        elif formula.getPlayoffsTypeByLvKey(lvKey) == gametypes.ARENA_PLAYOFFS_TYPE_3V3:
            gameglobal.rds.ui.pvpPlayoffsV2.refreshPlayoffsPanel()

    def onUpdateArenaPlayoffsAidState(self, lvKey, state):
        if not hasattr(self, 'arenaPlayoffsAidState'):
            self.arenaPlayoffsAidState = {}
        self.arenaPlayoffsAidState[lvKey] = state

    def getPlayoffsState(self):
        if self.isPlayoffs5V5():
            return self.getArenaPlayoffs5V5State()
        elif self.isBalancePlayoffs():
            return self.getArenaScoreState()
        else:
            return self.getArenaPlayoffs3V3State()

    def isPlayoffAidStateValid(self):
        stateCheck = False
        if self.isBalancePlayoffs():
            lvKey = gametypes.CROSS_ARENA_PLAYOFFS_LV_KEY_BALANCE
            stateCheck = self.getPlayoffAidState(lvKey) == gametypes.CROSS_ARENA_PLAYOFFS_AID_STATE_START
        else:
            lvKeys = (gametypes.CROSS_ARENA_PLAYOFFS_5V5_LV_KEY_60_69, gametypes.CROSS_ARENA_PLAYOFFS_5V5_LV_KEY_70_79)
            for lvKey in lvKeys:
                stateCheck = stateCheck or self.getPlayoffAidState(lvKey) == gametypes.CROSS_ARENA_PLAYOFFS_AID_STATE_START

        return stateCheck

    def getPlayoffAidState(self, lvKey):
        return getattr(self, 'arenaPlayoffsAidState', {}).get(lvKey, 0)

    def doPlayoffsCheer(self, data):
        lvKey, teamId = data.split(',')
        gamelog.debug('dxk@impArenaPlayoffs doPlayoffsCheer lvKey,teamId:', lvKey, teamId)
        self.cell.voteArenaPlayoffsTeam(lvKey, long(teamId), 0, 1)

    def onAddPlayoffsLuckyBag(self, bagId, num):
        gamelog.debug('dxk@onAddPlayoffsLuckyBag:', bagId, num)
        self.showGameMsg(GMDD.data.ADD_LUCKY_BAG_SUCCESS, ())
        gameglobal.rds.ui.pvpPlayoffs5v5Fudai.onSetFudaiSucess()

    def onVoteItemClick(self):
        if self.isPlayoffs5V5():
            gameglobal.rds.ui.pvpPlayoffs5V5.onVoteItemClick()
        else:
            gameglobal.rds.ui.arenaPlayoffsSupport.show()

    def onArenaPlayoffsAidSucc(self, aidNum, teamName):
        self.showGameMsg(GMDD.data.COMMON_MSG, (gameStrings.ARENA_PLAYOFFS_SUPPORT_VOTE_SUCESS,))
        gameglobal.rds.ui.arenaPlayoffsSupport.onArenaPlayoffsAidSucc(aidNum, teamName)
