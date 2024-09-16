#Embedded file name: /WORKSPACE/data/entities/client/sfx/sfx.o
import time
import math
import random
import C_ui
import Math
import BigWorld
import Pixie
import ResMgr
import const
import utils
import gamelog
import gameglobal
import gametypes
import logicInfo
import skillDataInfo
import groupEffect
import flyEffect
import clientcom
import formula
import clientUtils
from sMath import distance3D, distance2D
from callbackHelper import Functor
from guis import ui
from guis import cursor
from helpers import cellCmd
from data import monster_model_client_data as NMMD
from cdata import game_msg_def_data as GMDD
from data import skill_fx_data as SFD
from data import skill_fx_plus_data as SFPD
from data import sys_config_data as SYSCD
from data import model_effect_data as MED
from data import zaiju_data as ZJD
from data import fx_effect_data as FED
MAXDELAYTIME = 30
KEEPEFFECTTIME = 999999999
MAXHITDELAYTIME = 3.0
EFFECT_LOADCOUNT = 300
KEEPEFFECT_MAXDIS = 82
effectFileExistMap = {}
effectKeepTimeMap = {}
G_MONSTER_LOCKED = {}

def updateEffectKeepTime(effId, keepTime):
    if effectKeepTimeMap.has_key(effId):
        if keepTime > effectKeepTimeMap.get(effId, 0):
            effectKeepTimeMap[effId] = keepTime
    else:
        effectKeepTimeMap[effId] = keepTime


CHAR_SFX_ID_START = 100000
CHAR_SFX_ID_END = 299999
EFFECT_PATH = 'effect/'

def _getPath(effectId, effectPath):
    if type(effectId) == str:
        if effectId.endswith('.xml') or effectId.endswith('.XML'):
            return effectId
        else:
            return effectPath + 'char/combat/%s.xml' % effectId
    if 1 <= effectId <= 499:
        return effectPath + 'char/hit/%i.xml' % effectId
    if 500 <= effectId <= 999:
        return effectPath + 'char/buff/%i.xml' % effectId
    if 1000 <= effectId <= 9999:
        return effectPath + 'com/%i.xml' % effectId
    if 10000 <= effectId <= 99999:
        return effectPath + 'char/com/%i.xml' % effectId
    if CHAR_SFX_ID_START <= effectId <= CHAR_SFX_ID_END:
        return effectPath + 'char/combat/%i.xml' % effectId
    if 300000 <= effectId <= 999999:
        return effectPath + 'char/monster/%i.xml' % effectId
    if 1000000 <= effectId <= 1999999:
        return effectPath + 'home/%i.xml' % effectId
    if 2000000 <= effectId <= 5999999:
        return effectPath + 'char/monster/%i.xml' % effectId
    gamelog.debug('_getPath:Can not parse effect path...........', effectId)


def _getModelId(model):
    modelId = 0
    try:
        modelId = int(model.sources[-1].split('/')[1])
    except:
        modelId = 0

    return modelId


def _getRealFxInfo(effectId, modelId = 0):
    if type(effectId) == int and CHAR_SFX_ID_START <= effectId <= CHAR_SFX_ID_END and gameglobal.isAvatarModel(modelId):
        if MED.data.has_key((modelId, effectId)):
            fxPath = EFFECT_PATH + 'char/combat/%i_%i.xml' % (modelId, effectId)
            return ('%i_%i' % (modelId, effectId), fxPath)
    return (effectId, _getPath(effectId, EFFECT_PATH))


def getPath(effectId, modelId = None):
    realFxId, path = _getRealFxInfo(effectId, modelId)
    return path


EFFECT_UNLIMIT = 0
EFFECT_LIMIT = 1
EFFECT_LIMIT_MISC = 2

def needCounterEffect(fxId, effectType, ownerId, hostId):
    if gameglobal.rds.GameState <= gametypes.GS_LOGIN:
        return False
    if gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_PLAYING_TRACK_CAMERA:
        return False
    if effectType == EFFECT_UNLIMIT:
        return False
    important = isAlwaysAttach(fxId)
    if important:
        return False
    p = BigWorld.player()
    if not p:
        return False
    if ownerId == p.id or hostId == p.id:
        return False
    return True


class SkillEffectCounterMgr(object):
    MAX_SUM_EFFECT_COUNT = 800
    MAX_SUM_EFFECT_COUNT_FPS20 = 400
    MAX_SUM_EFFECT_COUNT_FPS15 = 300
    MAX_SUM_EFFECT_COUNT_FPS10 = 200
    MAX_SUM_MISC_EFFECT_COUNT = 100
    FPS30 = 30
    FPS20 = 20
    FPS15 = 15

    def __init__(self):
        self.sumEffCount = 0
        self.sumMiscEffCount = 0
        self.maxSumEffectCount = self.MAX_SUM_EFFECT_COUNT
        self.maxSumMiscEffectCount = self.MAX_SUM_MISC_EFFECT_COUNT

    def inc(self, fxId, effectType, ownerId, hostId):
        if not needCounterEffect(fxId, effectType, ownerId, hostId):
            return
        if effectType == EFFECT_LIMIT_MISC:
            self.sumMiscEffCount += 1
        else:
            self.sumEffCount += 1

    def dec(self, fxId, effectType, ownerId, hostId):
        if not needCounterEffect(fxId, effectType, ownerId, hostId):
            return
        if effectType == EFFECT_LIMIT_MISC:
            self.sumMiscEffCount -= 1
        else:
            self.sumEffCount -= 1

    def canAttach(self, fxId, effectType, ownerId, hostId):
        if not needCounterEffect(fxId, effectType, ownerId, hostId):
            return True
        attachDist = 30.0
        fps = BigWorld.getFps()
        p = BigWorld.player()
        if p.__class__.__name__ == 'PlayerAccount':
            return True
        if not p.isRealInFuben():
            if fps > self.FPS30:
                self.maxSumEffectCount = min(self.MAX_SUM_EFFECT_COUNT, self.maxSumEffectCount)
                attachDist = 40.0
            elif fps >= self.FPS20:
                self.maxSumEffectCount = min(self.MAX_SUM_EFFECT_COUNT_FPS20, self.maxSumEffectCount)
                attachDist = 35.0
            elif fps >= self.FPS15:
                self.maxSumEffectCount = min(self.MAX_SUM_EFFECT_COUNT_FPS15, self.maxSumEffectCount)
                attachDist = 25.0
            else:
                self.maxSumEffectCount = min(self.MAX_SUM_EFFECT_COUNT_FPS10, self.maxSumEffectCount)
                attachDist = 20.0
        if p.isRealInFuben():
            entity = BigWorld.entities.get(ownerId)
            if getattr(entity, 'IsMonster', False) or getattr(entity, 'isNPC', False):
                return True
        if effectType == EFFECT_LIMIT and self.sumEffCount > self.maxSumEffectCount:
            return False
        if effectType == EFFECT_LIMIT_MISC and self.sumMiscEffCount > self.maxSumMiscEffectCount:
            return False
        p = BigWorld.player()
        if not p.isRealInFuben() and not formula.inDotaBattleField(getattr(p, 'mapID', 0)) and effectType == EFFECT_LIMIT:
            pos = p.position
            entity = BigWorld.entities.get(ownerId)
            if entity:
                distToPlayer = (entity.position - pos).length
                if distToPlayer > attachDist:
                    return False
            entity = BigWorld.entities.get(hostId)
            if entity:
                distToPlayer = (entity.position - pos).length
                if distToPlayer > attachDist:
                    return False
        return True


ATTACH_ROOT = 1
ATTACH_LEFTWEAPON = 2
ATTACH_RIGHTWEAPON = 3
ATTACH_ORIGIN = 4
ATTACH_HIT = 5
ATTACH_NODE = 6
ATTACH_TARGET = 7
ATTACH_GROUP1 = 8
ATTACH_GROUP2 = 9
ATTACH_GROUP3 = 10
ATTACH_DROP_POINT = 11
ATTACH_RIGHTWEAPON_R1 = 12
ATTACH_RIGHTWEAPON_L1 = 13
ATTACH_HIT_ORIGIN = 14
ATTACH_YUANLING = 15
DIR_NODE_CONTROL = (0, 0, 0)
DIR_UP_FACEMODEL = (0, 1, 0)
DIR_UP_FACENODE = (1, 1, 1)
DIR_UP_FACETARGET = (0, 2, 0)
DIR_UP_FACEPLAYER = (0, 3, 0)
DIR_NODE_POSITION = (2, 0, 0)
Circle_Group = 1
Fan_Group = 2

class EffectInfoMap(object):

    def __init__(self):
        super(EffectInfoMap, self).__init__()
        self.cache = {}
        self.hasEffectInfo = False
        self.initEffectTable()

    def initEffectTable(self):
        gamelog.debug('initEffectTable')
        self.reloadRes()
        self.loadEffectTable('effect/effectInfo.xml')

    def loadEffectTable(self, effect_info_path):
        effectInfo = ResMgr.openSection(effect_info_path)
        if effectInfo:
            at = time.clock()
            for sect in effectInfo.items():
                if sect[0].isdigit():
                    self.addInfo(int(sect[0]), sect[1])
                else:
                    self.addInfo(sect[0], sect[1])

            dt = time.clock() - at
            self.hasEffectInfo = True
            gamelog.debug('initEffectInfoMap:', effect_info_path, dt)
        else:
            gamelog.debug('initEffectInfoMap not found:', effect_info_path)

    def reloadRes(self):
        for i in self.cache:
            ResMgr.purge(getPath(i))

        self.cache = {}

    def addToMap(self, effectId, attachPos, attachDirStr, scaleBase, alwaysShow):
        dropPoint = SFD.data.get(effectId, {}).get('dropPoint', 0)
        attachInfo = []
        for i in attachPos:
            if i == 'root':
                attachInfo.append((ATTACH_ROOT, i))
            elif i == 'originPos':
                if dropPoint:
                    attachInfo.append((ATTACH_DROP_POINT, i))
                else:
                    attachInfo.append((ATTACH_ORIGIN, i))
            elif i.startswith('HP_hit_originPos'):
                attachInfo.append((ATTACH_HIT_ORIGIN, i))
            elif i.startswith('HP_weapon_left_effect'):
                attachInfo.append((ATTACH_LEFTWEAPON, i))
            elif i.startswith('HP_weapon_right_effect'):
                attachInfo.append((ATTACH_RIGHTWEAPON, i))
            elif i.startswith('HP_weapon_right_r1_effect'):
                attachInfo.append((ATTACH_RIGHTWEAPON_R1, i))
            elif i.startswith('HP_weapon_right_l1_effect'):
                attachInfo.append((ATTACH_RIGHTWEAPON_L1, i))
            elif i.startswith('HP_hit'):
                attachInfo.append((ATTACH_HIT, i))
            elif i.startswith('Target_'):
                attachInfo.append((ATTACH_TARGET, i[7:]))
            elif i.startswith('group1'):
                attachInfo.append((ATTACH_GROUP1, i))
            elif i.startswith('group2'):
                attachInfo.append((ATTACH_GROUP2, i))
            elif i.startswith('group3'):
                attachInfo.append((ATTACH_GROUP3, i))
            elif i.startswith('HP_yuanling_effect'):
                attachInfo.append((ATTACH_YUANLING, i))
            else:
                attachInfo.append((ATTACH_NODE, i))

        attachDir = DIR_UP_FACEMODEL
        if attachDirStr == 'node_control':
            attachDir = DIR_NODE_CONTROL
        elif attachDirStr == 'up_faceTarget':
            attachDir = DIR_UP_FACETARGET
        elif attachDirStr == 'up_faceNode':
            attachDir = DIR_UP_FACENODE
        elif attachDirStr == 'up_facePlayer':
            attachDir = DIR_UP_FACEPLAYER
        elif attachDirStr == 'node_position':
            attachDir = DIR_NODE_POSITION
        self.cache[effectId] = (attachInfo,
         attachDir,
         scaleBase,
         alwaysShow)

    def addInfo(self, effectId, dataSection):
        if not dataSection:
            return
        attachPos = []
        attachDir = 'up_faceModel'
        scaleBase = None
        alwaysShow = False
        for i in dataSection.items():
            if i[0] == 'attach_pos':
                attachPos.append(i[1].asString)
            if i[0] == 'attach_dir':
                attachDir = i[1].asString
            if i[0] == 'scaleBase':
                scaleBase = i[1].asVector3
                if scaleBase.length == 0:
                    scaleBase = None
            if i[0] == 'alwaysShow':
                alwaysShow = i[1].asBool

        alwaysShow = alwaysShow or SFD.data.get(effectId, {}).get('alwaysShow', False)
        if len(attachPos) == 0:
            attachPos.append('root')
        self.addToMap(effectId, attachPos, attachDir, scaleBase, alwaysShow)

    def getInfo(self, effectId, model = None):
        modelId = _getModelId(model)
        realFxId, fxPath = _getRealFxInfo(effectId, modelId)
        if self.cache.has_key(realFxId):
            return self.cache[realFxId]
        ef = ResMgr.openSection(fxPath)
        if ef == None:
            self.cache[realFxId] = None
            return self.cache[realFxId]
        attachPos = []
        attachDir = 'up_faceModel'
        for i in ef.items():
            if i[0] == 'option':
                for j in i[1].items():
                    if j[0] == 'attach_pos':
                        attachPos.append(j[1].asString)
                    if j[0] == 'attach_dir':
                        attachDir = j[1].asString

        if len(attachPos) == 0:
            attachPos.append('root')
        gamelog.debug('effect:monster3', attachPos, dir(ef))
        scaleBase = ef.readVector3('extendInfo/scaleBase')
        if scaleBase.length == 0:
            scaleBase = None
        alwaysShow = ef.readBool('extendInfo/alwaysShow', False) or SFD.data.get(effectId, {}).get('alwaysShow', False)
        self.addToMap(realFxId, attachPos, attachDir, scaleBase, alwaysShow)
        return self.cache[realFxId]


gEffectInfoMap = EffectInfoMap()

def playShakeCamera(shakeCameras, fxOwner):
    gamelog.debug('lihang:__playShakeCamera', shakeCameras, fxOwner)
    cbs = []
    if shakeCameras:
        for shakeCameraId, delayTime in shakeCameras:
            cb = BigWorld.callback(delayTime, Functor(__swayCallBack, shakeCameraId, fxOwner))
            cbs.append(cb)

    return cbs


