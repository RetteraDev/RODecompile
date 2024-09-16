#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impCoinConsign.o
import cPickle
import zlib
import gametypes
import gameglobal

class ImpCoinConsign(object):

    def onCoinConsignInit(self, consignData):
        self.coinConsignData = consignData
        gameglobal.rds.ui.consign.mineCoinTabInfo.refreshCurrentPage()
        gameglobal.rds.ui.tabAuctionConsign.mineCoinTabInfo.refreshCurrentPage()

    def onCoinConsignUpdateMine(self, dbID, data):
        if not self.coinConsignData.has_key(dbID):
            self.coinConsignData[dbID] = data
        else:
            item = self.coinConsignData.get(dbID)
            if not item:
                return
            itemCnt, price, tModify = data
            if itemCnt == 0:
                self.coinConsignData.pop(dbID, None)
            else:
                item.setWrap(itemCnt)
                item._consignPrice = price
                item._consignModifyT = tModify
        gameglobal.rds.ui.consign.onSellItemSuccess()
        gameglobal.rds.ui.consign.mineCoinTabInfo.refreshCurrentPage()
        gameglobal.rds.ui.tabAuctionConsign.onSellItemSuccess()
        gameglobal.rds.ui.tabAuctionConsign.mineCoinTabInfo.refreshCurrentPage()

    def onCoinConsignUpdateOthers(self, dbID, data):
        itemCnt, price, tModify = data
        if not itemCnt:
            gameglobal.rds.ui.consign.buyCoinTabInfo.refreshCurrentPage(clearFollowingCache=True)
            gameglobal.rds.ui.tabAuctionConsign.buyCoinTabInfo.refreshCurrentPage(clearFollowingCache=True)
        else:
            consignments = []
            if gameglobal.rds.configData.get('enableTabAuction', False):
                consignments = gameglobal.rds.ui.tabAuctionConsign.otherConsignments
            else:
                consignments = gameglobal.rds.ui.consign.otherConsignments
            for consignment in consignments:
                consignment.onUpdateOthers(dbID, data)

    def onCoinConsignShowOthers(self, data):
        consignment = None
        if gameglobal.rds.configData.get('enableTabAuction', False):
            consignment = gameglobal.rds.ui.tabAuctionConsign.getConsignment(data[0])
        else:
            consignment = gameglobal.rds.ui.consign.getConsignment(data[0])
        if consignment:
            consignment.onShowOthers(data)

    def onQueryCoinConsignItemPrice(self, itemId, price, queryFor):
        if queryFor == gametypes.CONSIGN_QUERY_PRICE_FOR_CONSIGN_SELL:
            gameglobal.rds.ui.consign.onUpdatePrice(itemId, price)
        if queryFor == gametypes.CONSIGN_QUERY_PRICE_FOR_CONSIGN_SELL:
            gameglobal.rds.ui.tabAuctionConsign.onUpdatePrice(itemId, price)
        gameglobal.rds.ui.coinPrices.prices[itemId] = price

    def onQueryCoinConsignTradeHistory(self, data):
        try:
            self.consignTradeHistory = cPickle.loads(zlib.decompress(data))
        except:
            self.consignTradeHistory = []

        gameglobal.rds.ui.consign.historyTabInfo.refreshCurrentPage()
        gameglobal.rds.ui.tabAuctionConsign.historyTabInfo.refreshCurrentPage()
