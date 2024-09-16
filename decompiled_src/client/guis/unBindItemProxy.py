#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/unBindItemProxy.o
import BigWorld
from data import sys_config_data as SCD
from item import Item
import formula
import gameglobal
import gametypes
import const
from guis import ui
from guis import uiConst
from guis import uiUtils
from guis import events
from uiProxy import SlotDataProxy
from data import equip_data as ED
from cdata import game_msg_def_data as GMDD
from cdata import equip_unbind_consume_data as EUCD

class UnBindItemProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(UnBindItemProxy, self).__init__(uiAdapter)
        self.modelMap = {'closeWidget': self.onClose,
         'clearAllBindings': self.onClearAllBindings,
         'comfirmUnBind': self.onComfirmUnBind,
         'clearPanel': self.onClearPanel}
        self.type = 'unBindItem'
        self.bindType = 'unBindItem'
        self.srcPos = [-1, -1]
        self.mediator = None
        self.item = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_UNBIND_ITEM, self.onClose)

    def onClearAllBindings(self, *arg):
        self.binding = {}

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_UNBIND_ITEM:
            self.item = None
            self.mediator = mediator
            if gameglobal.rds.ui.inventory.mediator:
                gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def onComfirmUnBind(self, *arg):
        if self.srcPos:
            p = BigWorld.player()
            item = p.inv.getQuickVal(self.srcPos[0], self.srcPos[1])
            if getattr(item, 'id', -1) != getattr(self.item, 'id', -1):
                msg = 'unBindItem error %d %d' % (getattr(item, 'id', -1), getattr(self.item, 'id', -1))
                p.reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_SCRIPT, [msg], 0, {})
                return
            if item.isManualEquip() or item.isExtendedEquip():
                itemInfo = uiUtils.getGfxItem(item, location=const.ITEM_MANUAL_EQUIP)
                msg = uiUtils.getTextFromGMD(GMDD.data.UNBIND_MANUAL_EQUIP_CONFIRM, '')
                gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, self.confirmUnbindManualEquip, itemData=itemInfo)
            else:
                p.cell.unbindEquipment(self.srcPos[0], self.srcPos[1])

    def confirmUnbindManualEquip(self):
        if self.srcPos and self.item:
            p = BigWorld.player()
            item = p.inv.getQuickVal(self.srcPos[0], self.srcPos[1])
            if getattr(item, 'id', -1) == getattr(self.item, 'id', -1):
                p.cell.unbindEquipment(self.srcPos[0], self.srcPos[1])

    def getSlotID(self, key):
        idBar, idItem = key.split('.')
        return (int(idBar[10:]), int(idItem[4:]))

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_UNBIND_ITEM)
        if self.mediator:
            self.mediator.Invoke('show')

    def onClose(self, *arg):
        self.hide()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        self.item = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_UNBIND_ITEM)
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def clearPanel(self):
        if self.mediator:
            self.item = None
            self.mediator.Invoke('clearPanel')

    def onClearPanel(self, *arg):
        self.item = None

    def notSuitUnBind(self, item):
        if item:
            if not item.isEquip():
                return True
            if not item.isForeverBind():
                return True
            ed = ED.data.get(item.id)
            if not ed:
                return True
            ud = EUCD.data.get((item.quality, item.equipType, item.equipSType))
            if not ud:
                return True
            oldUnbindTimes = getattr(item, 'unbindTimes', 0)
            if oldUnbindTimes >= ed.get('unbindTimes', 0):
                return True
        return False

    def matchCondition(self, item):
        if item:
            if self.notSuitUnBind(item):
                return False
            p = BigWorld.player()
            if getattr(item, 'enhLv', 0) > 0:
                p.showGameMsg(GMDD.data.UNBIND_EQUIP_ERROR_ENHLV, ())
                return False
            if item.hasGem():
                p.showGameMsg(GMDD.data.UNBIND_EQUIP_ERROR_WEN_YING, ())
                return False
            if getattr(item, 'yaoPeiExp', 0) > 0:
                p.showGameMsg(GMDD.data.UNBIND_EQUIP_ERROR_YP_EXP, ())
                return False
            if hasattr(item, 'refineManual'):
                rCnt = item.refineManual.get(Item.REFINE_MANUAL_REFINE_CNT, 0)
                unCnt = item.refineManual.get(Item.REFINE_MANUAL_UNREFINE_CNT, 0)
                specialFlag = item.refineManual.get(Item.REFINE_MANUAL_UNREFINE_SPECIAL_FLAG, False)
                unrefineBase = SCD.data.get('unrefineManualEquipmentBaseCnt', 100)
                if not specialFlag and rCnt - unCnt * unrefineBase < unrefineBase:
                    BigWorld.player().showGameMsg(GMDD.data.UNBIND_EQUIP_REFINIE_BASE_CNT, ())
                    return False
            return True
        return True

    @ui.uiEvent(uiConst.WIDGET_UNBIND_ITEM, events.EVENT_INVENTORY_ITEM_CLICKED)
    def onUnBindItemClick(self, event):
        event.stop()
        it = event.data['item']
        nPage = event.data['page']
        nItem = event.data['pos']
        if it == None:
            return
        else:
            if self.matchCondition(it):
                self.equipItem(it, nPage, nItem)
            return

    def resetInventoryItemState(self):
        removePage = self.srcPos[0]
        removePos = self.srcPos[1]
        self.srcPos = [-1, -1]
        self.item = None
        gameglobal.rds.ui.inventory.updateSlotState(removePage, removePos)

    def equipItem(self, item, nPageSrc, nItemSrc):
        if self.item:
            self.resetInventoryItemState()
        self.updateItem(item, nPageSrc, nItemSrc)

    def updateItem(self, item, nPageSrc, nItemSrc):
        self.item = item
        self.srcPos[0] = nPageSrc
        self.srcPos[1] = nItemSrc
        gameglobal.rds.ui.inventory.updateSlotState(self.srcPos[0], self.srcPos[1])
        ud = EUCD.data.get((item.quality, item.equipType, item.equipSType))
        itemInfo = uiUtils.getGfxItem(item, location=const.ITEM_IN_BAG)
        p = BigWorld.player()
        needCash = formula.calcValueByFormulaData(ud.get('cash', None), {'order': item.order})
        needItemNum = formula.calcValueByFormulaData(ud.get('itemNum', None), {'order': item.order})
        needItemInfo = {}
        itemId = ud.get('itemId', 0)
        needItemInfo['cash'] = needCash
        needItemInfo['playerCash'] = p.cash
        ownCount = p.inv.countItemInPages(int(itemId), enableParentCheck=True)
        needItemInfo['hasItem'] = ownCount
        needItemInfo['needItem'] = needItemNum
        needItemInfo['item'] = uiUtils.getGfxItemById(itemId, '')
        self.updateEquipSlot(itemInfo, needItemInfo)
        gameglobal.rds.ui.inventory.updateSlotState(self.srcPos[0], self.srcPos[1])

    def updateEquipSlot(self, unBindInfo, needItemInfo):
        if self.mediator:
            self.mediator.Invoke('updateEquipSlot', (uiUtils.dict2GfxDict(unBindInfo, True), uiUtils.dict2GfxDict(needItemInfo, True)))

    def isItemDisabled(self, kind, page, pos, item):
        if self.mediator:
            if self.notSuitUnBind(item):
                return True
            if item == self.item:
                return True
        return False

    def unbindEquipSucc(self, page, pos):
        item = BigWorld.player().inv.getQuickVal(page, pos)
        self.item = item
        self.mediator.Invoke('unBindItemSucc')
        BigWorld.player().showGameMsg(GMDD.data.UNBIND_SUCCESS, ())
