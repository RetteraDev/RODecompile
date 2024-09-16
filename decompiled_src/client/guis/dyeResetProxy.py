#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/dyeResetProxy.o
from gamestrings import gameStrings
import copy
import BigWorld
from Scaleform import GfxValue
import gameglobal
from guis.uiProxy import SlotDataProxy
from guis import uiConst
from guis import uiUtils
from item import Item
from data import sys_config_data as SCD

class DyeResetProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(DyeResetProxy, self).__init__(uiAdapter)
        self.bindType = 'dyeReset'
        self.type = 'dyeReset'
        self.modelMap = {'handleClickSlot': self.onHandleClickSlot,
         'handleOkClick': self.onHandleOkClick}
        self.reset()
        self.med = None
        self.isShow = False

    def reset(self):
        self.equipPage = None
        self.equipPos = None
        self.equipItem = None
        self.resKind = 0
        self.npcEntId = 0

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_DYE_RESET:
            self.med = mediator
            self.isShow = True

    def show(self, npcEntId = 0):
        self.npcEntId = npcEntId
        if not self.isShow:
            self.uiAdapter.inventory.show()
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_DYE_RESET)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_DYE_RESET)
        self.isShow = False
        self.med = None
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()

    def getKey(self):
        return 'dyeReset.slot0'

    def close(self):
        if not self.hasEquiped():
            return
        msg = SCD.data.get('DYE_RESET_CONFIRM_MSG', gameStrings.TEXT_DYERESETPROXY_66)
        self.uiAdapter.messageBox.showYesNoMsgBox(msg, self.saveAndClose, gameStrings.TEXT_DYEPLANEPROXY_444, self.hide, gameStrings.TEXT_PLAYRECOMMPROXY_494_1)

    def saveAndClose(self):
        player = None
        if self.npcEntId:
            npc = BigWorld.entity(self.npcEntId)
            if npc and npc.inWorld:
                player = npc
        else:
            player = BigWorld.player()
        if player:
            player.cell.resetFashionEquip(self.equipPage, self.equipPos, self.resKind)
        self.hide()

    def onHandleOkClick(self, *arg):
        self.close()

    def setEquip(self, page, pos, item, resKind):
        if item and getattr(item, 'equipType', 0) != Item.EQUIP_BASETYPE_FASHION:
            gameglobal.rds.ui.topMessage.showTopMsg(gameStrings.TEXT_DYERESETPROXY_86)
            return
        else:
            self.reset()
            self.resKind = resKind
            key = self.getKey()
            if item == None:
                self.equipPage = None
                self.equipPos = None
                self.equipItem = None
                data = GfxValue(1)
                data.SetNull()
                self.binding[key][1].InvokeSelf(data)
            else:
                self.equipPage = page
                self.equipPos = pos
                gameglobal.rds.ui.inventory.updateSlotState(page, pos)
                self.equipItem = copy.copy(item)
                data = {}
                data['iconPath'] = uiUtils.getItemIconFile64(item.id)
                data['color'] = uiUtils.getItemColor(item.id)
                self.binding[key][1].InvokeSelf(uiUtils.dict2GfxDict(data))
            return

    def onHandleClickSlot(self, *arg):
        if self.hasEquiped():
            self.setEquip(None, None, None, None)

    def hasEquiped(self):
        return self.equipItem != None

    def onGetToolTip(self, *arg):
        if self.equipItem:
            return self.uiAdapter.inventory.GfxToolTip(self.equipItem)
