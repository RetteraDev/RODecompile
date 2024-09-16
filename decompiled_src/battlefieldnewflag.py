#Embedded file name: /WORKSPACE/data/entities/client/battlefieldnewflag.o
import BigWorld
import Math
import gamelog
from sfx import sfx
import gameglobal
from helpers import modelServer
from helpers import tintalt
from iClient import IClient
from data import battle_field_fort_data as BFFD

class BattleFieldNewFlag(IClient):

    def __init__(self):
        super(BattleFieldNewFlag, self).__init__()
        self.roleName = ''
        self.oldTempCamp = 0
        self.statusFx = {}
        self.effects = []

    def enterWorld(self):
        super(BattleFieldNewFlag, self).enterWorld()
        self.modelServer = modelServer.SimpleModelServer(self, self.isUrgentLoad())
        self.filter = BigWorld.DumbFilter()

    def leaveWorld(self):
        super(BattleFieldNewFlag, self).leaveWorld()

    def afterModelFinish(self):
        super(BattleFieldNewFlag, self).afterModelFinish()
        self.model.setModelNeedHide(0, 0.5)
        self.filter = BigWorld.DumbFilter()
        tintalt.ta_set_static([self.model], self.genTintStr())
        effect = BFFD.data.get(self.towerId, {}).get('effect', 0)
        if effect:
            sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
             self.getBasicEffectPriority(),
             self.model,
             effect,
             sfx.EFFECT_LIMIT))
        self.createObstacleModel()
        self.attachSfxEffect()

    def createObstacleModel(self):
        modelId = BFFD.data.get(self.towerId, {}).get('obstacleModel', 0)
        scale = BFFD.data.get(self.towerId, {}).get('obstacleScale', 0.9)
        if modelId:
            modelName = 'char/%d/%d.model' % (modelId, modelId)
            scaleMatrix = Math.Matrix()
            scaleMatrix.setScale((scale, scale, scale))
            mp = Math.MatrixProduct()
            mp.a = scaleMatrix
            mp.b = self.matrix
            BigWorld.fetchObstacleModel(modelName, mp, True, self._onLoadObstacleModel)

    def _onLoadObstacleModel(self, model):
        if model:
            self.obstacleModel = model
            self.addModel(model)
            model.setEntity(self.id)

    def showTargetUnitFrame(self):
        return False

    def getItemData(self):
        modelId = BFFD.data.get(self.towerId, {}).get('modelId', 60000)
        return {'model': modelId,
         'modelScale': 1}

    def use(self):
        pass

    def set_curValMap(self, old):
        tintalt.ta_set_static([self.model], self.genTintStr())
        gameglobal.rds.ui.battleField.fortValChanged(self.towerId, self.curValMap)
        self.attachSfxEffect()
        effect = BFFD.data.get(self.towerId, {}).get('effect', 0)
        if effect:
            sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
             self.getBasicEffectPriority(),
             self.model,
             effect,
             sfx.EFFECT_LIMIT))

    def genTintStr(self):
        if len(self.curValMap) == 0:
            return 'default'
        if self.curValMap.get(1, 0) == 0 and self.curValMap.get(2, 0) == 0:
            return 'default'
        status = 0
        myCamp = BigWorld.player().tempCamp
        otherCamp = 3 - BigWorld.player().tempCamp
        fData = BFFD.data.get(self.towerId, {})
        if self.curValMap.get(myCamp, 0) > self.curValMap.get(otherCamp, 0):
            campStr = '2'
            if self.curValMap[myCamp] >= fData.get('limitVal', 50):
                status = 2
            else:
                status = 1
        elif self.curValMap.get(myCamp, 0) < self.curValMap.get(otherCamp, 0):
            campStr = '1'
            if self.curValMap[otherCamp] >= fData.get('limitVal', 50):
                status = 2
            else:
                status = 1
        return 't_' + campStr + '_' + str(status)

    def attachSfxEffect(self):
        camps = self.genTintStr().split('_')
        curCamp = int(camps[1]) if len(camps) > 1 else 0
        if not curCamp:
            return
        if not self.oldTempCamp:
            self.oldTempCamp = curCamp
        if curCamp != self.oldTempCamp:
            self.releaseSfxEffect()
            self.oldTempCamp = curCamp
        effects = BFFD.data.get(self.towerId, {}).get('radiusEffect', {}).get(curCamp, [])
        eScale = BFFD.data.get(self.towerId, {}).get('radiusEffectScale', 0.5)
        if effects and effects != self.effects:
            self.effects = effects
            for effectId in effects:
                efs = sfx.attachEffectEx(self.model, effectId, 2, 2, 2)
                if efs:
                    self.statusFx[effectId] = efs
                    for ef in efs:
                        ef and ef.scale(eScale)

    def releaseSfxEffect(self):
        if self.statusFx:
            for effectId in self.statusFx.keys():
                sfx.detachEffect(self.model, effectId, self.statusFx[effectId], True)

            self.statusFx = {}
            self.effects = []
