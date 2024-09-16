#Embedded file name: /WORKSPACE/data/entities/client/helpers/capturephoto.o
import math
import copy
import os
import weakref
from PIL import Image
import BigWorld
import ResMgr
import GUI
import Math
import Pixie
import Scaleform
import gameglobal
import clientcom
import gamelog
import gametypes
import const
import clientUtils
from sfx import sfx
from item import Item
from helpers import tintalt as TA
from gameclass import Singleton
from callbackHelper import Functor
from helpers import charRes
from helpers import modelServer
from guis.zhanQiMorpherFactory import ZhanqiDyeMorpher
from data import equip_data as ED
from data import summon_sprite_info_data as SSID
LARGE_PHOTO_PATH = 'config/largephoto.xml'
SMALL_PHOTO_PATH = 'config/smallphoto.xml'
SKILL_PHOTO_PATH = 'config/skillphoto.xml'
PLAYER_PHOTO_PATH = 'config/playerphoto.xml'
TARGET_PHOTO_PATH = 'config/targetphoto.xml'
RIDE_PHOTO_PATH = 'config/ridephoto.xml'
FITTING_PHOTO_PATH = 'config/fittingphoto.xml'
NPC_PHOTO_PATH = 'config/npcphoto.xml'
availableXml = (LARGE_PHOTO_PATH,
 SMALL_PHOTO_PATH,
 SKILL_PHOTO_PATH,
 RIDE_PHOTO_PATH,
 FITTING_PHOTO_PATH,
 NPC_PHOTO_PATH)
photoDict = {}

def reloadPhotoXml():
    global photoDict
    for xml in availableXml:
        if not photoDict.has_key(xml):
            photoDict[xml] = ResMgr.openSection(xml)


DefaultLight = 8542950
DefaultLight2 = 15127200
LightDir = [-2.5, 4, 5]
LightExposure = [0.3, 0.7]

class BasePhotoGen(object):

    def __init__(self, mask, size, flashResName, phtoPath):
        self.image = None
        self.adaptor = GUI.MeshAdaptor(mask, 0)
        self.aaScale = 1.5
        self.adaptor.setSize(int(self.aaScale * size))
        self.adaptor.modelAlpha = True
        self.adaptor.mixTextureAlpha = False
        self.adaptor.photoFov = 1
        self.adaptor.flashResName = flashResName
        self.adaptor.flashWidth = size
        self.adaptor.flashHeight = size
        self.size = size
        self.dynamic = False
        self.path = phtoPath
        self.matrixData = photoDict.get(self.path, None)
        self.modelId = None
        self.action = None
        self.realHeight = None
        self.light = DefaultLight
        self.light2 = DefaultLight2
        self.light2Dir = LightDir
        self.exposure = LightExposure
        self.callback = None
        self.needAction = True
        self.needLoadAction = True
        self.attachedModel = []
        self.tintMs = None
        self.zoomScale = 1
        self.extraInfo = {}
        self.modelFinishCallback = None
        self.equipEnhanceEffects = []
        self.needXuarn = True
        self.cfType = const.SHADER_TYPE_F

    def setModelFinishCallback(self, func):
        self.modelFinishCallback = func

    def getUIExt(self):
        if gameglobal.rds.ui.isUIPublished():
            return '.gfx'
        else:
            return '.swf'

    def setModel(self, modelId, addedModel = None, attaches = None):
        if self.modelId == modelId:
            return True
        if modelId == 0:
            return self.setAvatar(BigWorld.player())
        self.clearModel()
        self.modelId = modelId
        gamelog.debug('jjh@photo setModel', modelId, self.adaptor.attachment, addedModel, attaches)
        if modelId == None:
            return False
        if addedModel:
            model = addedModel
            self.afterModelFinished(modelId, attaches, model)
        else:
            clientcom.fetchModel(gameglobal.URGENT_THREAD, Functor(self.afterModelFinished, modelId, attaches), modelId)

    def afterModelFinished(self, modelId, attaches, model):
        if modelId != self.modelId or self.modelId == None:
            model = None
            return
        if not model:
            return
        if hasattr(model, 'texturePriority'):
            model.texturePriority = 100
        clientcom.setModelIgnoreTpos(model)
        if self.matrixData and self.matrixData.has_key(str(modelId)):
            dataSect = self.matrixData[str(modelId)]
            matrix = dataSect.readMatrix('view')
        else:
            matrix = self.getDefaultMatrix(model)
        self.adaptor.transform = matrix
        model.soundCallback(self.actionCueCallback)
        self.adaptor.attachment = model
        p = BigWorld.player()
        clientcom.getHairNode(p, model, False)
        self._attachModelFromData(model, attaches)
        self.actionModel(modelId)
        self.setModelMaterial(self.tintMs)
        self.refresh()
        return True

    def _attachModelFromData(self, model, attaches = None):
        if attaches:
            p = BigWorld.player()
            for attach in attaches:
                modelPrefix = ''
                modelAction = None
                if len(attach) == 6:
                    attachHp, attachModel, attachEff, attachScale, attachEffScale, modelPrefix = attach
                elif len(attach) == 7:
                    attachHp, attachModel, attachEff, attachScale, attachEffScale, modelPrefix, modelAction = attach
                else:
                    attachHp, attachModel, attachEff, attachScale, attachEffScale = attach
                if attachScale <= 0:
                    attachScale = 1
                if not modelPrefix:
                    modelPrefix = 'item/model'
                if attachModel and attachHp:
                    if modelPrefix:
                        modelPath = '%s/%s' % (modelPrefix, attachModel)
                    if modelPrefix.endswith('headdress'):
                        hairNodePath = modelServer.getHairNodeModel(model)
                        charRes.getSimpleModel(hairNodePath, None, Functor(self._afterHairModelFinished, model, attachHp, attachScale, modelPath))
                    else:
                        charRes.getSimpleModel(modelPath, None, Functor(self._afterAttachModelFinished, model, attachHp, attachScale, modelPath, modelAction))
                if attachEff:
                    fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (p.getEquipEffectLv(),
                     p.getEquipEffectPriority(),
                     model,
                     attachEff,
                     sfx.EFFECT_LIMIT_MISC))
                    if fx:
                        for fxItem in fx:
                            fxItem.scale(attachEffScale, attachEffScale, attachEffScale)

    def actionCueCallback(self, cueId, data, actionName):
        if cueId == 34:
            self._playFaceEmote(data, actionName)

    def _playFaceEmote(self, data, actionName):
        model = self.adaptor.attachment
        if not model or not model.inWorld:
            return
        if not hasattr(model, 'morphAnimation'):
            return
        dataList = data.split(':')
        faceActionName = str(dataList[0])
        delay = float(dataList[1])
        blendinTime = float(dataList[2])
        stayTime = float(dataList[3])
        blendoutTime = float(dataList[4])
        blockEyebrow = False
        blockEye = False
        blockLip = False
        if len(dataList) > 7:
            blockEyebrow = bool(dataList[5])
            blockEye = bool(dataList[6])
            blockLip = bool(dataList[7])
        if delay > 0.0:
            BigWorld.callback(delay, Functor(self.playMorphAnimation, model, faceActionName, delay, blendinTime, stayTime, blendoutTime, blockEyebrow, blockEye, blockLip))
        else:
            self.playMorphAnimation(model, faceActionName, delay, blendinTime, stayTime, blendoutTime, blockEyebrow, blockEye, blockLip)

    def playMorphAnimation(self, model, faceActionName, delay, blendinTime, stayTime, blendoutTime, blockEyebrow, blockEye, blockLip):
        suspends = []
        if blockEyebrow:
            suspends.extend(const.EYE_BROW_BONES)
        if blockEye:
            suspends.extend(const.EYELID_BONES)
        if blockLip:
            suspends.extend(const.LIP_BONES)
        try:
            model.boneScale.suspend(*suspends)
        except:
            pass

        model.morphAnimation(1, faceActionName, delay, blendinTime, stayTime, blendoutTime, self.playFaceEmoteCallback)

    def playFaceEmoteCallback(self):
        model = self.adaptor.attachment
        if not model or not model.inWorld:
            return
        model.unsuspendMorphs(1)
        try:
            model.boneScale.unsuspend()
        except:
            pass

    def _afterHairModelFinished(self, bodyModel, attachHp, attachScale, modelPath, hairModel):
        if not bodyModel or not bodyModel.inWorld:
            return
        if hairModel:
            node = bodyModel.node('biped Head')
            if node and hairModel not in node.attachments:
                node.attach(hairModel, 'biped Head')
                callback = Functor(self._afterAttachModelFinished, hairModel, attachHp, attachScale, modelPath, None)
                charRes.getSimpleModel(modelPath, None, callback)

    def _afterAttachModelFinished(self, bodyModel, attachHp, attachScale, modelPath, attachAct, model):
        if not bodyModel:
            return
        if not model:
            return
        try:
            bodyModel.setHP(attachHp, None)
            bodyModel.setHP(attachHp, model)
            bodyModel.node(attachHp).scale(attachScale, attachScale, attachScale)
            model.texturePriority = 100
            self.attachedModel.append(model)
            if attachAct:
                actionName = str(attachAct)
                if actionName in model.actionNameList():
                    model.action(actionName)()
        except:
            return

    def setModelMaterial(self, tintMs):
        if tintMs and tintMs != 'Default' and self.adaptor.attachment:
            TA.ta_set_static([self.adaptor.attachment], tintMs)
        if self.addTint:
            TA.ta_add([self.adaptor.attachment], self.addTint)

    def clearModel(self):
        if self.adaptor.attachment:
            TA.ta_reset([self.adaptor.attachment])
            model = self.adaptor.attachment
            if hasattr(model, 'soundCallback'):
                model.soundCallback(None)
            if hasattr(model, 'texturePriority'):
                model.texturePriority = 0
            self.adaptor.attachment = None
            self.adaptor.transform = None
            if hasattr(self.adaptor, 'clear'):
                self.adaptor.clear()
            TA.ta_reset(self.attachedModel)
            for i, model in enumerate(self.attachedModel):
                if hasattr(model, 'texturePriority'):
                    model.texturePriority = 0
                self.attachedModel[i] = None

            self.attachedModel = []

    def setAvatar(self, ent):
        if not ent:
            return False
        modelServer = ent.modelServer
        modelId, bodyModel = modelServer.getMainModelAndID()
        oldSet = set(self.adaptor.attachment.sources) if self.adaptor.attachment else set()
        newSet = set(bodyModel.sources)
        if oldSet == newSet:
            return True
        self.clearModel()
        self.modelId = modelId
        clientcom.fetchAvatarModel(ent, gameglobal.URGENT_THREAD, Functor(self.afterPlayerModelFinished, modelId, ent))

    def afterPlayerModelFinished(self, modelId, ent, model):
        if not model:
            return False
        if modelId != self.modelId or self.modelId == None:
            model = None
            return False
        if hasattr(model, 'bkgLoadTint'):
            model.bkgLoadTint = False
        if hasattr(model, 'texturePriority'):
            model.texturePriority = 100
        matrix = self.getAvatarMatrix(ent, model)
        self.adaptor.transform = matrix
        self.adaptor.attachment = model
        rongGuang = charRes.RongGuangRes()
        if self.extraInfo.has_key('aspect'):
            rongGuang.queryByAttribute(self.extraInfo['aspect'], self.extraInfo.get('showFashion', False))
        else:
            rongGuang.queryByAvatar(ent)
        model.soundCallback(self.actionCueCallback)
        rongGuang.apply(model, self.needXuarn, self.cfType)
        if ent:
            clientcom.getHairNode(ent, model, True)
            clientcom.attachFashionEffect(ent, model, self.extraInfo.get('aspect', None))
        self.actionPlayerModel(modelId, ent)
        self.refresh()
        if self.modelFinishCallback:
            self.modelFinishCallback()
        self.refreshEquipEnhanceEffects(ent, model)
        return True

    def releaseEquipEnhanceEffects(self):
        if self.equipEnhanceEffects:
            for e in self.equipEnhanceEffects:
                if e:
                    e.stop()

        self.equipEnhanceEffects = []

    def refreshEquipEnhanceEffects(self, ent, model):
        if ent.__class__.__name__ not in ('Avatar', 'PlayerAvatar'):
            return
        self.releaseEquipEnhanceEffects()
        effs, eScale = ent.getEquipEnhanceEffects()
        if not effs:
            return
        for ef in effs:
            effLv = ent.getBasicEffectLv()
            priority = ent.getBasicEffectPriority()
            efs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, [effLv,
             priority,
             model,
             ef,
             sfx.EFFECT_UNLIMIT])
            if efs:
                for ef in efs:
                    ef.scale(eScale)

                self.equipEnhanceEffects.extend(efs)

    def actionModel(self, modelId, action = '1101'):
        if not self.needAction:
            return
        model = self.adaptor.attachment
        if not self.action:
            if action not in model.actionNameList():
                action = None
                for item in model.actionNamePair():
                    if item[1].find('idle_a') != -1:
                        action = item[0]
                        break

            if action:
                self.action = [action]
        try:
            if self.action and model:
                l = len(self.action)
                act = model.action(self.action[0])
                for i in xrange(1, l):
                    act = getattr(act(0, None, 0), self.action[i])

                act(0, None, 0)
        except:
            pass

    def actionPlayerModel(self, modelId, ent):
        if not self.needAction:
            return
        model = self.adaptor.attachment
        if not self.action:
            self.action = ['1101']
        try:
            if self.action and model:
                l = len(self.action)
                act = model.action(self.action[0])
                for i in xrange(1, l):
                    act = getattr(act(0, None, 0), self.action[i])

                act(0, None, 0)
        except:
            pass

    def take(self):
        if self.adaptor.attachment == None:
            return
            self.initFlashMesh()
            self.adaptor.setLights(self.light, self.light2)
            self.adaptor.setLightDir(*self.light2Dir)
            self.adaptor.setLightHDR(*self.exposure)
        try:
            self.adaptor.takePhoto(1)
        except:
            pass

    def initFlashMesh(self):
        if not self.adaptor.needDrawToFlash:
            self.adaptor.needDrawToFlash = True
            self.adaptor.drawToFlashFromMesh()

    def refresh(self):
        if self.adaptor.attachment == None:
            return
        self.take()
        if self.dynamic:
            self.callback = BigWorld.callback(0, self.refresh)

    def getDefaultMatrix(self, model):
        m = Math.Matrix()
        m.lookAt((0.35, model.height * 0.78, 1), (-0.3, 0, -1), (0, 1, 0))
        return m

    def getAvatarMatrix(self, ent, model, scale = 1):
        m = Math.Matrix()
        try:
            headHeight = clientcom.getModeNodePosition(model, 'biped Head')[1] - clientcom.getModeNodePosition(model, 'biped R Toe0')[1]
            dist = 0.6
            if headHeight > 0.8:
                dist = 6 / 13.0 * headHeight + 0.23
            m.lookAt((-0.05, headHeight, dist), (-0.05, -0.2, -1), (0, 1, 0))
            return m
        except:
            self.realHeight = model.height
            modelId = self.modelId
            if modelId == 10009:
                m.lookAt((-0.5, self.realHeight * 0.8, 1.5), (0.25, -0.1, -1), (0, 1, 0))
            elif modelId == 10004:
                m.lookAt((-0.1, self.realHeight * 0.85, 0.9), (-0.1, -0.2, -1), (0, 1, 0))
            elif modelId == 10005:
                m.lookAt((-0.1, self.realHeight * 0.9, 1.1), (-0.1, -0.3, -1), (0, 1, 0))
            elif modelId == 10006:
                m.lookAt((-0.05, self.realHeight * 0.9, 0.9), (-0.1, -0.3, -1), (0, 1, 0))
            return m

    def endCapture(self):
        self.setModel(None)
        self.dynamic = False
        try:
            self.adaptor.setSize(16)
        except:
            pass

        self.zoomScale = 1
        self.extraInfo = {}
        self.adaptor.modelYaw = 0
        self.adaptor.photoFov = 1.0

    def startCapture(self, modelId, tintMs, actions = None, addedModel = None, attaches = None, addTint = None):
        if self.callback:
            BigWorld.cancelCallback(self.callback)
        oldDynamic = self.dynamic
        self.action = actions
        self.tintMs = tintMs
        self.dynamic = True
        self.addTint = addTint
        if not oldDynamic:
            try:
                self.adaptor.setSize(int(self.size * self.aaScale))
            except:
                pass

            self.adaptor.drawToFlashFromMesh()
        self.setModel(modelId, addedModel, attaches)
        self.refresh()

    def startCaptureEnt(self, ent, actions = ('1901',)):
        if self.callback:
            BigWorld.cancelCallback(self.callback)
        self.action = actions
        self.dynamic = True
        self.adaptor.setSize(int(self.size * self.aaScale))
        self.adaptor.drawToFlashFromMesh()
        self.setAvatar(ent)
        self.refresh()

    def setModelDirectly(self, entity):
        self.adaptor.attachment = entity.model
        entity.model.setModelNeedHide(False, 1.0)

    def adjustMatrix(self, matrix):
        self.adaptor.transform = matrix

    def adjustLight(self, light1, light2, light2Dir, exposure):
        self.light = (light1[0] << 16) + (light1[1] << 8) + light1[2]
        self.light2 = (light2[0] << 16) + (light2[1] << 8) + light2[2]
        self.light2Dir = light2Dir
        self.exposure = exposure

    def saveData(self, modelID, width, height):
        matrix = self.adaptor.transform
        dataSect = ResMgr.openSection(self.path, True)
        if modelID not in dataSect.keys():
            sect = dataSect.createSection(modelID)
        else:
            sect = dataSect.openSection(modelID)
        sect.writeMatrix('view', matrix)
        sect.writeInt('light', self.light)
        if width and height:
            sect.writeInt('photoWidth', width)
            sect.writeInt('photoHeight', height)
        else:
            sect.deleteSection('photoWidth')
            sect.deleteSection('photoHeight')
        gamelog.debug('bgf:saveData', modelID, matrix, self.light)
        dataSect.save()

    def getInfoFromXML(self, modelId):
        if self.matrixData and self.matrixData.has_key(str(modelId)):
            dataSect = self.matrixData[str(modelId)]
            if dataSect:
                matrix = dataSect.readMatrix('view')
                light = dataSect.readInt('light', DefaultLight)
                return (matrix, light)

    def updateWeapon(self, ent, weapon):
        pass

    def updateWear(self, ent, wear):
        pass

    def rotateYaw(self, deltaYaw):
        self.adaptor.modelYaw += deltaYaw

    def getModelHeight(self, model):
        if not model:
            return 0
        height = 0
        try:
            height = clientcom.getModeNodePosition(model, 'biped Head')[1] - clientcom.getModeNodePosition(model, 'biped R Toe0')[1] + 0.24
        except:
            height = 0

        if height > 0.3:
            return height
        if not hasattr(model, 'bonesBoundingBoxSize'):
            height = model.height
        elif model.bonesBoundingBoxSize[1] <= 0:
            height = model.height
        else:
            height = model.bonesBoundingBoxSize[1]
        return height * model.scale[1]


