#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/inventoryResetPasswordProxy.o
import BigWorld
import gameglobal
import uiConst
from uiProxy import UIProxy
from cdata import game_msg_def_data as GMDD

class InventoryResetPasswordProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(InventoryResetPasswordProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickClose': self.onClickClose,
         'clickConfirm': self.onClickConfirm,
         'noPassword': self.onNoPassword,
         'inconsistentPassword': self.onInconsistentPassword}
        self.mediator = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_INV_RESET_PASSWORD, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_INV_RESET_PASSWORD:
            self.mediator = mediator

    def show(self):
        if self.mediator:
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_INV_RESET_PASSWORD, True, True)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_INV_RESET_PASSWORD)

    def reset(self):
        super(self.__class__, self).reset()

    def onClickClose(self, *arg):
        self.hide()

    def onNoPassword(self, *arg):
        BigWorld.player().showGameMsg(GMDD.data.LATCH_INPUT_NOT_PASSWORD, ())

    def onInconsistentPassword(self, *arg):
        BigWorld.player().showGameMsg(GMDD.data.LATCH_INCONSISTENT_PASSWORD, ())

    def onClickConfirm(self, *arg):
        newPassword = arg[3][0].GetString()
        oldPassword = arg[3][1].GetString()
        if not newPassword:
            BigWorld.player().showGameMsg(GMDD.data.LATCH_INPUT_NOT_PASSWORD, ())
            return
        if not oldPassword:
            return
        BigWorld.player().cell.modifyCipher(oldPassword, newPassword)
        self.hide()
