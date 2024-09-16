#Embedded file name: I:/bag/tmp/tw2/res/entities\client/WingWarCityBuilding.o
import gameglobal
from sfx import sfx
from WingCityBuilding import WingCityBuilding
from iCombatUnit import ICombatUnit
from data import wing_city_building_data as WCBD

class WingWarCityBuilding(WingCityBuilding, ICombatUnit):
    IsWingCityWarBuilding = True

    def __init__(self):
        self.applyTints = []
        super(WingWarCityBuilding, self).__init__()

    def leaveWorld(self):
        super(WingWarCityBuilding, self).leaveWorld()
