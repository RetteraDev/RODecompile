#Embedded file name: I:/bag/tmp/tw2/res/entities\client\guis/loginScene.o
import math
import copy
import BigWorld
import ResMgr
import Sound
import Math
from Scaleform import GfxValue
import C_ui
import gameglobal
import gametypes
import gamelog
import keys
import const
import utils
import commcalc
import clientcom
from guis import ui
from callbackHelper import Functor
from appearance import Appearance
from physique import Physique
from guis import uiConst
from guis import cursor
from helpers import cameraControl as CC
from helpers import charRes
from helpers import tintalt
from helpers import modelServer
from helpers import preload
from helpers import black
from helpers import capturePhoto
from appSetting import setShaderIndex
from appSetting import Obj
from sfx import cameraEffect
from sfx import sfx
from cdata import suit_data as SD
from data import char_show_data as CSD
from data import offline_char_show_data as OCSD
from data import equip_data as ED
from data import sys_config_data as SCD
import miniclient
LOGINSCENENAME = 'xrjm_new'
LOGINSCENENAME_OLD = 'dljm_n'
LOGINSCENENAME_NEW = 'dljm_619'

def getCharShowData():
    if hasattr(gameglobal.rds, 'applyOfflineCharShowData') and gameglobal.rds.applyOfflineCharShowData:
        return OCSD.data
    return CSD.data


class LoginSceneEffect(object):

    def __init__(self):
        self.attachFx = {}
        self.effectFade = SCD.data.get('INTRO_PART_EFFECT_FADE', 0.1)
        self.attachModel = None

    def addModel(self, ent):
        if not self.attachModel:
            self.attachModel = BigWorld.Model('char/10000/intro/black/black.model')
            ent.addModel(self.attachModel)
            self.attachModel.position = (-168.378, 53.23, -69.077)
            self.attachModel.yaw = -1.57

    def addEffect(self, ent):
        entFxs = self.attachFx.get(ent.school, [])
        if entFxs:
            return
        effects = SCD.data.get('INTRO_PART_EFFECT', {}).get(ent.school, [])
        for effect in effects:
            fxs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (gameglobal.EFFECT_HIGH,
             gameglobal.EFF_PLAYER_SKILL_PRIORITY,
             ent.model,
             effect,
             sfx.EFFECT_UNLIMIT))
            if fxs:
                self.attachFx.setdefault(ent.school, [])
                self.attachFx[ent.school].extend(fxs)
                for fx in fxs:
                    BigWorld.callback(0.5, Functor(fx.playRate, 0, self.effectFade))

        if getattr(gameglobal.rds, 'applyOfflineCharShowData', False):
            self.addModel(ent)

    def removeEffect(self, ent):
        entFxs = self.attachFx.get(ent.school, [])
        if self.attachFx.has_key(ent.school):
            entFxs = self.attachFx.pop(ent.school)
            if entFxs:
                for fx in entFxs:
                    fx.playRate(1)
                    fx.stop()

    def addSceneEffect(self):
        self.attachFx.setdefault(0, [])
        effectInfo = SCD.data.get('SCENE_PART_EFFECT', {})
        for effectInfo in effectInfo.values():
            effects = effectInfo.get('effect')
            position = effectInfo.get('position')
            direction = effectInfo.get('direction')
            sizeScale = effectInfo.get('scale')
            for effect in effects:
                fxs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_INPOS, [gameglobal.EFFECT_HIGH,
                 gameglobal.EFF_DEFAULT_PRIORITY,
                 None,
                 effect,
                 sfx.EFFECT_UNLIMIT,
                 position,
                 direction[0],
                 direction[2],
                 direction[1],
                 sfx.KEEPEFFECTTIME])
                if fxs:
                    self.attachFx[0].extend(fxs)
                    for fx in fxs:
                        fx.scale(*sizeScale)
                        BigWorld.callback(0.5, Functor(fx.playRate, 0, self.effectFade))

    def focusEffect(self, ent, enter = True):
        rate = 1.0 if enter else 0
        entFxs = self.attachFx.get(ent.school, [])
        sceneFxs = self.attachFx.get(0, [])
        for fx in entFxs + sceneFxs:
            fx.playRate(rate, self.effectFade)

    def removeAllEffect(self):
        for effectId in self.attachFx.keys():
            fxs = self.attachFx[effectId]
            for fx in fxs:
                if fx:
                    fx.stop()

        self.attachFx = {}


