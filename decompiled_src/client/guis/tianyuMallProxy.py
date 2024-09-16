#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/tianyuMallProxy.o
from gamestrings import gameStrings
import subprocess
import BigWorld
from Scaleform import GfxValue
import gameglobal
import utils
import const
import copy
import gametypes
import math
import random
import keys
import clientcom
import clientUtils
import time
import gamelog
from callbackHelper import Functor
from helpers import taboo
from item import Item
from gameclass import ClientMallVal as cmv
from guis import events
from guis import uiConst
from guis import ui
from ui import gbk2unicode
from ui import unicode2gbk
from uiProxy import UIProxy
from guis import uiUtils
from remotePicUtils import RemotePicGroup
from appSetting import Obj as AppSettings
from searchHistoryUtils import SearchHistoryUtils
from gameStrings import gameStrings
from data import bonus_data as BD
from data import mall_category_data as MCD
from data import mall_config_data as MCFD
from data import mall_item_data as MID
from data import mall_link_data as MLD
from data import item_data as ID
from data import vip_package_data as VPD
from data import vip_service_data as VSD
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD
from data import tuzhuang_category_data as TCD
from cdata import tuzhuang_equip_data as TED
from data import sys_config_data as SYSCD
from data import consumable_item_data as CID
from guis import tianYuMallAppVipProxy
from cdata import gui_bao_ge_item_reverse_data as GBGIRD
from data import gui_bao_ge_data as GBGD
SELL_BEFORE_TIME = 0
SELL_IN_TIME = 1
SELL_AFTER_TIME = 2
SELL_NO_TIME = 3
MAIN_TAB_SEARCH = 0
MAIN_TAB_HOMEPAGE = 1
MAIN_TAB_FIXED = 10000
MAIN_TAB_JISHOU = MAIN_TAB_FIXED
MAIN_TAB_VIP = MAIN_TAB_FIXED + 1
MAIN_TAB_FS_SEARCH = MAIN_TAB_VIP + 1
MAIN_TAB_APP_VIP = 13
MAIN_TAB_INV = MAIN_TAB_FIXED - 1
MAIN_TAB_HUANFU = MAIN_TAB_INV - 1
MAIN_TAB_TUZHUANG = 5
SUB_TAB_INV_WING = MAIN_TAB_FS_SEARCH * 100 + 1
SUB_TAB_INV_RIDE = MAIN_TAB_FS_SEARCH * 100 + 2
SUB_TAB_ALL = 0
ENABLE_SUB_TAB_ALL = False
ENABLE_DEL_MALL_ITEM = True
EXCHANGE_TIMEOUT = 10
PREVIEW_NONE = 0
PREVIEW_SHOW_MC = 1
PREVIEW_SHOW_NO_MC = 2
MARKET_ITEM_NUM = 7
MARKET_CALC_NUM = 10
AD_ICON_TEMPLATE = 'advertisement/%s.dds'
LIMIT_TYPE_NONE = 0
LIMIT_TYPE_DAY = 6
LIMIT_TYPE_WEEK = 7
LIMIT_TYPE_MONTH = 8
LIMIT_TYPE_FIRST_BUY = 9
LIMIT_TYPE_ONCE_BUY = 10
SECOND_PER_DAY = 24 * 60 * 60
SEARCH_SCOPE_ALL = 1
SEARCH_SCOPE_FITTING_ROOM = 2
TAB_SHOW_RULE_DISCOUNT = 1
TAB_SHOW_RULE_HISTORY_CONSUME = 2
ADVERTISEMENT_PATH = keys.SET_UI_INFO + '/advertisement/'
VIPPACKAGE_REMIND_TYPE_EARLY = 1
VIPPACKAGE_REMIND_TYPE_LATER = 2
MSG_EARLY_REMIND_LIST = [uiConst.MESSAGE_TYPE_VIP_BASIC_OVERDUE_EARLY_REMIND,
 uiConst.MESSAGE_TYPE_VIP_TRAVEL_OVERDUE_EARLY_REMIND,
 uiConst.MESSAGE_TYPE_VIP_EXP_OVERDUE_EARLY_REMIND,
 uiConst.MESSAGE_TYPE_VIP_PVP_OVERDUE_EARLY_REMIND,
 uiConst.MESSAGE_TYPE_VIP_FIRSTBUY_OVERDUE_EARLY_REMIND]
MSG_LATER_REMIND_LIST = [uiConst.MESSAGE_TYPE_VIP_BASIC_OVERDUE_LATER_REMIND,
 uiConst.MESSAGE_TYPE_VIP_TRAVEL_OVERDUE_LATER_REMIND,
 uiConst.MESSAGE_TYPE_VIP_EXP_OVERDUE_LATER_REMIND,
 uiConst.MESSAGE_TYPE_VIP_PVP_OVERDUE_LATER_REMIND,
 uiConst.MESSAGE_TYPE_VIP_FIRSTBUY_OVERDUE_LATER_REMIND]
MSG_BASIC_REMIND_LSIT = [uiConst.MESSAGE_TYPE_VIP_BASIC_OVERDUE_EARLY_REMIND,
 uiConst.MESSAGE_TYPE_VIP_BASIC_OVERDUE_LATER_REMIND,
 uiConst.MESSAGE_TYPE_VIP_FIRSTBUY_OVERDUE_EARLY_REMIND,
 uiConst.MESSAGE_TYPE_VIP_FIRSTBUY_OVERDUE_LATER_REMIND]
MSG_TRAVEL_REMIND_LIST = [uiConst.MESSAGE_TYPE_VIP_TRAVEL_OVERDUE_EARLY_REMIND, uiConst.MESSAGE_TYPE_VIP_TRAVEL_OVERDUE_LATER_REMIND]
MSG_EXP_REMIND_LIST = [uiConst.MESSAGE_TYPE_VIP_EXP_OVERDUE_EARLY_REMIND, uiConst.MESSAGE_TYPE_VIP_EXP_OVERDUE_LATER_REMIND]
MSG_PVP_REMIND_LIST = [uiConst.MESSAGE_TYPE_VIP_PVP_OVERDUE_EARLY_REMIND, uiConst.MESSAGE_TYPE_VIP_PVP_OVERDUE_LATER_REMIND]

