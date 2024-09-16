#Embedded file name: /WORKSPACE/data/entities/client/helpers/charres.o
import random
import BigWorld
import gametypes
import const
import gameglobal
import gamelog
import clientcom
import strmap
import clientUtils
import tmpdata as TD
import dyeMorpher as DM
from helpers import tintalt as TA
from callbackHelper import Functor
from data import school_data as SD
from data import equip_data as ED
from cdata import equip_ref_data as ERD
from data import sys_config_data as SCD
PART_NOT_NEED = -1
PART_NOT_EQUIPPED = 0
MODEL_BASE = 10000
NPC_MODEL_BASE = 11000
HEAD_TYPE0 = 0
HEAD_TYPE1 = 1
HEAD_TYPE2 = 2
HAND_LENGTH_0 = 0
HAND_LENGTH_1 = 1
HAND_LENGTH_2 = 2
PARTS_ASPECT = ('body',
 'leg',
 'hand',
 'shoe',
 'cape',
 'head')
PARTS_ASPECT_EQUIP = ('body',
 'leg',
 'hand',
 'shoe',
 'cape',
 'head',
 'fashionHead')
PARTS_ASPECT_FASHION_SUB = ('fashionBody',
 'fashionLeg',
 'fashionHand',
 'fashionCape',
 'fashionHead',
 'fashionShoe')
PARTS_ASPECT_FASHION = PARTS_ASPECT_FASHION_SUB + ('neiyi', 'neiku')
PARTS_ASPECT_BODY = ('body',
 'leg',
 'hand',
 'shoe',
 'cape')
PARTS_ASPECT_CLANWAR = ('clanWarArmor',)
PARTS_PHYSIQUE = ('face', 'hair')
FASHION_DICT = {'neiyi': 'body',
 'neiku': 'leg'}
ALL_AVAIABLE_MODELS = (10004,
 10005,
 10006,
 10009,
 10007,
 10010)
SPECIAL_MODEL_TRANSFER = {10007: 10005,
 10010: 10006}

