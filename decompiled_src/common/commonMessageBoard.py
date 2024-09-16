#Embedded file name: I:/bag/tmp/tw2/res/entities\common/commonMessageBoard.o
import copy
from userSoleType import UserSoleType
from userListType import UserListType
from userDictType import UserDictType

def _cmpMessageBoardEvent(e1, e2):
    if e1.priority != e2.priority:
        return cmp(e1.priority, e2.priority)
    else:
        return cmp(e1.tWhen, e2.tWhen)


def _cmpMessageBoardMessage(e1, e2):
    return cmp(e1.tWhen, e2.tWhen)


class EventVal(UserSoleType):

    def __init__(self, msgId = 0, args = (), tWhen = 0, priority = 0):
        self.msgId = msgId
        self.args = args
        self.tWhen = tWhen
        self.priority = priority

    def getDTO(self):
        return {'msgId': self.msgId,
         'args': self.args,
         'tWhen': self.tWhen,
         'priority': self.priority}

    def fromDTO(self, dto):
        self.__init__(msgId=dto['msgId'], args=dto['args'], tWhen=dto['tWhen'], priority=dto['priority'])
        return self


class MessageBoardEvent(UserListType):

    def _lateReload(self):
        super(MessageBoardEvent, self)._lateReload()
        for fVal in self:
            fVal.reloadScript()

    def getDTO(self):
        dto = []
        for val in self:
            dto.append(val.getDTO())

        return dto

    def fromDTO(self, dto):
        for val in dto:
            self.append(EventVal().fromDTO(val))

        return self


class MsgVal(UserSoleType):

    def __init__(self, who = '', msg = '', tWhen = 0):
        self.who = who
        self.msg = msg
        self.tWhen = tWhen

    def _lateReload(self):
        super(MsgVal, self)._lateReload()

    def getDTO(self):
        return {'who': self.who,
         'msg': self.msg,
         'tWhen': self.tWhen}

    def fromDTO(self, dto):
        self.__init__(who=dto['who'], msg=dto['msg'], tWhen=dto['tWhen'])
        return self


class MessageBoardMsg(UserListType):

    def __init__(self, version = 0):
        super(MessageBoardMsg, self).__init__()
        self.version = version

    def _lateReload(self):
        super(MessageBoardMsg, self)._lateReload()
        for fVal in self:
            fVal.reloadScript()

    def getDTO(self):
        info = []
        for mVal in self:
            info.append(mVal.getDTO())

        return info

    def fromDTO(self, dto):
        for val in dto:
            self.append(MsgVal().fromDTO(val))

        return self


class FbMessageBoardBase(UserSoleType):

    def __init__(self, fbNo = 0, hard = 0, hasNum = 0, challengeWeekList = [], challengeTimeStr = '', desc = '', num = 0):
        super(FbMessageBoardBase, self).__init__()
        self.fbNo = fbNo
        self.hard = hard
        self.hasNum = hasNum
        self.challengeWeekList = challengeWeekList
        self.challengeTimeStr = challengeTimeStr
        self.desc = desc
        self.num = num

    def _lateReload(self):
        super(FbMessageBoardBase, self)._lateReload()

    def getDTO(self):
        return {'fbNo': self.fbNo,
         'hard': self.hard,
         'hasNum': self.hasNum,
         'desc': self.desc,
         'num': self.num,
         'challengeWeekList': self.challengeWeekList,
         'challengeTimeStr': self.challengeTimeStr}


class ConnectionInfo(UserDictType):

    def _lateReload(self):
        super(ConnectionInfo, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()

    def transfer(self, owner):
        pass

    def getDTO(self):
        dto = {}
        for key, val in self.iteritems():
            dto[key] = val.getDTO()

        return dto

    def fromDTO(self, dto):
        for key, val in dto.iteritems():
            self[key] = FbMessageBoardItem().fromDTO(val)

        return self


class FbMessageBoardItem(FbMessageBoardBase):

    def __init__(self, roleName = '', fbNo = 0, hard = 0, itemType = 0, hasNum = 0, challengeWeekList = [], challengeTimeStr = '', desc = '', num = 0, tWhen = 0, fbProgressInfo = {}, fbRestEnterTimes = 0, sex = 0, school = 0, lv = 0, combatPower = 0, isOn = False):
        super(FbMessageBoardItem, self).__init__(fbNo, hard, hasNum, challengeWeekList, challengeTimeStr, desc, num)
        self.roleName = roleName
        self.itemType = itemType
        self.tWhen = tWhen
        self.fbProgressInfo = copy.copy(fbProgressInfo)
        self.fbRestEnterTimes = fbRestEnterTimes
        self.sex = sex
        self.school = school
        self.lv = lv
        self.combatPower = combatPower
        self.isOn = isOn

    def _lateReload(self):
        super(FbMessageBoardItem, self)._lateReload()

    def getDTO(self):
        dto = super(FbMessageBoardItem, self).getDTO()
        dto.update({'roleName': self.roleName,
         'itemType': self.itemType,
         'tWhen': self.tWhen,
         'fbProgressInfo': self.fbProgressInfo,
         'fbRestEnterTimes': self.fbRestEnterTimes})
        return dto

    def fromDTO(self, dto):
        self.__init__(roleName=dto.get('roleName', ''), fbNo=dto.get('fbNo', 0), hard=dto.get('hard', 0), itemType=dto.get('itemType', 0), hasNum=dto.get('hasNum', 0), challengeWeekList=dto.get('challengeWeekList', ()), challengeTimeStr=dto.get('challengeTimeStr', ''), desc=dto.get('desc', ''), num=dto.get('num', 0), tWhen=dto.get('tWhen', 0), fbProgressInfo=dto.get('fbProgressInfo', {}), fbRestEnterTimes=dto.get('fbRestEnterTimes', 0), sex=dto.get('sex', 0), lv=dto.get('lv', 0), school=dto.get('school', 0), combatPower=dto.get('combatPower', 0), isOn=dto.get('isOn', False))
        return self
