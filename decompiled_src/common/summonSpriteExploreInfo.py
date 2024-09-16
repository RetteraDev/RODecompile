#Embedded file name: I:/bag/tmp/tw2/res/entities\common/summonSpriteExploreInfo.o
from userInfo import UserInfo
from summonSpriteExplore import SummonSpriteExplore

class SummonSpriteExploreInfo(UserInfo):

    def createObjFromDict(self, d):
        dictInfo = d['dictInfo']
        obj = SummonSpriteExplore()
        obj.carryItem = dictInfo.get('carryItem', {})
        obj.exploringIndexSet = dictInfo.get('exploringIndexSet', set())
        obj.totalExploredCntDay = dictInfo.get('totalExploredCntDay', 0)
        obj.nowExploredCntDay = dictInfo.get('nowExploredCntDay', 0)
        obj.askGuildForHelpTimes = dictInfo.get('askGuildForHelpTimes', 0)
        obj.helpGuildAskerTimes = dictInfo.get('helpGuildAskerTimes', 0)
        obj.exploreLv = dictInfo.get('exploreLv', 0)
        obj.exploreTime = dictInfo.get('exploreTime', 0)
        obj.isCarryItem = dictInfo.get('isCarryItem', 0)
        obj.exploreEndTimeStamp = dictInfo.get('exploreEndTimeStamp', 0)
        obj.bonusRate = dictInfo.get('bonusRate', 0)
        obj.wealthLv = dictInfo.get('wealthLv', 0)
        obj.option = dictInfo.get('option', 0)
        obj.bonusId = dictInfo.get('bonusId', 0)
        obj.refreshTimes = dictInfo.get('refreshTimes', 0)
        obj.isDelayRestCarryItem = dictInfo.get('isDelayRestCarryItem', 0)
        obj.pendingBonusId = dictInfo.get('pendingBonusId', 0)
        return obj

    def getDictFromObj(self, obj):
        return {'dictInfo': {'carryItem': obj.carryItem,
                      'exploringIndexSet': obj.exploringIndexSet,
                      'totalExploredCntDay': obj.totalExploredCntDay,
                      'nowExploredCntDay': obj.nowExploredCntDay,
                      'askGuildForHelpTimes': obj.askGuildForHelpTimes,
                      'helpGuildAskerTimes': obj.helpGuildAskerTimes,
                      'exploreLv': obj.exploreLv,
                      'exploreTime': obj.exploreTime,
                      'isCarryItem': obj.isCarryItem,
                      'exploreEndTimeStamp': obj.exploreEndTimeStamp,
                      'bonusRate': obj.bonusRate,
                      'wealthLv': obj.wealthLv,
                      'option': obj.option,
                      'bonusId': obj.bonusId,
                      'refreshTimes': obj.refreshTimes,
                      'isDelayRestCarryItem': obj.isDelayRestCarryItem,
                      'pendingBonusId': obj.pendingBonusId}}

    def isSameType(self, obj):
        return type(obj) is SummonSpriteExplore


instance = SummonSpriteExploreInfo()
