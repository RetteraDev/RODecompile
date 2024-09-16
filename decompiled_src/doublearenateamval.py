#Embedded file name: /WORKSPACE/data/entities/common/doublearenateamval.o
import utils
import const
import gamelog
import const
import copy
import random
import math
from userSoleType import UserSoleType
from data import duel_config_data as DCD

class DoubleArenaTeamVal(UserSoleType):

    def __init__(self, teamName = '', hostId = 0, playerOne = None, playerTwo = None, statistics = None, camp = 0, relation = 0):
        self.teamName = teamName
        self.hostId = hostId
        self.playerOne = playerOne
        self.playerTwo = playerTwo
        self.statistics = statistics
        self.camp = camp
        self.relation = relation

    def _lateReload(self):
        super(DoubleArenaTeamVal, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()

    def checkLeaderGbId(self, gbId):
        if gbId == self.playerOne.gbId or gbId == self.playerTwo.gbId:
            return self.playerOne.gbId

    def getTeamMateGbId(self):
        return [self.playerOne.gbId, self.playerTwo.gbId]

    def hasGbId(self, gbIds):
        return self.playerOne.gbId in gbIds or self.playerTwo.gbId in gbIds

    def hasName(self, teamName):
        return self.teamName == teamName

    def getMaxCheers(self):
        return self.statistics.getMaxDayCheers()

    def addCheersNum(self):
        return self.statistics.addCheersNum()

    def refreshCheers(self):
        self.statistics.refreshCheers()

    def setStatistics(self, statistics):
        self.statistics = statistics

    def calcStatistics(self, statisInfo):
        return self.statistics.calcStatistics(statisInfo)

    def calcTeamScore(self, scoreInfo):
        return self.statistics.calcTeamScore(scoreInfo)

    def checkVersion(self, version):
        return self.statistics.checkVersion(version)

    def cheekCheers(self):
        return self.statistics.cheekCheers()

    def checkDisband(self):
        return self.statistics.checkDisband()

    def addScore(self, score):
        self.statistics.addScore(score)

    def getComboWins(self):
        return self.statistics.comboWins

    def setLastRank(self, rank):
        self.statistics.lastRank = rank

    def cmpLastRank(self, rank):
        return rank < self.statistics.lastRank

    def getRoleNameByGbId(self, gbId):
        if gbId == self.playerOne.gbId:
            return self.playerOne.roleName
        if gbId == self.playerTwo.gbId:
            return self.playerTwo.roleName
        return ''

    def clearGM(self):
        return self.statistics.clearGM()

    def genTeamLog(self):
        return (self.playerOne.gbId,
         self.playerTwo.gbId,
         self.teamName,
         self.camp,
         self.relation)

    def genMergeHostVals(self):
        return (self.playerOne.gbId,
         self.playerOne.roleName,
         self.playerTwo.gbId,
         self.playerTwo.roleName,
         self.teamName,
         self.camp,
         self.relation)


class DoubleArenaStatisticsVal(UserSoleType):

    def __init__(self, killCnt = 0, assistCnt = 0, damageVal = 0, cureVal = 0, beDamageVal = 0, totalCheers = 0, todayCheers = 0, cheersTimeStamp = utils.getNow(), usedCheer = 0, fights = 0, wins = 0, comboWins = 0, version = 0, troopNUID = 0, createTime = utils.getNow()):
        self.killCnt = killCnt
        self.assistCnt = assistCnt
        self.damageVal = damageVal
        self.cureVal = cureVal
        self.beDamageVal = beDamageVal
        self.totalCheers = totalCheers
        self.todayCheers = todayCheers
        self.usedCheers = usedCheer
        self.cheersTimeStamp = cheersTimeStamp
        self.score = DCD.data.get('dArenaInitScore', 0)
        self.fights = fights
        self.wins = wins
        self.comboWins = comboWins
        self.version = version
        self.troopNUID = troopNUID
        self.createTime = createTime
        self.todayFights = 0
        self.totalFights = 0
        self.fightsTimeStamp = 0
        self.lastRank = 0

    def _lateReload(self):
        super(DoubleArenaStatisticsVal, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()

    def getMaxDayCheers(self):
        self.refreshCheers()
        dArenaTotalCheersLimit = DCD.data.get('dArenaTotalCheersLimit', 30)
        dArenaDayCheersLimit = DCD.data.get('dArenaDayCheersLimit', 6)
        return min(dArenaTotalCheersLimit - self.totalCheers, dArenaDayCheersLimit)

    def refreshCheers(self):
        if utils.isSameDay(self.cheersTimeStamp):
            return
        self.cheersTimeStamp = utils.getNow()
        self.totalCheers += self.todayCheers
        self.todayCheers = self.usedCheers = 0

    def refreshFights(self):
        if utils.isSameDay(self.fightsTimeStamp):
            return
        self.fightsTimeStamp = utils.getNow()
        self.todayFights = 0

    def addCheersNum(self):
        maxCheers = self.getMaxDayCheers()
        if self.todayCheers >= maxCheers:
            return False
        self.refreshCheers()
        self.todayCheers += 1
        self.version += 1
        return True

    def addScore(self, score):
        self.version += 1
        self.score += score

    def calcStatistics(self, statisInfo):
        self.killCnt += statisInfo.get('murderer', 0)
        self.assistCnt += statisInfo.get('assistCount', 0)
        self.damageVal += statisInfo.get('damage', 0)
        self.cureVal += statisInfo.get('cure', 0)
        self.beDamageVal += statisInfo.get('beDamage', 0)

    def calcTeamScore(self, scoreInfo):
        self.version += 1
        self.refreshFights()
        self.refreshCheers()
        hasBuff = scoreInfo.get('buff', False)
        result = scoreInfo.get('result', 0)
        if hasBuff:
            self.usedCheers += 1
        self.fights += 1
        score, state = self.calcFightScore(scoreInfo)
        if result in const.WIN_FLAG:
            self.score += score
            self.wins += 1
            self.comboWins += 1
        elif result == const.TIE:
            self.score += score
        elif result in const.LOSE_FLAG:
            self.score += score
            self.comboWins = 0
        return (score, state, self.todayFights)

    def calcFightScore(self, statisInfo):
        dArenaDayFightLimit = DCD.data.get('dArenaDayFightLimit', 10)
        dArenaTotalFightLimit = DCD.data.get('dArenaTotalFightLimit', 50)
        if self.todayFights >= dArenaDayFightLimit or self.totalFights >= dArenaTotalFightLimit:
            return (0, const.DOUBLE_ARENA_TEAM_FIGHT_LIMIT)
        self.todayFights += 1
        self.totalFights += 1
        result = statisInfo.get('result', 0)
        hasBuff = statisInfo.get('buff', False)
        if result in const.WIN_FLAG:
            if hasBuff:
                return (DCD.data.get('dArenaWinScore', 0) * 2, const.DOUBLE_ARENA_TEAM_FIGHT_NORMAL)
            return (DCD.data.get('dArenaWinScore', 0), const.DOUBLE_ARENA_TEAM_FIGHT_NORMAL)
        if result == const.TIE:
            if hasBuff:
                return (0, const.DOUBLE_ARENA_TEAM_FIGHT_NORMAL)
            return (DCD.data.get('dArenaTieScore', 0), const.DOUBLE_ARENA_TEAM_FIGHT_NORMAL)
        if result in const.LOSE_FLAG:
            if hasBuff:
                return (0, const.DOUBLE_ARENA_TEAM_FIGHT_NORMAL)
            return (DCD.data.get('dArenaLoseScore', 0), const.DOUBLE_ARENA_TEAM_FIGHT_NORMAL)

    def checkVersion(self, version):
        return self.version < version

    def cheekCheers(self):
        self.refreshCheers()
        return self.todayCheers > self.usedCheers

    def checkDisband(self):
        dArenaDisbandCD = DCD.data.get('dArenaDisbandCD', 43200)
        if self.createTime + dArenaDisbandCD > utils.getNow():
            return False
        return True

    def clearGM(self):
        self.refreshCheers()
        self.refreshFights()
        self.killCnt = 0
        self.assistCnt = 0
        self.damageVal = 0
        self.cureVal = 0
        self.beDamageVal = 0
        self.score = DCD.data.get('dArenaInitScore', 0)
        self.fights = 0
        self.wins = 0
        self.comboWins = 0
        self.version += 1
        self.troopNUID = 0
        self.todayFights = 0
        self.totalFights = 0
        self.lastRank = 0


class DoubleArenaPlayerVal(UserSoleType):

    def __init__(self, gbId = 0, roleName = ''):
        self.gbId = gbId
        self.roleName = roleName

    def _lateReload(self):
        super(DoubleArenaPlayerVal, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()


class DoubleArenaApplyingVal(UserSoleType):

    def __init__(self, teamName = '', gbIds = [], timeStamp = 0):
        self.teamName = teamName
        self.gbIds = gbIds
        confirmTime = DCD.data.get('dArenaTeamConfirmTime', 60)
        self.timeStamp = timeStamp + confirmTime

    def _lateReload(self):
        super(DoubleArenaApplyingVal, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()

    def hasGbId(self, gbIds):
        tmp = [ val for val in self.gbIds if val in gbIds ]
        return len(tmp) != 0

    def isExpired(self):
        return utils.getNow() > self.timeStamp

    def hasName(self, teamName):
        return self.teamName == teamName

    def isSameGbId(self, gbIds):
        tmp = [ val for val in self.gbIds if val in gbIds ]
        return len(tmp) == len(gbIds)


class DoubleArenaPlayOffVal(UserSoleType):

    def __init__(self, teamList = {}, version = 0, stage = {}, roundNum = 0, beginTime = 0, endTime = 0):
        self.teamList = copy.deepcopy(teamList)
        self.version = version
        self.stage = copy.deepcopy(stage)
        self.roundNum = roundNum
        self.beginTime = beginTime
        self.endTime = endTime
        self.nowTroop = []

    def pushTroop(self, troopNUID):
        if troopNUID not in self.nowTroop:
            self.nowTroop.append(troopNUID)

    def popTroop(self, troopNUID):
        if troopNUID in self.nowTroop:
            self.nowTroop.remove(troopNUID)

    def checkTroop(self, troopNUID):
        return troopNUID in self.nowTroop

    def pushTeam(self, teamVal):
        if not type(teamVal) == DoubleArenaPlayOffTeamVal:
            return
        self.teamList[teamVal.gbId] = teamVal

    def getTeam(self, gbId):
        return self.teamList.get(gbId, None)

    def initStage(self, rankPool):
        self.version = 1
        for i in xrange(const.DOUBLE_ARENA_PLAYOFF_INIT_STAGE, const.DOUBLE_ARENA_PLAYOFF_FINAL_STAGE):
            self.stage[i] = {}

        temp = [[],
         [],
         [],
         []]
        indexes = [ i for i in xrange(const.DOUBLE_ARENA_PLAYOFF_RANK_NUM) ]
        for camp, val in enumerate(rankPool):
            random.shuffle(indexes)
            for idx, gbId in enumerate(val):
                temp[indexes[idx]].append(gbId)

        for i in xrange(1, 9):
            self.stage[1][i] = []

        for camp, val in enumerate(temp):
            groupNo = camp * 2 + 1
            for idx, gbId in enumerate(val):
                self.stage[1][groupNo + idx / 2].append(gbId)

    def refreshStage(self, gbId):
        group = 0
        for key, gbIds in self.stage[self.roundNum].iteritems():
            if gbId not in gbIds:
                continue
            group = key
            break

        if not group:
            return
        newGroup = int(math.ceil(group / 2.0))
        if newGroup not in self.stage[self.nextRound()]:
            self.stage[self.nextRound()][newGroup] = [gbId]
        elif gbId not in self.stage[self.nextRound()][newGroup]:
            self.stage[self.nextRound()][newGroup].append(gbId)
        self.version += 1

    def resetStageGM(self, targetStage):
        if targetStage > self.roundNum:
            return
        self.version += 1
        for i in xrange(targetStage + 1, const.DOUBLE_ARENA_PLAYOFF_FINAL_STAGE):
            self.stage[i] = {}

        self.roundNum = targetStage - 1
        self.beginTime = 0
        self.endTime = 0
        self.nowTroop = []

    def setTeamStateGM(self, gbId, op):
        if gbId not in self.teamList:
            return
        if self.roundNum >= 4:
            return
        if op == 1:
            group = 0
            for key, gbIds in self.stage[self.nextRound()].iteritems():
                if gbId not in gbIds:
                    continue
                group = key
                break

            if not group:
                return
            newGroup = int(math.ceil(group / 2.0))
            if newGroup not in self.stage[self.nextRound() + 1]:
                self.stage[self.nextRound() + 1][newGroup] = [gbId]
            elif gbId not in self.stage[self.nextRound() + 1][newGroup]:
                self.stage[self.nextRound() + 1][newGroup].append(gbId)
        elif op == 0:
            for groupNo, gbIds in self.stage.get(self.nextRound() + 1, {}).iteritems():
                if gbId not in gbIds:
                    continue
                gbIds.remove(gbId)
                break

        self.version += 1

    def getFinalRank(self):
        temp = []
        stage = {}
        for i in xrange(const.DOUBLE_ARENA_PLAYOFF_INIT_STAGE, const.DOUBLE_ARENA_PLAYOFF_FINAL_STAGE):
            stage[i] = []

        for i in xrange(const.DOUBLE_ARENA_PLAYOFF_FINAL_STAGE - 1, const.DOUBLE_ARENA_PLAYOFF_INIT_STAGE - 1, -1):
            for group, gbIds in self.stage[i].iteritems():
                for gbId in gbIds:
                    if gbId in temp:
                        continue
                    stage[i].append(gbId)
                    temp.append(gbId)

        return stage

    def nextRound(self):
        return self.roundNum + 1

    def getStageInfo(self):
        return self.stage[self.roundNum]

    def setRoundTime(self):
        self.roundNum += 1
        self.nowTroop = []
        self.beginTime = utils.getNow()
        self.endTime = self.beginTime + DCD.data.get('dArenaPrepareTime', 600)
        self.version += 1

    def checkTime(self):
        return self.beginTime < utils.getNow() < self.endTime

    def setTroopNUID(self, gbId, troopNUID):
        if gbId not in self.teamList:
            return
        self.teamList[gbId].setTroopNUID(troopNUID)

    def getTroopNUID(self, gbId):
        if gbId not in self.teamList:
            return 0
        return self.teamList[gbId].getTroopNUID()

    def setFbNo(self, gbId, fbNo):
        if gbId not in self.teamList:
            return
        self.teamList[gbId].setFbNo(fbNo)

    def getFbNo(self, gbId):
        if gbId not in self.teamList:
            return 0
        return self.teamList[gbId].getFbNo()

    def setAnnalUUID(self, gbId, annalUUID):
        if gbId not in self.teamList:
            return
        self.teamList[gbId].setAnnalUUID(annalUUID)

    def getAnnalUUID(self, gbId):
        if gbId not in self.teamList:
            return 0
        return self.teamList[gbId].getAnnalUUID()

    def setSpaceNo(self, gbId, spaceNo):
        if gbId not in self.teamList:
            return
        self.teamList[gbId].setSpaceNo(spaceNo)

    def getSpaceNo(self, gbId):
        if gbId not in self.teamList:
            return 0
        return self.teamList[gbId].getSpaceNo()


class DoubleArenaPlayOffTeamVal(UserSoleType):

    def __init__(self, gbId = 0, teamName = '', camp = 0, leaderName = '', mateName = '', troopNUID = 0, fbNo = 0, annalUUID = 0, spaceNo = 0):
        self.gbId = gbId
        self.teamName = teamName
        self.camp = camp
        self.leaderName = leaderName
        self.mateName = mateName
        self.troopNUID = troopNUID
        self.fbNo = fbNo
        self.annalUUID = annalUUID
        self.spaceNo = spaceNo

    def setTroopNUID(self, troopNUID):
        self.troopNUID = troopNUID

    def getTroopNUID(self):
        return self.troopNUID

    def setFbNo(self, fbNo):
        self.fbNo = fbNo

    def getFbNo(self):
        return self.fbNo

    def setAnnalUUID(self, annalUUID):
        self.annalUUID = annalUUID

    def getAnnalUUID(self):
        return self.annalUUID

    def setSpaceNo(self, spaceNo):
        self.spaceNo = spaceNo

    def getSpaceNo(self):
        return self.spaceNo


class DoubleArenaSpecialFight(UserSoleType):

    def __init__(self, msgId = 0, winTeam = '', loseTeam = '', val = '', timeStamp = 0, camp = 0):
        self.msgId = msgId
        self.winTeam = winTeam
        self.loseTeam = loseTeam
        self.val = val
        self.timeStamp = timeStamp
        self.camp = camp

    def getDTO(self):
        return (self.msgId,
         self.winTeam,
         self.loseTeam,
         self.val,
         self.timeStamp,
         self.camp)

    def fromDTO(self, dto):
        self.msgId, self.winTeam, self.loseTeam, self.val, self.timeStamp, self.camp = dto
        return self
