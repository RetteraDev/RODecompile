#Embedded file name: /WORKSPACE/data/entities/client/helpers/guild.o
import copy
import BigWorld
import gameglobal
import const
import gametypes
import gamelog
import commGuild
import utils
from commGuild import BaseGuildBuildingMarkerVal, BaseGuildResidentVal, BaseGuildBuildingVal, BaseGuildFactoryVal, GuildResidentPSkillVal, BaseGuildTechnologyVal, BaseGuild, BaseGuildPSkillVal, BaseGuildGrowthVal, BaseGuildPayVal, BaseGuildWSPracticeVal, GuildMergerVal
from userDictType import UserDictType
from callbackHelper import Functor
from guis import uiUtils
from cdata import font_config_data as FCD
from data import guild_config_data as GCD
from data import guild_building_marker_data as GBMD
from data import guild_job_data as GJD
from data import guild_area_data as GARD
from data import guild_technology_data as GTD
from data import guild_level_data as GLD
from data import guild_resident_pskill_data as GRPD
from data import guild_resident_template_data as GRTD
from data import guild_status_stype_data as GSSD
from data import guild_factory_product_data as GFPD
from data import novice_boost_score_type_data as NSTD
from data import guild_run_man_route_data as GRMRD
from cdata import guild_func_prop_def_data as GFNPDD

def _cmpEvent(e1, e2):
    if e1.priority == e2.priority:
        if e1.priority > 1:
            return cmp(e1.tWhen, e2.tWhen)
        else:
            return cmp(e2.tWhen, e1.tWhen)
    else:
        return cmp(e2.priority, e1.priority)


class Building(BaseGuildBuildingVal):

    def __init__(self, nuid = 0, buildingId = 0, level = 0, tEnd = 0, tStart = 0, progress = 0, markerId = 0):
        self.nuid = nuid
        self.buildingId = buildingId
        self.level = level
        self.tEnd = tEnd
        self.tStart = tStart
        self.progress = progress
        self.markerId = markerId

    def addProgress(self, val):
        super(Building, self).addProgress(val)
        gameglobal.rds.ui.guild.refreshCurBuildInfo()
        gameglobal.rds.ui.guildBuildUpgrade.setUpgradeProgress(self.nuid)


class Member(object):

    def __init__(self, gbId = 0, tJoin = 0, contrib = 0, contribTotal = 0, roleId = gametypes.GUILD_ROLE_NORMAL, role = '', school = 0, level = 0, spaceNo = 0, areaId = 0, tLastOnline = 0, box = None, online = False, groupId = 0, luxury = 0, combatScore = 0, wingWorldContri = 0, activityDict = {}):
        self.gbId = gbId
        self.role = role
        self.school = school
        self.level = level
        self.spaceNo = spaceNo
        self.areaId = areaId
        self.groupId = groupId
        self.tJoin = tJoin
        self.roleId = roleId
        self.contrib = contrib
        self.contribTotal = contribTotal
        self.tLastOnline = tLastOnline
        self.online = online
        self.luxury = luxury
        self.combatScore = combatScore
        self.wingWorldContri = wingWorldContri
        self.activityDict = copy.deepcopy(activityDict)

    def fromDTO(self, dto):
        self.gbId, self.role, self.school, self.level, self.spaceNo, self.areaId, self.roleId, self.groupId, self.contrib, self.contribTotal, self.tLastOnline, self.luxury, self.tJoin, self.online, self.combatScore, self.wingWorldContri, self.activityDict = dto
        return self


class Event(object):

    def __init__(self, msgId = 0, args = (), tWhen = 0, priority = 0):
        self.msgId = msgId
        self.args = args
        self.tWhen = tWhen
        self.priority = priority

    def fromDTO(self, dto):
        msgId, args, tWhen, priority = dto
        self.__init__(msgId=msgId, args=args, tWhen=tWhen, priority=priority)
        return self


class GuildSkill(object):

    def __init__(self, skillId = 0, nextTime = 0, duration = 0):
        self.skillId = skillId
        self.nextTime = nextTime
        self.duration = duration


