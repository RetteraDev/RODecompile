#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/bfDotaShopProxy.o
import BigWorld
from Scaleform import GfxValue
import formula
import const
import Queue
import gamelog
import gameglobal
from gamestrings import gameStrings
from item import Item
from uiProxy import UIProxy
from guis import uiConst
from guis import events
from guis import uiUtils
from guis import ui
from guis.asObject import ASObject
from guis.asObject import TipManager
from guis.asObject import ASUtils
from data import duel_config_data as DCD
from data import item_data as ID
from data import zaiju_data as ZD
from cdata import composite_shop_trade_data as CSTD
from cdata import game_msg_def_data as GMDD
UNION_ITEM_FRAME_PARTS = {1: 'One',
 2: 'Two',
 3: 'Three',
 4: 'Four',
 5: 'Five'}
TAB_ALL_ITEMS = 0
TAB_RECOMMEND_ITEMS = 1

class BfDotaShopProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BfDotaShopProxy, self).__init__(uiAdapter)
        self.widget = None
        self.shopId = 0
        self.itemTree = {}
        self.visibleRecord = True
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_BF_DOTA_SHOP, self.closeFun)

    def reset(self):
        self.bagItemMcList = []
        self.tabNames = []
        self.tabPagesRef = {}
        self.itemTypeIdx = 1
        self.lastItemTypeIdx = 1
        self.pageTabIdx = TAB_RECOMMEND_ITEMS
        self.lastSelectedItem = None
        self.pageStampRef = {}
        self.tabItemsRef = {}
        self.selectedTabMc = None
        self.selectedItemMc = None
        self.selectedItemPos = (0, -1, -1)
        self.selectedBagItemMc = None
        self.selectedUnionItemMc = None
        self.selectedUpperLvItemId = 0
        self.lastOnlySelectedItemId = 0
        self.recommendItemList = []
        self.tagIndexList = []
        self.recommendDataList = []
        self.selectedFavorEquipsKey = 1
        self.customDict = {}
        self.pageCount = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_BF_DOTA_SHOP:
            self.widget = widget
            self.initUI()
            self.refreshInfo()
            if not self.uiAdapter.bfDotaShopPush.widget:
                self.setVisible(False, True)
                self.uiAdapter.bfDotaShopPush.show()

    def clearWidget(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BF_DOTA_SHOP)
        self.widget = None
        self.reset()
        BigWorld.player().base.closePrivateShop(BigWorld.player().openShopId)
        BigWorld.player().openShopId = 0
        BigWorld.player().openShopType = 0

    def setRecommendTab(self):
        p = BigWorld.player()
        recommend_equips = self.getRecommEquip()
        page = 0
        pos = 0
        index = 0
        self.recommendDataList = []
        self.tagIndexList = []
        for equips in recommend_equips:
            if not equips:
                self.tagIndexList.append(-1)
            elif index not in self.tagIndexList:
                self.tagIndexList.append(index)
            data = []
            for itemId in equips:
                if not itemId:
                    continue
                if not self.itemTree.has_key(itemId):
                    continue
                if not data:
                    self.recommendDataList.append(data)
                item = Item(itemId)
                item.compositeId = self.itemTree[itemId]['compositeId']
                self.tabItemsRef.setdefault(0, {})[page, pos] = (item, page, pos)
                data.append(index)
                if len(data) == 3:
                    data = []
                pos += 1
                index += 1

    def show(self, compositeShopId, shopInv, customDict = None, pageCount = None):
        gamelog.debug('@jbx: bfDotaShop show', compositeShopId, shopInv, customDict, pageCount)
        p = BigWorld.player()
        isAllNone = True
        BigWorld.player().openShopId = compositeShopId
        BigWorld.player().openShopType = const.SHOP_TYPE_COMPOSITE
        customDict = self.customDict if not customDict else customDict
        pageCount = self.pageCount if not pageCount else pageCount
        self.customDict = customDict
        self.pageCount = pageCount
        for pageItems in shopInv.pages:
            for item in pageItems:
                if item != None:
                    isAllNone = False

        if isAllNone:
            return
        else:
            i = 0
            self.setVisible(True)
            if not self.widget:
                i += 1
                p.openShopId = compositeShopId
                p.openShopType = const.SHOP_TYPE_COMPOSITE
                customDicKeys = sorted(customDict.keys())
                for key in customDicKeys:
                    if len(customDict[key]) > 0:
                        self.tabNames.append(key[3:])
                        self.tabPagesRef[i] = customDict[key]
                        i += 1

                for page in xrange(len(shopInv.pages)):
                    info = []
                    for pos in xrange(len(shopInv.pages[page])):
                        it = shopInv.getQuickVal(page, pos)
                        if it != const.CONT_EMPTY_VAL:
                            info.append(it)

                    self.setTabData(page, shopInv.stamp[page], info)

                self.genItemTree(shopInv)
                self.setRecommendTab()
                self.uiAdapter.loadWidget(uiConst.WIDGET_BF_DOTA_SHOP)
            else:
                self.refreshInfo()
            return

    def genItemTree(self, shopInv):
        self.itemTree = {}
        BigWorld.player().shopInv = shopInv
        for page in shopInv.pages:
            for item in page:
                if item == const.CONT_EMPTY_VAL:
                    continue
                childList = []
                for itemId, cnt in ID.data.get(item.id, {}).get('dotaEquipFormula', ()):
                    childInfo = {}
                    childInfo['itemId'] = itemId
                    childInfo['cnt'] = cnt
                    childList.append(childInfo)
                    self.itemTree.setdefault(itemId, {}).setdefault('parentIds', set()).add(item.id)

                self.itemTree.setdefault(item.id, {})['childList'] = childList
                self.itemTree.setdefault(item.id, {})['itemId'] = item.id
                self.itemTree.setdefault(item.id, {})['cash'] = CSTD.data.get(item.compositeId, {}).get('consumeDotaBattleFieldCash', 0)
                self.itemTree.setdefault(item.id, {})['lv'] = ID.data.get(item.id, {}).get('dotaEquipLv', 1)
                self.itemTree.setdefault(item.id, {})['compositeId'] = item.compositeId

    def getTabIndex(self, page):
        for tabIndex, pages in self.tabPagesRef.iteritems():
            if page in pages:
                return tabIndex

        return 0

    def setTabData(self, page, stamp, itemInfo):
        self.pageStampRef[page] = stamp
        tabIndex = self.getTabIndex(page)
        pos = 0
        for item in itemInfo:
            self.tabItemsRef.setdefault(tabIndex, {})[page, pos] = (item, page, pos)
            pos += 1

    def sortItemArray(self, itemInfoList):
        itemInfoList.sort(key=lambda x: (x[1], x[2]))
        return itemInfoList

    def initUI(self):
        self.widget.closeBtn.addEventListener(events.MOUSE_CLICK, self.closeFun, False, 0, True)
        self.widget.removeAllInst(self.widget.tabAllItems.tabScrollList.canvas, True)
        self.widget.tabAllItems.tabScrollList.itemRenderer = 'BfDotaShop_shangdiantiaomu'
        self.widget.tabAllItems.tabScrollList.lableFunction = self.tabLableFunction
        self.widget.removeAllInst(self.widget.tabAllItems.itemScrollList.canvas, False)
        self.widget.tabAllItems.itemScrollList.itemWidth = 180
        self.widget.tabAllItems.itemScrollList.itemHeight = 58
        self.widget.tabAllItems.itemScrollList.itemRenderer = 'BfDotaShop_daojuanniu'
        self.widget.tabAllItems.itemScrollList.lableFunction = self.itemLableFunction
        self.widget.tabAllItems.itemScrollList.column = 2
        p = BigWorld.player()
        favorEquipDic = p.favorEquipInfo.get('favorEquipDict', {}).get(self.selectedFavorEquipsKey, {})
        favorEqipAlias = favorEquipDic.get('favorEquipAlias', str(self.selectedFavorEquipsKey))
        if not favorEqipAlias:
            favorEqipAlias = str(self.selectedFavorEquipsKey)
        self.widget.tabRecommend.txtDesc.text = gameStrings.BF_DOTA_SHOP_RECOMMEND_TYPE % favorEqipAlias
        self.widget.removeAllInst(self.widget.tabRecommend.scrollWndList.canvas, False)
        self.widget.tabRecommend.scrollWndList.itemRenderer = 'BfDotaShop_Items'
        self.widget.tabRecommend.scrollWndList.lableFunction = self.recommendItemLableFunction
        self.widget.tabRecommend.scrollWndList.itemHeightFunction = self.recommendItemHeightFunction
        self.widget.removeAllInst(self.widget.itemPageList.canvas, True)
        self.widget.itemPageList.childItem = 'BfDotaShop_daojuicon'
        self.widget.itemPageList.pageItemFunc = self.pageItemFunc
        self.widget.itemPageList.childWidth = 46
        self.widget.buyItem.label = ''
        self.bagItemMcList = []
        for i in xrange(uiConst.BF_DOTA_BAG_ITEM_CNT):
            bagItemMc = self.widget.getChildByName('item%d' % i)
            bagItemMc.icon.fitSize = True
            self.bagItemMcList.append(bagItemMc)
            bagItemMc.bagIdx = i
            bagItemMc.addEventListener(events.MOUSE_CLICK, self.handleBagItemClick, False, 0, True)

        self.widget.buyItem.validateNow()
        self.widget.buyItem.mouseChildren = True
        self.widget.buyItem.icon.fitSize = True
        self.widget.union.visible = False
        self.setTabNams()
        self.widget.buyBtn.addEventListener(events.BUTTON_CLICK, self.handleBuyBtnClick, False, 0, True)
        self.widget.sellBtn.addEventListener(events.BUTTON_CLICK, self.handleSellBtnClick, False, 0, True)
        self.widget.allItemsBtn.addEventListener(events.BUTTON_CLICK, self.handleAllItemsBtnClick, False, 0, True)
        self.widget.recommendItemsBtn.addEventListener(events.BUTTON_CLICK, self.handleRecommendItemsBtn, False, 0, True)
        self.widget.selecFavorEquipMC.visible = False
        isAllDefault = True
        for i in xrange(3):
            equipList = self.getRecommEquip(i + 1, False)[-1]
            if not self.isEquipListEmpty(equipList):
                isAllDefault = False
                break

        self.widget.tabRecommend.changeBtn.visible = gameglobal.rds.configData.get('enableBfDotaHeros', False) and not isAllDefault
        self.widget.tabRecommend.setChildIndex(self.widget.tabRecommend.changeBtn, self.widget.tabRecommend.numChildren - 1)
        self.widget.tabRecommend.changeBtn.x = 160
        self.widget.tabRecommend.changeBtn.addEventListener(events.MOUSE_CLICK, self.handleChangeBtnClick, False, 0, True)
        self.widget.selecFavorEquipMC.closeBtn.addEventListener(events.BUTTON_CLICK, self.handleCloseFavorEquipMCClick, False, 0, True)
        for i in xrange(3):
            favorMC = self.widget.selecFavorEquipMC.getChildByName('favorEquips%d' % i)
            favorMC.selectedBtn.key = i + 1
            favorMC.selectedBtn.addEventListener(events.BUTTON_CLICK, self.handleChangeRecommEquipsClick, False, 0, True)

    def setTabNams(self):
        self.widget.tabAllItems.tabScrollList.dataArray = range(len(self.tabNames))

    def refreshInfo(self):
        if not self.widget:
            return
        self.setTabIdx(self.pageTabIdx, True)
        self.refreshBagItems()
        self.refreshCash()

    def hadItem(self, itemId):
        p = BigWorld.player()
        for _, value in p.battleFieldBag.iteritems():
            if value and value.id == itemId:
                return True

        return False

    def closeFun(self, *args):
        p = BigWorld.player()
        if formula.inDotaBattleField(p.mapID):
            self.setVisible(False)
        else:
            self.hide()

    def getSortedItemListByTabIdx(self, itemTypeIdx):
        itemDict = self.tabItemsRef.get(itemTypeIdx, {})
        sortedItems = self.sortItemArray(itemDict.values())
        itemList = []
        for itemAndPosInfo in sortedItems:
            itemInfo = {}
            item, page, pos = itemAndPosInfo
            itemInfo['iconPath'] = uiUtils.getItemIconPath(item.id)
            itemInfo['position'] = (page, pos)
            itemInfo['itemId'] = item.id
            itemInfo['compositeId'] = item.compositeId
            itemInfo['name'] = uiUtils.getItemColorName(item.id)
            itemInfo['simpleDes'] = ID.data.get(item.id, {}).get('simpleDesc', '')
            itemInfo['consumeCash'] = self.getRealConsumeCash(item.id)
            itemInfo['owned'] = self.hadItem(item.id)
            itemInfo['quality'] = uiUtils.getItemColor(item.id)
            itemList.append(itemInfo)

        return itemList

    def refreshItemList(self):
        if not self.widget or not self.widget.visible or not self.widget.tabAllItems.visible:
            return
        itemList = self.getSortedItemListByTabIdx(self.itemTypeIdx)
        self.widget.tabAllItems.itemScrollList.dataArray = itemList
        self.widget.tabAllItems.itemScrollList.validateNow()
        self.widget.tabAllItems.itemScrollList.scrollbar.validateNow()
        self.widget.tabAllItems.itemScrollList.scrollbar.height = min(self.widget.tabAllItems.itemScrollList.canvasMask.height, self.widget.tabAllItems.itemScrollList.scrollbar.height)

    def refreshRecommendItemList(self):
        if not self.widget or not self.widget.visible or not self.widget.tabRecommend.visible:
            return
        p = BigWorld.player()
        favorEquipDic = p.favorEquipInfo.get('favorEquipDict', {}).get(self.selectedFavorEquipsKey, {})
        favorEqipAlias = favorEquipDic.get('favorEquipAlias', str(self.selectedFavorEquipsKey))
        if not favorEqipAlias:
            favorEqipAlias = str(self.selectedFavorEquipsKey)
        self.widget.tabRecommend.txtDesc.text = gameStrings.BF_DOTA_SHOP_RECOMMEND_TYPE % favorEqipAlias
        self.recommendItemList = self.getSortedItemListByTabIdx(0)
        self.widget.tabRecommend.scrollWndList.dataArray = self.recommendDataList

    def refreshBagItems(self):
        if not self.widget or not self.widget.visible:
            return
        else:
            p = BigWorld.player()
            for i in xrange(uiConst.BF_DOTA_BAG_ITEM_CNT):
                item = p.battleFieldBag.get(i, None)
                if item != None:
                    self.bagItemMcList[i].icon.visible = True
                    uiUtils.addItemTipById(self.bagItemMcList[i], item.id)
                    self.bagItemMcList[i].icon.loadImage(uiUtils.getItemIconPath(item.id))
                    self.bagItemMcList[i].label = str(item.cwrap) if item.cwrap > 1 else ''
                    self.bagItemMcList[i].quality.gotoAndStop(uiUtils.getItemQualityColor(item.id))
                else:
                    if self.selectedBagItemMc and int(self.bagItemMcList[i].bagIdx) == int(self.selectedBagItemMc.bagIdx):
                        self.selectedBagItemMc.selected = False
                        self.selectedBagItemMc = None
                        self.widget.sellBtn.enabled = False
                    self.bagItemMcList[i].icon.visible = False
                    self.bagItemMcList[i].label = ''
                    self.bagItemMcList[i].quality.gotoAndStop('white')

            self.refreshItemListWithOutSetDataArray()
            self.refreshUnionItemParts()
            self.refreshBuyItemParts()
            return

    def refreshCash(self):
        if not self.widget or not self.widget.visible:
            return
        else:
            p = BigWorld.player()
            self.widget.txtCashCnt.text = str(p.battleFieldDotaCash)
            self.widget.sellBtn.enabled = self.selectedBagItemMc != None
            self.refreshBuyItemParts()
            return

    def needOpen(self, composteiShopId):
        if composteiShopId == DCD.data.get('BF_DOTA_COMPOSITE_SHOP_ID', 0):
            return True
        return False

    def tabLableFunction(self, *args):
        itemTypeIdx = int(args[3][0].GetNumber()) + 1
        itemMc = ASObject(args[3][1])
        if itemTypeIdx == self.itemTypeIdx:
            if self.selectedTabMc:
                self.selectedTabMc.selected = False
            self.selectedTabMc = itemMc
        itemMc.selected = itemTypeIdx == self.itemTypeIdx
        itemMc.itemTypeIdx = itemTypeIdx
        itemMc.label = self.tabNames[itemTypeIdx - 1]
        itemMc.addEventListener(events.BUTTON_CLICK, self.handleTabChange, False, 0, True)

    def handleTabChange(self, *args):
        e = ASObject(args[3][0])
        if int(e.currentTarget.itemTypeIdx) == self.itemTypeIdx:
            return
        else:
            if self.selectedTabMc:
                self.selectedTabMc.selected = False
            self.selectedTabMc = e.currentTarget
            self.selectedTabMc.selected = True
            self.itemTypeIdx = int(e.currentTarget.itemTypeIdx)
            self.lastItemTypeIdx = self.itemTypeIdx
            if self.selectedItemMc:
                self.selectedItemMc.selected = False
            self.selectedItemMc = None
            self.selectedItemPos = (self.itemTypeIdx, -1, -1)
            self.refreshItemList()
            return

    def itemLableFunction(self, *args):
        itemInfo = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        self.doItemLableFunction(itemMc, itemInfo)

    def doItemLableFunction(self, itemMc, itemInfo):
        itemMc.validateNow()
        itemMc.mouseChildren = True
        TipManager.addItemTipById(itemMc.item, int(itemInfo.itemId))
        itemMc.data = itemInfo
        itemMc.item.icon.fitSize = True
        itemMc.item.icon.loadImage(itemInfo.iconPath)
        itemMc.itemName.htmlText = itemInfo.name
        ASUtils.autoSizeWithFont(itemMc.itemName, 14, itemMc.itemName.textWidth)
        itemMc.txtValue.text = itemInfo.consumeCash
        itemMc.selected = (self.itemTypeIdx, int(itemInfo.position[0]), int(itemInfo.position[1])) == self.selectedItemPos
        if itemMc.selected:
            self.selectedItemMc = itemMc
        itemMc.prebuy.visible = int(itemInfo.itemId) == self.uiAdapter.bfDotaShopPush.preBuyItemId
        itemMc.owned.visible = itemInfo.owned
        ASUtils.setHitTestDisable(itemMc.owned, True)
        itemMc.item.quality.gotoAndStop(itemInfo.quality)
        itemMc.addEventListener(events.MOUSE_DOWN, self.handleItemClick, False, 0, True)

    def recommendItemHeightFunction(self, *args):
        indexList = ASObject(args[3][0])
        firstIndex = indexList[0]
        height = 94 if firstIndex + 1 in self.tagIndexList else 72
        return GfxValue(height)

    def recommendItemLableFunction(self, *args):
        indexList = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        self.doRecommendItemLableFunction(itemMc, indexList)

    def doRecommendItemLableFunction(self, itemMc, indexList):
        firstIndex = int(indexList[0])
        itemMc.data = indexList
        if firstIndex in self.tagIndexList:
            itemMc.txtTitle.visible = True
            descIdx = self.tagIndexList.index(firstIndex)
            itemMc.txtTitle.text = gameStrings.BF_DOTA_SHOP_RECOMEND_ITEM_LV.get(descIdx, 0)
        else:
            itemMc.txtTitle.visible = False
        for i in range(3):
            realItemMc = itemMc.getChildByName('item%d' % i)
            if i < len(indexList):
                realIndx = int(indexList[i])
                realItemMc.visible = True
                itemInfo = self.recommendItemList[realIndx]
                realItemMc.data = itemInfo
                realItemMc.validateNow()
                realItemMc.mouseChildren = True
                TipManager.addItemTipById(realItemMc.item, itemInfo['itemId'])
                realItemMc.item.icon.fitSize = True
                realItemMc.item.icon.loadImage(itemInfo['iconPath'])
                realItemMc.itemName.htmlText = itemInfo['name']
                ASUtils.autoSizeWithFont(realItemMc.itemName, 14, realItemMc.itemName.textWidth)
                realItemMc.txtValue.text = itemInfo['consumeCash']
                realItemMc.txtDesc.text = itemInfo['simpleDes']
                realItemMc.selected = (self.itemTypeIdx, itemInfo['position'][0], itemInfo['position'][1]) == self.selectedItemPos
                if realItemMc.selected:
                    self.selectedItemMc = realItemMc
                realItemMc.prebuy.visible = itemInfo['itemId'] == self.uiAdapter.bfDotaShopPush.preBuyItemId
                realItemMc.owned.visible = itemInfo['owned']
                ASUtils.setHitTestDisable(realItemMc.owned, True)
                realItemMc.item.quality.gotoAndStop(itemInfo['quality'])
                realItemMc.addEventListener(events.MOUSE_DOWN, self.handleItemClick, False, 0, True)
            else:
                realItemMc.visible = False

    def getSelectedItemId(self):
        item = self.tabItemsRef.get(self.itemTypeIdx, {}).get((self.selectedItemPos[1], self.selectedItemPos[2]), None)
        if item:
            return item[0].id
        else:
            return 0

    def handleItemClick(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        itemInfo = itemMc.data
        newPos = (self.itemTypeIdx, int(itemInfo.position[0]), int(itemInfo.position[1]))
        clickRight = int(e.buttonIdx) == uiConst.RIGHT_BUTTON
        if newPos == self.selectedItemPos and int(itemInfo.itemId) == self.getOnlySelectedItemId() and not clickRight:
            return
        else:
            if self.selectedItemMc:
                self.selectedItemMc.selected = False
            self.selectedItemPos = newPos
            self.selectedItemMc = itemMc
            self.selectedItemMc.selected = True
            self.selectedUpperLvItemId = 0
            if self.selectedBagItemMc:
                self.selectedBagItemMc.selected = False
                self.selectedBagItemMc = None
                self.widget.sellBtn.enabled = False
            self.refreshUnionItemParts()
            self.refreshUpperLvPageList()
            if clickRight:
                self.handleBuyBtnClick()
            return

    def getSelectedBagItemId(self):
        p = BigWorld.player()
        if self.selectedBagItemMc:
            index = int(self.selectedBagItemMc.bagIdx)
            item = p.battleFieldBag.get(index, None)
            if item:
                return item.id
        return 0

    def getOnlySelectedItemId(self):
        if self.selectedUpperLvItemId:
            return self.selectedUpperLvItemId
        bagItemId = self.getSelectedBagItemId()
        itemId = self.getSelectedItemId()
        if itemId:
            return itemId
        return bagItemId

    def getUpperLvItemList(self, itemId):
        itemSet = set()
        parentItemId = itemId
        q = Queue.Queue()
        parentItemIds = list(self.itemTree.get(parentItemId, {}).get('parentIds', set()))
        sortOrderDic = {}
        for itemId in parentItemIds:
            q.put(itemId)
            sortOrderDic[itemId] = self.getSortOrder(itemId)

        while not q.empty():
            id = q.get()
            itemSet.add(id)
            parentItemIds = list(self.itemTree.get(id, {}).get('parentIds', set()))
            for itemId in parentItemIds:
                q.put(itemId)
                sortOrderDic[itemId] = self.getSortOrder(itemId)

        itemList = list(itemSet)
        itemList.sort(cmp=lambda x, y: cmp(sortOrderDic[x], sortOrderDic[y]))
        return itemList

    def getSortOrder(self, itemId):
        lv = ID.data.get(itemId, {}).get('dotaEquipLv', 1)
        cash = self.itemTree[itemId]['cash']
        return (lv, cash, itemId)

    def refreshUpperLvPageList(self):
        if not self.widget or not self.widget.visible:
            return
        if self.widget.union.visible and self.selectedUnionItemMc:
            selectedItemId = int(self.selectedUnionItemMc.itemId)
        else:
            selectedItemId = self.getOnlySelectedItemId()
        upperLvItemList = self.getUpperLvItemList(selectedItemId)
        self.widget.itemPageList.data = upperLvItemList

    def getChildItemList(self, itemId, itemCntDic = {}):
        itemList = []
        queue = Queue.Queue()
        itemInfo = self.itemTree.get(itemId, None)
        if itemInfo:
            queue.put(itemInfo)
            while not queue.empty():
                popInfo = queue.get()
                itemList.append(popInfo)
                childList = popInfo.get('childList', [])
                if childList:
                    for childInfo in popInfo.get('childList', []):
                        for i in xrange(childInfo['cnt']):
                            itemId = childInfo['itemId']
                            if itemCntDic.get(itemId, 0) > 0:
                                itemCntDic[itemId] = itemCntDic[itemId] - 1
                                continue
                            queue.put(self.itemTree[itemId])

        return itemList

    def isEquipListEmpty(self, equipList):
        for id in equipList:
            if id:
                return False

        return True

    def getRecommEquip(self, key = None, addDefault = True):
        key = self.selectedFavorEquipsKey if not key else key
        p = BigWorld.player()
        favorEqupDic = p.favorEquipInfo.get('favorEquipDict', {})
        defaultItemList = ZD.data.get(p.bfDotaZaijuRecord.get(p.gbId, 0), {}).get('recommend_equips', ((),))
        favorEquipList = favorEqupDic.get(key, {}).get('favorEquipList', [])
        if self.isEquipListEmpty(favorEquipList) and addDefault:
            favorEquipList = defaultItemList
        else:
            favorEquipList = ((), (), favorEquipList)
        return favorEquipList

    def getUnionFrameName(self, itemId):
        return ID.data.get(itemId, {}).get('unionFrameName', 'one')

    def getUnionItems(self):
        itemMcList = []
        for index in xrange(self.widget.union.numChildren):
            mc = self.widget.union.getChildAt(index)
            if mc.item:
                mcInfo = {}
                mcInfo['pos'] = (mc.y, mc.x)
                mcInfo['mc'] = mc.item
                itemMcList.append(mcInfo)

        itemMcList.sort(cmp=lambda x, y: cmp(x['pos'], y['pos']))
        return itemMcList

    def refreshUnionItemParts(self):
        if not self.widget or not self.widget.visible:
            return
        selectedItemId = self.getOnlySelectedItemId()
        if not selectedItemId and self.lastOnlySelectedItemId:
            selectedItemId = self.lastOnlySelectedItemId
        if not selectedItemId:
            return
        p = BigWorld.player()
        itemList = self.getChildItemList(selectedItemId)
        frameName = self.getUnionFrameName(selectedItemId)
        itemCntDic = self.getItemCntDic()
        if not itemList:
            self.widget.union.visible = False
            self.refreshBuyItemParts()
            return
        if not frameName:
            self.widget.union.visible = False
            self.refreshBuyItemParts()
            return
        self.widget.union.gotoAndStop(frameName)
        self.widget.union.visible = True
        itemMcList = self.getUnionItems()
        if len(itemList) != len(itemMcList):
            gamelog.error('@jbx:error unsupport frameNames', selectedItemId, frameName)
            self.refreshBuyItemParts()
            return
        hadShowPrebuy = False
        for i, itemInfo in enumerate(itemList):
            itemId = itemInfo['itemId']
            itemMc = itemMcList[i]['mc']
            itemMc.validateNow()
            itemMc.mouseChildren = True
            itemMc.label = ''
            itemMc.icon.fitSize = True
            itemMc.itemId = itemId
            uiUtils.addItemTipById(itemMc, int(itemMc.itemId))
            realConsumeCash = self.getRealConsumeCash(itemId)
            itemMc.parent.txtValue.text = str(realConsumeCash)
            itemMc.icon.loadImage(uiUtils.getItemIconPath(itemId))
            itemMc.parent.prebuy.visible = False
            if itemCntDic.get(itemId, 0):
                itemMc.parent.owned.visible = True
                itemCntDic[itemId] = itemCntDic[itemId] - 1
            else:
                itemMc.parent.owned.visible = False
            if itemId == self.uiAdapter.bfDotaShopPush.preBuyItemId and not hadShowPrebuy:
                itemMc.parent.prebuy.visible = True
                hadShowPrebuy = True
            ASUtils.setHitTestDisable(itemMc.parent.owned, True)
            itemMc.quality.gotoAndStop(uiUtils.getItemColor(itemId))
            itemMc.addEventListener(events.MOUSE_CLICK, self.handleUnionItemClick, False, 0, True)

        if self.lastOnlySelectedItemId != selectedItemId:
            self.selectedUnionItemMc = itemMcList[0]['mc']
            self.selectedUnionItemMc.selected = True
        self.lastOnlySelectedItemId = selectedItemId
        self.refreshBuyItemParts()

    def refreshBuyItemParts(self):
        if not self.widget or not self.widget.visible:
            return
        p = BigWorld.player()
        if self.widget.union.visible and self.selectedUnionItemMc:
            itemId = int(self.selectedUnionItemMc.itemId)
        else:
            itemId = self.getOnlySelectedItemId()
        if itemId == 0:
            self.widget.buyItem.icon.visible = False
            self.widget.txtBuyItemValue.text = ''
            self.widget.buyItem.quality.gotoAndStop('white')
            TipManager.removeTip(self.widget.buyItem)
            return
        self.widget.buyItem.icon.visible = True
        iconPath = uiUtils.getItemIconPath(itemId)
        self.widget.buyItem.icon.loadImage(iconPath)
        self.widget.buyItem.quality.gotoAndStop(uiUtils.getItemColor(itemId))
        uiUtils.addItemTipById(self.widget.buyItem, itemId)
        self.widget.txtBuyItemName.htmlText = uiUtils.getItemColorName(itemId)
        consumeCash = self.getRealConsumeCash(itemId)
        self.widget.txtBuyItemValue.text = str(consumeCash)
        if p.battleFieldDotaCash >= p.battleFieldDotaCash >= consumeCash:
            self.widget.buyBtn.label = gameStrings.BF_DOTA_SHOP_BUY
        else:
            self.widget.buyBtn.label = gameStrings.BF_DOTA_SHOP_PREBUY if itemId != self.uiAdapter.bfDotaShopPush.preBuyItemId else gameStrings.BF_DOTA_SHOP_CANCEL_PREBUY

    def getItemCntDic(self):
        p = BigWorld.player()
        itemCntDic = {}
        for index, item in p.battleFieldBag.iteritems():
            if item:
                itemCntDic[item.id] = itemCntDic.get(item.id, 0) + 1

        return itemCntDic

    def getRealConsumeCash(self, itemId, itemCntDic = None):
        if itemCntDic == None:
            itemCntDic = self.getItemCntDic()
        consumeCash = self.itemTree.get(itemId, {}).get('cash', 0)
        childItemList = self.itemTree.get(itemId, {}).get('childList', [])
        for itemInfo in childItemList:
            itemId = itemInfo['itemId']
            for i in xrange(itemInfo['cnt']):
                if itemCntDic.get(itemId, 0):
                    consumeCash -= self.itemTree.get(itemId, {}).get('cash', 0)
                    itemCntDic[itemId] -= 1
                else:
                    subCash = self.itemTree.get(itemId, {}).get('cash', 0) - self.getRealConsumeCash(itemId, itemCntDic)
                    consumeCash -= subCash

        consumeCash = max(0, consumeCash)
        return consumeCash

    def handleUnionItemClick(self, *args):
        e = ASObject(args[3][0])
        itemMc = e.currentTarget
        clickRight = int(e.buttonIdx) == uiConst.RIGHT_BUTTON
        if self.selectedUnionItemMc:
            if itemMc.itemId == self.selectedUnionItemMc.itemId:
                if clickRight:
                    self.handleBuyBtnClick()
                return
            self.selectedUnionItemMc.selected = False
        self.selectedUnionItemMc = itemMc
        self.selectedUnionItemMc.selected = True
        self.refreshBuyItemParts()
        self.refreshUpperLvPageList()
        if clickRight:
            self.handleBuyBtnClick()

    def handleBagItemClick(self, *args):
        bagItem = ASObject(args[3][0]).currentTarget
        index = int(bagItem.bagIdx)
        p = BigWorld.player()
        if not p.battleFieldBag.get(index, None):
            return
        else:
            if self.selectedItemMc:
                self.selectedItemMc.selected = False
                self.selectedItemMc = None
                self.selectedItemPos = (self.itemTypeIdx, -1, -1)
            if self.selectedBagItemMc:
                if int(self.selectedBagItemMc.bagIdx) == int(bagItem.bagIdx):
                    return
                self.selectedBagItemMc.selected = False
            self.selectedUpperLvItemId = 0
            self.selectedBagItemMc = bagItem
            self.selectedBagItemMc.selected = True
            self.selectedUpperLvItemId = 0
            if self.selectedUnionItemMc:
                self.selectedUnionItemMc.selected = False
                self.selectedUnionItemMc = None
            self.refreshUnionItemParts()
            self.refreshUpperLvPageList()
            self.refreshBagItems()
            self.refreshCash()
            return

    def pageItemFunc(self, *args):
        itemMc = ASObject(args[3][0])
        itemId = int(args[3][1].GetNumber())
        itemMc.itemId = itemId
        itemMc.validateNow()
        itemMc.mouseChildren = True
        itemMc.selected = False
        itemMc.icon.fitSize = True
        itemMc.icon.loadImage(uiUtils.getItemIconPath(itemId))
        itemMc.label = ''
        itemMc.quality.gotoAndStop(uiUtils.getItemColor(itemId))
        TipManager.addItemTipById(itemMc, itemId)
        itemMc.addEventListener(events.MOUSE_CLICK, self.handlePageItemClick, False, 0, True)

    def handlePageItemClick(self, *args):
        itemMc = ASObject(args[3][0]).currentTarget
        itemId = int(itemMc.itemId)
        if self.selectedUnionItemMc:
            self.selectedUnionItemMc.selected = False
            self.selectedUnionItemMc = None
        self.selectedUpperLvItemId = itemId
        self.refreshUnionItemParts()
        self.refreshUpperLvPageList()

    def setVisible(self, value, playSound = True):
        self.visibleRecord = value
        if self.widget and self.widget.visible != value:
            self.widget.visible = value
            if self.widget.visible:
                gameglobal.isWidgetNeedShowCursor = self.uiAdapter.isWidgetNeedShowCursor()
                self.uiAdapter.showCursorForActionPhysics()
                BigWorld.player().ap.restore(False)
                if playSound:
                    self.uiAdapter.playOpenSoundById(uiConst.WIDGET_BF_DOTA_SHOP)
                self.refreshInfo()
            else:
                gameglobal.isWidgetNeedShowCursor = self.uiAdapter.isWidgetNeedShowCursor()
                self.uiAdapter.hideCursorForActionPhysics()
                if playSound:
                    self.uiAdapter.playCloseSoundById(uiConst.WIDGET_BF_DOTA_SHOP)

    @ui.callFilter(1)
    def handleBuyBtnClick(self, *args):
        fromBuyBtn = ASObject(args[3][0]).currentTarget.name == 'buyBtn' if len(args) > 0 else False
        if self.widget.union.visible and self.selectedUnionItemMc and self.selectedUnionItemMc.itemId:
            itemId = int(self.selectedUnionItemMc.itemId)
        else:
            itemId = self.getOnlySelectedItemId()
        p = BigWorld.player()
        consumeCash = self.getRealConsumeCash(itemId)
        if p.battleFieldDotaCash < consumeCash:
            if fromBuyBtn:
                if itemId != self.uiAdapter.bfDotaShopPush.preBuyItemId:
                    self.uiAdapter.bfDotaShopPush.preBuyItemId = itemId
                    self.refreshByPrebuyItemIdChange()
                elif self.uiAdapter.bfDotaShopPush.preBuyItemId:
                    self.uiAdapter.bfDotaShopPush.preBuyItemId = 0
                    self.refreshByPrebuyItemIdChange()
            else:
                p.showGameMsg(GMDD.data.DOTA_CASH_NOT_ENOUTH, ())
        else:
            p.cell.unionEquipment(itemId)

    @ui.callFilter(0.2, True)
    def handleSellBtnClick(self, *args):
        if not self.selectedBagItemMc:
            return
        else:
            p = BigWorld.player()
            bagIdx = int(self.selectedBagItemMc.bagIdx)
            item = p.battleFieldBag.get(bagIdx, None)
            if not item:
                return
            p.cell.sellDotaBattleFieldItem(item.id, bagIdx)
            return

    def handleAllItemsBtnClick(self, *args):
        self.setTabIdx(TAB_ALL_ITEMS)

    def handleRecommendItemsBtn(self, *args):
        self.setTabIdx(TAB_RECOMMEND_ITEMS)

    def handleChangeBtnClick(self, *args):
        self.widget.selecFavorEquipMC.visible = True
        self.refreshSelecFavorEquipMC()

    def handleCloseFavorEquipMCClick(self, *args):
        self.widget.selecFavorEquipMC.visible = False

    def handleChangeRecommEquipsClick(self, *args):
        e = ASObject(args[3][0])
        newKey = int(e.currentTarget.key)
        if self.selectedFavorEquipsKey != newKey:
            self.selectedFavorEquipsKey = newKey
            self.setRecommendTab()
            self.refreshRecommendItemList()
            self.uiAdapter.bfDotaShopPush.resetCacheInfo()
            self.uiAdapter.bfDotaShopPush.refreshInfo()
        self.widget.selecFavorEquipMC.visible = False

    def refreshSelecFavorEquipMC(self):
        p = BigWorld.player()
        for i in xrange(3):
            favorEquipDic = p.favorEquipInfo.get('favorEquipDict', {}).get(i + 1, {})
            favorEquipList = self.getRecommEquip(i + 1, i == 0)[-1]
            favorEqipAlias = favorEquipDic.get('favorEquipAlias', '')
            if not favorEqipAlias:
                favorEqipAlias = gameStrings.BF_DOTA_FAVOR_EQUIPS_ALIAS % str(i + 1)
            mc = self.widget.selecFavorEquipMC.getChildByName('favorEquips%d' % i)
            mc.txtAlias.text = favorEqipAlias
            for i in xrange(6):
                itemMC = mc.getChildByName('item%d' % i)
                itemid = 0
                if i < len(favorEquipList) and favorEquipList[i]:
                    itemid = favorEquipList[i]
                    itemMC.icon.visible = True
                    itemMC.icon.fitSize = True
                    itemMC.icon.loadImage(uiUtils.getItemIconPath(itemid))
                    TipManager.addItemTipById(itemMC, itemid)
                else:
                    itemMC.icon.visible = False
                quality = uiUtils.getItemQualityColor(itemid)
                itemMC.quality.gotoAndStop(quality)

    def setTabIdx(self, index, force = False):
        if force or self.pageTabIdx != index:
            if index != self.pageTabIdx:
                self.selectedItemPos = (0, -1, -1)
                if self.selectedItemMc:
                    self.selectedItemMc.selected = False
                    self.selectedItemMc = None
            self.pageTabIdx = index
            if index == TAB_ALL_ITEMS:
                self.widget.allItemsBtn.selected = True
                self.widget.tabAllItems.visible = True
                self.widget.recommendItemsBtn.selected = False
                self.widget.tabRecommend.visible = False
                if not self.itemTypeIdx:
                    self.itemTypeIdx = self.lastItemTypeIdx
                self.lastItemTypeIdx = self.itemTypeIdx
                self.refreshItemList()
            else:
                self.widget.allItemsBtn.selected = False
                self.widget.tabAllItems.visible = False
                self.widget.recommendItemsBtn.selected = True
                self.widget.tabRecommend.visible = True
                self.itemTypeIdx = 0
                self.refreshRecommendItemList()

    def refreshItemListWithOutSetDataArray(self):
        if self.pageTabIdx == TAB_ALL_ITEMS:
            for itemMc in self.widget.tabAllItems.itemScrollList.items:
                itemInfo = itemMc.data
                itemId = int(itemInfo.itemId)
                itemInfo.consumeCash = self.getRealConsumeCash(itemId)
                itemInfo.owned = self.hadItem(itemId)
                self.doItemLableFunction(itemMc, itemInfo)

        else:
            self.recommendItemList = self.getSortedItemListByTabIdx(0)
            for itemMc in self.widget.tabRecommend.scrollWndList.items:
                itemInfo = itemMc.data
                self.doRecommendItemLableFunction(itemMc, itemInfo)

    def refreshByPrebuyItemIdChange(self):
        self.refreshItemListWithOutSetDataArray()
        self.refreshUnionItemParts()
        self.uiAdapter.bfDotaShopPush.refreshInfo()
        self.refreshBuyItemParts()

    def refreshByBuyItemSucc(self, itemId):
        if itemId == self.uiAdapter.bfDotaShopPush.preBuyItemId:
            self.uiAdapter.bfDotaShopPush.preBuyItemId = 0
            self.refreshByPrebuyItemIdChange()
