#Embedded file name: /WORKSPACE/data/entities/common/dynamicshop.o
from userSoleType import UserSoleType
from userDictType import UserDictType
import copy
import const
import gametypes
import sMath
import gamelog
import time
from gamescript import FormularEvalEnv
from data import sys_config_data as SCD
from cdata import dynamic_shop_item_data as DSID

def getSellPrice(changePriceCount, minPrice, maxPrice, nowPrice, itemTradedChangePriceCount, itemTradedChangePriceType, itemTradedChangePriceValue, count):
    """
    \xc4\xa3\xc4\xe2\xc9\xcc\xb5\xea\xc5\xfa\xc1\xbf\xc2\xf4\xb3\xf6,\xcd\xe6\xbc\xd2\xd0\xe8\xd2\xaa\xd6\xa7\xb8\xb6\xb5\xc4\xbb\xf5\xb1\xd2\xca\xfd
    :param changePriceCount: \xb5\xb1\xc7\xb0\xbd\xbb\xd2\xd7\xca\xfd
    :param minPrice:
    :param maxPrice:
    :param nowPrice:
    :param itemTradedChangePriceCount: \xb5\xc0\xbe\xdf\xbc\xc6\xca\xfd\xd3\xb0\xcf\xec\xbc\xdb\xb8\xf1\xb9\xab\xca\xbd\xcb\xe3\xb3\xf6\xb5\xc4\xb8\xf6\xca\xfd(\xbc\xb4\xc3\xbf\xbd\xbb\xd2\xd7\xbc\xb8\xb8\xf6\xa3\xac\xb8\xc4\xb1\xe4\xd2\xbb\xb4\xce\xbc\xdb\xb8\xf1)
    :param itemTradedChangePriceType: \xb5\xc0\xbe\xdf\xbc\xc6\xca\xfd\xbc\xdb\xb8\xf1\xb1\xe4\xbb\xaf\xb7\xbd\xca\xbd
    :param itemTradedChangePriceValue: \xb5\xc0\xbe\xdf\xbc\xc6\xca\xfd\xbc\xdb\xb8\xf1\xb1\xe4\xbb\xaf\xb7\xf9\xb6\xc8
    :param count:
    :return:
    """
    money = 0
    for i in xrange(count):
        changePriceCount += 1
        money += nowPrice
        if changePriceCount < itemTradedChangePriceCount:
            continue
        changePriceCount = 0
        if itemTradedChangePriceType == gametypes.DYNAMIC_SHOP_ITEM_TRADED_REFRESH_PRICE_TYPE_VALUE:
            nowPrice = sMath.clamp(nowPrice + int(itemTradedChangePriceValue), minPrice, maxPrice)
        elif itemTradedChangePriceType == gametypes.DYNAMIC_SHOP_ITEM_TRADED_REFRESH_PRICE_TYPE_PERCENT:
            nowPrice = sMath.clamp(int(nowPrice * (1 + itemTradedChangePriceValue)), minPrice, maxPrice)

    return money


def getBuyPrice(dynamicShopType, changePriceCount, minPrice, maxPrice, nowPrice, itemTradedChangePriceCount, itemTradedChangePriceType, itemTradedChangePriceValue, count):
    totalMoney = 0
    for i in xrange(count):
        changePriceCount -= 1
        if dynamicShopType == gametypes.DYNAMIC_SHOP_TYPE_BUY_AND_SELL:
            totalMoney += max(1, int(nowPrice * SCD.data.get('dynamicShopSellPricePercent', 0.85)))
        else:
            totalMoney += nowPrice
        if abs(changePriceCount) < itemTradedChangePriceCount:
            continue
        changePriceCount = 0
        if itemTradedChangePriceType == gametypes.DYNAMIC_SHOP_ITEM_TRADED_REFRESH_PRICE_TYPE_VALUE:
            nowPrice = sMath.clamp(nowPrice + int(itemTradedChangePriceValue), minPrice, maxPrice)
        elif itemTradedChangePriceType == gametypes.DYNAMIC_SHOP_ITEM_TRADED_REFRESH_PRICE_TYPE_PERCENT:
            nowPrice = sMath.clamp(int(nowPrice * (1 + itemTradedChangePriceValue)), minPrice, maxPrice)

    return totalMoney


