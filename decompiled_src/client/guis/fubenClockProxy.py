#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/fubenClockProxy.o
import BigWorld
from Scaleform import GfxValue
import gameglobal
import gametypes
import const
import utils
from uiProxy import UIProxy
from guis import uiConst

class FubenClockProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(FubenClockProxy, self).__init__(uiAdapter)
        self.modelMap = {'initClock': self.onInitClock,
         'isInSchoolTop': self.onIsInSchoolTop,
         'getLeftTime': self.onGetLeftTime}
        self.reset()
        self.clockMediator = None
        self.secondrayClockMed = None

    def onInitClock(self, *arg):
        clockType = int(arg[3][0].GetNumber())
        ret = self.movie.CreateArray()
        ret.SetElement(0, GfxValue(self.isCountDown[clockType]))
        ret.SetElement(1, GfxValue(self.time[clockType]))
        ret.SetElement(2, GfxValue(self.getStartOnShow(clockType)))
        return ret

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_FUBEN_CLOCK:
            self.clockMediator = mediator
        elif widgetId == uiConst.WIDGET_FUBEN_SECONDARY_CLOCK:
            self.secondrayClockMed = mediator

    def clearWidget(self):
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FUBEN_CLOCK)
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FUBEN_SECONDARY_CLOCK)
        self.clockMediator = None
        self.secondrayClockMed = None

    def show(self, *args):
        self.showClock(uiConst.FUBEN_MAIN_CLOCK, *args)

    def hideClock(self, clockType):
        if clockType == uiConst.FUBEN_MAIN_CLOCK:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FUBEN_CLOCK)
            self.clockMediator = None
        elif clockType == uiConst.FUBEN_SECONDARY_CLOCK:
            gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_FUBEN_SECONDARY_CLOCK)
            self.secondrayClockMed = None

    def showClock(self, clockType, isCountDown = True, time = 0, startOnShow = True):
        p = BigWorld.player()
        if p.mapID == const.FB_NO_SCHOOL_TOP_MATCH:
            time = utils.getNow() + time
        self.isCountDown[clockType] = isCountDown
        self.time[clockType] = 0 if time == None else time
        self.startOnShow[clockType] = startOnShow
        if clockType == uiConst.FUBEN_MAIN_CLOCK:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FUBEN_CLOCK)
        elif clockType == uiConst.FUBEN_SECONDARY_CLOCK:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_FUBEN_SECONDARY_CLOCK)

    def reset(self):
        self.isCountDown = [True, True]
        self.time = [0, 0]
        self.startOnShow = [True, True]

    def stopTimer(self, clockType, time = -1):
        if self.getMediatorByType(clockType) != None:
            self.getMediatorByType(clockType).Invoke('stopTimer', GfxValue(time))

    def setTimer(self, clockType, isCountDown, time, start = True):
        arr = self.movie.CreateArray()
        arr.SetElement(0, GfxValue(isCountDown))
        arr.SetElement(1, GfxValue(time))
        arr.SetElement(2, GfxValue(start))
        if self.getMediatorByType(clockType) != None:
            self.getMediatorByType(clockType).Invoke('setTimer', arr)

    def getIsCountDown(self, clockType):
        return self.isCountDown[clockType]

    def getTime(self, clockType):
        return self.time[clockType]

    def getStartOnShow(self, clockType):
        return self.startOnShow[clockType]

    def getMediatorByType(self, clockType):
        if clockType == uiConst.FUBEN_MAIN_CLOCK:
            return self.clockMediator
        elif clockType == uiConst.FUBEN_SECONDARY_CLOCK:
            return self.secondrayClockMed
        else:
            return None

    def onIsInSchoolTop(self, *args):
        p = BigWorld.player()
        return GfxValue(p.mapID == const.FB_NO_SCHOOL_TOP_MATCH)

    def onGetLeftTime(self, *args):
        p = BigWorld.player()
        if getattr(p, 'schoolTopMatchStage', None) == gametypes.SCHOOL_TOP_MATCH_PHASE_PREPARE:
            leftTime = max(0, p.schoolTopTimeStamp - utils.getNow())
        else:
            leftTime = max(0, self.getTime(uiConst.FUBEN_MAIN_CLOCK) - utils.getNow())
        return GfxValue(leftTime)
