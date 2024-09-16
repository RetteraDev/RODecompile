#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/activitySaleDailyGiftProxy.o
from gamestrings import gameStrings
import BigWorld
import events
import utils
from gamestrings import gameStrings
from callbackHelper import Functor
import gametypes
import math
from appSetting import Obj as AppSettings
import keys
import gameglobal
import random
from uiProxy import UIProxy
from guis import uiUtils
from guis import ui
from guis.asObject import ASObject
from data import daily_welfare_item_data as DWID
from data import game_msg_data as GMD
from data import sys_config_data as SCD
from data import consumable_item_data as CID
from data import bonus_data as BD
from data import bonus_set_data as BSD
from data import bonus_box_data as BBD
from cdata import game_msg_def_data as GMDD
DAILY_GIFT_MAX_CNT = 3
ITEM_MAX_CNT = 4
LINE_ADD_WIDTH = 5
TEXT_COLOR_LIST = ['#FF4343', '#FFFD56', '#BB3FC3']

class ActivitySaleDailyGiftProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ActivitySaleDailyGiftProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()

    def reset(self):
        self.itemList = {}
        self.keyIndexMap = {}

    def initPanel(self, widget):
        if self.getRedPointVisible():
            AppSettings[keys.SET_WELFARE_DAILYGIFT_SAMEDAY] = str(utils.getNow())
            AppSettings.save()
        self.widget = widget
        self.widget.mainMc.buyBtn0.addEventListener(events.BUTTON_CLICK, self.handleBuyOneDayClick, False, 0, True)
        self.widget.mainMc.chargeButton.addEventListener(events.BUTTON_CLICK, self.handleChargeClick, False, 0, True)
        self.addEvent(events.EVENT_TIANBI_COIN_CHANGED, self.refreshCoin)
        self.refreshInfo()
        self.refreshCoin()
        self.uiAdapter.activitySale.refreshInfo()

    def unRegisterDailyGift(self):
        self.widget = None
        self.delEvent(events.EVENT_TIANBI_COIN_CHANGED, self.refreshCoin)
        self.reset()

    def refreshInfo(self):
        if not self.widget:
            return
        idx = 0
        for key, info in DWID.data.iteritems():
            giftMc = getattr(self.widget.mainMc, 'gift%d' % idx)
            self.keyIndexMap[key] = idx
            giftMc.txtGiftName.htmlText = uiUtils.toHtml(gameStrings.ACTIVITY_SALE_DAILY_GIFT_NOW_PRICE % info.get('nowPrice', 0), TEXT_COLOR_LIST[idx])
            giftMc.txtSourcePrice.text = gameStrings.ACTIVITY_SALE_DAILY_GIFT_SOURCE_PRICE % info.get('sourcePrice', 0)
            costTianbi = DWID.data.get(key, {}).get('nowPrice', 0)
            costSourceTianbi = DWID.data.get(key, {}).get('sourcePrice', 1)
            disCountRate = costTianbi * 1.0 / costSourceTianbi * 10
            intPart = int(disCountRate)
            floatPart = math.ceil((disCountRate - intPart) * 10)
            disCountRateStr = '%d.%d' % (intPart, floatPart) if floatPart else str(intPart)
            giftMc.txtDiscount.text = gameStrings.ACTIVITY_SALE_DAILY_GIFT_DISCOUNT % disCountRateStr
            itemList, extraItemList = self.getBonusItems(key)
            line = giftMc.line
            line.width = giftMc.txtSourcePrice.textWidth
            line.x = giftMc.txtSourcePrice.x + giftMc.txtSourcePrice.width / 2 - giftMc.txtSourcePrice.textWidth / 2
            line.width = line.width + 2 * LINE_ADD_WIDTH
            line.x = line.x - LINE_ADD_WIDTH
            for i in xrange(ITEM_MAX_CNT):
                itemMc = getattr(giftMc, 'item%d' % i)
                if i < len(itemList):
                    itemMc.visible = True
                    itemMc.slot.dragable = False
                    itemMc.slot.setItemSlotData(uiUtils.getGfxItemById(itemList[i][0], itemList[i][1]))
                else:
                    itemMc.visible = False

            if gameglobal.rds.configData.get('enableDailyWelfareActivityOptimize', False):
                giftMc.probDesc.text = gameStrings.TEXT_ACTIVITYSALEDAILYGIFTPROXY_99 % info.get('bonusProb', '')
                giftMc.refreshBtn.visible = True
                giftMc.refreshTxt.visible = True
            else:
                giftMc.probDesc.text = gameStrings.TEXT_ACTIVITYSALEDAILYGIFTPROXY_103
                giftMc.refreshBtn.visible = False
                giftMc.refreshTxt.visible = False
            for i in xrange(ITEM_MAX_CNT):
                itemMc = getattr(giftMc, 'item%d' % (i + ITEM_MAX_CNT))
                if i < len(extraItemList):
                    itemMc.visible = True
                    itemMc.slot.dragable = False
                    itemMc.slot.setItemSlotData(uiUtils.getGfxItemById(extraItemList[i][0], extraItemList[i][1]))
                else:
                    itemMc.visible = False

            if idx >= DAILY_GIFT_MAX_CNT:
                break
            idx += 1
            btnEnabled = self.buySingleItemValid(key)
            if btnEnabled:
                giftMc.buyBtn.enabled = True
                giftMc.buyBtn.addEventListener(events.BUTTON_CLICK, self.handleBuyItemClick, False, 0, True)
                giftMc.buyBtn.key = key
                giftMc.refreshBtn.enabled = True
                giftMc.refreshBtn.addEventListener(events.BUTTON_CLICK, self.handleRefreshItemClick, False, 0, True)
                giftMc.refreshBtn.key = key
            else:
                giftMc.buyBtn.enabled = False
                giftMc.refreshBtn.enabled = False

        if gameglobal.rds.configData.get('enableDailyWelfareActivityOptimize', False):
            self.widget.mainMc.txtLeftDay.visible = False
        else:
            leftDay = self.getLeftDay()
            if leftDay:
                self.widget.mainMc.txtLeftDay.visible = True
                self.widget.mainMc.txtLeftDay.text = gameStrings.ACTIVITY_SALE_DAILY_GIFT_LEFT_DAT % leftDay
            else:
                self.widget.mainMc.txtLeftDay.visible = False
        self.widget.mainMc.buyBtn0.enabled = self.buyOneDayValid()

    def refreshCoin(self):
        if not self.widget:
            return
        p = BigWorld.player()
        tianbi = format(p.unbindCoin + p.bindCoin + p.freeCoin, ',')
        unBindTianbi = uiUtils.toHtml(gameStrings.TEXT_ACTIVITYSALEDAILYGIFTPROXY_145 % format(p.unbindCoin, ','), '#79c725')
        self.widget.mainMc.cashNum.htmlText = '%s%s' % (tianbi, unBindTianbi)

    @ui.checkInventoryLock()
    def handleBuyItemClick(self, *args):
        p = BigWorld.player()
        e = ASObject(args[3][0])
        key = int(e.currentTarget.key)
        costTianbi = DWID.data.get(key, {}).get('nowPrice', 0)
        text = GMD.data.get(GMDD.data.ACTIVITY_SALE_DAILY_GIFT_CONFIM, {}).get('text', '%d') % costTianbi
        if gameglobal.rds.configData.get('enableDailyWelfareActivityOptimize', False):
            itemId = self.itemList.get(key)
            fun = Functor(p.base.dailyWelfareSingleBuyOptimize, key, itemId, p.cipherOfPerson)
        else:
            fun = Functor(p.base.dailyWelfareSingleBuy, key, p.cipherOfPerson)
        self.uiAdapter.messageBox.showYesNoMsgBox(text, fun)

    def handleRefreshItemClick(self, *args):
        p = BigWorld.player()
        e = ASObject(args[3][0])
        key = int(e.currentTarget.key)
        oldItemId = self.itemList.get(key)
        itemIdList = DWID.data.get(key, {}).get('itemIdList')
        index = itemIdList.index(oldItemId)
        newItemId = itemIdList[index + 1] if index < len(itemIdList) - 1 else itemIdList[0]
        self.itemList[key] = newItemId
        itemList, extraItemList = self.getBonusItemsById(newItemId)
        giftMc = getattr(self.widget.mainMc, 'gift%d' % self.keyIndexMap.get(key))
        for i in xrange(ITEM_MAX_CNT):
            itemMc = getattr(giftMc, 'item%d' % i)
            if i < len(itemList):
                itemMc.visible = True
                itemMc.slot.setItemSlotData(uiUtils.getGfxItemById(itemList[i][0], itemList[i][1]))
            else:
                itemMc.visible = False

        for i in xrange(ITEM_MAX_CNT):
            itemMc = getattr(giftMc, 'item%d' % (i + ITEM_MAX_CNT))
            if i < len(extraItemList):
                itemMc.visible = True
                itemMc.slot.setItemSlotData(uiUtils.getGfxItemById(extraItemList[i][0], extraItemList[i][1]))
            else:
                itemMc.visible = False

    @ui.checkInventoryLock()
    def handleBuyOneDayClick(self, *args):
        totalPrice = 0
        for key, info in DWID.data.iteritems():
            totalPrice += info.get('nowPrice', 0)

        p = BigWorld.player()
        text = GMD.data.get(GMDD.data.ACTIVITY_SALE_DAILY_GIFT_CONFIM, {}).get('text', '%d') % totalPrice
        if gameglobal.rds.configData.get('enableDailyWelfareActivityOptimize', False):
            itemlist = self.itemList.values()
            fun = Functor(p.base.dailyWelfareMassBuyOptimize, itemlist, p.cipherOfPerson)
        else:
            fun = Functor(p.base.dailyWelfareMassBuy, gametypes.DAILY_WELFARE_BUY_TYPE_ONE_DAY, p.cipherOfPerson)
        self.uiAdapter.messageBox.showYesNoMsgBox(text, fun)

    @ui.checkInventoryLock()
    def handleBuySevenDayClick(self, *args):
        p = BigWorld.player()
        totalPrice = SCD.data.get('dailyWelfareBuyData', {}).get('sevenPrice', 0)
        text = GMD.data.get(GMDD.data.ACTIVITY_SALE_DAILY_GIFT_CONFIM, {}).get('text', '%d') % totalPrice
        fun = Functor(p.base.dailyWelfareMassBuy, gametypes.DAILY_WELFARE_BUY_TYPE_SEVEN_DAY, p.cipherOfPerson)
        self.uiAdapter.messageBox.showYesNoMsgBox(text, fun)

    def handleChargeClick(self, *args):
        self.uiAdapter.tianyuMall.onOpenChargeWindow()

    def getLeftDay(self):
        p = BigWorld.player()
        dailyGiftInfo = getattr(p, 'dailyGiftInfo', {})
        sevenDayInfo = dailyGiftInfo.get(gametypes.DAILY_WELFARE_BUY_TYPE_SEVEN_DAY, {})
        return sevenDayInfo.get(gametypes.DAILY_WELFARE_BUY_TYPE_SEVEN_DAY_DURATION, 0) - sevenDayInfo.get(gametypes.DAILY_WELFARE_BUY_TYPE_SEVEN_DAY_GOT, 0)

    def buyOneDayValid(self):
        p = BigWorld.player()
        dailyGiftInfo = getattr(p, 'dailyGiftInfo', {})
        if not dailyGiftInfo:
            return True
        now = utils.getNow()
        buyOneDayTime = dailyGiftInfo.get(gametypes.DAILY_WELFARE_BUY_TYPE_ONE_DAY, 0)
        if buyOneDayTime and utils.isSameDay(now, buyOneDayTime):
            return False
        singleItemInfo = dailyGiftInfo.get(gametypes.DAILY_WELFARE_BUY_TYPE_SINGLE, {})
        for key, time in singleItemInfo.iteritems():
            if utils.isSameDay(now, time):
                return False

        return True

    def buySingleItemValid(self, key):
        p = BigWorld.player()
        dailyGiftInfo = getattr(p, 'dailyGiftInfo', {})
        if not dailyGiftInfo:
            return True
        now = utils.getNow()
        buyOneDayTime = dailyGiftInfo.get(gametypes.DAILY_WELFARE_BUY_TYPE_ONE_DAY, 0)
        if buyOneDayTime and utils.isSameDay(now, buyOneDayTime):
            return False
        singleItemInfo = dailyGiftInfo.get(gametypes.DAILY_WELFARE_BUY_TYPE_SINGLE, {})
        itemBuyTime = singleItemInfo.get(key, 0)
        if itemBuyTime and utils.isSameDay(now, itemBuyTime):
            return False
        return True

    @property
    def redPointVisible(self):
        lastTimeStr = AppSettings.get(keys.SET_WELFARE_DAILYGIFT_SAMEDAY, '')
        if not lastTimeStr:
            return True
        return not utils.isSameDay(utils.getNow(), int(lastTimeStr))

    def getRedPointVisible(self):
        if not gameglobal.rds.configData.get('enableDailyWelfareActivityOptimize', False):
            return False
        p = BigWorld.player()
        dailyGiftInfo = getattr(p, 'dailyGiftInfo', {})
        singleItemInfo = dailyGiftInfo.get(gametypes.DAILY_WELFARE_BUY_TYPE_SINGLE, {})
        buyOneDayTime = dailyGiftInfo.get(gametypes.DAILY_WELFARE_BUY_TYPE_ONE_DAY, 0)
        if not dailyGiftInfo:
            return self.redPointVisible
        now = utils.getNow()
        for key, time in singleItemInfo.iteritems():
            if utils.isSameDay(now, time):
                return False

        if buyOneDayTime and utils.isSameDay(now, buyOneDayTime):
            return False
        return self.redPointVisible

    def getItemList(self, key):
        bonusIdList = []
        itemList = []
        boxDataInfo = BBD.data.get(key, [])
        for boxData in boxDataInfo:
            bonusSets = boxData.get('bonusSets', [])
            bonusIdList = [ x for x, _ in bonusSets ]

        for bonusId in bonusIdList:
            for setInfo in BSD.data.get(bonusId, []):
                itemList.append((setInfo.get('bonusId', 0), setInfo.get('minBonusNum', 1)))

        return itemList

    def getBonusItems(self, id):
        p = BigWorld.player()
        dailyGiftInfo = getattr(p, 'dailyGiftInfo', {})
        if gameglobal.rds.configData.get('enableDailyWelfareActivityOptimize', False):
            if self.itemList.has_key(id):
                itemId = self.itemList[id]
            else:
                lastItems = dailyGiftInfo.get(gametypes.DAILY_WELFARE_BUY_TYPE_LAST_ITEMIDS, {})
                itemId = lastItems.get(id, 0)
                if not itemId:
                    itemIdList = DWID.data.get(id, {}).get('itemIdList')
                    itemId = random.choice(itemIdList)
                self.itemList[id] = itemId
        else:
            itemId = DWID.data.get(id, {}).get('itemId', 0)
        return self.getBonusItemsById(itemId)

    def getBonusItemsById(self, itemId):
        bonusId = CID.data.get(itemId, {}).get('bonusId', 0)
        bonusIds = BD.data.get(bonusId, {}).get('bonusIds', (0, 0))
        itemList = self.getItemList(bonusIds[0])
        extraItemList = self.getItemList(bonusIds[1])
        return (itemList, extraItemList)
