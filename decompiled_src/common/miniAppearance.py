#Embedded file name: I:/bag/tmp/tw2/res/entities\common/miniAppearance.o
import gametypes
from userSoleType import UserSoleType
from userType import MemberProxy

class MiniAppearanceMeta(type):

    def __init__(cls, name, bases, dic):
        super(MiniAppearanceMeta, cls).__init__(name, bases, dic)
        for partName in gametypes.ASPECT_PART_DICT.iterkeys():
            dyeListName = partName + 'DyeList'
            enhLvName = partName + 'EnhLv'
            attrName = partName + 'Attr'
            rongGuangName = partName + 'RongGuang'

            def getDyeList(self, partName_ = partName):
                return []

            def getEnh(self, partName_ = partName):
                return 0

            def getRongGuang(self, partName_ = partName):
                return []

            setattr(cls, dyeListName, getDyeList)
            setattr(cls, enhLvName, getEnh)
            setattr(cls, rongGuangName, getRongGuang)

            def getAttr(self, partName_ = partName):
                return str((getattr(self, partName_, 0), getattr(self, partName_ + 'DyeList')(), getattr(self, partName_ + 'EnhLv')()))

            setattr(cls, attrName, getAttr)


class MiniAppearance(UserSoleType):
    __metaclass__ = MiniAppearanceMeta
    leftWeapon = MemberProxy('leftWeapon')
    rightWeapon = MemberProxy('rightWeapon')
    wingFly = MemberProxy('wingFly')
    ride = MemberProxy('ride')
    clanWarArmor = MemberProxy('clanWarArmor')

    def __init__(self, dict):
        super(MiniAppearance, self).__init__()
        for part, partName in gametypes.ASPECT_PART_REV_DICT.iteritems():
            if part in gametypes.ASPECT_PART_MINIMUN:
                if not dict.has_key(partName):
                    dict[partName] = 0
            else:
                setattr(self, partName, 0)

        self.enhLvs = {}
        self.dyeLists = {}
        self.rongGuangs = {}
        self.fixedDict = dict

    def deepcopy(self):
        return {'leftWeapon': self.leftWeapon,
         'rightWeapon': self.rightWeapon,
         'wingFly': self.wingFly,
         'ride': self.ride,
         'clanWarArmor': self.clanWarArmor}

    def set(self, part, id):
        if part in gametypes.ASPECT_PART_MINIMUN:
            partName = gametypes.ASPECT_PART_REV_DICT[part]
            setattr(self, partName, id)

    def __cmp__(self, v):
        return cmp(v.fixedDict, self.fixedDict)

    def getEnhLvsSum(self):
        return 0

    def isEmpty(self):
        for part in gametypes.ASPECT_PART_MINIMUN:
            partName = gametypes.ASPECT_PART_REV_DICT[part]
            if getattr(self, partName, None):
                return False

        return True

    def clear(self):
        for part in gametypes.ASPECT_PART_MINIMUN:
            setattr(self, part, 0)
