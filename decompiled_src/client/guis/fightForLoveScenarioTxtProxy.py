#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/fightForLoveScenarioTxtProxy.o
import BigWorld
import gameglobal
import uiConst
from uiProxy import UIProxy

class FightForLoveScenarioTxtProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FightForLoveScenarioTxtProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_FIGHT_FOR_LOVE_SCENARIO_TXT_WIDGET, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_FIGHT_FOR_LOVE_SCENARIO_TXT_WIDGET:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_FIGHT_FOR_LOVE_SCENARIO_TXT_WIDGET)

    def show(self):
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_FIGHT_FOR_LOVE_SCENARIO_TXT_WIDGET, True)

    def initUI(self):
        pass

    def refreshInfo(self):
        if not self.widget:
            return
