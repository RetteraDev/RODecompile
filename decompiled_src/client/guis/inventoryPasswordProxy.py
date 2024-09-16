#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/inventoryPasswordProxy.o
import BigWorld
import gameglobal
import uiConst
import const
from uiProxy import UIProxy
from cdata import game_msg_def_data as GMDD

class InventoryPasswordProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(InventoryPasswordProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickClose': self.onClickClose,
         'clickConfirm': self.onClickConfirm,
         'noPassword': self.onNoPassword}
        self.mediator = None
        self.source = const.LATCH_ITEM_INV
        self.page = const.CONT_NO_PAGE
        self.pos = const.CONT_NO_POS
        self.isUseForCC = False
        self.isUsedForCipher = False
        self.cancelCallback = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_INV_PASSWORD, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_INV_PASSWORD:
            self.mediator = mediator

    def show(self, source, page, pos, isUseForCC = False, isUsedForCipher = False, cancelCallback = None):
        if self.mediator:
            return
        self.source = source
        self.page = page
        self.pos = pos
        self.isUseForCC = isUseForCC
        self.isUsedForCipher = isUsedForCipher
        self.cancelCallback = cancelCallback
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_INV_PASSWORD, True)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        if self.cancelCallback:
            self.cancelCallback()
        self.cancelCallback = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_INV_PASSWORD)

    def reset(self):
        super(self.__class__, self).reset()
        self.source = const.LATCH_ITEM_INV
        self.page = const.CONT_NO_PAGE
        self.pos = const.CONT_NO_POS

    def onClickClose(self, *arg):
        p = BigWorld.player()
        p.onGetCipherCancelCallback = None
        self.hide()

    def onNoPassword(self, *arg):
        BigWorld.player().showGameMsg(GMDD.data.LATCH_INPUT_NOT_PASSWORD, ())

    def onClickConfirm(self, *arg):
        password = arg[3][0].GetString()
        if not password:
            return
        else:
            p = BigWorld.player()
            if self.isUsedForCipher:
                p.base.validateCipher(password)
            elif self.isUseForCC == False:
                if self.pos != const.CONT_NO_PAGE and self.page != const.CONT_NO_POS:
                    p.cell.unLatchCipher(self.source, self.page, self.pos, password)
            else:
                p.enterCCRoomByPassWord(password)
            self.cancelCallback = None
            self.hide()
            return
