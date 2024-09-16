#Embedded file name: /WORKSPACE/data/entities/client/helpers/navigatorrouter.o
import Math
import Pixie
import BigWorld
import utils
import clientUtils
from sfx import sfx
from callbackHelper import Functor
from data import sys_config_data as SCD
SFX_ROUTER = 2427

class Arrow(object):

    def __init__(self):
        self.model = None
        self.fx = None

    def update(self, pos, dir, isAffixed = True):
        p = BigWorld.player()
        if isAffixed:
            tpos = pos + (0, 3, 0)
            res = BigWorld.findDropPoint(p.spaceID, tpos)
            if res:
                pos = res[0]
        self.model = sfx.getDummyModel(True)
        self.model.position = pos
        self.fx = clientUtils.pixieFetch(sfx.getPath(SCD.data.get('sfxRouter', SFX_ROUTER)))
        self.fx.setAttachMode(0, 0, 0)
        self.model.root.scale(1, 1, 1)
        self.model.yaw = 0
        self.model.root.attach(self.fx)
        pitch = 0
        if not isAffixed:
            pitch = dir.pitch
        self.model.rotateYPR((dir.yaw, pitch, 0))
        self.fx.force()

    def release(self):
        if self.model:
            if self.fx:
                if self.fx in self.model.root.attachments:
                    self.model.root.detach(self.fx)
                self.fx.clear()
                self.fx = None
            sfx.giveBackDummyModel(self.model)
            self.model = None


class NavigatorRouter(object):
    ROUTE_OUT_TIME = 180

    def __init__(self):
        self.timeInterval = 0.15
        self.scope = 3
        self.path = {}
        self.pathStamp = {}

    def drawLine(self, pathId, path, isAffixed = True, ttl = 0):
        if pathId in self.path:
            return
        if len(path) == 0:
            return
        path = list(path)
        startPos = path.pop(0)
        pathPoint = [Math.Vector3(startPos)]
        for nextPoint in path:
            startPos = pathPoint[-1]
            pathPoint.extend(self.genPathPoint(startPos, nextPoint))

        l = len(pathPoint)
        if l >= 2:
            arrowArray = []
            arrow = Arrow()
            dir = pathPoint[1] - pathPoint[0]
            arrow.update(pathPoint[0], dir, isAffixed)
            arrowArray.append(arrow)
            self.path[pathId] = arrowArray
            if ttl == 0:
                ttl = self.ROUTE_OUT_TIME
            self.pathStamp[pathId] = utils.getNow() + ttl
            BigWorld.callback(self.timeInterval, Functor(self._drawLine, l, 1, arrowArray, pathPoint, isAffixed))

    def _drawLine(self, num, i, arrowArray, pathPoint, isAffixed = True):
        if i == num:
            return
        arrow = Arrow()
        dir = pathPoint[i] - pathPoint[i - 1]
        arrow.update(pathPoint[i], dir, isAffixed)
        arrowArray.append(arrow)
        BigWorld.callback(self.timeInterval, Functor(self._drawLine, num, i + 1, arrowArray, pathPoint, isAffixed))

    def hideLine(self, pathId):
        if pathId not in self.path:
            return
        arrowArray = self.path.pop(pathId)
        self.pathStamp.pop(pathId)
        self._hideLine(arrowArray)

    def _hideLine(self, arrowArray):
        if arrowArray:
            arrow = arrowArray.pop(0)
            arrow.release()
            arrow = None
            BigWorld.callback(self.timeInterval, Functor(self._hideLine, arrowArray))

    def genPathPoint(self, startPos, endPos):
        pathPoint = []
        startPos = Math.Vector3(startPos)
        endPos = Math.Vector3(endPos)
        distVector = endPos - startPos
        dist = distVector.length
        distVector.normalise()
        num = int(dist / self.scope)
        for i in xrange(num):
            startPos = startPos + distVector * self.scope
            pathPoint.append(startPos)

        return pathPoint

    def releaseLine(self, pathId):
        if pathId not in self.path:
            return
        arrowArray = self.path[pathId]
        for i, arrow in enumerate(arrowArray):
            arrow.release()
            arrowArray[i] = None

        self.path.pop(pathId)
        self.pathStamp.pop(pathId)

    def release(self):
        for pathId in self.path.keys():
            self.releaseLine(pathId)

    def selfCheck(self):
        now = utils.getNow()
        for pathId in self.path.keys():
            oldStamp = self.pathStamp.get(pathId, 0)
            if oldStamp < now:
                self.hideLine(pathId)
