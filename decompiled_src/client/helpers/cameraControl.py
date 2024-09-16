#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/cameraControl.o
import BigWorld
import Math
from Math import Vector3
import gameglobal
import gamelog
CAM_INDEX = 0
TC = None
CC = None

def newFree():
    global CC
    global TC
    if TC is None:
        TC = BigWorld.FreeCamera()
        CC = BigWorld.camera()
        BigWorld.camera(TC)
    elif isinstance(TC, BigWorld.TrackCamera):
        TC.stop()
        TC = BigWorld.FreeCamera()
        BigWorld.camera(TC)
    else:
        TC = BigWorld.FreeCamera()
        BigWorld.camera(TC)


def newTrack():
    global CC
    global CAM_INDEX
    global TC
    CAM_INDEX = 0
    if TC is None:
        TC = BigWorld.TrackCamera()
        CC = BigWorld.camera()
        BigWorld.camera(TC)
        TC.set(CC.matrix)
        TC.newTrack()
    elif isinstance(TC, BigWorld.TrackCamera):
        TC.stop()
        TC.newTrack()
    else:
        TC = BigWorld.TrackCamera()
        BigWorld.camera(TC)
        TC.newTrack()
    TC.showTrack = False


def endCamera():
    global CC
    global TC
    gamelog.debug('@szh: endCamera', TC, CC)
    if TC is None:
        gamelog.error('not in track camera')
        return
    BigWorld.camera(CC)
    TC = None
    CC = None


def record():
    global CAM_INDEX
    if TC is None:
        gamelog.error('not in track camera')
        return
    TC.insertAfter(CAM_INDEX)
    CAM_INDEX += 1
    gamelog.debug('total keys in this track:', TC.getKeyCount(), CAM_INDEX)


def _endCallback(arg):
    gamelog.debug('playback ends', arg)


def play(start = 0, endCallback = None, frameCallback = None):
    if TC is None:
        gamelog.error('not in track camera')
        return
    if endCallback is not None:
        TC.setStopCallback(endCallback)
    if frameCallback is not None:
        TC.setFrameCallback(frameCallback)
    TC.showTrack = False
    TC.play(start)


def pushKey(args, duration = 0):
    global CAM_INDEX
    if TC is None:
        gamelog.error('not in track camera')
        return
    TC.pushKey(*args)
    if duration > 0:
        TC.setKeytime(CAM_INDEX, duration)
    CAM_INDEX += 1


def shake(duration, depthVec):
    if TC is None:
        gamelog.error('not in track camera')
        return
    TC.shake(duration, Vector3(*depthVec))


def moveCamera(args):
    pushKey(args)
    TC.play(1)


def initCC(needSetMatrix = True, boundRemain = 5.0):
    global CC
    global TC
    if TC is None:
        CC = BigWorld.camera()
        TC = BigWorld.CursorCamera()
    elif not isinstance(TC, BigWorld.CursorCamera):
        TC = BigWorld.CursorCamera()
    if needSetMatrix:
        TC.set(CC.matrix)
        BigWorld.camera(TC)
        TC.source = BigWorld.dcursor().matrix
    TC.movementHalfLife = 0.1
    TC.turningHalfLife = 0.1
    TC.maxDistHalfLife = 0.14
    TC.boundRemain = boundRemain
    TC.maxVelocity = 100
    TC.followMovementHalfLife = 0.0


def restoreCC():
    global CC
    global TC
    TC = None
    if CC:
        BigWorld.camera(CC)
        CC = None
    else:
        BigWorld.camera(gameglobal.rds.cam.cc)


def playCC(delta, cameraInfo, targetMatrix = None, halfTime = 0.4):
    if not TC:
        return
    v4 = Math.Vector4Animation()
    v4.oneshot = True
    keyframes = []
    dist = cameraInfo[0]
    height = cameraInfo[1]
    xDist = cameraInfo[2]
    keyframes.append((delta, (xDist,
      height,
      halfTime,
      dist)))
    v4.duration = delta
    v4.keyframes = keyframes
    TC.target = targetMatrix
    TC.cameraDHProvider = v4


def playCCLine(lines, targetMatrix = None):
    v4 = Math.Vector4Animation()
    v4.oneshot = True
    v4.duration = lines[-1][0]
    v4.keyframes = lines
    TC.target = targetMatrix
    TC.cameraDHProvider = v4
