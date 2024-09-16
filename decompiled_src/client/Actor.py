#Embedded file name: I:/bag/tmp/tw2/res/entities\client/Actor.o
import BigWorld
from iClient import IClient
from helpers import fashion

class Actor(IClient):

    def __init__(self):
        super(Actor, self).__init__()

    def enterWorld(self):
        self.fashion = fashion.Fashion(self.id)
        self.fashion.loadDummyModel()
        self.filter = BigWorld.ClientFilter()
        self.filter.applyDrop = True
        self.bodyModel = self.model

    def enterTopLogoRange(self, rangeDist = -1):
        pass
