#Embedded file name: I:/bag/tmp/tw2/res/entities\client/Firework.o
import BigWorld
import Math
import utils
import gameglobal
from iClient import IClient
from helpers import modelServer
from sfx import sfx
from data import firework_data as FD

class Firework(IClient):

    def __init__(self):
        super(Firework, self).__init__()
        self.keepEffs = []

    def enterWorld(self):
        super(Firework, self).enterWorld()
        self.modelServer = modelServer.SimpleModelServer(self, self.isUrgentLoad())
        self.filter = BigWorld.DumbFilter()

    def afterModelFinish(self):
        super(Firework, self).afterModelFinish()
        self.setTargetCapsUse(True)
        self.filter = BigWorld.DumbFilter()
        p = BigWorld.player()
        if p.isBlockFirework():
            return
        itemData = self.getItemData()
        keepEff = itemData.get('keepEff', None)
        duration = itemData.get('duration', 0)
        radius = itemData.get('fireworkDist', 0)
        theta = itemData.get('fireworkYawOffset', 0)
        dstPos = utils.getRelativePosition(self.position, self.yaw, theta, radius)
        y_offset = itemData.get('fireworkYOffset', 0)
        dstPos = Math.Vector3(dstPos[0], dstPos[1] + y_offset, dstPos[2])
        if keepEff:
            yaw = 0
            if self.entityId:
                target = BigWorld.entities.get(self.entityId)
                if target and target.inWorld:
                    yaw = (dstPos - target.position).yaw
            fxs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_INPOS, (p.getSkillEffectLv(),
             p.getSkillEffectPriority(),
             self.model,
             keepEff,
             sfx.EFFECT_UNLIMIT,
             dstPos,
             0,
             yaw,
             0,
             duration))
            if fxs:
                self.keepEffs.extend(fxs)

    def releaseKeepEff(self):
        if self.keepEffs:
            for i in self.keepEffs:
                if i:
                    i.stop()

    def leaveWorld(self):
        self.releaseKeepEff()
        super(Firework, self).leaveWorld()

    def getItemData(self):
        return FD.data.get(self.fireworkId, {})
