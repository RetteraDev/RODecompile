#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/roleLoadProxy.o
from Scaleform import GfxValue
import gameglobal
import uiConst
from uiProxy import DataProxy

class RoleLoadProxy(DataProxy):

    def __init__(self, uiAdapter):
        super(RoleLoadProxy, self).__init__(uiAdapter)
        self.modelMap = {}
        self.reset()

    def reset(self):
        self.isShow = False
        self.mediator = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_ROLE_LOADING:
            self.mediator = mediator
            if not self.isShow:
                self.mediator.Invoke('setVisible', GfxValue(self.isShow))

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ROLE_LOADING)

    def show(self, isShow = True):
        self.isShow = isShow
        if self.mediator:
            self.mediator.Invoke('setVisible', GfxValue(isShow))
        elif isShow:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ROLE_LOADING)
