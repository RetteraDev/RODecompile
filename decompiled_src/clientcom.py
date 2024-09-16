#Embedded file name: /WORKSPACE/data/entities/client/clientcom.o
import math
import traceback
import md5
import random
import re
import time
import urllib
import gzip
from ftplib import FTP
import Math
import BigWorld
import GUI
import ResMgr
import utils
import const
import gamelog
import gameglobal
import gametypes
import keys
import formula
import appSetting
import clientUtils
from helpers import remoteInterface
from callbackHelper import Functor
from helpers import charRes
from helpers import avatarMorpher
from helpers import vertexMorpher
from helpers import dyeMorpher
from helpers import tuZhuangDyeMorpher
from helpers import tintalt
from sfx import sfx
from helpers import tintalt as TA
import commcalc
from data import map_config_data as MCD
from data import sys_config_data as SCD
from data import equip_data as ED
from data import consumable_item_data as CID
from data import zaiju_data as ZJD
from cdata import tuzhuang_equip_data as TED
from data import npc_model_client_data as NMCD
try:
    from data import clientRevision
    CLIENT_REVISION = clientRevision.CLIENT_REVISION
except:
    CLIENT_REVISION = 0

def loadModelMainThread(res):
    gamelog.debug('loadModelMainThread ', res)
    paths = []
    dyes = []
    for i in res:
        if isinstance(i, str):
            paths.append(i)
        else:
            dyes.append(i)

    if len(paths) == 0:
        gamelog.error('zf:Error, path parse error ', res)
        return
    try:
        model = clientUtils.model(*paths)
    except:
        gamelog.error('zf:Error can not load model ', paths)
        return

    matters = model.getMatterList()
    if matters != None:
        for m in matters:
            for d in dyes:
                if d[0][0] == '*' or d[0][0] == m[0][0]:
                    setattr(model, m[0], d[1])

    return model


def resolveAvatarModelPath(partname):
    if not partname:
        return ''
    if partname[1] == '1':
        if partname[2] == '1':
            return gameglobal.charRes + '10001/01/' + partname + '.model'
        else:
            return gameglobal.charRes + '10001/02/' + partname + '.model'
    elif partname[1] == '2':
        if partname[2] == '1':
            return gameglobal.charRes + '10004/01/' + partname + '.model'
        else:
            return gameglobal.charRes + '10004/02/' + partname + '.model'
    else:
        return partname


def isAvatarMaleModel(entity):
    if gameglobal.rds.isSinglePlayer:
        try:
            if entity.fashion.modelID & 1:
                sex = const.SEX_MALE
            else:
                sex = const.SEX_FEMALE
        except:
            sex = const.SEX_MALE

    else:
        try:
            sex = entity.physique.sex
        except:
            try:
                if entity.fashion.modelID & 1:
                    sex = const.SEX_MALE
                else:
                    sex = const.SEX_FEMALE
            except:
                sex = const.SEX_MALE

    return sex == const.SEX_MALE


def getAvatarWeaponModelScale(entity):
    if not hasattr(entity, 'physique'):
        return 'f5Scale'
    return getAvatarKeyByPhysique(entity.physique) + 'Scale'


def getAvatarWeaponModelScaleByPhysique(physique):
    return getAvatarKeyByPhysique(physique) + 'Scale'


def getAvatarKey(entity):
    if not hasattr(entity, 'physique'):
        return 'f5'
    return getAvatarKeyByPhysique(entity.physique)


def getAvatarKeyByPhysique(physique):
    sclaeKey = ''
    if physique.sex == const.SEX_MALE:
        sclaeKey = 'm'
    else:
        sclaeKey = 'f'
    key = sclaeKey + str(physique.bodyType)
    return key


def getAvatarModelType(entity):
    gamelog.debug('getAvatarModelType:', entity.physique.bodyType)
    return entity.physique.bodyType


def checkAttackThrough(spaceID, startPos, endPos, targetHeight, targetRadius):
    gamelog.debug('checkAttackThrough.......', startPos, endPos, targetHeight, targetRadius)
    for h in (0.5, 1.0):
        if BigWorld.collide(spaceID, startPos + Math.Vector3(0, h * 2, 0), endPos + Math.Vector3(0, h * targetHeight, 0), gameglobal.TREEMATTERKINDS) == None:
            return True

    direction = endPos - startPos
    direction.normalise()
    rightDir = direction * Math.Vector3(0, 1, 0)
    rightDir.normalise()
    for h in (0.4, 0.8):
        beginPos = startPos + rightDir * 0.2 + Math.Vector3(0, h * 2, 0)
        targetPos = endPos + rightDir * targetRadius + Math.Vector3(0, h * targetHeight, 0)
        if BigWorld.collide(spaceID, beginPos, targetPos, gameglobal.TREEMATTERKINDS) == None:
            return True
        beginPos = startPos + Math.Vector3(0, h * 2, 0) - rightDir * 0.2
        targetPos = endPos + Math.Vector3(0, h * targetRadius, 0) - rightDir * targetRadius
        if BigWorld.collide(spaceID, beginPos, targetPos, gameglobal.TREEMATTERKINDS) == None:
            return True

    return False


def cross_product(v1, v2):
    ox = v1.y * v2.z - v2.y * v1.z
    oy = v1.z * v2.x - v2.z * v1.x
    oz = v1.x * v2.y - v2.x * v1.y
    return Math.Vector3(ox, oy, oz)


def getPlayerAvatar():
    p = BigWorld.player()
    if p.__class__.__name__ == 'PlayerAvatar':
        return p


def cloneEntityModel(entity, clonePose, cloneScale, cloneDye, cloneAttachments):
    if not entity or not entity.inWorld:
        return None
    modelServer = entity.modelServer
    ms = modelServer.getMainModelAndID()
    if not ms[1]:
        return None
    newModel = cloneModel(ms[1], clonePose, cloneScale, cloneDye)
    if cloneAttachments:
        cloneEntityAllAttachments(entity, newModel)
    return newModel


def cloneModel(model, clonePose, cloneScale, cloneDye):
    if not model:
        return
    try:
        res = list(model.sources)
        checkRes(res)
        newModel = clientUtils.model(*res)
    except:
        raise Exception('cloneModel:' + str(res))

    if clonePose:
        newModel.yaw = model.yaw
        newModel.position = model.position
    if cloneScale:
        newModel.scale = model.scale
    if cloneDye:
        matters = newModel.getMatterList()
        if matters != None:
            for m in matters:
                setattr(newModel, m[0], getattr(model, m[0]).tint)

    return newModel


def getAllWeaponModel(entity):
    weapons = []
    modelServer = getattr(entity, 'modelServer', None)
    if not modelServer:
        return []
    if hasattr(modelServer, 'leftWeaponModel'):
        weapons.append(modelServer.leftWeaponModel)
    if hasattr(modelServer, 'rightWeaponModel'):
        weapons.append(modelServer.rightWeaponModel)
    if hasattr(modelServer, 'leftWeaponBackup'):
        weapons.extend(modelServer.leftWeaponBackup)
    if hasattr(modelServer, 'rightWeaponBackup'):
        weapons.extend(modelServer.rightWeaponBackup)
    return weapons


def getHairWearModel(entity):
    weapons = []
    modelServer = getattr(entity, 'modelServer', None)
    if not modelServer:
        return []
    if hasattr(modelServer, 'headdress'):
        weapons.append(modelServer.headdress)
    if hasattr(modelServer, 'headdressRight'):
        weapons.append(modelServer.headdressRight)
    if hasattr(modelServer, 'headdressLeft'):
        weapons.append(modelServer.headdressLeft)
    return weapons


def getFaceWearModel(entity):
    weapons = []
    modelServer = getattr(entity, 'modelServer', None)
    if not modelServer:
        return []
    if hasattr(modelServer, 'facewear'):
        weapons.append(modelServer.facewear)
    if hasattr(modelServer, 'earwear'):
        weapons.append(modelServer.earwear)
    return weapons


def getOtherWearModel(entity):
    weapons = []
    modelServer = getattr(entity, 'modelServer', None)
    if not modelServer:
        return []
    if hasattr(modelServer, 'waistwear'):
        weapons.append(modelServer.waistwear)
    if hasattr(modelServer, 'backwear'):
        weapons.append(modelServer.backwear)
    if hasattr(modelServer, 'tailwear'):
        weapons.append(modelServer.tailwear)
    if hasattr(modelServer, 'chestwear'):
        weapons.append(modelServer.chestwear)
    if hasattr(modelServer, 'yuanLing'):
        weapons.append(modelServer.yuanLing)
    return weapons


def cloneEntityAllAttachments(entity, newModel, hangUpWeapon = False):
    cloneEntityAllWeaponAttachments(entity, newModel, hangUpWeapon)
    cloneEntityAllWearAttachments(entity, newModel, hangUpWeapon)


def cloneEntityAllWeaponAttachments(entity, newModel, hangUpWeapon = False):
    weapons = getAllWeaponModel(entity)
    for item in weapons:
        cloneEntityModelAttachment(entity, item, newModel, hangUpWeapon)


def cloneEntityAllWearAttachments(entity, newModel, hangUpWeapon = False):
    cloneEntityOtherWearAttachments(entity, newModel, hangUpWeapon)
    cloneEntityHairWearAttachments(entity, newModel, hangUpWeapon)
    cloneEntityFaceWearAttachments(entity, newModel, hangUpWeapon)


def cloneEntityOtherWearAttachments(entity, newModel, hangUpWeapon = False):
    wears = getOtherWearModel(entity)
    for item in wears:
        if not item or not getattr(item, 'getPhotoAction', None):
            continue
        photoAction = item.getPhotoAction()
        cloneEntityModelWearAttachment(entity, item, newModel, None, hangUpWeapon, False, photoAction)


