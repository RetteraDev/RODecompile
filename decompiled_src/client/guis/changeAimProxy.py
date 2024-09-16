#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/changeAimProxy.o
from Scaleform import GfxValue
import gameglobal
import uiConst
from uiProxy import UIProxy

class ChangeAimProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ChangeAimProxy, self).__init__(uiAdapter)
        self.modelMap = {'confirmAim': self.onConfirmAim,
         'getCurSel': self.onGetCurSel,
         'close': self.onClose}
        self.mediator = None

    def _registerMediator(self, widgetId, mediator):
        self.mediator = mediator

    def show(self):
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_CHANGE_AIM)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CHANGE_AIM)

    def onConfirmAim(self, *arg):
        aimId = arg[3][0].GetNumber()
        gameglobal.rds.ui.controlSettingV2.refreshAimCrossId(aimId)
        self.hide()

    def onGetCurSel(self, *arg):
        return GfxValue(gameglobal.rds.ui.controlSettingV2.getAimCrossId())

    def onClose(self, *arg):
        self.hide()
