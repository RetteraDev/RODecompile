#Embedded file name: /WORKSPACE/data/entities/common/consignment.o
import BigWorld
import const
import formula
import utils
import gameglobal
from guis import uiConst
from data import item_data as ID
from cdata import game_msg_def_data as GMDD
SEARCH_STAMP_ID = 0
CACHE_STAMP_NUM = 10

def _cmp_quality(x, y):
    it1 = x[1]
    it2 = y[1]
    if it1.quality != it2.quality:
        return cmp(it1.quality, it2.quality)
    else:
        return cmp(x[0], y[0])


def _cmp_item_id(x, y):
    it1 = x[1]
    it2 = y[1]
    if it1.id != it2.id:
        return cmp(it1.id, it2.id)
    else:
        return cmp(x[0], y[0])


def _cmp_level(x, y):
    it1 = x[1]
    lv1 = it1.lvReq
    it2 = y[1]
    lv2 = it2.lvReq
    if lv1 != lv2:
        return cmp(lv1, lv2)
    else:
        return cmp(x[0], y[0])


def _cmp_end_time(x, y):
    it1 = x[1]
    it2 = y[1]
    if it1._consignEndT != it2._consignEndT:
        return cmp(it1._consignEndT, it2._consignEndT)
    else:
        return cmp(x[0], y[0])


def _cmp_bid_unit_price(x, y):
    it1 = x[1]
    it2 = y[1]
    p1 = formula.ceilIntDivide(it1._consignPrice, it1.cwrap)
    p2 = formula.ceilIntDivide(it2._consignPrice, it2.cwrap)
    if p1 != p2:
        return cmp(p1, p2)
    else:
        return cmp(x[0], y[0])


def _cmp_fixed_unit_price(x, y):
    it1 = x[1]
    it2 = y[1]
    p1 = formula.ceilIntDivide(it1._consignFixedPrice, it1.cwrap)
    p2 = formula.ceilIntDivide(it2._consignFixedPrice, it2.cwrap)
    if p1 != p2:
        if not p1:
            return 1
        elif not p2:
            return -1
        else:
            return cmp(p1, p2)
    else:
        return cmp(x[0], y[0])


def _cmp_bid_price(x, y):
    it1 = x[1]
    it2 = y[1]
    if it1._consignPrice != it2._consignPrice:
        return cmp(it1._consignPrice, it2._consignPrice)
    else:
        return cmp(x[0], y[0])


def _cmp_fixed_price(x, y):
    it1 = x[1]
    it2 = y[1]
    if it1._consignFixedPrice != it2._consignFixedPrice:
        if not it1._consignFixedPrice:
            return 1
        elif not it2._consignFixedPrice:
            return -1
        else:
            return cmp(it1._consignFixedPrice, it2._consignFixedPrice)
    else:
        return cmp(x[0], y[0])


