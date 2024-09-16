#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impDynamicShop.o
import gamelog
import gameglobal
import const
import utils
import gametypes
from callbackHelper import Functor
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD
from cdata import dynamic_shop_item_data as DSID

class ImpDynamicShop(object):

    def onQueryDynamicShopItemInfo(self, shopNo, info):
        gamelog.debug('@zqx|dynamicShop onQueryDynamicShopItemInfo ', shopNo, info)
        gameglobal.rds.ui.selfAdaptionShop.setShopInfo(shopNo, info)

    def onDynamicShopBuyPriceWarn(self, shopNo, setId, count):
        """
        \xe6\x89\xb9\xe9\x87\x8f\xe8\xb4\xad\xe4\xb9\xb0\xe7\x89\xa9\xe5\x93\x81\xe6\x97\xb6\xe4\xbb\xb7\xe6\xa0\xbc\xe4\xba\xa7\xe5\x87\xba5%\xef\xbc\x8c\xe4\xba\x8c\xe6\xac\xa1\xe7\xa1\xae\xe8\xae\xa4
        :param shopNo:
        :param setId:
        :param count:
        :return:
        """
        gamelog.debug('@zqx|dynamicShop onDynamicShopBuyPriceWarn ', shopNo, setId, count)
        msg = GMD.data.get(GMDD.data.DYNAMIC_SHOP_BUY_CONFIRM, {}).get('text', '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.cell.dynamicShopBuy, shopNo, setId, count, True))

    def onDynamicShopSellPriceWarn(self, shopNo, setId, count):
        """
        \xe6\x89\xb9\xe9\x87\x8f\xe5\x9b\x9e\xe6\x94\xb6\xe7\x89\xa9\xe5\x93\x81\xe6\x97\xb6\xe4\xbb\xb7\xe6\xa0\xbc\xe5\xb7\xae\xe8\xb6\x85\xe5\x87\xba5%,\xe4\xba\x8c\xe6\xac\xa1\xe7\xa1\xae\xe8\xae\xa4
        :param shopNo:
        :param setId:
        :param count:
        :return:
        """
        gamelog.debug('@zqx|dynamicShop onDynamicShopSellPriceWarn ', shopNo, setId, count)
        msg = GMD.data.get(GMDD.data.DYNAMIC_SHOP_SELL_CONFIRM, {}).get('text', '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.cell.dynamicShopSell, shopNo, setId, count, True))

    def onUpdateDynamicShopItemInfo(self, shopNo, info):
        gamelog.debug('@zqx|dynamicShop onUpdateDynamicShopItemInfo ', shopNo, info)
        gameglobal.rds.ui.selfAdaptionShop.updateShopInfo(shopNo, info)

    def getDynamicShopItemRemainCount(self, setId, isBuy = True):
        count, limitCount = self.getDynamicShopItemCount(setId, isBuy)
        if limitCount > 0:
            return limitCount - count
        return 999

    def getDynamicShopItemCount(self, setId, isBuy = True):
        dataKey = self.getDynamicShopItemLimitKey(setId, isBuy)
        count = 0
        lastTime = 0
        limitType = DSID.data.get(setId, {}).get('buyLimitType' if isBuy else 'sellLimitType', 0)
        if dataKey in self.dynamicShopTradeLimit:
            count, lastTime = self.dynamicShopTradeLimit[dataKey]
        limitCount = DSID.data.get(setId, {}).get('buyLimitCount' if isBuy else 'sellLimitCount', -1)
        if lastTime:
            samePeriod = False
            now = utils.getNow()
            if limitType == gametypes.DYNAMIC_SHOP_BUY_LIMIT_TYPE_DAY:
                samePeriod = utils.isSameDay(lastTime, now)
            elif limitType == gametypes.DYNAMIC_SHOP_BUY_LIMIT_TYPE_WEEK:
                samePeriod = utils.isSameWeek(lastTime, now)
            elif limitType == gametypes.DYNAMIC_SHOP_BUY_LIMIT_TYPE_MONTH:
                samePeriod = utils.isSameMonth(lastTime, now)
            elif limitType == gametypes.DYNAMIC_SHOP_BUY_LIMIT_TYPE_FOREVER:
                samePeriod = True
            if not samePeriod:
                count = 0
        return (count, limitCount)

    def getDynamicShopItemLimitKey(self, setId, isBuy):
        itemData = DSID.data.get(setId, {})
        if 'buyLimitGroup' in itemData:
            if isBuy:
                return 'g_buy_%d' % itemData['buyLimitGroup']
            return 'g_sell_%d' % itemData['buyLimitGroup']
        elif isBuy:
            return 'i_buy_%d' % setId
        else:
            return 'i_sell_%d' % setId
