#Embedded file name: /WORKSPACE/data/entities/common/combatutils.o
import math
import Math
import sMath
import formula
import utils
from sMath import distance2D, distance3D, inRange2D
from gameclass import SkillEffectInfo
from fbStatistics import FubenStats
from random import random as randomf, sample, uniform, choice, shuffle
import BigWorld
import commcalc
import gametypes
import gamelog
import const
import commcython
from collections import Iterable
from data import pskill_type_reverse_data as PTRD
from cdata import state_group_data as SGPD
from cdata import game_msg_def_data as GMDD
from data import map_config_data as MCD
from data import skill_general_data as SKGD
from data import zaiju_data as ZD
from data import skill_effects_data as SED
from data import sys_config_data as SCD
IN_CLIENT = False
if BigWorld.component in 'client':
    IN_CLIENT = True
    import gameglobal
else:
    import Netease
    import gameengine
    import gameconfig
    import relation
    SE_STATE = 0
    SE_SEX = 1
    SE_HP_LESS = 2
    SE_HP_NO_LESS = 3
    SE_FRIEND = 4
    SE_HATE = 5
    SE_UNIT_TYPE = 6
    SE_FRIEND_TYPE = 7
    SE_S_FRIEND_TYPE = 8
    SE_ENEMY_TYPE = 9
    SE_S_ENEMY_TYPE = 10
    SE_NOT_INCLUDE = 11
    SE_NOT_INCLUDE_CREATION = 12
    SE_SCHOOL = 13
    SE_MP_LESS = 14
    SE_MP_NO_LESS = 15
    SE_MHP_AND_MINE = 16
    SE_DEFENCE_RELATION = 17
    SE_SPECIAL_ATTR = 18
    SE_NO_UNIT_TYPE = 19
MAX_TARGET_NUM_WORLD = 8
MAX_TARGET_NUM_CRITICAL_SKILL = 10
MAX_TARGET_NUM_FUBEN = 24

class CombatDataBase(object):

    def __init__(self, combatUnit, isSrc = False):
        super(CombatDataBase, self).__init__()
        self.owner = combatUnit
        self.lv = combatUnit.realLv if combatUnit.IsAvatar else getattr(combatUnit, 'lv', 1)
        self.tempData = {}
        self.virtualMonster = None
        if combatUnit.IsVirtualMonster:
            self.virtualMonster = combatUnit
        if isSrc:
            self.effectListCache = {}


class ResultRecorderCommon(object):

    def __init__(self, owner, nextAtkDelay = 0):
        super(ResultRecorderCommon, self).__init__()
        self.owner = owner
        self.cc = None
        self.enemyCache = {}
        self.friendCache = {}

    def isEnemy(self, tgt):
        if tgt.id in self.enemyCache:
            return self.enemyCache[tgt.id] == True
        if IN_CLIENT:
            enemy = self.owner.isEnemy(tgt)
        else:
            enemy = relation.isEnemy(self.owner, tgt)
        self.enemyCache[tgt.id] = True if enemy else False
        return enemy

    def isFriend(self, tgt):
        if tgt.id in self.friendCache:
            return self.friendCache[tgt.id] == True
        if IN_CLIENT:
            friend = self.owner.isFriend(tgt)
        else:
            friend = relation.isFriend(self.owner, tgt)
        self.friendCache[tgt.id] = True if friend else False
        return friend

    def getRelation(self, tgt):
        if tgt.id in self.enemyCache and self.enemyCache[tgt.id] == True:
            return gametypes.RELATION_ENEMY
        elif tgt.id in self.friendCache and self.friendCache[tgt.id] == True:
            return gametypes.RELATION_FRIENDLY
        elif self.isEnemy(tgt):
            return gametypes.RELATION_ENEMY
        elif self.isFriend(tgt):
            return gametypes.RELATION_FRIENDLY
        else:
            return gametypes.RELATION_NEUTRAL


def getGroupStates(group):
    groupStates = set()
    if type(group) == int:
        groupStates = set(SGPD.data.get(group).get('states', ()))
    elif len(group) == 1:
        groupStates = set(SGPD.data.get(group[0]).get('states', ()))
    elif group[0] == 0:
        groupStates = set(SGPD.data.get(group[1]).get('states', ()))
        for gp in group[2:]:
            groupStates = groupStates & set(SGPD.data.get(gp).get('states', ()))
            if not groupStates:
                break

    elif group[0] == 1:
        groupStates = set(SGPD.data.get(group[1]).get('states', ()))
        for gp in group[2:]:
            groupStates = groupStates | set(SGPD.data.get(gp).get('states', ()))

    return groupStates


@commcython.cythonfuncentry
def _calcSkillEffectList(srccd, tgtcd, skillEffectInfo, skillId = 0, forceCenter = None):
    """
    @cython.locals(skillId=cython.int, tgtType=cython.int, srcid=cython.int, beastId=cython.int, maxTargetNum=cython.int,
        calcPriority=cython.int, selfIncluded=cython.bint, cliqueMaxDist=cython.float, cliqueNeedTgtNum=cython.int,
        eId=cython.int, rlimit=cython.int, nearestN=cython.int)
    """
    src = srccd.owner
    tgt = tgtcd.owner
    if tgtcd.virtualMonster:
        tgt = tgtcd.virtualMonster
    result = []
    effectProp = skillEffectInfo.getSkillEffectData('effectProp', gametypes.SKILL_EFFECT_PROP_DEFAULT_VAL)
    if effectProp != gametypes.SKILL_EFFECT_PROP_DEFAULT_VAL and randomf() > effectProp:
        return result
    tgtType = skillEffectInfo.getSkillEffectData('tgt', 0)
    srcid = src.id
    if src.IsThrownCreation:
        srcid = src.ownerId
    if tgtType == gametypes.SKILL_EFFECT_TGT_SELF:
        result.append(src)
    elif tgtType == gametypes.SKILL_EFFECT_TGT_OTHER:
        if srcid != tgt.id:
            result.append(tgt)
    elif gametypes.SKILL_EFFECT_TGT_ALL <= tgtType:
        if tgtType == gametypes.SKILL_EFFECT_TGT_ALL:
            result.append(tgt)
        elif tgtType == gametypes.SKILL_EFFECT_TGT_SELF_WHEN_LOCK_ENEMY:
            if srccd.rr.isEnemy(tgt):
                result.append(src)
            elif srcid == tgt.id:
                result.append(src)
        elif tgtType == gametypes.SKILL_EFFECT_TGT_MASTER:
            if not src.IsSummoned or not src.ownerId:
                return result
            owner = BigWorld.entities.get(src.ownerId)
            if owner:
                result.append(owner)
        elif tgtType == gametypes.SKILL_EFFECT_TGT_SUMMONED_BEAST:
            if IN_CLIENT:
                result.extend([ e for e in BigWorld.entities.values() if e.IsSummonedBeast and e.ownerId == srcid ])
            elif src.summonedBeasts:
                for _, val in src.summonedBeasts.iteritems():
                    for beastId, _ in val:
                        beast = BigWorld.entities.get(beastId)
                        if beast:
                            result.append(beast)

        elif tgtType == gametypes.SKILL_EFFECT_TGT_SUMMON_SPRIT_OWNER:
            if src.IsSummonedSprite and src.ownerId:
                spriteOwner = BigWorld.entities.get(src.ownerId)
                if spriteOwner:
                    result.append(spriteOwner)
        elif tgtType == gametypes.SKILL_EFFECT_TGT_SUMMON_SPRIT_AND_OWNER:
            if src.IsSummonedSprite and src.ownerId:
                spriteOwner = BigWorld.entities.get(src.ownerId)
                if spriteOwner:
                    result.append(spriteOwner)
                    result.append(src)
        elif tgtType == gametypes.SKILL_EFFECT_TGT_SUMMON_SPRIT_SELF:
            if IN_CLIENT:
                if src.IsAvatar and src.spriteObjId:
                    summonSprite = BigWorld.entities.get(src.spriteObjId)
                    if summonSprite:
                        result.append(summonSprite)
            elif src.IsAvatar and src.summonedSpriteBox:
                summonSprite = BigWorld.entities.get(src.summonedSpriteBox.id)
                if summonSprite:
                    result.append(summonSprite)
        elif tgtType == gametypes.SKILL_EFFECT_TGT_WING_WORLD_CARRIER_ENT:
            if src.IsAvatar and isinstance(src.wingWorldCarrier, dict) and srcid in src.wingWorldCarrier:
                carrierEnt = BigWorld.entities.get(src.wingWorldCarrier.carrierEntId)
                if carrierEnt:
                    result.append(carrierEnt)
    else:
        result = calcAreaSkillEffectList(srccd, tgtcd, skillEffectInfo, forceCenter)
    result = processVirturalCalcUnit(result)
    maxTargetNum = _getMaxTargetNum(src, skillEffectInfo, skillId)
    reserved = None
    filteredResult = set()
    calcPriority = 0
    lastPriorityResult = set()
    selfIncluded = skillEffectInfo.getSkillEffectData('selfIncluded', 0) or skillEffectInfo.getSkillEffectData('tgt') in (gametypes.SKILL_EFFECT_TGT_SELF, gametypes.SKILL_EFFECT_TGT_ALL, gametypes.SKILL_EFFECT_TGT_SELF_WHEN_LOCK_ENEMY)
    cliqueMaxDist, cliqueNeedTgtNum = skillEffectInfo.getSkillEffectData('tgtInCliqueArg', (0, 0))
    if cliqueMaxDist and cliqueNeedTgtNum:
        MIN_TGT_NEEDED_IN_CLIQUE = 2
        cliqueNeedTgtNum = max(MIN_TGT_NEEDED_IN_CLIQUE, cliqueNeedTgtNum)
        tmpResult = set()
        for e in result:
            if len(tmpResult) > maxTargetNum:
                break
            if checkSkillEffectTarget(srccd, e, skillEffectInfo):
                tmpResult.add(e)

        if not selfIncluded:
            tmpResult.discard(src)
        eIdsInMaxClique = getTgtsInMaxClique([ e for e in tmpResult ], cliqueMaxDist)
        if len(eIdsInMaxClique) >= MIN_TGT_NEEDED_IN_CLIQUE:
            result = set()
            selectedEIds = eIdsInMaxClique[:cliqueNeedTgtNum]
            for eId in selectedEIds:
                ent = BigWorld.entities.get(eId)
                if ent:
                    result.add(ent)

            return result
        else:
            return set()
    if len(result) > maxTargetNum:
        if src.IsAvatar and hasattr(src, 'lockedId'):
            locked = BigWorld.entities.get(src.lockedId)
            if locked and locked in result and checkSkillEffectTarget(srccd, locked, skillEffectInfo):
                result.remove(locked)
                reserved = locked
                if not selfIncluded and reserved == src:
                    reserved = None
        if src.IsAvatar and skillEffectInfo.getSkillEffectData('hurtType') in gametypes.SKILL_HURT_ADD:
            lastPriorityResult = set([ r for r in result if r.IsSummonedSprite ])
            for e in lastPriorityResult:
                result.discard(e)

        if src.IsMonster and skillEffectInfo.getSkillEffectData('hurtType') in gametypes.SKILL_HURT_REDUCE:
            lastPriorityResult = set([ r for r in result if r.IsSummonedSprite ])
            for e in lastPriorityResult:
                result.discard(e)

        calcPriority = skillEffectInfo.getSkillEffectData('tgtEnemyPriority', 0)
        if calcPriority:
            rList = list(result)
            shuffle(rList)
            for r in rList:
                if (calcPriority == 1 and r.IsAvatar or calcPriority == 2 and r.IsMonster) and checkSkillEffectTarget(srccd, r, skillEffectInfo):
                    filteredResult.add(r)
                    if len(filteredResult) >= maxTargetNum:
                        break

            if not selfIncluded:
                filteredResult.discard(src)
    rlimit = maxTargetNum - 1 if reserved else maxTargetNum
    if rlimit > len(filteredResult):
        for r in result:
            if len(filteredResult) >= rlimit:
                if not selfIncluded:
                    filteredResult.discard(src)
                if len(filteredResult) >= rlimit:
                    break
            if checkSkillEffectTarget(srccd, r, skillEffectInfo):
                filteredResult.add(r)

        if not selfIncluded:
            filteredResult.discard(src)
    elif rlimit < len(filteredResult):
        filteredResult = set(sample(filteredResult, rlimit))
    if rlimit > len(filteredResult):
        for r in lastPriorityResult:
            if len(filteredResult) >= rlimit:
                if not selfIncluded:
                    filteredResult.discard(src)
                if len(filteredResult) >= rlimit:
                    break
            if checkSkillEffectTarget(srccd, r, skillEffectInfo):
                filteredResult.add(r)

        if not selfIncluded:
            filteredResult.discard(src)
    if reserved:
        filteredResult.add(reserved)
    nearestN = skillEffectInfo.getSkillEffectData('nearestN', 0)
    farthestN = skillEffectInfo.getSkillEffectData('farthestN', 0)
    limitN = nearestN or farthestN
    if limitN and len(filteredResult) > limitN:
        listResult = []
        for entity in filteredResult:
            if not (entity.IsAvatar or entity.IsMonster or entity.IsAvatarRobot or entity.IsPuppet):
                continue
            if hasattr(entity, 'isCUAlive') and not entity.isCUAlive(entity):
                continue
            listResult.append(entity)

        if len(filteredResult) > limitN:
            isReverse = farthestN and True or False
            listResult.sort(key=lambda tgt: distance3D(src.position, tgt.position), reverse=isReverse)
            listResult = listResult[:limitN]
        filteredResult = set(listResult)
    randN = skillEffectInfo.getSkillEffectData('randN', 0)
    if randN and len(filteredResult) > randN:
        filteredResult = set(sample(filteredResult, randN))
    _processSkillEffectAffectTarget(srccd, tgtcd, skillEffectInfo, filteredResult)
    return filteredResult


def _processSkillEffectAffectTarget(srccd, tgtcd, skillEffectInfo, result):
    src = srccd.owner
    tgt = tgtcd.owner
    singleTgtEnemyType = skillEffectInfo.getSkillEffectData('singleTgtEnemyType', 0)
    tgtEnemyType = skillEffectInfo.getSkillEffectData('tgtEnemyType', 0)
    if not singleTgtEnemyType and not tgtEnemyType:
        return
    if not hasattr(src, 'dmgSECount') or gametypes.SKILL_EFFECT_SE_APPEND_AFFECT_TARGET not in src.dmgSECount:
        return
    affectId, lastTime, recordTime = src.dmgSECount[gametypes.SKILL_EFFECT_SE_APPEND_AFFECT_TARGET]
    affectEnt = BigWorld.entities.get(affectId)
    if not affectEnt:
        src.dmgSECount.pop(gametypes.SKILL_EFFECT_SE_APPEND_AFFECT_TARGET)
        return
    if utils.getNow() > recordTime + lastTime:
        src.dmgSECount.pop(gametypes.SKILL_EFFECT_SE_APPEND_AFFECT_TARGET)
        return
    if skillEffectInfo.getSkillEffectData('tgtNotIncluded'):
        if getattr(src, 'lockedId', 0) == tgt.id:
            return False
    if not checkSkillEffectTarget(srccd, affectEnt, skillEffectInfo):
        return
    result.add(affectEnt)


def _getMaxTargetNum(src, skillEffectInfo, skillId):
    isCriticalWsSkill = SKGD.data.get((skillId, 1), {}).get('wsStar', 0) >= 2
    hasTgtMax = False
    if skillEffectInfo.hasSkillEffectData('tgtFriendMax'):
        maxNum = skillEffectInfo.getSkillEffectData('tgtFriendMax')
        hasTgtMax = True
    elif skillEffectInfo.hasSkillEffectData('tgtEnemyMax'):
        maxNum = skillEffectInfo.getSkillEffectData('tgtEnemyMax')
        hasTgtMax = True
    else:
        maxNum = MAX_TARGET_NUM_CRITICAL_SKILL if isCriticalWsSkill else MAX_TARGET_NUM_FUBEN
    if (not hasattr(BigWorld, 'load') or BigWorld.load() < 0.95) and isCriticalWsSkill:
        return maxNum
    if hasattr(src, 'loadLv') and src.loadLv > const.SERVER_LOAD_LV_NORMAL:
        maxLimit = int(MAX_TARGET_NUM_WORLD / 2)
    elif skillEffectInfo.getSkillEffectData('skillNoTgtLimit'):
        if not src.IsAvatar:
            maxLimit = 50 if formula.spaceInFuben(src.spaceNo) else 30
            if hasTgtMax:
                return min(maxNum, maxLimit)
            return maxLimit
        maxLimit = MAX_TARGET_NUM_WORLD
    else:
        maxLimit = MAX_TARGET_NUM_FUBEN if formula.spaceInFuben(src.spaceNo) else MAX_TARGET_NUM_WORLD
    return min(maxNum, maxLimit)


