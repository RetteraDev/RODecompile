#Embedded file name: /WORKSPACE/data/entities/client/helpers/monsteraction.o
import random
import keys
import gameglobal
import gamelog
from data import monster_model_client_data as NMMD
from data import monster_action_data as MAD

class MonsterActionGroup(object):

    def __init__(self, owner, actGroupId = 1, idleGroupId = 0):
        super(MonsterActionGroup, self).__init__()
        self.idleGroupId = idleGroupId
        self.actGroupId = actGroupId
        self.dieActionGroupId = 0
        self.owner = owner
        self.actionList = None
        self.beHitMod = 0
        self.alphaBeHitActions = []

    def needSetIdleCaps(self):
        if MAD.data.has_key(self.actGroupId):
            return MAD.data[self.actGroupId].get('matchCaps', None)
        return False

    def getCapsIdle(self, fashion):
        if self.owner.isMultiPartMonster():
            return self.owner.getAvatarMonsterCap()
        if MAD.data.has_key(self.actGroupId):
            matchCaps = MAD.data[self.actGroupId].get('matchCaps', None)
            if matchCaps:
                return matchCaps
            idleActions = MAD.data[self.actGroupId].get('idleAct', None)
            if not idleActions:
                self.idleGroupId = keys.CAPS_IDLE0
                return keys.CAPS_IDLE0
            md = NMMD.data.get(self.owner.charType, None)
            if md:
                idleGroupId = md.get('idleGroupid', 0)
            else:
                idleGroupId = 1
            capsIdle = self.idleGroupId
            if idleGroupId > len(idleActions):
                capsIdle = random.randint(keys.CAPS_IDLE0, len(idleActions))
                self.idleGroupId = capsIdle
            return capsIdle
        return keys.CAPS_IDLE0

    def getCapsCombat(self, fashion):
        if MAD.data.has_key(self.actGroupId):
            matchCaps = MAD.data[self.actGroupId].get('combatMatchCaps', None)
            if matchCaps:
                return matchCaps
        return keys.CAPS_HAND_FREE

    def getGuardAction(self, fashion):
        gamelog.debug('getGuardAction:', self.owner.id)
        if MAD.data.has_key(self.actGroupId):
            guardActions = MAD.data[self.actGroupId].get('guardAct', None)
            if not guardActions:
                return
            guardAction = random.choice(guardActions)
            if guardAction not in fashion.action.actionList:
                return
            return guardAction

    def getAttackAction(self, fashion):
        if MAD.data.has_key(self.actGroupId):
            attackActions = MAD.data[self.actGroupId].get('attackAct', None)
            if not attackActions:
                return
            attackAction = random.choice(attackActions)
            gamelog.debug('zfactions:getAttackAction2', attackAction)
            if attackAction not in fashion.action.actionList:
                return attackActions[0]
            gamelog.debug('zfactions:getAttackAction3', attackActions)
            return attackAction

    def getHitFlyAction(self, fashion):
        if MAD.data.has_key(self.actGroupId):
            hitFlyActions = MAD.data[self.actGroupId].get('hitFlyAct', None)
            if not hitFlyActions:
                return
            hitFlyAction = random.choice(hitFlyActions)
            if hitFlyAction not in fashion.action.actionList:
                return hitFlyActions[0]
            return hitFlyAction

    def getHitDieFlyName(self, fashion):
        hitDieFly = []
        for act in ['1809', '1812']:
            if act in fashion.action.actionList:
                hitDieFly.append(act)

        if len(hitDieFly) > 0:
            return random.choice(hitDieFly)

    def getAlphaBeHitActions(self):
        if self.alphaBeHitActions:
            return self.alphaBeHitActions
        beHitActions = MAD.data[self.actGroupId].get('frontHit', None)
        if beHitActions:
            self.alphaBeHitActions.extend(beHitActions)
        beHitActions = MAD.data[self.actGroupId].get('backHit', None)
        if beHitActions:
            self.alphaBeHitActions.extend(beHitActions)
        beHitActions = MAD.data[self.actGroupId].get('frontCritHit', None)
        if beHitActions:
            self.alphaBeHitActions.extend(beHitActions)
        beHitActions = MAD.data[self.actGroupId].get('backCritHit', None)
        if beHitActions:
            self.alphaBeHitActions.extend(beHitActions)
        if MAD.data.has_key(self.actGroupId):
            beHitActions = MAD.data[self.actGroupId].get('forceBeHitAct', None)
            if beHitActions:
                self.alphaBeHitActions.extend(beHitActions)
        beHitActions = MAD.data[self.actGroupId].get('faintStartAct', None)
        if beHitActions:
            self.alphaBeHitActions.extend(beHitActions)
        return self.alphaBeHitActions

    def getBeHitAction(self, fashion, beHitType = gameglobal.NORMAL_HIT):
        if MAD.data.has_key(self.actGroupId):
            beHitActions = None
            if beHitType in gameglobal.FRONT_HIT_TUPLE:
                beHitActions = MAD.data[self.actGroupId].get('frontHit', None)
            elif beHitType in gameglobal.BACK_HIT_TUPLE:
                beHitActions = MAD.data[self.actGroupId].get('backHit', None)
            elif beHitType in gameglobal.FRONT_CRIT_HIT_TUPLE:
                beHitActions = MAD.data[self.actGroupId].get('frontCritHit', None)
            elif beHitType in gameglobal.BACK_CRIT_HIT_TUPLE:
                beHitActions = MAD.data[self.actGroupId].get('backCritHit', None)
            elif beHitType == gameglobal.LIE_HIT:
                acts = []
                if MAD.data[self.actGroupId].get('lieHit', None):
                    acts.append(MAD.data[self.actGroupId].get('lieHit', None))
                if MAD.data[self.actGroupId].get('lieHit1', None):
                    acts.append(MAD.data[self.actGroupId].get('lieHit1', None))
                if acts:
                    random.shuffle(acts)
                    beHitActions = acts[0]
            elif beHitType == gameglobal.LIE_CRIT_HIT:
                beHitActions = MAD.data[self.actGroupId].get('lieCritHit', None)
            elif beHitType == gameglobal.FAINT_HIT:
                beHitActions = MAD.data[self.actGroupId].get('faintStartAct', None)
            if not beHitActions:
                beHitActions = MAD.data[self.actGroupId].get('hitAct', None)
            if not beHitActions:
                return
            beHitAction = None
            if beHitType in gameglobal.FRONT_HIT_TUPLE:
                beHitAction = beHitActions[self.beHitMod]
                self.beHitMod = (self.beHitMod + 1) % len(beHitActions)
            else:
                beHitAction = random.choice(beHitActions)
            if beHitAction not in fashion.action.actionList:
                return beHitActions[0]
            return beHitAction

    def getFaintAction(self, fashion):
        if MAD.data.has_key(self.actGroupId):
            faintActions = MAD.data[self.actGroupId].get('faintAct', None)
            if not faintActions:
                return
            faintAction = random.choice(faintActions)
            if faintAction not in fashion.action.actionList:
                return faintActions[0]
            return faintAction

    def getPrefixStateAction(self, fashion):
        if MAD.data.has_key(self.actGroupId):
            return MAD.data.get(self.actGroupId, {}).get('prefixStateAction', '1')
        return '1'

    def getDieAction(self, fashion):
        if MAD.data.has_key(self.actGroupId):
            dieActions = MAD.data[self.actGroupId].get('dieAct', None)
            if not dieActions:
                return
            self.dieActionGroupId = random.randint(0, len(dieActions) - 1)
            if dieActions[self.dieActionGroupId] not in fashion.action.actionList:
                self.dieActionGroupId = 0
            return dieActions[self.dieActionGroupId]

    def getDie1Action(self, fashion):
        return self.getDieAction(fashion)

    def getDead1Action(self, fashion):
        return self.getDeadAction(fashion)

    def getDeadAction(self, fashion):
        if MAD.data.has_key(self.actGroupId):
            deadActions = MAD.data[self.actGroupId].get('deadAct', None)
            if not deadActions:
                return
            if deadActions[self.dieActionGroupId] not in fashion.action.actionList:
                return deadActions[0]
            return deadActions[self.dieActionGroupId]

    def getSummonAction(self, fashion):
        if MAD.data.has_key(self.actGroupId):
            summonActions = MAD.data[self.actGroupId].get('summonAct', None)
            if not summonActions:
                return
            if summonActions[self.dieActionGroupId] not in fashion.action.actionList:
                return summonActions[0]
            return summonActions[self.dieActionGroupId]

    def getAction(self, fashion, key):
        if MAD.data.has_key(self.actGroupId):
            actions = MAD.data[self.actGroupId].get(key, None)
            if not actions:
                return
            return actions[0]

    def getRandomAction(self, fashion, key):
        if MAD.data.has_key(self.actGroupId):
            actions = MAD.data[self.actGroupId].get(key, None)
            if not actions:
                return
            return random.choice(actions)

    def getBoredAction(self, fashion):
        if self.idleGroupId == None:
            return
        if MAD.data.has_key(self.actGroupId):
            if self.owner.inCombat:
                boredActions = MAD.data[self.actGroupId].get('specialGuardAct', None)
            else:
                boredActions = MAD.data[self.actGroupId].get('boredAct', None)
                if self.owner.IsSummonedSprite and self.owner.inFly:
                    flyBoredAct = MAD.data[self.actGroupId].get('flyBoredAct', None)
                    if flyBoredAct:
                        boredActions = flyBoredAct
            if not boredActions:
                return
            if self.owner.inCombat:
                return boredActions
            if self.idleGroupId <= len(boredActions):
                return boredActions[self.idleGroupId - 1]


monsterActionMap = {}

def getMonsterActionGroup(owner, index = 1):
    if hasattr(owner, 'getItemData'):
        md = owner.getItemData()
    else:
        md = NMMD.data.get(owner.charType, None)
    actGroupidStr = 'actGroupid'
    idleGroupidStr = 'idleGroupid'
    if index == 2 and md.has_key('actGroupid2'):
        actGroupidStr = 'actGroupid2'
        idleGroupidStr = 'idleGroupid2'
    if md:
        actGroupId = md.get(actGroupidStr, None)
        idleGroupId = md.get(idleGroupidStr, None)
        return MonsterActionGroup(owner, actGroupId, idleGroupId)
    gamelog.error('getMonstActionGroup:can not find model', owner.charType, owner.id)


global monsterActionMap ## Warning: Unused global
