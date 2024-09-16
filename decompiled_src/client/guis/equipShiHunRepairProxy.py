#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/equipShiHunRepairProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import const
import utils
from ui import gbk2unicode
from uiProxy import SlotDataProxy
from item import Item
from guis import uiConst
from guis import uiUtils
from data import item_data as ID
from cdata import game_msg_def_data as GMDD
from data import game_msg_data as GMD

class EquipShiHunRepairProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(EquipShiHunRepairProxy, self).__init__(uiAdapter)
        self.binding = {}
        self.bindType = 'shiHunRepair'
        self.type = 'shiHunRepair'
        self.modelMap = {'backItem': self.onBackItem,
         'repairItem': self.onRepairItem,
         'setText': self.onSetText}
        self.mediator = None
        self.equipPage = None
        self.equipPos = None
        self.equipItem = None
        self.costItemLen = None
        self.costItemList = []
        self.npcEntId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_EQUIP_SHI_HUN_REPAIR, self.hide)

    def show(self, npcEntId = 0):
        enableShiHunRepair = gameglobal.rds.configData.get('enableShiHunRepair', False)
        self.npcEntId = npcEntId
        if enableShiHunRepair and not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_EQUIP_SHI_HUN_REPAIR)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_EQUIP_SHI_HUN_REPAIR:
            self.mediator = mediator

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        if self.mediator:
            self.mediator = None
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EQUIP_SHI_HUN_REPAIR)
            if gameglobal.rds.ui.funcNpc.isOnFuncState():
                gameglobal.rds.ui.funcNpc.close()

    def reset(self):
        super(self.__class__, self).reset()
        self.mediator = None
        self.equipPage = None
        self.equipPos = None
        self.equipItem = None
        self.costItemLen = None
        self.costItemList = []
        self.npcEntId = 0
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def setShiHunEquip(self, page, pos, item):
        if self.equipPage != None and self.equipPos != None:
            gameglobal.rds.ui.inventory.updateSlotState(self.equipPage, self.equipPos)
        if not hasattr(item, 'shihun') or getattr(item, 'shihun') == False:
            BigWorld.player().showGameMsg(GMDD.data.ITEM_NOT_SHIHUN, (item.name,))
            return
        if item == const.CONT_EMPTY_VAL:
            return
        key = self.getKey(0)
        self.equipPage = page
        self.equipPos = pos
        self.equipItem = Item(item.id)
        data = {}
        data['iconPath'] = uiUtils.getItemIconFile64(item.id)
        self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(data))
        color = uiUtils.getItemColor(item.id)
        self.binding[key][0].Invoke('setSlotColor', GfxValue(color))
        self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.EQUIP_SHIHUN_REPAIR))
        gameglobal.rds.ui.inventory.updateSlotState(page, pos)
        self.equipItem = item
        self.costItemList = utils.findItemCost(item)
        self.costItemLen = len(self.costItemList)
        if self.mediator:
            self.mediator.Invoke('setCostItemNum', GfxValue(self.costItemLen))
            self.mediator.Invoke('setCostItem', uiUtils.array2GfxAarry(self._getItemData(self.costItemList)))

    def onSetText(self, *arg):
        content = GMD.data[GMDD.data.SHIHUN_TEXT].get('text', '≤ﬂªÆ≈‰±Ì')
        return GfxValue(gbk2unicode(content))

    def _getItemData(self, costItemList):
        if len(costItemList) <= 0:
            return
        p = BigWorld.player()
        costItemData = []
        num = 0
        for costItem in costItemList:
            ret = {}
            itemId = costItem[0]
            itemNum = costItem[1]
            ret['itemId'] = itemId
            ret['iconPath'] = uiUtils.getIcon(uiConst.ICON_TYPE_ITEM, ID.data.get(itemId, {}).get('icon'))
            num = p.inv.countItemInPages(uiUtils.getParentId(itemId), enableParentCheck=True)
            if num > itemNum:
                num = itemNum
            ret['num'] = '%d/%d' % (num, itemNum)
            ret['color'] = uiUtils.getItemColor(itemId)
            ret['srcType'] = 'equipShiHunRepair'
            costItemData.append(ret)

        return costItemData

    def getKey(self, index):
        return 'shiHunRepair%d' % index

    def onBackItem(self, *arg):
        if self.hasEquiped() and self.mediator:
            self.clearShiHunEquipSlot()

    def onRepairItem(self, *arg):
        if self.hasEquiped():
            if self.npcEntId:
                npc = BigWorld.entity(self.npcEntId)
                if npc and npc.inWorld:
                    npc.cell.repairShihunItem(self.equipPage, self.equipPos)
                    if self.mediator:
                        self.clearShiHunEquipSlot()

    def clearShiHunEquipSlot(self):
        key = self.getKey(0)
        gameglobal.rds.ui.inventory.updateSlotState(self.equipPage, self.equipPos)
        self.equipPage = None
        self.equipPos = None
        self.equipItem = None
        data = GfxValue(1)
        data.SetNull()
        self.binding[key][1].InvokeSelf(data)
        self.binding[key][0].Invoke('setSlotColor', GfxValue('nothing'))
        self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.ITEM_NORMAL))
        if self.mediator:
            self.mediator.Invoke('setCostItemNum', GfxValue(1))

    def hasEquiped(self):
        return self.equipItem != None

    def getRepairItem(self, itemId):
        if not self.equipItem:
            return Item(itemId)
        item = BigWorld.player().inv.findItemByUUID(self.equipItem.shihunItemUUID)[0]
        if not item:
            return Item(itemId)
        return item

    def onGetToolTip(self, *arg):
        i = BigWorld.player().inv.getQuickVal(self.equipPage, self.equipPos)
        if i == None:
            return
        return gameglobal.rds.ui.inventory.GfxToolTip(i)

    def isItemDisabled(self, kind, page, pos, item):
        if self.mediator and kind == const.RES_KIND_INV:
            if hasattr(item, 'shihun') and item.shihun == True:
                return False
            return True
        return False
