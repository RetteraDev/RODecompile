#Embedded file name: /WORKSPACE/data/entities/common/summonspriteappearance.o
import utils
from userSoleType import UserSoleType
from userDictType import UserDictType

class SummonSpriteAppearanceVal(UserSoleType):

    def __init__(self, spriteId):
        super(SummonSpriteAppearanceVal, self).__init__()
        self.spriteId = spriteId
        self.curUseDict = {}
        self.hasList = []
        self.tempDict = {}

    @property
    def totalList(self):
        return self.hasList + self.tempDict.keys()


class SummonSpriteAppearanceDict(UserDictType):

    def __init__(self):
        super(SummonSpriteAppearanceDict, self).__init__()

    def _lateReload(self):
        for v in self.itervalues():
            if hasattr(v, 'reloadScript'):
                v.reloadScript()
