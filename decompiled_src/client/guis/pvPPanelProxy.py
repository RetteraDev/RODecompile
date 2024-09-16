#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/pvPPanelProxy.o
import BigWorld
import gameglobal
import uiConst
import gametypes
import utils
import const
import formula
from uiTabProxy import UITabProxy
from guis import uiUtils
from data import battle_field_mode_data as BFMD
from data import battle_field_data as BFD
from data import arena_score_desc_data as ASDD
from cdata import game_msg_def_data as GMDD

class PvPPanelProxy(UITabProxy):

    def __init__(self, uiAdapter):
        super(PvPPanelProxy, self).__init__(uiAdapter)
        self.applyTab = -1
        self.cFlag = 0
        self.isTodayActivityPushed = False
        self.callbackTimer = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_PVP_BG_V2, self.hide)

    def onApplyCommander(self, *args):
        applyCommander = int(args[3][0].GetNumber())
        self.cFlag = applyCommander

    def onGetApplyCommander(self, *args):
        checkboxEnable = getattr(BigWorld.player(), 'battleFieldStage', 1) == uiConst.BF_PANEL_STAGE_INIT
        ret = [self.cFlag, checkboxEnable]
        return uiUtils.array2GfxAarry(ret, True)

    def getGroupHeaderCandidateFlag(self):
        return self.cFlag

    def openTodayActivity(self):
        if not self.todayActivityCheck():
            return
        self.toggle(uiConst.PVP_BG_V2_TAB_TODAY_BATTLE_FIELD, -1)

    def todayActivityCheck(self, checkTabIdx = -1):
        if checkTabIdx != -1:
            if checkTabIdx == uiConst.PVP_BG_V2_TAB_PUBG:
                return False
        for key, val in BFMD.data.items():
            if gameglobal.rds.ui.pvpActivityV2.isTodayActivityAvaliable(val) and gameglobal.rds.ui.pvpActivityV2.isInTodayActivity(val) and gameglobal.rds.ui.pvpActivityV2.isBFAvaliable(val):
                return True

        return False

    def show(self, tabIdx = 1, fbMode = 1):
        p = BigWorld.player()
        if formula.isDoubleArenaCrossServerML(formula.getMLGNo(p.spaceNo)):
            self.pvpPanelShow(uiConst.PVP_BG_V2_TAB_BALANCE_ARENA_2PERSON, fbMode)
            return
        if self.todayActivityCheck(tabIdx):
            self.pvpPanelShow(0, fbMode)
        elif tabIdx == 1:
            if not gameglobal.rds.configData.get('hidePvpArenaPanel', False):
                self.pvpPanelShow(2, fbMode)
            else:
                self.pvpPanelShow(1, fbMode)
        elif tabIdx == 2:
            self.pvpPanelShow(1, fbMode)
        else:
            self.pvpPanelShow(tabIdx, fbMode)

    def pvpPanelRefreshBF(self):
        p = BigWorld.player()
        stage = getattr(p, 'battleFieldStage', 1)
        if gameglobal.rds.ui.pvpActivityV2.widget:
            if stage == uiConst.BF_PANEL_STAGE_APPLYED:
                gameglobal.rds.ui.pvPPanel.setApply(uiConst.APPLY_TABIDX_ACTIVITYV2)
            else:
                gameglobal.rds.ui.pvPPanel.setApply(uiConst.APPLY_TABIDX_NONE)
            gameglobal.rds.ui.pvpActivityV2.refreshBF()
        elif self.currentTabIndex == uiConst.PVP_BG_V2_TAB_PUBG:
            if stage != uiConst.BF_PANEL_STAGE_INIT:
                gameglobal.rds.ui.pvPPanel.setApply(uiConst.APPLY_TABIDX_PUBG)
            else:
                gameglobal.rds.ui.pvPPanel.setApply(uiConst.APPLY_TABIDX_NONE)
            gameglobal.rds.ui.pvpPUBG.refreshBF()
        else:
            if stage == uiConst.BF_PANEL_STAGE_APPLYED:
                gameglobal.rds.ui.pvPPanel.setApply(uiConst.APPLY_TABIDX_BATTLEFIELDV2)
            else:
                gameglobal.rds.ui.pvPPanel.setApply(uiConst.APPLY_TABIDX_NONE)
            gameglobal.rds.ui.pvpBattleFieldV2.refreshBF()

    def getPlayerTopRankKey(self):
        p = BigWorld.player()
        return self.getPlayerLvKey() % str(p.school)

    def getPlayerLvKey(self):
        lvKey = uiUtils.getPlayerTopRankKey()
        return lvKey + '_%s'

    def pushTodayActivityMsg(self):
        if self.callbackTimer:
            BigWorld.cancelCallback(self.callbackTimer)
            self.callbackTimer = 0
        minNextTime = const.SECONDS_PER_WEEK
        needPushNow = False
        for key, bfItem in BFMD.data.items():
            if not bfItem.get('needCalcDaily', 0) or not gameglobal.rds.ui.pvpActivityV2.isBFAvaliable(bfItem):
                continue
            mode = bfItem.get('mode', const.BATTLE_FIELD_MODE_FLAG)
            if mode == const.BATTLE_FIELD_MODE_NEW_FLAG:
                openStartTimes = bfItem.get('openStartTimes', ())
                openEndTimes = bfItem.get('openEndTimes', ())
                for index, starTime in enumerate(openStartTimes):
                    if starTime and openEndTimes[index]:
                        if not needPushNow and utils.inTimeTupleRange(starTime, openEndTimes[index]):
                            needPushNow = True
                        nextTime = utils.nextByTimeTuple(starTime)
                        if nextTime > 0:
                            minNextTime = min(nextTime, minNextTime)

            else:
                openStartTimes = bfItem.get('todayActivityStartTime', ())
                openEndTimes = bfItem.get('todayActivityEndTime', ())
                for index, starTime in enumerate(openStartTimes):
                    if starTime and openEndTimes[index]:
                        if not needPushNow and utils.inTimeTupleRange(starTime[0], openEndTimes[index][0]):
                            needPushNow = True
                        nextTime = utils.nextByTimeTuple(starTime[0])
                        if nextTime > 0:
                            minNextTime = min(nextTime, minNextTime)

        if needPushNow:
            self.addPushMsg()
        if minNextTime > 0:
            self.callbackTimer = BigWorld.callback(minNextTime + 2, self.pushTodayActivityMsg)

    def addPushMsg(self):
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_TODAY_ACTIVITY)
        gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_TODAY_ACTIVITY, {'click': self.onClickTodayActivityMsg})
        self.callbackTimer = 0

    def onClickTodayActivityMsg(self):
        self.openTodayActivity()
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_TODAY_ACTIVITY)

    def todayActivityPushCheck(self):
        for key, val in BFMD.data.items():
            if gameglobal.rds.ui.pvpActivityV2.isBFAvaliable(val) and val.get('needCalcDaily', 0) and gameglobal.rds.ui.pvpActivityV2.isTodayActivityAvaliable(val):
                return True

        return False

    def pvpPanelShow(self, showTabIndex, fbMode = 1):
        if not BigWorld.player().checkMapLimitUI(gametypes.MAP_LIMIT_UI_PVP):
            return
        self.fbMode = fbMode
        self.showTabIndex = showTabIndex
        if self.widget:
            self.widget.swapPanelToFront()
            self.widget.setTabIndex(self.showTabIndex)
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_PVP_BG_V2)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_PVP_BG_V2:
            self.widget = widget
            self.initUI()
            self.widget.setTabIndex(self.showTabIndex)

    def _getTabList(self):
        return [{'tabIdx': uiConst.PVP_BG_V2_TAB_TODAY_BATTLE_FIELD,
          'tabName': 'todayBfTabBtn',
          'view': 'PvpActivityV2Widget',
          'proxy': 'pvpActivityV2'},
         {'tabIdx': uiConst.PVP_BG_V2_TAB_BATTLE_FIELD,
          'tabName': 'bfTabBtn',
          'view': 'PvpBattleFieldV2Widget',
          'proxy': 'pvpBattleFieldV2'},
         {'tabIdx': uiConst.PVP_BG_V2_TAB_ARENA,
          'tabName': 'arenaTabBtn',
          'view': 'PvpArenaV2Widget',
          'proxy': 'pvpArenaV2'},
         {'tabIdx': uiConst.PVP_BG_V2_TAB_PLAYOFFS,
          'tabName': 'playoffsBtn',
          'view': 'PvpPlayoffsV2Widget',
          'proxy': 'pvpPlayoffsV2'},
         {'tabIdx': uiConst.PVP_BG_V2_TAB_BALANCE_ARENA_2PERSON,
          'tabName': 'arena2PersonBtn',
          'view': 'BalanceArena2PersonWidget',
          'proxy': 'balanceArena2Person'},
         {'tabIdx': uiConst.PVP_BG_V2_TAB_BALANCE_PLAYOFFS,
          'tabName': 'arenaBalance',
          'view': 'BalanceArenaPlayoffsWidget',
          'proxy': 'balanceArenaPlayoffs'},
         {'tabIdx': uiConst.PVP_BG_V2_TAB_5V5_PLAYOFFS,
          'tabName': 'playoffs5V5Btn',
          'view': 'PvpPlayoffs5V5Widget',
          'proxy': 'pvpPlayoffs5V5'},
         {'tabIdx': uiConst.PVP_BG_V2_TAB_PUBG,
          'tabName': 'pubgBtn',
          'view': 'PvpPUBGWidget',
          'proxy': 'pvpPUBG'}]

    def initUI(self):
        p = BigWorld.player()
        self.initTabUI()
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.setTabVisible(uiConst.PVP_BG_V2_TAB_PLAYOFFS, self.enableArenaPlayoffs(), False)
        self.setTabVisible(uiConst.PVP_BG_V2_TAB_ARENA, gameglobal.rds.configData.get('enableArenaApply', False) and not gameglobal.rds.configData.get('hidePvpArenaPanel', False), False)
        self.setTabVisible(uiConst.PVP_BG_V2_TAB_TODAY_BATTLE_FIELD, gameglobal.rds.configData.get('enableBfTodayActivity', False), False)
        self.setTabVisible(uiConst.PVP_BG_V2_TAB_BALANCE_ARENA_2PERSON, gameglobal.rds.configData.get('enableDoubleArena', False), False)
        self.setTabVisible(uiConst.PVP_BG_V2_TAB_BALANCE_PLAYOFFS, gameglobal.rds.configData.get('enableArenaScore', False), False)
        self.setTabVisible(uiConst.PVP_BG_V2_TAB_5V5_PLAYOFFS, gameglobal.rds.configData.get('enablePlayoffs5V5', False), False)
        self.setTabVisible(uiConst.PVP_BG_V2_TAB_PUBG, gameglobal.rds.ui.pvpPUBG.isPUBGValid(), False)
        self.relayoutTab()
        if self.widget.playoffsBtn:
            self.widget.playoffsBtn.enabled = not BigWorld.player()._isSoul()

    def refreshTab(self):
        if self.widget:
            index1 = self.currentTabIndex
            index2 = self.fbMode
            self.hide()
            gameglobal.rds.ui.pvPPanel.pvpPanelShow(index1, index2)

    def toggle(self, tabIdx = 1, fbMode = 1):
        if self.widget:
            self.hide()
        else:
            self.pvpPanelShow(tabIdx, fbMode)

    def enableArenaPlayoffs(self):
        return gameglobal.rds.configData.get('enableArenaPlayoffs', False)

    def clearWidget(self):
        super(PvPPanelProxy, self).clearWidget()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_PVP_BG_V2)

    def reset(self):
        super(PvPPanelProxy, self).reset()

    def setApply(self, tab):
        self.applyTab = tab

    def getApply(self):
        return self.applyTab
