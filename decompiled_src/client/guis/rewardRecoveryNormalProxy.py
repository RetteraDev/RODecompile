#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/rewardRecoveryNormalProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import gametypes
from callbackHelper import Functor
import gamelog
from gamestrings import gameStrings
from uiProxy import UIProxy
from guis import uiUtils
from guis.asObject import ASUtils
from data import fame_data as FD
TEXT_COLOR_RED = '#F43804'

class RewardRecoveryNormalProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(RewardRecoveryNormalProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_REWARD_RECOVERY_CHOOSE, self.hide)

    def reset(self):
        self.itemData = {}
        self.selectedMc = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_REWARD_RECOVERY_CHOOSE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_REWARD_RECOVERY_CHOOSE)

    def show(self, itemData):
        if not itemData:
            return
        self.itemData = itemData
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_REWARD_RECOVERY_CHOOSE)
        else:
            self.refreshInfo()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.fame0.icon.gotoAndStop('yunChui')
        self.widget.fame1.icon.gotoAndStop('gongJiDian')
        p = BigWorld.player()
        if not self.itemData.has_key('costList'):
            self.hide()
            return
        consumeFame0, consumeFame1 = self.itemData['costList']
        fameName0 = FD.data.get(453, {}).get('name', '')
        fameName1 = FD.data.get(420, {}).get('name', '')
        self.widget.fame0.costTxt.text = gameStrings.WELFARE_REWARD_COST_TXT % (int(consumeFame0[1]), fameName0)
        self.widget.fame1.costTxt.text = gameStrings.WELFARE_REWARD_COST_TXT % (int(consumeFame1[1]), fameName1)
        self.widget.fame0.remainTxt.text = gameStrings.WELFARE_REWARD_REMAIN_TXT % p.fame.get(453, 0)
        self.widget.fame1.remainTxt.text = gameStrings.WELFARE_REWARD_REMAIN_TXT % p.fame.get(420, 0)
        fame0CanSelect = p.fame.get(453, 0) >= consumeFame0[1]
        fame1CanSelect = p.fame.get(420, 0) >= consumeFame1[1]
        if fame0CanSelect:
            ASUtils.setMcEffect(self.widget.fame0, 'normal')
            ASUtils.setHitTestDisable(self.widget.fame0, False)
            if not self.selectedMc:
                self.selectedMc = self.widget.fame0
                self.selectedMc.gotoAndStop('over')
        else:
            ASUtils.setMcEffect(self.widget.fame0, 'grey')
            ASUtils.setHitTestDisable(self.widget.fame0, True)
            self.widget.fame0.remainTxt.htmlText = uiUtils.toHtml(self.widget.fame0.remainTxt.text, TEXT_COLOR_RED)
        if fame1CanSelect:
            ASUtils.setHitTestDisable(self.widget.fame1, False)
            if not self.selectedMc:
                self.selectedMc = self.widget.fame1
                self.selectedMc.gotoAndStop('over')
        else:
            ASUtils.setHitTestDisable(self.widget.fame1, True)
            self.widget.fame1.remainTxt.htmlText = uiUtils.toHtml(self.widget.fame1.remainTxt.text, TEXT_COLOR_RED)
        if fame0CanSelect or fame1CanSelect:
            self.widget.yseBtn.enabled = True
            self.widget.yseBtn.addEventListener(events.BUTTON_CLICK, self.handleYesBtnClick, False, 0, True)
        else:
            self.widget.yseBtn.enabled = False
        self.widget.noBtn.addEventListener(events.BUTTON_CLICK, self.handleNoBtnClick, False, 0, True)
        self.widget.fame0.addEventListener(events.MOUSE_CLICK, self.handleItem0Click, False, 0, True)
        self.widget.fame1.addEventListener(events.MOUSE_CLICK, self.handleItem1Click, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return

    def handleItem0Click(self, *args):
        self.selectedMc.gotoAndStop('up')
        self.selectedMc = self.widget.fame0
        self.selectedMc.gotoAndStop('over')

    def handleItem1Click(self, *args):
        self.selectedMc.gotoAndStop('up')
        self.selectedMc = self.widget.fame1
        self.selectedMc.gotoAndStop('over')

    def handleYesBtnClick(self, *args):
        if not self.selectedMc:
            return
        if self.selectedMc.name == 'fame0':
            if self.itemData['activityType'] != gametypes.REWARD_RECOVER_ACTIVITY_TYPE_XUN_LING:
                gamelog.info('jbx:getBackActivityRewardEx', int(self.itemData['activityId']), gametypes.ACTIVITY_REWARD_RECOVERY_TYPE_FAME2)
                fun = Functor(BigWorld.player().base.getBackActivityRewardEx, int(self.itemData['activityId']), gametypes.ACTIVITY_REWARD_RECOVERY_TYPE_FAME2)
            else:
                fun = Functor(BigWorld.player().cell.getBackQuestLoopChainExp, gametypes.QUEST_LOOP_CHAIN_GET_BACK_EXP_TYPE_FAME2)
        elif self.selectedMc.name == 'fame1':
            if self.itemData['activityType'] != gametypes.REWARD_RECOVER_ACTIVITY_TYPE_XUN_LING:
                gamelog.info('jbx:getBackActivityRewardEx', int(self.itemData['activityId']), gametypes.ACTIVITY_REWARD_RECOVERY_TYPE_FAME1)
                fun = Functor(BigWorld.player().base.getBackActivityRewardEx, int(self.itemData['activityId']), gametypes.ACTIVITY_REWARD_RECOVERY_TYPE_FAME1)
            else:
                fun = Functor(BigWorld.player().cell.getBackQuestLoopChainExp, gametypes.QUEST_LOOP_CHAIN_GET_BACK_EXP_TYPE_FAME1)
        self.uiAdapter.welfareRewardRecovery.getBackActivityReward(fun, self.itemData)
        self.hide()

    def handleNoBtnClick(self, *args):
        self.hide()
