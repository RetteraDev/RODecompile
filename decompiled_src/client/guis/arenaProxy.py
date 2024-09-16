#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/arenaProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import formula
import gameglobal
import gametypes
import uiConst
import const
import gamelog
import uiUtils
import utils
from uiProxy import DataProxy
from ui import gbk2unicode
from callbackHelper import Functor
from guis.asObject import ASObject
from guis.asObject import ASUtils
from gamestrings import gameStrings
from data import school_data as SD
from data import arena_mode_data as AMD
from data import arena_score_desc_data as ASDD
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD
from data import sys_config_data as SCD
from data import message_desc_data as MSGDD
from data import duel_config_data as DCD
ITEM_FLAG_SELF = 1
ITEM_FLAG_FRIEND = 2
ITEM_FLAG_ENEMY = 3
MIN_NUM = 1

class ArenaProxy(DataProxy):
    PANEL_TYPE_BATTLE_FIELD = 2
    PANEL_TYPE_ARENA = 1

    def __init__(self, uiAdapter):
        super(ArenaProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerArenaPanel': self.onRegisterArenaPanel,
         'getPanelInfo': self.onGetPanelInfo,
         'clickFuncBtn': self.onClickFuncBtn,
         'clickShareBtn': self.onClickShareBtn,
         'applyOfPersonClick': self.onApplyOfPersonClick,
         'quickApply': self.onQuickApply,
         'selectArenaMode': self.onSelectArenaMode,
         'getArenaMode': self.onGetArenaMode,
         'getEnableArenaMode': self.onGetEnableArenaMode,
         'getTipsInfo': self.onGetTipsInfo,
         'arenaOkClick': self.onArenaOkClick,
         'arenaTimeout': self.onArenaTimeout,
         'arenaCancelClick': self.onArenaCancelClick,
         'getArenaConfirmDesc': self.onGetArenaConfirmDesc,
         'getInfo': self.onGetInfo,
         'quitGameClick': self.onQuitGameClick,
         'quitArenaClick': self.onQuitArenaClick,
         'arenaTmpResultClick': self.onArenaTmpResultClick,
         'getArenaTmpResultInfo': self.onGetArenaTmpResultInfo,
         'arenaSumClose': self.closeArenaTmpResult,
         'arenaStatClick': self.onArenaStatClick,
         'arenaEndClick': self.onArenaEndClick,
         'arenaTipMini': self.onArenaTipMini,
         'exchangeFame': self.onExchangeFame,
         'getArenaResult': self.onGetArenaResult,
         'getArenaSortedResult': self.onGetArenaSortedResult,
         'playArenaSound': self.onPlayArenaSound,
         'getArenaBtnNamesByMode': self.onGetArenaBtnNamesByMode,
         'getExchangeFameFlag': self.onGetExchangeFameFlag,
         'openRank': self.onOpenRank,
         'getArenaLevelDesc': self.onGetArenaLevelDesc,
         'getCountWeek': self.onGetCountWeek,
         'getPrepBtnShow': self.onGetPrepBtnShow,
         'handleClickPrep': self.onHandleClickPrep,
         'voteBalanceArenaTemplate': self.onVoteBalanceArenaTemplate,
         'getLeftTime': self.onGetLeftTime}
        self.bindType = 'arena'
        self.reset()
        uiAdapter.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_ARENA_MATCHED, {'click': self.clickPushIcon})

    def reset(self):
        self.arenaPanelMc = None
        self.arenaStatsMed = None
        self.arenaFinalResultMed = None
        self.arenaTmpResultMed = None
        self.arenaTipMed = None
        self.arenaCountDownMed = None
        self.isShowBattle = False
        self.showResult = False
        self.setStage(uiConst.ARENA_PANEL_START)
        self.tipsType = uiConst.ARENA_APPLY_TIP
        self.tipsTimeStamp = 0
        self.isShow = False
        self.isArenaTmpResultShow = False
        self.campSort = True
        self.sortedArray = None
        self.rankType = uiConst.ARENA_SORT_BY_CAMP
        self.arenaIsTimeOut = False
        self.whichConfirm = uiConst.ARENA_APPLY_TIP
        self.arenaBtnEnable = True
        self.lastTimeStamp = 0
        self.arenaMode = const.ARENA_MODE_ALL
        self.blockWarningList = []
        self.resultWidgetId = uiConst.WIDGET_ARENA_FINAL_RESULT
        self.isSchoolTop = False
        p = BigWorld.player()
        self.prepInfo = {'minePrep': False,
         'theirPrep': False}

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.arenaPanelMc = None
        self.arenaStatsMed = None
        self.arenaTmpResultMed = None
        self.arenaTipMed = None
        self.arenaCountDownMed = None
        self.isShowBattle = False
        self.arenaFinalResultMed = None
        self.isSchoolTop = False
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ARENA_TIPS)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ARENA_STATS)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ARENA_COUNT_DOWN)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ARENA_TMP_RESULT)
        gameglobal.rds.ui.unLoadWidget(self.resultWidgetId)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ARENA_FINAL_RESULT_BG)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_ARENA_COUNT_DOWN:
            self.arenaCountDownMed = mediator
        elif widgetId == uiConst.WIDGET_ARENA_TIPS:
            self.arenaTipMed = mediator
        elif widgetId == uiConst.WIDGET_ARENA_STATS:
            self.arenaStatsMed = mediator
        elif widgetId == uiConst.WIDGET_ARENA_TMP_RESULT:
            self.arenaTmpResultMed = mediator
        elif widgetId == uiConst.WIDGET_ARENA_FINAL_RESULT:
            self.arenaFinalResultMed = mediator
        elif widgetId == uiConst.WIDGET_ARENA_FINAL_RESULT_XINMO:
            self.arenaFinalResultMed = mediator
        elif widgetId == uiConst.WIDGET_BALANCE_ARENA_FINAL_RESULT:
            self.arenaFinalResultMed = mediator

    def onRegisterArenaPanel(self, *arg):
        self.arenaPanelMc = arg[3][0]

    def getValue(self, key):
        if key == 'arena.closeBtn':
            if self.arenaIsTimeOut:
                return GfxValue(False)
            else:
                return GfxValue(True)
        elif key == 'arena.sumModal':
            return GfxValue(True)
            if self.arenaIsTimeOut:
                return GfxValue(True)
            else:
                return GfxValue(False)

    def closeArenaFinalResult(self):
        self.isSchoolTop = False
        gameglobal.rds.ui.unLoadWidget(self.resultWidgetId)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ARENA_FINAL_RESULT_BG)

    def op(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ARENA_FINAL_RESULT_BG)
        if formula.spaceInWingWorldXinMoArena(BigWorld.player().spaceNo):
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ARENA_FINAL_RESULT_XINMO)
            return
        if BigWorld.player().isUsingTemp() and gameglobal.rds.configData.get('enableBalanceArenaFinalResult', False):
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_BALANCE_ARENA_FINAL_RESULT)
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ARENA_FINAL_RESULT)

    def onIsInTeam(self, *arg):
        p = BigWorld.player()
        return GfxValue(p.isInTeam())

    def onQuickApply(self, *arg):
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_ARENAPROXY_187, self.onRealQuickApply)

    def onRealQuickApply(self):
        p = BigWorld.player()
        p.arenaMode = const.ARENA_MODE_ALL
        p.applyArena()

    def onSelectArenaMode(self, *arg):
        self.arenaMode = int(arg[3][0].GetNumber())
        gamelog.debug('@hjx arena#onSelectArenaMode:', self.arenaMode)
        p = BigWorld.player()
        p.setArenaMode(self.arenaMode)

    def onGetCountWeek(self, *arg):
        p = BigWorld.player()
        total = SCD.data.get('arenaFameExchangePlayCntLimit', 15)
        return GfxValue(gbk2unicode(gameStrings.TEXT_ARENAPROXY_203 % (p.arenaInfo.weekPlayCnt, total)))

    def _getStage1Content(self):
        item = AMD.data.get(self.arenaMode, {})
        ar = self.movie.CreateArray()
        ar.SetElement(0, GfxValue(gbk2unicode(item.get('title', ''))))
        ar.SetElement(1, GfxValue(gbk2unicode(item.get('desc', ''))))
        ar.SetElement(2, GfxValue(gbk2unicode(item.get('winStandard', ''))))
        return ar

    def _getStage2Content(self):
        ar = self.movie.CreateArray()
        ar.SetElement(0, GfxValue(gbk2unicode(gameStrings.TEXT_ARENAPROXY_217)))
        return ar

    def _getStage3Content(self):
        ar = self.movie.CreateArray()
        ar.SetElement(0, GfxValue(gbk2unicode(gameStrings.TEXT_ARENAPROXY_222)))
        ar.SetElement(1, GfxValue(gbk2unicode('90s')))
        return ar

    def _getStage4Content(self):
        ar = self.movie.CreateArray()
        ar.SetElement(0, GfxValue(gbk2unicode(gameStrings.TEXT_ARENAPROXY_228)))
        return ar

    def _getText(self):
        if self.getStage() == uiConst.ARENA_PANEL_START:
            return (self._getStage1Content(), GfxValue(gbk2unicode(gameStrings.TEXT_BALANCEARENAHOVERPROXY_143)))
        if self.getStage() == uiConst.ARENA_PANEL_WAITING_TEAM:
            return (self._getStage2Content(), GfxValue(gbk2unicode(gameStrings.TEXT_ARENAPROXY_235)))
        if self.getStage() == uiConst.ARENA_PANEL_MATCHING:
            return (self._getStage3Content(), GfxValue(gbk2unicode(gameStrings.TEXT_ARENAPROXY_235)))
        if self.getStage() == uiConst.ARENA_PANEL_IN_GAME:
            return (self._getStage4Content(), GfxValue(gbk2unicode(gameStrings.TEXT_ARENAPROXY_239)))

    def getStage(self):
        return self.stage

    def setStage(self, stage):
        self.stage = stage
        if self.stage == uiConst.ARENA_PANEL_START:
            self.arenaBtnEnable = True

    def getCount(self):
        p = BigWorld.player()
        if self.getStage() == uiConst.ARENA_PANEL_MATCHING:
            interval = p.getServerTime() - self.lastTimeStamp
            return int(interval)
        return 0

    def getWinRate(self, winCount, loseCount, duelCount):
        if winCount + loseCount + duelCount == 0:
            val = '0.00'
        else:
            val = '%.2f' % (float(winCount) / (winCount + loseCount + duelCount) * 100)
        return str(val)

    def getWinMatch(self):
        p = BigWorld.player()
        arenaInfo = p.arenaInfo
        if formula.isBalanceAreanFb(formula.getFubenNo(p.spaceNo)):
            arenaInfo = p.arenaInfoEx
        details = p.arenaInfo.get(p.getArenaMode(), None)
        if details:
            return details.winMatch
        else:
            return 0

    def getLoseMatch(self):
        p = BigWorld.player()
        arenaInfo = p.arenaInfo
        if formula.isBalanceAreanFb(formula.getFubenNo(p.spaceNo)):
            arenaInfo = p.arenaInfoEx
        details = arenaInfo.get(p.getArenaMode(), None)
        if details:
            return details.loseMatch
        else:
            return 0

    def getDuelMatch(self):
        p = BigWorld.player()
        arenaInfo = p.arenaInfo
        if formula.isBalanceAreanFb(formula.getFubenNo(p.spaceNo)):
            arenaInfo = p.arenaInfoEx
        details = arenaInfo.get(p.getArenaMode(), None)
        if details:
            return details.duelMatch
        else:
            return 0

    def getKillCount(self):
        p = BigWorld.player()
        arenaInfo = p.arenaInfo
        if formula.isBalanceAreanFb(formula.getFubenNo(p.spaceNo)):
            arenaInfo = p.arenaInfoEx
        details = arenaInfo.get(p.getArenaMode(), None)
        if details:
            return details.killCount
        else:
            return 0

    def _genScoreDesc(self):
        p = BigWorld.player()
        curDesc = ''
        curFrame = 'orange1'
        tmpASDD = ASDD.data.keys()
        tmpASDD.sort()
        index = 0
        for minS, maxS in tmpASDD:
            if p.arenaInfo.arenaScore >= minS and p.arenaInfo.arenaScore <= maxS:
                curDesc = ASDD.data[minS, maxS].get('desc', gameStrings.TEXT_ARENAPROXY_321) + ' ' + gameStrings.TEXT_ARENAPROXY_321_1 + str(ASDD.data[minS, maxS].get('fameReward', 0))
                curFrame = ASDD.data[minS, maxS].get('frameName', 'orange1')
                break
            index += 1

        if index == len(ASDD.data.keys()):
            key = tmpASDD[index - 1]
        elif index == len(ASDD.data.keys()) - 1:
            key = tmpASDD[index]
        else:
            key = tmpASDD[index + 1]
        nextDesc = ASDD.data[key].get('desc', gameStrings.TEXT_ARENAPROXY_321) + ' ' + gameStrings.TEXT_ARENAPROXY_321_1 + str(ASDD.data[key].get('fameReward', 0))
        return (curDesc, curFrame, nextDesc)

    def onGetPanelInfo(self, *arg):
        p = BigWorld.player()
        arenaInfo = p.arenaInfo
        if formula.isBalanceAreanFb(formula.getFubenNo(p.spaceNo)):
            arenaInfo = p.arenaInfoEx
        curDesc, curFrame, nextDesc = self._genScoreDesc()
        text = self._getText()
        ret = self.movie.CreateObject()
        ret.SetMember('stage', GfxValue(self.getStage()))
        ret.SetMember('content', text[0])
        ret.SetMember('btnText', text[1])
        ret.SetMember('count', GfxValue(self.getCount()))
        ret.SetMember('curDesc', GfxValue(gbk2unicode(curDesc)))
        ret.SetMember('curFrame', GfxValue(gbk2unicode(curFrame)))
        ret.SetMember('nextDesc', GfxValue(gbk2unicode(nextDesc)))
        ret.SetMember('score', GfxValue(arenaInfo.arenaScore))
        ret.SetMember('fame', GfxValue(p.fame.get(const.JUN_ZI_FAME_ID, 0)))
        ret.SetMember('arenaCount', GfxValue(self.getWinMatch() + self.getLoseMatch() + self.getDuelMatch()))
        ret.SetMember('arenaWinCount', GfxValue(self.getWinMatch()))
        ret.SetMember('arenaWinRate', GfxValue(self.getWinRate(self.getWinMatch(), self.getLoseMatch(), self.getDuelMatch())))
        ret.SetMember('arenaKilledCount', GfxValue(self.getKillCount()))
        ret.SetMember('isQuickApply', GfxValue(p.getArenaMode() == const.ARENA_MODE_ALL))
        return ret

    def showBattlePanel(self):
        gameglobal.rds.ui.pvPPanel.toggle(uiConst.PVP_BG_V2_TAB_BATTLE_FIELD)

    def refreshArenaPanel(self, stage = uiConst.ARENA_PANEL_START):
        self.setStage(stage)

    def hideArenaPanel(self, *arg):
        self.isShow = False

    def onClickFuncBtn(self, *arg):
        stage = int(arg[3][0].GetNumber())
        arenaMode = int(arg[3][1].GetNumber())
        p = BigWorld.player()
        if stage == uiConst.ARENA_PANEL_START:
            if self.arenaBtnEnable:
                if not p.isInTeam():
                    p.showGameMsg(GMDD.data.DUEL_APPLY_FAILED_NOT_IN_TEAM, ())
                    return
                p.arenaMode = arenaMode
                p.applyArena()
            else:
                return
        elif stage == uiConst.ARENA_PANEL_WAITING_TEAM:
            pass
        elif stage == uiConst.ARENA_PANEL_MATCHING:
            p.cancelApplyArena()
            self.arenaBtnEnable = True
        elif stage == uiConst.ARENA_PANEL_IN_GAME:
            p.abortArena()

    def onApplyOfPersonClick(self, *arg):
        p = BigWorld.player()
        arenaMode = int(arg[3][0].GetNumber())
        if p.isInTeam():
            p.showGameMsg(GMDD.data.DUEL_APPLY_FAILED_IN_TEAM, ())
            return
        p.arenaMode = arenaMode
        p.applyArena()

    def showTips(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ARENA_TIPS, False)

    def closeTips(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ARENA_TIPS)
        self.arenaTipMed = None
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_ARENA_MATCHED)

    def onArenaTipMini(self, *arg):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ARENA_TIPS)
        self.arenaTipMed = None

    def genConfirmDesc(self, msg):
        p = BigWorld.player()
        arenaMode = p.getArenaMode()
        if arenaMode == const.ARENA_MODE_CROSS_MS_ROUND_2V2_DOUBLE_ARENA:
            msg = uiUtils.getTextFromGMD(GMDD.data.QUIT_DOUBLE_ARENA_MATCH)
        return msg

    def onGetArenaConfirmDesc(self, *args):
        msg = self.genConfirmDesc(gameStrings.TEXT_ARENAPROXY_434)
        return GfxValue(gbk2unicode(msg))

    def showConfirmTip(self, tipsType):
        self.refreshArenaTip(tipsType)

    def onGetTipsInfo(self, *arg):
        p = BigWorld.player()
        ret = self.movie.CreateObject()
        self.tipsTimeStamp = utils.getNow()
        ret.SetMember('type', GfxValue(self.tipsType))
        ret.SetMember('timerMaxValue', GfxValue(const.ARENA_CONFIRM_DELAY))
        ret.SetMember('timerCurValue', GfxValue(int(const.ARENA_CONFIRM_DELAY - (p.getServerTime() - self.tipsTimeStamp) - 3)))
        return ret

    def setPanelBtnVisible(self, flag):
        if self.arenaPanelMc:
            self.arenaPanelMc.Invoke('setBtnVisible', GfxValue(flag))

    def refreshArenaTip(self, tipsType = uiConst.ARENA_ENTER_TIP):
        self.tipsType = tipsType
        if self.arenaTipMed:
            self.arenaTipMed.Invoke('refreshPanel')
        else:
            self.showTips()

    def clickPushIcon(self):
        self.refreshArenaTip(uiConst.ARENA_ENTER_TIP)

    def onArenaOkClick(self, *arg):
        self.whichConfirm = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        if self.whichConfirm == uiConst.ARENA_APPLY_TIP:
            pass
        elif self.whichConfirm == uiConst.ARENA_QUIT_WAITING_TIP:
            pass
        elif self.whichConfirm == uiConst.ARENA_QUIT_TIP:
            pass
        elif self.whichConfirm == uiConst.ARENA_QUIT_GAME_TIP:
            pass
        elif self.whichConfirm == uiConst.ARENA_ENTER_TIP:
            if uiUtils.inNeedNotifyStates():
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_ARENAPROXY_478, self.onRealConfirmEnter)
            else:
                self._realConfirmEnter()
        elif self.whichConfirm == uiConst.ARENA_REMATCH_TIP:
            p.applyArena()
            self.closeTips()

    def onArenaTimeout(self, *args):
        stage = int(args[3][0].GetNumber())
        if stage != uiConst.ARENA_ENTER_TIP:
            return
        BigWorld.player().confirmEnterArena()

    def onRealConfirmEnter(self):
        self._realConfirmEnter()

    def _realConfirmEnter(self):
        BigWorld.player().confirmEnterArena()
        self.setPanelBtnVisible(False)

    def onArenaCancelClick(self, *arg):
        self.whichCancel = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        if self.whichCancel == uiConst.ARENA_APPLY_TIP:
            self.closeTips()
        elif self.whichCancel == uiConst.ARENA_QUIT_WAITING_TIP:
            self.closeTips()
        elif self.whichCancel == uiConst.ARENA_QUIT_TIP:
            self.closeTips()
        elif self.whichCancel == uiConst.ARENA_QUIT_GAME_TIP:
            self.closeTips()
        elif self.whichCancel == uiConst.ARENA_ENTER_TIP:
            p.confirmEnterArenaFailed()
        elif self.whichCancel == uiConst.ARENA_REMATCH_TIP:
            self.setPanelBtnVisible(True)
            self.refreshArenaPanel(stage=uiConst.ARENA_PANEL_START)
            self.closeTips()

    def showArenaStats(self):
        self.setStage(uiConst.ARENA_PANEL_IN_GAME)
        if self.arenaStatsMed:
            self.arenaStatsMed.Invoke('refreshPanel')

    def closeArenaInfo(self):
        if self.getStage() == uiConst.ARENA_PANEL_IN_GAME:
            self.setStage(uiConst.ARENA_PANEL_START)
        self.arenaStatsMed = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ARENA_STATS)
        self.closeArenaTmpResult(0)
        self.closeArenaCountDown()
        self.closeArenaFinalResult()
        gameglobal.rds.ui.teamComm.closeTeamPlayer()
        gameglobal.rds.ui.teamEnemyArena.closeTeamPlayer()

    def _getArenaHeadInfoContent(self):
        p = BigWorld.player()
        duration = self._getAttrByMode(p.getArenaMode(), 'duration')
        timePassing = duration - (p.getServerTime() - p.arenaReadyTime)
        ar = self.movie.CreateArray()
        ar.SetElement(0, GfxValue(p.getSumAliveMan(0)))
        ar.SetElement(1, GfxValue(p.getSumMan(0)))
        ar.SetElement(2, GfxValue(p.getSumAliveMan(1)))
        ar.SetElement(3, GfxValue(p.getSumMan(1)))
        ar.SetElement(4, GfxValue(p.getSumKilled()))
        ar.SetElement(5, GfxValue(p.getSumBeKilled()))
        ar.SetElement(6, GfxValue(self._getAttrByMode(p.getArenaMode(), 'winCondition')))
        ar.SetElement(7, GfxValue(timePassing))
        return ar

    def _getAttrByMode(self, arenaMode, attr):
        if AMD.data.has_key(arenaMode):
            return AMD.data[arenaMode].get(attr, 0)
        raise Exception('arenaMode error in _getAttrByMode!!!')

    def _genRoundDesc(self):
        p = BigWorld.player()
        return str(min(p.getRoundCount(), p.getTotalArenaRound())) + '/' + str(p.getTotalArenaRound())

    def _getArenaWinInfoContent(self):
        p = BigWorld.player()
        duration = AMD.data.get(p.getArenaMode(), {}).get('duration', 600)
        timePassing = duration - (p.getServerTime() - getattr(p, 'arenaReadyTime', p.getServerTime()))
        ar = self.movie.CreateArray()
        ar.SetElement(0, GfxValue(p.getMyWinNum()))
        ar.SetElement(1, GfxValue(p.getEnemyWinNum()))
        ar.SetElement(2, GfxValue(timePassing))
        ar.SetElement(3, GfxValue(self._genRoundDesc()))
        ar.SetElement(4, uiUtils.dict2GfxDict(self.prepInfo))
        return ar

    def getSchoolTopWinNums(self):
        gbId0 = 0
        gbId1 = 0
        p = BigWorld.player()
        finalCandidates = getattr(p, 'finalCandidates', [])
        for candidate in finalCandidates:
            if candidate.get('isSchoolTop', False):
                gbId0 = candidate.get('gbId', 0)
            else:
                gbId1 = candidate.get('gbId', 0)

        schoolTopMatchScore = getattr(p, 'schoolTopMatchScore', [])
        scoreInfo = {}
        for gbId, roleName in schoolTopMatchScore:
            score = scoreInfo.get(gbId, 0)
            scoreInfo[gbId] = score + 1

        return (scoreInfo.get(gbId1, 0), scoreInfo.get(gbId0, 0))

    def _getSchoolTopWinInfoContent(self):
        p = BigWorld.player()
        timePassing = max(0, getattr(p, 'schoolTopTimeStamp', 0) - utils.getNow())
        leftWinNums, rightWinNums = self.getSchoolTopWinNums()
        ar = self.movie.CreateArray()
        ar.SetElement(0, GfxValue(leftWinNums))
        ar.SetElement(1, GfxValue(rightWinNums))
        ar.SetElement(2, GfxValue(timePassing))
        ar.SetElement(3, GfxValue('%d/%d' % (leftWinNums + rightWinNums, 3)))
        prepStage = getattr(p, 'schoolTopMatchStage', None) in (gametypes.SCHOOL_TOP_MATCH_PHASE_ROUND_1_READY, gametypes.SCHOOL_TOP_MATCH_PHASE_ROUND_2_READY, gametypes.SCHOOL_TOP_MATCH_PHASE_ROUND_3_READY)
        ar.SetElement(4, uiUtils.dict2GfxDict({'minePrep': prepStage,
         'theirPrep': prepStage}))
        return ar

    def startArenaTimer(self, arenaMode):
        if self.arenaStatsMed:
            p = BigWorld.player()
            if p.inClanChallenge():
                duration = self._getAttrByMode(arenaMode, 'duration')
                timePassing = duration - (p.getServerTime() - p.arenaReadyTime)
            else:
                timePassing = self._getAttrByMode(arenaMode, 'duration')
            self.arenaStatsMed.Invoke('startTimer', GfxValue(timePassing))

    def setArenaRound(self):
        p = BigWorld.player()
        if self.arenaStatsMed:
            gamelog.debug('hjx debug arena setArenaRound:', p.getRoundCount())
            self.arenaStatsMed.Invoke('setRoundCount', GfxValue(self._genRoundDesc()))

    def resetArenaTimer(self):
        if self.arenaStatsMed:
            self.arenaStatsMed.Invoke('resetTimer')

    def getPanelByMode(self):
        p = BigWorld.player()
        if p.getArenaNo() in const.FB_NO_ARENA_TDM:
            return uiConst.ARENA_HEAD_INFO
        else:
            return uiConst.ARENA_WIN_INFO

    def onGetArenaMode(self, *arg):
        p = BigWorld.player()
        self.arenaMode = p.getArenaMode()
        return GfxValue(self.arenaMode)

    def onGetEnableArenaMode(self, *arg):
        ret = self.movie.CreateObject()
        for key, value in AMD.data.items():
            enable = value.get('isEnableUIApply', 0)
            if gameglobal.rds.configData.get('enableCrossServerArena', False):
                enable = enable and key in const.FB_NO_ARENA_CROSS_SERVER_MODES
            else:
                enable = enable and key not in const.FB_NO_ARENA_CROSS_SERVER_MODES
            ret.SetMember(str(key), GfxValue(enable))

        return ret

    def onGetInfo(self, *arg):
        p = BigWorld.player()
        ret = self.movie.CreateObject()
        ret.SetMember('type', GfxValue(self.getPanelByMode()))
        ret.SetMember('isTroopLogon', GfxValue(p.get_isTroopLogon() or self.isSchoolTop or p.inClanChallenge() and utils.getNow() >= p.arenaReadyTime))
        ret.SetMember('isSchoolTop', GfxValue(self.isSchoolTop))
        if self.getPanelByMode() == uiConst.ARENA_HEAD_INFO:
            ret.SetMember('content', self._getArenaHeadInfoContent())
        else:
            if self.isSchoolTop:
                content = self._getSchoolTopWinInfoContent()
            else:
                content = self._getArenaWinInfoContent()
            ret.SetMember('content', content)
        return ret

    def onQuitGameClick(self, *arg):
        p = BigWorld.player()
        p.abortArena()

    def onQuitArenaClick(self, *arg):
        p = BigWorld.player()
        if self.isSchoolTop:
            p.cell.leaveSchoolTopMatch()
            self.closeArenaFinalResult()
        else:
            p.leaveArena()

    def refreshArenaTmpResult(self, isNeedSort = True):
        if isNeedSort:
            p = BigWorld.player()
            self.sortedArray = self.sortByName(p.arenaStatistics, self.rankType)
        if self.arenaTmpResultMed:
            self.arenaTmpResultMed.Invoke('refreshPanel')

    def showArenaTmpResult(self):
        p = BigWorld.player()
        self.sortedArray = self.sortByName(getattr(p, 'arenaStatistics', {}), uiConst.ARENA_SORT_BY_CAMP)
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ARENA_TMP_RESULT, True)
        self.isArenaTmpResultShow = True

    def _genTestData(self):
        p = BigWorld.player()
        p.sideNUID = 1234
        p.arenaStatistics = [{'level': 10,
          'campNum': 0,
          'killedNum': 10,
          'assistAtkNum': 0,
          'beKilledNum': 3,
          'cureNum': 0,
          'damageNum': 231,
          'school': 3,
          'roleName': 'test1',
          'id': p.id,
          'sideNUID': p.sideNUID},
         {'level': 10,
          'campNum': 0,
          'killedNum': 10,
          'assistAtkNum': 4,
          'beKilledNum': 3,
          'cureNum': 12,
          'damageNum': 4545,
          'school': 4,
          'roleName': 'test2',
          'id': 5242,
          'sideNUID': p.sideNUID},
         {'level': 10,
          'campNum': 0,
          'killedNum': 10,
          'assistAtkNum': 2,
          'beKilledNum': 11,
          'cureNum': 122,
          'damageNum': 23,
          'school': 5,
          'roleName': 'test3',
          'id': 5243,
          'sideNUID': p.sideNUID},
         {'level': 10,
          'campNum': 1,
          'killedNum': 10,
          'assistAtkNum': 6,
          'beKilledNum': 3,
          'cureNum': 0,
          'damageNum': 405,
          'school': 6,
          'roleName': 'test4',
          'id': 5244,
          'sideNUID': 456},
         {'level': 10,
          'campNum': 1,
          'killedNum': 10,
          'assistAtkNum': 1,
          'beKilledNum': 3,
          'cureNum': 10,
          'damageNum': 45,
          'school': 7,
          'roleName': 'test5',
          'id': 5245,
          'sideNUID': 456},
         {'level': 10,
          'campNum': 1,
          'killedNum': 10,
          'assistAtkNum': 9,
          'beKilledNum': 6,
          'cureNum': 0,
          'damageNum': 12,
          'school': 8,
          'roleName': 'test6',
          'id': 5246,
          'sideNUID': 456}]

    def _updateTestData(self):
        p = BigWorld.player()
        p.arenaStatistics[0]['killedNum'] = 15

    def _doubleCheckForFinalResult(self):
        tmpArray = []
        p = BigWorld.player()
        index = 0
        for item in self.sortedArray:
            if item['sideNUID'] == p.sideNUID:
                tmpArray.append(item)
                index += 1

        if index > len(self.sortedArray) / 2:
            gamelog.error('@hjx reportCritical error:', index, self.sortedArray)
        for item in self.sortedArray:
            if item not in tmpArray:
                tmpArray.append(item)

        self.sortedArray = tmpArray

    def showArenaFinalResult(self):
        p = BigWorld.player()
        self.sortedArray = self.sortByName(p.arenaStatistics, uiConst.ARENA_SORT_BY_CAMP)
        self._doubleCheckForFinalResult()
        self.resultWidgetId = self.getResultWidgetId()
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ARENA_FINAL_RESULT_BG)
        gameglobal.rds.ui.loadWidget(self.resultWidgetId)

    def showSchoolTopFinalResult(self):
        p = BigWorld.player()
        self.isSchoolTop = True
        self.sortedArray = p.arenaStatistics
        self.resultWidgetId = uiConst.WIDGET_ARENA_FINAL_RESULT_XINMO
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ARENA_FINAL_RESULT_BG)
        gameglobal.rds.ui.loadWidget(self.resultWidgetId)

    def closeArenaTmpResult(self, *arg):
        self.arenaTmpResultMed = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ARENA_TMP_RESULT)
        self.isArenaTmpResultShow = False
        self.rankType = uiConst.ARENA_SORT_BY_CAMP

    def onArenaEndClick(self, *arg):
        p = BigWorld.player()
        p.leaveArena()
        if self.arenaIsTimeOut:
            p.countTimer = 1
        self.arenaIsTimeOut = False

    def sortByName(self, ar, attrName, myReverse = True):
        return sorted(ar, cmp=lambda x, y: cmp(x[attrName], y[attrName]), reverse=myReverse)

    def _genItemFlag(self, item):
        p = BigWorld.player()
        if item['id'] == p.id:
            return ITEM_FLAG_SELF
        elif getattr(p, 'sideNUID', 0) == item['sideNUID']:
            return ITEM_FLAG_FRIEND
        else:
            return ITEM_FLAG_ENEMY

    def _getItemInfo(self):
        p = BigWorld.player()
        ret = self.movie.CreateArray()
        index = 0
        for item in self.sortedArray:
            if not p._checkValidSchool(item['school']):
                continue
            obj = self.movie.CreateObject()
            obj.SetMember('itemFlag', GfxValue(self._genItemFlag(item)))
            if self.showResult:
                newName = uiUtils.genDuelCrossName(item['roleName'], item.get('fromHostName', ''))
                if formula.isBalanceAreanFb(formula.getFubenNo(p.spaceNo)):
                    newName = item['roleName']
                obj.SetMember('roleName', GfxValue(gbk2unicode(newName)))
            else:
                newName = uiUtils.genDuelCrossName('Lv.' + str(item['level']) + '-' + item['roleName'], item.get('fromHostName', ''))
                if formula.isBalanceAreanFb(formula.getFubenNo(p.spaceNo)):
                    newName = 'Lv.' + str(item['level']) + '-' + item['roleName']
                obj.SetMember('roleName', GfxValue(gbk2unicode(newName)))
            obj.SetMember('school', GfxValue(item['school']))
            obj.SetMember('campNum', GfxValue(item['campNum']))
            obj.SetMember('killedNum', GfxValue(item['killedNum']))
            obj.SetMember('assistAtkNum', GfxValue(item['assistAtkNum']))
            obj.SetMember('beKilledNum', GfxValue(item['beKilledNum']))
            obj.SetMember('cureNum', GfxValue(item['cureNum']))
            obj.SetMember('damageNum', GfxValue(item['damageNum']))
            obj.SetMember('gbId', GfxValue(str(item.get('gbId', 0))))
            realRoleName = '%s-%s' % (item.get('roleName', ''), item.get('fromHostName', ''))
            obj.SetMember('realRoleName', GfxValue(gbk2unicode(realRoleName)))
            if item.has_key('charTempInfo'):
                templateName = item['charTempInfo'].get('roleName', '')
                obj.SetMember('templateName', GfxValue(gbk2unicode(templateName)))
                obj.SetMember('templateId', GfxValue(item['charTempInfo'].get('tempId', 0)))
            else:
                obj.SetMember('templateName', GfxValue(''))
            ret.SetElement(index, obj)
            index += 1

        return ret

    def getArenaModeDesc(self):
        p = BigWorld.player()
        if p.getArenaMode() in (const.ARENA_MODE_TDM_3V3, const.ARENA_MODE_CROSS_MS_TDM_3V3):
            return 'shiwushadou'
        elif p.getArenaMode() == const.ARENA_MODE_TDM_5V5:
            return 'sanshishadou'
        elif p.getArenaMode() in (const.ARENA_MODE_ROUND_3V3_1,
         const.ARENA_MODE_ROUND_5V5,
         const.ARENA_MODE_ROUND_3V3_2,
         const.ARENA_MODE_CROSS_MS_ROUND_3V3,
         const.ARENA_MODE_CROSS_MS_ROUND_5V5,
         const.ARENA_MODE_CROSS_MS_ROUND_3V3_PRACTISE):
            return 'xuezhanleitai'
        elif p.getArenaMode() == const.ARENA_MODE_SS_ROUND_1V1:
            return 'tongmenzhengba'
        elif p.getArenaMode() in (const.ARENA_MODE_MS_ROUND_1V1, const.ARENA_MODE_CROSS_MS_ROUND_1V1):
            return 'juezhanjianghu'
        else:
            return 'xuezhanleitai'

    def onGetArenaResult(self, *arg):
        p = BigWorld.player()
        arenaInfo = p.arenaInfo
        if formula.isBalanceAreanFb(formula.getFubenNo(p.spaceNo)):
            arenaInfo = p.arenaInfoEx
        ret = self.movie.CreateObject()
        ret.SetMember('widgetId', GfxValue(self.resultWidgetId))
        ret.SetMember('roleName', GfxValue(gbk2unicode(p.realRoleName)))
        ret.SetMember('arenaMode', GfxValue(p.getArenaMode()))
        ret.SetMember('addedScore', GfxValue(p.getAddedScore()))
        ret.SetMember('score', GfxValue(arenaInfo.arenaScore))
        ret.SetMember('data', self._getItemInfo())
        ret.SetMember('arenaFame', GfxValue(p.fame.get(const.JUN_ZI_FAME_ID, 0)))
        ret.SetMember('arenaModeDesc', GfxValue(self.getArenaModeDesc()))
        ret.SetMember('enableQrCode', GfxValue(gameglobal.rds.configData.get('enableQRCode', False)))
        leftTeamName = ''
        rightTeamName = ''
        if self.isSchoolTop:
            leftTeamName = gameStrings.SCHOOL_TOP_ATK
            rightTeamName = gameStrings.SCHOOL_TOP_DEF
        else:
            for item in self.sortedArray:
                if self._genItemFlag(item) == ITEM_FLAG_ENEMY:
                    rightTeamName = item.get('fromHostName', '')
                else:
                    leftTeamName = item.get('fromHostName', '')

        ret.SetMember('leftTeamName', GfxValue(gbk2unicode(leftTeamName)))
        ret.SetMember('rightTeamName', GfxValue(gbk2unicode(rightTeamName)))
        ret.SetMember('winTeamName', GfxValue(gbk2unicode(gameStrings.ARENA_FINAL_RESULT_TITLE)))
        gamelog.debug('dxk@arenaProxy areanaResult', getattr(p, 'arenaResult', -3))
        if self.isSchoolTop:
            ret.SetMember('isWin', GfxValue(p.schoolTopEndInfo[1]['isSchoolTop']))
        elif getattr(p, 'arenaResult', const.LOSE) == const.WIN or getattr(p, 'arenaResult', const.LOSE) == const.WIN_QUIT_EARLY:
            ret.SetMember('isWin', GfxValue(True))
        else:
            ret.SetMember('isWin', GfxValue(False))
        if getattr(p, 'arenaResult', const.LOSE) == const.WIN:
            fbNo = formula.getFubenNo(p.spaceNo)
            arenaMode = formula.fbNo2ArenaMode(fbNo)
            arenaType = AMD.data.get(arenaMode, {}).get('arenaType', 0)
            disturbRatio = utils.getDisturbRatioByType(p, gametypes.DISTURB_TYPE_DUEL)
            isBalanceArena = formula.isBalanceArenaMode(arenaMode)
            if isBalanceArena:
                arenaModeType = const.ARENA_MODE_TYPE_BALANCE
            else:
                arenaModeType = const.ARENA_MODE_TYPE_NORMAL
            zhanxun = int(disturbRatio * utils.getAwardScoreByArenaType(arenaInfo.arenaScore, arenaType, gametypes.DUEL_AWARD_TYPE_ZHAN_XUN, arenaModeType, arenaMode))
            junzi = int(disturbRatio * utils.getAwardScoreByArenaType(arenaInfo.arenaScore, arenaType, gametypes.DUEL_AWARD_TYPE_JUN_ZI, arenaModeType, arenaMode))
            if arenaMode == const.ARENA_MODE_CROSS_MS_ROUND_2V2_DOUBLE_ARENA:
                if getattr(p.doubleArenaTeamInfo, 'relation', 0):
                    dArenaRelationAddRatio = DCD.data.get('dArenaRelationAddRatio', 0.5)
                    junzi += int(junzi * dArenaRelationAddRatio)
                    zhanxun += int(zhanxun * dArenaRelationAddRatio)
        else:
            zhanxun = 0
            junzi = 0
        ret.SetMember('junzi', GfxValue(junzi))
        ret.SetMember('zhanxun', GfxValue(zhanxun))
        if p.isUsingTemp():
            ret.SetMember('usingTempName', GfxValue(gbk2unicode(getattr(p, 'templateName', ''))))
        ret.SetMember('isTeamArena', GfxValue(self.isTeamArena()))
        if self.isTeamArena():
            self.setTeamArenaScore(ret)
        ret.SetMember('isSchoolTop', GfxValue(self.isSchoolTop))
        return ret

    def setTeamArenaScore(self, ret):
        p = BigWorld.player()
        arenaMode = p.getArenaMode()
        if arenaMode == const.ARENA_MODE_CROSS_MS_ROUND_3V3_SCORE:
            scoreInfo = p.arenaScorePlayoffsTeam.get('score', {})
            teamScore = scoreInfo.get('score', 0)
            ret.SetMember('score', GfxValue(teamScore))
        elif arenaMode == const.ARENA_MODE_CROSS_MS_ROUND_2V2_DOUBLE_ARENA:
            statistics = p.doubleArenaTeamInfo.statistics
            teamScore = statistics.score
            ret.SetMember('score', GfxValue(teamScore))

    def isTeamArena(self):
        p = BigWorld.player()
        arenaMode = p.getArenaMode()
        arenaInfo = AMD.data.get(arenaMode, {})
        if arenaInfo.get('team', 0):
            return True
        return False

    def onGetArenaTmpResultInfo(self, *arg):
        ret = self.movie.CreateObject()
        ret.SetMember('data', self._getItemInfo())
        ret.SetMember('arenaIsTimeOut', GfxValue(self.arenaIsTimeOut))
        return ret

    def onArenaTmpResultClick(self, *arg):
        self.showArenaTmpResult()

    def onArenaStatClick(self, *arg):
        self.rankType = arg[3][0].GetString()
        self.sortedArray = self.sortByName(BigWorld.player().arenaStatistics, self.rankType)

    def openArenaMsg(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ARENA_COUNT_DOWN)

    def _createAsArray(self, arg):
        ar = self.movie.CreateArray()
        for index, value in enumerate(arg):
            ar.SetElement(index, GfxValue(value))

        return ar

    def callArenaMsgFunc(self, funcName, arg = None):
        gamelog.debug('@hjx count#callArenaMsgFunc:', funcName, arg)
        if self.arenaCountDownMed:
            if arg != None:
                if len(arg) == 1:
                    self.arenaCountDownMed.Invoke(funcName, GfxValue(arg[0]))
                else:
                    ar = self._createAsArray(arg)
                    self.arenaCountDownMed.Invoke(funcName, ar)
            else:
                self.arenaCountDownMed.Invoke(funcName)

    def closeArenaCountDown(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ARENA_COUNT_DOWN)
        self.arenaCountDownMed = None

    def onGetArenaSortedResult(self, *arg):
        return self._getItemInfo()

    def onExchangeFame(self, *arg):
        p = BigWorld.player()
        p.cell.exchangeArenaFame()

    def onGetExchangeFameFlag(self, *arg):
        return GfxValue(BigWorld.player().arenaInfo.weekExchangeFameFlag)

    def onOpenRank(self, *arg):
        pass

    def setFame(self, fame):
        pass

    def onGetArenaLevelDesc(self, *arg):
        p = BigWorld.player()
        index = formula.getArenaLvTag(self.arenaMode, p.lv)
        maxArenaScores = AMD.data.get(self.arenaMode, {}).get('maxArenaScores', ())
        if index == -1 or index >= len(maxArenaScores):
            return
        desc = GMD.data.get(GMDD.data.ARENA_CURRENT_LEVEL_MAX_SCORE, {}).get('text', '')
        return GfxValue(gbk2unicode(desc % maxArenaScores[index]))

    def onPlayArenaSound(self, *arg):
        mode = arg[3][0].GetString()
        res = int(arg[3][1].GetNumber())
        if mode == 'ArenaResult':
            if res == const.WIN:
                gameglobal.rds.sound.playSound(gameglobal.SD_67)
                gameglobal.rds.sound.playSound(gameglobal.SD_68)
            elif res == const.TIE:
                gameglobal.rds.sound.playSound(gameglobal.SD_71)
                gameglobal.rds.sound.playSound(gameglobal.SD_72)
            elif res == const.LOSE:
                gameglobal.rds.sound.playSound(gameglobal.SD_69)
                gameglobal.rds.sound.playSound(gameglobal.SD_70)
        elif mode == 'ArenaTimer':
            gameglobal.rds.sound.playSound(gameglobal.SD_60)
        elif mode == 'ArenaStart':
            gameglobal.rds.sound.playSound(gameglobal.SD_61)
        elif mode == 'ArenaCount':
            gameglobal.rds.sound.playSound(gameglobal.SD_62)

    def genArenaSortedModeData(self):
        ret = []
        for key, item in AMD.data.items():
            enable = item.get('isEnableUIApply', 0)
            if gameglobal.rds.configData.get('enableCrossServerArena', False):
                enable = enable and key in const.FB_NO_ARENA_CROSS_SERVER_MODES
            else:
                enable = enable and key not in const.FB_NO_ARENA_CROSS_SERVER_MODES
            if enable:
                itemData = {}
                itemData['name'] = item.get('name', gameStrings.TEXT_ARENAPROXY_1034)
                itemData['mode'] = key
                itemData['playerBtn'] = item.get('playerBtn', 0)
                itemData['teamBtn'] = item.get('teamBtn', 0)
                itemData['ord'] = item.get('ord', 999)
                ret.append(itemData)

        ret = sorted(ret, key=lambda d: d['ord'], reverse=False)
        return ret

    def onGetArenaBtnNamesByMode(self, *arg):
        ret = self.genArenaSortedModeData()
        return uiUtils.array2GfxAarry(ret, True)

    def onClickShareBtn(self, *args):
        if self.arenaFinalResultMed:
            widget = ASObject(self.arenaFinalResultMed.Invoke('getWidget'))
            info = gameglobal.rds.ui.qrCodeAppScanShare.createShareInfoInstance(dailyShare=True)
            info.uiRange = uiUtils.getMCTopBottomOnWidget(widget, widget.canvas)
            gameglobal.rds.ui.qrCodeAppScanShare.show(info)

    def getResultWidgetId(self):
        if BigWorld.player().getArenaMode() in const.ARENA_CHALLENDE_MODE_LIST:
            return uiConst.WIDGET_ARENACHALLENGE_RESULT
        elif formula.spaceInWingWorldXinMoArena(BigWorld.player().spaceNo):
            return uiConst.WIDGET_ARENA_FINAL_RESULT_XINMO
        elif BigWorld.player().isUsingTemp() and gameglobal.rds.configData.get('enableBalanceArenaFinalResult', False):
            return uiConst.WIDGET_BALANCE_ARENA_FINAL_RESULT
        else:
            return uiConst.WIDGET_ARENA_FINAL_RESULT

    def refreshPrepInfo(self):
        p = BigWorld.player()
        minePrep = self.prepInfo['minePrep']
        theirPrep = self.prepInfo['theirPrep']
        for nuid, info in p.arenaSidePrepareDict.iteritems():
            if nuid == p.sideNUID:
                minePrep = info
            else:
                theirPrep = info

        self.refreshPrepIcon(minePrep, theirPrep)
        self.refreshPrepBtn(self.needShowPrepBtn())

    def refreshPrepIcon(self, minePrep, theirPrep):
        self.prepInfo['minePrep'] = minePrep
        self.prepInfo['theirPrep'] = theirPrep
        if not self.arenaStatsMed:
            return
        self.arenaStatsMed.Invoke('refreshPrepIcon', uiUtils.dict2GfxDict(self.prepInfo))

    def refreshPrepBtn(self, state):
        if not self.arenaStatsMed:
            return
        self.arenaStatsMed.Invoke('refreshBtn', GfxValue(state))

    def needShowPrepBtn(self):
        if self.prepInfo.get('minePrep'):
            return False
        p = BigWorld.player()
        if p.getArenaMode() not in const.ARENA_CHALLENDE_MODE_LIST:
            return False
        isChallengeSrc = p.arenaChallengeStatus == gametypes.CROSS_ARENA_CHALLENGE_STATUS_APPLY_SUCC
        isChallengeTgt = p.arenaChallengeStatus == gametypes.CROSS_ARENA_CHALLENGE_STATUS_APPLY_BY_SUCC
        return isChallengeSrc or isChallengeTgt

    def onGetPrepBtnShow(self, *args):
        return GfxValue(self.needShowPrepBtn())

    def onHandleClickPrep(self, *args):
        p = BigWorld.player()
        maxNum = int(AMD.data.get(p.getArenaMode(), {}).get('modeName', '1v1')[-1])
        curNum = p.arenaTeam.get(p.gbId, {}).get('sideInMan', (1,))[0]
        prepTime = DCD.data.get('challengeQuickReadyTime', 10)
        if curNum < maxNum:
            msg = uiUtils.getTextFromGMD(GMDD.data.ARENA_CHALLENGE_PREPARE_HINTTEXT1, '%d') % prepTime
        else:
            msg = uiUtils.getTextFromGMD(GMDD.data.ARENA_CHALLENGE_PREPARE_HINTTEXT2, '%d') % prepTime
        callBack = BigWorld.player().cell.arenaChallengePrepareDone
        self.uiAdapter.messageBox.showYesNoMsgBox(msg, yesCallback=callBack, title=gameStrings.PREPARETITLE)

    def onVoteBalanceArenaTemplate(self, *args):
        p = BigWorld.player()
        if p.isUsingTemp():
            gamelog.debug('dxk arena@onVoteBalanceArenaTemplate zanUsingCharTemp', p.charTempId)
            p.base.zanUsingCharTemp(long(p.charTempId))

    def onGetLeftTime(self, *args):
        p = BigWorld.player()
        return GfxValue(max(0, getattr(p, 'schoolTopTimeStamp', 0) - utils.getNow()))
