#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/guildBusinessShopProxy.o
from gamestrings import gameStrings
import BigWorld
import time
import gameglobal
import uiUtils
import uiConst
import utils
import const
import gametypes
from uiProxy import UIProxy
from data import business_config_data as BCD
from data import sale_business_data as SBD
from data import npc_business_data as NBD
from data import zaiju_data as ZD
from cdata import game_msg_def_data as GMDD
PACKAGE_PAGE = 0
MARKET_PAGE = 1

class GuildBusinessShopProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GuildBusinessShopProxy, self).__init__(uiAdapter)
        self.modelMap = {'getPackageInfo': self.onGetPackageInfo,
         'getMarketInfo': self.onGetMarketInfo,
         'refresh': self.onRefresh,
         'buy': self.onBuy,
         'sell': self.onSell}
        self.mediator = None
        self.tabId = PACKAGE_PAGE
        self.npcId = 0
        self.entityId = 0
        self.salePriceClass = {}
        self.saleReserveInfo = {}
        self.npcSellPriceInfo = {}
        self.npcBuyPriceInfo = {}
        self.lastRefreshTime = 0
        self.refreshCD = 0
        self.timer = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_GUILD_BUSINESS_SHOP, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GUILD_BUSINESS_SHOP:
            self.mediator = mediator

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GUILD_BUSINESS_SHOP)
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()

    def reset(self):
        self.tabId = PACKAGE_PAGE
        self.npcId = 0
        self.entityId = 0
        self.salePriceClass = {}
        self.saleReserveInfo = {}
        self.npcSellPriceInfo = {}
        self.npcBuyPriceInfo = {}
        self.lastRefreshTime = 0
        self.stopTimer()

    def stopTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None

    def show(self, entityId):
        self.entityId = entityId
        if not self.mediator:
            npc = BigWorld.entities.get(self.entityId)
            if npc is not None and npc._isBusinessNpc():
                self.npcId = npc.npcId
                npc.priceVer = 0
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_GUILD_BUSINESS_SHOP)

    def setShopInfo(self, entityId, salePriceClass, saleReserveInfo, npcSellPriceInfo, npcBuyPriceInfo, lastRefreshTime):
        if self.entityId != entityId:
            return
        self.salePriceClass = salePriceClass
        self.saleReserveInfo = saleReserveInfo
        self.npcSellPriceInfo = npcSellPriceInfo
        self.npcBuyPriceInfo = npcBuyPriceInfo
        self.lastRefreshTime = lastRefreshTime
        self.refreshCD = 30

    def refreshShopInfo(self):
        if self.mediator:
            p = BigWorld.player()
            info = {}
            info['own'] = p.getFame(BCD.data.get('businessFameId', 0))
            zjd = ZD.data.get(p._getZaijuNo(), {})
            bagSlotCount = zjd.get('bagSlotCount', 0)
            gameglobal.rds.ui.guildBusinessBag.setBagSlotCount(bagSlotCount)
            info['maxBagNum'] = bagSlotCount - p.zaijuBag.countZaijuBagNum()
            buyStateTips = BCD.data.get('buyStateTips', {})
            npcSellInfo = NBD.data.get(self.npcId, {}).get('npcSellInfo', {})
            itemList = []
            for businessId, unitPrice in npcSellInfo.iteritems():
                itemId = SBD.data.get(businessId, {}).get('itemId', 0)
                if itemId == 0:
                    continue
                itemInfo = uiUtils.getGfxItemById(itemId)
                itemInfo['nameText'] = uiUtils.getItemColorName(itemId)
                itemInfo['businessId'] = businessId
                itemInfo['unitPrice'] = self.npcSellPriceInfo.get(businessId, 0) if businessId in self.npcSellPriceInfo else unitPrice
                itemInfo['buyState'] = 'lv%d' % self.salePriceClass.get(businessId, 0)
                itemInfo['buyStateTips'] = buyStateTips.get(self.salePriceClass.get(businessId, 0), '')
                itemList.append(itemInfo)

            info['itemList'] = itemList
            self.mediator.Invoke('refreshShopInfo', uiUtils.dict2GfxDict(info, True))
            self.stopTimer()
            self.updateTime()

    def onGetPackageInfo(self, *arg):
        self.tabId = PACKAGE_PAGE
        self.refreshPackageInfo()

    def refreshPackageInfo(self):
        if self.tabId != PACKAGE_PAGE:
            return
        if self.mediator:
            p = BigWorld.player()
            info = {}
            saleReserveMargin = BCD.data.get('saleReserveMargin', ())
            maxReserve = NBD.data.get(self.npcId, {}).get('maxReserve', {})
            npcBuyInfo = NBD.data.get(self.npcId, {}).get('npcBuyInfo', {})
            itemList = []
            for businessId, unitPrice in npcBuyInfo.iteritems():
                itemId = SBD.data.get(businessId, {}).get('itemId', 0)
                reserve = maxReserve.get(businessId, 0)
                count = len(p.zaijuBag.searchAllPosByID(itemId, False))
                if itemId == 0 or reserve <= 0 or count <= 0:
                    continue
                itemInfo = uiUtils.getGfxItemById(itemId)
                itemInfo['nameText'] = uiUtils.getItemColorName(itemId)
                itemInfo['businessId'] = businessId
                itemInfo['unitPrice'] = self.npcBuyPriceInfo.get(businessId, 0) if businessId in self.npcBuyPriceInfo else unitPrice
                itemInfo['count'] = str(count)
                saleReserve = min(1.0, 1.0 * self.saleReserveInfo.get(businessId, 0) / reserve)
                itemInfo['sellState'] = 'lv%d' % utils.getListIndexInclude(saleReserve, saleReserveMargin)
                itemInfo['sellStateTips'] = BCD.data.get('sellStateTips', '')
                itemList.append(itemInfo)

            info['itemList'] = itemList
            zjd = ZD.data.get(p._getZaijuNo(), {})
            bagSlotCount = zjd.get('bagSlotCount', 0)
            gameglobal.rds.ui.guildBusinessBag.setBagSlotCount(bagSlotCount)
            zaijuBagNum = p.zaijuBag.countZaijuBagNum()
            info['maxBagNum'] = bagSlotCount - zaijuBagNum
            info['bagSpace'] = '%d/%d' % (zaijuBagNum, bagSlotCount)
            hint = ''
            if p.guildBusiness:
                if utils.isInBusinessZaiju(p):
                    if len(itemList) == 0:
                        hint = uiUtils.getTextFromGMD(GMDD.data.GUILD_BUSINESS_SHOP_EMPTY_BAG, '')
                else:
                    hint = uiUtils.getTextFromGMD(GMDD.data.GUILD_BUSINESS_SHOP_NO_ZAIJU, '')
            else:
                hint = uiUtils.getTextFromGMD(GMDD.data.GUILD_BUSINESS_SHOP_NOT_MAN, '')
            info['hint'] = hint
            self.mediator.Invoke('refreshPackageInfo', uiUtils.dict2GfxDict(info, True))

    def onGetMarketInfo(self, *arg):
        self.tabId = MARKET_PAGE
        self.refreshMarketInfo()

    def refreshMarketInfo(self):
        if self.tabId != MARKET_PAGE:
            return
        if self.mediator:
            info = {}
            saleReserveMargin = BCD.data.get('saleReserveMargin', ())
            maxReserve = NBD.data.get(self.npcId, {}).get('maxReserve', {})
            itemList = []
            for businessId, reserve in maxReserve.iteritems():
                itemId = SBD.data.get(businessId, {}).get('itemId', 0)
                if itemId == 0 or reserve <= 0:
                    continue
                itemInfo = uiUtils.getGfxItemById(itemId)
                itemInfo['nameText'] = uiUtils.getItemColorName(itemId)
                saleReserve = min(1.0, 1.0 * self.saleReserveInfo.get(businessId, 0) / reserve)
                itemInfo['sellState'] = 'lv%d' % utils.getListIndexInclude(saleReserve, saleReserveMargin)
                itemInfo['sellStateTips'] = BCD.data.get('sellStateTips', '')
                itemList.append(itemInfo)

            info['itemList'] = itemList
            self.mediator.Invoke('refreshMarketInfo', uiUtils.dict2GfxDict(info, True))

    def onRefresh(self, *arg):
        BigWorld.player().fetchBusinessNpcInfo(self.entityId)
        self.refreshCD = 30
        self.stopTimer()
        self.updateTime()

    def updateTime(self):
        if self.mediator:
            p = BigWorld.player()
            info = {}
            serverTime = int(p.getServerTime())
            if self.lastRefreshTime == 0:
                info['priceTime'] = ''
                info['reserveTime'] = ''
            else:
                leftTime = self.lastRefreshTime + 5 * const.TIME_INTERVAL_MINUTE - serverTime
                if leftTime < 0:
                    info['priceTime'] = uiUtils.toHtml(gameStrings.TEXT_GUILDBUSINESSSHOPPROXY_229, '#F43804')
                    self.refreshCD = 0
                else:
                    info['priceTime'] = gameStrings.TEXT_GUILDBUSINESSSHOPPROXY_232 % utils.formatTimeStr(leftTime, 'm:s', True, 2, 2)
                tplSec1 = time.localtime(serverTime)
                leftTime = (60 - tplSec1[4]) * 60 - tplSec1[5] - const.GUILD_BUSINESS_HOUR_REFRESH_OFFSET
                if leftTime < 0:
                    if leftTime == -1:
                        BigWorld.player().fetchBusinessNpcInfo(self.entityId)
                    leftTime += const.TIME_INTERVAL_HOUR
                info['reserveTime'] = gameStrings.TEXT_GUILDBUSINESSSHOPPROXY_240 % utils.formatTimeStr(leftTime, 'm:s', True, 2, 2)
            if self.refreshCD <= 0:
                info['label'] = gameStrings.TEXT_GUILDBUSINESSSHOPPROXY_243
                info['enabled'] = True
            else:
                info['label'] = gameStrings.TEXT_GUILDBUSINESSSHOPPROXY_246 % self.refreshCD
                info['enabled'] = False
                self.refreshCD -= 1
            self.mediator.Invoke('updateTime', uiUtils.dict2GfxDict(info, True))
            self.timer = BigWorld.callback(1, self.updateTime)

    def onBuy(self, *arg):
        businessId = int(arg[3][0].GetNumber())
        num = int(arg[3][1].GetNumber())
        p = BigWorld.player()
        saleIds = [businessId] * num
        p.buyBusinessItemFromNpc(self.entityId, saleIds)

    def onSell(self, *arg):
        businessId = int(arg[3][0].GetNumber())
        num = int(arg[3][1].GetNumber())
        p = BigWorld.player()
        itemId = SBD.data.get(businessId, {}).get('itemId', 0)
        positions = p.zaijuBag.searchAllPosByID(itemId, False)[0:num]
        if len(positions) < num:
            p.showGameMsg(GMDD.data.BUSINESS_SELL_ITEM_NOT_ENOUGH, ())
            return
        saleIds = [businessId] * num
        p.sellBusinessItemToNpc(self.entityId, saleIds, positions, False)

    def createSpyChat(self, saleId, saleInfoType, businessNpcNo):
        if saleInfoType in (gametypes.BUSINESS_SPY_EXCESS, gametypes.BUSINESS_SPY_LACK):
            chat = SBD.data.get(saleId, {}).get('spyChat', {}).get(saleInfoType, '')
        elif saleInfoType in (gametypes.BUSINESS_SPY_RESERVE_EXCESS, gametypes.BUSINESS_SPY_RESERVE_LACK):
            chat = SBD.data.get(saleId, {}).get('spyChat', {}).get(saleInfoType, '%s') % NBD.data.get(businessNpcNo, {}).get('locationDesc', '')
        else:
            chat = uiUtils.getTextFromGMD(GMDD.data.GUILD_BUSINESS_SPY_DEFAULT)
        return chat
