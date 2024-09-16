#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/marryRingProxy.o
import BigWorld
import gameglobal
import uiConst
import gametypes
from uiProxy import UIProxy
from data import marriage_config_data as MCD

class MarryRingProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MarryRingProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_MARRY_RING, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MARRY_RING:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MARRY_RING)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_MARRY_RING, True)

    def initUI(self):
        rTime = MCD.data.get('ringWaitingTime', 10)
        BigWorld.callback(rTime, self.continueMarriageScenario)

    def refreshInfo(self):
        if not self.widget:
            return

    def _onTxtBtnClick(self, e):
        if not self.widget:
            return
        self.continueMarriageScenario()

    def continueMarriageScenario(self):
        if not self.widget:
            return
        p = BigWorld.player()
        if p.marriageStage == gametypes.MARRIAGE_STAGE_ENTER_HALL:
            p.continuePlayScenario()
        else:
            p.scenarioStopPlay()
        self.hide()
