#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/consignProxy.o
from gamestrings import gameStrings
import math
import re
import time
import BigWorld
from Scaleform import GfxValue
import gamelog
import gameglobal
import gametypes
import const
import formula
import utils
import keys
import copy
import commcalc
import itemToolTipUtils
from guis import uiConst
from guis import pinyinConvert
from guis import uiUtils
from guis import ui
from searchHistoryUtils import SearchHistoryUtils
from ui import gbk2unicode
from ui import unicode2gbk
from uiProxy import SlotDataProxy
from consignment import Consignment, ConsignmentMine, ConsignmentMyBid
from consignment import ConsignmentTradeHistory
from callbackHelper import Functor
from guis import events
from cdata import game_msg_def_data as GMDD
from data import item_data as ID
from data import item_catagory_data as ICD
from data import school_data as SD
from cdata import font_config_data as FCD
from data import sys_config_data as SCD
from data import item_name_data as IND
from cdata import coin_consign_config_Data as CCCD
CATE_WEAPON = 1
CATE_ARMOR = 2
CATE_JEWELRY = 3
CATE_RIDE = 4
CATE_FASHION = 5
CATE_ITEM = 6
CATE_MATERIAL = 7
CATE_CONSUME = 8
CATE_OTHER = 9
BUY_PANEL = 0
SELL_PANEL = 1
MINE_PANEL = 2
MINE_BID_PANEL = 3
TRADE_HISTORY_PANEL = 4
SORT_BY_PARAM = 10
PRICE_MAX = 999999999

class ConsignProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(ConsignProxy, self).__init__(uiAdapter)
        self.modelMap = {'getCategory': self.onGetCategory,
         'selectCategory': self.onSelectCategory,
         'getQualityTypes': self.onGetQualityTypes,
         'searchItems': self.onSearchItems,
         'sellItem': self.onSellItem,
         'getItemMaxNum': self.onGetItemMaxNum,
         'cancelSellItem': self.onCancelSellItem,
         'bidItem': self.onBidItem,
         'buyItem': self.onBuyItem,
         'fitting': self.onFitting,
         'getSellRecord': self.onGetSellRecord,
         'sortItems': self.onSortItems,
         'closePanel': self.onClosePanel,
         'getCash': self.onGetCash,
         'changeKeepTime': self.onChangeKeepTime,
         'changeTab': self.onChangeTab,
         'closeBuyPanel': self.onCloseBuyPanel,
         'confirmBuy': self.onConfirmBuy,
         'getBuyItemInfo': self.onGetBuyItemInfo,
         'closeBidPanel': self.onCloseBidPanel,
         'confirmBid': self.onConfirmBid,
         'prevPage': self.onPrevPage,
         'nextPage': self.onNextPage,
         'firstPage': self.onFirstPage,
         'lastPage': self.onLastPage,
         'refreshContent': self.onRefreshContent,
         'getMinBidPrice': self.onGetMinBidPrice,
         'changeSortType': self.onChangeSortType,
         'gotoPage': self.onGotoPage,
         'removeItem': self.onRemoveItem,
         'numChange': self.onNumChange,
         'getItemNames': self.onGetItemNames,
         'priceChange': self.onPriceChange,
         'fixedPriceChange': self.onFixedPriceChange,
         'getTax': self.onGetTax,
         'setConsignType': self.onSetConsignType,
         'getCoinConsignEnable': self.onGetCoinConsignEnable,
         'getCoinConsignLimit': self.onGetCoinConsignLimit,
         'openExchangeWindow': self.onOpenCoinExchange,
         'getMaxCount': self.onGetMaxCount,
         'autoSearchByChangeTab': self.onAutoSearchByChangeTab,
         'getTabChangeCD': self.onGetTabChangeCD,
         'showTabChangeWarning': self.onShowTabChangeWarning,
         'getStorageFeeTip': self.onGetStorageFeeTip,
         'getSearchHistory': self.onGetSearchHistory,
         'getHistoryCfg': self.onGetHistoryCfg}
        self.mediator = None
        self.buyMediator = None
        self.bidMediator = None
        self.bindType = 'consign'
        self.type = 'consign'
        self.pageItems = None
        self.curDbId = None
        self.pageSrc = -1
        self.posSrc = -1
        self.npcId = 0
        self.dealAverage = 0
        self.average = 0
        self.fixedPrice = 0
        self.consignNum = 0
        self.tab = BUY_PANEL
        self.prices = {}
        self.coinPrices = {}
        self.priceSortBy = const.ITEM_CONSIGN_SORT_BY_FIXED_UNIT_PRICE
        self.bidTabInfoInited = False
        self.buyTabInfo = Consignment()
        self.sellTabInfo = Consignment()
        self.buyCoinTabInfo = Consignment()
        self.sellCoinTabInfo = Consignment()
        self.mineTabInfo = ConsignmentMine()
        self.mineCoinTabInfo = ConsignmentMine()
        self.historyTabInfo = ConsignmentTradeHistory()
        self.buyTabInfo.consignType = uiConst.CONSIGN_TYPE_COMMON
        self.sellTabInfo.consignType = uiConst.CONSIGN_TYPE_COMMON
        self.mineTabInfo.consignType = uiConst.CONSIGN_TYPE_COMMON
        self.buyCoinTabInfo.consignType = uiConst.CONSIGN_TYPE_COIN
        self.sellCoinTabInfo.consignType = uiConst.CONSIGN_TYPE_COIN
        self.mineCoinTabInfo.consignType = uiConst.CONSIGN_TYPE_COIN
        self.buyCoinTabInfo.searchSortType = const.ITEM_CONSIGN_SORT_BY_UNIT_COIN
        self.sellCoinTabInfo.searchSortType = const.ITEM_CONSIGN_SORT_BY_UNIT_COIN
        self.mineCoinTabInfo.searchSortType = const.ITEM_CONSIGN_SORT_BY_UNIT_COIN
        self.myBidTabInfo = ConsignmentMyBid()
        self.otherConsignments = [self.buyTabInfo,
         self.sellTabInfo,
         self.buyCoinTabInfo,
         self.sellCoinTabInfo]
        self.curTabInfo = self.buyTabInfo
        self.searchItemName = ''
        self.curConsignType = uiConst.CONSIGN_TYPE_COMMON
        self.keepTime = 0
        self.consignSearchHistory = ConsignSearchHistory()
        uiAdapter.registerEscFunc(uiConst.WIDGET_CONSIGN, self.hide)

    def clearData(self):
        self.myBidTabInfo = ConsignmentMyBid()
        self.bidTabInfoInited = False

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_CONSIGN:
            self.mediator = mediator
            self.consignSearchHistory.readConfigData()
            self.updateSortState()
            self.buyTabInfo.clearCache()
            self.sellTabInfo.clearCache()
            self.buyCoinTabInfo.clearCache()
            self.sellCoinTabInfo.clearCache()
            self.curTabInfo = self.buyTabInfo
            self.showTab()
            if self.searchItemName:
                self.searchItemsByName(self.searchItemName)
            return GfxValue(gbk2unicode(self.searchItemName))
        if widgetId == uiConst.WIDGET_CONSIGN_BUY:
            self.buyMediator = mediator
        elif widgetId == uiConst.WIDGET_CONSIGN_BID:
            self.bidMediator = mediator

    def isShow(self):
        return self.mediator != None

    def show(self, npcId = 0, layoutType = uiConst.LAYOUT_DEFAULT, searchItemName = '', seekId = 0):
        if not BigWorld.player().checkMapLimitUI(gametypes.MAP_LIMIT_UI_CONSIGN):
            return
        else:
            BigWorld.player().checkSetPassword()
            self.npcId = npcId
            if npcId == 0:
                openLv = SCD.data.get('openConsignLv', 20)
                if BigWorld.player().lv < openLv:
                    BigWorld.player().showGameMsg(GMDD.data.FORBIDDEN_OPEN_CONSIGN, ())
                    if seekId:
                        uiUtils.findPosWithAlert(seekId)
                    return
            self.searchItemName = searchItemName
            if not self.isShow():
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CONSIGN, layoutType=layoutType)
            elif self.mediator != None:
                self.mediator.Invoke('refreshConsign', GfxValue(gbk2unicode(self.searchItemName)))
            return

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        if self.mediator != None:
            self.mediator = None
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CONSIGN)
        self.consignSearchHistory.writeConfigData()
        self.pageItems = None
        self.npcId = 0
        self.bindingData = {}
        gameglobal.rds.ui.inventory.updateSlotState(self.pageSrc, self.posSrc)
        self.pageSrc = -1
        self.posSrc = -1
        self.average = 0
        self.searchItemName = ''
        self.fixedPrice = 0
        self.consignNum = 0
        self.priceSortBy = const.ITEM_CONSIGN_SORT_BY_FIXED_UNIT_PRICE
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()
        self.closeBuyPanel()
        self.closeBidPanel()

    def showBuyPanel(self):
        if self.buyMediator:
            self.buyMediator.Invoke('setBuyItemInfo', self.onGetBuyItemInfo())
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CONSIGN_BUY)

    def closeBuyPanel(self):
        self.buyMediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CONSIGN_BUY)

    def showBidPanel(self):
        if self.bidMediator:
            self.bidMediator.Invoke('refreshItemInfo', (self.onGetMinBidPrice(), self.onGetBuyItemInfo()))
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CONSIGN_BID)

    def closeBidPanel(self):
        self.bidMediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CONSIGN_BID)

    def getSlotID(self, key):
        idBar, idItem = key.split('.')
        return (int(idBar[7:]), int(idItem[4:]))

    def _getKey(self, bar, slot):
        return 'consign%d.slot%d' % (bar, slot)

    @ui.checkItemIsLock([4, 5])
    def setItem(self, bar, slot, item, pageSrc, posSrc):
        if self.curConsignType == uiConst.CONSIGN_TYPE_COMMON and item.isItemNoConsign():
            BigWorld.player().showGameMsg(GMDD.data.ITEM_NOCONSIGN, ())
            return
        elif self.curConsignType == uiConst.CONSIGN_TYPE_COIN and not item.isItemCoinConsign():
            BigWorld.player().showGameMsg(GMDD.data.ITEM_NO_COINCONSIGN, ())
            return
        else:
            key = self._getKey(bar, slot)
            if self.binding.has_key(key):
                self.bindingData[key] = item
                self.pageSrc = pageSrc
                self.posSrc = posSrc
                p = BigWorld.player()
                e = self._getEntity()
                if self.curConsignType == uiConst.CONSIGN_TYPE_COMMON:
                    self.curTabInfo = self.sellTabInfo
                elif self.curConsignType == uiConst.CONSIGN_TYPE_COIN:
                    self.curTabInfo = self.sellCoinTabInfo
                self.curTabInfo._commitSearchByName(e, [0, item.id])
                gameglobal.rds.ui.inventory.updateSlotState(pageSrc, posSrc)
                self.consignNum = item.cwrap
                data = uiUtils.getGfxItem(item)
                self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(data))
                self.average = 0
                self.fixedPrice = 0
                self.dealAverage = 0
                if self.mediator != None:
                    self.mediator.Invoke('setKeepType', GfxValue(0))
                    self.mediator.Invoke('setSellPanelTitle', GfxValue(1))
                    if p.consignPrices.has_key(item.id):
                        self.average = p.consignPrices[item.id]['price']
                        self.fixedPrice = p.consignPrices[item.id]['fixedPrice']
                    self.setStorageFee(0)
                    if self.curConsignType == uiConst.CONSIGN_TYPE_COMMON:
                        p.base.queryConsignItemPrice(item.id, gametypes.CONSIGN_QUERY_PRICE_FOR_CONSIGN_SELL)
                    elif self.curConsignType == uiConst.CONSIGN_TYPE_COIN:
                        p.base.queryCoinConsignItemPrice(item.id, gametypes.CONSIGN_QUERY_PRICE_FOR_CONSIGN_SELL)
            return

    def removeItem(self, bar, slot):
        key = self._getKey(bar, slot)
        if self.binding.has_key(key):
            self.bindingData[key] = None
            data = GfxValue(0)
            data.SetNull()
            self.binding[key][1].InvokeSelf(data)
            self.binding[key][0].Invoke('setSlotColor', GfxValue('nothing'))
            if self.mediator != None:
                self.mediator.Invoke('setItemPrice', uiUtils.array2GfxAarry([0,
                 '',
                 '',
                 '',
                 0]))
                self.mediator.Invoke('setBidBtnState', GfxValue(False))
                self.mediator.Invoke('setSellPanelTitle', GfxValue(0))
            gameglobal.rds.ui.inventory.updateSlotState(self.pageSrc, self.posSrc)
            self.pageSrc = -1
            self.posSrc = -1
            self.average = 0
            self.fixedPrice = 0
            self.consignNum = 0
            self.keepTime = 0
            self.setStorageFee(0)
            if self.curTabInfo in (self.mineCoinTabInfo,
             self.mineTabInfo,
             self.sellTabInfo,
             self.sellCoinTabInfo):
                if self.curConsignType == uiConst.CONSIGN_TYPE_COMMON:
                    self.curTabInfo = self.mineTabInfo
                elif self.curConsignType == uiConst.CONSIGN_TYPE_COIN:
                    self.curTabInfo = self.mineCoinTabInfo
                self.showTab()

    def setStorageFee(self, ctype):
        if self.curConsignType == uiConst.CONSIGN_TYPE_COMMON:
            key = self._getKey(1, 99)
            if self.bindingData.has_key(key) and self.bindingData[key]:
                val = formula.getConsignStorageFee(ctype, (self.fixedPrice or self.average) * self.consignNum)
            else:
                val = 0
        elif self.curConsignType == uiConst.CONSIGN_TYPE_COIN:
            val = CCCD.data.get('coinConsignStorageCash', 0)
        if self.mediator != None:
            self.mediator.Invoke('setSellPanelFee', GfxValue(val))

    def updateSortState(self, sortType = -1, orderType = -1):
        if sortType == -1:
            sortType = self.curTabInfo.searchSortType
        if orderType == -1:
            orderType = self.curTabInfo.searchOrderType
        self.setSortState(sortType / SORT_BY_PARAM, orderType)

    def setSortState(self, idx, state):
        if self.mediator != None:
            self.mediator.Invoke('setSortState', (GfxValue(idx), GfxValue(state)))

    def addConsignItem(self):
        if self.mediator != None:
            self.mediator.Invoke('addConsignItem')

    def setMinLv(self, val):
        if self.mediator != None:
            self.mediator.Invoke('setMinLv', GfxValue(str(val)))

    def setMaxLv(self, val):
        if self.mediator != None:
            self.mediator.Invoke('setMaxLv', GfxValue(str(val)))

    def updateCash(self):
        if self.mediator != None:
            p = BigWorld.player()
            cash = format(p.cash, ',')
            tianbi = format(p.unbindCoin + p.bindCoin + p.freeCoin, ',')
            unBindTianbi = uiUtils.toHtml(gameStrings.TEXT_ACTIVITYSALEDAILYGIFTPROXY_145 % format(p.unbindCoin, ','), '#79c725')
            tianbiStr = '%s%s' % (tianbi, unBindTianbi)
            if not cash:
                cash = 0
            if not tianbi:
                tianbi = 0
            ret = {'cash': cash,
             'tianbi': tianbiStr}
            self.mediator.Invoke('setCash', uiUtils.dict2GfxDict(ret, True))

    def onGetCategory(self, *arg):
        ret = []
        schoolData = []
        for key, item in SD.data.items():
            obj = {}
            obj['key'] = key
            obj['value'] = item.get('name', '')
            if not gameglobal.rds.configData.get('enableNewSchoolYeCha', False) and key == const.SCHOOL_YECHA:
                continue
            schoolData.append(obj)

        cate = {}
        cateNames = {}
        for key, value in ICD.data.items():
            if not value.get('showSubCategory', 0):
                continue
            if self.curConsignType == uiConst.CONSIGN_TYPE_COIN and not value.get('showInCoinConsign', 0):
                continue
            if self.curConsignType == uiConst.CONSIGN_TYPE_COMMON and value.get('noShowInCommonConsign', 0):
                continue
            subCategoryName = value.get('subCategoryName', '')
            needSchool = value.get('needSchool', 0)
            if not cate.has_key(key[0]):
                cate[key[0]] = []
            if needSchool:
                cate[key[0]].append([subCategoryName,
                 schoolData,
                 key,
                 True])
            elif len(value.get('dcategories', [])) > 0:
                dcategories = value.get('dcategories', [])
                dcategoriesName = value.get('dcategoriesName', [])
                thirdCate = []
                for idx in xrange(len(dcategories)):
                    tCateObj = {}
                    tCateObj['key'] = dcategories[idx]
                    tCateObj['value'] = dcategoriesName[idx]
                    thirdCate.append(tCateObj)

                cate[key[0]].append([subCategoryName,
                 thirdCate,
                 key,
                 False])
            else:
                cate[key[0]].append([subCategoryName,
                 [],
                 key,
                 False])
            cate[key[0]].sort(key=lambda k: k[2][1])
            cateNames[key[0]] = value.get('categoryName', '')

        catekeys = cate.keys()
        for key in catekeys:
            value = cate.get(key)
            ret.append([cateNames[key], value, key])

        return uiUtils.array2GfxAarry(ret, True)

    def onSelectCategory(self, *arg):
        pass

    def onGetQualityTypes(self, *arg):
        ret = [{'label': gameStrings.TEXT_CONSIGNPROXY_453},
         {'label': gameStrings.TEXT_CONSIGNPROXY_453_1},
         {'label': gameStrings.TEXT_CONSIGNPROXY_453_2},
         {'label': gameStrings.TEXT_CONSIGNPROXY_453_3},
         {'label': gameStrings.TEXT_CONSIGNPROXY_453_4},
         {'label': gameStrings.TEXT_CONSIGNPROXY_453_5},
         {'label': gameStrings.TEXT_CONSIGNPROXY_453_6},
         {'label': gameStrings.TEXT_CONSIGNPROXY_453_7}]
        return uiUtils.array2GfxAarry(ret, True)

    @ui.callInCD(1)
    def onSearchItems(self, *arg):
        name = arg[3][0].GetString().strip()
        if name:
            name = unicode2gbk(name)
        cate = arg[3][6].GetString().strip().split(',')
        self.searchItemsByName(name, cate, *arg)

    @ui.callInCD(1)
    def onAutoSearchByChangeTab(self, *arg):
        name = arg[3][0].GetString().strip()
        if name:
            name = unicode2gbk(name)
        cate = arg[3][6].GetString().strip().split(',')
        if name == '' and cate == ['']:
            return
        self.searchItemsByName(name, cate, *arg)

    def searchItemsByName(self, name, cate = [''], *arg):
        p = BigWorld.player()
        e = self._getEntity()
        if not e:
            return
        isSchool = arg[3][7].GetBool() if arg else 0
        category = -1
        subcategory = -1
        school = -1
        dtype = -1
        if cate[0]:
            category = int(cate[0])
            if len(cate) > 1:
                subcategory = int(cate[1])
            if len(cate) > 2:
                if isSchool:
                    school = int(cate[2])
                else:
                    dtype = int(cate[2])
        if name:
            self.consignSearchHistory.addSearchHistoryData(name)
            forme = arg[3][1].GetBool() if arg else 0
            minLv = arg[3][2].GetString().strip() if arg else 0
            maxLv = arg[3][3].GetString().strip() if arg else 0
            quality = arg[3][4].GetString().strip() if arg else 0
            if forme or minLv or maxLv or int(quality):
                p.showGameMsg(GMDD.data.CONSIGN_SEARCH_ITEM_WRONG_OPTIONS, ())
                return
            if self.curConsignType == uiConst.CONSIGN_TYPE_COMMON:
                if not self.buyTabInfo.searchByName(e, name, school=school, mType=category, sType=subcategory):
                    self.buyTabInfo.clearCache()
                    self.showTab()
            elif self.curConsignType == uiConst.CONSIGN_TYPE_COIN:
                if not self.buyCoinTabInfo.searchByName(e, name, school=school, mType=category, sType=subcategory):
                    self.buyCoinTabInfo.clearCache()
                    self.showTab()
        else:
            forme = arg[3][1].GetBool() if arg else 0
            minLv = arg[3][2].GetString().strip() if arg else 0
            if not minLv:
                minLv = -1
            else:
                minLv = int(minLv)
            maxLv = arg[3][3].GetString().strip() if arg else 0
            if not maxLv:
                maxLv = -1
            else:
                maxLv = int(maxLv)
            if minLv > const.MAX_LEVEL:
                minLv = const.MAX_LEVEL
                self.setMinLv(minLv)
            if maxLv > const.MAX_LEVEL:
                maxLv = const.MAX_LEVEL
                self.setMaxLv(maxLv)
            if minLv != -1 and maxLv != -1 and minLv > maxLv:
                minLv, maxLv = maxLv, minLv
            quality = arg[3][4].GetString().strip() if arg else 0
            if not quality:
                quality = -1
            else:
                quality = int(quality)
            if category == -1:
                p.showGameMsg(GMDD.data.CONSIGN_SEARCH_ITEM_TYPE_REQUIRED, ())
                self.buyTabInfo.clearCache()
                self.buyCoinTabInfo.clearCache()
                return
            if self.curConsignType == uiConst.CONSIGN_TYPE_COMMON:
                self.buyTabInfo.searchByType(e, category, subcategory, dtype, quality, minLv, maxLv, school, forme)
            elif self.curConsignType == uiConst.CONSIGN_TYPE_COIN:
                self.buyCoinTabInfo.searchByType(e, category, subcategory, dtype, quality, minLv, maxLv, school, forme)

    def onGetSearchHistory(self, *arg):
        return uiUtils.array2GfxAarry(self.consignSearchHistory.getReverseHistoryList(), True)

    def onGetHistoryCfg(self, *arg):
        ret = gameStrings.TEXT_CONSIGNPROXY_556
        return GfxValue(gbk2unicode(ret))

    def _formatLeftTime(self, endT, beginT, now):
        delta = endT - max(now, beginT)
        if delta <= 0:
            return gameStrings.TEXT_CONSIGNPROXY_562
        if self.curConsignType == uiConst.CONSIGN_TYPE_COIN:
            coinConsignDuration = CCCD.data.get('coinConsignPublicityTime', 60)
            if now - beginT < coinConsignDuration:
                delta = coinConsignDuration + beginT - now
                return uiUtils.toHtml(gameStrings.TEXT_CONSIGNPROXY_568 % self._getTimeStr(delta), '#f43804')
            else:
                return self._getTimeStr(delta)
        elif self.curConsignType == uiConst.CONSIGN_TYPE_COMMON:
            return self._getTimeStr(delta)

    def _getTimeStr(self, delta):
        if delta >= 3600:
            return gameStrings.TEXT_CONSIGNPROXY_577 % formula.ceilIntDivide(delta, 3600)
        else:
            delta = delta % 3600
            return gameStrings.TEXT_CONSIGNPROXY_580 % formula.ceilIntDivide(delta, 60)

    def setSearchResult(self, items):
        info = []
        now = utils.getNow()
        p = BigWorld.player()
        if self.mediator != None:
            if self.curTabInfo == self.historyTabInfo:
                for item in items:
                    gfxItem = {'opTime': time.strftime('%Y-%m-%d %H:%M', time.localtime(item[0])),
                     'type': uiUtils.toHtml(gameStrings.TEXT_CONSIGNPROXY_592, '#FFBF66') if item[1] == p.gbId else uiUtils.toHtml(gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_990, '#aa7acc'),
                     'price': item[5],
                     'cnt': item[6],
                     'totalPrice': item[5] * item[6],
                     'itemName': '<u>%s</u>' % uiUtils.getItemColorNameByItem(item[3]),
                     'uuid': str(item[3].uuid.encode('hex')),
                     'location': const.ITEM_IN_CONSIGN_HISTORY,
                     'incomeTime': item[0] + CCCD.data.get('coinConsignIncomeFreezeTime')}
                    info.append(gfxItem)

            else:
                for itemData in items:
                    dbID, item = itemData
                    if hasattr(item, 'quality'):
                        quality = item.quality
                    else:
                        quality = ID.data.get(item.id, {}).get('quality', 1)
                    qualitycolor = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
                    info.append([uiUtils.getItemIconFile64(item.id),
                     item.cwrap,
                     qualitycolor,
                     uiUtils.getItemColorNameByItem(item, True, 8),
                     item.lvReq,
                     self._formatLeftTime(item._consignEndT, item._consignBeginT, now),
                     item._consignVendor if hasattr(item, '_consignVendor') else '',
                     item._consignPrice,
                     item._consignFixedPrice if hasattr(item, '_consignFixedPrice') else item._consignPrice * item.cwrap,
                     item._consignBid if hasattr(item, '_consignBid') else 0,
                     str(dbID),
                     item._consignVendor == BigWorld.player().roleName if hasattr(item, '_consignVendor') else False,
                     item._consignBidderRole if hasattr(item, '_consignBidderRole') else '' or '',
                     (item._consignBidderRole if hasattr(item, '_consignBidderRole') else '') == BigWorld.player().roleName,
                     item.canUseNow(p.physique.sex, p.physique.school, p.physique.bodyType, p.lv, p),
                     uiUtils.getPinXing(item.id),
                     itemToolTipUtils.getCornerMark(item)])

            self.mediator.Invoke('setDetailCanvas', (uiUtils.array2GfxAarry(info, True), GfxValue(self.curTabInfo.curPage + 1), GfxValue(self.curTabInfo.totalPages)))

    def onSellItem(self, *arg):
        if self.curConsignType == uiConst.CONSIGN_TYPE_COMMON:
            self.sellCommonItem(*arg)
        elif self.curConsignType == uiConst.CONSIGN_TYPE_COIN:
            self.sellCoinItem(*arg)

    def sellCoinItem(self, *arg):
        num = arg[3][1].GetString().strip()
        bidPrice = arg[3][2].GetString().strip()
        if not bidPrice:
            BigWorld.player().showGameMsg(GMDD.data.CONSIGN_NO_COIN_PRICE, ())
            return
        if bidPrice and not long(bidPrice):
            BigWorld.player().showGameMsg(GMDD.data.CONSIGN_NO_COIN_PRICE, ())
            return
        if not num or re.match('^0+$', num):
            BigWorld.player().showGameMsg(GMDD.data.CONSIGN_NO_ITEM_COUNT, ())
            return
        self._onSellItem(int(num), long(bidPrice), 0, 0)

    def sellCommonItem(self, *arg):
        num = arg[3][1].GetString().strip()
        p = BigWorld.player()
        if not num or re.match('^0+$', num):
            p.showGameMsg(GMDD.data.CONSIGN_NO_MANY, ())
            return
        if not num.isdigit():
            p.showGameMsg(GMDD.data.CONSIGN_NO_MANY, ())
            return
        num = int(num)
        bidPrice = arg[3][2].GetString().strip()
        fixedPrice = arg[3][3].GetString().strip()
        isSinglePrice = arg[3][5].GetBool()
        if bidPrice:
            bidPrice = int(bidPrice)
        if fixedPrice:
            fixedPrice = int(fixedPrice)
        else:
            fixedPrice = 0
        if isSinglePrice:
            bidPrice *= num
            fixedPrice *= num
        if not bidPrice:
            p.showGameMsg(GMDD.data.CONSIGN_NO_BID_NOR_FIXED_PRICE, ())
            return
        if not bidPrice and not fixedPrice:
            p.showGameMsg(GMDD.data.CONSIGN_NO_BID_NOR_FIXED_PRICE, ())
            return
        if fixedPrice and fixedPrice < bidPrice:
            p.showGameMsg(GMDD.data.CONSIGN_BID_EXCEED_FIXED_PRICE, ())
            return
        it = p.inv.getQuickVal(self.pageSrc, self.posSrc)
        if not it or not it.canSplit(num):
            p.showGameMsg(GMDD.data.ITEM_NO_ENOUGH, (it.name if it else '',))
            return
        if fixedPrice > PRICE_MAX:
            p.showGameMsg(GMDD.data.CONSIGN_PRICE_TOO_MUCH, ())
            return
        if fixedPrice and self.dealAverage and gameglobal.rds.configData.get('enableConsignMaxFixedPrice'):
            if ICD.data.get((it.category, it.subcategory), {}).get('checkConsignMax'):
                maxFixedPrice = commcalc.getConsignMaxFixedPrice(num, self.dealAverage)
                if fixedPrice > maxFixedPrice:
                    p.showGameMsg(GMDD.data.CONSIGN_MAX_FIXED_PRICE, ())
                    return
        durationType = int(arg[3][4].GetNumber())
        if durationType > len(const.ITEM_CONSIGN_DURATION):
            durationType = durationType / 24 - 1
        e = self._getEntity()
        if e and self.pageSrc != -1:
            self.checkLowPrice(it, bidPrice / num, self._onSellItem, (num,
             bidPrice,
             fixedPrice,
             durationType))

    @ui.checkInventoryLock()
    def _onSellItem(self, num, bidPrice, fixedPrice, durationType):
        e = self._getEntity()
        if e and self.pageSrc != -1:
            if self.curConsignType == uiConst.CONSIGN_TYPE_COMMON:
                e.cell.consignItem(self.pageSrc, self.posSrc, num, bidPrice, fixedPrice, durationType, BigWorld.player().cipherOfPerson)
            elif self.curConsignType == uiConst.CONSIGN_TYPE_COIN:
                e.cell.coinConsignItem(self.pageSrc, self.posSrc, num, bidPrice, 0, BigWorld.player().cipherOfPerson)

    def onSellItemSuccess(self):
        self.removeItem(1, 99)
        if self.curConsignType == uiConst.CONSIGN_TYPE_COMMON:
            self.mineTabInfo.searchSortBy(self.priceSortBy, 0)
        elif self.curConsignType == uiConst.CONSIGN_TYPE_COIN:
            self.mineCoinTabInfo.searchSortBy(self.priceSortBy, 0)
        if self.mediator != None:
            self.mediator.Invoke('clearSellInput')

    def onGetItemMaxNum(self, *arg):
        key = arg[3][0].GetString()
        ret = 0
        if self.bindingData.has_key(key):
            item = self.bindingData[key]
            ret = item.cwrap if item and hasattr(item, 'cwrap') else ''
            if self.mediator != None:
                self.mediator.Invoke('setSellPanelNum', GfxValue(ret))
            if item:
                self._updatePrice(item.id, ret, item.cwrap)

    def onCancelSellItem(self, *arg):
        dbID = int(arg[3][0].GetString())
        e = self._getEntity()
        if e:
            if self.curConsignType == uiConst.CONSIGN_TYPE_COMMON:
                item = self.mineTabInfo.getItemInCurrentPage(dbID)
                e.cell.cancelConsignItem(dbID, item.id, item.cwrap)
            elif self.curConsignType == uiConst.CONSIGN_TYPE_COIN:
                item = self.mineCoinTabInfo.getItemInCurrentPage(dbID)
                BigWorld.player().cell.cancelCoinConsignItem(dbID, item.id, item.cwrap)

    def onBidItem(self, *arg):
        dbId = int(arg[3][0].GetString())
        self.curDbId = dbId
        self.showBidPanel()

    def onBuyItem(self, *arg):
        dbId = int(arg[3][0].GetString())
        self.curDbId = dbId
        item = self.curTabInfo.getItemInCurrentPage(self.curDbId)
        if item:
            if self.curConsignType == uiConst.CONSIGN_TYPE_COMMON:
                BigWorld.player().base.queryConsignItemPrice(item.id, gametypes.CONSIGN_QUERY_PRICE_FOR_CONSING_BUY)
            elif self.curConsignType == uiConst.CONSIGN_TYPE_COIN:
                BigWorld.player().base.queryCoinConsignItemPrice(item.id, gametypes.CONSIGN_QUERY_PRICE_FOR_CONSIGN_SELL)
        self.showBuyPanel()

    def onFitting(self, *arg):
        dbId = int(arg[3][0].GetString())
        if self.curConsignType == uiConst.CONSIGN_TYPE_COMMON:
            it = self.buyTabInfo.getItemInCurrentPage(dbId)
        elif self.curConsignType == uiConst.CONSIGN_TYPE_COIN:
            it = self.buyCoinTabInfo.getItemInCurrentPage(dbId)
        if it:
            gameglobal.rds.ui.fittingRoom.addItem(it)

    def onGetSellRecord(self, *arg):
        pass

    def onSortItems(self, *arg):
        idx = int(arg[3][0].GetNumber())
        sortId = idx * SORT_BY_PARAM
        if sortId == const.ITEM_CONSIGN_SORT_BY_PRICE:
            sortId = self.priceSortBy
        self.curTabInfo.searchSortBy(sortId)

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        bar, slot = self.getSlotID(key)
        if self.bindingData.has_key(key):
            return gameglobal.rds.ui.inventory.GfxToolTip(self.bindingData[key])
        if bar == 0:
            item = self.curTabInfo.getItemInCurrentPage(slot)
            if item:
                return gameglobal.rds.ui.inventory.GfxToolTip(item)
            else:
                return GfxValue('')
        else:
            return GfxValue('')

    def onClosePanel(self, *arg):
        self.hide()

    def onGetCash(self, *arg):
        p = BigWorld.player()
        cash = format(p.cash, ',')
        tianbi = format(p.unbindCoin + p.bindCoin + p.freeCoin, ',')
        unBindTianbi = uiUtils.toHtml(gameStrings.TEXT_ACTIVITYSALEDAILYGIFTPROXY_145 % format(p.unbindCoin, ','), '#79c725')
        tianbiStr = '%s%s' % (tianbi, unBindTianbi)
        if not cash:
            cash = 0
        if not tianbi:
            tianbi = 0
        ret = {'cash': cash,
         'tianbi': tianbiStr}
        return uiUtils.dict2GfxDict(ret, True)

    def onChangeKeepTime(self, *arg):
        self.keepTime = int(arg[3][0].GetNumber())
        self.setStorageFee(self.keepTime)

    def checkItemCondition(self, item):
        if self.curConsignType == uiConst.CONSIGN_TYPE_COMMON and item:
            return not item.isItemNoConsign()
        if self.curConsignType == uiConst.CONSIGN_TYPE_COIN and item:
            return item.isItemCoinConsign()
        return False

    def onChangeTab(self, *arg):
        tabIdx = int(arg[3][0].GetNumber())
        self.curDbId = 0
        self.tab = tabIdx
        if tabIdx == BUY_PANEL:
            if self.curConsignType == uiConst.CONSIGN_TYPE_COMMON:
                self.curTabInfo = self.buyTabInfo
            elif self.curConsignType == uiConst.CONSIGN_TYPE_COIN:
                self.curTabInfo = self.buyCoinTabInfo
        elif tabIdx == SELL_PANEL:
            if self.pageSrc != -1:
                if self.curConsignType == uiConst.CONSIGN_TYPE_COMMON:
                    self.curTabInfo = self.sellTabInfo
                elif self.curConsignType == uiConst.CONSIGN_TYPE_COIN:
                    self.curTabInfo = self.sellCoinTabInfo
            elif self.curConsignType == uiConst.CONSIGN_TYPE_COMMON:
                self.curTabInfo = self.mineTabInfo
            elif self.curConsignType == uiConst.CONSIGN_TYPE_COIN:
                self.curTabInfo = self.mineCoinTabInfo
            self.setStorageFee(0)
            key = self._getKey(1, 99)
            if self.binding.has_key(key) and self.bindingData.has_key(key) and self.bindingData[key]:
                if not self.checkItemCondition(self.bindingData[key]):
                    self.removeItem(1, 99)
        elif tabIdx == MINE_BID_PANEL:
            self.curTabInfo = self.myBidTabInfo
            if not self.bidTabInfoInited:
                self.bidTabInfoInited = True
            BigWorld.player().base.fetchMyConsignBidItems()
        elif tabIdx == TRADE_HISTORY_PANEL:
            self.curTabInfo = self.historyTabInfo
            self._queryTradeHistory()
        self.updateSortState()
        self.showTab()

    @ui.callFilter(3, False)
    def _queryTradeHistory(self):
        BigWorld.player().base.queryCoinConsignTradeHistory()

    def onCloseBuyPanel(self, *arg):
        self.closeBuyPanel()

    def onConfirmBuy(self, *arg):
        num = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        if num == 0:
            p.showTopMsg(gameStrings.TEXT_CONSIGNPROXY_890)
            return
        e = self._getEntity()
        if e:
            item = self.curTabInfo.getItemInCurrentPage(self.curDbId)
            if item:
                many = num != item.cwrap and num or 0
                if self.curConsignType == uiConst.CONSIGN_TYPE_COMMON:
                    price = 0
                    if many > 0:
                        if many > item.cwrap:
                            p.showGameMsg(GMDD.data.ITEM_NO_ENOUGH, (item.name,))
                            return
                        price = int(math.ceil(item._consignFixedPrice * 1.0 * many / item.cwrap))
                    else:
                        price = item._consignFixedPrice
                    self.checkOverPrice(item, price * 1.0 / item.cwrap, self._onConfirmBuy, (item, price, many))
                elif self.curConsignType == uiConst.CONSIGN_TYPE_COIN:
                    price = item._consignPrice
                    self._onConfirmBuy(item, price, many)

    @ui.checkInventoryLock()
    def _onConfirmBuy(self, item, price, many):
        if self.curConsignType == uiConst.CONSIGN_TYPE_COIN:
            BigWorld.player().cell.buyCoinConsignItem(item.id, self.curDbId, many or item.cwrap, BigWorld.player().cipherOfPerson)
        elif self.curConsignType == uiConst.CONSIGN_TYPE_COMMON:
            e = self._getEntity()
            if not e:
                return
            e.cell.buyConsignItem(item.id, self.curDbId, price, False, many or item.cwrap, BigWorld.player().cipherOfPerson)
        self.closeBuyPanel()

    def onGetBuyItemInfo(self, *arg):
        item = self.curTabInfo.getItemInCurrentPage(self.curDbId)
        ret = {}
        if self.curConsignType == uiConst.CONSIGN_TYPE_COMMON:
            ret['title'] = gameStrings.TEXT_CONSIGNPROXY_929
        elif self.curConsignType == uiConst.CONSIGN_TYPE_COIN:
            ret['title'] = gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_990
        if self.curConsignType == uiConst.CONSIGN_TYPE_COMMON:
            ret['priceText'] = gameStrings.TEXT_CONSIGNPROXY_934
        elif self.curConsignType == uiConst.CONSIGN_TYPE_COIN:
            ret['priceText'] = gameStrings.TEXT_CONSIGNPROXY_936
        if self.curConsignType == uiConst.CONSIGN_TYPE_COMMON:
            ret['bonusType'] = 'cash'
        elif self.curConsignType == uiConst.CONSIGN_TYPE_COIN:
            ret['bonusType'] = 'tianBi'
        if item:
            ret['item'] = uiUtils.getGfxItem(item)
            ret['item']['name'] = uiUtils.getItemColorNameByItem(item)
            if self.curConsignType == uiConst.CONSIGN_TYPE_COMMON:
                ret['item']['_consignFixedPrice'] = item._consignFixedPrice
            elif self.curConsignType == uiConst.CONSIGN_TYPE_COIN:
                ret['item']['_consignFixedPrice'] = item._consignPrice * item.cwrap
            if hasattr(item, '_consignBid'):
                ret['item']['_consignBid'] = item._consignBid
            else:
                ret['item']['_consignBid'] = 0
        ret['playerCash'] = BigWorld.player().cash
        ret['playerCoin'] = BigWorld.player().unbindCoin
        ret['consignType'] = self.curConsignType
        return uiUtils.dict2GfxDict(ret, True)

    def onCloseBidPanel(self, *arg):
        self.closeBidPanel()

    def onConfirmBid(self, *arg):
        p = BigWorld.player()
        price = int(arg[3][0].GetString())
        if price == 0:
            p.showTopMsg(gameStrings.TEXT_CONSIGNPROXY_970)
            return
        e = self._getEntity()
        if e:
            item = self.curTabInfo.getItemInCurrentPage(self.curDbId)
            if item:
                if item._consignFixedPrice and price >= item._consignFixedPrice:
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_CONSIGNPROXY_977, Functor(self._confirmBid, e, item, self.curDbId, item._consignFixedPrice, False, item.cwrap))
                else:
                    self._confirmBid(e, item, self.curDbId, price, True, 0)

    @ui.checkInventoryLock()
    def _confirmBid(self, entity, item, DbId, price, bid, many):
        entity.cell.buyConsignItem(item.id, DbId, price, bid, many, BigWorld.player().cipherOfPerson)
        self.closeBidPanel()

    def showOthers(self, tab = None):
        if not tab or tab == self.curTabInfo:
            self.setCancelBtnVisible(self.curTabInfo == self.mineTabInfo or self.curTabInfo == self.mineCoinTabInfo)
            items = self.curTabInfo.getCurrentPageItems()
            self.setSearchResult(items)

    def showMine(self):
        if self.curTabInfo == self.mineTabInfo or self.curTabInfo == self.myBidTabInfo or self.curTabInfo == self.mineCoinTabInfo:
            self.setCancelBtnVisible(True)
            items = self.curTabInfo.getCurrentPageItems()
            self.setSearchResult(items)

    def showTab(self, tab = None):
        if not tab or tab == self.curTabInfo:
            self.setCancelBtnVisible(self.curTabInfo == self.mineTabInfo or self.curTabInfo == self.mineCoinTabInfo)
            if self.priceSortBy != self.curTabInfo.searchSortType:
                self.curTabInfo.searchSortBy(self.priceSortBy, self.curTabInfo.searchOrderType)
            else:
                items = self.curTabInfo.getCurrentPageItems()
                self.setSearchResult(items)

    def showTradeHistory(self):
        if self.curTabInfo == self.historyTabInfo:
            items = self.curTabInfo.getCurrentPageItems()
            self.setSearchResult(items)

    def _getEntity(self):
        e = None
        if self.npcId:
            e = BigWorld.entities.get(self.npcId)
        else:
            e = BigWorld.player()
        return e

    def onPrevPage(self, *arg):
        self.curTabInfo.showPrevPage()

    def onNextPage(self, *arg):
        self.curTabInfo.showNextPage()

    def onFirstPage(self, *arg):
        self.curTabInfo.gotoPage(0)

    def onLastPage(self, *arg):
        self.curTabInfo.gotoPage(self.curTabInfo.totalPages - 1)

    def onRefreshContent(self, *arg):
        self.buyTabInfo.clearCache()
        self.buyCoinTabInfo.clearCache()

    def onGetMinBidPrice(self, *arg):
        val = 0
        fixedVal = 0
        item = self.curTabInfo.getItemInCurrentPage(self.curDbId)
        if item:
            val = item._consignBid and formula.getMinBidPrice(item._consignPrice) or item._consignPrice
            fixedVal = item._consignFixedPrice
        ret = [val, fixedVal]
        return uiUtils.array2GfxAarry(ret)

    def onChangeSortType(self, *arg):
        args = arg[3][0].GetString().split(',')
        bidType = int(args[0])
        priceType = int(args[1])
        priceSortBy = const.ITEM_CONSIGN_SORT_BY_PRICE + priceType * 2 + bidType
        if priceSortBy != self.priceSortBy:
            self.priceSortBy = priceSortBy
            self.curTabInfo.searchSortBy(priceSortBy, self.curTabInfo.searchOrderType)

    def onGotoPage(self, *arg):
        page = arg[3][0].GetString()
        page = int(page) if page else 0
        self.curTabInfo.gotoPage(page - 1)

    def onUpdatePrice(self, itemId, price):
        if self.mediator and self.pageSrc != -1:
            p = BigWorld.player()
            it = p.inv.getQuickVal(self.pageSrc, self.posSrc)
            self.dealAverage = price
            if not self.average:
                self.average = price * 0.8
                self.fixedPrice = price
            if it and it.id == itemId:
                self.mediator.Invoke('setItemPrice', uiUtils.array2GfxAarry([int(self.dealAverage),
                 it.cwrap,
                 int(self.average),
                 int(self.fixedPrice),
                 it.cwrap]))
            self.setStorageFee(self.keepTime)

    def getConsignment(self, stamp):
        if self.buyTabInfo.ownStamp(stamp):
            return self.buyTabInfo
        elif self.buyCoinTabInfo.ownStamp(stamp):
            return self.buyCoinTabInfo
        elif self.sellTabInfo.ownStamp(stamp):
            return self.sellTabInfo
        elif self.sellCoinTabInfo.ownStamp(stamp):
            return self.sellCoinTabInfo
        else:
            gamelog.warning('getConsignment no matched consignment for stamp', stamp)
            return None

    def onRemoveItem(self, *arg):
        key = arg[3][0].GetString()
        bar, slot = self.getSlotID(key)
        self.removeItem(bar, slot)

    def onNumChange(self, *arg):
        num = int(arg[3][0].GetNumber())
        it = BigWorld.player().inv.getQuickVal(self.pageSrc, self.posSrc)
        curItem = self.bindingData.get('consign1.slot99', None)
        self.consignNum = num
        if it and curItem and it.id == curItem.id:
            self._updatePrice(it.id, num, it.cwrap)
        self.setStorageFee(self.keepTime)

    def onPriceChange(self, *arg):
        price = int(arg[3][0].GetNumber())
        self.average = price
        self.setStorageFee(self.keepTime)

    def onFixedPriceChange(self, *arg):
        fixedPrice = int(arg[3][0].GetNumber())
        self.fixedPrice = fixedPrice
        self.setStorageFee(self.keepTime)

    def onGetItemNames(self, *arg):
        name = unicode2gbk(arg[3][0].GetString().strip())
        ret = []
        if name == '':
            return uiUtils.array2GfxAarry(ret, True)
        name = name.lower()
        isPinyinAndHanzi = utils.isPinyinAndHanzi(name)
        if isPinyinAndHanzi == const.STR_HANZI_PINYIN:
            return uiUtils.array2GfxAarry(ret, True)
        pinyin = pinyinConvert.strPinyinFirst(name)
        if self.curConsignType == uiConst.CONSIGN_TYPE_COMMON:
            names = IND.data.get(uiConst.ITEM_NAME_CONSIGN, {}).get(pinyin[0], [])
        else:
            names = IND.data.get(uiConst.ITEM_NAME_COIN_CONSIGN, {}).get(pinyin[0], [])
        if len(name) == 1:
            namesCp = list(copy.deepcopy(names))
            historyList = self.consignSearchHistory.getHistoryList()
            for history in historyList:
                if history in namesCp:
                    namesCp.remove(history)
                    namesCp.insert(0, history)

            return uiUtils.array2GfxAarry(namesCp, True)
        if isPinyinAndHanzi == const.STR_ONLY_PINYIN:
            ret = [ x for x in names if name in str(pinyinConvert.strPinyinFirst(x)) ]
        else:
            ret = [ x for x in names if name in str(x) ]
        historyList = self.consignSearchHistory.getHistoryList()
        for history in historyList:
            if history in ret:
                ret.remove(history)
                ret.insert(0, history)

        return uiUtils.array2GfxAarry(ret, True)

    def setCancelBtnVisible(self, visible):
        if self.mediator != None:
            self.mediator.Invoke('setCancelBtnVisible', GfxValue(visible))

    def _updatePrice(self, itemId, count, maxCnt):
        self.mediator.Invoke('setItemPrice', uiUtils.array2GfxAarry([int(self.dealAverage),
         count,
         int(self.average),
         int(self.fixedPrice),
         int(maxCnt)]))

    def onGetTax(self, *arg):
        if self.curConsignType == uiConst.CONSIGN_TYPE_COMMON:
            tax = SCD.data.get('consignTaxRate', 0)
        elif self.curConsignType == uiConst.CONSIGN_TYPE_COIN:
            tax = CCCD.data.get('coinConsignTaxRatio', 0)
        return GfxValue(tax)

    def checkOverPrice(self, item, price, callback, params, noCallback = None, noParams = ()):
        rate = SCD.data.get('consignOverPriceRate', const.ITEM_CONSIGN_OVER_PRICE_RATE)
        basePrice = self.prices.get(item.id, 0)
        if basePrice and price >= basePrice * 1.0 * rate:
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_CONSIGNPROXY_1169 % item.name, yesCallback=lambda : callback(*params), noCallback=lambda : noCallback and noCallback(*noParams))
        else:
            callback(*params)

    def checkLowPrice(self, item, price, callback, params, noCallback = None, noParams = (), opName = gameStrings.TEXT_CONSIGNPROXY_1173):
        rate = SCD.data.get('consignLowPriceRate', const.ITEM_CONSIGN_LOW_PRICE_RATE)
        basePrice = self.prices.get(item.id, 0)
        if basePrice and price <= basePrice * 1.0 * rate:
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_CONSIGNPROXY_1177 % (item.name, opName), yesCallback=lambda : callback(*params), noCallback=lambda : noCallback and noCallback(*noParams))
        else:
            callback(*params)

    def isItemDisabled(self, kind, page, pos, item):
        if self.mediator and kind == const.RES_KIND_INV:
            key = self._getKey(1, 99)
            if page == self.pageSrc and pos == self.posSrc:
                return self.bindingData.get(key, None)

    def onSetConsignType(self, *arg):
        self.curConsignType = int(arg[3][0].GetNumber())
        if self.curTabInfo == self.historyTabInfo:
            return
        if self.curConsignType == uiConst.CONSIGN_TYPE_COMMON:
            self.priceSortBy = const.ITEM_CONSIGN_SORT_BY_FIXED_UNIT_PRICE
            if self.curTabInfo == self.buyCoinTabInfo:
                self.curTabInfo = self.buyTabInfo
        elif self.curConsignType == uiConst.CONSIGN_TYPE_COIN:
            self.priceSortBy = const.ITEM_CONSIGN_SORT_BY_UNIT_COIN
            if self.curTabInfo == self.buyTabInfo:
                self.curTabInfo = self.buyCoinTabInfo
        if self.curTabInfo != self.buyTabInfo and self.curTabInfo != self.buyCoinTabInfo:
            self.removeItem(1, 99)
            if self.curConsignType == uiConst.CONSIGN_TYPE_COMMON:
                self.curTabInfo = self.mineTabInfo
            elif self.curConsignType == uiConst.CONSIGN_TYPE_COIN:
                self.curTabInfo = self.mineCoinTabInfo
            self.setStorageFee(0)
        self.showTab()

    @ui.uiEvent(uiConst.WIDGET_CONSIGN, events.EVENT_TIANBI_COIN_CHANGED)
    def onCoinChanged(self, event):
        self.updateCash()

    def enableCoinConsign(self):
        enable = gameglobal.rds.configData.get('enableCoinConsign', False)
        if self.mediator:
            self.mediator.Invoke('updateCoinConsignEnable', GfxValue(enable))

    def onGetCoinConsignEnable(self, *arg):
        enable = gameglobal.rds.configData.get('enableCoinConsign', False)
        return GfxValue(enable)

    def onGetCoinConsignLimit(self, *arg):
        p = BigWorld.player()
        playerLv = p.realLv
        coinConsignLimit = CCCD.data.get('coinConsignLimit', {})
        coinConsignLimit = sorted(coinConsignLimit.items(), reverse=True)
        for data in coinConsignLimit:
            if playerLv >= data[0]:
                return GfxValue(gbk2unicode(uiUtils.getTextFromGMD(GMDD.data.COIN_CONSIGN_LIMIT, gameStrings.TEXT_CONSIGNPROXY_1235) % data[1]))

        return GfxValue(gbk2unicode(uiUtils.getTextFromGMD(GMDD.data.COIN_CONSIGN_LIMIT, gameStrings.TEXT_CONSIGNPROXY_1235) % 0))

    def onOpenCoinExchange(self, *arg):
        pass

    def shortKeyDown(self, key):
        if self.buyMediator:
            if key == keys.KEY_Y:
                self.buyMediator.Invoke('handleConfirm')
            else:
                self.closeBuyPanel()
        if self.bidMediator:
            if key == keys.KEY_Y:
                self.bidMediator.Invoke('handleConfirm')
            else:
                self.closeBidPanel()

    @ui.uiEvent(uiConst.WIDGET_CONSIGN, events.EVENT_INVENTORY_ITEM_CLICKED)
    def onInventoryRightClick(self, event):
        event.stop()
        i = event.data['item']
        nPage = event.data['page']
        nItem = event.data['pos']
        if i == None:
            return
        else:
            self.setInventoryItem(nPage, nItem, 1, 99)
            return

    def setInventoryItem(self, nPageSrc, nItemSrc, nPageDes, nItemDes):
        p = BigWorld.player()
        i = p.inv.getQuickVal(nPageSrc, nItemSrc)
        if i.isRuneHasRuneData():
            p.showGameMsg(GMDD.data.ITEM_CONSIGN_RUNE_EQUIP, ())
            return
        if i.isForeverBind():
            p.showGameMsg(GMDD.data.CONSIGN_ITEM_BIND, (i.name,))
            return
        if self.curConsignType == uiConst.CONSIGN_TYPE_COMMON and i.isItemNoConsign():
            BigWorld.player().showGameMsg(GMDD.data.ITEM_NOCONSIGN, ())
            return
        if self.curConsignType == uiConst.CONSIGN_TYPE_COIN and not i.isItemCoinConsign():
            BigWorld.player().showGameMsg(GMDD.data.ITEM_NO_COINCONSIGN, ())
            return
        self.addConsignItem()
        gameglobal.rds.ui.consign.setItem(nPageDes, nItemDes, i, nPageSrc, nItemSrc)

    def onGetMaxCount(self, *arg):
        p = BigWorld.player()
        count = 1
        item = self.curTabInfo.getItemInCurrentPage(self.curDbId)
        if item == None or item.cwrap == 0:
            return 1
        else:
            if self.curConsignType == uiConst.CONSIGN_TYPE_COMMON:
                cash = p.cash
                count = min(cash / (item._consignFixedPrice * 1.0 / item.cwrap), item.cwrap)
            elif self.curConsignType == uiConst.CONSIGN_TYPE_COIN:
                coin = p.unbindCoin
                count = min(coin / item._consignPrice, item.cwrap)
            return GfxValue(int(count))

    def onGetTabChangeCD(self, *arg):
        cd = CCCD.data.get('ConsignTypeChangeCD', 2)
        return GfxValue(cd)

    def onShowTabChangeWarning(self, *arg):
        BigWorld.player().showGameMsg(GMDD.data.CONSIGN_CHANGE_TAB_COUNT_DOWN, ())

    def onGetStorageFeeTip(self, *arg):
        tip = SCD.data.get('storageFeeTip', gameStrings.TEXT_CONSIGNPROXY_1315)
        return GfxValue(gbk2unicode(tip))


class ConsignSearchHistory(SearchHistoryUtils):

    def __init__(self):
        super(ConsignSearchHistory, self).__init__('Consign')
        self.maxCount = 20