def checkSellPriceGap(money, changePriceCount, minPrice, maxPrice, sourcePrice, nowPrice, itemTradedChangePriceCount, itemTradedChangePriceType, itemTradedChangePriceValue, count, sellForce):
    """
    \xc4\xa3\xc4\xe2\xc9\xcc\xb5\xea\xc5\xfa\xc1\xbf\xc2\xf4\xb3\xf6\xbc\xdb\xb8\xf1\xca\xc7\xb7\xf1\xd3\xd0\xb3\xac5%\xa3\xac\xbb\xf5\xb1\xd2\xca\xc7\xb7\xf1\xb3\xe4\xd7\xe3
    :param money: \xcd\xe6\xbc\xd2\xc9\xed\xc9\xcf\xd3\xb5\xd3\xd0\xb5\xc4\xd3\xc3\xd3\xda\xb9\xba\xc2\xf2\xb8\xc3\xce\xef\xc6\xb7\xb5\xc4\xbb\xf5\xb1\xd2\xca\xfd
    :param changePriceCount: \xb5\xb1\xc7\xb0\xbd\xbb\xd2\xd7\xca\xfd
    :param minPrice: \xb5\xb1\xcc\xec\xbc\xdb\xb8\xf1\xcf\xc2\xcf\xde
    :param maxPrice: \xb5\xb1\xcc\xec\xbc\xdb\xb8\xf1\xc9\xcf\xcf\xde
    :param sourcePrice: \xc9\xcc\xb5\xea\xc5\xfa\xc1\xbf\xc2\xf4\xb3\xf6\xc7\xb0\xce\xef\xc6\xb7\xbc\xdb\xb8\xf1
    :param nowPrice: \xc9\xcc\xb5\xea\xce\xef\xc6\xb7\xb5\xb1\xc7\xb0\xbc\xdb\xb8\xf1
    :param itemTradedChangePriceCount: \xb5\xc0\xbe\xdf\xbc\xc6\xca\xfd\xd3\xb0\xcf\xec\xbc\xdb\xb8\xf1\xb9\xab\xca\xbd\xcb\xe3\xb3\xf6\xb5\xc4\xb8\xf6\xca\xfd(\xbc\xb4\xc3\xbf\xbd\xbb\xd2\xd7\xbc\xb8\xb8\xf6\xa3\xac\xb8\xc4\xb1\xe4\xd2\xbb\xb4\xce\xbc\xdb\xb8\xf1)
    :param itemTradedChangePriceType: \xb5\xc0\xbe\xdf\xbc\xc6\xca\xfd\xbc\xdb\xb8\xf1\xb1\xe4\xbb\xaf\xb7\xbd\xca\xbd
    :param itemTradedChangePriceValue: \xb5\xc0\xbe\xdf\xbc\xc6\xca\xfd\xbc\xdb\xb8\xf1\xb1\xe4\xbb\xaf\xb7\xf9\xb6\xc8
    :param count: \xc9\xcc\xb5\xea\xc5\xfa\xc1\xbf\xc2\xf4\xb3\xf6\xca\xfd
    :param sellForce: \xcd\xe6\xbc\xd2\xc7\xbf\xd6\xc6\xb9\xba\xc2\xf2(\xbc\xb4\xba\xf6\xc2\xd4\xbc\xdb\xb8\xf1\xb2\xee\xbe\xaf\xb8\xe6)
    :return:
    """
    for i in xrange(count):
        money -= nowPrice
        if money < 0:
            return (gametypes.DYNAMIC_SHOP_BUY_FAIL_MONEY_LIMIT, money)
        if abs(sourcePrice - nowPrice) / float(nowPrice) > SCD.data.get('dynamicShopPriceGapWarningValue', 0.05) and not sellForce:
            return (gametypes.DYNAMIC_SHOP_BUY_FAIL_PRICE_WARN, money)
        changePriceCount += 1
        if changePriceCount < itemTradedChangePriceCount:
            continue
        changePriceCount = 0
        if itemTradedChangePriceType == gametypes.DYNAMIC_SHOP_ITEM_TRADED_REFRESH_PRICE_TYPE_VALUE:
            nowPrice = sMath.clamp(nowPrice + int(itemTradedChangePriceValue), minPrice, maxPrice)
        elif itemTradedChangePriceType == gametypes.DYNAMIC_SHOP_ITEM_TRADED_REFRESH_PRICE_TYPE_PERCENT:
            nowPrice = sMath.clamp(int(nowPrice * (1 + itemTradedChangePriceValue)), minPrice, maxPrice)

    return (gametypes.DYNAMIC_SHOP_BUY_SUCCESS, money)


