#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/inventoryLatchTimeProxy.o
import BigWorld
import gameglobal
import uiConst
import const
from uiProxy import UIProxy
from cdata import game_msg_def_data as GMDD

class InventoryLatchTimeProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(InventoryLatchTimeProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickClose': self.onClickClose,
         'clickConfirm': self.onClickConfirm}
        self.mediator = None
        self.source = const.LATCH_ITEM_INV
        self.page = const.CONT_NO_PAGE
        self.pos = const.CONT_NO_POS
        uiAdapter.registerEscFunc(uiConst.WIDGET_INV_LATCH_TIME, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_INV_LATCH_TIME:
            self.mediator = mediator

    def show(self, source, page, pos):
        if self.mediator:
            return
        self.source = source
        self.page = page
        self.pos = pos
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_INV_LATCH_TIME, True)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_INV_LATCH_TIME)

    def reset(self):
        super(self.__class__, self).reset()
        self.source = const.LATCH_ITEM_INV
        self.page = const.CONT_NO_PAGE
        self.pos = const.CONT_NO_POS

    def onClickClose(self, *arg):
        self.hide()

    def onClickConfirm(self, *arg):
        p = BigWorld.player()
        day = arg[3][0].GetString()
        if not day:
            p.showGameMsg(GMDD.data.LATCH_FORBIDDEN_DAY, ())
            return
        day = int(day)
        if day < 1 or day > 15:
            p.showGameMsg(GMDD.data.LATCH_FORBIDDEN_DAY, ())
            return
        if self.source == const.LATCH_ITEM_STORAGE:
            p.base.latchTimeStorage(self.page, self.pos, day)
        else:
            p.cell.latchTime(self.source, self.page, self.pos, day)
        self.hide()
