#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\common/commGuild.o
from gamestrings import gameStrings
import BigWorld
import formula
import time
import math
import copy
import const
import gametypes
import utils
import gamelog
if BigWorld.component in ('base', 'cell'):
    import gameconfig
else:
    import gameglobal
from userSoleType import UserSoleType
from userDictType import UserDictType
from cdata import pskill_template_data as PSTD
from cdata import game_msg_def_data as GMDD
from data import guild_building_data as GBD
from data import guild_growth_volumn_data as GGVD
from data import guild_pskill_data as GPD
from data import guild_growth_prop_data as GGPD
from data import guild_building_upgrade_data as GBUD
from data import guild_level_data as GLD
from data import guild_config_data as GCD
from data import guild_building_marker_data as GBMD
from data import guild_job_data as GJD
from data import guild_factory_product_data as GFPD
from data import guild_resident_template_data as GRTD
from data import guild_resident_pskill_data as GRPD
from data import guild_status_stype_data as GSSD
from data import guild_technology_data as GTD
from data import guild_func_prop_data as GFNPD
from data import guild_static_entity_data as GSED
from data import guild_activity_data as GATD
from data import guild_growth_data as GGD
from data import guild_shop_data as GSHD
from data import item_data as ID
from data import guild_run_man_route_data as GRMRD
from data import guild_run_man_data as GRMD
from data import achievement_data as AD
from data import sys_config_data as SCD
from cdata import guild_resident_lv_data as GRLD
from cdata import guild_factory_data as GFD
from cdata import guild_func_prop_def_data as GFNPDD
from cdata import guild_job_reverse_data as GJRD
from cdata import guild_storage_data as GSD
ACTIVITY_ATTR_ROUND_NUM = 'roundNum'
ACTIVITY_ATTR_TIMER_ID = 'timerId'
ACTIVITY_ATTR_WIN_GBIDS = 'winGbIds'
ACTIVITY_ATTR_TOP_GBIDS = 'topGbIds'
ACTIVITY_ATTR_JOIN_GBIDS = 'joinGbIds'
ACTIVITY_ATTR_TOP_NAMES = 'topNames'
ACTIVITY_ATTR_NO_REWARD_GBIDS = 'noRewardGbIds'
ACTIVITY_ATTR_PUZZLE_IDS = 'puzzleIds'
ACTIVITY_ATTR_PUZZLE_DESC = 'puzzleDesc'
ACTIVITY_ATTR_PUZZLE_ANSWER = 'puzzleAnswer'
ACTIVITY_ATTR_PUZZLE_STATS = 'puzzleStats'
ACTIVITY_ATTR_PUZZLE_DYNAMIC_ANSWER = 'dynamicAnswer'
ACTIVITY_ATTR_FIRST_ANSWER_NAME = 'firstName'
ACTIVITY_CLIENT_DATA_ATTR = (ACTIVITY_ATTR_ROUND_NUM,
 ACTIVITY_ATTR_PUZZLE_DESC,
 ACTIVITY_ATTR_TOP_NAMES,
 ACTIVITY_ATTR_PUZZLE_ANSWER)