class TianyuMallProxy(UIProxy):
    MALL_CAN_BUY_OK = 0
    MALL_BUY_LIMIT_SEX = 1
    MALL_BUY_LIMIT_SCHOOL = 2
    MALL_BUY_LIMIT_BODYTYPE = 3

    def __init__(self, uiAdapter):
        super(TianyuMallProxy, self).__init__(uiAdapter)
        self.modelMap = {'closeWidget': self.onCloseWidget,
         'getMainTabsInfo': self.onGetMainTabsInfo,
         'getTabContentInfo': self.onGetTabContentInfo,
         'selectMainTabById': self.onSelectMainTabById,
         'selectSubTabById': self.onSelectSubTabById,
         'gotoTab': self.onGotoTab,
         'linkToPreview': self.onLinkToPreview,
         'openBuyConfirm': self.onOpenBuyConfirm,
         'closeBuyConfirm': self.onCloseBuyConfirm,
         'getBuyItemInfo': self.onGetBuyItemInfo,
         'confirmBuy': self.onConfirmBuy,
         'openGiveConfirm': self.onOpenGiveConfirm,
         'closeGiveConfirm': self.onCloseGiveConfirm,
         'getGiveItemInfo': self.onGetGiveItemInfo,
         'getFriendList': self.onGetFriendList,
         'confirmGive': self.onConfirmGive,
         'getMyMoneyInfo': self.onGetMyMoneyInfo,
         'openChargeWindow': self.onOpenChargeWindow,
         'openChargeRewardWindow': self.OnOpenChargeRewardWindow,
         'requestBuyHistory': self.onRequestBuyHistory,
         'setPreviewInfo': self.onSetPreviewInfo,
         'queryPointsInfo': self.onQueryPointsInfo,
         'getMyPointsInfo': self.onGetMyPointsInfo,
         'searchMallItem': self.onSearchMallItem,
         'loadComplete': self.onLoadComplete,
         'reSetFigure': self.onReSetFigure,
         'updateFigure': self.onUpdateFigure,
         'rotateFigure': self.onRotateFigure,
         'zoomFigure': self.onZoomFigure,
         'changeColor': self.onChangeColor,
         'getColor': self.onGetColor,
         'enterFullScreenFittingRoom': self.onEnterFullScreenFittingRoom,
         'changeBody': self.onChangeBody,
         'registerJishouMc': self.onRegisterJishouMc,
         'unRegisterJishouMc': self.onUnRegisterJishouMc,
         'confirmJishou': self.onConfirmJishou,
         'getMarketInfo': self.onGetMarketInfo,
         'getMyMarketInfo': self.onGetMyMarketInfo,
         'getMyTradeHistroyInfo': self.onGetMyTradeHistoryInfo,
         'queryCoinMarket': self.onQueryCoinMarket,
         'queryMyTradeInfo': self.onQueryMyTradeInfo,
         'deleteOrder': self.onDeleteOrder,
         'initTradeBtn': self.onInitTradeBtn,
         'openJishouConfirm': self.onOpenJishouConfirm,
         'closeJishouConfirm': self.onCloseJishouConfirm,
         'registerVipMc': self.onRegisterVipMc,
         'unRegisterVipMc': self.onUnRegisterVipMc,
         'openVipBasicPackageConfirm': self.onOpenVipBasicPackageConfirm,
         'closeVipBasicPackageConfirm': self.onCloseVipBasicPackageConfirm,
         'confirmBuyVipBasicPackage': self.onConfirmBuyVipBasicPackage,
         'closeVipDiscount': self.onCloseVipDiscount,
         'getVipRoleInfo': self.onGetVipRoleInfo,
         'takeVipBonus': self.onTakeVipBonus,
         'getDoubleExpInfo': self.onGetDoubleExpInfo,
         'toggleDoubleExp': self.onToggleDoubleExp,
         'openVipExpBonus': self.onOpenVipExpBonus,
         'getFashionDesc': self.onGetFashionDesc,
         'gotoChargeReward': self.onGotoChargeReward,
         'getChargeRewardName': self.onGetChargeRewardName,
         'enterTuZhuang': self.onEnterTuZhuang,
         'openCompensateTake': self.onOpenCompensateTake,
         'takeAllVipReward': self.onTakeAllVipReward,
         'getCompensateBuyItemInfo': self.onGetCompensateBuyItemInfo,
         'closeCompensateBuyConfirm': self.onCloseCompensateBuyConfirm,
         'confirmCompensateBuy': self.onConfirmCompensateBuy,
         'getSearchHistory': self.onGetSearchHistory,
         'openWebMall': self.onOpenWebMall,
         'openXiuChang': self.onOpenXiuChang,
         'isCurrentMallTab': self.onIsCurrentMallTab,
         'registerAppVipMc': self.onRegisterAppVipMc,
         'unRegisterAppVipMc': self.onUnRegisterAppVipMc,
         'openOutsideUrl': self.onOpenOutsideUrl,
         'queryVipSameCompensate': self.onQueryVipIsSameCompensate,
         'itemSlotClick': self.onItemSlotClick}
        self.mallMediator = None
        self.giveMediator = None
        self.buyMediator = None
        self.buyVipMediator = None
        self.jishouConfirmMediator = None
        self.vipDiscountMediator = None
        self.compensateBugMediator = None
        self.mallWidgetId = uiConst.WIDGET_COMBINE_TIANYU_MALL
        self.giveWidgetId = uiConst.WIDGET_COMBINE_TIANYU_MALL_GIVE
        self.buyWidgetId = uiConst.WIDGET_COMBINE_TIANYU_MALL_BUY
        self.jishouConfirmWidgetId = uiConst.WIDGET_COMBINE_JISHOU_CONFIRM
        self.buyVipWidgetId = uiConst.WIDGET_COMBINE_TIANYU_VIP_BUY
        self.vipDiscountWidgetId = uiConst.WIDGET_COMBINE_VIP_DISCOUNT
        self.compensateBugWidgetId = uiConst.WIDGET_COMBINE_TIANYU_COMPENSATE_BUY
        uiAdapter.registerEscFunc(self.mallWidgetId, self.hide)
        uiAdapter.registerEscFunc(self.giveWidgetId, self.onCloseGiveConfirm)
        uiAdapter.registerEscFunc(self.buyWidgetId, self.onCloseBuyConfirm)
        uiAdapter.registerEscFunc(self.jishouConfirmWidgetId, self.onCloseJishouConfirm)
        uiAdapter.registerEscFunc(self.buyVipWidgetId, self.onCloseVipBasicPackageConfirm)
        uiAdapter.registerEscFunc(self.vipDiscountWidgetId, self.onCloseVipDiscount)
        uiAdapter.registerEscFunc(self.compensateBugWidgetId, self.onCloseCompensateBuyConfirm)
        self.addEvent(events.EVENT_POINTS_EXCHANGE_DONE, self.onExchangeTianbiDone, isGlobal=True)
        self.addEvent(events.EVENT_POINTS_EXCHANGE_FAILED, self.onExchangeTianbiFailed, isGlobal=True)
        self.addEvent(events.EVENT_VIP_INFO_UPDATE, self.refreshVipRoleInfo, isGlobal=True)
        self.addEvent(events.EVENT_VIP_PACKAGEINFO_UPDATE, self.vipExpirePushEx, isGlobal=True)
        self.exchanging = False
        self.exchangePending = 0
        self.exchangStartTime = 0
        self.isShow = False
        self.firstTradeBtnName = 'buyBtn'
        self.tabMgr = TabManager()
        self.clearAll()
        self.mallPicGroup = MallPicGroup()
        self.vipPicGroup = VipPicGroup()
        self.checkImageExist = True
        self.globalLimitLeft = {}
        self.tianyuSearchHistory = TianyuMallSearchHistory()
        self.timeState = SELL_NO_TIME
        self.clockId = None
        self.lastResetMallTabTime = utils.getNow()
        self.pushPackageInfos = self.initPushPackageInfos()
        self.tianyuAppVipPanel = tianYuMallAppVipProxy.TianYuMallAppVipProxy()
        self.searchKey = ''
        self.historyConsumedStatus = 0

    def _registerMediator(self, widgetId, mediator):
        if widgetId == self.mallWidgetId:
            self.mallMediator = mediator
            self.tabMgr.initTabs()
            self.tabMgr.prepareOpen()
            self.tianyuSearchHistory.readConfigData()
            ret = {}
            ret['showJishou'] = self.showJiShouConfig()
            ret['showVip'] = self.showVipConfig()
            ret['showChargeReward'] = gameglobal.rds.ui.chargeReward.showChargeReward()
            ret['showShanghui'] = gameglobal.rds.configData.get('enableShowMallWeb', 0) == 1
            ret['showXiuchang'] = gameglobal.rds.configData.get('enableShowMallWeb', 0) == 2
            self.queryMallGlobalLimit()
            self.tianyuAppVipPanel = tianYuMallAppVipProxy.TianYuMallAppVipProxy()
            BigWorld.callback(0.1, self.refreshSearchResult)
            return uiUtils.dict2GfxDict(ret, True)
        if widgetId == self.giveWidgetId:
            self.giveMediator = mediator
        elif widgetId == self.buyWidgetId:
            self.buyMediator = mediator
        elif widgetId == self.buyVipWidgetId:
            self.buyVipMediator = mediator
        elif widgetId == self.compensateBugWidgetId:
            self.compensateBugMediator = mediator
        else:
            if widgetId == self.jishouConfirmWidgetId:
                self.jishouConfirmMediator = mediator
                return uiUtils.dict2GfxDict(self.jishouInfo, True)
            if widgetId == self.vipDiscountWidgetId:
                self.vipDiscountMediator = mediator
                ret = {}
                giftList = self.getGiftMallItems(self.confirmBuyMallId)
                giftList.insert(0, self.confirmBuyMallId)
                ret['giftInfo'] = self.getGiftMallData(giftList)
                ret['vipDayList'] = MCFD.data.get('vipFirstBuyDaysList', [{'label': gameStrings.TEXT_TIANYUMALLPROXY_309,
                  'days': 7}])
                return uiUtils.dict2GfxDict(ret, True)

    def refreshSearchResult(self):
        if self.searchKey:
            self.refreshSearchItem(self.searchKey)
            self.searchKey = ''

    def initUI(self):
        self.mallMediator.Invoke('initUI')

    def refreshTimeState(self):
        if not self.mallMediator:
            return
        itemsInfo = self.getTabItemsInfo()
        oldTimeState = self.timeState
        nowTimeState = oldTimeState
        for item in itemsInfo:
            mid = item.get('mallId')
            if item.get('beginTime', ''):
                self.timeState = self.getSellTimeState(mid)
                nowTimeState = self.timeState
                break

        if nowTimeState != oldTimeState:
            self.refreshContentWithoutScrollInit()
        self.clockId = BigWorld.callback(5, self.refreshTimeState)

    def refreshContentWithoutScrollInit(self):
        if self.mallMediator:
            scrollPosition = self.mallMediator.Invoke('getScrollPosition')
            self.mallMediator.Invoke('refreshSelTabContent')
            self.mallMediator.Invoke('scrollToOldPosition', scrollPosition)
            self.mallMediator.Invoke('refreshMainTabs')

    def onUpdateClientCfg(self):
        if not self.showVipConfig() or not self.showJiShouConfig() or not self.showMallConfig():
            self.hide()

    def toggleShowMall(self):
        if self.mallMediator:
            self.hide()
        self.show()

    def notifyMallCantUse(self):
        p = BigWorld.player()
        minLv = self.getMallUseableMinLv()
        if gameglobal.rds.configData.get('offMall', True):
            p.showGameMsg(GMDD.data.MALL_IS_OFF, ())
        elif p.lv < minLv:
            p.showGameMsg(GMDD.data.MALL_USE_LV_LIMIT, (minLv,))
        elif getattr(p, 'isolateType', gametypes.ISOLATE_TYPE_NONE) != gametypes.ISOLATE_TYPE_NONE:
            p.showGameMsg(GMDD.data.FORBIDDEN_IN_ISOLATE, ())

    def _checkRefreshMallTab(self):
        if utils.isSameHour(self.lastResetMallTabTime, utils.getNow()):
            return
        else:
            gameglobal.rds.ui.tianyuMall.tabMgr.children = None
            gameglobal.rds.ui.tianyuMall.tabMgr.initTabs()
            self.lastResetMallTabTime = utils.getNow()
            return

    def show(self, mallId = 0, keyWord = '', tab = None):
        if not self.showMallConfig():
            self.notifyMallCantUse()
            return
        else:
            if self.checkImageExist:
                self.checkTianyuMallImagesExist()
            self._checkRefreshMallTab()
            self.searchMallId = mallId
            self.searchKeyWord = keyWord
            if mallId != 0 or keyWord != '':
                self.showMallTab(MAIN_TAB_SEARCH, 0)
                if self.mallMediator:
                    gameglobal.rds.ui.combineMall.handleClickMallTab0()
                    self.tabMgr.setSelectedChildId(MAIN_TAB_SEARCH)
                    if mallId:
                        self.mallMediator.Invoke('refreshSearchId', GfxValue(mallId))
                        self.mallMediator.Invoke('refreshSelTabContent')
            elif tab != None:
                self.showMallTab(tab, 0)
            else:
                self.showMallTab(MAIN_TAB_HOMEPAGE, 0)
            return

    def isHasNewInfo(self):
        self._checkRefreshMallTab()
        if not self.tabMgr.children:
            self.tabMgr.initTabs()
        childrenInfo = self.tabMgr.getChildrenInfo()[:-2]
        for childInfo in childrenInfo:
            if childInfo.get('redPotVisible', False):
                return True

        return False

    def onQueryVipIsSameCompensate(self, *args):
        BigWorld.player().cell.queryVipIsSameCompensate()

    def showMallTab(self, mainTab, subTab, searchKey = ''):
        if not self.showMallConfig():
            self.notifyMallCantUse()
            return
        self.searchKey = searchKey
        if self.mallMediator:
            self.refreshSearchResult()
        if self.enablePswdSetCheck:
            BigWorld.player().checkSetPassword()
        self.isShow = True
        invlidMainTab = False
        invlidMainTab = invlidMainTab or mainTab == MAIN_TAB_JISHOU and not self.showJiShouConfig()
        invlidMainTab = invlidMainTab or mainTab == MAIN_TAB_VIP and not self.showVipConfig()
        if invlidMainTab:
            mainTab = MAIN_TAB_HOMEPAGE
            subTab = SUB_TAB_ALL
        if mainTab == MAIN_TAB_JISHOU and subTab == 1:
            self.firstTradeBtnName = 'sellBtn'
        else:
            self.firstTradeBtnName = 'buyBtn'
        self.tabMgr.openSpetialTab(mainTab, subTab)
        gameglobal.rds.ui.loadWidget(self.mallWidgetId, False, True)
        if gameglobal.rds.ui.combineMall.currentTab == 1:
            return
        gameglobal.rds.ui.combineMall.show(0)

    def queryMallGlobalLimit(self):
        p = BigWorld.player()
        itemsInfo = self.getTabItemsInfo()
        mids = []
        for item in itemsInfo:
            if item.get('globalLimit', 0):
                mids.append(item.get('mallId'))

        if mids:
            p.base.queryMallGlobalLimit(mids)

    def getTabItemsInfo(self):
        ret = {}
        if self.tabMgr.selChildId == MAIN_TAB_SEARCH:
            if self.searchMallId != 0:
                ret = self.tabMgr.searchByMallId(self.searchMallId)
            else:
                ret = self.tabMgr.searchByKeyWord(self.searchKeyWord)
            return ret['itemsInfo']
        else:
            mainTab = self.tabMgr.getSelChild()
            if mainTab is None:
                return []
            if mainTab.selChildId == SUB_TAB_ALL:
                itemsInfo = mainTab.getAllItemsInfo()
            else:
                subTab = mainTab.getSelChild()
                if subTab is None:
                    return []
                itemsInfo = subTab.getChildrenInfo()
            return itemsInfo

    def showVipTab(self):
        if self.mallMediator and not self.vipMc:
            self.hide()
        self.showMallTab(MAIN_TAB_VIP, 0)

    def tutorialBuyVip(self):
        self.enablePswdSetCheck = False
        self.showVipTab()
        if self.showMallConfig() and self.showVipConfig():
            self.onOpenVipBasicPackageConfirm()

    def clearWidget(self):
        if gameglobal.rds.ui.combineMall.widget:
            self.checkParentShow()
        self.isShow = False
        self.saveFashionPreviewLog()
        gameglobal.rds.ui.unLoadWidget(self.mallWidgetId)
        self.mallMediator = None
        gameglobal.rds.ui.recharge.hide()
        self.onCloseBuyConfirm()
        self.onCloseGiveConfirm()
        self.onCloseJishouConfirm()
        self.onCloseVipBasicPackageConfirm()
        self.onCloseVipDiscount()
        self.tianyuAppVipPanel.onWidgetUnRegister()
        self.vipMc = None
        self.uiAdapter.fittingRoom.resetMallHeadGen()
        self.tianyuSearchHistory.writeConfigData()
        gameglobal.rds.ui.fittingRoom.mallHeadGen = None
        self.reset()

    def tabHide(self):
        self.setWidgetVisible(False)
        gameglobal.rds.ui.yunChuiShop.setWidgetVisible(True)
        gameglobal.rds.ui.recharge.hide()

    def setWidgetVisible(self, visible):
        if self.mallMediator:
            self.mallMediator.Invoke('setWidgetVisible', GfxValue(visible))

    def checkParentShow(self):
        gameglobal.rds.ui.combineMall.hide()
        isYunChuiShopLoading = gameglobal.rds.ui.isWidgetLoading(uiConst.WIDGET_COMBINE_YUNCHUI_SHOP)
        isYunChuiShopLoaded = gameglobal.rds.ui.isWidgetLoaded(uiConst.WIDGET_COMBINE_YUNCHUI_SHOP)
        if isYunChuiShopLoaded or isYunChuiShopLoading:
            gameglobal.rds.ui.yunChuiShop.hide()

    def onIsCurrentMallTab(self, *arg):
        return GfxValue(gameglobal.rds.ui.combineMall.currentTab == 0)

    def clearAll(self):
        self.reset()
        self.tabMgr.children = None
        self.coinMaketVersion = 0
        self.buyMarketInfo = []
        self.sellMarketInfo = []
        self.buyMarkeyExtra = 0
        self.sellMarketExtra = 0
        self.marketHistoryInfo = []
        self.myCoinMarketInfo = []
        self.myTradeHistroy = []
        self.defaultSelectInfo = [-1, False]

    def reset(self):
        self.tabMgr.reset()
        self.confirmBuyMallId = 0
        self.confirmBuyNum = 0
        self.confirmBuyType = ''
        self.pendingBuyMallId = 0
        self.pendingBuyType = 0
        self.confirmGiveMallId = 0
        self.confirmGiveNum = 0
        self.flNeedRefresh = True
        self.friendList = []
        self.cacheItemsInfo = []
        self.searchKeyWord = ''
        self.searchMallId = 0
        self.childRef = 0
        self.jishouInfo = None
        self.jishouMc = None
        self.vipMc = None
        self.numInGroup = 4
        self.cancelCoinMarketIndex = -1
        self.fashionPreviewLog = {}
        self.enablePswdSetCheck = True
        self.confirmBuyExtraInfo = {}

    def getHomePageAdInfo(self):
        ret = []
        if gameglobal.rds.configData.get('enableRemotePic', False):
            ret = self.mallPicGroup.getPicInfoList()
        else:
            hasVip = bool(BigWorld.player().vipBasicPackage)
            vip_icon = 'vip_1'
            adInfo = MCFD.data.get('adHomePage', ())
            for item in adInfo:
                icon = item.get('icon', '1')
                if hasVip and icon == vip_icon:
                    continue
                if not hasVip and icon != vip_icon:
                    continue
                item['iconPath'] = AD_ICON_TEMPLATE % str(item.get('icon', '1'))
                ret.append(item)

        return ret

    def getChargeActivityInfo(self):
        ret = {}
        ret['hasCAInfo'] = gameglobal.rds.ui.newRecharge.checkChargeActivityInfo()
        ret['caDesc'] = MCFD.data.get('chargeActivityDesc', gameStrings.TEXT_TIANYUMALLPROXY_597)
        return ret

    def getVipPageAdInfo(self):
        ret = []
        if gameglobal.rds.configData.get('enableRemotePic', False):
            ret = self.vipPicGroup.getPicInfoList()
        else:
            adInfo = MCFD.data.get('adVipPage', {})
            for item in adInfo:
                item['iconPath'] = AD_ICON_TEMPLATE % str(item.get('icon', 'vip_1'))
                ret.append(item)

        return ret

    def mallPicDownloadDone(self, ret):
        if self.mallMediator:
            self.mallMediator.Invoke('refreshAdvertisement', uiUtils.array2GfxAarry(ret, True))

    def vipPicDownloadDone(self, ret):
        if self.vipMc:
            self.vipMc.Invoke('refreshAdvertisement', uiUtils.array2GfxAarry(ret, True))

    def showMallConfig(self):
        openMall = not gameglobal.rds.configData.get('offMall', True)
        lvCheck = BigWorld.player().lv >= self.getMallUseableMinLv()
        return openMall and lvCheck

    def showJiShouConfig(self):
        return not gameglobal.rds.configData.get('offCoinMarket', True)

    def showVipConfig(self):
        return gameglobal.rds.configData.get('enableVip', False)

    def vipGiftConfig(self):
        return gameglobal.rds.configData.get('enableTrialVipGift', False)

    def getMallUseableMinLv(self):
        minLvKey = 'mallUseableMinLv'
        if gameglobal.rds.configData.has_key(minLvKey):
            return int(gameglobal.rds.configData.get(minLvKey))
        return MCFD.data.get(minLvKey, 17)

    def saveFashionPreviewLog(self):
        if not self.fashionPreviewLog:
            return
        ret = []
        one_log_limit = 20
        for mallId in self.fashionPreviewLog:
            log = self.fashionPreviewLog[mallId]
            ret.append([mallId, log[0], log[1]])

        for i in range(0, len(ret), one_log_limit):
            splitLog = ret[i:i + one_log_limit]
            data = [str(splitLog)]
            BigWorld.player().base.recordClientLog(gametypes.CLIENT_RECORD_TYPE_MALL_PREVIEW, data)

    def formatVipTips(self, mallId):
        ret = {}
        mallData = MID.data.get(mallId, {})
        itemId = mallData.get('itemId', 0)
        itemData = ID.data.get(itemId, {})
        ret['name'] = itemData.get('name', gameStrings.TEXT_TIANYUMALLPROXY_662)
        ret['iconPath'] = uiUtils.getItemIconFile64(itemId)
        ret['price'] = mallData.get('priceVal', 888)
        ret['priceType'] = mallData.get('priceType', 1)
        packageId = mallData.get('packageID', 0)
        serviceList = VPD.data.get(packageId, {}).get('serviceList', ())
        props = []
        vsdd = VSD.data
        for sid in serviceList:
            if vsdd.get(sid, {}).get('invalid', 0) == 1:
                continue
            props.append(vsdd.get(sid, {}).get('propDesc', gameStrings.TEXT_TIANYUMALLPROXY_675 + str(sid)))

        ret['props'] = props
        return uiUtils.dict2GfxDict(ret, True)

    def refreshFriendList(self):
        self.flNeedRefresh = True

    def onSendMoneyCallback(self):
        if self.mallMediator:
            self.mallMediator.Invoke('refreshMyMoney')
        gameglobal.rds.ui.fullscreenFittingRoom.onSendMoneyCallback()
        gameglobal.rds.ui.tuZhuang.refreshMyMoney()

    def onConfirmGiveSuccess(self):
        self.confirmGiveMallId = 0
        self.confirmGiveNum = 0
        self.onCloseGiveConfirm()
        if self.mallMediator:
            self.mallMediator.Invoke('refreshMyMoney')

    def onConfirmBuySuccess(self):
        if self.buyMediator:
            self.buyMediator.Invoke('showBuySuccessAnim')
        if self.confirmBuyType.find('.') < 0:
            return
        else:
            type, index = self.confirmBuyType.split('.')
            index = int(index)
            if type == 'fsfr' or type == 'fsfrpv':
                return gameglobal.rds.ui.fullscreenFittingRoom.onBuyAllPreviewItemsSucc(type, index)
            self.confirmBuyMallId = 0
            self.confirmBuyNum = 0
            self.confirmBuyType = ''
            if type == 'home':
                self.onRequestBuyHistory()
            elif type == 'sprite':
                pass
            if type != 'vipBasic' and type != 'vip' and gameglobal.rds.ui.inventory.tempBagMediator is None:
                gameglobal.rds.ui.inventory.show(tempPanel='mall')
            if self.mallMediator:
                self.mallMediator.Invoke('confirmBuyDone', (GfxValue(type), GfxValue(index)))
            self.queryMallGlobalLimit()
            self.tianyuAppVipPanel.refreshInfo()
            return

    def refreshMainTabs(self):
        if self.mallMediator:
            self.mallMediator.Invoke('refreshMainTabs')

    def onVipPackageConfirmBuySuccess(self, mid):
        packageId = MID.data.get(self.confirmBuyMallId, {}).get('packageID', -1)
        if packageId <= 0:
            return
        isBasic = VPD.data.get(packageId, {}).get('isBasic', 0)
        if isBasic:
            self.confirmBuyMallId = 0
            self.confirmBuyNum = 0
            self.confirmBuyType = ''
            if self.pendingBuyMallId:
                self.pendingBuyVipAddedPackage(self.pendingBuyMallId)
            self.onCloseVipBasicPackageConfirm()
            self.onCloseVipDiscount()
        else:
            self.onConfirmBuySuccess()

    def onConfirmBuyFailed(self):
        self.queryMallGlobalLimit()

    def onGetMallHistoryDone(self):
        p = BigWorld.player()
        now = p.getServerTime()
        ret = []
        for item in p.mallHistory:
            duration = (now - item[5]) / 3600
            if duration > MCFD.data.get('historyKeepHour', 8760):
                continue
            mallId = item[0]
            info = genMallItemInfo(mallId)
            if ENABLE_DEL_MALL_ITEM and not info:
                continue
            if info.get('soldOut', 0) == 1:
                continue
            serverIncludeList = info.get('serverIncludeList')
            if serverIncludeList and utils.getHostId() not in serverIncludeList:
                continue
            serverProgressMsId = info.get('spId', 0)
            if serverProgressMsId and not isAllMileStoneFinished(serverProgressMsId):
                continue
            info['buyCount'] = item[2]
            ret.append(info)

        ret.reverse()
        if self.mallMediator:
            self.mallMediator.Invoke('refreshMallHistory', uiUtils.array2GfxAarry(ret, True))

    @ui.uiEvent(uiConst.WIDGET_COMBINE_TIANYU_MALL, events.EVENT_POINTS_CHANGE)
    def onEventPointsChange(self):
        if self.mallMediator:
            self.mallMediator.Invoke('refreshMyPointsInfo')

    def onExchangeTianbiDone(self):
        if self.exchangePending > 0:
            caId = gameglobal.rds.ui.easyPay.easyPayInfo.get('caId', 0)
            BigWorld.player().base.buyCoinUseStandbyPoint(self.exchangePending, caId)
            self.exchangePending = 0
        else:
            self.exchanging = False
            self.dispatchEvent(events.EVENT_POINTS_EXCHANGE_COMPLETE)

    def onExchangeTianbiFailed(self):
        self.exchangePending = 0
        self.exchanging = False
        self.exchangStartTime = 0

    def onQueryMallGlobalLimitDone(self, left):
        for key, val in left.items():
            self.globalLimitLeft[key] = val

        self.refreshContentWithoutScrollInit()

    def onQueryMarketInfoDone(self, version, market, tSell, tBuy, history):
        buyMarket = []
        sellMarket = []
        self.coinMaketVersion = version
        if self.jishouMc is None:
            return
        else:
            sellFullScreen = 0
            buyFullScreen = 0
            for m in market:
                type, coin, price = int(m[0]), int(m[1]), int(m[2])
                if type == const.COIN_MARKET_OP_SELL_COIN:
                    if len(sellMarket) < MARKET_CALC_NUM:
                        sellMarket.append((coin, price))
                    if len(sellMarket) <= MARKET_ITEM_NUM:
                        sellFullScreen += coin
                elif type == const.COIN_MARKET_OP_BUY_COIN:
                    if len(buyMarket) < MARKET_CALC_NUM:
                        buyMarket.append((coin, price))
                    if len(buyMarket) <= MARKET_ITEM_NUM:
                        buyFullScreen += coin
                else:
                    continue

            history.reverse()
            self.buyMarketInfo = buyMarket
            self.sellMarketInfo = sellMarket
            self.marketHistoryInfo = history
            self.buyMarkeyExtra = tBuy - buyFullScreen
            self.sellMarketExtra = tSell - sellFullScreen
            self.jishouMc.Invoke('refreshMarketInfo')
            return

    def onQueryMyMarketInfoDone(self, data):
        if self.jishouMc is None:
            return
        else:
            data.sort(key=lambda k: k[5])
            self.myCoinMarketInfo = data
            self.jishouMc.Invoke('refreshMarketInfo')
            self.jishouMc.Invoke('refreshMyMarketInfo')
            return

    def onQueryMyHistoryInfoDone(self, data):
        if self.jishouMc is None:
            return
        else:
            self.myTradeHistroy = []
            for item in data:
                if BigWorld.player().gbId == item[1]:
                    type = const.COIN_MARKET_OP_SELL_COIN
                else:
                    type = const.COIN_MARKET_OP_BUY_COIN
                self.myTradeHistroy.append((item[0],
                 type,
                 item[3],
                 item[4]))

            self.jishouMc.Invoke('refreshMyHistoryInfo')
            return

    def onBuySellCoinInMarketOk(self, type, opNUID, coin, price, expireTime, restCoin):
        self.onCloseJishouConfirm()
        self.jishouInfo = None
        tradeTime = expireTime - MCFD.data.get('coinMarketTradeExpireTime', (const.TIME_INTERVAL_DAY,))[0]
        if coin > restCoin:
            self.myTradeHistroy.insert(0, (tradeTime,
             type,
             coin - restCoin,
             price))
        if restCoin > 0:
            self.myCoinMarketInfo.append((tradeTime,
             type,
             opNUID,
             restCoin,
             price,
             expireTime))
        if self.jishouMc:
            self.jishouMc.Invoke('buySellOK')

    def onDeleteOrderOk(self, opNUID):
        self.cancelCoinMarketIndex = -1

    def relayoutItemList(self, itemList, previewAble):
        self.numInGroup = 2 if previewAble else 4
        ret = []
        i = 0
        while i < len(itemList):
            ret.append(itemList[i:i + self.numInGroup])
            i += self.numInGroup

        if i == 0:
            ret.append([])
        return ret

    def addDiscountInfo(self, itemInfo):
        if itemInfo.has_key('discountItem'):
            discountItemId = itemInfo.get('discountItem', 0)
            itemName = ID.data.get(discountItemId, {}).get('name', '')
            hasDiscount = checkCanDiscount(discountItemId)
            discountType = itemInfo.get('discountType', const.MALL_DISCOUNT_TYPE_ZHEKOU)
            if discountType == const.MALL_DISCOUNT_TYPE_ZHEKOU:
                discountText = gameStrings.TEXT_TIANYUMALLPROXY_935 % itemName
            else:
                discountText = gameStrings.TEXT_TIANYUMALLPROXY_937 % itemName
            if not hasDiscount and discountType == const.MALL_DISCOUNT_TYPE_DIJIA:
                discountText = ''
            itemInfo['discount'] = {'hasDiscount': hasDiscount,
             'discountText': discountText,
             'discountType': discountType}
            if discountType == const.MALL_DISCOUNT_TYPE_DIJIA:
                discountMoney = MCFD.data.get('discountItemDict', {}).get(discountItemId, 0)
                itemInfo['discount']['discountMoney'] = discountMoney
        return itemInfo

    def isOnceBuyLimitValid(self, last, dayNum):
        currTime = utils.getNow()
        last += 28800
        lastZeroTime = last - last % SECOND_PER_DAY - 28800
        validZeroTime = dayNum * SECOND_PER_DAY + lastZeroTime
        return validZeroTime < currTime

    def isMallItemCanBuy(self, itemInfo):
        leftNum = 0
        limitType = LIMIT_TYPE_NONE
        mallId = itemInfo.get('mallId', 0)
        p = BigWorld.player()
        currTime = utils.getNow()
        if itemInfo.get('dayLimit', 0) > 0:
            limitType = LIMIT_TYPE_DAY
            leftNum = itemInfo.get('dayLimit', 0) - p.mallInfo.get(mallId, cmv()).nDay / itemInfo.get('many', 1)
        elif itemInfo.get('weekLimit', 0) > 0:
            limitType = LIMIT_TYPE_WEEK
            leftNum = itemInfo.get('weekLimit', 0) - p.mallInfo.get(mallId, cmv()).nWeek / itemInfo.get('many', 1)
        elif itemInfo.get('monthLimit', 0) > 0:
            limitType = LIMIT_TYPE_MONTH
            leftNum = itemInfo.get('monthLimit', 0) - p.mallInfo.get(mallId, cmv()).nMonth / itemInfo.get('many', 1)
        elif itemInfo.get('totalLimit', 0) > 0:
            limitType = LIMIT_TYPE_FIRST_BUY
            leftNum = itemInfo.get('totalLimit', 0) - p.mallInfo.get(mallId, cmv()).nTotal / itemInfo.get('many', 1)
        elif itemInfo.get('onceBuyDaysLimit', 0) > 0:
            limitType = LIMIT_TYPE_ONCE_BUY
            tLast = p.mallInfo.get(mallId, cmv()).tLast
            leftNum = 1 if tLast == 0 or self.isOnceBuyLimitValid(tLast, itemInfo.get('onceBuyDaysLimit', 0)) else 0
        if limitType != LIMIT_TYPE_NONE and leftNum <= 0:
            return False
        hasPermission = True
        if itemInfo.get('mallScoreLimit', 0) > 0:
            needScore = itemInfo.get('mallScoreLimit', 0)
            hasPermission = p.totalMallScore >= needScore
        elif itemInfo.get('vipService', []):
            hasPermission = self.mallBuyVipPermissionCheck(itemInfo.get('vipService', []))
        if not hasPermission:
            return False
        if itemInfo.get('beginTime', ''):
            beginTime = itemInfo.get('beginTime', '')
            endTime = itemInfo.get('endTime', '')
            beginStamp = utils.getTimeSecondFromStr(beginTime)
            if endTime:
                endStamp = utils.getTimeSecondFromStr(endTime)
            else:
                endStamp = 0
            now = utils.getNow()
            if not endStamp:
                if now < beginStamp:
                    return False
            else:
                if now < beginStamp:
                    return False
                if beginStamp <= now <= endStamp:
                    pass
                else:
                    return False
        if itemInfo.get('globalLimit', 0):
            globalLimitLeft = self.getGlobalLimitLeft(mallId)
            if globalLimitLeft <= 0:
                return False
        return True

    def appendLimitInfo(self, itemList):
        p = BigWorld.player()
        currTime = utils.getNow()
        ret = []
        for i, itemInfo in enumerate(itemList):
            leftNum = 0
            limitType = LIMIT_TYPE_NONE
            mallId = itemInfo.get('mallId', 0)
            if itemInfo.get('dayLimit', 0) > 0:
                limitType = LIMIT_TYPE_DAY
                leftNum = itemInfo.get('dayLimit', 0) - p.mallInfo.get(mallId, cmv()).nDay / itemInfo.get('many', 1)
            elif itemInfo.get('weekLimit', 0) > 0:
                limitType = LIMIT_TYPE_WEEK
                leftNum = itemInfo.get('weekLimit', 0) - p.mallInfo.get(mallId, cmv()).nWeek / itemInfo.get('many', 1)
            elif itemInfo.get('monthLimit', 0) > 0:
                limitType = LIMIT_TYPE_MONTH
                leftNum = itemInfo.get('monthLimit', 0) - p.mallInfo.get(mallId, cmv()).nMonth / itemInfo.get('many', 1)
            elif itemInfo.get('totalLimit', 0) > 0:
                limitType = LIMIT_TYPE_FIRST_BUY
                leftNum = itemInfo.get('totalLimit', 0) - p.mallInfo.get(mallId, cmv()).nTotal / itemInfo.get('many', 1)
            elif itemInfo.get('onceBuyDaysLimit', 0) > 0:
                limitType = LIMIT_TYPE_ONCE_BUY
                tLast = p.mallInfo.get(mallId, cmv()).tLast
                leftNum = 1 if tLast == 0 or self.isOnceBuyLimitValid(tLast, itemInfo.get('onceBuyDaysLimit', 0)) else 0
            itemInfo['limitType'] = limitType
            itemInfo['leftNum'] = max(leftNum, 0)
            permissionTip = ''
            hasPermission = True
            if itemInfo.get('mallScoreLimit', 0) > 0:
                needScore = itemInfo.get('mallScoreLimit', 0)
                permissionTip = gameStrings.TEXT_TIANYUMALLPROXY_1067 % needScore
                hasPermission = p.totalMallScore >= needScore
            elif itemInfo.get('vipService', []):
                permissionTip = gameStrings.TEXT_TIANYUMALLPROXY_1071
                hasPermission = self.mallBuyVipPermissionCheck(itemInfo.get('vipService', []))
            itemInfo['permissionTip'] = permissionTip
            itemInfo['hasPermission'] = hasPermission
            soldOutDaysFromHostStart = itemInfo.get('soldOutDaysFromHostStart', 0)
            if itemInfo.get('beginTime', '') or soldOutDaysFromHostStart:
                beginTime = itemInfo.get('beginTime', '')
                endTime = itemInfo.get('endTime', '')
                beginStamp = utils.getTimeSecondFromStr(beginTime)
                month = time.strftime('%m', time.localtime(beginStamp))
                day = time.strftime('%d', time.localtime(beginStamp))
                hour = time.strftime('%H', time.localtime(beginStamp))
                beginTxt = gameStrings.TIME_DATE_START_SELL % (month, day, hour)
                hostEndTime = 0
                if soldOutDaysFromHostStart:
                    hostEndTime = utils.getDaySecond(utils.getServerOpenTime() + soldOutDaysFromHostStart * 24 * 60 * 60)
                endStamp = utils.getTimeSecondFromStr(endTime) if endTime else 0
                endStamp = max(hostEndTime, endStamp)
                if endStamp:
                    month = time.strftime('%m', time.localtime(endStamp))
                    day = time.strftime('%d', time.localtime(endStamp))
                    hour = time.strftime('%H', time.localtime(endStamp))
                    endTxt = gameStrings.TIME_DATE_END_SELL % (month, day, hour)
                else:
                    endTxt = ''
                now = utils.getNow()
                if not endStamp:
                    if now < beginStamp:
                        itemInfo['sellTimeState'] = SELL_BEFORE_TIME
                        itemInfo['sellTimeLabel'] = gameStrings.TEXT_TIANYUMALLPROXY_1105
                        itemInfo['sellTime'] = beginTxt
                    else:
                        itemInfo['sellTimeState'] = SELL_IN_TIME
                        itemInfo['sellTimeLabel'] = ''
                        itemInfo['sellTime'] = ''
                elif now < beginStamp:
                    itemInfo['sellTimeState'] = SELL_BEFORE_TIME
                    itemInfo['sellTimeLabel'] = gameStrings.TEXT_TIANYUMALLPROXY_1105
                    itemInfo['sellTime'] = beginTxt
                elif now >= beginStamp and now <= endStamp:
                    itemInfo['sellTimeState'] = SELL_IN_TIME
                    itemInfo['sellTimeLabel'] = ''
                    itemInfo['sellTime'] = endTxt
                else:
                    itemInfo['sellTimeState'] = SELL_AFTER_TIME
                    itemInfo['sellTimeLabel'] = gameStrings.TEXT_TIANYUMALLPROXY_1122
                    itemInfo['sellTime'] = endTxt
            else:
                itemInfo['sellTimeState'] = SELL_NO_TIME
                itemInfo['sellTimeLabel'] = ''
                itemInfo['sellTime'] = ''
            if itemInfo.get('globalLimit', 0):
                globalLimit = itemInfo.get('globalLimit', 0)
                globalLimitLeft = self.getGlobalLimitLeft(mallId)
                itemInfo['globalLimitTxt'] = gameStrings.TEXT_TIANYUMALLPROXY_1134 % (globalLimitLeft, globalLimit)
            if itemInfo.has_key('discountItem'):
                discountItemId = itemInfo.get('discountItem', 0)
                hasDiscount = checkCanDiscount(discountItemId)
                discountType = itemInfo.get('discountType', const.MALL_DISCOUNT_TYPE_ZHEKOU)
                if discountType == const.MALL_DISCOUNT_TYPE_ZHEKOU:
                    if not hasDiscount:
                        continue
            self.addDiscountInfo(itemInfo)
            self.addPocessInfo(itemInfo)
            ret.append(itemInfo)

        return ret

    def addPocessInfo(self, itemInfo):
        itemId = itemInfo.get('itemId', 0)
        if itemId:
            guiBaoGeId = GBGIRD.data.get(itemId, 0)
            if guiBaoGeId:
                p = BigWorld.player()
                isHave = False
                assosiateIds = list(GBGD.data.get(guiBaoGeId, {}).get('associateIds', []))
                assosiateIds.append(guiBaoGeId)
                for assId in assosiateIds:
                    if assId in getattr(p, 'appearanceItemCollectSet', set([])):
                        isHave = True
                        break

                itemInfo['isHave'] = isHave

    def isEquipItem(self, assosiateIds):
        p = BigWorld.player()
        equipmets = p.equipment
        for i in xrange(len(equipmets)):
            if equipmets[i]:
                if equipmets[i].id in assosiateIds:
                    return True

        return False

    def getGlobalLimitLeft(self, mallId):
        data = MID.data
        if not data.get(mallId, {}).get('globalLimit', 0):
            return 1
        elif self.globalLimitLeft.has_key(mallId):
            return self.globalLimitLeft.get(mallId, 0)
        else:
            return data.get(mallId, {}).get('globalLimit', 0)

    def mallBuyVipPermissionCheck(self, svcList):
        for sid in svcList:
            if not self.vipServiceCheck(sid):
                return False

        return True

    def vipServiceCheck(self, sid):
        if not self.showVipConfig():
            return False
        p = BigWorld.player()
        now = utils.getNow()
        vsList = []
        vsList.extend(p.vipBasicPackage.get('services', []))
        for pid in p.vipAddedPackage:
            vsList.extend(p.vipAddedPackage[pid].get('services', []))

        for svcId, tExpire in vsList:
            if svcId == sid and tExpire > now and not VSD.data.get(sid, {}).get('invalid', 0):
                return True

        return False

    def globalIdx2DetailIdx(self, index):
        lineIdx = index / self.numInGroup
        rowIdx = index % self.numInGroup
        return (lineIdx, rowIdx)

    def onCloseWidget(self, *arg):
        tag = arg[3][0].GetString()
        if tag == 'mall':
            gameglobal.rds.ui.combineMall.hide()
            self.clearWidget()

    def onGetMainTabsInfo(self, *arg):
        ret = self.tabMgr.getChildrenInfo()
        return uiUtils.array2GfxAarry(ret, True)

    def onSelectMainTabById(self, *arg):
        selId = int(arg[3][0].GetNumber())
        self.tabMgr.setSelectedChildId(selId)
        self.searchKeyWord = ''
        self.searchMallId = 0
        self.updatePreviewMc()
        self.queryMallGlobalLimit()

    def onSelectSubTabById(self, *arg):
        selId = int(arg[3][0].GetNumber())
        self.selectSubTabById(selId)

    def selectSubTabById(self, selId):
        self.tabMgr.getSelChild().setSelectedChildId(selId)
        self.searchKeyWord = ''
        self.searchMallId = 0
        self.updatePreviewMc()
        self.queryMallGlobalLimit()

    def onGotoTab(self, *arg):
        mainTabId = int(arg[3][0].GetNumber())
        subTabId = int(arg[3][1].GetNumber())
        gameglobal.rds.ui.combineMall.hide()
        self.clearWidget()
        self.showMallTab(mainTabId, subTabId)

    def onLinkToPreview(self, *arg):
        p = BigWorld.player()
        linkId = int(arg[3][0].GetNumber())
        mldd = MLD.data.get(linkId, {})
        physique = getattr(p, 'physique', None)
        sex = getattr(physique, 'sex', -1)
        bodyType = getattr(physique, 'bodyType', -1)
        key = 'm' if sex == 1 else 'f'
        key += str(bodyType)
        linkData = mldd.get(key, ())
        if not linkData:
            linkData = mldd.get('default', ())
        if not linkData:
            return
        elif len(linkData) != 3:
            return
        else:
            mainTab, subTab, selMallId = linkData
            canBuy, name = self.mallItemCanBuyCheck(selMallId, p)
            selectIndex = self.findMallIdInTab(mainTab, subTab, selMallId)
            self.defaultSelectInfo = [selectIndex, canBuy == self.MALL_CAN_BUY_OK]
            gameglobal.rds.ui.combineMall.hide()
            self.clearWidget()
            self.showMallTab(mainTab, subTab)
            return

    def findMallIdInTab(self, mainId, subId, mallId):
        mainTab = self.tabMgr.getChild(mainId)
        if not mainTab:
            return -1
        subTab = mainTab.getChild(subId)
        if not subTab:
            return -1
        mallIdList = subTab.mallIdList
        if mallId not in mallIdList:
            return -1
        return mallIdList.index(mallId)

    def updatePreviewMc(self):
        mainTab = self.tabMgr.getSelChild()
        if mainTab is None:
            return
        else:
            subTab = mainTab.getSelChild()
            if subTab is None:
                return
            if self.mallMediator is None:
                return
            preview = subTab.getTabInfo().get('preview', PREVIEW_NONE)
            if preview == PREVIEW_SHOW_NO_MC:
                self.mallMediator.Invoke('setPreviewMcVisible', GfxValue(False))
            elif preview == PREVIEW_SHOW_MC:
                self.mallMediator.Invoke('setPreviewMcVisible', GfxValue(True))
            return

    def setLoadingMcVisible(self, value):
        if self.mallMediator:
            self.mallMediator.Invoke('setLoadingMcVisible', GfxValue(value))

    def genTabContentInfo(self):
        previewAble = False
        p = BigWorld.player()
        if self.tabMgr.selChildId == MAIN_TAB_SEARCH:
            if self.searchMallId != 0:
                ret = self.tabMgr.searchByMallId(self.searchMallId)
            else:
                ret = self.tabMgr.searchByKeyWord(self.searchKeyWord)
            ret['itemsInfo'] = self.appendLimitInfo(ret['itemsInfo'])
            ret['itemsInfo'] = self.relayoutItemList(ret['itemsInfo'], False)
            ret['selMallInfo'] = [-1, False]
            self.cacheItemsInfo = ret['itemsInfo']
            return ret
        else:
            ret = {}
            mainTab = self.tabMgr.getSelChild()
            if mainTab is None:
                return ret
            subTabInfo = mainTab.getChildrenInfo()
            if mainTab.selChildId == SUB_TAB_ALL:
                itemsInfo = mainTab.getAllItemsInfo()
            else:
                subTab = mainTab.getSelChild()
                if subTab is None:
                    return ret
                itemsInfo = subTab.getChildrenInfo()
                previewAble = subTab.previewAble
                isRandom = subTab.isRandom
            if self.tabMgr.selChildId == MAIN_TAB_HOMEPAGE:
                ret['adInfo'] = self.getHomePageAdInfo()
                ret['caInfo'] = self.getChargeActivityInfo()
                if isRandom:
                    itemsInfo = self.randomSelect(itemsInfo, 4)
                else:
                    itemsInfo = self.selectItems(itemsInfo, 4)
            elif self.tabMgr.selChildId == MAIN_TAB_VIP:
                ret['adInfo'] = self.getVipPageAdInfo()
                ret['vipDayList'] = MCFD.data.get('vipDaysList', [{'label': gameStrings.TEXT_TIANYUMALLPROXY_1380,
                  'days': 30}])
                now = BigWorld.player().getServerTime()
                for item in itemsInfo:
                    packageId = item.get('packageID', 0)
                    item['expire'] = p.vipAddedPackage.get(packageId, {}).get('tExpire', 0) - now
                    item['vipDayList'] = self.genVipDayList(packageId)

            itemsInfo = self.appendLimitInfo(itemsInfo)
            itemsInfo = self.relayoutItemList(itemsInfo, previewAble)
            ret['subTabInfo'] = subTabInfo
            ret['itemsInfo'] = itemsInfo
            ret['selMallInfo'] = self.defaultSelectInfo
            ret['showFSFittingRoom'] = gameglobal.rds.ui.fullscreenFittingRoom.showFullscreenFittingRoomConfig()
            ret['showTuZhuang'] = gameglobal.rds.ui.tuZhuang.canShowTuZhuang()
            return ret

    def onGetTabContentInfo(self, *arg):
        ret = self.genTabContentInfo()
        itemsInfo = ret.get('itemsInfo', {})
        self.defaultSelectInfo = [-1, False]
        self.cacheItemsInfo = itemsInfo
        return uiUtils.dict2GfxDict(ret, True)

    def randomSelect(self, orgList, selNum):
        if len(orgList) <= selNum:
            return orgList
        oldList = copy.deepcopy(orgList)
        randomList = []
        for i in range(selNum):
            randIdx = random.randint(0, len(oldList) - 1)
            randItem = oldList.pop(randIdx)
            randomList.append(randItem)

        return randomList

    def selectItems(self, orgList, selNum):
        if len(orgList) <= selNum:
            return orgList
        randomList = orgList[0:4]
        return randomList

    def genVipDayList(self, packageId):
        p = BigWorld.player()
        now = p.getServerTime()
        origList = MCFD.data.get('vipDaysList', [{'label': gameStrings.TEXT_TIANYUMALLPROXY_1380,
          'days': 30}])
        daysList = map(lambda item: item['days'], origList)
        resultList = []
        packageLeftTime = max(p.vipAddedPackage.get(packageId, {}).get('tExpire', 0) - now, 0)
        basicLeftTime = max(p.vipBasicPackage.get('tExpire', 0) - now, 0)
        canBuyDay = int(math.ceil((basicLeftTime - packageLeftTime) / const.TIME_INTERVAL_DAY))
        for i in range(len(daysList)):
            if daysList[i] <= canBuyDay:
                resultList.append(origList[i])

        if canBuyDay == 0:
            resultList = origList[:1]
        elif canBuyDay not in daysList:
            resultList.append({'label': str(canBuyDay) + gameStrings.TEXT_PLAYRECOMMPROXY_848_6,
             'days': canBuyDay})
        return resultList

    def mallItemCanBuyCheck(self, mallId, p):
        itemId = MID.data.get(mallId, {}).get('itemId', 0)
        itemName = ID.data.get(itemId, {}).get('name', gameStrings.TEXT_TIANYUMALLPROXY_1455)
        sexReq = ID.data.get(itemId, {}).get('sexReq', 0)
        physique = getattr(p, 'physique', None)
        pSex = getattr(physique, 'sex', -1)
        if sexReq > 0 and sexReq != pSex:
            return (self.MALL_BUY_LIMIT_SEX, itemName)
        else:
            if ID.data.get(itemId, {}).has_key('schReq'):
                if getattr(p, 'realSchool', const.SCHOOL_DEFAULT) not in ID.data.get(itemId, {}).get('schReq', 0):
                    return (self.MALL_BUY_LIMIT_SCHOOL, itemName)
            if not utils.inAllowBodyType(itemId, getattr(physique, 'bodyType', -1), ID):
                return (self.MALL_BUY_LIMIT_BODYTYPE, itemName)
            return (self.MALL_CAN_BUY_OK, itemName)

    def onOpenBuyConfirm(self, *arg):
        self.mallBuyConfirm(int(arg[3][0].GetNumber()), int(arg[3][1].GetNumber()), arg[3][2].GetString())

    def spriteBuyMallItem(self, mallId, buyNum = 1):
        self.mallBuyConfirm(mallId, buyNum, 'sprite.0')

    def newPlayerTBBuyMallItem(self, confirmBuyCallBack = None):
        mallId = SYSCD.data.get('newPlayerTBPurchaseMallItem', 0)
        buyNum = 1
        self.mallBuyConfirm(mallId, buyNum, 'npTB.0', extra={'confirmBuyCallBack': confirmBuyCallBack})

    def mallBuyConfirm(self, mallId, buyNum, buyType, extra = {}):
        ret = self.mallItemCanBuyCheck(int(mallId), BigWorld.player())
        if ret[0] == self.MALL_BUY_LIMIT_SEX:
            gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_TIANYUMALLPROXY_1486 + ret[1] + gameStrings.TEXT_TIANYUMALLPROXY_1486_1)
            return
        if ret[0] == self.MALL_BUY_LIMIT_SCHOOL:
            gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_TIANYUMALLPROXY_1486 + ret[1] + gameStrings.TEXT_TIANYUMALLPROXY_1490)
            return
        if ret[0] == self.MALL_BUY_LIMIT_BODYTYPE:
            gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_TIANYUMALLPROXY_1486 + ret[1] + gameStrings.TEXT_TIANYUMALLPROXY_1494)
            return
        if self.getGlobalLimitLeft(mallId) <= 0:
            gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_TIANYUMALLPROXY_1486 + ret[1] + gameStrings.TEXT_TIANYUMALLPROXY_1498)
            return
        if self.getSellTimeState(mallId) == SELL_BEFORE_TIME:
            gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_TIANYUMALLPROXY_1486 + ret[1] + gameStrings.TEXT_TIANYUMALLPROXY_1503)
            return
        if self.getSellTimeState(mallId) == SELL_AFTER_TIME:
            gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_TIANYUMALLPROXY_1486 + ret[1] + gameStrings.TEXT_TIANYUMALLPROXY_1506)
            return
        self.confirmBuyMallId = int(mallId)
        self.confirmBuyNum = int(buyNum)
        self.confirmBuyType = buyType
        self.confirmBuyExtraInfo = extra
        if not self.vipBasicPackgeCheck():
            return
        gameglobal.rds.ui.loadWidget(self.buyWidgetId, True)

    def getSellTimeState(self, mallId):
        itemInfo = MID.data.get(mallId)
        if itemInfo.get('beginTime', ''):
            beginTime = itemInfo.get('beginTime', '')
            endTime = itemInfo.get('endTime', '')
            now = utils.getNow()
            beginStamp = utils.getTimeSecondFromStr(beginTime)
            if endTime:
                endStamp = utils.getTimeSecondFromStr(endTime)
            else:
                endStamp = 0
            now = utils.getNow()
            if not endStamp:
                if now < beginStamp:
                    return SELL_BEFORE_TIME
                else:
                    return SELL_IN_TIME
            elif now < beginStamp:
                return SELL_BEFORE_TIME
            elif now >= beginStamp and now <= endStamp:
                return SELL_IN_TIME
            else:
                return SELL_AFTER_TIME
        elif itemInfo.get('soldDaysFromHostStart', 0) or itemInfo.get('soldOutDaysFromHostStart', 0):
            soldDaysFromHostStart = itemInfo.get('soldDaysFromHostStart', 0)
            soldOutDaysFromHostStart = itemInfo.get('soldOutDaysFromHostStart', 0)
            beginStamp = utils.getDaySecond(utils.getServerOpenTime() + soldDaysFromHostStart * const.SECONDS_PER_DAY)
            endStamp = utils.getDaySecond(utils.getServerOpenTime() + soldOutDaysFromHostStart * const.SECONDS_PER_DAY)
            now = utils.getNow()
            if not endStamp:
                if now < beginStamp:
                    return SELL_BEFORE_TIME
                else:
                    return SELL_IN_TIME
            elif now < beginStamp:
                return SELL_BEFORE_TIME
            elif now >= beginStamp and now <= endStamp:
                return SELL_IN_TIME
            else:
                return SELL_AFTER_TIME
        else:
            return SELL_NO_TIME

    def vipBasicPackgeCheck(self):
        if self.confirmBuyType.find('.') < 0:
            return True
        type, index = self.confirmBuyType.split('.')
        if type != 'vip':
            return True
        if BigWorld.player().vipBasicPackage.get('tExpire', 0) < utils.getNow():
            msg = GMD.data.get(GMDD.data.MALL_BUY_BASIC_PACKAGE_FIRST, {}).get('text', gameStrings.TEXT_TIANYUMALLPROXY_1573)
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.buyVipBasicPackage), gameStrings.TEXT_TIANYUMALLPROXY_1574)
            return False
        return True

    def buyVipBasicPackage(self):
        self.pendingBuyMallId = self.confirmBuyMallId
        self.pendingBuyType = self.confirmBuyType
        self.onOpenVipBasicPackageConfirm()

    def pendingBuyVipAddedPackage(self, mid):
        if not self.vipMc:
            self.hide()
        self.tabMgr.initTabs()
        self.tabMgr.openSpetialTab(MAIN_TAB_VIP, 0)
        self.tabMgr.prepareOpen()
        self.onGetTabContentInfo()
        index = 0
        values = MCFD.data.get('vipValues', {}).get('value', ())
        for i in range(len(values)):
            vMid, tag = values[i]
            if mid == vMid:
                index = i
                break

        vipLeftTime = BigWorld.player().vipBasicPackage.get('tExpire', 0) - utils.getNow()
        self.confirmBuyMallId = mid
        self.confirmBuyNum = math.ceil(float(vipLeftTime) / const.TIME_INTERVAL_DAY)
        self.confirmBuyType = 'vip.' + str(index)
        gameglobal.rds.ui.loadWidget(self.buyWidgetId, True)

    def onCloseBuyConfirm(self, *arg):
        gameglobal.rds.ui.unLoadWidget(self.buyWidgetId)
        self.buyMediator = None

    def onGetCompensateBuyItemInfo(self, *arg):
        p = BigWorld.player()
        ret = {}
        compensateList = []
        if p.vipCompensateCnt > 0:
            for i in xrange(p.vipCompensateCnt):
                compensateList.append({'label': '%d' % (i + 1),
                 'times': i + 1})

        ret['compensateList'] = compensateList
        ret['priceType'] = gametypes.MALL_PRICE_TYPE_COIN
        mId = SYSCD.data.get('VIP_COMPENSATE_MALL_ID', 0)
        ret['priceVal'] = MID.data.get(mId, {}).get('priceVal', 999999)
        ret['moneyInfo'] = self.getMyMoneyInfo()
        ret['isVipSameCompensate'] = p.isVipSameCompensate()
        return uiUtils.dict2GfxDict(ret, True)

    def onGetBuyItemInfo(self, *arg):
        p = BigWorld.player()
        if self.confirmBuyMallId == 0:
            return
        if self.confirmBuyType.find('.') < 0:
            return
        type, index = self.confirmBuyType.split('.')
        if type == 'history':
            ret = genMallItemInfo(self.confirmBuyMallId)
            ret = self.addDiscountInfo(ret)
        elif type in ('adv', 'sprite', 'mallWeb', 'huiliu', 'playRecomm', 'appVip', 'zhanmo', 'challengePassport', 'mapgame', 'collect'):
            ret = genMallItemInfo(self.confirmBuyMallId)
        elif type == 'fsfr':
            ret = gameglobal.rds.ui.fullscreenFittingRoom.getItemInfoByIdx(int(index))
        elif type == 'vipBasic':
            ret = genMallItemInfo(self.confirmBuyMallId)
            if not p.vipBasicPackage and MCFD.data.get('vipFirstBuyDaysList', {}) and MCFD.data.get('vipFirstBuyBasicPackage', 0):
                gameStrings.TEXT_TIANYUMALLPROXY_1647
                ret['vipDayList'] = MCFD.data.get('vipFirstBuyDaysList', [{'label': gameStrings.TEXT_TIANYUMALLPROXY_309,
                  'days': 7}])
            else:
                ret['vipDayList'] = MCFD.data.get('vipDaysList', [{'label': gameStrings.TEXT_TIANYUMALLPROXY_1380,
                  'days': 30}])
        elif type == 'wardrobe':
            ret = genMallItemInfo(self.confirmBuyMallId)
        else:
            if type == 'npTB':
                ret = genMallItemInfo(self.confirmBuyMallId)
                ret['buyCount'] = self.confirmBuyNum
                ret['priceAll'] = self.confirmBuyNum * ret['priceVal']
                ret['moneyInfo'] = self.getMyMoneyInfo()
                return uiUtils.dict2GfxDict(ret, True)
            index = int(index)
            line, row = self.globalIdx2DetailIdx(index)
            if line < 0 or line >= len(self.cacheItemsInfo):
                return
            ret = self.cacheItemsInfo[line][row]
        if type == 'vip':
            buyPackageId = MID.data.get(self.confirmBuyMallId, {}).get('packageID', 0)
            ret['basicExpire'] = p.vipBasicPackage.get('tExpire', 0)
            ret['packageExpire'] = p.vipAddedPackage.get(buyPackageId, {}).get('tExpire', 0)
        ret['buyCount'] = self.confirmBuyNum
        ret['priceAll'] = self.confirmBuyNum * ret['priceVal']
        ret['moneyInfo'] = self.getMyMoneyInfo()
        self.appendDiKouInfo(ret)
        ret['buyType'] = type
        if self.tabMgr.getSelChild():
            selTabId = self.tabMgr.getSelChild().selChildId
            children = self.tabMgr.getSelChild().children
            if children:
                if children.get(selTabId):
                    subTabData = children.get(selTabId).data
                    if subTabData.get('isAvoidBtnSprite', 0):
                        ret['isAvoidBtnSprite'] = True
                    else:
                        ret['isAvoidBtnSprite'] = False
        return uiUtils.dict2GfxDict(ret, True)

    @ui.checkInventoryLock()
    def onConfirmBuy(self, *arg):
        if self.confirmBuyMallId <= 0:
            return
        else:
            self.confirmBuyNum = int(arg[3][0].GetNumber())
            if self.confirmBuyNum <= 0:
                return
            mData = MID.data.get(self.confirmBuyMallId, {})
            minLv = mData.get('minLv', 0)
            maxLv = mData.get('maxLv', 0)
            p = BigWorld.player()
            if minLv > 0 and p.lv < minLv:
                p.showGameMsg(GMDD.data.MALL_BUY_MIN_LV, (minLv,))
                return
            if maxLv > 0 and p.lv > maxLv:
                p.showGameMsg(GMDD.data.MALL_BUY_MAX_LV, (maxLv,))
                return
            toBuyItems = []
            toBuyNums = []
            p = BigWorld.player()
            packageId = MID.data.get(self.confirmBuyMallId, {}).get('packageID', -1)
            if packageId > 0:
                if self.confirmBuyNum <= 0:
                    gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_TIANYUMALLPROXY_1720)
                    return
                toBuyItems.append(self.confirmBuyMallId)
                toBuyNums.append(self.confirmBuyNum)
                p.cell.buyVipPackages(0, 0, toBuyItems, toBuyNums, BigWorld.player().cipherOfPerson)
            else:
                buySrc = 0
                if self.confirmBuyType.find('.') >= 0:
                    type, index = self.confirmBuyType.split('.')
                    if type == 'sprite':
                        buySrc = 1
                    elif type == 'fsfr':
                        buySrc = 2
                    else:
                        if type == 'npTB':
                            confirmBuyCallBack = self.confirmBuyExtraInfo.get('confirmBuyCallBack', None)
                            if confirmBuyCallBack:
                                confirmBuyCallBack()
                            self.onCloseBuyConfirm()
                            return
                        buySrc = 0
                toBuyItems.append(self.confirmBuyMallId)
                toBuyNums.append(self.confirmBuyNum)
                discountInfo, IsDiscountItems = clientUtils.getMallItemDiscountInfo(toBuyItems, toBuyNums)
                if not discountInfo:
                    return
                if len(IsDiscountItems) == 1 and IsDiscountItems[0]:
                    if len(discountInfo) == 1 and not discountInfo[0]:
                        p.showGameMsg(GMDD.data.DISCOUNT_COUPON_NOT_ENOUGH, ())
                        return
                historyConsumeFlag = mData.get('historyConsumeFlag', 0)
                if historyConsumeFlag:
                    if self.historyConsumedStatus == gametypes.HISTORY_CONSUMED_STATUS_CAN:
                        msg = uiUtils.getTextFromGMD(GMDD.data.CONFIRM_HISTORY_CONSUME_MALL_BUY)
                        gameglobal.rds.ui.doubleCheckWithInput.show(msg, 'YES', title=gameStrings.ITEM_MSG_BOX_TITLE_DEFAULT, confirmCallback=Functor(p.base.buyMallItems, toBuyItems, toBuyNums, BigWorld.player().cipherOfPerson, buySrc, discountInfo))
                        return
                p.base.buyMallItems(toBuyItems, toBuyNums, BigWorld.player().cipherOfPerson, buySrc, discountInfo)
            return

    def onOpenGiveConfirm(self, *arg):
        self.confirmGiveMallId = int(arg[3][0].GetNumber())
        self.confirmGiveNum = int(arg[3][1].GetNumber())
        if not self.checkGiveItemValid(self.confirmGiveMallId, self.confirmGiveNum):
            return
        gameglobal.rds.ui.loadWidget(self.giveWidgetId, True)

    def checkGiveItemValid(self, mid, num):
        p = BigWorld.player()
        lv = p.lv
        school = p.school
        md = MID.data.get(mid)
        if not md:
            return False
        if md.has_key('minLv') and lv < md['minLv']:
            p.showGameMsg(GMDD.data.MALL_GIVE_WRONG_LV)
            return False
        if md.has_key('maxLv') and lv > md['maxLv']:
            p.showGameMsg(GMDD.data.MALL_GIVE_WRONG_LV)
            return False
        if md.has_key('schoolsLimit') and school not in md['schoolsLimit']:
            p.showGameMsg(GMDD.data.MALL_GIVE_WRONG_SCHOOL)
            return False
        return True

    def onCloseGiveConfirm(self, *arg):
        gameglobal.rds.ui.unLoadWidget(self.giveWidgetId)
        self.giveMediator = None

    def onGetGiveItemInfo(self, *arg):
        if self.confirmGiveMallId == 0:
            return
        ret = genMallItemInfo(self.confirmGiveMallId)
        ret['buyCount'] = self.confirmGiveNum
        ret['priceAll'] = self.confirmGiveNum * ret['priceVal']
        return uiUtils.dict2GfxDict(ret, True)

    def onGetFriendList(self, *arg):
        return uiUtils.array2GfxAarry(self.getFriendList(), True)

    def getFriendList(self):
        p = BigWorld.player()
        if self.flNeedRefresh:
            self.friendList = []
            for fVal in p.friend.itervalues():
                if not p.friend.isFriend(fVal.gbId):
                    continue
                fdata = {'label': fVal.name,
                 'gbid': fVal.gbId}
                self.friendList.append(fdata)

            self.flNeedRefresh = False
        return self.friendList

    def onConfirmGive(self, *arg):
        if arg[3][0] is None or arg[3][1] is None:
            return
        elif self.confirmGiveMallId == 0:
            return
        else:
            msg = str(arg[3][0].GetString())
            msg = unicode2gbk(msg)
            isNormal, subject = taboo.checkDisbWord(msg)
            if not isNormal:
                BigWorld.player().showGameMsg(GMDD.data.CHAT_TABOO_WORD, ())
                return
            flIdx = int(arg[3][1].GetNumber())
            if flIdx < 0:
                return
            friend = self.friendList[flIdx]
            gbid = friend.get('gbid', 0)
            friendName = friend.get('label', 0)
            WARN_COLOR = '#cc2929'
            itemId = MID.data.get(self.confirmGiveMallId, {}).get('itemId', 0)
            itemName = ID.data.get(itemId).get('name', gameStrings.TEXT_TIANYUMALLPROXY_1455)
            confirmMsg = gameStrings.TEXT_TIANYUMALLPROXY_1860 + uiUtils.toHtml(itemName + 'x' + str(self.confirmGiveNum), WARN_COLOR)
            confirmMsg += gameStrings.TEXT_TIANYUMALLPROXY_1861 + uiUtils.toHtml(friendName, WARN_COLOR) + '?'
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(confirmMsg, Functor(self.onConfirmGiveToFriend, gbid, msg))
            return

    @ui.checkInventoryLock()
    def onConfirmGiveToFriend(self, gbid, msg):
        mallIds = []
        giveNums = []
        if self.confirmGiveMallId == 0:
            return
        mallIds.append(self.confirmGiveMallId)
        giveNums.append(self.confirmGiveNum)
        BigWorld.player().base.givePayMall(gbid, mallIds, giveNums, msg, BigWorld.player().cipherOfPerson)

    def appendDiKouInfo(self, itemInfo):
        if gameglobal.rds.configData.get('enableMallCashCoinPay', False) and itemInfo.get('priceType', 0) == uiConst.MONEY_TYPE_TIANQUAN:
            itemInfo['dikouInfo'] = uiConst.MONEY_TYPE_TIANBI

    def getMyMoneyInfo(self):
        attrValid = True
        p = BigWorld.player()
        ret = {'tianbi': 0,
         'tianquan': 0,
         'jifen': 0,
         'cash': 0,
         'unBindCoin': 0,
         'bindCoin': 0}
        attrValid &= hasattr(p, 'unbindCoin')
        attrValid &= hasattr(p, 'bindCoin')
        attrValid &= hasattr(p, 'freeCoin')
        attrValid &= hasattr(p, 'mallCash')
        attrValid &= hasattr(p, 'mallScore')
        attrValid &= hasattr(p, 'totalMallScore')
        if not attrValid:
            return ret
        ret['tianBi'] = p.unbindCoin + p.bindCoin + p.freeCoin
        ret['tianQuan'] = p.mallCash
        ret['jiFenBi'] = p.mallScore
        ret['totalJiFen'] = p.totalMallScore
        ret['cash'] = getattr(p, 'cash', 0)
        ret['unBindCoin'] = getattr(p, 'unbindCoin', 0)
        ret['bindCoin'] = getattr(p, 'bindCoin', 0) + getattr(p, 'freeCoin', 0)
        return ret

    def onGetMyMoneyInfo(self, *arg):
        return uiUtils.dict2GfxDict(self.getMyMoneyInfo(), True)

    def onOpenChargeWindow(self, *arg):
        if utils.getGameLanuage() in ('en',):
            projectId = AppSettings.get('conf/projectId', '13.2000026')
            cmd = 'start mycomgames://demandgamingform/%s' % projectId
            subprocess.Popen(cmd, shell=True)
        else:
            BigWorld.player().openRechargeFunc()

    def OnOpenChargeRewardWindow(self, *arg):
        if gameglobal.rds.configData.get('enableChargeRewardLoop', False):
            gameglobal.rds.ui.activitySale.show(uiConst.ACTIVITY_SALE_TAB_LOOP_CHARGE)
        else:
            gameglobal.rds.ui.chargeReward.show()

    def onRequestBuyHistory(self, *arg):
        BigWorld.player().base.getMallHistory()

    def onSetPreviewInfo(self, *arg):
        index = int(arg[3][0].GetNumber())
        line, row = self.globalIdx2DetailIdx(index)
        if line < 0 or line >= len(self.cacheItemsInfo):
            return
        info = self.cacheItemsInfo[line][row]
        mallId = info['mallId']
        itemId = info['itemId']
        if self.fashionPreviewLog.has_key(mallId):
            self.fashionPreviewLog[mallId][1] += 1
        else:
            self.fashionPreviewLog[mallId] = [itemId, 1]
        item = Item(itemId)
        self.uiAdapter.fittingRoom.addMallItem(item)

    def onItemSlotClick(self, *arg):
        index = int(arg[3][0].GetNumber())
        line, row = self.globalIdx2DetailIdx(index)
        if line < 0 or line >= len(self.cacheItemsInfo):
            return
        info = self.cacheItemsInfo[line][row]
        mallId = info['mallId']
        itemId = info['itemId']
        if CID.data.get(itemId, {}).get('itemQuest', []):
            gameglobal.rds.ui.itemRewardList.show(itemId)

    @ui.callFilter(3, False)
    def onQueryPointsInfo(self, *arg):
        BigWorld.player().base.queryDianKa()

    def doExchangePoints(self, pointsToBuy):
        p = BigWorld.player()
        now = p.getServerTime()
        if self.exchanging:
            if now - self.exchangStartTime < EXCHANGE_TIMEOUT:
                p.showGameMsg(GMDD.data.EXCHANGE_PENDING, ())
                return
        self.exchanging = True
        self.exchangStartTime = now
        self.exchangePending = 0
        commonPoints = p.commonPoints + p.specialPoints
        caId = gameglobal.rds.ui.easyPay.easyPayInfo.get('caId', 0)
        if commonPoints > 0:
            if pointsToBuy > commonPoints:
                self.exchangePending = pointsToBuy - commonPoints
                pointsToBuy = commonPoints
            else:
                self.exchangePending = 0
            p.base.buyCoinUseCommonPoint(pointsToBuy, caId)
        else:
            self.exchangePending = 0
            p.base.buyCoinUseStandbyPoint(pointsToBuy, caId)

    def onGetMyPointsInfo(self, *arg):
        pointsInfo = {}
        p = BigWorld.player()
        pointsInfo['account'] = getattr(p, 'roleURS', gameStrings.TEXT_RECHARGEPROXY_34)
        pointsInfo['commonPoints'] = p.commonPoints + p.specialPoints
        pointsInfo['standbyPoints'] = p.standbyPoints
        pointsInfo['allPoints'] = p.standbyPoints + p.commonPoints + p.specialPoints
        pointsInfo['rate'] = 1.0
        return uiUtils.dict2GfxDict(pointsInfo, True)

    def onSearchMallItem(self, *arg):
        self.searchKeyWord = unicode2gbk(arg[3][0].GetString())
        self.tianyuSearchHistory.addSearchHistoryData(self.searchKeyWord)
        self.tabMgr.setSelectedChildId(MAIN_TAB_SEARCH)

    def refreshSearchItem(self, searchKey):
        self.mallMediator.Invoke('refreshSearchItem', GfxValue(gbk2unicode(searchKey)))

    def onLoadComplete(self, *arg):
        withFashion = int(arg[3][0].GetNumber())
        self.uiAdapter.fittingRoom.initMallHeadGen()
        if not gameglobal.rds.ui.fittingRoom.item:
            withFashion = 0
        if withFashion:
            self.setLoadingMcVisible(False)
        else:
            self.uiAdapter.fittingRoom.restorePhoto3D()

    def onRotateFigure(self, *arg):
        index = arg[3][0].GetNumber()
        deltaYaw = -0.02 * index
        headGen = self.uiAdapter.fittingRoom.mallHeadGen
        if headGen:
            headGen.rotateYaw(deltaYaw)

    def onZoomFigure(self, *arg):
        index = arg[3][0].GetNumber()
        deltaZoom = -0.02 * index
        headGen = self.uiAdapter.fittingRoom.mallHeadGen
        if headGen:
            headGen.zoom(deltaZoom)

    def onReSetFigure(self, *arg):
        self.uiAdapter.fittingRoom.restorePhoto3D()
        headGen = self.uiAdapter.fittingRoom.mallHeadGen
        if headGen:
            headGen.resetYaw()

    def onUpdateFigure(self, *arg):
        self.uiAdapter.fittingRoom.updateFigure()

    def onGetFashionDesc(self, *arg):
        desc = self.uiAdapter.fittingRoom.getFashionDesc()
        return GfxValue(gbk2unicode(desc))

    def onGotoChargeReward(self, *arg):
        if gameglobal.rds.configData.get('enableChargeRewardLoop', False):
            gameglobal.rds.ui.activitySale.show(uiConst.ACTIVITY_SALE_TAB_LOOP_CHARGE)
        else:
            gameglobal.rds.ui.chargeReward.show()

    def onGetChargeRewardName(self, *arg):
        ret = gameglobal.rds.ui.chargeReward.getTitleInfo()
        return GfxValue(gbk2unicode(ret))

    def onChangeColor(self, *arg):
        index = int(arg[3][0].GetNumber())
        descStr = 'prbDyeLists' if self.uiAdapter.fittingRoom.isPbrEquip() else 'dyeLists'
        dyeLists = MCFD.data.get(descStr, [(), ('255,0,0,255', '255,0,0,255'), ('0,255,0,255', '0,255,0,255')])
        if index < len(dyeLists):
            dyeList = dyeLists[index]
            self.uiAdapter.fittingRoom.setDyeList(dyeList)

    def onChangeBody(self, *arg):
        index = int(arg[3][0].GetNumber()) - 1
        figureXmls = MCFD.data.get('figureInfo', ['1_3_401', '1_3_402'])
        if index == -1:
            self.uiAdapter.fittingRoom.setFigureInfo('')
        elif index < len(figureXmls):
            xmlName = figureXmls[index]
            self.uiAdapter.fittingRoom.setFigureInfo(xmlName)

    def onGetColor(self, *arg):
        dyeLists = MCFD.data.get('dyeLists', [(), ('255,0,0,255', '255,0,0,255'), ('0,255,0,255', '0,255,0,255')])
        ret = []
        for dyeList in dyeLists:
            if not dyeList:
                ret.append(-1)
            else:
                color = dyeList[0]
                color = color.split(',')
                color = [ (int(item) if int(item) <= 255 else 255) for item in color ]
                ret.append((color[0] << 16) + (color[1] << 8) + color[2])

        return uiUtils.array2GfxAarry(ret)

    def onEnterFullScreenFittingRoom(self, *arg):
        gameglobal.rds.ui.fullscreenFittingRoom.show()

    def onRegisterJishouMc(self, *arg):
        self.jishouMc = arg[3][0]

    def onUnRegisterJishouMc(self, *arg):
        self.jishouMc = None

    def onOpenJishouConfirm(self, *arg):
        if arg[3][0] is None:
            return
        else:
            self.jishouInfo = {}
            self.jishouInfo['type'] = arg[3][0].GetString()
            self.jishouInfo['price'] = int(arg[3][1].GetNumber())
            self.jishouInfo['count'] = int(arg[3][2].GetNumber())
            self.jishouInfo['coinMarketTaxRate'] = MCFD.data.get('coinMarketTaxRate', 0.02)
            gameglobal.rds.ui.loadWidget(self.jishouConfirmWidgetId, True)
            return

    def onCloseJishouConfirm(self, *arg):
        gameglobal.rds.ui.unLoadWidget(self.jishouConfirmWidgetId)
        self.jishouConfirmMediator = None

    @ui.checkInventoryLock()
    def onConfirmJishou(self, *arg):
        if self.jishouInfo is None:
            return
        else:
            expTime = MCFD.data.get('coinMarketTradeExpireTime', (86400,))[0]
            count = self.jishouInfo['count']
            price = self.jishouInfo['price']
            p = BigWorld.player()
            if self.jishouInfo['type'] == 'buy':
                BigWorld.player().base.buyCoinInMarket(count, price, expTime, p.cipherOfPerson)
            else:
                BigWorld.player().base.sellCoinInMarket(count, price, expTime, p.cipherOfPerson)
            return

    def onInitTradeBtn(self, *arg):
        return GfxValue(self.firstTradeBtnName)

    def onGetMarketInfo(self, *arg):
        p = BigWorld.player()
        ret = {}
        mcfdd = MCFD.data
        ret['buyMarket'] = self.buyMarketInfo
        ret['sellMarket'] = self.sellMarketInfo
        ret['history'] = self.marketHistoryInfo
        ret['buyMarketExtra'] = self.buyMarkeyExtra
        ret['sellMarketExtra'] = self.sellMarketExtra
        ret['cash'] = getattr(p, 'cash', 0)
        ret['unBindCoin'] = getattr(p, 'unbindCoin', 0)
        ret['bindCoin'] = getattr(p, 'bindCoin', 0) + getattr(p, 'freeCoin', 0)
        ret['myCurrentTradeList'] = self.myCoinMarketInfo
        ret['coinMarketTaxRate'] = mcfdd.get('coinMarketTaxRate', 0.02)
        ret['coinMarketMaxPrice'] = mcfdd.get('coinMarketMaxPrice', 100)
        ret['coinMarketMinPrice'] = mcfdd.get('coinMarketMinPrice', 10)
        ret['coinMarketDefaultPrice'] = mcfdd.get('coinMarketDefaultPrice', 10000)
        ret['coinMarketMinCoinLimit'] = mcfdd.get('coinMarketMinCoinLimit', 10)
        ret['coinCountMaxChars'] = mcfdd.get('coinCountMaxChars', 5)
        ret['coinPriceMaxChars'] = mcfdd.get('coinPriceMaxChars', 10)
        ret['extraCoinSegList'] = mcfdd.get('extraCoinSegList', (1000,))
        return uiUtils.dict2GfxDict(ret, True)

    def onGetMyMarketInfo(self, *arg):
        ret = self.myCoinMarketInfo[:MARKET_ITEM_NUM]
        if len(ret) < MARKET_ITEM_NUM:
            ret.extend([()] * (MARKET_ITEM_NUM - len(ret)))
        return uiUtils.array2GfxAarry(ret, True)

    def onGetMyTradeHistoryInfo(self, *arg):
        ret = self.myTradeHistroy[:MARKET_ITEM_NUM]
        if len(ret) < MARKET_ITEM_NUM:
            ret.extend([()] * (MARKET_ITEM_NUM - len(ret)))
        return uiUtils.array2GfxAarry(ret, True)

    @ui.callFilter(2, False)
    def onQueryCoinMarket(self, *arg):
        BigWorld.player().base.queryCurrentCoinMarketTrade()
        BigWorld.player().base.queryCoinMarket(self.coinMaketVersion)

    @ui.callFilter(3, False)
    def onQueryMyTradeInfo(self, *arg):
        BigWorld.player().base.queryCurrentCoinMarketTrade()
        BigWorld.player().base.queryCoinMarketTradeHistory()

    def onDeleteOrder(self, *arg):
        self.cancelCoinMarketIndex = int(arg[3][0].GetNumber())
        if self.cancelCoinMarketIndex < 0 or self.cancelCoinMarketIndex >= len(self.myCoinMarketInfo):
            return
        marketInfo = self.myCoinMarketInfo[self.cancelCoinMarketIndex]
        msg = gameStrings.TEXT_TIANYUMALLPROXY_2196
        if marketInfo[1] == const.COIN_MARKET_OP_BUY_COIN:
            msg += gameStrings.TEXT_TIANYUMALLPROXY_2198 + str(marketInfo[3] * marketInfo[4])
        else:
            msg += gameStrings.TEXT_TIANYUMALLPROXY_2200 + str(marketInfo[3])
        msg += gameStrings.TEXT_TIANYUMALLPROXY_2202
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.onCancelOrder)

    def onCancelOrder(self):
        if self.cancelCoinMarketIndex < 0 or self.cancelCoinMarketIndex >= len(self.myCoinMarketInfo):
            return
        BigWorld.player().base.cancelCoinMarketTrade(self.myCoinMarketInfo[self.cancelCoinMarketIndex][2])

    def onRegisterVipMc(self, *arg):
        self.vipMc = arg[3][0]

    def onUnRegisterVipMc(self, *arg):
        self.vipMc = None

    def onRegisterAppVipMc(self, *arg):
        self.tianyuAppVipPanel.onWidgetRegister(arg[3][0], self)

    def onUnRegisterAppVipMc(self, *arg):
        self.tianyuAppVipPanel.onWidgetUnRegister()

    def onOpenVipBasicPackageConfirm(self, *arg):
        p = BigWorld.player()
        firstBuy = False
        if not p.vipBasicPackage and MCFD.data.get('vipFirstBuyDaysList', {}) and MCFD.data.get('vipFirstBuyBasicPackage', 0):
            gameStrings.TEXT_TIANYUMALLPROXY_1647
            self.confirmBuyMallId = MCFD.data.get('vipFirstBuyBasicPackage', -1)
            firstBuy = True
        else:
            self.confirmBuyMallId = MCFD.data.get('vipBasicPackage', -1)
        self.confirmBuyNum = 0
        self.confirmBuyType = 'vipBasic.0'
        giftPackages = self.getGiftMallItems(self.confirmBuyMallId) if firstBuy else ()
        if giftPackages:
            gameglobal.rds.ui.loadWidget(self.vipDiscountWidgetId, True)
        else:
            gameglobal.rds.ui.loadWidget(self.buyVipWidgetId, True)

    def getGiftMallItems(self, basicPackageMid):
        if not self.vipGiftConfig():
            return []
        packageId = MID.data.get(basicPackageMid, {}).get('packageID', 0)
        giftItems = VPD.data.get(packageId, {}).get('giftMallIds', [])
        return list(giftItems)

    def getGiftMallData(self, giftMids):
        ret = []
        for mid in giftMids:
            info = genMallItemInfo(mid)
            if info == {}:
                continue
            if info.get('soldOut', 0) == 1:
                continue
            ret.append(info)

        return ret

    def onCloseVipBasicPackageConfirm(self, *arg):
        gameglobal.rds.ui.unLoadWidget(self.buyVipWidgetId)
        self.buyVipMediator = None
        self.pendingBuyMallId = 0
        self.pendingBuyType = 0

    def onCloseCompensateBuyConfirm(self, *arg):
        gameglobal.rds.ui.unLoadWidget(self.compensateBugWidgetId)

    def onConfirmCompensateBuy(self, *arg):
        times = int(arg[3][0].GetNumber())
        BigWorld.player().cell.getVipCompensateAward(times)
        self.onCloseCompensateBuyConfirm()

    def onGetSearchHistory(self, *arg):
        ret = self.tianyuSearchHistory.getReverseHistoryList()
        return uiUtils.array2GfxAarry(ret, True)

    def onOpenWebMall(self, *arg):
        gameglobal.rds.ui.mallWeb.show()

    def onOpenOutsideUrl(self, *args):
        picIndex = int(args[3][0].GetNumber())
        urlPath = MCFD.data.get('combineTianyuMallOutsideUrl', {}).get(picIndex, 'https://ty.163.com/index.html')
        BigWorld.openUrl(urlPath)

    def onOpenXiuChang(self, *arg):
        gameglobal.rds.ui.mallWeb.show()

    def onCloseVipDiscount(self, *arg):
        self.vipDiscountMediator = None
        gameglobal.rds.ui.unLoadWidget(self.vipDiscountWidgetId)
        self.pendingBuyMallId = 0
        self.pendingBuyType = 0

    @ui.callFilter(3)
    @ui.checkInventoryLock()
    def onConfirmBuyVipBasicPackage(self, *arg):
        p = BigWorld.player()
        days = int(arg[3][0].GetNumber())
        packageId = MID.data.get(self.confirmBuyMallId, {}).get('packageID', -1)
        if packageId <= 0:
            return
        myBasicPackageId = p.vipBasicPackage.get('packageID', 0)
        myBpInRange = uiUtils.hasVipBasic()
        if uiUtils.IsVipBasicSimple(packageId) and uiUtils.hasVipBasicFirst():
            p.cell.buyVipPackages(self.confirmBuyMallId, days, [], [], p.cipherOfPerson)
            return
        if myBpInRange and VPD.data.get(myBasicPackageId, {}).get('noExpend', 0):
            gameglobal.rds.ui.messageBox.showMsgBox(gameStrings.TEXT_TIANYUMALLPROXY_2322)
            return
        p.cell.buyVipPackages(self.confirmBuyMallId, days, [], [], p.cipherOfPerson)

    def checkVipBonus(self):
        p = BigWorld.player()
        now = p.getServerTime()
        for sid, expire, take in p.vipDailyBonus:
            invalid = VSD.data.get(sid, {}).get('invalid', 0)
            if not take and now < expire and not invalid:
                return True

        for sid, expire, take in p.vipWeeklyBonus:
            invalid = VSD.data.get(sid, {}).get('invalid', 0)
            if not take and now < expire and not invalid:
                return True

        return False

    @ui.uiEvent(uiConst.WIDGET_COMBINE_TIANYU_MALL, events.EVENT_EXP_BONUS_UPDATE)
    def refreshVipRoleInfo(self):
        self.vipBonusPush()
        if self.vipMc is None:
            return
        else:
            self.vipMc.Invoke('refreshVipPanel')
            return

    def vipBonusPush(self):
        hasBonus = self.checkVipBonus()
        hasPushed = gameglobal.rds.ui.pushMessage.hasMsgType(uiConst.MESSAGE_TYPE_VIP_BONUS)
        if hasBonus and not hasPushed:
            callBackDict = {'click': self.showVipTab}
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_VIP_BONUS)
            gameglobal.rds.ui.pushMessage.setCallBack(uiConst.MESSAGE_TYPE_VIP_BONUS, callBackDict)
        elif not hasBonus and hasPushed:
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_VIP_BONUS)

    def initPushPackageInfos(self):
        infos = {k:v for k, v in VPD.data.iteritems() if v.get('pushPriority')}
        return sorted(infos.iteritems(), key=lambda d: d[1].get('pushPriority'))

    def vipExpirePushEx(self):
        p = BigWorld.player()
        now = utils.getNow()
        if not p.vipBasicPackage:
            return
        else:
            earlyRemindMsgId = None
            laterRemindMsgId = None
            for packageId, packageInfo in self.pushPackageInfos:
                if packageInfo.get('isBasic'):
                    if p.vipBasicPackage.get('packageID') != packageId:
                        continue
                    overDueTime = BigWorld.player().vipBasicPackage.get('tExpire', 0)
                else:
                    if not p.vipAddedPackage.get(packageId):
                        continue
                    overDueTime = p.vipAddedPackage.get(packageId, {}).get('tExpire', 0)
                earlyId = self.getEarlyRemindInfo(packageInfo, now, overDueTime)
                laterId = self.getLaterRemindInfo(packageInfo, now, overDueTime)
                if earlyId:
                    earlyRemindMsgId = earlyId
                if laterId:
                    laterRemindMsgId = laterId

            if p.vipBasicPackage.get('packageID') == uiConst.VIP_FIRSTBUY_PACKAGE_ID:
                earlyRemindMsgId = None
            if self.updatePushDate(earlyRemindMsgId, now):
                self.updatePushMsg(earlyRemindMsgId, MSG_EARLY_REMIND_LIST)
            if self.updatePushDate(laterRemindMsgId, now):
                self.updatePushMsg(laterRemindMsgId, MSG_LATER_REMIND_LIST)
            return

    def getEarlyRemindInfo(self, packageInfo, nowTime, overDueTime):
        earlyRemindTime = packageInfo.get('earlyRemindTime', 3) * const.TIME_INTERVAL_DAY
        if overDueTime - earlyRemindTime <= nowTime < overDueTime:
            return packageInfo.get('pushEarlyMsgId')
        else:
            return None

    def getLaterRemindInfo(self, packageInfo, nowTime, overDueTime):
        laterRemindTime = packageInfo.get('laterRemindTime', 3) * const.TIME_INTERVAL_DAY
        if overDueTime <= nowTime < overDueTime + laterRemindTime:
            return packageInfo.get('pushLaterMsgId')
        else:
            return None

    def updatePushMsg(self, newMsg, msgList):
        oldMsg = self.uiAdapter.pushMessage.hasMsgInMsgList(msgList)
        if not newMsg and oldMsg:
            self.uiAdapter.pushMessage.removePushMsg(oldMsg)
        elif newMsg != oldMsg:
            self.uiAdapter.pushMessage.removePushMsg(oldMsg)
            self.uiAdapter.pushMessage.addPushMsg(newMsg)
            self.uiAdapter.pushMessage.setCallBack(newMsg, {'click': Functor(self.onMsgClick, newMsg)})

    def onMsgClick(self, msgId):
        if msgId in MSG_BASIC_REMIND_LSIT:
            self.tutorialBuyVip()
        elif msgId in MSG_TRAVEL_REMIND_LIST:
            self.pendingBuyVipAddedPackage(uiConst.VIP_TRAVEL_PACKAGE_MALL_ITEMID)
        elif msgId in MSG_EXP_REMIND_LIST:
            self.pendingBuyVipAddedPackage(uiConst.VIP_EXP_PACKAGE_MALL_ITEMID)
        elif msgId in MSG_PVP_REMIND_LIST:
            self.pendingBuyVipAddedPackage(uiConst.VIP_PVP_PACKAGE_MALL_ITEMID)

    def genVipProp(self, serviceList):
        ret = []
        now = BigWorld.player().getServerTime()
        for s in serviceList:
            sid, expire = s
            if expire <= now:
                continue
            svsData = VSD.data.get(sid, {})
            if svsData.get('invalid', 0) == 1:
                continue
            if not svsData.get('propDesc', None):
                continue
            item = {}
            item['desc'] = svsData.get('propDesc', gameStrings.TEXT_TIANYUMALLPROXY_675 + str(sid))
            item['expire'] = expire - now
            ret.append(item)

        return ret

    def genVipFunc(self, svcList):
        ret = []
        now = BigWorld.player().getServerTime()
        for s in svcList:
            sid, expire = s
            if expire <= now:
                continue
            svsData = VSD.data.get(sid, {})
            if svsData.get('invalid', 0) == 1:
                continue
            if svsData.get('serviceType', 1) != 4:
                continue
            if not svsData.get('propDesc', None):
                continue
            item = {}
            item['desc'] = svsData.get('propDesc', gameStrings.TEXT_TIANYUMALLPROXY_675 + str(sid))
            item['expire'] = expire - now
            item['funcName'] = svsData.get('funcName', None)
            item['funcTitle'] = svsData.get('funcTitle', (gameStrings.TEXT_TIANYUMALLPROXY_2492, gameStrings.TEXT_TIANYUMALLPROXY_2492))
            item['extraParam'] = svsData.get('extraParam', (0,))
            if not item['funcName']:
                continue
            ret.append(item)

        return ret

    def getUnTakeVipBonusCount(self, vipDailyBonus):
        vipBonuses = self.genVipBonusInfo(vipDailyBonus)
        count = 0
        for bonus in vipBonuses:
            if bonus and not bonus.get('taken'):
                count = count + 1

        return count

    def genVipBonusInfo(self, svcList):
        ret = []
        now = BigWorld.player().getServerTime()
        for s in svcList:
            sid, expire, taken = s
            if expire <= now:
                continue
            svsData = VSD.data.get(sid, {})
            if svsData.get('serviceType', 1) != 2:
                continue
            if svsData.get('invalid', 0) == 1:
                continue
            bonusId = svsData.get('bonusId', 0)
            if bonusId == 0:
                continue
            bonusData = BD.data.get(bonusId, {})
            fixedBonus = bonusData.get('fixedBonus', ())
            fixedBonus = utils.filtItemByConfig(fixedBonus, lambda e: (e[1] if e[0] == gametypes.BONUS_TYPE_ITEM else None))
            if len(fixedBonus) <= 0:
                continue
            bonusType, bonusItemId, bonusNum = fixedBonus[0]
            if bonusType != gametypes.BONUS_TYPE_ITEM:
                continue
            itemInfo = {'itemId': bonusItemId}
            appendBasicItemInfo(itemInfo)
            itemInfo['count'] = bonusNum
            itemInfo['taken'] = taken
            itemInfo['sid'] = sid
            ret.append(itemInfo)

        return ret

    def onGetVipRoleInfo(self, *arg):
        ret = {}
        p = BigWorld.player()
        serviceProp = []
        serviceFunc = []
        basicPackageSvc = p.vipBasicPackage.get('services', [])
        serviceProp.extend(self.genVipProp(basicPackageSvc))
        serviceFunc.extend(self.genVipFunc(basicPackageSvc))
        for pkg in p.vipAddedPackage:
            addedPackageSvc = p.vipAddedPackage[pkg].get('services', [])
            serviceProp.extend(self.genVipProp(addedPackageSvc))
            serviceFunc.extend(self.genVipFunc(addedPackageSvc))

        ret['basicExpire'] = p.vipBasicPackage.get('tExpire', 0)
        ret['serviceProp'] = serviceProp
        ret['serviceFunc'] = serviceFunc
        ret['dailyBonus'] = self.genVipBonusInfo(p.vipDailyBonus)
        ret['weeklyBonus'] = self.genVipBonusInfo(p.vipWeeklyBonus)
        ret['tipData'] = self.genVipBasicPackageTipInfo()
        ret['vipCompensateCnt'] = BigWorld.player().vipCompensateCnt
        ret['unTakeVipBonusCount'] = self.getUnTakeVipBonusCount(p.vipDailyBonus)
        ret['basicPackageBuyRecordStr'] = self.getBasicPackageBuyShowInfo(p.basicPackageBuyRecord)
        return uiUtils.dict2GfxDict(ret, True)

    def genVipBasicPackageTipInfo(self):
        ret = {}
        p = BigWorld.player()
        if not p.vipBasicPackage:
            mid = MCFD.data.get('vipFirstBuyBasicPackage', 0)
        else:
            mid = MCFD.data.get('vipBasicPackage', 0)
        ret['mallId'] = mid
        ret['packageID'] = MID.data.get(mid, {}).get('packageID', 0)
        ret['itemId'] = MID.data.get(mid, {}).get('itemId', 0)
        return ret

    def getBasicPackageBuyShowInfo(self, basicPackageBuyRecord):
        result = gameStrings.MALL_ACTICATE_SERVICE_SHOW
        if basicPackageBuyRecord is None:
            return result
        else:
            return result + gameStrings.MALL_BASICPACKAGE_BUYRECORD_SHOW % basicPackageBuyRecord[1]

    def onTakeVipBonus(self, *arg):
        sid = int(arg[3][0].GetNumber())
        BigWorld.player().cell.getVipAward(sid)

    def onGetDoubleExpInfo(self, *arg):
        ret = {}
        ret['freeze'] = gameglobal.rds.ui.expBonus.isFreezed
        ret['remainTime'] = gameglobal.rds.ui.expBonus.getTotalRemainTime()
        return uiUtils.dict2GfxDict(ret, True)

    @ui.callFilter(3)
    def onToggleDoubleExp(self, *arg):
        totalTime = gameglobal.rds.ui.expBonus.getTotalRemainTime()
        if totalTime <= 0:
            msg = GMD.data.get(GMDD.data.NONE_REMAIN_EXP_BONUS, {}).get('text', gameStrings.TEXT_EXPBONUSPROXY_76)
        elif gameglobal.rds.ui.expBonus.isFreezed:
            msg = GMD.data.get(GMDD.data.CONFIRM_TO_UNFREEZE_EXP_BONUS, {}).get('text', gameStrings.TEXT_EXPBONUSPROXY_79) % utils.formatTimeStr(totalTime, gameStrings.TEXT_EXPBONUSPROXY_79_1)
        else:
            msg = GMD.data.get(GMDD.data.CONFIRM_TO_FREEZE_EXP_BONUS, {}).get('text', gameStrings.TEXT_EXPBONUSPROXY_81) % utils.formatTimeStr(totalTime, gameStrings.TEXT_EXPBONUSPROXY_79_1)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.onConfirmToggleDoubleExp)

    def onConfirmToggleDoubleExp(self):
        p = BigWorld.player()
        if gameglobal.rds.ui.expBonus.isFreezed:
            p.cell.unfreezeExpBonusVip()
        else:
            p.cell.freezeExpBonusVip()

    def onOpenVipExpBonus(self, *arg):
        funcId = int(arg[3][0].GetNumber())
        gameglobal.rds.ui.expBonus.show(0, funcId, True)

    def checkTianyuMallImagesExist(self):
        if gameglobal.rds.configData.get('enableRemotePic', False):
            self.checkImageExist = False
            mallPath = ADVERTISEMENT_PATH + uiConst.REMOTE_PIC_MALL
            vipPath = ADVERTISEMENT_PATH + uiConst.REMOTE_PIC_VIP
            self.checkImages(mallPath)
            self.checkImages(vipPath)

    def checkImages(self, path):
        picNum = AppSettings.get(path + '/picNum', -1) + 1
        for i in range(picNum):
            PIC_NUMBER = '/PIC' + str(i)
            ASAP_ICONNAME = path + PIC_NUMBER + '/iconName'
            iconPath = const.IMAGES_DOWNLOAD_DIR + '/' + AppSettings.get(ASAP_ICONNAME, '') + '.dds'
            if not clientcom.isFileExist(iconPath):
                AppSettings[path + '/version'] = 0

    def onEnterTuZhuang(self, *arg):
        gameglobal.rds.ui.tuZhuang.show()

    def onOpenCompensateTake(self, *arg):
        self.uiAdapter.loadWidget(self.compensateBugWidgetId, True)

    def onTakeAllVipReward(self, *arg):
        p = BigWorld.player()
        count = self.getUnTakeVipBonusCount(p.vipDailyBonus)
        cntEmpty = p.inv.countBlankInPages()
        if count > cntEmpty:
            p.showGameMsg(GMDD.data.TAKE_ALL_VIP_BONUS_BAG_FULL, ())
            return
        p.cell.getAllVipAward()

    def updatePushDate(self, pushMsgId, nowTime):
        if not pushMsgId:
            return True
        else:
            key = keys.SET_VIPPACKAGE_PUSH + '/%d/%d' % (BigWorld.player().gbId, pushMsgId)
            oldTime = AppSettings.get(key, 0)
            if utils.isSameDay(nowTime, oldTime):
                return False
            AppSettings[key] = nowTime
            AppSettings.save()
            return True


