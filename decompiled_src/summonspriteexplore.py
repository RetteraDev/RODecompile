#Embedded file name: /WORKSPACE/data/entities/common/summonspriteexplore.o
import gamelog
import random
import const
import BigWorld
from data import sys_config_data as SCD
from data import summon_sprite_explore_data as SSED
from userSoleType import UserSoleType
BASE_BAG = {1: 'materialBag',
 2: 'hierogramBag'}
MATERIAL_BAG = 1
HIEROGRAM_BAG = 2

def getBaseBag(owner, bagType):
    bagName = BASE_BAG.get(bagType, '')
    bag = getattr(owner, bagName, None)
    return bag


class SummonSpriteExplore(UserSoleType):

    def __init__(self):
        super(SummonSpriteExplore, self).__init__()
        self.carryItem = {}
        self.exploringIndexSet = set()
        self.totalExploredCntDay = 0
        self.nowExploredCntDay = 0
        self.askGuildForHelpTimes = 0
        self.helpGuildAskerTimes = 0
        self.exploreLv = 0
        self.exploreTime = 0
        self.isCarryItem = 0
        self.exploreEndTimeStamp = 0
        self.bonusRate = 0
        self.wealthLv = 0
        self.option = 0
        self.bonusId = 0
        self.refreshTimes = 0
        self.isDelayRestCarryItem = 0
        self.pendingBonusId = 0

    def resetDaily(self, nowLv, totalLimitDay):
        self.option = getSpriteExploreOption(nowLv)
        self.carryItem = getSpriteExploreCarryItem(self.option)
        self.totalExploredCntDay = totalLimitDay
        self.exploreTime = getSpriteExploreTime()
        self.nowExploredCntDay = 0
        self.askGuildForHelpTimes = 0
        self.helpGuildAskerTimes = 0
        if self.isCarryItem == const.EXPLORE_WITH_ITEM:
            self.isDelayRestCarryItem = 1
            if not self.pendingBonusId:
                self.pendingBonusId = self.bonusId
        else:
            self.isCarryItem = 0
            self.isDelayRestCarryItem = 0
            self.pendingBonusId = 0
        self.refreshTimes = 0
        self.bonusId = getExploreSpriteBonus(self.option)


def getSpriteExploreOption(mlv):
    if BigWorld.component == 'client':
        return 0
    import serverProgress
    lvAndServerProgress = SCD.data.get('spriteExploreLvAndServerProgress', 0)
    if not lvAndServerProgress:
        return 0
    for limitLv, limitServerProgressId, index in lvAndServerProgress:
        if mlv >= limitLv:
            if limitServerProgressId is 0 or serverProgress.isMileStoneFinished(limitServerProgressId):
                return index

    return 1


def getSpriteExploreCarryItem(option):
    if BigWorld.component != 'client':
        import gameutils
        gamelog.debug('@hqx_getSpriteExploreCarryItem_option', option)
        sevenGroups = SSED.data.get(option, {}).get('carryGroup', None)
        if not sevenGroups:
            return {}
        groupList = []
        for groups in sevenGroups:
            r = random.randint(*const.RANDOM_RATE_BASE_10K)
            curRate = 0
            for groupId, groupRate in groups:
                curRate += groupRate
                if curRate > r:
                    groupList.append(groupId)
                    break

        itemDict = {}
        index = 0
        isPrepare = False
        askHelpTimeStamp = 0
        for groupId in groupList:
            bonusRate = getExploreSpriteGroupData(groupId).get('bonusRate', 0)
            res = gameutils.genItemsInItemSet(groupId)
            itemDict[index] = {'itemId': res[0][0],
             'itemNum': res[0][1],
             'isPrepare': isPrepare,
             'bonusRate': bonusRate,
             'groupId': groupId,
             'askHelpTimeStamp': askHelpTimeStamp}
            index += 1

        return itemDict


def getSpriteExploreTotalLimit(activation):
    totalLimitRange = SCD.data.get('spriteExploreTotalTimes', 0)
    if not totalLimitRange:
        return 0
    for limitActivePoints, times in totalLimitRange:
        if activation >= limitActivePoints:
            totalLimitPerDay = times
            break

    return totalLimitPerDay


def getSpriteExploreTime():
    exploreTime = SCD.data.get('spriteExploreTime', 5400)
    return exploreTime


def getSpriteExploreBonusNum(rate):
    if rate > 200:
        rate = 200
    r = random.randint(0, 99)
    bonusNum = 0
    if rate % 100 > r:
        bonusNum += 1
    bonusNum += rate / 100
    return bonusNum


def getExploreSpriteGroupData(itemGroupId):
    from data import summon_sprite_explore_group_data as SSEGD
    item = SSEGD.data.get(itemGroupId, None)
    return item


def getExploreSpriteSingleLimit():
    singleLimitPerDay = SCD.data.get('spriteExploreSingleTimes', 0)
    return singleLimitPerDay


def getExploreSpriteReward(mlv, wlv):
    import formula
    args = {'mlv': mlv,
     'wlv': wlv}
    expReward = formula.calcFormulaWithPArg(SCD.data.get('spriteExploreExp', (0, 0)), args, default=0)
    famiReward = formula.calcFormulaWithPArg(SCD.data.get('spriteExploreFami', (0, 0)), args, default=0)
    return (expReward, famiReward)


def getExploreSpriteCost(mlv):
    import formula
    args = {'mlv': mlv}
    moneyCost = formula.calcFormulaWithPArg(SCD.data.get('spriteExploreMoney', (0, 0)), args, default=0)
    return moneyCost


def getExploreSpriteBonus(option):
    gamelog.debug('@hqx_getExploreSpriteBonus_choice', option)
    bonus = SSED.data.get(option, {}).get('bonusId', None)
    if not bonus:
        return 0
    r = random.randint(*const.RANDOM_RATE_BASE_10K)
    curRate = 0
    for bonusId, bonusRate, itemId in bonus:
        curRate += bonusRate
        if curRate > r:
            return bonusId
            break

    return 0


def getExploreSpriteAskForHelpTimes():
    return SCD.data.get('exploreSpriteAskHelpTimes', 0)


def getExploreSpriteAskForHelpLimit():
    return SCD.data.get('exploreSpriteAskHelpLimit', 0)


def getExploreSpriteHelpGuildAkserLimit():
    return SCD.data.get('exploreSpriteHelpAskerLimit', 0)


def getItemIdByBonusId(option, bonusID):
    bonus = SSED.data.get(option, {}).get('bonusId', ())
    for bonusId, bonusRate, itemId in bonus:
        if bonusId == bonusID:
            return itemId

    return 0


def getBonusLevel(option, bonusID):
    bonus = SSED.data.get(option, {}).get('bonusId', None)
    if not bonus:
        return 0
    bonusNum = len(bonus)
    for index, bonus in enumerate(bonus):
        bonusId, bonusRate, itemId = bonus
        if bonusId == bonusID:
            return bonusNum - index

    return 0
