#Embedded file name: /WORKSPACE/data/entities/client/dynamicsceneobject.o
import BigWorld
import Math
import gameglobal
import gamelog
import clientcom
from iNpc import INpc
from callbackHelper import Functor
from sfx import sfx
from data import dynamic_scene_objects_data as DSOD

class DynamicSceneObject(INpc):

    def __init__(self):
        super(DynamicSceneObject, self).__init__()
        self.roleName = DSOD.data.get('name', '')
        self.noCollideModel = None
        self.modelHolder = None

    def getItemData(self):
        data = DSOD.data.get(self.objId, {})
        data['collide'] = True
        data['dynamicObstacle'] = True
        return data

    def needBlackShadow(self):
        data = self.getItemData()
        noBlackUfo = data.get('noBlackUfo', False)
        return not noBlackUfo

    def enterWorld(self):
        super(DynamicSceneObject, self).enterWorld()

    def afterModelFinish(self):
        super(DynamicSceneObject, self).afterModelFinish()
        self.filter = BigWorld.AvatarFilter()
        self.filter.clientYawMinDist = gameglobal.CLIENT_MIN_YAW_DIST
        self.filter.suckPop = False
        self.setTargetCapsUse(False)
        self.model.setCollide(True)
        self.model.setPicker(True)
        self._addNoCollideModel()
        BigWorld.callback(0.1, Functor(self.checkCollideWithPlayer, self.model))
        self.setExtraDirection()

    def _addNoCollideModel(self):
        data = DSOD.data.get(self.objId)
        modelId = data.get('noCollideModel', 0)
        if modelId:
            clientcom.fetchModel(gameglobal.URGENT_THREAD, self.onGetNoCollideModel, modelId)

    def onGetNoCollideModel(self, model):
        if not self.inWorld:
            return
        if model:
            self.noCollideModel = model
            if self.isSceneObj(self.noCollideModel):
                self.noCollideModel.isSceneObj = True
            BigWorld.player().addModel(model)
            self.noCollideModel.position = self.position
            self.noCollideModel.yaw = self.yaw
            self.modelServer.attachEffectFromData(model)
        modelHolder = self.model
        self.fashion.loadDummyModel()
        if not modelHolder or modelHolder.inWorld:
            return
        BigWorld.player().addModel(modelHolder)
        self.modelHolder = modelHolder
        data = DSOD.data.get(self.objId)
        enterAction = data.get('enterAction', '')
        if enterAction:
            try:
                self.noCollideModel.action(enterAction)(0, None, 0, 1.0, 1000)
            except:
                gamelog.error('dynamic action error')

    def leaveWorld(self):
        data = DSOD.data.get(self.objId)
        leaveAction = data.get('leaveAction', '')
        modelHoldTime = data.get('modelHoldTime', 0)
        noCollideModelHoldTime = data.get('noCollideModelHoldTime', 0)
        if self.noCollideModel:
            try:
                self.noCollideModel.action(leaveAction)(0, None, 0, 1.0, 1000)
            except:
                gamelog.error('dynamic action error')

        BigWorld.callback(modelHoldTime, Functor(self.releaseModel, self.modelHolder))
        BigWorld.callback(noCollideModelHoldTime, Functor(self.releaseModel, self.noCollideModel))
        super(DynamicSceneObject, self).leaveWorld()

    def releaseModel(self, modelHolder):
        if modelHolder:
            p = BigWorld.player()
            if not p:
                modelHolder = None
                return
            try:
                p.delModel(modelHolder)
            except:
                pass

            modelHolder = None

    def checkCollideWithPlayer(self, model):
        player = BigWorld.player()
        if not model or not model.inWorld or not model.collidable or not player.ap:
            return
        if clientcom.isIntersectWithPlayer(model) and self.position.distTo(player.position) < 1.0:
            dist = 2.0
            invMatrix = Math.Matrix(model.matrix)
            invMatrix.invert()
            localPos = invMatrix.applyPoint(player.position)
            if localPos.x < 0:
                dstPos = Math.Vector3(0, 0, -dist)
            else:
                dstPos = Math.Vector3(0, 0, dist)
            mat = Math.Matrix(model.matrix)
            dstPos = mat.applyPoint(dstPos)
            player.physics.teleport(dstPos)

    def enterTopLogoRange(self, rangeDist = -1):
        pass

    def leaveTopLogoRange(self, rangeDist = -1):
        pass

    def playEffect(self, effectId, targetPos = None, pitch = 0, yaw = 0, roll = 0, maxDelayTime = -1, scale = 1.0):
        model = self.noCollideModel if self.noCollideModel else self.model
        model.entityId = self.id
        if targetPos is None:
            fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getSkillEffectLv(),
             self.getSkillEffectPriority(),
             model,
             effectId,
             sfx.EFFECT_LIMIT,
             maxDelayTime))
        else:
            fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_INPOS, (self.getSkillEffectLv(),
             self.getSkillEffectPriority(),
             model,
             effectId,
             sfx.EFFECT_LIMIT,
             targetPos,
             pitch,
             yaw,
             roll,
             maxDelayTime))
        if fx:
            for fxItem in fx:
                fxItem.scale(scale, scale, scale)

    def isUrgentLoad(self):
        data = DSOD.data.get(self.objId, {})
        needUrgentLoad = data.get('needUrgentLoad', False)
        return needUrgentLoad

    def isSceneObj(self, model):
        return self.getItemData().get('isSceneObj', False)