def appendBasicItemInfo(item):
    itemId = item.get('itemId', 0)
    itemInfo = ID.data.get(itemId, {})
    icon = uiUtils.getItemIconFile64(itemId)
    iconLarge = uiConst.ITEM_ICON_IMAGE_RES_110 + str(itemInfo.get('icon', 'notFound')) + '.dds'
    name = itemInfo.get('name', gameStrings.TEXT_TIANYUMALLPROXY_1455)
    mwrap = itemInfo.get('mwrap', 1)
    if item.get('many', 0) > 1:
        mwrap = mwrap / item.get('many', 1)
        name = name + gameStrings.TEXT_HISTORYCONSUMEDPROXY_256 + str(item.get('many', 0))
    item['name'] = name
    item['qualityColor'] = 'white'
    item['color'] = 'nothing'
    item['iconPath'] = icon
    item['iconPathLarge'] = iconLarge
    item['mwrap'] = mwrap


def checkCanDiscount(itemId):
    p = BigWorld.player()
    pg, ps = p.inv.findItemInPages(itemId, enableParentCheck=True)
    return not (pg, ps) == (const.CONT_NO_PAGE, const.CONT_NO_POS)


def genMallItemInfo(mallId):
    info = copy.deepcopy(MID.data.get(mallId, {}))
    if info == {}:
        return {}
    appendBasicItemInfo(info)
    info['mallId'] = mallId
    info['srcType'] = 'mall'
    return info


