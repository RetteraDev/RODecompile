#Embedded file name: /WORKSPACE/data/entities/client/iboids.o
import random
import BigWorld
import Math
import Pixie
import gameglobal
import clientUtils
import utils
import iNpc
STATE_FLYING = 0
STATE_LANDING = 1
CAP_NEVER = 0

class IBoids(iNpc.INpc):

    def __init__(self):
        super(IBoids, self).__init__()
        self.createDimpleInWater = False
        if hasattr(self, 'noNeedClientTick'):
            self.noNeedClientTick = gameglobal.gNoNeedClientTick
            self.needClientTickDist = gameglobal.gNoNeedClientDist
        self.setTargetCapsUse(False)
        self.topLogo = utils.MyNone
        self.roleName = ''
        self.actions = [self.actionName1, self.actionName2, self.actionName3]

    def getFilter(self):
        ft = BigWorld.BoidsFilter()
        ft.speed = self.speed
        ft.influenceRadius = self.outerradius
        ft.collisionFraction = self.influenceFactor
        ft.pitchShift = self.pitchShift
        ft.turnYawFactor = self.turnYawFactor
        return ft

    def prerequisites(self):
        return [self.modelFile]

    def createModels(self):
        for i in xrange(self.amount - len(self.models)):
            clientUtils.fetchModel(gameglobal.DEFAULT_THREAD, self.onModelLoaded, self.modelFile)

        self.filter.scale = self.scale

    def onModelLoaded(self, model):
        if not model:
            return
        try:
            actions = []
            for action in self.actions:
                if action in model.actionNameList():
                    actions.append(action)

        except:
            return

        model.outsideOnly = 1
        self.addModel(model)
        try:
            if actions:
                model.action(random.choice(actions))(5 * random.random(), None, 0, 1, -100000)
        except:
            utils.reportExcept()

        if self.effectFile:
            effect = clientUtils.pixieFetch(self.effectFile)
            if effect:
                model.root.attach(effect)
                effect.force()
                effect.setAttachMode(0, 0, 0)
        model.visible = self.state == STATE_FLYING

    def enterWorld(self):
        self.filter = self.getFilter()
        BigWorld.callback(0, self.enterWorldAfterWhile)

    def enterWorldAfterWhile(self):
        if self.inWorld:
            matrix = Math.Matrix(self.matrix)
            self.scale = matrix.scale
            self.createModels()

    def leaveWorld(self):
        if self.effectFile:
            for m in self.models:
                m.root.attachments = []

        self.models = []

    def set_state(self, oldState):
        if self.state == STATE_FLYING:
            for boid in self.models:
                boid.visible = 1

    def boidsLanded(self):
        landedBoids = filter(lambda x, pos = self.position: x.position == pos, self.models)
        for boid in landedBoids:
            boid.visible = 0

    def enterClientRange(self, dist):
        pass

    def leaveClientRange(self, dist):
        pass

    def enterTopLogoRange(self, rangeDist = -1):
        pass

    def leaveTopLogoRange(self, rangeDist = -1):
        pass

    def leaveDlgRange(self, unUsedDist):
        pass

    def enterLoadModelRange(self, rangeDist = -1):
        pass

    def leaveLoadModelRange(self, rangeDist = -1):
        pass
