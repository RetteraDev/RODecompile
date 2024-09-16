#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/equipRepairProxy.o
import BigWorld
import const
import gameglobal
from Scaleform import GfxValue
from uiProxy import UIProxy
from guis import uiConst
from gamestrings import gameStrings
from guis import uiUtils
from callbackHelper import Functor
from data import game_msg_data as GMD
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SCD

class EquipRepairProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(EquipRepairProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerEquipRepair': self.onRegisterEquipRepair,
         'getEquipState': self.onGetEquipState,
         'findRepairNpc': self.onFindRepairNpc}
        self.mc = None
        self.isShow = False

    def onRegisterEquipRepair(self, *arg):
        self.mc = arg[3][0]

    def onGetEquipState(self, *arg):
        ret = self.formEquipArr()
        return ret

    def show(self):
        if self.needShow() and not self.isShow:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_EQUIP_REPAIR)
            self.isShow = True
        elif self.isShow and not self.needShow():
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EQUIP_REPAIR)
            self.isShow = False

    def formEquipArr(self):
        ret = self.movie.CreateArray()
        p = BigWorld.player()
        for i, item in enumerate(p.equipment):
            if i > 10 or i == 5:
                break
            if item:
                if item.cdura >= const.EQUIP_HALF_BROKEN * item.initMaxDura:
                    ret.SetElement(i, GfxValue(0))
                elif item.cdura > const.EQUIP_BROKEN and item.cdura < const.EQUIP_HALF_BROKEN * item.initMaxDura:
                    ret.SetElement(i, GfxValue(1))
                else:
                    ret.SetElement(i, GfxValue(2))
            else:
                ret.SetElement(i, GfxValue(0))

        return ret

    def close(self):
        if self.isShow:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EQUIP_REPAIR)
            self.isShow = False

    def setEquipState(self):
        if self.needShow():
            if self.isShow:
                ret = self.formEquipArr()
                if self.mc != None:
                    self.mc.Invoke('setEquipState', ret)
            else:
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_EQUIP_REPAIR)
                self.isShow = True
            gameglobal.rds.tutorial.onEquipRepair()
        elif self.isShow:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_EQUIP_REPAIR)
            gameglobal.rds.ui.setVisRecord(uiConst.WIDGET_EQUIP_REPAIR, False)
            self.isShow = False

    def needShow(self):
        p = BigWorld.player()
        needShow = False
        for item in p.equipment:
            if not item:
                continue
            if item.isWingOrRide():
                continue
            if item.cdura < const.EQUIP_HALF_BROKEN * item.initMaxDura:
                needShow = True
                break

        return needShow

    def onFindRepairNpc(self, *arg):
        shopSeekId = SCD.data.get('equipRepairNavigatorTarget', (11010418,))
        msg = GMD.data.get(GMDD.data.EQUIP_REPAIR_FIND_NPC_MSG, {}).get('text', gameStrings.EQUIP_REPAIR_FIND_NPC_MSG)
        if not gameglobal.rds.ui.messageBox.checkOnceMap.get(uiConst.CHECK_ONCE_TYPE_FIND_EQUIP_REPAIR_NPC, False):
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(uiUtils.findPosWithAlert, shopSeekId), isShowCheckBox=True, checkOnceType=uiConst.CHECK_ONCE_TYPE_FIND_EQUIP_REPAIR_NPC)
        else:
            uiUtils.findPosWithAlert(shopSeekId)
