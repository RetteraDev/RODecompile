#Embedded file name: /WORKSPACE/data/entities/client/clanwargate.o
import copy
import BigWorld
import Math
import gameglobal
import clientUtils
from Monster import Monster
from iClanWarCreation import IClanWarCreation
from data import clan_war_gate_model_data as CWGMD
from data import npc_data as ND

class ClanWarGate(Monster, IClanWarCreation):
    IsMonster = False
    IsClanWarUnit = True

    def __init__(self):
        super(ClanWarGate, self).__init__()
        self.applyTints = []
        self.openModel = None
        self.closeModel = None
        self.obstacleModel = None
        self.modelInitInClanWar = False

    def set_guildNUID(self, old):
        self.refreshStateUI()

    def set_clanNUID(self, old):
        self.refreshStateUI()

    def afterModelFinish(self):
        super(ClanWarGate, self).afterModelFinish()
        self.createObstacleModel()
        if self.modelInitInClanWar:
            self.closeModel = self.model
        else:
            self.openModel = self.model
        if self.inClanWar != self.modelInitInClanWar:
            self.refreshModel()

    def createObstacleModel(self):
        modelId = self._getObstacleModelId()
        if modelId:
            modelName = 'char/%d/%d.model' % (modelId, modelId)
            scaleMatrix = Math.Matrix()
            scaleMatrix.setScale((1, 1, 1))
            mp = Math.MatrixProduct()
            mp.a = scaleMatrix
            mp.b = self.matrix
            BigWorld.fetchObstacleModel(modelName, mp, True, self._onLoadObstacleModel)

    def _onLoadObstacleModel(self, model):
        if not self.inWorld:
            return
        if model:
            model.setCollide(True)
            model.setPicker(True)
            self.obstacleModel = model
            self.addModel(model)
            if not self.inClanWar:
                model.setCollide(False)
            else:
                IClanWarCreation.checkCollideWithPlayer(self)

    def set_inClanWar(self, old):
        super(ClanWarGate, self).set_inClanWar(old)
        self.refreshModel()

    def getItemData(self):
        itemData = getattr(self, 'itemData', None)
        if itemData:
            return itemData
        md = copy.deepcopy(super(ClanWarGate, self).getItemData())
        modelId = self._getModelId()
        if modelId:
            md['model'] = modelId
        self.modelInitInClanWar = self.inClanWar
        obastacleModelId = self._getObstacleModelId()
        if obastacleModelId:
            md['obstacleModel'] = obastacleModelId
        self.itemData = md
        return md

    def _getModelId(self):
        mid = ND.data.get(self.markerId).get('functions')[0][2][2]
        data = CWGMD.data.get(mid)
        if self.inClanWar:
            return data.get('closeModel')
        else:
            return data.get('openModel')

    def _getObstacleModelId(self):
        mid = ND.data.get(self.markerId).get('functions')[0][2][2]
        data = CWGMD.data.get(mid)
        return data.get('obstacleModel')

    def refreshModel(self):
        if not self.firstFetchFinished:
            return
        if self.inClanWar:
            if not self.closeModel:
                modelId = self._getModelId()
                modelPath = 'char/%d/%d.model' % (modelId, modelId)
                clientUtils.fetchModel(gameglobal.DEFAULT_THREAD, self._afterCloseModelFinished, modelPath)
            else:
                self._afterCloseModelFinished(self.closeModel)
        elif not self.openModel:
            modelId = self._getModelId()
            modelPath = 'char/%d/%d.model' % (modelId, modelId)
            clientUtils.fetchModel(gameglobal.DEFAULT_THREAD, self._afterOpenModelFinished, modelPath)
        else:
            self._afterOpenModelFinished(self.openModel)

    def _afterCloseModelFinished(self, model):
        if not self.inWorld:
            return
        if self.obstacleModel:
            self.obstacleModel.setCollide(True)
        self.closeModel = model
        if self.firstFetchFinished:
            self.fashion.setupModel(model)
            self.refreshOpacityState()
            self.checkCollideWithPlayer()

    def _afterOpenModelFinished(self, model):
        if not self.inWorld:
            return
        if self.obstacleModel:
            self.obstacleModel.setCollide(False)
        self.openModel = model
        if self.firstFetchFinished:
            self.fashion.setupModel(model)
            self.refreshOpacityState()

    def needAttachUFO(self):
        return False

    def canOutline(self):
        return False

    def isUrgentLoad(self):
        return True