def cloneAllAttachments(aspect, physique, showFashion, newModel, hangUpWeapon = False):
    cloneAllWeaponAttachments(aspect, physique, showFashion, newModel, hangUpWeapon)
    cloneAllWearAttachments(aspect, physique, newModel, hangUpWeapon)


def cloneAllWeaponAttachments(aspect, physique, showFashion, newModel, hangUpWeapon = False):
    attachments = []
    p = BigWorld.player()
    weapons = ('leftWeapon', 'rightWeapon')
    fashionWeapons = ('leftFashionWeapon', 'rightFashionWeapon')
    for i in xrange(0, 2):
        weaponId = getattr(aspect, fashionWeapons[i])
        weaponEnhLv = getattr(aspect, fashionWeapons[i] + 'EnhLv')()
        if not weaponId:
            weaponId = getattr(aspect, weapons[i])
            weaponEnhLv = getattr(aspect, weapons[i] + 'EnhLv')()
        if weaponId:
            equipModel = p.modelServer.leftWeaponModel
            subIdList = ED.data.get(weaponId, {}).get('subId', [])
            for i in xrange(0, len(subIdList)):
                attachments.extend(equipModel.getAttachments(weaponId, i, weaponEnhLv, physique))

    cloneEntityModelAttachment(p, attachments, newModel, hangUpWeapon, True)


def cloneAllWearAttachments(aspect, physique, newModel, hangUpWeapon = False):
    cloneOtherWearAttachments(aspect, physique, newModel, hangUpWeapon)
    cloneHairWearAttachments(aspect, physique, newModel, hangUpWeapon)
    cloneFaceWearAttachments(aspect, physique, newModel, hangUpWeapon)


def cloneOtherWearAttachments(aspect, physique, newModel, hangUpWeapon = False):
    p = BigWorld.player()
    for wearStr in p.modelServer.otherwears:
        wearId = getattr(aspect, wearStr)
        if wearId:
            wear = getattr(p.modelServer, wearStr)
            attachments = wear.getAttachments(wearId, None, physique)
            photoAction = wear.getPhotoAction(wearId)
            cloneEntityModelWearAttachment(p, attachments, newModel, None, hangUpWeapon, True, photoAction)

    yuanLingId = aspect.yuanLing
    if yuanLingId:
        wear = p.modelServer.yuanLing
        attachments = wear.getAttachments(yuanLingId, 0, 0, physique)
        photoAction = wear.getPhotoAction(yuanLingId)
        cloneEntityModelWearAttachment(p, attachments, newModel, None, hangUpWeapon, True, photoAction)


def cloneHairWearAttachments(aspect, physique, newModel, hangUpWeapon = False):
    p = BigWorld.player()
    hairNode = getHairNode(p, newModel, True, aspect)
    for wearStr in p.modelServer.headdresses:
        wearId = getattr(aspect, wearStr)
        if wearId:
            wear = getattr(p.modelServer, wearStr)
            photoAction = wear.getPhotoAction(wearId)
            attachments = wear.getAttachments(wearId, None, physique)
            cloneEntityModelWearAttachment(p, attachments, newModel, hairNode, hangUpWeapon, True, photoAction)


def cloneFaceWearAttachments(aspect, physique, newModel, hangUpWeapon = False):
    p = BigWorld.player()
    for wearStr in p.modelServer.headwear:
        wearId = getattr(aspect, wearStr)
        if wearId:
            wear = getattr(p.modelServer, wearStr)
            attachments = wear.getAttachments(wearId, None, physique)
            photoAction = wear.getPhotoAction(wearId)
            cloneEntityModelWearAttachment(p, attachments, newModel, None, hangUpWeapon, True, photoAction)


def getHairNode(entity, newModel, needSetDye = True, aspect = None):
    if not newModel:
        return
    hairNode = None
    try:
        path = entity.modelServer.getHairNode(newModel)
        if path and isFileExist(path):
            hairNode = clientUtils.model(path)
    except:
        hairNode = None

    node = newModel.node('biped Head')
    if node and hairNode:
        if node.attachments:
            for model in node.attachments:
                node.detach(model)

        node.attach(hairNode, 'biped Head')
        try:
            hairNode.action('1101')()
        except:
            pass

        if needSetDye:
            if aspect:
                setHairNodeDyeByAspect(aspect, hairNode)
            else:
                setHairNodeDye(entity, hairNode)
    return hairNode


def setHairNodeDye(entity, model):
    if hasattr(entity, 'realAspect') and model:
        aspect = entity.realAspect
        setHairNodeDyeByAspect(aspect, model)


def setHairNodeDyeByAspect(aspect, model):
    if aspect:
        fashionHead = aspect.fashionHead
        headType = charRes.getHeadType(fashionHead)
        if headType == charRes.HEAD_TYPE2:
            dyeList = aspect.fashionHeadDyeList()
            material = ED.data.get(fashionHead, {}).get('materials', None)
            hairDyeMorpher = dyeMorpher.HairDyeMorpher(model)
            hairDyeMorpher.read(dyeList, material)
            hairDyeMorpher.apply()


def getHairNodeDynamicTint(entity):
    if hasattr(entity, 'realAspect'):
        aspect = entity.realAspect
        return getHairNodeDynamicTintByAsepect(aspect)


def getHairNodeDynamicTintByAsepect(aspect):
    if aspect:
        fashionHead = aspect.fashionHead
        headType = charRes.getHeadType(fashionHead)
        if headType == charRes.HEAD_TYPE2:
            dyeList = aspect.fashionHeadDyeList()
            material = ED.data.get(fashionHead, {}).get('materials', None)
            hairDyeMorpher = dyeMorpher.HairDyeMorpher(None)
            hairDyeMorpher.read(dyeList, material)
            return hairDyeMorpher.getDynamicTint()


def cloneEntityHairWearAttachments(entity, newModel, hangUpWeapon = False, aspect = None):
    wears = getHairWearModel(entity)
    hairNode = getHairNode(entity, newModel, aspect=aspect)
    for item in wears:
        if not item:
            continue
        photoAction = item.getPhotoAction()
        cloneEntityModelWearAttachment(entity, item, newModel, hairNode, hangUpWeapon, False, photoAction)

    wears = getFaceWearModel(entity)
    for item in wears:
        if not item:
            continue
        photoAction = item.getPhotoAction()
        cloneEntityModelWearAttachment(entity, item, newModel, None, hangUpWeapon, False, photoAction)


def cloneEntityFaceWearAttachments(entity, newModel, hangUpWeapon = False):
    wears = getFaceWearModel(entity)
    for item in wears:
        if not item:
            continue
        photoAction = item.getPhotoAction()
        cloneEntityModelWearAttachment(entity, item, newModel, None, hangUpWeapon, False, photoAction)


def cloneEntityModelWearAttachment(entity, tempModel, newModel, hairNode = None, hangUpWeapon = False, isFittingRoom = False, idleAction = None, showEffect = None):
    if tempModel:
        if isFittingRoom:
            models = tempModel
        else:
            models = tempModel.models
        attachModels = []
        cloneHPs = getattr(entity, 'cloneHPs', [])
        for i in models:
            attachModel = None
            try:
                if isFittingRoom or i[1]:
                    if isFittingRoom:
                        attachModel = clientUtils.model(i[0])
                    else:
                        attachModel = clientUtils.model(*i[0].sources)
                    if attachModel:
                        attachModel.isWear = True
                        attachModels.append(attachModel)
                    attachHP = i[3] if hangUpWeapon else i[2]
                    if attachHP in ('HP_root', 'Scene Root'):
                        node = newModel.node(attachHP)
                        if node and node.attachments:
                            for subModel in node.attachments:
                                if getattr(subModel, 'isWear', False):
                                    node.detach(subModel)
                                    break

                        newModel.node(attachHP).attach(attachModel)
                        newModel.node(attachHP).scale(i[5])
                    elif newModel.node(attachHP):
                        newModel.setHP(attachHP, None)
                        newModel.setHP(attachHP, attachModel)
                        newModel.node(attachHP).scale(i[5])
                        cloneHPs.append(attachHP)
                    elif hairNode and hairNode.node(attachHP):
                        hairNode.setHP(attachHP, None)
                        hairNode.setHP(attachHP, attachModel)
                        hairNode.node(attachHP).scale(i[5])
                        cloneHPs.append(attachHP)
                    if showEffect:
                        for ef in showEffect:
                            sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (entity.getBasicEffectLv(),
                             entity.getBasicEffectPriority(),
                             attachModel,
                             ef,
                             sfx.EFFECT_UNLIMIT))

                    if attachModel:
                        try:
                            if idleAction:
                                attachModel.action(idleAction)()
                        except:
                            pass

                else:
                    for hp in i[2:4]:
                        if hp != None:
                            if hp in ('HP_root', 'Scene Root'):
                                node = newModel.node(hp)
                                if node and node.attachments:
                                    for subModel in node.attachments:
                                        if getattr(subModel, 'isWear', False):
                                            node.detach(subModel)
                                            break

                            elif newModel.node(hp):
                                newModel.setHP(hp, None)
                            else:
                                hairNode.setHP(hp, None)

            except:
                traceback.print_exc()

            if newModel and newModel.inWorld:
                try:
                    if i[2] in ('HP_root', 'Scene Root'):
                        attachModel.bias = (0.5, 1.5, -0.5)
                        attachModel.action('1101')()
                except:
                    pass

                if i[6]:
                    for effect in i[6]:
                        fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (entity.getEquipEffectLv(),
                         entity.getEquipEffectPriority(),
                         attachModel,
                         effect,
                         sfx.EFFECT_LIMIT_MISC))

                if i[8]:
                    TA.ta_set_static([attachModel], i[8])

        return attachModels


