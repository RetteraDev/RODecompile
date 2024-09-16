#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/fishing.o
import math
import BigWorld
import Math
import keys
import gameglobal
import gamelog
import const
import attachedModel
from helpers import action as ACT
from helpers import charRes
from callbackHelper import Functor
from sfx import sfx
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD

class FishingMgr(object):
    FISHING_ROD_DELAY = 1.0
    FISHING_AUTO_DELAY = 3.0
    FISHING_DURATION = 30.0

    def __init__(self, owner):
        self.owner = owner
        self.isPlayer = owner.id == BigWorld.player().id
        self.lineModel = None
        self.rodModel = None
        self.buoyModel = None
        self.syncID = 0
        self.realStartTimer = 0
        self.showRodTimer = 0
        self.stopFishTimer = 0
        self.autoFishTimer = 0
        self.buoyFx0 = None
        self.buoyFx1 = None
        self.buoyFx2 = None
        self.buoyPos = None
        self.isCharging = False
        self.autoFishing = False
        self.step = None

    def release(self):
        self.clearRes(self.syncID)
        self.owner = None
        self.isPlayer = False
        self.isCharging = False
        self.autoFishing = False
        self.syncID += 1

    def clearRes(self, syncID, keepRod = False):
        if syncID != self.syncID:
            return
        self.buoyPos = None
        if self.lineModel:
            if self.lineModel.inWorld:
                self.owner.delModel(self.lineModel)
            self.lineModel = None
        if self.buoyModel:
            self._endBuoyFx0()
            self._endBuoyFx1()
            self._endBuoyFx2()
            sfx.giveBackDummyModel(self.buoyModel)
            self.buoyModel = None
        self.clearTimer()
        if not keepRod:
            self.rodModel = None
            if hasattr(self.owner, 'modelServer') and self.owner.modelServer:
                fishModel = self.owner.modelServer.fishingModel
                if fishModel.state != attachedModel.DETACHED:
                    fishModel.detach()
            if hasattr(self.owner, 'fashion') and self.owner.fashion:
                self.owner.fashion.stopAction()

    def clearTimer(self):
        if self.realStartTimer:
            BigWorld.cancelCallback(self.realStartTimer)
        self.realStartTimer = 0
        if self.showRodTimer:
            BigWorld.cancelCallback(self.showRodTimer)
        self.showRodTimer = 0

    def clearAutoTimer(self):
        if self.isPlayer:
            if self.autoFishTimer:
                BigWorld.cancelCallback(self.autoFishTimer)
                self.autoFishTimer = 0

    def setAutoTimer(self):
        self.clearAutoTimer()
        if self.isPlayer and self.autoFishing:
            self.autoFishTimer = BigWorld.callback(FishingMgr.FISHING_AUTO_DELAY, self.owner.autoFishAgain)

    def start(self, step = const.ST_READY_FISHING):
        if not self.owner.inWorld:
            return
        self.step = step
        gamelog.debug('fishingMgr@start', self.lineModel, self.rodModel, step)
        if self.lineModel and self.rodModel:
            self.realStart(self.syncID)
            return
        self.syncID += 1
        self.owner.modelServer.fishingModel.equipItem(self.syncID, self.owner.aspect.fishingRod)
        self.loadFishRod(self.syncID)

    def loadFishRod(self, syncID):
        if syncID != self.syncID:
            return
        if not self.lineModel:
            charRes.getSimpleModel(gameglobal.LINE_MODEL, None, Functor(self._afterFishModelFinished, syncID))
        else:
            self._afterFishModelFinished(syncID, self.lineModel)

    def _afterFishModelFinished(self, syncID, model):
        if syncID != self.syncID:
            return
        self.lineModel = model
        self.realStart(syncID)

    def readyFish(self, syncID):
        if syncID != self.syncID:
            return
        if not self.owner or not self.owner.inWorld:
            self.release()
            return
        self.owner.fashion.stopAction()
        self.owner.am.matchCaps = [keys.CAPS_HAND_FREE, keys.CAPS_FISH_READY]

    def holdFishRod(self, syncID):
        if syncID != self.syncID:
            return
        if not self.owner or not self.owner.inWorld:
            self.release()
            return
        self.owner.fashion.stopAction()
        fishingHoldAction = self.owner.fashion.action.getFishingHoldAction(self.owner.fashion)
        gamelog.debug('holdFishRod', fishingHoldAction)
        self.owner.fashion.playAction([fishingHoldAction], ACT.FISHING_HOLD_ACTION)

    def realStart(self, syncID):
        if syncID != self.syncID:
            return
        if not self.owner or not self.owner.inWorld:
            self.release()
            return
        if self.step == const.ST_READY_FISHING and not self.owner.inFishingReady():
            return
        if not self.lineModel or not self.owner.modelServer.fishingModel.model:
            return
        fishingModel = self.owner.modelServer.fishingModel
        if fishingModel.state != attachedModel.ATTACHED:
            fishingModel.attach(self.owner.modelServer.bodyModel)
        self.rodModel = self.owner.modelServer.fishingModel.model
        gamelog.debug('jorsef2: realStart', self.rodModel, self.step)
        if self.owner.inSwim:
            self.owner.stopFish()
            return
        if self.step == const.ST_READY_FISHING:
            self.readyFish(self.syncID)
        elif self.step == const.ST_HOLD_FISHING:
            self.holdFishRod(self.syncID)
        elif self.step == const.ST_THROW_FISHING:
            self._throwFishRod(self.syncID)

    def shakeBuoy(self, time, isCharging):
        if time < 0.8:
            time = 0.8
        if self.buoyModel:
            self._endBuoyFx0()
            self.buoyFx1 = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.owner.getBasicEffectLv(),
             self.owner.getBasicEffectPriority(),
             self.buoyModel,
             SCD.data.get('sfxFishing1', gameglobal.SFX_FISHING_1),
             sfx.EFFECT_LIMIT_MISC))

    def _endBuoyFx0(self):
        if self.buoyFx0:
            for fx in self.buoyFx0:
                fx.clear()

            sfx.detachEffect(self.buoyModel, SCD.data.get('sfxFishing0', gameglobal.SFX_FISHING_0), self.buoyFx0)
            self.buoyFx0 = None

    def _endBuoyFx1(self):
        if self.buoyFx1:
            for fx in self.buoyFx1:
                fx.clear()

            sfx.detachEffect(self.buoyModel, SCD.data.get('sfxFishing1', gameglobal.SFX_FISHING_1), self.buoyFx1)
            self.buoyFx1 = None

    def _endBuoyFx2(self):
        if self.buoyFx2:
            for fx in self.buoyFx2:
                fx.clear()

            sfx.detachEffect(self.buoyModel, SCD.data.get('sfxFishing2', gameglobal.SFX_FISHING_2), self.buoyFx2)
            self.buoyFx2 = None

    def throwFishRod(self, buoyPos):
        self.buoyPos = buoyPos
        self.clearTimer()
        self.start(const.ST_THROW_FISHING)

    def _throwFishRod(self, syncID):
        self.owner.am.matchCaps = [keys.CAPS_HAND_FREE, keys.CAPS_FISH]
        fishingStartAction = self.owner.fashion.action.getFishingStartAction(self.owner.fashion)
        gamelog.debug('throwFishRod', fishingStartAction)
        self.owner.fashion.stopAction()
        self.owner.fashion.playAction([fishingStartAction], ACT.FISHING_ACTION, blend=True)
        self.showRodTimer = BigWorld.callback(FishingMgr.FISHING_ROD_DELAY, Functor(self._showFishRod, syncID))

    def _showFishRod(self, syncID):
        self.buoyModel = sfx.getDummyModel()
        if not self.owner or not self.owner.inWorld or not self.owner.buoyPos:
            return
        if not self.buoyPos:
            self.buoyPos = self.owner.buoyPos
        self.buoyModel.position = Math.Vector3(0, 1.5, 0) + self.buoyPos
        motor = BigWorld.Rlauncher()
        mat = Math.Matrix()
        mat.setTranslate(self.buoyPos)
        motor.target = mat
        motor.acceleration = 3
        motor.speed = 3
        self.buoyModel.addMotor(motor)
        motor.curvature = 0.1
        motor.proximityCallback = Functor(self.approach, syncID)
        if self.lineModel:
            if not self.lineModel.inWorld:
                self.owner.addModel(self.lineModel)
            if self.rodModel:
                mot = BigWorld.Connector()
                mot.length = 5
                self.lineModel.addMotor(mot)
                mot.start = self.rodModel.node('HP_line')
                mot.end = self.buoyModel.node('Scene Root')

    def approach(self, syncID):
        gamelog.debug('jorsef2 : fishing approach', syncID == self.syncID)
        if syncID != self.syncID:
            return
        if not self.owner.inWorld:
            self.release()
            return
        if self.buoyModel:
            for m in self.buoyModel.motors:
                self.buoyModel.delMotor(m)

            self.buoyModel.position = self.buoyPos
        if self.isPlayer:
            gameglobal.rds.sound.playSound(gameglobal.SD_410)
        if self.buoyModel:
            self.buoyFx0 = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.owner.getBasicEffectLv(),
             self.owner.getBasicEffectPriority(),
             self.buoyModel,
             SCD.data.get('sfxFishing0', gameglobal.SFX_FISHING_0),
             sfx.EFFECT_LIMIT_MISC))

    def pullFish(self, isRealPull):
        gamelog.debug('pullFish')
        if not self.owner or not self.owner.inWorld:
            self.clearRes(self.syncID)
            return
        if isRealPull:
            self._endBuoyFx0()
            self._endBuoyFx1()
            if not self.buoyFx2:
                self.buoyFx2 = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.owner.getBasicEffectLv(),
                 self.owner.getBasicEffectPriority(),
                 self.buoyModel,
                 SCD.data.get('sfxFishing2', gameglobal.SFX_FISHING_2),
                 sfx.EFFECT_LIMIT_MISC))
            else:
                for fx in self.buoyFx2:
                    fx.force()

            if self.lineModel:
                if self.lineModel.inWorld:
                    self.owner.delModel(self.lineModel)
                self.lineModel = None
            self.owner.fashion.stopAction()
            if not self.owner.inFishingReady():
                fishingPullEndAction = self.owner.fashion.action.getFishingPullEndAction(self.owner.fashion)
                self.owner.fashion.playAction([fishingPullEndAction], ACT.FISHING_ACTION, blend=True)
                BigWorld.callback(FishingMgr.FISHING_ROD_DELAY, Functor(self.clearRes, self.syncID))
            else:
                fishingPullEndAction = self.owner.fashion.action.getFishingPullEndAction(self.owner.fashion)
                self.readyFish(self.syncID)
                self.owner.fashion.playAction([fishingPullEndAction], ACT.FISHING_ACTION, blend=True)
                BigWorld.callback(FishingMgr.FISHING_ROD_DELAY, Functor(self.clearRes, self.syncID, True))
                self.setAutoTimer()
        else:
            fishingPullAction = self.owner.fashion.action.getFishingPullAction(self.owner.fashion)
            fishingPullLoopAction = self.owner.fashion.action.getFishingPullLoopAction(self.owner.fashion)
            self.owner.fashion.playAction([fishingPullAction, fishingPullLoopAction], ACT.FISHING_ACTION, blend=True)
            self.isCharging = False

    def stopFish(self):
        self.autoFishing = False
        self.clearAutoTimer()
        self.clearRes(self.syncID)
        self.owner.fashion.stopAction()
        self.owner.fashion.setGuard(self.owner.inCombat)


