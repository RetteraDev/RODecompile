#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/resourceMarketManager.o
from gamestrings import gameStrings
import BigWorld
import const
import gamelog
import utils
import uiUtils
from gameclass import Singleton
from data import item_data as ID
from data import life_skill_market_data as LSMD
from data import life_skill_config_data as LSCD
from data import life_skill_market_desc_data as LSMDD

class DealInfo(object):

    def __init__(self, dealInfo, marketId):
        self.marketId = marketId
        self.dealInfo = dealInfo

    def getPanelInfo(self):
        self.dealInfo['itemName'] = ID.data[self.dealInfo['icon']['itemId']]['name']
        return self.dealInfo

    def dealConfirmClick(self, itemId, amount, price):
        pass

    def calcTotalPrice(self, owner, cnt, curCnt):
        pass

    def updateDealInfo(self, itemId, count, price):
        if self.dealInfo['icon']['itemId'] != itemId:
            return
        self.dealInfo['levelDesc'] = uiUtils.getLevelDesc(self.dealInfo['price'], price)
        self.dealInfo['adjustPrice'] = self.dealInfo['price']
        self.dealInfo['price'] = price
        self.dealInfo['icon']['count'] -= count


class SellInfo(DealInfo):

    def __init__(self, dealInfo, marketId):
        super(SellInfo, self).__init__(dealInfo, marketId)

    def getPanelInfo(self):
        super(SellInfo, self).getPanelInfo()
        self.dealInfo['icon']['iconPath'] = uiUtils.getItemIconFile64(self.dealInfo['icon']['itemId'])
        self.dealInfo['tax'] = str(LSCD.data.get('marketTax', 15)) + '%'
        return self.dealInfo

    def dealConfirmClick(self, marketId, itemId, amount, price):
        p = BigWorld.player()
        p.cell.sellToMarket(marketId, itemId, amount, price)

    def calcTotalPrice(self, owner, cnt):
        itemInfo = LSMD.data.get((self.marketId, self.dealInfo['icon']['itemId']), None)
        if itemInfo is None:
            return 0
        else:
            cntStep = LSCD.data.get('marketCntStep', 10)
            curCnt = owner.getCnt(self.dealInfo['icon']['itemId'])
            price = owner.getPrice(self.dealInfo['icon']['itemId'])
            priceStep = itemInfo['priceStep']
            priceLowest = itemInfo['priceLowest']
            gamelog.debug('@hjx market#SellInfo#calcTotalPrice:', cnt, curCnt, cntStep, price, priceStep, priceLowest)
            return utils.calcSellPriceInMarket(cnt, curCnt, cntStep, price, priceStep, priceLowest)


class BuyInfo(DealInfo):

    def __init__(self, dealInfo, marketId):
        super(BuyInfo, self).__init__(dealInfo, marketId)

    def dealConfirmClick(self, marketId, itemId, amount, price):
        p = BigWorld.player()
        p.cell.buyFromMarket(marketId, itemId, amount, price)

    def calcTotalPrice(self, owner, cnt):
        itemInfo = LSMD.data.get((self.marketId, self.dealInfo['icon']['itemId']), None)
        if itemInfo is None:
            return 0
        else:
            cntStep = LSCD.data.get('marketCntStep', 10)
            curCnt = owner.getCnt(self.dealInfo['icon']['itemId'])
            price = owner.getPrice(self.dealInfo['icon']['itemId'])
            priceStep = itemInfo['priceStep']
            priceHighest = itemInfo['priceHighest']
            gamelog.debug('@hjx market#BuyInfo#calcTotalPrice:', cnt, curCnt, cntStep, price, priceStep, priceHighest)
            return utils.calcBuyPriceInMarket(cnt, curCnt, cntStep, price, priceStep, priceHighest)


