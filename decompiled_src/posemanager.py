#Embedded file name: /WORKSPACE/data/entities/client/helpers/posemanager.o
import math
import Math
import BigWorld
import gametypes
import gamelog
import gameglobal
import const
import appSetting
import keys
from helpers import action
from data import foot_dust_data as FDD
from data import equip_data as ED
UNKNOW_TYPE = 0
LOOKAT_TYPE = 1
RIDE_TYPE = 2
LOOKTARGET_TYPE = 3

class PoseManager(object):

    def __init__(self, ownerId):
        self.ownerId = ownerId
        self.enable = False
        self.needLookAt = False
        self.source = None
        self.target = None
        self.enableLookAt = False
        self.deltaAngle = 0.0
        self.model = None
        self.lookAtModeEnable = appSetting.Obj.get(keys.SET_LOOK_AT, 1)
        self.poseTye = UNKNOW_TYPE
        self.posePath = ''

    def getPosePath(self, owner):
        matchType = 0 if gameglobal.rds.GameState <= gametypes.GS_LOGIN and gameglobal.rds.loginScene.inAvatarStage() else owner.fashion.getWeaponMatchType()
        posePath = 'char/' + str(owner.fashion.modelID) + '/config/pose/' + str(matchType + 1) + '.xml'
        if owner.bianshen[0] != gametypes.BIANSHEN_HUMAN:
            lookPoserPath = self.getLookPoserPath(owner.fashion.modelID)
            if lookPoserPath:
                posePath = 'char/' + str(owner.fashion.modelID) + '/config/pose/' + str(lookPoserPath) + '.xml'
        return posePath

    def getLookPoserPath(self, modelID):
        return FDD.data.get(modelID, {}).get('lookPoserPath', '')

    def setPoseModel(self, targetMatrix = None):
        owner = BigWorld.entities.get(self.ownerId)
        if not owner or not owner.inWorld:
            return
        self.stopPoseModel()
        model = owner.model
        if owner.bianshen[0] != gametypes.BIANSHEN_HUMAN and self.getLookPoserPath(owner.fashion.modelID):
            model = owner.modelServer.bodyModel
        posePath = self.getPosePath(owner)
        if getattr(model, 'posePath', None) == posePath:
            return
        if hasattr(model, 'poser'):
            self.model.poser = None
        poser = BigWorld.MatcherAnimationPoser(model, posePath)
        self.model = model
        self.model.poser = poser
        self.model.poser.enableLookAt = False
        self.model.poser.deltaAngle = 0.0
        self.model.poser.ridePoseDeltaAngle = 0.3
        self.model.poser.turnHalfTime = 0.5
        self.model.poser.source = None
        self.model.poser.target = None
        self.model.poser.enable = False
        self.model.poser.enableRidePose = False
        self.model.posePath = posePath
        if hasattr(self.model.poser, 'targetMatrix'):
            self.model.poser.targetMatrix = targetMatrix
        self.posePath = posePath
        if self.lookAtModeEnable:
            self.startGaze(targetMatrix)
        if owner.bianshen[0] != gametypes.BIANSHEN_HUMAN:
            if owner.bianshen[0] == gametypes.BIANSHEN_RIDING_RB and ED.data.get(owner.bianshen[1], {}).get('disableRidePose', False):
                pass
            else:
                self.startRidePose()

    def startNearPlanePosFollow(self):
        self.targetMatrix = Math.Matrix()
        self.model.poser.targetMatrix = self.targetMatrix
        BigWorld.callback(0, self.flollowCallbackFun)

    def flollowCallbackFun(self):
        if not getattr(self.model, 'poser', None) or not getattr(self.model.poser, 'targetMatrix', None):
            return
        if hasattr(BigWorld, 'getCursorNearplaneWorldPos'):
            pos = BigWorld.getCursorNearplaneWorldPos(-100)
        else:
            pos = Math.Vector3(0, 0, 0)
        self.targetMatrix.setTranslate(pos)
        BigWorld.callback(0, self.flollowCallbackFun)

    def startFacePosFollow(self):
        if self.model and getattr(self.model, 'poser', None):
            self.targetMatrix = Math.Matrix()
            self.model.poser.targetMatrix = self.targetMatrix
            BigWorld.callback(0, self.flollowFacePosCallbackFun)

    def flollowFacePosCallbackFun(self):
        if not getattr(self.model, 'poser', None) or not getattr(self.model.poser, 'targetMatrix', None) or not gameglobal.rds.ui.cameraV2.isShow or not gameglobal.rds.ui.cameraV2.faceOrientation:
            return
        if hasattr(BigWorld, 'getCursorNearplaneWorldPos'):
            pos = BigWorld.getCursorNearplaneWorldPos(-100)
        else:
            pos = Math.Vector3(0, 0, 0)
        self.targetMatrix.setTranslate(pos)
        BigWorld.callback(0, self.flollowFacePosCallbackFun)

    def startEyesPosFollow(self):
        self.startGaze()
        if self.model and getattr(self.model, 'gaze', None):
            self.targetMatrix = Math.Matrix()
            self.model.gaze.targetMatrix = self.targetMatrix
            BigWorld.callback(0, self.flollowEyesPosCallbackFun)

    def flollowEyesPosCallbackFun(self):
        if not getattr(self.model, 'gaze', None) or not getattr(self.model.gaze, 'targetMatrix', None) or not gameglobal.rds.ui.cameraV2.isShow or not gameglobal.rds.ui.cameraV2.eyeOrientation:
            return
        if hasattr(BigWorld, 'getCursorNearplaneWorldPos'):
            pos = BigWorld.getCursorNearplaneWorldPos(-100)
        else:
            pos = Math.Vector3(0, 0, 0)
        self.targetMatrix.setTranslate(pos)
        BigWorld.callback(0, self.flollowEyesPosCallbackFun)

    def startRidePose(self):
        owner = BigWorld.entities.get(self.ownerId)
        if not owner or not owner.inWorld:
            return
        if not self.model:
            return
        if not hasattr(self.model, 'poser'):
            return
        self.model.poser.enable = True
        self.model.poser.enableLookAt = False
        self.model.poser.source = None
        self.model.poser.enableRidePose = True
        self.model.poser.turnHalfTime = 0.5
        self.model.poser.ridePoseDeltaAngle = 0.3
        self.model.poser.target = None

    def enableRideIdlePose(self, enable):
        owner = BigWorld.entities.get(self.ownerId)
        if not hasattr(self.model, 'poser'):
            return
        if self.getLookPoserPath(owner.fashion.modelID) and hasattr(self.model.poser, 'enableRideIdlePose'):
            self.model.poser.enableRidePose = not enable
            self.model.poser.enableRideIdlePose = enable

    def startGaze(self, targetMatrix = None):
        if not gameglobal.rds.configData.get('enableNewCamera', False) or not gameglobal.rds.ui.cameraV2.isShow:
            return
        if not self.model:
            return
        owner = BigWorld.entities.get(self.ownerId)
        if owner.bianshen[0] != gametypes.BIANSHEN_HUMAN:
            return
        if not getattr(self.model, 'gaze', None):
            gaze = BigWorld.GazeControl()
            data = FDD.data.get(owner.fashion.modelID, {})
            gaze.yawLimit = data.get('eyeYawLimit', 0.04)
            self.model.gaze = gaze
            if targetMatrix and hasattr(self.model.gaze, 'targetMatrix'):
                self.model.gaze.targetMatrix = targetMatrix

    def stopGaze(self):
        owner = BigWorld.entities.get(self.ownerId)
        if owner.bianshen[0] != gametypes.BIANSHEN_HUMAN:
            return
        if getattr(self.model, 'gaze', None):
            self.model.gaze = None

    def startLookAtPose(self):
        owner = BigWorld.entities.get(self.ownerId)
        if not owner or not owner.inWorld:
            return
        if not self.model:
            return
        if not hasattr(self.model, 'poser'):
            return
        if owner.inMoving():
            return
        if owner.fashion.doingActionType() == action.BORED_ACTION:
            return
        if owner.weaponInHandState() != gametypes.WEAPON_HANDFREE:
            return
        if owner.bianshen[0] != gametypes.BIANSHEN_HUMAN:
            return
        if self.lookAtModeEnable == 0:
            return
        if gameglobal.rds.GameState > gametypes.GS_LOGIN:
            if not owner.stateMachine.checkStatus(const.CT_LOOK_AT) and not gameglobal.rds.ui.cameraV2.isShow:
                return
        self.model.poser.enable = True
        self.model.poser.enableLookAt = True
        self.model.poser.source = BigWorld.camera().matrix
        self.model.poser.minYaw = -2.0
        self.model.poser.enableRidePose = False
        self.model.poser.turnHalfTime = 0.15
        self.model.poser.maxYaw = math.pi
        self.model.poser.target = self.model.node('Scene Root')
        self.model.poser.offset = (0, owner.getModelHeight(), 0)

    def startIdelPose(self):
        owner = BigWorld.entities.get(self.ownerId)
        if not owner or not owner.inWorld:
            return
        if not self.model:
            return
        if not hasattr(self.model, 'poser'):
            return
        if owner.inCombat:
            return
        if owner.bianshen[0] != gametypes.BIANSHEN_HUMAN:
            return
        self.model.poser.enable = True
        self.model.poser.enableLookAt = False
        self.model.poser.deltaAngle = 0.785
        self.model.poser.turnHalfTime = 0.15
        self.model.poser.source = None
        self.model.poser.target = None

    def startTargetPose(self):
        owner = BigWorld.entities.get(self.ownerId)
        if not owner or not owner.inWorld:
            return
        if not self.model:
            return
        if not hasattr(self.model, 'poser'):
            return
        if not owner.targetLocked:
            return
        if owner.inCombat:
            return
        self.model.poser.enable = True
        self.model.poser.enableLookAt = False
        self.model.poser.source = None
        self.model.poser.target = owner.targetLocked
        self.model.poser.deltaAngle = 0.785

    def setLookAtEnable(self, enable):
        if not enable:
            if not self.model:
                return
            if self.model.poser:
                self.model.poser.enableLookAt = False
                self.model.poser.enable = False
                self.model.poser.target = None
                self.model.poser.source = None
        if self.lookAtModeEnable == False and enable:
            self.lookAtModeEnable = enable
            cam = gameglobal.rds.cam
            newKey = cam.getKey(cam.currentScrollNum)
            if newKey <= 3:
                p = BigWorld.player()
                p.modelServer.poseManager.startLookAtPose()
        else:
            self.lookAtModeEnable = enable

    def stopPoseModel(self):
        owner = BigWorld.entities.get(self.ownerId)
        if not owner or not owner.inWorld:
            return
        if not self.model:
            return
        if not hasattr(self.model, 'poser'):
            return
        if owner.bianshen[0] != gametypes.BIANSHEN_HUMAN:
            return
        self.model.poser.deltaAngle = 0.0
        self.model.poser.turnHalfTime = 0.5
        self.model.poser.enableLookAt = False
        self.model.poser.enable = False
        self.model.poser.target = None
        self.model.poser.source = None
        if hasattr(self.model.poser, 'targetMatrix'):
            self.model.poser.targetMatrix = None

    def release(self):
        owner = BigWorld.entities.get(self.ownerId)
        if not owner or not owner.inWorld:
            return
        if not self.model:
            return
        if not hasattr(self.model, 'poser'):
            return
        self.posePath = None
        self.model.poser = None
        self.model.gaze = None
        self.model = None