class NpcPhotoGen(BasePhotoGen):
    __metaclass__ = Singleton


class LargePhotoGen(NpcPhotoGen):

    def __init__(self, mask, size):
        super(LargePhotoGen, self).__init__(mask, size, 'unit4d', LARGE_PHOTO_PATH)
        self.adaptor.swfPath = 'gui/widgets/npcQuestPanel' + self.getUIExt()

    def take(self):
        if self.adaptor.attachment == None:
            return
        try:
            value = gameglobal.rds.configData.get('enableNewFPanelRender', False) or gameglobal.rds.isSinglePlayer
            self.adaptor.takePhoto(1, value)
        except:
            pass

    def afterModelFinished(self, modelId, attaches, model):
        if gameglobal.rds.configData.get('enableNewFPanelRender', False) and hasattr(self.adaptor, 'isNPC'):
            self.adaptor.isNPC = True
        super(LargePhotoGen, self).afterModelFinished(modelId, attaches, model)

    def afterPlayerModelFinished(self, modelId, ent, model):
        if gameglobal.rds.configData.get('enableNewFPanelRender', False) and hasattr(self.adaptor, 'isNPC'):
            self.adaptor.isNPC = not ent == BigWorld.player()
        super(LargePhotoGen, self).afterPlayerModelFinished(modelId, ent, model)


class NpcV2LargePhotoGen(NpcPhotoGen):

    def __init__(self, mask, size, imgSize):
        super(NpcV2LargePhotoGen, self).__init__(mask, size, 'NpcV2_LargePhoto', LARGE_PHOTO_PATH)
        self.adaptor.swfPath = 'gui/widgets/NpcV2Widget' + self.getUIExt()
        self.adaptor.photoFov = 1.4
        self.adaptor.flashWidth = imgSize
        self.adaptor.flashHeight = imgSize

    def afterModelFinished(self, modelId, attaches, model):
        super(NpcV2LargePhotoGen, self).afterModelFinished(modelId, attaches, model)
        if self.modelFinishCallback:
            self.modelFinishCallback()

    def endCapture(self):
        super(NpcV2LargePhotoGen, self).endCapture()
        self.adaptor.photoFov = 1.4


class NpcInteractiveLargePhotoGen(NpcPhotoGen):

    def __init__(self, mask, size, imgSize):
        super(NpcInteractiveLargePhotoGen, self).__init__(mask, size, 'NpcInteractive_LargePhoto', LARGE_PHOTO_PATH)
        self.adaptor.swfPath = 'gui/widgets/NpcInteractiveWidget' + self.getUIExt()
        self.adaptor.photoFov = 1.4
        self.adaptor.flashWidth = imgSize
        self.adaptor.flashHeight = imgSize

    def afterModelFinished(self, modelId, attaches, model):
        super(NpcInteractiveLargePhotoGen, self).afterModelFinished(modelId, attaches, model)
        if self.modelFinishCallback:
            self.modelFinishCallback()

    def endCapture(self):
        super(NpcInteractiveLargePhotoGen, self).endCapture()
        self.adaptor.photoFov = 1.4

    def playTmpAction(self, tmpAction):
        if self.adaptor.attachment and self.action:
            callback = Functor(BigWorld.player().fashion.playActionSequence, self.adaptor.attachment, [self.action[-1]], None)
            BigWorld.player().fashion.playActionSequence(self.adaptor.attachment, [tmpAction], callback)


class NpcV2PhotoGen(NpcPhotoGen):

    def __init__(self, mask, size):
        super(NpcV2PhotoGen, self).__init__(mask, size, 'NpcV2_Photo', NPC_PHOTO_PATH)
        self.adaptor.swfPath = 'gui/widgets/NpcV2Widget' + self.getUIExt()
        self.adaptor.photoFov = 0.3
        self.needAction = False
        self.aaScale = 9
        self.adaptor.setSize(size * self.aaScale)

    def afterModelFinished(self, modelId, attaches, model):
        super(NpcV2PhotoGen, self).afterModelFinished(modelId, attaches, model)
        if self.modelFinishCallback:
            self.modelFinishCallback()


class SmallPhotoGen(NpcPhotoGen):

    def __init__(self, mask, size):
        super(SmallPhotoGen, self).__init__(mask, size, 'AutoQuest_unit7d', SMALL_PHOTO_PATH)
        self.adaptor.swfPath = 'gui/widgets/AutoQuestWidget' + self.getUIExt()


class FubenSmallPhotoGen(NpcPhotoGen):

    def __init__(self, mask, size):
        super(FubenSmallPhotoGen, self).__init__(mask, size, 'unit7d', SMALL_PHOTO_PATH)
        self.adaptor.swfPath = 'gui/widgets/SmallAutoQuestWidget' + self.getUIExt()


class TinyPhotoGen(NpcPhotoGen):

    def __init__(self, mask, size):
        super(TinyPhotoGen, self).__init__(mask, size, 'unit8d', SMALL_PHOTO_PATH)
        self.adaptor.swfPath = 'gui/widgets/FubenMessageWidget' + self.getUIExt()
        self.needLoadAction = False


class PurchaseShopPhotoGen(NpcPhotoGen):

    def __init__(self, mask, size):
        super(PurchaseShopPhotoGen, self).__init__(mask, size, 'unitPurchaseShop', LARGE_PHOTO_PATH)
        self.adaptor.swfPath = 'gui/widgets/PurchaseShopWidget' + self.getUIExt()


