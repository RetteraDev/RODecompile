#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/backflowProxy.o
import BigWorld
import gameglobal
import uiConst
import utils
from Scaleform import GfxValue
from asObject import RedPotManager
from uiTabProxy import UITabProxy
from guis.asObject import TipManager
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD
RED_POT_W = 159
RED_POT_H = 0
BACKFLOW_TAB_INDEX0 = 0
BACKFLOW_TAB_INDEX1 = 1
BACKFLOW_TAB_INDEX2 = 2
BACKFLOW_ERROR_TBA_INDEX = -1

class BackflowProxy(UITabProxy):

    def __init__(self, uiAdapter):
        super(BackflowProxy, self).__init__(uiAdapter)
        uiAdapter.registerEscFunc(uiConst.WIDGET_BACK_FLOW, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_BACK_FLOW:
            self.widget = widget
            self.initUI()
            self.widget.setTabIndex(self.showTabIndex)

    def clearWidget(self):
        super(BackflowProxy, self).clearWidget()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BACK_FLOW)
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()

    def reset(self):
        super(BackflowProxy, self).reset()

    def _getTabList(self):
        return [{'tabIdx': BACKFLOW_TAB_INDEX0,
          'tabName': 'catchExpTabBtn',
          'view': 'BackflowCatchExpWidget',
          'proxy': 'backflowCatchExp'}, {'tabIdx': BACKFLOW_TAB_INDEX1,
          'tabName': 'priviegeTabBtn',
          'view': 'BackflowPriviegeWidget',
          'proxy': 'backflowPriviege'}, {'tabIdx': BACKFLOW_TAB_INDEX2,
          'tabName': 'discountTabBtn',
          'view': 'BackflowDiscountWidget',
          'proxy': 'backflowDiscount'}]

    def show(self):
        p = BigWorld.player()
        if not gameglobal.rds.configData.get('enableFlowbackGroup', False):
            p.showGameMsg(GMDD.data.BACKFLOW_ACTIVITY_NONE_CONFIG, ())
            return
        if not self.checkBackflowInTime():
            p.showGameMsg(GMDD.data.BACKFLOW_ACTIVITY_NOT_IN_TIME, ())
            return
        if self.getTabIndex() == BACKFLOW_ERROR_TBA_INDEX:
            return
        self.showTabIndex = self.getTabIndex()
        if self.widget:
            self.widget.setTabIndex(self.showTabIndex)
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_BACK_FLOW)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.initTabUI()
        RedPotManager.addRedPot(self.widget.catchExpTabBtn, uiConst.BACK_FLOW_CATCH_EXP_RED_POT, (RED_POT_W, RED_POT_H), self.visiblePotFunC)
        RedPotManager.addRedPot(self.widget.priviegeTabBtn, uiConst.BACK_FLOW_PRIVIEGE_RED_POT, (RED_POT_W, RED_POT_H), self.visiblePotFunP)
        RedPotManager.addRedPot(self.widget.discountTabBtn, uiConst.BACK_FLOW_DISCOUNT_RED_POT, (RED_POT_W, RED_POT_H), self.visiblePotFunD)
        p = BigWorld.player()
        rechargeOp = p.flowbackGroupBonus.rechargeOp
        self.widget.discountTabBtn.visible = True if rechargeOp else False

    def onTabChanged(self, *args):
        super(BackflowProxy, self).onTabChanged(*args)
        self.refreshInfo()

    def refreshInfo(self):
        if not self.widget:
            return
        gameglobal.rds.ui.backflowCatchExp.updateRedPot()
        gameglobal.rds.ui.backflowPriviege.updateRedPot()
        gameglobal.rds.ui.backflowDiscount.updateRedPot()
        self.updateBackflowTimeEnd(self.widget.catchExpTabBtn, gameglobal.rds.ui.backflowCatchExp.checkTimeEnd())
        self.updateBackflowTimeEnd(self.widget.priviegeTabBtn, gameglobal.rds.ui.backflowPriviege.checkTimeEnd())
        self.updateBackflowTimeEnd(self.widget.discountTabBtn, gameglobal.rds.ui.backflowDiscount.checkTimeEnd())
        proxy = self.getCurrentProxy()
        if proxy and hasattr(proxy, 'refreshInfo'):
            proxy.refreshInfo()

    def checkRedFlag(self):
        isRedPot = gameglobal.rds.ui.backflowCatchExp.checkRedPoint() or gameglobal.rds.ui.backflowPriviege.checkRedPoint() or gameglobal.rds.ui.backflowDiscount.checkRedPoint()
        return isRedPot

    def visiblePotFunC(self, *args):
        isRedPot = gameglobal.rds.ui.backflowCatchExp.checkRedPoint()
        return GfxValue(isRedPot)

    def visiblePotFunP(self, *args):
        isRedPot = gameglobal.rds.ui.backflowPriviege.checkRedPoint()
        return GfxValue(isRedPot)

    def visiblePotFunD(self, *args):
        isRedPot = gameglobal.rds.ui.backflowDiscount.checkRedPoint()
        return GfxValue(isRedPot)

    def updateBackflowTimeEnd(self, tabBtn, isEnd):
        tip = SCD.data.get('flowbackTimeEndTip', '')
        if isEnd:
            tabBtn.disabled = True
            TipManager.addTip(tabBtn, tip)
        else:
            tabBtn.disabled = False
            TipManager.removeTip(tabBtn)

    def checkBackflowTimeEnd(self):
        isEnd = gameglobal.rds.ui.backflowCatchExp.checkTimeEnd() and gameglobal.rds.ui.backflowPriviege.checkTimeEnd() and gameglobal.rds.ui.backflowDiscount.checkTimeEnd()
        return isEnd

    def checkBackflow(self):
        p = BigWorld.player()
        flowbackGroupType = p.flowbackGroupBonus.flowbackGroupType
        endTime = p.flowbackGroupBonus.endTime
        if not flowbackGroupType or endTime < utils.getNow():
            return False
        return True

    def checkBackflowInTime(self):
        p = BigWorld.player()
        startTime = p.flowbackGroupBonus.startTime
        endTime = p.flowbackGroupBonus.endTime
        nowTime = utils.getNow()
        if nowTime >= startTime and nowTime <= endTime:
            return True
        return False

    def getTabIndex(self):
        p = BigWorld.player()
        rechargeOp = p.flowbackGroupBonus.rechargeOp
        targetsStateInfo = p.flowbackGroupBonus.targetsStateInfo
        privilegesInfo = p.flowbackGroupBonus.privilegesInfo
        if not gameglobal.rds.ui.backflowCatchExp.checkTimeEnd() and targetsStateInfo:
            return BACKFLOW_TAB_INDEX0
        if not gameglobal.rds.ui.backflowPriviege.checkTimeEnd() and privilegesInfo:
            return BACKFLOW_TAB_INDEX1
        if not gameglobal.rds.ui.backflowDiscount.checkTimeEnd() and rechargeOp:
            return BACKFLOW_TAB_INDEX2
        return BACKFLOW_ERROR_TBA_INDEX