def __swayCallBack(shakeCameraId, fxOwner):
    pass


EFFECT_GET_CNT = 0
EFFECT_HIT_CNT = 0

class CacheNode():

    def __init__(self, key, value):
        self.key = key
        self.prev = None
        self.next = None
        self.valueList = [value]

    def addValue(self, value):
        self.valueList.append(value)

    def __repr__(self):
        return str(self.valueList)


class EffectCache(object):
    MAX_CACHE_COUNT = 400

    def __init__(self):
        self.cache = {}
        self.cacheCount = 0

    def getEffect(self, id):
        effects = self.cache.get(id, None)
        if effects is None:
            return
        if len(effects) > 0:
            fx = effects.pop()
            if fx.attached or fx.inWorld:
                return
            else:
                return fx

    def addEffect(self, id, obj):
        if self.cacheCount > self.MAX_CACHE_COUNT:
            obj = None
            return
        assert obj != None
        self.cacheCount += 1
        self.cache.setdefault(id, []).append(obj)

    def clearEffectCache(self):
        if self.cacheCount > self.MAX_CACHE_COUNT:
            self.realClearEffectCache()

    def realClearEffectCache(self):
        self.cacheCount = 0
        self.cache.clear()
        self.cache = {}

    def reloadAll(self):
        self.cacheCount = 0
        self.cache = {}
        ResMgr.purgeAll()


class LRUEffectCache(object):

    def clearEffectCache(self):
        pass

    def realClearEffectCache(self):
        global EFFECT_GET_CNT
        global EFFECT_HIT_CNT
        EFFECT_GET_CNT = 0
        EFFECT_HIT_CNT = 0
        self.cacheCount = 0
        self.cacheDic = {}
        self.resetCacheList()

    def resetCacheList(self):
        cacheNode = self.headNode.next
        while cacheNode != self.flagNode:
            nextNode = cacheNode.next
            self.removeNode(cacheNode)
            cacheNode = nextNode

    def moveNodeToHead(self, effectNode):
        if effectNode.prev:
            effectNode.prev.next = effectNode.next
            effectNode.next.prev = effectNode.prev
        self.headNode.next.prev = effectNode
        effectNode.next = self.headNode.next
        self.headNode.next = effectNode
        effectNode.prev = self.headNode

    def removeNode(self, node):
        if node == self.flagNode:
            return
        node.prev.next = node.next
        node.next.prev = node.prev
        node.prev = None
        node.next = None
        node.valueList = []

    def reloadAll(self):
        self.clearEffectCache()
        ResMgr.purgeAll()

    def __init__(self):
        self.flagNode = CacheNode(0, None)
        self.headNode = self.flagNode
        self.tailNode = self.flagNode
        self.headNode.next = self.tailNode
        self.tailNode.prev = self.headNode
        self.cacheDic = {}
        self.cacheCount = 0
        self.MAX_CACHE_COUNT = 400

    def addEffect(self, id, obj):
        self.cacheCount += 1
        if self.cacheDic.has_key(id):
            effectNode = self.cacheDic[id]
            effectNode.addValue(obj)
        else:
            effectNode = CacheNode(id, obj)
        self.moveNodeToHead(effectNode)
        self.cacheDic[id] = effectNode
        if self.cacheCount > self.MAX_CACHE_COUNT:
            self.cacheCount -= 1
            cacheNode = self.tailNode.prev
            cacheNode.valueList.pop(-1)
            if not cacheNode.valueList:
                self.removeNode(cacheNode)
                self.cacheDic.pop(cacheNode.key)

    def getEffect(self, id):
        global EFFECT_GET_CNT
        global EFFECT_HIT_CNT
        EFFECT_GET_CNT += 1
        cacheNode = self.cacheDic.get(id, None)
        cacheEff = None
        if not cacheNode:
            return
        while cacheNode.valueList:
            fx = cacheNode.valueList.pop(-1)
            self.cacheCount -= 1
            if fx.attached or fx.inWorld:
                continue
            EFFECT_HIT_CNT += 1
            cacheEff = fx
            break

        if not cacheNode.valueList:
            self.removeNode(cacheNode)
            self.cacheDic.pop(id)
        return cacheEff

    def getAll(self):
        s = 0
        for cacheNode in self.cacheDic.values():
            s += len(cacheNode.valueList)

        return s


class SkillEffectMgr(object):

    def __init__(self):
        super(SkillEffectMgr, self).__init__()
        self.LRUEffectCache = LRUEffectCache()
        self.oldEffectCache = EffectCache()
        self.fetchFailed = {}
        self.effCounter = SkillEffectCounterMgr()
        self.delayGiveBackTime = SYSCD.data.get('danDaoEffectDelayGiveBackTime', 1.0)
        self.dummyEffects = {}

    @property
    def effectCache(self):
        if clientcom.enableLRUCache():
            return self.LRUEffectCache
        else:
            return self.oldEffectCache

    def reloadRes(self):
        self.effectCache.reloadAll()

    def preloadFx(self, fxId, lv, modelId = None):
        realFxId, fxPath = _getRealFxInfo(fxId, modelId)
        if not self.effectCache.getEffect(realFxId):
            try:
                fx = clientUtils.pixieFetch(fxPath, lv)
            except:
                self.fetchFailed[realFxId] = True
                return

            self.effectCache.addEffect(realFxId, fx)

    def canAttach(self, fxId, effectType, ownerId, hostId):
        return self.effCounter.canAttach(fxId, effectType, ownerId, hostId)

    def disableParticleLightVisible(self, fx, ownerId):
        if not fx or not ownerId:
            return
        host = BigWorld.entities.get(ownerId, None)
        if not host:
            return
        if host.__class__.__name__ == 'Avatar':
            fx.particleLightVisible = False

    def checkTaskLoad(self, fx, important, maxDelayTime):
        if not fx and not important and hasattr(BigWorld, 'getTaskLoadByPrio'):
            taskCnt = BigWorld.getTaskLoadByPrio(gameglobal.PRIO_LOW)
            if maxDelayTime > 0 and taskCnt / max(gameglobal.TASKPERFRAME * BigWorld.getFps() * 1.5, 10) > maxDelayTime:
                return False
        return True

    def checkNewTaskLoad(self, fx, important, maxDelayTime, ownerId, hostId):
        playerId = BigWorld.player().id
        if ownerId == playerId or hostId == playerId:
            return True
        if not fx and not important:
            taskCnt = BigWorld.getTaskLoadByPrio(gameglobal.PRIO_LOW)
            if maxDelayTime > 0 and taskCnt > EFFECT_LOADCOUNT:
                return False
        return True

    def ownerInHiding(self, ownerId, hostId):
        owner = BigWorld.entity(ownerId)
        if hasattr(owner, 'inHiding') and owner.inHiding():
            if owner.getOpacityValue()[0] in gameglobal.OPACITY_HIDE_TOPLOGO:
                return True
        return False

    def attachEffect(self, fxId, lv, priority, node, attachDir, effectType, maxDelayTime, txtInfo = None, nodeScale = 1.0, model = None):
        global gNoAvatarEffect
        if gameglobal.DISABLE_FX_LOAD:
            gamelog.critical('bgf@sfx_attachEffect', fxId, lv, priority)
            return
        if node == None:
            return
        important = isAlwaysAttach(fxId)
        if priority > clientcom.getEffectPriority():
            if not important or gNoAvatarEffect:
                return
        modelId = _getModelId(model)
        realFxId, fxPath = _getRealFxInfo(fxId, modelId)
        fx = self.effectCache.getEffect(realFxId)
        hostId = getattr(model, 'hostId', -1)
        ownerId = getattr(model, 'ownerId', -1)
        if gameglobal.rds.configData.get('enableCheckTaskLoad', False):
            if not self.checkNewTaskLoad(fx, important, maxDelayTime, ownerId, hostId):
                return
        elif not self.checkTaskLoad(fx, important, maxDelayTime):
            return
        if self.ownerInHiding(ownerId, hostId):
            return
        if fx != None and getattr(fx, 'isOK', True):
            if fx.loadLevel() >= lv:
                fx.drawLevel(lv)
                gamelog.debug('#zf:EffectManager:find effect from cache ', fxId, realFxId, fx, effectType)
                fx.setAttachMode(attachDir[0], attachDir[1], attachDir[2])
                fx.clear()
                fx.hostId = hostId
                fx.ownerId = ownerId
                fx.overCallback(Functor(self.giveBack, realFxId, fx, node, effectType), maxDelayTime)
                self.disableParticleLightVisible(fx, ownerId)
                fx.force()
                if txtInfo:
                    fx.setText(*txtInfo)
                node.attach(fx)
                fixModelScale = SFD.data.get(fxId, {}).get('fixModelScale', 0)
                if fixModelScale and model:
                    nodeScale *= 1.0 / model.scale[0]
                if hasattr(fx, 'scale'):
                    fx.scale(nodeScale)
                self.effCounter.inc(realFxId, effectType, ownerId, hostId)
                self.playEffectCameraEffect(hostId, ownerId, fxId, model)
                return fx
            fx = None
        try:
            if gameglobal.rds.configData.get('enableEffectLoadOptimize', False):
                fx = clientUtils.pixieFetch(fxPath, lv, maxDelayTime)
            else:
                fx = clientUtils.pixieFetch(fxPath, lv)
            fx.hostId = hostId
            fx.ownerId = ownerId
        except:
            self.fetchFailed[realFxId] = True
            return

        gamelog.debug('#zf:EffectManager:find effect not from cache ', fxId, fx, lv, effectType)
        fx.overCallback(Functor(self.giveBack, realFxId, fx, node, effectType), maxDelayTime)
        fx.setAttachMode(attachDir[0], attachDir[1], attachDir[2])
        fx.clear()
        self.disableParticleLightVisible(fx, ownerId)
        fx.force()
        if txtInfo:
            fx.setText(*txtInfo)
        node.attach(fx)
        fixModelScale = SFD.data.get(fxId, {}).get('fixModelScale', 0)
        if fixModelScale and model:
            nodeScale *= 1.0 / model.scale[0]
        if hasattr(fx, 'scale'):
            fx.scale(nodeScale)
        self.effCounter.inc(realFxId, effectType, ownerId, hostId)
        self.playEffectCameraEffect(hostId, ownerId, fxId, model)
        return fx

    def playEffectCameraEffect(self, hostId, ownerId, effectId, model):
        p = BigWorld.player()
        if model:
            model.hostId = -1
        effectId = str(effectId)
        if effectId.find('_') != -1:
            effectId = effectId.split('_')[1]
        try:
            effectId = int(effectId)
        except:
            return

        effectData = FED.data.get(effectId, {})
        if not effectData:
            return
        broadcast = effectData.get('broadcast', False)
        if hostId == p.id or ownerId == p.id or broadcast:
            if hostId == p.id:
                entity = BigWorld.entities.get(hostId)
            else:
                entity = BigWorld.entities.get(ownerId)
            fxEffectDelay = effectData.get('fxEffectDelay', 0.0)
            if fxEffectDelay > 0.0:
                BigWorld.callback(fxEffectDelay, Functor(self._playAllHitEffect, entity, effectData))
            else:
                self._playAllHitEffect(entity, effectData)

    def _playAllHitEffect(self, owner, effectData):
        if owner:
            owner.playCameraPush(effectData)
            owner.playMotionBlur(effectData)
            owner.playSpecialShakeCamera(effectData)

    def giveBack(self, fxId, effect, node, effectType):
        if hasattr(effect, 'delayGiveBack') and effect.delayGiveBack:
            BigWorld.callback(self.delayGiveBackTime, Functor(self.realGiveBack, fxId, effect, node, effectType))
        else:
            self.realGiveBack(fxId, effect, node, effectType)

    def realGiveBack(self, fxId, effect, node, effectType):
        hostId = getattr(effect, 'hostId', -1)
        ownerId = getattr(effect, 'ownerId', -1)
        self.removeDummyEffect(effect)
        self.effCounter.dec(fxId, effectType, ownerId, hostId)
        self.detach(fxId, effect, node)

    def detach(self, fxId, effect, node):
        if not node:
            effect = None
            return
        if effect in node.attachments:
            node.detach(effect)
            effect.clear()
            effect.scale(1)
            effect.bias = (0, 0, 0)
            self.effectCache.addEffect(fxId, effect)
        else:
            effect = None

    def addDummyEffect(self, fx, fxInfo):
        self.dummyEffects[id(fx)] = fxInfo

    def removeDummyEffect(self, fx):
        fxInfo = self.dummyEffects.get(id(fx), None)
        if fxInfo:
            del self.dummyEffects[id(fx)]

    def giveBackDummyEffect(self, fxAddr):
        fxInfo = self.dummyEffects.get(fxAddr, None)
        if fxInfo:
            effectId, mist, dummy, effectType = fxInfo
            del self.dummyEffects[fxAddr]
            detachOriginEffect(effectId, mist, dummy, effectType)

    def checkDummyEffects(self):
        needGiveBackEffects = []
        needRemoveEffects = []
        p = BigWorld.player()
        if not utils.instanceof(p, 'PlayerAvatar'):
            return
        for fxAddr, fxInfo in self.dummyEffects.iteritems():
            dummy = fxInfo[2]
            if dummy and dummy.inWorld:
                if distance2D(dummy.position, p.position) > KEEPEFFECT_MAXDIS:
                    needGiveBackEffects.append(fxAddr)
            elif not dummy:
                needRemoveEffects.append(fxAddr)
            else:
                needGiveBackEffects.append(fxAddr)

        for fxAddr in needGiveBackEffects:
            self.giveBackDummyEffect(fxAddr)

        for fxAddr in needRemoveEffects:
            self.removeDummyEffect(fxAddr)


gEffectMgr = SkillEffectMgr()
gNoEffect = False
gNoAvatarEffect = False

