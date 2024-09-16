#Embedded file name: /WORKSPACE/data/entities/client/helpers/seqtask.o
"""
\xb8\xc3\xc4\xa3\xbf\xe9\xb9\xa6\xc4\xdc:\xcc\xe1\xb9\xa9\xc5\xc5\xb6\xd3\xbc\xd3\xd4\xd8\xc4\xa3\xd0\xcd\xa3\xac\xcd\xe2\xb2\xbf\xca\xb9\xd3\xc3\xb7\xbd\xb7\xa8\xa3\xba
loader = SeqTask.SeqModelLoader(entityID,threadID,callback)
loader.beginLoad(res)  #  res\xb8\xf1\xca\xbd (fullPath1,('*',dye1), fullPath2,('*',dye2), .....)
\xc4\xa3\xd0\xcd\xbc\xd3\xd4\xd8\xba\xc3\xba\xf3\xa3\xac\xb5\xf7\xd3\xc3callback
callback(model)
\xb9\xa4\xd7\xf7\xb7\xbd\xca\xbd\xa3\xba
SeqTaskMgr\xca\xc7\xb8\xf6\xc8\xab\xbe\xd6\xb5\xc4\xc5\xc5\xb6\xd3\xb5\xf7\xb6\xc8\xb6\xd4\xcf\xf3\xa3\xac\xd3\xd0\xc1\xbd\xb8\xf6\xb6\xd3\xc1\xd0\xa3\xacself.taskCache = deque()\xba\xcdself.fetchCache = []\xa3\xac
taskCache\xb6\xd3\xc1\xd0\xd3\xc3\xd3\xda\xb1\xa3\xb4\xe6\xd2\xd1\xbe\xad\xcd\xea\xb3\xc9\xbc\xd3\xd4\xd8\xc4\xa3\xd0\xcd\xb5\xc4FashionTaskOrder\xb6\xd4\xcf\xf3\xa3\xac\xc4\xbf\xb5\xc4\xca\xc7\xb7\xc0\xd6\xb9\xd4\xda\xb6\xcc\xca\xb1\xbc\xe4\xc4\xda\xba\xf3\xcc\xa8\xcd\xea\xb3\xc9\xb4\xf3\xc1\xbf\xb5\xc4\xbc\xd3\xd4\xd8\xc8\xce\xce\xf1\xa3\xac
\xb5\xbc\xd6\xc2\xbd\xc5\xb1\xbe\xb6\xcc\xc6\xda\xb8\xba\xd4\xd8\xb9\xfd\xb4\xf3\xa3\xac\xcb\xf9\xd2\xd4\xbd\xab\xcd\xea\xb3\xc9\xba\xf3\xcc\xa8\xbc\xd3\xd4\xd8\xc8\xce\xce\xf1\xb5\xc4\xb6\xd4\xcf\xf3\xbd\xf8\xd0\xd0\xc5\xc5\xd0\xf2\xa3\xac\xd2\xc0\xb4\xce\xc8\xc3\xbd\xc5\xb1\xbe\xb4\xa6\xc0\xed\xbc\xd3\xd4\xd8\xcd\xea\xb1\xcf\xb5\xc4\xc4\xa3\xd0\xcd
fetchCache\xd3\xc3\xd3\xda\xbc\xd3\xd4\xd8\xb7\xb6\xce\xa7\xbf\xd8\xd6\xc6\xa3\xac\xbc\xf5\xc9\xd9\xbc\xd3\xd4\xd8\xc8\xce\xce\xf1\xa3\xac\xd2\xd4\xbc\xb0\xd7\xdf\xbd\xf8\xb6\xc8\xcc\xf5\xb5\xc4\xca\xb1\xba\xf2\xb4\xe6\xb4\xa2\xbc\xd3\xd4\xd8\xc8\xce\xce\xf1\xa1\xa3\xd3\xce\xcf\xb7\xd6\xd0\xbf\xc9\xd2\xd4\xb6\xaf\xcc\xac\xb5\xf7\xd5\xfbentity\xc4\xa3\xd0\xcd\xbc\xd3\xd4\xd8\xb5\xc4
\xb0\xeb\xbe\xb6\xa3\xac\xc8\xe7\xb9\xfbentity\xb4\xa6\xd3\xda\xb7\xb6\xce\xa7\xd6\xae\xcd\xe2\xa3\xac\xd5\xe2\xb1\xbb\xbc\xd3\xc8\xebfetchCache\xb6\xd3\xc1\xd0\xa3\xac\xb2\xbb\xcc\xe1\xbd\xbb\xd2\xfd\xc7\xe6\xbd\xf8\xd0\xd0\xbc\xd3\xd4\xd8\xa3\xac\xc4\xdc\xbc\xf5\xc7\xe1\xd3\xce\xcf\xb7\xb5\xc4\xb8\xba\xd4\xd8
"""
import Math
import BigWorld
import gameglobal
import types
import gametypes
import clientcom
import utils
import gamelog
import tintalt as TA
from collections import deque
from callbackHelper import Functor
from gameclass import Singleton
import clientUtils
gEnableQueue = True