def getWingWorldWarCityGlobalTgt(spaceNo):
    if not IN_CLIENT:
        entIdSet = Netease.wingWorldWarBuildingEntIdsDict.get(spaceNo, set())
        ret = set()
        for entId in entIdSet:
            ent = BigWorld.entities.get(entId)
            if ent:
                ret.add(ent)

        return ret
    else:
        ret = set()
        player = BigWorld.player()
        if player and hasattr(player, 'wingWorldWarBuildingEntIdSet'):
            for entId in player.wingWorldWarBuildingEntIdSet:
                ent = BigWorld.entities.get(entId)
                if ent:
                    ret.add(ent)

        return ret


def isWithoutStateEx(obj):
    if obj == None:
        return False
    if IN_CLIENT and not obj.inWorld:
        return False
    return obj.IsCreation or obj.IsObstacle or obj.IsNaiveCombatUnit or obj.IsFragileObject


def _checkSingleState(curTgtStates, stateId, tgtStateLv, tgtStateSrcId):
    if tgtStateLv:
        if curTgtStates.get(stateId, (0, ()))[0] != tgtStateLv:
            return False
    if tgtStateSrcId:
        if tgtStateSrcId not in curTgtStates.get(stateId, (0, ()))[1]:
            return False
    return stateId in curTgtStates


def checkSkillEffectTarget(srccd, tgt, skillEffectInfo):
    if not IN_CLIENT:
        if not gameconfig.enableFrequentCache():
            return _checkSkillEffectTargetNormal(srccd, tgt, skillEffectInfo)
        elif not (skillEffectInfo.hijackData or skillEffectInfo.tgtHijackData or skillEffectInfo.tgtHijackDataCache):
            if Netease.hasSkillEffectCache.has_key(skillEffectInfo.num):
                ttags, ftags = Netease.hasSkillEffectCache[skillEffectInfo.num]
            else:
                ttags = [0] * 32
                ftags = [0] * 32
                Netease.hasSkillEffectCache[skillEffectInfo.num] = (ttags, ftags)
            r = _checkSkillEffectTargetCache(srccd, tgt, skillEffectInfo, ttags, ftags)
            if gameconfig.enableFrequentCacheCheck():
                nr = _checkSkillEffectTargetNormal(srccd, tgt, skillEffectInfo)
                if nr != r:
                    gameengine.reportCritical('checkSkillEffectTarget cache is not the same as origin', r, nr, skillEffectInfo.num, skillEffectInfo.lv, skillEffectInfo)
            return r
        else:
            return _checkSkillEffectTargetNormal(srccd, tgt, skillEffectInfo)
    else:
        return _checkSkillEffectTargetNormal(srccd, tgt, skillEffectInfo)


def _checkSkillEffectTargetNormal(srccd, tgt, skillEffectInfo):
    """
    @cython.locals(sid=cython.int, tgtStateLv=cython.int, tgtStateSrc=cython.int, checkType=cython.int,
        tgtStateSrcId=cython.int, sexReq=cython.int, tgtHpLessPct=cython.int, tgtHpNoLessPct=cython.int,
        tgtMpLessPct=cython.int, tgtMpNoLessPct=cython.int, relationType=cython.int, tgtUnitType=cython.int,
        tgtNoUnitType=cython.int, objType=cython.int, tgtMhpCmpMine=cython.int, tgtDefenceRelation=cython.int,
        attrId=cython.int)
    """
    src = srccd.owner
    if not validCalcTgt(tgt):
        return False
    if isAvatarOnWingWorldCarrier(tgt):
        return False
    if isWithoutStateEx(tgt):
        if getattr(tgt, 'ownerId', tgt.id) == src.id:
            return False
        if not srccd.rr.isEnemy(tgt) or not tgt.isCUAlive(tgt) or formula.inProtect(tgt) or formula.inPVPProtect(tgt) and (src.IsAvatar or src.IsSummonedSprite) and not skillEffectInfo.isHealTypeEffect():
            return False
        return True
    if srccd.rr.isMagicField and srccd.rr.cc and getattr(srccd.rr.cc, 'calcOnceForSingleTgt', False):
        if tgt.id in srccd.rr.cc.calcEntities:
            return False
    if tgt.getCUFlag(tgt, gametypes.FLAG_NOT_SKILL_TARGET) > 0:
        return False
    if (formula.inProtect(tgt) or (src.IsAvatar or src.IsSummonedSprite) and formula.inPVPProtect(tgt) and not skillEffectInfo.isHealTypeEffect()) and not getattr(srccd, 'ignoreProtect', 0) > 0 and src.id != tgt.id:
        return False
    if tgt.IsSummonedSprite:
        if skillEffectInfo.getSkillEffectData('hurtType', 0) == gametypes.SKILL_HURT_ADD_MP and src.id != tgt.id:
            return False
    if skillEffectInfo.hasSkillEffectData('tgtStates') or skillEffectInfo.hasSkillEffectData('tgtNoStates') or skillEffectInfo.hasSkillEffectData('tgtStateGroup') or skillEffectInfo.hasSkillEffectData('tgtNoStateGroup'):
        curTgtStates = {}
        if not IN_CLIENT or tgt == BigWorld.player():
            curTgtStates = {sid:(sum([ sVal[gametypes.STATE_INDEX_LAYER] for sVal in slst ]), [ sVal[gametypes.STATE_INDEX_SRCID] for sVal in slst ]) for sid, slst in tgt.statesServerAndOwn.iteritems()}
        else:
            curTgtStates = {sid:(sum([ sVal[gametypes.STATE_INDEX_LAYER] for sVal in slst ]), [ sVal[gametypes.STATE_INDEX_SRCID] for sVal in slst ]) for sid, slst in tgt.statesClientPub.iteritems()}
        tgtStates = skillEffectInfo.getSkillEffectData('tgtStates', [])
        if tgtStates:
            tgtStateLv = skillEffectInfo.getSkillEffectData('tgtStateLvl', 0)
            tgtStateSrc = skillEffectInfo.getSkillEffectData('tgtStateSrc', 0)
            checkType = tgtStates[0]
            tgtStates = tgtStates[1:] if checkType in gametypes.ALL_TGT_STATE_CHECK else tgtStates
            tgtStateSrcId = src.id if tgtStateSrc else 0
            if checkType == gametypes.TGT_STATE_CHECK_OR:
                flag = False
                for stateId in tgtStates:
                    if _checkSingleState(curTgtStates, stateId, tgtStateLv, tgtStateSrcId):
                        flag = True
                        break

            else:
                flag = True
                for stateId in tgtStates:
                    if not _checkSingleState(curTgtStates, stateId, tgtStateLv, tgtStateSrcId):
                        flag = False
                        break

            if not flag:
                return False
        tgtNoStates = skillEffectInfo.getSkillEffectData('tgtNoStates', [])
        for s in tgtNoStates:
            if s in curTgtStates:
                return False

        curTgtStateIds = set(curTgtStates.keys())
        tgtStateGroup = skillEffectInfo.getSkillEffectData('tgtStateGroup', [])
        if tgtStateGroup:
            groupStates = getGroupStates(tgtStateGroup)
            if not curTgtStateIds & groupStates:
                return False
        tgtNoStateGroup = skillEffectInfo.getSkillEffectData('tgtNoStateGroup', [])
        if tgtNoStateGroup:
            groupStates = getGroupStates(tgtNoStateGroup)
            if curTgtStateIds & groupStates:
                return False
    if skillEffectInfo.hasSkillEffectData('sexReq'):
        sexReq = skillEffectInfo.getSkillEffectData('sexReq')
        if sexReq > 0 and tgt.IsAvatar and tgt.physique.sex != sexReq:
            return False
    if skillEffectInfo.hasSkillEffectData('tgtHpLessPct'):
        tgtHpLessPct = skillEffectInfo.getSkillEffectData('tgtHpLessPct')
        if tgt.hp > tgtHpLessPct * getattr(tgt, 'mhp', 0) / 100.0:
            return False
    if skillEffectInfo.hasSkillEffectData('tgtHpNoLessPct'):
        tgtHpNoLessPct = skillEffectInfo.getSkillEffectData('tgtHpNoLessPct')
        if tgt.hp < tgtHpNoLessPct * getattr(tgt, 'mhp', 0) / 100.0:
            return False
    if skillEffectInfo.hasSkillEffectData('tgtMpLessPct'):
        tgtMpLessPct = skillEffectInfo.getSkillEffectData('tgtMpLessPct')
        if tgt.mp > tgtMpLessPct * getattr(tgt, 'mmp', 0) / 100.0:
            return False
    if skillEffectInfo.hasSkillEffectData('tgtMpNoLessPct'):
        tgtMpNoLessPct = skillEffectInfo.getSkillEffectData('tgtMpNoLessPct')
        if tgt.mp < tgtMpNoLessPct * getattr(tgt, 'mmp', 0) / 100.0:
            return False
    if skillEffectInfo.hasSkillEffectData('tgtFriendRelation'):
        if not srccd.rr.isFriend(tgt):
            return False
        relationType = skillEffectInfo.getSkillEffectData('tgtFriendRelation')
        if relationType == gametypes.SKILL_TGT_FRIEND_RELATION_TEAM_MATE:
            if not inSameGroup(src, tgt, True):
                return False
        elif relationType == gametypes.SKILL_TGT_FRIEND_RELATION_GROUP_MATE:
            if not inSameGroup(src, tgt, False):
                return False
        elif relationType == gametypes.SKILL_TGT_FRIEND_RELATION_TEAM_MATE_SUMMON_SPRITE:
            if not inSameGroup(src, tgt, True) or not tgt.IsSummonedSprite:
                return False
    if not IN_CLIENT and skillEffectInfo.getSkillEffectData('inHateUnits', 0) and src.IsAvatar:
        if tgt.id not in src.hateUnits:
            return False
    if skillEffectInfo.hasSkillEffectData('tgtUnitType'):
        tgtUnitType = skillEffectInfo.getSkillEffectData('tgtUnitType')
        if not utils.checkTgtUnitType(tgt, tgtUnitType):
            return False
    if skillEffectInfo.hasSkillEffectData('tgtNoUnitType'):
        tgtNoUnitType = skillEffectInfo.getSkillEffectData('tgtNoUnitType')
        if utils.checkTgtUnitType(tgt, tgtNoUnitType):
            return False
    if skillEffectInfo.hasSkillEffectData('tgtFriendType'):
        objType = skillEffectInfo.getSkillEffectData('tgtFriendType')
        if not checkTgtType(src, tgt, objType):
            return False
        if not srccd.rr.isFriend(tgt):
            return False
        if not checkHealSameGroup(src, tgt):
            return False
    elif skillEffectInfo.hasSkillEffectData('singleTgtFriendType'):
        objType = skillEffectInfo.getSkillEffectData('singleTgtFriendType')
        if not checkTgtType(src, tgt, objType):
            return False
        if not srccd.rr.isFriend(tgt):
            return False
        if not checkHealSameGroup(src, tgt):
            return False
    elif skillEffectInfo.hasSkillEffectData('tgtEnemyType'):
        objType = skillEffectInfo.getSkillEffectData('tgtEnemyType')
        if not checkTgtType(src, tgt, objType):
            return False
        if not srccd.rr.isEnemy(tgt):
            return False
    elif skillEffectInfo.hasSkillEffectData('singleTgtEnemyType'):
        objType = skillEffectInfo.getSkillEffectData('singleTgtEnemyType')
        if not checkTgtType(src, tgt, objType):
            return False
        if not srccd.rr.isEnemy(tgt):
            return False
    if skillEffectInfo.getSkillEffectData('tgtNotIncluded'):
        if getattr(srccd.owner, 'lockedId', 0) == tgt.id:
            return False
    if skillEffectInfo.getSkillEffectData('notIncludeCreation'):
        if tgt.IsSummonedBeast or tgt.IsCreation:
            return False
    if skillEffectInfo.hasSkillEffectData('tgtSchoolsLimit'):
        tgtSchoolsLimit = skillEffectInfo.getSkillEffectData('tgtSchoolsLimit')
        if tgt.IsAvatar and tgt.school not in tgtSchoolsLimit:
            return False
    if skillEffectInfo.hasSkillEffectData('tgtMhpCmpMine'):
        tgtMhpCmpMine = skillEffectInfo.getSkillEffectData('tgtMhpCmpMine')
        if tgtMhpCmpMine == const.SKILLEFFECT_PRECONDITION_TGT_MHP_CMP_MINE_MORE and tgt.mhp <= src.mhp:
            return False
        if tgtMhpCmpMine == const.SKILLEFFECT_PRECONDITION_TGT_MHP_CMP_MINE_LESS and tgt.mhp >= src.mhp:
            return False
    if not IN_CLIENT and skillEffectInfo.hasSkillEffectData('tgtDefenceRelation'):
        tgtDefenceRelation = skillEffectInfo.getSkillEffectData('tgtDefenceRelation')
        if tgtDefenceRelation == const.SKILLEFFECT_PRECONDITION_TGT_DEFENCE_RELATION_MORE_PHY and tgt.defence[0] <= tgt.defence[1]:
            return False
        if tgtDefenceRelation == const.SKILLEFFECT_PRECONDITION_TGT_DEFENCE_RELATION_MORE_MAG and tgt.defence[0] >= tgt.defence[1]:
            return False
    if not IN_CLIENT and skillEffectInfo.hasSkillEffectData('tgtHasSpecialAttr'):
        tgtHasSpecialAttr = skillEffectInfo.getSkillEffectData('tgtHasSpecialAttr', ())
        for attrId in tgtHasSpecialAttr:
            if attrId not in tgt.statesSpecialEffectCache and (attrId,) not in tgt.statesSpecialEffectCache:
                return False

    return True