class GuildPSkillVal(BaseGuildPSkillVal):

    def __init__(self, skillId = 0, level = 0, tEnd = 0, tStart = 0):
        super(GuildPSkillVal, self).__init__(skillId, level, tEnd, tStart)
        self.timer = None

    def isUpgrading(self):
        return self.tEnd > 0

    def start(self):
        self.stop()
        self.sendTimerInfo()

    def stop(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None

    def sendTimerInfo(self):
        p = BigWorld.player()
        leftTime = int(self.tEnd - p.getServerTime())
        if leftTime <= 0:
            p.cell.checkGuildResearchPSkill(self.skillId)
            return
        if not gameglobal.rds.ui.guildGrowth.mediator:
            return
        gameglobal.rds.ui.guildGrowth.researchPSkillTimer(self.skillId, self.level + 1, leftTime)
        self.timer = BigWorld.callback(1, self.sendTimerInfo)


class GuildMemberSkill(object):

    def __init__(self, skillId = 0, level = 0, nextTime = 0):
        self.skillId = skillId
        self.level = level
        self.nextTime = nextTime


class GuildGrowthVal(BaseGuildGrowthVal):

    def __init__(self, propertyId = 0, level = 0, active = False):
        super(GuildGrowthVal, self).__init__(propertyId, level, active)


class GuildGrowthVolumn(UserDictType):

    def __init__(self, volumnId = 0, score = 0, enabled = False):
        self.volumnId = volumnId
        self.score = score
        self.enabled = enabled

    def getGrowth(self, propertyId):
        growth = self.get(propertyId)
        if not growth:
            growth = GuildGrowthVal(propertyId=propertyId)
            self[propertyId] = growth
        return growth


class GuildGrowth(UserDictType):

    def __init__(self, dto = None):
        if dto:
            self.fromDTO(dto)

    def getVolumn(self, volumnId):
        volumn = self.get(volumnId)
        if not volumn:
            volumn = GuildGrowthVolumn(volumnId=volumnId)
            self[volumnId] = volumn
        return volumn

    def fromDTO(self, dto):
        for volumnId, score, gdto in dto:
            volumn = self.getVolumn(volumnId)
            volumn.score = score
            for propertyId, level, active in gdto:
                growth = volumn.getGrowth(propertyId)
                growth.level = level
                growth.active = active


class GuildGroupVal(object):

    def __init__(self, groupId = 0, name = '', tWhen = 0, leaderGbId = 0):
        self.groupId = groupId
        self.name = name
        self.tWhen = tWhen
        self.leaderGbId = leaderGbId


class GuildResidentVal(BaseGuildResidentVal):

    def __init__(self, nuid = 0, name = 0, templateId = 0, statusType = 0, statusStype = 0, quality = 0, bpow = 0, bagi = 0, bint = 0, bspr = 0, cpow = 0, cagi = 0, cint = 0, cspr = 0, qpow = 0, qagi = 0, qint = 0, qspr = 0, minqpow = 0, minqagi = 0, minqint = 0, minqspr = 0, maxqpow = 0, maxqagi = 0, maxqint = 0, maxqspr = 0, bindType = 1, blevel = 0, level = 0, exp = 0, expAll = 0, mood = 0, salary = 0, loyalty = 0, savvy = 0, tired = 0, tHire = 0, recommender = 0, jobId = 0, tJob = 0, subJobId = 0, pskills = {}, ability = {}, jobAbility = {}):
        self.nuid = nuid
        self.name = name
        self.templateId = templateId
        self.statusType = statusType
        self.statusStype = statusStype
        self.quality = quality
        self.bpow = bpow
        self.bagi = bagi
        self.bint = bint
        self.bspr = bspr
        self.cpow = cpow
        self.cagi = cagi
        self.cint = cint
        self.cspr = cspr
        self.qpow = qpow
        self.qagi = qagi
        self.qint = qint
        self.qspr = qspr
        self.minqpow = minqpow
        self.minqagi = minqagi
        self.minqint = minqint
        self.minqspr = minqspr
        self.maxqpow = maxqpow
        self.maxqagi = maxqagi
        self.maxqint = maxqint
        self.maxqspr = maxqspr
        self.bindType = bindType
        self.blevel = blevel
        self.level = level
        self.exp = exp
        self.expAll = expAll
        self.mood = mood
        self.salary = salary
        self.loyalty = loyalty
        self.savvy = savvy
        self.tired = tired
        self.tHire = tHire
        self.recommender = recommender
        self.jobId = jobId
        self.tJob = tJob
        self.subJobId = subJobId
        self.pskills = copy.deepcopy(pskills)
        self.ability = copy.deepcopy(ability)
        self.jobAbility = copy.deepcopy(jobAbility)

    def fromDTO(self, dto):
        self.nuid, self.name, self.templateId, self.statusType, self.statusStype, self.cpow, self.cagi, self.cint, self.cspr, self.qpow, self.qagi, self.qint, self.qspr, self.level, self.exp, self.mood, self.salary, self.loyalty, self.savvy, self.tired, self.tHire, self.recommender, self.jobId, self.tJob, self.subJobId, pskills = dto
        for pskill in pskills:
            pskill = GuildResidentPSkillVal().fromDTO(pskill)
            self.pskills[pskill.skillId] = pskill

        return self

    def onAssignJob(self, guild, jobId, tJob):
        marker = commGuild.whereJob(guild, jobId)
        self.jobId = jobId
        self.tJob = tJob
        if marker:
            marker.addWorker(guild, jobId, self.nuid)


class GuildAreaVal(object):

    def __init__(self, areaId = 0, ext = 0, state = 0):
        self.areaId = areaId
        self.ext = ext
        self.state = state

    def fromDTO(self, dto):
        self.areaId, self.ext, self.state = dto
        return self

    def isExtFinished(self):
        if self.state == gametypes.GUILD_AREA_STATE_OPEN:
            return True
        r = self.ext >= GARD.data.get(self.areaId).get('ext')
        if r:
            self.state = gametypes.GUILD_AREA_STATE_OPEN
        return r


class GuildBuildingMarkerVal(BaseGuildBuildingMarkerVal):

    def __init__(self, markerId = 0, buildingNUID = 0, progress = 0, tDev = 0, workers = [], funcWorkers = {}, ability = {}, residentAbility = {}, state = 0):
        super(GuildBuildingMarkerVal, self).__init__(markerId=markerId, buildingNUID=buildingNUID, progress=progress, tDev=tDev, workers=workers, funcWorkers=funcWorkers, state=state)

    def fromDTO(self, dto):
        self.markerId, self.buildingNUID, self.tDev, self.progress, self.state = dto
        return self

    def getStepModelId(self):
        data = GBMD.data.get(self.markerId)
        if data.get('steps'):
            return None
        idx = utils.getListIndex(self.progress, data.get('steps'))
        return data.get('stepModels')[idx]

    def addDevProgress(self, val):
        super(GuildBuildingMarkerVal, self).addDevProgress(val)
        gameglobal.rds.ui.guild.refreshCurBuildInfo()
        gameglobal.rds.ui.guildAssart.setAssartProgress(self.markerId)

    def addProgress(self, guild):
        if self.inDev():
            progress = self.getWorkload(guild, bTired=True, funcType=GFNPDD.data.DEV_EFFICIENCY)
            self.addDevProgress(int(progress))
            if self.isDevFinished():
                self.stopDev(guild, False)
                gameglobal.rds.ui.guildAssart.assartFinish(self.markerId)
                for childMarkerId in GBMD.data.get(self.markerId).get('children', ()):
                    cmarker = guild.marker.get(childMarkerId)
                    cmarker.tDev = self.tDev
                    cmarker.progress = self.progress

                BigWorld.player().onQuestInfoModifiedAtClient(const.QD_GUILD)
        else:
            if self.inBuilding(guild):
                building = guild.building.get(self.buildingNUID)
                progress = self.getWorkload(guild, bTired=True, funcType=GFNPDD.data.BUILDING_EFFICIENCY)
                building.addProgress(int(progress))
                if building.checkFinishUpgrading():
                    BigWorld.player().onGuildBuildingUpgradeFinish(guild.nuid, [(building.nuid, building.level)])
            self.getFuncWorkload(guild, bTired=True)


class GuildFactoryVal(BaseGuildFactoryVal):
    pass


class Guild(BaseGuild):

    def __init__(self, dbID = 0, nuid = 0, spaceNo = 0, tBuild = 0, merit = 0, prosperity = 0, scale = 0, bindCash = 0, mojing = 0, xirang = 0, wood = 0, reserveCash = 0, reserveCoin = 0, reserveBindCash = 0, donateWeekly = 0, tLastDonate = 0, maxMember = 0, hasSpace = False, leaderGbId = 0, leaderRole = '', creatorGbId = 0, creatorRole = '', announcement = '', menifest = '', state = 0, member = {}, event = [], building = {}, shop = [], clanWarFlagMorpher = '', clanWarScore = 0, skills = {}, pskill = {}, growth = GuildGrowth(), tMatchStart = 0, tMatchEnd = 0, matchRound = 0, tMatchRoundEnd = 0, matchScore = 0, matches = {}, group = {}, stability = 0, tMaintainDestroy = 0, vitality = 0, lastActiveNum = 0, recommendedResident = {}, hiredResident = {}, area = {}, marker = {}, factory = {}, technology = {}, otherRes = {}, cancelRes = {}, ability = {}, residentAbility = {}, tutorialStep = {}, activity = {}, guildEnemy = {}, clanEnemy = {}, pkEnemyVer = 0, stats = {}, statsVer = {}, challengeScore = {}, challengeInfo = {}, payroll = {}, enemyGuildNUIDs = set(), enemyClanNUIDs = set(), businessMan = [], options = {}, noviceBoosting = {}, memberShopRefreshCnt = 0, noviceBoosted = {}, noviceBoostVer = -1, kindness = 0, puzzleJoined = False, leaderAutoResignTime = 0, chickenMealScore = 0, fishActivityScore = 0, monsterClanWarScore = 0, guildYMFScore = 0, guildNewFlagScore = 0, signInNum = 0, prestige = 0, guildDonateWeeklyNum = 0):
        self.dbID = dbID
        self.nuid = nuid
        self.spaceNo = spaceNo
        self.tBuild = tBuild
        self.merit = merit
        self.bindCash = bindCash
        self.mojing = mojing
        self.xirang = xirang
        self.wood = wood
        self.reserveCash = reserveCash
        self.reserveCoin = reserveCoin
        self.reserveBindCash = reserveBindCash
        self.prosperity = prosperity
        self.scale = scale
        self.donateWeekly = donateWeekly
        self.tLastDonate = tLastDonate
        self.maxMember = maxMember
        self.hasSpace = hasSpace
        self.state = state
        self.leaderGbId = leaderGbId
        self.leaderRole = leaderRole
        self.creatorGbId = creatorGbId
        self.creatorRole = creatorRole
        self.member = copy.deepcopy(member)
        self.event = copy.deepcopy(event)
        self.building = copy.deepcopy(building)
        self.shop = copy.deepcopy(shop)
        self.skills = copy.deepcopy(skills)
        self.pskill = copy.deepcopy(pskill)
        self.growth = copy.deepcopy(growth)
        self.clanWarFlagMorpher = clanWarFlagMorpher
        self.clanWarScore = clanWarScore
        self.tMatchStart = tMatchStart
        self.tMatchEnd = tMatchEnd
        self.matchRound = matchRound
        self.tMatchRoundEnd = tMatchRoundEnd
        self.matchScore = matchScore
        self.matches = copy.deepcopy(matches)
        self.group = copy.deepcopy(group)
        self.stability = stability
        self.tMaintainDestroy = tMaintainDestroy
        self.vitality = vitality
        self.lastActiveNum = lastActiveNum
        self.recommendedResident = copy.deepcopy(recommendedResident)
        self.hiredResident = copy.deepcopy(hiredResident)
        self.area = copy.deepcopy(area)
        self.marker = copy.deepcopy(marker)
        self.factory = copy.deepcopy(factory)
        self.technology = copy.deepcopy(technology)
        self.otherRes = copy.deepcopy(otherRes)
        self.cancelRes = copy.deepcopy(cancelRes)
        self.ability = copy.deepcopy(ability)
        self.residentAbility = copy.deepcopy(residentAbility)
        self.tutorialStep = copy.deepcopy(tutorialStep)
        self.activity = copy.deepcopy(activity)
        self.guildEnemy = copy.deepcopy(guildEnemy)
        self.clanEnemy = copy.deepcopy(clanEnemy)
        self.enemyGuildNUIDs = copy.deepcopy(enemyGuildNUIDs)
        self.enemyClanNUIDs = copy.deepcopy(enemyClanNUIDs)
        self.pkEnemyVer = pkEnemyVer
        self.stats = copy.deepcopy(stats)
        self.statsVer = copy.deepcopy(statsVer)
        self.challengeScore = copy.copy(challengeScore)
        self.challengeInfo = copy.deepcopy(challengeInfo)
        self.payroll = copy.deepcopy(payroll)
        self.businessMan = copy.deepcopy(businessMan)
        self.options = copy.deepcopy(options)
        self.noviceBoosting = copy.deepcopy(noviceBoosting)
        self.noviceBoosted = copy.deepcopy(noviceBoosted)
        self.noviceBoostVer = noviceBoostVer
        self.memberShopRefreshCnt = memberShopRefreshCnt
        self.kindness = kindness
        self.announcement = announcement
        self.menifest = menifest
        self.puzzleJoined = puzzleJoined
        self.setFlag()
        self.leaderAutoResignTime = leaderAutoResignTime
        self.chickenMealScore = chickenMealScore
        self.fishActivityScore = fishActivityScore
        self.monsterClanWarScore = monsterClanWarScore
        self.guildYMFScore = guildYMFScore
        self.guildNewFlagScore = guildNewFlagScore
        self.bonfire = GuildBonfire()
        self.redPacket = GuildRedPacket()
        self.signInNum = signInNum
        self.prestige = prestige
        self.guildMergerVal = GuildMergerVal()
        self.guildDonateWeeklyNum = guildDonateWeeklyNum

    def addEvent(self, event):
        if self.event != None:
            self.event.append(event)

    def sortEvent(self):
        self.event.sort(cmp=_cmpEvent)

    def addMember(self, gbId, member):
        if self.member != None:
            self.member[gbId] = member

    def delMember(self, gbId):
        if self.member != None:
            self.member.pop(gbId, None)

    def setFlag(self):
        try:
            config = eval(self.clanWarFlagMorpher)
            self.flag = config.get(2, '')
        except:
            gamelog.error('zt: cannot eval config', self.clanWarFlagMorpher)

    def isResInDebt(self):
        return self.mojing < 0 or self.xirang < 0 or self.wood < 0 or self.bindCash < 0

    def updateReserveRes(self, reserveRes):
        self.reserveCash, self.reserveCoin, self.reserveBindCash = reserveRes

    def updateRes(self, res):
        inDebt = self.isResInDebt()
        bindCash, mojing, xirang, wood = res
        self.bindCash = bindCash
        self.mojing = mojing
        self.xirang = xirang
        self.wood = wood
        gameglobal.rds.ui.topBar.setValueByName('guildCash')
        gameglobal.rds.ui.topBar.setValueByName('guildWood')
        gameglobal.rds.ui.topBar.setValueByName('guildMojing')
        gameglobal.rds.ui.topBar.setValueByName('guildXirang')
        if self.state == gametypes.GUILD_STATE_ACTIVE:
            if not self.isResInDebt():
                self.tMaintainDestroy = 0
            elif not inDebt:
                self.tMaintainDestroy = utils.getNow() + GCD.data.get('maintainDestroyTime', const.GUILD_MAINTAIN_DESTROY_TIME)
        self.refreshRes()

    def refreshRes(self):
        gameglobal.rds.ui.guild.refreshResourceInfo()
        gameglobal.rds.ui.guildStorage.refreshResourceInfo()
        gameglobal.rds.ui.guildFactory.refreshResourceInfo()

    def getPuzzleRoundNum(self):
        activity = self._getActivity(gametypes.GUILD_ACTIVITY_PUZZLE)
        return activity and activity.data.get(commGuild.ACTIVITY_ATTR_ROUND_NUM, 0) or 0

    def getPuzzleDesc(self):
        activity = self._getActivity(gametypes.GUILD_ACTIVITY_PUZZLE)
        return activity and activity.data.get(commGuild.ACTIVITY_ATTR_PUZZLE_DESC, '') or ''

    def getPuzzleAnswer(self):
        activity = self.activity.get(gametypes.GUILD_ACTIVITY_PUZZLE)
        return activity and activity.data.get(commGuild.ACTIVITY_ATTR_PUZZLE_ANSWER, '') or ''

    def getPuzzleLeftTime(self):
        activity = self.activity.get(gametypes.GUILD_ACTIVITY_PUZZLE)
        if activity is None:
            return 0
        return max(0, activity.nextTime - utils.getNow())

    def getPuzzleState(self):
        activity = self.activity.get(gametypes.GUILD_ACTIVITY_PUZZLE)
        return activity and activity.state or 0

    def getPuzzleTops(self, bVoice):
        activity = self.activity.get(gametypes.GUILD_ACTIVITY_PUZZLE)
        if activity is None:
            return []
        else:
            topNames = activity.data.get(commGuild.ACTIVITY_ATTR_TOP_NAMES)
            if not topNames:
                return []
            return topNames[bVoice]

    def getShop(self, shopType):
        return self.shop[shopType - 1]

    def updateShop(self, data):
        version, shopType, posCountDict, tNextRefresh, tLastForceRefresh, invData = data
        shop = self.getShop(shopType)
        shop.cleanPages()
        shop.version = version
        shop.posCountDict = posCountDict
        shop.tNextRefresh = tNextRefresh
        shop.tLastForceRefresh = tLastForceRefresh
        for pg, ps, item in invData:
            if hasattr(item, 'remainNum'):
                item.cwrap = item.remainNum
            shop.setQuickVal(item, pg, ps)

    def getPSkill(self, pskillId):
        pskill = self.pskill.get(pskillId)
        if not pskill:
            pskill = GuildPSkillVal(skillId=pskillId)
            self.pskill[pskillId] = pskill
        return pskill

    def getGrowthVolumn(self, volumnId):
        volumn = self.growth.get(volumnId)
        if not volumn:
            volumn = GuildGrowthVolumn(volumnId=volumnId)
            volumn.enabled = commGuild.isGuildGrowthVolumnActivated(BigWorld.player(), volumnId, bldLv=self.getBuildingLevelById(gametypes.GUILD_BUILDING_GROWTH_ID))
            self.growth[volumnId] = volumn
        return volumn

    def getBuildingById(self, buildingId, bMaxLevel = False):
        tBuilding = None
        for building in self.building.itervalues():
            if building.buildingId == buildingId:
                if not bMaxLevel:
                    return building
                if not tBuilding or building.level > tBuilding.level:
                    tBuilding = building

        return tBuilding

    def getBuildingByMarkerId(self, markerId):
        for building in self.building.itervalues():
            if building.markerId == markerId:
                return building

    def _getFactory(self, tp):
        if tp not in gametypes.GUILD_FACTORY_TYPE:
            return None
        factory = self.factory.get(tp)
        if not factory:
            factory = GuildFactoryVal(type=tp)
            self.factory[tp] = factory
        return factory

    def doCheckPoint(self):
        p = BigWorld.player()
        for marker in self.marker.itervalues():
            marker.addProgress(self)
            managers = marker.getManagers(self)
            for manager in managers:
                manager.getWorkload(bTired=True)

        for techId, technology in self.technology.iteritems():
            if technology.inResearching():
                manager = technology.getManager(self)
                if not manager:
                    continue
                tdata = GTD.data.get(techId)
                pskillId = tdata.get('pskillId')
                if pskillId and not manager.pskills.has_key(pskillId):
                    continue
                progress = manager.getTechWorkload(self, techId, bTired=True)
                technology.addProgress(progress)
                if technology.checkFinishResearch():
                    p.onGuildResearchTechnologyFinish(self.nuid, techId)

        for resident in self.hiredResident.itervalues():
            resident.onRest()

    def getAvailJobList(self):
        r = []
        for jobId, jdata in GJD.data.iteritems():
            placeType, placeId = jdata.get('placeType'), jdata.get('placeId')
            if placeType == gametypes.GUILD_JOB_PLACE_MARKER:
                marker = self.marker.get(placeId)
                jobType = jdata.get('type', 0)
                if jobType == gametypes.GUILD_JOB_TYPE_DEV:
                    if marker.inDev():
                        if jdata.get('difficulty', 0) == gametypes.GUILD_JOB_DIFFICULTY_NORMAL:
                            r.append((jobId, marker.getDevWorkerLimit(), len(marker.workers)))
                        else:
                            r.append((jobId, 1, 1 if marker.getManager(self, type=gametypes.GUILD_JOB_TYPE_DEV) else 0))
                elif jobType == gametypes.GUILD_JOB_TYPE_UPGRADE:
                    if marker.inBuilding(self):
                        if jdata.get('difficulty', 0) == gametypes.GUILD_JOB_DIFFICULTY_NORMAL:
                            r.append((jobId, marker.getBuildingWorkerLimit(self), len(marker.workers)))
                        else:
                            r.append((jobId, 1, 1 if marker.getManager(self, type=gametypes.GUILD_JOB_TYPE_UPGRADE) else 0))
                elif jobType == gametypes.GUILD_JOB_TYPE_FUNC:
                    building = marker.getBuilding(self)
                    if building and building.exist():
                        r.append((jobId, jdata.get('workerLimit')[building.level - 1], marker.getFuncWorkerCount(jobId)))

        return r

    def isBuildingFinished(self, markerId):
        building = self.marker.get(markerId).getBuilding(self)
        return building and building.tStart == 0

    def isDevFinished(self, markerId):
        return self.marker.get(markerId).isDevFinished()

    def isAreaExtFinished(self, areaId):
        return self.area.get(areaId).isExtFinished()

    def inSpace(self, owner):
        return owner.spaceNo == self.spaceNo

    def _getMaxMojing(self):
        if gameglobal.rds.configData.get('enableNewGuild'):
            return super(Guild, self)._getMaxMojing()
        else:
            return const.GUILD_RES_MAX

    def _getMaxXirang(self):
        if gameglobal.rds.configData.get('enableNewGuild'):
            return super(Guild, self)._getMaxXirang()
        else:
            return const.GUILD_RES_MAX

    def _getMaxWood(self):
        if gameglobal.rds.configData.get('enableNewGuild'):
            return super(Guild, self)._getMaxWood()
        else:
            return const.GUILD_RES_MAX

    def _getMaxBindCash(self):
        if gameglobal.rds.configData.get('enableNewGuild'):
            return super(Guild, self)._getMaxBindCash()
        else:
            return const.GUILD_RES_MAX

    def _getMaxMember(self, delta = 0):
        if gameglobal.rds.configData.get('enableNewGuild'):
            return super(Guild, self)._getMaxMember(delta)
        else:
            data = GLD.data.get(self.level)
            if not data:
                return 0
            maxMemberEx = data.get('maxMemberEx')
            if maxMemberEx:
                hostId = gameglobal.rds.g_serverid
                if maxMemberEx.has_key(hostId):
                    return maxMemberEx.get(hostId)
            return data.get('maxMember')

    def getTutorialStepIds(self):
        stepIds = []
        p = BigWorld.player()
        for stepId in self.tutorialStep.iterkeys():
            data = getGTSD().data.get(stepId, {})
            visibleType = data.get('visibleType')
            if visibleType == gametypes.GUILD_TUTORIAL_VISIBLE_NOT:
                continue
            elif visibleType == gametypes.GUILD_TUTORIAL_VISIBLE_SCENE:
                if not p.inGuildSpace():
                    continue
            targetType = data.get('targetType')
            if targetType == gametypes.GUILD_TUTORIAL_TARGET_LEADER:
                if not p.gbId == self.leaderGbId:
                    continue
            elif targetType == gametypes.GUILD_TUTORIAL_TARGET_MGR:
                if not gametypes.GUILD_PRIVILEGES.get(self.memberMe.roleId, {}).get('bMgr'):
                    continue
            stepIds.append(stepId)

        return stepIds

    def getTutorialStepProgress(self, stepId):
        step = self.tutorialStep.get(stepId)
        if not step:
            return 0
        return step.progress

    def resetPayrollCache(self):
        for payroll in self.payroll.itervalues():
            for group in payroll.group.itervalues():
                group.payments = None

    def getSelfContrib(self):
        p = BigWorld.player()
        if not self.member.has_key(p.gbId):
            return 0
        return self.member[p.gbId].contrib

    def getRedPacket(self, sn):
        v = self.redPacket.get(sn)
        if not v:
            v = GuildRedPacketVal(sn=sn)
            self.redPacket[sn] = v
        return v

    def hasRedPacket(self, sn):
        v = self.redPacket.get(sn)
        if not v:
            return False
        return True


class GuildList(object):

    def __init__(self, state):
        self.state = state
        self.sortBy = gametypes.GUILD_ORDER_BY_LEVEL
        self.orderType = 1
        self.historyOrderType = {}
        self.guild = []
        self.curPage = 0
        self.totalPages = 1

    def setSearchSortBy(self, sortBy, orderType = None):
        if sortBy == self.sortBy:
            if orderType == None:
                self.orderType = 1 - self.orderType
            else:
                self.orderType = orderType
            self.historyOrderType[sortBy] = self.orderType
        else:
            if orderType == None:
                orderType = self.historyOrderType.get(sortBy)
                if not orderType:
                    orderType = 1
            else:
                orderType = orderType
            self.sortBy = sortBy
            self.orderType = orderType
            self.historyOrderType[sortBy] = self.orderType

    def prevPage(self):
        if self.page == 0:
            return
        self.queryGuildList(self.page - 1)

    def nextPage(self):
        if self.page >= self.totalPages - 1:
            return
        self.queryGuildList(self.page + 1)

    def queryGuildList(self, page = None):
        if page == None:
            page = self.curPage
        p = BigWorld.player()
        p.base.queryGuildList(page, self.state, self.sortBy, self.orderType)

    def setData(self, totalPages, page, guild):
        self.page = page
        self.totalPages = totalPages
        self.guild = guild


class GuildTechnologyVal(BaseGuildTechnologyVal):

    def __init__(self, techId = 0, state = 0, progress = 0):
        super(GuildTechnologyVal, self).__init__(techId=techId, state=state, progress=progress)

    def addProgress(self, val):
        super(GuildTechnologyVal, self).addProgress(val)
        gameglobal.rds.ui.guild.refreshSingleTechnologyInfo(self.techId, False)
        gameglobal.rds.ui.guildTechResearch.refreshInfo(self.techId)


class GuildPayVal(BaseGuildPayVal):

    def __init__(self, nuid = 0, gbId = 0, amount = 0, tWhen = 0, tExpire = 0, tPaid = 0, mtype = 0, salaryType = 0):
        super(GuildPayVal, self).__init__(nuid=nuid, gbId=gbId, amount=amount, tWhen=tWhen, tExpire=tExpire, tPaid=tPaid, salaryType=salaryType)
        self.mtype = mtype

    def fromDTO(self, dto):
        self.mtype, self.nuid, self.amount, self.tWhen, self.tExpire, self.tPaid, self.salaryType = dto
        return self


class GuildPayGroupVal(object):

    def __init__(self, serialNUID = 0, tWhen = 0, tExpire = 0, payments = None):
        self.serialNUID = serialNUID
        self.tWhen = tWhen
        self.tExpire = tExpire
        self.payments = payments

    def fromDTO(self, dto):
        self.serialNUID, self.tWhen, self.tExpire = dto
        return self


class GuildPayrollVal(object):

    def __init__(self, mtype = 0, salaryTotal = 0, settings = {}, group = {}, ver = 0, groupVer = 0):
        self.mtype = mtype
        self.salaryTotal = salaryTotal
        self.settings = copy.deepcopy(settings)
        self.group = copy.deepcopy(group)
        self.ver = ver
        self.groupVer = groupVer

    def getEarliestGroup(self):
        group = None
        for _group in self.group.itervalues():
            if group == None:
                group = _group
            elif _group.tWhen < group.tWhen:
                group = _group

        return group


class GuildWSPracticeVal(BaseGuildWSPracticeVal):
    pass


class GuildNoviceBoostVal(object):

    def __init__(self, gbId = 0, name = '', actId = 0, bPerfect = False, tWhen = 0, state = 0):
        self.gbId = gbId
        self.name = name
        self.actId = actId
        self.bPerfect = bPerfect
        self.tWhen = tWhen
        self.state = state

    def fromDTO(self, dto):
        self.gbId, self.name, self.actId, self.tWhen, self.state, self.bPerfect = dto
        return self

    def getBonusId(self):
        return NSTD.data.get(self.actId, {}).get(self.bPerfect and 'fineGuildBonusId' or 'guildBonusId', 0)


class RunManPlayerMarkerVal(commGuild.RunManPlayerMarkerVal):

    def fromDTO(self, dto):
        self.passed, self.passNum = dto
        return self


class RunManPlayerRouteVal(commGuild.RunManPlayerRouteVal):

    def fromDTO(self, dto):
        for idx, mdto in dto:
            mVal = RunManPlayerMarkerVal().fromDTO(mdto)
            self[idx] = mVal

        return self

    def getMarker(self, num):
        mVal = self.get(num)
        if mVal == None:
            mVal = RunManPlayerMarkerVal()
            self[num] = mVal
        return mVal

    def _close(self):
        self.state = gametypes.GUILD_RUN_MAN_STATE_CLOSED
        self.currNum = 0


class RunManPlayerRoute(commGuild.RunManPlayerRoute):

    def getRoute(self, runManType):
        route = self.get(runManType)
        if route == None:
            route = RunManPlayerRouteVal(runManType=runManType)
            for rtype, idx in GRMRD.data.iterkeys():
                if rtype == runManType:
                    route[idx] = RunManPlayerMarkerVal()

            self[runManType] = route
        return route

    def fromDTO(self, dto):
        for runManType, passNum, rdto in dto:
            route = RunManPlayerRouteVal(runManType=runManType, passNum=passNum).fromDTO(rdto)
            self[runManType] = route


class GuildBonfire(object):

    def __init__(self, endTime = 0):
        self.endTime = endTime
        self.torch = {}

    def fromDTO(self, dto):
        self.endTime, d = dto
        self.torch.clear()
        for idx, name in d:
            self.torch[idx] = name

    def finish(self):
        self.endTime = utils.getNow()

    def isOpening(self):
        startTime = self.endTime - GCD.data.get('bonfireDuration', 600) - 10
        return startTime < utils.getNow() < self.endTime

    def isTorchOn(self, idx):
        return self.torch.get(idx, False)


class GuildRedPacket(commGuild.GuildRedPacket):

    def fromDTO(self, dto):
        self.signInRedPacket, self.sendEndTime = dto
        return self


class GuildRedPacketVal(commGuild.GuildRedPacketVal):

    def __init__(self, sn = 0, received = 0):
        super(GuildRedPacketVal, self).__init__(sn=sn)
        self.received = received


def getPhotoPath40(icon):
    return 'guildResident/unitType/40/%d.dds' % icon


def getPhotoPath96(icon):
    return 'guildResident/unitType/96/%d.dds' % icon


def getStatusStypePath20(icon):
    return 'guildResident/statusStype/20/%d.dds' % icon


def getStatusStypePath32(icon):
    return 'guildResident/statusStype/32/%d.dds' % icon


def getResidentSkillPath40(icon):
    return 'guildResidentSkill/40/%d.dds' % icon


def getResidentSkillPath64(icon):
    return 'guildResidentSkill/64/%d.dds' % icon


def getStatusField(statusType, statusStype, useShort):
    statusField = gametypes.GUILD_RESIDENT_STATUS_NAME.get(statusType, '')
    if statusStype == gametypes.GUILD_RESIDENT_STATUS_GIANT:
        if useShort:
            statusField = GSSD.data.get(statusStype, {}).get('name', '')
        else:
            statusField += '-' + GSSD.data.get(statusStype, {}).get('name', '')
    return statusField


def getResidentQuality(templateId):
    quality = GRTD.data.get(templateId, {}).get('quality', 0)
    return (quality, FCD.data.get(('item', quality + 1), {}).get('qualitycolor', 'nothing'))


def createResidentInfo(guild, residentNUID, size = const.GUILD_RESIDENT_SIZE40):
    resident = guild.hiredResident.get(residentNUID)
    residentInfo = {}
    residentInfo['residentNUID'] = str(residentNUID)
    if size == const.GUILD_RESIDENT_SIZE40:
        residentInfo['iconPath'] = getPhotoPath40(GRTD.data.get(resident.templateId, {}).get('icon', 0))
        residentInfo['statusStype'] = getStatusStypePath20(resident.statusStype)
    else:
        residentInfo['iconPath'] = getPhotoPath96(GRTD.data.get(resident.templateId, {}).get('icon', 0))
        residentInfo['statusStype'] = getStatusStypePath32(resident.statusStype)
    residentInfo['quality'], residentInfo['qualitycolor'] = getResidentQuality(resident.templateId)
    residentInfo['statusField'] = getStatusField(resident.statusType, resident.statusStype, False)
    residentInfo['tiredLv'] = 'lv%d' % commGuild.getTiredType(resident.tired)
    residentInfo['tiredValue'] = resident.tired
    residentInfo['isWorking'] = resident.subJobId != 0
    return residentInfo


def addManagerInfo(guild, residentNUID, residentInfo, jobId):
    resident = guild.hiredResident.get(residentNUID)
    residentInfo['nameField'] = resident.name
    residentInfo['levelField'] = resident.level
    addSkillInfo(guild, residentNUID, residentInfo, jobId)


def addSkillInfo(guild, residentNUID, residentInfo, jobId):
    resident = guild.hiredResident.get(residentNUID)
    skills = []
    if resident.pskills:
        for pskill in resident.pskills.itervalues():
            skillInfo = createResidentSkillInfo(pskill.skillId, pskill.level, jobId=jobId)
            if skillInfo:
                skills.append(skillInfo)

    skills.sort(cmp=sort_by_statusType)
    residentInfo['skills'] = skills


def sort_by_statusType(a, b):
    if a['statusType'] == b['statusType']:
        return a['skillId'] - b['skillId']
    return b['statusType'] - a['statusType']


def getDescFromType(desc, descType, value, divisor):
    if descType == 1:
        desc = desc.replace('%s', str(int(value)), 1)
    elif descType == 2:
        if divisor != 0:
            value *= divisor
        desc = desc.replace('%s', format(value, '.1%'), 1)
    elif descType == 3:
        desc = desc.replace('%s', format(value, '.2f'), 1)
    return desc


def getResidentSkillDesc(skillInfo, resident):
    descType = skillInfo.get('descType', 0)
    desc = skillInfo.get('desc', '')
    divisor = skillInfo.get('divisor', 0)
    if descType == 0:
        return desc
    for fparams in skillInfo.get('funcs'):
        fv = None
        if len(fparams) == 4:
            aid, buildingId, v, fv = fparams
        else:
            aid, buildingId, v = fparams
        rv = v
        if not rv:
            if not resident:
                continue
            dp = {'cpow': resident.cpow,
             'cagi': resident.cagi,
             'cint': resident.cint,
             'cspr': resident.cspr}
            rv = fv and fv(dp) or 0
            if rv == dp:
                continue
            desc = getDescFromType(desc, descType, rv, divisor)
        elif isinstance(rv, dict):
            if not resident:
                continue
            if not rv.values()[0] and fv:
                dp = {'cpow': resident.cpow,
                 'cagi': resident.cagi,
                 'cint': resident.cint,
                 'cspr': resident.cspr}
                tv = fv(dp)
                if tv == dp:
                    continue
                desc = getDescFromType(desc, descType, tv, divisor)

    return desc


def createResidentSkillInfo(skillId, lv, isTips = False, resident = None, jobId = 0):
    skillInfo = {}
    baseInfo = GRPD.data.get((skillId, lv), {})
    if jobId:
        for val in baseInfo.get('jobId', ()):
            if val == jobId:
                break
        else:
            return None

    skillInfo['skillId'] = skillId
    skillInfo['skillLv'] = lv
    skillInfo['skillName'] = baseInfo.get('name', '')
    skillInfo['statusType'] = baseInfo.get('statusType', 0)
    if isTips:
        skillInfo['statusStypeCN'] = '%s技能' % gametypes.GUILD_RESIDENT_STATUS_NAME.get(baseInfo.get('statusType', 0), '居民')
        skillInfo['skillType'] = '被动技能'
        skillInfo['propType'] = '%s系' % gametypes.GUILD_RESIDENT_PROP_NAME.get(baseInfo.get('propType', 0), '通用')
        skillInfo['reqLv'] = baseInfo.get('reqLv', '')
        skillInfo['iconPath'] = getResidentSkillPath64(baseInfo.get('icon', 0))
        mainEff = getResidentSkillDesc(baseInfo, resident)
        nextLvInfo = GRPD.data.get((skillId, lv + 1), {})
        if nextLvInfo != {}:
            mainEff += '<br><br>下一等级：<br>%s' % getResidentSkillDesc(nextLvInfo, resident)
        else:
            mainEff += '<br><br>已达到最高级'
        skillInfo['mainEff'] = mainEff
    else:
        skillInfo['iconPath'] = getResidentSkillPath40(baseInfo.get('icon', 0))
    return skillInfo


def dispatchCheck(residentNUID, jobId):
    p = BigWorld.player()
    guild = p.guild
    if not guild:
        return
    resident = guild.hiredResident.get(residentNUID)
    if resident.subJobId:
        marker = commGuild.whereJob(guild, resident.jobId)
        if not marker:
            return
        buildValue = guild.building.get(marker.buildingNUID) if marker.buildingNUID else None
        if not buildValue:
            return
        if buildValue.buildingId == gametypes.GUILD_BUILDING_FACTORY_MACHINE_ID:
            selectType = gametypes.GUILD_FACTORY_PRODUCT_MACHINE
        elif buildValue.buildingId == gametypes.GUILD_BUILDING_FACTORY_FACILITY_ID:
            selectType = gametypes.GUILD_FACTORY_PRODUCT_FACILITY
        else:
            return
        factory = guild._getFactory(selectType)
        taskVal = factory.task.get(resident.subJobId, {})
        if not taskVal:
            return
        itemId = GFPD.data.get(taskVal.productId, {}).get('itemId', 0)
        msg = '该居民正在%s生产%s，确定改派该工作？' % (commGuild.getBuildNameByJobId(guild, resident.jobId), uiUtils.getItemColorName(itemId))
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.assignGuildJob, residentNUID, jobId))
    else:
        p.cell.assignGuildJob(residentNUID, jobId)


