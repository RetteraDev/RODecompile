#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/equipSoulStarProxy.o
import BigWorld
import gameglobal
import uiConst
import events
import uiUtils
import gametypes
import utils
from uiProxy import UIProxy
from gamestrings import gameStrings
from data import sys_config_data as SCD

class EquipSoulStarProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(EquipSoulStarProxy, self).__init__(uiAdapter)
        self.widget = None
        self.itemId = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_EQUIP_SOUL_STAR, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_EQUIP_SOUL_STAR:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_EQUIP_SOUL_STAR)

    def show(self):
        if not gameglobal.rds.configData.get('enableEquipSoul', False):
            return
        self.itemId = SCD.data.get('equipSoulStarItemId', 0)
        if self.widget:
            self.widget.swapPanelToFront()
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_EQUIP_SOUL_STAR)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        itemNum = BigWorld.player().inv.countItemInPages(self.itemId, enableParentCheck=True)
        self.widget.itemSlot.setItemSlotData(uiUtils.getGfxItemById(self.itemId, itemNum))
        if not itemNum:
            self.widget.itemSlot.setSlotState(uiConst.COMPLETE_ITEM_LEAKED)
        self.widget.itemSlot.dragable = False
        self.widget.useOneBtn.addEventListener(events.MOUSE_CLICK, self.handleClickUseOneBtn, False, 0, True)
        self.widget.useTenBtn.addEventListener(events.MOUSE_CLICK, self.handleClickUseTenBtn, False, 0, True)

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        itemNum = BigWorld.player().inv.countItemInPages(self.itemId, enableParentCheck=True)
        self.widget.itemSlot.setValueAmountTxt(itemNum)
        useNum = uiUtils.getItemUseNum(self.itemId, gametypes.ITEM_USE_LIMIT_TYPE_WEEK)
        useLimit = uiUtils.getItemUseLimit(self.itemId, gametypes.ITEM_USE_LIMIT_TYPE_WEEK)
        limitNum = utils.getUseLimitByLv(self.itemId, p.lv, gametypes.ITEM_USE_LIMIT_TYPE_WEEK, useLimit)
        self.widget.canUseTimes.htmlText = gameStrings.EQUIP_SOUL_STAR_USE_TIMES % (limitNum - useNum, limitNum)

    def handleClickUseOneBtn(self, *args):
        BigWorld.player().cell.useEquipSoulItem(self.itemId, 1)

    def handleClickUseTenBtn(self, *args):
        BigWorld.player().cell.useEquipSoulItem(self.itemId, 10)
