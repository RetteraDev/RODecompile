#Embedded file name: /WORKSPACE/data/entities/client/sfx/cameraeffect.o
import math
import BigWorld
import Math
import gameglobal
import gamelog
import clientUtils
from callbackHelper import Functor
from helpers import cameraControl
startTime = 0
cameraModel = None
cameraEntityId = None

def rotateCameraFromScript(script):
    circle = script.readInt('circle', 1)
    befTime = script.readFloat('beforeTime', 0)
    aftTime = script.readFloat('afterTime', 0)
    dataArray = []
    data = script['data']
    for child in data.values():
        dataArray.append(child.asVector4)

    timeArray = []
    time = script['time']
    for child in time.values():
        timeArray.append(child.asFloat)

    cameraRotate(dataArray, timeArray, circle, befTime, aftTime)


def cameraRotate(path, time, circle, befTime, aftTime):
    global startTime
    tc = cameraControl.TC
    if tc == None:
        cameraControl.TC = BigWorld.TrackCamera()
        tc = cameraControl.TC
    tc.set(gameglobal.rds.cam.cc.matrix)
    BigWorld.camera(tc)
    tc.newTrack()
    tc.setKeytime(0, befTime)
    p = BigWorld.player()
    p.excludeCam = True
    BigWorld.player().lockKey(gameglobal.KEY_POS_EFFECT)
    mo = p.model
    if p.model.bonesBoundingBoxSize[1] == 0:
        height = mo.height
    else:
        height = mo.bonesBoundingBoxSize[1] * mo.scale[1]
    yaw = p.model.yaw
    yawPath = []
    for i in path:
        i = (i[0],
         i[1],
         i[2],
         math.pi / 2 - yaw + i[3] * 2 * math.pi)
        yawPath.append(i)

    time.append(0)
    l = len(yawPath)
    for i in xrange(l):
        data = yawPath[i]
        pos = Math.Vector3(mo.position[0] + math.cos(data[3]) * data[2], mo.position[1] + data[1] * height, mo.position[2] + math.sin(data[3]) * data[2])
        gamelog.debug('bgf:pos', pos)
        targetPos = Math.Vector3(mo.position)
        targetPos[1] += height * data[0]
        dir = targetPos - pos
        dir.normalise()
        m = Math.Matrix()
        m.lookAt(pos, dir, (0, 1, 0))
        quad = eulerAngleToQuad(m.yaw, m.pitch, m.roll)
        fov = BigWorld.projection().fov
        keyData = (pos[0],
         pos[1],
         pos[2],
         quad[0],
         quad[1],
         quad[2],
         quad[3],
         fov,
         time[i],
         True,
         0,
         0,
         0,
         0)
        tc.pushKey(*keyData)

    processLastStep(aftTime, pos, gameglobal.rds.cam.cc.position, targetPos)
    startTime = BigWorld.time()
    tc.setStopCallback(endPlay)
    tc.play(0)


mapCallback = None

def mapCameraRotate():
    global startTime
    path = [(1, 6, -5, 0),
     (1, 10, -8, 0),
     (1, 15, -1, 0),
     (1, 18, -1, 0)]
    tc = cameraControl.TC
    if tc == None:
        cameraControl.TC = BigWorld.TrackCamera()
        tc = cameraControl.TC
    tc.set(gameglobal.rds.cam.cc.matrix)
    BigWorld.camera(tc)
    tc.newTrack()
    tc.setKeytime(0, 0)
    p = BigWorld.player()
    p.ap.stopMove()
    p.ap.forceAllKeysUp()
    p.lockKey(gameglobal.KEY_POS_EFFECT)
    p.excludeCam = True
    mo = p.model
    if p.model.bonesBoundingBoxSize[1] == 0:
        height = mo.height
    else:
        height = mo.bonesBoundingBoxSize[1] * mo.scale[1]
    yaw = p.model.yaw
    yawPath = []
    for i in path:
        i = (i[0],
         i[1],
         i[2],
         math.pi / 2 - yaw + i[3] * 2 * math.pi)
        yawPath.append(i)

    ht = mo.position[1] + height
    zt = mo.position[2] - 3
    pos = Math.Vector3(mo.position[0], ht, zt)
    targetPos = Math.Vector3(mo.position)
    targetPos[1] = mo.position[1] + height
    dir = targetPos - gameglobal.rds.cam.cc.position
    dir.normalise()
    pos = gameglobal.rds.cam.cc.position - dir * 5 + (0, 18, 0)
    cdir2 = targetPos - pos
    cdir2.normalise()
    m = Math.Matrix()
    m.lookAt(pos, cdir2, (0, 1, 0))
    quad = eulerAngleToQuad(m.yaw, m.pitch, m.roll)
    fov = BigWorld.projection().fov
    keyData = (pos[0],
     pos[1],
     pos[2],
     quad[0],
     quad[1],
     quad[2],
     quad[3],
     fov,
     0.3,
     True,
     0,
     0,
     0,
     0)
    pos3 = gameglobal.rds.cam.cc.position
    cdir4 = targetPos - gameglobal.rds.cam.cc.position
    cdir4.normalise()
    m3 = Math.Matrix()
    m3.lookAt(pos3, cdir4, (0, 1, 0))
    quad3 = eulerAngleToQuad(m3.yaw, m3.pitch, m3.roll)
    keyData3 = (pos3[0],
     pos3[1],
     pos3[2],
     quad3[0],
     quad3[1],
     quad3[2],
     quad3[3],
     fov,
     0.5,
     True,
     0,
     0,
     0,
     0)
    tc.pushKey(*keyData3)
    tc.pushKey(*keyData)
    startTime = BigWorld.time()
    tc.setStopCallback(mapEndPlay)
    gameglobal.MAP_PLAYING = True
    tc.showTrack = False
    tc.play(0)


