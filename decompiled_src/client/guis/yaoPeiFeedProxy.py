#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/yaoPeiFeedProxy.o
import BigWorld
import gameglobal
import uiConst
import uiUtils
import events
import ui
import const
import commcalc
import gametypes
import utils
from uiProxy import SlotDataProxy
from callbackHelper import Functor
from gameStrings import gameStrings
from data import item_data as ID
from data import sys_config_data as SCD
from cdata import yaopei_lv_data as YLD
from cdata import yaopei_lv_exp_data as YLED
from cdata import game_msg_def_data as GMDD
from cdata import pursue_yaopei_data as PYD
FEED_READY = 1
FEED_WAITING = 2
FEED_FINISH = 3

class YaoPeiFeedProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(YaoPeiFeedProxy, self).__init__(uiAdapter)
        self.bindType = 'yaoPeiFeed'
        self.type = 'yaoPeiFeed'
        self.modelMap = {'init': self.onInit,
         'confirm': self.onConfirm,
         'showLvUp': self.onShowLvUp,
         'getCurCash': self.onGetCurCash,
         'removeItem': self.onRemoveItem,
         'speedUp': self.onSpeedUp,
         'showYaoPeiFeedCatchUp': self.onShowYaoPeiFeedCatchUp}
        self.mediator = None
        self.inBag = True
        self.resPos = None
        self.feedState = FEED_READY
        self.needShowLvUp = False
        self.oldLv = 0
        self.lvUpItem = None
        self.lvUpItemInBag = True
        uiAdapter.registerEscFunc(uiConst.WIDGET_YAOPEI_FEED, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_YAOPEI_FEED:
            self.mediator = mediator
        BigWorld.callback(0.1, gameglobal.rds.ui.inventory.updateCurrentPageSlotState)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_YAOPEI_FEED)
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def reset(self):
        self.feedState = FEED_READY
        if self.needShowLvUp:
            gameglobal.rds.ui.yaoPeiLvUp.show(self.oldLv, self.lvUpItem, self.lvUpItemInBag)
            self.needShowLvUp = False
        self.removeItem(False)

    def show(self):
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_YAOPEI_FEED)
        if not gameglobal.rds.ui.inventory.mediator:
            gameglobal.rds.ui.inventory.show()

    def showInEquip(self):
        self.setItem(uiConst.EQUIP_ACTION_BAR, gametypes.EQU_PART_YAOPEI, False)
        if self.mediator:
            self.mediator.Invoke('swapPanelToFront')
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_YAOPEI_FEED)

    def onInit(self, *arg):
        self.refreshInfo()

    def refreshInfo(self):
        if self.mediator:
            self.feedState = FEED_READY
            p = BigWorld.player()
            info = {}
            srcItem = None
            if self.resPos:
                info['hasRes'] = True
                if self.inBag:
                    srcItem = p.inv.getQuickVal(self.resPos[0], self.resPos[1])
                    location = const.ITEM_IN_BAG
                else:
                    srcItem = p.equipment[gametypes.EQU_PART_YAOPEI]
                    location = const.ITEM_IN_EQUIPMENT
                if not srcItem:
                    return
                info['itemInfo'] = uiUtils.getGfxItem(srcItem, location=location)
                yaoPeiLv = srcItem.getYaoPeiLv()
                info['itemInfo']['count'] = 'Lv.%d' % yaoPeiLv
                nowLvExp = YLED.data.get((srcItem.quality, yaoPeiLv), {}).get('exp', 0)
                maxYaoPeiLv = SCD.data.get('maxYaoPeiLv', 0)
                if yaoPeiLv >= maxYaoPeiLv:
                    info['nowExp'] = 1
                    info['lvMaxExp'] = 1
                    info['allMaxExp'] = 1
                else:
                    info['nowExp'] = srcItem.yaoPeiExp - nowLvExp
                    info['lvMaxExp'] = YLED.data.get((srcItem.quality, yaoPeiLv + 1), {}).get('exp', 0) - nowLvExp
                    info['allMaxExp'] = YLED.data.get((srcItem.quality, maxYaoPeiLv), {}).get('exp', 0) - srcItem.yaoPeiExp
                maxYaoPeiMaterial = SCD.data.get('maxYaoPeiMaterial', 0)
                freeYaoPeiMaterialWeekly = SCD.data.get('freeYaoPeiMaterialWeekly', 0)
                yaoPeiMaterialWeekly = srcItem.getYaoPeiMaterialWeekly()
                if yaoPeiLv >= maxYaoPeiLv:
                    info['extraVisible'] = False
                    info['maxFlagVisible'] = True
                    info['hint'] = uiUtils.getTextFromGMD(GMDD.data.YAOPEI_FEED_MAX_LEVEL_HINT, '')
                elif yaoPeiMaterialWeekly >= maxYaoPeiMaterial:
                    info['extraVisible'] = False
                    info['maxFlagVisible'] = False
                    info['hint'] = uiUtils.getTextFromGMD(GMDD.data.YAOPEI_FEED_WEEK_LIMIT_HINT, '')
                else:
                    info['extraVisible'] = True
                    info['maxFlagVisible'] = False
                    info['freeNum'] = max(freeYaoPeiMaterialWeekly - yaoPeiMaterialWeekly, 0)
                    info['allNum'] = maxYaoPeiMaterial - yaoPeiMaterialWeekly
                    info['weekNum'] = yaoPeiMaterialWeekly
                    yaoPeiFeedItems = SCD.data.get('yaoPeiFeedItems', ())
                    extraItemList = []
                    for itemId in yaoPeiFeedItems:
                        extraItemInfo = uiUtils.getGfxItemById(itemId)
                        extraItemInfo['count'] = str(p.inv.countItemInPages(itemId, enableParentCheck=True))
                        extraItemInfo['expValue'] = ID.data.get(itemId, {}).get('yaoPeiExp', 0)
                        if extraItemInfo['count'] == 0:
                            extraItemInfo['state'] = uiConst.COMPLETE_ITEM_LEAKED
                        else:
                            extraItemInfo['state'] = uiConst.ITEM_NORMAL
                        extraItemList.append(extraItemInfo)

                    info['extraItemList'] = extraItemList
            else:
                info['hasRes'] = False
                info['hint'] = uiUtils.getTextFromGMD(GMDD.data.YAOPEI_FEED_HINT, '')
            if srcItem:
                info['speedUpText'] = gameStrings.CATCH_UP_PROXY_BTN_TEXT
                weekDiff = uiUtils.getCatchUpWeekDiff('ypInterval')
                yaoPeiTargetExp = PYD.data.get(weekDiff, {}).get('standard' + str(srcItem.quality), 0)
                info['showSpeedUp'] = False
                if gameglobal.rds.configData.get('enablePursueYaopei', False) and yaoPeiTargetExp != 0:
                    info['showSpeedUp'] = True
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))
            if gameglobal.rds.ui.yaoPeiFeedCatchUp.widget:
                gameglobal.rds.ui.yaoPeiFeedCatchUp.refreshInfo()

    def updateExtraInfo(self):
        if self.mediator:
            self.feedState = FEED_READY
            self.mediator.Invoke('updateExtraInfo')

    def feedFinish(self, ok, resKind, page, pos):
        if ok:
            self.feedSuccess(resKind, page, pos)
        else:
            self.refreshInfo()

    def feedSuccess(self, resKind, page, pos):
        p = BigWorld.player()
        if resKind == const.RES_KIND_INV:
            item = p.inv.getQuickVal(page, pos)
            self.lvUpItemInBag = True
        else:
            item = p.equipment[gametypes.EQU_PART_YAOPEI]
            self.lvUpItemInBag = False
        if not item:
            return
        self.lvUpItem = item
        yaoPeiLv = item.getYaoPeiLv()
        self.needShowLvUp = yaoPeiLv > self.oldLv
        if self.mediator:
            self.feedState = FEED_FINISH
            info = {}
            nowLvExp = YLED.data.get((item.quality, yaoPeiLv), {}).get('exp', 0)
            maxYaoPeiLv = SCD.data.get('maxYaoPeiLv', 0)
            if yaoPeiLv >= maxYaoPeiLv:
                nowExp = 1
                lvMaxExp = 1
            else:
                nowExp = item.yaoPeiExp - nowLvExp
                lvMaxExp = YLED.data.get((item.quality, yaoPeiLv + 1), {}).get('exp', 0) - nowLvExp
            currentValue = 100.0
            if lvMaxExp > nowExp:
                currentValue = currentValue * nowExp / lvMaxExp
            info['needShowLvUp'] = self.needShowLvUp
            if self.needShowLvUp:
                currentValue = 100.0
            info['currentValue'] = currentValue
            self.mediator.Invoke('feedSuccess', uiUtils.dict2GfxDict(info, True))
            if gameglobal.rds.ui.yaoPeiFeedCatchUp.widget:
                gameglobal.rds.ui.yaoPeiFeedCatchUp.refreshInfo()
        elif self.needShowLvUp:
            gameglobal.rds.ui.yaoPeiLvUp.show(self.oldLv, self.lvUpItem, self.lvUpItemInBag)
            self.needShowLvUp = False

    def updateOldLv(self):
        p = BigWorld.player()
        if self.inBag:
            if self.resPos:
                item = p.inv.getQuickVal(self.resPos[0], self.resPos[1])
            else:
                item = None
        else:
            item = p.equipment[gametypes.EQU_PART_YAOPEI]
        if item:
            self.oldLv = item.getYaoPeiLv()

    def onConfirm(self, *arg):
        addExp = int(arg[3][0].GetNumber())
        itemNums = (int(arg[3][1].GetNumber()), int(arg[3][2].GetNumber()), int(arg[3][3].GetNumber()))
        self.feedState = FEED_WAITING
        yaoPeiFeedItems = SCD.data.get('yaoPeiFeedItems', ())
        p = BigWorld.player()
        if self.inBag:
            item = p.inv.getQuickVal(self.resPos[0], self.resPos[1])
        else:
            item = p.equipment[gametypes.EQU_PART_YAOPEI]
        self.updateOldLv()
        if not hasattr(item, 'yaoPeiExp'):
            return
        newLv = uiUtils.calcYaoPeiLv(item.quality, item.yaoPeiExp + addExp)
        newLvReqUp = ID.data.get(item.id, {}).get('lvReq', 0) + YLD.data.get(newLv, {}).get('lvReqUp', 0)
        if newLvReqUp > p.lv:
            msg = uiUtils.getTextFromGMD(GMDD.data.YAOPEI_FEED_ERROR_LVREQUP_HINT, '')
            gameglobal.rds.ui.messageBox.showMsgBox(msg)
            self.updateExtraInfo()
            return
        isBind = item.isForeverBind()
        yaoPeiMaterialWeekly = item.getYaoPeiMaterialWeekly()
        costCash = self.calcCostCash(yaoPeiMaterialWeekly, itemNums[0] + itemNums[1] + itemNums[2])
        needMessageBox = False
        msg = ''
        if isBind and costCash > 0:
            needMessageBox = True
            msg = uiUtils.getTextFromGMD(GMDD.data.YAOPEI_FEED_CASH_HINT, '%s') % format(costCash, ',')
        elif not isBind and costCash <= 0:
            needMessageBox = True
            msg = uiUtils.getTextFromGMD(GMDD.data.YAOPEI_FEED_UNBIND_TO_BIND_HINT, '')
        elif not isBind and costCash > 0:
            needMessageBox = True
            msg = uiUtils.getTextFromGMD(GMDD.data.YAOPEI_FEED_UNBIND_TO_BIND_AND_CASH_HINT, '%s') % format(costCash, ',')
        if self.inBag:
            resKind = const.RES_KIND_INV
        else:
            resKind = const.RES_KIND_EQUIP
        if needMessageBox:
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.addYaoPeiExp, resKind, self.resPos[0], self.resPos[1], yaoPeiFeedItems, itemNums), noCallback=self.updateExtraInfo)
        else:
            p.cell.addYaoPeiExp(resKind, self.resPos[0], self.resPos[1], yaoPeiFeedItems, itemNums)

    def onShowLvUp(self, *arg):
        if self.needShowLvUp:
            gameglobal.rds.ui.yaoPeiLvUp.show(self.oldLv, self.lvUpItem, self.lvUpItemInBag)
            self.needShowLvUp = False
        self.refreshInfo()

    def onGetCurCash(self, *arg):
        weekNum = int(arg[3][0].GetNumber())
        curNum = int(arg[3][1].GetNumber())
        info = {}
        info['playerCash'] = BigWorld.player().cash
        info['costCash'] = self.calcCostCash(weekNum, curNum)
        return uiUtils.dict2GfxDict(info, True)

    def calcCostCash(self, weekNum, curNum):
        freeMaterialWeekly = SCD.data.get('freeYaoPeiMaterialWeekly', 5)
        ccFormulaId = SCD.data.get('yaoPeiExpCostFormula', 0)
        if ccFormulaId:
            return commcalc._calcFormulaById(ccFormulaId, {'oldNum': weekNum,
             'delta': curNum,
             'freeNum': freeMaterialWeekly})
        else:
            return 0

    def onRemoveItem(self, *arg):
        if self.feedState != FEED_READY:
            return
        self.removeItem(True)

    def getSlotID(self, key):
        return (0, 0)

    def setItem(self, srcBar, srcSlot, inBag):
        if self.feedState != FEED_READY:
            return
        p = BigWorld.player()
        if inBag:
            item = p.inv.getQuickVal(srcBar, srcSlot)
        else:
            item = p.equipment[gametypes.EQU_PART_YAOPEI]
        if item.hasLatch():
            p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
            return
        self.removeItem(False)
        self.inBag = inBag
        self.resPos = (srcBar, srcSlot)
        if self.inBag:
            gameglobal.rds.ui.inventory.updateSlotState(srcBar, srcSlot)
        self.refreshInfo()

    def removeItem(self, needRefresh):
        if self.resPos:
            page, pos = self.resPos
            self.resPos = None
            if self.inBag:
                gameglobal.rds.ui.inventory.updateSlotState(page, pos)
            self.inBag = True
        if needRefresh:
            self.refreshInfo()

    def isItemDisabled(self, kind, page, pos, item):
        if self.mediator and kind == const.RES_KIND_INV:
            if item.isYaoPei():
                if self.inBag:
                    return (page, pos) == self.resPos
                else:
                    return False
            else:
                return True
        else:
            return False

    @ui.uiEvent(uiConst.WIDGET_YAOPEI_FEED, events.EVENT_INVENTORY_ITEM_CLICKED)
    def onInventoryRightClick(self, event):
        event.stop()
        i = event.data['item']
        nPage = event.data['page']
        nItem = event.data['pos']
        if i == None:
            return
        else:
            self.setInventoryItem(nPage, nItem)
            return

    def setInventoryItem(self, nPageSrc, nItemSrc):
        p = BigWorld.player()
        srcItem = p.inv.getQuickVal(nPageSrc, nItemSrc)
        if srcItem:
            if srcItem.isYaoPei():
                self.setItem(nPageSrc, nItemSrc, True)
                if self.mediator:
                    self.mediator.Invoke('swapPanelToFront')

    def onSpeedUp(self, *args):
        if gameglobal.rds.ui.yaoPeiFeedCatchUp.widget:
            gameglobal.rds.ui.yaoPeiFeedCatchUp.hide()
        else:
            gameglobal.rds.ui.yaoPeiFeedCatchUp.show()

    def onShowYaoPeiFeedCatchUp(self, *args):
        show = args[3][0].GetBool()
        if show:
            p = BigWorld.player()
            if self.inBag:
                srcIt = p.inv.getQuickVal(self.resPos[0], self.resPos[1])
            else:
                srcIt = p.equipment[gametypes.EQU_PART_YAOPEI]
            times, maxTimes = srcIt.getYaoPeiPursueNum()
            if maxTimes != 0:
                gameglobal.rds.ui.yaoPeiFeedCatchUp.show()
            else:
                gameglobal.rds.ui.yaoPeiFeedCatchUp.hide()
        else:
            gameglobal.rds.ui.yaoPeiFeedCatchUp.hide()

    def getYaoPeiInfo(self):
        if self.inBag:
            resKind = const.RES_KIND_INV
        else:
            resKind = const.RES_KIND_EQUIP
        return (resKind, self.resPos)
