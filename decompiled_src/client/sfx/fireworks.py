#Embedded file name: I:/bag/tmp/tw2/res/entities\client\sfx/fireworks.o
import math
import random
import BigWorld
import Math
import gameglobal
import sfx
import utils
from guis import ui
from data import fireworks_effect_data as FWED
PIVOT_HEIGHT = 1.7
CAM_PITCH = 0
DHPROVIDER = None
NUM_USING_FIREWORK = 0
NEED_CHANGE_CAM = False
OTHER_PLAYER_FIRE_COUNT = 0
MAX_OTHER_FIRE_COUNT = 5

class LaunchFire(object):

    def __init__(self, eff, pos, height, ownerId = -1, targetOffset = None, duration = 3.0, delayDestroyTime = 3, speed = 3):
        self.ownerID = ownerId
        self.effects = eff
        self.pos = pos
        self.duration = duration
        self.delayDestroyTime = delayDestroyTime
        self.speed = speed
        if targetOffset is None:
            self.targetOffset = Math.Vector3(0, height, 0)
        else:
            self.targetOffset = Math.Vector3(targetOffset[0], targetOffset[1] + height, targetOffset[2])
        self.dummyModel = sfx.getDummyModel()
        self.fireEffect = None
        self.explodeEffects = []
        self.effTxtInfo = None
        self.increOtherFireCount()

    def increOtherFireCount(self):
        global OTHER_PLAYER_FIRE_COUNT
        if self.ownerID != BigWorld.player().id:
            OTHER_PLAYER_FIRE_COUNT = OTHER_PLAYER_FIRE_COUNT + 1

    def decreOtherFireCount(self):
        global OTHER_PLAYER_FIRE_COUNT
        if self.ownerID != BigWorld.player().id:
            OTHER_PLAYER_FIRE_COUNT = OTHER_PLAYER_FIRE_COUNT - 1

    def setTxt(self, txt):
        if txt and len(txt) > 0:
            self.effTxtInfo = (txt,
             64,
             64,
             ui.font60)
        else:
            self.effTxtInfo = None

    def getEffectType(self):
        if self.ownerID == BigWorld.player().id:
            return sfx.EFFECT_UNLIMIT
        else:
            return sfx.EFFECT_LIMIT_MISC

    def launch(self):
        global MAX_OTHER_FIRE_COUNT
        global DHPROVIDER
        global NUM_USING_FIREWORK
        global CAM_PITCH
        global NEED_CHANGE_CAM
        global PIVOT_HEIGHT
        if self.ownerID != BigWorld.player().id and OTHER_PLAYER_FIRE_COUNT > MAX_OTHER_FIRE_COUNT:
            self.disappear()
            return
        self.dummyModel.position = self.pos
        motor = BigWorld.Rlauncher()
        motor.acceleration = -4
        self.dummyModel.addMotor(motor)
        target = self.dummyModel.position + self.targetOffset
        mat = Math.Matrix()
        mat.setTranslate(target)
        motor.target = mat
        motor.proximityCallback = self.explode
        motor.speed = self.speed
        motor.curvature = 0.2
        self.fireEffect = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (3,
         3,
         self.dummyModel,
         self.effects[0],
         self.getEffectType(),
         gameglobal.EFFECT_LAST_TIME + 30))
        p = BigWorld.player()
        if not gameglobal.CAMERA_FOCUS_FIREWORK and self.ownerID == p.id:
            if NUM_USING_FIREWORK != 1 or not NEED_CHANGE_CAM:
                NEED_CHANGE_CAM = False
                return
            NEED_CHANGE_CAM = False
            c = BigWorld.camera()
            if not (sfx.gNoEffect or c.firstPerson):
                gameglobal.CAMERA_FOCUS_FIREWORK = True
                PIVOT_HEIGHT = c.pivotPosition[1]
                DHPROVIDER = c.cameraDHProvider
                c.cameraDHProvider = None
                c.pivotPosition = (0, 4, 0)
                dc = BigWorld.dcursor()
                CAM_PITCH = dc.pitch
                atan = (target[1] - p.position[1]) / max(target.flatDistSqrTo(p.position), 0.01)
                pitch = math.atan(atan)
                dc.pitch = pitch

    def explode(self):
        if self.fireEffect:
            for i in self.fireEffect:
                i.stop()
                if self.dummyModel and i in self.dummyModel.root.attachments:
                    self.dummyModel.root.detach(i)

        self.fireEffect = []
        if self.dummyModel is None:
            self.disappear()
            return
        p = BigWorld.player()
        if not (p and p.inWorld):
            self.disappear()
            return
        for m in self.dummyModel.motors:
            self.dummyModel.delMotor(m)

        for fxId in self.effects[1:]:
            fxs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_INPOS, (p.getBasicEffectLv(),
             p.getBasicEffectPriority(),
             None,
             fxId,
             sfx.EFFECT_UNLIMIT,
             self.dummyModel.position,
             0,
             0,
             0,
             self.duration))
            if fxs:
                self.explodeEffects.extend(fxs)

        BigWorld.callback(self.duration, self.disappear)

    def disappear(self):
        p = BigWorld.player()
        if gameglobal.CAMERA_FOCUS_FIREWORK and self.ownerID == p.id:
            if not sfx.gNoEffect:
                restoreCam()
        try:
            if self.explodeEffects:
                for fx in self.explodeEffects:
                    if fx:
                        fx.stop()

            self.explodeEffects = []
        except:
            pass

        self.decreOtherFireCount()
        if self.dummyModel is None:
            self.destroy()
            return
        p = BigWorld.player()
        if p and p.inWorld:
            BigWorld.callback(self.delayDestroyTime, self.destroy)
        else:
            self.destroy()

    def destroy(self):
        self.fireEffect = None
        if self.dummyModel:
            sfx.giveBackDummyModel(self.dummyModel)
        self.dummyModel = None
        self.effects = None
        self.effTxtInfo = None


