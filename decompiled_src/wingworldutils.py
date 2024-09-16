#Embedded file name: /WORKSPACE/data/entities/common/wingworldutils.o
import BigWorld
import gamelog
import random
import const
import utils
import gametypes
import formula
import gameconfigCommon
from sMath import distance3D, distance2D
from data import wing_world_city_data as WWCTD
from data import wing_world_config_data as WWCD
from data import wing_city_building_data as WCBD
from data import wing_world_carrier_construct_data as WWCCD
from data import wing_world_carrier_enhance_prop_data as WWCEPD
from data import region_server_config_data as RSCD
from data import wing_world_country_power_level_data as WWCPLD
from data import wing_world_trend_data as WWTD
from data import wing_world_country_title_data as WWCNTD
from data import wing_city_resource_data as WCRD
from data import wing_world_army_data as WWAD
from data import wing_world_camp_army_data as WWCAD
from data import guild_top_reward_data as GTRD
from data import wing_world_resource_speed_data as WWRSD
from cdata import wing_world_schedule_data as WWSHD
from data import map_config_data as MCD
from data import wing_world_country_event_data as WWCSED
from data import wing_world_season_event_data as WWGSED
from data import transport_data as TD
from cdata import teleport_destination_data as TDD
from cdata import transport_ref_data as TREFD
from cdata import top_reward_data as TRD
from cdata import wing_world_schedule_data as WWSD
from data import wing_world_data as WWD
from data import wing_world_army_skill_data as WWASD
from data import wing_world_camp_army_skill_data as WWCASD
from data import sys_config_data as SCD
from data import wing_world_celebration_reward_data as WWCRD
if BigWorld.component == 'client':
    import gameglobal
    from data import wing_city_building_entity_data as WCBED
else:
    import gameutils
    import gameengine
    import Netease
    import serverProgress
    import gameconst
    import gameconfig
    from data import wing_city_building_entity_data as WCBED
    from data import npc_statue_data as NSD
if BigWorld.component in ('base', 'cell'):
    from data import wing_world_region_data as WGWRD
    from data import wing_world_army_privilege_reverse_data as WWAPRD
    from data import wing_world_camp_army_privilege_reverse_data as WWCAPRD

def checkDeclareQualification(ownCityIds, targetCityId, lostCityIdsLastWeek, groupId):
    if targetCityId in ownCityIds:
        return False
    targetLv = WWCTD.data.get(targetCityId, {}).get('level', 0)
    if targetLv == 0:
        gamelog.info('@hxm checkDeclareLevel invalid cityId', targetLv)
        return False
    if targetLv == 1:
        return True
    if gameconfigCommon.enableWingWorldDeclareNewLink():
        if targetLv <= getMaxSwallowCityLevel(groupId) + 1:
            return True
    isHasLowCity = False
    if targetCityId in lostCityIdsLastWeek:
        return True
    for cityId in ownCityIds:
        lv = WWCTD.data.get(cityId, {}).get('level', 0)
        if lv + 1 >= targetLv:
            isHasLowCity = True
            break

    if not isHasLowCity:
        return False
    for cityId in ownCityIds:
        if checkCityLinkable(cityId, targetCityId):
            return True

    return False


def isBuildintEntityOccupyable(entityNo):
    return WCBED.data.get(entityNo, {}).get('canOccupy', False)


def isArmyLeader(postId):
    return postId in wingPostIdData.ARMY_SUPER_MGR_POST_IDS


def isArmyFirstLeader(postId):
    return postId == gametypes.WING_WORLD_CAMP_LEADER_POST_ID


def isCampLeader(postId):
    return postId in wingPostIdData.ARMY_SUPER_MGR_POST_IDS


def checkDeclareCityPermission(canDeclareNum, postId):
    if postId not in wingPostIdData.ARMY_SUPER_MGR_POST_IDS:
        return False
    elif gameconfigCommon.enableWingWorldWarCampMode():
        return True
    else:
        idx = wingPostIdData.ARMY_SUPER_MGR_POST_IDS.index(postId)
        return idx < canDeclareNum


def checkCampDeclareCityPermission(canDeclareNum, postId):
    if postId not in wingPostIdData.ARMY_SUPER_MGR_POST_IDS:
        return False
    return True


def getCityDelareCount(isHasOwner):
    if isHasOwner:
        return WWCD.data.get('maxDeclareCnt', 3) - 1
    else:
        return WWCD.data.get('maxDeclareCnt', 3)


def getCityDelareCountEx(isHasOwner):
    if isHasOwner:
        return WWCD.data.get('maxDeclareCntEx', 2) - 1
    else:
        return WWCD.data.get('maxDeclareCntEx', 2)


def getBuildingName(buildingId, hostId):
    name = WCBD.data.get(buildingId, {}).get('name', '')
    if not hostId:
        return name
    elif hostId in gametypes.WING_WORLD_CAMPS:
        return '%s-%s' % (name, wingWorldCamp2Desc(hostId))
    else:
        return '%s-%s' % (name, utils.getServerName(hostId))


def getBuildingType(buildingId):
    return WCBD.data.get(buildingId, {}).get('buildingType', 0)


def checkCityLinkable(fromCityId, dstCityId, originalHostId = None):
    if gameconfigCommon.enableWingWorldDeclareNewLink():
        return True
    if originalHostId and RSCD.data.get(originalHostId, {}).get('wingWorldNeighborCityId', 0) == dstCityId:
        return True
    return dstCityId in WWCTD.data.get(fromCityId, {}).get('linkCities', ())


def getCityLevel(cityId):
    return WWCTD.data.get(cityId, {}).get('level', 10)


def getCityName(cityId):
    return WWCTD.data.get(cityId, {}).get('name', '')


def isCityInSameSpace(cityId1, cityId2):
    return WWCTD.data.get(cityId1, {}).get('spaceNos', (0, 0))[0] == WWCTD.data.get(cityId2, {}).get('spaceNos', (-1, 0))[0]


def getCountryTitleName(titleLevel):
    return WWCNTD.data.get(titleLevel, {}).get('titleName', '')


def getCityLevelName(cityLevel):
    return WWCD.data.get('cityLevelDesc', {}).get(cityLevel, '')


def getCityScore(groupId, cityId):
    if groupId and isCitySwallow(groupId, cityId):
        return 0
    return WWCTD.data.get(cityId, {}).get('score', 0)


def getBuildingScore(buildingId):
    return WCBD.data.get(buildingId, {}).get('score', 0)


def getPeaceCityReliveHereFrameCost():
    return WWCD.data.get('peaceCityReliveHereFrameCost', 0)


def getAirStoneActiveHpPercent():
    return WWCD.data.get('airStoneActiveHpPercent', 50)


def getAirStoneAciveMinCount(cityId):
    return WWCTD.data.get(cityId, {}).get('airStoneActiveMinCount', 3)


def getAirStoneDormantContinueTime():
    return WWCD.data.get('airStoneDormantContinueTime', 180)


def getAirStoneDormantRecoverEnergyPercent():
    return WWCD.data.get('airStoneDormantRecoverEnergyPercent', 0.1)


def getAirStoneRecoverRate():
    return WWCD.data.get('airStoneRecoverRate', (2, 0.03))


def isInAirDefenseRange(position, cityId):
    noAirRange = WWCTD.data.get(cityId, {}).get('noAirRange')
    if not noAirRange:
        return False
    pos1, pos2, pos3, pos4 = noAirRange
    pos = (position[0], position[2])
    return utils.isInRectangle(pos1, pos2, pos3, pos4, pos)


def getAirDefenseHeight(cityId):
    return WWCTD.data.get(cityId, {}).get('noAirHeight', 300)


def getWingWorldWarCarrierConstructCost(carrierType, enhanceDict):
    totalCoreCost, totalLoaderCost, totalTimeCost = WWCCD.data.get(carrierType, {}).get('initCost', (0, 0, 0))
    enhCostDict = WWCCD.data.get(carrierType, {}).get('enhanceCost', {})
    for enhPropId, cnt in enhanceDict.iteritems():
        coreCost, loaderCost, timeCost = enhCostDict.get(enhPropId, (0, 0, 0))
        totalCoreCost += coreCost * cnt
        totalLoaderCost += loaderCost * cnt
        totalTimeCost += timeCost * cnt

    return (totalCoreCost, totalLoaderCost, totalTimeCost)


