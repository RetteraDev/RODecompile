#Embedded file name: I:/bag/tmp/tw2/res/entities\client\sfx/screenEffect.o
import time
import math
import BigWorld
import gameglobal
import gamelog
import gametypes
from gameclass import Singleton
from callbackHelper import Functor
from data import screen_effect_data as SED
DEFAULT_PATH = 'effect/screen/'
SWAY_PRIORITY = (0, 0)
DARK_ANGLE_EFFECT = 1017

class ScreenEffectManager(object):
    __metaclass__ = Singleton

    def __init__(self):
        super(ScreenEffectManager, self).__init__()
        self.reset()

    def reset(self):
        self.dict = {}
        self.lv = 0
        self.tag = 0
        self.path = None
        self.callback = None

    def startScreenEffect(self, tag, id, autoRemove = True, isSkill = True):
        if gameglobal.ENABLE_SCREEN_EFFECT:
            lv, lastTime, path, fadeIn, fadeOut, ignoreSwitch = getScreenInfo(id)
            if path:
                self.delScreenEffect(tag)
                self.addScreenEffect(tag, lv, path, lastTime, autoRemove, fadeIn, fadeOut, ignoreSwitch, isSkill)

    def startScreenEffectByPath(self, tag, lv, lastTime, path, fadeIn, fadeOut):
        if gameglobal.ENABLE_SCREEN_EFFECT:
            if path:
                self.delScreenEffect(tag)
                self.addScreenEffect(tag, lv, path, lastTime, True, fadeIn, fadeOut, False, False)

    def addScreenEffect(self, tag, lv, path, lastTime, autoRemove = True, fadeIn = 0, fadeOut = 0, ignoreSwitch = False, isSkill = True):
        if isSkill and not gameglobal.ENABLE_SKILL_SCREEN_EFFECT and not ignoreSwitch:
            return
        if gameglobal.ENABLE_SCREEN_EFFECT:
            if lv == -1:
                if autoRemove and lastTime:
                    callback = BigWorld.callback(lastTime, Functor(self.delScreenEffect, tag, True))
                else:
                    callback = None
                self.dict[tag] = (path, callback)
            elif lv >= self.lv:
                self.lv = lv
                self.tag = tag
                self.path = path
                if autoRemove and lastTime:
                    self.callback = BigWorld.callback(lastTime, Functor(self.delScreenEffect, tag, True))
            self.showScreenEffect(fadeIn, fadeOut)

    def delScreenEffect(self, tag, refresh = False):
        hasFound = False
        if self.tag == tag:
            hasFound = True
            self.lv = 0
            self.tag = 0
            self.path = None
            if self.callback:
                BigWorld.cancelCallback(self.callback)
                self.callback = None
        elif tag in self.dict:
            hasFound = True
            path, callback = self.dict[tag]
            if callback:
                BigWorld.cancelCallback(callback)
            del self.dict[tag]
        if hasFound and refresh:
            self.showScreenEffect()

    def showScreenEffect(self, fadeIn = 0, fadeOut = 0):
        path = []
        for tag, value in self.dict.items():
            path.append(value[0])

        if self.path:
            path.append(self.path)
        if path:
            BigWorld.setScreenVisualTimeIn(fadeIn)
            BigWorld.setScreenVisualTimeOut(fadeOut)
        gamelog.info('BGF@showScreenEffect', path)
        BigWorld.setScreenVisualEffects(*path)

    def clear(self):
        self.reset()
        self.showScreenEffect()


ins = ScreenEffectManager.getInstance()

def getScreenInfo(id):
    data = SED.data.get(id, {})
    if data:
        lv = data.get('priority', 0)
        lastTime = data.get('lastTime', 0)
        path = data.get('screenEffectPath', '')
        path = DEFAULT_PATH + '%s/%s.model' % (path, path)
        fadeIn = data.get('fadeIn', 0)
        fadeOut = data.get('fadeOut', 0)
        ignoreSwitch = data.get('ignoreSwitch', 0)
        return (lv,
         lastTime,
         path,
         fadeIn,
         fadeOut,
         ignoreSwitch)
    return (0, 0, None, 0, 0)


def startEffect(tag, id):
    ins.startScreenEffect(tag, id, True, False)


def startEffectByPath(tag, lv, lastTime, path, fadeIn, fadeOut):
    ins.startScreenEffectByPath(tag, lv, lastTime, path, fadeIn, fadeOut)


def startSkillEffect(tag, id):
    ins.startScreenEffect(tag, id, True, True)


def delEffect(tag):
    ins.delScreenEffect(tag, True)


def startEffects(tag, screenEffs, isSkill = True, owner = None):
    if owner and owner.getEffectLv() < gameglobal.EFFECT_MID:
        return
    l = len(screenEffs)
    t = 0
    for i in xrange(0, l):
        if screenEffs[i]:
            lv, lastTime, path, fadeIn, fadeOut, ignoreSwitch = getScreenInfo(screenEffs[i])
            if path:
                if t == 0:
                    ins.addScreenEffect(tag, lv, path, lastTime, True, fadeIn, fadeOut, ignoreSwitch, isSkill)
                elif i != l - 1:
                    BigWorld.callback(t, Functor(ins.addScreenEffect, tag, lv, path, lastTime, False, fadeIn, fadeOut, ignoreSwitch, isSkill))
                else:
                    BigWorld.callback(t, Functor(ins.addScreenEffect, tag, lv, path, lastTime, True, fadeIn, fadeOut, ignoreSwitch, isSkill))
                t += lastTime


