#Embedded file name: /WORKSPACE/data/entities/common/commcalc.o
import random
from sMath import limit
import BigWorld
import gametypes
import utils
import const
import formula
import math
import copy
import gamelog
import gameconfigCommon
import commcython
if BigWorld.component in ('base', 'cell'):
    import cythonutils
from gameclass import StateInfo, SkillInfo, SkillEffectInfo, CombatCreationInfo
from data import prop_data as PD
from cdata import prop_ref_reverse_data as PRRD
from data import prop_ref_data as PRD
from data import state_group_inverted_index_data as SGIID
from cdata import prop_def_data as PDD
from cdata import equip_star_factor_data as ESFD
from cdata import equip_order_factor_data as EOFD
from data import avatar_data as AD
from cdata import primary_property_transform_data as PPTD
from cdata import radar_chart_value_data as RCVD
from data import radar_chart_dimension_data as RCDD
from data import school_switch_general_data as SSGD
from data import guild_growth_data as GGD
from cdata import equip_enhance_prop_data as EEPD
from cdata import state_group_data as SGPD
from cdata import equip_quality_factor_data as EQFD
from data import horsewing_upgrade_data as HWUD
from cdata import equip_enhance_juexing_prop_data as EEJPD
from cdata import pskill_template_data as PSTD
from data import life_skill_equip_data as LSEPD
from data import title_data as TD
from cdata import yaopei_lv_data as YLD
from cdata import pursue_server_config_data as PSCD
from cdata import pursue_pvp_enhance_data as PPED
from cdata import pursue_yaopei_data as PYD
from data import sys_config_data as SCD
from data import map_config_data as MCD
from data import skill_general_data as SKGD
if BigWorld.component in ('base', 'cell'):
    import gameengine
    import gameconst
    import gameconfig
    from data import formula_server_data as FMD
elif BigWorld.component in ('client',):
    if not getattr(BigWorld, 'isBot', False):
        from data import formula_client_data as FMD
    import gameglobal

def setBit(x, index, on = True):
    bi = int(index / 8)
    si = index % 8
    qfl = len(x)
    if on and qfl < bi + 1:
        x.extend(' ' * (bi - qfl + 1))
    tmp = 1 << si
    if on:
        x[bi] |= tmp
    elif getBit(x, index):
        x[bi] ^= tmp
    return x


def getBit(x, index):
    bi = int(index / 8)
    si = index % 8
    if len(x) < bi + 1:
        return False
    else:
        return x[bi] & 1 << si != 0


def getBitCount(x):
    totalCount = 0
    for idx in xrange(len(x) * 8):
        totalCount += 1 if getBit(x, idx) else 0

    return totalCount


def getQuestFlag(player, index):
    return getBit(player.questFlag, index)


def calcBitDword(x, index, value):
    on = value > 0
    if not 31 >= index >= 0:
        return x
    if index == 31:
        tmp = -2147483648
    else:
        tmp = 1 << index
    if on:
        return x | tmp
    elif getBitDword(x, index):
        return x ^ tmp
    else:
        return x


def getBitDword(x, index):
    return x & 1 << index != 0


def getBitDwords(x, indexes):
    return any([ getBitDword(x, index) for index in indexes ])


def setBitQword(x, index, value):
    on = value > 0
    if not 63 >= index >= 0:
        return x
    if index == 63:
        tmp = int(-9223372036854775808L)
    else:
        tmp = 1 << index
    if on:
        return x | tmp
    elif getBitQword(x, index):
        return x ^ tmp
    else:
        return x


def getBitQword(x, index):
    return x & 1 << index != 0


def getBitQwords(x, indexes):
    return any([ getBitQword(x, index) for index in indexes ])


def getSingleBit(x, index):
    return x & 1 << index


def setSingleBit(x, index, on):
    if on:
        return int(x | 1 << index)
    else:
        return int(x & ~(1 << index))


def getEntFlag(ent, f):
    if not hasattr(ent, 'publicFlags') or not hasattr(ent, 'flags'):
        return False
    elif f in gametypes.ALL_CLIENT_FLAG_SET:
        return getBitDword(ent.publicFlags, f)
    else:
        return getBitDword(ent.flags, f)


def hasFlagChanged(new, old, index):
    return getBitDword(new, index) != getBitDword(old, index)


def weightingChoiceN(choices, weights, cnt):
    if len(choices) == 0 or len(choices) != len(weights) or len(choices) < cnt:
        return []
    results = []
    for j in xrange(cnt):
        curRatio = random.random() * sum(weights)
        for i in xrange(len(choices)):
            if weights[i] <= 0:
                continue
            curRatio -= weights[i]
            if curRatio <= 0:
                questId = choices.pop(i)
                weights.pop(i)
                results.append(questId)
                break

    return results


def weightingChoiceIndex(w):
    s = sum(w)
    d = random.randint(1, s)
    for i, v in enumerate(w):
        if d <= v:
            return i
        d -= v

    return len(w) - 1


def weightingChoice(data, weightings):
    s = sum(weightings)
    w = [ float(x) / s for x in weightings ]
    t = 0
    for i, v in enumerate(w):
        t += v
        w[i] = t

    c = __inWhichPart(random.random(), w)
    try:
        return data[c]
    except IndexError:
        return data[-1]


def __inWhichPart(n, w):
    for i, v in enumerate(w):
        if n < v:
            return i

    return len(w) - 1


def calcPSkillRandomValue(pskillId, value):
    if type(value) != tuple:
        if type(value) not in [int, float]:
            raise Exception('error!!!!, wrong pskill data, pskill id:%d', pskillId)
        return value
    if len(value) != 2:
        raise Exception('error!!!!, pskill id:%d', pskillId)
        return
    if value[0] == value[1]:
        return value[0]
    res = random.uniform(value[0], value[1])
    return res


def pskillPreConditionCheckCommon(owner, preConditions, skillId = 0, isSrc = True):
    if not preConditions:
        return True
    preCondition, preConditionVal, preNoCondition, preNoConditonVal = preConditions
    if preCondition != gametypes.PSKILL_PRE_CONDITION_NONE and preConditionVal:
        if preCondition == gametypes.PSKILL_PRE_CONDITION_STATE:
            flag = False
            for t in preConditionVal:
                if owner.hasState(t):
                    flag = True
                    break

            if not flag:
                return False
        elif preCondition == gametypes.PSKILL_PRE_CONDITION_ATTR:
            if not isSrc and BigWorld.component in ('base', 'cell') and gameconfig.warnOnPSkillPreconditionAttrUsed():
                gameengine.reportCritical('exception, pskill precondition has attr is not supported! %s %d' % (str(preConditions), skillId))
            flag = False
            for t in preConditionVal:
                if owner.hasStateAttr(t):
                    flag = True
                    break

            if not flag:
                return False
        elif preCondition == gametypes.PSKILL_PRE_CONDITION_HP_LESS:
            if not owner.mhp or float(owner.hp) / owner.mhp > preConditionVal / 100.0:
                return False
        elif preCondition == gametypes.PSKILL_PRE_CONDITION_SKILL:
            if skillId not in preConditionVal:
                return False
        elif preCondition == gametypes.PSKILL_PRE_CONDITION_AMMO_ID:
            if owner.IsAvatar and owner.ammoType not in preConditionVal:
                return False
        elif preCondition == gametypes.PSKILL_PRE_CONDITION_STATE_GROUP:
            curTgtStateIds = set(owner.statesServerAndOwn.keys())
            if not any((curTgtStateIds & set(SGPD.data.get(group).get('states', ())) for group in preConditionVal)):
                return False
        elif preCondition == gametypes.PSKILL_PRE_CONDITION_HP_HIGHER:
            if not owner.mhp or float(owner.hp) / owner.mhp < preConditionVal / 100.0:
                return False
        elif preCondition == gametypes.PSKILL_PRE_CONDITION_MAP:
            if formula.getMapId(owner.spaceNo) not in preConditionVal:
                return False
        elif preCondition == gametypes.PSKILL_PRE_CONDITION_SPRITE_OUT:
            if not owner.IsAvatar or not owner.summonedSpriteBox:
                return False
        elif preCondition == gametypes.PSKILL_PRE_CONDITION_MP_LESS:
            if not owner.mmp or float(owner.mp) / owner.mmp > preConditionVal / 100.0:
                return False
        elif preCondition == gametypes.PSKILL_PRE_CONDITION_MP_HIGHER:
            if not owner.mmp or float(owner.mp) / owner.mmp < preConditionVal / 100.0:
                return False
        elif preCondition == gametypes.PSKILL_PRE_CONDITION_MAPTYPE:
            mapType = formula.getItemForbidMapType(owner.spaceNo)
            if mapType not in preConditionVal:
                return False
        elif preCondition == gametypes.PSKILL_PRE_CONDITION_PSKILL:
            flag = False
            for t in preConditionVal:
                if owner.hasPSkills(t) or owner.hasTriggerSkills(t):
                    flag = True
                    break

            if not flag:
                return False
    if preNoCondition != gametypes.PSKILL_PRE_CONDITION_NONE and preNoConditonVal:
        if preNoCondition == gametypes.PSKILL_PRE_CONDITION_STATE:
            for t in preNoConditonVal:
                if owner.hasState(t):
                    return False

        elif preNoCondition == gametypes.PSKILL_PRE_CONDITION_ATTR:
            if BigWorld.component in ('base', 'cell') and gameconfig.warnOnPSkillPreconditionAttrUsed():
                gameengine.reportCritical('exception, pskill precondition tgt has attr is not supported! %s %d' % (str(preConditions), skillId))
            for t in preNoConditonVal:
                if owner.hasStateAttr(t):
                    return False

        elif preNoCondition == gametypes.PSKILL_PRE_CONDITION_AMMO_ID:
            if owner.IsAvatar and owner.ammoType in preNoConditonVal:
                return False
        elif preCondition == gametypes.PSKILL_PRE_CONDITION_STATE_GROUP:
            curTgtStateIds = set(owner.statesServerAndOwn.keys())
            if any((curTgtStateIds & set(SGPD.data.get(group).get('states', ())) for group in preConditionVal)):
                return False
        elif preNoCondition == gametypes.PSKILL_PRE_CONDITION_MAPTYPE:
            mapType = formula.getItemForbidMapType(owner.spaceNo)
            if mapType in preNoConditonVal:
                return False
        elif preNoCondition == gametypes.PSKILL_PRE_CONDITION_MAP:
            if formula.getMapId(owner.spaceNo) in preNoConditonVal:
                return False
        if preNoCondition == gametypes.PSKILL_PRE_CONDITION_PSKILL:
            for t in preNoConditonVal:
                if owner.hasPSkills(t) or owner.hasTriggerSkills(t):
                    return False

    return True


def getPSkillPreCondition(owner, pskInfo):
    preCondition = pskInfo.getSkillData('preCondition', gametypes.PSKILL_PRE_CONDITION_NONE)
    preNoCondition = pskInfo.getSkillData('preNoCondition', gametypes.PSKILL_PRE_CONDITION_NONE)
    if not preCondition and not preNoCondition:
        return None
    preConditonVal = pskInfo.getSkillData('preConditonVal', 0)
    preNoConditonVal = pskInfo.getSkillData('preNoConditonVal', 0)
    preConditions = (preCondition,
     preConditonVal,
     preNoCondition,
     preNoConditonVal)
    return preConditions


def checkPSkillPreCondition(owner, pskInfo):
    preCondition = pskInfo.getSkillData('preCondition', gametypes.PSKILL_PRE_CONDITION_NONE)
    preConditonVal = pskInfo.getSkillData('preConditonVal', 0)
    preNoCondition = pskInfo.getSkillData('preNoCondition', gametypes.PSKILL_PRE_CONDITION_NONE)
    preNoConditonVal = pskInfo.getSkillData('preNoConditonVal', 0)
    preConditions = (preCondition,
     preConditonVal,
     preNoCondition,
     preNoConditonVal)
    return pskillPreConditionCheckCommon(owner, preConditions)


