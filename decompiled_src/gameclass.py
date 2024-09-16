#Embedded file name: /WORKSPACE/data/entities/common/gameclass.o
import copy
import time
import BigWorld
if BigWorld.component in ('base', 'cell'):
    import gameengine
if BigWorld.component in 'client' and not getattr(BigWorld, 'isBot', False):
    from data import skill_general_template_data as SGTD
from data import skill_effects_data as SEFFD
import traceback
import cStringIO
import formula
import const
import gametypes
import utils
import commcalc
import sys
import random
from sMath import limit
from gamelog import error
from gamestrings import gameStrings
from userSoleType import UserSoleType
from userListType import UserListType
from userDictType import UserDictType
from data import skill_general_data as SGD
from data import state_data as SD
from data import state_group_inverted_index_data as SGIID
from cdata import pskill_data as PD
from cdata import pskill_template_data as PSTD
from data import skill_creation_data as SCD

class Singleton(type):

    def __init__(cls, name, bases, dic):
        super(Singleton, cls).__init__(name, bases, dic)
        cls.instance = None

    def __call__(cls, *args, **kwargs):
        error('please use getInstance function to get the instance')

    def getInstance(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance


class SkillDataBase(object):

    def __init__(self, num, lv):
        super(SkillDataBase, self).__init__()
        self.num = num
        self.lv = lv
        self.skillData = None

    def getSkillData(self, key, default = 0):
        return self.skillData.get(key, default)

    def hasSkillData(self, key):
        return self.skillData.has_key(key)


class CombatCreationInfo(object):
    DATA_TYPE = const.COMBAT_CREATION_INFO
    COMBAT_CREATION_ID_BASE = 20000
    LV_DEPENDENT_ATTR_LIST = SCD.data.get(const.LV_DEPENDENT_ATTR_ID, [])
    LV_DEPENDENT_ATTR_DICT = dict(zip(LV_DEPENDENT_ATTR_LIST, [1] * len(LV_DEPENDENT_ATTR_LIST))) if len(LV_DEPENDENT_ATTR_LIST) > 0 else {}

    def __init__(self, cid, clv, sid, slv = 1, addWsFlag = False, hijackData = {}):
        super(CombatCreationInfo, self).__init__()
        self.num = cid
        self.lv = clv
        self.sid = sid
        self.slv = slv
        self.addWsFlag = addWsFlag
        skillData = SGD.data.get((sid, slv), {})
        self.isWsCreation = skillData.has_key('wsNeed1') or skillData.has_key('wsNeed2')
        self.combatCreationData = SCD.data.get(cid, None)
        if self.combatCreationData == None:
            raise Exception('combatCreationInfo is None. %d, %d' % (cid, clv))
        self.hijackData = copy.copy(hijackData)

    def getCombatCreationData(self, key, default = 0):
        if self.hijackData.has_key(key):
            return self.hijackData[key]
        if key in self.LV_DEPENDENT_ATTR_DICT:
            try:
                d = self.combatCreationData.get(key, default)
                if type(d) == list:
                    return d[self.slv - 1]
                return d
            except (TypeError, KeyError, IndexError):
                return default

        return self.combatCreationData.get(key, default)

    def hasCombatCreationData(self, key):
        return self.combatCreationData.has_key(key)

    def setHijackData(self, key, val):
        self.hijackData[key] = val

    def updateHijackData(self, data):
        self.hijackData.update(data)


class SimpleCreationInfo(object):

    def __init__(self, cid):
        self.combatCreationData = SCD.data.get(cid, {})

    def getCombatCreationData(self, key, default = 0):
        return self.combatCreationData.get(key, default)

    def hasCombatCreationData(self, key):
        return self.combatCreationData.has_key(key)


SKILL_CATEGORY = 'skillCategory'

class SkillInfo(SkillDataBase):
    DATA_TYPE = const.SKILL_INFO
    LV_DEPENDENT_ATTR_LIST = set()

    def __init__(self, num, lv):
        super(SkillInfo, self).__init__(num, lv)
        if utils.isMonsterSkill(num):
            lv = const.MONSTER_SKILL_LV
        lv = min(const.MAX_SKILL_LEVEL, lv)
        self.skillData = SGD.data.get((num, lv), {})
        if not self.skillData and num:
            if BigWorld.component in ('base', 'cell'):
                gameengine.reportCritical('skill data not found! skillId: %d. sillLv: %d ' % (self.num, self.lv))
            else:
                msg = 'skill data not found! skillId: %d. sillLv: %d ' % (self.num, self.lv)
                try:
                    if random.randint(1, 100) < 10:
                        traceback.print_stack(None, None, sys.stdout)
                        outputFile = cStringIO.StringIO()
                        outputFile.write(msg + '\n')
                        traceback.print_stack(None, None, outputFile)
                        traceMsg = outputFile.getvalue()[0:512]
                        BigWorld.player().reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_CRITICAL, [traceMsg], 0, {})
                except:
                    pass

        self.hijackData = {}
        self.hijackDataCache = {}

    def evalSkillData(self, key, default = 0):
        data = self.skillData.get(key, None)
        if data == None:
            return default
        return formula.evalScript(self.lv, data)

    def getSkillTargetType(self):
        for key, value in gametypes.SKILL_TGT_DICT.iteritems():
            if self.hasSkillData(key):
                return (value, self.getSkillData(key))

        return (gametypes.SKILL_TARGET_NONE, 1)

    def getSkillData(self, key, default = 0):
        if self.hijackData.has_key(key):
            return self.hijackData[key]
        return self.skillData.get(key, default)

    def hasSkillData(self, key):
        return self.skillData.has_key(key) or self.hijackData.has_key(key)

    def isWsSkill(self):
        return self.getSkillData(SKILL_CATEGORY) == const.SKILL_CATEGORY_WS

    def isAirSkill(self):
        return self.getSkillData(SKILL_CATEGORY) == const.SKILL_CATEGORY_AIR

    def isMobaAtkSkill(self):
        return self.getSkillData(SKILL_CATEGORY) == const.SKILL_CATEGORY_BF_DOTA_NORMAL

    def isTargetSkill(self):
        noTgt = self.getSkillData('noTgt', 0)
        tgtSelf = self.getSkillData('tgtSelf', 0)
        tgtPos = self.getSkillData('tgtPos', 0)
        tgtDir = self.getSkillData('tgtDir', 0)
        return not noTgt | tgtSelf | tgtPos | tgtDir

    def setHijackData(self, key, val):
        self.hijackData[key] = val

    def updateHijackData(self, data):
        self.hijackData.update(data)

    def initHijackDataByPskills(self, owner):
        pass

    def __str__(self):
        return '(%d, %d)' % (self.num, self.lv)


