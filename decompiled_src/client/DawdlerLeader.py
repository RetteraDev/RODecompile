#Embedded file name: I:/bag/tmp/tw2/res/entities\client/DawdlerLeader.o
import BigWorld
import utils
import iNpc
from guis import topLogo
import gameglobal
gShowDawdlerLeader = BigWorld.isPublishedVersion() == False

class DawdlerLeader(iNpc.INpc):

    def __init__(self):
        if gShowDawdlerLeader:
            super(DawdlerLeader, self).__init__()
            self.hp = 1000
            self.mhp = 1000
            self.roleName = ''

    def getItemData(self):
        return {'model': 20008,
         'dye': 'Default'}

    def enterWorld(self):
        if gShowDawdlerLeader:
            super(DawdlerLeader, self).enterWorld()
            if not self.topLogo:
                enableNotCreateTopLogoForHide = gameglobal.rds.configData.get('enableNotCreateTopLogoForHide', False)
                if enableNotCreateTopLogoForHide and hasattr(self, 'getOpacityValue') and self.getOpacityValue()[0] in gameglobal.OPACITY_HIDE_TOPLOGO:
                    return
                self.topLogo = topLogo.TopLogo(self.id)

    def leaveWorld(self):
        if gShowDawdlerLeader:
            super(DawdlerLeader, self).leaveWorld()
            if self.topLogo != None:
                self.topLogo.release()
                self.topLogo = utils.MyNone

    def afterModelFinish(self):
        if gShowDawdlerLeader:
            super(DawdlerLeader, self).afterModelFinish()

    def enterTopLogoRange(self, rangeDist = -1):
        pass

    def leaveTopLogoRange(self, rangeDist = -1):
        pass

    def showTargetUnitFrame(self):
        return False
