#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impNpcShop.o
import BigWorld
import gameglobal
import gamelog
import npcConst
from guis import ui
from guis import uiConst
from data import npc_data as ND

class ImpNpcShop(object):

    def shopItemsUpdate(self, npcId, page, stamp, info, forceUpdate):
        gamelog.debug('jorsef: shopGoodsUpdate', npcId, page, stamp, info)
        gameglobal.rds.ui.shop.setPageItem(page, stamp, info, forceUpdate)

    def shopSingleItemUpdate(self, npcId, page, pos, item):
        gamelog.debug('jorsef: shopSingleItemUpdate', npcId, page, pos, item)
        if gameglobal.rds.ui.shop.show:
            gameglobal.rds.ui.shop.setSingleItem(page, pos, item)

    def shopItemsKeep(self, npcId, page, stamp):
        gamelog.debug('jorsef: shopGoodsKeep', npcId, page, stamp)
        gameglobal.rds.ui.shop.setPageItem(page, stamp)

    @ui.callFilter(1)
    def npcShopOpen(self, npcId, shopId, pageCount, discount):
        gamelog.debug('jorsef: npcShopOpen', npcId, pageCount, discount)
        npcData = ND.data.get(npcId, None)
        if npcData == None:
            return
        else:
            if gameglobal.rds.ui.compositeShop.isOpen:
                gameglobal.rds.ui.compositeShop.closeShop()
            openType = npcData.get('full', 0)
            gamelog.debug('@hjx npc#npcShopOpen', openType)
            if openType:
                gameglobal.rds.ui.funcNpc.openDirectly(self.id, npcId, npcConst.NPC_FUNC_SHOP)
                if BigWorld.player()._isInCross():
                    if gameglobal.rds.configData.get('enableWingWorld', False):
                        gameglobal.rds.ui.crossServerBag.show()
                else:
                    gameglobal.rds.ui.inventory.show(True, uiConst.LAYOUT_NPC_FUNC)
            elif BigWorld.player()._isInCross():
                if gameglobal.rds.configData.get('enableWingWorld', False):
                    gameglobal.rds.ui.crossServerBag.show()
            else:
                gameglobal.rds.ui.inventory.show(True)
            newShop = gameglobal.rds.ui.shop.showShop(self.id, shopId, pageCount, discount, uiConst.LAYOUT_NPC_FUNC)
            gamelog.debug('jorsef: npcShopOpen1', newShop)
            if newShop:
                self.cell.turnPage(shopId, 0, 0)
            elif gameglobal.rds.ui.shop.option == gameglobal.rds.ui.shop.OPTION_SHOP:
                page = gameglobal.rds.ui.shop.currPage
                stamp = gameglobal.rds.ui.shop.pageStamp.get(page, 0)
                self.cell.turnPage(shopId, page, stamp)
            return