if BigWorld.component in ('client',) and not getattr(BigWorld, 'isBot', False):

    def _getSkillData(self, key, default = 0):
        if self.hijackData.has_key(key):
            return self.hijackData[key]
        sgTemplateData = SGTD.data.get(self.num, {})
        if sgTemplateData.has_key(key):
            return sgTemplateData.get(key)
        return self.skillData.get(key, default)


    SkillInfo.getSkillData = _getSkillData
if BigWorld.component in ('client',):

    def _hasSkillData(self, key):
        sgTemplateData = SGTD.data.get(self.num, {})
        templateHasKey = sgTemplateData.has_key(key)
        return self.skillData.has_key(key) or self.hijackData.has_key(key) or templateHasKey


    SkillInfo.hasSkillData = _hasSkillData
ATTR_ID_BASE = 'attrId'
ATTR_VAL_TYPE_BASE = 'attrValType'
ATTR_VAL_BASE = 'attrVal'
ATTR_ID_EX = 'attrId%d'
ATTR_VAL_TYPE_EX = 'attrValType%d'
ATTR_VAL_EX = 'attrVal%d'
ATTR_GROUP_ID = 'attrGroupId'
ATTR_GROUP_VAL_TYPE = 'attrGroupValType'
ATTR_GROUP_VAL = 'attrGroupVal'
ATTR_GROUP_ID_2 = 'attrGroupId2'
ATTR_GROUP_VAL_TYPE_2 = 'attrGroupValType2'
ATTR_GROUP_VAL_2 = 'attrGroupVal2'

