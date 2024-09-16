#Embedded file name: I:/bag/tmp/tw2/res/entities\common/commonWorldWar.o
import copy
import const
import gametypes
import utils
import gamelog
import BigWorld
from userSoleType import UserSoleType
from userDictType import UserDictType
from data import world_war_config_data as WWCD
from data import world_war_fort_data as WWFD
from data import world_war_battle_task_target_data as WWBTTD
from data import world_war_battle_task_data as WWBTD
from data import world_war_battle_reward_data as WWBRD
from data import world_war_army_data as WWAD
if BigWorld.component != 'client':
    import gameconfig
else:
    import gameglobal

def getEnemyCamp(camp):
    if not camp:
        return 0
    elif camp == gametypes.WORLD_WAR_CAMP_ATTACK:
        return gametypes.WORLD_WAR_CAMP_DEFEND
    else:
        return gametypes.WORLD_WAR_CAMP_ATTACK


def getCurrCampOfDate(camp):
    if utils.getWeekInt() % 2 == 0:
        return camp
    else:
        return getEnemyCamp(camp)


def calcQuestStarLv(score1, score2):
    starLv = getQuestStarLv(abs(score1 - score2))
    if score1 > score2:
        return (const.WORLD_WAR_MAX_QUEST_STAR_LV, starLv)
    else:
        return (starLv, const.WORLD_WAR_MAX_QUEST_STAR_LV)


def getQuestStarLv(diff):
    diffs = WWCD.data.get('combatScoreDiffForQuestStar', ())
    for i, v in enumerate(diffs):
        if diff <= v:
            return const.WORLD_WAR_MAX_QUEST_STAR_LV - i

    return 1


def judgeRecord(rtype, c1, c2):
    s1 = c1.record.get(rtype, 0)
    s2 = c2.record.get(rtype, 0)
    if s1 + s2 <= 0:
        return (0, 0)
    else:
        if BigWorld.component == 'client' and gameglobal.rds.configData.get('enableWorldWarYoungGroup', False):
            param = WWCD.data.get('judgeParamNew', {}).get(rtype, 1)
        elif BigWorld.component in ('base', 'cell') and gameconfig.enableWorldWarYoungGroup():
            param = WWCD.data.get('judgeParamNew', {}).get(rtype, 1)
        else:
            param = WWCD.data.get('judgeParam', {}).get(rtype, 1)
        if rtype == gametypes.WORLD_WAR_RECORD_KILL_BOSS:
            return (int(param * s1), int(param * s2))
        if s1 > s2:
            r2 = int(param * s2 * 1.0 / (s1 + s2))
            return (param - r2, r2)
        r1 = int(param * s1 * 1.0 / (s1 + s2))
        return (r1, param - r1)


def calcResult(s1, s2):
    if s1 > s2:
        return const.WIN
    else:
        return const.LOSE


def judge(c1, c2):
    s1 = 0
    s2 = 0
    for rtype in gametypes.WORLD_WAR_RECORD_JUDGE_TYPES:
        ts1, ts2 = judgeRecord(rtype, c1, c2)
        s1 += ts1
        s2 += ts2

    return (s1, s2)


def _calcMoraleIdx(c1, c2):
    if WWCD.data.get('moraleReverse'):
        c2, c1 = c1, c2
    if not c1 or not c2:
        return -1
    elif not c1.lastMorale and not c2.lastMorale:
        return -1
    elif c1.lastMorale == c2.lastMorale:
        return -1
    elif c1.lastMorale < c2.lastMorale:
        return -1
    else:
        params = WWCD.data.get('moraleEffect')
        if not params:
            return -1
        elif not c2.lastMorale:
            return len(params) - 1
        t = c1.lastMorale * 1.0 / c2.lastMorale
        r = -1
        for i, (v1, _, _) in enumerate(params):
            if t >= v1:
                r = i
            else:
                break

        return r


def calcMoraleEffect(c1, c2):
    idx = _calcMoraleIdx(c1, c2)
    if idx < 0:
        return 0
    params = WWCD.data.get('moraleEffect')
    _, v2, _ = params[idx]
    return v2


def calcMoraleStateId(c1, c2):
    idx = _calcMoraleIdx(c1, c2)
    if idx < 0:
        return 0
    params = WWCD.data.get('moraleEffect')
    _, _, stateId = params[idx]
    return stateId


def calcBattleRes(c1, c2):
    res = WWCD.data.get('initBattleRes', 10000)
    s = c1.lastRes + c2.lastRes
    r = s == 0 and 0.5 or c1.lastRes * 1.0 / s
    r1 = int(r * res)
    return (r1, res - r1)