def cloneEntityModelAttachment(entity, tempModel, newModel, hangUpWeapon = False, isFittingRoom = False):
    if tempModel:
        if isFittingRoom:
            models = tempModel
        else:
            models = tempModel.models
        attachModels = []
        for i in models:
            attachModel = None
            try:
                if isFittingRoom or i[1]:
                    if isFittingRoom:
                        attachModel = clientUtils.model(i[0])
                    else:
                        attachModel = clientUtils.model(*i[0].sources)
                    attachModel.isWeapon = True
                    if attachModel:
                        attachModels.append(attachModel)
                    attachHP = i[3] if hangUpWeapon else i[1]
                    if not attachHP:
                        continue
                    if attachHP in ('HP_root', 'Scene Root'):
                        node = newModel.node(attachHP)
                        if node and node.attachments and attachModel:
                            for subModel in node.attachments:
                                if getattr(subModel, 'isWeapon', False):
                                    node.detach(subModel)
                                    break

                        newModel.node(attachHP).attach(attachModel)
                    elif hasattr(entity, 'showBackWaist') and entity.showBackWaist:
                        newModel.setHP(attachHP, None)
                    else:
                        newModel.setHP(attachHP, None)
                        newModel.setHP(attachHP, attachModel)
                    newModel.node(attachHP).scale(i[5])
                else:
                    for hp in i[2:4]:
                        if hp != None:
                            if hp in ('HP_root', 'Scene Root'):
                                node = newModel.node(hp)
                                if node and node.attachments:
                                    for subModel in node.attachments:
                                        if getattr(subModel, 'isWeapon', False):
                                            node.detach(subModel)
                                            break

                            else:
                                newModel.setHP(hp, None)

            except:
                traceback.print_exc()

            if newModel and newModel.inWorld:
                if isFittingRoom:
                    attachHasAni = i[9]
                    dye = i[1]
                else:
                    attachHasAni = tempModel.attachHasAni
                    dye = tempModel.orginDye
                try:
                    if attachHasAni:
                        attachModel.bias = (-0.5, 1.5, -0.5)
                        attachModel.action('1101')()
                    else:
                        act = i[13] if hangUpWeapon else i[12]
                        attachModel.action(act)()
                except:
                    pass

                if i[6]:
                    for effect in i[6]:
                        sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (entity.getEquipEffectLv(),
                         entity.getEquipEffectPriority(),
                         attachModel,
                         effect,
                         sfx.EFFECT_LIMIT_MISC))

                if dye:
                    TA.ta_set_static([attachModel], dye)

        return attachModels


def cloneBasicAttachment(entity, tempModel, newModel, isFittingRoom = False, isRide = False, equipId = 0, rScale = None):
    if tempModel:
        if isFittingRoom:
            models = tempModel
        else:
            models = tempModel.models
        i = models[0]
        attachModel = None
        try:
            if isFittingRoom:
                attachModel = clientUtils.model(i[0])
            else:
                attachModel = clientUtils.model(*i[0].sources)
            attachHP = i[2]
            if equipId and ED.data.get(equipId, {}).get('hideMajorRide', 0):
                pass
            elif isRide:
                attachModel.setHP(attachHP, None)
                attachModel.setHP(attachHP, newModel)
                attachModel.scale = (i[3], i[3], i[3])
                if rScale:
                    attachModel.node(attachHP).scale(rScale, rScale, rScale)
            else:
                newModel.setHP(attachHP, None)
                newModel.setHP(attachHP, attachModel)
                newModel.node(attachHP).scale(i[3])
            if i[1]:
                TA.ta_set_static([attachModel], i[1])
        except:
            traceback.print_exc()

        if newModel and newModel.inWorld:
            if i[4]:
                for effect in i[4]:
                    fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (entity.getEquipEffectLv(),
                     entity.getEquipEffectPriority(),
                     attachModel,
                     effect,
                     sfx.EFFECT_LIMIT_MISC))
                    if fx:
                        for item in fx:
                            item.scale(i[3])

        return attachModel


def worldPointToScreen(worldPoint):
    if not isinstance(BigWorld.camera(), BigWorld.CursorCamera):
        return (-10000, -10000)
    posInCamera = Math.Matrix(gameglobal.rds.cam.ccMatrixProvider).applyPoint(worldPoint)
    if posInCamera.z < 0:
        return (-10000, -10000)
    projection = BigWorld.projection()
    projMat = Math.Matrix()
    screenWidth = BigWorld.screenWidth()
    screenHeight = BigWorld.screenHeight()
    if hasattr(BigWorld, 'getInnerScreenSize'):
        innerSize = BigWorld.getInnerScreenSize()
        screenWidth = screenWidth / innerSize
        screenHeight = screenHeight / innerSize
    projMat.perspectiveProjection(projection.fov, float(screenWidth) / screenHeight, projection.nearPlane, projection.farPlane)
    posInClip = projMat.applyPoint(posInCamera)
    xCoord = screenWidth * (posInClip.x + 1) / 2.0
    yCoord = screenHeight * (1 - posInClip.y) / 2.0
    if math.isnan(xCoord) or math.isnan(yCoord):
        return (-10000, -10000)
    return (xCoord, yCoord)


gRidableModels = frozenset((2588, 2822, 60001, 60003))

def worldPointToScreenCheckBound(worldPoint):
    result = worldPointToScreen(worldPoint)
    screenWidth = BigWorld.screenWidth()
    screenHeight = BigWorld.screenHeight()
    if result[0] < 0 or result[0] > screenWidth or result[1] < 0 or result[1] > screenHeight:
        return None
    return result


def _getAvatarConfigFromFile(conf):
    if not conf:
        return {'model': gameglobal.defaultModelID,
         'dye': 'Default'}
    avatarConfig = conf.readString('avatarConfig')
    gender = conf.readInt('gender')
    bodyType = conf.readInt('bodyType')
    school = conf.readInt('school')
    transModelId = conf.readInt('transModelId', 1)
    hair = conf.readInt('hair')
    headType = conf.readInt('headType', charRes.HEAD_TYPE0)
    head = conf.readInt('head', 0)
    hand = conf.readInt('hand')
    body = conf.readInt('body')
    leg = conf.readInt('leg')
    shoe = conf.readInt('shoe')
    dyesDict = {}
    dyesDict['head'] = parseStrToList(conf.readString('headDye', ''))
    dyesDict['hand'] = parseStrToList(conf.readString('handDye', ''))
    dyesDict['leg'] = parseStrToList(conf.readString('legDye', ''))
    dyesDict['shoe'] = parseStrToList(conf.readString('shoeDye', ''))
    dyesDict['body'] = parseStrToList(conf.readString('bodyDye', ''))
    mattersDict = {}
    mattersDict['head'] = conf.readString('headMatter', None)
    mattersDict['hand'] = conf.readString('handMatter', None)
    mattersDict['leg'] = conf.readString('legMatter', None)
    mattersDict['shoe'] = conf.readString('shoeMatter', None)
    mattersDict['body'] = conf.readString('bodyMatter', None)
    return {'isAvatar': False,
     'multiPart': True,
     'transModelId': transModelId,
     'bodyType': bodyType,
     'school': school,
     'hair': hair,
     'shoe': shoe,
     'leg': leg,
     'body': body,
     'hand': hand,
     'head': head,
     'sex': gender,
     'headType': headType,
     'dyesDict': dyesDict,
     'avatarConfig': avatarConfig,
     'mattersDict': mattersDict}


def parseStrToList(confString):
    if not confString or confString == '[]':
        return ()
    confString = confString.replace(' ', '')
    confString = confString.replace("\'", '\"')
    confString = confString.replace('(\"', '')
    confString = confString.replace('\",)', '')
    confString = confString.replace('\")', '')
    confString = confString.replace('\",\"', '#')
    confString = confString.strip(" ()[]\'\"")
    confData = confString.split('#')
    if not confData:
        return ()
    return tuple(confData)


class XMLCache(object):

    def __init__(self):
        self.cache = {}

    def get(self, path, default = None):
        if self.cache.has_key(path):
            return self.cache.get(path, default)
        return default

    def add(self, path, data):
        self.cache[path] = data

    def remove(self):
        self.cache = {}

    def has_key(self, path):
        return self.cache.has_key(path)

    def getConfig(self, path, default = {}):
        if not self.has_key(path):
            self.loadConfig(path)
        return self.get(path, default)

    def getConfigCopy(self, path, default = {}):
        if not self.has_key(path):
            self.loadConfig(path)
        return dict(self.get(path, default))

    def loadConfig(self, path):
        conf = ResMgr.openSection(path)
        self.add(path, conf)

    def fetchConfig(self, path, callback):
        if not self.cache.has_key(path):
            ResMgr.bkgOpenSections(Functor(self.afterFetchConfig, path, callback), path)
        elif callback:
            callback(self.get(path))

    def afterFetchConfig(self, path, callback, rs):
        conf = rs[0][1]
        if not conf:
            raise Exception('error xml File: %s' % path)
        self.add(path, conf)
        if callback:
            callback(conf)


class AvatarConfigCache(XMLCache):

    def loadConfig(self, path):
        conf = ResMgr.openSection(path)
        itemData = _getAvatarConfigFromFile(conf)
        self.add(path, itemData)

    def afterFetchConfig(self, path, callback, rs):
        conf = rs[0][1]
        if not conf:
            raise Exception('error xml File: %s' % path)
        itemData = _getAvatarConfigFromFile(conf)
        self.add(path, itemData)
        if callback:
            callback(itemData)


