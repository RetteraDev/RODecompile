#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/faceEmote.o
import BigWorld
import Math
import gameglobal
from callbackHelper import Functor
MIN_YAW = -180
MAX_YAW = 180
MIN_PITCH = -50.0
MAX_PITCH = 50.0
ANGLE_VELOCITY = 1000

class HeadCtrl(object):

    def __init__(self):
        super(HeadCtrl, self).__init__()
        self.model = None
        self.dirProvider = None
        self.enable = True
        self.nodeInfo = None
        self.callbackHandle = None
        self.isResuming = False

    def releaseHeadCtrl(self):
        if self.callbackHandle:
            BigWorld.cancelCallback(self.callbackHandle)
            self.callbackHandle = None
        if self.model and hasattr(self.model, 'tracker') and self.model.tracker:
            self.model.tracker.nodeInfo = None
        self.model = None
        self.dirProvider = None
        self.enable = True
        self.nodeInfo = None
        self.isResuming = False

    def stopHeadCtrl(self):
        model = self.model
        if model and hasattr(model, 'tracker') and model.tracker:
            self.enable = False
            self.setResuming(False)
            self.model.tracker.enable = self.enable

    def checkModel(self):
        return self.enable and self.model and hasattr(self.model, 'tracker') and self.model.tracker

    def resetHeadCtrl(self):
        if self.model:
            self.setResuming(True)
            self.enable = False
            self.idle(self.model)
            BigWorld.callback(gameglobal.RESUME_HEADCTRL_TIME, self.stopHeadCtrl)

    def idle(self, model):
        self.model.tracker.directionYPProvider = self.dirProvider
        self.model.tracker.nodeInfo = self.nodeInfo

    def setResuming(self, isResuming):
        self.isResuming = isResuming

    def getLookAtYawPitch(self):
        tPos = BigWorld.camera().position - self.model.node('biped Head').position
        deltaYaw = self.model.yaw - tPos.yaw
        if deltaYaw > 3.14:
            deltaYaw -= 6.28
        elif deltaYaw < -3.14:
            deltaYaw += 6.28
        return (-deltaYaw, BigWorld.camera().direction.pitch)

    def headLookAtCamera(self):
        if self.model:
            self.enable = True
            self.checkHeadLookAtState()

    def checkHeadLookAtState(self):
        if not self.checkModel():
            if self.callbackHandle:
                BigWorld.cancelCallback(self.callbackHandle)
                self.callbackHandle = None
            return
        yaw, pitch = self.getLookAtYawPitch()
        if yaw > gameglobal.HEAD_MAX_YAW:
            yaw = gameglobal.HEAD_MAX_YAW
        elif yaw < gameglobal.HEAD_MIN_YAW:
            yaw = gameglobal.HEAD_MIN_YAW
        if pitch > gameglobal.HEAD_MAX_PITCH:
            pitch = gameglobal.HEAD_MAX_PITCH
        elif pitch < gameglobal.HEAD_MIN_PITCH:
            pitch = gameglobal.HEAD_MIN_PITCH
        self.model.tracker.directionYPProvider = (yaw,
         pitch,
         gameglobal.LOOKAT_CAMERA_TIME,
         0.0)
        self.model.tracker.enable = True
        if self.callbackHandle:
            BigWorld.cancelCallback(self.callbackHandle)
        self.callbackHandle = BigWorld.callback(0.2, self.checkHeadLookAtState)

    def setTargetModel(self, model):
        if self.model:
            self.model.tracker = None
            self.dirProvider = None
        if not model:
            self.model = None
            return
        try:
            nodeInfo = BigWorld.TrackerNodeInfo(model, 'biped Head', [], 'None', MIN_PITCH, MAX_PITCH, MIN_YAW, MAX_YAW, ANGLE_VELOCITY)
        except:
            return

        tracker = BigWorld.Tracker()
        tracker.maxLod = 80
        model.tracker = tracker
        self.dirProvider = (0.0,
         0.0,
         gameglobal.RESUME_HEADCTRL_TIME,
         0.0)
        self.model = model
        self.nodeInfo = nodeInfo
        self.model.tracker.directionYPProvider = self.dirProvider
        self.model.tracker.nodeInfo = self.nodeInfo
        self.model.tracker.enable = False


