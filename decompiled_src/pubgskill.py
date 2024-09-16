#Embedded file name: /WORKSPACE/data/entities/common/pubgskill.o
from userSoleType import UserSoleType
from userDictType import UserDictType

class PubgSkillVal(UserSoleType):

    def __init__(self, skillLv = 1):
        self.skillLv = skillLv


class PubgSkill(UserDictType):

    def __init__(self, spaceNo):
        self.spaceNo = spaceNo

    def _lateReload(self):
        super(PubgSkill, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()

    def reset(self, spaceNo):
        self.clear()
        self.spaceNo = spaceNo