class Launcher(object):

    @staticmethod
    def getObj(fwId, ownerID, previewDuration):
        avt = BigWorld.entity(ownerID)
        pos = avt.position
        return Launcher(fwId, None, pos, ownerID, previewDuration)

    @staticmethod
    def getObjByPostion(fwId, ownerID, previewDuration, pos):
        avt = BigWorld.entity(ownerID)
        return Launcher(fwId, None, pos, ownerID, previewDuration)

    def __init__(self, fwId, model, pos, ownerID, previewDuration):
        self.fireID = fwId
        self.model = model
        self.ownerID = ownerID
        self.previewDuration = previewDuration
        p = BigWorld.player()
        if model:
            p.addModel(model)
            model.position = pos
            self.pos = pos + (0, model.height, 0)
        else:
            self.pos = pos
        scale = 1.0
        if scale != 1.0:
            model.scale = (scale, scale, scale)
        data = FWED.data.get(fwId, {})
        self.upEff = data.get('upEff', 12501)
        self.txtEff = None
        self.txtFire = None
        self.effects = data.get('effects', [12501,
         12501,
         12501,
         12501])
        self.height = data.get('height', 1.0)
        self.shots = 1
        self.txt = data.get('text', '1')

    def launch(self):
        global NUM_USING_FIREWORK
        if self.shots > 0:
            NUM_USING_FIREWORK += 1
            self._launchTxt()
            self._launch()

    def _launchTxt(self):
        if not self.txtEff:
            return
        eff = (self.upEff, self.txtEff)
        duration = 30
        self.txtFire = LaunchFire(eff, self.pos, self.height, self.ownerID, None, duration)
        self.txtFire.setTxt(self.txt)
        self.txtFire.launch()

    def _launch(self):
        avt = BigWorld.entity(self.ownerID)
        if not (avt and avt.inWorld):
            self.clearRes()
            return
        data = FWED.data.get(self.fireID, {})
        radius = data.get('radius', 0)
        theta = data.get('yaw', 0)
        dstPos = utils.getRelativePosition(avt.position, avt.yaw, theta, radius)
        y_offset = data.get('yOffset', 0)
        targetOffset = (dstPos[0] - avt.position[0], y_offset, dstPos[2] - avt.position[2])
        needRandom = data.get('needRandom', False)
        durationEffs = [random.choice(self.effects)] if needRandom else self.effects
        eff = [self.upEff]
        eff.extend(durationEffs)
        duration = data.get('duration', 3)
        if self.previewDuration > 0:
            duration = min(duration, self.previewDuration)
        delayDestroyTime = data.get('delayDestroyTime', 3)
        speed = data.get('speed', 10)
        fw = LaunchFire(eff, self.pos, self.height, self.ownerID, targetOffset, duration, delayDestroyTime, speed)
        fw.launch()
        self.shots -= 1
        launchTime = data.get('launchTime', 2)
        if self.shots > 0:
            BigWorld.callback(launchTime, self._launch)
        else:
            BigWorld.callback(duration + launchTime + delayDestroyTime, self.clearRes)

    def clearRes(self):
        global NUM_USING_FIREWORK
        NUM_USING_FIREWORK -= 1
        if self.model:
            p = BigWorld.player()
            if p and p.inWorld:
                p.delModel(self.model)
            self.model = None
        if self.txtFire:
            self.txtFire.destroy()
            self.txtFire = None


def restoreCam():
    global DHPROVIDER
    global CAM_PITCH
    if gameglobal.CAMERA_FOCUS_FIREWORK:
        gameglobal.CAMERA_FOCUS_FIREWORK = False
        p = BigWorld.player()
        if p and p.inWorld:
            c = BigWorld.camera()
            c.cameraDHProvider = DHPROVIDER
            c.pivotPosition = (0, PIVOT_HEIGHT, 0)
            dc = BigWorld.dcursor()
            dc.pitch = CAM_PITCH
            CAM_PITCH = 0
            DHPROVIDER = None


def attachFireWorksLove(owner, keepTime = 5.0, effects = [12301]):
    for effect in effects:
        sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (3,
         3,
         owner.model,
         effect,
         sfx.EFFECT_UNLIMIT,
         keepTime))


def testFireWorks(fwid, entId, extra = '—Ãª®≤‚ ‘', previewDuration = 0):
    fw = Launcher.getObj(fwid, entId, previewDuration)
    fw.launch()
