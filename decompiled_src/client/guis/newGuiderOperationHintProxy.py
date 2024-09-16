#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/newGuiderOperationHintProxy.o
import BigWorld
import uiConst
import gameglobal
from uiProxy import UIProxy
from data import sys_config_data as SCD

class NewGuiderOperationHintProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(NewGuiderOperationHintProxy, self).__init__(uiAdapter)
        self.modelMap = {'toggleOp': self.onToggleOp}
        self.mediator = None
        self.isPlayedOnce = False

    def reset(self):
        self.mediator = None
        self.isPlayedOnce = False

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_NEW_GUIDER_OPERATION_HINT:
            self.mediator = mediator

    def onToggleOp(self, *args):
        if not gameglobal.rds.ui.newGuiderOpera.mediator:
            gameglobal.rds.ui.newGuiderOpera.show()
        else:
            gameglobal.rds.ui.newGuiderOpera.hide()

    def playEffect(self):
        if self.mediator:
            if not self.isPlayedOnce:
                self.mediator.Invoke('playEffect', ())
                self.isPlayedOnce = True

    def clearWidget(self):
        self.mediator = None

    def showOrHide(self):
        needShowLv = SCD.data.get('Op_needShow_lv', 30)
        if needShowLv > BigWorld.player().lv:
            if not self.mediator:
                gameglobal.rds.ui.loadWidget(uiConst.WIDGET_NEW_GUIDER_OPERATION_HINT)
        elif self.mediator:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_NEW_GUIDER_OPERATION_HINT)
            self.mediator = None
