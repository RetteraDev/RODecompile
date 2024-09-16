#Embedded file name: I:/bag/tmp/tw2/res/entities\common/statsTargetsInfo.o
from userInfo import UserInfo
from statsTargets import StatsTarget, StatsTargets

class StatsTargetsInfo(UserInfo):

    def createObjFromDict(self, dict):
        statsTargets = StatsTargets()
        for statsTargetVal in dict['statsTargets']:
            statsTarget = StatsTarget(statsTargetVal['statsTargetId'])
            statsTarget.done = True if statsTargetVal['done'] > 0 else False
            statsTarget.rewardApplied = True if statsTargetVal['rewardApplied'] > 0 else False
            statsTargets[statsTarget.statsTargetId] = statsTarget

        return statsTargets

    def getDictFromObj(self, obj):
        aVals = []
        for statsTarget in obj.itervalues():
            aVals.append({'statsTargetId': statsTarget.statsTargetId,
             'done': 1 if statsTarget.done else 0,
             'rewardApplied': 1 if statsTarget.rewardApplied else 0})

        return {'statsTargets': aVals}

    def isSameType(self, obj):
        return type(obj) is StatsTargets


instance = StatsTargetsInfo()
