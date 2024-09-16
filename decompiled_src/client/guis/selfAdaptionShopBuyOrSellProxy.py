#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/selfAdaptionShopBuyOrSellProxy.o
import BigWorld
import gametypes
import uiConst
import events
import const
from gamestrings import gameStrings
import dynamicShop
from guis import uiUtils
from guis import compositeShopHelpFunc
from guis import ui
from uiProxy import UIProxy
from guis.asObject import ASObject
from guis.asObject import TipManager
from data import fame_data as FD
from data import item_data as ID
from cdata import dynamic_shop_item_data as DSID
from cdata import game_msg_def_data as GMDD
LIMIT_CONDITION_MAX_CNT = 3

class SelfAdaptionShopBuyOrSellProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SelfAdaptionShopBuyOrSellProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_SELF_ADAPTION_SHOP_BUY_OR_SELL, self.hide)

    def reset(self):
        self.frameInfo = {}
        self.tradeCount = 1

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SELF_ADAPTION_SHOP_BUY_OR_SELL:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SELF_ADAPTION_SHOP_BUY_OR_SELL)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_SELF_ADAPTION_SHOP_BUY_OR_SELL)
        else:
            self.initUI()
            self.refreshInfo()
            self.widget.swapPanelToFront()

    def initUI(self):
        isValid, compositeInfo = compositeShopHelpFunc.getLimitedInfo(DSID.data.get(self.uiAdapter.selfAdaptionShop.selectSetId, {}))
        self.widget.gotoAndStop('extra' if compositeInfo else 'normal')
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.counter.count = 1
        self.widget.counter.minCount = 1
        self.widget.counter.numberLimitCallback = self.numberLimitCallback
        self.widget.counter.addEventListener(events.EVENT_COUNT_CHANGE, self.handleBuyCountChange, False, 0, True)
        self.widget.yesBtn.addEventListener(events.BUTTON_CLICK, self.handleYesBtnClick, False, 0, True)
        self.widget.noBtn.addEventListener(events.BUTTON_CLICK, self.handleNoBtnClick, False, 0, True)
        isBuyTab = self.uiAdapter.selfAdaptionShop.tabIdx == uiConst.SELF_ADAPTION_SHOP_TAB_TYPE_BUY
        self.widget.txtTitle.text = gameStrings.SELF_ADAPTION_SHOP_TITLE_BUY if isBuyTab else gameStrings.SELF_ADAPTION_SHOP_TITLE_SELL
        self.widget.txtDesc0.text = gameStrings.SELF_ADAPTION_SHOP_TXT_DESC0_BUY if isBuyTab else gameStrings.SELF_ADAPTION_SHOP_TXT_DESC0_SELL
        self.widget.txtDesc1.text = gameStrings.SELF_ADAPTION_SHOP_TXT_DESC1_BUY if isBuyTab else gameStrings.SELF_ADAPTION_SHOP_TXT_DESC1_SELL
        self.widget.txtDesc2.text = gameStrings.SELF_ADAPTION_SHOP_TXT_DESC2
        if compositeInfo:
            self.initExtraUI(isValid, compositeInfo)

    def initExtraUI(self, isValid, compositeInfo):
        isBuyTab = self.uiAdapter.selfAdaptionShop.tabIdx == uiConst.SELF_ADAPTION_SHOP_TAB_TYPE_BUY
        self.widget.conditionTxt.text = gameStrings.SELF_ADAPTION_SHOP_TXT_CONDITION_BUY if isBuyTab else gameStrings.SELF_ADAPTION_SHOP_TXT_CONDITON_SELL
        for i in xrange(LIMIT_CONDITION_MAX_CNT):
            mcTxt = getattr(self.widget, 'condition%d' % i)
            mcYesOrNo = getattr(self.widget, 'yesOrNo%d' % i)
            if i < len(compositeInfo):
                mcTxt.visible = True
                mcYesOrNo.visible = True
                desc, valid, _ = compositeInfo[i]
                if not isBuyTab:
                    desc = desc.replace(gameStrings.SELF_ADAPTION_SHOP_CONDITION_BUY, gameStrings.SELF_ADAPTION_SHOP_CONDITION_SELL)
                mcTxt.text = desc
                mcYesOrNo.gotoAndStop('yes' if valid else 'no')
            else:
                mcTxt.visible = False
                mcYesOrNo.visible = False

        self.widget.yesBtn.enabled = isValid

    def getFrameInfo(self):
        p = BigWorld.player()
        setId = self.uiAdapter.selfAdaptionShop.selectSetId
        self.frameInfo = self.uiAdapter.selfAdaptionShop.getItemInfo(setId)

    def handleBuyCountChange(self, *args):
        e = ASObject(args[3][0])
        self.tradeCount = int(self.widget.counter.count)
        self.refreshPriceInfo()

    @ui.callInCD(0.5)
    def refreshPriceInfo(self):
        setId = self.frameInfo.get('setId', 0)
        if not setId:
            return
        predictPrice = self.getPredictPrice(setId, self.tradeCount)
        self.widget.txtTotalCost.text = gameStrings.SELF_ADAPTION_SHOP_TOTAL_COST % predictPrice

    def getPredictPrice(self, setId, count):
        dynamicShopItemVal = self.uiAdapter.selfAdaptionShop.set2ValDic.get(setId, None)
        if not dynamicShopItemVal:
            return 0
        else:
            configData = DSID.data.get(setId, {})
            dynamicShopType = configData.get('dynamicShopType', 0)
            changePriceCount = dynamicShopItemVal.tradedCount
            minPrice = dynamicShopItemVal.minPrice
            maxPrice = dynamicShopItemVal.maxPrice
            nowPrice = dynamicShopItemVal.price
            lastCyclePlayerTradedCount = dynamicShopItemVal.lastCyclePlayerTradedCount
            lastCycleItemTradedCount = dynamicShopItemVal.lastCycleItemTradedCount
            itemTradedChangePriceCount = int(dynamicShop._evaluateData('itemTradedChangePriceCountFormula', configData, {'playerTradedCount': lastCyclePlayerTradedCount,
             'itemTradedCount': lastCycleItemTradedCount}))
            itemTradedChangePriceType = configData['itemTradedChangePriceType']
            itemTradedChangePriceValue = float(dynamicShop._evaluateData('itemTradedChangePriceValueFormula', configData, {'playerTradedCount': lastCyclePlayerTradedCount,
             'itemTradedCount': lastCycleItemTradedCount}))
            if self.uiAdapter.selfAdaptionShop.tabIdx == uiConst.SELF_ADAPTION_SHOP_TAB_TYPE_SELL:
                predictPrice = dynamicShop.getBuyPrice(dynamicShopType, changePriceCount, minPrice, maxPrice, nowPrice, itemTradedChangePriceCount, itemTradedChangePriceType, itemTradedChangePriceValue, count)
            else:
                predictPrice = dynamicShop.getSellPrice(changePriceCount, minPrice, maxPrice, nowPrice, itemTradedChangePriceCount, itemTradedChangePriceType, itemTradedChangePriceValue, count)
            return predictPrice

    def handleYesBtnClick(self, *args):
        p = BigWorld.player()
        if self.uiAdapter.selfAdaptionShop.tabIdx == uiConst.SELF_ADAPTION_SHOP_TAB_TYPE_BUY:
            p.cell.dynamicShopBuy(self.uiAdapter.selfAdaptionShop.shopId, self.uiAdapter.selfAdaptionShop.selectSetId, self.tradeCount, False)
        else:
            p.cell.dynamicShopSell(self.uiAdapter.selfAdaptionShop.shopId, self.uiAdapter.selfAdaptionShop.selectSetId, self.tradeCount, False)
        self.hide()

    def handleNoBtnClick(self, *args):
        self.hide()

    def numberLimitCallback(self, *args):
        isMaxLimit = args[3][0].GetBool()
        if isMaxLimit:
            msgId = GMDD.data.SELF_ADAPTION_SHOP_MAX_COUNT_BUY if self.uiAdapter.selfAdaptionShop.tabIdx == uiConst.SELF_ADAPTION_SHOP_TAB_TYPE_BUY else GMDD.data.SELF_ADAPTION_SHOP_MAX_COUNT_SELL
            maxCount = int(self.widget.counter.maxCount)
            BigWorld.player().showGameMsg(msgId, maxCount)

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        self.getFrameInfo()
        if self.uiAdapter.selfAdaptionShop.tabIdx == uiConst.SELF_ADAPTION_SHOP_TAB_TYPE_BUY:
            count = self.frameInfo['count']
        else:
            count = p.inv.countItemInPages(uiUtils.getParentId(self.frameInfo['itemId']), enableParentCheck=True)
            if DSID.data.get(self.frameInfo['setId'], {}).get('isInventory', 0):
                count = min(self.frameInfo['count'], count)
        self.frameInfo['count'] = 1
        self.widget.itemSlot.setItemSlotData(self.frameInfo)
        self.widget.txtItemName.htmlText = self.frameInfo['name']
        self.widget.txtPrice.text = str(self.frameInfo['price'])
        setId = self.frameInfo['setId']
        currencyType = self.frameInfo['priceType']
        if self.uiAdapter.selfAdaptionShop.tabIdx == uiConst.SELF_ADAPTION_SHOP_TAB_TYPE_BUY:
            currencyId = DSID.data.get(setId, {}).get('currencyList', [0, 0])[0] if currencyType == gametypes.DYNAMIC_SHOP_CURRENCY_TYPE_ITEM else DSID.data.get(setId, {}).get('currencyId', 0)
        else:
            currencyId = DSID.data.get(setId, {}).get('currencyId', 0)
        self.widget.txtRemainCount.text = str(count) if DSID.data.get(setId, {}).get('isInventory', 0) else gameStrings.SELF_ADAPTION_SHOP_TXT_DESC_NO_LIMIT
        itemId = self.frameInfo['itemId']
        count = min(count, ID.data.get(itemId, {}).get('mwrap', 999))
        count = min(count, DSID.data.get(setId, {}).get('tradeLimitCnt', 999))
        count = min(count, const.DYNAMIC_SHOP_MAX_TRADE_COUNT)
        self.widget.counter.maxCount = count
        self.widget.itemIcon.visible = False
        self.widget.itemIcon.fitSize = True
        self.widget.itemIcon2.visible = False
        self.widget.itemIcon2.fitSize = True
        self.widget.bonusIcon.visible = True
        self.widget.bonusIcon2.visible = True
        if currencyType == gametypes.DYNAMIC_SHOP_CURRENCY_TYPE_CASH_BIND_CASH:
            if currencyId in (gametypes.DYNAMIC_SHOP_BUY_BIND_CASH_FIRST, gametypes.DYNAMIC_SHOP_BUY_ONLY_BIND_CASH):
                self.widget.bonusIcon.bonusType = 'bindCash'
                self.widget.bonusIcon2.bonusType = 'bindCash'
            else:
                self.widget.bonusIcon.bonusType = 'cash'
                self.widget.bonusIcon2.bonusType = 'cash'
        elif currencyType == gametypes.DYNAMIC_SHOP_CURRENCY_TYPE_FAME:
            self.widget.bonusIcon.bonusType = 'fame'
            self.widget.bonusIcon.tip = FD.data.get(currencyId, {}).get('name', '')
            self.widget.bonusIcon2.bonusType = 'fame'
            self.widget.bonusIcon2.tip = FD.data.get(currencyId, {}).get('name', '')
        elif currencyType == gametypes.DYNAMIC_SHOP_CURRENCY_TYPE_ITEM:
            self.widget.itemIcon.visible = True
            self.widget.itemIcon2.visible = True
            self.widget.bonusIcon.visible = False
            self.widget.bonusIcon2.visible = False
            self.widget.itemIcon.loadImage(uiUtils.getItemIconPath(currencyId))
            TipManager.addItemTipById(self.widget.itemIcon, currencyId)
            self.widget.itemIcon2.loadImage(uiUtils.getItemIconPath(currencyId))
            TipManager.addItemTipById(self.widget.itemIcon2, currencyId)
        else:
            self.widget.bonusIcon.bonusType = 'guildContribution'
            self.widget.bonusIcon2.bonusType = 'guildContribution'
        self.refreshPriceInfo()