def stopWorkCheck(residentNUID):
    p = BigWorld.player()
    guild = p.guild
    if not guild:
        return
    resident = guild.hiredResident.get(residentNUID)
    if resident.subJobId:
        marker = commGuild.whereJob(guild, resident.jobId)
        if not marker:
            return
        buildValue = guild.building.get(marker.buildingNUID) if marker.buildingNUID else None
        if not buildValue:
            return
        if buildValue.buildingId == gametypes.GUILD_BUILDING_FACTORY_MACHINE_ID:
            selectType = gametypes.GUILD_FACTORY_PRODUCT_MACHINE
        elif buildValue.buildingId == gametypes.GUILD_BUILDING_FACTORY_FACILITY_ID:
            selectType = gametypes.GUILD_FACTORY_PRODUCT_FACILITY
        else:
            return
        factory = guild._getFactory(selectType)
        taskVal = factory.task.get(resident.subJobId, {})
        if not taskVal:
            return
        itemId = GFPD.data.get(taskVal.productId, {}).get('itemId', 0)
        msg = '该居民正在%s生产%s，确定休息？' % (commGuild.getBuildNameByJobId(guild, resident.jobId), uiUtils.getItemColorName(itemId))
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(p.cell.stopGuildWork, residentNUID))
    else:
        p.cell.stopGuildWork(residentNUID)


def getGTSD():
    if gameglobal.rds.configData.get('enableGuildTutorialNew'):
        from data import guild_new_tutorial_step_data as GTSD
        return GTSD
    else:
        from data import guild_tutorial_step_data as GTSD
        return GTSD


def getGTNSD():
    if gameglobal.rds.configData.get('enableWWGuildTournament'):
        from data import guild_wwtournament_schedule_data as GTSD
        return GTSD
    else:
        from data import guild_tournament_schedule_data as GTSD
        return GTSD


def getGuildTopRewardInfo(tData, rank):
    for td in tData:
        minRank, maxRank = td['rankRange']
        if not minRank <= rank <= maxRank:
            continue
        progressBonusIds = td.get('progressBonusIds', ())
        bonusIdList = [ bonusId for bonusId, eventId in progressBonusIds if not eventId or BigWorld.player().isServerProgressFinished(eventId) ]
        return (bonusIdList[:1], [td.get('guildFame', 0),
          td.get('guildCash', 0),
          td.get('guildWood', 0),
          td.get('guildCrystal', 0),
          td.get('guildIron', 0)])

    return ([], [0,
      0,
      0,
      0,
      0])
