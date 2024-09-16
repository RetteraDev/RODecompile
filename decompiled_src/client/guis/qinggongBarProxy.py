#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/qinggongBarProxy.o
import BigWorld
from Scaleform import GfxValue
import gametypes
from uiProxy import UIProxy

class QinggongBarProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(QinggongBarProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerQinggongBar': self.onRegisterQinggongBar}
        self.mc = None
        self.thisMc = None

    def onRegisterQinggongBar(self, *arg):
        self.mc = arg[3][0]
        self.thisMc = arg[3][1]
        p = BigWorld.player()
        if p.life == gametypes.LIFE_DEAD:
            self.thisMc.SetVisible(False)
        if self.mc != None:
            if p.mep == 0:
                p.mep = 100
            self.mc.SetMember('scaleX', GfxValue(float(max(1, p.ep)) / p.mep))
        self.changeQinggongBarState(True, False)

    def setEp(self, ep):
        self.stopTweenEp()
        p = BigWorld.player()
        if self.mc:
            if p.mep == 0:
                p.mep = 100
            self.mc.SetMember('scaleX', GfxValue(float(max(1, p.ep)) / p.mep))

    def tweenEp(self, time, marknum):
        if self.thisMc:
            p = BigWorld.player()
            if p.mep == 0:
                p.mep = 100
            self.thisMc.Invoke('tweenEp', (GfxValue(time), GfxValue(marknum), GfxValue(p.mep)))

    def stopTweenEp(self):
        if self.thisMc:
            self.thisMc.Invoke('stopTweenEp')

    def changeQinggongBarState(self, isFull, inCombat):
        visible = True
        if not inCombat:
            if isFull:
                visible = False
        if self.thisMc:
            self.thisMc.Invoke('changeQinggongBarState', GfxValue(visible))