def attachEffect(funcType, args):
    global gEffectMgr
    if gNoEffect:
        return None
    effectType = EFFECT_LIMIT
    hostId = getattr(args[2], 'hostId', -1)
    ownerId = getattr(args[2], 'entityId', -1)
    if gNoAvatarEffect:
        en = BigWorld.entities.get(ownerId)
        if getattr(en, 'IsAvatarRobot', False) or getattr(en, 'IsAvatar', False) or getattr(en, 'IsPuppet', False):
            return None
    if funcType == gameglobal.ATTACH_EFFECT_NORMAL:
        effectType = args[4]
    elif funcType == gameglobal.ATTACH_EFFECT_ONHIT:
        effectType = args[6]
        if args[5]:
            hostId = args[5].id
    elif funcType == gameglobal.ATTACH_EFFECT_INPOS:
        effectType = args[4]
    elif funcType == gameglobal.ATTACH_EFFECT_ONNODE:
        effectType = args[5]
    effId = args[4] if funcType in (gameglobal.ATTACH_EFFECT_ONNODE, gameglobal.ATTACH_EFFECT_ONHIT) else args[3]
    if funcType == gameglobal.ATTACH_EFFECT_CONNECTOR or funcType == gameglobal.ATTACH_EFFECT_CONNECTOR2:
        effId = args[2]
    if not gEffectMgr.canAttach(effId, effectType, ownerId, hostId):
        return None
    if funcType != gameglobal.ATTACH_EFFECT_CONNECTOR and funcType != gameglobal.ATTACH_EFFECT_CONNECTOR2 and args[2]:
        args[2].hostId = hostId
        args[2].ownerId = ownerId
    if args[0] == gameglobal.EFFECT_CLOSE:
        alwaysAttach = isAlwaysAttach(effId)
        if not alwaysAttach:
            return None
        args = list(args)
        args[0] = gameglobal.EFFECT_LOW
    attachEffectFunc = {gameglobal.ATTACH_EFFECT_NORMAL: attachEffectNormal,
     gameglobal.ATTACH_EFFECT_ONHIT: attachEffectOnHitNode,
     gameglobal.ATTACH_EFFECT_INPOS: attachEffectInPos,
     gameglobal.ATTACH_EFFECT_CONNECTOR: NodeEffectConnector,
     gameglobal.ATTACH_EFFECT_ONNODE: attachEffectOnNode,
     gameglobal.ATTACH_EFFECT_CONNECTOR2: PositionNodeEffectConnect,
     gameglobal.ATTACH_CACHED_EFFECT_CONNECTOR: CachedNodeEffectConnector}
    func = attachEffectFunc.get(funcType, '')
    if func:
        return func(*args)


def isAlwaysAttach(effectId):
    global gEffectInfoMap
    info = gEffectInfoMap.getInfo(effectId)
    if info:
        return info[3]
    return False


def getModelKeepFx(effectId):
    keepFxTime = SFD.data.get(effectId, {}).get('modelKeepFx', None)
    if not keepFxTime and type(effectId) == str:
        keepFxTime = SFPD.data.get(effectId, {}).get('modelKeepFx', None)
    return keepFxTime


def attachEffectNormal(effectLv, priority, model, effectId, effectType = EFFECT_LIMIT, maxDelayTime = -1, targetPos = 0, ignorePrefix = False, txtInfo = None, targetYaw = None):
    keepFxTime = SFD.data.get(effectId, {}).get('modelKeepFx', None)
    if maxDelayTime > 0:
        pass
    elif keepFxTime:
        if keepFxTime < 0.0:
            maxDelayTime = KEEPEFFECTTIME
        else:
            maxDelayTime = keepFxTime
    elif maxDelayTime < 0.0:
        maxDelayTime = MAXDELAYTIME
    if isinstance(effectId, list) or isinstance(effectId, tuple):
        effList = []
        for effId in effectId:
            eArr = attachEffectEx(model, effId, effectLv, priority, effectType, maxDelayTime, targetPos, ignorePrefix, txtInfo, targetYaw)
            if eArr:
                effList.extend(eArr)

        return effList
    else:
        return attachEffectEx(model, effectId, effectLv, priority, effectType, maxDelayTime, targetPos, ignorePrefix, txtInfo, targetYaw)


HIT_EFFECT_FACEPLAYERSIZE = 3

def attachEffectOnHitNode(effectLv, priority, model, hitNode, effectId, host, effectType = EFFECT_LIMIT, maxDelayTime = -1, targetPos = 0, ignorePrefix = False, txtInfo = None):
    if maxDelayTime < 0.0:
        maxDelayTime = MAXHITDELAYTIME
    info, nodeScale = getEffectInfo(model, effectId, maxDelayTime, targetPos, ignorePrefix, txtInfo)
    if info and model and model.inWorld:
        attachPos = info[0][0][0]
        if attachPos == ATTACH_HIT:
            attachedEffect = []
            hitNode = model.node(hitNode)
            if not hitNode:
                hitNode = model.node('HP_hit_default')
            if hitNode != None:
                if info[1] == DIR_UP_FACEPLAYER:
                    if len(hitNode.attachments) > HIT_EFFECT_FACEPLAYERSIZE:
                        return
                    dummy = getDummyModel()
                    position = clientcom.getPositionByNode(hitNode)
                    dummy.position = position
                    dummy.yaw = (BigWorld.player().position - position).yaw
                    gamelog.debug('DIR_UP_FACEPLAYER', dummy.position, dummy.yaw)
                    hitNode = dummy.root
                    BigWorld.callback(maxDelayTime + 1.0, Functor(giveBackDummyModel, dummy))
                elif info[1] == DIR_UP_FACETARGET and host:
                    if len(hitNode.attachments) > HIT_EFFECT_FACEPLAYERSIZE:
                        return
                    dummy = getDummyModel()
                    position = clientcom.getPositionByNode(hitNode)
                    dummy.position = position
                    dummy.yaw = (host.position - position).yaw
                    gamelog.debug('DIR_UP_FACEPLAYER', dummy.position, dummy.yaw)
                    hitNode = dummy.root
                    BigWorld.callback(maxDelayTime + 1.0, Functor(giveBackDummyModel, dummy))
                else:
                    scale = 1.0
                    if model:
                        scale = model.scale[0]
                    nodeScale *= 1.0 / scale
                mist = gEffectMgr.attachEffect(effectId, effectLv, priority, hitNode, info[1], effectType, maxDelayTime, txtInfo, nodeScale, model)
                if mist:
                    attachedEffect.append(mist)
            return attachedEffect
        if attachPos == ATTACH_HIT_ORIGIN:
            attachedEffect = []
            hitNode = model.node(hitNode)
            if not hitNode:
                hitNode = model.node('HP_hit_default')
            if hitNode != None:
                targetPos = clientcom.getPositionByNode(hitNode)
                mist = attachEffectInPos(effectLv, priority, model, effectId, effectType, targetPos, maxDelayTime)
                if mist:
                    attachedEffect.append(mist)
        else:
            return attachEffectEx(model, effectId, effectLv, priority, effectType, maxDelayTime, targetPos, ignorePrefix, txtInfo)


def attachEffectOnNode(effectLv, priority, model, nodeName, effectId, effectType = EFFECT_LIMIT, maxDelayTime = -1, targetPos = 0, ignorePrefix = False, txtInfo = None):
    if maxDelayTime < 0.0:
        maxDelayTime = MAXHITDELAYTIME
    info, nodeScale = getEffectInfo(model, effectId, maxDelayTime, targetPos, ignorePrefix, txtInfo)
    if info and model and model.inWorld:
        attachedEffect = []
        node = model.node(nodeName)
        if not node:
            gamelog.error('attachEffectOnHPNode:Error, can not get hpnode %s' % (nodeName,))
            return
        if node != None:
            mist = gEffectMgr.attachEffect(effectId, effectLv, priority, node, info[1], effectType, maxDelayTime, txtInfo, nodeScale, model)
            if mist:
                attachedEffect.append(mist)
        return attachedEffect


def attachEffectInPos(effectLv, priority, model, effectId, effectType = EFFECT_LIMIT, targetPos = None, roll = 0, yaw = 0, pitch = 0, maxDelayTime = -1):
    keepFxTime = getModelKeepFx(effectId)
    if keepFxTime:
        if keepFxTime < 0.0:
            if maxDelayTime < 0.0:
                maxDelayTime = MAXDELAYTIME
        else:
            maxDelayTime = keepFxTime
    elif maxDelayTime < 0.0:
        maxDelayTime = MAXDELAYTIME
    dummy = getDummyModel()
    if targetPos is not None:
        dummy.position = targetPos
    else:
        dummy.position = model.position
    info = gEffectInfoMap.getInfo(effectId, model)
    if info == None:
        return
    if targetPos is not None:
        dummy.yaw = yaw
        dummy.roll = roll
        dummy.pitch = pitch
    else:
        dummy.yaw = model.yaw
    fx = gEffectMgr.attachEffect(effectId, effectLv, priority, dummy.root, info[1], effectType, maxDelayTime, None, 1.0, model)
    if fx:
        fx.overCallback(Functor(detachOriginEffect, effectId, fx, dummy, effectType), maxDelayTime)
    else:
        giveBackDummyModel(dummy)
    return [fx]


def getEffectInfo(model, effectId, maxDelayTime = -1, targetPos = 0, ignorePrefix = False, txtInfo = None):
    if model == None:
        gamelog.debug('groupeffect:Error attachEffect failed,model is None!')
        return (None, None)
    if not model.inWorld:
        gamelog.debug('groupeffect:Error attachEffect failed,model is not attached!', model.sources, effectId)
        return (None, None)
    if hasattr(model, 'noAttachFx_') and model.noAttachFx_:
        return (None, None)
    nodeScale = 1.0
    if hasattr(model, 'entityId'):
        eid = model.entityId
        entity = BigWorld.entity(eid)
        if entity and hasattr(entity, 'charType'):
            if entity.charType:
                nodeScale = NMMD.data.get(entity.charType, {}).get('attachFxScale', 1.0)
    info = gEffectInfoMap.getInfo(effectId, model)
    return (info, nodeScale)


