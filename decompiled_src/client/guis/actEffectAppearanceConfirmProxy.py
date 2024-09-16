#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/actEffectAppearanceConfirmProxy.o
import BigWorld
import gameglobal
import math
import uiConst
import const
import events
import utils
from uiProxy import SlotDataProxy
from item import Item
from gamestrings import gameStrings
from callbackHelper import Functor
from sfx import physicsEffect
from helpers import skillAppearancesUtils
from guis import uiUtils
from data import consumable_item_data as CID
from data import act_appearance_data as AAD
from cdata import game_msg_def_data as GMDD

class ActEffectAppearanceConfirmProxy(SlotDataProxy):

    def __init__(self, uiAdapter):
        super(ActEffectAppearanceConfirmProxy, self).__init__(uiAdapter)
        self.bindType = 'actEffectAppearanceConfirm'
        self.type = 'actEffectAppearanceConfirm'
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_ACTION_EFFECT_APPEARANCE_CONFIRM, self.hide)

    def reset(self):
        self.itemId = -1
        self.itemUUID = None

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ACTION_EFFECT_APPEARANCE_CONFIRM:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.reset()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ACTION_EFFECT_APPEARANCE_CONFIRM)
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def getSlotID(self, key):
        return (0, 0)

    def show(self, itemId, itemUUID):
        tmpItem = Item(itemId)
        if not tmpItem or not tmpItem.isActEffectAppearanceItem():
            return
        self.itemId = itemId
        self.itemUUID = itemUUID
        self._realShow()
        if not gameglobal.rds.ui.inventory.mediator:
            gameglobal.rds.ui.inventory.show()

    def _realShow(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_ACTION_EFFECT_APPEARANCE_CONFIRM)
        else:
            self.refreshInfo()

    def isShow(self):
        return not not self.widget

    def onItemDrag(self, item):
        if not item or not item.isActEffectAppearanceItem():
            return
        if not physicsEffect.checkItemCanUse(item):
            return
        self.show(item.id, item.uuid)

    def onUseItem(self, item):
        if not item or not item.isActEffectAppearanceItem():
            return
        if not physicsEffect.checkItemCanUse(item):
            return
        self.show(item.id, item.uuid)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.desc.text = ''
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.handleConfirmBtnClick, False, 0, True)
        self.widget.cancelBtn.addEventListener(events.BUTTON_CLICK, self.handleCancelBtnClick, False, 0, True)
        self.widget.item.binding = 'actEffectAppearanceConfirm0.slot0'
        self.widget.item.dragable = False

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        self.widget.item.enabled = True
        allNum = p.inv.countItemInPages(self.itemId)
        needNum = 1
        itemInfo = uiUtils.getGfxItemById(self.itemId, uiUtils.convertNumStr(allNum, needNum))
        if allNum < needNum:
            itemInfo['state'] = uiConst.COMPLETE_ITEM_LEAKED
        else:
            itemInfo['state'] = uiConst.ITEM_NORMAL
        self.widget.item.setItemSlotData(itemInfo)
        self.widget.confirmBtn.enabled = allNum >= needNum
        itemConfig = CID.data.get(self.itemId, {})
        expireTime = itemConfig.get('expireTime', -1)
        appearanceId = itemConfig.get('appearanceId', 0)
        nName = AAD.data.get(appearanceId, {}).get('nName', '')
        if nName:
            self.widget.desc.text = gameStrings.ACT_APPEARANCE_CONFIRM_DESC % (nName, self._getCurrentLeftTime(expireTime))
        else:
            self.widget.desc.text = ''
        gameglobal.rds.ui.inventory.updateCurrentPageSlotState()

    def handleConfirmBtnClick(self, *args):
        p = BigWorld.player()
        item, page, idx = p.inv.findItemByUUID(self.itemUUID)
        if not item or not item.isActEffectAppearanceItem():
            return
        if not physicsEffect.checkItemCanUse(item):
            return
        aid = CID.data.get(item.id, {}).get('appearanceId', 0)
        expire = physicsEffect.getAppearanceDeadLineTime(aid)
        if expire == -1 or expire > 0 and expire > utils.getNow():
            import gamelog
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.ACT_APPEARANCE_CONTINUE_USE % gameglobal.rds.ui.actEffectAppearance.getDeadlineTextPure(expire), Functor(self._realUseAppearanceItem, page, idx))
            return
        self._realUseAppearanceItem(page, idx)

    def handleCancelBtnClick(self, *args):
        self.hide()

    def isItemDisabled(self, kind, page, pos, item):
        p = BigWorld.player()
        _, pg, i = p.inv.findItemByUUID(self.itemUUID)
        if self.widget and kind == const.RES_KIND_INV:
            if (page, pos) == (pg, i):
                return True
            if not item.isActEffectAppearanceItem():
                return True
            if physicsEffect.checkItemCanUse(item):
                return False
            return True
        else:
            return False

    def _getCurrentLeftTime(self, leftTime):
        if leftTime == -1:
            return gameStrings.COMMON_INFINITE_TIME
        elif leftTime > const.TIME_INTERVAL_DAY:
            return str(int(math.ceil(float(leftTime) / const.TIME_INTERVAL_DAY))) + gameStrings.COMMON_DAY
        elif leftTime > const.TIME_INTERVAL_HOUR:
            return str(int(math.ceil(float(leftTime) / const.TIME_INTERVAL_HOUR))) + gameStrings.COMMON_HOUR
        elif leftTime > const.TIME_INTERVAL_MINUTE:
            return str(int(math.ceil(float(leftTime) / const.TIME_INTERVAL_MINUTE))) + gameStrings.COMMON_MINUTE
        else:
            return gameStrings.COMMON_LESSTHAN_ONE_MINUTE

    def _getAppearanceId(self, itemId):
        appearanceId = CID.data.get(itemId, {}).get('appearanceId', -1)
        return appearanceId

    def _realUseAppearanceItem(self, page, idx):
        p = BigWorld.player()
        p.useBagItem(page, idx)
        self.hide()
