#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impPrivateShop.o
from gamestrings import gameStrings
import BigWorld
import const
import gameglobal
import gametypes
import gamelog
from container import Container
from guis import uiConst
from data import sys_config_data as SCD
from data import private_shop_data as PSD
from data import composite_shop_data as CSD
from cdata import game_msg_def_data as GMDD

class ImpPrivateShop(object):

    def _getCurrPrivateShopId(self):
        shopId = SCD.data.get('PRIVATE_SHOP_ID', 0)
        return shopId

    def getCurrPrivateShop(self):
        shopId = self._getCurrPrivateShopId()
        type = PSD.data.get(shopId, {}).get('type', 0)
        if type == gametypes.PRIVATE_SHOP_TYPE_ACTIVITY:
            if gameglobal.rds.ui.activityShop.canOpen():
                BigWorld.player().base.openPrivateShop(0, shopId)
            else:
                BigWorld.player().showGameMsg(GMDD.data.ACTIVITY_SHOP_CLOSED, ())

    def getPrivateCompositeShop(self):
        shopId = SCD.data.get('privateCompositeShopId', 0)
        if not shopId:
            return
        type = PSD.data.get(shopId, {}).get('type', 0)
        if type == gametypes.PRIVATE_SHOP_TYPE_COMPOSITE:
            if self._isSoul():
                self.showGameMsg(GMDD.data.PRIVATE_YUNCHUI_SHOP_FORBIDDEN, gameStrings.TEXT_IMPPRIVATESHOP_41)
                return
            self.base.openPrivateShop(0, shopId)

    def getPrivateShop(self, shopId, createIfNotExist = False, pageCount = const.SHOP_PAGE_NUM):
        data = CSD.data.get(shopId, {})
        if not data:
            return
        else:
            compositeShopType = data.get('compositeShopType', -1)
            if compositeShopType in [const.SHOP_TYPE_PRIVATE_EXTEND, const.SHOP_COMPOSITE_TYPE_NO_SELL_AND_NO_RETRIEVE]:
                width = const.COMPOSITE_SHOP_GROUP_UP_TYPE_WIDTH
                height = const.COMPOSITE_SHOP_GROUP_UP_TYPE_HEIGHT
            else:
                width = const.COMPOSITE_SHOP_WIDTH
                height = const.COMPOSITE_SHOP_HEIGHT
            shop = self.privateShop.get(shopId)
            if shop == None and createIfNotExist:
                shop = Container(pageCount=pageCount, width=width, height=height)
                shop.stamp = [ 1 for x in xrange(shop.pageCount) ]
                shop.tRefreshFree = 0
                shop.refreshCnt = 0
                shop.buyCount = {}
                self.privateShop[shopId] = shop
            return shop

    def onOpenPrivateShop(self, npcId, compositeShopId, pageCount, customDict):
        shopInv = self.getPrivateShop(compositeShopId, True)
        if not shopInv:
            return None
        else:
            type = PSD.data.get(compositeShopId, {}).get('type', 0)
            showType = PSD.data.get(compositeShopId, {}).get('showType', uiConst.PRIVATE_SHOP_SHOW_TYPE_YUNCHUI)
            if type == gametypes.PRIVATE_SHOP_TYPE_ACTIVITY:
                gameglobal.rds.ui.activityShop.refreshPrivateShop(compositeShopId, shopInv, True)
            elif type == gametypes.PRIVATE_SHOP_TYPE_COMPOSITE:
                if self.isInBfDota():
                    if gameglobal.rds.ui.bfDotaShop.needOpen(compositeShopId):
                        gameglobal.rds.ui.bfDotaShop.show(compositeShopId, shopInv, customDict, pageCount)
                elif showType == uiConst.PRIVATE_SHOP_SHOW_TYPE_YUNCHUI:
                    gameglobal.rds.ui.yunChuiShop.openPrivateShop(compositeShopId, shopInv, customDict, pageCount)
                else:
                    gameglobal.rds.ui.compositeShop.openShop(npcId, compositeShopId, pageCount, customDict)
            return None

    def _delayedOpenPrivateShop(self, npcId, compositeShopId, pageCount, customDict):
        e = BigWorld.entities.get(npcId)
        if not e:
            return
        shopInv = self.getPrivateShop(compositeShopId)
        gameglobal.rds.ui.activityShop.refreshPrivateShop(compositeShopId, shopInv, True)

    def onOpenPrivateShopPage(self, shopId, page):
        self._refreshPrivateShopPage(shopId, page)

    def privateShopItemsUpdate(self, shopId, data):
        info, tRefreshFree, refreshCnt, buyCount = data
        self.privateShop.pop(shopId, None)
        shopInv = self.getPrivateShop(shopId, createIfNotExist=True, pageCount=len(info))
        if not shopInv:
            return
        else:
            shopInv.tRefreshFree = tRefreshFree
            shopInv.refreshCnt = refreshCnt
            shopInv.buyCount = buyCount
            shopInv.stamp = [0] * len(info)
            for page, (stamp, pgInfo) in enumerate(info):
                shopInv.stamp[page] = stamp
                for pos, it in enumerate(pgInfo):
                    shopInv.setQuickVal(it, page, pos)

            type = PSD.data.get(shopId, {}).get('type', 0)
            showType = PSD.data.get(shopId, {}).get('showType', uiConst.PRIVATE_SHOP_SHOW_TYPE_COMPOSITE)
            if type == gametypes.PRIVATE_SHOP_TYPE_ACTIVITY:
                self._refreshPrivateShopPage(shopId, 1)
            elif type == gametypes.PRIVATE_SHOP_TYPE_COMPOSITE and self.openShopId == shopId:
                if self.isInBfDota():
                    if gameglobal.rds.ui.bfDotaShop.needOpen(shopId):
                        gameglobal.rds.ui.bfDotaShop.show(shopId, shopInv)
                elif showType == uiConst.PRIVATE_SHOP_SHOW_TYPE_YUNCHUI:
                    gameglobal.rds.ui.yunChuiShop.refreshTabItems()
                else:
                    gameglobal.rds.ui.compositeShop.refreshPageItem(shopInv)
            return

    def _refreshPrivateShopPage(self, shopId, page):
        shopInv = self.getPrivateShop(shopId)
        gameglobal.rds.ui.activityShop.refreshPrivateShop(shopId, shopInv)

    def privateShopSingleItemUpdate(self, shopId, page, pos, item, buyCount):
        shopInv = self.getPrivateShop(shopId)
        shopInv.setQuickVal(item, page, pos)
        if not shopInv:
            return
        shopInv.buyCount[item.compositeId] = buyCount
        type = PSD.data.get(shopId, {}).get('type', 0)
        showType = PSD.data.get(shopId, {}).get('showType', uiConst.PRIVATE_SHOP_SHOW_TYPE_YUNCHUI)
        if type == gametypes.PRIVATE_SHOP_TYPE_ACTIVITY:
            self._refreshPrivateShopPage(shopId, 1)
        elif type == gametypes.PRIVATE_SHOP_TYPE_COMPOSITE and self.openShopId == shopId:
            if showType == uiConst.PRIVATE_SHOP_SHOW_TYPE_YUNCHUI:
                gameglobal.rds.ui.yunChuiShop.refreshSingleItem(page, pos, item)
            else:
                gameglobal.rds.ui.compositeShop.setSingleItem(page, pos, item)

    def _resetPrivateShopDaily(self):
        for shopInv in self.privateShop.itervalues():
            shopInv.refreshCnt = 0

        gameglobal.rds.ui.activityShop.refreshCurrPrivateShop()

    def compositeShopTurnPage(self, shopId, page, stamp):
        shopInv = self.getPrivateShop(shopId)
        if not shopInv:
            gamelog.error('@jbx: shopInv is None', shopId, page, stamp)
            return
        if page >= len(shopInv.pages):
            return
        items = shopInv.pages[page]
        st = shopInv.stamp[page]
        gameglobal.rds.ui.compositeShop.setNormalPageItem(shopId, page, st, items)

    def onDeletePrivateShop(self, shopIds):
        gamelog.info('@jbx:onDeletePrivateShop', shopIds)
        for shopId in shopIds:
            self.privateShop.pop(shopId, None)
            if self.openShopId == shopId:
                type = PSD.data.get(shopId, {}).get('type', 0)
                showType = PSD.data.get(shopId, {}).get('showType', uiConst.PRIVATE_SHOP_SHOW_TYPE_YUNCHUI)
                if type == gametypes.PRIVATE_SHOP_TYPE_ACTIVITY and gameglobal.rds.ui.activityShop.widget:
                    gameglobal.rds.ui.activityShop.hide()
                elif type == gametypes.PRIVATE_SHOP_TYPE_COMPOSITE:
                    yunChuiShopProxy = gameglobal.rds.ui.yunChuiShop
                    if showType == uiConst.PRIVATE_SHOP_SHOW_TYPE_YUNCHUI and yunChuiShopProxy.mediator:
                        gameglobal.rds.ui.yunChuiShop.hide()
                    elif gameglobal.rds.ui.compositeShop.mediator:
                        gameglobal.rds.ui.compositeShop.hide()
