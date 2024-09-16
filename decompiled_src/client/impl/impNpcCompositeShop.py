#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impNpcCompositeShop.o
import BigWorld
import gameglobal
import gamelog
import npcConst
from callbackHelper import Functor
from guis import uiConst
from guis import ui
from guis import uiUtils
from data import npc_data as ND

class ImpNpcCompositeShop(object):

    @ui.callFilter(1)
    def npcCompositeShopOpen(self, npcId, compositeShopId, pageCount, buybackShopPageCount, customDict):
        gamelog.debug('@zs npcCompositeShopOpen', npcId, compositeShopId, pageCount, customDict)
        npcData = ND.data.get(npcId, None)
        if npcData == None:
            return
        else:
            openType = npcData.get('full', 0)
            if openType:
                gameglobal.rds.ui.funcNpc.openDirectly(self.id, npcId, npcConst.NPC_FUNC_COMPOSITE_SHOP)
            if gameglobal.rds.ui.shop.show:
                gameglobal.rds.ui.shop.hide()
            if BigWorld.player()._isInCross():
                if gameglobal.rds.configData.get('enableWingWorld', False):
                    gameglobal.rds.ui.crossServerBag.show()
            else:
                gameglobal.rds.ui.inventory.show(layoutType=uiConst.LAYOUT_NPC_FUNC)
            compositeShop = gameglobal.rds.ui.compositeShop
            yunChuiShop = gameglobal.rds.ui.yunChuiShop
            if compositeShop.isOpen or yunChuiShop.mediator:
                uiUtils.closeCompositeShop()
                BigWorld.callback(0.5, Functor(self._delayedOpenShop, compositeShopId, pageCount, customDict))
            else:
                compositeShop.openShop(self.id, compositeShopId, pageCount, customDict, buybackShopPageCount, layoutType=uiConst.LAYOUT_NPC_FUNC)
                self.cell.compositeShopTurnPage(compositeShopId, 0, 0)
            return

    def _delayedOpenShop(self, compositeShopId, pageCount, customDict):
        gameglobal.rds.ui.compositeShop.openShop(self.id, compositeShopId, pageCount, customDict)
        self.cell.compositeShopTurnPage(compositeShopId, 0, 0)

    def compositeShopItemsUpdate(self, npcId, idx, compositeShopId, page, stamp, info, forceUpdate):
        yunChuiShopProxy = gameglobal.rds.ui.yunChuiShop
        if gameglobal.rds.ui.compositeShop.isOpen or yunChuiShopProxy.mediator:
            gameglobal.rds.ui.compositeShop.setNormalPageItem(compositeShopId, page, stamp, info, forceUpdate)

    def compositeShopSingleItemUpdate(self, npcId, idx, page, pos, item):
        gamelog.debug('@zs: compositeShopSingleItemUpdate', npcId, page, pos, item)
        yunChuiShopProxy = gameglobal.rds.ui.yunChuiShop
        if gameglobal.rds.ui.compositeShop.isOpen or yunChuiShopProxy.mediator:
            gameglobal.rds.ui.compositeShop.setSingleItem(page, pos, item)

    def compositeShopItemsKeep(self, npcId, idx, shopId, page, stamp):
        gamelog.debug('@zs: shopGoodsKeep', npcId, shopId, page, stamp)
        yunChuiShopProxy = gameglobal.rds.ui.yunChuiShop
        if gameglobal.rds.ui.compositeShop.isOpen or yunChuiShopProxy.mediator:
            gameglobal.rds.ui.compositeShop.setNormalPageItem(shopId, page, stamp)

    def purchaseShopItemsUpdate(self, npcId, idx, page, stamp, info, forceUpdate):
        if gameglobal.rds.ui.purchaseShop.mediator:
            gameglobal.rds.ui.purchaseShop.setPurchaseItem(page, stamp, info, forceUpdate)

    def purchaseShopSingleItemUpdate(self, npcId, idx, page, pos, item):
        if gameglobal.rds.ui.purchaseShop.mediator:
            gameglobal.rds.ui.purchaseShop.setSingleItem(page, pos, item)
            gameglobal.rds.ui.purchaseShop.refreshFameData()

    def purchaseShopItemsKeep(self, npcId, idx, page, stamp):
        if gameglobal.rds.ui.purchaseShop.mediator:
            gameglobal.rds.ui.purchaseShop.setPurchaseItem(page, stamp)