def calcHijackData(dataInfo, effects, skillLvDelta = 0):
    allEffects = {}
    paramNameSet = set()
    hijackData = {}
    if skillLvDelta > 0:
        hijackData['skillLvDelta'] = skillLvDelta
        if dataInfo.DATA_TYPE == const.SKILL_INFO:
            newLv = min(dataInfo.lv + skillLvDelta, const.MAX_SKILL_LEVEL)
            dataInfo = SkillInfo(dataInfo.num, newLv)
    getDataFunc = fetchGetDataFunc(dataInfo)
    if not getDataFunc:
        return {}
    for paramName, calcType, paramVal in effects:
        key = (paramName, calcType)
        if not allEffects.has_key(key):
            allEffects[key] = 0
        paramNameSet.add(paramName)
        if calcType == gametypes.PSKILL_AFFECT_SKILL_CALC_TYPE_SET:
            allEffects[key] = paramVal
        else:
            allEffects[key] += paramVal

    for paramName in paramNameSet:
        setKey = (paramName, gametypes.PSKILL_AFFECT_SKILL_CALC_TYPE_SET)
        if allEffects.has_key(setKey):
            paramVal = allEffects[setKey]
            val = paramVal[dataInfo.lv - 1] if paramName in dataInfo.LV_DEPENDENT_ATTR_LIST and type(paramVal) in const.TYPE_TUPLE_AND_LIST and len(paramVal) == const.MAX_SKILL_LEVEL else paramVal
            hijackData[paramName] = val
            continue
        tmpVal = getDataFunc(paramName)
        addKey = (paramName, gametypes.PSKILL_AFFECT_SKILL_CALC_TYPE_ADD)
        if allEffects.has_key(addKey):
            tmpVal += allEffects[addKey]
        multiKey = (paramName, gametypes.PSKILL_AFFECT_SKILL_CALC_TYPE_MULTIPLY)
        if allEffects.has_key(multiKey):
            tmpVal *= 1.0 + allEffects[multiKey]
        hijackData[paramName] = tmpVal

    return hijackData


def fetchGetDataFunc(dataInfo):
    getDataFunc = None
    if dataInfo.DATA_TYPE == const.SKILL_INFO:
        getDataFunc = getattr(dataInfo, 'getSkillData')
    elif dataInfo.DATA_TYPE == const.SKILL_EFFECT_INFO:
        getDataFunc = getattr(dataInfo, 'getSkillEffectData')
    elif dataInfo.DATA_TYPE == const.STATE_INFO:
        getDataFunc = getattr(dataInfo, 'getStateData')
    elif dataInfo.DATA_TYPE == const.COMBAT_CREATION_INFO:
        getDataFunc = getattr(dataInfo, 'getCombatCreationData')
    return getDataFunc


def _doCalcDataInfoAffectedByPSkill(owner, dataInfo, dataType, affectDataRes, affectDataByTgtRes):
    if not affectDataRes:
        return dataInfo
    effectsList = []
    for key, val in affectDataRes.iteritems():
        if key == 'skillLvDelta':
            continue
        preCondition, effects = val
        if not pskillPreConditionCheckCommon(owner, preCondition):
            continue
        effectsList.extend(effects)

    hijackData = calcHijackData(dataInfo, effectsList, affectDataRes.get('skillLvDelta', 0))
    if affectDataRes.get('skillLvDelta', 0):
        hijackData['skillCalcLvAdd'] = affectDataRes.get('skillLvDelta', 0)
    dataInfo.updateHijackData(hijackData)
    return dataInfo


def checkPSkillTriggerDuration(psk, pskInfo):
    needTrigger = pskInfo.getSkillData('needTrigger', 0)
    if not needTrigger:
        return True
    now = utils.getNow()
    if now > psk.triggerInvalidTime:
        return False
    return True


def _mergePSkillAffectSkillData(owner, dataType, dataId, pskInfo, res):
    if pskInfo.hasSkillData('skillLvDelta'):
        res['skillLvDelta'] = res.setdefault('skillLvDelta', 0) + pskInfo.getSkillData('skillLvDelta')
    affectSkillData = pskInfo.getSkillData('affectSkillData', [])
    if not affectSkillData:
        return
    effect = []
    for dataTp, tdataId, paramName, calcType, paramVal in affectSkillData:
        if dataType != dataTp:
            continue
        if not paramName:
            continue
        if type(tdataId) in const.TYPE_TUPLE_AND_LIST:
            if dataId not in tdataId:
                continue
        elif tdataId != dataId:
            continue
        effect.append((paramName, calcType, paramVal))

    if not effect:
        return
    preConditions = getPSkillPreCondition(owner, pskInfo)
    if res.has_key(pskInfo.num):
        res[pskInfo.num][1].extend(effect)
    else:
        res[pskInfo.num] = (preConditions, effect)


def mergeAllPSkillAffectSkillData(owner, dataType, dataId, skillId):
    affectDataRes = {}
    affectDataByTgtRes = {}
    pskillInfoList = owner.getAllAffectPSkillInfo(dataType, dataId)
    for psk, pskInfo in pskillInfoList:
        if not pskInfo:
            continue
        skillCategories = pskInfo.getSkillData('skillCategory')
        if skillCategories:
            skillCategory = SKGD.data.get((skillId, 1), {}).get('skillCategory')
            if type(skillCategories) in const.TYPE_TUPLE_AND_LIST:
                if skillCategory not in skillCategories:
                    continue
            elif skillCategories != skillCategory:
                continue
        else:
            skillIds = pskInfo.getSkillData('skillId', 0)
            if type(skillIds) in const.TYPE_TUPLE_AND_LIST:
                if skillId not in skillIds:
                    continue
            elif skillIds != skillId:
                continue
        _mergePSkillAffectSkillData(owner, dataType, dataId, pskInfo, affectDataRes)
        _mergePSkillAffectSkillByTgtData(owner, dataType, dataId, pskInfo, affectDataByTgtRes)

    return (affectDataRes, affectDataByTgtRes)


def _mergePSkillAffectSkillByTgtData(owner, dataType, dataId, pskInfo, res):
    affectSkillTgtData = pskInfo.getSkillData('affectSkillTgtData', [])
    if not affectSkillTgtData:
        return
    tgtPreCondition = pskInfo.getSkillData('tgtPreCondition', gametypes.PSKILL_PRE_CONDITION_NONE)
    tgtPreNoCondition = pskInfo.getSkillData('tgtPreNoCondition', gametypes.PSKILL_PRE_CONDITION_NONE)
    if not tgtPreCondition and not tgtPreNoCondition:
        tgtConditions = None
    else:
        tgtPreConditonVal = pskInfo.getSkillData('tgtPreConditonVal', 0)
        tgtPreNoConditonVal = pskInfo.getSkillData('tgtPreNoConditonVal', 0)
        tgtConditions = (tgtPreCondition,
         tgtPreConditonVal,
         tgtPreNoCondition,
         tgtPreNoConditonVal)
    effect = []
    for dataTp, tdataId, paramName, calcType, paramVal in affectSkillTgtData:
        if dataType != dataTp:
            continue
        if not paramName:
            continue
        if type(tdataId) in const.TYPE_TUPLE_AND_LIST:
            if dataId not in tdataId:
                continue
        elif tdataId != dataId:
            continue
        effect.append((paramName, calcType, paramVal))

    if res.has_key(pskInfo.num):
        res[pskInfo.num][1].extend(effect)
    else:
        res[pskInfo.num] = (tgtConditions, effect)


def calcDataInfoAffectedByPSkill(owner, dataInfo, dataType, skillId):
    if owner.IsAvatar and owner._isSchoolSwitch():
        return dataInfo
    affectDataRes, affectDataByTgtRes = mergeAllPSkillAffectSkillData(owner, dataType, dataInfo.num, skillId)
    _doCalcDataInfoAffectedByPSkill(owner, dataInfo, dataType, affectDataRes, affectDataByTgtRes)
    return dataInfo


def calcPSkillRandomData(pskillId, pskillData):
    pskillTemplateData = PSTD.data.get(pskillId, {})
    randomType = pskillTemplateData.get('randomType', gametypes.PSKILL_DATA_RANDOM_TYPE_NONE)
    if randomType != gametypes.PSKILL_DATA_RANDOM_TYPE_ONCE:
        return {}
    pData = {}
    for key in const.PSKILL_DATA_NEED_RANDOM:
        if not pskillData.has_key(key):
            continue
        rawValue = pskillData[key]
        val = calcPSkillRandomValue(pskillId, rawValue)
        pData[key] = val

    affectSkillData = pskillData.get('affectSkillData', [])
    if affectSkillData:
        tmpList = []
        for dataType, dataId, paramName, calcType, paramVal in affectSkillData:
            tmpVal = calcPSkillRandomValue(pskillId, paramVal)
            tmpList.append((dataType,
             dataId,
             paramName,
             calcType,
             tmpVal))

        pData['affectSkillData'] = tuple(tmpList)
    return pData


NEED_HIJACK_PROP_MAX_FOR_MONSTER = frozenset([PDD.data.PROPERTY_MHP, PDD.data.PROPERTY_HP])

def getAttrHijackMax(owner, propId):
    if not owner.IsMonster or propId not in NEED_HIJACK_PROP_MAX_FOR_MONSTER:
        return None
    return const.MAX_INT64


@commcython.cythonfuncentry
def calcAttrHelper(owner, states, propId, value):
    """
    @cython.locals(propId=cython.int, addAttrSumId=cython.int, addAttrMaxId=cython.int, redAttrSumId=cython.int,
        redAttrMaxId=cython.int, tt=cython.float,
        tmpAddSumDataNum=cython.float, tmpAddMaxDataNum=cython.float, tmpRedSumDataNum=cython.float, tmpRedMaxDataNum=cython.float,
        tmpAddSumDataPer=cython.float, tmpAddMaxDataPer=cython.float, tmpRedSumDataPer=cython.float, tmpRedMaxDataPer=cython.float)
    """
    pData = PD.data.get(propId, None)
    if pData == None:
        raise Exception('@zs:calcAttrHelper,propId error!!!!')
    attrIdList = PRRD.data.get(propId, [])
    if not attrIdList:
        return checkFinalPropValue(pData, value, hijackMax=getAttrHijackMax(owner, propId), owner=owner)
    addAttrSumId, addAttrMaxId, redAttrSumId, redAttrMaxId = attrIdList
    temSetAddDataNum = None
    temSetAddDataNum1 = states.get((addAttrSumId, gametypes.DATA_TYPE_SET), None)
    temSetAddDataNum2 = states.get((addAttrMaxId, gametypes.DATA_TYPE_SET), None)
    if temSetAddDataNum1 != None:
        temSetAddDataNum = temSetAddDataNum1
    if temSetAddDataNum2 != None and temSetAddDataNum2 > temSetAddDataNum:
        temSetAddDataNum = temSetAddDataNum2
    temSetRedDataNum = None
    temSetRedDataNum1 = states.get((redAttrSumId, gametypes.DATA_TYPE_SET), None)
    temSetRedDataNum2 = states.get((redAttrMaxId, gametypes.DATA_TYPE_SET), None)
    if temSetRedDataNum1 != None:
        temSetRedDataNum = temSetRedDataNum1
    if temSetRedDataNum2 != None and temSetRedDataNum2 > temSetRedDataNum:
        temSetRedDataNum = temSetRedDataNum2
    if temSetAddDataNum != None or temSetRedDataNum != None:
        res = temSetAddDataNum if temSetAddDataNum != None else -1 * temSetRedDataNum
    else:
        res = value
        tmpAddSumDataNum = states.get((addAttrSumId, gametypes.DATA_TYPE_NUM), 0.0)
        tmpAddMaxDataNum = states.get((addAttrMaxId, gametypes.DATA_TYPE_NUM), 0.0)
        tmpRedSumDataNum = states.get((redAttrSumId, gametypes.DATA_TYPE_NUM), 0.0)
        tmpRedMaxDataNum = states.get((redAttrMaxId, gametypes.DATA_TYPE_NUM), 0.0)
        res = res + tmpAddSumDataNum + tmpAddMaxDataNum - tmpRedSumDataNum - tmpRedMaxDataNum
        tmpAddSumDataPer = states.get((addAttrSumId, gametypes.DATA_TYPE_PER), 0.0)
        tmpAddMaxDataPer = states.get((addAttrMaxId, gametypes.DATA_TYPE_PER), 0.0)
        tmpRedSumDataPer = states.get((redAttrSumId, gametypes.DATA_TYPE_PER), 0.0)
        tmpRedMaxDataPer = states.get((redAttrMaxId, gametypes.DATA_TYPE_PER), 0.0)
        tt = tmpAddSumDataPer + tmpAddMaxDataPer - tmpRedSumDataPer - tmpRedMaxDataPer
        res = res * (1.0 + tt)
    res = checkFinalPropValue(pData, res, hijackMax=getAttrHijackMax(owner, propId), owner=owner)
    return res