def calcCountryPowerLevel(power):
    maxLevel = len(WWCPLD.data)
    for lv in xrange(1, maxLevel + 1):
        if power < WWCPLD.data.get(lv, {}).get('power', 100000):
            return max(1, lv - 1)

    return maxLevel


def getCityOpennessLevel(powerLevel):
    return WWCPLD.data.get(powerLevel, {}).get('opennessCityLevel', 0)


def isCountryHost(hostId = 0):
    if not hostId:
        hostId = utils.getHostId()
    if gameutils.getWingWorldGroupId(hostId):
        return True
    return False


def getAllCountryHostId(centerHostId, groupId):
    if BigWorld.component not in ('base', 'cell'):
        return []
    if not WGWRD.data.has_key(centerHostId):
        return []
    hostIdList = []
    for hostId in WGWRD.data[centerHostId]:
        if RSCD.data.get(hostId, {}).get('wingWorldGroupId') == groupId:
            hostIdList.append(hostId)

    return hostIdList


def isOpennessSeasonStep(step):
    return step >= gametypes.WING_WORLD_SEASON_STEP_COMBAT_LEVEL_1 and step <= gametypes.WING_WORLD_SEASON_STEP_CELEBRATION


def isCombatStep(step):
    return step >= gametypes.WING_WORLD_SEASON_STEP_COMBAT_LEVEL_1 and step <= gametypes.WING_WORLD_SEASON_STEP_COMBAT_LEVEL_4


def getCombatLevel(step):
    if step >= gametypes.WING_WORLD_SEASON_STEP_COMBAT_LEVEL_1 and step < gametypes.WING_WORLD_SEASON_STEP_CELEBRATION:
        return step - gametypes.WING_WORLD_SEASON_STEP_COMBAT_LEVEL_1 + 1
    if step == gametypes.WING_WORLD_SEASON_STEP_CELEBRATION:
        return step - gametypes.WING_WORLD_SEASON_STEP_COMBAT_LEVEL_1
    return 0


def isCelebrationSeasonStep(step):
    return step == gametypes.WING_WORLD_SEASON_STEP_CELEBRATION


def isInWingCelebration(groupId = 0):
    if BigWorld.component == 'client':
        step = BigWorld.player().wingWorld.step
    else:
        if not groupId:
            groupId = gameutils.getWingWorldGroupId()
        step = getCurSeasonStep(groupId)
    return isCelebrationSeasonStep(step)


def getWingWorldCombatLevel(groupId = 0):
    if BigWorld.component == 'client':
        step = BigWorld.player().wingWorld.step
    else:
        if not groupId:
            groupId = gameutils.getWingWorldGroupId()
        step = getCurSeasonStep(groupId)
    if step >= gametypes.WING_WORLD_SEASON_STEP_CELEBRATION:
        step = 0
    return step


def checkWarSpace(f):

    def func(self, *args, **kwargs):
        if not formula.spaceInWingWarCity(self.spaceNo):
            return
        f(self, *args, **kwargs)

    return func


def checkPeaceSpace(f):

    def func(self, *args, **kwargs):
        if not formula.spaceInWingPeaceCity(self.spaceNo):
            return
        f(self, *args, **kwargs)

    return func


def getSeasonOpenedLevel(seasonStep):
    if seasonStep < gametypes.WING_WORLD_SEASON_STEP_COMBAT_LEVEL_1 or seasonStep > gametypes.WING_WORLD_SEASON_STEP_COMBAT_LEVEL_4:
        return 0
    return seasonStep - gametypes.WING_WORLD_SEASON_STEP_COMBAT_LEVEL_1 + 1


def getWingWorldSoulBossOpenLevel(seasonStep):
    if seasonStep == gametypes.WING_WORLD_SEASON_STEP_CLOSE or seasonStep == gametypes.WING_WORLD_SEASON_STEP_ADJOURNING:
        return -1
    if seasonStep >= gametypes.WING_WORLD_SEASON_STEP_COMBAT_LEVEL_1 and seasonStep <= gametypes.WING_WORLD_SEASON_STEP_COMBAT_LEVEL_4:
        return seasonStep - gametypes.WING_WORLD_SEASON_STEP_COMBAT_LEVEL_1 + 1
    if seasonStep == gametypes.WING_WORLD_SEASON_STEP_CELEBRATION:
        return gametypes.WING_WORLD_SEASON_STEP_COMBAE_MAX_LEVEL


def getWorldTrendTarget(trendId):
    return WWTD.data.get(trendId, {}).get('limitTarget', (10, 10))


def getResourcePointCityId(pointId):
    return WCRD.data.get(pointId, {}).get('cityId', 0)


def getResourcePointPosition(pointId):
    return WCRD.data.get(pointId, {}).get('position', (0, 0, 0))


def isBornIslandResourcePoint(pointId):
    return WCRD.data.get(pointId, {}).get('isBornIsland', False)


def getResourcePointCityName(pointId):
    cityId = getResourcePointCityId(pointId)
    if cityId == 0:
        return WWCD.data.get('wingWorldBornIsland', '')
    return WWCTD.data.get(cityId, {}).get('name', '')


def getResourcePointType(pointId):
    return WCRD.data.get(pointId, {}).get('resType', -1)


def getResourcePointsByCityId(cityId):
    resPoints = []
    for pointId, data in WCRD.data.iteritems():
        if data.get('cityId', 0) == cityId:
            resPoints.append(pointId)

    return resPoints


def getResourcePointName(pointId):
    return WCRD.data.get(pointId, {}).get('name', '')


def getResourcePointResName(pointId):
    pointType = getResourcePointType(pointId)
    return WWCD.data.get('restype%d' % (pointType + 1), '')


def getAdminGuildMemberMinNum():
    return WWCD.data.get('adminGuildMemberMinNum', 1)


def getAdminGuildMaxNum():
    return WWCD.data.get('adminGuildMaxNum', 20)


def getPersonalContributeAwardMinScore():
    return WWCD.data.get('personalContributeAwardMinScore', 1000)


def getAdminGuildProfitMinZhanXun():
    return WWCD.data.get('adminGuildProfitMinZhanXun', 3000)


def getEnterWingWorldMapMinLevel():
    return WWCD.data.get('enterWingWorldMapMinLevel', 69)


def isEnterWarCityNoQueue(postId, recentLeaveInfo, gbId):
    if getWingArmyData().get(postId, {}).get('noQueue', 0):
        return True
    if recentLeaveInfo and utils.getNow() - recentLeaveInfo.get(gbId, 0) <= const.WING_WORLD_LEAVE_PROTECT_INTERVAL:
        return True
    return False


def getGuildTopContributeRewardInfo(countryRank, guildRank):
    if gameconfigCommon.enableWingWorldWarCampMode():
        if countryRank == 1:
            isWin = 1
        else:
            isWin = 0
        rewardKey = (135, 0, isWin)
    else:
        rewardKey = (1000, countryRank, 0)
    return _genGuildContributeRewardInfo(rewardKey, guildRank)


def getGuildCityAdminRewardInfo(cityLevel, adminLevel):
    rewardKey = (1001, cityLevel, 0)
    return _genGuildContributeRewardInfo(rewardKey, adminLevel)


def getGuildCityOccupyRewardInfo(cityLevel, guildRank):
    rewardKey = (1005, cityLevel, 0)
    return _genGuildContributeRewardInfo(rewardKey, guildRank)


def getGuildWorldTrendRewardInfo(trendId, adminLevel):
    rewardKey = WWTD.data.get(trendId, {}).get('rewards', ())
    return _genGuildContributeRewardInfo(rewardKey, adminLevel)


