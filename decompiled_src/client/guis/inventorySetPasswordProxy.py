#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/inventorySetPasswordProxy.o
import BigWorld
import gameglobal
import uiConst
from uiProxy import UIProxy
from cdata import game_msg_def_data as GMDD

class InventorySetPasswordProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(InventorySetPasswordProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickClose': self.onClickClose,
         'clickConfirm': self.onClickConfirm,
         'noPassword': self.onNoPassword,
         'inconsistentPassword': self.onInconsistentPassword}
        self.mediator = None
        self.callback = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_INV_SET_PASSWORD, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_INV_SET_PASSWORD:
            self.mediator = mediator

    def show(self, callback = None):
        if self.mediator:
            return
        self.callback = callback
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_INV_SET_PASSWORD, True, True)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_INV_SET_PASSWORD)

    def reset(self):
        super(self.__class__, self).reset()
        self.callback = None

    def onClickClose(self, *arg):
        if self.callback:
            self.callback()
        self.callback = None
        self.hide()

    def onNoPassword(self, *arg):
        BigWorld.player().showGameMsg(GMDD.data.LATCH_INPUT_NOT_PASSWORD, ())

    def onInconsistentPassword(self, *arg):
        BigWorld.player().showGameMsg(GMDD.data.LATCH_INCONSISTENT_PASSWORD, ())

    def onClickConfirm(self, *arg):
        password = arg[3][0].GetString()
        if not password:
            return
        else:
            BigWorld.player().cell.modifyCipher('', password)
            if self.callback:
                self.callback()
            self.hide()
            self.callback = None
            return