class BaseGuild(object):

    def _getMaxRoleIdCount(self, roleId):
        d = self.getAbility(GFNPDD.data.ROLE_NUM)
        v = 0
        if d:
            v = d.get(roleId, 0)
        return gametypes.GUILD_PRIVILEGES.get(roleId).get('num')[self.level] + v

    def _getMaxConcurrentDevNum(self):
        return GLD.data.get(self.level).get('concurrentDevNum') + self.getAbility(GFNPDD.data.CONCURRENT_DEV_NUM)

    def _getMaxConcurrentBuildingNum(self):
        return GLD.data.get(self.level).get('concurrentBuildingNum', 1) + self.getAbility(GFNPDD.data.CONCURRENT_BUILDING_NUM)

    def _getMaxConcurrentTechResearchNum(self):
        return 3 + self.getAbility(GFNPDD.data.CONCURRENT_TECH_RESEARCH_NUM)

    def _getMaxMojing(self):
        rate = 1 + self.getAbility(GFNPDD.data.MOJING_MAX)
        v = GSD.data.get(self.getBuildingLevelById(gametypes.GUILD_BUILDING_STORAGE_ID), {}).get('mojing', 0)
        return int(v * rate)

    def _getMaxXirang(self):
        rate = 1 + self.getAbility(GFNPDD.data.XIRANG_MAX)
        v = GSD.data.get(self.getBuildingLevelById(gametypes.GUILD_BUILDING_STORAGE_ID), {}).get('xirang', 0)
        return int(v * rate)

    def _getMaxWood(self):
        rate = 1 + self.getAbility(GFNPDD.data.WOOD_MAX)
        v = GSD.data.get(self.getBuildingLevelById(gametypes.GUILD_BUILDING_STORAGE_ID), {}).get('wood', 0)
        return int(v * rate)

    def _getMaxBindCash(self):
        rate = 1 + self.getAbility(GFNPDD.data.BIND_CASH_MAX)
        v = GSD.data.get(self.getBuildingLevelById(gametypes.GUILD_BUILDING_STORAGE_ID), {}).get('bindCash', 0)
        return int(v * rate)

    def _getMaxOtherRes(self):
        rate = 1 + self.getAbility(GFNPDD.data.SPECIAL_RES_MAX)
        v = GSD.data.get(self.getBuildingLevelById(gametypes.GUILD_BUILDING_STORAGE_ID), {}).get('specialRes', 0)
        return int(v * rate)

    def _getMaxStorageSize(self):
        return GSD.data.get(self.getBuildingLevelById(gametypes.GUILD_BUILDING_STORAGE_ID), {}).get('size', 0) + self.getAbility(GFNPDD.data.STORAGE_SIZE)

    def _getMaxStability(self):
        return GCD.data.get('defaultMaxStability', const.GUILD_DEFAULT_MAX_STABILITY) + self.getAbility(GFNPDD.data.STABILITY_MAX)

    def _getMaxAstrologyState(self):
        return 3 + self.getAbility(GFNPDD.data.ASTROLOGY_BUFF_MAX)

    def _getMaxGroupNum(self):
        return const.GUILD_GROUP_NUM_LIMIT + self.getAbility(GFNPDD.data.GUILD_GROUP_NUM) + len(gametypes.GUILD_TOURNAMENT_GUILD_GROUP)

    def _getMaxConcurrentPSkillResearchNum(self):
        return 2 + self.getAbility(GFNPDD.data.CONCURRENT_PSKILL_RESEARCH_NUM)

    def _getMaxBusinessManNum(self):
        return 3 + self.getAbility(GFNPDD.data.BUSINESS_MAN_NUM, 0)

    def _getMaxMember(self, delta = 0):
        num = len(getBuildingsById(self, gametypes.GUILD_BUILDING_HOUSE_ID, True))
        num = max(0, num + delta)
        return 40 + 4 * num + self.getAbility(GFNPDD.data.GUILD_MEMBER_NUM)

    def _getPopulation(self):
        v = 0
        for resident in self.hiredResident.itervalues():
            v += resident.getPopulation()

        return v

    def _getMaxPopulation(self, delta = 0):
        num = len(getBuildingsById(self, gametypes.GUILD_BUILDING_FARMHOUSE_ID, True))
        num = max(0, num + delta)
        return const.GUILD_FARMHOUSE_POPULATION * num + self.getAbility(GFNPDD.data.POPULATION_NUM)

    def _getLearnPskillBindCashRate(self):
        return const.GUILD_LEARN_PSKILL_BIND_CASH_RATE + self.getAbility(GFNPDD.data.LEARN_PSKILL_BIND_CASH)

    def _getLearnGrowthBindCashRate(self, volumnId, propertyId, level):
        growthBindCashRate = GGD.data.get((volumnId, propertyId, level), {}).get('growthBindCashRate', 0)
        GUILD_LEARN_GROWTH_BIND_CASH_RATE_LIMIT = GCD.data.get('GUILD_LEARN_GROWTH_BIND_CASH_RATE_LIMIT', 0)
        return min(growthBindCashRate * (1 + self.getAbility(GFNPDD.data.LEARN_GROWTH_BIND_CASH)), GUILD_LEARN_GROWTH_BIND_CASH_RATE_LIMIT)

    def _getActivity(self, aid):
        if not GATD.data.get(aid):
            return None
        else:
            activity = self.activity.get(aid)
            if not activity:
                activity = GuildActivityVal(aid=aid)
                self.activity[aid] = activity
            return activity

    def _getMaintainFeeRate(self):
        rate = 1
        maintainFeeRateFormula = GCD.data.get('maintainFeeRateFormula')
        if maintainFeeRateFormula:
            rate = maintainFeeRateFormula({'n': self.lastActiveNum})
        return rate

    def _getBaseMaintainFee(self, withRate = True):
        baseMaintainFeeFormula = GCD.data.get('baseMaintainFeeFormula')
        bindCash = baseMaintainFeeFormula({'l': self.level,
         'n': len(self.member)})
        if withRate:
            rate = max(1 - self.getAbility(GFNPDD.data.REDUCE_BASE_MAINTAIN_FEE), const.GUILD_MIN_RATE)
            return (0,
             0,
             0,
             int(math.ceil(bindCash * rate)))
        else:
            return (0,
             0,
             0,
             bindCash)

    def _getGrowthMaintainFee(self, withRate = True):
        growthMojing = 0
        growthXirang = 0
        growthWood = 0
        growthBindCash = 0
        for volumn in self.growth.itervalues():
            for propId, growth in volumn.iteritems():
                if growth.active:
                    data = GGPD.data.get((volumn.volumnId, propId), {})
                    growthMojing += data.get('maintainMojing', 0)
                    growthXirang += data.get('maintainXirang', 0)
                    growthWood += data.get('maintainWood', 0)
                    growthBindCash += data.get('maintainBindCash', 0)

        if withRate:
            rate = max(1 - self.getAbility(GFNPDD.data.REDUCE_GROWTH_MAINTAIN_FEE), const.GUILD_MIN_RATE)
            return (int(math.ceil(growthMojing * rate)),
             int(math.ceil(growthXirang * rate)),
             int(math.ceil(growthWood * rate)),
             int(math.ceil(growthBindCash * rate)))
        else:
            return (growthMojing,
             growthXirang,
             growthWood,
             growthBindCash)

    def _getBuildingMaintainFee(self, withRate = 1):
        buildingMojing = 0
        buildingXirang = 0
        buildingWood = 0
        buildingBindCash = 0
        for building in self.building.itervalues():
            if building.level > 0:
                data = GBUD.data.get((building.buildingId, building.level), {})
                buildingMojing += data.get('maintainMojing', 0)
                buildingXirang += data.get('maintainXirang', 0)
                buildingWood += data.get('maintainWood', 0)
                buildingBindCash += data.get('maintainBindCash', 0)

        if withRate:
            rate = max(1 - self.getAbility(GFNPDD.data.REDUCE_BUILDING_MAINTAIN_FEE), const.GUILD_MIN_RATE)
            return (int(math.ceil(buildingMojing * rate)),
             int(math.ceil(buildingXirang * rate)),
             int(math.ceil(buildingWood * rate)),
             int(math.ceil(buildingBindCash * rate)))
        else:
            return (buildingMojing,
             buildingXirang,
             buildingWood,
             buildingBindCash)

    def _getActivityCost(self, activityId):
        adata = GATD.data.get(activityId)
        return (adata.get('mojing', 0),
         adata.get('xirang', 0),
         adata.get('wood', 0),
         adata.get('bindCash', 0),
         adata.get('stability', 0))

    def isGroupLeader(self, groupId, gbId):
        group = self.group.get(groupId)
        if not group:
            return False
        return group.leaderGbId == gbId

    def getGroupLeaderGbId(self, groupId):
        group = self.group.get(groupId)
        if not group:
            return
        return group.leaderGbId

    def setGroupLeader(self, groupId, gbId):
        group = self.group.get(groupId)
        if group:
            group.leaderGbId = gbId

    def getGroupIdOfLeader(self, gbId):
        if not gbId:
            return 0
        for groupId, gval in self.group.iteritems():
            if gval.leaderGbId == gbId:
                return groupId

        return 0

    def checkGroupLeaderConsistant(self, gbId):
        member = self.member.get(gbId)
        if not member:
            return False
        lid = self.getGroupIdOfLeader(gbId)
        if lid and member.groupId != lid:
            self.setGroupLeader(lid, 0)
            return True
        return False

    def removeGroupLeader(self, groupId):
        group = self.group.get(groupId)
        if group:
            group.leaderGbId = 0

    def getMemberShopRefreshContrib(self, refreshCnt):
        building = self.getBuildingById(gametypes.GUILD_BUILDING_TREASURE_SHOP_ID)
        if not building or building.level < 1:
            return 0
        b = GCD.data.get('treasureRefreshContribParam')[building.level - 1]
        c = GCD.data.get('treasureRefreshContribCntParam')[refreshCnt - 1]
        v = b * c * (1 - self.getAbility(GFNPDD.data.REDUCE_TREASURE_REFRESH_CONTRIB_COST))
        return int(math.ceil(v))

    def getShopItemContrib(self, sid, amount = 1):
        data = GSHD.data.get(sid, {})
        v = GSHD.data.get(sid, {}).get('contrib', 0)
        if data.get('shopType') == gametypes.GUILD_SHOP_TYPE_TREASURE:
            v = v * (1 - self.getAbility(GFNPDD.data.REDUCE_TREASURE_BUY_CONTRIB_COST))
        return int(math.ceil(v * amount))

    def getShopItemCash(self, sid, amount = 1):
        data = GSHD.data.get(sid, {})
        v = GSHD.data.get(sid, {}).get('cash', 0)
        if data.get('shopType') == gametypes.GUILD_SHOP_TYPE_TREASURE:
            v = v * (1 - self.getAbility(GFNPDD.data.REDUCE_TREASURE_BUY_CASH_COST))
        return int(math.ceil(v * amount))

    def getShopItemBindCash(self, sid, amount = 1):
        data = GSHD.data.get(sid, {})
        v = GSHD.data.get(sid, {}).get('bindCash', 0)
        if data.get('shopType') == gametypes.GUILD_SHOP_TYPE_TREASURE:
            v = v * (1 - self.getAbility(GFNPDD.data.REDUCE_TREASURE_BUY_BIND_CASH_COST))
        return int(math.ceil(v * amount))

    def _getTotalSalary(self, withRate = True):
        if not self.hasSpace:
            return 0
        salary = 0
        for resident in self.hiredResident.itervalues():
            if resident.jobId:
                salary += resident.salary

        if withRate:
            rate = max(1 - self.getAbility(GFNPDD.data.REDUCE_RESIDENT_SALARY), const.GUILD_MIN_RATE)
            return int(math.ceil(salary * rate))
        else:
            return salary

    def _getWSPracticeNum(self):
        building = self.getBuildingById(gametypes.GUILD_BUILDING_GROWTH_ID)
        if not building:
            return 0
        num = utils.getListIndex(building.level, GCD.data.get('wsPracticeNum', const.GUILD_WS_PRACTICE_NUM))
        return min(num, GCD.data.get('wsGuildPracticeOpenNum', const.GUILD_WS_PRACTICE_OPEN_NUM))

    def _unpackRes(self, res):
        mojing = res.pop(gametypes.GUILD_RES_MOJING, 0)
        xirang = res.pop(gametypes.GUILD_RES_XIRANG, 0)
        wood = res.pop(gametypes.GUILD_RES_WOOD, 0)
        bindCash = res.pop(gametypes.GUILD_RES_BINDCASH, 0)
        otherRes = res
        return (mojing,
         xirang,
         wood,
         bindCash,
         otherRes)

    def _packRes(self, mojing, xirang, wood, bindCash, otherRes = None):
        r = {}
        if mojing:
            r[gametypes.GUILD_RES_MOJING] = mojing
        if xirang:
            r[gametypes.GUILD_RES_XIRANG] = xirang
        if wood:
            r[gametypes.GUILD_RES_WOOD] = wood
        if bindCash:
            r[gametypes.GUILD_RES_BINDCASH] = bindCash
        if otherRes:
            r.update(otherRes)
        return r

    def _addCancelRes(self, tp, k, v):
        dt = self.cancelRes.get(tp)
        if dt == None:
            dt = {}
            self.cancelRes[tp] = dt
        dt[k] = v

    def _popCancelRes(self, tp, k):
        dt = self.cancelRes.get(tp)
        if not dt:
            return None
        else:
            return dt.pop(k, None)

    def _checkPayMembers(self, owner, guild, salaryTotal, settings, payments, amountTotal, paylimit, groupSettings = None):
        tsum = 0
        tsumrole = {}
        tsumgroup = {}
        now = utils.getNow()
        for gbId, amount in payments:
            member = guild.member.get(gbId)
            if not member:
                owner.showGameMsg(GMDD.data.GUILD_MEMBER_DIRTY, ())
                return
            if now - member.tJoin < const.GUILD_PAY_JOIN_TIME:
                owner.showGameMsg(GMDD.data.GUILD_PAY_JOIN_TIME, (member.role, utils.formatDuration(const.GUILD_PAY_JOIN_TIME)))
                return
            if paylimit and amount > paylimit:
                owner.showGameMsg(GMDD.data.GUILD_PAY_MAX_MEMBER_SALARY, (member.role, paylimit))
                return
            if tsumrole.has_key(member.roleId):
                tsumrole[member.roleId] += amount
            else:
                tsumrole[member.roleId] = amount
            if groupSettings and guild.group.has_key(member.groupId):
                if tsumgroup.has_key(member.groupId):
                    tsumgroup[member.groupId] += amount
                else:
                    tsumgroup[member.groupId] = amount
            tsum += amount

        if tsum > salaryTotal:
            owner.showGameMsg(GMDD.data.GUILD_INVALID_PAYMENT_SUM, ())
            return
        if salaryTotal > amountTotal:
            owner.showGameMsg(GMDD.data.GUILD_SALARY_TOTAL_EXCEED, ())
            return
        sump = 0
        for roleId, percent in settings:
            sump += percent

        if sump > 100:
            owner.showGameMsg(GMDD.data.GUILD_INVALID_PERCENT_SUM, ())
            return
        if groupSettings:
            sump = 0
            for groupId, percent in groupSettings:
                if not guild.group.has_key(groupId):
                    owner.showGameMsg(GMDD.data.GUILD_GROUP_NOT_EXIST, ())
                    return
                sump += percent

            if sump > 100:
                owner.showGameMsg(GMDD.data.GUILD_INVALID_PERCENT_SUM, ())
                return
        return True

    def getBuildingLevelById(self, buildingId, bMaxLevel = False):
        building = self.getBuildingById(buildingId, bMaxLevel)
        return building and building.level or 0

    def getAbility(self, aid, subId = None):
        d = self.ability.get(aid, 0)
        if subId:
            return d and d.get(subId, 0) or 0
        else:
            return d

    def addAbility(self, aid, v):
        doAddAbility(self.ability, aid, v)

    def decAbility(self, aid, v):
        doDecAbility(self.ability, aid, v)

    def addResidentAbility(self, nuid, aid, v):
        ability = self.residentAbility.get(nuid)
        if not ability:
            ability = {}
            self.residentAbility[nuid] = ability
        doAddAbility(ability, aid, v)
        self.addAbility(aid, v)

    def removeResidentAbility(self, nuid):
        ability = self.residentAbility.pop(nuid, None)
        if not ability:
            return
        else:
            for aid, v in ability.iteritems():
                self.decAbility(aid, v)

            return

    def recalcAbility(self, guild):
        self.ability = {}
        for tech in self.technology.itervalues():
            for aid, v in tech.getAbility():
                self.addAbility(aid, v)

    def _addOtherRes(self, otherRes):
        old = {}
        newv = {}
        maxOtherRes = self._getMaxOtherRes()
        for itemId, cnt in otherRes.iteritems():
            v = self.otherRes.get(itemId, 0)
            old[itemId] = v
            if v < maxOtherRes:
                if self.otherRes.has_key(itemId):
                    v += cnt
                else:
                    v = cnt
                if v > maxOtherRes:
                    v = maxOtherRes
                self.otherRes[itemId] = v
            newv[itemId] = v

        return (old, newv)

    def _getFactoryBuildingId(self, ftype):
        if ftype == gametypes.GUILD_FACTORY_PRODUCT_MACHINE:
            return gametypes.GUILD_BUILDING_FACTORY_MACHINE_ID
        if ftype == gametypes.GUILD_FACTORY_PRODUCT_FACILITY:
            return gametypes.GUILD_BUILDING_FACTORY_FACILITY_ID

    def _hasTechnology(self, techId):
        tech = self.technology.get(techId)
        return tech and tech.isAvail()

    def _getAstrologyBuffType(self, stype):
        return (stype - 1) // 4 + 1

    def _getAstrologyBuffTypeLow(self, btype):
        return btype + 3

    def _getAstrologyBuff(self):
        building = self.getBuildingById(gametypes.GUILD_BUILDING_ASTROLOGY_ID)
        if not building:
            return
        r = []
        for stype in range(1, const.GUILD_ASTROLOGY_STYPE_NUM + 1):
            btype = self._getAstrologyBuffType(stype)
            lvAdd = self.getAbility(GFNPDD.data.ASTROLOGY_BUFF_TYPE_LV, btype) + self.getAbility(GFNPDD.data.ASTROLOGY_BUFF_ALL_LV)
            lv = min(const.GUILD_ASTROLOGY_MAX_HIGH_BUFF_LV, building.level + lvAdd)
            locked = stype in const.GUILD_ASTROLOGY_LOCKED_BUFF_TYPE and not self.getAbility(GFNPDD.data.ASTROLOGY_BUFF_UNLOCK, stype)
            r.append((lv, stype, locked))

        for stype in range(1, const.GUILD_ASTROLOGY_STYPE_NUM + 1):
            btype = self._getAstrologyBuffType(stype)
            lvAdd = self.getAbility(GFNPDD.data.ASTROLOGY_BUFF_ALL_LV)
            lv = min(const.GUILD_ASTROLOGY_MAX_LOW_BUFF_LV, building.level + lvAdd)
            locked = stype in const.GUILD_ASTROLOGY_LOCKED_BUFF_TYPE and not self.getAbility(GFNPDD.data.ASTROLOGY_BUFF_UNLOCK, stype)
            r.append((lv, stype, locked))

        return r

    def _getResidentSitPosition(self, chairId, dist = 0):
        eData = GSED.data.get(chairId)
        x, y, z = eData.get('position')
        direction = eData.get('direction')
        yaw = math.radians(direction[2])
        v = formula.pitchYawToVector(0, yaw)
        d = dist or const.GUILD_SIT_DIST
        position = (x + v[0] * d, y + v[1] * d, z + v[2] * d)
        return position

    def _isMemberShop(self, shopType):
        return shopType == gametypes.GUILD_SHOP_TYPE_TREASURE

    def _applyBuildingAbilities(self):
        for building in self.building.itervalues():
            if building.level > 0:
                for lv in range(1, building.level + 1):
                    budata = GBUD.data.get((building.buildingId, lv), {})
                    abilities = budata.get('abilities')
                    if abilities:
                        for aid, v in abilities.iteritems():
                            doAddAbility(self.ability, aid, v)


