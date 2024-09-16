#Embedded file name: I:/bag/tmp/tw2/res/entities\common/globalAward.o
from userDictType import UserDictType
from userSoleType import UserSoleType

class GlobalAward(UserSoleType):

    def __init__(self, expTime, awardVal, claimed = False, claimTime = 0):
        self.expTime = expTime
        self.awardVal = awardVal
        self.claimed = claimed
        self.claimTime = claimTime


class GlobalAwardGroup(UserDictType):

    def _lateReload(self):
        super(GlobalAwardGroup, self)._lateReload()
        for val in self.itervalues():
            val.reloadScript()


class GlobalAwardDict(UserDictType):

    def _lateReload(self):
        super(GlobalAwardDict, self)._lateReload()
        for val in self.itervalues():
            val.reloadScript()


class GlobalAwarCache(UserDictType):

    def _lateReload(self):
        super(GlobalAwarCache, self)._lateReload()
        for val in self.itervalues():
            val.reloadScript()