def clearTintState(res):
    for dyeTintData in res:
        if type(dyeTintData) is tuple:
            for dyeTint in dyeTintData:
                if type(dyeTint) is str:
                    if dyeTint.find('@TA.') != -1:
                        TA.setContentStateNoUse(dyeTint)


def isNeedToLoad(entity):
    if not entity or not entity.inWorld:
        return False
    needToLoad = True
    if hasattr(entity, 'getOpacityValue'):
        opacityValue = entity.getOpacityValue()
        if opacityValue:
            needToLoad = opacityValue[0] in (gameglobal.OPACITY_FULL, gameglobal.OPACITY_TRANS, gameglobal.OPACITY_HIDE_WITHOUT_NAME)
            needToLoad = needToLoad or entity.__class__.__name__ == 'HomeFurniture'
            if getattr(entity, 'hidingPower', 0):
                needToLoad = True
    return needToLoad


class ModelMemoryCtrl(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.avatarModelCnt = 0
        self.monsterModelCnt = 0
        self.spriteCnt = 0

    def isNeedRealModel(self, entity):
        if entity.isRealModel:
            return False
        if hasattr(entity, 'getOpacityValue') and entity.getOpacityValue()[0] == gameglobal.OPACITY_HIDE:
            return False
        return True

    def shouldLoadRealModel(self, entity):
        if gameglobal.ignorePerformanceLimit:
            return True
        if not entity or not entity.inWorld:
            return False
        if gameglobal.rds.GameState <= gametypes.GS_LOGIN:
            return True
        if entity.model and not getattr(entity.model, 'dummyModel', False):
            return True
        if hasattr(entity, 'bianshen') and entity.bianshen[0] == gametypes.BIANSHEN_ZAIJU and entity.bianshen[1] in gametypes.WW_ROB_ZAI_JU_ID:
            return True
        if self.isNeedRealModel(entity):
            entity.isRealModel = True
            if utils.instanceof(entity, 'Avatar') or utils.instanceof(entity, 'AvatarRobot'):
                self.incAvatarModel()
            elif utils.instanceof(entity, 'SummonedSprite'):
                self.incSummonedSprite()
            elif utils.instanceof(entity, 'Monster'):
                self.incMonsterModel()
            return True
        entityId = entity.id
        memorySize = BigWorld.getMemoryInfo()[0]
        p = BigWorld.player()
        entity.isRealModel = False
        if not p:
            return True
        if (utils.instanceof(entity, 'Avatar') or utils.instanceof(entity, 'AvatarRobot')) and entityId != p.id:
            if not p.isInMyTeam(entity):
                if gameglobal.MEMORY_LIMIT_FLAG and memorySize > gameglobal.MEMORY_LIMIT_SUM or self.avatarModelCnt >= gameglobal.rds.avatarModelCnt:
                    if entity and hasattr(entity, 'alwaysShowModel') and entity.alwaysShowModel():
                        return True
                    return False
            self.incAvatarModel()
        if utils.instanceof(entity, 'Monster'):
            if hasattr(entity, 'getOpacityValue') and entity.getOpacityValue()[0] == gameglobal.OPACITY_HIDE:
                return False
        elif utils.instanceof(entity, 'Monster') or utils.instanceof(entity, 'AvatarMonster'):
            if not (p.targetLocked and p.targetLocked.id == entityId) and self.monsterModelCnt >= gameglobal.MONSTER_MODEL_CNT:
                return False
            self.incMonsterModel()
        if utils.instanceof(entity, 'SummonedSprite'):
            spriteMaxCnt = gameglobal.rds.configData.get('maxSpriteModelCnt', 0)
            if spriteMaxCnt <= 0:
                spriteMaxCnt = gameglobal.rds.avatarModelCnt / 2
            if not (p.targetLocked and p.targetLocked.id == entityId) and entity.ownerId != p.id and self.spriteCnt >= spriteMaxCnt:
                return False
            self.incSummonedSprite()
        entity.isRealModel = True
        return True

    def incAvatarModel(self):
        self.avatarModelCnt += 1

    def decAvatarModel(self):
        self.avatarModelCnt -= 1

    def incMonsterModel(self):
        self.monsterModelCnt += 1

    def decMonsterModel(self):
        self.monsterModelCnt -= 1

    def incSummonedSprite(self):
        self.spriteCnt += 1

    def decSummonedSprite(self):
        self.spriteCnt -= 1

    def countReset(self):
        self.avatarModelCnt = 0
        self.monsterModelCnt = 0
        self.spriteCnt = 0


def modelMemoryCtrl():
    return ModelMemoryCtrl.getInstance()


def shouldLoadRealModel(entity):
    return ModelMemoryCtrl.getInstance().shouldLoadRealModel(entity)


def needHideEntity(entity):
    if utils.instanceof(entity, 'Avatar') or utils.instanceof(entity, 'Monster'):
        return entity.getOpacityValue()[0] == gameglobal.OPACITY_HIDE
    else:
        return False


class ParentOrder(object):

    def __init__(self):
        super(ParentOrder, self).__init__()

    def doTask(self):
        pass

    def canDoTask(self):
        return True

    def release(self):
        pass


class FashionTaskOrder(ParentOrder):

    def __init__(self, callback, loadID, model):
        super(FashionTaskOrder, self).__init__()
        self.expire = False
        self.callback = callback
        self.model = model
        self.loadID = loadID

    def doTask(self):
        self.callback(self.loadID, self.model)
        self.callback = None
        self.model = None
        self.loadID = None

    def release(self):
        self.expire = True
        self.callback = None
        self.model = None
        self.loadID = None


class FetchOrder(ParentOrder):

    def __init__(self, entity, threadID, callback, resPath):
        super(FetchOrder, self).__init__()
        self.entity = entity
        self.threadID = threadID
        self.callback = callback
        self.resPath = resPath
        self.expire = False
        self.fetchID = -1

    def doTask(self):
        if not self.expire:
            gamelog.debug('zf:FetchOrder::doTask .........')
            self.fetchID = clientUtils.fetchModel(self.threadID, self.callback, *self.resPath)
            self.callback = None
            self.entity = None
            self.resPath = None
            self.expire = True

    def release(self, cancelFetch = False):
        self.entity = None
        self.callback = None
        self.resPath = None
        self.expire = True
        if cancelFetch and self.fetchID != -1:
            BigWorld.cancelBgTask(self.fetchID)


class ModelLoadingChecker(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.clear()

    def clear(self):
        self.loadingSet = set()
        self.loadedSet = set()

    def inLoading(self, resPath):
        if isinstance(resPath, list):
            resPath = resPath[0]
        return resPath in self.loadingSet

    def addLoadingRes(self, resPath):
        if isinstance(resPath, list):
            resPath = resPath[0]
        if resPath not in self.loadedSet:
            self.loadingSet.add(resPath)

    def removeLoadingRes(self, resPath, addLoaded = True):
        if isinstance(resPath, list):
            resPath = resPath[0]
        if resPath in self.loadingSet:
            self.loadingSet.remove(resPath)
        if addLoaded:
            self.loadedSet.add(resPath)


class FurnitureFetchOrder(FetchOrder):

    def __init__(self, entity, threadID, callback, resPath):
        super(FurnitureFetchOrder, self).__init__(entity, threadID, callback, resPath)
        self.loadedChecker = ModelLoadingChecker.getInstance()

    def canDoTask(self):
        return not self.loadedChecker.inLoading(self.resPath)

    def doTask(self):
        if not self.expire:
            gamelog.debug('bgf:FurnitureFetchOrder::doTask .........')
            self.fetchID = clientUtils.fetchModel(self.threadID, self._afterFetchFinished, *self.resPath)
            self.loadedChecker.addLoadingRes(self.resPath)
            self.entity = None
            self.expire = True

    def _afterFetchFinished(self, model):
        self.loadedChecker.removeLoadingRes(self.resPath, True)
        if self.callback:
            self.callback(model)
        self.callback = None

    def release(self, cancelFetch = False):
        self.entity = None
        self.callback = None
        self.expire = True
        if cancelFetch and self.fetchID != -1:
            self.loadedChecker.removeLoadingRes(self.resPath, False)
            BigWorld.cancelBgTask(self.fetchID)
        self.resPath = None


class NosServiceOrder(ParentOrder):

    def __init__(self, actionType, actionArgs, callback):
        super(NosServiceOrder, self).__init__()
        self.actionType = actionType
        self.actionArgs = actionArgs
        self.callback = callback
        self.expire = False
        self.fetchID = -1

    def doTask(self):
        if self.actionType == gametypes.NOS_SERVICE_UPLOAD:
            md5, timeStamp, filePath, fileType, fileSrc, extra = self.actionArgs
            clientcom.uploadFileToNos(md5, timeStamp, filePath, fileType, fileSrc, extra, self.callback)
        elif self.actionType == gametypes.NOS_SERVICE_DOWNLOAD:
            directory, key, fileType, status = self.actionArgs
            clientcom.downloadFileFromNos(directory, key, fileType, status, self.callback)
        elif self.actionType == gametypes.NOS_SERVICE_STATUS_CHECK:
            player = BigWorld.player()
            key, = self.actionArgs
            player.base.fetchNOSFileStatus(key)
        elif self.actionType == gametypes.NOS_SERVICE_STATUS_CROSS_CHECK:
            player = BigWorld.player()
            key, serverId = self.actionArgs
            player.base.fetchCrossNOSFileStatus(key, serverId)
        elif self.actionType == gametypes.SOUND_FILE_UPLOAD:
            filePath, extra = self.actionArgs
            clientcom.uploadSound(self.actionType, filePath, extra, self.callback)
        elif self.actionType == gametypes.SOUND_FILE_DOWNLOAD:
            key, extra = self.actionArgs
            clientcom.downloadSound(self.actionType, key, extra, self.callback)
        elif self.actionType == gametypes.SOUND_FILE_TRANSLATE:
            key, extra = self.actionArgs
            clientcom.getTranslation(self.actionType, key, extra, self.callback)

    def release(self):
        self.expire = True
        if self.fetchID != -1:
            pass


class BkgModelLoader(object):

    def __init__(self, entity, threadID, res, callback, loadID):
        self.callback = callback
        self.loadID = loadID
        self.res = res
        if threadID == gameglobal.MAIN_THREAD and callback:
            model = clientcom.loadModelMainThread(res)
            self.fetchID = 0
            self.fetchOrder = None
            callback(loadID, model)
            return
        p = BigWorld.player()
        pos = p.position if p else (0, 0, 0)
        distToPlayer = (entity.position - pos).length
        if hasattr(entity, 'notLoadModelRange') and entity.notLoadModelRange:
            return
        needToLoad = isNeedToLoad(entity)
        if not needToLoad:
            waiting = True
        elif distToPlayer > gameglobal.loadingDist:
            waiting = not entity.loadImmediately()
        elif gameglobal.rds.GameState == gametypes.GS_LOADING:
            if hasattr(entity, 'npcInstance'):
                if distToPlayer > gameglobal.npcPriorityDist:
                    waiting = True
                else:
                    waiting = False
            else:
                waiting = True
        else:
            waiting = False
        if waiting:
            if utils.instanceof(entity, 'HomeFurniture'):
                self.fetchOrder = FurnitureFetchOrder(entity, threadID, self._fetchFinish, res)
            else:
                self.fetchOrder = FetchOrder(entity, threadID, self._fetchFinish, res)
            addFetchOrder(self.fetchOrder)
            self.fetchID = 0
        else:
            self.fetchOrder = None
            self.fetchID = clientUtils.fetchModel(threadID, self._fetchFinish, *res)

    def _fetchFinish(self, model):
        if self.callback:
            self.callback(self.loadID, model)
            if self.fetchOrder:
                self.fetchOrder.release()
                self.fetchOrder = None
            self.callback = None
            self.fetchID = 0

    def cancel(self):
        clearTintState(self.res)
        if self.fetchOrder:
            self.fetchOrder.release(True)
        if self.fetchID:
            BigWorld.cancelBgTask(self.fetchID)
        self.callback = None
        self.loadID += 1


class SeqModelLoader(object):

    def __init__(self, entityID, threadID, modelOkCallback):
        self.entityID = entityID
        self.threadID = threadID
        self.modelOkCallback = modelOkCallback
        self.loader = None
        self.loadID = 0
        self.taskOrder = None
        self.matterDyePairs = []

    def beginLoad(self, res, urgent = False):
        self.loadID += 1
        entity = BigWorld.entity(self.entityID)
        if self.loader:
            self.loader.cancel()
        if hasattr(entity, 'notLoadModelRange') and entity.notLoadModelRange:
            clearTintState(res)
            return
        threadID = self.threadID
        self.matterDyePairs = clientcom.parseMatterDyePair(res)
        if threadID == gameglobal.MAIN_THREAD:
            model = clientcom.loadModelMainThread(res)
            if urgent:
                self._modelLoadFinishUrgent(self.loadID, model)
            else:
                self._modelLoadFinish(res, self.loadID, model)
            return
        if threadID == gameglobal.URGENT_THREAD:
            if urgent:
                self.fetchID = clientUtils.fetchModel(threadID, Functor(self._modelLoadFinishUrgent, self.loadID), *res)
            else:
                self.fetchID = clientUtils.fetchModel(threadID, Functor(self._modelLoadFinish, res, self.loadID), *res)
            self.loader = None
        else:
            self.loader = BkgModelLoader(entity, threadID, res, Functor(self._modelLoadFinish, res), self.loadID)

    def _modelLoadFinishUrgent(self, loadID, model):
        if self.loadID != loadID:
            return
        entity = BigWorld.entity(self.entityID)
        afterFinishSetStatic(entity, model, self.matterDyePairs)
        if self.modelOkCallback:
            self.modelOkCallback(model)
            self.modelOkCallback = None

    def _modelLoadFinish(self, res, loadID, model):
        if self.loadID != loadID:
            return
        self.loader = None
        if not model:
            if model == 0:
                self.cancel()
                return
            if not BigWorld.isPublishedVersion():
                checkResources(res)
            gamelog.error('Error .... load model failed! use default model', self.entityID, gameglobal.defaultModelName)
            if not BigWorld.isPublishedVersion():
                try:
                    model = clientUtils.model(gameglobal.defaultModelName)
                except:
                    return

        if self.taskOrder:
            self.taskOrder.release()
        entity = BigWorld.entity(self.entityID)
        afterFinishSetStatic(entity, model, self.matterDyePairs)
        self.taskOrder = FashionTaskOrder(self._doSeqTask, loadID, model)
        addSeqTask(self.taskOrder)

    def _doSeqTask(self, loadID, model):
        if loadID != self.loadID:
            return
        if self.taskOrder:
            self.taskOrder.release()
            self.taskOrder = None
        if self.modelOkCallback:
            self.modelOkCallback(model)
            self.modelOkCallback = None

    def cancel(self):
        if self.loader:
            self.loader.cancel()
            self.loader = None
        if self.taskOrder:
            self.taskOrder.release()
            self.taskOrder = None
        self.modelOkCallback = None
        self.loadID += 1


class SeqModelUpdater(object):

    def __init__(self, model, threadID, modelOkCallback):
        self.model = model
        self.threadID = threadID
        self.modelOkCallback = modelOkCallback
        self._updaing = False
        self._updateCache = []
        self.updateID = 0

    def beginUpdate(self, oldRes, res, oldDyes, dyes, tints):
        self._updateCache.append((oldRes,
         res,
         oldDyes,
         dyes,
         tints))
        if not self._updaing:
            if self._doUpdate():
                self._updaing = True

    def _doUpdate(self):
        l = len(self._updateCache)
        if l == 0:
            return False
        oldRes = self._updateCache[0][0]
        res = self._updateCache[l - 1][1]
        oldDyes = self._updateCache[0][2]
        dyes = self._updateCache[l - 1][3]
        tints = self._updateCache[l - 1][4]
        self._updateCache[:l] = []
        oldPathList = list(set(oldRes) - set(res))
        newPathList = list(set(res) - set(oldRes))
        if not oldPathList and not newPathList:
            if oldDyes != dyes:
                self._modelUpdateFinish(self.updateID, True)
            return False
        currentRes = list(self.model.sources)
        clientcom.checkRes(currentRes)
        if set(currentRes) == set(res):
            self._modelUpdateFinish(self.updateID, True)
            return False
        if tints:
            newPathList.extend(tints)
        self.updateID += 1
        gamelog.debug('b.e.:seqModelUpdater._doUpdate', oldPathList, newPathList)
        self.model.replaceSubModel(self.threadID, Functor(self._modelUpdateFinish, self.updateID), tuple(oldPathList), tuple(newPathList))
        return True

    def _modelUpdateFinish(self, updateID, r):
        if not r:
            gamelog.error('b.e.:replaceSubModel error! Please check configs or resouces!')
        if self.updateID != updateID:
            return
        if not self._doUpdate():
            self._updaing = False
            if self.modelOkCallback:
                self.modelOkCallback()

    def release(self):
        self.modelOkCallback = None
        self._updaing = False
        self._updateCache[:] = []
        self.updateID += 1


class SeqTaskMgr(object):

    def __init__(self):
        super(SeqTaskMgr, self).__init__()
        self.taskCache = deque()
        self.fetchCache = []
        self.checkInterval = 0.1
        self.checkMaxCache = 2000
        self.cycle = True
        self.forceLoad = False

    def setForceLoad(self, value):
        if not self.forceLoad and value:
            gameglobal.loadingDist = gameglobal.MIN_LOADING_DIST
            ModelLoadingChecker.getInstance().clear()
        self.forceLoad = value

    def isEmpty(self):
        return len(self.taskCache) == 0

    def addTask(self, task):
        if len(self.taskCache) > self.checkMaxCache:
            return
        self.taskCache.appendleft(task)

    def addFetch(self, order):
        if len(self.fetchCache) > self.checkMaxCache:
            return
        self.fetchCache.append(order)

    def start(self):
        self.__cycleCheck()

    def __cycleCheck(self):
        try:
            self.__doTaskOrder()
            self.__doFetchOrder()
        except Exception as e:
            gamelog.error('m.l@SeqTaskMgr.__cycleCheck error', e.message)
            utils.reportExcept()

        if self.cycle:
            BigWorld.callback(self.checkInterval, self.__cycleCheck)

    def __doTaskOrder(self):
        if len(self.taskCache) > 0:
            task = self.taskCache.pop()
            while task.expire == True and len(self.taskCache) > 0:
                task = self.taskCache.pop()

            if not task.expire:
                task.expire = True
                try:
                    task.doTask()
                except Exception as e:
                    gamelog.error('zf:Error doTask except', e.message)

    def __doFetchOrder(self):
        if gameglobal.rds.GameState == gametypes.GS_LOADING and not self.forceLoad:
            gameglobal.loadingDist = gameglobal.MIN_LOADING_DIST
            return
        ppos = Math.Vector3(0, 0, 0)
        p = BigWorld.player()
        if p:
            ppos = p.position
        loadDistSquared = gameglobal.loadingDist
        loadDistSquared = loadDistSquared * loadDistSquared
        nearestFetch = None
        nearestDist = 10000000.0
        isFetched = False
        for i in self.fetchCache:
            en = i.entity
            if i.expire:
                self.fetchCache.remove(i)
            elif not en or not en.inWorld:
                clearTintState(i.resPath)
                if i.callback:
                    i.callback(0)
                i.release()
                self.fetchCache.remove(i)
            else:
                distSq = ppos.distSqrTo(en.position)
                if distSq < loadDistSquared and gameglobal.rds.GameState >= gametypes.GS_LOADING or gameglobal.rds.GameState < gametypes.GS_LOADING:
                    needToLoad = isNeedToLoad(en)
                    if not needToLoad:
                        continue
                    if i.canDoTask():
                        try:
                            i.doTask()
                        except Exception as e:
                            gamelog.error('m.l@SeqTaskMgr.__doFetchOrder error', e.message)
                            utils.reportExcept()

                        self.fetchCache.remove(i)
                        isFetched = True
                if not isFetched:
                    if nearestDist > distSq:
                        nearestDist = distSq
                        nearestFetch = i

        unload = BigWorld.bgTaskTotalLoad()
        if not isFetched and len(self.fetchCache) > 0 and unload < 5 and nearestDist < gameglobal.MAX_LOADING_DIST * gameglobal.MAX_LOADING_DIST:
            if nearestFetch.canDoTask():
                try:
                    nearestFetch.doTask()
                except Exception as e:
                    gamelog.error('m.l@SeqTaskMgr.__doFetchOrder error', e.message)
                    utils.reportExcept()

                self.fetchCache.remove(nearestFetch)
        delta = 1.2 - (gameglobal.loadingDist - gameglobal.MIN_LOADING_DIST) / (gameglobal.MAX_LOADING_DIST - gameglobal.MIN_LOADING_DIST)
        if unload > 1:
            gameglobal.loadingDist -= delta * 2
        elif len(self.fetchCache) > 0:
            gameglobal.loadingDist += delta
        else:
            gameglobal.loadingDist -= max(0.5, delta * 2)
        if gameglobal.loadingDist > gameglobal.MAX_LOADING_DIST:
            gameglobal.loadingDist = gameglobal.MAX_LOADING_DIST
        elif gameglobal.loadingDist < gameglobal.MIN_LOADING_DIST:
            gameglobal.loadingDist = gameglobal.MIN_LOADING_DIST


class NOSDownLoadTaskMgr(SeqTaskMgr):

    def __init__(self):
        super(NOSDownLoadTaskMgr, self).__init__()
        self.checkInterval = 10
        self.lastTaskTime = utils.getNow()
        self.isDownload = False

    def isEmpty(self):
        return len(self.taskCache) == 0

    def addTask(self, task):
        self.taskCache.appendleft(task)
        if not self.isDownload:
            self.__doTaskOrder()

    def onTaskDone(self):
        self.isDownload = False
        self.__doTaskOrder()

    def start(self):
        self.__cycleCheck()

    def __cycleCheck(self):
        try:
            if not self.isDownload or utils.getNow() > self.lastTaskTime + self.checkInterval:
                self.__doTaskOrder()
        except Exception as e:
            gamelog.error('m.l@NOSDownLoadTaskMgr.__cycleCheck error', e.message)
            utils.reportExcept()

        if self.cycle:
            BigWorld.callback(self.checkInterval, self.__cycleCheck)

    def __doTaskOrder(self):
        if len(self.taskCache) > 0:
            task = self.taskCache.pop()
            while task.expire == True and len(self.taskCache) > 0:
                task = self.taskCache.pop()

            if not task.expire:
                task.expire = True
                try:
                    self.isDownload = True
                    self.lastTaskTime = utils.getNow()
                    task.doTask()
                except Exception as e:
                    gamelog.error('zf:Error NOSDownLoadTaskMgr.__doTaskOrder except', e.message)


gNOSDownloadTaskMgr = None
gSoundRecordTaskMgr = None
gTaskMgr = None

def addSeqTask(taskOrder):
    global gTaskMgr
    global gEnableQueue
    if gTaskMgr == None:
        gTaskMgr = SeqTaskMgr()
        gTaskMgr.start()
    if gEnableQueue:
        gTaskMgr.addTask(taskOrder)
    else:
        taskOrder.expire = True
        taskOrder.doTask()


def addFetchOrder(fetchOrder):
    global gTaskMgr
    if gTaskMgr == None:
        gTaskMgr = SeqTaskMgr()
        gTaskMgr.start()
    gTaskMgr.addFetch(fetchOrder)


def checkResources(res):
    try:
        it = iter(res)
    except Exception as e:
        gamelog.error('m.l@seqTask.checkResources error', e.message)
        checkResource(res)
        return

    for res in it:
        checkResource(res)


def checkResource(res):
    if not isinstance(res, types.StringTypes):
        return
    if not clientcom.isFileExist(res):
        gamelog.error('resource %s is not available!!!' % res)


gNOSTaskMgr = None
gNosDLCallBackMgr = None

class AyncCallBackOrder(ParentOrder):

    def __init__(self, key, callback):
        super(AyncCallBackOrder, self).__init__()
        self.key = key
        self.callback, self.args = callback
        self.expire = False
        self.fetchID = -1

    def doTask(self):
        if self.callback:
            self.callback(self.key, *self.args)


def addNOSSeqTask(actionType, args, callback):
    global gSoundRecordTaskMgr
    global gNOSDownloadTaskMgr
    global gNOSTaskMgr
    if gNOSTaskMgr == None:
        gNOSTaskMgr = SeqTaskMgr()
        gNOSTaskMgr.checkInterval = 0.3
        gNOSTaskMgr.start()
    if gNOSDownloadTaskMgr == None:
        gNOSDownloadTaskMgr = NOSDownLoadTaskMgr()
        gNOSDownloadTaskMgr.start()
    player = BigWorld.player()
    if actionType == gametypes.NOS_SERVICE_UPLOAD:
        md5, timeStamp, filePath, fileType, fileSrc, extra = args
        taskOrder = NosServiceOrder(gametypes.NOS_SERVICE_UPLOAD, (md5,
         timeStamp,
         filePath,
         fileType,
         fileSrc,
         extra), callback)
        if len(gNOSTaskMgr.taskCache) < 1000:
            gNOSTaskMgr.addTask(taskOrder)
    elif actionType == gametypes.NOS_SERVICE_DOWNLOAD:
        directory, key, fileType, status = args
        if player.nosDownListCallbacks.has_key(key):
            player.nosDownListCallbacks[key].append(callback)
            return
        player.nosDownListCallbacks[key] = [callback]
        taskOrder = NosServiceOrder(gametypes.NOS_SERVICE_DOWNLOAD, (directory,
         key,
         fileType,
         status), (downLoadCallback, (key,)))
        if len(gNOSDownloadTaskMgr.taskCache) < 1000:
            gNOSDownloadTaskMgr.addTask(taskOrder)
    elif actionType == gametypes.NOS_SERVICE_STATUS_CHECK:
        filePath, key, fileType = args
        if player.nosStatusFetchCallbacks.has_key(key):
            player.nosStatusFetchCallbacks[key].append((filePath,
             fileType,
             callback[0],
             callback[1]))
            now = utils.getNow()
            nosTimeStamp = player.nosStatusFetchCallbacksTimeStamp.get(key, 0)
            if nosTimeStamp and now - nosTimeStamp > 10:
                taskOrder = NosServiceOrder(gametypes.NOS_SERVICE_STATUS_CHECK, (key,), ())
                if len(gNOSTaskMgr.taskCache) < 1000:
                    gNOSTaskMgr.addTask(taskOrder)
                    player.nosStatusFetchCallbacksTimeStamp[key] = now
            return
        now = utils.getNow()
        player.nosStatusFetchCallbacks[key] = [(filePath,
          fileType,
          callback[0],
          callback[1])]
        taskOrder = NosServiceOrder(gametypes.NOS_SERVICE_STATUS_CHECK, (key,), ())
        if len(gNOSTaskMgr.taskCache) < 1000:
            gNOSTaskMgr.addTask(taskOrder)
            player.nosStatusFetchCallbacksTimeStamp[key] = now
    elif actionType == gametypes.NOS_SERVICE_STATUS_CROSS_CHECK:
        filePath, key, serverId, fileType = args
        if player.nosStatusFetchCallbacks.has_key(key):
            player.nosStatusFetchCallbacks[key].append((filePath,
             fileType,
             callback[0],
             callback[1]))
            now = utils.getNow()
            nosTimeStamp = player.nosStatusFetchCallbacksTimeStamp.get(key, 0)
            if nosTimeStamp and now - nosTimeStamp > 10:
                taskOrder = NosServiceOrder(gametypes.NOS_SERVICE_STATUS_CROSS_CHECK, (key,), ())
                if len(gNOSTaskMgr.taskCache) < 1000:
                    gNOSTaskMgr.addTask(taskOrder)
                    player.nosStatusFetchCallbacksTimeStamp[key] = now
            return
        now = utils.getNow()
        player.nosStatusFetchCallbacks[key] = [(filePath,
          fileType,
          callback[0],
          callback[1])]
        taskOrder = NosServiceOrder(gametypes.NOS_SERVICE_STATUS_CROSS_CHECK, (key, serverId), ())
        if len(gNOSTaskMgr.taskCache) < 1000:
            gNOSTaskMgr.addTask(taskOrder)
            player.nosStatusFetchCallbacksTimeStamp[key] = now
    elif actionType == gametypes.SOUND_FILE_UPLOAD:
        filePath, extra = args
        taskOrder = NosServiceOrder(gametypes.SOUND_FILE_UPLOAD, (filePath, extra), callback)
        if len(gNOSTaskMgr.taskCache) < 1000:
            gNOSTaskMgr.addTask(taskOrder)
    elif actionType == gametypes.SOUND_FILE_DOWNLOAD:
        if gSoundRecordTaskMgr == None:
            gSoundRecordTaskMgr = NOSDownLoadTaskMgr()
            gSoundRecordTaskMgr.checkInterval = 2
            gSoundRecordTaskMgr.start()
        key, extra = args
        if player.nosDownListCallbacks.has_key(key):
            player.nosDownListCallbacks[key].append(callback)
            return
        player.nosDownListCallbacks[key] = [callback]
        taskOrder = NosServiceOrder(gametypes.SOUND_FILE_DOWNLOAD, (key, extra), (downLoadCallback, (key,)))
        if len(gSoundRecordTaskMgr.taskCache) < 1000:
            gSoundRecordTaskMgr.addTask(taskOrder)
    elif actionType == gametypes.SOUND_FILE_TRANSLATE:
        key, extra = args
        taskOrder = NosServiceOrder(gametypes.SOUND_FILE_TRANSLATE, (key, extra), callback)
        if len(gNOSTaskMgr.taskCache) < 1000:
            gNOSTaskMgr.addTask(taskOrder)


def downLoadCallback(status, key):
    global gNosDLCallBackMgr
    p = BigWorld.player()
    if gNosDLCallBackMgr == None:
        gNosDLCallBackMgr = SeqTaskMgr()
        gNosDLCallBackMgr.start()
    if p.nosDownListCallbacks.has_key(key):
        for callback in p.nosDownListCallbacks[key]:
            taskOrder = AyncCallBackOrder(status, callback)
            if len(gNosDLCallBackMgr.taskCache) < 1000:
                gNosDLCallBackMgr.addTask(taskOrder)

        p.nosDownListCallbacks.pop(key)


def onFetchNOSFileStatus(status, fileType, key):
    global gNosDLCallBackMgr
    player = BigWorld.player()
    if player.nosStatusFetchCallbacks.has_key(key):
        for _filePath, _fileType, callback, callbackArgs in player.nosStatusFetchCallbacks[key]:
            if fileType != fileType:
                gamelog.error('@szh onFetchNOSFileStatus fileType does not match', status, fileType, _fileType, key)
                continue
            if status == gametypes.NOS_FILE_STATUS_SERVER_APPROVED:
                addNOSSeqTask(gametypes.NOS_SERVICE_DOWNLOAD, (_filePath,
                 key,
                 fileType,
                 status), (callback, callbackArgs))
            else:
                if gNosDLCallBackMgr == None:
                    gNosDLCallBackMgr = SeqTaskMgr()
                    gNosDLCallBackMgr.start()
                taskOrder = AyncCallBackOrder(status, (callback, callbackArgs))
                gNosDLCallBackMgr.addTask(taskOrder)

        del player.nosStatusFetchCallbacks[key]
        del player.nosStatusFetchCallbacksTimeStamp[key]
    else:
        return


gYixinTaskMgr = None

class YinxinServiceOrder(ParentOrder):

    def __init__(self, actionType, actionArgs, callback):
        super(YinxinServiceOrder, self).__init__()
        self.actionType = actionType
        self.actionArgs = actionArgs
        self.callback = callback
        self.expire = False

    def doTask(self):
        if self.actionType == gametypes.NOS_SERVICE_DOWNLOAD:
            account, urlPath = self.actionArgs
            clientcom.downloadFileFromYixin(account, urlPath, self.callback)

    def release(self):
        if self.expire:
            return
        if self.callback is not None:
            method, callbackArgs = self.callback
            if method is not None:
                method(gametypes.YIXIN_DOWNLOAD_CANCEL, *callbackArgs)
        self.expire = True


def addYinxinSeqTask(actionType, args, callback):
    global gYixinTaskMgr
    if gYixinTaskMgr == None:
        gYixinTaskMgr = NOSDownLoadTaskMgr()
        gYixinTaskMgr.checkInterval = 0.3
        gYixinTaskMgr.start()
    if actionType == gametypes.NOS_SERVICE_DOWNLOAD:
        while len(gYixinTaskMgr.taskCache) > 0:
            task = gYixinTaskMgr.taskCache.pop()
            task.release()

        taskOrder = YinxinServiceOrder(gametypes.NOS_SERVICE_DOWNLOAD, args, callback)
        gYixinTaskMgr.addTask(taskOrder)


def afterFinishSetStatic(entity, model, matterDyePairs):
    if entity and entity.inWorld:
        for matterDyePair in matterDyePairs:
            if entity.needSetStaticStates():
                if len(matterDyePair) > 2:
                    TA.ta_set_static_states(model, matterDyePair[1], matterDyePair[0], matterDyePair[2], matterDyePair[3], needBuildName=False)
                else:
                    TA.ta_set_static_states(model, matterDyePair[1], matterDyePair[0], needBuildName=False)
            else:
                TA.setContentStateNoUse(matterDyePair[1])
