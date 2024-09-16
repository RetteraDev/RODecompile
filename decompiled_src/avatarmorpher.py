#Embedded file name: /WORKSPACE/data/entities/client/helpers/avatarmorpher.o
import random
import copy
import zlib
import BigWorld
import ResMgr
import charRes
import strmap
import const
from helpers import boneMorpher
from helpers import vertexMorpher
from helpers import avatarMorpherUtils as AMU
from helpers import dyeMorpher
from data import sys_config_data as SCD
AVAILABLE_MORPHER = {'faxing_style': ('res', 'hair'),
 'zhuangshi_style': ('head', 'maskCTex')}

def getDisableMorpher(availableMorpher, sex, bodyType, school):
    modelId = charRes.transDummyBodyType(sex, bodyType, True)
    disableMorpher = copy.deepcopy(SCD.data.get('disableMorpher', {}).get(modelId, {}))
    schoolDisableMorpher = SCD.data.get('schoolDisableMorpher', {}).get((modelId, school), {})
    if schoolDisableMorpher:
        for morpher in AVAILABLE_MORPHER.keys():
            if schoolDisableMorpher.has_key(morpher):
                morpherData = schoolDisableMorpher[morpher]
                tempDict = dict(zip(morpherData, [-1] * len(morpherData)))
                disableMorpher.setdefault(morpher, {}).update(tempDict)

    for morpher in AVAILABLE_MORPHER.keys():
        if availableMorpher.has_key(morpher):
            morpherData = availableMorpher[morpher].get((sex, bodyType), [])
            if disableMorpher.has_key(morpher):
                for x in morpherData:
                    if x in disableMorpher[morpher]:
                        disableMorpher[morpher].pop(x)

    return disableMorpher


def getDisableMorpherInfo(disableMorpher, sex, bodyType):
    modelId = charRes.transDummyBodyType(sex, bodyType, True)
    ret = {}
    for morpher, file in AVAILABLE_MORPHER.iteritems():
        config = None
        if file[0] == 'res':
            config = getAvatarResConfig(modelId)
            config = config[file[1]][1]
        else:
            config = dyeMorpher.getDyeConfig(modelId, file[0])
            if not config:
                return ret
            for item in config:
                if item[0] == file[1]:
                    config = item[1][0][2]
                    break

        ret[morpher] = {}
        ret[morpher + '_Num'] = len(config)
        if disableMorpher.has_key(morpher):
            for x in disableMorpher[morpher]:
                if x in config:
                    ret[morpher][config.index(x)] = disableMorpher[morpher][x]

    return ret


def getDisableMorpherInfoFromAvatar(avatar):
    physique = avatar.physique
    availableMorpher = getattr(avatar, 'availableMorpher', {})
    disableMorpher = getDisableMorpher(availableMorpher, physique.sex, physique.bodyType, physique.school)
    return getDisableMorpherInfo(disableMorpher, physique.sex, physique.bodyType)


AVATAR_RES_CONFIG_CACHE = {}

def getAvatarResConfig(modelId):
    resConfig = AVATAR_RES_CONFIG_CACHE.get(modelId)
    if resConfig is not None:
        return resConfig
    path = 'char/%d/config/res.xml' % modelId
    dataInfo = ResMgr.openSection(path)
    if not dataInfo:
        return
    resConfig = {}
    for key in dataInfo.keys():
        ps = dataInfo[key].asString.split('|')
        t = int(ps[0])
        if t == 1:
            ops = []
            ss = ps[1].split(';')
            for s in ss:
                if s != '':
                    ops.append(int(s))

            if len(ops) < 1:
                raise TypeError, 'Unknown format %s in %s' % (key, path)
            resConfig[key] = (t, tuple(ops))
        elif t == 2:
            ops = []
            ss = ps[1].split(';')
            for s in ss:
                if s != '':
                    ops.append(s)

            if len(ops) < 1:
                raise TypeError, 'Unknown format %s in %s' % (key, path)
            resConfig[key] = (t, tuple(ops))
        elif t == 3:
            ops = []
            ss = ps[1].split(';')
            if len(ss) < 2 or ss[0] == '' or ss[1] == '':
                raise TypeError, 'Unknown format %s in %s' % (key, path)
            m1, m2 = float(ss[0]), float(ss[1])
            resConfig[key] = (t, (m1, m2))
        else:
            raise TypeError, 'Unknown format %s in %s' % (key, path)

    AVATAR_RES_CONFIG_CACHE[modelId] = resConfig
    return resConfig


def fillFreeInfo(section, resConfig):
    for key in section.keys():
        resConfig[key] = section[key].asInt


def getConfigByAvatarRes(modelId, key):
    resConfig = getAvatarResConfig(modelId)
    if resConfig:
        return resConfig.get(key)