class MultiPartRes(object):

    def __init__(self):
        super(MultiPartRes, self).__init__()
        self.ownerId = 0
        self.bodyType = None
        self.school = None
        self.sex = const.SEX_MALE
        self.isAvatar = False
        self.headType = HEAD_TYPE0
        self.face = PART_NOT_EQUIPPED
        self.hair = PART_NOT_EQUIPPED
        self.head = PART_NOT_EQUIPPED
        self.shoe = PART_NOT_EQUIPPED
        self.leg = PART_NOT_EQUIPPED
        self.body = PART_NOT_EQUIPPED
        self.hand = PART_NOT_EQUIPPED
        self.cape = PART_NOT_NEED
        self.dyesDict = None
        self.avatarConfig = None
        self.applyConfig = True
        self.mattersDict = None
        self.handLength = HAND_LENGTH_0

    def _getPartPath(self, bodyType, part, partValue):
        if partValue == PART_NOT_EQUIPPED:
            return getPartPath(bodyType, part, partValue, True)
        path = getPartPath(bodyType, part, partValue, False)
        return path

    def getPrerequisites(self):
        gamelog.debug('b.e.: getPrerequisites', self.bodyType, self.school, self.sex)
        gamelog.debug('b.e.: getPrerequisites parts: ', self.face, self.hair, self.head, self.shoe, self.leg, self.body, self.hand, self.cape)
        filelist = []
        if self.isAvatar and gameglobal.rds.isSinglePlayer and gameglobal.ANNAL_STATE != gameglobal.ANNAL_STATE_START:
            filelists = TD.avatar_random_create_data
            filelist = filelists[random.randint(0, len(filelists) - 1)]
            return filelist
        if self.school in SD.data.keys() or gameglobal.rds.isSinglePlayer:
            modelId = transBodyType(self.sex, self.bodyType)
            dummyModelId = transDummyBodyType(self.sex, self.bodyType, self.isAvatar)
            for part in PARTS_ASPECT_BODY:
                partValue = getattr(self, part, PART_NOT_EQUIPPED)
                if partValue in (None, PART_NOT_NEED):
                    continue
                realModelId = transRealBodyType(self.sex, self.bodyType, partValue)
                if part == 'hand' and partValue != PART_NOT_EQUIPPED and self.handLength:
                    path = getHandPath(realModelId, partValue, self.handLength)
                elif part == 'shoe' and partValue == PART_NOT_EQUIPPED:
                    path = getNakedShoePath(realModelId, self.leg)
                elif part == 'leg' and partValue == PART_NOT_EQUIPPED:
                    path = getLegPath(realModelId, self.leg, self.shoe)
                else:
                    path = self._getPartPath(realModelId, part, partValue)
                filelist.append(path)

            filelist.extend(getHeadHairPath(modelId, self.face, self.hair, self.head, self.headType))
            filelist.append('char/%d/dummy.model' % dummyModelId)
        else:
            filelist.append('char/10004/base.model')
        if self.applyConfig:
            matterDyePairs = self.getMatterDyePairs()
            if matterDyePairs:
                for matterDye in matterDyePairs:
                    filelist.append(matterDye)

            if self.avatarConfig:
                boneData = self.getBoneConfigData()
                if boneData:
                    filelist.append(boneData)
        filelist = self.__deduplicate(filelist)
        gamelog.debug('b.e.: getPrerequisites filelist:', filelist)
        return filelist

    def getHairPath(self):
        bodyType = transBodyType(self.sex, self.bodyType)
        headType = self.headType
        hair = self.hair
        head = self.head
        if headType == HEAD_TYPE0:
            if hair != None:
                return getHairPath(bodyType, hair)
        else:
            if headType == HEAD_TYPE1:
                return
            if headType == HEAD_TYPE2 and head != None:
                path = getPartPath(bodyType, 'hair', head, False, 'hair')
                return path

    def getHeadPath(self):
        bodyType = transBodyType(self.sex, self.bodyType)
        headType = self.headType
        head = self.head
        face = self.face
        path = None
        if headType == HEAD_TYPE0:
            if face != None:
                path = getHeadPath(bodyType, face)
            return (headType, path)
        if headType == HEAD_TYPE1:
            if head != None:
                path = getPartPath(bodyType, 'head', head, False, 'head')
            return (headType, path)
        if headType == HEAD_TYPE2:
            if face != None:
                path = getHeadPath(bodyType, face)
            return (headType, path)
        return (headType, path)

    def __deduplicate(self, filelist):
        output = []
        for x in filelist:
            if x not in output:
                output.append(x)

        return output

    def queryByAvatar(self, avatar):
        if not avatar:
            return
        if hasattr(avatar, 'IsAvatar'):
            self.isAvatar = True
        else:
            self.isAvatar = False
        self.ownerId = avatar.id
        avatarConfig = getattr(avatar, 'realAvatarConfig', None)
        interactiveChangeFashionId = getattr(avatar, 'interactiveChangeFashionId', 0)
        self.queryByAttribute(avatar.realPhysique, avatar.realAspect, avatar.isShowFashion(), avatarConfig, avatar.isShowClanWar(), getattr(avatar, 'inWenQuanState', False), avatar.checkNeiYiBuff(), avatar.isHideFashionHead(), interactiveChangeFashionId=interactiveChangeFashionId)

    def getEquipHead(self, aspect, isHideFashionHead = False):
        if aspect.fashionHead and not isHideFashionHead:
            return aspect.fashionHead
        return aspect.head

    def getEquipHeadDyeList(self, aspect, isHideFashionHead = False):
        if aspect.fashionHead and not isHideFashionHead:
            return aspect.fashionHeadDyeList()
        return aspect.headDyeList()

    def getDyeDict(self, aspect, showFashion = False, inClanWar = False, inWenQuan = False, forceShowNeiYi = False, isHideFashionHead = False, interactiveChangeFashionId = 0):
        if inWenQuan:
            dyesDict = {}
            for i, part in enumerate(PARTS_ASPECT_FASHION):
                partId = getattr(aspect, part)
                isVisibleInWenQuan = ED.data.get(partId, {}).get('isVisibleInWenQuan', False)
                if isVisibleInWenQuan:
                    fashoinDyeList = part + 'DyeList'
                    if part in FASHION_DICT:
                        parts_aspect = FASHION_DICT[part]
                    else:
                        parts_aspect = PARTS_ASPECT[i]
                    dyesDict[parts_aspect] = getattr(aspect, fashoinDyeList)()

        elif inClanWar:
            bodyDyeList = []
            if inClanWar != gameglobal.CLAN_WAR_FASHION_TYPE_NO_COLOR:
                bodyDyeList = aspect.clanWarArmorDyeList()
            dyesDict = {'head': [],
             'shoe': [],
             'leg': [],
             'body': bodyDyeList,
             'hand': [],
             'cape': []}
        elif interactiveChangeFashionId:
            dyesDict = {'head': [],
             'shoe': [],
             'leg': [],
             'body': [],
             'hand': [],
             'cape': []}
            _dyeList = ED.data.get(interactiveChangeFashionId, {}).get('dyeList', None)
            dyesDict['body'] = _dyeList
        elif not showFashion:
            dyesDict = {'head': self.getEquipHeadDyeList(aspect, isHideFashionHead),
             'shoe': aspect.shoeDyeList(),
             'leg': aspect.legDyeList(),
             'body': aspect.bodyDyeList(),
             'hand': aspect.handDyeList(),
             'cape': []}
        elif (aspect.neiyi or aspect.neiku) and not self.hasFashion(aspect):
            dyesDict = {'head': [],
             'shoe': [],
             'leg': aspect.neikuDyeList(),
             'body': aspect.neiyiDyeList(),
             'hand': [],
             'cape': []}
        else:
            dyesDict = {'head': self.getEquipHeadDyeList(aspect, isHideFashionHead),
             'shoe': aspect.fashionShoeDyeList(),
             'leg': aspect.fashionLegDyeList(),
             'body': aspect.fashionBodyDyeList(),
             'hand': aspect.fashionHandDyeList(),
             'cape': aspect.fashionCapeDyeList()}
        return dyesDict

    def getMatterDict(self, aspect, showFashion = False, inClanWar = False, inWenQuan = False, forceShowNeiYi = False, isHideFashionHead = False, interactiveChangeFashionId = 0):
        if inWenQuan:
            matterDict = {}
            for i, part in enumerate(PARTS_ASPECT_FASHION):
                partId = getattr(aspect, part)
                isVisibleInWenQuan = ED.data.get(partId, {}).get('isVisibleInWenQuan', False)
                if isVisibleInWenQuan:
                    if part in FASHION_DICT:
                        parts_aspect = FASHION_DICT[part]
                    else:
                        parts_aspect = PARTS_ASPECT[i]
                    fashionPart = getattr(aspect, part)
                    matterDict[parts_aspect] = getMatter(fashionPart)

        elif inClanWar:
            matterDict = {'body': getMatter(aspect.clanWarArmor)}
        elif interactiveChangeFashionId:
            matterDict = {'head': None,
             'shoe': None,
             'leg': None,
             'body': None,
             'hand': None,
             'cape': None}
            matterData = getMatter(interactiveChangeFashionId)
            matterDict['body'] = matterData
        elif not showFashion:
            matterDict = {'head': getMatter(self.getEquipHead(aspect, isHideFashionHead)),
             'shoe': getMatter(aspect.shoe),
             'leg': getMatter(aspect.leg),
             'body': getMatter(aspect.body),
             'hand': getMatter(aspect.hand),
             'cape': getMatter(aspect.cape)}
        elif (aspect.neiyi or aspect.neiku) and not self.hasFashion(aspect):
            matterDict = {'head': None,
             'shoe': None,
             'leg': getMatter(aspect.neiku),
             'body': getMatter(aspect.neiyi),
             'hand': None,
             'cape': None}
        else:
            matterDict = {'head': getMatter(self.getEquipHead(aspect, isHideFashionHead)),
             'shoe': getMatter(aspect.fashionShoe),
             'leg': getMatter(aspect.fashionLeg),
             'body': getMatter(aspect.fashionBody),
             'hand': getMatter(aspect.fashionHand),
             'cape': getMatter(aspect.fashionCape)}
        return matterDict

    def queryByAttribute(self, physique, aspect, showFashion = False, avatarConfig = None, inClanWar = False, inWenQuan = False, forceShowNeiYi = False, isHideFashionHead = False, interactiveChangeFashionId = 0):
        dyesDict = self.getDyeDict(aspect, showFashion, inClanWar, inWenQuan, forceShowNeiYi, isHideFashionHead, interactiveChangeFashionId=interactiveChangeFashionId)
        mattersDict = self.getMatterDict(aspect, showFashion, inClanWar, inWenQuan, forceShowNeiYi, isHideFashionHead, interactiveChangeFashionId=interactiveChangeFashionId)
        if inWenQuan:
            charaterPart = {'fashionHead': PART_NOT_EQUIPPED,
             'fashionBody': aspect.neiyi,
             'fashionLeg': aspect.neiku,
             'fashionShoe': PART_NOT_EQUIPPED,
             'fashionHand': PART_NOT_EQUIPPED,
             'fashionCape': PART_NOT_NEED}
            for part in PARTS_ASPECT_FASHION:
                partId = getattr(aspect, part)
                isVisibleInWenQuan = ED.data.get(partId, {}).get('isVisibleInWenQuan', False)
                if isVisibleInWenQuan:
                    charaterPart[part] = partId

            self.queryByEquip(physique.bodyType, physique.school, physique.sex, physique.face, physique.hair, charaterPart['fashionHead'], charaterPart['fashionShoe'], charaterPart['fashionLeg'], charaterPart['fashionBody'], charaterPart['fashionHand'], charaterPart['fashionCape'], dyesDict, avatarConfig, mattersDict)
        elif inClanWar:
            self.queryByEquip(physique.bodyType, physique.school, physique.sex, physique.face, physique.hair, 0, 0, 0, aspect.clanWarArmor, 0, 0, dyesDict, avatarConfig, mattersDict)
        elif interactiveChangeFashionId:
            charaterPart = {'fashionHead': PART_NOT_EQUIPPED,
             'fashionBody': aspect.neiyi,
             'fashionLeg': aspect.neiku,
             'fashionShoe': PART_NOT_EQUIPPED,
             'fashionHand': PART_NOT_EQUIPPED,
             'fashionCape': PART_NOT_NEED}
            charaterPart['fashionBody'] = interactiveChangeFashionId
            self.queryByEquip(physique.bodyType, physique.school, physique.sex, physique.face, physique.hair, charaterPart['fashionHead'], charaterPart['fashionShoe'], charaterPart['fashionLeg'], charaterPart['fashionBody'], charaterPart['fashionHand'], charaterPart['fashionCape'], dyesDict, avatarConfig, mattersDict)
        elif not showFashion:
            self.queryByEquip(physique.bodyType, physique.school, physique.sex, physique.face, physique.hair, self.getEquipHead(aspect, isHideFashionHead), aspect.shoe, aspect.leg, aspect.body, aspect.hand, aspect.cape, dyesDict, avatarConfig, mattersDict)
        elif forceShowNeiYi:
            self.queryByEquip(physique.bodyType, physique.school, physique.sex, physique.face, physique.hair, PART_NOT_EQUIPPED, PART_NOT_EQUIPPED, aspect.neiku, aspect.neiyi, PART_NOT_EQUIPPED, aspect.cape, dyesDict, avatarConfig, mattersDict)
        elif (aspect.neiyi or aspect.neiku) and not self.hasFashion(aspect):
            self.queryByEquip(physique.bodyType, physique.school, physique.sex, physique.face, physique.hair, PART_NOT_EQUIPPED, PART_NOT_EQUIPPED, aspect.neiku, aspect.neiyi, PART_NOT_EQUIPPED, aspect.cape, dyesDict, avatarConfig, mattersDict)
        else:
            self.queryByEquip(physique.bodyType, physique.school, physique.sex, physique.face, physique.hair, self.getEquipHead(aspect, isHideFashionHead), aspect.fashionShoe, aspect.fashionLeg, aspect.fashionBody, aspect.fashionHand, aspect.fashionCape, dyesDict, avatarConfig, mattersDict)

    def hasFashion(self, aspect):
        for part in PARTS_ASPECT_FASHION_SUB:
            if hasattr(aspect, part) and getattr(aspect, part):
                return True

        return False

    def queryByEquip(self, bodyType, school, sex, face, hair, head, shoe, leg, body, hand, cape, dyesDict = None, avatarConfig = None, mattersDict = None):
        modelId = transBodyType(sex, bodyType)
        headModel = getEquipModelWithParts(head, school, modelId)
        headModel = (headModel[0], None)
        headType = getHeadType(head)
        shoeModel = getEquipModelWithParts(shoe, school, modelId)
        legModel = getEquipModelWithParts(leg, school, modelId)
        bodyModel = getEquipModelWithParts(body, school, modelId)
        handModel = getEquipModelWithParts(hand, school, modelId)
        capeModel = getEquipModelWithParts(cape, school, modelId)
        handLength = getHandLength(hand, body)
        part_parts_data = {'head': headModel,
         'shoe': shoeModel,
         'leg': legModel,
         'body': bodyModel,
         'hand': handModel,
         'cape': capeModel}
        part_data = {'head': PART_NOT_EQUIPPED,
         'shoe': PART_NOT_EQUIPPED,
         'leg': PART_NOT_EQUIPPED,
         'body': PART_NOT_EQUIPPED,
         'hand': PART_NOT_EQUIPPED,
         'cape': PART_NOT_NEED}
        for part in PARTS_ASPECT:
            if part_data.get(part) != PART_NOT_EQUIPPED and part_data.get(part) != PART_NOT_NEED:
                continue
            part_parts_value = part_parts_data.get(part)
            if part_parts_value == None or part_parts_value[0] == PART_NOT_EQUIPPED:
                continue
            part_data[part] = part_parts_value[0]
            if not part_parts_value[1]:
                continue
            for subPart in part_parts_value[1]:
                subType = None
                if subPart.startswith('head'):
                    subType = int(subPart[4:]) if subPart[4:] else HEAD_TYPE0
                    subPart = 'head'
                if part_data.get(subPart) == PART_NOT_EQUIPPED:
                    part_data[subPart] = None
                    if subPart == 'head' and subType != None:
                        headType = subType

        self.queryByModel(bodyType, school, sex, face, hair, part_data.get('head'), part_data.get('shoe'), part_data.get('leg'), part_data.get('body'), part_data.get('hand'), part_data.get('cape'), headType, dyesDict, avatarConfig, mattersDict, handLength)

    def queryByModel(self, bodyType, school, sex, face, hair, head, shoe, leg, body, hand, cape, headType = HEAD_TYPE0, dyesDict = None, avatarConfig = None, mattersDict = None, handLength = HAND_LENGTH_0):
        self.bodyType = bodyType
        self.school = school
        self.sex = sex
        self.face = face
        self.hair = hair
        self.head = head
        self.shoe = shoe
        self.leg = leg
        self.body = body
        self.hand = hand
        self.cape = cape
        self.headType = headType
        self.dyesDict = dyesDict
        self.avatarConfig = avatarConfig
        self.mattersDict = mattersDict
        self.handLength = handLength

    def getBoneConfigFile(self):
        modelId = transDummyBodyType(self.sex, self.bodyType, True)
        bodyFile = 'char/%d/config/body'
        faceFile = 'char/%d/config/face'
        return (bodyFile % modelId, faceFile % modelId)

    def getBoneConfigData(self):
        if self.avatarConfig:
            configFile = self.getBoneConfigFile()
            strMap = strmap.strmap(self.avatarConfig)
            faceBones = strMap.get('faceBones', '')
            bodyBones = strMap.get('bodyBones', '')
            configData = ''
            if bodyBones and faceBones:
                configData = bodyBones + '\n' + faceBones
            elif faceBones:
                configData = faceBones
            elif bodyBones:
                configData = bodyBones
            if configData:
                return (configFile, configData)

    def getMatterDyePairs(self):
        modelId = transBodyType(self.sex, self.bodyType)
        dummyModelId = transDummyBodyType(self.sex, self.bodyType, True)
        buildDyeMorpher = DM.BuildDyeMorpher(modelId, dummyModelId, self.face, self.hair, self.head, self.body, self.hand, self.leg, self.shoe, self.headType, self.dyesDict, self.mattersDict, self.ownerId, cape=self.cape)
        buildDyeMorpher.readConfig(self.avatarConfig)
        buildDyeMorpher.buildDynamicTintAll()
        return buildDyeMorpher.matterDyes


