#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/tianBiToYunChuiProxy.o
import BigWorld
import gameglobal
import uiConst
import events
from uiProxy import UIProxy
from guis import uiUtils
from guis import ui
from data import sys_config_data as SCD
from data import mall_item_data as MID
BUY_MAX_NUM = 999
TIANBI_COST = 10

class TianBiToYunChuiProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(TianBiToYunChuiProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_TIANBI_TO_YUNCHUI, self.hide)

    def reset(self):
        self.buyNum = 1

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_TIANBI_TO_YUNCHUI:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_TIANBI_TO_YUNCHUI)
        self.reset()

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_TIANBI_TO_YUNCHUI)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        mallId = SCD.data.get('buyYunChuiCreditConsumeCoinMallId', 0)
        itemId = MID.data.get(mallId, {}).get('itemId', 0)
        self.widget.itemSlot.dragable = False
        self.widget.itemSlot.setItemSlotData(uiUtils.getGfxItemById(itemId))
        self.widget.txtItemName.htmlText = uiUtils.getItemColorName(itemId)

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        self.widget.txtCost.text = str(self.buyNum * TIANBI_COST)
        tianbi = p.unbindCoin + p.bindCoin + p.freeCoin
        maxCount = max(1, tianbi / TIANBI_COST)
        maxCount = min(BUY_MAX_NUM, maxCount)
        self.widget.counter.maxCount = maxCount
        self.widget.counter.count = self.buyNum
        self.widget.txtGained.text = str(self.buyNum * TIANBI_COST * SCD.data.get('yunchuiCreditPerCoin', 0))
        self.widget.counter.addEventListener(events.EVENT_COUNT_CHANGE, self.handleCounterChange, False, 0, True)
        self.widget.maxBtn.addEventListener(events.BUTTON_CLICK, self.handleMaxBtnClick, False, 0, True)
        self.widget.buyBtn.addEventListener(events.BUTTON_CLICK, self.handleBuyBtnClick, False, 0, True)

    @ui.checkInventoryLock()
    def handleBuyBtnClick(self, *args):
        p = BigWorld.player()
        p.cell.buyYunChuiCreditConsumeCoin(self.buyNum * TIANBI_COST, p.cipherOfPerson)
        self.hide()

    def handleCounterChange(self, *args):
        count = int(self.widget.counter.count)
        if count != self.buyNum:
            self.buyNum = count
            self.refreshInfo()

    def handleMaxBtnClick(self, *args):
        p = BigWorld.player()
        tianbi = p.unbindCoin + p.bindCoin + p.freeCoin
        maxCount = max(1, tianbi / TIANBI_COST)
        maxCount = min(1000, maxCount)
        self.widget.counter.count = maxCount
        self.refreshInfo()