class RolePhotoGen(NpcPhotoGen):

    def __init__(self, mask, size):
        super(RolePhotoGen, self).__init__(mask, size, 'unit11d', LARGE_PHOTO_PATH)
        self.adaptor.swfPath = 'gui/widgets/RoleInformationProperty' + self.getUIExt()
        self.adaptor.enableOpaque = 1
        self.cfType = const.SHADER_TYPE_C
        self.backGroundPath = 'gui/photoGenBg/role_photo_bg.dds'

    def getAvatarMatrix(self, ent, model, scale = 1):
        oldSources = list(ent.model.sources)
        newSources = list(model.sources)
        clientcom.checkRes(oldSources)
        clientcom.checkRes(newSources)
        oldSet = set(oldSources)
        newSet = set(newSources)
        if oldSet == newSet:
            self.realHeight = ent.getModelHeight()
        else:
            self.realHeight = self.getModelHeight(model)
        modelServer = ent.modelServer
        modelId, _ = modelServer.getMainModelAndID()
        m = Math.Matrix()
        if modelId == 10009:
            m.lookAt((0.55, self.realHeight * 0.57, 2.8), (-0.2, 0, -1), (0, 1, 0))
        elif modelId == 10004:
            m.lookAt((0, self.realHeight * 0.56, 2.1), (0, 0, -1), (0, 1, 0))
        elif modelId == 10005:
            m.lookAt((0, self.realHeight * 0.56, 2.4), (0, 0, -1), (0, 1, 0))
        elif modelId == 10006:
            m.lookAt((0, self.realHeight * 0.56, 2.3), (0, 0, -1), (0, 1, 0))
        return m

    def getDefaultMatrix(self, model):
        m = Math.Matrix()
        m.lookAt((-0.2, model.height * 0.88, 0.4), (0.45, 0, -1), (0, 1, 0))
        return m

    def setAvatar(self, ent):
        if not ent:
            return False
        modelServer = ent.modelServer
        modelId, bodyModel = modelServer.getMainModelAndID()
        oldList = list(self.adaptor.attachment.sources) if self.adaptor.attachment else []
        clientcom.checkRes(oldList)
        oldSet = set(oldList)
        newList = list(bodyModel.sources)
        clientcom.checkRes(newList)
        newSet = set(newList)
        if oldSet == newSet:
            return True
        if self.adaptor.attachment:
            TA.ta_reset([self.adaptor.attachment])
            model = self.adaptor.attachment
            if hasattr(model, 'texturePriority'):
                model.texturePriority = 0
            self.adaptor.attachment = None
            self.adaptor.transform = None
        self.modelId = modelId
        clientcom.fetchAvatarModel(ent, gameglobal.URGENT_THREAD, Functor(self.afterModelFinished, ent))

    def afterModelFinished(self, ent, model):
        if not model:
            return False
        clientcom.setModelIgnoreTpos(model)
        super(RolePhotoGen, self).afterPlayerModelFinished(self.modelId, ent, model)
        clientcom.cloneEntityAllAttachments(ent, model, True)
        return True

    def updateWeapon(self, ent, weapon):
        if self.adaptor.attachment:
            clientcom.cloneEntityModelAttachment(ent, weapon, self.adaptor.attachment, True)

    def updateWear(self, ent, wear):
        if self.adaptor.attachment:
            clientcom.cloneEntityAllAttachments(ent, self.adaptor.attachment, True)

    def endCapture(self):
        self.adaptor.closePhoto()
        super(RolePhotoGen, self).endCapture()

    def take(self):
        try:
            self.adaptor.takePhoto(1, 0, False, True, self.backGroundPath, 0, 1, 0, 1)
        except:
            pass


class BaseShopPhotoGen(BasePhotoGen):

    def __init__(self, mask, size, flashResName = 'unitShop'):
        super(BaseShopPhotoGen, self).__init__(mask, size, flashResName, RIDE_PHOTO_PATH)
        self.adaptor.swfPath = 'gui/widgets/FittingRoomWidget' + self.getUIExt()
        self.offset = (0, 0, 0)
        self.offsetDir = (0, 0, 0)
        self.adaptor.enableOpaque = 1
        self.cfType = const.SHADER_TYPE_C
        self.fittngModel = None

    def setFitingModel(self, fittingModel):
        self.fittngModel = weakref.proxy(fittingModel)

    def endCapture(self):
        super(BaseShopPhotoGen, self).endCapture()
        self.offset = (0, 0, 0)
        self.offsetDir = (0, 0, 0)
        self.fittngModel = None

    def getAvatarMatrix(self, ent, model, scale = 1):
        self.realHeight = self.getModelHeight(model)
        modelId = self.modelId
        m = Math.Matrix()
        pos = (0, 0, 0)
        dir = (0, 0, -1)
        if modelId == 10009:
            pos = (0.0, self.realHeight * 0.52, 2.3)
        elif modelId == 10004:
            pos = (0.0, self.realHeight * 0.52, 1.7)
        elif modelId == 10005:
            pos = (0.0, self.realHeight * 0.52, 2.2)
        elif modelId == 10006:
            pos = (0.0, self.realHeight * 0.52, 1.8)
        if self.offset:
            pos = (pos[0] + self.offset[0], pos[1] + self.offset[1], pos[2] + self.offset[2])
        if self.offsetDir:
            dir = (dir[0] + self.offsetDir[0], dir[1] + self.offsetDir[1], dir[2] + self.offsetDir[2])
        if scale >= 1:
            pos = (pos[0] * scale, pos[1], pos[2] * scale)
        else:
            pos = (pos[0] * scale, pos[1] / (scale * 1.05), pos[2] * scale)
        m.lookAt(pos, dir, (0, 1, 0))
        return m

    def getDefaultMatrix(self, model):
        m = Math.Matrix()
        m.lookAt((-0.1, model.height * 0.88, 0.4), (0.45, 0, -1), (0, 1, 0))
        return m

    def setModelPath(self, ent, res, isFittingRoom = False, isWingAndMount = False, isWingAndMountUpgrade = False):
        if not ent:
            return False
        if self.extraInfo and self.extraInfo.get('physique', None):
            physique = self.extraInfo['physique']
            modelId = charRes.transBodyType(physique.sex, physique.bodyType)
        else:
            modelServer = ent.modelServer
            modelId, _ = modelServer.getMainModelAndID()
        if not self.extraInfo.get('showAvatar', True):
            try:
                if res.has_key('fullPath'):
                    modelId = res['fullPath'].split('/')[-1].split('.')[0]
                else:
                    modelId = res['model']
            except:
                modelId = 0

        if self.adaptor.attachment:
            TA.ta_reset([self.adaptor.attachment])
            model = self.adaptor.attachment
            if hasattr(model, 'texturePriority'):
                model.texturePriority = 0
            self.adaptor.attachment = None
            self.adaptor.transform = None
            TA.ta_reset(self.attachedModel)
            for i, model in enumerate(self.attachedModel):
                if hasattr(model, 'texturePriority'):
                    model.texturePriority = 0
                self.attachedModel[i] = None

            self.attachedModel = []
        self.zoomScale = 1
        self.offset = (0, 0, 0)
        self.offsetDir = (0, 0, 0)
        self.adaptor.modelYaw = 0
        self.adaptor.photoFov = 1.0
        self.modelId = modelId
        if not self.extraInfo.get('showAvatar', True):
            if res.has_key('fullPath'):
                clientUtils.fetchModel(gameglobal.URGENT_THREAD, Functor(self.afterSingleModelFinished, self.modelId), res['fullPath'])
            else:
                clientcom.fetchModel(gameglobal.URGENT_THREAD, Functor(self.afterSingleModelFinished, self.modelId), res['model'])
        else:
            clientcom.fetchAvatarModelByRes(res, getattr(ent, 'realAvatarConfig', None), gameglobal.URGENT_THREAD, Functor(self.afterModelFinished, ent, isFittingRoom, isWingAndMount, isWingAndMountUpgrade))

    def afterSingleModelFinished(self, modelId, model):
        if not model:
            return False
        if modelId != self.modelId or self.modelId == None:
            model = None
            return False
        if hasattr(model, 'bkgLoadTint'):
            model.bkgLoadTint = False
        if hasattr(model, 'texturePriority'):
            model.texturePriority = 100
        clientcom.setModelIgnoreTpos(model)
        matrix = self.getRideMatrix(model)
        if matrix == None:
            matrix = self.getDefaultMatrix(model)
        self.adaptor.transform = matrix
        self.adaptor.attachment = model
        self.refresh()
        self.actionModel(self.modelId)
        if self.modelFinishCallback:
            self.modelFinishCallback()
        return True

    def afterModelFinished(self, ent, isFittingRoom, isWingAndMount, isWingAndMountUpgrade, model):
        if not model:
            return False
        super(BaseShopPhotoGen, self).afterPlayerModelFinished(self.modelId, ent, model)
        if isFittingRoom:
            item = None
            showItems = None
            originalAspect = None
            if self.fittngModel:
                item = self.fittngModel.item
                showItems = self.fittngModel.showItems
                originalAspect = self.fittngModel.originalAspect
            if not (self.extraInfo and self.extraInfo.get('physique', None)):
                if not gameglobal.rds.ui.fittingRoom.needHideHairWear(item):
                    aspect = self.extraInfo.get('aspect', None)
                    clientcom.cloneEntityHairWearAttachments(ent, model, True, aspect=aspect)
                if not gameglobal.rds.ui.fittingRoom.needHideFaceWear(item):
                    clientcom.cloneEntityFaceWearAttachments(ent, model, True)
                clientcom.cloneEntityOtherWearAttachments(ent, model, True)
                if not gameglobal.rds.ui.fittingRoom.needHideWeapon(item, originalAspect) and not gameglobal.rds.ui.fittingRoom.withFashionBack(showItems):
                    clientcom.cloneEntityAllWeaponAttachments(ent, model, True)
            if showItems or gameglobal.rds.ui.fittingRoom.showItems:
                aspect = self.extraInfo.get('aspect', None)
                physique = self.extraInfo.get('physique', None)
                clientcom.cloneAllWearAttachments(aspect, physique, model, True)
        elif isWingAndMount or isWingAndMountUpgrade:
            clientcom.cloneEntityAllWearAttachments(ent, model, True)
        else:
            clientcom.cloneEntityAllAttachments(ent, model, True)
        if self.fittngModel:
            item = self.fittngModel.item
            originalAspect = self.fittngModel.originalAspect
        else:
            item = gameglobal.rds.ui.fittingRoom.item
            originalAspect = gameglobal.rds.ui.fittingRoom.originalAspect
        if isFittingRoom and item:
            if originalAspect:
                p = BigWorld.player()
                for part in gametypes.EQU_PART_WEARS:
                    partName = gametypes.ASPECT_PART_REV_DICT[part]
                    if getattr(originalAspect, partName, None) and getattr(p.aspect, partName, None) != getattr(originalAspect, partName, None):
                        itemNew = Item(getattr(originalAspect, partName))
                        gameglobal.rds.ui.fittingRoom.setAttachMent(ent, model, itemNew, True, self.beforeSetAttachment, self.afterSetAttachment)

            if gameglobal.rds.ui.fittingRoom.checkBonusData(item):
                items = gameglobal.rds.ui.fittingRoom.getBonusData(item)
                for item in items:
                    gameglobal.rds.ui.fittingRoom.setAttachMent(ent, model, item, True, self.beforeSetAttachment, self.afterSetAttachment)

            else:
                gameglobal.rds.ui.fittingRoom.setAttachMent(ent, model, item, True, self.beforeSetAttachment, self.afterSetAttachment)
            if item.type == Item.BASETYPE_EQUIP:
                if item.equipType == Item.EQUIP_BASETYPE_FASHION:
                    if item.equipSType == Item.EQUIP_FASHION_SUBTYPE_CAPE:
                        self.rotateYaw(3.14)
                    elif item.equipSType in Item.EQUIP_FASHION_WEAR:
                        if item.equipSType == Item.EQUIP_FASHION_SUBTYPE_BACKWEAR:
                            self.rotateYaw(3.14)
                        elif item.equipSType == Item.EQUIP_FASHION_SUBTYPE_WAISTWEAR:
                            self.rotateYaw(1.57)
                        elif item.equipSType in (Item.EQUIP_FASHION_SUBTYPE_HEADWEAR_ASSEMBLE,
                         Item.EQUIP_FASHION_SUBTYPE_HEADWEAR_FRONT,
                         Item.EQUIP_FASHION_SUBTYPE_HEADWEAR_LR,
                         Item.EQUIP_FASHION_SUBTYPE_FACEWEAR):
                            self.zoom(-0.5)
        elif isWingAndMount and gameglobal.rds.ui.wingAndMount.item:
            item = gameglobal.rds.ui.wingAndMount.item
            if item:
                gameglobal.rds.ui.fittingRoom.setAttachMent(ent, model, item, True, self.beforeSetAttachment, self.afterSetAttachment)
        elif isWingAndMountUpgrade and gameglobal.rds.ui.wingAndMountUpgrade.item:
            item = gameglobal.rds.ui.wingAndMountUpgrade.item
            if item:
                gameglobal.rds.ui.fittingRoom.setAttachMent(ent, model, item, True, self.beforeSetAttachment, self.afterSetAttachment)
        return True

    def saveData(self, modelID, width, height):
        matrix = self.adaptor.transform
        dataSect = ResMgr.openSection(self.path, True)
        if modelID not in dataSect.keys():
            sect = dataSect.createSection(modelID)
        else:
            sect = dataSect.openSection(modelID)
        sect.writeMatrix('view', matrix)
        dataSect.save()

    def beforeSetAttachment(self, ent, model, item, hangUp = True):
        if item.equipType == Item.EQUIP_BASETYPE_ARMOR:
            if item.whereEquip()[0] == gametypes.EQU_PART_RIDE:
                self.adaptor.attachment = None

    def afterSetAttachment(self, ent, model, newModel, item, hangUp = True, scale = 0):
        if item.equipType == Item.EQUIP_BASETYPE_ARMOR:
            if item.whereEquip()[0] == gametypes.EQU_PART_RIDE:
                if not newModel:
                    return
                self.adaptor.attachment = newModel
                self.adaptor.transform = self.getRideMatrix(newModel)
                if hasattr(newModel, 'texturePriority'):
                    newModel.texturePriority = 100
                self.attachedModel = [newModel]
                ed = ED.data.get(item.id, {})
                horseShowAction = ed.get('horseShowAction', None)
                charShowAction = ed.get('charShowAction', None)
                try:
                    if horseShowAction:
                        newModel.action(horseShowAction)()
                    else:
                        self.action = None
                        self.actionModel(self.modelId)
                    if charShowAction:
                        model.action(charShowAction)()
                    elif self.action:
                        model.action(self.action[0])()
                    equipModel = ent.modelServer.rideAttached
                    attachments = equipModel.getAttachments(item.id, None, getattr(item, 'rideWingStage', 0))
                    if newModel and newModel.inWorld and attachments:
                        attachments = attachments[0]
                        for effect in attachments[4]:
                            fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (ent.getEquipEffectLv(),
                             ent.getEquipEffectPriority(),
                             newModel,
                             effect,
                             sfx.EFFECT_LIMIT_MISC))

                    clientcom.setTuZhuangConfig(item.id, newModel, getattr(item, 'dyeList', []))
                    if self.extraInfo and self.extraInfo.get('aspect', None):
                        clientcom.attachFashionEffect(ent, model, self.extraInfo['aspect'])
                except:
                    pass

            elif item.whereEquip()[0] == gametypes.EQU_PART_WINGFLY:
                self.offset = (0, 0.3, 1.5)
                self.adaptor.transform = self.getAvatarMatrix(ent, model, self.zoomScale)
                if hasattr(newModel, 'texturePriority'):
                    newModel.texturePriority = 100
                self.attachedModel = [newModel]
                clientcom.setTuZhuangConfig(item.id, newModel, getattr(item, 'dyeList', []))
                try:
                    newModel.action('21101')()
                    model.action('21101')()
                except:
                    pass

        elif item.equipType == Item.EQUIP_BASETYPE_FASHION and item.equipSType in Item.EQUIP_FASHION_WEAR:
            if newModel:
                for m in newModel:
                    m.texturePriority = 100

                self.attachedModel.extend(newModel)

    def getRideMatrix(self, rideModel):
        if not rideModel:
            return
        path = rideModel.sources[0]
        try:
            modelId = path.split('/')[-1].split('.')[0]
        except:
            modelId = self.modelId

        dataSect = self.matrixData.openSection(modelId) if self.matrixData else None
        if dataSect:
            matrix = dataSect.readMatrix('view')
            return matrix

    def startCaptureEntAndRes(self, ent, res, isFittingRoom = False, extraInfo = {}, isWingAndMount = False, isWingAndMountUpgrade = False):
        if self.callback:
            BigWorld.cancelCallback(self.callback)
        oldDynamic = self.dynamic
        self.action = ('1101',)
        self.dynamic = True
        self.extraInfo = extraInfo
        if not oldDynamic:
            self.adaptor.setSize(int(self.size * self.aaScale))
            self.adaptor.drawToFlashFromMesh()
        self.setModelPath(ent, res, isFittingRoom, isWingAndMount, isWingAndMountUpgrade)
        self.refresh()

    def zoom(self, deltaZoom):
        if self.zoomScale + deltaZoom < 0.5 or self.zoomScale + deltaZoom > 1.5:
            return
        self.zoomScale = self.zoomScale + deltaZoom
        self.adaptor.photoFov = self.zoomScale
        if self.adaptor.transform and (self.zoomScale - 1 < -0.01 or math.fabs(self.zoomScale - 1) <= 0.01 and deltaZoom >= 0):
            trans = self.adaptor.transform.translation
            self.adaptor.transform.translation = (trans[0], trans[1] + deltaZoom * 1.4, trans[2])

    def resetYaw(self):
        p = BigWorld.player()
        if self.adaptor.attachment:
            model = self.adaptor.attachment
            matrix = self.getRideMatrix(model)
            if matrix:
                self.adaptor.transform = matrix
            else:
                self.adaptor.transform = self.getAvatarMatrix(p, model)
        self.zoomScale = 1
        self.adaptor.modelYaw = 0
        self.adaptor.photoFov = 1.0