class PSkillInfo(SkillDataBase):

    def __init__(self, num, lv, pData = None):
        super(PSkillInfo, self).__init__(num, lv)
        if utils.isMonsterPSkill(num):
            lv = const.MONSTER_PSKILL_LV
        key = (num, lv)
        self.skillId = num
        self.skillData = PD.data.get(key, {})
        self.templateData = PSTD.data.get(num, {})
        if key not in PD.data:
            raise Exception('pskill data not found! pskillId:' + str(self.num) + ', sillLv: ' + str(self.lv))
        if pData is None:
            self.pData = {}
        else:
            self.pData = pData

    def getSkillData(self, key, default = 0):
        if self.pData.has_key(key):
            return self.pData[key]
        if self.templateData.has_key(key):
            return self.templateData.get(key)
        skillData = self.skillData.get(key, default)
        if BigWorld.component in ('client',) and not BigWorld.isPublishedVersion():
            if key == 'mainEff':
                skillData = '' if not skillData else skillData
                skillData = gameStrings.SKILL_TIPS_ID % self.skillId + '\n' + skillData
        return skillData

    def hasSkillData(self, key):
        return self.pData.has_key(key) or self.templateData.has_key(key) or self.skillData.has_key(key)

    def getAllAffectedEffect(self):
        res = []
        for idx in xrange(MIN_STATE_ATTR_SEQ, MAX_STATE_ATTR_SEQ + 1):
            if idx == MIN_STATE_ATTR_SEQ:
                attrIdKey = ATTR_ID_BASE
                attrValTypeKey = ATTR_VAL_TYPE_BASE
                attrValKey = ATTR_VAL_BASE
            else:
                attrIdKey = ATTR_ID_EX % idx
                attrValTypeKey = ATTR_VAL_TYPE_EX % idx
                attrValKey = ATTR_VAL_EX % idx
            if self.hasSkillData(attrIdKey):
                attrId = self.getSkillData(attrIdKey)
                attrValType = self.getSkillData(attrValTypeKey)
                attrVal = self.getSkillData(attrValKey)
                res.append((attrId, attrValType, attrVal))

        if self.hasSkillData(ATTR_GROUP_ID):
            attrGroupId = self.getSkillData(ATTR_GROUP_ID)
            attrGroupValType = self.getSkillData(ATTR_GROUP_VAL_TYPE)
            attrGroupVal = self.getSkillData(ATTR_GROUP_VAL)
            attrs = SGIID.data.get(attrGroupId, None)
            if attrs:
                for attrId in attrs:
                    res.append((attrId, attrGroupValType, attrGroupVal))

        if self.hasSkillData(ATTR_GROUP_ID_2):
            attrGroupId2 = self.getSkillData(ATTR_GROUP_ID_2)
            attrGroupValType2 = self.getSkillData(ATTR_GROUP_VAL_TYPE_2)
            attrGroupVal2 = self.getSkillData(ATTR_GROUP_VAL_2)
            attrs = SGIID.data.get(attrGroupId2, None)
            if attrs:
                for attrId in attrs:
                    res.append((attrId, attrGroupValType2, attrGroupVal2))

        return res


ATTR_ID = 'attrId'
ATTR_VALUE_TYPE = 'attrValueType'
ATTR_FST_VALUE = 'attrFstValue'
ATTR_CONTI_VALUE = 'attrContiValue'
ATTR_ID_2 = 'attrId2'
ATTR_VALUE_TYPE_2 = 'attrValueType2'
ATTR_FST_VALUE_2 = 'attrFstValue2'
ATTR_CONTI_VALUE_2 = 'attrContiValue2'
ATTR_ID_3 = 'attrId3'
ATTR_VALUE_TYPE_3 = 'attrValueType3'
ATTR_FST_VALUE_3 = 'attrFstValue3'
ATTR_CONTI_VALUE_3 = 'attrContiValue3'
ATTR_ID_4 = 'attrId4'
ATTR_VALUE_TYPE_4 = 'attrValueType4'
ATTR_FST_VALUE_4 = 'attrFstValue4'
ATTR_CONTI_VALUE_4 = 'attrContiValue4'
ATTR_ID_5 = 'attrId5'
ATTR_VALUE_TYPE_5 = 'attrValueType5'
ATTR_FST_VALUE_5 = 'attrFstValue5'
ATTR_CONTI_VALUE_5 = 'attrContiValue5'
ATTR_ID_6 = 'attrId6'
ATTR_VALUE_TYPE_6 = 'attrValueType6'
ATTR_FST_VALUE_6 = 'attrFstValue6'
ATTR_CONTI_VALUE_6 = 'attrContiValue6'
ATTR_ID_7 = 'attrId7'
ATTR_VALUE_TYPE_7 = 'attrValueType7'
ATTR_FST_VALUE_7 = 'attrFstValue7'
ATTR_CONTI_VALUE_7 = 'attrContiValue7'
GROUP_ID = 'groupId'
GROUP_VALUE_TYPE = 'groupValueType'
GROUP_FST_VALUE = 'groupFstValue'
GROUP_CONTI_VALUE = 'groupContiValue'
GROUP_ID_2 = 'groupId2'
GROUP_VALUE_TYPE_2 = 'groupValueType2'
GROUP_FST_VALUE_2 = 'groupFstValue2'
GROUP_CONTI_VALUE_2 = 'groupContiValue2'
GROUP_CE_VALC_FIELDS = (GROUP_FST_VALUE,
 GROUP_CONTI_VALUE,
 GROUP_FST_VALUE_2,
 GROUP_CONTI_VALUE_2)
