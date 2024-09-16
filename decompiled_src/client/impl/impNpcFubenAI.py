#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impNpcFubenAI.o
import gameglobal
import gamelog

class ImpNpcFubenAI(object):

    def showFbAIWindow(self, npcId):
        gamelog.debug('zsnpc', self.aiInfoId)
        gameglobal.rds.ui.npcPanel.showTDNpc(npcId, self.aiInfoId)
