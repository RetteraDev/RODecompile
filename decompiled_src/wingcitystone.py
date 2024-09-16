#Embedded file name: /WORKSPACE/data/entities/client/wingcitystone.o
import BigWorld
from WingCityBuilding import WingCityBuilding

class WingCityStone(WingCityBuilding):

    def _refreshItemIcon(self):
        p = BigWorld.player()
        selfSideId = p.wingWorldCamp if p.isWingWorldCampMode() else p.getOriginHostId()
        if self.canOccupy and selfSideId and self.ownerHostId != selfSideId and self.isInTrap:
            p.showOccupyItemIcon(self.id)
        else:
            p.hideOccupyItemIcon(self.id)

    def _hideItemIcon(self):
        p = BigWorld.player()
        p.hideOccupyItemIcon(self.id)

    def afterModelFinish(self):
        super(WingCityStone, self).afterModelFinish()
        BigWorld.player()._hideSight(self.id)

    def leaveWorld(self):
        super(WingCityStone, self).leaveWorld()
        BigWorld.player()._showSight(self.id)
