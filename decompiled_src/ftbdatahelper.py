#Embedded file name: /WORKSPACE/data/entities/client/helpers/ftbdatahelper.o
import BigWorld
import gameglobal
import utils
from helpers.eventDispatcher import Event
from helpers import tickManager
from guis import events

class DigEventNode(dict):
    START = 0
    STOP = 1
    EARNING = 2

    def __init__(self, type, timeStamp, value):
        super(DigEventNode, self).__init__()
        self['type'] = type
        self['time'] = timeStamp
        self['value'] = value


class DigEventList(list):

    def addEvent(self, type, value = 0, specifiedTime = None):
        eventTime = specifiedTime if specifiedTime else utils.getNow()
        if type == DigEventNode.START or type == DigEventNode.STOP:
            self.append(DigEventNode(type, eventTime, 0))
        elif type == DigEventNode.EARNING:
            self.append(DigEventNode(type, eventTime, value))
        evt = Event(events.EVNET_FTB_EVENTLIST_CHANGE, self)
        gameglobal.rds.ui.dispatchEvent(evt)


class DigStartRecorder(object):

    def setDuration(self, value):
        if self._duration != value:
            self._duration = value
            if self._onTimeChanged:
                self._onTimeChanged()

    def getDuration(self):
        return max(0, self._duration)

    duration = property(getDuration, setDuration)

    def __init__(self):
        self._startTime = 0
        self._duration = 0
        self._tickId = -1
        self._onTimeChanged = None

    def start(self, onTimeChange, specifiedTime = None):
        self._startTime = specifiedTime if specifiedTime else utils.getNow()
        self.duration = 0
        self._onTimeChanged = onTimeChange
        if self._tickId != -1:
            tickManager.stopTick(self._tickId)
        self._tickId = tickManager.addTick(1, self.__timer)

    def stop(self):
        if self._tickId != -1:
            tickManager.stopTick(self._tickId)
        self.duration = 0
        self._onTimeChanged = None

    def __timer(self):
        self.duration = self.duration + 1


