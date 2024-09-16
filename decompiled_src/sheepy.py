#Embedded file name: /WORKSPACE/data/entities/client/sheepy.o
import math
import random
import BigWorld
import gameglobal
import clientUtils
import iClientOnly

class Sheepy(iClientOnly.IClientOnly):

    def __init__(self):
        super(Sheepy, self).__init__()
        self.walking = True
        self.eating = True
        if hasattr(self, 'noNeedClientTick'):
            self.noNeedClientTick = gameglobal.gNoNeedClientTick
            self.needClientTickDist = gameglobal.gNoNeedClientDist

    def __getattr__(self, name):
        if not self.inWorld:
            raise AttributeError, "type \'%s\' has no attibute \'%s\'" % (type(self), name)
        try:
            return self.__dict__['attrs'][name]
        except KeyError:
            raise AttributeError, "type \'%s\' has no attibute \'%s\'" % (type(self), name)

    def randomYaw(self):
        self.filter.yaw = random.random() * math.pi * 2

    def enterWorld(self):
        pass

    def setupFilter(self):
        self.filter = BigWorld.ClientFilter()
        self.filter.applyDrop = True
        self.filter.position = self.position

    def onModelLoaded(self, model):
        if not self.inWorld:
            return
        if not model:
            return
        self.model = model
        p = BigWorld.player()
        if getattr(self, 'onlyInPhaseShow', False) and p.isInPhase:
            self.model.visible = False
        self.initModel(model)
        self.eating = False
        self.walking = False
        self.randomYaw()

    def initModel(self, model):
        model.scale = (self.scale, self.scale, self.scale)
        am = BigWorld.ActionMatcher(self)
        am.turnModelToEntity = 1
        am.matcherCoupled = 1
        am.inheritOnRecouple = 1
        am.bodyTwistSpeed = 15
        am.matchCaps = [0, 10]
        model.motors = (am,)
        shader = BigWorld.BlendFashion(2)
        shader.distance(75)
        model.distFadeShader = shader

    def seekTo(self, destination, speed):
        if self.eating or self.walking:
            return
        self.walking = True
        self.filter.seek(destination, speed, self.seekFinish)

    def seekFinish(self, finished):
        self.randomYaw()
        self.walking = False

    def leaveWorld(self):
        if hasattr(self.model, 'distFadeShader'):
            self.model.distFadeShader = None
        super(Sheepy, self).leaveWorld()

    def eatGrass(self):
        if self.eating or self.walking:
            return
        action = getattr(self.model, 'idle_0_1', None)
        if not action:
            return
        self.eating = True
        action(0, self.eatGrassFinish)

    def eatGrassFinish(self):
        self.eating = False

    def enterTopLogoRange(self, dist):
        super(Sheepy, self).enterTopLogoRange(dist)
        self.setupFilter()
        clientUtils.fetchModel(gameglobal.DEFAULT_THREAD, self.onModelLoaded, self.modelName)

    def leaveTopLogoRange(self, dist):
        super(Sheepy, self).leaveTopLogoRange(dist)
