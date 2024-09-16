#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/waBaoPreProxy.o
import BigWorld
import gameglobal
import uiConst
import uiUtils
from uiProxy import UIProxy

class WaBaoPreProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WaBaoPreProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirm': self.onConfirm}
        self.mediator = None
        self.resItemId = 0
        self.resItemList = []
        self.jumpList = []
        self.hasShowDetail = False
        uiAdapter.registerEscFunc(uiConst.WIDGET_WABAO_PRE, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_WABAO_PRE:
            self.mediator = mediator
            self.refreshInfo()

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_WABAO_PRE)

    def reset(self):
        self.resItemId = 0
        self.resItemList = []
        self.jumpList = []
        if not self.hasShowDetail:
            BigWorld.player().cell.cancelWabaoTurn()
        self.hasShowDetail = False
        if not gameglobal.rds.ui.waBao.mediator:
            BigWorld.player().unlockKey(gameglobal.KEY_POS_UI)

    def show(self, resItemId, resItemList, jumpList):
        self.resItemId = resItemId
        self.resItemList = resItemList
        self.jumpList = jumpList
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_WABAO_PRE, isModal=True)
        p = BigWorld.player()
        p.ap.stopMove()
        p.ap.forceAllKeysUp()
        p.lockKey(gameglobal.KEY_POS_UI, False)

    def refreshInfo(self):
        if self.mediator:
            info = {}
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))

    def onConfirm(self, *arg):
        self.hasShowDetail = True
        gameglobal.rds.ui.waBao.show(self.resItemId, self.resItemList, self.jumpList)