def _checkSkillEffectTargetCache(srccd, tgt, skillEffectInfo, ttags, ftags):
    src = srccd.owner
    if not validCalcTgt(tgt):
        return False
    if isAvatarOnWingWorldCarrier(tgt):
        return False
    if isWithoutStateEx(tgt):
        if getattr(tgt, 'ownerId', tgt.id) == src.id:
            return False
        if not srccd.rr.isEnemy(tgt) or not tgt.isCUAlive(tgt) or formula.inProtect(tgt) or formula.inPVPProtect(tgt) and src.IsAvatar and src.IsSummonedSprite and not skillEffectInfo.isHealTypeEffect():
            return False
        return True
    if srccd.rr.isMagicField and srccd.rr.cc and hasattr(srccd.rr.cc, 'calcOnceForSingleTgt') and srccd.rr.cc.calcOnceForSingleTgt:
        if tgt.id in srccd.rr.cc.calcEntities:
            return False
    if tgt.getCUFlag(tgt, gametypes.FLAG_NOT_SKILL_TARGET) > 0:
        return False
    if (formula.inProtect(tgt) or formula.inPVPProtect(tgt) and (src.IsAvatar or src.IsSummonedSprite) and not skillEffectInfo.isHealTypeEffect()) and not (hasattr(srccd, 'ignoreProtect') and srccd.ignoreProtect > 0) and src.id != tgt.id:
        return False
    if tgt.IsSummonedSprite:
        if skillEffectInfo.getSkillEffectData('hurtType', 0) == gametypes.SKILL_HURT_ADD_MP and src.id != tgt.id:
            return False
    if ttags[SE_STATE] or not ftags[SE_STATE] and (skillEffectInfo.hasSkillEffectData('tgtStates') or skillEffectInfo.hasSkillEffectData('tgtNoStates') or skillEffectInfo.hasSkillEffectData('tgtStateGroup') or skillEffectInfo.hasSkillEffectData('tgtNoStateGroup')):
        if not ttags[SE_STATE]:
            ttags[SE_STATE] = True
        curTgtStates = {}
        if not IN_CLIENT or tgt == BigWorld.player():
            curTgtStates = {sid:(sum([ sVal[gametypes.STATE_INDEX_LAYER] for sVal in slst ]), [ sVal[gametypes.STATE_INDEX_SRCID] for sVal in slst ]) for sid, slst in tgt.statesServerAndOwn.iteritems()}
        else:
            curTgtStates = {sid:(sum([ sVal[gametypes.STATE_INDEX_LAYER] for sVal in slst ]), [ sVal[gametypes.STATE_INDEX_SRCID] for sVal in slst ]) for sid, slst in tgt.statesClientPub.iteritems()}
        tgtStates = skillEffectInfo.getSkillEffectData('tgtStates', [])
        if tgtStates:
            tgtStateLv = skillEffectInfo.getSkillEffectData('tgtStateLvl', 0)
            tgtStateSrc = skillEffectInfo.getSkillEffectData('tgtStateSrc', 0)
            checkType = tgtStates[0]
            tgtStates = tgtStates[1:] if checkType in (0, 1) else tgtStates
            tgtStateSrcId = src.id if tgtStateSrc else 0
            if checkType == 1:
                flag = False
                for stateId in tgtStates:
                    if _checkSingleState(curTgtStates, stateId, tgtStateLv, tgtStateSrcId):
                        flag = True
                        break

            else:
                flag = True
                for stateId in tgtStates:
                    if not _checkSingleState(curTgtStates, stateId, tgtStateLv, tgtStateSrcId):
                        flag = False
                        break

            if not flag:
                return False
        tgtNoStates = skillEffectInfo.getSkillEffectData('tgtNoStates', [])
        for s in tgtNoStates:
            if s in curTgtStates:
                return False

        curTgtStateIds = set(curTgtStates.keys())
        tgtStateGroup = skillEffectInfo.getSkillEffectData('tgtStateGroup', [])
        if tgtStateGroup:
            groupStates = getGroupStates(tgtStateGroup)
            if not curTgtStateIds & groupStates:
                return False
        tgtNoStateGroup = skillEffectInfo.getSkillEffectData('tgtNoStateGroup', [])
        if tgtNoStateGroup:
            groupStates = getGroupStates(tgtNoStateGroup)
            if curTgtStateIds & groupStates:
                return False
    elif not ftags[SE_STATE]:
        ftags[SE_STATE] = True
    if ttags[SE_SEX] or not ftags[SE_SEX] and skillEffectInfo.hasSkillEffectData('sexReq'):
        if not ttags[SE_SEX]:
            ttags[SE_SEX] = True
        sexReq = skillEffectInfo.getSkillEffectData('sexReq')
        if sexReq > 0 and tgt.IsAvatar and tgt.physique.sex != sexReq:
            return False
    elif not ftags[SE_SEX]:
        ftags[SE_SEX] = True
    if ttags[SE_HP_LESS] or not ftags[SE_HP_LESS] and skillEffectInfo.hasSkillEffectData('tgtHpLessPct'):
        if not ttags[SE_HP_LESS]:
            ttags[SE_HP_LESS] = True
        tgtHpLessPct = skillEffectInfo.getSkillEffectData('tgtHpLessPct')
        if tgt.hp > tgtHpLessPct * getattr(tgt, 'mhp', 0) / 100.0:
            return False
    elif not ftags[SE_HP_LESS]:
        ftags[SE_HP_LESS] = True
    if ttags[SE_HP_NO_LESS] or not ftags[SE_HP_NO_LESS] and skillEffectInfo.hasSkillEffectData('tgtHpNoLessPct'):
        if not ttags[SE_HP_NO_LESS]:
            ttags[SE_HP_NO_LESS] = True
        tgtHpNoLessPct = skillEffectInfo.getSkillEffectData('tgtHpNoLessPct')
        if tgt.hp < tgtHpNoLessPct * getattr(tgt, 'mhp', 0) / 100.0:
            return False
    elif not ftags[SE_HP_NO_LESS]:
        ftags[SE_HP_NO_LESS] = True
    if ttags[SE_MP_LESS] or not ftags[SE_MP_LESS] and skillEffectInfo.hasSkillEffectData('tgtMpLessPct'):
        if not ttags[SE_MP_LESS]:
            ttags[SE_MP_LESS] = True
        tgtMpLessPct = skillEffectInfo.getSkillEffectData('tgtMpLessPct')
        if tgt.mp > tgtMpLessPct * getattr(tgt, 'mmp', 0) / 100.0:
            return False
    elif not ftags[SE_MP_LESS]:
        ftags[SE_MP_LESS] = True
    if ttags[SE_MP_NO_LESS] or not ftags[SE_MP_NO_LESS] and skillEffectInfo.hasSkillEffectData('tgtMpNoLessPct'):
        if not ttags[SE_MP_NO_LESS]:
            ttags[SE_MP_NO_LESS] = True
        tgtMpNoLessPct = skillEffectInfo.getSkillEffectData('tgtMpNoLessPct')
        if tgt.mp < tgtMpNoLessPct * getattr(tgt, 'mmp', 0) / 100.0:
            return False
    elif not ftags[SE_MP_NO_LESS]:
        ftags[SE_MP_NO_LESS] = True
    if ttags[SE_FRIEND] or not ftags[SE_FRIEND] and skillEffectInfo.hasSkillEffectData('tgtFriendRelation'):
        if not ttags[SE_FRIEND]:
            ttags[SE_FRIEND] = True
        if not srccd.rr.isFriend(tgt):
            return False
        relationType = skillEffectInfo.getSkillEffectData('tgtFriendRelation')
        if relationType == gametypes.SKILL_TGT_FRIEND_RELATION_TEAM_MATE:
            if not inSameGroup(src, tgt, True):
                return False
        elif relationType == gametypes.SKILL_TGT_FRIEND_RELATION_GROUP_MATE:
            if not inSameGroup(src, tgt, False):
                return False
        elif relationType == gametypes.SKILL_TGT_FRIEND_RELATION_TEAM_MATE_SUMMON_SPRITE:
            if not inSameGroup(src, tgt, True) or not tgt.IsSummonedSprite:
                return False
    elif not ftags[SE_FRIEND]:
        ftags[SE_FRIEND] = True
    if not IN_CLIENT and src.IsAvatar:
        if ttags[SE_HATE] or not ftags[SE_HATE] and skillEffectInfo.hasSkillEffectData('inHateUnits'):
            if not ttags[SE_HATE]:
                ttags[SE_HATE] = True
            if tgt.id not in src.hateUnits:
                return False
        elif not ftags[SE_HATE]:
            ftags[SE_HATE] = True
    if ttags[SE_UNIT_TYPE] or not ftags[SE_UNIT_TYPE] and skillEffectInfo.hasSkillEffectData('tgtUnitType'):
        if not ttags[SE_UNIT_TYPE]:
            ttags[SE_UNIT_TYPE] = True
        tgtUnitType = skillEffectInfo.getSkillEffectData('tgtUnitType')
        if not utils.checkTgtUnitType(tgt, tgtUnitType):
            return False
    elif not ftags[SE_UNIT_TYPE]:
        ftags[SE_UNIT_TYPE] = True
    if ttags[SE_NO_UNIT_TYPE] or not ftags[SE_NO_UNIT_TYPE] and skillEffectInfo.hasSkillEffectData('tgtNoUnitType'):
        if not ttags[SE_NO_UNIT_TYPE]:
            ttags[SE_NO_UNIT_TYPE] = True
        tgtNoUnitType = skillEffectInfo.getSkillEffectData('tgtNoUnitType')
        if utils.checkTgtUnitType(tgt, tgtNoUnitType):
            return False
    elif not ftags[SE_NO_UNIT_TYPE]:
        ftags[SE_NO_UNIT_TYPE] = True
    if ttags[SE_FRIEND_TYPE] or not ftags[SE_FRIEND_TYPE] and skillEffectInfo.hasSkillEffectData('tgtFriendType'):
        if not ttags[SE_FRIEND_TYPE]:
            ttags[SE_FRIEND_TYPE] = True
        objType = skillEffectInfo.getSkillEffectData('tgtFriendType')
        if not checkTgtType(src, tgt, objType):
            return False
        if not srccd.rr.isFriend(tgt):
            return False
        if not checkHealSameGroup(src, tgt):
            return False
    else:
        if not ftags[SE_FRIEND_TYPE]:
            ftags[SE_FRIEND_TYPE] = True
        if ttags[SE_S_FRIEND_TYPE] or not ftags[SE_S_FRIEND_TYPE] and skillEffectInfo.hasSkillEffectData('singleTgtFriendType'):
            if not ttags[SE_S_FRIEND_TYPE]:
                ttags[SE_S_FRIEND_TYPE] = True
            objType = skillEffectInfo.getSkillEffectData('singleTgtFriendType')
            if not checkTgtType(src, tgt, objType):
                return False
            if not srccd.rr.isFriend(tgt):
                return False
            if not checkHealSameGroup(src, tgt):
                return False
        else:
            if not ftags[SE_S_FRIEND_TYPE]:
                ftags[SE_S_FRIEND_TYPE] = True
            if ttags[SE_ENEMY_TYPE] or not ftags[SE_ENEMY_TYPE] and skillEffectInfo.hasSkillEffectData('tgtEnemyType'):
                if not ttags[SE_ENEMY_TYPE]:
                    ttags[SE_ENEMY_TYPE] = True
                objType = skillEffectInfo.getSkillEffectData('tgtEnemyType')
                if not checkTgtType(src, tgt, objType):
                    return False
                if not srccd.rr.isEnemy(tgt):
                    return False
            else:
                if not ftags[SE_ENEMY_TYPE]:
                    ftags[SE_ENEMY_TYPE] = True
                if ttags[SE_S_ENEMY_TYPE] or not ftags[SE_S_ENEMY_TYPE] and skillEffectInfo.hasSkillEffectData('singleTgtEnemyType'):
                    if not ttags[SE_S_ENEMY_TYPE]:
                        ttags[SE_S_ENEMY_TYPE] = True
                    objType = skillEffectInfo.getSkillEffectData('singleTgtEnemyType')
                    if not checkTgtType(src, tgt, objType):
                        return False
                    if not srccd.rr.isEnemy(tgt):
                        return False
                elif not ftags[SE_S_ENEMY_TYPE]:
                    ftags[SE_S_ENEMY_TYPE] = True
    if ttags[SE_NOT_INCLUDE] or not ftags[SE_NOT_INCLUDE] and skillEffectInfo.hasSkillEffectData('tgtNotIncluded'):
        if not ttags[SE_NOT_INCLUDE]:
            ttags[SE_NOT_INCLUDE] = True
        if getattr(srccd.owner, 'lockedId', 0) == tgt.id:
            return False
    elif not ftags[SE_NOT_INCLUDE]:
        ftags[SE_NOT_INCLUDE] = True
    if ttags[SE_NOT_INCLUDE_CREATION] or not ftags[SE_NOT_INCLUDE_CREATION] and skillEffectInfo.hasSkillEffectData('notIncludeCreation'):
        if not ttags[SE_NOT_INCLUDE_CREATION]:
            ttags[SE_NOT_INCLUDE_CREATION] = True
        if tgt.IsSummonedBeast or tgt.IsCreation:
            return False
    elif not ftags[SE_NOT_INCLUDE_CREATION]:
        ftags[SE_NOT_INCLUDE_CREATION] = True
    if ttags[SE_SCHOOL] or not ftags[SE_SCHOOL] and skillEffectInfo.hasSkillEffectData('tgtSchoolsLimit'):
        if not ttags[SE_SCHOOL]:
            ttags[SE_SCHOOL] = True
        tgtSchoolsLimit = skillEffectInfo.getSkillEffectData('tgtSchoolsLimit')
        if tgt.IsAvatar and tgt.school not in tgtSchoolsLimit:
            return False
    elif not ftags[SE_SCHOOL]:
        ftags[SE_SCHOOL] = True
    if ttags[SE_MHP_AND_MINE] or not ftags[SE_MHP_AND_MINE] and skillEffectInfo.hasSkillEffectData('tgtMhpCmpMine'):
        if not ttags[SE_MHP_AND_MINE]:
            ttags[SE_MHP_AND_MINE] = True
        tgtMhpCmpMine = skillEffectInfo.getSkillEffectData('tgtMhpCmpMine')
        if tgtMhpCmpMine == const.SKILLEFFECT_PRECONDITION_TGT_MHP_CMP_MINE_MORE and tgt.mhp <= src.mhp:
            return False
        if tgtMhpCmpMine == const.SKILLEFFECT_PRECONDITION_TGT_MHP_CMP_MINE_LESS and tgt.mhp >= src.mhp:
            return False
    elif not ftags[SE_MHP_AND_MINE]:
        ftags[SE_MHP_AND_MINE] = True
    if not IN_CLIENT:
        if ttags[SE_DEFENCE_RELATION] or not ftags[SE_DEFENCE_RELATION] and skillEffectInfo.hasSkillEffectData('tgtDefenceRelation'):
            if not ttags[SE_DEFENCE_RELATION]:
                ttags[SE_DEFENCE_RELATION] = True
            tgtDefenceRelation = skillEffectInfo.getSkillEffectData('tgtDefenceRelation')
            if tgtDefenceRelation == const.SKILLEFFECT_PRECONDITION_TGT_DEFENCE_RELATION_MORE_PHY and tgt.defence[0] <= src.defence[1]:
                return False
            if tgtDefenceRelation == const.SKILLEFFECT_PRECONDITION_TGT_DEFENCE_RELATION_MORE_MAG and tgt.defence[0] >= src.defence[1]:
                return False
        elif not ftags[SE_DEFENCE_RELATION]:
            ftags[SE_DEFENCE_RELATION] = True
    if not IN_CLIENT:
        if ttags[SE_SPECIAL_ATTR] or not ftags[SE_SPECIAL_ATTR] and skillEffectInfo.hasSkillEffectData('tgtHasSpecialAttr'):
            if not ttags[SE_SPECIAL_ATTR]:
                ttags[SE_SPECIAL_ATTR] = True
            if skillEffectInfo.hasSkillEffectData('tgtHasSpecialAttr'):
                tgtHasSpecialAttr = skillEffectInfo.getSkillEffectData('tgtHasSpecialAttr', ())
                for attrId in tgtHasSpecialAttr:
                    if attrId not in tgt.statesSpecialEffectCache and (attrId,) not in tgt.statesSpecialEffectCache:
                        return False

        elif not ftags[SE_SPECIAL_ATTR]:
            ftags[SE_SPECIAL_ATTR] = True
    return True


def checkTgtType(src, tgt, objType):
    if objType == gametypes.OBJ_TYPE_CREATURE:
        if not tgt.isCUAlive(tgt):
            return False
    elif objType == gametypes.OBJ_TYPE_CONSTRUCT:
        pass
    elif objType == gametypes.OBJ_TYPE_TRAP:
        pass
    elif objType == gametypes.OBJ_TYPE_DEAD_BODY:
        if tgt.isCUAlive(tgt):
            return False
    elif objType == gametypes.OBJ_TYPE_SUMMON_SPRITE:
        if not tgt.IsSummonedSprite:
            return False
    return True


def checkHealSameGroup(src, tgt):
    if src and (src.IsSummoned or src.IsCreation and src.IsCombatCreation):
        src = BigWorld.entities.get(src.ownerId)
    if tgt and (tgt.IsSummoned or tgt.IsCreation and tgt.IsCombatCreation):
        tgt = BigWorld.entities.get(tgt.ownerId)
    if not src or not tgt:
        return True
    if checkLimitPk(src):
        return True
    if src.IsAvatarOrPuppet and tgt.IsAvatarOrPuppet:
        if src.id == tgt.id:
            return True
        if src.groupNUID and src.groupNUID == tgt.groupNUID:
            return True
        if src.pkStatus == const.PK_STATUS_WHITE and tgt.pkStatus == const.PK_STATUS_WHITE:
            return True
        if src.inWorldWarEx() and src.getWorldWarSide() == tgt.getWorldWarSide():
            return True
        if BigWorld.component == 'client':
            BigWorld.player().showGameMsg(GMDD.data.NOT_GROUP_WHITE_HEAL, ())
        return False
    return True


