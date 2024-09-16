#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/tabAuctionCrossServerProxy.o
from gamestrings import gameStrings
import re
import copy
import time
import math
import BigWorld
import gameglobal
import uiUtils
import utils
import keys
import uiConst
import const
import events
import ui
from Scaleform import GfxValue
import gamelog
from callbackHelper import Functor
from guis import pinyinConvert
import formula
from gamestrings import gameStrings
from helpers import searchItemHelper
from ui import gbk2unicode
from ui import unicode2gbk
from searchHistoryUtils import SearchHistoryUtils
from uiProxy import SlotDataProxy
from cdata import game_msg_def_data as GMDD
from data import item_data as ID
from data import item_catagory_data as ICD
from data import school_data as SD
from data import sys_config_data as SCD
from data import item_name_data as IND
from data import push_data as PMD
from data import prop_ref_data as PRD
from data import manual_equip_props_data as MEPD
from data import manual_equip_special_prop_data as MESPD
from data import extended_equip_prop_data as EEPD
from data import skill_general_template_data as SGTD
from data import yaopei_extra_prop_data as YEPD
from data import equip_random_property_data as ERPD
from data import equip_property_pool_data as EPPD
from data import equip_data as ED
from data import region_server_config_data as RSCD
from cdata import equip_special_props_data as ESPD
from cdata import yaopei_prop_data as YPD
from cdata import coin_consign_config_Data as CCCD
FILTER_SEARCH_TYPE_COLOR_DICT = {const.XCONSIGN_FILTER_TYPE_RPROP: '#0088CC',
 const.XCONSIGN_FILTER_TYPE_YAOPEI_PROP: '#E6A712',
 const.XCONSIGN_FILTER_TYPE_YAOPEI_SKILL: '#FF8C19',
 const.XCONSIGN_FILTER_TYPE_SE_MANUAL: '#ED7600'}
FILTER_SEARCH_TYPE_LABEL_DICT = {const.XCONSIGN_FILTER_TYPE_RPROP: gameStrings.CROSS_CONSIGN_FILTER_RPROP,
 const.XCONSIGN_FILTER_TYPE_YAOPEI_PROP: gameStrings.CROSS_CONSIGN_FILTER_YAOPEI_PROP,
 const.XCONSIGN_FILTER_TYPE_YAOPEI_SKILL: gameStrings.CROSS_CONSIGN_FILTER_YAOPEI_SKILL,
 const.XCONSIGN_FILTER_TYPE_SE_MANUAL: gameStrings.CROSS_CONSIGN_FILTER_SPECIAL_EFFECT}
BUY_PANEL = 0
CARE_PANEL = 1
BID_PANEL = 2
SELL_PANEL = 3
TRADE_HISTORY_PANEL = 4
TIME_OUT_CHECK = 3
CHECK_DATA_TIME = 4
CARE_MAX_CNT = 20
ITEM_NUM_PER_PAGE = 20
ONE_DAY_SEC = 86400
ONE_DAY_HOUR = 24
AUTO_REFRESH_INTERVAL = 5
SORT_TYPE_DICT = {BUY_PANEL: ('qualityBtn',
             'nameBtn',
             'lvBtn',
             'timeBtn',
             'priceBtn',
             'careBtn'),
 CARE_PANEL: ('qualityBtn',
              'nameBtn',
              'priceBtn',
              'timeBtn',
              'careBtn'),
 BID_PANEL: ('qualityBtn',
             'nameBtn',
             'priceBtn',
             'timeBtn',
             'careBtn'),
 SELL_PANEL: ('qualityBtn',
              'nameBtn',
              'lvBtn',
              'timeBtn',
              'priceBtn',
              'careBtn'),
 TRADE_HISTORY_PANEL: ()}
SORT_BTN_TO_TYPE = {'qualityBtn': const.XCONSIGN_SORT_TYPE_QUALITY,
 'nameBtn': const.XCONSIGN_SORT_TYPE_DBID,
 'lvBtn': const.XCONSIGN_SORT_TYPE_LEVEL,
 'timeBtn': const.XCONSIGN_SORT_TYPE_ENDDAY,
 'careBtn': const.XCONSIGN_SORT_TYPE_FOLLOW}
SELECTEDTIPS = {(0, 0): gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_100,
 (0, 1): gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_101,
 (0, 2): gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_102,
 (1, 0): gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_103,
 (1, 1): gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_104,
 (1, 2): gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_105}

class TabAuctionCrossServerProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(TabAuctionCrossServerProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerMc': self.onRegisterMc,
         'unRegisterMc': self.onUnRegisterMc,
         'getCash': self.onGetCash,
         'changeTab': self.onChangeTab,
         'getTax': self.onGetTax,
         'getCategory': self.onGetCategory,
         'getQualityTypes': self.onGetQualityTypes,
         'selectCategory': self.onSelectCategory,
         'getSearchHistory': self.onGetSearchHistory,
         'getItemNames': self.onGetItemNames,
         'getHistoryCfg': self.onGetHistoryCfg,
         'fitting': self.onFitting,
         'prevPage': self.onPrevPage,
         'nextPage': self.onNextPage,
         'firstPage': self.onFirstPage,
         'lastPage': self.onLastPage,
         'gotoPage': self.onGotoPage,
         'sortItems': self.onSortItems,
         'getCoinConsignLimit': self.onGetCoinConsignLimit,
         'getStorageFeeTip': self.onGetStorageFeeTip,
         'getSellRecord': self.onGetSellRecord,
         'setSwitchData': self.onSetSwitchData,
         'removeItem': self.onRemoveItem,
         'bidItem': self.onBidItem,
         'sellItem': self.onSellItem,
         'getDetailCanvasInfo': self.onGetDetailCanvasInfo,
         'getInitConstStr': self.onGetInitConstStr,
         'cancelSellItem': self.onCancelSellItem,
         'getFee': self.onGetFee,
         'getItemMaxNum': self.onGetItemMaxNum,
         'numChange': self.onNumChange,
         'getPriceLimit': self.onGetPriceLimit,
         'searchItems': self.onSearchItems,
         'careItem': self.onCareItem,
         'getBuyItemInfo': self.onGetBuyItemInfo,
         'closeBidPanel': self.onCloseBidPanel,
         'closeBidFailedPanel': self.onCloseBidFailedPanel,
         'closeSellSuccessPanel': self.onCloseSellSuccessPanel,
         'closeSubmitFailedPanel': self.onCloseSubmitFailedPanel,
         'confirmBid': self.onConfirmBid,
         'getMinBidPrice': self.onGetMinBidPrice,
         'getPushData': self.onGetPushData,
         'receivePushCoin': self.onReceivePushCoin,
         'getBidMaxNum': self.onGetBidMaxNum,
         'getSelectedTips': self.onGetSelectedTips,
         'getSellPanelType': self.onGetSellPanelType,
         'getHasRegionQuery': self.onGetHasRegionQuery,
         'openRegionQueryPanel': self.onOpenRegionQueryPanel,
         'getServerTimezone': self.onGetServerTimezone,
         'commonRefresh': self.onCommonRefreshBtn,
         'saveFilterSetting': self.onSaveFilterSetting,
         'getFilterSearchType': self.onGetFilterSearchType,
         'getFilterSubSearchType': self.onGetFilterSubSearchType,
         'canFilterSearch': self.onCanFilterSearch,
         'showGameMsg': self.onShowGameMsg,
         'getSelectedCateName': self.onGetSelectedCateName,
         'openCharge': self.onOpenCharge}
        self.panelMc = None
        self.bidMediator = None
        self.bidFailedMediator = None
        self.sellSuccessMediator = None
        self.submitFailedMediator = None
        self.searchItemName = ''
        self.bindType = 'tabAuctionCrossServer'
        self.type = 'tabAuctionCrossServer'
        self.pageSrc = -1
        self.posSrc = -1
        self.npcId = None
        self.dealAverage = 0
        self.average = 0
        self.fixedPrice = 0
        self.curTradeInfoCache = {}
        self.historyInfoCache = {}
        self.tabIdx = BUY_PANEL
        self.reqInfoStep = 0
        self.reqInfoCheckCallBack = None
        self.timeCheckCB = None
        self.buyData = {}
        self.buyDbIds = []
        self.buyInfo = {}
        self.buySearchArg = None
        self.myCareData = {}
        self.myCareDbIds = []
        self.myCareInfo = {}
        self.myBidData = {}
        self.myBidDbIds = []
        self.myBidInfo = {}
        self.mySellData = {}
        self.mySellDbIds = []
        self.mySellInfo = {}
        self.sameSellItemData = {}
        self.sameSellItemDbIds = []
        self.sameSellItemInfo = {}
        self.historyData = {}
        self.historyDbIds = []
        self.historyInfo = {}
        self.refreshDbIds = []
        self.initInfo = {}
        self.consignSearchHistory = TabAuctionCrossServerSearchHistory()
        self.curDbId = None
        self.bidFailedPushMessageInfo = []
        self.sellSuccessPushMessageInfo = []
        self.submitFailedPushMessageInfo = []
        self.curBidFailedPushData = {}
        self.curSellSuccessPushData = {}
        self.curSubmitFailedPushData = {}
        self.autoRefreshCallBack = None
        self.xconsignStartCallBack = None
        self.canFilterCache = {}
        self.filterTypeCache = {}
        self.filterPropCache = {}
        self.nameItemCache = {}
        self.anonymousCache = {}
        self.searchItemId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_TAB_CROSS_SERVER_BID, self.closeBidPanel)
        uiAdapter.registerEscFunc(uiConst.WIDGET_TAB_CROSS_SERVER_BID_FAILED, self.closeBidFailedPanel)
        uiAdapter.registerEscFunc(uiConst.WIDGET_TAB_CROSS_SERVER_SELL_SUCCESS, self.closeSellSuccessPanel)
        uiAdapter.registerEscFunc(uiConst.WIDGET_TAB_CROSS_SERVER_SUBMIT_FAILED, self.closeSubmitFailedPanel)

    def onRegisterMc(self, *arg):
        p = BigWorld.player()
        p.base.guessXConsignFollowingDBIDs(uiConst.TABAUCTION_OPTYPE_REFRESH_MYCARE_SERVERDATA)
        self.panelMc = arg[3][0]
        self.consignSearchHistory.readConfigData()
        self.addEvent(events.EVENT_INVENTORY_ITEM_CLICKED, self.onInventoryRightClick)
        self.addEvent(events.EVENT_TIANBI_COIN_CHANGED, self.onCoinChanged)
        self.resetBuyInfo()
        self.resetCareInfo()
        self.resetBidInfo()
        self.resetMySellInfo()
        self.resetSameSellItemInfo()
        self.resetHistoryInfo()
        self.setStateTxt()
        self.setAutoRefreshCallBack()
        gamelog.debug('@zq self.initInfo', self.initInfo)
        return uiUtils.dict2GfxDict(self.initInfo, True)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_TAB_CROSS_SERVER_BID:
            self.bidMediator = mediator
        elif widgetId == uiConst.WIDGET_TAB_CROSS_SERVER_BID_FAILED:
            self.bidFailedMediator = mediator
        elif widgetId == uiConst.WIDGET_TAB_CROSS_SERVER_SELL_SUCCESS:
            self.sellSuccessMediator = mediator
        elif widgetId == uiConst.WIDGET_TAB_CROSS_SERVER_SUBMIT_FAILED:
            self.submitFailedMediator = mediator

    def onUnRegisterMc(self, *arg):
        self.clearWidgetData()
        gamelog.debug('@zq CrossServer onUnRegisterMc')

    def cancelAutoRefreshCallBack(self):
        if self.autoRefreshCallBack:
            BigWorld.cancelCallback(self.autoRefreshCallBack)
            self.autoRefreshCallBack = None

    def setAutoRefreshCallBack(self):
        self.cancelAutoRefreshCallBack()
        auto_refresh_interval = gameglobal.rds.configData.get('xConsignClientAutoRefresh', 20)
        self.autoRefreshCallBack = BigWorld.callback(auto_refresh_interval, self.autoRefreshCB)
        gamelog.debug('@zq setAutoRefreshCallBack', auto_refresh_interval)

    def autoRefreshCB(self):
        if self.tabIdx == CARE_PANEL:
            if self.myCareDbIds:
                self.refreshOneCurItemWithUpdate(self.myCareDbIds)
        elif self.tabIdx == BID_PANEL:
            if self.myBidDbIds:
                self.refreshOneCurItemWithUpdate(self.myBidDbIds)
        self.setAutoRefreshCallBack()
        gamelog.debug('@zq autoRefreshCB b2')

    def resetMySellInfo(self):
        self.mySellInfo = {}
        self.mySellInfo['curPage'] = 1
        self.mySellInfo['maxPage'] = 1
        self.mySellInfo['isSinglePrice'] = False
        self.mySellInfo['sortType'] = 'priceBtn'
        self.mySellInfo['sortOrderType'] = const.XCONSIGN_ORDER_TYPE_INC

    def resetSameSellItemInfo(self):
        self.sameSellItemInfo = {}
        self.sameSellItemInfo['curPage'] = 1
        self.sameSellItemInfo['maxPage'] = 1
        self.sameSellItemInfo['isSinglePrice'] = False
        self.sameSellItemInfo['sortType'] = 'priceBtn'
        self.sameSellItemInfo['sortOrderType'] = const.XCONSIGN_ORDER_TYPE_INC

    def resetBuyInfo(self):
        self.buyInfo = {}
        self.buyInfo['curPage'] = 1
        self.buyInfo['maxPage'] = 1
        self.buyInfo['isSinglePrice'] = False
        self.buyInfo['sortType'] = 'priceBtn'
        self.buyInfo['sortOrderType'] = const.XCONSIGN_ORDER_TYPE_INC

    def resetBidInfo(self):
        self.myBidInfo = {}
        self.myBidInfo['curPage'] = 1
        self.myBidInfo['maxPage'] = 1
        self.myBidInfo['isSinglePrice'] = False
        self.myBidInfo['sortType'] = 'priceBtn'
        self.myBidInfo['sortOrderType'] = const.XCONSIGN_ORDER_TYPE_INC

    def resetCareInfo(self):
        self.myCareInfo = {}
        self.myCareInfo['curPage'] = 1
        self.myCareInfo['maxPage'] = 1
        self.myCareInfo['isSinglePrice'] = False
        self.myCareInfo['sortType'] = 'priceBtn'
        self.myCareInfo['sortOrderType'] = const.XCONSIGN_ORDER_TYPE_INC

    def resetHistoryInfo(self):
        self.historyInfo = {}
        self.historyInfo['curPage'] = 1
        self.historyInfo['maxPage'] = 1
        self.historyInfo['isSinglePrice'] = False
        self.historyInfo['sortType'] = ''
        self.historyInfo['sortOrderType'] = const.XCONSIGN_ORDER_TYPE_INC

    def onGetDetailCanvasInfo(self, *arg):
        return uiUtils.dict2GfxDict(self.getTabInfo(), True)

    def onGetInitConstStr(self, *args):
        ret = {1: gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_359,
         2: gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_360,
         3: gameStrings.TEXT_GM_COMMAND_WINGWORLD_1215,
         4: gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_362,
         5: gameStrings.TEXT_IMPITEM_2349,
         6: gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_364,
         7: gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_365,
         8: gameStrings.TEXT_ITEMTOOLTIPUTILS_768,
         9: gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_367,
         10: gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_368,
         11: gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_369,
         12: gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_370,
         13: gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_371,
         14: gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_372,
         15: gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_373,
         16: gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_374,
         17: gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_375,
         18: [gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_376, gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_376_1, gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_376_2],
         19: gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_377,
         20: gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_378,
         21: gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_379,
         22: gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_380,
         23: gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_381}
        return uiUtils.dict2GfxDict(ret, True)

    def clearWidgetData(self):
        if self.searchItemId:
            sHelper = searchItemHelper.getInstance()
            sHelper.cancelTask(self.searchItemId)
            self.searchItemId = 0
        self.cancelAutoRefreshCallBack()
        self.panelMc = None
        self.reqInfoStep = 0
        self.buyData = {}
        self.buyDbIds = []
        self.buyInfo = {}
        self.buySearchArg = None
        self.myCareData = {}
        self.myCareDbIds = []
        self.myCareInfo = {}
        self.myBidData = {}
        self.myBidDbIds = []
        self.myBidInfo = {}
        self.mySellData = {}
        self.mySellDbIds = []
        self.mySellInfo = {}
        self.sameSellItemData = {}
        self.sameSellItemDbIds = []
        self.sameSellItemInfo = {}
        self.historyData = {}
        self.historyDbIds = []
        self.historyInfo = {}
        self.consignSearchHistory.writeConfigData()
        self.cancelTimeOutCB()
        self.cancelCheckCB()
        self.removeItem(1, 99)
        self.initInfo = {}
        self.closeBidPanel()

    def clearPushData(self):
        self.bidFailedPushMessageInfo = []
        self.sellSuccessPushMessageInfo = []
        self.submitFailedPushMessageInfo = []
        self.curBidFailedPushData = {}
        self.curSellSuccessPushData = {}
        self.curSubmitFailedPushData = {}
        if self.xconsignStartCallBack:
            BigWorld.cancelCallback(self.xconsignStartCallBack)
            self.xconsignStartCallBack = None

    def cancelTimeOutCB(self):
        if self.reqInfoCheckCallBack:
            BigWorld.cancelCallback(self.reqInfoCheckCallBack)
            self.reqInfoCheckCallBack = None

    def setTimeOutCB(self, _cb):
        if self.reqInfoCheckCallBack:
            BigWorld.cancelCallback(self.reqInfoCheckCallBack)
        self.reqInfoCheckCallBack = BigWorld.callback(TIME_OUT_CHECK, _cb)

    def cancelCheckCB(self):
        if self.timeCheckCB:
            BigWorld.cancelCallback(self.timeCheckCB)
            self.timeCheckCB = None

    def setTimeCheckCB(self, _cb):
        if self.timeCheckCB:
            BigWorld.cancelCallback(self.timeCheckCB)
        self.timeCheckCB = BigWorld.callback(2, _cb)

    def onSetSwitchData(self, *arg):
        gameglobal.rds.ui.tabAuction.setSwitchData(*arg)

    def setInitInfo(self, dataDic):
        self.initInfo = dataDic

    def refreshInfo(self):
        if self.panelMc:
            info = {}
            self.panelMc.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

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

    def onChangeTab(self, *arg):
        tabIdx = int(arg[3][0].GetNumber())
        self.tabIdx = tabIdx
        if self.panelMc:
            _info = self.getTabInfo()
            self.panelMc.Invoke('setSortState', uiUtils.dict2GfxDict(_info, True))
            self.refreshItems()

    def onGetTax(self, *arg):
        tax = CCCD.data.get('crossConsignTaxRatio', 0)
        return GfxValue(tax)

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
            if not value.get('showInCrossConsign', 0):
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

    def onSelectCategory(self, *arg):
        pass

    def onGetSearchHistory(self, *arg):
        return uiUtils.array2GfxAarry(self.consignSearchHistory.getReverseHistoryList(), True)

    def onGetItemMaxNum(self, *arg):
        key = arg[3][0].GetString()
        ret = 0
        if self.bindingData.has_key(key):
            item = self.bindingData[key]
            ret = item.cwrap if item and hasattr(item, 'cwrap') else ''
            if self.panelMc != None:
                self.panelMc.Invoke('setSellPanelNum', GfxValue(ret))
            if item:
                self._updatePrice(item.id, ret, item.cwrap)

    def onNumChange(self, *arg):
        num = int(arg[3][0].GetNumber())
        it = BigWorld.player().inv.getQuickVal(self.pageSrc, self.posSrc)
        curItem = self.bindingData.get('tabAuctionCrossServer1.slot99', None)
        self.consignNum = num
        if it and curItem and it.id == curItem.id:
            self._updatePrice(it.id, num, it.cwrap)

    def _updatePrice(self, itemId, count, maxCnt):
        self.panelMc.Invoke('setItemPrice', uiUtils.array2GfxAarry([int(self.dealAverage),
         count,
         int(self.average),
         int(self.fixedPrice),
         int(maxCnt)]))

    @ui.callFilter(2)
    def onSearchItems(self, *arg):
        name = arg[3][0].GetString().strip()
        if name:
            name = unicode2gbk(name)
        cate = arg[3][6].GetString().strip().split(',')
        self.searchItemsByName(name, cate, *arg)
        self.buySearchArg = arg

    def searchItemsByName(self, name, cate = [''], *arg):
        p = BigWorld.player()
        e = self._getEntity()
        if not e:
            return
        else:
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
            scoreReq = int(arg[3][8].GetNumber())
            cond1 = int(arg[3][9].GetNumber())
            arg1 = int(arg[3][10].GetNumber())
            cond2 = int(arg[3][11].GetNumber())
            arg2 = int(arg[3][12].GetNumber())
            cond3 = int(arg[3][13].GetNumber())
            arg3 = int(arg[3][14].GetNumber())
            specialArg = unicode2gbk(arg[3][15].GetString())
            rarityMiracle = int(arg[3][16].GetBool())
            enabledFilterSearch = gameglobal.rds.configData.get('enableCrossConsignFilterSearch')
            advArgsTuple = (cond1,
             arg1,
             cond2,
             arg2,
             cond3,
             arg3,
             scoreReq,
             rarityMiracle) if enabledFilterSearch else ()
            advArgs = []
            for advId in advArgsTuple:
                if advId:
                    advArgs = advArgsTuple
                    break

            specialArgTuple = specialArg.split(',') if enabledFilterSearch else ()
            specialArgs = []
            for specialId in specialArgTuple:
                if specialId:
                    specialArgs.append(int(specialId))

            sortType = self.buyInfo.get('sortType', '')
            isSinglePrice = self.buyInfo.get('isSinglePrice', False)
            realSortType = self.getRealSortType(sortType, isSinglePrice)
            sortOrderType = self.buyInfo.get('sortOrderType', 1)
            if name:
                self.consignSearchHistory.addSearchHistoryData(name)
                forme = arg[3][1].GetBool() if arg else 0
                minLv = arg[3][2].GetString().strip() if arg else 0
                maxLv = arg[3][3].GetString().strip() if arg else 0
                quality = arg[3][4].GetString().strip() if arg else 0
                if forme or minLv or maxLv or int(quality):
                    p.showGameMsg(GMDD.data.CONSIGN_SEARCH_ITEM_WRONG_OPTIONS, ())
                    self.buySearchArg = None
                    return

                def searchComplete(searchId, itemArr):
                    if not self.panelMc:
                        return
                    itemIds = self.getItemIdsByName(name, school=school, forme=forme, mType=category, sType=subcategory, itemIdArr=itemArr)
                    p = BigWorld.player()
                    if not itemIds:
                        _info = {'itemDbIds': [],
                         'itemInfo': {},
                         'pageData': {}}
                        self.panelMc.Invoke('setDetailItems', uiUtils.dict2GfxDict(_info, True))
                        return
                    p.base.doSearchXConsignByID(uiConst.TABAUCTION_OPTYPE_SEARCH_BUY, itemIds, realSortType, sortOrderType, advArgs, specialArgs)

                sHelper = searchItemHelper.getInstance()
                if self.searchItemId:
                    sHelper.cancelTask(self.searchItemId)
                    self.searchItemId = 0
                curSearchArgs = {'owner': e,
                 'name': name,
                 'school': school,
                 'category': category,
                 'subcategory': subcategory,
                 'hasItemName': False}
                self.searchItemId = sHelper.addCrossServerConsignTask(curSearchArgs, searchComplete)
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
                    self.buySearchArg = None
                    return
                p.base.doSearchXConsignByType(uiConst.TABAUCTION_OPTYPE_SEARCH_BUY, category, subcategory, quality, minLv, maxLv, school, realSortType, sortOrderType, advArgs, specialArgs)
            return

    def getItemIdsByName(self, name, school = -1, forme = False, mType = -1, sType = -1, itemIdArr = None, bSearch = False):
        itemIds = []
        if itemIdArr:
            itemIds = itemIdArr
        p = BigWorld.player()
        hasItemName = False
        if not itemIds:
            itemIds = self.nameItemCache.get((name,
             school,
             forme,
             mType,
             sType), None)
        if itemIds != None:
            for itemId in itemIds:
                if name == ID.data.get('name', ''):
                    hasItemName = True

        else:
            itemIds = []
            if not itemIds and bSearch:
                for itemId, itemData in ID.data.iteritems():
                    if not utils.getItemCrossConsign(itemData):
                        continue
                    if name in itemData.get('name', ''):
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
                        hasItemName = hasItemName or itemData.get('name') == name
                        if itemData.get('name') == name:
                            itemIds.insert(0, itemId)
                        else:
                            itemIds.append(itemId)
                        if len(itemIds) >= const.ITEM_CONSIGN_MATCH and hasItemName:
                            break

        self.nameItemCache[name, school, forme, mType, sType] = itemIds
        if len(itemIds) >= const.ITEM_CONSIGN_MATCH and not hasItemName:
            BigWorld.player().showGameMsg(GMDD.data.CONSIGN_SEARCH_MATCH_FUZZY, ())
            return []
        elif not itemIds and not hasItemName:
            BigWorld.player().showGameMsg(GMDD.data.CONSIGN_SEARCH_MATCH_EMPTY, ())
            return []
        else:
            return itemIds

    def setMinLv(self, val):
        if self.panelMc != None:
            self.panelMc.Invoke('setMinLv', GfxValue(str(val)))

    def setMaxLv(self, val):
        if self.panelMc != None:
            self.panelMc.Invoke('setMaxLv', GfxValue(str(val)))

    def onRefreshContent(self, *arg):
        pass

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
        names = IND.data.get(uiConst.ITEM_NAME_CROSS_CONSIGN, {}).get(pinyin[0], [])
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

    def onGetHistoryCfg(self, *arg):
        ret = gameStrings.TEXT_CONSIGNPROXY_556
        return GfxValue(gbk2unicode(ret))

    def onFitting(self, *arg):
        dbId = int(arg[3][0].GetNumber())
        itData = copy.deepcopy(self.curTradeInfoCache.get(dbId, {}))
        it = itData.get('item', None)
        if it:
            gameglobal.rds.ui.fittingRoom.addItem(it)

    def onPrevPage(self, *arg):
        self.pageChangeEx(self._onPrevPage, *arg)

    def onNextPage(self, *arg):
        self.pageChangeEx(self._onNextPage, *arg)

    def onFirstPage(self, *arg):
        self.pageChangeEx(self._onFirstPage, *arg)

    def onLastPage(self, *arg):
        self.pageChangeEx(self._onLastPage, *arg)

    def onGotoPage(self, *arg):
        self.pageChangeEx(self._onGotoPage, *arg)

    def pageChangeEx(self, fun, *arg):
        if self.tabIdx == BUY_PANEL:
            self.pageChangeWithLimit(fun, *arg)
        elif self.tabIdx == SELL_PANEL and self.pageSrc != -1 and self.posSrc != -1:
            self.pageChangeWithLimit(fun, *arg)
        else:
            self.pageChangeWithoutLimit(fun, *arg)

    @ui.callFilter(1)
    def pageChangeWithLimit(self, fun, *arg):
        fun(*arg)

    def pageChangeWithoutLimit(self, fun, *arg):
        fun(*arg)

    def _onPrevPage(self, *arg):
        _info = self.getTabInfo()
        if _info.get('curPage', 0) > 1:
            _info['curPage'] -= 1
            self.refreshItems(pageChange=True)

    def _onNextPage(self, *arg):
        _info = self.getTabInfo()
        if _info.get('curPage', 0) < _info.get('maxPage', 0):
            _info['curPage'] += 1
            self.refreshItems(pageChange=True)

    def _onFirstPage(self, *arg):
        _info = self.getTabInfo()
        _info['curPage'] = 1
        self.refreshItems(pageChange=True)

    def _onLastPage(self, *arg):
        _info = self.getTabInfo()
        _info['curPage'] = _info['maxPage']
        self.refreshItems(pageChange=True)

    def _onGotoPage(self, *arg):
        page = unicode2gbk(arg[3][0].GetString())
        if page:
            _info = self.getTabInfo()
            page = int(page)
            if page > 0 and page <= _info['maxPage']:
                _info['curPage'] = page
                self.refreshItems(pageChange=True)

    def refreshItems(self, bSort = False, pageChange = False, commonRefresh = False):
        if self.tabIdx == BUY_PANEL:
            self.setBuyItems(bSort, pageChange, commonRefresh)
        elif self.tabIdx == CARE_PANEL:
            self.setMyCareItems()
        elif self.tabIdx == BID_PANEL:
            self.setMyBidItems()
        elif self.tabIdx == SELL_PANEL:
            if self.pageSrc == -1 and self.posSrc == -1:
                self.setMySellItems(commonRefresh)
            else:
                self.setSameSellItems(commonRefresh, bSort, pageChange)
        elif self.tabIdx == TRADE_HISTORY_PANEL:
            self.setHistoryItems()

    def getTabInfo(self):
        if self.tabIdx == BUY_PANEL:
            return self.buyInfo
        if self.tabIdx == CARE_PANEL:
            return self.myCareInfo
        if self.tabIdx == BID_PANEL:
            return self.myBidInfo
        if self.tabIdx == SELL_PANEL:
            if self.pageSrc == -1 and self.posSrc == -1:
                return self.mySellInfo
            else:
                return self.sameSellItemInfo
        elif self.tabIdx == TRADE_HISTORY_PANEL:
            return self.historyInfo

    def onGetSellPanelType(self, *arg):
        _type = self.getSellPanelType()
        return GfxValue(gbk2unicode(_type))

    def getSellPanelType(self):
        if self.tabIdx == SELL_PANEL:
            if self.pageSrc == -1 and self.posSrc == -1:
                return 'mySell'
            else:
                return 'sameSell'
        return ''

    def onSortItems(self, *arg):
        if self.tabIdx == BUY_PANEL:
            self.onSortItemsWithLimit(*arg)
        elif self.tabIdx == SELL_PANEL and self.pageSrc != -1 and self.posSrc != -1:
            self.onSortItemsWithLimit(*arg)
        else:
            self.onSortItemsWithoutLimit(*arg)

    @ui.callFilter(2)
    def onSortItemsWithLimit(self, *arg):
        self._sortItemsEx(*arg)

    def onSortItemsWithoutLimit(self, *arg):
        self._sortItemsEx(*arg)

    def _sortItemsEx(self, *arg):
        btnName = unicode2gbk(arg[3][0].GetString())
        isSinglePrice = arg[3][1].GetBool()
        gamelog.debug('@zq onSortItems', btnName)
        bRefresh = False
        _info = self.getTabInfo()
        if _info['isSinglePrice'] != isSinglePrice:
            _info['isSinglePrice'] = isSinglePrice
            bRefresh = True
        if btnName in SORT_TYPE_DICT[self.tabIdx]:
            if _info['sortType'] == btnName:
                if _info['sortOrderType'] == const.XCONSIGN_ORDER_TYPE_INC:
                    _info['sortOrderType'] = const.XCONSIGN_ORDER_TYPE_DEC
                elif _info['sortOrderType'] == const.XCONSIGN_ORDER_TYPE_DEC:
                    _info['sortOrderType'] = const.XCONSIGN_ORDER_TYPE_INC
                else:
                    _info['sortOrderType'] = const.XCONSIGN_ORDER_TYPE_INC
            else:
                _info['sortType'] = btnName
            bRefresh = True
        if self.panelMc and bRefresh:
            self.panelMc.Invoke('setShowSinglePrice')
            self.panelMc.Invoke('setSortState', uiUtils.dict2GfxDict(_info, True))
            self.refreshItems(bSort=True)

    def onGetCoinConsignLimit(self, *arg):
        p = BigWorld.player()
        playerLv = p.realLv
        coinConsignLimit = CCCD.data.get('crossConsignSellMax', {})
        coinConsignLimit = sorted(coinConsignLimit.items(), reverse=True)
        for data in coinConsignLimit:
            if playerLv >= data[0]:
                return GfxValue(gbk2unicode(uiUtils.getTextFromGMD(GMDD.data.CROSS_CONSIGN_LIMIT, gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_987) % data[1]))

        return GfxValue(gbk2unicode(uiUtils.getTextFromGMD(GMDD.data.CROSS_CONSIGN_LIMIT, gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_987) % 0))

    def onGetStorageFeeTip(self, *arg):
        tip = gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_992
        return GfxValue(gbk2unicode(tip))

    def onGetSellRecord(self, *arg):
        pass

    def isItemDisabled(self, kind, page, pos, item):
        if self.panelMc and kind == const.RES_KIND_INV:
            key = self._getKey(1, 99)
            if page == self.pageSrc and pos == self.posSrc:
                return self.bindingData.get(key, None)

    def _getKey(self, bar, slot):
        return 'tabAuctionCrossServer%d.slot%d' % (bar, slot)

    def _getEntity(self):
        return gameglobal.rds.ui.tabAuction.getEntity()

    @ui.checkItemIsLock([4, 5])
    def setItem(self, bar, slot, item, pageSrc, posSrc):
        gamelog.debug('@zq setItem', bar, slot, item, pageSrc, posSrc)
        if not item.isItemCrossConsign():
            BigWorld.player().showGameMsg(GMDD.data.ITEM_NO_XCONSIGN, ())
            return
        else:
            key = self._getKey(bar, slot)
            if self.binding.has_key(key):
                self.bindingData[key] = item
                self.pageSrc = pageSrc
                self.posSrc = posSrc
                p = BigWorld.player()
                gameglobal.rds.ui.inventory.updateSlotState(pageSrc, posSrc)
                self.consignNum = item.cwrap
                data = uiUtils.getGfxItem(item)
                self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(data))
                self.average = 0
                self.fixedPrice = 0
                self.dealAverage = 0
                if self.panelMc != None:
                    self.panelMc.Invoke('setKeepType', GfxValue(0))
                    self.panelMc.Invoke('setSellPanelTitle', GfxValue(1))
                    _info = self.getTabInfo()
                    self.panelMc.Invoke('setSortState', uiUtils.dict2GfxDict(_info, True))
                    self.onUpdatePrice(item.id, 0)
                    p.base.guessXConsignAvgPrice(item.id)
                    self.setSameSellItems(setItem=True)
                    self.setItemPriceLimit(item.id)
            return

    def setItemPriceLimit(self, itemId = None):
        if self.panelMc:
            info = {'maxUnitPrice': self._getXConsignMaxUnitPrice(),
             'minUnitPrice': self._getLowestUnitPriceOfItem(itemId),
             'maxTotalPrice': self._getXConsignMaxTotalPrice(),
             'minTotalPrice': self._getXConsignMinTotalPrice(),
             'visible': itemId != None}
            self.panelMc.Invoke('setItemPriceLimit', uiUtils.dict2GfxDict(info, True))

    def onUpdatePrice(self, itemId, price):
        if self.panelMc and self.pageSrc != -1:
            p = BigWorld.player()
            it = p.inv.getQuickVal(self.pageSrc, self.posSrc)
            self.dealAverage = price
            self.average = price
            self.fixedPrice = price
            minUnitPrice = self._getLowestUnitPriceOfItem(itemId)
            if self.average < minUnitPrice:
                self.average = minUnitPrice
            if it and it.id == itemId:
                self.panelMc.Invoke('setItemPrice', uiUtils.array2GfxAarry([int(self.dealAverage),
                 it.cwrap,
                 int(self.average),
                 int(self.fixedPrice),
                 it.cwrap]))

    def onGetFee(self, *arg):
        timeType = int(arg[3][0].GetNumber()) + 1
        fee = CCCD.data.get('crossConsignStorageCash' + str(timeType), 0)
        return GfxValue(fee)

    def removeItem(self, bar, slot):
        gamelog.debug('@zq removeItem')
        key = self._getKey(bar, slot)
        if self.binding.has_key(key):
            self.bindingData[key] = None
            data = GfxValue(0)
            data.SetNull()
            self.binding[key][1].InvokeSelf(data)
            self.binding[key][0].Invoke('setSlotColor', GfxValue('nothing'))
            gameglobal.rds.ui.inventory.updateSlotState(self.pageSrc, self.posSrc)
            self.pageSrc = -1
            self.posSrc = -1
            self.average = 0
            self.fixedPrice = 0
            if self.panelMc != None:
                self.panelMc.Invoke('setItemPrice', uiUtils.array2GfxAarry([0,
                 '',
                 '',
                 '',
                 0]))
                self.panelMc.Invoke('setBidBtnState', GfxValue(False))
                self.panelMc.Invoke('setSellPanelTitle', GfxValue(0))
                _info = self.getTabInfo()
                self.panelMc.Invoke('setSortState', uiUtils.dict2GfxDict(_info, True))
                self.setTab(SELL_PANEL)
                self.setMySellItems()
                self.setItemPriceLimit()

    def setInventoryItem(self, nPageSrc, nItemSrc, nPageDes, nItemDes):
        gamelog.debug('@zq setInventoryItem')
        p = BigWorld.player()
        i = p.inv.getQuickVal(nPageSrc, nItemSrc)
        if i.isRuneHasRuneData():
            p.showGameMsg(GMDD.data.ITEM_CONSIGN_RUNE_EQUIP, ())
            return
        if i.isForeverBind():
            p.showGameMsg(GMDD.data.CONSIGN_ITEM_BIND, (i.name,))
            return
        if not i.isItemCrossConsign():
            BigWorld.player().showGameMsg(GMDD.data.ITEM_NO_XCONSIGN, ())
            return
        self.setTab(SELL_PANEL)
        self.setItem(nPageDes, nItemDes, i, nPageSrc, nItemSrc)

    def onInventoryRightClick(self, event):
        if self.panelMc:
            event.stop()
            i = event.data['item']
            nPage = event.data['page']
            nItem = event.data['pos']
            if i == None:
                return
            self.setInventoryItem(nPage, nItem, 1, 99)

    def onCoinChanged(self, event):
        if self.panelMc:
            self.updateCash()

    def updateCash(self):
        if self.panelMc != None:
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
            self.panelMc.Invoke('setCash', uiUtils.dict2GfxDict(ret, True))

    def getSlotID(self, key):
        idBar, idItem = key.split('.')
        return (int(idBar[21:]), int(idItem[4:]))

    def setTab(self, _tabId):
        if self.panelMc != None:
            self.panelMc.Invoke('setTab', GfxValue(_tabId))
            self.tabIdx = _tabId
            _info = self.getTabInfo()
            self.panelMc.Invoke('setSortState', uiUtils.dict2GfxDict(_info, True))

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        bar, slot = self.getSlotID(key)
        gamelog.debug('@zq onGetToolTip', bar, slot)
        if self.bindingData.has_key(key):
            item = None
            if self.bindingData[key]:
                item = copy.copy(self.bindingData[key])
                item.hideSign = True
            return gameglobal.rds.ui.inventory.GfxToolTip(item)
        else:
            if bar == 0:
                item = self.curTradeInfoCache.get(slot, {}).get('item', None)
                if item:
                    item.hideSign = True
                    return gameglobal.rds.ui.inventory.GfxToolTip(item)
                else:
                    return GfxValue('')
            else:
                return GfxValue('')
            return

    def onRemoveItem(self, *arg):
        key = arg[3][0].GetString()
        bar, slot = self.getSlotID(key)
        self.removeItem(bar, slot)

    def onBidItem(self, *arg):
        dbId = int(arg[3][0].GetNumber())
        if dbId:
            p = BigWorld.player()
            itemData = copy.deepcopy(self.curTradeInfoCache.get(dbId, {}))
            bidderIsMe = itemData['bidderHostID'] == int(gameglobal.rds.g_serverid) and itemData['bidderName'] == p.roleName
            vendorIsMe = itemData['vendorHostID'] == int(gameglobal.rds.g_serverid) and itemData['vendorName'] == p.roleName
            if vendorIsMe:
                p.showGameMsg(GMDD.data.XCONSIGN_NO_BID_SELF, ())
                return
        self.curDbId = dbId
        self.showBidPanel()

    def onCancelSellItem(self, *arg):
        itemId = int(arg[3][0].GetNumber())
        dbId = int(arg[3][1].GetNumber())
        e = self._getEntity()
        if e:
            e.cell.reqXConsignWithdraw(itemId, dbId)

    @ui.checkInventoryLock()
    def _onSellItem(self, num, bidPrice, durationType):
        e = self._getEntity()
        if e and self.pageSrc != -1:
            e.cell.reqXConsignItem(self.pageSrc, self.posSrc, num, bidPrice, durationType, BigWorld.player().cipherOfPerson)

    def onSellItem(self, *arg):
        self.sellCommonItem(*arg)

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
        isSinglePrice = arg[3][4].GetBool()
        if bidPrice:
            bidPrice = int(bidPrice)
        if isSinglePrice:
            bidPrice *= num
        if not bidPrice:
            p.showGameMsg(GMDD.data.CONSIGN_NO_BID_NOR_FIXED_PRICE, ())
            return
        it = p.inv.getQuickVal(self.pageSrc, self.posSrc)
        if not it or not it.canSplit(num):
            p.showGameMsg(GMDD.data.ITEM_NO_ENOUGH, (it.name if it else '',))
            return
        durationType = int(arg[3][3].GetNumber()) - 1
        e = self._getEntity()
        if e and self.pageSrc != -1:
            self._onSellItem(num, bidPrice, durationType)

    def setBuyItems(self, bSort = False, pageChange = False, commonRefresh = False):
        if self.panelMc:
            if commonRefresh:
                if self.buyDbIds:
                    self.buyInfo['resetPage'] = False
                    self.calcPageData(self.buyDbIds, self.buyInfo)
                    pagedItemInfo = self.getPagedData(self.buyDbIds, self.buyInfo.get('curPage', 1), self.buyInfo.get('maxPage', 1))
                    self.setClearPreData(uiConst.TABAUCTION_OPTYPE_SEARCH_BUY, pagedItemInfo, self.buyData)
                    result = self.getInfoFromCurCache(self.buyData, uiConst.TABAUCTION_OPTYPE_SEARCH_BUY)
                    self.dealCompleteOpId(uiConst.TABAUCTION_OPTYPE_SEARCH_BUY, result)
            elif bSort:
                self.buyInfo['resetPage'] = False
                self.panelMc.Invoke('keyUpFunctionBuy')
            elif self.buyDbIds:
                if pageChange:
                    self.buyInfo['resetPage'] = False
                self.calcPageData(self.buyDbIds, self.buyInfo)
                pagedItemInfo = self.getPagedData(self.buyDbIds, self.buyInfo.get('curPage', 1), self.buyInfo.get('maxPage', 1))
                self.setClearPreData(uiConst.TABAUCTION_OPTYPE_SEARCH_BUY, pagedItemInfo, self.buyData)
                result = self.getInfoFromCurCache(self.buyData, uiConst.TABAUCTION_OPTYPE_SEARCH_BUY)
                self.dealCompleteOpId(uiConst.TABAUCTION_OPTYPE_SEARCH_BUY, result)
            elif self.buySearchArg:
                self.buyInfo['resetPage'] = False
                self.onSearchItems(*self.buySearchArg)
                self.buySearchArg = None

    def setMyBidItems(self):
        if self.panelMc:
            self.myBidInfo['resetPage'] = False
            p = BigWorld.player()
            p.base.guessXConsignBiddingDBIDs(uiConst.TABAUCTION_OPTYPE_SEARCH_MYBID)

    def setMyCareItems(self):
        if self.panelMc:
            self.myCareInfo['resetPage'] = False
            p = BigWorld.player()
            p.base.guessXConsignFollowingDBIDs(uiConst.TABAUCTION_OPTYPE_SEARCH_MYCARE)

    def setHistoryItems(self):
        if self.panelMc:
            p = BigWorld.player()
            p.base.listMyXConsignHistory(uiConst.TABAUCTION_OPTYPE_SEARCH_HISTORY)

    def setMySellItems(self, commonRefresh = False):
        if self.panelMc:
            if self.mySellDbIds and not commonRefresh:
                result = self.getInfoFromCurCache(self.mySellData, uiConst.TABAUCTION_OPTYPE_SEARCH_MYSELL)
                self.dealCompleteOpId(uiConst.TABAUCTION_OPTYPE_SEARCH_MYSELL, result)
            else:
                p = BigWorld.player()
                p.base.guessXConsignSellingDBIDs(uiConst.TABAUCTION_OPTYPE_SEARCH_MYSELL)

    def setSameSellItems(self, checkData = True, bSort = False, pageChange = False, setItem = False):
        if self.panelMc:
            if not checkData and not bSort:
                if pageChange:
                    self.sameSellItemInfo['resetPage'] = False
                self.calcPageData(self.sameSellItemDbIds, self.sameSellItemInfo)
                pagedItemInfo = self.getPagedData(self.sameSellItemDbIds, self.sameSellItemInfo.get('curPage', 1), self.sameSellItemInfo.get('maxPage', 1))
                self.setClearPreData(uiConst.TABAUCTION_OPTYPE_SEARCH_SAMESELL, pagedItemInfo, self.sameSellItemData)
                result = self.getInfoFromCurCache(self.sameSellItemData, uiConst.TABAUCTION_OPTYPE_SEARCH_SAMESELL)
                self.dealCompleteOpId(uiConst.TABAUCTION_OPTYPE_SEARCH_SAMESELL, result)
            else:
                key = self._getKey(1, 99)
                if key in self.binding and key in self.bindingData:
                    itemId = self.bindingData[key].id
                    sortType = self.sameSellItemInfo.get('sortType', '')
                    isSinglePrice = self.sameSellItemInfo.get('isSinglePrice', False)
                    realSortType = self.getRealSortType(sortType, isSinglePrice)
                    sortOrderType = self.sameSellItemInfo.get('sortOrderType', 1)
                    p = BigWorld.player()
                    if not setItem:
                        self.sameSellItemInfo['resetPage'] = False
                    p.base.doSearchXConsignByID(uiConst.TABAUCTION_OPTYPE_SEARCH_SAMESELL, [itemId], realSortType, sortOrderType, (), ())

    def getRealSortType(self, btnName, isSinglePrice = False):
        if btnName in SORT_BTN_TO_TYPE:
            return SORT_BTN_TO_TYPE[btnName]
        if btnName == 'priceBtn':
            if isSinglePrice:
                return const.XCONSIGN_SORT_TYPE_UNITPRICE
            else:
                return const.XCONSIGN_SORT_TYPE_TOTALPRICE
        return 0

    def setSearchItemsByName(self):
        pass

    def setSearchItemsById(self, opNUID):
        if self.panelMc:
            if self.mySellDbIds:
                result = self.getInfoFromCurCache(self.mySellData, uiConst.TABAUCTION_OPTYPE_SEARCH_MYSELL)
                self.dealCompleteOpId(uiConst.TABAUCTION_OPTYPE_SEARCH_MYSELL, result)
            else:
                p = BigWorld.player()
                p.base.guessXConsignSellingDBIDs(uiConst.TABAUCTION_OPTYPE_SEARCH_MYSELL)

    def onXConsignSellingDBIDs(self, opNUID, listCurDBID):
        if opNUID == uiConst.TABAUCTION_OPTYPE_SEARCH_MYSELL:
            self.mySellDbIds = list(listCurDBID)
            self.calcPageData(self.mySellDbIds, self.mySellInfo)
            self.setClearPreData(opNUID, self.mySellDbIds, self.mySellData)
            result = self.getInfoFromCurCache(self.mySellData, opNUID)
            self.dealCompleteOpId(opNUID, result)

    def onXConsignBiddingDBIDs(self, opNUID, listCurDBID):
        if opNUID == uiConst.TABAUCTION_OPTYPE_SEARCH_MYBID:
            self.myBidDbIds = list(listCurDBID)
            self.calcPageData(self.myBidDbIds, self.myBidInfo)
            self.setClearPreData(opNUID, self.myBidDbIds, self.myBidData)
            result = self.getInfoFromCurCache(self.myBidData, opNUID)
            self.dealCompleteOpId(opNUID, result)
        elif opNUID == uiConst.TABAUCTION_OPTYPE_REFRESH_MYBID:
            self.myBidDbIds = list(listCurDBID)
            self.refreshOneCurItemWithUpdate(self.myBidDbIds)

    def onXConsignFollowingDBIDs(self, opNUID, listCurDBID):
        if opNUID == uiConst.TABAUCTION_OPTYPE_SEARCH_MYCARE:
            self.myCareDbIds = list(listCurDBID)
            self.calcPageData(self.myCareDbIds, self.myCareInfo)
            self.setClearPreData(opNUID, self.myCareDbIds, self.myCareData)
            result = self.getInfoFromCurCache(self.myCareData, opNUID)
            self.dealCompleteOpId(opNUID, result)
        elif opNUID == uiConst.TABAUCTION_OPTYPE_REFRESH_MYCARE:
            self.myCareDbIds = list(listCurDBID)
            self.refreshOneCurItemWithUpdate(self.myCareDbIds)
        elif opNUID == uiConst.TABAUCTION_OPTYPE_REFRESH_MYCARE_SERVERDATA:
            p = BigWorld.player()
            p.base.getXConsignInfoByCurDBIDs(opNUID, listCurDBID, False)

    def onXConsignHistories(self, opNUID, listCurDBID):
        if opNUID == uiConst.TABAUCTION_OPTYPE_SEARCH_HISTORY:
            self.historyDbIds = list(listCurDBID)
            self.calcPageData(self.historyDbIds, self.historyInfo)
            self.setClearPreData(opNUID, self.historyDbIds, self.historyData)
            result = self.getInfoFromHisCache(self.historyData, opNUID)
            self.dealCompleteOpId(opNUID, result)

    def onSearchXConsignByID(self, opNUID, curDBIDs):
        if opNUID == uiConst.TABAUCTION_OPTYPE_SEARCH_SAMESELL:
            self.sameSellItemDbIds = list(curDBIDs)
            self.calcPageData(self.sameSellItemDbIds, self.sameSellItemInfo)
            pagedItemInfo = self.getPagedData(self.sameSellItemDbIds, self.sameSellItemInfo.get('curPage', 1), self.sameSellItemInfo.get('maxPage', 1))
            self.setClearPreData(opNUID, pagedItemInfo, self.sameSellItemData)
            result = self.getInfoFromCurCache(self.sameSellItemData, opNUID)
            self.dealCompleteOpId(opNUID, result)
        elif opNUID == uiConst.TABAUCTION_OPTYPE_SEARCH_BUY:
            self.buyDbIds = list(curDBIDs)
            self.calcPageData(self.buyDbIds, self.buyInfo)
            pagedItemInfo = self.getPagedData(self.buyDbIds, self.buyInfo.get('curPage', 1), self.buyInfo.get('maxPage', 1))
            self.setClearPreData(opNUID, pagedItemInfo, self.buyData)
            result = self.getInfoFromCurCache(self.buyData, opNUID)
            self.dealCompleteOpId(opNUID, result)

    def setClearPreData(self, opNUID, listCurDBID, _info):
        _info.clear()
        for _dbId in listCurDBID:
            _info[_dbId] = {}

    def getInfoFromCurCache(self, _info, opNUID):
        isHolyData = True
        p = BigWorld.player()
        needAllInfoDbIds = []
        needInfoDbIds = []
        for _dbId, _v in _info.iteritems():
            bNeedAllInfo = True
            itemData = self.curTradeInfoCache.get(_dbId, None)
            if itemData:
                if self.hasCurBaseData(itemData):
                    bNeedAllInfo = False
                    if self.needGetVolatileData(itemData) or _v.get('forceRefresh', False):
                        needInfoDbIds.append(_dbId)
                    _info[_dbId] = copy.deepcopy(itemData)
            if bNeedAllInfo:
                needAllInfoDbIds.append(_dbId)
                _info[_dbId] = {}

        if needAllInfoDbIds:
            isHolyData = False
            self.reqInfoStep += 1
            p.base.getXConsignInfoByCurDBIDs(opNUID, needAllInfoDbIds, False)
        if needInfoDbIds:
            isHolyData = False
            self.reqInfoStep += 1
            p.base.getXConsignInfoByCurDBIDs(opNUID, needInfoDbIds, True)
        if not isHolyData:
            self.setTimeOutCB(Functor(self.getInfoTimeOut))
        return isHolyData

    def getInfoTimeOut(self):
        gamelog.debug('@zq getInfoTimeOut reqInfoStep', self.reqInfoStep)
        self.reqInfoStep = 0
        gamelog.debug('@zq CrossServerCosign get info time out')

    def hasCurBaseData(self, data):
        if data and 'item' in data and 'curDBID' in data and 'vendorHostID' in data and 'vendorName' in data and 'beginDay' in data and 'endDay' in data:
            return True
        return False

    def needGetVolatileData(self, data):
        if 'bidderHostID' in data and 'bidderName' in data and 'latestPrice' in data and 'followCount' in data:
            if 'criticalBidCount' in data:
                if utils.getNow() - data.get('time', 0) > CHECK_DATA_TIME:
                    return True
                return False
        return True

    def onGetCurItemInfoFormServer(self, opNUID, res, volatileOnly):
        gamelog.debug('@zq onGetCurItemInfoFormServer', opNUID, res, volatileOnly, self.reqInfoStep)
        self.reqInfoStep -= 1
        self.setInfoToCurCache(opNUID, res, volatileOnly)
        if self.reqInfoStep <= 0:
            self.reqInfoStep = 0
            self.cancelTimeOutCB()
            if opNUID == uiConst.TABAUCTION_OPTYPE_SEARCH_MYSELL:
                result = self.getInfoFromCurCache(self.mySellData, opNUID)
                self.dealCompleteOpId(opNUID, result)
            elif opNUID == uiConst.TABAUCTION_OPTYPE_SEARCH_SAMESELL:
                result = self.getInfoFromCurCache(self.sameSellItemData, opNUID)
                self.dealCompleteOpId(opNUID, result)
            elif opNUID == uiConst.TABAUCTION_OPTYPE_SEARCH_BUY:
                result = self.getInfoFromCurCache(self.buyData, opNUID)
                self.dealCompleteOpId(opNUID, result)
            elif opNUID == uiConst.TABAUCTION_OPTYPE_SEARCH_MYBID:
                result = self.getInfoFromCurCache(self.myBidData, opNUID)
                self.dealCompleteOpId(opNUID, result)
            elif opNUID == uiConst.TABAUCTION_OPTYPE_SEARCH_MYCARE:
                result = self.getInfoFromCurCache(self.myCareData, opNUID)
                self.dealCompleteOpId(opNUID, result)
            elif opNUID == uiConst.TABAUCTION_OPTYPE_REFRESH_ITEMS:
                _data = {}
                self.setClearPreData(uiConst.TABAUCTION_OPTYPE_REFRESH_ITEMS, self.refreshDbIds, _data)
                result = self.getInfoFromCurCache(_data, uiConst.TABAUCTION_OPTYPE_REFRESH_ITEMS)
                self.dealCompleteOpId(uiConst.TABAUCTION_OPTYPE_REFRESH_ITEMS, result)

    def setInfoToCurCache(self, opNUID, res, volatileOnly):
        for k, v in res.iteritems():
            if v:
                if volatileOnly:
                    self.curTradeInfoCache[k]['bidderHostID'] = v[0]
                    self.curTradeInfoCache[k]['bidderName'] = v[1]
                    self.curTradeInfoCache[k]['latestPrice'] = v[2]
                    self.curTradeInfoCache[k]['followCount'] = v[3]
                    self.curTradeInfoCache[k]['criticalBidCount'] = v[4]
                    self.curTradeInfoCache[k]['followed'] = v[5]
                    self.curTradeInfoCache[k]['anonymous'] = v[6]
                    self.curTradeInfoCache[k]['time'] = utils.getNow()
                else:
                    self.curTradeInfoCache[k] = {'item': v[0],
                     'curDBID': v[1],
                     'vendorHostID': v[2],
                     'vendorName': v[3],
                     'bidderHostID': v[4],
                     'bidderName': v[5],
                     'latestPrice': v[6],
                     'beginDay': v[7],
                     'endDay': v[8],
                     'followCount': v[9],
                     'criticalBidCount': v[10],
                     'followed': v[11],
                     'anonymous': v[12],
                     'time': utils.getNow()}
            else:
                gamelog.debug('@zq   setInfoToCurCache no data ', k, v)
                dbIds = self.getDbIdList(opNUID)
                if k in dbIds:
                    dbIds.remove(k)
                data = self.getItemData(opNUID)
                if k in data:
                    del data[k]

    def getInfoFromHisCache(self, _info, opNUID):
        isHolyData = True
        p = BigWorld.player()
        needAllInfoDbIds = []
        for _dbId in _info.iterkeys():
            bNeedAllInfo = True
            itemData = self.historyInfoCache.get(_dbId, None)
            if itemData:
                if self.hasHisBaseData(itemData):
                    bNeedAllInfo = False
                    _info[_dbId] = copy.deepcopy(itemData)
            if bNeedAllInfo:
                needAllInfoDbIds.append(_dbId)
                _info[_dbId] = {}

        if needAllInfoDbIds:
            isHolyData = False
            self.reqInfoStep += 1
            p.base.getXConsignInfoByResultClrDBIDs(opNUID, needAllInfoDbIds)
        if not isHolyData:
            self.setTimeOutCB(Functor(self.getInfoTimeOut))
        return isHolyData

    def getDbIdList(self, opNUID):
        if opNUID == uiConst.TABAUCTION_OPTYPE_SEARCH_MYSELL:
            return self.mySellDbIds
        if opNUID == uiConst.TABAUCTION_OPTYPE_SEARCH_SAMESELL:
            return self.sameSellItemDbIds
        if opNUID == uiConst.TABAUCTION_OPTYPE_SEARCH_BUY:
            return self.buyDbIds
        if opNUID == uiConst.TABAUCTION_OPTYPE_SEARCH_MYBID:
            return self.myBidDbIds
        if opNUID == uiConst.TABAUCTION_OPTYPE_SEARCH_MYCARE:
            return self.myCareDbIds
        if opNUID == uiConst.TABAUCTION_OPTYPE_SEARCH_HISTORY:
            return self.historyDbIds
        if opNUID == uiConst.TABAUCTION_OPTYPE_REFRESH_ITEMS:
            return self.refreshDbIds
        return []

    def getItemData(self, opNUID):
        if opNUID == uiConst.TABAUCTION_OPTYPE_SEARCH_MYSELL:
            return self.mySellData
        if opNUID == uiConst.TABAUCTION_OPTYPE_SEARCH_SAMESELL:
            return self.sameSellItemData
        if opNUID == uiConst.TABAUCTION_OPTYPE_SEARCH_BUY:
            return self.buyData
        if opNUID == uiConst.TABAUCTION_OPTYPE_SEARCH_MYBID:
            return self.myBidData
        if opNUID == uiConst.TABAUCTION_OPTYPE_SEARCH_MYCARE:
            return self.myCareData
        if opNUID == uiConst.TABAUCTION_OPTYPE_SEARCH_HISTORY:
            return self.historyData
        return {}

    def hasHisBaseData(self, data):
        if 'opType' in data and 'isValid' in data and 'tValidate' in data and 'otherRole' in data and 'otherGBID' in data and 'otherHID' in data and 'relativeDBID' in data and 'price' in data and 'isCoin' in data and 'coinNum' in data and 'item' in data:
            return True
        return False

    def onGetHisItemInfoFormServer(self, opNUID, res):
        gamelog.debug('@zq onGetCurItemInfoFormServer', opNUID, res, self.reqInfoStep)
        self.reqInfoStep -= 1
        self.setInfoToHisCache(opNUID, res)
        if self.reqInfoStep <= 0:
            self.reqInfoStep = 0
            self.cancelTimeOutCB()
            if opNUID == uiConst.TABAUCTION_OPTYPE_SEARCH_HISTORY:
                result = self.getInfoFromHisCache(self.historyData, opNUID)
                self.dealCompleteOpId(opNUID, result)
            elif opNUID == uiConst.TABAUCTION_OPTYPE_PUSH_OVERBID:
                pushData = self.getLastPushMessageData(opNUID)
                result = self.getInfoFromHisCache(pushData, opNUID)
                self.dealCompleteOpId(opNUID, result)
            elif opNUID == uiConst.TABAUCTION_OPTYPE_PUSH_COINSOLD:
                pushData = self.getLastPushMessageData(opNUID)
                result = self.getInfoFromHisCache(pushData, opNUID)
                self.dealCompleteOpId(opNUID, result)
            elif opNUID == uiConst.TABAUCTION_OPTYPE_PUSH_FAIL2BID:
                pushData = self.getLastPushMessageData(opNUID)
                result = self.getInfoFromHisCache(pushData, opNUID)
                self.dealCompleteOpId(opNUID, result)

    def setInfoToHisCache(self, opNUID, res):
        for k, v in res.iteritems():
            if v:
                self.historyInfoCache[k] = {'opType': v[0],
                 'isValid': v[1],
                 'tValidate': v[2],
                 'otherRole': v[3],
                 'otherGBID': v[4],
                 'otherHID': v[5],
                 'relativeDBID': v[6],
                 'price': v[7],
                 'isCoin': v[8],
                 'coinNum': v[9],
                 'item': v[10]}
                gamelog.debug('@zq set HisCache', k)
            else:
                gamelog.debug('@zq setInfoToHisCache no data ', k, v)
                dbIds = self.getDbIdList(opNUID)
                if k in dbIds:
                    dbIds.remove(k)
                data = self.getItemData(opNUID)
                if k in data:
                    del data[k]
                curPushData = self.getCurPushData(opNUID)
                curPushData.clear()
                pmInfo = self.getPushMessageInfo(opNUID)
                for i, pData in enumerate(pmInfo):
                    if k == pData.get('clrDBID', None):
                        pmInfo.remove(pData)
                        break

    def dealCompleteOpId(self, opNUID, result):
        if not result:
            return
        if opNUID == uiConst.TABAUCTION_OPTYPE_SEARCH_MYSELL and self.tabIdx == SELL_PANEL:
            if not self.panelMc:
                return
            data = self.getSortData(self.mySellDbIds, self.curTradeInfoCache, self.mySellInfo)
            pagedItemInfo = self.getPagedData(data, self.mySellInfo.get('curPage', 1), self.mySellInfo.get('maxPage', 1))
            self.transItemInfo(self.mySellData)
            _info = {'itemDbIds': pagedItemInfo,
             'itemInfo': self.mySellData,
             'pageData': self.mySellInfo}
            self.panelMc.Invoke('setDetailItems', uiUtils.dict2GfxDict(_info, True))
            gamelog.debug('@zq MYSELL mission complete')
        elif opNUID == uiConst.TABAUCTION_OPTYPE_SEARCH_SAMESELL and self.tabIdx == SELL_PANEL:
            if not self.panelMc:
                return
            pagedItemInfo = self.getPagedData(self.sameSellItemDbIds, self.sameSellItemInfo.get('curPage', 1), self.sameSellItemInfo.get('maxPage', 1))
            self.transItemInfo(self.sameSellItemData)
            _info = {'itemDbIds': pagedItemInfo,
             'itemInfo': self.sameSellItemData,
             'pageData': self.sameSellItemInfo}
            self.panelMc.Invoke('setDetailItems', uiUtils.dict2GfxDict(_info, True))
            gamelog.debug('@zq SAMESELL mission complete')
        elif opNUID == uiConst.TABAUCTION_OPTYPE_SEARCH_BUY and self.tabIdx == BUY_PANEL:
            if not self.panelMc:
                return
            pagedItemInfo = self.getPagedData(self.buyDbIds, self.buyInfo.get('curPage', 1), self.buyInfo.get('maxPage', 1))
            self.transItemInfo(self.buyData)
            _info = {'itemDbIds': pagedItemInfo,
             'itemInfo': self.buyData,
             'pageData': self.buyInfo}
            self.panelMc.Invoke('setDetailItems', uiUtils.dict2GfxDict(_info, True))
            gamelog.debug('@zq buy mission complete')
        elif opNUID == uiConst.TABAUCTION_OPTYPE_SEARCH_MYBID and self.tabIdx == BID_PANEL:
            if not self.panelMc:
                return
            data = self.getSortData(self.myBidDbIds, self.curTradeInfoCache, self.myBidInfo)
            pagedItemInfo = self.getPagedData(data, self.myBidInfo.get('curPage', 1), self.myBidInfo.get('maxPage', 1))
            self.transItemInfo(self.myBidData)
            _info = {'itemDbIds': pagedItemInfo,
             'itemInfo': self.myBidData,
             'pageData': self.myBidInfo}
            self.panelMc.Invoke('setDetailItems', uiUtils.dict2GfxDict(_info, True))
            gamelog.debug('@zq MYBID mission complete')
        elif opNUID == uiConst.TABAUCTION_OPTYPE_SEARCH_MYCARE and self.tabIdx == CARE_PANEL:
            if not self.panelMc:
                return
            data = self.getSortData(self.myCareDbIds, self.curTradeInfoCache, self.myCareInfo)
            pagedItemInfo = self.getPagedData(data, self.myCareInfo.get('curPage', 1), self.myCareInfo.get('maxPage', 1))
            self.transItemInfo(self.myCareData)
            _info = {'itemDbIds': pagedItemInfo,
             'itemInfo': self.myCareData,
             'pageData': self.myCareInfo}
            self.panelMc.Invoke('setDetailItems', uiUtils.dict2GfxDict(_info, True))
            gamelog.debug('@zq MYCare mission complete')
        elif opNUID == uiConst.TABAUCTION_OPTYPE_SEARCH_HISTORY and self.tabIdx == TRADE_HISTORY_PANEL:
            if not self.panelMc:
                return
            data = self.historyDbIds
            pagedItemInfo = self.getPagedData(data, self.historyInfo.get('curPage', 1), self.historyInfo.get('maxPage', 1))
            self.transHisItemInfo(self.historyData)
            _info = {'itemDbIds': pagedItemInfo,
             'itemInfo': self.historyData,
             'pageData': self.historyInfo}
            self.panelMc.Invoke('setDetailItems', uiUtils.dict2GfxDict(_info, True))
            gamelog.debug('@zq history mission complete')
        elif opNUID == uiConst.TABAUCTION_OPTYPE_PUSH_OVERBID:
            self.closeAllPushUI(uiConst.TABAUCTION_OPTYPE_PUSH_OVERBID)
            self.showBidFailedPanel()
            gamelog.debug('@zq PUSH_OVERBID mission complete')
        elif opNUID == uiConst.TABAUCTION_OPTYPE_PUSH_COINSOLD:
            self.closeAllPushUI(uiConst.TABAUCTION_OPTYPE_PUSH_COINSOLD)
            self.showSellSuccessPanel()
            gamelog.debug('@zq PUSH_COINSOLD mission complete')
        elif opNUID == uiConst.TABAUCTION_OPTYPE_PUSH_FAIL2BID:
            self.closeAllPushUI(uiConst.TABAUCTION_OPTYPE_PUSH_FAIL2BID)
            self.showSubmitFailedPanel()
            gamelog.debug('@zq PUSH_FAIL2BID mission complete')
        elif opNUID == uiConst.TABAUCTION_OPTYPE_REFRESH_ITEMS:
            for _dbIds in self.refreshDbIds:
                self.refreshOneCurItems(_dbIds)

            self.refreshDbIds = []
            gamelog.debug('@zq FORCE_REFRESH_ITEMS mission complete')

    def calcPageData(self, dataList, pageInfo):
        maxPage = len(dataList) / ITEM_NUM_PER_PAGE
        if len(dataList) % ITEM_NUM_PER_PAGE:
            maxPage += 1
        pageInfo['maxPage'] = maxPage
        if pageInfo.get('resetPage', False):
            pageInfo['curPage'] = 1
        else:
            if pageInfo.get('curPage', 0) < 1:
                pageInfo['curPage'] = 1
            if pageInfo.get('curPage', 0) > maxPage:
                pageInfo['curPage'] = maxPage
            pageInfo['resetPage'] = True

    def getPagedData(self, dataList, curPage, maxPage):
        idx1 = (curPage - 1) * ITEM_NUM_PER_PAGE
        idx2 = curPage * ITEM_NUM_PER_PAGE
        return dataList[idx1:idx2]

    def getSortData(self, dbIdList, dataInfo, panelInfo):
        sortType = panelInfo.get('sortType', 0)
        sortOrderType = panelInfo.get('sortOrderType', 1)
        isSinglePrice = panelInfo.get('isSinglePrice', False)
        if not sortType or not sortOrderType or not dbIdList:
            return dbIdList
        gamelog.debug('@zq sortType', sortType, sortOrderType, dbIdList)

        def _cmp(a, b):
            if a > b:
                return 1
            if a < b:
                return -1
            return 0

        reverse = sortOrderType != const.XCONSIGN_ORDER_TYPE_INC
        if sortType == 'qualityBtn':

            def _genKey(dbId):
                item = dataInfo.get(dbId, {}).get('item', None)
                if item:
                    return item.quality
                else:
                    return 0

        elif sortType == 'nameBtn':

            def _genKey(dbId):
                item = dataInfo.get(dbId, {}).get('item', None)
                if item:
                    return item.id
                else:
                    return 0

        elif sortType == 'lvBtn':

            def _genKey(dbId):
                item = dataInfo.get(dbId, {}).get('item', None)
                if item:
                    return item.lvReq
                else:
                    return 0

        elif sortType == 'timeBtn':

            def _genKey(dbId):
                endDay = dataInfo.get(dbId, {}).get('endDay', 0)
                return endDay

        elif sortType == 'playerBtn':
            pass
        elif sortType == 'priceBtn':

            def _genKey(dbId):
                latestPrice = dataInfo.get(dbId, {}).get('latestPrice', None)
                if isSinglePrice:
                    item = dataInfo.get(dbId, {}).get('item', None)
                    latestPrice = int(latestPrice / item.cwrap)
                return latestPrice

        elif sortType == 'bidPriceBtn':
            pass
        elif sortType == 'stateBtn':
            pass
        elif sortType == 'careBtn':

            def _genKey(dbId):
                followCount = dataInfo.get(dbId, {}).get('followCount', None)
                return followCount

        dbIdList.sort(cmp=_cmp, key=_genKey, reverse=reverse)
        gamelog.debug('@zq dbIdList', dbIdList)
        return dbIdList

    def onXConsignItemRes(self, _dbId):
        if _dbId not in self.mySellDbIds:
            self.removeItem(1, 99)
            self.mySellDbIds.append(_dbId)
            self.onXConsignSellingDBIDs(uiConst.TABAUCTION_OPTYPE_SEARCH_MYSELL, self.mySellDbIds)

    def onXConsignWithdrawRes(self, _dbId):
        if _dbId in self.sameSellItemDbIds:
            self.sameSellItemDbIds.remove(_dbId)
            if self.pageSrc != -1 and self.posSrc != -1:
                self.onSearchXConsignByID(uiConst.TABAUCTION_OPTYPE_SEARCH_SAMESELL, self.sameSellItemDbIds)
        if _dbId in self.mySellDbIds:
            self.mySellDbIds.remove(_dbId)
            if self.pageSrc == -1 and self.posSrc == -1:
                self.onXConsignSellingDBIDs(uiConst.TABAUCTION_OPTYPE_SEARCH_MYSELL, self.mySellDbIds)

    def transItemInfo(self, _info):
        p = BigWorld.player()
        for k, v in _info.iteritems():
            if self.tabIdx == BUY_PANEL or self.tabIdx == SELL_PANEL:
                _length = 6
            else:
                _length = 8
            v['itemName'] = uiUtils.getItemColorNameByItem(v['item'], length=_length)
            v['itemLv'] = v['item'].lvReq
            v['hasBidder'] = v['bidderName']
            v['bidderIsMe'] = v['bidderHostID'] == int(gameglobal.rds.g_serverid) and v['bidderName'] == p.roleName
            v['vendorIsMe'] = v['vendorHostID'] == int(gameglobal.rds.g_serverid) and v['vendorName'] == p.roleName
            v['canUseNow'] = v['item'].canUseNow(p.physique.sex, p.physique.school, p.physique.bodyType, p.lv, p)
            v['item'] = uiUtils.getGfxItem(v['item'])
            nowday = int(utils.getNow() / 86400)
            v['dayBeginTime'], v['dayEndTime'] = self.getBeginEndTimeDay(v['criticalBidCount'], nowday == v['endDay'])
            v['timeStr'] = [gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_1918, gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_1918_1, gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_1918_2]
            v['ftimeStr'] = [gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_1918, gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_1919, gameStrings.TEXT_EXPBONUSPROXY_79_1]
            v['followStr'] = gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_1920
            v['bidStr'] = [gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_364, gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_367]
            v['pubStr'] = [gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_1922]
            v['deadStr'] = [gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_1923]
            v['bidderServerName'] = utils.getServerName(v['bidderHostID'])
            v['vendorServerName'] = gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_1925 % utils.getServerName(v['vendorHostID'])
            v['care_max_cnt'] = CARE_MAX_CNT
            endDayCount = v['endDay'] - nowday
            _mins = int(v['dayEndTime'] / 60)
            _hours = _mins / 60 % 24
            _mins = _mins % 60
            dayStr = [gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_1931,
             gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_1931_1,
             gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_1931_2,
             gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_1931_3]
            holdDayStr = [gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_376, gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_376_1, gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_376_2]
            v['holdDayStr'] = holdDayStr[v['endDay'] - v['beginDay']]
            v['sellDeadStr'] = gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_1934 % (dayStr[endDayCount], _hours, _mins)
            v['specialPropLen'] = 0

    def transHisItemInfo(self, _info):
        p = BigWorld.player()
        for k, v in _info.iteritems():
            typeStr = ''
            if v['opType'] == const.XCONSIGN_OP_TYPE_BOUGHT:
                typeStr = uiUtils.toHtml(gameStrings.TEXT_PLAYRECOMMSTRONGERPROXY_990, '#aa7acc')
            if v['opType'] == const.XCONSIGN_OP_TYPE_COINSOLD:
                typeStr = uiUtils.toHtml(gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_1944, '#FFBF66')
            v['typeStr'] = typeStr
            v['isShow'] = True if typeStr else False
            v['itemName'] = '<u>%s</u>' % uiUtils.getItemColorNameByItem(v['item'], length=7)
            v['singlePrice'] = int(v['price'] / v['item'].cwrap)
            v['num'] = v['item'].cwrap
            v['coin'] = 0
            v['time'] = time.strftime('%Y-%m-%d %H:%M:%S', utils.localtimeEx(v['tValidate']))
            v['uuid'] = v['item'].uuid.encode('hex')
            v['location'] = const.ITEM_IN_CROSS_CONSIGN_HISTORY
            v['item'] = None

    def getBeginEndTimeDay(self, bidCount, isEndDay = False):
        dayBeginTime = CCCD.data.get('xConsignTime2PubEnd', 1859) + 1
        dayEndTime = CCCD.data.get('xConsignTime3BidEnd', 2059) + 1
        finalTime = CCCD.data.get('xConsignTime4PostEnd', 2259) + 1
        dayBeginTime = self.getTimeSec(dayBeginTime)
        dayEndTime = self.getTimeSec(dayEndTime)
        if isEndDay:
            dayEndTime += bidCount * 60
        finalTime = self.getTimeSec(finalTime)
        return (dayBeginTime, min(dayEndTime, finalTime))

    def getTimeSec(self, data):
        _hours = int(data / 100)
        _min = int(data % 100)
        _time = _hours * 60 * 60 + _min * 60
        return _time

    def _getXConsignMaxUnitPrice(self):
        return CCCD.data.get('crossConsignMaxUnitPrice', 9999999)

    def _getXConsignMinUnitPrice(self):
        return CCCD.data.get('crossConsignMinUnitPrice', 1000)

    def _getXConsignMaxTotalPrice(self):
        return CCCD.data.get('crossConsignMaxTotalPrice', 99999999)

    def _getXConsignMinTotalPrice(self):
        return CCCD.data.get('crossConsignMinTotalPrice', 1000)

    def _getLowestUnitPriceOfItem(self, itemID):
        return ID.data.get(itemID, {}).get('crossConsignLowest', self._getXConsignMinUnitPrice())

    def onGetPriceLimit(self, *arg):
        info = {'maxUnitPrice': self._getXConsignMaxUnitPrice(),
         'minUnitPrice': self._getLowestUnitPriceOfItem(None),
         'maxTotalPrice': self._getXConsignMaxTotalPrice(),
         'minTotalPrice': self._getXConsignMinTotalPrice()}
        return uiUtils.dict2GfxDict(info, True)

    def onCareItem(self, *arg):
        dbId = int(arg[3][0].GetNumber())
        _data = copy.deepcopy(self.curTradeInfoCache.get(dbId, None))
        if self.hasCurBaseData(_data):
            e = self._getEntity()
            if _data.get('followed', False):
                e.cell.reqXConsignCancelFollow(_data['item'].id, dbId)
            else:
                e.cell.reqXConsignFollow(_data['item'].id, dbId)

    def onXConsignFollowDone(self, curDBID, newFollowCount):
        _data = self.curTradeInfoCache.get(curDBID, None)
        if self.hasCurBaseData(_data):
            _data['followed'] = True
            _data['followCount'] = newFollowCount
        if curDBID not in self.myCareDbIds:
            self.myCareDbIds.append(curDBID)
            self.onXConsignFollowingDBIDs(uiConst.TABAUCTION_OPTYPE_SEARCH_MYCARE, self.myCareDbIds)
        if self.tabIdx == CARE_PANEL:
            self.refreshItems()
        elif self.tabIdx != TRADE_HISTORY_PANEL:
            self.refreshOneCurItems(curDBID)

    def onXConsignCancelFollowDone(self, curDBID, newFollowCount):
        _data = self.curTradeInfoCache.get(curDBID, None)
        if self.hasCurBaseData(_data):
            _data['followed'] = False
            _data['followCount'] = newFollowCount
        if curDBID in self.myCareDbIds:
            self.myCareDbIds.remove(curDBID)
            self.onXConsignFollowingDBIDs(uiConst.TABAUCTION_OPTYPE_SEARCH_MYCARE, self.myCareDbIds)
        if self.tabIdx == CARE_PANEL:
            self.refreshItems()
        elif self.tabIdx != TRADE_HISTORY_PANEL:
            self.refreshOneCurItems(curDBID)

    def refreshOneCurItemWithUpdate(self, _dbIds):
        gamelog.debug('@zq refreshOneCurItemWithUpdate', _dbIds)
        self.refreshDbIds = list(_dbIds)
        _data = {}
        self.setForceRefreshPreData(uiConst.TABAUCTION_OPTYPE_REFRESH_ITEMS, self.refreshDbIds, _data)
        result = self.getInfoFromCurCache(_data, uiConst.TABAUCTION_OPTYPE_REFRESH_ITEMS)
        self.dealCompleteOpId(uiConst.TABAUCTION_OPTYPE_REFRESH_ITEMS, result)

    def setForceRefreshPreData(self, opNUID, listCurDBID, _info):
        _info.clear()
        for _dbId in listCurDBID:
            _info[_dbId] = {'forceRefresh': True}

    def refreshOneCurItems(self, _dbId):
        gamelog.debug('@zq refreshOneCurItems')
        itemData = copy.deepcopy(self.curTradeInfoCache.get(_dbId, None))
        if not itemData:
            return
        else:
            if self.panelMc:
                _info = {_dbId: itemData}
                self.transItemInfo(_info)
                self.panelMc.Invoke('setRefreshSelectedItem', (uiUtils.dict2GfxDict(itemData, True), GfxValue(_dbId)))
            return

    def showBidPanel(self):
        if self.bidMediator:
            self.bidMediator.Invoke('refreshItemInfo', (self.onGetMinBidPrice(), self.onGetBuyItemInfo()))
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_TAB_CROSS_SERVER_BID)

    def closeBidPanel(self):
        self.bidMediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_TAB_CROSS_SERVER_BID)

    def onCloseBidPanel(self, *arg):
        self.closeBidPanel()

    def showBidFailedPanel(self):
        if self.bidFailedMediator:
            gamelog.debug('@zq bidFailedMediator already')
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_TAB_CROSS_SERVER_BID_FAILED)

    def closeBidFailedPanel(self):
        self.bidFailedMediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_TAB_CROSS_SERVER_BID_FAILED)

    def onCloseBidFailedPanel(self, *arg):
        self.closeBidFailedPanel()

    def showSellSuccessPanel(self):
        if self.sellSuccessMediator:
            gamelog.debug('@zq sellSuccessMediator already')
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_TAB_CROSS_SERVER_SELL_SUCCESS)

    def closeSellSuccessPanel(self):
        self.sellSuccessMediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_TAB_CROSS_SERVER_SELL_SUCCESS)

    def onCloseSellSuccessPanel(self, *arg):
        self.closeSellSuccessPanel()

    def showSubmitFailedPanel(self):
        if self.submitFailedMediator:
            gamelog.debug('@zq submitFailedMediator already')
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_TAB_CROSS_SERVER_SUBMIT_FAILED)

    def closeSubmitFailedPanel(self):
        self.submitFailedMediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_TAB_CROSS_SERVER_SUBMIT_FAILED)

    def onCloseSubmitFailedPanel(self, *arg):
        self.closeSubmitFailedPanel()

    def onGetMinBidPrice(self, *arg):
        bidPrice = 0
        if self.curDbId:
            itemData = copy.deepcopy(self.curTradeInfoCache.get(self.curDbId, {}))
            bidPrice = itemData.get('latestPrice', 0) if not itemData.get('bidderName') else itemData.get('latestPrice', 0) * const.XCONSIGN_PRICE_HIGHER_RATIO
        return GfxValue(math.ceil(bidPrice))

    def onGetBuyItemInfo(self, *arg):
        itemData = {}
        if self.curDbId:
            itemData = copy.deepcopy(self.curTradeInfoCache.get(self.curDbId, None))
            if itemData:
                item = itemData['item']
                itemData['item'] = uiUtils.getGfxItem(itemData['item'])
                itemData['item']['name'] = uiUtils.getItemColorNameByItem(item)
                itemData['item']['dbId'] = self.curDbId
                itemData['item']['isAnony'] = self.anonymousCache.get(self.curDbId)
                gamelog.debug('@zq itemData', itemData)
        return uiUtils.dict2GfxDict(itemData, True)

    def onConfirmBid(self, *arg):
        p = BigWorld.player()
        price = int(arg[3][0].GetString())
        anonymous = arg[3][1].GetBool()
        if price == 0:
            p.showGameMsg(GMDD.data.CROSS_CONSIGN_BID_PRICE_NULL, ())
            return
        else:
            if utils.getTimeZone() == gameglobal.SERVER_TIME_ZONE:
                _endDay = self.curTradeInfoCache.get(self.curDbId, {}).get('endDay', 0)
                _bidCount = self.curTradeInfoCache.get(self.curDbId, {}).get('criticalBidCount', 0)
                nowday = int(utils.getNow() / 86400)
                dayBeginTime, dayEndTime = self.getBeginEndTimeDay(_bidCount, nowday == _endDay)
                tmpT = utils.localtimeEx(utils.getNow())
                _time = tmpT.tm_hour * 60 * 60 + tmpT.tm_min * 60 + tmpT.tm_sec
                if _time < dayBeginTime or _time > dayEndTime:
                    p.showGameMsg(GMDD.data.XCONSIGN_TIME_ERROR, ())
                    return
            e = self._getEntity()
            if e:
                item = copy.deepcopy(self.curTradeInfoCache.get(self.curDbId, {}).get('item', None))
                if item:
                    self.anonymousCache[self.curDbId] = anonymous
                    self._confirmBid(e, item, self.curDbId, price, anonymous)
            return

    @ui.checkInventoryLock()
    def _confirmBid(self, entity, item, DbId, price, anonymous = False):
        entity.cell.reqXConsignBid(item.id, DbId, price, BigWorld.player().cipherOfPerson, anonymous)
        self.closeBidPanel()

    def onXConsignBidRes(self, curDBID):
        _data = self.curTradeInfoCache.get(curDBID, None)
        if self.hasCurBaseData(_data):
            _data['time'] = 0
        if curDBID not in self.myBidDbIds:
            self.myBidDbIds.append(curDBID)
            self.onXConsignBiddingDBIDs(uiConst.TABAUCTION_OPTYPE_SEARCH_MYBID, self.myBidDbIds)
        self.refreshItems()

    def setStateTxt(self):
        dayBeginTime, dayEndTime = self.getBeginEndTimeDay(0)
        tmpT = utils.localtimeEx(utils.getNow())
        _time = tmpT.tm_hour * 60 * 60 + tmpT.tm_min * 60 + tmpT.tm_sec
        dayBegin = CCCD.data.get('xConsignTime2PubEnd', 1859) + 1
        _hours, _min = self.transTime(dayBegin)
        tmptxt = ''
        state = 0
        if _time < dayBeginTime:
            tmptxt = gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_2193 % (_hours, _min)
            state = 'shijian'
        elif _time > dayEndTime:
            tmptxt = gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_2196 % (_hours, _min)
            state = 'shijian'
        else:
            tmptxt = gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_2199
            state = 'kaishi'
        if self.panelMc:
            self.panelMc.Invoke('setStateTxt', (GfxValue(gbk2unicode(tmptxt)), GfxValue(gbk2unicode(state))))
            self.setTimeCheckCB(self.setStateTxt)

    def openXConsignPushMessage(self, opNUID):
        pushMessageInfo = self.getPushMessageInfo(opNUID)
        if pushMessageInfo:
            pushData = self.getLastPushMessageData(opNUID)
            gamelog.debug('@zq openXConsignPushMessage', pushData)
            item = pushMessageInfo[len(pushMessageInfo) - 1]
            opType = item['opType']
            if opType == const.XCONSIGN_OP_TYPE_OVERBID:
                result = self.getInfoFromHisCache(pushData, uiConst.TABAUCTION_OPTYPE_PUSH_OVERBID)
                self.dealCompleteOpId(uiConst.TABAUCTION_OPTYPE_PUSH_OVERBID, result)
            elif opType == const.XCONSIGN_OP_TYPE_COINSOLD:
                result = self.getInfoFromHisCache(pushData, uiConst.TABAUCTION_OPTYPE_PUSH_COINSOLD)
                self.dealCompleteOpId(uiConst.TABAUCTION_OPTYPE_PUSH_COINSOLD, result)
            elif opType == const.XCONSIGN_OP_TYPE_FAIL2BID:
                self.closeAllPushUI(uiConst.TABAUCTION_OPTYPE_PUSH_FAIL2BID)
                self.showSubmitFailedPanel()
        else:
            gamelog.debug('@zq openXConsignPushMessage pushMessageInfo null')

    def getLastPushMessageData(self, opNUID):
        curPushData = self.getCurPushData(opNUID)
        pmInfo = self.getPushMessageInfo(opNUID)
        if pmInfo:
            item = pmInfo[len(pmInfo) - 1]
            pushDbIds = [item['clrDBID']]
            self.setClearPreData(None, pushDbIds, curPushData)
        return curPushData

    def getPushMessageInfo(self, opNUID):
        if opNUID == uiConst.TABAUCTION_OPTYPE_PUSH_OVERBID:
            return self.bidFailedPushMessageInfo
        if opNUID == uiConst.TABAUCTION_OPTYPE_PUSH_COINSOLD:
            return self.sellSuccessPushMessageInfo
        if opNUID == uiConst.TABAUCTION_OPTYPE_PUSH_FAIL2BID:
            return self.submitFailedPushMessageInfo
        return []

    def getPushMessageInfoByMsgType(self, msgType):
        if msgType == uiConst.MESSAGE_TYPE_XCONSIGN_BID_FAILED:
            return self.bidFailedPushMessageInfo
        if msgType == uiConst.MESSAGE_TYPE_XCONSIGN_SELL_SUCCESS:
            return self.sellSuccessPushMessageInfo
        if msgType == uiConst.MESSAGE_TYPE_XCONSIGN_SUBMIT_FAILED:
            return self.submitFailedPushMessageInfo
        return []

    def getMsgInfoByMsgType(self, msgType):
        pushMessageInfo = self.getPushMessageInfoByMsgType(msgType)
        cnt = len(pushMessageInfo)
        pmd = PMD.data.get(msgType, {})
        msgInfo = {'iconId': pmd.get('iconId', 0),
         'tooltip': pmd.get('tooltip', '%d') % cnt}
        return msgInfo

    def getCurPushData(self, opNUID):
        if opNUID == uiConst.TABAUCTION_OPTYPE_PUSH_OVERBID:
            return self.curBidFailedPushData
        if opNUID == uiConst.TABAUCTION_OPTYPE_PUSH_COINSOLD:
            return self.curSellSuccessPushData
        if opNUID == uiConst.TABAUCTION_OPTYPE_PUSH_FAIL2BID:
            return self.curSubmitFailedPushData
        return {}

    def closeAllPushUI(self, opNUID):
        if opNUID == uiConst.TABAUCTION_OPTYPE_PUSH_OVERBID:
            self.closeBidFailedPanel()
        elif opNUID == uiConst.TABAUCTION_OPTYPE_PUSH_COINSOLD:
            self.closeSellSuccessPanel()
        elif opNUID == uiConst.TABAUCTION_OPTYPE_PUSH_FAIL2BID:
            self.closeSubmitFailedPanel()
        else:
            self.closeBidFailedPanel()
            self.closeSellSuccessPanel()
            self.closeSubmitFailedPanel()

    def onGetPushData(self, *arg):
        opNUID = int(arg[3][0].GetNumber())
        _data = {}
        if opNUID == uiConst.TABAUCTION_OPTYPE_PUSH_OVERBID:
            curPushData = self.getCurPushData(opNUID)
            _data = self.transPushDataInfo(curPushData)
        elif opNUID == uiConst.TABAUCTION_OPTYPE_PUSH_COINSOLD:
            curPushData = self.getCurPushData(opNUID)
            _data = self.transPushDataInfo(curPushData)
        elif opNUID == uiConst.TABAUCTION_OPTYPE_PUSH_FAIL2BID:
            pmInfo = self.getPushMessageInfo(uiConst.TABAUCTION_OPTYPE_PUSH_FAIL2BID)
            if pmInfo:
                _data = pmInfo[-1]
        return uiUtils.dict2GfxDict(_data, True)

    def transPushDataInfo(self, _data):
        for k, v in _data.iteritems():
            v['num'] = v['item'].cwrap
            v['uuid'] = v['item'].uuid.encode('hex')
            v['location'] = const.ITEM_IN_CROSS_CONSIGN_HISTORY
            v['itemName'] = uiUtils.getItemColorNameByItem(v['item'])
            v['itemLv'] = v['item'].lvReq
            v['item'] = uiUtils.getGfxItem(v['item'], location=const.ITEM_IN_CROSS_CONSIGN_HISTORY)
            return v

    @ui.callFilter(1)
    def onReceivePushCoin(self, *arg):
        opNUID = int(arg[3][0].GetNumber())
        isOpenBidPanel = arg[3][1].GetBool()
        pushMessageInfo = self.getPushMessageInfo(opNUID)
        p = BigWorld.player()
        if formula.inIsolatedMap(p.spaceNo):
            self.closeAllPushUI(opNUID)
            p.showGameMsg(GMDD.data.XCONSIGN_NOT_AVAIL_IN_ISOLATED_MAP, ())
            return
        if pushMessageInfo:
            item = pushMessageInfo[len(pushMessageInfo) - 1]
            p.base.doFetchXConsignCoin(item['opType'], item['coinNum'], item['clrDBID'], item['itemId'])
            pushMessageInfo.pop()
            self.closeAllPushUI(opNUID)
            if isOpenBidPanel:
                gameglobal.rds.ui.tabAuction.show(uiConst.TABAUCTION_TAB_CROSS_SERVER, 2)
        self.checkPushMessage(opNUID)

    def checkPushMessage(self, opNUID):
        pushMessageInfo = self.getPushMessageInfo(opNUID)
        if not pushMessageInfo:
            if opNUID == uiConst.TABAUCTION_OPTYPE_PUSH_OVERBID:
                gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_XCONSIGN_BID_FAILED)
            elif opNUID == uiConst.TABAUCTION_OPTYPE_PUSH_COINSOLD:
                gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_XCONSIGN_SELL_SUCCESS)
            elif opNUID == uiConst.TABAUCTION_OPTYPE_PUSH_FAIL2BID:
                gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_XCONSIGN_SUBMIT_FAILED)
            self.closeAllPushUI(opNUID)
        elif opNUID == uiConst.TABAUCTION_OPTYPE_PUSH_OVERBID:
            msgInfo = self.getMsgInfoByMsgType(uiConst.MESSAGE_TYPE_XCONSIGN_BID_FAILED)
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_XCONSIGN_BID_FAILED, msgInfo=msgInfo)
        elif opNUID == uiConst.TABAUCTION_OPTYPE_PUSH_COINSOLD:
            msgInfo = self.getMsgInfoByMsgType(uiConst.MESSAGE_TYPE_XCONSIGN_SELL_SUCCESS)
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_XCONSIGN_SELL_SUCCESS, msgInfo=msgInfo)
        elif opNUID == uiConst.TABAUCTION_OPTYPE_PUSH_FAIL2BID:
            msgInfo = self.getMsgInfoByMsgType(uiConst.MESSAGE_TYPE_XCONSIGN_SUBMIT_FAILED)
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_XCONSIGN_SUBMIT_FAILED, msgInfo=msgInfo)

    def onGetBidMaxNum(self, *arg):
        bidMaxNum = CCCD.data.get('crossConsignMaxPrice', 0)
        gamelog.debug('@zq onGetBidMaxNum', bidMaxNum)
        return GfxValue(bidMaxNum)

    def onGetSelectedTips(self, *arg):
        timeType = int(arg[3][0].GetNumber())
        dayBeginTime, dayEndTime = self.getBeginEndTimeDay(0)
        tmpT = utils.localtimeEx(utils.getNow())
        _time = tmpT.tm_hour * 60 * 60 + tmpT.tm_min * 60 + tmpT.tm_sec
        preTime = CCCD.data.get('xConsignTime1UpEnd', 1829) + 1
        _preTimeHours, _preTimeMin = self.transTime(preTime)
        dayBegin = CCCD.data.get('xConsignTime2PubEnd', 1859) + 1
        _dayBeginHours, _dayBeginMin = self.transTime(dayBegin)
        dayEnd = CCCD.data.get('xConsignTime3BidEnd', 2059) + 1
        _dayEndHours, _dayEndMin = self.transTime(dayEnd)
        preTimeSec = self.getTimeSec(preTime)
        tmptxt = ''
        tmpPretxt = ''
        state = 0
        if _time < preTimeSec:
            tmptxt = SELECTEDTIPS[0, timeType] % (_dayBeginHours,
             _dayBeginMin,
             _dayEndHours,
             _dayEndMin)
            tmpPretxt = gameStrings.TEXT_TABAUCTIONCROSSSERVERPROXY_2378 % (_preTimeHours, _preTimeMin)
        else:
            tmptxt = SELECTEDTIPS[1, timeType] % (_dayBeginHours,
             _dayBeginMin,
             _dayEndHours,
             _dayEndMin)
        info = {'selectedTips': tmptxt,
         'preTips': tmpPretxt}
        return uiUtils.dict2GfxDict(info, True)

    def transTime(self, _time):
        _hours = int(_time / 100)
        _min = int(_time % 100)
        while _min >= 60:
            _min -= 60
            _hours += 1

        return (_hours, _min)

    def shortKeyDown(self, key):
        if self.bidMediator:
            if key == keys.KEY_Y:
                self.bidMediator.Invoke('handleConfirm')
            else:
                self.closeBidPanel()

    def onGetHasRegionQuery(self, *args):
        xConsignRegionId = RSCD.data.get(int(gameglobal.rds.g_serverid), {}).get('xConsignRegionId', 0)
        if xConsignRegionId:
            return GfxValue(True)
        return GfxValue(False)

    def onOpenRegionQueryPanel(self, *args):
        gameglobal.rds.ui.tabAuctionCrossServerRegion.show()

    def onGetServerTimezone(self, *args):
        return GfxValue(gameglobal.SERVER_TIME_ZONE)

    @ui.callFilter(2)
    def onCommonRefreshBtn(self, *args):
        self.refreshItems(commonRefresh=True)

    def onSaveFilterSetting(self, *args):
        pass

    def onGetSelectedCateName(self, *args):
        cate = args[3][0].GetString().strip().split(',')
        isSchool = args[3][1].GetBool()
        category = -1
        subcategory = -1
        school = -1
        if len(cate) > 0 and cate[0]:
            category = int(cate[0])
            if len(cate) > 1:
                subcategory = int(cate[1])
            if len(cate) > 2:
                if isSchool:
                    school = int(cate[2])
        nameStr = self._getSelectedCateName(category, subcategory, school, isSchool)
        return GfxValue(gbk2unicode(nameStr))

    def _getSelectedCateName(self, category, subCategory, schoolIdx, isSchool):
        cateStr = ''
        categoryName = ''
        subCategoryName = ''
        if subCategory != -1:
            cData = ICD.data.get((category, subCategory), {})
            categoryName = cData.get('categoryName', '')
            subCategoryName = cData.get('subCategoryName', '')
        elif category != -1:
            for k, v in ICD.data.iteritems():
                if len(k) == 2:
                    _cate, _subCate = k
                    if _cate == category:
                        categoryName = v.get('categoryName', ())
                        break

        cateArr = []
        if categoryName:
            cateArr += [gameStrings.CROSS_CONSIGN_FILTER_CATE_PREFIX, categoryName]
            if subCategoryName:
                cateArr += [gameStrings.CROSS_CONSIGN_FILTER_CATE_SEPARATOR, subCategoryName]
                if isSchool:
                    schoolName = const.SCHOOL_DICT.get(schoolIdx, '')
                    if schoolName:
                        cateArr += [gameStrings.CROSS_CONSIGN_FILTER_CATE_SEPARATOR, schoolName]
        if not cateArr:
            cateArr = [gameStrings.CROSS_CONSIGN_FILTER_CATE_NONE]
        cateStr = ''.join(cateArr)
        return cateStr

    def onGetFilterSearchType(self, *arg):
        cate = arg[3][0].GetString().strip().split(',')
        name = arg[3][1].GetString().strip()
        if name:
            name = unicode2gbk(name)
        ret = []
        subcategory = -1
        category = -1
        if len(cate) > 0 and cate[0]:
            category = int(cate[0])
            if len(cate) > 1:
                subcategory = int(cate[1])
        ret = [{'label': gameStrings.CROSS_CONSIGN_FILTER_NONE,
          'data': 0}, {'label': self.getFSTLabel(const.XCONSIGN_FILTER_TYPE_RPROP),
          'data': const.XCONSIGN_FILTER_TYPE_RPROP}]
        isManual, isFubenEquip, isYaopei = self.filterTypeCache.get((name, category, subcategory), (None, None, None))
        if isYaopei == None:
            isYaopei = False
            if name:
                isYaopei = self.processItemByName(name, school=-1, forme=False, mType=category, sType=subcategory, isYaopei=True)
            elif subcategory != -1:
                cData = ICD.data.get((category, subcategory), {})
                filterYaopeiProp = cData.get('filterYaopeiProp', ())
                filterYaopeiSkill = cData.get('filterYaopeiSkill', ())
                if filterYaopeiProp or filterYaopeiSkill:
                    isYaopei = True
            elif category != -1:
                for k, v in ICD.data.iteritems():
                    if len(k) == 2:
                        _cate, _subCate = k
                        if _cate == category:
                            filterYaopeiProp = v.get('filterYaopeiProp', ())
                            filterYaopeiSkill = v.get('filterYaopeiSkill', ())
                            if filterYaopeiProp or filterYaopeiSkill:
                                isYaopei = True
                                break

        if isManual == None:
            isManual = False
            if name:
                isManual = self.processItemByName(name, school=-1, forme=False, mType=category, sType=subcategory, isManual=True)
            elif subcategory != -1:
                cData = ICD.data.get((category, subcategory), {})
                filterSpeicalEffect = cData.get('filterSpeicalEffect', ())
                if filterSpeicalEffect:
                    isManual = True
            elif category != -1:
                for k, v in ICD.data.iteritems():
                    if len(k) == 2:
                        _cate, _subCate = k
                        if _cate == category:
                            filterSpeicalEffect = v.get('filterSpeicalEffect', ())
                            if filterSpeicalEffect:
                                isManual = True
                                break

        if isFubenEquip == None:
            isFubenEquip = False
            if name:
                isFubenEquip = self.processItemByName(name, school=-1, forme=False, mType=category, sType=subcategory, isFubenEquip=True)
            elif subcategory != -1:
                cData = ICD.data.get((category, subcategory), {})
                filterSpeicalEffect = cData.get('filterSpeicalEffect', ())
                if filterSpeicalEffect:
                    isFubenEquip = True
            elif category != -1:
                for k, v in ICD.data.iteritems():
                    if len(k) == 2:
                        _cate, _subCate = k
                        if _cate == category:
                            filterSpeicalEffect = v.get('filterSpeicalEffect', ())
                            if filterSpeicalEffect:
                                isFubenEquip = True
                                break

        if isYaopei:
            yaopei = [{'label': self.getFSTLabel(const.XCONSIGN_FILTER_TYPE_YAOPEI_PROP),
              'data': const.XCONSIGN_FILTER_TYPE_YAOPEI_PROP}, {'label': self.getFSTLabel(const.XCONSIGN_FILTER_TYPE_YAOPEI_SKILL),
              'data': const.XCONSIGN_FILTER_TYPE_YAOPEI_SKILL}]
            ret += yaopei
        if isManual or isFubenEquip:
            goldProp = [{'label': self.getFSTLabel(const.XCONSIGN_FILTER_TYPE_SE_MANUAL),
              'data': const.XCONSIGN_FILTER_TYPE_SE_MANUAL}]
            ret += goldProp
        self.filterTypeCache[name, category, subcategory] = (isManual, isFubenEquip, isYaopei)
        return uiUtils.array2GfxAarry(ret, True)

    def onGetFilterSubSearchType(self, *arg):
        fSearchType = int(arg[3][0].GetNumber())
        cate = arg[3][1].GetString().strip().split(',')
        name = arg[3][2].GetString().strip()
        if name:
            name = unicode2gbk(name)
        subcategory = -1
        category = -1
        if len(cate) > 0 and cate[0]:
            category = int(cate[0])
            if len(cate) > 1:
                subcategory = int(cate[1])
        ret = self.filterPropCache.get((name,
         category,
         subcategory,
         fSearchType), None)
        if ret != None:
            return uiUtils.array2GfxAarry(ret, True)
        else:
            ret = []
            if name:
                result = self.processItemByName(name, school=-1, forme=False, mType=category, sType=subcategory, fSearchType=fSearchType, ret=ret)
            elif subcategory != -1:
                cData = ICD.data.get((category, subcategory), {})
                self.appendPropItems(fSearchType, cData, ret)
            elif category != -1:
                for k, v in ICD.data.iteritems():
                    if len(k) == 2:
                        _cate, _subCate = k
                        if _cate == category:
                            self.appendPropItems(fSearchType, v, ret)

            ret.sort(key=lambda k: k.get('weight', 0), reverse=True)
            self.filterPropCache[name, category, subcategory, fSearchType] = ret
            return uiUtils.array2GfxAarry(ret, True)

    def appendPropItems(self, fSearchType, cData, ret):
        if fSearchType == const.XCONSIGN_FILTER_TYPE_RPROP:
            filterRprop = cData.get('filterRprop', ())
            for propId in filterRprop:
                itemData = PRD.data.get(propId, {})
                name = itemData.get('extraName', '')
                weight = itemData.get('filterWeight', 0)
                if name:
                    sItem = self.genSubcategoryItemData(name, propId, fSearchType, weight)
                    if sItem not in ret:
                        ret.append(sItem)

        elif fSearchType == const.XCONSIGN_FILTER_TYPE_YAOPEI_PROP:
            filterYaopeiProp = cData.get('filterYaopeiProp', ())
            for propId in filterYaopeiProp:
                itemData = PRD.data.get(propId, {})
                name = itemData.get('extraName', '')
                weight = itemData.get('filterWeight', 0)
                if name:
                    sItem = self.genSubcategoryItemData(name, propId, fSearchType, weight)
                    if sItem not in ret:
                        ret.append(sItem)

        elif fSearchType == const.XCONSIGN_FILTER_TYPE_YAOPEI_SKILL:
            filterYaopeiSkill = cData.get('filterYaopeiSkill', ())
            for propId in filterYaopeiSkill:
                name = SGTD.data.get(propId, {}).get('name', '')
                if name:
                    sItem = self.genSubcategoryItemData(name, propId, fSearchType, 0)
                    if sItem not in ret:
                        ret.append(sItem)

        elif fSearchType == const.XCONSIGN_FILTER_TYPE_SE_MANUAL:
            filterSpeicalEffect = cData.get('filterSpeicalEffect', ())
            propNameDict = {}
            for specialEffectId in filterSpeicalEffect:
                seData = ESPD.data.get(specialEffectId, {})
                name = seData.get('name', '')
                if name:
                    propNameDict.setdefault(name, [])
                    if str(specialEffectId) not in propNameDict[name]:
                        propNameDict[name].append(str(specialEffectId))

            for k, v in propNameDict.iteritems():
                data = ','.join(v)
                sItem = self.genSubcategoryItemData(k, data, fSearchType, 0)
                if sItem not in ret:
                    ret.append(sItem)

    def genSubcategoryItemData(self, name, data, fSearchType, weight = 0):
        return {'label': uiUtils.toHtml(name, FILTER_SEARCH_TYPE_COLOR_DICT.get(fSearchType, '')),
         'data': data,
         'weight': weight}

    def processItemPropByItemId(self, itemId, fSearchType, ret):
        resultId = 0
        if fSearchType == const.XCONSIGN_FILTER_TYPE_RPROP:
            mData = MEPD.data.get(itemId, {})
            if mData:
                extraPools = mData.get('extraPools', [])
                for propPool in extraPools:
                    self.processItemPropByPropPool(propPool, ret, fSearchType)

            eData = EEPD.data.get(itemId, {})
            if eData:
                propPool = eData.get('extraPools', 0)
                self.processItemPropByPropPool(propPool, ret, fSearchType)
            yData = YPD.data.get(itemId, {})
            if yData:
                propPool = ED.data.get(itemId, {}).get('randPropId', 0)
                self.processItemPropByPropPool(propPool, ret, fSearchType)
        elif fSearchType == const.XCONSIGN_FILTER_TYPE_YAOPEI_PROP:
            propPool = YPD.data.get(itemId, {}).get('extraProps', ())
            for pId, aLv in propPool:
                propData = YEPD.data.get(pId, [])
                for pData in propData:
                    propId = pData.get('aid', 0)
                    itemData = PRD.data.get(propId, {})
                    name = itemData.get('extraName', '')
                    weight = itemData.get('filterWeight', 0)
                    if name:
                        sItem = self.genSubcategoryItemData(name, propId, fSearchType, weight)
                        if sItem not in ret:
                            ret.append(sItem)

        elif fSearchType == const.XCONSIGN_FILTER_TYPE_YAOPEI_SKILL:
            skills = YPD.data.get(itemId, {}).get('randSkill', ())
            for skillId, skillScore, skillProb in skills:
                name = SGTD.data.get(skillId, {}).get('name', '')
                if name:
                    sItem = self.genSubcategoryItemData(name, skillId, fSearchType, 0)
                    if sItem not in ret:
                        ret.append(sItem)

        elif fSearchType == const.XCONSIGN_FILTER_TYPE_SE_MANUAL:
            mData = MEPD.data.get(itemId, {})
            propNameDict = {}
            if mData:
                specialPools = mData.get('specialPools', ())
                for propTuple in specialPools:
                    for propId, propRate in propTuple:
                        mmData = MESPD.data.get(propId, {})
                        for pData in mmData:
                            specialEffectId = pData.get('specialEffect', 0)
                            seData = ESPD.data.get(specialEffectId, {})
                            name = seData.get('name', '')
                            if name:
                                propNameDict.setdefault(name, [])
                                if str(specialEffectId) not in propNameDict[name]:
                                    propNameDict[name].append(str(specialEffectId))

            eData = EEPD.data.get(itemId, {})
            if eData:
                propTuple = eData.get('specialPools', 0)
                for propId, propRate in propTuple:
                    mmData = MESPD.data.get(propId, {})
                    for pData in mmData:
                        specialEffectId = pData.get('specialEffect', 0)
                        seData = ESPD.data.get(specialEffectId, {})
                        name = seData.get('name', '')
                        if name:
                            propNameDict.setdefault(name, [])
                            if str(specialEffectId) not in propNameDict[name]:
                                propNameDict[name].append(str(specialEffectId))

            for k, v in propNameDict.iteritems():
                data = ','.join(v)
                sItem = self.genSubcategoryItemData(k, data, fSearchType, 0)
                if sItem not in ret:
                    ret.append(sItem)

        return resultId

    def processItemPropByPropPool(self, propPool, ret, fSearchType):
        for k, v in const.ITEM_QUALITY_DESC.iteritems():
            dataList = ERPD.data.get((propPool, k), {})
            for pData in dataList:
                poolIds = pData.get('pool', [])
                for poolIdData in poolIds:
                    poolId, attrNum, extractWay = poolIdData
                    poolDatas = EPPD.data.get(poolId, {})
                    for poolData in poolDatas:
                        poolValue = poolData.get('value', [])
                        aid, atype, transType, amax, amin, pmin, pmax = poolValue
                        itemData = PRD.data.get(aid, {})
                        name = itemData.get('extraName', '')
                        weight = itemData.get('filterWeight', 0)
                        if name:
                            sItem = self.genSubcategoryItemData(name, aid, fSearchType, weight)
                            if sItem not in ret:
                                ret.append(sItem)

    def onCanFilterSearch(self, *arg):
        cate = arg[3][0].GetString().strip().split(',')
        name = arg[3][1].GetString().strip()
        if name:
            name = unicode2gbk(name)
        ret = []
        subcategory = -1
        category = -1
        if len(cate) > 0 and cate[0]:
            category = int(cate[0])
            if len(cate) > 1:
                subcategory = int(cate[1])
        p = BigWorld.player()
        if not name and category == -1 and subcategory == -1:
            p.showGameMsg(GMDD.data.CROSSCONSIGN_FILTERSEARCH_NOT_SELECT, ())
            return
        else:
            canFilterSearch = self.canFilterCache.get((name, category, subcategory), None)
            if canFilterSearch != None:
                itemList = self.nameItemCache.get((name,
                 -1,
                 False,
                 category,
                 subcategory), None)
                if not canFilterSearch:
                    msg = None
                    if name:
                        if len(itemList) >= const.ITEM_CONSIGN_MATCH:
                            hasItem = False
                            for itemId in itemList:
                                if name == ID.data.get(itemId, {}).get('name'):
                                    hasItem = True
                                    break

                            if not hasItem:
                                p.showGameMsg(GMDD.data.CONSIGN_SEARCH_MATCH_FUZZY, ())
                            else:
                                p.showGameMsg(GMDD.data.CUR_ITEM_CANNOT_FILTERSEARCH, ())
                        elif itemList == []:
                            if subcategory != -1 or category != -1:
                                p.showGameMsg(GMDD.data.CONSIGN_SEARCH_MATCH_EMPTY, ())
                            else:
                                p.showGameMsg(GMDD.data.CUR_ITEM_CANNOT_FILTERSEARCH, ())
                        elif itemList == None:
                            pass
                        else:
                            p.showGameMsg(GMDD.data.CUR_ITEM_CANNOT_FILTERSEARCH, ())
                    else:
                        msg = GMDD.data.CUR_CATE_CANNOT_FILTERSEARCH
                    if msg:
                        p.showGameMsg(msg, ())
                return GfxValue(canFilterSearch)
            canFilterSearch = False
            if name:
                result = self.processItemByName(name, school=-1, forme=False, mType=category, sType=subcategory, judgeFilter=True, bMsg=False)
                canFilterSearch = result
                itemList = self.nameItemCache.get((name,
                 -1,
                 False,
                 category,
                 subcategory), None)
                if not canFilterSearch:
                    if len(itemList) >= const.ITEM_CONSIGN_MATCH:
                        hasItem = False
                        for itemId in itemList:
                            if name == ID.data.get(itemId, {}).get('name'):
                                hasItem = True
                                break

                        if not hasItem:
                            p.showGameMsg(GMDD.data.CONSIGN_SEARCH_MATCH_FUZZY, ())
                        else:
                            p.showGameMsg(GMDD.data.CONSIGN_SEARCH_MATCH_EMPTY, ())
                    elif itemList == []:
                        if subcategory != -1 or category != -1:
                            p.showGameMsg(GMDD.data.CONSIGN_SEARCH_MATCH_EMPTY, ())
                        else:
                            p.showGameMsg(GMDD.data.CUR_ITEM_CANNOT_FILTERSEARCH, ())
                    elif itemList == None:
                        pass
                    else:
                        p.showGameMsg(GMDD.data.CUR_ITEM_CANNOT_FILTERSEARCH, ())
            else:
                if subcategory != -1:
                    ret = []
                    cData = ICD.data.get((category, subcategory), {})
                    canFilterSearch = cData.get('canFilterSearch', False)
                elif category != -1:
                    ret = []
                    for k, v in ICD.data.iteritems():
                        if len(k) == 2:
                            _cate, _subCate = k
                            if _cate == category:
                                if v.get('canFilterSearch', False):
                                    canFilterSearch = v.get('canFilterSearch', False)
                                    break

                if not canFilterSearch:
                    p.showGameMsg(GMDD.data.CUR_CATE_CANNOT_FILTERSEARCH, ())
            self.canFilterCache[name, category, subcategory] = canFilterSearch
            return GfxValue(canFilterSearch)

    def processItemByName(self, name, school = -1, forme = False, mType = -1, sType = -1, fSearchType = 0, ret = [], judgeFilter = False, isManual = False, isFubenEquip = False, isYaopei = False, bMsg = True):
        itemIds = []
        p = BigWorld.player()
        hasItemName = False
        itemIds = self.nameItemCache.get((name,
         school,
         forme,
         mType,
         sType), None)
        judgeFilterResult = False
        isYaopeiResult = False
        isManualResult = False
        isFubenEquipResult = False
        if itemIds != None:
            for itemId in itemIds:
                itemData = ID.data.get(itemId, {})
                if name == itemData.get('name', ''):
                    hasItemName = True
                if judgeFilter:
                    if self.canFilterSearchByData(itemData):
                        return True
                if fSearchType:
                    self.processItemPropByItemId(itemId, fSearchType, ret)
                if isYaopei:
                    if itemId in YPD.data:
                        return True
                if isManual:
                    if itemId in MEPD.data:
                        return True
                if isFubenEquip:
                    if itemId in EEPD.data:
                        return True

        else:
            itemIds = []
            for itemId, itemData in ID.data.iteritems():
                if not utils.getItemCrossConsign(itemData):
                    continue
                if name in itemData.get('name', ''):
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
                    hasItemName = hasItemName or itemData.get('name') == name
                    if itemData.get('name') == name:
                        itemIds.insert(0, itemId)
                    else:
                        itemIds.append(itemId)
                    if judgeFilter and not judgeFilterResult:
                        if self.canFilterSearchByData(itemData):
                            judgeFilterResult = True
                    if fSearchType:
                        self.processItemPropByItemId(itemId, fSearchType, ret)
                    if isYaopei and not isYaopeiResult:
                        if itemId in YPD.data:
                            isYaopeiResult = True
                    if isManual and not isManualResult:
                        if itemId in MEPD.data:
                            isManualResult = True
                    if isFubenEquip and not isFubenEquipResult:
                        if itemId in EEPD.data:
                            isFubenEquipResult = True
                    if len(itemIds) >= const.ITEM_CONSIGN_MATCH and hasItemName:
                        break

        self.nameItemCache[name, school, forme, mType, sType] = itemIds
        if judgeFilter and judgeFilterResult:
            return judgeFilterResult
        elif isYaopei and isYaopeiResult:
            return isYaopeiResult
        elif isManual and isManualResult:
            return isManualResult
        elif isFubenEquip and isFubenEquipResult:
            return isFubenEquipResult
        elif len(itemIds) >= const.ITEM_CONSIGN_MATCH and not hasItemName:
            self.nameItemCache[name, school, forme, mType, sType] = itemIds
            bMsg and BigWorld.player().showGameMsg(GMDD.data.CONSIGN_SEARCH_MATCH_FUZZY, ())
            return False
        elif not itemIds and not hasItemName:
            bMsg and BigWorld.player().showGameMsg(GMDD.data.CONSIGN_SEARCH_MATCH_EMPTY, ())
            return False
        elif fSearchType and ret:
            return True
        else:
            return False

    def canFilterSearchByData(self, itemData):
        category = itemData.get('category', -1)
        subcategory = itemData.get('subcategory', -1)
        canFilter = ICD.data.get((category, subcategory), {}).get('canFilterSearch', False)
        return canFilter

    def getFSTLabel(self, _type):
        return uiUtils.toHtml(FILTER_SEARCH_TYPE_LABEL_DICT.get(_type, ''), FILTER_SEARCH_TYPE_COLOR_DICT.get(_type, ''))

    def onShowGameMsg(self, *arg):
        msgId = unicode2gbk(arg[3][0].GetString())
        BigWorld.player().showGameMsg(getattr(GMDD.data, msgId, 0), ())

    def onOpenCharge(self, *arg):
        self.uiAdapter.newRecharge.show()


class TabAuctionCrossServerSearchHistory(SearchHistoryUtils):

    def __init__(self):
        super(TabAuctionCrossServerSearchHistory, self).__init__('TabAuctionCrossServer')
        self.maxCount = 20
