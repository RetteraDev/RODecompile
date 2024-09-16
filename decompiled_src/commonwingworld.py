#Embedded file name: /WORKSPACE/data/entities/common/commonwingworld.o
import const
import formula
import gametypes
import wingWorldUtils
import gameconfigCommon
import copy
from userSoleType import UserSoleType
from userDictType import UserDictType
from checkResult import CheckResult
from data import wing_world_army_data as WWAD
from cdata import game_msg_def_data as GMDD
from data import wing_world_city_data as WWCTD
from data import wing_world_country_title_data as WWTD

class WingWorldCityVal(UserSoleType):

    def __init__(self, cityType = 0, cityId = 0, ownerHostId = 0, ownerCampId = 0):
        self.cityId = cityId
        self.cityType = cityType
        self.ownerHostId = ownerHostId
        self.ownerCampId = ownerCampId

    def onReset(self):
        pass

    def onSeasonReset(self):
        self.ownerHostId = 0
        self.ownerCampId = 0

    def getSpaceNo(self, groupId):
        return formula.getWingCitySpaceNo(groupId, self.cityType, self.cityId)

    def isSameType(self, cityType):
        return self.cityType == cityType

    def isAvailable(self):
        return self.available

    def getLevel(self):
        return WWCTD.data.get(self.cityId, {}).get('level', 0)


class WingWorldCity(UserSoleType):

    def __init__(self):
        self.cityVals = [{}, {}]

    def getCountryOwnCityIds(self, hostId):
        return [ v.cityId for v in self.cityVals[const.WING_CITY_TYPE_PEACE].itervalues() if v.ownerHostId == hostId ]

    def getCampOwnCityIds(self, campId):
        return [ v.cityId for v in self.cityVals[const.WING_CITY_TYPE_PEACE].itervalues() if v.ownerCampId == campId ]


class WingWorldCountryVal(UserSoleType):

    def __init__(self, hostId, power = 0, flagId = 0, postInfo = None, neighborCityId = 0, allowAttackCityIds = None, titleLevel = 0, trendIds = None, eventsBlob = None, resourceRecords = None, buildingScore = 0, robRes = None, campId = 0):
        self.hostId = hostId
        self.neighborCityId = neighborCityId
        self.allowAttackCityIds = allowAttackCityIds if allowAttackCityIds else []
        self.ownedCityIds = []
        self.declaredCityId2PostId = {}
        self.flagId = flagId
        self.postInfo = postInfo if postInfo else {}
        self.power = power
        self.titleLevel = titleLevel
        self.trendIds = trendIds or []
        self.eventsBlob = eventsBlob or ''
        self.resourceRecords = resourceRecords or []
        self.mp = 0
        self.buildingScore = buildingScore
        self.scoreRank = 0
        self.robRes = robRes or {}
        self.destroyScore = sum(self.robRes.itervalues())
        self.campId = campId

    def onReset(self):
        self.allowAttackCityIds = []
        self.declaredCityId2PostId = {}

    def getCanDeclareNum(self, groupId, step = None):
        if step is None:
            step = wingWorldUtils.getWingWorldCombatLevel(groupId)
        for _, v in enumerate(const.WING_HOST_DECARE_NUM_LIMIT):
            cityNum, declareNum, extraNum = v
            if len(self.ownedCityIds) >= cityNum:
                if step >= gametypes.WING_WORLD_SEASON_STEP_COMBAT_LEVEL_2:
                    return declareNum + extraNum
                else:
                    return declareNum

        return 0

    def checkCanDeclareCity(self, cityId, postId, groupId, step = None):
        if cityId in self.ownedCityIds:
            return CheckResult(False, GMDD.data.WING_WORLD_DECLARE_IS_OWNED)
        if self.declaredCityId2PostId.has_key(cityId):
            return CheckResult(False, GMDD.data.WING_WORLD_DECLARE_REPEAT)
        for declaredPostId in self.declaredCityId2PostId.itervalues():
            if declaredPostId == postId:
                return CheckResult(False, GMDD.data.WING_WORLD_DECLARE_POSID_REPEAT)

        canDeclareNum = self.getCanDeclareNum(groupId, step)
        if not wingWorldUtils.checkDeclareCityPermission(canDeclareNum, postId):
            return CheckResult(False, GMDD.data.WING_WORLD_DECLARE_NO_PERMISSION)
        return CheckResult(True, 0)

    def isDeclaredCity(self, cityId):
        return self.declaredCityId2PostId.has_key(cityId)

    def getDeclaredCityPostId(self, cityId):
        return self.declaredCityId2PostId.get(cityId, 0)

    def isOpenAttack(self, cityId):
        return cityId in self.allowAttackCityIds

    def setFlagId(self, flagId):
        self.flagId = flagId

    def getPowerLevel(self):
        return wingWorldUtils.calcCountryPowerLevel(self.power)

    def getCityScore(self, groupId, skipSwallow = False):
        score = 0
        for cityId in self.ownedCityIds:
            if skipSwallow and wingWorldUtils.isCitySwallow(groupId, cityId):
                continue
            score += wingWorldUtils.getCityScore(groupId, cityId)

        return score

    def getMaxOwnerCityLevel(self):
        if not self.ownedCityIds:
            return 0
        return max([ wingWorldUtils.getCityLevel(cityId) for cityId in self.ownedCityIds ])

    def getCityNumByCityLevel(self, cityLevel):
        num = 0
        for cityId in self.ownedCityIds or []:
            if wingWorldUtils.getCityLevel(cityId) == cityLevel:
                num += 1

        return num

    def calcTitleLevel(self, groupId):
        maxLevel = len(WWTD.data)
        for lv in reversed(xrange(1, maxLevel + 1)):
            levelData = WWTD.data.get(lv)
            if not levelData:
                continue
            if self.getCityScore(groupId) < levelData['score']:
                continue
            if self.getMaxOwnerCityLevel() < levelData['cityLevelLimit']:
                continue
            if self.getPowerLevel() < levelData['countryLevelLimit']:
                continue
            return lv

        return 0

    def getTitleLevel(self):
        return self.titleLevel