def newSway(duration1, duration2, threshold, rotationAmp, amp, frequency, controlPts, ent, priority = gameglobal.SWAY_PRIORITY_LOW):
    global SWAY_PRIORITY
    oldPrio = SWAY_PRIORITY[0]
    endTime = SWAY_PRIORITY[1]
    if time.time() < endTime:
        if oldPrio > priority:
            return
    if gameglobal.rds.GameState > gametypes.GS_LOGIN:
        if BigWorld.player().ap.dcursor.pitch < -1.3:
            return
        if not gameglobal.ENABLE_SHAKE_CAMERA:
            return
        if gameglobal.ENABLE_SHAKE_CAMERA and not ent or ent != BigWorld.player():
            return
    cam = BigWorld.camera()
    if hasattr(cam, 'newsway'):
        try:
            cam.uprightDirection = (0, 1, 0)
            cam.newsway(duration1, duration2, threshold, rotationAmp, amp, frequency, controlPts)
            SWAY_PRIORITY = [priority, time.time() + duration1 + duration2]
        except:
            pass


def swayCamera(duration, frequency, verticalAmplitude, horizontalAmplitude, playerOnly, decayDist, delayTime, ent):
    if gameglobal.rds.GameState > gametypes.GS_LOGIN:
        if not gameglobal.ENABLE_SHAKE_CAMERA:
            return
        if gameglobal.ENABLE_SHAKE_CAMERA:
            if ent and ent.getEffectLv() < gameglobal.EFFECT_MID:
                return
    BigWorld.callback(delayTime, Functor(__swayCallBack, duration, frequency, verticalAmplitude, horizontalAmplitude, playerOnly, decayDist, ent))


def __swayCallBack(duration, frequency, verticalAmplitude, horizontalAmplitude, playerOnly, decayDist, ent):
    cam = BigWorld.camera()
    if hasattr(cam, 'sway'):
        if playerOnly:
            if ent:
                if ent == BigWorld.player():
                    cam.sway(duration, (horizontalAmplitude, verticalAmplitude, horizontalAmplitude), frequency)
            else:
                cam.sway(duration, (horizontalAmplitude, verticalAmplitude, horizontalAmplitude), frequency)
        else:
            dist = ent != None and (ent.position - BigWorld.player().position).length or 0
            scale = max(0.0, 1.0 - dist / float(decayDist))
            amplitude = (horizontalAmplitude * scale, verticalAmplitude * scale, horizontalAmplitude * scale)
            cam.sway(duration, amplitude, frequency)


def shakeCamera(duration, x, y, z, playerOnly, decayDist, delayTime, ent):
    if gameglobal.rds.GameState > gametypes.GS_LOGIN:
        if not gameglobal.ENABLE_SHAKE_CAMERA:
            return
        if gameglobal.ENABLE_SHAKE_CAMERA:
            if ent and ent.getEffectLv() < gameglobal.EFFECT_MID:
                return
    BigWorld.callback(delayTime, Functor(__shakeCallBack, duration, x, y, z, playerOnly, decayDist, ent))


def __shakeCallBack(duration, x, y, z, playerOnly, decayDist, ent):
    cam = BigWorld.camera()
    if hasattr(cam, 'shake'):
        if playerOnly:
            if ent:
                if ent == BigWorld.player():
                    cam.shake(duration, (x, y, z))
            else:
                cam.shake(duration, (x, y, z))
        else:
            dist = ent != None and (ent.position - BigWorld.player().position).length or 0
            scale = max(0.0, 1.0 - dist / float(decayDist))
            x *= scale
            y *= scale
            z *= scale
            cam.shake(duration, (x, y, z))


def playCameraPush(params):
    gameglobal.rds.cam.setAdaptiveFov()
    fov = gameglobal.rds.cam.getAdaptiveFov()
    strength = gameglobal.SHAKE_CAMERA_STRENGTH
    rampFov = fov - (fov - float(params[0]) * 0.01745329) * strength / 10.0
    if rampFov <= 0 or rampFov >= math.pi:
        return
    BigWorld.projection().rampFov(rampFov, float(params[1]))
    cb = BigWorld.callback(float(params[1]) + float(params[2]), Functor(gameglobal.rds.cam.restoreCameraFov, float(params[3])))
    p = BigWorld.player()
    if p:
        p.zoomInHandler = cb


def showDarkAngle(isShow):
    if isShow:
        startEffect(gameglobal.EFFECT_TAG_DARK_ANGLE, DARK_ANGLE_EFFECT)
    else:
        delEffect(gameglobal.EFFECT_TAG_DARK_ANGLE)


def canIgnoreSwitch(id):
    return SED.data.get(id, {}).get('ignoreSwitch', 0)