def checkLimitPk(src):
    if not src:
        return True
    mapId = formula.getMapId(src.spaceNo)
    mData = MCD.data.get(mapId)
    if mData and mData.get('limitPk'):
        return True
    return False


def checkLimitSprite(spaceNo):
    mapId = formula.getMapId(spaceNo)
    if gameconfig.enableSummonedSpriteInCWAndWMD() and mapId in const.ENABLE_SUMMONED_SPRITE_SPECIAL_MAP_ID:
        return False
    mData = MCD.data.get(mapId)
    if mData and not mData.get('allowSprite', 0):
        return True
    return False


def inSameGroup(src, tgt, checkGroupTeam = False):
    if not tgt.IsAvatarOrPuppet:
        if checkGroupTeam:
            if src.IsSummoned:
                if src.ownerId == 0:
                    return False
                src = BigWorld.entities.get(src.ownerId)
            if src and src.IsAvatarOrPuppet and tgt.IsMonster and hasattr(tgt, 'isTeamMate') and tgt.isTeamMate and src.inFuben():
                return True
        if src and src.IsAvatarOrPuppet and tgt.IsSummonedSprite:
            summonedSpriteOwner = BigWorld.entities.get(tgt.ownerId)
            if summonedSpriteOwner and inSameGroup(src, summonedSpriteOwner, checkGroupTeam):
                return True
        return False
    if src.inDuelZone():
        if src.IsSummoned or src.IsCreation and src.IsCombatCreation:
            if src.ownerId == 0:
                return False
            owner = BigWorld.entities.get(src.ownerId)
            if not owner:
                return False
            elif owner.id == tgt.id:
                return True
            elif owner.tempCamp == tgt.tempCamp:
                return True
            else:
                return False
        if src.tCamp != tgt.tCamp:
            return False
        else:
            return True
    else:
        if src.id == tgt.id:
            return True
        if src.IsSummoned:
            if src.ownerId == 0:
                return False
            owner = BigWorld.entities.get(src.ownerId)
            if not owner:
                return False
            elif owner.id == tgt.id:
                return True
            elif getattr(owner, 'groupNUID', 0) == 0 or getattr(owner, 'groupNUID', 0) != getattr(tgt, 'groupNUID', 0) or checkGroupTeam and not utils.isSameTeam(getattr(owner, 'groupIndex', 0), getattr(tgt, 'groupIndex', 0)):
                return False
            else:
                return True
        elif src.IsAvatarOrPuppet:
            if src.groupNUID == 0 or tgt.groupNUID == 0:
                return False
            elif src.groupNUID != tgt.groupNUID or checkGroupTeam and not utils.isSameTeam(getattr(src, 'groupIndex', 0), getattr(tgt, 'groupIndex', 0)):
                return False
            else:
                return True
        else:
            return False


def processVirturalCalcUnit(l):
    res = set()
    for u in l:
        if u.IsVirtualCalcUnit:
            owner = BigWorld.entities.get(u.ownerId)
            if owner:
                res.add(owner)
        else:
            res.add(u)

    return res


def calcAreaSkillEffectList(srccd, tgtcd, skillEffectInfo, forceCenter):
    src = srccd.owner
    tgt = tgtcd.owner
    if tgtcd.virtualMonster:
        tgt = tgtcd.virtualMonster
    if hasattr(srccd.rr, 'cc') and srccd.rr.cc:
        src = srccd.rr.cc
    result = []
    areaCenter = skillEffectInfo.getSkillEffectData('areaCenter', gametypes.SKILL_USER)
    areaType = skillEffectInfo.getSkillEffectData('areaType')
    areaParam = skillEffectInfo.getAreaParam()
    selfIncluded = skillEffectInfo.getSkillEffectData('selfIncluded', 0)
    tgtNotIncluded = skillEffectInfo.getSkillEffectData('tgtNotIncluded', 0)
    offsetAngle = skillEffectInfo.getSkillEffectData('offsetAngle', 0)
    offsetAngle = offsetAngle * 2 * math.pi / 360
    offsetPos = skillEffectInfo.getSkillEffectData('offsetPos', None)
    tgtIncluded = skillEffectInfo.getSkillEffectData('tgtIncluded', 0)
    key = (areaCenter,
     areaType,
     areaParam,
     selfIncluded,
     tgtNotIncluded,
     offsetAngle,
     offsetPos)
    if srccd.effectListCache and key in srccd.effectListCache:
        return srccd.effectListCache[key]
    if skillEffectInfo.hasSkillEffectData('rAreaCenter'):
        not IN_CLIENT and __calcRandomAreaCenter(srccd, tgtcd, skillEffectInfo)
    if areaType == gametypes.SKILL_AREA_SPHERE:
        radius = areaParam[0]
        if radius <= 0:
            gamelog.error('wrong radius for sphere area, return %f' % radius)
        if areaCenter == gametypes.SKILL_USER:
            centerPos = calcPosOffset(src, offsetPos) if offsetPos else src.position
            result = __skillEntitiesInSphere(src, radius, centerPos)
            if selfIncluded > 0:
                result.append(src)
        elif areaCenter == gametypes.SKILL_TARGET:
            if forceCenter:
                centerPos = forceCenter.position
                result = __skillEntitiesInSphere(forceCenter, radius, centerPos)
                if not tgtNotIncluded > 0:
                    result.append(forceCenter)
            else:
                centerPos = calcPosOffset(tgt, offsetPos) if offsetPos else tgt.position
                result = __skillEntitiesInSphere(tgt, radius, centerPos)
                if not tgtNotIncluded > 0:
                    result.append(tgt)
        elif areaCenter == gametypes.SKILL_POSITION:
            if not hasattr(skillEffectInfo, 'targetPosition') or not skillEffectInfo.targetPosition:
                not IN_CLIENT and gameengine.reportCritical('damn, you should config area center! %d' % skillEffectInfo.num)
            else:
                result = __skillEntitiesInSphere(src, radius, skillEffectInfo.targetPosition)
    elif areaType == gametypes.SKILL_AREA_CYLINDER:
        radius, height, depth, _ = areaParam
        if radius <= 0:
            gamelog.error('wrong radius for sphere area, return %f' % radius)
        if not depth:
            depth = 5
        if areaCenter == gametypes.SKILL_USER:
            centerPos = calcPosOffset(src, offsetPos) if offsetPos else src.position
            result = __skillEntitiesInRange(src, radius, height, depth, centerPos, selfIncluded)
        elif areaCenter == gametypes.SKILL_TARGET:
            if forceCenter:
                centerPos = forceCenter.position
                result = __skillEntitiesInRange(forceCenter, radius, height, depth, centerPos, selfIncluded)
                if not tgtNotIncluded > 0:
                    result.append(forceCenter)
            else:
                centerPos = calcPosOffset(tgt, offsetPos) if offsetPos else tgt.position
                result = __skillEntitiesInRange(tgt, radius, height, depth, centerPos, selfIncluded)
                if not tgtNotIncluded > 0:
                    result.append(tgt)
        elif areaCenter == gametypes.SKILL_POSITION:
            if not hasattr(skillEffectInfo, 'targetPosition') or not skillEffectInfo.targetPosition:
                not IN_CLIENT and gameengine.reportCritical('damn, you should config area center! %d' % skillEffectInfo.num)
            else:
                result = __skillEntitiesInRange(src, radius, height, depth, skillEffectInfo.targetPosition, selfIncluded)
    elif areaType == gametypes.SKILL_AREA_CUBE:
        length, width, height, depth = areaParam
        if forceCenter:
            centerPos = calcPosOffset(forceCenter, offsetPos) if offsetPos else forceCenter.position
            result = __skillEntitiesInCube(forceCenter, width, length, height, depth, centerPos, offsetAngle)
        else:
            if skillEffectInfo.getSkillEffectData('offsetTarget'):
                offsetAngle = (tgt.position - src.position).yaw - src.yaw
            centerPos = calcPosOffset(src, offsetPos) if offsetPos else src.position
            result = __skillEntitiesInCube(src, width, length, height, depth, centerPos, offsetAngle)
    elif areaType == gametypes.SKILL_AREA_RADIAN:
        radius, height, radian, depth = areaParam
        radian = radian * math.pi / 360
        if radius <= 0 or height <= 0:
            gamelog.error('wrong radius or radian for radian area, return %f, %f' % (radius, radian))
        if areaCenter == gametypes.SKILL_USER:
            centerPos = calcPosOffset(src, offsetPos) if offsetPos else src.position
            if skillEffectInfo.getSkillEffectData('offsetTarget'):
                offsetAngle = (tgt.position - src.position).yaw - src.yaw
            result = __skillEntitiesInFOV(src, radius, radian, height, depth, offsetAngle, centerPos)
            if selfIncluded > 0:
                result.append(src)
        elif areaCenter == gametypes.SKILL_TARGET:
            centerPos = calcPosOffset(tgt, offsetPos) if offsetPos else tgt.position
            result = __skillEntitiesInFOV(tgt, radius, radian, height, depth, offsetAngle, centerPos)
            if not tgtNotIncluded > 0:
                result.append(tgt)
    elif areaType == gametypes.SKILL_AREA_TARGET_LINE:
        width = areaParam[0]
        height = areaParam[1]
        depth = areaParam[2]
        if not depth:
            depth = 5
        offsetAngle = (tgt.position - src.position).yaw - src.yaw
        length = distance3D(src.position, tgt.position)
        if forceCenter:
            result = __skillEntitiesInCube(forceCenter, width, length, height, depth, forceCenter.position, offsetAngle)
        else:
            result = __skillEntitiesInCube(src, width, length, height, depth, src.position, offsetAngle)
        if not tgtNotIncluded > 0:
            result.append(tgt)
    elif areaType == gametypes.SKILL_AREA_RING:
        iRadius, oRadius, height, depth = areaParam
        if areaCenter == gametypes.SKILL_USER:
            centerPos = calcPosOffset(src, offsetPos) if offsetPos else src.position
            result, centerInResult = __skillEntitiesInRing(src, iRadius, oRadius, height, depth, centerPos)
            if selfIncluded and not centerInResult:
                result.append(src)
        elif areaCenter == gametypes.SKILL_TARGET:
            if forceCenter:
                centerPos = forceCenter.position
                result, centerInResult = __skillEntitiesInRing(forceCenter, iRadius, oRadius, height, depth, centerPos)
                if tgtIncluded and not centerInResult:
                    result.append(forceCenter)
            else:
                centerPos = calcPosOffset(tgt, offsetPos) if offsetPos else tgt.position
                result, centerInResult = __skillEntitiesInRing(tgt, iRadius, oRadius, height, depth, centerPos)
                if tgtIncluded and not centerInResult:
                    result.append(tgt)
        elif areaCenter == gametypes.SKILL_POSITION:
            if not hasattr(skillEffectInfo, 'targetPosition') or not skillEffectInfo.targetPosition:
                if not IN_CLIENT:
                    gameengine.reportCritical('damn, you should config area center! %d' % skillEffectInfo.num)
            else:
                result, centerInResult = __skillEntitiesInRing(src, iRadius, oRadius, height, depth, skillEffectInfo.targetPosition)
    srccd.effectListCache[key] = result
    return result


def __skillEntitiesInRing(src, innerRadius, outerRadius, height, depth, centerPos = None):
    es = src.entitiesInRange(outerRadius + src.getMaxTgtBodySize(), None, centerPos)
    centerInResult = False
    if centerPos == None:
        centerPos = src.position
    if utils.needShowScopeDebug(src, gametypes.SCOPCE_TYPE_CALC_DEBUG):
        if IN_CLIENT:
            src.showScopeViewDebug(gametypes.SCOPCE_TYPE_CALC_DEBUG, (gametypes.CALC_SCOPCE_TYPE_RING,
             centerPos,
             innerRadius,
             outerRadius,
             height))
        else:
            src.allClients.showScopeViewDebug(gametypes.SCOPCE_TYPE_CALC_DEBUG, (gametypes.CALC_SCOPCE_TYPE_RING,
             centerPos,
             innerRadius,
             outerRadius,
             height))
    res = []
    es.append(src)
    curSpaceNo = getCurrentSpaceNo(src)
    if formula.spaceInWingWarCity(curSpaceNo):
        rs = getWingWorldWarCityGlobalTgt(curSpaceNo)
        if rs:
            es = set(es) | rs
    for e in es:
        if not validCalcTgt(e):
            continue
        if not -depth <= e.position[1] - centerPos[1] <= height:
            continue
        dist = distance2D(centerPos, e.position)
        if dist - e.bodySize < innerRadius or outerRadius + e.bodySize < dist:
            continue
        res.append(e)
        if e.id == src.id:
            centerInResult = True

    return (res, centerInResult)


def checkTgtInRing(tgt, innerRadius, outerRadius, dist, height, depth, centerPos):
    if not -depth <= tgt.position[1] - centerPos[1] <= height:
        return False
    if dist - tgt.bodySize < innerRadius or outerRadius + tgt.bodySize < dist:
        return False
    return True


def __skillEntitiesInFOV(src, radii, radian, height, depth, offsetAngle, centerPos = None):
    res = []
    yaw = src.yaw + offsetAngle
    if yaw > math.pi:
        yaw -= 2 * math.pi
    if not centerPos:
        centerPos = src.position
    es = src.entitiesInRangeFOV(radii + src.getMaxTgtBodySize(), radian, None, centerPos, formula.pitchYawToVector(0.0, yaw))
    if utils.needShowScopeDebug(src, gametypes.SCOPCE_TYPE_CALC_DEBUG):
        if not IN_CLIENT:
            src.allClients.showScopeViewDebug(gametypes.SCOPCE_TYPE_CALC_DEBUG, (gametypes.CALC_SCOPCE_TYPE_RADIAN,
             src.position,
             centerPos,
             radii,
             radian,
             height,
             yaw))
        else:
            src.showScopeViewDebug(gametypes.SCOPCE_TYPE_CALC_DEBUG, (gametypes.CALC_SCOPCE_TYPE_RADIAN,
             src.position,
             centerPos,
             radii,
             radian,
             height,
             yaw))
    curSpaceNo = getCurrentSpaceNo(src)
    if formula.spaceInWingWarCity(curSpaceNo):
        rs = getWingWorldWarCityGlobalTgt(curSpaceNo)
        if rs:
            es = set(es) | rs
    for e in es:
        if e.id == src.id:
            continue
        if not validCalcTgt(e):
            continue
        if not -depth <= e.position[1] - centerPos[1] <= height:
            continue
        res.append(e)

    res = filter(lambda m: _caclRangeRadian(src, m, offsetAngle, radii, 2 * radian, centerPos), res)
    return res


@commcython.cythonfuncentry
def _caclRangeRadian(src, tgt, offsetAngle, radii, radian, centerPos):
    """
    @cython.locals(offsetAngle=cython.float, radii=cython.float, radian=cython.float, cx=cython.float, cz=cython.float,
        cr=cython.float, v=cython.float, px1=cython.float, pz1=cython.float, px2=cython.float, pz2=cython.float,
        a=cython.float, halfPi=cython.float, maxa=cython.float, mina=cython.float)
    """
    if not centerPos:
        centerPos = src.position
    m = Math.Matrix()
    if IN_CLIENT:
        m.setRotateYPR(Math.Vector3(src.yaw + offsetAngle, 0.0, 0))
    else:
        m.setRotateYPR(Math.Vector3(src.direction[2] + offsetAngle, 0.0, src.direction[0]))
    m2 = Math.Matrix()
    m2.setTranslate(centerPos)
    m.postMultiply(m2)
    m.invert()
    pos = m.applyPoint(Math.Vector3(tgt.position[0], tgt.position[1], tgt.position[2]))
    cx = pos[0]
    cz = pos[2]
    cr = tgt.bodySize
    if cx * cx + cz * cz > (cr + radii) * (cr + radii):
        return False
    v = formula.pitchYawToVector(0, radian / 2)
    px1, pz1 = v[0] * radii, v[2] * radii
    px2, pz2 = -px1, pz1
    if sMath.circleIntersectLineSegment2D(cx, cz, cr, px1, pz1) or sMath.circleIntersectLineSegment2D(cx, cz, cr, px2, pz2):
        return True
    a = math.atan2(cz, cx)
    halfPi = math.pi / 2
    maxa = halfPi + radian / 2
    mina = halfPi - radian / 2
    if radian > math.pi:
        if a > 0:
            return True
        elif a > -halfPi:
            return a >= mina
        else:
            return a <= maxa - 2 * math.pi
    else:
        return a >= mina and a <= maxa


