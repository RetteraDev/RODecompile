#Embedded file name: I:/bag/tmp/tw2/res/entities\client/WingCityAirStone.o
import BigWorld
from Monster import Monster

class WingCityAirStone(Monster):
    IsMonster = False
    IsWingCityWarBuilding = True

    def __init__(self):
        super(WingCityAirStone, self).__init__()

    def afterModelFinish(self):
        super(WingCityAirStone, self).afterModelFinish()
        BigWorld.player()._hideSight(self.id)

    def leaveWorld(self):
        super(WingCityAirStone, self).leaveWorld()
        BigWorld.player()._showSight(self.id)
