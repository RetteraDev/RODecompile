#Embedded file name: /WORKSPACE/data/entities/client/helpers/impactionfashion.o
import random
import BigWorld
import Sound
import gametypes
import gameglobal
import gamelog
import action
import skillDataInfo
import const
import utils
import formula
from sfx import sfx
from sfx import screenEffect
from guis import hotkey as HK
from callbackHelper import Functor
from helpers import tintalt
from helpers import charRes
from data import skill_fx_data as SFD
from data import equip_data as ED
from data import interactive_basic_action_data as IBAD
from data import interactive_data as IAD
from data import foot_dust_data as FDD
effectKeepTimeMap = {}

class ActionSeq(object):

    def __init__(self):
        self.callback = None
        self.len = 0
        self.action = []
        self.active = True
        self.trigger = -1
        self.blend = False


class ActionSeqEx(ActionSeq):

    def __init__(self, parent):
        super(ActionSeqEx, self).__init__()
        self.actLinker = None
        self._parent = parent

    def next(self, actName, actType = action.UNKNOWN_ACTION, delay = 0, callback = None, ext = 0, scale = 1, keep = 0, blend = False):
        for act in self.action:
            act.stop()

        fashion = self._parent
        act = getattr(self.actLinker, actName, None)
        if act:
            fashion.doAction(act, actType, delay, callback, ext, scale, keep, blend)


