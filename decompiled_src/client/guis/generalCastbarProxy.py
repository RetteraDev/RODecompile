#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/generalCastbarProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiConst
import ui
from ui import gbk2unicode
from uiProxy import UIProxy
ANIM_INTERVAL = 0.02

class GeneralCastbarProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(GeneralCastbarProxy, self).__init__(uiAdapter)
        self.modelMap = {}
        self.mediator = None
        self.nowtick = 0
        self.lefttick = 0
        self.Mode = uiConst.MODE_Inactive
        self.pct = 0
        self.func = None
        self.callbackHandle = None

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_GENERAL_CAST:
            self.mediator = mediator
            self.allMc = self.mediator.Invoke('getWidget')
            self.mc = self.allMc.GetMember('castbar')
            self.barRef0 = self.mc.GetMember('castbar0')
            self.barRef1 = self.mc.GetMember('castbar1')
            self.maskRef0 = self.barRef0.GetMember('fillMask')
            self.fillRef0 = self.barRef0.GetMember('fill')
            self.shineRef0 = self.barRef0.GetMember('shine')
            self.effectRef = self.mc.GetMember('shine')
            self.textRef0 = self.barRef0.GetMember('castName')
            self.barInToRef0 = self.fillRef0.GetMember('bar')
            self.maskRef1 = self.barRef1.GetMember('fillMask')
            self.fillRef1 = self.barRef1.GetMember('fill')
            self.barRef1.SetVisible(False)
            self.mc.SetVisible(False)
            self.fillStartX = self.fillRef0.GetMember('x').GetNumber()
            self.fillEndX = self.fillRef0.GetMember('width').GetNumber() + self.fillStartX
            self.Mode = uiConst.MODE_Inactive

    @ui.checkWidgetLoaded(uiConst.WIDGET_GENERAL_CAST)
    def startGeneralCastBar(self, time, func = None, useText = ''):
        if self.callbackHandle:
            BigWorld.cancelCallback(self.callbackHandle)
        self.func = func
        self.totaltick = BigWorld.time() + time
        self.starttick = BigWorld.time()
        self.nowtick = BigWorld.time()
        self.textRef0.SetText(gbk2unicode(useText))
        self.barInToRef0.GotoAndStop('bar0')
        self.effectRef.SetVisible(False)
        self.shineRef0.SetVisible(True)
        self._setPercent(0, 0)
        self.fadeOutUseTime = 1000
        self.fadeOutHoldTime = ANIM_INTERVAL
        self.callbackHandle = BigWorld.callback(ANIM_INTERVAL, self._updateGeneralCastBar)

    def _updateGeneralCastBar(self):
        self.nowtick = BigWorld.time()
        self.lefttick = self.totaltick - self.nowtick
        if self.lefttick > 0 and self.Mode != uiConst.MODE_Active:
            self._setPercent(0, self.lefttick)
            self.mc.SetVisible(True)
            self.mc.SetAlpha(100)
            self.Mode = uiConst.MODE_Active
            self.callbackHandle = BigWorld.callback(ANIM_INTERVAL, self._updateGeneralCastBar)
            return
        else:
            if self.Mode == uiConst.MODE_FadeOutHold:
                if self.nowtick - self.fadetick > ANIM_INTERVAL:
                    self.Mode = uiConst.MODE_FadeOut
                    self.fadetick = BigWorld.time()
                self.callbackHandle = BigWorld.callback(ANIM_INTERVAL, self._updateGeneralCastBar)
            elif self.Mode == uiConst.MODE_FadeOut:
                fadePct = (self.nowtick - self.fadetick) * 1000 / self.fadeOutUseTime
                if fadePct > 1:
                    self.Mode = uiConst.MODE_Inactive
                    self.mc.SetVisible(False)
                else:
                    self.mc.SetAlpha((1 - fadePct) * 100)
                    self.callbackHandle = BigWorld.callback(ANIM_INTERVAL, self._updateGeneralCastBar)
                if self.func is not None:
                    self.func()
            if self.lefttick > 0:
                self.pct = self._getPct()
                self._setPercent(self.pct, self.lefttick)
                self.callbackHandle = BigWorld.callback(ANIM_INTERVAL, self._updateGeneralCastBar)
            elif self.Mode == uiConst.MODE_Active:
                self._setPercent(1, self.lefttick)
                self.Mode = uiConst.MODE_FadeOut
                self.effectRef.SetVisible(True)
                self.barInToRef0.GotoAndStop('bar3')
                self.shineRef0.SetVisible(False)
                self.callbackHandle = BigWorld.callback(ANIM_INTERVAL, self._updateGeneralCastBar)
                self.fadetick = BigWorld.time()
            return

    def _getPct(self):
        return (self.nowtick - self.starttick) / (self.totaltick - self.starttick)

    def _setPercent(self, pct, leftTicks):
        self._setPercentBar(pct, self.maskRef0)

    def _setPercentBar(self, pct, maskref):
        maskref.SetXScale((pct + 0.01) * 100)
        sx = (self.fillEndX - self.fillStartX) * (pct + 0.01) + self.fillStartX
        sx = min(self.fillEndX, sx)
        if sx < 17 or pct == 1:
            self.shineRef0.SetVisible(False)
        else:
            self.shineRef0.SetVisible(True)
        self.shineRef0.SetX(sx)

    @ui.checkWidgetLoaded(uiConst.WIDGET_GENERAL_CAST)
    def notifyCastInterrupt(self):
        self.textRef0.SetText(gbk2unicode(gameStrings.TEXT_GENERALCASTBARPROXY_147))
        self._setPercent(1, self.lefttick)
        self.barInToRef0.GotoAndStop('bar1')
        self.fadeOutUseTime = 500
        self.fadeOutHoldTime = 1
        self.Mode = uiConst.MODE_FadeOutHold
        self.totaltick = BigWorld.time()
        self.fadetick = BigWorld.time()
        self.shineRef0.SetVisible(False)
        if self.callbackHandle:
            BigWorld.cancelCallback(self.callbackHandle)
        self.callbackHandle = BigWorld.callback(1, self._updateGeneralCastBar)

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_GENERAL_CAST)
