#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/playerSelectProxy.o
import gameglobal
from guis import uiConst
from uiProxy import UIProxy
from guis import uiUtils
from guis.ui import unicode2gbk

class PlayerSelectProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(PlayerSelectProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirm': self.onConfirm}
        self.mediator = None
        self.playerList = []
        self.title = ''
        self.okCallback = None
        self.widgetId = uiConst.WIDGET_PLAYER_SELECT
        uiAdapter.registerEscFunc(self.widgetId, self.hide)

    def show(self, playerList, title, okCallback = None):
        self.playerList = playerList
        self.okCallback = okCallback
        self.title = title
        gameglobal.rds.ui.loadWidget(self.widgetId, isModal=True)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(self.widgetId)
        self.mediator = None

    def reset(self):
        self.playerList = []
        self.okCallback = None
        self.title = ''

    def _registerMediator(self, widgetId, mediator):
        if widgetId == self.widgetId:
            self.mediator = mediator
            initData = {'list': self.playerList,
             'title': self.title}
            return uiUtils.dict2GfxDict(initData, True)

    def onConfirm(self, *arg):
        gbId = int(arg[3][0].GetString())
        name = unicode2gbk(arg[3][1].GetString())
        if self.okCallback is not None:
            self.okCallback(gbId, name)
        self.hide()
