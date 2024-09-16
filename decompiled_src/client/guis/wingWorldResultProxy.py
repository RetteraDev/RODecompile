#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/wingWorldResultProxy.o
import BigWorld
import gameglobal
import uiConst
from guis.asObject import ASUtils
from uiProxy import UIProxy

class WingWorldResultProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WingWorldResultProxy, self).__init__(uiAdapter)
        self.widget = None
        self.hadOpened = False
        self.reset()

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        self.widget = widget
        self.initUI()
        self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_WORLD_FAIL)
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_WING_WORLD_WIN)

    def show(self, isWin):
        if self.hadOpened:
            return
        self.hadOpened = True
        if not self.widget:
            gameglobal.rds.sound.playSound(5698 if isWin else 5699)
            self.uiAdapter.loadWidget(uiConst.WIDGET_WING_WORLD_WIN if isWin else uiConst.WIDGET_WING_WORLD_FAIL)

    def initUI(self):
        ASUtils.setHitTestDisable(self.widget, True)

    def refreshInfo(self):
        if not self.widget:
            return

    def clearAll(self):
        self.hadOpened = False
