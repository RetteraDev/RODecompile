#Embedded file name: /WORKSPACE/data/entities/client/fragileobject.o
import BigWorld
import Math
import clientcom
import gameglobal
from sfx import sfx
from iCombatUnit import ICombatUnit
from helpers import fashion
from helpers import modelServer
from helpers import ufo
from helpers import action
from helpers import tintalt
from data import fragile_objects_data as FOD

class FragileObject(ICombatUnit):
    IsFragileObject = True
    COLLIDE_NONE = 0
    COLLIDE_OBSTACLE = 1
    COLLIDE_AM = 2
    COLLIDE_ADD = 3
    TOPLOGO_OFFSET = 0.5

    def __init__(self):
        super(FragileObject, self).__init__()
        self.roleName = FOD.data[self.objId].get('name', '')
        self.bornActionName = FOD.data[self.objId].get('bornAction')
        self.inCombat = False
        self.topLogoOffset = FOD.data.get(self.objId).get('logoOffset', FragileObject.TOPLOGO_OFFSET)
        self.collideType = FOD.data.get(self.objId).get('collideType', FragileObject.COLLIDE_NONE)
        self.obstacleModel = None
        self.hidingPower = 0

    def getItemData(self):
        data = FOD.data.get(self.objId)
        if self.collideType == FragileObject.COLLIDE_OBSTACLE:
            data['collide'] = True
            data['dynamicObstacle'] = True
        return data

    def isUrgentLoad(self):
        return False

    def enterWorld(self):
        self.fashion = fashion.Fashion(self.id)
        self.fashion.loadDummyModel()
        self.initYaw = self.yaw
        self.modelServer = modelServer.SimpleModelServer(self, self.isUrgentLoad())

    def afterModelFinish(self):
        super(FragileObject, self).afterModelFinish()
        self.filter = BigWorld.AvatarFilter()
        self.filter.clientYawMinDist = gameglobal.CLIENT_DEAD_YAW_DIST
        fod = FOD.data.get(self.objId)
        if fod.get('beSelected', 0):
            self.noSelected = False
        else:
            self.noSelected = True
        self.setTargetCapsUse(not self.noSelected)
        if self.collideType == FragileObject.COLLIDE_OBSTACLE:
            self.model.setCollide(True)
            self.model.setPicker(False)
        elif self.collideType == FragileObject.COLLIDE_AM:
            self.collideWithPlayer = True
        elif self.collideType == FragileObject.COLLIDE_ADD:
            self._bindObstacleModel()
        BigWorld.callback(0.5, self.checkCollideWithPlayer)
        if self.topLogo:
            self.topLogo.showBlood(True)
        self.setExtraDirection()
        if self.isSceneObj():
            self.model.isSceneObj = True

    def _bindObstacleModel(self):
        data = FOD.data.get(self.objId)
        scaleMatrix = Math.Matrix()
        mp = Math.MatrixProduct()
        mp.a = scaleMatrix
        mp.b = self.matrix
        modelId = data.get('collideArg', 0)
        modelName = 'char/%d/%d.model' % (modelId, modelId)
        BigWorld.fetchObstacleModel(modelName, mp, True, self._onLoadObstacleModel)

    def _onLoadObstacleModel(self, model):
        if model:
            model.setCollide(True)
            model.setPicker(True)
            model.visible = False
            self.obstacleModel = model
            self.addModel(model)

    def leaveWorld(self):
        super(FragileObject, self).leaveWorld()
        if self.obstacleModel:
            self.delModel(self.obstacleModel)
            self.obstacleModel = None

    def checkCollideWithPlayer(self):
        player = BigWorld.player()
        model = self.model
        if not model or not self.inWorld or player.isAscending or not player.ap:
            return
        if self.isIntersectWithPlayer(model):
            beginPos = Math.Vector3(player.position.x, model.pickbdbox[1][1] + 1.0, player.position.z)
            diffHeight = model.pickbdbox[1][1] - player.position.y + 2
            result = BigWorld.findRectDropPoint(player.spaceID, beginPos, 0.8, 0.8, diffHeight)
            if result != None and result[0][1] > player.position[1]:
                player.ap.beginForceMove(result[0])

    def isIntersectWithPlayer(self, model):
        pos = BigWorld.player().position
        minbd = model.pickbdbox[0] - Math.Vector3(0.5, 2, 0.5)
        maxbd = model.pickbdbox[1] + Math.Vector3(0.5, 0, 0.5)
        return clientcom.isInBoundingBox(minbd, maxbd, pos)

    def getOpacityValue(self):
        return (gameglobal.OPACITY_FULL, True)

    def hide(self, needHide):
        if self.fashion:
            self.fashion.hide(needHide)
        self.setTargetCapsUse(not needHide)

    def stopSpell(self, force):
        pass

    def playDieAction(self):
        if not self.inWorld:
            return
        self.fashion.attachUFO(ufo.UFO_SHADOW)
        fod = FOD.data.get(self.objId)
        if self.collideType == FragileObject.COLLIDE_OBSTACLE:
            modelId = fod.get('collideArg', 0)
            if modelId != 0:
                self.switchModel(modelId)
        elif self.collideType in (FragileObject.COLLIDE_AM, FragileObject.COLLIDE_ADD):
            if self.obstacleModel:
                self.delModel(self.obstacleModel)
                self.obstacleModel = None
        dieActs = fod.get('dieActs', ())
        self.fashion.playAction(dieActs)
        self.afterDieAction()
        deadTint = fod.get('deadTint', None)
        if deadTint:
            self.addTint(deadTint, self.allModels, 0, tintType=tintalt.DIETINT)

    def switchModel(self, modelId):
        clientcom.fetchModel(gameglobal.URGENT_THREAD, self.onSwitchModel, modelId)

    def onSwitchModel(self, model):
        self.fashion.setupModel(model)
        dieActs = FOD.data.get(self.objId).get('dieActs', ())
        self.fashion.playAction(dieActs)
        deadTint = FOD.data.get(self.objId).get('deadTint', None)
        if deadTint:
            self.addTint(deadTint, self.allModels, 0, tintType=tintalt.DIETINT)
        self.afterDieAction()

    def damage(self, host, damageValue, damageAbsorb, mpsValue = 0, attackType = 0, isSkill = False, healAbsorb = None):
        if self.collideType == FragileObject.COLLIDE_OBSTACLE:
            self._actionSimulate()
        else:
            beHitAct = FOD.data.get(self.objId).get('beHitAct', '')
            self.fashion.playAction([beHitAct], action.BEHIT_ACTION, None, 0)

    def _actionSimulate(self):
        pass

    def needBlackShadow(self):
        return False

    def showTargetUnitFrame(self):
        return False

    def playerHitEffect(self, host, clientSkillInfo, extInfo, crit, dmg):
        pass

    def _playInCombatAction(self):
        pass

    def getModelScale(self):
        data = FOD.data.get(self.objId)
        scale = data.get('scale', 1.0)
        self.model.scale = (scale, scale, scale)
        return (scale, scale, scale)

    def resetTopLogo(self):
        super(FragileObject, self).resetTopLogo()
        if self.topLogo:
            self.topLogo.showBlood(True)

    def isSceneObj(self):
        if getattr(self.model, 'isSceneObj', False):
            return self.getItemData().get('isSceneObj', False)
        return False

    def getSkinMaterial(self):
        sd = FOD.data.get(self.objId)
        material = sd.get('skinMaterial', gameglobal.SKIN_MATERIAL_NO)
        return material

    def playEffect(self, effectId, targetPos = None, pitch = 0, yaw = 0, roll = 0, maxDelayTime = -1, scale = 1.0):
        if targetPos is None:
            fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getSkillEffectLv(),
             self.getSkillEffectPriority(),
             self.model,
             effectId,
             sfx.EFFECT_LIMIT,
             maxDelayTime))
        else:
            fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_INPOS, (self.getSkillEffectLv(),
             self.getSkillEffectPriority(),
             self.model,
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
