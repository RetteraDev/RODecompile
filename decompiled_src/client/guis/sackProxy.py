#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/sackProxy.o
import BigWorld
import gameglobal
import const
from uiProxy import SlotDataProxy

class SackProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(SackProxy, self).__init__(uiAdapter)
        self.binding = {}
        self.bindType = 'sack'
        self.type = 'sackslot'

    def onNotifySlotUse(self, *arg):
        pass

    def getSlotID(self, key):
        idCon, idItem = key.split('.')
        return (int(idCon[4:]), int(idItem[4:]))

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        idPage, itemSlot = self.getSlotID(key)
        if idPage == const.MATERIAL_BAG_BIND_ID:
            i = BigWorld.player().materialBag.getQuickVal(0, itemSlot)
        elif idPage == const.FASHION_BAG_BIND_ID:
            i = BigWorld.player().fashionBag.getQuickVal(0, itemSlot)
        elif idPage == const.CART_BIND_ID:
            i = BigWorld.player().cart.getQuickVal(0, itemSlot)
        elif idPage == const.BAG_BAR_BIND_ID:
            i = BigWorld.player().bagBar.getQuickVal(0, itemSlot)
        elif idPage == const.TEMP_BAG_BIND_ID:
            i = BigWorld.player().tempBag.getQuickVal(0, itemSlot)
        elif idPage == const.MALL_BAR_BIND_ID:
            i = BigWorld.player().mallBag.getQuickVal(0, itemSlot)
        else:
            return
        if i == None:
            return
        else:
            return gameglobal.rds.ui.inventory.GfxToolTip(i)