class FtbDataHelper(object):
    guideDigPower = property(lambda self: self._guideDigPower)
    ephemeralPower = property(lambda self: self._ephemeralPower)
    isDigging = property(lambda self: self._isDigging)
    ftbAddr = property(lambda self: self._ftbAddr)
    licenseNo = property(lambda self: self._licenseNo)
    hasSigned = property(lambda self: self._hasSigned)
    ftbSite = property(lambda self: self._ftbSite)
    totalNowEarning = property(lambda self: self._totalNowEarning)
    nowEarning = property(lambda self: self._nowEarning)
    totalEarning = property(lambda self: self._totalEarning)
    yaojingTicket = property(lambda self: self._yaojingTicket)
    leftDigingTime = property(lambda self: self._genLeftDigingTime())
    weekTimeOfConsumed = property(lambda self: self._weekTimeOfConsumed)
    digEventList = property(lambda self: self._digEventList)
    totalOutput = property(lambda self: self._totalOutput)
    dailyOutput = property(lambda self: self._dailyOutput)
    digDuration = property(lambda self: self._digTimeRecorder.duration)
    hasVipRewardTaken = property(lambda self: self._hasVipRewardTaken)
    hasLicense = property(lambda self: self._hasLicense)
    hasHome = property(lambda self: self._hasHome)
    historyTaskList = property(lambda self: self._historyTaskList)
    todayTaskList = property(lambda self: self._todayTaskList)
    digStateSwitch = property(lambda self: self._digStateSwitch)
    availDigTime = property(lambda self: self._availTime)
    isAutoDig = property(lambda self: self._isAutoDig)

    def __init__(self):
        self._isDigging = False
        self._guideDigPower = 0
        self._ephemeralPower = 0
        self._ftbAddr = ''
        self._licenseNo = 0L
        self._hasSigned = False
        self._ftbSite = 0
        self._totalNowEarning = 0.0
        self._nowEarning = 0.0
        self._totalEarning = 0.0
        self._yaojingTicket = 0.0
        self._lastDigingTime = utils.getNow()
        self._weekTimeOfConsumed = 0
        self._availTime = 0
        self._digEventList = DigEventList()
        self._totalOutput = 0.0
        self._dailyOutput = 0.0
        self._digTimeRecorder = DigStartRecorder()
        self._hasVipRewardTaken = False
        self._hasLicense = False
        self._hasHome = False
        self._historyTaskList = []
        self._todayTaskList = []
        self._digStateSwitch = False
        self._isAutoDig = False

    def clear(self):
        self._digTimeRecorder.stop()
        self._digEventList = DigEventList()

    def updateDigPower(self, value):
        self._guideDigPower = value
        evt = Event(events.EVNET_FTB_DIGPOWER_CHANGE)
        gameglobal.rds.ui.dispatchEvent(evt)

    def updateEphemeralPower(self, value):
        self._ephemeralPower = value
        evt = Event(events.EVNET_FTB_DIGPOWER_CHANGE)
        gameglobal.rds.ui.dispatchEvent(evt)

    def updateLicenseData(self, values):
        if not values:
            return
        if 'licenseNo' in values:
            self._licenseNo = values['licenseNo']
        if 'hasSigned' in values:
            self._hasSigned = values['hasSigned']
        if 'ftbSite' in values:
            self._ftbSite = values['ftbSite']
        if 'ftbAddr' in values:
            self._ftbAddr = values['ftbAddr']
        evt = Event(events.EVNET_FTB_LICENSEDATA_CHANGE, {'licenseNo': self._licenseNo,
         'hasSigned': self._hasSigned,
         'ftbSite': self._ftbSite,
         'ftbAddr': self._ftbAddr})
        gameglobal.rds.ui.dispatchEvent(evt)

    def updateFtbSite(self, value):
        self._ftbSite = value

    def updateEarningData(self, values):
        if 'totalNowEarning' in values:
            self._totalNowEarning = values['totalNowEarning']
        if 'nowEarning' in values:
            self._nowEarning = values['nowEarning']
            self._digEventList.addEvent(DigEventNode.EARNING, self._nowEarning)
        if 'totalEarning' in values:
            self._totalEarning = values['totalEarning']
        if 'yaojingTicket' in values:
            self._yaojingTicket = float(values['yaojingTicket']) / 100
        evt = Event(events.EVNET_FTB_EARNINGDATA_CHANGE, {'totalNowEarning': self._totalNowEarning,
         'nowEarning': self._nowEarning,
         'yaojingTicket': self._yaojingTicket,
         'totalEarning': self._totalEarning})
        gameglobal.rds.ui.dispatchEvent(evt)

    def updateIsDigging(self, value, nowTime, buildEvent = True):
        self._isDigging = value
        evt = Event(events.EVNET_FTB_DIGINGSTATE_CHANGE, self._isDigging)
        gameglobal.rds.ui.dispatchEvent(evt)
        if self._isDigging:
            self._lastDigingTime = nowTime
            if buildEvent:
                self._digEventList.addEvent(DigEventNode.START, 0, nowTime)
            self._digTimeRecorder.start(self._onTimeChanged, nowTime)
        else:
            if buildEvent:
                self._digEventList.addEvent(DigEventNode.STOP, 0, nowTime)
            self._digTimeRecorder.stop()

    def updateTimeData(self, weekTimeOfConsumed, availTime):
        self._availTime = availTime
        self._weekTimeOfConsumed = weekTimeOfConsumed
        evt = Event(events.EVNET_FTB_TIMEDATA_CHANGE, {'weekTimeOfConsumed': self._weekTimeOfConsumed,
         'leftDigingTime': self._genLeftDigingTime()})
        gameglobal.rds.ui.dispatchEvent(evt)

    def updateOutputData(self, totalOutput, dailyOutput):
        self._totalOutput = totalOutput
        self._dailyOutput = dailyOutput
        evt = Event(events.EVNET_FTB_OUTPUTDATA_CHANGE, {'totalOutput': totalOutput,
         'dailyOutput': dailyOutput})
        gameglobal.rds.ui.dispatchEvent(evt)

    def updateHasVipRewardTaken(self, hasTaken):
        self._hasVipRewardTaken = hasTaken
        evt = Event(events.EVNET_FTB_HASVIPREWARDTAKEN_CHANGE, self._hasVipRewardTaken)
        gameglobal.rds.ui.dispatchEvent(evt)

    def updateConditionData(self, hasLicense, hasHome):
        self._hasLicense = hasLicense
        self._hasHome = hasHome
        evt = Event(events.EVNET_FTB_CONDITIONDATA_CHANGE, {'hasLicense': self._hasLicense,
         'hasHome': self._hasHome})
        gameglobal.rds.ui.dispatchEvent(evt)

    def updateTaskList(self, taskDict):
        historyTasks = []
        for taskId, value, expired in taskDict.get('taskHistory', []):
            historyTasks.append({'taskId': taskId,
             'expired': expired,
             'value': value})

        historyTasks.sort(key=lambda x: x['expired'], reverse=True)
        self._historyTaskList = historyTasks
        todayTasks = []
        for taskId, value in taskDict.get('curTasks', {}).iteritems():
            todayTasks.append({'taskId': taskId,
             'value': value})

        self._todayTaskList = todayTasks
        evt = Event(events.EVNET_FTB_DIGPOWERTASK_CHANGE)
        gameglobal.rds.ui.dispatchEvent(evt)

    def updateDigStateSwitch(self, stateSwitch):
        self._digStateSwitch = stateSwitch

    def updateAutoDigState(self, autoDig):
        self._isAutoDig = autoDig
        evt = Event(events.EVNET_FTB_AUTODIGSTATE_CHANGE, autoDig)
        gameglobal.rds.ui.dispatchEvent(evt)

    def updateCrossbackState(self, isDigging, tLastDig):
        self.clear()
        buildEvent = not not isDigging
        self.updateIsDigging(isDigging, tLastDig, buildEvent)

    def _genLeftDigingTime(self):
        if not self._isDigging:
            return self._availTime
        else:
            now = utils.getNow()
            last = self._lastDigingTime
            cost = max(now - last, 0)
            return max(self._availTime - cost, 0)

    def _onTimeChanged(self):
        evt = Event(events.EVNET_FTB_DIGTIMEDURATION_CHANGE, self._digTimeRecorder.getDuration())
        gameglobal.rds.ui.dispatchEvent(evt)
        evt = Event(events.EVNET_FTB_TIMEDATA_CHANGE, {'weekTimeOfConsumed': self._weekTimeOfConsumed,
         'leftDigingTime': self._genLeftDigingTime()})
        gameglobal.rds.ui.dispatchEvent(evt)