class BaseGuildBuildingVal(UserSoleType):

    def getName(self):
        return GBD.data.get(self.buildingId).get('name')

    def inUpgrading(self):
        return self.tStart > 0

    def getMarker(self, guild):
        return guild.marker.get(self.markerId)

    def canFinishUpgrading(self):
        if self.tStart:
            data = GBUD.data.get((self.buildingId, self.level + 1))
            return self.progress >= data.get('progress')
        return False

    def addProgress(self, val):
        oldv = self.progress
        data = GBUD.data.get((self.buildingId, self.level + 1))
        if not data:
            return 0
        self.progress = min(self.progress + val, data.get('progress'))
        return self.progress - oldv

    def checkFinishUpgrading(self):
        if self.canFinishUpgrading():
            self.tStart = 0
            self.level += 1
            self.progress = 0
            return True
        return False

    def exist(self):
        return self.level > 0

    def stopUpgrading(self, guild):
        self.tStart = 0
        self.progress = 0
        marker = guild.marker.get(self.markerId)
        if marker:
            marker.stopBuilding(guild)

    def getInResearchingTechnology(self, guild):
        bdata = GBD.data.get(self.buildingId)
        technologies = bdata.get('technologies')
        for i in range(0, guild.scale):
            scale = i + 1
            for techId in technologies.get(scale, ()):
                technology = guild.technology.get(techId)
                if technology.inResearching():
                    return technology

    def getManager(self, guild, type = gametypes.GUILD_JOB_TYPE_FUNC):
        return self.getMarker(guild).getManager(guild, type)


class GuildResidentPSkillVal(UserSoleType):

    def __init__(self, skillId = 0, level = 0):
        self.skillId = skillId
        self.level = level

    def getDTO(self):
        return (self.skillId, self.level)

    def fromDTO(self, dto):
        self.skillId, self.level = dto
        return self


class BaseGuildResidentVal(UserSoleType):

    def getPopulation(self):
        sdata = GSSD.data.get(self.statusStype)
        if sdata:
            return sdata.get('population', 2)
        else:
            return 2

    def getAbility(self, aid, subId = None):
        d = self.ability.get(aid, 0)
        if subId:
            return d and d.get(subId, 0) or 0
        else:
            return d

    def addAbility(self, aid, v):
        doAddAbility(self.ability, aid, v)

    def decAbility(self, aid, v):
        doDecAbility(self.ability, aid, v)

    def addJobAbility(self, aid, v):
        doAddAbility(self.jobAbility, aid, v)
        self.addAbility(aid, v)

    def removeJobAbility(self):
        for aid, v in self.jobAbility.iteritems():
            self.decAbility(aid, v)

        self.jobAbility.clear()

    def refreshAbility(self, guild):
        if not self.jobId:
            return
        marker = whereJob(guild, self.jobId)
        self.removeJobAbility()
        marker.removeResidentAbility(self.nuid)
        guild.removeResidentAbility(self.nuid)
        marker._applyResidentAbility(guild, self.jobId, self)

    def stopWork(self, guild, newJobId = 0):
        if self.jobId:
            marker = whereJob(guild, self.jobId)
            if marker:
                if self.subJobId:
                    building = marker.getBuilding(guild)
                    if building and building.buildingId in (gametypes.GUILD_BUILDING_FACTORY_MACHINE_ID, gametypes.GUILD_BUILDING_FACTORY_FACILITY_ID):
                        for factory in guild.factory.itervalues():
                            for i in range(len(factory.queue) - 1, -1, -1):
                                task = factory.queue[i]
                                if task.residentNUID == self.nuid:
                                    factory.queue.remove(task)
                                    task.onCancel(guild, factory)
                                    if BigWorld.component == 'base':
                                        guild._sendMailOnCancelTask(factory, task, bSchedule=True, bNotifyRes=True)

                            for task in factory.task.values():
                                if task.residentNUID == self.nuid:
                                    factory.task.pop(task.nuid)
                                    task.onCancel(guild, factory)
                                    if BigWorld.component == 'base':
                                        guild._sendMailOnCancelTask(factory, task, bSchedule=True, bNotifyRes=True)

                self.removeJobAbility()
                marker.removeWorker(self.nuid)
            self.jobId = 0
            self.subJobId = 0
            self.tJob = utils.getNow()
            self.wayNo = 0
            if BigWorld.component == 'base':
                guild._destroyWorkingResidentEntity(self)
                if newJobId:
                    self.jobId = newJobId
                guild._createWorkingResidentEntity(self)
            guild.removeResidentAbility(self.nuid)

    def checkFactoryWork(self, guild):
        if not self.jobId or not self.subJobId:
            return False
        marker = whereJob(self.jobId, guild)
        building = marker.getBuilding(guild)
        if building and building.buildingId in (gametypes.GUILD_BUILDING_FACTORY_MACHINE_ID, gametypes.GUILD_BUILDING_FACTORY_FACILITY_ID):
            return False
        return True

    def getPropType(self):
        return GRTD.data.get(self.templateId, {}).get('propType', 0)

    def getProp(self, propType):
        if propType == gametypes.GUILD_RESIDENT_PROP_POW:
            return self.cpow
        if propType == gametypes.GUILD_RESIDENT_PROP_AGI:
            return self.cagi
        if propType == gametypes.GUILD_RESIDENT_PROP_INT:
            return self.cint
        if propType == gametypes.GUILD_RESIDENT_PROP_SPR:
            return self.cspr

    def getQprop(self, propType):
        if propType == gametypes.GUILD_RESIDENT_PROP_POW:
            return self.qpow
        if propType == gametypes.GUILD_RESIDENT_PROP_AGI:
            return self.qagi
        if propType == gametypes.GUILD_RESIDENT_PROP_INT:
            return self.qint
        if propType == gametypes.GUILD_RESIDENT_PROP_SPR:
            return self.qspr

    def getTechWorkEffect(self, guild, techId):
        marker = whereJob(guild, self.jobId)
        tdata = GTD.data.get(techId)
        v = self.getWorkEffect(tdata.get('propType')) + self.getAbility(GFNPDD.data.RESEARCH_EFFICIENCY, techId) + self.getAbility(GFNPDD.data.RESEARCH_COMMON_EFFICIENCY) + guild.getAbility(GFNPDD.data.RESEARCH_EFFICIENCY, techId) + guild.getAbility(GFNPDD.data.RESEARCH_COMMON_EFFICIENCY)
        if marker:
            v += marker.getAbility(GFNPDD.data.RESEARCH_EFFICIENCY, techId) + marker.getAbility(GFNPDD.data.RESEARCH_COMMON_EFFICIENCY)
        return v

    def getTechWorkload(self, guild, techId, bTired = False, ignoreTime = False):
        tdata = GTD.data.get(techId)
        if ignoreTime:
            tparam = 1
        else:
            tparam = min(utils.getNow() - self.tJob, const.GUILD_MAINTAIN_INTERVAL) * 1.0 / const.GUILD_MAINTAIN_INTERVAL
            tparam = max(0, tparam)
        v = tdata.get('speed', 0) * self.getTechWorkEffect(guild, techId) * tparam
        return int(v)

    def getMgrEffect(self, funcType, targetType = gametypes.GUILD_FUNC_TARGET_ALL):
        return self.getAbility(funcType)

    def getBaseWorkEffect(self, propType):
        v = self.getProp(propType)
        return max(0.1 + 0.9 / 400 * v, 1 / 400 * v)

    def getWorkEffect(self, propType, funcType = None):
        v = self.getBaseWorkEffect(propType) * getTiredEffect(self.tired)
        if funcType:
            v *= 1 + self.getAbility(funcType)
        return v

    def getProduceTime(self, guild, productId):
        if not self.jobId:
            return 0
        propType = GJD.data.get(self.jobId, {}).get('propType', 0)
        funcType = GFNPDD.data.REDUCE_COMMON_PRODUCT_TIME
        factory = guild._getFactory(GFPD.data.get(productId, {}).get('type', 0))
        if not factory:
            return 0
        rate = 1 - (self.getAbility(GFNPDD.data.REDUCE_PRODUCT_TIME, productId) + self.getAbility(funcType) + factory.getMgrEffect(guild) + guild.getAbility(funcType))
        rate = max(rate, const.GUILD_MIN_RATE)
        t = GFPD.data.get(productId, {}).get('time', 0) * 1.0 / self.getWorkEffect(propType) * rate
        return int(t)

    def getWorkload(self, propType = None, bTired = False, ignoreTime = False, funcType = 0):
        if not self.jobId:
            return 0
        jdata = GJD.data.get(self.jobId)
        if not propType:
            propType = jdata.get('propType')
        if ignoreTime:
            tparam = 1
        else:
            tparam = min(utils.getNow() - self.tJob, const.GUILD_MAINTAIN_INTERVAL) * 1.0 / const.GUILD_MAINTAIN_INTERVAL
            tparam = max(0, tparam)
        if bTired:
            self.tired += int(math.ceil(jdata.get('tired', 0)[propType - 1] * tparam))
            self.tired = min(self.tired, const.GUILD_MAX_TIRED)
            if self.canAddExp():
                exp = self.getWorkExp(tparam * jdata.get('exp', 0), propType)
                self.addExp(exp)
        return jdata.get('progress') * self.getWorkEffect(propType, funcType=funcType) * tparam

    def getWorkExp(self, baseVal, propType):
        return baseVal * getExpParam(self.getQprop(propType))

    def isAdvancedJob(self):
        if not self.jobId:
            return False
        jdata = GJD.data.get(self.jobId)
        return jdata.get('difficulty') == gametypes.GUILD_JOB_DIFFICULTY_ADVANCED

    def onRest(self):
        if not self.jobId:
            if self.tired:
                tired = max(0, self.tired - const.GUILD_TIRED_REGEN)
                self.tired = tired

    def checkStatusLevel(self):
        if self.statusType < gametypes.GUILD_RESIDENT_STATUS_FAMOUS:
            if self.level >= const.GUILD_RESIDENT_STATUS_FAMOUS_LV:
                return False
        elif self.statusType < gametypes.GUILD_RESIDENT_STATUS_GIANT:
            if self.level >= const.GUILD_RESIDENT_STATUS_GIANT_LV:
                return False
        return True

    def canAddExp(self):
        return True

    def addExp(self, val):
        if val <= 0:
            return
        maxExp = GRLD.data.get(self.level).get('maxExp', 0)
        if maxExp:
            self.exp = min(maxExp, self.exp + val)
        else:
            self.exp += val

    def isMaxLv(self):
        return self.level >= const.GUILD_RESIDENT_MAX_LV

    def canLvUp(self):
        if self.isMaxLv():
            return False
        if not self.checkStatusLevel():
            return False
        upExp = GRLD.data.get(self.level + 1).get('upExp', 0)
        return upExp and self.exp >= upExp

    def lvUp(self):
        self.exp -= GRLD.data.get(self.level + 1).get('upExp')
        self.level += 1

    def onInsightToStatus(self, stype):
        bsalary = GRTD.data.get(self.templateId).get('salary', 0)
        self.statusStype = stype
        self.statusType = GSSD.data.get(stype).get('statusType')
        sdata = gametypes.GUILD_RESIDENT_STATUS.get(self.statusType, {})
        salaryRateKey = sdata.get('salaryRate')
        salaryRate = GCD.data.get(salaryRateKey, sdata.get('salaryRateDefault', 1))
        self.salary = int(bsalary * salaryRate)

    def getPSkillSavvyParam(self):
        return (0.05 + self.savvy * 1.0 / 2000) * 100

    def getPSkillCount(self, statusType = 0):
        cnt = 0
        for pskillId in self.pskills.iterkeys():
            if statusType and self.getPSkillStatusType(pskillId) == statusType:
                cnt += 1

        return cnt

    def getPSkillStatusType(self, pskillId, lv = 1):
        return GRPD.data.get((pskillId, lv), {}).get('statusType', 0)

    def learnPSkill(self, pskillId, level = 1):
        pskill = GuildResidentPSkillVal(skillId=pskillId, level=level)
        self.pskills[pskillId] = pskill

    def pskillLevelUp(self, pskillId, level = 0):
        pskill = self.pskills[pskillId]
        if level:
            pskill.level = level
        else:
            pskill.level += 1

    def canPSkillLevelUp(self, pskillId):
        pskill = self.pskills[pskillId]
        return GRPD.data.has_key((pskillId, pskill.level + 1))

    def isPSkillAvail(self, guild, pskillId):
        pskill = self.pskills.get(pskillId)
        if not pskill:
            return False
        if not self.jobId:
            return True
        psdata = GRPD.data.get((pskillId, pskill.level))
        marker = whereJob(guild, self.jobId)
        building = marker and marker.getBuilding(guild)
        for aid, v in psdata.get('funcs'):
            fdata = GFNPD.data.get(aid)
            if not fdata:
                continue
            buildingIds = fdata.get('buildingIds')
            if buildingIds:
                if building and building.buildingId in buildingIds:
                    return True
            else:
                return True

        return False

    def getAvailAbility(self, guild, targetType = 0, jobId = None):
        ability = {}
        if not jobId:
            jobId = self.jobId
        if not jobId:
            return ability
        else:
            marker = whereJob(guild, jobId)
            building = marker and marker.getBuilding(guild)
            jdata = GJD.data.get(jobId)
            dp = {'cpow': self.cpow,
             'cagi': self.cagi,
             'cint': self.cint,
             'cspr': self.cspr}
            for pskillId, pskill in self.pskills.iteritems():
                psdata = GRPD.data.get((pskillId, pskill.level))
                if targetType and psdata.get('targetType') != targetType:
                    continue
                for fparams in psdata.get('funcs'):
                    fv = None
                    if len(fparams) == 4:
                        aid, buildingId, v, fv = fparams
                    else:
                        aid, buildingId, v = fparams
                    if buildingId and (not building or building.buildingId != buildingId):
                        continue
                    jobType = GFNPD.data.get(aid).get('jobType')
                    if jobType and jobType != jdata.get('type'):
                        continue
                    rv = v
                    if not rv:
                        rv = fv and fv(dp) or 0
                        if rv == dp:
                            continue
                    elif isinstance(rv, dict):
                        if not rv.values()[0] and fv:
                            tv = fv(dp)
                            if tv == dp:
                                continue
                            td = {}
                            for tk in rv.iterkeys():
                                td[tk] = tv

                            rv = td
                    doAddAbility(ability, aid, rv)

            return ability


