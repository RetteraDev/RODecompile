#Embedded file name: I:/bag/tmp/tw2/res/entities\client/PotMoveCreationMgr.o
import BigWorld
import clientcom
from iCreation import ICreation
from data import client_creation_move_data as CCMD
from data import creation_client_data as CCD
from data import skill_creation_data as SCD

class PotMoveCreationMgr(ICreation):
    IsIsolatedCreation = False
    IsCombatCreation = True

    def __init__(self):
        self.data = CCD.data.get(self.cid, {})
        super(PotMoveCreationMgr, self).__init__()
        self.potEntities = {}

    def createPotAtClient(self, nuids, targetId):
        if not self.inWorld:
            return
        scd = SCD.data[self.cid]
        creationIds = scd.get('ccreations', [])
        for i, creationId in enumerate(creationIds):
            param = {'cid': creationId,
             'ownerId': self.id,
             'potNUID': nuids[i],
             'followTgt': targetId}
            target = BigWorld.entities.get(targetId)
            pos = self._getCombatCreationPosition(creationId, self, target)
            spaceID = BigWorld.player().spaceID
            entityID = BigWorld.createEntity('PotMoveCreation', spaceID, 0, pos, (0, 0, self.yaw), param)
            self.potEntities[nuids[i]] = entityID

    def _getCombatCreationPosition(self, creationId, relSelf, tgt):
        ccmd = CCMD.data[creationId]
        targetRel = ccmd.get('targetRel', 0)
        if targetRel and tgt:
            rel = tgt
        else:
            rel = relSelf
        angleFix = ccmd.get('angleFix', 0)
        heightFix = ccmd.get('heightFix', 0)
        distFix = ccmd.get('distFix', 0)
        if angleFix or heightFix or distFix:
            pos = clientcom.getRelativePosition(rel.position, rel.yaw, angleFix, distFix)
            if heightFix:
                pos = (pos[0], pos[1] + heightFix, pos[2])
        else:
            pos = (rel.position[0], rel.position[1], rel.position[2])
        return pos

    def unregPotAtClient(self, nuid, playerId):
        if not self.inWorld:
            return
        if self.potEntities.has_key(nuid):
            entityId = self.potEntities[nuid]
            self.potEntities.pop(nuid)
            potEntity = BigWorld.entities.get(entityId)
            if potEntity:
                if playerId > 0 and playerId != BigWorld.player().id:
                    potEntity.activate(playerId)
                potEntity.onDestroy()

    def safeDestroyAtClient(self):
        if not self.inWorld:
            return
        for nuid in self.potEntities.keys():
            self.unregPotAtClient(nuid, 0)

    def enterWorld(self):
        super(PotMoveCreationMgr, self).enterWorld()

    def leaveWorld(self):
        super(PotMoveCreationMgr, self).leaveWorld()
        self.safeDestroyAtClient()
