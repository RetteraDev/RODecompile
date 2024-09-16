#Embedded file name: I:/bag/tmp/tw2/res/entities\common/flagStateCommon.o
from userDictType import UserDictType
from userSoleType import UserSoleType
import BigWorld
import time
if BigWorld.component == 'client':
    IN_CLIENT = True
else:
    IN_CLIENT = False

class FlagStateVal(UserSoleType):

    def __init__(self, time = 0.0, lastTime = 0, flagCnt = 1):
        self.time = time
        self.lastTime = lastTime
        self.flagCnt = flagCnt


class FlagStateCommon(UserDictType):

    def _getNow(self):
        if IN_CLIENT:
            return BigWorld.player().getServerTime()
        else:
            return time.time()

    def markFlagState(self, owner, flagStateId, lastTime, flagCnt = 1, needTransfer = True):
        now = self._getNow()
        if flagStateId not in self:
            self[flagStateId] = FlagStateVal(time=now, lastTime=lastTime, flagCnt=flagCnt)
        else:
            self[flagStateId].time = now
            self[flagStateId].lastTime = lastTime
            self[flagStateId].flagCnt = flagCnt
        return True

    def checkInFlagState(self, owner, flagStateId):
        if self._checkRemoveFlagState(owner, flagStateId):
            self.removeFlagState(owner, flagStateId)
        if flagStateId not in self:
            return False
        return True

    def removeFlagState(self, owner, flagStateId, needTransfer = True):
        if flagStateId not in self:
            return False
        del self[flagStateId]
        return True

    def _checkRemoveFlagState(self, owner, flagStateId):
        val = self.get(flagStateId)
        if not val or val.lastTime == -1:
            return False
        if IN_CLIENT:
            if val.time + val.lastTime < self._getNow():
                return True
        elif val.time + val.lastTime < self._getNow() - 0.3:
            return True
        return False
