#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/selfAdaptionShopProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gametypes
import const
import uiConst
import events
from gamestrings import gameStrings
from guis.asObject import ASObject
from uiProxy import UIProxy
from guis import uiUtils
from guis import ui
from guis.asObject import ASUtils
from guis.asObject import TipManager
from data import school_data as SD
from data import item_catagory_data as ICD
from data import item_data as ID
from data import fame_data as FD
from cdata import dynamic_shop_item_data as DSID
from cdata import game_msg_def_data as GMDD
PAGE_ITEM_CNT = 30
LIMIT_TYPE_DYA = 1
LIMIT_TYPE_WEEK = 2
TEXT_COLOR_RED = '#d34024'
TEXT_COLOR_NORMAL = '#d9CFB6'
BUY_LIMIT_DES = {0: '',
 gametypes.DYNAMIC_SHOP_SELL_LIMIT_TYPE_DAY: gameStrings.TEXT_SELFADAPTIONSHOPPROXY_35,
 gametypes.DYNAMIC_SHOP_SELL_LIMIT_TYPE_WEEK: gameStrings.TEXT_IMPITEM_2350,
 gametypes.DYNAMIC_SHOP_SELL_LIMIT_TYPE_MONTH: gameStrings.TEXT_CHALLENGEPROXY_282,
 gametypes.DYNAMIC_SHOP_SELL_LIMIT_TYPE_FOREVER: gameStrings.TEXT_SELFADAPTIONSHOPPROXY_38}

class SelfAdaptionShopProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SelfAdaptionShopProxy, self).__init__(uiAdapter)
        self.widget = None
        self.shopId = 0
        self.shopInfo = None
        self.category2BuyItemListDic = {}
        self.category2SellItemListDic = {}
        self.tabIdx = uiConst.SELF_ADAPTION_SHOP_TAB_TYPE_BUY
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_SELF_ADAPTION_SHOP, self.hide)

    def reset(self):
        self.searchContent = ''
        self.itemCategoryList = []
        self.searchHistory = []
        self.itemsContent = {}
        self.isNeedSortRevert = False
        self.searchKey = None
        self.searchName = None
        self.selectSetId = 0
        self.selectRenderMC = None
        self.selectedTreeMc = None
        self.itemNameList = []
        self.set2ValDic = {}
        self.selectKey = None

    def openShop(self, shopId = 10001):
        BigWorld.player().cell.queryDynamicShopInfo(shopId)

    def setShopInfo(self, shopId, shopInfo):
        self.shopId = shopId
        self.shopInfo = shopInfo
        self.category2BuyItemListDic = {}
        self.category2SellItemListDic = {}
        if not shopInfo:
            return
        for setId, dynamicShopItemVal in shopInfo.iteritems():
            self.set2ValDic[setId] = dynamicShopItemVal
            shopType = DSID.data.get(setId, {}).get('dynamicShopType', 0)
            if shopType in (gametypes.DYNAMIC_SHOP_TYPE_BUY_ONLY, gametypes.DYNAMIC_SHOP_TYPE_BUY_AND_SELL):
                itemId = DSID.data.get(setId, {}).get('itemId', 0)
                category = ID.data.get(itemId, {}).get('category', 0)
                subCategory = ID.data.get(itemId, {}).get('subcategory', 0)
                self.category2BuyItemListDic.setdefault((category, subCategory), []).append(dynamicShopItemVal)
            if shopType in (gametypes.DYNAMIC_SHOP_TYPE_SELL_ONLY, gametypes.DYNAMIC_SHOP_TYPE_BUY_AND_SELL):
                itemId = DSID.data.get(setId, {}).get('itemList', [0, 0])[0]
                category = ID.data.get(itemId, {}).get('category', 0)
                subCategory = ID.data.get(itemId, {}).get('subcategory', 0)
                self.category2SellItemListDic.setdefault((category, subCategory), []).append(dynamicShopItemVal)

        if not self.widget:
            self.show()
        else:
            self.refreshInfo()

    def updateShopInfo(self, shopId, shopInfo):
        if self.shopId != shopId:
            return
        if not shopInfo:
            return
        for setId, dynamicShopItemVal in shopInfo.iteritems():
            self.set2ValDic[setId] = dynamicShopItemVal

        self.refreshInfoWithoutSetDataArray()

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_SELF_ADAPTION_SHOP:
            self.addEvent(events.EVENT_TIANBI_COIN_CHANGED, self.refreshCashInfo)
            self.addEvent(events.EVENT_CASH_CHANGED, self.refreshCashInfo)
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.setShopInfo(0, None)
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_SELF_ADAPTION_SHOP)
        self.uiAdapter.selfAdaptionShopBuyOrSell.hide()

    def show(self, tabIdx = uiConst.SELF_ADAPTION_SHOP_TAB_TYPE_BUY):
        self.tabIdx = tabIdx
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_SELF_ADAPTION_SHOP)
        else:
            self.refreshInfo()

    def initUI(self):
        if not self.category2BuyItemListDic and self.tabIdx == uiConst.SELF_ADAPTION_SHOP_TAB_TYPE_BUY:
            self.tabIdx = uiConst.SELF_ADAPTION_SHOP_TAB_TYPE_SELL
        elif not self.category2SellItemListDic and self.tabIdx == uiConst.SELF_ADAPTION_SHOP_TAB_TYPE_SELL:
            self.tabIdx = uiConst.SELF_ADAPTION_SHOP_TAB_TYPE_BUY
        self.widget.mainMC.sortTxt.addEventListener(events.BUTTON_CLICK, self.handleSortClick, False, 0, True)
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.mainMC.typeTreeList.tree.lvItemGap = 6
        self.widget.mainMC.typeTreeList.tree.itemHeights = [28, 28]
        self.widget.mainMC.typeTreeList.tree.itemRenderers = ('SelfAdaptionShop_ScrollItem_Lv1', 'SelfAdaptionShop_TreeItem1')
        self.widget.mainMC.typeTreeList.tree.labelFunction = self.treeLabelFun
        self.widget.mainMC.typeTreeList.tree.addEventListener(events.EVENT_SELECTED_DATA_CHANGED, self.handleTreeItemChange, False, 0, True)
        self.widget.mainMC.typeTreeList.tree.addEventListener(events.EVENT_ITEM_EXPAND_CHANGED, self.handleTreeItemGroupChange, False, 0, True)
        self.widget.mainMC.typeTreeList.tree.childItemEffect = False
        self.widget.mainMC.txtInput.labelFunction = self.addHistoryMark
        self.widget.mainMC.txtInput.selectItemFunction = self.selectItem
        self.widget.mainMC.txtInput.labelField = None
        self.widget.mainMC.txtInput.defaultText = gameStrings.SELF_ADAPTION_SHOP_SEARCH_DEFAULT
        self.widget.mainMC.txtInput.addEventListener(events.INDEX_CHANGE, self.handleIndexChange, False, 0, True)
        self.widget.mainMC.txtInput.addEventListener(events.KEYBOARD_EVENT_KEY_UP, self.handleInputKeyUp, 0, uiConst.AS_INT_MIN_VALUE)
        TipManager.addTip(self.widget.mainMC.searchBtn, gameStrings.SELF_ADAPTION_SHOP_SEARCH_TIPS)
        self.widget.mainMC.searchBtn.addEventListener(events.BUTTON_CLICK, self.handleClickSearch, False, 0, True)
        self.widget.mainMC.itemScrollWndList.itemRenderer = 'SelfAdaptionShop_Item'
        self.widget.mainMC.itemScrollWndList.labelFunction = self.scrollWndLabelFunction
        self.widget.tabBuyBtn.visible = len(self.category2BuyItemListDic) > 0
        self.widget.tabSellBtn.visible = len(self.category2SellItemListDic) > 0
        self.widget.mainMC.cashBonusIcon.bonusType = 'cash'
        self.widget.mainMC.coinBonusIcon.bonusType = 'tianBi'

    def handleTreeItemGroupChange(self, *args):
        self.widget.mainMC.typeTreeList.refreshHeight(self.widget.mainMC.typeTreeList.tree.height)

    def handleTreeItemChange(self, *args):
        e = ASObject(args[3][0])
        if e.data.selectData:
            if self.selectedTreeMc:
                self.selectedTreeMc.selected = False
                self.selectedTreeMc = None
            self.searchKey = e.data.selectData.key
            self.selectKey = tuple(e.data.selectData.key)
            self.searchName = None
            self.refreshItemsContent()

    def handleSortClick(self, *args):
        self.isNeedSortRevert = not self.isNeedSortRevert
        self.refreshItemsContent()

    def treeLabelFun(self, *args):
        item = ASObject(args[3][0])
        itemData = ASObject(args[3][1])
        isFirst = args[3][2].GetBool()
        if isFirst:
            item.textField.text = itemData.label
        else:
            item.label = itemData.label
            if tuple(itemData.key) == self.selectKey:
                if self.selectedTreeMc:
                    self.selectedTreeMc.selected = False
                item.selected = True
                self.selectedTreeMc = item

    def addHistoryMark(self, *args):
        itemName = ASObject(args[3][0]).label
        return GfxValue(ui.gbk2unicode(itemName))

    def showDropItems(self):
        itemValList = self.getItemValListByStr(self.widget.mainMC.txtInput.text)
        itemNameList = []
        for dynamicShopItemVal in itemValList:
            itemId = self.getItemIdBySetId(dynamicShopItemVal.setId)
            itemName = ID.data.get(itemId, {}).get('name', '')
            if itemName:
                itemNameList.append({'label': itemName,
                 'setId': dynamicShopItemVal.setId})

        if itemNameList:
            self.itemNameList = itemNameList
            ASUtils.setDropdownMenuData(self.widget.mainMC.txtInput, itemNameList)
        if self.widget.mainMC.txtInput.text == '':
            self.widget.mainMC.txtInput.open()

    def selectItem(self, *args):
        return ASObject(args[3][0]).label

    def _onTabBuyBtnClick(self, *args):
        self.setTabIdx(uiConst.SELF_ADAPTION_SHOP_TAB_TYPE_BUY)

    def _onTabSellBtnClick(self, *args):
        self.setTabIdx(uiConst.SELF_ADAPTION_SHOP_TAB_TYPE_SELL)

    def _onSearchBtnClick(self, *args):
        searchContent = self.widget.mainMC.txtInput.text
        if self.searchContent != searchContent:
            self.refreshTree()

    @ui.callInCD(0.1)
    def handleInputKeyUp(self, *args):
        e = ASObject(args[3][0])
        if int(e.keyCode) == uiConst.AS_KEY_CODE_ENTER:
            self.handleClickSearch()
        else:
            self.showDropItems()

    def handleIndexChange(self, *args):
        index = self.widget.mainMC.txtInput.selectedIndex
        if index < len(self.itemNameList):
            self.searchName = self.itemNameList[index]['label']
            self.searchKey = None
            self.widget.mainMC.txtInput.text = self.searchName
            self.widget.mainMC.txtInput.close()
            self.refreshItemsContent()

    def handleClickSearch(self, *args):
        self.searchName = self.widget.mainMC.txtInput.text
        self.searchKey = None
        self.widget.mainMC.txtInput.close()
        self.refreshItemsContent()

    def scrollWndLabelFunction(self, *args):
        p = BigWorld.player()
        itemData = ASObject(args[3][0])
        itemMC = ASObject(args[3][1])
        self.doScrollWndLabelFunction(itemMC, itemData)

    def doScrollWndLabelFunction(self, itemMC, itemData):
        p = BigWorld.player()
        itemMC.itemData = itemData
        itemMC.slot.setItemSlotData(itemData)
        itemMC.slot.validateNow()
        itemMC.slot.valueAmount.text = str(int(itemData.count)) if DSID.data.get(int(itemData.setId), {}).get('isInventory', 0) else ''
        TipManager.addItemTipById(itemMC.slot, int(itemData.itemId))
        itemMC.slot.dragable = False
        itemMC.txtItemName.htmlText = itemData.name
        itemMC.txtLv.text = itemData.lv
        itemMC.txtPrice.text = itemData.price
        itemMC.arrow.visible = False
        currencyType = int(itemData.priceType)
        setId = int(itemData.setId)
        if self.tabIdx == uiConst.SELF_ADAPTION_SHOP_TAB_TYPE_BUY:
            currencyId = DSID.data.get(setId, {}).get('currencyList', [0, 0])[0] if currencyType == gametypes.DYNAMIC_SHOP_CURRENCY_TYPE_ITEM else DSID.data.get(setId, {}).get('currencyId', 0)
        else:
            currencyId = DSID.data.get(setId, {}).get('currencyId', 0)
        itemMC.bonusIcon.visible = True
        itemMC.itemIcon.visible = False
        if currencyType == gametypes.DYNAMIC_SHOP_CURRENCY_TYPE_CASH_BIND_CASH:
            if currencyId in (gametypes.DYNAMIC_SHOP_BUY_BIND_CASH_FIRST, gametypes.DYNAMIC_SHOP_BUY_ONLY_BIND_CASH):
                itemMC.bonusIcon.bonusType = 'bindCash'
            else:
                itemMC.bonusIcon.bonusType = 'cash'
        elif currencyType == gametypes.DYNAMIC_SHOP_CURRENCY_TYPE_FAME:
            itemMC.bonusIcon.bonusType = 'fame'
            itemMC.bonusIcon.tip = FD.data.get(currencyId, {}).get('name', '')
        elif currencyType == gametypes.DYNAMIC_SHOP_CURRENCY_TYPE_ITEM:
            itemMC.bonusIcon.visible = False
            itemMC.itemIcon.visible = True
            itemMC.itemIcon.fitSize = True
            itemMC.itemIcon.loadImage(uiUtils.getItemIconPath(currencyId))
            TipManager.addItemTipById(itemMC.itemIcon, currencyId)
        else:
            itemMC.bonusIcon.bonusType = 'guildContribution'
        limitKey = 'buyLimitType' if self.tabIdx == uiConst.SELF_ADAPTION_SHOP_TAB_TYPE_BUY else 'sellLimitType'
        limitType = DSID.data.get(setId, {}).get(limitKey, 0)
        if not limitType:
            itemMC.txtLimitType.visible = False
            itemMC.txtLimitCount.visible = False
            itemMC.txtLimitTime.visible = False
        else:
            itemMC.txtLimitType.visible = True
            itemMC.txtLimitType.text = gameStrings.SELF_ADAPTION_SHOP_TXT_LIMIT_BUY if self.tabIdx == uiConst.SELF_ADAPTION_SHOP_TAB_TYPE_BUY else gameStrings.SELF_ADAPTION_SHOP_TXT_LIMIT_SELL
            itemMC.txtLimitCount.visible = True
            itemMC.txtLimitTime.visible = True
            itemMC.txtLimitTime.text = BUY_LIMIT_DES[limitType]
            count, limitCount = p.getDynamicShopItemCount(setId, self.tabIdx == uiConst.SELF_ADAPTION_SHOP_TAB_TYPE_BUY)
            limitDesc = '%d/%d' % (count, limitCount)
            limitDesc = uiUtils.toHtml(limitDesc, TEXT_COLOR_NORMAL if count < limitCount else TEXT_COLOR_RED)
            itemMC.txtLimitCount.htmlText = limitDesc
        itemMC.addEventListener(events.MOUSE_CLICK, self.handleRenderClick, True, 0, True)

    def refreshCashInfo(self, *args):
        if not self.widget:
            return
        p = BigWorld.player()
        self.widget.mainMC.txtCash.text = format(p.cash, ',')
        tianbi = format(p.unbindCoin + p.bindCoin + p.freeCoin, ',')
        unBindTianbi = uiUtils.toHtml(gameStrings.TEXT_ACTIVITYSALEDAILYGIFTPROXY_145 % format(p.unbindCoin, ','), '#79c725')
        tianbiStr = '%s%s' % (tianbi, unBindTianbi)
        self.widget.mainMC.txtFreeCoin.visible = False
        self.widget.mainMC.txtCoint.htmlText = tianbiStr

    def handleTxtInputFocusIn(self, *args):
        self.showDropItems()

    def handleRenderClick(self, *args):
        e = ASObject(args[3][0])
        if int(e.currentTarget.itemData.setId) != self.selectSetId:
            if self.selectRenderMC:
                self.selectRenderMC.gotoAndStop('over')
            self.selectRenderMC = e.currentTarget
            self.selectRenderMC.gotoAndStop('down')
            self.selectSetId = int(e.currentTarget.itemData.setId)
        p = BigWorld.player()
        itemId = int(e.currentTarget.itemData.itemId)
        dynamicShopItemVal = self.set2ValDic.get(int(e.currentTarget.itemData.setId), None)
        if not dynamicShopItemVal:
            return
        elif not self.getItemRemainCount(dynamicShopItemVal):
            if self.tabIdx == uiConst.SELF_ADAPTION_SHOP_TAB_TYPE_BUY:
                p.showGameMsg(GMDD.data.SELF_ADAPTION_SHOP_INV_EMPTY, ())
            else:
                p.showGameMsg(GMDD.data.SELF_ADAPTION_SHOP_INV_FULL, ())
            return
        else:
            if self.tabIdx == uiConst.SELF_ADAPTION_SHOP_TAB_TYPE_SELL and not p.inv.countItemInPages(uiUtils.getParentId(itemId), enableParentCheck=True):
                p.showGameMsg(GMDD.data.SELF_ADAPTION_LACK_ITEM, uiUtils.getItemColorName(itemId))
            else:
                self.uiAdapter.selfAdaptionShopBuyOrSell.show()
            return

    def genItemCategoryList(self):
        ret = []
        schoolData = []
        for key, item in SD.data.iteritems():
            obj = {}
            obj['key'] = key
            obj['value'] = item.get('name', '')
            if not gameglobal.rds.configData.get('enableNewSchoolYeCha', False) and key == const.SCHOOL_YECHA:
                continue
            schoolData.append(obj)

        cate = {}
        cateNames = {}
        for key, value in ICD.data.iteritems():
            category2ItemListDic = self.getCategory2ItemDict()
            if key not in category2ItemListDic:
                continue
            if not value.get('showSubCategory', 0):
                continue
            subCategoryName = value.get('subCategoryName', '')
            needSchool = value.get('needSchool', 0)
            if needSchool:
                cate.setdefault(key[0], []).append([subCategoryName,
                 schoolData,
                 key,
                 True])
            else:
                cate.setdefault(key[0], []).append({'label': subCategoryName,
                 'key': key,
                 'expand': False,
                 'children': []})
            cateNames[key[0]] = value.get('categoryName', '')

        catekeys = cate.keys()
        for index, key in enumerate(catekeys):
            value = cate.get(key)
            ret.append({'label': cateNames[key],
             'children': value,
             'expand': index == 0,
             'key': key})
            if index == 0:
                for childIndex, childValue in enumerate(value):
                    if childIndex == 0:
                        childValue['expand'] = True
                        self.searchKey = childValue['key']
                        self.selectKey = childValue['key']
                        self.searchName = None

        self.itemCategoryList = ret

    def getCategory2ItemDict(self):
        if self.tabIdx == uiConst.SELF_ADAPTION_SHOP_TAB_TYPE_BUY:
            return self.category2BuyItemListDic
        return self.category2SellItemListDic

    def getItemValListByStr(self, searchKey):
        ret = []
        for valList in self.getCategory2ItemDict().values():
            for dynamicShopItemVal in valList:
                if not self.checkSetId(dynamicShopItemVal.setId):
                    continue
                dynamicShopItemVal = self.set2ValDic[dynamicShopItemVal.setId]
                itemId = DSID.data.get(dynamicShopItemVal.setId, {}).get('itemId', 0)
                itemName = ID.data.get(itemId, {}).get('name', '')
                if searchKey == '' or uiUtils.filterPinYin(searchKey, itemName):
                    ret.append(dynamicShopItemVal)

        return ret

    def getItemValListByKey(self, key):
        ret = []
        valList = self.getCategory2ItemDict().get(tuple(key), [])
        for dynamicShopItemVal in valList:
            if not self.checkSetId(dynamicShopItemVal.setId):
                continue
            dynamicShopItemVal = self.set2ValDic[dynamicShopItemVal.setId]
            ret.append(dynamicShopItemVal)

        return ret

    def checkSetId(self, setId):
        dynamicShopType = DSID.data.get(setId, {}).get('dynamicShopType', gametypes.DYNAMIC_SHOP_TYPE_BUY_ONLY)
        if self.tabIdx == uiConst.SELF_ADAPTION_SHOP_TAB_TYPE_BUY and dynamicShopType not in (gametypes.DYNAMIC_SHOP_TYPE_BUY_ONLY, gametypes.DYNAMIC_SHOP_TYPE_BUY_AND_SELL):
            return False
        if self.tabIdx == uiConst.SELF_ADAPTION_SHOP_TAB_TYPE_SELL and dynamicShopType not in (gametypes.DYNAMIC_SHOP_TYPE_SELL_ONLY, gametypes.DYNAMIC_SHOP_TYPE_BUY_AND_SELL):
            return False
        return True

    def getItemsContent(self):
        self.itemsContent = {}
        itemList = []
        self.itemsContent['itemList'] = itemList
        valList = []
        if self.searchName:
            valList = self.getItemValListByStr(self.searchName)
        elif self.searchKey:
            valList = self.getItemValListByKey(self.searchKey)
        for dynamicShopItemVal in valList:
            itemList.append(self.getItemInfo(dynamicShopItemVal.setId))

        itemList.sort(cmp=lambda x, y: cmp(x['price'], y['price']), reverse=self.isNeedSortRevert)
        return self.itemsContent

    def getItemIdBySetId(self, setId):
        if self.tabIdx == uiConst.SELF_ADAPTION_SHOP_TAB_TYPE_BUY:
            return DSID.data.get(setId, {}).get('itemId', 0)
        else:
            return DSID.data.get(setId, {}).get('itemList', (0, 0))[0]

    def getItemInfo(self, setId):
        dynamicShopItemVal = self.set2ValDic.get(setId, None)
        count = self.getItemRemainCount(dynamicShopItemVal)
        itemId = self.getItemIdBySetId(setId)
        itemInfo = uiUtils.getGfxItemById(itemId, count)
        itemInfo['name'] = uiUtils.getItemColorName(itemId)
        itemInfo['lv'] = ID.data.get(itemId, {}).get('lvReq', 1)
        cfgData = DSID.data.get(setId, {})
        itemInfo['price'] = self.uiAdapter.selfAdaptionShopBuyOrSell.getPredictPrice(setId, 1)
        itemInfo['priceType'] = cfgData.get('currencyType', gametypes.DYNAMIC_SHOP_CURRENCY_TYPE_CASH_BIND_CASH)
        itemInfo['setId'] = setId
        return itemInfo

    def getItemRemainCount(self, dynamicShopItemVal):
        if self.tabIdx == uiConst.SELF_ADAPTION_SHOP_TAB_TYPE_BUY:
            return dynamicShopItemVal.inventory
        elif DSID.data.get(dynamicShopItemVal.setId, {}).get('isInventory', 0):
            return max(0, dynamicShopItemVal.maxInventory - dynamicShopItemVal.inventory)
        else:
            return 1

    def refreshTab(self):
        self.widget.tabBuyBtn.selected = self.tabIdx == uiConst.SELF_ADAPTION_SHOP_TAB_TYPE_BUY
        self.widget.tabSellBtn.selected = self.tabIdx == uiConst.SELF_ADAPTION_SHOP_TAB_TYPE_SELL

    def refreshTree(self):
        self.genItemCategoryList()
        self.widget.mainMC.typeTreeList.tree.dataArray = self.itemCategoryList
        self.refreshItemsContent()

    def setTabIdx(self, idx, forceRefresh = False):
        if idx != self.tabIdx or forceRefresh:
            self.searchContent = ''
            self.searchKey = ''
            self.selectKey = None
            self.tabIdx = idx
            self.selectSetId = 0
            self.selectRenderMC = None
            self.refreshTab()
            self.refreshTabContent()

    def refreshTabContent(self):
        if not self.widget:
            return
        self.refreshTree()
        self.refreshItemsContent()

    def refreshItemsContent(self):
        if not self.widget:
            return
        if self.isNeedSortRevert:
            self.widget.mainMC.sortTxt.sortIcon.gotoAndStop('down')
        else:
            self.widget.mainMC.sortTxt.sortIcon.gotoAndStop('up')
        self.getItemsContent()
        self.widget.mainMC.itemScrollWndList.dataArray = self.itemsContent['itemList']
        self.refreshStepNumber()

    def refreshStepNumber(self):
        self.widget.mainMC.itemScrollWndList.numStepper.visible = False
        self.widget.mainMC.itemScrollWndList.bottomBtn.visible = False
        self.widget.mainMC.itemScrollWndList.upBtn.visible = False

    def refreshInfo(self):
        if not self.widget:
            return
        self.setTabIdx(self.tabIdx, True)
        self.refreshItemsContent()
        self.refreshCashInfo()

    def refreshInfoWithoutSetDataArray(self):
        if not self.widget:
            return
        else:
            for itemMC in self.widget.mainMC.itemScrollWndList.items:
                itemData = itemMC.itemData
                setId = int(itemData.setId)
                dynamicShopItemVal = self.set2ValDic.get(setId, None)
                if not dynamicShopItemVal:
                    continue
                itemData.count = self.getItemRemainCount(dynamicShopItemVal)
                itemData.price = dynamicShopItemVal.price
                self.doScrollWndLabelFunction(itemMC, itemData)

            return