class ShopPhotoGen(BaseShopPhotoGen):
    __metaclass__ = Singleton


class FittingRoomPhotoGen(ShopPhotoGen):

    def __init__(self, mask, size, flashResName = 'unitShop'):
        super(ShopPhotoGen, self).__init__(mask, size, flashResName)
        self.backGroundPath = 'gui/photoGenBg/role_preview_bg.dds'

    def take(self):
        if self.adaptor.attachment == None:
            return
        try:
            self.adaptor.takePhoto(1, 0, False, True, self.backGroundPath, 0, 1, 0, 1)
        except:
            pass


class DyePhotoGen(ShopPhotoGen):

    def __init__(self, mask, size):
        super(DyePhotoGen, self).__init__(mask, size, 'unitDye')
        self.adaptor.swfPath = 'gui/widgets/DyeColorWidget' + self.getUIExt()


class MallPhotoGen(ShopPhotoGen):

    def __init__(self, mask, size):
        super(MallPhotoGen, self).__init__(mask, size, 'unitMall')
        self.adaptor.swfPath = 'gui/widgets/TianyuMallItems' + self.getUIExt()


class CombineMallPhotoGen(ShopPhotoGen):

    def __init__(self, mask, size):
        super(CombineMallPhotoGen, self).__init__(mask, size, 'unitCombineMall')
        self.adaptor.swfPath = 'gui/widgets/CombineTianyuMallItems' + self.getUIExt()


class GuiBaoGePhotoGen(ShopPhotoGen):

    def __init__(self, mask, size):
        super(GuiBaoGePhotoGen, self).__init__(mask, size, 'GuiBaoGe_unitGuibaoge')
        self.adaptor.enableOpaque = 1
        self.adaptor.swfPath = 'gui/widgets/GuiBaoGeWidget' + self.getUIExt()

    def afterSetAttachment(self, ent, model, newModel, item, hangUp = True, scale = 0):
        if item.equipType == Item.EQUIP_BASETYPE_ARMOR:
            if item.whereEquip()[0] == gametypes.EQU_PART_RIDE:
                if not newModel:
                    return
                self.adaptor.attachment = newModel
                self.adaptor.transform = self.getRideMatrix(newModel)
                if hasattr(newModel, 'texturePriority'):
                    newModel.texturePriority = 100
                self.attachedModel = [newModel]
                ed = ED.data.get(item.id, {})
                horseShowAction = ed.get('horseShowAction', None)
                charShowAction = ed.get('charShowAction', None)
                try:
                    if horseShowAction:
                        newModel.action(horseShowAction)()
                    else:
                        self.action = None
                        self.actionModel(self.modelId)
                    if charShowAction:
                        model.action(charShowAction)()
                    elif self.action:
                        model.action(self.action[0])()
                    equipModel = ent.modelServer.rideAttached
                    attachments = equipModel.getAttachments(item.id, None, getattr(item, 'rideWingStage', 0))
                    if newModel and newModel.inWorld and attachments:
                        attachments = attachments[0]
                        for effect in attachments[4]:
                            fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (ent.getEquipEffectLv(),
                             ent.getEquipEffectPriority(),
                             newModel,
                             effect,
                             sfx.EFFECT_LIMIT_MISC))

                except:
                    pass

            elif item.whereEquip()[0] == gametypes.EQU_PART_WINGFLY:
                self.offset = (0, 0.3, 1.5)
                self.adaptor.transform = self.getAvatarMatrix(ent, model, self.zoomScale * 1.2)
                if hasattr(newModel, 'texturePriority'):
                    newModel.texturePriority = 100
                self.attachedModel = [newModel]
                try:
                    newModel.action('21101')()
                    model.action('21101')()
                except:
                    pass


class FigurePhotoGen(RolePhotoGen):

    def __init__(self, mask, size):
        super(FigurePhotoGen, self).__init__(mask, size)
        self.adaptor.swfPath = ''
        self.adaptor.enableOpaque = 0
        self.aaScale = 128

    def getAvatarMatrix(self, ent, model, scale = 1):
        oldSources = list(ent.model.sources)
        newSources = list(model.sources)
        clientcom.checkRes(oldSources)
        clientcom.checkRes(newSources)
        oldSet = set(oldSources)
        newSet = set(newSources)
        if oldSet == newSet:
            self.realHeight = ent.getModelHeight()
        else:
            self.realHeight = self.getModelHeight(model)
        modelServer = ent.modelServer
        modelId, _ = modelServer.getMainModelAndID()
        m = Math.Matrix()
        if modelId == 10009:
            m.lookAt((0.0, self.realHeight * 0.57, 2.8), (0, 0, -1), (0, 1, 0))
        elif modelId == 10004:
            m.lookAt((0.0, self.realHeight * 0.56, 2.1), (0, 0, -1), (0, 1, 0))
        elif modelId == 10005:
            m.lookAt((0.0, self.realHeight * 0.56, 2.4), (0, 0, -1), (0, 1, 0))
        elif modelId == 10006:
            m.lookAt((0.0, self.realHeight * 0.56, 2.3), (0, 0, -1), (0, 1, 0))
        return m

    def setAvatar(self, ent):
        if not ent:
            return False
        modelServer = ent.modelServer
        modelId, bodyModel = modelServer.getMainModelAndID()
        self.clearModel()
        self.modelId = modelId
        mpr = charRes.MultiPartRes()
        mpr.queryByAttribute(ent.physique, ent.aspect, ent.isShowFashion(), ent.avatarConfig)
        res = mpr.getPrerequisites()
        clientcom.fetchAvatarModelByRes(res, getattr(ent, 'avatarConfig', None), gameglobal.URGENT_THREAD, Functor(self.afterModelFinished, ent))

    def afterModelFinished(self, ent, model):
        if not ent.inWorld:
            return False
        super(FigurePhotoGen, self).afterModelFinished(ent, model)
        return True


class FigureHeadPhotoGen(RolePhotoGen):

    def __init__(self, mask, size):
        super(FigureHeadPhotoGen, self).__init__(mask, size)
        self.adaptor.swfPath = ''
        self.adaptor.enableOpaque = 0
        self.aaScale = 27
        self.needAction = False

    def getAvatarMatrix(self, ent, model, scale = 1):
        m = Math.Matrix()
        try:
            headHeight = clientcom.getModeNodePosition(model, 'eyes_control_R')[1] - clientcom.getModeNodePosition(model, 'biped R Toe0')[1]
        except:
            headHeight = 0 if not model else model.height

        dist = 0.8
        m.lookAt((0, headHeight, dist), (0, 0, -1), (0, 1, 0))
        return m

    def afterModelFinished(self, ent, model):
        self.adaptor.photoFov = 0.4
        super(FigureHeadPhotoGen, self).afterModelFinished(ent, model)
        return True

    def setAvatar(self, ent):
        if not ent:
            return False
        modelServer = ent.modelServer
        modelId, bodyModel = modelServer.getMainModelAndID()
        self.clearModel()
        self.modelId = modelId
        mpr = charRes.MultiPartRes()
        mpr.queryByAttribute(ent.physique, ent.aspect, ent.isShowFashion(), ent.avatarConfig)
        res = mpr.getPrerequisites()
        clientcom.fetchAvatarModelByRes(res, getattr(ent, 'avatarConfig', None), gameglobal.URGENT_THREAD, Functor(self.afterModelFinished, ent))


