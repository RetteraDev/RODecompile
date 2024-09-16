#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/followModel.o
import BigWorld
import gamelog
from helpers import attachedModelCueFashion

class FollowModel(object):
    __metaclass__ = attachedModelCueFashion.AttachedModelCueFashionMeta

    def __init__(self, entityID, threadID):
        self.entityID = entityID
        self.threadID = threadID
        self.model = None

    def apprach(self, isMoving, speed = 0):
        pass

    def release(self):
        self.entityID = None
        self.threadID = None
        self.model = None


class AvatarFollowModel(FollowModel):

    def __init__(self, entityID, threadID):
        super(AvatarFollowModel, self).__init__(entityID, threadID)

    def loadModel(self):
        entity = BigWorld.entity(self.entityID)
        if not entity or not entity.inWorld:
            return
        self.model = entity.modelServer.bodyModel

    def apprach(self, isMoving, speed = 0):
        pass

    def bored(self, actionName, scale):
        pass

    def follow(self):
        if self.model:
            gamelog.log('m.l@AvatarFollowModel.follow still in follow')
            return
        entity = BigWorld.entity(self.entityID)
        if not entity or not entity.inWorld:
            return
        self.loadModel()
        entity.addModel(self.model)
        follow = BigWorld.Follow()
        follow.target = entity.matrix
        self.followModelBias = 3
        bias = (self.followModelBias, 3, -0.5)
        if entity.model:
            bias = (self.followModelBias, entity.model.height, -0.5)
        follow.biasPos = bias
        follow.biasTolerance = 2
        follow.speedHalflife = 1
        follow.proximityCallback = self.apprach
        if hasattr(follow, 'lineAttach'):
            follow.lineAttach = True
        if hasattr(follow, 'fixedSpeed'):
            follow.fixedSpeed = 2.0
        self.model.addMotor(follow)
        am = BigWorld.ActionMatcher(entity)
        am.matchActionOnly = True
        am.patience = 12.5
        am.boredNotifier = self.bored
        self.model.addMotor(am)

    def cancelFollow(self):
        entity = BigWorld.entity(self.entityID)
        if not entity or not entity.inWorld:
            return
        if self.model:
            if len(self.model.motors) > 0:
                self.model.motors = []
            entity.delModel(self.model)
            self.model = None

    def release(self):
        super(AvatarFollowModel, self).__init__()
        self.cancelFollow()