MIN_STATE_ATTR_SEQ = 1
MAX_STATE_ATTR_SEQ = 7
STATE_ATTR_ID_FIELD_SUB_IDX = 0
STATE_ATTR_CALC_TYPE_FIELD_SUB_IDX = 1
STATE_ATTR_FST_VALUE_FIELD_SUB_IDX = 2
STATE_ATTR_CONTI_VALUE_FIELD_SUB_IDX = 3
STATE_ATTR_POWER_FIELD_SUB_IDX = 4
STATE_ATTR_REF_PROP_FIELD_SUB_IDX = 5
STATE_ATTR_REF_PROP_FORMULA_FIELD_SUB_IDX = 6
STATE_ATTR_REF_PROP_TGT_FIELD_SUB_IDX = 7
STATE_ATTR_FIELD_MAP = {}
for i in xrange(MIN_STATE_ATTR_SEQ, MAX_STATE_ATTR_SEQ + 1):
    if i == 1:
        STATE_ATTR_FIELD_MAP[i] = ('attrId', 'attrCalcType', 'attrFstValue', 'attrContiValue', 'attrPower', 'attrRefPropIds', 'attrRefPropFormulaId', 'attrRefTgt')
    else:
        args = (i,)
        STATE_ATTR_FIELD_MAP[i] = ('attrId%d' % args,
         'attrCalcType%d' % args,
         'attrFstValue%d' % args,
         'attrContiValue%d' % args,
         'attrPower%d' % args,
         'attrRefPropIds%d' % args,
         'attrRefPropFormulaId%d' % args,
         'attrRefTgt%d' % args)

def getStateSingleField(idx, fieldId):
    try:
        fields = STATE_ATTR_FIELD_MAP[idx]
        return fields[fieldId]
    except:
        return ''


def getStateFields(idx, fieldIdxes):
    try:
        fields = STATE_ATTR_FIELD_MAP[idx]
        ret = []
        for i in fieldIdxes:
            ret.append(fields[i])

        return ret
    except:
        return [''] * len(fieldIdxes)


