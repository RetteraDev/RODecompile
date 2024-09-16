#Embedded file name: /WORKSPACE/data/entities/client/helpers/puppetnav.o
import BigWorld
import navigator
import formula
import Math
import gamelog
from gameclass import Singleton
from helpers import tickManager
from callbackHelper import Functor
import utils
RESULT_UNKNOW = 0
NAV_FAILED = 1
NAV_SUCCESS = 2
TIME_OUT = 1
CHECK_TIME_OUT = 3
RETURN_TIME_OUT = 4
PATHFINDING_NUM = 20

def getInstance():
    return PuppetNavManager.getInstance()


class PuppetTaskBase(object):

    def __init__(self):
        self.result = 0

    def start(self):
        pass

    def stop(self):
        pass

    def process(self):
        pass

    def isTaskDone(self):
        return bool(self.result)


class PathFindingTask(PuppetTaskBase):

    def __init__(self, spaceNo, asyncId, nuid, entId, targetPos, oriPos, callback, checkTime):
        super(PathFindingTask, self).__init__()
        self.spaceNo = spaceNo
        self.asyncId = asyncId
        self.nuid = nuid
        self.entId = entId
        self.targetPos = Math.Vector3(targetPos)
        self.oriPos = Math.Vector3(oriPos)
        self.callback = callback
        self.nav = None
        self.tickId = 0
        self.isGo = False
        self.beginTime = 0
        self.posList = []
        self.checkTime = checkTime

    def setNav(self, nav):
        self.nav = nav

    def start(self):
        if not self.nav:
            return
        self._navCancel()
        self.beginTime = utils.getNow()

    def stop(self):
        self._navCancel()

    def process(self):
        if not self.nav:
            return
        if not self.beginTime:
            return
        if utils.getNow() - self.beginTime > TIME_OUT:
            self.result = NAV_FAILED
        if self.isTaskDone():
            return
        if not self.isGo:
            self.navGo()
        else:
            positions = self.nav.getNextPositions()
            if positions:
                if len(positions) > 1:
                    self.posList.append(self.oriPos)
                    for pos in positions:
                        if pos not in self.posList:
                            self.posList.append(pos)

                    data = {'asyncId': self.asyncId,
                     'nuid': self.nuid,
                     'entId': self.entId,
                     'positions': self.posList}
                    self.result = NAV_SUCCESS
                    if self.callback and utils.getNow(False) - self.checkTime < RETURN_TIME_OUT:
                        self.callback(self.result, data)
            else:
                gamelog.debug('@zq navigator PathTraceManager no positions')

    def _navCancel(self):
        self.nav.cancel()

    def navGo(self):
        res = self.nav.go(self.oriPos.x, self.oriPos.y, self.oriPos.z, self.targetPos.x, self.targetPos.y, self.targetPos.z)
        if res is None:
            gamelog.debug('@zq navigator PathTraceManager navGo failed')
            self._navCancel()
            self.result = NAV_FAILED
            return
        self.isGo = True

    def hasNav(self):
        return bool(self.nav)

    def getSpaceNo(self):
        return self.spaceNo

    def getResult(self):
        return self.result


class PuppetNavManager(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.waitingList = []
        self.seekNavs = {}
        self.curTask = None
        self.tickId = 0

    def queryValidPosition(self, asyncId, nuid, entId, targetPos, callback, oriPos):
        if len(self.waitingList) > PATHFINDING_NUM:
            return
        checkTime = utils.getNow(False)
        self.waitingList.append((asyncId,
         nuid,
         entId,
         targetPos,
         callback,
         oriPos,
         checkTime))
        self.startTick()

    def startTick(self):
        if self.tickId:
            tickManager.stopTick(self.tickId)
            self.tickId = 0
        self.tickId = tickManager.addTick(0.1, self.tick)

    def tick(self):
        if self.curTask and self.curTask.isTaskDone():
            self.clearTask()
        if not self.waitingList:
            if not self.curTask:
                tickManager.stopTick(self.tickId)
                self.tickId = 0
                return
        if not self.curTask:
            self.buildTask()
        else:
            self.curTask.process()

    def buildTask(self):
        p = BigWorld.player()
        spaceNo = p.spaceNo
        mapId = p.mapID
        asyncId, nuid, entId, targetPos, callback, oriPos, checkTime = self.waitingList.pop(0)
        nowTime = utils.getNow()
        if nowTime - checkTime > CHECK_TIME_OUT:
            return
        position = None
        self.curTask = PathFindingTask(spaceNo, asyncId, nuid, entId, targetPos, oriPos, callback, checkTime)
        currentNav = self.seekNavs.get(mapId, None)
        if not currentNav:
            self.initSeekNavsBySpaceNo(spaceNo, Functor(self.initSeekNavsCallback, spaceNo))
            return
        self.curTask.setNav(currentNav)
        self.curTask.start()

    def clearTask(self):
        if self.curTask:
            self.curTask.stop()
            self.curTask = None

    def initSeekNavsCallback(self, spaceNo, navs):
        p = BigWorld.player()
        if navs != self.seekNavs:
            for k, v in navs.iteritems():
                mapIds = formula.whatAllSpaceNoByFileName(k)
                for mId in mapIds:
                    self.seekNavs[mId] = v

        mapId = formula.getMapId(spaceNo)
        if formula.getMapId(self.curTask.getSpaceNo()) == mapId:
            currentNav = self.seekNavs.get(mapId, None)
            if currentNav:
                self.curTask.setNav(currentNav)
                self.curTask.start()
            else:
                self.clearTask()

    def initSeekNavsBySpaceNo(self, spaceNo, callback = None):
        if spaceNo <= 0:
            return
        tFileList = [navigator.getPhaseMappingNameBySpaceNo(spaceNo)]
        BigWorld.initAllNavigators(tFileList, Functor(self.initSeekNavsCallback, spaceNo))