class CharacterPhotoGen(RolePhotoGen):

    def __init__(self, mask, size):
        super(CharacterPhotoGen, self).__init__(mask, size)
        self.adaptor.swfPath = ''
        self.adaptor.enableOpaque = 0
        self.aaScale = 120
        self.needAction = True
        self.photoConfig = []

    def getAvatarMatrix(self, ent, model, scale = 1):
        m = Math.Matrix()
        try:
            headHeight = clientcom.getModeNodePosition(model, 'eyes_control_R')[1] - clientcom.getModeNodePosition(model, 'biped R Toe0')[1]
        except:
            headHeight = 0 if not model else model.height

        dist = 0.8
        m.lookAt((0, headHeight, dist), (0, 0, -1), (0, 1, 0))
        return m

    def afterModelFinished(self, ent, model):
        self.genPhotoConfig(model)
        self.adaptor.photoFov = 0.4
        clientcom.setModelIgnoreTpos(model)
        super(CharacterPhotoGen, self).afterModelFinished(ent, model)
        return True

    def genPhotoConfig(self, model):
        self.photoConfig = []
        m = Math.Matrix()
        rot = Math.Matrix()
        try:
            headHeight = clientcom.getModeNodePosition(model, 'eyes_control_R')[1] - clientcom.getModeNodePosition(model, 'biped R Toe0')[1]
        except:
            headHeight = 0 if not model else model.height

        dist = 0.8
        fov = 0.2 * headHeight + 0.2
        m.lookAt((0, headHeight, dist), (0, 0, -1), (0, 1, 0))
        self.photoConfig.append((fov, m, 'character0.png'))
        m1 = Math.Matrix(m)
        rot.setRotateY(math.pi / 4)
        m1.preMultiply(rot)
        self.photoConfig.append((fov, m1, 'character1.png'))
        m2 = Math.Matrix(m)
        rot.setRotateY(-math.pi / 4)
        m2.preMultiply(rot)
        self.photoConfig.append((fov, m2, 'character2.png'))
        m3 = Math.Matrix(m)
        rot.setRotateY(math.pi / 2)
        m3.preMultiply(rot)
        self.photoConfig.append((fov, m3, 'character3.png'))
        dist = 2.8
        m4 = Math.Matrix()
        fov = 0.367 * headHeight + 0.096
        m4.lookAt((0, headHeight * 0.55, dist), (0, 0, -1), (0, 1, 0))
        self.photoConfig.append((fov, m4, 'character4.png'))
        m5 = Math.Matrix(m4)
        rot.setRotateY(-math.pi / 4)
        m5.preMultiply(rot)
        self.photoConfig.append((fov, m5, 'character5.png'))

    def takeAndSave(self, index, callback = None):
        self._takeAndSave(index)
        fov, matrix, fileName = self.photoConfig[index]
        BigWorld.callback(0.3, Functor(self._processImage, fileName, callback))

    def _takeAndSave(self, index):
        fov, matrix, fileName = self.photoConfig[index]
        self.adaptor.photoFov = fov
        self.adaptor.transform = matrix
        self.adaptor.saveFrame(fileName)
        self.take()

    def _processImage(self, fileName, callback):
        try:
            backImg = Image.new('RGB', (self.aaScale * 10, self.aaScale * 10), 1578517)
            png = Image.open(fileName)
            png.load()
            channels = png.split()
            frontImg = Image.merge('RGB', channels[0:3])
            newImage = Image.composite(frontImg, backImg, channels[3])
            newImage.save(fileName.split('.')[0] + '.jpg')
            os.remove(fileName)
        except:
            pass

        if callback:
            BigWorld.callback(0, callback)

    def setAvatar(self, ent):
        if not ent:
            return False
        modelServer = ent.modelServer
        modelId, bodyModel = modelServer.getMainModelAndID()
        self.clearModel()
        self.modelId = modelId
        mpr = charRes.MultiPartRes()
        mpr.queryByAttribute(ent.physique, ent.aspect, ent.isShowFashion(), ent.avatarConfig)
        res = mpr.getPrerequisites()
        clientcom.fetchAvatarModelByRes(res, getattr(ent, 'avatarConfig', None), gameglobal.URGENT_THREAD, Functor(self.afterModelFinished, ent))

    def actionPlayerModel(self, modelId, ent):
        if not self.needAction:
            return
        model = self.adaptor.attachment
        if not self.action:
            self.action = ['1101']
        try:
            if model:
                model.action(self.action[0])(0, None, 0, 0)
        except:
            pass


class FaceEmotePhotoGen(ShopPhotoGen):

    def __init__(self, mask, size):
        super(FaceEmotePhotoGen, self).__init__(mask, size, 'unitEmotion')
        self.adaptor.swfPath = 'gui/widgets/GeneralSkillWidget' + self.getUIExt()
        self.adaptor.enableOpaque = 0

    def getAvatarMatrix(self, ent, model, scale = 1):
        m = Math.Matrix()
        try:
            headHeight = clientcom.getModeNodePosition(model, 'eyes_control_R')[1] - clientcom.getModeNodePosition(model, 'biped R Toe0')[1]
        except:
            headHeight = 0 if not model else model.height

        dist = 0.8
        m.lookAt((0, headHeight, dist), (0, 0, -1), (0, 1, 0))
        return m

    def afterPlayerModelFinished(self, modelId, ent, model):
        super(FaceEmotePhotoGen, self).afterPlayerModelFinished(modelId, ent, model)
        self.adaptor.photoFov = 0.5
        return True


class EmoteActionPhotoGen(ShopPhotoGen):

    def __init__(self, mask, size):
        super(EmoteActionPhotoGen, self).__init__(mask, size, 'unitEmotion')
        self.adaptor.swfPath = 'gui/widgets/EmoteActionWidget' + self.getUIExt()
        self.adaptor.enableOpaque = 0

    def getAvatarMatrix(self, ent, model, scale = 1):
        m = Math.Matrix()
        try:
            headHeight = clientcom.getModeNodePosition(model, 'eyes_control_R')[1] - clientcom.getModeNodePosition(model, 'biped R Toe0')[1]
        except:
            headHeight = 0 if not model else model.height

        dist = 0.8
        m.lookAt((0, headHeight, dist), (0, 0, -1), (0, 1, 0))
        return m

    def afterPlayerModelFinished(self, modelId, ent, model):
        super(EmoteActionPhotoGen, self).afterPlayerModelFinished(modelId, ent, model)
        self.adaptor.photoFov = 0.5
        return True


class TargetRoleInfoPhotoGen(ShopPhotoGen):

    def __init__(self, mask, size, flashResName = 'TargetRoleInfo_unitTargetRole'):
        super(TargetRoleInfoPhotoGen, self).__init__(mask, size, flashResName)
        self.adaptor.swfPath = 'gui/widgets/TargetRoleInfoWidget' + self.getUIExt()
        self.adaptor.enableOpaque = 1
        self.backGroundPath = 'gui/photoGenBg/target_role_bg.dds'
        self.loadID = 0

    def getAvatarMatrix(self, ent, model, scale = 1):
        self.realHeight = self.getModelHeight(model)
        modelId = self.modelId
        m = Math.Matrix()
        if modelId == 10009:
            m.lookAt((0.55, self.realHeight * 0.57, 2.8), (-0.2, 0, -1), (0, 1, 0))
        elif modelId == 10004:
            m.lookAt((0, self.realHeight * 0.56, 2.1), (0, 0, -1), (0, 1, 0))
        elif modelId == 10005:
            m.lookAt((0, self.realHeight * 0.56, 2.4), (0, 0, -1), (0, 1, 0))
        elif modelId == 10006:
            m.lookAt((0, self.realHeight * 0.56, 2.3), (0, 0, -1), (0, 1, 0))
        return m

    def afterModelFinished(self, modelId, aspect, physique, showFashion, loadID, model):
        if loadID != self.loadID:
            return
        super(TargetRoleInfoPhotoGen, self).afterPlayerModelFinished(self.modelId, None, model)
        clientcom.cloneAllAttachments(aspect, physique, showFashion, model, True)
        rongGuang = charRes.RongGuangRes()
        if aspect:
            rongGuang.queryByAttribute(aspect, showFashion)
            rongGuang.apply(model, self.needXuarn, self.cfType)
            clientcom.attachFashionEffect(BigWorld.player(), model, aspect)
        return True

    def startCaptureRes(self, modelId, aspect, physique, avatarConfig, actions = '1901', showFashion = False):
        if self.callback:
            BigWorld.cancelCallback(self.callback)
        self.action = actions
        self.dynamic = True
        self.adaptor.setSize(int(self.size * self.aaScale))
        self.adaptor.drawToFlashFromMesh()
        self.setModelRes(modelId, aspect, physique, avatarConfig, showFashion)
        self.refresh()

    def setModelRes(self, modelId, aspect, physique, avatarConfig, showFashion = False):
        if modelId == 0:
            return self.setAvatar(BigWorld.player())
        self.clearModel()
        self.modelId = modelId
        gamelog.debug('jjh@photo setModel', modelId, self.adaptor.attachment)
        if modelId == None:
            return False
        mpr = charRes.MultiPartRes()
        mpr.queryByAttribute(physique, aspect, showFashion, avatarConfig)
        self.extraInfo = {'aspect': aspect,
         'shwoFashion': showFashion}
        res = mpr.getPrerequisites()
        self.loadID += 1
        clientcom.fetchAvatarModelByRes(res, avatarConfig, gameglobal.URGENT_THREAD, Functor(self.afterModelFinished, modelId, aspect, physique, showFashion, self.loadID))

    def take(self):
        try:
            self.adaptor.takePhoto(1, 0, False, True, self.backGroundPath, 0, 1, 0, 1)
        except:
            pass


class TemplateRoleInfoPhotoGen(TargetRoleInfoPhotoGen):

    def __init__(self, mask, size):
        super(TemplateRoleInfoPhotoGen, self).__init__(mask, size, 'BalanceArenaPreview_unitTargetRole')
        self.adaptor.swfPath = 'gui/widgets/BalanceArenaPreviewWidget' + self.getUIExt()
        self.adaptor.enableOpaque = 1
        self.backGroundPath = 'gui/photoGenBg/target_role_bg.dds'
        self.loadID = 0

    def getAvatarMatrix(self, ent, model, scale = 1):
        self.realHeight = self.getModelHeight(model)
        modelId = self.modelId
        m = Math.Matrix()
        if modelId == 10009:
            m.lookAt((0.5, self.realHeight * 0.57, 2.8), (-0.2, 0, -1), (0, 1, 0))
        elif modelId == 10004:
            m.lookAt((-0.05, self.realHeight * 0.56, 2.1), (0, 0, -1), (0, 1, 0))
        elif modelId == 10005:
            m.lookAt((-0.05, self.realHeight * 0.56, 2.4), (0, 0, -1), (0, 1, 0))
        elif modelId == 10006:
            m.lookAt((-0.05, self.realHeight * 0.56, 2.3), (0, 0, -1), (0, 1, 0))
        return m


class ModelRoleInfoPhotoGen(ShopPhotoGen):

    def __init__(self, mask, size):
        super(ModelRoleInfoPhotoGen, self).__init__(mask, size, 'ModelRole_unitTargetRole')
        self.adaptor.swfPath = 'gui/widgets/ModelRoleInfoWidget' + self.getUIExt()
        self.loadID = 0

    def getAvatarMatrix(self, ent, model, scale = 1):
        self.realHeight = self.getModelHeight(model)
        modelId = self.modelId
        m = Math.Matrix()
        pos = (0, 0, 0)
        dir = (0, 0, -1)
        if modelId == 10009:
            pos = (0.0, self.realHeight * 0.52, 2.3)
        elif modelId == 10004:
            pos = (0.0, self.realHeight * 0.52, 1.7)
        elif modelId == 10005:
            pos = (0.0, self.realHeight * 0.52, 2.2)
        elif modelId == 10006:
            pos = (0.0, self.realHeight * 0.52, 1.8)
        if self.offset:
            pos = (pos[0] + self.offset[0], pos[1] + self.offset[1], pos[2] + self.offset[2])
        if self.offsetDir:
            dir = (dir[0] + self.offsetDir[0], dir[1] + self.offsetDir[1], dir[2] + self.offsetDir[2])
        pos = (pos[0] * scale, pos[1], pos[2] * scale)
        m.lookAt(pos, dir, (0, 1, 0))
        return m

    def afterModelFinished(self, modelId, aspect, physique, showFashion, loadID, model):
        if loadID != self.loadID:
            return
        super(ModelRoleInfoPhotoGen, self).afterPlayerModelFinished(self.modelId, None, model)
        clientcom.cloneAllAttachments(aspect, physique, showFashion, model, True)
        rongGuang = charRes.RongGuangRes()
        if aspect:
            rongGuang.queryByAttribute(aspect, showFashion)
            rongGuang.apply(model, self.needXuarn, self.cfType)
            clientcom.attachFashionEffect(BigWorld.player(), model, aspect)
        return True

    def startCaptureRes(self, modelId, aspect, physique, avatarConfig, actions = '1901', showFashion = False):
        if self.callback:
            BigWorld.cancelCallback(self.callback)
        self.action = actions
        self.dynamic = True
        self.adaptor.setSize(int(self.size * self.aaScale))
        self.adaptor.drawToFlashFromMesh()
        self.setModelRes(modelId, aspect, physique, avatarConfig, showFashion)
        self.refresh()

    def setModelRes(self, modelId, aspect, physique, avatarConfig, showFashion = False):
        if modelId == 0:
            return self.setAvatar(BigWorld.player())
        self.clearModel()
        self.modelId = modelId
        gamelog.debug('m.l@ModelRoleInfoPhotoGen.setModel', modelId, self.adaptor.attachment)
        if modelId == None:
            return False
        mpr = charRes.MultiPartRes()
        mpr.queryByAttribute(physique, aspect, showFashion, avatarConfig)
        self.extraInfo = {'aspect': aspect,
         'shwoFashion': showFashion}
        res = mpr.getPrerequisites()
        self.loadID += 1
        clientcom.fetchAvatarModelByRes(res, avatarConfig, gameglobal.URGENT_THREAD, Functor(self.afterModelFinished, modelId, aspect, physique, showFashion, self.loadID))


class ZhanQiPhotoGen(NpcPhotoGen):

    def __init__(self, mask, size):
        super(ZhanQiPhotoGen, self).__init__(mask, size, 'ZhanQi_unitZhanqi', TARGET_PHOTO_PATH)
        self.adaptor.swfPath = 'gui/widgets/ZhanQiWidget' + self.getUIExt()

    def getDefaultMatrix(self, model):
        m = Math.Matrix()
        m.lookAt((0, model.height * 0.5, -30), (0, 0, 1), (0, 1, 0))
        return m

    def setModel(self, modelId, addedModel = None, attaches = None):
        if self.modelId == modelId:
            return True
        if self.adaptor.attachment:
            TA.ta_reset([self.adaptor.attachment])
            model = self.adaptor.attachment
            if hasattr(model, 'texturePriority'):
                model.texturePriority = 0
            self.adaptor.attachment = None
            self.adaptor.transform = None
            for i, model in enumerate(self.attachedModel):
                if hasattr(model, 'texturePriority'):
                    model.texturePriority = 0
                self.attachedModel[i] = None

            self.attachedModel = []
        self.modelId = modelId
        if modelId == None:
            return False
        clientcom.fetchModel(gameglobal.URGENT_THREAD, self.afterModelFinished, modelId)

    def afterModelFinished(self, model):
        if self.modelId == None:
            model = None
            return True
        if hasattr(model, 'texturePriority'):
            model.texturePriority = 100
        morpher = ZhanqiDyeMorpher(model, self.modelId)
        morpher.genDefaultParam()
        morpher.apply()
        matrix = self.getDefaultMatrix(model)
        self.adaptor.transform = matrix
        self.adaptor.attachment = model
        self.refresh()
        return True