class StateInfo(object):
    STATE_ID_BASE = 30000
    LV_DEPENDENT_ATTR_LIST = SD.data.get(const.LV_DEPENDENT_ATTR_ID, [])
    LV_DEPENDENT_ATTR_DICT = dict(zip(LV_DEPENDENT_ATTR_LIST, [1] * len(LV_DEPENDENT_ATTR_LIST))) if len(LV_DEPENDENT_ATTR_LIST) > 0 else {}
    DATA_TYPE = const.STATE_INFO

    def __init__(self, num, lv, hijackData = {}):
        super(StateInfo, self).__init__()
        if num < self.STATE_ID_BASE:
            raise Exception('state id invalid! %d' % num)
        self.num = num
        self.lv = limit(lv, 1, const.MAX_SKILL_LEVEL)
        self.layer = 1
        self.stateData = SD.data.get(num, {})
        if not self.stateData:
            raise Exception('state data not found! stateId:' + str(self.num) + '. stateLv: ' + str(self.lv))
        if hijackData:
            self.hijackData = copy.copy(hijackData)
        else:
            self.hijackData = {}

    def getStateData(self, key, default = 0):
        if self.hijackData.has_key(key):
            return self.hijackData[key]
        if key in self.LV_DEPENDENT_ATTR_DICT:
            try:
                d = self.stateData.get(key, default)
                if type(d) in const.TYPE_TUPLE_AND_LIST and len(d) == const.MAX_SKILL_LEVEL:
                    return d[self.lv - 1]
                return d
            except (TypeError, KeyError, IndexError):
                return default

        return self.stateData.get(key, default)

    def hasStateData(self, key):
        return self.stateData.has_key(key) or self.hijackData.has_key(key)

    def setHijackData(self, key, val):
        self.hijackData[key] = val

    def updateHiackData(self, data):
        self.hijackData.update(data)

    def getAllAffectedEffect(self):
        res = []
        if self.hasStateData(ATTR_ID):
            attrId = self.getStateData(ATTR_ID)
            attrValueType = self.getStateData(ATTR_VALUE_TYPE, 0)
            attrFstValue = self.getStateData(ATTR_FST_VALUE, 0)
            attrContiValue = self.getStateData(ATTR_CONTI_VALUE, 0)
            res.append((attrId,
             attrValueType,
             attrFstValue,
             attrContiValue))
        if self.hasStateData(ATTR_ID_2):
            attrId2 = self.getStateData(ATTR_ID_2)
            attrValueType2 = self.getStateData(ATTR_VALUE_TYPE_2, 0)
            attrFstValue2 = self.getStateData(ATTR_FST_VALUE_2, 0)
            attrContiValue2 = self.getStateData(ATTR_CONTI_VALUE_2, 0)
            res.append((attrId2,
             attrValueType2,
             attrFstValue2,
             attrContiValue2))
        if self.hasStateData(ATTR_ID_3):
            attrId3 = self.getStateData(ATTR_ID_3)
            attrValueType3 = self.getStateData(ATTR_VALUE_TYPE_3, 0)
            attrFstValue3 = self.getStateData(ATTR_FST_VALUE_3, 0)
            attrContiValue3 = self.getStateData(ATTR_CONTI_VALUE_3, 0)
            res.append((attrId3,
             attrValueType3,
             attrFstValue3,
             attrContiValue3))
        if self.hasStateData(ATTR_ID_4):
            attrId4 = self.getStateData(ATTR_ID_4)
            attrValueType4 = self.getStateData(ATTR_VALUE_TYPE_4, 0)
            attrFstValue4 = self.getStateData(ATTR_FST_VALUE_4, 0)
            attrContiValue4 = self.getStateData(ATTR_CONTI_VALUE_4, 0)
            res.append((attrId4,
             attrValueType4,
             attrFstValue4,
             attrContiValue4))
        if self.hasStateData(ATTR_ID_5):
            attrId5 = self.getStateData(ATTR_ID_5)
            attrValueType5 = self.getStateData(ATTR_VALUE_TYPE_5, 0)
            attrFstValue5 = self.getStateData(ATTR_FST_VALUE_5, 0)
            attrContiValue5 = self.getStateData(ATTR_CONTI_VALUE_5, 0)
            res.append((attrId5,
             attrValueType5,
             attrFstValue5,
             attrContiValue5))
        if self.hasStateData(ATTR_ID_6):
            attrId6 = self.getStateData(ATTR_ID_6)
            attrValueType6 = self.getStateData(ATTR_VALUE_TYPE_6, 0)
            attrFstValue6 = self.getStateData(ATTR_FST_VALUE_6, 0)
            attrContiValue6 = self.getStateData(ATTR_CONTI_VALUE_6, 0)
            res.append((attrId6,
             attrValueType6,
             attrFstValue6,
             attrContiValue6))
        if self.hasStateData(ATTR_ID_7):
            attrId7 = self.getStateData(ATTR_ID_7)
            attrValueType7 = self.getStateData(ATTR_VALUE_TYPE_7, 0)
            attrFstValue7 = self.getStateData(ATTR_FST_VALUE_7, 0)
            attrContiValue7 = self.getStateData(ATTR_CONTI_VALUE_7, 0)
            res.append((attrId7,
             attrValueType7,
             attrFstValue7,
             attrContiValue7))
        if self.hasStateData(GROUP_ID):
            groupId = self.getStateData(GROUP_ID)
            groupValueType = self.getStateData(GROUP_VALUE_TYPE)
            groupFstValue = self.getStateData(GROUP_FST_VALUE)
            groupContiValue = self.getStateData(GROUP_CONTI_VALUE)
            group = SGIID.data.get(groupId)
            if group is not None:
                for attrId in group:
                    res.append((attrId,
                     groupValueType,
                     groupFstValue,
                     groupContiValue))

        if self.hasStateData(GROUP_ID_2):
            groupId2 = self.getStateData(GROUP_ID_2)
            groupValueType2 = self.getStateData(GROUP_VALUE_TYPE_2)
            groupFstValue2 = self.getStateData(GROUP_FST_VALUE_2)
            groupContiValue2 = self.getStateData(GROUP_CONTI_VALUE_2)
            group = SGIID.data.get(groupId2)
            if group is not None:
                for attrId in group:
                    res.append((attrId,
                     groupValueType2,
                     groupFstValue2,
                     groupContiValue2))

        return res

    def getInfoByAttrId(self, attrId):
        if self.getStateData(ATTR_ID) == attrId:
            attrValueType = self.getStateData(ATTR_VALUE_TYPE, 0)
            attrFstValue = self.getStateData(ATTR_FST_VALUE, 0)
            attrContiValue = self.getStateData(ATTR_CONTI_VALUE, 0)
            return (attrValueType, attrFstValue, attrContiValue)
        if self.getStateData(ATTR_ID_2) == attrId:
            attrValueType = self.getStateData(ATTR_VALUE_TYPE_2, 0)
            attrFstValue = self.getStateData(ATTR_FST_VALUE_2, 0)
            attrContiValue = self.getStateData(ATTR_CONTI_VALUE_2, 0)
            return (attrValueType, attrFstValue, attrContiValue)
        if self.getStateData(ATTR_ID_3) == attrId:
            attrValueType = self.getStateData(ATTR_VALUE_TYPE_3, 0)
            attrFstValue = self.getStateData(ATTR_FST_VALUE_3, 0)
            attrContiValue = self.getStateData(ATTR_CONTI_VALUE_3, 0)
            return (attrValueType, attrFstValue, attrContiValue)
        if self.getStateData(ATTR_ID_4) == attrId:
            attrValueType = self.getStateData(ATTR_VALUE_TYPE_4, 0)
            attrFstValue = self.getStateData(ATTR_FST_VALUE_4, 0)
            attrContiValue = self.getStateData(ATTR_CONTI_VALUE_4, 0)
            return (attrValueType, attrFstValue, attrContiValue)
        if self.getStateData(ATTR_ID_5) == attrId:
            attrValueType = self.getStateData(ATTR_VALUE_TYPE_5, 0)
            attrFstValue = self.getStateData(ATTR_FST_VALUE_5, 0)
            attrContiValue = self.getStateData(ATTR_CONTI_VALUE_5, 0)
            return (attrValueType, attrFstValue, attrContiValue)
        if self.getStateData(ATTR_ID_6) == attrId:
            attrValueType = self.getStateData(ATTR_VALUE_TYPE_6, 0)
            attrFstValue = self.getStateData(ATTR_FST_VALUE_6, 0)
            attrContiValue = self.getStateData(ATTR_CONTI_VALUE_6, 0)
            return (attrValueType, attrFstValue, attrContiValue)
        if self.getStateData(ATTR_ID_7) == attrId:
            attrValueType = self.getStateData(ATTR_VALUE_TYPE_7, 0)
            attrFstValue = self.getStateData(ATTR_FST_VALUE_7, 0)
            attrContiValue = self.getStateData(ATTR_CONTI_VALUE_7, 0)
            return (attrValueType, attrFstValue, attrContiValue)
        groupId = self.getStateData(GROUP_ID)
        if groupId:
            group = SGIID.data.get(groupId)
            if group is not None:
                for attrId in group:
                    groupValueType = self.getStateData(GROUP_VALUE_TYPE)
                    groupFstValue = self.getStateData(GROUP_FST_VALUE)
                    groupContiValue = self.getStateData(GROUP_CONTI_VALUE)
                    return (groupValueType, groupFstValue, groupContiValue)

        else:
            groupId2 = self.getStateData(GROUP_ID_2)
            if groupId2:
                group = SGIID.data.get(groupId2)
                if group is not None:
                    for attrId in group:
                        groupValueType = self.getStateData(GROUP_VALUE_TYPE_2)
                        groupFstValue = self.getStateData(GROUP_FST_VALUE_2)
                        groupContiValue = self.getStateData(GROUP_CONTI_VALUE_2)
                        return (groupValueType, groupFstValue, groupContiValue)

    def getStateCalcType(self):
        dmgType = self.getStateData('dotDmgType', gametypes.SKILL_EFFECT_PHYSICS)
        if dmgType == gametypes.SKILL_EFFECT_PHYSICS:
            return gametypes.DMGTYPE_HP_STATE_PHYSICS
        if dmgType == gametypes.SKILL_EFFECT_MAGIC:
            return gametypes.DMGTYPE_HP_STATE_MAGIC
        if dmgType == gametypes.SKILL_EFFECT_OTHER:
            return gametypes.DMGTYPE_HP_STATE_SELF

    def iterAllAttrIndex(self):
        for i in xrange(1, const.STATE_INFO_ATTR_NUM_MAX + 1):
            yield i

    def getAttrIndexMap(self):
        ret = {}
        for i in self.iterAllAttrIndex():
            attrName = self.getColName('attrId', i)
            attrId = self.getStateData(attrName, 0)
            if attrId:
                ret[attrId] = i
            else:
                break

        return ret

    def getColName(self, preStr, index):
        if index == 1:
            return preStr
        else:
            return preStr + str(index)


