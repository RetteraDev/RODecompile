#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/randomDyeProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gametypes
import ui
import const
import gamelog
from guis import events
from guis import uiConst
from guis import uiUtils
from guis.asObject import ASObject
from uiProxy import UIProxy
from item import Item
from cdata import material_dye_data as MDD
from cdata import game_msg_def_data as GMDD
from gamestrings import gameStrings
from data import equip_data as ED
RANDOM_DYE_NUM = 6

class RandomDyeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(RandomDyeProxy, self).__init__(uiAdapter)
        self.widget = None
        self.posMap = {}
        self.itemCostInfo = {}
        self.dyeItem = None
        self.equipPage = 0
        self.equipPos = 0
        self.resKind = 0
        self.totalCost = 0
        self.itemRevertMap = {}
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_RANDOM_DYE, self.hide)

    def reset(self):
        for key in self.posMap:
            page, pos = key
            gameglobal.rds.ui.inventory.updateSlotState(page, pos)

        self.posMap = {}
        self.itemCostInfo = {}
        self.totalCost = 0
        self.dyeItem = None
        self.equipPage = 0
        self.equipPos = 0
        self.resKind = 0
        self.itemRevertMap = {}

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_RANDOM_DYE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()
        BigWorld.callback(0.1, gameglobal.rds.ui.inventory.updateCurrentPageSlotState)

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_RANDOM_DYE)
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def show(self, equipItem, resKind, equipPage, equipPos):
        if not equipItem:
            return
        self.dyeItem = equipItem
        self.resKind = resKind
        self.equipPage = equipPage
        self.equipPos = equipPos
        self.totalCost = equipItem.fashionEquipDyeMaterialsNum()
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_RANDOM_DYE)
        self.onOpenInventory()
        self.initRevertMap()

    def initRevertMap(self):
        self.itemRevertMap = {}
        for itemId in MDD.data.keys():
            self.itemRevertMap[Item.parentId(itemId)] = itemId

    def onOpenInventory(self):
        if not gameglobal.rds.ui.inventory.mediator:
            gameglobal.rds.ui.inventory.show()
        else:
            gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_INVENTORY, True)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.onConfirmBtnClick, False, 0, True)
        self.widget.cancelBtn.addEventListener(events.BUTTON_CLICK, self.onCancelBtnClick, False, 0, True)

    def onConfirmBtnClick(self, *args):
        msg = gameStrings.WARDROBE_RANDOMDYE_CONFIRM
        self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.randomDyeItem, gameStrings.TEXT_AUTOGENERATEWIDGETEXMODEL_235, self.hide, gameStrings.TEXT_IMPPLAYERTEAM_595)

    def onCancelBtnClick(self, *args):
        self.hide()

    def refreshInfo(self):
        if not self.widget:
            return
        self.refreshItems()

    def isItemDisabled(self, kind, page, pos, item):
        if self.widget:
            if (page, pos) in self.posMap.keys():
                return True
            if not self.haveEmptyPos(item.id):
                return True
            if self.totalCost <= self.getCostNum():
                return True
            if Item.isMaterialItem(item.id) and Item.parentId(item.id) in self.itemRevertMap:
                revertId = self.itemRevertMap.get(Item.parentId(item.id))
                if MDD.data.get(revertId, {}).get('dyeType') == Item.CONSUME_DYE_NORMAL:
                    return False
            return True
        else:
            return False

    @ui.uiEvent(uiConst.WIDGET_RANDOM_DYE, events.EVENT_INVENTORY_ITEM_CLICKED)
    def onInventoryRightClick(self, event):
        event.stop()
        i = event.data['item']
        nPage = event.data['page']
        nItem = event.data['pos']
        if i == None:
            return
        elif not self.haveEmptyPos(i.id):
            return
        else:
            self.setInventoryItem(nPage, nItem)
            return

    def setInventoryItem(self, nPageSrc, nItemSrc):
        p = BigWorld.player()
        srcItem = p.inv.getQuickVal(nPageSrc, nItemSrc)
        if srcItem:
            if Item.parentId(srcItem.id) in self.itemRevertMap:
                if srcItem.hasLatch():
                    p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
                    return
                self.setItem(nPageSrc, nItemSrc, srcItem, srcItem.cwrap)
            else:
                p.showGameMsg(GMDD.data.ITEM_NOT_DYE_TYPE, ())

    def setItem(self, srcBar, srcSlot, item, num):
        requireCost = self.totalCost - self.getCostNum()
        putNum = min(requireCost, num)
        if self.itemCostInfo.has_key(item.id):
            self.itemCostInfo[item.id] += putNum
        else:
            self.itemCostInfo[item.id] = putNum
        self.posMap[srcBar, srcSlot] = (item.id, putNum)
        gameglobal.rds.ui.inventory.updateSlotState(srcBar, srcSlot)
        self.refreshItems()

    def removeItem(self, itemId):
        if self.itemCostInfo.has_key(itemId):
            del self.itemCostInfo[itemId]
        for key in self.posMap.keys():
            posItemId, putNum = self.posMap[key]
            srcBar, srcSlot = key
            if posItemId == itemId:
                self.posMap.pop(key)
                gameglobal.rds.ui.inventory.updateSlotState(srcBar, srcSlot)

        self.refreshItems()

    def refreshItems(self):
        i = 0
        for itemId in self.itemCostInfo:
            itemCost = self.itemCostInfo[itemId]
            slotMc = self.widget.getChildByName('slot%d' % i)
            if slotMc:
                itemData = uiUtils.getGfxItemById(itemId, itemCost)
                slotMc.setItemSlotData(itemData)
                slotMc.dragable = False
                slotMc.itemIdInfo = itemId
                slotMc.addEventListener(events.MOUSE_CLICK, self.onSlotClick, False, 0, True)
            i += 1

        for j in xrange(i, RANDOM_DYE_NUM):
            slotMc = self.widget.getChildByName('slot%d' % j)
            if slotMc:
                slotMc.setItemSlotData(None)

        self.widget.infoText.text = gameStrings.WARDROBE_RANDOMDYE_STR % (self.getCostNum(), self.totalCost)
        if self.getCostNum() >= self.totalCost:
            self.widget.confirmBtn.enabled = True
        else:
            self.widget.confirmBtn.enabled = False

    def onSlotClick(self, *args):
        e = ASObject(args[3][0])
        itemId = e.currentTarget.itemIdInfo
        if e.buttonIdx == uiConst.RIGHT_BUTTON and itemId:
            self.removeItem(itemId)

    def getCostNum(self):
        currentCost = 0
        for itemId in self.itemCostInfo:
            currentCost += self.itemCostInfo[itemId]

        return currentCost

    def haveEmptyPos(self, itemId):
        if len(self.itemCostInfo) < RANDOM_DYE_NUM:
            return True
        if itemId in self.itemCostInfo:
            return True
        return False

    def randomDyeItem(self):
        if self.resKind == const.RES_KIND_WARDROBE_BAG:
            uuid = self.dyeItem.uuid
            pos = uuid
        else:
            pos = str(self.equipPos)
        equipMats = []
        matPages = []
        matPoses = []
        matCounts = []
        for key in self.posMap:
            posItemId, putNum = self.posMap[key]
            srcBar, srcSlot = key
            equipMats.append(posItemId)
            matPages.append(srcBar)
            matPoses.append(str(srcSlot))
            matCounts.append(putNum)

        gamelog.debug('dxk@randomDyeProxy requireRandomDye', self.resKind, self.equipPage, pos, equipMats, matPages, matPoses, matCounts)
        BigWorld.player().base.requireRandomDye(self.resKind, self.equipPage, pos, const.RES_KIND_INV, matPages, matPoses, matCounts)
        self.hide()

    def randomDyeEquipCallback(self, sucess, equRes, equPage, equPos):
        gamelog.debug('dxk@randomDye randomDyeEquipCallback', sucess, equRes, equPage, equPos)
        p = BigWorld.player()
        if sucess:
            if equRes == const.RES_KIND_WARDROBE_BAG:
                uuid = equPos
                item = p.wardrobeBag.getDrobeItems().get(uuid, None)
                if item:
                    gameglobal.rds.ui.dyePlane.setEquip(equPage, equPos, item, equRes)
                else:
                    gameglobal.rds.ui.dyePlane.hide()

    def clearItem(self):
        pass
