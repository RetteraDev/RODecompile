#Embedded file name: I:/bag/tmp/tw2/res/entities\common/worldChallengeInfo.o
from userInfo import UserInfo
from worldChallenge import WorldChallenge

class WorldChallengeInfo(UserInfo):

    def isSameType(self, obj):
        return type(obj) is WorldChallenge

    def createObjFromDict(self, dictVal):
        obj = WorldChallenge()
        if dictVal.has_key('acceptChallenges') and dictVal['acceptChallenges']:
            for value in dictVal['acceptChallenges']:
                obj.addChallengeVal(value['challengeId'], value['curScore'], value['highestScore'], value['highestScoreTime'], value['bComplete'])

        if dictVal.has_key('groupCompleteTimes') and dictVal['groupCompleteTimes']:
            for key, value in dictVal['groupCompleteTimes'].iteritems():
                obj.setGroupTimes(key, value)

        return obj

    def getDictFromObj(self, obj):
        result = {}
        challengeIds = []
        for key, value in obj.acceptChallenges.iteritems():
            curScore = value.curScore
            highestScore = value.highestScore
            highestScoreTime = value.highestScoreTime
            bComplete = value.bComplete
            challengeIds.append({'challengeId': key,
             'curScore': curScore,
             'highestScore': highestScore,
             'highestScoreTime': highestScoreTime,
             'bComplete': bComplete})

        result['acceptChallenges'] = challengeIds
        result['groupCompleteTimes'] = obj.groupCompleteTimes
        return result


instance = WorldChallengeInfo()
