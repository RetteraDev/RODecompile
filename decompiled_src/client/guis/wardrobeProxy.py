#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wardrobeProxy.o
from gamestrings import gameStrings
import base64
import BigWorld
import gameglobal
import uiConst
import utils
import const
import gamelog
import gametypes
import commcalc
import ui
import copy
import time
from uiProxy import UIProxy
from helpers import aspectHelper
from helpers import cellCmd
from guis import wardrobeHelper
from data import sys_config_data as SCD
from data import gui_bao_ge_data as GBGD
from data import gui_bao_ge_config_data as GBGCD
from cdata import gui_bao_ge_item_reverse_data as GBGIRD
from data import mall_item_data as MID
from cdata import game_msg_def_data as GMDD
from data import item_data as ID
from data import equip_data as ED
from callbackHelper import Functor
from guis.asObject import TipManager
from guis import events
from guis import uiUtils
from guis import tipUtils
from guis import pinyinConvert
from item import Item
from asObject import ASUtils
from guis.asObject import ASObject
from gamestrings import gameStrings
from data import item_name_data as IND
from data import wardrobe_suit_data as WSD
SUIT_CATE = (100, 100)
CategoryMap = {gameStrings.TEXT_WARDROBEPROXY_41: [SUIT_CATE,
                                     (4, 1),
                                     (4, 2),
                                     (4, 3),
                                     (4, 4),
                                     (4, 5)],
 gameStrings.TEXT_WARDROBEPROXY_42: [(4, 6),
                                     (4, 7),
                                     (4, 8),
                                     (4, 9),
                                     (4, 17),
                                     (4, 18),
                                     (4, 19)],
 gameStrings.TEXT_EQUIPMIXNEWPROXY_183: [(5, 35), (5, 36)]}
ITEM1_HEIGHT = 26
ITEM2_HEIGHT = 28
CLOTH_ITEM_HEIGHT = 136
CLOTH_ITEM_WIDTH = 123
SUIT_ITEM_HEIGHT = 136
SUIT_ITEM_WIDTH = 123
SUIT_TIP_WIDTH = 277
CLOTH_LINE_NUM = 3
SHOP_SOURCE = 4
FILTER_COLORS = [2,
 3,
 4,
 5,
 6]
FILTER_SOURCES = [2,
 3,
 4,
 5,
 6,
 7]
MARK_TYPES = []
STATE_COMMON = 0
STATE_DYE = 1
SUIT_ITEM_NUM = 8
SUIT_ITEM_ITEM_HEIGHT = 72
SUIT_ITEM_ITEM_MARGIN = 5
SUIT_STATES = {1: 'new',
 2: 'recommend',
 3: 'hot'}
DEMO_SUIT_INFOS = {(5, 2, 1): {'icon': 'xxx.dds',
             'suitName': 'Suit Name',
             'state': 1,
             'suitItems': [(620176, 15354), (620691, 15357)]},
 (5, 2, 2): {'icon': 'xxx.dds',
             'suitName': 'Suit Name2',
             'suitItems': [(620176, 15354), (620691, 15357)]}}

class WardrobeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WardrobeProxy, self).__init__(uiAdapter)
        self.widget = None
        self.state = STATE_COMMON
        self.categoryInfo = {}
        self.jumpCate = (4, 2)
        self.filterData = {}
        self.showOnlyOwned = False
        self.currentCateData = ''
        self.searchText = ''
        self.categoryData = None
        self.showSuits = False
        self.selectSuitKey = None
        self.scrollToId = 0
        self.scrollToUUID = ''
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_WARDROBE, self.hideAll)

    def reset(self):
        self.filterData = {}

    def clearAll(self):
        self.categoryInfo = {}
        aspectHelper.getInstance().resetData()

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_WARDROBE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()
            self.queryServerInfo()

    def queryServerInfo(self):
        BigWorld.player().wardrobeBag.requireLoveList()

    def clearWidget(self):
        self.widget = None
        self.searchText = ''
        self.filterData = {}
        self.state = STATE_COMMON
        self.showSuits = False
        self.selectSuitKey = None
        self.showOnlyOwned = False
        self.scrollToId = 0
        self.scrollToUUID = ''
        wardrobeHelper.getInstance().removeWardrobeBg()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WARDROBE)

    def show(self, showCate = None):
        if not gameglobal.rds.configData.get('enableWardrobe', False):
            return
        if self.isJumpCateValid(showCate):
            self.jumpCate = showCate
        elif self.currentCateData:
            self.jumpCate = self.stringToTuple(self.currentCateData)
        else:
            self.jumpCate = (4, 2)
        self.currentCateData = ''
        gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_WARDROBE, True)
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_WARDROBE)
        else:
            self.refreshInfo()

    def setDyeState(self):
        self.state = STATE_DYE
        if self.currentCateData == self.tupleToString(SUIT_CATE):
            self.currentCateData = ''
        self.refreshInfo()

    def clearDyeState(self):
        self.state = STATE_COMMON
        self.refreshInfo()

    def initUI(self):
        self.categoryData = self.genClothCategory()
        self.initAllItems()
        self.initCatergoryTree()
        self.initOtherWnds()
        self.widget.guiBaoGeBtn.addEventListener(events.BUTTON_CLICK, self.handleBtnClick, False, 0, True)
        self.widget.shopBtn.addEventListener(events.BUTTON_CLICK, self.handleBtnClick, False, 0, True)
        self.widget.closeBtn.addEventListener(events.BUTTON_CLICK, self.handleBtnClick, False, 0, True)
        self.widget.filterBtn.addEventListener(events.BUTTON_CLICK, self.handleBtnClick, False, 0, True)
        self.widget.hideWeaponMc.addEventListener(events.EVENT_SELECT, self.handleSignalChanged, False, 0, True)
        self.widget.hideHeadMc.addEventListener(events.EVENT_SELECT, self.handleSignalChanged, False, 0, True)
        self.widget.isHave.addEventListener(events.EVENT_SELECT, self.handleSignalChanged, False, 0, True)
        self.widget.searchInput.addEventListener(events.EVENT_CHANGE, self.handleInputTextChange, False, 0, True)
        self.widget.itemList.cacheAsBitmap = True
        self.widget.suitsList.cacheAsBitmap = True
        self.widget.searchInput.labelFunction = None
        self.widget.searchInput.labelField = None
        self.addEvent(events.EVENT_MY_CLOTH_CHANGED, self.refreshItemsInsiteInfo)
        self.addEvent(events.EVENT_WARDROBE_ITEM_CHANGED, self.refreshItems)
        gameglobal.rds.ui.dyeList.registerEvents()

    def refreshItemsInsiteInfo(self, refreshAll = False):
        if not self.widget:
            return
        if refreshAll:
            if self.widget.itemList.dataArray:
                self.widget.itemList.dataArray = sorted(self.widget.itemList.dataArray, cmp=self.itemSortFunc)
            return
        for i in xrange(self.widget.itemList.canvas.numChildren):
            itemMc = self.widget.itemList.canvas.getChildAt(i)
            self.setClothItemData(itemMc, itemMc.clothData)

    def handleInputTextChange(self, *args):
        searchText = self.widget.searchInput.text
        self.setInputDataProvider(self.widget.searchInput)
        self.searchText = searchText
        self.refreshItems()

    def handelInputKeyBoard(self, *args):
        e = ASObject(args[3][0])
        if e.keyCode == events.KEYBOARD_CODE_ENTER or e.keyCode == events.KEYBOARD_CODE_NUMPAD_ENTER:
            searchText = self.widget.searchInput.text

    def handleBtnClick(self, *args):
        e = ASObject(args[3][0])
        btnName = e.currentTarget.name
        if btnName == 'guiBaoGeBtn':
            gameglobal.rds.ui.guibaoge.show()
        elif btnName == 'shopBtn':
            gameglobal.rds.ui.tianyuMall.show()
        elif btnName == 'closeBtn':
            self.hideAll()
        elif btnName == 'filterBtn':
            self.setFilterVisible(not self.widget.filterMenu.visible)
        elif btnName == 'cancelFilterBtn':
            self.filterData = {}
            self.initFilterInfo()
            self.refreshItems()

    def hideAll(self):
        if self.state == STATE_DYE:
            gameglobal.rds.ui.dyePlane.close()
            return
        wardrobeHelper.getInstance().close()

    def refreshSignalValues(self):
        if not self.widget:
            return
        p = BigWorld.player()
        signal = p.serverSignal
        self.widget.hideWeaponMc.removeEventListener(events.EVENT_SELECT, self.handleSignalChanged)
        self.widget.hideHeadMc.removeEventListener(events.EVENT_SELECT, self.handleSignalChanged)
        self.widget.hideWeaponMc.selected = commcalc.getSingleBit(signal, gametypes.SIGNAL_SHOW_BACK)
        self.widget.hideHeadMc.selected = commcalc.getSingleBit(signal, gametypes.SIGNAL_HIDE_FASHION_HEAD)
        self.widget.hideWeaponMc.addEventListener(events.EVENT_SELECT, self.handleSignalChanged, False, 0, True)
        self.widget.hideHeadMc.addEventListener(events.EVENT_SELECT, self.handleSignalChanged, False, 0, True)

    def handleSignalChanged(self, *args):
        e = ASObject(args[3][0])
        p = BigWorld.player()
        checkName = e.currentTarget.name
        if checkName == 'hideWeaponMc':
            value = 1 if e.currentTarget.selected else 0
            p.cell.setSignal(gametypes.SIGNAL_SHOW_BACK, value)
        elif checkName == 'hideHeadMc':
            value = 1 if e.currentTarget.selected else 0
            p.cell.setSignal(gametypes.SIGNAL_HIDE_FASHION_HEAD, value)
        elif checkName == 'isHave':
            self.showOnlyOwned = e.currentTarget.selected
            self.refreshItems()

    def initOtherWnds(self):
        self.setFilterVisible(False)
        self.setTipVisible(False)

    def initCatergoryTree(self):
        self.widget.typeList.tree.lvItemGap = 2
        self.widget.typeList.tree.itemRenderers = ['Wardrobe_TabAuctionCrossServer_Category', 'Wardrobe_TabAuctionCrossServer_SubCategory']
        self.widget.typeList.tree.itemHeights = [ITEM1_HEIGHT, ITEM2_HEIGHT]
        self.widget.typeList.tree.labelFunction = self.treeLabelFun
        self.widget.typeList.tree.addEventListener(events.EVENT_SELECTED_DATA_CHANGED, self.handleSelectChange, False, 0, True)
        self.widget.typeList.tree.addEventListener(events.EVENT_ITEM_EXPAND_CHANGED, self.handleTreeItemGroupChange, False, 0, True)

    def handleSelectChange(self, *args):
        e = ASObject(args[3][0])
        if e.data and e.data.selectData:
            if self.currentCateData != e.data.selectData:
                self.currentCateData = e.data.selectData
                cateInfo = self.stringToTuple(self.currentCateData)
                if cateInfo == SUIT_CATE:
                    self.showSuits = True
                else:
                    self.showSuits = False
                self.refreshItems()

    def handleTreeItemGroupChange(self, *args):
        e = ASObject(args[3][0])
        target = e.data.item

    def treeLabelFun(self, *args):
        itemMc = ASObject(args[3][0])
        isFirst = args[3][2].GetBool()
        itemMc.isFirst = isFirst
        if isFirst:
            itemData = ASObject(args[3][1]).parent
            self.updateParent(itemMc, itemData)
        else:
            itemData = args[3][1].GetString()
            self.updateChildren(itemMc, itemData)

    def tupleToString(self, tupleInfo):
        return '_'.join((str(i) for i in tupleInfo))

    def stringToTuple(self, tupleStr):
        if tupleStr:
            tupleInfo = tupleStr.split('_')
            return tuple([ int(i) for i in tupleInfo ])

    def updateParent(self, itemMc, itemData):
        itemMc.tf.textField.text = itemData

    def updateChildren(self, itemMc, itemData):
        cateInfo = self.stringToTuple(itemData)
        if cateInfo == SUIT_CATE:
            itemMc.textField.text = gameStrings.WARDROBE_TAOZHUANG
        else:
            itemMc.textField.text = str(self.categoryData.get(cateInfo, ''))
        itemMc.data = cateInfo
        itemMc.selected = False
        if self.currentCateData == itemData:
            itemMc.selected = True
            self.widget.typeList.tree.selectData = self.currentCateData

    def isJumpCateValid(self, cate):
        global CategoryMap
        for key in CategoryMap:
            if cate in CategoryMap.get(key, []):
                return True

        return False

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.typeList.tree.dataArray = self.getTreeData()
        self.widget.typeList.tree.validateNow()
        if not self.currentCateData:
            self.widget.typeList.tree.selectData = self.tupleToString(self.jumpCate)
        else:
            self.widget.typeList.tree.selectData = self.currentCateData
        self.refreshSignalValues()
        self.refreshGuiBaoInfo()

    def refreshGuiBaoInfo(self):
        self.widget.guibaoValueIcon.visible = False
        self.widget.guibaoValueText.visible = False
        self.widget.guiBaoCoinIcon.visible = False
        self.widget.guiBaoCoinText.visible = False

    def refreshItems(self):
        if not self.showSuits:
            self.setTipVisible(False)
            self.widget.suitsList.visible = False
            self.widget.itemList.visible = True
            self.refreshCloths()
        else:
            self.setTipVisible(False)
            self.widget.suitsList.visible = True
            self.widget.itemList.visible = False
            self.refreshSuits()

    def refreshCloths(self):
        category = self.stringToTuple(self.currentCateData)
        itemInfos = self.getItemsInfoByCategory(category)
        self.widget.itemList.labelFunction = self.itemLabelFunc
        self.widget.itemList.column = CLOTH_LINE_NUM
        self.widget.itemList.itemHeight = CLOTH_ITEM_HEIGHT
        self.widget.itemList.itemWidth = CLOTH_ITEM_WIDTH
        self.widget.itemList.itemRenderer = 'Wardrobe_clothItem'
        self.widget.itemList.dataArray = sorted(itemInfos, cmp=self.itemSortFunc)
        self.widget.itemList.validateNow()
        if self.scrollToUUID:
            self.scrollToPosByUUID(self.scrollToUUID)
        elif self.scrollToId:
            self.srcollToPosById(self.scrollToId)
        self.scrollToId = 0
        self.scrollToUUID = ''

    def refreshSuits(self):
        suitsData = self.getSuitData()
        self.selectSuitKey = None
        self.widget.suitsList.labelFunction = self.suitLabelFunc
        self.widget.suitsList.column = CLOTH_LINE_NUM
        self.widget.suitsList.itemHeight = SUIT_ITEM_HEIGHT
        self.widget.suitsList.itemWidth = SUIT_ITEM_WIDTH
        self.widget.suitsList.itemRenderer = 'Wardrobe_suitItem'
        self.widget.suitsList.dataArray = suitsData
        self.widget.suitsList.validateNow()

    def getSuitData(self):
        suitsInfo = WSD.data
        suitsData = []
        p = BigWorld.player()
        for key in suitsInfo:
            if key[0] != p.physique.bodyType:
                continue
            if key[1] != p.physique.sex:
                continue
            suitInfo = copy.deepcopy(suitsInfo.get(key, {}))
            school = getattr(p, 'school', const.SCHOOL_DEFAULT)
            if suitInfo.has_key('school') and suitInfo.get('school', 0) != p.physique.school:
                continue
            suitInfo['key'] = key
            suitItems = []
            for itemInfo in suitInfo['suitItems']:
                itemId = itemInfo[0]
                itemData = ID.data.get(itemId, {})
                if itemData.has_key('schReq'):
                    if school not in itemData['schReq']:
                        continue
                suitItems.append(itemInfo)

            suitInfo['suitItems'] = suitItems
            suitsData.append(suitInfo)

        return suitsData

    def itemSortFunc(self, itemInfoA, itemInfoB):
        p = BigWorld.player()
        uuidStrA = itemInfoA.get('uuid')
        uuidStrB = itemInfoB.get('uuid')
        if uuidStrA and not uuidStrB:
            return -1
        elif not uuidStrA and uuidStrB:
            return 1
        if uuidStrA and uuidStrB:
            uuidA = base64.decodestring(uuidStrA)
            uuidB = base64.decodestring(uuidStrB)
            isLoveA = p.wardrobeBag.isLoveUUID(uuidA)
            isLoveB = p.wardrobeBag.isLoveUUID(uuidB)
            if isLoveA and not isLoveB:
                return -1
            if isLoveB and not isLoveA:
                return 1
        timeDiff = itemInfoB.get('timeIndex', 0) - itemInfoA.get('timeIndex', 0)
        if timeDiff:
            return timeDiff
        itemAId = itemInfoA.get('itemId')
        itemBId = itemInfoB.get('itemId')
        if itemAId != itemBId:
            return itemBId - itemAId
        else:
            return cmp(uuidStrA, uuidStrB)

    def suitLabelFunc(self, *args):
        suitData = ASObject(args[3][0])
        suitMc = ASObject(args[3][1])
        suitMc.suitName.htmlText = suitData.suitName
        iconName = uiUtils.getItemIconFile64(suitData.icon)
        ASUtils.setHitTestDisable(suitMc.suitIcon, True)
        suitMc.suitIcon.fitSize = True
        suitMc.suitIcon.loadImage(iconName)
        if suitData.tips:
            TipManager.addTip(suitMc, suitData.tips)
        else:
            TipManager.removeTip(suitMc)
        if suitData.key == self.selectSuitKey:
            suitMc.bg.selected = True
        else:
            suitMc.bg.selected = False
        count = 0
        for suitItem in suitData.suitItems:
            itemId, mallId = suitItem
            if self.getOwnClothInfo(itemId):
                count += 1

        suitMc.collectText.text = gameStrings.WARDROBE_SUIT_COLLECT % (str(count), str(len(suitData.suitItems)))
        suitState = getattr(suitData, 'state', 0)
        if suitState:
            suitMc.itemLabel.visible = True
            suitMc.itemLabel.gotoAndPlay(SUIT_STATES.get(suitState))
        else:
            suitMc.itemLabel.visible = False
        suitMc.suitData = suitData
        suitMc.addEventListener(events.MOUSE_CLICK, self.onSuitItemClick, False, 0, True)

    def onSuitItemBuyClick(self, *args):
        e = ASObject(args[3][0])
        mallId = e.currentTarget.mallId
        self.uiAdapter.tianyuMall.mallBuyConfirm(mallId, 1, 'wardrobe.0')

    def itemLabelFunc(self, *args):
        itemData = ASObject(args[3][0])
        itemMc = ASObject(args[3][1])
        self.setClothItemData(itemMc, itemData)
        itemMc.loveMc.addEventListener(events.MOUSE_CLICK, self.onLoveClick, False, 0, True)
        itemMc.addEventListener(events.MOUSE_CLICK, self.onClothItemClick, False, 0, True)
        itemMc.addEventListener(events.MOUSE_ROLL_OVER, self.onClothItemRollOver, False, 0, True)
        itemMc.addEventListener(events.MOUSE_ROLL_OUT, self.onClothItemRollOut, False, 0, True)
        itemMc.buyBtn.visible = False
        itemMc.buyBtn.addEventListener(events.MOUSE_CLICK, self.onBuyBtnClick, False, 0, True)
        itemMc.removeBtn.visible = False
        TipManager.addTip(itemMc.removeBtn, gameStrings.WARDROBE_RETURN_ITEM_TIP)
        itemMc.removeBtn.addEventListener(events.MOUSE_CLICK, self.onRemoveBtnClick, False, 0, True)

    def onLoveClick(self, *args):
        e = ASObject(args[3][0])
        e.stopImmediatePropagation()
        p = BigWorld.player()
        itemData = e.currentTarget.parent.clothData
        uuid = base64.decodestring(itemData.uuid)
        isLove = e.currentTarget.isLove
        self.tempUUID = uuid
        p.base.requireChangeItemToLoveList(uuid, not isLove)

    def onClothItemRollOver(self, *args):
        e = ASObject(args[3][0])
        data = e.currentTarget.clothData
        if not data.uuid:
            if SHOP_SOURCE in data.get('source', []):
                e.currentTarget.buyBtn.visible = True
        elif e.currentTarget.filterPart.bg.selected != True:
            if gameglobal.rds.configData.get('enableWardrobeReturn', False):
                e.currentTarget.removeBtn.visible = True

    def onClothItemRollOut(self, *args):
        e = ASObject(args[3][0])
        data = e.currentTarget.clothData
        e.currentTarget.buyBtn.visible = False
        e.currentTarget.removeBtn.visible = False

    def onBuyBtnClick(self, *args):
        e = ASObject(args[3][0])
        data = e.currentTarget.parent.clothData
        e.stopPropagation()
        if not data.uuid:
            itemId = data.itemId
            item = Item(itemId)
            gameglobal.rds.ui.tianyuMall.showMallTab(0, 0, item.name)

    def onRemoveBtnClick(self, *args):
        e = ASObject(args[3][0])
        data = e.currentTarget.parent.clothData
        e.stopPropagation()
        p = BigWorld.player()
        if data.uuid:
            uuid = base64.decodestring(data.uuid)
            cellCmd.removeWardrobeItemFromWardrobe(uuid)

    def calcSuitItemPos(self, parentMc, targetMc):
        globalPosX, globalPosY = ASUtils.local2Global(parentMc, 0, 0)
        posX, posY = globalPosX - self.widget.x, globalPosY - self.widget.y
        return (posX - SUIT_TIP_WIDTH - 10, posY)

    def onSuitStageClick(self, *args):
        if not self.widget:
            return
        else:
            self.selectSuitKey = None
            self.widget.suitsList.dataArray = self.widget.suitsList.dataArray
            self.widget.suitTip.visible = False
            self.widget.stage.removeEventListener(events.MOUSE_CLICK, self.onSuitStageClick)
            return

    def onSuitTipClick(self, *args):
        e = ASObject(args[3][0])
        e.stopImmediatePropagation()

    def setSuitStageEvent(self):
        if self.widget:
            self.widget.stage.addEventListener(events.MOUSE_CLICK, self.onSuitStageClick, False, 0, True)

    @ui.callFilter(0.8)
    def onSuitItemClick(self, *args):
        e = ASObject(args[3][0])
        suitData = e.currentTarget.suitData
        wearSuits = {}
        trialSuits = {}
        for suitItem in suitData.suitItems:
            itemId, mallId = suitItem
            ownItem = self.getOwnClothInfo(itemId)
            if ownItem:
                wearParts = list(ownItem.whereEquip())
                wearPart = wearParts[0]
                wearSuits[wearPart] = ownItem.uuid
            else:
                trialItem = Item(itemId)
                wearParts = list(trialItem.whereEquip())
                trialPart = wearParts[0]
                trialSuits[trialPart] = trialItem

        identifyStr = ''
        if suitData.get('key', ''):
            identifyStr = self.tupleToString(suitData.get('key', ''))
        aspectHelper.getInstance().unwearAllAndEquipMultiEquips(wearSuits, identifyStr=identifyStr, trialInfoDicts=trialSuits)
        self.refreshSuitSelectInfo(e.currentTarget)

    def refreshSuitSelectInfo(self, itemMc):
        data = itemMc.suitData
        if self.selectSuitKey == data.key:
            self.selectSuitKey = None
            self.widget.suitsList.dataArray = self.widget.suitsList.dataArray
            self.widget.suitTip.visible = False
            return
        else:
            if self.widget.suitTip.visible == True:
                self.widget.suitTip.visible = False
                self.widget.stage.removeEventListener(events.MOUSE_CLICK, self.onSuitStageClick)
            self.widget.suitTip.visible = True
            self.widget.suitTip.addEventListener(events.MOUSE_CLICK, self.onSuitTipClick, False, 0, True)
            BigWorld.callback(0.1, self.setSuitStageEvent)
            posX, posY = self.calcSuitItemPos(itemMc, self.widget.suitTip)
            tip = self.widget.suitTip
            tip.x = posX
            tip.y = posY
            suitItem = data.suitItems
            fashionTypeMap = SCD.data.get('fashionTypeMap')
            weaponTypeMap = {35: gameStrings.WARDROBE_WEAPON_ZHUSHOU,
             36: gameStrings.WARDROBE_WEAPON_FUSHOU}
            for index in xrange(SUIT_ITEM_NUM):
                itemMc = tip.getChildByName('pos%d' % index)
                itemMc.y = (SUIT_ITEM_ITEM_HEIGHT + SUIT_ITEM_ITEM_MARGIN) * index + SUIT_ITEM_ITEM_MARGIN
                if itemMc:
                    if index < len(suitItem):
                        suitItemId = suitItem[index][0]
                        itemMc.visible = True
                        uuid = ''
                        item = self.getOwnClothInfo(suitItemId)
                        if item:
                            uuid = base64.encodestring(item.uuid)
                        if not item:
                            item = Item(suitItemId)
                            itemMc.buyBtn.visible = True
                        else:
                            itemMc.buyBtn.visible = False
                        appendInfo = {'itemId': suitItemId,
                         'color': 'nothing',
                         'srcType': 'wardrobe%s' % uuid}
                        itemInfo = uiUtils.getGfxItem(item, appendInfo=appendInfo)
                        itemMc.slot.setItemSlotData(itemInfo)
                        itemMc.nameText.text = item.name
                        equipInfo = ED.data.get(suitItemId, {})
                        if equipInfo:
                            equipType = equipInfo.get('equipType', 0)
                            if equipType == Item.EQUIP_BASETYPE_FASHION:
                                equipSType = equipInfo.get('fashionSType', 0)
                                itemMc.part.text = fashionTypeMap.get(equipSType, '')
                            elif equipType == Item.EQUIP_BASETYPE_FASHION_WEAPON:
                                equipSType = equipInfo.get('weaponSType', 0)
                                itemMc.part.text = weaponTypeMap.get(equipSType, '')
                            else:
                                itemMc.part.text = ''
                        mallId = suitItem[index][1]
                        itemMc.price.visible = False
                        itemMc.priceIcon.visible = False
                        if mallId:
                            price = MID.data.get(mallId, {}).get('priceVal', 0)
                            priceType = MID.data.get(mallId, {}).get('priceType', 0)
                            if price and priceType == gametypes.MALL_PRICE_TYPE_COIN:
                                itemMc.price.visible = True
                                itemMc.priceIcon.visible = True
                                itemMc.price.text = MID.data.get(mallId, {}).get('priceVal', 0)
                                itemMc.priceIcon.bonusType = 'tianBi'
                            itemMc.buyBtn.mallId = mallId
                        else:
                            itemMc.buyBtn.visible = False
                            itemMc.price.visible = False
                            itemMc.priceIcon.visible = False
                        itemMc.buyBtn.addEventListener(events.MOUSE_CLICK, self.onSuitItemBuyClick, False, 0, True)
                    else:
                        itemMc.visible = False

            tip.bg.height = len(suitItem) * (SUIT_ITEM_ITEM_HEIGHT + SUIT_ITEM_ITEM_MARGIN) + SUIT_ITEM_ITEM_MARGIN
            self.selectSuitKey = data.key
            self.widget.suitsList.dataArray = self.widget.suitsList.dataArray
            return

    def getWearClothInfoByUUID(self, uuid):
        p = BigWorld.player()
        for i in xrange(len(p.equipment)):
            equip = p.equipment[i]
            if equip:
                if getattr(equip, 'uuid', '') == uuid:
                    return (True, i)

        return (False, 0)

    def getWearPart(self, item):
        p = BigWorld.player()
        wearPart = item.whereEquip()[0]
        if wearPart == 26 and (p.equipment[26] or aspectHelper.getInstance().trialEquipment.has_key(26)):
            if not p.equipment[27] or not aspectHelper.getInstance().trialEquipment.has_key(27):
                wearPart = 27
        return wearPart

    def processRongGuangClick(self, item):
        p = BigWorld.player()
        if hasattr(item, 'isExpireTTL') and item.isExpireTTL():
            return
        i = p.inv.getQuickVal(self.uiAdapter.inventory.dyeItemPage, self.uiAdapter.inventory.dyeItemPos)
        wearPos = p.getWardrobeItemWearPart(item.uuid)
        invPage = const.INV_PAGE_EQUIP
        if wearPos == -1:
            wearPos = item.uuid
            invPage = const.INV_PAGE_WARDROBE
        if i.isDye():
            self.uiAdapter.inventory._onDyeDesItem(invPage, wearPos)
        elif i.isRongGuang():
            self.uiAdapter.inventory._onRongGuangDesItem(invPage, wearPos)
        elif getattr(i, 'cstype', 0) == Item.SUBTYPE_2_RUBBING_CLEAN:
            self.uiAdapter.inventory._onRubbingCleanItem(invPage, wearPos)

    def isSameCloth(self, itemId1, itemId2):
        return itemId1 == itemId2 or GBGIRD.data.get(itemId1, -1) == GBGIRD.data.get(itemId2, -1) and self.getItemCate(itemId1) == self.getItemCate(itemId2)

    def onClothItemClick(self, *args):
        e = ASObject(args[3][0])
        data = e.currentTarget.clothData
        if self.state == STATE_COMMON:
            gameglobal.rds.ui.dyeList.hide()
            if e.buttonIdx == uiConst.LEFT_BUTTON:
                if e.shiftKey:
                    if data.uuid:
                        uuid = base64.decodestring(data.uuid)
                        self.sendFashionSet(uuid)
                    return
            if not data.uuid:
                isTrial = False
                tiralPart = 0
                for part in aspectHelper.getInstance().trialEquipment:
                    trialItem = aspectHelper.getInstance().trialEquipment.get(part, None)
                    if trialItem and self.isSameCloth(trialItem.id, data.itemId):
                        isTrial = True
                        tiralPart = part
                        break

                if isTrial:
                    pass
                else:
                    item = Item(data.itemId)
                    wearPart = self.getWearPart(item)
                    aspectHelper.getInstance().trialEquip(item, wearPart)
            else:
                uuid = base64.decodestring(data.uuid)
                p = BigWorld.player()
                item = p.wardrobeBag.getDrobeItems().get(uuid, None)
                if item:
                    wearPart = self.getWearPart(item)
                    if hasattr(item, 'isExpireTTL') and item.isExpireTTL():
                        return
                    isEquip, part = self.getWearClothInfoByUUID(uuid)
                    if isEquip:
                        aspectHelper.getInstance().unEquipConflictItems(item, part)
                        gameglobal.rds.ui.dyeList.show(part, item)
                    else:
                        aspectHelper.getInstance().wearWardrobeItem({wearPart: uuid}, identifyStr='dyeList', callBack=Functor(self.onWearSucess, wearPart, uuid))
        elif self.state == STATE_DYE:
            if data.uuid:
                uuid = base64.decodestring(data.uuid)
                p = BigWorld.player()
                item = p.wardrobeBag.getDrobeItems().get(uuid, None)
                if p.wardrobeBag.drobeItems.has_key(uuid):
                    gameglobal.rds.ui.dyePlane.setEquip(0, 0, item, const.RES_KIND_WARDROBE_BAG)
                    self.refreshItems()
                else:
                    p.showGameMsg(GMDD.data.WARDROBE_WEAR_ITEM_CANT_DYE, ())

    def onWearSucess(self, wearPart, uuid, identifyStr):
        gameglobal.rds.ui.dyeList.onWearSucess(wearPart, uuid)

    def sendFashionSet(self, uuid):
        p = BigWorld.player()
        wearPart = p.getWardrobeItemWearPart(uuid)
        if wearPart == -1:
            p.constructItemInfo(const.RES_KIND_WARDROBE_BAG, 0, uuid)
        else:
            p.constructItemInfo(const.RES_KIND_EQUIP, 0, wearPart)

    def setClothItemData(self, itemMc, data):
        itemMc.clothData = data
        itemId = data.itemId
        p = BigWorld.player()
        equipment = p.equipment
        isEquiped = False
        isTrial = False
        item = Item(itemId)
        uuid = ''
        if data.uuid:
            uuid = base64.decodestring(data.uuid)
        if uuid:
            wardrobeItem = p.wardrobeBag.getDrobeItems().get(uuid, None)
            if wardrobeItem:
                item = wardrobeItem
            else:
                return
            isEquiped, equipPart = self.getWearClothInfoByUUID(uuid)
            if not isEquiped:
                for part in aspectHelper.getInstance().trialEquipment:
                    trialItem = aspectHelper.getInstance().trialEquipment.get(part, None)
                    if trialItem and trialItem.id == itemId:
                        if getattr(trialItem, 'uuid', None) and getattr(trialItem, 'uuid', None) == uuid:
                            isTrial = True

        else:
            for part in aspectHelper.getInstance().trialEquipment:
                trialItem = aspectHelper.getInstance().trialEquipment.get(part, None)
                if trialItem and self.isSameCloth(trialItem.id, itemId):
                    isTrial = True

        appendInfo = {'itemId': itemId,
         'color': 'nothing',
         'srcType': 'wardrobe%s' % data.uuid}
        if item.getTTLExpireTime() > 0 and uuid:
            itemMc.overTimeMc.visible = True
            TipManager.addTip(itemMc.overTimeMc, gameStrings.XIUYING_TRANS_REMAIN_TIME % utils.formatTimeStr(item.getTTLExpireTime() - utils.getNow(), gameStrings.TEXT_SKILLPROXY_3418_1))
        else:
            itemMc.overTimeMc.visible = False
            TipManager.removeTip(itemMc.overTimeMc)
        if hasattr(item, 'isExpireTTL') and item.isExpireTTL():
            TipManager.removeTip(itemMc.overTimeMc)
            TipManager.addTip(itemMc.overTimeMc, gameStrings.MALL_APP_OUT_OF_DATE)
            ASUtils.setMcEffect(itemMc.filterPart.slot, 'gray')
        else:
            ASUtils.setMcEffect(itemMc.filterPart.slot, '')
        if uuid:
            itemMc.loveMc.visible = True
            if p.wardrobeBag.isLoveUUID(uuid):
                itemMc.loveMc.isLove = True
                itemMc.loveMc.gotoAndStop('up')
            else:
                itemMc.loveMc.isLove = False
                itemMc.loveMc.gotoAndStop('disable')
            ASUtils.setMcEffect(itemMc.filterPart, '')
        else:
            itemMc.loveMc.visible = False
            ASUtils.setMcEffect(itemMc.filterPart, 'gray')
        if item.isCanDye():
            itemMc.filterPart.dyeMc.visible = True
            TipManager.addTip(itemMc.filterPart.dyeMc, gameStrings.WARDROBE_CAN_DYE)
        else:
            itemMc.filterPart.dyeMc.visible = False
        itemMc.filterPart.bg.label = item.name
        itemMc.shiChuanMc.visible = False
        itemMc.filterPart.bg.selected = False
        itemInfo = uiUtils.getGfxItem(item, appendInfo=appendInfo)
        itemMc.filterPart.slot.dragable = False
        itemMc.filterPart.slot.setItemSlotData(itemInfo)
        if self.state == STATE_COMMON:
            if isTrial:
                itemMc.shiChuanMc.visible = True
                itemMc.filterPart.bg.selected = True
            elif isEquiped:
                itemMc.filterPart.bg.selected = True
        elif self.state == STATE_DYE:
            if gameglobal.rds.ui.dyePlane.isWardrobeItemInDyePlane(uuid):
                itemMc.filterPart.bg.selected = True

    def getItemTipInfoByUUID(self, uuid, itemId):
        p = BigWorld.player()
        if not uuid:
            return tipUtils.getItemTipById(itemId)
        uuid = base64.decodestring(uuid)
        item = p.wardrobeBag.getDrobeItems().get(uuid, None)
        if item:
            return tipUtils.getItemTipByLocation(item, const.ITEM_IN_WARDROBE)
        else:
            return

    def onFilterClick(self, *args):
        e = ASObject(args[3][0])
        e.stopImmediatePropagation()

    def onStageClick(self, *args):
        if not self.widget:
            return
        self.widget.filterMenu.visible = False
        self.widget.stage.removeEventListener(events.MOUSE_CLICK, self.onStageClick)

    def setFilterVisible(self, visible):
        self.widget.filterMenu.visible = visible
        if visible:
            self.initFilterInfo()
            self.widget.filterMenu.addEventListener(events.MOUSE_CLICK, self.onFilterClick, False, 0, True)
            self.widget.stage.removeEventListener(events.MOUSE_CLICK, self.onStageClick)
            BigWorld.callback(0.1, self.setStageEvent)
        self.widget.filterMenu.cancelFilterBtn.addEventListener(events.BUTTON_CLICK, self.handleBtnClick, False, 0, True)

    def setStageEvent(self):
        if self.widget:
            self.widget.stage.addEventListener(events.MOUSE_CLICK, self.onStageClick, False, 0, True)

    def initFilterInfo(self):
        for i in xrange(len(FILTER_COLORS)):
            item = self.widget.filterMenu.getChildByName('color%d' % i)
            item.selected = FILTER_COLORS[i] in self.filterData.get('color', [])
            if item:
                item.addEventListener(events.EVENT_SELECT, self.onFilterItemChanged, False, 0, True)

        for i in xrange(len(FILTER_SOURCES)):
            item = self.widget.filterMenu.getChildByName('from%d' % i)
            item.selected = FILTER_SOURCES[i] in self.filterData.get('source', [])
            if item:
                item.addEventListener(events.EVENT_SELECT, self.onFilterItemChanged, False, 0, True)

        self.widget.filterMenu.like0.selected = self.filterData.get('isLove', False)
        self.widget.filterMenu.like0.addEventListener(events.EVENT_SELECT, self.onFilterItemChanged, False, 0, True)

    def onFilterItemChanged(self, *args):
        e = ASObject(args[3][0])
        filterName = e.currentTarget.name
        isSelect = e.currentTarget.selected
        if filterName.find('color') != -1:
            filterIndex = int(filterName[5:])
            filterValue = FILTER_COLORS[filterIndex]
            if not self.filterData.has_key('color'):
                self.filterData['color'] = set()
            if isSelect:
                self.filterData['color'].add(filterValue)
            else:
                self.filterData['color'].discard(filterValue)
        if filterName.find('from') != -1:
            filterIndex = int(filterName[4:])
            filterValue = FILTER_SOURCES[filterIndex]
            if not self.filterData.has_key('source'):
                self.filterData['source'] = set()
            if isSelect:
                self.filterData['source'].add(filterValue)
            else:
                self.filterData['source'].discard(filterValue)
        if filterName.find('like') != -1:
            if isSelect:
                self.filterData['isLove'] = True
            else:
                self.filterData['isLove'] = False
        self.refreshItems()

    def setTipVisible(self, visible):
        self.widget.suitTip.visible = visible

    def getItemsInfoByCategory(self, category):
        filter = self.filterData
        searchText = self.searchText
        itemInfos = self.categoryInfo.get(category, [])
        res = []
        if searchText:
            for itemInfo in itemInfos:
                itemId = itemInfo.get('itemId')
                tempInfo = ID.data.get(itemId, {})
                if tempInfo.get('name', '').find(searchText) != -1:
                    res.append(itemInfo)

        elif filter:
            colorFilter = filter.get('color', [])
            sourceFilter = filter.get('source', [])
            for itemInfo in itemInfos:
                itemId = itemInfo.get('itemId')
                if colorFilter:
                    quality = uiUtils.getItemQuality(itemId)
                    if quality not in colorFilter:
                        continue
                if sourceFilter:
                    if not set(itemInfo.get('source')) & set(sourceFilter):
                        continue
                res.append(itemInfo)

        else:
            res = itemInfos
        self.refreshCollectStr(res)
        return self.combineWithPocessItems(res)

    def refreshCollectStr(self, itemInfos):
        p = BigWorld.player()
        wardrobeInfo = p.wardrobeBag.getDrobeItems()
        total = len(itemInfos)
        count = 0
        for itemInfo in itemInfos:
            for uuid in wardrobeInfo:
                wardrobeItem = wardrobeInfo.get(uuid)
                if wardrobeItem.id == itemInfo.get('itemId') or wardrobeItem.id in itemInfo.get('associateIds', []):
                    if self.getItemCate(itemInfo.get('itemId')) != self.getItemCate(wardrobeItem.id):
                        continue
                    if hasattr(wardrobeItem, 'isExpireTTL') and wardrobeItem.isExpireTTL():
                        continue
                    else:
                        count += 1
                        break

        self.widget.collectText.htmlText = gameStrings.WARDROBE_COLLECT_RATE % (str(count), str(total))

    def combineWithPocessItems(self, itemInfos):
        filter = self.filterData
        showLove = filter.get('isLove', False)
        combineRes = []
        p = BigWorld.player()
        wardrobeInfo = p.wardrobeBag.getDrobeItems()
        for iteminfo in itemInfos:
            itemId = iteminfo.get('itemId')
            isOwned = False
            for uuid in wardrobeInfo:
                wardrobeItem = wardrobeInfo[uuid]
                if self.state == STATE_DYE:
                    if not wardrobeItem.isCanDye() or hasattr(wardrobeItem, 'isExpireTTL') and wardrobeItem.isExpireTTL():
                        continue
                    if p.getWardrobeItemWearPart(uuid) != -1:
                        continue
                if wardrobeItem.id == itemId or GBGIRD.data.get(wardrobeItem.id, -1) == GBGIRD.data.get(itemId, 0) or wardrobeItem.id in iteminfo.get('associateIds', ()):
                    if showLove and not p.wardrobeBag.isLoveUUID(uuid):
                        continue
                    if self.getItemCate(itemId) == self.getItemCate(wardrobeItem.id):
                        wardrobeItemInfo = {'itemId': itemId,
                         'source': self.getItemSource(itemId),
                         'uuid': base64.encodestring(uuid),
                         'name': wardrobeItem.name,
                         'score': iteminfo.get('score', 0),
                         'associateIds': iteminfo.get('associateIds', ()),
                         'timeIndex': iteminfo.get('timeIndex', 0)}
                        combineRes.append(wardrobeItemInfo)
                        isOwned = True

            if self.state == STATE_DYE:
                continue
            if not isOwned and not showLove and not self.showOnlyOwned:
                combineRes.append(iteminfo)

        return combineRes

    def getOwnClothInfo(self, itemId):
        p = BigWorld.player()
        wardrobeInfo = p.wardrobeBag.getDrobeItems()
        for uuid in wardrobeInfo:
            wardrobeItem = wardrobeInfo[uuid]
            if self.isSameCloth(wardrobeItem.id, itemId):
                return wardrobeItem

    def getTreeData(self):
        treeData = []
        for name in CategoryMap:
            childCate = CategoryMap.get(name, [])
            childData = []
            for itemTuple in childCate:
                if itemTuple == SUIT_CATE:
                    if not gameglobal.rds.configData.get('enableWardrobeSuitShow', False) or self.state != STATE_COMMON:
                        continue
                childData.append(self.tupleToString(itemTuple))

            treeData.append({'parent': name,
             'children': childData})

        return treeData

    def genClothCategory(self):
        fashionTypeMap = SCD.data.get('fashionTypeMap')
        weaponTypeMap = {35: gameStrings.WARDROBE_WEAPON_ZHUSHOU,
         36: gameStrings.WARDROBE_WEAPON_FUSHOU}
        cateData = {}
        for name in CategoryMap:
            childCate = CategoryMap.get(name, [])
            for item in childCate:
                if item[0] == Item.EQUIP_BASETYPE_FASHION:
                    cateData[item] = fashionTypeMap.get(item[1], '')
                elif item[0] == Item.EQUIP_BASETYPE_FASHION_WEAPON:
                    cateData[item] = weaponTypeMap.get(item[1], '')

        return cateData

    def initAllItems(self):
        if self.categoryInfo:
            return
        for itemId in GBGD.data:
            self.tryAddItemInfo(itemId)
            if GBGD.data.get(itemId, {}).get('schoolweaponId', 0):
                self.tryAddItemInfo(GBGD.data.get(itemId, {}).get('schoolweaponId', 0))

    def tryAddItemInfo(self, itemId):
        p = BigWorld.player()
        bodyType = p.physique.bodyType
        school = getattr(p, 'school', const.SCHOOL_DEFAULT)
        playerSex = getattr(p.physique, 'sex', -1)
        if not utils.inAllowBodyType(itemId, bodyType):
            return
        itemData = ID.data.get(itemId, {})
        if not utils.inAllowSex(itemId, playerSex):
            return
        if itemData.has_key('schReq'):
            if school not in itemData['schReq']:
                return
        key = self.getItemCate(itemId)
        if key:
            if not self.categoryInfo.has_key(key):
                self.categoryInfo[key] = []
            itemInfo = {'itemId': itemId,
             'source': self.getItemSource(itemId),
             'uuid': '',
             'name': itemData['name'],
             'associateIds': GBGD.data.get(itemId, {}).get('associateIds', ()),
             'score': GBGD.data.get(itemId, {}).get('score', 0),
             'timeIndex': GBGD.data.get(itemId, {}).get('thirdCate', (0,))[0]}
            self.categoryInfo[key].append(itemInfo)

    def getItemCate(self, itemId):
        equipInfo = ED.data.get(itemId, {})
        if equipInfo:
            equipType = equipInfo.get('equipType', 0)
            equipSType = 0
            if equipType == Item.EQUIP_BASETYPE_FASHION:
                equipSType = equipInfo.get('fashionSType', 0)
                if equipSType == Item.EQUIP_FASHION_SUBTYPE_HEADWEAR_FRONT or equipSType == Item.EQUIP_FASHION_SUBTYPE_HEADWEAR_LR:
                    equipSType = Item.EQUIP_FASHION_SUBTYPE_HEADWEAR_ASSEMBLE
            elif equipType == Item.EQUIP_BASETYPE_FASHION_WEAPON:
                equipSType = equipInfo.get('weaponSType', 0)
                equipSType = Item.EQUIP_PART_TABLE[equipType][equipSType][0]
            if equipType and equipSType:
                key = (equipType, equipSType)
                return key

    def getItemSource(self, itemId):
        guibaoInfo = GBGD.data.get(itemId, {})
        subCate = guibaoInfo.get('subCate', ())
        return subCate

    def scrollToItem(self, itemId, uuid = None):
        if not self.widget:
            return
        itemCate = self.getItemCate(itemId)
        if self.widget.typeList.tree.selectData == self.tupleToString(itemCate):
            if uuid:
                self.scrollToPosByUUID(uuid)
            elif itemId:
                self.srcollToPosById(itemId)
        else:
            self.scrollToId = itemId
            self.scrollToUUID = uuid
            self.widget.typeList.tree.selectData = self.tupleToString(itemCate)
            self.widget.typeList.validateNow()

    def scrollToPosByUUID(self, uuid):
        itemDataArray = self.widget.itemList.dataArray
        uuidStr = base64.encodestring(uuid)
        for index, itemData in enumerate(itemDataArray):
            wardrobeItemUUID = itemData.get('uuid', '')
            if wardrobeItemUUID and wardrobeItemUUID == uuidStr:
                pos = self.widget.itemList.getIndexPosY(index)
                self.widget.itemList.scrollTo(pos)
                return

    def srcollToPosById(self, itemId):
        itemDataArray = self.widget.itemList.dataArray
        for index, itemData in enumerate(itemDataArray):
            wardrobeItemId = itemData.get('itemId', -1)
            if itemId == wardrobeItemId or itemId in itemData.get('associateIds'):
                pos = self.widget.itemList.getIndexPosY(index)
                self.widget.itemList.scrollTo(pos)
                return

    def setInputDataProvider(self, inputMc):
        ASUtils.setDropdownMenuData(inputMc, self.onGetItemNames(inputMc.text))
        if inputMc.text == '':
            inputMc.open()

    def onGetItemNames(self, name):
        name = name.strip()
        ret = []
        if name == '':
            return ret
        name = name.lower()
        isPinyinAndHanzi = utils.isPinyinAndHanzi(name)
        if isPinyinAndHanzi == const.STR_HANZI_PINYIN:
            return ret
        pinyin = pinyinConvert.strPinyinFirst(name)
        names = IND.data.get(uiConst.ITEM_NAME_ALL, {}).get(pinyin[0], [])
        finalSearch = []
        category = self.stringToTuple(self.currentCateData)
        itemsData = self.categoryInfo.get(category, [])
        for itemInfo in itemsData:
            if itemInfo.get('name', '') in names:
                finalSearch.insert(0, itemInfo.get('name', ''))

        return finalSearch
