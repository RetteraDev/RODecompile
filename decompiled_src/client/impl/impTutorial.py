#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impTutorial.o
import gamelog
import gameglobal

class ImpTutorial(object):

    def finishFbByTutorial(self, fubenId = 1011):
        gamelog.debug('hjx debug tutor finishFbByGuider:', fubenId)
        gameglobal.rds.tutorial.onFinishFbId(fubenId)

    def onEnterTrapTutorial(self, npcId):
        gamelog.debug('hjx debug tutor onEnterTrap:', npcId)
        gameglobal.rds.tutorial.onEnterTrap(npcId)

    def onMonsterDying(self, charType):
        gamelog.debug('hjx debug tutor onMonsterDying:', charType)
        gameglobal.rds.tutorial.onMonsterDying(charType)

    def onFinishQuest(self, questId):
        gamelog.debug('hjx debug tutor onRewardByQuest:', questId)
        gameglobal.rds.tutorial.onFinishQuest(questId)
        gameglobal.rds.tutorial.onFinishedQuest(questId)
        gameglobal.rds.ui.qinggongWingTutorialIcon.pushIcon(questId)

    def onGetTitle(self, titleId):
        gameglobal.rds.tutorial.onGetTitle()
        gameglobal.rds.tutorial.onGetSpecificTitle(titleId)

    def onFeedbackReward(self, comId):
        gamelog.debug('@hjx tutorial#onFeedbackReward:', comId)
        gameglobal.rds.tutorial.componentFinish(comId)

    def onStartTutorialComponent(self, componentId):
        gameglobal.rds.tutorial.startComponent(componentId)

    def onAddDaoHengSlot(self, skillId):
        gameglobal.rds.tutorial.onAddDaoHengSlot(skillId)

    def onMultiCarrierReadyFull(self, carrierNo):
        gameglobal.rds.tutorial.onMultiCarrierReadyFull(carrierNo)
