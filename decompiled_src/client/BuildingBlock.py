#Embedded file name: I:/bag/tmp/tw2/res/entities\client/BuildingBlock.o
import BigWorld
from iClient import IClient
from helpers import modelServer

class BuildingBlock(IClient):

    def __init__(self):
        super(BuildingBlock, self).__init__()
        self.roleName = 'ЕЪзг'

    def getItemData(self):
        return {'fullPath': 'scene/common/homes/n/wj/nwj_02_02001.model'}

    def needBlackShadow(self):
        return False

    def afterModelFinish(self):
        super(BuildingBlock, self).afterModelFinish()
        self.setTargetCapsUse(False)
        self.filter = BigWorld.ClientFilter()

    def getTopLogoHeight(self):
        return 2

    def enterWorld(self):
        super(BuildingBlock, self).enterWorld()
        self.modelServer = modelServer.SimpleModelServer(self, self.isUrgentLoad())

    def leaveWorld(self):
        super(BuildingBlock, self).leaveWorld()
