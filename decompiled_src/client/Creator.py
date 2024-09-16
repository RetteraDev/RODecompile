#Embedded file name: I:/bag/tmp/tw2/res/entities\client/Creator.o
import cPickle
import BigWorld
import const
import gameglobal
from iNpc import INpc
Obj = None

class Creator(INpc):
    last = {}

    def __init__(self):
        global Obj
        super(Creator, self).__init__()
        self.desc = {}
        self.default = {}
        self.hp = 1000000
        Obj = self
        self.npcId = 10000

    def enterWorld(self):
        super(Creator, self).enterWorld()
        self.setTargetCapsUse(True)

    def afterModelFinish(self):
        super(Creator, self).afterModelFinish()
        if self.fashion == None:
            return
        self.filter = BigWorld.DumbFilter()

    def use(self):
        super(Creator, self).use()
        self.cell.queryType()

    def sendDesc(self, descInfo):
        descInfo[1]['publishTag'] = 'tags±ê¼Ç'
        self.desc[descInfo[0]] = descInfo[1]

    def queryType(self):
        gameglobal.rds.ui.creator.showCreatorOptionsPage()

    def querySpec(self, entType, attr):
        attr['publishTag'] = ''
        self.property = attr
        self.entType = entType
        if Creator.last.has_key(entType):
            self.property = Creator.last[entType]
        gameglobal.rds.ui.creator.showCreatorProPage()

    def onEdited(self, entType, neo):
        if not Creator.last.has_key(entType):
            Creator.last[entType] = {}
        self.cell.bornSpec(entType, cPickle.dumps(neo, -1))
        self.setLastProperty(entType, neo)
        return True

    def setLastProperty(self, entType, neo):
        Creator.last[entType] = neo
        if entType == 'FishSpawnPoint':
            needPopVal = []
            for key in Creator.last[entType].keys():
                if isinstance(key, str) and key.find(const.FISH_SP_LIST) != -1:
                    needPopVal.append(key)

            for key in needPopVal:
                Creator.last[entType].pop(key, None)

    def showTargetUnitFrame(self):
        return False
