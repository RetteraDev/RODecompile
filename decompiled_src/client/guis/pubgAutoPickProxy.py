#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/pubgAutoPickProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import keys
import gametypes
import const
import pubgUtils
import ui
import utils
from guis import hotkeyProxy
from uiProxy import UIProxy
from item import Item
from guis import uiUtils
from ui import unicode2gbk
from guis import asObject
from guis.asObject import ASObject
from guis.asObject import ASUtils
from guis.asObject import TipManager
from gamestrings import gameStrings
import clientUtils
from data import duel_config_data as DCD
from data import consumable_item_data as CID
from data import item_data as ID
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD

class PubgAutoPickProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PubgAutoPickProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_PUBG_AUTO_PICK, self.hide)

    def reset(self):
        self.itemEntIdList = list()
        self.itemDataDict = dict()
        self.treasureBoxId = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_PUBG_AUTO_PICK:
            self.widget = widget
            self.initUI()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_PUBG_AUTO_PICK)

    @property
    def pubgAutoPickEquipFilterList(self):
        return DCD.data.get('pubgAutoPickEquipFilterType', [(3, gameStrings.PUBG_AUTO_PICK_EQUIP_FILTER_BLUE, ''), (4, gameStrings.PUBG_AUTO_PICK_EQUIP_FILTER_PURPLE, '')])

    def initUI(self):
        if not self.widget:
            return
        _, _, desc = hotkeyProxy.getPickAsKeyContent()
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.pickSettingBtn.addEventListener(events.BUTTON_CLICK, self.handlePickSettingBtnClick, False, 0, True)
        self.widget.pickBtn.addEventListener(events.BUTTON_CLICK, self.handlePickBtnClick, False, 0, True)
        self.widget.pickBtn.label = gameStrings.PUBG_AUTO_PICK_BTN_LABEL % desc
        self.initCheckBoxUI()
        self.initItemsScrollViewUI()

    def initCheckBoxUI(self):
        p = BigWorld.player()
        for idx, filterData in enumerate(self.pubgAutoPickEquipFilterList):
            checkBox = getattr(self.widget, 'filterCheckBox%d' % idx)
            checkBoxContent = getattr(self.widget, 'filterCheckBoxContent%d' % idx)
            if checkBox and checkBoxContent:
                checkBox.selected = p.checkPickFilterTypeEnable(filterData[0])
                checkBox.filterType = filterData[0]
                checkBox.addEventListener(events.BUTTON_CLICK, self.handleFilterCheckBoxClick, False, 0, True)
                checkBoxContent.addEventListener(events.MOUSE_CLICK, self.handleFilterCheckBoxClick, False, 0, True)
                checkBoxContent.htmlText = filterData[1]
                TipManager.addTip(checkBox, filterData[2])
                TipManager.addTip(checkBoxContent, filterData[2])

        self.widget.autoPickCheckBoxContent.text = gameStrings.PUBG_AUTO_PICK_TEXT
        self.widget.autoPickCheckBox.selected = p.checkEnableAutoPick()
        self.widget.autoPickCheckBox.addEventListener(events.BUTTON_CLICK, self.handleAutoPickClick, False, 0, True)

    def initItemsScrollViewUI(self):
        listMc = self.widget.mainContent
        listMc.itemRenderer = 'PUBGAutoPick_ScrollWndListItems'
        listMc.lableFunction = self.itemDataListLabelFunction
        listMc.column = 1
        listMc.itemWidth = 201
        listMc.itemHeight = 65
        listMc.dataArray = self.itemEntIdSortList
        listMc.validateNow()

    def handleFilterCheckBoxClick(self, *args):
        p = BigWorld.player()
        checkBoxMc = ASObject(args[3][0]).currentTarget
        if str(checkBoxMc.name).startswith('filterCheckBoxContent'):
            checkBoxIdx = str(str(checkBoxMc.name).replace('filterCheckBoxContent', ''))
            realcheckBoxMc = getattr(self.widget, 'filterCheckBox' + checkBoxIdx)
            checkBoxSelected = not bool(realcheckBoxMc.selected)
            filterType = int(realcheckBoxMc.filterType)
            realcheckBoxMc.selected = checkBoxSelected
        else:
            checkBoxSelected = bool(checkBoxMc.selected)
            filterType = int(checkBoxMc.filterType)
        p.setPickFilterTypeEnable(filterType, checkBoxSelected)
        if filterType == self.pubgAutoPickEquipFilterList[1][0] and checkBoxSelected:
            checkBox0 = getattr(self.widget, 'filterCheckBox0')
            checkBox0.selected = True
            p.setPickFilterTypeEnable(self.pubgAutoPickEquipFilterList[0][0], True)
        self.refreshAll()

    def handleAutoPickClick(self, *args):
        checkBoxSelected = bool(ASObject(args[3][0]).currentTarget.selected)
        p = BigWorld.player()
        p.setEnableAutoPick(checkBoxSelected)
        self.refreshAll()

    def handlePickSettingBtnClick(self, *args):
        gameglobal.rds.ui.pubgAutoPickSetting.show()

    def handlePickBtnClick(self, *args):
        self.pickAllItems()
        self.hide()

    def itemDataListLabelFunction(self, *args):
        if not self.treasureBoxId:
            itemEntId = int(args[3][0].GetNumber())
        else:
            itemEntId = args[3][0].GetString()
        itemMc = ASObject(args[3][1])
        itemData = self.itemDataDict[itemEntId]['itemData']
        itemId = self.itemDataDict[itemEntId]['itemId']
        itemCount = self.itemDataDict[itemEntId]['itemCount']
        color = uiUtils.getColorByQuality(itemData['quality'])
        iconPath = uiUtils.getItemIconPath(itemId, uiConst.ICON_SIZE64)
        itemMc.itemId = itemId
        itemMc.itemTempId = itemEntId
        if itemCount and itemCount > 1:
            itemMc.content.num.visible = True
            itemMc.content.num.text = str(itemCount)
        else:
            itemMc.content.num.visible = False
        itemMc.content.textField.gotoAndStop(color)
        itemMc.content.textField.textField.text = itemData['name']
        itemMc.content.colorFrame.gotoAndPlay(color)
        itemMc.content.icon.fitSize = True
        itemMc.content.icon.loadImage(iconPath)
        itemMc.addEventListener(events.MOUSE_ROLL_OUT, self.handleListItemsRollOut, False, 0, True)
        itemMc.addEventListener(events.MOUSE_ROLL_OVER, self.handleListItemsRollOver, False, 0, True)
        itemMc.addEventListener(events.MOUSE_CLICK, self.handleListItemsClick, False, 0, True)
        TipManager.addItemTipById(itemMc, itemId, True, 'right')

    def handleListItemsRollOut(self, *args):
        ASObject(args[3][0]).currentTarget.gotoAndStop('up')

    def handleListItemsRollOver(self, *args):
        ASObject(args[3][0]).currentTarget.gotoAndStop('over')

    def handleListItemsClick(self, *args):
        e = ASObject(args[3][0])
        if e.buttonIdx == uiConst.RIGHT_BUTTON:
            self.pickOneItem(e.currentTarget.itemTempId)

    def refreshAll(self):
        self.refreshUI()

    def refreshUI(self):
        if not self.widget:
            return
        listMc = self.widget.mainContent
        listMc.dataArray = self.itemEntIdSortList
        listMc.validateNow()

    def refreshAllByBoxId(self, treasureBoxId, itemUUIDs):
        if self.treasureBoxId != treasureBoxId:
            return
        for idx, itemGuid in enumerate(self.itemEntIdList):
            itemUUID = self.getUUIDFromGUID(itemGuid)
            if itemUUID and itemUUID in itemUUIDs:
                self.itemEntIdList.pop(idx)
                del self.itemDataDict[itemGuid]

        if len(self.itemEntIdList) == 0:
            self.hide()
        else:
            self.refreshAll()

    def getUUIDFromGUID(self, tempGuid):
        for guid, itemData in self.itemDataDict.iteritems():
            item = itemData.get('Item', None)
            if guid == tempGuid and item:
                return item.uuid

        return 0

    def getGUIDFromUUID(self, uuid):
        for guid, itemData in self.itemDataDict.iteritems():
            item = itemData.get('Item', None)
            if item and item.uuid == uuid:
                return guid

        return 0

    def genItemDataList(self, items):
        del self.itemEntIdList[:]
        self.itemDataDict.clear()
        for item in items:
            if utils.instanceof(item, 'DroppedItem'):
                self.itemDataDict[item.id] = {'itemId': item.itemId,
                 'Item': Item(id=item.itemId, cwrap=int(item.itemNum), genRandProp=False),
                 'itemData': item.itemData,
                 'itemCount': int(item.itemNum)}
                self.itemEntIdList.append(item.id)
            elif utils.instanceof(item, 'Item'):
                self.itemDataDict[item.guid()] = {'itemId': item.id,
                 'Item': item,
                 'itemData': ID.data.get(item.id, {}),
                 'itemCount': int(item.cwrap)}
                self.itemEntIdList.append(item.guid())

    def show(self, droppedItemEnts, boxId = 0):
        self.treasureBoxId = boxId
        self.genItemDataList(droppedItemEnts)
        if droppedItemEnts and len(droppedItemEnts) >= 1:
            if not self.widget:
                self.uiAdapter.loadWidget(uiConst.WIDGET_PUBG_AUTO_PICK)
            else:
                self.refreshAll()
        else:
            self.hide()

    def hideByBoxId(self, treasureBoxId):
        if treasureBoxId != 0 and self.treasureBoxId == treasureBoxId:
            self.hide()

    def hide(self, destroy = True):
        if self.treasureBoxId:
            box = BigWorld.entities.get(self.treasureBoxId)
            if box:
                box.cell.onClientCloseBox()
        super(PubgAutoPickProxy, self).hide(destroy)

    @property
    def isPUBGAutoPickOpening(self):
        if self.widget:
            return True
        return False

    @property
    def isPUBGAutoPickInTreasureBox(self):
        if self.treasureBoxId:
            return True
        return False

    def getItemTypeInPUBG(self, itemId, itemData):
        p = BigWorld.player()
        if itemData['type'] == Item.BASETYPE_EQUIP:
            return pubgUtils.AUTO_PICK_EQUIPMENT
        else:
            itemConsumableData = CID.data.get(itemId, None)
            if itemConsumableData:
                itemSubType = itemConsumableData.get('sType', None)
                itemSkillSSypeSet = [Item.SUBTYPE_2_PUBG_SKILL_BOOK_LEARN, Item.SUBTYPE_2_PUBG_SKILL_BOOK_UNLOCK]
                if itemSubType and itemSubType in itemSkillSSypeSet:
                    return pubgUtils.AUTO_PICK_SKILL
                if itemSubType and itemSubType in DCD.data.get('pubgItemType', []):
                    return pubgUtils.AUTO_PICK_POTION
            return pubgUtils.AUTO_PICK_OTHERS

    def pubgPickItemSortCmp(self, entIdA, entIdB):
        itemDataA = self.itemDataDict[entIdA]['itemData']
        itemIdA = self.itemDataDict[entIdA]['itemId']
        itemDataB = self.itemDataDict[entIdB]['itemData']
        itemIdB = self.itemDataDict[entIdB]['itemId']
        itemQualityA = itemDataA.get('quality', 1)
        itemQualityB = itemDataB.get('quality', 1)
        if itemQualityA != itemQualityB:
            return cmp(itemQualityB, itemQualityA)
        else:
            itemTypeA = self.getItemTypeInPUBG(itemIdA, itemDataA)
            itemTypeB = self.getItemTypeInPUBG(itemIdB, itemDataB)
            pubgPickItemSortTypeList = DCD.data.get('pubgPickItemSortTypeList', [1,
             2,
             3,
             4])
            itemTypeIdxA = pubgPickItemSortTypeList.index(itemTypeA)
            itemTypeIdxB = pubgPickItemSortTypeList.index(itemTypeB)
            return cmp(itemTypeIdxA, itemTypeIdxB)

    @property
    def itemEntIdSortList(self):
        p = BigWorld.player()
        resultItemEntIdList = sorted(self.itemEntIdList, cmp=self.pubgPickItemSortCmp)
        return resultItemEntIdList

    @property
    def itemFilterEntIdList(self):
        p = BigWorld.player()
        resultItemEntIdList = list()
        for itemTempId in self.itemEntIdList:
            itemData = self.itemDataDict[itemTempId]['itemData']
            item = self.itemDataDict[itemTempId]['Item']
            if itemData['type'] == Item.BASETYPE_EQUIP:
                p.tempPUBGItem = item
                isFilter = False
                for filterData in self.pubgAutoPickEquipFilterList:
                    if p.checkPickFilterTypeEnable(filterData[0]) and itemData['quality'] == filterData[0]:
                        canEquip, _ = p.checkGetBestMainEquipPart(item)
                        isFilter = not canEquip
                        break

                if isFilter:
                    continue
            if p.checkEnableAutoPick():
                if not p.checkAutoPickTypeEnable(pubgUtils.AUTO_PICK_EQUIPMENT) and itemData['type'] == Item.BASETYPE_EQUIP:
                    continue
                itemConsumableData = CID.data.get(self.itemDataDict[itemTempId]['itemId'], None)
                if itemConsumableData:
                    itemSubType = itemConsumableData.get('sType', None)
                    itemSkillSSypeSet = [Item.SUBTYPE_2_PUBG_SKILL_BOOK_LEARN, Item.SUBTYPE_2_PUBG_SKILL_BOOK_UNLOCK]
                    if not p.checkAutoPickTypeEnable(pubgUtils.AUTO_PICK_SKILL) and itemSubType and itemSubType in itemSkillSSypeSet:
                        continue
                    if not p.checkAutoPickTypeEnable(pubgUtils.AUTO_PICK_POTION) and itemSubType and itemSubType in DCD.data.get('pubgItemType', []):
                        continue
            resultItemEntIdList.append(itemTempId)

        return resultItemEntIdList

    def pickAllItems(self):
        p = BigWorld.player()
        if len(self.itemFilterEntIdList) >= 1:
            if not self.treasureBoxId:
                p.cell.pickNearItem(self.itemFilterEntIdList)
            else:
                box = BigWorld.entities.get(self.treasureBoxId)
                if not box:
                    return
                itemDataList = list()
                for itemGbId in self.itemFilterEntIdList:
                    itemUUID = self.getUUIDFromGUID(itemGbId)
                    if not itemUUID:
                        continue
                    itemData = self.itemDataDict[itemGbId]
                    tempDataDict = {'itemId': itemData.get('itemId', 0),
                     'amount': int(itemData.get('itemCount', 1)),
                     'uuid': itemUUID,
                     'src': itemData.get('Item', None)}
                    itemDataList.append(tempDataDict)

                pageAndPosResult = p.crossInv.searchBestInPagesWithList(itemDataList)
                realPickResult = []
                bagFullError = False
                for itemUUID, (page, pos) in pageAndPosResult.iteritems():
                    if page == const.CONT_NO_PAGE or pos == const.CONT_NO_POS:
                        bagFullError = True
                        continue
                    realPickResult.append({'page': page,
                     'pos': pos,
                     'uuid': itemUUID})

                bagFullError and p.showGameMsg(GMDD.data.ITEM_GET_SOME_BUT_CROSS_BAG_FULL_IN_PUBG, ())
                box.cell.confirmPickPartItem(realPickResult)

    def pickOneItem(self, itemTempId):
        p = BigWorld.player()
        if itemTempId:
            if not self.treasureBoxId:
                entId = itemTempId
                BigWorld.player().cell.pickNearItem([entId])
            else:
                itemGbId = itemTempId
                box = BigWorld.entities.get(self.treasureBoxId)
                if not box:
                    return
                itemUUID = self.getUUIDFromGUID(itemGbId)
                if not itemUUID:
                    return
                item = self.itemDataDict[itemGbId].get('Item', None)
                if item:
                    dstPg, dstPos = p.crossInv.searchBestInPages(item.id, item.cwrap, item)
                    if dstPg == const.CONT_NO_PAGE:
                        p.showGameMsg(GMDD.data.ITEM_GET_CROSS_BAG_FULL_IN_PUBG, ())
                        return
                    box.cell.confirmPickOneItem(itemUUID, dstPg, dstPos)