class LoginScene(object):
    PATH = 'gui/loginScene/'
    STAGE_CHARACTER_CREATE = 1
    STAGE_CHARACTER_SELECT_ZERO = 1.5
    STAGE_CHARACTER_SELECT_ONE = 2
    STAGE_CHARACTER_SELECT_TWO = 2.5
    STAGE_CHARACTER_DETAIL_ADJUST = 3
    STAGE_CHARACTER_BODYTYPE = 4
    STAGE_CHARACTER_AVATARCONFIG = 5
    STAGE_CHARACTER_AVATARCONFIG_2 = 6
    STAGE_CHARACTER_CONTROL = 7
    STAGE_CHARACTER_SEX = 8
    STAGE_CHARACTER_AVATARCONFIG_2_SUB = 9
    STAGE_CHARACTER_SCHOOL = 10
    STAGE_CHARACTER_SCHOOL_AVATARCONFIG = 11
    ALL_LOGINMODEL_POSITION = (-168.378, 53.23, -69.077)
    SELECT_STAGE_CAMERA_YAW = 0.5
    SELECT_STAGE_CAMERA_PITCH = 0.0
    CAMERA_INIT_POSITION = (-107.3, 96.8, -100.2)
    CAMERA_INIT_YAW = 0.5
    CAMERA_INIT_PITCH = 0
    PLAYER_POSITION = (-107.3, 96.8, -100.2)
    LOGINENTITY_POSITION = (-112.866, 129.48, -108.692299)
    PLAYER_YAW = 3.68
    LOGINMODEL_POSITION = (-107.3, 96.8, -100.2)
    SCENE_POSITION = [[(-111.05, 133.15, -99.2),
      (0.75, 0.25, -1),
      0.45,
      'dljm01'],
     [(-113.099998, 123.7, -137.6),
      (0.209492, 0.222187, -0.952232),
      0.45,
      'dljm02'],
     [(-16.4494, 0.977, 32.1957),
      (-0.945994, 0.081258, -0.313586),
      0.969,
      'dljm01'],
     [(5615.0, 53.899, -1494.9996),
      (-0.484, -0.08, -0.871),
      0.4,
      'dljm_619']]

    def __init__(self):
        self.spaceID = None
        self.spaceMapping = None
        self.playerId = None
        self.player = None
        if not gameglobal.rds.enableBinkLogoCG:
            self.spaceName = LOGINSCENENAME_NEW
        else:
            self.spaceName = LOGINSCENENAME
        self.stage = self.STAGE_CHARACTER_CREATE
        self.loginModel = None
        self.selectSchool = const.SCHOOL_SHENTANG
        self.selectGender = const.SEX_MALE
        self.selectBodyType = const.BODY_TYPE_5
        self.bodyIdx = 0
        self.isZoom = uiConst.ZOOMOUT
        self.oldX = 640
        self.heightConfigs = {}
        self.headHeight = 0
        self.DELTA_T = 0.2
        dataInfo = ResMgr.openSection(self.PATH + 'height.track')
        if dataInfo:
            for key in dataInfo.keys():
                if key == 'head':
                    self.headHeight = dataInfo[key].asFloat
                    continue
                heightData = [ float(x) for x in dataInfo[key].asString.split(',') ]
                if heightData:
                    self.heightConfigs[int(key)] = heightData

        self.multiModels = []
        self.chooseModel = None
        self.trackNo = 0
        self.loadingNum = 0
        self.oldYaw = None
        self.cc = None
        self.tc = None
        self.dotaTC = None
        self.cursorCameraSatge = -1
        self.lookModel = None
        self.oldFov = None
        self.oldNearPlane = None
        self.effectManager = LoginSceneEffect()
        self.focusPositionMap = gameglobal.OLD_XRJM_FOCUS_MAP
        self.cameraSound = 0
        self.callbackHandle = None
        self.cameraEffect = []
        self.editMode = 0
        self.editDist = 0.25
        self.oldCamera = None

    def setEditMode(self, value):
        self.editMode = value

    def getCameraInfo(self):
        if CC.TC and hasattr(CC.TC, 'cameraDHProvider'):
            value = CC.TC.cameraDHProvider.value
            cameraInfo = [value[3], value[1], value[0]]
            return cameraInfo

    def getModelYaw(self):
        model = self.lookModel if self.lookModel else self.player.model
        if model:
            return model.yaw
        return 0

    def saveCameraAndYaw(self):
        model = self.lookModel if self.lookModel else self.player.model
        if model:
            cameraInfo = self.getCameraInfo()
            yaw = self.getModelYaw()
            path = model.sources[0]
            modelId = path.split('/')[1]
            dataSect = ResMgr.openSection(capturePhoto.FITTING_PHOTO_PATH, True)
            if modelId not in dataSect.keys():
                sect = dataSect.createSection(modelId)
            else:
                sect = dataSect.openSection(modelId)
            sect.writeVector3('camera', Math.Vector3(cameraInfo))
            sect.writeFloat('yaw', yaw)
            dataSect.save()

    def loadCameraAndYaw(self, modelId):
        dataSect = capturePhoto.photoDict[capturePhoto.FITTING_PHOTO_PATH]
        dataSect = dataSect.openSection(modelId) if dataSect else None
        if dataSect:
            cameraInfo = dataSect.readVector3('camera')
            yaw = dataSect.readFloat('yaw')
            return (cameraInfo, yaw)
        return (None, 0)

    def loadingInc(self):
        self.loadingNum = 1
        gameglobal.rds.ui.roleLoad.show(True)

    def loadingDec(self):
        self.loadingNum -= 1
        if self.loadingNum <= 0:
            gameglobal.rds.ui.roleLoad.show(False)

    def _createPlayerEntity(self, school, aspect, physique, signal = 0, avatarConfig = '', availableMorpher = {}):
        if not self.spaceID:
            return
        self.loadingInc()
        if not gameglobal.rds.enableBinkLogoCG:
            BigWorld.setColorGrading('', 1)
        else:
            BigWorld.setColorGrading('', 1)
        gamelog.debug('jorsef: _createPlayerEntity', school, aspect, physique, signal, avatarConfig)
        if not self.player:
            self.playerId = BigWorld.createEntity('Avatar', self.spaceID, 0, self.PLAYER_POSITION, (0, 0, self.PLAYER_YAW), {'school': school,
             'pubAspect': aspect,
             'physique': physique,
             'signal': signal,
             'pubAvatarConfig': avatarConfig})
            self.player = BigWorld.entity(self.playerId)
            self.player.canSelectWhenHide = False
            self.player.availableMorpher = availableMorpher
        else:
            if hasattr(self.player, 'allModels'):
                tintalt.ta_reset(self.player.allModels)
            self.player.allModels = []
            self.player.model.visible = False
            self.player.school = school
            self.player.aspect = aspect
            self.player.physique = physique
            self.player.aspectOld = copy.deepcopy(aspect)
            self.player.physiqueOld = copy.deepcopy(physique)
            self.player.signal = signal
            self.player.showBackWaist = commcalc.getSingleBit(signal, gametypes.SIGNAL_SHOW_BACK)
            self.player.avatarConfig = avatarConfig
            self.player.modelServer.leftWeaponModel.release()
            self.player.modelServer.rightWeaponModel.release()
            self.player.modelServer.headdressRight.release()
            self.player.modelServer.headdressLeft.release()
            self.player.modelServer.facewear.release()
            self.player.modelServer.waistwear.release()
            self.player.modelServer.backwear.release()
            self.player.modelServer.tailwear.release()
            self.player.modelServer.chestwear.release()
            self.player.modelServer.earwear.release()
            self.player.modelServer.bodyUpdateStatus = modelServer.BODY_UPDATE_STATUS_NORMAL
            self.player.modelServer.bodyUpdate()
            self.player.modelServer.weaponUpdate()
            self.player.modelServer.wearUpdate()
            self.player.availableMorpher = availableMorpher
            if isinstance(self.player.filter, BigWorld.ClientFilter):
                self.player.filter.yaw = self.PLAYER_YAW

    def initLoginModels(self, visibility = gameglobal.OPACITY_HIDE):
        if not self.spaceID:
            return
        csd = getCharShowData()
        visible = visibility
        for school, bodyData in csd.iteritems():
            if school == const.SCHOOL_YECHA and not clientcom.enableNewSchoolYeCha():
                continue
            visible = visibility
            for i, data in enumerate(bodyData):
                if data.get('showModel', 0):
                    modelPlace = data['showPlacement']
                    if clientcom.enableNewSchoolYeCha():
                        modelPlace = gameglobal.NEW_XRJM_SHOW_POSOITON[school]
                    else:
                        modelPlace = gameglobal.OLD_XRJM_SHOW_POSOITON[school]
                    self.loadingInc()
                    entityId = BigWorld.createEntity('LoginModel', self.spaceID, 0, modelPlace[0], (0, 0, modelPlace[1]), {'school': school,
                     'gender': data.get('sex', const.SEX_MALE),
                     'bodyType': data.get('bodyType', const.BODY_TYPE_5),
                     'bodyIdx': i,
                     'visibility': visible,
                     'originalPos': modelPlace[0],
                     'originalYaw': modelPlace[1]})
                    ent = BigWorld.entity(entityId)
                    self.multiModels.append(ent)

        self.effectManager.addSceneEffect()

    def showLoginModel(self, ent):
        if hasattr(ent.filter, 'position'):
            ent.filter.position = ent.originalPos
            ent.filter.yaw = ent.originalYaw
            ent.refreshOpacity(gameglobal.OPACITY_FULL)
        if hasattr(ent.model, 'blender'):
            ent.model.blender.dest(255)
        if self.inSelectZeroStage():
            ent.tryAction(gameglobal.STAGE_ZERO_SHOW_ACTION)
        elif self.inSelectOneStage():
            ent.tryAction(gameglobal.STAGE_ZERA_FOCUS_ACTION)
        self.effectManager.addEffect(ent)

    def showLoginModels(self):
        for ent in self.multiModels:
            self.showLoginModel(ent)

    def hideLoginModels(self, excludeEnt = None):
        for ent in self.multiModels:
            if ent != excludeEnt:
                ent.refreshOpacity(gameglobal.OPACITY_HIDE)

    def clearLoginModels(self):
        while self.multiModels:
            ent = self.multiModels.pop()
            if ent and ent.inWorld:
                BigWorld.destroyEntity(ent.id)

    def moveLoginModel(self):
        if self.loginModel:
            self.loginModel.refreshOpacity(gameglobal.OPACITY_FULL)
            self.selectSchool = self.loginModel.school
            self.selectGender = self.loginModel.gender
            self.selectBodyType = self.loginModel.bodyType
            self.bodyIdx = self.loginModel.bodyIdx
            csd = self.getCharShowData(self.selectSchool, self.selectGender, self.selectBodyType)
            modelPlace = csd['placement']
            self.moveToDestination(0, 'select_%d_%d.track' % (self.selectGender, self.selectBodyType))
            self.loginModel.filter.position = modelPlace[0]
            self.loginModel.filter.yaw = modelPlace[1]
            self.loginModel.showWeapon(True)

    def searchLoginModel(self, school, gender, bodyType):
        if self.multiModels:
            for ent in self.multiModels:
                if ent.school == school and ent.gender == gender and ent.bodyType == bodyType:
                    self.loginModel = ent
                    self.chooseModel = ent
                    return self.loginModel

    def searchLoginModelByEntity(self, loginModel):
        if loginModel and self.multiModels:
            if loginModel not in self.multiModels:
                for ent in self.multiModels:
                    if ent.school == loginModel.school:
                        return ent

            else:
                return loginModel

    def arrangeLoginModels(self):
        BigWorld.target.source = BigWorld.camera().matrix
        BigWorld.target.updateBBoxFreq = 5
        BigWorld.target.caps(keys.CAP_CAN_USE)
        BigWorld.target.exclude = None
        BigWorld.enableOfflineFocus(True)
        self.lookAtStage(1)
        inWorld = True
        for ent in self.multiModels:
            if not ent or not ent.inWorld:
                inWorld = False
                break

        if not self.multiModels:
            inWorld = False
        if not inWorld:
            self.multiModels = []
            self.initLoginModels(gameglobal.OPACITY_FULL)
        else:
            self.showLoginModels()

    def createLoginModel(self, school, gender, bodyType, bodyIdx = 0, applyAvatarConfig = False):
        if not self.spaceID:
            return
        csd = self.getCharShowData(school, gender, bodyType)
        if not csd:
            return
        modelPlace = csd['placement']
        self.moveToDestination(0, 'select_%d_%d.track' % (gender, bodyType))
        self.loadingInc()
        entityId = BigWorld.createEntity('LoginModel', self.spaceID, 0, modelPlace[0], (0, 0, modelPlace[1]), {'school': school,
         'gender': gender,
         'bodyType': bodyType,
         'bodyIdx': bodyIdx,
         'visibility': gameglobal.OPACITY_FULL,
         'applyAvatarConfig': applyAvatarConfig})
        self.loginModel = BigWorld.entity(entityId)
        self.selectSchool = school
        self.selectGender = gender
        self.selectBodyType = bodyType
        self.bodyIdx = bodyIdx

    def getCharShowData(self, school, gender, bodyType):
        bodyData = getCharShowData().get(school)
        if bodyData:
            for data in bodyData:
                if data['sex'] == gender and data['bodyType'] == bodyType:
                    return data

    def createPlayer(self, school, gender, bodyType, isNew = False, hair = 0, suitId = 0, avatarConfig = '', availableMorpher = {}):
        gamelog.debug('jorsef: createPlayer', school, gender, bodyType, isNew, self.player)
        if isNew:
            self.clearLoginModel()
        aspect = Appearance({})
        isFashion = utils.setDefaultSuit(suitId, school, aspect, SD, ED)
        signal = commcalc.setSingleBit(0, gametypes.SIGNAL_SHOW_FASHION, isFashion)
        physique = Physique({'hair': hair})
        physique.school = school
        physique.sex = gender
        physique.bodyType = bodyType
        if availableMorpher == None:
            availableMorpher = {}
        self._createPlayerEntity(school, aspect, physique, signal, avatarConfig, availableMorpher)
        self.isZoom = uiConst.ZOOMOUT

    def clearPlayer(self):
        if self.player and self.player.inWorld:
            BigWorld.destroyEntity(self.playerId)
            self.playerId = None
        self.player = None

    def clearLoginModel(self):
        if self.loginModel and self.loginModel.inWorld:
            if self.loginModel in self.multiModels:
                self.loginModel.showWeapon(False)
                self.loginModel.filter.position = self.loginModel.originalPos
                self.loginModel.filter.yaw = self.loginModel.originalYaw
                self.loginModel.refreshOpacity(gameglobal.OPACITY_HIDE)
            else:
                BigWorld.destroyEntity(self.loginModel.id)
        self.loginModel = None

    def hideLoginModel(self):
        if self.loginModel:
            self.loginModel.refreshOpacity(gameglobal.OPACITY_HIDE)

    def preLoadData(self):
        self.loadSpace()
        self.initCamera()

    def loadOfflineSpace(self):
        if self.spaceID == None:
            spaceID = BigWorld.createSpace()
            self.spaceMapping = BigWorld.addSpaceGeometryMapping(spaceID, None, 'universes/eg/' + LOGINSCENENAME)
            gameglobal.rds.clientSpaceMapping = self.spaceMapping
            self.spaceID = spaceID
            BigWorld.cameraSpaceID(self.spaceID)

    def loadSpace(self, school = const.SCHOOL_SHENTANG):
        if gameglobal.rds.GameState == gametypes.GS_START:
            self.spaceName = LOGINSCENENAME_NEW
        elif gameglobal.rds.GameState == gametypes.GS_LOGIN:
            self.spaceName = LOGINSCENENAME
        if hasattr(gameglobal.rds, 'transServerInfo') and gameglobal.rds.transServerInfo:
            return
        if self.spaceID == None:
            BigWorld.clearAllSpaces()
            spaceID = BigWorld.createSpace()
            if not gameglobal.rds.enableBinkLogoCG:
                Sound.changeZone(gameglobal.NEW_LOGIN_MUSIC, '')
            self.spaceMapping = BigWorld.addSpaceGeometryMapping(spaceID, None, 'universes/eg/' + self.spaceName)
            gameglobal.rds.clientSpaceMapping = self.spaceMapping
            self.spaceID = spaceID
            BigWorld.cameraSpaceID(self.spaceID)
            if hasattr(BigWorld, 'enableVisualStreaming'):
                BigWorld.enableVisualStreaming(False)
            position = Math.Vector3(-86, 64, -142)
            if not BigWorld.player() or gameglobal.rds.GameState == gametypes.GS_START:
                self.initCameraData()
        BigWorld.enableAutoLod(False)
        gamelog.debug('b.e.: loadSpace', self.spaceID)
        BigWorld.renderFeatures('deferred', True)
        BigWorld.renderFeatures('vsm', False)
        BigWorld.renderFeatures('hdr', True)
        BigWorld.renderFeatures('hiQuality', True)
        BigWorld.renderFeatures('plsm', True)
        BigWorld.enableVSync(True)
        BigWorld.simpleShaderDistance(gameglobal.LARGE_SIMPLE_SHADER_DISTANCE)
        if hasattr(BigWorld, 'smallSimpleShaderDistance'):
            BigWorld.smallSimpleShaderDistance(gameglobal.LARGE_SIMPLE_SHADER_DISTANCE)
        BigWorld.enableTerrainLOD(False)
        BigWorld.enableBkgAnimLoad(False)
        BigWorld.setInnerScreenSize(1.0)
        if hasattr(BigWorld, 'setSharpen'):
            BigWorld.setSharpen(0, 0)
        if hasattr(BigWorld, 'forceSkipMipMap'):
            BigWorld.forceSkipMipMap(-1)
        if hasattr(BigWorld, 'setAnimationLevel'):
            BigWorld.setAnimationLevel(1)
        if hasattr(BigWorld, 'skeletonRecalcInterval'):
            BigWorld.skeletonRecalcInterval(0.0)
        if hasattr(BigWorld, 'enableMultiThreadAnim'):
            BigWorld.enableMultiThreadAnim(False)
        if hasattr(BigWorld, 'textureLODSizeLimit'):
            if Obj._AppSetting__sect:
                dataSection = Obj._AppSetting__sect.openSection('renderer/textureLimit')
                if dataSection:
                    for key in dataSection.keys():
                        if key != 'char':
                            size = dataSection[key].asInt
                            BigWorld.textureLODSizeLimit(key, size)
                        else:
                            BigWorld.textureLODSizeLimit('char', 150)

        if hasattr(BigWorld, 'modelLODScale'):
            BigWorld.modelLODScale(1.0)
        BigWorld.setVideoParams({'SSAO': 0})
        BigWorld.enableSkipSkeletonUpdate(False)
        setShaderIndex(0, False)
        refPosMatrix = Math.Matrix()
        refPosMatrix.setTranslate(self.PLAYER_POSITION)
        BigWorld.setPlayerPosRef(refPosMatrix)

    def createLogonEntity(self):
        self.initCameraData()
        BigWorld.cameraSpaceID(self.spaceID)
        BigWorld.worldDrawEnabled(True)

    def clearSpaceAndPlayer(self):
        if self.playerId:
            BigWorld.destroyEntity(self.playerId)
            self.playerId = None
        self.clearSpace()

    def clearSpace(self):
        if self.spaceID:
            BigWorld.cameraSpaceID()
            gamelog.debug('b.e.: clearSpace', self.spaceID, self.spaceMapping)
            BigWorld.delSpaceGeometryMapping(self.spaceID, self.spaceMapping)
            BigWorld.clearSpace(self.spaceID)
            BigWorld.releaseSpace(self.spaceID)
            BigWorld.enableTerrainLOD(True)
            BigWorld.simpleShaderDistance(gameglobal.NORMAL_SIMPLE_SHADER_DISTANCE)
            if hasattr(BigWorld, 'smallSimpleShaderDistance'):
                BigWorld.smallSimpleShaderDistance(gameglobal.NORMAL_SIMPLE_SHADER_DISTANCE)
            if hasattr(BigWorld, 'closeAvatarShadow'):
                BigWorld.closeAvatarShadow()
            if hasattr(BigWorld, 'enableMultiThreadAnim'):
                BigWorld.enableMultiThreadAnim(True)
            if hasattr(BigWorld, 'enableVisualStreaming'):
                BigWorld.enableVisualStreaming(True)
            BigWorld.enableSkipSkeletonUpdate(True)
            BigWorld.setPlayerPosRef(None)
            self.spaceID = None
            self.spaceMapping = None

    def clearScene(self):
        self.clearPlayer()
        self.clearLoginModels()
        self.clearLoginModel()
        self.clearSpace()
        self.chooseModel = None
        preload.freeTempPreload()
        gameglobal.rds.ui.roleLoad.hide()
        self.effectManager.removeAllEffect()
        self.lookAtStage(False)
        CC.CC = None
        CC.TC = None

    def placePlayer(self, characterDetail):
        gamelog.debug('b.e.:placePlayer:', self.player)
        miniclient.setCharLevel(characterDetail['lv'])
        school = characterDetail['school']
        aspect = characterDetail['appearance']
        physique = characterDetail['physique']
        signal = characterDetail['signal']
        avatarConfig = characterDetail['avatarConfig']
        self._createPlayerEntity(school, aspect, physique, signal, avatarConfig)

    def zoomIn(self):
        if self.trackNo < 2 and self.player and self.player.firstFetchFinished:
            self.trackNo += 1
            self.moveToDestination(self.trackNo, 'detailAdjust_%d_%d.track' % (self.player.physique.sex, self.player.physique.bodyType))

    def zoomOut(self):
        if self.trackNo > 0 and self.trackNo <= 2 and self.player and self.player.firstFetchFinished:
            self.trackNo -= 1
            self.moveToDestination(self.trackNo, 'detailAdjust_%d_%d.track' % (self.player.physique.sex, self.player.physique.bodyType))

    def zoomTo(self, trackNo):
        if trackNo >= 0 and trackNo <= 3:
            self.trackNo = trackNo
            self.moveToDestination(self.trackNo, 'detailAdjust_%d_%d.track' % (self.player.physique.sex, self.player.physique.bodyType))

    def turnLeft(self):
        if self.player == None or not self.player.inWorld:
            return
        if hasattr(self.player, 'am'):
            self.player.am.matcherCoupled = False
        self.player.filter.yaw += 0.05
        if gameglobal.rds.ui.characterDetailAdjust.isRotate:
            BigWorld.callback(0, self.turningLeft)

    def turningLeft(self):
        if self.player == None or not self.player.inWorld:
            return
        self.player.filter.yaw += 0.05
        if gameglobal.rds.ui.characterDetailAdjust.isRotate:
            BigWorld.callback(0, self.turningLeft)

    def turnRight(self):
        if self.player == None or not self.player.inWorld:
            return
        if hasattr(self.player, 'am'):
            self.player.am.matcherCoupled = False
        self.player.filter.yaw -= 0.05
        if gameglobal.rds.ui.characterDetailAdjust.isRotate:
            BigWorld.callback(0, self.turningRight)

    def turningRight(self):
        if self.player == None or not self.player.inWorld:
            return
        self.player.filter.yaw -= 0.05
        if gameglobal.rds.ui.characterDetailAdjust.isRotate:
            BigWorld.callback(0, self.turningRight)

    def loadWidgets(self, widgetsList):
        if widgetsList == None:
            gamelog.error('hjx loadWidgets widgetsList is None')
            return
        for item in widgetsList:
            gameglobal.rds.ui.loadWidget(item)

    def unloadWidgets(self, widgetsList):
        if widgetsList == None:
            gamelog.error('hjx unloadWidgets widgetsList is None')
            return
        for item in widgetsList:
            gameglobal.rds.ui.movie.invoke(('_root.unloadWidget', GfxValue(item)))

    def setCameraToEntity(self, npcId, dis = 2.5, farPlane = 100, fov = 0.7, modelHeight = 0.5, offX = 0):
        if not self.oldCamera:
            self.oldCamera = BigWorld.camera()
        e = BigWorld.entities.get(npcId)
        height = e.model.height * modelHeight
        yaw = e.model.yaw
        pos = e.model.position + Math.Vector3(math.sin(yaw) * dis, height, math.cos(yaw) * dis) + (offX, 0, 0)
        dir = Math.Vector3(math.sin(yaw + math.pi), 0, math.cos(yaw + math.pi))
        dir.normalise()
        m = Math.Matrix()
        m.lookAt(pos, dir, (0, 1, 0))
        if not self.dotaTC:
            self.dotaTC = BigWorld.TrackCamera()
            self.dotaTC.set(m)
        BigWorld.camera(self.dotaTC)
        self.dotaTC.newTrack()
        quad = cameraEffect.eulerAngleToQuad(m.yaw, m.pitch, m.roll)
        fov = BigWorld.projection().fov
        keyData = (pos[0],
         pos[1],
         pos[2],
         quad[0],
         quad[1],
         quad[2],
         quad[3],
         fov,
         0.5,
         True,
         0,
         0,
         0,
         0)
        self.dotaTC.pushKey(*keyData)
        self.dotaTC.showTrack = False
        self.dotaTC.setStopCallback(self.trackCallback)
        self.dotaTC.play(0)

    def trackCallback(self, param):
        self.dotaTC.newTrack()
        self.dotaTC.deleteKey(0)

    def resetOldCamera(self):
        if self.oldCamera:
            BigWorld.camera(self.oldCamera)
            self.oldCamera = None

    def initCamera(self):
        if self.spaceID:
            BigWorld.cameraSpaceID(self.spaceID)
            self.setCursorCamera()

    def initCameraData(self):
        cam = gameglobal.rds.cam.cc
        cam.reverseView = False
        cam.cameraDHProvider = None
        BigWorld.enableClearCameraSpace(True)
        BigWorld.enableCameraChange(True)
        cam.set(BigWorld.camera().matrix)
        BigWorld.camera(cam)
        BigWorld.cameraBindPlayer(True)
        index = gameglobal.rds.loginIndex
        scenePos = self.SCENE_POSITION[index]
        cam.destPosition = scenePos[0]
        cam.destDirection = scenePos[1]
        cam.needfixCamera = True
        BigWorld.projection().fov = scenePos[2]
        BigWorld.setZonePriority(scenePos[3], gameglobal.LOGINZONE_PRIO)
        BigWorld.setZonePriority('hand', -gameglobal.LOGINZONE_PRIO)
        if index == 2:
            BigWorld.setDepthOfField(True, 1.7869, 1 / 3938.77, 1.0, 0.204, 0.204)
        elif index == 3:
            BigWorld.setTime(6.9)

    def setCursorCamera(self):
        BigWorld.dcursor().yaw = self.CAMERA_INIT_YAW
        BigWorld.dcursor().pitch = self.CAMERA_INIT_PITCH
        CC.initCC()
        cameraInfo = self.loadCameraKey(self.PATH + 'show.track', 0, 'CursorParam')
        matrix = Math.Matrix()
        matrix.setTranslate(self.CAMERA_INIT_POSITION)
        if cameraInfo:
            BigWorld.projection().fov = cameraInfo[-1]
            CC.playCC(0, cameraInfo, matrix, 0)

    def fixTrackCamera(self):
        currentCamera = BigWorld.camera()
        m = currentCamera.matrix
        CC.newTrack()
        CC.TC.set(m)

    def setDetailAdjustCamera(self, track, cameraInfo):
        if self.player == None:
            return
        modelId = charRes.transDummyBodyType(self.player.physique.sex, self.player.physique.bodyType, True)
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

    def loadCameraKey(self, trackName, key = 0, tag = 'Param'):
        gamelog.debug('b.e.:loadCameraKey', trackName, key)
        track = clientcom.loadCameraTrack(trackName)
        if track == None:
            if trackName.find('detailAdjust') >= 0:
                track = ResMgr.openSection(self.PATH + 'detailAdjust_1_3.track', False)
            elif trackName.find('select') >= 0:
                track = ResMgr.openSection(self.PATH + 'select_1_3.track', False)
            elif trackName.find('show') >= 0:
                track = ResMgr.openSection(self.PATH + 'show.track', False)
        if track == None:
            gamelog.error('hjx: Cannot open track ', trackName)
            return
        count = track.readInt('keyframes', 0)
        if key < 0 or key >= count:
            gamelog.error('hjx: Invalid key number', key)
            return
        item = track.openSection('key%i' % key)
        params = item.readString(tag)
        if len(params):
            cameraInfo = [ float(x) for x in params.split(',') ]
            if len(cameraInfo) > 9:
                cameraInfo[9] = int(cameraInfo[9])
            if key == 1 or key == 2:
                if trackName.find('detailAdjust_') >= 0:
                    return self.setDetailAdjustCamera(track, cameraInfo)
            return cameraInfo

    def deleteTrackcameraFrame(self, arg):
        CC.newTrack()
        CC.TC.deleteKey(0)

    def moveToDestination(self, key, track, t = 1):
        cameraInfo = self.loadCameraKey(self.PATH + track, key, 'CursorParam')
        if self.stage == self.STAGE_CHARACTER_CONTROL:
            matrix = self.lookModel.matrix
        else:
            originalPos = self.PLAYER_POSITION
            if self.inSelectStage() or self.inBodyTypeStage():
                originalPos = self.LOGINMODEL_POSITION
            matrix = Math.Matrix()
            matrix.setTranslate(originalPos)
        if cameraInfo:
            BigWorld.projection().fov = cameraInfo[-1]
            if self.stage != self.STAGE_CHARACTER_CONTROL:
                dc = BigWorld.dcursor()
                dc.yaw = self.SELECT_STAGE_CAMERA_YAW
                dc.pitch = self.SELECT_STAGE_CAMERA_PITCH
                if self.inSelectTwoStage() and self.loginModel:
                    data = self.getCharShowData(self.selectSchool, self.selectGender, self.selectBodyType)
                    dc.pitch = data.get('placementPitch', 0)
            if CC.TC and not isinstance(CC.TC, BigWorld.CursorCamera):
                CC.initCC()
            CC.playCC(self.DELTA_T, cameraInfo, matrix)
            if self.player and self.trackNo > 0:
                self.player.model.setModelNeedHide(False, 0.1)

    def __moveToDestination(self, key, track, t):
        self.trackNo = key
        parameter = self.loadCameraKey(self.PATH + track, key)
        if not parameter:
            return
        gamelog.debug('b.e.:moveToDestination', parameter, track)
        CC.newTrack()
        CC.TC.setKeytime(0, t)
        CC.pushKey(parameter)
        CC.play(endCallback=self.deleteTrackcameraFrame)
        if self.player and self.trackNo > 0:
            self.player.model.setModelNeedHide(False, 0.3)

    def initYaw(self, oldX):
        self.oldX = oldX
        if self.inSelectStage() or self.inBodyTypeStage():
            if self.loginModel:
                self.oldYaw = self.loginModel.filter.yaw
        elif self.lookModel:
            self.oldYaw = self.lookModel.yaw
        elif self.player and self.player.filter:
            self.oldYaw = self.player.filter.yaw

    def mouseRotate(self, x, y):
        width = -500.0
        value = x - self.oldX
        yaw = value * math.pi / width
        if self.oldYaw != None:
            if self.inSelectStage() or self.inBodyTypeStage():
                self.loginModel.filter.yaw = yaw + self.oldYaw
            elif self.lookModel:
                self.lookModel.yaw = yaw + self.oldYaw
            elif self.player:
                self.player.filter.yaw = yaw + self.oldYaw

    def handleKeyEvent(self, down, key, vk, mods):
        if self.editMode and CC.TC and hasattr(CC.TC, 'cameraDHProvider'):
            value = CC.TC.cameraDHProvider.value
            targetMatrix = CC.TC.target
            cameraInfo = [value[3], value[1], value[0]]
            if key in (keys.KEY_Q,
             keys.KEY_E,
             keys.KEY_W,
             keys.KEY_S):
                if key == keys.KEY_Q:
                    cameraInfo[1] += self.editDist
                if key == keys.KEY_E:
                    cameraInfo[1] -= self.editDist
                if key == keys.KEY_W:
                    cameraInfo[0] -= self.editDist
                if key == keys.KEY_S:
                    cameraInfo[0] += self.editDist
                CC.playCC(0.1, cameraInfo, targetMatrix)
                return True
        if self.inSelectZeroStage():
            if down:
                if key == keys.KEY_LEFTMOUSE:
                    self.enterCharacterSelectOne()
        if self.inSelectOneStage() or self.inSelectZeroStage():
            if key in (keys.KEY_RIGHTMOUSE, keys.KEY_LEFTMOUSE):
                BigWorld.dcursor().canRotate = down
                if down:
                    cursor.setOutAndSaveOldPos()
                    C_ui.cursor_show(False)
                else:
                    cursor.setInAndRestoreOldPos()
                    C_ui.cursor_show(True)
                return True
        if self.inCreateStage or self.inAvatarStage() or self.inSelectOneStage() or self.inSelectTwoStage() or self.inBodyTypeStage():
            if down and key in (keys.KEY_RIGHTMOUSE, keys.KEY_LEFTMOUSE):
                self.disableMouseMsgForUI(down)
                gameglobal.rds.ui.movie.invoke(('_root.setIsRotate', GfxValue(True)))
                return True
            if not down and key in (keys.KEY_RIGHTMOUSE, keys.KEY_LEFTMOUSE):
                self.disableMouseMsgForUI(down)
                gameglobal.rds.ui.movie.invoke(('_root.setIsRotate', GfxValue(False)))
                return True
        return False

    def disableMouseMsgForUI(self, disableMsg):
        C_ui.cursor_show(not disableMsg)

    def handleMouseEvent(self, dx, dy, dz):
        if self.inSelectZeroStage():
            if dz > 0:
                self.enterCharacterSelectOne()
        if self.inSelectOneStage():
            if dz < 0:
                self.leaveCharacterSelectOne()
        if self.inAvatarStage():
            if dz > 0:
                self.zoomIn()
            else:
                self.zoomOut()
            return True
        return False

    def leaveCharacterSelectOne(self):
        if self.callbackHandle:
            BigWorld.cancelCallback(self.callbackHandle)
            self.callbackHandle = None
        gameglobal.rds.ui.characterSelect.gotoJobSelectZero()
        self.setTaTint(False)
        self.stopChangeFov()
        self.lookAtLoginModel(None)
        self._stopCameraAction()
        self.clearLoginModel()
        self.arrangeLoginModels()

    def enterCharacterSelectOne(self):
        if self.chooseModel:
            self.loginModel = self.chooseModel
            self.selectSchool = self.loginModel.school
            self.selectGender = self.loginModel.gender
            self.selectBodyType = self.loginModel.bodyType
            self.loginModel.refreshOpacity(gameglobal.OPACITY_FULL)
            self.hideLoginModels(self.loginModel)
            gameglobal.rds.ui.characterSelect.gotoJobSelectOne()
            self.setTaTint(True)
            self.lookAtLoginModel(self.loginModel, False)
            self.loginModel.model.setModelNeedHide(False, 0.1)
            return
        if self.chooseModel:
            self.loginModel = self.chooseModel
            self.hideLoginModels()
            self.moveLoginModel()
            gameglobal.rds.ui.characterSelect.gotoJobSelectOne()
            if getattr(self.loginModel, 'firstFetchFinished', False):
                self.loginModel.playChooseSound()

    def startEnterCharacterSelectTwo(self):
        self.effectManager.removeEffect(self.loginModel)
        unloadWidgetsList = [uiConst.WIDGET_CHARACTER_SELECT_JOB_LIST, uiConst.WIDGET_CHARACTER_SELECT_JOB_DESC]
        gameglobal.rds.loginScene.unloadWidgets(unloadWidgetsList)
        BigWorld.setDepthOfField(False)
        self.removeCameraEffect()
        self.startChangeFov()
        self._playIntroAni(0, self._enterCharacterSelectTwo)

    def startChangeFov(self):
        projection = BigWorld.projection()
        if hasattr(projection, 'inputChangeFov'):
            config = ResMgr.openSection('%s/select_fov_%d.xml' % (self.PATH, self.selectSchool))
            if config:
                array = []
                for data in config.values():
                    time = data.readFloat('time', 0)
                    fov = data.readFloat('fovAngle', 0) / 180.0 * math.pi
                    array.append((time, fov))

                projection.inputChangeFov(array)
                projection.startChangeFov(0)

    def stopChangeFov(self):
        projection = BigWorld.projection()
        if hasattr(projection, 'inputChangeFov'):
            projection.inputChangeFov([])
            projection.startChangeFov(0)

    def returnCharacterSelectOne(self):
        BigWorld.setZonePriority('hand', -gameglobal.LOGINZONE_PRIO)
        newLoginModel = self.searchLoginModelByEntity(self.loginModel)
        if newLoginModel and self.loginModel != newLoginModel:
            self.clearLoginModel()
            self.loginModel = newLoginModel
            self.selectSchool = self.loginModel.school
            self.selectGender = self.loginModel.gender
            self.selectBodyType = self.loginModel.bodyType
        self.showLoginModel(self.loginModel)
        self.effectManager.addEffect(self.loginModel)
        self.callbackHandle = BigWorld.callback(0.2, Functor(self.lookAtLoginModel, self.loginModel))

    def _playIntroAni(self, stage, callback = None):
        if self.loginModel:
            modelAction = gameglobal.INTRO_PART_ONE_MODEL[stage]
            cameraAction = gameglobal.INTRO_PART_ONE_CAMERA[self.loginModel.school][stage]
            cueData = ':'.join((str(gameglobal.CAMERA_MODEL), 'camBone', cameraAction))
            cameraEffect.startAnimateCamera(cueData, self.loginModel, callback)
            self.loginModel.tryAction(modelAction)

    def _enterCharacterSelectTwo(self):
        if self.inSelectOneStage():
            if self.loginModel:
                self.moveLoginModel()
                BigWorld.setZonePriority('hand', gameglobal.LOGINZONE_PRIO)
                BigWorld.callback(0, Functor(self._playIntroAni, 1, self._afterEnterCharacterSelectTwo))

    def _afterEnterCharacterSelectTwo(self):
        if self.inSelectOneStage():
            gameglobal.rds.ui.characterSelect.gotoJobSelectTwo()
            if self.loginModel:
                self.loginModel.tryAction(gameglobal.STAGE_ONE_SHOW_ACTION)

    def _stopCameraAction(self):
        if cameraEffect.cameraModel and cameraEffect.cameraModel.inWorld:
            actQueue = cameraEffect.cameraModel.queue
            for i in actQueue:
                aq = cameraEffect.cameraModel.action(i)
                aq.stop()

    def _directlyEnterCharacterSelectTwo(self):
        if self.loginModel:
            self.stopChangeFov()
            self.moveLoginModel()
            BigWorld.setZonePriority('hand', gameglobal.LOGINZONE_PRIO)
            self._afterEnterCharacterSelectTwo()
            self._stopCameraAction()
            gender = self.loginModel.gender
            bodyType = self.loginModel.bodyType
            gameglobal.rds.loginScene.moveToDestination(0, 'select_%d_%d.track' % (gender, bodyType))

    def getPlayerHeight(self):
        model = self.lookModel if self.lookModel else self.player.model
        height = max((model.node('biped Head').position - model.node('biped R Toe0').position).y, (model.node('biped Head').position - model.node('biped L Toe0').position).y) + (self.headHeight if self.player else 0)
        return height

    def recordCC(self):
        playerHeight = self.getPlayerHeight()
        CC.newTrack()
        CC.record()
        gamelog.debug('b.e.: recordCC', CC.TC.getKey(1), playerHeight)

    def inCreateStage(self):
        return self.stage == self.STAGE_CHARACTER_CREATE

    def inSelectZeroStage(self):
        return self.stage == self.STAGE_CHARACTER_SELECT_ZERO

    def inSelectOneStage(self):
        return self.stage == self.STAGE_CHARACTER_SELECT_ONE

    def inSelectTwoStage(self):
        return self.stage == self.STAGE_CHARACTER_SELECT_TWO

    def inSelectStage(self):
        return self.stage in (self.STAGE_CHARACTER_SELECT_ZERO, self.STAGE_CHARACTER_SELECT_ONE, self.STAGE_CHARACTER_SELECT_TWO)

    def inDetailAdjustStage(self):
        return self.stage == self.STAGE_CHARACTER_DETAIL_ADJUST

    def gotoCreateStage(self):
        self.stage = self.STAGE_CHARACTER_CREATE

    def gotoSelectZeroStage(self):
        self.stage = self.STAGE_CHARACTER_SELECT_ZERO

    def gotoSelectOneStage(self):
        self.stage = self.STAGE_CHARACTER_SELECT_ONE

    def gotoSelectTwoStage(self):
        self.stage = self.STAGE_CHARACTER_SELECT_TWO

    def gotoDetailAdjustStage(self):
        self.stage = self.STAGE_CHARACTER_DETAIL_ADJUST

    def gotoBodyTypeStage(self):
        self.stage = self.STAGE_CHARACTER_BODYTYPE

    def gotoSexStage(self):
        self.stage = self.STAGE_CHARACTER_SEX

    def gotoAvatarconfigStage(self):
        self.stage = self.STAGE_CHARACTER_AVATARCONFIG

    def inBodyTypeStage(self):
        return self.stage in (self.STAGE_CHARACTER_BODYTYPE, self.STAGE_CHARACTER_SEX, self.STAGE_CHARACTER_SCHOOL)

    def inBodyTypeSubStage(self):
        return self.stage in (self.STAGE_CHARACTER_BODYTYPE,)

    def inBodyTypeSexStage(self):
        return self.stage == self.STAGE_CHARACTER_SEX

    def inAvatarconfigStage(self):
        return self.stage == self.STAGE_CHARACTER_AVATARCONFIG

    def gotoAvatarconfigStage2(self):
        self.stage = self.STAGE_CHARACTER_AVATARCONFIG_2

    def inAvatarconfigStage2(self):
        return self.stage in (self.STAGE_CHARACTER_AVATARCONFIG_2, self.STAGE_CHARACTER_AVATARCONFIG_2_SUB, self.STAGE_CHARACTER_SCHOOL_AVATARCONFIG)

    def inAvatarconfigStage2Sub(self):
        return self.stage in (self.STAGE_CHARACTER_AVATARCONFIG_2_SUB,)

    def inAvatarStage(self):
        return self.stage in (self.STAGE_CHARACTER_AVATARCONFIG_2,
         self.STAGE_CHARACTER_AVATARCONFIG,
         self.STAGE_CHARACTER_DETAIL_ADJUST,
         self.STAGE_CHARACTER_CONTROL,
         self.STAGE_CHARACTER_AVATARCONFIG_2_SUB,
         self.STAGE_CHARACTER_SCHOOL_AVATARCONFIG)

    def gotoSchoolStage(self):
        self.stage = self.STAGE_CHARACTER_SCHOOL

    def inSchoolStage(self):
        return self.stage == self.STAGE_CHARACTER_SCHOOL

    def gotoSchoolAvatarConfigStage(self):
        self.stage = self.STAGE_CHARACTER_SCHOOL_AVATARCONFIG

    def inSchoolAvatarConfigStage(self):
        return self.stage == self.STAGE_CHARACTER_SCHOOL_AVATARCONFIG

    def setPlayer(self, player = None, lookModel = None):
        self.player = player
        self.lookModel = lookModel
        if player:
            self.stage = self.STAGE_CHARACTER_CONTROL
            self.oldFov = BigWorld.projection().fov
            self.oldNearPlane = BigWorld.projection().nearPlane
            self.getPlayerHeight()
            CC.initCC()
            self.zoomTo(0)
            BigWorld.dcursor().yaw = 3.14
            BigWorld.dcursor().pitch = 0.0
            BigWorld.projection().nearPlane = 0.4
        else:
            self.stage = self.STAGE_CHARACTER_CREATE
            CC.restoreCC()
            if self.oldFov:
                BigWorld.projection().fov = self.oldFov
            if self.oldNearPlane:
                BigWorld.projection().nearPlane = self.oldNearPlane

    def lookAtLoginModel(self, player, needSetMatrix = True):
        if player:
            CC.initCC(needSetMatrix)
            matrix = Math.Matrix()
            node = player.model.node('biped Head')
            school = getattr(player, 'school', const.SCHOOL_SHENTANG)
            if clientcom.enableNewSchoolYeCha():
                self.focusPositionMap = gameglobal.NEW_XRJM_FOCUS_MAP
            else:
                self.focusPositionMap = gameglobal.OLD_XRJM_FOCUS_MAP
            if self.focusPositionMap.has_key(school):
                position = self.focusPositionMap[school]
            else:
                position = clientcom.getPositionByNode(node)
                self.focusPositionMap[school] = position
            matrix.setTranslate(position)
            CC.TC.movementHalfLife = 0.2
            CC.TC.maxDistHalfLife = 0.2
            gender = getattr(player, 'gender', const.SEX_MALE)
            bodyType = getattr(player, 'bodyType', const.BODY_TYPE_5)
            charShowData = self.getCharShowData(school, gender, bodyType)
            offset = charShowData.get('cameraOffset', (0.9, -0.1, 0))
            yaw, pitch = charShowData.get('yawPitch', (1.61, 0))
            self.cameraSound = charShowData.get('cameraSound', 980)
            self.addCameraEffect(player, charShowData)
            gameglobal.rds.sound.playSound(self.cameraSound)
            dc = BigWorld.dcursor()
            dc.yaw = yaw
            dc.pitch = pitch
            CC.playCC(0.01, offset, matrix, 0)
            BigWorld.projection().fov = 0.7
            BigWorld.setDepthOfField(True, 2, 0.15)
            BigWorld.projection().nearPlane = 0.25
        else:
            CC.TC = None
            CC.CC = None
            BigWorld.setDepthOfField(False)
            gameglobal.rds.sound.playSound(gameglobal.SD_992)
            self.removeCameraEffect()

    def addCameraEffect(self, player, charShowData):
        self.removeCameraEffect()
        fxId = charShowData.get('cameraEffect', 119211)
        fxs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (gameglobal.EFFECT_HIGH,
         gameglobal.EFF_PLAYER_SKILL_PRIORITY,
         player.model,
         fxId,
         sfx.EFFECT_UNLIMIT))
        self.cameraEffect = [player.model, fxId, fxs]

    def removeCameraEffect(self):
        if self.cameraEffect:
            model, fxId, fxs = self.cameraEffect
            sfx.detachEffect(model, fxId, fxs, True)
            self.cameraEffect = []

    def lookAtStage(self, enter):
        dc = BigWorld.dcursor()
        if enter:
            CC.initCC()
            matrix = Math.Matrix()
            matrix.setRotateY(1.61)
            dc.yaw = 1.426
            dc.pitch = 0.076
            dc.yawReference = matrix
            dc.minYaw = -1.57
            dc.maxYaw = 1.0
            dc.maxPitch = 0.4
            targetMatrix = Math.Matrix()
            targetMatrix.setTranslate(self.ALL_LOGINMODEL_POSITION)
            CC.playCC(0, (7, 1.5, -0.4), targetMatrix, 0.1)
            BigWorld.projection().fov = 0.7
        else:
            CC.restoreCC()
            dc.yawReference = None
            dc.minYaw = 0
            dc.maxYaw = 0

    def rotateStage(self):
        cueData = ':'.join((str(gameglobal.CAMERA_MODEL), 'camBone', 'intro_cam'))
        ent = self.multiModels[0]
        ent.filter.yaw = 2.0
        black.fade(0, 0.1, 4)
        cameraEffect.startAnimateCamera(cueData, ent, self._afterRotate)

    def _afterRotate(self):
        pass

    def setTaTint(self, isLight):
        if self.multiModels:
            for ent in self.multiModels:
                ent.setTaTint(isLight)
