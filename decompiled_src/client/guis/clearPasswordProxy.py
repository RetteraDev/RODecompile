#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/clearPasswordProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
from uiProxy import UIProxy

class ClearPasswordProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ClearPasswordProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickClose': self.onClickClose,
         'clickConfirm': self.onClickConfirm}
        self.mediator = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_CLEAR_PASSWORD_WIDGET, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_CLEAR_PASSWORD_WIDGET:
            self.mediator = mediator

    def show(self):
        if self.mediator:
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CLEAR_PASSWORD_WIDGET, True, True)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CLEAR_PASSWORD_WIDGET)

    def reset(self):
        super(self.__class__, self).reset()

    def onClickClose(self, *arg):
        self.hide()

    def onClickConfirm(self, *arg):
        selectType = int(arg[3][0].GetNumber())
        if selectType == 0:
            oldPassword = arg[3][1].GetString()
            if not oldPassword:
                return
            BigWorld.player().cell.modifyCipher(oldPassword, '')
            self.hide()
        else:
            self.hide()
            p = BigWorld.player()
            p.base.resetCipher()
            if p.cipherResetTime > 0:
                p.showTopMsg(gameStrings.TEXT_CLEARPASSWORDPROXY_58)
            self.hide()
