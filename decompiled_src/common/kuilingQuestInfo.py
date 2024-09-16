#Embedded file name: I:/bag/tmp/tw2/res/entities\common/kuilingQuestInfo.o
from userDictType import UserDictType
from kuilingQuest import KuilingQuest, KuilingQuestVal

class KuilingQuestInfo(UserDictType):

    def createObjFromDict(self, dict):
        kuilingQuests = KuilingQuest()
        kuilingQuests.refreshTime = dict['refreshTime']
        vals = dict['kuilingQuests']
        for v in vals:
            questId = v['questId']
            status = v['status']
            kuilingQuests[questId] = KuilingQuestVal(status)

        return kuilingQuests

    def getDictFromObj(self, obj):
        kuilingQuests = []
        for questId, kuilingQuestVal in obj.iteritems():
            val = {}
            val['questId'] = questId
            val['status'] = kuilingQuestVal.status
            kuilingQuests.append(val)

        return {'kuilingQuests': kuilingQuests,
         'refreshTime': obj.refreshTime}

    def isSameType(self, obj):
        return type(obj) is KuilingQuest


instance = KuilingQuestInfo()
