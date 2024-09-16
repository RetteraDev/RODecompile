#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/equipGemProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import utils
import const
from guis import ui
from guis import uiConst
from guis import uiUtils
from uiProxy import SlotDataProxy
from ui import gbk2unicode
from item import Item
from callbackHelper import Functor
from guis import events
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD

class EquipGemProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(EquipGemProxy, self).__init__(uiAdapter)
        self.modelMap = {'closeWidget': self.onClose,
         'changeTab': self.onChangeTab,
         'addGem': self.onAddGem,
         'removeGem': self.onRemoveGem,
         'returnItemToBag': self.onRemoveItemToBag,
         'selectGem': self.onSelectGem,
         'clickOnLockedSlot': self.onClickLockedSlot}
        self.type = 'equipGem'
        self.bindType = 'equipGem'
        self.mediator = None
        self.pageType = 0
        self.srcPos = [-1, -1]
        self.gemPos = [-1, -1]
        self.item = None
        self.gem = None
        self.equipGems = {}
        self.slotMaxCount = 3
        self.yinSlotAvaliableIdx = -1
        self.yangSlotAvaliableIdx = -1
        self.isPutEquip = False
        self.avaliableGemSlot = -1
        self.addSlotPos = [-1, -1]
        uiAdapter.registerEscFunc(uiConst.WIDGET_EQUIP_GEM_ADD_REMOVE, self.onClose)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_EQUIP_GEM_ADD_REMOVE:
            self.mediator = mediator
        if gameglobal.rds.ui.inventory.mediator:
            gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def show(self, type):
        self.pageType = type
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_EQUIP_GEM_ADD_REMOVE)
        if self.mediator:
            self.mediator.Invoke('show', GfxValue(self.pageType))

    def _getKey(self, bar, slot):
        return 'equipGem%d.slot%d' % (bar, slot)

    def getSlotID(self, key):
        idBar, idItem = key.split('.')
        return (int(idBar[8:]), int(idItem[4:]))

    def onClose(self, *arg):
        self.hide()

    def onChangeTab(self, *arg):
        self.pageType = int(arg[3][0].GetNumber())
        self.reset()

    def onAddGem(self, *arg):
        if self.pageType == 0 and self.item and self.gem:
            equipIt = BigWorld.player().inv.getQuickVal(self.srcPos[0], self.srcPos[1])
            if equipIt == None:
                return
            if not equipIt.isForeverBind():
                text = GMD.data.get(GMDD.data.BIND_EQUIP_IF_ADD_GEM, {}).get('text', gameStrings.TEXT_EQUIPCHANGEINLAYPROXY_517)
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(text, Functor(self.confirmAddGem))
            else:
                self.confirmAddGem()

    def confirmAddGem(self):
        self.trueConfirmAddGem(self.srcPos[0], self.srcPos[1])

    @ui.checkEquipCanReturnByPos([1, 2], GMDD.data.RETURN_BACK_ADD_GEM)
    @ui.looseGroupTradeConfirm([1, 2], GMDD.data.RETURN_BACK_ADD_GEM)
    def trueConfirmAddGem(self, srcPage, srcPos):
        if self.srcPos[0] >= 0 and self.srcPos[1] >= 0 and self.avaliableGemSlot >= 0 and self.gemPos[0] >= 0 and self.gemPos[1] >= 0:
            BigWorld.player().cell.addEquipGem(const.RES_KIND_INV, srcPage, srcPos, self.avaliableGemSlot, self.gemPos[0], self.gemPos[1])

    def onRemoveGem(self, *arg):
        if self.pageType == 1:
            p = BigWorld.player()
            item = p.inv.getQuickVal(self.srcPos[0], self.srcPos[1])
            if item.hasLatch():
                p.showGameMsg(GMDD.data.EQUIP_REMOVE_GEM_AFTER_UNLOCK, ())
            else:
                gemType = int(arg[3][0].GetNumber())
                gemSlotIdx = int(arg[3][1].GetNumber())
                p.cell.removeEquipGem(const.RES_KIND_INV, self.srcPos[0], self.srcPos[1], gemType, gemSlotIdx)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EQUIP_GEM_ADD_REMOVE)
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def onChooseGemType(self, *arg):
        type = arg[3][0].GetNumber()
        self.gemType = int(type)

    def equipGem(self, gem, nPageSrc, nItemSrc):
        if self.gem:
            self.resetInventoryGemState()
        p = BigWorld.player()
        self.gem = gem
        gemId = self.gem.id
        gemType = utils.getEquipGemData(gemId).get('type', 1)
        self.avaliableGemSlot = self.getAvaliableGemSlot(gemType)
        if self.avaliableGemSlot == -1:
            p.showGameMsg(GMDD.data.EQUIP_GEM_NO_AVALIABLE_SLOT, ())
            if self.mediator:
                self.mediator.Invoke('removeNeedItem')
        elif self.item:
            if not self.item._canAddGem(p, self.avaliableGemSlot, self.gem):
                if self.mediator:
                    self.mediator.Invoke('removeNeedItem')
                return
            self.gemPos[0] = nPageSrc
            self.gemPos[1] = nItemSrc
            gameglobal.rds.ui.inventory.updateSlotState(self.gemPos[0], self.gemPos[1])
            self.showTip('')
            self.updateGem()

    def updateGem(self):
        gemId = self.gem.id
        gemInfo = uiUtils.getGfxItemById(gemId, appendInfo={'srcType': 'equipGem'})
        if self.mediator:
            self.mediator.Invoke('updateGem', uiUtils.dict2GfxDict(gemInfo, True))

    def resetInventoryItemState(self):
        removePage = self.srcPos[0]
        removePos = self.srcPos[1]
        self.srcPos = [-1, -1]
        gameglobal.rds.ui.inventory.updateSlotState(removePage, removePos)

    def resetInventoryGemState(self):
        removeGemPage = self.gemPos[0]
        removeGemPos = self.gemPos[1]
        self.gemPos = [-1, -1]
        gameglobal.rds.ui.inventory.updateSlotState(removeGemPage, removeGemPos)

    def equipItem(self, item, nPageSrc, nItemSrc):
        if self.item:
            self.resetInventoryItemState()
        if self.gem:
            self.resetInventoryGemState()
            self.gem = None
        self.item = item
        self.updateItem(nPageSrc, nItemSrc)

    def reset(self):
        self.item = None
        self.gem = None
        self.slotMaxCount = 3
        self.yinSlotAvaliableIdx = -1
        self.yangSlotAvaliableIdx = -1
        self.isPutEquip = False
        self.avaliableGemSlot = -1
        self.equipGems['yinSlots'] = []
        self.equipGems['yangSlots'] = []
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def resSetPanel(self, item, page, pos):
        if self.pageType == 0:
            self.showTip(GMD.data.get(GMDD.data.ADD_GEM_SUCCEESS, {}).get('text', gameStrings.TEXT_EQUIPGEMPROXY_189))
        else:
            self.showTip(GMD.data.get(GMDD.data.REMOVE_GEM_SUCCEESS, {}).get('text', gameStrings.TEXT_EQUIPGEMPROXY_191))
        if self.pageType == 0 and self.addSlotPos[0] != -1 and self.addSlotPos[1] != -1:
            if self.mediator:
                self.mediator.Invoke('shineSlot', (GfxValue(self.addSlotPos[0]), GfxValue(self.addSlotPos[1])))
        self.yinSlotAvaliableIdx = -1
        self.yangSlotAvaliableIdx = -1
        self.avaliableGemSlot = -1
        if item:
            self.item = item
            itemId = self.item.id
            itemInfo = uiUtils.getGfxItemById(itemId, appendInfo={'srcType': 'equipGem'})
            self.updateEquipSlot(itemInfo)
            self.getAllSlots(self.item, True, False)
            if self.pageType == 0:
                self.isPutEquip = True
            if self.pageType == 0:
                if self.mediator:
                    self.mediator.Invoke('removeNeedItem')
            self.resetInventoryGemState()

    def matchCondition(self, item):
        if item:
            if not hasattr(item, 'yangSlots'):
                if item.type == Item.BASETYPE_EQUIP:
                    if self.pageType == 0:
                        BigWorld.player().showGameMsg(GMDD.data.EQUIP_GEM_CANNOT_ADD_GEM, ())
                    elif self.pageType == 1:
                        BigWorld.player().showGameMsg(GMDD.data.EQUIP_GEM_CANNOT_REMOVE_GEM, ())
                return False
            if not self.getAllSlots(item):
                return False
        return True

    def updateItem(self, nPageSrc, nItemSrc):
        p = BigWorld.player()
        self.clearPanel()
        if self.item:
            if not hasattr(self.item, 'yangSlots'):
                if self.pageType == 0:
                    p.showGameMsg(GMDD.data.EQUIP_GEM_CANNOT_ADD_GEM, ())
                elif self.pageType == 1:
                    p.showGameMsg(GMDD.data.EQUIP_GEM_CANNOT_REMOVE_GEM, ())
                return
            if not self.getAllSlots(self.item):
                return
            itemId = self.item.id
            self.srcPos[0] = nPageSrc
            self.srcPos[1] = nItemSrc
            itemInfo = uiUtils.getGfxItemById(itemId, appendInfo={'srcType': 'equipGem'})
            self.updateEquipSlot(itemInfo)
            if self.pageType == 0:
                self.isPutEquip = True
            gameglobal.rds.ui.inventory.updateSlotState(self.srcPos[0], self.srcPos[1])
            if self.pageType == 0:
                self.showTip(GMD.data.get(GMDD.data.PUT_YINGYANG_GEM, {}).get('text', gameStrings.TEXT_EQUIPGEMPROXY_252))
            else:
                self.showTip(GMD.data.get(GMDD.data.CHOOSE_GEM_TO_REMOVE, {}).get('text', gameStrings.TEXT_EQUIPGEMPROXY_254))

    def updateCost(self, gemId):
        cash = 0
        p = BigWorld.player()
        gemUnlockSlotData = utils.getEquipGemData(gemId)
        itemId = gemUnlockSlotData.get('removeItemId', 240000)
        itemNum = gemUnlockSlotData.get('removeItemNum', 0)
        costInfo = {}
        costInfo['cash'] = cash
        costInfo['playerCash'] = p.cash
        ownCount = p.inv.countItemInPages(int(itemId), enableParentCheck=True)
        costInfo['hasItem'] = ownCount
        costInfo['needItem'] = itemNum
        costInfo['item'] = uiUtils.getGfxItemById(itemId, uiUtils.convertNumStr(ownCount, itemNum))
        self.setCost(costInfo)

    def clearPanel(self):
        self.isPutEquip = False
        if self.mediator:
            self.mediator.Invoke('clearPanel')

    def updateEquipSlot(self, info):
        if self.mediator:
            self.mediator.Invoke('updateEquipSlot', uiUtils.dict2GfxDict(info, True))

    def updateGemSlots(self, info):
        if self.mediator and info != None:
            self.mediator.Invoke('updateGemSlots', uiUtils.dict2GfxDict(info, True))

    def getAvaliableGemSlot(self, type):
        slotIdx = -1
        if type == uiConst.GEM_TYPE_YIN and self.yinSlotAvaliableIdx != -1:
            slotIdx = self.yinSlotAvaliableIdx
        elif type == uiConst.GEM_TYPE_YANG and self.yangSlotAvaliableIdx != -1:
            slotIdx = self.yangSlotAvaliableIdx
        self.addSlotPos[0] = type
        self.addSlotPos[1] = slotIdx
        return slotIdx

    def getAllSlots(self, item, showItem = False, showTip = True):
        isAvaliable = True
        slotsInfo = {}
        self.equipGems['yinSlots'] = []
        self.equipGems['yangSlots'] = []
        slotsInfo['yinSlots'] = []
        slotsInfo['yangSlots'] = []
        hasEmptyYinSlot = False
        hasEmptyYangSlot = False
        hasGem = False
        if item:
            for i in range(self.slotMaxCount):
                yinSlot = {}
                yinSlotData = item.getEquipGemSlot(uiConst.GEM_TYPE_YIN, i)
                if yinSlotData != None:
                    self.equipGems['yinSlots'].append(yinSlotData.gem)
                    if yinSlotData.gem != None:
                        yinSlot['gem'] = uiUtils.getGfxItemById(yinSlotData.gem.id, appendInfo={'srcType': 'equipGem'})
                    yinSlot['state'] = yinSlotData.state
                    slotsInfo['yinSlots'].append(yinSlot)
                    if yinSlotData.state == uiConst.GEM_SLOT_EMPTY and not hasEmptyYinSlot:
                        self.yinSlotAvaliableIdx = i
                        hasEmptyYinSlot = True
                    if yinSlotData.state == uiConst.GEM_SLOT_FILLED:
                        hasGem = True

            for i in range(self.slotMaxCount):
                yangSlot = {}
                yangSlotData = item.getEquipGemSlot(uiConst.GEM_TYPE_YANG, i)
                if yangSlotData != None:
                    self.equipGems['yangSlots'].append(yangSlotData.gem)
                    if yangSlotData.gem != None:
                        yangSlot['gem'] = uiUtils.getGfxItemById(yangSlotData.gem.id, appendInfo={'srcType': 'equipGem'})
                    yangSlot['state'] = yangSlotData.state
                    slotsInfo['yangSlots'].append(yangSlot)
                    if yangSlotData.state == uiConst.GEM_SLOT_EMPTY and not hasEmptyYangSlot:
                        self.yangSlotAvaliableIdx = i
                        hasEmptyYangSlot = True
                    if yangSlotData.state == uiConst.GEM_SLOT_FILLED:
                        hasGem = True

        p = BigWorld.player()
        if self.pageType == 0 and not (hasEmptyYangSlot or hasEmptyYinSlot):
            if showTip:
                p.showGameMsg(GMDD.data.EQUIP_GEM_NO_EMPTY_SLOT_ADD, ())
            isAvaliable = False
            if not showItem:
                return isAvaliable
        if self.pageType == 1 and not hasGem:
            if showTip:
                p.showGameMsg(GMDD.data.EQUIP_GEM_NO_EMPTY_SLOT_REMOVE, ())
            isAvaliable = False
            if not showItem:
                return isAvaliable
        self.updateGemSlots(slotsInfo)
        return isAvaliable

    def setCost(self, info):
        if self.mediator:
            self.mediator.Invoke('setCost', uiUtils.dict2GfxDict(info, True))

    def showTip(self, warningType):
        if self.mediator:
            self.mediator.Invoke('showTip', GfxValue(gbk2unicode(warningType)))

    def onRemoveItemToBag(self, *arg):
        type = int(arg[3][0].GetNumber())
        self.returnItemToBag(type)

    def returnItemToBag(self, type):
        if type == 0:
            self.reset()
            self.clearPanel()
        elif type == 1 and self.pageType == 0:
            self.resetInventoryGemState()
            self.gem = None
            if self.mediator:
                self.mediator.Invoke('removeNeedItem')

    def onSelectGem(self, *arg):
        self.gemType = int(arg[3][0].GetNumber())
        gemId = int(arg[3][2].GetNumber())
        self.updateCost(gemId)

    def onClickLockedSlot(self, *arg):
        BigWorld.player().showGameMsg(GMDD.data.GO_FOR_GEM_UNLOCK_NPC, ())
        if self.mediator:
            self.mediator.Invoke('removeNeedItem')

    def isItemDisabled(self, kind, page, pos, item):
        if self.mediator:
            if self.item == None:
                if self.pageType == 0 and not (item.type == Item.BASETYPE_EQUIP or item.type == Item.BASETYPE_EQUIP_GEM):
                    return True
                if self.pageType == 1 and not item.type == Item.BASETYPE_EQUIP:
                    return True
            else:
                if not (item.type == Item.BASETYPE_EQUIP or item.type == Item.BASETYPE_EQUIP_GEM):
                    return True
                if item.type == Item.BASETYPE_EQUIP:
                    if page == self.srcPos[0] and pos == self.srcPos[1]:
                        return True
                    else:
                        return False
                elif item.type == Item.BASETYPE_EQUIP_GEM:
                    if self.pageType == 0 and self.gem and page == self.gemPos[0] and pos == self.gemPos[1]:
                        return True
                    if self.pageType == 1:
                        return True
        return False

    def onGetToolTip(self, key):
        page, pos = self.getSlotID(key)
        if page == 0 and self.item:
            return gameglobal.rds.ui.inventory.GfxToolTip(self.item)
        else:
            if page == uiConst.GEM_TYPE_YANG and pos < len(self.equipGems['yangSlots']):
                gem = self.equipGems['yangSlots'][pos]
                if gem != None:
                    return gameglobal.rds.ui.inventory.GfxToolTip(gem)
            elif page == uiConst.GEM_TYPE_YIN and pos < len(self.equipGems['yinSlots']):
                gem = self.equipGems['yinSlots'][pos]
                if gem != None:
                    return gameglobal.rds.ui.inventory.GfxToolTip(gem)
            elif page == 4 and self.gem:
                return gameglobal.rds.ui.inventory.GfxToolTip(self.gem)
            return

    @ui.uiEvent(uiConst.WIDGET_EQUIP_GEM_ADD_REMOVE, events.EVENT_INVENTORY_ITEM_CLICKED)
    def onEquipGemItemClick(self, event):
        event.stop()
        it = event.data['item']
        nPage = event.data['page']
        nItem = event.data['pos']
        if it == None:
            return
        else:
            p = BigWorld.player()
            if self.pageType == 1:
                if it.type == Item.BASETYPE_EQUIP:
                    if self.matchCondition(it):
                        self.equipItem(it, nPage, nItem)
                elif self.item == None:
                    p.showGameMsg(GMDD.data.EQUIP_GEM_WRONG_TYPE_EQUIP, ())
            elif self.pageType == 0:
                if self.isPutEquip:
                    if it.type == Item.BASETYPE_EQUIP_GEM:
                        if it.hasLatch():
                            p.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
                        else:
                            self.equipGem(it, nPage, nItem)
                    elif it.type == Item.BASETYPE_EQUIP:
                        if self.matchCondition(it):
                            self.equipItem(it, nPage, nItem)
                    elif not self.gem:
                        p.showGameMsg(GMDD.data.EQUIP_GEM_WRONG_TYPE_GEM, ())
                elif it.type == Item.BASETYPE_EQUIP:
                    if self.matchCondition(it):
                        self.equipItem(it, nPage, nItem)
                else:
                    p.showGameMsg(GMDD.data.EQUIP_GEM_WRONG_TYPE_EQUIP, ())
            return