class BaseGuildBuildingMarkerVal(UserSoleType):

    def __init__(self, markerId = 0, buildingNUID = 0, progress = 0, tDev = 0, workers = [], funcWorkers = {}, ability = {}, residentAbility = {}, state = 0):
        self.markerId = markerId
        self.buildingNUID = buildingNUID
        self.progress = progress
        self.tDev = tDev
        self.state = state
        self.workers = copy.deepcopy(workers)
        self.funcWorkers = copy.deepcopy(funcWorkers)
        self.ability = copy.deepcopy(ability)
        self.residentAbility = copy.deepcopy(residentAbility)

    def getAbility(self, aid, subId = None):
        d = self.ability.get(aid, 0)
        if subId:
            return d and d.get(subId, 0) or 0
        else:
            return d

    def addAbility(self, aid, v):
        doAddAbility(self.ability, aid, v)

    def decAbility(self, aid, v):
        doDecAbility(self.ability, aid, v)

    def addResidentAbility(self, nuid, aid, v):
        ability = self.residentAbility.get(nuid)
        if not ability:
            ability = {}
            self.residentAbility[nuid] = ability
        doAddAbility(ability, aid, v)
        self.addAbility(aid, v)

    def removeResidentAbility(self, nuid):
        ability = self.residentAbility.pop(nuid, None)
        if not ability:
            return
        else:
            for aid, v in ability.iteritems():
                self.decAbility(aid, v)

            return

    def getResidentAbility(self, aid, subId = 0):
        v = 0
        for ability in self.residentAbility.itervalues():
            d = ability.get(aid, 0)
            if subId:
                v += d and d.get(subId, 0) or 0
            else:
                v += d

        return v

    def isHide(self, guild):
        building = self.getBuilding(guild)
        if building and building.exist():
            return True
        data = GBMD.data.get(self.markerId)
        if data.get('disabled'):
            return True
        elif guild.level < data.get('glevel', 0):
            return True
        elif not self.isDevFinished():
            return data.get('parentId')
        else:
            return False

    def getFuncWorker(self, guild, jobId):
        workers = self.funcWorkers.get(jobId)
        if not workers:
            return
        for residentNUID in workers:
            resident = guild.hiredResident.get(residentNUID)
            if resident:
                return resident

    def stopFuncWorker(self, guild, jobId):
        workers = copy.copy(self.funcWorkers.get(jobId))
        if not workers:
            return
        for residentNUID in workers:
            resident = guild.hiredResident.get(residentNUID)
            if resident:
                resident.stopWork(guild)
                return resident

    def addWorker(self, guild, jobId, residentNUID):
        jdata = GJD.data.get(jobId)
        tp = jdata.get('type')
        if jdata.get('difficulty') == gametypes.GUILD_JOB_DIFFICULTY_NORMAL and (tp == gametypes.GUILD_JOB_TYPE_DEV or tp == gametypes.GUILD_JOB_TYPE_UPGRADE):
            self.workers.append(residentNUID)
            resident = guild.hiredResident.get(residentNUID)
            for aid, v in resident.getAvailAbility(guild, gametypes.GUILD_FUNC_TARGET_SELF, jobId=jobId).iteritems():
                resident.addJobAbility(aid, v)

        else:
            self.addFuncWorker(guild, jobId, residentNUID)

    def addFuncWorker(self, guild, jobId, residentNUID):
        workers = self.funcWorkers.get(jobId)
        if not workers:
            workers = []
            self.funcWorkers[jobId] = workers
        workers.append(residentNUID)
        resident = guild.hiredResident.get(residentNUID)
        self._applyResidentAbility(guild, jobId, resident)

    def _applyResidentAbility(self, guild, jobId, resident):
        if GJD.data.get(jobId).get('difficulty') == gametypes.GUILD_JOB_DIFFICULTY_ADVANCED:
            for aid, v in resident.getAvailAbility(guild, gametypes.GUILD_FUNC_TARGET_GLOBAL, jobId=jobId).iteritems():
                guild.addResidentAbility(resident.nuid, aid, v)

            for aid, v in resident.getAvailAbility(guild, gametypes.GUILD_FUNC_TARGET_ALL, jobId=jobId).iteritems():
                self.addResidentAbility(resident.nuid, aid, v)

        else:
            for aid, v in resident.getAvailAbility(guild, gametypes.GUILD_FUNC_TARGET_SELF, jobId=jobId).iteritems():
                resident.addJobAbility(aid, v)

    def removeWorker(self, residentNUID):
        if residentNUID in self.workers:
            self.workers.remove(residentNUID)
        for workers in self.funcWorkers.itervalues():
            if residentNUID in workers:
                workers.remove(residentNUID)
                self.removeResidentAbility(residentNUID)

    def hasFuncWorker(self, jobId, residentNUID):
        workers = self.funcWorkers.get(jobId)
        return workers and residentNUID in workers

    def getName(self):
        mdata = GBMD.data.get(self.markerId)
        if mdata.get('name'):
            return mdata.get('name', '')

    def isDevFinished(self):
        if self.state == gametypes.GUILD_DEV_STATE_FINISHED:
            return True
        data = GBMD.data.get(self.markerId)
        r = self.progress >= data.get('progress')
        if r:
            self.state = gametypes.GUILD_DEV_STATE_FINISHED
        return r

    def inDev(self):
        return not self.isDevFinished() and self.tDev > 0

    def getDevState(self):
        if self.inDev():
            return gametypes.GUILD_DEV_STATE_START
        elif self.isDevFinished():
            return gametypes.GUILD_DEV_STATE_FINISHED
        else:
            return gametypes.GUILD_DEV_STATE_NONE

    def inBuilding(self, guild):
        if not self.buildingNUID:
            return False
        building = guild.building.get(self.buildingNUID)
        if not building or not building.inUpgrading() or building.canFinishUpgrading():
            return False
        return True

    def getBuilding(self, guild):
        return guild.building.get(self.buildingNUID)

    def getStep(self):
        data = GBMD.data.get(self.markerId)
        if not data.get('steps'):
            return 0
        return utils.getListIndex(self.progress, data.get('steps'))

    def addDevProgress(self, val):
        oldv = self.progress
        self.progress = min(int(self.progress + val), GBMD.data.get(self.markerId).get('progress', 0))
        return self.progress - oldv

    def stopDev(self, guild, bResetProgress = True):
        self.tDev = 0
        self.state = 0
        if bResetProgress:
            self.progress = 0
        workers = copy.copy(self.workers)
        for residentNUID in workers:
            resident = guild.hiredResident.get(residentNUID)
            if resident and resident.jobId:
                resident.stopWork(guild)

        for jobId, funcWorkers in self.funcWorkers.iteritems():
            jdata = GJD.data.get(jobId)
            if jdata.get('type', 0) == gametypes.GUILD_JOB_TYPE_DEV and jdata.get('difficulty', 0) == gametypes.GUILD_JOB_DIFFICULTY_ADVANCED:
                for residentNUID in copy.copy(funcWorkers):
                    resident = guild.hiredResident.get(residentNUID)
                    if resident and resident.jobId:
                        resident.stopWork(guild)

    def stopBuilding(self, guild):
        building = guild.building.get(self.buildingNUID)
        if building:
            workers = copy.copy(self.workers)
            for residentNUID in workers:
                resident = guild.hiredResident.get(residentNUID)
                if resident and resident.jobId:
                    resident.stopWork(guild)

        for jobId, funcWorkers in self.funcWorkers.iteritems():
            jdata = GJD.data.get(jobId)
            if jdata.get('type', 0) == gametypes.GUILD_JOB_TYPE_UPGRADE and jdata.get('difficulty', 0) == gametypes.GUILD_JOB_DIFFICULTY_ADVANCED:
                for residentNUID in copy.copy(funcWorkers):
                    resident = guild.hiredResident.get(residentNUID)
                    if resident and resident.jobId:
                        resident.stopWork(guild)

    def getFuncWorkerCount(self, jobId):
        workers = self.funcWorkers.get(jobId)
        if workers:
            return len(workers)
        else:
            return 0

    def getDevWorkerLimit(self):
        return GBMD.data.get(self.markerId).get('workerLimit')

    def getBuildingWorkerLimit(self, guild):
        building = self.getBuilding(guild)
        if building.inUpgrading():
            return GBUD.data.get((building.buildingId, building.level + 1)).get('workerLimit')

    def getFuncWorkerLimitByJobId(self, guild, jobId):
        jdata = GJD.data.get(jobId, {})
        if jdata.get('difficulty', 0) == gametypes.GUILD_JOB_DIFFICULTY_ADVANCED:
            return 1
        limit = 0
        building = self.getBuilding(guild)
        limits = jdata.get('workerLimit')
        if limits:
            limit += limits[building.level - 1]
        else:
            limit = GBD.data.get(building.buildingId).get('workerLimit')
        return limit

    def getManager(self, guild, type = gametypes.GUILD_JOB_TYPE_FUNC):
        for jobId, funcWorkers in self.funcWorkers.iteritems():
            if funcWorkers:
                jdata = GJD.data.get(jobId)
                if jdata.get('type') == type and jdata.get('difficulty') == gametypes.GUILD_JOB_DIFFICULTY_ADVANCED:
                    return guild.hiredResident.get(funcWorkers[0])

    def getManagers(self, guild):
        mgrs = []
        for jobId, funcWorkers in self.funcWorkers.iteritems():
            if funcWorkers:
                jdata = GJD.data.get(jobId)
                if jdata.get('difficulty') == gametypes.GUILD_JOB_DIFFICULTY_ADVANCED:
                    for nuid in funcWorkers:
                        mgrs.append(guild.hiredResident.get(nuid))

        return mgrs

    def getFuncWorkerLimit(self, guild, difficulty):
        limit = 0
        building = self.getBuilding(guild)
        for jobId in self.getJobIds(guild):
            jdata = GJD.data.get(jobId, {})
            if jdata.get('difficulty') == difficulty and jdata.get('type') == gametypes.GUILD_JOB_TYPE_FUNC:
                limits = jdata.get('workerLimit', GBD.data.get(building.buildingId).get('workerLimit'))
                if limits:
                    limit += limits[building.level - 1]

        return limit

    def getJobIds(self, guild):
        jobIds = []
        for jobId in GJD.data.iterkeys():
            if whereJob(guild, jobId) == self:
                jobIds.append(jobId)

        return jobIds

    def getFuncWorkers(self, difficulty = gametypes.GUILD_JOB_DIFFICULTY_NORMAL):
        r = []
        for jobId, funcWorkers in self.funcWorkers.iteritems():
            jdata = GJD.data.get(jobId, {})
            if jdata.get('type', 0) == gametypes.GUILD_JOB_TYPE_FUNC and jdata.get('difficulty', 0) == difficulty:
                r.extend(funcWorkers)

        return r

    def getWorkerEffect(self, resident):
        pass

    def getMgrWorkEffect(self, guild):
        if self.inDev():
            return self.getAbility(gametypes.GUILD_FUNC_DEV)
        if self.inBuilding(guild):
            return self.getAbility(gametypes.GUILD_FUNC_BUILDING)
        return 0

    def getBaseWorkload(self, guild, ignoreTime = False, bTired = False, funcType = None):
        if not funcType:
            if self.inDev():
                funcType = GFNPDD.data.DEV_EFFICIENCY
            elif self.inBuilding(guild):
                funcType = GFNPDD.data.BUILDING_EFFICIENCY
        r = 0
        for residentNUID in self.workers:
            resident = guild.hiredResident.get(residentNUID)
            r += resident.getWorkload(bTired=bTired, ignoreTime=ignoreTime, funcType=funcType)

        return r

    def getWorkload(self, guild, ignoreTime = False, bTired = False, funcType = None):
        if not funcType:
            if self.inDev():
                funcType = GFNPDD.data.DEV_EFFICIENCY
            elif self.inBuilding(guild):
                funcType = GFNPDD.data.BUILDING_EFFICIENCY
        v = self.getBaseWorkload(guild, ignoreTime, bTired=bTired, funcType=funcType) * (1 + self.getAbility(funcType) + guild.getAbility(funcType))
        return int(v)

    def getTechFuncWorkEffect(self, guild):
        funcType = GFNPDD.data.FUNC_WORK_EFFICIENCY
        v = guild.getAbility(funcType) + self.getAbility(funcType) - self.getResidentAbility(funcType)
        return round(v * 100.0) / 100

    def getMgrFuncWorkEffect(self, guild, funcType = GFNPDD.data.FUNC_WORK_EFFICIENCY):
        v = self.getResidentAbility(funcType)
        return v

    def getBaseFuncWorkload(self, guild, ignoreTime = False, bTired = False, funcType = GFNPDD.data.FUNC_WORK_EFFICIENCY):
        r = 0
        for jobId, funcWorkers in self.funcWorkers.iteritems():
            jdata = GJD.data.get(jobId)
            if jdata.get('difficulty') == gametypes.GUILD_JOB_DIFFICULTY_NORMAL:
                for residentNUID in funcWorkers:
                    resident = guild.hiredResident.get(residentNUID)
                    if not resident.isAdvancedJob():
                        r += resident.getWorkload(bTired=bTired, ignoreTime=ignoreTime, funcType=funcType)

        return r

    def getFuncWorkload(self, guild, ignoreTime = False, bTired = False, funcType = GFNPDD.data.FUNC_WORK_EFFICIENCY):
        v = self.getBaseFuncWorkload(guild, ignoreTime=ignoreTime, bTired=bTired, funcType=funcType) * (1 + self.getAbility(funcType) + guild.getAbility(funcType)) * 1.0
        return int(v)


