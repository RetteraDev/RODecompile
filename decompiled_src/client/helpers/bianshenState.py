#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/bianshenState.o
import BigWorld

class BianshenStateMgr:

    def __init__(self, ownerId):
        self.ownerId = ownerId

    def canFly(self):
        owner = BigWorld.entities.get(self.ownerId)
        if not owner or not owner.inWorld:
            return False
        if owner.isOnFlyRide() and owner.qinggongMgr.checkCanFlyRideUp():
            return True
        return False

    def canSwim(self):
        owner = BigWorld.entities.get(self.ownerId)
        if not owner or not owner.inWorld:
            return False
        if owner.isOnSwimRide() and owner.qinggongMgr.checkCanRideSwim():
            return True
        return False

    def canDive(self):
        owner = BigWorld.entities.get(self.ownerId)
        if not owner or not owner.inWorld:
            return False
        return False

    def enterSwim(self):
        pass

    def enterFly(self):
        pass

    def enterDive(self):
        pass