Cache = XMLCache()
ConfigCache = AvatarConfigCache()

def _getModelData(modelId):
    resPath = '%s/%d.xml' % (gameglobal.AVATAR_TEMPLATE_PATH, modelId)
    return ConfigCache.getConfigCopy(resPath)


def _getAvatarConfig(modelId):
    resPath = '%s/%d.xml' % (gameglobal.AVATAR_TEMPLATE_PATH, modelId)
    itemData = ConfigCache.getConfig(resPath)
    if itemData:
        mpr = charRes.convertToMultiPartRes(itemData)
        res = mpr.getPrerequisites()
        return (res, itemData)
    defaultModel = {'model': gameglobal.defaultModelID,
     'dye': 'Default'}
    return (None, defaultModel)


def _fetchAvatarConfig(modelId, callback):
    resPath = '%s/%d.xml' % (gameglobal.AVATAR_TEMPLATE_PATH, modelId)
    ConfigCache.fetchConfig(resPath, Functor(_afterAvatarConfigFinished, modelId, callback))


def _afterAvatarConfigFinished(modelId, callback, itemData):
    mpr = charRes.convertToMultiPartRes(itemData)
    res = mpr.getPrerequisites()
    if callback:
        callback(res, itemData)


def setAvatarConfig(callback, avatarConfig, model, applyBoneMorph = True, loadImmediate = False):
    m = avatarMorpher.SimpleModelMorpher(model, avatarConfig['sex'], avatarConfig['school'], avatarConfig['bodyType'], 0, avatarConfig['hair'], 0, avatarConfig['body'], avatarConfig['hand'], avatarConfig['leg'], avatarConfig['shoe'], avatarConfig['transModelId'], avatarConfig.get('headType', charRes.HEAD_TYPE0), avatarConfig['dyesDict'], cape=avatarConfig.get('cape', None))
    config = avatarConfig['avatarConfig']
    if config:
        m.readConfig(config)
        if applyBoneMorph:
            m.apply(loadImmediate)
        else:
            m.applyFaceMorph()
            if loadImmediate:
                m.applyDyeMorph(loadImmediate)
    if callback:
        callback(model)


def copyAndSetAvatarConfig(callback, player, model, applyBoneMorph = True, loadImmediate = False):
    player.tintAvatarTas = {}
    mpr = charRes.MultiPartRes()
    mpr.queryByAvatar(player)
    m = avatarMorpher.SimpleModelMorpher(model, player.realPhysique.sex, player.realPhysique.school, player.realPhysique.bodyType, mpr.face, mpr.hair, mpr.head, mpr.body, mpr.hand, mpr.leg, mpr.shoe, False, mpr.headType, mpr.dyesDict, mpr.mattersDict, cape=mpr.cape)
    if player.realAvatarConfig:
        m.readConfig(player.realAvatarConfig)
        m.applyFaceMorph()
        m.applyDyeMorph(loadImmediate)
        if applyBoneMorph:
            m.applyBoneMorph()
        else:
            m.applyFaceBoneMorph()
    if callback:
        callback(model)


def checkRes(res):
    pattern = re.compile('::/[0-9a-z]+/')
    for i, item in enumerate(res):
        if type(item) == str:
            match = pattern.match(item)
            if match:
                res[i] = res[i][len(match.group()):]


def parseMatterDyePair(res):
    matterDyePairs = []
    for value in res:
        if type(value) == tuple:
            if type(value[0]) == str:
                matterDyePairs.append(value)

    return matterDyePairs


def saveMatterDyePair(res, model):
    matterDyePairs = parseMatterDyePair(res)
    for matterDyePair in matterDyePairs:
        if len(matterDyePair) > 2:
            TA.ta_set_static_states(model, matterDyePair[1], matterDyePair[0], matterDyePair[2], matterDyePair[3])
        else:
            TA.ta_set_static_states(model, matterDyePair[1], matterDyePair[0])


def getModel(modelId):
    if modelId > const.MODEL_AVATAR_BORDER:
        res, avatarConfig = _getAvatarConfig(modelId)
        try:
            res = list(res)
            checkRes(res)
            res = [ item for item in res if type(item) != tuple ]
            model = clientUtils.model(*res)
        except:
            raise Exception('getModel: %d %s' % (modelId, str(res)))

        if hasattr(model, 'bkgLoadTint'):
            model.bkgLoadTint = False
        setAvatarConfig(None, avatarConfig, model, loadImmediate=True)
    else:
        res = 'char/%i/%i.model' % (modelId, modelId)
        try:
            model = clientUtils.model(res)
        except:
            raise Exception('getModel: %d %s' % (modelId, str(res)))

    return model


def fetchModel(threadId, callback, modelId):
    if modelId > const.MODEL_AVATAR_BORDER:
        _fetchAvatarConfig(modelId, Functor(afterFetchAvatarConfig, threadId, callback, modelId))
    else:
        res = 'char/%i/%i.model' % (modelId, modelId)
        clientUtils.fetchModel(threadId, callback, res)


def afterFetchAvatarConfig(threadId, callback, modelId, res, avatarConfig):
    try:
        res = list(res)
        checkRes(res)
        clientUtils.fetchModel(threadId, Functor(afterFetchModel, callback, avatarConfig, res), *res)
    except:
        raise Exception('getModel: %d' % modelId)


def afterFetchModel(callback, avatarConfig, res, model):
    if model:
        m = vertexMorpher.AvatarFaceMorpher(None, model)
        m.readConfig(avatarConfig['avatarConfig'])
        m.apply()
        saveMatterDyePair(res, model)
    if callback:
        callback(model)


def cloneEntityModelByFetch(entity, threadId, callback, clonePose, cloneScale, cloneDye, cloneAttachments):
    if not entity or not entity.inWorld:
        return None
    modelServer = entity.modelServer
    ms = modelServer.getMainModelAndID()
    if not ms[1]:
        return None
    model = ms[1]
    try:
        res = list(model.sources)
        checkRes(res)
        clientUtils.fetchModel(threadId, Functor(afterEntityModelLoadFinished, ms[1], modelServer, callback, clonePose, cloneScale, cloneDye, cloneAttachments), *res)
    except:
        raise Exception('cloneEntityModelByFetch:' + str(res))


def afterEntityModelLoadFinished(model, modelServer, callback, clonePose, cloneScale, cloneDye, cloneAttachments, newModel):
    if clonePose:
        newModel.yaw = model.yaw
        newModel.position = model.position
    if cloneScale:
        newModel.scale = model.scale
    if cloneDye:
        matters = newModel.getMatterList()
        if matters != None:
            for m in matters:
                setattr(newModel, m[0], getattr(model, m[0]).tint)

    if callback:
        callback(newModel)


def getAvatarRes(ent):
    if hasattr(ent, 'realAspect'):
        mpr = charRes.MultiPartRes()
        mpr.queryByAvatar(ent)
        mpr.isAvatar = False
        res = mpr.getPrerequisites()
        avatarConfig = mpr.avatarConfig
    elif hasattr(ent, 'getItemData'):
        itemData = ent.getItemData()
        multiPart = itemData.get('multiPart', False)
        modelId = itemData.get('model')
        if not multiPart:
            if modelId > const.MODEL_AVATAR_BORDER:
                itemData = _getModelData(modelId)
        if multiPart:
            mpr = charRes.convertToMultiPartRes(itemData)
            res = mpr.getPrerequisites()
            avatarConfig = mpr.avatarConfig
        else:
            res = ('%s/%d.xml' % (gameglobal.AVATAR_TEMPLATE_PATH, modelId),)
            avatarConfig = ''
    return (res, avatarConfig)


def fetchAvatarModel(ent, threadId, callback):
    if hasattr(ent, 'modelServer'):
        res = None
        avatarConfig = ''
        ent.tintAvatarTas = {}
        if hasattr(ent, 'realAspect'):
            mpr = charRes.MultiPartRes()
            mpr.queryByAvatar(ent)
            mpr.isAvatar = False
            res = mpr.getPrerequisites()
            avatarConfig = mpr.avatarConfig
        elif hasattr(ent, 'getItemData'):
            itemData = ent.getItemData()
            multiPart = itemData.get('multiPart', False)
            modelId = itemData.get('model')
            if not multiPart:
                if modelId > const.MODEL_AVATAR_BORDER:
                    itemData = _getModelData(modelId)
            if multiPart:
                mpr = charRes.convertToMultiPartRes(itemData)
                res = mpr.getPrerequisites()
                avatarConfig = mpr.avatarConfig
            else:
                res = ('%s/%d.xml' % (gameglobal.AVATAR_TEMPLATE_PATH, modelId),)
                avatarConfig = ''
        if res:
            clientUtils.fetchModel(threadId, Functor(afterAvatarModelFinished, callback, avatarConfig, res), *res)


def fetchAvatarModelByRes(res, avatarConfig, threadId, callback):
    clientUtils.fetchModel(threadId, Functor(afterAvatarModelFinished, callback, avatarConfig, res), *res)


def afterAvatarModelFinished(callback, avatarConfig, res, model):
    if avatarConfig:
        m = vertexMorpher.AvatarFaceMorpher(None, model)
        m.readConfig(avatarConfig)
        m.apply()
    saveMatterDyePair(res, model)
    if callback:
        callback(model)


def openUrl(emailAddress):
    t = utils.getNow()
    salt = 'Kz`bs{9?<=p7zsu:mk7'
    psw = str(md5.new(emailAddress + str(t) + salt).hexdigest())
    gamelog.debug(psw)
    path = 'http://next.netease.com'
    gamelog.debug('openUrl:', path)
    BigWorld.openUrl(path)


