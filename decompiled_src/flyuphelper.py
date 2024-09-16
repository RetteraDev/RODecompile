#Embedded file name: /WORKSPACE/data/entities/client/helpers/flyuphelper.o
import BigWorld
import const
import copy
from data import fly_up_exp_data as FUED
from data import fly_up_challenge_data as FUCD
from data import quest_data as QD

class FlyUpHelper(object):

    def __init__(self):
        super(FlyUpHelper, self).__init__()

    def getPlayerFlyUpInfo(self):
        p = BigWorld.player()
        flyUpLv = p.flyUpLv
        currExp = getattr(p, 'exp', 0)
        xiuWeiVal = p.expXiuWei
        sectionInfo = self.getFlyUpSectionInfo(flyUpLv)
        sectionInfo['currExp'] = currExp
        sectionInfo['xiuWeiVal'] = xiuWeiVal
        sectionInfo['totalExp'] = currExp + xiuWeiVal
        return sectionInfo

    def getFlyUpSectionInfo(self, flyLv):
        sectionPerChapter = const.SUB_FLYUP_NUM
        mainLv = int(flyLv / sectionPerChapter)
        subLv = flyLv - sectionPerChapter * mainLv
        expData = FUED.data.get(flyLv + 1, {})
        currData = FUED.data.get(flyLv, {})
        sectionInfo = {'mainLv': mainLv + 1,
         'subLv': subLv,
         'lv': expData.get('lv', 0),
         'flyDec': currData.get('flyDec', ''),
         'isMax': flyLv > 0 and not expData}
        sectionInfo.update(expData)
        return sectionInfo

    def isChallengeFinished(self, flyLv):
        challengeInfo = FUCD.data.get(flyLv, {})
        endQuestId = challengeInfo.get('endQuestId', 0)
        if not endQuestId:
            return True
        p = BigWorld.player()
        if p.getQuestFlag(endQuestId):
            return True
        return False

    def getFlyUpChallengeInfo(self, flyLv):
        p = BigWorld.player()
        challengeInfo = copy.deepcopy(FUCD.data.get(flyLv, {}))
        challengeInfo['lv'] = FUED.data.get(flyLv, {}).get('lv', 0)
        startQuestId = challengeInfo.get('startQuestId', 0)
        endQuestId = challengeInfo.get('endQuestId', 0)
        questId = startQuestId
        maxLoopTime = 15
        currTime = 0
        while questId != endQuestId and currTime <= maxLoopTime:
            currTime += 1
            if not p.getQuestFlag(questId):
                break
            else:
                td = QD.data.get(questId, {})
                if td.has_key('acSucQst'):
                    nextQuest = td.get('acSucQst', [])
                    if nextQuest:
                        questId = nextQuest[0]
                    else:
                        break

        if currTime >= maxLoopTime:
            pass
        currentQuest = questId
        challengeInfo['currentQuest'] = currentQuest
        return challengeInfo

    def flyUpLvUp(self):
        pass


instance = None

def getInstance():
    global instance
    if not instance:
        instance = FlyUpHelper()
    return instance
