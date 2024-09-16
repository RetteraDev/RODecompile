#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/activitySaleGroupBuyConfirmProxy.o
import BigWorld
import math
import uiConst
import events
from asObject import ASObject
from gamestrings import gameStrings
from uiProxy import UIProxy
from guis import uiUtils
from cdata import group_purchase_data as GPD
from data import item_data as ID
STATE_GROUP_PREORDER_ITEM = 1
STATE_GROUP_PURCHASE_ITEM = 2

class ActivitySaleGroupBuyConfirmProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ActivitySaleGroupBuyConfirmProxy, self).__init__(uiAdapter)
        self.widget = None
        self.state = None
        self.itemId = None
        self.discount = 1
        self.curItemNums = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_ACTIVITY_SALE_GROUP_BUY_CONFIRM, self.hide)

    def reset(self):
        self.widget = None
        self.state = None
        self.itemId = None
        self.discount = 1
        self.curItemNums = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ACTIVITY_SALE_GROUP_BUY_CONFIRM:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ACTIVITY_SALE_GROUP_BUY_CONFIRM)

    def show(self, state, itemId, discount):
        self.state = state
        self.itemId = itemId
        self.discount = discount
        self.curItemNums = 1
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_ACTIVITY_SALE_GROUP_BUY_CONFIRM)
        else:
            self.initUI()

    @property
    def preOrderItemIds(self):
        return BigWorld.player().groupPurchaseInfo.get('preOrderItemIds', {})

    @property
    def alReadyPurchaseItemIds(self):
        return BigWorld.player().groupPurchaseInfo.get('alReadyPurchaseItemIds', {})

    @property
    def itemInfo(self):
        return self.getItemInfo(self.itemId)

    def getItemInfo(self, itemId):
        items = [ v for v in GPD.data.itervalues() if v.get('itemId', 0) == itemId ]
        itemInfo = items[0]
        return itemInfo

    def initUI(self):
        originalPrice = self.itemInfo.get('originalPrice', 0)
        preOrderPrice = self.itemInfo.get('preOrderPrice', 0)
        preOrderPriceDeducted = self.itemInfo.get('preOrderPriceDeducted', 0)
        itemMaxNums = self.itemInfo.get('maxNums', 1)
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.itemIcon.itemId = self.itemId
        self.widget.itemIcon.setItemSlotData(uiUtils.getGfxItemById(self.itemId))
        self.widget.itemName.text = ID.data.get(self.itemId, {}).get('name', '')
        self.widget.priceIcon.bonusType = 'tianBi'
        self.widget.totalPriceIcon.bonusType = 'tianBi'
        self.widget.buyCount.minCount = 1
        self.widget.buyCount.count = self.curItemNums
        self.widget.buyCount.addEventListener(events.EVENT_COUNT_CHANGE, self.handleBuyCounterChange, False, 0, True)
        self.widget.rechargeBtn.addEventListener(events.BUTTON_CLICK, self.handleRechargeBtnClick, False, 0, True)
        if self.state == STATE_GROUP_PREORDER_ITEM:
            self.widget.totalNumTitle.text = gameStrings.ACTIVITY_SALE_GROUP_BUY_CONFIRM_PREORDER_TOTAL_NUMS_TITLE
            self.widget.totalPriceTitle.text = gameStrings.ACTIVITY_SALE_GROUP_BUY_CONFIRM_PREORDER_TOTAL_PRICE_TITLE
            self.widget.deductedTxt.visible = True
            self.widget.deductedTxt.text = gameStrings.ACTIVITY_SALE_GROUP_BUY_DEDUCTED_PREORDER
            self.widget.deductionTxt.visible = True
            self.widget.deductionTxt.text = gameStrings.ACTIVITY_SALE_GROUP_BUY_DEDUCTION % preOrderPriceDeducted
            self.widget.priceTxt.text = gameStrings.ACTIVITY_SALE_GROUP_BUY_CONFIRM_PREORDER
            self.widget.price.text = preOrderPrice
            self.widget.buyCount.maxCount = itemMaxNums - self.preOrderItemIds.get(self.itemId, 0)
            self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handlePreorderBtnClick, False, 0, True)
        elif self.state == STATE_GROUP_PURCHASE_ITEM:
            self.widget.totalNumTitle.text = gameStrings.ACTIVITY_SALE_GROUP_BUY_CONFIRM_PURCHASE_TOTAL_NUMS_TITLE
            self.widget.totalPriceTitle.text = gameStrings.ACTIVITY_SALE_GROUP_BUY_CONFIRM_PURCHASE_TOTAL_PRICE_TITLE
            self.widget.deductionTxt.visible = False
            self.widget.priceTxt.text = gameStrings.ACTIVITY_SALE_GROUP_BUY_CONFIRM_GURCHASE
            self.widget.deductedTxt.visible = False
            self.widget.buyCount.maxCount = itemMaxNums - self.alReadyPurchaseItemIds.get(self.itemId, 0)
            self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleGroupPurchaseBtnClick, False, 0, True)
        self.refreshInfo()

    def refreshInfo(self):
        if not self.widget:
            return
        originalPrice = self.itemInfo.get('originalPrice', 0)
        preOrderPrice = self.itemInfo.get('preOrderPrice', 0)
        if self.state == STATE_GROUP_PREORDER_ITEM:
            self.widget.totalPrice.text = str(preOrderPrice * self.curItemNums)
        elif self.state == STATE_GROUP_PURCHASE_ITEM:
            self.widget.deductedTxt.visible = False
            nowPrice = math.ceil(originalPrice * self.discount)
            canDeductedPrice, canDeductedNums = self.getCanDeductedPrice(self.itemId, self.curItemNums)
            if canDeductedPrice > 0:
                self.widget.deductedTxt.visible = True
                self.widget.deductedTxt.text = gameStrings.ACTIVITY_SALE_GROUP_BUY_DEDUCTED % (canDeductedNums, canDeductedPrice)
            self.widget.price.text = nowPrice
            self.widget.totalPrice.text = nowPrice * self.curItemNums - canDeductedPrice

    def getCanDeductedPrice(self, buyItemId, buyItemNums):
        itemInfo = self.getItemInfo(buyItemId)
        preOrderPriceDeducted = itemInfo.get('preOrderPriceDeducted', 0)
        preOrderNums = self.preOrderItemIds.get(buyItemId, 0)
        alReadyPurchaseNums = self.alReadyPurchaseItemIds.get(buyItemId, 0)
        canDeductedPrice = 0
        canDeductedNums = 0
        if preOrderNums > alReadyPurchaseNums:
            canDeductedNums = preOrderNums - alReadyPurchaseNums
            if buyItemNums <= canDeductedNums:
                canDeductedPrice = preOrderPriceDeducted * buyItemNums
                canDeductedNums = buyItemNums
            else:
                canDeductedPrice = preOrderPriceDeducted * canDeductedNums
        return (canDeductedPrice, canDeductedNums)

    def handlePreorderBtnClick(self, *args):
        BigWorld.player().cell.preOrderItem(self.itemId, self.curItemNums)
        self.hide()

    def handleGroupPurchaseBtnClick(self, *args):
        BigWorld.player().cell.groupPurchaseItem(self.itemId, self.curItemNums)
        self.hide()

    def handleRechargeBtnClick(self, *args):
        self.uiAdapter.tianyuMall.onOpenChargeWindow()
        self.hide()

    def handleBuyCounterChange(self, *args):
        e = ASObject(args[3][0])
        self.curItemNums = int(e.currentTarget.count)
        self.refreshInfo()
