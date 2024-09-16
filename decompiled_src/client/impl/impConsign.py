#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impConsign.o
import BigWorld
import gametypes
import gameglobal
import gamelog
import npcConst
from guis import uiConst
from data import npc_data as ND

class ImpConsign(object):

    def onConsignInit(self, consignation):
        gamelog.debug('@zq onConsignInit', consignation)
        self.consignation = consignation
        self.consignPrices = {}
        gameglobal.rds.ui.consign.mineTabInfo.refreshCurrentPage()
        gameglobal.rds.ui.tabAuctionConsign.mineTabInfo.refreshCurrentPage()
        self.consignBidItems = {}

    def onOpenConsign(self, id):
        gamelog.debug('@zq onOpenConsign', id)
        if not BigWorld.entities.get(id):
            return
        else:
            npcId = BigWorld.entities.get(id).npcId
            npcData = ND.data.get(npcId, None)
            if npcData == None:
                return
            openType = npcData.get('full', 0)
            if openType:
                gameglobal.rds.ui.funcNpc.openDirectly(self.id, npcId, npcConst.NPC_FUNC_CONSIGN)
                gameglobal.rds.ui.inventory.show(True, uiConst.LAYOUT_NPC_FUNC)
            else:
                gameglobal.rds.ui.inventory.show(False)
            self.openAuctionFun(id, uiConst.LAYOUT_NPC_FUNC)
            return

    def onConsignShowOthers(self, data):
        gamelog.debug('@zq onConsignShowOthers', data)
        consignment = None
        if gameglobal.rds.configData.get('enableTabAuction', False):
            consignment = gameglobal.rds.ui.tabAuctionConsign.getConsignment(data[0])
        else:
            consignment = gameglobal.rds.ui.consign.getConsignment(data[0])
        if consignment:
            consignment.onShowOthers(data)

    def onQueryConsignItemPrice(self, itemId, price, queryFor):
        gamelog.debug('@zq onQueryConsignItemPrice', itemId, price, queryFor)
        if queryFor == gametypes.CONSIGN_QUERY_PRICE_FOR_CONSIGN_SELL:
            gameglobal.rds.ui.consign.onUpdatePrice(itemId, price)
        gameglobal.rds.ui.consign.prices[itemId] = price
        if queryFor == gametypes.CONSIGN_QUERY_PRICE_FOR_CONSIGN_SELL:
            gameglobal.rds.ui.tabAuctionConsign.onUpdatePrice(itemId, price)
        gameglobal.rds.ui.tabAuctionConsign.prices[itemId] = price

    def onConsignUpdateOthers(self, dbID, data):
        gamelog.debug('@zq onConsignUpdateOthers', dbID, data)
        consignUI = None
        if gameglobal.rds.configData.get('enableTabAuction', False):
            consignUI = gameglobal.rds.ui.tabAuctionConsign
        else:
            consignUI = gameglobal.rds.ui.consign
        if not data:
            consignUI.buyTabInfo.refreshCurrentPage(clearFollowingCache=True)
        else:
            consignments = consignUI.otherConsignments
            for consignment in consignments:
                consignment.onUpdateOthers(dbID, data)

    def onConsignUpdateMine(self, dbID, op, data):
        gamelog.debug('@zq onConsignUpdateMine', dbID, op, data)
        if op == gametypes.CONSIGN_OP_PLACE:
            self.consignation[dbID] = data
            gameglobal.rds.ui.consign.onSellItemSuccess()
            gameglobal.rds.ui.tabAuctionConsign.onSellItemSuccess()
            self.consignPrices[data.id] = {'price': data._consignPrice * 1.0 / data.cwrap,
             'fixedPrice': data._consignFixedPrice * 1.0 / data.cwrap}
        elif op == gametypes.CONSIGN_OP_BID:
            item = self.consignation.get(dbID)
            if item:
                bidPrice, bidderRole, bidderGBID, tModify = data
                item._consignPrice = bidPrice
                item._consignBidderRole = bidderRole
                item._consignBidderGBID = bidderGBID
                item._consignModifyT = tModify
                item._consignBid = True
        elif op == gametypes.CONSIGN_OP_SOLD_PARTIAL:
            item = self.consignation.get(dbID)
            if item:
                itemCount, fixedPrice, bidPrice, tModify = data
                item.setWrap(itemCount)
                item._consignPrice = bidPrice
                item._consignFixedPrice = fixedPrice
                item._consignModifyT = tModify
        elif op == gametypes.CONSIGN_OP_DEL:
            self.consignation.pop(dbID, None)
        elif op == gametypes.CONSIGN_OP_FREEZE:
            item = self.consignation.get(dbID)
            if item:
                tEnd, tModify = data
                item._consignModifyT = tModify
                item._consignEndT = tEnd
                item._consignBid = False
        gameglobal.rds.ui.consign.mineTabInfo.refreshCurrentPage()
        gameglobal.rds.ui.tabAuctionConsign.mineTabInfo.refreshCurrentPage()

    def onConsignDeleteMine(self, dbIDs):
        gamelog.debug('@zq onConsignDeleteMine', dbIDs)
        if not hasattr(self, 'consignation'):
            return
        else:
            for dbID in dbIDs:
                self.consignation.pop(dbID, None)

            gameglobal.rds.ui.consign.mineTabInfo.refreshCurrentPage()
            gameglobal.rds.ui.tabAuctionConsign.mineTabInfo.refreshCurrentPage()
            return

    def onAddConsignBidItem(self, dbID, it):
        gamelog.debug('@zq onAddConsignBidItem', dbID, it)
        self.consignBidItems[dbID] = it
        gameglobal.rds.ui.consign.myBidTabInfo.refreshCurrentPage()
        gameglobal.rds.ui.tabAuctionConsign.myBidTabInfo.refreshCurrentPage()

    def onInitMyConsignBidItems(self, data):
        gamelog.debug('@zq onInitMyConsignBidItems', data)
        self.consignBidItems = {}
        for dbID, it in data.iteritems():
            self.consignBidItems[dbID] = it

        gameglobal.rds.ui.consign.myBidTabInfo.refreshCurrentPage()
        gameglobal.rds.ui.tabAuctionConsign.myBidTabInfo.refreshCurrentPage()

    def onUpdateMyConsignBidItems(self, data):
        gamelog.debug('@zq onUpdateMyConsignBidItems', data)
        for dbID, (bidPrice, bidderRole, bidderGBID, tModify) in data.iteritems():
            it = self.consignBidItems.get(dbID)
            if it:
                it.updateProp({'_consignPrice': bidPrice,
                 '_consignModifyT': tModify,
                 '_consignBidderRole': bidderRole,
                 '_consignBidderGBID': bidderGBID})

        gameglobal.rds.ui.consign.myBidTabInfo.refreshCurrentPage()
        gameglobal.rds.ui.tabAuctionConsign.myBidTabInfo.refreshCurrentPage()

    def onConsignBidItemBuyByOther(self, dbID):
        gamelog.debug('@zq onConsignBidItemBuyByOther', dbID)
        self.consignBidItems.pop(dbID, None)
        gameglobal.rds.ui.consign.myBidTabInfo.refreshCurrentPage()
        gameglobal.rds.ui.tabAuctionConsign.myBidTabInfo.refreshCurrentPage()
