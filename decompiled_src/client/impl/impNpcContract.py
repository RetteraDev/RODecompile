#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impNpcContract.o
import gamelog
import gameglobal

class ImpNpcContract(object):

    def formContract(self, style = 1):
        gamelog.info('@zkl formContractByNpc')
        if not self.inWorld:
            return
        self.cell.formContract(style)

    def removeContract(self):
        gamelog.info('@zkl removeContractByNpc')
        if not self.inWorld:
            return
        self.cell.removeContract()

    def showUnbindFriendshipWindow(self, npcId):
        gameglobal.rds.ui.npcPanel.showTDNpc(npcId, self.chatId)

    def showbindFriendshipWindow(self, npcId):
        gameglobal.rds.ui.npcPanel.showTDNpc(npcId, self.chatId)
