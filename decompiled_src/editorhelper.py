#Embedded file name: /WORKSPACE/data/entities/client/helpers/editorhelper.o
import copy
import math
import BigWorld
import Math
import C_ui
try:
    import MCModelRegistery as CubeModel
except:
    CubeModel = None

import formula
import gameglobal
import keys
import utils
import const
import clientcom
import gamelog
import clientUtils
from guis import hotkey as HK
from guis import cursor
from gameclass import Singleton
from sfx import flyEffect
from helpers import outlineHelper
from helpers import strmap
from helpers import seqTask
from appearance import Appearance
from physique import Physique
from callbackHelper import Functor
from data import item_furniture_data as IFD
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SCD
from data import map_config_data as MCD
ed = None
pg = None
rg = None
sg = None
m = None
edInited = False
mInited = False

def handleMouseMove(mp):
    global m
    global rg
    global sg
    global pg
    clipCursorPos = BigWorld.getCursorPosInClip()
    p = BigWorld.player()
    result = BigWorld.getScreenPosInWorld(p.spaceID, clipCursorPos.x, clipCursorPos.y, 1000, 1, ())
    ca = BigWorld.camera()
    x1, y1, z1 = ca.position
    x2, y2, z2 = result[0]
    y3 = p.position[1]
    if y1 != y2:
        x3 = (x2 - x1) * (y3 - y1) / (y2 - y1) + x1
        z3 = (z2 - z1) * (y3 - y1) / (y2 - y1) + z1
    else:
        x3 = x2
        z3 = z2
        y3 = y3
    result = list(result)
    result[0] = Math.Vector3(x3, y3, z3)
    pos = flyEffect._findDropPoint(result[0])
    m.position = pos
    pg.setMatrix(m.matrix)
    rg.setMatrix(m.matrix)
    sg.setMatrix(m.matrix)


def handleMouseRotate(mp):
    oldscale = m.scale
    m.rotateYPR((mp.yaw, mp.pitch, mp.roll))
    m.scale = oldscale
    sg.setMatrix(m.matrix)


def handleMouseScale(mp):
    m.scale = mp.scale
    sg.setMatrix(m.matrix)


def initEditor():
    global edInited
    global rg
    global pg
    global ed
    global sg
    if edInited:
        return
    ed = BigWorld.BWEditor()
    pg = BigWorld.PositionGizmo()
    rg = BigWorld.RotationGizmo()
    sg = BigWorld.ScaleGizmo()
    ed.addGizmo(pg)
    ed.addGizmo(rg)
    ed.addGizmo(sg)
    edInited = True


def initModel():
    global m
    global mInited
    if mInited:
        return
    m = clientUtils.model('scene/common/homes/n/wj/nwj_02_02001.model')
    p = BigWorld.player()
    p.addModel(m)
    m.position = p.position
    mInited = True


def setCallback():
    pg.mouseCallback = handleMouseMove
    rg.mouseCallback = handleMouseRotate
    sg.mouseCallback = handleMouseScale
    rg.setMatrix(m.matrix)
    pg.setMatrix(m.matrix)
    sg.setMatrix(m.matrix)


def test():
    initEditor()
    initModel()
    setCallback()
    BigWorld.enableEditorMode(1)


def testSetMatrix():
    mp = Math.Matrix(m.matrix)
    mp.setTranslate((5, 5, 5))
    rg.setMatrix(mp)


class OperateObj(object):

    def __init__(self):
        super(OperateObj, self).__init__()
        self.model = clientUtils.model('scene/common/homes/n/wj/nwj_02_01002.model')
        self.model.visible = False
        p = BigWorld.player()
        p.addModel(self.model)
        self.model.position = p.position

    def show(self):
        self.model.visible = True

    def matrix(self):
        return self.model.matrix

    def onMouseMove(self, matrix):
        self.model.position = matrix.position

    def onMouseRotate(self, matrix):
        self.model.yaw = matrix.yaw
        self.model.pitch = matrix.pitch
        self.model.roll = matrix.roll


class Editor(object):

    def __init__(self):
        super(Editor, self).__init__()
        self.ed = BigWorld.BWEditor()
        self.pg = BigWorld.PositionGizmo()
        self.rg = BigWorld.RotationGizmo()

    def initMove(self):
        self.ed.addGizmo(self.pg)

    def initRotate(self):
        self.ed.addGizmo(self.rg)

    def initScale(self):
        self.ed.addGizmo(self.sg)

    def show(self):
        BigWorld.enableEditorMode(1)

    def hide(self):
        BigWorld.enableEditorMode(0)

    def clear(self):
        self.ed.removeAllGizmo()

    def destroy(self):
        self.ed.removeAllGizmo()
        self.pg = None
        self.rg = None
        self.ed = None
        self.sg = None
        BigWorld.enableEditorMode(0)

    def attachToMoveObj(self, obj, onMoveCallback = 'onMouseMove'):
        self.pg.setMatrix(obj.matrix())
        self.pg.mouseCallback = getattr(obj, onMoveCallback, None)

    def attachToRotateObj(self, obj, onRotateCallback = 'onMouseRotate'):
        self.rg.setMatrix(obj.matrix())
        self.rg.mouseCallback = getattr(obj, onRotateCallback, None)


OpObj = None
Edr = None

def testMove():
    global Edr
    global OpObj
    OpObj = OpObj or OperateObj()
    OpObj.show()
    Edr = Edr or Editor()
    Edr.clear()
    Edr.initMove()
    Edr.show()
    Edr.attachToMoveObj(OpObj)


def testRotate():
    global Edr
    global OpObj
    OpObj = OpObj or OperateObj()
    OpObj.show()
    Edr = Edr or Editor()
    Edr.clear()
    Edr.initRotate()
    Edr.show()
    Edr.attachToRotateObj(OpObj)


def testYawRotate():
    initEditor()
    initModel()
    setCallback()
    ed.removeAllGizmo()
    ed.addGizmo(rg)
    rg.enableYaw = 1
    rg.enablePitch = 0
    rg.enableRoll = 0
    ed.enable = 1


YAW_ROTATE_VALUE = -math.pi / 180 * 2
FLOOR_HEIGHT_MAX = 7.39
FLOOR_HEIGHT_MID = 2.0
FLOOR_HEIGHT_MIN = 0.11
MOVE_DISTANCE = 0.1
PITCH_MIN = -1.57
PITCH_MAX = 1.57

def getFloorHeight():
    p = BigWorld.player()
    floorHeight = MCD.data.get(p.mapID, {}).get('floorHeight', (FLOOR_HEIGHT_MIN, FLOOR_HEIGHT_MID, FLOOR_HEIGHT_MAX))
    return floorHeight


def getFloorHeightMin():
    return getFloorHeight()[0]


def getFloorHeightMid():
    return getFloorHeight()[1]


def getFloorHeightMax():
    return getFloorHeight()[2]


class BWObjectInfo(object):

    def __init__(self, uuid = 0, furnitureId = 0):
        self.ownerUUID = uuid
        self.furnitureId = furnitureId
        self.position = None
        self.direction = None
        self.parentUUID = ''
        self.isNew = False
        self.ownerGbID = 0

    def initFromTuple(self, info):
        self.furnitureId = info[0]
        self.position = info[1]
        self.direction = info[2]
        self.parentUUID = info[3]
        if len(info) >= 5:
            self.ownerGbID = info[4]

    def dumpToDict(self):
        map = {}
        map['furnitureId'] = self.furnitureId
        map['ownerUUID'] = self.ownerUUID
        map['position'] = self.position
        map['direction'] = self.direction
        if self.parentUUID:
            map['parentUUID'] = self.parentUUID
        return {self.ownerUUID: map}

    def dumpToDict2(self):
        map = {}
        map['furnitureId'] = self.furnitureId
        map['ownerUUID'] = self.ownerUUID
        map['parentUUID'] = self.parentUUID
        map['isNew'] = self.isNew
        return map

    def syncEntity(self, ent):
        if ent:
            self.position = ent.position.tuple()
            self.direction = (ent.roll, ent.pitch, ent.yaw)
            self.isNew = False

    def reSyncEntity(self, ent):
        if ent:
            if self.position and hasattr(ent.filter, 'position'):
                ent.filter.position = self.position
            if self.direction and hasattr(ent.filter, 'yaw'):
                ent.filter.yaw = self.direction[2]
                ent.filter.pitch = self.direction[1]

    def addParent(self, subId):
        self.parentUUID = subId

    def __eq__(self, other):
        return self.ownerUUID == other.ownerUUID and self.parentUUID == other.parentUUID and self.position == other.position and self.direction == other.direction and self.furnitureId == other.furnitureId


