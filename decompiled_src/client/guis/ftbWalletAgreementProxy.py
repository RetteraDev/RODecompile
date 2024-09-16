#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/ftbWalletAgreementProxy.o
import BigWorld
import gameglobal
import uiConst
from uiProxy import UIProxy
from guis import events
from guis import ftbWalletHelper
from data import ftb_config_data as FCD

class FtbWalletAgreementProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FtbWalletAgreementProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_FTB_WALLET_AGREEMENT, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_FTB_WALLET_AGREEMENT:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_FTB_WALLET_AGREEMENT)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_FTB_WALLET_AGREEMENT)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.confirmCheck.selected = False
        self.widget.agreeBtn.enabled = False
        self.widget.agreeBtn.addEventListener(events.BUTTON_CLICK, self.onAgreeBtnClick)
        self.widget.cancelBtn.addEventListener(events.BUTTON_CLICK, self.onCancelBtnClick)
        self.widget.confirmCheck.addEventListener(events.EVENT_SELECT, self.onConfirmCheckChanged)
        self.widget.eventList.canvas.agreementText.htmlText = FCD.data.get('ftbWalletArgreement', '')
        self.widget.eventList.canvas.agreementText.height = self.widget.eventList.canvas.agreementText.textHeight + 5

    def onConfirmCheckChanged(self, *args):
        if self.widget.confirmCheck.selected:
            self.widget.agreeBtn.enabled = True
        else:
            self.widget.agreeBtn.enabled = False

    def onAgreeBtnClick(self, *args):
        if not ftbWalletHelper.getInstance().isBindGame():
            gameglobal.rds.ui.ftbWalletSubWnd.showSetPassWnd()
        else:
            p = BigWorld.player()
            p.base.createdFtbWallet()
            p.isFtbWalletCreated = True
            gameglobal.rds.ui.ftbWallet.show()
        self.hide()

    def onCancelBtnClick(self, *args):
        self.hide()

    def refreshInfo(self):
        if not self.widget:
            return