def getHeadHairPath(bodyType, face, hair, head, headType):
    filelist = []
    gamelog.debug('b.e.:getHeadHairPath', bodyType, face, hair, head, headType)
    if headType == HEAD_TYPE0:
        if face != None:
            path = getHeadPath(bodyType, face)
            filelist.append(path)
        if hair != None:
            path = getHairPath(bodyType, hair)
            filelist.append(path)
    elif headType == HEAD_TYPE1:
        if head == None:
            return filelist
        path = getPartPath(bodyType, 'head', head, False, 'head')
        filelist.append(path)
    elif headType == HEAD_TYPE2:
        if face != None:
            path = getHeadPath(bodyType, face)
            filelist.append(path)
        if head == None:
            return filelist
        path = getPartPath(bodyType, 'hair', head, False, 'hair')
        filelist.append(path)
    gamelog.debug('b.e.:getHeadHairPath', filelist)
    return filelist


def getHeadPath(bodyType, head):
    path = getPartPath(bodyType, 'head', head)
    return path


def getHairPath(bodyType, hair):
    path = getPartPath(bodyType, 'hair', hair)
    return path


def getHairNode(bodyType, hair):
    path = getPartPath(bodyType, 'gd_hair', hair, False, 'hair')
    return path


def getNakedShoePath(bodyType, leg):
    if needFootAsShoe(leg, PART_NOT_EQUIPPED):
        return getPartPath(bodyType, 'foot', PART_NOT_EQUIPPED, True)
    return getPartPath(bodyType, 'shoe', PART_NOT_EQUIPPED, True)