class ImpActionFashion(object):

    def getActionNameList(self):
        if not getattr(self, 'action', None):
            return frozenset([])
        return self.action.actionList

    def getAttackAction(self):
        if getattr(self, 'action', None):
            name = self.action.getAttackAction(self)
            owner = BigWorld.entity(self.owner)
            if name != None and name in self.getActionNameList():
                return owner.model.action(name)

    def getAttackActionName(self):
        if getattr(self, 'action', None):
            return self.action.getAttackAction(self)

    def getHitFlyActionName(self):
        if getattr(self, 'action', None):
            return self.action.getHitFlyAction(self)

    def getLieBeHit(self):
        acts = []
        actionName = getattr(self.action, 'getLieHitAction')(self)
        if actionName in self.getActionNameList():
            acts.append(actionName)
        actionName = getattr(self.action, 'getLieHit1Action')(self)
        if actionName in self.getActionNameList():
            acts.append(actionName)
        return acts

    def getBeHitActionName(self, beHitType = gameglobal.NORMAL_HIT):
        owner = BigWorld.entity(self.owner)
        try:
            if getattr(owner, 'monsterInstance', False) and not owner.isAvatarMonster():
                return self.action.getBeHitAction(self, beHitType)
            if beHitType == gameglobal.LIE_HIT:
                acts = self.getLieBeHit()
                actionName = None
                if acts:
                    actionName = random.choice(acts)
                if actionName not in self.getActionNameList():
                    actionName = self.action.getBeHitAction(self)
                return actionName
            actionName = getattr(self.action, gameglobal.HIT_ACTION_MAP[beHitType])(self)
            if actionName not in self.getActionNameList():
                actionName = self.action.getBeHitAction(self)
            return actionName
        except:
            return

    def getAlphaBeHitActions(self):
        owner = BigWorld.entity(self.owner)
        retActions = []
        try:
            if getattr(owner, 'monsterInstance', False) and not owner.isAvatarMonster():
                return self.action.getAlphaBeHitActions()
            types = [gameglobal.FAINT_HIT,
             gameglobal.AVOID_HIT,
             gameglobal.BLOCK_HIT,
             gameglobal.FRONT_MID_LONG,
             gameglobal.BACK_MID_LONG,
             gameglobal.FRONT_MID_LONG_CRIT]
            for t in types:
                try:
                    action = getattr(self.action, gameglobal.HIT_ACTION_MAP[t])(self)
                    if action:
                        retActions.append(action)
                except:
                    pass

            return retActions
        except:
            return retActions

    def getPrefixStateAction(self):
        owner = BigWorld.entity(self.owner)
        try:
            if getattr(owner, 'monsterInstance', False):
                if self.action:
                    return self.action.getPrefixStateAction(self)
            elif self.action:
                return self.action.getPrefixStateAction(self)
        except:
            pass

        return '1'

    def getDeadActionName(self):
        if getattr(self, 'action', None):
            if self.dieActionGroupId:
                return self.action.getDeadAction(self)
            else:
                return self.action.getDead1Action(self)

    def getAllDeadAction(self):
        return [self.action.getDeadAction(self),
         self.action.getDead1Action(self),
         self.action.getDieAction(self),
         self.action.getDie1Action(self)]

    def doingDeadAction(self):
        owner = BigWorld.entity(self.owner)
        queue = owner.model.queue
        deadActions = self.getDeadActionName()
        if queue and deadActions:
            for ac in queue:
                if ac in deadActions:
                    return True

        return False

    def getDieActionName(self):
        if getattr(self, 'action', None):
            self.dieActionGroupId = random.randint(0, 1)
            if self.dieActionGroupId:
                return self.action.getDieAction(self)
            else:
                return self.action.getDie1Action(self)

    def getSummonActionName(self):
        if getattr(self, 'action', None):
            return self.action.getSummonAction(self)

    def getDyingDieActionName(self):
        if getattr(self, 'action', None):
            return self.action.getAction(self, 'dyingDieAct')

    def getDyingDeadActionName(self):
        if getattr(self, 'action', None):
            return self.action.getAction(self, 'dyingDeadAct')

    def getDyingBeHitActionName(self):
        if getattr(self, 'action', None):
            return self.action.getAction(self, 'dyingBeHitAct')

    def getDyingBeHitActionNameNormal(self):
        if getattr(self, 'action', None):
            return self.action.getAction(self, 'dyingBeHitActNormal')

    def getDyingStandupActionName(self):
        if getattr(self, 'action', None):
            return self.action.getAction(self, 'dyingStandupAct')

    def getInCombatStartActionName(self):
        if getattr(self, 'action', None):
            return self.action.getAction(self, 'inCombatStartAct')

    def getBornIdleActionName(self):
        if getattr(self, 'action', None):
            return self.action.getAction(self, 'bornIdleAct')

    def getLeaveBornActionName(self):
        if getattr(self, 'action', None):
            return self.action.getAction(self, 'leaveBornAct')

    def getForceBeHitActionName(self):
        owner = BigWorld.entity(self.owner)
        try:
            if getattr(owner, 'monsterInstance', False) and not owner.isAvatarMonster():
                return self.action.getRandomAction(self, 'forceBeHitAct')
            return self.action.getForceBeHitAction(self)
        except:
            return None

    def getTalkActionName(self):
        try:
            return self.action.getTalkAction()
        except:
            return None

    def getDieAction(self):
        if getattr(self, 'action', None):
            name = self.action.getDieAction(self)
            owner = BigWorld.entity(self.owner)
            if name != None and name in self.getActionNameList():
                return owner.model.action(name)

    def getHitDieFlyName(self):
        if getattr(self, 'action', None):
            return self.action.getHitDieFlyName(self)

    def getFlyBoredActionForIdleType(self):
        if self.idleType == gametypes.IDLE_TYPE_NORMAL:
            return [self.action.getFlyBored1Action(self)]
        if self.idleType == gametypes.IDLE_TYPE_RUN_STOP:
            return [self.action.getFlyBored2Action(self)]
        if self.idleType == gametypes.IDLE_TYPE_SPRINT_STOP:
            return [self.action.getFlyBored3Action(self)]
        return []

    def getHorseBoredActionForIdleType(self):
        if self.idleType == gametypes.IDLE_TYPE_NORMAL:
            return [self.action.getHorseBored1Action(self)]
        if self.idleType == gametypes.IDLE_TYPE_RUN_STOP:
            return [self.action.getHorseBored2Action(self)]
        if self.idleType == gametypes.IDLE_TYPE_SPRINT_STOP:
            return [self.action.getHorseBored3Action(self)]
        return []

    def getAvatarBoredActionNames(self):
        owner = BigWorld.entity(self.owner)
        enableIdlePlus = FDD.data.get(self.modelID, {}).get('enableIdlePlus')
        if owner.inRiding():
            if owner.inMoving():
                if owner.inFly:
                    if owner.qinggongState == gametypes.QINGGONG_ACT_DEFAULT:
                        return [self.action.getFlyRunBoredAction(self)]
                    else:
                        return [self.action.getFlySprintBoredAction(self)]
                elif owner.qinggongState == gametypes.QINGGONG_ACT_DEFAULT:
                    return [self.action.getHorseRunBoredAction(self)]
                else:
                    return [self.action.getHorseSprintsBoredAction(self)]

            elif owner.inFly:
                if enableIdlePlus:
                    return self.getFlyBoredActionForIdleType()
                return [self.action.getFlyBoredAction(self)]
            elif enableIdlePlus:
                return self.getHorseBoredActionForIdleType()
            else:
                return [self.action.getHorseBoredAction(self)]
        else:
            if hasattr(owner, 'inInteractiveObject') and owner.inInteractiveObject():
                return self.getInteractiveSpecialIdle()
            if owner.inMoving():
                if owner.inFly:
                    if owner.qinggongState == gametypes.QINGGONG_ACT_DEFAULT:
                        return [self.action.getFlyRunBoredAction(self)]
                    else:
                        return [self.action.getFlySprintBoredAction(self)]
            else:
                if owner.inFly:
                    return [self.action.getFlyBoredAction(self)]
                if owner.inFishing():
                    return [self.action.getFishingBoredAction(self)]
                return [self.action.getBoredAction(self)]

    def getInteractiveSpecialIdle(self):
        owner = BigWorld.entity(self.owner)
        if hasattr(owner, 'inInteractiveObject') and owner.inInteractiveObject():
            interObj = BigWorld.entities.get(owner.interactiveObjectEntId, None)
            if interObj and interObj.inWorld:
                interBasicActionId = IAD.data.get(interObj.objectId, {}).get('interactiveActionId', None)
                specialIdleAction = IBAD.data.get(interBasicActionId, {}).get('specialIdleAction')
                if specialIdleAction:
                    return specialIdleAction
                else:
                    return

    def getInteractiveSpecialIdleChatId(self):
        owner = BigWorld.entity(self.owner)
        if hasattr(owner, 'inInteractiveObject') and owner.inInteractiveObject():
            interObj = BigWorld.entities.get(owner.interactiveObjectEntId, None)
            if interObj and interObj.inWorld:
                interBasicActionId = IAD.data.get(interObj.objectId, {}).get('interactiveActionId', None)
                specialIdleChatId = IBAD.data.get(interBasicActionId, {}).get('specialIdleChatId')
                if specialIdleChatId:
                    return specialIdleChatId
                else:
                    return

    def getInteractiveSpecialIdleEmote(self):
        owner = BigWorld.entity(self.owner)
        if hasattr(owner, 'inInteractiveObject') and owner.inInteractiveObject():
            interObj = BigWorld.entities.get(owner.interactiveObjectEntId, None)
            if interObj and interObj.inWorld:
                interBasicActionId = IAD.data.get(interObj.objectId, {}).get('interactiveActionId', None)
                specialIdleEmote = IBAD.data.get(interBasicActionId, {}).get('specialIdleEmote')
                if specialIdleEmote:
                    return specialIdleEmote
                else:
                    return

    def getBoredActionNames(self):
        owner = BigWorld.entity(self.owner)
        if getattr(self, 'action', None):
            if getattr(owner, 'avatarInstance', None):
                return self.getAvatarBoredActionNames()
            if owner.isAvatarMonster():
                return [self.action.getBoredAction(self)]
            if utils.instanceof(owner, 'MultiplayMovingPlatform'):
                return owner.getBoredActionNames()
            boredAction = None
            try:
                boredAction = self.action.getBoredAction(self)
                return boredAction
            except:
                return boredAction

    def getRushStartAction(self):
        owner = BigWorld.entity(self.owner)
        if getattr(self, 'action', None):
            if owner.qinggongState == gametypes.QINGGONG_STATE_FAST_SLIDING:
                acttionName = 'getRushStart' + str(self.rushActionIndex) + 'Action'
                return getattr(self.action, acttionName)(self)
            if owner.qinggongState == gametypes.QINGGONG_STATE_FAST_SLIDING_WEAPON_IN_HAND:
                acttionName = 'getRushStartWeaponInHandAction'
                return getattr(self.action, acttionName)(self)

    def getRushAction(self):
        owner = BigWorld.entity(self.owner)
        if getattr(self, 'action', None):
            if owner.qinggongState == gametypes.QINGGONG_STATE_FAST_SLIDING:
                acttionName = 'getRush' + str(self.rushActionIndex) + 'Action'
                return getattr(self.action, acttionName)(self)
            if owner.qinggongState == gametypes.QINGGONG_STATE_FAST_SLIDING_WEAPON_IN_HAND:
                acttionName = 'getRushWeaponInHandAction'
                return getattr(self.action, acttionName)(self)

    def getRushEndAction(self):
        owner = BigWorld.entity(self.owner)
        if getattr(self, 'action', None):
            if owner.qinggongState == gametypes.QINGGONG_STATE_RUSH_DOWN:
                acttionName = 'getRushEnd' + str(self.rushActionIndex) + 'Action'
                return getattr(self.action, acttionName)(self)
            if owner.qinggongState == gametypes.QINGGONG_STATE_RUSH_DOWN_WEAPON_IN_HAND:
                acttionName = 'getRushEndWeaponInHandAction'
                return getattr(self.action, acttionName)(self)

    def getRushEndDownAction(self):
        owner = BigWorld.entity(self.owner)
        if getattr(self, 'action', None):
            if owner.qinggongState == gametypes.QINGGONG_STATE_RUSH_DOWN:
                acttionName = 'getRushEndDown' + str(self.rushActionIndex) + 'Action'
                return getattr(self.action, acttionName)(self)
            if owner.qinggongState == gametypes.QINGGONG_STATE_RUSH_DOWN_WEAPON_IN_HAND:
                acttionName = 'getRushEndDownWeaponInHandAction'
                return getattr(self.action, acttionName)(self)

    def getHorseFallRunDownAction(self):
        if getattr(self, 'action', None):
            return getattr(self.action, 'getHorseFallRunDownAction')(self)

    def getWingFlyRushStartAction(self):
        owner = BigWorld.entity(self.owner)
        if getattr(self, 'action', None):
            if not owner.inFly:
                return self.action.getWingNoFlyRushStartAction(self)
            if owner.isInCoupleRide():
                return
            return self.action.getWingFlyRushStartAction(self)

    def getWingFlyLeftStartAction(self):
        owner = BigWorld.entity(self.owner)
        if getattr(self, 'action', None):
            if owner.isInCoupleRide():
                return
            return self.action.getWingFlyLeftStartAction(self)

    def getWingFlyRightStartAction(self):
        owner = BigWorld.entity(self.owner)
        if getattr(self, 'action', None):
            if owner.isInCoupleRide():
                return
            return self.action.getWingFlyRightStartAction(self)

    def getWingFlyBackStartAction(self):
        owner = BigWorld.entity(self.owner)
        if getattr(self, 'action', None):
            if owner.isInCoupleRide():
                return
            return self.action.getWingFlyBackStartAction(self)

    def getWingFlyDownStartAction(self):
        owner = BigWorld.entity(self.owner)
        if getattr(self, 'action', None):
            if owner.isInCoupleRide():
                return
            return self.action.getWingFlyDownStartAction(self)

    def getEnterHorseAction(self):
        owner = BigWorld.entity(self.owner)
        if getattr(self, 'action', None):
            actionName = self.action.getEnterHorseAction(self)
            if actionName and owner == BigWorld.player():
                equip = BigWorld.player().equipment[gametypes.EQU_PART_RIDE]
                if equip:
                    eId = equip.id
                    if owner.bianshen:
                        eId = owner.bianshen[1]
                    idx = ED.data.get(eId, {}).get('horseWingActionIdx', None)
                    if idx:
                        return str(idx) + actionName
                return actionName
            return actionName

    def getEnterHorseMountAction(self):
        owner = BigWorld.entity(self.owner)
        if getattr(self, 'action', None):
            actionName = self.action.getEnterHorseMountAction(self)
            if actionName and owner == BigWorld.player():
                equip = BigWorld.player().equipment[gametypes.EQU_PART_RIDE]
                if equip:
                    eId = equip.id
                    if owner.bianshen:
                        eId = owner.bianshen[1]
                    idx = ED.data.get(eId, {}).get('horseWingActionIdx', None)
                    if idx:
                        return str(idx) + actionName
                return actionName
            return actionName

    def getHorseEnterHorseAction(self):
        if getattr(self, 'action', None):
            actionName = self.action.getHorseEnterHorseAction(self)
            return actionName

    def getLeaveHorseAction(self):
        owner = BigWorld.entity(self.owner)
        if getattr(self, 'action', None):
            actionName = self.action.getLeaveHorseAction(self)
            if actionName and owner == BigWorld.player():
                equip = BigWorld.player().equipment[gametypes.EQU_PART_RIDE]
                if equip:
                    idx = ED.data.get(equip.id, {}).get('horseWingActionIdx', None)
                    if idx:
                        return str(idx) + actionName
                return actionName
            return actionName

    def getStraightToLeftAction(self):
        if getattr(self, 'action', None):
            try:
                owner = BigWorld.entity(self.owner)
                if owner.inFly:
                    actionName = self.action.getFlyStraightToLeftAction(self)
                else:
                    actionName = self.action.getStraightToLeftAction(self)
                return actionName
            except:
                return

    def getStraightToRightAction(self):
        if getattr(self, 'action', None):
            try:
                owner = BigWorld.entity(self.owner)
                if owner.inFly:
                    actionName = self.action.getFlyStraightToRightAction(self)
                else:
                    actionName = self.action.getStraightToRightAction(self)
                return actionName
            except:
                return

    def getLeftToRightAction(self):
        if getattr(self, 'action', None):
            try:
                owner = BigWorld.entity(self.owner)
                if owner.inFly:
                    actionName = self.action.getFlyLeftToRightAction(self)
                else:
                    actionName = self.action.getLeftToRightAction(self)
                return actionName
            except:
                return

    def getRightToLeftAction(self):
        if getattr(self, 'action', None):
            try:
                owner = BigWorld.entity(self.owner)
                if owner.inFly:
                    actionName = self.action.getFlyRightToLeftAction(self)
                else:
                    actionName = self.action.getRightToLeftAction(self)
                return actionName
            except:
                return

    def getLandToFlyAction(self):
        if getattr(self, 'action', None):
            try:
                actionName = self.action.getLandToFlyAction(self)
                return actionName
            except:
                return

    def getFlyToLandAction(self):
        if getattr(self, 'action', None):
            try:
                actionName = self.action.getFlyToLandAction(self)
                return actionName
            except:
                return

    def getLeftToStraightAction(self):
        if getattr(self, 'action', None):
            try:
                owner = BigWorld.entity(self.owner)
                if owner.inFly:
                    actionName = self.action.getFlyLeftToStraightAction(self)
                else:
                    actionName = self.action.getLeftToStraightAction(self)
                return actionName
            except:
                return

    def getRightToStraightAction(self):
        if getattr(self, 'action', None):
            try:
                owner = BigWorld.entity(self.owner)
                if owner.inFly:
                    actionName = self.action.getFlyRightToStraightAction(self)
                else:
                    actionName = self.action.getRightToStraightAction(self)
                return actionName
            except:
                return

    def getStartToRunLeftAction(self):
        if getattr(self, 'action', None):
            return self.action.getStartToRunLeftAction(self)

    def getStartToRunAction(self):
        owner = BigWorld.entity(self.owner)
        startToRun = None
        if getattr(self, 'action', None):
            try:
                if owner.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
                    startToRun = self.action.getHorseStartToRunAction(self)
            except:
                pass

        return startToRun

    def getStartToRunRightAction(self):
        if getattr(self, 'action', None):
            return self.action.getStartToRunRightAction(self)

    def getRunToIdleAction(self):
        if getattr(self, 'action', None):
            owner = BigWorld.entity(self.owner)
            if owner.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
                horseDashStopAction = self.action.getHorseRunToIdleAction(self)
                return horseDashStopAction
            else:
                return self.action.getRunToIdleAction(self)

    def getNormalFlyUpStartAction(self):
        if getattr(self, 'action', None):
            return self.action.getNormalFlyUpStartAction(self)

    def getNormalFlyDownStartAction(self):
        if getattr(self, 'action', None):
            return self.action.getNormalFlyDownStartAction(self)

    def getNormalFlyLeftStartAction(self):
        if getattr(self, 'action', None):
            return self.action.getNormalFlyLeftStartAction(self)

    def getNormalFlyRightStartAction(self):
        if getattr(self, 'action', None):
            return self.action.getNormalFlyRightStartAction(self)

    def getNormalFlyForwardStartAction(self):
        if getattr(self, 'action', None):
            return self.action.getNormalFlyForwardStartAction(self)

    def getNormalFlyBackwardStartAction(self):
        if getattr(self, 'action', None):
            return self.action.getNormalFlyBackwardStartAction(self)

    def getHorseWingActionKey(self, actName):
        idx = self.getHorseWingActionIdx()
        if not idx:
            return actName
        if not actName:
            return actName
        return str(idx) + actName

    def getNormalHorseLeftStartAction(self):
        if getattr(self, 'action', None):
            return self.action.getNormalHorseLeftStartAction(self)

    def getNormalHorseRightStartAction(self):
        if getattr(self, 'action', None):
            return self.action.getNormalHorseRightStartAction(self)

    def getNormalHorseForwardStartAction(self):
        if getattr(self, 'action', None):
            return self.action.getNormalHorseForwardStartAction(self)

    def getNormalHorseBackwardStartAction(self):
        if getattr(self, 'action', None):
            return self.action.getNormalHorseBackwardStartAction(self)

    def getFaintActionName(self):
        if getattr(self, 'action', None):
            return self.action.getFaintAction(self)

    def getPickActionName(self):
        owner = BigWorld.entity(self.owner)
        if owner.inRiding():
            modelId = charRes.transBodyType(owner.physique.sex, owner.physique.bodyType)
            actionGroup = action.getActionGroup(modelId)
            return actionGroup.getPickItemAction(self)
        else:
            return self.action.getPickItemAction(self)

    def _pushSeq(self, seq):
        self.actionKey += 1
        key = self.actionKey
        if self.playedAction.get(key, None) == None:
            self.playedAction[key] = seq
            return key
        else:
            gamelog.error('Error:zf:_pushSeq, key already exists')
            return 0

    def playSingleAction(self, actName, actType = action.UNKNOWN_ACTION, delay = 0, callback = None, ext = 0, scale = 1, keep = 0, blend = False):
        if self.modelID == 0 or actName is None:
            return
        self._releaseFx()
        owner = BigWorld.entity(self.owner)
        try:
            act = owner.model.action(actName)
        except:
            if callback != None:
                callback()
            return

        return self.doAction(act, actType, delay, callback, ext, scale, keep, blend)

    def doAction(self, act, actType = action.UNKNOWN_ACTION, delay = 0, callback = None, ext = 0, scale = 1, keep = 0, blend = False):
        owner = BigWorld.entity(self.owner)
        seq = ActionSeq()
        seq.callback = callback
        seq.len = 1
        seq.action = [act]
        seq.blend = blend
        key = self._pushSeq(seq)
        if key == 0:
            return None
        self.setDoingActionType(actType)
        if act.blended:
            act.enableAlpha(blend and (owner.inMoving() or getattr(owner, 'inFly', False)))
        try:
            act(delay, Functor(globalActionComplete, self, key), ext, scale, keep)
        except:
            owner = BigWorld.entity(self.owner)
            gamelog.error('bgf:doAction error', delay, Functor(globalActionComplete, self, key), ext, scale, keep, owner.model.sources)
            BigWorld.callback(0, Functor(globalActionComplete, self, key))
            return None

        self.doingActionCount += 1
        return act

    def playAction(self, actions, actType = action.UNKNOWN_ACTION, callback = None, trigger = -1, blend = False, promote = False, scale = 1.0, keep = 0, targetPos = None):
        owner = BigWorld.entity(self.owner)
        if self.modelID == 0 or actions == None or len(actions) <= 0:
            if callback:
                BigWorld.callback(0, callback)
            return
        self._releaseFx()
        seq = ActionSeq()
        seq.callback = callback
        seq.len = len(actions)
        seq.action = []
        seq.trigger = trigger
        seq.blend = blend
        key = self._pushSeq(seq)
        if key == 0:
            return
        self.setDoingActionType(actType)
        self.doingActionCount += seq.len
        try:
            self.__nextAction(owner, list(actions), key, None, blend, promote, scale, keep, targetPos)
        except:
            gamelog.error('ERROR:zf:play action except ', owner, actions, key, owner.model.sources, owner.roleName)
            self._actionComplete(key)

    def initAction(self):
        self.doingActionCount = 0
        self.setDoingActionType(action.UNKNOWN_ACTION)
        self.playedAction = {}

    def __nextAction(self, owner, actions, key, curAct = None, blend = False, promote = False, scale = 1.0, keep = 0, targetPos = None):
        if len(actions) == 0:
            if curAct.blended:
                curAct.enableAlpha(blend and owner.inMoving() or getattr(owner, 'inFly', 0))
            curAct(0, Functor(globalActionComplete, self, key), promote, scale, keep, targetPos)
            return
        act = actions.pop(0)
        if None == curAct:
            actObj = owner.model.action(act)
        else:
            seq = self.playedAction[key]
            if curAct.blended:
                curAct.enableAlpha(blend and owner.inMoving() or getattr(owner, 'inFly', 0))
            if seq.trigger == seq.len - len(actions) - 2:
                link = curAct(0, seq.callback, promote)
            else:
                link = curAct()
            actObj = getattr(link, act)
        if actObj:
            self.playedAction[key].action.append(actObj)
            self.__nextAction(owner, actions, key, actObj, blend, promote, scale, keep, targetPos)

    def _actionComplete(self, key):
        owner = BigWorld.entity(self.owner)
        if not owner:
            return
        try:
            for act in self.playedAction[key].action:
                self._stopCueSoundAndEffect(act.name)

            seq = self.playedAction.pop(key)
            if not owner.model.hasPlayAction():
                owner.model.unlockSpine()
        except KeyError:
            if owner.model:
                owner.model.unlockSpine()
            return

        self.doingActionCount -= seq.len
        if self.doingActionCount <= 0:
            self.doingActionCount = 0
        if self.doingActionCount == 0:
            self._doingActionType = action.UNKNOWN_ACTION
        if seq.callback != None and seq.trigger == -1:
            seq.callback()
        owner = BigWorld.entity(self.owner)
        if self.isPlayer:
            if owner.schedule != None:
                owner.schedule()
            owner.schedule = None
        if owner:
            owner.am.fuse = 0

    def breakModelHitFreeze(self):
        owner = BigWorld.entity(self.owner)
        if not owner:
            return
        if owner.model.freezeTime > 0:
            if getattr(owner.model, 'freezeType', None) == gameglobal.FREEZE_TYPE_HIT:
                owner.updateModelFreeze(-1.0)

    def breakModelMoveFreeze(self):
        owner = BigWorld.entity(self.owner)
        if not owner:
            return
        if owner.model.freezeTime > 0:
            if getattr(owner.model, 'freezeType', None) == gameglobal.FREEZE_TYPE_MOVE:
                owner.updateModelFreeze(-1.0)

    def inStateAction(self):
        return self.doingActionType() in (action.FUKONG_START_ACTION,
         action.FUKONG_LOOP_ACTION,
         action.FUKONG_STOP_ACTION,
         action.TIAOGAO_START_ACTION,
         action.TIAOGAO_LOOP_ACTION,
         action.TIAOGAO_STOP_ACTION,
         action.JIDAO_START_ACTION,
         action.JIDAO_LOOP_ACTION,
         action.JIDAO_STOP_ACTION,
         action.FAINT_START_ACTION,
         action.FAINT_LOOP_ACTION,
         action.FAINT_STOP_ACTION)

    def playActionWithFx(self, actions, actType, callback = None, blend = False, targetPos = 0, keep = 0, priority = 1, extraInfo = {}):
        if self.modelID == 0 or actions == None or len(actions) <= 0:
            return
        self._releaseFx()
        self.setDoingActionType(actType)
        owner = BigWorld.entity(self.owner)
        if hasattr(owner, 'clearFreezeAct'):
            owner.clearFreezeAct()
        owner.clearFreezeEffect()
        seq = ActionSeq()
        seq.callback = callback
        seq.len = len(actions)
        seq.action = []
        seq.blend = blend
        key = self._pushSeq(seq)
        if key == 0:
            return
        self.doingActionCount += seq.len
        try:
            p = BigWorld.player()
            scale = 1.0
            if not owner.IsSummonedSprite:
                scale = owner.getCombatSpeedIncreseRatio()
            elif owner.IsSummonedSprite and extraInfo:
                affectedBySpriteCombatSpeedIncrease = extraInfo.get('affectedBySpriteCombatSpeedIncrease', None)
                scale = affectedBySpriteCombatSpeedIncrease if affectedBySpriteCombatSpeedIncrease else 1.0
            if p.inFubenType(const.FB_TYPE_BATTLE_FIELD_DOTA) and hasattr(owner, 'bfDotaNormalAttackSpeedIncreseRatio'):
                scale += owner.bfDotaNormalAttackSpeedIncreseRatio
            self.__nextActionFx(owner, list(actions), key, None, 0, scale, blend, targetPos, keep, priority, extraInfo)
        except:
            gamelog.error('playActionWithFx:ERROR:play action fx except 1 ', owner.id, actions, key, owner.model.sources)
            self._actionComplete(key)

    def inMoving(self):
        if self.doingActionType() not in [action.GUIDESTOP_ACTION,
         action.MOVINGSTOP_ACTION,
         action.AFTERMOVESTOP_ACTION,
         action.CASTSTOP_ACTION]:
            return False
        if self.isPlayer:
            return HK.HKM[HK.KEY_FORWARD].isAnyDown() or HK.HKM[HK.KEY_BACKWARD].isAnyDown() or HK.HKM[HK.KEY_MOVERIGHT].isAnyDown() or HK.HKM[HK.KEY_MOVELEFT].isAnyDown()
        return False

    def __nextActionFx(self, owner, actions, key, curAct = None, moveType = 0, scale = 1.0, blend = False, targetPos = 0, keep = 0, priority = 1, extraInfo = {}):
        if len(actions) <= 0:
            curAct.enableDummyTrack(not (owner.inMoving() or self.inMoving()) and not getattr(owner, 'inFly', 0))
            curAct.enableAlpha(blend and (owner.inMoving() or self.inMoving()) or getattr(owner, 'inFly', 0))
            curAct.needBlendOutTime(False)
            if owner.IsSummonedSprite and extraInfo:
                affectedBySpriteCombatSpeedIncrease = extraInfo.get('affectedBySpriteCombatSpeedIncrease', None)
                scale = affectedBySpriteCombatSpeedIncrease if affectedBySpriteCombatSpeedIncrease else 1.0
            curAct(0, Functor(globalActionComplete, self, key), moveType, scale, keep)
            return
        pair = actions.pop(0)
        sizeScale = pair[6] if len(pair) >= 7 else 1.0
        realPair4 = pair[4]
        if curAct == None:
            actObj = owner.model.action(pair[0])
            if owner.inMoving() and getattr(actObj, 'needLockSpine', False):
                owner.model.lockSpine()
            else:
                owner.model.unlockSpine()
            actObj.needBlendOutTime(False)
            actObj.enableDummyTrack(not owner.inMoving() and not getattr(owner, 'inFly', 0))
            self.__actionCallback(owner.id, owner.model, pair[0], pair[1], pair[2], pair[5], key, targetPos, priority, pair[4], sizeScale)
        else:
            curAct.enableDummyTrack(not owner.inMoving() and not getattr(owner, 'inFly', 0))
            curAct.enableAlpha(blend and owner.inMoving() or getattr(owner, 'inFly', 0))
            curAct.needBlendOutTime(False)
            if not owner.IsSummonedSprite:
                realPair4 = owner.getCombatSpeedIncreseRatio()
            elif owner.IsSummonedSprite and extraInfo:
                affectedBySpriteCombatSpeedIncrease = extraInfo.get('affectedBySpriteCombatSpeedIncrease', None)
                realPair4 = affectedBySpriteCombatSpeedIncrease if affectedBySpriteCombatSpeedIncrease else 1.0
            p = BigWorld.player()
            if p.inFubenType(const.FB_TYPE_BATTLE_FIELD_DOTA) and owner.bfDotaNormalAttackSpeedIncreseRatio:
                realPair4 += owner.bfDotaNormalAttackSpeedIncreseRatio
            link = curAct(0, Functor(self.__actionCallback, owner.id, owner.model, pair[0], pair[1], pair[2], pair[5], key, targetPos, priority, realPair4, sizeScale), moveType, realPair4)
            curAct.needBlendOutTime(False)
            link.enableDummyTrack(not owner.inMoving() and not getattr(owner, 'inFly', 0))
            actObj = getattr(link, pair[0])
            actObj.needBlendOutTime(False)
            actObj.enableDummyTrack(not owner.inMoving() and not getattr(owner, 'inFly', 0))
        self.playedAction[key].action.append(actObj)
        self.__nextActionFx(owner, actions, key, actObj, pair[3], realPair4, blend, targetPos, keep, priority, extraInfo)

    def __actionCallback(self, entityId, where, act, fx, actType, tintData, key, targetPos = 0, priority = 1, scale = 1.0, sizeScale = 1.0):
        if self.playedAction.has_key(key) and self.playedAction[key].active:
            self._actionSetActionType(actType, act)
            self.__actionFx(entityId, where, act, fx, key, targetPos, priority, scale, sizeScale)
            self.__actionTintFx(tintData)

    def __actionTintFx(self, tintData):
        owner = BigWorld.entity(self.owner)
        if not tintData or not owner:
            return
        if owner.getEffectLv() < gameglobal.EFFECT_MID:
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
        if tintName and self.isPlayer:
            tintalt.ta_add(allModels, tintName, [tint, BigWorld.shaderTime()], gameglobal.SKILLTINT_TIME, None, False, False, owner, owner, tintType=tintalt.SKILLTINT)
        else:
            tintalt.ta_addHitGaoLiang(allModels, gameglobal.HIT_HIGHLIGHT_BEGINTIME, gameglobal.SKILLTINT_TIME, gameglobal.HIT_HIGHLIGHT_ENDTIME, tint, owner, owner)
        owner.tintStateType[0] = tintPrio
        owner.tintStateType[1] = tintName
        if tintName:
            self.playedTintFx.append((allModels, tintName, tintPrio))
        else:
            self.playedTintFx.append((allModels, tint, tintPrio))

    def _actionSetActionType(self, actType, actionName = None):
        owner = BigWorld.entity(self.owner)
        if not owner:
            return
        self.setDoingActionType(actType)
        if owner.IsMonster:
            return
        if actType in [action.ROLLSTOP_ACTION, action.CASTSTOP_ACTION, action.LEAVE_HORSE_END_ACTION]:
            if owner.inMoving() and actType != action.CASTSTOP_ACTION and actionName in owner.model.queue:
                self.stopActionByName(owner.model, actionName)
            if getattr(owner, 'castSkillBusy', None):
                owner.castSkillBusy = False
            if self.isPlayer:
                owner.updateActionKeyState()

    def __actionFx(self, entityId, where, act, fx, key, targetPos = 0, priority = 1, scale = 1.0, sizeScale = 1.0):
        seq = self.playedAction.get(key, None)
        if seq == None or seq.active == False:
            return
        self._releaseFx()
        if fx != None:
            isFiller = where.action(act).filler
            fxs = self._attachFx(entityId, where, fx, isFiller, targetPos, priority, scale, sizeScale)
            self.playedFx.extend(fxs)

    def freezeEffect(self, freezeTime):
        for fx in self.freezedEffs:
            if fx:
                fx.pause(freezeTime)

    def clearFreezeEffect(self):
        if self.freezedEffs:
            for eff in self.freezedEffs:
                if eff:
                    eff.pause(0)

        self.freezedEffs = []

    def stopAction(self):
        owner = BigWorld.entity(self.owner)
        if not owner or self._doingActionType == action.DEAD_ACTION and owner.life == gametypes.LIFE_DEAD or self._doingActionType == action.HIT_DIEFLY_ACTION:
            return
        if self._doingActionType in (action.SHOW_WEAPON_ACTION, action.HANG_WEAPON_ACTION) and self.weaponCallback:
            BigWorld.cancelCallback(self.weaponCallback[0])
            self.weaponCallback[1]()
            self.weaponCallback = None
        if getattr(owner.modelServer, 'rightWeaponModel', None):
            owner.modelServer.rightWeaponModel.detachRightToLeft()
        if self._doingActionType in (action.SOCIAL_ACTION,):
            if hasattr(owner, 'emoteActionDone'):
                owner.emoteActionDone()
        temp = self.playedAction.keys()
        for key in temp:
            self.playedAction[key].callback = None
            if owner.model.freezeTime <= 0:
                for act in self.playedAction[key].action:
                    actName = None
                    try:
                        act.stop()
                        actName = act.name
                    except:
                        pass

                    self._stopCueSoundAndEffect(actName)

            self.playedAction[key].active = False

        if owner == BigWorld.player():
            if hasattr(owner, 'physics') and owner.physics:
                owner.physics.keepJumpVelocity = False
            owner.setRightMouseAble(True)
            screenEffect.delEffect(gameglobal.EFFECT_TAG_CAST_SKILL)
        if owner.model and hasattr(owner.model, 'unlockSpine'):
            owner.model.unlockSpine()
        self._releaseFx()
        self._doingActionType = action.UNKNOWN_ACTION
        owner.inWingTakeOff = False

    def _stopCueSoundAndEffect(self, actionName):
        if self.cueSound.has_key(actionName):
            for handle in self.cueSound.get(actionName, []):
                Sound.stopFx(handle)

            del self.cueSound[actionName]
        if self.cueVoice.has_key(actionName):
            for handle in self.cueVoice.get(actionName, []):
                Sound.stopVoice(handle)

            del self.cueVoice[actionName]
        if self.cueEffect.has_key(actionName):
            for fxs in self.cueEffect.get(actionName, []):
                gamelog.debug('zrz:', '_stopEffect', actionName, fxs)
                sfx.detachEffect(None, None, fxs)

            del self.cueEffect[actionName]

    def _attachFx(self, entityId, model, effects, isFiller, targetPos = 0, priority = 1, scale = 1.0, sizeScale = 1.0):
        keepTime = gameglobal.EFFECT_LAST_TIME
        retList = []
        ent = BigWorld.entity(entityId)
        if ent:
            for fx in effects:
                if sfx.effectKeepTimeMap.has_key(fx):
                    keepTime = sfx.effectKeepTimeMap[fx]
                elif isFiller:
                    keepTime = -1.0
                else:
                    keepTime = sfx.getModelKeepFx(fx)
                if hasattr(ent, 'inCombat') and ent.inCombat:
                    effectLv = ent.getSkillEffectLv()
                else:
                    effectLv = ent.getBasicEffectLv()
                mist = sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (effectLv,
                 priority,
                 model,
                 fx,
                 sfx.EFFECT_LIMIT,
                 keepTime,
                 targetPos))
                if mist != None:
                    if hasattr(mist[0], 'playRate'):
                        mist[0].playRate(scale)
                    if sizeScale != 1.0:
                        for fx in mist:
                            if hasattr(fx, 'scale'):
                                fx.scale(sizeScale)

                    retList.append([mist, fx])
                    self.freezedEffs.extend(mist)

        return retList

    def playActionSequence(self, model, actions, callback, scale = 1, keep = 0, blend = 0, releaseFx = True):
        owner = BigWorld.entity(self.owner)
        if not owner:
            return
        if len(actions) == 0 or not model or not model.inWorld:
            return
        if not owner.IsSummonedSprite:
            scale = owner.getCombatSpeedIncreseRatio()
        p = BigWorld.player()
        if gameglobal.rds.GameState == gametypes.GS_PLAYGAME and p.inFubenType(const.FB_TYPE_BATTLE_FIELD_DOTA) and hasattr(owner, 'bfDotaNormalAttackSpeedIncreseRatio'):
            scale += owner.bfDotaNormalAttackSpeedIncreseRatio
        if releaseFx:
            self._releaseFx()
        try:
            act = model.action(actions[0])
            if act.blended:
                act.enableAlpha(blend and (owner.inMoving() or owner.inRiding()))
        except:
            return

        for i in xrange(len(actions) - 1):
            if act != None:
                try:
                    act = getattr(act(0, None, 0, scale, keep), actions[i + 1])
                    if act.blended:
                        act.enableAlpha(blend and (owner.inMoving() or owner.inRiding()))
                except:
                    return

        if act != None:
            act(0, callback, 0, scale, keep)

    def playActionSequence2(self, model, actions, actType = action.UNKNOWN_ACTION, scale = 1, keep = 0, blend = 0):
        owner = BigWorld.entity(self.owner)
        if not owner or not model:
            return
        if len(actions) == 0 or not model.inWorld:
            return
        self._releaseFx()
        if not owner.IsSummonedSprite:
            scale = owner.getCombatSpeedIncreseRatio()
        p = BigWorld.player()
        if p.inFubenType(const.FB_TYPE_BATTLE_FIELD_DOTA) and hasattr(owner, 'bfDotaNormalAttackSpeedIncreseRatio'):
            scale += owner.bfDotaNormalAttackSpeedIncreseRatio
        self.setDoingActionType(actType)
        seq = ActionSeq()
        seq.len = len(actions)
        seq.action = []
        seq.blend = blend
        key = self._pushSeq(seq)
        if key == 0:
            return
        self.doingActionCount += seq.len
        try:
            pair = actions[0]
            act = model.action(pair[0])
            act.enableAlpha(blend)
        except:
            self._actionComplete(key)
            self._actionSetActionType(action.UNKNOWN_ACTION, pair[0])
            return

        for i in xrange(len(actions) - 1):
            if act != None:
                try:
                    pair = actions[i]
                    nextPair = actions[i + 1]
                    act = getattr(act(0, Functor(self._actionSetActionType, nextPair[3], nextPair[0]), pair[2], scale, keep), nextPair[0])
                    act.enableAlpha(blend)
                except:
                    self._actionSetActionType(action.UNKNOWN_ACTION, nextPair[3])
                    return

        if act != None:
            pair = actions[len(actions) - 1]
            act(0, Functor(self.endPlayActionSequence2, pair[0], key), pair[2], scale, keep)

    def endPlayActionSequence2(self, actionName, seqKey):
        self._actionSetActionType(action.UNKNOWN_ACTION, actionName)
        self._actionComplete(seqKey)

    def stopModelAction(self, model):
        if not hasattr(model, 'queue'):
            return
        actQueue = model.queue
        if len(actQueue) == 0:
            return
        model.unlockSpine()
        owner = BigWorld.entity(self.owner)
        faceEmotionAction = None
        if hasattr(owner, 'modelServer') and getattr(owner.modelServer, 'faceIdleAction', None):
            faceEmotionAction = owner.modelServer.faceIdleAction
        else:
            faceEmotionAction = getattr(owner, 'faceEmoteXmlInfo', {}).get('faceEmotionAction', None)
        for i in actQueue:
            try:
                if faceEmotionAction == i:
                    continue
                aq = model.action(i)
                if model.freezeTime <= 0:
                    aq.stop()
                    self._stopCueSoundAndEffect(aq.name)
                    self._doingActionType = action.UNKNOWN_ACTION
            except:
                pass

    def stopActionByName(self, model, actionName):
        if not model:
            self._doingActionType = action.UNKNOWN_ACTION
            return
        actQueue = model.queue
        if len(actQueue) == 0:
            self._doingActionType = action.UNKNOWN_ACTION
            return
        if actionName in actQueue:
            aq = model.action(actionName)
            if model.freezeTime <= 0:
                aq.stop()
                self._stopCueSoundAndEffect(aq.name)
                self._doingActionType = action.UNKNOWN_ACTION

    def stopAllActions(self):
        owner = BigWorld.entity(self.owner)
        if not owner:
            return
        self.stopAction()
        self.stopModelAction(owner.model)
        if hasattr(owner, 'isInCoupleRide') and owner.isInCoupleRide():
            if owner.modelServer.coupleModel:
                self.stopModelAction(owner.modelServer.coupleModel)
        if hasattr(owner, 'inRidingHorse') and owner.inRidingHorse():
            if getattr(owner.model, 'ride', None):
                self.stopModelAction(owner.model.ride)
            else:
                model = owner.modelServer.bodyModel
                if model:
                    self.stopModelAction(model)
            self.stopRideTogetherActions()

    def stopRideTogetherActions(self):
        owner = BigWorld.entity(self.owner)
        if not owner:
            return
        if hasattr(owner, 'tride') and owner.tride.inRide():
            for key in owner.tride.keys():
                idx = owner.tride.get(key)
                model = owner.modelServer.getRideTogetherModelByIdx(idx)
                self.stopModelAction(model)

    def _releaseFxByIDs(self, effIds, tintId):
        if len(self.playedFx) > 0 and effIds:
            needRm = []
            for fxsPair in self.playedFx:
                fxs = fxsPair[0]
                effect = fxsPair[1]
                if effect not in effIds:
                    continue
                if self._notStopFxWhenActStop(effect):
                    pass
                else:
                    for fx in fxs:
                        fx.stop()

                    needRm.append(fxsPair)

            for fxsPair in needRm:
                self.playedFx.remove(fxsPair)

        self._releaseTintFxById(tintId)

    def _releaseTintFxById(self, tintId):
        if not tintId:
            return
        owner = BigWorld.entity(self.owner)
        if len(self.playedTintFx) > 0:
            needRm = []
            for Tints in self.playedTintFx:
                if tintId != Tints[1]:
                    continue
                if type(Tints[1]) is tuple:
                    tintalt.ta_delGaoLiang(Tints[0])
                elif self.isPlayer:
                    tintalt.ta_del(Tints[0], Tints[1], isTaAddCall=True, tintType=tintalt.SKILLTINT)
                needRm.append(Tints)
                if hasattr(owner, 'restoreTintStateType') and owner.tintStateType[0] <= Tints[2]:
                    owner.restoreTintStateType()

            for Tints in needRm:
                self.playedTintFx.remove(Tints)

    def _releaseFx(self):
        if len(self.playedFx) > 0:
            for fxsPair in self.playedFx:
                fxs = fxsPair[0]
                effect = fxsPair[1]
                if self._notStopFxWhenActStop(effect):
                    pass
                else:
                    for fx in fxs:
                        fx.stop()

        self.playedFx = []
        self._releaseTintFx()

    def _notStopFxWhenActStop(self, effect):
        sfd = SFD.data.get(effect, {})
        if sfd:
            return sfd.get('stopType', False)
        else:
            return False

    def _releaseTintFx(self):
        owner = BigWorld.entity(self.owner)
        if len(self.playedTintFx) > 0:
            for Tints in self.playedTintFx:
                if type(Tints[1]) is tuple:
                    tintalt.ta_delGaoLiang(Tints[0])
                else:
                    tintalt.ta_del(Tints[0], Tints[1], isTaAddCall=True, tintType=tintalt.SKILLTINT)
                if hasattr(owner, 'restoreTintStateType') and owner.tintStateType[0] <= Tints[2]:
                    owner.restoreTintStateType()

        self.playedTintFx = []

    def setDoingActionType(self, actionType):
        if self._doingActionType in [action.IDLE_ACTION,
         action.CASTSTOP_ACTION,
         action.AFTERMOVESTOP_ACTION,
         action.ROLLSTOP_ACTION,
         action.FALLEND_ACTION,
         action.GUIDESTOP_ACTION,
         action.MOVINGSTOP_ACTION,
         action.CHAT_ACTION]:
            owner = BigWorld.entity(self.owner)
            if getattr(owner, 'castSkillBusy', None):
                owner.castSkillBusy = False
        self._doingActionType = actionType

    def doingActionType(self):
        return self._doingActionType

    def verticalMoveNotifier(self, isVerticalMove):
        owner = BigWorld.entity(self.owner)
        apEffectEx = getattr(owner, 'apEffectEx', None)
        if apEffectEx:
            apEffectEx.verticalMoveNotifier(isVerticalMove)
        if owner and owner.inWorld:
            if hasattr(owner, 'verticalMoveNotifier'):
                owner.verticalMoveNotifier(isVerticalMove)

    def movingNotifier(self, isMoving, moveSpeed = 1.0):
        owner = BigWorld.entity(self.owner)
        apEffectEx = getattr(owner, 'apEffectEx', None)
        if apEffectEx:
            apEffectEx.movingNotifier(isMoving)
        if isMoving:
            if hasattr(owner, 'resetClientYawMinDist'):
                owner.resetClientYawMinDist()
            self.resetTurnBodyState()
        if hasattr(owner, 'movingNotifier'):
            owner.movingNotifier(isMoving, moveSpeed)

    def getActionTime(self, actionName):
        if not actionName:
            return 0.0
        owner = BigWorld.entity(self.owner)
        if actionName not in self.getActionNameList():
            return 0.0
        try:
            actionTime = owner.model.action(actionName).duration
            if actionTime < 0.0:
                return 0.5
            return actionTime
        except:
            gamelog.error('ERROR:actionName not valid', actionName)
            return 0.5

    def forceUpdateMovingNotifier(self):
        owner = BigWorld.entity(self.owner)
        if not owner:
            return
        if self.isPlayer:
            owner.updateActionKeyState()
        owner.movingNotifier(owner.inMoving())

    def getRollLeftStartAction(self):
        if getattr(self, 'action', None):
            owner = BigWorld.entity(self.owner)
            if not owner.inFly:
                return self.action.getRollLeftStartAction(self)
            else:
                return self.action.getFlyRollLeftStartAction(self)

    def getRollLeftStopAction(self):
        if getattr(self, 'action', None):
            owner = BigWorld.entity(self.owner)
            if not owner.inFly:
                return self.action.getRollLeftStopAction(self)
            else:
                return self.action.getFlyRollLeftStopAction(self)

    def getRollRightStartAction(self):
        if getattr(self, 'action', None):
            owner = BigWorld.entity(self.owner)
            if not owner.inFly:
                return self.action.getRollRightStartAction(self)
            else:
                return self.action.getFlyRollRightStartAction(self)

    def getRollRightStopAction(self):
        if getattr(self, 'action', None):
            owner = BigWorld.entity(self.owner)
            if not owner.inFly:
                return self.action.getRollRightStopAction(self)
            else:
                return self.action.getFlyRollRightStopAction(self)

    def getRollBackStartAction(self):
        if getattr(self, 'action', None):
            owner = BigWorld.entity(self.owner)
            if not owner.inFly:
                return self.action.getRollBackStartAction(self)
            else:
                return self.action.getFlyRollBackStartAction(self)

    def getRollBackStopAction(self):
        if getattr(self, 'action', None):
            owner = BigWorld.entity(self.owner)
            if not owner.inFly:
                return self.action.getRollBackStopAction(self)
            else:
                return self.action.getFlyRollBackStopAction(self)

    def getRollFollowStartAction(self):
        if getattr(self, 'action', None):
            owner = BigWorld.entity(self.owner)
            if not owner.inFly:
                return self.action.getRollFollowStartAction(self)
            else:
                return self.action.getFlyRollFollowStartAction(self)

    def getRollFollowStopAction(self):
        if getattr(self, 'action', None):
            owner = BigWorld.entity(self.owner)
            if not owner.inFly:
                return self.action.getRollFollowStopAction(self)
            else:
                return self.action.getFlyRollFollowStopAction(self)

    def getRollUpStartAction(self):
        if getattr(self, 'action', None):
            owner = BigWorld.entity(self.owner)
            if not owner.inFly:
                return self.action.getRollUpStartAction(self)
            else:
                return self.action.getFlyRollUpStartAction(self)

    def getRollUpStopAction(self):
        if getattr(self, 'action', None):
            owner = BigWorld.entity(self.owner)
            if not owner.inFly:
                return self.action.getRollUpStopAction(self)
            else:
                return self.action.getFlyRollUpStopAction(self)

    def getRollDownStartAction(self):
        if getattr(self, 'action', None):
            owner = BigWorld.entity(self.owner)
            if not owner.inFly:
                return self.action.getRollDownStartAction(self)
            else:
                return self.action.getFlyRollDownStartAction(self)

    def getRollDownStopAction(self):
        if getattr(self, 'action', None):
            owner = BigWorld.entity(self.owner)
            if not owner.inFly:
                return self.action.getRollDownStartAction(self)
            else:
                return self.action.getFlyRollDownStopAction(self)

    def getWingFlyStopAction(self):
        owner = BigWorld.entity(self.owner)
        if getattr(self, 'action', None):
            if owner.isInCoupleRide():
                return
            return self.action.getWingFlyStopAction(self)

    def getWingFlyUpStartAction(self):
        owner = BigWorld.entity(self.owner)
        if getattr(self, 'action', None):
            if owner.isInCoupleRide():
                return
            return self.action.getWingFlyUpStartAction(self)

    def getWingFlyUpAction(self):
        owner = BigWorld.entity(self.owner)
        if getattr(self, 'action', None):
            if owner.isInCoupleRide():
                return
            return self.action.getWingFlyUpAction(self)

    def getWingFlyDownAction(self):
        owner = BigWorld.entity(self.owner)
        if getattr(self, 'action', None):
            if owner.isInCoupleRide():
                return
            return self.action.getWingFlyDownAction(self)

    def getWingFlyNormalDownAction(self):
        if getattr(self, 'action', None):
            return self.action.getWingFlyNormalDownAction(self)

    def getWingFlyNormalUpAction(self):
        if getattr(self, 'action', None):
            return self.action.getWingFlyNormalUpAction(self)

    def getWingFlyFastFallAction(self):
        if getattr(self, 'action', None):
            return self.action.getWingFlyFastDownAction(self)

    def getWingFlyFastFallEndAction(self):
        if getattr(self, 'action', None):
            return self.action.getWingFlyFastDownEndAction(self)


def globalActionComplete(fashionObj, key):
    fashionObj._actionComplete(key)
