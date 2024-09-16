#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impArena.o
from gamestrings import gameStrings
import BigWorld
import utils
import const
import gameconfigCommon
import gameglobal
import gametypes
import formula
import commcalc
import gamelog
import zlib
import cPickle
from guis import events
from guis import ui
from guis import uiConst
from guis import uiUtils
from guis import messageBoxProxy
from callbackHelper import Functor
from data import arena_mode_data as AMD
from cdata import game_msg_def_data as GMDD
from data import arena_data as AD
from data import cross_clan_war_config_data as CWCCD
ARENA_START = 1
ARENA_QUIT = 2
SHOW_COUNT = [30,
 20,
 15,
 10,
 5,
 4,
 3,
 2,
 1]
SHOW_COUNT.extend([ i * 60 for i in xrange(1, 31) ])
COUNT_DWON_NUM = (5, 4, 3, 2, 1)
ARENA_STAGE = {ARENA_START: (GMDD.data.DUEL_START_COUNT, 'readyTime'),
 ARENA_QUIT: (GMDD.data.DUEL_QUIT_COUNT, 'quitTime')}
ANIMATION_SHOW_COUNT = [15, 10]
START_COUNT = 1
END_COUNT = 2

class ImpArena(object):

    def outArena(self):
        gameglobal.rds.ui.chat.goToWorld()

    @ui.callAfterTime(2)
    def refreshArenaInfo(self):
        if not self.inFubenTypes(const.FB_TYPE_ARENA):
            return
        gameglobal.rds.ui.arena.refreshArenaTmpResult()
        gameglobal.rds.ui.teamComm.refreshMemberInfo(False)
        gameglobal.rds.ui.teamEnemyArena.refreshMemberInfo(False)

    def refreshArenaStats(self, roundCount):
        if hasattr(self, 'roundCount') and self.roundCount == roundCount:
            return
        self.roundCount = roundCount
        gameglobal.rds.ui.arena.showArenaStats()

    def arenaQuery(self, arenaStatistics, arenaInfo, mGbId, tReady, troopLogonName, roundWinRec, fbNo, roundCount, arenaPlayoffsCurRoundNum, sideNUID):
        gamelog.debug('hjx debug arena arenaQuery:', troopLogonName, arenaStatistics, arenaInfo, mGbId, tReady, fbNo)
        self.mGbId = mGbId
        self.sideNUID = sideNUID
        self.arenaTeam = arenaInfo
        self.arenaStatistics = arenaStatistics
        self.arenaReadyTime = tReady
        self.setArenaNo(fbNo)
        self.setArenaMode(formula.fbNo2ArenaMode(fbNo))
        self.roundWinRec = roundWinRec
        self.arenaPlayoffsCurRoundNum = arenaPlayoffsCurRoundNum
        self.refreshArenaStats(roundCount)
        self.isTroopLogon = troopLogonName == self.roleName
        self._setMemberPos()
        self._refreshMemberBuffState()
        self.refreshArenaInfo()
        gameglobal.rds.ui.teamComm.refreshMemberInfo(False)
        if not formula.spaceInWingWorldXinMoArena(BigWorld.player().spaceNo) and not gameglobal.rds.ui.arena.arenaStatsMed:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ARENA_STATS)
        if self.inClanChallenge() and utils.getNow() >= tReady:
            gameglobal.rds.ui.arena.startArenaTimer(self.getArenaMode())

    def get_isTroopLogon(self):
        if not hasattr(self, 'isTroopLogon'):
            return False
        return self.isTroopLogon

    def refreshArenaCampInfo(self):
        if not self.inFubenTypes(const.FB_TYPE_ARENA):
            return
        if hasattr(self, 'refreshTimer') and self.refreshTimer != 0:
            BigWorld.cancelCallback(self.refreshTimer)
            self.refreshTimer = 0
        members = gameglobal.rds.ui.teamComm.memberId + gameglobal.rds.ui.teamEnemyArena.memberId
        others = [ (mGbId, mVal['id']) for mGbId, mVal in self.arenaTeam.iteritems() if mVal['id'] in members ]
        self.getOthersInfo(others)
        self.refreshTimer = BigWorld.callback(utils.getRefreshAvatarInfoInterval(self), self.refreshArenaCampInfo)

    def onReceiveArenaCampInfo(self, gbId, info):
        if not self.arenaTeam.has_key(gbId):
            return
        memberId = self.arenaTeam[gbId]['id']
        hp, mhp, mp, mmp, lv = info
        for idx, mid in enumerate(gameglobal.rds.ui.teamComm.memberId):
            if mid == memberId:
                gameglobal.rds.ui.teamComm.setOldVal(idx, hp, mhp, mp, mmp, lv)
                return

        for idx, mid in enumerate(gameglobal.rds.ui.teamEnemyArena.memberId):
            if mid == memberId:
                gameglobal.rds.ui.teamEnemyArena.setOldVal(idx, hp, mhp, mp, mmp, lv)
                return

    def getSumAliveMan(self, side):
        if hasattr(self, 'arenaTeam') and hasattr(self, 'mGbId'):
            return self.arenaTeam[self.mGbId]['sideInMan'][side]
        else:
            return 0

    def getSumMan(self, side):
        if hasattr(self, 'arenaTeam') and hasattr(self, 'mGbId'):
            return self.arenaTeam[self.mGbId]['sideAllMan'][side]
        else:
            return 0

    def getSumKilled(self):
        if hasattr(self, 'arenaTeam') and hasattr(self, 'mGbId'):
            return self.arenaTeam[self.mGbId]['sideKillNum']
        else:
            return 0

    def getSumBeKilled(self):
        if hasattr(self, 'arenaTeam') and hasattr(self, 'mGbId'):
            return self.arenaTeam[self.mGbId]['sideBeKillNum']
        else:
            return 0

    def getMyWinNum(self):
        gamelog.debug('hjx debug arena getMyWinNum:', self.roundWinRec)
        if hasattr(self, 'roundWinRec') and hasattr(self, 'sideNUID'):
            return self.roundWinRec.get(self.sideNUID, 0)
        else:
            return 0

    def getEnemyWinNum(self):
        gamelog.debug('hjx debug arena getEnemyWinNum0---:', self.roundWinRec)
        if hasattr(self, 'roundWinRec') and hasattr(self, 'sideNUID'):
            nuids = self.roundWinRec.keys()
            if self.sideNUID in nuids:
                nuids.remove(self.sideNUID)
                nuid = nuids[0] if nuids else 0
                gamelog.debug('hjx debug arena getEnemyWinNum1---:', nuid, self.roundWinRec)
                return self.roundWinRec.get(nuid, 0)
            elif len(self.roundWinRec.values()) > 0:
                return self.roundWinRec.values()[0]
            else:
                return 0
        else:
            return 0

    def getSideIndex(self):
        for item in self.arenaStatistics:
            if self.id == item[8]:
                return item[0]

        return 0

    def getRoundCount(self):
        if hasattr(self, 'roundCount'):
            return self.roundCount
        return 0

    def getTotalArenaRound(self):
        fbNo = formula.getFubenNo(self.spaceNo)
        arenaMode = formula.fbNo2ArenaMode(fbNo)
        totalRound = AMD.data.get(arenaMode, {}).get('winCondition', 2) * 2 - 1
        return totalRound

    def getAddedScore(self):
        if hasattr(self, 'addedScore'):
            return self.addedScore
        return 0

    def getArenaMode(self):
        enableArenaMode = gameglobal.rds.configData.get('enableArenaMode', False)
        if enableArenaMode:
            if hasattr(self, 'arenaMode'):
                return self.arenaMode
            return gameglobal.rds.ui.arena.genArenaSortedModeData()[0]['mode']
        else:
            return gameglobal.rds.ui.arena.genArenaSortedModeData()[0]['mode']

    def setArenaMode(self, arenaMode):
        self.arenaMode = arenaMode

    def getArenaNo(self):
        if hasattr(self, 'fbNo'):
            return self.fbNo
        return const.FB_NO_ARENA_ALL

    def setArenaNo(self, fbNo):
        self.fbNo = fbNo

    def getArenaCallback(self):
        if hasattr(self, 'arenaCallback'):
            return self.arenaCallback
        return 0

    def setArenaCallback(self, callback):
        self.arenaCallback = callback

    def sendAddedScore(self, score):
        gamelog.debug('dxk@sendAddedScore', score)
        self.addedScore = score

    def showArenaResult(self):
        if self.inFubenTypes(const.FB_TYPE_ARENA):
            fbNo = formula.getFubenNo(self.spaceNo)
            if fbNo in const.FB_NO_LUN_ZHAN_YUN_DIAN:
                gamelog.info('showArenaResult')
                gameglobal.rds.ui.LZYDResult.show()
            else:
                gameglobal.rds.ui.arena.showResult = True
                gameglobal.rds.ui.arena.showArenaFinalResult()

    def arenaEndNotify(self, info, arenaStatistics):
        gamelog.debug('hjx debug arena: arenaEndNotify:', self.id)
        self.arenaStatistics = arenaStatistics
        gameglobal.rds.ui.arena.arenaIsTimeOut = True
        gameglobal.rds.ui.arena.resetArenaTimer()
        BigWorld.callback(6, Functor(self.showArenaResult))
        self.motionPin()
        self.showGameMsg(GMDD.data.ARENA_QUIT_IN_30S, ())
        self.addTimerCount(ARENA_QUIT, uiUtils.getDuelCountTime('quitTime', self.getArenaNo()))

    def calcCurrentCount(self):
        self.curTimeOfArena = self.getServerTime()
        self.deltaOfArena += self.curTimeOfArena - self.lastTimeOfArena
        self.countTimer -= int(round(self.deltaOfArena))
        gamelog.debug('@hjx arena#time:', self.lastTimeOfArena, self.curTimeOfArena, self.deltaOfArena, self.countTimer, self.id)
        self.lastTimeOfArena = self.curTimeOfArena

    def timerCounting(self, stage):
        if not hasattr(self, 'countTimer'):
            return
        if not self.isNeedCounting:
            BigWorld.cancelCallback(self.getArenaCallback())
            return
        self.calcCurrentCount()
        if self.countTimer <= 0:
            self.motionUnpin()
            self.callArenaMsg('showArenaStart', (self.inFubenTypes(const.FB_TYPE_ARENA), self.getRoundCount()))
            gameglobal.rds.ui.arena.refreshPrepIcon(False, False)
            gameglobal.rds.ui.arena.refreshPrepBtn(False)
        else:
            if self.inFuben() or formula.spaceInMultiLine(self.spaceNo):
                if stage == ARENA_START:
                    BigWorld.cancelCallback(self.getArenaCallback())
                    if self.countTimer in ANIMATION_SHOW_COUNT:
                        self.callArenaMsg('showCountDown15', (self.countTimer,))
                        gameglobal.rds.sound.playSound(gameglobal.SD_60)
                    elif self.countTimer in COUNT_DWON_NUM:
                        self.callArenaMsg('showCountDown5', (self.countTimer,))
                        gameglobal.rds.sound.playSound(gameglobal.SD_60)
                elif stage == ARENA_QUIT:
                    BigWorld.cancelCallback(self.getArenaCallback())
                if self.countTimer in SHOW_COUNT:
                    self.showGameMsg(ARENA_STAGE[stage][0], (utils.formatDuration(self.countTimer),))
            else:
                self.motionUnpin()
            self.setArenaCallback(BigWorld.callback(1, Functor(self.timerCounting, stage)))
        self.countTimer = self.countDurationTime

    def callArenaMsg(self, funcName, arg = None):
        gameglobal.rds.ui.arena.callArenaMsgFunc(funcName, arg)

    def addTimerCount(self, stage, durationTime, lastTimeStamp = None):
        self.countTimer = durationTime
        self.countDurationTime = durationTime
        self.deltaOfArena = 0
        self.isNeedCounting = True
        if lastTimeStamp:
            self.lastTimeOfArena = lastTimeStamp
        else:
            self.lastTimeOfArena = self.getServerTime()
        gamelog.debug('@hjx ssc#addTimerCount2:', self.id, self.lastTimeOfArena)
        self.timerCounting(stage)

    def notifyLeaveArena(self, roleName):
        gamelog.debug('hjx debug arena notifyLeaveArena', roleName)
        gameglobal.rds.ui.arena.stage = 1
        self.enableCountTimer = False
        self.showGameMsg(GMDD.data.ARENA_FORCE_QUIT, (roleName,))

    def resultNotify(self, result):
        gamelog.debug('hjx debug arena resultNotify:', result)
        self.arenaResultNotify(result)

    def arenaResultNotify(self, result):
        gamelog.debug('hjx debug arena arenaResultNotify:', result)
        msg = ''
        if result in const.LOSE_FLAG:
            msg = gameStrings.TEXT_UICONST_3507_2
        elif result == const.TIE:
            msg = gameStrings.TEXT_IMPARENA_322
        elif result in const.WIN_FLAG:
            result = const.WIN
            msg = gameStrings.TEXT_UICONST_3507
        self.arenaResult = result
        self.callArenaMsg('showGameOver', (result,))
        self.chatToEventEx(msg, const.CHANNEL_COLOR_RED)

    def countOn(self):
        gameglobal.rds.ui.arena.startArenaTimer(self.getArenaMode())
        if self.fbNo in const.FB_NO_ARENA_ROUND:
            gameglobal.rds.ui.arena.setArenaRound()

    def arenaStart(self):
        self.showGameMsg(GMDD.data.ARENA_START, ())
        self.countOn()

    def arenaSyncPrepareDict(self, sidePrepareDict):
        self.arenaSidePrepareDict = sidePrepareDict
        gameglobal.rds.ui.arena.refreshPrepInfo()

    def arenaChallengeQuickStart(self, challengeQuickReadyTime, timestamp):
        gamelog.debug('@hjx arenaChallenge#arenaChallengeQuickStart:', challengeQuickReadyTime, timestamp)
        gameglobal.rds.ui.arena.resetArenaTimer()
        callbackId = self.getArenaCallback()
        if callbackId > 0:
            BigWorld.cancelCallback(callbackId)
        self.addTimerCount(ARENA_START, challengeQuickReadyTime, timestamp)

    def arenaCountDown(self, tCountDownFrom):
        gamelog.debug('hjx debug arena:arenaCountDown:', self.id)
        gameglobal.rds.ui.arena.resetArenaTimer()
        self.addTimerCount(ARENA_START, utils.getArenaReadyTime(self.getArenaNo(), self.arenaPlayoffsCurRoundNum, self.getRoundCount()), tCountDownFrom)

    def arenaKill(self, roleName):
        gamelog.debug('hjx debug arena:arenaKill')
        if self == BigWorld.player():
            gameglobal.rds.sound.playSound(gameglobal.SD_65)
        self.showGameMsg(GMDD.data.ARENA_KILL_PLAYER, (roleName,))

    def enterArenaFailed(self, roleNames, msg):
        gamelog.debug('jorsef: enterArenaFailed', roleNames, msg)
        self.chatToEventEx(msg, const.CHANNEL_COLOR_RED)
        gameglobal.rds.ui.arena.closeTips()
        gameglobal.rds.ui.duelMatchTime.removeMatchTimeItem(self.getArenaMode())
        gameglobal.rds.ui.arena.setPanelBtnVisible(True)
        gameglobal.rds.ui.arena.refreshArenaPanel(stage=uiConst.ARENA_PANEL_START)
        self.arenaStage = uiConst.ARENA_PANEL_START
        gameglobal.rds.ui.arenaWait.closeArenaWait()
        gameglobal.rds.ui.dispatchEvent(events.EVENT_CHANGE_ARENA_STATE)

    def enterArenaRematch(self, msg):
        self.chatToEventEx(msg, const.CHANNEL_COLOR_RED)
        gameglobal.rds.ui.arena.closeTips()
        gameglobal.rds.ui.arena.setPanelBtnVisible(True)
        gameglobal.rds.ui.duelMatchTime.addMatchTimeItem(self.getArenaMode())
        gameglobal.rds.ui.arenaWait.closeArenaWait()
        self.arenaStage = uiConst.ARENA_PANEL_MATCHING
        gameglobal.rds.ui.dispatchEvent(events.EVENT_CHANGE_ARENA_STATE)

    def onConfirmEnterArenaSucc(self):
        gamelog.debug('jorsef: onConfirmEnterArenaSucc')
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_ARENA_MATCHED)
        if not gameglobal.rds.ui.arenaWait.isShow:
            gameglobal.rds.ui.arena.refreshArenaTip(uiConst.ARENA_ENTER_WAITING_TIP)
        if gameglobal.rds.ui.arenaCommonTips.widget:
            gameglobal.rds.ui.arenaCommonTips.hide()

    def arenaApplySucc(self, arenaMode):
        self.setArenaMode(arenaMode)
        gameglobal.rds.ui.arena.arenaBtnEnable = False
        gameglobal.rds.ui.duelMatchTime.addMatchTimeItem(arenaMode)
        gameglobal.rds.ui.arena.lastTimeStamp = self.getServerTime()
        gameglobal.rds.ui.arena.refreshArenaPanel(stage=uiConst.ARENA_PANEL_MATCHING)
        self.arenaStage = uiConst.ARENA_PANEL_MATCHING
        self.showGameMsg(GMDD.data.ARENA_APPLY_SUCC, ())
        gameglobal.rds.ui.dispatchEvent(events.EVENT_CHANGE_ARENA_STATE)

    def quitWaitingArena(self):
        gameglobal.rds.ui.duelMatchTime.removeMatchTimeItem(self.getArenaMode())
        gameglobal.rds.ui.arenaWait.closeArenaWait()
        gameglobal.rds.ui.arena.closeTips()
        gameglobal.rds.ui.arena.refreshArenaPanel(stage=uiConst.ARENA_PANEL_START)
        self.arenaStage = uiConst.ARENA_PANEL_START
        gameglobal.rds.ui.dispatchEvent(events.EVENT_CHANGE_ARENA_STATE)

    def applyArena(self):
        arenaMode = self.getArenaMode()
        minLv, maxLv = formula.getArenaLvByMode(arenaMode)
        if self.lv < minLv or self.lv > maxLv:
            self.applyArenaFailed()
            self.showGameMsg(GMDD.data.ARENA_APPLY_FAILED_LV, (minLv, maxLv))
            return
        if self.inCombat:
            self.applyArenaFailed()
            self.showGameMsg(GMDD.data.ARENA_APPLY_FAILED_IN_COMBAT, ())
            return
        if self.inFuben():
            self.applyArenaFailed()
            spaceName = formula.whatSpaceName(self.spaceNo)
            self.showGameMsg(GMDD.data.ARENA_APPLY_FAILED_IN_FUBEN, (spaceName,))
            return False
        if self.isInTeam():
            if self.groupHeader != self.id:
                self.showGameMsg(GMDD.data.ARENA_APPLY_FAILED_NOT_LEADER, ())
                return
            if arenaMode == const.ARENA_MODE_ALL:
                self.showGameMsg(GMDD.data.ARENA_QUICK_APPLY_FAILED_IN_TEAM, ())
                return
            self.base.applyArenaOfTeam(arenaMode)
        elif not self.isInGroup():
            self.base.applyArena(arenaMode)
        else:
            self.showGameMsg(GMDD.data.APPLY_FAILED_IN_GROUP, ())

    def applyArenaFailed(self):
        gameglobal.rds.ui.arena.refreshArenaPanel(uiConst.ARENA_PANEL_START)
        self.arenaStage = uiConst.ARENA_PANEL_START
        gameglobal.rds.ui.dispatchEvent(events.EVENT_CHANGE_ARENA_STATE)

    def abortArena(self):
        if BigWorld.player().inFightObserve() and not self.inClanChallengeOb():
            BigWorld.player().cell.endObserveFuben()
            return
        if formula.whatFubenType(self.mapID) == const.FB_TYPE_SCHOOL_TOP_MATCH:
            self.cell.leaveSchoolTopMatch()
            return
        if commcalc.getBitDword(self.flags, gametypes.FLAG_ARENA_PREPARING):
            if BigWorld.player().getArenaMode() in const.ARENA_CHALLENDE_MODE_LIST:
                self.showGameMsg(GMDD.data.ARENA_CHALLENGE_ABORT_FAILED_IN_PREPARING, ())
            else:
                self.showGameMsg(GMDD.data.ARENA_ABORT_FAILED_IN_PREPARING, ())
            return
        self.cell.abortArena(self.fbNo)

    def leaveArena(self):
        self.cell.leaveArena(self.fbNo)

    def cancelApplyArena(self):
        self.cell.cancelApplyArena(self.getArenaMode())

    def showConfirmMsg(self, fbNo, blockWarningList):
        if self.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            return
        self.setArenaNo(fbNo)
        gameglobal.rds.ui.arena.setPanelBtnVisible(False)
        self.arenaStage = uiConst.ARENA_PANEL_MATCHED
        enableAddScore = AD.data.get(fbNo, {}).get('enableAddScore', 0)
        if enableAddScore:
            gameglobal.rds.ui.arena.blockWarningList = blockWarningList
        else:
            gameglobal.rds.ui.arena.blockWarningList = []
        gameglobal.rds.ui.arena.tipsTimeStamp = self.getServerTime()
        gameglobal.rds.ui.arena.showConfirmTip(uiConst.ARENA_ENTER_TIP)
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_ARENA_MATCHED)
        uiUtils.showWindowEffect()
        gameglobal.rds.ui.dispatchEvent(events.EVENT_CHANGE_ARENA_STATE)

    def confirmEnterArena(self):
        self.cell.confirmEnterArena(self.getArenaMode())

    def confirmEnterArenaFailed(self):
        msg = gameglobal.rds.ui.arena.genConfirmDesc(gameStrings.TEXT_IMPARENA_513)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self._doConfirmEnterArenaFailed, yesBtnText=gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, noBtnText=gameStrings.TEXT_PLAYRECOMMPROXY_494_1)

    def _doConfirmEnterArenaFailed(self):
        self.cell.confirmEnterArenaFailed(self.getArenaMode())
        gameglobal.rds.ui.arena.refreshArenaPanel(stage=uiConst.ARENA_PANEL_START)
        gameglobal.rds.ui.arena.closeTips()

    def closeArena(self):
        self.cell.closeArena(self.fbNo)

    def notifyQuitArena(self):
        gamelog.debug('notifyQuitArena', self.id, BigWorld.player().id)
        self.isNeedCounting = False
        if self == BigWorld.player():
            self.switchHideMode(gameglobal.HIDE_MODE0)

    def arenaConfirm(self, confirmedInfo):
        gamelog.debug('hjx debug arenaConfirm:', confirmedInfo)
        if self == BigWorld.player():
            gameglobal.rds.ui.arenaWait.openArenaWait(confirmedInfo)

    def testArenaChoosePrint(self, msg):
        gamelog.debug('hjx debug choose:', msg)

    def onLeaveArena(self):
        gameglobal.rds.ui.arena.closeArenaInfo()
        self._refreshMemberBuffState(1)
        gameglobal.rds.ui.arena.refreshArenaPanel(stage=uiConst.ARENA_PANEL_START)
        self.arenaStage = uiConst.ARENA_PANEL_START
        gameglobal.rds.ui.player.setLv(self.lv)
        gameglobal.rds.ui.dispatchEvent(events.EVENT_CHANGE_ARENA_STATE)
        gameglobal.rds.ui.LZYDResult.hide()

    def enterArenaBefore(self):
        self.arenaReadyTime = getattr(self, 'arenaReadyTime', utils.getNow())
        gameglobal.rds.ui.arena.showArenaStats()
        BigWorld.callback(2.5, self._enterArenaBefore)

    def _enterArenaBefore(self):
        gameglobal.rds.ui.duelMatchTime.resetDuelMatch()
        gameglobal.rds.ui.arena.closeTips()
        gameglobal.rds.ui.teamComm.closeTeamPlayer()
        filterWidgets = [uiConst.WIDGET_ARENA_STATS,
         uiConst.WIDGET_TEAM_INVITE_V2,
         uiConst.WIDGET_CHAT_LOG,
         uiConst.WIDGET_FIGHT_OBSERVE_ACTION_BAR,
         uiConst.WIDGET_TOPBAR,
         uiConst.WIDGET_BULLET,
         uiConst.WIDGET_SKILL_PUSH,
         uiConst.WIDGET_BATTLE_FIELD_TIPS,
         uiConst.WIDGET_PUSH_MESSSAGES,
         uiConst.WIDGET_FEEDBACK_ICON,
         uiConst.WIDGET_BARRAGE,
         uiConst.WIDGET_WING_PUSH,
         uiConst.WIDGET_WING_CHEER_TOPBAR,
         uiConst.WIDGET_ARENA_PSKILL_HOVER,
         uiConst.WIDGET_BUFF_LISTENER_SHOW,
         uiConst.WIDGET_GENERAL_PUSH,
         uiConst.WIDGET_LZYD_PUSH]
        if self.inClanChallengeOb():
            filterWidgets.append(uiConst.WIDGET_BF_GUILD_TOURNAMENT_OBSERVE)
        filterWidgets.extend(uiConst.HUD_WIDGETS)
        gameglobal.rds.ui.unLoadAllWidget(filterWidgets)
        gameglobal.rds.ui.map.realClose()
        gameglobal.rds.ui.teamComm.refreshMemberInfo()
        gameglobal.rds.ui.teamEnemyArena.refreshMemberInfo()
        gameglobal.rds.ui.arena.arenaIsTimeOut = False
        gameglobal.rds.ui.arena.openArenaMsg()
        gameglobal.rds.ui.chat.goToArena()
        gameglobal.rds.ui.player.setLv(self.lv)
        self._refreshMemberBuffState(1)
        gameglobal.rds.ui.arena.showResult = False
        self.showCancelHideInBFConfirm()
        self.addedScore = 0

    def isArenaMatching(self):
        return gameglobal.rds.ui.arena.getStage() == uiConst.ARENA_PANEL_MATCHING

    def confirmCancelApplyArena(self, cause, callbackOnConfirm):
        MBButton = messageBoxProxy.MBButton
        buttons = [MBButton(gameStrings.TEXT_IMPARENA_582, callbackOnConfirm), MBButton(gameStrings.TEXT_PLAYRECOMMPROXY_494_1, self.messageBoxCancel)]
        self.msgBoxId = gameglobal.rds.ui.messageBox.show(True, gameStrings.TEXT_FUBENDEGREEPROXY_56, gameStrings.TEXT_IMPARENA_584 % cause, buttons)

    def onCheckArenaSkillSchemeFail(self, reason):
        self.applyArenaFailed()

    def onQueryArenaHistoryInfo(self, arenaInfo):
        arenaInfo = cPickle.loads(zlib.decompress(arenaInfo))
        gamelog.debug('@lhb onQueryArenaHistory ', arenaInfo)
        gameglobal.rds.ui.pvpArenaV2.transformData(arenaInfo)

    def onChangeBalanceArneaMode(self):
        gameglobal.rds.ui.balanceArenaHover.onChangeArenaMode(self.arenaModeCache)

    def set_arenaModeCache(self, old):
        self.onChangeBalanceArneaMode()

    def isInBlanceArenaWaitRoom(self):
        return formula.isBalanceArenaCrossServerML(formula.getMLGNo(self.spaceNo))

    def _getArenaWeekPlayerCnt(self, arenaModeType = const.ARENA_MODE_TYPE_BALANCE):
        if arenaModeType == const.ARENA_MODE_TYPE_BALANCE:
            if gameconfigCommon.enableBalanceArenaWeekCntLimit():
                return self.validBalanceArenaWeeklyCnt
            else:
                return self.arenaInfoEx.weekPlayCnt
        else:
            return self.arenaInfo.weekPlayCnt
