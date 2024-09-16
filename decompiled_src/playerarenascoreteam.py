#Embedded file name: /WORKSPACE/data/entities/common/playerarenascoreteam.o
import copy
import const
from userSoleType import UserSoleType
from userDictType import UserDictType
from data import duel_config_data as DCD

class PlayerArenaScoreTeamVal(UserSoleType):

    def __init__(self, teamType = 0, teamNUID = 0, headGBID = 0, stage = 0):
        self.teamType = teamType
        self.teamNUID = teamNUID
        self.headGBID = headGBID
        self.stage = stage

    def clear(self):
        self.teamType = 0
        self.teamNUID = 0
        self.headGBID = 0
        self.stage = 0


class PlayerArenaScoreTeam(UserDictType):

    def _lateReload(self):
        super(PlayerArenaScoreTeam, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()


class PlayerArenaScoreScoreVal(UserSoleType):

    def __init__(self, teamType = 0, score = 0, dailyScore = 0, totalCnt = 0, dailyLoseCnt = 0, rewarded = {}, tTime = 0):
        self.teamType = teamType
        self.score = score
        self.dailyScore = dailyScore
        self.totalCnt = totalCnt
        self.dailyLoseCnt = dailyLoseCnt
        self.rewarded = copy.deepcopy(rewarded)
        self.tTime = tTime

    def clear(self):
        self.score = 0
        self.totalCnt = 0
        self.dailyScore = 0
        self.dailyLoseCnt = 0
        self.rewarded.clear()
        self.tTime = 0

    def onDaily(self):
        self.dailyScore = 0
        self.dailyLoseCnt = 0
        for rewardId in self.rewarded.keys():
            rewardCfg = DCD.data.get('arenaScorePlayerAward', {}).get(rewardId)
            if rewardCfg and rewardCfg[0] in const.ARENA_SCORE_PLAYER_REWARD_TYPES_DAILY and self.rewarded[rewardId]:
                self.rewarded[rewardId] = False

    def getDTO(self):
        return {'score': self.score,
         'totalCnt': self.totalCnt,
         'dailyScore': self.dailyScore,
         'dailyLoseScore': self.dailyLoseCnt,
         'rewarded': self.rewarded,
         'tTimer': self.tTime}


class PlayerArenaScoreScore(UserDictType):

    def _lateReload(self):
        super(PlayerArenaScoreScore, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()