def _genGuildContributeRewardInfo(rewardKey, guildRank):
    rData = GTRD.data.get(rewardKey, {})
    if not rData:
        return ([], [0,
          0,
          0,
          0,
          0])
    for td in rData:
        minRank, maxRank = td['rankRange']
        if not minRank <= guildRank <= maxRank:
            continue
        progressBonusIds = td.get('progressBonusIds', ())
        if BigWorld.component == 'client':
            bonusIdList = [ bonusId for bonusId, eventId in progressBonusIds if not eventId or BigWorld.player().isServerProgressFinished(eventId) ]
        else:
            bonusIdList = [ bonusId for bonusId, eventId in progressBonusIds if not eventId or serverProgress.isMileStoneFinished(eventId) ]
        bonusIdList = [] if not bonusIdList else bonusIdList[:1]
        return (bonusIdList, [td.get('guildFame', 0),
          td.get('guildCash', 0),
          td.get('guildWood', 0),
          td.get('guildCrystal', 0),
          td.get('guildIron', 0)])

    return ([], [0,
      0,
      0,
      0,
      0])


def getPersonalWorldTrendRewardInfo(trendId, adminLevel):
    return WWTD.data.get(trendId, {}).get('personalReward', {}).get(adminLevel, 0)


def getWorldTrendCampRewardInfo(trendId, adminLevel):
    return WWTD.data.get(trendId, {}).get('campReward', {}).get(adminLevel, 0)


def getWorldTrendCamp1RewardInfo(trendId, adminLevel):
    return WWTD.data.get(trendId, {}).get('campReward1', {}).get(adminLevel, 0)


def getWorldTrendMailTemplateId(trendId, adminLevel):
    return WWTD.data.get(trendId, {}).get('mailId', {}).get(adminLevel, 0)


def getWorldTrendType(trendId):
    return WWTD.data.get(trendId, {}).get('trendType', 0)


def getMinCampWorldTrendId():
    return min((x for x, v in WWTD.data.iteritems() if v.get('trendType', 0) > 0))


def getWingWorldCampTrends():
    trendList = []
    for trendId, trendVal in WWTD.data.iteritems():
        if trendVal.get('trendType') == gametypes.WING_WORLD_TREND_TYPE_CAMP:
            trendList.append(trendId)

    trendList.sort()
    return trendList


def getWingWorldContriGroupIdByTrend(trendId):
    trendList = getWingWorldCampTrends()
    if trendId not in trendList:
        return 0
    return trendList.index(trendId) + 1


def getGuildResourceWeight(rank):
    guildResourceWeight = WWCD.data.get('guildResourceWeight', {(1, 1): 5,
     (2, 5): 3,
     (6, 10): 2,
     (11, 20): 1})
    for (rank1, rank2), weight in guildResourceWeight.iteritems():
        if rank >= rank1 and rank <= rank2:
            return weight

    return 0


def calcGuildResourceWeightSum(totalRank):
    guildResourceWeight = WWCD.data.get('guildResourceWeight', {(1, 1): 5,
     (2, 5): 3,
     (6, 10): 2,
     (11, 20): 1})
    weightSum = 0
    for (rank1, rank2), weight in guildResourceWeight.iteritems():
        if totalRank >= rank1:
            if totalRank >= rank2:
                weightSum += weight * (rank2 - rank1 + 1)
            else:
                weightSum += weight * (totalRank - rank1 + 1)

    return weightSum


def calcCityAdminLevel(adminRank):
    if adminRank <= 0:
        return 0
    rank2Level = WWCD.data.get('cityGuildRankToAdminLevel', {1: (1, 1),
     2: (2, 10),
     3: (11, 20)})
    for level, (minRank, maxRank) in rank2Level.iteritems():
        if adminRank >= minRank and adminRank <= maxRank:
            return level

    return 0


def getCityAdminGuildLevelCnt(level):
    rank2Level = WWCD.data.get('cityGuildRankToAdminLevel', {1: (1, 1),
     2: (2, 10),
     3: (11, 20)}).get(level, (1, 1))
    return rank2Level[-1] + 1 - rank2Level[0]


def getResCollectRatioGuild(pointNum):
    fId = WWCD.data.get('spriteResSpeedAddRatioGuildFormulaId', 0)
    if fId:
        return formula.calcFormulaById(fId, {'pointNum': pointNum})
    return 1.0


def getResCollectRatioCountry(pointNum):
    fId = WWCD.data.get('spriteResSpeedAddRatioCountryFormulaId', 0)
    if fId:
        return formula.calcFormulaById(fId, {'pointNum': pointNum})
    return 1.0


def getResourceCollectSpeed(resType, propVal, guildPointNum = 0, countryPointNum = 0):
    """
    \xbc\xc6\xcb\xe3\xd3\xa2\xc1\xe9\xb9\xd2\xbb\xfa\xd7\xca\xd4\xb4\xb2\xfa\xb3\xf6\xcb\xd9\xc2\xca
    :param resType: \xd7\xca\xd4\xb4\xb1\xe0\xba\xc5 0/1/2
    :param propVal: \xca\xf4\xd0\xd4\xd6\xb5
    :param ratio: \xbc\xd3\xcb\xd9\xb1\xc8\xa3\xa8>=1\xa3\xa9
    """
    ratio = getResCollectRatioGuild(guildPointNum) * getResCollectRatioCountry(countryPointNum)
    initSpeedFId = WWRSD.data.get(resType, {}).get('speedFormulaId', 0)
    initSpeed = 0
    if initSpeedFId:
        initSpeed = formula.calcFormulaById(initSpeedFId, {'propVal': propVal})
    return initSpeed * ratio


def getFameByResourceCollectVal(val):
    """
    \xbc\xc6\xcb\xe3\xb1\xbe\xb4\xce\xb2\xc9\xbc\xaf\xd7\xca\xd4\xb4\xbf\xc6\xbb\xf1\xb5\xc3\xb5\xc4\xbb\xc3\xbc\xf8\xb2\xd0\xc6\xac\xa3\xa8\xd2\xbb\xd6\xd6\xc9\xf9\xcd\xfb\xa3\xa9
    :param val: \xb1\xbe\xb4\xce\xd2\xd1\xb2\xc9\xbc\xaf\xd7\xca\xd4\xb4\xd7\xdc\xd6\xb5
    """
    f = WWCD.data.get('spriteResCollectFameFamula', None)
    if f:
        return f({'resVal': val})
    return 0


def getCountryRankResAward(rank):
    return WWCD.data.get('countryRankResAward', {}).get(rank, (0, 0, 0))


def getCountrySeasonEventPriority(eventId):
    return WWCSED.data.get(eventId, {}).get('priority', 0)


def getGroupSeasonEventPriority(eventId):
    return WWGSED.data.get(eventId, {}).get('priority', 0)


def getExtraTeleportJunzi():
    return WWCD.data.get('extraTeleportJunzi', 0)


def getBornIslandToNeightCityDistance():
    return WWCD.data.get('bornIslandToNeightCityDistance', 1000)


def getCityToCityDistance(hostId, srcCityId, destCityId):
    if srcCityId == destCityId:
        return 0
    if not srcCityId:
        neighborCityId = getDefaultNeighborCityId(hostId)
        if not neighborCityId:
            return 0
        if neighborCityId == destCityId:
            return 0
        return getBornIslandToNeightCityDistance() + getCityToCityDistance(hostId, neighborCityId, destCityId)
    if not destCityId:
        neighborCityId = getDefaultNeighborCityId(hostId)
        if not neighborCityId:
            return 0
        if srcCityId == neighborCityId:
            return 0
        return getBornIslandToNeightCityDistance() + getCityToCityDistance(hostId, srcCityId, neighborCityId)
    srcPos = WWCTD.data.get(srcCityId, {}).get('transPosition')
    destPos = WWCTD.data.get(destCityId, {}).get('transPosition')
    if not srcPos or not destPos:
        return 0
    return distance2D(srcPos, destPos)


def getWorldTrendCrontabType(groupId):
    types = gametypes.WING_WORLD_TREND_CRONTAB_PRIORITY.get(groupId, ())
    for sType in types:
        for val in WWSHD.data.itervalues():
            if val['stype'] == sType:
                return sType

    return 0


def getEnterBornIslandSkillCD():
    return WWCD.data.get('enterBornIslandSkillCD', 1800)


def getWarCityTeleportCD():
    return WWCD.data.get('warCityTeleportCD', 120)