def preloadAllAvatarConfig(modelIds):
    if not modelIds:
        return
    for modelId in modelIds:
        getAvatarResConfig(modelId)
        for configName in dyeMorpher.CONFIG_NAME:
            dyeMorpher.getDyeConfig(modelId, configName)

        boneMorpher.getBoneConfig('char/' + str(modelId) + '/config/face')
        boneMorpher.getBoneConfig('char/' + str(modelId) + '/config/body')


class SimpleModelMorpher(object):

    def __init__(self, model, gender, school, bodyType, face = None, hair = None, head = None, body = None, hand = None, leg = None, shoe = None, isEquipId = False, headType = charRes.HEAD_TYPE0, dyesDict = None, matterDict = None, fxType = 1, availableMorpher = {}, cape = None):
        self.enableBoneMorph = True
        self.school = school
        self.modelId = charRes.transBodyType(gender, bodyType)
        self.dummyModelId = charRes.transDummyBodyType(gender, bodyType, True)
        self.face = face
        self.hair = hair
        self.head = self._getModelId(head) if isEquipId else head
        self.body = self._getModelId(body) if isEquipId else body
        self.hand = self._getModelId(hand) if isEquipId else hand
        self.leg = self._getModelId(leg) if isEquipId else leg
        self.shoe = self._getModelId(shoe) if isEquipId else shoe
        self.cape = self._getModelId(cape) if isEquipId else cape
        self.head = None if self.head == charRes.PART_NOT_NEED else self.head
        self.body = None if self.body == charRes.PART_NOT_NEED else self.body
        self.hand = None if self.hand == charRes.PART_NOT_NEED else self.hand
        self.leg = None if self.leg == charRes.PART_NOT_NEED else self.leg
        self.shoe = None if self.shoe == charRes.PART_NOT_NEED else self.shoe
        self.cape = None if self.cape == charRes.PART_NOT_NEED else self.cape
        self.fxType = fxType
        self.morpherLimit = {}
        if self.enableBoneMorph:
            self.boneFactory = boneMorpher.BoneMorpherFactory(model)
            self.faceBone = boneMorpher.BoneMorpher(model, 'char/' + str(self.dummyModelId) + '/config/face', 'faceBones')
            self.bodyBone = boneMorpher.BoneMorpher(model, 'char/' + str(self.dummyModelId) + '/config/body', 'bodyBones')
            self.boneFactory.register(self.faceBone)
            self.boneFactory.register(self.bodyBone)
        self.faceMorpher = vertexMorpher.VertexMorpher(model, AMU.FACE_MORPHER_DATA, 'faceMorphs')
        self.dyeMorpher = dyeMorpher.DyeMorpher(model, self.modelId, self.dummyModelId, self.face, self.hair, self.head, self.body, self.hand, self.leg, self.shoe, headType, dyesDict, matterDict, cape=self.cape)
        self.fetchDisableMorpher(availableMorpher, gender, bodyType, school)

    def fetchDisableMorpher(self, availableMorpher, gender, bodyType, school):
        disableMorpher = getDisableMorpher(availableMorpher, gender, bodyType, school)
        self.morpherLimit = getDisableMorpherInfo(disableMorpher, gender, bodyType)

    def _getModelId(self, value):
        return charRes.getEquipModel(value, self.school, self.modelId)

    def readConfig(self, config):
        configMap = strmap.strmap(config)
        if self.enableBoneMorph:
            self.faceBone.read(configMap, lambda v: AMU.getMorpherByIdx(v))
            self.bodyBone.read(configMap, lambda v: AMU.getMorpherByIdx(v))
        self.faceMorpher.read(configMap, lambda v: AMU.getMorpherByIdx(v))
        self.dyeMorpher.read(configMap, lambda v: AMU.getMorpherByIdx(v))
        self.fxType = configMap.get('fxType', 1)

    def export(self, orig, needCompress = True, needEncrypt = False):
        orig = self.exportFaceBoneMorph(orig)
        orig = self.exportFaceMorph(orig)
        orig = self.exportBodyBoneMorph(orig)
        orig = self.exportDyeMorph(orig)
        orig = self.exporetFxType(orig)
        if needCompress:
            orig = zlib.compress(orig)
        if needEncrypt:
            orig = strmap.encryptContent(orig)
        return orig

    def exportFaceBoneMorph(self, orig):
        return self.faceBone.export(orig, lambda v: AMU.getIdxByMorpher(v))

    def exportBodyBoneMorph(self, orig):
        return self.bodyBone.export(orig, lambda v: AMU.getIdxByMorpher(v))

    def exportFaceMorph(self, orig):
        return self.faceMorpher.export(orig, lambda v: AMU.getIdxByMorpher(v))

    def exportDyeMorph(self, orig):
        return self.dyeMorpher.export(orig, lambda v: AMU.getIdxByMorpher(v))

    def exporetFxType(self, orig):
        sm = strmap.strmap(orig)
        sm.set('fxType', self.fxType)
        return sm.__str__()

    def apply(self, loadImmediate = False):
        if self.enableBoneMorph:
            self.applyBoneMorph()
        self.applyFaceMorph()
        self.applyDyeMorph(loadImmediate)

    def applyBoneMorph(self):
        self.boneFactory.apply()

    def applyFaceBoneMorph(self):
        self.boneFactory.applyFaceBone()

    def setAndApplyFaceBoneMorph(self, transform, ratio, resetForm = None):
        self.setFaceBoneMorph(transform, ratio, resetForm)
        self.applyBoneMorph()

    def setFaceBoneMorph(self, transform, ratio, resetForm = None):
        if resetForm:
            self.faceBone.setMorph(resetForm, 0)
        self.faceBone.setMorph(transform, ratio)

    def setAndApplyBodyBoneMorph(self, transform, ratio, resetForm = None):
        self.setBodyBoneMorph(transform, ratio, resetForm)
        self.applyBoneMorph()

    def setBodyBoneMorph(self, transform, ratio, resetForm = None):
        if resetForm:
            self.bodyBone.setMorph(resetForm, 0)
        self.bodyBone.setMorph(transform, ratio)

    def applyFaceMorph(self):
        self.faceMorpher.apply()

    def setAndApplyFaceMorph(self, transform, ratio, resetForm = None):
        self.setFaceMorph(transform, ratio, resetForm)
        self.applyFaceMorph()

    def setFaceMorph(self, transform, ratio, resetForm = None):
        if resetForm:
            self.faceMorpher.setMorph(resetForm, 0)
        self.faceMorpher.setMorph(transform, ratio)

    def applyDyeMorph(self, loadImmediate = False):
        self.dyeMorpher.apply(None, loadImmediate)

    def setAndApplyDyeMorph(self, matters, transform, value):
        self.dyeMorpher.setAndApply(matters, transform, value, True)

    def getDyeMorpherRandomValue(self, matters, transform):
        isMale = charRes.retransGender(self.modelId) == const.SEX_MALE
        uiBtn, value = AMU.getUIParamByDyeMorpher(transform, 0, isMale)
        if uiBtn in self.morpherLimit.keys():
            num = self.morpherLimit[uiBtn + '_Num']
            avaiableIndex = range(0, num)
            for index in self.morpherLimit[uiBtn].keys():
                if index in avaiableIndex:
                    avaiableIndex.remove(index)

            return random.choice(avaiableIndex)
        return self.dyeMorpher.getRandomValue(matters, transform)

    def resetAndApply(self):
        if self.enableBoneMorph:
            self.boneFactory.resetAndApply()
        self.faceMorpher.resetAndApply()
        self.dyeMorpher.resetAndApply()

    def getHairNum(self):
        config = getConfigByAvatarRes(self.dummyModelId, 'hair')
        if not config:
            return 0
        l = len(config[1])
        return l

    def setHairStyle(self, value, isRatio = True):
        config = getConfigByAvatarRes(self.dummyModelId, 'hair')
        if not config:
            return
        disableHairIndex = self.morpherLimit.get('faxing_style', {}).keys()
        if isRatio:
            if value >= 0 and value not in disableHairIndex:
                self.hair = config[1][int(value)]
        elif value in config[1]:
            self.hair = value

    def getRandomHair(self):
        config = getConfigByAvatarRes(self.dummyModelId, 'hair')
        if not config:
            return 0
        disableHairIndex = self.morpherLimit.get('faxing_style', {}).keys()
        hairIndex = range(0, len(config[1]))
        for index in disableHairIndex:
            if index in hairIndex:
                hairIndex.remove(index)

        return random.choice(hairIndex)

    def getHairStyle(self):
        config = getConfigByAvatarRes(self.dummyModelId, 'hair')
        if config and self.hair in config[1]:
            return config[1].index(self.hair)
        return 0

    def isValidHair(self):
        config = getConfigByAvatarRes(self.dummyModelId, 'hair')
        if config and self.hair in config[1]:
            return True
        return False


class AvatarModelMorpher(SimpleModelMorpher):

    def __init__(self, avatarId, enableBoneMorph = True):
        mpr = charRes.MultiPartRes()
        avatar = BigWorld.entities.get(avatarId)
        mpr.queryByAvatar(avatar)
        model = avatar.model
        if hasattr(avatar.modelServer, 'bodyModel'):
            model = avatar.modelServer.bodyModel
        elif avatar.inRiding():
            model = avatar.model.ride
        availableMorpher = getattr(avatar, 'availableMorpher', {})
        super(AvatarModelMorpher, self).__init__(model, avatar.realPhysique.sex, avatar.realPhysique.school, avatar.realPhysique.bodyType, mpr.face, mpr.hair, mpr.head, mpr.body, mpr.hand, mpr.leg, mpr.shoe, False, mpr.headType, mpr.dyesDict, mpr.mattersDict, 1, availableMorpher, cape=mpr.cape)
        self.enableBoneMorph = enableBoneMorph