def attachEffectEx(model, effectId, effectLv, priority, effectType, maxDelayTime = -1, targetPos = 0, ignorePrefix = False, txtInfo = None, targetYaw = None):
    info, nodeScale = getEffectInfo(model, effectId, maxDelayTime, targetPos, ignorePrefix, txtInfo)
    if not info:
        return
    attachedEffect = []
    for attachinfo in info[0]:
        attachType = attachinfo[0]
        if ignorePrefix and attachType in (ATTACH_LEFTWEAPON,
         ATTACH_RIGHTWEAPON,
         ATTACH_RIGHTWEAPON_R1,
         ATTACH_RIGHTWEAPON_L1):
            attachType = ATTACH_NODE
        attachPos = attachinfo[1]
        mist = None
        if attachType == ATTACH_ROOT:
            mist = gEffectMgr.attachEffect(effectId, effectLv, priority, model.root, info[1], effectType, maxDelayTime, txtInfo, 1.0, model)
            if mist:
                attachedEffect.append(mist)
        elif attachType == ATTACH_LEFTWEAPON:
            if hasattr(model, 'entityId'):
                owner = BigWorld.entity(model.entityId)
                if not owner or not owner.inWorld:
                    return
                models = owner.fashion.getWeaponModels(gameglobal.WEAPON_LEFT)
                if not models:
                    return
                for i in models:
                    if i.inWorld:
                        node = i.node('HP_effect')
                        mist = gEffectMgr.attachEffect(effectId, effectLv, priority, node, info[1], effectType, maxDelayTime, txtInfo, 1.0, owner.model)
                        if mist != None:
                            attachedEffect.append(mist)

        elif attachType == ATTACH_RIGHTWEAPON:
            if hasattr(model, 'entityId'):
                owner = BigWorld.entity(model.entityId)
                models = owner.fashion.getWeaponModels(gameglobal.WEAPON_RIGHT)
                if not models:
                    return
                for i in models:
                    if i.inWorld:
                        node = i.node('HP_effect')
                        mist = gEffectMgr.attachEffect(effectId, effectLv, priority, node, info[1], effectType, maxDelayTime, txtInfo, 1.0, owner.model)
                        if mist != None:
                            attachedEffect.append(mist)

        elif attachType == ATTACH_RIGHTWEAPON_R1:
            if hasattr(model, 'entityId'):
                owner = BigWorld.entity(model.entityId)
                models = owner.fashion.getWeaponModels(gameglobal.WEAPON_RIGHT)
                if not models:
                    return
                for i in models:
                    if i.inWorld:
                        node = i.node('HP_effect')
                        mist = gEffectMgr.attachEffect(effectId, effectLv, priority, node, info[1], effectType, maxDelayTime, txtInfo, 1.0, owner.model)
                        if mist != None:
                            attachedEffect.append(mist)

        elif attachType == ATTACH_RIGHTWEAPON_L1:
            if hasattr(model, 'entityId'):
                owner = BigWorld.entity(model.entityId)
                models = owner.fashion.getWeaponModels(gameglobal.WEAPON_LEFT)
                if not models:
                    return
                for i in models:
                    if i.inWorld:
                        node = i.node('HP_effect')
                        mist = gEffectMgr.attachEffect(effectId, effectLv, priority, node, info[1], effectType, maxDelayTime, txtInfo, 1.0, owner.model)
                        if mist != None:
                            attachedEffect.append(mist)

        elif attachType == ATTACH_ORIGIN:
            dummy = getDummyModel()
            if targetPos:
                dummy.position = targetPos
            else:
                dummy.position = model.position
            if info[1] == DIR_UP_FACETARGET:
                if targetYaw:
                    dummy.yaw
                elif targetPos:
                    dummy.yaw = (targetPos - model.position).yaw
                elif getattr(model, 'creationId', None) and BigWorld.entities.get(model.creationId):
                    dummy.yaw = (BigWorld.entities.get(model.creationId).position - model.position).yaw
                elif getattr(model, 'hostId', None) and BigWorld.entities.get(model.hostId):
                    dummy.yaw = (BigWorld.entities.get(model.hostId).position - model.position).yaw
                else:
                    dummy.yaw = model.yaw
            elif targetYaw:
                dummy.yaw
            else:
                dummy.yaw = model.yaw
            mist = gEffectMgr.attachEffect(effectId, effectLv, priority, dummy.root, info[1], effectType, maxDelayTime, txtInfo, 1.0, model)
            if mist:
                attachedEffect.append(mist)
                if maxDelayTime == KEEPEFFECTTIME:
                    if clientcom.needDoOptimize():
                        maxDelayTime = MAXDELAYTIME
                    else:
                        gEffectMgr.addDummyEffect(mist, (effectId,
                         mist,
                         dummy,
                         effectType))
                mist.overCallback(Functor(detachOriginEffect, effectId, mist, dummy, effectType), maxDelayTime)
            else:
                giveBackDummyModel(dummy)
        elif attachType == ATTACH_DROP_POINT:
            dummy = getDummyModel()
            pos = flyEffect._findDropPoint(model.position)
            if pos:
                dummy.position = pos
            else:
                dummy.position = model.position
            if info[1] == DIR_UP_FACETARGET:
                if targetPos:
                    dummy.yaw = (targetPos - model.position).yaw
                elif getattr(model, 'creationId') and BigWorld.entities.get(model.creationId):
                    dummy.yaw = (BigWorld.entities.get(model.creationId).position - model.position).yaw
                elif getattr(model, 'hostId', None) and BigWorld.entities.get(model.hostId):
                    dummy.yaw = (BigWorld.entities.get(model.hostId).position - model.position).yaw
                else:
                    dummy.yaw = model.yaw
            else:
                dummy.yaw = model.yaw
            mist = gEffectMgr.attachEffect(effectId, effectLv, priority, dummy.root, info[1], effectType, maxDelayTime, txtInfo, 1.0, model)
            if mist:
                attachedEffect.append(mist)
                mist.overCallback(Functor(detachOriginEffect, effectId, mist, dummy, effectType), maxDelayTime)
            else:
                giveBackDummyModel(dummy)
        elif attachType == ATTACH_HIT:
            hitNode = None
            if hasattr(model, 'entityId'):
                owner = BigWorld.entity(model.entityId)
                if owner != None:
                    if hasattr(owner, 'getHitNodeRandom'):
                        hitNode = owner.getHitNodeRandom()
                    else:
                        gamelog.error('owner do not have getHitNodeRandom function, effectId: ' + str(effectId))
            else:
                hitNode = model.node('HP_hit_default')
            if hitNode != None:
                if info[1] == DIR_UP_FACEPLAYER:
                    dummy = getDummyModel()
                    position = clientcom.getPositionByNode(hitNode)
                    dummy.position = position
                    dummy.yaw = (BigWorld.player().position - position).yaw
                    gamelog.debug('DIR_UP_FACEPLAYER', dummy.position, dummy.yaw)
                    hitNode = dummy.root
                    BigWorld.callback(maxDelayTime + 1.0, Functor(giveBackDummyModel, dummy))
                elif info[1] == DIR_UP_FACETARGET and hasattr(model, 'hostId') and BigWorld.entities.get(model.hostId):
                    if len(hitNode.attachments) > HIT_EFFECT_FACEPLAYERSIZE:
                        return
                    dummy = getDummyModel()
                    position = clientcom.getPositionByNode(hitNode)
                    dummy.position = position
                    dummy.yaw = (BigWorld.entities.get(model.hostId).position - position).yaw
                    gamelog.debug('DIR_UP_FACEPLAYER', dummy.position, dummy.yaw)
                    hitNode = dummy.root
                    BigWorld.callback(maxDelayTime + 1.0, Functor(giveBackDummyModel, dummy))
                nodeScale = nodeScale / model.scale[0]
                mist = gEffectMgr.attachEffect(effectId, effectLv, priority, hitNode, info[1], effectType, maxDelayTime, txtInfo, nodeScale, model)
                if mist:
                    attachedEffect.append(mist)
            else:
                gamelog.error('zf:Error can not find HP_hit_default in model', model.sources, effectId)
        elif attachType == ATTACH_TARGET:
            if hasattr(model, 'entityId'):
                owner = BigWorld.entity(model.entityId)
                if owner != None and hasattr(owner, 'skillPlayer') and owner.skillPlayer.target != None:
                    targetModel = owner.skillPlayer.target.model
                    if targetModel and targetModel.inWorld:
                        mist = gEffectMgr.attachEffect(effectId, effectLv, priority, targetModel.root, info[1], effectType, maxDelayTime, txtInfo, 1.0, owner.model)
                        if mist:
                            attachedEffect.append(mist)
        elif attachType == ATTACH_YUANLING:
            if hasattr(model, 'entityId'):
                owner = BigWorld.entity(model.entityId)
                models = owner.fashion.getYuanLingModels()
                if not models:
                    return
                for i in models:
                    if i.inWorld:
                        node = i.node('HP_effect')
                        mist = gEffectMgr.attachEffect(effectId, effectLv, priority, node, info[1], effectType, maxDelayTime, txtInfo, 1.0, owner.model)
                        if mist != None:
                            attachedEffect.append(mist)

        else:
            node = model.node(attachPos)
            if node != None:
                mist = gEffectMgr.attachEffect(effectId, effectLv, priority, node, info[1], effectType, maxDelayTime, txtInfo, 1.0, model)
                if mist:
                    attachedEffect.append(mist)
            else:
                gamelog.warning('zf:attachEffect warning : can not find %s in model' % attachPos, model.sources, effectId, attachType)

    if len(attachedEffect) > 0:
        return attachedEffect


def attachMultiEffect(model, effectId, effectLv, priority, maxDelayTime = -1, targetPos = 0, ignorePrefix = False, txtInfo = None):
    targetPos = BigWorld.player().position
    step = 1.3
    numStep = len(effectId)
    delayTime = 0.05
    duration = 3
    deltaAngle = math.pi * 2.0 / 5
    rotateAngle = math.pi / 15.0
    groupEffect.playMultiEffectInCircum(effectId, effectLv, targetPos, step, numStep, delayTime, duration, deltaAngle, True, rotateAngle)


def detachOriginEffect(fxId, effect, dummy, effectType):
    gEffectMgr.giveBack(fxId, effect, dummy.root, effectType)
    giveBackDummyModel(dummy)


def testEffect(effectId, fxNumber = 10, effectLv = 3, radius = 3.0, maxDelayTime = 5.0):
    targetPos = BigWorld.player().position
    groupEffect.playCircle(effectId, effectLv, targetPos, radius, fxNumber, maxDelayTime)


dummyModel = 'effect/dummy/effectdummy.model'

class DummyModelMgr(object):
    INIT_CACHE_NUM = 50
    MAX_CACHE_NUM = 250

    def __init__(self):
        super(DummyModelMgr, self).__init__()
        self.cache = []
        for i in xrange(DummyModelMgr.INIT_CACHE_NUM):
            model = clientUtils.model(gameglobal.SFX_DUMMY_MODEL)
            model.dummyModel = True
            self.cache.append(model)

    def getModel(self, addToWorld = True):
        model = None
        if len(self.cache) > 0:
            model = self.cache.pop()
        if model is None or model.inWorld or model.attached or type(model) != BigWorld.Model:
            model = clientUtils.model(gameglobal.SFX_DUMMY_MODEL)
        model.dummyModel = True
        model.visible = True
        model.scale = (1.0, 1.0, 1.0)
        model.conn = None
        if addToWorld:
            try:
                player = BigWorld.player()
                if gameglobal.rds.GameState <= gametypes.GS_LOGIN:
                    if gameglobal.rds.loginScene.multiModels:
                        player = gameglobal.rds.loginScene.multiModels[0]
                player.addModel(model)
            except:
                gamelog.debug("can\'t find add model", model.sources)

        return model

    def clearAll(self):
        while self.cache:
            model = self.cache.pop()
            model = None

    def cacheSize(self):
        return len(self.cache)

    def isEmpty(self):
        return len(self.cache) == 0

    def giveBack(self, model, addToWorld = True):
        if model.inWorld:
            if addToWorld:
                p = BigWorld.player()
                if p:
                    try:
                        p.delModel(model)
                    except:
                        model = None
                        return

        if len(self.cache) >= DummyModelMgr.MAX_CACHE_NUM:
            model = None
        else:
            model.motors = ()
            model.visible = False
            if hasattr(model, 'fadeShader'):
                model.fadeShader = None
            if hasattr(model, 'distFadeShader'):
                model.distFadeShader = None
            if hasattr(model, 'noAttachFx_'):
                model.noAttachFx_ = False
            for attachemnt in model.root.attachments:
                model.root.detach(attachemnt)

            if not model.attached:
                if len(model.sources) == 1:
                    self.cache.append(model)
            else:
                gamelog.debug('model has attached', model.sources)


gDummyModelMgr = DummyModelMgr()

def getDummyModel(addToWorld = True):
    return gDummyModelMgr.getModel(addToWorld)


def giveBackDummyModel(model, addToWorld = True):
    return gDummyModelMgr.giveBack(model, addToWorld)


ARROW_COUNT = 0
REACH_COUNT = 0

class SimpleFlyer(object):

    def __init__(self):
        super(SimpleFlyer, self).__init__()
        self.motor = None
        self.model = None

    def start(self, model, srcPos, desPos, speed, callback):
        self.model = model
        motor = BigWorld.Slider()
        dir = desPos - srcPos
        motor.speed = speed
        motor.keepTime = dir.length / speed
        dir.normalise()
        motor.slideDir = dir
        self.motor = motor
        self.model.addMotor(self.motor)
        self.callback = callback
        BigWorld.callback(motor.keepTime, self.approach)

    def approach(self):
        if self.motor in self.model.motors:
            self.model.delMotor(self.motor)
        self.model = None
        self.motor = None
        if self.callback:
            self.callback()


class Flyer(object):

    def __init__(self, approachCallback = None):
        gamelog.debug('Flyer init.....................')
        super(Flyer, self).__init__()
        self.callback = approachCallback
        self.effects = None
        self.model = gDummyModelMgr.getModel()
        self.model.visible = False
        self.isReach = False
        self.flyDestEff = []
        self.flyTarget = None
        self.flyDestShakeCameras = []
        self.owner = None
        self.delayGiveBackTime = SYSCD.data.get('danDaoEffectDelayGiveBackTime', 1.0) + 0.5

    def setCallback(self, approachCallback):
        self.callback = approachCallback

    def start(self, startPos, matrix, heightOffset = 1.2, curvature = 0, zroll = 0, speed = 30, attachedEffects = None):
        global ARROW_COUNT
        gamelog.debug('Flyer start ... ', startPos, matrix, heightOffset, curvature, zroll, speed)
        ARROW_COUNT += 1
        self.model.position = startPos
        self.effects = attachedEffects
        mot = BigWorld.Rlauncher()
        self.model.addMotor(mot)
        mot.target = matrix
        mot.rotateSpeed = Math.Vector3(0, 0, 0)
        mot.offset = Math.Vector3(0, heightOffset, 0)
        mot.speed = speed
        mot.zroll = zroll
        mot.curvature = curvature
        mot.proximityCallback = self.approach
        self.mot = mot

    def setFlyDestEff(self, effs):
        self.flyDestEff = effs

    def approach(self):
        global REACH_COUNT
        self.isReach = True
        REACH_COUNT += 1
        if self.flyDestEff:
            effectLv = BigWorld.player().getSkillEffectLv()
            priority = BigWorld.player().getSkillEffectPriority()
            if self.owner and self.owner.inWorld:
                effectLv = self.owner.getSkillEffectLv()
                priority = self.owner.getSkillEffectPriority()
            for ef in self.flyDestEff:
                if self.flyTarget:
                    attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (effectLv,
                     priority,
                     self.flyTarget.model,
                     ef,
                     EFFECT_LIMIT,
                     gameglobal.EFFECT_LAST_TIME))
                else:
                    attachEffect(gameglobal.ATTACH_EFFECT_INPOS, [effectLv,
                     priority,
                     None,
                     ef,
                     EFFECT_LIMIT,
                     self.model.position,
                     0,
                     0,
                     0,
                     gameglobal.EFFECT_LAST_TIME])

            playShakeCamera(self.flyDestShakeCameras, None)
        if self.callback != None:
            self.callback()
        try:
            self.model.delMotor(self.mot)
        except:
            pass

        for ef in self.effects:
            ef.delayGiveBack = True
            ef.stop()

        delayTime = self.delayGiveBackTime
        BigWorld.callback(delayTime, self.release)

    def release(self):
        gDummyModelMgr.giveBack(self.model)
        self.owner = None
        self.model = None
        self.mot = None
        self.flyDestEff = []
        self.flyDestShakeCameras = []

    def addFlyEffect(self, effects):
        effectLv = BigWorld.player().getSkillEffectLv()
        priority = BigWorld.player().getSkillEffectPriority()
        if self.owner and self.owner.inWorld:
            effectLv = self.owner.getSkillEffectLv()
            priority = self.owner.getSkillEffectPriority()
        effs = []
        for effId in effects:
            eff = attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (effectLv,
             priority,
             self.model,
             effId,
             EFFECT_LIMIT,
             -1))
            if eff:
                effs.extend(eff)

        self.effects = effs


class FlyToNode(Flyer):

    def start(self, startPos, targetNode, curvature = 0, zroll = 0, speed = 20, attachedEffects = None, acceleration = 0, flyAccFlag = True, rotateSpeed = Math.Vector3(0, 0, 0), flyDestEff = None, flyTarget = None, shakeCameras = (), owner = None, isSucker = False):
        global ARROW_COUNT
        if isSucker == False:
            self.model.position = startPos
        else:
            self.model.position = targetNode.position
        ARROW_COUNT += 1
        self.model.visible = True
        self.effects = attachedEffects
        self.flyDestEff = flyDestEff
        if isSucker == False:
            self.flyTarget = flyTarget
        else:
            self.flyTarget = owner
        self.flyDestShakeCameras = shakeCameras
        self.owner = owner
        mot = BigWorld.Rlauncher()
        self.model.addMotor(mot)
        if isSucker == False:
            mot.target = targetNode
        elif str(type(startPos)) == "<type \'PyModelNode\'>":
            mot.target = startPos
        else:
            matrix = Math.Matrix()
            matrix.setTranslate(startPos)
            mot.target = matrix
        mot.rotateSpeed = rotateSpeed
        mot.speed = speed
        mot.acceleration = acceleration
        mot.proximity = 1
        mot.zroll = zroll
        mot.curvature = curvature
        mot.proximityCallback = self.approach
        self.mot = mot
        if flyAccFlag:
            if targetNode == None:
                return
            position = None
            if isSucker == False:
                position = clientcom.getPositionByNode(targetNode)
            else:
                if str(type(startPos)) == "<type \'PyModelNode\'>":
                    position = startPos.position
                else:
                    position = startPos
                startPos = targetNode.position
            dist = (position - startPos).length
            desireTime = dist / speed
            BigWorld.callback(desireTime, self.setAcceleration)

    def setAcceleration(self):
        if not self.isReach:
            self.mot.acceleration = self.mot.speed

    def _setOwner(self, onwer):
        self.owner = onwer

    def _setProximity(self, proximity = 0.5):
        if self.mot:
            self.mot.proximity = proximity

    def _adjustOffset(self, dist, angle):
        if self.isReach or self.mot == None:
            return
        owner = BigWorld.entity(self.owner)
        if owner == None or not owner.inWorld:
            return
        dir = self.mot.target.position - owner.position
        if dir.length < 1:
            yaw = owner.yaw
        else:
            dir.y = 0
            dir.normalise()
            yaw = dir.yaw + random.choice((-1, 1)) * angle
        self.mot.offset = (dist * math.sin(yaw), 0, dist * math.cos(yaw))
        BigWorld.callback(0.5, Functor(self._adjustOffset, dist, angle))

    def adjustOffset(self, owner, dist = 2, angle = 3.14 / 5):
        self._setOwner(owner)
        self._adjustOffset(dist, angle)


