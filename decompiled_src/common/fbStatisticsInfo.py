#Embedded file name: I:/bag/tmp/tw2/res/entities\common/fbStatisticsInfo.o
import copy
from userInfo import UserInfo
from fbStatistics import FubenStats

class FubenStatsInfo(UserInfo):

    def createObjFromDict(self, dict):
        fbStats = FubenStats()
        if dict['statsDict']:
            fbStats.statsDict.update(dict['statsDict'])
        return fbStats

    def getDictFromObj(self, obj):
        res = {}
        if not obj.statsDict:
            res['statsDict'] = {}
        else:
            res['statsDict'] = copy.deepcopy(obj.statsDict)
        return res

    def isSameType(self, obj):
        return type(obj) is FubenStats


instance = FubenStatsInfo()