def getLegPath(bodyType, leg, shoe):
    if needLegAsTui(leg, shoe):
        return getPartPath(bodyType, 'tui', PART_NOT_EQUIPPED, True)
    return getPartPath(bodyType, 'leg', leg, True)


def getHandPath(bodyType, hand, handLength):
    handPath = getPartPath(bodyType, 'hand', hand, False)
    if handLength:
        array = handPath.split('.')
        return '%s_%02d.%s' % (array[0], handLength, array[1])
    return handPath


def needLegAsTui(leg, shoe):
    return leg == PART_NOT_EQUIPPED and (shoe < 10000 or shoe > 39999)


def needFootAsShoe(leg, shoe):
    return shoe == PART_NOT_EQUIPPED and leg >= 10000 and leg <= 39999


def getHeadType(headId):
    data = ED.data.get(headId, {})
    headType = data.get('bodyLength', HEAD_TYPE0)
    return headType


def getHandLength(handId, bodyId):
    handData = ED.data.get(handId, {})
    handLengthType = handData.get('handLengthType', 0)
    if handLengthType:
        bodyData = ED.data.get(bodyId, {})
        handLength = bodyData.get('handLength', HAND_LENGTH_0)
        if handLength <= handLengthType:
            return handLength
    return HAND_LENGTH_0


