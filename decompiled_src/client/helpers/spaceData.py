#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/spaceData.o
import BigWorld
import const
import gametypes
import formula
import clientUtils
from callbackHelper import Functor
from gameclass import Singleton
from data import sys_config_data as SCD

def instance():
    return SpaceData.getInstance()


XINGJI_RESET_RULE = {(0.0, 3.0): (0.0, 5.0),
 (3.0, 6.1): (5.0, 7.0),
 (6.1, 17.9): (7.0, 17.0),
 (17.9, 21.0): (17.0, 19.0),
 (21.0, 24.0): (19.0, 24.0)}

class SpaceData(object):
    __metaclass__ = Singleton

    def _setTimeOfDay(self, startTime, endTime, interval, step):
        toTime = step * (endTime - startTime) / interval + startTime
        if toTime > endTime:
            toTime = endTime
        toTimeStr = clientUtils.timeIntToStr(toTime)
        BigWorld.timeOfDay(toTimeStr)
        if getattr(self, 'timeOfDayCallback', None):
            BigWorld.cancelCallback(self.timeOfDayCallback)
        if toTime == endTime:
            return
        self.timeOfDayCallback = BigWorld.callback(1, Functor(self._setTimeOfDay, startTime, endTime, interval, step + 1))

    def __onSetSpaceTimeOfDayData(self, data):
        if not data:
            return
        args = data.split('#')
        timeType = args[0]
        if timeType == gametypes.SPACE_TIME_OF_DAY_VARIATION:
            startTimeStr, endTimeStr, interval = args[1:]
            startTime = clientUtils.timeStrToInt(startTimeStr)
            endTime = clientUtils.timeStrToInt(endTimeStr)
            self._setTimeOfDay(startTime, endTime, int(interval), 0)
        elif timeType == gametypes.SPACE_TIME_OF_DAY_FIXED:
            if getattr(self, 'timeOfDayCallback', None):
                BigWorld.cancelCallback(self.timeOfDayCallback)
                self.timeOfDayCallback = None
            endTimeStr = args[1]
            BigWorld.timeOfDay(endTimeStr)

    def __onShowFbRoute(self, data):
        if not data:
            return
        args = data.split('#')
        showRouteId = int(args[0])
        routes = eval(args[1])
        hideRouteId = int(args[2])
        routeTTL = int(args[3])
        p = BigWorld.player()
        p.showFbRoute(showRouteId, routes, hideRouteId, True, routeTTL)

    FUNCTION_MAP = {const.SPACE_KEY_FB_TIME_OF_DAY: __onSetSpaceTimeOfDayData,
     const.SPACE_KEY_SHOW_ROUTE: __onShowFbRoute}
    DAY_PERIOD_CALLBACK_INTERVAL = 0.0

    def __init__(self):
        self.data = {}
        self.periodCallback = None

    def set(self, spaceID, key, data):
        if self.data.has_key(spaceID):
            self.data[spaceID].update({key: data})
        else:
            self.data[spaceID] = {key: data}
        if spaceID == BigWorld.player().spaceID:
            self.__onSet(spaceID, key, data)

    def __onSet(self, spaceID, key, data):
        func = self.FUNCTION_MAP.get(key, None)
        if func != None:
            func(self, data)

    def get(self, spaceID, key):
        try:
            return self.data[spaceID][key]
        except:
            return None

    def getBySpaceID(self, spaceID):
        try:
            return self.data[spaceID]
        except:
            return None

    def enterSpace(self, spaceID):
        p = BigWorld.player()
        if not p or not p.inWorld:
            return
        if hasattr(BigWorld, 'setSecondsPerGameHour'):
            BigWorld.setSecondsPerGameHour(formula.getSecondsPerXingJiHour())
        self._setDayPeroid()
        spaceData = self.getBySpaceID(spaceID)
        if not spaceData:
            return
        for key, data in spaceData.iteritems():
            self.__onSet(spaceID, key, data)

    def _setDayPeroid(self):
        player = BigWorld.player()
        if not player or not player.inWorld:
            return
        spaceNo = player.spaceNo
        if player.inFuben():
            spaceNo = formula.getFubenNo(spaceNo)
        elif player.inMLSpace():
            spaceNo = formula.getMLNo(spaceNo)
        elif player.inGuildSpace():
            spaceNo = formula.getGuildSceneNo(spaceNo)
        elif formula.spaceInHome(spaceNo):
            spaceNo = formula.getMapId(spaceNo)
        elif formula.spaceInAnnalReplay(spaceNo):
            spaceNo = formula.getMapId(spaceNo)
        elif formula.spaceInWingCity(spaceNo):
            spaceNo = formula.getMapId(spaceNo)
        diurnal = const.spaceDict[spaceNo].get('diurnal', 0)
        self.stopDiurnalChange()
        if diurnal > 0:
            BigWorld.setTime(self.resetXingJiTime(formula.getXingJiTime()))
            self.periodCallback = BigWorld.callback(self.DAY_PERIOD_CALLBACK_INTERVAL, self._setDayPeroid)

    def resetXingJiTime(self, xingjiTime):
        resetRule = SCD.data.get('xingjiDisplayRule', XINGJI_RESET_RULE)
        for (minTime, maxTime), (minOrginTime, maxOrginTime) in resetRule.iteritems():
            if minTime <= xingjiTime <= maxTime:
                return (xingjiTime - minTime) * (maxOrginTime - minOrginTime) / (maxTime - minTime) + minOrginTime

        return xingjiTime

    def stopDiurnalChange(self):
        if self.periodCallback is not None:
            BigWorld.cancelCallback(self.periodCallback)
            self.periodCallback = None

    def setDiurnalChangeParam(self, period, interval = 0.0):
        player = BigWorld.player()
        spaceNo = player.spaceNo
        if player.inFuben():
            spaceNo = formula.getFubenNo(spaceNo)
        elif player.inMLSpace():
            spaceNo = formula.getMLNo(spaceNo)
        self.DAY_PERIOD_CALLBACK_INTERVAL = interval
        self._setDayPeroid()


instance()