def _caclRangeRadianWithHeight(src, tgt, offsetAngle, radii, radian, height, depth, centerPos):
    if not -depth <= tgt.position[1] - centerPos[1] <= height:
        return False
    return _caclRangeRadian(src, tgt, offsetAngle, radii, radian, centerPos)


def __skillEntitiesInCube(src, width, length, height, depth, centerPos = None, offsetAngle = 0):
    res = []
    width /= 2.0
    yaw = src.yaw + offsetAngle
    while yaw > math.pi:
        yaw -= 2 * math.pi

    bodySizeFix = src.getMaxTgtBodySize()
    es = src.entitiesInRangeCube(width + bodySizeFix, length + bodySizeFix, False, None, centerPos, formula.pitchYawToVector(src.pitch, yaw))
    if utils.needShowScopeDebug(src, gametypes.SCOPCE_TYPE_CALC_DEBUG):
        if not IN_CLIENT:
            src.allClients.showScopeViewDebug(gametypes.SCOPCE_TYPE_CALC_DEBUG, (gametypes.CALC_SCOPCE_TYPE_CUBE,
             src.position,
             centerPos,
             width,
             length,
             height,
             yaw))
        else:
            src.showScopeViewDebug(gametypes.SCOPCE_TYPE_CALC_DEBUG, (gametypes.CALC_SCOPCE_TYPE_CUBE,
             src.position,
             centerPos,
             width,
             length,
             height,
             yaw))
    curSpaceNo = getCurrentSpaceNo(src)
    if formula.spaceInWingWarCity(curSpaceNo):
        rs = getWingWorldWarCityGlobalTgt(curSpaceNo)
        if rs:
            es = set(es) | rs
    for e in es:
        if e.id == src.id:
            continue
        if not validCalcTgt(e):
            continue
        if not -depth <= e.position[1] - centerPos[1] <= height:
            continue
        res.append(e)

    res = filter(lambda m: _calcRangeCube(src, m, offsetAngle, math.sqrt(width * width + length * length), length, width, centerPos), res)
    return res


def _calcRangeCube(src, tgt, offsetAngle, diagonal, depth, width, centerPos):
    if not centerPos:
        centerPos = src.position
    m = Math.Matrix()
    if IN_CLIENT:
        m.setRotateYPR(Math.Vector3(src.yaw + offsetAngle, 0, 0))
    else:
        m.setRotateYPR(Math.Vector3(src.direction[2] + offsetAngle, 0, src.direction[0]))
    m2 = Math.Matrix()
    m2.setTranslate(centerPos)
    m.postMultiply(m2)
    m.invert()
    pos = m.applyPoint(Math.Vector3(tgt.position[0], tgt.position[1], tgt.position[2]))
    return sMath.circleIntersectRectange2D(pos[0], pos[2], tgt.bodySize, -width, 0, width, depth)


def _calcRangeCubeWithHeight(src, tgt, offsetAngle, length, height, depth, width, centerPos):
    width /= 2.0
    if not -depth <= tgt.position[1] - centerPos[1] <= height:
        return False
    diagonal = math.sqrt(width * width + length * length)
    return _calcRangeCube(src, tgt, offsetAngle, diagonal, length, width, centerPos)


def __skillEntitiesInRange(src, radii, height, depth, centerPos = None, selfIncluded = 0):
    res = []
    es = src.entitiesInRange(radii + src.getMaxTgtBodySize(), None, centerPos)
    if centerPos == None:
        centerPos = src.position
    if utils.needShowScopeDebug(src, gametypes.SCOPCE_TYPE_CALC_DEBUG):
        if not IN_CLIENT:
            src.allClients.showScopeViewDebug(gametypes.SCOPCE_TYPE_CALC_DEBUG, (gametypes.CALC_SCOPCE_TYPE_CYLINDER,
             centerPos,
             radii,
             height,
             depth))
        else:
            src.showScopeViewDebug(gametypes.SCOPCE_TYPE_CALC_DEBUG, (gametypes.CALC_SCOPCE_TYPE_CYLINDER,
             centerPos,
             radii,
             height,
             depth))
    curSpaceNo = getCurrentSpaceNo(src)
    if formula.spaceInWingWarCity(curSpaceNo):
        rs = getWingWorldWarCityGlobalTgt(curSpaceNo)
        if rs:
            es = set(es) | rs
    for e in es:
        if e.id == src.id:
            continue
        if not validCalcTgt(e):
            continue
        if not -depth <= e.position[1] - centerPos[1] <= height:
            continue
        res.append(e)

    if selfIncluded > 0 and validCalcTgt(src):
        res.append(src)
    res = filter(lambda m: _calcRange(src, m, radii, centerPos), res)
    return res


def __calcRandomAreaCenter(srccd, tgtcd, skillEffectInfo):
    if not skillEffectInfo.hasSkillEffectData('rAreaCenter'):
        return
    areaCenter = skillEffectInfo.getSkillEffectData('rAreaCenter')
    areaType = skillEffectInfo.getSkillEffectData('rAreaType')
    areaParam = skillEffectInfo.getSkillEffectData('rAreaPa', (0, 0, 0))
    src = srccd.owner
    tgt = tgtcd.owner
    centerPos = None
    if areaCenter == gametypes.SKILL_USER:
        centerPos = src.position
    elif areaCenter == gametypes.SKILL_TARGET:
        centerPos = tgt.position
    elif areaCenter == gametypes.SKILL_POSITION:
        if not hasattr(skillEffectInfo, 'targetPosition') or not skillEffectInfo.targetPosition:
            not IN_CLIENT and gameengine.reportCritical('damn, you should config area center! %d' % skillEffectInfo.num)
        else:
            centerPos = skillEffectInfo.targetPosition
    if not centerPos:
        return
    if areaType == gametypes.SKILL_AREA_CYLINDER:
        radius, _, _ = areaParam
        if radius <= 0:
            gamelog.error('wrong radius for sphere area, return %f' % radius)
            return
        tgtPos = __genRandomPositionInCircle(src, centerPos, radius)
        skillEffectInfo.targetPosition = tgtPos
        srccd.rr.addRandomPos(tgtPos)


def calcRandomPosInRing(inR, outR):
    r = math.sqrt((outR * outR - inR * inR) * randomf() + inR * inR)
    deta = uniform(0, 2 * math.pi)
    return (r * math.sin(deta), 0, r * math.cos(deta))


def calcPosOffset(src, offset):
    if offset:
        if len(offset) != 3:
            if not IN_CLIENT:
                gameengine.reportCritical('offset pos should be (x, y, z)!')
            return src.position
        m = Math.Matrix()
        if IN_CLIENT:
            m.setRotateYPR(Math.Vector3(src.yaw, 0, 0))
        else:
            m.setRotateYPR(Math.Vector3(src.direction[2], 0, src.direction[0]))
        pos = m.applyPoint(Math.Vector3(offset[0], offset[1], offset[2]))
        return (src.position[0] + pos[0], src.position[1] + pos[1], src.position[2] + pos[2])
    else:
        return src.position


def __genRandomPositionInCircle(src, centerPos, radius):
    r = radius * math.sqrt(random())
    deta = uniform(0, 2 * math.pi)
    x = centerPos[0] + r * math.sin(deta)
    y = centerPos[1]
    z = centerPos[2] + r * math.cos(deta)
    try:
        tgtPos = BigWorld.findRandomNeighbourPoint(src.spaceID, (x, y, z), 0.5)
    except ValueError:
        return centerPos

    return tgtPos


def needShowCalcScopeDebug(src):
    if not gameconfig.publicServer() and gametypes.ENABLE_CALC_SCOPCE_DEBUG:
        if gametypes.CALC_SCOPCE_LIMIT_IDS:
            if src and src.id in gametypes.CALC_SCOPCE_LIMIT_IDS:
                return True
        else:
            return True
    return False


def __skillEntitiesInSphere(src, radii, centerPos = None):
    res = []
    es = src.entitiesInRange(radii + src.getMaxTgtBodySize(), None, centerPos)
    if centerPos == None:
        centerPos = src.position
    if utils.needShowScopeDebug(src, gametypes.SCOPCE_TYPE_CALC_DEBUG):
        if not IN_CLIENT:
            src.allClients.showScopeViewDebug(gametypes.SCOPCE_TYPE_CALC_DEBUG, (gametypes.CALC_SCOPCE_TYPE_SPHERE, centerPos, radii))
        else:
            src.showScopeViewDebug(gametypes.SCOPCE_TYPE_CALC_DEBUG, (gametypes.CALC_SCOPCE_TYPE_SPHERE, centerPos, radii))
    curSpaceNo = getCurrentSpaceNo(src)
    if formula.spaceInWingWarCity(curSpaceNo):
        rs = getWingWorldWarCityGlobalTgt(curSpaceNo)
        if rs:
            es = set(es) | rs
    for e in es:
        if e.id == src.id:
            continue
        if not validCalcTgt(e):
            continue
        res.append(e)

    res = filter(lambda m: _calcRange(src, m, radii, centerPos), res)
    return res


def _calcRange(src, m, atkRange, centerPos):
    if not centerPos:
        centerPos = src.position
    if not sMath.inRange2D(getattr(m, 'bodySize', 0) + atkRange, centerPos, m.position):
        return False
    return True


def _calcRangeWithHeight(src, tgt, radius, height, depth, centerPos):
    if not -depth <= tgt.position[1] - centerPos[1] <= height:
        return False
    return _calcRange(src, tgt, radius, centerPos)


def validCalcTgt(obj):
    if obj == None:
        return False
    elif IN_CLIENT:
        if not obj.inWorld:
            return False
        return getattr(obj, 'IsCombatUnit') or getattr(obj, 'IsVirtualCalcUnit', False)
    elif obj.isDestroyed:
        return False
    else:
        return obj.IsCombatUnit or obj.IsVirtualCalcUnit


def isAvatarOnWingWorldCarrier(obj):
    if obj == None:
        return False
    elif not getattr(obj, 'IsAvatar'):
        return False
    elif IN_CLIENT:
        return obj.checkInWingWorldCarrierStateOnClient()
    else:
        return obj.checkInWingWorldCarrierStateOnCell()


def getCurrentSpaceNo(src):
    if not IN_CLIENT:
        return src.spaceNo
    else:
        return BigWorld.player().spaceNo


def checkTargetAreaValid(srccd, tgt, skillEffectInfo, forceCenter):
    src = srccd.owner
    if srccd.rr.cc:
        src = srccd.rr.cc
    areaCenter = skillEffectInfo.getSkillEffectData('areaCenter', gametypes.SKILL_USER)
    areaType = skillEffectInfo.getSkillEffectData('areaType')
    areaParam = skillEffectInfo.getAreaParam()
    offsetAngle = skillEffectInfo.getSkillEffectData('offsetAngle', 0)
    offsetAngle = offsetAngle * 2 * math.pi / 360
    offsetPos = skillEffectInfo.getSkillEffectData('offsetPos', None)
    if areaType == gametypes.SKILL_AREA_SPHERE:
        radius = max(areaParam[0] * gametypes.MF_CLIENT_CALC_CHECK_RATE, areaParam[0] + 0.5)
        if radius <= 0:
            gamelog.error('wrong radius for sphere area, return %f' % radius)
        if areaCenter == gametypes.SKILL_USER:
            centerPos = calcPosOffset(src, offsetPos) if offsetPos else src.position
            return _calcRange(src, tgt, radius, centerPos)
        if areaCenter == gametypes.SKILL_TARGET:
            if forceCenter:
                centerPos = forceCenter.position
                return _calcRange(forceCenter, tgt, radius, centerPos)
            else:
                centerPos = calcPosOffset(tgt, offsetPos) if offsetPos else tgt.position
                return _calcRange(tgt, tgt, radius, centerPos)
        elif areaCenter == gametypes.SKILL_POSITION:
            if not hasattr(skillEffectInfo, 'targetPosition') or not skillEffectInfo.targetPosition:
                if not IN_CLIENT:
                    gameengine.reportCritical('damn, you should config area center! %d' % skillEffectInfo.num)
            else:
                return _calcRange(src, tgt, radius, skillEffectInfo.targetPosition)
    elif areaType == gametypes.SKILL_AREA_CYLINDER:
        radius, height, depth, _ = areaParam
        radius = max(radius * gametypes.MF_CLIENT_CALC_CHECK_RATE, radius + 0.5)
        height = max(height * gametypes.MF_CLIENT_CALC_CHECK_RATE, height + 0.5)
        depth = max(depth * gametypes.MF_CLIENT_CALC_CHECK_RATE, depth + 0.5)
        if radius <= 0:
            gamelog.error('wrong radius for sphere area, return %f' % radius)
        if not depth:
            depth = 5
        if areaCenter == gametypes.SKILL_USER:
            centerPos = calcPosOffset(src, offsetPos) if offsetPos else src.position
            return _calcRangeWithHeight(src, tgt, radius, height, depth, centerPos)
        if areaCenter == gametypes.SKILL_TARGET:
            if forceCenter:
                centerPos = forceCenter.position
                return _calcRangeWithHeight(forceCenter, tgt, radius, height, depth, centerPos)
            else:
                centerPos = calcPosOffset(tgt, offsetPos) if offsetPos else tgt.position
                return _calcRangeWithHeight(tgt, tgt, radius, height, depth, centerPos)
        elif areaCenter == gametypes.SKILL_POSITION:
            if not hasattr(skillEffectInfo, 'targetPosition') or not skillEffectInfo.targetPosition:
                if not IN_CLIENT:
                    gameengine.reportCritical('damn, you should config area center! %d' % skillEffectInfo.num)
            else:
                return _calcRangeWithHeight(src, tgt, radius, height, depth, skillEffectInfo.targetPosition)
    elif areaType == gametypes.SKILL_AREA_CUBE:
        length, width, height, depth = areaParam
        length = max(length * gametypes.MF_CLIENT_CALC_CHECK_RATE, length + 0.5)
        width = max(width * gametypes.MF_CLIENT_CALC_CHECK_RATE, width + 0.5)
        height = max(height * gametypes.MF_CLIENT_CALC_CHECK_RATE, height + 0.5)
        depth = max(depth * gametypes.MF_CLIENT_CALC_CHECK_RATE, depth + 0.5)
        if forceCenter:
            centerPos = calcPosOffset(forceCenter, offsetPos) if offsetPos else forceCenter.position
            return _calcRangeCubeWithHeight(forceCenter, tgt, offsetAngle, length, height, depth, width, centerPos)
        else:
            if skillEffectInfo.getSkillEffectData('offsetTarget'):
                offsetAngle = (tgt.position - src.position).yaw - src.yaw
            centerPos = calcPosOffset(src, offsetPos) if offsetPos else src.position
            return _calcRangeCubeWithHeight(src, tgt, offsetAngle, length, height, depth, width, centerPos)
    elif areaType == gametypes.SKILL_AREA_RADIAN:
        radius, height, radian, depth = areaParam
        radius = max(radius * gametypes.MF_CLIENT_CALC_CHECK_RATE, radius + 0.5)
        height = max(height * gametypes.MF_CLIENT_CALC_CHECK_RATE, height + 0.5)
        depth = max(depth * gametypes.MF_CLIENT_CALC_CHECK_RATE, depth + 0.5)
        radian = radian * math.pi / 360
        if radius <= 0 or height <= 0:
            gamelog.error('wrong radius or radian for radian area, return %f, %f' % (radius, radian))
        if areaCenter == gametypes.SKILL_USER:
            centerPos = calcPosOffset(src, offsetPos) if offsetPos else src.position
            if skillEffectInfo.getSkillEffectData('offsetTarget'):
                offsetAngle = (tgt.position - src.position).yaw - src.yaw
            return _caclRangeRadianWithHeight(src, tgt, offsetAngle, radius, radian, height, depth, centerPos)
        if areaCenter == gametypes.SKILL_TARGET:
            centerPos = calcPosOffset(tgt, offsetPos) if offsetPos else tgt.position
            return _caclRangeRadianWithHeight(tgt, tgt, offsetAngle, radius, radian, height, depth, centerPos)
    elif areaType == gametypes.SKILL_AREA_TARGET_LINE:
        width = max(areaParam[0] * gametypes.MF_CLIENT_CALC_CHECK_RATE, areaParam[0] + 0.5)
        height = max(areaParam[1] * gametypes.MF_CLIENT_CALC_CHECK_RATE, areaParam[1] + 0.5)
        depth = max(areaParam[2] * gametypes.MF_CLIENT_CALC_CHECK_RATE, areaParam[2] + 0.5)
        if not depth:
            depth = 5
        offsetAngle = (tgt.position - src.position).yaw - src.yaw
        length = distance3D(src.position, tgt.position)
        if forceCenter:
            centerPos = calcPosOffset(forceCenter, offsetPos) if offsetPos else forceCenter.position
            return _calcRangeCubeWithHeight(forceCenter, tgt, offsetAngle, length, height, depth, width, centerPos)
        else:
            centerPos = calcPosOffset(src, offsetPos) if offsetPos else src.position
            return _calcRangeCubeWithHeight(src, tgt, offsetAngle, length, height, depth, width, centerPos)
    elif areaType == gametypes.SKILL_AREA_RING:
        iRadius, oRadius, height, depth = areaParam
        oRadius = max(oRadius * gametypes.MF_CLIENT_CALC_CHECK_RATE, oRadius + 0.5)
        height = max(height * gametypes.MF_CLIENT_CALC_CHECK_RATE, height + 0.5)
        depth = max(depth * gametypes.MF_CLIENT_CALC_CHECK_RATE, depth + 0.5)
        if areaCenter == gametypes.SKILL_USER:
            centerPos = calcPosOffset(src, offsetPos) if offsetPos else src.position
            dist = distance2D(centerPos, tgt.position)
            return checkTgtInRing(tgt, iRadius, oRadius, dist, height, depth, centerPos)
        if areaCenter == gametypes.SKILL_TARGET:
            if forceCenter:
                centerPos = forceCenter.position
                dist = distance2D(centerPos, tgt.position)
                return checkTgtInRing(tgt, iRadius, oRadius, dist, height, depth, centerPos)
            else:
                centerPos = calcPosOffset(tgt, offsetPos) if offsetPos else tgt.position
                dist = distance2D(centerPos, tgt.position)
                return checkTgtInRing(tgt, iRadius, oRadius, dist, height, depth, centerPos)
        elif areaCenter == gametypes.SKILL_POSITION:
            if not hasattr(skillEffectInfo, 'targetPosition') or not skillEffectInfo.targetPosition:
                if not IN_CLIENT:
                    gameengine.reportCritical('damn, you should config area center! %d' % skillEffectInfo.num)
            else:
                dist = distance2D(tgt.position, skillEffectInfo.targetPosition)
                return checkTgtInRing(tgt, iRadius, oRadius, dist, height, depth, skillEffectInfo.targetPosition)
    return True


