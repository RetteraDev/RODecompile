#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/battleFieldProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import time
import const
import gameglobal
import uiConst
import gamelog
import formula
import gametypes
import utils
import uiUtils
from callbackHelper import Functor
from uiProxy import DataProxy
from ui import gbk2unicode
from ui import unicode2gbk
from asObject import ASUtils
from guis import ui
from gamestrings import gameStrings
from guis.asObject import ASObject
from data import item_data as ID
from data import school_data as SD
from data import battle_field_data as BFD
from data import battle_field_mode_data as BFMD
from cdata import game_msg_def_data as GMDD
from data import junjie_config_data as JCD
from data import sys_config_data as SCD
from data import guild_tournament_data as GTD
from data import cross_guild_tournament_data as CGTD
from data import duel_config_data as DCD
from cdata import battle_field_shop_item_data as BFSID
from data import battle_field_fort_data as BFFD
DESCEND = True
ASCEND = False
SORT_TYPE_ROLE_NAME = 'roleName'
SORT_TYPE_DAMAGE = 'damage'
SORT_TYPE_CURE = 'cure'
SORT_TYPE_KILL_NUM = 'killNum'
SORT_TYPE_DEATH_NUM = 'deathNum'
SORT_TYPE_ASSIST_NUM = 'assistNum'
SORT_TYPE_KILL_MONSTER_NUM = 'killMonsterNum'
SORT_TYPE_TITLE_NUM = 'titleNum'

class BattleFieldProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(BattleFieldProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerBattleFieldPanel': self.onRegisterBattleFieldPanel,
         'getPanelInfo': self.onGetPanelInfo,
         'getTipsInfo': self.onGetTipsInfo,
         'okClick': self.onOkClick,
         'cancelClick': self.onCancelClick,
         'closeTips': self.onCloseTips,
         'applyClick': self.onApplyClick,
         'applyOfDoubleClick': self.onApplyOfDoubleClick,
         'applyOfTeamClick': self.onApplyOfTeamClick,
         'clickFuncBtn': self.onClickFuncBtn,
         'miniClick': self.onMiniClick,
         'getStatsInfo': self.onGetStatsInfo,
         'getHookScore': self.onGetHookScore,
         'getTotalTime': self.onGetTotalTime,
         'getBFTmpResultInfo': self.onGetBFTmpResultInfo,
         'tmpResultSortClick': self.onTmpResultSortClick,
         'getDurationTime': self.onGetDurationTime,
         'tmpResultCloseClick': self.onTmpResultCloseClick,
         'getBFFinalResultInfo': self.onGetBFFinalResultInfo,
         'finalResultSortClick': self.onFinalResultSortClick,
         'finalResultLeaveClick': self.onFinalResultLeaveClick,
         'showScoreAward': self.onShowScoreAward,
         'useSpecialItem': self.onUseSpecialItem,
         'openRank': self.onOpenRank,
         'getGongXianFen': self.onGetGongXianFen,
         'goHomeClick': self.onGoHomeClick,
         'openShopClick': self.onOpenShopClick,
         'openStatsClick': self.onOpenStatsClick,
         'getFirstKillInfo': self.onGetFirstKillInfo,
         'getKillCnt': self.onGetKillCnt,
         'getTmpResultRes': self.onGetTmpResultRes,
         'addFriendWithTopPlayer': self.onAddFriendWithTopPlayer,
         'getBFButtonList': self.onGetBFButtonList,
         'setCurrentBattleField': self.onSetCurrentBattleField,
         'useBattleFieldItem': self.onUseBattleFieldItem,
         'bfFortInitDone': self.onBfFortInitDone,
         'needScoreAward': self.onNeedScoreAward,
         'reportClick': self.onReportClick,
         'needReportBtn': self.onNeedReportBtn,
         'setAutoUse': self.onSetAutoUse,
         'getAutoUseInfo': self.onGetAutoUseInfo,
         'getBfMemPerforms': self.onGetBfMemPerforms,
         'clickShareBtn': self.onClickShareBtn,
         'enableQRCode': self.onEnableQRCode}
        uiAdapter.registerEscFunc(uiConst.WIDGET_BF_TMP_RESULT, Functor(self.closeBFTmpResultWidget))
        uiAdapter.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_BF_MATCHED, {'click': self.clickPushIcon})
        self.bindType = 'battleField'
        self.resetBattleFieldData()
        self.selFbMode = None
        self.bfShopItems = []
        self.monsterInfo = {}
        self.tmpResultFbNo = 0
        self.reset()

    def reset(self):
        self.tipsTimeStamp = 0
        self.tipsTimeOutCB = None
        self.stage = uiConst.BF_PANEL_STAGE_INIT
        self.isJumpQueue = False
        self.killer = 0
        self.killee = 0
        self.killCnt = 0
        self.bfTipMed = None
        self.bfPanelMc = None
        self.bfStatsMed = None
        self.bfFlagStatsMed = None
        self.monsterTimerMed = None
        self.bfFirstKillMed = None
        self.bfAssistMed = None
        self.bfKillMed = None
        self.bfTopMsg = None
        self.selFbMode = None
        self.bfFortMed = None
        self.enterFortId = None
        self.bfShopItems = []
        self.autoUseArr = []
        self.consume = 0
        self.resetTmpResult()
        self.resetFinalResult()

    def resetBattleFieldData(self):
        self.fame = 0

    def resetTmpResult(self):
        self.tmpResSortedKey = SORT_TYPE_ROLE_NAME
        self.tmpResSortedType = ASCEND
        self.tmpSortedArray = []
        self.isBFTmpResultShow = False
        self.bfTmpResultMed = None
        self.tmpResultFbNo = 0

    def resetFinalResult(self):
        self.finalResSortedKey = SORT_TYPE_ROLE_NAME
        self.finalResSortedType = ASCEND
        self.finalSortedArray = []
        self.bfFinalResultMed = None

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.bfTipMed = None
        self.bfPanelMc = None
        self.bfStatsMed = None
        self.bfFinalResultMed = None
        self.bfAssistMed = None
        self.bfKillMed = None
        self.bfTopMsg = None
        self.bfFortMed = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_BATTLE_FIELD_TIPS)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_BF_STATS)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_BFFLAG_STATS)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_BF_TMP_RESULT)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_BF_FINAL_RESULT)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_BF_FIRST_KILL)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_BF_ASSIST)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_BF_KILL)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_BF_MSG)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_BATTLE_FIELD_FORT_INFO)
        gameglobal.rds.ui.battleOfFortProgressBar.hide()
        gameglobal.rds.ui.battleCQZZProgressBar.hide()
        gameglobal.rds.ui.battleRaceCountDown.hide()
        if gameglobal.rds.configData.get('enableGuildTournamentLiveAndInspire', False):
            gameglobal.rds.ui.bFFortInfoV1.clearWidget()
            gameglobal.rds.ui.bFFlagStatsV1.clearWidget()
            gameglobal.rds.ui.bFGuildTournamentObserve.clearWidget()

    def _asWidgetClose(self, widgetId, multiID):
        self.clearWidget()

    def onRegisterBattleFieldPanel(self, *arg):
        self.bfPanelMc = arg[3][0]

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_BATTLE_FIELD_TIPS:
            self.bfTipMed = mediator
        else:
            if widgetId == uiConst.WIDGET_BF_STATS:
                self.bfStatsMed = mediator
                menuData = [{'lable': gameStrings.TEXT_BATTLEFIELDPROXY_197,
                  'index': -1}]
                initData = {}
                return uiUtils.dict2GfxDict(initData, True)
            if widgetId == uiConst.WIDGET_BFFLAG_STATS:
                self.bfFlagStatsMed = mediator
            elif widgetId == uiConst.WIDGET_BF_FINAL_RESULT:
                self.bfFinalResultMed = mediator
            elif widgetId == uiConst.WIDGET_BF_FIRST_KILL:
                self.bfFirstKillMed = mediator
            elif widgetId == uiConst.WIDGET_BF_ASSIST:
                self.bfAssistMed = mediator
            elif widgetId == uiConst.WIDGET_BF_KILL:
                self.bfKillMed = mediator
            elif widgetId == uiConst.WIDGET_MONSTER_TIMER:
                self.monsterTimerMed = mediator
            elif widgetId == uiConst.WIDGET_BF_TMP_RESULT:
                self.bfTmpResultMed = mediator
            elif widgetId == uiConst.WIDGET_BF_MSG:
                self.bfTopMsg = mediator
            elif widgetId == uiConst.WIDGET_BATTLE_FIELD_FORT_INFO:
                self.bfFortMed = mediator
                self.refreshAllBulletInfo()

    def showTips(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_BATTLE_FIELD_TIPS, False)
        if gameglobal.rds.ui.isHideAllUI():
            gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_BATTLE_FIELD_TIPS, True)

    def closeTips(self):
        if self.bfTipMed:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_BATTLE_FIELD_TIPS)
        self.bfTipMed = None
        self.whichCancel = self.whichConfirm = uiConst.BF_ENTER_TIP
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_BF_MATCHED)

    def onCloseTips(self, *arg):
        self.closeTips()

    def onGetTipsInfo(self, *arg):
        p = BigWorld.player()
        enterTime = BFD.data.get(p.getBattleFieldFbNo(), {}).get('enterTime', 45)
        ret = self.movie.CreateObject()
        ret.SetMember('type', GfxValue(self.tipsType))
        ret.SetMember('timerMaxValue', GfxValue(enterTime))
        ret.SetMember('timerCurValue', GfxValue(int(enterTime - (p.getServerTime() - self.tipsTimeStamp))))
        return ret

    def onGetBFButtonList(self, *arg):
        p = BigWorld.player()
        ret = []
        sel = False
        for key, val in BFMD.data.items():
            isEnableFlagBf = gameglobal.rds.configData.get('enableFlagBf', False)
            if key == const.BATTLE_FIELD_MODE_FLAG and not isEnableFlagBf:
                continue
            if gameglobal.rds.configData.get('enableDuelTimeCheck', True) and not self.isNeedShow(key):
                continue
            isCrossBF = gameglobal.rds.configData.get('enableCrossServerBF', False)
            namePrefix = gameStrings.TEXT_BATTLEFIELDPROXY_256 if isCrossBF else ''
            obj = {}
            obj['id'] = key
            obj['name'] = namePrefix + val.get('name', '')
            obj['desc'] = val.get('desc', '')
            obj['winStandard'] = val.get('winStandard', '')
            obj['visible'] = 1
            if p.battleFieldFbNo in val.get('fbs', []):
                obj['selected'] = True
                sel = True
            ret.append(obj)

        if len(ret) > 0 and not sel:
            ret[0]['selected'] = True
        return uiUtils.array2GfxAarry(ret, True)

    def isNeedShow(self, mode):
        p = BigWorld.player()
        isOpen = False
        openStartTimes = BFMD.data.get(mode, {}).get('openStartTimes', ())
        openEndTimes = BFMD.data.get(mode, {}).get('openEndTimes', ())
        if hasattr(p, 'getServerTime'):
            current = p.getServerTime()
        else:
            current = time.time()
        if len(openStartTimes) == 0:
            isOpen = True
        else:
            for index in xrange(len(openStartTimes)):
                if utils.inTimeTupleRange(openStartTimes[index], openEndTimes[index], current):
                    isOpen = True
                    break

        return isOpen

    def onSetCurrentBattleField(self, *arg):
        bfId = int(arg[3][0].GetNumber())
        self.selFbMode = bfId

    def refreshBattleFieldTip(self, tipsType, confrimTimeOut = False):
        self.tipsType = tipsType
        confrimTimeOut and self.setBattleFieldTipsTimeOut()
        if self.bfTipMed:
            self.bfTipMed.Invoke('refreshPanel')
        else:
            self.showTips()

    def setBattleFieldTipsTimeOut(self):
        p = BigWorld.player()
        self.cancelBattleFieldTipsTimeOut()
        enterTime = BFD.data.get(p.getBattleFieldFbNo(), {}).get('enterTime', 45)
        self.tipsTimeOutCB = BigWorld.callback(enterTime - (p.getServerTime() - self.tipsTimeStamp) - 1, self.confirmTimeOut)

    def cancelBattleFieldTipsTimeOut(self):
        self.tipsTimeOutCB and BigWorld.cancelCallback(self.tipsTimeOutCB)
        self.tipsTimeOutCB = None

    def clickPushIcon(self):
        gamelog.debug('@hjx bf#clickPushIcon:', self.isJumpQueue)
        if self.isJumpQueue:
            self.refreshBattleFieldTip(uiConst.BF_JUMP_QUEUE_TIP)
        else:
            self.refreshBattleFieldTip(uiConst.BF_ENTER_TIP)

    def onOkClick(self, *arg):
        self.whichConfirm = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        if p.isArenaMatching():
            bfd = BFD.data.get(p.getBattleFieldFbNo(), {})
            p.confirmCancelApplyArena(bfd.get('name', ''), self.onRealConfirmEnter)
        elif uiUtils.inNeedNotifyStates():
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_BATTLEFIELDPROXY_328, self.onRealConfirmEnter)
        else:
            self.onRealConfirmEnter()

    def onRealConfirmEnter(self):
        p = BigWorld.player()
        self.cancelBattleFieldTipsTimeOut()
        if self.whichConfirm == uiConst.BF_ENTER_TIP:
            battleFieldNo = p.getBattleFieldFbNo()
            if battleFieldNo:
                if p.isPUBGFbNo(battleFieldNo):
                    p.cell.confirmEnterPUBG(battleFieldNo)
                else:
                    p.cell.confirmEnterBattleField(p.getBattleFieldFbNo())
        elif self.whichConfirm == uiConst.BF_REMATCH_TIP:
            self.closeTips()
        elif self.whichConfirm == uiConst.BF_JUMP_QUEUE_TIP:
            p.confirmJumpQueue()

    def onCancelClick(self, *arg):
        self.whichCancel = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        self.cancelBattleFieldTipsTimeOut()
        if self.whichCancel == uiConst.BF_ENTER_TIP:
            if p.getBattleFieldFbNo():
                p.cell.confirmEnterBattleFieldFailed(p.getBattleFieldFbNo())
        elif self.whichCancel == uiConst.BF_JUMP_QUEUE_TIP:
            p.cancelJumpQueue()
        self.closeTips()

    def confirmTimeOut(self):
        p = BigWorld.player()
        if self.tipsType == uiConst.BF_ENTER_TIP:
            if p.getBattleFieldFbNo():
                confirmTimeOutInGame = BFD.data.get(p.getBattleFieldFbNo(), {}).get('confirmTimeOutInGame', 0)
                if confirmTimeOutInGame:
                    self.whichConfirm = uiConst.BF_ENTER_TIP
                    self.onRealConfirmEnter()
                else:
                    p.cell.confirmEnterBattleFieldFailed(p.getBattleFieldFbNo())
        elif self.tipsType == uiConst.BF_JUMP_QUEUE_TIP:
            p.cancelJumpQueue()
        self.closeTips()

    def onMiniClick(self, *arg):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_BATTLE_FIELD_TIPS)
        self.bfTipMed = None

    def _getContent(self):
        item = BFMD.data.get(self.selFbMode, {})
        ar = self.movie.CreateArray()
        ar.SetElement(0, GfxValue(gbk2unicode(item.get('name', ''))))
        ar.SetElement(1, GfxValue(gbk2unicode(item.get('desc', ''))))
        ar.SetElement(2, GfxValue(gbk2unicode(item.get('winStandard', ''))))
        return ar

    def setFame(self, value):
        self.fame = value

    def onGetPanelInfo(self, *arg):
        ret = self.movie.CreateObject()
        ret.SetMember('stage', GfxValue(self.stage))
        ret.SetMember('content', self._getContent())
        ret.SetMember('count', GfxValue(0))
        ret.SetMember('score', GfxValue(self.fame))
        ret.SetMember('fame', GfxValue(0))
        ret.SetMember('arenaCount', GfxValue(0))
        ret.SetMember('arenaWinCount', GfxValue(0))
        ret.SetMember('arenaWinRate', GfxValue(0))
        ret.SetMember('arenaKilledCount', GfxValue(0))
        return ret

    def onApplyClick(self, *arg):
        stage = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        if stage == uiConst.BF_PANEL_STAGE_INIT:
            p.applyBattleFieldOfPerson()

    def onApplyOfDoubleClick(self, *arg):
        stage = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        if stage == uiConst.BF_PANEL_STAGE_INIT:
            p.applyBattleFieldOfTeam(gametypes.BATTLE_FIELD_APPLY_GROUP_OF_DOUBLE)

    def onApplyOfTeamClick(self, *arg):
        stage = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        if stage == uiConst.BF_PANEL_STAGE_INIT:
            p.applyBattleFieldOfTeam(gametypes.BATTLE_FIELD_APPLY_GROUP_OF_TEAM)

    def onClickFuncBtn(self, *arg):
        stage = int(arg[3][0].GetNumber())
        gamelog.debug('@hjx bf#onQuitClick:', stage)
        p = BigWorld.player()
        if stage == uiConst.BF_PANEL_STAGE_INIT:
            p.applyBattleFieldOfTeam(gametypes.BATTLE_FIELD_APPLY_GROUP_OF_GROUP)
        elif stage == uiConst.BF_PANEL_STAGE_APPLYED:
            p.cancelApplyBattleField()
        elif stage == uiConst.BF_PANEL_STAGE_IN_GAME:
            p.cell.quitBattleField()

    def refreshBFPanel(self, stage):
        p = BigWorld.player()
        if p.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            self.stage = uiConst.BF_PANEL_STAGE_IN_GAME
        self.stage = stage
        if self.bfPanelMc:
            self.bfPanelMc.Invoke('refreshPanel')

    def _genStatsTestData(self):
        p = BigWorld.player()
        p.bfSideIndex = 1
        self.monsterInfo = {40301: {'entityId': 9844,
                 'campId': 3,
                 'hp': 1269688,
                 'mhp': 1269688},
         40302: {'entityId': 9842,
                 'campId': 3,
                 'hp': 493600,
                 'mhp': 493600},
         40303: {'entityId': 9841,
                 'campId': 3,
                 'hp': 493600,
                 'mhp': 493600},
         40304: {'entityId': 9843,
                 'campId': 3,
                 'hp': 493600,
                 'mhp': 493600},
         40305: {'entityId': 9840,
                 'campId': 4,
                 'hp': 1269688,
                 'mhp': 1269688},
         40306: {'entityId': 9839,
                 'campId': 4,
                 'hp': 493600,
                 'mhp': 493600},
         40307: {'entityId': 9838,
                 'campId': 4,
                 'hp': 493600,
                 'mhp': 493600},
         40308: {'entityId': 9837,
                 'campId': 4,
                 'hp': 679958,
                 'mhp': 690160}}
        self.setHpInfo(self.monsterInfo)

    def _setHp(self, charType, hp):
        self.monsterInfo[charType]['hp'] = hp
        self.setHpInfo(self.monsterInfo)

    def onGetStatsInfo(self, *arg):
        obj = self.movie.CreateObject()
        p = BigWorld.player()
        enemyMaxRes = myMaxRes = BFD.data.get(p.getBattleFieldFbNo(), {}).get('winResLimit', 100)
        obj.SetMember('myMaxRes', GfxValue(myMaxRes))
        obj.SetMember('myCurName', GfxValue(gbk2unicode(gameStrings.SELF_SIDE)))
        obj.SetMember('enemyName', GfxValue(gbk2unicode(gameStrings.ENERMY_SIDE)))
        obj.SetMember('myCurRes', GfxValue(p.getMyRes()))
        obj.SetMember('enemyMaxRes', GfxValue(enemyMaxRes))
        obj.SetMember('enemyCurRes', GfxValue(p.getEnemyRes()))
        obj.SetMember('isResBattleField', GfxValue(p.inFubenType(const.FB_TYPE_BATTLE_FIELD_RES)))
        obj.SetMember('isHookBattleField', GfxValue(p.inFubenType(const.FB_TYPE_BATTLE_FIELD_HOOK)))
        return obj

    def onGetHookScore(self, *args):
        return GfxValue(BigWorld.player().bfHookScore)

    def refreshBFStats(self):
        p = BigWorld.player()
        if p.inFubenType(const.FB_TYPE_BATTLE_FIELD_RES) or p.inFubenType(const.FB_TYPE_BATTLE_FIELD_HOOK):
            if self.bfStatsMed:
                self.bfStatsMed.Invoke('refreshStatsInfo')
            else:
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_BF_STATS)
        elif p.inFubenType(const.FB_TYPE_BATTLE_FIELD_FLAG):
            if gameglobal.rds.configData.get('enableGuildTournamentLiveAndInspire', False):
                if gameglobal.rds.ui.bFFlagStatsV1.widget:
                    gameglobal.rds.ui.bFFlagStatsV1.refreshStatsInfo()
                else:
                    gameglobal.rds.ui.loadWidget(uiConst.WIDGET_BF_FLAG_STATS_V1)
            elif self.bfFlagStatsMed:
                self.bfFlagStatsMed.Invoke('refreshStatsInfo')
            else:
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_BFFLAG_STATS)
        elif p.inFubenType(const.FB_TYPE_BATTLE_FIELD_FORT):
            if gameglobal.rds.configData.get('enableGuildTournamentLiveAndInspire', False):
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_BF_FORT_INFO_V1)
            elif not self.bfFortMed:
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_BATTLE_FIELD_FORT_INFO)
        elif p.inFubenType(const.FB_TYPE_BATTLE_FIELD_NEW_FLAG):
            if gameglobal.rds.configData.get('enableNewFlagBF', False):
                gameglobal.rds.ui.battleOfFortProgressBar.show()
        elif p.inFubenType(const.FB_TYPE_BATTLE_FIELD_CQZZ):
            if gameglobal.rds.configData.get('enableCqzzBf', False):
                gameglobal.rds.ui.battleCQZZProgressBar.show()
        elif p.inFubenType(const.FB_TYPE_BATTLE_FIELD_RACE):
            if gameglobal.rds.configData.get('enableRaceBattleField', False):
                gameglobal.rds.ui.battleRaceCountDown.show()

    def refreshHookScore(self):
        if self.bfStatsMed:
            self.bfStatsMed.Invoke('refreshScore')

    def isNeedRefresh(self, monsterInfo):
        if len(monsterInfo) != len(self.monsterInfo):
            return True
        for fbEntityNo, val in monsterInfo.iteritems():
            if not self.monsterInfo.has_key(fbEntityNo):
                return True
            bVal = self.monsterInfo[fbEntityNo]
            hp = val.get('hp', 0)
            bHp = bVal.get('hp', 0)
            if hp != 0 and hp != bHp:
                return True
            mhp = val.get('mhp', 0)
            bMhp = bVal.get('mhp', 0)
            if mhp != 0 and mhp != bMhp:
                return True

        return False

    def getHpInfoFromMonsterInfo(self, monsterInfo):
        p = BigWorld.player()
        if not hasattr(p, 'bfSideIndex'):
            return []
        ret = []
        index = 0
        bfdata = BFD.data.get(p.getBattleFieldFbNo(), {})
        myMonsterOrder = bfdata.get('monsterOrder', {}).get(str(p.bfSideIndex + 1), [])
        myMonsterIdOrder = []
        for monsFbEntNo in myMonsterOrder:
            isSucc = False
            for val in monsterInfo.values():
                if val.get('fbEntityNo', -1) == monsFbEntNo:
                    myMonsterIdOrder.append(val.get('entityId', 0))
                    isSucc = True
                    break

            if not isSucc:
                myMonsterIdOrder.append(0)

        for entityId in myMonsterIdOrder:
            info = {}
            info['hp'] = monsterInfo.get(entityId, {}).get('hp', 0)
            info['mhp'] = monsterInfo.get(entityId, {}).get('mhp', 1)
            info['myIndex'] = index
            fbEntityNo = monsterInfo.get(entityId, {}).get('fbEntityNo', 0)
            info['icon'] = 'battleFieldMonsterName/' + str(fbEntityNo) + '.dds'
            ret.append(info)
            index += 1

        enemyMonsterOrder = bfdata.get('monsterOrder', {}).get(str(2 - p.bfSideIndex), [])
        enemyMonsterIdOrder = []
        for monsFbEntNo in enemyMonsterOrder:
            isSucc = False
            for val in monsterInfo.values():
                if val.get('fbEntityNo', -1) == monsFbEntNo:
                    enemyMonsterIdOrder.append(val.get('entityId', 0))
                    isSucc = True
                    break

            if not isSucc:
                enemyMonsterIdOrder.append(0)

        for entityId in enemyMonsterIdOrder:
            info = {}
            info['hp'] = monsterInfo.get(entityId, {}).get('hp', 0)
            info['mhp'] = monsterInfo.get(entityId, {}).get('mhp', 1)
            info['myIndex'] = index - 4
            fbEntityNo = monsterInfo.get(entityId, {}).get('fbEntityNo', 0)
            info['icon'] = 'battleFieldMonsterName/' + str(fbEntityNo) + '.dds'
            ret.append(info)
            index += 1

        return ret

    def setHpInfo(self, monsterInfo):
        p = BigWorld.player()
        if not p.inFubenType(const.FB_TYPE_BATTLE_FIELD_RES) and not p.inFubenType(const.FB_TYPE_BATTLE_FIELD_FORT):
            return
        elif not self.isNeedRefresh(monsterInfo):
            return
        elif not hasattr(p, 'bfSideIndex'):
            return
        elif self.bfStatsMed is None and self.bfFortMed is None and gameglobal.rds.ui.bFFortInfoV1.widget is None:
            return
        else:
            self.monsterInfo = monsterInfo
            ret = self.getHpInfoFromMonsterInfo(monsterInfo)
            if self.bfStatsMed:
                self.bfStatsMed.Invoke('setHpInfo', uiUtils.array2GfxAarry(ret, True))
            if gameglobal.rds.configData.get('enableGuildTournamentLiveAndInspire', False):
                if gameglobal.rds.ui.bFFortInfoV1.widget:
                    gameglobal.rds.ui.bFFortInfoV1.setHpInfo(ret)
            elif self.bfFortMed:
                self.bfFortMed.Invoke('setHpInfo', uiUtils.array2GfxAarry(ret, True))
            return

    def closeBFWidget(self):
        self.hide()
        gameglobal.rds.ui.teamComm.closeTeamPlayer()

    def onTmpResultSortClick(self, *arg):
        self.tmpResSortedKey = arg[3][0].GetString()
        self.tmpResSortedType = int(arg[3][1].GetNumber())
        gamelog.debug('@hjx bf result#onTmpResultSortClick:', self.tmpResSortedKey, self.tmpResSortedType)

    def onGetDurationTime(self, *arg):
        p = BigWorld.player()
        if not p.bfTimeRec.has_key('tReady'):
            return
        totalTime = BFD.data.get(p.getBattleFieldFbNo(), {}).get('durationTime', 1800)
        countTime = totalTime - int(p.getServerTime() - p.bfTimeRec['tReady'])
        return GfxValue(countTime)

    def onGetTotalTime(self, *arg):
        p = BigWorld.player()
        totalTime = BFD.data.get(p.getBattleFieldFbNo(), {}).get('durationTime', 1800)
        return GfxValue(totalTime)

    def startCounting(self):
        p = BigWorld.player()
        if p.inFubenType(const.FB_TYPE_BATTLE_FIELD_RES) or p.inFubenType(const.FB_TYPE_BATTLE_FIELD_HOOK):
            if self.bfStatsMed:
                self.bfStatsMed.Invoke('startTimer')
        elif p.inFubenType(const.FB_TYPE_BATTLE_FIELD_FLAG):
            if gameglobal.rds.configData.get('enableGuildTournamentLiveAndInspire', False):
                if gameglobal.rds.ui.bFFlagStatsV1.widget:
                    gameglobal.rds.ui.bFFlagStatsV1.startTimer()
            elif self.bfFlagStatsMed:
                self.bfFlagStatsMed.Invoke('startTimer')
        elif p.inFubenType(const.FB_TYPE_BATTLE_FIELD_FORT):
            if gameglobal.rds.configData.get('enableGuildTournamentLiveAndInspire', False):
                if gameglobal.rds.ui.bFFortInfoV1.widget:
                    gameglobal.rds.ui.bFFortInfoV1.startTimer()
            elif self.bfFortMed:
                self.bfFortMed.Invoke('startTimer')

    def sortByName(self, ar, attrName, myReverse = True):
        return sorted(ar, cmp=lambda x, y: cmp(x.get(attrName, 0), y.get(attrName, 0)), reverse=myReverse)

    def _genTestData(self):
        p = BigWorld.player()
        p.firstBloodKiller = p.gbId
        delattr(p, 'bfSideStats')
        p.bfMemStats = [{'gbId': p.gbId,
          'roleName': 'A',
          'isFriend': True,
          'isMyself': True,
          'level': 60,
          'school': 4,
          'damage': 12,
          'cure': 33,
          'reliveTime': 40,
          'killNum': 34,
          'deathNum': 2,
          'assistNum': 890,
          'killMonsterNum': 1,
          'isOn': True,
          'isDead': False,
          'isConfirmRelive': False},
         {'gbId': 1,
          'roleName': 'B',
          'isFriend': True,
          'isMyself': False,
          'level': 60,
          'school': 5,
          'damage': 16,
          'cure': 78,
          'reliveTime': 30,
          'killNum': 56,
          'deathNum': 5,
          'assistNum': 123,
          'killMonsterNum': 0,
          'isOn': True,
          'isDead': True,
          'isConfirmRelive': True},
         {'gbId': 1,
          'roleName': 'C',
          'isFriend': False,
          'isMyself': False,
          'level': 60,
          'school': 6,
          'damage': 19,
          'cure': 19,
          'reliveTime': 50,
          'killNum': 16,
          'deathNum': 1,
          'assistNum': 1230,
          'killMonsterNum': 2,
          'isOn': True,
          'isDead': True,
          'isConfirmRelive': True},
         {'gbId': 1,
          'roleName': 'D',
          'isFriend': False,
          'isMyself': False,
          'level': 60,
          'school': 7,
          'damage': 88,
          'cure': 552,
          'reliveTime': 20,
          'killNum': 78,
          'deathNum': 3,
          'assistNum': 789,
          'killMonsterNum': 0,
          'isOn': True,
          'isDead': True,
          'isConfirmRelive': True},
         {'gbId': 1,
          'roleName': 'E',
          'isFriend': False,
          'isMyself': False,
          'level': 60,
          'school': 7,
          'damage': 45,
          'cure': 789,
          'reliveTime': 20,
          'killNum': 3,
          'deathNum': 1,
          'assistNum': 12,
          'killMonsterNum': 0,
          'isOn': True,
          'isDead': True,
          'isConfirmRelive': True},
         {'gbId': 1,
          'roleName': 'F',
          'isFriend': True,
          'isMyself': False,
          'level': 60,
          'school': 7,
          'damage': 45,
          'cure': 444,
          'reliveTime': 20,
          'killNum': 1,
          'deathNum': 1,
          'assistNum': 12,
          'killMonsterNum': 0,
          'isOn': True,
          'isDead': True,
          'isConfirmRelive': True},
         {'gbId': 1,
          'roleName': 'G',
          'isFriend': False,
          'isMyself': False,
          'level': 60,
          'school': 7,
          'damage': 7489,
          'cure': 45,
          'reliveTime': 20,
          'killNum': 6,
          'deathNum': 1,
          'assistNum': 12,
          'killMonsterNum': 78,
          'isOn': True,
          'isDead': True,
          'isConfirmRelive': True},
         {'gbId': 3,
          'roleName': 'A',
          'isFriend': True,
          'isMyself': True,
          'level': 60,
          'school': 4,
          'damage': 12,
          'cure': 33,
          'reliveTime': 40,
          'killNum': 34,
          'deathNum': 2,
          'assistNum': 890,
          'killMonsterNum': 1,
          'isOn': True,
          'isDead': False,
          'isConfirmRelive': False},
         {'gbId': 1,
          'roleName': 'B',
          'isFriend': True,
          'isMyself': False,
          'level': 60,
          'school': 5,
          'damage': 16,
          'cure': 78,
          'reliveTime': 30,
          'killNum': 56,
          'deathNum': 5,
          'assistNum': 123,
          'killMonsterNum': 0,
          'isOn': True,
          'isDead': True,
          'isConfirmRelive': True},
         {'gbId': 1,
          'roleName': 'C',
          'isFriend': False,
          'isMyself': False,
          'level': 60,
          'school': 6,
          'damage': 19,
          'cure': 19,
          'reliveTime': 50,
          'killNum': 16,
          'deathNum': 1,
          'assistNum': 1230,
          'killMonsterNum': 2,
          'isOn': True,
          'isDead': True,
          'isConfirmRelive': True},
         {'gbId': 1,
          'roleName': 'D',
          'isFriend': False,
          'isMyself': False,
          'level': 60,
          'school': 7,
          'damage': 88,
          'cure': 552,
          'reliveTime': 20,
          'killNum': 78,
          'deathNum': 3,
          'assistNum': 789,
          'killMonsterNum': 0,
          'isOn': True,
          'isDead': True,
          'isConfirmRelive': True},
         {'gbId': 1,
          'roleName': 'E',
          'isFriend': False,
          'isMyself': False,
          'level': 60,
          'school': 7,
          'damage': 45,
          'cure': 789,
          'reliveTime': 20,
          'killNum': 3,
          'deathNum': 1,
          'assistNum': 12,
          'killMonsterNum': 0,
          'isOn': True,
          'isDead': True,
          'isConfirmRelive': True},
         {'gbId': 1,
          'roleName': 'F',
          'isFriend': True,
          'isMyself': False,
          'level': 60,
          'school': 7,
          'damage': 45,
          'cure': 444,
          'reliveTime': 20,
          'killNum': 1,
          'deathNum': 1,
          'assistNum': 12,
          'killMonsterNum': 0,
          'isOn': True,
          'isDead': True,
          'isConfirmRelive': True},
         {'gbId': 1,
          'roleName': 'G',
          'isFriend': False,
          'isMyself': False,
          'level': 60,
          'school': 7,
          'damage': 7489,
          'cure': 45,
          'reliveTime': 20,
          'killNum': 6,
          'deathNum': 1,
          'assistNum': 12,
          'killMonsterNum': 78,
          'isOn': True,
          'isDead': True,
          'isConfirmRelive': True},
         {'gbId': 3,
          'roleName': 'A',
          'isFriend': True,
          'isMyself': True,
          'level': 60,
          'school': 4,
          'damage': 12,
          'cure': 33,
          'reliveTime': 40,
          'killNum': 34,
          'deathNum': 2,
          'assistNum': 890,
          'killMonsterNum': 1,
          'isOn': True,
          'isDead': False,
          'isConfirmRelive': False},
         {'gbId': 1,
          'roleName': 'B',
          'isFriend': True,
          'isMyself': False,
          'level': 60,
          'school': 5,
          'damage': 16,
          'cure': 78,
          'reliveTime': 30,
          'killNum': 56,
          'deathNum': 5,
          'assistNum': 123,
          'killMonsterNum': 0,
          'isOn': True,
          'isDead': True,
          'isConfirmRelive': True},
         {'gbId': 1,
          'roleName': 'C',
          'isFriend': False,
          'isMyself': False,
          'level': 60,
          'school': 6,
          'damage': 19,
          'cure': 19,
          'reliveTime': 50,
          'killNum': 16,
          'deathNum': 1,
          'assistNum': 1230,
          'killMonsterNum': 2,
          'isOn': True,
          'isDead': True,
          'isConfirmRelive': True},
         {'gbId': 1,
          'roleName': 'D',
          'isFriend': False,
          'isMyself': False,
          'level': 60,
          'school': 7,
          'damage': 88,
          'cure': 552,
          'reliveTime': 20,
          'killNum': 78,
          'deathNum': 3,
          'assistNum': 789,
          'killMonsterNum': 0,
          'isOn': True,
          'isDead': True,
          'isConfirmRelive': True},
         {'gbId': 1,
          'roleName': 'E',
          'isFriend': False,
          'isMyself': False,
          'level': 60,
          'school': 7,
          'damage': 45,
          'cure': 789,
          'reliveTime': 20,
          'killNum': 3,
          'deathNum': 1,
          'assistNum': 12,
          'killMonsterNum': 0,
          'isOn': True,
          'isDead': True,
          'isConfirmRelive': True},
         {'gbId': 1,
          'roleName': 'F',
          'isFriend': True,
          'isMyself': False,
          'level': 60,
          'school': 7,
          'damage': 45,
          'cure': 444,
          'reliveTime': 20,
          'killNum': 1,
          'deathNum': 1,
          'assistNum': 12,
          'killMonsterNum': 0,
          'isOn': True,
          'isDead': True,
          'isConfirmRelive': True},
         {'gbId': 1,
          'roleName': 'G',
          'isFriend': False,
          'isMyself': False,
          'level': 60,
          'school': 7,
          'damage': 7489,
          'cure': 45,
          'reliveTime': 20,
          'killNum': 6,
          'deathNum': 1,
          'assistNum': 12,
          'killMonsterNum': 78,
          'isOn': True,
          'isDead': True,
          'isConfirmRelive': True}]
        p._genTitleDesc()

    def getSelfBFSideNUID(self):
        p = BigWorld.player()
        selfBFSideNUID = p.bfSideNUID
        if self.tmpResultFbNo:
            for item in self.tmpSortedArray:
                guildNUID = item.get('sideNUID', 0) >> 1
                if guildNUID == p.guildNUID:
                    selfBFSideNUID = item.get('sideNUID', 0)
                    break

        return selfBFSideNUID

    def onGetBFTmpResultInfo(self, *arg):
        p = BigWorld.player()
        ret = self.movie.CreateObject()
        retArray = self.movie.CreateArray()
        self.tmpSortedArray = self.sortByName(p.bfMemPerforms, self.tmpResSortedKey, myReverse=self.tmpResSortedType)
        index = 0
        if not self.tmpResultFbNo:
            fbNo = formula.getFubenNo(p.spaceNo)
        else:
            fbNo = self.tmpResultFbNo
        menuNames = uiConst.BATTLE_FIELD_RESULT_MENU_NAME[formula.whatFubenType(fbNo)]
        ret.SetMember('bfSpecialScore0', GfxValue(gbk2unicode(menuNames[0])))
        ret.SetMember('bfSpecialScore1', GfxValue(gbk2unicode(menuNames[1])))
        selfBFSideNUID = self.getSelfBFSideNUID()
        for item in self.tmpSortedArray:
            memItem = p.getMemInfoByGbId(item['gbId'])
            if not memItem and not self.tmpResultFbNo:
                continue
            if not p._checkValidSchool(memItem.get('school', const.SCHOOL_YUXU)):
                continue
            lv = memItem.get('level', 0) if not self.tmpResultFbNo else item.get('lv', 0)
            school = memItem.get('school', 0) if not self.tmpResultFbNo else item.get('school', 0)
            roleName = memItem.get('roleName', 0) if not self.tmpResultFbNo else item.get('roleName', 0)
            sideNUID = memItem.get('sideNUID', 0) if not self.tmpResultFbNo else item.get('sideNUID', 0)
            obj = self.movie.CreateObject()
            obj.SetMember('isMyself', GfxValue(item['gbId'] == p.gbId))
            obj.SetMember('isFriend', GfxValue(sideNUID == selfBFSideNUID))
            obj.SetMember('isDead', GfxValue(memItem.get('life', gametypes.LIFE_ALIVE) == gametypes.LIFE_DEAD))
            reliveTime = 0
            if memItem.get('isConfirmRelive', 0):
                reliveTime = uiUtils.getBFReliveTime(memItem)
            obj.SetMember('reliveTime', GfxValue(reliveTime))
            if memItem.get('life', 0) == gametypes.LIFE_DEAD:
                gamelog.debug('@hjx bf result#reliveTime0:', reliveTime)
            obj.SetMember('isConfirmRelive', GfxValue(memItem.get('isConfirmRelive', False)))
            obj.SetMember('isPresent', GfxValue(memItem.get('isOn', True)))
            obj.SetMember('school', GfxValue(gbk2unicode(SD.data[school]['name'])))
            obj.SetMember('schoolLabel', GfxValue(gbk2unicode(uiConst.SCHOOL_FRAME_DESC.get(school, ''))))
            newName = uiUtils.genDuelCrossName('Lv.' + str(lv) + '-' + roleName, memItem.get('fromHostName', ''))
            obj.SetMember('roleName', GfxValue(gbk2unicode(newName)))
            obj.SetMember(const.BF_COMMON_DAMAGE, GfxValue(gbk2unicode(self._getFixSizeNum(item.get(const.BF_COMMON_DAMAGE, 0)))))
            obj.SetMember(const.BF_COMMON_DAMAGE + 'Tip', GfxValue(gbk2unicode(self._getNumTip(item.get(const.BF_COMMON_DAMAGE, 0)))))
            obj.SetMember(const.BF_COMMON_CURE, GfxValue(gbk2unicode(self._getFixSizeNum(item.get(const.BF_COMMON_CURE, 0)))))
            obj.SetMember(const.BF_COMMON_CURE + 'Tip', GfxValue(gbk2unicode(self._getNumTip(item.get(const.BF_COMMON_CURE, 0)))))
            obj.SetMember(const.BF_COMMON_JIBAI_DONATE, GfxValue(gbk2unicode(self._convertToDonate(item.get(const.BF_COMMON_JIBAI_DONATE, 0)))))
            obj.SetMember(const.BF_COMMON_BE_DAMAGE, GfxValue(gbk2unicode(self._getFixSizeNum(item.get(const.BF_COMMON_BE_DAMAGE, 0)))))
            obj.SetMember(const.BF_COMMON_BE_DAMAGE + 'Tip', GfxValue(gbk2unicode(self._getNumTip(item.get(const.BF_COMMON_BE_DAMAGE, 0)))))
            obj.SetMember(const.BF_COMMON_KILL_NUM, GfxValue(gbk2unicode(self._getFixSizeNum(item.get(const.BF_COMMON_KILL_NUM, 0)))))
            obj.SetMember(const.BF_COMMON_ASSIST_NUM, GfxValue(gbk2unicode(self._getFixSizeNum(item.get(const.BF_COMMON_ASSIST_NUM, 0)))))
            obj.SetMember('bfSpecialScore0', GfxValue(gbk2unicode(self._convertToDonate(item.get('bfSpecialScore0', 0)))))
            obj.SetMember('bfSpecialScore1', GfxValue(gbk2unicode(self._convertToDonate(item.get('bfSpecialScore1', 0)))))
            obj.SetMember('inLive', GfxValue(p.inLiveOfGuildTournament))
            obj.SetMember('resRoleName', GfxValue(gbk2unicode(memItem.get('roleName', ''))))
            retArray.SetElement(index, obj)
            index += 1

        isBtnVisible = True if not self.tmpResultFbNo else False
        isTimeVisible = True if not self.tmpResultFbNo else False
        ret.SetMember('isBtnVisible', GfxValue(isBtnVisible))
        ret.SetMember('isTimeVisible', GfxValue(isTimeVisible))
        ret.SetMember('array', retArray)
        return ret

    def onGetTmpResultRes(self, *arg):
        info = {}
        p = BigWorld.player()
        info['selfRes'] = p.getMyRes()
        info['enemyRes'] = p.getEnemyRes()
        return uiUtils.dict2GfxDict(info)

    def onTmpResultCloseClick(self, *arg):
        self.closeBFTmpResultWidget()

    def refreshTmpResultWidget(self):
        if self.bfTmpResultMed:
            self.bfTmpResultMed.Invoke('refreshPanel')

    def onNeedReportBtn(self, *arg):
        if not gameglobal.rds.configData.get('enableBfReport', False):
            return GfxValue(False)
        p = BigWorld.player()
        fbNo = formula.getFubenNo(p.spaceNo)
        ret = BFD.data.get(fbNo, {}).get('enableReport', 0)
        return GfxValue(ret)

    def onSetAutoUse(self, *arg):
        p = BigWorld.player()
        autoUseId = int(arg[3][0].GetNumber())
        p.cell.turnBattleFieldShopItemAutoUseSwitch(autoUseId)

    def onGetAutoUseInfo(self, *arg):
        ret = {}
        p = BigWorld.player()
        ret['shopIndex'] = p.autoUseBattleFieldShopIndex
        if p.inFubenType(const.FB_TYPE_BATTLE_FIELD_RES):
            ret['enable'] = gameglobal.rds.configData.get('enableAutoUseBattleFieldShopItem', False)
        else:
            ret['enable'] = False
        ret['textArr'] = self.autoUseArr
        ret['consumeDesc'] = SCD.data.get('BF_CONSUME_AUTOUSE_DESC', gameStrings.TEXT_BATTLEFIELDPROXY_840) % self.consume
        return uiUtils.dict2GfxDict(ret, True)

    def onGetBfMemPerforms(self, *args):
        p = BigWorld.player()
        if not p.bfEnd:
            p.getBfMemPerforms()

    def showBFTmpResultWidget(self):
        p = BigWorld.player()
        if formula.inHuntBattleField(p.mapID) or formula.inDotaBattleField(p.mapID) or p.inFubenType(const.FB_TYPE_BATTLE_FIELD_HOOK) or p.inFubenType(const.FB_TYPE_BATTLE_FIELD_RACE):
            return
        self.onGetBfMemPerforms()
        self.openBFTmpResultWidget()

    def closeBFTmpResultWidget(self):
        self.resetTmpResult()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_BF_TMP_RESULT)
        self.isBFTmpResultShow = False

    def openBFTmpResultWidget(self, tmpResultFbNo = 0):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_BF_TMP_RESULT)
        self.isBFTmpResultShow = True
        self.tmpResultFbNo = tmpResultFbNo

    def _getTitleDesc(self, item):
        ret = self.movie.CreateArray()
        for index, elem in enumerate(item):
            ret.SetElement(index, GfxValue(elem))

        return ret

    def _getExtraAward(self, awardType):
        p = BigWorld.player()
        if not hasattr(p, 'bfResultInfo'):
            return 0
        else:
            disturbRatio = utils.getDisturbRatioByType(p, gametypes.DISTURB_TYPE_DUEL)
            if p.bfResultInfo.get('canGetFame') and p.bfResult == const.WIN and p.bfResultInfo.get('isJumpWeakSide'):
                return int(DCD.data.get(awardType, 0) * p.bfResultInfo.get('extraRatioWithIntimacy', 1) * disturbRatio)
            return 0

    def _getBFPointByResult(self, pointType, resultType):
        p = BigWorld.player()
        if not p.bfResultInfo.get('canGetFame'):
            return 0
        fbNo = formula.getFubenNo(p.spaceNo)
        bfData = BFD.data.get(fbNo, {})
        sPoint = bfData.get(pointType, 0)
        topOneStats = p.getMemStatsByGbId(p.gbId)
        topOneMemInfo = p.getMemInfoByGbId(p.gbId)
        score = 0
        extraScore = 0
        if type(sPoint) == tuple:
            sPoint = list(sPoint)
            topCandidate = p.bfResultInfo.get(resultType, [])
            if p.gbId in topCandidate:
                index = topCandidate.index(p.gbId)
                if resultType == 'cure' and topOneMemInfo.get('school', 0) not in const.SCHOOL_N:
                    if index >= 0 and index < len(sPoint):
                        sPoint[index] = 0
                if index >= 0 and index < len(sPoint):
                    score = sPoint[index]
            else:
                score = 0
        elif resultType == 'mvp':
            if p.gbId == p.bfResultInfo.get('mvp', 0):
                score = sPoint
            else:
                score = 0
        if resultType == 'killNum':
            mode = formula.fbNo2BattleFieldMode(fbNo)
            modeData = BFMD.data.get(mode, {})
            killResUnit = modeData.get('killResUnit', 0)
            killResLimit = modeData.get('killResLimit', 0)
            extraScore = min(topOneStats.get('killNum', 0) * killResUnit, killResLimit)
        elif resultType == 'assist':
            mode = formula.fbNo2BattleFieldMode(fbNo)
            modeData = BFMD.data.get(mode, {})
            assistResUnit = modeData.get('assistResUnit', 0)
            assistResLimit = modeData.get('assistResLimit', 0)
            extraScore = min(topOneStats.get('assistNum', 0) * assistResUnit, assistResLimit)
        disturbRatio = utils.getDisturbRatioByType(p, gametypes.DISTURB_TYPE_DUEL)
        return int((score + extraScore) * p.bfResultInfo.get('extraRatioWithIntimacy', 1) * disturbRatio)

    def _getFailTop3Score(self, pointType, resultType):
        p = BigWorld.player()
        if not p.bfResultInfo.get('canGetFame'):
            return 0
        fbNo = formula.getFubenNo(p.spaceNo)
        bfData = BFD.data.get(fbNo, {})
        sPoint = bfData.get(pointType, 0)
        if hasattr(p, 'bfResultInfo'):
            failTop3 = p.bfResultInfo.get(resultType)
            if failTop3 and p.gbId in failTop3:
                index = failTop3.index(p.gbId)
                return sPoint[index]
            else:
                return -sPoint[0]
        return 0

    def _getFailTopRoleName(self):
        p = BigWorld.player()
        if hasattr(p, 'bfResultInfo'):
            failTop3 = p.bfResultInfo.get('loseMvpList')
            if failTop3:
                gbId = failTop3[0]
                return p.battleFieldTeam.get(gbId, {}).get('roleName')
        return ''

    def _getSumPointByDetail(self, detailList):
        sumPoint = 0
        for item in detailList:
            if item > 0:
                sumPoint += item

        return sumPoint

    def _getTopPlayerNameList(self):
        ret = []
        p = BigWorld.player()
        if len(p.bfMemStats) == 0:
            return ['',
             '',
             '',
             '',
             '']
        attrList = [const.BATTLE_FIELD_TITLE_INDEX_MVP,
         const.BATTLE_FIELD_TITLE_INDEX_KILL,
         const.BATTLE_FIELD_TITLE_INDEX_ASSIST,
         const.BATTLE_FIELD_TITLE_INDEX_CURE,
         const.BATTLE_FIELD_TITLE_INDEX_DAMAGE]
        for attrNameIndex in attrList:
            isGot = False
            for memStats in p.bfMemStats:
                if memStats.has_key('titleDesc') and memStats['titleDesc'][attrNameIndex]:
                    ret.append(memStats['roleName'])
                    isGot = True
                    break

            if not isGot:
                ret.append('')

        return ret

    def onAddFriendWithTopPlayer(self, *arg):
        p = BigWorld.player()
        roleName = unicode2gbk(arg[3][0].GetString())
        p.base.addContact(roleName, gametypes.FRIEND_GROUP_FRIEND, const.FRIEND_SRC_BATTLE_FIELD)

    def _getEnemyConsumeFame(self):
        p = BigWorld.player()
        fbNo = formula.getFubenNo(p.spaceNo)
        if not p.bfResultInfo.get('canGetFame'):
            return (0, 0)
        winResLimit = BFD.data.get(fbNo, {}).get('winResLimit', 100)
        mode = formula.fbNo2BattleFieldMode(fbNo)
        modeData = BFMD.data.get(mode, {})
        winResDiv = modeData.get('winResDiv', 100)
        enemyConsumeZhanXun, enemyConsumeJunZi = min(int(p.getMyRes() / winResDiv), winResLimit), min(int(p.getMyRes() / winResDiv), winResLimit)
        flagReward = 0
        if p.inFubenType(const.FB_TYPE_BATTLE_FIELD_FLAG):
            totalCnt = 0
            for cnt in p._getFlagStats(p.gbId).itervalues():
                totalCnt += cnt

            holdFlagRes = modeData.get('holdFlagRes', 2)
            holdFlagLimit = modeData.get('holdFlagLimit', 20)
            flagReward = min(holdFlagLimit, totalCnt * holdFlagRes)
        disturbRatio = utils.getDisturbRatioByType(p, gametypes.DISTURB_TYPE_DUEL)
        return (int((enemyConsumeZhanXun + flagReward) * p.bfResultInfo.get('extraRatioWithIntimacy', 1) * disturbRatio), int((enemyConsumeJunZi + flagReward) * p.bfResultInfo.get('extraRatioWithIntimacy', 1) * disturbRatio))

    def onGetBFFinalResultInfo(self, *arg):
        p = BigWorld.player()
        ret = self.movie.CreateObject()
        fbNo = formula.getFubenNo(p.spaceNo)
        bfData = BFD.data.get(fbNo, {})
        fbName = bfData.get('name', 'test')
        if not p.bfTimeRec.has_key('tReady'):
            return ret
        duration = int(p.getServerTime() - p.bfTimeRec['tReady'])
        ret.SetMember('battleFieldName', GfxValue(gbk2unicode(fbName)))
        ret.SetMember('duration', GfxValue(duration))
        ret.SetMember('addedFame', GfxValue(p.battleFieldInfo.addedFame))
        ret.SetMember('oldFame', GfxValue(self.fame - p.battleFieldInfo.addedFame))
        ret.SetMember('maxFame', GfxValue(SCD.data.get('maxBattleFieldFame', 9999)))
        ret.SetMember('result', GfxValue(p.getBfResult()))
        selfStats = self.movie.CreateArray()
        selfStats.SetElement(0, GfxValue(p.getMySideKillNum()))
        selfStats.SetElement(1, GfxValue(p.getMySideDeathNum()))
        selfStats.SetElement(2, GfxValue(p.getMySideAssistNum()))
        ret.SetMember('selfStats', selfStats)
        enemyStats = self.movie.CreateArray()
        enemyStats.SetElement(0, GfxValue(p.getOtherSideKillNum()))
        enemyStats.SetElement(1, GfxValue(p.getOtherSideDeathNum()))
        enemyStats.SetElement(2, GfxValue(p.getOtherSideAssistNum()))
        ret.SetMember('enemyStats', enemyStats)
        ret.SetMember('selfRes', GfxValue(p.getMyRes()))
        ret.SetMember('enemyRes', GfxValue(p.getEnemyRes()))
        winRewardZhanXun = self._getWinRewardZhanXun()
        winRewardJunZi = self._getWinRewardJunZi()
        mvpZhanXun = self._getBFPointByResult('mvpZhanXun', 'mvp')
        mvpJunZi = self._getBFPointByResult('mvpJunZi', 'mvp')
        killTop3ZhanXun = self._getBFPointByResult('killTop3ZhanXun', 'killNum')
        killTop3JunZi = self._getBFPointByResult('killTop3JunZi', 'killNum')
        assistTop3ZhanXun = self._getBFPointByResult('assistTop3ZhanXun', 'assist')
        assistTop3JunZi = self._getBFPointByResult('assistTop3JunZi', 'assist')
        damageTop3ZhanXun = self._getBFPointByResult('damageTop3ZhanXun', 'damage')
        damageTop3JunZi = self._getBFPointByResult('damageTop3JunZi', 'damage')
        cureTop3ZhanXun = self._getBFPointByResult('cureTop3ZhanXun', 'cure')
        cureTop3JunZi = self._getBFPointByResult('cureTop3JunZi', 'cure')
        extraAwardZhanXun = self._getExtraAward('bfExtraZhanXun')
        extraAwardJunZi = self._getExtraAward('bfExtraJunZi')
        enemyConsumeZhanXun, enemyConsumeJunZi = self._getEnemyConsumeFame()
        gainJunZi = p.bfResultInfo.get('rewardJunZi', 0)
        gainZhanXun = p.bfResultInfo.get('rewardZhanXun', 0)
        gainJinbi = p.bfResultInfo.get('rewardJinbi', 0)
        gainJinbiVisible = gameglobal.rds.configData.get('enableBattleJinbiReward', False)
        ret.SetMember('winRewardZhanXun', GfxValue(winRewardZhanXun))
        ret.SetMember('winRewardJunZi', GfxValue('+%d' % winRewardJunZi))
        ret.SetMember('enemyConsumeJunZi', GfxValue(enemyConsumeJunZi))
        ret.SetMember('enemyConsumeZhanXun', GfxValue(enemyConsumeZhanXun))
        ret.SetMember('mvpZhanXun', GfxValue(mvpZhanXun))
        ret.SetMember('mvpJunZi', GfxValue(mvpJunZi))
        ret.SetMember('killTop3ZhanXun', GfxValue(killTop3ZhanXun))
        ret.SetMember('killTop3JunZi', GfxValue(killTop3JunZi))
        ret.SetMember('assistTop3ZhanXun', GfxValue(assistTop3ZhanXun))
        ret.SetMember('assistTop3JunZi', GfxValue(assistTop3JunZi))
        ret.SetMember('damageTop3ZhanXun', GfxValue(damageTop3ZhanXun))
        ret.SetMember('damageTop3JunZi', GfxValue(damageTop3JunZi))
        ret.SetMember('cureTop3ZhanXun', GfxValue(cureTop3ZhanXun))
        ret.SetMember('cureTop3JunZi', GfxValue(cureTop3JunZi))
        ret.SetMember('gainZhanXun', GfxValue(gainZhanXun))
        ret.SetMember('gainJunZi', GfxValue(gainJunZi))
        ret.SetMember('gainJinbi', GfxValue(gainJinbi))
        ret.SetMember('gainJinbiVisible', GfxValue(gainJinbiVisible))
        ret.SetMember('topRoleNameList', uiUtils.array2GfxAarry(self._getTopPlayerNameList(), True))
        oldJunZi = p.getFame(const.JUN_ZI_FAME_ID) - gainJunZi
        oldZhanXun = p.getFame(const.ZHAN_XUN_FAME_ID) - gainZhanXun
        maxJunZi = int(JCD.data.get(p.junJieLv, {}).get('maxJunZi', 0) * p.getMaxJunziRate())
        maxZhanXun = int(JCD.data.get(p.junJieLv, {}).get('curMaxJunJie', 0) * p.getMaxZhanxunRate())
        ret.SetMember('oldJunZi', GfxValue(oldJunZi))
        ret.SetMember('oldZhanXun', GfxValue(oldZhanXun))
        ret.SetMember('maxJunZi', GfxValue(maxJunZi))
        ret.SetMember('maxZhanXun', GfxValue(maxZhanXun))
        self.finalSortedArray = self.sortByName(p.bfMemPerforms, self.finalResSortedKey, myReverse=self.finalResSortedType)
        memberStats = self.movie.CreateArray()
        cnt = 0
        for item in self.finalSortedArray:
            try:
                memItem = p.getMemInfoByGbId(item['gbId'])
                if not memItem:
                    continue
                if not p._checkValidSchool(memItem.get('school', 0)):
                    continue
                schoolId = memItem.get('school', 0)
                obj = self.movie.CreateObject()
                obj.SetMember('isMyself', GfxValue(item['gbId'] == p.gbId))
                obj.SetMember('isFriend', GfxValue(memItem['sideNUID'] == p.bfSideNUID))
                obj.SetMember('school', GfxValue(gbk2unicode(SD.data[memItem['school']]['name'])))
                obj.SetMember('schoolLabel', GfxValue(gbk2unicode(uiConst.SCHOOL_FRAME_DESC.get(schoolId, ''))))
                newName = uiUtils.genDuelCrossName('Lv.' + str(memItem['level']) + '-' + memItem['roleName'], memItem.get('fromHostName', ''))
                obj.SetMember('roleName', GfxValue(gbk2unicode(newName)))
                obj.SetMember(const.BF_COMMON_DAMAGE, GfxValue(gbk2unicode(self._getFixSizeNum(item.get(const.BF_COMMON_DAMAGE, 0)))))
                obj.SetMember(const.BF_COMMON_DAMAGE + 'Tip', GfxValue(self._getNumTip(item.get(const.BF_COMMON_DAMAGE, 0))))
                obj.SetMember(const.BF_COMMON_CURE, GfxValue(gbk2unicode(self._getFixSizeNum(item.get(const.BF_COMMON_CURE, 0)))))
                obj.SetMember(const.BF_COMMON_CURE + 'Tip', GfxValue(self._getNumTip(item.get(const.BF_COMMON_CURE, 0))))
                obj.SetMember(const.BF_COMMON_JIBAI_DONATE, GfxValue(gbk2unicode(self._convertToDonate(item.get(const.BF_COMMON_JIBAI_DONATE, 0)))))
                obj.SetMember(const.BF_COMMON_BE_DAMAGE, GfxValue(gbk2unicode(self._getFixSizeNum(item.get(const.BF_COMMON_BE_DAMAGE, 0)))))
                obj.SetMember(const.BF_COMMON_BE_DAMAGE + 'Tip', GfxValue(self._getNumTip(item.get(const.BF_COMMON_BE_DAMAGE, 0))))
                obj.SetMember(const.BF_COMMON_KILL_NUM, GfxValue(gbk2unicode(self._getFixSizeNum(item.get(const.BF_COMMON_KILL_NUM, 0)))))
                obj.SetMember(const.BF_COMMON_ASSIST_NUM, GfxValue(gbk2unicode(self._getFixSizeNum(item.get(const.BF_COMMON_ASSIST_NUM, 0)))))
                obj.SetMember('bfSpecialScore0', GfxValue(gbk2unicode(self._convertToDonate(item.get('bfSpecialScore0', 0)))))
                obj.SetMember('bfSpecialScore1', GfxValue(gbk2unicode(self._convertToDonate(item.get('bfSpecialScore1', 0)))))
                obj.SetMember('titleDesc', self._getTitleDesc(item.get('titleDesc', [0,
                 0,
                 0,
                 0,
                 0,
                 0])))
                memberStats.SetElement(cnt, obj)
                cnt += 1
            except:
                continue

        ret.SetMember('memberStats', memberStats)
        ret.SetMember('enableTJL', GfxValue(gameglobal.rds.configData.get('enableTJL', False)))
        ret.SetMember('usedTJL', GfxValue(getattr(p, 'battleFieldFinalRewardApplied', False)))
        ret.SetMember('isSoul', GfxValue(p._isSoul()))
        ret.SetMember('waitRewardJunzi', GfxValue(gbk2unicode(gameStrings.WAIT_REWARD_JUN_ZI % p.bfResultInfo.get('waitRewardJunzi', 0))))
        ret.SetMember('waitRewardJunziTip', GfxValue(gbk2unicode(DCD.data.get('waitRewardJunziTip', ''))))
        ret.SetMember('mvps', uiUtils.array2GfxAarry(self._getBFMvpsInfo(), True))
        fbNo = formula.getFubenNo(p.spaceNo)
        if formula.whatFubenType(fbNo) == const.FB_TYPE_BATTLE_FIELD_NEW_FLAG:
            jiBai = p.bfResultInfo.get(const.BF_NEW_FLAG_POINT_SRC_AVATAR, [])
        else:
            jiBai = p.bfResultInfo.get(const.BF_COMMON_JI_BAI, [])
        jiBaiData = self._getBattleScoreFromList(jiBai)
        ret.SetMember('jiBaiData', uiUtils.dict2GfxDict(jiBaiData, True))
        battleData = []
        if formula.whatFubenType(fbNo) == const.FB_TYPE_BATTLE_FIELD_RES:
            battleData.append(self._getBattleDataItem(p.bfResultInfo.get(const.BF_RES_SPECIAL_BOSS_JIBAI_CNT, []), 0, const.FB_TYPE_BATTLE_FIELD_RES))
            battleData.append(self._getBattleDataItem(p.bfResultInfo.get(const.BF_RES_SPECIAL_ZAIJU_DAMAGE, []), 1, const.FB_TYPE_BATTLE_FIELD_RES))
        elif formula.whatFubenType(fbNo) == const.FB_TYPE_BATTLE_FIELD_FLAG:
            battleData.append(self._getBattleDataItem(p.bfResultInfo.get(const.BF_FLAG_FIGHT_IN_FLAG_TIME, []), 0, const.FB_TYPE_BATTLE_FIELD_FLAG))
            battleData.append(self._getBattleDataItem(p.bfResultInfo.get(const.BF_FLAG_HOLD_FLAG_CNT, []), 1, const.FB_TYPE_BATTLE_FIELD_FLAG))
        elif formula.whatFubenType(fbNo) == const.FB_TYPE_BATTLE_FIELD_FORT:
            battleData.append(self._getBattleDataItem(p.bfResultInfo.get(const.BF_FORT_FIGHT_IN_FLAG_TIME, []), 0, const.FB_TYPE_BATTLE_FIELD_FORT))
            battleData.append(self._getBattleDataItem(p.bfResultInfo.get(const.BF_FORT_WITH_FLY_DAMAGE_TOTAL, []), 1, const.FB_TYPE_BATTLE_FIELD_FORT))
        elif formula.whatFubenType(fbNo) == const.FB_TYPE_BATTLE_FIELD_NEW_FLAG:
            battleData.append(self._getBattleDataItem(p.bfResultInfo.get(const.BF_NEW_FLAG_POINT_SRC_MONSTER, []), 0, const.FB_TYPE_BATTLE_FIELD_NEW_FLAG))
            battleData.append(self._getBattleDataItem(p.bfResultInfo.get(const.BF_NEW_FLAG_POINT_SRC_TOWER, []), 1, const.FB_TYPE_BATTLE_FIELD_NEW_FLAG))
        elif formula.whatFubenType(fbNo) == const.FB_TYPE_BATTLE_FIELD_CQZZ:
            battleData.append(self._getBattleDataItem(p.bfResultInfo.get(const.BF_CQZZ_POINT_SRC_FLAG, []), 0, const.FB_TYPE_BATTLE_FIELD_CQZZ))
            battleData.append(self._getBattleDataItem(p.bfResultInfo.get(const.BF_CQZZ_POINT_SRC_AVATAR, []), 1, const.FB_TYPE_BATTLE_FIELD_CQZZ))
        ret.SetMember('battleData', uiUtils.array2GfxAarry(battleData, True))
        basisBattleData = []
        basisBattleData.append(self._getBattleScoreFromList(p.bfResultInfo.get(const.BF_COMMON_DAMAGE, [])))
        basisBattleData.append(self._getBattleScoreFromList(p.bfResultInfo.get(const.BF_COMMON_CURE, [])))
        basisBattleData.append(self._getBattleScoreFromList(p.bfResultInfo.get(const.BF_COMMON_BE_DAMAGE, [])))
        ret.SetMember('basisBattleData', uiUtils.array2GfxAarry(basisBattleData, True))
        topInfo = []
        for topGbId in p.bfResultInfo.get('top5', []):
            topInfo.append({'gbId': topGbId,
             'topName': p.battleFieldTeam.get(topGbId).get('roleName'),
             'school': SD.data[p.battleFieldTeam.get(topGbId).get('school')]['name'],
             'schoolLabel': uiConst.SCHOOL_FRAME_DESC.get(p.battleFieldTeam.get(topGbId).get('school'), '')})

        ret.SetMember('topInfo', uiUtils.array2GfxAarry(topInfo, True))
        bfItem = BFD.data.get(p.getBattleFieldFbNo(), {})
        isInTodayActivity = bfItem.get('isInTodayActivity', False)
        zhanxunContentList = []
        if p.bfResultInfo.get('hasDailyZhanxun', 0):
            zhanxunContentList.append(gameStrings.FIRST_EXTRA_REWARD % bfItem.get('dailyZhanxunVal', 0))
        if p.bfResultInfo.get('hasDailyWinZhanxun', 0):
            zhanxunContentList.append(gameStrings.FIRST_WIN_REWARD % (bfItem.get('dailyWinZhanxunRadio', 0) * 100))
        if bfItem.get('teamTimeZhanxunRadio', 0) and isInTodayActivity:
            szFbExtra = gameStrings.EXTRAREWARD % (bfItem.get('teamTimeZhanxunRadio', 0) * 100)
            if p.bfResultInfo.get('bfExtraZhanxunNum', 0):
                zhanxunContentList.append(szFbExtra)
            else:
                zhanxunContentList.append("<font color = \'#999999\'>%s</font>" % szFbExtra)
        if p.bfResultInfo.get('hasUpRegionZhanxun', 0):
            zhanxunContentList.append(gameStrings.WAR_EXTRA_REWARD % (bfItem.get('upRegionZhanxunRadio', 0) * 100))
        ret.SetMember('bfZhanxunContentList', uiUtils.array2GfxAarry(zhanxunContentList, True))
        junziContentList = []
        if p.bfResultInfo.get('hasDailyJunzi', 0):
            junziContentList.append(gameStrings.FIRST_EXTRA_REWARD % bfItem.get('dailyJunziVal', 0))
        if p.bfResultInfo.get('hasDailyWinJunzi', 0):
            junziContentList.append(gameStrings.FIRST_WIN_REWARD % (bfItem.get('dailyWinJunziRadio', 0) * 100))
        if bfItem.get('teamTimeJunziRadio', 0) and isInTodayActivity:
            szFbExtra = gameStrings.EXTRAREWARD % (bfItem.get('teamTimeJunziRadio', 0) * 100)
            if p.bfResultInfo.get('hasTeamOpenTimeJunzi', 0):
                junziContentList.append(szFbExtra)
            else:
                junziContentList.append("<font color = \'#999999\'>%s</font>" % szFbExtra)
        if p.bfResultInfo.get('hasUpRegionJunzi', 0):
            junziContentList.append(gameStrings.WAR_EXTRA_REWARD % (bfItem.get('upRegionJunziRadio', 0) * 100))
        ret.SetMember('bfJunziContentList', uiUtils.array2GfxAarry(junziContentList, True))
        jinbiContentList = []
        if p.bfResultInfo.get('hasDailyJunzi', 0):
            jinbiContentList.append(gameStrings.FIRST_EXTRA_REWARD % bfItem.get('dailyJinbiVal', 0))
        if p.bfResultInfo.get('hasDailyWinJunzi', 0):
            jinbiContentList.append(gameStrings.FIRST_WIN_REWARD % (bfItem.get('dailyWinJinbiRadio', 0) * 100))
        if bfItem.get('teamTimeJinbiRadio', 0) and isInTodayActivity:
            jinbiContentList.append(gameStrings.EXTRAREWARD % (bfItem.get('teamTimeJinbiRadio', 0) * 100))
        if p.bfResultInfo.get('hasUpRegionJunzi', 0):
            jinbiContentList.append(gameStrings.WAR_EXTRA_REWARD % (bfItem.get('upRegionJinbiRadio', 0) * 100))
        ret.SetMember('bfJinbiContentList', uiUtils.array2GfxAarry(jinbiContentList, True))
        ret.SetMember('resultMenuTipNormal', uiUtils.array2GfxAarry(DCD.data.get('resultMenuTipNormal', ()), True))
        ret.SetMember('resultMenuTipSpecial', uiUtils.array2GfxAarry(DCD.data.get('resultMenuTipSpecial', {}).get(formula.whatFubenType(fbNo), ()), True))
        ret.SetMember('resultRankTip', uiUtils.array2GfxAarry(DCD.data.get('resultRankTip', ()), True))
        isHideZhanxunAndJunzi = gameglobal.rds.configData.get('enableNewFlagBF', False) and formula.whatFubenType(fbNo) == const.FB_TYPE_BATTLE_FIELD_NEW_FLAG
        ret.SetMember('isHideZhanxunAndJunzi', GfxValue(isHideZhanxunAndJunzi))
        return ret

    def _getFixSizeNum(self, num):
        num = max(0, num)
        if num > 10000:
            return gameStrings.BF_RESULT_WAN % int(num / 10000)
        return str(num)

    def _getNumTip(self, num):
        num = max(0, num)
        if num > 10000:
            return gameStrings.DETAIL_NUM % num
        return ''

    def _convertToDonate(self, donate):
        return gameStrings.BF_MEM_CONTRIBUTE_TXT % donate

    def _getBFMvpsInfo(self):
        p = BigWorld.player()
        mvps = []
        mySideGbId = 0
        for gbId, mvpItem in p.bfResultInfo.get('mvps', {}).iteritems():
            for mem in p.bfMemPerforms:
                if mem['gbId'] == gbId and mem['sideNUID'] == p.bfSideNUID:
                    mySideGbId = mem['gbId']
                    mvps.append({'mvpName': p.battleFieldTeam.get(gbId, {}).get('roleName'),
                     'serverName': mvpItem.get('serverName', '') if mvpItem.get('serverName', '') else utils.getServerName(utils.getHostId()),
                     'donateScore': mvpItem.get('donateScore', 0),
                     'school': SD.data[p.battleFieldTeam.get(gbId).get('school')]['name'],
                     'schoolLabel': uiConst.SCHOOL_FRAME_DESC.get(p.battleFieldTeam.get(gbId).get('school'), '')})

        for gbId, mvpItem in p.bfResultInfo.get('mvps', {}).iteritems():
            if gbId != mySideGbId:
                mvps.append({'mvpName': p.battleFieldTeam.get(gbId, {}).get('roleName'),
                 'serverName': mvpItem.get('serverName', '') if mvpItem.get('serverName', '') else utils.getServerName(utils.getHostId()),
                 'donateScore': mvpItem.get('donateScore', 0),
                 'school': SD.data[p.battleFieldTeam.get(gbId).get('school')]['name'],
                 'schoolLabel': uiConst.SCHOOL_FRAME_DESC.get(p.battleFieldTeam.get(gbId).get('school'), '')})

        return mvps

    def _getBattleScoreFromList(self, originData):
        return {'rank': originData[0],
         'num': originData[1],
         'contribute': originData[2],
         'reward': '%s' % str(int(originData[4])),
         'zhanXun': '%s' % str(int(originData[3]))}

    def _getBattleDataItem(self, originData, menuIndex, battleId):
        menuName = uiConst.BATTLE_FIELD_RESULT_MENU_NAME[battleId][menuIndex]
        item = self._getBattleScoreFromList(originData)
        item['menuName'] = menuName
        return item

    def _getSelfDetail(self, key):
        p = BigWorld.player()
        myInfo = p.getMemStatsByGbId(p.gbId)
        if not myInfo.has_key('titleDesc'):
            return 0
        if key == 'cure':
            return myInfo['titleDesc'][1]
        if key == 'killNum':
            return myInfo['titleDesc'][4]
        if key == 'damage':
            return myInfo['titleDesc'][2]
        if key == 'assist':
            return myInfo['titleDesc'][3]
        if key == 'mvp':
            return myInfo['titleDesc'][5]
        return 0

    def _getEnemyConsume(self):
        junZi = 0
        zhanXun = 0
        p = BigWorld.player()
        data = BFD.data.get(p.getBattleFieldFbNo(), {})
        enemyMaxRes = data.get('initRes', 100)
        damageRes = enemyMaxRes - p.getEnemyRes()
        enemyConsumeResAward = data.get('enemyConsumeResAward', [])
        enemyConsumeResAward = sorted(enemyConsumeResAward, cmp=lambda x, y: cmp(x[0], y[0]), reverse=True)
        for item in enemyConsumeResAward:
            if damageRes >= item[0]:
                junZi = item[1]
                zhanXun = item[2]
                break

        return (junZi, zhanXun)

    def _getWinRewardZhanXun(self):
        p = BigWorld.player()
        fbNo = formula.getFubenNo(p.spaceNo)
        if not p.bfResultInfo.get('canGetFame'):
            return 0
        if p.getBfResult() == const.WIN:
            ret = BFD.data.get(fbNo, {}).get('winRewardZhanXun', 0) * p.bfResultInfo.get('extraRatioWithIntimacy', 1)
        else:
            ret = 0
        disturbRatio = utils.getDisturbRatioByType(p, gametypes.DISTURB_TYPE_DUEL)
        return int(ret * disturbRatio)

    def _getWinRewardJunZi(self):
        p = BigWorld.player()
        fbNo = formula.getFubenNo(p.spaceNo)
        if not p.bfResultInfo.get('canGetFame'):
            return 0
        if p.getBfResult() == const.WIN:
            ret = BFD.data.get(fbNo, {}).get('winRewardJunZi', 0) * p.bfResultInfo.get('extraRatioWithIntimacy', 1)
        else:
            ret = 0
        disturbRatio = utils.getDisturbRatioByType(p, gametypes.DISTURB_TYPE_DUEL)
        return int(ret * disturbRatio)

    def onFinalResultSortClick(self, *arg):
        self.finalResSortedKey = arg[3][0].GetString()
        self.finalResSortedType = int(arg[3][1].GetNumber())
        gamelog.debug('@hjx bf result#onFinalResultSortClick:', self.finalResSortedKey, self.finalResSortedType)

    def onFinalResultLeaveClick(self, *arg):
        p = BigWorld.player()
        p.cell.quitBattleField()

    def onShowScoreAward(self, *arg):
        if gameglobal.rds.ui.bFScoreAward.mediator:
            gameglobal.rds.ui.bFScoreAward.hide()
        else:
            gameglobal.rds.ui.bFScoreAward.show()

    def onNeedScoreAward(self, *arg):
        needShow = False
        for value in GTD.data.itervalues():
            if value.get('bfNo', 0) == BigWorld.player().getBattleFieldFbNo() or value.get('testbfNo', 0) == BigWorld.player().getBattleFieldFbNo() or BigWorld.player().getBattleFieldFbNo() in value.get('fbNoList', []):
                needShow = True
                break

        if not needShow:
            for value in CGTD.data.itervalues():
                if value.get('bfNo', 0) == BigWorld.player().getBattleFieldFbNo() or value.get('testbfNo', 0) == BigWorld.player().getBattleFieldFbNo():
                    needShow = True
                    break

        if needShow:
            gameglobal.rds.ui.bFScoreAward.show()
        return GfxValue(needShow)

    @ui.callFilter(3)
    def onUseSpecialItem(self, *arg):
        itemId = DCD.data.get('tianjianglingitemId', 0)
        reGetItemCnt = DCD.data.get('reGetItemCnt', 1)
        p = BigWorld.player()
        if not itemId:
            return
        itemInfo = uiUtils.getGfxItemById(itemId)
        itemName = uiUtils.getItemColorName(itemId)
        if not p.inv.canRemoveItems({itemId: reGetItemCnt}, enableParentCheck=True):
            p.showGameMsg(GMDD.data.RE_GET_FAME_FAILED_IN_BATTLE_FIELD_NO_SUCH_ITEM, (reGetItemCnt, itemName))
            return
        msg = DCD.data.get('tianjianglingTips', gameStrings.TEXT_BATTLEFIELDPROXY_1439) % itemName
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.onConfirmUseSpecialItem, itemId), itemData=itemInfo)

    def onConfirmUseSpecialItem(self, itemId):
        BigWorld.player().cell.applyBattleFieldFinalReward()

    def onOpenRank(self, *arg):
        gameglobal.rds.ui.ranking.show(const.PROXY_KEY_TOP_CLAN_WAR_SCORE)

    def onGetGongXianFen(self, *arg):
        return GfxValue(BigWorld.player().battleFieldScore)

    def refreshBattleFieldScore(self):
        p = BigWorld.player()
        if not p.inFubenType(const.FB_TYPE_BATTLE_FIELD_RES) and not p.inFubenType(const.FB_TYPE_BATTLE_FIELD_HOOK):
            return
        if self.bfStatsMed:
            self.bfStatsMed.Invoke('setScore')

    def onGoHomeClick(self, *arg):
        BigWorld.player().bfGoHome()

    def onOpenShopClick(self, *arg):
        BigWorld.player().cell.openBattleFieldShop()

    def onOpenStatsClick(self, *arg):
        if gameglobal.rds.ui.battleField.isBFTmpResultShow:
            gameglobal.rds.ui.battleField.closeBFTmpResultWidget()
        else:
            gameglobal.rds.ui.battleField.showBFTmpResultWidget()

    def showBFFinalResultWidget(self):
        p = BigWorld.player()
        if formula.inHuntBattleField(p.mapID) or formula.inDotaBattleField(p.mapID) or p.inFubenType(const.FB_TYPE_BATTLE_FIELD_HOOK):
            return
        self.closeBFTmpResultWidget()
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_BF_FINAL_RESULT, isModal=True)

    def closeBFFinalResutlWidget(self):
        self.resetFinalResult()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_BF_FINAL_RESULT)

    def refreshBFFinalResult(self):
        if self.bfFinalResultMed:
            self.bfFinalResultMed.Invoke('refreshPanel', GfxValue(True))

    def onGetFirstKillInfo(self, *arg):
        ret = self.movie.CreateObject()
        ret.SetMember('killer', GfxValue(gbk2unicode(self.killer)))
        ret.SetMember('killee', GfxValue(gbk2unicode(self.killee)))
        return ret

    def showFirstKill(self, killer, killee):
        self.killer = killer
        self.killee = killee
        soundId = SCD.data.get('FistBloodSoundId', 954)
        gameglobal.rds.sound.playSound(int(soundId))
        if self.bfFirstKillMed:
            self.bfFirstKillMed.Invoke('refreshPanel')
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_BF_FIRST_KILL)

    def showAssist(self):
        if self.bfAssistMed:
            self.bfAssistMed.Invoke('refreshPanel')
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_BF_ASSIST)

    def showTopMsg(self):
        if not self.bfTopMsg:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_BF_MSG)

    def setTopMsgString(self, topMsg):
        if self.bfTopMsg:
            self.bfTopMsg.Invoke('showSystemTips', GfxValue(gbk2unicode(topMsg)))

    def onGetKillCnt(self, *arg):
        return GfxValue(self.killCnt)

    def showKill(self, killCnt):
        if killCnt > 10:
            killCnt = 10
        soundIdList = SCD.data.get('ComboKillSoundId', [956,
         957,
         958,
         959,
         960,
         962,
         963,
         964,
         965,
         966])
        pos = killCnt - 2
        if pos >= len(soundIdList):
            pos = len(soundIdList) - 1
        gameglobal.rds.sound.playSound(soundIdList[pos])
        self.killCnt = killCnt
        if self.bfKillMed:
            self.bfKillMed.Invoke('refreshPanel')
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_BF_KILL)

    def showKillInWingWorld(self, killCnt):
        if killCnt > 10:
            killCnt = 10
        soundIdList = SCD.data.get('ComboKillSoundId', [956,
         957,
         958,
         959,
         960,
         962,
         963,
         964,
         965,
         966])
        pos = killCnt - 2
        if pos >= len(soundIdList):
            pos = len(soundIdList) - 1
        if killCnt == 1:
            return
        gameglobal.rds.sound.playSound(soundIdList[pos])
        self.killCnt = killCnt
        if self.bfKillMed:
            self.bfKillMed.Invoke('refreshPanel')
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_BF_KILL)

    def showMonsterTimer(self, vis):
        if vis:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_MONSTER_TIMER)
        else:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_MONSTER_TIMER)

    def addMonsterTimer(self, monsterName, time):
        if self.monsterTimerMed:
            self.monsterTimerMed.Invoke('addMonsterTimerItem', (GfxValue(gbk2unicode(monsterName)), GfxValue(int(time))))

    def onUseBattleFieldItem(self, *arg):
        index = int(arg[3][0].GetNumber())
        it = self._getBfShopItem(index)
        if not it:
            gamelog.error('shopProxy, no data in infoDic ', 0, index)
            return
        p = BigWorld.player()
        bagPage, bagPos = p.inv.searchBestInPages(it.id, 1, it)
        if bagPage == const.CONT_NO_PAGE or bagPos == const.CONT_NO_POS:
            p.showGameMsg(GMDD.data.SHOP_BAG_FULL, ())
            return
        p.cell.buyBattleFileItem(0, index, 1)
        gameglobal.rds.sound.playSound(gameglobal.SD_26)

    def onBfFortInitDone(self, *args):
        if not self.bfFortMed:
            return
        if not self.enterFortId:
            return
        p = BigWorld.player()
        for info in getattr(p, 'bfFortInfo', {}).values():
            if info.get('fortId', 0) == self.enterFortId:
                self.enterFort(self.enterFortId, info.get('curValMap', {}))
                break

    def _getBfShopItem(self, index):
        if index >= len(self.bfShopItems):
            return None
        else:
            return self.bfShopItems[index]

    def openItemShop(self, items):
        self.bfShopItems = items
        self.initAutoUseArray()
        self.showBfItemShop()

    def initAutoUseArray(self):
        self.autoUseArr = [{'label': gameStrings.TEXT_BATTLEFIELDPROXY_1605}]
        for it in self.bfShopItems:
            if it:
                name = ID.data.get(it.id, {}).get('name', '')
                self.autoUseArr.append({'label': gameStrings.TEXT_BATTLEFIELDPROXY_1609 % name})

    def showBfItemShop(self):
        ret = []
        i = 0
        for item in self.bfShopItems:
            itemId = item.id
            itemObj = self._getItemInfo(itemId)
            itemObj['index'] = i
            i += 1
            ret.append(itemObj)

        if self.bfStatsMed:
            self.bfStatsMed.Invoke('openShop', uiUtils.array2GfxAarry(ret, True))

    def _getItemInfo(self, itemId):
        p = BigWorld.player()
        playerScore = p.battleFieldScore
        obj = self._getItemData(itemId)
        itemObj = {}
        itemObj['itemId'] = itemId
        itemObj['itemName'] = uiUtils.getItemColorName(itemId)
        itemObj['itemDesc'] = obj.get('desc', '')
        itemObj['itemCost'] = uiUtils.getTextFromGMD(GMDD.data.BATTLE_FIELD_ITEM_COST_TEXT, gameStrings.TEXT_BATTLEFIELDPROXY_1633) % obj.get('consume', 0)
        self.consume = obj.get('consume', 0)
        if obj['useDirectly']:
            itemObj['btnLabel'] = gameStrings.TEXT_CLANWARPROXY_217
        else:
            itemObj['btnLabel'] = gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_990
        itemObj['isEnough'] = playerScore >= obj.get('consume', 0)
        return itemObj

    def _getItemData(self, itemId):
        p = BigWorld.player()
        battleNo = formula.getFubenNo(p.spaceNo)
        data = BFSID.data.get(battleNo, {})
        for obj in data:
            if obj['itemId'] == itemId:
                return obj

        return {}

    def refreshShopList(self):
        if not BigWorld.player().inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
            return
        ret = []
        i = 0
        for item in self.bfShopItems:
            itemId = item.id
            itemObj = self._getItemInfo(itemId)
            itemObj['index'] = i
            i += 1
            ret.append(itemObj)

        if self.bfStatsMed:
            self.bfStatsMed.Invoke('updateShop', uiUtils.array2GfxAarry(ret, True))

    def enterFort(self, fortId, curValMap):
        self.enterFortId = fortId
        if not self.isBFFortMedNone():
            return
        fortData = BFFD.data.get(fortId, {})
        fortInfo = {'fortType': fortData.get('icon', 0),
         'values': (fortData.get('limitVal', 50), fortData.get('maxVal', 100))}
        fortVal = curValMap.get(BigWorld.player().tempCamp, 0)
        if fortVal <= 0:
            otherCamp = 3 - BigWorld.player().tempCamp
            fortVal = -curValMap.get(otherCamp, 0)
        fortInfo['fortVal'] = fortVal
        fortInfo['state'] = self.getFortOccupType(fortId, fortVal)
        if gameglobal.rds.configData.get('enableGuildTournamentLiveAndInspire', False):
            if gameglobal.rds.ui.bFFortInfoV1.widget:
                gameglobal.rds.ui.bFFortInfoV1.setFortInfo(fortInfo)
        else:
            self.bfFortMed.Invoke('setFortInfo', uiUtils.dict2GfxDict(fortInfo, True))

    def leaveFort(self, fortId):
        if self.enterFortId == fortId:
            self.enterFortId = None
            if gameglobal.rds.configData.get('enableGuildTournamentLiveAndInspire', False):
                if gameglobal.rds.ui.bFFortInfoV1.widget:
                    gameglobal.rds.ui.bFFortInfoV1.setFortInfo()
            elif self.bfFortMed:
                self.bfFortMed.Invoke('setFortInfo')

    def fortValChanged(self, fortId, curValMap):
        if not self.isBFFortMedNone():
            return
        if self.enterFortId == fortId:
            self.enterFort(fortId, curValMap)

    def isBFFortMedNone(self):
        if gameglobal.rds.configData.get('enableGuildTournamentLiveAndInspire', False):
            return gameglobal.rds.ui.bFFortInfoV1.widget
        else:
            return self.bfFortMed

    def getFortOccupType(self, fortId, fortVal):
        fortData = BFFD.data.get(fortId, {})
        limitVal = fortData.get('limitVal', 50)
        if fortVal >= limitVal:
            return uiConst.BF_FORT_STATE_MY_FULL_HOLDED
        if fortVal > 0:
            return uiConst.BF_FORT_STATE_MY_HALF_HOLDED
        if fortVal <= -limitVal:
            return uiConst.BF_FORT_STATE_ENEMY_FULL_HOLDED
        if fortVal < 0:
            return uiConst.BF_FORT_STATE_ENEMY_HALF_HOLDED
        return uiConst.BF_FORT_STATE_DEFAULT

    def refreshAllPlaneInfo(self):
        if not self.isBFFortMedNone():
            return
        if not hasattr(BigWorld.player(), 'bfScore'):
            return
        p = BigWorld.player()
        planeResUnit = BFD.data.get(p.getBattleFieldFbNo(), {}).get('planeConsumeScore', 100)
        myScore = p.getMyScore()
        enemyScore = p.getEnemyScore()
        ret = ((int(myScore / planeResUnit), myScore % planeResUnit * 1.0 / planeResUnit), (int(enemyScore / planeResUnit), enemyScore % planeResUnit * 1.0 / planeResUnit))
        if gameglobal.rds.configData.get('enableGuildTournamentLiveAndInspire', False):
            if gameglobal.rds.ui.bFFortInfoV1.widget:
                gameglobal.rds.ui.bFFortInfoV1.setAllPlaneInfo(ret)
        else:
            self.bfFortMed.Invoke('setAllPlaneInfo', uiUtils.array2GfxAarry(ret))

    def refreshAllBulletInfo(self):
        if not self.isBFFortMedNone():
            return
        p = BigWorld.player()
        bulletMax = BFD.data.get(p.getBattleFieldFbNo(), {}).get('maxBullet', 50)
        ret = {'myBullet': p.getMyBullet(),
         'enemyBullet': p.getEnemyBullet(),
         'myMaxBullet': bulletMax,
         'enemyMaxBullet': bulletMax}
        if gameglobal.rds.configData.get('enableGuildTournamentLiveAndInspire', False):
            if gameglobal.rds.ui.bFFortInfoV1.widget:
                gameglobal.rds.ui.bFFortInfoV1.setBulletInfo(ret)
        else:
            self.bfFortMed.Invoke('setBulletInfo', uiUtils.dict2GfxDict(ret, True))

    def onReportClick(self, *arg):
        if self.bfTmpResultMed:
            gameglobal.rds.ui.bFReportChoose.show()

    def onClickShareBtn(self, *args):
        if self.bfFinalResultMed:
            widget = ASObject(self.bfFinalResultMed.Invoke('getWidget'))
            shareInfo = gameglobal.rds.ui.qrCodeAppScanShare.createShareInfoInstance(dailyShare=True)
            shareInfo.uiRange = uiUtils.getMCTopBottomOnWidget(widget, widget.resultView)
            gameglobal.rds.ui.qrCodeAppScanShare.show(shareInfo)

    def onEnableQRCode(self, *args):
        return GfxValue(gameglobal.rds.configData.get('enableQRCode', False))
