#Embedded file name: /WORKSPACE/data/entities/client/wingcityreliveboard.o
import BigWorld
import gameglobal
import const
from WingCityBuilding import WingCityBuilding
from data import wing_city_building_data as WCBD

class WingCityReliveBoard(WingCityBuilding):

    def __init__(self):
        super(WingCityReliveBoard, self).__init__()

    def _refreshItemIcon(self):
        p = BigWorld.player()
        selfSideId = p.wingWorldCamp if p.isWingWorldCampMode() else p.getOriginHostId()
        if self.canOccupy and selfSideId and self.ownerHostId != selfSideId and self.isInTrap:
            p.showOccupyItemIcon(self.id)
        elif gameglobal.rds.ui.pressKeyF.targetId == self.id:
            p.hideOccupyItemIcon(self.id)
        self.refreshTransport()

    def _hideItemIcon(self):
        p = BigWorld.player()
        p.hideOccupyItemIcon(self.id)

    def _trapCallback(self, enteredTrap, handle):
        if not self.inWorld:
            return
        super(WingCityReliveBoard, self)._trapCallback(enteredTrap, handle)
        self.refreshTransport()

    def afterModelFinish(self):
        super(WingCityReliveBoard, self).afterModelFinish()
        BigWorld.player()._hideSight(self.id)

    def leaveWorld(self):
        super(WingCityReliveBoard, self).leaveWorld()
        self.refreshTransport()
        BigWorld.player()._showSight(self.id)

    def refreshTransport(self):
        p = BigWorld.player()
        selfSideId = p.wingWorldCamp if p.isWingWorldCampMode() else p.getOriginHostId()
        if self.isInTrap and selfSideId and self.ownerHostId == selfSideId:
            gameglobal.rds.ui.pressKeyF.wingWorldReliveBoardId = self.id
            gameglobal.rds.ui.pressKeyF.setType(const.F_TRANSPORT)
            return
        gameglobal.rds.ui.pressKeyF.wingWorldReliveBoardId == None
        gameglobal.rds.ui.pressKeyF.removeType(const.F_TRANSPORT)

    def getFKey(self):
        return WCBD.data.get(self.buildingId, {}).get('fKey', 2011)
