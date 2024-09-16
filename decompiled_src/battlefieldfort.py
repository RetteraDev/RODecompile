#Embedded file name: /WORKSPACE/data/entities/client/battlefieldfort.o
import BigWorld
import Math
import gamelog
from sfx import sfx
import gameglobal
from helpers import modelServer
from helpers import tintalt
from iClient import IClient
from data import battle_field_fort_data as BFFD

class BattleFieldFort(IClient):

    def __init__(self):
        super(BattleFieldFort, self).__init__()
        self.roleName = ''
        self.oldTempCamp = 0
        self.statusFx = {}
        self.effects = []

    def enterWorld(self):
        super(BattleFieldFort, self).enterWorld()
        self.modelServer = modelServer.SimpleModelServer(self, self.isUrgentLoad())
        self.filter = BigWorld.DumbFilter()

    def afterModelFinish(self):
        super(BattleFieldFort, self).afterModelFinish()
        self.model.setModelNeedHide(0, 0.5)
        self.filter = BigWorld.DumbFilter()
        tintalt.ta_set_static([self.model], self.genTintStr())
        effect = BFFD.data.get(self.fortId, {}).get('effect', 0)
        if effect:
            sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
             self.getBasicEffectPriority(),
             self.model,
             effect,
             sfx.EFFECT_LIMIT))
        self.createObstacleModel()
        self.attachSfxEffect()

    def createObstacleModel(self):
        modelId = BFFD.data.get(self.fortId, {}).get('obstacleModel', 0)
        scale = BFFD.data.get(self.fortId, {}).get('obstacleScale', 0.9)
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
        modelId = BFFD.data.get(self.fortId, {}).get('modelId', 60000)
        return {'model': modelId,
         'modelScale': 1}

    def use(self):
        pass

    def set_curValMap(self, old):
        gamelog.debug('@hjx flag#set_camp:', self.id, old, self.curValMap)
        tintalt.ta_set_static([self.model], self.genTintStr())
        gameglobal.rds.ui.battleField.fortValChanged(self.fortId, self.curValMap)
        effect = BFFD.data.get(self.fortId, {}).get('effect', 0)
        if effect:
            sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
             self.getBasicEffectPriority(),
             self.model,
             effect,
             sfx.EFFECT_LIMIT))
        self.attachSfxEffect()

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
        effects = BFFD.data.get(self.fortId, {}).get('radiusEffect', {}).get(curCamp, [])
        eScale = BFFD.data.get(self.fortId, {}).get('radiusEffectScale', 0.5)
        if effects and effects != self.effects:
            self.effects = effects
            for effectId in effects:
                efs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getBasicEffectLv(),
                 gameglobal.EFF_HIGHEST_PRIORITY,
                 self.model,
                 effectId,
                 sfx.EFFECT_UNLIMIT))
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

    def genTintStr(self):
        if len(self.curValMap) == 0:
            return 'default'
        if self.curValMap.get(1, 0) == 0 and self.curValMap.get(2, 0) == 0:
            return 'default'
        status = 0
        fData = BFFD.data.get(self.fortId, {})
        if self.curValMap.get(BigWorld.player().tempCamp, 0) > 0:
            campStr = '2'
            if self.curValMap[BigWorld.player().tempCamp] > fData.get('limitVal', 50):
                status = 2
            else:
                status = 1
        else:
            campStr = '1'
            if self.curValMap[3 - BigWorld.player().tempCamp] > fData.get('limitVal', 50):
                status = 2
            else:
                status = 1
        return 't_' + campStr + '_' + str(status)
