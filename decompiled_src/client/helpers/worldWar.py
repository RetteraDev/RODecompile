#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/worldWar.o
import copy
import BigWorld
import const
import utils
import gametypes
import commonWorldWar
import gameglobal
from commonWorldWar import BaseCountryVal, BaseCountry, WWArmyPostVal, SimpleWWFortVal, WWTournamentResult
from guis import uiUtils
from guis import uiConst
from data import world_war_fort_data as WWFD
from data import world_war_battle_reward_data as WWBRD
from data import world_war_battle_task_reward_data as WWBTRD
from cdata import top_reward_data as TRD
from cdata import game_msg_def_data as GMDD
from data import world_war_config_data as WWCD

class CountryVal(BaseCountryVal):
    pass


class Country(BaseCountry):

    def getCountry(self, hostId):
        c = self.get(hostId)
        if not c:
            c = CountryVal(hostId=hostId)
            self[hostId] = c
        return c

    def fromDTO(self, dtos):
        simpleLen = len(CountryVal().getSimpleDTO())
        for dto in dtos:
            hostId = dto[0]
            if not hostId:
                continue
            c = self.getCountry(hostId)
            if len(dto) == simpleLen:
                c.fromSimpleDTO(dto)
            else:
                c.fromDTO(dto)

    def resetCamp(self, groupId = 0):
        for c in self.itervalues():
            if groupId and c.groupId != groupId:
                continue
            c.resetCamp()


class WWRobZaiju(object):

    def __init__(self, level = 1, position = None, hp = 0, mhp = 0, robRes = 0, playerDieNum = 0):
        self.level = level
        self.position = position
        self.hp = hp
        self.mhp = mhp
        self.robRes = robRes
        self.playerDieNum = playerDieNum
        self.mineRobRes = 0
        self.enemyRobRes = 0
        self.robEachFortRes = dict()

    def fromDTO(self, dto):
        self.position, self.hp, self.playerDieNum, robRes, robEachFortRes = dto
        self.robRes = robRes
        self.robEachFortRes.update(robEachFortRes)
        for hostId, res in self.robRes.iteritems():
            if hostId == utils.getHostId():
                self.mineRobRes = res
            else:
                self.enemyRobRes = res