def getHistoryBookScore():
    return WWCD.data.get('historyBookScore', 12)


def getCityDirectWinRatio():
    return WWCD.data.get('cityDirectWinRatio', 0.6)


def getCityOwnerHostName(hostId):
    if hostId:
        return utils.getCountryName(hostId)
    return WWCD.data.get('emptyCityShowName', '无归属')


def getSpecialContributeTopAwardMailId(topType, rank):
    rewardKey = (gametypes.TOP_TYPE_WING_WAR_PERSONAL_CONTRIBUTE_OTHER, topType, 0)
    rewardData = TRD.data.get(rewardKey)
    if not rewardData:
        return 0
    for td in rewardData:
        minRank, maxRank = td['rankRange']
        if not minRank <= rank <= maxRank:
            continue
        return td.get('mailTemplateId', 0)

    return 0


def getTotalContributeTopAwardMailId(school, rank):
    rewardKey = (gametypes.TOP_TYPE_WING_WAR_PERSONAL_CONTRIBUTE_TOTAL, school, 0)
    rewardData = TRD.data.get(rewardKey)
    if not rewardData:
        return 0
    for td in rewardData:
        minRank, maxRank = td['rankRange']
        if not minRank <= rank <= maxRank:
            continue
        return td.get('mailTemplateId', 0)

    return 0


def getPeaceCityDestId(tId, cityId):
    td = TD.data.get(tId, {})
    for destId in td.get('destination', ()):
        spaceNo = TDD.data.get(destId, {}).get('space')
        if not formula.spaceInWingPeaceCity(spaceNo):
            continue
        destId2 = TREFD.data.get(destId, {}).get('destId', 0)
        if cityId == TD.data.get(destId2, {}).get('cityId', 0):
            return destId

    return 0


def getDefaultNeighborCityId(hostId):
    neighborCityId = RSCD.data.get(hostId, {}).get('wingWorldNeighborCityId', 0)
    if neighborCityId and WWCTD.data.has_key(neighborCityId):
        return neighborCityId
    cityIds = [ cityId for cityId, val in WWCTD.data.iteritems() if val.get('level', 0) == 1 ]
    return cityIds[hostId % len(cityIds)]


def getYabiaoZaijuNo(isBroken = False):
    if isBroken:
        return WWCD.data.get('wingWorldYabiaoBrokenZaijuNo', 9315)
    else:
        return WWCD.data.get('wingWorldYabiaoZaijuNo', 9308)


def getYabiaoZaijuNos():
    return (WWCD.data.get('wingWorldYabiaoBrokenZaijuNo', 9315), WWCD.data.get('wingWorldYabiaoZaijuNo', 9308))


def getResNameByType(resType):
    return WWCD.data.get('restype%s' % (resType + 1), '')


def isResourcePointBossExistPeriod():
    startCronTab = ''
    endCronTab = ''
    for val in WWSHD.data.itervalues():
        if val['stype'] == gametypes.WING_CRONTAB_STYPE_RESOURCE:
            if val['state'] == 1:
                startCronTab = val['crontab']
            else:
                endCronTab = val['crontab']

    if not startCronTab or not endCronTab:
        if BigWorld.component != 'client':
            gameengine.reportCritical('@hxm wing world resource miss crontab')
        return False
    nextOpen = utils.getNextCrontabTime(startCronTab)
    nextEnd = utils.getNextCrontabTime(endCronTab)
    if nextEnd < nextOpen:
        return True
    return False


def wingGroupName(groupId):
    return WWD.data.get(groupId, {}).get('name', '')


def getWingWarAccurateEndTime():
    for sid, data in WWSD.data.iteritems():
        sType = data['stype']
        state = data['state']
        if sType == gametypes.WING_CRONTAB_STYPE_WAR_STATE and state == gametypes.WING_WORLD_STATE_SETTLEMENT:
            endTime = utils.getNextCrontabTime(data['crontab'])
            return endTime

    gameengine.reportCritical('@hxm wing war end time crontab error')
    return 0


def getMaxSwallowCityLevel(groupId):
    if groupId == 1:
        cityStr = gameconfigCommon.enableWingCitySwallowList1()
    elif groupId == 2:
        cityStr = gameconfigCommon.enableWingCitySwallowList2()
    elif groupId == 3:
        cityStr = gameconfigCommon.enableWingCitySwallowList3()
    else:
        if BigWorld.component in ('base', 'cell'):
            gameengine.reportCritical('@xjw error wingworld group', groupId)
        return 0
    cityList = [ int(x) for x in cityStr.split(',') if x != '' ]
    maxLv = 0
    for cityId in cityList:
        maxLv = max(WWCTD.data.get(cityId, {}).get('level', 0), maxLv)

    return maxLv


def getNextSwallowTime(groupId, cityId, startTime = None):
    if BigWorld.component == 'client' and not gameglobal.rds.configData.get('enableWingWorldSwallow', False):
        return -1
    for val in WWSD.data.itervalues():
        if val.get('stype', 0) == gametypes.WING_WORLD_SCHEDULE_STYPE_SWALLOW and val.get('state', 0) == groupId and val.get('city', ''):
            cityList = [ int(x) for x in val['city'].split(',') if x != '' ]
            if cityId in cityList:
                if val.get('crontab', ''):
                    return utils.getDisposableCronTabTimeStamp(val['crontab'], startTime)
                else:
                    return -1

    return -1


def getWingWorldCampStartCrontab():
    index = 80 + gametypes.WW_CAMP_STATE_SIGNUP_START - 1
    data = WWSD.data.get(index)
    if not data or data.get('stype', 0) != gametypes.WING_CRONTAB_STYPE_CAMP_SEASON:
        return ''
    return data.get('crontab', '')


def getWingWorldCampEndCrontab():
    index = 80 + gametypes.WW_CAMP_STATE_RESET - 1
    data = WWSD.data.get(index)
    if not data or data.get('stype', 0) != gametypes.WING_CRONTAB_STYPE_CAMP_SEASON:
        return ''
    return data.get('crontab', '')


def getPreWingWorldCampStartTime():
    startCrontab = getWingWorldCampStartCrontab()
    if not startCrontab:
        return 0
    return utils.getDisposableCronTabTimeStamp(startCrontab)


def getPreWingWorldCampEndTime():
    endContab = getWingWorldCampEndCrontab()
    if not endContab:
        return 0
    return utils.getDisposableCronTabTimeStamp(endContab)


def checkWingWorldCampTime(timeStamp = 0, useCache = True, tz = None):
    if BigWorld.component in ('base', 'cell') and useCache:
        return Netease.wingWorldCampIsOpen
    timeStamp = timeStamp or utils.getNow()
    startContab = getWingWorldCampStartCrontab()
    endContab = getWingWorldCampEndCrontab()
    if not startContab or not endContab:
        return False
    else:
        return utils.inCrontabRangeWithYear(startContab, endContab, timeStamp)


def wingWorldCamp2Desc(camp):
    return WWCD.data.get('wingCampNames', {}).get(camp, '')


def wingWorldCampState2Desc(state):
    if state == gametypes.WW_CAMP_STATE_DEFAULT:
        desc = '未开始'
    elif state == gametypes.WW_CAMP_STATE_SIGNUP_START:
        desc = '报名期'
    elif state == gametypes.WW_CAMP_STATE_SIGNUP_END:
        desc = '报名结束'
    elif state == gametypes.WW_CAMP_STATE_ALLOC:
        desc = '分配期'
    elif state == gametypes.WW_CAMP_STATE_NOTIFICATION:
        desc = '公布期'
    elif state == gametypes.WW_CAMP_STATE_START:
        desc = '城战期'
    elif state == gametypes.WW_CAMP_STATE_END:
        desc = '城战结束'
    elif state == gametypes.WW_CAMP_STATE_RESET:
        desc = '重置'
    else:
        desc = '无'
    return desc + '(' + str(state) + ')'


def getNormalWingArmyData():
    return WWAD.data


