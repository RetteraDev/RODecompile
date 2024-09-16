#Embedded file name: /WORKSPACE/data/entities/common/playerarenascoreteaminfo.o
from userInfo import UserInfo
from playerArenaScoreTeam import PlayerArenaScoreTeamVal, PlayerArenaScoreTeam, PlayerArenaScoreScoreVal, PlayerArenaScoreScore

class PlayerArenaScoreTeamInfo(UserInfo):

    def createObjFromDict(self, dictData):
        obj = PlayerArenaScoreTeam()
        for child in dictData['data']:
            teamVal = PlayerArenaScoreTeamVal()
            teamVal.teamType = child['teamType']
            teamVal.teamNUID = child['teamNUID']
            teamVal.headGBID = child['headGBID']
            teamVal.stage = child['stage']
            obj[teamVal.teamType] = teamVal

        return obj

    def getDictFromObj(self, obj):
        teamData = []
        for teamVal in obj.itervalues():
            teamData.append({'teamType': teamVal.teamType,
             'teamNUID': teamVal.teamNUID,
             'headGBID': teamVal.headGBID,
             'stage': teamVal.stage})

        return {'data': teamData}

    def isSameType(self, obj):
        return type(obj) is PlayerArenaScoreTeam


teamInstance = PlayerArenaScoreTeamInfo()

class PlayerArenaScoreScoreInfo(UserInfo):

    def createObjFromDict(self, dictData):
        obj = PlayerArenaScoreScore()
        for child in dictData['data']:
            scoreVal = PlayerArenaScoreScoreVal()
            scoreVal.teamType = child['teamType']
            scoreVal.score = child['score']
            scoreVal.totalCnt = child['totalCnt']
            scoreVal.dailyLoseCnt = child['dailyLoseCnt']
            scoreVal.dailyScore = child['dailyScore']
            scoreVal.rewarded = child['rewarded']
            scoreVal.tTime = child['tTime']
            obj[scoreVal.teamType] = scoreVal

        return obj

    def getDictFromObj(self, obj):
        scoreData = []
        for scoreVal in obj.itervalues():
            scoreData.append({'teamType': scoreVal.teamType,
             'score': scoreVal.score,
             'totalCnt': scoreVal.totalCnt,
             'dailyLoseCnt': scoreVal.dailyLoseCnt,
             'dailyScore': scoreVal.dailyScore,
             'rewarded': scoreVal.rewarded,
             'tTime': scoreVal.tTime})

        return {'data': scoreData}

    def isSameType(self, obj):
        return type(obj) is PlayerArenaScoreScore


scoreInstance = PlayerArenaScoreScoreInfo()
