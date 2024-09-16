#Embedded file name: I:/bag/tmp/tw2/res/entities\client/MovableNpc.o
import BigWorld
import clientUtils
import gameglobal
from Npc import Npc
from guis import uiConst

class MovableNpc(Npc):

    def __init__(self):
        super(MovableNpc, self).__init__()

    def enterWorld(self):
        super(MovableNpc, self).enterWorld()

    def leaveWorld(self):
        super(MovableNpc, self).leaveWorld()

    @clientUtils.callFilter(1.0, False)
    def use(self):
        super(MovableNpc, self).use()
        self.cell.useFunc()
        soundIdx = self.getItemData().get('useNpcSound', 0)
        gameglobal.rds.sound.playSound(soundIdx)

    def needMoveNotifier(self):
        return True

    def movingNotifier(self, isMoving, moveSpeed = 1.0):
        self.isMoving = isMoving
        if isMoving:
            self.fashion.stopAction()
        elif self.isPlaySchemedIdleAct():
            self.fashion.playSingleAction(self.idleActName)
        if not self.isMoving and gameglobal.rds.ui.multiNpcChat.uiAdapter.quest.npcType == uiConst.NPC_MULTI and gameglobal.rds.ui.multiNpcChat.uiAdapter.quest.isShow:
            self.faceTo(BigWorld.player())

    def afterModelFinish(self):
        super(MovableNpc, self).afterModelFinish()
        self.filter = BigWorld.AvatarDropFilter()
