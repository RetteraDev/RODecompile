#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/runeXiLianProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import const
from guis import uiUtils
from uiProxy import UIProxy
from item import Item
from data import item_data as ID
from cdata import font_config_data as FCD
from cdata import rune_equip_xilian_data as REXD

class RuneXiLianProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(RuneXiLianProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickClose': self.onClickClose,
         'clickConfirm': self.onClickConfirm,
         'getInitData': self.onGetInitData}
        self.mediator = None
        self.itemList = ()

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_RUNE_XILIAN:
            self.mediator = mediator

    def show(self):
        if not self.mediator and BigWorld.player().runeBoard.runeEquip:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_RUNE_XILIAN)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_RUNE_XILIAN)

    def reset(self):
        super(self.__class__, self).reset()
        self.itemList = ()

    def onClickClose(self, *arg):
        self.hide()

    def onClickConfirm(self, *arg):
        if gameglobal.rds.ui.runeChongXi.mediator:
            return
        p = BigWorld.player()
        posList = []
        for itemNeed in self.itemList:
            pg, pos = p.inv.findItemByAttr({'id': itemNeed[0]})
            if pg != const.CONT_NO_PAGE:
                posList.append((pg, pos))

        if posList:
            p.cell.runeEquipXiLian(posList)
        self.hide()

    def onGetInitData(self, *arg):
        initObj = self.movie.CreateObject()
        slotArray = self.movie.CreateArray()
        p = BigWorld.player()
        runeEquip = p.runeBoard.runeEquip
        xData = REXD.data.get(runeEquip.runeEquipOrder)
        if not xData:
            self.hide()
            return
        xiLianData = xData.get('xiLianData')
        if not xiLianData:
            self.hide()
            return
        canConfirm = True
        self.itemList = xiLianData[0][0]
        for i, item in enumerate(xiLianData[0][0]):
            itemId, itemNum = item
            slotObj = self.movie.CreateObject()
            if itemNum > p.inv.countItemInPages(itemId):
                canConfirm = False
                slotObj.SetMember('isDisable', GfxValue(True))
            else:
                slotObj.SetMember('isDisable', GfxValue(False))
            slotObj.SetMember('count', GfxValue(itemNum))
            path = uiUtils.getItemIconFile40(itemId)
            slotObj.SetMember('icon', GfxValue(path))
            quality = ID.data.get(itemId, {}).get('quality', 1)
            color = FCD.data.get(('item', quality), {}).get('qualitycolor', 'nothing')
            slotObj.SetMember('color', GfxValue(color))
            slotArray.SetElement(i, slotObj)

        initObj.SetMember('slotArray', slotArray)
        initObj.SetMember('canConfirm', GfxValue(canConfirm))
        return initObj

    def onGetToolTip(self, *arg):
        index = int(arg[3][0].GetString()[15:])
        return gameglobal.rds.ui.inventory.GfxToolTip(Item(self.itemList[index][0]))

    def updateItemNum(self, item):
        if self.mediator:
            for itemNeed in self.itemList:
                if itemNeed[0] == item.id:
                    self.refreshConfirmBtn()
                    return

    def refreshConfirmBtn(self):
        if self.mediator:
            updateObj = self.movie.CreateObject()
            slotArray = self.movie.CreateArray()
            p = BigWorld.player()
            canConfirm = True
            for i, item in enumerate(self.itemList):
                itemId, itemNum = item
                if itemNum > p.inv.countItemInPages(itemId):
                    canConfirm = False
                    slotArray.SetElement(i, GfxValue(True))
                else:
                    slotArray.SetElement(i, GfxValue(False))

            updateObj.SetMember('slotArray', slotArray)
            updateObj.SetMember('canConfirm', GfxValue(canConfirm))
            self.mediator.Invoke('refreshConfirmBtn', updateObj)
