#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/itemBatchUseProxy.o
import BigWorld
import uiConst
import events
import const
import uiUtils
import sys
import gametypes
import utils
from guis import ui
from uiProxy import UIProxy
from asObject import ASObject
from cdata import game_msg_def_data as GMDD
COUNTER_MIN = 0
COUNTER_MAX = 99

class ItemBatchUseProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ItemBatchUseProxy, self).__init__(uiAdapter)
        self.widget = None
        self.itemId = 0
        self.useNumber = 1
        self.page = 0
        self.index = 0
        self.itemCwrap = 0
        self.restNum = sys.maxint
        self.item = None
        self.LimitExceedMsg = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_ITEM_BATCH_USE, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_ITEM_BATCH_USE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    @ui.uiEvent(uiConst.WIDGET_ITEM_BATCH_USE, events.EVENT_PLAYER_SPACE_NO_CHANGED)
    def onSpaceNoChanged(self):
        self.hide()

    def clearWidget(self):
        self.widget = None
        self.reset()
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ITEM_BATCH_USE)
        if BigWorld.player():
            BigWorld.player().unRegisterEvent(const.EVENT_ITEM_CHANGE, self.setCount)
            BigWorld.player().unRegisterEvent(const.EVENT_ITEM_MOVE, self.setCount)
            BigWorld.player().unRegisterEvent(const.EVENT_ITEM_REMOVE, self.setCount)
            BigWorld.player().unRegisterEvent(const.EVENT_ITEM_SORT, self.onItemSort)

    def reset(self):
        self.startTime = 0
        self.isFirstSortItem = False
        self.isFindItem = False

    def show(self):
        self.setRestNum(self.itemId)
        if not self.widget and self.restNum:
            self.uiAdapter.loadWidget(uiConst.WIDGET_ITEM_BATCH_USE)
        self.refreshInfo()

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.maxBtn.enabled = True
        self.widget.counter.enableMouseWheel = False
        self.widget.counter.count = self.itemCwrap
        self.widget.itemSlot.setItemSlotData(uiUtils.getGfxItemById(self.itemId))
        self.widget.counter.minCount = COUNTER_MIN
        self.widget.counter.maxCount = COUNTER_MAX
        self.widget.counter.addEventListener(events.EVENT_COUNT_CHANGE, self.handleUseNumberChange, False, 0, True)
        self.widget.maxBtn.addEventListener(events.MOUSE_CLICK, self.handleClickMaxBtn, False, 0, True)
        self.widget.confirmBtn.addEventListener(events.MOUSE_CLICK, self.handleClickConfirmBtn, False, 0, True)
        self.widget.cancelBtn.addEventListener(events.MOUSE_CLICK, self.handleClickCancelBtn, False, 0, True)
        BigWorld.player().registerEvent(const.EVENT_ITEM_MOVE, self.setCount)
        BigWorld.player().registerEvent(const.EVENT_ITEM_CHANGE, self.setCount)
        BigWorld.player().registerEvent(const.EVENT_ITEM_REMOVE, self.setCount)
        BigWorld.player().registerEvent(const.EVENT_ITEM_SORT, self.onItemSort)
        self.widget.maxBtn.enable = True

    def refreshInfo(self):
        if not self.widget:
            return
        self.widget.itemSlot.setItemSlotData(uiUtils.getGfxItemById(self.itemId))
        self.setCount()

    def setItem(self, item, page, index):
        self.item = item
        self.itemCwrap = item.cwrap
        self.itemId = item.id
        self.itemUuid = item.uuid

    def setLimitExceedMsg(self, limitType):
        if limitType == gametypes.ITEM_USE_LIMIT_TYPE_DAY:
            self.LimitExceedMsg = GMDD.data.ITEM_LIMIT_EXCEED_TODAY
        elif limitType == gametypes.ITEM_USE_LIMIT_TYPE_WEEK:
            self.LimitExceedMsg = GMDD.data.ITEM_LIMIT_EXCEED_THIS_WEEK
        elif limitType == gametypes.ITEM_USE_LIMIT_TYPE_MONTH:
            self.LimitExceedMsg = GMDD.data.ITEM_LIMIT_EXCEED_THIS_MONTH
        elif limitType == gametypes.ITEM_USE_LIMIT_TYPE_QUARTER:
            self.LimitExceedMsg = GMDD.data.ITEM_LIMIT_EXCEED_THIS_QUARTER

    def handleUseNumberChange(self, *args):
        e = ASObject(args[3][0])
        self.useNumber = int(e.currentTarget.count)

    def handleClickMaxBtn(self, *args):
        self.setCount()

    def handleClickConfirmBtn(self, *args):
        p = BigWorld.player()
        useNum = self.widget.counter.count
        if useNum == 0:
            self.widget.confirmBtn.enabled = False
            return
        p.cell.useCommonItem(self.page, self.index, useNum, const.RES_KIND_INV)

    def setCount(self, *args):
        if self.widget:
            p = BigWorld.player()
            item, page, pos = p.inv.findItemByUUID(self.itemUuid)
            if item:
                itemNum = item.cwrap
                self.index = pos
                self.page = page
                self.setRestNum(item.id)
                maxNum = min(self.restNum, itemNum)
                self.widget.confirmBtn.enabled = True
                self.widget.counter.maxCount = maxNum
                self.widget.counter.count = maxNum
            else:
                self.widget.counter.maxCount = 0
                self.widget.counter.count = 0
                self.widget.confirmBtn.enabled = False

    def onItemSort(self, params):
        currentTime = utils.getNow()
        if not self.isFirstSortItem:
            self.isFirstSortItem = True
            self.startTime = currentTime
        sortTime = currentTime - self.startTime
        if self.isFindItem:
            if sortTime <= 20:
                return
            self.isFindItem = False
            self.startTime = currentTime
        item = params[3]
        if self.widget:
            if item.uuid == self.itemUuid:
                itemNum = item.cwrap
                self.index = params[2]
                self.page = params[1]
                self.setRestNum(item.id)
                maxNum = min(self.restNum, itemNum)
                self.widget.confirmBtn.enabled = True
                self.widget.counter.maxCount = maxNum
                self.widget.counter.count = maxNum
                self.isFindItem = True
            else:
                self.widget.counter.maxCount = 0
                self.widget.counter.count = 0
                self.widget.confirmBtn.enabled = False

    def handleClickCancelBtn(self, *args):
        self.clearWidget()

    def setRestNum(self, itemId):
        p = BigWorld.player()
        rest = uiUtils.getitemUseLimitNum(itemId)
        if rest:
            self.restNum = rest[1]
            self.setLimitExceedMsg(rest[0])
            if self.restNum == 0:
                p.showGameMsg(self.LimitExceedMsg, ())
        else:
            self.restNum = sys.maxint

    def onUseItem(self):
        if self.widget:
            self.clearWidget()
