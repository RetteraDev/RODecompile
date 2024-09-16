#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/continuousHitProxy.o
import Sound
import BigWorld
from Scaleform import GfxValue
import gameglobal
import uiConst
import formula
import ui
from uiProxy import UIProxy
from guis import events

class ContinuousHitProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ContinuousHitProxy, self).__init__(uiAdapter)
        self.modelMap = {}
        self.mediator = None
        self.killMediaotr = None
        self.demageHit = 0
        self.healHit = 0
        self.kill = 0
        self.addEvent(events.EVENT_PLAYER_SPACE_NO_CHANGED, self.onSpaceNoChanged, 0, True)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_CONTINUOUS_HIT:
            self.mediator = mediator
        elif widgetId == uiConst.WIDGET_CONTINUOUS_KILL:
            self.killMediaotr = mediator
            return GfxValue(self.kill)

    @ui.checkWidgetLoaded(uiConst.WIDGET_CONTINUOUS_HIT)
    def hit(self, type, num):
        if self.mediator != None:
            Sound.playSimple('hit')
            self.mediator.Invoke('setHit', (GfxValue(type), GfxValue(num)))

    def endHit(self, type):
        if self.mediator != None:
            self.mediator.Invoke('endHit', GfxValue(type))

    def showCombokill(self, num):
        if self.killMediaotr:
            self.killMediaotr.Invoke('setHit', GfxValue(num))
        else:
            self.kill = num
            self.uiAdapter.loadWidget(uiConst.WIDGET_CONTINUOUS_KILL)

    def hideCombokill(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_CONTINUOUS_KILL)
        self.killMediaotr = None

    def clearWidget(self):
        super(self.__class__, self).clearWidget()
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CONTINUOUS_HIT)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_CONTINUOUS_KILL)

    def onSpaceNoChanged(self):
        if not formula.inWorldWar(BigWorld.player().spaceNo):
            self.hideCombokill()
