#Embedded file name: /WORKSPACE/data/entities/common/appearance.o
import copy
import gametypes
import const
from userSoleType import UserSoleType
from userType import MemberProxy

class AppearanceMeta(type):

    def __init__(cls, name, bases, dic):
        super(AppearanceMeta, cls).__init__(name, bases, dic)
        for partName in gametypes.ASPECT_PART_DICT.iterkeys():
            dyeListName = partName + 'DyeList'
            enhLvName = partName + 'EnhLv'
            attrName = partName + 'Attr'
            rongGuangName = partName + 'RongGuang'

            def getDyeList(self, partName_ = partName):
                part = gametypes.ASPECT_PART_DICT[partName_]
                dyeList = self.dyeLists.get(part, [])
                if dyeList:
                    if part in (gametypes.EQU_PART_RIDE, gametypes.EQU_PART_WINGFLY):
                        return dyeList
                    dyeList = list(dyeList)
                    for i, item in enumerate(dyeList):
                        if i >= const.DYES_INDEX_COLOR and i < const.DYES_INDEX_TEXTURE or i >= const.DYES_INDEX_DUAL_COLOR and i < const.DYES_INDEX_PBR_TEXTURE_DEGREE:
                            dyeList[i] = self.colorInt2Str(item)
                        else:
                            dyeList[i] = str(item)

                return dyeList

            def getEnh(self, partName_ = partName):
                part = gametypes.ASPECT_PART_DICT[partName_]
                enhLv = self.enhLvs.get(part, 0)
                return enhLv

            def getRongGuang(self, partName_ = partName):
                part = gametypes.ASPECT_PART_DICT[partName_]
                rongGuang = self.rongGuangs.get(part, [])
                return rongGuang

            setattr(cls, dyeListName, getDyeList)
            setattr(cls, enhLvName, getEnh)
            setattr(cls, rongGuangName, getRongGuang)

            def getAttr(self, partName_ = partName):
                return str((getattr(self, partName_, 0), getattr(self, partName_ + 'DyeList')(), getattr(self, partName_ + 'EnhLv')()))

            setattr(cls, attrName, getAttr)