def getCampWingArmyData():
    if BigWorld.component == 'client':
        data = WWCAD.data
        p = BigWorld.player()
        if p.wingWorldCamp:
            for postId in data:
                item = data[postId]
                item['name'] = item.get('name1', '') if p.wingWorldCamp == 1 else item.get('name2', '')

            return data
    return WWCAD.data


def getWingArmyData():
    if gameconfigCommon.enableWingWorldCampArmy():
        if BigWorld.component == 'client':
            data = WWCAD.data
            p = BigWorld.player()
            if p.wingWorldCamp:
                for postId in data:
                    item = data[postId]
                    item['name'] = item.get('name1', '') if p.wingWorldCamp == 1 else item.get('name2', '')

                return data
        return WWCAD.data
    else:
        return WWAD.data


def getArmyDataPreciseNameByCamp(name, wingCampId):
    if gameconfig.enableWingWorldCampArmy():
        preciseName = '%s%s' % (name, wingCampId if wingCampId else '')
    else:
        preciseName = name
    return preciseName


def getOtherCamp(campId):
    if campId == gametypes.WING_WORLD_WAR_CAMP_BLACK:
        return gametypes.WING_WORLD_WAR_CAMP_WHITE
    if campId == gametypes.WING_WORLD_WAR_CAMP_WHITE:
        return gametypes.WING_WORLD_WAR_CAMP_BLACK
    return gametypes.WING_WORLD_WAR_CAMP_DEFAULT


class wingPostIdDataCls(object):

    @property
    def ARMY_LEADER_POST_ID(self):
        if gameconfigCommon.enableWingWorldCampArmy():
            return gametypes.WING_WORLD_CAMP_LEADER_POST_ID
        else:
            return gametypes.WING_WORLD_ARMY_LEADER_POST_ID

    @property
    def ARMY_ASSIST1_POST_ID(self):
        if gameconfigCommon.enableWingWorldCampArmy():
            return gametypes.WING_WORLD_CAMP_ARMY_ASSIST1_POST_ID
        else:
            return gametypes.WING_WORLD_ARMY_ASSIST1_POST_ID

    @property
    def ARMY_ASSIST2_POST_ID(self):
        if gameconfigCommon.enableWingWorldCampArmy():
            return gametypes.WING_WORLD_CAMP_ARMY_ASSIST2_POST_ID
        else:
            return gametypes.WING_WORLD_ARMY_ASSIST2_POST_ID

    @property
    def ARMY_ASSIST3_POST_ID(self):
        if gameconfigCommon.enableWingWorldCampArmy():
            return gametypes.WING_WORLD_CAMP_ARMY_ASSIST3_POST_ID
        else:
            return gametypes.WING_WORLD_ARMY_ASSIST3_POST_ID

    @property
    def ARMY_SPECIAL_POST_ID(self):
        if gameconfigCommon.enableWingWorldCampArmy():
            return gametypes.WING_WORLD_CAMP_ARMY_SPECIAL_POST_ID
        else:
            return gametypes.WING_WORLD_ARMY_SPECIAL_POST_ID

    @property
    def ARMY_SUPER_MGR_POST_IDS(self):
        if gameconfigCommon.enableWingWorldCampArmy():
            return gametypes.WING_WORLD_CAMP_SUPER_MGR_POST_IDS
        else:
            return gametypes.WING_WORLD_ARMY_SUPER_MGR_POST_IDS

    @property
    def START_CELEBRATION_POST_IDS(self):
        if gameconfigCommon.enableWingWorldCampArmy():
            return gametypes.WING_WORLD_CAMP_START_CELEBRATION_POST_IDS
        else:
            return gametypes.WING_WORLD_START_CELEBRATION_POST_IDS


wingPostIdData = wingPostIdDataCls()

def getWingArmySkillData():
    if gameconfigCommon.enableWingWorldCampArmy():
        return WWCASD.data
    else:
        return WWASD.data


def getCountryId(campId, hostId = 0):
    if gameconfigCommon.enableWingWorldWarCampMode():
        return campId
    else:
        return hostId or utils.getHostId()


def getShowHostId(hostId):
    if gameconfigCommon.enableWingWorldWarCampMode():
        if hostId in gametypes.WING_WORLD_CAMPS:
            return gametypes.CAMP_TO_HOST_START_INDEX + hostId
        if hostId in gametypes.WING_WORLD_CAMP_SHOW_HOSTIDS:
            return hostId
    return hostId


def getRealCampId(hostId):
    if gameconfigCommon.enableWingWorldWarCampMode():
        if hostId in gametypes.WING_WORLD_CAMPS:
            return hostId
        if hostId in gametypes.WING_WORLD_CAMP_SHOW_HOSTIDS:
            return hostId - gametypes.CAMP_TO_HOST_START_INDEX
    return 0


def getWarQueuePower(power, guildRank, isCaptain, lastContri, tSign):
    fId = WWCD.data.get('warQueuePowerFormula', 90392)
    if fId:
        tToTommorow = utils.getToTomorrowSecond(tSign)
        value = formula.calcFormulaById(fId, {'tSign': tToTommorow,
         'power': power,
         'guildRank': guildRank,
         'isCaptain': isCaptain,
         'lastContri': lastContri})
    else:
        if guildRank == 0:
            guildRank = 99
        value = utils.getToTomorrowSecond(tSign) - WWCD.data.get('wingWorldQueueBaseValue', 12600) - (power - 50000) ** 2 / 100000000 - max(10 - guildRank, 0) - int(isCaptain) * 300 - lastContri / 100
    return value


def calcWingWorldCampPower(recentMaxCombatScore):
    param = {'combatScore': recentMaxCombatScore}
    formulaId = SCD.data.get('wingWorldBattleScoreId', 0)
    power = min(int(formula.calcFormulaById(formulaId, param)), const.MAX_UINT16)
    return power


if BigWorld.component == 'client':

    def isOpenWingWorld():
        msId = WWCD.data.get('openWingWorldServerProgress', 19008)
        if not msId:
            return True
        return BigWorld.player().isServerProgressFinished(msId)


    def getWingCitysName(cityList):
        cityNames = ''
        for cityId in cityList:
            if cityNames:
                cityNames += ','
            cityNames += WWCTD.data.get(int(cityId), {}).get('name', '')

        return cityNames


    def isCityOpen(groupId, cityId):
        if groupId == 1:
            cityList = gameglobal.rds.configData.get('enableWingCityDeclareList1', '')
        elif groupId == 2:
            cityList = gameglobal.rds.configData.get('enableWingCityDeclareList2', '')
        elif groupId == 3:
            cityList = gameglobal.rds.configData.get('enableWingCityDeclareList3', '')
        else:
            return False
        return str(cityId) in cityList.split(',')


    def isCitySwallow(groupId, cityId):
        if not gameglobal.rds.configData.get('enableWingWorldSwallow', False):
            return False
        if groupId == 1:
            cityList = gameglobal.rds.configData.get('enableWingCitySwallowList1', '')
        elif groupId == 2:
            cityList = gameglobal.rds.configData.get('enableWingCitySwallowList2', '')
        elif groupId == 3:
            cityList = gameglobal.rds.configData.get('enableWingCitySwallowList3', '')
        else:
            return False
        return str(cityId) in cityList.split(',')


    def isCitySwallowed(groupId, cityId, time):
        if not gameglobal.rds.configData.get('enableWingWorldSwallow', False):
            return False
        else:
            nextSwallowTime = getNextSwallowTime(groupId, cityId, time)
            if nextSwallowTime < utils.getNow():
                return True
            return False


    def getCityOwnerHostId(cityId):
        p = BigWorld.player()
        wingWorld = p.wingWorld
        isInWarState = wingWorld.state in (gametypes.WING_WORLD_STATE_DECLARE_END, gametypes.WING_WORLD_STATE_OPEN, gametypes.WING_WORLD_STATE_SETTLEMENT)
        if isInWarState:
            return wingWorld.city.getCity(const.WING_CITY_TYPE_WAR, cityId).ownerHostId
        else:
            return wingWorld.city.getCity(const.WING_CITY_TYPE_PEACE, cityId).ownerHostId


    def getCityOwnerHostIdByWeek(cityId, week):
        p = BigWorld.player()
        currentSeasonRecord = getattr(p, 'currentSeasonRecord', [None] * gametypes.WING_WORLD_BATTLE_MAX_CNT)
        if 0 <= week - 1 < gametypes.WING_WORLD_BATTLE_MAX_CNT and currentSeasonRecord[week - 1]:
            time, weekInfo = currentSeasonRecord[week - 1]
            return weekInfo.get(cityId, (0, '', '', ''))
        else:
            return (0, '', '', '')


    def getCurrentSeasonStartTime():
        for info in WWSD.data.values():
            if info.get('stype', 0) == gametypes.WING_CRONTAB_STYPE_SEASON and info.get('state', 0) == 1:
                return utils.getPreCrontabTime(info.get('crontab'))


    def getWingWorldWarCityMaxCount(cityId, cityLevel = 0):
        defaultVal = gameconfigCommon.wingWorldWarCityMaxCount()
        if cityId and not cityLevel:
            cityLevel = getCityLevel(cityId)
        limitStr = gameconfigCommon.wingWorldWarCityMaxCountEx()
        limitList = limitStr.split(',')
        try:
            for strVal in limitList:
                if not strVal:
                    continue
                val = strVal.split(':')
                if not val:
                    continue
                if int(val[0]) == cityLevel:
                    return int(val[1])

        except Exception as e:
            print 'Exception:', e.message
            return defaultVal

        return defaultVal


