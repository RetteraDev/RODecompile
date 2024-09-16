#Embedded file name: I:/bag/tmp/tw2/res/entities\client/Tinker.o
import cPickle
import BigWorld
import gameglobal
from iNpc import INpc
Obj = None

class Tinker(INpc):

    def __init__(self):
        global Obj
        super(Tinker, self).__init__()
        self.desc = {}
        self.entType = None
        Obj = self

    def enterWorld(self):
        super(Tinker, self).enterWorld()

    def afterModelFinish(self):
        super(Tinker, self).afterModelFinish()
        self.filter = BigWorld.DumbFilter()

    def use(self):
        super(Tinker, self).use()
        self.cell.examine()

    def desc_send(self, npcID, npcType, descPair):
        self.desc[descPair[0]] = descPair[1]

    def attr_send(self, npcID, npcType, npcAttr):
        self.desc[npcType] = npcAttr
        self.entType = npcType
        self.property = npcAttr
        print '@hjx attr_send:', npcID, npcType, npcAttr
        gameglobal.rds.ui.tinker.showTinkerProPage()

    def onEdited(self, neo):
        self.cell.reforge(cPickle.dumps(neo, -1))
        return True

    def showTargetUnitFrame(self):
        return False