def isItemFilteredByServer(mallId):
    p = BigWorld.player()
    hostId = utils.getHostId()
    itemData = MID.data.get(mallId, {})
    serverIncludeList = itemData.get('serverIncludeList', ())
    if serverIncludeList:
        for serverId in serverIncludeList:
            if hostId == serverId:
                return False

        return True
    return False


def isAllMileStoneFinished(spData):
    if isinstance(spData, int):
        if not BigWorld.player().checkServerProgress(spData, False):
            return False
    elif isinstance(spData, tuple):
        for spId in spData:
            if not BigWorld.player().checkServerProgress(spId, False):
                return False

    elif isinstance(spData, list):
        anyFinished = False
        for spId in spData:
            if BigWorld.player().checkServerProgress(spId, False):
                anyFinished = True
                break

        if not anyFinished:
            return False
    return True


class Tab(object):

    def __init__(self, tabId):
        self.children = None
        self.selChildId = 0
        self.tabId = tabId

    def getChild(self, childId):
        if self.children is None:
            return
        else:
            return self.children.get(childId, None)

    def setSelectedChildId(self, chId):
        self.selChildId = chId

    def getSelChild(self):
        return self.getChild(self.selChildId)

    def systemFixed(self):
        return False

    def getChildrenInfo(self):
        ret = []
        listIdx = list(self.children)
        listIdx.sort()
        for idx in xrange(len(listIdx)):
            tabId = listIdx[idx]
            child = self.getChild(tabId)
            if child.systemFixed():
                if self.selChildId == tabId and tabId < MAIN_TAB_FIXED:
                    self.selChildId = listIdx[(idx + 1) % len(listIdx)]
                continue
            info = child.getTabInfo()
            ret.append(info)

        ret.append(len(ret))
        ret.append(self.selChildId)
        return ret

    def getTabInfo(self):
        return {}

    def reset(self):
        pass


