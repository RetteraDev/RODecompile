#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/lunZhanYunDianProxy.o
import BigWorld
import gameglobal
import uiConst
import uiUtils
import events
import const
import formula
import utils
import gametypes
from uiTabProxy import UITabProxy
from gamestrings import gameStrings
from callbackHelper import Functor
from data import sys_config_data as SCD
from data import arena_mode_data as AMD
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD
TAB_REPORT = 0
TAB_INTRO = 1
MAX_ROUND = 6

class LunZhanYunDianProxy(UITabProxy):

    def __init__(self, uiAdapter):
        super(LunZhanYunDianProxy, self).__init__(uiAdapter)
        self.tabType = UITabProxy.TAB_TYPE_CLS
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_LUNZHAN_YUNDIAN, self.hide)

    def reset(self):
        super(LunZhanYunDianProxy, self).reset()
        self.arenaMode = None
        self.widget = None
        self.round = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_LUNZHAN_YUNDIAN:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        super(LunZhanYunDianProxy, self).clearWidget()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_LUNZHAN_YUNDIAN)

    def _getTabList(self):
        return [{'tabIdx': TAB_REPORT,
          'tabName': 'reportTab',
          'view': 'LunZhanYunDian_reportPanel',
          'pos': (158, 168)}, {'tabIdx': TAB_INTRO,
          'tabName': 'introTab',
          'view': 'LunZhanYunDian_introPanel',
          'pos': (158, 168)}]

    def show(self, showTabIndex = 0):
        p = BigWorld.player()
        self.arenaMode = self.getArenaMode()
        if not self.widget:
            self.showTabIndex = showTabIndex
            self.uiAdapter.loadWidget(uiConst.WIDGET_LUNZHAN_YUNDIAN)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.helpIcon.helpKey = SCD.data.get('lunZhanYunDianHelpKey', 0)
        self.initTabUI()
        self.widget.setTabIndex(self.showTabIndex)
        self.widget.personBtn.addEventListener(events.BUTTON_CLICK, self.handlePersonBtnClick, False, 0, True)
        self.widget.teamBtn.addEventListener(events.BUTTON_CLICK, self.handleTeamBtnClick, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        if not self.currentView:
            return
        recordInfo = BigWorld.player().lunZhanYunDianInfo
        if not recordInfo:
            return
        self.arenaMode = self.getArenaMode()
        if self.currentTabIndex == TAB_REPORT:
            self.refreshReportPanel()
        elif self.currentTabIndex == TAB_INTRO:
            arenaData = AMD.data.get(self.arenaMode, {})
            self.currentView.introTitle.text = gameStrings.LZYD_INTRO_TITLE
            self.currentView.introDesc.htmlText = arenaData.get('introDesc', '')
        startTime, endTime, _ = gameglobal.rds.ui.LZYDPush.getTime()
        if startTime <= utils.getNow() <= endTime or not gameglobal.rds.configData.get('enableDuelTimeCheck', False):
            self.widget.personBtn.enabled = True
            self.widget.teamBtn.enable = True
        else:
            self.widget.personBtn.enabled = False
            self.widget.teamBtn.enabled = False
        applyTime = recordInfo.lzydApplyTime
        applyType = recordInfo.lzydApplyType
        if applyTime and utils.isSameWeek(applyTime, utils.getNow()):
            if gameglobal.rds.configData.get('enableDuelTimeCheck', False):
                self.widget.personBtn.enabled = False
                self.widget.teamBtn.enabled = False
            if applyType and applyType == gametypes.LUN_ZHAN_YUN_DIAN_APPLY_SINGLE:
                self.widget.personBtn.label = gameStrings.LZYD_BTN_DISABLE
                self.widget.teamBtn.label = gameStrings.LZYD_BTN_TEAM
            elif applyType and applyType == gametypes.LUN_ZHAN_YUN_DIAN_APPLY_TEAM:
                self.widget.personBtn.label = gameStrings.LZYD_BTN_SINGLE
                self.widget.teamBtn.label = gameStrings.LZYD_BTN_DISABLE

    def getArenaMode(self):
        p = BigWorld.player()
        arenaMode = 0
        LZYDServerProgress = SCD.data.get('LZYDServerProgress', [])
        if not LZYDServerProgress:
            return
        if not p.isServerProgressFinished(LZYDServerProgress[0]):
            if p.lv >= 40:
                arenaMode = const.ARENA_MODE_40_LUN_ZHAN_YUN_DIAN
        elif not p.isServerProgressFinished(LZYDServerProgress[1]):
            if p.lv >= 60:
                arenaMode = const.ARENA_MODE_60_LUN_ZHAN_YUN_DIAN
        elif not p.isServerProgressFinished(LZYDServerProgress[2]):
            if p.lv >= 60 and p.lv <= 69:
                arenaMode = const.ARENA_MODE_CROSS_LUN_ZHAN_YUN_DIAN
            elif p.lv >= 70:
                arenaMode = const.ARENA_MODE_60_LUN_ZHAN_YUN_DIAN
        elif p.lv >= 60:
            arenaMode = const.ARENA_MODE_CROSS_LUN_ZHAN_YUN_DIAN
        return arenaMode

    def refreshReportPanel(self):
        if not self.widget:
            return
        if not self.currentView:
            return
        p = BigWorld.player()
        recordInfo = p.lunZhanYunDianInfo
        if not recordInfo:
            return
        arenaData = AMD.data.get(self.arenaMode, {})
        matchTimes = arenaData.get('matchTimes', [])
        if not matchTimes:
            return
        self.round = gameglobal.rds.ui.LZYDPush.round
        _, endTime, _ = gameglobal.rds.ui.LZYDPush.getTime()
        panel = self.currentView
        if utils.getNow() > endTime:
            self.widget.roundDesc.text = gameStrings.LZYD_ROUND_END
            self.widget.nextTime.visible = False
        else:
            self.widget.nextTime.visible = True
            if self.round == 0:
                self.widget.roundDesc.text = gameStrings.LZYD_ROUND_NOT_OPEN
            else:
                self.widget.roundDesc.text = gameStrings.LZYD_ROUND_DESC % self.round
        if self.round == len(matchTimes):
            self.widget.nextTime.visible = False
        else:
            self.widget.nextTime.visible = True
            timeStr = utils.formatCustomTime(int(utils.getNextCrontabTime(matchTimes[self.round])), '%H:%M')
            timeDesc = gameStrings.LZYD_NEXT_ROUND_DESC % timeStr
            self.widget.nextTime.htmlText = timeDesc
        panel.roundCnt.text = gameStrings.LZYD_ROUND_COUNT_DESC % recordInfo.victoryRound
        panel.damage.text = gameStrings.LZYD_DAMAGE_DESC % recordInfo.damage
        panel.treatment.text = gameStrings.LZYD_TREATMENT_DESC % recordInfo.cure
        panel.kill.text = gameStrings.LZYD_KILL_DESC % recordInfo.killCount
        panel.assist.text = gameStrings.LZYD_ASSIST_DESC % recordInfo.assistCount
        victoryRoundReward = arenaData.get('victoryRoundReward', [])
        if victoryRoundReward:
            currentReward = victoryRoundReward[recordInfo.victoryRound][0]
            nextReward = victoryRoundReward[min(recordInfo.victoryRound + 1, MAX_ROUND)][0]
            panel.nextItem.visible = recordInfo.victoryRound < MAX_ROUND
            panel.slot0.setItemSlotData(uiUtils.getGfxItemById(currentReward, 1))
            panel.slot0.dragable = False
            panel.nextItem.slot1.setItemSlotData(uiUtils.getGfxItemById(nextReward, 1))
            panel.nextItem.slot1.dragable = False
        panel.currentTxt.text = gameStrings.LZYD_CURRENT_DESC
        panel.nextItem.nextTxt.text = gameStrings.LZYD_NEXT_DESC
        panel.rewardBtn.addEventListener(events.BUTTON_CLICK, self.handleRewardBtnClick, False, 0, True)

    def onTabChanged(self, *args):
        super(LunZhanYunDianProxy, self).onTabChanged(*args)
        self.refreshInfo()

    def handleRewardBtnClick(self, *args):
        gameglobal.rds.ui.generalReward.show(gametypes.GENERAL_REWARD_LZYD)

    def handlePersonBtnClick(self, *args):
        round = min(self.round + 1, MAX_ROUND)
        msg = GMD.data.get(GMDD.data.APPLY_LZYD_SINGLE_CONFIRM, {}).get('text', '') % (round, MAX_ROUND - round)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(BigWorld.player().cell.applyLunZhanYunDianCell, self.arenaMode))

    def handleTeamBtnClick(self, *args):
        round = min(self.round + 1, MAX_ROUND)
        msg = GMD.data.get(GMDD.data.APPLY_LZYD_SINGLE_CONFIRM, {}).get('text', '') % (round, MAX_ROUND - round)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(BigWorld.player().cell.applyLzydOfTeamCell, self.arenaMode))
