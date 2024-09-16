#Embedded file name: I:/bag/tmp/tw2/res/entities\client\debug/bodyChangeProxy.o
import copy
import BigWorld
import ResMgr
from Scaleform import GfxValue
import gameglobal
import gametypes
import clientcom
import gamelog
import const
from item import Item
from guis.ui import gbk2unicode
from guis.uiProxy import DataProxy
from guis import uiConst
from helpers import charRes
from sfx import sfx
from helpers import avatarMorpher as AM
from cdata import suit_data as SD
from data import item_data as ID
from data import equip_data as ED
EQU_PART_HAIR = -1
HAIR_PATH = 'char/%d/model/hair'

class BodyChangeProxy(DataProxy):
    PART_LIST = [('【头盔】', gametypes.EQU_PART_HEAD),
     ('【衣服】', gametypes.EQU_PART_BODY),
     ('【手套】', gametypes.EQU_PART_HAND),
     ('【腿部】', gametypes.EQU_PART_LEG),
     ('【鞋子】', gametypes.EQU_PART_SHOE),
     ('【主手】', gametypes.EQU_PART_WEAPON_ZHUSHOU),
     ('【副手】', gametypes.EQU_PART_WEAPON_FUSHOU),
     ('【头发】', EQU_PART_HAIR)]
    PART_MAP = {gametypes.EQU_PART_HEAD: 'head',
     gametypes.EQU_PART_BODY: 'body',
     gametypes.EQU_PART_HAND: 'hand',
     gametypes.EQU_PART_LEG: 'leg',
     gametypes.EQU_PART_SHOE: 'shoe'}

    def __init__(self, uiAdapter):
        super(BodyChangeProxy, self).__init__(uiAdapter)
        self.bindType = 'bodyChange'
        self.modelMap = {'chooseCloth': self.onChooseCloth,
         'chooseEquip': self.onChooseEquip,
         'chooseEquipItem': self.onChooseEquipItem,
         'register': self.onRegister,
         'changeAspect': self.onChangeAspect,
         'chooseSchool': self.onChooseSchool,
         'setPhysicsParam': self.onSetPhysicsParam}
        self.mc = None
        self.school = const.SCHOOL_DEFAULT
        self.gender = const.SEX_UNKNOWN
        self.bodyType = 0
        self.suitList = []
        self.partList = []
        self.itemData = None
        self.avatarConfig = ''
        self.weaponData = [0, 0]
        resDir = ResMgr.openSection(gameglobal.AVATAR_TEMPLATE_PATH)
        if resDir:
            self.avatarRes = [ item for item in resDir.keys() if item.endswith('.xml') ]

    def onRegister(self, *arg):
        self.mc = arg[3][0]
        self.bodyType = 0
        self.gender = const.SEX_UNKNOWN
        self.school = const.SCHOOL_DEFAULT
        self.itemData = None
        self.weaponData = [0, 0]

    def onChooseCloth(self, *arg):
        if not self.inValid():
            return
        index = int(arg[3][0].GetNumber())
        suitId = self.suitList[index][1]
        gamelog.debug('b.e.: onChooseCloth', index, suitId)
        self.itemData = self._getItemDataFromSuit(suitId)
        self.avatarConfig = ''
        self.weaponData = self._getWeaponDataFromSuit(suitId)
        self._showAvatar()

    def onChooseEquip(self, *arg):
        if not self.inValid():
            return
        index = int(arg[3][0].GetNumber())
        part = self.PART_LIST[index][1]
        gamelog.debug('b.e.: onChooseEquip', index, part, self.school, self.gender)
        if self.school == const.SCHOOL_DEFAULT:
            return
        self.partList = []
        nl = []
        if part == EQU_PART_HAIR:
            p = BigWorld.player()
            modelId = sfx._getModelId(p.model)
            hairPath = HAIR_PATH % modelId
            section = ResMgr.openSection(hairPath)
            if section:
                for i, key in enumerate(section.keys()):
                    if key.isdigit():
                        nl.append(key)
                        self.partList.append((key, int(key), part))

        else:
            for key, value in ID.data.iteritems():
                if value.get('type') != Item.BASETYPE_EQUIP:
                    continue
                schReq = value.get('schReq', None)
                if schReq and self.school not in schReq:
                    continue
                sexReq = value.get('sexReq', 0)
                if sexReq != 0 and sexReq != self.gender:
                    continue
                ed = ED.data.get(key, None)
                if not ed:
                    continue
                etp = ed.get('equipType')
                if etp == Item.EQUIP_BASETYPE_WEAPON:
                    esp = ed.get('weaponSType')
                elif etp == Item.EQUIP_BASETYPE_ARMOR:
                    esp = ed.get('armorSType')
                elif etp == Item.EQUIP_BASETYPE_JEWELRY:
                    esp = ed.get('jewelSType')
                else:
                    continue
                if etp == None or esp == None:
                    continue
                if part not in Item.EQUIP_PART_TABLE[etp][esp]:
                    continue
                n = '【%s(%d)】' % (value.get('name'), ed.get('modelId', 0))
                self.partList.append((n, key, part))
                nl.append(n)

        self.mc.Invoke('setEquipItemData', self.createAsArray(nl))

    def _getOldHair(self):
        p = BigWorld.player()
        hairPath = None
        for path in p.model.sources:
            if path.endswith('hair.model'):
                hairPath = path

        return int(hairPath.split('/')[-1].split('_')[1])

    def onChooseEquipItem(self, *arg):
        if not self.inValid():
            return
        if self.school == const.SCHOOL_DEFAULT or not self.itemData:
            self.uiAdapter.showTips('请先选择套装或者avatar文件')
            return
        index = int(arg[3][0].GetNumber())
        pd = self.partList[index]
        _, itemId, part = pd
        gamelog.debug('b.e.: onChooseEquipItem', index, itemId, part)
        p = BigWorld.player()
        if part == gametypes.EQU_PART_WEAPON_FUSHOU:
            self.weaponData[0] = itemId
            p.aspect.set(gametypes.EQU_PART_WEAPON_FUSHOU, itemId)
            p.modelServer.weaponUpdate()
        elif part == gametypes.EQU_PART_WEAPON_ZHUSHOU:
            self.weaponData[1] = itemId
            p.aspect.set(gametypes.EQU_PART_WEAPON_ZHUSHOU, itemId)
            p.modelServer.weaponUpdate()
        elif part == EQU_PART_HAIR:
            p.physique.hair = itemId
            p.set_physique(p.physiqueOld)
        else:
            partN = self.PART_MAP.get(part)
            self.itemData[partN] = itemId
            self._showAvatar()

    def onChooseSchool(self, *arg):
        if not self.inValid():
            return
        school = int(arg[3][0].GetNumber())
        gamelog.debug('b.e.: onChooseSchool', school)
        self.school = school
        self.itemData = self._getItemData()
        self.avatarConfig = ''
        self.weaponData = self._getWeaponData()
        self._showAvatar()
        self._chooseSuit()

    def onChangeAspect(self, *arg):
        btnName = arg[3][0].GetString()
        gamelog.debug('b.e.: onChangeAspect', btnName)
        if btnName == 'ok0Btn':
            self.gender = const.SEX_MALE if arg[3][1].GetBool() else const.SEX_FEMALE
            self.bodyType = int(arg[3][2].GetNumber())
            self.itemData = {'school': self.school,
             'multiPart': True,
             'transModelId': True,
             'sex': self.gender,
             'bodyType': self.bodyType}
            self.avatarConfig = None
            self.weaponData = [0, 0]
            self._showAvatar()
        elif btnName == 'ok1Btn':
            if not self.inValid():
                return
            index = int(arg[3][1].GetNumber())
            xml = self.avatarRes[index]
            gamelog.debug('b.e.: chooseClothFromXml', index, xml)
            self.itemData, self.avatarConfig = self._getItemDataFromXml(xml)
            self.weaponData = [0, 0]
            self._showAvatar()
        elif btnName == 'ok2Btn':
            gamelog.debug('ok2Btn', index)
        elif btnName == 'ok3Btn':
            gamelog.debug('ok3Btn')
        elif btnName == 'ok4Btn':
            dranseColor = arg[3][1].GetString()
            sranseColor = arg[3][2].GetString()
            gamelog.debug('ok4Btn', dranseColor, sranseColor)
            data = dict(self.itemData)
            data['avatarConfig'] = self.avatarConfig
            dyesDict = {}
            dyesDict['head'] = [dranseColor, sranseColor]
            dyesDict['hand'] = [dranseColor, sranseColor]
            dyesDict['leg'] = [dranseColor, sranseColor]
            dyesDict['shoe'] = [dranseColor, sranseColor]
            dyesDict['body'] = [dranseColor, sranseColor]
            data['dyesDict'] = dyesDict
            clientcom.setAvatarConfig(None, data, BigWorld.player().model)
            m = AM.SimpleModelMorpher(BigWorld.player().model, data['sex'], data['school'], data['bodyType'], 0, data['hair'], 0, data['body'], data['hand'], data['leg'], data['shoe'], data['transModelId'], charRes.HEAD_TYPE0, data['dyesDict'])
            m.readConfig(self.avatarConfig)
            m.apply()

    def createAsArray(self, array):
        ar = self.movie.CreateArray()
        for i, item in enumerate(array):
            value = GfxValue(gbk2unicode(item))
            ar.SetElement(i, value)
            i = i + 1

        return ar

    def getValue(self, key):
        if key == 'bodyChange.clothList':
            ar = self.createAsArray([])
            return ar
        if key == 'bodyChange.equipList':
            nl = []
            for v in self.PART_LIST:
                nl.append(v[0])

            ar = self.createAsArray(nl)
            return ar
        if key == 'bodyChange.avatarMenu':
            ar = self.createAsArray(self.avatarRes)
            return ar

    def showBodyChangeProxy(self):
        self.uiAdapter.loadWidget(uiConst.WIDGET_DEBUG_BODYCHANGE)

    def _chooseSuit(self):
        self.suitList = []
        nl = []
        for key, value in SD.data.iteritems():
            if key < 1000:
                continue
            schReq = value.get('schReq')
            if schReq and self.school not in schReq:
                continue
            n = '【%s】' % value.get('name')
            self.suitList.append((n, key))
            nl.append(n)

        self.mc.Invoke('setClothData', self.createAsArray(nl))
        self.mc.Invoke('setEquipItemData', self.createAsArray([]))

    def _getPartData(self, part):
        data = gameglobal.rds.loginScene.getCharShowData(self.school, self.gender, self.bodyType)
        if not data:
            data = SD.data[self.school][0]
        return data.get(part, 0)

    def _getItemData(self):
        data = {'school': self.school,
         'multiPart': True,
         'transModelId': True,
         'sex': self.gender,
         'bodyType': self.bodyType}
        data['body'] = self._getPartData('body')
        data['shoe'] = self._getPartData('shoe')
        data['hand'] = self._getPartData('hand')
        data['leg'] = self._getPartData('leg')
        data['hair'] = self._getPartData('hair')
        data['head'] = self._getPartData('head')
        return data

    def _getWeaponData(self):
        fuShou = self._getPartData('fuShou')
        zhuShou = self._getPartData('zhuShou')
        return [fuShou, zhuShou]

    def _getPartDataFromSuit(self, suitId, part):
        if part in ('fuShou', 'zhuShou'):
            return SD.data[suitId].get(part, 0)
        return SD.data[suitId].get(part, -1)

    def _getItemDataFromSuit(self, suitId):
        data = {'school': self.school,
         'multiPart': True,
         'transModelId': True,
         'sex': self.gender,
         'bodyType': self.bodyType}
        data['body'] = self._getPartDataFromSuit(suitId, 'body')
        data['shoe'] = self._getPartDataFromSuit(suitId, 'shoe')
        data['hand'] = self._getPartDataFromSuit(suitId, 'hand')
        data['leg'] = self._getPartDataFromSuit(suitId, 'leg')
        if self.itemData:
            data['hair'] = self.itemData.get('hair', 0)
        data['head'] = self._getPartDataFromSuit(suitId, 'head')
        return data

    def _getWeaponDataFromSuit(self, suitId):
        fuShou = self._getPartDataFromSuit(suitId, 'fuShou')
        zhuShou = self._getPartDataFromSuit(suitId, 'zhuShou')
        return [fuShou, zhuShou]

    def _getItemDataFromXml(self, xml):
        avatarInfo = ResMgr.openSection(gameglobal.AVATAR_TEMPLATE_PATH + '/' + xml)
        if not avatarInfo:
            return
        itemData = clientcom._getAvatarConfigFromFile(avatarInfo)
        avatarConfig = itemData.pop('avatarConfig')
        return (itemData, avatarConfig)

    def _showAvatar(self):
        gamelog.debug('b.e.: bodyChange._showAvatar', self.itemData)
        gamelog.debug('b.e.: bodyChange._showAvatar', self.weaponData)
        p = BigWorld.player()
        p.school = self.school
        p.physique.sex = self.gender
        p.physique.bodyType = self.itemData.get('bodyType', 0)
        p.physique.hair = self.itemData.get('hair', 0)
        p.avatarConfig = self.avatarConfig
        p.physiqueOld = copy.deepcopy(p.physique)
        data = dict(self.itemData)
        data['avatarConfig'] = self.avatarConfig
        mpr = charRes.convertToMultiPartRes(data)
        mpr.isAvatar = False
        resList = mpr.getPrerequisites()
        gamelog.debug('b.e.: bodyChange.loadRes', resList)
        p.aspect.set(gametypes.EQU_PART_WEAPON_FUSHOU, self.weaponData[0])
        p.aspect.set(gametypes.EQU_PART_WEAPON_ZHUSHOU, self.weaponData[1])
        p.allModels = []
        p.modelServer.bodyUpdateOffLine(resList)
        p.modelServer.weaponUpdate()
        if self.avatarConfig:
            clientcom.setAvatarConfig(None, data, p.model)

    def onSetPhysicsParam(self, *arg):
        gamelog.debug('onSetPhysicsParam')
        p = BigWorld.player()
        for part in clientcom.physicsPart:
            if hasattr(p.model, part + 'Physics'):
                getattr(p.model, part + 'Physics').tweak()

    def inValid(self):
        if self.gender == const.SEX_UNKNOWN or self.bodyType == 0:
            self.uiAdapter.showTips('先选择性别体型，然后单击确定')
            return False
        return True