class EyeBallCtrl(object):

    def __init__(self):
        super(EyeBallCtrl, self).__init__()
        self.model = None
        self.dirProviderL = None
        self.dirProviderR = None
        self.nodeInfoL = None
        self.nodeInfoR = None
        self.enable = True
        self.callbackHandle = None
        self.isResuming = False

    def releaseEyeCtrl(self):
        if self.callbackHandle:
            BigWorld.cancelCallback(self.callbackHandle)
            self.callbackHandle = None
        if self.model and hasattr(self.model, 'trackerL') and self.model.trackerL:
            self.model.trackerL.directionProvider = None
            self.model.trackerR.directionProvider = None
            self.model.trackerL.nodeInfo = None
            self.model.trackerR.nodeInfo = None
        self.model = None
        self.dirProviderL = None
        self.dirProviderR = None
        self.nodeInfoL = None
        self.nodeInfoR = None
        self.enable = False
        self.isResuming = False

    def stopEyeCtrl(self):
        self.model.trackerL.enable = False
        self.model.trackerR.enable = False
        self.enable = False
        self.setResuming(False)

    def resetEyeCtrl(self):
        if self.model:
            if self.isResuming:
                return
            self.setResuming(True)
            self.enable = True
            self.model.trackerL.enable = True
            self.model.trackerR.enable = True
            BigWorld.callback(gameglobal.RESUME_EYECTRL_TIME, self.stopEyeCtrl)
            self.idle(self.model)

    def getLookAtYawPitch(self, NodeName):
        camPos = BigWorld.camera().position
        if NodeName == 'head_eveball_L':
            targetPos = Math.Vector3(camPos[0] + gameglobal.OFFSET_LEFT_POSITION[0], camPos[1] + gameglobal.OFFSET_LEFT_POSITION[1], camPos[2] + gameglobal.OFFSET_LEFT_POSITION[2])
        elif NodeName == 'head_eveball_R':
            targetPos = Math.Vector3(camPos[0] + gameglobal.OFFSET_RIGHT_POSITION[0], camPos[1] + gameglobal.OFFSET_RIGHT_POSITION[1], camPos[2] + gameglobal.OFFSET_RIGHT_POSITION[2])
        else:
            targetPos = camPos
        tPos = self.model.node(NodeName).position - targetPos
        deltaYaw = self.model.yaw - tPos.yaw
        if deltaYaw > 3.14:
            deltaYaw -= 6.28
        elif deltaYaw < -3.14:
            deltaYaw += 6.28
        return (deltaYaw, tPos.pitch)

    def eyeLookAtCamera(self):
        if self.model:
            self.enable = True
            self.model.trackerL.nodeInfo = self.nodeInfoL
            self.model.trackerR.nodeInfo = self.nodeInfoR
            self.checkEyeLookAtState()

    def checkEyeLookAtState(self):
        if not self.checkModel():
            if self.callbackHandle:
                BigWorld.cancelCallback(self.callbackHandle)
                self.callbackHandle = None
            return
        yaw, pitch = self.getLookAtYawPitch('head_eveball_L')
        if yaw > gameglobal.EYE_MAX_YAW:
            yaw = gameglobal.EYE_MAX_YAW
        elif yaw < gameglobal.EYE_MIN_YAW:
            yaw = gameglobal.EYE_MIN_YAW
        if pitch > gameglobal.EYE_MAX_PITCH:
            pitch = gameglobal.EYE_MAX_PITCH
        elif pitch < gameglobal.EYE_MIN_PITCH:
            pitch = gameglobal.EYE_MIN_PITCH
        self.model.trackerL.directionYPProvider = (yaw,
         pitch,
         gameglobal.LOOKAT_CAMERA_EYE_TIME,
         0.0)
        yaw, pitch = self.getLookAtYawPitch('head_eveball_R')
        if yaw > gameglobal.EYE_MAX_YAW:
            yaw = gameglobal.EYE_MAX_YAW
        elif yaw < gameglobal.EYE_MIN_YAW:
            yaw = gameglobal.EYE_MIN_YAW
        if pitch > gameglobal.EYE_MAX_PITCH:
            pitch = gameglobal.EYE_MAX_PITCH
        elif pitch < gameglobal.EYE_MIN_PITCH:
            pitch = gameglobal.EYE_MIN_PITCH
        self.model.trackerR.directionYPProvider = (yaw,
         pitch,
         gameglobal.LOOKAT_CAMERA_EYE_TIME,
         0.0)
        if self.callbackHandle:
            BigWorld.cancelCallback(self.callbackHandle)
        self.callbackHandle = BigWorld.callback(0.2, self.checkEyeLookAtState)

    def setResuming(self, isResuming):
        self.isResuming = isResuming

    def setTargetModel(self, model):
        if self.model:
            self.model.trackerL = None
            self.model.trackerR = None
            self.dirProviderR = None
            self.dirProviderL = None
        if not model:
            self.model = None
            return
        try:
            hinfoL = BigWorld.TrackerNodeInfo(model, 'head_eveball_L', [], 'head_eveball_L', MIN_PITCH, MAX_PITCH, MIN_YAW, MAX_YAW, ANGLE_VELOCITY)
            hinfoR = BigWorld.TrackerNodeInfo(model, 'head_eveball_R', [], 'head_eveball_R', MIN_PITCH, MAX_PITCH, MIN_YAW, MAX_YAW, ANGLE_VELOCITY)
        except:
            return

        trackerL = BigWorld.Tracker()
        trackerL.maxLod = 80
        model.trackerL = trackerL
        trackerR = BigWorld.Tracker()
        trackerR.maxLod = 80
        model.trackerR = trackerR
        self.dirProviderL = (0.0,
         0.0,
         gameglobal.RESUME_EYECTRL_TIME,
         0.0)
        self.dirProviderR = (0.0,
         0.0,
         gameglobal.RESUME_EYECTRL_TIME,
         0.0)
        self.model = model
        self.nodeInfoL = hinfoL
        self.nodeInfoR = hinfoR

    def idle(self, model):
        if not self.checkModel() or model != self.model:
            return
        self.model.trackerR.directionYPProvider = self.dirProviderR
        self.model.trackerR.nodeInfo = self.nodeInfoR
        self.model.trackerL.directionYPProvider = self.dirProviderL
        self.model.trackerL.nodeInfo = self.nodeInfoL

    def checkModel(self):
        return self.enable and self.model and hasattr(self.model, 'trackerR') and self.model.trackerR and hasattr(self.model, 'trackerL') and self.model.trackerL


