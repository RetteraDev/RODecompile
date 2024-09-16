#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/fullScreenFireworkProxy.o
import BigWorld
from guis import uiConst
from guis.uiProxy import UIProxy
from guis.asObject import ASUtils
from data import fireworks_effect_data as FED
from data import intimacy_config_data as ICD

class FullScreenFireworkProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FullScreenFireworkProxy, self).__init__(uiAdapter)
        self.widget = None
        self.swfName = None
        self.icon = None
        self.index = 0

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_FULL_SCREEN_FIREWORK:
            self.widget = widget
            self.initUI()
            self.refreshInfo()

    def reset(self):
        self.swfName = None
        self.icon = None

    def clearWidget(self):
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_FULL_SCREEN_FIREWORK)

    def show(self, fireworksId):
        swfName = FED.data.get(fireworksId, {}).get('fullScreenSwfName', '')
        if not swfName:
            return
        p = BigWorld.player()
        if p.inCombat:
            return
        self.swfName = swfName
        self.index = self.index + 1
        if not self.widget:
            self.uiAdapter.loadWidget(uiConst.WIDGET_FULL_SCREEN_FIREWORK)

    def initUI(self):
        ASUtils.setHitTestDisable(self.widget, True)
        self.icon = self.widget.getInstByClsName('com.scaleform.mmo.core.component.SwfLoader')

    def refreshInfo(self):
        if not self.widget:
            return
        if not self.index:
            self.hide()
            return
        self.index = self.index - 1
        self.widget.canvas.addChild(self.icon)
        self.icon.setCallback(self.swfLoadComp)
        self.icon.visible = True
        self.icon.load('widgets/%s.swf' % self.swfName)
        BigWorld.callback(ICD.data.get('fullScreenFireworkCD', 10), self.callBackFun)

    def swfLoadComp(self, *args):
        pass

    def callBackFun(self):
        if self.index:
            self.widget.canvas.removeChildAt(0)
            self.refreshInfo()
        else:
            self.hide()