def getEquipModel(itemId, school = None, bodyType = None):
    equipModel = getEquipModelWithParts(itemId, school, bodyType)
    if equipModel == None:
        return
    return equipModel[0]


def getEquipModelWithParts(itemId, school = None, bodyType = None):
    if itemId == None or itemId == PART_NOT_NEED:
        return
    else:
        itemId = int(itemId)
        if ED.data.has_key(itemId):
            ed = ED.data[itemId]
            modelId = ed.get('modelId', PART_NOT_EQUIPPED)
            parts = ed.get('parts', None)
            data = ERD.data.get(modelId, None)
            if data:
                for item in data['reference']:
                    if item and item[0] == bodyType and (item[1] == const.SCHOOL_DEFAULT or item[1] == school):
                        modelId = item[2]
                        break

            return (modelId, parts)
        return (PART_NOT_EQUIPPED, None)


def getMatter(itemId):
    if itemId == None or itemId == PART_NOT_NEED:
        return
    itemId = int(itemId)
    return ED.data.get(itemId, {}).get('materials', None)


def convertToMultiPartRes(itemData, entityId = 0):
    if itemData.has_key('mpr'):
        return itemData.pop('mpr')
    multiPart = MultiPartRes()
    multiPart.ownerId = entityId
    bodyType = itemData.get('bodyType', 0)
    school = itemData.get('school', 0)
    sex = itemData.get('sex', const.SEX_MALE)
    face = itemData.get('face', PART_NOT_EQUIPPED)
    hair = itemData.get('hair', PART_NOT_EQUIPPED)
    head = itemData.get('head', PART_NOT_EQUIPPED) or itemData.get('part_%d' % gametypes.EQU_PART_HEAD, PART_NOT_EQUIPPED)
    shoe = itemData.get('shoe', PART_NOT_EQUIPPED) or itemData.get('part_%d' % gametypes.EQU_PART_SHOE, PART_NOT_EQUIPPED)
    leg = itemData.get('leg', PART_NOT_EQUIPPED) or itemData.get('part_%d' % gametypes.EQU_PART_LEG, PART_NOT_EQUIPPED)
    body = itemData.get('body', PART_NOT_EQUIPPED) or itemData.get('part_%d' % gametypes.EQU_PART_BODY, PART_NOT_EQUIPPED)
    hand = itemData.get('hand', PART_NOT_EQUIPPED) or itemData.get('part_%d' % gametypes.EQU_PART_HAND, PART_NOT_EQUIPPED)
    cape = itemData.get('cape', PART_NOT_NEED) or itemData.get('part_%d' % gametypes.EQU_PART_CAPE, PART_NOT_NEED)
    headType = itemData.get('headType', HEAD_TYPE0)
    dyesDict = itemData.get('dyesDict', None)
    mattersDict = itemData.get('mattersDict', None)
    avatarConfig = itemData.get('avatarConfig')
    isAvatar = itemData.get('isAvatar', True)
    handLength = itemData.get('handLength', HAND_LENGTH_0)
    multiPart.isAvatar = isAvatar
    if itemData.get('transModelId', False):
        multiPart.queryByEquip(bodyType, school, sex, face, hair, head, shoe, leg, body, hand, cape, dyesDict, avatarConfig, mattersDict)
    else:
        multiPart.queryByModel(bodyType, school, sex, face, hair, head, shoe, leg, body, hand, cape, headType, dyesDict, avatarConfig, mattersDict, handLength)
    return multiPart


