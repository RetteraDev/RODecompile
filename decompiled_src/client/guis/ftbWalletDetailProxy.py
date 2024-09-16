#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/ftbWalletDetailProxy.o
from gamestrings import gameStrings
import BigWorld
import time
import gametypes
import gameglobal
import uiConst
from gamestrings import gameStrings
from uiProxy import UIProxy

class FtbWalletDetailProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FtbWalletDetailProxy, self).__init__(uiAdapter)
        self.widget = None
        self.itemData = {}
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_FTB_WALLET_DETAIL, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_FTB_WALLET_DETAIL:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_FTB_WALLET_DETAIL)

    def show(self, itemData):
        self.itemData = itemData
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_FTB_WALLET_DETAIL)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.widget.coinIcon.bonusType = gametypes.ICON_FRAME_FTB

    def refreshInfo(self):
        if not self.widget:
            return
        data = self.itemData
        self.widget.descText.text = data.tradeDescription
        if data.onChain:
            self.widget.stateText.text = gameStrings.FTB_WALLET_DEAL_STATE_OK_RAW
        else:
            self.widget.stateText.text = gameStrings.FTB_WALLET_DEAL_STATE_CONFIRM_RAW
        self.widget.sendAdress.text = data.fromAddress
        self.widget.recvAdress.text = data.toAddress
        timeArray = time.localtime(int(data.operationTime) / 1000)
        self.widget.timeText.text = str(time.strftime(gameStrings.TEXT_FTBWALLETDETAILPROXY_53, timeArray))
        self.widget.idText.text = data.tnxSerialNum
        self.widget.moneyText.text = '%.07f' % (data.transactionValue,)
        if data.transactionValue > 0:
            self.widget.moneyTitle.text = gameStrings.FTB_WALLET_GET
        else:
            self.widget.moneyTitle.text = gameStrings.FTB_WALLET_SPEND