else:

    def isEnableWingWar(groupId):
        if groupId == 1:
            return gameconfig.enableWingWarGroup1()
        if groupId == 2:
            return gameconfig.enableWingWarGroup2()
        if groupId == 3:
            return gameconfig.enableWingWarGroup3()
        return False


    def getDefaultOpennessLevel():
        return WWCD.data.get('defaultOpennessLevel', 4)


    def randBornIslandRelivePosition():
        posList = MCD.data.get(const.SPACE_NO_WING_WORLD_ISLAND, {}).get('relivePos', (gameconst.WING_BORN_ISLAND_POSITION,))
        return random.choice(posList)


    def getDefaultOwnerReliveBoardEntityNos(cityType, cityId):
        for no, data in WCBED.data.iteritems():
            if data.get('cityType', -1) == cityType and data.get('cityId', 0) == cityId and not data.get('canOccupy', False) and data.get('initCamp', 0) == 1 and getBuildingTypeByEntityNo(no) == gametypes.WING_CITY_BUILDING_TYPE_RELIVE_BOARD:
                return no

        return 0


    def getBuildingTypeByEntityNo(no):
        buildingId = WCBED.data.get(no, {}).get('buildingId', 0)
        return getBuildingType(buildingId)


    def randomDefaultAttackReliveBoardEntityNos(cityType, cityId):
        tempList = []
        for no, data in WCBED.data.iteritems():
            if data.get('cityType', -1) == cityType and data.get('cityId', 0) == cityId and not data.get('canOccupy', False) and data.get('initCamp', 0) == 0:
                tempList.append(no)

        random.shuffle(tempList)
        return tempList


    def getBuildingEntityCityId(entityNo):
        return WCBED.data.get(entityNo, {}).get('cityId')


    def getPeaceBuildingEntNoByWarBuildingEntNo(entoityNo):
        return WCBED.data.get(entoityNo, {}).get('peaceEntNo')


    def randReliveBoardTeleportPos(entityNo):
        positions = WCBED.data.get(entityNo, {}).get('teleportPositions')
        if not positions:
            gameengine.reportCritical('@hxm randReliveBoardTeleportPos relive board miss teleporterPosistions', entityNo)
            return
        return random.choice(positions)


    def getSpaceOnwerHost(spaceNo):
        wingCityHosts = gameutils.getWingCityLocatedHosts()
        cityHostNum = len(wingCityHosts)
        wingGroupNum = gameutils.getWingWorldHostGroupNum(gameutils.getWingWorldGlobalHostId())
        spaceNos = []
        for groupId in range(1, wingGroupNum + 1):
            spaceNos += const.WING_CITY_SPACE_NOS_ALL[groupId]

        spaceNos.sort()
        spaceIdx = spaceNos.index(spaceNo)
        hostIdx = spaceIdx % cityHostNum
        return wingCityHosts[hostIdx]


    def getCurState(groupId = 0):
        if not groupId:
            groupId = gameutils.getWingWorldGroupId()
            if not groupId:
                gameengine.reportCritical('@hxm getCurState error wing world groupId', utils.getHostId())
                return 0
        return Netease.wingWorldCache[groupId].state


    def getCurSeasonStep(groupId = 0):
        if not groupId:
            groupId = gameutils.getWingWorldGroupId()
            if not groupId:
                gamelog.error('@hxm getCurSeasonStep error wing world groupId:', utils.getHostId())
                return 0
        return Netease.wingWorldCache[groupId].step


    def getCurHostResourcePointCount(resType):
        groupId = gameutils.getWingWorldGroupId()
        if not groupId:
            return 0
        return Netease.wingWorldCache[groupId].resourcePointCounts[resType]


    def getServerIsInCelebrationState(hostId = 0):
        if not hostId:
            hostId = utils.getHostId()
        groupId = RSCD.data.get(hostId, {}).get('wingWorldGroupId', 0)
        if not groupId:
            return False
        expireTime = Netease.wingWorldCache[groupId].coutryCelebrationCache.get(hostId)
        if not expireTime:
            return False
        return utils.getNow() <= expireTime


    def getGuildResourcePointCount(guildNUID, resType):
        groupId = gameutils.getWingWorldGroupId()
        if not groupId:
            return 0
        guildData = Netease.wingWorldCache[groupId].guildResPointCountDict.get(guildNUID)
        if not guildData:
            return 0
        return guildData[resType]


    def getGroupCache(groupId):
        return Netease.wingWorldCache.get(groupId)


    def getBuildingIdByEntityNo(entNo):
        return WCBED.data.get(entNo, {}).get('buildingId', 0)


    def getBuildingScoreByEntityNo(entNo):
        buildingId = WCBED.data.get(entNo, {}).get('buildingId', 0)
        return getBuildingScore(buildingId)


    def getBuildingConfigByEntityNo(entNo):
        buildingId = WCBED.data.get(entNo, {}).get('buildingId', 0)
        return WCBD.data.get(buildingId, {})


    def getWingWorldCarrierConfigByNo(carrierNo):
        from data import wing_world_carrier_data as WWCD
        return WWCD.data.get(carrierNo, {})


    def getWarRiliveIntervel():
        return WWCD.data.get('warRiliveIntervel', 5)


    def getCitiesBuildingNum(cityType, cityIds):
        entityNos = [ k for k, v in WCBED.data.iteritems() if v.get('cityType') == cityType and v.get('cityId') in cityIds and getEntityName(getBuildingTypeByEntityNo(k)) ]
        return len(entityNos)


    def getCitiesResourcePointIds(cityIds):
        pointIds = [ k for k, v in WCRD.data.iteritems() if v.get('cityId') in cityIds ]
        return pointIds


    def getBornIslandResourcePointIds():
        pointIds = [ k for k, v in WCRD.data.iteritems() if v.get('isBornIsland') and v.get('cityId', 0) == 0 ]
        return pointIds


    def getEntityName(buildingType):
        if buildingType == gametypes.WING_CITY_BUILDING_TYPE_STONE:
            return 'WingCityStone'
        elif buildingType == gametypes.WING_CITY_BUILDING_TYPE_RELIVE_BOARD:
            return 'WingCityReliveBoard'
        elif buildingType == gametypes.WING_CITY_BUILDING_TYPE_AIR_STONE:
            return 'WingCityAirStone'
        elif buildingType == gametypes.WING_CITY_BUILDING_TYPE_GATE:
            return 'WingCityGate'
        elif buildingType in gametypes.WING_CITY_WAR_BUILDING_NORMAL_TYPES:
            return 'WingCityNormalBuilding'
        elif buildingType == gametypes.WING_CITY_BUILDING_TYPE_ADMIN_GUILD_FLAG:
            return 'ClanWarFlag'
        elif buildingType == gametypes.WING_CITY_BUILDING_TYPE_COUNTRY_FLAG:
            return 'WingCountryFlag'
        elif buildingType == gametypes.WING_CITY_BUILDING_TYPE_TALOU or buildingType == gametypes.WING_CITY_BUILDING_TYPE_GATE_SWITCH:
            return 'Npc'
        elif buildingType == gametypes.WING_CITY_BUILDING_TYPE_TRANSPORT:
            return 'Transport'
        else:
            return None


    def getGlobalCityMgr(spaceNo):
        if not formula.spaceInWingCity(spaceNo):
            return None
        groupId, cityType, cityIds = formula.getWingCityInfo(spaceNo)
        return Netease.wingWorldCache.get(groupId, {}).getCity(cityType, cityIds[0]).globalBox


    def getWarCityCacheBySpaceNo(spaceNo):
        if not formula.spaceInWingWarCity(spaceNo):
            return None
        groupId, cityType, cityIds = formula.getWingCityInfo(spaceNo)
        return Netease.wingWorldCache.get(groupId, {}).getCity(cityType, cityIds[0])


    def getAirStoneEnergyBuffId(cityId, energy):
        if not energy:
            return 0
        airStoneBuff = WWCTD.data.get(cityId, {}).get('airStoneBuff')
        if not airStoneBuff:
            return 0
        for minEnergy, buffId in airStoneBuff:
            if energy >= minEnergy:
                return buffId

        return 0


    def getAirStoneBufferIdList(cityId):
        airStoneBuff = WWCTD.data.get(cityId, {}).get('airStoneBuff')
        if not airStoneBuff:
            return 0
        return [ bufferId for _, bufferId in airStoneBuff ]


    def appendCityWarBuildingEntId(spaceNo, entId):
        Netease.wingWorldWarBuildingEntIdsDict.setdefault(spaceNo, set()).add(entId)


    def getOccupyBuildingStateId():
        return WWCD.data.get('occupyBuildingStateId', 0)


    def isCityMapServer():
        hostId = utils.getHostId()
        wingCityHosts = gameutils.getWingCityLocatedHosts()
        if wingCityHosts and hostId in wingCityHosts:
            return True
        return False


    def isOpenWingWorld(hostId = 0):
        msId = WWCD.data.get('openWingWorldServerProgress', 19008)
        if not msId:
            return True
        elif hostId and hostId != utils.getHostId():
            return gameutils.checkExistServerProgressCross(hostId, [msId])
        else:
            return gameutils.checkExistServerProgress([msId])


    def isCityOpen(groupId, cityId):
        if groupId == 1:
            cityList = gameconfig.enableWingCityDeclareList1()
        elif groupId == 2:
            cityList = gameconfig.enableWingCityDeclareList2()
        elif groupId == 3:
            cityList = gameconfig.enableWingCityDeclareList3()
        else:
            gameengine.reportCritical('@hxm error wingworld group', groupId)
            return False
        return str(cityId) in cityList.split(',')


    def isCitySwallow(groupId, cityId):
        if groupId == 1:
            cityList = gameconfig.enableWingCitySwallowList1()
        elif groupId == 2:
            cityList = gameconfig.enableWingCitySwallowList2()
        elif groupId == 3:
            cityList = gameconfig.enableWingCitySwallowList3()
        else:
            gameengine.reportCritical('@hxm error wingworld group', groupId)
            return False
        return str(cityId) in cityList.split(',')


    def getValidCityList(groupId):
        cityList = []
        for cityId in WWCTD.data.iterkeys():
            if isCityOpen(groupId, cityId) and not isCitySwallow(groupId, cityId):
                cityList.append(cityId)

        return cityList


    def isAllowDrivingCarrier(wingWorldPostId):
        return wingWorldPostId > 0


    def getCityTitles(titleLevel, guildNUID, guildRole, wingCache):
        titleConfig = WWCNTD.data.get(titleLevel)
        if not titleConfig:
            return []
        titles = []
        citites = wingCache.getCities(const.WING_CITY_TYPE_PEACE)
        for cityId, val in citites:
            guildRank = val.guild2AdminRank.get(guildNUID, 0)
            if not guildRank:
                continue
            if guildRank == 1 and guildRole == gametypes.GUILD_ROLE_LEADER:
                titleId = titleConfig.get('cityTitle', {}).get(cityId, (0, 0))[0]
            else:
                titleId = titleConfig.get('cityTitle', {}).get(cityId, (0, 0))[1]
            if titleId:
                titles.append(titleId)

        return titles


    def getCityGuildAdminLevel(groupId, cityId, guildNUID):
        wingCache = getGroupCache(groupId)
        if not wingCache:
            return 0
        cityVal = wingCache.getCity(const.WING_CITY_TYPE_PEACE, cityId)
        if not cityVal:
            return 0
        guildRank = cityVal.guild2AdminRank.get(guildNUID, 0)
        if not guildRank:
            return 0
        return calcCityAdminLevel(guildRank)


    def getArmyTitle(titleLevel, postId):
        titleConfig = WWCNTD.data.get(titleLevel)
        if not titleConfig:
            return 0
        return titleConfig.get('armyTitle', {}).get(postId, (0,))[0]


    def getCityGlobalBoxBySpaceNo(spaceNo):
        if not formula.spaceInWingCity(spaceNo):
            return None
        groupId, cityType, cityIds = formula.getWingCityInfo(spaceNo)
        cityVal = Netease.wingWorldCache[groupId].getCity(cityType, cityIds[0])
        if cityVal:
            return cityVal.globalBox
        else:
            return None


    def getAdminGuildStatueArgSet(groupId, cityIds):
        maxRank = getAdminGuildMaxNum()
        argsSet = set()
        for cityId in cityIds:
            for rank in xrange(1, maxRank + 1):
                statueArgs = (gameconst.NPC_STATUE_TYPE_WING_GUILD,
                 cityId,
                 rank,
                 groupId)
                if NSD.data.has_key(statueArgs):
                    argsSet.add(statueArgs)

        return argsSet


    def getCityOwnerHostId(groupId, cityId, cityType = const.WING_CITY_TYPE_PEACE):
        cityVal = Netease.wingWorldCache[groupId].getCity(cityType, cityId)
        if cityVal:
            return cityVal.ownerHostId
        else:
            return 0


    def getWingWorldSeasonResult(groupId, countryId):
        if not hasattr(Netease, 'seasonResultCache'):
            return False
        return Netease.seasonResultCache.get(groupId, {}).get(countryId, False)


    def getPersonalAttendAwardMailId():
        return WWCD.data.get('personalAttendAwardMailId', 2352)


    def monsterIsResourceBoss(monsterData):
        return 'wingresboss' in monsterData.get('worldTags', ())


    def isCrossSeasonStep(curStep, lastLoginTime):
        if not curStep:
            return False
        if curStep >= gametypes.WING_WORLD_SEASON_STEP_ADJOURNING:
            return False
        curCronTab = ''
        for val in WWSHD.data.itervalues():
            if val['stype'] == gametypes.WING_CRONTAB_STYPE_SEASON:
                if val['state'] == curStep:
                    curCronTab = val['crontab']
                    break

        if not curCronTab:
            return False
        openTime = utils.getPreCrontabTime(curCronTab)
        gamelog.debug('@hxm isCrossSeasonStep', curStep, lastLoginTime, utils.getNow(), openTime, openTime - lastLoginTime, openTime - utils.getNow())
        if utils.getNow() < openTime:
            return False
        return lastLoginTime < openTime


    def getContributeShareRange():
        return WWCD.data.get('contributeShareRange', 0)


    def getContributeShareHeight():
        return WWCD.data.get('contributeShareHeight', 0)


    def getMaxKillAvContributeOnCarrier():
        return WWCD.data.get('maxKillAvContributeOnCarrier', 0)


    def getDestroyBuildingAssistConfig():
        return WWCD.data.get('destroyBuildingAssistConfig', (0, 0))


    def getDestroyCarrierAssistConfig():
        return WWCD.data.get('destroyCarrierAssistConfig', (0, 0))


    def getKillMonsterContributeConfig(charType):
        return WWCD.data.get('killMonsterContribute', {}).get(charType, (0, 0, 0))


    def getKillAvatarContributeConfig():
        return WWCD.data.get('killAvatarContribute', (0, 0, 0))


    def getDestroyCarrierContributeConfig(carrierType):
        return WWCD.data.get('destroyCarrierContribute', {}).get(carrierType, (0, 0, 0, 0))


    def getOccupyBuildingContributeConfig(buildingId):
        return WWCD.data.get('occupyBuildingContribute', {}).get(buildingId, (0, 0, 0))


    def getRecoverBuildingContributeConfig(buildingId):
        return WWCD.data.get('recoverBuildingContribute', {}).get(buildingId, (0, 0, 0))


    def getDestroyBuildingContributeConfig(buildingId):
        return WWCD.data.get('destroyBuildingContribute', {}).get(buildingId, (0, 0, 0, 0))


    def getProtectBuildingContributeConfig(buildingId):
        return WWCD.data.get('protectBuildingContribute', {}).get(buildingId, (0, 0))


    def getMutableBuildingRadius(buildingId, defaultRadius):
        return WCBD.data.get(buildingId, {}).get('radius', defaultRadius)


    def getDestroyAirStoneContributeConfig(step):
        return WWCD.data.get('destroyAirStoneContribute', ((0, 0, 0), (0, 0, 0)))[step]


    def getCityBuffEffectChunkName(cityId, chunkName, adminLevel):
        if not adminLevel:
            return 0
        cityData = WWCTD.data.get(cityId, {})
        if chunkName not in cityData.get('buffChunks', ()):
            return 0
        return cityData.get('leaderGuildStrengthenBuffId', {}).get(adminLevel, 0)


    def getKingStatueKey():
        return WWCD.data.get('kingStatueKey', (9, 26, 1, ''))


    def getCityTotalBuildScore(cityId):
        buildingIds = [ v['buildingId'] for v in WCBED.data.itervalues() if v.get('cityType', -1) == const.WING_CITY_TYPE_WAR and v.get('cityId', 0) == cityId and v.get('canOccupy', 0) ]
        return sum([ getBuildingScore(buildingId) for buildingId in buildingIds ])


    def getTrendStepId(groupId = 0, trendId = None):
        if not gameconfig.enableWingWorldWarCampMode():
            return 0
        groupId = groupId or gameutils.getWingWorldGroupId()
        if not groupId:
            return 0
        if trendId is None:
            trendId = Netease.wingWorldCache[groupId].trendId
        if trendId == 0:
            return 1
        campTrends = getWingWorldCampTrends()
        if trendId not in campTrends:
            return 0
        stepId = campTrends.index(trendId) + 2
        if stepId > const.WING_WORLD_SEASON_CONTRI_TOP_NUM:
            return 0
        return stepId


    def getWarQueueState(groupId = 0):
        groupId = groupId or gameutils.getWingWorldGroupId()
        if not hasattr(Netease, 'wingWorldCache'):
            return 0
        if not Netease.wingWorldCache.get(groupId):
            return 0
        return Netease.wingWorldCach[groupId].warQueueState


    def setXinMoState(groupId, state, stateTime):
        Netease.wingWorldXinMoState[groupId] = state
        Netease.wingWorldXinMoStateTime[groupId] = stateTime


    def getXinMoState(groupId):
        return Netease.wingWorldXinMoState.get(groupId, const.WING_WORLD_XINMO_STATE_CLOSE)


    def getXinMoStateTime(groupId):
        return Netease.wingWorldXinMoStateTime.get(groupId, 0)


    def setXinMoAllowGroupNUIDs(groupId, nuids):
        Netease.wingWorldXinMoAllowGroupNUIDs[groupId] = tuple(nuids)


    def getXinMoAllowGroupNUID(groupId):
        return Netease.wingWorldXinMoAllowGroupNUIDs.get(groupId, ())


    def isXinMoAllowGroupNUID(groupId, nuid):
        return nuid in getXinMoAllowGroupNUID(groupId)


    def isXinMoActState(groupId):
        return getXinMoState(groupId) != const.WING_WORLD_XINMO_STATE_CLOSE


    def isXinMoEnterMLState(groupId):
        return getXinMoState(groupId) == const.WING_WORLD_XINMO_STATE_ENTER_ML


    def isXinMoArenaState(groupId):
        return getXinMoState(groupId) == const.WING_WORLD_XINMO_STATE_ARENA


    def isXinMoUniqueBossState(groupId):
        return getXinMoState(groupId) == const.WING_WORLD_XINMO_STATE_UNIQUE_BOSS


    def isXinMoNormalBossState(groupId):
        return getXinMoState(groupId) == const.WING_WORLD_XINMO_STATE_NORMAL_BOSS


    def isXinMoCanAnnalState(groupId):
        return getXinMoState(groupId) in const.WING_WORLD_XINMO_STATE_CAN_ANNAL_LIST


    def isXinMoCanEnterMLState(groupId):
        return getXinMoState(groupId) in const.WING_WORLD_XINMO_STATE_CAN_ENTER_ML_LIST


    def setXinMoArenaFinalWinner(groupId, winnerRecord):
        Netease.wingWorldXinMoArenaWinnerRecord[groupId] = winnerRecord


    def getXinMoArenaFinalWinner(groupId):
        return Netease.wingWorldXinMoArenaWinnerRecord.get(groupId, None)


    def setXinMoUniqueBossWinner(groupId, winnerRecord):
        Netease.wingWorldXinMoUniqueBossWinnerRecord[groupId] = winnerRecord


    def getXinMoUniqueBossWinner(groupId):
        return Netease.wingWorldXinMoUniqueBossWinnerRecord.get(groupId, None)


    def setXinMoUniqueInfo(groupId, uniqueInfo):
        Netease.wingWorldXinMoUniqueInfo[groupId] = uniqueInfo


    def getXinMoUniqueInfo(groupId):
        return Netease.wingWorldXinMoUniqueInfo.get(groupId, None)


    def getRealUnitViaYabiaoResValue(res):
        scale = WWCD.data.get('forgeResCost', const.WINGWORLD_FORGE_RESOURCE_PER_ITEM)
        realUnit = int(res) / scale
        realUnit = min(realUnit, WWCD.data.get('wingYabiaoMaxResUnit', 10))
        return realUnit


    def getYabiaoResValueViaRealUnit(unit):
        scale = WWCD.data.get('forgeResCost', const.WINGWORLD_FORGE_RESOURCE_PER_ITEM)
        res = int(unit * scale)
        return res


    def updateSoulBossState(cfgId, entityId, state, chunk):
        Netease.wingWorldSoulBossCache[cfgId] = (entityId, state, chunk)


    def getArmyPrivilegeReverseData():
        if gameconfig.enableWingWorldCampArmy():
            return WWCAPRD.data
        else:
            return WWAPRD.data


    def getWingWorldWarCityMaxCount(cityId, cityLevel = 0, useCache = True):
        defaultVal = gameconfigCommon.wingWorldWarCityMaxCount()
        if cityId and not cityLevel:
            cityLevel = getCityLevel(cityId)
        if useCache:
            return Netease.wingWorldWarCityMaxDict.get(cityLevel, defaultVal)
        limitStr = gameconfigCommon.wingWorldWarCityMaxCountEx()
        limitList = limitStr.split(',')
        try:
            for strVal in limitList:
                if not strVal:
                    continue
                val = strVal.split(':')
                if not val:
                    continue
                if int(val[0]) == cityLevel:
                    return int(val[1])

        except Exception as e:
            print 'Exception:', e.message
            return defaultVal

        return defaultVal


    def getWWContriScores(scoreDict):
        addSum = 0
        if isinstance(scoreDict, dict):
            for type, score in scoreDict.iteritems():
                addSum += score

        else:
            for type, score in enumerate(scoreDict):
                if not score:
                    continue
                addSum += score

        return addSum


    def getCityMemberCnt(groupId, cityId, countryId):
        if BigWorld.component != 'cell':
            return 0
        cntDict = Netease.wingCityMemberCnt.get(groupId, {}).get(cityId, {})
        if countryId:
            return cntDict.get(countryId, 0)
        return sum(cntDict.itervalues())
