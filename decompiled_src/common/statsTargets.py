#Embedded file name: I:/bag/tmp/tw2/res/entities\common/statsTargets.o
from userSoleType import UserSoleType
from userDictType import UserDictType

class StatsTarget(UserSoleType):

    def __init__(self, statsTargetId):
        self.statsTargetId = statsTargetId
        self.done = False
        self.rewardApplied = False


class StatsTargets(UserDictType):

    def __init__(self):
        super(StatsTargets, self).__init__()

    def _lateReload(self):
        for v in self.itervalues():
            if hasattr(v, 'reloadScript'):
                v.reloadScript()