def mapEndPlay(param):
    global mapCallback
    gameglobal.MAP_PLAYING = False
    p = BigWorld.player()
    p.unlockKey(gameglobal.KEY_POS_EFFECT)
    p.updateActionKeyState()
    p.excludeCam = False
    BigWorld.camera(gameglobal.rds.cam.cc)
    mapCallback = BigWorld.callback(0.5, onMapEndPlayCallback)
    tc = cameraControl.TC
    if tc:
        tc.newTrack()
        tc.deleteKey(0)


def onMapEndPlayCallback():
    BigWorld.worldDrawEnabled(False)
    if hasattr(BigWorld, 'bigMapEnabled'):
        BigWorld.bigMapEnabled(True)


def processLastStep(time, begPos, endPos, targetPos):
    tc = cameraControl.TC
    beg = begPos - targetPos
    end = endPos - targetPos
    begYaw = beg.yaw
    deltaYaw = end.yaw - beg.yaw
    if deltaYaw > math.pi:
        deltaYaw -= math.pi * 2
    elif deltaYaw < -math.pi:
        deltaYaw += math.pi * 2
    if deltaYaw == 0:
        tc.setKeytime(tc.getKeyCount() - 1, time)
        lastKeyData = tc.getKey(0)
        listKey = list(lastKeyData)
        listKey[8] = 0
        tc.pushKey(*listKey)
    else:
        numStep = 10
        time /= numStep
        deltaYaw /= numStep
        deltaH = (endPos[1] - begPos[1]) / numStep
        deltaD = (math.sqrt(end[0] ** 2 + end[2] ** 2) - math.sqrt(beg[0] ** 2 + beg[2] ** 2)) / numStep
        tc.setKeytime(tc.getKeyCount() - 1, time)
        H = begPos[1]
        D = math.sqrt(beg[0] ** 2 + beg[2] ** 2)
        for i in xrange(1, numStep):
            begYaw += deltaYaw
            D += deltaD
            H += deltaH
            pos = Math.Vector3(targetPos[0] + D * math.sin(begYaw), H, targetPos[2] + D * math.cos(begYaw))
            dir = targetPos - pos
            dir.normalise()
            m = Math.Matrix()
            m.lookAt(pos, dir, (0, 1, 0))
            quad = eulerAngleToQuad(m.yaw, m.pitch, m.roll)
            fov = BigWorld.projection().fov
            keyData = (pos[0],
             pos[1],
             pos[2],
             quad[0],
             quad[1],
             quad[2],
             quad[3],
             fov,
             time,
             True,
             0,
             0,
             0,
             0)
            tc.pushKey(*keyData)

        lastKeyData = tc.getKey(0)
        gamelog.debug('bgf:pos5', lastKeyData[0], lastKeyData[1], lastKeyData[2])
        listKey = list(lastKeyData)
        listKey[8] = 0
        tc.pushKey(*listKey)


def endPlay(param):
    p = BigWorld.player()
    p.unlockKey(gameglobal.KEY_POS_EFFECT)
    p.updateActionKeyState()
    p.excludeCam = False
    BigWorld.camera(gameglobal.rds.cam.cc)
    tc = cameraControl.TC
    tc.newTrack()
    tc.deleteKey(0)


