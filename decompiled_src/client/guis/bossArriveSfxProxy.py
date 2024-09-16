#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/bossArriveSfxProxy.o
import BigWorld
import gameglobal
import uiConst
from uiProxy import UIProxy
from guis.asObject import ASUtils
SFX_STOP_FRAME = 90

class BossArriveSfxProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BossArriveSfxProxy, self).__init__(uiAdapter)
        self.widget = None
        uiAdapter.registerEscFunc(uiConst.WIDGET_BOSS_ARRIVE_SFX, self.hide)

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_BOSS_ARRIVE_SFX:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def show(self):
        if self.widget:
            self.refreshInfo()
            return
        gameglobal.rds.ui.loadWidget(uiConst.WIDGET_BOSS_ARRIVE_SFX)

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_BOSS_ARRIVE_SFX)

    def reset(self):
        pass

    def initUI(self):
        ASUtils.setHitTestDisable(self.widget, True)

    def refreshInfo(self):
        if not self.widget:
            return
        ASUtils.callbackAtFrame(self.widget.bossSfx, SFX_STOP_FRAME, self.sfxFinished)

    def sfxFinished(self, *arg):
        self.hide()