def openFeedbackUrl(url):
    gamelog.debug('openFeedbackUrl', url)
    BigWorld.openUrl(url)


def isInBoundingBox(minBounds, maxBounds, point):
    if point[0] < minBounds[0] or point[0] > maxBounds[0] or point[1] < minBounds[1] or point[1] > maxBounds[1] or point[2] < minBounds[2] or point[2] > maxBounds[2]:
        return False
    return True


def isIntersectWithPlayer(model):
    pos = BigWorld.player().position
    if hasattr(model, 'depth'):
        pos = Math.Vector2(pos.x, pos.z)
        width = model.width
        depth = model.depth
        yaw = model.yaw
        dir = Math.Vector2(math.sin(yaw), math.cos(yaw))
        crossDir = Math.Vector2(-dir.y, dir.x)
        pos0 = Math.Vector2(model.position.x, model.position.z)
        pos1 = pos0 - crossDir * (0.5 * width)
        pos2 = pos0 + crossDir * (0.5 * width)
        p0 = pos1 + dir * (0.5 * depth)
        p1 = pos1 - dir * (0.5 * depth)
        p2 = pos2 + dir * (0.5 * depth)
        p3 = pos2 - dir * (0.5 * depth)
        return utils.isInRectangle(p0, p2, p3, p1, pos)
    minbd = model.pickbdbox[0] - Math.Vector3(0.5, 2, 0.5)
    maxbd = model.pickbdbox[1] + Math.Vector3(0.5, 0, 0.5)
    return isInBoundingBox(minbd, maxbd, pos)


def delDebugGui(guis):
    if guis:
        for g in guis:
            if g:
                GUI.delRoot(g)


def genLineGui(startPos, endPos, radius, colour = None):
    line = GUI.WorldDebugGUI()
    line.startPos = startPos
    line.endPos = endPos
    line.radius = radius
    if colour:
        line.colour = colour
    GUI.addRoot(line)
    return line


def drawLines(positions, close = True, color = None):
    if not positions:
        return
    length = len(positions)
    if length < 2:
        return
    lines = []
    for i in xrange(length):
        if i != length - 1:
            lines.append(genLineGui(positions[i], positions[i + 1], 0.01, color))

    if close:
        lines.append(genLineGui(positions[length - 1], positions[0], 0.01, color))
    return lines


def drawRingDebug(centerPos, innerRadius, outerRadius, height, maxDelayTime = 1, colorInner = (0, 0, 255, 0), colorOuter = None):
    lineList = []
    line = genLineGui(centerPos, (centerPos[0], centerPos[1] + height, centerPos[2]), innerRadius, colorInner)
    lineList.append(line)
    line = genLineGui(centerPos, (centerPos[0], centerPos[1] + height, centerPos[2]), outerRadius, colorOuter)
    lineList.append(line)
    BigWorld.callback(maxDelayTime, Functor(delDebugGui, lineList))


def drawCylinderDebug(centerPos, radii, height, depth, maxDelayTime = 1, color = None):
    lineList = []
    startPos = (centerPos[0], centerPos[1] - depth, centerPos[2])
    endPos = (centerPos[0], centerPos[1] + height, centerPos[2])
    line = genLineGui(startPos, endPos, radii, color)
    lineList.append(line)
    BigWorld.callback(maxDelayTime, Functor(delDebugGui, lineList))


def drawCubeDebug(centerPos, width, depth, height, yaw, maxDelayTime = 1, color = None):
    lineList = []
    leftPos = utils.getRelativePosition(centerPos, yaw, -90, width)
    rightPos = utils.getRelativePosition(centerPos, yaw, 90, width)
    frontMidPos = utils.getRelativePosition(centerPos, yaw, 0, depth)
    leftFrontPos = utils.getRelativePosition(frontMidPos, yaw, -90, width)
    rightFrontPos = utils.getRelativePosition(frontMidPos, yaw, 90, width)
    leftHPos = (leftPos[0], leftPos[1] + height, leftPos[2])
    rightHPos = (rightPos[0], rightPos[1] + height, rightPos[2])
    leftFrontHPos = (leftFrontPos[0], leftFrontPos[1] + height, leftFrontPos[2])
    rightFrontHPos = (rightFrontPos[0], rightFrontPos[1] + height, rightFrontPos[2])
    lineList.extend(drawLines([leftPos,
     leftFrontPos,
     rightFrontPos,
     rightPos], color=color))
    lineList.append(genLineGui(leftPos, leftHPos, 0.01, color))
    lineList.append(genLineGui(rightPos, rightHPos, 0.01, color))
    lineList.append(genLineGui(leftFrontPos, leftFrontHPos, 0.01, color))
    lineList.append(genLineGui(rightFrontPos, rightFrontHPos, 0.01, color))
    BigWorld.callback(maxDelayTime, Functor(delDebugGui, lineList))


def drawCubeViewDebug(centerPos, width, depth, height, yaw, maxDelayTime = 1, color = None):
    lineList = []
    leftTopPos = (centerPos[0] - depth, centerPos[1], centerPos[2] + width)
    leftBottomPos = (centerPos[0] - depth, centerPos[1], centerPos[2] - width)
    rightTopPos = (centerPos[0] + depth, centerPos[1], centerPos[2] + width)
    rightBottomPos = (centerPos[0] + depth, centerPos[1], centerPos[2] - width)
    leftTopHPos = (leftTopPos[0], leftTopPos[1] + height, leftTopPos[2])
    leftBottomHPos = (leftBottomPos[0], leftBottomPos[1] + height, leftBottomPos[2])
    rightTopHPos = (rightTopPos[0], rightTopPos[1] + height, rightTopPos[2])
    rightBottomHPos = (rightBottomPos[0], rightBottomPos[1] + height, rightBottomPos[2])
    lineList.extend(drawLines([leftTopPos,
     rightTopPos,
     rightBottomPos,
     leftBottomPos], color=color))
    lineList.append(genLineGui(leftTopPos, leftTopHPos, 0.01, color))
    lineList.append(genLineGui(leftBottomPos, leftBottomHPos, 0.01, color))
    lineList.append(genLineGui(rightTopPos, rightTopHPos, 0.01, color))
    lineList.append(genLineGui(rightBottomPos, rightBottomHPos, 0.01, color))
    BigWorld.callback(maxDelayTime, Functor(delDebugGui, lineList))


def drawRadianDebug(centerPos, radii, radian, height, yaw, maxDelayTime = 1, color = None):
    lineList = []
    points = getRadianPoints(centerPos, radii, radian, height, yaw, 8)
    lineList.extend(drawLines(points))
    length = len(points)
    startL = points[1]
    start = (startL[0], startL[1] + height, startL[2])
    endL = points[length - 1]
    end = (endL[0], endL[1] + height, endL[2])
    lineList.append(genLineGui(startL, start, 0.01, color))
    lineList.append(genLineGui(endL, end, 0.01, color))
    BigWorld.callback(maxDelayTime, Functor(delDebugGui, lineList))


def getRadianPoints(centerPos, radii, radian, height, yaw, step):
    theta = radian * 180 / math.pi
    points = [centerPos]
    stepR = theta * 2 / step
    for i in xrange(step):
        points.append(utils.getRelativePosition(centerPos, yaw, -theta + stepR * i, radii))

    points.append(utils.getRelativePosition(centerPos, yaw, theta, radii))
    return points


def isAltDown():
    return BigWorld.getKeyDownState(keys.KEY_RALT, 0) or BigWorld.getKeyDownState(keys.KEY_LALT, 0)


def getMatrialsName(entity, data):
    dye = data.get('materials', ('DefaultMatter', None))
    if dye:
        if type(dye) == tuple:
            if getattr(entity, 'model', None):
                entity.model.newFxName = dye[1]
            tintName = dye[0]
        else:
            tintName = dye
    return tintName


def getFlyRideMatrialsName(data):
    return data.get('flyRideMaterial')


physicsPart = ['body', 'hair', 'leg']

def setModelPhysics(model):
    global physicsPart
    if not model or not model.inWorld:
        return
    for part in physicsPart:
        setattr(model, part + 'Physics', None)

    if gameglobal.rds.GameState <= gametypes.GS_LOGIN:
        return
    if gameglobal.gDisableBulletPhy and gameglobal.rds.GameState > gametypes.GS_LOGIN:
        return
    if hasattr(BigWorld, 'BulletRope'):
        for part in physicsPart:
            if getattr(model, part + 'Physics', None):
                continue
            for path in model.sources:
                if path.endswith(part + '.model'):
                    phyPath = path.split('.')[0] + '.phy'
                    if isFileExist(phyPath):
                        phy = BigWorld.BulletRope(phyPath)
                        setattr(model, part + 'Physics', phy)
                        if not getattr(gameglobal.rds, 'enableModelPhysics', True):
                            getattr(model, part + 'Physics').enable = False
                        break


def resetModelPhysics(model):
    if gameglobal.gDisableBulletPhy:
        return
    if not getattr(gameglobal.rds, 'enableModelPhysics', True):
        return
    for part in physicsPart:
        phy = getattr(model, part + 'Physics', None)
        if phy:
            phy.reset()


def enableModelPhysics(model, enable):
    if gameglobal.gDisableBulletPhy:
        return
    gameglobal.rds.enableModelPhysics = enable
    for part in physicsPart:
        phy = getattr(model, part + 'Physics', None)
        if phy:
            phy.enable = enable


def isFileExist(path):
    return ResMgr.fileExist(path)