def transBodyType(sex, bodyType):
    modelId = MODEL_BASE + (sex % 2 and bodyType * 2 - 1 or bodyType * 2)
    if SPECIAL_MODEL_TRANSFER.has_key(modelId):
        modelId = SPECIAL_MODEL_TRANSFER[modelId]
    return modelId


def transDummyBodyType(sex, bodyType, isAvatar):
    if isAvatar:
        return MODEL_BASE + (sex % 2 and bodyType * 2 - 1 or bodyType * 2)
    else:
        return NPC_MODEL_BASE + (sex % 2 and bodyType * 2 - 1 or bodyType * 2)


def transRealBodyType(sex, bodyType, partValue):
    modelId = transBodyType(sex, bodyType)
    avatarModelId = transDummyBodyType(sex, bodyType, True)
    return transRealBodyType2(modelId, avatarModelId, partValue)


def transRealBodyType2(modelId, avatarModelId, partValue):
    if avatarModelId in SPECIAL_MODEL_TRANSFER.keys():
        clothModel = SCD.data.get('%s_CLOTH_MODEL' % avatarModelId, (PART_NOT_EQUIPPED, 1))
        if partValue in clothModel:
            return avatarModelId
    return modelId


def retransBodyType(sex, modelId):
    return sex % 2 and (modelId - MODEL_BASE + sex) / 2 or (modelId - MODEL_BASE) / 2


