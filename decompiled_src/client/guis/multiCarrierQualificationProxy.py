#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/multiCarrierQualificationProxy.o
import BigWorld
import gameglobal
import uiConst
import events
from uiProxy import UIProxy
from guis import asObject

class MultiCarrierQualificationProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MultiCarrierQualificationProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_MULTI_CARRIER_QUALIFICATION, self.hide)

    def reset(self):
        self.enterTypeOption = [False, False, True]

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MULTI_CARRIER_QUALIFICATION:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MULTI_CARRIER_QUALIFICATION)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_MULTI_CARRIER_QUALIFICATION)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.confirmBtn.addEventListener(events.MOUSE_CLICK, self.handleClickConfirmBtn, False, 0, True)
        self.widget.cancelBtn.addEventListener(events.MOUSE_CLICK, self.handleClickCancelBtn, False, 0, True)
        self.widget.cBoxSameGuild.addEventListener(events.BUTTON_CLICK, self.handleValueChange, False, 0, True)
        self.widget.cBoxSameTeam.addEventListener(events.BUTTON_CLICK, self.handleValueChange, False, 0, True)
        self.refreshInfo()

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        self.enterTypeOption = list(p.wingWorldCarrier.enterTypeOption)
        self.widget.cBoxSameTeam.selected = self.enterTypeOption[0]
        self.widget.cBoxSameGuild.selected = self.enterTypeOption[1]

    def handleClickConfirmBtn(self, *args):
        p = BigWorld.player()
        if p.isOnWingWorldCarrier():
            p.cell.applyUpdateWingWorldCarrierEnterType(self.enterTypeOption)
        self.hide()

    def handleClickCancelBtn(self, *args):
        self.hide()

    def handleValueChange(self, *args):
        e = asObject.ASObject(args[3][0])
        if e.target.name == 'cBoxSameTeam':
            self.enterTypeOption[0] = e.target.selected
        elif e.target.name == 'cBoxSameGuild':
            self.enterTypeOption[1] = e.target.selected
        self.enterTypeOption[2] = not (self.enterTypeOption[0] or self.enterTypeOption[1])