def getMonthId():
    return utils.getMonthSecond(utils.getWeekSecond())


def inBloodWeek(bloodWeekId):
    return utils.getWeekSecond() == bloodWeekId


class BaseCountryVal(UserSoleType):

    def __init__(self, hostId = 0, groupId = 0, combatScore = 0, declarePoint = 0, bidDeclarePoint = 0, enemyHostId = 0, camp = 0, currCamp = 0, intentTargets = [], applyIdx = 0, luckyWeekId = 0, score = 0, lastScore = 0, gradeScore = 0, gradeScoreDelta = 0, conquerScore = 0, starLv = 0, winNum = 0, battleRes = 0, lastRes = 0, lastMorale = 0, battleScore = 0, battleRewardId = 0, battleTaskRewardId = 0, mp = 0, bfHostId = 0, record = {}, monthRecord = {}):
        self.hostId = hostId
        self.groupId = groupId
        self.combatScore = combatScore
        self.declarePoint = declarePoint
        self.bidDeclarePoint = bidDeclarePoint
        self.enemyHostId = enemyHostId
        self.camp = camp
        self.currCamp = currCamp
        self.intentTargets = copy.deepcopy(intentTargets)
        self.applyIdx = applyIdx
        self.luckyWeekId = luckyWeekId
        self.starLv = starLv
        self.score = score
        self.lastScore = lastScore
        self.gradeScore = gradeScore
        self.gradeScoreDelta = gradeScoreDelta
        self.record = copy.deepcopy(record)
        self.winNum = winNum
        self.battleRes = battleRes
        self.lastRes = lastRes
        self.lastMorale = lastMorale
        self.conquerScore = conquerScore
        self.battleScore = battleScore
        self.battleRewardId = battleRewardId
        self.battleTaskRewardId = battleTaskRewardId
        self.mp = mp
        self.bfHostId = bfHostId
        self.monthRecord = copy.deepcopy(monthRecord)

    def getDTO(self):
        return (self.hostId,
         self.groupId,
         self.combatScore,
         self.declarePoint,
         self.enemyHostId,
         self.camp,
         self.currCamp,
         self.applyIdx,
         self.luckyWeekId,
         self.gradeScore,
         self.gradeScoreDelta,
         self.lastScore,
         self.battleRes,
         self.battleRewardId,
         self.battleTaskRewardId,
         self.mp)

    def fromDTO(self, dto):
        self.hostId, self.groupId, self.combatScore, self.declarePoint, self.enemyHostId, self.camp, self.currCamp, self.applyIdx, self.luckyWeekId, self.gradeScore, self.gradeScoreDelta, self.lastScore, self.battleRes, self.battleRewardId, self.battleTaskRewardId, self.mp = dto
        return self

    def getQueryDTO(self):
        return (self.declarePoint,
         self.bidDeclarePoint,
         self.camp,
         self.currCamp,
         self.enemyHostId,
         self.gradeScore,
         self.gradeScoreDelta,
         self.lastScore,
         self.battleRes,
         self.battleRewardId,
         self.battleTaskRewardId,
         self.mp)

    def fromQueryDTO(self, dto):
        self.declarePoint, self.bidDeclarePoint, self.camp, self.currCamp, self.enemyHostId, self.gradeScore, self.gradeScoreDelta, self.lastScore, self.battleRes, self.battleRewardId, self.battleTaskRewardId, self.mp = dto
        return self

    def getSimpleDTO(self):
        return (self.hostId,
         self.camp,
         self.currCamp,
         self.enemyHostId,
         self.combatScore,
         self.starLv)

    def fromSimpleDTO(self, dto):
        self.hostId, self.camp, self.currCamp, self.enemyHostId, self.combatScore, self.starLv = dto
        return self

    def getRankData(self):
        return (self.hostId, self.winNum, self.conquerScore)

    def fromRankData(self, d):
        self.hostId, self.winNum, self.conquerScore = d
        return self

    def getData(self, attrs):
        r = {}
        for attr in attrs:
            r[attr] = getattr(self, attr)

        return r

    def updateData(self, d):
        for attr, v in d:
            setattr(self, attr, v)

    def resetCamp(self):
        self.camp = 0
        self.currCamp = 0
        self.enemyHostId = 0
        self.intentTargets = []
        self.lastScore = 0

    def resetRecord(self):
        self.record.clear()
        self.gradeScoreDelta = 0
        self.starLv = 0

    def switchCamp(self):
        self.currCamp = getEnemyCamp(self.currCamp)

    def switchCampOfDate(self):
        self.currCamp = getCurrCampOfDate(self.camp)

    def inLuckyWeek(self, weekId = 0):
        if not self.luckyWeekId:
            return False
        if not weekId:
            weekId = utils.getWeekSecond()
        return weekId == self.luckyWeekId


