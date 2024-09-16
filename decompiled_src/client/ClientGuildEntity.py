#Embedded file name: I:/bag/tmp/tw2/res/entities\client/ClientGuildEntity.o
import math
import BigWorld
import gametypes
import gameglobal
from BaseClientEntity import BaseClientEntity
from data import guild_static_entity_data as GSED
from sfx import sfx

class ClientGuildEntity(BaseClientEntity):

    def __init__(self):
        super(ClientGuildEntity, self).__init__()
        self.trapId = None
        self.interactEffects = []
        self.sitAvatarId = None

    def isObstacle(self):
        return GSED.data.get(self.geId).get('type') != 1

    def getPrefabId(self):
        return GSED.data.get(self.geId).get('modelId')

    def getInteractEffects(self):
        return GSED.data.get(self.geId).get('interactEffects', [])

    def canInteract(self):
        return GSED.data.get('canInteract', False)

    def getPrefabIdPath(self, prefabId):
        path = 'scene/common/building/prefab/%d.prefab' % prefabId
        return path

    def getLoadModelRadius(self):
        return 0

    def getUnloadModelRadius(self):
        return 0

    def enterWorld(self):
        super(ClientGuildEntity, self).enterWorld()
        data = GSED.data.get(self.geId)
        radius = data.get('radius', 0)
        if data.get('canInteract') and radius:
            self.trapId = BigWorld.addPot(self.matrix, radius, self._trapCallback)

    def setupFilter(self):
        self.filter = BigWorld.ClientFilter()
        self.filter.applyDrop = True

    def leaveWorld(self):
        if self.trapId != None:
            BigWorld.delPot(self.trapId)
            self.trapId = None
            p = BigWorld.player()
            p.hideGuildEntityItemIcon(self.id)
            self._checkLeaveChair()
        super(ClientGuildEntity, self).leaveWorld()

    def _checkLeaveChair(self):
        p = BigWorld.player()
        data = GSED.data.get(self.geId)
        if data.get('type') == gametypes.GUILD_STATIC_ENTITY_CHAIR and getattr(p, 'chairEntId', 0) == self.id:
            if p.isGuildSitInChair():
                p.guildLeaveChair()

    def _trapCallback(self, enteredTrap, handle):
        if not self.inWorld:
            return
        p = BigWorld.player()
        if enteredTrap:
            if p.guildNUID == self.guildNUID:
                p.showGuildEntityItemIcon(self.id)
        else:
            p.hideGuildEntityItemIcon(self.id)
            self._checkLeaveChair()

    def releaseInteractEffects(self):
        if self.interactEffects:
            for ef in self.interactEffects:
                if ef:
                    ef.stop()

        self.interactEffects = []

    def refreshInteractEffects(self):
        self.releaseInteractEffects()
        if not getattr(self, 'ownerModels', []):
            return
        data = GSED.data.get(self.geId)
        if data.get('type') != gametypes.GUILD_STATIC_ENTITY_CHAIR:
            return
        if getattr(self, 'sitAvatarId', None):
            return
        model = self.ownerModels[0]
        effects = self.getInteractEffects()
        if effects:
            effecLv = BigWorld.player().getBasicEffectLv()
            priority = BigWorld.player().getBasicEffectPriority()
            for effId in effects:
                res = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (effecLv,
                 priority,
                 model,
                 effId,
                 sfx.EFFECT_UNLIMIT,
                 -1))
                if res:
                    self.interactEffects += res

    def onModelFinish(self, model):
        super(ClientGuildEntity, self).onModelFinish(model)
        if self.inWorld and model:
            model.yaw = math.radians(GSED.data.get(self.geId).get('direction')[2])
            self.refreshInteractEffects()
