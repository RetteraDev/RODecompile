#Embedded file name: I:/bag/tmp/tw2/res/entities\client/WingCityGate.o
import BigWorld
import keys
import const
from callbackHelper import Functor
from WingWarCityBuilding import WingWarCityBuilding
from data import wing_city_building_data as WCBD

class WingCityGate(WingWarCityBuilding):

    def __init__(self):
        super(WingCityGate, self).__init__()

    def set_gateStatus(self, old):
        p = BigWorld.player()
        if self.gateStatus == const.WING_CITY_GATE_STATUS_OPEN:
            self.delObstacleModel()
            self.targetCaps = []
            if p.targetLocked and p.targetLocked.id == self.id:
                p.unlockTarget()
        elif self.obstacleModel == None:
            self.createObstacleModel()
            self.targetCaps = [keys.CAP_CAN_USE]
        self.setTargetCapsUse(True)
        self.refreshStatusAction()

    def setTargetCapsUse(self, canUse):
        if canUse:
            self.targetCaps = [] if self.gateStatus == const.WING_CITY_GATE_STATUS_OPEN or self.isBroken() else [keys.CAP_CAN_USE]
        else:
            self.targetCaps = []

    def isBroken(self):
        return self.buildingStatus == len(WCBD.data.get(self.buildingId, {}).get('statusModel', [])) - 1

    def set_buildingStatus(self, old):
        p = BigWorld.player()
        super(WingCityGate, self).set_buildingStatus(old)
        self.setTargetCapsUse(True)
        if p.targetLocked and p.targetLocked.id == self.id:
            p.unlockTarget()

    def afterModelFinish(self):
        super(WingCityGate, self).afterModelFinish()
        self.refreshStatusAction()
        BigWorld.callback(2, Functor(BigWorld.player()._hideSight, self.id))

    def createObstacleModel(self):
        if self.gateStatus == const.WING_CITY_GATE_STATUS_OPEN:
            return
        super(WingCityGate, self).createObstacleModel()

    def leaveWorld(self):
        super(WingCityGate, self).leaveWorld()
        if self.gateStatus == const.WING_CITY_GATE_STATUS_CLOSE:
            BigWorld.player()._showSight(self.id)

    def refreshStatusAction(self):
        if self.gateStatus == const.WING_CITY_GATE_STATUS_OPEN:
            self.model.action('1902')()
        else:
            self.model.action('1900')()

    def loadImmediately(self):
        return True


def test():
    p = BigWorld.player()
    return BigWorld.createEntity('WingCityGate', p.spaceID, 0, p.position, (0, 0, 0), {'buildingId': 7,
     'cityEntityNo': 1})