def eulerAngleToQuad(yaw, pitch, roll):
    yaw /= 2
    pitch /= 2
    roll /= 2
    l = [-math.cos(yaw) * math.sin(pitch) * math.cos(roll) - math.sin(yaw) * math.cos(pitch) * math.sin(roll),
     -math.sin(yaw) * math.cos(pitch) * math.cos(roll) + math.cos(yaw) * math.sin(pitch) * math.sin(roll),
     -math.cos(yaw) * math.cos(pitch) * math.sin(roll) + math.sin(yaw) * math.sin(pitch) * math.cos(roll),
     math.cos(yaw) * math.cos(pitch) * math.cos(roll) + math.sin(yaw) * math.sin(pitch) * math.sin(roll)]
    return l


def checkEnableAnimateCamera():
    if gameglobal.ENABLE_ANIMATE_CAMERA and gameglobal.SCENARIO_PLAYING != gameglobal.SCENARIO_PLAYING_TRACK_CAMERA:
        return True
    else:
        return False


def startAnimateCamera(cueData, ent = None, callback = None):
    global cameraEntityId
    global cameraModel
    dataList = cueData.split(':')
    modelId = dataList[0]
    boneName = dataList[1]
    actionName = dataList[2]
    modelPath = 'item/model/' + modelId + '/' + modelId + '.model'
    model = cameraModel
    if not model:
        model = clientUtils.model(modelPath)
        cameraModel = model
    if actionName not in model.actionNameList():
        gamelog.error('jbx:actionName not exist', actionName)
        return
    if ent == None:
        ent = BigWorld.player()
    cameraEntityId = ent.id
    if not model.inWorld:
        ent.addModel(model)
    model.yaw = ent.yaw
    model.position = ent.position
    cameraControl.newFree()
    gamelog.debug('bgf:AnimationCamera', cueData, modelId, boneName, actionName, modelPath)
    action = model.action(actionName)
    action(0, Functor(endAnimateCamera, model, ent, callback), 0)
    cameraControl.TC.invViewProvider = model.node(boneName)
    if ent == BigWorld.player():
        ent.ap.stopMove()
        ent.ap.forceAllKeysUp()
        ent.lockKey(gameglobal.KEY_POS_EFFECT)


def endAnimateCamera(model = None, ent = None, callback = None):
    global cameraModel
    if ent and cameraEntityId != ent.id:
        return
    if ent == None:
        ent = BigWorld.player()
    if ent == BigWorld.player():
        ent.unlockKey(gameglobal.KEY_POS_EFFECT)
    if callback:
        callback()
    else:
        if not model:
            model = cameraModel
        if model and model.inWorld:
            try:
                ent.delModel(model)
            except:
                pass

            cameraModel = None
            cameraControl.endCamera()


def deadCameraRotate():
    global startTime
    tc = cameraControl.TC
    if tc == None:
        cameraControl.TC = BigWorld.TrackCamera()
        tc = cameraControl.TC
    tc.set(gameglobal.rds.cam.cc.matrix)
    BigWorld.camera(tc)
    tc.newTrack()
    tc.setKeytime(0, 0)
    p = BigWorld.player()
    p.excludeCam = True
    p.lockHotKey = True
    mo = p.model
    if p.model.bonesBoundingBoxSize[1] == 0:
        height = mo.height
    else:
        height = mo.bonesBoundingBoxSize[1] * mo.scale[1]
    yaw = p.model.yaw
    yawPath = []
    for i in xrange(60):
        i = (1,
         6,
         5,
         math.pi / 2 - yaw + -math.pi / 180 * 0.5 * i * 2 * math.pi)
        yawPath.append(i)

    for i in xrange(60):
        data = yawPath[i]
        pos = Math.Vector3(mo.position[0] + math.cos(data[3]) * data[2], mo.position[1] + data[1] * height, mo.position[2] + math.sin(data[3]) * data[2])
        gamelog.debug('bgf:pos', pos)
        targetPos = Math.Vector3(mo.position)
        targetPos[1] += height * data[0]
        dir = targetPos - pos
        dir.normalise()
        m = Math.Matrix()
        m.lookAt(pos, dir, (0, 1, 0))
        quad = eulerAngleToQuad(m.yaw, m.pitch, m.roll)
        fov = BigWorld.projection().fov
        keyData = (pos[0],
         pos[1],
         pos[2],
         quad[0],
         quad[1],
         quad[2],
         quad[3],
         fov,
         1,
         True,
         0,
         0,
         0,
         0)
        tc.pushKey(*keyData)

    startTime = BigWorld.time()
    tc.setStopCallback(endPlay)
    tc.play(0)