def checkFinalPropValue(pData, value, hijackMax = None, owner = None):
    minValue = pData['min']
    maxValue = pData['max'] if hijackMax is None else hijackMax
    if owner and owner.IsAvatar:
        minFormulaId = pData.get('minFormulaId', 0)
        maxFormulaId = pData.get('maxFormulaId', 0)
        minValue = formula.calcFormulaById(minFormulaId, {'lv': owner.realLv}) if minFormulaId else minValue
        maxValue = formula.calcFormulaById(maxFormulaId, {'lv': owner.realLv}) if maxFormulaId else maxValue
    if pData['numtype'] == 'I':
        value = int(round(round(value, 5)))
        minValue = int(minValue)
        maxValue = int(maxValue)
    elif pData['numtype'] == 'F':
        value = float(value)
        minValue = float(minValue)
        maxValue = float(maxValue)
    res = limit(value, minValue, maxValue)
    return res


@commcython.cythonfuncentry
def attrMerge(owner, res, attrId, attrValueType, attrFstValue, times = 1):
    """
    @cython.locals(attrId=cython.int, attrValueType=cython.int, times=cython.int, propId=cython.int, propType=cython.int)
    """
    attrData = PRD.data.get(attrId)
    if not attrData:
        if BigWorld.component in ('base', 'cell'):
            gameengine.reportCritical('attr not found in PRD. %d' % (attrId,))
        return res
    if owner and owner.IsAvatar:
        propId = attrData.get('property')
        if owner.bfDotaZaijuEnergyType:
            propType = const.BATTLE_FIELD_DOTA_ZAIJU_ENERGY_PROP_TYPE_MAP.get(propId, 0)
            if propType and propType != owner.bfDotaZaijuEnergyType:
                return res
        elif propId in const.BATTLE_FIELD_DOTA_ZAIJU_PROP_ID_SET:
            return res
    return realAttrMerge(res, attrId, attrValueType, attrFstValue, times)


@commcython.cythonfuncentry
def realAttrMerge(res, attrId, attrValueType, attrFstValue, times = 1):
    """
    @cython.locals(attrId=cython.int, attrValueType=cython.int, times=cython.int, attrStyle=cython.int)
    """
    import gamelog
    attrData = PRD.data.get(attrId)
    attrStyle = attrData.get('style')
    if attrValueType == gametypes.DATA_TYPE_COND:
        attrFstValue = 1
    elif attrValueType == gametypes.DATA_TYPE_SPECIAL_EFFECT:
        attrFstValue = 1
    if attrStyle == gametypes.STATE_STYLE_TICK:
        return res
    if res.has_key((attrId, attrValueType)):
        data = res[attrId, attrValueType]
        if attrValueType == gametypes.DATA_TYPE_SET:
            data = max(data, attrFstValue)
        else:
            attrAddRule = attrData.get('addRule')
            if attrAddRule == gametypes.STATE_ADD_RULE_MAX:
                data = max(data, attrFstValue * times)
            elif attrAddRule == gametypes.STATE_ADD_RULE_SUM:
                data = data + attrFstValue * times
            else:
                data = data
    elif attrValueType == gametypes.DATA_TYPE_SET:
        data = attrFstValue
    else:
        attrAddRule = attrData.get('addRule')
        if attrAddRule == gametypes.STATE_ADD_RULE_MAX:
            data = attrFstValue * times
        elif attrAddRule == gametypes.STATE_ADD_RULE_SUM:
            data = attrFstValue * times
        else:
            data = attrFstValue
    res[attrId, attrValueType] = data
    return res


def validEquipOnCalcProp(owner, equip):
    if getattr(equip, 'cdura', 0) == 0:
        return False
    if equip.isExpireTTL():
        return False
    if equip.isShihun():
        return False
    if equip.lvReq > owner.realLvByCause(gametypes.REAL_LV_EQUIPMENT):
        return False
    return True


def enableShareEquipProp(owner):
    if owner._isSchoolSwitch():
        return False
    elif BigWorld.component in ('base', 'cell'):
        return gameconfig.enableShareEquipProp()
    else:
        return gameglobal.rds.configData.get('enableShareEquipProp', False)


def enableEquipChangeJuexingStrength():
    if BigWorld.component in ('base', 'cell'):
        return gameconfig.enableEquipChangeJuexingStrength()
    else:
        return gameglobal.rds.configData.get('enableEquipChangeJuexingStrength', False)


def applyEnhJuexingAddData(enhJuexingNoAddData, enhJuexingAddRatio, maxEnhlv):
    if not enableEquipChangeJuexingStrength():
        return enhJuexingNoAddData
    if maxEnhlv < SCD.data.get('enhJuexingStrengthEnhLvLimit', const.EQUIP_ENH_JUEXING_STRENGTH_LV_LIMIT):
        return enhJuexingNoAddData
    enhJuexingAddData = {}
    for enhLv, enhVal in enhJuexingNoAddData.iteritems():
        if not enhVal:
            continue
        addRatio = enhJuexingAddRatio.get(enhLv, 0)
        enhJuexingAddData.setdefault(enhLv, [])
        for propRefId, propType, oldVal in enhVal:
            newVal = oldVal * (1 + addRatio)
            enhJuexingAddData[enhLv].append((propRefId, propType, newVal))

    return enhJuexingAddData


def calcSingleItem(owner, res, equip, part = -1):
    if not validEquipOnCalcProp(owner, equip):
        return
    inServerSide = BigWorld.component in ('base', 'cell')
    isYaoPei = equip.isYaoPei()
    if isYaoPei and inServerSide and not gameconfig.enableYaoPei():
        return
    starFactor = ESFD.data.get(equip.addedStarLv, {}).get('factor', 1.0)
    qualityFactor = EQFD.data.get(equip.quality, {}).get('factor', 1.0)
    ypLv = 0
    if isYaoPei:
        ypLv = equip.getYaoPeiLv()
        if inServerSide and gameconfig.enableRebalance() and owner.rebalancing:
            methodID, factor = owner.getMethodFactorByModeID(gametypes.REBALANCE_SUBSYS_ID_HSF, owner.rebalanceMode)
            if methodID:
                ypLv = min(ypLv, factor)
        ypd = YLD.data.get(ypLv, {})
    if isYaoPei:
        bParam = ypd.get('basicAdd', 1)
        for prop, type, value in getattr(equip, 'yaoPeiProps', []):
            attrMerge(owner, res, prop, type, value * bParam)

    elif hasattr(equip, 'props') and equip.props:
        for prop, type, value in equip.props:
            attrMerge(owner, res, prop, type, value * starFactor * qualityFactor)

    if hasattr(equip, 'fixedProps') and equip.fixedProps:
        for prop, type, value in equip.fixedProps:
            attrMerge(owner, res, prop, type, value * starFactor * qualityFactor)

    if isYaoPei:
        eParam = ypd.get('extraAdd', 1)
        for prop, type, val, _, _, lv in getattr(equip, 'yaoPeiExtraProps', []):
            if ypLv >= lv:
                attrMerge(owner, res, prop, type, val * eParam)

    elif hasattr(equip, 'extraProps') and equip.extraProps:
        for prop, type, value in equip.extraProps:
            attrMerge(owner, res, prop, type, value * starFactor * qualityFactor)

    if hasattr(equip, 'rprops') and equip.rprops:
        if isYaoPei:
            rpParam = ypd.get('extraAdd', 1)
        elif not gameconfigCommon.enableNewLv89():
            rpParam = starFactor * qualityFactor
        else:
            param = equip.isSesMaker(owner.gbId)
            rpParam = (starFactor + param) * qualityFactor
        for prop, type, value in equip.rprops:
            attrMerge(owner, res, prop, type, value * rpParam)

    orderFactor = EOFD.data.get(equip.addedOrder, {}).get('factor', 1.0)
    enhCalcData = getEquipShareEnhProp(owner, equip, getAlternativeEquip(owner, part))
    if enableShareEquipProp(owner) and enhCalcData:
        enhLv = enhCalcData['enhLv']
        maxEnhlv = enhCalcData['maxEnhlv']
        enhanceRefining = enhCalcData['enhanceRefining']
        equipType = enhCalcData['equipType']
        equipSType = enhCalcData['equipSType']
        enhanceType = enhCalcData['enhanceType']
    else:
        enhLv = getattr(equip, 'enhLv', 0)
        maxEnhlv = equip.getMaxEnhLv(owner)
        enhanceRefining = getattr(equip, 'enhanceRefining', {})
        equipType = equip.equipType
        equipSType = equip.equipSType
        enhanceType = equip.enhanceType
    if inServerSide and owner.rebalancing and gameconfig.enableRebalance():
        methodID, factor = owner.getMethodFactorByModeID(gametypes.REBALANCE_SUBSYS_ID_QH, owner.rebalanceMode)
        if methodID:
            maxEnhlv = min(maxEnhlv, factor)
    refiningFactor = 0
    tEnhLv = min(maxEnhlv, enhLv)
    if enhanceRefining:
        for elv, enh in enhanceRefining.items():
            if elv <= tEnhLv:
                refiningFactor += enh

    enhanceData = EEPD.data.get((equipType, equipSType, enhanceType))
    if enhanceData:
        for prop, type, value in enhanceData.get('enhProps', []):
            attrMerge(owner, res, prop, type, value * orderFactor * refiningFactor)

    if enableShareEquipProp(owner) and enhCalcData:
        enhJuexingNoAddData = enhCalcData['enhJuexingData']
        enhJuexingAddRatio = enhCalcData['enhJuexingAddRatio']
    else:
        enhJuexingNoAddData = getattr(equip, 'enhJuexingData', {})
        enhJuexingAddRatio = getattr(equip, 'enhJuexingAddRatio', {})
    enhJuexingData = applyEnhJuexingAddData(enhJuexingNoAddData, enhJuexingAddRatio, maxEnhlv)
    if enhJuexingData:
        refiningStar = equip.getEquipRefiningStar()
        if inServerSide and owner.rebalancing and gameconfig.enableRebalance():
            methodID, factor = owner.getMethodFactorByModeID(gametypes.REBALANCE_SUBSYS_ID_QHJX, owner.rebalanceMode)
            if methodID:
                tEnhLv = min(tEnhLv, factor)
        for eLv, jxData in enhJuexingData.items():
            if eLv > tEnhLv:
                continue
            juexingDataList = utils.getEquipEnhJuexingPropData(equipType, equipSType, eLv, enhanceType)
            for prop, type, value in jxData:
                if prop not in juexingDataList:
                    continue
                attrMerge(owner, res, prop, type, value * refiningStar)

    if hasattr(equip, 'preprops') and equip.preprops:
        for prop, type, value in equip.preprops:
            attrMerge(owner, res, prop, type, value * starFactor * qualityFactor)

    for prop, type, value in equip.getGemProps(owner):
        if not gameconfigCommon.enableNewLv89():
            attrMerge(owner, res, prop, type, value)
        else:
            wenYinEnh = equip.isSesWenYinEnh()
            attrMerge(owner, res, prop, type, value * (1 + wenYinEnh))

    if equip.isWingOrRide():
        ridewing_quality = equip.quality
        ridewing_type = equip.getVehicleType()
        ridewing_stage = getattr(equip, 'rideWingStage', None)
        if utils.isRideWingShareEpRegenEnabled():
            if part == gametypes.EQU_PART_RIDE and owner.sharedRideAttr.itemId > 0 and owner.hasSharedRideMaxSpeed():
                ridewing_quality = owner.sharedRideAttr.quality
                ridewing_type = owner.sharedRideAttr.equipType
                ridewing_stage = owner.sharedRideAttr.rideWingStage
            elif part == gametypes.EQU_PART_WINGFLY and owner.sharedWingAttr.itemId > 0 and owner.hasSharedWingMaxSpeed():
                ridewing_quality = owner.sharedWingAttr.quality
                ridewing_type = owner.sharedWingAttr.equipType
                ridewing_stage = owner.sharedWingAttr.rideWingStage
        if ridewing_stage is not None:
            hwud = HWUD.data.get((ridewing_quality, ridewing_type, ridewing_stage))
            if hwud:
                for prop, type, value in hwud.get('props', []):
                    attrMerge(owner, res, prop, type, value)