STATE_1 = 'state1'
STATE_TRIGGER_RATE_1 = 'stateTriggerRate1'
STATE_CONTROL_LV_1 = 'stateControlLv1'
STATE_TIME_1 = 'stateTime1'
STATE_2 = 'state2'
STATE_TRIGGER_RATE_2 = 'stateTriggerRate2'
STATE_CONTROL_LV_2 = 'stateControlLv2'
STATE_TIME_2 = 'stateTime2'
STATE_3 = 'state3'
STATE_TRIGGER_RATE_3 = 'stateTriggerRate3'
STATE_CONTROL_LV_3 = 'stateControlLv3'
STATE_TIME_3 = 'stateTime3'
STATE_4 = 'state4'
STATE_TRIGGER_RATE_4 = 'stateTriggerRate4'
STATE_CONTROL_LV_4 = 'stateControlLv4'
STATE_TIME_4 = 'stateTime4'
AREA_ARG_1 = 'areaArg1'
AREA_ARG_2 = 'areaArg2'
AREA_ARG_3 = 'areaArg3'
AREA_ARG_4 = 'areaArg4'
TYPE = 'type'
HURT_TYPE = 'hurtType'

class SkillEffectInfo(object):
    DATA_TYPE = const.SKILL_EFFECT_INFO
    LV_DEPENDENT_ATTR_LIST = SEFFD.data.get(const.LV_DEPENDENT_ATTR_ID, [])
    LV_DEPENDENT_ATTR_DICT = dict(zip(LV_DEPENDENT_ATTR_LIST, [1] * len(LV_DEPENDENT_ATTR_LIST))) if len(LV_DEPENDENT_ATTR_LIST) > 0 else {}

    def __init__(self, num, lv):
        super(SkillEffectInfo, self).__init__()
        self.num = num
        self.lv = lv
        self.skillEffectData = SEFFD.data.get(self.num)
        if self.skillEffectData == None:
            raise Exception('SkillEffectInfo is None, skillId:%d lv:%d' % (self.num, self.lv))
        self.hijackData = {}
        self.tgtHijackData = {}
        self.tgtHijackDataCache = {}

    def getSkillEffectData(self, key, default = 0):
        if self.tgtHijackData.has_key(key):
            return self.tgtHijackData[key]
        if self.hijackData.has_key(key):
            return self.hijackData[key]
        if key in self.LV_DEPENDENT_ATTR_DICT:
            try:
                return self.skillEffectData[key][self.lv - 1]
            except (TypeError, KeyError, IndexError):
                return default

        return self.skillEffectData.get(key, default)

    def hasSkillEffectData(self, key):
        if self.skillEffectData.has_key(key) or self.hijackData.has_key(key) or self.tgtHijackData.has_key(key):
            return True
        return False

    def evalSkillEffectData(self, key, default = 0):
        data = self.skillEffectData.get(key, None)
        if data == None:
            return default
        return formula.evalScript(self.lv, data)

    def setHijackData(self, key, val):
        self.hijackData[key] = val

    def updateHijackData(self, data):
        self.hijackData.update(data)

    def pskillAffectDataByTgt(self, pskillAffectDataByTgtRes):
        self.pskillAffectDataByTgtRes = pskillAffectDataByTgtRes

    def calcTgtHijackData(self, tgt):
        if not hasattr(self, 'pskillAffectDataByTgtRes') or not self.pskillAffectDataByTgtRes:
            return
        if not tgt.IsCombatUnit or tgt.IsNaiveCombatUnit:
            return
        self.tgtHijackData = {}
        pskillKeys = []
        for pskillNum, (tgtConditions, affectData) in self.pskillAffectDataByTgtRes.iteritems():
            if commcalc.pskillPreConditionCheckCommon(tgt, tgtConditions, isSrc=False):
                pskillKeys.append(pskillNum)

        if not pskillKeys:
            return
        cacheKeys = ','.join([ str(psk) for psk in pskillKeys ])
        if cacheKeys in self.tgtHijackDataCache:
            self.tgtHijackData = self.tgtHijackDataCache[cacheKeys]
            return
        self.tgtHijackData = {}
        allEffects = []
        for key in pskillKeys:
            _, effects = self.pskillAffectDataByTgtRes[key]
            allEffects.extend(effects)

        self.tgtHijackData = commcalc.calcHijackData(self, allEffects)
        self.tgtHijackDataCache[cacheKeys] = self.tgtHijackData

    def getStateEffects(self):
        res = []
        state1 = self.getSkillEffectData(STATE_1)
        if state1:
            triggerRate1 = self.getSkillEffectData(STATE_TRIGGER_RATE_1, 0)
            controlLv1 = self.getSkillEffectData(STATE_CONTROL_LV_1)
            time1 = self.getSkillEffectData(STATE_TIME_1, 0)
            res.append((state1,
             triggerRate1,
             controlLv1,
             time1))
        state2 = self.getSkillEffectData(STATE_2)
        if state2:
            triggerRate2 = self.getSkillEffectData(STATE_TRIGGER_RATE_2, 0)
            controlLv2 = self.getSkillEffectData(STATE_CONTROL_LV_2)
            time2 = self.getSkillEffectData(STATE_TIME_2, 0)
            res.append((state2,
             triggerRate2,
             controlLv2,
             time2))
        state3 = self.getSkillEffectData(STATE_3)
        if state3:
            triggerRate3 = self.getSkillEffectData(STATE_TRIGGER_RATE_3, 0)
            controlLv3 = self.getSkillEffectData(STATE_CONTROL_LV_3)
            time3 = self.getSkillEffectData(STATE_TIME_3, 0)
            res.append((state3,
             triggerRate3,
             controlLv3,
             time3))
        state4 = self.getSkillEffectData(STATE_4)
        if state4:
            triggerRate4 = self.getSkillEffectData(STATE_TRIGGER_RATE_4, 0)
            controlLv4 = self.getSkillEffectData(STATE_CONTROL_LV_4)
            time4 = self.getSkillEffectData(STATE_TIME_4, 0)
            res.append((state4,
             triggerRate4,
             controlLv4,
             time4))
        return res

    def getAreaParam(self):
        areaArg1 = self.getSkillEffectData(AREA_ARG_1, 0)
        areaArg2 = self.getSkillEffectData(AREA_ARG_2, 0)
        areaArg3 = self.getSkillEffectData(AREA_ARG_3, 0)
        areaArg4 = self.getSkillEffectData(AREA_ARG_4, 5)
        return (areaArg1,
         areaArg2,
         areaArg3,
         areaArg4)

    def getRealSkillEffectType(self, attacker, default = gametypes.SKILL_EFFECT_PHYSICS):
        effectType = self.getSkillEffectData(TYPE, default)
        if effectType != gametypes.SKILL_EFFECT_MAX_PHYSICS_MAGIC:
            return effectType
        if attacker.atk[1] > attacker.atk[3]:
            return gametypes.SKILL_EFFECT_PHYSICS
        return gametypes.SKILL_EFFECT_MAGIC

    def getSkillEffectCalcType(self, hurtType = -1, forceEffectType = None):
        effectType = forceEffectType if forceEffectType else self.getSkillEffectData(TYPE)
        if hurtType == -1:
            hurtType = self.getSkillEffectData(HURT_TYPE)
        if hurtType == gametypes.SKILL_HURT_REDUCE_HP:
            if effectType == gametypes.SKILL_EFFECT_PHYSICS:
                return gametypes.DMGTYPE_HP_WEAPON_SKILL
            if effectType == gametypes.SKILL_EFFECT_MAGIC:
                return gametypes.DMGTYPE_HP_MAGIC_SKILL
            if effectType == gametypes.SKILL_EFFECT_OTHER:
                return gametypes.DMGTYPE_HP_SELF_SKILL
            if effectType == gametypes.SKILL_EFFECT_NORMAL_ATTCT_BF_DOTA:
                return gametypes.DMGTYPE_HP_NORMAL_ATTACK_BF_DOTA
        else:
            if hurtType == gametypes.SKILL_HURT_ADD_HP:
                return gametypes.HEALTYPE_HP_SKILL
            if hurtType == gametypes.SKILL_HURT_REDUCE_MP:
                return gametypes.DMGTYPE_MP_SKILL
            if hurtType == gametypes.SKILL_HURT_ADD_MP:
                return gametypes.HEALTYPE_MP_SKILL
            if hurtType == gametypes.SKILL_HURT_REDUCE_EP:
                return gametypes.DMGTYPE_EP_SKILL
            if hurtType == gametypes.SKILL_HURT_ADD_EP:
                return gametypes.HEALTYPE_EP_SKILL
            if hurtType == gametypes.SKILL_HURT_ADD_LABOUR:
                return gametypes.HEALTYPE_LABOUR_SKILL
            if hurtType == gametypes.SKILL_HURT_REDUCE_LABOUR:
                return gametypes.DMGTYPE_LABOUR_SKILL

    def isHealTypeEffect(self):
        hurtType = self.getSkillEffectData(HURT_TYPE)
        return hurtType == gametypes.SKILL_HURT_ADD_HP


