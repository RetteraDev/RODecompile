#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/yaoPeiFeedCatchUpProxy.o
import BigWorld
import events
import uiConst
import uiUtils
import gametypes
import gameglobal
import utils
import const
import math
from uiProxy import UIProxy
from data import item_data as ID
from data import sys_config_data as SCD
from cdata import yaopei_lv_exp_data as YLED
from cdata import pursue_yaopei_data as PYD
from cdata import game_msg_def_data as GMDD
from cdata import yaopei_lv_data as YLD
USE_ONE_ITEM_ADD_EXP = 100

class YaoPeiFeedCatchUpProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(YaoPeiFeedCatchUpProxy, self).__init__(uiAdapter)
        self.widget = None
        self.srcIt = None
        self.resPos = None
        self.resKind = 0
        self.lvMap = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_YAOPEI_FEED_CATCHUP, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_YAOPEI_FEED_CATCHUP:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def show(self):
        if not gameglobal.rds.configData.get('enablePursueYaopei', False):
            return
        if self.widget:
            return
        self.uiAdapter.loadWidget(uiConst.WIDGET_YAOPEI_FEED_CATCHUP)

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_YAOPEI_FEED_CATCHUP)

    def reset(self):
        self.srcIt = None
        self.resPos = None
        self.resKind = 0

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.useOneBtn.addEventListener(events.BUTTON_CLICK, self.handleClickUseOne, False, 0, True)
        self.widget.useAllBtn.addEventListener(events.BUTTON_CLICK, self.handleClickUseAll, False, 0, True)

    def handleClickUseOne(self, *args):
        p = BigWorld.player()
        itemId = SCD.data.get('amuletLevelChaseItem', 0)
        itemNum = p.inv.countItemInPages(itemId, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck=True)
        if itemNum <= 0:
            p.showGameMsg(GMDD.data.YAO_PEI_CATCHUP_ADD_EXP_ERROR_NO_ITEM, ())
            return
        newLv = uiUtils.calcYaoPeiLv(self.srcIt.quality, self.srcIt.yaoPeiExp + USE_ONE_ITEM_ADD_EXP)
        newLvReqUp = ID.data.get(self.srcIt.id, {}).get('lvReq', 0) + YLD.data.get(newLv, {}).get('lvReqUp', 0)
        if newLvReqUp > p.lv:
            p.showGameMsg(GMDD.data.YAOPEI_CAN_TAKE_OLREADY_LARGEST_LV, ())
            return
        gameglobal.rds.ui.yaoPeiFeed.updateOldLv()
        items = []
        items.append(itemId)
        itemNums = [1]
        p.cell.addYaoPeiExp(self.resKind, self.resPos[0], self.resPos[1], items, itemNums)

    def handleClickUseAll(self, *args):
        p = BigWorld.player()
        itemId = SCD.data.get('amuletLevelChaseItem', 0)
        itemNum = p.inv.countItemInPages(itemId, bindPolicy=gametypes.ITEM_REMOVE_POLICY_BIND_FIRST, enableParentCheck=True)
        if itemNum <= 0:
            p.showGameMsg(GMDD.data.YAO_PEI_CATCHUP_ADD_EXP_ERROR_NO_ITEM, ())
            return
        usedTimes, maxTimes = self.srcIt.getYaoPeiPursueNum()
        itemNum = min(itemNum, maxTimes - usedTimes)
        newLv = uiUtils.calcYaoPeiLv(self.srcIt.quality, self.srcIt.yaoPeiExp + itemNum * USE_ONE_ITEM_ADD_EXP)
        newLvReqUp = ID.data.get(self.srcIt.id, {}).get('lvReq', 0) + YLD.data.get(newLv, {}).get('lvReqUp', 0)
        if newLvReqUp > p.lv and self.lvMap:
            yaoPeiLimitLv = self.lvMap[p.lv]
            yaoPeiLimitExp = YLED.data.get((self.srcIt.quality, yaoPeiLimitLv + 1), {}).get('exp', 0)
            yaoPeiDiffExp = max(yaoPeiLimitExp - self.srcIt.yaoPeiExp, 0)
            itemNum = math.floor(yaoPeiDiffExp / USE_ONE_ITEM_ADD_EXP)
            if itemNum == 0:
                p.showGameMsg(GMDD.data.YAOPEI_CAN_TAKE_OLREADY_LARGEST_LV, ())
                return
        gameglobal.rds.ui.yaoPeiFeed.updateOldLv()
        items = []
        items.append(itemId)
        itemNums = []
        itemNums.append(itemNum)
        p.cell.addYaoPeiExp(self.resKind, self.resPos[0], self.resPos[1], items, itemNums)

    def refreshInfo(self):
        p = BigWorld.player()
        self.resKind, self.resPos = gameglobal.rds.ui.yaoPeiFeed.getYaoPeiInfo()
        if self.resKind == const.RES_KIND_INV:
            if self.resPos:
                self.srcIt = p.inv.getQuickVal(self.resPos[0], self.resPos[1])
            else:
                self.srcIt = None
        else:
            self.srcIt = p.equipment[gametypes.EQU_PART_YAOPEI]
        if not self.srcIt:
            return
        else:
            if not self.lvMap:
                self.lvMap = {}
                for lv in YLD.data:
                    pLv = ID.data.get(self.srcIt.id, {}).get('lvReq', 0) + YLD.data.get(lv, {}).get('lvReqUp', 0)
                    self.lvMap[pLv] = lv

            usedTimes, maxTimes = self.srcIt.getYaoPeiPursueNum()
            if maxTimes == 0:
                self.widget.gotoAndStop('catchUp')
                self.refreshAverageValue()
            else:
                self.widget.gotoAndStop('noCatchUp')
                self.refreshAverageValue()
                self.refreshConsumeItemInfo()
            return

    def getYaoPeiAverageValueInfo(self):
        if not self.srcIt:
            return
        quality = getattr(self.srcIt, 'quality', 0)
        yaoPeiExp = getattr(self.srcIt, 'yaoPeiExp', 0)
        weekDiff = uiUtils.getCatchUpWeekDiff('ypInterval')
        yaoPeiTargetExp = PYD.data.get(weekDiff, {}).get('standard' + str(self.srcIt.quality), 0)
        if yaoPeiTargetExp != 0:
            targetAverage = self.getAverageValue(quality, yaoPeiTargetExp)
        else:
            targetAverage = 0
        myAverage = self.getAverageValue(quality, yaoPeiExp)
        return (myAverage, targetAverage)

    def refreshAverageValue(self):
        myAverage, targetAverage = self.getYaoPeiAverageValueInfo()
        if myAverage > targetAverage:
            self.widget.symbol.gotoAndStop('larger')
        elif myAverage == targetAverage:
            self.widget.symbol.gotoAndStop('equal')
        else:
            self.widget.symbol.gotoAndStop('less')
        self.widget.myAverage.text = str('%.2f' % myAverage)
        self.widget.targetAverage.text = str('%.2f' % targetAverage)

    def refreshConsumeItemInfo(self):
        p = BigWorld.player()
        itemId = SCD.data.get('amuletLevelChaseItem', 0)
        itemInfo = uiUtils.getGfxItemById(itemId)
        itemNum = p.inv.countItemInPages(itemId)
        itemInfo['count'] = str(itemNum)
        if not itemNum:
            itemInfo['state'] = uiConst.COMPLETE_ITEM_LEAKED
        else:
            itemInfo['state'] = uiConst.ITEM_NORMAL
        self.widget.consumeSlot.dragable = False
        if not self.widget.consumeSlot.data:
            self.widget.consumeSlot.setItemSlotData(itemInfo)
        else:
            self.widget.consumeSlot.setValueAmountTxt(str(itemNum))
        if not self.srcIt:
            return
        else:
            usedTimes, maxTimes = self.srcIt.getYaoPeiPursueNum()
            if usedTimes != None and maxTimes != None:
                self.widget.valueTimes.text = str('%d/%d' % (maxTimes - usedTimes, maxTimes))
                if usedTimes == maxTimes:
                    self.widget.useOneBtn.enabled = False
                    self.widget.useAllBtn.enabled = False
                else:
                    self.widget.useOneBtn.enabled = True
                    self.widget.useAllBtn.enabled = True
            return

    def getAverageValue(self, quality, yaoPeiExp):
        lvPre = 0
        lvLast = 0
        maxYaoPeiLv = SCD.data.get('maxYaoPeiLv', 0)
        for lv in range(1, maxYaoPeiLv + 1):
            if yaoPeiExp < YLED.data.get((quality, lv), {}).get('exp', 0):
                lvPre = lv - 1
                lvLast = lv
                break

        if lvPre == 0 and lvLast == 0:
            lvPre = maxYaoPeiLv
            point = 0
        else:
            expPre = YLED.data.get((quality, lvPre), {}).get('exp', 0)
            expLast = YLED.data.get((quality, lvLast), {}).get('exp', 0)
            point = 0
            if expLast - expPre != 0:
                point = (yaoPeiExp - expPre) / float(expLast - expPre)
        arverageValue = round(lvPre + point, 2)
        return arverageValue
