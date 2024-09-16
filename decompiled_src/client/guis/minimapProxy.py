#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/minimapProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import formula
import const
import gamelog
from uiProxy import UIProxy

class MinimapProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(MinimapProxy, self).__init__(uiAdapter)
        self.maplv = 1
        self.modelMap = {'setMinimapScale': self.onSetMinimapScale,
         'registerMinimap': self.onRegisterMinimap,
         'NotifySignal': self.onNotifySignal}
        self.handler = None

    def onRegisterMinimap(self, *arg):
        gamelog.debug('onRegisterMinimap')
        self.handler = arg[3][0]
        spaceNo = BigWorld.player().spaceNo
        fbNo = formula.getFubenNo(spaceNo)
        if formula.whatFubenType(fbNo) not in const.FB_TYPE_BATTLE_FIELD:
            gameglobal.rds.minimap.hide(0)
        else:
            self.show(False)

    def show(self, bVisible):
        if self.handler != None:
            self.handler.SetVisible(bVisible)

    def onSetMinimapScale(self, *arg):
        number = arg[3][0].GetNumber()
        if number < self.maplv:
            gameglobal.rds.minimap.zoomOut()
        else:
            gameglobal.rds.minimap.zoomIn()
        self.maplv = number
        gamelog.debug('zfminimap scale:', arg[3][0].GetNumber())

    def onNotifySignal(self, *arg):
        x = arg[3][0].GetNumber()
        y = arg[3][1].GetNumber()
        gamelog.debug('onNotifySignal', x, y)
        BigWorld.player().notifySignal(x, y)

    def setAltState(self, state):
        self.handler.Invoke('setAltState', GfxValue(state))
