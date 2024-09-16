#Embedded file name: I:/bag/tmp/tw2/res/entities\common/worldChallenge.o
import utils
from userDictType import UserDictType
from userSoleType import UserSoleType

class WorldChallengeVal(UserSoleType):

    def __init__(self, curScore = 0, highestScore = 0, highestScoreTime = 0, bComplete = False):
        self.bComplete = bComplete
        self.curScore = curScore
        self.highestScore = highestScore
        self.highestScoreTime = highestScoreTime

    def setCurScore(self, curScore):
        self.curScore = curScore

    def setHighestScore(self, highestScore):
        self.highestScore = highestScore
        self.highestScoreTime = utils.getNow()

    def _lateReload(self):
        super(WorldChallengeVal, self)._lateReload()


class WorldChallenge(UserDictType):

    def __init__(self):
        super(WorldChallenge, self).__init__()
        self.acceptChallenges = {}
        self.groupCompleteTimes = {}

    def addChallengeVal(self, challengeId, curScore = 0, highestScore = 0, highestScoreTime = 0, bComplete = False):
        val = WorldChallengeVal(curScore, highestScore, highestScoreTime, bComplete)
        self.acceptChallenges[challengeId] = val

    def setGroupTimes(self, groupId, completeTimes):
        self.groupCompleteTimes[groupId] = completeTimes

    def addGroupTimes(self, groupId):
        if not self.groupCompleteTimes.has_key(groupId):
            self.groupCompleteTimes[groupId] = 0
        self.groupCompleteTimes[groupId] += 1

    def _lateReload(self):
        for k, v in self.acceptChallenges.iteritems():
            if hasattr(v, 'reloadScript'):
                v.reloadScript()

        for k, v in self.groupCompleteTimes.iteritems():
            if hasattr(v, 'reloadScript'):
                v.reloadScript()
