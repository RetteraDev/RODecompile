#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/activitySaleGroupBuyProxy.o
import BigWorld
import gameglobal
import uiConst
import utils
import events
import math
from uiProxy import UIProxy
from guis import uiUtils
from guis.asObject import ASObject
from gamestrings import gameStrings
from item import Item
from cdata import group_purchase_data as GPD
from data import item_data as ID
from data import sys_config_data as SCD
ITEM_START_Y = 173
ITEM_OFFSET_Y = 161
STATE_GROUP_PREORDER_ITEM = 1
STATE_GROUP_PURCHASE_ITEM = 2
GROUP_BUY_BG_IMAGE_PATH = 'activitySale/%s.dds'

class ActivitySaleGroupBuyProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ActivitySaleGroupBuyProxy, self).__init__(uiAdapter)
        self.widget = None
        self.tabSubIdxToGBData = {}
        self.reset()

    def clearAll(self):
        self.reset()
        self.tabSubIdxToGBData = {}

    def reset(self):
        self.widget = None
        self.tabIdx = 0
        self.curIdList = []
        self.callbackTimer = 0
        self.itemRenderMcList = []

    @property
    def curTabData(self):
        return self.tabSubIdxToGBData.get(self.tabIdx, {})

    def getValidGroupBuyBasicData(self):
        result = list()
        groupPurchaseBannerName = SCD.data.get('groupPurchaseBannerName', {})
        groupPurchaseName = SCD.data.get('groupPurchaseName', {})
        groupPurchaseIdList = SCD.data.get('groupPurchaseIdList', {})
        groupPurchasePriority = SCD.data.get('groupPurchasePriority', {})
        for tempIdx, bannerName in groupPurchaseBannerName.iteritems():
            name = groupPurchaseName.get(tempIdx, '')
            idList = groupPurchaseIdList.get(tempIdx, [])
            priority = groupPurchasePriority.get(tempIdx, 1)
            if self.canOpenByIdList(idList):
                result.append({'bannerName': bannerName,
                 'name': name,
                 'idList': idList,
                 'priority': priority})

        result = sorted(result, reverse=True, cmp=lambda data1, data2: data1.get('priority', 1) - data2.get('priority', 1))
        return result

    def initGroupBuy(self, tabIdx, widget):
        self.widget = widget
        self.tabIdx = tabIdx
        self.curIdList = self.curTabData.get('idList', [])
        self.initUI()

    def initUI(self):
        if not self.curIdList:
            return
        if not self.widget:
            return
        if not self.widget.mainPanel:
            return
        self.refreshPanel()
        self.checkTimer()

    def unRegisterGroupBuy(self):
        self.uiAdapter.fittingRoom.hide()
        self.widget = None
        self.reset()

    def clearItem(self):
        if self.widget:
            for childIdx in xrange(self.widget.mainPanel.canvas.numChildren - 1, -1, -1):
                childMc = self.widget.mainPanel.canvas.getChildAt(childIdx)
                if childMc.name != 'bgImage':
                    self.widget.mainPanel.canvas.removeChildAt(childIdx)

    def refreshPanel(self):
        if not self.widget:
            return
        self.clearItem()
        self.widget.mainPanel.canvas.bgImage.loadImage(GROUP_BUY_BG_IMAGE_PATH % self.curTabData.get('bannerName', 'groupbuy'))
        posY = ITEM_START_Y
        for groupBuyId in self.curIdList:
            itemInfo = GPD.data.get(groupBuyId, {})
            if not itemInfo:
                continue
            preOrderStartTime = itemInfo.get('preOrderStartTime', '')
            preOrderEndTime = itemInfo.get('preOrderEndTime', '')
            groupPurchaseStartTime = itemInfo.get('groupPurchaseStartTime', '')
            groupPurchaseEndTime = itemInfo.get('groupPurchaseEndTime', '')
            if utils.getNow() < utils.getDisposableCronTabTimeStamp(preOrderStartTime) or utils.getNow() >= utils.getDisposableCronTabTimeStamp(groupPurchaseEndTime):
                continue
            itemRenderMc = self.widget.getInstByClsName('ActivitySaleGroupBuy_Item')
            self.widget.mainPanel.canvas.addChild(itemRenderMc)
            self.itemRenderMcList.append(itemRenderMc)
            itemRenderMc.x = 10
            itemRenderMc.y = posY
            posY += ITEM_OFFSET_Y
            itemId = itemInfo['itemId']
            itemRenderMc.name = str(itemId)
            itemRenderMc.itemIcon.itemId = itemId
            itemRenderMc.itemIcon.setItemSlotData(uiUtils.getGfxItemById(itemId))
            itemRenderMc.itemIcon.dragable = False
            itemRenderMc.itemIcon.addEventListener(events.MOUSE_CLICK, self.handleShowFit, False, 0, True)
            itemRenderMc.itemName.text = ID.data.get(itemId, {}).get('name', '')
            originalPrice = itemInfo.get('originalPrice', 0)
            preOrderPrice = itemInfo.get('preOrderPrice', 0)
            preOrderPriceDeducted = itemInfo.get('preOrderPriceDeducted', 0)
            itemMaxNums = itemInfo.get('maxNums', 1)
            itemRenderMc.originalPriceIcon.bonusType = 'tianBi'
            itemRenderMc.preOrderPriceIcon.bonusType = 'tianBi'
            p = BigWorld.player()
            p.cell.getPreOrderCounterInfo()
            preOrderInfo = p.preOrderInfo
            preOrderCount = preOrderInfo.get(itemId, 0)
            discountInfo = itemInfo['triggerCountMargins']
            discounts = itemInfo['triggerDisCountMargins']
            itemRenderMc.progressBar.maxValue = discountInfo[-1]
            itemRenderMc.progressBar.currentValue = preOrderCount
            itemRenderMc.progressBar.textField.visible = False
            itemRenderMc.discount = 1
            startPos_X = 2
            i = 0
            for discount in discounts:
                discountFlagMc = self.widget.getInstByClsName('ActivitySaleGroupBuy_ProgressBarFlag')
                itemRenderMc.addChild(discountFlagMc)
                discountFlagMc.discount.discountTxt.visible = False
                pos_X = startPos_X + 560 * discountInfo[i] / discountInfo[-1]
                discountFlagMc.x = pos_X
                discountFlagMc.y = 92
                if preOrderCount >= discountInfo[i]:
                    discountFlagMc.discount.gotoAndStop('small')
                    discountFlagMc.overFlag.gotoAndStop('you')
                    if i < len(discountInfo) - 1 and preOrderCount < discountInfo[i + 1] or i == len(discountInfo) - 1:
                        itemRenderMc.discount = discount
                        discountFlagMc.discount.gotoAndStop('big')
                        discountFlagMc.discount.discountTxt.visible = True
                else:
                    discountFlagMc.discount.gotoAndStop('small')
                    discountFlagMc.overFlag.gotoAndStop('wu')
                i = i + 1
                discountFlagMc.discount.discountNum.text = gameStrings.ACTIVITY_SALE_GROUP_DISCOUNT % (discount * 10)

            preOrderItemIds = p.groupPurchaseInfo.get('preOrderItemIds', {})
            alReadyPurchaseItemIds = p.groupPurchaseInfo.get('alReadyPurchaseItemIds', {})
            if utils.getDisposableCronTabTimeStamp(preOrderStartTime) <= utils.getNow() < utils.getDisposableCronTabTimeStamp(preOrderEndTime):
                end = utils.formatDatetime(utils.getDisposableCronTabTimeStamp(preOrderEndTime))
                itemRenderMc.stateFlag.gotoAndStop('yushou')
                itemRenderMc.timeTxt.text = gameStrings.ACTIVITY_SALE_GROUP_BUY_PREODER_END + end
                itemRenderMc.state = STATE_GROUP_PREORDER_ITEM
                itemRenderMc.originalPriceTxt.text = gameStrings.ACTIVITY_SALE_GROUP_BUY_ORIGINAL_PRICE
                itemRenderMc.preOrderPriceTxt.text = gameStrings.ACTIVITY_SALE_GROUP_BUY_PREODER_PRICE
                itemRenderMc.originalPrice.text = originalPrice
                itemRenderMc.preOrderPrice.text = preOrderPrice
                itemRenderMc.deductionTxt.text = '(' + gameStrings.ACTIVITY_SALE_GROUP_BUY_DEDUCTION % preOrderPriceDeducted + ')'
                itemRenderMc.deductionTxt.x = 310
                itemRenderMc.buyBtn.addEventListener(events.BUTTON_CLICK, self.handleClickBuyBtn, False, 0, True)
                if itemId in preOrderItemIds:
                    preOrderNums = preOrderItemIds[itemId]
                    itemRenderMc.itemName.text = str(itemRenderMc.itemName.text) + str(gameStrings.ACTIVITY_SALE_GROUP_BUY_HAVE_PREORDERED_NUMS % preOrderNums)
                    if preOrderNums < itemMaxNums:
                        itemRenderMc.buyBtn.enabled = True
                        itemRenderMc.buyBtn.label = gameStrings.ACTIVITY_SALE_GROUP_BUY_CONTINUE_PREORDERED
                    else:
                        itemRenderMc.buyBtn.enabled = False
                        itemRenderMc.buyBtn.label = gameStrings.ACTIVITY_SALE_GROUP_BUY_HAVE_PREORDERED
                else:
                    itemRenderMc.buyBtn.enabled = True
                    itemRenderMc.buyBtn.label = gameStrings.ACTIVITY_SALE_GROUP_BUY_PREODER_NOW
            elif utils.getDisposableCronTabTimeStamp(groupPurchaseStartTime) <= utils.getNow() < utils.getDisposableCronTabTimeStamp(groupPurchaseEndTime):
                end = utils.formatDatetime(utils.getDisposableCronTabTimeStamp(groupPurchaseEndTime))
                itemRenderMc.stateFlag.gotoAndStop('tuangou')
                itemRenderMc.timeTxt.text = gameStrings.ACTIVITY_SALE_GROUP_BUY_PURCHASE_END + end
                itemRenderMc.state = STATE_GROUP_PURCHASE_ITEM
                itemRenderMc.originalPriceTxt.text = gameStrings.ACTIVITY_SALE_GROUP_BUY_ORIGINAL_PRICE
                itemRenderMc.preOrderPriceTxt.text = gameStrings.ACTIVITY_SALE_GROUP_BUY_CURRENT_PRICE
                itemRenderMc.originalPrice.text = originalPrice
                itemRenderMc.preOrderPrice.text = math.ceil(originalPrice * itemRenderMc.discount)
                itemRenderMc.deductionTxt.text = gameStrings.ACTIVITY_SALE_GROUP_BUY_PREODER_HAVE_END
                itemRenderMc.deductionTxt.x = 328
                itemRenderMc.buyBtn.addEventListener(events.BUTTON_CLICK, self.handleClickBuyBtn, False, 0, True)
                alReadyPurchaseNums = alReadyPurchaseItemIds.get(itemId, 0)
                preOrderNums = preOrderItemIds.get(itemId, 0)
                if alReadyPurchaseNums > 0:
                    if preOrderNums > 0:
                        itemRenderMc.itemName.text = str(itemRenderMc.itemName.text) + str(gameStrings.ACTIVITY_SALE_GROUP_BUY_HAVE_PREORDERED_NUMS_AND_HAVE_BOUGHT_NUMS % (preOrderNums, alReadyPurchaseNums))
                    else:
                        itemRenderMc.itemName.text = str(itemRenderMc.itemName.text) + str(gameStrings.ACTIVITY_SALE_GROUP_BUY_HAVE_BOUGHT_NUMS % alReadyPurchaseNums)
                    if alReadyPurchaseNums < itemMaxNums:
                        itemRenderMc.buyBtn.enabled = True
                        itemRenderMc.buyBtn.label = gameStrings.ACTIVITY_SALE_GROUP_BUY_CONTINUE_BOUGHT
                    else:
                        itemRenderMc.buyBtn.enabled = False
                        itemRenderMc.buyBtn.label = gameStrings.ACTIVITY_SALE_GROUP_BUY_HAVE_BOUGHT
                else:
                    if preOrderNums > 0:
                        itemRenderMc.itemName.text = str(itemRenderMc.itemName.text) + str(gameStrings.ACTIVITY_SALE_GROUP_BUY_HAVE_PREORDERED_NUMS % preOrderNums)
                    itemRenderMc.buyBtn.enabled = True
                    itemRenderMc.buyBtn.label = gameStrings.ACTIVITY_SALE_GROUP_BUY_PURCHASE_NOW
            else:
                itemRenderMc.timeTxt.text = gameStrings.ACTIVITY_SALE_GROUP_BUY_NOT_IN_TIME

        self.widget.mainPanel.validateNow()
        self.widget.mainPanel.refreshHeight(posY)
        self.uiAdapter.activitySale.refreshInfo()

    def handleClickBuyBtn(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget.parent
        itemId = itemMc.itemIcon.itemId
        state = itemMc.state
        discount = itemMc.discount
        gameglobal.rds.ui.activitySaleGroupBuyConfirm.show(state, itemId, discount)

    def canOpenByIdList(self, idList):
        if not gameglobal.rds.configData.get('enableGroupPurchase', False):
            return False
        for id in idList:
            if self.canOpenById(id):
                return True

        return False

    def canOpenById(self, id):
        if not id or id not in GPD.data:
            return False
        value = GPD.data.get(id, {})
        if not value:
            return False
        startTime = value.get('preOrderStartTime', '')
        endTime = value.get('groupPurchaseEndTime', '')
        sec = utils.getNow()
        if utils.getDisposableCronTabTimeStamp(startTime) <= sec < utils.getDisposableCronTabTimeStamp(endTime):
            return True
        return False

    def getRedPointVisible(self, idList):
        groupPurchaseInfo = BigWorld.player().groupPurchaseInfo
        preOrderItemList = groupPurchaseInfo.get('preOrderItemIds', {})
        purchaseItemList = groupPurchaseInfo.get('alReadyPurchaseItemIds', {})
        for itemId in preOrderItemList:
            if itemId not in purchaseItemList or preOrderItemList[itemId] > purchaseItemList[itemId]:
                item_value = {}
                item_idx = 0
                for idx, value in GPD.data.iteritems():
                    if value.get('itemId', 0) == itemId:
                        item_idx = idx
                        item_value = value

                if not item_idx or not item_value:
                    continue
                if item_idx not in idList:
                    continue
                groupPurchaseStartTime = item_value.get('groupPurchaseStartTime', 0)
                groupPurchaseEndTime = item_value.get('groupPurchaseEndTime', 0)
                if utils.getDisposableCronTabTimeStamp(groupPurchaseStartTime) <= utils.getNow() < utils.getDisposableCronTabTimeStamp(groupPurchaseEndTime):
                    return True

        return False

    def checkTimer(self):
        timeList = []
        for groupBuyId in self.curIdList:
            value = GPD.data.get(groupBuyId, {})
            if not value:
                continue
            sec = utils.getNow()
            preOrderStartTime = utils.getDisposableCronTabTimeStamp(value.get('preOrderStartTime', 0)) - sec
            preOrderEndTime = utils.getDisposableCronTabTimeStamp(value.get('preOrderEndTime', 0)) - sec
            groupPurchaseStartTime = utils.getDisposableCronTabTimeStamp(value.get('groupPurchaseStartTime', 0)) - sec
            groupPurchaseEndTime = utils.getDisposableCronTabTimeStamp(value.get('groupPurchaseEndTime', 0)) - sec
            preOrderStartTime and preOrderStartTime >= 0 and timeList.append(preOrderStartTime)
            preOrderEndTime and preOrderEndTime >= 0 and timeList.append(preOrderEndTime)
            groupPurchaseStartTime and groupPurchaseStartTime >= 0 and timeList.append(groupPurchaseStartTime)
            groupPurchaseEndTime and groupPurchaseEndTime >= 0 and timeList.append(groupPurchaseEndTime)

        if len(timeList):
            self.refreshPanel()
            self.callbackTimer = BigWorld.callback(min(timeList) + 1, self.checkTimer)
        else:
            self.refreshPanel()

    def handleShowFit(self, *args):
        e = ASObject(args[3][0])
        if e.buttonIdx == uiConst.LEFT_BUTTON:
            itemId = int(e.currentTarget.itemId)
            self.uiAdapter.fittingRoom.addItem(Item(itemId))

    def pushPreOrderMessage(self):
        if uiConst.MESSAGE_TYPE_PRE_ORDER not in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_PRE_ORDER)
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_PRE_ORDER, {'click': self.onPushPreOrderMsgClick})

    def onPushPreOrderMsgClick(self):
        if not self.widget:
            gameglobal.rds.ui.activitySale.show(uiConst.ACTIVITY_SALE_TAB_GROUP_BUY)
        self.removePreOrderPushMsg()

    def removePreOrderPushMsg(self):
        if uiConst.MESSAGE_TYPE_PRE_ORDER in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_PRE_ORDER)

    def pushGroupBuyMessage(self):
        if uiConst.MESSAGE_TYPE_GROUP_PURCHASE not in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GROUP_PURCHASE)
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_GROUP_PURCHASE, {'click': self.onPushGroupBuyMsgClick})

    def onPushGroupBuyMsgClick(self):
        if not self.widget:
            gameglobal.rds.ui.activitySale.show(uiConst.ACTIVITY_SALE_TAB_GROUP_BUY)
        self.removeGroupBuyPushMsg()

    def removeGroupBuyPushMsg(self):
        if uiConst.MESSAGE_TYPE_GROUP_PURCHASE in gameglobal.rds.ui.pushMessage.msgs:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_GROUP_PURCHASE)
