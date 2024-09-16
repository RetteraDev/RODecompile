#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/equipmentSlotProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import commcalc
import gamelog
import utils
import const
from guis import ui
from guis import uiConst
from guis import uiUtils
from ui import gbk2unicode
from uiProxy import SlotDataProxy
from item import Item
from guis import events
from data import equip_data as ED
from cdata import equip_gem_unlock_slot_data as EGUSD
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD

class EquipmentSlotProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(EquipmentSlotProxy, self).__init__(uiAdapter)
        self.modelMap = {'closeWidget': self.onClose,
         'unlockEquipGemSlot': self.onUnlockEquipGemSlot,
         'chooseGemType': self.onChooseGemType,
         'returnItemToBag': self.onRemoveItemToBag,
         'clickYunchuiBtn': self.onClickYunchuiBtn}
        self.type = 'gemUnclok'
        self.bindType = 'gemUnclok'
        self.mediator = None
        self.npcId = 0
        self.slotMaxCount = 3
        self.item = None
        self.yinSlotAvaliableIdx = -1
        self.yangSlotAvaliableIdx = -1
        self.srcPos = [-1, -1]
        self.desPos = []
        self.gemType = 1
        self.gemPos = -1
        uiAdapter.registerEscFunc(uiConst.WIDGET_EQUIPMENT_SLOT, self.onClose)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_EQUIPMENT_SLOT:
            self.mediator = mediator

    def show(self, npcId):
        self.npcId = npcId
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_EQUIPMENT_SLOT)

    def onClose(self, *arg):
        gameglobal.rds.ui.funcNpc.close()
        self.hide()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EQUIPMENT_SLOT)
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def onRemoveItemToBag(self, *arg):
        self.reset()
        self.clearPanel()

    def reset(self):
        self.item = None
        removePage = self.srcPos[0]
        removePos = self.srcPos[1]
        self.srcPos = [-1, -1]
        gameglobal.rds.ui.inventory.updateSlotState(removePage, removePos)

    def onUnlockEquipGemSlot(self, *arg):
        self.onTrueUnlockEquipGemSlot(self.srcPos[0], self.srcPos[1])

    @ui.checkEquipCanReturnByPos([1, 2], GMDD.data.RETURN_BACK_UNLOCK_EQUIP_GEM)
    @ui.looseGroupTradeConfirm([1, 2], GMDD.data.RETURN_BACK_UNLOCK_EQUIP_GEM)
    def onTrueUnlockEquipGemSlot(self, page, pos):
        ent = BigWorld.entities.get(self.npcId)
        if not ent:
            return
        self.gemPos = self.getAvaliableGemSlot(self.gemType)
        if self.gemPos == -1:
            BigWorld.player().showGameMsg(GMDD.data.EQUIP_GEM_SLOT_CANNOT_UNLOCK, ())
            return
        p = BigWorld.player()
        equipIt = p.inv.getQuickVal(self.srcPos[0], self.srcPos[1])
        ed = ED.data.get(equipIt.id, {})
        order = ed.get('order')
        unlockData = EGUSD.data.get((equipIt.quality, order, self.gemType))
        if not unlockData:
            gamelog.error('cannot get unlock data', equipIt.id, equipIt.quality, order, self.gemType)
            return
        if not equipIt.isForeverBind():
            costItemId, costItemNumFormula = unlockData.get('itemId'), unlockData.get('itemNum')
            needBind = False
            if costItemId and costItemNumFormula:
                costRatio = ed.get('yangCostRatio', 1) if self.gemType == Item.GEM_TYPE_YANG else ed.get('yinCostRatio', 1)
                yangSlotsCnt = sum([ 1 for slot in getattr(equipIt, 'yangSlots', ()) if not slot.isLocked() ])
                yinSlotsCnt = sum([ 1 for slot in getattr(equipIt, 'yinSlots', ()) if not slot.isLocked() ])
                fvars = {'itemLv': equipIt.itemLv,
                 'quality': equipIt.quality,
                 'p1': costItemNumFormula[1],
                 'yangSlotsCnt': yangSlotsCnt,
                 'yinSlotsCnt': yinSlotsCnt}
                costItemNum = int(round(commcalc._calcFormulaById(costItemNumFormula[0], fvars) * costRatio))
                if costItemNum:
                    removePlans = p.inv.canRemoveItemWithPlans(costItemId, costItemNum, enableParentCheck=True)
                    if removePlans:
                        needBind = any([ p.inv.getQuickVal(pg, pos).isForeverBind() for pg, pos, _ in removePlans ])
            if gameglobal.rds.configData.get('enableEquipDiKou', False):
                itemDict = {costItemId: costItemNum}
                _, yunchuiNeed, _, _ = utils.calcEquipMaterialDiKou(p, itemDict)
                if yunchuiNeed > 0:
                    msg = uiUtils.getTextFromGMD(GMDD.data.ENHANCE_BIND_CONFIRM)
                    gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=lambda : ent.cell.unlockEquipSlot(const.RES_KIND_INV, self.srcPos[0], self.srcPos[1], self.gemType, self.gemPos))
                    return
            if needBind:
                msg = GMD.data.get(GMDD.data.BIND_EQUIP_IF_UNLOCK, {}).get('text', gameStrings.TEXT_EQUIPCHANGEINLAYPROXY_1063)
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=lambda : ent.cell.unlockEquipSlot(const.RES_KIND_INV, self.srcPos[0], self.srcPos[1], self.gemType, self.gemPos))
                return
        ent.cell.unlockEquipSlot(const.RES_KIND_INV, self.srcPos[0], self.srcPos[1], self.gemType, self.gemPos)

    def getSlotID(self, key):
        idBar, idItem = key.split('.')
        return (int(idBar[9:]), int(idItem[4:]))

    def onChooseGemType(self, *arg):
        type = arg[3][0].GetNumber()
        self.gemType = int(type)
        if self.item:
            self.updateCost(self.item.id, self.item.quality)

    def equipItem(self, item, nPageSrc, nItemSrc):
        self.item = item
        gameglobal.rds.ui.inventory.updateSlotState(nPageSrc, nItemSrc)
        self.updateItem(nPageSrc, nItemSrc)

    def resSetPanel(self, item, nPageSrc, nItemSrc):
        self.showTip(gameStrings.TEXT_EQUIPMENTSLOTPROXY_146)
        self.item = item
        gameglobal.rds.ui.inventory.updateSlotState(nPageSrc, nItemSrc)
        self.updateItem(nPageSrc, nItemSrc)

    def resetInventoryItemState(self):
        removePage = self.srcPos[0]
        removePos = self.srcPos[1]
        self.srcPos = [-1, -1]
        gameglobal.rds.ui.inventory.updateSlotState(removePage, removePos)

    def matchCondition(self, item):
        if item:
            if not hasattr(item, 'yangSlots'):
                BigWorld.player().showGameMsg(GMDD.data.EQUIP_CANNOT_UNLOCK_SLOT, ())
                return False
            if not item.checkLockedSlot():
                BigWorld.player().showGameMsg(GMDD.data.EQUIP_CANNOT_UNLOCK, ())
                return False
        return True

    def updateItem(self, nPageSrc, nItemSrc):
        p = BigWorld.player()
        self.clearPanel()
        if self.item:
            if not hasattr(self.item, 'yangSlots'):
                p.showGameMsg(GMDD.data.EQUIP_CANNOT_UNLOCK_SLOT, ())
                return
            if not self.getAllSlots(self.item):
                self.item = None
                if self.mediator:
                    self.mediator.Invoke('removeNeedItem')
                if self.srcPos[0] != -1:
                    self.resetInventoryItemState()
                self.showTip(gameStrings.TEXT_EQUIPMENTSLOTPROXY_182)
                return
            itemId = self.item.id
            itemQuality = self.item.quality
            self.srcPos[0] = nPageSrc
            self.srcPos[1] = nItemSrc
            self.updateCost(itemId, itemQuality)
            itemInfo = uiUtils.getGfxItemById(itemId)
            self.showTip(GMD.data.get(GMDD.data.CHOOSE_GEM_TYPE_TO_EXPAND_SLOT, {}).get('text', gameStrings.TEXT_EQUIPMENTSLOTPROXY_192))
            self.updateEquipSlot(itemInfo)

    def updateCost(self, itemId, itemQuality):
        itemNum = 0
        cash = 0
        p = BigWorld.player()
        ed = ED.data.get(itemId, {})
        itemOrder = ed.get('order', 0)
        gemUnlockSlotData = EGUSD.data.get((itemQuality, itemOrder, self.gemType), {})
        itemNumCalc = gemUnlockSlotData.get('itemNum', [])
        cashCalc = gemUnlockSlotData.get('cash', [])
        if len(itemNumCalc) >= 2:
            if self.item:
                costRatio = ed.get('yangCostRatio', 1) if self.gemType == Item.GEM_TYPE_YANG else ed.get('yinCostRatio', 1)
                yangSlotsCnt = sum([ 1 for slot in getattr(self.item, 'yangSlots', ()) if not slot.isLocked() ])
                yinSlotsCnt = sum([ 1 for slot in getattr(self.item, 'yinSlots', ()) if not slot.isLocked() ])
                fvars = {'itemLv': self.item.itemLv,
                 'quality': itemQuality,
                 'p1': itemNumCalc[1],
                 'yangSlotsCnt': yangSlotsCnt,
                 'yinSlotsCnt': yinSlotsCnt}
                itemNum = int(round(commcalc._calcFormulaById(itemNumCalc[0], fvars) * costRatio))
        if len(cashCalc) > 2:
            cash = commcalc._calcFormulaById(cashCalc[0], cashCalc[1])
        costItemId = gemUnlockSlotData.get('itemId', 0)
        costInfo = {}
        costInfo['cash'] = cash
        costInfo['playerCash'] = p.cash
        costInfo['item'] = uiUtils.getGfxItemById(costItemId, 1, uiConst.ICON_SIZE64)
        ownNum = p.inv.countItemInPages(int(costItemId), enableParentCheck=True)
        if itemNum > ownNum:
            costInfo['itemCount'] = '%s/%s' % (uiUtils.toHtml(str(ownNum), '#FB0000'), str(itemNum))
        else:
            costInfo['itemCount'] = '%s/%s' % (str(ownNum), str(itemNum))
        costInfo['enableEquipDiKou'] = gameglobal.rds.configData.get('enableEquipDiKou', False)
        isEnough = True
        if costInfo['enableEquipDiKou']:
            itemDict = {costItemId: itemNum}
            self.appendDiKouInfo(costInfo, itemDict)
            if not uiUtils.checkEquipMaterialDiKou(itemDict):
                isEnough = False
        elif itemNum > ownNum:
            isEnough = False
        costInfo['isEnough'] = isEnough
        costInfo['itemNum'] = itemNum
        costInfo['ownNum'] = ownNum
        self.setCost(costInfo)

    def appendDiKouInfo(self, ret, itemDict):
        if itemDict != {}:
            p = BigWorld.player()
            _, yunchuiNeed, _, _ = utils.calcEquipMaterialDiKou(p, itemDict)
            yunchuiOwn = p.getFame(const.YUN_CHUI_JI_FEN_FAME_ID)
            if yunchuiNeed > yunchuiOwn:
                ret['yunchui'] = '%s/%s' % (uiUtils.toHtml(format(yunchuiOwn, ','), '#FB0000'), format(yunchuiNeed, ','))
                ret['yunchuiEnabled'] = True
            else:
                ret['yunchui'] = '%s/%s' % (format(yunchuiOwn, ','), format(yunchuiNeed, ','))
                ret['yunchuiEnabled'] = False
            ret['diKouVisible'] = True
        else:
            ret['diKouVisible'] = False

    def clearPanel(self):
        self.gemSlotInfo = {}
        if self.mediator:
            self.mediator.Invoke('clearPanel')

    def updateEquipSlot(self, info):
        if self.mediator:
            self.mediator.Invoke('updateEquipSlot', uiUtils.dict2GfxDict(info, True))

    def updateGemSlots(self, info):
        if self.mediator:
            self.mediator.Invoke('updateGemSlots', uiUtils.dict2GfxDict(info, True))

    def getAvaliableGemSlot(self, type):
        slotIdx = -1
        if type == uiConst.GEM_TYPE_YIN and self.yinSlotAvaliableIdx != -1:
            slotIdx = self.yinSlotAvaliableIdx
        elif type == uiConst.GEM_TYPE_YANG and self.yangSlotAvaliableIdx != -1:
            slotIdx = self.yangSlotAvaliableIdx
        return slotIdx

    def getAllSlots(self, item):
        slotsInfo = {}
        slotsInfo['yinSlots'] = []
        slotsInfo['yangSlots'] = []
        slotsInfo['slotState'] = 0
        hasLockedYinSlot = False
        hasLockedYangSlot = False
        self.yinSlotAvaliableIdx = -1
        self.yangSlotAvaliableIdx = -1
        if item:
            for i in range(self.slotMaxCount):
                yinSlot = {}
                yinSlotData = item.getEquipGemSlot(uiConst.GEM_TYPE_YIN, i)
                if yinSlotData != None:
                    if yinSlotData.gem:
                        yinSlot['gem'] = uiUtils.getGfxItemById(yinSlotData.gem.id)
                    yinSlot['state'] = yinSlotData.state
                    slotsInfo['yinSlots'].append(yinSlot)
                    if yinSlotData.state == uiConst.GEM_SLOT_LOCKED and hasLockedYinSlot == False:
                        self.yinSlotAvaliableIdx = i
                        self.updateSelectType(uiConst.GEM_TYPE_YIN)
                        hasLockedYinSlot = True
                        slotsInfo['slotState'] = 2

            for i in range(self.slotMaxCount):
                yangSlot = {}
                yangSlotData = item.getEquipGemSlot(uiConst.GEM_TYPE_YANG, i)
                if yangSlotData != None:
                    if yangSlotData.gem:
                        yangSlot['gem'] = uiUtils.getGfxItemById(yangSlotData.gem.id)
                    yangSlot['state'] = yangSlotData.state
                    slotsInfo['yangSlots'].append(yangSlot)
                    if yangSlotData.state == uiConst.GEM_SLOT_LOCKED and hasLockedYangSlot == False:
                        self.yangSlotAvaliableIdx = i
                        if not hasLockedYinSlot:
                            self.updateSelectType(uiConst.GEM_TYPE_YANG)
                        hasLockedYangSlot = True
                        if hasLockedYinSlot:
                            slotsInfo['slotState'] = 3
                        else:
                            slotsInfo['slotState'] = 1

        self.gemSlotInfo = slotsInfo
        if hasLockedYangSlot or hasLockedYinSlot:
            self.updateGemSlots(slotsInfo)
            return True
        else:
            BigWorld.player().showGameMsg(GMDD.data.EQUIP_CANNOT_UNLOCK, ())
            self.updateSelectType(-1)
            return False

    def setCost(self, info):
        if self.mediator:
            self.mediator.Invoke('setCost', uiUtils.dict2GfxDict(info, True))

    def showTip(self, warningType):
        if self.mediator:
            self.mediator.Invoke('showTip', GfxValue(gbk2unicode(warningType)))

    def updateSelectType(self, type):
        if self.mediator:
            self.mediator.Invoke('updateSelectType', GfxValue(type))

    def isItemDisabled(self, kind, page, pos, item):
        if self.mediator:
            if self.item == None and not item.type == Item.BASETYPE_EQUIP:
                return True
            if item.type == Item.BASETYPE_EQUIP:
                if page == self.srcPos[0] and pos == self.srcPos[1]:
                    return True
            else:
                return True
        return False

    def checkLockedSlot(self, item):
        if item:
            for i in range(self.slotMaxCount):
                yinSlotData = item.getEquipGemSlot(uiConst.GEM_TYPE_YIN, i)
                if yinSlotData != None and yinSlotData.state == uiConst.GEM_SLOT_LOCKED:
                    return True

            for i in range(self.slotMaxCount):
                yangSlotData = item.getEquipGemSlot(uiConst.GEM_TYPE_YANG, i)
                if yangSlotData != None and yangSlotData.state == uiConst.GEM_SLOT_LOCKED:
                    return True

        return False

    @ui.uiEvent(uiConst.WIDGET_EQUIPMENT_SLOT, events.EVENT_INVENTORY_ITEM_CLICKED)
    def onEquipSlotItemClick(self, event):
        event.stop()
        i = event.data['item']
        nPage = event.data['page']
        nItem = event.data['pos']
        if i == None:
            return
        else:
            p = BigWorld.player()
            if i.type == Item.BASETYPE_EQUIP:
                if self.matchCondition(i):
                    self.equipItem(i, nPage, nItem)
            else:
                p.showGameMsg(GMDD.data.EQUIP_GEM_WRONG_TYPE_EQUIP, ())
            return

    def onClickYunchuiBtn(self, *arg):
        mall = gameglobal.rds.ui.tianyuMall
        if mall.mallMediator:
            mall.hide()
        mall.show(keyWord=gameStrings.TEXT_INVENTORYPROXY_3299)