gPlayerIsFader = False

def cameraTooCloseNotify(isTooClose):
    global gPlayerIsFader
    if not gameglobal.NEED_CAMERA_NOTIFY:
        return
    if gameglobal.rds.GameState != gametypes.GS_PLAYGAME:
        return
    p = BigWorld.player()
    if not p.model.visible:
        return
    if p.inCombat:
        return
    cameraVersion = None
    if not gameglobal.rds.configData.get('enableNewCamera', False):
        cameraVersion = gameglobal.rds.ui.camera
    else:
        cameraVersion = gameglobal.rds.ui.cameraV2
    if isTooClose and not gPlayerIsFader and not cameraVersion.isShow:
        setPlayerIsFader(True)
        gameglobal.rds.cam.handleMouseEvent(0, 0, 120)
        BigWorld.callback(0.1, Functor(setPlayerIsFader, False))


def setPlayerIsFader(isFader):
    global gPlayerIsFader
    gPlayerIsFader = isFader


def getModeNodePosition(model, nodeName, forceUpdate = True):
    position = None
    try:
        position = model.node('Scene Root').position
    except:
        eid = getattr(model, 'entityId', -1)
        entity = BigWorld.entity(eid)
        p = BigWorld.player()
        if entity == p:
            spaceNo = getattr(p, 'spaceNo', 0)
            msg = 'model has no Scene Root node,%s %s %s %d %s %s' % (str(eid),
             str(entity),
             str(model.position),
             spaceNo,
             str(p.position),
             str(model.sources))
            p.reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_SCRIPT, [msg], 0, {})

    try:
        node = model.node(nodeName)
    except:
        return position

    if node:
        origForceUpdate = node.forceUpdate
        node.forceUpdate = forceUpdate
        position = node.position
        node.forceUpdate = origForceUpdate
    return position


def getPositionByNode(node):
    try:
        node.forceUpdate = True
        position = node.position
        node.forceUpdate = False
    except:
        position = node.position

    return position


SYS_ALLOW_EFFECT_PRIORITY = gameglobal.EFF_LOWEST_PRIORITY

def getEffectPriority():
    global SYS_ALLOW_EFFECT_PRIORITY
    return SYS_ALLOW_EFFECT_PRIORITY


def allowLowerPriority():
    global SYS_ALLOW_EFFECT_PRIORITY
    if SYS_ALLOW_EFFECT_PRIORITY < gameglobal.EFF_LOWEST_PRIORITY:
        SYS_ALLOW_EFFECT_PRIORITY = SYS_ALLOW_EFFECT_PRIORITY + 1


def highAllowEffectPriority():
    global SYS_ALLOW_EFFECT_PRIORITY
    if SYS_ALLOW_EFFECT_PRIORITY > gameglobal.EFF_HIGHEST_PRIORITY + 1:
        SYS_ALLOW_EFFECT_PRIORITY = SYS_ALLOW_EFFECT_PRIORITY - 1


def getRelativePosition(pos, yaw, theta, dist):
    x = pos[0] + dist * math.sin(yaw + theta * math.pi / 180)
    z = pos[2] + dist * math.cos(yaw + theta * math.pi / 180)
    return (x, pos[1], z)


def getLeftUpperIK():
    ik = BigWorld.UpperLimbIK('left')
    ik.reachSpeed = 1.5
    ik.clavicleBoneName = 'biped L Clavicle'
    ik.foreArmBoneName = 'biped L ForeTwist1'
    ik.handBoneName = 'biped L Hand'
    ik.upperArmBoneName = 'biped L UpperArm'
    ik.touchNodeName = 'HP_hand_left_1'
    return ik


def getRightUpperIK():
    ik = BigWorld.UpperLimbIK('right')
    ik.reachSpeed = 1.5
    ik.clavicleBoneName = 'biped R Clavicle'
    ik.foreArmBoneName = 'biped R ForeTwist1'
    ik.handBoneName = 'biped R Hand'
    ik.upperArmBoneName = 'biped R UpperArm'
    ik.touchNodeName = 'HP_hand_right_1'
    return ik


def randomChoiceByProportion(arr, pro):
    if len(arr) == 0 or len(arr) != len(pro) or sum(pro) != 1.0:
        return None
    rd = random.random()
    lst = 0.0
    for i in xrange(len(arr)):
        if rd <= lst + pro[i]:
            return arr[i]
        lst += pro[i]


def uploadFileToNos(md5, timeStamp, filePath, fileType, fileSrc, extra, callback):
    remoteInterface.uploadFileToNos(md5, timeStamp, filePath, fileType, fileSrc, extra, callback)


def downloadFileFromNos(directory, key, fileType, status, callback):
    remoteInterface.downloadFileFromNos(directory, key, fileType, status, callback)


def downloadFileFromYixin(account, urlPath, callback):
    remoteInterface.downloadFileFromYixin(account, urlPath, callback)


def uploadSound(actionType, filePath, extra, callback):
    remoteInterface.uploadSound(actionType, filePath, extra, callback)


def downloadSound(actionType, key, extra, callback):
    remoteInterface.downloadSound(actionType, key, extra, callback)


def getTranslation(actionType, key, extra, callback):
    remoteInterface.getTranslation(actionType, key, extra, callback)


def getMacAddress():
    macAddress = []
    try:
        for mac in BigWorld.get_mac_addr():
            macAddress.append(mac[1])

    except:
        pass

    return macAddress


def resetLimitFps(isLoading = False):
    limitForegroundFPS = int(gameglobal.FORGROUND_FPS) if gameglobal.FORGROUND_FPS < gameglobal.LIMIT_MAX_FPS else 1000
    limitBackgroundFPS = int(gameglobal.BACKGROUND_FPS) if gameglobal.BACKGROUND_FPS < gameglobal.LIMIT_MAX_FPS else 1000
    p = BigWorld.player()
    if isLoading or gameglobal.rds.GameState == gametypes.GS_LOADING:
        limitBackgroundFPS = gameglobal.LOADING_LIMIT_FPS
    elif hasattr(p, 'checkInAutoQuest'):
        if p.checkInAutoQuest():
            limitBackgroundFPS = max(limitBackgroundFPS, gameglobal.AUTOQUEST_LIMIT_FPS)
    limitForegroundFPS = max(limitForegroundFPS, 30)
    BigWorld.limitForegroundFPS(limitForegroundFPS)
    BigWorld.limitBackgroundFPS(limitBackgroundFPS)


def needDoOptimize():
    try:
        p = BigWorld.player()
        if p.isRealInFuben():
            return False
        spaceNo = getattr(p, 'spaceNo', 0)
        mapId = formula.getMapId(spaceNo)
        syncStateOptimize = p.inClanWar or MCD.data.get(mapId, {}).get('syncStateOptimize', False) or p.inWorldWarEx() or mapId in const.PVP_ARENA or p.inWingCity()
    except:
        return False

    return syncStateOptimize


def needAvatarCntOptimize():
    try:
        p = BigWorld.player()
        if p.isRealInFuben():
            return False
        spaceNo = getattr(p, 'spaceNo', 0)
        mapId = formula.getMapId(spaceNo)
        avatarCntOptimize = p.inClanWar or MCD.data.get(mapId, {}).get('syncAvatarCntOptimize', False) or p.inWorldWarEx() or mapId in const.PVP_ARENA or p.inWingCity()
    except:
        return False

    return avatarCntOptimize


def quitGameByNeprot(exitType):
    msgInfo = ''
    if exitType == gameglobal.EXIT_MAX_CLIENT:
        msgInfo = '游戏客户端超过限定数量，即将关闭'
    elif exitType == gameglobal.EXIT_ACCELERATOR:
        msgInfo = '系统检测到你使用变速齿轮类软件，游戏即将关闭'
    if msgInfo:
        BigWorld.msgBox(msgInfo)
    BigWorld.quit()


def isPbrEquip(equipId):
    return True


def isPbrModel(modelId):
    return True


def isNewSkinModel(modelId, subModelId):
    if gameglobal.APPLY_NEW_SKIN_MODEL:
        return True
    newSkinModel = SCD.data.get('%d_NewSkinModel' % modelId, [])
    if subModelId in newSkinModel:
        return True
    return False


def isTransparentModel(modelId, subModelId):
    if not gameglobal.rds.configData.get('enableEquipTransparenceDye', True):
        return False
    transparentModel = SCD.data.get('%d_TransparentModel' % modelId, [])
    if subModelId in transparentModel:
        return True
    return False


def getNewXrjmModelPath(school):
    path = 'char/10000/intro/%s/base.model' % school
    return {'fullPath': path}


def getLoginModelNewPath(school):
    return {'fullPath': 'char/10000/login/%s/base.model' % school}


def fetchTintEffectsContents(ownerId, callback):
    if gameglobal.gDisableNewTint or not hasattr(ResMgr, 'bkgTintEffects'):
        callback(ownerId, {}, [])
        return
    en = BigWorld.entities.get(ownerId)
    mpr = None
    if hasattr(en, 'avatarInfo') and en.avatarInfo:
        mpr = charRes.convertToMultiPartRes(en.avatarInfo, ownerId)
    else:
        mpr = charRes.MultiPartRes()
        mpr.queryByAvatar(en)
    en.tintAvatarTas = {}
    tintAvatarTas, tintAvatarName = getTintAvatarTas(mpr)
    fetchTintTas = []
    for key in tintAvatarTas:
        fetchTintTas.append(tintAvatarTas[key])

    ResMgr.bkgTintEffects(Functor(callback, ownerId, tintAvatarTas, tintAvatarName), fetchTintTas)


