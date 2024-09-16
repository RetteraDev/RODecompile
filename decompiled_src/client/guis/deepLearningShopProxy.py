#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/deepLearningShopProxy.o
import BigWorld
import utils
import events
import uiConst
import gameglobal
import gametypes
from uiProxy import UIProxy
from asObject import ASObject
from asObject import ASUtils
from guis import uiUtils
from gameStrings import gameStrings
from data import sys_config_data as SCD
from data import item_data as ID
from cdata import deep_learning_data_apply_item_data as DLDAID
ITEM_COUNT_MAX = 10

class DeepLearningShopProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(DeepLearningShopProxy, self).__init__(uiAdapter)
        self.widget = None
        self.callback = None
        self.callbackPush = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_DEEP_LEARNING_SHOP, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_DEEP_LEARNING_SHOP:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_DEEP_LEARNING_SHOP)
        p = BigWorld.player()
        if p.inWorld:
            p.cell.operateDeepLearningDataApplyShop(gametypes.DEEP_LEARNING_DATA_APPLY_SHOP_CLOSE)

    def reset(self):
        self.callback = None

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.help.visible = False
        ASUtils.setHitTestDisable(self.widget.shopNameT, True)

    def show(self):
        p = BigWorld.player()
        if p._isSoul():
            return
        if not gameglobal.rds.configData.get('enableDeepLearningDataApply', False):
            return
        if self.widget:
            self.refreshInfo()
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_DEEP_LEARNING_SHOP)
        p.cell.operateDeepLearningDataApplyShop(gametypes.DEEP_LEARNING_DATA_APPLY_SHOP_OPEN)

    def refreshInfo(self):
        if not self.widget:
            return
        self.updateLeftTime()
        self.updateDiscountItems()
        self.widget.desc.text = SCD.data.get('DEEP_LEARNING_DESC', '')
        p = BigWorld.player()
        if hasattr(p, 'unbindCoin') and hasattr(p, 'bindCoin') and hasattr(p, 'freeCoin'):
            tianBi = p.unbindCoin + p.bindCoin + p.freeCoin
            self.widget.cashT.text = tianBi

    def _onRechargeBtnClick(self, e):
        p = BigWorld.player()
        p.openRechargeFunc()

    def handleBuyBtnClick(self, *args):
        e = ASObject(args[3][0])
        itemId = e.currentTarget.parent.itemId
        if itemId:
            gameglobal.rds.ui.deepLearningMsgBox.show(itemId)

    def handleRollOverItem(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        itemMc.gotoAndStop('over')
        if itemMc.leftNum:
            itemMc.buyBtn.label = gameStrings.BACK_FLOW_DISCOUNT_BUY_BTN_LABEL
            itemMc.buyBtn.enabled = True
        else:
            itemMc.buyBtn.label = gameStrings.BACK_FLOW_DISCOUNT_BUY_BTN_ENABLED_LABEL
            itemMc.buyBtn.enabled = False
        ASUtils.setHitTestDisable(itemMc.overBg, True)
        itemMc.buyBtn.addEventListener(events.MOUSE_CLICK, self.handleBuyBtnClick, False, 0, True)

    def handleRollOutItem(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        itemMc.gotoAndStop('normal')

    def updateLeftTime(self):
        if not self.widget:
            self.stopCallback()
            return
        p = BigWorld.player()
        beginTime = p.deepLearningData.beginTime
        curTime = utils.getNow()
        second = SCD.data.get('deepLearningDataApplyInfo', {}).get('durationTime', 0)
        endTime = beginTime + second
        leftTime = max(endTime - curTime, 0)
        if leftTime < 0:
            self.stopCallback()
            return
        srtTime = utils.formatDurationShortVersion(leftTime)
        self.widget.countDownT.htmlText = gameStrings.BACK_FLOW_LEFT_TIME_TITLE % uiUtils.toHtml(srtTime, '#d34024')
        self.callback = BigWorld.callback(1, self.updateLeftTime)

    def stopCallback(self):
        if self.callback:
            BigWorld.cancelCallback(self.callback)
            self.callback = None

    def getItemInfo(self):
        p = BigWorld.player()
        itemIds = p.deepLearningData.item
        itemList = []
        for id, items in itemIds.iteritems():
            itemId = items.itemId
            buyCount = items.buyCount
            idData = ID.data.get(itemId, {})
            itemName = idData.get('name', '')
            deepData = DLDAID.data.get(itemId, {})
            priceVal = deepData.get('nowPrice', 0)
            originalPrice = int(deepData.get('sourcePrice', 0))
            totalLimit = int(deepData.get('maxBuyCount', 1))
            leftNum = max(0, totalLimit - buyCount)
            if originalPrice:
                discountRate = int(round(priceVal * 100.0 / originalPrice))
                intPart = int(discountRate / 10)
                floatPart = int(discountRate - intPart * 10)
                if floatPart:
                    subText = '.%d%s' % (floatPart, gameStrings.ACTIVITY_SHOP_PROXY_DISCOUNT)
                else:
                    subText = gameStrings.ACTIVITY_SHOP_PROXY_DISCOUNT
            else:
                intPart = 0
                subText = 0
            itemInfo = {}
            itemInfo['itemId'] = itemId
            itemInfo['itemName'] = itemName
            itemInfo['leftNum'] = leftNum
            itemInfo['totalLimit'] = totalLimit
            itemInfo['priceVal'] = priceVal
            itemInfo['originalPrice'] = originalPrice
            itemInfo['intPart'] = str(intPart)
            itemInfo['subText'] = subText
            itemList.append(itemInfo)

        return itemList

    def updateDiscountItems(self):
        if not self.widget:
            return
        itemList = self.getItemInfo()
        for i in xrange(ITEM_COUNT_MAX):
            itemMc = self.widget.itemList.getChildByName('item%d' % i)
            if i <= len(itemList):
                itemMc.visible = True
                itemData = itemList[i]
                itemMc.itemId = itemData['itemId']
                itemMc.leftNum = itemData['leftNum']
                if itemMc.leftNum:
                    color = '#FFFFE5'
                else:
                    color = '#d34024'
                itemMc.itemNum.htmlText = '%s/%d' % (uiUtils.toHtml(itemMc.leftNum, color), itemData['totalLimit'])
                itemMc.itemSlot.fitSize = True
                itemMc.itemSlot.dragable = False
                itemMc.itemSlot.setItemSlotData(uiUtils.getGfxItemById(itemMc.itemId))
                if not itemData['intPart'] and not itemData['subText']:
                    itemMc.discountLabel.visible = False
                else:
                    itemMc.discountLabel.visible = True
                    itemMc.discountLabel.mainText.text = itemData['intPart']
                    itemMc.discountLabel.subText.text = itemData['subText']
                itemMc.itemName.text = itemData['itemName']
                itemMc.costMc.costCount.text = itemData['priceVal']
                itemMc.costMc.costIcon.bonusType = 'tianbi'
                if itemData['originalPrice']:
                    itemMc.priceOrig.visible = True
                    itemMc.priceOrig.textField.text = gameStrings.BACK_FLOW_DISCOUNT_BUY_ITEM_DESC % itemData['originalPrice']
                    itemMc.priceOrig.textField.width = itemMc.priceOrig.textField.textWidth + 4
                    itemMc.priceOrig.delFlag.width = itemMc.priceOrig.textField.width
                    itemMc.priceOrig.delFlag.x = 0
                else:
                    itemMc.priceOrig.visible = False
                itemMc.addEventListener(events.MOUSE_ROLL_OVER, self.handleRollOverItem, False, 0, True)
                itemMc.addEventListener(events.MOUSE_ROLL_OUT, self.handleRollOutItem, False, 0, True)
            else:
                itemMc.visible = False

    def checkTimeEnd(self):
        p = BigWorld.player()
        beginTime = p.deepLearningData.beginTime
        curTime = utils.getNow()
        second = SCD.data.get('deepLearningDataApplyInfo', {}).get('durationTime', 0)
        endTime = beginTime + second
        leftTime = max(endTime - curTime, 0)
        if leftTime <= 0:
            return True
        return False

    def checkTimeDownPush(self):
        p = BigWorld.player()
        beginTime = p.deepLearningData.beginTime
        second = SCD.data.get('deepLearningDataApplyInfo', {}).get('durationTime', 0)
        endTime = beginTime + second
        curTime = utils.getNow()
        leftTime = max(endTime - curTime, 0)
        if leftTime <= 0:
            self.stopCallbackPush()
            p.deepLearningData = {}
            gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
            if self.widget:
                self.hide()
            return
        timePush = SCD.data.get('deepLearningTimeDownPush', 900)
        if leftTime == timePush:
            if not self.widget:
                self.show()
        if self.callbackPush:
            self.stopCallbackPush()
        self.callbackPush = BigWorld.callback(1, self.checkTimeDownPush)

    def stopCallbackPush(self):
        if self.callbackPush:
            BigWorld.cancelCallback(self.callbackPush)
            self.callbackPush = None
