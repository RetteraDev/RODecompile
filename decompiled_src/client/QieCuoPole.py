#Embedded file name: I:/bag/tmp/tw2/res/entities\client/QieCuoPole.o
import utils
import gameglobal
from iClient import IClient
from helpers import fashion
from helpers import modelServer
from helpers import ufo

class QieCuoPole(IClient):

    def enterWorld(self):
        self.fashion = fashion.Fashion(self.id)
        self.fashion.loadDummyModel()
        self.initYaw = self.yaw
        self.modelServer = modelServer.SimpleModelServer(self)

    def leaveWorld(self):
        if hasattr(self, 'modelServer') and self.modelServer:
            self.modelServer.release()
            self.modelServer = None
        if self.fashion != None:
            self.fashion.attachUFO(ufo.UFO_NULL)
            self.fashion.release()
            self.fashion = None
        if self.topLogo != None:
            self.topLogo.release()
            self.topLogo = utils.MyNone
        self.removeAllFx()

    def getItemData(self):
        return {'model': gameglobal.QIECUO_POLE_MODEL,
         'dye': 'Default'}

    def afterModelFinish(self):
        super(QieCuoPole, self).afterModelFinish()
        self.model.action(gameglobal.QIECUO_POLE_ACTION)()

    def set_visibleUsers(self, old):
        self.updateVis()

    def updateVis(self):
        pass