class GuildFactoryTaskVal(UserSoleType):

    def __init__(self, nuid = 0, gbId = 0, productId = 0, residentNUID = 0, tStart = 0, tEnd = 0, res = {}):
        self.nuid = nuid
        self.gbId = gbId
        self.productId = productId
        self.residentNUID = residentNUID
        self.tStart = tStart
        self.tEnd = tEnd
        self.res = copy.deepcopy(res)

    def onStart(self, guild, factory):
        self.tStart = utils.getNow()
        resident = guild.hiredResident.get(self.residentNUID)
        self.tEnd = self.tStart + resident.getProduceTime(guild, self.productId)
        resident.subJobId = self.nuid

    def onFinish(self, guild, factory):
        resident = guild.hiredResident.get(self.residentNUID)
        if resident.subJobId == self.nuid:
            resident.subJobId = 0
        else:
            gamelog.warning('inconsistent guild factory task', guild.nuid, self.nuid, resident.nuid, resident.subJobId)
        factory.incProduct(self.productId)
        if BigWorld.component == 'base':
            member = guild.member.get(self.gbId)
            if member:
                contrib = GFPD.data.get(self.productId).get('contrib', 0)
                if contrib:
                    member.addContrib(guild, contrib, op=gametypes.GUILD_LOG_OP_FACTORY_TASK)

    def onCancel(self, guild, factory):
        resident = guild.hiredResident.get(self.residentNUID)
        if resident and resident.subJobId == self.nuid:
            resident.subJobId = 0

    def getDTO(self):
        return (self.nuid,
         self.productId,
         self.residentNUID,
         self.tStart,
         self.tEnd,
         self.res)

    def fromDTO(self, dto):
        self.nuid, self.productId, self.residentNUID, self.tStart, self.tEnd, self.res = dto
        return self


class BaseGuildFactoryVal(UserSoleType):

    def __init__(self, type = 0, product = {}, task = {}, queue = []):
        self.type = type
        self.product = copy.deepcopy(product)
        self.task = copy.deepcopy(task)
        self.queue = copy.deepcopy(queue)

    def incProduct(self, productId, cnt = 1):
        if self.product.has_key(productId):
            self.product[productId] += cnt
        else:
            self.product[productId] = cnt

    def decProduct(self, productId, cnt = 1):
        v = self.product.get(productId, 0)
        if v:
            v -= cnt
            if v:
                self.product[productId] = v
            else:
                self.product.pop(productId)

    def hasProduct(self, productId, cnt = 1):
        v = self.product.get(productId, 0)
        return v >= cnt

    def findInQueue(self, taskNUID):
        for task in self.queue:
            if task.nuid == taskNUID:
                return task

    def cancelQueue(self, guild, taskNUID):
        task = self.findInQueue(taskNUID)
        if task:
            self.queue.remove(task)
            task.onCancel(guild, self)
            return task
        else:
            return None

    def cancelTask(self, guild, taskNUID):
        task = self.task.pop(taskNUID, None)
        if task:
            task.onCancel(guild, self)
        return task

    def getDTO(self):
        return (self.type,
         self.product,
         [ t.getDTO() for t in self.task.itervalues() ],
         [ t.getDTO() for t in self.queue ])

    def fromDTO(self, dto):
        self.type, self.product, task, queue = dto
        for t in task:
            t = GuildFactoryTaskVal().fromDTO(t)
            self.task[t.nuid] = t

        for t in queue:
            t = GuildFactoryTaskVal().fromDTO(t)
            self.queue.append(t)

        return self

    def getMarker(self, guild):
        return guild.marker.get(guild._getFactoryBuildingId(self.type))

    def getMgrEffect(self, guild):
        marker = self.getMarker(guild)
        funcType = GFNPDD.data.REDUCE_COMMON_PRODUCT_TIME
        return marker.getMgrFuncWorkEffect(guild, funcType)

    def getProduceCost(self, guild, productId):
        marker = self.getMarker(guild)
        pdata = GFPD.data.get(productId)
        mojing, xirang, wood, bindCash = (pdata.get('mojing'),
         pdata.get('xirang'),
         pdata.get('wood'),
         pdata.get('bindCash'))
        rc = marker.getAbility(GFNPDD.data.REDUCE_COMMON_PRODUCT_COST)
        consumeItems = pdata.get('consumeItems', ())
        if rc > 0:
            rate = max(1 - rc, const.GUILD_MIN_RATE)
            mojing = int(math.ceil(mojing * rate))
            xirang = int(math.ceil(xirang * rate))
            wood = int(math.ceil(wood * rate))
            bindCash = int(math.ceil(bindCash * rate))
        return (mojing,
         xirang,
         wood,
         bindCash,
         consumeItems)

    def getIncomingProductCnt(self, productId):
        cnt = 0
        for task in self.task.itervalues():
            if task.productId == productId:
                cnt += 1

        for task in self.queue:
            if task.productId == productId:
                cnt += 1

        return cnt

    def getProductCnt(self, productId, includeIncoming = False):
        if includeIncoming:
            return self.product.get(productId, 0) + self.getIncomingProductCnt(productId)
        else:
            return self.product.get(productId, 0)