def calcCombatCreatorEffectEx(owner, cc, ccInfo, tgt, tickCnt, skillId):
    if ccInfo.getCombatCreationData('forceSkillEffectIds', ()):
        skillEffects, skillEffectLv = ccInfo.getCombatCreationData('forceSkillEffectIds')
    else:
        skillEffects, skillEffectLv = ccInfo.getCombatCreationData('effects', []), ccInfo.slv
    retValue = {}
    if ccInfo.getCombatCreationData('calcOnceForSingleTgt'):
        cc.calcOnceForSingleTgt = True
    srccd = CombatDataBase(owner, True)
    srccd.rr = ResultRecorderCommon(owner)
    srccd.rr.cc = cc
    srccd.rr.isMagicField = True
    tgtcd = CombatDataBase(tgt)
    for effect in skillEffects:
        if effect <= 0:
            continue
        skillEffectInfo = owner.getSkillEffectInfo(effect, skillEffectLv, skillId)
        if skillEffectInfo.hasSkillEffectData('creationCalcCnt') and tickCnt not in skillEffectInfo.getSkillEffectData('creationCalcCnt'):
            continue
        effectIdList = _calcSkillEffectList(srccd, tgtcd, skillEffectInfo, skillId)
        if effectIdList:
            retValue[effect] = [ e.id for e in effectIdList ]

    return retValue


def calcUseSkillEffect(src, tgt, skillInfo):
    srccd = CombatDataBase(src, True)
    srccd.rr = ResultRecorderCommon(src)
    srccd.rr.isMagicField = False
    tgtcd = CombatDataBase(tgt)
    skillEffects, _, _ = calcPSkillExtraEffect(src, srccd, skillInfo, ignoreHighLoad=False, isClient=True, tgt=tgt)
    res = {}
    for effect in skillEffects:
        if effect:
            skillEffectInfo = checkUseSkillEffect(srccd, tgtcd, skillInfo, effect)
            if skillEffectInfo:
                skillEffectInfo = commcalc.calcDataInfoAffectedByPSkill(src, skillEffectInfo, const.DATA_TYPE_SKILL_EFFECT_INFO, skillInfo.num)
                effectIdList = _calcSkillEffectList(srccd, tgtcd, skillEffectInfo, skillInfo.num)
                if effectIdList:
                    res[effect] = [ e.id for e in effectIdList ]
                else:
                    ses = skillEffectInfo.getSkillEffectData('ses')
                    if ses:
                        for seId, _, _ in ses:
                            if seId in gametypes.SKILL_SE_FORCE_CLIENT_CALC:
                                res[effect] = [src.id]

    return res


def _sortSkillEffectsByPriority(skillEffects):
    cmpList = []
    needSort = False
    for seId in skillEffects:
        priority = SED.data.get(seId, {}).get('priority', 0)
        cmpList.append((seId, priority))
        if priority:
            needSort = True

    if not needSort:
        return skillEffects
    sortCmpList = sorted(cmpList, cmp=lambda x, y: cmp(x[1], y[1]), reverse=True)
    seIds = [ c[0] for c in sortCmpList ]
    return seIds


@commcython.cythonfuncentry
def calcPSkillExtraEffect(owner, srccd, skillInfo, ignoreHighLoad, isClient = False, tgt = None):
    """
    @cython.locals(ignoreHighLoad=cython.bint, isClient=cython.bint, zaijuNo=cython.int, randomNum=cython.int, trigger=cython.int)
    """
    skillEffects, skillCreations, skillAuras = list(skillInfo.getSkillData('effects', [])), list(skillInfo.getSkillData('creations', [])), list(skillInfo.getSkillData('auras', []))
    if owner.IsAvatar and owner._isOnZaiju():
        zaijuNo = owner._getZaijuNo()
        if ZD.data.get(zaijuNo, {}).get('disablePSkill', 0):
            return (_sortSkillEffectsByPriority(skillEffects), skillCreations, skillAuras)
    randomNum = skillInfo.getSkillData('ranCreationNum', 0)
    if randomNum and randomNum < len(skillCreations):
        skillCreations = sample(skillCreations, randomNum)
    for trigger in gametypes.PSKILL_TRIGGER_TYPE_SKILLS:
        for pskInfo in getAllTriggerPSkillByTrigger(owner, trigger, ignoreHighLoad):
            if not pskInfo:
                continue
            if trigger == gametypes.PSKILL_TRIGGER_USE_SKILL:
                if not owner.checkPSkillTrigger(pskInfo, trigger, skillInfo.num):
                    continue
            elif trigger == gametypes.PSKILL_TRIGGER_USE_SKILL_BY_CATEGORY:
                if not owner.checkPSkillTrigger(pskInfo, trigger, skillInfo.getSkillData('skillCategory')):
                    continue
            elif trigger == gametypes.PSKILL_TRIGGER_USE_SKILL_FILTER:
                param = (owner, skillInfo.num, skillInfo.getSkillData('skillCategory'))
                if not owner.checkPSkillTrigger(pskInfo, trigger, param):
                    continue
            else:
                continue
            not isClient and owner.calcPSkillTriggerCD(pskInfo)
            addSkillEffects, addCreations, delSkillEffects, delCreations, auras = _getTriggerPSkillEffectData(owner, pskInfo, skillInfo.num)
            if delSkillEffects:
                for seid in delSkillEffects:
                    if seid in skillEffects:
                        skillEffects.remove(seid)

            if addSkillEffects:
                skillEffects.extend(addSkillEffects)
                if pskInfo.getSkillData('src') == const.PSKILL_SOURCE_LEARN and pskInfo.hasSkillData('learnLv'):
                    if not hasattr(skillInfo, 'skillEffectLvFixDict'):
                        skillInfo.skillEffectLvFixDict = {}
                    for eId in addSkillEffects:
                        skillInfo.skillEffectLvFixDict[eId] = pskInfo.lv

                if pskInfo.getSkillData('forceAsPskLv'):
                    if not hasattr(skillInfo, 'skillEffectLvFixDict'):
                        skillInfo.skillEffectLvFixDict = {}
                    for eId in addSkillEffects:
                        skillInfo.skillEffectLvFixDict[eId] = pskInfo.lv

                if owner.IsSummonedSprite and pskInfo.getSkillData('resultShowPskName'):
                    if not hasattr(srccd.rr, 'resultShowPskNameDict'):
                        setattr(srccd.rr, 'resultShowPskNameDict', {})
                    for eId in addSkillEffects:
                        srccd.rr.resultShowPskNameDict[eId] = pskInfo.num

            if delCreations:
                for cid in delCreations:
                    if cid in skillCreations:
                        skillCreations.remove(cid)

            if addCreations:
                skillCreations.extend(addCreations)
            if auras:
                skillAuras.extend(auras)

    if tgt and skillInfo.getSkillData('judgeTgtSelf', False):
        removeList = []
        isSelf = owner.id == tgt.id
        for sEffect in skillEffects:
            tgtType = SED.data.get(sEffect, {}).get('tgt', 0)
            if not tgtType:
                continue
            if isSelf and tgtType != gametypes.SKILL_EFFECT_TGT_SELF:
                removeList.append(sEffect)
            elif not isSelf and tgtType == gametypes.SKILL_EFFECT_TGT_SELF:
                removeList.append(sEffect)

        for removeEffect in removeList:
            skillEffects.remove(removeEffect)

        gamelog.debug('@hqx_skill_judgeTgtSelf', removeEffect, skillEffects, isSelf)
    return (_sortSkillEffectsByPriority(skillEffects), skillCreations, skillAuras)


def getAllTriggerPSkillByTrigger(owner, trigger, ignoreHighLoad = False):
    res = []
    key = (gametypes.PSKILL_REVERSE_TYPE_TRIGGER_PSKILL, trigger)
    if key not in PTRD.data:
        return []
    ids = set(owner.myTriggerPSkills().keys()).intersection(PTRD.data[key])
    for pid in ids:
        psk = owner.myTriggerPSkills()[pid]
        pskInfo = owner.getPSkillInfo(psk)
        if pskInfo and (not ignoreHighLoad or not pskInfo.getSkillData('ignoreOnHighLoad')):
            res.append(pskInfo)

    return res


def checkPSkillTrigger(owner, pskInfo, trigger, param, isClient):
    if trigger != pskInfo.getSkillData('trigger', 0):
        return False
    psk = owner.myTriggerPSkills().get(pskInfo.num)
    if not psk:
        return False
    if not psk.enable:
        return False
    if owner.IsAvatar and owner._isSchoolSwitch():
        return False
    if owner.IsAvatar and owner._isOnZaiju() and owner.inFubenType(const.FB_TYPE_BATTLE_FIELD_DOTA):
        if not pskInfo.getSkillData('isDotaPskill', 0):
            return False
        if not IN_CLIENT:
            triggerPskillCdDict = owner.getCellPrivateMiscProperty(gametypes.MISC_VAR_CPRI_BATTLE_FIELD_DOTA_TRIGGER_PSKILL_CD_DICT, {})
            if triggerPskillCdDict and pskInfo.num in triggerPskillCdDict and triggerPskillCdDict[pskInfo.num] > utils.getNow():
                return False
    if not __checkPSkillTriggerCD(psk, pskInfo, trigger):
        return False
    if not __checkPSkillTriggerParam(pskInfo, trigger, param):
        return False
    if not commcalc.checkPSkillPreCondition(owner, pskInfo):
        return False
    if not isClient and not owner._checkPSkillTriggerRatio(pskInfo):
        return False
    return True


def __checkPSkillTriggerCD(psk, pskInfo, trigger):
    now = utils.getNow()
    if now > psk.nextTriggerTime:
        return True
    return False


PSKILL_TRIGGER_25_MAX_RANGE = 100
PSKILL_TRIGGER_25_TARGET_ENEMY = 1
PSKILL_TRIGGER_25_TARGET_FRIEND = 2
PSKILL_TRIGGER_25_GE = 1
PSKILL_TRIGGER_25_LE = 2

def __checkPSkillTriggerParam(pskInfo, trigger, srcParam):
    triggerParam = pskInfo.getSkillData('triggerParam', 0)
    if not triggerParam:
        return True
    if trigger == gametypes.PSKILL_TRIGGER_BE_DAMAGE:
        if not triggerParam:
            return True
        if type(triggerParam) == tuple:
            categoryParam, aoeParam = triggerParam
        else:
            categoryParam = triggerParam
            aoeParam = 0
        totalDmg, srcId, srcLv, skillEffectId = srcParam
        skillCategory = SKGD.data.get((srcId, srcLv), {}).get('skillCategory', 0)
        if categoryParam and skillCategory not in categoryParam:
            return False
        if aoeParam and SED.data.get(skillEffectId, {}).get('tgt', 0):
            return False
        return True
    if trigger == gametypes.PSKILL_TRIGGER_USE_SKILL:
        if srcParam not in triggerParam:
            return False
        return True
    if trigger == gametypes.PSKILL_TRIGGER_USE_SKILL_BY_CATEGORY:
        if srcParam not in triggerParam:
            return False
        return True
    if trigger == gametypes.PSKILL_TRIGGER_REDUCE_HP_PER:
        if srcParam < triggerParam:
            return False
        return True
    if trigger == gametypes.PSKILL_TRIGGER_STATE:
        if set(triggerParam) & set(srcParam):
            return True
        return False
    if trigger == gametypes.PSKILL_TRIGGER_DO_SKILL:
        skillId, skillLv, powers = srcParam
        pw, sks = triggerParam[0], triggerParam[1]
        skillCategory = triggerParam[2] if len(triggerParam) >= 3 else []
        if sks:
            if skillId not in sks:
                return False
        if pw >= gametypes.DMGPOWER_NORMAL and pw not in powers:
            return False
        if pw < gametypes.DMGPOWER_NORMAL and abs(pw) in powers:
            return False
        if skillCategory:
            if SKGD.data.get((skillId, skillLv), {}).get('skillCategory', 0) not in skillCategory:
                return False
        return True
    if trigger in (gametypes.PSKILL_TRIGGER_BE_SKILL, gametypes.PSKILL_TRIGGER_DODGE, gametypes.PSKILL_TRIGGER_SKILL_KILL_LOCKED_TGT):
        if type(triggerParam) == int:
            return srcParam == triggerParam
        else:
            return srcParam in triggerParam
    elif trigger == gametypes.PSKILL_TRIGGER_KILL_OTHERS:
        if type(triggerParam) == int:
            return srcParam[0] == triggerParam
        elif srcParam[0] != triggerParam[0] or srcParam[1] != triggerParam[1]:
            return False
        elif srcParam[1] == gametypes.PSKILL_TRIGGER_KILL_OTHERS_SKILL_ALL:
            return True
        else:
            if srcParam[1] == gametypes.PSKILL_TRIGGER_KILL_OTHERS_SKILL_LIMIT:
                if type(triggerParam[2]) == int:
                    return srcParam[2] == triggerParam[2]
                else:
                    return srcParam[2] in triggerParam[2]
            return False
    else:
        if trigger == gametypes.PSKILL_TRIGGER_DEATH_STRIKE:
            if pskInfo.num == SCD.data.get('fbAvoidDiePskId') and not gameconfig.enableFbAvoidDieItem():
                return False
            return True
        if trigger == gametypes.PSKILL_TRIGGER_DAMAGE_BY_CATEGORY:
            sId, sLv, dmgType = srcParam
            skillCategory = SKGD.data.get((sId, sLv), {}).get('skillCategory', [])
            if not skillCategory:
                return False
            if type(triggerParam) == list:
                if skillCategory in triggerParam:
                    return True
            elif type(triggerParam) == utils.roDict or type(triggerParam) == dict:
                if skillCategory in triggerParam:
                    if len(triggerParam[skillCategory]) == 0:
                        return True
                    if dmgType in triggerParam[skillCategory]:
                        return True
            else:
                return False
        elif trigger == gametypes.PSKILL_TRIGGER_USE_SKILL_WITH_TARGET_INHERIT:
            skillCategory, _ = srcParam
            if type(triggerParam) == int:
                return skillCategory == triggerParam
            else:
                return skillCategory in triggerParam
        else:
            if trigger == gametypes.PSKILL_TRIGGER_SPECIAL_EFFECT:
                return triggerParam == srcParam
            if trigger == gametypes.PSKILL_TRIGGER_SPRITE_DIE:
                needSpriteIds, needInAwakeCd = triggerParam
                spriteId, inAwakeCd = srcParam
                return (spriteId in needSpriteIds if needSpriteIds else True) and (inAwakeCd if needInAwakeCd else True)
            if trigger in gametypes.PSKILL_TRIGGERS_NOT_CHECK_PARAM:
                return True
            if trigger == gametypes.PSKILL_TRIGGER_USE_SKILL_FILTER:
                owner, skillId, skillCategory = srcParam
                enemyType, radius, limitType, limitNum, skillTagList = triggerParam
                if not owner:
                    return False
                if type(skillTagList) == int:
                    skillTagList = (skillTagList,)
                validSkill = False
                for skillTag in skillTagList:
                    if skillTag == 0:
                        validSkill = True
                        break
                    elif skillTag <= const.SKILL_CATEGORY_SPRITE_MAX_LIMIT:
                        if skillCategory == skillTag:
                            validSkill = True
                            break
                    elif skillId == skillTag:
                        validSkill = True
                        break

                if not validSkill:
                    return False
                avatars = owner.entitiesInRange(min(radius, PSKILL_TRIGGER_25_MAX_RANGE), 'Avatar')
                puppets = owner.entitiesInRange(min(radius, PSKILL_TRIGGER_25_MAX_RANGE), 'Puppet')
                num = 0
                if enemyType == PSKILL_TRIGGER_25_TARGET_ENEMY:
                    for unit in avatars + puppets:
                        if owner.isEnemy(unit):
                            num += 1

                elif enemyType == PSKILL_TRIGGER_25_TARGET_FRIEND:
                    for unit in avatars + puppets:
                        if owner.isFriend(unit):
                            num += 1

                if limitType == PSKILL_TRIGGER_25_GE:
                    return num >= limitNum
                if limitType == PSKILL_TRIGGER_25_LE:
                    return num <= limitNum
    return False


