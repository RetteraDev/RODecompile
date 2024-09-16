#Embedded file name: /WORKSPACE/data/entities/client/helpers/tournament.o
import copy
import utils
import const
import gametypes
import commTournament
from userDictType import UserDictType
from commTournament import CrossTournamentRecordVal, BaseCrossTournamentVal
from cdata import rank_guild_tournament_star_data as RGTSD

class SubGroupVal(object):

    def __init__(self, subGroupId = 0, isSeed = False, hasApplied = False, canEnter = False, isInMatches = False):
        self.isSeed = isSeed
        self.hasApplied = hasApplied
        self.canEnter = canEnter
        self.isInMatches = isInMatches


class TournamentVal(object):

    def __init__(self, groupId = 0, guild = {}, matches = [], ranks = [], seedGuildNUIDs = [], state = 0, roundNum = 0, ver = 0, rankVer = 0, isSeed = False, hasApplied = False, canEnter = False, appliedSeedNum = 0, simpleVer = 0, isInMatches = False):
        self.groupId = groupId
        self.guild = copy.deepcopy(guild)
        self.matches = copy.deepcopy(matches)
        self.ranks = copy.deepcopy(ranks)
        self.seedGuildNUIDs = copy.deepcopy(seedGuildNUIDs)
        self.state = state
        self.roundNum = roundNum
        self.ver = ver
        self.rankVer = ver
        self.isSeed = isSeed
        self.hasApplied = hasApplied
        self.canEnter = canEnter
        self.appliedSeedNum = appliedSeedNum
        self.simpleVer = simpleVer
        self.isInMatches = isInMatches
        self.trainingState = gametypes.GUILD_TOURNAMENT_TRAINING_STATE_CLOSE
        self.trainingAppliesByNuid = {}
        self.subGroups = {0: SubGroupVal(subGroupId=0),
         1: SubGroupVal(subGroupId=1)}

    def getSubGroup(self, subGroupId):
        if self.subGroups.has_key(subGroupId):
            return self.subGroups[subGroupId]
        else:
            subGroup = SubGroupVal(subGroupId=subGroupId)
            self.subGroups[subGroupId] = subGroup
            return subGroup

    def getTop4(self):
        r = [0] * 4
        if self.roundNum == const.GUILD_TOURNAMENT_MAX_ROUND and len(self.matches) == const.GUILD_TOURNAMENT_MAX_ROUND + 1:
            r[0] = self.matches[-1][0]
            if r[0]:
                for i in (0, 1):
                    if self.matches[-2][i] != r[0]:
                        r[1] = self.matches[-2][i]
                        break

            r[2] = self.matches[-1][1]
            if r[2]:
                r[2] = self.matches[-1][1]
                for i in (2, 3):
                    if self.matches[-2][i] != r[2]:
                        r[3] = self.matches[-2][i]
                        break

        return r


class TournamentRankVal(object):

    def __init__(self, rank = 0, guildNUID = 0, guildName = '', score = 0, totalScore = 0):
        self.rank = rank
        self.score = score
        self.totalScore = totalScore
        self.guildNUID = guildNUID
        self.guildName = guildName


class GuildTournament(UserDictType):

    def __init__(self):
        for groupId in gametypes.GUILD_TOURNAMENT_GROUP:
            self[groupId] = TournamentVal(groupId=groupId)


class CrossTournamentVal(BaseCrossTournamentVal):

    def __init__(self, tWhen = 0, groupId = 0, state = 0, guild = {}, groupGuildNUIDs = [], groupRoundNum = 0, groupMatchResult = {}, playoffMatches = [], playoffRoundNum = 0, playoffMatchResult = [], top4 = [], isCandidate = False, canEnter = False, simpleVer = 0, ver = 0):
        self.tWhen = tWhen
        self.groupId = groupId
        self.guild = copy.deepcopy(guild)
        self.state = state
        self.groupGuildNUIDs = copy.deepcopy(groupGuildNUIDs)
        self.groupRoundNum = groupRoundNum
        self.groupMatchResult = copy.deepcopy(groupMatchResult)
        self.playoffMatches = copy.deepcopy(playoffMatches)
        self.playoffRoundNum = copy.deepcopy(playoffRoundNum)
        self.playoffMatchResult = copy.deepcopy(playoffMatchResult)
        self.isCandidate = (isCandidate,)
        self.top4 = (copy.deepcopy(top4),)
        self.canEnter = canEnter
        self.simpleVer = simpleVer
        self.ver = ver
        self.mode = 0
        self.circularRoundNum = 0
        self.circularMatchResult = {}
        self.circularTroopNUID = 0
        self.circularGuildNUIDs = ()

    def fromDTO(self, dto):
        self.tWhen, self.state, self.top4, self.groupGuildNUIDs, self.groupMatchResult, self.groupRoundNum, self.playoffMatches, self.playoffMatchResult, self.playoffRoundNum, recordDTOs, self.mode, self.circularRoundNum, self.circularMatchResult, self.circularTroopNUID, self.circularGuildNUIDs = dto
        self.guild = {}
        for rdto in recordDTOs:
            r = CrossTournamentRecordVal().fromDTO(rdto)
            self.guild[r.guildNUID] = r

        return self

    def _getMonthId(self):
        return utils.getMonthSecond(self._getWeekId())

    def _getWeekId(self, t = None):
        return utils.getWeekSecond(t)

    def getWeekNum(self):
        return commTournament.getWeekNum()


class CrossGuildTournament(UserDictType):

    def __init__(self):
        for groupId in gametypes.GUILD_TOURNAMENT_GROUP:
            self[groupId] = CrossTournamentVal(groupId=groupId)


def getRankStarKey(groupId, groupScore):
    for k, v in RGTSD.data.iteritems():
        if groupId == k[2]:
            if k[0] <= groupScore <= k[1]:
                return k

    return 0


def getRankStarText(groupId, groupScore):
    rankKey = getRankStarKey(groupId, groupScore)
    starText = RGTSD.data.get(rankKey, {}).get('name', '')
    return starText


class CrossRankTournamentVal(BaseCrossTournamentVal):

    def __init__(self, tWhen = 0, groupId = 0, state = 0, isCandidate = False, canEnter = False, simpleVer = 0, ver = 0):
        self.tWhen = tWhen
        self.groupId = groupId
        self.state = state
        self.isCandidate = (isCandidate,)
        self.canEnter = canEnter
        self.simpleVer = simpleVer
        self.matchInfo = {}
        self.rank = 0
        self.groupScore = 0
        self.ver = ver
        self.bonus = 0
        self.hasApplied = False
        self.roundNum = 0

    def getRankStarKey(self):
        return getRankStarKey(self.groupId, self.groupScore)


class CrossRankGuildTournament(UserDictType):

    def __init__(self):
        for groupId in gametypes.GUILD_TOURNAMENT_GROUP:
            self[groupId] = CrossRankTournamentVal(groupId=groupId)