class Appearance(UserSoleType):
    __metaclass__ = AppearanceMeta
    head = MemberProxy('head')
    body = MemberProxy('body')
    shoe = MemberProxy('shoe')
    hand = MemberProxy('hand')
    leg = MemberProxy('leg')
    cape = MemberProxy('cape')
    necklace = MemberProxy('necklace')
    ring1 = MemberProxy('ring1')
    ring2 = MemberProxy('ring2')
    leftWeapon = MemberProxy('leftWeapon')
    rightWeapon = MemberProxy('rightWeapon')
    wingFly = MemberProxy('wingFly')
    ride = MemberProxy('ride')
    fashionHead = MemberProxy('fashionHead')
    fashionBody = MemberProxy('fashionBody')
    fashionShoe = MemberProxy('fashionShoe')
    fashionHand = MemberProxy('fashionHand')
    fashionLeg = MemberProxy('fashionLeg')
    fashionCape = MemberProxy('fashionCape')
    fishingRod = MemberProxy('fishingRod')
    earring1 = MemberProxy('earring1')
    earring2 = MemberProxy('earring2')
    yaopei = MemberProxy('yaopei')
    clanWarArmor = MemberProxy('clanWarArmor')
    headdress = MemberProxy('headdress')
    headdressRight = MemberProxy('headdressRight')
    headdressLeft = MemberProxy('headdressLeft')
    facewear = MemberProxy('facewear')
    waistwear = MemberProxy('waistwear')
    backwear = MemberProxy('backwear')
    tailwear = MemberProxy('tailwear')
    chestwear = MemberProxy('chestwear')
    earwear = MemberProxy('earwear')
    rightFashionWeapon = MemberProxy('rightFashionWeapon')
    leftFashionWeapon = MemberProxy('leftFashionWeapon')
    yuanLing = MemberProxy('yuanLing')
    wuHun = MemberProxy('wuHun')
    enhLvs = MemberProxy('enhLvs')
    dyeLists = MemberProxy('dyeLists')
    rongGuangs = MemberProxy('rongGuangs')
    neiyi = MemberProxy('neiyi')
    neiku = MemberProxy('neiku')
    footdust = MemberProxy('footdust')

    def __init__(self, dict):
        super(Appearance, self).__init__()
        for partName in gametypes.ASPECT_PART_DICT.iterkeys():
            if not dict.has_key(partName):
                dict[partName] = 0

        if not dict.has_key('enhLvs') or dict['enhLvs'] == None:
            dict['enhLvs'] = {}
        if not dict.has_key('dyeLists') or dict['dyeLists'] == None:
            dict['dyeLists'] = {}
        if not dict.has_key('rongGuangs') or dict['rongGuangs'] == None:
            dict['rongGuangs'] = {}
        for index, val in dict['enhLvs'].get('ext', {}).iteritems():
            if index in gametypes.ASPECT_USING_EXT:
                attrName = gametypes.ASPECT_PART_REV_DICT.get(index)
                if attrName:
                    dict[attrName] = val

        self.fixedDict = dict
        self.calSlotCountSelf()

    def getPersistentKeys(self):
        excludeKeys = [ gametypes.ASPECT_PART_REV_DICT.get(k) for k in gametypes.ASPECT_USING_EXT ]
        aspectKeys = [ k for k in self.fixedDict.keys() if k not in excludeKeys ]
        return aspectKeys

    def reloadScript(self):
        super(Appearance, self).reloadScript()

    def calSlotCountSelf(self):
        count = 0
        for part in gametypes.ASPECT_PART_DICT.iterkeys():
            if getattr(self, part, None):
                count += 1

        self.slotCount = count

    def deepcopy(self):
        return {'head': self.head,
         'body': self.body,
         'shoe': self.shoe,
         'hand': self.hand,
         'leg': self.leg,
         'cape': self.cape,
         'necklace': self.necklace,
         'ring1': self.ring1,
         'ring2': self.ring2,
         'leftWeapon': self.leftWeapon,
         'rightWeapon': self.rightWeapon,
         'wingFly': self.wingFly,
         'fashionHead': self.fashionHead,
         'fashionBody': self.fashionBody,
         'fashionShoe': self.fashionShoe,
         'fashionHand': self.fashionHand,
         'fashionCape': self.fashionCape,
         'fashionLeg': self.fashionLeg,
         'fishingRod': self.fishingRod,
         'clanWarArmor': self.clanWarArmor,
         'earring1': self.earring1,
         'earring2': self.earring2,
         'yaopei': self.yaopei,
         'headdress': self.headdress,
         'headdressRight': self.headdressRight,
         'headdressLeft': self.headdressLeft,
         'facewear': self.facewear,
         'waistwear': self.waistwear,
         'backwear': self.backwear,
         'tailwear': self.tailwear,
         'chestwear': self.chestwear,
         'earwear': self.earwear,
         'rightFashionWeapon': self.rightFashionWeapon,
         'leftFashionWeapon': self.leftFashionWeapon,
         'enhLvs': self.enhLvs,
         'dyeLists': self.dyeLists,
         'rongGuangs': self.rongGuangs,
         'neiyi': self.neiyi,
         'neiku': self.neiku,
         'footdust': self.footdust}

    def colorStr2Int(self, strColor):
        color = eval(strColor)
        return (color[0] << 18) + (color[1] << 9) + color[2] + (color[3] << 27)

    def colorInt2Str(self, color):
        ret = ''
        try:
            ret = '%d,%d,%d,%d' % (color >> 18 & 511,
             color >> 9 & 511,
             color & 511,
             color >> 27)
        except:
            ret = '255,255,255,255'

        return ret

    def getEnhLvsSum(self):
        eSum = 0
        for v in gametypes.ASPECT_PART_DICT.values():
            eSum = eSum + self.enhLvs.get(v, 0)

        return eSum

    def _setExtVal(self, part, id):
        if not self.enhLvs.has_key('ext'):
            self.enhLvs['ext'] = {}
        self.enhLvs['ext'][part] = id

    def dyeListToLocalData(self, dyeList):
        dyeList = list(dyeList)
        for i, item in enumerate(dyeList):
            if i >= const.DYES_INDEX_COLOR and i < const.DYES_INDEX_TEXTURE or i >= const.DYES_INDEX_DUAL_COLOR and i < const.DYES_INDEX_PBR_TEXTURE_DEGREE:
                dyeList[i] = self.colorStr2Int(item)
            else:
                dyeList[i] = float(item)

        dyeList = tuple(dyeList)
        return dyeList

    def set(self, part, id, dyeList = [], enhLv = 0, rongGuang = []):
        if part in gametypes.ASPECT_PART_REV_DICT:
            if id == 0 or id == None:
                if getattr(self, gametypes.ASPECT_PART_REV_DICT[part], 0):
                    self.slotCount -= 1
                setattr(self, gametypes.ASPECT_PART_REV_DICT[part], 0)
                if part in gametypes.ASPECT_USING_EXT:
                    self._setExtVal(part, 0)
                if self.enhLvs.has_key(part):
                    enhLv = self.enhLvs.pop(part)
                    if enhLv:
                        self.enhLvs = copy.copy(self.enhLvs)
                if self.dyeLists.has_key(part):
                    dyeList = self.dyeLists.pop(part)
                    if dyeList:
                        self.dyeLists = copy.copy(self.dyeLists)
                if self.rongGuangs.has_key(part):
                    rongGuang = self.rongGuangs.pop(part)
                    if rongGuang:
                        self.rongGuangs = copy.copy(self.rongGuangs)
            else:
                if not getattr(self, gametypes.ASPECT_PART_REV_DICT[part], 0):
                    self.slotCount += 1
                setattr(self, gametypes.ASPECT_PART_REV_DICT[part], id)
                if part in gametypes.ASPECT_USING_EXT:
                    self._setExtVal(part, id)
                if dyeList:
                    try:
                        if part not in (gametypes.EQU_PART_RIDE, gametypes.EQU_PART_WINGFLY):
                            dyeList = self.dyeListToLocalData(dyeList)
                        hasChange = True if self.dyeLists.get(part, None) != dyeList else False
                        self.dyeLists[part] = dyeList
                    except:
                        hasChange = False
                        self.dyeLists[part] = dyeList
                    finally:
                        if hasChange:
                            self.dyeLists = copy.copy(self.dyeLists)

                elif self.dyeLists.get(part, None):
                    self.dyeLists.pop(part)
                    self.dyeLists = copy.copy(self.dyeLists)
                if self.enhLvs.get(part, 0) != enhLv:
                    self.enhLvs[part] = enhLv
                    self.enhLvs = copy.copy(self.enhLvs)
                rongGuang = [ float(x) for x in rongGuang ]
                if self.rongGuangs.get(part, []) != rongGuang:
                    self.rongGuangs[part] = rongGuang
                    self.rongGuangs = copy.copy(self.rongGuangs)

    def __cmp__(self, v):
        return cmp(v.fixedDict, self.fixedDict)

    def isEmpty(self):
        return self.slotCount == 0

    def clear(self):
        for part in gametypes.ASPECT_PART_REV_DICT:
            setattr(self, gametypes.ASPECT_PART_REV_DICT[part], 0)

        self.enhLvs = {}
        self.dyeLists = {}
        self.rongGuangs = {}
        self.slotCount = 0
