#Embedded file name: /WORKSPACE/data/entities/client/clientwingcitybuilding.o
import BigWorld
import Math
import const
import gamelog
import gametypes
import gameglobal
import iClientOnly
from helpers import modelServer
from sfx import sfx
from data import wing_city_building_data as WCBD
from data import wing_city_building_static_data as WCBSD

class ClientWingCityBuilding(iClientOnly.IClientOnly):

    def __getattr__(self, name):
        if not self.inWorld:
            raise AttributeError, "type \'%s\' has no attibute \'%s\'" % (type(self), name)
        try:
            return self.__dict__['attrs'][name]
        except KeyError:
            raise AttributeError, "type \'%s\' has no attibute \'%s\'" % (type(self), name)

    def getItemData(self):
        return {}

    def _getBuildingData(self, key, default = None):
        sdata = WCBSD.data.get(self.cityEntityNo)
        bdata = WCBD.data.get(sdata.get('buildingId'), {})
        return bdata.get(key, default)

    def isGate(self):
        return self._getBuildingData('buildingType') == gametypes.WING_CITY_BUILDING_TYPE_GATE

    def hasBuildingStatus(self):
        return self._getBuildingData('buildingType') in gametypes.WING_CITY_BUILDING_STATUS_TYPES

    def enterWorld(self):
        super(ClientWingCityBuilding, self).enterWorld()
        self._loadBuildingModel()
        self.setupFilter()

    def _getBuildingModelId(self):
        modelId = self._getBuildingData('model')
        if self.hasBuildingStatus():
            modelId = self._getBuildingData('statusModel', [modelId,
             modelId,
             modelId,
             modelId])[self.buildingStatus]
        return modelId

    def _loadBuildingModel(self):
        modelId = self._getBuildingModelId()
        modelServer.loadModelByItemData(self.id, gameglobal.getLoadThread(), self.onModelLoaded, {'model': modelId,
         'modelScale': self._getBuildingData('scale', 1.0)}, False, False)

    def loadImmediately(self):
        return True

    def setupFilter(self):
        self.filter = BigWorld.ClientFilter()
        self.filter.applyDrop = False
        self.filter.position = self.position

    def afterModelFinish(self):
        super(ClientWingCityBuilding, self).afterModelFinish()

    def onModelLoaded(self, model):
        if not self.inWorld:
            return
        if self.model:
            self.model = None
        self.model = model
        entity = BigWorld.entities.get(self.entityID) if hasattr(self, 'entityID') else None
        if entity and entity.inWorld:
            self.model.visible = False
        self.initModel(model)

    def initModel(self, model):
        model.scale = self.getModelScale()
        am = BigWorld.ActionMatcher(self)
        model.motors = (am,)
        obstacleModelId = self._getBuildingData('obstacleModel')
        if obstacleModelId:
            self.createObstacleModel(obstacleModelId)
        if self.isGate():
            self.refreshGate()
        self.attachCampEffect()
        self.attachStatusEffect()

    def getBuildingId(self):
        sdata = WCBSD.data.get(self.cityEntityNo)
        return sdata.get('buildingId')

    def attachStatusEffect(self):
        self.releaseStatusEffect()
        effect = WCBD.data.get(self.getBuildingId(), {}).get('statusEffect', [0,
         0,
         0,
         0])[getattr(self, 'buildingStatus', 0)]
        gamelog.info('jbx:attachStatusEffect', self.cityEntityNo, effect, getattr(self, 'buildingStatus', 0))
        if effect:
            p = BigWorld.player()
            self.statusFx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (p.getBasicEffectLv(),
             p.getBasicEffectPriority(),
             self.model,
             effect,
             sfx.EFFECT_UNLIMIT))

    def attachCampEffect(self):
        p = BigWorld.player()
        if p.wingWorldMiniMap:
            self.releaseCampEffect()
            index = p.wingWorldMiniMap.attendHost2ColorIdx.get(self.ownerHostId, 0)
            effect = WCBD.data.get(self.getBuildingId(), {}).get('campEffect', [0,
             0,
             0,
             0])[index]
            effectScale = WCBD.data.get(self.getBuildingId(), {}).get('campEffectScale', 1.0)
            gamelog.info('jbx:attachCampEffect', self.cityEntityNo, effect, self.ownerHostId)
            if effect:
                self.campFx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (p.getBasicEffectLv(),
                 p.getBasicEffectPriority(),
                 self.model,
                 effect,
                 sfx.EFFECT_UNLIMIT))
                if self.campFx:
                    for eff in self.campFx:
                        eff.scale(effectScale)

    def releaseCampEffect(self):
        if hasattr(self, 'campFx') and self.campFx:
            for fx in self.campFx:
                fx.stop()

        self.campFx = []

    def releaseStatusEffect(self):
        if hasattr(self, 'statusFx') and self.statusFx:
            for fx in self.statusFx:
                fx.stop()

        self.statusFx = []

    def createObstacleModel(self, modelId):
        modelName = 'char/%d/%d.model' % (modelId, modelId)
        scaleMatrix = Math.Matrix()
        scaleMatrix.setScale(self.model.scale)
        mp = Math.MatrixProduct()
        mp.a = scaleMatrix
        mp.b = self.matrix
        BigWorld.fetchObstacleModel(modelName, mp, False, self._onLoadObstacleModel)

    def _onLoadObstacleModel(self, model):
        if not self.inWorld:
            return
        if model:
            model.setCollide(True)
            model.setPicker(True)
            self.addModel(model)

    def setGateStatus(self, old):
        if old != self.gateStatus:
            self.refreshGate()

    def refreshGate(self):
        if not self.inWorld or not self.model:
            return
        if self.gateStatus == const.WING_CITY_GATE_STATUS_OPEN:
            self.model.visible = False
        else:
            self.model.visible = True

    def setBuildingStatus(self, old):
        if old != self.buildingStatus:
            self.refreshBuildingStatus()

    def getModelScale(self):
        modelScale = self._getBuildingData('scale', 1.0)
        return (modelScale, modelScale, modelScale)

    def refreshBuildingStatus(self):
        self._loadBuildingModel()

    def setOwnerHostId(self, old):
        if old != self.ownerHostId:
            pass
        self.attachCampEffect()