class ZhanPaoPhotoGen(ShopPhotoGen):

    def __init__(self, mask, size):
        super(ZhanPaoPhotoGen, self).__init__(mask, size)
        self.adaptor.swfPath = 'gui/widgets/GuildArmorWidget' + self.getUIExt()
        self.adaptor.flashResName = 'GuildArmor_unitZhanpao'
        self.needXuarn = False

    def getAvatarMatrix(self, ent, model):
        self.realHeight = self.getModelHeight(model)
        modelServer = ent.modelServer
        modelId, _ = modelServer.getMainModelAndID()
        m = Math.Matrix()
        if modelId == 10009:
            m.lookAt((0, self.realHeight * 0.52, 2.3), (0, 0, -1), (0, 1, 0))
        elif modelId == 10004:
            m.lookAt((0, self.realHeight * 0.52, 1.7), (0, 0, -1), (0, 1, 0))
        elif modelId == 10005:
            m.lookAt((0, self.realHeight * 0.52, 2.2), (0, 0, -1), (0, 1, 0))
        elif modelId == 10006:
            m.lookAt((0, self.realHeight * 0.52, 1.8), (0, 0, -1), (0, 1, 0))
        return m


class ApplyGuildZhanQiPhotoGen(ZhanQiPhotoGen):

    def __init__(self, mask, size):
        super(ApplyGuildZhanQiPhotoGen, self).__init__(mask, size)
        self.adaptor.swfPath = 'gui/widgets/ApplyGuildWidget' + self.getUIExt()
        self.adaptor.flashResName = 'ApplyGuild_unitApplyGuildZhanqi'


class GuildZhanQiPhotoGen(ZhanQiPhotoGen):

    def __init__(self, mask, size):
        super(GuildZhanQiPhotoGen, self).__init__(mask, size)
        self.adaptor.swfPath = 'gui/widgets/GuildInfoManageWidget' + self.getUIExt()
        self.adaptor.flashResName = 'unitGuildZhanqi'


class GuildZhanQiPhotoCreateGen(ZhanQiPhotoGen):

    def __init__(self, mask, size):
        super(GuildZhanQiPhotoCreateGen, self).__init__(mask, size)
        self.adaptor.swfPath = 'gui/widgets/CreateGuildWidget' + self.getUIExt()
        self.adaptor.flashResName = 'CreateGuild_unitGuildZhanqiCreate'


class GuildZhanPaoPhotoGen(ZhanPaoPhotoGen):

    def __init__(self, mask, size):
        super(GuildZhanPaoPhotoGen, self).__init__(mask, size)
        self.adaptor.swfPath = 'gui/widgets/GuildInfoManageWidget' + self.getUIExt()
        self.adaptor.flashResName = 'unitGuildZhanpao'


class PhotoGen(object):
    __metaclass__ = Singleton

    def __init__(self, type, size, flashResName):
        self.image = None
        self.adaptor = GUI.MeshAdaptor('gui/taskmask.tga', 0)
        self.aaScale = 1.5
        self.adaptor.setSize(int(self.aaScale * size))
        self.adaptor.modelAlpha = True
        self.adaptor.mixTextureAlpha = False
        self.adaptor.photoFov = 1
        self.adaptor.flashResName = flashResName
        self.adaptor.flashWidth = size
        self.adaptor.flashHeight = size
        self.dynamic = False
        self.size = size
        self.path = SKILL_PHOTO_PATH
        self.matrixData = photoDict.get(self.path, None)
        self.light = DefaultLight
        self.light1 = DefaultLight2
        self.lightDir = LightDir
        self.exposure = LightExposure
        self.callback = None
        self.type = type
        self.avatarPath = None
        self.endCallback = None

    def setAvatarSwfPath(self, path):
        self.avatarPath = path

    def getUIExt(self):
        if gameglobal.rds.ui.isUIPublished():
            return '.gfx'
        else:
            return '.swf'

    def setPlayer(self, actionId):
        if self.adaptor.attachment:
            TA.ta_reset([self.adaptor.attachment])
            self.adaptor.attachment = None
            self.adaptor.transform = None
        p = BigWorld.player()
        if not p:
            return False
        clientUtils.fetchModel(gameglobal.URGENT_THREAD, Functor(self.onLoadModel, actionId), *p.model.sources)
        return True

    def onLoadModel(self, actionId, model):
        if hasattr(model, 'bkgLoadTint'):
            model.bkgLoadTint = False
        clientcom.setModelIgnoreTpos(model)
        p = BigWorld.player()
        clientcom.copyAndSetAvatarConfig(None, p, model, False)
        matrix, _, _, _ = self.getPlayerMatrixAndLight()
        self.adaptor.transform = matrix
        self.adaptor.attachment = model
        self.doAction(actionId)
        if self.avatarPath:
            gameglobal.rds.ui.uiObj.Invoke('showBigPlayerPhoto', Scaleform.GfxValue(self.avatarPath))
        self.refresh()

    def doAction(self, actionId = '1101'):
        if self.adaptor.attachment:
            try:
                self.adaptor.attachment.action(actionId)()
            except:
                pass

    def take(self):
        if self.adaptor.attachment == None:
            return
        self.initFlashMesh()
        self.adaptor.setLights(self.light, self.light1)
        self.adaptor.setLightDir(*self.lightDir)
        self.adaptor.setLightHDR(*self.exposure)
        self.adaptor.takePhoto(1)

    def initFlashMesh(self):
        if not self.adaptor.needDrawToFlash:
            self.adaptor.needDrawToFlash = True
            self.adaptor.drawToFlashFromMesh()

    def refresh(self):
        if self.adaptor.attachment == None:
            return
        self.take()
        if self.dynamic:
            self.callback = BigWorld.callback(0, self.refresh)

    def getDefaultMatrix(self, model):
        m = Math.Matrix()
        m.lookAt((0, model.height * 0.8, 0.5), (0, 0, -1), (0, 1, 0))
        return m

    def getPlayerMatrixAndLight(self):
        p = BigWorld.player()
        dataSect = self.matrixData.openSection('%s/%d' % (self.type, p.fashion.modelID)) if self.matrixData else None
        if dataSect:
            matrix = dataSect.readMatrix('view')
            light = dataSect.readInt('light', DefaultLight)
            light1 = dataSect.readInt('light1', DefaultLight)
            lightDir = dataSect.readVector3('lightDir', Math.Vector3(-1, -1, -1))
        else:
            matrix = self.getDefaultMatrix(p.model)
            light = light1 = DefaultLight
            lightDir = Math.Vector3(-1, -1, -1)
        return (matrix,
         light,
         light1,
         lightDir)

    def startCapture(self, actionId):
        if self.callback:
            BigWorld.cancelCallback(self.callback)
        self.dynamic = True
        self.adaptor.setSize(int(self.size * self.aaScale))
        self.adaptor.drawToFlashFromMesh()
        self.setPlayer(actionId)
        if self.endCallback:
            BigWorld.cancelCallback(self.endCallback)
        self.endCallback = BigWorld.callback(3, self.endCapture)

    def endCapture(self):
        if self.adaptor.attachment:
            TA.ta_reset([self.adaptor.attachment])
            self.adaptor.attachment = None
            self.adaptor.transform = None
        self.dynamic = False
        self.adaptor.setSize(16)
        self.adaptor.needDrawToFlash = False

    def setModelDirectly(self, model):
        self.adaptor.attachment = model
        model.setModelNeedHide(False, 1.0)

    def adjustMatrix(self, matrix):
        self.adaptor.transform = matrix

    def adjustLight(self, light1):
        self.light = (light1 << 16) + (light1 << 8) + light1

    def saveData(self):
        modelID = str(BigWorld.player().fashion.modelID)
        matrix = self.adaptor.transform
        dataSect = ResMgr.openSection(self.path, True)
        if self.type not in dataSect.keys():
            typeSect = dataSect.createSection(self.type)
        else:
            typeSect = dataSect.openSection(self.type)
        if modelID not in typeSect.keys():
            sect = typeSect.createSection(modelID)
        else:
            sect = typeSect.openSection(modelID)
        sect.writeMatrix('view', matrix)
        sect.writeInt('light', self.light)
        sect.writeInt('light1', self.light1)
        sect.writeVector3('lightDir', self.lightDir)
        gamelog.debug('bgf:saveData', modelID, matrix, self.light)
        dataSect.save()


class SkillPlayerPhotoGen(PhotoGen):

    def __init__(self, size):
        super(SkillPlayerPhotoGen, self).__init__('unitSkill', size, 'unitSkill')
        self.adaptor.swfPath = 'gui/widgets/CombatSkillWidget' + self.getUIExt()

    def setPlayer(self, actionId):
        if self.adaptor.attachment:
            TA.ta_reset([self.adaptor.attachment])
            self.adaptor.attachment = None
            self.adaptor.transform = None
        p = BigWorld.player()
        if not p:
            return False
        model = clientUtils.model(gameglobal.SFX_DUMMY_MODEL)
        self.fx = clientUtils.pixieFetch(sfx.getPath(12130))
        model.root.attach(self.fx)
        matrix = self.getDefaultMatrix(model)
        self.fx.force()
        model.setAttachMode(0, 1, 0)
        self.adaptor.transform = matrix
        self.adaptor.attachment = model
        return True

    def getDefaultMatrix(self, model):
        m = Math.Matrix()
        m.lookAt((-0.4, 0.1, -0.4), (0.1, 0, 0.1), (0, 1, 0))
        return m


class BigPlayerPhotoGen(PhotoGen):

    def __init__(self, size):
        super(BigPlayerPhotoGen, self).__init__('unit5d', size, 'unit5d')


class SmallPlayerPhotoGen(PhotoGen):

    def __init__(self, size):
        super(SmallPlayerPhotoGen, self).__init__('unit6d', size, 'unit6d')


class WingAndMountPhotoGen(ShopPhotoGen):

    def __init__(self, mask, size):
        super(WingAndMountPhotoGen, self).__init__(mask, size, 'WingAndMount_unit')
        self.adaptor.swfPath = 'gui/widgets/WingAndMountWidget' + self.getUIExt()
        self.backGroundPath = 'gui/photoGenBg/wing_skill_bg.dds'

    def take(self):
        self.adaptor.takePhoto(1, 0, False, True, self.backGroundPath, 0, 1, 0, 1)


class WingAndMountUpgradePhotoGen(ShopPhotoGen):

    def __init__(self, mask, size):
        super(WingAndMountUpgradePhotoGen, self).__init__(mask, size, 'WingAndMountUpgrade_unit')
        self.adaptor.swfPath = 'gui/widgets/WingAndMountUpgradeWidget' + self.getUIExt()


class ZhenYaoPhotoGen(ShopPhotoGen):

    def __init__(self, mask, size):
        super(ZhenYaoPhotoGen, self).__init__(mask, size, 'unitZhenyao')
        self.adaptor.swfPath = 'gui/widgets/ZhenYaoFbResultWidget' + self.getUIExt()
        self.adaptor.enableOpaque = 0

    def take(self):
        if self.adaptor.attachment == None:
            return
        try:
            self.adaptor.takePhoto(1, 0)
        except:
            pass

    def getAvatarMatrix(self, ent, model, scale = 1):
        m = Math.Matrix()
        try:
            headHeight = clientcom.getModeNodePosition(model, 'eyes_control_R')[1] - clientcom.getModeNodePosition(model, 'biped R Toe0')[1]
        except:
            headHeight = 0 if not model else model.height

        dist = 0.8
        m.lookAt((0, headHeight, dist), (0, 0, -1), (0, 1, 0))
        return m


class ItemPreviewSelectPhotoGen(ShopPhotoGen):

    def __init__(self, mask, size):
        super(ItemPreviewSelectPhotoGen, self).__init__(mask, size, 'ItemPreviewSelect_unitItem')
        self.adaptor.enableOpaque = 1
        self.adaptor.swfPath = 'gui/widgets/ItemPreviewSelectWidget' + self.getUIExt()


class EvaluatePlayPhotoGen(ShopPhotoGen):

    def __init__(self, mask, size):
        super(EvaluatePlayPhotoGen, self).__init__(mask, size, 'EvaluatePlay_unitEvaluatePlay')
        self.adaptor.enableOpaque = 1
        self.adaptor.swfPath = 'gui/widgets/EvaluatePlayWidget' + self.getUIExt()