def retransGender(modelId):
    return modelId % 2 and const.SEX_MALE or const.SEX_FEMALE


def getSimpleModel(modelName, dyeName, callback = None):
    threadID = gameglobal.getLoadThread()
    try:
        if dyeName:
            clientUtils.fetchModel(threadID, callback, modelName, ('*', dyeName))
        else:
            clientUtils.fetchModel(threadID, callback, modelName)
    except:
        modelName = gameglobal.defaultModelName
        clientUtils.fetchModel(threadID, callback, modelName)


def getPartType(part):
    if part in ('hair', 'head', 'face', 'headdress'):
        return part
    else:
        return 'cloth'


def getPartPath(bodyType, part, partValue, isBare = False, partType = None):
    equip = '%05d' % partValue
    if partType == None:
        partType = getPartType(part)
    if isBare:
        if partType == 'cloth':
            equip = '00000'
        elif partType == 'hair':
            partValue = SCD.data.get('hair_%d' % bodyType, 1)
            equip = '%05d' % partValue
        elif partType == 'head':
            partValue = SCD.data.get('head_%d' % bodyType, 0)
            equip = '%05d' % partValue
    if equip[0] == '4' and partType not in ('hair', 'head'):
        subEquip = equip[1:3]
    else:
        subEquip = '00'
    fileName = '_'.join((str(bodyType),
     equip,
     subEquip,
     part)) + '.model'
    dirName = 'char/%d/model/%s/%s/' % (bodyType, partType, equip)
    return dirName + fileName


def getPartTexturePath(bodyType, part, partValue, matter, tga, tgaValue = 1, isBare = False, partType = None, fusionValue = 0):
    equip = '%05d' % partValue
    texture = '%03d' % tgaValue
    fusionTexture = '%03d' % fusionValue if fusionValue else None
    if partType == None:
        partType = getPartType(part)
    if isBare:
        if partType == 'cloth':
            equip = '00000'
        elif partType == 'hair':
            partValue = SCD.data.get('hair_%d' % bodyType, 1)
            equip = '%05d' % partValue
        elif partType == 'head':
            partValue = SCD.data.get('head_%d' % bodyType, 0)
            equip = '%05d' % partValue
        texture = '001'
        fusionTexture = None
    if fusionTexture != None and fusionTexture != texture:
        texture = texture + '_' + fusionTexture
    fileName = '_'.join((str(bodyType),
     equip,
     matter,
     tga,
     texture)) + '.tga'
    dirName = 'char/%d/model/%s/%s/texture/' % (bodyType, partType, equip)
    return dirName + fileName


