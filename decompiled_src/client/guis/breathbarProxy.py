#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/breathbarProxy.o
import time
import BigWorld
import gameglobal
import uiConst
import const
import ui
from uiProxy import UIProxy
from data import sys_config_data as SCD
CALLBACK_TIME = 0.1

class BreathbarProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(BreathbarProxy, self).__init__(uiAdapter)
        self.mediator = None
        self.nowtick = 0
        self.totaltick = SCD.data.get('mbp', 180)
        self.Mode = uiConst.MODE_Inactive
        self.callbackHandle = None
        self.lastBreathRegenTime = 0

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_BREATHBAR:
            self.mediator = mediator
            self.mc = self.mediator.Invoke('getWidget').GetMember('breathbar')
            self.barRef0 = self.mc.GetMember('breathbar0')
            self.barRef1 = self.mc.GetMember('breathbar1')
            self.maskRef0 = self.barRef0.GetMember('fillMask')
            self.fillRef0 = self.barRef0.GetMember('fill')
            self.shineRef0 = self.barRef0.GetMember('shine')
            self.maskRef1 = self.barRef1.GetMember('fillMask')
            self.fillRef1 = self.barRef1.GetMember('fill')
            self.barRef1.SetVisible(False)
            self.mc.SetVisible(False)
            self.fillStartX = self.fillRef0.GetMember('x').GetNumber()
            self.fillEndX = self.fillRef0.GetMember('width').GetNumber() + self.fillStartX
            self.Mode = uiConst.MODE_Inactive

    @ui.checkWidgetLoaded(uiConst.WIDGET_BREATHBAR)
    def setBreathbar(self, value, isBpChange = True):
        p = BigWorld.player()
        if isBpChange and (value == p._getmbp() and self.nowtick > value or value == 0 and self.nowtick <= value):
            return
        self.nowtick = value
        self.totaltick = p._getmbp()
        self._setPercent(1.0 * value / self.totaltick)
        if self.mediator and value:
            self.mc.SetVisible(True)
            self.mc.SetAlpha(100)
        if self.callbackHandle:
            BigWorld.cancelCallback(self.callbackHandle)
        self.lastBreathRegenTime = time.time()
        self.callbackHandle = BigWorld.callback(CALLBACK_TIME, self._updateBreathbar)

    def _updateBreathbar(self):
        p = BigWorld.player()
        if not p:
            return
        else:
            self.totaltick = p._getmbp()
            timeInterval = time.time() - self.lastBreathRegenTime
            self.lastBreathRegenTime = time.time()
            self.callbackHandle = None
            if p.inSwim == const.DEEPWATER:
                self.nowtick -= timeInterval * p.bpReduce
                if self.nowtick <= 0:
                    self._setPercent(0)
                    return
                pct = 1.0 * self.nowtick / self.totaltick
                self._setPercent(pct)
                self.callbackHandle = BigWorld.callback(CALLBACK_TIME, self._updateBreathbar)
            else:
                self.nowtick += timeInterval * SCD.data.get('bpAdd', 8)
                pct = 1.0 * self.nowtick / self.totaltick
                if pct >= 1:
                    if self.mediator:
                        self.mc.SetVisible(False)
                else:
                    self._setPercent(pct)
                    self.callbackHandle = BigWorld.callback(CALLBACK_TIME, self._updateBreathbar)
            return

    def _setPercent(self, pct):
        if self.mediator:
            self._setPercentBar(pct, self.maskRef0)

    def _setPercentBar(self, pct, maskref):
        maskref.SetXScale((pct + 0.01) * 100)
        sx = (self.fillEndX - self.fillStartX) * (pct + 0.01) + self.fillStartX
        sx = min(self.fillEndX, sx)
        self.shineRef0.SetX(sx)

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_BREATHBAR)