class MouthCtrl(object):

    def __init__(self):
        super(MouthCtrl, self).__init__()
        self.model = None
        self.dirProvider = None
        self.nodeInfo = None
        self.enable = True

    def stopEmote(self):
        model = self.model
        if model and hasattr(model, 'trackerM') and model.trackerM:
            model.trackerM.directionProvider = None
            model.trackerM.nodeInfo = None
            self.enable = False

    def resumeEmote(self):
        if self.model:
            self.enable = True
            BigWorld.callback(0.5, Functor(self.idle, self.model))

    def setTargetModel(self, model):
        if self.model:
            self.model.trackerM = None
        if not model:
            self.model = None
            return
        try:
            infm = BigWorld.TrackerNodeInfo(model, 'head_chin', [], 'head_chin', -15.0, 15.0, -30, 30.0, 999999.0)
        except:
            return

        drpm = BigWorld.ScriptDirProvider()
        trackerM = BigWorld.Tracker()
        trackerM.maxLod = 8
        model.trackerM = trackerM
        a = -2
        b = 2
        p = (0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         a,
         a,
         a,
         a,
         a,
         a,
         a,
         a,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         a,
         a,
         a,
         a,
         a,
         a,
         a,
         a,
         a,
         a,
         a,
         0,
         0,
         a,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         a,
         a,
         a,
         a,
         a,
         a,
         a,
         a,
         a,
         a,
         a,
         a,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         a,
         a,
         a,
         a,
         a,
         a,
         a,
         a,
         a,
         a,
         a,
         a,
         a,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         0,
         0,
         0,
         0,
         0)
        a = -2
        y = (0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         a,
         a,
         a,
         a,
         a,
         a,
         a,
         a,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         a,
         a,
         a,
         a,
         a,
         a,
         a,
         a,
         a,
         a,
         a,
         0,
         0,
         a,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         a,
         a,
         a,
         a,
         a,
         a,
         a,
         a,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         b,
         0,
         0,
         0,
         0,
         0)
        drpm.setPitchScript(p, 0.3, 2)
        drpm.setYawScript(y, 0.3, 2)
        self.dirProvider = drpm
        self.model = model
        self.nodeInfo = infm
        self.idle(self.model)

    def idle(self, model):
        if not self.checkModel() or model != self.model:
            return
        self.model.trackerM.directionProvider = self.dirProvider
        self.model.trackerM.nodeInfo = self.nodeInfo
        self.model.trackerM.relativeProvider = True

    def twistLeft(self, keepTime = 0.4):
        if not self.checkModel():
            return
        drp = BigWorld.ScriptDirProvider()
        self.model.trackerM.directionProvider = drp
        self.model.trackerM.nodeInfo = self.nodeInfo
        self.model.trackerM.relativeProvider = True
        drp.setPitchScript((3, 3), 0.05, 1)
        drp.setYawScript((-4, -4), 0.05, 1)
        BigWorld.callback(keepTime, Functor(self.idle, self.model))

    def twistRight(self, keepTime = 0.4):
        if not self.checkModel():
            return
        drp = BigWorld.ScriptDirProvider()
        self.model.trackerM.directionProvider = drp
        self.model.trackerM.nodeInfo = self.nodeInfo
        self.model.trackerM.relativeProvider = True
        drp.setPitchScript((3, 3), 0.05, 1)
        drp.setYawScript((4, 4), 0.05, 1)
        BigWorld.callback(keepTime, Functor(self.idle, self.model))

    def talk(self, keepTime = 2):
        if not self.checkModel():
            return
        p = (0, -1, -5, -2, 2, -1, -8, -2, -6, -3, 1, 0, -2, 2, -2, -6, -2, 1, -1, -3, -9, 0, -1, 3, 0, -3, -1, -6, -2, 0)
        y = (0, 0)
        drp = BigWorld.ScriptDirProvider()
        self.model.trackerM.directionProvider = drp
        self.model.trackerM.nodeInfo = self.nodeInfo
        self.model.trackerM.relativeProvider = True
        drp.setPitchScript(p, 0.12, 2)
        drp.setYawScript(y, 0.15, 2)
        BigWorld.callback(keepTime, Functor(self.idle, self.model))

    def checkModel(self):
        return self.enable and self.model and hasattr(self.model, 'trackerM') and self.model.trackerM
