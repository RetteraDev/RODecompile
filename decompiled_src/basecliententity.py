#Embedded file name: /WORKSPACE/data/entities/client/basecliententity.o
import math
import BigWorld
import Math
import ResMgr
import gameglobal
import iClientOnly
import utils
from callbackHelper import Functor
from sfx import sfx
import clientUtils

class BaseClientEntity(iClientOnly.IClientOnly):
    PREFAB_MAP = {}
    DEFAULTPREFABID = 10001

    def __init__(self):
        super(BaseClientEntity, self).__init__()
        self.handleCallback = None
        self.isRealModel = True
        self.prefabId = 0
        self.ownerModels = None
        self.loadModelTrapId = None
        self.unloadModelTrapId = None
        self.modelsLoadedNum = 0
        self.extraModels = []
        self.effects = []
        self.lightsModel = []

    def getPrefabId(self):
        pass

    def getPrefabIdPath(self, prefabId):
        pass

    def isUsingPrefabPosDir(self):
        return False

    def isObstacle(self):
        return True

    def showMultiModel(self):
        return False

    def getLoadModelRadius(self):
        return 500

    def getUnloadModelRadius(self):
        return 750

    def __getattr__(self, name):
        try:
            return self.__dict__['attrs'][name]
        except KeyError:
            raise AttributeError, "type \'%s\' has no attibute \'%s\'" % (type(self), name)

    def enterWorld(self):
        loadRadius = self.getLoadModelRadius()
        if loadRadius:
            self.loadModelTrapId = BigWorld.addPot(self.matrix, loadRadius, self._loadModelTrapCallback)
            unloadRadius = self.getUnloadModelRadius()
            if unloadRadius:
                self.unloadModelTrapId = BigWorld.addPot(self.matrix, unloadRadius, self._unloadModelTrapCallback)
        else:
            self.createModels()

    def loadImmediately(self):
        return True

    def leaveWorld(self):
        self.clearModels()
        if self.loadModelTrapId != None:
            BigWorld.delPot(self.loadModelTrapId)
            self.loadModelTrapId = None
        if self.unloadModelTrapId != None:
            BigWorld.delPot(self.unloadModelTrapId)
            self.unloadModelTrapId = None

    def _loadModelTrapCallback(self, enteredTrap, handle):
        if not self.inWorld:
            return
        if enteredTrap:
            self.createModels()

    def _unloadModelTrapCallback(self, enteredTrap, handle):
        if not self.inWorld:
            return
        if not enteredTrap:
            self.clearModels()

    def releaseLights(self):
        if not self.lightsModel:
            return
        for model in self.lightsModel:
            if model:
                try:
                    attaches = model.root.attachments
                    if attaches:
                        for a in attaches:
                            model.root.detach(a)

                    sfx.giveBackDummyModel(model)
                except:
                    pass

        self.lightsModel = []

    def addLight(self, colour, position, innerRadius, outerRadius):
        if len(self.lightsModel) > 25:
            return
        light = BigWorld.Light(colour, outerRadius, innerRadius)
        dummy = sfx.getDummyModel()
        dummy.position = position
        dummy.root.attach(light)
        self.lightsModel.append(dummy)

    def onGetPrefab(self, bExtra, prefabId, ds):
        if not self.inWorld:
            return
        if not ds:
            return
        datasect = ds[0][1]
        if datasect != None:
            names = []
            matrices = []
            effNames = []
            effMatrices = []
            lights = []
            dataitems = datasect.openSection('items')
            if dataitems != None:
                enableGuildLight = gameglobal.rds.configData.get('enableGuildLight', False)
                for v in dataitems.values():
                    if v.sectionName() == 'model':
                        resName = v.readString('resource')
                        resAniName = None
                        resAnimation = v.openSections('animation')
                        frameRateMultiplier = 1.0
                        scriptCueCb = False
                        if resAnimation:
                            resAniName = resAnimation[0].readString('name')
                            frameRateMultiplier = resAnimation[0].readFloat('frameRateMultiplier', 1.0)
                            scriptCueCb = resAnimation[0].readBool('scriptCueCb', False)
                        importance = v.readFloat('importance', 0)
                        names.append((resName,
                         resAniName,
                         importance,
                         frameRateMultiplier,
                         scriptCueCb))
                        matrix = v.readMatrix('prefabTransform')
                        matrices.append(matrix)
                    if v.sectionName() == 'particles':
                        resName = v.readString('resource')
                        effNames.append((resName,))
                        matrix = v.readMatrix('prefabTransform')
                        effMatrices.append(matrix)
                    if enableGuildLight:
                        if v.sectionName() == 'omniLight':
                            try:
                                colour = v.readVector3('colour')
                                position = v.readVector3('position')
                                innerRadius = v.readFloat('innerRadius')
                                outerRadius = v.readFloat('outerRadius')
                                matrix = v.readMatrix('prefabTransform')
                                lights.append((colour,
                                 innerRadius,
                                 outerRadius,
                                 matrix,
                                 position))
                            except:
                                pass

            centerPos = datasect.readVector3('averageOrigin')
            self.PREFAB_MAP[prefabId] = {'models': tuple(names),
             'matrices': tuple(matrices),
             'centerPos': centerPos,
             'effNames': effNames,
             'effMatrices': effMatrices,
             'lights': lights}
            self.doFetchPrefabRes(prefabId, bExtra)
        else:
            self.PREFAB_MAP[prefabId] = {'models': [],
             'matrices': [],
             'centerPos': Math.Vector3(0, 0, 0),
             'effNames': [],
             'effMatrices': [],
             'lights': []}

    def _registerPrefabMap(self, prefabId, bExtra = None):
        if not self.PREFAB_MAP.has_key(prefabId):
            prefab = self.getPrefabIdPath(prefabId)
            ResMgr.bkgOpenSections(Functor(self.onGetPrefab, bExtra, prefabId), prefab)

    def getModelNameList(self):
        prefabId = self.getPrefabId()
        self._registerPrefabMap(prefabId)
        return self.PREFAB_MAP[prefabId]['models']

    def getPrefabIds(self):
        prefabIds = self.getPrefabId()
        if isinstance(prefabIds, int):
            prefabIds = [prefabIds]
        return prefabIds

    def _isExtraPrefab(self, prefabId):
        prefabIds = self.getPrefabIds()
        return prefabId in prefabIds and prefabIds.index(prefabId)

    def isAllModelsLoaded(self):
        prefabIds = self.getPrefabIds()
        modelNum = 0
        for prefabId in prefabIds:
            if not self.PREFAB_MAP.has_key(prefabId):
                return False
            prefabSect = self.PREFAB_MAP[prefabId]
            modelNum += len(prefabSect['models'])

        loadedModelNum = self.modelsLoadedNum
        return modelNum == loadedModelNum

    def createModels(self, prefabIds = None):
        if self.ownerModels != None:
            return
        self.ownerModels = []
        prefabIds = self.getPrefabIds()
        p = BigWorld.player()
        if self.spaceID != p.spaceID:
            return
        self._loadPrefabs(prefabIds)

    def clearEffects(self):
        if self.effects:
            for ef in self.effects:
                if ef:
                    ef.stop()

            self.effects = []

    def doFetchPrefabRes(self, prefabId, bExtra):
        prefabSect = self.PREFAB_MAP[prefabId]
        for i in xrange(len(prefabSect['models'])):
            modelName = prefabSect['models'][i][0]
            aniName = prefabSect['models'][i][1]
            importance = prefabSect['models'][i][2]
            frameRateMultiplier = prefabSect['models'][i][3]
            scriptCueCb = prefabSect['models'][i][4]
            matrix = Math.Matrix(prefabSect['matrices'][i])
            if not self.isUsingPrefabPosDir():
                centerPos = self.position
            else:
                centerPos = prefabSect['centerPos']
            transMatrix = Math.Matrix()
            transMatrix.setTranslate(centerPos)
            matrix.postMultiply(transMatrix)
            if not self.isUsingPrefabPosDir():
                matrixRotate = Math.Matrix()
                matrixRotate.setRotateY(math.radians(self.yaw))
                matrix.preMultiply(matrixRotate)
            if self.isObstacle():
                try:
                    BigWorld.fetchObstacleModel(modelName, matrix, False, Functor(self.onObstacleModelFinish, aniName, bExtra, importance, frameRateMultiplier, scriptCueCb), True)
                except:
                    BigWorld.fetchObstacleModel(modelName, matrix, False, Functor(self.onObstacleModelFinish, aniName, bExtra, importance, frameRateMultiplier, scriptCueCb))

            else:
                clientUtils.fetchModel(gameglobal.URGENT_THREAD, self.onModelFinish, modelName)

        self.clearEffects()
        for i in xrange(len(prefabSect['effNames'])):
            if i > 15:
                break
            effName = prefabSect['effNames'][i][0]
            matrix = Math.Matrix(prefabSect['effMatrices'][i])
            if not self.isUsingPrefabPosDir():
                centerPos = self.position
            else:
                centerPos = prefabSect['centerPos']
            transMatrix = Math.Matrix()
            transMatrix.setTranslate(centerPos)
            transMatrix = Math.Matrix()
            transMatrix.setTranslate(centerPos)
            matrix.postMultiply(transMatrix)
            p = BigWorld.player()
            fx = sfx.attachEffect(gameglobal.ATTACH_EFFECT_INPOS, (p.getSkillEffectLv(),
             p.getSkillEffectPriority(),
             None,
             effName,
             sfx.EFFECT_LIMIT,
             matrix.position,
             0,
             0,
             0,
             -1))
            if fx:
                for e in fx:
                    if e:
                        e.scale(matrix.scale[0], matrix.scale[1], matrix.scale[2])

                self.effects.extend(fx)

        self.analyseLights(prefabSect)

    def analyseLights(self, prefabSect):
        if not prefabSect:
            return
        for i in xrange(len(prefabSect['lights'])):
            if i > 10:
                break
            light = prefabSect['lights'][i]
            colour = light[0]
            innerRadius = light[1]
            outerRadius = light[2]
            matrix = light[3]
            if not self.isUsingPrefabPosDir():
                centerPos = self.position
            else:
                centerPos = prefabSect['centerPos']
            transMatrix = Math.Matrix()
            transMatrix.setTranslate(centerPos)
            transMatrix = Math.Matrix()
            transMatrix.setTranslate(centerPos)
            matrix.postMultiply(transMatrix)
            color = utils.rgb2hex(colour)
            self.addLight(color, matrix.position, innerRadius, outerRadius)

    def _loadPrefabs(self, prefabIds, bExtra = None):
        for idx, prefabId in enumerate(prefabIds):
            if bExtra == None:
                bExtra = idx > 0
            if not self.PREFAB_MAP.has_key(prefabId):
                self._registerPrefabMap(prefabId, bExtra)
            else:
                prefab = self.getPrefabIdPath(prefabId)
                ResMgr.bkgOpenSections(Functor(self.onGetPrefab, bExtra, prefabId), prefab)

    def onObstacleModelFinish(self, aniName, bExtra, importance, frameRateMultiplier, scriptCueCb, model):
        if not self.inWorld:
            return
        self.modelsLoadedNum += 1
        if model and self.ownerModels != None:
            p = BigWorld.player()
            p.addModel(model)
            model.setEntity(self.id)
            model.setUserData(-1)
            model.importance = importance
            if aniName:
                try:
                    model.animation(aniName, frameRateMultiplier, scriptCueCb)
                except:
                    pass

            self.ownerModels.append(model)
            if bExtra:
                self.extraModels.append(model)

    def onModelFinish(self, model):
        if not self.inWorld:
            return
        self.modelsLoadedNum += 1
        if model and self.ownerModels != None:
            p = BigWorld.player()
            p.addModel(model)
            model.position = self.position
            model.scale = (1.0, 1.0, 1.0)
            self.ownerModels.append(model)

    def clearModels(self):
        self.modelsLoadedNum = 0
        if self.ownerModels:
            p = BigWorld.player()
            while self.ownerModels:
                m = self.ownerModels.pop()
                if m and m.inWorld:
                    p.delModel(m)

        self.ownerModels = None
        while self.extraModels:
            self.extraModels.pop()

        self.clearEffects()
        self.releaseLights()

    def clearExtraModels(self):
        if self.extraModels:
            p = BigWorld.player()
            while self.extraModels:
                m = self.extraModels.pop()
                self.ownerModels.remove(m)
                if m and m.inWorld:
                    p.delModel(m)

        self.clearEffects()