def _evaluateData(fieldName, data, locals = {}):
    script = data.get(fieldName, '')
    if script:
        try:
            return FormularEvalEnv.evaluate(script, locals)
        except:
            gamelog.error('_evaluateData wrong!', fieldName, data, locals)
            return 0

    else:
        return 0


def checkBuyPriceGap(dynamicShopType, changePriceCount, minPrice, maxPrice, sourcePrice, nowPrice, itemTradedChangePriceCount, itemTradedChangePriceType, itemTradedChangePriceValue, count, buyForce):
    totalMoney = 0
    for i in xrange(count):
        if abs(sourcePrice - nowPrice) / float(nowPrice) > SCD.data.get('dynamicShopPriceGapWarningValue', 0.05) and not buyForce:
            return (gametypes.DYNAMIC_SHOP_BUY_FAIL_PRICE_WARN, totalMoney)
        changePriceCount -= 1
        if dynamicShopType == gametypes.DYNAMIC_SHOP_TYPE_BUY_AND_SELL:
            totalMoney += max(1, int(nowPrice * SCD.data.get('dynamicShopSellPricePercent', 0.85)))
        else:
            totalMoney += nowPrice
        if abs(changePriceCount) < itemTradedChangePriceCount:
            continue
        changePriceCount = 0
        if itemTradedChangePriceType == gametypes.DYNAMIC_SHOP_ITEM_TRADED_REFRESH_PRICE_TYPE_VALUE:
            nowPrice = sMath.clamp(nowPrice + int(itemTradedChangePriceValue), minPrice, maxPrice)
        elif itemTradedChangePriceType == gametypes.DYNAMIC_SHOP_ITEM_TRADED_REFRESH_PRICE_TYPE_PERCENT:
            nowPrice = sMath.clamp(int(nowPrice * (1 + itemTradedChangePriceValue)), minPrice, maxPrice)

    return (gametypes.DYNAMIC_SHOP_BUY_SUCCESS, totalMoney)


