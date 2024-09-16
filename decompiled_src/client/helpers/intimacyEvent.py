#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/intimacyEvent.o
import copy
import utils
from userDictType import UserDictType

class EventVal(object):

    def __init__(self, who = '', where = '', msg = '', msgType = 0, when = 0, picList = []):
        self.who = who
        self.where = where
        self.msg = msg
        self.msgType = msgType
        self.when = when
        self.picList = copy.copy(picList)

    def fromDTO(self, dto):
        self.__init__(who=dto.get('who', ''), where=dto['eWhere'], msg=dto['msg'], msgType=dto['msgType'], when=dto['eWhen'], picList=dto['picList'])
        return self


class IntimacyEvent(UserDictType):

    def __init__(self):
        super(IntimacyEvent, self).__init__()

    def addEvent(self, key, eVal):
        if not self.has_key(key):
            self[key] = []
        return self[key].append(eVal)

    def removeEvent(self, key, when):
        if not self.has_key(key):
            return False
        index = -1
        for i, val in enumerate(self[key]):
            if val.when == when:
                index = i
                break

        if i == -1:
            return None
        item = self[key][index]
        del self[key][index]
        if len(self[key]) == 0:
            self.pop(key)
        return item

    def fromDTO(self, dto):
        for item in dto:
            key = utils.genIntimacyEventKey(item['eWhen'])
            if not self.has_key(key):
                self[key] = []
            self[key].append(EventVal().fromDTO(item))

        return self
