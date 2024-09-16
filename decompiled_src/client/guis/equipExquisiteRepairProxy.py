#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/equipExquisiteRepairProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import const
from item import Item
from guis import uiUtils
from uiProxy import SlotDataProxy
from cdata import game_msg_def_data as GMDD

class EquipExquisiteRepairProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(EquipExquisiteRepairProxy, self).__init__(uiAdapter)
        self.binding = {}
        self.bindType = 'exquisiteEquip'
        self.type = 'exquisiteEquip'
        self.modelMap = {'clickClose': self.onClickClose,
         'clickConfirm': self.onClickConfirm,
         'clearSlot': self.onClearSlot}
        self.mediator = None
        self.equipPage = -1
        self.equipPos = -1
        self.equipItem = None
        self.itemCost = None
        self.npc = None
        self.cashCost = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_EQUIP_EXQUISITE_REPAIR, self.clearWidget)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_EQUIP_EXQUISITE_REPAIR:
            self.mediator = mediator
            if gameglobal.rds.ui.inventory.mediator:
                gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def show(self, npc, shopId):
        BigWorld.player().openShopId = shopId
        BigWorld.player().openShopType = const.SHOP_TYPE_COMMON
        self.npc = npc
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_EQUIP_EXQUISITE_REPAIR)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        self.equipPage = -1
        self.equipPos = -1
        self.equipItem = None
        self.itemCost = None
        self.npc = None
        self.cashCost = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EQUIP_EXQUISITE_REPAIR)

    def reset(self):
        super(self.__class__, self).reset()
        self.message = ''
        self.nPage = const.CONT_NO_PAGE
        self.nItem = const.CONT_NO_POS

    def onClickConfirm(self, *arg):
        p = BigWorld.player()
        if p.bindCash >= self.cashCost:
            self._doRepair()
        elif p.cash >= self.cashCost:
            gameglobal.rds.ui.moneyConvertConfirm.show(self._doRepair)
        else:
            return

    def _doRepair(self):
        pass

    def onClickClose(self, *arg):
        self.hide()

    def setExquisiteEquip(self, page, pos, item):
        pass

    def getKey(self, index):
        return 'exquisiteEquip%d' % index

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        if key == 'exquisiteEquip0':
            ret = gameglobal.rds.ui.inventory.GfxToolTip(self.equipItem)
        elif key == 'exquisiteEquip1':
            ret = gameglobal.rds.ui.inventory.GfxToolTip(Item(self.itemCost[0]))
        return ret

    def onClearSlot(self, *arg):
        self.clearSlot()

    def clearSlot(self):
        self.equipPage = -1
        self.equipPos = -1
        for i in xrange(2):
            key = self.getKey(i)
            data = GfxValue(1)
            data.SetNull()
            self.binding[key][0].Invoke('setSlotState', GfxValue(uiConst.ITEM_NORMAL))
            self.binding[key][0].Invoke('setSlotColor', GfxValue('nothing'))
            self.binding[key][1].InvokeSelf(data)

        if self.mediator:
            self.mediator.Invoke('clear')

    def getSlotID(self, key):
        return (0, int(key[14:]))

    def succeed(self):
        self.clearSlot()
        if self.mediator:
            self.mediator.Invoke('repairSucceed')

    def isItemDisabled(self, kind, page, pos, item):
        if self.mediator and kind == const.RES_KIND_INV:
            return True
        return False
