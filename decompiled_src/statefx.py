#Embedded file name: /WORKSPACE/data/entities/client/sfx/statefx.o
import time
import random
import BigWorld
import Math
import math
import utils
import gametypes
import gameglobal
import keys
import sfx
import const
import screenEffect
import skillDataInfo
import gamelog
import clientcom
import cameraEffect
from callbackHelper import Functor
from helpers import attachedModel
from helpers import tintalt, modelServer
from helpers import action
from helpers import weaponModel
from helpers import action as ACT
from helpers import charRes
from data import state_data as SD
from data import monster_model_client_data as MMCD
from data import zaiju_data as ZJD
from data import state_client_data as SCD
from data import sys_config_data as SYSCD
from data import simple_qte_data as SQD

class EffectMgr(object):

    def __init__(self, ownerId):
        self.ownerId = ownerId
        self.effect = {}
        self.fxMap = {}
        self.startFxMap = {}
        self.enterFuncMap = EnterStateMap
        self.leaveFuncMap = LeaveStateMap
        self.refreshing = False
        self.actTime = 0.0
        self.actStopCallBack = {}
        self.actLoopCallBack = {}
        self.stateActMap = {}
        self.stateStartTimeMap = {}
        self.forceUpdate = False
        self.motor = None
        self.mf = None
        self.tintStateMap = {}
        self.oldBoneScale = {}
        self.stateHostMap = {}
        self.effEndTimeDict = {}
        self.effStateDict = {}
        self.playerEffs = {}
        self.enemySideEffs = []
        self.freezedEffs = []
        self.connEffs = []
        self.tempSkillInfo = {}
        self.teamSSCGroupEffectHandle = None
        self.isLeavingWorld = False
        self.attachingStateDataMap = {}

    def release(self, isLeavingWorld = False):
        self.isLeavingWorld = isLeavingWorld
        owner = BigWorld.entity(self.ownerId)
        if self.motor:
            owner.model.delMotor(self.motor)
        self.motor = None
        for i in self.effect.keys():
            self._delState(i)

        self.effect = {}
        if owner and owner.inWorld:
            attachModel = owner.model
            if owner.inRiding() and hasattr(owner.model, 'ride'):
                attachModel = owner.model.ride
            for fxId in self.fxMap.keys():
                sfx.detachEffect(attachModel, fxId, self.fxMap[fxId])

        self.fxMap = {}
        self.startFxMap = {}
        self.enterFuncMap = {}
        self.leaveFuncMap = {}
        self.ownerId = 0
        self.actStopCallBack = {}
        self.actLoopCallBack = {}
        self.stateActMap = {}
        self.stateStartTimeMap = {}
        self.effEndTimeDict = {}
        self.effStateDict = {}
        if self.mf:
            self.mf.release()
        self.freezedEffs = []
        self.teamSSCGroupEffectHandle and BigWorld.cancelCallback(self.teamSSCGroupEffectHandle)
        self.teamSSCGroupEffectHandle = None

    def freezeEffect(self, freezeTime):
        if self.fxMap:
            for fxs in self.fxMap.values():
                if fxs:
                    for fx in fxs:
                        fx.pause(freezeTime)
                        self.freezedEffs.append(fx)

        if self.startFxMap:
            for fxs in self.startFxMap.values():
                if fxs:
                    for fx in fxs:
                        fx.pause(freezeTime)
                        self.freezedEffs.append(fx)

        if self.playerEffs:
            for fxs in self.playerEffs.values():
                if fxs:
                    for fx in fxs:
                        fx.pause(freezeTime)
                        self.freezedEffs.append(fx)

        if self.enemySideEffs:
            for fx in self.enemySideEffs:
                if fx:
                    fx.pause(freezeTime)
                    self.freezedEffs.append(fx)

    def clearFreezeEffect(self):
        if self.freezedEffs:
            for eff in self.freezedEffs:
                if eff:
                    eff.pause(0)

        self.freezedEffs = []

    def refresh(self):
        if self.refreshing:
            return
        self.refreshing = True
        self.refreshing = False

    def updateEffectInCombat(self, inCombat, newstateSet):
        gamelog.debug('-----@updateEffectInCombat', inCombat, newstateSet)
        owner = BigWorld.entity(self.ownerId)
        if owner == None:
            return
        for stateId in newstateSet:
            stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
            if stateData != None:
                showType = self.getStateShowType(stateData)
                if showType == gameglobal.STATE_FX_SHOW_TYPE_IN_COMBAT:
                    if inCombat:
                        gamelog.debug('进入战斗新增特效', stateId)
                        self._addInCombatStateFx(stateData, owner)
                    else:
                        gamelog.debug('脱离战斗删除特效', stateId)
                        self._stopCombatStateFx(stateData)
                        if self.effect.has_key(stateId):
                            self.effect.pop(stateId)
                if showType == gameglobal.STATE_FX_SHOW_TYPE_NOT_IN_COMBAT:
                    if inCombat:
                        gamelog.debug('进入战斗删除特效', stateId)
                        self._stopCombatStateFx(stateData)
                        if self.effect.has_key(stateId):
                            self.effect.pop(stateId)
                    else:
                        gamelog.debug('脱离战斗新增特效', stateId)
                        self._addInCombatStateFx(stateData, owner)

    def getStateShowType(self, stateData):
        return stateData.getSkillData('showType', gameglobal.STATE_FX_SHOW_TYPE_ANY_TIME)

    def updateEffect(self, newStates):
        if self.isLeavingWorld:
            return
        oldStates = set(self.effect.keys())
        addSet = newStates - oldStates
        delSet = oldStates - newStates
        intersectionSet = oldStates & newStates
        forceUpdateSet = set([])
        for stateId in intersectionSet:
            isSumTime = SD.data.get(stateId, {}).get('isSumTime', 0)
            if isSumTime:
                forceUpdateSet.add(stateId)

        gamelog.debug('zf:updateEffect.......', addSet, delSet)
        self.addForceState(addSet, delSet)
        gamelog.debug('zf:updateEffect.......', addSet, delSet)
        map(self._delState, delSet)
        map(self._addState, addSet)
        if forceUpdateSet:
            map(self._delState, forceUpdateSet)
            map(self._addState, forceUpdateSet)
        self.refreshTempSkill()

    def _needAddStateFx(self, stateData, owner):
        showType = self.getStateShowType(stateData)
        if showType == gameglobal.STATE_FX_SHOW_TYPE_ANY_TIME:
            return True
        if showType == gameglobal.STATE_FX_SHOW_TYPE_IN_COMBAT and hasattr(owner, 'inCombat') and owner.inCombat:
            return True
        if showType == gameglobal.STATE_FX_SHOW_TYPE_NOT_IN_COMBAT and hasattr(owner, 'inCombat') and not owner.inCombat:
            return True
        return False

    def _addState(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        if stateData == None or owner == None:
            return
        if self._needAddStateFx(stateData, owner):
            self._addStateFx(stateData, owner)
            self._addEnemySideStateFx(stateData, owner)
        self.addStopAct(stateId)
        self.addStopEffect(stateId)
        self.addStateAct(stateId)
        self.addStateSelfAct(stateId)
        self.addStateCaps(stateId)
        self.addChangeModel(stateId)
        self.addForceMove(stateId)
        self.addStateTint(stateId)
        self.addStateTwinkleFresnel(stateId)
        self.addFloatage(stateId)
        self.addConfusional(stateId)
        self.addAttachModel(stateId)
        self.addChangeWeapon(stateId)
        self.addScreenEffect(stateId)
        self.addModelScale(stateId)
        self.addHitInAir(stateId)
        self.addHideLvSpan(stateId)
        self.addDefaultModelState(stateId)
        self.addAnimateCamera(stateId)
        self.handleAvatar(stateId)
        self.addChangeYaw(stateId)
        self.updateNeiYiState(stateId)
        self.addNoJump(stateId)
        self.addPlayerEffect(stateId)
        self.addMeiHuo(stateId)
        self.addRefreshSkillRange(stateId)
        self.addRefreshZaijuSkill(stateId)
        self.addFear(stateId)
        self.addRaged(stateId)
        self.addRadar(stateId)
        self.addFootDust(stateId)
        self.addChaoFeng(stateId)
        self.addSpeedField(stateId)
        self.addSimpleQTE(stateId)
        self.addConnectEffect(stateId)
        self.addTempSkill(stateId)
        self.addHideBloodNumState(stateId)
        self.addTeamSSCGroupEffect(stateId)
        self.addStaticTint(stateId)
        self.refreshBanWsSkill(stateId)
        self.addChangeGravity(stateId)
        self.addChangeVisible(stateId)
        self.refreshCreationVisible(stateId)
        self.addForbidLock(stateId)
        func = self.enterFuncMap.get(stateId, None)
        if func != None:
            func(self, owner)
        self.stateHostMap[stateId] = self._findHostIdByStateId(stateId)
        self.effect[stateId] = None
        return stateId

    def needTintState(self, tintName = None):
        owner = BigWorld.entity(self.ownerId)
        if tintName == 'copperstealth_fnl':
            return True
        if owner and owner.fashion.isPlayer:
            return True
        return False

    def addHitInAir(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        flyHeight = stateData.getSkillData('hitInAir', None)
        owner = BigWorld.entity(self.ownerId)
        if owner.fashion.modelID not in (31004,):
            return
        if not flyHeight:
            return
        owner.am.enable = False
        startPos = Math.Vector3(owner.model.position)
        targetPos = Math.Vector3(startPos[0], startPos[1] + flyHeight, startPos[2])
        points = [(startPos,
          targetPos,
          self.motorSpeedOverCallback,
          20,
          0.0,
          -10), (targetPos,
          owner.position,
          self._collideScene,
          20,
          0.0,
          30.0)]
        if self.mf:
            self.mf.release()
        owner.model.action('1816')()
        self.mf = HitFlyPointFlyer(owner.model, points)
        self.mf.start()

    def delHitInAir(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        flyHeight = stateData.getSkillData('hitInAir', None)
        if owner.fashion.modelID not in (31004,):
            return
        if not flyHeight:
            return
        owner.am.enable = True

    def motorSpeedOverCallback(self):
        owner = BigWorld.entity(self.ownerId)
        try:
            owner.model.action('1817')().action('1818')()
        except:
            pass

    def _collideScene(self):
        owner = BigWorld.entity(self.ownerId)
        owner.am.enable = True
        try:
            owner.model.action('1819')()
        except:
            pass

    def getHostEffectLv(self, stateId, owner):
        owner = BigWorld.entity(self.ownerId)
        hostId = self._findHostIdByStateId(stateId)
        host = BigWorld.entities.get(hostId)
        effectLv, priority = (1, 1)
        if host and host.inWorld:
            effectLv = owner.getBuffEffectLv()
            priority = owner.getBuffEffectPriority(host)
        else:
            effectLv = owner.getBuffEffectLv()
            priority = owner.getBuffEffectPriority(host)
        return (effectLv, priority)

    def _addInCombatStateFx(self, stateData, owner):
        stateId = stateData.num
        attachModel = owner.model
        if owner.inRiding() and hasattr(owner.model, 'ride'):
            attachModel = owner.model.ride
        hostId = self._findHostIdByStateId(stateId)
        self.stateStartTimeMap[stateId] = BigWorld.time()
        fxList = self._getStateFxIndepended(stateId)
        gamelog.debug('----lihang@_addInCombatStateFx', fxList)
        if fxList:
            effectLv, priority = self.getHostEffectLv(stateId, owner)
            for i in fxList:
                lastTime = self._getStateLastTime(stateId)
                if self.fxMap.has_key(i) and not self.forceUpdate:
                    if not self.oldEffDurLongger(i, lastTime):
                        sfx.detachEffect(attachModel, i, self.fxMap[i])
                        self.fxMap.pop(i)
                        self.realAttachStateFx(attachModel, hostId, stateId, i, lastTime, effectLv, priority)
                else:
                    self.realAttachStateFx(attachModel, hostId, stateId, i, lastTime, effectLv, priority)

        self.effect[stateId] = None

    def oldEffDurLongger(self, effId, duration):
        if self.effEndTimeDict.has_key(effId):
            if self.effEndTimeDict.get(effId, 0) >= utils.getNow() + duration:
                return True
        return False

    def hasOtherStateWithEff(self, effId):
        owner = BigWorld.entity(self.ownerId)
        stateIds = self.effStateDict.get(effId, [])
        for stateId in stateIds:
            if stateId in owner.getStates():
                return True

        return False

    def realAttachStateFx(self, attachModel, hostId, stateId, effId, lastTime, effectLv, priority):
        if attachModel:
            attachModel.hostId = hostId
        isSumTime = SD.data.get(stateId, {}).get('isSumTime', 0)
        originEndTime = self.effEndTimeDict.get(effId, 0)
        if isSumTime and originEndTime:
            lastTime = originEndTime - utils.getNow() + lastTime
        ef = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (effectLv,
         priority,
         attachModel,
         effId,
         sfx.EFFECT_LIMIT,
         lastTime))
        if ef != None:
            if self.fxMap.has_key(effId) and self.fxMap[effId]:
                self.fxMap[effId].extend(ef)
            else:
                self.fxMap[effId] = ef
            if isSumTime and originEndTime:
                self.effEndTimeDict[effId] = originEndTime + self._getStateLastTime(stateId)
            else:
                self.effEndTimeDict[effId] = utils.getNow() + self._getStateLastTime(stateId)
            if self.effStateDict.has_key(effId) and self.fxMap[effId]:
                self.effStateDict[effId].append(stateId)
            else:
                self.effStateDict[effId] = [stateId]

    def _addStateFx(self, stateData, owner):
        stateId = stateData.num
        self.stateStartTimeMap[stateId] = BigWorld.time()
        if hasattr(owner, 'getOpacityValue') and owner.getOpacityValue()[0] in (gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, gameglobal.OPACITY_HIDE):
            return
        attachModel = owner.model
        isRiding = False
        if owner.inRiding() and hasattr(owner.model, 'ride'):
            isRiding = True
            try:
                attachModel = owner.model.ride
            except:
                raise Exception('_addStateFx, model: ' + str(owner.model.sources) + str(owner.bianshen))

        hostId = self._findHostIdByStateId(stateId)
        fxList = self._getAddedStateFx(stateId)
        effectLv, priority = self.getHostEffectLv(stateId, owner)
        ridingHideStates = SYSCD.data.get('ridingHideStates', ()) if isRiding else ()
        if fxList:
            for i in fxList:
                if i in ridingHideStates:
                    continue
                lastTime = self._getStateLastTime(stateId)
                if self.fxMap.has_key(i):
                    if not self.oldEffDurLongger(i, lastTime) or self.forceUpdate:
                        sfx.detachEffect(attachModel, i, self.fxMap[i])
                        self.fxMap.pop(i)
                        self.realAttachStateFx(attachModel, hostId, stateId, i, lastTime, effectLv, priority)
                else:
                    self.realAttachStateFx(attachModel, hostId, stateId, i, lastTime, effectLv, priority)

        if self.forceUpdate:
            pass
        else:
            fxList = stateData.getSkillData('startFx', [])
            for i in fxList:
                if self.startFxMap.has_key(i):
                    sfx.detachEffect(attachModel, i, self.startFxMap[i])
                if attachModel:
                    attachModel.hostId = hostId
                ef = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (effectLv,
                 priority,
                 attachModel,
                 i,
                 sfx.EFFECT_LIMIT,
                 gameglobal.EFFECT_LAST_TIME))
                if ef:
                    self.startFxMap[i] = ef

        self.attachingStateDataMap[stateId] = stateData

    def _addEnemySideStateFx(self, stateData, owner):
        p = BigWorld.player()
        if not p:
            return
        if not p.isEnemy(owner):
            return
        stateId = stateData.num
        if hasattr(owner, 'getOpacityValue') and owner.getOpacityValue()[0] in (gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, gameglobal.OPACITY_HIDE):
            return
        attachModel = owner.model
        if owner.inRiding() and hasattr(owner.model, 'ride'):
            try:
                attachModel = owner.model.ride
            except:
                raise Exception('_addEnemySideStateFx, model: ' + str(owner.model.sources) + str(owner.bianshen))

        hostId = self._findHostIdByStateId(stateId)
        fxList = stateData.getSkillData('enemySideFx', ())
        effectLv, priority = self.getHostEffectLv(stateId, owner)
        if fxList:
            for i in fxList:
                lastTime = self._getStateLastTime(stateId)
                ef = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (effectLv,
                 priority,
                 attachModel,
                 i,
                 sfx.EFFECT_LIMIT,
                 lastTime))
                if ef:
                    self.enemySideEffs.extend(ef)

    def _stopCombatStateFx(self, stopStateData):
        owner = BigWorld.entity(self.ownerId)
        stopStateId = stopStateData.num
        if stopStateData:
            fxList = self._getStateFxIndepended(stopStateId)
            gamelog.debug('----lihang@_stopCombatStateFx', fxList)
            if fxList:
                for i in fxList:
                    exist = False
                    for stateId in self.effect.keys():
                        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
                        if stateData and i in stateData.getSkillData('fx', []):
                            exist = True
                            break

                    if not exist:
                        owner = BigWorld.entity(self.ownerId)
                        attachModel = owner.model
                        if owner.inRiding() and hasattr(owner.model, 'ride'):
                            attachModel = owner.model.ride
                        if self.fxMap.has_key(i):
                            sfx.detachEffect(attachModel, i, self.fxMap[i])
                            self.fxMap.pop(i)

    def needDetachEffect(self, effId):
        if self.fxMap.has_key(effId):
            if self.oldEffDurLongger(effId, 1):
                if self.hasOtherStateWithEff(effId):
                    return False
                else:
                    return True
            else:
                return True
        return False

    def _stopStateFx(self, stopStateData):
        if not stopStateData:
            return
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        newStateList = owner.getStates().keys()
        oldStateList = owner.statesOld.keys()
        fxList = self._getDelStateFx(stopStateData, newStateList, oldStateList)
        gamelog.debug('----lihang@_stopStateFx', fxList)
        if fxList:
            for i in fxList:
                exist = False
                for stateId in self.effect.keys():
                    stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
                    if stateData and i in stateData.getSkillData('fx', []):
                        exist = True
                        break

                if not exist:
                    owner = BigWorld.entity(self.ownerId)
                    attachModel = owner.model
                    if owner.inRiding() and hasattr(owner.model, 'ride'):
                        attachModel = owner.model.ride
                    if self.needDetachEffect(i):
                        sfx.detachEffect(attachModel, i, self.fxMap[i])
                        self.fxMap.pop(i)

        fxList = stopStateData.getSkillData('startFx', [])
        for i in fxList:
            if self.startFxMap.has_key(i):
                self.startFxMap.pop(i)

    def _stopEnemySideStateFx(self, stateData, owner):
        p = BigWorld.player()
        if not p:
            return
        if not p.isEnemy(owner):
            return
        if hasattr(owner, 'getOpacityValue') and owner.getOpacityValue()[0] in (gameglobal.OPACITY_HIDE_INCLUDE_ATTACK, gameglobal.OPACITY_HIDE):
            return
        for eff in self.enemySideEffs:
            if eff:
                eff.stop()

        self.enemySideEffs = []

    def _delState(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return False
        if self.effect.has_key(stateId):
            stateData = self.attachingStateDataMap.pop(stateId, None)
            if not stateData:
                stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
            if not stateData:
                return
            self._stopStateFx(stateData)
            self._stopEnemySideStateFx(stateData, owner)
            if self._isStateExist(stateId):
                return
            self.effect.pop(stateId)
            self.addDelFx(stateId)
            self.delStopAct(stateId)
            self.delStopEffect(stateId)
            self.delStateAct(stateId)
            self.delStateSelfAct(stateId)
            self.delStateCaps(stateId)
            self.delChangeModel(stateId)
            self.delForceMove(stateId)
            self.delStateTint(stateId)
            self.delStateTwinkleFresnel(stateId)
            self.delFloatage(stateId)
            self.delConfusional(stateId)
            self.delChangeWeapon(stateId)
            self.delScreenEffect(stateId)
            self.delModelScale(stateId)
            self.delHitInAir(stateId)
            self.delHideLvSpan(stateId)
            self.delDefaultModelState(stateId)
            self.delAnimateCamera(stateId)
            self.delAvatar(stateId)
            self.delChangeYaw(stateId)
            self.delAttachModel(stateId)
            self.updateNeiYiState(stateId)
            self.delNoJump(stateId)
            self.delPlayerEffect(stateId)
            self.delMeiHuo(stateId)
            self.delRefreshSkillRange(stateId)
            self.delRefreshZaijuSkill(stateId)
            self.delFear(stateId)
            self.delRaged(stateId)
            self.delRadar(stateId)
            self.delFootDust(stateId)
            self.delChaoFeng(stateId)
            self.delSpeedField(stateId)
            self.delSimpleQTE(stateId)
            self.delConnectEffect(stateId)
            self.delTempSkill(stateId)
            self.delHideBloodNumState(stateId)
            self.delTeamSSCGroupEffect(stateId)
            self.delStaticTint(stateId)
            self.delChangeGravity(stateId)
            self.delChangeVisible(stateId)
            self.refreshBanWsSkill(stateId)
            self.refreshCreationVisible(stateId)
            self.delForbidLock(stateId)
            func = self.leaveFuncMap.get(stateId, None)
            if not func:
                func = self.leaveFuncMap.get(stateId, None)
            if func != None:
                owner = BigWorld.entity(self.ownerId)
                func(self, owner)
            del self.stateStartTimeMap[stateId]
            self.stateHostMap.pop(stateId, None)

    def addPlayerEffect(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        if owner != BigWorld.player():
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        playerEffs = stateData.getSkillData('playerEffs', ())
        effectLv, priority = self.getHostEffectLv(stateId, owner)
        attachModel = owner.model
        if owner.inRiding() and hasattr(owner.model, 'ride'):
            attachModel = owner.model.ride
        if playerEffs:
            for effId in playerEffs:
                if effId:
                    effs = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (effectLv,
                     priority,
                     attachModel,
                     effId,
                     sfx.EFFECT_LIMIT,
                     self._getStateLastTime(stateId)))
                    if effs:
                        self.playerEffs[effId] = effs

    def delPlayerEffect(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        playerEffs = stateData.getSkillData('playerEffs', ())
        for effId in playerEffs:
            effs = self.playerEffs.pop(effId, ())
            if effs:
                for eff in effs:
                    if eff:
                        eff.stop()

    def addStateTwinkleFresnel(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        twinkleFresnel = stateData.getSkillData('twinkleFresnel', False)
        if twinkleFresnel:
            owner.model.setTwinkleFresnel(twinkleFresnel[0], twinkleFresnel[1], twinkleFresnel[2], twinkleFresnel[3], twinkleFresnel[4])

    def delStateTwinkleFresnel(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        twinkleFresnel = stateData.getSkillData('twinkleFresnel', False)
        if twinkleFresnel:
            owner.model.setTwinkleFresnel(0.0, 0.0, 0.0, 0.0, 0.0)

    def addConfusional(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        confusionalState = stateData.getSkillData('confusional', False)
        if confusionalState and owner.fashion.isPlayer:
            owner.confusionalState = confusionalState
            owner.ap.stopMove()
            owner.ap.updateConfusionalMoveState()

    def addFloatage(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        if not owner.model:
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        floatHeight = stateData.getSkillData('floatage', None)
        if floatHeight:
            floatage = BigWorld.PyPoseControl()
            owner.model.floatage = floatage
            floatage.floatHeight = floatHeight
            if owner.fashion.isPlayer:
                owner.loseGravity()
            owner.resetTopLogo()

    def addDelFx(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        attachModel = owner.model
        hostId = self.stateHostMap.get(stateId, -1)
        effectLv, priority = self.getHostEffectLv(stateId, owner)
        for i in stateData.getSkillData('delFx', []):
            if attachModel:
                attachModel.hostId = hostId
            sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (effectLv,
             priority,
             attachModel,
             i,
             sfx.EFFECT_LIMIT,
             5))

    def addModelScale(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        oldStates = getattr(owner, 'statesOld', {})
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        msData = None
        physique = getattr(owner, 'physique', None)
        if physique:
            msData = stateData.getSkillData('scaleType', {}).get((physique.sex, physique.bodyType), ())
        if not msData:
            msData = stateData.getSkillData('modelScale', None)
        if msData and len(msData) == 2:
            if not getattr(owner, 'buffModelScale', None):
                owner.buffModelScale = [(stateId, msData)]
            elif (stateId, msData) not in owner.buffModelScale:
                owner.buffModelScale.append((stateId, msData))
            scale = msData[0]
            modelTypes = msData[1]
            for modelType in modelTypes:
                self._modelScale(stateId, owner, modelType, scale)

    def _getModelHP(self, model, state):
        gamelog.debug('_getModelHP', model, state)
        if not model:
            return None
        elif state == weaponModel.ATTACHED:
            return (model[2], model[4])
        elif state == weaponModel.HANG_UP or state == weaponModel.ATTACHED_RIGHT:
            return (model[3], model[5])
        else:
            return None

    def _modelScale(self, stateId, owner, modelType, scale):
        if modelType == gameglobal.STATE_MODEL_SCALE_TYPE_BODY:
            model = owner.model
            if hasattr(owner.modelServer, 'bodyModel'):
                model = owner.modelServer.bodyModel
            if owner.stateModelScale.get(stateId, 0) == scale:
                return
            if getattr(owner, 'IsSummonedSprite', None):
                return
            owner.stateModelScale[stateId] = scale
            owner.baseScale = owner.baseScale * scale
            owner.refreshModelScale(model)
        elif modelType == gameglobal.STATE_MODEL_SCALE_TYPE_RIGHT_WEAPON:
            rm = owner.modelServer.rightWeaponModel
            state = rm.state
            models = rm.models
            if models:
                for model in models:
                    hp = self._getModelHP(model, state)
                    if hp and hp[0]:
                        if rm.ownerModel and rm.ownerModel.node(hp[0]):
                            rm.ownerModel.node(hp[0]).scale(hp[1] * scale)
                        owner.stateModelScale[stateId] = (hp[0], hp[1])

        elif modelType == gameglobal.STATE_MODEL_SCALE_TYPE_LEFT_WEAPON:
            lm = owner.modelServer.leftWeaponModel
            state = lm.state
            models = lm.models
            if models:
                for model in models:
                    hp = self._getModelHP(model, state)
                    if hp and hp[0]:
                        if lm.ownerModel and lm.ownerModel.node(hp[0]):
                            lm.ownerModel.node(hp[0]).scale(hp[1] * scale)
                        owner.stateModelScale[stateId] = (hp[0], hp[1])

        if owner == BigWorld.player():
            owner.resetTopLogo()
            owner.resetCamera()

    def delModelScale(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        msData = None
        physique = getattr(owner, 'physique', None)
        if physique:
            msData = stateData.getSkillData('scaleType', {}).get((physique.sex, physique.bodyType), ())
        if not msData:
            msData = stateData.getSkillData('modelScale', None)
        gamelog.debug('------delModelScale', stateId, msData)
        if msData and len(msData) == 2:
            if owner.buffModelScale and (stateId, msData) in owner.buffModelScale:
                owner.buffModelScale.remove((stateId, msData))
            owner.buffIdModelScale = None
            modelTypes = msData[1]
            for modelType in modelTypes:
                if modelType == gameglobal.STATE_MODEL_SCALE_TYPE_BODY:
                    model = owner.model
                    if hasattr(owner.modelServer, 'bodyModel'):
                        model = owner.modelServer.bodyModel
                    if stateId in owner.stateModelScale:
                        scale = owner.stateModelScale.pop(stateId)
                        owner.baseScale = owner.baseScale / scale
                        owner.refreshModelScale(model)
                elif modelType == gameglobal.STATE_MODEL_SCALE_TYPE_RIGHT_WEAPON:
                    rm = owner.modelServer.rightWeaponModel
                    models = rm.models
                    if models:
                        if stateId in owner.stateModelScale:
                            scale = owner.stateModelScale.pop(stateId)
                            if scale and rm.ownerModel and rm.ownerModel.node(scale[0]):
                                rm.ownerModel.node(scale[0]).scale(scale[1])
                elif modelType == gameglobal.STATE_MODEL_SCALE_TYPE_LEFT_WEAPON:
                    lm = owner.modelServer.leftWeaponModel
                    models = lm.models
                    if models:
                        if stateId in owner.stateModelScale:
                            scale = owner.stateModelScale.pop(stateId)
                            if scale and lm.ownerModel and lm.ownerModel.node(scale[0]):
                                lm.ownerModel.node(scale[0]).scale(scale[1])

            if owner == BigWorld.player():
                owner.resetTopLogo()
                owner.resetCamera()

    def delNoJump(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        noJump = stateData.getSkillData('noJump', None)
        if noJump:
            owner.bufNoJump = False

    def delMeiHuo(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        meiHuo = stateData.getSkillData('meiHuo', None)
        if meiHuo:
            owner.inMeiHuo = False
            if owner == BigWorld.player():
                owner.endMeiHuoCallback()

    def delRefreshSkillRange(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        if owner != BigWorld.player():
            return
        if not BigWorld.player().targetLocked:
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        refreshSkillRange = stateData.getSkillData('refreshSkillRange', None)
        if refreshSkillRange:
            gameglobal.rds.ui.actionbar.checkAllSkillStat(gameglobal.SKILL_STAT_LACK_ENERGY)
            if hasattr(BigWorld.player().targetLocked, 'addRanges'):
                BigWorld.player().targetLocked.skillRanges.clear()
                BigWorld.player().targetLocked.addRanges()

    def delRefreshZaijuSkill(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        if owner != BigWorld.player():
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        refreshZaijuSkill = stateData.getSkillData('refreshZaijuSkill', None)
        if refreshZaijuSkill and gameglobal.rds.ui.zaijuV2.widget:
            gameglobal.rds.ui.zaijuV2.refreshSkillSlotsBind()

    def delFear(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        fear = stateData.getSkillData('fear', None)
        if fear:
            owner.inFear = False
            if owner == BigWorld.player():
                owner.endFearCallback()

    def delRaged(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        bloodIcon = SCD.data.get(stateId, {}).get('bloodIcon', '')
        if not bloodIcon:
            return
        if bloodIcon == 'raged':
            gameglobal.rds.ui.fightObserve.hideRaged(owner.id)

    def delForbidLock(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        forbidLock = SCD.data.get(stateId, {}).get('forbidLock', 0)
        if forbidLock:
            owner.forbidLock = False

    def delChangeGravity(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        changGravity = SCD.data.get(stateId, {}).get('changeGravity', None)
        if changGravity == None:
            return
        owner.inChangeGravity = False
        if getattr(owner, 'cacheGravity', None) != None:
            owner.physics.gravity = owner.cacheGravity
            owner.cacheGravity = None

    def delChangeVisible(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        hideModel = SCD.data.get(stateId, {}).get('hideModel', None)
        if not hideModel:
            return
        owner.isBuffHideModel = False
        owner.refreshOpacityState()

    def refreshCreationVisible(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld or not self.ownerId == BigWorld.player().id:
            return
        for entityId in BigWorld.player().creationVisibleByBuff.get(stateId, []):
            entity = BigWorld.entity(entityId)
            entity.refreshOpacityState()

    def delHideBloodNumState(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        hideBloodNum = SCD.data.get(stateId, {}).get('hideBloodNum', '')
        if hideBloodNum:
            clientcom.setEntityHideBloodNumState(owner, False)

    def delFootDust(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        footDustEffect = SCD.data.get(stateId, {}).get('footDustEffect', ())
        if not footDustEffect:
            return
        owner.footDustEffect = None

    def delRadar(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        p = BigWorld.player()
        if not owner or not owner.inWorld:
            return
        if not owner.id == p.id:
            return
        if stateId == const.BATTLE_FIELD_HUNT_DETECTION_BUFF:
            gameglobal.rds.ui.littleMap.setPlayIconVisible(False)
            soundId = SCD.data.get('HUNT_SOUND_RADAR', 5108)
            gameglobal.rds.sound.stopSound(soundId)

    def delChaoFeng(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        chaoFeng = stateData.getSkillData('chaoFeng', None)
        if chaoFeng:
            owner.inChaoFeng = False
            if owner == BigWorld.player():
                owner.endChaoFengCallback()

    def delTeamSSCGroupEffect(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        if stateId == const.TEAM_SSC_GROUP_MARK_BUFF:
            self.teamSSCGroupEffectHandle and BigWorld.cancelCallback(self.teamSSCGroupEffectHandle)
            self.teamSSCGroupEffectHandle = None
            owner.removeTeamSSCGroupEffect()

    def addStateTint(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        owner = BigWorld.entity(self.ownerId)
        tintData = stateData.getSkillData('stateTint', None)
        if not tintData:
            return
        tintFx = tintData[0]
        allModels = owner.allModels
        if len(tintData) == 2:
            allModels = owner.getTintModels(tintData[1])
        tintName, tintPrio, tint = skillDataInfo.getTintDataInfo(owner, tintFx)
        if owner.tintStateType[0] > tintPrio:
            return
        if owner.tintStateType[1]:
            owner.restoreTintStateType()
        if owner.tintDelCallBack:
            BigWorld.cancelCallback(owner.tintDelCallBack)
            owner.tintDelCallBack = None
        if self.tintStateMap.has_key(stateId):
            tintalt.gTintEffectCounterMgr.dec(tintalt.STATETINT)
        else:
            self.tintStateMap[stateId] = True
        hostId = self._findHostIdByStateId(stateId)
        host = BigWorld.entities.get(hostId)
        owner.tintStateType[0] = tintPrio
        if tintName and self.needTintState(tintName):
            owner.tintStateType[1] = tintName
            owner.tintDelCallBack = tintalt.ta_add(allModels, tintName, [tint, BigWorld.shaderTime()], 0.0, None, False, False, host, owner, tintType=tintalt.STATETINT)
        else:
            tintalt.ta_addHitGaoLiang(allModels, gameglobal.STATE_HIGHLIGHT_BEGINTIME, gameglobal.FRESNEL_STATE_KEEPTIME, gameglobal.STATE_HIGHLIGHT_ENDTIME, tint)
            owner.tintStateType[1] = tint

    def delConfusional(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        confusionalState = stateData.getSkillData('confusional', False)
        if confusionalState and owner.fashion.isPlayer:
            owner.ap.stopMove()
            owner.ap.needKeyInvert = False
            owner.confusionalState = gameglobal.CONFUSIONAL_DEFAULT
            owner.ap.updateMoveControl()

    def delFloatage(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        if not owner.model:
            return
        stateData = skillDataInfo.ClientSkillInfo(stateId, 1, 1)
        floatHeight = stateData.getSkillData('floatage', None)
        if floatHeight:
            owner.model.floatage = None
            owner.resetTopLogo()
            if owner.fashion.isPlayer:
                owner.restoreGravity()

    def _isExistSameTint(self, tintData):
        owner = BigWorld.entity(self.ownerId)
        for sid in owner.getStates().iterkeys():
            otherStateData = skillDataInfo.ClientSkillInfo(sid, 1, 1)
            otherTintData = otherStateData.getSkillData('stateTint', ())
            if tintData == otherTintData:
                return True

        return False

    def delStateTint(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        owner = BigWorld.entity(self.ownerId)
        tintData = stateData.getSkillData('stateTint', ())
        if not tintData:
            return
        if stateData == None or owner == None:
            return
        if self._isExistSameTint(tintData):
            tintalt.gTintEffectCounterMgr.dec(tintalt.STATETINT)
            if self.tintStateMap.has_key(stateId):
                del self.tintStateMap[stateId]
            return
        tintFx = tintData[0]
        allModels = owner.allModels
        if len(tintData) == 2:
            allModels = owner.getTintModels(tintData[1])
            if allModels is None:
                return
        tintName, tintPrio, tint = skillDataInfo.getTintDataInfo(owner, tintFx)
        if tintName and self.needTintState(tintName):
            tintalt.ta_del(allModels, tintName, isTaAddCall=True, tintType=tintalt.STATETINT)
        if self.tintStateMap.has_key(stateId):
            del self.tintStateMap[stateId]
        if hasattr(owner, 'tintStateType') and owner.tintStateType[0] <= tintPrio:
            owner.restoreTintStateType()

    def addForceMove(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        owner = BigWorld.entity(self.ownerId)
        needAutoMove = stateData.getSkillData('autoMove', 0)
        if needAutoMove and owner.fashion.isPlayer:
            owner.ap.forwardMagnitude = 1
            owner.ap.backwardMagnitude = 0
            owner.ap.leftwardMagnitude = 0
            owner.ap.rightwardMagnitude = 0
            owner.ap.updateVelocity()
            owner.isForceMove = needAutoMove

    def addChangeModel(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner:
            return
        forceChangeModel = SD.data.get(stateId, {}).get('forceChangeModel', False)
        if owner.IsAvatar and not forceChangeModel:
            return
        if hasattr(owner, 'firstFetchFinished') and not owner.firstFetchFinished:
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        modelIds = stateData.getSkillData('mReplace', None)
        scales = stateData.getSkillData('scale', None)
        if modelIds and scales:
            index = random.randint(0, len(modelIds) - 1)
            modelId = modelIds[index]
            scale = scales[index]
            if hasattr(owner, 'bsState'):
                newBsLv = SD.data.get(stateId).get('bsLv', 0)
                if owner.bsState:
                    return
                owner.bsState = (stateId, newBsLv)
                owner.bufActState = None
            modelPath = gameglobal.charRes + str(modelId) + '/' + str(modelId) + '.model'
            gamelog.debug('----------------addChangeModel', owner, BigWorld.player())
            if owner == BigWorld.player():
                if owner.inFly:
                    owner.cell.leaveWingFly()
                if owner.inRiding():
                    owner.cell.leaveRide()
            if owner.oldModel:
                owner.oldModel = None
            if hasattr(owner.modelServer, 'bodyModel'):
                owner.oldModel = owner.modelServer.bodyModel
            else:
                owner.oldModel = owner.model
            if owner.oldModel:
                owner.oldModel.entityId = owner.id
            owner.fashion.loadSinglePartModel(modelPath, callback=Functor(self._reAddFxAfterChangeModel, stateId, scale))
            if owner.IsAvatar:
                owner.resetFootIK()

    def addAttachModel(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        attachModel = stateData.getSkillData('attachModel', None)
        if attachModel:
            bm = getattr(owner.modelServer, 'buffModel', None)
            if bm:
                bm.equipItem(attachModel)
                bm.attach(owner.modelServer.bodyModel)
                owner.buffAttachModel = True
                if hasattr(owner, 'refreshWeaponVisible'):
                    owner.refreshWeaponVisible()
                if hasattr(owner, 'refreshBackWearVisible'):
                    owner.refreshBackWearVisible()

    def updateNeiYiState(self, stateId):
        if stateId in const.ALL_SHOW_NEIYI_BUFF:
            owner = BigWorld.entity(self.ownerId)
            if not owner or not owner.inWorld or not hasattr(owner, 'modelServer'):
                return
            if owner.modelServer.isReady() and getattr(owner, 'firstFetchFinished', False):
                owner.modelServer.bodyPartsUpdate(False, False, False, True)

    def addNoJump(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        noJump = stateData.getSkillData('noJump', None)
        if noJump:
            owner.bufNoJump = True

    def addMeiHuo(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        meiHuo = stateData.getSkillData('meiHuo', None)
        if meiHuo:
            owner.inMeiHuo = True
            if owner == BigWorld.player():
                owner.ap.stopMove()
                owner.beginMeiHuo()
                if BigWorld.player().getOperationMode() == gameglobal.ACTION_MODE:
                    owner.ap.restore()

    def addRefreshSkillRange(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        if owner != BigWorld.player():
            return
        if not BigWorld.player().targetLocked:
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        refreshSkillRange = stateData.getSkillData('refreshSkillRange', None)
        if refreshSkillRange:
            gameglobal.rds.ui.actionbar.checkAllSkillStat(gameglobal.SKILL_STAT_LACK_ENERGY)
            if hasattr(BigWorld.player().targetLocked, 'addRanges'):
                BigWorld.player().targetLocked.skillRanges.clear()
                BigWorld.player().targetLocked.addRanges()

    def addRefreshZaijuSkill(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        if owner != BigWorld.player():
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        refreshZaijuSkill = stateData.getSkillData('refreshZaijuSkill', None)
        if refreshZaijuSkill and gameglobal.rds.ui.zaijuV2.widget:
            gameglobal.rds.ui.zaijuV2.refreshSkillSlotsBind()

    def refreshBanWsSkill(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        if owner != BigWorld.player():
            return
        if gameglobal.rds.ui.actionbar.isBanWSSkillBuff(stateId):
            gameglobal.rds.ui.actionbar.initAllSkillStat()

    def addFear(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        fear = stateData.getSkillData('fear', None)
        if fear:
            owner.inFear = True
            if owner == BigWorld.player():
                owner.beginFear()

    def addFootDust(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        footDustEffect = SCD.data.get(stateId, {}).get('footDustEffect', ())
        if not footDustEffect:
            return
        owner.footDustEffect = footDustEffect

    def addRaged(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        bloodIcon = SCD.data.get(stateId, {}).get('bloodIcon', '')
        if not bloodIcon:
            return
        if bloodIcon == 'raged':
            state = owner.getStates().get(stateId, [])
            if state:
                lastTime = state[0][2]
                gameglobal.rds.ui.fightObserve.showRaged(owner.id, lastTime)

    def addForbidLock(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        forbidLock = SCD.data.get(stateId, {}).get('forbidLock', 0)
        if forbidLock:
            owner.forbidLock = True
            p = BigWorld.player()
            if p and getattr(p, 'targetLocked', None) == owner:
                p.unlockTarget()

    def addChangeGravity(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        changeGravity = SCD.data.get(stateId, {}).get('changeGravity', None)
        if changeGravity == None:
            return
        if hasattr(owner, '_setGravity'):
            owner._setGravity(changeGravity)
            owner.inChangeGravity = True

    def addChangeVisible(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        hideModel = SCD.data.get(stateId, {}).get('hideModel', None)
        if not hideModel:
            return
        owner.isBuffHideModel = True
        owner.refreshOpacityState()

    def addHideBloodNumState(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        hideBloodNum = SCD.data.get(stateId, {}).get('hideBloodNum', '')
        if not hideBloodNum:
            return
        clientcom.setEntityHideBloodNumState(owner, True)

    def addRadar(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        p = BigWorld.player()
        if not owner or not owner.inWorld:
            return
        if not owner.id == p.id:
            return
        if stateId == const.BATTLE_FIELD_HUNT_DETECTION_BUFF:
            gameglobal.rds.ui.littleMap.setPlayIconVisible(True)
            soundId = SCD.data.get('HUNT_SOUND_RADAR', 5108)
            gameglobal.rds.sound.playSound(soundId)

    def addChaoFeng(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        chaoFeng = stateData.getSkillData('chaoFeng', None)
        if chaoFeng:
            owner.inChaoFeng = stateId
            if owner == BigWorld.player():
                owner.ap.stopMove()
                owner.beginChaoFeng()

    def addSpeedField(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        if owner != BigWorld.player():
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        speedField = stateData.getSkillData('speedField', None)
        if speedField:
            owner.speedField = (self._findHostIdByStateId(stateId), speedField)
            owner.beginSpeedField()

    def delSpeedField(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        if owner != BigWorld.player():
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        speedField = stateData.getSkillData('speedField', None)
        if speedField:
            owner.speedField = None
            owner.ap.updateVelocity()
            owner.endSpeedFieldCB()

    def addStaticTint(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        staticTint = stateData.getSkillData('staticTint', None)
        if staticTint:
            tintalt.ta_set_static([owner.model], staticTint)

    def delStaticTint(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        staticTint = stateData.getSkillData('staticTint', None)
        if staticTint:
            tintalt.ta_reset([owner.model])

    def addSimpleQTE(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        simpleQTEId = stateData.getSkillData('simpleQTEId', None)
        if simpleQTEId:
            owner.inSimpleQte = simpleQTEId
            if owner == BigWorld.player():
                gameglobal.rds.ui.simpleQTE.show(simpleQTEId)

    def delSimpleQTE(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        simpleQTEId = stateData.getSkillData('simpleQTEId', None)
        if simpleQTEId:
            owner.inSimpleQte = False
            if owner == BigWorld.player():
                gameglobal.rds.ui.simpleQTE.endSimpleQte()

    def addConnectEffect(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        connEffs = stateData.getSkillData('connEffs', None)
        if connEffs:
            startNodeName = stateData.getSkillData('connEffStartNode', '')
            endNodeName = stateData.getSkillData('connEffEndNode', '')
            startNode = owner.model.node(startNodeName)
            hostId = self._findHostIdByStateId(stateId)
            host = BigWorld.entities.get(hostId, None)
            if not host or not host.inWorld:
                return
            if not host.model:
                return
            endNode = host.model.node(endNodeName)
            if startNode and endNode:
                for ef in connEffs:
                    effect = sfx.attachEffect(gameglobal.ATTACH_EFFECT_CONNECTOR, (owner.getSkillEffectLv(),
                     startNode,
                     ef,
                     endNode,
                     50,
                     owner.getSkillEffectPriority()))
                    self.connEffs.append(effect)

    def addTeamSSCGroupEffect(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        if stateId == const.TEAM_SSC_GROUP_MARK_BUFF:
            self.teamSSCGroupEffectHandle and BigWorld.cancelCallback(self.teamSSCGroupEffectHandle)
            self.teamSSCGroupEffectHandle = BigWorld.callback(5, owner.addTeamSSCGroupEffect)

    def delConnectEffect(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        connEffs = stateData.getSkillData('connEffs', None)
        if connEffs:
            self.releaseConnectEffect()

    def addTempSkill(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        if owner != BigWorld.player():
            return
        stateData = SD.data.get(stateId, {})
        tempSkillId = stateData.get('tempSkillId', None)
        if tempSkillId:
            needMoreBuff = stateData.get('needMoreBuff', None)
            self.tempSkillInfo[stateId] = needMoreBuff
            if not needMoreBuff:
                gameglobal.rds.ui.buffSkill.addInfo((gameglobal.BUFF_SKILL_TYPE_BUFF, stateId), None)

    def refreshTempSkill(self):
        if not self.tempSkillInfo:
            return
        for stateId, info in self.tempSkillInfo.iteritems():
            if info:
                if self.hasTempSkillExtraBuff(info):
                    gameglobal.rds.ui.buffSkill.addInfo((gameglobal.BUFF_SKILL_TYPE_BUFF, stateId), None)
                else:
                    gameglobal.rds.ui.buffSkill.removeInfo((gameglobal.BUFF_SKILL_TYPE_BUFF, stateId))

    def hasTempSkillExtraBuff(self, info):
        owner = BigWorld.entity(self.ownerId)
        for stateId in info:
            if not owner.hasState(stateId):
                return False

        return True

    def delTempSkill(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        if owner != BigWorld.player():
            return
        stateData = SD.data.get(stateId, {})
        tempSkillId = stateData.get('tempSkillId', None)
        if tempSkillId:
            if self.tempSkillInfo.has_key(stateId):
                self.tempSkillInfo.pop(stateId, None)
            gameglobal.rds.ui.buffSkill.removeInfo((gameglobal.BUFF_SKILL_TYPE_BUFF, stateId))

    def releaseConnectEffect(self):
        for ec in self.connEffs:
            if ec:
                ec.detach()

    def addChangeYaw(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        changeYawByHost = stateData.getSkillData('changeYawByHost', None)
        if changeYawByHost:
            hostId = self._findHostIdByStateId(stateId)
            host = BigWorld.entities.get(hostId, None)
            if not host or not host.inWorld:
                return
            if changeYawByHost == gameglobal.STATE_CAHGNE_YAW_TYPE_SAME:
                yaw = host.yaw
            else:
                yaw = host.yaw - math.pi
            BigWorld.callback(0.1, Functor(self.changeYawCallback, yaw))

    def changeYawCallback(self, yaw):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        owner.am.turnModelToEntity = False
        owner.model.yaw = yaw
        if owner == BigWorld.player():
            owner.faceToDir(yaw)

    def handleAvatar(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner:
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        avatarInfo = stateData.getSkillData('avatarInfo', None)
        if avatarInfo:
            model = owner.modelServer.bodyModel
            for info in avatarInfo:
                if hasattr(model, 'boneScale') and not self.oldBoneScale.has_key(info[0]):
                    scale, length = self.getBoneScaleByNode(info[0])
                    self.oldBoneScale[info[0]] = (scale, length)
                    model.boneScale.setBoneScale(info[0], info[1], info[2], False)

            clientcom.enableModelPhysics(owner.model, False)

    def getBoneScaleByNode(self, nodeName):
        owner = BigWorld.entity(self.ownerId)
        if not owner:
            return (1.0, 1.0)
        model = owner.modelServer.bodyModel
        if hasattr(model, 'boneScale'):
            boneInfo = model.boneScale.getBoneScale()
            for info in boneInfo:
                if info[0] == nodeName:
                    return (info[1], info[2])

        return (1.0, 1.0)

    def delAvatar(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner:
            return
        stateData = skillDataInfo.ClientSkillInfo(stateId, 1, 1)
        avatarInfo = stateData.getSkillData('avatarInfo', None)
        if avatarInfo and self.oldBoneScale:
            model = owner.modelServer.bodyModel
            for info in avatarInfo:
                scale = self.oldBoneScale[info[0]][0]
                length = self.oldBoneScale[info[0]][1]
                del self.oldBoneScale[info[0]]
                if hasattr(model, 'boneScale'):
                    model.boneScale.setBoneScale(info[0], scale, length, False)

            clientcom.enableModelPhysics(owner.model, True)

    def delChangeYaw(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        owner.fashion.resetTurnBodyState()

    def delAttachModel(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        attachModel = stateData.getSkillData('attachModel', None)
        if attachModel:
            bm = getattr(owner.modelServer, 'buffModel', None)
            if bm:
                owner.buffAttachModel = False
                if hasattr(owner, 'refreshWeaponVisible'):
                    owner.refreshWeaponVisible()
                if hasattr(owner, 'refreshBackWearVisible'):
                    owner.refreshBackWearVisible()
                if bm.state == weaponModel.ATTACHED:
                    bm.detach()
                bm.release()

    def _reAddFxAfterChangeModel(self, stateId, scale, model):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        if not model:
            return
        if owner.oldModel == None:
            return
        owner.fashion.setupModel(model, False)
        BigWorld.callback(0, owner.resetTopLogo)
        model.scale = (scale, scale, scale)
        if not hasattr(owner, 'effect'):
            return
        ids = owner.getStates().keys()
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        if stateData == None or owner == None or stateId not in ids:
            return
        if self._needAddStateFx(stateData, owner):
            attachModel = owner.model
            hostId = self._findHostIdByStateId(stateId)
            fx = stateData.getSkillData('fx', [])
            if fx:
                effectLv, priority = self.getHostEffectLv(stateId, owner)
                for i in fx[0]:
                    if owner.inRiding() and hasattr(owner.model, 'ride'):
                        attachModel = owner.model.ride
                    if attachedModel:
                        attachModel.hostId = hostId
                    ef = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (effectLv,
                     priority,
                     attachModel,
                     i,
                     sfx.EFFECT_LIMIT,
                     self._getStateLastTime(stateId)))
                    if ef != None:
                        self.fxMap[i] = ef

        if owner.IsSummonedSprite:
            owner.refreshOpacityState()

    def delChangeModel(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner:
            return
        forceChangeModel = SD.data.get(stateId, {}).get('forceChangeModel', False)
        if owner.IsAvatar and not forceChangeModel:
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        modelId = stateData.getSkillData('mReplace', None)
        if hasattr(owner, 'inBoothing') and owner.inBoothing():
            return
        if modelId:
            if getattr(owner, 'bsState', None):
                if stateId != owner.bsState[0]:
                    return
                owner.bsState = None
                if owner.IsSummonedSprite:
                    if owner.transformed and owner.transformModel:
                        owner.oldModel = owner.transformModel
                    else:
                        owner.oldModel = owner.bodyModel
                if owner.oldModel:
                    if not owner.oldModel.attached:
                        owner.fashion.setupModel(owner.oldModel, True)
                        owner.oldModel = None
                    else:
                        owner.oldModel = None
                    if getattr(owner, 'life') == gametypes.LIFE_DEAD:
                        if owner.fashion.doingActionType() != action.DEAD_ACTION:
                            owner.playDieAction()
                if owner.IsAvatar or owner.isAvatarMonster():
                    owner.modelServer.refreshWeaponState()
                    if owner.fashion.isPlayer:
                        velocity = Math.Vector3(owner.physics.velocity.x, 0, owner.physics.velocity.z)
                        owner.physics.velocity = velocity
                        owner.physics.maxTopVelocity = velocity
                owner.forceUpdateEffect()
                owner.resetTopLogo()
                if owner.IsAvatar:
                    owner.resetFootIK()
                if owner == BigWorld.player():
                    owner.resetCamera()
                if owner.IsSummonedSprite:
                    owner.refreshOpacityState()

    def addStopAct(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld or not owner.fashion:
            return
        if owner.fashion.doingActionType() in [action.HIT_DIEFLY_ACTION]:
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        stopact = stateData.getSkillData('stopact', 0)
        gamelog.debug('@zf:state:addStopact', stopact, stateId)
        if stopact:
            self.addStopActEffect()

    def addStopEffect(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld or not owner.fashion:
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        stopEffect = stateData.getSkillData('stopEffect', 0)
        if stopEffect:
            owner.freezeEffect(stopEffect)

    def addDefaultModelState(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner.firstFetchFinished:
            return
        if getattr(owner, 'inWenQuanState', False):
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        needDefaultModelState = stateData.getSkillData('defaultModelState', 0)
        if not needDefaultModelState:
            return
        owner.modelServer.bodyUpdateStatus = modelServer.BODY_UPDATE_STATUS_NORMAL
        owner.inWenQuanState = True
        owner.modelServer.bodyPartsUpdate(False, False, True)
        owner.modelServer.weaponUpdate()

    def addAnimateCamera(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner.firstFetchFinished or owner != BigWorld.player():
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        animateInfo = stateData.getSkillData('animateInfo', 0)
        if not animateInfo:
            return
        if not cameraEffect.checkEnableAnimateCamera():
            return
        animateCamera, actionId, skillList = animateInfo
        _cameraAction = None
        _playerAction = None
        for modelId, school, cameraAction, playerAction in actionId:
            if modelId == owner.fashion.modelID and owner.realPhysique.school == school:
                _cameraAction = cameraAction
                _playerAction = playerAction
                break

        modelId = animateCamera[0]
        boneName = animateCamera[1]
        owner.skillPlayer.animateInfo = ((modelId, boneName, _cameraAction), _playerAction, skillList)
        if _playerAction:
            owner.model.resideActions(_playerAction)
        modelPath = 'item/model/%d/%d.model' % (modelId, modelId)
        if not cameraEffect.cameraModel:
            charRes.getSimpleModel(modelPath, None, Functor(self._playCameraAction, _cameraAction))
        else:
            self._playCameraAction(_cameraAction, cameraEffect.cameraModel)

    def delAnimateCamera(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner.firstFetchFinished or owner != BigWorld.player():
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        animateInfo = stateData.getSkillData('animateInfo', 0)
        if not animateInfo:
            return
        cameraEffect.cameraModel = None
        owner.skillPlayer.animateInfo = None

    def _playCameraAction(self, actionName, model):
        if not model:
            return
        cameraEffect.cameraModel = model
        if not model.inWorld:
            BigWorld.player().addModel(model)
        try:
            model.action(actionName)()
        except:
            pass

    def delDefaultModelState(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        needDefaultModelState = stateData.getSkillData('defaultModelState', 0)
        if not needDefaultModelState:
            return
        if not getattr(owner, 'inWenQuanState', False):
            return
        self._delDefaultModelState()

    def _delDefaultModelState(self):
        owner = BigWorld.entity(self.ownerId)
        owner.inWenQuanState = False
        owner.modelServer.bodyPartsUpdate(False, False, True)
        owner.modelServer.weaponUpdate()
        owner.modelServer.wearUpdate()
        owner.modelServer.wingFlyModelUpdate()

    def addStopActEffect(self):
        gamelog.debug('@zf:state:addStopActEffect')
        owner = BigWorld.entity(self.ownerId)
        if owner.model:
            owner.updateModelFreeze(99999.0)
            owner.model.freezeType = gameglobal.FREEZE_TYPE_STATE
        owner.isFreezeAct = True
        owner.hitStateType = 5

    def delForceMove(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        owner = BigWorld.entity(self.ownerId)
        needAutoMove = stateData.getSkillData('autoMove', 0)
        if needAutoMove and owner.fashion.isPlayer:
            owner.isForceMove = gameglobal.FORCE_MOVE_NONE
            owner.ap.forwardMagnitude = 0
            owner.ap.updateVelocity()
            owner.updateActionKeyState()

    def delStopAct(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        stopact = stateData.getSkillData('stopact', 0)
        if stopact:
            self.delStopActEffect(stateId)

    def delStopActEffect(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        owner.updateModelFreeze(-1.0)
        owner.isFreezeAct = False
        owner.stopSkillMove(True)
        self.__updateHitStateAction(stateId)

    def delStopEffect(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        stopEffect = stateData.getSkillData('stopEffect', 0)
        if stopEffect:
            owner.clearFreezeEffect()

    def _pushActionGroup(self, stateId, idx):
        self.stateActMap[stateId] = idx

    def _popActionGroup(self, stateId):
        if self.stateActMap.has_key(stateId):
            idx = self.stateActMap[stateId]
            del self.stateActMap[stateId]
            return idx
        return 0

    def __getStateActActions(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        actions = stateData.getSkillData('stateAct', None)
        if actions:
            actType = owner.fashion.getPrefixStateAction()
            newAct = []
            for i, act in enumerate(actions):
                act = list(act)
                for j in xrange(2, len(act)):
                    if act[j] != '':
                        act[j] = actType + act[j]
                        if act[j] not in owner.fashion.getActionNameList():
                            break

                if j == len(act) - 1:
                    act.append(i)
                    newAct.append(act)

            if newAct:
                idx = random.randint(0, len(newAct) - 1)
                newAct = newAct[idx]
                self._pushActionGroup(stateId, newAct[-1])
                actions = newAct[:-1]
            else:
                idx = random.randint(0, len(actions) - 1)
                newAct = actions[idx]
                self._pushActionGroup(stateId, idx)
                actions = [newAct[0], newAct[1], owner.fashion.getFaintActionName()]
        return actions

    def _findHostIdByStateId(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        slst = owner.getStates().get(stateId)
        if not slst:
            return -1
        for s in slst:
            return s[gametypes.STATE_INDEX_SRCID]

        return -1

    def addStateAct(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner.inWorld:
            return
        if not owner.fashion:
            raise Exception('owner no fashion: ' + str(type(owner)) + '. stateId: ' + str(stateId))
            return
        if owner.life == gametypes.LIFE_DEAD or owner.fashion.doingActionType() in [action.HIT_DIEFLY_ACTION]:
            return
        if hasattr(owner, 'castSkillBusy'):
            owner.castSkillBusy = False
        actions = self.__getStateActActions(stateId)
        if actions:
            owner.fashion.breakModelMoveFreeze()
            actions = list(actions)
            delayTime = actions.pop(0)
            delayTime = delayTime + random.random() / 10.0
            hitStateType = actions.pop(0)
            gamelog.debug('hitStateType', hitStateType, owner.hitStateType)
            if hitStateType >= owner.hitStateType or owner.fashion.doingActionType() in [action.FUKONG_STOP_ACTION,
             action.TIAOGAO_STOP_ACTION,
             action.JIDAO_STOP_ACTION,
             action.FAINT_STOP_ACTION]:
                BigWorld.callback(delayTime, Functor(self._addStateAct, stateId, actions, delayTime, hitStateType))

    def _addStateAct(self, sId, actions, delayTime, hitStateType):
        owner = BigWorld.entity(self.ownerId)
        if not owner:
            return
        if owner.life == gametypes.LIFE_DEAD or owner.fashion.doingActionType() in [action.HIT_DIEFLY_ACTION]:
            return
        owner.fashion.stopAction()
        hitPrefix = 'FAINT'
        if hitStateType == action.FAINT_STATE:
            hitPrefix = 'FAINT'
        elif hitStateType == action.JIDAO_STATE:
            hitPrefix = 'JIDAO'
        elif hitStateType == action.TIAOGAO_STATE:
            hitPrefix = 'TIAOGAO'
        elif hitStateType == action.FUKONG_STATE:
            hitPrefix = 'FUKONG'
        if self.actStopCallBack.has_key(sId):
            BigWorld.cancelCallback(self.actStopCallBack[sId])
            del self.actStopCallBack[sId]
        if self.actLoopCallBack.has_key(sId):
            BigWorld.cancelCallback(self.actLoopCallBack[sId])
            del self.actLoopCallBack[sId]
        if hasattr(owner, 'bianshen') and owner.bianshen[0] in (gametypes.BIANSHEN_ZAIJU, gametypes.BIANSHEN_BIANYAO):
            if owner.modelServer.rideAttached.zaijuMode in (attachedModel.ZAIJU_BEATTACHED, attachedModel.ZAIJU_ATTACH):
                faintAction = ZJD.data.get(owner.bianshen[1], {}).get('faintAction', None)
                if faintAction:
                    actType = getattr(action, hitPrefix + '_LOOP_ACTION')
                    owner.fashion.playAction([faintAction], actType)
                    return
        elif getattr(owner, 'IsAvatar', False) and owner.canFly():
            if hitPrefix != 'FAINT':
                hitPrefix = 'FAINT'
                faintAction = owner.fashion.getFaintActionName()
                if faintAction:
                    actType = getattr(action, hitPrefix + '_LOOP_ACTION')
                    owner.fashion.playAction([faintAction], actType)
                return
        if owner.hitStateType == hitStateType and hitStateType == action.FUKONG_STATE:
            if owner.fashion.doingActionType() != getattr(action, hitPrefix + '_STOP_ACTION'):
                actions = self.__getStateActActions(sId)
                totalTime = self._getStateLastTime(sId)
                actions = list(actions)
                delayTime = actions.pop(0)
                hitStateType = actions.pop(0)
                l = len(actions)
                if l > 2:
                    dropTime = owner.fashion.getActionTime(actions[2])
                    self.actStopCallBack[sId] = BigWorld.callback(totalTime - dropTime, Functor(self.addFollowAct, sId, actions, hitPrefix))
                    return
        owner.hitStateType = hitStateType
        totalTime = 0
        l = len(actions)
        if l == 1:
            if actions[0] in owner.fashion.getActionNameList():
                owner.fashion.playAction(actions[0:1], getattr(action, hitPrefix + '_LOOP_ACTION'))
        else:
            startTime = owner.fashion.getActionTime(actions[0])
            dropTime = owner.fashion.getActionTime(actions[2])
            if SD.data.has_key(sId):
                totalTime = self._getStateLastTime(sId) - delayTime
            if startTime:
                gamelog.debug('startTime:', startTime)
                BigWorld.callback(startTime - 0.15, Functor(self.__checkDeadState, sId, getattr(action, hitPrefix + '_START_ACTION')))
                owner.fashion.playAction(actions[0:-2], getattr(action, hitPrefix + '_START_ACTION'), keep=startTime)
                if hitStateType == action.JIDAO_STATE:
                    owner.beginDaoDiStartAction(actions[0:-2], sId, actions[1:-1])
            if totalTime > startTime + dropTime:
                self.actLoopCallBack[sId] = BigWorld.callback(startTime - 0.15, Functor(self.stateLoopAction, actions[1:-1], getattr(action, hitPrefix + '_LOOP_ACTION')))
            self.actStopCallBack[sId] = BigWorld.callback(totalTime - dropTime, Functor(self.addFollowAct, sId, actions, hitPrefix))

    def resetStateLoopAction(self, timm, sId, actions, actType):
        if self.actLoopCallBack.get(sId, None):
            BigWorld.cancelCallback(self.actLoopCallBack.get(sId, None))
        self.actLoopCallBack[sId] = BigWorld.callback(timm - 0.2, Functor(self.stateLoopAction, actions, actType))

    def stateLoopAction(self, actions, actType):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        owner.daoDiStartAction = None
        if owner.life == gametypes.LIFE_DEAD or owner.fashion.doingActionType() in [action.HIT_DIEFLY_ACTION]:
            return
        owner.fashion.playAction(actions, actType)

    def _getStateLastTime(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        slst = owner.getStates().get(stateId)
        if not slst:
            return 0.0
        for s in slst:
            return s[gametypes.STATE_INDEX_LASTTIME]

        return 0.0

    def __checkDeadState(self, stateId, actionType):
        gamelog.debug('__checkDeadState')
        owner = BigWorld.entity(self.ownerId)
        if not owner:
            return
        if owner.life != gametypes.LIFE_DEAD or owner.fashion.doingActionType() == ACT.HIT_DIEFLY_ACTION:
            return
        actions = self.__getDelStateActActions(stateId, False)
        actions = list(actions)
        if actionType in [action.TIAOGAO_START_ACTION,
         action.JIDAO_START_ACTION,
         action.FAINT_START_ACTION,
         action.FUKONG_START_ACTION]:
            needDieAction = False
            if owner.IsMonster:
                needDieAction = MMCD.data.get(owner.charType, {}).get('dieActGround', False)
            if self.actStopCallBack.has_key(stateId):
                BigWorld.cancelCallback(self.actStopCallBack[stateId])
                del self.actStopCallBack[stateId]
            if self.actLoopCallBack.has_key(stateId):
                gamelog.debug('__checkDeadState1')
                BigWorld.cancelCallback(self.actLoopCallBack[stateId])
                del self.actLoopCallBack[stateId]
            if actionType == action.FAINT_START_ACTION:
                owner.playDieAction(True, forcePlayAction=True)
            elif actionType == action.FUKONG_START_ACTION:
                if len(actions) == 5:
                    stopActionTime = owner.fashion.getActionTime(actions[4])
                    if stopActionTime:
                        hitPrefix = 'FUKONG'
                        actions.pop(0)
                        actions.pop(0)
                        self.addFollowAct(stateId, actions, hitPrefix, True)
                        BigWorld.callback(stopActionTime, Functor(owner.playDieAction, True, True))
            else:
                owner.playDieAction(False, True)
                needDieAction = False
            if needDieAction:
                owner.playDieAction(True, True)

    def addStateSelfAct(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner:
            return
        if owner.inRiding():
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        actionCaps = stateData.getSkillData('stateSelfAct', None)
        if actionCaps:
            owner.updateModelFreeze(-1.0)
            owner.fashion.stopAction()
            if hasattr(owner, 'am'):
                matchCap = keys.CAPS_HAND_FREE
                if owner.inCombat:
                    matchCap = owner.fashion.getWeaponActType()
                owner.fashion.setWeaponCaps([matchCap, actionCaps])
                if not (hasattr(owner, '_isOnZaijuOrBianyao') and owner._isOnZaijuOrBianyao()):
                    owner.bufActState = owner.am.matchCaps

    def addStateCaps(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner:
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        stateCaps = stateData.getSkillData('stateCaps', None)
        if stateCaps:
            owner.buffCaps = list(stateCaps)
            owner.fashion.autoSetStateCaps()

    def delStateSelfAct(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner:
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        actionCaps = stateData.getSkillData('stateSelfAct', None)
        if actionCaps:
            owner.bufActState = None
            if not owner.inCombat and hasattr(owner, 'switchWeaponState'):
                owner.switchWeaponState(gametypes.WEAPON_HANDFREE)
            elif owner.IsAvatar:
                weaponCaps = owner.fashion.weaponType if owner.fashion.weaponType else 1
                owner.fashion.setWeaponCaps([weaponCaps])
            owner.fashion.autoSetStateCaps()

    def delStateCaps(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner:
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        stateCaps = stateData.getSkillData('stateCaps', None)
        if stateCaps:
            owner.buffCaps = None
            owner.fashion.autoSetStateCaps()

    def addFollowAct(self, sId, actions, hitPrefix, needForcePlay = False):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        if self.actLoopCallBack.get(sId, None):
            BigWorld.cancelCallback(self.actLoopCallBack[sId])
        owner.daoDiStartAction = None
        if owner.life == gametypes.LIFE_DEAD and not needForcePlay:
            return
        stateData = skillDataInfo.ClientSkillInfo(sId, 1, 1)
        stateActions = stateData.getSkillData('stateAct', 0)
        hitStateType = action.UNKNOWN_STATE
        if stateActions:
            hitStateType = stateActions[0][1]
        for saveStateId in self.stateActMap:
            saveId = saveStateId
            saveLv = 1
            stateData = skillDataInfo.ClientSkillInfo(saveId, saveLv, 1)
            saveActions = stateData.getSkillData('stateAct', 0)
            saveActions = saveActions[self.stateActMap[saveStateId]]
            gamelog.debug('addFollowAct:', hitStateType, saveActions[1], saveId, sId)
            if hitStateType <= saveActions[1] and saveId != sId:
                return

        if owner.life == gametypes.LIFE_ALIVE:
            for i in xrange(len(actions) - 1):
                owner.fashion.stopActionByName(owner.model, actions[i])

            owner.fashion.playAction(actions[-1:], getattr(action, hitPrefix + '_STOP_ACTION'))

    def __getDelStateActActions(self, stateId, needPop = True):
        owner = BigWorld.entity(self.ownerId)
        stateData = skillDataInfo.ClientSkillInfo(stateId, 1, 1)
        actions = stateData.getSkillData('stateAct', 0)
        idx = 0
        if actions:
            if needPop:
                idx = self._popActionGroup(stateId)
            elif self.stateActMap.has_key(stateId):
                idx = self.stateActMap[stateId]
            actions = actions[idx]
            actType = owner.fashion.getWeaponActType()
            actions = list(actions)
            if actions:
                for i in xrange(2, len(actions)):
                    if actions[i] != '':
                        actions[i] = str(actType) + actions[i]

        return actions

    def delStateAct(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if not owner or not owner.inWorld:
            return
        stateData = skillDataInfo.ClientSkillInfo(stateId, 1, 1)
        actions = stateData.getSkillData('stateAct', None)
        if not actions:
            return
        if owner.life == gametypes.LIFE_DEAD or owner.fashion.doingActionType() in [action.HIT_DIEFLY_ACTION]:
            actions = self.__getDelStateActActions(stateId)
            return
        actions = self.__getDelStateActActions(stateId)
        if owner.fashion.isPlayer:
            owner.model.yaw = BigWorld.dcursor().yaw
            owner.physics.userDirected = True
        if actions:
            hitStateType = actions[1]
            for saveStateId in self.stateActMap:
                saveId = saveStateId
                saveLv = 1
                stateData = skillDataInfo.ClientSkillInfo(saveId, saveLv, 1)
                saveActions = stateData.getSkillData('stateAct', 0)
                saveActions = saveActions[self.stateActMap[saveStateId]]
                if hitStateType == saveActions[1]:
                    totalTime = self._getStateLastTime(stateId)
                    saveTotalTime = self._getStateLastTime(saveId)
                    stateStartTime = saveStartTime = 0.0
                    if self.stateStartTimeMap.has_key(stateId):
                        stateStartTime = self.stateStartTimeMap[stateId]
                    if self.stateStartTimeMap.has_key(saveStateId):
                        saveStartTime = self.stateStartTimeMap[saveStateId]
                    keepTime = totalTime - (BigWorld.time() - stateStartTime)
                    savekeepTime = saveTotalTime - (BigWorld.time() - saveStartTime)
                    gamelog.debug('delStateAct', savekeepTime, keepTime)
                    if savekeepTime > keepTime:
                        return

            if owner.hitStateType > hitStateType:
                return
            stopActions = actions[2:-1]
            actQueue = owner.model.queue
            if len(actQueue) == 0:
                return
            for i in stopActions:
                if owner.fashion.doingActionType() in [ACT.MAN_DOWN_START_ACTION, ACT.MAN_DOWN_STOP_ACTION]:
                    continue
                owner.fashion.stopActionByName(owner.model, i)

            if not self.__updateHitStateAction(stateId):
                if not owner.am.moveNotifier:
                    owner.am.moveNotifier = owner.fashion.movingNotifier
                if owner.fashion.doingActionType() not in [ACT.JUMP_ACTION,
                 ACT.ROLL_ACTION,
                 ACT.ROLLSTOP_ACTION,
                 ACT.MAN_DOWN_START_ACTION,
                 ACT.MAN_DOWN_STOP_ACTION,
                 ACT.GUIDE_ACTION]:
                    owner.fashion.stopAllActions()

    def __updateHitStateAction(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        canFind = False
        maxHitStateType = action.UNKNOWN_STATE
        for saveStateId in self.stateActMap:
            stateData = skillDataInfo.ClientSkillInfo(saveStateId, 1, 1)
            actions = stateData.getSkillData('stateAct', 0)
            if actions:
                actions = actions[self.stateActMap[saveStateId]]
                actType = owner.fashion.getWeaponActType()
                actions = list(actions)
                for i in xrange(2, len(actions)):
                    if actions[i] != '':
                        actions[i] = str(actType) + actions[i]

                if not actions:
                    return canFind
                if canFind:
                    if maxHitStateType < actions[1]:
                        maxHitStateType = actions[1]
                else:
                    canFind = True
                    if self.actStopCallBack.has_key(saveStateId):
                        BigWorld.cancelCallback(self.actStopCallBack[saveStateId])
                        del self.actStopCallBack[saveStateId]
                    if self.actLoopCallBack.has_key(saveStateId):
                        BigWorld.cancelCallback(self.actLoopCallBack[saveStateId])
                        del self.actLoopCallBack[saveStateId]
                    owner.fashion.stopAction()
                    faintActionName = owner.fashion.getFaintActionName()
                    owner.fashion.playAction([faintActionName], action.FAINT_LOOP_ACTION)
                    maxHitStateType = actions[1]

        owner.hitStateType = maxHitStateType
        if not canFind:
            if self.actStopCallBack.has_key(stateId):
                BigWorld.cancelCallback(self.actStopCallBack[stateId])
                del self.actStopCallBack[stateId]
            if self.actLoopCallBack.has_key(stateId):
                BigWorld.cancelCallback(self.actLoopCallBack[stateId])
                del self.actLoopCallBack[stateId]
            owner.hitStateType = action.UNKNOWN_STATE
        return canFind

    def setBufActStateQingGongCaps(self):
        owner = BigWorld.entity(self.ownerId)
        if owner.IsAvatar and owner.bufActState and not owner.inRiding():
            if owner.skillPlayer.inWeaponBuff:
                if owner.inCombat:
                    owner.switchWeaponState(gametypes.WEAPON_DOUBLEATTACH)
                    if hasattr(owner, 'modelServer'):
                        owner.modelServer.setWeaponCaps()
                else:
                    owner.switchWeaponState(gametypes.WEAPON_HANDFREE, True, True)
            owner.am.matchCaps = [keys.CAPS_HAND_FREE, keys.CAPS_GROUND]

    def restoreBufActState(self):
        owner = BigWorld.entity(self.ownerId)
        if owner.IsAvatar and owner.bufActState and not owner.inRiding():
            if owner.skillPlayer.inWeaponBuff:
                owner.switchWeaponState(owner.skillPlayer.inWeaponBuff)
            owner.am.matchCaps = owner.bufActState
            if owner.buffModelScale:
                for stateId, data in owner.buffModelScale:
                    scale = data[0]
                    modelTypes = data[1]
                    for modelType in modelTypes:
                        if modelType != gameglobal.STATE_MODEL_SCALE_TYPE_BODY:
                            self._modelScale(stateId, owner, modelType, scale)

    def addChangeWeapon(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if owner.inRiding():
            return
        if not owner.inWorld or not owner.skillPlayer:
            return
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        weaponState = stateData.getSkillData('changeWeapon', None)
        if owner.IsAvatar and weaponState:
            owner.switchWeaponState(weaponState)
            owner.skillPlayer.inWeaponBuff = weaponState
            if not (hasattr(owner, '_isOnZaijuOrBianyao') and owner._isOnZaijuOrBianyao()):
                owner.bufActState = owner.am.matchCaps

    def delChangeWeapon(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        weaponState = stateData.getSkillData('changeWeapon', None)
        if owner.IsAvatar and weaponState:
            owner.bufActState = None
            owner.fashion.autoSetStateCaps()
            if owner.inCombat:
                owner.switchWeaponState(gametypes.WEAPON_DOUBLEATTACH)
                if hasattr(owner, 'modelServer'):
                    owner.modelServer.setWeaponCaps()
            else:
                owner.switchWeaponState(gametypes.WEAPON_HANDFREE, True, True)
            if owner.skillPlayer:
                owner.skillPlayer.inWeaponBuff = None
                owner.skillPlayer.endWeaponState = 0

    def addScreenEffect(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        if owner == BigWorld.player():
            stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
            se = stateData.getSkillData('screenEffect', 0)
            if se and (owner.getEffectLv() >= gameglobal.EFFECT_MID or screenEffect.canIgnoreSwitch(se)):
                screenEffect.startSkillEffect(gameglobal.EFFECT_TAG_STATE, se)

    def delScreenEffect(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        se = stateData.getSkillData('screenEffect', 0)
        if se and owner == BigWorld.player():
            screenEffect.delEffect(gameglobal.EFFECT_TAG_STATE)

    def addForceState(self, addSet, delSet):
        e = BigWorld.entity(self.ownerId)
        if not e:
            return
        newStateSet, deltaState = utils.getModifiedStates(e.statesOld, e.getStates()) if self.ownerId != BigWorld.player().id else utils.getModifiedStatesByStartTime(e.statesOld, e.getStates())
        newStateList = e.getStates().keys()
        for stateId in newStateSet:
            if self._isRefreshForced(stateId, 1):
                addSet.add(stateId)
            self._addForceWhenDependFx(stateId, newStateList, addSet)

        for stateId in deltaState:
            if stateId in const.ALL_SHOW_NEIYI_BUFF:
                delSet.add(stateId)
            self._addForceWhenDependFx(stateId, newStateList, delSet)

    def _addForceWhenDependFx(self, stateId, newStateList, addSet):
        for sid in newStateList:
            stateData = skillDataInfo.ClientSkillInfo(sid, 1, 1)
            if stateData and stateData.getSkillData('fxDependState', None):
                if stateData.getSkillData('fxDependState', None) == stateId:
                    addSet.add(sid)

    def _getStateFxIndepended(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        if not stateData:
            return
        fxDependState = stateData.getSkillData('fxDependState', None)
        e = BigWorld.entity(self.ownerId)
        newStateList = e.getStates().keys()
        if fxDependState:
            fx = []
            for i in xrange(0, newStateList.count(fxDependState)):
                efs = self._getFxByNum(stateData, i + 1)
                if efs:
                    fx.extend(efs)

            return fx
        else:
            return self._getFxByNum(stateData, 1)

    def _getAddedStateFx(self, stateId):
        e = BigWorld.entity(self.ownerId)
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, e)
        if not stateData:
            return
        fxDependState = stateData.getSkillData('fxDependState', None)
        newState = e.getStates()
        oldState = e.statesOld
        if self.forceUpdate:
            oldState = {}
        newStateList = newState.keys()
        oldStateList = oldState.keys()
        if stateId not in oldStateList:
            if fxDependState:
                fx = []
                for i in xrange(0, newStateList.count(fxDependState)):
                    efs = self._getFxByNum(stateData, i + 1)
                    if efs:
                        fx.extend(efs)

                return fx
            else:
                return self._getFxByNum(stateData, 1)
        else:
            if fxDependState:
                fx = []
                for i in xrange(oldStateList.count(fxDependState), newStateList.count(fxDependState)):
                    efs = self._getFxByNum(stateData, i + 1)
                    if efs:
                        fx.extend(efs)

                return fx
            return self._getFxByNum(stateData, 1)

    def _getDelStateFx(self, stateData, newStateList, oldStateList):
        if not stateData:
            return
        stateId = stateData.num
        fxDependState = stateData.getSkillData('fxDependState', None)
        if stateId not in newStateList:
            if fxDependState:
                fx = []
                for i in xrange(0, oldStateList.count(fxDependState)):
                    efs = self._getFxByNum(stateData, i + 1)
                    if efs:
                        fx.extend(efs)

                return fx
            else:
                return self._getFxByNum(stateData, 1)
        else:
            if fxDependState:
                fx = []
                for i in xrange(newStateList.count(fxDependState), oldStateList.count(fxDependState)):
                    efs = self._getFxByNum(stateData, i + 1)
                    if efs:
                        fx.extend(efs)

                return fx
            return self._getFxByNum(stateData, 1)

    def _isStateExist(self, stateId):
        e = BigWorld.entity(self.ownerId)
        return stateId in e.getStates()

    def _getFxByNum(self, stateData, num):
        if not stateData:
            return
        fxList = stateData.getSkillData('fx', [])
        if not fxList or num <= 0:
            return
        fxDependState = stateData.getSkillData('fxDependState', None)
        if fxDependState:
            if len(fxList) < num:
                return
            else:
                return fxList[num - 1]
        else:
            return fxList[0]

    def _isRefreshForced(self, sId, sLv):
        stateData = skillDataInfo.ClientSkillInfo(sId, sLv, 1)
        if stateData.hasSkillData('stateAct') or stateData.hasSkillData('startFx') or stateData.hasSkillData('stateTint') or stateData.hasSkillData('hitInAir') or stateData.hasSkillData('fx') or sId in const.ALL_SHOW_NEIYI_BUFF:
            return True
        else:
            return False

    def addHideLvSpan(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        hideLvSpan = stateData.getSkillData('hideLvSpan', 0)
        if hideLvSpan:
            owner.hideLvSpan = hideLvSpan

    def delHideLvSpan(self, stateId):
        owner = BigWorld.entity(self.ownerId)
        stateData = skillDataInfo.getBuffClientSkillInfo(stateId, owner)
        hideLvSpan = stateData.getSkillData('hideLvSpan', 0)
        if hideLvSpan:
            owner.hideLvSpan = gameglobal.DEFAULT_HIDE_LV_SPAN


class GradualScale(object):

    def __init__(self):
        self.startTime = 0
        self.keepTime = 0
        self.owner = None
        self.syncID = 0
        self.recallTime = 0.1
        self.modelScale = 1.0

    def getModelScale(self):
        return (self.modelScale, self.modelScale, self.modelScale)

    def startScale(self, ownerId, modelScale = 1.0, keepTime = 1.0, recallTime = 0.1):
        self.owner = BigWorld.entities.get(ownerId)
        self.modelScale = modelScale
        finalScale = self.getModelScale()
        currScale = tuple(self.owner.model.scale)
        if currScale == finalScale:
            return
        self.keepTime = keepTime
        self.startTime = time.clock()
        self.syncID += 1
        self.doScale(self.syncID)

    def doScale(self, syncId):
        if syncId != self.syncID:
            return
        if not self.owner.inWorld:
            self.owner = None
            return
        now = time.clock()
        fraction = (now - self.startTime) / self.keepTime
        currScale = self.owner.model.scale
        finalScale = self.getModelScale()
        diffScale = (finalScale[0] - currScale[0], finalScale[1] - currScale[1], finalScale[2] - currScale[2])
        if fraction < 1.0:
            self.owner.model.scale = (currScale[0] + fraction * diffScale[0], currScale[1] + fraction * diffScale[1], currScale[2] + fraction * diffScale[2])
            self.owner.resetTopLogo()
            BigWorld.callback(self.recallTime, Functor(self.doScale, self.syncID))
        else:
            self.owner.model.scale = finalScale
            self.owner.resetTopLogo()
            if BigWorld.player() == self.owner:
                self.owner.resetCamera()
            self.owner = None


EnterStateMap = {}
LeaveStateMap = {}

class HitFlyPointFlyer(object):

    def __init__(self, model, points = []):
        super(HitFlyPointFlyer, self).__init__()
        self.model = model
        self.mot = BigWorld.Rlauncher()
        self.model.addMotor(self.mot)
        self.points = points

    def start(self):
        if len(self.points) == 0:
            return
        point = self.points.pop(0)
        if point[4] > 0:
            BigWorld.callback(point[4], Functor(self._run, point))
        else:
            self._run(point)

    def _run(self, point):
        if not self.mot:
            return
        self.model.position = point[0]
        if point[1].__class__.__name__ in ('Vector3', 'tuple'):
            mat = Math.Matrix()
            mat.setTranslate(point[1])
        else:
            mat = point[1]
        self.mot.target = mat
        self.mot.speed = point[3]
        self.mot.curvature = 0.0
        self.mot.proximity = 0.0
        self.mot.acceleration = point[5]
        self.callback = point[2]
        self.mot.proximityCallback = Functor(self.approachPoint)

    def approachPoint(self):
        if self.callback:
            self.callback()
            self.callback = None
        self.start()

    def release(self):
        self.points = []
        if self.mot:
            self.model.delMotor(self.mot)
        self.mot = None
