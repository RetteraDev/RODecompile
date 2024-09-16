#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/summonFriendShopV2Proxy.o
from gamestrings import gameStrings
import BigWorld
import utils
import events
import gameglobal
import tipUtils
import uiConst
import ui
import const
from asObject import RedPotManager
from uiProxy import UIProxy
from asObject import ASObject
from guis import uiUtils
from helpers import capturePhoto
from gameStrings import gameStrings
from callbackHelper import Functor
from guis.asObject import ASUtils
from guis.asObject import TipManager
from data import sys_config_data as SCD
from data import composite_shop_item_set_data as CSISD
from cdata import composite_shop_trade_data as CSTD
from cdata import game_msg_def_data as GMDD
INVITE_SHOP_ID = 308

class SummonFriendShopV2Proxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SummonFriendShopV2Proxy, self).__init__(uiAdapter)
        self.widget = None
        self.inviteShopBuyCount = 1
        self.canBuyCount = 0
        self.lastInviteShopSelected = None

    def reset(self):
        self.inviteShopBuyCount = 1
        self.canBuyCount = 0
        self.lastInviteShopSelected = None

    def unRegisterPanel(self):
        self.widget = None
        self.reset()

    def initPanel(self, widget):
        self.widget = widget
        self.initUI()

    def initUI(self):
        p = BigWorld.player()
        self.widget.shopPanel.iconScore.bonusType = 'invite'
        self.widget.shopPanel.count.text = str(p.invitePoint)
        self.widget.shopPanel.buyBtn.addEventListener(events.MOUSE_CLICK, self.showHelp, False, 0, True)
        self.widget.shopPanel.scrollList.itemRenderer = 'SummonFriendShopV2_Item'
        self.widget.shopPanel.scrollList.barAlwaysVisible = True
        self.widget.shopPanel.scrollList.lableFunction = self.inviteShopLabelFun
        self.widget.shopPanel.scrollList.column = 3
        self.widget.shopPanel.scrollList.itemWidth = 244
        self.widget.shopPanel.scrollList.itemHeight = 155

    def refreshInfo(self):
        if not self.widget:
            return
        else:
            p = BigWorld.player()
            self.lastInviteShopSelected = None
            self.widget.shopPanel.count.text = str(p.invitePoint)
            itemList = self.getInviteShopItemList()
            self.widget.shopPanel.scrollList.dataArray = itemList
            self.widget.shopPanel.scrollList.validateNow()
            return

    def showHelp(self, *args):
        gameglobal.rds.ui.showHelpByKey(304)

    def inviteShopLabelFun(self, *args):
        data = ASObject(args[3][0])
        mc = ASObject(args[3][1])
        mc.name = str(int(data.compositeId))
        mc.selBg.visible = False
        mc.selBg.mouseEnabled = False
        mc.addEventListener(events.MOUSE_ROLL_OVER, self.onItemRollOver, False, 0, True)
        mc.addEventListener(events.MOUSE_ROLL_OUT, self.onItemRollOut, False, 0, True)
        mc.addEventListener(events.MOUSE_CLICK, self.onInviteShopItemClick, True, 0, True)
        if data.tag == '':
            mc.basicBox.itemLabel.visible = False
        elif data.tag == 'new':
            mc.basicBox.itemLabel.gotoAndStop('new')
        elif data.tag == 'hot':
            mc.basicBox.itemLabel.gotoAndStop('hot')
        mc.basicBox.itemSlot.setItemSlotData(data)
        mc.basicBox.itemSlot.dragable = False
        mc.basicBox.priceValue.textField.text = str(int(data.invitePoint))
        mc.basicBox.itemName.nameText.htmlText = data.itemName

    def onItemRollOver(self, *args):
        e = ASObject(args[3][0])
        mc = e.currentTarget
        mc.gotoAndStop('over')
        mc.overBg.mouseEnabled = False
        mc.overBg.visible = False
        compositeId = int(mc.name)
        cfgInfo = CSTD.data.get(compositeId, {})
        if not cfgInfo:
            return
        p = BigWorld.player()
        invitePoint = cfgInfo.get('consumeInvitePoint', 0)
        self.canBuyCount = p.invitePoint / invitePoint
        mc.counter.minCount = 0
        mc.counter.maxCount = max(1, self.canBuyCount)
        if self.lastInviteShopSelected:
            if e.currentTarget.name != self.lastInviteShopSelected.name:
                mc.counter.count = 1
            else:
                mc.counter.count = self.inviteShopBuyCount
        else:
            mc.counter.count = 1
        mc.counter.addEventListener(events.EVENT_COUNT_CHANGE, self.inviteShopCountChange, False, 0, True)
        mc.buyBtn.addEventListener(events.MOUSE_CLICK, self.buyInviteShopItem, False, 0, True)

    def inviteShopCountChange(self, *args):
        e = ASObject(args[3][0])
        if self.lastInviteShopSelected:
            if self.lastInviteShopSelected.name == e.currentTarget.parent.name:
                self.inviteShopBuyCount = int(e.currentTarget.count)

    def buyInviteShopItem(self, *args):
        e = ASObject(args[3][0])
        counter = e.currentTarget.parent.counter
        self.inviteShopBuyCount = int(counter.count)
        if self.inviteShopBuyCount == 0:
            if self.canBuyCount == 0:
                BigWorld.player().showGameMsg(GMDD.data.INVITE_POINT_NOT_ENOUGH, ())
            counter.count = 1
        if self.inviteShopBuyCount > self.canBuyCount:
            BigWorld.player().showGameMsg(GMDD.data.INVITE_POINT_NOT_ENOUGH, ())
            return
        compositeId = int(e.currentTarget.parent.name)
        cfgData = CSTD.data.get(compositeId, {})
        if not cfgData:
            return
        canBuyCount = self.getCompositeRemainBuyCount(compositeId)
        itemId = cfgData.get('itemId', 0)
        itemInfo = uiUtils.getGfxItemById(itemId)
        if self.inviteShopBuyCount > canBuyCount:
            msg = self._getLimitStr(compositeId)
            gameglobal.rds.ui.messageBox.showMsgBox(msg)
            return
        frameInfo = {}
        itemInfo['itemId'] = cfgData.get('itemId', 0)
        itemInfo['price'] = cfgData.get('consumeInvitePoint', 0)
        itemInfo['count'] = self.inviteShopBuyCount
        itemInfo['bonusType'] = 'invite'
        frameInfo['itemInfo'] = itemInfo
        yesFun = Functor(self.yesFun, compositeId, self.inviteShopBuyCount)
        frameInfo['yesFun'] = yesFun
        frameInfo['yesLabel'] = gameStrings.TEXT_SUMMONFRIENDNEWPROXY_502
        frameInfo['noLabel'] = gameStrings.TEXT_PLAYRECOMMPROXY_494_1
        gameglobal.rds.ui.itemBuyConfirm.show(frameInfo)

    def yesFun(self, id, count):
        BigWorld.player().cell.buyItemWithInvitePoint(id, count)

    def getCompositeRemainBuyCount(self, compositeId):
        p = BigWorld.player()
        dataKey = self._getCompositeItemLimitKey(compositeId)
        if dataKey not in p.compositeShopItemBuyLimit:
            buyCount = 0
            lastBuyTime = 0
        else:
            buyCount, lastBuyTime = p.compositeShopItemBuyLimit[dataKey]
        buyLimitType = CSTD.data.get(compositeId, {}).get('buyLimitType', 0)
        buyLimitCount = CSTD.data.get(compositeId, {}).get('buyLimitCount', -1)
        if lastBuyTime:
            samePeriod = False
            now = utils.getNow()
            if buyLimitType == const.COMPOSITE_BUY_LIMIT_TYPE_DAY:
                samePeriod = utils.isSameDay(lastBuyTime, now)
            elif buyLimitType == const.COMPOSITE_BUY_LIMIT_TYPE_WEEK:
                samePeriod = utils.isSameWeek(lastBuyTime, now)
            elif buyLimitType == const.COMPOSITE_BUY_LIMIT_TYPE_MONTH:
                samePeriod = utils.isSameMonth(lastBuyTime, now)
            elif buyLimitType == const.COMPOSITE_BUY_LIMIT_TYPE_FOREVER:
                samePeriod = True
            if not samePeriod:
                buyCount = 0
        return buyLimitCount - buyCount

    def _getCompositeItemLimitKey(self, compositeId):
        compositeData = CSTD.data[compositeId]
        if 'buyLimitGroup' in compositeData:
            return 'g%d' % (compositeData['buyLimitGroup'],)
        else:
            return 'i%d' % (compositeId,)

    def _getLimitStr(self, compositeId):
        ret = ''
        buyLimitType = CSTD.data.get(compositeId, {}).get('buyLimitType', 0)
        buyLimitCount = CSTD.data.get(compositeId, {}).get('buyLimitCount', -1)
        if buyLimitType != const.COMPOSITE_BUY_LIMIT_TYPE_NO:
            remainBuyCount = max(0, self.getCompositeRemainBuyCount(compositeId))
            if remainBuyCount <= 0:
                remainBuyCountStr = uiUtils.toHtml(str(remainBuyCount), '#F43804')
            else:
                remainBuyCountStr = str(remainBuyCount)
            if buyLimitType == const.COMPOSITE_BUY_LIMIT_TYPE_DAY:
                ret = gameStrings.TEXT_COMPOSITESHOPPROXY_530 % (remainBuyCountStr, buyLimitCount)
            elif buyLimitType == const.COMPOSITE_BUY_LIMIT_TYPE_WEEK:
                ret = gameStrings.TEXT_COMPOSITESHOPPROXY_532 % (remainBuyCountStr, buyLimitCount)
            elif buyLimitType == const.COMPOSITE_BUY_LIMIT_TYPE_MONTH:
                ret = gameStrings.TEXT_COMPOSITESHOPPROXY_534 % (remainBuyCountStr, buyLimitCount)
            elif buyLimitType == const.COMPOSITE_BUY_LIMIT_TYPE_FOREVER:
                ret = gameStrings.TEXT_COMPOSITESHOPPROXY_536 % (remainBuyCountStr, buyLimitCount)
        return ret

    def onItemRollOut(self, *args):
        e = ASObject(args[3][0])
        mc = e.currentTarget
        mc.gotoAndStop('normal')

    def onInviteShopItemClick(self, *args):
        e = ASObject(args[3][0])
        if self.lastInviteShopSelected:
            self.lastInviteShopSelected.selBg.visible = False
            if self.lastInviteShopSelected.name != e.currentTarget.name:
                self.inviteShopBuyCount = 1
        e.currentTarget.selBg.visible = True
        self.lastInviteShopSelected = e.currentTarget

    def getInviteShopItemList(self):
        itemList = []
        list0 = CSISD.data.get(INVITE_SHOP_ID, [])
        for value in list0:
            compositeId = value.get('compositeId', 0)
            cfgData = CSTD.data.get(compositeId, {})
            itemId = cfgData.get('itemId', 0)
            itemInfo = uiUtils.getGfxItemById(itemId)
            itemInfo['tag'] = cfgData.get('tag', '')
            itemInfo['itemName'] = uiUtils.getItemColorName(itemId)
            itemInfo['invitePoint'] = cfgData.get('consumeInvitePoint', 1)
            itemInfo['buyLimitType'] = cfgData.get('buyLimitType', 0)
            itemInfo['buyLimitCount'] = cfgData.get('buyLimitCount', 0)
            itemInfo['compositeId'] = compositeId
            itemList.append(itemInfo)

        return itemList
