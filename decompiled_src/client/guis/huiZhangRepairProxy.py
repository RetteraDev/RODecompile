#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/huiZhangRepairProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import const
from item import Item
from guis import uiUtils
from uiProxy import SlotDataProxy
from cdata import game_msg_def_data as GMDD
from cdata import guanyin_data as GD

class HuiZhangRepairProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(HuiZhangRepairProxy, self).__init__(uiAdapter)
        self.binding = {}
        self.bindType = 'huizhangRepair'
        self.type = 'huizhangRepair'
        self.modelMap = {'clickClose': self.onClickClose,
         'clickConfirm': self.onClickConfirm,
         'clearSlot': self.onClearSlot}
        self.mediator = None
        self.equipPage = -1
        self.equipPos = -1
        self.equipItem = None
        self.itemCost = None
        self.cashCost = None

    def _registerMediator(self, widgetId, mediator):
        pass

    def show(self):
        pass

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        self.equipPage = -1
        self.equipPos = -1
        self.equipItem = None
        self.itemCost = None
        self.cashCost = None
        if gameglobal.rds.ui.funcNpc.isOnFuncState():
            gameglobal.rds.ui.funcNpc.close()
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def reset(self):
        super(self.__class__, self).reset()
        self.message = ''
        self.nPage = const.CONT_NO_PAGE
        self.nItem = const.CONT_NO_POS

    def onClickConfirm(self, *arg):
        self._doRepair()

    def _doRepair(self):
        p = BigWorld.player()
        p.cell.repairGuanYin(const.RES_KIND_INV, self.equipPage, self.equipPos)

    def onClickClose(self, *arg):
        self.hide()

    def setRepairHuiZhang(self, page, pos, item):
        p = BigWorld.player()
        if item == const.CONT_EMPTY_VAL:
            return
        if not item.isGuanYin():
            return
        gd = GD.data.get(item.id)
        if not gd:
            return
        self.equipPage = page
        self.equipPos = pos
        self.equipItem = item
        btnVisible = True
        key0 = self.getKey(0)
        data = {}
        moneyString = ''
        numStr = ''
        data['iconPath'] = uiUtils.getItemIconFile64(item.id)
        self.binding[key0][1].InvokeSelf(uiUtils.dict2GfxDict(data))
        color = uiUtils.getItemColor(item.id)
        self.binding[key0][0].Invoke('setSlotColor', GfxValue(color))
        self.itemCost = GD.data.get(item.id, {}).get('repairItem')
        cashCost = GD.data.get(item.id, {}).get('repairCash')
        self.cashCost = cashCost
        if not self.itemCost:
            return
        key1 = self.getKey(1)
        data2 = {}
        data2['iconPath'] = uiUtils.getItemIconFile64(self.itemCost[0])
        data2['num'] = 1
        self.binding[key1][1].InvokeSelf(uiUtils.dict2GfxDict(data2))
        color = uiUtils.getItemColor(self.itemCost[0])
        self.binding[key1][0].Invoke('setSlotColor', GfxValue(color))
        num = p.inv.countItemInPages(uiUtils.getParentId(self.itemCost[0]), enableParentCheck=True)
        numStr = '%d/%d' % (num, self.itemCost[1])
        if num < self.itemCost[1]:
            numStr = "<font color = \'#FF0000\'>" + numStr
            btnVisible = False
        if p.cash < cashCost:
            moneyString = "<font color = \'#FF0000\'>" + str(cashCost)
            btnVisible = False
        else:
            moneyString = str(cashCost)
        equipData = {}
        equipData['money'] = moneyString
        equipData['num'] = numStr
        equipData['btnVisible'] = btnVisible
        if self.mediator:
            self.mediator.Invoke('setData', uiUtils.dict2GfxDict(equipData))
            self.mediator.Invoke('setText')

    def getKey(self, index):
        return 'huizhangRepair%d' % index

    def onGetToolTip(self, *arg):
        key = arg[3][0].GetString()
        if key == 'huizhangRepair0':
            ret = gameglobal.rds.ui.inventory.GfxToolTip(self.equipItem)
        elif key == 'huizhangRepair1':
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
            if not item.isGuanYin():
                return True
        return False
