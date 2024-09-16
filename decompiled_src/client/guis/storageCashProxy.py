#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/storageCashProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
from uiProxy import UIProxy
from guis import uiUtils

class StorageCashProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(StorageCashProxy, self).__init__(uiAdapter)
        self.modelMap = {'initData': self.onInitData,
         'clickClose': self.onClickClose,
         'clickConfirm': self.onClickConfirm}
        self.mediator = None
        self.type = 0
        uiAdapter.registerEscFunc(uiConst.WIDGET_STORAGE_CASH, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_STORAGE_CASH:
            self.mediator = mediator

    def show(self, type):
        if self.mediator == None:
            self.type = type
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_STORAGE_CASH, True)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_STORAGE_CASH)

    def reset(self):
        self.mediator = None

    def onClickClose(self, *arg):
        self.hide()

    def onInitData(self, *arg):
        p = BigWorld.player()
        info = {}
        if self.type == 0:
            info['modeText'] = gameStrings.TEXT_STORAGECASHPROXY_43
            info['cash'] = p.cash
        else:
            info['modeText'] = gameStrings.TEXT_STORAGECASHPROXY_46
            info['cash'] = p.storageCash
        return uiUtils.dict2GfxDict(info, True)

    def onClickConfirm(self, *arg):
        cash = int(arg[3][0].GetNumber())
        if self.type == 0:
            gameglobal.rds.ui.storage._transferCashToStorage(cash)
        else:
            gameglobal.rds.ui.storage._drawCashFromStorage(cash)
        self.hide()
