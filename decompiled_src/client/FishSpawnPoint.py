#Embedded file name: I:/bag/tmp/tw2/res/entities\client/FishSpawnPoint.o
import BigWorld
import utils
import iNpc
import gameglobal
from guis import topLogo
gShowFishSpawnPoint = False
if not BigWorld.isPublishedVersion():
    gShowFishSpawnPoint = True

class FishSpawnPoint(iNpc.INpc):

    def __init__(self):
        if gShowFishSpawnPoint:
            super(FishSpawnPoint, self).__init__()
            self.hp = 1000
            self.mhp = 1000

    def getItemData(self):
        return {'model': 20008,
         'dye': 'Default'}

    def enterWorld(self):
        if gShowFishSpawnPoint:
            super(FishSpawnPoint, self).enterWorld()
            if not self.topLogo:
                enableNotCreateTopLogoForHide = gameglobal.rds.configData.get('enableNotCreateTopLogoForHide', False)
                if enableNotCreateTopLogoForHide and hasattr(self, 'getOpacityValue') and self.getOpacityValue()[0] in gameglobal.OPACITY_HIDE_TOPLOGO:
                    return
                self.topLogo = topLogo.TopLogo(self.id)

    def leaveWorld(self):
        if gShowFishSpawnPoint:
            super(FishSpawnPoint, self).leaveWorld()
            if self.topLogo != None:
                self.topLogo.release()
                self.topLogo = utils.MyNone

    def afterModelFinish(self):
        if gShowFishSpawnPoint:
            super(FishSpawnPoint, self).afterModelFinish()

    def enterTopLogoRange(self, rangeDist = -1):
        pass

    def leaveTopLogoRange(self, rangeDist = -1):
        pass

    def showTargetUnitFrame(self):
        return False
