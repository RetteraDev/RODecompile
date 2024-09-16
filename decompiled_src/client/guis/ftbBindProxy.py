#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/ftbBindProxy.o
import BigWorld
import gameglobal
import uiConst
from guis import events
from uiProxy import UIProxy
from gamestrings import gameStrings
from cdata import game_msg_def_data as GMDD
WNDTYPE_SELECT = 1
WNDTYPE_BIND = 2

class FtbBindProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FtbBindProxy, self).__init__(uiAdapter)
        self.widget = None
        self.wndType = WNDTYPE_SELECT
        self.args = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_FTB_BIND, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_FTB_BIND:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.args = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_FTB_BIND)

    def show(self, wndType = WNDTYPE_SELECT):
        self.hide()
        self.wndType = wndType
        gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_FTB_BIND, True)
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_FTB_BIND)

    def initUI(self):
        self.widget.gotoAndStop('type%d' % self.wndType)
        self.widget.confirmBtn.addEventListener(events.BUTTON_CLICK, self.onConfirmBtnClick)
        self.widget.cancelBtn.addEventListener(events.BUTTON_CLICK, self.onCancelBtnClick)
        self.widget.closeBtn.addEventListener(events.BUTTON_CLICK, self.onCancelBtnClick)

    def refreshSelectWnd(self):
        self.widget.title.txtTitle.text = gameStrings.FTB_BIND_TITLE_SELECT
        self.widget.selectBtn0.selected = True

    def refreshBindWnd(self):
        self.widget.title.txtTitle.text = gameStrings.FTB_BIND_TITLE_BIND

    def refreshInfo(self):
        if not self.widget:
            return
        if self.wndType == WNDTYPE_SELECT:
            self.refreshSelectWnd()
        elif self.wndType == WNDTYPE_BIND:
            self.refreshBindWnd()

    def onCancelBtnClick(self, *args):
        if self.wndType == WNDTYPE_SELECT:
            self.hide()
        elif self.wndType == WNDTYPE_BIND:
            self.show(WNDTYPE_SELECT)

    def onConfirmBtnClick(self, *args):
        p = BigWorld.player()
        if self.wndType == WNDTYPE_SELECT:
            if self.widget.selectBtn0.selected:
                p.base.createFtbAddr()
                gameglobal.rds.ui.ftbLicense.show()
                self.hide()
            else:
                self.show(WNDTYPE_BIND)
        elif self.wndType == WNDTYPE_BIND:
            if self.widget.inputText.text == '':
                p.showGameMsg(GMDD.data.COMMON_MSG, (gameStrings.FTB_BIND_NOT_EMPTY,))
            else:
                p.base.bindFtbAddrByWords(self.widget.inputText.text)
