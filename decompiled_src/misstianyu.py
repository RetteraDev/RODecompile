#Embedded file name: /WORKSPACE/data/entities/common/misstianyu.o
from userSoleType import UserSoleType
from userDictType import UserDictType
import const
from cdata import personal_zone_config_data as PZCD

class MissTianyuGroupVal(UserSoleType):

    def __init__(self, gbId = 0, roleName = '', photo = '', borderId = 0, hostId = 0, val = 0, school = 0, sex = 0):
        super(MissTianyuGroupVal, self).__init__()
        self.gbId = gbId
        self.roleName = roleName
        self.photo = photo
        self.hostId = hostId
        self.borderId = borderId
        self.val = val
        self.school = school
        self.sex = sex

    def _lateReload(self):
        super(MissTianyuGroupVal, self)._lateReload()

    def addVal(self, val, valType):
        factor = 0
        if valType == const.GROUP_VAL_TYPE_PYQ_MT:
            factor = PZCD.data.get('mtPYQFactor', 0)
        elif valType == const.GROUP_VAL_TYPE_GIFT_MT:
            factor = PZCD.data.get('mtGiftFactor', 0)
        elif valType == const.GROUP_VAL_TYPE_GM_MT:
            factor = 1
        self.val += val * factor
        return self.val

    def getDTO(self):
        return (self.gbId,
         self.roleName,
         self.photo,
         self.borderId,
         self.hostId,
         self.val,
         self.school,
         self.sex)

    def fromDTO(self, dto):
        self.gbId, self.roleName, self.photo, self.borderId, self.hostId, self.val, self.school, self.sex = dto

    def toDict(self):
        return {'gbId': self.gbId,
         'roleName': self.roleName,
         'photo': self.photo,
         'school': self.school,
         'borderId': self.borderId,
         'hostId': self.hostId,
         'val': self.val,
         'gender': self.sex}


class MissTianyuPlayoffVal(MissTianyuGroupVal):

    def __init__(self, gbId = 0, roleName = '', photo = '', borderId = 0, hostId = 0, val = 0, school = 0, sex = 0, fansGbId = 0, fansRoleName = '', fansPhoto = '', fansBorderId = 0, fansVal = 0, fansHostId = 0, fansSchool = 0, fansSex = 0):
        super(MissTianyuPlayoffVal, self).__init__(gbId, roleName, photo, borderId, hostId, val, school, sex)
        self.fansGbId = fansGbId
        self.fansRoleName = fansRoleName
        self.fansPhoto = fansPhoto
        self.fansBorderId = fansBorderId
        self.fansVal = fansVal
        self.fansHostId = fansHostId
        self.fansSchool = fansSchool
        self.fansSex = fansSex

    def copyGroupVal(self, groupVal):
        if type(groupVal) is not MissTianyuGroupVal:
            return
        self.gbId, self.roleName, self.photo, self.borderId, self.hostId, _, self.school, self.sex = groupVal.getDTO()
        return self

    def addVal(self, val):
        self.val += val
        return self.val

    def updateFans(self, fansInfo, totalVal):
        self.fansGbId, self.fansRoleName, self.fansPhoto, self.fansBorderId, self.fansHostId, self.fansSchool, self.fansSex = fansInfo
        self.fansVal = totalVal

    def genTopDataFansExtra(self):
        return (self.fansGbId,
         self.fansRoleName,
         self.fansPhoto,
         self.fansBorderId)

    def getDTO(self):
        return (self.gbId,
         self.roleName,
         self.photo,
         self.borderId,
         self.hostId,
         self.val,
         self.school,
         self.sex,
         self.fansGbId,
         self.fansRoleName,
         self.fansPhoto,
         self.fansBorderId,
         self.fansHostId,
         self.fansVal,
         self.fansSchool,
         self.fansSex)

    def fromDTO(self, dto):
        self.gbId, self.roleName, self.photo, self.borderId, self.hostId, self.val, self.school, self.sex, self.fansGbId, self.fansRoleName, self.fansPhoto, self.fansBorderId, self.fansHostId, self.fansVal, self.fansSchool, self.fansSex = dto

    def _lateReload(self):
        super(MissTianyuPlayoffVal, self)._lateReload()

    def toDict(self):
        dic = super(MissTianyuPlayoffVal, self).toDict()
        dic.update({'fansGbId': self.fansGbId,
         'fansRoleName': self.fansRoleName,
         'fansPhoto': self.fansPhoto,
         'fansBorderId': self.fansBorderId,
         'fansVal': self.fansVal,
         'fansHostId': self.fansHostId,
         'fansSchool': self.fansSchool,
         'fansGender': self.fansSex})
        return dic


class MissTianyuDict(UserDictType):

    def _lateReload(self):
        super(MissTianyuDict, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()
