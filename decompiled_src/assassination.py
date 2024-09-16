#Embedded file name: /WORKSPACE/data/entities/common/assassination.o
from userSoleType import UserSoleType
from userDictType import UserDictType
import utils
from cdata import assassination_config_data as ACD

class Assassination(UserSoleType):

    def __init__(self, onBoard = {}, offBoard = {}, extra = {}):
        self.onBoard = onBoard
        self.offBoard = offBoard
        self.extra = extra

    def getDTO(self):
        return (self.onBoard, self.offBoard, self.extra)

    def fromDTO(self, dto):
        self.onBoard, self.offBoard, self.extra = dto
        return self


class AssassinationVal(UserSoleType):

    def __init__(self, aId = 0, gbId = 0, roleName = '', school = 0, sex = 0, lv = 0, score = 0, reward = 0, fromGbId = 0, toGbId = 0, tOn = 0, tOff = 0, tKill = 0, lose = 0, isOn = 0, isShow = True, msg = 0, ownerName = ''):
        self.aId = aId
        self.gbId = gbId
        self.roleName = roleName
        self.school = school
        self.sex = sex
        self.lv = lv
        self.score = score
        self.reward = reward
        self.fromGbId = fromGbId
        self.toGbId = toGbId
        self.tOn = tOn
        self.tOff = tOff
        self.tKill = tKill
        self.lose = lose
        self.isOn = isOn
        self.isShow = isShow
        self.msg = msg
        self.ownerName = ownerName

    def getDTO(self):
        return (self.aId,
         self.gbId,
         self.roleName,
         self.school,
         self.sex,
         self.lv,
         self.score,
         self.reward,
         self.fromGbId,
         self.toGbId,
         self.tOn,
         self.tOff,
         self.tKill,
         self.lose,
         self.isOn,
         self.isShow,
         self.msg,
         self.ownerName)

    def fromDTO(self, dto):
        self.aId, self.gbId, self.roleName, self.school, self.sex, self.lv, self.score, self.reward, self.fromGbId, self.toGbId, self.tOn, self.tOff, self.tKill, self.lose, self.isOn, self.isShow, self.msg, self.ownerName = dto
        return self

    def setKiller(self, stamp, toGbId):
        self.toGbId = toGbId
        self.tOff = stamp

    def killStart(self, now):
        self.tKill = now

    def killFail(self):
        self.tOff = self.toGbId = self.tKill = 0
        self.lose += 1

    def genKillInfo(self):
        return (self.gbId,
         self.fromGbId,
         self.tKill,
         self.toGbId)

    def rewardDesc(self):
        rewardDesc = ACD.data.get('assassinationRewardDesc', {0: 'ÈË¼¶'})
        for k in sorted(rewardDesc.keys(), reverse=True):
            if self.reward >= k:
                return rewardDesc.get(k, '')


class AssassinationDict(UserDictType):

    def _lateReload(self):
        super(AssassinationDict, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()


class AssassinationTombMsg(UserSoleType):

    def __init__(self, gbId = 0, roleName = '', school = 0, sex = 0, photo = '', msg = '', stamp = 0):
        self.gbId = gbId
        self.roleName = roleName
        self.school = school
        self.sex = sex
        self.photo = photo
        self.msg = msg
        self.stamp = stamp

    def getDTO(self):
        return (self.gbId,
         self.roleName,
         self.school,
         self.sex,
         self.photo,
         self.msg,
         self.stamp)

    def fromDTO(self, dto):
        self.gbId, self.roleName, self.school, self.sex, self.photo, self.msg, self.stamp = dto
        return self


class AssassinationTomb(UserSoleType):

    def __init__(self, gbId = 0, roleName = '', school = 0, sex = 0, photo = '', ownerName = '', ownerGbId = 0, msg = 0, lv = 0, box = None):
        self.gbId = gbId
        self.roleName = roleName
        self.school = school
        self.sex = sex
        self.photo = photo
        self.ownerName = ownerName
        self.ownerGbId = ownerGbId
        self.msg = msg
        self.lv = lv
        self.stamp = utils.getNow()
        self.comment = []
        self.box = box

    def commentAssassinationTomb(self, args):
        maxLength = ACD.data.get('assasstionTombMsgMaxLength', 40)
        if len(self.comment) >= maxLength:
            length = ACD.data.get('assasstionTombMsgLength', 30)
            del self.comment[:maxLength - length]
        self.comment.append(AssassinationTombMsg().fromDTO(args))

    def getDTO(self):
        cRes = []
        for cVal in self.comment:
            if type(cVal) is not AssassinationTombMsg:
                return
            cRes.append(cVal.getDTO())

        return (self.gbId,
         self.roleName,
         self.school,
         self.sex,
         self.photo,
         self.ownerName,
         self.ownerGbId,
         self.msg,
         self.lv,
         self.stamp,
         cRes)

    def fromDTO(self, dto):
        self.gbId, self.roleName, self.school, self.sex, self.photo, self.ownerName, self.ownerGbId, self.msg, self.lv, self.stamp, cRes = dto
        for cDto in cRes:
            self.comment.append(AssassinationTombMsg().fromDTO(cDto))

        return self