def tintSectionsToCache(entity, tintAvatarTas, tintAvatarName, tintEffects):
    if not tintEffects:
        return
    index = 0
    for key in tintAvatarTas:
        try:
            tintAvatarTas[key] = tintEffects[index]
        except:
            tintAvatarTas[key] = None

        index += 1

    entity.tintAvatarTas = tintAvatarTas
    entity.tintAvatarName = tintAvatarName


def getTintAvatarTas(mpr):
    tintAvatarTas = {}
    tintAvatarName = {}
    sex = mpr.sex
    bodyType = mpr.bodyType
    modelId = charRes.transRealBodyType(sex, bodyType, mpr.body)
    isNewSkin = isNewSkinModel(modelId, mpr.body)
    isTransparent = isTransparentModel(modelId, mpr.body)
    if isNewSkin:
        tint = 'avatarSkinEquip'
        if TA.TAs.has_key('avatarSkinBare'):
            tintAvatarTas['skin'] = TA.TAs['avatarSkinBare'][1]
            tintAvatarName['skin'] = 'avatarSkinBare'
    else:
        tint = 'avatarSkin'
    for part in charRes.PARTS_ASPECT_BODY:
        partValue = getattr(mpr, part, charRes.PART_NOT_NEED)
        if not (partValue == None or partValue < 0):
            if TA.TAs.has_key(tint):
                tintAvatarTas[part] = TA.TAs[tint][1]
                tintAvatarName[part] = tint
                if isTransparent and TA.TAs.has_key('avatarSkinTrans'):
                    tintAvatarTas['%s2' % part] = TA.TAs['avatarSkinTrans'][1]
                    tintAvatarName['%s2' % part] = 'avatarSkinTrans'

    headType = mpr.headType
    if headType in (charRes.HEAD_TYPE0, charRes.HEAD_TYPE2):
        if TA.TAs.has_key('avatarHead' + str(sex)):
            tintAvatarTas['head'] = TA.TAs['avatarHead' + str(sex)][1]
            tintAvatarName['head'] = 'avatarHead' + str(sex)
        if TA.TAs.has_key('avatarEye'):
            tintAvatarTas['eye'] = TA.TAs['avatarEye'][1]
            tintAvatarName['eye'] = 'avatarEye'
        if TA.TAs.has_key('avatarHair'):
            tintAvatarTas['hair'] = TA.TAs['avatarHair'][1]
            tintAvatarName['hair'] = 'avatarHair'
        if TA.TAs.has_key('avatarEyelash'):
            tintAvatarTas['eyelash'] = TA.TAs['avatarEyelash'][1]
            tintAvatarName['eyelash'] = 'avatarEyelash'
    return (tintAvatarTas, tintAvatarName)


def fetchSimpleTintEffectsContents(ownerId, threadID, itemData, finishcall, callback):
    if gameglobal.gDisableNewTint or not hasattr(ResMgr, 'bkgTintEffects'):
        callback(ownerId, threadID, itemData, finishcall, {}, [])
        return
    mpr = charRes.convertToMultiPartRes(itemData, ownerId)
    tintAvatarTas, tintAvatarName = getTintAvatarTas(mpr)
    fetchTintTas = []
    for key in tintAvatarTas:
        fetchTintTas.append(tintAvatarTas[key])

    ResMgr.bkgTintEffects(Functor(callback, ownerId, threadID, itemData, finishcall, tintAvatarTas, tintAvatarName), fetchTintTas)


def fetchExtraTintEffectsContents(model, tintName, param, time, matter, force, applyLater, effectHost, effectOwner, tintType, callback):
    if not model:
        return
    if gameglobal.gDisableNewTint or not hasattr(ResMgr, 'bkgTintEffects') or not tintName:
        callback(model, tintName, param, time, matter, force, applyLater, effectHost, effectOwner, tintType, {}, [])
        return
    tintAvatarTas = {tintName: TA.TAs[tintName][1]}
    fetchTintTas = []
    for key in tintAvatarTas:
        fetchTintTas.append(tintAvatarTas[key])

    ResMgr.bkgTintEffects(Functor(callback, model, tintName, param, time, matter, force, applyLater, effectHost, effectOwner, tintType, tintAvatarTas), fetchTintTas)


def afterFetchTintEffectContents(model, tintName, param, time, matter, force, applyLater, effectHost, effectOwner, tintType, tintAvatarTas, tintEffects):
    if not model or not model.inWorld:
        return
    index = 0
    for key in tintAvatarTas:
        try:
            tintAvatarTas[key] = tintEffects[index]
        except:
            tintAvatarTas[key] = None

        index += 1

    model.tintCopy = tintAvatarTas
    TA.ta_add([model], tintName, param, time, matter, force, applyLater, effectHost, effectOwner, tintType)
    TA.clearTintCopy(model.tintCopy)
    model.tintCopy = None


def fetchTintEffectContentsByName(tintNames, callback):
    if gameglobal.gDisableNewTint or not hasattr(ResMgr, 'bkgTintEffects') or not tintNames:
        callback([])
        return
    tintAvatarTas = {}
    fetchTintTas = []
    for tintName in tintNames:
        fetchTintTas.append(TA.TAs[tintName][1])
        tintAvatarTas[tintName] = TA.TAs[tintName][1]

    ResMgr.bkgTintEffects(callback, fetchTintTas)


class CameraTrackCache(object):

    def __init__(self):
        self.cache = {}

    def loadCameraTrack(self, trackName):
        if not self.cache.has_key(trackName):
            track = ResMgr.openSection(trackName, False)
            self.cache[trackName] = track
        return self.cache.get(trackName, None)


cameraTrackCache = CameraTrackCache()

def loadCameraTrack(trackName):
    return cameraTrackCache.loadCameraTrack(trackName)


def openForceUrl():
    enableForceOpenUrl = gameglobal.rds.configData.get('enableForceOpenUrl', True)
    if enableForceOpenUrl and gameglobal.rds.GameState > gametypes.GS_LOGON:
        urlPath = SCD.data.get('exitOpenUrl', None)
        if urlPath:
            urlPath += '?timeStamp=' + str(int(time.time()))
            BigWorld.openUrl(urlPath)


def genCameraShareUrl(fileKey):
    if gameglobal.rds.configData.get('enableNOSCDNDeploy', False) and hasattr(BigWorld, 'httpDownloadFileNew'):
        host = gameglobal.rds.configSect.readString('nos/host', 'nos.netease.com')
        u = urllib.quote('/' + fileKey)
    else:
        host = 'nos.netease.com'
        account = gameglobal.rds.configSect.readString('nos/account')
        u = urllib.quote('/' + account + '/' + fileKey)
    return (host, u)


def attachFashionEffect(entity, model, aspect = None):
    fxs = []
    if not aspect and hasattr(entity, 'realAspect'):
        aspect = entity.realAspect
    if aspect:
        modelId = 0
        if hasattr(entity, 'realPhysique'):
            modelId = charRes.transBodyType(entity.realPhysique.sex, entity.realPhysique.bodyType)
        for partName in charRes.PARTS_ASPECT_FASHION:
            partId = getattr(aspect, partName, 0)
            if partId:
                data = ED.data.get(partId, {})
                effects = data.get('effect', ())
                bodyTypeEffect = data.get('bodyTypeEffect', {}).get(modelId, ())
                for effectId in effects + bodyTypeEffect:
                    fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (entity.getEquipEffectLv(),
                     entity.getEquipEffectPriority(),
                     model,
                     effectId,
                     sfx.EFFECT_LIMIT_MISC))
                    if fx:
                        fxs.extend(fx)

    return fxs


def previewEffect(entity, itemId):
    dustId = ED.data.get(itemId, {}).get('footDust', None)
    if dustId:
        entity.fashion.footTriggerMgr.setPreviewDustId(dustId)
        return
    fireworksId = CID.data.get(itemId, {}).get('fireworksId', None)
    if fireworksId:
        entity.doFireworks(fireworksId, 8)
        return


filePath = '../planb.txt'

def enablePlanb():
    cc = BigWorld.CursorCamera()
    if not hasattr(cc, 'needfixCamera'):
        return False
    try:
        with open(filePath, 'r') as f:
            line = f.read()
            if line:
                args = line.split(',')
                if len(args) >= 3:
                    if random.randint(1, 100) < int(args[2]):
                        return True
            return False
    except:
        return False


def enableBinkLogoCG():
    try:
        if '32Bit' in BigWorld.getOSDesc():
            return False
        if not hasattr(BigWorld, 'PyBinkMovie'):
            return False
        return True
    except:
        return False


def enableUILazyInit():
    try:
        with open(filePath, 'r') as f:
            line = f.read()
            if line:
                args = line.split(',')
                if len(args) >= 5:
                    if random.randint(0, 99) < int(args[4]):
                        return True
            return False
    except:
        return False


def useCEFLogin():
    try:
        with open(filePath, 'r') as f:
            line = f.read()
            if line:
                args = line.split(',')
                if len(args) >= 9:
                    rand = random.randint(0, 99)
                    if rand < int(args[8]):
                        return True
            return False
    except:
        return False


def enableNewLoginScene():
    try:
        with open(filePath, 'r') as f:
            line = f.read()
            if line:
                args = line.split(',')
                if len(args) >= 10:
                    rand = random.randint(0, 99)
                    if rand < int(args[9]):
                        return False
            gamelog.debug('ypc@ enableCharacterSelectNew file error!')
            return True
    except:
        gamelog.debug('ypc@ enableCharacterSelectNew file error!')
        return True


def enableExtendChatBox():
    if '32Bit' in BigWorld.getOSDesc():
        return False
    if not hasattr(BigWorld, 'setWindowAlpha'):
        return False
    return gameglobal.rds.configData.get('enableExtendChatBox', False)


