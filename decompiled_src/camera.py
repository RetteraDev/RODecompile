#Embedded file name: /WORKSPACE/data/entities/client/helpers/camera.o
import math
import BigWorld
import Math
import ResMgr
import gametypes
import gameglobal
import clientcom
import keys
import gamelog
import appSetting
from guis import uiConst
from helpers import charRes
from callbackHelper import Functor
from data import zaiju_data as ZD
from data import equip_data as ED
from data import horsewing_camera_data as HCD
from data import sys_config_data as SCD
from data import interactive_data as ITAD
from data import simple_qte_data as SQD
from data import multi_carrier_data as MCD
D2 = [0.65,
 1.17,
 3.25,
 4.16,
 4.16,
 5.85,
 7.67,
 7.8,
 8.45,
 8.84,
 9.1,
 9.75,
 10.4,
 11.05,
 11.7,
 12.35,
 13.0,
 14.3,
 15.6,
 16.9,
 18.2,
 19.5]
H2 = [0.85,
 0.8,
 0.9,
 0.6,
 1.0,
 0.9,
 0.85,
 0.8,
 0.78,
 0.75,
 0.7,
 0.75,
 0.8,
 0.85,
 0.9,
 0.95,
 1.0,
 1.0,
 1.0,
 1.0,
 1.0,
 1.0]
T2 = [0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1]
HT2 = [0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1]
KEY2 = [0,
 1,
 2,
 3,
 4,
 5,
 6,
 7,
 8,
 9,
 10,
 11,
 12,
 13,
 14,
 15,
 16,
 17,
 18,
 19,
 20,
 21]
MH2 = [0.85,
 0.8,
 0.9,
 0.6,
 1.0,
 0.9,
 0.85,
 0.8,
 0.78,
 0.75,
 0.7,
 0.75,
 0.8,
 0.85,
 0.9,
 0.95,
 1.0,
 1.0,
 1.0,
 1.0,
 1.0,
 1.0]
D1 = [0.65,
 1.17,
 3.25,
 4.16,
 4.16,
 5.85,
 7.67,
 7.8,
 8.45,
 8.84,
 9.1,
 9.75,
 10.4,
 11.05,
 11.7,
 12.35,
 13.0,
 14.3,
 15.6,
 16.9,
 18.2,
 19.5]
H1 = [0.9,
 0.8,
 0.7,
 0.58,
 0.85,
 0.85,
 0.83,
 0.79,
 0.75,
 0.72,
 0.7,
 0.73,
 0.78,
 0.85,
 0.91,
 0.96,
 1.0,
 1.0,
 1.0,
 1.0,
 1.0,
 1.0]
T1 = [0.3,
 0.3,
 0.3,
 0.3,
 0.3,
 0.3,
 0.3,
 0.3,
 0.3,
 0.3,
 0.3,
 0.3,
 0.3,
 0.3,
 0.3,
 0.3,
 0.3,
 0.3,
 0.3,
 0.3,
 0.3]
HT1 = [0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1]
KEY1 = [0,
 1,
 2,
 3,
 4,
 5,
 6,
 7,
 8,
 9,
 10,
 11,
 12,
 13,
 14,
 15,
 16,
 17,
 18,
 19,
 20,
 21]
MH1 = [0.85,
 0.8,
 0.9,
 0.6,
 1.0,
 0.9,
 0.85,
 0.8,
 0.78,
 0.75,
 0.7,
 0.75,
 0.8,
 0.85,
 0.9,
 0.95,
 1.0,
 1.0,
 1.0,
 1.0,
 1.0,
 1.0]
D0 = [0.65,
 1.17,
 3.25,
 4.16,
 4.16,
 5.85,
 7.67,
 7.8,
 8.45,
 8.84,
 9.1,
 9.75,
 10.4,
 11.05,
 11.7,
 12.35,
 13.0,
 14.3,
 15.6,
 16.9,
 18.2,
 19.5]
H0 = [0.85,
 0.8,
 0.9,
 0.6,
 1.0,
 0.9,
 0.85,
 0.8,
 0.78,
 0.75,
 0.7,
 0.75,
 0.8,
 0.85,
 0.9,
 0.95,
 1.0,
 1.0,
 1.0,
 1.0,
 1.0,
 1.0]
T0 = [0.5,
 0.5,
 0.5,
 0.5,
 0.5,
 0.5,
 0.5,
 0.5,
 0.5,
 0.5,
 0.5,
 0.5,
 0.5,
 0.5,
 0.5,
 0.5,
 0.5,
 0.5,
 0.5,
 0.5,
 0.5]
HT0 = [0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1,
 0.1]
KEY0 = [0,
 1,
 2,
 3,
 4,
 5,
 6,
 7,
 8,
 9,
 10,
 11,
 12,
 13,
 14,
 15,
 16,
 17,
 18,
 19,
 20,
 21]
MH0 = [0.85,
 0.8,
 0.9,
 0.6,
 1.0,
 0.9,
 0.85,
 0.8,
 0.78,
 0.75,
 0.7,
 0.75,
 0.8,
 0.85,
 0.9,
 0.95,
 1.0,
 1.0,
 1.0,
 1.0,
 1.0,
 1.0]
KEYDIST = {10004: 0.9,
 10005: 1.2,
 10006: 1.2,
 10007: 1.2,
 10009: 1.2}
NEAR_PLANE_MAX = 0.8
NEAR_PLANE_MIN = 0.4