class RongGuangRes(object):
    CubeTex = 'env/pbr_cubemap/s/rg_00%d_specular_.dds'

    def __init__(self):
        super(RongGuangRes, self).__init__()
        self.rongGuangDict = {}
        self.dutyOverCallBack = None

    def dutyOver(self):
        if self.dutyOverCallBack:
            self.dutyOverCallBack()

    def queryByAvatar(self, avatar):
        if not avatar or not avatar.inWorld or not hasattr(avatar, 'realAspect'):
            return
        self.queryByAttribute(avatar.realAspect, avatar.isShowFashion(), avatar.isShowClanWar(), getattr(avatar, 'inWenQuanState', False))

    def queryByAttribute(self, aspect, showFashion = False, inClanWar = False, inWenQuan = False):
        self.rongGuangDict = self.getRongGuangDict(aspect, showFashion, inClanWar, inWenQuan)

    def getRongGuangDict(self, aspect, showFashion = False, inClanWar = False, inWenQuan = False):
        if inClanWar or inWenQuan:
            return {}
        else:
            rongGuangDict = {}
            parts = PARTS_ASPECT_FASHION if showFashion else PARTS_ASPECT
            for part in zip(PARTS_ASPECT, parts):
                rongGuang = getattr(aspect, part[1] + 'RongGuang')()
                if rongGuang:
                    rongGuangDict[part[0]] = rongGuang

            return rongGuangDict

    def apply(self, model, needXuanren = False, cfType = 0, dutyOverCallBack = None):
        self.dutyOverCallBack = dutyOverCallBack
        xuanrenTint = gameglobal.rds.xuanrenTint
        if needXuanren and cfType:
            if cfType == const.SHADER_TYPE_C:
                xuanrenTint = 'cmianban'
            else:
                xuanrenTint = 'fmianban'
        if not self.rongGuangDict:
            TA.ta_del([model], 'rongGuang', None, True, False, TA.AVATARTINT)
            if needXuanren:
                TA.ta_add([model], xuanrenTint, [], tintType=TA.AVATARTINT)
            self.dutyOver()
            return
        TA.ta_del([model], 'rongGuang', None, True, True, TA.AVATARTINT)
        rongGuangName = 'rongGuang'
        if needXuanren:
            rongGuangName += xuanrenTint[0].upper() + xuanrenTint[1:]
        tintNames = []
        matters = []
        for matter, param in self.rongGuangDict.iteritems():
            tintNames.append(rongGuangName)
            matters.append(matter)

        clientcom.fetchTintEffectContentsByName(tintNames, Functor(self.realApply, model, rongGuangName, matters, tintNames))

    def realApply(self, model, rongGuangName, matters, tintNames, tintEffects):
        if not model or not model.inWorld:
            self.dutyOver()
            return
        if tintEffects:
            model.tintCopy = dict(zip(tintNames, tintEffects))
        for matter in matters:
            param = self.rongGuangDict[matter]
            if len(param) < 3:
                param = (1, 1, 1)
            param = (self.CubeTex % int(param[0]), param[1], param[2])
            if param:
                TA.ta_add([model], rongGuangName, param, 0, matter, applyLater=True, tintType=TA.AVATARTINT)

        TA.ta_apply([model], tintName=rongGuangName)
        TA.clearTintCopy(model.tintCopy)
        model.tintCopy = None
        self.dutyOver()


class RongGuangResDutyList(object):

    def __init__(self):
        super(RongGuangResDutyList, self).__init__()
        self.dutyList = []
        self.isDoingDuty = False

    def addDuty(self, avatar, needXuanren = False):
        rongGuang = RongGuangRes()
        rongGuang.queryByAvatar(avatar)
        self.dutyList.append(Functor(rongGuang.apply, avatar.modelServer.bodyModel, needXuanren, 0, self.doNextDuty))
        if not self.isDoingDuty:
            self.doNextDuty()

    def doNextDuty(self):
        if self.dutyList:
            self.isDoingDuty = True
            nextDuty = self.dutyList.pop(0)
            nextDuty()
        else:
            self.isDoingDuty = False
