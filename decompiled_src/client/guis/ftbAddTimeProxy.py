#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/ftbAddTimeProxy.o
import BigWorld
import gameglobal
import uiConst
from guis import events
from uiProxy import UIProxy
from data import ftb_config_data as FCD
COUNTER_MAX = 99

class FtbAddTimeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FtbAddTimeProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_FTB_ADD_TIME, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_FTB_ADD_TIME:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_FTB_ADD_TIME)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_FTB_ADD_TIME)

    def initUI(self):
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.onConfirmBtnClick)
        self.widget.cancelBtn.addEventListener(events.BUTTON_CLICK, self.onCancelBtnClick)
        self.widget.betTime.count = 1
        self.widget.betTime.minCount = 1
        self.widget.betTime.maxCount = COUNTER_MAX
        self.widget.betTime.addEventListener(events.EVENT_COUNT_CHANGE, self.handleCountChange, False, 0, True)

    def onConfirmBtnClick(self, *args):
        addTime = self.widget.betTime.count
        if addTime:
            BigWorld.player().base.buyFtbTradeItem(addTime)
        self.hide()

    def handleCountChange(self, *args):
        self.refreshInfo()

    def onCancelBtnClick(self, *args):
        self.hide()

    def refreshInfo(self):
        if not self.widget:
            return
        addTime = self.widget.betTime.count
        if addTime:
            self.widget.confirmBtn.enable = False
        else:
            self.widget.confirmBtn.enable = True
        price = FCD.data.get('ftbTradeItemPrice', 0)
        cost = price * addTime
        p = BigWorld.player()
        if p.cash < cost:
            self.widget.costText.htmlText = "<font color = \'#FF0000\'>%s</font>" % str(cost)
        else:
            self.widget.costText.htmlText = cost
