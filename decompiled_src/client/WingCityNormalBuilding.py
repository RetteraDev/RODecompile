#Embedded file name: I:/bag/tmp/tw2/res/entities\client/WingCityNormalBuilding.o
import BigWorld
import const
from callbackHelper import Functor
from WingWarCityBuilding import WingWarCityBuilding

class WingCityNormalBuilding(WingWarCityBuilding):
    IsMonster = False

    def __init__(self):
        super(WingCityNormalBuilding, self).__init__()

    def afterModelFinish(self):
        super(WingCityNormalBuilding, self).afterModelFinish()
        BigWorld.callback(2, Functor(BigWorld.player()._hideSight, self.id))

    def leaveWorld(self):
        super(WingCityNormalBuilding, self).leaveWorld()
        BigWorld.player()._showSight(self.id)
