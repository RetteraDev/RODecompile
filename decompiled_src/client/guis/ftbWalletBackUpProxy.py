#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/ftbWalletBackUpProxy.o
import BigWorld
import base64
import gameglobal
import uiConst
from guis import ftbWalletSubWndProxy
from guis import events
from guis.asObject import TipManager
from uiProxy import UIProxy
from guis import ftbWalletHelper
from gamestrings import gameStrings

class FtbWalletBackUpProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FtbWalletBackUpProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_FTB_WALLET_BACKUP, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_FTB_WALLET_BACKUP:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_FTB_WALLET_BACKUP)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_FTB_WALLET_BACKUP)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.protectBtn.addEventListener(events.MOUSE_CLICK, self.onProtectBtnClick)
        TipManager.addTip(self.widget.unProtectBtn, gameStrings.FRIEND_NOTICETEXT)
        TipManager.addTip(self.widget.protectBtn, gameStrings.FTB_WALLET_PROTECT_TIP)

    def onProtectBtnClick(self, *args):
        gameglobal.rds.ui.ftbWalletAgreement.show()
        self.hide()

    def refreshInfo(self):
        if not self.widget:
            return
        p = BigWorld.player()
        walletData = getattr(p, 'ftbWalletData', {})
        self.widget.adressText.text = walletData.get('bcAddress', '')
        privatekey = walletData.get('privateKey', '')
        if privatekey:
            self.widget.privateKeyText.text = base64.decodestring(privatekey)
        else:
            self.widget.privateKeyText.text = base64.decodestring(getattr(p, 'ftbPrivateKey', {}).get('privateKey', ''))