class VoidDreamlandPhotoGen(ShopPhotoGen):

    def __init__(self, mask, size):
        super(VoidDreamlandPhotoGen, self).__init__(mask, size, 'VoidDreamlandRank_unitVoidDreamland')
        self.adaptor.swfPath = 'gui/widgets/VoidDreamlandRankWidget' + self.getUIExt()
        self.adaptor.enableOpaque = 0


class SummonedWarSpritePhotoGen(NpcPhotoGen):

    def __init__(self, mask, size):
        super(SummonedWarSpritePhotoGen, self).__init__(mask, size, 'SummonedWarSpriteMine_unitItem', TARGET_PHOTO_PATH)
        self.adaptor.swfPath = 'gui/widgets/SummonedWarSpriteMineWidget' + self.getUIExt()
        self.adaptor.enableOpaque = 1
        self.backGroundPath = 'gui/photoGenBg/summoned_sprite2_bg.dds'

    def getDefaultMatrix(self, model):
        spriteInfo = gameglobal.rds.ui.summonedWarSpriteMine.getCurSelectSpriteInfo()
        spriteId = spriteInfo.get('spriteId', 0)
        isTransform = gameglobal.rds.ui.summonedWarSpriteMine.isTransform
        if isTransform:
            spritePos = SSID.data.get(spriteId, {}).get('spriteTransformPos', [0.35, 0.78, 4])
        else:
            spritePos = SSID.data.get(spriteId, {}).get('spritePos', [0.35, 0.78, 4])
        m = Math.Matrix()
        x = spritePos[0]
        quotiety = spritePos[1]
        z = spritePos[2]
        m.lookAt((x, model.height * quotiety, z), (0, 0, -1), (0, 1, 0))
        return m

    def endCapture(self):
        self.adaptor.closePhoto()
        super(SummonedWarSpritePhotoGen, self).endCapture()

    def take(self):
        self.adaptor.takePhoto(1, 0, False, True, self.backGroundPath, 0, 1, 0, 1)

    def setModel(self, modelId, addedModel = None, attaches = None):
        super(SummonedWarSpritePhotoGen, self).setModel(modelId, addedModel, attaches)
        if modelId == 0:
            return self.setAvatar(BigWorld.player())
        self.clearModel()
        self.modelId = modelId
        if modelId == None:
            return False
        if addedModel:
            model = addedModel
            self.afterModelFinished(modelId, attaches, model)
        else:
            clientcom.fetchModel(gameglobal.URGENT_THREAD, Functor(self.afterModelFinished, modelId, attaches), modelId)

    def afterModelFinished(self, modelId, attaches, model):
        super(SummonedWarSpritePhotoGen, self).afterModelFinished(modelId, attaches, model)
        gameglobal.rds.ui.summonedWarSpriteMine.updateAttachEffect(model, None, False)


class SummonedWarSpriteBiographyPhotoGen(NpcPhotoGen):

    def __init__(self, mask, size):
        super(SummonedWarSpriteBiographyPhotoGen, self).__init__(mask, size, 'SummonedWarSpriteBiography_unitItem', TARGET_PHOTO_PATH)
        self.adaptor.swfPath = 'gui/widgets/SummonedWarSpriteBiographyWidget' + self.getUIExt()
        self.adaptor.enableOpaque = 1
        self.backGroundPath = 'gui/photoGenBg/summoned_sprite2_bg.dds'

    def getDefaultMatrix(self, model):
        spriteId = gameglobal.rds.ui.summonedWarSpriteBiography.currSelectItemSpriteId
        spritePos = SSID.data.get(spriteId, {}).get('spritePos', [0.35, 0.78, 4])
        m = Math.Matrix()
        x = spritePos[0]
        quotiety = spritePos[1]
        z = spritePos[2]
        m.lookAt((x, model.height * quotiety, z), (0, 0, -1), (0, 1, 0))
        return m

    def endCapture(self):
        self.adaptor.closePhoto()
        super(SummonedWarSpriteBiographyPhotoGen, self).endCapture()

    def take(self):
        self.adaptor.takePhoto(1, 0, False, True, self.backGroundPath, 0, 1, 0, 1)


class SummonedWarSpriteExplorePhotoGen(BasePhotoGen):

    def __init__(self, mask, size, flashResName, backBg, iconIdx):
        super(SummonedWarSpriteExplorePhotoGen, self).__init__(mask, size, flashResName, TARGET_PHOTO_PATH)
        self.adaptor.swfPath = 'gui/widgets/SummonedWarSpriteExploreWidget' + self.getUIExt()
        self.adaptor.enableOpaque = 1
        self.backGroundPath = backBg
        self.iconIdx = iconIdx

    def getDefaultMatrix(self, model):
        p = BigWorld.player()
        exploreSpriteIdx = gameglobal.rds.ui.summonedWarSpriteExplore.exploreSpriteIdx
        spriteIndex = exploreSpriteIdx.get(self.iconIdx, 0)
        spriteInfo = p.summonSpriteList.get(spriteIndex, {})
        spriteId = spriteInfo.get('spriteId', 0)
        spritePos = SSID.data.get(spriteId, {}).get('spriteExplorePos', [0.35, 0.78, 4])
        m = Math.Matrix()
        x = spritePos[0]
        quotiety = spritePos[1]
        z = spritePos[2]
        m.lookAt((x, model.height * quotiety, z), (0, 0, -1), (0, 1, 0))
        return m

    def endCapture(self):
        self.adaptor.closePhoto()
        super(SummonedWarSpriteExplorePhotoGen, self).endCapture()

    def take(self):
        self.adaptor.takePhoto(1, 0, False, True, self.backGroundPath, 0, 1, 0, 1)


class SummonedWarSpriteUpGradePhotoGen(BasePhotoGen):

    def __init__(self, mask, size, flashResName):
        super(SummonedWarSpriteUpGradePhotoGen, self).__init__(mask, size, flashResName, TARGET_PHOTO_PATH)
        self.adaptor.swfPath = 'gui/widgets/SummonedWarSpriteUpGradeWidget' + self.getUIExt()
        self.adaptor.enableOpaque = 1
        self.backGroundPath = 'gui/photoGenBg/sprite_upGrade_bg.dds'

    def getDefaultMatrix(self, model):
        spritePos = [0.2, 0.55, 1.7]
        m = Math.Matrix()
        x = spritePos[0]
        quotiety = spritePos[1]
        z = spritePos[2]
        m.lookAt((x, model.height * quotiety, z), (0, 0, -1), (0, 1, 0))
        return m

    def endCapture(self):
        self.adaptor.closePhoto()
        super(SummonedWarSpriteUpGradePhotoGen, self).endCapture()

    def take(self):
        self.adaptor.takePhoto(1, 0, False, True, self.backGroundPath, 0, 1, 0, 1)

    def setModel(self, modelId, addedModel = None, attaches = None):
        super(SummonedWarSpriteUpGradePhotoGen, self).setModel(modelId, addedModel, attaches)
        if modelId == 0:
            return self.setAvatar(BigWorld.player())
        self.clearModel()
        self.modelId = modelId
        if modelId == None:
            return False
        if addedModel:
            model = addedModel
            self.afterModelFinished(modelId, attaches, model)
        else:
            clientcom.fetchModel(gameglobal.URGENT_THREAD, Functor(self.afterModelFinished, modelId, attaches), modelId)

    def afterModelFinished(self, modelId, attaches, model):
        super(SummonedWarSpriteUpGradePhotoGen, self).afterModelFinished(modelId, attaches, model)


class WingWorldSpriteCollectPhotoGen(BasePhotoGen):

    def __init__(self, mask, size, flashResName, iconIdx):
        super(WingWorldSpriteCollectPhotoGen, self).__init__(mask, size, flashResName, TARGET_PHOTO_PATH)
        self.adaptor.swfPath = 'gui/widgets/WingWorldResourcePanel' + self.getUIExt()
        self.adaptor.enableOpaque = 1
        self.backGroundPath = 'gui/photoGenBg/sprite_collect_bg.dds'
        self.iconIdx = iconIdx

    def getDefaultMatrix(self, model):
        p = BigWorld.player()
        spriteInSlots = p.spriteWingWorldRes.spriteInSlots
        spriteIndex = spriteInSlots.get(self.iconIdx, 0)
        if not spriteIndex:
            return
        spriteInfo = p.summonSpriteList.get(spriteIndex, {})
        spriteId = spriteInfo.get('spriteId', 0)
        spritePos = SSID.data.get(spriteId, {}).get('spriteCollectPos', [0.35, 0.78, 4])
        m = Math.Matrix()
        x = spritePos[0]
        quotiety = spritePos[1]
        z = spritePos[2]
        m.lookAt((x, model.height * quotiety, z), (0, 0, -1), (0, 1, 0))
        return m

    def endCapture(self):
        self.adaptor.closePhoto()
        super(WingWorldSpriteCollectPhotoGen, self).endCapture()

    def take(self):
        self.adaptor.takePhoto(1, 0, False, True, self.backGroundPath, 0, 1, 0, 1)


bigPhoto = BigPlayerPhotoGen.getInstance(560)

class MapGameSpriteDispatchPhotoGen(BasePhotoGen):

    def __init__(self, mask, size, flashResName, index):
        super(MapGameSpriteDispatchPhotoGen, self).__init__(mask, size, flashResName, TARGET_PHOTO_PATH)
        self.adaptor.swfPath = 'gui/widgets/MapGameDispatchWidget' + self.getUIExt()
        self.adaptor.enableOpaque = 0
        self.index = index

    def getDefaultMatrix(self, model):
        self.spriteIndex = gameglobal.rds.ui.mapGameDispatch.selectSpriteInfo[self.index]
        if self.spriteIndex < 0:
            return
        p = BigWorld.player()
        spriteInfo = p.summonSpriteList.get(self.spriteIndex, {})
        spriteId = spriteInfo.get('spriteId', 0)
        spritePos = SSID.data.get(spriteId, {}).get('spriteCollectPos', [0.35, 0.78, 4])
        m = Math.Matrix()
        x = spritePos[0]
        quotiety = spritePos[1]
        z = spritePos[2]
        m.lookAt((x, model.height * quotiety, z), (0, 0, -1), (0, 1, 0))
        return m

    def endCapture(self):
        self.adaptor.closePhoto()
        super(MapGameSpriteDispatchPhotoGen, self).endCapture()


class NormalPhotoGen(BaseShopPhotoGen):

    def __init__(self, mask, size, flashResName):
        super(NormalPhotoGen, self).__init__(mask, size, flashResName)
        self.adaptor.swfPath = 'gui/widgets/PartnerMainWidget' + self.getUIExt()
        self.loadID = 0

    def getAvatarMatrix(self, ent, model, scale = 1):
        self.realHeight = self.getModelHeight(model)
        modelId = self.modelId
        m = Math.Matrix()
        pos = (0, 0, 0)
        dir = (0, 0, -1)
        if modelId == 10009:
            pos = (0.0, self.realHeight * 0.52, 2.3)
        elif modelId == 10004:
            pos = (0.0, self.realHeight * 0.52, 1.7)
        elif modelId == 10005:
            pos = (0.0, self.realHeight * 0.52, 2.2)
        elif modelId == 10006:
            pos = (0.0, self.realHeight * 0.52, 1.8)
        if self.offset:
            pos = (pos[0] + self.offset[0], pos[1] + self.offset[1], pos[2] + self.offset[2])
        if self.offsetDir:
            dir = (dir[0] + self.offsetDir[0], dir[1] + self.offsetDir[1], dir[2] + self.offsetDir[2])
        pos = (pos[0] * scale, pos[1], pos[2] * scale)
        m.lookAt(pos, dir, (0, 1, 0))
        return m

    def afterModelFinished(self, modelId, aspect, physique, showFashion, loadID, model):
        if loadID != self.loadID:
            return
        super(NormalPhotoGen, self).afterPlayerModelFinished(self.modelId, None, model)
        clientcom.cloneAllAttachments(aspect, physique, showFashion, model, True)
        rongGuang = charRes.RongGuangRes()
        if aspect:
            rongGuang.queryByAttribute(aspect, showFashion)
            rongGuang.apply(model, self.needXuarn, self.cfType)
        return True

    def startCaptureRes(self, modelId, aspect, physique, avatarConfig, actions = '1901', showFashion = False):
        if self.callback:
            BigWorld.cancelCallback(self.callback)
        self.action = actions
        self.dynamic = True
        self.adaptor.setSize(int(self.size * self.aaScale))
        self.adaptor.drawToFlashFromMesh()
        self.setModelRes(modelId, aspect, physique, avatarConfig, showFashion)
        self.refresh()

    def setModelRes(self, modelId, aspect, physique, avatarConfig, showFashion = False):
        if modelId == 0:
            return self.setAvatar(BigWorld.player())
        self.clearModel()
        self.modelId = modelId
        if modelId == None:
            return False
        mpr = charRes.MultiPartRes()
        mpr.queryByAttribute(physique, aspect, showFashion, avatarConfig)
        self.extraInfo = {'aspect': aspect,
         'shwoFashion': showFashion}
        res = mpr.getPrerequisites()
        self.loadID += 1
        clientcom.fetchAvatarModelByRes(res, avatarConfig, gameglobal.URGENT_THREAD, Functor(self.afterModelFinished, modelId, aspect, physique, showFashion, self.loadID))


