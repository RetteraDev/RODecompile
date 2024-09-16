#Embedded file name: I:/bag/tmp/tw2/res/entities\client/MonsterLeader.o
import BigWorld
import gameglobal
import utils
from guis import topLogo
from iClient import IClient
from iDisplay import IDisplay
gShowMonsterLeader = BigWorld.isPublishedVersion() == False

class MonsterLeader(IClient, IDisplay):
    defaultModelName = 'char/20008/20008.model'

    def __init__(self):
        if gShowMonsterLeader:
            super(MonsterLeader, self).__init__()
            self.hp = 1000000
            self.mp = 1000000
            self.roleName = 'π÷»∫'

    def enterWorld(self):
        if gShowMonsterLeader:
            super(MonsterLeader, self).enterWorld()
            self.fashion.loadSinglePartModel(MonsterLeader.defaultModelName)
            if not self.topLogo:
                enableNotCreateTopLogoForHide = gameglobal.rds.configData.get('enableNotCreateTopLogoForHide', False)
                if enableNotCreateTopLogoForHide and hasattr(self, 'getOpacityValue') and self.getOpacityValue()[0] in gameglobal.OPACITY_HIDE_TOPLOGO:
                    return
                self.topLogo = topLogo.TopLogo(self.id)

    def leaveWorld(self):
        if gShowMonsterLeader:
            super(MonsterLeader, self).leaveWorld()
            if self.topLogo != None:
                self.topLogo.release()
                self.topLogo = utils.MyNone

    def afterModelFinish(self):
        if gShowMonsterLeader:
            super(MonsterLeader, self).afterModelFinish()

    def enterTopLogoRange(self, rangeDist = -1):
        pass

    def leaveTopLogoRange(self, rangeDist = -1):
        pass

    def showTargetUnitFrame(self):
        return False
