#Embedded file name: /WORKSPACE/data/entities/client/ibox.o
import BigWorld
import const
import gameglobal
from iPickable import IPickable
from iNpc import INpc
from data import sys_config_data as SCD

class IBox(INpc, IPickable):

    def __init__(self):
        super(IBox, self).__init__()
        self.trapId = None
        self.isLeaveWorld = False
        self.pickNearDist = 0

    def enterWorld(self):
        super(IBox, self).enterWorld()
        if not self.trapId:
            self.trapId = BigWorld.addPot(self.matrix, self.getBoxTrapRange(), self.trapCallback)

    def getBoxTrapRange(self):
        return SCD.data.get('pickNearQuestBoxLength', 6)

    def trapCallback(self, enteredTrap, handle):
        if not self.inWorld:
            return
        p = BigWorld.player()
        pickNearDist = self.getBoxTrapRange()
        self.pickNearDist = pickNearDist
        valid = self.checkEntValid(self)
        if valid and enteredTrap:
            p.addBoxTrapEx(self)
        else:
            p.delBoxTrapEx(self)
            p.onLeaveTreasureBoxTrap(self.id)

    def boxTrapCallback(self):
        p = BigWorld.player()
        pickNearDist = self.getBoxTrapRange()
        self.pickNearDist = pickNearDist
        if not self.checkEntValid(self):
            p.delBoxTrapEx(self)
            p.onLeaveTreasureBoxTrap(self.id)
        else:
            p.addBoxTrapEx(self)

    def checkEntValid(self, entity):
        if not isinstance(entity, IBox):
            return False
        pickNearDist = self.getBoxTrapRange()
        if not (entity.position - BigWorld.player().position).lengthSquared < pickNearDist * pickNearDist:
            return False
        if entity.isLeaveWorld:
            return False
        if not (hasattr(entity, 'getOpacityValue') and entity.getOpacityValue()[0] == gameglobal.OPACITY_FULL):
            return False
        return True

    def leaveWorld(self):
        super(IBox, self).leaveWorld()
        self.isLeaveWorld = True
        self.boxTrapCallback()
        if self.trapId != None:
            BigWorld.delPot(self.trapId)
            self.trapId = None
        self.pickNearDist = 0

    def use(self):
        super(IBox, self).use()
        p = BigWorld.player()
        exclude = ('WINGFLY_ST', 'WINGFLY_FLYRIDE_ST', 'FLY_RIDE_ST') if getattr(self, 'useDummyFilter', False) else ()
        if hasattr(p, 'stateMachine') and not p.stateMachine.checkStatus_check(const.CT_OPEN_BOX, exclude=exclude):
            return
        p.cell.useBox(self.id)

    def hide(self, bHide, retainTopLogo = False):
        super(IBox, self).hide(bHide, retainTopLogo)
        if self.pickNearDist:
            if (self.position - BigWorld.player().position).lengthSquared < self.pickNearDist * self.pickNearDist:
                self.boxTrapCallback()

    def getFKey(self):
        data = self.getItemData()
        if data:
            return data.get('fKey', 0)
        return 0