class WorldWar(object):

    def __init__(self, country = Country(), state = 0, readyForJoin = False, battleState = 0, armyState = 0, battleEndTime = 0, battleMoraleIdx = -1, luckyHostId = 0, questStarLv = const.WORLD_WAR_MAX_QUEST_STAR_LV, enemyQuestStarLv = const.WORLD_WAR_MAX_QUEST_STAR_LV, intentTargets = [], bloodWeekId = 0, bidDeclarePoint = 0, applyTargetsRoundNum = 0, applyTargetsEndTime = 0, applyGbId = 0, applyRoleName = '', killAvatarCnt = 0, killAvatarCntTotal = 0, monthRank = 0, weeklyKillAvatarRank = 0, weeklyKillAvatarSchoolRank = 0, totalKillAvatarRank = 0, totalKillAvatarSchoolRank = 0, lastEnemyHostId = 0, wwscore = 0, maxComboKill = 0, winCount = {}, battleScore = 0, battleKillAvatar = 0, battleAssist = 0, battleRes = 0, armyCandidate = [], gbId2AmryCandidate = {}, army = {}, postId2gbId = {}, armyMark = {}, voteResultEndTime = 0, impeachText = '', impeachState = '', impeachVoteEndTime = 0, impeachApplyGbId = 0, impeachAgreeNum = 0, impeachTotalNum = 0, announcement = '', armySkills = {}, battleHireStopped = False, robState = 0, robScore = 0, totalRobScore = 0, rank = {}, fort = {}, hireVer = 0, volatileVer = -1, reliveBoard = {}, recordVer = -1, countryVer = -1, rankVer = -1, fortVer = -1, armyCandidateVer = -1, armyCandidateVoteVer = -1, armyVer = -1, armyOnlineVer = -1, armyMarkVer = -1, ver = -1, robStateDict = {}, battleStateDict = {}):
        self.country = copy.deepcopy(country)
        self.state = state
        self.readyForJoin = readyForJoin
        self.battleState = battleState
        self.armyState = armyState
        self.battleEndTime = battleEndTime
        self.battleMoraleIdx = battleMoraleIdx
        self.luckyHostId = luckyHostId
        self.questStarLv = questStarLv
        self.enemyQuestStarLv = enemyQuestStarLv
        self.bloodWeekId = bloodWeekId
        self.intentTargets = copy.deepcopy(intentTargets)
        self.bidDeclarePoint = bidDeclarePoint
        self.applyTargetsRoundNum = applyTargetsRoundNum
        self.applyTargetsEndTime = applyTargetsEndTime
        self.applyGbId = applyGbId
        self.applyRoleName = applyRoleName
        self.killAvatarCnt = killAvatarCnt
        self.killAvatarCntTotal = killAvatarCntTotal
        self.weeklyKillAvatarRank = weeklyKillAvatarRank
        self.weeklyKillAvatarSchoolRank = weeklyKillAvatarSchoolRank
        self.totalKillAvatarRank = totalKillAvatarRank
        self.totalKillAvatarSchoolRank = totalKillAvatarSchoolRank
        self.lastEnemyHostId = lastEnemyHostId
        self.wwscore = wwscore
        self.maxComboKill = maxComboKill
        self.winCount = winCount
        self.battleScore = battleScore
        self.battleKillAvatar = battleKillAvatar
        self.battleAssist = battleAssist
        self.battleRes = battleRes
        self.monthRank = monthRank
        self.rank = copy.deepcopy(rank)
        self.fort = copy.deepcopy(fort)
        self.reliveBoard = copy.deepcopy(reliveBoard)
        self.armyCandidate = copy.deepcopy(armyCandidate)
        self.gbId2AmryCandidate = copy.deepcopy(gbId2AmryCandidate)
        self.army = copy.deepcopy(army)
        self.armyMark = copy.deepcopy(armyMark)
        self.postId2gbId = copy.deepcopy(postId2gbId)
        self.voteResultEndTime = voteResultEndTime
        self.wwqorders = dict()
        self.wwTicketHosts = dict()
        self.impeachText = impeachText
        self.impeachState = impeachState
        self.impeachVoteEndTime = impeachVoteEndTime
        self.impeachApplyGbId = impeachApplyGbId
        self.impeachAgreeNum = impeachAgreeNum
        self.impeachTotalNum = impeachTotalNum
        self.announcement = announcement
        self.armySkills = copy.deepcopy(armySkills)
        self.battleHireStopped = battleHireStopped
        self.robState = robState
        self.hireVer = hireVer
        self.volatileVer = volatileVer
        self.recordVer = recordVer
        self.countryVer = countryVer
        self.rankVer = rankVer
        self.fortVer = fortVer
        self.armyCandidateVer = armyCandidateVer
        self.armyCandidateVoteVer = armyCandidateVoteVer
        self.armyVer = armyVer
        self.armyOnlineVer = armyOnlineVer
        self.armyMarkVer = armyMarkVer
        self.ver = ver
        self.voteResultEndTime = 0
        self.tournamentResult = WWTournamentResult(groupVer={1: 0,
         2: 0}, guildVer=0)
        self.isNeedCheckInactive = False
        self.robZaiju = WWRobZaiju()
        self.robScore = robScore
        self.totalRobScore = totalRobScore
        self.totalRobAttends = 0
        self.tNextTeleport = 0
        self.tRobStateEnd = 0
        self.robZaijuEntID = 0
        self.robAuraCheckTimeID = 0
        self.robBossHintTimeID = 0
        self.robBossInZaiju = False
        self.WWQLBHSelection = {gametypes.WORLD_WAR_TYPE_BATTLE: 0,
         gametypes.WORLD_WAR_TYPE_ROB: 0}
        self.robStateDict = robStateDict
        self.battleStateDict = battleStateDict

    def isOpen(self):
        return self.state == gametypes.WORLD_WAR_STATE_OPEN

    def isRunning(self):
        return self.state in gametypes.WORLD_WAR_STATE_RUNNING

    def isLucky(self):
        return utils.getHostId() == self.luckyHostId and not self.readyForJoin

    def inBloodWeek(self):
        return utils.getWeekSecond() == self.bloodWeekId

    def getCamp(self):
        return self.getCountry().camp

    def getBattleCamp(self):
        return self.getCountry(BigWorld.player().getWBHostId()).camp

    def getCurrCamp(self):
        return self.getCountry().currCamp

    def getDayCamp(self, day):
        if day <= 0 or self.getCamp() == gametypes.WOLD_WAR_CAMP_NONE:
            return gametypes.WOLD_WAR_CAMP_NONE
        return (self.getCamp() + day + 1) % 2 + 1

    def getEnemyCamp(self):
        camp = self.getCamp()
        if not camp:
            return 0
        else:
            return commonWorldWar.getEnemyCamp(camp)

    def getBattleEnemyCamp(self):
        camp = self.getBattleCamp()
        if not camp:
            return 0
        else:
            return commonWorldWar.getEnemyCamp(camp)

    def getCurrEnemyCamp(self):
        camp = self.getCurrCamp()
        if not camp:
            return 0
        else:
            return commonWorldWar.getEnemyCamp(camp)

    def switchCamp(self, currCamp):
        self.getCountry().currCamp = currCamp
        self.getCountry(self.getEnemyHostId()).currCamp = commonWorldWar.getEnemyCamp(currCamp)

    def reset(self):
        self.luckyHostId = 0
        self.applyGbId = 0
        self.applyRoleName = ''
        self.intentTargets = []
        self.country.resetCamp()

    def getBattleEnemyHostId(self):
        return self.getCountry(BigWorld.player().getWBHostId()).enemyHostId

    def getEnemyHostId(self):
        return self.getCountry().enemyHostId

    def getGroupId(self):
        return self.getCountry().groupId

    def getEnemyCountry(self):
        hostId = self.getEnemyHostId()
        if not hostId:
            return
        return self.getCountry(hostId)

    def getCountry(self, hostId = 0):
        if not hostId:
            p = BigWorld.player()
            if p._isSoul():
                hostId = p.crossFromHostId
            else:
                hostId = utils.getHostId()
        return self.country.getCountry(hostId)

    def fromDTO(self, dto):
        c = self.getCountry()
        c.groupId, self.state, self.readyForJoin, self.battleStateDict, self.robStateDict, self.bloodWeekId, self.armyState, self.battleEndTime, self.luckyHostId, self.applyGbId, self.applyRoleName, c.combatScore, self.applyTargetsRoundNum, self.applyTargetsEndTime, self.questStarLv, self.enemyQuestStarLv, self.winCount, self.lastEnemyHostId, self.announcement, self.intentTargets, cdto, edto = dto
        self.battleState = self.battleStateDict.get(gametypes.WORLD_WAR_TYPE_BATTLE, 0)
        if cdto:
            c.fromQueryDTO(cdto)
        if edto:
            enemyHostId = edto[0]
            self.country.getCountry(enemyHostId).fromDTO(edto)

    def getArmyFromDTO(self, dtos):
        self.army.clear()
        for dto in dtos:
            val = WWArmyPostVal().fromDTO(dto)
            self.army[val.gbId] = val

        return self.army

    def _recalcQuestStarLv(self):
        self.questStarLv, self.enemyQuestStarLv = self.calcQuestStarLv(self.getEnemyHostId())

    def calcQuestStarLv(self, hostId = 0):
        if not hostId or hostId == utils.getHostId():
            return (1, 1)
        c = self.getCountry()
        other = self.getCountry(hostId)
        return commonWorldWar.calcQuestStarLv(c.combatScore, other.combatScore)

    def calcBattleQuestStarLv(self):
        p = BigWorld.player()
        c = self.getCountry(p.getWBHostId())
        other = self.getCountry(c.enemyHostId)
        return commonWorldWar.calcQuestStarLv(c.combatScore, other.combatScore)

    def recalcScore(self):
        enemyHostId = self.lastEnemyHostId
        if not enemyHostId:
            return
        c = self.getCountry()
        ec = self.getCountry(enemyHostId)
        s1, s2 = commonWorldWar.judge(c, ec)
        c.score = s1
        ec.score = s2

    def _calcBattleScore(self, hostId):
        score = 0
        for fortId, fort in self.fort.iteritems():
            if hostId == fort.hostId:
                score += WWFD.data.get(fortId).get('score', 0)

        return score

    def getBattleScores(self, hostId):
        c = self.getCountry(hostId)
        return (self._calcBattleScore(hostId), self._calcBattleScore(c.enemyHostId))

    def getBattleMoraleEffect(self):
        if self.battleMoraleIdx < 0:
            return 0
        params = WWCD.data.get('moraleEffect')
        if not params:
            return 0
        if self.battleMoraleIdx >= len(params):
            return 0
        return params[self.battleMoraleIdx][1]

    def buildArmyIndex(self):
        self.postId2gbId.clear()
        for gbId, post in self.army.iteritems():
            if self.postId2gbId.has_key(post.postId):
                self.postId2gbId[post.postId].append(gbId)
            else:
                self.postId2gbId[post.postId] = [post.gbId]

    def removeArmyByPostId(self, postId):
        gbIds = self.postId2gbId.get(postId)
        if gbIds:
            for gbId in gbIds:
                self.army.pop(gbId, None)

    def getArmyByPostId(self, postId, index = 0):
        gbIds = self.postId2gbId.get(postId)
        if not gbIds:
            return
        if index >= len(gbIds):
            return
        return self.army.get(gbIds[index])

    def getArmyByGbId(self, gbId):
        post = self.army.get(gbId)
        if post:
            return post
        p = BigWorld.player()
        if p.gbId == gbId and p.wwArmyPostId:
            post = WWArmyPostVal(gbId=gbId, postId=p.wwArmyPostId, name=p.roleName, school=p.school, sex=p.physique.sex, lv=p.lv, photo=p.friend.photo)
            self.army[gbId] = post
            self.buildArmyIndex()
        return post

    def getArmySuperMgrs(self):
        posts = []
        for postId in gametypes.WW_ARMY_SUPER_MGR_POST_IDS:
            post = self.getArmyByPostId(postId)
            if post:
                posts.append(post)

        return posts

    def getArmyLeader(self):
        return self.getArmyByPostId(gametypes.WW_ARMY_LEADER_POST_ID)

    def getPostByGbId(self, gbId = 0):
        if not gbId:
            gbId = BigWorld.player().gbId
        val = self.getArmyByGbId(gbId)
        if val:
            return val.postId
        return 0

    def getFort(self, fortId):
        fort = self.fort.get(fortId)
        if not fort:
            fort = SimpleWWFortVal()
            self.fort[fortId] = fort
        return fort

    def getFortHostId(self, fortId):
        fort = self.fort.get(fortId)
        if not fort:
            return 0
        return fort.hostId

    def getBattleRankReward(self, rank):
        p = BigWorld.player()
        rankType = gametypes.TOP_TYPE_WB_SCORE
        if p.recentEnterWWType == gametypes.WORLD_WAR_TYPE_BATTLE:
            rankType = gametypes.TOP_TYPE_WB_SCORE_QL
        elif p.recentEnterWWType == gametypes.WORLD_WAR_TYPE_BATTLE_YOUNG:
            rankType = gametypes.TOP_TYPE_WB_SCORE_BH
        for data in TRD.data.get((rankType, 0, 0), ()):
            rankStart, rankEnd = data.get('rankRange')
            if rank >= rankStart and rank <= rankEnd:
                return data.get('bonusId', 0)

        if self.battleScore > WWCD.data.get('battlePersonalRewardScore', 0):
            return WWCD.data.get('battlePersonalBonusId', 0)
        else:
            return 0

    def getBattleTaskPersonalReward(self, taskIds):
        bonusIds = []
        if self.battleScore < WWCD.data.get('battlePersonalRewardScore', 0):
            return bonusIds
        wbHireHostId = BigWorld.player()._getWBHireHostId()
        if wbHireHostId:
            c = self.getCountry(wbHireHostId)
            camp = c.camp
            questStarLv = c.starLv
            enemyQuestStarLv = self.getCountry(c.enemyHostId).starLv
        else:
            camp = self.getCamp()
            questStarLv = self.questStarLv
            enemyQuestStarLv = self.enemyQuestStarLv
        if wbHireHostId:
            if self.inBloodWeek():
                key = 'hireBloodBonusId'
            else:
                key = 'hireBonusId'
        elif self.inBloodWeek():
            key = 'bloodBonusId'
        else:
            key = 'bonusId'
        for taskId in taskIds:
            bonusId = WWBTRD.data.get((camp,
             questStarLv,
             enemyQuestStarLv,
             taskId), {}).get(key)
            if bonusId:
                bonusIds.append(bonusId)

        return bonusIds

    def getBattleTaskCountryReward(self, taskIds):
        bonusIds = []
        if BigWorld.player().fame.get(const.WW_WAR_SCORE_FAME_ID, 0) < WWCD.data.get('battleCountryRewardScore', 0):
            return bonusIds
        for taskId in taskIds:
            bonusId = WWBRD.data.get((self.getCamp(),
             self.questStarLv,
             self.enemyQuestStarLv,
             taskId), {}).get('bonusId')
            if bonusId:
                bonusIds.append(bonusId)

        return bonusIds

    def getBattleQueueMsg(self):
        pnum, oldNum, youngNum, hnum = self.wwqorders.get(gametypes.WORLD_WAR_TYPE_BATTLE, (0, 0, 0, 0))
        num = sum([oldNum, youngNum])
        p = BigWorld.player()
        if self.battleState == gametypes.WORLD_WAR_BATTLE_STATE_OPEN:
            if (p.wbApplyHireHostId or p.wbHireHostId) and hnum:
                return uiUtils.getTextFromGMD(GMDD.data.WORLD_WAR_ENTER_QUEUE_BOX_HIRE_FULL_HIRE_NOTIFY) % hnum
            elif num:
                return uiUtils.getTextFromGMD(GMDD.data.WORLD_WAR_ENTER_QUEUE_FULL_NOTIFY) % (pnum, num)
            else:
                return uiUtils.getTextFromGMD(GMDD.data.WORLD_WAR_ENTER_QUEUE_FULL_ARMY_NOTIFY) % pnum
        else:
            if num:
                return uiUtils.getTextFromGMD(GMDD.data.WORLD_WAR_ENTER_QUEUE_NOTIFY) % (pnum, num)
            return uiUtils.getTextFromGMD(GMDD.data.WORLD_WAR_ENTER_QUEUE_ARMY_NOTIFY) % pnum

    def getQueueBoxMsg(self, queueType):
        pnum, oldNum, youngNum, hnum = self.wwqorders.get(queueType, (0, 0, 0, 0))
        p = BigWorld.player()
        num = sum([oldNum, youngNum])
        isMinLv = False
        isInArmy = self.getPostByGbId(p.gbId)
        if p.lv == const.WORLD_WAR_ARMY_MINLV:
            isMinLv = True
        groupType = '%s£º' % gametypes.WORLD_WAR_TYPE_GROUP_TXT[queueType]
        if not gameglobal.rds.configData.get('enableWorldWarYoungGroup', False):
            groupType = ''
        if queueType == uiConst.WW_QUEUE_TYPE_BATTLE or queueType == uiConst.WW_QUEUE_TYPE_BATTLE_YOUNG:
            if self.battleState == gametypes.WORLD_WAR_BATTLE_STATE_OPEN:
                if BigWorld.player().isWBHired():
                    num = pnum + num
                    if num:
                        if hnum:
                            return uiUtils.getTextFromGMD(GMDD.data.WORLD_WAR_ENTER_QUEUE_BOX_HIRE_FULL_NOTIFY, '%s_%s') % (num, hnum)
                        else:
                            return uiUtils.getTextFromGMD(GMDD.data.WORLD_WAR_ENTER_QUEUE_BOX_HIRE_FULL_NO_HIRE_NOTIFY, '%s') % num
                    else:
                        return uiUtils.getTextFromGMD(GMDD.data.WORLD_WAR_ENTER_QUEUE_BOX_HIRE_FULL_HIRE_NOTIFY, '%s') % hnum
                elif num:
                    if pnum:
                        if queueType == uiConst.WW_QUEUE_TYPE_BATTLE and not isInArmy and isMinLv:
                            return uiUtils.getTextFromGMD(GMDD.data.WORLD_WAR_ENTER_QUEUE_BOX_FULL_NOTIFY_YOUNG) % (groupType, pnum + oldNum, youngNum)
                        return uiUtils.getTextFromGMD(GMDD.data.WORLD_WAR_ENTER_QUEUE_BOX_FULL_NOTIFY) % (groupType, pnum, num)
                    elif queueType == uiConst.WW_QUEUE_TYPE_BATTLE and not isInArmy and isMinLv:
                        return uiUtils.getTextFromGMD(GMDD.data.WORLD_WAR_ENTER_QUEUE_BOX_FULL_NOTIFY_YOUNG) % (groupType, oldNum, youngNum)
                    else:
                        return uiUtils.getTextFromGMD(GMDD.data.WORLD_WAR_ENTER_QUEUE_BOX_FULL_NO_ARMY_NOTIFY) % (groupType, num)
                else:
                    return uiUtils.getTextFromGMD(GMDD.data.WORLD_WAR_ENTER_QUEUE_BOX_FULL_ARMY_NOTIFY) % (groupType, pnum)
            elif num:
                if pnum:
                    if queueType == uiConst.WW_QUEUE_TYPE_BATTLE and not isInArmy and isMinLv:
                        return uiUtils.getTextFromGMD(GMDD.data.WORLD_WAR_ENTER_QUEUE_BOX_NOTIFY_YOUNG) % (groupType, pnum + oldNum, youngNum)
                    return uiUtils.getTextFromGMD(GMDD.data.WORLD_WAR_ENTER_QUEUE_BOX_NOTIFY) % (groupType, pnum, num)
                elif queueType == uiConst.WW_QUEUE_TYPE_BATTLE and not isInArmy and isMinLv:
                    return uiUtils.getTextFromGMD(GMDD.data.WORLD_WAR_ENTER_QUEUE_BOX_NOTIFY_YOUNG) % (groupType, oldNum, youngNum)
                else:
                    return uiUtils.getTextFromGMD(GMDD.data.WORLD_WAR_ENTER_QUEUE_BOX_NO_ARMY_NOTIFY) % (groupType, num)
            else:
                return uiUtils.getTextFromGMD(GMDD.data.WORLD_WAR_ENTER_QUEUE_BOX_ARMY_NOTIFY) % (groupType, pnum)
        elif queueType == uiConst.WW_QUEUE_TYPE_ROB or queueType == uiConst.WW_QUEUE_TYPE_ROB_YOUNG:
            if self.robStateDict[queueType] in gametypes.WW_ROB_STATE_ENTER_SET:
                if num:
                    if pnum:
                        if queueType == uiConst.WW_QUEUE_TYPE_ROB and not isInArmy and isMinLv:
                            return uiUtils.getTextFromGMD(GMDD.data.WORLD_WAR_ROB_ENTER_QUEUE_BOX_FULL_NOTIFY_YOUNG) % (groupType, pnum + oldNum, youngNum)
                        return uiUtils.getTextFromGMD(GMDD.data.WORLD_WAR_ROB_ENTER_QUEUE_BOX_FULL_NOTIFY) % (groupType, pnum, num)
                    elif queueType == uiConst.WW_QUEUE_TYPE_ROB and not isInArmy and isMinLv:
                        return uiUtils.getTextFromGMD(GMDD.data.WORLD_WAR_ROB_ENTER_QUEUE_BOX_FULL_NOTIFY_YOUNG) % (groupType, oldNum, youngNum)
                    else:
                        return uiUtils.getTextFromGMD(GMDD.data.WORLD_WAR_ROB_ENTER_QUEUE_BOX_FULL_NO_ARMY_NOTIFY) % (groupType, num)
                else:
                    return uiUtils.getTextFromGMD(GMDD.data.WORLD_WAR_ROB_ENTER_QUEUE_BOX_FULL_ARMY_NOTIFY) % (groupType, pnum)
            elif num:
                if pnum:
                    if queueType == uiConst.WW_QUEUE_TYPE_ROB and not isInArmy and isMinLv:
                        return uiUtils.getTextFromGMD(GMDD.data.WORLD_WAR_ROB_ENTER_QUEUE_BOX_NOTIFY_YOUNG) % (groupType, pnum + oldNum, youngNum)
                    return uiUtils.getTextFromGMD(GMDD.data.WORLD_WAR_ROB_ENTER_QUEUE_BOX_NOTIFY) % (groupType, pnum, num)
                elif queueType == uiConst.WW_QUEUE_TYPE_ROB and not isInArmy and isMinLv:
                    return uiUtils.getTextFromGMD(GMDD.data.WORLD_WAR_ROB_ENTER_QUEUE_BOX_NOTIFY_YOUNG) % (groupType, oldNum, youngNum)
                else:
                    return uiUtils.getTextFromGMD(GMDD.data.WORLD_WAR_ROB_ENTER_QUEUE_BOX_NO_ARMY_NOTIFY) % (groupType, num)
            else:
                return uiUtils.getTextFromGMD(GMDD.data.WORLD_WAR_ROB_ENTER_QUEUE_BOX_ARMY_NOTIFY) % (groupType, pnum)
        elif num:
            if pnum:
                return uiUtils.getTextFromGMD(GMDD.data.WORLD_WAR_NORMAL_ENTER_QUEUE_BOX_FULL_NOTIFY) % (pnum, num)
            else:
                return uiUtils.getTextFromGMD(GMDD.data.WORLD_WAR_NORMAL_ENTER_QUEUE_BOX_FULL_NO_ARMY_NOTIFY) % num
        else:
            return uiUtils.getTextFromGMD(GMDD.data.WORLD_WAR_NORMAL_ENTER_QUEUE_BOX_FULL_ARMY_NOTIFY) % pnum

    def showBattleQueueMsg(self, wwType):
        p = BigWorld.player()
        pnum, oldNum, youngNum, hnum = self.wwqorders.get(wwType, (0, 0, 0, 0))
        num = sum([oldNum, youngNum])
        isMinLv = False
        isInArmy = self.getPostByGbId(p.gbId)
        if p.lv == const.WORLD_WAR_ARMY_MINLV:
            isMinLv = True
        if self.battleState == gametypes.WORLD_WAR_BATTLE_STATE_OPEN:
            if (p.wbApplyHireHostId or p.wbHireHostId) and hnum:
                p.showGameMsg(GMDD.data.WORLD_WAR_ENTER_QUEUE_BOX_HIRE_FULL_HIRE_NOTIFY, (hnum,))
            elif num:
                if wwType == uiConst.WW_QUEUE_TYPE_BATTLE and not isInArmy and isMinLv:
                    p.showGameMsg(GMDD.data.WORLD_WAR_ENTER_QUEUE_FULL_NOTIFY_YOUNG, (pnum + oldNum, youngNum))
                else:
                    p.showGameMsg(GMDD.data.WORLD_WAR_ENTER_QUEUE_FULL_NOTIFY, (pnum, num))
            else:
                p.showGameMsg(GMDD.data.WORLD_WAR_ENTER_QUEUE_FULL_ARMY_NOTIFY, (pnum,))
        elif num:
            if wwType == uiConst.WW_QUEUE_TYPE_BATTLE and not isInArmy and isMinLv:
                p.showGameMsg(GMDD.data.WORLD_WAR_ENTER_QUEUE_NOTIFY_YOUNG, (pnum + oldNum, youngNum))
            else:
                p.showGameMsg(GMDD.data.WORLD_WAR_ENTER_QUEUE_NOTIFY, (pnum, num))
        else:
            p.showGameMsg(GMDD.data.WORLD_WAR_ENTER_QUEUE_ARMY_NOTIFY, (pnum,))

    def inVotePhase(self):
        return self.armyState == gametypes.WORLD_WAR_ARMY_STATE_VOTE or self.voteResultEndTime > utils.getNow()

    def clearMpUsed(self):
        for post in self.army.itervalues():
            post.mpUsed = 0

    def getRobBindCash(self):
        return commonWorldWar.calcRobBindCash(self.totalRobScore, self.robScore, self.robZaiju.mineRobRes + WWCD.data.get('robMinRes', 1000000), self.totalRobAttends)