class TabManager(Tab):

    def __init__(self):
        super(TabManager, self).__init__(0)
        self.selChildId = MAIN_TAB_HOMEPAGE
        self.mse = MallSearchEngine()
        self.preOpenMainTab = MAIN_TAB_HOMEPAGE
        self.preOpenSubTab = 0
        self.enableNeteaseMemberShip = False

    def initTabs(self):
        showNeteaseMemberShip = gameglobal.rds.configData.get('enableNeteaseGameMembershipRights', False) and not gameglobal.rds.configData.get('hideNeteaseGameMembershipMall', False)
        if self.children is not None and self.enableNeteaseMemberShip == showNeteaseMemberShip:
            return
        else:
            self.enableNeteaseMemberShip = showNeteaseMemberShip
            self.children = {}
            mcdd = MCD.data
            for key in mcdd.keys():
                mainId, subId = key
                data = mcdd[key]
                serverProgressMsId = data.get('spId', 0)
                if serverProgressMsId and not isAllMileStoneFinished(serverProgressMsId):
                    continue
                if not self.children.has_key(mainId):
                    if mainId == MAIN_TAB_HOMEPAGE:
                        self.children[mainId] = HomeTab(mainId)
                    else:
                        self.children[mainId] = MainTab(mainId)
                self.children[mainId].appendSubTab(subId, data)

            if not self.children.has_key(MAIN_TAB_JISHOU):
                self.children[MAIN_TAB_JISHOU] = MainTab(MAIN_TAB_JISHOU)
            if not self.children.has_key(MAIN_TAB_VIP):
                self.children[MAIN_TAB_VIP] = MainTab(MAIN_TAB_VIP)
                self.children[MAIN_TAB_VIP].appendSubTab(1, MCFD.data.get('vipValues', {}))
            if self.enableNeteaseMemberShip:
                if not self.children.has_key(MAIN_TAB_APP_VIP):
                    self.children[MAIN_TAB_APP_VIP] = MainTab(MAIN_TAB_APP_VIP)
            self.reset()
            return

    def openSpetialTab(self, mainTab, subTab):
        self.preOpenMainTab = mainTab
        self.preOpenSubTab = subTab

    def prepareOpen(self):
        self.setSelectedChildId(self.preOpenMainTab)
        selMainTab = self.getSelChild()
        if selMainTab is None:
            return
        else:
            if self.preOpenSubTab:
                selMainTab.setSelectedChildId(self.preOpenSubTab)
            else:
                selMainTab.reset()
            return

    def reset(self):
        if self.children is None:
            return
        else:
            for chId in self.children:
                self.getChild(chId).reset()

            return

    def searchByKeyWord(self, keyWord, scope = SEARCH_SCOPE_ALL):
        ret = {}
        result = []
        self.mse.setKeyWord(keyWord)
        mainTabKeys = list(self.children)
        mainTabKeys.sort()
        searchTabKeys = mainTabKeys[1:]
        for key in searchTabKeys:
            if key == MAIN_TAB_APP_VIP:
                continue
            mainTab = self.getChild(key)
            if mainTab.systemFixed():
                continue
            if scope == SEARCH_SCOPE_FITTING_ROOM and mainTab.fsPreviewTabNum <= 0:
                continue
            allItems = mainTab.getAllItemsInfo(scope)
            for item in allItems:
                if item['mallId'] in map(lambda item: item['mallId'], result):
                    continue
                if self.mse.match(item):
                    result.append(item)

        ret['searchTab'] = True
        ret['itemsInfo'] = result
        return ret

    def searchByMallId(self, mallId):
        ret = {}
        result = []
        found = False
        mainTabKeys = list(self.children)
        mainTabKeys.sort()
        searchTabKeys = mainTabKeys[1:]
        for key in searchTabKeys:
            allItems = self.getChild(key).getAllItemsInfo()
            for item in allItems:
                if mallId == item['mallId']:
                    result.append(item)
                    found = True
                    break

            if found:
                break

        ret['searchTab'] = True
        ret['itemsInfo'] = result
        return ret