class DroppedItemFlyToNode(Flyer):

    def start(self, startPos, targetNode, curvature = 0, zroll = 0, speed = 20, attachedEffects = None, acceleration = 0, rotateSpeed = Math.Vector3(0, 0, 0)):
        self.model.position = startPos
        self.model.visible = True
        self.effects = attachedEffects
        mot = BigWorld.Rlauncher()
        self.model.addMotor(mot)
        mot.target = targetNode
        mot.rotateSpeed = rotateSpeed
        mot.speed = speed
        mot.acceleration = acceleration
        mot.proximity = 0.2
        mot.offset = Math.Vector3(0, 2.4, 0)
        mot.zroll = zroll
        mot.curvature = curvature
        mot.proximityCallback = self.approach
        self.mot = mot


class DroppedItemMultiPointFlyer(object):

    def __init__(self, model, points = []):
        super(DroppedItemMultiPointFlyer, self).__init__()
        self.effects = None
        self.model = model
        self.mot = BigWorld.Rlauncher()
        self.model.addMotor(self.mot)
        self.points = points

    def start(self, attachedEffects = None):
        if len(self.points) == 0:
            return
        self.effects = attachedEffects
        point = self.points.pop(0)
        if point[4] > 0:
            BigWorld.callback(point[4], Functor(self._run, point, attachedEffects))
        else:
            self._run(point, attachedEffects)

    def _run(self, point, attachedEffects):
        gamelog.debug('DroppedItemMultiPointFlyer_run ', point)
        self.model.position = point[0]
        if point[1].__class__.__name__ in ('Vector3', 'tuple'):
            mat = Math.Matrix()
            mat.setTranslate(point[1])
        else:
            mat = point[1]
        self.mot.target = mat
        self.mot.speed = point[3]
        self.mot.curvature = point[5]
        self.callback = point[2]
        self.mot.proximityCallback = Functor(self.approachPoint, attachedEffects)

    def approachPoint(self, attachedEffects = None):
        if self.callback:
            self.callback()
            self.callback = None
        self.start(attachedEffects)

    def release(self):
        try:
            self.model.delMotor(self.mot)
        except:
            gamelog.debug('DroppedItemMultiPointFlyer_run release', self.mot)

        self.mot = None
        gDummyModelMgr.giveBack(self.model)
        self.model = None


def droppedItemMultiFlyer(source, target):
    height = 0.0
    startPos = Math.Vector3(source.position + (0, height, 0))
    speed = 4.5
    points = [(startPos,
      target.position,
      target.endFly,
      speed * 2.5,
      0,
      0.0)]
    mf = DroppedItemMultiPointFlyer(target.model, points)
    mf.start()


def droppedItemFlyDemo(sourcePos, target, callback):
    dist = target.position.distTo(sourcePos)
    mot = BigWorld.Slider()
    mot.speed = 3
    mot.keepTime = dist / mot.speed - 0.2
    mot.speedAttenu = 1
    mot.rotateSpeed = 0
    dirp = target.position - sourcePos
    dirp.normalise()
    mot.slideDir = dirp
    target.model.addMotor(mot)
    BigWorld.callback(mot.keepTime, callback)


SHOOT_MODE_OK = 1
SHOOT_MODE_OVER_DISTANCE = 2
SHOOT_MODE_OBSTACLE = 3

class CircleEffect(object):

    def __init__(self):
        self.skillID = 0
        self.model = clientUtils.model(gameglobal.SFX_DUMMY_MODEL)
        self.model.dummyModel = True
        BigWorld.player().addModel(self.model)
        self.dirModel = clientUtils.model(gameglobal.SFX_DUMMY_MODEL)
        self.dirModel.dummyModel = True
        BigWorld.player().addModel(self.dirModel)
        self.indicatorModel = clientUtils.model(gameglobal.SFX_DUMMY_MODEL)
        self.indicatorModel.dummyModel = True
        BigWorld.player().addModel(self.indicatorModel)
        self.isShowingEffect = False
        self.isShowingBigCircle = False
        self.clipCursorPos = None
        self.skillPosition = None
        self.fxMode = gameglobal.CIRCLE_EFFECT_FX_MODE_POSITION
        self.gcd = 0.05
        self.runTime = 0
        self.skillRangeModel = None
        self.skillRangeFx = None
        self.skillRangeLimited = False
        try:
            self.fx = clientUtils.pixieFetch(getPath(SYSCD.data.get('sfxNormalCircle', gameglobal.SFX_NORMAL_CIRCLE)))
            self.fx.setAttachMode(0, 1, 0)
            self.fx.force()
            self.indicatorFx = clientUtils.pixieFetch(getPath(SYSCD.data.get('sfxIndicatorCircle', gameglobal.SFX_NORMAL_CIRCLE)))
            self.indicatorFx.setAttachMode(0, 1, 0)
            self.indicatorFx.force()
            self.redCircle = clientUtils.pixieFetch(getPath(SYSCD.data.get('sfxRedCircle', gameglobal.SFX_RED_CIRCLE)))
            self.redCircle.setAttachMode(0, 1, 0)
            self.redCircle.force()
            self.redIndicatorCircle = clientUtils.pixieFetch(getPath(SYSCD.data.get('sfxRedIndicatorCircle', gameglobal.SFX_RED_CIRCLE)))
            self.redIndicatorCircle.setAttachMode(0, 1, 0)
            self.redIndicatorCircle.force()
            self.dirCircles = []
            for fxId in SYSCD.data.get('sfxCircleShapes', gameglobal.SFX_CIRCLE_SHAPES):
                fx = clientUtils.pixieFetch(getPath(fxId))
                fx.force()
                self.dirCircles.append(fx)

            self.model.root.attach(self.fx)
            self.model.root.attach(self.redCircle)
            self.model.visible = False
            self.dirModel.visible = False
            self.indicatorModel.visible = False
            self._loaded = True
        except Exception as e:
            gamelog.error('CircleEffect load error', e.message)
            self._loaded = False

        self.isSkillMacroUse = False
        self.clearnIndicatorEffCB = None

    def addSkillRangeCircleModel(self):
        if self.skillRangeModel:
            return
        self.skillRangeModel = clientUtils.model(gameglobal.SFX_DUMMY_MODEL)
        self.skillRangeModel.dummyModel = True
        BigWorld.player().model.root.attach(self.skillRangeModel)
        self.skillRangeFx = clientUtils.pixieFetch(getPath(SYSCD.data.get('sfxBigNormalCircle', gameglobal.SFX_NORMAL_CIRCLE)))
        self.skillRangeFx.setAttachMode(0, 1, 0)
        self.skillRangeFx.force()
        self.skillRangeModel.root.attach(self.skillRangeFx)
        self.skillRangeModel.visible = False

    def delSkillRangeCircleModel(self):
        if not self.skillRangeModel:
            return
        if self.skillRangeFx in self.skillRangeModel.root.attachments:
            self.skillRangeModel.root.detach(self.skillRangeFx)
        self.skillRangeFx = None
        p = BigWorld.player()
        if p:
            if self.skillRangeModel in p.model.root.attachments:
                p.model.root.detach(self.skillRangeModel)
        self.skillRangeModel = None

    def playIndicatorEff(self, position, red):
        if not gameglobal.PLAY_INDICATOR_EFF:
            return
        if self.clearnIndicatorEffCB:
            BigWorld.cancelCallback(self.clearnIndicatorEffCB)
            self.clearnIndicatorEffCB = None
        self.indicatorModel.position = position
        self.indicatorModel.visible = True
        if red:
            if self.indicatorFx in self.indicatorModel.root.attachments:
                self.indicatorModel.root.detach(self.indicatorFx)
            if self.redIndicatorCircle not in self.indicatorModel.root.attachments:
                self.indicatorModel.root.attach(self.redIndicatorCircle)
            self.redIndicatorCircle.force()
        else:
            if self.redIndicatorCircle in self.indicatorModel.root.attachments:
                self.indicatorModel.root.detach(self.redIndicatorCircle)
            if self.indicatorFx not in self.indicatorModel.root.attachments:
                self.indicatorModel.root.attach(self.indicatorFx)
            self.indicatorFx.force()
        duration = SYSCD.data.get('sfxIndicatorFxDuration', 0.5)
        self.clearnIndicatorEffCB = BigWorld.callback(duration, self.clearnIndicatorEff)

    def clearnIndicatorEff(self):
        self.indicatorModel.visible = False

    def hasZaijuSkill(self, skillID):
        p = BigWorld.player()
        if p.bianshen and p.bianshen[0] == gametypes.BIANSHEN_ZAIJU:
            zaijuNo = p.bianshen[1]
            skills = ZJD.data.get(zaijuNo, {}).get('skills', [])
            for sid, lv in skills:
                if skillID == sid:
                    return True

        return False

    def specialCheckForActionPhysics(self, skillID, skillLevel):
        if BigWorld.player().getOperationMode() == gameglobal.ACTION_MODE and gameglobal.INTELLIGENT_CAST:
            self.skillID = skillID
            self.skillLevel = skillLevel
            result = self.getScreenPosInWorld()
            if result and self.canShoot(result[0]) == SHOOT_MODE_OVER_DISTANCE:
                return result
        return False

    def start(self, skillID, skillLevel, isDebug = False, fxMode = gameglobal.CIRCLE_EFFECT_FX_MODE_POSITION, circleShape = None):
        if BigWorld.time() < self.runTime + self.gcd:
            return
        self.isDebug = isDebug
        self.fxMode = fxMode
        if not self._loaded:
            return
        if not BigWorld.player().skills.has_key(skillID) and not BigWorld.player().wsSkills.has_key(skillID) and not self.hasZaijuSkill(skillID):
            return
        if not self.isShowingEffect:
            if BigWorld.player().chooseEffect.isShowingEffect:
                BigWorld.player().chooseEffect.cancel()
            self.isShowingEffect = True
            self.skillID = skillID
            self.skillLevel = skillLevel
            self._showCursor()
            if self.fxMode == gameglobal.CIRCLE_EFFECT_FX_MODE_POSITION:
                self.showSkillRangeLimitCircle()
                self.model.visible = True
            elif self.fxMode == gameglobal.CIRCLE_EFFECT_FX_MODE_DIRECTION:
                self._showShapeCircle(circleShape)
                self.dirModel.visible = True
            self.initCircleRadius()
            self.updateEffect()
            if BigWorld.player().getOperationMode() == gameglobal.ACTION_MODE:
                cord = BigWorld.player().ap.getAimCord()
                C_ui.set_cursor_pos(cord[0] + 1, cord[1])
        BigWorld.player().shortcutToPostionSkillId = skillID

    def showSkillRangeLimitCircle(self):
        p = BigWorld.player()
        if p.isInBfDota():
            self.skillRangeLimited = True
            self.isShowingBigCircle = True
            if self.skillRangeModel:
                self.skillRangeModel.visible = True
                self.skillRangeFx.scale(self.getDistance()[1] / 20.0 / p.model.scale[0])

    def hideSkillRangeLimitCircle(self):
        self.skillRangeLimited = False
        self.isShowingBigCircle = False
        if self.skillRangeModel:
            self.skillRangeModel.visible = False

    def _showShapeCircle(self, circleShape):
        for fx in self.dirCircles:
            if fx in self.dirModel.root.attachments:
                self.dirModel.root.detach(fx)
                fx.clear()
                fx.scale(1)

        shapeIdx = circleShape[0]
        xScale = circleShape[1]
        zScale = circleShape[2]
        shapeFx = self.dirCircles[shapeIdx - 1]
        shapeFx.clear()
        if shapeIdx in gameglobal.CIRCLE_EFFECT_WHOLE_SCALE:
            shapeFx.scale(xScale, xScale, xScale)
        elif shapeIdx == gameglobal.SFX_SQUARE_CIRCLE_IDX:
            shapeFx.scale(xScale, xScale, zScale)
        self.dirModel.root.attach(shapeFx)
        shapeFx.force()

    def _showCursor(self):
        if BigWorld.player().getOperationMode() == gameglobal.ACTION_MODE:
            BigWorld.player().ap.restore()
            BigWorld.player().ap.inMouseSelectSkillPos = True
            BigWorld.player().ap.refreshUIEnabled()

    def _restoreCursor(self):
        if BigWorld.player().getOperationMode() == gameglobal.ACTION_MODE:
            BigWorld.player().ap.showCursor = False
            BigWorld.player().ap.reset()
            BigWorld.player().ap.inMouseSelectSkillPos = False
            BigWorld.player().ap.refreshUIEnabled()

    def initCircleRadius(self):
        radius = skillDataInfo.getSkillAreaRadius(BigWorld.player().getSkillInfo(self.skillID, self.skillLevel))
        if radius:
            self.circleRadius = radius
        self.redCircle.scale(self.circleRadius / 5.0)
        self.fx.scale(self.circleRadius / 5.0)

    def getDistance(self):
        skillMinRange, skillMaxRange = skillDataInfo.getSkillRange(BigWorld.player().getSkillInfo(self.skillID, self.skillLevel))
        if not skillMinRange:
            skillMinRange = 0
        if not skillMaxRange:
            skillMaxRange = 1000
        return (skillMinRange, skillMaxRange)

    def updatePosFx(self, result, cameraInWater):
        if not self.skillRangeLimited:
            if self.canShoot(result[0]) != SHOOT_MODE_OK:
                if self.fx in self.model.root.attachments:
                    self.model.root.detach(self.fx)
                if self.redCircle not in self.model.root.attachments:
                    self.model.root.attach(self.redCircle)
            else:
                if self.redCircle in self.model.root.attachments:
                    self.model.root.detach(self.redCircle)
                if self.fx not in self.model.root.attachments:
                    self.model.root.attach(self.fx)
        if result[0] != None:
            if result[3] == 256 and not cameraInWater:
                self.fx.enableTerrainTouch(False)
                self.redCircle.enableTerrainTouch(False)
                self.model.position = result[0] + Math.Vector3(0, 0.1, 0)
            else:
                self.fx.enableTerrainTouch(True)
                self.redCircle.enableTerrainTouch(True)
                self.model.position = result[0]

    def updateDirFx(self, result, cameraInWater):
        p = BigWorld.player()
        self.dirModel.position = p.position
        self.dirModel.yaw = (result[0] - p.position).yaw

    def getScreenPosInWorld(self, calcClip = False):
        p = BigWorld.player()
        cameraInWater = self.isCameraInWater()
        if self.clipCursorPos and p.getOperationMode() == gameglobal.KEYBOARD_MODE and p.ap._msleft:
            result = BigWorld.getScreenPosInWorld(p.spaceID, self.clipCursorPos.x, self.clipCursorPos.y, 1000, not cameraInWater, (gameglobal.TREEMATTERKINDS,))
        elif p.getOperationMode() == gameglobal.ACTION_MODE and (gameglobal.INTELLIGENT_CAST or self.isSkillMacroUse):
            yOffset = BigWorld.player().ap.aimCross.cursorAim.position[1]
            result = BigWorld.getScreenPosInWorld(p.spaceID, 0, yOffset, 1000, not cameraInWater, (gameglobal.TREEMATTERKINDS,))
        else:
            result = BigWorld.getCursorPosInWorld(p.spaceID, 1000, not cameraInWater, (gameglobal.TREEMATTERKINDS, gameglobal.GLASSMATTERKINDS))
        result = list(result)
        if self.skillRangeLimited and self.fxMode == gameglobal.CIRCLE_EFFECT_FX_MODE_POSITION:
            if self.canShoot(result[0]) == SHOOT_MODE_OVER_DISTANCE:
                p = BigWorld.player()
                vMousePoint = Math.Vector3(result[0])
                vPlayer = Math.Vector3(p.position)
                dist = vPlayer.distTo(vMousePoint)
                vPlayer2Point = vMousePoint - vPlayer
                minDis, maxDis = self.getDistance()
                if dist < minDis:
                    vPlayer2LimitPoint = vPlayer2Point * ((minDis - 0.1) * 1.0 / dist)
                else:
                    vPlayer2LimitPoint = vPlayer2Point * ((maxDis - 0.1) * 1.0 / dist)
                vLimitPoint = vPlayer + vPlayer2LimitPoint
                result[0] = vLimitPoint
        if not calcClip:
            return result
        ca = BigWorld.camera()
        x1, y1, z1 = ca.position
        x2, y2, z2 = result[0]
        y3 = p.position[1]
        if y1 != y2:
            x3 = (x2 - x1) * (y3 - y1) / (y2 - y1) + x1
            z3 = (z2 - z1) * (y3 - y1) / (y2 - y1) + z1
        else:
            x3 = x2
            z3 = z2
            y3 = y3
        result[0] = Math.Vector3(x3, y3, z3)
        return result

    def updateEffect(self, isSkillMacroUse = False):
        self.isSkillMacroUse = isSkillMacroUse
        if self.isShowingEffect:
            cameraInWater = self.isCameraInWater()
            if self.fxMode == gameglobal.CIRCLE_EFFECT_FX_MODE_POSITION:
                result = self.getScreenPosInWorld()
                self.updatePosFx(result, cameraInWater)
            elif self.fxMode == gameglobal.CIRCLE_EFFECT_FX_MODE_DIRECTION:
                result = self.getScreenPosInWorld(True)
                self.updateDirFx(result, cameraInWater)
            BigWorld.callback(0.01, self.updateEffect)

    def run(self):
        if not gameglobal.gIsAppActive:
            self.cancel()
            return
        if self.isShowingEffect:
            self.runTime = BigWorld.time()
            p = BigWorld.player()
            if self.fxMode == gameglobal.CIRCLE_EFFECT_FX_MODE_POSITION:
                result = self.model.position
            else:
                result = self.dirModel.position
            shootMode = self.canShoot(result)
            castTime = skillDataInfo.getCastTime(p.getSkillInfo(self.skillID, self.skillLevel))
            if p.spellingType:
                gamelog.debug('zf:动作未完成')
            if not logicInfo.isUseableSkill(self.skillID):
                gamelog.debug('zf:技能不可用')
            elif shootMode == SHOOT_MODE_OK:
                self.isShowingEffect = False
                self.model.visible = False
                self.hideSkillRangeLimitCircle()
                self.dirModel.visible = False
                if castTime:
                    p.ap.stopMove()
                if self.fxMode == gameglobal.CIRCLE_EFFECT_FX_MODE_POSITION:
                    p.skillPlayer.targetPos = result
                    if not getattr(self, 'isDebug', False):
                        p.cell.useSkillPos(self.skillID, result)
                    else:
                        p.cell.useSkillPosDebug(self.skillID, self.skillLevel, result)
                    if gameglobal.INTELLIGENT_CAST and p.getOperationMode() in (gameglobal.KEYBOARD_MODE, gameglobal.ACTION_MODE):
                        self.playIndicatorEff(result, False)
                elif self.fxMode == gameglobal.CIRCLE_EFFECT_FX_MODE_DIRECTION:
                    self.fxMode = gameglobal.CIRCLE_EFFECT_FX_MODE_POSITION
                    yaw = self.dirModel.yaw
                    p.faceToDir(yaw, True)
                    skillInfo = p.getSkillInfo(self.skillID, self.skillLevel)
                    cellCmd._callUseSkill(p, skillInfo, BigWorld.player())
                if gameglobal.INTELLIGENT_CAST and p.getOperationMode() == gameglobal.ACTION_MODE:
                    cursor.ignoreCursorPos = True
                self._restoreCursor()
            elif shootMode == SHOOT_MODE_OVER_DISTANCE:
                enableSkillDistAutoOpt = gameglobal.rds.configData.get('enableSkillDistAutoOpt', False)
                if p.getOperationMode() == gameglobal.MOUSE_MODE or enableSkillDistAutoOpt:
                    skillMinDist, skillMaxDist = skillDataInfo.getSkillRange(p.getSkillInfo(self.skillID, self.skillLevel))
                    if not p.ap.isChasing:
                        p.skillId = self.skillID
                        p.skillLevel = 1
                        p.autoUseSkill = True
                        p.ap.isChasing = True
                        self.cancel()
                        dist = p.position.distTo(result) - skillMaxDist
                        dirVector = result - p.position
                        x = p.position[0] + dist * math.sin(dirVector.yaw)
                        y = p.position[1]
                        z = p.position[2] + dist * math.cos(dirVector.yaw)
                        destPosition = Math.Vector3(x, y, z)
                        self.skillPosition = result
                        p.ap.seekPath(destPosition, self.autoUseSkillPos)
                else:
                    dist = Math.Vector3(p.position).distTo(result)
                    minRange, maxRange = self.getDistance()
                    if dist > maxRange:
                        p.showGameMsg(GMDD.data.DIST_TOO_FAR, ())
                    elif dist < minRange:
                        p.showGameMsg(GMDD.data.DIST_TOO_CLOSE, ())
            elif shootMode == SHOOT_MODE_OBSTACLE:
                p.showGameMsg(GMDD.data.BLOCKED_BY_WALL, ())
                gamelog.debug('zf:障碍阻挡')
            p.shortcutToPostionSkillId = 1

    def autoUseSkillPos(self, success):
        p = BigWorld.player()
        if self.skillPosition:
            if not getattr(self, 'isDebug', False):
                p.cell.useSkillPos(self.skillID, self.skillPosition)
            else:
                p.cell.useSkillPosDebug(self.skillID, self.skillLevel, self.skillPosition)
            self.skillPosition = None
            p.autoUseSkill = False

    def cancel(self):
        if self.isShowingEffect:
            self.isShowingEffect = False
            self.model.visible = False
            self.dirModel.visible = False
            self._restoreCursor()
        self.isSkillMacroUse = False
        self.hideSkillRangeLimitCircle()
        BigWorld.player().shortcutToPostionSkillId = 1

    def canShoot(self, targetPos):
        p = BigWorld.player()
        dist = Math.Vector3(p.position).distTo(targetPos)
        minRange, maxRange = self.getDistance()
        if dist > maxRange or dist < minRange:
            return SHOOT_MODE_OVER_DISTANCE
        for h in (0.5, 1.0):
            if BigWorld.collide(p.spaceID, p.position + Math.Vector3(0, h * 2, 0), targetPos + Math.Vector3(0, h * 2, 0), gameglobal.TREEMATTERKINDS) == None:
                return SHOOT_MODE_OK

        return SHOOT_MODE_OBSTACLE

    def isCameraInWater(self):
        p = BigWorld.player()
        if not p:
            return False
        c = BigWorld.camera()
        waterHeight = BigWorld.findWaterFromPoint(p.spaceID, c.position)
        if waterHeight and c.position[1] < waterHeight[0]:
            return True
        return False


