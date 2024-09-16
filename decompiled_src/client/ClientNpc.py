#Embedded file name: I:/bag/tmp/tw2/res/entities\client/ClientNpc.o
import BigWorld
import gamelog
import commQuest
from Npc import Npc
from data import npc_data as ND
from data import quest_data as QD
from data import npc_model_client_data as NMCD
from data import npc_action_data as NAD

class ClientNpc(Npc):

    def __init__(self):
        super(ClientNpc, self).__init__()
        self.owner = BigWorld.entities.get(self.hostId)
        self.roleName = ND.data.get(self.npcId, {}).get('name', '')
        self.bindHostNode = ND.data.get(self.npcId, {}).get('bindHostDict', {}).get(self.hostNo, None)
        self.setBornAction(ND.data.get(self.npcId, {}).get('bornAction', ''))

    def __getattribute__(self, name):
        if name == 'cell':
            return self
        else:
            return BigWorld.Entity.__getattribute__(self, name)

    def npcTeleport(self, data, idx):
        BigWorld.player().npcTeleportByClientNpc(self.hostId, data, idx)

    def executeFbAI(self, aid, aiType):
        pass

    def acceptQuest(self, questId):
        if not QD.data.has_key(questId) or commQuest.isQuestDisable(questId):
            gamelog.error('@szh: the quest %d does not exist' % questId)
            return
        anpc = QD.data[questId]['acNpc']
        if not isinstance(anpc, tuple):
            anpc = tuple([anpc])
        if self.npcId not in anpc:
            gamelog.error('@szh: the quest %d can not assign the quest %d' % self.npcId)
            return
        player = BigWorld.player()
        if not commQuest.gainQuestCheck(player, questId, True):
            return
        player.acceptQuestByClientNpc(self.id, self.npcId, self.hostId, questId)

    def completeQuest(self, questId, options):
        player = BigWorld.player()
        if player is None:
            gamelog.error('@szh: the completeQuest quest player is None')
            return
        if not QD.data.has_key(questId):
            gamelog.error('@szh: the completeQuest quest does not exist', questId)
            return
        cnpc = QD.data[questId]['compNpc']
        if not isinstance(cnpc, tuple):
            cnpc = tuple([cnpc])
        if self.npcId not in cnpc:
            gamelog.error('@szh: the quest %d can not complete the quest %d' % (self.npcId, questId))
            return
        if not commQuest.completeQuestCheck(player, questId, True):
            return
        optionKeys = options.keys()
        optionVals = [ options[k] for k in optionKeys ]
        player.completeQuestByClientNpc(self.id, self.npcId, self.hostId, questId, optionKeys, optionVals)

    def afterModelFinish(self):
        super(ClientNpc, self).afterModelFinish()
        self.firstFetchFinished = True
        self.setTargetCapsUse(True)
        self.filter = BigWorld.ClientFilter()
        notFollowHost = ND.data.get(self.npcId, {}).get('notFollowHost', False)
        if not notFollowHost:
            self.followtarget = self.owner.matrix
            self.biasPos = self.offset
        try:
            platAct = NAD.data.get(NMCD.data.get(self.npcId, {}).get('actGroupid', 0), {}).get('platAct', ('1101',))[0]
            self.model.action(platAct)()
        except:
            pass

        self.enterTopLogoRange()

    def enterWorld(self):
        super(ClientNpc, self).enterWorld()

    def isUrgentLoad(self):
        return True

    def enterTopLogoRange(self, rangeDist = -1):
        super(ClientNpc, self).enterTopLogoRange(rangeDist)

    def resetTopLogo(self):
        super(ClientNpc, self).resetTopLogo()

    def faceTo(self, target):
        if not target:
            return
        if not self.inWorld:
            return
        nd = NMCD.data.get(self.npcId, None)
        if not nd:
            return
        keepYaw = nd.get('keepYaw', 0)
        if keepYaw:
            return
        self.filter.yaw = (target.position - self.position).yaw
