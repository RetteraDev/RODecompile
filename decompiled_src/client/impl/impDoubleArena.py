#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impDoubleArena.o
from gamestrings import gameStrings
import BigWorld
import gamelog
import gametypes
import utils
import gameglobal
import const
from guis import events
from guis import generalPushMappings
from guis import uiUtils
from guis import uiConst
from guis import menuManager
from callbackHelper import Functor
from guis import messageBoxProxy
from data import duel_config_data as DCD
from gamestrings import gameStrings
from cdata import game_msg_def_data as GMDD
from doubleArenaTeamVal import DoubleArenaTeamVal, DoubleArenaStatisticsVal, DoubleArenaPlayerVal, DoubleArenaApplyingVal

class ImpDoubleArena(object):

    def dArenaOnSyncTimeInfo(self, state, stateEndTimeStamp):
        gamelog.debug('dxk@doubleArena dArenaOnSyncTimeInfo', state, stateEndTimeStamp)
        self.doubleArenaState = state
        self.pushDoubleArenaMsg(state)
        self.doubleArenaStateEndTimeStamp = stateEndTimeStamp
        dArenaDuration = DCD.data.get('dArenaDuration', {1: 3600,
         2: 3600,
         3: 3600,
         4: 3600})
        if not hasattr(self, 'stateStartTimes') or state == gametypes.DOUBLE_ARENA_STATE_CLOSE:
            defaultBeginTimeCrontab = DCD.data.get('dArenaBeginTime', '0 8 11 11 *')
            defaultBeginTime = utils.getNextCrontabTime(defaultBeginTimeCrontab)
            self.stateStartTimes = []
            curr = defaultBeginTime
            for i in xrange(len(dArenaDuration)):
                self.stateStartTimes.append(curr)
                curr += dArenaDuration.get(i + 1, 0)

        if state != gametypes.DOUBLE_ARENA_STATE_CLOSE:
            curr = stateEndTimeStamp - dArenaDuration.get(state, 0)
            for i in xrange(state - 1, len(dArenaDuration)):
                self.stateStartTimes[i] = curr
                curr += dArenaDuration.get(i + 1, 0)

        gamelog.debug('@dxk_da generate start times:', self.stateStartTimes)
        gameglobal.rds.ui.balanceArena2PersonOverview.refreshInfo()
        gameglobal.rds.ui.dispatchEvent(events.EVENT_GENERAL_PUSH_STATECHANGE, (generalPushMappings.GENERAL_PUSH_DOUBLE_ARENA, state))

    def pushDoubleArenaMsg(self, state):
        self.removeOtherDoubleArenaPush()
        if state == gametypes.DOUBLE_ARENA_STATE_PREPARE:
            if self.lv < 50:
                return
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_DOUBLE_ARENA_PERPARE)
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_DOUBLE_ARENA_PERPARE, {'click': self.onDoubleArenaPushMsgClick})
        elif state == gametypes.DOUBLE_ARENA_STATE_GROUP_GAME:
            if self.lv < 50:
                return
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_DOUBLE_ARENA_START)
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_DOUBLE_ARENA_START, {'click': self.onDoubleArenaPushMsgClick})
        elif state == gametypes.DOUBLE_ARENA_STATE_PLAY_OFF:
            if self.lv < 50:
                return
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_DOUBLE_ARENA_STATE16_START)
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_DOUBLE_ARENA_STATE16_START, {'click': self.onDoubleArenaPushMsgClick})

    def onDoubleArenaPushMsgClick(self):
        self.removeOtherDoubleArenaPush()
        gameglobal.rds.ui.pvPPanel.pvpPanelShow(uiConst.PVP_BG_V2_TAB_BALANCE_ARENA_2PERSON)

    def removeOtherDoubleArenaPush(self):
        if uiConst.MESSAGE_TYPE_DOUBLE_ARENA_PERPARE in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_DOUBLE_ARENA_PERPARE)
        if uiConst.MESSAGE_TYPE_DOUBLE_ARENA_START in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_DOUBLE_ARENA_START)
        if uiConst.MESSAGE_TYPE_DOUBLE_ARENA_STATE16_START in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_DOUBLE_ARENA_STATE16_START)

    def dArenaOnOpenPanel(self, isOK):
        if isOK:
            if hasattr(self, 'doubleArenaTeamInfo') and self.doubleArenaTeamInfo:
                self.showGameMsg(GMDD.data.DOUBLE_ARENA_ALREADY_CREATE_TEAM, ())
                return
            gameglobal.rds.ui.balanceArena2PersonCreateTeam.show(isOK)

    def dArenaOnInviteTeamMate(self, leaderRoleName, teamName, camp):
        MBButton = messageBoxProxy.MBButton
        buttons = [MBButton(gameStrings.CBG_RLUE_AGREE, Functor(self.onInviteAgree, leaderRoleName, teamName, camp)), MBButton(gameStrings.CBG_RLUE_DISAGREE, Functor(self.onInviteDisAgree, teamName))]
        zhenyingInfos = DCD.data.get('doubleArenaZhenYingInfo', {})
        msg = gameStrings.DOUBLEARENA_CREATE_INVITE % (leaderRoleName, zhenyingInfos.get(camp).get('name', ''), teamName)
        gameglobal.rds.ui.messageBox.show(True, gameStrings.TEXT_IMPDOUBLEARENA_94, msg, buttons, repeat=60, repeatText=gameStrings.TEXT_IMPDOUBLEARENA_95, countDownFunctor=Functor(self.onInviteDisAgree, teamName))

    def onInviteAgree(self, leaderRoleName, teamName, camp):
        headerGbId = getattr(self, 'headerGbId', 0)
        gamelog.debug('dxk@impDoubleArena argree invite demand', headerGbId)
        self.cell.dArenaAcceptInvitation(headerGbId, teamName, camp)

    def onInviteDisAgree(self, teamName):
        headerGbId = getattr(self, 'headerGbId', 0)
        gamelog.debug('dxk@impDoubleArena disargree invite demand', headerGbId)
        self.cell.dArenaRejectInvitation(headerGbId, teamName)

    def refreshDoubleArenaTeamInfo(self):
        self.base.dArenaCheckTeamInfo()

    def isInDoubleArenaState16(self):
        return getattr(self, 'doubleArenaState', 0) == gametypes.DOUBLE_ARENA_STATE_PLAY_OFF

    def isInDoubleArenaGroup(self):
        return getattr(self, 'doubleArenaState', 0) == gametypes.DOUBLE_ARENA_STATE_GROUP_GAME

    def isInDoubleArenaStateEnd(self):
        return getattr(self, 'doubleArenaState', 0) == gametypes.DOUBLE_ARENA_STATE_END_GAME

    def dArenaOnApplyTeamSucc(self, teamVal):
        self.doubleArenaTeamInfo = teamVal

    def dArenaSyncGetAvatarInfo(self, gbId, physique, aspect, avatarConfig, signal):
        self.doubleArenaMateInfo = {'gbId': gbId,
         'physique': physique,
         'aspect': aspect,
         'avatarConfig': avatarConfig,
         'signal': signal}

    def dArenaOnDisbandTeamSucc(self):
        self.doubleArenaTeamInfo = {}
        gameglobal.rds.ui.balanceArena2PersonMatch.refreshInfo()

    def dArenaOnSyncTeamInfo(self, teamVal):
        self.doubleArenaTeamInfo = teamVal

    def dArenaOnSyncStatistics(self, statisInfo):
        if getattr(self, 'doubleArenaTeamInfo', {}):
            self.doubleArenaTeamInfo.statistics = statisInfo

    def dArenaOnSyncCampInfo(self, campInfo):
        self.doubleArenaCampInfo = campInfo
        gameglobal.rds.ui.balanceArena2PersonOverview.refreshInfo()

    def doCheer(self, data):
        leaderGbId, timeStamp, roleName = str(data).split(const.SYMBOL_RENAME_SPLIT)
        gamelog.debug('dxk@impDoubleArena do cheer:', leaderGbId, timeStamp, roleName)
        self.base.dArenaHelpCheers(long(leaderGbId), long(timeStamp), roleName)

    def dArenaOnSyncTopSixteen(self, topSixteen):
        gameglobal.rds.ui.balanceArena2PersonInfo.onGetServerData(topSixteen)

    def dArenaOnNotifyPlayOff(self):
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_DOUBLE_ARENA_STATE16_MATCH_START)
        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_DOUBLE_ARENA_STATE16_MATCH_START, {'click': self.dArenaShowConfirmGoSixteen})

    def dArenaShowConfirmGoSixteen(self):
        msg = uiUtils.getTextFromGMD(GMDD.data.DOBLE_ARENA_PLAYOFF_ENTER)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=self.onDoubleArenaConfirmEnterClick, yesBtnText=gameStrings.TEXT_IMPPLAYERTEAM_644, noBtnText=gameStrings.TEXT_AVATAR_2876_1)

    def dArenaConfirmSixteenReadyRoom(self):
        msg = uiUtils.getTextFromGMD(GMDD.data.DOBLE_ARENA_PLAYOFF_NEED_TELEPORT)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.cell.applyEnterDoubleArenaReadyRoom, const.ARENA_MODE_CROSS_MS_ROUND_2V2_DOUBLE_ARENA), yesBtnText=gameStrings.TEXT_IMPPLAYERTEAM_644, noBtnText=gameStrings.TEXT_AVATAR_2876_1)

    def onDoubleArenaConfirmEnterClick(self):
        self.removeArenaSixteenMatchPushMsg()
        self.cell.dArenaApplyEnterSixteenArena()

    def removeArenaSixteenMatchPushMsg(self):
        if uiConst.MESSAGE_TYPE_DOUBLE_ARENA_STATE16_MATCH_START in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_DOUBLE_ARENA_STATE16_MATCH_START)

    def teleportToDoubleArenaReadyRoom(self):
        self.cell.applyEnterDoubleArenaReadyRoom(const.ARENA_MODE_CROSS_MS_ROUND_2V2_DOUBLE_ARENA)

    def dArenaOnQueryFightScore(self, todayScore, totalScore):
        self.doubleArenatodayScore = todayScore
        self.doubleArenatotalScore = totalScore
        gameglobal.rds.ui.balanceArena2PersonReward.refreshInfo()
        gameglobal.rds.ui.balanceArena2PersonMatch.refreshInfo()

    def dArenaOnQuerySpFight(self, spFight):
        gameglobal.rds.ui.balanceArena2PersonZhanBao.onGetServerData(spFight)

    def isDoubleArenaLeader(self):
        if hasattr(self, 'doubleArenaTeamInfo') and self.doubleArenaTeamInfo:
            return self.doubleArenaTeamInfo.playerOne.gbId == self.gbId
        return False

    def inviteDoubleArenaMate(self):
        mateInfo = self.doubleArenaTeamInfo.playerOne
        if self.isDoubleArenaLeader():
            mateInfo = self.doubleArenaTeamInfo.playerTwo
        menuTarget = menuManager.getInstance().menuTarget
        targetRoleName = mateInfo.roleName
        if self._isSoul():
            targetRoleName = '%s-%s' % (mateInfo.roleName, utils.getServerName(utils.getHostId()))
        menuTarget.apply(roleName=targetRoleName)
        if menuTarget.canInviteTeam(self):
            menuManager.getInstance().inviteTeam()

    def dArenaAskForInviteTeamMate(self):
        msg = gameStrings.DOUBLE_ARENA_NO_TEAM_CONFIRM
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=self.inviteDoubleArenaMate, noCallback=self.dArenaShowInviteRefuseInfo, yesBtnText=gameStrings.TEXT_IMPPLAYERTEAM_644, noBtnText=gameStrings.TEXT_AVATAR_2876_1, textAlign='center')

    def dArenaShowInviteRefuseInfo(self):
        self.showGameMsg(GMDD.data.DOUBLE_ARENA_TEAM_MATE_WRONG, ())