class MarryPreviewPhotoGen(NormalPhotoGen):
    __metaclass__ = Singleton

    def __init__(self, mask, size):
        super(MarryPreviewPhotoGen, self).__init__(mask, size, 'MarryPlanPreview_MarryPreview')
        self.adaptor.enableOpaque = 1
        self.adaptor.swfPath = 'gui/widgets/MarryPlanPreviewWidget' + self.getUIExt()
        self.backGroundPath = 'gui/photoGenBg/marry_plan_preview_bg.dds'

    def endCapture(self):
        self.adaptor.closePhoto()
        super(MarryPreviewPhotoGen, self).endCapture()

    def take(self):
        try:
            self.adaptor.takePhoto(1, 0, False, True, self.backGroundPath, 0, 1, 0, 1)
        except:
            pass


class MarryPlayerPreviewPhotoGen(BaseShopPhotoGen):
    __metaclass__ = Singleton

    def __init__(self, mask, size):
        super(MarryPlayerPreviewPhotoGen, self).__init__(mask, size, 'MarryPlanPreview_MarryPlayerPreview')
        self.adaptor.enableOpaque = 1
        self.adaptor.swfPath = 'gui/widgets/MarryPlanPreviewWidget' + self.getUIExt()
        self.backGroundPath = 'gui/photoGenBg/marry_plan_preview_bg.dds'

    def endCapture(self):
        self.adaptor.closePhoto()
        super(MarryPlayerPreviewPhotoGen, self).endCapture()

    def take(self):
        try:
            self.adaptor.takePhoto(1, 0, False, True, self.backGroundPath, 0, 1, 0, 1)
        except:
            pass


class PartnerPhotoGen(NormalPhotoGen):

    def __init__(self, mask, size, flashResName):
        super(PartnerPhotoGen, self).__init__(mask, size, flashResName)
        self.adaptor.swfPath = 'gui/widgets/PartnerMainWidget' + self.getUIExt()
        self.adaptor.enableOpaque = 1
        self.backGroundPath = 'gui/photoGenBg/partner_main_bg.dds'

    def getAvatarMatrix(self, ent, model, scale = 1):
        self.realHeight = self.getModelHeight(model)
        modelId = self.modelId
        m = Math.Matrix()
        pos = (0, 0, 0)
        dir = (0, 0, -1)
        if modelId == 10009:
            pos = (0.0, self.realHeight * 0.52, 2.3)
        elif modelId == 10004:
            pos = (0.0, self.realHeight * 0.65, 1.7)
        elif modelId == 10005:
            pos = (0.0, self.realHeight * 0.57, 2.2)
        elif modelId == 10006:
            pos = (0.0, self.realHeight * 0.52, 1.8)
        elif modelId == 10010:
            pos = (-0.1, self.realHeight * 0.52, 2.0)
        elif modelId == 10007:
            pos = (0.0, self.realHeight * 0.57, 2.2)
        if self.offset:
            pos = (pos[0] + self.offset[0], pos[1] + self.offset[1], pos[2] + self.offset[2])
        if self.offsetDir:
            dir = (dir[0] + self.offsetDir[0], dir[1] + self.offsetDir[1], dir[2] + self.offsetDir[2])
        pos = (pos[0] * scale, pos[1], pos[2] * scale)
        m.lookAt(pos, dir, (0, 1, 0))
        return m

    def endCapture(self):
        if hasattr(self.adaptor, 'closePhoto'):
            self.adaptor.closePhoto()
        super(PartnerPhotoGen, self).endCapture()

    def take(self):
        try:
            if hasattr(self.adaptor, 'closePhoto'):
                self.adaptor.takePhoto(1, 0, False, True, self.backGroundPath, 0, 1, 0, 1)
            else:
                self.adaptor.takePhoto(1)
        except:
            pass


class CombatPhotoGen(NormalPhotoGen):

    def __init__(self, mask, size, iconName):
        super(CombatPhotoGen, self).__init__(mask, size, iconName)
        self.adaptor.swfPath = 'gui/widgets/ZhiQiangDuiJueWidget' + self.getUIExt()

    def getAvatarMatrix(self, ent, model, scale = 1):
        m = Math.Matrix()
        try:
            headHeight = clientcom.getModeNodePosition(model, 'biped Head')[1] - clientcom.getModeNodePosition(model, 'biped R Toe0')[1]
            dist = 6 / 19.0 * headHeight + 0.55
            if 'c999' in self.action and self.modelId == 10004:
                m.lookAt((-0.05, headHeight, dist), (0.2, -0.2, -1), (0, 1, 0))
            elif 'b999' in self.action and self.modelId == 10004:
                m.lookAt((-0.05, headHeight, dist), (0.2, -0.18, -1), (0, 1, 0))
            else:
                m.lookAt((-0.05, headHeight, dist), (-0.05, -0.2, -1), (0, 1, 0))
            return m
        except:
            self.realHeight = model.height
            modelId = self.modelId
            if modelId == 10009:
                m.lookAt((-0.5, self.realHeight * 0.8, 1.5), (0.25, -0.1, -1), (0, 1, 0))
            elif modelId == 10004:
                m.lookAt((-0.1, self.realHeight * 0.85, 0.9), (-0.1, -0.2, -1), (0, 1, 0))
            elif modelId == 10005:
                m.lookAt((-0.1, self.realHeight * 0.9, 1.1), (-0.1, -0.3, -1), (0, 1, 0))
            elif modelId == 10006:
                m.lookAt((-0.05, self.realHeight * 0.9, 0.9), (-0.1, -0.3, -1), (0, 1, 0))
            return m

    def startCaptureDummy(self):
        if self.callback:
            BigWorld.cancelCallback(self.callback)
        self.dynamic = True
        self.adaptor.setSize(int(self.size * self.aaScale))
        self.adaptor.attachment = sfx.getDummyModel(False)
        self.adaptor.drawToFlashFromMesh()
        self.refresh()

    def startCaptureRes(self, modelId, aspect, physique, avatarConfig, actions = '1901', showFashion = False):
        if self.callback:
            BigWorld.cancelCallback(self.callback)
        self.action = actions
        self.dynamic = True
        self.adaptor.setSize(int(self.size * self.aaScale))
        self.setModelRes(modelId, aspect, physique, avatarConfig, showFashion)
        self.refresh()


class BalanceArenaPerson2PhotoGen(CombatPhotoGen):

    def __init__(self, mask, size, iconName):
        super(CombatPhotoGen, self).__init__(mask, size, iconName)
        self.adaptor.swfPath = 'gui/widgets/BalanceArena2PersonWidget' + self.getUIExt()
        self.backGroundPath = ''

    def getAvatarMatrix(self, ent, model, scale = 1):
        self.realHeight = self.getModelHeight(model)
        modelId = self.modelId
        m = Math.Matrix()
        if modelId == 10009:
            m.lookAt((0.5, self.realHeight * 0.57, 2.8), (-0.2, 0.02, -1), (0, 1, 0))
        elif modelId == 10004:
            m.lookAt((-0.05, self.realHeight * 0.56, 2.1), (0, 0.1, -1), (0, 1, 0))
        elif modelId == 10005:
            m.lookAt((-0.05, self.realHeight * 0.56, 2.4), (0, 0, -1), (0, 1, 0))
        elif modelId == 10006:
            m.lookAt((-0.05, self.realHeight * 0.56, 2.3), (0, 0, -1), (0, 1, 0))
        return m

    def take(self):
        try:
            self.adaptor.takePhoto(1, 0, False, True, self.backGroundPath, 0, 1, 0, 1)
        except:
            pass


class SchoolTopPhotoGen(NormalPhotoGen):

    def __init__(self, mask, size, iconName):
        super(SchoolTopPhotoGen, self).__init__(mask, size, iconName)
        self.adaptor.swfPath = 'gui/widgets/SchoolTopFightWidget' + self.getUIExt()

    def getAvatarMatrix(self, ent, model, scale = 1):
        m = Math.Matrix()
        try:
            headHeight = clientcom.getModeNodePosition(model, 'biped Head')[1] - clientcom.getModeNodePosition(model, 'biped R Toe0')[1]
            dist = 6 / 19.0 * headHeight + 0.55
            if 'c999' in self.action and self.modelId == 10004:
                m.lookAt((-0.05, headHeight, dist), (0.2, -0.2, -1), (0, 1, 0))
            elif 'b999' in self.action and self.modelId == 10004:
                m.lookAt((-0.05, headHeight, dist), (0.2, -0.18, -1), (0, 1, 0))
            else:
                m.lookAt((-0.05, headHeight, dist), (-0.05, -0.2, -1), (0, 1, 0))
            return m
        except:
            self.realHeight = model.height
            modelId = self.modelId
            if modelId == 10009:
                m.lookAt((-0.5, self.realHeight * 0.8, 1.5), (0.25, -0.1, -1), (0, 1, 0))
            elif modelId == 10004:
                m.lookAt((-0.1, self.realHeight * 0.85, 0.9), (-0.1, -0.2, -1), (0, 1, 0))
            elif modelId == 10005:
                m.lookAt((-0.1, self.realHeight * 0.9, 1.1), (-0.1, -0.3, -1), (0, 1, 0))
            elif modelId == 10006:
                m.lookAt((-0.05, self.realHeight * 0.9, 0.9), (-0.1, -0.3, -1), (0, 1, 0))
            return m

    def startCaptureDummy(self):
        if self.callback:
            BigWorld.cancelCallback(self.callback)
        self.dynamic = True
        self.adaptor.setSize(int(self.size * self.aaScale))
        self.adaptor.attachment = sfx.getDummyModel(False)
        self.adaptor.drawToFlashFromMesh()
        self.refresh()

    def startCaptureRes(self, modelId, aspect, physique, avatarConfig, actions = '1901', showFashion = False):
        if self.callback:
            BigWorld.cancelCallback(self.callback)
        self.action = actions
        self.dynamic = True
        self.adaptor.setSize(int(self.size * self.aaScale))
        self.setModelRes(modelId, aspect, physique, avatarConfig, showFashion)
        self.refresh()


class QuizzesAvatarPhotoGen(NpcPhotoGen):

    def __init__(self, mask, size):
        super(QuizzesAvatarPhotoGen, self).__init__(mask, size, 'YunChuiQuizzes_unitItem', TARGET_PHOTO_PATH)
        self.adaptor.swfPath = 'gui/widgets/YunChuiQuizzesWidget' + self.getUIExt()
        self.adaptor.photoFov = 0.7

    def getDefaultMatrix(self, model, scale = 1):
        self.realHeight = self.getModelHeight(model)
        modelId = self.modelId
        gamelog.debug('yedawang### modelId realHeight model.height', modelId, self.realHeight, model.height)
        m = Math.Matrix()
        pos = (0, 0, 0)
        dir = (0, 0, -1)
        if modelId == 10260:
            pos = (0.0, self.realHeight * 0.3, 0.25)
        elif modelId == 10264:
            pos = (0.0, self.realHeight * 0.5, 0.25)
        elif modelId == 10265:
            pos = (0.0, self.realHeight * 0.55, 0.25)
        elif modelId == 10266:
            pos = (0.0, self.realHeight * 0.5, 0.25)
        elif modelId == 10262:
            pos = (0.0, self.realHeight * 0.6, 0.25)
        elif modelId == 10263:
            pos = (0.0, self.realHeight * 0.5, 0.25)
        elif modelId == 10267:
            pos = (45, self.realHeight * 0.5, 45)
            dir = (-1, 0, -1)
        elif modelId == 10268:
            pos = (0.8, self.realHeight * 0.925, -0.05)
            dir = (-1, 0, 0)
        if scale >= 1:
            pos = (pos[0] * scale, pos[1], pos[2] * scale)
        m.lookAt(pos, dir, (0, 1, 0))
        return m


class GuildMembersFbPhotoGen(ShopPhotoGen):

    def __init__(self, mask, size):
        super(GuildMembersFbPhotoGen, self).__init__(mask, size, 'GuildMembersFbResult_unit')
        self.adaptor.swfPath = 'gui/widgets/GuildMembersFbResultWidget' + self.getUIExt()
        self.adaptor.enableOpaque = 0

    def take(self):
        if self.adaptor.attachment == None:
            return
        try:
            self.adaptor.takePhoto(1, 0)
        except:
            pass

    def getAvatarMatrix(self, ent, model, scale = 1):
        m = Math.Matrix()
        try:
            headHeight = clientcom.getModeNodePosition(model, 'eyes_control_R')[1] - clientcom.getModeNodePosition(model, 'biped R Toe0')[1]
        except:
            headHeight = 0 if not model else model.height

        dist = 0.8
        m.lookAt((0, headHeight, dist), (0, 0, -1), (0, 1, 0))
        return m