class WingWorldCountry(UserDictType):

    def getUsedFlags(self):
        return [ c.flagId for c in self.itervalues() if c.flagId ]

    def isUsedFlag(self, flagId):
        for c in self.itervalues():
            if c.flagId and c.flagId == flagId:
                return True

        return False

    def checkCanSetFlag(self, hostId, flagId):
        if not self.has_key(hostId):
            return CheckResult(False, 0)
        country = self.get(hostId)
        if country.flagId:
            return CheckResult(False, GMDD.data.WING_WORLD_SET_COUNTRY_FLAG_REPEAT)
        if self.isUsedFlag(flagId):
            return CheckResult(False, GMDD.data.WING_WORLD_SET_COUNTRY_FLAG_BEUSED)
        return CheckResult(True, 0)


class WingWorldCityHostMinMap(object):

    def __init__(self):
        pass


class WingWorldCampVal(UserSoleType):

    def __init__(self, campId, power = 0, flagId = 0, postInfo = None, neighborCityId = 0, allowAttackCityIds = None, titleLevel = 0, trendIds = None, eventsBlob = None, resourceRecords = None, buildingScore = 0, robRes = None):
        self.campId = campId
        self.neighborCityId = neighborCityId
        self.allowAttackCityIds = allowAttackCityIds if allowAttackCityIds else []
        self.ownedCityIds = []
        self.declaredCityId2PostId = {}
        self.flagId = flagId
        self.postInfo = postInfo if postInfo else {}
        self.power = power
        self.titleLevel = titleLevel
        self.trendIds = trendIds or []
        self.eventsBlob = eventsBlob or ''
        self.resourceRecords = resourceRecords or []
        self.mp = 0
        self.buildingScore = buildingScore
        self.scoreRank = 0
        self.robRes = robRes or {}
        self.destroyScore = sum(self.robRes.itervalues())

    def onReset(self):
        self.allowAttackCityIds = []
        self.declaredCityId2PostId = {}

    def getCanDeclareNum(self, groupId, step = None):
        if step is None:
            step = wingWorldUtils.getWingWorldCombatLevel(groupId)
        for _, v in enumerate(const.WING_HOST_DECARE_NUM_LIMIT):
            cityNum, declareNum, extraNum = v
            if len(self.ownedCityIds) >= cityNum:
                if step >= gametypes.WING_WORLD_SEASON_STEP_COMBAT_LEVEL_2:
                    return declareNum + extraNum
                else:
                    return declareNum

        return 0

    def checkCanDeclareCity(self, cityId, postId, groupId, step = None):
        if cityId in self.ownedCityIds:
            return CheckResult(False, GMDD.data.WING_WORLD_DECLARE_IS_OWNED)
        if self.declaredCityId2PostId.has_key(cityId):
            return CheckResult(False, GMDD.data.WING_WORLD_DECLARE_REPEAT)
        for declaredPostId in self.declaredCityId2PostId.itervalues():
            if declaredPostId == postId:
                return CheckResult(False, GMDD.data.WING_WORLD_DECLARE_POSID_REPEAT)

        canDeclareNum = self.getCanDeclareNum(groupId, step)
        if not wingWorldUtils.checkCampDeclareCityPermission(canDeclareNum, postId):
            return CheckResult(False, GMDD.data.WING_WORLD_DECLARE_NO_PERMISSION)
        return CheckResult(True, 0)

    def isDeclaredCity(self, cityId):
        return self.declaredCityId2PostId.has_key(cityId)

    def getDeclaredCityPostId(self, cityId):
        return self.declaredCityId2PostId.get(cityId, 0)

    def isOpenAttack(self, cityId):
        return cityId in self.allowAttackCityIds

    def setFlagId(self, flagId):
        self.flagId = flagId

    def getPowerLevel(self):
        return wingWorldUtils.calcCountryPowerLevel(self.power)

    def getCityScore(self):
        score = 0
        for cityId in self.ownedCityIds:
            score += wingWorldUtils.getCityScore(cityId)

        return score

    def getMaxOwnerCityLevel(self):
        if not self.ownedCityIds:
            return 0
        return max([ wingWorldUtils.getCityLevel(cityId) for cityId in self.ownedCityIds ])

    def calcTitleLevel(self):
        maxLevel = len(WWTD.data)
        for lv in reversed(xrange(1, maxLevel + 1)):
            levelData = WWTD.data.get(lv)
            if not levelData:
                continue
            if self.getCityScore() < levelData['score']:
                continue
            if self.getMaxOwnerCityLevel() < levelData['cityLevelLimit']:
                continue
            if self.getPowerLevel() < levelData['countryLevelLimit']:
                continue
            return lv

        return 0

    def getTitleLevel(self):
        return self.titleLevel


