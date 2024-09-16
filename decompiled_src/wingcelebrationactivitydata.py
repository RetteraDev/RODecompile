#Embedded file name: /WORKSPACE/data/entities/common/wingcelebrationactivitydata.o
from userSoleType import UserSoleType
from userDictType import UserDictType

class WingCelebrationActivityData(UserSoleType):

    def __init__(self):
        self.expireTime = 0
        self.totalCnt = 0
        self.rank = 0
        self.cntByGbId = {}

    def resetAll(self):
        self.expireTime = 0
        self.totalCnt = 0
        self.rank = 0
        self.cntByGbId = {}


class WingCelebrationActivityDict(UserDictType):

    def _iter_child_values(self):
        for _, cVal in self.iteritems():
            for _, gVal in cVal.iteritems():
                yield gVal

    def _lateReload(self):
        super(WingCelebrationActivityDict, self)._lateReload()
        for v in self._iter_child_values():
            v.reloadScript()

    def resetAll(self):
        for v in self._iter_child_values():
            v.resetAll()