class ChooseEffect(object):

    def __init__(self):
        self.skillID = 0
        self.isShowingEffect = False
        self.gcd = 0.05
        self.runTime = 0
        self.lastCursorPos = ()

    def hasZaijuSkill(self, skillID):
        p = BigWorld.player()
        if p.bianshen and p.bianshen[0] == gametypes.BIANSHEN_ZAIJU:
            zaijuNo = p.bianshen[1]
            skills = ZJD.data.get(zaijuNo, {}).get('skills', [])
            for sid, lv in skills:
                if skillID == sid:
                    return True

        return False

    def start(self, skillID, skillLevel, isDebug = False):
        if BigWorld.time() < self.runTime + self.gcd:
            return
        self.isDebug = isDebug
        if not BigWorld.player().skills.has_key(skillID) and not BigWorld.player().wsSkills.has_key(skillID) and not self.hasZaijuSkill(skillID):
            return
        if not self.isShowingEffect:
            if BigWorld.player().circleEffect.isShowingEffect:
                BigWorld.player().circleEffect.cancel()
            self.isShowingEffect = True
            self._showCursor()
            self.skillID = skillID
            self.skillLevel = skillLevel
            if BigWorld.player().getOperationMode() == gameglobal.ACTION_MODE:
                cord = BigWorld.player().ap.getAimCord()
                C_ui.set_cursor_pos(cord[0] + 1, cord[1])
                ui.reset_cursor()
                if self.lastCursorPos and self.lastCursorPos[0][0] > 0:
                    if time.time() - self.lastCursorPos[1] < SYSCD.data.get('chooseCursorTime', 3.0):
                        C_ui.set_cursor_pos(self.lastCursorPos[0][0], self.lastCursorPos[0][1])
                        BigWorld.player().needUpdateChoosePos = True
                BigWorld.target.exclude = None
        BigWorld.player().shortcutToChooseSkillId = skillID

    def _showCursor(self):
        if BigWorld.player().getOperationMode() == gameglobal.ACTION_MODE:
            BigWorld.player().ap.restore()

    def _restoreCursor(self):
        if BigWorld.player().getOperationMode() == gameglobal.ACTION_MODE:
            BigWorld.player().ap.showCursor = False
            BigWorld.player().ap.reset()
            ui.reset_cursor()

    def getDistance(self):
        skillMinRange, skillMaxRange = skillDataInfo.getSkillRange(BigWorld.player().getSkillInfo(self.skillID, self.skillLevel))
        if not skillMinRange:
            skillMinRange = 0
        if not skillMaxRange:
            skillMaxRange = 1000
        return (skillMinRange, skillMaxRange)

    def run(self, target):
        if not gameglobal.gIsAppActive:
            self.cancel()
            return
        if self.isShowingEffect:
            self.runTime = BigWorld.time()
            p = BigWorld.player()
            shootMode = self.canShoot(target)
            castTime = skillDataInfo.getCastTime(BigWorld.player().getSkillInfo(self.skillID, self.skillLevel))
            if p.spellingType:
                gamelog.debug('zf:动作未完成')
            if not logicInfo.isUseableSkill(self.skillID):
                gamelog.debug('zf:技能不可用')
            elif shootMode == SHOOT_MODE_OK:
                self.isShowingEffect = False
                if castTime:
                    p.ap.stopMove()
                if not getattr(self, 'isDebug', False):
                    skillInfo = p.getSkillInfo(self.skillID, self.skillLevel)
                    cellCmd._callUseSkill(p, skillInfo, target)
                else:
                    p.cell.useSkillDebug(self.skillID, self.skillLevel, target)
                lastCursorPos = cursor.setOutAndSaveOldPos()
                self.lastCursorPos = (lastCursorPos, time.time())
                self._restoreCursor()
            elif shootMode == SHOOT_MODE_OVER_DISTANCE:
                gamelog.debug('--------------超出距离')
            elif shootMode == SHOOT_MODE_OBSTACLE:
                p.showGameMsg(GMDD.data.BLOCKED_BY_WALL, ())
                gamelog.debug('zf:障碍阻挡')
            p.shortcutToChooseSkillId = 1
            ui.reset_cursor()
            BigWorld.target.exclude = BigWorld.player()

    def autoUseSkillPos(self, success):
        p = BigWorld.player()
        if self.skillPosition:
            if not getattr(self, 'isDebug', False):
                p.cell.useSkillPos(self.skillID, self.skillPosition)
            else:
                p.cell.useSkillPosDebug(self.skillID, self.skillLevel, self.skillPosition)
            self.skillPosition = None
            p.autoUseSkill = False

    def cancel(self):
        if self.isShowingEffect:
            self.isShowingEffect = False
            lastCursorPos = cursor.setOutAndSaveOldPos()
            if self.lastCursorPos:
                lastCursorPos = lastCursorPos if lastCursorPos[0] > 0 else self.lastCursorPos[0]
            self.lastCursorPos = (lastCursorPos, time.time())
            self._restoreCursor()
        BigWorld.player().shortcutToChooseSkillId = 1
        if not BigWorld.player().inBooth():
            BigWorld.target.exclude = BigWorld.player()

    def canShoot(self, target):
        p = BigWorld.player()
        dist = Math.Vector3(p.position).distTo(target.position)
        rangeMin, rangeMax = self.getDistance()
        if rangeMax and rangeMax < dist:
            p.showGameMsg(GMDD.data.DIST_TOO_FAR, ())
            return SHOOT_MODE_OVER_DISTANCE
        if rangeMin and rangeMin > dist:
            p.showGameMsg(GMDD.data.DIST_TOO_FAR, ())
            return SHOOT_MODE_OVER_DISTANCE
        if not getattr(target, 'IsCombatUnit', False):
            p.showGameMsg(GMDD.data.DIST_TOO_FAR, ())
            return SHOOT_MODE_OVER_DISTANCE
        skillInfo = BigWorld.player().getSkillInfo(self.skillID, self.skillLevel)
        skillTargetType, skillTargetValue = p.getSkillTargetType(skillInfo)
        if skillTargetType == gametypes.SKILL_TARGET_FRIEND:
            if not p.isFriend(target):
                p.showGameMsg(GMDD.data.NEED_TARGET_FRIEND, ())
                return SHOOT_MODE_OVER_DISTANCE
        elif skillTargetType == gametypes.SKILL_TARGET_SELF_FRIEND:
            if not p.isFriend(target):
                p.showGameMsg(GMDD.data.NEED_TARGET_FRIEND, ())
                return SHOOT_MODE_OVER_DISTANCE
        if skillTargetValue != gametypes.OBJ_TYPE_DEAD_BODY and target.life == gametypes.LIFE_DEAD:
            p.showGameMsg(GMDD.data.SKILL_FORBIDDEN_TARGET_REMAIN, ())
            return SHOOT_MODE_OVER_DISTANCE
        if skillTargetValue == gametypes.OBJ_TYPE_DEAD_BODY and target.life != gametypes.LIFE_DEAD:
            p.showGameMsg(GMDD.data.SKILL_FORBIDDEN_TARGET_ALIVE, ())
            return SHOOT_MODE_OVER_DISTANCE
        for h in (0.5, 1.0):
            if BigWorld.collide(p.spaceID, p.position + Math.Vector3(0, h * 2, 0), target.position + Math.Vector3(0, h * 2, 0), gameglobal.TREEMATTERKINDS) == None:
                return SHOOT_MODE_OK

        return SHOOT_MODE_OBSTACLE