class BaseGuildTechnologyVal(UserSoleType):

    def __init__(self, techId = 0, state = 0, progress = 0):
        self.techId = techId
        self.state = state
        self.progress = progress

    def getDTO(self):
        return (self.techId, self.state, self.progress)

    def fromDTO(self, dto):
        self.techId, self.state, self.progress = dto
        return self

    def cancelResearching(self):
        self.state = 0
        self.progress = 0

    def inResearching(self):
        return self.state == gametypes.GUILD_TECHNOLOGY_STATE_START

    def isAvail(self):
        return self.state == gametypes.GUILD_TECHNOLOGY_STATE_FINISH

    def getBuilding(self, guild):
        return guild.getBuildingById(GTD.data.get(self.techId, {}).get('buildingId'))

    def getManager(self, guild, type = gametypes.GUILD_JOB_TYPE_FUNC):
        building = self.getBuilding(guild)
        if not building:
            return None
        else:
            return building.getManager(guild, type)

    def getWorkload(self, guild):
        progress = 0
        manager = self.getManager(guild)
        if not manager:
            return progress
        return progress

    def addProgress(self, val):
        tdata = GTD.data.get(self.techId)
        self.progress = min(self.progress + val, tdata.get('progress'))

    def checkFinishResearch(self):
        tdata = GTD.data.get(self.techId)
        if self.progress >= tdata.get('progress'):
            self.state = gametypes.GUILD_TECHNOLOGY_STATE_FINISH
            return True
        return False

    def getAbility(self):
        tdata = GTD.data.get(self.techId)
        if BigWorld.component in ('base', 'cell'):
            armyConfig = gameconfig.enableWingWorldGuildRoleOptimization()
        else:
            armyConfig = gameglobal.rds.configData.get('enableWingWorldGuildRoleOptimization', False)
        if armyConfig:
            return tdata.get('funcs2', ())
        else:
            return tdata.get('funcs', ())

    def applyAbility(self, guild):
        tdata = GTD.data.get(self.techId)
        if not tdata:
            return
        buildingId = tdata.get('buildingId', 0)
        if buildingId in gametypes.GUILD_TECH_MULTI_BUILDING:
            building = self.getBuilding(guild)
            if building:
                marker = building.getMarker(guild)
                if marker:
                    for aid, v in self.getAbility():
                        if GFNPD.data.get(aid).get('gsync'):
                            guild.addAbility(aid, v)
                        else:
                            marker.addAbility(aid, v)

        else:
            for aid, v in self.getAbility():
                guild.addAbility(aid, v)

    def removeAbility(self, guild):
        tdata = GTD.data.get(self.techId)
        if not tdata:
            return
        buildingId = tdata.get('buildingId', 0)
        if buildingId in gametypes.GUILD_TECH_MULTI_BUILDING:
            building = self.getBuilding(guild)
            if building:
                marker = building.getMarker(guild)
                if marker:
                    for aid, v in self.getAbility():
                        if GFNPD.data.get(aid).get('gsync'):
                            guild.decAbility(aid, v)
                        else:
                            marker.decAbility(aid, v)

        else:
            for aid, v in self.getAbility():
                guild.decAbility(aid, v)


class BaseGuildPSkillVal(UserSoleType):

    def __init__(self, skillId = 0, level = 0, tEnd = 0, tStart = 0):
        self.skillId = skillId
        self.level = level
        self.tStart = tStart
        self.tEnd = tEnd

    def getResearchTime(self, guild):
        building = guild.getBuildingById(gametypes.GUILD_BUILDING_GROWTH_ID)
        marker = building.getMarker(guild)
        level = self.level + 1
        timeVal = GPD.data.get((self.skillId, level)).get('time', 1)
        timeVal = timeVal * (1 - marker.getAbility(GFNPDD.data.REDUCE_COMMON_PSKILL_RESEACH_TIME) - marker.getAbility(GFNPDD.data.REDUCE_PSKILL_RESEACH_TIME, self.skillId) - guild.getAbility(GFNPDD.data.REDUCE_COMMON_PSKILL_RESEACH_TIME) - guild.getAbility(GFNPDD.data.REDUCE_PSKILL_RESEACH_TIME, self.skillId))
        return max(int(math.ceil(timeVal)), 1)

    def getLearnMoney(self, guild, money):
        building = guild.getBuildingById(gametypes.GUILD_BUILDING_GROWTH_ID)
        marker = building.getMarker(guild)
        rate = 1 - marker.getAbility(GFNPDD.data.REDUCE_LEARN_PSKILL_COST, self.skillId) - guild.getAbility(GFNPDD.data.REDUCE_LEARN_PSKILL_COST, self.skillId) - guild.getAbility(GFNPDD.data.REDUCE_COMMON_LEARN_PSKILL_COST)
        rate = max(rate, const.GUILD_MIN_RATE)
        money = money * rate
        return max(int(math.ceil(money)), 1)

    def getLearnContrib(self, guild, contrib):
        building = guild.getBuildingById(gametypes.GUILD_BUILDING_GROWTH_ID)
        marker = building.getMarker(guild)
        rate = 1 - marker.getAbility(GFNPDD.data.REDUCE_LEARN_PSKILL_COST, self.skillId) - guild.getAbility(GFNPDD.data.REDUCE_LEARN_PSKILL_COST, self.skillId) - guild.getAbility(GFNPDD.data.REDUCE_COMMON_LEARN_PSKILL_COST)
        rate = max(rate, const.GUILD_MIN_RATE)
        contrib = contrib * rate
        return max(int(math.ceil(contrib)), 1)

    def finishUpgrade(self, guild):
        if self.isUpgrading():
            self.tStart = 0
            self.tEnd = 0
            self.level += 1
            return True
        return False

    def isUpgrading(self):
        return self.tStart > 0 and self.tEnd > 0


class BaseGuildGrowthVal(UserSoleType):

    def __init__(self, propertyId = 0, level = 0, active = False):
        self.propertyId = propertyId
        self.level = level
        self.active = active

    def getLearnMoney(self, guild, money):
        building = guild.getBuildingById(gametypes.GUILD_BUILDING_GROWTH_ID)
        marker = building.getMarker(guild)
        rate = 1 - marker.getAbility(GFNPDD.data.REDUCE_LEARN_GROWTH_COST, self.propertyId) - guild.getAbility(GFNPDD.data.REDUCE_LEARN_GROWTH_COST, self.propertyId) - guild.getAbility(GFNPDD.data.REDUCE_COMMON_LEARN_GROWTH_COST)
        rate = max(rate, const.GUILD_MIN_RATE)
        money = money * rate
        return int(math.ceil(money))

    def getLearnContrib(self, guild, contrib):
        building = guild.getBuildingById(gametypes.GUILD_BUILDING_GROWTH_ID)
        marker = building.getMarker(guild)
        rate = 1 - marker.getAbility(GFNPDD.data.REDUCE_LEARN_GROWTH_COST, self.propertyId) - guild.getAbility(GFNPDD.data.REDUCE_LEARN_GROWTH_COST, self.propertyId) - guild.getAbility(GFNPDD.data.REDUCE_COMMON_LEARN_GROWTH_COST)
        rate = max(rate, const.GUILD_MIN_RATE)
        contrib = contrib * rate
        return int(math.ceil(contrib))

    def getLearnCost(self, guild, money, contrib):
        building = guild.getBuildingById(gametypes.GUILD_BUILDING_GROWTH_ID)
        marker = building.getMarker(guild)
        rate = 1 - marker.getAbility(GFNPDD.data.REDUCE_LEARN_GROWTH_COST, self.propertyId) - guild.getAbility(GFNPDD.data.REDUCE_LEARN_GROWTH_COST, self.propertyId) - guild.getAbility(GFNPDD.data.REDUCE_COMMON_LEARN_GROWTH_COST)
        rate = max(rate, const.GUILD_MIN_RATE)
        money = money * rate
        contrib = contrib * rate
        return (int(math.ceil(money)), int(math.ceil(contrib)))


class GuildTutorialStepVal(UserSoleType):

    def __init__(self, stepId = 0, progress = 0):
        self.stepId = stepId
        self.progress = progress

    def getDTO(self):
        return (self.stepId, self.progress)

    def fromDTO(self, dto):
        self.stepId, self.progress = dto
        return self


class GuildActivityVal(UserSoleType):

    def __init__(self, aid = 0, nextTime = 0, state = 0, data = {}, tStart = 0, cnt = 0):
        self.aid = aid
        self.nextTime = nextTime
        self.state = state
        self.data = copy.deepcopy(data)
        self.tStart = tStart
        self.cnt = cnt

    def getDTO(self):
        cdata = {}
        for attr in ACTIVITY_CLIENT_DATA_ATTR:
            if self.data.has_key(attr):
                cdata[attr] = self.data.get(attr)

        return (self.aid,
         self.state,
         self.nextTime,
         self.cnt,
         cdata)

    def fromDTO(self, dto):
        self.aid, self.state, self.nextTime, self.cnt, self.data = dto
        return self

    def getState(self):
        if self.state in gametypes.GUILD_ACTIVITY_ACTIVE_STATE:
            return self.state
        data = GATD.data.get(self.aid)
        cdType = data.get('cdType', 0)
        if self.nextTime:
            if cdType == gametypes.GUILD_ACTIVITY_CD_WEEKLY:
                if utils.getWeekSecond(self.nextTime) > utils.getWeekSecond():
                    return gametypes.GUILD_ACTIVITY_END
            elif cdType == gametypes.GUILD_ACTIVITY_CD_DAILY:
                if utils.getDaySecond(self.nextTime) > utils.getDaySecond():
                    return gametypes.GUILD_ACTIVITY_END
        if cdType == gametypes.GUILD_ACTIVITY_CD_DAILY_MULTI:
            if self.cnt >= data.get('limitNum', 0):
                return gametypes.GUILD_ACTIVITY_END
        return gametypes.GUILD_ACTIVITY_READY


class GuildMemberActionStatsVal(UserSoleType):

    def __init__(self, contrib = 0, bindCash = 0, action = {}):
        self.contrib = contrib
        self.bindCash = bindCash
        self.action = copy.deepcopy(action)

    def getDTO(self):
        return (self.contrib, self.bindCash, self.action)

    def fromDTO(self, dto):
        self.contrib, self.bindCash, self.action = dto
        return self


class BaseGuildPayVal(UserSoleType):

    def __init__(self, nuid = 0, gbId = 0, amount = 0, tWhen = 0, tExpire = 0, tPaid = 0, salaryType = 0):
        self.nuid = nuid
        self.gbId = gbId
        self.amount = amount
        self.tWhen = tWhen
        self.tExpire = tExpire
        self.tPaid = tPaid
        self.salaryType = salaryType

    def isExpired(self):
        return self.tExpire <= utils.getNow()

    def isPaid(self):
        return self.tPaid > 0

    def isUnpaid(self):
        return not self.isExpired() and self.tPaid == 0


class BaseGuildWSPracticeVal(UserSoleType):

    def __init__(self, idx = 0, skillId = 0, duration = 0, tStart = 0, val = 0, interval = 0, cnt = 0, tCost = 0):
        self.idx = idx
        self.skillId = skillId
        self.duration = duration
        self.tStart = tStart
        self.val = val
        self.interval = interval
        self.cnt = cnt
        self.tCost = tCost

    def stop(self, owner):
        self.skillId = 0
        self.duration = 0
        self.val = 0
        self.interval = 0
        self.cnt = 0
        self.tCost = 0

    def onInterval(self):
        self.cnt += 1
        self.tCost += self.interval

    def isFinished(self):
        return self.tCost >= self.duration

    def isBusy(self):
        return self.skillId > 0

    def getDTO(self):
        return (self.idx,
         self.skillId,
         self.duration,
         self.tStart,
         self.val,
         self.interval,
         self.cnt,
         self.tCost)

    def fromDTO(self, dto):
        self.idx, self.skillId, self.duration, self.tStart, self.val, self.interval, self.cnt, self.tCost = dto
        return self

    def isAvailToday(self):
        return not utils.isSameDay(self.tStart)