def calcSingleLifeEquip(owner, res, equip):
    d = LSEPD.data.get(equip.id)
    if not d:
        return
    for prop, type, value in d.get('gProps', []):
        attrMerge(owner, res, prop, type, value)


def calcSinglePSkill(owner, res, pskInfo):
    import gameconfigCommon
    if not gameconfigCommon.enablePskillExtraAttr():
        attrId = pskInfo.getSkillData('attrId', 0)
        if attrId != 0:
            attrValType = pskInfo.getSkillData('attrValType', 0)
            attrVal = pskInfo.getSkillData('attrVal', 0)
            attrMerge(owner, res, attrId, attrValType, attrVal)
        groupId = pskInfo.getSkillData('attrGroupId', 0)
        if groupId != 0:
            attrs = SGIID.data.get(groupId, None)
            if attrs:
                groupValType = pskInfo.getSkillData('attrGroupValType', 0)
                groupVal = pskInfo.getSkillData('attrGroupVal', 0)
                for attrId in attrs:
                    attrMerge(owner, res, attrId, groupValType, groupVal)

    else:
        effects = pskInfo.getAllAffectedEffect()
        if effects:
            for attrId, attrValType, attrVal in effects:
                attrMerge(owner, res, attrId, attrValType, attrVal)

    return res


def calcSingleGuildGrowth(owner, res, volumnId, attrId, level):
    if BigWorld.component in ('base', 'cell'):
        if gameconfig.enableRebalance() and owner.rebalancing:
            methodID, factor = owner.getMethodFactorByModeID(gametypes.REBALANCE_SUBSYS_ID_RWXL, owner.rebalanceMode)
            if methodID == const.REBALANCE_METHOD_2_SETVALUE:
                level = factor.get(volumnId, 0)
            elif methodID == const.REBALANCE_METHOD_1_UPLIMIT:
                level = min(level, factor.get(volumnId, 0))
            if level <= 0:
                return res
    data = GGD.data.get((volumnId, attrId, level))
    if not data:
        if BigWorld.component in ('base', 'cell'):
            gameengine.reportCritical('guild growth never exists now ownerId=%d, volumnId=%s attrId=%s level=%s' % (owner and owner.id or 0,
             volumnId,
             attrId,
             level))
        return res
    attrValType = data.get('valueType', 0)
    attrVal = data.get('value', 0)
    if attrVal:
        attrMerge(owner, res, attrId, attrValType, attrVal)
    if BigWorld.component in ('base', 'cell'):
        if gameconfig.enableGuildGrowthExtraPropsAdd():
            extraAttrs = data.get('extraProps', ())
            gamelog.debug('@zmm extraProps£º', extraAttrs)
            for attrId, attrVal in extraAttrs:
                if attrId and attrVal:
                    attrMerge(owner, res, attrId, attrValType, attrVal)

    return res


def calcAllPropVal(owner, primaryPropDict, euqips, pskills, titles, propsFilter = [], guildGrowth = None):
    filteredSkills = []
    for psk in pskills:
        skillData = owner.getPSkillInfo(psk).skillData
        if skillData.has_key('src'):
            if skillData['src'] != const.PSKILL_SOURCE_AIR_COMBAT:
                filteredSkills.append(psk)
        else:
            filteredSkills.append(psk)

    states = _mergeAllPropAdd(owner, euqips, filteredSkills, titles, guildGrowth)
    data = AD.data.get(owner.realSchool, None)
    if not data:
        return {}
    res = {}
    primaryProperties = PDD.data.PRIMARY_PROPERTIES
    for propId in primaryProperties:
        if primaryPropDict.has_key(propId):
            res[propId] = primaryPropDict[propId]
        else:
            res[propId] = _calcSinglePropVal(owner, propId, states, data)

    _mergeAllPrimaryProp(owner, res, states)
    if not propsFilter:
        props = PD.data.keys()
    else:
        props = propsFilter
    for propId in props:
        if propId in primaryProperties or propId == 0:
            continue
        res[propId] = _calcSinglePropVal(owner, propId, states, data)

    return res


def _mergeAllPrimaryProp(owner, propCache, states):
    primaryProperties = PDD.data.PRIMARY_PROPERTIES
    for propId in primaryProperties:
        trsId = owner.realSchool
        ptData = PPTD.data.get((trsId, propId), None)
        if ptData == None:
            continue
        attrData = ptData.get('attrData', None)
        if attrData == None:
            continue
        baseValue = propCache.get(propId, 0)
        for attrId, transRatio, transParam in attrData:
            attrFstValue = baseValue // transParam * transRatio
            attrValueType = gametypes.DATA_TYPE_NUM
            states = attrMerge(owner, states, attrId, attrValueType, attrFstValue)

    return states


def _calcSinglePropVal(owner, propId, states, data):
    pData = PD.data.get(propId, None)
    if pData == None:
        raise Exception('@zs, propId wrong:%d' % propId)
        return
    baseValue = _calcPropBaseValue(owner, propId, data)
    finalVal = calcAttrHelper(owner, states, propId, baseValue)
    return finalVal


def _mergeAllPropAdd(owner, euqips, pskills, titles, guildGrowth = None):
    res = {}
    if guildGrowth:
        for volumnId, volumn in guildGrowth.iteritems():
            for attrId, growth in volumn.iteritems():
                calcSingleGuildGrowth(owner, res, volumnId, attrId, growth.level)

    for equip in euqips:
        calcSingleItem(owner, res, equip)

    pstdd = PSTD.data
    for psk in pskills:
        if BigWorld.component in 'client':
            srcVal = pstdd.get(psk.id, {}).get('src', 0)
            if srcVal == const.PSKILL_SOURCE_AIR_COMBAT:
                continue
        pskInfo = owner.getPSkillInfo(psk)
        calcSinglePSkill(owner, res, pskInfo)

    for title in titles:
        _mergeSingleTitleProp(owner, title, res)

    return res


def _mergeSingleTitleProp(self, titileId, res):
    if not TD.data.has_key(titileId):
        return res
    tData = TD.data[titileId]
    if not tData.has_key('props'):
        return res
    for propId, valueType, value in tData['props']:
        res = attrMerge(self, res, propId, valueType, value)

    return res


def _calcFormulaById(fId, vars):
    if not FMD.data.has_key(fId):
        return
    fData = FMD.data[fId]
    func = fData['formula']
    res = func(vars)
    return res


def _calcPropBaseValue(owner, propId, avatarData):
    if propId in PDD.data.PRIMARY_PROPERTIES:
        return _getPrimaryPropBaseValue(owner, propId)
    propName = PD.data.get(propId, {}).get('name', '')
    pd = avatarData.get(propName, None)
    if pd:
        fId = pd[0]
        if fId == 0:
            return pd[1]
        else:
            vars = {'lv': owner.lv}
            params = pd[1:]
            for i in range(len(params)):
                param = params[i]
                vars['p%d' % (i + 1,)] = param

            value = _calcFormulaById(fId, vars)
            return value
    else:
        if propName in PDD.data.PROPERTY_NAME_FLOAT:
            return 0.0
        return 0


@commcython.cythonfuncentry
def _getPrimaryPropBaseValue(owner, propId):
    """
    @cython.locals(propId=cython.int)
    """
    if propId not in PDD.data.PRIMARY_PROPERTIES:
        return 0
    if propId == PDD.data.PROPERTY_ATTR_PW:
        v = owner.primaryProp.bpow
    elif propId == PDD.data.PROPERTY_ATTR_INT:
        v = owner.primaryProp.bint
    elif propId == PDD.data.PROPERTY_ATTR_PHY:
        v = owner.primaryProp.bphy
    elif propId == PDD.data.PROPERTY_ATTR_SPR:
        v = owner.primaryProp.bspr
    elif propId == PDD.data.PROPERTY_ATTR_AGI:
        v = owner.primaryProp.bagi
    return v


def _createFormulaArgs(owner, id, type, args, isClient):
    ret = {}
    if type == TYPE_PROPS:
        for i, arg in enumerate(args):
            ret['p%d' % (i + 1)] = arg

    elif type in (TYPE_SKILL, TYPE_PSKILL):
        for i, arg in enumerate(args):
            ret['p%d' % (i + 1)] = arg

        if type == TYPE_SKILL:
            if isClient:
                skVal = owner.getSkills().get(id, None)
            else:
                skVal = owner.mySkills().get(id, None)
            ret['skLv'] = skVal.level if skVal else 0
        else:
            ret['skLv'] = 0
            for key, value in owner.pskills.get(id, {}).items():
                ret['skLv'] += value.level if value else 0

    return ret


TYPE_PROPS = 1
TYPE_SKILL = 2
TYPE_PSKILL = 3
DIM_SKILL = 3

def createRadarChartData(owner, preview = None, isClient = False, calcAtkScoreOnly = False):
    ret = []
    skills = owner.getSkills().keys() if isClient else owner.mySkills().keys()
    pskills = owner.pskills.keys()
    for idx in xrange(1, 6):
        data = RCDD.data.get(idx, {})
        formulaStr = data.get('formula%d' % (owner.realSchool - 2), '0')
        params = data.get('formual1Params%d' % (owner.realSchool - 2), [])
        for i, param in enumerate(params):
            propId = PRD.data.get(param, {}).get('property', 0)
            if preview:
                val = preview.get(propId, 0)
            else:
                val = getAvatarPropValueById(owner, propId) if propId else 0
            formulaStr = formulaStr.replace('p' + str(i + 1).zfill(2), str(val * 1.0))

        formulaStr = formulaStr.replace('lv', str(owner.lv))
        try:
            res = eval(formulaStr)
        except:
            res = 0

        tempRes = 0
        if idx == DIM_SKILL:
            for skillId in skills + pskills:
                skData = RCVD.data.get(skillId, {})
                if not skData:
                    continue
                fid = skData['value'][0] if skData['value'] else 0
                args = skData['value'][1:] if skData['value'] else []
                if fid:
                    if skillId in skills:
                        valType = TYPE_SKILL
                    else:
                        valType = TYPE_PSKILL
                    args = _createFormulaArgs(owner, skillId, valType, args, isClient)
                    fVal = _calcFormulaById(fid, args)
                    if fVal == None:
                        fVal = 0
                    tempRes += fVal
                else:
                    tempRes += sum(args)

        res += tempRes
        transfer = data.get('transfer', '0').replace('p1', str(res))
        try:
            res = eval(transfer)
        except:
            res = 0

        ret.append(res)
        if calcAtkScoreOnly:
            break

    maxVal = max(ret)
    for idx in xrange(1, 7):
        limit = data.get('hopRaito%d' % idx, maxVal)
        if limit == 0:
            limit = maxVal
        if maxVal <= limit:
            break

    ret.append(limit)
    ret.append(idx)
    return ret


