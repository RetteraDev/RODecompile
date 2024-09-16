#Embedded file name: I:/bag/tmp/tw2/res/entities\common/globalAwardInfo.o
from userInfo import UserInfo
from globalAward import GlobalAward, GlobalAwardGroup, GlobalAwardDict, GlobalAwarCache

class GlobalAwardInfo(UserInfo):

    def createObjFromDict(self, dict):
        globalAwardDict = GlobalAwardDict()
        awards = dict['awards']
        for meta in awards:
            gbId = meta['gbId']
            awardType = meta['awardType']
            awardTime = meta['awardTime']
            expTime = meta['expTime']
            awardVal = meta['awardVal']
            claimed = meta['claimed']
            claimTime = meta['claimTime']
            globalAward = GlobalAward(expTime, awardVal, claimed, claimTime)
            globalAwardDict.setdefault((awardType, awardTime), GlobalAwardGroup())[gbId] = globalAward

        return globalAwardDict

    def getDictFromObj(self, obj):
        awards = []
        for (awardType, awardTime), awardGroup in obj.iteritems():
            for gbId, awardVal in awardGroup.iteritems():
                meta = {'gbId': gbId,
                 'awardType': awardType,
                 'awardTime': awardTime,
                 'expTime': awardVal.expTime,
                 'awardVal': awardVal.awardVal,
                 'claimed': awardVal.claimed,
                 'claimTime': awardVal.claimTime}
                awards.append(meta)

        return {'awards': awards}

    def isSameType(self, obj):
        return type(obj) is GlobalAwardDict


instance = GlobalAwardInfo()

class GlobalAwarCacheInfo(UserInfo):

    def createObjFromDict(self, dict):
        globalAwardCache = GlobalAwarCache()
        awards = dict['awards']
        for awardDict in awards:
            awardType = awardDict['awardType']
            awardTime = awardDict['awardTime']
            expTime = awardDict['expTime']
            awardVal = awardDict['awardVal']
            claimed = awardDict['claimed']
            claimTime = awardDict['claimTime']
            globalAward = GlobalAward(expTime, awardVal, claimed, claimTime)
            globalAwardCache[awardType, awardTime] = globalAward

        return globalAwardCache

    def getDictFromObj(self, obj):
        awards = []
        for (awardType, awardTime), awardVal in obj.iteritems():
            awardDict = {'gbId': 0,
             'awardType': awardType,
             'awardTime': awardTime,
             'expTime': awardVal.expTime,
             'awardVal': awardVal.awardVal,
             'claimed': awardVal.claimed,
             'claimTime': awardVal.claimTime}
            awards.append(awardDict)

        return {'awards': awards}

    def isSameType(self, obj):
        return type(obj) is GlobalAwarCache


awardCacheInstance = GlobalAwarCacheInfo()
