#Embedded file name: I:/bag/tmp/tw2/res/entities\common/newbieCharge.o
from userSoleType import UserSoleType
from userDictType import UserDictType
from data import newbie_activity_data as NAD

class newbieCharge(UserDictType):

    def _lateReload(self):
        super(newbieCharge, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()

    def __init__(self, currActivityId = 0, tLastActivityFinish = 0):
        super(newbieCharge, self).__init__()
        self.currActivityId = currActivityId
        self.tLastActivityFinish = tLastActivityFinish

    def resetAll(self):
        self.currActivityId = 0
        self.tLastActivityFinish = 0
        self.clear()

    def getNewbieChargeVal(self, activityId):
        if not NAD.data.has_key(activityId):
            return None
        if not self.has_key(activityId):
            self[activityId] = newbieChargeVal(activityId, 0, 0, 0)
        return self[activityId]

    def getCurrChargeVal(self):
        return self.getNewbieChargeVal(self.currActivityId)


class newbieChargeVal(UserSoleType):

    def __init__(self, aId = 0, tCharge = 0, isReward = 0, remainTime = 0, endTime = 0):
        super(newbieChargeVal, self).__init__()
        self.aId = aId
        self.tCharge = tCharge
        self.isReward = isReward
        self.remainTime = remainTime
        self.endTime = endTime

    def resetAll(self):
        self.tCharge = 0
        self.isReward = 0
        self.remainTime = 0
        self.endTime = 0