class WingWorldCamp(UserDictType):

    def getUsedFlags(self):
        return [ c.flagId for c in self.itervalues() if c.flagId ]

    def isUsedFlag(self, flagId):
        for c in self.itervalues():
            if c.flagId and c.flagId == flagId:
                return True

        return False

    def checkCanSetFlag(self, camp, flagId):
        if not self.has_key(camp):
            return CheckResult(False, 0)
        campVal = self.get(camp)
        if campVal.flagId:
            return CheckResult(False, GMDD.data.WING_WORLD_SET_COUNTRY_FLAG_REPEAT)
        if self.isUsedFlag(flagId):
            return CheckResult(False, GMDD.data.WING_WORLD_SET_COUNTRY_FLAG_BEUSED)
        return CheckResult(True, 0)


class WingWorldCampHostMinMap(object):

    def __init__(self):
        pass


class WingWorldCityBuildingMinMap(object):

    def __init__(self, buildingId, pos, ownHostId, entNo, hpPercent = 100):
        self.position = pos
        self.buildingId = buildingId
        self.ownHostId = ownHostId
        self.entNo = entNo
        self.hpPercent = hpPercent


class WingCityAdminGuildVal(object):

    def __init__(self, rank, guildNUID, guildName, guildFlag, memberCount, campId, fromHostId):
        self.rank = rank
        self.guildNUID = guildNUID
        self.guildName = guildName
        self.guildFlag = guildFlag
        self.memberCount = memberCount
        self.campId = campId
        self.fromHostId = fromHostId


class WingCityAdminGuildValMap(UserDictType):

    def __init__(self):
        pass

    def checkAuthority(self, adminids):
        pass

    def getMasterGuildVal(self):
        return self.getGuildValByRank(1)

    def getGuildValByRank(self, rank):
        for guildVal in self.itervalues():
            if guildVal.rank == rank:
                return guildVal

    def getGuildNUIDSByRank(self, minRank, maxRank):
        nuids = []
        for rank in xrange(minRank, maxRank + 1):
            guildVal = self.getGuildValByRank(rank)
            nuids.append(guildVal and guildVal.guildNUID or 0)

        return nuids

    def getRankToGuildValDict(self):
        temp = {}
        for guildVal in self.itervalues():
            if guildVal.rank and guildVal.guildName:
                temp[guildVal.rank] = guildVal

        return temp