class BaseCountry(UserDictType):

    def applyMatches(self, matches):
        for hostId, enemyHostId in matches:
            c = self.getCountry(hostId)
            c.enemyHostId = enemyHostId
            c = self.getCountry(enemyHostId)
            c.enemyHostId = hostId

    def applyCamps(self, camps):
        for hostId, camp, declarePoint, applyIdx in camps:
            c = self.getCountry(hostId)
            c.camp = camp
            c.currCamp = getEnemyCamp(camp)
            c.declarePoint = declarePoint
            c.applyIdx = applyIdx


class SimpleWWFortVal(UserSoleType):

    def __init__(self, hostId = 0, inCombat = False, bossEntId = 0):
        self.hostId = hostId
        self.inCombat = inCombat
        self.bossEntId = bossEntId


class SimpleWWReliveBoardVal(UserSoleType):

    def __init__(self, hostId = 0):
        self.hostId = hostId


class BaseWWFortVal(UserSoleType):

    def __init__(self, fortId = 0, ownerCamp = 0, inCombat = False):
        self.fortId = fortId
        self.ownerCamp = ownerCamp
        self.inCombat = inCombat


class BaseWWReliveBoardVal(UserSoleType):

    def __init__(self, ownerCamp = 0):
        self.ownerCamp = ownerCamp


class WWArmyCandidateVal(UserSoleType):

    def __init__(self, gbId, name = '', ctype = 0, rank = 0, guildNUID = 0, votes = 0, deleted = False, guildName = '', groupType = 0):
        self.gbId = gbId
        self.name = name
        self.ctype = ctype
        self.rank = rank
        self.guildNUID = guildNUID
        self.guildName = guildName
        self.votes = votes
        self.deleted = deleted
        self.groupType = groupType

    def fromDTO(self, dto):
        self.gbId, self.votes, self.name, self.ctype, self.rank, self.deleted, self.guildName, self.groupType = dto
        return self

    def getDTO(self):
        return (self.gbId,
         self.votes,
         self.name,
         self.ctype,
         self.rank,
         self.deleted,
         self.guildName,
         self.groupType)


class WWArmySkillVal(UserSoleType):

    def __init__(self, skillId = 0, level = 1, nextTime = 0):
        self.skillId = skillId
        self.level = level
        self.nextTime = nextTime

    def getDTO(self):
        return (self.skillId, self.level, self.nextTime)

    def fromDTO(self, dto):
        self.skillId, self.level, self.nextTime = dto


class WWTournamentResultMatchVal(UserSoleType):

    def __init__(self, winGuildNUID = 0, troopNUID = 0, idx = 0):
        self.winGuildNUID = winGuildNUID
        self.troopNUID = troopNUID
        self.idx = idx

    def inMatch(self):
        return self.troopNUID and not self.winGuildNUID