class MarketInfo(object):

    def __init__(self, marketId, marketInfo, tabType):
        self.marketId = marketId
        self.marketInfo = marketInfo
        self.tabType = tabType
        self.dealIns = None
        self.reset()

    def reset(self):
        self.sellIndex = -1
        self.buyIndex = -1
        self.tabType = 0

    def getMarketPanelInfo(self):
        info = {}
        p = BigWorld.player()
        info['tax'] = LSCD.data.get('marketTax', 15)
        info['cash'] = p.cash
        info['dialog'] = gameStrings.TEXT_RESOURCEMARKETMANAGER_107
        return uiUtils.dict2GfxDict(info, True)

    def getMarketInfo(self):
        self.resInfo = []
        for itemId, val in self.marketInfo.iteritems():
            itemInfo = {}
            resource = LSMD.data.get((self.marketId, itemId), None)
            if resource is None:
                continue
            if self.tabType != 0 and resource['typeId'] != self.tabType:
                continue
            if const.LIFE_SKILL_MARKET_FLAG_HOT & val['flag']:
                continue
            iconPath = uiUtils.getItemIconFile64(itemId)
            itemInfo['icon'] = {'iconPath': iconPath,
             'itemId': itemId,
             'count': val['count']}
            itemInfo['price'] = val['price']
            itemInfo['flag'] = val['flag']
            itemInfo['maxCount'] = resource['maxCnt']
            itemInfo['curCount'] = val['count']
            itemInfo['fame'] = val.get('fame', 1)
            itemInfo['levelDesc'] = uiUtils.getLevelDesc(val['adjustPrice'], val['price'])
            self.resInfo.append(itemInfo)

        return uiUtils.array2GfxAarry(self.resInfo)

    def getTitleInfo(self):
        info = {}
        info['type1'] = LSMDD.data[self.marketId].get(1, gameStrings.TEXT_RESOURCEMARKETMANAGER_145)
        info['type2'] = LSMDD.data[self.marketId].get(2, gameStrings.TEXT_RESOURCEMARKETMANAGER_146)
        info['type3'] = LSMDD.data[self.marketId].get(3, gameStrings.TEXT_RESOURCEMARKETMANAGER_147)
        return uiUtils.dict2GfxDict(info, True)

    def getHotResourceInfo(self):
        self.hotResInfo = []
        for itemId, val in self.marketInfo.iteritems():
            itemInfo = {}
            resource = LSMD.data.get((self.marketId, itemId), None)
            if resource is None:
                continue
            if const.LIFE_SKILL_MARKET_FLAG_HOT & val['flag'] == 0:
                continue
            iconPath = uiUtils.getItemIconFile64(itemId)
            itemInfo['icon'] = {'iconPath': iconPath,
             'itemId': itemId,
             'count': val['count']}
            itemInfo['price'] = val['price']
            itemInfo['flag'] = val['flag']
            itemInfo['fame'] = val.get('fame', 1)
            itemInfo['maxCount'] = resource['maxCnt']
            itemInfo['levelDesc'] = uiUtils.getLevelDesc(val['adjustPrice'], val['price'])
            self.hotResInfo.append(itemInfo)

        return uiUtils.array2GfxAarry(self.hotResInfo)

    def inMaket(self, itemId):
        if (self.marketId, itemId) not in LSMD.data or not self.marketInfo.has_key(itemId):
            return False
        else:
            return True

    def getMarketItem(self, itemId):
        return self.marketInfo.get(itemId)

    def getPrice(self, itemId):
        if not self.marketInfo.has_key(itemId):
            return 0
        return self.marketInfo[itemId]['price']

    def getCnt(self, itemId):
        if not self.marketInfo.has_key(itemId):
            return 0
        return self.marketInfo[itemId]['count']

    def getBagInfo(self):
        self.bagInfo = []
        p = BigWorld.player()
        for pg in p.inv.getPageTuple():
            for ps in p.inv.getPosTuple(pg):
                it = p.inv.getQuickVal(pg, ps)
                itemInfo = {}
                if it == const.CONT_EMPTY_VAL:
                    continue
                if it.isExpireTTL():
                    continue
                if it.hasLatch():
                    continue
                if not self.inMaket(it.id):
                    continue
                resource = LSMD.data.get((self.marketId, it.id), {})
                itemInfo['maxCount'] = resource.get('maxCnt', 0)
                iconPath = uiUtils.getItemIconFile40(it.id)
                itemInfo['icon'] = {'iconPath': iconPath,
                 'itemId': it.id,
                 'count': it.cwrap}
                itemInfo['price'] = self.getPrice(it.id)
                item = self.getMarketItem(it.id)
                if item:
                    itemInfo['levelDesc'] = uiUtils.getLevelDesc(item['adjustPrice'], item['price'])
                    itemInfo['curCount'] = item['count']
                self.bagInfo.append(itemInfo)

        return uiUtils.array2GfxAarry(self.bagInfo)

    def setTabType(self, tabType):
        self.tabType = tabType

    def createDealIns(self, typeStr, index):
        if typeStr == 'sell':
            self.dealIns = SellInfo(self.bagInfo[index], self.marketId)
        elif typeStr == 'buy':
            self.dealIns = BuyInfo(self.resInfo[index], self.marketId)
        elif typeStr == 'buyHot':
            self.dealIns = BuyInfo(self.hotResInfo[index], self.marketId)
        else:
            print '@hjx error createDealIns:', typeStr

    def getDealPanelInfo(self):
        if self.dealIns is None:
            return {}
        else:
            return self.dealIns.getPanelInfo()

    def updateDealInfo(self, mid, itemId, count, price):
        if mid != self.marketId:
            return
        self.marketInfo[itemId]['adjustPrice'] = self.marketInfo[itemId]['price']
        self.marketInfo[itemId]['price'] = price
        if self.dealIns.__class__.__name__ == 'SellInfo':
            self.marketInfo[itemId]['count'] += count
        else:
            self.marketInfo[itemId]['count'] -= count
        self.dealIns.updateDealInfo(itemId, count, price)

    def dealConfirmClick(self, itemId, amount, price):
        if self.dealIns is None:
            return
        else:
            self.dealIns.dealConfirmClick(self.marketId, itemId, amount, price)
            return

    def calcTotalPrice(self, cnt):
        if self.dealIns is None:
            return
        else:
            return self.dealIns.calcTotalPrice(self, cnt)


class ResourceMarketManager(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.marketIns = None
        self.marketCache = {}
        self.timeStamp = 0

    def resetInsByMarketId(self, marketId, marketInfo, tabType, timeStamp):
        if marketId < 1 or marketId > const.LIFE_SKILL_ORG_NUM:
            gamelog.error('@hjx ResourceMarketManager#resetInsByMarketId error: marketId is over num!')
            return
        self.timeStamp = timeStamp
        self.marketIns = MarketInfo(marketId, marketInfo, tabType)

    def getMarketInfo(self):
        if self.marketIns is None:
            return uiUtils.array2GfxAarry([])
        else:
            return self.marketIns.getMarketInfo()

    def getTitleInfo(self):
        if self.marketIns is None:
            return uiUtils.dict2GfxDict({})
        else:
            return self.marketIns.getTitleInfo()

    def getHotResourceInfo(self):
        if self.marketIns is None:
            return uiUtils.array2GfxAarry([])
        else:
            return self.marketIns.getHotResourceInfo()

    def getBagInfo(self):
        if self.marketIns is None:
            return uiUtils.array2GfxAarry([])
        else:
            return self.marketIns.getBagInfo()

    def reset(self):
        self.timeStamp = 0
        if self.marketIns:
            self.marketIns.reset()


def getInstance():
    return ResourceMarketManager.getInstance()