def instance():
    return BWEditor.getInstance()


def findDropPoint(result):
    player = BigWorld.player()
    pos = Math.Vector3(result)
    newPos = BigWorld.findDropPoint(player.spaceID, Math.Vector3(pos[0], pos[1] + 2, pos[2]))
    if newPos:
        newPos = newPos[0]
    else:
        newPos = pos
    return newPos


def findUpPoint(result):
    pass


KEY_EQUIP = 'equips'
KEY_ASPECT = 'aspect'
KEY_PHYSIQUE = 'physique'
KEY_AVATARCONFIG = 'avatarConfig'
KEY_ACTION_ID = 'actionId'
KEY_ITEM_PLUS_INFO = 'itemPlusInfo'
BATCH_LOADING_NUM = 1500
BATCH_SAVE_NUM = 15

class UniqueIntFactory(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.clear()

    def clear(self):
        self.map = {'0': 0}
        self.array = ['0']

    def toInt(self, strVal):
        if strVal not in self.map:
            self.array.append(strVal)
            self.map[strVal] = len(self.array) - 1
        return self.map[strVal]

    def toStr(self, intVal):
        if intVal < len(self.array):
            return self.array[intVal]
        return -1


gUniqueInt = UniqueIntFactory.getInstance()

def enableCubeOptimization():
    return gameglobal.rds.configData.get('enableCubeOptimization', False) and CubeModel != None


def isCubeFurniture(furnitureId):
    ifd = IFD.data.get(furnitureId, {})
    return ifd.get('isCubeFurniture', 0)


class BWEditor(object):
    __metaclass__ = Singleton
    CLIENT_UUID_POSTFIX_BEGIN = '@@client_furniture_'
    CLIENT_UUID_POSTFIX = CLIENT_UUID_POSTFIX_BEGIN + '%d'

    def __init__(self):
        super(BWEditor, self).__init__()
        self.reset()
        self.reloadKey()

    def reset(self):
        self.bwInfoMap = {}
        self.bwEntityIdMap = {}
        self.bwPhysiqueInfoMap = {}
        self.selectedEnt = None
        self.editMode = False
        self.bwInfoMapSave = {}
        self.isRightPos = True
        self.parentUUID = None
        self.furnitureUsed = {}
        self.furnitureRecycle = []
        self.lastLeftMouseDownTime = 0
        self.entScreenPos = None
        self._q = False
        self._e = False
        self._z = False
        self._c = False
        self._isSlow = False
        self.rotateHandle = None
        self.updateMouseHandle = None
        self._left = False
        self._right = False
        self._up = False
        self._down = False
        self.moveHandle = None
        self.interactiveObjectMap = {}
        self.modifiedSuccData = {}
        self.saveAndQuit = False
        self.isDrag = False
        self.increasedId = 0
        self.ownerGbID = 0
        self.lastTabTime = 0
        self.tabTargetIdx = 0
        self.tabTargetCandidates = []
        self.oldIgnoreMaterialKind = []
        self.focusedTarget = None
        self.ownerName = None
        self.bwInfoMapLoadCache = {}
        self.batchCreateHandle = None
        self.batchSaveHandle = None
        self.batchSaveData = []
        self.cubeData = {}
        self.cubeModel = None
        self.cubeRegisterNum = 0
        self.selectCubeEntId = 0

    def init(self, gbId, info):
        gamelog.debug('@bgf BWEditor@init', gbId, info)
        self.ownerGbID = gbId
        if not info:
            return
        gUniqueInt.clear()
        self.bwInfoMap = {}
        for key, value in info.iteritems():
            bwInfo = BWObjectInfo(key)
            bwInfo.initFromTuple(value)
            self.bwInfoMap[key] = bwInfo

        self.createAllFurniture()

    def updatePhysiqueInfo(self, uuid, equips, aspect, physique, avatarConfig, actionId, itemPlusInfo):
        self.bwPhysiqueInfoMap[uuid] = {KEY_EQUIP: equips,
         KEY_ASPECT: aspect,
         KEY_PHYSIQUE: physique,
         KEY_AVATARCONFIG: avatarConfig,
         KEY_ACTION_ID: actionId,
         KEY_ITEM_PLUS_INFO: itemPlusInfo}

    def getPhysiqueInfo(self, uuid):
        return (self.bwPhysiqueInfoMap.get(uuid, {}).get(KEY_EQUIP),
         self.bwPhysiqueInfoMap.get(uuid, {}).get(KEY_ASPECT),
         self.bwPhysiqueInfoMap.get(uuid, {}).get(KEY_PHYSIQUE, {}),
         self.bwPhysiqueInfoMap.get(uuid, {}).get(KEY_AVATARCONFIG, ''),
         self.bwPhysiqueInfoMap.get(uuid, {}).get(KEY_ACTION_ID, 0),
         self.bwPhysiqueInfoMap.get(uuid, {}).get(KEY_ITEM_PLUS_INFO, 0))

    def export(self):
        if self.selectedEnt:
            item = self.findBWObject(self.selectedEnt.ownerUUID)
            item.syncEntity(self.selectedEnt)
        ret = {}
        for item in self.bwInfoMap.itervalues():
            ret.update(item.dumpToDict())

        return ret

    def getEntityId(self, uuid):
        return self.bwEntityIdMap.get(uuid, 0)

    def getAllHomeFurniture(self):
        entList = []
        for uuid, eId in self.bwEntityIdMap.iteritems():
            ent = BigWorld.entities.get(eId)
            if ent:
                entList.append(ent)

        return entList

    def getAllDressUpFurniture(self):
        dressUpFurnitures = []
        furnitures = self.getAllHomeFurniture()
        for furniture in furnitures:
            if furniture and furniture.isAvatarFurniture():
                dressUpFurnitures.append(furniture)

        return dressUpFurnitures

    def setPlayerHair(self, map):
        a = strmap.strmap('')
        playerAC = strmap.strmap(BigWorld.player().avatarConfig)
        playerHair = playerAC.map.get('hairDyes')
        a.set('hairDyes', playerHair)
        a.set('dyeMode', 1)
        map['avatarConfig'] = str(a)

    def transferValidPos(self, info):
        data = IFD.data.get(info.furnitureId, {})
        player = BigWorld.player()
        pos = info.position
        if data.get('type', 0) == const.HOME_FURNITURE_TYPE_AVATAR:
            pos = player.transferFittingRoomValidArea(info.position, self.ownerGbID)
        elif formula.spaceInHomeRoom(player.spaceNo):
            pos = player.transferHomeRoomValidArea(info.position)
        else:
            pos = player.transferLargeRoomValidArea(info.position)
        return pos

    def createEntity(self, info, isNew = False, ownerGbID = 0, extra = None):
        player = BigWorld.player()
        spaceID = player.spaceID
        map = info.dumpToDict2()
        data = IFD.data.get(info.furnitureId, {})
        if data.get('type', 0) == const.HOME_FURNITURE_TYPE_AVATAR:
            physique = {}
            if data.get('advancedModel', False):
                map['physique'] = copy.deepcopy(player.physique)
            else:
                physique['school'] = data.get('school', 0)
                physique['sex'] = data.get('sex', 0)
                physique['face'] = data.get('face', 0)
                physique['hair'] = data.get('hair', 0)
                physique['bodyType'] = data.get('bodyType', 0)
                map['physique'] = Physique(physique)
            map['aspect'] = Appearance({})
            map['avatarConfig'] = ''
            if isNew:
                if data.get('advancedModel', False):
                    map['avatarConfig'] = str(player.avatarConfig)
                    map['physique'] = copy.deepcopy(player.physique)
                else:
                    self.setPlayerHair(map)
            elif ownerGbID and ownerGbID != player.gbId:
                if data.get('advancedModel', False):
                    map['avatarConfig'] = str(extra and extra.get('avatarConfig') or player.avatarConfig)
                    map['physique'] = extra and extra.get('physique') and Physique(extra.get('physique')) or copy.deepcopy(player.physique)
        if data.get('playerClone', 0):
            if ownerGbID and ownerGbID != player.gbId:
                map['physique'] = extra and extra.get('physique') and Physique(extra.get('physique')) or copy.deepcopy(player.physique)
                map['aspect'] = Appearance(extra and extra.get('aspect') or player.aspect.deepcopy())
                map['avatarConfig'] = extra and extra.get('avatarConfig') or player.avatarConfig
            else:
                map['physique'] = copy.deepcopy(player.physique)
                map['aspect'] = Appearance(player.aspect.deepcopy())
                map['avatarConfig'] = player.avatarConfig
        pos = self.transferValidPos(info)
        entityID = BigWorld.createEntity('HomeFurniture', spaceID, 0, pos, info.direction, map)
        self.bwEntityIdMap[info.ownerUUID] = entityID
        return entityID

    def findBWObject(self, ownerUUID):
        return self.bwInfoMap.get(ownerUUID, None)

    def removeEntity(self, entId, clearInfo = True):
        ent = BigWorld.entity(entId)
        if ent:
            ownerUUID = ent.ownerUUID
            BigWorld.destroyEntity(entId)
            item = self.findBWObject(ownerUUID)
            if item:
                if clearInfo:
                    self.bwInfoMap.pop(ownerUUID, None)
                self.bwEntityIdMap.pop(ownerUUID, None)

    def createAllFurniture(self):
        self.bwInfoMapLoadCache = {}
        self.cubeData = {}
        for key, item in self.bwInfoMap.iteritems():
            furnitureId = item.furnitureId
            if enableCubeOptimization() and isCubeFurniture(furnitureId):
                self.cubeData.setdefault(furnitureId, [])
                self.cubeData[furnitureId].append(item)
            else:
                self.bwInfoMapLoadCache[key] = item

        self.batchCreateEntity()
        self.createAllCube()

    def createAllCube(self):
        if not enableCubeOptimization():
            return
        if not self.cubeData:
            return
        import HomeFurniture
        for furnitureId in self.cubeData.iterkeys():
            path = HomeFurniture.HomeFurniture.getModelPath(furnitureId).get('fullPath', None)
            if path:
                ret = CubeModel.registerModel(furnitureId, path, self._registerAllCubeCallback)
                self.cubeRegisterNum += 1 if ret else 0
        else:
            self.cubeModel = BigWorld.MCCubes()
            if not self.cubeRegisterNum:
                BigWorld.player().addModel(self.cubeModel)

        array = []
        for furnitureId, items in self.cubeData.iteritems():
            for item in items:
                uuidInt = gUniqueInt.toInt(item.ownerUUID)
                pos = self.transferValidPos(item)
                dir = item.direction
                array.append((pos[0],
                 pos[1],
                 pos[2],
                 dir[2],
                 dir[1],
                 dir[0],
                 uuidInt,
                 furnitureId,
                 0))

        self.cubeModel.add(array)

    def removeAllCube(self):
        self.cubeData = {}
        if self.cubeModel:
            self.cubeModel.clear()
            BigWorld.player().delModel(self.cubeModel)
        self.cubeModel = None
        self.selectCubeEntId = 0

    def createCube(self, info):
        if not enableCubeOptimization():
            return
        import HomeFurniture
        furnitureId = info.furnitureId
        path = HomeFurniture.HomeFurniture.getModelPath(furnitureId).get('fullPath', None)
        if path:
            if not CubeModel.registerModel(furnitureId, path, Functor(self._registerSingleCubeCallback, info)):
                self._registerSingleCubeCallback(info, None)

    def _registerSingleCubeCallback(self, info, path):
        if not self.cubeModel:
            self.cubeModel = BigWorld.MCCubes()
            BigWorld.player().addModel(self.cubeModel)
        uuidInt = gUniqueInt.toInt(info.ownerUUID)
        pos = self.transferValidPos(info)
        dir = info.direction
        self.cubeModel.add([(pos[0],
          pos[1],
          pos[2],
          dir[2],
          dir[1],
          dir[0],
          uuidInt,
          info.furnitureId,
          0)])

    def _registerAllCubeCallback(self, path):
        self.cubeRegisterNum -= 1
        if not self.cubeRegisterNum and self.cubeModel:
            BigWorld.player().addModel(self.cubeModel)

    def removeCube(self, uuIdStr):
        if self.cubeModel:
            uuIdInt = gUniqueInt.toInt(uuIdStr)
            self.cubeModel.remove([uuIdInt])

    def batchCreateEntity(self):
        if self.batchCreateHandle:
            BigWorld.cancelCallback(self.batchCreateHandle)
            self.batchCreateHandle = None
        gTaskMgr = seqTask.gTaskMgr
        count = 0
        while self.bwInfoMapLoadCache and count <= BATCH_LOADING_NUM:
            if gTaskMgr and len(gTaskMgr.fetchCache) <= gTaskMgr.checkMaxCache or not gTaskMgr:
                key, item = self.bwInfoMapLoadCache.popitem()
                self.createEntity(item)
                count += 1
            else:
                break

        if self.bwInfoMapLoadCache:
            self.batchCreateHandle = BigWorld.callback(5, self.batchCreateEntity)

    def removeAllFurniture(self):
        if self.batchCreateHandle:
            BigWorld.cancelCallback(self.batchCreateHandle)
            self.batchCreateHandle = None
        self.bwInfoMapLoadCache = {}
        for entId in self.bwEntityIdMap.values():
            self.removeEntity(entId)

        self.bwInfoMap = {}
        self.removeAllCube()

    def addFurniture(self, uuid, furnitureId, isNew = False, newBwObject = None, ownerGbID = 0, extra = None):
        if not newBwObject:
            bwObject = BWObjectInfo(uuid, furnitureId)
            p = BigWorld.player()
            bwObject.syncEntity(p)
            bwObject.isNew = isNew
            bwObject.direction = (0, 0, 0)
        else:
            bwObject = newBwObject
            furnitureId = bwObject.furnitureId
        self.bwInfoMap[bwObject.ownerUUID] = bwObject
        if not isNew and enableCubeOptimization() and isCubeFurniture(furnitureId):
            return self.createCube(bwObject)
        return self.createEntity(bwObject, isNew, ownerGbID=ownerGbID, extra=extra)

    def delFurniture(self, uuId):
        entId = self.getEntityId(uuId)
        if entId:
            self.removeEntity(entId)
        else:
            self.removeCube(uuId)

    def updateEntity(self, entId, bwInfo):
        ent = BigWorld.entity(entId)
        if ent:
            if utils.instanceof(ent.filter, 'ClientFilter'):
                if bwInfo.position:
                    ent.filter.position = bwInfo.position
                if bwInfo.direction:
                    ent.filter.yaw = bwInfo.direction[2]
                    ent.filter.pitch = bwInfo.direction[1]

    def updateCube(self, uuIdStr, value):
        if self.cubeModel:
            uuIdInt = gUniqueInt.toInt(uuIdStr)
            self.cubeModel.remove([uuIdInt])
            pos = value.position
            dir = value.direction
            self.cubeModel.add([(pos[0],
              pos[1],
              pos[2],
              dir[2],
              dir[1],
              dir[0],
              uuIdInt,
              value.furnitureId,
              0)])

    def updateFurniture(self, uuId, value):
        bwInfo = self.findBWObject(uuId)
        if not bwInfo:
            bwInfo = BWObjectInfo(uuId)
        bwInfo.initFromTuple(value)
        self.bwInfoMap[uuId] = bwInfo
        entId = self.getEntityId(uuId)
        if entId:
            self.updateEntity(entId, bwInfo)
        else:
            self.updateCube(uuId, bwInfo)

    def delSelEntity(self):
        if self.selectedEnt:
            self.removeEntity(self.selectedEnt.id)

    def lockTarget(self, ent):
        player = BigWorld.player()
        if self.selectedEnt:
            if self.selectedEnt == player.targetLocked:
                player.lockTarget(None)
            self.selectedEnt = None
        if ent and getattr(ent, 'ownerUUID', 0):
            self.selectedEnt = ent
            BigWorld.callback(0.2, Functor(player.lockTarget, ent))

    def updateMousePosition(self):
        if self.selectedEnt:
            if not self.selectedEnt.inWorld:
                return
            if self.updateMouseHandle:
                BigWorld.cancelCallback(self.updateMouseHandle)
            player = BigWorld.player()
            result = BigWorld.getCursorPosInWorld(player.spaceID, 1000, False, (gameglobal.TREEMATTERKINDS, gameglobal.GLASSMATTERKINDS))
            screenWidth = BigWorld.screenWidth()
            screenHeight = BigWorld.screenHeight()
            mousePos = C_ui.get_cursor_pos()
            if not (mousePos[0] < 0 or mousePos[0] > screenWidth or mousePos[1] < 0 or mousePos[1] > screenHeight):
                if result[0]:
                    pos = result[0]
                    self._updateMousePosition(pos)
                    self.isDrag = True
                    self.selectedEnt.setCollide(False)
            self.updateMouseHandle = BigWorld.callback(0.01, self.updateMousePosition)

    def checkEntPosValid(self, ent, pos):
        if not (ent.isWallAttached() or ent.isRoofAttached()):
            pos = findDropPoint(pos)
        controlPos = ent.getControlPointPos()
        value = True
        if controlPos:
            value = self.checkPosValid(ent, controlPos)
        value = value and self.checkPosValid(ent, pos)
        return value

    def _updateMousePosition(self, pos):
        if not self.selectedEnt or not self.selectedEnt.inWorld:
            return
        value = self.checkEntPosValid(self.selectedEnt, pos)
        self.setPosValid(self.selectedEnt, value)
        if not (self.selectedEnt.isWallAttached() or self.selectedEnt.isRoofAttached()):
            pos = findDropPoint(pos)
        if utils.instanceof(self.selectedEnt.filter, 'ClientFilter'):
            self.selectedEnt.filter.position = pos

    def getChildEntity(self, ent):
        ret = []
        if ent and ent.ownerUUID:
            for entId in self.bwEntityIdMap.itervalues():
                newEnt = BigWorld.entity(entId)
                if newEnt and newEnt.parentUUID == ent.ownerUUID:
                    ret.append(newEnt)

        return ret

    def handleMouseRotate(self, mp):
        if self.selectedEnt:
            self.selectedEnt.filter.setYaw(mp.yaw)
            bwObject = self.findBWObject(self.selectedEnt.ownerUUID)
            bwObject.syncEntity(self.selectedEnt)

    def addChild(self, subEnt, ent):
        bwObject = self.bwInfoMap[ent.ownerUUID]
        bwObject.addChild(subEnt.ownerUUID)

    def setEditMode(self, value):
        self.editMode = value
        for entId in self.bwEntityIdMap.itervalues():
            ent = BigWorld.entity(entId)
            if ent:
                ent.refreshOpacityState()
                ent.refreshTargetCaps()
                if not value:
                    ent.triggerTrap(True)

        for entId in self.interactiveObjectMap.itervalues():
            ent = BigWorld.entity(entId)
            if ent:
                ent.refreshOpacityState()
                if not value:
                    ent.triggerTrap(True)

        if not value and self.selectedEnt:
            if self.selectedEnt.inWorld:
                bwObject = self.findBWObject(getattr(self.selectedEnt, 'ownerUUID', 0))
                if bwObject:
                    if not bwObject.isNew:
                        bwObject.reSyncEntity(self.selectedEnt)
            self.lockTarget(None)
        cam = BigWorld.camera()
        if hasattr(cam, 'ignoreMaterialKind'):
            if value:
                if not self.oldIgnoreMaterialKind:
                    self.oldIgnoreMaterialKind = cam.ignoreMaterialKind()
                cam.ignoreMaterialKind([])
            elif not value:
                cam.ignoreMaterialKind(*self.oldIgnoreMaterialKind)

    def destroy(self):
        self.removeAllFurniture()
        self.clearFurnitureRecycle()
        self.clearFurnitureUsed()
        self.reset()

    def handleMouseEvent(self, dx, dy, dz):
        if not self.editMode:
            return False
        if self.selectedEnt:
            count = dz / 120
            value = YAW_ROTATE_VALUE * count
            if self._isSlow:
                value *= 0.125
            if utils.instanceof(self.selectedEnt.filter, 'ClientFilter'):
                self.selectedEnt.filter.yaw -= value
            if self.rotateHandle:
                BigWorld.cancelCallback(self.rotateHandle)
            self.rotateHandle = BigWorld.callback(0.1, self.syncEntity)
            return True
        return False

    def syncEntity(self):
        if self.selectedEnt:
            bwObject = self.findBWObject(self.selectedEnt.ownerUUID)
            if bwObject and not bwObject.isNew:
                bwObject.syncEntity(self.selectedEnt)

    def handleKeyEvent(self, down, key, vk, mods):
        rdfkey = None
        if key in (keys.KEY_MOUSE0, keys.KEY_MOUSE1):
            rdfkey = HK.keyDef(key, 1, 0)
        else:
            rdfkey = HK.keyDef(key, 1, mods)
        if key in (keys.KEY_LSHIFT, keys.KEY_RSHIFT):
            self._isSlow = down
        for downKeys, action in self.keyBindings:
            if rdfkey in downKeys:
                return action(down)

        return False

    def reloadKey(self):
        self.keyBindings = [([HK.keyDef(keys.KEY_LEFTMOUSE, 1, 0)], self.leftMouseFunction),
         ([HK.keyDef(keys.KEY_ESCAPE, 1, 0)], self.handleEscape),
         ([HK.keyDef(keys.KEY_Q, 1, 0)], self.clockRotate),
         ([HK.keyDef(keys.KEY_E, 1, 0)], self.unClockRotate),
         ([HK.keyDef(keys.KEY_Q, 1, 1)], self.clockRotateSlowly),
         ([HK.keyDef(keys.KEY_E, 1, 1)], self.unClockRotateSlowly),
         ([HK.keyDef(keys.KEY_DELETE, 1, 0)], self.handleKeyDelete),
         ([HK.keyDef(keys.KEY_S, 1, 2)], self.handleSaveArrange),
         ([HK.HKM[HK.KEY_SHOW_BAG]], self.handleShowInv),
         ([HK.keyDef(keys.KEY_TAB, 1, 0)], self.selectNearHomeFurniture),
         ([HK.keyDef(keys.KEY_LEFTARROW, 1, 0)], self.leftMove),
         ([HK.keyDef(keys.KEY_RIGHTARROW, 1, 0)], self.rightMove),
         ([HK.keyDef(keys.KEY_UPARROW, 1, 0)], self.upMove),
         ([HK.keyDef(keys.KEY_DOWNARROW, 1, 0)], self.downMove),
         ([HK.keyDef(keys.KEY_LEFTARROW, 1, 1)], self.leftMoveSlowly),
         ([HK.keyDef(keys.KEY_RIGHTARROW, 1, 1)], self.rightMoveSlowly),
         ([HK.keyDef(keys.KEY_UPARROW, 1, 1)], self.upMoveSlowly),
         ([HK.keyDef(keys.KEY_DOWNARROW, 1, 1)], self.downMoveSlowly),
         ([HK.keyDef(keys.KEY_Z, 1, 0)], self.clockRotatePitch),
         ([HK.keyDef(keys.KEY_C, 1, 0)], self.unClockRotatePitch),
         ([HK.keyDef(keys.KEY_Z, 1, 1)], self.clockRotatePitchSlowly),
         ([HK.keyDef(keys.KEY_C, 1, 1)], self.unClockRotatePitchSlowly)]

    def selectNearHomeFurniture(self, isDown):
        if isDown:
            return False
        if not self.editMode:
            return False
        ents = BigWorld.inCameraEntity(80)
        if ents == None or len(ents) <= 0:
            return False
        ret = self.getNearestTarget()
        if ret:
            self.lockTarget(ret)
            return True
        return False

    def getNearestTarget(self):
        if self.needRegenCandidates():
            self.regenCandidates()
            self.tabTargetIdx = 0
            self.lastTabTime = utils.getNow()
            target = self.getTargetFromCandidates()
            return target
        else:
            target = self.getTargetFromCandidates()
            if not target:
                self.regenCandidates()
                target = self.getTargetFromCandidates()
            self.lastTabTime = utils.getNow()
            return target

    def regenCandidates(self):
        candidates = []
        blockDist = SCD.data.get('tabTargetDist', 80)
        player = BigWorld.player()
        ents = BigWorld.inCameraEntity(blockDist)
        if ents == None or len(ents) <= 0:
            return
        for ent in ents:
            if self.isHomeFurniture(ent) and ent.canSelected():
                candidates.append((ent, (ent.position - player.position).length))

        if candidates:
            candidates.sort(lambda x, y: cmp(x[1], y[1]))
            self.tabTargetCandidates = [ x[0] for x in candidates ]
        else:
            self.tabTargetCandidates = []

    def needRegenCandidates(self):
        if self.tabTargetIdx >= len(self.tabTargetCandidates):
            return True
        now = utils.getNow()
        if now - self.lastTabTime > SCD.data.get('tabTargetLastTime', 3):
            return True
        return False

    def getTargetFromCandidates(self):
        num = len(self.tabTargetCandidates)
        idx = self.tabTargetIdx
        for i in xrange(idx, num):
            ent = self.tabTargetCandidates[i]
            self.tabTargetIdx = self.tabTargetIdx + 1
            if ent:
                if self.isHomeFurniture(ent) and ent.canSelected():
                    if ent == self.selectedEnt:
                        continue
                    return ent

    def getCursorPosInClip(self, cursorPos):
        innerScreenSize = 1.0
        if hasattr(BigWorld, 'getInnerScreenSize'):
            innerScreenSize = BigWorld.getInnerScreenSize()
        screenWidth = BigWorld.screenWidth() / innerScreenSize * 0.5
        screenHeight = BigWorld.screenHeight() / innerScreenSize * 0.5
        x = (cursorPos[0] - screenWidth) / screenWidth
        y = -(cursorPos[1] - screenHeight) / screenHeight
        return (x, y)

    def leftMouseFunction(self, isDown):
        if not isDown:
            if self.entScreenPos:
                cursor.setOutAndSaveOldPos([int(self.entScreenPos[0]), int(self.entScreenPos[1])])
                self.entScreenPos = None
                if self.selectedEnt:
                    self.updateMousePosition()
            return False
        if not self.editMode:
            return False
        player = BigWorld.player()
        ent = player.target
        nowTime = BigWorld.time()
        cursorPos = C_ui.get_cursor_pos()
        if cursorPos[0] < 0 or cursorPos[1] < 0:
            cursorPos = cursor.oldCursorPos
        if cursorPos:
            cursorPos = self.getCursorPosInClip(cursorPos)
            res = BigWorld.getScreenPosInWorld(player.spaceID, cursorPos[0], cursorPos[1], 1000, False, (gameglobal.GLASSMATTERKINDS,))
            if res and res[2]:
                if res[1] == None:
                    pickEnt = BigWorld.entity(res[2])
                    if pickEnt and pickEnt.inWorld and self.isHomeFurniture(pickEnt):
                        ent = pickEnt
                elif res[1] == -1 and enableCubeOptimization() and not (self.selectedEnt and self.isDrag):
                    uniqueId = res[2]
                    self.cubeModel.remove([uniqueId])
                    uniqueStr = gUniqueInt.toStr(uniqueId)
                    info = self.findBWObject(uniqueStr)
                    if self.bwEntityIdMap.has_key(uniqueStr):
                        entId = self.getEntityId(uniqueStr)
                        ent = BigWorld.entity(entId)
                    elif info:
                        if self.selectCubeEntId:
                            oldEnt = BigWorld.entity(self.selectCubeEntId)
                            if oldEnt:
                                if oldEnt.ownerUUID == uniqueStr:
                                    ent = oldEnt
                                else:
                                    if self.cubeModel:
                                        oldInfo = self.findBWObject(oldEnt.ownerUUID)
                                        if oldInfo:
                                            pos = oldInfo.position
                                            dir = oldInfo.direction
                                            uuidInt = gUniqueInt.toInt(oldInfo.ownerUUID)
                                            self.cubeModel.add([(pos[0],
                                              pos[1],
                                              pos[2],
                                              dir[2],
                                              dir[1],
                                              dir[0],
                                              uuidInt,
                                              oldInfo.furnitureId,
                                              0)])
                                    self.removeEntity(self.selectCubeEntId, False)
                                    self.selectCubeEntId = 0
                            else:
                                self.selectCubeEntId = 0
                        if not self.selectCubeEntId:
                            self.selectCubeEntId = self.createEntity(info, False)
                            ent = BigWorld.entity(self.selectCubeEntId)
        if nowTime - self.lastLeftMouseDownTime <= 0.3:
            if self.selectedEnt and ent == self.selectedEnt:
                self.entScreenPos = clientcom.worldPointToScreenCheckBound(ent.position)
                gameglobal.rds.ui.inventory.hide()
        elif self.selectedEnt and self.isDrag:
            self.endMoveTarget(ent)
        elif ent and self.isHomeFurniture(ent):
            self.lockTarget(ent)
        self.lastLeftMouseDownTime = nowTime
        return False

    def endMoveTarget(self, ent):
        player = BigWorld.player()
        if self.selectedEnt:
            if not self.isRightPos:
                player.showGameMsg(GMDD.data.FURNITURE_POS_NOT_VALID, ())
                return
            bwObject = self.findBWObject(self.selectedEnt.ownerUUID)
            if bwObject:
                bwObject.syncEntity(self.selectedEnt)
                if self.parentUUID:
                    bwObject.addParent(self.parentUUID)
            childEntity = self.getChildEntity(self.selectedEnt)
            for ent in childEntity:
                bwObject = self.findBWObject(ent.ownerUUID)
                if bwObject:
                    bwObject.syncEntity(ent)

            self.selectedEnt.refreshCollide()
            self.lockTarget(None)
            self.isDrag = False
            if not gameglobal.rds.ui.inventory.isShow():
                gameglobal.rds.ui.homeEditor.openInv(True)

    def rightMouseFunction(self, isDown):
        if not isDown:
            return False
        if not self.editMode:
            return False
        if self.selectedEnt:
            ent = self.selectedEnt
            self.lockTarget(None)
            bwObject = self.findBWObject(ent.ownerUUID)
            if bwObject:
                if not bwObject.isNew:
                    bwObject.reSyncEntity(ent)
                    gameglobal.rds.ui.homeEditor.openInv(True)
                else:
                    self.handleKeyDelete(isDown, ent)
                return True
        return False

    def handleEscape(self, isDown):
        if isDown:
            return False
        elif not self.editMode:
            return False
        elif self.selectedEnt:
            ent = self.selectedEnt
            self.lockTarget(None)
            if ent.inWorld:
                bwObject = self.findBWObject(ent.ownerUUID)
                if bwObject and not bwObject.isNew:
                    bwObject.reSyncEntity(ent)
                    gameglobal.rds.ui.homeEditor.openInv(True)
                else:
                    self.handleKeyDelete(1, ent)
            return True
        else:
            gameglobal.rds.ui.homeEditor.quitEditMode()
            return True
        return False

    def clockRotate(self, isDown):
        self._q = isDown
        self._isSlow = False
        return self.rotateYaw()

    def unClockRotate(self, isDown):
        self._e = isDown
        self._isSlow = False
        return self.rotateYaw()

    def clockRotateSlowly(self, isDown):
        self._q = isDown
        self._isSlow = isDown
        return self.rotateYaw()

    def unClockRotateSlowly(self, isDown):
        self._e = isDown
        self._isSlow = isDown
        return self.rotateYaw()

    def rotateYaw(self):
        if not self.editMode:
            return False
        if self.selectedEnt:
            self._rotateYaw()
            return True
        return False

    def _rotateYaw(self):
        if not self._q and not self._e:
            self.syncEntity()
            return
        if not self.selectedEnt or not self.selectedEnt.inWorld:
            return
        if self.rotateHandle:
            BigWorld.cancelCallback(self.rotateHandle)
        if self._q:
            isClock = True
        elif self._e:
            isClock = False
        isSlow = self._isSlow
        if utils.instanceof(self.selectedEnt.filter, 'ClientFilter'):
            self.selectedEnt.filter.yaw += self.getRotateValue(isClock, isSlow)
        self.rotateHandle = BigWorld.callback(0.05, self._rotateYaw)

    def getRotateValue(self, isClock, isSlow):
        value = YAW_ROTATE_VALUE
        if isClock:
            value = -value
        if isSlow:
            value *= 0.125
        return value

    def clockRotatePitch(self, isDown):
        self._z = isDown
        self._isSlow = False
        return self.rotatePitch()

    def unClockRotatePitch(self, isDown):
        self._c = isDown
        self._isSlow = False
        return self.rotatePitch()

    def clockRotatePitchSlowly(self, isDown):
        self._z = isDown
        self._isSlow = isDown
        return self.rotatePitch()

    def unClockRotatePitchSlowly(self, isDown):
        self._c = isDown
        self._isSlow = isDown
        return self.rotatePitch()

    def rotatePitch(self):
        if not gameglobal.rds.configData.get('enableFurnitureRotatePitch', False):
            return False
        if not self.editMode:
            return False
        if self.selectedEnt:
            self._rotatePitch()
            return True
        return False

    def _rotatePitch(self):
        if not self._z and not self._c:
            self.syncEntity()
            return
        if not self.selectedEnt or not self.selectedEnt.inWorld:
            return
        if self.rotateHandle:
            BigWorld.cancelCallback(self.rotateHandle)
        if self._z:
            isClock = True
        elif self._c:
            isClock = False
        isSlow = self._isSlow
        if utils.instanceof(self.selectedEnt.filter, 'ClientFilter'):
            if hasattr(self.selectedEnt.filter, 'enableRotatePitch') and self.selectedEnt.canRotatePitch():
                self.selectedEnt.filter.enableRotatePitch = True
                pitch = self.selectedEnt.filter.pitch
                pitch += self.getRotateValue(isClock, isSlow)
                if pitch > PITCH_MAX:
                    pitch = PITCH_MAX
                if pitch < PITCH_MIN:
                    pitch = PITCH_MIN
                self.selectedEnt.filter.pitch = pitch
        self.rotateHandle = BigWorld.callback(0.05, self._rotatePitch)

    def handleKeyDelete(self, isDown, ent = None):
        if not isDown:
            return False
        ent = self.selectedEnt if not ent else ent
        if ent and self.isHomeFurniture(ent) and self.canRecycleFurniture(ent.ownerUUID):
            if self.selectedEnt == ent:
                self.lockTarget(None)
            self.recycleFurniture(ent.ownerUUID, ent.furnitureId, ent.isNew)
            self.removeEntity(ent.id)
            gameglobal.rds.ui.homeEditor.openInv(True)
            return True
        return False

    def saveState(self):
        self.bwInfoMapSave = copy.deepcopy(self.bwInfoMap)

    def haveModified(self):
        return self.bwInfoMap != self.bwInfoMapSave

    def getModifyUUID(self):
        newSet = set(self.bwInfoMap.keys())
        oldSet = set(self.bwInfoMapSave.keys())
        addSet = newSet - oldSet
        removeSet = oldSet - newSet
        updateSet = newSet & oldSet
        for uuid in list(updateSet):
            if self.bwInfoMap[uuid] == self.bwInfoMapSave[uuid]:
                updateSet.remove(uuid)

        addInfo = []
        removeInfo = []
        updateInfo = []
        if addSet:
            addInfo = [[],
             [],
             [],
             [],
             [],
             []]
            for uuid in addSet:
                bwObject = self.findBWObject(uuid)
                invInfo = self.furnitureUsed.get(self.parseClientUUID(uuid), None)
                if bwObject and invInfo:
                    addInfo[0].append(invInfo[2])
                    addInfo[1].append(invInfo[0])
                    addInfo[2].append(invInfo[1])
                    addInfo[3].append(bwObject.position)
                    addInfo[4].append(bwObject.direction)
                    addInfo[5].append(bwObject.parentUUID)

        if removeSet:
            removeInfo = list(removeSet)
        if updateSet:
            updateInfo = [[],
             [],
             [],
             []]
            for uuid in updateSet:
                bwObject = self.findBWObject(uuid)
                if bwObject:
                    updateInfo[0].append(uuid)
                    updateInfo[1].append(bwObject.position)
                    updateInfo[2].append(bwObject.direction)
                    updateInfo[3].append(bwObject.parentUUID)

        return ((addSet, addInfo), (removeSet, removeInfo), (updateSet, updateInfo))

    def targetFocus(self, target):
        if self.selectedEnt and target != self.selectedEnt:
            if not self.selectedEnt.inWorld:
                self.selectedEnt = None
                return
            if target and self.isHomeFurniture(target):
                self.focusedTarget = target
                if not self.checkPosValid(self.selectedEnt, self.selectedEnt.position):
                    self.setPosValid(self.selectedEnt, False)
                else:
                    self.parentUUID = target.ownerUUID

    def setPosValid(self, ent, isValid):
        if isValid:
            selColor = 4278574181L
            outlineHelper.enableOutline(ent.model, selColor)
            self.isRightPos = True
        else:
            selColor = 4294521109L
            outlineHelper.enableOutline(ent.model, selColor)
            self.isRightPos = False

    def checkPosValid(self, ent, pos):
        if self.focusedTarget and self.focusedTarget.inWorld:
            if not ent.canPutOver(self.focusedTarget):
                return False
        else:
            self.focusedTarget = None
        p = BigWorld.player()
        if formula.spaceInHomeEnlargedRoom(p.spaceNo) and not p.inMainRoomValidArea(pos):
            return False
        if formula.spaceInHomeRoom(p.spaceNo) and not p.inHomeRoomValidArea(pos):
            return False
        if ent.isRoofAttached():
            if pos.y <= getFloorHeightMid():
                return False
        elif pos.y >= getFloorHeightMax():
            return False
        return True

    def targetBlur(self, target):
        if self.selectedEnt:
            if target and self.isHomeFurniture(target):
                self.focusedTarget = None
            if self.selectedEnt.inWorld:
                if self.checkPosValid(self.selectedEnt, self.selectedEnt.position):
                    self.setPosValid(self.selectedEnt, True)
            self.parentUUID = None

    def returnToSaveState(self):
        add, remove, update = self.getModifyUUID()
        if add[0]:
            for uuid in add[0]:
                self.delFurniture(uuid)

        if remove[0]:
            for uuid in remove[0]:
                bwObject = self.bwInfoMapSave.get(uuid, None)
                if bwObject:
                    self.addFurniture(uuid, 0, False, bwObject)

        if update[0]:
            for uuid in update[0]:
                bwObject = self.bwInfoMapSave.get(uuid, None)
                entId = self.getEntityId(uuid)
                ent = BigWorld.entity(entId)
                if ent:
                    if bwObject.position:
                        ent.filter.position = bwObject.position
                    if bwObject.direction:
                        ent.filter.yaw = bwObject.direction[2]
                        ent.filter.pitch = bwObject.direction[1]

        self.clearFurnitureRecycle()
        self.clearFurnitureUsed()
        self.bwInfoMap = self.bwInfoMapSave
        self.selectedEnt = None

    def genClientUUID(self, uuid):
        uuid = uuid + self.CLIENT_UUID_POSTFIX % self.increasedId
        self.increasedId += 1
        return uuid

    def parseClientUUID(self, uuid):
        index = uuid.find(self.CLIENT_UUID_POSTFIX_BEGIN)
        if index != -1:
            return uuid[:index]
        return uuid

    def useFurniture(self, it, nPage, nPos, resKind):
        if self.isFurnitureUsedOut(it):
            return
        if self.selectedEnt and self.selectedEnt.inWorld and self.isDrag:
            return
        player = BigWorld.player()
        iType = IFD.data.get(it.id, {}).get('type', 0)
        isInHomeFittingRoom = player.inHomeFittingRoom()
        if not (isInHomeFittingRoom and iType in (const.HOME_FURNITURE_TYPE_AVATAR, const.HOME_FURNITURE_TYPE_ALL) or not isInHomeFittingRoom and iType != const.HOME_FURNITURE_TYPE_AVATAR):
            player.showGameMsg(GMDD.data.AVATAR_HOME_FURNITURE_INVALID_POS, ())
            return
        if iType == const.HOME_FURNITURE_TYPE_AVATAR and not (self.ownerGbID == player.gbId or self.ownerGbID == getattr(player.friend, 'intimacyTgt', 0) and gameglobal.rds.configData.get('enableFittingRoomIntimacy', False)):
            player.showGameMsg(GMDD.data.AVATAR_HOME_FURNITURE_NOT_PUT_BY_INTIMACY, ())
            return
        res = self.furnitureUsed.setdefault(it.guid(), [nPage,
         nPos,
         resKind,
         0])
        res[3] += 1
        gameglobal.rds.ui.inventory.updateSlotState(nPage, nPos)
        uuid = self.genClientUUID(it.guid())
        entId = self.addFurniture(uuid, it.id, True)
        ent = BigWorld.entity(entId)
        self.lockTarget(ent)
        self.updateMousePosition()
        gameglobal.rds.ui.inventory.hide()

    def recycleFurniture(self, uuid, itemId, isNew = False):
        uuid = self.parseClientUUID(uuid)
        if uuid in self.furnitureUsed:
            nPage, nPos, resKind, cnt = self.furnitureUsed[uuid]
            cnt -= 1
            if cnt <= 0:
                self.furnitureUsed.pop(uuid)
            else:
                self.furnitureUsed[uuid][3] = cnt
            if resKind == const.RES_KIND_INV:
                gameglobal.rds.ui.inventory.updateSlotState(nPage, nPos)
        else:
            self.furnitureRecycle.append(uuid)

    def canRecycleFurniture(self, uuid):
        item = self.findBWObject(uuid)
        player = BigWorld.player()
        if item and item.ownerGbID and item.ownerGbID != player.gbId:
            player.showGameMsg(GMDD.data.HOME_FURNITURE_NO_AUTHORITY_REMOVE, ())
            return False
        eId = self.getEntityId(uuid)
        ent = BigWorld.entities.get(eId)
        if ent and ent.isAvatarFurniture() and ent.withEquip():
            player.showGameMsg(GMDD.data.HOME_FURNITURE_WITH_EQUIP, ())
            return False
        return True

    def clearFurnitureRecycle(self):
        self.furnitureRecycle = []

    def clearFurnitureUsed(self):
        if self.furnitureUsed:
            tempData = self.furnitureUsed
            self.furnitureUsed = {}
            for nPage, nPos, resKind, _ in tempData.values():
                gameglobal.rds.ui.inventory.updateSlotState(nPage, nPos)

    def saveArrange(self, saveAndQuit = False):
        add, remove, update = self.getModifyUUID()
        if add[0] and not self.checkAddRoomFurniture(add[1][0], add[1][1], add[1][2]):
            return
        if remove[0] and not self.checkRemoveRoomFurniture(remove[1]):
            return
        self.batchSaveData = [add[1], remove[1], update[1]]
        self.batchSave()
        self.modifiedSuccData = {}
        self.saveAndQuit = saveAndQuit

    def batchSave(self, needAdd = True, needUpdate = True):
        if self.batchSaveHandle:
            BigWorld.cancelCallback(self.batchSaveHandle)
            self.batchSaveHandle = None
        if not self.batchSaveData:
            return
        add, remove, update = self.batchSaveData
        if not add and not remove and not update:
            return
        p = BigWorld.player()
        if (add or remove) and needAdd:
            if add:
                resKinds, invPages, invPos, posList, dirList, parentList = add
                sResKinds, resKinds = resKinds[:BATCH_SAVE_NUM], resKinds[BATCH_SAVE_NUM:]
                sInvPages, invPages = invPages[:BATCH_SAVE_NUM], invPages[BATCH_SAVE_NUM:]
                sInvPos, invPos = invPos[:BATCH_SAVE_NUM], invPos[BATCH_SAVE_NUM:]
                sPosList, posList = posList[:BATCH_SAVE_NUM], posList[BATCH_SAVE_NUM:]
                sDirList, dirList = dirList[:BATCH_SAVE_NUM], dirList[BATCH_SAVE_NUM:]
                sParentList, parentList = parentList[:BATCH_SAVE_NUM], parentList[BATCH_SAVE_NUM:]
                if resKinds:
                    add = [resKinds,
                     invPages,
                     invPos,
                     posList,
                     dirList,
                     parentList]
                else:
                    add = []
            else:
                sResKinds, sInvPages, sInvPos, sPosList, sDirList, sParentList = ([],
                 [],
                 [],
                 [],
                 [],
                 [])
            hairColor = p.getPlayerHairColor()
            sRemove, remove = remove[:BATCH_SAVE_NUM], remove[BATCH_SAVE_NUM:]
            p.cell.alterRoomFurniture(sResKinds, sInvPages, sInvPos, sPosList, sDirList, sParentList, sRemove, hairColor)
        if update and needUpdate:
            uuid, pos, dir, parentUUID = update
            sUUID, uuid = uuid[:BATCH_SAVE_NUM], uuid[BATCH_SAVE_NUM:]
            sPos, pos = pos[:BATCH_SAVE_NUM], pos[BATCH_SAVE_NUM:]
            sDir, dir = dir[:BATCH_SAVE_NUM], dir[BATCH_SAVE_NUM:]
            sParentUUID, parentUUID = parentUUID[:BATCH_SAVE_NUM], parentUUID[BATCH_SAVE_NUM:]
            if uuid:
                update = [uuid,
                 pos,
                 dir,
                 parentUUID]
            else:
                update = []
            p.cell.updateRoomFurniture(sUUID, sPos, sDir, sParentUUID)
        self.batchSaveData = [add, remove, update]

    def checkAddRoomFurniture(self, reskinds, invPages, invPos):
        player = BigWorld.player()
        for pg, ps in zip(invPages, invPos):
            it = player.inv.getQuickVal(pg, ps)
            if not it:
                player.showGameMsg(GMDD.data.NO_FURNITURE, ())
                return False
            if it.hasLatch():
                player.showGameMsg(GMDD.data.ITEM_FORBIDDEN_LATCH, ())
                return False
            if it.id not in IFD.data:
                player.showGameMsg(GMDD.data.NO_FURNITURE, ())
                return False

        return True

    def checkRemoveRoomFurniture(self, uuidList):
        player = BigWorld.player()
        for uuid in uuidList:
            entId = self.interactiveObjectMap.get(uuid, 0)
            if entId:
                ent = BigWorld.entity(entId)
                if ent and getattr(ent, 'avatarMap', {}):
                    player.showGameMsg(GMDD.data.FURNITURE_OCCUPIED, ())
                    return False

        return True

    def addModifiedSuccData(self, opType, data, ownerGbID = 0, extra = None):
        if self.editMode:
            self.updateModifiedSuccData(opType, data)
        elif opType == const.HOME_FURNITURE_OP_ADD:
            for uuid, value in data.iteritems():
                bwInfo = BWObjectInfo(uuid)
                bwInfo.initFromTuple(value)
                self.addFurniture(uuid, 0, False, bwInfo, ownerGbID=ownerGbID, extra=extra)

        elif opType == const.HOME_FURNITURE_OP_REMOVE:
            for uuid in data:
                self.delFurniture(uuid)

        elif opType == const.HOME_FURNITURE_OP_UPDATE:
            for uuid, value in data.iteritems():
                self.updateFurniture(uuid, value)
                entId = self.interactiveObjectMap.get(uuid, 0)
                interEnt = BigWorld.entity(entId)
                if interEnt and utils.instanceof(interEnt.filter, 'DumbFilter'):
                    interEnt.filter.clientYawMinDist = 0
                    BigWorld.callback(0.1, Functor(interEnt.filter.setYaw, value[2][2]))

    def updateModifiedSuccData(self, opType, data):
        if isinstance(data, dict):
            self.modifiedSuccData.setdefault(opType, {})
            self.modifiedSuccData[opType].update(data)
        elif not self.modifiedSuccData.has_key(opType):
            self.modifiedSuccData[opType] = data
        else:
            self.modifiedSuccData[opType] += data
        info = self.getModifyUUID()
        for index, subInfo in enumerate(info):
            if subInfo[0]:
                if not self.modifiedSuccData.has_key(index + 1):
                    return
                if len(subInfo[0]) != len(self.modifiedSuccData[index + 1]):
                    return

        if self.modifiedSuccData.has_key(const.HOME_FURNITURE_OP_ADD):
            add, remove, update = self.getModifyUUID()
            if add[0]:
                for uuid in add[0]:
                    self.delFurniture(uuid)

            for key, value in self.modifiedSuccData[const.HOME_FURNITURE_OP_ADD].iteritems():
                bwInfo = BWObjectInfo(key)
                bwInfo.initFromTuple(value)
                self.addFurniture(key, 0, False, bwInfo)

        if self.modifiedSuccData.has_key(const.HOME_FURNITURE_OP_UPDATE):
            for key, value in self.modifiedSuccData[const.HOME_FURNITURE_OP_UPDATE].iteritems():
                bwInfo = self.findBWObject(key)
                if not bwInfo:
                    bwInfo = BWObjectInfo(key)
                bwInfo.initFromTuple(value)
                entId = self.interactiveObjectMap.get(key, 0)
                interEnt = BigWorld.entity(entId)
                if interEnt and utils.instanceof(interEnt.filter, 'DumbFilter'):
                    interEnt.filter.clientYawMinDist = 0.0
                    BigWorld.callback(0.1, Functor(interEnt.filter.setYaw, bwInfo.direction[2]))

        self.saveState()
        self.clearFurnitureRecycle()
        self.clearFurnitureUsed()
        self.modifiedSuccData = {}
        if self.saveAndQuit:
            self.saveAndQuit = False
            gameglobal.rds.ui.homeEditor.endEditMode()

    def handleSaveArrange(self, isDown):
        if not isDown:
            return False
        if self.editMode:
            self.saveArrange()
            return True
        return False

    def handleShowInv(self, isDown):
        if not isDown:
            return False
        if self.editMode:
            gameglobal.rds.ui.homeEditor.openInv()
            return True
        return False

    def isHomeFurniture(self, ent):
        return utils.instanceof(ent, 'HomeFurniture')

    def addInteractiveObject(self, entId):
        ent = BigWorld.entity(entId)
        if ent:
            uuid = ent.ownerUUID
            if uuid and not self.interactiveObjectMap.has_key(uuid):
                self.interactiveObjectMap[uuid] = ent.id

    def removeInteractiveObject(self, entId):
        ent = BigWorld.entity(entId)
        if ent:
            uuid = ent.ownerUUID
            self.interactiveObjectMap.pop(uuid, None)

    def isFurnitureUsedOut(self, it):
        uuid = it.guid()
        if uuid in self.furnitureUsed:
            if self.furnitureUsed[uuid][3] >= it.cwrap:
                return True
        return False

    def leftMove(self, isDown):
        self._left = isDown
        return self.moveEntity()

    def rightMove(self, isDown):
        self._right = isDown
        return self.moveEntity()

    def upMove(self, isDown):
        self._up = isDown
        return self.moveEntity()

    def downMove(self, isDown):
        self._down = isDown
        return self.moveEntity()

    def leftMoveSlowly(self, isDown):
        self._left = isDown
        self._isSlow = isDown
        return self.moveEntity()

    def rightMoveSlowly(self, isDown):
        self._right = isDown
        self._isSlow = isDown
        return self.moveEntity()

    def upMoveSlowly(self, isDown):
        self._up = isDown
        self._isSlow = isDown
        return self.moveEntity()

    def downMoveSlowly(self, isDown):
        self._down = isDown
        self._isSlow = isDown
        return self.moveEntity()

    def moveEntity(self):
        if not gameglobal.rds.configData.get('enableKeyBoardMoveFurniture', True):
            return False
        if not self.editMode:
            return False
        if not self.selectedEnt:
            return False
        player = BigWorld.player()
        if not self.isRightPos:
            player.showGameMsg(GMDD.data.FURNITURE_POS_NOT_VALID, ())
            return False
        self._moveEntity()
        return True

    def _moveEntity(self):
        if not self._left and not self._right and not self._up and not self._down:
            if self.isRightPos:
                self.syncEntity()
            return
        if not self.selectedEnt or not self.selectedEnt.inWorld:
            return
        if self.moveHandle:
            BigWorld.cancelCallback(self.moveHandle)
        if self.updateMouseHandle:
            BigWorld.cancelCallback(self.updateMouseHandle)
            self.updateMouseHandle = None
        isSlow = self._isSlow
        cam = BigWorld.camera()
        direction = Math.Vector3(cam.direction)
        direction.y = 0
        direction.normalise()
        oldPos = self.selectedEnt.position
        newPos = Math.Vector3(oldPos)
        ratio = 0.1 if isSlow else 1
        disVector = MOVE_DISTANCE * direction * ratio
        if self._up:
            newPos += disVector
        elif self._down:
            newPos -= disVector
        elif self._left or self._right:
            m = Math.Matrix()
            m.setRotateY(math.pi * 0.5)
            disVector = m.applyPoint(disVector)
            if self._right:
                newPos += disVector
            else:
                newPos -= disVector
        self.selectedEnt.setCollide(False)
        p = BigWorld.player()
        isValidPos = False
        if formula.spaceInHomeRoom(p.spaceNo) and self.selectedEnt.model:
            collidePoint = BigWorld.collide(p.spaceID, (oldPos.x, oldPos.y, oldPos.z), (newPos.x, newPos.y, newPos.z))
            modelHeight = self.selectedEnt.model.height
            collidePoint1 = BigWorld.collide(p.spaceID, (oldPos.x, oldPos.y + modelHeight, oldPos.z), (newPos.x, newPos.y + modelHeight, newPos.z))
            if not collidePoint or not collidePoint1:
                isValidPos = self.checkEntPosValid(self.selectedEnt, newPos)
        else:
            isValidPos = self.checkEntPosValid(self.selectedEnt, newPos)
        if isValidPos:
            self._updateMousePosition(newPos)
        self.moveHandle = BigWorld.callback(0.05, self._moveEntity)

    def lvUpFittingRoom(self):
        player = BigWorld.player()
        newLv = player.myHome.fittingRoomLv
        oldLv = newLv - 1
        if oldLv > 0:
            updateInfo = [[],
             [],
             [],
             []]
            for key, item in self.bwInfoMap.iteritems():
                position = item.position
                if player.inHomeFittingRoom(position, oldLv):
                    newPosition = player.transferFittingRoomValidArea(position, self.ownerGbID)
                    updateInfo[0].append(key)
                    updateInfo[1].append(newPosition)
                    updateInfo[2].append(item.direction)
                    updateInfo[3].append(item.parentUUID)

            self.batchSaveData = [[], [], updateInfo]
            self.batchSave(False, True)


def testAddCube(page, pos, num):
    import random
    p = BigWorld.player()
    sResKinds = [const.RES_KIND_INV] * num
    sInvPages = [page] * num
    sInvPos = [pos] * num
    pos = p.position
    sPosList = []
    for i in xrange(0, num):
        sPosList.append((pos.x + random.uniform(-2, 2), pos.y + random.uniform(-2, 2), pos.z + random.uniform(-2, 2)))

    sDirList = [(0, 0, 0)] * num
    sParentList = [''] * num
    p.cell.alterRoomFurniture(sResKinds, sInvPages, sInvPos, sPosList, sDirList, sParentList, [], '')
