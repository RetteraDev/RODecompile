#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/surrenderProxy.o
import BigWorld
import gameglobal
from guis import uiConst
from uiProxy import UIProxy

class SurrenderProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(SurrenderProxy, self).__init__(uiAdapter)
        self.modelMap = {'clickSurrenderBtn': self.onClickSurrenderBtn}
        self.mediator = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_SURRENDER_WIDGET:
            self.mediator = mediator

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_SURRENDER_WIDGET)
        if gameglobal.rds.ui.isHideAllUI():
            gameglobal.rds.ui.setWidgetVisible(uiConst.WIDGET_SURRENDER_WIDGET, True)

    def hide(self, destroy = True):
        self.clearWidget()
        if destroy:
            self.reset()

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_SURRENDER_WIDGET)
        self.mediator = None

    def reset(self):
        super(self.__class__, self).reset()

    def onClickSurrenderBtn(self, *arg):
        p = BigWorld.player()
        p.confirmQieCuoSurrender()
