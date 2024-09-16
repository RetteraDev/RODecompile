#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impWorldChallenge.o
import gameglobal

class ImpWorldChallenge(object):

    def onApplyWCSuccess(self, challengeId):
        gameglobal.rds.ui.challenge.onApplyChallengeSucc()

    def onGetRandomChallenge(self, challengeId, refId):
        gameglobal.rds.ui.roleInfo.refreshQumoQuests(refId)
