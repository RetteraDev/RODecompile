#Embedded file name: I:/bag/tmp/tw2/res/entities\client/SpawnPoint.o
import BigWorld
import utils
import iNpc
import gamelog
from guis import topLogo

class SpawnPoint(iNpc.INpc):
    defaultModelName = 'char/20008/20008.model'

    def __init__(self):
        super(SpawnPoint, self).__init__()
        self.createDimpleInWater = False
        self.hasDebugInfo = False

    def getItemData(self):
        return {'model': 20008,
         'dye': 'Default'}

    def enterWorld(self):
        super(SpawnPoint, self).enterWorld()
        if not BigWorld.isPublishedVersion():
            self.showDebugInfo()
        else:
            self.hide(True)

    def afterModelFinish(self):
        self.setTargetCapsUse(False)
        if not BigWorld.isPublishedVersion():
            self.showDebugInfo()
        else:
            self.hide(True)
        self.filter = BigWorld.DumbFilter()

    def hide(self, isHide):
        super(SpawnPoint, self).hide(isHide)
        self.model.visible = not isHide

    def leaveWorld(self):
        self.hideDebugInfo()
        super(SpawnPoint, self).leaveWorld()
        gamelog.debug('SpawnPoint::leaveWorld................')
        if self.topLogo != None:
            self.topLogo.release()
            self.topLogo = utils.MyNone

    def enterTopLogoRange(self, rangeDist = -1):
        pass

    def leaveTopLogoRange(self, rangeDist = -1):
        pass

    def showDebugInfo(self):
        gamelog.debug('SpawnPoint::showDebugInfo........', self.hasDebugInfo)
        self.hideDebugInfo()
        self.hide(False)
        self.fashion.loadSinglePartModel(SpawnPoint.defaultModelName)
        if not self.topLogo:
            self.topLogo = topLogo.TopLogo(self.id)
        self.hasDebugInfo = True

    def hideDebugInfo(self):
        gamelog.debug('SpawnPoint::hideDebugInfo........', self.hasDebugInfo)
        if self.hasDebugInfo:
            self.hide(True)
        self.hasDebugInfo = False

    def showTargetUnitFrame(self):
        return False
