#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/pvpMasteryCatchUpProxy.o
import BigWorld
import events
import uiConst
import uiUtils
import gametypes
import gameglobal
from uiProxy import UIProxy
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD

class PvpMasteryCatchUpProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PvpMasteryCatchUpProxy, self).__init__(uiAdapter)
        self.widget = None
        self.school = 0
        self.eType = 0
        self.myAverage = 0
        self.targetAverage = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_PVP_MASTERY_CATCHUP, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_PVP_MASTERY_CATCHUP:
            self.widget = widget
            self.initUI()

    def show(self, school, eType):
        if not gameglobal.rds.configData.get('enablePursuePvp', False):
            return
        self.school = school
        self.eType = eType
        if self.widget:
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_PVP_MASTERY_CATCHUP)

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_PVP_MASTERY_CATCHUP)

    def reset(self):
        self.school = 0
        self.eType = 0
        self.myAverage = 0
        self.targetAverage = 0

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.useOneBtn.addEventListener(events.BUTTON_CLICK, self.handleClickUseOne, False, 0, True)
        self.widget.useAllBtn.addEventListener(events.BUTTON_CLICK, self.handleClickUseAll, False, 0, True)
        self.refreshInfo()

    def handleClickUseOne(self, *args):
        p = BigWorld.player()
        if gameglobal.rds.ui.pvpEnhance.canLvUp(self.eType, self.school):
            p.showGameMsg(GMDD.data.PVP_ENHANCE_ADD_EXP_ERROR_ENOUGH_EXP, ())
            return
        itemId = SCD.data.get('pvpLevelChaseItem', 0)
        itemNum = p.inv.countItemInPages(itemId, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck=True)
        if itemNum <= 0:
            p.showGameMsg(GMDD.data.PVP_CATCHUP_ADD_EXP_ERROR_NO_ITEM, ())
            return
        p.cell.addPvpEnh(self.school, self.eType, itemId, 1, 1)

    def handleClickUseAll(self, *args):
        p = BigWorld.player()
        if gameglobal.rds.ui.pvpEnhance.canLvUp(self.eType, self.school):
            p.showGameMsg(GMDD.data.PVP_ENHANCE_ADD_EXP_ERROR_ENOUGH_EXP, ())
            return
        itemId = SCD.data.get('pvpLevelChaseItem', 0)
        itemNum = p.inv.countItemInPages(itemId, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck=True)
        if itemNum <= 0:
            p.showGameMsg(GMDD.data.PVP_CATCHUP_ADD_EXP_ERROR_NO_ITEM, ())
            return
        itemNum = min(itemNum, p.maxPursuePvpEnhNum - p.curPursuePvpEnhNum)
        p.cell.addPvpEnh(self.school, self.eType, itemId, itemNum, 1)

    def refreshInfo(self):
        self.myAverage, self.targetAverage = uiUtils.getPvpMasteryAverageValue(self.school, self.eType)
        p = BigWorld.player()
        if p.maxPursuePvpEnhNum == 0:
            self.widget.gotoAndStop('catchUp')
            self.refreshAverageValue()
        else:
            self.widget.gotoAndStop('noCatchUp')
            self.refreshAverageValue()
            self.refreshConsumeItemInfo()

    def refreshAverageValue(self):
        if self.myAverage > self.targetAverage:
            self.widget.symbol.gotoAndStop('larger')
        elif self.myAverage == self.targetAverage:
            self.widget.symbol.gotoAndStop('equal')
        else:
            self.widget.symbol.gotoAndStop('less')
        self.widget.myAverage.text = str('%.2f' % self.myAverage)
        self.widget.targetAverage.text = str('%.2f' % self.targetAverage)

    def refreshConsumeItemInfo(self):
        p = BigWorld.player()
        itemId = SCD.data.get('pvpLevelChaseItem', 0)
        itemInfo = uiUtils.getGfxItemById(itemId)
        itemNum = p.inv.countItemInPages(itemId)
        itemInfo['count'] = str(itemNum)
        if not itemNum:
            itemInfo['state'] = uiConst.COMPLETE_ITEM_LEAKED
        else:
            itemInfo['state'] = uiConst.ITEM_NORMAL
        self.widget.consumeSlot.dragable = False
        self.widget.consumeSlot.setItemSlotData(itemInfo)
        times = p.maxPursuePvpEnhNum - p.curPursuePvpEnhNum
        maxTimes = p.maxPursuePvpEnhNum
        self.widget.valueTimes.text = str('%d/%d' % (times, maxTimes))
        if p.curPursuePvpEnhNum == p.maxPursuePvpEnhNum:
            self.widget.useOneBtn.enabled = False
            self.widget.useAllBtn.enabled = False
        else:
            self.widget.useOneBtn.enabled = True
            self.widget.useAllBtn.enabled = True
