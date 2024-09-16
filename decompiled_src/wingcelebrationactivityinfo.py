#Embedded file name: /WORKSPACE/data/entities/common/wingcelebrationactivityinfo.o
from userInfo import UserInfo
from wingCelebrationActivityData import WingCelebrationActivityData, WingCelebrationActivityDict

class WingCelebrationActivityInfo(UserInfo):

    def createObjFromDict(self, d):
        celebration = WingCelebrationActivityData()
        celebration.expireTime = d['expireTime']
        celebration.totalCnt = d['totalCnt']
        celebration.cntByGbId = d['cntByGbId']
        celebration.rank = d['rank']
        return celebration

    def getDictFromObj(self, obj):
        return {'expireTime': obj.expireTime,
         'totalCnt': obj.totalCnt,
         'cntByGbId': obj.cntByGbId,
         'rank': obj.rank}

    def isSameType(self, obj):
        return type(obj) is WingCelebrationActivityData


instance = WingCelebrationActivityInfo()

class WingCampCelebrationActivityInfo(UserInfo):

    def createObjFromDict(self, d):
        obj = WingCelebrationActivityDict()
        founder = d['founder']
        extra = d['extra']
        minNum = min(len(founder), len(extra))
        for index in xrange(minNum):
            campId = extra[index]['campId']
            guildNUID = extra[index]['guildNUID']
            obj.setdefault(campId, {})[guildNUID] = founder[index]

        return obj

    def getDictFromObj(self, obj):
        founder = []
        extraList = []
        for campId, cVal in obj.iteritems():
            for guildNUID, gVal in cVal.iteritems():
                extraList.append({'campId': campId,
                 'guildNUID': guildNUID})
                founder.append(gVal)

        return {'founder': founder,
         'extra': extraList}

    def isSameType(self, obj):
        return type(obj) is WingCelebrationActivityDict


dictInstance = WingCampCelebrationActivityInfo()
