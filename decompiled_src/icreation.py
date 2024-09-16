#Embedded file name: /WORKSPACE/data/entities/client/icreation.o
import random
import BigWorld
import Math
import gametypes
import const
import gamelog
import gameglobal
import utils
import combatUtils
import clientcom
import formula
from callbackHelper import Functor
from helpers import fashion
from helpers import modelServer
from helpers import ufo
from iCombatUnit import ICombatUnit
from sfx import sfx
from gameclass import SimpleCreationInfo
from guis import uiConst
from data import creation_client_data as CCD
from data import duel_config_data as DCD
DUMMY_MODEL_ID = 39999

class ICreation(ICombatUnit):
    IsCreation = True
    CRETIONT_LOADDIST = 35.0
    CREATION_INCLANWAR_LOADDIST = 10.0

    def __init__(self):
        super(ICreation, self).__init__()
        self.initing = True
        self.magicEffect = None
        self.effects = []
        self.effectConnector = []
        self.keepEffects = []
        self.disabled = False
        self.shakeCameraCB = []
        self.obstacleModel = None
        self.ownerByPlayer = False
        self.clientCalcCB = 0
        self.calcOnceForSingleTgt = False
        self.isMagicField = True
        self.calcEntities = []
        self.creationInfo = None
        self.trapId = DCD.data.get('hunt_trap_id', 0)
        self.data = {}
        enableMFClientCalc = gameglobal.rds.configData.get('enableMFClientCalc', False)
        if enableMFClientCalc:
            self.enableClientActived()
        if self.activateProp and self.activateProp[0]:
            self.set_activateProp(self.activateProp)
        if self.disableCreation:
            self.set_disableCreation(False)
        if self.enableClientIntervalEffect:
            self.set_enableClientIntervalEffect(False)

    def prerequisites(self):
        return []

    def getOwnerOpacityValue(self):
        opValues = None
        if hasattr(self, 'ownerId'):
            owner = BigWorld.entity(self.ownerId)
            if owner and owner.inWorld:
                opValues = owner.getOpacityValue()
        return opValues

    def enterWorld(self):
        ownerId = getattr(self, 'ownerId', 0)
        p = BigWorld.player()
        self.initing = False
        self.initCreationData()
        opValues = self.getOwnerOpacityValue()
        if opValues and opValues[0] == gameglobal.OPACITY_HIDE_INCLUDE_ATTACK:
            return
        super(ICreation, self).enterWorld()
        self.fashion = fashion.Fashion(self.id)
        self.model.noAttachFx_ = False
        if self.needToLoad():
            if getattr(self, 'modelServer', None):
                self.modelServer.release()
                self.modelServer = None
            self.modelServer = modelServer.SimpleModelServer(self, self.isUrgentLoad())
        data = self.data
        shakeCameras = data.get('shakeCameras', ())
        cbs = sfx.playShakeCamera(shakeCameras, self.id)
        self.shakeCameraCB.extend(cbs)
        if formula.inHuntBattleField(p.mapID):
            if self.cid == self.trapId and ownerId == p.id:
                gameglobal.rds.ui.littleMap.addBFHuntIcon(uiConst.ICON_TYPE_HUNT_TRAP, p.gbId, None, self.position, 'setTrap')
        if self.data.get('showBuffId', 0):
            p = BigWorld.player()
            if p and getattr(p, 'creationVisibleByBuff', None):
                p.creationVisibleByBuff.setdefault(self.data['showBuffId'], []).append(self.id)

    def set_enableClientIntervalEffect(self, old):
        ccInfo = self._getCreationInfo()
        if not ccInfo:
            return
        ttl = ccInfo.getCombatCreationData('ttl', 0)
        interval = ccInfo.getCombatCreationData('interval', 0)
        count = min(int(ttl / interval), 30) if interval > 0 else 1
        for i in xrange(count):
            BigWorld.callback(i * interval, Functor(self.playTriggerEffect, self.id))

    def needToLoad(self):
        p = BigWorld.player()
        if not p:
            return False
        data = self.data
        needToLoad = data.get('needToLoad', False)
        dist = p.position.distTo(self.position)
        if needToLoad:
            return True
        if p.inClanWar or p.inWorldWarEx():
            if dist < self.CREATION_INCLANWAR_LOADDIST:
                return True
            else:
                return False
        else:
            if dist < self.CRETIONT_LOADDIST:
                return True
            return False

    def isUrgentLoad(self):
        p = BigWorld.player()
        data = self.data
        isUrgentLoad = data.get('isUrgentLoad', False)
        if p and not clientcom.needDoOptimize() and isUrgentLoad:
            return True
        return False

    def getEffectPriority(self):
        ownerId = getattr(self, 'ownerId', 0)
        if ownerId:
            ownEnt = BigWorld.entities.get(ownerId)
            if ownEnt and ownEnt.inWorld:
                return ownEnt.getSkillEffectPriority()
        return self.getSkillEffectPriority()

    def set_activateProp(self, old):
        self.activate(self.activateProp[0])

    def leaveWorld(self):
        if self.obstacleModel:
            self.delModel(self.obstacleModel)
            self.obstacleModel = None
        keepModel = self.model
        if self.model != None:
            self.model = None
        if not self.disabled:
            self.releaseKeepEffect()
        super(ICreation, self).leaveWorld()
        BigWorld.callback(1, Functor(self.__delayReleaseEffects, keepModel, self.effects))
        if getattr(self, 'checkVisibleHandler', None):
            BigWorld.cancelCallback(self.checkVisibleHandler)
            self.checkVisibleHandler = None
        if self.data.get('showBuffId', 0):
            if self.id in BigWorld.player().creationVisibleByBuff.get(self.data['showBuffId'], []):
                BigWorld.player().creationVisibleByBuff.setdefault(self.data['showBuffId'], []).remove(self.id)

    def showStopEff(self, yaw):
        p = BigWorld.player()
        opValues = self.getOwnerOpacityValue()
        if opValues and opValues[0] in (gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, gameglobal.OPACITY_HIDE):
            return
        stopEff = self.__getStopEffect()
        stopEffScale = self.__getEffectScale(gametypes.SKILL_CLIENT_ARG_CREATION_STOP)
        if stopEff:
            for effId in stopEff:
                priority = self.getEffectPriority()
                if self.ownerByPlayer:
                    self.model.hostId = p.id
                res = sfx.attachEffect(gameglobal.ATTACH_EFFECT_INPOS, (self.getSkillEffectLv(),
                 priority,
                 None,
                 effId,
                 sfx.EFFECT_LIMIT_MISC,
                 self.position,
                 0,
                 yaw,
                 0,
                 gameglobal.EFFECT_LAST_TIME))
                if res:
                    for r in res:
                        if r:
                            r.scale(stopEffScale)

    def set_disableCreation(self, old):
        if self.disableCreation:
            self.disabledCreation()

    def disabledCreation(self):
        self.disabled = True
        delayTime = self.data.get('keepEffectDelayTime', 0)
        BigWorld.callback(delayTime, Functor(self.releaseEffect, self.keepEffects))
        self.showStopEff(self.yaw)
        for cb in self.shakeCameraCB:
            if cb:
                BigWorld.cancelCallback(cb)

        self.shakeCameraCB = []

    def releaseEffect(self, effects):
        if effects:
            for i in effects:
                i.stop()

            effects = None

    def releaseKeepEffect(self):
        for i in self.keepEffects:
            i.stop()

        self.keepEffects = []

    def __delayReleaseEffects(self, keepModel, effects):
        for i in effects:
            i.stop()

        effects = []

    def enterTopLogoRange(self, rangeDist = -1):
        uishow = self.data.get('uishow', False)
        if not uishow:
            return
        super(ICreation, self).enterTopLogoRange(rangeDist)
        self.refreshTopLogo()

    def leaveTopLogoRange(self, rangeDist = -1):
        super(ICreation, self).leaveTopLogoRange(rangeDist)

    def getItemData(self):
        self.fid = self.data.get('sid', None)
        modelId = self.data.get('modelId', None)
        return {'model': modelId,
         'dye': 'Default',
         'modelShow': 1}

    def getOpacityValue(self):
        p = BigWorld.player()
        ownerId = getattr(self, 'ownerId', 0)
        owner = BigWorld.entities.get(ownerId, None)
        if owner and hasattr(owner, 'getOpacityValue'):
            if owner.getOpacityValue()[0] == gameglobal.OPACITY_HIDE_INCLUDE_ATTACK:
                return (gameglobal.OPACITY_HIDE, True)
        if self.data.get('showBuffId', 0):
            if p.hasState(self.data['showBuffId']):
                return (gameglobal.OPACITY_FULL, True)
            else:
                return (gameglobal.OPACITY_HIDE, True)
        if self.visiType == 1:
            if ownerId != BigWorld.player().id:
                return (gameglobal.OPACITY_HIDE, True)
        elif self.visiType == 2:
            if p.isEnemy(owner):
                return (gameglobal.OPACITY_HIDE, True)
        elif self.visiType == 3:
            if not p.isEnemy(owner):
                return (gameglobal.OPACITY_HIDE, True)
        elif self.visiType == 4:
            if not self.isOwnerOrSameGroup(p):
                return (gameglobal.OPACITY_HIDE, True)
        return (gameglobal.OPACITY_FULL, True)

    def getStartAct(self):
        if not self.data:
            return []
        actList = []
        startActData = self.data.get('startAct', None)
        if startActData:
            startActData = list(startActData)
            startActData.pop(0)
            actList.append(random.choice(startActData))
        keepActData = self.data.get('keepAct', None)
        if keepActData:
            keepActData = list(keepActData)
            keepActData.pop(0)
            actList.append(random.choice(keepActData))
        return actList

    def afterModelFinish(self):
        p = BigWorld.player()
        if not self.inWorld:
            return
        self.refreshOpacityState()
        modelScale = self.data.get('modelScale', 1.0)
        if modelScale != 1.0:
            self.model.scale = (modelScale, modelScale, modelScale)
        canSelect = self.data.get('canSelect', False)
        self.setTargetCapsUse(canSelect)
        self.fashion.attachUFO(ufo.UFO_NULL)
        if self.data.get('creationNoDrop', False):
            self.filter = BigWorld.AvatarFilter()
            self.filter.applyEntityPitch = True
        else:
            self.filter = BigWorld.AvatarDropFilter()
            self.filter.popDist = 5.0
        startActNames = self.getStartAct()
        self.fashion.playActionSequence(self.model, startActNames, None)
        self.createObstacleModel()
        self.ownerByPlayer = self.isOwnedByPlayer()
        keepEffect = self.__getKeepEffect()
        keepEffectScale = self.__getEffectScale(gametypes.SKILL_CLIENT_ARG_CREATION_KEEP)
        creationInfo = self._getCreationInfo()
        ttl = creationInfo.getCombatCreationData('ttl', 0)
        if not ttl:
            ttl = self.data.get('ttl', 0)
        if ttl > 0:
            ttl = ttl + gameglobal.EFFECT_LAST_TIME
        if keepEffect and not self.disabled:
            for i in keepEffect:
                priority = self.getEffectPriority()
                if self.ownerByPlayer:
                    self.model.hostId = p.id
                res = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getSkillEffectLv(),
                 priority,
                 self.model,
                 i,
                 sfx.EFFECT_UNLIMIT if self.ownerByPlayer else sfx.EFFECT_LIMIT_MISC,
                 ttl))
                if res:
                    for e in res:
                        if e:
                            e.scale(keepEffectScale)

                    self.keepEffects += res

        effect = self.__getMagicEffect()
        effectScale = self.__getEffectScale(gametypes.SKILL_CLIENT_ARG_CREATION_START)
        if effect:
            roll = 0
            pitch = 0
            for i in effect:
                priority = self.getEffectPriority()
                res = sfx.attachEffect(gameglobal.ATTACH_EFFECT_INPOS, (self.getSkillEffectLv(),
                 priority,
                 None,
                 i,
                 sfx.EFFECT_UNLIMIT if self.ownerByPlayer else sfx.EFFECT_LIMIT,
                 self.position,
                 roll,
                 self.yaw,
                 pitch,
                 ttl))
                if res:
                    for r in res:
                        if r:
                            r.scale(effectScale)

        self.playConnectEffect()
        if self.visiType == 4:
            self.checkVisibleHandler = BigWorld.callback(1, self.__checkVisible)
        if not self.topLogo:
            self.enterTopLogoRange()
        else:
            self.resetTopLogo()

    def createObstacleModel(self):
        data = self.data
        modelId = data.get('obstacleModel', 0)
        if modelId:
            modelName = 'char/%d/%d.model' % (modelId, modelId)
            scaleMatrix = Math.Matrix()
            scaleMatrix.setScale((1, 1, 1))
            mp = Math.MatrixProduct()
            mp.a = scaleMatrix
            mp.b = self.matrix
            BigWorld.fetchObstacleModel(modelName, mp, True, self._onLoadObstacleModel)

    def _onLoadObstacleModel(self, model):
        if model:
            model.setCollide(True)
            model.setPicker(True)
            self.obstacleModel = model
            self.addModel(model)
            self.checkCollideWithPlayer()

    def __checkVisible(self):
        p = BigWorld.player()
        isVisible = self.isOwnerOrSameGroup(p)
        if hasattr(self, 'isVisible') and isVisible != self.isVisible:
            self.isVisible = isVisible
            self.hide(not isVisible)
        self.checkVisibleHandler = BigWorld.callback(1, self.__checkVisible)

    def hide(self, needHide, retainTopLogo = False):
        if self.fashion:
            self.fashion.hide(needHide)
        canSelect = self.data.get('canSelect', False)
        self.setTargetCapsUse(canSelect)
        if not needHide:
            self.refreshTopLogo()

    def refreshTopLogo(self):
        if not self.topLogo:
            return
        self.resetTopLogo()

    def getTopLogoHeight(self):
        if not self.model:
            return 0.0
        elif self.data != None:
            height = self.data.get('topLogoHeight', self.model.height)
            return height * self.model.scale[1] + 0.2
        else:
            return self.model.height * self.model.scale[1] + 0.2

    def __getKeepEffect(self):
        return self.__getEffect('keepEffect')

    def __getMagicEffect(self):
        return self.__getEffect('startEffect')

    def __getStopEffect(self):
        if self.stopType == const.CREATION_STOP_TYPE_QTE and self.data.has_key('qteStopEffect'):
            return [self.data.get('qteStopEffect')]
        return self.__getEffect('stopEffect')

    def __getPreTriggerEffect(self):
        return self.__getEffect('preTriggerEffect')

    def __getEffect(self, key):
        if not key:
            return
        effectData = self.data.get(key, None)
        if effectData:
            effectData = list(effectData)
            num = effectData.pop(0)
            if num == 0:
                return [random.choice(effectData)]
            else:
                return effectData
        else:
            return

    def __getEffectScale(self, stage):
        if not hasattr(self, 'ownerId'):
            return 1.0
        owner = BigWorld.entities.get(self.ownerId)
        if not hasattr(owner, 'skillClientArgs'):
            return 1.0
        skillId = CCD.data.get(self.cid, {}).get('sid', -1)
        if skillId not in owner.skillClientArgs or stage not in owner.skillClientArgs[skillId]:
            return 1.0
        return max(0.0, owner.skillClientArgs[skillId][stage] + 1.0)

    def needBlackShadow(self):
        return False

    def activate(self, entId):
        self.playTriggerEffect(entId)

    def playTriggerEffect(self, entId):
        p = BigWorld.player()
        ent = BigWorld.entities.get(entId)
        if not ent or not ent.inWorld:
            return
        if not self.inWorld and not getattr(self, 'initing', False):
            return
        if self.getOpacityValue()[0] in (gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, gameglobal.OPACITY_HIDE):
            return
        self._releaseEffects()
        effects = self.data.get('triggerEffect', None)
        if effects:
            for i in effects:
                priority = self.getEffectPriority()
                if self.ownerByPlayer:
                    ent.model.hostId = p.id
                    ent.model.creationId = self.id
                ef = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getSkillEffectLv(),
                 priority,
                 ent.model,
                 i,
                 sfx.EFFECT_UNLIMIT if self.ownerByPlayer else sfx.EFFECT_LIMIT))
                if ef:
                    self.effects += ef

        triggerActs = self.data.get('triggerAct', None)
        if triggerActs:
            triggerActs = list(triggerActs)
            triggerActs.pop(0)
            triggerAct = random.choice(triggerActs)
            if triggerAct in ent.fashion.getActionNameList():
                ent.model.action(triggerAct)()

    def enableClientActived(self):
        if not self.isOwnedByPlayer():
            return
        ccInfo = self._getCreationInfo()
        ctype = ccInfo.getCombatCreationData('type')
        if ctype != gametypes.CREATION_TYPE_MAGIC_FIELD:
            return
        trigRule = ccInfo.getCombatCreationData('trigRule', 0)
        if trigRule in (gametypes.COMBATCREATION_TRAP_TGT_TYPE_LOCK_TARGET,):
            return
        interval = ccInfo.getCombatCreationData('interval', 0)
        if not interval:
            return
        if BigWorld.player().isInBfDota() and gameglobal.rds.configData.get('enableBFDotaCreationServerCalc', False):
            return
        delayTime = ccInfo.getCombatCreationData('delayTime', 0) + ccInfo.getCombatCreationData('bornTime', 0)
        if delayTime > 0:
            BigWorld.callback(delayTime, self.realEnableClientActived)
        else:
            self.realEnableClientActived()

    def realEnableClientActived(self):
        ccInfo = self._getCreationInfo()
        if not ccInfo:
            return
        self.tickCnt = 1
        ttl = ccInfo.getCombatCreationData('ttl', 0)
        interval = ccInfo.getCombatCreationData('interval', 0)
        delayTime = ccInfo.getCombatCreationData('delayTime', 0) + ccInfo.getCombatCreationData('bornTime', 0)
        count = min(int((ttl - delayTime) / interval + 1), 65535)
        for i in xrange(count):
            BigWorld.callback(i * interval, Functor(self.clientCalc, i))

    def _getCreationInfo(self):
        if self.isOwnedByPlayer():
            if not self.creationInfo:
                info = BigWorld.player().getCombatCreationInfo(self.cid, self.clv, self.skillId)
                self.creationInfo = info
            return self.creationInfo
        elif hasattr(self, 'cid'):
            return SimpleCreationInfo(self.cid)
        else:
            return None

    def clientCalc(self, count):
        if not hasattr(self, 'clientCalcCB'):
            return
        if not self.inWorld:
            return
        if self.clientCalcCB:
            BigWorld.cancelCallback(self.clientCalcCB)
        p = BigWorld.player()
        ccInfo = self._getCreationInfo()
        effectDict = combatUtils.calcCombatCreatorEffectEx(p, self, ccInfo, self, self.tickCnt, self.skillId)
        gamelog.debug('m.l@iCreaion.clientCalc effectDict:', effectDict)
        strValue = utils.getStrFromEffectDict(effectDict)
        BigWorld.player().cell.activedByClient(self.id, strValue)
        self.tickCnt = self.tickCnt + 1

    def isEnemy(self, target):
        if target == None:
            return False
        owner = BigWorld.entities.get(getattr(self, 'ownerId', 0))
        if owner:
            return owner.isEnemy(target)
        return False

    def _mlSpaceForceWithMonster(self, tgt):
        return tgt.IsAvatar and tgt._isInBianyao() or tgt.IsMonster

    def isOwnedByPlayer(self):
        ownerId = getattr(self, 'ownerId', 0)
        p = BigWorld.player()
        if not ownerId or p == None:
            return False
        if ownerId == p.id:
            return True
        return False

    def isOwnerOrSameGroup(self, target):
        ownerId = getattr(self, 'ownerId', 0)
        if not ownerId:
            return False
        if ownerId == target.id:
            return True
        ent = BigWorld.entities.get(ownerId)
        if not ent or not ent.IsAvatar or not target.IsAvatar:
            return False
        if target.isQieCuoWith(ownerId):
            return False
        return ent.groupNUID != 0 and ent.groupNUID == target.groupNUID

    def _releaseEffects(self):
        if hasattr(self, 'effects'):
            for i in self.effects:
                i.stop()

            self.effects = []

    def onTargetCursor(self, enter):
        super(ICreation, self).onTargetCursor(enter)

    def playQteEffect(self):
        if not self.inWorld:
            return
        if self.getOpacityValue()[0] in (gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, gameglobal.OPACITY_HIDE):
            return
        effect = self.data.get('qteEffect', None)
        if effect:
            priority = self.getEffectPriority()
            sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getSkillEffectLv(),
             priority,
             self.model,
             effect,
             sfx.EFFECT_LIMIT_MISC,
             gameglobal.EFFECT_LAST_TIME))

    def playPreTriggerEffect(self):
        opValues = self.getOwnerOpacityValue()
        if opValues and opValues[0] == gameglobal.OPACITY_HIDE_INCLUDE_ATTACK:
            return
        p = BigWorld.player()
        effect = self.__getPreTriggerEffect()
        if effect:
            for i in effect:
                priority = self.getEffectPriority()
                if self.ownerByPlayer:
                    self.model.hostId = p.id
                sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (self.getSkillEffectLv(),
                 priority,
                 self.model,
                 i,
                 sfx.EFFECT_UNLIMIT if self.ownerByPlayer else sfx.EFFECT_LIMIT))

    def playConnectEffect(self):
        self.releaseConnectEffects()
        startNodeName = self.data.get('connEffStartNode', '')
        endNodeName = self.data.get('connEffEndNode', '')
        connEffs = self.data.get('connEffs', [])
        if not connEffs:
            return
        if not hasattr(self, 'ownerId'):
            return
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        startNode = self.model.node(startNodeName)
        endNode = owner.model.node(endNodeName)
        if startNode and endNode:
            for ef in connEffs:
                effect = sfx.attachEffect(gameglobal.ATTACH_EFFECT_CONNECTOR, (owner.getSkillEffectLv(),
                 startNode,
                 ef,
                 endNode,
                 50,
                 owner.getSkillEffectPriority()))
                self.effectConnector.append(effect)

    def releaseConnectEffects(self):
        for ec in self.effectConnector:
            if ec:
                ec.detach()

    def getEffectLv(self):
        if utils.instanceof(BigWorld.player(), 'PlayerAvatar'):
            if hasattr(self, 'ownerId') and BigWorld.entity(self.ownerId):
                if not getattr(BigWorld.entity(self.ownerId), 'fashion', None):
                    return gameglobal.EFFECT_CLOSE
                return BigWorld.entity(self.ownerId).getEffectLv()
            else:
                return getattr(BigWorld.player(), 'monsterEffectLv', gameglobal.EFFECT_MID)
        else:
            return gameglobal.EFFECT_MID

    def getSkillEffectLv(self):
        lv = super(ICreation, self).getSkillEffectLv()
        ownerId = getattr(self, 'ownerId', 0)
        if not ownerId:
            return lv
        owner = BigWorld.entity(ownerId)
        if owner and owner.__class__.__name__ == 'Avatar':
            lv = self.getClanWarEffectLv(lv)
        return lv

    def getBeHitEffectLv(self):
        lv = super(ICreation, self).getBeHitEffectLv()
        ownerId = getattr(self, 'ownerId', 0)
        if not ownerId:
            return lv
        owner = BigWorld.entity(ownerId)
        if owner and owner.__class__.__name__ == 'Avatar':
            lv = self.getClanWarEffectLv(lv)
        return lv

    def getBuffEffectLv(self):
        lv = super(ICreation, self).getBuffEffectLv()
        ownerId = getattr(self, 'ownerId', 0)
        if not ownerId:
            return lv
        owner = BigWorld.entity(ownerId)
        if owner and owner.__class__.__name__ == 'Avatar':
            lv = self.getClanWarEffectLv(lv)
        return lv

    def getEquipEffectLv(self):
        lv = super(ICreation, self).getEquipEffectLv()
        ownerId = getattr(self, 'ownerId', 0)
        if not ownerId:
            return lv
        owner = BigWorld.entity(ownerId)
        if owner and owner.__class__.__name__ == 'Avatar':
            lv = self.getClanWarEffectLv(lv)
        return lv

    def getBasicEffectLv(self):
        lv = super(ICreation, self).getBasicEffectLv()
        ownerId = getattr(self, 'ownerId', 0)
        if not ownerId:
            return lv
        owner = BigWorld.entity(ownerId)
        if owner and owner.__class__.__name__ == 'Avatar':
            lv = self.getClanWarEffectLv(lv)
        return lv

    def needSetStaticStates(self):
        return False

    def initCreationData(self):
        ownerId = getattr(self, 'ownerId', 0)
        owner = BigWorld.entities.get(ownerId)
        if owner and hasattr(owner, 'skillAppearancesDetail'):
            self.data = owner.skillAppearancesDetail.getCreationAppearanceData(self.cid)
        else:
            self.data = CCD.data.get(self.cid, {})
