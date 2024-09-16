#Embedded file name: /WORKSPACE/data/entities/client/helpers/entitydebugnamefactory.o
import heapq
import BigWorld
import utils
from guis import topLogo
from gameclass import Singleton
from data import npc_model_client_data as NMCD

class IEntityNameDesc(object):

    def __init__(self, ent):
        self.ent = ent

    def getEntityDebugName(self):
        pass


class NpcNameDesc(IEntityNameDesc):

    def __init__(self, ent):
        super(NpcNameDesc, self).__init__(ent)

    def getEntityDebugName(self):
        npcName = ''
        npcName += 'npcId:' + str(self.ent.npcId) + '\n'
        npcName += 'seekerId:' + str(self.ent.gamedbid) + '\n'
        npcName += 'pTag:' + str(self.ent.publishtag) + '\n'
        tmpName = NMCD.data.get(self.ent.npcId, {}).get('tmpName', '')
        if tmpName:
            npcName += 'tName:' + tmpName
        return npcName


class DawdlerNameDesc(IEntityNameDesc):

    def __init__(self, ent):
        super(DawdlerNameDesc, self).__init__(ent)

    def getEntityDebugName(self):
        npcName = ''
        npcName += 'npcId:' + str(self.ent.npcId) + '\n'
        npcName += 'seekerId:' + str(self.ent.gamedbid) + '\n'
        npcName += 'pTag:' + str(self.ent.publishtag) + '\n'
        return npcName


class QuestBoxNameDesc(IEntityNameDesc):

    def __init__(self, ent):
        super(QuestBoxNameDesc, self).__init__(ent)

    def getEntityDebugName(self):
        descName = ''
        descName += 'questBoxType:' + str(self.ent.questBoxType) + '\n'
        descName += 'seekerId:' + str(self.ent.gamedbid) + '\n'
        descName += 'pTag:' + str(self.ent.publishtag) + '\n'
        return descName


class SpawnPointNameDesc(IEntityNameDesc):

    def __init__(self, ent):
        super(SpawnPointNameDesc, self).__init__(ent)

    def getEntityDebugName(self):
        descName = ''
        descName += 'dbId:' + str(self.ent.gamedbid) + '\n'
        descName += 'pTag:' + str(self.ent.publishtag) + '\n'
        return descName


class MonsterNameDesc(IEntityNameDesc):

    def __init__(self, ent):
        super(MonsterNameDesc, self).__init__(ent)

    def getEntityDebugName(self):
        descName = ''
        if self.ent.charType:
            descName += 'charType:' + str(self.ent.charType) + '\n'
        if self.ent.gamedbid:
            descName += 'dbId:' + str(self.ent.gamedbid) + '\n'
        if self.ent.publishtag:
            descName += 'pTag:' + str(self.ent.publishtag) + '\n'
        fbEntityNo = getattr(self.ent, 'fbEntityNo', 0)
        if fbEntityNo:
            descName += 'fbEntityNo:' + str(fbEntityNo) + '\n'
        return descName


class TransportNameDesc(IEntityNameDesc):

    def __init__(self, ent):
        super(TransportNameDesc, self).__init__(ent)

    def getEntityDebugName(self):
        descName = ''
        descName += 'charType:' + str(self.ent.charType) + '\n'
        descName += 'dbId:' + str(self.ent.gamedbid) + '\n'
        descName += 'pTag:' + str(self.ent.publishtag) + '\n'
        return descName


class DawdlerLeaderNameDesc(IEntityNameDesc):

    def __init__(self, ent):
        super(DawdlerLeaderNameDesc, self).__init__(ent)

    def getEntityDebugName(self):
        npcName = ''
        npcName += 'entId:' + str(self.ent.id) + '\n'
        npcName += 'seekerId:' + str(self.ent.gamedbid) + '\n'
        npcName += 'pTag:' + str(self.ent.publishtag) + '\n'
        return npcName


class MovableNpcNameDesc(IEntityNameDesc):

    def __init__(self, ent):
        super(MovableNpcNameDesc, self).__init__(ent)

    def getEntityDebugName(self):
        npcName = ''
        npcName += 'npcId:' + str(self.ent.npcId) + '\n'
        npcName += 'seekerId:' + str(self.ent.gamedbid) + '\n'
        npcName += 'pTag:' + str(self.ent.publishtag) + '\n'
        return npcName