def createSelfAllPropVal(owner, isClient = False):
    equips = [ equip for equip in owner.equipment if equip ]
    pskills = []
    for pskVal in owner.pskills.values():
        for subVal in pskVal.values():
            pskInfo = owner.getPSkillInfo(subVal)
            if checkPSkillPreCondition(owner, pskInfo):
                pskills.append(subVal)

    titles = []
    props = calcSelfPropVal(owner, equips, pskills, titles, owner.guildGrowth)
    propsFilter = []
    for idx in xrange(1, 6):
        data = RCDD.data.get(idx, {})
        propsFilter += data.get('formual1Params%d' % (owner.realSchool - 2), [])

    propsFilter = [ PRD.data.get(id, {}).get('property', 0) for id in propsFilter ]
    return calcAllPropVal(owner, props, equips, pskills, titles, propsFilter, owner.guildGrowth)


def createSelfRadarChartData(owner, isClient = False, calcAtkScoreOnly = False):
    allPropVal = createSelfAllPropVal(owner, isClient)
    return createRadarChartData(owner, allPropVal, isClient, calcAtkScoreOnly)


def calcSelfPropVal(owner, equips, pskills, titles, guildGrowth = None):
    states = _mergeAllPropAdd(owner, equips, pskills, titles, guildGrowth)
    data = AD.data.get(owner.realSchool, None)
    if not data:
        return {}
    res = {}
    for propId in PDD.data.PRIMARY_PROPERTIES:
        res[propId] = _calcSinglePropVal(owner, propId, states, data)

    return res


def getPrimaryPropBaseValueInSchoolSwitch(owner, propId):
    if propId not in PDD.data.PRIMARY_PROPERTIES:
        return 0
    v = 0
    if propId == PDD.data.PROPERTY_ATTR_PW:
        v = _getSchoolSwitchPrimaryPropVal(owner, 'strFormula')
    elif propId == PDD.data.PROPERTY_ATTR_INT:
        v = _getSchoolSwitchPrimaryPropVal(owner, 'intFormula')
    elif propId == PDD.data.PROPERTY_ATTR_PHY:
        v = _getSchoolSwitchPrimaryPropVal(owner, 'phyFormula')
    elif propId == PDD.data.PROPERTY_ATTR_SPR:
        v = _getSchoolSwitchPrimaryPropVal(owner, 'sprFormula')
    elif propId == PDD.data.PROPERTY_ATTR_AGI:
        v = _getSchoolSwitchPrimaryPropVal(owner, 'agiFormula')
    return v


def _getSchoolSwitchPrimaryPropVal(owner, propName):
    switchNo = owner._getSchoolSwitchNo()
    data = SSGD.data.get(switchNo)
    val = data.get(propName)
    if not val:
        return 0
    fId = val[0]
    vars = {'lv': owner.realLv}
    params = val[1:]
    for i in range(len(params)):
        param = params[i]
        vars['p%d' % (i + 1,)] = param

    value = _calcFormulaById(fId, vars)
    return value


def getPrimaryPropValue(owner, propId):
    if propId not in PDD.data.PRIMARY_PROPERTIES:
        return 0
    if owner.IsAvatar or owner.IsAvatarRobot or owner.IsPuppet:
        if propId == PDD.data.PROPERTY_ATTR_PW:
            v = owner.primaryProp.pow
        elif propId == PDD.data.PROPERTY_ATTR_INT:
            v = owner.primaryProp.int
        elif propId == PDD.data.PROPERTY_ATTR_PHY:
            v = owner.primaryProp.phy
        elif propId == PDD.data.PROPERTY_ATTR_SPR:
            v = owner.primaryProp.spr
        elif propId == PDD.data.PROPERTY_ATTR_AGI:
            v = owner.primaryProp.agi
    elif propId == PDD.data.PROPERTY_ATTR_PW:
        v = owner.primaryProp[0]
    elif propId == PDD.data.PROPERTY_ATTR_INT:
        v = owner.primaryProp[1]
    elif propId == PDD.data.PROPERTY_ATTR_PHY:
        v = owner.primaryProp[2]
    elif propId == PDD.data.PROPERTY_ATTR_SPR:
        v = owner.primaryProp[3]
    elif propId == PDD.data.PROPERTY_ATTR_AGI:
        v = owner.primaryProp[4]
    return v


def getAvatarPropValueById(owner, propId):
    if propId in PDD.data.PRIMARY_PROPERTIES:
        return getPrimaryPropValue(owner, propId)
    if propId not in PROP_MAP:
        return
    name, index = PROP_MAP[propId]
    if not hasattr(owner, name):
        return
    p = getattr(owner, name)
    if index != None:
        if len(p) <= index:
            return
        p = p[index]
    return p


def getAvatarPropValueByIdEx(owner, propId):
    if not PD.data.has_key(propId):
        if propId == 20001:
            return owner.atk[0]
        elif propId == 20002:
            return max(owner.atk[0], owner.atk[1])
        elif propId == 20003:
            return owner.atk[2]
        elif propId == 20004:
            return max(owner.atk[2], owner.atk[3])
        elif propId == 20005:
            return owner.defence[0]
        elif propId == 20006:
            return owner.defence[1]
        elif propId == 20007:
            return max(0, int((0.4 * owner.equipAtk[2] + owner.healAdd) * (1 + owner.atkDefRatio[9])))
        elif propId == 20008:
            return max(0, int((0.4 * max(owner.equipAtk[2], owner.equipAtk[3]) + owner.healAdd) * (1 + owner.atkDefRatio[9])))
        else:
            return 0
    else:
        return getAvatarPropValueById(owner, propId)


def getSummonedSpritePropValueById(spriteProp, propId):
    spriteBaseVirtualPropId = SCD.data.get('spriteBaseVirtualPropId', ())
    if propId not in PD.data and propId in spriteBaseVirtualPropId:
        return spriteProp.get(propId, 0)
    name = PD.data.get(propId, {}).get('name', '')
    p = spriteProp.get(name, 0)
    return p


def getMonsterPropValueById(owner, propId):
    if propId in PDD.data.PRIMARY_PROPERTIES:
        return getPrimaryPropValue(owner, propId)
    if propId not in PROP_MAP:
        return
    name, index = PROP_MAP[propId]
    if not hasattr(owner, name):
        return
    p = getattr(owner, name)
    if index != None:
        p = p[index]
    return p


