#Embedded file name: /WORKSPACE/data/entities/client/clientship.o
import BigWorld
import const
import gameglobal
import gamelog
import iClientOnly
from helpers import modelServer
from sfx import sfx

class ClientShip(iClientOnly.IClientOnly):

    def __init__(self):
        super(ClientShip, self).__init__()
        self.handleCallback = None
        self.isRealModel = True
        self.moving = False
        self.keepEffects = []

    def __getattr__(self, name):
        if not self.inWorld:
            raise AttributeError, "type \'%s\' has no attibute \'%s\'" % (type(self), name)
        try:
            return self.__dict__['attrs'][name]
        except KeyError:
            raise AttributeError, "type \'%s\' has no attibute \'%s\'" % (type(self), name)

    def enterWorld(self):
        super(ClientShip, self).enterWorld()
        self.setupFilter()
        modelServer.loadModelByItemData(self.id, gameglobal.getLoadThread(), self.onModelLoaded, {'model': self.modelName}, False, False)

    def loadImmediately(self):
        return True

    def setupFilter(self):
        self.filter = BigWorld.ClientFilter()
        applyDrop = True
        if getattr(self, 'noDrop', False):
            applyDrop = False
        self.filter.applyDrop = applyDrop
        self.filter.position = self.position

    def onModelLoaded(self, model):
        if not self.inWorld:
            return
        model.soundCallback(self.actionCueCallback)
        self.model = model
        entity = BigWorld.entities.get(self.entityID) if hasattr(self, 'entityID') else None
        if entity and entity.inWorld:
            self.model.visible = False
        self.initModel(model)

    def attachKeepEffects(self):
        keepEffs = getattr(self, 'keepEffs', [])
        effTime = getattr(self, 'effTime', 0)
        if not keepEffs:
            return
        if keepEffs:
            for i in keepEffs:
                priority = BigWorld.player().getSkillEffectPriority()
                res = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (BigWorld.player().getSkillEffectLv(),
                 priority,
                 self.model,
                 i,
                 sfx.EFFECT_LIMIT_MISC,
                 effTime))
                if res:
                    self.keepEffects += res

    def initModel(self, model):
        model.scale = (self.scale, self.scale, self.scale)
        am = BigWorld.ActionMatcher(self)
        am.turnModelToEntity = 1
        am.matcherCoupled = 1
        am.inheritOnRecouple = 1
        am.bodyTwistSpeed = 15
        am.maxMatchDist = 700
        am.matchCaps = [1, 10]
        model.motors = (am,)
        if self.moving:
            self.seekTo(self.destPos, self.speed)
        self.attachKeepEffects()

    def seekTo(self, destination, speed):
        self.moving = True
        self.destPos = destination
        self.speed = speed
        gamelog.debug('@PGF:ClientShip seekTo', destination, self.filter.position, speed)
        self.filter.seek(destination, speed, self.seekFinish)

    def seekFinish(self, finished):
        self.moving = False

    def leaveWorld(self):
        super(ClientShip, self).leaveWorld()
        keepEffects = getattr(self, 'keepEffects', [])
        if keepEffects:
            for i in keepEffects:
                if i:
                    i.stop()

            self.keepEffects = []
        self.model = None

    def setYaw(self, yaw):
        if self.yaw != yaw:
            self.targetYaw = yaw
            self.deltaYaw = (self.targetYaw - self.yaw) / 200
            if self.handleCallback:
                BigWorld.cancelCallback(self.handleCallback)
            self.handleCallback = None
            self.handleCallback = BigWorld.callback(0, self.setDeltaYaw)
            self.model.action('1110')()

    def setDeltaYaw(self):
        if not self.inWorld:
            return
        if abs(self.targetYaw - self.yaw) < 0.05:
            self.model.action('1110').stop()
            return
        yaw = self.yaw + self.deltaYaw
        self.filter.yaw = yaw
        self.handleCallback = BigWorld.callback(0.1, self.setDeltaYaw)

    def playMonsterDieAction(self):
        try:
            act = self.model.action('1520')()
            getattr(act, '1521')()
        except:
            pass

    def actionCueCallback(self, cueId, data, actionName):
        p = BigWorld.player()
        if not self.inWorld:
            return
        if cueId == 1:
            if p != None:
                params = data.split(':')
                soundPath = str(params[0])
                gameglobal.rds.sound.playFx(soundPath, self.position, False)
                if gameglobal.g_Print_SoundPath:
                    gameglobal.rds.ui.chat.addMessage(const.CHAT_CHANNEL_SYSTEM, soundPath, '')
