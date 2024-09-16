#Embedded file name: I:/bag/tmp/tw2/res/entities\client/WingCityBuilding.o
import BigWorld
import Math
import sMath
import const
import utils
import gametypes
import gameglobal
import wingWorldUtils
from helpers import modelServer
from sfx import sfx
from iClient import IClient
from iDisplay import IDisplay
from data import wing_city_building_data as WCBD
from data import wing_city_building_static_data as WCBSD

class WingCityBuilding(IClient, IDisplay):

    def __init__(self):
        super(WingCityBuilding, self).__init__()
        self.trapId = None
        self.campFx = []
        self.isInTrap = False
        self.statusFx = []
        self.obstacleModel = None

    def _getBuildingData(self, key, default = None):
        bdata = WCBD.data.get(self.buildingId, {})
        return bdata.get(key, default)

    def enterWorld(self):
        super(WingCityBuilding, self).enterWorld()
        self.isInTrap = False
        self.modelServer = modelServer.SimpleModelServer(self, self.isUrgentLoad())
        self.filter = BigWorld.DumbFilter()
        self.topLogoOffset = self._getBuildingData('heightOffset', 0)
        radius = self._getBuildingData('radius')
        if radius:
            self.trapId = BigWorld.addPot(self.matrix, radius, self._trapCallback)

    def hasBuildingStatus(self):
        return self._getBuildingData('buildingType') in gametypes.WING_CITY_BUILDING_STATUS_TYPES

    def _getBuildingModelId(self):
        modelId = self._getBuildingData('model')
        if self.hasBuildingStatus():
            modelId = self._getBuildingData('statusModel', [modelId,
             modelId,
             modelId,
             modelId])[self.buildingStatus]
        return modelId

    def _getBuildingData(self, key, default = None):
        sdata = WCBSD.data.get(self.cityEntityNo)
        bdata = WCBD.data.get(sdata.get('buildingId'), {})
        return bdata.get(key, default)

    def releaseStatusEffect(self):
        if self.statusFx:
            for fx in self.statusFx:
                fx.stop()

        self.statusFx = []

    def getItemData(self):
        data = WCBD.data.get(self.buildingId, {})
        modelId = data.get('model', 0)
        if self.hasBuildingStatus():
            modelId = data.get('statusModel', [modelId,
             modelId,
             modelId,
             modelId])[self.buildingStatus]
        scale = data.get('scale', 1.0)
        return {'model': modelId,
         'modelScale': scale}

    def set_buildingStatus(self, old):
        modelServer.loadModelByItemData(self.id, gameglobal.URGENT_THREAD, self.shitfModelFinished, self.getItemData())
        self.attachStatusEffect()

    def shitfModelFinished(self, model):
        self.modelServer._singlePartModelFinish(model)

    def attachStatusEffect(self):
        self.releaseStatusEffect()
        effect = WCBD.data.get(self.buildingId, {}).get('statusEffect', [0,
         0,
         0,
         0])[getattr(self, 'buildingStatus', 0)]
        if effect:
            self.statusFx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
             self.getBasicEffectPriority(),
             self.model,
             effect,
             sfx.EFFECT_LIMIT))

    def leaveWorld(self):
        self.delObstacleModel()
        super(WingCityBuilding, self).leaveWorld()
        self.isInTrap = False
        if self.trapId != None:
            BigWorld.delPot(self.trapId)
            self.trapId = None
        p = BigWorld.player()
        radius = self._getBuildingData('radius')
        if radius and sMath.distance2D(p.position, self.position) > radius:
            BigWorld.player().hideDestroyableItemIcon(self.id)
        self.releaseCampEffect()
        self.releaseStatusEffect()
        self._trapCallback(False, None)

    def _trapCallback(self, enteredTrap, handle):
        if not self.inWorld:
            return
        if enteredTrap:
            self.isInTrap = True
            self._refreshItemIcon()
        else:
            self._hideItemIcon()
            self.isInTrap = False

    def needAttachUFO(self):
        return False

    def canOutline(self):
        return False

    def set_ownerHostId(self, old):
        self._updateName()
        self._refreshItemIcon()
        self.attachCampEffect()

    def set_roleName(self, old):
        self._updateName(self.roleName)

    def _getName(self):
        if self.roleName:
            return self.roleName
        return wingWorldUtils.getBuildingName(self.buildingId, self.ownerHostId)

    def _updateName(self, name = None):
        if not name:
            name = self._getName()
        if self.topLogo.__class__.__name__ != 'TopLogo':
            return
        self.topLogo.name = name
        self.topLogo.updateRoleName(self.topLogo.name)

    def _refreshItemIcon(self):
        pass

    def _hideItemIcon(self):
        pass

    def attachCampEffect(self):
        player = BigWorld.player()
        if player.wingWorldMiniMap:
            self.releaseCampEffect()
            index = player.wingWorldMiniMap.attendHost2ColorIdx.get(self.ownerHostId, 0)
            effect = WCBD.data.get(self.buildingId, {}).get('campEffect', [0,
             0,
             0,
             0])[index]
            effectScale = WCBD.data.get(self.buildingId, {}).get('campEffectScale', 1)
            if effect:
                self.campFx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
                 self.getBasicEffectPriority(),
                 self.model,
                 effect,
                 sfx.EFFECT_LIMIT))
                if self.campFx:
                    for eff in self.campFx:
                        eff.scale(effectScale)

    def releaseCampEffect(self):
        if self.campFx:
            for fx in self.campFx:
                fx.stop()

        self.campFx = []

    def getModelScale(self):
        modelScale = self.getItemData().get('modelScale', 1)
        return (modelScale, modelScale, modelScale)

    def afterModelFinish(self):
        super(WingCityBuilding, self).afterModelFinish()
        self.attachCampEffect()
        self.attachStatusEffect()
        self.createObstacleModel()

    def canOutline(self):
        return True

    def createObstacleModel(self):
        data = WCBD.data.get(self.buildingId, {})
        modelId = data.get('model', 0)
        if data.get('statusObstacleModel'):
            modelId = data.get('statusObstacleModel', [modelId,
             modelId,
             modelId,
             modelId])[getattr(self, 'buildingStatus', 0)]
        else:
            modelId = data.get('obstacleModel')
        scale = 0.95
        if modelId:
            modelName = 'char/%d/%d.model' % (modelId, modelId)
            scaleMatrix = Math.Matrix()
            scaleMatrix.setScale((scale, scale, scale))
            mp = Math.MatrixProduct()
            mp.a = scaleMatrix
            mp.b = self.matrix
            BigWorld.fetchObstacleModel(modelName, mp, True, self.onLoadObstacleModel)

    def onLoadObstacleModel(self, model):
        if not self.inWorld:
            return
        self.delObstacleModel()
        if model:
            self.obstacleModel = model
            self.addModel(model)
            model.setEntity(self.id)
        self.filter = BigWorld.AvatarFilter()

    def delObstacleModel(self):
        if self.obstacleModel:
            self.delModel(self.obstacleModel)
        self.obstacleModel = None