def _getTriggerPSkillEffectData(owner, pskInfo, skillId = 0):
    triggerData = pskInfo.getSkillData('triggerData', [])
    skillEffects = []
    creations = []
    delSkillEffects = []
    delCreations = []
    for preConditions, _skillEffects, _creations, _delSkillEffects, _delCreations in triggerData:
        if not _checkPSkillTriggerPreCondition(owner, preConditions, skillId):
            continue
        if _skillEffects:
            skillEffects.extend(_skillEffects)
        if _creations:
            creations.extend(_creations)
        if _delSkillEffects:
            delSkillEffects.extend(_delSkillEffects)
        if _delCreations:
            delCreations.extend(_delCreations)

    auras = pskInfo.getSkillData('auras', [])
    return (skillEffects,
     creations,
     delSkillEffects,
     delCreations,
     auras)


def _checkPSkillTriggerPreCondition(owner, preConditions, skillId = 0):
    return commcalc.pskillPreConditionCheckCommon(owner, preConditions, skillId)


def checkUseSkillEffect(srccd, tgtcd, skillInfo, effect):
    if hasattr(skillInfo, 'skillEffectLvFixDict') and skillInfo.skillEffectLvFixDict.has_key(effect):
        skillEffectLv = skillInfo.skillEffectLvFixDict[effect]
    else:
        skillEffectLv = skillInfo.lv
    skillEffectInfo = SkillEffectInfo(effect, skillEffectLv)
    if not checkSelfSkillEffect(srccd.owner, skillEffectInfo, skillInfo):
        return None
    if not checkTgtSkillEffect(srccd, tgtcd, skillEffectInfo, skillInfo):
        return None
    return skillEffectInfo


def checkSelfSkillEffect(src, skillEffectInfo, skillInfo):
    if skillEffectInfo.hasSkillEffectData('selfStates'):
        selfStates = skillEffectInfo.getSkillEffectData('selfStates', [])
        selfStateLvEx = skillEffectInfo.getSkillEffectData('selfStateLvEx', 0)
        if not selfStateLvEx:
            selfStateLv = skillEffectInfo.getSkillEffectData('selfStateLv', 0)
            for s in selfStates:
                if not __checkSelfStates(src, s, selfStateLv):
                    return False

        else:
            for stateId in selfStates:
                if src.combatStates.getLayerCount(stateId) < selfStateLvEx:
                    return False

    if not IN_CLIENT and skillEffectInfo.hasSkillEffectData('selfFlagStates'):
        selfFlagStates = skillEffectInfo.getSkillEffectData('selfFlagStates', [])
        flagStates = src.flagStates
        for flagState in selfFlagStates:
            if not flagStates.checkInFlagState(src, flagState):
                return False

    if not IN_CLIENT and skillEffectInfo.hasSkillEffectData('selfNoFlagStates'):
        selfNoFlagStates = skillEffectInfo.getSkillEffectData('selfNoFlagStates', [])
        flagStates = src.flagStates
        for flagState in selfNoFlagStates:
            if flagStates.checkInFlagState(src, flagState):
                return False

    if skillEffectInfo.hasSkillEffectData('selfAmmoCnt'):
        ammoType, ammoNum = skillEffectInfo.getSkillEffectData('selfAmmoCnt')
        if src.ammoType != ammoType or src.ammoNum != ammoNum:
            return False
    if skillEffectInfo.hasSkillEffectData('preAmmoType'):
        ammoTypes = skillEffectInfo.getSkillEffectData('preAmmoType')
        if src.ammoType not in ammoTypes:
            return False
    selfNoStates = skillEffectInfo.getSkillEffectData('selfNoStates', [])
    selfNoStateLv = skillEffectInfo.getSkillEffectData('selfNoStateLv', 0)
    for s in selfNoStates:
        if src.hasState(s, stateLayer=selfNoStateLv):
            return False

    if skillEffectInfo.hasSkillEffectData('selfHpLessPct'):
        selfHpLessPct = skillEffectInfo.getSkillEffectData('selfHpLessPct')
        if src.hp > selfHpLessPct * src.mhp / 100.0:
            return False
    if skillEffectInfo.hasSkillEffectData('selfHpNoLessPct'):
        selfHpNoLessPct = skillEffectInfo.getSkillEffectData('selfHpNoLessPct')
        if src.hp < selfHpNoLessPct * src.mhp / 100.0:
            return False
    if skillEffectInfo.hasSkillEffectData('selfMpLessPct'):
        selfMpLessPct = skillEffectInfo.getSkillEffectData('selfMpLessPct')
        if src.mp > selfMpLessPct * src.mmp / 100.0:
            return False
    if skillEffectInfo.hasSkillEffectData('selfMpNoLessPct'):
        selfMpNoLessPct = skillEffectInfo.getSkillEffectData('selfMpNoLessPct')
        if src.mp < selfMpNoLessPct * src.mmp / 100.0:
            return False
    if skillEffectInfo.hasSkillEffectData('selfMpLess'):
        selfMpLess = skillEffectInfo.getSkillEffectData('selfMpLess')
        if src.mp > selfMpLess:
            return False
    if skillEffectInfo.hasSkillEffectData('selfMpNoLess'):
        selfMpNoLess = skillEffectInfo.getSkillEffectData('selfMpNoLess')
        if src.mp < selfMpNoLess:
            return False
    if skillEffectInfo.hasSkillEffectData('selfAttrs') or skillEffectInfo.hasSkillEffectData('selfNoAttrs'):
        curAttrs = src.getStateAttrs()
        selfAttrs = set(skillEffectInfo.getSkillEffectData('selfAttrs', []))
        if selfAttrs and not selfAttrs & curAttrs:
            return False
        selfNoAttrs = set(skillEffectInfo.getSkillEffectData('selfNoAttrs', []))
        if selfNoAttrs & curAttrs:
            return False
    if skillEffectInfo.hasSkillEffectData('selfMinVirussafe'):
        selfMinVirussafe = skillEffectInfo.getSkillEffectData('selfMinVirussafe', 0)
        if selfMinVirussafe > src.virussafe:
            return False
    if skillEffectInfo.hasSkillEffectData('selfMaxVirussafe'):
        selfMaxVirussafe = skillEffectInfo.getSkillEffectData('selfMaxVirussafe', 0)
        if selfMaxVirussafe < src.virussafe:
            return False
    return True


def __checkSelfStates(src, stateId, stateLv):
    return src.hasState(stateId, stateLv)


def checkTgtSkillEffect(srccd, tgtcd, skillEffectInfo, skillInfo):
    src = srccd.owner
    tgt = tgtcd.owner
    if skillEffectInfo.getSkillEffectData('needLockedFriend'):
        if src.id == tgt.id:
            return False
        if not srccd.rr.isFriend(tgt):
            return False
    if isWithoutStateEx(tgt):
        return True
    if skillEffectInfo.hasSkillEffectData('lockTgtStates') and src.lockedId:
        lockTgtStates = skillEffectInfo.getSkillEffectData('lockTgtStates')
        tgt = BigWorld.entities.get(src.lockedId)
        tgtStateLv = skillEffectInfo.getSkillEffectData('lockTgtStateLvl', 0)
        if tgt and tgt.IsCombatUnit and not tgt.IsNaiveCombatUnit:
            curTgtStates = {}
            if not IN_CLIENT or tgt == BigWorld.player():
                curTgtStates = {sid:(sum([ sVal[gametypes.STATE_INDEX_LAYER] for sVal in slst ]), [ sVal[gametypes.STATE_INDEX_SRCID] for sVal in slst ]) for sid, slst in tgt.statesServerAndOwn.iteritems()}
            else:
                curTgtStates = {sid:(sum([ sVal[gametypes.STATE_INDEX_LAYER] for sVal in slst ]), [ sVal[gametypes.STATE_INDEX_SRCID] for sVal in slst ]) for sid, slst in tgt.statesClientPub.iteritems()}
            checkType = lockTgtStates[0]
            lockTgtStates = lockTgtStates[1:] if checkType in (0, 1) else lockTgtStates
            if checkType == 1:
                flag = False
                for st in lockTgtStates:
                    if _checkSingleState(curTgtStates, st, tgtStateLv, 0):
                        flag = True
                        break

            else:
                flag = True
                for st in lockTgtStates:
                    if not _checkSingleState(curTgtStates, st, tgtStateLv, 0):
                        flag = False
                        break

            if not flag:
                return False
    return True


def needClientEffectCalc(owner, skillInfo):
    if not owner.IsAvatar:
        return False
    spellTime = getFinalSpellTime(owner, skillInfo)
    if spellTime:
        return False
    castType = skillInfo.getSkillData('castType')
    if castType == gametypes.SKILL_FIRE_CHARGE or castType == gametypes.SKILL_FIRE_GUIDED:
        return False
    moveDelay = skillInfo.getSkillData('movedelay', 0)
    moveSpeed = skillInfo.getSkillData('moveSpeed', 0)
    if moveDelay or moveSpeed:
        return False
    if BigWorld.component == 'client':
        forceSkillClientCalc = gameglobal.rds.configData.get('forceSkillClientCalc')
    else:
        forceSkillClientCalc = gameconfig.forceSkillClientCalc()
    if forceSkillClientCalc or hasattr(owner, 'loadLv') and owner.loadLv > const.SERVER_LOAD_LV_NORMAL:
        return True
    castDelay = getCastDelay(owner, skillInfo)
    flySpeed = skillInfo.getSkillData('flySpeed', 0)
    flyNoDelay = skillInfo.getSkillData('flyNoDelay', 0)
    if castDelay or not flyNoDelay and flySpeed:
        return False
    return True


def getFinalSpellTime(owner, skillInfo):
    spellTime = skillInfo.getSkillData('spellTime', 0)
    if owner.IsAvatar:
        spellTime = max(0, (spellTime - owner.skillAdd[4]) * (1 - owner.skillAdd[5]))
    if owner.IsSummonedSprite:
        spellTime = max(0, (spellTime - owner.skillAdd[4]) / (1 + owner.skillAdd[6]))
        if skillInfo.num in owner.combatSpeedIncreseWhiteList:
            spellTime /= 1 + owner.combatSpeedIncreseRatio[0]
    elif hasattr(owner, 'combatSpeedIncreseRatio') and skillInfo.num in owner.combatSpeedIncreseWhiteList:
        spellTime *= 1 - owner.combatSpeedIncreseRatio[1]
    return spellTime


def getCastDelay(owner, skillInfo):
    d = skillInfo.getSkillData('castDelay', 0)
    if isinstance(d, tuple):
        defalutVal = 0
        for sid, t in d:
            if sid == 0:
                defalutVal = t
                continue
            if owner.hasState(sid) or owner.ammoType == sid:
                return t

        return defalutVal
    else:
        return d


def getCombatCreationPosition(cData, pos, owner):
    try:
        radii = cData.get('bornRadii', None)
        if radii:
            position = BigWorld.findRandomNeighbourPoint(owner.spaceID, pos, radii)
            if inRange2D(radii, pos, position):
                pos = position
    except:
        pass

    return pos


SPECIAL_EFFECT_SKILL_CD_DECREASE_TYPE_ALL = 0

def cdBySpecialEffectDecrease(owner, cd, skillInfo):
    if not hasattr(owner, 'statesSpecialEffectCache'):
        return cd
    if gametypes.SKILL_STATE_SE_SKILL_CD_DECREASE not in owner.statesSpecialEffectCache:
        return cd
    sType, sVal = owner.statesSpecialEffectCache[gametypes.SKILL_STATE_SE_SKILL_CD_DECREASE]
    if sType == SPECIAL_EFFECT_SKILL_CD_DECREASE_TYPE_ALL or sType == skillInfo.getSkillData('skillCategory', 0) or sType == skillInfo.num:
        cd /= 1 + sVal
    return cd


def cdByCombatSpeedIncreseRatio(owner, cd, skillInfo):
    if owner.IsSummonedSprite:
        skillCategory = skillInfo.getSkillData('skillCategory')
        if skillCategory == const.SKILL_CATEGORY_SPRITE_AWAKE:
            cd = max(0, (cd - owner.spriteCDReduce[2]) * (1 - owner.spriteCDReduce[3]))
        elif skillCategory in const.SKILL_CATEGORY_SPRITE_ACT_SKILLS:
            cd = max(0, (cd - owner.spriteCDReduce[0]) * (1 - owner.spriteCDReduce[1]))
        elif skillInfo.num in owner.combatSpeedIncreseWhiteList:
            if owner.combatSpeedIncreseRatio[0]:
                cd /= 1 + owner.combatSpeedIncreseRatio[0]
    elif hasattr(owner, 'combatSpeedIncreseRatio') and skillInfo.num in owner.combatSpeedIncreseWhiteList:
        if owner.combatSpeedIncreseRatio[1]:
            cd *= 1 - owner.combatSpeedIncreseRatio[1]
    return cd


