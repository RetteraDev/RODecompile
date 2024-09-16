#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impArenaScore.o
from gamestrings import gameStrings
import cPickle
import zlib
import gameglobal
import gametypes
import gamelog
import utils
import const
import formula
from guis import events
from guis import generalPushMappings
from guis import ui
from guis import uiConst
from guis import uiUtils
from callbackHelper import Functor
from cdata import game_msg_def_data as GMDD

class ImpArenaScore(object):

    def getArenaScorePlayoffsState(self, data):
        gamelog.debug('@dxk playoffs#getArenaScorePlayoffsState:', data)
        self.arenaScoreStateData = data

    def arenaScoreTeamQuery(self, teamInfo, memberInfo):
        gamelog.debug('@dxk playoffs#arenaScoreTeamQuery:', self.roleName, teamInfo, memberInfo)
        self.arenaScorePlayoffsTeam = teamInfo if teamInfo else {}
        self.arenaScorePlayoffsMember = memberInfo if memberInfo else {}
        self.maualSetArenaScorePlayoffsInfo(self.arenaScorePlayoffsTeam)
        gameglobal.rds.ui.arenaPlayoffs.onArenaPlayoffsTeamInfoChanged()

    def getArenaPlayoffsTeam(self):
        if self.isBalancePlayoffs() and self.isBeforeArenaScoreState64():
            return self.arenaScorePlayoffsTeam
        else:
            return self.arenaPlayoffsTeam

    def getArenaPlayoffsMember(self):
        if self.isBalancePlayoffs() and self.isBeforeArenaScoreState64():
            return self.arenaScorePlayoffsMember
        else:
            return self.arenaPlayoffsMember

    def getArenaPlayoffsTeamNUID(self):
        if self.isBalancePlayoffs() and self.isBeforeArenaScoreState64():
            return self.arenaScorePlayoffsTeamNUID
        else:
            return self.arenaPlayoffsTeamNUID

    def getArenaPlayoffsTeamHeader(self):
        if self.isBalancePlayoffs() and self.isBeforeArenaScoreState64():
            return self.arenaScorePlayoffsTeamHeader
        else:
            return self.arenaPlayoffsTeamHeader

    def maualSetArenaScorePlayoffsInfo(self, teamInfo):
        self.arenaScorePlayoffsTeamNUID = teamInfo.get('nuid', 0)
        self.arenaScorePlayoffsTeamHeader = teamInfo.get('rHeader', 0)
        gamelog.debug('dxk @impArenaScore maualSetArenaScorePlayoffsInfo', self.arenaScorePlayoffsTeamNUID, self.arenaScorePlayoffsTeamHeader)

    def syncArenaScoreMemberInfo(self, mType, mGbId, info):
        gamelog.debug('@dxk playoffs#syncArenaScoreMemberInfo:', self.roleName, mGbId, mType, info)
        if mType in (gametypes.DUEL_MEM_PUSH, gametypes.DUEL_MEM_UPDATE):
            self.arenaScorePlayoffsMember[mGbId] = info
        elif mType == gametypes.DUEL_MEM_POP:
            self.arenaScorePlayoffsMember.pop(mGbId, None)
        gameglobal.rds.ui.arenaPlayoffs.onArenaPlayoffsTeamInfoChanged()

    def syncArenaScoreTeamInfo(self, teamInfo):
        gamelog.debug('@dxk playoffs#syncArenaScoreTeamInfo:', teamInfo)
        self.arenaScorePlayoffsTeam = teamInfo if teamInfo else {}
        self.maualSetArenaScorePlayoffsInfo(self.arenaScorePlayoffsTeam)
        gameglobal.rds.ui.arenaPlayoffs.onArenaPlayoffsTeamInfoChanged()

    def onInviteByArenaScoreTeam(self, teamType, nuid, srcGbId, srcName, srcLv, srcSchool):
        gamelog.debug('@dxk arenaScore#onInviteByArenaScoreTeam:', teamType, nuid, srcGbId, srcName, srcLv, srcSchool)
        msg = uiUtils.getTextFromGMD(GMDD.data.INVITE_ARENA_PLAYOFFS_MEMEBER_MSG, '%s') % srcName
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.acceptArenaScoreInvite, teamType, nuid, srcGbId), noCallback=Functor(self.cell.rejectArenaScoreTeamInvite, teamType, nuid, srcGbId), noBtnText=gameStrings.TEXT_IMPFRIEND_963)

    def acceptArenaScoreInvite(self, teamType, nuid, srcGbId):
        gamelog.debug('@dxk arenaScore#acceptArenaScoreInvite:', teamType, nuid, srcGbId)
        self.cell.acceptArenaScoreTeamInvite(teamType, nuid, srcGbId)

    def onAskArenaScoreTeamForPrepare(self):
        gamelog.debug('@dxk playoffs#onAskArenaScoreTeamForPrepare:')
        msg = uiUtils.getTextFromGMD(GMDD.data.APPLY_ARENA_PLAYOFFS_TEAM_MSG, '%s')
        gameglobal.rds.ui.doubleCheckWithInput.show(msg, 'YES', confirmCallback=self.answerArenaScoreTeamPrepare)

    @ui.checkInventoryLock()
    def answerArenaScoreTeamPrepare(self):
        self.cell.answerArenaScoreTeamPrepare(const.ARENA_SCORE_TYPE_1)

    def notifyArenaScoreTeamMemberLogon(self, extra):
        if extra['needRename']:
            pass

    def onArenaScoreStateChanged(self, teamType, state):
        gamelog.debug('@dxk #onArenaScoreStateChanged:', state)
        self.arenaScoreState = state
        if state in [const.ARENA_SCORE_STATE_READY]:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_ARENA_SCORE_APPLY_START, ())
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_ARENA_SCORE_APPLY_START, {'click': self.onClickArenaScorePush})
        if state in [const.ARENA_SCORE_STATE_START]:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_ARENA_SCORE_START, ())
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_ARENA_SCORE_START, {'click': self.onClickArenaScorePush})
        gameglobal.rds.ui.balanceArenaPlayoffs.refreshPlayoffsPanel()
        gameglobal.rds.ui.dispatchEvent(events.EVENT_GENERAL_PUSH_STATECHANGE, (generalPushMappings.GENERAL_PUSH_BALANCE_PLAYOFFS, state))

    def onClickArenaScorePush(self):
        gameglobal.rds.ui.pvPPanel.pvpPanelShow(uiConst.PVP_BG_V2_TAB_BALANCE_PLAYOFFS)
        if uiConst.MESSAGE_TYPE_ARENA_SCORE_START in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_ARENA_SCORE_START)
        if uiConst.MESSAGE_TYPE_ARENA_SCORE_APPLY_START in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_ARENA_SCORE_APPLY_START)

    def canArenaScoreTeleport(self):
        if not self.isArenaScoreTeamCreated():
            return False
        if gametypes.CROSS_ARENA_PLAYOFFS_STATE_START_VOTE <= self.getArenaScoreState() < gametypes.CROSS_ARENA_PLAYOFFS_STATE_END_VOTE:
            return True
        if self.arenaPlayoffsTeamNUID:
            return True
        return False

    def canArenaScoreBet(self):
        return gametypes.CROSS_ARENA_PLAYOFFS_STATE_APPLY_END <= self.getArenaScoreState() <= gametypes.CROSS_ARENA_PLAYOFFS_STATE_FINISHED

    def isInArenaScoreStateJiFen(self):
        return gametypes.CROSS_ARENA_PLAYOFFS_STATE_START_VOTE <= self.getArenaScoreState() <= gametypes.CROSS_ARENA_PLAYOFFS_STATE_END_VOTE or gametypes.CROSS_ARENA_PLAYOFFS_STATE_APPLY <= self.getArenaScoreState() <= gametypes.CROSS_ARENA_PLAYOFFS_STATE_APPLY_END

    def isInArenaScoreStateApply(self):
        return self.getArenaScoreState() in (gametypes.CROSS_ARENA_PLAYOFFS_STATE_START_BUILD, gametypes.CROSS_ARENA_PLAYOFFS_STATE_END_BUILD)

    def isBeforeArenaScoreState64(self):
        return self.getArenaScoreState() in gametypes.ARENA_PLAYOFFS_SCORE_STATES

    def isInArenaScoreStateWuDao(self):
        return self.getArenaScoreState() in gametypes.ARENA_PLAYOFFS_WUDAO_STATES

    def isInArenaScoreStateNotJiFen(self):
        if self.isInArenaScoreStateWuDao():
            return True
        if self.getArenaScoreState() == gametypes.CROSS_ARENA_PLAYOFFS_STATE_APPLY_END:
            return True

    def isInArenaScoreStateGroup(self):
        return gametypes.CROSS_ARENA_PLAYOFFS_STATE_GROUP_MATCH_READY <= self.getArenaScoreState() <= gametypes.CROSS_ARENA_PLAYOFFS_STATE_GROUP_MATCH_FINISHED

    def isInArenaScoreStateFinal(self):
        return gametypes.CROSS_ARENA_PLAYOFFS_STATE_FINAL_MATCH_READY <= self.getArenaScoreState() <= gametypes.CROSS_ARENA_PLAYOFFS_STATE_FINISHED

    def canArenaScoreCreateTeam(self):
        return gametypes.CROSS_ARENA_PLAYOFFS_STATE_START_BUILD <= self.getArenaScoreState() < gametypes.CROSS_ARENA_PLAYOFFS_STATE_END_BUILD

    def isArenaScoreTeamCreated(self):
        return self.getArenaPlayoffsTeam().get('isDone', False)

    def getArenaScoreUIState(self, isDone = True):
        if not self.isBalancePlayoffs():
            return uiConst.ARENA_PLAYOFFS_STATE_NOT_OPEN
        if self.isInArenaScoreStateWuDao() and not self.arenaPlayoffsTeamNUID:
            return uiConst.ARENA_PLAYOFFS_STATE_NO_REQUIEMENT
        if isDone and self.getArenaPlayoffsTeam().get('isDone', False):
            return uiConst.ARENA_PLAYOFFS_STATE_NORMAL
        if self.getArenaPlayoffsTeamNUID():
            if self.getArenaPlayoffsTeamHeader() == self.gbId:
                return uiConst.ARENA_PLAYOFFS_STATE_LEADER
            else:
                return uiConst.ARENA_PLAYOFFS_STATE_TEAMER
        return uiConst.ARENA_PLAYOFFS_STATE_NO_TEAM

    def onQueryArenaScoreTeamDetail(self, lvKey, nuid, teamInfo, info):
        gamelog.debug('@dxk playoffs#onQueryArenaScoreTeamDetail:', lvKey, nuid, cPickle.loads(zlib.decompress(info)))
        info = cPickle.loads(zlib.decompress(info))
        gameglobal.rds.ui.arenaPlayoffs.onQueryArenaPlayoffsTeamDetail(nuid, teamInfo, info)

    def getArenaScoreCurrentSeason(self):
        return formula.getPlayoffsSeason()

    def isArenaScoreLvKey(self, lvKey):
        return lvKey in (gametypes.CROSS_ARENA_PLAYOFFS_LV_KEY_BALANCE,)

    def isBalancePlayoffs(self):
        return gameglobal.rds.configData.get('enableArenaScore', False)
