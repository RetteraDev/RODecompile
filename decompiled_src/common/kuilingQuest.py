#Embedded file name: I:/bag/tmp/tw2/res/entities\common/kuilingQuest.o
import const
from userDictType import UserDictType
from userSoleType import UserSoleType

class KuilingQuest(UserDictType):

    def __init__(self, refTime = 0):
        self.refreshTime = refTime

    def completeKuilingQuest(self, questId):
        kuilingQuestVal = self[questId]
        kuilingQuestVal.status = const.QUEST_STATUS_SUCC

    def _lateReload(self):
        super(KuilingQuest, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()


class KuilingQuestVal(UserSoleType):

    def __init__(self, status = const.QUEST_STATUS_DEFAULT):
        self.status = status