class Consignment(object):

    def __init__(self):
        self.itemCache = {}
        self.itemStamp = -1
        self.itemCursor = -1
        self.searchSortType = const.ITEM_CONSIGN_SORT_BY_FIXED_UNIT_PRICE
        self.searchOrderType = 1
        self.historySearchOrderType = {}
        self.itemPrices = {}
        self.searchForData = {}
        self.curPage = 0
        self.totalPages = 1
        self.owner = None
        self.searchState = []
        self.stamps = []
        self.consignType = uiConst.CONSIGN_TYPE_COMMON

    def clearCache(self):
        self.itemCache.clear()
        self.curPage = 0
        self.searchState = []
        self.totalPages = 1

    def createStamp(self):
        global CACHE_STAMP_NUM
        global SEARCH_STAMP_ID
        SEARCH_STAMP_ID += 1
        stamp = SEARCH_STAMP_ID
        self.stamps.append(stamp)
        if len(self.stamps) > CACHE_STAMP_NUM:
            self.stamps.pop(0)
        return stamp

    def ownStamp(self, stamp):
        return stamp in self.stamps

    def onShowOthers(self, data):
        stamp, cursor, page, totalPages, items = data
        if stamp != self.itemStamp:
            self.itemCache.clear()
            self.totalPages = totalPages
        self.itemCache[page] = items
        if items and cursor != items[-1][0]:
            self.reachEnd = False
        else:
            self.reachEnd = True
        self.curPage = page
        self.itemStamp = stamp
        self.itemCursor = cursor
        searchSortType, searchOrderType = self.searchForData.pop(stamp, (self.searchSortType, self.searchOrderType))
        gameglobal.rds.ui.consign.updateSortState(searchSortType, searchOrderType)
        gameglobal.rds.ui.tabAuctionConsign.updateSortState(searchSortType, searchOrderType)
        self.showPage()

    def setSearchSortBy(self, sortId, orderType = None):
        if sortId == self.searchSortType:
            if orderType == None:
                self.searchOrderType = 1 - self.searchOrderType
            else:
                self.searchOrderType = orderType
            self.historySearchOrderType[sortId] = self.searchOrderType
        else:
            if orderType == None:
                orderType = self.historySearchOrderType.get(sortId)
                if not orderType:
                    orderType = const.ITEM_CONSIGN_SORT[sortId]['default']
            else:
                orderType = orderType
            self.searchSortType = sortId
            self.searchOrderType = orderType
            self.historySearchOrderType[sortId] = self.searchOrderType

    def searchSortBy(self, sortId, orderType = None):
        if not const.ITEM_CONSIGN_SORT.get(sortId):
            return
        self.setSearchSortBy(sortId, orderType)
        self.refreshCurrentPage(newSearch=True)

    def onUpdateOthers(self, dbID, data):
        if not data:
            self.itemCache.clear()
            self.curPage = 0
            self.itemCursor = -1
            self.refreshCurrentPage(clearFollowingCache=True)
        else:
            for page, items in self.itemCache.iteritems():
                for _, itemData in enumerate(items):
                    if itemData[0] == dbID:
                        item = itemData[1]
                        if self.consignType == uiConst.CONSIGN_TYPE_COMMON:
                            itemCount, bidPrice, fixedPrice, tModify, bidderRole = data
                            hasBidder = not not bidderRole
                        elif self.consignType == uiConst.CONSIGN_TYPE_COIN:
                            itemCount, bidPrice, tModify = data
                            fixedPrice = bidPrice * itemCount
                            bidderRole = ''
                            hasBidder = False
                        item.setWrap(itemCount)
                        item.updateProp({'_consignPrice': bidPrice,
                         '_consignFixedPrice': fixedPrice,
                         '_consignModifyT': tModify,
                         '_consignBid': hasBidder,
                         '_consignBidderRole': bidderRole})
                        if page == self.curPage:
                            self.showPage()
                        break

    def searchByName(self, owner, name, school = -1, forme = False, mType = -1, sType = -1, itemIdArr = None, bSearch = False):
        itemIds = []
        if itemIdArr:
            itemIds = itemIdArr
        p = BigWorld.player()
        hasItemName = False
        if not itemIds and bSearch:
            for itemId in ID.data.iterkeys():
                itemData = ID.data.get(itemId)
                itemName = itemData.get('name', '')
                if len(name) > len(itemName):
                    continue
                if name in itemName:
                    if self.consignType == uiConst.CONSIGN_TYPE_COMMON and utils.getItemNoConsign(itemData):
                        continue
                    if self.consignType == uiConst.CONSIGN_TYPE_COIN and not utils.getItemCoinConsign(itemData):
                        continue
                    if forme:
                        if itemData.get('lvReq', 0) > p.lv:
                            continue
                        if p.school not in itemData.get('schReq', ()):
                            continue
                    elif school != -1:
                        if school not in itemData.get('schReq', ()):
                            continue
                    if mType != -1:
                        if mType != itemData.get('category', 0):
                            continue
                        if sType != -1 and sType != itemData.get('subcategory', 0):
                            continue
                    hasItemName = hasItemName or itemName == name
                    if itemName == name:
                        itemIds.insert(0, itemId)
                    else:
                        itemIds.append(itemId)
                    if len(itemIds) >= const.ITEM_CONSIGN_MATCH and hasItemName:
                        break

        if len(itemIds) >= const.ITEM_CONSIGN_MATCH and not hasItemName:
            BigWorld.player().showGameMsg(GMDD.data.CONSIGN_SEARCH_MATCH_FUZZY, ())
            return False
        if not itemIds:
            BigWorld.player().showGameMsg(GMDD.data.CONSIGN_SEARCH_MATCH_EMPTY, ())
            return False
        self._commitSearchByName(owner, itemIds[:min(len(itemIds), const.ITEM_CONSIGN_MATCH)])
        return True

    def _getSearchInfo(self):
        return (self.searchSortType, self.searchOrderType)

    def _commitSearchByName(self, owner, itemIds):
        stamp = self.createStamp()
        self.searchForData[stamp] = self._getSearchInfo()
        if self.consignType == uiConst.CONSIGN_TYPE_COMMON:
            if owner != None:
                owner.cell.searchConsignByID(itemIds, stamp, 0, self.searchSortType, self.searchOrderType)
        elif self.consignType == uiConst.CONSIGN_TYPE_COIN:
            BigWorld.player().base.searchCoinConsignByID(itemIds, stamp, 0, self.searchSortType, self.searchOrderType)
        self.owner = owner
        self.searchState = ['searchConsignByID', itemIds]

    def searchByType(self, owner, mtype, stype, dtype, quality = 0, minLv = 0, maxLv = const.MAX_LEVEL, school = 0, forme = False):
        if not minLv:
            minLv = -1
        if maxLv == const.MAX_LEVEL:
            maxLv = -1
        if not quality:
            quality = -1
        if not school:
            school = -1
        self._commitSearchByType(owner, mtype, stype, dtype, quality, minLv, maxLv, school, forme)

    def _commitSearchByType(self, owner, mtype, stype, dtype, quality, minLv, maxLv, school, forme):
        stamp = self.createStamp()
        self.searchForData[stamp] = self._getSearchInfo()
        if self.consignType == uiConst.CONSIGN_TYPE_COMMON:
            owner.cell.searchConsignByType(stamp, 0, mtype, stype, dtype, quality, minLv, maxLv, school, forme, self.searchSortType, self.searchOrderType)
            self.searchState = ['searchConsignByType',
             mtype,
             stype,
             dtype,
             quality,
             minLv,
             maxLv,
             school,
             forme]
        elif self.consignType == uiConst.CONSIGN_TYPE_COIN:
            BigWorld.player().base.searchCoinConsignByType(stamp, 0, mtype, stype, quality, minLv, maxLv, school, forme, self.searchSortType, self.searchOrderType)
            self.searchState = ['searchConsignByType',
             mtype,
             stype,
             quality,
             minLv,
             maxLv,
             school,
             forme]
        self.owner = owner

    def showPrevPage(self):
        if self.curPage > 0:
            if self.itemCache.get(self.curPage - 1):
                self.curPage -= 1
                self.showPage()
            else:
                self.refreshCurrentPage(self.curPage - 1)

    def showNextPage(self):
        if self.curPage >= self.totalPages - 1:
            return
        if self.itemCache.get(self.curPage + 1):
            self.curPage += 1
            self.showPage()
        else:
            self.refreshCurrentPage(self.curPage + 1)

    def gotoPage(self, page):
        if page < 0 or page >= self.totalPages:
            return
        if self.itemCache.get(page):
            self.curPage = page
            self.showPage()
        else:
            self.refreshCurrentPage(page)

    def refreshCurrentPage(self, page = -1, newSearch = False, clearFollowingCache = False):
        if not self.searchState:
            return
        funname = self.searchState[0]
        if page < 0:
            page = self.curPage
        if newSearch:
            page = 0
            stamp = self.createStamp()
            self.searchForData[stamp] = self._getSearchInfo()
        else:
            stamp = self.itemStamp
        if clearFollowingCache:
            for k in self.itemCache.keys():
                if k > page:
                    self.itemCache.pop(k)

        if self.consignType == uiConst.CONSIGN_TYPE_COMMON:
            if funname == 'searchConsignByID':
                self.owner.cell.searchConsignByID(self.searchState[1], stamp, page, self.searchSortType, self.searchOrderType)
            elif funname == 'searchConsignByType':
                self.owner.cell.searchConsignByType(stamp, page, *(self.searchState[1:] + [self.searchSortType, self.searchOrderType]))
        elif self.consignType == uiConst.CONSIGN_TYPE_COIN:
            if funname == 'searchConsignByID':
                BigWorld.player().base.searchCoinConsignByID(self.searchState[1], stamp, page, self.searchSortType, self.searchOrderType)
            elif funname == 'searchConsignByType':
                BigWorld.player().base.searchCoinConsignByType(stamp, page, *(self.searchState[1:] + [self.searchSortType, self.searchOrderType]))

    def getCurrentPageItems(self):
        items = self.itemCache.get(self.curPage, [])
        return items

    def getItemInCurrentPage(self, dbID):
        items = self.getCurrentPageItems()
        for _dbID, item in items:
            if _dbID == dbID:
                return item

    def showPage(self):
        gameglobal.rds.ui.consign.showOthers(self)
        gameglobal.rds.ui.tabAuctionConsign.showOthers(self)