PROP_RECALC_MAP = {PDD.data.PROPERTY_MHP: ('mhp', None),
 PDD.data.PROPERTY_MMP: ('mmp', None),
 PDD.data.PROPERTY_BATTLE_FIELD_DOTA_NUQI_PROP_MAX_VAL: ('mmp', None),
 PDD.data.PROPERTY_BATTLE_FIELD_DOTA_JINGQI_PROP_MAX_VAL: ('mmp', None),
 PDD.data.PROPERTY_BATTLE_FIELD_DOTA_NENGLIANG_PROP_MAX_VAL: ('mmp', None),
 PDD.data.PROPERTY_MBP: ('mbp', None),
 PDD.data.PROPERTY_BP_REDUCE: ('bpReduce', None),
 PDD.data.PROPERTY_SWIM_SPEED_FACTOR: ('swimSpeedFactor', None),
 PDD.data.PROPERTY_HP_REGEN: ('regenSpeed', 0),
 PDD.data.PROPERTY_NON_CMBT_HP_REGEN: ('regenSpeed', 1),
 PDD.data.PROPERTY_MP_REGEN: ('regenSpeed', 2),
 PDD.data.PROPERTY_NON_CMBT_MP_REGEN: ('regenSpeed', 3),
 PDD.data.PROPERTY_BATTLE_FIELD_DOTA_NUQI_REGEN: ('regenSpeed', 2),
 PDD.data.PROPERTY_BATTLE_FIELD_DOTA_NONCMBT_NUQI_REGEN: ('regenSpeed', 3),
 PDD.data.PROPERTY_BATTLE_FIELD_DOTA_JINGQI_REGEN: ('regenSpeed', 2),
 PDD.data.PROPERTY_BATTLE_FIELD_DOTA_NONCMBT_JINGQI_REGEN: ('regenSpeed', 3),
 PDD.data.PROPERTY_BATTLE_FIELD_DOTA_NENGLIANG_REGEN: ('regenSpeed', 2),
 PDD.data.PROPERTY_BATTLE_FIELD_DOTA_NONCMBT_NENGLIANG_REGEN: ('regenSpeed', 3),
 PDD.data.PROPERTY_HP_REGEN_RATIO: ('regenRatioSpeed', 0),
 PDD.data.PROPERTY_NON_CMBT_HP_REGEN_RATIO: ('regenRatioSpeed', 1),
 PDD.data.PROPERTY_MP_REGEN_RATIO: ('regenRatioSpeed', 2),
 PDD.data.PROPERTY_NON_CMBT_MP_REGEN_RATIO: ('regenRatioSpeed', 3),
 PDD.data.PROPERTY_BATTLE_FIELD_DOTA_NUQI_REGEN_RATIO: ('regenRatioSpeed', 2),
 PDD.data.PROPERTY_BATTLE_FIELD_DOTA_NONCMBT_NUQI_REGEN_RATIO: ('regenRatioSpeed', 3),
 PDD.data.PROPERTY_BATTLE_FIELD_DOTA_JINGQI_REGEN_RATIO: ('regenRatioSpeed', 2),
 PDD.data.PROPERTY_BATTLE_FIELD_DOTA_NONCMBT_JINGQI_REGEN_RATIO: ('regenRatioSpeed', 3),
 PDD.data.PROPERTY_BATTLE_FIELD_DOTA_NENGLIANG_REGEN_RATIO: ('regenRatioSpeed', 2),
 PDD.data.PROPERTY_BATTLE_FIELD_DOTA_NONCMBT_NENGLIANG_REGEN_RATIO: ('regenRatioSpeed', 3),
 PDD.data.PROPERTY_COMBAT_EP_REGEN: ('combatEpRegen', None),
 PDD.data.PROPERTY_NON_COMBAT_EP_REGEN: ('nonCombatEpRegen', 0),
 PDD.data.PROPERTY_WS_A_REGEN: ('wsRegen', 0),
 PDD.data.PROPERTY_NON_CMBT_WS_A_REGEN: ('wsRegen', 1),
 PDD.data.PROPERTY_WS_B_REGEN: ('wsRegen', 2),
 PDD.data.PROPERTY_NON_CMBT_WS_B_REGEN: ('wsRegen', 3),
 PDD.data.PROPERTY_DEAFEN_MINUS: ('deafenMinus', None),
 PDD.data.PROPERTY_RESTORE_HP: ('restore', 0),
 PDD.data.PROPERTY_RESTORE_MP: ('restore', 1),
 PDD.data.PROPERTY_QIJUE_ADD: ('mSpecialStateParam', 0),
 PDD.data.PROPERTY_MABI_ADD: ('mSpecialStateParam', 1),
 PDD.data.PROPERTY_SHUIMIAN_ADD: ('mSpecialStateParam', 2),
 PDD.data.PROPERTY_DESTROY_ADD: ('mSpecialStateParam', 3),
 PDD.data.PROPERTY_RELATION_EXP_ADD: ('expAdd', 0),
 PDD.data.PROPERTY_AVATAR_EXP_ADD: ('expAdd', 1),
 PDD.data.PROPERTY_PET_EXP_ADD: ('expAdd', 2),
 PDD.data.PROPERTY_WEAPON_EXP_ADD: ('expAdd', 3),
 PDD.data.PROPERTY_KILL_MONSTER_EXP_ADD: ('expAdd', 4),
 PDD.data.PROPERTY_ROD_ENHANCE: ('rodEnhance', None),
 PDD.data.PROPERTY_BATTLE_FIELD_DOTA_ADD_CASH_TIME: ('bfDotaAddCashTimeExtra', None),
 PDD.data.PROPERTY_BATTLE_FIELD_DOTA_ADD_CASH_MONSTER: ('bfDotaAddCashMonsterExtra', None),
 PDD.data.PROPERTY_BATTLE_FIELD_DOTA_ADD_EXP_MONSTER: ('bfDotaAddExpMonsterExtraRadio', None),
 PDD.data.PROPERTY_BATTLE_FIELD_DOTA_NORMAL_ATTACK_SPEED_INCREASE_RATIO: ('bfDotaNormalAttackSpeedIncreseRatio', None),
 PDD.data.PROPERTY_BATTLE_FIELD_DOTA_SKILL_ATTACK_SPEED_INCREASE_RATIO: ('bfDotaSkillAttackSpeedIncreseRatio', None),
 PDD.data.PROPERTY_BATTLE_FIELD_DOTA_NORMAL_ATTACK_XIXUE_RATIO: ('bfDotaXixueRatio', 0),
 PDD.data.PROPERTY_BATTLE_FIELD_DOTA_PHY_ATTACK_XIXUE_RATIO: ('bfDotaXixueRatio', 1),
 PDD.data.PROPERTY_BATTLE_FIELD_DOTA_MAG_ATTACK_XIXUE_RATIO: ('bfDotaXixueRatio', 2),
 PDD.data.PROPERTY_BATTLE_FIELD_DOTA_MIN_KEEP_NUQI_VAL: ('bfDotaZaijuMinNuqi', None),
 PDD.data.PROPERTY_SKILL_ATTACK_SPEED_INCREASE_RATIO: ('skillAttackSpeedIncreseRatio', None),
 PDD.data.PROPERTY_HOOK_ENHANCE: ('hookEnhance', None),
 PDD.data.PROPERTY_BUOY_ENHANCE: ('buoyEnhance', None),
 PDD.data.PROPERTY_PVP_ADD_FORCE: ('pvpForce', 0),
 PDD.data.PROPERTY_PVP_MINUS_FORCE: ('pvpForce', 1),
 PDD.data.PROPERTY_PVE_ADD_FORCE: ('pveForce', 0),
 PDD.data.PROPERTY_PVE_MINUS_FORCE: ('pveForce', 1),
 PDD.data.PROPERTY_PVP_ADD_RATIO: ('pvpRatio', 0),
 PDD.data.PROPERTY_PVP_MINUS_RATIO: ('pvpRatio', 1),
 PDD.data.PROPERTY_PVE_ADD_RATIO: ('pveRatio', 0),
 PDD.data.PROPERTY_PVE_MINUS_RATIO: ('pveRatio', 1),
 PDD.data.PROPERTY_PVE_QUOTA: ('pveQuota', None),
 PDD.data.PROPERTY_MIN_WSP_A: ('minws', 0),
 PDD.data.PROPERTY_MIN_WSP_B: ('minws', 1),
 PDD.data.PROPERTY_EQUIP_MIN_PHY_ATK: ('equipAtk', 0),
 PDD.data.PROPERTY_EQUIP_MAX_PHY_ATK: ('equipAtk', 1),
 PDD.data.PROPERTY_EQUIP_MIN_MAG_ATK: ('equipAtk', 2),
 PDD.data.PROPERTY_EQUIP_MAX_MAG_ATK: ('equipAtk', 3),
 PDD.data.PROPERTY_EQUIP_PHY_ATK_RATIO: ('equipAtkRatio', 0),
 PDD.data.PROPERTY_EQUIP_MAG_ATK_RATIO: ('equipAtkRatio', 1),
 PDD.data.PROPERTY_PHY_ATK_ADD: ('atkAdd', 0),
 PDD.data.PROPERTY_MAG_ATK_ADD: ('atkAdd', 1),
 PDD.data.PROPERTY_PHY_DMG_ADD_RAITO: ('dmgAddRaito', 0),
 PDD.data.PROPERTY_MAG_DMG_ADD_RAITO: ('dmgAddRaito', 1),
 PDD.data.PROPERTY_CRIT_FORCE: ('atkDefForce', 0),
 PDD.data.PROPERTY_HIT_FORCE: ('atkDefForce', 1),
 PDD.data.PROPERTY_CRIT_RATIO: ('atkDefRatio', 0),
 PDD.data.PROPERTY_HIT_RATIO: ('atkDefRatio', 1),
 PDD.data.PROPERTY_CRIT_ADD: ('atkDefAdd', 0),
 PDD.data.PROPERTY_PHY_DEF_OVERCOME: ('defCrush', 0),
 PDD.data.PROPERTY_MEG_DEF_OVERCOME: ('defCrush', 1),
 PDD.data.PROPERTY_CONTROL_LV: ('stateControlLv', 0),
 PDD.data.PROPERTY_EQUIP_PHY_DEF: ('equipDef', 0),
 PDD.data.PROPERTY_EQUIP_MAG_DEF: ('equipDef', 1),
 PDD.data.PROPERTY_EQUIP_PHY_DEF_RATIO: ('equipDefRatio', 0),
 PDD.data.PROPERTY_EQUIP_MAG_DEF_RATIO: ('equipDefRatio', 1),
 PDD.data.PROPERTY_PHY_DMG_MIN: ('dmgMinusRatio', 0),
 PDD.data.PROPERTY_MAG_DMG_MIN: ('dmgMinusRatio', 1),
 PDD.data.PROPERTY_PHY_DMG_MIN_EX1: ('dmgMinusRatio', 2),
 PDD.data.PROPERTY_MAG_DMG_MIN_EX1: ('dmgMinusRatio', 3),
 PDD.data.PROPERTY_PHY_DMG_MIN_EX2: ('dmgMinusRatio', 4),
 PDD.data.PROPERTY_MAG_DMG_MIN_EX2: ('dmgMinusRatio', 5),
 PDD.data.PROPERTY_BLOCK_FORCE: ('atkDefForce', 2),
 PDD.data.PROPERTY_AVOID_FORCE: ('atkDefForce', 3),
 PDD.data.PROPERTY_CRIT_DEF_FORCE: ('atkDefForce', 4),
 PDD.data.PROPERTY_CRIT_ADD_FORCE: ('atkDefForce', 5),
 PDD.data.PROPERTY_CRIT_MINUS_FORCE: ('atkDefForce', 6),
 PDD.data.PROPERTY_CRIT_DEF_IGN_FORCE: ('atkDefForce', 7),
 PDD.data.PROPERTY_BLOCK_RATIO: ('atkDefRatio', 2),
 PDD.data.PROPERTY_AVOID_RATIO: ('atkDefRatio', 3),
 PDD.data.PROPERTY_CRIT_DEF_RATIO: ('atkDefRatio', 4),
 PDD.data.PROPERTY_BLOCK_ADD: ('atkDefAdd', 1),
 PDD.data.PROPERTY_CRIT_MINUS: ('atkDefAdd', 2),
 PDD.data.PROPERTY_AVOID_ADD: ('atkDefAdd', 3),
 PDD.data.PROPERTY_CONTROL_DEF_LV: ('stateControlLv', 1),
 PDD.data.PROPERTY_PHY_DEF_ADD: ('defAdd', 0),
 PDD.data.PROPERTY_MGI_DEF_ADD: ('defAdd', 1),
 PDD.data.PROPERTY_HEAL_ADD: ('healAdd', None),
 PDD.data.PROPERTY_HEAL_ADD_RATIO: ('healRaito', 0),
 PDD.data.PROPERTY_HEAL_MINUS_RATIO: ('healRaito', 1),
 PDD.data.PROPERTY_BEHEALED_ADD_RATIO: ('healRaito', 2),
 PDD.data.PROPERTY_BEHEALED_MINUS_RATIO: ('healRaito', 3),
 PDD.data.PROPERTY_MAX_WSP_A: ('mws', 0),
 PDD.data.PROPERTY_MAX_WSP_B: ('mws', 1),
 PDD.data.PROPERTY_GCD_MINUS: ('skillAdd', 0),
 PDD.data.PROPERTY_GCD_MINUS_RATIO: ('skillAdd', 1),
 PDD.data.PROPERTY_SKILL_DIST_ADD: ('skillAdd', 2),
 PDD.data.PROPERTY_SKILL_DIST_ADD_RATIO: ('skillAdd', 3),
 PDD.data.PROPERTY_SPELL_TIME_MINUS: ('skillAdd', 4),
 PDD.data.PROPERTY_SPELL_TIME_MINUS_RATIO: ('skillAdd', 5),
 PDD.data.PROPERTY_SPELL_TIME_MINUS_RATIO_SPRITE: ('skillAdd', 6),
 PDD.data.PROPERTY_SPRITE_CD_REDUCE: ('spriteCDReduce', 0),
 PDD.data.PROPERTY_SPRITE_CD_REDUCE_RATIO: ('spriteCDReduce', 1),
 PDD.data.PROPERTY_SPRITE_AWAKE_CD_REDU: ('spriteCDReduce', 2),
 PDD.data.PROPERTY_SPRITE_AWAKE_CD_REDU_R: ('spriteCDReduce', 3),
 PDD.data.PROPERTY_MOVE_SPEED: ('speed', 0),
 PDD.data.PROPERTY_FLY_SPEED: ('speed', 3),
 PDD.data.PROPERTY_SWIM_SPEED: ('speed', 4),
 PDD.data.PROPERTY_RIDE_SPEED: ('speed', 5),
 PDD.data.PROPERTY_YAOLI_REDUCE: ('yaoliReducePercent', None),
 PDD.data.PROPERTY_MLABOUR: ('mLabour', None),
 PDD.data.PROPERTY_MMENTAL: ('mMental', None),
 PDD.data.PROPERTY_WALK_EP_REGEN_ADJUST: ('nonCombatEpRegen', 1),
 PDD.data.PROPERTY_RIDE_EP_REGEN_ADJUST: ('nonCombatEpRegen', 2),
 PDD.data.PROPERTY_WING_EP_REGEN_ADJUST: ('nonCombatEpRegen', 3),
 PDD.data.PROPERY_VIRUSSAFE_REGEN: ('virussafeRegen', None),
 PDD.data.PROPERTY_VP_DAILY_ADD: ('vpAdd', 0),
 PDD.data.PROPERTY_VP_LVUP_ADD: ('vpAdd', 1),
 PDD.data.PROPERTY_MAX_VP: ('vpAdd', 2),
 PDD.data.PROPERTY_STAGE_RATIO_ADD: ('vpAdd', 3),
 PDD.data.PROPERTY_TOOL_DR_A: ('lifeEquipDuraReduce', 0),
 PDD.data.PROPERTY_TOOL_DR_B: ('lifeEquipDuraReduce', 1),
 PDD.data.PROPERTY_TOOL_DR_C: ('lifeEquipDuraReduce', 2),
 PDD.data.PROPERTY_TOOL_DR_D: ('lifeEquipDuraReduce', 3),
 PDD.data.PROPERTY_TOOL_DR_E: ('lifeEquipDuraReduce', 4),
 PDD.data.PROPERTY_TOOL_DR_F: ('lifeEquipDuraReduce', 5),
 PDD.data.PROPERTY_TOOL_FR_A: ('lifeEquipFixReduce', 0),
 PDD.data.PROPERTY_TOOL_FR_B: ('lifeEquipFixReduce', 1),
 PDD.data.PROPERTY_TOOL_FR_C: ('lifeEquipFixReduce', 2),
 PDD.data.PROPERTY_TOOL_FR_D: ('lifeEquipFixReduce', 3),
 PDD.data.PROPERTY_TOOL_FR_E: ('lifeEquipFixReduce', 4),
 PDD.data.PROPERTY_TOOL_FR_F: ('lifeEquipFixReduce', 5),
 PDD.data.PROPERTY_FIRE_ATK: ('elementAtk', 0),
 PDD.data.PROPERTY_ICE_ATK: ('elementAtk', 1),
 PDD.data.PROPERTY_THUNDER_ATK: ('elementAtk', 2),
 PDD.data.PROPERTY_EARTH_ATK: ('elementAtk', 3),
 PDD.data.PROPERTY_DARK_ATK: ('elementAtk', 4),
 PDD.data.PROPERTY_LIGHT_ATK: ('elementAtk', 5),
 PDD.data.PROPERTY_SOUL_ATK: ('elementAtk', 6),
 PDD.data.PROPERTY_FIRE_DEF: ('elementDef', 0),
 PDD.data.PROPERTY_ICE_DEF: ('elementDef', 1),
 PDD.data.PROPERTY_THUNDER_DEF: ('elementDef', 2),
 PDD.data.PROPERTY_EARTH_DEF: ('elementDef', 3),
 PDD.data.PROPERTY_DARK_DEF: ('elementDef', 4),
 PDD.data.PROPERTY_LIGHT_DEF: ('elementDef', 5),
 PDD.data.PROPERTY_SOUL_DEF: ('elementDef', 6),
 PDD.data.PROPERTY_FIRE_TRANS_RATIO: ('elementRatio', 0),
 PDD.data.PROPERTY_ICE_TRANS_RATIO: ('elementRatio', 1),
 PDD.data.PROPERTY_THUNDER_TRANS_RATIO: ('elementRatio', 2),
 PDD.data.PROPERTY_EARTH_TRANS_RATIO: ('elementRatio', 3),
 PDD.data.PROPERTY_DARK_TRANS_RATIO: ('elementRatio', 4),
 PDD.data.PROPERTY_LIGHT_TRANS_RATIO: ('elementRatio', 5),
 PDD.data.PROPERTY_SOUL_TRANS_RATIO: ('elementRatio', 6),
 PDD.data.PROPERTY_WS_DMG_ADD_FORCE: ('wsSkillDmgAdd', 0),
 PDD.data.PROPERTY_WS_DMG_ADD_RATIO: ('wsSkillDmgAddRatio', 0),
 PDD.data.PROPERTY_WS_DMG_MINUS_FORCE: ('wsSkillDmgAdd', 1),
 PDD.data.PROPERTY_WS_DMG_MINUS_RATIO: ('wsSkillDmgAddRatio', 1),
 PDD.data.PROPERTY_BOSS_DMG_ADD_RATIO: ('bossDmgAddRatio', None),
 PDD.data.PROPERTY_BOSS_DMG_ADD_FORCE: ('bossDmgAddForce', None),
 PDD.data.PROPERTY_MEP: ('mep', None),
 PDD.data.PROPERTY_SOC_EXP_ADD: ('socExpAdd', None),
 PDD.data.PROPERTY_PHY_HURT_REDUCE_RATIO: ('hurtReduceRatio', 0),
 PDD.data.PROPERTY_MAG_HURT_REDUCE_RATIO: ('hurtReduceRatio', 1),
 PDD.data.PROPERTY_PHY_HURT_RATIO: ('atkDefRatio', 5),
 PDD.data.PROPERTY_MAG_HURT_RATIO: ('atkDefRatio', 6),
 PDD.data.PROPERTY_PHY_DEFENSE_RATIO: ('atkDefRatio', 7),
 PDD.data.PROPERTY_MAG_DEFENSE_RATIO: ('atkDefRatio', 8),
 PDD.data.PROPERTY_HEAL_RATIO: ('atkDefRatio', 9),
 PDD.data.PROPERTY_PHY_DEF_CRUSH_RATIO: ('defCrushRatio', 0),
 PDD.data.PROPERTY_MAG_DEF_CRUSH_RATIO: ('defCrushRatio', 1),
 PDD.data.PROPERTY_WS_A_REDUCE: ('wsReduce', 0),
 PDD.data.PROPERTY_WS_B_REDUCE: ('wsReduce', 1),
 PDD.data.PROPERTY_BLESS_FORCE: ('blessCurseForce', 0),
 PDD.data.PROPERTY_CURSE_FORCE: ('blessCurseForce', 1),
 PDD.data.PROPERTY_BLESS_RATIO: ('blessCurseRatio', 0),
 PDD.data.PROPERTY_CURSE_RATIO: ('blessCurseRatio', 1),
 PDD.data.PROPERTY_DEF_OVERCOME_RESIST: ('defOvercomeResist', None),
 PDD.data.PROPERTY_DEF_OVERCOME_RESIST_RATIO: ('defOvercomeResistRatio', None),
 PDD.data.PROPERTY_COMBAT_SPEED_INCREASE_RATIO_SPRITE: ('combatSpeedIncreseRatio', 0),
 PDD.data.PROPERTY_COMBAT_SPEED_INCREASE_RATIO: ('combatSpeedIncreseRatio', 1),
 PDD.data.DEFENSE_DIRECT_REDUCE_PHY: ('defDirectReduce', 0),
 PDD.data.DEFENSE_DIRECT_REDUCE_MAG: ('defDirectReduce', 1),
 PDD.data.PROPERTY_SPRITE_DOUBLESTRIKE_RATIO: ('doubleStrike', 0),
 PDD.data.PROPERTY_SPRITE_DOUBLESTRIKE_DEF_RATIO: ('doubleStrike', 1),
 PDD.data.PROPERTY_SPRITE_MULTISTRIKE_RATIO: ('multiStrikeRatio', None),
 PDD.data.PROPERTY_SPRITE_CRITICALSTRIKE_RATIO: ('huixinStrike', 0),
 PDD.data.PROPERTY_SPRITE_CRITICALSTRIKE_DEF_RATIO: ('huixinStrike', 1),
 PDD.data.PROPERTY_SPRITE_CRITICALSTRIKE_ADD_RATIO: ('huixinStrike', 2),
 PDD.data.PROPERTY_NORMAL_SKILL_ADD_FORCE: ('skillForce', 0),
 PDD.data.PROPERTY_NORMAL_SKILL_MINUS_FORCE: ('skillForce', 1),
 PDD.data.PROPERTY_WS1_SKILL_ADD_FORCE: ('skillForce', 2),
 PDD.data.PROPERTY_WS1_SKILL_MINUS_FORCE: ('skillForce', 3),
 PDD.data.PROPERTY_WS2_SKILL_ADD_FORCE: ('skillForce', 4),
 PDD.data.PROPERTY_WS2_SKILL_MINUS_FORCE: ('skillForce', 5),
 PDD.data.PROPERTY_WS3_SKILL_ADD_FORCE: ('skillForce', 6),
 PDD.data.PROPERTY_WS3_SKILL_MINUS_FORCE: ('skillForce', 7),
 PDD.data.PROPERTY_NORMAL_SKILL_ADD_RATIO: ('skillRatio', 0),
 PDD.data.PROPERTY_NORMAL_SKILL_MINUS_RATIO: ('skillRatio', 1),
 PDD.data.PROPERTY_WS1_SKILL_ADD_RATIO: ('skillRatio', 2),
 PDD.data.PROPERTY_WS1_SKILL_MINUS_RATIO: ('skillRatio', 3),
 PDD.data.PROPERTY_WS2_SKILL_ADD_RATIO: ('skillRatio', 4),
 PDD.data.PROPERTY_WS2_SKILL_MINUS_RATIO: ('skillRatio', 5),
 PDD.data.PROPERTY_WS3_SKILL_ADD_RATIO: ('skillRatio', 6),
 PDD.data.PROPERTY_WS3_SKILL_MINUS_RATIO: ('skillRatio', 7),
 PDD.data.PROPERTY_FROM_LOW_HP_ADD_FORCE: ('dmgForceByHpPct', 0),
 PDD.data.PROPERTY_FROM_LOW_HP_MINUS_FORCE: ('dmgForceByHpPct', 1),
 PDD.data.PROPERTY_FROM_HIGH_HP_ADD_FORCE: ('dmgForceByHpPct', 2),
 PDD.data.PROPERTY_FROM_HIGH_HP_MINUS_FORCE: ('dmgForceByHpPct', 3),
 PDD.data.PROPERTY_TO_LOW_HP_ADD_FORCE: ('dmgForceByHpPct', 4),
 PDD.data.PROPERTY_TO_LOW_HP_MINUS_FORCE: ('dmgForceByHpPct', 5),
 PDD.data.PROPERTY_TO_HIGH_HP_ADD_FORCE: ('dmgForceByHpPct', 6),
 PDD.data.PROPERTY_TO_HIGH_HP_MINUS_FORCE: ('dmgForceByHpPct', 7),
 PDD.data.PROPERTY_FROM_LOW_HP_ADD_RATIO: ('dmgRatioByHpPct', 0),
 PDD.data.PROPERTY_FROM_LOW_HP_MINUS_RATIO: ('dmgRatioByHpPct', 1),
 PDD.data.PROPERTY_FROM_HIGH_HP_ADD_RATIO: ('dmgRatioByHpPct', 2),
 PDD.data.PROPERTY_FROM_HIGH_HP_MINUS_RATIO: ('dmgRatioByHpPct', 3),
 PDD.data.PROPERTY_TO_LOW_HP_ADD_RATIO: ('dmgRatioByHpPct', 4),
 PDD.data.PROPERTY_TO_LOW_HP_MINUS_RATIO: ('dmgRatioByHpPct', 5),
 PDD.data.PROPERTY_TO_HIGH_HP_ADD_RATIO: ('dmgRatioByHpPct', 6),
 PDD.data.PROPERTY_TO_HIGH_HP_MINUS_RATIO: ('dmgRatioByHpPct', 7),
 PDD.data.PROPERTY_DMG_ADD_RATIO_TO_PLAYER: ('dmgAddRatioByTgtType', 0),
 PDD.data.PROPERTY_DMG_ADD_RATIO_TO_CARRIER: ('dmgAddRatioByTgtType', 1),
 PDD.data.PROPERTY_DMG_ADD_RATIO_TO_BUILDING: ('dmgAddRatioByTgtType', 2),
 PDD.data.PROPERTY_DMG_ADD_FORCE_TO_SPRITE: ('dmgForceAboutSprite', 0),
 PDD.data.PROPERTY_DMG_MINUS_FORCE_FROM_SPRITE: ('dmgForceAboutSprite', 1),
 PDD.data.PROPERTY_DMG_ADD_RATIO_TO_SPRITE: ('dmgRatioAboutSprite', 0),
 PDD.data.PROPERTY_DMG_MINUS_RATIO_FROM_SPRITE: ('dmgRatioAboutSprite', 1),
 PDD.data.PROPERTY_DMG_ADD_FORCE_LOW_EP: ('dmgForceAboutEP', 0),
 PDD.data.PROPERTY_DMG_MINUS_FORCE_LOW_EP: ('dmgForceAboutEP', 1),
 PDD.data.PROPERTY_DMG_ADD_RATIO_LOW_EP: ('dmgRatioAboutEP', 0),
 PDD.data.PROPERTY_DMG_MINUS_RATIO_LOW_EP: ('dmgRatioAboutEP', 1)}
