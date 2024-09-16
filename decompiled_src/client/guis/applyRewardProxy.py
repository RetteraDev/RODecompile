#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/applyRewardProxy.o
import BigWorld
import gameglobal
import uiConst
from uiProxy import UIProxy

class ApplyRewardProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ApplyRewardProxy, self).__init__(uiAdapter)
        self.modelMap = {'applyReward': self.onApplyReward}
        self.mediator = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_APPLY_REWARD:
            self.mediator = mediator

    def refresh(self):
        pass

    def show(self):
        if self.mediator:
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_APPLY_REWARD)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_APPLY_REWARD)

    def onASWidgetClose(self, *arg):
        super(self.__class__, self).clearWidget()
        self.hide()

    def onApplyReward(self, *arg):
        code = arg[3][0].GetString()
        if code == '':
            return
        p = BigWorld.player()
        p.base.applyRewardByCode(code.strip())
        self.hide()