class DynamicShopItemVal(UserSoleType):

    def __init__(self, setId, price, minPrice, maxPrice, inventory, maxInventory, tradedCount = 0, lastCyclePlayerTradedCount = 0, lastCycleItemTradedCount = 0, lastPriceRefreshTime = 0, lastInventoryRefreshTime = 0, lastTradeRefreshTime = 0):
        """
        
        :param setId: \xb8\xa1\xb6\xaf\xc9\xcc\xb5\xea\xb9\xe6\xd4\xf2id
        :param price: \xbc\xdb\xb8\xf1
        :param minPrice: \xbc\xdb\xb8\xf1\xcf\xc2\xcf\xde
        :param maxPrice: \xbc\xdb\xb8\xf1\xc9\xcf\xcf\xde
        :param inventory: \xbf\xe2\xb4\xe6
        :param maxInventory: \xbf\xe2\xb4\xe6\xc9\xcf\xcf\xde
        :param lastCyclePlayerTradedCount:
        :param lastCycleItemTradedCount:
        """
        self.setId = setId
        self.price = price
        self.minPrice = minPrice
        self.maxPrice = maxPrice
        self.inventory = inventory
        self.maxInventory = maxInventory
        self.tradedCount = tradedCount
        self.lastCyclePlayerTradedCount = lastCyclePlayerTradedCount
        self.lastCycleItemTradedCount = lastCycleItemTradedCount
        self.lastPriceRefreshTime = lastPriceRefreshTime
        self.lastInventoryRefreshTime = lastInventoryRefreshTime
        self.lastTradeRefreshTime = lastTradeRefreshTime

    def _lateReload(self):
        super(DynamicShopItemVal, self)._lateReload()


