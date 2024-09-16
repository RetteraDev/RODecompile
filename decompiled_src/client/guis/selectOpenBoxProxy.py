#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/selectOpenBoxProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import gamelog
import const
import clientUtils
import tipUtils
import uiUtils
import math
import events
from uiProxy import UIProxy
from guis.asObject import TipManager
from guis.asObject import ASObject
from callbackHelper import Functor
from guis import ui
from data import consumable_item_data as CID
from cdata import game_msg_def_data as GMDD
ITEM_START_Y = 61
TWO_ITEM_START_X = 164
THREE_ITEM_START_X = 30
LIST_ITEM_START_X = 1
LIST_ITEM_START_Y = 0
TITLE_OFFSET_Y = 25
ITEM_OFFSET_Y = 56
ITEM_NUM_PER_LINE = 4
TEXT_COLOR_RED = '#F43804'
TEXT_COLOR_NORMAL = '#FFFFE7'
BONUS_ID = 0
CONSUME_ITEMS = 1
CONSUME_FAME = 2
CONSUME_COIN = 3
CONSUME_MALL_SCORE = 4
CONSUME_CASH = 5
CONSUME_BIND_CASH = 6
BONUS_DESC = 7

class SelectOpenBoxProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SelectOpenBoxProxy, self).__init__(uiAdapter)
        self.widget = None
        self.nPage = const.CONT_NO_PAGE
        self.nItem = const.CONT_NO_POS
        self.maxNum = 1
        self.itemId = 0
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_SELECT_OPEN_BOX, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SELECT_OPEN_BOX:
            self.widget = widget
            self.initUI()

    def reset(self):
        self.itemId = 0
        self.boxMc = None
        self.nPage = const.CONT_NO_PAGE
        self.nItem = const.CONT_NO_POS
        self.maxNum = 1

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SELECT_OPEN_BOX)
        self.reset()

    def show(self, itemId, nPage, nItem):
        self.itemId = itemId
        self.nPage = nPage
        self.nItem = nItem
        self.maxNum = self.getMaxOpenCount()
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_SELECT_OPEN_BOX)
        else:
            self.initUI()

    def initUI(self):
        if not self.widget:
            return
        self.widget.defaultCloseBtn = self.widget.closeBtn
        if self.boxMc:
            self.widget.removeChild(self.boxMc)
        cidData = CID.data.get(self.itemId, {})
        bonusInfo = cidData.get('bonusInfo', [])
        boxNum = len(bonusInfo)
        if boxNum == 2:
            bonusMc = self.widget.getInstByClsName('SelectOpenBox_TwoBonusMc')
            self.widget.addChild(bonusMc)
            bonusMc.x = TWO_ITEM_START_X
        else:
            bonusMc = self.widget.getInstByClsName('SelectOpenBox_ThreeBonusMc')
            self.widget.addChild(bonusMc)
            bonusMc.x = THREE_ITEM_START_X
        self.boxMc = bonusMc
        bonusMc.y = ITEM_START_Y
        for index, info in enumerate(bonusInfo):
            boxMc = bonusMc.getChildByName('box%d' % (index + 1))
            boxMc.data = index
            bonusDesc = info[BONUS_DESC] or ''
            boxMc.bonusDesc.htmlText = bonusDesc
            bonusId = info[BONUS_ID]
            mustObtainIdList = []
            possibleObtainIdList = []
            tipUtils._genBonusWithBonusId(bonusId, mustObtainIdList, possibleObtainIdList)
            posY = LIST_ITEM_START_Y
            if mustObtainIdList:
                titleMc = self.widget.getInstByClsName('SelectOpenBox_ItemTitle')
                boxMc.itemWnd.canvas.addChild(titleMc)
                titleMc.title.text = gameStrings.TEXT_SELECTOPENBOXPROXY_124
                titleMc.x = LIST_ITEM_START_X
                titleMc.y = posY
                posY += TITLE_OFFSET_Y
                itemNum = len(mustObtainIdList)
                groupNum = int(math.ceil(float(itemNum) / ITEM_NUM_PER_LINE))
                currentItemIndex = 0
                for i in xrange(groupNum):
                    groupItemMc = self.widget.getInstByClsName('SelectOpenBox_BonusItem')
                    boxMc.itemWnd.canvas.addChild(groupItemMc)
                    groupItemMc.x = LIST_ITEM_START_X
                    groupItemMc.y = posY
                    posY += ITEM_OFFSET_Y
                    for i in xrange(ITEM_NUM_PER_LINE):
                        itemMc = getattr(groupItemMc, 'item%d' % i)
                        if currentItemIndex < itemNum:
                            item = mustObtainIdList[currentItemIndex]
                            itemMc.visible = True
                            itemMc.dragable = False
                            itemMc.itemId = item[0]
                            itemMc.itemCount = item[2]
                            itemMc.setItemSlotData(uiUtils.getGfxItemById(item[0], item[2]))
                        else:
                            itemMc.visible = False
                        currentItemIndex += 1

                posY += 5
            if possibleObtainIdList:
                titleMc = self.widget.getInstByClsName('SelectOpenBox_ItemTitle')
                boxMc.itemWnd.canvas.addChild(titleMc)
                titleMc.title.text = gameStrings.TEXT_ACTIVITYSALEDAILYGIFTPROXY_103
                titleMc.x = LIST_ITEM_START_X
                titleMc.y = posY
                posY += TITLE_OFFSET_Y
                itemNum = len(possibleObtainIdList)
                groupNum = int(math.ceil(float(itemNum) / ITEM_NUM_PER_LINE))
                currentItemIndex = 0
                for i in xrange(groupNum):
                    groupItemMc = self.widget.getInstByClsName('SelectOpenBox_BonusItem')
                    boxMc.itemWnd.canvas.addChild(groupItemMc)
                    groupItemMc.x = LIST_ITEM_START_X
                    groupItemMc.y = posY
                    posY += ITEM_OFFSET_Y
                    for i in xrange(ITEM_NUM_PER_LINE):
                        itemMc = getattr(groupItemMc, 'item%d' % i)
                        if currentItemIndex < itemNum:
                            item = possibleObtainIdList[currentItemIndex]
                            itemMc.visible = True
                            itemMc.dragable = False
                            itemMc.itemId = item[0]
                            itemMc.itemCount = item[2]
                            itemMc.setItemSlotData(uiUtils.getGfxItemById(item[0], item[2]))
                        else:
                            itemMc.visible = False
                        currentItemIndex += 1

            boxMc.cost0.visible = False
            boxMc.cost1.visible = False
            boxMc.cost2.visible = False
            boxMc.counter.count = 1
            boxMc.counter.minCount = 1
            boxMc.counter.maxCount = self.getMaxOpenCount()
            boxMc.counter.addEventListener(events.EVENT_COUNT_CHANGE, self.boxCounterChange, False, 0, True)
            boxMc.maxBtn.addEventListener(events.BUTTON_CLICK, self.onMaxBtnClick)
            boxMc.confirmBtn.isCashReplace = False
            self.refreshCostInfo(boxMc)
            boxMc.confirmBtn.data = index
            boxMc.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleClickConfirmBtn, False, 0, True)

    def onMaxBtnClick(self, *args):
        e = ASObject(args[3][0])
        e.currentTarget.parent.counter.count = self.getMaxOpenCount()

    def boxCounterChange(self, *args):
        e = ASObject(args[3][0])
        self.refreshCostInfo(e.currentTarget.parent)

    def getMaxOpenCount(self):
        p = BigWorld.player()
        boxItem = p.inv.getQuickVal(self.nPage, self.nItem)
        boxNum = boxItem.cwrap
        return max(boxNum, 1)

    def refreshCostInfo(self, boxMc):
        p = BigWorld.player()
        index = boxMc.data
        cidData = CID.data.get(self.itemId, {})
        bonusInfo = cidData.get('bonusInfo', [])
        info = bonusInfo[index]
        openNum = boxMc.counter.count
        consumeList, consumeNum = self.getConsumeList(info, openNum)
        costMc = boxMc.getChildByName('cost%d' % consumeNum)
        costMc.visible = True
        boxMc.confirmBtn.openNum = openNum
        if consumeNum == 1:
            cost = consumeList[0]
            count = cost.get('count', 0)
            isEnough = cost.get('isEnough', False)
            if cost.has_key('itemId'):
                itemId = cost.get('itemId', 0)
                path = uiUtils.getItemIconPath(itemId)
                costMc.moneyIcon.visible = False
                costMc.costItem.visible = True
                costMc.costItem.fitSize = True
                costMc.costItem.loadImage(path)
                TipManager.addItemTipById(costMc.costItem, itemId)
            else:
                bonusType = cost.get('bonusType', 'cash')
                costMc.moneyIcon.visible = True
                costMc.costItem.visible = False
                costMc.moneyIcon.bonusType = bonusType
                TipManager.removeTip(costMc.costItem)
                if bonusType == 'bindCash' and not isEnough:
                    cash = p.bindCash + p.cash
                    boxMc.confirmBtn.isCashReplace = cash >= count
            if isEnough:
                countDesc = uiUtils.toHtml(count, TEXT_COLOR_NORMAL)
            else:
                countDesc = uiUtils.toHtml(count, TEXT_COLOR_RED)
            costMc.money.htmlText = countDesc
        elif consumeNum == 2:
            consumeCash = info.get('consumeCash', 0)
            consumeBindCash = info.get('consumeBindCash', 0)
            for costIndex in xrange(consumeNum):
                cost = consumeList[costIndex]
                count = cost.get('count', 0)
                isEnough = cost.get('isEnough', False)
                subCostMc = costMc.getChildByName('subCost%d' % costIndex)
                if cost.has_key('itemId'):
                    itemId = cost.get('itemId', 0)
                    path = uiUtils.getItemIconPath(itemId)
                    subCostMc.moneyIcon.visible = False
                    subCostMc.costItem.visible = True
                    subCostMc.costItem.fitSize = True
                    subCostMc.costItem.loadImage(path)
                    TipManager.addItemTipById(subCostMc.costItem, itemId)
                else:
                    bonusType = cost.get('bonusType', 'cash')
                    subCostMc.moneyIcon.visible = True
                    subCostMc.costItem.visible = False
                    subCostMc.moneyIcon.bonusType = bonusType
                    TipManager.removeTip(subCostMc.costItem)
                    if bonusType == 'bindCash' and not isEnough:
                        cash = p.bindCash + p.cash
                        isReplace = False
                        if consumeCash:
                            isReplace = cash >= consumeBindCash + consumeCash
                        else:
                            isReplace = cash >= consumeBindCash
                        boxMc.confirmBtn.isCashReplace = isReplace
                if isEnough:
                    countDesc = uiUtils.toHtml(count, TEXT_COLOR_NORMAL)
                else:
                    countDesc = uiUtils.toHtml(count, TEXT_COLOR_RED)
                subCostMc.money.htmlText = countDesc

    def getConsumeList(self, info, openNum = 1):
        costs = []
        p = BigWorld.player()
        consumeItems = info[CONSUME_ITEMS] or ()
        consumeFame = info[CONSUME_FAME] or ()
        consumeCoin = info[CONSUME_COIN] or 0
        consumeCash = info[CONSUME_CASH] or 0
        consumeBindCash = info[CONSUME_BIND_CASH] or 0
        consumeMallScore = info[CONSUME_MALL_SCORE] or 0
        if consumeItems:
            for itemId, consumeCount in consumeItems:
                consumeCount *= openNum
                itemInfo = {}
                itemInfo['itemId'] = itemId
                itemInfo['count'] = consumeCount
                itemCount = p.inv.countItemInPages(itemId, enableParentCheck=True)
                itemInfo['isEnough'] = itemCount >= consumeCount
                costs.append(itemInfo)

        if consumeFame:
            for fameId, fameNum in consumeFame:
                fameNum *= openNum
                itemInfo = {}
                fame = p.getFame(const.YUN_CHUI_JI_FEN_FAME_ID)
                itemInfo['bonusType'] = 'yunChui'
                itemInfo['count'] = fameNum
                itemInfo['isEnough'] = fame >= fameNum
                costs.append(itemInfo)

        if consumeCoin:
            consumeCoin *= openNum
            itemInfo = {}
            coin = p.unbindCoin + p.bindCoin + p.freeCoin
            itemInfo['bonusType'] = 'tianBi'
            itemInfo['count'] = consumeCoin
            itemInfo['isEnough'] = coin >= consumeCoin
            costs.append(itemInfo)
        if consumeCash:
            consumeCash *= openNum
            itemInfo = {}
            cash = p.cash
            itemInfo['bonusType'] = 'cash'
            itemInfo['count'] = consumeCash
            itemInfo['isEnough'] = cash >= consumeCash
            costs.append(itemInfo)
        if consumeBindCash:
            consumeBindCash *= openNum
            itemInfo = {}
            bindCash = p.bindCash
            itemInfo['bonusType'] = 'bindCash'
            itemInfo['count'] = consumeBindCash
            itemInfo['isEnough'] = bindCash >= consumeBindCash
            costs.append(itemInfo)
        if consumeMallScore:
            consumeMallScore *= openNum
            itemInfo = {}
            mallScore = p.mallScore
            itemInfo['bonusType'] = 'jiFenBi'
            itemInfo['count'] = consumeMallScore
            itemInfo['isEnough'] = mallScore >= consumeMallScore
            costs.append(itemInfo)
        consumeNum = 0
        if len(costs) == 1 or len(costs) > 2:
            consumeNum = 1
        elif len(costs) == 2:
            consumeNum = 2
        return (costs, consumeNum)

    @ui.checkInventoryLock()
    def handleClickConfirmBtn(self, *args):
        p = BigWorld.player()
        e = ASObject(args[3][0])
        boxType = int(e.target.data)
        isCashReplace = e.target.isCashReplace
        count = e.target.openNum
        if self.nPage != const.CONT_NO_PAGE and self.nItem != const.CONT_NO_POS:
            if isCashReplace:
                msg = uiUtils.getTextFromGMD(GMDD.data.BINDCASH_IS_NOT_ENOUGH, '')
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.useCommonItemToSelectBox, self.nPage, self.nItem, count, boxType, p.cipherOfPerson))
            else:
                p.cell.useCommonItemToSelectBox(self.nPage, self.nItem, count, boxType, p.cipherOfPerson)