class RunManPlayerMarkerVal(UserSoleType):

    def __init__(self, passed = False, passNum = 0):
        self.passed = passed
        self.passNum = passNum

    def onPass(self):
        self.passed = True
        self.passNum += 1

    def getDTO(self):
        return (self.passed, self.passNum)


class RunManPlayerRouteVal(UserDictType):

    def __init__(self, runManType = 0, state = 0, currNum = 0, tStart = 0, passNum = 0):
        self.runManType = runManType
        self.state = state
        self.currNum = currNum
        self.tStart = tStart
        self.passNum = passNum

    def isFinished(self):
        lastIdx = len(self)
        mVal = self.get(lastIdx)
        if mVal and mVal.passed and not GRMRD.data.get((self.runManType, lastIdx + 1)):
            return True
        else:
            return False

    def _getMarkerData(self, num = 0):
        if not num:
            num = self.currNum
        return GRMRD.data.get((self.runManType, num))

    def _getData(self):
        return GRMD.data.get(self.runManType)

    def getMarkerNpcId(self, num = 0):
        data = self._getMarkerData(num=num)
        if data:
            return data.get('markerNpcId')
        else:
            return 0

    def getMarkerSeekId(self, num = 0):
        data = self._getMarkerData(num=num)
        if data:
            return data.get('seekId')
        else:
            return 0

    def getName(self):
        return self._getData().get('name')

    def isCompleted(self):
        return self.currNum and not self._getMarkerData(self.currNum + 1)

    def isExpired(self):
        markerData = self._getMarkerData()
        return self.tStart + markerData.get('time', 0) <= utils.getNow()

    def getDTO(self):
        return (self.runManType, self.passNum, [ (idx, x.getDTO()) for idx, x in self.iteritems() ])


class RunManPlayerRoute(UserDictType):

    def isMarkerVisible(self, markerNpcId):
        runManType, idx = getRunManRouteFromNpcId(markerNpcId)
        if runManType:
            route = self.getRoute(runManType)
            return route.state == gametypes.GUILD_RUN_MAN_STATE_OPEN
        return False

    def isMarkerActive(self, markerNpcId):
        runManType, idx = getRunManRouteFromNpcId(markerNpcId)
        if runManType:
            route = self.getRoute(runManType)
            return route.state == gametypes.GUILD_RUN_MAN_STATE_OPEN and route.currNum <= idx


def getRunManRouteFromNpcId(npcId):
    for (runManType, idx), data in GRMRD.data.iteritems():
        if data.get('markerNpcId') == npcId:
            return (runManType, idx)

    return (0, 0)


class GuildRedPacketVal(UserSoleType):

    def __init__(self, sn = 0, pType = 0, subType = 0, tWhen = 0, photo = '', state = 0, srcGbId = 0, srcName = '', amount = 0, cnt = 0, dirty = False, doublePlayers = set()):
        self.sn = sn
        self.pType = pType
        self.subType = subType
        self.tWhen = tWhen
        self.photo = photo
        self.state = state
        self.srcGbId = srcGbId
        self.srcName = srcName
        self.amount = amount
        self.cnt = cnt
        self.data = []
        self.assignInfo = []
        self.dirty = dirty
        self.doublePlayers = copy.copy(doublePlayers)

    def getDTO(self):
        return (self.sn,
         self.pType,
         self.subType,
         self.tWhen,
         self.state,
         self.photo,
         self.srcGbId,
         self.srcName,
         self.amount,
         self.cnt,
         self.assignInfo,
         self.data[:len(self.assignInfo)],
         self.doublePlayers)

    def fromDTO(self, dto):
        self.sn, self.pType, self.subType, self.tWhen, self.state, self.photo, self.srcGbId, self.srcName, self.amount, self.cnt, self.assignInfo, self.data, self.doublePlayers = dto
        return self

    def getSimpleDTO(self, gbId = 0):
        return (self.sn,
         self.pType,
         self.subType,
         self.tWhen,
         self.state,
         self.photo,
         self.srcGbId,
         self.srcName,
         self.amount,
         self.cnt,
         self.getAssignNum(gbId))

    def fromSimpleDTO(self, dto):
        self.sn, self.pType, self.subType, self.tWhen, self.state, self.photo, self.srcGbId, self.srcName, self.amount, self.cnt, self.received = dto
        return self

    def isExpired(self):
        return not utils.isSameDay(self.tWhen)

    def isAllAssigned(self):
        return len(self.data) <= len(self.assignInfo)

    def isAvail(self, gbId):
        return not self.isExpired() and self.state != gametypes.GUILD_RED_PACKET_STATE_DONE and not self.hasAssigned(gbId)

    def hasAssigned(self, gbId):
        for _gbId, _ in self.assignInfo:
            if _gbId == gbId:
                return True

        return False

    def getAssignNum(self, gbId):
        for i, (_gbId, _) in enumerate(self.assignInfo):
            if _gbId == gbId:
                return self.data[i]

        return 0

    def assign(self, gbId, roleName):
        if self.isAllAssigned():
            return False
        if self.hasAssigned(gbId):
            return False
        self.assignInfo.append((gbId, roleName))
        if self.isAllAssigned():
            self.state = gametypes.GUILD_RED_PACKET_STATE_DONE
        self.dirty = True
        return True

    def setPlayerDoubleReward(self, fGbId):
        self.doublePlayers.add(fGbId)
        self.dirty = True

    def getLastNum(self):
        if not self.assignInfo:
            return 0
        return self.data[len(self.assignInfo) - 1]

    def getSrc(self):
        msg = ''
        if self.srcGbId:
            msg = self.srcName
        elif self.pType == const.RED_PACKET_TYPE_GUILD:
            msg = GCD.data.get('redPacketSignInNameDict', {}).get(self.subType, '')
        elif self.pType == const.RED_PACKET_TYPE_GUILD_MERGER_CLAP:
            msg = GCD.data.get('guildMergerClapredPacketName', gameStrings.TEXT_COMMGUILD_1907)
        return msg

    def getMsg(self):
        msg = ''
        if self.srcGbId:
            adata = AD.data.get(self.subType)
            if adata:
                msg = adata.get('name')
        elif self.pType == const.RED_PACKET_TYPE_GUILD:
            msg = GCD.data.get('redPacketSignInNameDict', {}).get(self.subType, '')
        return msg

    def getRichText(self, owner):
        return '[redpacket%s]' % SCD.data.get('redPacketSplit', const.RED_PACKET_SPLIT).join((self.sn,
         str(self.pType),
         self.getMsg(),
         self.photo,
         self.srcName,
         str(self.amount),
         str(self.cnt),
         str(self.tWhen)))


class AchieveRedPacketVal(UserSoleType):

    def __init__(self, gbId = 0, achieveId = 0, tWhen = 0):
        self.gbId = gbId
        self.achieveId = achieveId
        self.tWhen = tWhen

    def getDTO(self):
        return (self.gbId, self.achieveId)

    def fromDTO(self, dto):
        self.gbId, self.achieveId = dto
        return self


class GuildRedPacket(UserDictType):

    def __init__(self, signInRedPacket = {}, sendEndTime = 0, achieveRedPacketPool = [], ver = 0, poolVer = 0):
        self.signInRedPacket = copy.deepcopy(signInRedPacket)
        self.achieveRedPacketPool = copy.deepcopy(achieveRedPacketPool)
        self.sendEndTime = sendEndTime
        self.ver = ver
        self.poolVer = poolVer

    def isSent(self, idx):
        return self.signInRedPacket.get(idx)

    def markSent(self, idx):
        self.signInRedPacket[idx] = True

    def isSendActive(self):
        return utils.getNow() <= self.sendEndTime

    def fromPoolDTO(self, dto):
        self.achieveRedPacketPool = []
        for d in dto:
            v = AchieveRedPacketVal().fromDTO(d)
            self.achieveRedPacketPool.append(v)

    def getInPool(self, gbId, achieveId):
        for v in self.achieveRedPacketPool:
            if v.gbId == gbId and v.achieveId == achieveId:
                return v

        return False

    def removeFromPool(self, gbId, achieveId):
        for i, v in enumerate(self.achieveRedPacketPool):
            if v.gbId == gbId and v.achieveId == achieveId:
                return self.achieveRedPacketPool.pop(i)


class GuildMergerVal(UserSoleType):

    def __init__(self, fGuildNUID = 0, tGuildNUID = 0, fGuildName = '', tGuildName = '', fComfirm = 0, tComfirm = 0, state = 0, callbackHander = 0, tStateEnd = 0):
        self.guildMergerKey = (fGuildNUID, tGuildNUID)
        self.stepComfirm = [fComfirm, tComfirm]
        self.guildNames = (fGuildName, tGuildName)
        self.state = state
        self.callbackHander = callbackHander
        self.tStateEnd = tStateEnd
        super(GuildMergerVal, self).__init__()

    def getDTO(self):
        return (self.guildMergerKey,
         self.stepComfirm,
         self.guildNames,
         self.state,
         self.tStateEnd)

    def fromDTO(self, dto):
        self.guildMergerKey, self.stepComfirm, self.guildNames, self.state, self.tStateEnd = dto

    def isAllComfirm(self):
        return all(self.stepComfirm)

    def setComfirm(self, guildNUID):
        index = self.guildMergerKey.index(guildNUID)
        self.stepComfirm[index] = True

    def cancelComfirm(self, guildNUID):
        index = self.guildMergerKey.index(guildNUID)
        self.stepComfirm[index] = False

    def cancelAllComfirm(self):
        self.stepComfirm = [False, False]

    def getComfirm(self, guildNUID):
        index = self.guildMergerKey.index(guildNUID)
        return self.stepComfirm[index]

    def getOtherNUID(self, guildNUID):
        index = self.guildMergerKey.index(guildNUID)
        index += 1
        otherIndex = index % 2
        return self.guildMergerKey[otherIndex]

    def getFromGuildNUID(self):
        return self.guildMergerKey[0]

    def getToGuildNUID(self):
        return self.guildMergerKey[1]

    def getFromGuildName(self):
        return self.guildNames[0]

    def getToGuildName(self):
        return self.guildNames[1]

    def getGuildNameViaNUID(self, guildNUID):
        try:
            index = self.guildMergerKey.index(guildNUID)
            return self.guildNames[index]
        except Exception as e:
            return ''

    def getOtherGuildNameViaNUID(self, guildNUID):
        try:
            index = self.guildMergerKey.index(guildNUID)
            index += 1
            otherIndex = index % 2
            return self.guildNames[otherIndex]
        except Exception as e:
            return ''

    def resetAll(self):
        self.guildMergerKey = (0, 0)
        self.stepComfirm = [False, False]
        self.guildNames = ('', '')
        self.state = 0
        self.tStateEnd = 0

    def __repr__(self):
        return 'guilds:{}, steps:{}, guildNames:{}, state:{}, tStateEnd:{})'.format(self.guildMergerKey, self.stepComfirm, self.guildNames, self.state, self.tStateEnd)