class WingCityCampAdminGuildVal(object):

    def __init__(self, hostId, rank, guildNUID, guildName, guildFlag, memberCount):
        self.hostId = hostId
        self.rank = rank
        self.guildNUID = guildNUID
        self.guildName = guildName
        self.guildFlag = guildFlag
        self.memberCount = memberCount


class WingCityCampAdminGuildValMap(UserDictType):

    def __init__(self):
        pass

    def checkAuthority(self, adminids):
        pass

    def getMasterGuildVal(self):
        return self.getGuildValByRank(1)

    def getGuildValByRank(self, rank):
        for guildVal in self.itervalues():
            if guildVal.rank == rank:
                return guildVal

    def getGuildNUIDSByRank(self, minRank, maxRank):
        nuids = []
        for rank in xrange(minRank, maxRank + 1):
            guildVal = self.getGuildValByRank(rank)
            nuids.append(guildVal and guildVal.guildNUID or 0)

        return nuids

    def getRankToGuildValDict(self):
        temp = {}
        for guildVal in self.itervalues():
            if guildVal.rank and guildVal.guildName:
                temp[guildVal.rank] = guildVal

        return temp


class WingCityResourcePointVal(object):

    def __init__(self, pointId = 0, ownerHostId = 0, occupyTime = 0, gbId = 0, roleName = '', guildNUID = 0, guildName = 0):
        self.pointId = pointId
        self.ownerHostId = ownerHostId
        self.occupyTime = 0
        self.gbId = gbId
        self.roleName = roleName
        self.guildNUID = guildNUID
        self.guildName = guildName
        self.state = 0

    def reset(self):
        self.ownerHostId = 0
        self.occupyTime = 0
        self.gbId = 0
        self.roleName = ''
        self.guildNUID = 0
        self.guildName = ''
        self.state = 0

    def getDTO(self):
        return (self.pointId,
         self.ownerHostId,
         self.occupyTime,
         self.gbId,
         self.roleName,
         self.guildNUID,
         self.guildName,
         self.state)

    def fromDTO(self, dto):
        self.pointId, self.ownerHostId, self.occupyTime, self.gbId, self.roleName, self.guildNUID, self.guildName, self.state = dto


