#Embedded file name: I:/bag/tmp/tw2/res/entities\common/summonSpriteBiography.o
import utils
from userSoleType import UserSoleType
from userDictType import UserDictType

class SummonSpriteBiographyTarget(UserSoleType):

    def __init__(self, achieveTargetId):
        super(SummonSpriteBiographyTarget, self).__init__()
        self.achieveTargetId = achieveTargetId
        self.done = False
        self.date = 0


class SummonSpriteBiographyTargets(UserDictType):

    def __init__(self):
        super(SummonSpriteBiographyTargets, self).__init__()

    def _lateReload(self):
        for v in self.itervalues():
            if hasattr(v, 'reloadScript'):
                v.reloadScript()


class SummonSpriteBiography(UserSoleType):

    def __init__(self, achieveId):
        super(SummonSpriteBiography, self).__init__()
        self.achieveId = achieveId
        self.isDone = False
        self.doneDate = 0
        self.isUnlock = False
        self.unlockDate = 0


class SummonSpriteBiographies(UserDictType):

    def __init__(self):
        super(SummonSpriteBiographies, self).__init__()

    def _lateReload(self):
        for v in self.itervalues():
            if hasattr(v, 'reloadScript'):
                v.reloadScript()