class MainTab(Tab):
    mainTabCfgData = MCFD.data.get('mainTabsConfig', {})

    def __init__(self, mainId):
        super(MainTab, self).__init__(mainId)
        self.selChildId = SUB_TAB_ALL
        configData = MainTab.mainTabCfgData.get(mainId, {})
        self.name = configData.get('name', '')
        self.image = configData.get('image', '')
        self.fsPreviewTabNum = 0
        self.children = {}

    def __str__(self):
        return str(self.tabId) + ' ' + str(self.name) + ' ' + str(self.image)

    def appendSubTab(self, subId, data):
        if self.children.has_key(subId):
            return
        subTab = SubTab(subId, data)
        self.children[subId] = subTab
        self.fsPreviewTabNum += subTab.data.get('fullscreenPreview', 0)

    def appendSubInvTab(self, subId, data, items):
        if self.children.has_key(subId):
            return
        subTab = SubInvTab(subId, data)
        subTab.appendInvItems(items)
        self.children[subId] = subTab

    def getTabInfo(self):
        info = {}
        info['mainId'] = self.tabId
        info['name'] = self.name
        info['image'] = self.image
        info['fsPreview'] = self.fsPreviewTabNum > 0
        info['redPotVisible'] = self.isRedPotVisible()
        return info

    def isRedPotVisible(self):
        for subTab in self.children.values():
            if subTab.getTabInfo().get('redPotVisible', False):
                return True

        return False

    def getAllItemsInfo(self, scope = SEARCH_SCOPE_ALL):
        ret = []
        listIdx = list(self.children)
        listIdx.sort()
        for idx in listIdx:
            subTab = self.getChild(idx)
            if scope == SEARCH_SCOPE_FITTING_ROOM and not subTab.data.get('fullscreenPreview', 0):
                continue
            ret.extend(subTab.getChildrenInfo())

        return ret

    def systemFixed(self):
        return self.tabId >= MAIN_TAB_FIXED

    def reset(self):
        if not ENABLE_SUB_TAB_ALL and len(self.children) > 0:
            listIdx = list(self.children)
            listIdx.sort()
            self.selChildId = listIdx[0]
            self.setSelfTab(listIdx)
        else:
            self.selChildId = SUB_TAB_ALL

    def setSelfTab(self, listIdx):
        if self.tabId == MCFD.data.get('fashionTabId', 4):
            p = BigWorld.player()
            physique = getattr(p, 'physique', None)
            pSex = getattr(physique, 'sex', -1)
            if pSex == const.SEX_MALE:
                self.selChildId = listIdx[0]
            elif pSex == const.SEX_FEMALE:
                self.selChildId = listIdx[1]


