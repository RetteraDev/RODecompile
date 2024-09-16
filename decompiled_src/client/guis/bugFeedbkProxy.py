#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/bugFeedbkProxy.o
import BigWorld
import gameglobal
from guis import uiConst
from uiProxy import UIProxy

class BugFeedbkProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BugFeedbkProxy, self).__init__(uiAdapter)
        self.modelMap = {'closeWidget': self.onCloseWidget,
         'openUrl': self.onOpenUrl}
        self.mediator = None
        self.widgetId = uiConst.WIDGET_BUG_FEEDBK
        uiAdapter.registerEscFunc(self.widgetId, self.hide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == self.widgetId:
            self.mediator = mediator

    def show(self):
        gameglobal.rds.ui.loadWidget(self.widgetId)

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(self.widgetId)
        self.mediator = None

    def reset(self):
        pass

    def onCloseWidget(self, *arg):
        self.clearWidget()

    def onOpenUrl(self, *arg):
        url = 'tianyu.163.com'
        if arg[3][0] is not None:
            url = arg[3][0].GetString()
        BigWorld.openUrl(url)