PROP_FIXED_MAP = {PDD.data.PROPERTY_ATK_SPEED: ('speed', 1),
 PDD.data.PROPERTY_LV: ('lv', None),
 PDD.data.PROPERTY_EXP: ('exp', None),
 PDD.data.PROPERTY_HP: ('hp', None),
 PDD.data.PROPERTY_MP: ('mp', None),
 PDD.data.PROPERTY_BATTLE_FIELD_DOTA_NUQI_PROP_VAL: ('mp', None),
 PDD.data.PROPERTY_BATTLE_FIELD_DOTA_JINGQI_PROP_VAL: ('mp', None),
 PDD.data.PROPERTY_BATTLE_FIELD_DOTA_NENGLIANG_PROP_VAL: ('mp', None),
 PDD.data.PROPERTY_SKILL_POINT: ('skillPoint', None),
 PDD.data.PROPERTY_EP: ('ep', None),
 PDD.data.PROPERTY_WS_A: ('ws', 0),
 PDD.data.PROPERTY_WS_B: ('ws', 1),
 PDD.data.PROPERTY_BASE_VP: ('baseVp', None),
 PDD.data.PROPERTY_SOC_EXP: ('socExp', None),
 PDD.data.PROPERTY_FISH_ATTRACTION: ('fishAttraction', None),
 PDD.data.PROPERTY_TOTAL_SKILL_ENHANCE_POINT: ('totalSkillEnhancePoint', None)}