def isGuildGrowthVolumnActivated(owner, volumnId, reqLv = 0, bldLv = 0, bNotify = False, bLearn = False):
    data = GGVD.data.get(volumnId, {})
    if bldLv and bldLv < data.get('bldLv', 0):
        bNotify and owner.client.showGameMsg(GMDD.data.GUILD_ACTIVATE_GROWTH_BLDLV, (data.get('bldLv', 0),))
        return False
    if not bLearn and reqLv and reqLv < data.get('reqLv', 0):
        bNotify and owner.client.showGameMsg(GMDD.data.GUILD_ACTIVATE_GROWTH_REQLV, (data.get('reqLv', 0),))
        return False
    if utils.getTotalSkillEnhancePoint(owner) < data.get('skillEnhancePoint', 0):
        bNotify and owner.client.showGameMsg(GMDD.data.GUILD_ACTIVATE_GROWTH_NEED_ENHANCEPOINT, (data.get('skillEnhancePoint', 0),))
        return False
    condition = data.get('condition')
    if condition:
        for vlmnId, score in condition:
            volumn = owner.guildGrowth.get(vlmnId)
            if not volumn or volumn.score < score:
                bNotify and owner.client.showGameMsg(GMDD.data.GUILD_GROWTH_CONDITION, (GGVD.data.get(vlmnId, {}).get('name'), score))
                return False

    return True


def getPSkillName(pskillId):
    key = (pskillId, 1)
    if GPD.data.get(key, {}).get('type') == gametypes.GUILD_PSKILL_TYPE_PASSIVE:
        return PSTD.data.get(pskillId, {}).get('sname')
    else:
        return GPD.data.get(key, {}).get('name', '')


def calcMaintainFee(guild, inDebt = False):
    mojing = 0
    xirang = 0
    wood = 0
    bindCash = 0
    if BigWorld.component == 'client':
        hours = 1
    else:
        hours = int(round((utils.getNow() - guild.tLastMaintain) * 1.0 / const.GUILD_MAINTAIN_INTERVAL))
        if hours == 0:
            return (mojing,
             xirang,
             wood,
             bindCash)
    baseMojing, baseXirang, baseWood, baseBindCash = guild._getBaseMaintainFee()
    mojing += baseMojing
    xirang += baseXirang
    wood += baseWood
    bindCash += baseBindCash
    if not inDebt:
        growthMojing, growthXirang, growthWood, growthBindCash = guild._getGrowthMaintainFee()
        mojing += growthMojing
        xirang += growthXirang
        wood += growthWood
        bindCash += growthBindCash
        buildingMojing, buildingXirang, buildingWood, buildingBindCash = guild._getBuildingMaintainFee()
        mojing += buildingMojing
        xirang += buildingXirang
        wood += buildingWood
        bindCash += buildingBindCash
    salary = guild._getTotalSalary()
    bindCash += salary
    rate = guild._getMaintainFeeRate()
    rate *= max(1 - guild.getAbility(GFNPDD.data.REDUCE_MAINTAIN_FEE), const.GUILD_MIN_RATE)
    bindCash = int(math.ceil(bindCash * rate * hours))
    mojing = int(math.ceil(mojing * rate * hours))
    xirang = int(math.ceil(xirang * rate * hours))
    wood = int(math.ceil(wood * rate * hours))
    return (mojing,
     xirang,
     wood,
     bindCash)


def getStabilityRegen(guild):
    v = GCD.data.get('defaultStabilityRegen', const.GUILD_DEFAULT_STABILITY_REGEN)
    v *= 1 + guild.getAbility(GFNPDD.data.STABILITY_REGEN)
    return v


def whichFactoryType(jobId):
    try:
        return GFD.data.get(1).get('jobIds').index(jobId) + 1
    except:
        return None


def getJobFuncType(guild, jobId):
    if not jobId:
        return
    else:
        jdata = GJD.data.get(jobId)
        jtype = jdata.get('type')
        if jtype == gametypes.GUILD_JOB_TYPE_DEV:
            return gametypes.GUILD_FUNC_DEV
        if jtype == gametypes.GUILD_JOB_TYPE_UPGRADE:
            return gametypes.GUILD_FUNC_BUILDING
        marker = whereJob(guild, jobId)
        if not marker:
            return
        building = marker.getBuilding(guild)
        if not building:
            return
        if building.buildingId in (gametypes.GUILD_BUILDING_FACTORY_MACHINE_ID, gametypes.GUILD_BUILDING_FACTORY_FACILITY_ID):
            ftype = whichFactoryType(jobId)
            if ftype != None:
                return gametypes.GUILD_FACTORY_FUNCS[ftype - 1]
        return GBD.data.get(building.buildingId).get('funcType')


def whereJob(guild, jobId):
    if not jobId:
        return
    else:
        jdata = GJD.data.get(jobId, None)
        if jdata:
            placeType, placeId = jdata.get('placeType', 0), jdata.get('placeId', 0)
            if placeType == gametypes.GUILD_JOB_PLACE_MARKER:
                return guild.marker.get(placeId)
        return


def initWorkers(guild):
    for resident in guild.hiredResident.itervalues():
        jobId = resident.jobId
        if jobId:
            marker = whereJob(guild, jobId)
            if marker:
                marker.addWorker(guild, jobId, resident.nuid)


def getTiredType(val):
    return utils.getListIndex(val, const.GUILD_TIRED)


def getTiredEffect(val):
    return const.GUILD_TIRED_EFFECT[getTiredType(val)]


def getExpParam(val):
    return const.GUILD_PROP_EXP_PARAM[utils.getListIndex(val, const.GUILD_PROP_EXP)]


def getJobIdFromGJRD(markerId, difficulty, type, placeType = gametypes.GUILD_JOB_PLACE_MARKER):
    jobList = GJRD.data.get((placeType, markerId), {}).get(difficulty, [])
    for jobId in jobList:
        jobInfo = GJD.data.get(jobId, {})
        if jobInfo.get('type', 0) == type:
            return jobId

    return 0


def getBuildingsById(guild, buildingId, bAvail):
    return [ b for b in guild.building.itervalues() if b.buildingId == buildingId and (not bAvail or b.level > 0) ]


def findResident(guild, name):
    for resident in guild.hiredResident.itervalues():
        if resident.name == name:
            return resident


def isMultiBuilding(buildingId):
    return GBD.data.get(buildingId).get('limit')


def isMultiBuildingMarker(markerId):
    buildingIds = GBMD.data.get(markerId, {}).get('buildingId', None)
    return isinstance(buildingIds, tuple) and len(buildingIds) > 1


def getMarkerIdByBuildingId(guild, buildingId):
    if not guild:
        return 0
    else:
        for markerId in guild.marker.iterkeys():
            buildingNUID = guild.marker[markerId].buildingNUID
            buildValue = guild.building.get(buildingNUID) if buildingNUID else None
            if buildValue and buildValue.buildingId == buildingId:
                return markerId

        return 0


def getBuildNameByJobId(guild, jobId):
    marker = whereJob(guild, jobId)
    if marker:
        buildValue = guild.building.get(marker.buildingNUID) if marker.buildingNUID else None
        if buildValue:
            return buildValue.getName()
        else:
            return marker.getName()
    return ''


def getGuildBuildingImgPath(imgPath):
    return 'guildBuilding/%s.dds' % imgPath


def onNotInDebt(guild):
    if guild.state == gametypes.GUILD_STATE_ACTIVE:
        guild.tMaintainDestroy = 0


def doAddAbility(ability, aid, v):
    if ability.has_key(aid):
        if isinstance(v, dict):
            ev = ability.get(aid)
            for _k, _v in v.iteritems():
                if ev.has_key(_k):
                    ev[_k] += _v
                else:
                    ev[_k] = _v

        else:
            ability[aid] += v
    elif isinstance(v, dict):
        tv = {}
        for _k, _v in v.iteritems():
            tv[_k] = _v

        ability[aid] = tv
    else:
        ability[aid] = v


def doDecAbility(ability, aid, v):
    if ability.has_key(aid):
        if isinstance(v, dict):
            ev = ability.get(aid)
            for _k, _v in v.iteritems():
                if ev.has_key(_k):
                    ev[_k] -= _v
                    if not ev[_k]:
                        ev.pop(_k)

        else:
            ability[aid] -= v
            if not ability[aid]:
                ability.pop(aid)


def getGuildFlagItemCnt(owner, amount, timeInterval):
    if BigWorld.component in 'cell':
        current = time.time()
    elif BigWorld.component in 'client':
        current = BigWorld.player().getServerTime()
    remainTime = timeInterval - (current - owner.updateGuildIconTime)
    if remainTime <= 0:
        return 0
    elif remainTime > timeInterval * 0.5:
        return amount
    elif remainTime > timeInterval * 0.25:
        return int(amount * 0.5)
    else:
        return int(amount * 0.25)


def getNoticeBoardItemCnt(owner, amount, timeInterval):
    if BigWorld.component in 'cell':
        current = time.time()
    elif BigWorld.component in 'client':
        current = BigWorld.player().getServerTime()
    remainTime = timeInterval - (current - owner.uploadTime)
    if remainTime <= 0:
        return 0
    elif remainTime > timeInterval * 0.5:
        return amount
    elif remainTime > timeInterval * 0.25:
        return int(amount * 0.5)
    else:
        return int(amount * 0.25)


def calcLuxury(cash, coin):
    luxuryValue = min(const.GUILD_MAX_LUXURY, coin * const.GUILD_LUXURY_COIN_RATE)
    return luxuryValue


def calcPkEnemyCost(numGuild, numClan):
    return GCD.data.get('pkEnemyGuildCost', 0) * numGuild + GCD.data.get('pkEnemyClanCost', 0) * numClan


def getMemberShopMaxRefreshCnt():
    return len(GCD.data.get('treasureRefreshContribCntParam', ()))


def calcGrowthItemAndMoney(owner, useItem, data):
    items = data.get('item')
    if not items:
        return (None, {}, 0)
    else:
        msgInfo = None
        needMoney = 0
        needItems = {}
        for itemId, cnt in items:
            if useItem:
                rcnt = owner.inv.countItemInPages(itemId, enableParentCheck=True)
            else:
                rcnt = 0
            if rcnt < cnt:
                price = 0
                for _itemId, v in data.get('itemReplaceMoney', ()):
                    if _itemId == itemId:
                        price = v
                        break

                if not price:
                    if not msgInfo:
                        msgInfo = (GMDD.data.GUILD_LEARN_GROWTH_NOT_ENOUGH_ITEM, (ID.data.get(itemId, {}).get('name'),))
                else:
                    needMoney += price * (cnt - rcnt)
            else:
                rcnt = cnt
            if needItems.has_key(itemId):
                needItems[itemId] += rcnt
            else:
                needItems[itemId] = rcnt

        return (msgInfo, needItems, needMoney)


def getSubGroupGuildNames(guildNUIDs, guildNames, renameRanks = 0):
    gnum = {}
    renameRanks = renameRanks or len(guildNUIDs)
    if renameRanks:
        for i, x in enumerate(guildNUIDs):
            if i >= renameRanks:
                break
            if not x:
                continue
            guildNUID, subGroupId = x
            if gnum.has_key(guildNUID):
                gnum[guildNUID] += 1
            else:
                gnum[guildNUID] = 1

    guildNames = [ (x, guildNames.get(x[0], '') + gametypes.GUILD_TOURNAMENT_GUILD_SUBGROUP_SUFFIX.get(x[1]) if gnum.get(x[0], 0) > 1 else guildNames.get(x[0], '')) for x in guildNUIDs if x ]
    guildNames = dict(guildNames)
    return guildNames