class WWArmyPostVal(UserSoleType):

    def __init__(self, postId = 0, gbId = 0, name = '', school = 0, lv = 0, combatScore = 0, tWhen = 0, sex = 0, photo = '', bOnline = False, skills = {}, mpUsed = 0, statueLoaded = False, privileges = [], supportTgt = 0, mgrPostIds = set(), srcRank = (0, 0), guildName = '', weeklyZhanXun = 0, armyCategory = 0, yabiaoRescue = 0, ownerLeaderGbId = 0, guildNUID = 0, guildRoleId = 0, borderId = 0, hostId = 0, wingCampId = 0):
        self.postId = postId
        self.gbId = gbId
        self.name = name
        self.school = school
        self.lv = lv
        self.combatScore = combatScore
        self.tWhen = tWhen
        self.photo = photo
        self.bOnline = bOnline
        self.sex = sex
        self.mpUsed = 0
        self.skills = copy.deepcopy(skills)
        self.statueLoaded = statueLoaded
        self.privileges = copy.deepcopy(privileges)
        self.supportTgt = supportTgt
        self.mgrPostIds = copy.copy(mgrPostIds)
        self.srcRank = copy.copy(srcRank)
        self.guildName = guildName
        self.weeklyZhanXun = weeklyZhanXun
        self.armyCategory = armyCategory
        self.yabiaoRescue = yabiaoRescue
        self.ownerLeaderGbId = ownerLeaderGbId
        self.guildNUID = guildNUID
        self.guildRoleId = guildRoleId
        self.borderId = borderId
        self.hostId = hostId
        self.wingCampId = wingCampId

    def getSkill(self, skillId):
        if skillId not in wingWorldUtils.getWingArmyData().get(self.postId, {}).get('skills', ()):
            return None
        skill = self.skills.get(skillId)
        if not skill:
            skill = WWArmySkillVal(skillId=skillId)
            self.skills[skillId] = skill
        return skill

    def _lateReload(self):
        super(WWArmyPostVal, self)._lateReload()
        for v in self.skills.itervalues():
            v.reloadScript()

    def getDTO(self):
        return (self.postId,
         self.gbId,
         self.name,
         self.sex,
         self.school,
         self.lv,
         self.combatScore,
         self.photo,
         self.bOnline,
         self.mpUsed,
         self.privileges,
         self.supportTgt,
         self.srcRank,
         self.guildName,
         self.weeklyZhanXun,
         self.mgrPostIds,
         self.yabiaoRescue,
         self.ownerLeaderGbId,
         self.borderId,
         self.hostId)

    def fromDTO(self, dto):
        self.postId, self.gbId, self.name, self.sex, self.school, self.lv, self.combatScore, self.photo, self.bOnline, self.mpUsed, self.privileges, self.supportTgt, self.srcRank, self.guildName, self.weeklyZhanXun, self.mgrPostIds, self.yabiaoRescue, self.ownerLeaderGbId, self.borderId, self.hostId = dto
        return self

    def getSkillDTO(self):
        return [ (x.skillId, x.level, x.nextTime) for x in self.skills.itervalues() ]

    def fromSkillDTO(self, dto):
        self.skills.clear()
        for skillId, level, nextTime in dto:
            self.skills[skillId] = WWArmySkillVal(skillId=skillId, level=level, nextTime=nextTime)

    def getArmyData(self, key, default = None):
        return wingWorldUtils.getWingArmyData().get(self.postId, {}).get(key, default)

    def hasPrivilege(self, privilegeId):
        data = wingWorldUtils.getWingArmyData().get(self.postId, {})
        fixedPrivileges = data.get('fixedPrivileges')
        if fixedPrivileges and privilegeId in fixedPrivileges:
            return True
        return privilegeId in self.privileges

    @staticmethod
    def isGeneral(postId):
        return WWArmyPostVal.assignType(postId) == gametypes.WING_WORLD_POST_ASSIGN_TYPE_GEN_FROM_TOP

    @staticmethod
    def isGeneralEx(postId):
        return WWArmyPostVal.assignType(postId) == gametypes.WING_WORLD_POST_ASSIGN_TYPE_GEN_FROM_TOP and not WWArmyPostVal.isLeadersEx(postId)

    @staticmethod
    def isSoldier(postId):
        return WWArmyPostVal.assignType(postId) == gametypes.WING_WORLD_POST_ASSIGN_TYPE_APPOINT

    @staticmethod
    def isLeaders(postId):
        return WWArmyPostVal.assignType(postId) == gametypes.WING_WORLD_POST_ASSIGN_TYPE_VOTE

    @staticmethod
    def isLeadersEx(postId):
        return postId in wingWorldUtils.wingPostIdData.ARMY_SUPER_MGR_POST_IDS

    @staticmethod
    def assignType(postId):
        data = wingWorldUtils.getWingArmyData().get(postId, {})
        return data.get('assignType', 0)

    def getPostName(self):
        nameStr = wingWorldUtils.getArmyDataPreciseNameByCamp('name', self.wingCampId)
        return wingWorldUtils.getWingArmyData().get(self.postId, {}).get(nameStr)

    def updateMgrPostIds(self):
        data = wingWorldUtils.getWingArmyData().get(self.postId, {})
        for mgrPostId in data.get('mgrPostIds', ()):
            self.mgrPostIds.add(mgrPostId)

    def getSupPostId(self):
        data = wingWorldUtils.getWingArmyData().get(self.postId, {})
        if data.get('assignType') != gametypes.WING_WORLD_POST_ASSIGN_TYPE_APPOINT:
            return 0
        return data.get('supPostId')

    def updateCategory(self, category):
        self.armyCategory = category


class WWArmySkillVal(UserSoleType):

    def __init__(self, skillId = 0, level = 1, nextTime = 0):
        self.skillId = skillId
        self.level = level
        self.nextTime = nextTime

    def getDTO(self):
        return (self.skillId, self.level, self.nextTime)

    def fromDTO(self, dto):
        self.skillId, self.level, self.nextTime = dto


class WWArmyGuildVoteVal(UserSoleType):

    def __init__(self, name = '', guildName = '', tgtGbId = 0):
        self.name = name
        self.guildName = guildName
        self.tgtGbId = tgtGbId


def getWingWorldArmySalary(postId, score):
    data = wingWorldUtils.getWingArmyData().get(postId)
    bonusId = 0
    for (start, end), bonusId in data.get('salary', ()):
        if score >= start and score <= end:
            return bonusId

    return bonusId
