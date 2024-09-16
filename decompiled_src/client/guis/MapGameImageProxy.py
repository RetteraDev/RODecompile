#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/MapGameImageProxy.o
import BigWorld
import uiConst
from uiProxy import UIProxy

class MapGameImageProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MapGameImageProxy, self).__init__(uiAdapter)
        self.widget = None
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_MAP_GAME_IMAGE, self.hide)

    def reset(self):
        pass

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_MAP_GAME_IMAGE:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_MAP_GAME_IMAGE)

    def show(self):
        if BigWorld.player().mapGameGraveEndFlashState:
            return
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_MAP_GAME_IMAGE)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        BigWorld.player().cell.mapGameGraveStopFlash()

    def refreshInfo(self):
        if not self.widget:
            return