def gcdByCombatSpeedIncreseRatio(owner, gcd, skillInfo):
    if owner.IsSummonedSprite:
        if skillInfo.num in owner.combatSpeedIncreseWhiteList:
            if owner.combatSpeedIncreseRatio[0]:
                gcd /= 1 + owner.combatSpeedIncreseRatio[0]
    else:
        if owner.IsAvatar:
            gcd = max(0.1, (gcd - owner.skillAdd[0]) * (1 - owner.skillAdd[1]))
        if hasattr(owner, 'combatSpeedIncreseRatio') and skillInfo.num in owner.combatSpeedIncreseWhiteList:
            if owner.combatSpeedIncreseRatio[1]:
                gcd *= 1 - owner.combatSpeedIncreseRatio[1]
    return gcd


def checkSelfCombatCreation(ent, ccInfo):
    selfStates = ccInfo.getCombatCreationData('selfStates')
    if selfStates != None and type(selfStates) == list:
        checkType = selfStates[0]
        selfStates = selfStates[1:] if checkType in (0, 1) else selfStates
        if checkType == 1:
            flag = False
            for stateId in selfStates:
                if ent.hasState(stateId):
                    flag = True
                    break

        else:
            flag = True
            for stateId in selfStates:
                if not ent.hasState(stateId):
                    flag = False
                    break

        if not flag:
            return False
    selfNoStates = ccInfo.getCombatCreationData('selfNoStates', [])
    if selfNoStates:
        for s in selfNoStates:
            if ent.hasState(s):
                return False

    if ccInfo.hasCombatCreationData('selfAmmoCnt'):
        ammoType, ammoNum = ccInfo.getCombatCreationData('selfAmmoCnt')
        if ent.ammoType != ammoType or ent.ammoNum != ammoNum:
            return False
    if ccInfo.hasCombatCreationData('preAmmoType'):
        ammoType = ccInfo.getCombatCreationData('preAmmoType')
        if ent.ammoType != ammoType:
            return False
    return True


def getTgtsInMaxClique(ents, dist):
    adjList = _getTgtAdjList(ents, dist)
    eIdsInMaxClique = _getMaxClique([ e.id for e in ents if adjList.has_key(e.id) ], adjList)
    return list(eIdsInMaxClique)


def _getTgtAdjList(ents, dist):
    tgtAdjList = {}
    sLen = len(ents)
    for i in xrange(sLen):
        se = ents[i]
        for j in xrange(i + 1, sLen):
            te = ents[j]
            d = (se.position - te.position).length
            if d <= dist:
                tgtAdjList.setdefault(se.id, {})[te.id] = d
                tgtAdjList.setdefault(te.id, {})[se.id] = d

    return tgtAdjList


def _minBoundBoxAreaP2(eIds):
    pIds = list(eIds)
    if len(pIds) <= 1:
        return 0
    ent = BigWorld.entities.get(pIds[0])
    if not ent:
        return 0
    minP = list(ent.position)
    maxP = list(ent.position)
    for i in xrange(1, len(pIds)):
        pId = pIds[i]
        ent = BigWorld.entities.get(pId)
        if not ent:
            continue
        pos = list(ent.position)
        for j in xrange(len(minP)):
            srcP = pos[j]
            minP[j] = min(minP[j], srcP)
            maxP[j] = max(maxP[j], srcP)

    p2Dist = 0
    for i in xrange(len(minP)):
        p2Dist += pow(minP[i] - maxP[i], 2)

    return p2Dist


def _findMaxClique(curEId, eIds, size, adjList, pruningDict, gArgs):
    gArgs.setdefault('tmpResult', set()).add(curEId)
    try:
        if not eIds:
            curMax = gArgs.get('max', 0)
            if size >= curMax:
                curAreaP2 = _minBoundBoxAreaP2(gArgs.get('result', set()))
                if size > gArgs.get('max', 0) or size == gArgs.get('max', 0) and curAreaP2 < gArgs.get('areaP2', 0):
                    gArgs['max'] = size
                    gArgs['found'] = True
                    gArgs['result'] = set(gArgs.get('tmpResult', set()))
                    gArgs['areaP2'] = curAreaP2
                    return
        else:
            while eIds:
                if size + len(eIds) < gArgs.get('max', 0):
                    return
                nextId = eIds.pop()
                if size + pruningDict.get(nextId, 0) < gArgs.get('max', 0):
                    return
                _findMaxClique(nextId, [ eId for eId in eIds if eId in set(eIds) & set(adjList.get(nextId, {}).keys()) ], size + 1, adjList, pruningDict, gArgs)
                if gArgs.get('found', False):
                    return

    finally:
        gArgs.get('tmpResult', set()).discard(curEId)


def _getMaxClique(eIds, adjList):
    gArgs = {'max': 0,
     'found': False}
    pruningDict = {}
    sortedEIds = list(sorted(eIds, cmp=lambda x, y: cmp(len(adjList.get(x, {})), len(adjList.get(y, {}))), reverse=True))
    for pos, curEId in enumerate(sortedEIds):
        gArgs['found'] = False
        _findMaxClique(curEId, [ eId for eId in sortedEIds if eId in set(sortedEIds[:pos]) & set(adjList.get(curEId, {}).keys()) ], 1, adjList, pruningDict, gArgs)
        pruningDict[curEId] = gArgs.get('max', 0)

    return gArgs.get('result', set())


def samplePosInCircleSub2DFrom3D(center0_3d, center1_3d, radius0, radius1):
    pos_2d = samplePosInCircleSub2D(Math.Vector2(center0_3d.x, center0_3d.z), Math.Vector2(center1_3d.x, center1_3d.z), radius0, radius1)
    if pos_2d:
        return Math.Vector3(pos_2d.x, center0_3d.y, pos_2d.y)


def samplePosInCircleSub2D(center0, center1, radius0, radius1):
    """
    \xcb\xe6\xbb\xfa\xd1\xa1\xc8\xa1\xd4\xda\xd4\xb20\xc4\xda\xb5\xab\xb2\xbb\xd4\xda\xd4\xb21\xc4\xda\xb5\xc4\xd7\xf8\xb1\xea
    :param center0: Vector2 \xd4\xb20\xb5\xc4\xd4\xb2\xd0\xc4
    :param center1: Vector2 \xd4\xb21\xb5\xc4\xd4\xb2\xd0\xc4
    :param radius0: \xd4\xb20\xb5\xc4\xb0\xeb\xbe\xb6
    :param radius1: \xd4\xb21\xb5\xc4\xb0\xeb\xbe\xb6
    :return: Vector2 or None
    """
    if type(center0) != Math.Vector2 or type(center1) != Math.Vector2:
        raise TypeError('intersection2DCircle center0 and center1 must be vectors')
    if center1.distTo(center0) <= 1e-09:
        return _polarToRectCoord2D(center0, randomf() * 2 * math.pi, randomf() * (radius0 - radius1) + radius1)
    isIntersect, intersectPos = intersection2DCircle(center0, center1, radius0, radius1)
    distCenter = center0.distTo(center1)
    try:
        if isIntersect:
            if len(intersectPos) == 2:
                sampleAngle = randomf() * 2 * math.pi
                sampleDist = randomf() * radius0
                ret = _polarToRectCoord2D(center0, sampleAngle, sampleDist)
                if ret.distTo(center1) >= radius1 - 0.0001:
                    return ret
                if sampleDist < 0.0001:
                    sampleDist = 0.0003
                    ret = _polarToRectCoord2D(center0, sampleAngle, sampleDist)
                lineIntersects = lineIntersectCircle(center1, radius1, center0, ret)
                if len(lineIntersects) < 2:
                    return ret
                lineInterP1, lineInterP2 = lineIntersects
                dist1, dist2 = (lineInterP1 - center0).length, (lineInterP2 - center0).length
                if dist1 > dist2:
                    dist1, dist2 = dist2, dist1
                    lineInterP1, lineInterP2 = lineInterP2, lineInterP1
                if distCenter >= radius1:
                    dist = randomf() * dist1
                    return _polarToRectCoord2D(center0, sampleAngle, dist)
                elif min(lineInterP2.x, center0.x) <= ret.x <= max(lineInterP2.x, center0.x) and min(lineInterP2.y, center0.y) <= ret.y <= max(lineInterP2.y, center0.y):
                    return _polarToRectCoord2D(center0, sampleAngle + math.pi, randomf() * (radius0 - dist1) + dist1)
                else:
                    return _polarToRectCoord2D(center0, sampleAngle, randomf() * (radius0 - dist1) + dist1)
            elif len(intersectPos) == 1:
                return _polarToRectCoord2D(center0, randomf() * 2 * math.pi, randomf() * radius0)
        else:
            if distCenter > radius0 + radius1:
                return _polarToRectCoord2D(center0, randomf() * 2 * math.pi, randomf() * radius0)
            if distCenter < radius0 + radius1 and radius0 > radius1:
                sampleAngle = randomf() * 2 * math.pi
                sampleDist = randomf() * radius0
                ret = _polarToRectCoord2D(center0, sampleAngle, sampleDist)
                if ret.distTo(center1) >= radius1 - 0.0001:
                    return ret
                if sampleDist < 0.0001:
                    sampleDist = 0.0003
                    ret = _polarToRectCoord2D(center0, sampleAngle, sampleDist)
                lineIntersects = lineIntersectCircle(center1, radius1, center0, ret)
                if len(lineIntersects) < 2:
                    return ret
                lineInterP1, lineInterP2 = lineIntersects
                dist1, dist2 = (lineInterP1 - center0).length, (lineInterP2 - center0).length
                if dist1 > dist2:
                    dist1, dist2 = dist2, dist1
                    lineInterP1, lineInterP2 = lineInterP2, lineInterP1
                if distCenter >= radius1:
                    dist = choice([randomf() * dist1, randomf() * (radius0 - dist2) + dist2])
                    return _polarToRectCoord2D(center0, sampleAngle, dist)
                elif min(lineInterP1.x, ret.x) <= center0.x <= max(lineInterP1.x, ret.x) and min(lineInterP1.y, ret.y) <= center0.y <= max(lineInterP1.y, ret.y):
                    return _polarToRectCoord2D(center0, sampleAngle, randomf() * (radius0 - dist2) + dist2)
                else:
                    return _polarToRectCoord2D(center0, sampleAngle, randomf() * (radius0 - dist1) + dist1)
    except Exception as e:
        return _polarToRectCoord2D(center0, randomf() * 2 * math.pi, randomf() * radius0)


def intersection2DCircle(center0, center1, radius0, radius1):
    """
    \xc7\xf3\xc1\xbd\xb8\xf6\xd4\xb2\xb5\xc4\xbd\xbb\xb5\xe3
    :param center0: Vecoter2 \xd4\xb20\xb5\xc4\xd4\xb2\xd0\xc4 
    :param center1: Vecoter2 \xd4\xb21\xb5\xc4\xd4\xb2\xd0\xc4 
    :param radius0: \xd4\xb20\xb5\xc4\xb0\xeb\xbe\xb6
    :param radius1: \xd4\xb21\xb5\xc4\xb0\xeb\xbe\xb6
    :return: bool\xa3\xa8\xca\xc7\xb7\xf1\xcf\xe0\xbd\xbb\xa3\xa9, list\xa3\xa8\xbd\xbb\xb5\xe30-2\xb8\xf6\xa3\xa9
    """
    d = center1.distTo(center0)
    if d > radius0 + radius1:
        return (False, [])
    if d == 0 or d < abs(radius0 - radius1):
        return (False, [])
    a = (radius0 ** 2 - radius1 ** 2 + d ** 2) / (2 * d)
    h = math.sqrt(radius0 ** 2 - a ** 2)
    tmpPoint = center0 + a * (center1 - center0) / d
    if d == radius0 + radius1:
        return (True, [tmpPoint])
    alpha_x = tmpPoint.x + h * (center1.y - center0.y) / d
    alpha_y = tmpPoint.y - h * (center1.x - center0.x) / d
    alpha = Math.Vector2(alpha_x, alpha_y)
    beta_x = tmpPoint.x - h * (center1.y - center0.y) / d
    beta_y = tmpPoint.y + h * (center1.x - center0.x) / d
    beta = Math.Vector2(beta_x, beta_y)
    return (True, [alpha, beta])


def _polarToRectCoord2D(posRect, theta, r):
    """
    \xbd\xab\xbc\xab\xd7\xf8\xb1\xea\xb5\xc4\xc6\xab\xd2\xc6\xbd\xc7\xba\xcd\xc6\xab\xd2\xc6\xbe\xe0\xc0\xeb\xa3\xac\xd3\xa6\xd3\xc3\xb5\xbd\xd6\xb1\xbd\xc7\xd7\xf8\xb1\xea
    :param posRect: Vector2 \xd6\xb1\xbd\xc7\xd7\xf8\xb1\xea\xcf\xb5\xd4\xad\xca\xbc\xd7\xf8\xb1\xea
    :param theta: \xc6\xab\xd2\xc6\xbd\xc7\xb6\xc8
    :param r: \xc6\xab\xd2\xc6\xbe\xe0\xc0\xeb
    :return: Vector \xc6\xab\xd2\xc6\xba\xf3\xb5\xc4\xd6\xb1\xbd\xc7\xd7\xf8\xb1\xea\xcf\xb5\xd7\xf8\xb1\xea
    """
    return Math.Vector2(posRect.x + math.cos(theta) * r, posRect.y + math.sin(theta) * r)


def pointProjectionOnLine(point, pointOnLine1, pointOnLine2):
    """
    \xc7\xf3\xb5\xe3\xd4\xda\xd6\xb1\xcf\xdf\xb5\xc4\xcd\xb6\xd3\xb0
    :param point: \xd6\xb8\xb6\xa8\xb5\xe3
    :param pointOnLine1: \xd6\xb1\xcf\xdf\xc9\xcf\xd2\xbb\xb5\xe3
    :param pointOnLine2: \xd6\xb1\xcf\xdf\xc9\xcf\xd2\xbb\xb5\xe3
    :return: Vector2 \xcd\xb6\xd3\xb0\xb5\xe3
    """
    tmp = pointOnLine2 - pointOnLine1
    return pointOnLine1 + tmp * tmp.dot(point - pointOnLine1) / tmp.lengthSquared


def lineIntersectCircle(center, radius, pointOnLine1, pointOnLine2):
    """
    \xd6\xb1\xcf\xdf\xba\xcd\xd4\xb2\xb5\xc4\xbd\xbb\xb5\xe3
    :param center: \xd4\xb2\xd0\xc4
    :param radius: \xb0\xeb\xbe\xb6
    :param pointOnLine1: \xd6\xb1\xcf\xdf\xc9\xcf\xd2\xbb\xb5\xe3
    :param pointOnLine2: \xd6\xb1\xcf\xdf\xc9\xcf\xd2\xbb\xb5\xe3
    :return: \xbd\xbb\xb5\xe3\xc1\xd0\xb1\xed
    """
    projectionPoint = pointProjectionOnLine(center, pointOnLine1, pointOnLine2)
    normlizedLineVec = (pointOnLine2 - pointOnLine1) / (pointOnLine2 - pointOnLine1).length
    squaredRatio = radius * radius - (projectionPoint - center).lengthSquared
    if squaredRatio < 0:
        return []
    offsetRatio = math.sqrt(squaredRatio)
    if offsetRatio == 0.0:
        return [projectionPoint]
    offsetVec = offsetRatio * normlizedLineVec
    return [projectionPoint + offsetVec, projectionPoint - offsetVec]


def genDmgDpsStats(player, sprite):
    dmgDpsStats = FubenStats()
    for ent, (srcTp, tarTp) in zip([player, sprite], [(FubenStats.K_SKILL_DAMAGE, FubenStats.K_SKILL_DPS), (FubenStats.K_SPRITE_SKILL_DAMAGE, FubenStats.K_SPRITE_SKILL_DPS)]):
        if ent and ent.dmgStats:
            endTime = ent.dmgEndTime if ent.dmgEndTime else int(BigWorld.player().getServerTime() if BigWorld.component == 'client' else utils.getNow())
            interval = max(endTime - ent.dmgStartTime, 0)
            dmgStats = ent.dmgStats.statsDict.get(srcTp, None)
            if dmgStats:
                if interval:
                    dmgDpsStats.statsDict[tarTp] = {k:int(v / interval) for k, v in dmgStats.iteritems()}
                else:
                    dmgDpsStats.statsDict[tarTp] = {k:0 for k, v in dmgStats.iteritems()}

    return dmgDpsStats
