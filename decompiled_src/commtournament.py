#Embedded file name: /WORKSPACE/data/entities/common/commtournament.o
import time
import copy
import const
import utils
from userSoleType import UserSoleType
from userDictType import UserDictType

def getWeekNum(wt = 0):
    wt = wt or utils.getWeekSecond()
    mval = time.localtime(wt)[1]
    wnum = 1
    while True:
        wt -= const.TIME_INTERVAL_WEEK
        if time.localtime(wt)[1] != mval:
            break
        wnum += 1

    return wnum


class CrossTournamentRecordVal(UserSoleType):

    def __init__(self, guildNUID = 0, guildName = '', hostId = '', groupScore = 0, playoffScore = 0, rank = 0, groupScoresDict = {}, playoffScoresDict = {}, circularScore = 0, circularScoreDict = {}, guildRank = 0, playoffWinNum = 0, circularWinNum = 0):
        self.guildNUID = guildNUID
        self.guildName = guildName
        self.hostId = hostId
        self.groupScore = groupScore
        self.playoffScore = playoffScore
        self.groupScoresDict = copy.copy(groupScoresDict)
        self.playoffScoresDict = copy.copy(playoffScoresDict)
        self.playoffWinNum = playoffWinNum
        self.rank = rank
        self.circularScore = circularScore
        self.circularScoreDict = circularScoreDict
        self.circularWinNum = circularWinNum
        self.guildRank = guildRank

    def getDTO(self):
        return (self.guildNUID,
         self.guildName,
         self.hostId,
         self.groupScore,
         self.playoffScore,
         self.rank,
         self.circularScore)

    def fromDTO(self, dto):
        self.guildNUID, self.guildName, self.hostId, self.groupScore, self.playoffScore, self.rank, self.circularScore = dto
        return self


class BaseCrossTournamentVal(UserDictType):

    def _getGroupMatchPairs(self, idx, roundNum):
        if len(self.groupGuildNUIDs) <= idx:
            return ((0, 0), (0, 0))
        guildNUIDs = list(self.groupGuildNUIDs[idx])
        g1 = guildNUIDs.pop(roundNum)
        g2 = guildNUIDs.pop(0)
        return ((g2, g1), tuple(guildNUIDs))
