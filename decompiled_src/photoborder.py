#Embedded file name: /WORKSPACE/data/entities/common/photoborder.o
import const
import utils
from userSoleType import UserSoleType
from data import sys_config_data as SCD

class PhotoBorder(UserSoleType):

    def __init__(self):
        self.borderId = 0
        self.borderDict = {}

    def push(self, val):
        if type(val) is not PhotoBorderVal:
            return
        self.borderDict[val.bId] = val

    def transBorderVal(self):
        tmp = []
        for val in self.borderDict.itervalues():
            tmp.append(val.__dict__)

        return tmp

    def unlock(self, borderId, borderType, expireTime):
        if borderId not in self.borderDict:
            val = PhotoBorderVal(borderId, borderType)
            val.initTime(expireTime)
            self.push(val)
            return val
        val = self.borderDict[borderId]
        if borderType == const.PHOTO_BORDER_TYPE_FOREVER:
            val.tTime = const.PHOTO_BORDER_FOREVER_EXPIRE_TIME
        elif borderType == const.PHOTO_BORDER_TYPE_DURATION and val.bType == borderType:
            val.tTime = max(val.tTime, utils.getNow())
            val.tTime += expireTime
        elif borderType == const.PHOTO_BORDER_TYPE_TIMESTAMP and val.bType == borderType:
            val.tTime = max(val.tTime, expireTime)
        return val

    def isForever(self, borderId):
        if borderId in self.borderDict and self.borderDict[borderId].bType == const.PHOTO_BORDER_TYPE_FOREVER:
            return True
        return False

    def isExpire(self, borderId = 0):
        borderId = borderId or self.borderId
        if borderId not in self.borderDict:
            return True
        else:
            tTime = self.borderDict[borderId].tTime
            if tTime == const.PHOTO_BORDER_FOREVER_EXPIRE_TIME:
                return False
            return tTime < utils.getNow()

    def switch(self, borderId):
        self.borderId = borderId

    def getDTO(self):
        return {'bId': self.borderId,
         'bData': [ val.getDTO() for val in self.borderDict.itervalues() ]}

    def fromDTO(self, dto):
        if not dto:
            return
        self.borderId = dto.get('bId', 0)
        for bData in dto['bData']:
            val = PhotoBorderVal().fromDTO(bData)
            self.push(val)

        return self


class PhotoBorderVal(UserSoleType):

    def __init__(self, bId = 0, bType = 0, tTime = 0):
        self.bId = bId
        self.bType = bType
        self.tTime = tTime

    def initTime(self, tTime):
        if self.bType == const.PHOTO_BORDER_TYPE_FOREVER:
            self.tTime = const.PHOTO_BORDER_FOREVER_EXPIRE_TIME
        elif self.bType == const.PHOTO_BORDER_TYPE_DURATION:
            self.tTime = utils.getNow() + tTime
        elif self.bType == const.PHOTO_BORDER_TYPE_TIMESTAMP:
            self.tTime = tTime

    def getDTO(self):
        return [self.bId, self.bType, self.tTime]

    def fromDTO(self, dto):
        self.bId, self.bType, self.tTime = dto
        return self
