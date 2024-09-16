#Embedded file name: I:/bag/tmp/tw2/res/entities\client/VirtualCalcUnit.o
import gameglobal
import utils
from iClient import IClient
from helpers import fashion
from helpers import ufo

class VirtualCalcUnit(IClient):
    IsVirtualCalcUnit = True

    def enterWorld(self):
        self.fashion = fashion.Fashion(self.id)
        self.fashion.loadDummyModel()
        self.initYaw = self.yaw
        self.hide(True, False)

    def leaveWorld(self):
        if self.fashion != None:
            self.fashion.attachUFO(ufo.UFO_NULL)
            self.fashion.release()
            self.fashion = None
        if self.topLogo != None:
            self.topLogo.release()
            self.topLogo = utils.MyNone
        self.removeAllFx()

    def getItemData(self):
        return {}

    def getOpacityValue(self):
        return (gameglobal.OPACITY_HIDE, False)

    def afterModelFinish(self):
        super(VirtualCalcUnit, self).afterModelFinish()
        self.hide(True, False)
