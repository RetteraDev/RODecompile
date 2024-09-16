#Embedded file name: I:/bag/tmp/tw2/res/entities\client/PotMoveCreation.o
import math
import BigWorld
import Math
import gametypes
import const
import formula
import clientcom
import gameglobal
from iCreation import ICreation
from sMath import distance3D
from data import client_creation_move_data as CCMD
from data import creation_client_data as CCD
DEFAULT_MODEL = 39999

class PotMoveCreation(ICreation):
    IsIsolatedCreation = False
    IsCombatCreation = True

    def __init__(self):
        super(PotMoveCreation, self).__init__()
        self.data = CCD.data.get(self.cid, {})
        self.visiType = 50
        self.bodySize = 0.5
        ccmd = CCMD.data[self.cid]
        ttl = ccmd['ttl']
        BigWorld.callback(ttl, self.safeDestroyAtClient)

    def enterWorld(self):
        super(PotMoveCreation, self).enterWorld()

    def afterModelFinish(self):
        super(PotMoveCreation, self).afterModelFinish()
        self.filter = BigWorld.ClientFilter()
        owner = BigWorld.entities.get(self.ownerId)
        target = BigWorld.entities.get(self.followTgt)
        if owner is None:
            self.safeDestroyAtClient()
            return
        self._setUpMoveInfo(owner, target)
        ccmd = CCMD.data[self.cid]
        self.trapId = BigWorld.addPot(self.matrix, ccmd['radius'], self.trapEventCallback)
        self.move()

    def leaveWorld(self):
        super(PotMoveCreation, self).leaveWorld()

    def enterTopLogoRange(self, rangeDist = -1):
        super(PotMoveCreation, self).enterTopLogoRange(rangeDist)

    def leaveTopLogoRange(self, rangeDist = -1):
        super(PotMoveCreation, self).leaveTopLogoRange(rangeDist)

    def getOpacityValue(self):
        return (gameglobal.OPACITY_FULL, True)

    def resetClientYawMinDist(self):
        pass

    def safeDestroyAtClient(self):
        if not self.inWorld:
            return
        owner = BigWorld.entities.get(self.ownerId)
        if owner:
            owner.unregPotAtClient(self.potNUID, 0)
        else:
            self.onDestroy()

    def onDestroy(self):
        if hasattr(self, 'trapId') and self.trapId:
            BigWorld.delPot(self.trapId)
            self.trapId = None
        BigWorld.destroyEntity(self.id)

    def trapEventCallback(self, enteredTrap, handle):
        if not self.inWorld:
            return
        if enteredTrap:
            ccmd = CCMD.data[self.cid]
            if ccmd.get('trigUnlimit', 0):
                canRemove = False
            else:
                canRemove = True
            owner = BigWorld.entities.get(self.ownerId)
            if owner and self.potNUID in owner.clientPots:
                owner.cell.onPotEnter(self.potNUID, self.position, canRemove)
                self.activate(BigWorld.player().id)

    def _setUpMoveInfo(self, owner, target):
        ccmd = CCMD.data[self.cid]
        oriDirFix = formula.angleToRadian(ccmd.get('originalDirFix', 0))
        if oriDirFix != 0:
            self.filter.yaw = owner.yaw + oriDirFix
        self.moveType = ccmd.get('moveType', 0)
        moveAngleFix = ccmd.get('moveAngleFix', 0)
        speed = ccmd.get('speed', const.DEFAULT_MOVE_SPEED)
        if self.moveType == gametypes.COMBATCREATION_AUTO_ROTATION:
            speed = formula.angleToRadian(speed)
        self.moveSpeed = speed
        ttl = max(ccmd['ttl'], 0.1)
        if self.moveType in gametypes.MAGIC_FIELD_MOVING:
            if self.moveType == gametypes.COMBATCREATION_FOLLOW_TGT:
                pass
            elif self.moveType == gametypes.COMBATCREATION_MOVE_FORWARD:
                self.moveToPos = clientcom.getRelativePosition(owner.position, owner.yaw, moveAngleFix, self.moveSpeed * (ttl + 1))
            elif self.moveType == gametypes.COMBATCREATION_MOVE_BACKWARD:
                self.moveToPos = clientcom.getRelativePosition(owner.position, owner.yaw, 180 + moveAngleFix, self.moveSpeed * (ttl + 1))
            elif self.moveType == gametypes.COMBATCREATION_MOVE_TOWARD_TGT:
                target = BigWorld.entities.get(self.followTgt)
                if not target:
                    return
                yaw = math.atan2(target.position[0] - owner.position[0], target.position[2] - owner.position[2])
                self.moveToPos = clientcom.getRelativePosition(self.position, yaw, moveAngleFix, self.moveSpeed * (ttl + 1))
            elif self.moveType == gametypes.COMBATCREATION_MOVE_FORWARD_SELF:
                self.moveToPos = clientcom.getRelativePosition(self.position, self.filter.yaw, moveAngleFix, self.moveSpeed * (ttl + 1))
            elif self.moveType == gametypes.COMBATCREATION_MOVE_BACKWARD_SELF:
                self.moveToPos = clientcom.getRelativePosition(self.position, self.filter.yaw, 180 + moveAngleFix, self.moveSpeed * (ttl + 1))
            elif self.moveType == gametypes.COMBATCREATION_FOLLOW_TARGET_MULTI:
                pass

    def move(self):
        if self.moveType in gametypes.MAGIC_FIELD_FOLLOW:
            self._follow()
        elif self.moveType in gametypes.MAGIC_FIELD_MOVE_TO_POS:
            self._moveToPoint(self.moveToPos)

    def _follow(self):
        tgt = BigWorld.entities.get(self.followTgt)
        if not tgt:
            return
        dist = distance3D(self.position, tgt.position)
        if dist < 0.1:
            return
        self._moveToPoint(tgt.position)
        BigWorld.callback(0.5, self._follow)

    def _facePosition(self, pos):
        if self.position == pos:
            return
        yaw = (pos - self.position).yaw
        self.filter.yaw = yaw

    def _moveToPoint(self, position):
        self._facePosition(position)
        position = Math.Vector3(position)
        self.filter.seek(position, self.moveSpeed, None)

    def needToLoad(self):
        return True

    def isUrgentLoad(self):
        isUrgentLoad = CCMD.data.get(self.cid, {}).get('isUrgentLoad', False)
        return isUrgentLoad

    def forceUpdateEffect(self):
        pass

    def getItemData(self):
        self.fid = self.data.get('sid', None)
        modelId = self.data.get('modelId', None)
        if modelId is None:
            modelId = DEFAULT_MODEL
        return {'model': modelId,
         'dye': 'Default',
         'modelShow': 1}