class HomeFurnitureNameDesc(IEntityNameDesc):

    def __init__(self, ent):
        super(HomeFurnitureNameDesc, self).__init__(ent)

    def getEntityDebugName(self):
        npcName = getattr(self.ent, 'showName', '')
        return npcName


class InteractiveObjectNameDesc(IEntityNameDesc):

    def __init__(self, ent):
        super(InteractiveObjectNameDesc, self).__init__(ent)

    def getEntityDebugName(self):
        npcName = getattr(self.ent, 'showName', '')
        return npcName


class EntityDebugNameFactory(object):
    __metaclass__ = Singleton
    ENTITY_LIST = ['Npc',
     'Dawdler',
     'QuestBox',
     'SpawnPoint',
     'Monster',
     'Transport',
     'DawdlerLeader',
     'MovableNpc']
    PUBLISH_ENTITY_LIST = ['HomeFurniture', 'InteractiveObject']
    NUM_MAX_NAME = 50

    def __init__(self):
        self.insList = []
        self.resetEntitySet = set()

    def __createIns(self, entType, ent):
        if entType == 'Npc':
            return NpcNameDesc(ent)
        elif entType == 'Dawdler':
            return DawdlerNameDesc(ent)
        elif entType == 'QuestBox':
            return QuestBoxNameDesc(ent)
        elif entType == 'SpawnPoint':
            return SpawnPointNameDesc(ent)
        elif entType == 'Monster':
            return MonsterNameDesc(ent)
        elif entType == 'Transport':
            return TransportNameDesc(ent)
        elif entType == 'DawdlerLeader':
            return DawdlerLeaderNameDesc(ent)
        elif entType == 'MovableNpc':
            return MovableNpcNameDesc(ent)
        elif entType == 'HomeFurniture':
            return HomeFurnitureNameDesc(ent)
        elif entType == 'InteractiveObject':
            return InteractiveObjectNameDesc(ent)
        else:
            return None

    def showEntityDebugName(self, isReset):
        entityList = EntityDebugNameFactory.PUBLISH_ENTITY_LIST
        if not BigWorld.isPublishedVersion():
            entityList += EntityDebugNameFactory.ENTITY_LIST
        self.insList = []
        entities = BigWorld.entities.values()
        for ent in entities:
            if ent and ent.__class__.__name__ not in entityList:
                continue
            if not hasattr(ent, 'getTopLogoHeight'):
                continue
            if ent.getTopLogoHeight() < 0:
                continue
            if not utils.instanceof(ent, 'HomeFurniture'):
                if not hasattr(ent, 'topLogo'):
                    continue
                if not ent.topLogo:
                    continue
            ins = self.__createIns(ent.__class__.__name__, ent)
            if ins:
                self.insList.append(ins)

        if len(self.insList) < self.NUM_MAX_NAME:
            for ins in self.insList:
                if not ins.ent.topLogo:
                    ins.ent.topLogo = topLogo.TopLogo(ins.ent.id)
                if isReset:
                    ins.ent.topLogo.updateRoleName(ins.ent.topLogo.name)
                    self.resetEntitySet.discard(ins.ent.id)
                else:
                    ins.ent.topLogo.updateRoleName(ins.getEntityDebugName())
                    self.resetEntitySet.add(ins.ent.id)

        else:
            maxHeap = []
            p = BigWorld.player()
            for i, ins in enumerate(self.insList):
                dis = (ins.ent.position - p.position).lengthSquared
                if i < self.NUM_MAX_NAME:
                    heapq.heappush(maxHeap, (-dis, ins))
                else:
                    top = maxHeap[0]
                    maxDis = -top[0]
                    if dis < maxDis:
                        heapq.heappop(maxHeap)
                        heapq.heappush(maxHeap, (-dis, ins))

            for i in xrange(self.NUM_MAX_NAME):
                ins = maxHeap[i][1]
                if not ins.ent.topLogo:
                    ins.ent.topLogo = topLogo.TopLogo(ins.ent.id)
                if isReset:
                    ins.ent.topLogo.updateRoleName(ins.ent.topLogo.name)
                    self.resetEntitySet.discard(ins.ent.id)
                else:
                    ins.ent.topLogo.updateRoleName(ins.getEntityDebugName())
                    self.resetEntitySet.add(ins.ent.id)

        if isReset:
            for id in self.resetEntitySet:
                entity = BigWorld.entities.get(id, None)
                if entity and entity.topLogo:
                    entity.topLogo.updateRoleName(entity.topLogo.name)

            self.resetEntitySet.clear()


def getInstance():
    return EntityDebugNameFactory.getInstance()