class DynamicShopItemInfo(UserDictType):

    def __init(self):
        super(DynamicShopItemInfo, self).__init__()

    def _lateReload(self):
        super(DynamicShopItemInfo, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()

    def addItemInfo(self, setId, price, minPrice, maxPrice, inventory, maxInventory, lastCyclePlayerTradedCount, lastCycleItemTradedCount, lastPriceRefreshTime = 0, lastInventoryRefreshTime = 0, lastTradeRefreshTime = 0):
        self[setId] = DynamicShopItemVal(setId, price, minPrice, maxPrice, inventory, maxInventory, lastCyclePlayerTradedCount=lastCyclePlayerTradedCount, lastCycleItemTradedCount=lastCycleItemTradedCount, lastPriceRefreshTime=lastPriceRefreshTime, lastInventoryRefreshTime=lastInventoryRefreshTime, lastTradeRefreshTime=lastTradeRefreshTime)

    def updateItemInfo(self, setId, price, minPrice, maxPrice, inventory, maxInventory, lastCyclePlayerTradedCount, lastCycleItemTradedCount, lastPriceRefreshTime, lastInventoryRefreshTime, lastTradeRefreshTime):
        if not self.has_key(setId):
            return
        if price != -1:
            self[setId].price = price
        if minPrice != -1:
            self[setId].minPrice = minPrice
        if maxPrice != -1:
            self[setId].maxPrice = maxPrice
        if inventory != -1:
            self[setId].inventory = inventory
        if maxInventory != -1:
            self[setId].maxInventory = maxInventory
        if lastCyclePlayerTradedCount != -1:
            self[setId].lastCyclePlayerTradedCount = lastCyclePlayerTradedCount
        if lastCycleItemTradedCount != -1:
            self[setId].lastCycleItemTradedCount = lastCycleItemTradedCount
        if lastPriceRefreshTime != -1:
            self[setId].lastPriceRefreshTime = lastPriceRefreshTime
        if lastInventoryRefreshTime != -1:
            self[setId].lastInventoryRefreshTime = lastInventoryRefreshTime
        if lastTradeRefreshTime != -1:
            self[setId].lastTradeRefreshTime = lastTradeRefreshTime

    def delItemInfo(self, setIds):
        for id in setIds:
            self.pop(id, None)

    def updateLastCyclePlayerTradedCount(self, setId, count):
        if not self.has_key(setId):
            return
        self[setId].lastCyclePlayerTradedCount = count

    def getLastCyclePlayerTradedCount(self, setId):
        if not self.has_key(setId):
            return 0
        return self[setId].lastCyclePlayerTradedCount

    def updateLastCycleItemTradedCount(self, setId, count):
        if not self.has_key(setId):
            return
        self[setId].lastCycleItemTradedCount = count

    def getLastCycleItemTradedCount(self, setId):
        if not self.has_key(setId):
            return 0
        return self[setId].lastCycleItemTradedCount

    def updateItemPrice(self, setId, priceChangeType, priceChangeValue):
        if not self.has_key(setId):
            return
        if priceChangeType == gametypes.DYNAMIC_SHOP_PRICE_REFRESH_TYPE_VALUE:
            self[setId].price = sMath.clamp(self[setId].price + int(priceChangeValue), self[setId].minPrice, self[setId].maxPrice)
        elif priceChangeType == gametypes.DYNAMIC_SHOP_PRICE_REFRESH_TYPE_PERCENT:
            self[setId].price = sMath.clamp(int(self[setId].price * (1 + priceChangeValue)), self[setId].minPrice, self[setId].maxPrice)

    def updateItemMinMaxPrice(self, setId, priceFix):
        if not self.has_key(setId):
            return
        self.initItemMinPrice(setId, priceFix)
        self.initItemMaxPrice(setId, priceFix)

    def initItemPrice(self, setId, priceFix):
        if not self.has_key(setId):
            return
        self[setId].price = min(int(self[setId].price * priceFix), const.DYNAMIC_SHOP_MAX_PRICE)

    def initItemMaxPrice(self, setId, priceFix):
        if not self.has_key(setId):
            return
        initialMaxPrice = DSID.data.get(setId, {}).get('initialMaxPrice')
        if initialMaxPrice and initialMaxPrice > 0:
            self[setId].maxPrice = min(int(initialMaxPrice * priceFix), const.DYNAMIC_SHOP_MAX_PRICE)

    def initItemMinPrice(self, setId, priceFix):
        if not self.has_key(setId):
            return
        initialMinPrice = DSID.data.get(setId, {}).get('initialMinPrice')
        if initialMinPrice and initialMinPrice > 0:
            self[setId].maxPrice = min(int(initialMinPrice * priceFix), const.DYNAMIC_SHOP_MAX_PRICE)

    def updateItemInventory(self, setId, inventoryChangeType, inventoryChangeValue):
        if not self.has_key(setId):
            return
        if inventoryChangeType == gametypes.DYNAMIC_SHOP_INVENTORY_REFRESH_TYPE_VALUE:
            self[setId].inventory += int(inventoryChangeValue)
        elif inventoryChangeType == gametypes.DYNAMIC_SHOP_INVENTORY_REFRESH_TYPE_PERCENT:
            self[setId].inventory = int(self[setId].inventory * (1 + inventoryChangeValue))
        elif inventoryChangeType == gametypes.DYNAMIC_SHOP_INVENTORY_REFRESH_TYPE_FULL:
            self[setId].inventory = self[setId].maxInventory
        elif inventoryChangeType == gametypes.DYNAMIC_SHOP_INVENTORY_REFRESH_TYPE_EMPTY:
            self[setId].inventory = 0

    def updateItemMaxInventory(self, setId, value):
        if not self.has_key(setId):
            return
        self[setId].maxInventory = value

    def listItemInfo(self, setId):
        info = []
        if setId != 0:
            self._listItemInfo(info, setId)
            return info
        for setId in self.keys():
            self._listItemInfo(info, setId)

        return info

    def _listItemInfo(self, info, setId):
        if not self.has_key(setId):
            return
        value = self[setId]
        info.append({'setId': value.setId,
         'price': value.price,
         'minPrice': value.minPrice,
         'maxPrice': value.maxPrice,
         'inventory': value.inventory,
         'maxInventory': value.maxInventory,
         'tradedCount': value.tradedCount,
         'lastCyclePlayerTradedCount': value.lastCyclePlayerTradedCount,
         'lastCycleItemTradedCount': value.lastCycleItemTradedCount,
         'lastPriceRefreshTime': time.ctime(value.lastPriceRefreshTime),
         'lastInventoryRefreshTime': time.ctime(value.lastInventoryRefreshTime),
         'lastTradeRefreshTime': time.ctime(value.lastTradeRefreshTime)})