class HomeTab(MainTab):

    def reset(self):
        if ENABLE_SUB_TAB_ALL:
            self.selChildId = SUB_TAB_ALL
            return
        for subId, subTab in self.children.iteritems():
            if int(self.isNewServer()) == subTab.data.get('newServerRecommend', 0):
                self.setSelectedChildId(subId)
                return

        super(HomeTab, self).reset()

    def isNewServer(self):
        return utils.getServerOpenDays() <= MCFD.data.get('newServerDays', 10)


class SubTab(Tab):

    def __init__(self, subId, data):
        super(SubTab, self).__init__(subId)
        self.data = data
        self.previewAble = data.get('preview', 0)
        self.name = data.get('subTab', '')
        self.canbuyFilter = data.get('canBuyFilter', 0)
        self.showRule = data.get('showRule', 0)
        self.isRandom = self.data.get('isRandom', 0)
        self.mallProxy = gameglobal.rds.ui.tianyuMall
        self.children = []
        self.mallIdList = []
        self.brokenChildren = []
        self.brokenMallIdList = []
        self.initItemInfo()

    def __str__(self):
        return str(self.tabId)

    def getTabInfo(self):
        info = {}
        info['subId'] = self.tabId
        info['name'] = self.name
        info['preview'] = self.previewAble
        info['fsPreview'] = self.data.get('fullscreenPreview', 0)
        info['redPotVisible'] = self.isRedPotVisible()
        return info

    def systemFixed(self):
        if self.showRule == TAB_SHOW_RULE_DISCOUNT:
            p = BigWorld.player()
            for pg in p.inv.getPageTuple():
                for ps in p.inv.getPosTuple(pg):
                    it = p.inv.getQuickVal(pg, ps)
                    if it == const.CONT_EMPTY_VAL:
                        continue
                    if it.isMallDiscount():
                        mallDiscountShowTab = CID.data.get(it.id, {}).get('mallDiscountShowTab', (None, None))
                        if self.data.get('id', 0) == mallDiscountShowTab[0] and self.data.get('subId', 0) == mallDiscountShowTab[1]:
                            return False

            return True
        elif self.showRule == TAB_SHOW_RULE_HISTORY_CONSUME:
            if not gameglobal.rds.configData.get('enableNoHistoryConsumedBuy', False):
                return True
            if utils.getHistoryConsumedActId() <= 0:
                return True
            if self.mallProxy.historyConsumedStatus == gametypes.HISTORY_CONSUMED_STATUS_JOINED:
                return True
            for mallId in self.mallIdList:
                latestTime = 0
                info = MID.data.get(mallId, {})
                showTime = info.get('soldOutDaysFromHostStart', 0) * 24 * 60 * 60
                if showTime > latestTime:
                    latestTime = showTime
                if utils.getNow() >= latestTime + utils.getServerOpenTime():
                    return True

            return False
        else:
            return False

    def getChildrenInfo(self):
        return self.children

    def isRedPotVisible(self):
        mallItems = self.getChildrenInfo()
        for mallItemInfo in mallItems:
            if mallItemInfo.get('showRedPot', 0):
                if mallItemInfo.get('canBuy', 0):
                    if gameglobal.rds.ui.tianyuMall.isMallItemCanBuy(mallItemInfo):
                        return True

        return False

    def initItemInfo(self):
        values = self.data.get('value', ())
        for i in range(len(values)):
            mallId = values[i][0]
            mallLabel = values[i][1]
            if isItemFilteredByServer(mallId):
                continue
            info = genMallItemInfo(mallId)
            if info == {}:
                continue
            if info.get('soldOut', 0) == 1:
                continue
            serverProgressMsId = info.get('spId', 0)
            if serverProgressMsId and not isAllMileStoneFinished(serverProgressMsId):
                continue
            if self.mallProxy.getSellTimeState(mallId) in (SELL_BEFORE_TIME, SELL_AFTER_TIME):
                if info.get('invisibleForPromotion'):
                    continue
                if self.mallProxy.getSellTimeState(mallId) == SELL_AFTER_TIME and info.get('invisibleForTimeLimit'):
                    continue
            buyFlag, name = self.mallProxy.mallItemCanBuyCheck(mallId, BigWorld.player())
            info['canBuy'] = buyFlag == self.mallProxy.MALL_CAN_BUY_OK
            info['state'] = uiConst.ITEM_NORMAL
            if self.canbuyFilter == uiConst.MALL_FILTER_TYPE_HIDE:
                ignore = not info['canBuy']
                if ignore:
                    continue
            elif self.canbuyFilter == uiConst.MALL_FILTER_TYPE_GARY:
                ignore = not info['canBuy']
                if ignore:
                    info['state'] = uiConst.EQUIP_BROKEN
                    self.brokenChildren.append(info)
                    self.brokenMallIdList.append(mallId)
                    continue
            if info.get('historyConsumeFlag', 0):
                if gameglobal.rds.configData.get('enableNoHistoryConsumedBuy', False):
                    if self.mallProxy.historyConsumedStatus == gametypes.HISTORY_CONSUMED_STATUS_JOINED:
                        continue
            if info.get('soldOutDaysFromHostStart', 0):
                if utils.getNow() >= utils.getServerOpenTime() + info.get('soldOutDaysFromHostStart', 0) * 24 * 60 * 60:
                    continue
            info['label'] = mallLabel
            if len(values[i]) >= 3:
                info['linkId'] = values[i][2]
            self.children.append(info)
            self.mallIdList.append(mallId)

        self.children.extend(self.brokenChildren)
        self.mallIdList.extend(self.brokenMallIdList)

    def getChild(self, childId):
        if self.children is None:
            return
        elif childId < 0 or childId >= len(self.children):
            return
        else:
            return self.children[childId]