PROP_MAP = dict(PROP_RECALC_MAP)
PROP_MAP.update(PROP_FIXED_MAP)

def _calcPropReverseMap(propMap):
    reverseMap = {}
    for propId, (propName, propIndex) in propMap.iteritems():
        reverseMap.setdefault(propName, {})[propIndex] = propId

    return reverseMap


PROP_REVERSE_MAP = _calcPropReverseMap(PROP_MAP)

def _getPropIdByNameAndIndex(propName, index):
    return PROP_REVERSE_MAP.get(propName, {}).get(index, 0)


def genBitSet(setbits):
    a = bytearray()
    for x in list(setbits):
        setBit(a, x, on=True)

    return a


def getAlternativeEquip(owner, part):
    if part < 0:
        return None
    if not gametypes.equipTosubEquipPartMap.has_key(part):
        return None
    dstPart = gametypes.equipTosubEquipPartMap[part]
    return owner.subEquipment.get(const.DEFAULT_SUB_EQU_PAGE_NO, dstPart)


def getEquipShareEnhProp(owner, sEquip, tEquip):
    if not sEquip and not tEquip:
        return {}
    calcEquip = None
    calcLv = 0
    if sEquip and not tEquip:
        calcEquip = sEquip
        calcLv = getattr(sEquip, 'enhLv', 0)
    elif tEquip and not sEquip:
        calcEquip = tEquip
        calcLv = getattr(tEquip, 'enhLv', 0)
    elif sEquip and tEquip:
        sLv = getattr(sEquip, 'enhLv', 0)
        tLv = getattr(tEquip, 'enhLv', 0)
        calcLv = max(sLv, tLv)
        calcEquip = sEquip if sLv >= tLv else tEquip
    if not calcEquip:
        return {}
    data = {'enhLv': calcLv,
     'maxEnhlv': sEquip.getMaxEnhLv(owner),
     'enhanceRefining': getattr(calcEquip, 'enhanceRefining', {}),
     'enhJuexingData': getattr(calcEquip, 'enhJuexingData', {}),
     'enhJuexingAddRatio': getattr(calcEquip, 'enhJuexingAddRatio', {}),
     'equipType': sEquip.equipType,
     'equipSType': sEquip.equipSType,
     'enhanceType': sEquip.enhanceType}
    return data


def canPursueYaoPei():
    openTime = int(utils.getServerOpenTime())
    sd = PSCD.data.get(utils.getHostId(), {})
    if sd.has_key('ypInterval'):
        ypDelayTime = sd.get('ypInterval', 0) * const.TIME_INTERVAL_WEEK
    else:
        ypDelayTime = 0
    weekDiff = utils.getIntervalWeek(openTime + ypDelayTime, utils.getNow())
    yd = PYD.data.get(weekDiff)
    return yd


def canPursuePvpEnh():
    openTime = int(utils.getServerOpenTime())
    sd = PSCD.data.get(utils.getHostId(), {})
    if sd.has_key('pvpInterval'):
        pvpDelayTime = sd.get('pvpInterval', 0) * const.TIME_INTERVAL_WEEK
    else:
        pvpDelayTime = 0
    weekDiff = utils.getIntervalWeek(openTime + pvpDelayTime, utils.getNow())
    pd = PPED.data.get(weekDiff)
    return pd


def calcPursueYaoPeiData(item):
    item.curPursueNum = 0
    item.maxPursueNum = 0
    yd = canPursueYaoPei()
    if yd:
        pId = SCD.data.get('pursueYaoPeiFormulaId', 0)
        key = 'standard' + str(item.quality)
        n0 = yd.get(key, 0)
        n1 = getattr(item, 'yaoPeiExp', 0)
        item.maxPursueNum = formula.calcFormulaById(pId, {'e': math.e,
         'n0': n0,
         'n1': n1})


def getConsignMaxFixedPrice(num, avgPrice):
    return max(avgPrice * 3, 1000) * num


def calcFbMonsterDmgFixToSprite(mapId, src, tgt, dmg):
    fixedDmg = dmg
    if src.IsMonster and tgt.IsSummonedSprite:
        mDmgRatio = MCD.data.get(formula.getMapId(tgt.spaceNo), {}).get('dmgRatioMonsterToSprite', None)
        if mDmgRatio is not None:
            if gametypes.SKILL_STATE_SE_FB_MONSTER_DEC_TO_SPRITE in tgt.statesSpecialEffectCache:
                minRatioToSprite = 1
                for eachParam in tgt.getStateSpecialEffectParam(gametypes.SKILL_STATE_SE_FB_MONSTER_DEC_TO_SPRITE, []):
                    if eachParam < minRatioToSprite:
                        minRatioToSprite = eachParam

                mDmgRatio *= minRatioToSprite
            fixedDmg *= max(0, mDmgRatio)
    return int(fixedDmg)


def getLifeLinkedTgts(combatUnit, lifeLinkInfo, exclude = ()):
    """
    \xbb\xf1\xb5\xc3\xc9\xfa\xc3\xfc\xc1\xb4\xbd\xd3\xb5\xc4\xd7\xb7\xbc\xd3\xbd\xe1\xcb\xe3\xb6\xd4\xcf\xf3
    :param combatUnit: \xb1\xbb\xb9\xa5\xbb\xf7\xb7\xbd
    :param lifeLinkInfo: \xb1\xbb\xb9\xa5\xbb\xf7\xb7\xbd\xb5\xc4\xc9\xfa\xc3\xfc\xc1\xb4\xbd\xd3\xca\xfd\xbe\xdd
    :return: \xb4\xab\xb5\xdd\xc4\xbf\xb1\xea\xbc\xaf\xba\xcf\xa1\xa2\xb7\xd6\xcc\xaf\xc4\xbf\xb1\xea\xbc\xaf\xba\xcf
    """
    from data import life_link_data as LLD
    linkTgtsChuandi = set()
    linkTgtsFentan = set()
    for stId, linkInfo in lifeLinkInfo.iteritems():
        if stId in exclude:
            continue
        linkId = linkInfo.get('linkId', 0)
        linkType = LLD.data.get(linkId, {}).get('type', gametypes.LIFE_LINK_TYPE_DEFAULT)
        if linkType == gametypes.LIFE_LINK_TYPE_DEFAULT:
            continue
        for linkEntId in linkInfo.get('globalLinkedEntIds', []):
            linkedEnt = BigWorld.entities.get(linkEntId)
            if linkedEnt:
                if linkType == gametypes.LIFE_LINK_TYPE_CHAUNDI:
                    linkTgtsChuandi.add(linkedEnt)
                elif linkType == gametypes.LIFE_LINK_TYPE_FENTAN:
                    linkTgtsFentan.add(linkedEnt)

    linkTgtsChuandi = linkTgtsChuandi - linkTgtsFentan
    linkTgtsChuandi.discard(combatUnit)
    linkTgtsFentan.discard(combatUnit)
    return (linkTgtsChuandi, linkTgtsFentan)


def getLifeLinkRealValue(srcVal, linkTgtsChuandi, linkTgtsFentan):
    realVal = srcVal
    fentanSize = len(linkTgtsFentan)
    if fentanSize > 0:
        realVal = int(realVal / (fentanSize + 1))
    return realVal


def checkEntCanMove(src, tgt, moveType):
    srcFlag = src.getStateSpecialEffectParam(gametypes.SKILL_STATE_SE_IMMUNE_MOVE, None) if hasattr(src, 'statesSpecialEffectCache') else None
    tgtFlag = tgt.getStateSpecialEffectParam(gametypes.SKILL_STATE_SE_IMMUNE_MOVE, None) if hasattr(tgt, 'statesSpecialEffectCache') else None
    srcCanMove = True
    if srcFlag == 0:
        srcCanMove = False
    tgtCanMove = True
    if tgtFlag == 0:
        tgtCanMove = False
    elif tgtFlag == 1 and src.isEnemy(tgt):
        tgtCanMove = False
    elif tgtFlag == 2 and src.id != tgt.id:
        tgtCanMove = False
    if moveType == gametypes.MOVEMENT_SKILL_MOVE_SELF:
        return srcCanMove
    if moveType == gametypes.MOVEMENT_SKILL_MOVE_TGT:
        return tgtCanMove
    if moveType == gametypes.MOVEMENT_SKILL_MOVE_SELF_AND_TGT:
        return srcCanMove and tgtCanMove
    return True


def calcXiXueParamBySE(owner, param):
    if owner and hasattr(owner, 'statesSpecialEffectCache') and gametypes.SKILL_STATE_SE_ADD_XI_XUE_PARAM in owner.statesSpecialEffectCache:
        s = sum(owner.statesSpecialEffectCache.get(gametypes.SKILL_STATE_SE_ADD_XI_XUE_PARAM, []))
        param *= s
    return param


if BigWorld.component in ('base', 'cell'):

    def getTgtDmgMinusRatio(tgtcd, offset1, ignoreList = None):
        multiRatio = 1 - tgtcd.dmgMinusRatio[4 + offset1]
        subRation = tgtcd.dmgMinusRatio[0 + offset1]
        totalReduceRate = 0
        for ignoreEX1Type, reduceRate in ignoreList or []:
            if ignoreEX1Type == const.IGNORE_EX1_TYPE_IGNORE_ALL or ignoreEX1Type == const.IGNORE_EX1_TYPE_IGNORE_PHY and offset1 == 0 or ignoreEX1Type == const.IGNORE_EX1_TYPE_IGNORE_MAG and offset1 == 1:
                totalReduceRate += reduceRate

        if totalReduceRate:
            gamelog.debug('xjw## getTgtDmgMinusRatio, totalReduceRate', totalReduceRate, offset1, tgtcd.dmgMinusRatio[2 + offset1])
        subRation += max(0, tgtcd.dmgMinusRatio[2 + offset1] - totalReduceRate)
        return (1 - min(gameconst.DMG_MINUS_RATIO_UP_LIMIT, subRation)) * multiRatio


    def getDmgMinusRatioIgnoreType(srccd, tgttcd):
        if not srccd or not tgttcd:
            return []
        if not getattr(srccd, 'IsAvatar', False) or not getattr(tgttcd, 'IsAvatar', False):
            return []
        src = srccd.owner
        tgt = tgttcd.owner
        effects = srccd.statesSpecialEffectPubCache.get(gametypes.SKILL_STATE_SE_IGNORE_EX1_FIX_TO_CAST_TGT, [])
        if not effects:
            return []
        ignoreTypeDict = {}
        checkEffectDict = {}
        for param in effects:
            stateId, ignoreType, ignoreRate = param
            if not checkEffectDict.has_key(stateId):
                hasState = tgt.hasStateWithSrc(stateId, 0, src.id)
                checkEffectDict[stateId] = hasState
            if not checkEffectDict.get(stateId, False):
                continue
            if not ignoreType:
                ignoreType = 1
            ignoreTypeDict[ignoreType] = ignoreTypeDict.get(ignoreType, 0) + ignoreRate

        return zip(ignoreTypeDict.keys(), ignoreTypeDict.values())
