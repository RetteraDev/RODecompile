#Embedded file name: I:/bag/tmp/tw2/res/entities\common/dynamicShopInfo.o
from userInfo import UserInfo
from dynamicShop import *

class dynamicShopItemInfo(UserInfo):

    def createObjFromDict(self, dict):
        obj = DynamicShopItemInfo()
        for child in dict['data']:
            lastPriceRefreshTime = 0
            if child.has_key('lastPriceRefreshTime') and child['lastPriceRefreshTime']:
                lastPriceRefreshTime = child['lastPriceRefreshTime']
            lastInventoryRefreshTime = 0
            if child.has_key('lastInventoryRefreshTime') and child['lastInventoryRefreshTime']:
                lastInventoryRefreshTime = child['lastInventoryRefreshTime']
            lastTradeRefreshTime = 0
            if child.has_key('lastTradeRefreshTime') and child['lastTradeRefreshTime']:
                lastTradeRefreshTime = child['lastTradeRefreshTime']
            tmpVal = DynamicShopItemVal(child['setId'], child['price'], child['minPrice'], child['maxPrice'], child['inventory'], child['maxInventory'], child['tradedCount'], child['lastCyclePlayerTradedCount'], child['lastCycleItemTradedCount'], lastPriceRefreshTime, lastInventoryRefreshTime, lastTradeRefreshTime)
            obj[tmpVal.setId] = tmpVal

        return obj

    def getDictFromObj(self, obj):
        info = []
        for tempInfo in obj.itervalues():
            tempValue = {'setId': tempInfo.setId,
             'price': tempInfo.price,
             'minPrice': tempInfo.minPrice,
             'maxPrice': tempInfo.maxPrice,
             'inventory': tempInfo.inventory,
             'maxInventory': tempInfo.maxInventory,
             'tradedCount': tempInfo.tradedCount,
             'lastCyclePlayerTradedCount': tempInfo.lastCyclePlayerTradedCount,
             'lastCycleItemTradedCount': tempInfo.lastCycleItemTradedCount,
             'lastPriceRefreshTime': tempInfo.lastPriceRefreshTime,
             'lastInventoryRefreshTime': tempInfo.lastInventoryRefreshTime,
             'lastTradeRefreshTime': tempInfo.lastTradeRefreshTime}
            info.append(tempValue)

        return {'data': info}

    def isSameType(self, obj):
        return type(obj) is DynamicShopItemInfo


shopInstance = dynamicShopItemInfo()
