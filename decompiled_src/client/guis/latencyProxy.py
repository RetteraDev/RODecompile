#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/latencyProxy.o
import BigWorld
from Scaleform import GfxValue
import gametypes
from uiProxy import UIProxy

class LatencyProxy(UIProxy):
    INTERVAL = 5.0
    POSITION_INTERVAL = 1.0

    def __init__(self, uiAdapter):
        super(LatencyProxy, self).__init__(uiAdapter)
        self.modelMap = {'register': self.onRegister,
         'getLatency': self.onGetLatency,
         'registerCoordinate': self.onRegisterCoordinate,
         'getPosition': self.onGetPosition}
        self.mc = None
        self.coordinateMc = None
        self.callback = None
        self.isCheck = False
        self.isCheckPos = False
        self.callbackPos = None

    def onRegister(self, *arg):
        self.mc = arg[3][0]
        if not self.isCheck:
            self.isCheck = True
        if BigWorld.player().life == gametypes.LIFE_DEAD:
            self.mc.SetVisible(False)

    def onRegisterCoordinate(self, *arg):
        self.coordinateMc = arg[3][0]
        if not self.isCheckPos:
            self.isCheckPos = True
        self.coordinateMc.SetVisible(False)

    def onGetLatency(self, *arg):
        latency = BigWorld.LatencyInfo()
        return GfxValue(latency.value[3])

    def onGetPosition(self, *arg):
        pos = BigWorld.player().position
        return GfxValue('%.f %.f' % (pos[0], pos[2]))

    def sendLatency(self):
        if self.mc:
            self.mc.Invoke('showLatency', self.onGetLatency())

    def sendPosition(self):
        if self.coordinateMc:
            self.coordinateMc.Invoke('showCoordinate', self.onGetPosition())