class BodyShakeFlyer(object):

    def __init__(self, owner, points = [], speed = 0):
        self.owner = owner
        self.points = points
        self.model = owner.model
        self.speed = speed
        if hasattr(self.owner.filter, 'resetClientYawMinDist'):
            self.owner.filter.clientYawMinDist = 0.0
        if hasattr(self.owner.filter, 'keepYawTime'):
            self.owner.filter.keepYawTime = 999999
        if not hasattr(self.model, 'modelShake'):
            self.model.modelShake = BigWorld.ModelShake()

    def start(self):
        if not self.owner or not self.owner.inWorld:
            self.release()
            return
        if len(self.points) == 0:
            self.release()
            return
        self.model.modelShake.shake(self.points, self.speed)

    def release(self):
        if hasattr(self.owner, 'resetClientYawMinDist'):
            self.owner.resetClientYawMinDist()
        if self.owner and hasattr(self.owner.filter, 'keepYawTime'):
            self.owner.filter.keepYawTime = 0.0
        if hasattr(self.model, 'modelShake'):
            self.model.modelShake = None
        self.owner = None
        self.model = None
        self.points = None
        self.speed = 0


class MultiPointFlyer(object):

    def __init__(self, points = []):
        super(MultiPointFlyer, self).__init__()
        self.effects = None
        self.model = gDummyModelMgr.getModel()
        self.mot = BigWorld.Rlauncher()
        self.model.addMotor(self.mot)
        self.points = points

    def start(self, attachedEffects = None):
        if len(self.points) == 0:
            ef = None
            soundPath = 'fx/char/soul_end'
            gameglobal.rds.sound.playFx(soundPath, self.model.position, False, BigWorld.player())
            for ef in self.effects:
                ef.stop()

            self.release()
            return
        self.effects = attachedEffects
        point = self.points.pop(0)
        if point[4] > 0:
            BigWorld.callback(point[4], Functor(self._run, point, attachedEffects))
        else:
            self._run(point, attachedEffects)

    def _run(self, point, attachedEffects):
        global ARROW_COUNT
        gamelog.debug('_run ', point)
        ARROW_COUNT += 1
        self.model.position = point[0]
        if point[1].__class__.__name__ in ('Vector3', 'tuple'):
            mat = Math.Matrix()
            mat.setTranslate(point[1])
        else:
            mat = point[1]
        self.mot.target = mat
        self.mot.speed = point[3]
        self.mot.curvature = point[5]
        self.mot.acceleration = 2
        self.mot.proximity = 0.2
        self.mot.zroll = random.uniform(-1, 1)
        self.callback = point[2]
        self.mot.proximityCallback = Functor(self.approachPoint, attachedEffects)

    def approachPoint(self, attachedEffects = None):
        if self.callback:
            self.callback()
            self.callback = None
        self.start(attachedEffects)

    def release(self):
        global REACH_COUNT
        REACH_COUNT += 1
        try:
            self.model.delMotor(self.mot)
        except:
            gamelog.debug('MultiPointFlyer:release', self.mot)

        self.mot = None
        gDummyModelMgr.giveBack(self.model)
        self.model = None


def testMultiFlyer(target, sourceBodySize, sourceData = ()):
    p = BigWorld.player()
    if sourceBodySize > 5:
        height = 3
    else:
        height = 0.5
    startPos = Math.Vector3(target.position + (0, height, 0))
    localToWorld = Math.Matrix(target.matrix)
    x1 = random.choice((1, -1)) * random.uniform(0.75, 1.5)
    z1 = random.choice((1, -1)) * random.uniform(0.75, 1.5)
    y1 = random.uniform(0.25, 0.75)
    sp = localToWorld.applyPoint((x1, y1, z1))
    secondPos = sp + (sp - startPos) / 2
    secondPos[1] = sp[1]
    speed = 2
    data = SYSCD.data
    effects = (data.get('sfxExp', 0),
     data.get('sfxBindCash', 0),
     data.get('sfxCash', 0),
     data.get('sfxHp', 0),
     data.get('sfxMp', 0),
     data.get('sfxQuest', 0))
    if sourceData:
        effect = effects[sourceData[0]]
    else:
        effect = random.choice(effects)
    points = [(startPos,
      sp,
      None,
      speed,
      0,
      1.5), (sp,
      secondPos,
      None,
      speed,
      0,
      1.5), (secondPos,
      BigWorld.player().getHitNodeRandom(),
      Functor(endSoulFlyDemo, target, sourceData),
      speed * 2.5,
      0,
      1)]
    mf = MultiPointFlyer(points)
    mf.mot.needStepBackTime = False
    attached = attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (p.getSkillEffectLv(),
     p.getSkillEffectPriority(),
     mf.model,
     effect,
     EFFECT_LIMIT,
     15.0))
    attachedEffects = []
    if attached != None:
        for ae in attached:
            attachedEffects.append(ae)

    mf.start(attachedEffects)


def testBodyShakeFlyer(eid):
    ent = BigWorld.entities[eid]
    effectData = {'shakeModel': [1,
                    1,
                    1,
                    5,
                    0.9]}
    ent.playBodyShake(effectData)


def soulFlyDemo(target, sourceBodySize, isBianshi = False):
    if target:
        if isBianshi:
            sourceDataTuple = ((const.REWARD_LABEL_EXP,), (const.REWARD_LABEL_BINDCASH,))
        else:
            sourceDataTuple = []
            if target.id in gameglobal.rds.ui.cashMap or target.id in gameglobal.rds.ui.bindCashMap:
                sourceDataTuple.append((const.REWARD_LABEL_BINDCASH, target.id))
            if target.id in gameglobal.rds.ui.expMap:
                sourceDataTuple.append((const.REWARD_LABEL_EXP, target.id))
            if target.id in gameglobal.rds.ui.hpMap:
                sourceDataTuple.append((const.REWARD_LABEL_HP, target.id))
            if target.id in gameglobal.rds.ui.mpMap:
                sourceDataTuple.append((const.REWARD_LABEL_MP, target.id))
            if not sourceDataTuple:
                return
            sourceDataTuple = tuple(sourceDataTuple)
        for sourceDataItem in sourceDataTuple:
            testMultiFlyer(target, sourceBodySize, sourceDataItem)


def showSpecialQuestsExp(tgtId, exp, times):
    tgt = BigWorld.entities.get(tgtId)
    if not tgt:
        return
    for i in xrange(times):
        testMultiFlyer(tgt, getattr(tgt, 'bodySize', 1), (5, 0))

    t = (tgt.position - BigWorld.player().position).length / 5
    BigWorld.callback(t, Functor(showQuestsExpLabel, exp, times))


def showQuestsExpLabel(exp, times):
    for i in xrange(times):
        BigWorld.callback(0.2 * i, Functor(gameglobal.rds.ui.showRewardLabel, exp, 0))


def restoreFresnelColor():
    BigWorld.player().model.setFresnel(0, 0, 1, 0, 0, 0)


def addSoulFlyTint(tintTime, fresnelColor = (0.2, 3.2, 0.2)):
    p = BigWorld.player()
    if hasattr(BigWorld.player().model, 'fresnelColor'):
        p.model.setFresnel(0.1, tintTime / 2, tintTime, fresnelColor[0], fresnelColor[1], fresnelColor[2])


def endSoulFlyDemo(tgt, sourceData = ()):
    p = BigWorld.player()
    tintTime, expTintId, cashTintId, hpTintId, mpTintId = SYSCD.data.get('soulFresnelColor', (0.3,
     (0.2, 3.2, 0.2),
     (0.2, 3.2, 0.2),
     (0.2, 3.2, 0.2),
     (0.2, 3.2, 0.2)))
    if sourceData:
        if sourceData[0] == const.REWARD_LABEL_SPECIAL_QUESTS:
            if p.model and hasattr(p.model, 'fresnelColor'):
                addSoulFlyTint(tintTime)
        elif sourceData[0] == const.REWARD_LABEL_EXP:
            addSoulFlyTint(tintTime, expTintId)
            if len(sourceData) == 2 and sourceData[1] in gameglobal.rds.ui.expMap:
                gameglobal.rds.ui.showRewardLabel(gameglobal.rds.ui.expMap[sourceData[1]], sourceData[0])
                del gameglobal.rds.ui.expMap[sourceData[1]]
        elif sourceData[0] == const.REWARD_LABEL_BINDCASH:
            addSoulFlyTint(tintTime, cashTintId)
            if len(sourceData) == 2:
                if sourceData[1] in gameglobal.rds.ui.bindCashMap:
                    gameglobal.rds.ui.showRewardLabel(gameglobal.rds.ui.bindCashMap[sourceData[1]], const.REWARD_LABEL_BINDCASH)
                    del gameglobal.rds.ui.bindCashMap[sourceData[1]]
                if sourceData[1] in gameglobal.rds.ui.cashMap:
                    gameglobal.rds.ui.showRewardLabel(gameglobal.rds.ui.cashMap[sourceData[1]], const.REWARD_LABEL_CASH)
                    del gameglobal.rds.ui.cashMap[sourceData[1]]
        elif sourceData[0] == const.REWARD_LABEL_HP:
            addSoulFlyTint(tintTime, hpTintId)
            if len(sourceData) == 2:
                if sourceData[1] in gameglobal.rds.ui.hpMap:
                    del gameglobal.rds.ui.hpMap[sourceData[1]]
        elif sourceData[0] == const.REWARD_LABEL_MP:
            addSoulFlyTint(tintTime, mpTintId)
            if len(sourceData) == 2:
                if sourceData[1] in gameglobal.rds.ui.mpMap:
                    del gameglobal.rds.ui.mpMap[sourceData[1]]
    attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (p.getBasicEffectLv(),
     p.getBasicEffectPriority(),
     p.model,
     2039,
     EFFECT_LIMIT,
     3.0))
    soundPath = 'fx/char/Shared/soul_end'
    gameglobal.rds.sound.playFx(soundPath, tgt.position, False)


gLength = 15
gNumStep = 7
gDuration = 2
gDelayTime = 0.0
gDelayStart = 0.0

def getEffectNode(model, effectId):
    attachNode = []
    if not model or not model.inWorld:
        return attachNode
    if hasattr(model, 'noAttachFx_') and model.noAttachFx_:
        return attachNode
    attachInfo = gEffectInfoMap.getInfo(effectId, model)
    if attachInfo == None:
        return attachNode
    for info in attachInfo[0]:
        attachType = info[0]
        attachPos = info[1]
        if attachType == ATTACH_ROOT:
            attachNode.append(model.root)
        elif attachType == ATTACH_LEFTWEAPON:
            if hasattr(model, 'entityId'):
                owner = BigWorld.entity(model.entityId)
                models = owner.fashion.getWeaponModels(gameglobal.WEAPON_LEFT)
                for i in models:
                    if i.inWorld:
                        node = i.node(attachPos)
                        attachNode.append(node)

        elif attachType == ATTACH_RIGHTWEAPON:
            if hasattr(model, 'entityId'):
                owner = BigWorld.entity(model.entityId)
                models = owner.fashion.getWeaponModels(gameglobal.WEAPON_RIGHT)
                for i in models:
                    if i.inWorld:
                        node = i.node(attachPos)
                        attachNode.append(node)

        elif attachType == ATTACH_ORIGIN:
            attachNode.append(model.root)
        elif attachType == ATTACH_HIT:
            attachNode.append(model.root)
        elif attachType == ATTACH_TARGET:
            if hasattr(model, 'entityId'):
                owner = BigWorld.entity(model.entityId)
                if owner != None and hasattr(owner, 'skillPlayer') and owner.skillPlayer.target != None:
                    targetModel = owner.skillPlayer.target.model
                    if targetModel and targetModel.inWorld:
                        attachNode.append(targetModel.root)
        elif attachType == ATTACH_NODE:
            node = model.node(attachPos)
            attachNode.append(node)

    return attachNode


