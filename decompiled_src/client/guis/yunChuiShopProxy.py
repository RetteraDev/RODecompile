#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/yunChuiShopProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
from Scaleform import GfxValue
import const
import utils
import gametypes
import commShop
import keys
import formula
import gamelog
from item import Item
from guis import ui
from guis import uiConst
from guis import uiUtils
from guis import compositeShopHelpFunc
from appSetting import Obj as AppSettings
from uiProxy import UIProxy
from cdata import game_msg_def_data as GMDD
from cdata import composite_shop_trade_data as CSTD
from data import item_data as ID
from data import fame_data as FD
from data import sys_config_data as SCD
from data import jingjie_data as JJD
from data import junjie_config_data as JJCD
from data import composite_shop_data as CSD
from data import juewei_data as JD
from data import school_data as SD
from data import qiren_clue_data as QCD
from data import qiren_role_data as QRD
MAOXIANJIA_FAMEID = 410
YUNCHUI_FAME_ID = 453

class YunChuiShopProxy(UIProxy):
    BUYBACK_SHOP = 99

    def __init__(self, uiAdapter):
        super(YunChuiShopProxy, self).__init__(uiAdapter)
        self.modelMap = {'changeTab': self.onChangeTab,
         'startView': self.onStartView,
         'clickItem': self.onClickItem,
         'buyItem': self.onBuyItem,
         'setDiJiaItemNum': self.onSetDiJiaItemNum,
         'getConsumeMaxNum': self.onGetConsumeMaxNum,
         'setBuyItemNum': self.onSetBuyItemNum,
         'setUseableChk': self.onSetUseableChk,
         'setConfirmSellChk': self.onSetConfirmSellChk,
         'buybackItem': self.onBuyBackItem,
         'gotoShop': self.onGotoShop,
         'closeShop': self.onCloseShop,
         'isCurrentMallTab': self.onIsCurrentMallTab}
        self.DIJIA_ITEM_TO_FAME = 0
        self.DIJIA_ITEM_TO_ITEM = 1
        self.mediator = None
        self.tabPagedRef = {}
        self.pageStampRef = {}
        self.tabItemsRef = {}
        self.itemTab = None
        self.buybackShopId = 0
        self.bindType = 'yunChuiShop'
        self.tabNameArray = []
        self.itemArray = []
        self.compositeShowType = 0
        self.buyItemPos = (-1, -1)
        self.diJiaItemToItemNum = 0
        self.consumeItemInfo = {}
        self.page = 0
        self.pos = 0
        self.isUseableChk = False
        self.isSellConfirmChk = False
        self.buyItemNum = 1
        self.diJiaItemNum = 0
        self.diJiaItemToItemNum = 0
        self.npcId = -1
        self.isPrivateShop = False
        self.initTabIdx = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_COMBINE_YUNCHUI_SHOP, self.onCloseShop)

    def itemChange(self, *args):
        self.refreshBuyItemData()

    def _registerMediator(self, widgetId, mediator):
        self.mediator = mediator
        BigWorld.player().registerEvent(const.EVENT_ITEM_CHANGE, self.itemChange)
        BigWorld.player().registerEvent(const.EVENT_ITEM_REMOVE, self.itemChange)
        self.tabIndex = 0
        itemDict = self.tabItemsRef.get(self.tabIndex, {})
        sortedItems = self.sortItemArray(itemDict.values())
        shopId = BigWorld.player().openShopId
        self.setTabItems(self.tabIndex, sortedItems)
        return GfxValue(ui.gbk2unicode(CSD.data.get(shopId, {}).get('shopName', '')))

    def clearWidget(self):
        p = BigWorld.player()
        if self.isPrivateShop:
            self.isPrivateShop = False
            if p:
                BigWorld.player().base.closePrivateShop(BigWorld.player().openShopId)
        self.mediator = None
        self.tabPagedRef = {}
        self.pageStampRef = {}
        self.tabItemsRef = {}
        self.itemTab = None
        self.tabNameArray = []
        self.buybackShopId = 0
        self.buyItemPos = (-1, -1)
        self.diJiaItemToItemNum = 0
        self.page = 0
        self.pos = 0
        self.npcId = -1
        self.initTabIdx = 0
        if p:
            BigWorld.player().openShopId = 0
            BigWorld.player().openShopType = 0
            BigWorld.player().openShopId = 0
            BigWorld.player().unRegisterEvent(const.EVENT_ITEM_CHANGE, self.itemChange)
            BigWorld.player().unRegisterEvent(const.EVENT_ITEM_REMOVE, self.itemChange)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_COMBINE_YUNCHUI_SHOP)

    def tabHide(self):
        self.setWidgetVisible(False)
        gameglobal.rds.ui.tianyuMall.setWidgetVisible(True)

    def setWidgetVisible(self, visible):
        if self.mediator:
            self.mediator.Invoke('setWidgetVisible', GfxValue(visible))

    def show(self, compositeShopId = 0):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_COMBINE_YUNCHUI_SHOP)
        if gameglobal.rds.ui.combineMall.currentTab == 0:
            return
        isShowLeftTab = CSD.data.get(compositeShopId, {}).get('showLeftTab', 1)
        gameglobal.rds.ui.combineMall.show(1, showLeftTab=isShowLeftTab)

    def getPrivateCompositeShop(self):
        if self.mediator:
            return
        p = BigWorld.player()
        p.getPrivateCompositeShop()

    def onCloseShop(self, *args):
        if gameglobal.rds.ui.combineMall.widget:
            self.checkParentShow()
        self.hide()

    def checkParentShow(self):
        gameglobal.rds.ui.combineMall.hide()
        isTianyuMallLoading = gameglobal.rds.ui.isWidgetLoading(uiConst.WIDGET_COMBINE_TIANYU_MALL)
        isTianyuMallLoaded = gameglobal.rds.ui.isWidgetLoaded(uiConst.WIDGET_COMBINE_TIANYU_MALL)
        if isTianyuMallLoaded or isTianyuMallLoading:
            gameglobal.rds.ui.tianyuMall.hide()

    def onIsCurrentMallTab(self, *arg):
        return GfxValue(gameglobal.rds.ui.combineMall.currentTab == 1)

    def onStartView(self, *args):
        self.updateSet()
        self.initTab(self.tabNameArray)
        if self.itemTab:
            self.mediator.Invoke('setTabItems', uiUtils.dict2GfxDict(self.itemTab, True))
            self.setCash()
            self.itemTab = None

    def updateSet(self):
        if not self.mediator:
            return
        setting = {}
        setting['useable'] = self.isUseableChk
        setting['confirmSet'] = gameglobal.rds.ui.compositeShop.confirmStatus
        self.mediator.Invoke('updateUserSetting', uiUtils.dict2GfxDict(setting, True))

    def initTab(self, tabNameArray):
        if self.mediator:
            self.mediator.Invoke('setTabArray', (uiUtils.array2GfxAarry(tabNameArray, True), GfxValue(self.initTabIdx)))
            self.initTabIdx = 0

    def openPrivateShop(self, compositeShopId, shopInv, customDict, pageCount):
        p = BigWorld.player()
        self.isPrivateShop = True
        self.openShop(0, compositeShopId, pageCount, customDict)
        pages = shopInv.pages
        self.isPrivateShop = True
        for i in range(len(pages)):
            info = []
            for j in range(len(pages[i])):
                it = shopInv.getQuickVal(i, j)
                if it != const.CONT_EMPTY_VAL:
                    info.append(it)

            self.setTabData(i, shopInv.stamp[i], info)

        if self.mediator:
            self.tabIndex = 0
            itemDict = self.tabItemsRef.get(self.tabIndex, {})
            sortedItems = self.sortItemArray(itemDict.values())
            self.setTabItems(self.tabIndex, sortedItems)

    def openShop(self, npcId, compositeShopId, pageCount, customDic, buyBackShopPageCount = 0, layoutType = uiConst.LAYOUT_DEFAULT):
        self.npcId = npcId
        self.customDict = customDic
        customDicKeys = sorted(customDic.keys())
        self.tabNameArray = []
        i = 0
        for key in customDicKeys:
            if len(self.customDict[key]) > 0:
                self.tabNameArray.append(key[3:])
                self.tabPagedRef[i] = customDic[key]
                i = i + 1

        self.tabNameArray.append(gameStrings.TEXT_GAMECONST_1204)
        if not self.isPrivateShop:
            ent = BigWorld.entities.get(self.npcId)
        self.hadBuybackTab = False
        BigWorld.player().openShopId = compositeShopId
        BigWorld.player().openShopType = const.SHOP_TYPE_COMPOSITE
        self.compositeShowType = CSD.data.get(compositeShopId, {}).get('compositeShopType', -1)
        self.show(compositeShopId)
        return True

    def onGetConsumeMaxNum(self, *arg):
        item = self.getItem(*self.buyItemPos)
        it = self.getShopItem(*self.buyItemPos)
        if not item:
            return GfxValue(0)
        p = BigWorld.player()
        compositeData = CSTD.data.get(item['compositeId'], {})
        consumeItem, consumeFame, _ = commShop._calcCompositeShopConsumeInfo(p, compositeData, 1, 0, 0, False)
        ret = item['count']
        if ret == const.ITEM_NUM_INFINITE:
            ret = 999
        for itemId, itemNum in consumeItem:
            curItemNum = p.inv.countItemInPages(itemId, enableParentCheck=True)
            ret = min(curItemNum / itemNum, ret)

        for fameId, fameNum in consumeFame:
            curFameNum = p.fame.get(fameId, 0)
            ret = min(curFameNum / fameNum, ret)

        if compositeData.has_key('consumeContrib'):
            consumeContrib = compositeData['consumeContrib']
            ret = min(p.guildContrib / consumeContrib, ret)
        consumeCash, consumeBindCash = self._calcConsumeCash(compositeData, 1)
        consumeCashType = compositeData.get('cashType', gametypes.CONSUME_CASH_TYPE_NO_LIMIT)
        if consumeCashType == gametypes.CONSUME_CASH_TYPE_NO_LIMIT and (consumeCash > 0 or consumeBindCash > 0):
            ret = min((p.cash + p.bindCash) / (consumeCash + consumeBindCash), ret)
        elif consumeCashType == gametypes.CONSUME_CASH_TYPE_BIND_CASH and consumeBindCash > 0:
            ret = min(p.bindCash / consumeBindCash, ret)
        elif consumeCashType == gametypes.CONSUME_CASH_TYPE_CASH and consumeCash > 0:
            ret = min(p.cash / consumeCash, ret)
        buyLimitType = CSTD.data.get(item['compositeId'], {}).get('buyLimitType', 0)
        if buyLimitType != const.COMPOSITE_BUY_LIMIT_TYPE_NO:
            maxCnt = compositeShopHelpFunc.getMaxBuyCnt(it)
            ret = min(maxCnt, ret)
        if ret == 0:
            ret = 1
        return GfxValue(ret)

    def setNormalPageItem(self, page, stamp, itemInfo = None, foreceUpdate = False):
        tabIndex, tabItems = self.setTabData(page, stamp, itemInfo)
        self.setTabItems(tabIndex, tabItems)

    def setTabData(self, page, stamp, itemInfo):
        self.pageStampRef[page] = stamp
        tabIndex = self.getTabIndex(page)
        itemDict = self.tabItemsRef.get(tabIndex, {})
        pos = 0
        if itemInfo != None:
            for item in itemInfo:
                if not item:
                    continue
                itemDict[page, pos] = (item, page, pos)
                pos += 1

            self.tabItemsRef[tabIndex] = itemDict
        sortedItmes = self.sortItemArray(itemDict.values())
        return (tabIndex, sortedItmes)

    def getShopItem(self, page, pos):
        itemDic = self.tabItemsRef.get(self.tabIndex, {})
        item = itemDic.get((page, pos), None)
        if item:
            return item[0]
        else:
            return

    def sortItemArray(self, itemArray):
        itemArray.sort(key=lambda x: (x[1], x[2]))
        return itemArray

    def getTabIndex(self, page):
        for tabIndex in self.tabPagedRef.keys():
            pages = self.tabPagedRef[tabIndex]
            if page in pages:
                return tabIndex

        return 0

    def hasItem(self, itemId):
        for item in self.itemArray:
            if item['id'] == itemId:
                return True

        return False

    def getItem(self, page, pos):
        if self.tabIndex + 1 == len(self.tabNameArray):
            return None
        else:
            for item in self.itemArray:
                if item['page'] == page and item['pos'] == pos:
                    return item

            return None

    def onGetToolTip(self, *args):
        key = args[3][0].GetString()
        itemId = int(key[16:])
        if self.tabIndex + 1 != len(self.tabNameArray):
            if self.hasItem(itemId):
                it = Item(itemId)
                ret = gameglobal.rds.ui.inventory.GfxToolTip(it)
                return ret
            else:
                return GfxValue('')
        else:
            return GfxValue('')

    def setTabItems(self, tabIndex, itemList):
        p = BigWorld.player()
        itemArray = []
        for index in xrange(len(itemList)):
            it = itemList[index][0]
            pos = itemList[index][2]
            page = itemList[index][1]
            if it:
                data = ID.data.get(it.id, {})
                if data.get('quality') == 0 and data.get('type') == Item.BASETYPE_EQUIP:
                    it = Item(it.id)
                itemInfo = uiUtils.getGfxItemById(it.id)
                itemInfo['hot'] = False
                itemInfo['name'] = uiUtils.getItemColorNameByItem(it)
                itemInfo['value'] = str(it.bPrice)
                itemInfo['page'] = page
                itemInfo['pos'] = pos
                itemInfo['limitStr'] = self._getLimitStr(it)
                itemInfo['compositeId'] = it.compositeId
                itemInfo['limitStrDesc'] = self._getLimitStrDesc(it)
                itemInfo['count'] = str(999 if it.remainNum == const.ITEM_NUM_INFINITE else it.remainNum)
                itemInfo['maxCnt'] = compositeShopHelpFunc.getMaxBuyCnt(it)
                itemInfo['useable'] = self.useable(it.id, p)
                if not self.getColorFrameFlag(it):
                    itemInfo['state'] = uiConst.EQUIP_NOT_USE
                else:
                    itemInfo['state'] = uiConst.ITEM_NORMAL
                itemInfo['priceType'] = data.get('bPriceType', gametypes.ITEM_PRICE_TYPE_BIND_CASH)
                if tabIndex + 1 == len(self.tabNameArray):
                    sFamePrice, sPrice = self.getBuyBackPrice(self.buybackShopId, it.id)
                    itemInfo['sFameprice'] = sFamePrice
                    itemInfo['sPrice'] = sPrice
                itemInfo['fameCost'] = self._getFameCost(itemInfo, p)
                itemArray.append(itemInfo)

        itemDic = {}
        itemDic['itemArray'] = itemArray
        itemDic['selectedItemPos'] = self.buyItemPos
        self.itemArray = itemArray
        if self.mediator:
            self.mediator.Invoke('setTabItems', uiUtils.dict2GfxDict(itemDic, True))
            self.setCash()
        else:
            self.itemTab = itemDic

    def getBuyBackPrice(self, buybackShopId, itemId):
        sFamePrice = 0
        sPrice = 0
        itemRecord = ID.data.get(itemId, '')
        if itemRecord == '':
            return (sFamePrice, sPrice)
        famePriceDict = itemRecord.get('buybackFamePrice') or itemRecord.get('famePrice', '')
        if famePriceDict != '':
            for key in famePriceDict.keys():
                if buybackShopId in key:
                    fameData = famePriceDict[key]
                    fameId = fameData[0]
                    sFamePrice = fameData[1]
                    if len(fameData) > 2:
                        fprices = fameData[2]
                        fameLv = BigWorld.player().getFameLv(fameId)
                        for i in xrange(0, len(fprices), 2):
                            if fameLv >= fprices[i]:
                                sFamePrice = fprices[i + 1]
                            else:
                                break

                    break

        sPrice = itemRecord['sPrice']
        return (sFamePrice, sPrice)

    def useable(self, itmeId, p):
        it = Item(itmeId)
        return it.canUseNow(p.physique.sex, p.physique.school, p.physique.bodyType, p.lv, p)

    def setCash(self):
        if not self.mediator:
            return
        cash = self.getFame()
        self.mediator.Invoke('setCash', GfxValue(cash))

    def getFame(self):
        p = BigWorld.player()
        cash = str(p.fame.get(YUNCHUI_FAME_ID, 0))
        return cash

    def _getLimitStr(self, item):
        ret = ''
        if hasattr(item, 'compositeId'):
            buyLimitType = CSTD.data.get(item.compositeId, {}).get('buyLimitType', 0)
            buyLimitCount = CSTD.data.get(item.compositeId, {}).get('buyLimitCount', -1)
            if buyLimitType != const.COMPOSITE_BUY_LIMIT_TYPE_NO:
                remainBuyCount = max(0, compositeShopHelpFunc.getCompositeRemainBuyCount(item))
                if remainBuyCount <= 0:
                    remainBuyCountStr = uiUtils.toHtml(str(remainBuyCount), '#F43804')
                else:
                    remainBuyCountStr = str(remainBuyCount)
                if buyLimitType == const.COMPOSITE_BUY_LIMIT_TYPE_DAY:
                    ret = gameStrings.TEXT_COMPOSITESHOPPROXY_530 % (remainBuyCountStr, buyLimitCount)
                elif buyLimitType == const.COMPOSITE_BUY_LIMIT_TYPE_WEEK:
                    ret = gameStrings.TEXT_COMPOSITESHOPPROXY_532 % (remainBuyCountStr, buyLimitCount)
                elif buyLimitType == const.COMPOSITE_BUY_LIMIT_TYPE_MONTH:
                    ret = gameStrings.TEXT_COMPOSITESHOPPROXY_534 % (remainBuyCountStr, buyLimitCount)
                elif buyLimitType == const.COMPOSITE_BUY_LIMIT_TYPE_FOREVER:
                    ret = gameStrings.TEXT_COMPOSITESHOPPROXY_536 % (remainBuyCountStr, buyLimitCount)
        return ret

    def _getLimitStrDesc(self, item):
        buyLimitDesc = ''
        if hasattr(item, 'compositeId'):
            buyLimitType = CSTD.data.get(item.compositeId, {}).get('buyLimitType', 0)
            buyLimitCount = CSTD.data.get(item.compositeId, {}).get('buyLimitCount', -1)
            if buyLimitType != const.COMPOSITE_BUY_LIMIT_TYPE_NO and buyLimitCount != -1:
                buyLimitDesc = gameStrings.TEXT_COMPOSITESHOPPROXY_553 % CSTD.data.get(item.compositeId, {}).get('buyLimitDesc', '')
        return buyLimitDesc

    def getColorFrameFlag(self, item):
        p = BigWorld.player()
        compositeData = CSTD.data.get(item.compositeId, {})
        schReq = ID.data.get(item.id, {}).get('schReq', ())
        if schReq and p.school not in schReq:
            return False
        if compositeData.has_key('sexLimit'):
            sexLimit = compositeData['sexLimit']
            if p.realPhysique.sex != sexLimit:
                return False
        return True

    def setBuyBackItem(self, shopId):
        p = BigWorld.player()
        compositeShopId = shopId
        if compositeShopId in p.buyBackDict:
            itemList = p.buyBackDict[compositeShopId]
        else:
            itemList = []
        itemArray = []
        pos = 0
        for it in itemList:
            if it == None:
                continue
            data = ID.data.get(it.id, {})
            itemInfo = uiUtils.getGfxItem(it, location=const.ITEM_IN_COMPOSITESHOP)
            itemInfo['name'] = uiUtils.getItemColorNameByItem(it)
            canSell, fameData = it.canSellToCompositeShopId(shopId)
            if canSell:
                itemInfo['value'] = fameData[1]
                itemInfo['priceType'] = fameData[0]
                itemInfo['tipsInfo'] = FD.data.get(fameData[0], {}).get('name', '')
                itemInfo['isEnough'] = fameData[1] <= p.fame.get(fameData[0], 0)
            else:
                itemInfo['value'] = str(it.sPrice)
                itemInfo['priceType'] = data.get('sPriceType', gametypes.ITEM_PRICE_TYPE_BIND_CASH)
            itemInfo['itemId'] = it.id
            if not it.canUseNow(p.physique.sex, p.physique.school, p.physique.bodyType, p.lv, p):
                itemInfo['state'] = uiConst.EQUIP_NOT_USE
            else:
                itemInfo['state'] = uiConst.ITEM_NORMAL
            itemInfo['pos'] = pos
            itemArray.append(itemInfo)
            pos += 1

        self.setCash()
        self.itemArray = itemArray
        if self.mediator:
            self.mediator.Invoke('setTabItems', uiUtils.array2GfxAarry(itemArray, True))

    def onChangeTab(self, *arg):
        if arg[3][0]:
            self.tabIndex = arg[3][0].GetNumber()
        else:
            return
        if self.tabIndex + 1 == len(self.tabNameArray):
            self.buyItemPos = (-1, -1)
            self.mediator.Invoke('setBuySettingWnd', GfxValue(False))
        else:
            tab = self.tabPagedRef[self.tabIndex][0]
            self.buyItemPos = (tab, 0)
            self.mediator.Invoke('setBuySettingWnd', GfxValue(True))
        self.refreshTabItems()

    def refreshTabItems(self):
        if not self.mediator:
            return
        ent = BigWorld.entities.get(self.npcId)
        if ent or self.isPrivateShop:
            if self.tabIndex + 1 == len(self.tabNameArray):
                self.setBuyBackItem(BigWorld.player().openShopId)
            elif not self.isPrivateShop:
                pages = self.tabPagedRef.get(self.tabIndex, [0])
                for page in pages:
                    stamp = self.pageStampRef.get(page, 0)
                    ent.cell.compositeShopTurnPage(BigWorld.player().openShopId, page, stamp)

            else:
                itemDict = self.tabItemsRef.get(self.tabIndex, {})
                sortedItems = self.sortItemArray(itemDict.values())
                self.setTabItems(self.tabIndex, sortedItems)

    def refresh(self):
        if not self.mediator:
            return
        self.refreshTabItems()

    def _getFameCost(self, item, p):
        compositeId = item['compositeId']
        compositeData = CSTD.data.get(compositeId, {})
        consumeItem, consumeFame, consumeDiJia = commShop._calcCompositeShopConsumeInfo(p, compositeData, 1, 0, 0, True)
        if len(consumeFame) == 0:
            return 0
        else:
            return consumeFame[0][1]

    def _getCompositeData(self):
        shopItem = None
        shopItem = self.getShopItem(*self.buyItemPos)
        if not shopItem:
            return
        else:
            compositeId = shopItem.compositeId
            compositeData = CSTD.data.get(compositeId, {})
            return compositeData

    def onClickItem(self, *args):
        page = int(args[3][0].GetNumber())
        pos = int(args[3][1].GetNumber())
        if page == -1 or pos == -1:
            self.buyItemNum = 1
            self.diJiaItemNum = 0
            self.diJiaItemToItemNum = 0
        self.buyItemPos = (page, pos)
        item = self.getItem(page, pos)
        if not item:
            return
        self.page = item['page']
        self.pos = item['pos']
        self.diJiaItemNum = 0
        self.buyItemNum = 1
        self.diJiaItemToItemNum = 0
        self.refreshBuyItemData()

    @ui.callAfterTime()
    def refreshBuyItemData(self):
        if not self.mediator:
            return
        consumeItemInfo = self.getConsumeInfo()
        self.mediator.Invoke('refreshBuySetting', uiUtils.dict2GfxDict(consumeItemInfo, True))

    def getConsumeInfo(self):
        compositeData = self._getCompositeData()
        if not compositeData:
            return
        p = BigWorld.player()
        itemNum = self.buyItemNum if self.buyItemNum > 0 else 1
        consumeItem, consumeFame, consumeDiJia = commShop._calcCompositeShopConsumeInfo(p, compositeData, itemNum, self.diJiaItemNum, self.diJiaItemToItemNum, True)
        consumeItemInfo = {}
        conditionList = []
        isValid, limitedInfo = self.getLimitedInfo(compositeData, p)
        conditionList.extend(limitedInfo)
        isValid, costItemInfo, costItemList = self.getCostItemInfo(consumeItem, compositeData, isValid, p)
        conditionList.extend(costItemInfo)
        diJiaInfo, isValid = self.getDiJiaInfo(compositeData, consumeDiJia, costItemList, p, isValid)
        consumeItemInfo['consumeDiJiaInfo'] = diJiaInfo
        fameInfo, isValid = self.getFameInfo(consumeFame, p, conditionList, isValid)
        consumeItemInfo['fameInfo'] = fameInfo
        guildInfo, juqingInfo, consumeCash, consumeBindCash, isValid = self.getOtherInfo(compositeData, p, isValid)
        conditionList.extend(guildInfo)
        conditionList.extend(juqingInfo)
        consumeItemInfo['conditionList'] = conditionList
        consumeItemInfo['consumeCash'] = consumeCash
        consumeItemInfo['consumeBindCash'] = consumeBindCash
        consumeItemInfo['playerCash'] = p.cash
        consumeItemInfo['playerBindCash'] = p.bindCash
        consumeItemInfo['isValid'] = isValid
        consumeItemInfo['count'] = self.buyItemNum
        consumeItemInfo['fameCash'] = self.getFame()
        consumeItemInfo['tips'] = SCD.data.get('compositeShopMaxBtnTips', 'compositeShopMaxBtnTips not found')
        consumeItemInfo['coin'] = p.unbindCoin + p.bindCoin + p.freeCoin
        self.consumeItemInfo = consumeItemInfo
        return consumeItemInfo

    def getLimitedInfo(self, compositeData, p):
        consumeItemInfo = []
        isValid = True
        if compositeData.has_key('lvLimit'):
            lvLimit = compositeData['lvLimit']
            if lvLimit[0] == -1:
                itemName = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_289 % lvLimit[1]
                if p.realLv <= lvLimit[1]:
                    consumeItemInfo.append([itemName, True])
                else:
                    consumeItemInfo.append([itemName, False])
                    isValid = False
            elif lvLimit[1] == -1:
                itemName = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_293 % lvLimit[0]
                if p.realLv >= lvLimit[0]:
                    consumeItemInfo.append([itemName, True])
                else:
                    consumeItemInfo.append([itemName, False])
                    isValid = False
            else:
                itemName = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_297 % (lvLimit[0], lvLimit[1])
                if p.realLv >= lvLimit[0] and p.realLv <= lvLimit[1]:
                    consumeItemInfo.append([itemName, True])
                else:
                    consumeItemInfo.append([itemName, False])
                    isValid = False
        if compositeData.has_key('sexLimit'):
            sexLimit = compositeData['sexLimit']
            itemName = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_303 % (const.SEX_NAME[sexLimit],)
            if p.realPhysique.sex == sexLimit:
                consumeItemInfo.append([itemName, True])
            else:
                consumeItemInfo.append([itemName, False])
                isValid = False
        if compositeData.has_key('arenaScoreLimit'):
            arenaScoreLimit = compositeData['arenaScoreLimit']
            itemName = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_310 % (arenaScoreLimit,)
            if p.arenaInfo.arenaScore >= arenaScoreLimit:
                consumeItemInfo.append([itemName, True])
            else:
                consumeItemInfo.append([itemName, False])
                isValid = False
        if compositeData.has_key('qumoLimit'):
            qumoLimit = compositeData['qumoLimit']
            itemName = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_317 % (qumoLimit,)
            if p.qumoLv >= qumoLimit:
                consumeItemInfo.append([itemName, True])
            else:
                consumeItemInfo.append([itemName, False])
                isValid = False
        if compositeData.has_key('shopJingJieRequire'):
            jingJieLimit = compositeData['shopJingJieRequire']
            jingJieName = JJD.data.get(jingJieLimit, {}).get('name', gameStrings.TEXT_COMPOSITESHOPHELPFUNC_324)
            itemName = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_325 % (jingJieName,)
            if p.jingJie >= jingJieLimit:
                consumeItemInfo.append([itemName, True])
            else:
                consumeItemInfo.append([itemName, False])
                isValid = False
        if compositeData.has_key('needJunJieLv'):
            junJieLvLimit = compositeData['needJunJieLv']
            junJieName = JJCD.data.get(junJieLvLimit, {}).get('name', gameStrings.TEXT_COMPOSITESHOPHELPFUNC_324)
            itemName = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_333 % (junJieName,)
            if p.junJieLv >= junJieLvLimit:
                consumeItemInfo.append([itemName, True])
            else:
                consumeItemInfo.append([itemName, False])
                isValid = False
        if compositeData.has_key('needJueWeiLv'):
            jueWeiLvLimit = compositeData['needJueWeiLv']
            jueWeiName = JD.data.get(jueWeiLvLimit, {}).get('name', gameStrings.TEXT_COMPOSITESHOPHELPFUNC_324)
            itemName = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_341 % (jueWeiName,)
            if p.jueWeiLv >= jueWeiLvLimit:
                consumeItemInfo.append([itemName, True])
            else:
                consumeItemInfo.append([itemName, False])
                isValid = False
        if compositeData.has_key('schoolLimit'):
            schLimit = compositeData['schoolLimit']
            schoolNames = ''
            for school in schLimit:
                schoolNames += SD.data.get(school, {}).get('name', gameStrings.TEXT_GAME_1747) + ' '

            itemName = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_351 % schoolNames
            if p.realSchool in schLimit:
                consumeItemInfo.append([itemName, True])
            else:
                consumeItemInfo.append([itemName, False])
                isValid = False
        if compositeData.has_key('appearanceItemPointLimit'):
            appearanceItemPointLimit = compositeData['appearanceItemPointLimit']
            itemName = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_358 % (appearanceItemPointLimit,)
            if p.appearanceItemCollectPoint >= appearanceItemPointLimit:
                consumeItemInfo.append([itemName, True])
            else:
                consumeItemInfo.append([itemName, False])
                isValid = False
        if compositeData.has_key('delegationRank'):
            maoxianFameLv = compositeData['delegationRank']
            maoxianFameName = FD.data.get(MAOXIANJIA_FAMEID, {}).get('lvDesc')[maoxianFameLv]
            itemName = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_366 % (maoxianFameName,)
            if p.delegationRank >= maoxianFameLv:
                consumeItemInfo.append([itemName, True])
            else:
                consumeItemInfo.append([itemName, False])
                isValid = False
        elif compositeData.has_key('fameLimit'):
            fameLimit = compositeData['fameLimit']
            for fameId, fameNum in fameLimit:
                fd = FD.data.get(fameId, {})
                if not fd or fd.has_key('lvDesc'):
                    continue
                fameLv, extraFame = self._getFameLv(fameId, fameNum)
                fameName = fd.get('shopTips', '')
                fameLvName = SCD.data.get('fameLvName', {}).get(fameLv, '')
                if fameLvName == '':
                    continue
                if extraFame <= 0:
                    itemName = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_443 % (fameName, fameLvName)
                else:
                    extraFame = str(extraFame)
                    itemName = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_446 % (fameName, fameLvName, extraFame)
                if p.getFame(fameId) >= fameNum:
                    consumeItemInfo.append([itemName, True])
                else:
                    consumeItemInfo.append([itemName, False])
                    isValid = False

        return (isValid, consumeItemInfo)

    def _getFameLv(self, fameId, fameVal):
        fd = FD.data.get(fameId)
        ret = 1
        if fd.has_key('lvUpCondition'):
            lvUpCondition = fd.get('lvUpCondition', [])
            if lvUpCondition:
                lvArray = lvUpCondition[1].items()
            else:
                lvArray = []
        else:
            lvArray = fd.get('lvUpNeed', {}).items()
        lvArray.sort(key=lambda k: k[1], reverse=True)
        for key, val in lvArray:
            if fameVal >= val:
                ret = key + 1
                break

        return (ret, fameVal - val)

    def onSetDiJiaItemNum(self, *args):
        num = int(args[3][0].GetNumber())
        diJiaType = self._getDijiaType()
        if diJiaType == self.DIJIA_ITEM_TO_FAME:
            if self.diJiaItemNum == num:
                return
            self.diJiaItemNum = int(args[3][0].GetNumber())
            self.diJiaItemToItemNum = 0
        elif diJiaType == self.DIJIA_ITEM_TO_ITEM:
            if num == self.diJiaItemToItemNum:
                return
            self.diJiaItemNum = 0
            self.diJiaItemToItemNum = int(args[3][0].GetNumber())
        self.refreshBuyItemData()

    def _getDijiaType(self):
        compositeData = self._getCompositeData()
        if not compositeData:
            return self.DIJIA_ITEM_TO_ITEM
        diJiaItemid = compositeData.get('diJiaItemid', 0)
        diJiaSrcItemid = compositeData.get('diJiaSrcItemId', 0)
        if diJiaItemid > 0:
            return self.DIJIA_ITEM_TO_FAME
        if diJiaSrcItemid > 0:
            return self.DIJIA_ITEM_TO_ITEM
        return self.DIJIA_ITEM_TO_FAME

    def getCostItemInfo(self, consumeItem, compositeData, isValid, p):
        costItemInfo = []
        diJiaType = self._getDijiaType()
        tgtDiJiaItemId = compositeData.get('diJiaTargetItemId', 0)
        costItemList = {}
        for itemId, itemNum in consumeItem:
            if not itemId:
                continue
            itemName = ID.data.get(itemId, {}).get('name', '')
            if itemId in costItemList:
                curItemNum = costItemList[itemId]
            else:
                curItemNum = p.inv.countItemInPages(itemId, enableParentCheck=True)
                if curItemNum - itemNum < 0:
                    costItemList[itemId] = 0
                else:
                    costItemList[itemId] = curItemNum - itemNum
            if curItemNum >= itemNum:
                costItemInfo.append([itemName,
                 True,
                 str(curItemNum) + '/' + str(itemNum),
                 itemId])
            else:
                costItemInfo.append([itemName,
                 False,
                 str(curItemNum) + '/' + str(itemNum),
                 itemId])
                isValid = False
            if diJiaType == self.DIJIA_ITEM_TO_ITEM and itemId == tgtDiJiaItemId:
                costItemInfo.append(['addDijia', True])

        return (isValid, costItemInfo, costItemList)

    def _getDijiaItemId(self):
        compositeData = self._getCompositeData()
        if not compositeData:
            return 0
        diJiaType = self._getDijiaType()
        if diJiaType == self.DIJIA_ITEM_TO_FAME:
            return compositeData.get('diJiaItemid', 0)
        if diJiaType == self.DIJIA_ITEM_TO_ITEM:
            return compositeData.get('diJiaSrcItemId', 0)

    def getDiJiaInfo(self, compositeData, consumeDiJia, costItemList, p, isValid):
        diJiaItemId = self._getDijiaItemId()
        diJiaType = self._getDijiaType()
        tgtDiJiaItemId = compositeData.get('diJiaTargetItemId', 0)
        if diJiaType == self.DIJIA_ITEM_TO_FAME:
            diJiaItemMaxNum = compositeData.get('diJiaItemMaxNum', 0)
            self.diJiaFame = compositeData.get('diJiaFame', [])
        elif diJiaType == self.DIJIA_ITEM_TO_ITEM:
            diJiaItemMaxNum = compositeData.get('diJiaSrcMaxNum', 0)
            self.diJiaFame = []
        else:
            diJiaItemMaxNum = 0
            self.diJiaFame = []
        consumeDiJiaInfo = {}
        if diJiaItemMaxNum:
            diJiaItemNum = consumeDiJia[1] if consumeDiJia else 0
            diJiaItemName = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_660 % ID.data.get(diJiaItemId, {}).get('name', '')
            if diJiaItemId in costItemList:
                curItemNum = costItemList[diJiaItemId]
            else:
                curItemNum = p.inv.countItemInPages(diJiaItemId, enableParentCheck=True)
                if curItemNum - diJiaItemNum < 0:
                    costItemList[diJiaItemId] = 0
                else:
                    costItemList[diJiaItemId] = curItemNum - diJiaItemNum
            if curItemNum >= diJiaItemNum:
                diJiaDesc1 = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_670 % diJiaItemName
                diJiaNumStr = '%d/%d' % (curItemNum, diJiaItemNum)
            else:
                diJiaDesc1 = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_670 % uiUtils.toHtml(diJiaItemName, '#D9482B')
                diJiaNumStr = uiUtils.toHtml('%d/%d' % (curItemNum, diJiaItemNum), '#D9482B')
                isValid = isValid and False
            if diJiaType == self.DIJIA_ITEM_TO_FAME and self.diJiaFame:
                diJiaDesc2 = ''
                for fameId, fameNum in self.diJiaFame:
                    if diJiaDesc2 != '':
                        diJiaDesc2 += '<br>'
                    diJiaDesc2 += gameStrings.TEXT_COMPOSITESHOPHELPFUNC_682 % (1, FD.data.get(fameId, {}).get('name', ''), fameNum)

            elif diJiaType == self.DIJIA_ITEM_TO_ITEM:
                diJiaDesc2 = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_682 % (compositeData.get('diJiaSrcItemNum', 0), ID.data.get(tgtDiJiaItemId, {}).get('name', ''), compositeData.get('diJiaTargetItemNum', 0))
            else:
                diJiaDesc2 = ''
            consumeDiJiaInfo['curNum'] = curItemNum
            consumeDiJiaInfo['itemNum'] = diJiaItemNum
            consumeDiJiaInfo['numLimit'] = diJiaItemMaxNum * self.buyItemNum
            consumeDiJiaInfo['visible'] = True
            consumeDiJiaInfo['diJiaItemId1'] = diJiaItemId
            consumeDiJiaInfo['diJiaItemId2'] = tgtDiJiaItemId
            consumeDiJiaInfo['diJiaDesc1'] = diJiaDesc1
            consumeDiJiaInfo['diJiaDesc2'] = diJiaDesc2
            consumeDiJiaInfo['diJiaNumStr'] = diJiaNumStr
            consumeDiJiaInfo['check'] = curItemNum >= diJiaItemNum
            consumeDiJiaInfo['itemName'] = ID.data.get(diJiaItemId, {}).get('name', '')
        else:
            consumeDiJiaInfo['visible'] = False
        return (consumeDiJiaInfo, isValid)

    def getFameInfo(self, consumeFame, p, conditionLsit, isValid):
        diJiaType = self._getDijiaType()
        fameInfo = []
        for fameId, fameNum in consumeFame:
            fameName = FD.data.get(fameId, {}).get('name', '')
            curFameNum = p.fame.get(fameId, 0)
            curCoin = p.unbindCoin + p.bindCoin + p.freeCoin
            if curFameNum >= fameNum or curFameNum + curCoin // 10 * 400 >= fameNum and curCoin >= 10:
                fameInfo.append([fameName, False, format(fameNum, ',')])
            elif curFameNum >= fameNum:
                fameInfo.append([fameName, True, format(fameNum, ',')])
            else:
                fameInfo.append([fameName, False, format(fameNum, ',')])
                isValid = False
            if diJiaType == self.DIJIA_ITEM_TO_FAME and self.diJiaFame and self.diJiaFame[0][0] == fameId:
                conditionLsit.append(['addDijia', True, ''])

        return (fameInfo, isValid)

    def _calcConsumeCash(self, compositeData, buyNum = 0):
        cash = 0
        bindCash = 0
        consumeCash = compositeData.get('consumeCash', 0)
        if consumeCash == 0:
            return (cash, bindCash)
        consumeCashType = compositeData.get('cashType', gametypes.CONSUME_CASH_TYPE_NO_LIMIT)
        if buyNum == 0:
            consumeCash *= self.buyItemNum
        else:
            consumeCash *= buyNum
        p = BigWorld.player()
        if consumeCashType == gametypes.CONSUME_CASH_TYPE_NO_LIMIT:
            bindCash = min(consumeCash, p.bindCash)
            cash = max(consumeCash - bindCash, 0)
        elif consumeCashType == gametypes.CONSUME_CASH_TYPE_BIND_CASH:
            bindCash = consumeCash
        elif consumeCashType == gametypes.CONSUME_CASH_TYPE_CASH:
            cash = consumeCash
        return (cash, bindCash)

    def getOtherInfo(self, compositeData, p, isValid):
        guildInfo = []
        juqingInfo = []
        if compositeData.has_key('consumeContrib'):
            fameName = gameStrings.TEXT_CONST_8340
            consumeContrib = compositeData['consumeContrib'] * self.buyItemNum
            if p.guildContrib >= consumeContrib:
                guildInfo.append([fameName, True, format(p.guildContrib, ',') + '/' + format(consumeContrib, ',')])
            else:
                guildInfo.append([fameName, False, format(p.guildContrib, ',') + '/' + format(consumeContrib, ',')])
                isValid = False
        if compositeData.has_key('needClue'):
            needClue = compositeData['needClue']
            desc = compositeData.get('clueDesc', '')
            finished = all([ p.getClueFlag(cid) for cid in needClue ])
            if not desc:
                roleId = QCD.data.get(needClue[0], {}).get('pushRoleId')
                role = QRD.data.get(roleId, {}).get('name', '')
                desc = gameStrings.TEXT_COMPOSITESHOPHELPFUNC_108 % role
            if finished:
                juqingInfo.append([desc, True, ''])
            else:
                juqingInfo.append([desc, False, ''])
                isValid = False
        consumeCash, consumeBindCash = self._calcConsumeCash(compositeData)
        consumeCashType = compositeData.get('cashType', gametypes.CONSUME_CASH_TYPE_NO_LIMIT)
        if consumeCashType == gametypes.CONSUME_CASH_TYPE_NO_LIMIT:
            if p.cash + p.bindCash < consumeCash + consumeBindCash:
                isValid = False
        elif consumeCashType == gametypes.CONSUME_CASH_TYPE_BIND_CASH:
            if p.bindCash < consumeBindCash:
                isValid = False
        elif consumeCashType == gametypes.CONSUME_CASH_TYPE_CASH:
            if p.cash < consumeCash:
                isValid = False
        return (guildInfo,
         juqingInfo,
         consumeCash,
         consumeBindCash,
         isValid)

    def onSetBuyItemNum(self, *arg):
        self.buyItemNum = int(arg[3][0].GetNumber())
        self.refreshBuyItemData()

    def onBuyItem(self, *args):
        if len(args[3]) > 0:
            self.buyItemPos = int(args[3][0].GetNumber(), int(args[3][1].GetNumber()))
            self.buyItemNum = 1
        p = BigWorld.player()
        if not self.getItem(*self.buyItemPos):
            p.showGameMsg(GMDD.data.COMPOSITE_SHOP_BUY_FORBIDDEN_CHOOSE_ITEM, ())
            return
        else:
            itemNum = self.buyItemNum
            cashItem = self.getItem(*self.buyItemPos)
            itemId = cashItem['id']
            self.page = cashItem.get('page', 0)
            self.pos = cashItem.get('pos', 0)
            maxCnt = cashItem.get('maxCnt', 999)
            judge = (1, maxCnt, GMDD.data.ITEM_TRADE_NUM)
            if not ui.inputRangeJudge(judge, itemNum, (maxCnt,)):
                return
            npcEnt = BigWorld.entity(self.npcId)
            if not npcEnt and not self.isPrivateShop:
                return
            if itemNum > Item.maxWrap(itemId):
                p.showGameMsg(GMDD.data.SHOP_BUY_ITEM_OVER_MWRAP, ())
                return
            buyIt = Item(itemId, cwrap=itemNum, genRandProp=False)
            if ID.data.get(buyIt.id, {}).get('needOwner'):
                buyIt.setOwner(p.gbId, p.realRoleName)
            if Item.isDotaBattleFieldItem(itemId):
                invPage, invPos = p.battleFieldBag.searchBestInPages(itemId, itemNum, buyIt)
            elif Item.isQuestItem(itemId):
                invPage, invPos = p.questBag.searchBestInPages(itemId, itemNum, buyIt)
            elif p._isInCross():
                if gameglobal.rds.configData.get('enableWingWorld', False):
                    invPage, invPos = p.crossInv.searchBestInPages(itemId, itemNum, buyIt)
            else:
                invPage, invPos = p.inv.searchBestInPages(itemId, itemNum, buyIt)
            if invPage == const.CONT_NO_PAGE or invPos == const.CONT_NO_POS:
                p.showGameMsg(GMDD.data.SHOP_BAG_FULL, ())
                return
            shopItem = self.getShopItem(*self.buyItemPos)
            if shopItem is None:
                return False
            compositeId = shopItem.compositeId
            if not CSTD.data.has_key(compositeId):
                return False
            compositeData = CSTD.data.get(compositeId, {})
            if not commShop._checkCompositeShopPreLimit(p, compositeData, self.buyItemNum):
                p.showGameMsg(GMDD.data.COMPOSITE_SHOP_BUY_FORBIDDEN_PRE_LIMIT, ())
                return
            if not self._checkdiJiaItem(compositeData):
                return
            if not self._getCompositeData().get('diJiaItemid'):
                self.diJiaItemNum = 0
            if not self._getCompositeData().get('diJiaSrcItemId'):
                self.diJiaItemToItemNum = 0
            if not commShop._checkBuyItemConsume(p, compositeData, self.buyItemNum, self.diJiaItemNum, self.diJiaItemToItemNum):
                p.showGameMsg(GMDD.data.COMPOSITE_SHOP_BUY_FORBIDDEN_MATERIAL_SHORTAGE, ())
                return
            if compositeData.has_key('lvLimit'):
                lvLimit = compositeData['lvLimit']
                if lvLimit[0] == -1:
                    if p.lv > lvLimit[1]:
                        return
                elif lvLimit[1] == -1:
                    if p.lv < lvLimit[0]:
                        return
                elif p.lv < lvLimit[0] or p.lv > lvLimit[1]:
                    return
            diJiaItemId = self._getDijiaItemId()
            if self.diJiaItemNum != 0 or self.diJiaItemToItemNum != 0:
                diJiaItemPage, diJiaItemPos = BigWorld.player().inv.findItemInPages(diJiaItemId, enableParentCheck=True, includeExpired=True, includeLatch=True, includeShihun=True)
                if diJiaItemPage == const.CONT_NO_PAGE or diJiaItemPos == const.CONT_NO_POS:
                    return
            else:
                diJiaItemPage, diJiaItemPos = (0, 0)
            if self.isPrivateShop:
                p.base.buyPrivateShopItem(BigWorld.player().openShopId, self.page, self.pos, itemNum, invPage, invPos, diJiaItemPage, diJiaItemPos, self.diJiaItemNum, self.diJiaItemToItemNum)
            else:
                npcEnt.cell.compositeShopSell(BigWorld.player().openShopId, self.page, self.pos, itemNum, invPage, invPos, diJiaItemPage, diJiaItemPos, self.diJiaItemNum, self.diJiaItemToItemNum)
                stamp = self.pageStampRef.get(self.page, 0)
                npcEnt.cell.compositeShopTurnPage(BigWorld.player().openShopId, self.page, stamp)
            gameglobal.rds.sound.playSound(gameglobal.SD_26)
            return

    def refreshSingleItem(self, page, pos, item):
        if not self.mediator:
            return
        itemDict = self.tabItemsRef.get(self.tabIndex, {})
        itemDict[page, pos] = (item, page, pos)
        self.refreshTabItems()

    def _checkdiJiaItem(self, compositeData):
        diJiaType = self._getDijiaType()
        if diJiaType == self.DIJIA_ITEM_TO_FAME and self.diJiaItemNum == 0:
            return True
        if diJiaType == self.DIJIA_ITEM_TO_ITEM and self.diJiaItemToItemNum == 0:
            return True
        p = BigWorld.player()
        diJiaItemId = self._getDijiaItemId()
        if diJiaItemId == 0:
            return True
        curCnt = p.inv.countItemInPages(diJiaItemId, enableParentCheck=True)
        if self.diJiaItemNum > curCnt:
            p.showGameMsg(GMDD.data.COMPOSITE_SHOP_BUY_FORBIDDEN_DIJIA_ITEM_NUM, ())
            return False
        return True

    def onSetUseableChk(self, *args):
        self.isUseableChk = args[3][0].GetBool()

    def onSetConfirmSellChk(self, *args):
        gameglobal.rds.ui.compositeShop.confirmStatus = args[3][0].GetBool()
        AppSettings[keys.SET_COMPOSITE_SHOP_CONFIRM] = gameglobal.rds.ui.compositeShop.confirmStatus
        AppSettings.save()
        gameglobal.rds.ui.compositeShopConfirm.updateCheckBox()

    def onBuyBackItem(self, *args):
        pos = int(args[3][0].GetNumber())
        ent = BigWorld.entity(self.npcId)
        if not ent and not self.isPrivateShop:
            return
        if self.isPrivateShop:
            BigWorld.player().base.compositeShopRetrieve(BigWorld.player().openShopId, pos)
        else:
            ent.cell.compositeShopRetrieve(BigWorld.player().openShopId, pos)

    def updateBuybackItem(self):
        if not self.mediator:
            return
        if self.tabIndex + 1 != len(self.tabNameArray):
            return
        self.setBuyBackItem(BigWorld.player().openShopId)

    def onGotoShop(self, *args):
        if gameglobal.rds.configData.get('enableBuyYunChuiCreditThroughCoin', False):
            if args[3]:
                maxCoin = int(args[3][0].GetNumber())
                self.uiAdapter.tianBiToYunChui.buyNum = maxCoin
            self.uiAdapter.tianBiToYunChui.show()
        else:
            searchKey = SCD.data.get('yunChuiShop2TiYuMall', '')
            self.setWidgetVisible(False)
            if gameglobal.rds.ui.tianyuMall.mallMediator:
                gameglobal.rds.ui.tianyuMall.refreshSearchItem(searchKey)
                gameglobal.rds.ui.tianyuMall.setWidgetVisible(True)
            gameglobal.rds.ui.combineMall.currentTab = 0
            gameglobal.rds.ui.combineMall.setSelectedBtn(0)
            gameglobal.rds.ui.tianyuMall.show(keyWord=searchKey)

    def needOpen(self, compositeShopId):
        shopType = CSD.data.get(compositeShopId, {}).get('newShopType', 0)
        if gameglobal.rds.configData.get('enableYunChuiShop', False) and shopType == const.COMPOSTIE_SHOP_SHOW_TYE_YUNCHUI:
            return True
        else:
            return False

    def onBuyYunChuiScore(self, *args):
        self.uiAdapter.tianBiToYunChui.show()