class ConsignmentMine(Consignment):

    def __init__(self):
        super(ConsignmentMine, self).__init__()
        self.searchSortType = const.ITEM_CONSIGN_SORT_BY_FIXED_UNIT_PRICE
        self.searchOrderType = 1
        self.consignType = uiConst.CONSIGN_TYPE_COMMON
        self.itemCache = []

    def _getMyItems(self):
        p = BigWorld.player()
        if p:
            if self.consignType == uiConst.CONSIGN_TYPE_COMMON:
                return p.consignation
            if self.consignType == uiConst.CONSIGN_TYPE_COIN:
                return p.coinConsignData
        else:
            return {}

    def _sortBy(self, sortId, orderType):
        self.setSearchSortBy(sortId, orderType)
        myItems = self._getMyItems()
        reverse = self.searchOrderType == 0
        if self.searchSortType == const.ITEM_CONSIGN_SORT_BY_ID:
            keys = myItems.keys()
            keys.sort(reverse=True)
            items = []
            for dbID in keys:
                items.append((dbID, myItems[dbID]))

        elif self.searchSortType == const.ITEM_CONSIGN_SORT_BY_QUALITY:
            items = myItems.items()
            items.sort(cmp=_cmp_quality, reverse=reverse)
        elif self.searchSortType == const.ITEM_CONSIGN_SORT_BY_ITEM_ID:
            items = myItems.items()
            items.sort(cmp=_cmp_item_id, reverse=reverse)
        elif self.searchSortType == const.ITEM_CONSIGN_SORT_BY_LEVEL:
            items = myItems.items()
            items.sort(cmp=_cmp_level, reverse=reverse)
        elif self.searchSortType == const.ITEM_CONSIGN_SORT_BY_END_TIME:
            items = myItems.items()
            items.sort(cmp=_cmp_end_time, reverse=reverse)
        elif self.searchSortType == const.ITEM_CONSIGN_SORT_BY_BID_UNIT_PRICE:
            items = myItems.items()
            items.sort(cmp=_cmp_bid_unit_price, reverse=reverse)
        elif self.searchSortType == const.ITEM_CONSIGN_SORT_BY_BID_PRICE:
            items = myItems.items()
            items.sort(cmp=_cmp_bid_price, reverse=reverse)
        elif self.searchSortType == const.ITEM_CONSIGN_SORT_BY_FIXED_UNIT_PRICE:
            items = myItems.items()
            if self.consignType == uiConst.CONSIGN_TYPE_COMMON:
                items.sort(cmp=_cmp_fixed_unit_price, reverse=reverse)
            elif self.consignType == uiConst.CONSIGN_TYPE_COIN:
                items.sort(cmp=_cmp_bid_unit_price, reverse=reverse)
        elif self.searchSortType == const.ITEM_CONSIGN_SORT_BY_FIXED_PRICE:
            items = myItems.items()
            items.sort(cmp=_cmp_fixed_price, reverse=reverse)
        elif self.searchSortType == const.ITEM_CONSIGN_SORT_BY_UNIT_COIN:
            items = myItems.items()
            items.sort(cmp=_cmp_bid_price, reverse=reverse)
        self.itemCache = items

    def searchSortBy(self, sortId, orderType = None):
        if not const.ITEM_CONSIGN_SORT.get(sortId):
            return
        self._sortBy(sortId, orderType)
        self.curPage = 0
        self.totalPages = max(1, formula.ceilIntDivide(len(self.itemCache), const.ITEM_CONSIGN_PAGE_SIZE))
        gameglobal.rds.ui.consign.updateSortState(self.searchSortType, self.searchOrderType)
        gameglobal.rds.ui.consign.showMine()
        gameglobal.rds.ui.tabAuctionConsign.updateSortState(self.searchSortType, self.searchOrderType)
        gameglobal.rds.ui.tabAuctionConsign.showMine()

    def getCurrentPageItems(self):
        start = self.curPage * const.ITEM_CONSIGN_PAGE_SIZE
        end = min(len(self.itemCache), start + const.ITEM_CONSIGN_PAGE_SIZE)
        items = self.itemCache[start:end]
        return items

    def getItemInCurrentPage(self, dbID):
        myItems = self._getMyItems()
        for _dbID, item in myItems.iteritems():
            if _dbID == dbID:
                return item

    def showPrevPage(self):
        if self.curPage > 0:
            self.curPage -= 1
            self.showPage()

    def showNextPage(self):
        if self.curPage >= self.totalPages - 1:
            return
        self.curPage += 1
        self.showPage()

    def gotoPage(self, page):
        if page < 0 or page >= self.totalPages:
            return
        self.curPage = page
        self.showPage()

    def refreshCurrentPage(self):
        self._sortBy(self.searchSortType, self.searchOrderType)
        self.totalPages = max(1, formula.ceilIntDivide(len(self.itemCache), const.ITEM_CONSIGN_PAGE_SIZE))
        if not self.curPage < self.totalPages:
            self.curPage = self.totalPages - 1
        gameglobal.rds.ui.consign.showMine()
        gameglobal.rds.ui.tabAuctionConsign.showMine()

    def showPage(self):
        gameglobal.rds.ui.consign.showMine()
        gameglobal.rds.ui.tabAuctionConsign.showMine()

    def clearCache(self):
        self.itemCache = []
        self.curPage = 0
        self.searchState = []
        self.totalPages = 1


class ConsignmentMyBid(ConsignmentMine):

    def __init__(self):
        super(ConsignmentMyBid, self).__init__()
        self._inited = False

    def _getMyItems(self):
        p = BigWorld.player()
        if p:
            return p.consignBidItems
        else:
            return {}


class ConsignmentTradeHistory(ConsignmentMine):

    def __init__(self):
        super(ConsignmentTradeHistory, self).__init__()
        self._inited = False

    def _getMyItems(self):
        p = BigWorld.player()
        if p and hasattr(p, 'consignTradeHistory'):
            return p.consignTradeHistory
        else:
            return []

    def _sortBy(self, sortId, orderType):
        self.setSearchSortBy(sortId, orderType)
        self.itemCache = self._getMyItems()

    def refreshCurrentPage(self):
        self._sortBy(self.searchSortType, self.searchOrderType)
        self.totalPages = max(1, formula.ceilIntDivide(len(self.itemCache), const.ITEM_CONSIGN_PAGE_SIZE))
        if not self.curPage < self.totalPages:
            self.curPage = self.totalPages - 1
        gameglobal.rds.ui.consign.showTradeHistory()
        gameglobal.rds.ui.tabAuctionConsign.showTradeHistory()