def setTuZhuangConfig(itemId, model, dyeList):
    if dyeList and model:
        if tuZhuangDyeMorpher.checkDyes(dyeList):
            dyeMorpher = tuZhuangDyeMorpher.TuZhuangDyeMorpher(model)
            dyeTint = TED.data.get(itemId, {}).get('dyeTint', None)
            dyeMorpher.read(dyeList, dyeTint)
            dyeMorpher.syncApply()
        else:
            tintalt.ta_set_static([model], dyeList)


def filterNpcNeedHighlight(ent):
    className = ent.__class__.__name__
    return className.find('Npc') != -1 or className == 'Dawdler' or className == 'HomeFurniture'


_DEFAULT_HIGHLIGHT_EFFECT = 50662
_DEFAULT_HIGHLIGHT_EFFECT_SCALE = 5.0

def highlightEntity(ent, bShow = True, effectId = _DEFAULT_HIGHLIGHT_EFFECT):
    if not filterNpcNeedHighlight(ent):
        return
    if not bShow:
        ent.removeFx(effectId)
        return
    if effectId in ent.attachFx:
        return
    nmcd = NMCD.data.get(ent.npcId, {})
    effScale = nmcd['effScale'] if nmcd.has_key('effScale') else nmcd.get('modelScale', 1)
    effScale *= _DEFAULT_HIGHLIGHT_EFFECT_SCALE
    fxs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (gameglobal.EFFECT_LOW,
     ent.getBasicEffectPriority(),
     ent.model,
     effectId,
     sfx.EFFECT_UNLIMIT))
    if fxs:
        for fx in fxs:
            fx.scale(effScale, effScale, effScale)

        ent.addFx(effectId, fxs)


def highlightNpcNearby(effectId = _DEFAULT_HIGHLIGHT_EFFECT):
    ents = BigWorld.entities.values()
    bHighlight = gameglobal.GM_NPC_HIGHLIGHT_ALL
    for e in ents:
        highlightEntity(e, bHighlight, effectId)


def enableNewSchoolYeCha():
    return gameglobal.rds.configData.get('enableNewSchoolYeCha', False) or getattr(gameglobal.rds, 'applyOfflineCharShowData', False)


def enableNewSchoolMiaoYin():
    return gameglobal.rds.configData.get('enableNewSchoolMiaoyin', False) or getattr(gameglobal.rds, 'applyOfflineCharShowData', False)


def enableNewSchoolTianZhao():
    return gameglobal.rds.configData.get('enableNewSchoolTianZhao', False) or getattr(gameglobal.rds, 'applyOfflineCharShowData', False)


def bfDotaAoIInfinity():
    return hasattr(BigWorld.player(), 'isInBfDota') and BigWorld.player().isInBfDota() and gameglobal.rds.configData.get('bfDotaAoIInfinity', False)


def enalbePreOpenCEF():
    return not BigWorld.isPublishedVersion() or gameglobal.rds.configData.get('enablePreOpenCEF', False)


def isCoupleWear(wearId1, wearId2):
    coupleWear = SCD.data.get('coupleWear', {})
    if coupleWear:
        from item import Item
        wearId1 = Item.parentId(wearId1)
        wearId2 = Item.parentId(wearId2)
        if wearId2 in coupleWear.get(wearId1, []) or wearId1 in coupleWear.get(wearId2, []):
            return True
    return False


def setModelIgnoreTpos(model):
    if not gameglobal.rds.configData.get('enableNeedIgnoreTpos', True):
        return
    if not model:
        return
    if getattr(model, 'dummyModel', False):
        return
    model.needIgnoreTpos = True
    BigWorld.callback(0.5, Functor(checkModelIgnoreTposState, model))


def checkModelIgnoreTposState(model):
    if not model.needIgnoreTpos:
        return
    if len(model.queue) <= 0:
        model.needIgnoreTpos = False


def uploadfile(localpath, fileName):
    ftp = FTP()
    ftp.connect('10.246.46.103', 30021)
    ftp.login('pg', 'JT2oNeSbmsERk')
    bufsize = 1024
    ftp.cwd('./zhou_feng/')
    fp = open(localpath, 'rb')
    ftp.storbinary('STOR ' + fileName, fp, bufsize)
    ftp.set_debuglevel(0)
    fp.close()


def enableTopLogoOptimize():
    return True


def isInDotaZaiju(avatar):
    if avatar.bianshen[0] == gametypes.BIANSHEN_ZAIJU:
        data = ZJD.data.get(avatar.bianshen[1], {})
        if data.get('isDotaZaiju', 0):
            return True
    return False


def setDotaEntityBlood(entity):
    p = BigWorld.player()
    if p.isInBfDota():
        if entity and hasattr(entity, 'topLogo'):
            visible = entity.hp < entity.mhp if entity.hp > 0 else False
            if utils.instanceof(entity, 'Monster'):
                entity.topLogo.showMonsterBlood(visible)


def getShowNpcCnt():
    p = BigWorld.player()
    entities = BigWorld.entities.values()
    cnt = 0
    for entity in entities:
        if entity.__class__.__name__ in ('Npc', 'Dawdler'):
            opacityValue = entity.getOpacityValue()
            if opacityValue[0] == gameglobal.OPACITY_FULL:
                cnt += 1

    return cnt


def getNpcModelMaxCnt():
    baseCnt = gameglobal.rds.configData.get('getNpcModelMaxCnt', 150)
    videoSettingLv = appSetting.VideoQualitySettingObj.getVideoQualityLv()
    if videoSettingLv == 2:
        baseCnt = baseCnt * 1.6
    elif videoSettingLv >= 3:
        baseCnt = baseCnt * 1.96
    return baseCnt


def setEntityHideBloodNumState(entity, isHideBloodNum):
    oldState = getattr(entity, 'isHideBloodNum', False)
    if oldState != isHideBloodNum:
        entity.isHideBloodNum = isHideBloodNum
        if hasattr(entity, 'topLogo'):
            entity.topLogo.setHideBloodNumState(isHideBloodNum)
        gameglobal.rds.ui.target.setHideBloodState()
        gameglobal.rds.ui.bossBlood.setHideBloodNumState()
        gameglobal.rds.ui.focusTarget.refreshHideBloodState()
        gameglobal.rds.ui.subTarget.setHideBloodNumState()


def deleteFile():
    ftp = FTP()
    ftp.connect('10.246.46.103', 30021)
    ftp.login('pg', 'JT2oNeSbmsERk')
    bufsize = 1024
    ftp.cwd('./snail/')
    fileNames = ftp.nlst()
    for name in fileNames:
        if '@163.com' in name or '@126.com' in name or '@qq.com' in name or '-2017-' in name:
            print name
            ftp.delete(name)


def enableMicroprofile(value):
    if hasattr(BigWorld, 'enableMicroprofile'):
        BigWorld.enableMicroprofile(value)
        return value
    return -1


def dumpAndUploadMicroprofile(md5, timeStamp):
    if not hasattr(BigWorld, 'dumpMicroprofile'):
        return -1
    p = BigWorld.player()
    date = time.strftime('%Y%m%d%H%M%S')
    fileName = '%s_%s.html' % ('microprofile', date)
    BigWorld.dumpMicroprofile(fileName)
    data = None
    with open(fileName, 'rb') as file:
        data = file.read()
    with gzip.open('%s.gz' % fileName, 'wb') as wfile:
        wfile.write(data)
    p.uploadNOSFile('../game/%s.gz' % fileName, gametypes.NOS_FILE_DUMP, gametypes.NOS_FILE_SRC_MICROPROFILE, {'gbId': p.gbId,
     'type': 'microprofile',
     'md5': (md5, timeStamp)})
    return 'OK'


def diableFxLoad(val):
    gameglobal.DISABLE_FX_LOAD = val
    return val


def enableLRUCache():
    return not BigWorld.isPublishedVersion() or gameglobal.rds.configData.get('enableLRUCache', False)


def getEntityLingShiOpacityValue(data):
    p = BigWorld.player()
    if data['islingshi'] == gametypes.LINGSHI_STATE_VISIBLE_ONLY:
        if getattr(p, 'lingShiFlag', True):
            return (gameglobal.OPACITY_FULL, True)
        else:
            return (gameglobal.OPACITY_HIDE, False)
    elif data['islingshi'] == gametypes.LINGSHI_STATE_HIDE_ONLY:
        if getattr(p, 'lingShiFlag', True):
            return (gameglobal.OPACITY_HIDE, False)
        else:
            return (gameglobal.OPACITY_FULL, True)


def uploadGameFile(md5, timeStamp, fileName):
    p = BigWorld.player()
    import os
    if not os.path.exists(fileName):
        return 'FileNotExsist'
    data = None
    with open(fileName, 'rb') as file:
        data = file.read()
    with gzip.open('%s.gz' % fileName, 'wb') as wfile:
        wfile.write(data)
    p.uploadNOSFile('../game/%s.gz' % fileName, gametypes.NOS_FILE_DUMP, gametypes.NOS_FILE_SRC_GAMEFILE, {'gbId': p.gbId,
     'type': 'gamefile',
     'md5': (md5, timeStamp)})
    return 'OK'


def getEquipPart(equipItem):
    p = BigWorld.player()
    for i, item in enumerate(p.equipment):
        if item and item.uuid == equipItem.uuid:
            return i

    for pos in gametypes.EQU_PART_SUB:
        item = commcalc.getAlternativeEquip(p, pos)
        if item and item.uuid == equipItem.uuid:
            return pos

    return -1
