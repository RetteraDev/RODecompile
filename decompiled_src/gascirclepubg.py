#Embedded file name: /WORKSPACE/data/entities/client/helpers/gascirclepubg.o
import BigWorld
import gameglobal
import Math
import gamelog
import Pixie
from gameclass import Singleton
from helpers import tickManager
from callbackHelper import Functor
from sfx import sfx
import utils
from data import duel_config_data as DCD
from cdata import pubg_safe_area_data as PSAD
DEFAULT_RADIUS = 3000
RES_RADIUS = 100
EFFECT_ID = 61152
GAS_DUMMY_MODEL_PATH = 'effect/dummy/effectdummy.model'

def getInstance():
    return GasCirclePUBG.getInstance()


class GasCirclePUBG(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.circleFx = None
        self.circleRefreshCallBack = None

    def init(self):
        p = BigWorld.player()
        if hasattr(BigWorld, 'attachToWonder') and p.isInPUBG():
            self.clear()
            self.attachEffect()
            self.update()

    def attachEffect(self):
        effectId = self.getEffectId()
        fx = Pixie.fetch(sfx.getPath(effectId))
        self.circleFx = fx
        self.circleFx.fetchCallback = self.fetchCallback
        BigWorld.attachToWonder(GAS_DUMMY_MODEL_PATH, self.circleFx)
        self.circleFx.force()

    def getEffectId(self):
        return EFFECT_ID

    def fetchCallback(self, isSuccess):
        if isSuccess:
            if not self.circleFx:
                return
            BigWorld.callback(0, self.circleFx.force)
        else:
            self.attachEffect()

    def setCircleCallBack(self):
        self.cancelCircleCallBack()
        self.circleRefreshCallBack = BigWorld.callback(0.01, self.update)

    def cancelCircleCallBack(self):
        if self.circleRefreshCallBack:
            BigWorld.cancelCallback(self.circleRefreshCallBack)
            self.circleRefreshCallBack = None

    def update(self):
        p = BigWorld.player()
        if not p or not p.isInPUBG():
            return
        stage, stamp, nowPos, nextPos = self.getCircleData()
        radius = p.getCurPoisonCircleRadius(stage, stamp)
        pos = p.getCurPoisonCirclePos(stage, stamp, nowPos, nextPos)
        self.setCirclePos(pos)
        self.setCircleRadius(radius)
        self.setCircleCallBack()

    def getCircleData(self):
        p = BigWorld.player()
        if p.curPoisonCircleData:
            stage, stamp, nowPos, nextPos = p.curPoisonCircleData
            return (stage,
             stamp,
             nowPos,
             nextPos)

    def setCircleRadius(self, radius):
        scale = float(radius) / RES_RADIUS
        self.setCircleScale(scale)

    def setCircleScale(self, scale):
        if self.circleFx:
            scale = Math.Vector3((scale, scale, scale))
            BigWorld.setAttachScaleToWonder(GAS_DUMMY_MODEL_PATH, scale)

    def setCirclePos(self, pos):
        pos = (pos[0], pos[1] - 50, pos[2])
        pos = Math.Vector3(pos)
        if self.circleFx:
            BigWorld.setAttachPosToWonder(GAS_DUMMY_MODEL_PATH, pos)

    def removeCircle(self):
        if hasattr(BigWorld, 'attachToWonder'):
            self.refreshEffect()

    def refreshEffect(self):
        if self.circleFx:
            BigWorld.clearAttachmentsInWonder(GAS_DUMMY_MODEL_PATH)
            self.circleFx = None

    def clear(self):
        self.cancelCircleCallBack()
        self.removeCircle()
        self.circleFx = None
