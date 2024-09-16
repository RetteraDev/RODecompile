#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impCoinMarket.o
import cPickle
import zlib
import const
import gameglobal

class ImpCoinMarket(object):

    def onQueryCoinMarket(self, version, data, tSell, tBuy, history):
        try:
            data = cPickle.loads(zlib.decompress(data))
            history = cPickle.loads(zlib.decompress(history))
        except:
            data = []
            history = []

        gameglobal.rds.ui.tianyuMall.onQueryMarketInfoDone(version, data, tSell, tBuy, history)

    def onSellCoinInMarketOk(self, opNUID, coin, price, expireTime, restCoin):
        gameglobal.rds.ui.tianyuMall.onBuySellCoinInMarketOk(const.COIN_MARKET_OP_SELL_COIN, opNUID, coin, price, expireTime, restCoin)

    def onBuyCoinInMarketOk(self, opNUID, coin, price, expireTime, restCoin):
        gameglobal.rds.ui.tianyuMall.onBuySellCoinInMarketOk(const.COIN_MARKET_OP_BUY_COIN, opNUID, coin, price, expireTime, restCoin)

    def onCancelCoinMarketTradeOk(self, opNUID):
        gameglobal.rds.ui.tianyuMall.onDeleteOrderOk(opNUID)

    def onQueryCoinMarketTradeHistory(self, data):
        try:
            data = cPickle.loads(zlib.decompress(data))
        except:
            data = []

        gameglobal.rds.ui.tianyuMall.onQueryMyHistoryInfoDone(data)

    def onQueryCurrentCoinMarketTrade(self, data):
        try:
            data = cPickle.loads(zlib.decompress(data))
        except:
            data = []

        gameglobal.rds.ui.tianyuMall.onQueryMyMarketInfoDone(data)
