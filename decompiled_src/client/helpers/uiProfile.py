#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/uiProfile.o
import time
import os
import BigWorld
from guis import asObject
PROFILE_EVENT = {'buttonClick', 'click'}

class UIProfile(object):

    def __init__(self):
        self.statInfo = {}
        self.eventCost = {}
        self.widSwfName = {}

    def startLoadWidget(self, wid):
        statList = self.statInfo.get(wid, [])
        if statList and not statList[-1].hasEndData():
            statList.pop()
        obj = ProfileSnapShot(wid)
        obj.startLoad()
        statList.append(obj)
        self.statInfo[wid] = statList

    def endLoadWidget(self, wid, widget):
        widget = asObject.ASObject(widget)
        swfName = os.path.basename(widget.loaderInfo.url)
        self.widSwfName[wid] = swfName
        statDicts = self.statInfo.get(wid, [])
        if statDicts and not statDicts[-1].hasEndData():
            statDicts[-1].endLoad(swfName)
        self.statInfo[wid] = statDicts
        for e in PROFILE_EVENT:
            widget.addEventListener(e, self.handleEventStart, True, 0, True)
            widget.addEventListener(e, self.handleEventEnd, False, 0, True)

    def handleEventStart(self, *args):
        e = asObject.ASObject(args[3][0])
        wid = e.currentTarget.widgetId
        name = e.target.name
        cost = EventCost(wid, e.type)
        cost.eventStart()
        tmp = self.eventCost.get(wid, {})
        tmp.setdefault(name, []).append(cost)
        self.eventCost[wid] = tmp

    def handleEventEnd(self, *args):
        e = asObject.ASObject(args[3][0])
        wid = e.currentTarget.widgetId
        name = e.target.name
        tmp = self.eventCost.get(wid, {})
        if tmp.has_key(name):
            costs = tmp.setdefault(name, [])
            if costs:
                if not costs[-1].isEventEnded():
                    costs[-1].enventEnd()

    def getProfileData(self):
        memData = []
        openTime = {}
        uiMemData = {}
        for wid, dicts in self.statInfo.iteritems():
            for index, snapShot in enumerate(dicts):
                memData.append([snapShot.startTime, snapShot.memStart])
                if snapShot.hasEndData():
                    memData.append([snapShot.endTime, snapShot.memEnd])
                    openTime.setdefault(wid, []).append(snapShot.getTimeCost())
                    if index == 0:
                        uiMemData[wid] = snapShot.getMemCost()

        return {'memoryData': memData,
         'uiMemory': uiMemData,
         'timeCost': openTime}


class EventCost(object):

    def __init__(self, wid, type):
        self.wid = wid
        self.eventType = type
        self.startTime = 0
        self.endTime = 0

    def eventStart(self):
        self.startTime = time.time()

    def enventEnd(self):
        self.endTime = time.time()

    def isEventEnded(self):
        return self.endTime > 0

    def getCost(self):
        return self.endTime - self.startTime


class ProfileSnapShot(object):

    def __init__(self, wid):
        self.wid = wid
        self.swfName = ''
        self.startTime = 0
        self.endTime = 0
        self.memStart = 0
        self.memEnd = 0
        self.movieDataMem = 0

    def hasEndData(self):
        return self.endTime > 0

    def startLoad(self):
        self.startTime = time.time()
        self.memStart = BigWorld.getUIMem()

    def endLoad(self, swfName):
        self.swfName = swfName
        self.endTime = time.time()
        self.memEnd = BigWorld.getUIMem()
        self.movieDataMem = 1
        memList = BigWorld.getMemWidgetList()
        for line in memList.splitlines():
            if '\"%s\"' % self.swfName in line:
                self.movieDataMem += int(line.split('\"%s\"' % self.swfName)[1].strip().replace(',', ''))

    def getTimeCost(self):
        return self.endTime - self.startTime

    def getMemCost(self):
        return self.movieDataMem