class SubInvTab(SubTab):

    def __init__(self, subId, data):
        super(SubInvTab, self).__init__(subId, data)

    def appendInvItems(self, items):
        for pg, ps, item in items:
            mallId = -1
            mallLabel = 0
            info = {'page': pg,
             'pos': ps,
             'mallId': mallId,
             'itemId': item.id,
             'label': mallLabel}
            appendBasicItemInfo(info)
            info['itemName'] = info['name']
            info['priceType'] = gametypes.MALL_PRICE_TYPE_COIN
            info['priceVal'] = 0
            self.children.append(info)
            self.mallIdList.append(mallId)


class MallSearchEngine(object):

    def setKeyWord(self, k):
        self.keyWord = gbk2unicode(k)

    def match(self, mallItem):
        match = False
        name = gbk2unicode(mallItem.get('name', ''))
        matchField = gbk2unicode(mallItem.get('matchField', ''))
        match = match or name.find(self.keyWord) >= 0
        match = match or matchField.find(self.keyWord) >= 0
        return match


class MallPicGroup(RemotePicGroup):

    def __init__(self):
        super(MallPicGroup, self).__init__()
        self.remoteKey = uiConst.REMOTE_PIC_MALL
        self.path = ADVERTISEMENT_PATH + self.remoteKey + '/'

    def downloadADOver(self):
        self.writeList2config()
        ret = self.getLocalPicInfoList()
        gameglobal.rds.ui.tianyuMall.mallPicDownloadDone(ret)

    def writeList2config(self):
        if self.dloadedPicList:
            for i, item in enumerate(self.dloadedPicList):
                maxi = i
                retItem = {}
                pathGroup = self.getPathGroup(i)
                paramMap = eval(item.get('param', '1'))
                AppSettings[pathGroup['ASAP_MAINID']] = paramMap.get('mainId', 1)
                AppSettings[pathGroup['ASAP_TYPE']] = paramMap.get('type', 1)
                AppSettings[pathGroup['ASAP_SUBID']] = paramMap.get('subId', 1)
                AppSettings[pathGroup['ASAP_ICONNAME']] = item.get('url', '1')

            AppSettings[self.path + 'picNum'] = str(maxi)
            AppSettings[self.path + 'version'] = self.remoteVersion
            self.reset()

    def getBuiltInPicInfoList(self):
        ret = []
        hasVip = bool(BigWorld.player().vipBasicPackage)
        vip_icon = 'vip_1'
        adInfo = MCFD.data.get('adHomePage', ())
        for item in adInfo:
            icon = item.get('icon', '1')
            if hasVip and icon == vip_icon:
                continue
            if not hasVip and icon != vip_icon:
                continue
            item['iconPath'] = AD_ICON_TEMPLATE % str(item.get('icon', '1'))
            ret.append(item)

        return ret

    def getLocalPicInfoList(self):
        localAdList = []
        hasVip = bool(BigWorld.player().vipBasicPackage)
        picNum = AppSettings.get(self.path + 'picNum', -1) + 1
        for i in range(picNum):
            retItem = self.getLocalRetItem(i)
            if not hasVip:
                if retItem['mainId'] == MAIN_TAB_VIP:
                    localAdList.append(retItem)
            else:
                if retItem['mainId'] == MAIN_TAB_VIP:
                    continue
                localAdList.append(retItem)

        return localAdList

    def getLocalRetItem(self, i):
        retItem = {}
        pathGroup = self.getPathGroup(i)
        retItem['mainId'] = AppSettings.get(pathGroup['ASAP_MAINID'], 0)
        retItem['subId'] = AppSettings.get(pathGroup['ASAP_SUBID'], 0)
        retItem['type'] = AppSettings.get(pathGroup['ASAP_TYPE'], 0)
        retItem['iconPath'] = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + AppSettings.get(pathGroup['ASAP_ICONNAME'], '') + '.dds'
        retItem['mallId'] = retItem['mainId']
        retItem['buyCnt'] = retItem['subId']
        retItem['picIndex'] = i
        if not self.paramFailover(retItem):
            retItem['type'] = 3
            retItem['mainId'] = MAIN_TAB_JISHOU
        return retItem

    def paramFailover(self, item):
        ret = False
        if item['type'] in uiConst.MALL_TYPE_LIMIT:
            if item['type'] == 1:
                ret = True
            elif item['type'] == 2:
                if MID.data.get(item['mainId'], {}) and item['buyCnt'] > 0:
                    ret = True
            elif item['type'] == 3:
                if item['mainId'] in (MAIN_TAB_JISHOU, MAIN_TAB_VIP) or MCD.data.get((item['mainId'], item['subId']), ()):
                    ret = True
            elif item['type'] in (4, 5, 6):
                ret = True
        return ret


class VipPicGroup(RemotePicGroup):

    def __init__(self):
        super(VipPicGroup, self).__init__()
        self.remoteKey = uiConst.REMOTE_PIC_VIP
        self.path = ADVERTISEMENT_PATH + self.remoteKey + '/'

    def downloadADOver(self):
        self.writeList2config()
        ret = self.getLocalPicInfoList()
        gameglobal.rds.ui.tianyuMall.vipPicDownloadDone(ret)

    def writeList2config(self):
        if self.dloadedPicList:
            for i, item in enumerate(self.dloadedPicList):
                maxi = i
                pathGroup = self.getPathGroup(i)
                paramMap = eval(item.get('param', '1'))
                AppSettings[pathGroup['ASAP_TYPE']] = paramMap.get('type', 1)
                AppSettings[pathGroup['ASAP_MAINID']] = paramMap.get('mainId', 1)
                AppSettings[pathGroup['ASAP_SUBID']] = paramMap.get('subId', 1)
                AppSettings[pathGroup['ASAP_ICONNAME']] = item.get('url', '1')

            AppSettings[self.path + 'picNum'] = str(maxi)
            AppSettings[self.path + 'version'] = self.remoteVersion
            self.reset()

    def getLocalPicInfoList(self):
        localAdList = []
        picNum = AppSettings.get(self.path + 'picNum', -1) + 1
        for i in range(picNum):
            retItem = self.getLocalRetItem(i)
            localAdList.append(retItem)

        return localAdList

    def getLocalRetItem(self, i):
        retItem = {}
        pathGroup = self.getPathGroup(i)
        retItem['mainId'] = AppSettings.get(pathGroup['ASAP_MAINID'], 0)
        retItem['type'] = AppSettings.get(pathGroup['ASAP_TYPE'], 0)
        retItem['buyCnt'] = AppSettings.get(pathGroup['ASAP_SUBID'], 0)
        retItem['iconPath'] = '../' + const.IMAGES_DOWNLOAD_DIR + '/' + AppSettings.get(pathGroup['ASAP_ICONNAME'], '') + '.dds'
        return retItem

    def getBuiltInPicInfoList(self):
        ret = []
        adInfo = MCFD.data.get('adVipPage', {})
        for item in adInfo:
            item['iconPath'] = AD_ICON_TEMPLATE % str(item.get('icon', 'vip_1'))
            ret.append(item)

        return ret


class TuZhuangTabManager(Tab):

    def __init__(self):
        super(TuZhuangTabManager, self).__init__(0)
        self.selChildId = 0
        self.mse = MallSearchEngine()
        self.preOpenMainTab = 0
        self.preOpenSubTab = 0

    def initTabs(self):
        self.children = {}
        tcd = TCD.data
        for key in tcd.keys():
            mainId, subId = key
            data = tcd[key]
            if not self.children.has_key(mainId):
                self.children[mainId] = MainTab(mainId)
            self.children[mainId].appendSubTab(subId, data)
            if not self.selChildId:
                self.selChildId = mainId
                self.preOpenMainTab = mainId

        self.children[MAIN_TAB_TUZHUANG].name = gameStrings.TAB_DESC_TUZHUANG
        self.children[MAIN_TAB_HUANFU].name = gameStrings.TAB_DESC_HUANFU
        if not gameglobal.rds.configData.get('enableHuanFu', False):
            self.children.pop(MAIN_TAB_HUANFU, None)
        self.reset()

    def initInvItem(self):
        self.children[MAIN_TAB_INV] = MainTab(MAIN_TAB_INV)
        self.children[MAIN_TAB_INV].name = gameStrings.TEXT_TIANYUMALLPROXY_3397
        wingItems = []
        rideItems = []
        p = BigWorld.player()
        for pg in p.inv.getPageTuple():
            for ps in p.inv.getPosTuple(pg):
                it = p.inv.getQuickVal(pg, ps)
                if it == const.CONT_EMPTY_VAL:
                    continue
                if it.id not in TED.data.keys():
                    continue
                if it.isWingEquip():
                    wingItems.append((pg, ps, it))
                elif it.isRideEquip():
                    rideItems.append((pg, ps, it))

        if rideItems:
            self.children[MAIN_TAB_INV].appendSubInvTab(SUB_TAB_INV_RIDE, {'subTab': gameStrings.TEXT_EQUIPMIXNEWPROXY_189}, rideItems)
        if wingItems:
            self.children[MAIN_TAB_INV].appendSubInvTab(SUB_TAB_INV_WING, {'subTab': gameStrings.TEXT_TIANYUMALLPROXY_3415}, wingItems)

    def openSpetialTab(self, mainTab, subTab):
        self.preOpenMainTab = mainTab
        self.preOpenSubTab = subTab

    def prepareOpen(self):
        self.setSelectedChildId(self.preOpenMainTab)
        selMainTab = self.getSelChild()
        if selMainTab is None:
            return
        else:
            if self.preOpenSubTab:
                selMainTab.setSelectedChildId(self.preOpenSubTab)
            else:
                selMainTab.reset()
            return

    def reset(self):
        if self.children is None:
            return
        else:
            for chId in self.children:
                self.getChild(chId).reset()

            return

    def searchByKeyWord(self, keyWord, scope = SEARCH_SCOPE_ALL):
        ret = {}
        result = []
        self.mse.setKeyWord(keyWord)
        mainTabKeys = list(self.children)
        mainTabKeys.sort()
        searchTabKeys = mainTabKeys
        for key in searchTabKeys:
            mainTab = self.getChild(key)
            if mainTab.systemFixed():
                continue
            if scope == SEARCH_SCOPE_FITTING_ROOM and mainTab.fsPreviewTabNum <= 0:
                continue
            allItems = mainTab.getAllItemsInfo(scope)
            for item in allItems:
                if item['mallId'] in map(lambda item: item['mallId'], result):
                    continue
                if self.mse.match(item):
                    result.append(item)

        ret['searchTab'] = True
        ret['itemsInfo'] = result
        return ret

    def searchByMallId(self, mallId):
        ret = {}
        result = []
        found = False
        mainTabKeys = list(self.children)
        mainTabKeys.sort()
        searchTabKeys = mainTabKeys[1:]
        for key in searchTabKeys:
            allItems = self.getChild(key).getAllItemsInfo()
            for item in allItems:
                if mallId == item['mallId']:
                    result.append(item)
                    found = True
                    break

            if found:
                break

        ret['searchTab'] = True
        ret['itemsInfo'] = result
        return ret


class TianyuMallSearchHistory(SearchHistoryUtils):

    def __init__(self):
        super(TianyuMallSearchHistory, self).__init__('TianyuMall')
        self.maxCount = 20
