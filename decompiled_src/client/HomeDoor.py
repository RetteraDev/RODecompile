#Embedded file name: I:/bag/tmp/tw2/res/entities\client/HomeDoor.o
import BigWorld
import gameglobal
from iClient import IClient
from helpers import fashion
from data import sys_config_data as SCD

class HomeDoor(IClient):

    def __init__(self):
        super(HomeDoor, self).__init__()
        self.trapId = None
        self.fashion = None
        self.roleName = ''
        self.intimacyName = ''

    def enterWorld(self):
        self.trapId = BigWorld.addPot(self.matrix, SCD.data.get('USE_DOOR_DIST', 1.5), self.trapCallback)
        self.roleName = self.name
        self.intimacyName = self.intimacyName
        self.fashion = fashion.Fashion(self.id)
        self.fashion.loadDummyModel()
        gameglobal.rds.ui.homeDoorPlate.show(self.id)

    def trapCallback(self, enteredTrap, handle):
        if not self.inWorld:
            return
        p = BigWorld.player()
        p.cell.enterRoom(self.roomNo)

    def leaveWorld(self):
        gameglobal.rds.ui.homeDoorPlate.dismiss(self.id)
        if self.trapId != None:
            BigWorld.delPot(self.trapId)
            self.trapId = None
        if self.fashion:
            self.fashion.release()
            self.fashion = None

    def getTopLogoHeight(self):
        return -1