class Camera(object):
    BOSS_HEIGT = 4
    BOSS_TIME = 0.3
    HIDE_DIST = 1.5
    DELTA_Z = 120
    CAMERA_SCROLL_NUM = 22
    CAMERA_BOSS_BATTLE = 4
    CAMERA_FIRST_PERSON = 5
    CAMERA_QUITE_FIRST_PERSON = 6
    DELTA_T = 0.2
    BOUND_REMAIN = 0.4
    BOUND_MAX_REMAIN = 5.0
    FLY_HEIGHT_OFFSET = 0.5
    FLY_DIST_OFFSET = 0.1
    RIDE_RATIO = 1.3
    FIRSTPERSON_HEIGHT_RAIO = 1.05
    FIRSTPERSON_OUT_SCROLL_NUM = 7
    FIRSTPERSON_TIME = 0.2
    BLOCK_AREA = {2: 1,
     1: 1,
     3: 1}
    INITIAL_SCROLL_NUM = 6
    NORMAL_MIN_PITCH = -1.57
    NORMAL_MAX_PITCH = 1.57
    PHOTO_MIN_PITCH = -1.57
    PHOTO_MAX_PITCH = 1.57
    MOUSE_MODE_PITCH = -0.77
    MIN_DIS = 0.5
    MAX_DIS = 12.0
    BLOCK_TIME = 0.5
    MOUSE_MODE_DIST_RATIO = 1.3

    def __init__(self):
        super(Camera, self).__init__()
        self.cc = None
        self.ccMatrixProvider = None
        self.scrollRange = None
        self.camBindState = -1
        self.enableScroll = True
        self.cameraMoveSpeed = 1.0
        self.dofCaps = False
        self.dataInfo = None
        self.currentScrollNum = self.INITIAL_SCROLL_NUM
        self.keyDist = [0.0,
         0.0,
         0.0,
         0.0]
        self.keyHeight = [0.0,
         0.0,
         0.0,
         0.0]
        self.headHeight = 0.3
        self.heightConfigs = {}
        self.configCamera()
        self.setScrollSpeed()
        self.mouseModePitch = self.MOUSE_MODE_PITCH
        self.setAdaptiveFov()

    def setAdaptiveFov(self):
        if gameglobal.rds.GameState <= gametypes.GS_LOGIN:
            return
        aspect = float(BigWorld.screenWidth()) / BigWorld.screenHeight()
        if aspect > 1.34:
            BigWorld.projection().fov = gameglobal.CAMERA_FOV_51
        else:
            BigWorld.projection().fov = gameglobal.CAMERA_FOV_68

    def getAdaptiveFov(self):
        return BigWorld.projection().fov

    def configCamera(self, configSect = None):
        cc = BigWorld.CursorCamera()
        cc.source = BigWorld.dcursor().matrix
        cc.target = BigWorld.PlayerMatrix()
        cc.movementHalfLife = 0.1
        cc.turningHalfLife = 0.1
        cc.maxDistHalfLife = 0.14
        cc.boundRemain = self.BOUND_REMAIN
        cc.maxVelocity = 100
        cc.followMovementHalfLife = 0.0
        cc.minNearPlane = 0.1
        self.ccHeight = 2
        self.cc = cc
        self.ccMatrixProvider = cc.matrix
        BigWorld.camera(cc)
        self.loadHeigtByTrack()
        cc.ignoreMaterialKind(gameglobal.GLASS, gameglobal.DIE, gameglobal.TREE, gameglobal.TELEPORT, gameglobal.NOCOLLIDECAMERA)

    def camera(self, idx):
        return self.cc

    def getDefaultFov(self):
        aspect = float(BigWorld.screenWidth()) / BigWorld.screenHeight()
        fov = gameglobal.CAMERA_FOV_68
        if aspect > 1.34:
            fov = gameglobal.CAMERA_FOV_51
        return fov

    def restoreCameraFov(self, halfLifeTime):
        fov = self.getDefaultFov()
        BigWorld.projection().rampFov(fov, halfLifeTime)

    def getRealDist(self):
        if gameglobal.rds.GameState == gametypes.GS_PLAYGAME:
            p = BigWorld.player()
            if p.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
                horsewingCameraId = ED.data.get(p.bianshen[1], {}).get('horsewingCameraId', None)
                horsewingCameraData = HCD.data.get(horsewingCameraId, {})
                dist = horsewingCameraData.get('dist', None)
                if dist:
                    return dist
            elif hasattr(p, 'isRidingTogetherAsVice') and p.isRidingTogetherAsVice():
                if hasattr(p, 'tride'):
                    header = p.tride.getHeader()
                    if header and header.inWorld:
                        horsewingCameraId = ED.data.get(header.bianshen[1], {}).get('horsewingCameraId', None)
                        horsewingCameraData = HCD.data.get(horsewingCameraId, {})
                        dist = horsewingCameraData.get('dist', None)
                        if dist:
                            return dist
            elif hasattr(p, 'inFightObserve') and p.inFightObserve():
                dist = SCD.data.get('shaXingCamDist', None)
                if dist:
                    return dist
            elif hasattr(p, 'getInteractiveObjTId') and p.getInteractiveObjTId():
                dist = ITAD.data.get(p.getInteractiveObjTId(), {}).get('camDist', None)
                if dist:
                    return dist
            elif hasattr(p, 'isOnCarrier') and p.isOnCarrier():
                dist = p.carrier.getCamDist()
                if dist:
                    return dist
        return self.D

    def getRealHeight(self):
        if gameglobal.rds.GameState == gametypes.GS_PLAYGAME:
            p = BigWorld.player()
            if p.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
                horsewingCameraId = ED.data.get(p.bianshen[1], {}).get('horsewingCameraId', None)
                horsewingCameraData = HCD.data.get(horsewingCameraId, {})
                height = horsewingCameraData.get('height', None)
                if height:
                    return height
            elif hasattr(p, 'isRidingTogetherAsVice') and p.isRidingTogetherAsVice():
                if hasattr(p, 'tride'):
                    header = p.tride.getHeader()
                    if header and header.inWorld:
                        horsewingCameraId = ED.data.get(header.bianshen[1], {}).get('horsewingCameraId', None)
                        horsewingCameraData = HCD.data.get(horsewingCameraId, {})
                        height = horsewingCameraData.get('height', None)
                        if height:
                            return height
            elif hasattr(p, 'inFightObserve') and p.inFightObserve() and not p.isInBfDota():
                height = SCD.data.get('shaXingCamHeight', None)
                if height:
                    return height
            elif hasattr(p, 'getInteractiveObjTId') and p.getInteractiveObjTId():
                height = ITAD.data.get(p.getInteractiveObjTId(), {}).get('camHeight', None)
                if height:
                    return height
            elif hasattr(p, 'isOnCarrier') and p.isOnCarrier():
                height = p.carrier.getCamHeight()
                if height:
                    return height
        return self.H

    def getRealTime(self):
        if gameglobal.rds.GameState == gametypes.GS_PLAYGAME:
            p = BigWorld.player()
            if p.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
                horsewingCameraId = ED.data.get(p.bianshen[1], {}).get('horsewingCameraId', None)
                horsewingCameraData = HCD.data.get(horsewingCameraId, {})
                deltaTime = horsewingCameraData.get('deltaTime', None)
                if deltaTime:
                    return deltaTime
            elif hasattr(p, 'isRidingTogetherAsVice') and p.isRidingTogetherAsVice():
                if hasattr(p, 'tride'):
                    header = p.tride.getHeader()
                    if header and header.inWorld:
                        horsewingCameraId = ED.data.get(header.bianshen[1], {}).get('horsewingCameraId', None)
                        horsewingCameraData = HCD.data.get(horsewingCameraId, {})
                        deltaTime = horsewingCameraData.get('deltaTime', None)
                        if deltaTime:
                            return deltaTime
            elif hasattr(p, 'inFightObserve') and p.inFightObserve():
                deltaTime = SCD.data.get('shaXingCamDeltaTime', None)
                if deltaTime:
                    return deltaTime
        return self.T

    def getRealHT(self):
        if gameglobal.rds.GameState == gametypes.GS_PLAYGAME:
            p = BigWorld.player()
            if p.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
                horsewingCameraId = ED.data.get(p.bianshen[1], {}).get('horsewingCameraId', None)
                horsewingCameraData = HCD.data.get(horsewingCameraId, {})
                halfTime = horsewingCameraData.get('halfTime', None)
                if halfTime:
                    return halfTime
            elif hasattr(p, 'isRidingTogetherAsVice') and p.isRidingTogetherAsVice():
                if hasattr(p, 'tride'):
                    header = p.tride.getHeader()
                    if header and header.inWorld:
                        horsewingCameraId = ED.data.get(header.bianshen[1], {}).get('horsewingCameraId', None)
                        horsewingCameraData = HCD.data.get(horsewingCameraId, {})
                        halfTime = horsewingCameraData.get('halfTime', None)
                        if halfTime:
                            return halfTime
            elif hasattr(p, 'inFightObserve') and p.inFightObserve():
                halfTime = SCD.data.get('shaXingCamHalfTime', None)
                if halfTime:
                    return halfTime
        return self.HT

    def getRealKey(self):
        if gameglobal.rds.GameState == gametypes.GS_PLAYGAME:
            p = BigWorld.player()
            if p.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
                horsewingCameraId = ED.data.get(p.bianshen[1], {}).get('horsewingCameraId', None)
                horsewingCameraData = HCD.data.get(horsewingCameraId, {})
                key = horsewingCameraData.get('key', None)
                if key:
                    return key
            elif hasattr(p, 'isRidingTogetherAsVice') and p.isRidingTogetherAsVice():
                if hasattr(p, 'tride'):
                    header = p.tride.getHeader()
                    if header and header.inWorld:
                        horsewingCameraId = ED.data.get(header.bianshen[1], {}).get('horsewingCameraId', None)
                        horsewingCameraData = HCD.data.get(horsewingCameraId, {})
                        key = horsewingCameraData.get('key', None)
                        if key:
                            return key
            elif hasattr(p, 'inFightObserve') and p.inFightObserve():
                key = SCD.data.get('shaXingCamKey', None)
                if key:
                    return key
            elif hasattr(p, 'isOnCarrier') and p.isOnCarrier():
                camKey = p.carrier.getCamKey()
                if camKey:
                    return camKey
        return self.KEY

    def reloadCamera(self):
        global KEY1
        global H1
        global T1
        global D1
        self.D = D1
        self.T = T1
        self.H = H1
        self.HT = HT1
        self.KEY = KEY1

    def checkBlock(self, step):
        if self.currentScrollNum - step <= 0:
            step = self.currentScrollNum
        elif self.currentScrollNum - step >= self.SCROLL_NUM:
            step = self.currentScrollNum - self.SCROLL_NUM + 1
        for blockPos in self.BLOCK_AREA.keys():
            oldKey = self.getKey(self.currentScrollNum)
            newKey = self.getKey(self.currentScrollNum - step)
            if oldKey > blockPos and newKey <= blockPos:
                return (self.getRealKey().index(blockPos), True)

        return (self.currentScrollNum - step, False)

    def isInMouseMode(self):
        return hasattr(BigWorld.player(), 'getOperationMode') and BigWorld.player().getOperationMode() == gameglobal.MOUSE_MODE

    def resetDcursorPitch(self):
        dc = BigWorld.dcursor()
        if self.isInMouseMode():
            if gameglobal.ENABLE_FREE_ROTATE_CAM or BigWorld.player().ap.freeRotateCam:
                dc.minPitch = self.NORMAL_MIN_PITCH
                dc.maxPitch = self.NORMAL_MAX_PITCH
            else:
                dc.pitch = self.mouseModePitch
                dc.minPitch = self.mouseModePitch
                dc.maxPitch = self.mouseModePitch
        else:
            dc.minPitch = self.NORMAL_MIN_PITCH
            dc.maxPitch = self.NORMAL_MAX_PITCH

    def changeView(self, step):
        isBlock = False
        p = BigWorld.player()
        oldScrollNum = self.currentScrollNum
        if oldScrollNum <= -1 and step > 0:
            self.currentScrollNum = -1
        else:
            if oldScrollNum == 1 and step > 0:
                if self.checkNeedNewCreateCurve():
                    self.enterNewFirstPerson()
                    if BigWorld.projection().nearPlane < NEAR_PLANE_MAX:
                        BigWorld.projection().nearPlane = NEAR_PLANE_MAX
                    return
                self.enterFirstPerson()
            elif oldScrollNum <= 0 and step < 0:
                self.currentScrollNum = 1
                if self.checkNeedNewCreateCurve():
                    self.quitNewFirstPerson()
                else:
                    self.quitFirstPerson()
            self.currentScrollNum, isBlock = self.checkBlock(step)
            if self.currentScrollNum == oldScrollNum:
                return
            if self.currentScrollNum == 0 and step > 0:
                isBlock = True
            if self.checkNeedNewCreateCurve():
                self.cc.cameraDHProvider = self.newCreateCurve()
                if self.currentScrollNum == 1:
                    self.cc.boundRemain = self.BOUND_MAX_REMAIN
                    BigWorld.enablePlayerFade(False)
                else:
                    self.cc.boundRemain = self.BOUND_REMAIN
                    BigWorld.enablePlayerFade(True)
                p.resetFootIK()
            else:
                self.cc.cameraDHProvider = self.createCurve(oldScrollNum)
        if isBlock and not self.isInMouseMode():
            self.passCameraBindWaist()
            self.enableScroll = False
            BigWorld.callback(self.BLOCK_TIME, Functor(self.setEnableScroll, True))
        self.resetDepthOfField()
        self.resetNearPlane()

    def resetDepthOfField(self):
        if self.currentScrollNum > 0:
            if self.checkNeedSetDepthOfField() and self.currentScrollNum <= 3:
                dist = self.keyDist[self.currentScrollNum]
                self.setDepthOfField(True, dist)
            else:
                self.setDepthOfField(False)
        else:
            self.setDepthOfField(False)

    def resetNearPlane(self):
        nearPlane = BigWorld.projection().nearPlane
        if self.currentScrollNum == 1:
            if nearPlane > NEAR_PLANE_MIN:
                BigWorld.projection().nearPlane = NEAR_PLANE_MIN
        elif nearPlane < NEAR_PLANE_MAX:
            BigWorld.projection().nearPlane = NEAR_PLANE_MAX

    def checkNeedNewCreateCurve(self):
        p = BigWorld.player()
        if self.currentScrollNum in (1, 2, 3) and not p.inFly and not p.isRidingTogetherAsVice() and not p.isInCoupleRideAsRider() and not p.inRiding() and not p.inCarrousel() and not p.isOnCarrier() and (keys.CAPS_HAND_FREE in p.am.matchCaps or keys.CAPS_WEAR in p.am.matchCaps):
            return True
        return False

    def setDepthOfField(self, enable, dist = None):
        if gameglobal.rds.ui.quest.isShow or gameglobal.rds.ui.npcV2.isShow or gameglobal.rds.ui.wingWorldRemoveSeal.widget:
            return
        if enable:
            if not appSetting.VideoQualitySettingObj.isDofForceEnable():
                BigWorld.enableU3DOF(True)
            BigWorld.setDepthOfField(True, dist, 0.02, 0.5, 0.2, 0.7)
        else:
            BigWorld.setDepthOfField(False)
            if not appSetting.VideoQualitySettingObj.isDofForceEnable():
                BigWorld.enableU3DOF(False)

    def checkNeedSetDepthOfField(self):
        p = BigWorld.player()
        if p.isMoving or p.inRiding() or p.inFly or p.bianshen[0] != gametypes.BIANSHEN_HUMAN:
            return False
        return True

    def awayFrom(self, step):
        if not self.enableScroll:
            return
        self.changeView(step)

    def closeTo(self, step):
        if not self.enableScroll:
            return
        self.changeView(step)

    def getKey(self, pos):
        if pos >= 0 and pos < self.SCROLL_NUM:
            return self.getRealKey()[pos]
        elif pos == -1:
            return -1
        else:
            return self.getRealKey()[self.SCROLL_NUM - 1]

    def getCoupleEmoteNodeHeight(self, nodeName, forceNodeUpdate = True):
        other = BigWorld.entity(BigWorld.player().getOtherIDInCoupleEmote())
        if not other or not other.inWorld:
            return 0
        return clientcom.getModeNodePosition(other.model, nodeName, forceNodeUpdate)[1] - other.position[1]

    def calcHeight(self, key, forceNodeUpdate = True):
        p = BigWorld.player()
        if not p:
            return 0.0
        elif key == -1:
            return self.FIRSTPERSON_HEIGHT_RAIO * self.modelHeight
        elif hasattr(self, 'modelHeight'):
            height = self.getRealHeight()[key] * self.modelHeight
            if not p.inFly and not p.inRiding() and not (hasattr(p, 'isRidingTogetherAsVice') and p.isRidingTogetherAsVice()):
                if key == 3:
                    if p.isInCoupleRideAsRider():
                        height = self.getCoupleEmoteNodeHeight('biped', forceNodeUpdate)
                    height = height - 0.1
                elif key == 2:
                    if p.isInCoupleRideAsRider():
                        height = self.getCoupleEmoteNodeHeight('biped Spine2', forceNodeUpdate)
                elif key == 1:
                    if p.isInCoupleRideAsRider():
                        height = self.getCoupleEmoteNodeHeight('biped Head', forceNodeUpdate)
                if height < 0.3:
                    height = 0.3
                return height
            if p.inFly in (gametypes.IN_FLY_TYPE_WING, gametypes.IN_FLY_TYPE_ZAIJU, gametypes.IN_FLY_OBSERVER):
                height += self.FLY_HEIGHT_OFFSET
            elif p.inRiding():
                height += p.getModelHeight() / 2
                height += p.getCameraFloatageHeight()
            elif hasattr(p, 'isRidingTogetherAsVice') and p.isRidingTogetherAsVice():
                if hasattr(p, 'tride'):
                    header = p.tride.getHeader()
                    if header:
                        if header.inFly in (gametypes.IN_FLY_TYPE_WING, gametypes.IN_FLY_TYPE_ZAIJU, gametypes.IN_FLY_OBSERVER):
                            height += self.FLY_HEIGHT_OFFSET
                        elif header.inRiding():
                            height += header.getModelHeight() / 2
                            height += header.getCameraFloatageHeight()
            return height
        else:
            return self.cc.pivotPosition[1]

    def calcXOffset(self):
        p = BigWorld.player()
        if getattr(p, 'bianshen', None) and p.bianshen[0] == gametypes.BIANSHEN_ZAIJU:
            return ZD.data.get(p.bianshen[1], {}).get('cameraXOffset', 0)
        return 0

    def calcDist(self, key, height = 0.0):
        global KEYDIST
        p = BigWorld.player()
        if not p:
            return 0.0
        if key == -1:
            return 0
        dist = self.getRealDist()[key]
        if not p.inFly and not p.inRiding() and not (hasattr(p, 'isRidingTogetherAsVice') and p.isRidingTogetherAsVice()) and not clientcom.isInDotaZaiju(p) and not (hasattr(p, 'isOnCarrier') and p.isOnCarrier()):
            if key == 3:
                fov = BigWorld.projection().fov
                dist = (self.modelHeight - height + 0.3) * 1.45 / math.tan(fov / 2.0)
                dist = self.modelHeight
                if fov < gameglobal.CAMERA_FOV_51:
                    dist = dist + 0.7
                else:
                    dist = dist + 0.5
                self.keyDist[key] = dist
                return dist
            if key == 2:
                fov = gameglobal.CAMERA_FOV_51
                BigWorld.projection().rampFov(fov, gameglobal.TIME_FOV)
                dist = (self.modelHeight - height + 0.3) * 1.35 / math.tan(fov / 2.0)
                self.keyDist[key] = dist
                return dist
            if key == 1:
                if p.inMoving():
                    fov = gameglobal.CAMERA_FOV_51
                else:
                    fov = gameglobal.DIST_FOV
                BigWorld.projection().rampFov(fov, gameglobal.TIME_FOV)
                dist = (self.modelHeight - height + 0.3) / math.tan(fov / 2.0)
                if dist <= self.HIDE_DIST:
                    dist = self.HIDE_DIST + 0.1
                dist = KEYDIST.get(p.fashion.modelID, dist)
                self.keyDist[key] = dist
                return dist
            if key == 0:
                fov = gameglobal.CAMERA_FOV_51
                BigWorld.projection().rampFov(fov, gameglobal.FIRST_TIME_FOV)
            self.cc.boundRemain = self.BOUND_REMAIN
        else:
            scrollRange = self.getScrollRange()
            if scrollRange:
                if dist <= scrollRange[0]:
                    dist = scrollRange[0]
                elif dist >= scrollRange[1]:
                    dist = scrollRange[1]
            if p:
                if p.inRiding():
                    dist *= self.RIDE_RATIO + 0.2
                elif p.inFly:
                    dist = dist + 0.1
            if hasattr(p, 'isRidingTogetherAsVice') and p.isRidingTogetherAsVice():
                if hasattr(p, 'tride'):
                    header = p.tride.getHeader()
                    if header:
                        scrollRange = self.getScrollRangeByEnt(header)
                        if scrollRange:
                            if dist <= scrollRange[0]:
                                dist = scrollRange[0]
                            elif dist >= scrollRange[1]:
                                dist = scrollRange[1]
                        if header.inRiding():
                            dist *= self.RIDE_RATIO + 0.2
                        elif header.inFly:
                            dist = dist + 0.1
        if key == 0:
            if dist >= self.HIDE_DIST:
                dist = self.HIDE_DIST - 0.5
        return dist

    def calcHalfTime(self, key):
        return self.getRealHT()[key] * self.cameraMoveSpeed

    def setEnableScroll(self, flag):
        self.enableScroll = flag

    def passCameraBindWaist(self):
        k = self.getKey(self.currentScrollNum)
        if k in self.BLOCK_AREA.keys():
            dc = BigWorld.dcursor()
            if self.BLOCK_AREA[k]:
                dc.minPitch = self.PHOTO_MIN_PITCH
                dc.maxPitch = self.PHOTO_MAX_PITCH
            else:
                dc.minPitch = self.NORMAL_MIN_PITCH
                dc.maxPitch = self.NORMAL_MAX_PITCH

    def handleKeyEvent(self, down, key, vk, mods):
        return False

    def handleMouseEvent(self, dx, dy, dz):
        p = BigWorld.player()
        isInBfDotaChooseHero = False
        if p:
            isInBfDotaChooseHero = getattr(p, 'isInBfDotaChooseHero', False)
        if gameglobal.rds.GameState == gametypes.GS_PLAYGAME and gameglobal.SCENARIO_PLAYING != gameglobal.SCENARIO_PLAYING_TRACK_CAMERA and not isInBfDotaChooseHero:
            step = dz / self.DELTA_Z
            if step < 0:
                self.awayFrom(step)
            else:
                self.closeTo(step)
            if hasattr(p, 'getOperationMode') and p.getOperationMode() == gameglobal.ACTION_MODE:
                p.ap.resetAimCrossPos(self.currentScrollNum)
        if isInBfDotaChooseHero:
            if dz > 0:
                gameglobal.rds.ui.bfDotaChooseHeroBottom.setTurnDir(uiConst.MODEL_TURN_CLOCKWISE)
            elif dz < 0:
                gameglobal.rds.ui.bfDotaChooseHeroBottom.setTurnDir(uiConst.MODEL_TURN_ANTICLOCKWISE)
            else:
                gameglobal.rds.ui.bfDotaChooseHeroBottom.setTurnDir(uiConst.MODEL_TURN_STOP)

    def enterDashFov(self):
        if gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_PLAYING_TRACK_CAMERA:
            return
        self.setAdaptiveFov()
        BigWorld.projection().rampFov(1.0, 0.1)

    def leaveDashFov(self):
        if gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_PLAYING_TRACK_CAMERA:
            return
        self.restoreCameraFov(0.1)

    def reset(self):
        if gameglobal.rds.GameState == gametypes.GS_LOADING:
            self.cc.cameraDHProvider = None
            return
        p = BigWorld.player()
        self.modelHeight = p.getModelHeight()
        if p.bianshen[0] in (gametypes.BIANSHEN_RIDING_RB, gametypes.BIANSHEN_ZAIJU, gametypes.BIANSHEN_BIANYAO) and getattr(p.model, 'ride', None):
            self.modelHeight += p.model.ride.height * 0.3 * p.model.ride.scale[1]
        if hasattr(p, 'isRidingTogetherAsVice') and p.isRidingTogetherAsVice():
            if hasattr(p, 'tride'):
                header = p.tride.getHeader()
                if header and header.model:
                    self.modelHeight = header.getModelHeight()
                    if hasattr(header.model, 'ride'):
                        height = getattr(header.model.ride, 'height', 0)
                        scale = getattr(header.model.ride, 'scale', (1, 1, 1))[1]
                        self.modelHeight += height * 0.3 * scale
        if self.modelHeight < 0.7:
            self.modelHeight = 0.7
        self.quitFirstPerson()
        if self.currentScrollNum < 3:
            self.currentScrollNum = 3
        key = self.getKey(self.currentScrollNum)
        height = self.calcHeight(key)
        dist = self.calcDist(key)
        xOffset = self.calcXOffset()
        self.cc.cameraDHProvider = self.createLine(dist, height, 0.5, xOffset)
        BigWorld.projection().nearPlane = NEAR_PLANE_MAX
        self.cc.needfixCamera = False
        self.HIDE_DIST = self.modelHeight * gameglobal.HIDE_DIST_RATE
        self.setAdaptiveFov()
        self.cc.setHideCallback(self.cameraDistCallBack, self.HIDE_DIST)

    def getNodeHeight(self, nodeName, forceNodeUpdate = True):
        p = BigWorld.player()
        return clientcom.getModeNodePosition(p.model, nodeName, forceNodeUpdate)[1] - p.position[1]

    def cameraDistCallBack(self, dist):
        p = BigWorld.player()
        if not p:
            return
        calbackDist = self.HIDE_DIST
        if dist <= calbackDist:
            p.model.visible = False
        elif self.camBindState == self.CAMERA_QUITE_FIRST_PERSON:
            self.camBindState = -1
            if hasattr(p, 'getOpacityValue') and p.getOpacityValue()[0] != gameglobal.OPACITY_HIDE:
                p.model.visible = True
        elif hasattr(p, 'getOpacityValue') and p.getOpacityValue()[0] != gameglobal.OPACITY_HIDE:
            p.model.visible = True

    def enterFirstPerson(self):
        if self.camBindState != self.CAMERA_FIRST_PERSON:
            p = BigWorld.player()
            p.model.visible = False
            self.camBindState = self.CAMERA_FIRST_PERSON
            dist = 0
            height = self.calcHeight(0) * self.FIRSTPERSON_HEIGHT_RAIO
            self.cc.cameraDHProvider = self.createLine(dist, height, self.FIRSTPERSON_TIME)
            print 'jbx:set 0'

    def quitFirstPerson(self):
        if self.camBindState == self.CAMERA_FIRST_PERSON:
            p = BigWorld.player()
            self.currentScrollNum = 0
            key = self.getKey(self.currentScrollNum)
            dist = self.calcDist(key)
            height = self.calcHeight(key)
            self.cc.boundRemain = self.BOUND_REMAIN
            self.cc.cameraDHProvider = self.createLine(dist, height, self.FIRSTPERSON_TIME)
            self.camBindState = self.CAMERA_QUITE_FIRST_PERSON
            if hasattr(p, 'getOpacityValue') and p.getOpacityValue()[0] != gameglobal.OPACITY_HIDE:
                p.model.visible = True

    def enterBossBattle(self):
        try:
            if self.camBindState == self.CAMERA_BOSS_BATTLE:
                return
            self.oldModelHeight = self.modelHeight
            self.modelHeight = self.BOSS_HEIGT
            self.camBindState = self.CAMERA_BOSS_BATTLE
            key = self.getKey(self.currentScrollNum)
            dist = self.cc.pivotMaxDist
            height = self.calcHeight(key)
            self.cc.cameraDHProvider = self.createLine(dist, height, self.BOSS_TIME)
        except:
            pass

    def quitBossBattle(self):
        try:
            if self.camBindState == self.CAMERA_BOSS_BATTLE:
                self.camBindState = -1
                self.modelHeight = self.oldModelHeight
                key = self.getKey(self.currentScrollNum)
                dist = self.cc.pivotMaxDist
                height = self.calcHeight(key)
                self.cc.cameraDHProvider = self.createLine(dist, height, self.BOSS_TIME)
        except:
            pass

    def setMaxScrollRange(self, maxRange):
        self.MAX_DIS = maxRange
        self.setScrollRange()

    def getScrollRange(self):
        return self.getScrollRangeByEnt(BigWorld.player())

    def getScrollRangeByEnt(self, ent):
        p = BigWorld.player()
        if ent == p and hasattr(p, 'isOnCarrier') and p.isOnCarrier():
            scrollRange = ent.carrier.getCamScrollRange()
            if scrollRange:
                return scrollRange
        if hasattr(ent, '_isOnZaijuOrBianyao') and ent._isOnZaijuOrBianyao():
            beastKey = ent._getZaijuOrBianyaoNo()
            scrollRange = ZD.data.get(beastKey, {}).get('scrollRange', None)
            if scrollRange:
                return scrollRange[0:2]
        if gameglobal.rds.GameState == gametypes.GS_PLAYGAME:
            if ent.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
                horsewingCameraId = ED.data.get(ent.bianshen[1], {}).get('horsewingCameraId', None)
                horsewingCameraData = HCD.data.get(horsewingCameraId, {})
                scrollRange = horsewingCameraData.get('scrollRange', None)
                if scrollRange:
                    return scrollRange
        if hasattr(BigWorld.player(), 'inFightObserve') and BigWorld.player().inFightObserve():
            scrollRange = SCD.data.get('shaXingCamScrollRange', None)
            if scrollRange:
                return scrollRange
        if hasattr(ent, 'getInteractiveObjTId') and ent.getInteractiveObjTId():
            scrollRange = ITAD.data.get(ent.getInteractiveObjTId(), {}).get('camScrollRange', None)
            if scrollRange:
                return scrollRange
        if getattr(ent, 'inSimpleQte', False):
            cameraRange = SQD.data.get(ent.inSimpleQte, {}).get('cameraRange', ())
            if cameraRange:
                return cameraRange
        return self.scrollRange

    def setCameraOffset(self, offset):
        try:
            self.cc.targetOffset = offset
        except:
            pass

    def setScrollRange(self, ranges = None, defaultValue = None):
        p = BigWorld.player()
        if ranges == None:
            ranges = (self.MIN_DIS, self.MAX_DIS)
        if ranges != self.scrollRange:
            self.scrollRange = ranges
        if p.isInDotaZaiju():
            self._calcScrollNum(defaultValue)
        else:
            self._calcScrollNum()
        if hasattr(self, 'D'):
            if self.cc.pivotMaxDist > self.getRealDist()[self.SCROLL_NUM - 1] or p.isInDotaZaiju():
                self.currentScrollNum = self.SCROLL_NUM - 1
                key = self.getKey(self.currentScrollNum)
                dist = self.calcDist(key)
                height = self.calcHeight(key)
                self.cc.cameraDHProvider = self.createLine(dist, height, 0.5)

    def _calcScrollNum(self, dstRange = None):
        if hasattr(self, 'KEY') and self.getScrollRange():
            dstRange = dstRange if dstRange != None else self.getScrollRange()[1]
            for i, key in enumerate(self.getRealKey()):
                if self.getRealDist()[key] > dstRange:
                    self.SCROLL_NUM = i
                    return

            self.SCROLL_NUM = len(self.getRealKey())
        else:
            self.SCROLL_NUM = len(self.getRealKey())

    def createLine(self, dist, height, time, xOffetset = 0):
        v4 = Math.Vector4Animation()
        v4.oneshot = True
        keyframes = []
        moveHalfTime = self.cc.movementHalfLife
        keyframes.append((0.0, (xOffetset,
          height,
          moveHalfTime,
          self.cc.pivotMaxDist)))
        keyframes.append((time, (xOffetset,
          height,
          0,
          dist)))
        v4.duration = time
        v4.keyframes = keyframes
        return v4

    def createCurve(self, oldScrollNum):
        p = BigWorld.player()
        hOffset = self.calcXOffset()
        if BigWorld.projection().fov != gameglobal.CAMERA_FOV_51:
            BigWorld.projection().rampFov(gameglobal.CAMERA_FOV_51, gameglobal.TIME_FOV)
        v4 = Math.Vector4Animation()
        v4.oneshot = True
        keyframes = []
        keyframes.append((0.0, (hOffset,
          self.cc.pivotPosition[1],
          0,
          self.cc.pivotMaxDist)))
        oldKey = self.getKey(oldScrollNum)
        newKey = self.getKey(self.currentScrollNum)
        if newKey <= 3:
            p.modelServer.poseManager.startLookAtPose()
        else:
            p.modelServer.poseManager.stopPoseModel()
        deltaTime = 0
        if newKey > oldKey:
            i = newKey - 1
            deltaTime = self.getRealTime()[i]
            height = self.calcHeight(i + 1, False)
            dist = self.calcDist(i + 1, height)
            halfTime = self.calcHalfTime(i + 1)
            keyframes.append((deltaTime, (hOffset,
              height,
              halfTime,
              dist)))
        elif newKey < oldKey:
            i = newKey + 1
            deltaTime = self.getRealTime()[i - 1]
            height = self.calcHeight(i - 1, False)
            dist = self.calcDist(i - 1, height)
            halfTime = self.calcHalfTime(i - 1)
            keyframes.append((deltaTime, (hOffset,
              height,
              halfTime,
              dist)))
        else:
            height = self.calcHeight(newKey, False)
            dist = self.calcDist(newKey, height)
            halfTime = self.calcHalfTime(newKey)
            keyframes.append((self.DELTA_T, (hOffset,
              height,
              halfTime,
              dist)))
            deltaTime = self.DELTA_T
        gamelog.debug('createCurve', deltaTime, keyframes)
        v4.duration = deltaTime
        v4.keyframes = keyframes
        return v4

    def enterNewFirstPerson(self):
        if self.camBindState != self.CAMERA_FIRST_PERSON:
            p = BigWorld.player()
            p.model.visible = False
            self.camBindState = self.CAMERA_FIRST_PERSON
            self.currentScrollNum = -1

    def quitNewFirstPerson(self):
        if self.camBindState == self.CAMERA_FIRST_PERSON:
            p = BigWorld.player()
            self.currentScrollNum = 1
            self.camBindState = self.CAMERA_QUITE_FIRST_PERSON
            if hasattr(p, 'getOpacityValue') and p.getOpacityValue()[0] != gameglobal.OPACITY_HIDE:
                p.model.visible = True

    def newCreateCurve(self):
        p = BigWorld.player()
        newKey = self.getKey(self.currentScrollNum)
        if newKey <= 3:
            p.modelServer.poseManager.startLookAtPose()
        else:
            p.modelServer.poseManager.stopPoseModel()
        if newKey == 3:
            if p.inMoving() and BigWorld.projection().fov != gameglobal.CAMERA_FOV_51:
                BigWorld.projection().rampFov(gameglobal.CAMERA_FOV_51, gameglobal.TIME_FOV)
            else:
                BigWorld.projection().rampFov(gameglobal.DIST_FOV, gameglobal.TIME_FOV)
        elif p.inMoving() and BigWorld.projection().fov != gameglobal.CAMERA_FOV_51:
            BigWorld.projection().rampFov(gameglobal.CAMERA_FOV_51, gameglobal.TIME_FOV)
        v4 = Math.Vector4Animation()
        v4.oneshot = True
        deltaTime = 0.2
        keyframes = []
        xOffset = self.calcXOffset()
        keyframes.append((0.0, (xOffset,
          self.cc.pivotPosition[1],
          0,
          self.cc.pivotMaxDist)))
        dist, height = self.newCalcDistAndHeight(newKey)
        self.keyDist[newKey] = dist
        halfTime = 0.4
        keyframes.append((deltaTime, (0,
          height,
          halfTime,
          dist)))
        v4.duration = deltaTime
        v4.keyframes = keyframes
        return v4

    def newCalcDistAndHeight(self, key):
        p = BigWorld.player()
        if not p:
            return 0.0
        cameraInfo = self.loadCursorCameraKey(key)
        if not cameraInfo:
            return (0, 0)
        dist = cameraInfo[0]
        height = cameraInfo[1]
        return (dist, height)

    def _calNearestPosition(self, oldD, oldH):
        if not oldD:
            return self.SCROLL_NUM - 1
        minDiff = 1000
        pos = -1
        for i, d in enumerate(self.getRealDist()):
            temp = math.fabs(d - oldD)
            if temp < minDiff and self.getRealHeight()[i] == oldH and i in self.getRealKey():
                minDiff = temp
                pos = i

        for i, item in enumerate(self.getRealKey()):
            if item == pos:
                return i

        return self.SCROLL_NUM - 1

    def setScrollSpeed(self, speed = 1, scrollNum = -2):
        global H2
        global KEY2
        global H0
        global KEY0
        global T2
        global D2
        global T0
        global MH0
        global MH2
        global D0
        global MH1
        if hasattr(self, 'KEY'):
            key = self.getRealKey()[self.currentScrollNum] if self.currentScrollNum < len(self.getRealKey()) else self.getRealKey()[-1]
            oldD = self.getRealDist()[key] if hasattr(self, 'D') else None
            oldH = self.getRealHeight()[key] if hasattr(self, 'H') else None
        else:
            oldD = oldH = None
        if speed == 0:
            self.D = D0
            if self.isInMouseMode():
                self.H = MH0
            else:
                self.H = H0
            self.T = T0
            self.KEY = KEY0
            self.HT = HT0
            self.cameraMoveSpeed = 2.0
        elif speed == 1:
            self.D = D1
            if self.isInMouseMode():
                self.H = MH1
            else:
                self.H = H1
            self.T = T1
            self.KEY = KEY1
            self.HT = HT1
            self.cameraMoveSpeed = 1.0
        else:
            self.D = D2
            if self.isInMouseMode():
                self.H = MH2
            else:
                self.H = H2
            self.T = T2
            self.KEY = KEY2
            self.HT = HT2
            self.cameraMoveSpeed = 0.5
        self._calcScrollNum()
        oldScrollNum = self.currentScrollNum
        if scrollNum != -2:
            self.currentScrollNum = scrollNum
        else:
            self.currentScrollNum = self._calNearestPosition(oldD, oldH)
        if oldScrollNum == -1 and self.currentScrollNum > 0:
            self.camBindState = self.CAMERA_QUITE_FIRST_PERSON
            p = BigWorld.player()
            if p and p.model and hasattr(p, 'getOpacityValue') and p.getOpacityValue()[0] != gameglobal.OPACITY_HIDE:
                p.model.visible = True
        key = self.getKey(self.currentScrollNum)
        dist = self.calcDist(key)
        height = self.calcHeight(key)
        xOffset = self.calcXOffset()
        self.cc.cameraDHProvider = self.createLine(dist, height, 0.5, xOffset)
        self.keyDist = [0.0,
         0.0,
         0.0,
         0.0]
        self.keyHeight = [0.0,
         0.0,
         0.0,
         0.0]

    def getCurrentScrollNum(self):
        if self.currentScrollNum == -1:
            return self.SCROLL_NUM - 1
        return self.currentScrollNum

    def loadCursorCameraKey(self, key):
        if key > 0:
            key = 3 - key
        p = BigWorld.player()
        trackName = 'gui/loginScene/detailAdjust_%d_%d.track' % (p.physique.sex, p.physique.bodyType)
        track = clientcom.loadCameraTrack(trackName)
        if track == None:
            return
        count = track.readInt('keyframes', 0)
        if key < 0 or key >= count:
            return
        item = track.openSection('key%i' % key)
        params = item.readString('CursorParam')
        if len(params):
            cameraInfo = [ float(x) for x in params.split(',') ]
            if len(cameraInfo) > 9:
                cameraInfo[9] = int(cameraInfo[9])
            if key == 1 or key == 2:
                if trackName.find('detailAdjust_') >= 0:
                    return self.setDetailAdjustCamera(track, cameraInfo)
            return cameraInfo

    def setDetailAdjustCamera(self, track, cameraInfo):
        p = BigWorld.player()
        if p == None:
            return
        modelId = charRes.transDummyBodyType(p.physique.sex, p.physique.bodyType, True)
        heightData = self.heightConfigs.get(modelId)
        if not heightData:
            return cameraInfo
        playerHeight = self.getPlayerHeight()
        if playerHeight < heightData[1]:
            low = track.readString('key4')
            low = [ float(x) for x in low.split(',') ]
            cameraInfo[1] -= (cameraInfo[1] - low[0]) / (heightData[1] - heightData[0]) * (heightData[1] - playerHeight)
            if len(cameraInfo) > 5:
                cameraInfo[5] -= (cameraInfo[5] - low[1]) / (heightData[1] - heightData[0]) * (heightData[1] - playerHeight)
        elif playerHeight > heightData[1]:
            high = track.readString('key5')
            high = [ float(x) for x in high.split(',') ]
            cameraInfo[1] += (high[0] - cameraInfo[1]) / (heightData[2] - heightData[1]) * (playerHeight - heightData[1])
            if len(cameraInfo) > 5:
                cameraInfo[5] += (high[1] - cameraInfo[5]) / (heightData[2] - heightData[1]) * (playerHeight - heightData[1])
        return cameraInfo

    def getPlayerHeight(self):
        p = BigWorld.player()
        try:
            height = max((p.model.node('biped Head').position - p.model.node('biped R Toe0').position).y, (p.model.node('biped Head').position - p.model.node('biped L Toe0').position).y) + self.headHeight if p else 0
        except:
            height = p.model.height

        return height

    def loadHeigtByTrack(self):
        if self.dataInfo:
            return
        self.dataInfo = ResMgr.openSection('gui/loginScene/height.track')
        if self.dataInfo:
            for key in self.dataInfo.keys():
                if key == 'head':
                    self.headHeight = self.dataInfo[key].asFloat
                    continue
                heightData = [ float(x) for x in self.dataInfo[key].asString.split(',') ]
                if heightData:
                    self.heightConfigs[int(key)] = heightData


ins_ = None

def instance():
    global ins_
    if ins_ == None:
        ins_ = Camera()
    return ins_