def detachEffect(model, effectId, fxs, forceRemove = False):
    if not fxs:
        return
    if not forceRemove:
        forceRemove = SFD.data.get(effectId, {}).get('forceRemove', False)
    if not forceRemove:
        for fx in fxs:
            fx.stop()

        return
    attachNode = getEffectNode(model, effectId)
    for fx in fxs:
        if fx:
            for node in attachNode:
                gEffectMgr.giveBack(effectId, fx, node, EFFECT_UNLIMIT)


class PositionNodeEffectConnect(object):

    def __init__(self, lv, startPosition, fxFilename, node2, maxLength = 50, priority = 7):
        self.dummy = None
        if not startPosition or not node2:
            return
        try:
            fxFilename = getPath(fxFilename)
            particle = clientUtils.pixieFetch(fxFilename, lv)
        except:
            gamelog.error('can not create particle', fxFilename)
            return

        conn = BigWorld.PyConnector()
        conn.target = node2
        conn.length = 15
        conn.maxLength = maxLength
        conn.distExceedCallback = self.distExceedCallback
        dummy = gDummyModelMgr.getModel()
        dummy.dummyModel = True
        dummy.conn = conn
        dummy.position = startPosition
        dummy.visible = True
        self.dummy = dummy
        particle.setAttachMode(0, 0, 0)
        dummy.root.attach(particle)
        dummy.lightningEffect = particle
        particle.force()

    def release(self):
        if self.dummy:
            self.dummy.visible = False
        BigWorld.callback(1.0, self.detach)

    def detach(self):
        if self.dummy:
            if self.dummy.lightningEffect and self.dummy.lightningEffect.attached:
                self.dummy.root.detach(self.dummy.lightningEffect)
            gDummyModelMgr.giveBack(self.dummy, True)
            self.dummy = None

    def distExceedCallback(self):
        self.release()


class NodeEffectConnector(object):

    def __init__(self, lv, node1, fxFilename, node2, maxLength = 50, priority = 7):
        self.dummy = None
        if not node1 or not node2:
            return
        try:
            fxFilename = getPath(fxFilename)
            particle = clientUtils.pixieFetch(fxFilename, lv)
        except:
            gamelog.error('can not create particle', fxFilename)
            return

        conn = BigWorld.PyConnector()
        conn.target = node2
        conn.length = 15
        conn.maxLength = maxLength
        conn.distExceedCallback = self.distExceedCallback
        dummy = clientUtils.model(gameglobal.SFX_DUMMY_MODEL)
        dummy.dummyModel = True
        dummy.conn = conn
        node1.attach(dummy)
        self.dummy = dummy
        self.node1 = node1
        particle.setAttachMode(0, 0, 0)
        dummy.root.attach(particle)
        dummy.lightningEffect = particle
        particle.force()

    def release(self):
        if self.dummy:
            self.dummy.visible = False
        BigWorld.callback(1.0, self.detach)

    def detach(self):
        if self.dummy:
            if self.dummy.lightningEffect and self.dummy.lightningEffect in self.dummy.root.attachments:
                self.dummy.root.detach(self.dummy.lightningEffect)
            if self.node1 and self.dummy in self.node1.attachments:
                self.node1.detach(self.dummy)
            self.dummy = None

    def distExceedCallback(self):
        self.release()


class CachedNodeEffectConnector(NodeEffectConnector):

    def __init__(self, lv, node1, particle, node2, maxLength = 50, priority = 7):
        self.dummy = None
        if not node1 or not node2:
            return
        conn = BigWorld.PyConnector()
        conn.target = node2
        conn.length = 15
        conn.maxLength = maxLength
        conn.distExceedCallback = self.distExceedCallback
        dummy = clientUtils.model(gameglobal.SFX_DUMMY_MODEL)
        dummy.dummyModel = True
        dummy.conn = conn
        node1.attach(dummy)
        self.dummy = dummy
        self.node1 = node1
        particle.clear()
        particle.setAttachMode(0, 0, 0)
        dummy.root.attach(particle)
        dummy.lightningEffect = particle
        particle.force()

    def release(self):
        if self.dummy:
            self.dummy.visible = False
        self.detach()


class Navigation(object):

    def __init__(self, effectId = None):
        self.model = clientUtils.model(gameglobal.SFX_DUMMY_MODEL)
        self.model.dummyModel = True
        BigWorld.player().addModel(self.model)
        if not effectId:
            effectId = SYSCD.data.get('sfxNavigationCircle', gameglobal.SFX_NAVIGATION_CIRCLE)
        try:
            self.fx = clientUtils.pixieFetch(getPath(effectId))
            self.fx.setAttachMode(0, 1, 0)
            self._loaded = True
        except:
            gamelog.error('Can not find %s' % getPath(effectId))
            self._loaded = False

        self.isShowingEffect = False
        self.updateFlag = True

    def start(self, pos, collideWater, vehicleID = 0, needUpdate = False):
        if not self._loaded:
            return
        self.updateFlag = True
        if collideWater:
            self.model.position = pos + Math.Vector3(0, 0.1, 0)
        else:
            self.model.position = pos
        if not self.isShowingEffect:
            self.fx.enableTerrainTouch(not collideWater and not vehicleID)
            self.fx.force()
            self.model.root.attach(self.fx)
            self.isShowingEffect = True
            if vehicleID:
                en = BigWorld.entity(vehicleID)
                if not en:
                    return
                mat = Math.Matrix(en.model.matrix)
                mat.invert()
                localPos = mat.applyPoint(pos)
                mat.setTranslate(localPos)
                mprod = Math.MatrixProduct()
                mprod.a = mat
                mprod.b = en.model.matrix
                motor = BigWorld.Follow()
                motor.hardAttach = True
                motor.target = mprod
                self.model.addMotor(motor)
        if needUpdate:
            self.updateEffect()

    def updateEffect(self):
        p = BigWorld.player()
        if self.isShowingEffect and self.updateFlag:
            p.ap.updateMousePosition()
            BigWorld.callback(0.01, self.updateEffect)

    def stopUpdateEffect(self):
        self.updateFlag = False

    def stop(self):
        if not self._loaded:
            return
        self.updateFlag = True
        if self.isShowingEffect:
            self.model.root.detach(self.fx)
            self.fx.clear()
            self.isShowingEffect = False
            if len(self.model.motors):
                self.model.motors = ()


class GroupMapMarkCircle(object):

    def __init__(self, effectId = 2581):
        self.model = clientUtils.model(gameglobal.SFX_DUMMY_MODEL)
        self.model.dummyModel = True
        BigWorld.player().addModel(self.model)
        if not effectId:
            effectId = SYSCD.data.get('sfxNavigationCircle', gameglobal.SFX_NAVIGATION_CIRCLE)
        try:
            self.fx = clientUtils.pixieFetch(getPath(effectId))
            self.fx.setAttachMode(0, 1, 0)
            self._loaded = True
        except:
            gamelog.error('Can not find %s' % getPath(effectId))
            self._loaded = False

        self.isShowingEffect = False
        self.updateFlag = True

    def start(self, pos, collideWater, vehicleID = 0, needUpdate = False):
        if not self._loaded:
            return
        self.updateFlag = True
        if collideWater:
            self.model.position = pos + Math.Vector3(0, 0.1, 0)
        else:
            self.model.position = pos
        if not self.isShowingEffect:
            self.fx.enableTerrainTouch(not collideWater and not vehicleID)
            self.fx.force()
            self.model.root.attach(self.fx)
            self.isShowingEffect = True
            if vehicleID:
                en = BigWorld.entity(vehicleID)
                if not en:
                    return
                mat = Math.Matrix(en.model.matrix)
                mat.invert()
                localPos = mat.applyPoint(pos)
                mat.setTranslate(localPos)
                mprod = Math.MatrixProduct()
                mprod.a = mat
                mprod.b = en.model.matrix
                motor = BigWorld.Follow()
                motor.hardAttach = True
                motor.target = mprod
                self.model.addMotor(motor)
        if needUpdate:
            self.updateEffect()

    def isInGroupMapMarkStatus(self):
        return self.isShowingEffect

    def updateEffect(self):
        p = BigWorld.player()
        if self.isShowingEffect and self.updateFlag:
            p.ap.mapMarkingPosition()
            BigWorld.callback(0.01, self.updateEffect)

    def isSamePosition(self, pos):
        groupMarkMapIndex = 0
        gamelog.debug('@hjx marking#isSamePosition0:', pos)
        for key, val in BigWorld.player().groupMapMark.items():
            gamelog.debug('@hjx marking#isSamePosition1:', val['pos'])
            if val['pos'] == pos:
                groupMarkMapIndex = key
                break

        return groupMarkMapIndex

    def markMapDone(self, pos):
        p = BigWorld.player()
        self.stopUpdateEffect()
        self.stop()
        gamelog.debug('@hjx marking#markMapDone0:', pos)
        if pos is None:
            p.chatToGm('场景标记失败！')
            return
        for h in (0.5, 1.0):
            if BigWorld.collide(p.spaceID, p.position + Math.Vector3(0, h * 2, 0), pos + Math.Vector3(0, h * 2, 0), gameglobal.TREEMATTERKINDS):
                return

        oldMarkMapIndex = self.isSamePosition(pos)
        if oldMarkMapIndex:
            gameglobal.rds.ui.messageBox.showYesNoMsgBox('\n是否覆盖前一场景标记', Functor(self.onRealConfirm, oldMarkMapIndex, pos))
            return
        self._realDoMarkMap(pos)

    def onRealConfirm(self, oldMarkMapIndex, pos):
        p = BigWorld.player()
        p.cell.markMap(oldMarkMapIndex, 0, 0, 0, 0.0, 0, 0, '')
        self._realDoMarkMap(pos)

    def _realDoMarkMap(self, pos):
        p = BigWorld.player()
        groupMarkMapEffects = SYSCD.data.get('groupMarkMapEffects', [])
        markMapIndex = gameglobal.rds.ui.group.markMapIndex
        xPos, yPos, zPos = pos
        chunkName = BigWorld.ChunkInfoAt(pos)
        p.cell.markMap(markMapIndex, xPos, yPos, zPos, 1.0, groupMarkMapEffects[markMapIndex - 1], p.spaceNo, chunkName)

    def stopUpdateEffect(self):
        self.updateFlag = False

    def stop(self):
        if ui.get_cursor_state() == ui.MARK_MAP_STATE:
            ui.reset_cursor()
        if not self._loaded:
            return
        self.updateFlag = True
        if self.isShowingEffect:
            self.model.root.detach(self.fx)
            self.fx.clear()
            self.isShowingEffect = False
            if len(self.model.motors):
                self.model.motors = ()


class FlyToNodeEx(Flyer):

    def __init__(self, model, approachCallback = None):
        self.model = model
        self.callback = approachCallback

    def start(self, startPos, targetNode, curvature = 0, zroll = 0, speed = 30, rotateSpeed = 30):
        if not self.model.inWorld:
            if self.callback:
                BigWorld.callback(0.001, self.callback)
            self.model = None
            return
        self.model.position = startPos
        mot = BigWorld.Rlauncher()
        self.model.addMotor(mot)
        mot.target = targetNode
        mot.rotateSpeed = Math.Vector3(0, rotateSpeed, 0)
        mot.speed = speed
        mot.zroll = zroll
        mot.curvature = curvature
        mot.proximityCallback = Functor(self.approach, targetNode)
        mot.proximity = 0.2
        self.mot = mot

    def approach(self, targetNode):
        self.model.delMotor(self.mot)
        if self.callback != None:
            self.callback()
        self.model = None
        self.mot = None


def testAttach(fxPath = 'effect/char/combat/170131.xml'):
    fx = clientUtils.pixieFetch(fxPath, 3)
    fx.overCallback(Functor(testgiveBack, fx, fxPath), 10)
    BigWorld.player().model.node('Scene Root').attach(fx)


def testgiveBack(effect, fxPath):
    node = BigWorld.player().model.node('Scene Root')
    if effect in node.attachments:
        print 'testgiveBack:', fxPath
        node.detach(effect)
        effect.clear()
        effect.scale(1)
        effect.bias = (0, 0, 0)


class FlyNodeCurve(FlyToNode):

    def approach(self):
        p = BigWorld.player()
        self.model.motors = []
        self.mot = None
        for ef in self.effects:
            ef.delayGiveBack = True
            ef.stop()

        self.effects = []
        p.delModel(self.model)
        if self.callback:
            self.callback(self)


class FlyCurve(object):
    FLYER_MAX_NUM = 50

    def __init__(self):
        self.flyers = []
        self.callbackHandle = None
        self.interval = 0.1
        self.isStart = False

    def setInterval(self, delta):
        self.interval = delta

    def start(self, startPos, targetPos, speed, curvature = 0.3, flyEff = []):
        self.isStart = True
        self._start(startPos, targetPos, speed, curvature, flyEff)

    def _start(self, startPos, targetPos, speed, curvature = 0.3, flyEff = []):
        if not self.isStart:
            return
        m = Math.Matrix()
        m.setTranslate(targetPos)
        if not self.flyers:
            flyer = FlyNodeCurve()
            flyer.setCallback(self.approach)
            flyer.start(startPos, m, curvature, 0, speed)
            flyer.addFlyEffect(flyEff)
        else:
            flyer = self.flyers.pop(0)
            p = BigWorld.player()
            p.addModel(flyer.model)
            flyer.model.position = startPos
            mot = BigWorld.Rlauncher()
            flyer.model.addMotor(mot)
            flyer.mot = mot
            mot.speed = speed
            mot.target = m
            mot.curvature = curvature
            mot.proximityCallback = flyer.approach
            flyer.addFlyEffect(flyEff)
        if self.callbackHandle:
            BigWorld.cancelCallback(self.callbackHandle)
            self.callbackHandle = None
        self.callbackHandle = BigWorld.callback(self.interval, Functor(self._start, startPos, targetPos, speed, curvature, flyEff))

    def stop(self):
        self.isStart = False

    def approach(self, flyer):
        self.flyers.append(flyer)

    def release(self):
        self.isStart = False
        for flyer in self.flyers:
            flyer.release()

        self.flyers = []


def getHitPercent():
    if EFFECT_HIT_CNT:
        return EFFECT_HIT_CNT * 1.0 / EFFECT_GET_CNT
    else:
        return 0