class PSkill(UserSoleType):

    def __init__(self, id, lv, name):
        super(PSkill, self).__init__()
        self.id = id
        self.level = lv
        self.name = name
        self.enable = True
        self.nextTriggerTime = 0
        self.triggerInvalidTime = 0


class DictZipper(object):

    def __init__(self, *data):
        self.data = data

    def __len__(self):
        return sum([ len(d) for d in self.data ])

    def __getitem__(self, key):
        for d in self.data:
            try:
                return d[key]
            except KeyError:
                pass

        raise KeyError()

    def get(self, key, default = None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def items(self):
        res = []
        for d in self.data:
            res.extend([ (key, value) for key, value in d.iteritems() ])

        return res

    def has_key(self, key):
        return any((True for d in self.data if key in d))

    def keys(self):
        res = []
        for d in self.data:
            res.extend([ key for key in d.iterkeys() ])

        return res

    def values(self):
        res = []
        for d in self.data:
            res.extend([ value for value in d.itervalues() ])

        return res

    def iteritems(self):
        raise NotImplementedError()

    def iterkeys(self):
        raise NotImplementedError()

    def itervalues(self):
        raise NotImplementedError()

    def add(self, d):
        self.data.append(d)


class ItemList(UserListType):

    def _lateReload(self):
        super(ItemList, self)._lateReload()
        for v in self:
            v and v.reloadScript()


class SkillQteInfoVal(UserSoleType):

    def __init__(self, srcSkillId, interval, lastTime, triggerTime, qteSkills):
        self.srcSkillId = srcSkillId
        self.interval = interval
        self.lastTime = lastTime
        self.triggerTime = triggerTime
        self.qteSkills = copy.copy(qteSkills)
        self.timerId = 0

    def canUseQteSkill(self):
        return time.time() - self.triggerTime > self.interval

    def resetAll(self):
        self.interval = 0
        self.lastTime = 0
        self.triggerTime = 0
        self.qteSkills = []


class SkillQteDict(UserDictType):

    def _lateReload(self):
        super(SkillQteDict, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()


class ClientMallVal(object):

    def __init__(self, nDay = 0, nWeek = 0, nTotal = 0, tLast = 0, nMonth = 0):
        self.nDay = nDay
        self.nWeek = nWeek
        self.nTotal = nTotal
        self.nMonth = nMonth
        self.tLast = tLast