FISHING_ROD_LENGTH = 3
FISHING_ROD_ANGLE = math.pi * 15 / 180
FISHING_ROD_HORIZONTAL_LENGTH = FISHING_ROD_LENGTH * math.cos(FISHING_ROD_ANGLE)
FISHING_ROD_VERTICAL_LENGTH = FISHING_ROD_LENGTH * math.sin(FISHING_ROD_ANGLE)

def checkWater(dist):
    p = BigWorld.player()
    if p.inSwim or p.canFly():
        return
    xOffset = dist * math.sin(p.model.yaw)
    zOffset = dist * math.cos(p.model.yaw)
    offVec = Math.Vector3(xOffset, 1.0, zOffset)
    dstPos = p.position + offVec
    waterHeight = BigWorld.findWaterFromPoint(p.spaceID, dstPos)
    if waterHeight is None:
        if p.fishingMgr.autoFishing:
            p.stopFish()
            gameglobal.rds.ui.fishing.show()
        p.showGameMsg(GMDD.data.FISHING_NOT_ALLOWED_HERE, ())
        return
    dstPos = (dstPos[0], waterHeight[0], dstPos[2])
    tmpPos = p.position + Math.Vector3(0, p.model.height / 2, 0)
    x = tmpPos[0] + FISHING_ROD_HORIZONTAL_LENGTH * math.sin(p.yaw)
    y = tmpPos[1] + FISHING_ROD_VERTICAL_LENGTH
    z = tmpPos[2] + FISHING_ROD_HORIZONTAL_LENGTH * math.cos(p.yaw)
    if BigWorld.collide(p.spaceID, (x, y, z), dstPos + Math.Vector3(0, p.model.height / 2, 0)):
        p.stopFish()
        gameglobal.rds.ui.fishing.show()
        p.showGameMsg(GMDD.data.FISHING_NOT_ALLOWED_HERE, ())
        return
    if (p.position - dstPos).y >= SCD.data.get('fishLimitHeight', 20):
        p.showGameMsg(GMDD.data.FISH_TO_HIGH, ())
        return
    return dstPos


def start():
    p = BigWorld.player()
    p.fishingMgr = FishingMgr(p)
    pos = Math.Vector3(p.position)
    pos.x += 4
    p.fishingMgr.start(pos)


def end(real = True):
    p = BigWorld.player()
    p.fishingMgr.pullFish(real)