class WWTournamentResultMatch(UserDictType):

    def _lateReload(self):
        super(WWTournamentResultMatch, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()

    def addAll(self, guildNUIDs):
        for i in range(0, len(guildNUIDs), 2):
            self[guildNUIDs[i], guildNUIDs[i + 1]] = WWTournamentResultMatchVal(idx=i / 2)

    def isFinished(self):
        for (g1, g2), mVal in self.iteritems():
            if g1 and g2 and not mVal.winGuildNUID:
                return False

        return True

    def updateWinner(self, guildNUID):
        for k, mVal in self.iteritems():
            if guildNUID in k:
                mVal.winGuildNUID = guildNUID
                break

    def updateTroopNUID(self, guildNUID, troopNUID):
        for k, mVal in self.iteritems():
            if guildNUID in k:
                mVal.troopNUID = troopNUID
                break

    def getWinner(self, guildNUID):
        for k, mVal in self.iteritems():
            if guildNUID in k:
                return mVal.winGuildNUID

    def getTroopNUID(self, guildNUID):
        for k, mVal in self.iteritems():
            if guildNUID in k:
                return mVal.troopNUID

    def getIdx(self, guildNUID):
        if not guildNUID:
            return -1
        for k, mVal in self.iteritems():
            if guildNUID in k:
                return mVal.idx

        return -1

    def getGuildsNUID(self):
        guildsNUID = []
        for (g1, g2), mVal in self.iteritems():
            guildsNUID.append(g1)
            guildsNUID.append(g2)

        return guildsNUID

    def getDTO(self, bSort = False):
        r = []
        for (guildNUID1, guildNUID2), v in self.iteritems():
            r.append((guildNUID1,
             guildNUID2,
             v.winGuildNUID,
             v.troopNUID,
             v.idx))

        if bSort:
            r.sort(key=lambda x: x[-1])
        return r

    def fromDTO(self, dto):
        for guildNUID1, guildNUID2, winGuildNUID, troopNUID, idx in dto:
            self[guildNUID1, guildNUID2] = WWTournamentResultMatchVal(winGuildNUID=winGuildNUID, troopNUID=troopNUID, idx=idx)

        return self


class WWTournamentResultVal(UserDictType):

    def __init__(self, hostId = 0, guilds = {}, ver = 0, candidateGuildNUIDs = {}, resultGuildNUIDs = {}):
        self.hostId = hostId
        self.guilds = copy.deepcopy(guilds)
        self.candidateGuildNUIDs = copy.deepcopy(candidateGuildNUIDs)
        self.resultGuildNUIDs = copy.deepcopy(resultGuildNUIDs)
        self.ver = ver

    def _lateReload(self):
        super(WWTournamentResultVal, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()

    def initMatch(self, groupId, roundNum, guildNUIDs):
        match = WWTournamentResultMatch()
        match.addAll(guildNUIDs)
        self[groupId, roundNum] = match

    def updateWinner(self, groupId, roundNum, winGuildNUID):
        match = self.get((groupId, roundNum))
        if match != None:
            match.updateWinner(winGuildNUID)

    def updateTroopNUID(self, groupId, roundNum, guildNUID, troopNUID):
        match = self.get((groupId, roundNum))
        if match != None:
            match.updateTroopNUID(guildNUID, troopNUID)

    def getTroopNUID(self, groupId, roundNum, guildNUID):
        match = self.get((groupId, roundNum))
        if match != None:
            return match.getTroopNUID(guildNUID)

    def getIdx(self, groupId, roundNum, guildNUID):
        match = self.get((groupId, roundNum))
        if match != None:
            return match.getIdx(guildNUID)

    def isFinished(self, groupId, roundNum, guildNUID):
        match = self.get((groupId, roundNum))
        if match != None:
            return match.getWinner(guildNUID)
        return True

    def isRoundFinished(self, groupId, roundNum):
        match = self.get((groupId, roundNum))
        if match != None:
            return match.isFinished()
        return True

    def getGuildsNUIDByRound(self, roundNum, groupId):
        if not self.get((groupId, roundNum), None):
            return []
        return self.get((groupId, roundNum)).getGuildsNUID()

    def getDTOByGroup(self, groupId):
        r = []
        for (groupId_, roundNum), mVal in self.iteritems():
            if groupId_ == groupId:
                r.append((roundNum, mVal.getDTO()))

        return r

    def fromDTOByGroup(self, groupId, dto):
        for roundNum, mValDTO in dto:
            self[groupId, roundNum] = WWTournamentResultMatch().fromDTO(mValDTO)

        return self

    def resetByGroup(self, groupId):
        self.candidateGuildNUIDs.pop(groupId, None)
        self.resultGuildNUIDs.pop(groupId, None)
        for _groupId, roundNum in self.keys():
            if _groupId == groupId:
                self.pop((groupId, roundNum))

    def resetByRound(self, groupId, roundNum):
        match = self.get((groupId, roundNum))
        if match != None:
            for mVal in match.itervalues():
                mVal.troopNUID = 0
                mVal.winGuildNUID = 0


class WWTournamentResult(UserDictType):

    def __init__(self, bfHostId = 0, groupVer = {}, guildVer = 1):
        self.bfHostId = bfHostId
        self.groupVer = copy.deepcopy(groupVer)
        self.guildVer = guildVer
        for groupId in gametypes.GUILD_TOURNAMENT_GROUP:
            self.groupVer[groupId] = 1

    def _lateReload(self):
        super(WWTournamentResult, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()

    def reset(self):
        self.bfHostId = 0
        self.updateGuildVer()
        self.updateGroupVer()
        self.clear()

    def resetByGroup(self, hostId, groupId):
        self.updateGuildVer()
        self.updateGroupVer(groupId)
        rVal = self.get(hostId)
        if rVal != None:
            rVal.resetByGroup(groupId)

    def getGuildName(self, guildNUID, includeHost = False):
        for hostId, rVal in self.iteritems():
            guildName = rVal.guilds.get(guildNUID)
            if guildName:
                if includeHost:
                    return '%s(%s)'(guildName, utils.getServerName(hostId))
                else:
                    return guildName

        return ''

    def getByHostId(self, hostId):
        if not hostId:
            return
        val = self.get(hostId)
        if val == None:
            val = WWTournamentResultVal(hostId=hostId)
            self[hostId] = val
        return val

    def getHostDTO(self, groupId):
        return [ (hostId, rVal.resultGuildNUIDs.get(groupId, ())) for hostId, rVal in self.iteritems() ]

    def getResultGuilds(self, hostId, groupId):
        return self.get(hostId).resultGuildNUIDs.get(groupId, ())

    def fromHostDTO(self, groupId, dto):
        for hostId, resultGuildNUIDs in dto:
            rVal = self.getByHostId(hostId)
            rVal.resultGuildNUIDs[groupId] = resultGuildNUIDs

        return self

    def getGuildDTO(self):
        return [ (hostId, rVal.guilds) for hostId, rVal in self.iteritems() ]

    def fromGuildDTO(self, dto):
        for hostId, guilds in dto:
            rVal = self.getByHostId(hostId)
            rVal.guilds = guilds

    def getDTOByGroup(self, groupId):
        r = []
        for hostId, rVal in self.iteritems():
            r.append((hostId, rVal.getDTOByGroup(groupId)))

        return r

    def fromDTOByGroup(self, groupId, dto):
        for hostId, rValDTO in dto:
            self.getByHostId(hostId).fromDTOByGroup(groupId, rValDTO)

        return self

    def getGuildHostId(self, groupId, guildNUID):
        for hostId, rVal in self.iteritems():
            if guildNUID in rVal.guilds:
                return hostId

        return 0

    def updateGuildVer(self):
        self.guildVer += 1

    def updateGroupVer(self, groupId = 0):
        if groupId:
            self.groupVer[groupId] += 1
        else:
            for _groupId in self.groupVer.iterkeys():
                self.groupVer[_groupId] += 1


class WWArmyPostVal(UserSoleType):

    def __init__(self, postId = 0, gbId = 0, name = '', school = 0, lv = 0, combatScore = 0, tWhen = 0, sex = 0, photo = '', bOnline = False, skills = {}, mpUsed = 0, statueLoaded = False, privileges = []):
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

    def getSkill(self, skillId):
        if skillId not in WWAD.data.get(self.postId, {}).get('skills', ()):
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
         self.privileges)

    def fromDTO(self, dto):
        self.postId, self.gbId, self.name, self.sex, self.school, self.lv, self.combatScore, self.photo, self.bOnline, self.mpUsed, self.privileges = dto
        return self

    def getSkillDTO(self):
        return [ (x.skillId, x.level, x.nextTime) for x in self.skills.itervalues() ]

    def fromSkillDTO(self, dto):
        self.skills.clear()
        for skillId, level, nextTime in dto:
            self.skills[skillId] = WWArmySkillVal(skillId=skillId, level=level, nextTime=nextTime)

    def getArmyData(self, key, default = None):
        return WWAD.data.get(self.postId, {}).get(key, default)

    def hasPrivilege(self, privilegeId):
        data = WWAD.data.get(self.postId, {})
        if gameconfig.enableWorldWarYoungGroup():
            fixedPrivileges = data.get('fixedPrivilegesNew')
        else:
            fixedPrivileges = data.get('fixedPrivileges')
        if fixedPrivileges and privilegeId in fixedPrivileges:
            return True
        return privilegeId in self.privileges


def getCompletedTaskIds(fort, hostId, bWin = False, battleScore = None):
    score = 0
    fortNum = 0
    for fortId, _hostId in fort.iteritems():
        if _hostId == hostId:
            score += WWFD.data.get(fortId).get('score', 0)
            fortNum += 1

    if battleScore:
        score = battleScore
    completedTargetIds = set()
    for targetId, data in WWBTTD.data.iteritems():
        ftype = data.get('ftype')
        params = data.get('params')
        r = False
        if ftype == gametypes.WORLD_WAR_BATTLE_TARGET_FORT:
            r = fort.get(params) == hostId
        elif ftype == gametypes.WORLD_WAR_BATTLE_TARGET_SCORE:
            r = score >= params
        elif ftype == gametypes.WORLD_WAR_BATTLE_TARGET_WIN:
            r = bWin
        elif ftype == gametypes.WORLD_WAR_BATTLE_TARGET_FORT_NUM:
            r = fortNum >= params
        if r:
            completedTargetIds.add(targetId)

    completedTaskIds = []
    for taskId, data in WWBTD.data.iteritems():
        targetIds = data.get('targetIds', ())
        if not targetIds:
            continue
        if set(targetIds).issubset(completedTargetIds):
            completedTaskIds.append(taskId)

    return completedTaskIds


def filterTaskIds(camp, starLv, enemyStarLv, taskIds):
    r = []
    for taskId in taskIds:
        if WWBRD.data.has_key((camp,
         starLv,
         enemyStarLv,
         taskId)):
            r.append(taskId)

    return r


def isWinTask(taskId):
    return WWBTTD.data.get(WWBTD.data.get(taskId, {}).get('targetIds')[0], {}).get('ftype') == gametypes.WORLD_WAR_BATTLE_TARGET_WIN


def getArmyOrder(postId):
    return WWAD.data.get(postId, {}).get('order', 0)


def getArmySalary(postId, score):
    data = WWAD.data.get(postId)
    bonusId = 0
    for (start, end), bonusId in data.get('salary', ()):
        if score >= start and score <= end:
            return bonusId

    return bonusId


def isValidOrderInfo(v):
    return v and v[0] != None


def getPSkillPostIds():
    postIds = []
    for postId, data in WWAD.data.iteritems():
        if data.get('pskills'):
            postId.append(postId)

    return postIds


def getSkillPostIds():
    postIds = []
    for postId, data in WWAD.data.iteritems():
        if data.get('skills'):
            postId.append(postId)

    return postIds


def isSameHireGroup(g1, g2):
    return g1 == gametypes.WORLD_WAR_GROUP_ZHENGZHAN and g2 == gametypes.WORLD_WAR_GROUP_ZHENGZHAN or g1 != gametypes.WORLD_WAR_GROUP_ZHENGZHAN and g2 != gametypes.WORLD_WAR_GROUP_ZHENGZHAN


def calcRobBindCash(totalRobScore, score, res, attends):
    if totalRobScore <= 0 or score <= 0 or attends <= 0:
        return 0
    f = WWCD.data.get('robResExchangeCashFormula')
    if not f:
        return 0
    allCash = f({'res': res,
     'attends': attends})
    cash = min(WWCD.data.get('robMaxExchangeCash', 200000), int(allCash * score / totalRobScore))
    gamelog.debug('calcRobBindCash: ', totalRobScore, score, res, attends, cash)
    return cash


def getQLBHDescByWWType(wwtype):
    if wwtype in (gametypes.WORLD_WAR_TYPE_BATTLE_YOUNG, gametypes.WORLD_WAR_TYPE_ROB_YOUNG):
        return '°×»¢'
    if wwtype in (gametypes.WORLD_WAR_TYPE_BATTLE, gametypes.WORLD_WAR_TYPE_ROB):
        return 'ÇàÁú'
    return ''


def getRobTopRewardKey(wwtype):
    trdKey = gametypes.TOP_TYPE_WW_ROB_SCORE
    if gameconfig.enableWorldWarYoungGroup():
        if wwtype == gametypes.WORLD_WAR_TYPE_ROB:
            trdKey = gametypes.TOP_TYPE_WW_ROB_SCORE_QL
        elif wwtype == gametypes.WORLD_WAR_TYPE_ROB_YOUNG:
            trdKey = gametypes.TOP_TYPE_WW_ROB_SCORE_BH
        else:
            trdKey = None
    return trdKey


def getBattleTopRewardKey(wwtype):
    trdKey = gametypes.TOP_TYPE_WB_SCORE
    if gameconfig.enableWorldWarYoungGroup():
        if wwtype == gametypes.WORLD_WAR_TYPE_BATTLE:
            trdKey = gametypes.TOP_TYPE_WB_SCORE_QL
        elif wwtype == gametypes.WORLD_WAR_TYPE_BATTLE_YOUNG:
            trdKey = gametypes.TOP_TYPE_WB_SCORE_BH
        else:
            trdKey = None
    return trdKey


def getBattleHireTypeByLevel(level):
    if level > const.WORLD_WAR_HIRE_MINLV_NEW:
        return gametypes.WORLD_WAR_TYPE_BATTLE
    else:
        return gametypes.WORLD_WAR_TYPE_BATTLE_YOUNG
