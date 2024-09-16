#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client/skillDataInfo.o
from gamestrings import gameStrings
import random
import time
import copy
import BigWorld
import const
import utils
import gametypes
import gameglobal
import gamelog
import formula
from gameclass import SkillDataBase
from sfx import flyEffect
from helpers import tintalt
from skillEnhanceCommon import SkillEnhanceCommon
from callbackHelper import Functor
from gamestrings import gameStrings
from data import skill_client_data as SD
from data import state_client_data as SCD
from data import skill_general_data as SGD
from data import skill_general_template_data as SGTD
from data import skill_state_client_data as SSCD
from data import item_data as ID
from data import equip_data as ED
from data import weapon_client_data as WCD
from data import state_data as STD
from data import monster_model_client_data as MMCD
from data import tint_client_data as TCD
from data import skill_tips_desc_data as STDD
from data import skill_tips_value_data as STVD
from data import sys_config_data as SCFD
from data import zaiju_data as ZD
from data import skill_appearance_detail_data as SADD
from data import skill_state_apprearance_data as SSAD
from data import state_client_appearance_data as SCAD
from cdata import game_msg_def_data as GMDD
from data import summon_sprite_skill_data as SSSD
SPECIAL_EFFECT_SKILL_CD_DECREASE_TYPE_ALL = 0

class ClientSkillTips(SkillDataBase):

    def __init__(self, num, lv = 1):
        super(ClientSkillTips, self).__init__(num, lv)
        self.skillId = num
        self.skillData = STDD.data.get((num, lv), {})
        self.skillValueData = STVD.data.get((num, lv), {})
        if not self.skillData:
            self.skillData = STDD.data.get((num, 1), {})
        elif lv != 1:
            lv1dataTmp = copy.deepcopy(STDD.data.get((num, 1), {}))
            skillData = STDD.data.get((num, lv), {})
            if skillData:
                for key in skillData:
                    lv1dataTmp[key] = skillData[key]

            self.skillData = lv1dataTmp
        if not self.skillData:
            raise Exception('skillTips data not found! skillId: ' + str(self.num) + '. skillLv: ' + str(self.lv))

    def getSkillData(self, key, default = 0):
        skillTipsDesc = self.skillData.get(key, None)
        if not skillTipsDesc:
            skillTips = default
        elif not self.skillValueData:
            skillTips = skillTipsDesc
        else:
            skillTipsValue = self.skillValueData.get(key, None)
            if not skillTipsValue:
                skillTips = skillTipsDesc
            else:
                skillTipsValue = list(skillTipsValue.split(','))
                skillTipsValue = tuple(skillTipsValue[0:len(skillTipsValue) - 1])
                skillTips = skillTipsDesc % skillTipsValue
        if skillTips:
            skillTips = skillTips.replace('%%', '%')
        if not BigWorld.isPublishedVersion():
            if key == 'mainEff' or key == 'shortMainEff':
                showSkillId = self.skillId
                skillTips = '' if not skillTips else skillTips
                for realSpriteId, spriteSkillData in SSSD.data.iteritems():
                    if spriteSkillData.get('virtualSkill', 0) == self.skillId:
                        showSkillId = realSpriteId
                        break

                skillTips = gameStrings.SKILL_TIPS_ID % showSkillId + '\n' + skillTips
        return skillTips


class ClientSkillInfo(SkillDataBase):

    def __init__(self, num, lv = 1, type = 0, stateId = 0):
        if utils.isMonsterSkill(num):
            lv = const.MONSTER_SKILL_LV
        super(ClientSkillInfo, self).__init__(num, lv)
        self.type = type
        if type == 0:
            self.skillData = copy.copy(SD.data.get((num, lv), {}))
            if not self.skillData:
                self.skillData = copy.copy(SD.data.get((num, 1), {}))
            else:
                lv1data = SD.data.get((num, 1), {})
                if lv1data:
                    if len(lv1data) != len(self.skillData):
                        for key, value in lv1data.items():
                            if not self.skillData.has_key(key):
                                self.skillData[key] = value

        elif type == 1:
            self.skillData = SCD.data.get(num, {})
        elif type == 2:
            self.skillData = SGD.data.get((num, lv), {})
        if type == 3:
            self.skillData = SSCD.data.get((num, stateId), {})
            if isinstance(self.skillData, tuple) or isinstance(self.skillData, list):
                for item in self.skillData:
                    if lv >= item['lvStart'] and lv <= item['lvEnd']:
                        self.skillData = item
                        break

        if not self.skillData and num:
            raise Exception('skill data not found! skillId: ' + str(self.num) + '. skillLv: ' + str(self.lv))

    def getSkillData(self, key, default = 0):
        if self.type == 2:
            sgTemplateData = SGTD.data.get(self.num, {})
            if sgTemplateData.has_key(key):
                return sgTemplateData.get(key)
        return self.skillData.get(key, default)

    def hasSkillData(self, key):
        templateHasKey = False
        if self.type == 2:
            sgTemplateData = SGTD.data.get(self.num, {})
            templateHasKey = sgTemplateData.has_key(key)
        return self.skillData.has_key(key) or templateHasKey


class AppearanceSkillInfo(SkillDataBase):
    SKILL_TYPE_GENERAL = 0
    SKILL_TYPE_BUFF = 1
    SKILL_TYPE_STATE = 2

    def __init__(self, skillId, appearanceId, type = SKILL_TYPE_GENERAL, state = -1):
        super(AppearanceSkillInfo, self).__init__(skillId, 0)
        self.appearanceId = appearanceId
        if type == self.SKILL_TYPE_GENERAL:
            self.skillData = copy.copy(SADD.data.get((skillId, appearanceId), {}))
        elif type == self.SKILL_TYPE_BUFF:
            self.skillData = copy.copy(SCAD.data.get((skillId, appearanceId), {}))
        elif type == self.SKILL_TYPE_STATE:
            if state == -1:
                self.skillData = copy.copy(SADD.data.get((skillId, appearanceId), {}))
            else:
                self.skillData = copy.copy(SSAD.data.get((skillId, state, appearanceId), {}))


def getBuffClientSkillInfo(stateId, owner):
    if not owner:
        return ClientSkillInfo(stateId, 1, 1)
    return getBuffAppearanceSkillInfo(owner, stateId)


subSkillMap = None

def _createSubSkillMap():
    global subSkillMap
    subSkillMap = {}


def getSubCount(skillId):
    if subSkillMap == None:
        _createSubSkillMap()
    return subSkillMap.get(skillId, 1)


def getSkillType(skillInfo):
    return skillInfo.getSkillData('skillType', 0)


def getMainEff(skillInfo):
    return skillInfo.getSkillData('mainEff', '')


def getDetailEff1(skillInfo):
    return skillInfo.getSkillData('detailEff1', '')


def getDetailEff2(skillInfo):
    return skillInfo.getSkillData('detailEff2', '')


def getDetailEff3(skillInfo):
    return skillInfo.getSkillData('detailEff3', '')


def getGraph1(skillInfo):
    return skillInfo.getSkillData('graph1')


def getGraph2(skillInfo):
    return skillInfo.getSkillData('graph2')


def getGraph3(skillInfo):
    return skillInfo.getSkillData('graph3')


def getGraph4(skillInfo):
    return skillInfo.getSkillData('graph4')


def getLearnLv(skillInfo):
    return skillInfo.getSkillData('learnLv')


def getLearnGold(skillInfo):
    return skillInfo.getSkillData('learnGold')


def getLearnPoint(skillInfo):
    return skillInfo.getSkillData('learnPoint')


def getSkillSch(skillId):
    return 1


def getSkillIspk(skillId, level):
    return 0


def getSkillLv(skillInfo):
    lv = skillInfo.getSkillData('lv', 0)
    if lv == 0:
        lv = getattr(skillInfo, 'lv', 0)
    return lv


def getCastTime(skillInfo):
    return skillInfo.getSkillData('castTime', 0)


def getSkillName(skillInfo):
    return skillInfo.getSkillData('name', 0)


def getWuShuang(skillInfo):
    return (skillInfo.getSkillData('wsAdd1', 0), skillInfo.getSkillData('wsAdd2', 0))


def getWuShuangMwsAdd(skillInfo):
    return skillInfo.getSkillData('mwsAdd', 0)


def getSkillDesc(skillInfo):
    return skillInfo.getSkillData('describe', '')


def getSkillDetails(skillInfo):
    return skillInfo.getSkillData('details', '')


def getEquipName(skillInfo):
    equipId = skillInfo.getSkillData('equipmentId', '')
    equipName = []
    if equipId != '':
        for item in equipId:
            equipName.append(ED.data.get(item, {}).get('name', ''))

    return equipName


def _getWeaponId(weapon):
    itemId = weapon
    if ED.data.has_key(itemId):
        return ED.data[itemId].get('subId', [0])[0]
    return 0


def _getWeaponList():
    p = BigWorld.player()
    weaponList = []
    weaponList.append(_getWeaponId(p.aspect.leftWeapon))
    weaponList.append(_getWeaponId(p.aspect.rightWeapon))
    return weaponList


def getWeaponName(skillInfo):
    weaponId = skillInfo.getSkillData('wpSkillType', [])
    weaponName = []
    weaponIdList = _getWeaponList()
    if weaponId != '':
        for item in weaponId:
            for element in WCD.data.get(item, []):
                if item in weaponIdList:
                    weaponName.append((element.get('name', ''), True))
                else:
                    weaponName.append((element.get('name', ''), False))

    return weaponName


def getWeaponTips(skillInfo):
    weaponId = skillInfo.getSkillData('wpSkillType', [])
    weaponTips = []
    weaponIdList = _getWeaponList()
    if weaponId != '':
        for item in weaponId:
            wcd = WCD.data.get(item, [])
            strTips = ''
            for element in wcd:
                strTips += element.get('tips', '')

            if item in weaponIdList:
                weaponTips.append((strTips, True))
            else:
                weaponTips.append((strTips, False))

    return weaponTips


def getPropName(skillInfo):
    propId = skillInfo.getSkillData('propId', '')
    propName = []
    if propId != '':
        for item in propId:
            propName.append(ID.data.get(item, {}).get('name', ''))

    return propName


def _checkSelfBuffer(bufferId):
    if len(_getBufferList()) > 0 and bufferId in _getBufferList():
        return True
    else:
        return False


def getSelfBufferName(skillInfo):
    selfBufferId = skillInfo.getSkillData('selfStates', '')
    selfBufferName = []
    if selfBufferId != '':
        for item in selfBufferId:
            bufferName = STD.data.get(item, None)
            if bufferName:
                selfBufferName.append((bufferName.get('name', ''), _checkSelfBuffer(item)))

    return selfBufferName


def getTgtBufferName(skillInfo):
    tgtBufferId = skillInfo.getSkillData('tgtStates', '')
    tgtBufferName = []
    if tgtBufferId != '':
        for item in tgtBufferId:
            tgtBufferName.append(STD.data.get(item, {}).get('name', ''))

    return tgtBufferName


def _getBufferList():
    p = BigWorld.player()
    return p.getStates().keys()


def _checkSelfNoBuffer(bufferId):
    if len(_getBufferList()) > 0 and bufferId in _getBufferList():
        return False
    else:
        return True


def getSelfNoBufferName(skillInfo):
    selfNoBufferId = skillInfo.getSkillData('selfNoStates', '')
    selfNoBufferName = []
    if selfNoBufferId != '':
        for item in selfNoBufferId:
            bufferName = STD.data.get(item, None)
            if bufferName:
                selfNoBufferName.append((bufferName.get('name', ''), _checkSelfNoBuffer(item)))

    return selfNoBufferName


def getTgtNoBufferName(skillInfo):
    tgtNoBufferId = skillInfo.getSkillData('tgtNoStates', '')
    tgtNoBufferName = []
    if tgtNoBufferId != '':
        for item in tgtNoBufferId:
            tgtNoBufferName.append(STD.data.get(item, {}).get('name', ''))

    return tgtNoBufferName


def getSkillMpNeed(skillInfo):
    return skillInfo.getSkillData('mpNeed', 0)


def getSkillHpNeed(skillInfo):
    return skillInfo.getSkillData('hpNeed', 0)


def getCDTime(skillInfo):
    return skillInfo.getSkillData('cd', 0)


def getNotMoveTime(skillInfo):
    return skillInfo.getSkillData('notMoveTime', 0)


def getTargetCamp(skillInfo):
    return 1


def getTargetType(skillInfo):
    return 1


def getCastMoveType(skillInfo):
    return skillInfo.getSkillData('castMoveType')


def getSkillRange(skillInfo):
    rangeMin = skillInfo.getSkillData('rangeMin', 0)
    rangeMax = skillInfo.getSkillData('rangeMax', 0)
    if rangeMax:
        p = BigWorld.player()
        rangeMax = max(rangeMin, (rangeMax + p.skillAdd[2]) * (1 + p.skillAdd[3]))
    return (rangeMin, rangeMax)


def getData(id, level, attr, default = None):
    return default


def getFlyType(clientSkillInfo):
    return clientSkillInfo.getSkillData('flyType') % 10


def getSkillAreaRadius(skillInfo):
    clientSkillInfo = ClientSkillInfo(skillInfo.num, skillInfo.lv, 0)
    return clientSkillInfo.getSkillData('areaRadius', 6.0)


def getCurvature(clientSkillInfo):
    return clientSkillInfo.getSkillData('curvature', 1)


def getFlyZroll(clientSkillInfo):
    return clientSkillInfo.getSkillData('zroll', 0)


def getRotateFlySpeed(clientSkillInfo):
    return clientSkillInfo.getSkillData('rotateFlySpeed', (0, 0, 0))


def getFlySrcNode(clientSkillInfo):
    return clientSkillInfo.getSkillData('srcFlyNode')


def hideWeaponInFlyNode(clientSkillInfo):
    return clientSkillInfo.getSkillData('hideWeaponInFlyNode')


def getFlySrcNodeType(clientSkillInfo):
    return clientSkillInfo.getSkillData('srcFlyNodeType')


def getFlyEndNode(clientSkillInfo):
    return clientSkillInfo.getSkillData('tgtFlyNode')


def getSplitDamageData(clientSkillInfo):
    damTime = clientSkillInfo.getSkillData('damTime')
    damBL = clientSkillInfo.getSkillData('damBL')
    return (damTime, damBL)


def getNoNeedHit(clientSkillInfo):
    return clientSkillInfo.getSkillData('noNeedHit', 0)


def isNeedPlayClientEffect(clientSkillInfo):
    return clientSkillInfo.getSkillData('flyType') % 10


def isSuckerFlyer(clientSkillInfo):
    return clientSkillInfo.getSkillData('flyType') / 10


def getTintDataInfo(owner, tintId):
    if owner.tintIdMapTintName.has_key(tintId):
        tintName = owner.tintIdMapTintName[tintId][0]
        tintPrio = owner.tintIdMapTintName[tintId][1]
        tint = owner.tintIdMapTintName[tintId][2]
    else:
        tcd = TCD.data.get(tintId, {})
        tintType = tcd.get('mType', None)
        if tintType:
            tint = tintalt.getTintName(tintType)
        else:
            tint = ''
        tintPrio = tcd.get('mPrio', 1)
        tintSuffix = tcd.get('mParam', '')
        fresnelColor = tcd.get('fresnelColor', None)
        if fresnelColor:
            return (None, tintPrio, fresnelColor)
        tintName = tint + tintSuffix
    return (tintName, tintPrio, tint)


def getTintHitDataInfo(tintId):
    tcd = TCD.data.get(tintId, {})
    fresnelColor = tcd.get('fresnelColor', (1.0, 0.6, 0.0))
    return fresnelColor


_levelDescMap = {}

def getLevelString(power):
    return _levelDescMap.get(power, '')


def getRecoverTime(skillInfo, power, cdArg = 1.0):
    p = BigWorld.player()
    if skillInfo.num in p.combatSpeedIncreseWhiteList:
        cdArg = cdArg - getattr(p, 'combatSpeedIncreseRatio', (0.0, 0.0))[1]
    if p.inFubenType(const.FB_TYPE_BATTLE_FIELD_DOTA):
        if skillInfo.getSkillData('skillCategory') == const.SKILL_CATEGORY_BF_DOTA_NORMAL:
            cdArg /= 1 + getattr(p, 'bfDotaNormalAttackSpeedIncreseRatio', 0.0)
        elif skillInfo.getSkillData('skillForbidBeIncrease') == 0:
            cdArg = cdArg - getattr(p, 'bfDotaSkillAttackSpeedIncreseRatio', 0.0)
    if skillInfo.num not in getattr(p, 'skillAttackSpeedIncreseRatioBlackList') and (formula.spaceInFuben(p.spaceNo) or p.isOnWingWorldCarrier() or formula.spaceInChaosFlagsBattleField(p.spaceNo)) and getattr(p, 'skillAttackSpeedIncreseRatio', 0.0):
        cdArg = cdArg - getattr(p, 'skillAttackSpeedIncreseRatio', 0.0)
    cd = skillInfo.getSkillData('cd', 0) * cdArg
    skillCDDecrease = getattr(p, 'skillCDDecrease', None)
    if skillCDDecrease:
        sType, sVal = skillCDDecrease
        if sType == SPECIAL_EFFECT_SKILL_CD_DECREASE_TYPE_ALL or sType == skillInfo.getSkillData('skillCategory', 0) or sType == skillInfo.num:
            cd /= 1 + sVal
    return cd


def getCommonCoolDown(skillInfo, power, ccdArg = 1.0):
    p = BigWorld.player()
    if skillInfo.num in p.combatSpeedIncreseWhiteList:
        ccdArg = ccdArg - getattr(p, 'combatSpeedIncreseRatio', (0.0, 0.0))[1]
    if skillInfo.getSkillData('skillCategory') == const.SKILL_CATEGORY_BF_DOTA_NORMAL:
        ccdArg /= 1 + getattr(p, 'bfDotaNormalAttackSpeedIncreseRatio', 0.0)
    gcd = skillInfo.getSkillData('gcd', 0) * ccdArg
    gcd = max(0.0, (gcd - p.skillAdd[0]) * (1 - p.skillAdd[1]))
    return gcd


def isNeedTarget(skillInfo):
    if not skillInfo.hasSkillData('noTgt'):
        return True
    return False


def getCircleShape(skillInfo):
    return skillInfo.getSkillData('circleShape', None)


def getFlySpeed(skillInfo):
    return skillInfo.getSkillData('flySpeed', 20)


def getSpellTime(skillInfo):
    return skillInfo.getSkillData('spellTime', 0)


def isChargeSkill(skillInfo):
    return skillInfo.getSkillData('castType', 0) == gameglobal.CAST_TYPE_CHARGE


def isGuideSkill(skillInfo):
    return skillInfo.getSkillData('castType', 0) == gameglobal.CAST_TYPE_GUIDE


def isEnemySkill(skillInfo):
    skillTargetType, skillTargetValue = BigWorld.player().getSkillTargetType(skillInfo)
    return skillTargetType in (gametypes.SKILL_TARGET_ENERMY, gametypes.SKILL_TARGET_SELF_ENERMY, gametypes.SKILL_TARGET_ALL_TYPE)


def isFriendSkill(skillInfo):
    skillTargetType, skillTargetValue = BigWorld.player().getSkillTargetType(skillInfo)
    return skillTargetType in (gametypes.SKILL_TARGET_FRIEND, gametypes.SKILL_TARGET_SELF_FRIEND, gametypes.SKILL_TARGET_ALL_TYPE)


def getPreSpell(skillInfo):
    return skillInfo.getSkillData('preSpell', 0)


def getWsNeed(skillInfo):
    return (skillInfo.getSkillData('wsNeed1', 0), skillInfo.getSkillData('wsNeed2', 0))


def getWsStarLv(skillInfo):
    return skillInfo.getSkillData('wsStar', 0)


def needTarget(skillInfo):
    if skillInfo.hasSkillData('tgtEnemyType'):
        return True
    if skillInfo.hasSkillData('tgtFriendType'):
        return True
    if skillInfo.hasSkillData('tgtAllType'):
        return True
    if skillInfo.hasSkillData('tgtSelfEnemyType'):
        return True
    if skillInfo.hasSkillData('tgtSelfFriendType'):
        return True
    return False


def checkTargetRelationRequest(skillInfo, showMsg = True, needBlockMsg = False, checkSprite = False):
    p = BigWorld.player()
    skillTargetType, skillTargetValue = p.getSkillTargetType(skillInfo)
    if checkSprite:
        target = BigWorld.entities.get(p.summonedSpriteInWorld.targetId) if p.summonedSpriteInWorld else None
    else:
        target = p.targetLocked
    if skillTargetType == gametypes.SKILL_TARGET_SELF:
        if target == None:
            if not needBlockMsg:
                showMsg and p.showGameMsg(GMDD.data.NEED_LOCK_TARGET, ())
            return False
        if p.id != target.id:
            if not needBlockMsg:
                showMsg and p.showGameMsg(GMDD.data.SKILL_FORBIDDEN_TARGET_SELF, ())
            return False
    elif skillTargetType == gametypes.SKILL_TARGET_NONE:
        pass
    elif skillTargetType == gametypes.SKILL_TARGET_POSITION:
        pass
    elif skillTargetType == gametypes.SKILL_TARGET_DIRECTION:
        pass
    else:
        if target == None:
            if p.lockEnemy and skillTargetType in (gametypes.SKILL_TARGET_ENERMY, gametypes.SKILL_TARGET_SELF_ENERMY, gametypes.SKILL_TARGET_ALL_TYPE):
                if hasattr(p, 'getOperationMode') and p.getOperationMode() != gameglobal.ACTION_MODE:
                    p.selectNearAttackable(False)
                    target = p.targetLocked
                elif hasattr(p, 'getOperationMode') and p.getOperationMode() == gameglobal.ACTION_MODE:
                    if p.lockEnemy:
                        p.selectNearAttackable(False, True)
                        if p.targetLocked:
                            p.ap.onTargetFocus(p.targetLocked, True)
            target = p.targetLocked
            if target == None:
                if not needBlockMsg:
                    showMsg and p.showGameMsg(GMDD.data.NEED_LOCK_TARGET, ())
                return False
        if not target.IsCombatUnit:
            if not needBlockMsg:
                showMsg and p.showGameMsg(GMDD.data.INVALID_TARGET, ())
            return False
        if skillTargetType == gametypes.SKILL_TARGET_FRIEND:
            if p.getOperationMode() == gameglobal.ACTION_MODE and p.optionalTargetLocked:
                pass
            else:
                if p.id == target.id:
                    if not needBlockMsg:
                        showMsg and p.showGameMsg(GMDD.data.NEED_TARGET_OTHER, ())
                    return False
                if not p.isFriend(target):
                    if not needBlockMsg:
                        showMsg and p.showGameMsg(GMDD.data.NEED_TARGET_FRIEND, ())
                    return False
        elif skillTargetType == gametypes.SKILL_TARGET_ENERMY:
            if p.getOperationMode() == gameglobal.ACTION_MODE and p.optionalTargetLocked:
                pass
            elif p.id == target.id or not p.isEnemy(target):
                if not needBlockMsg:
                    showMsg and p.showGameMsg(GMDD.data.NEED_TARGET_ENEMY, ())
                return False
        elif skillTargetType == gametypes.SKILL_TARGET_SELF_FRIEND:
            if p.getOperationMode() == gameglobal.ACTION_MODE and p.optionalTargetLocked:
                pass
            elif p.id != target.id and not p.isFriend(target):
                if not needBlockMsg:
                    showMsg and p.showGameMsg(GMDD.data.NEED_TARGET_FRIEND, ())
                return False
        elif skillTargetType == gametypes.SKILL_TARGET_SELF_ENERMY:
            if p.getOperationMode() == gameglobal.ACTION_MODE and p.optionalTargetLocked:
                pass
            elif p.id != target.id and not p.isEnemy(target):
                if not needBlockMsg:
                    showMsg and p.showGameMsg(GMDD.data.NEED_TARGET_ENEMY, ())
                return False
        elif skillTargetType == gametypes.SKILL_TARGET_NOT_SELF:
            if p.getOperationMode() == gameglobal.ACTION_MODE and p.optionalTargetLocked:
                pass
            elif p.id == target.id:
                if not needBlockMsg:
                    showMsg and p.showGameMsg(GMDD.data.NEED_TARGET_NOT_SELF, ())
                return False
        elif skillTargetType == gametypes.SKILL_TARGET_ALL_TYPE:
            pass
        if skillTargetValue != gametypes.OBJ_TYPE_DEAD_BODY and target.life == gametypes.LIFE_DEAD:
            if not needBlockMsg:
                showMsg and p.showGameMsg(GMDD.data.SKILL_FORBIDDEN_TARGET_REMAIN, ())
            return False
        if skillTargetValue == gametypes.OBJ_TYPE_DEAD_BODY and target.life != gametypes.LIFE_DEAD:
            if not needBlockMsg:
                showMsg and p.showGameMsg(GMDD.data.SKILL_FORBIDDEN_TARGET_ALIVE, ())
            return False
        if skillInfo.getSkillData('noInCombat', 0) and p.inCombat == True:
            if not needBlockMsg:
                showMsg and p.showGameMsg(GMDD.data.SKILL_FORBIDDEN_TARGET_IN_COMBAT, ())
            return False
    return True


def checkTargetRequest(skillInfo, showMsg = True, target = None, needBlockMsg = False):
    if not checkTargetRelationRequest(skillInfo, showMsg, needBlockMsg=needBlockMsg):
        return False
    p = BigWorld.player()
    targetLocked = None == target and p.targetLocked or target
    if p.getOperationMode() != gameglobal.MOUSE_MODE:
        if skillInfo.getSkillData('facePos', 0) > 0:
            if not p.isFace(targetLocked):
                if not needBlockMsg:
                    showMsg and p.showGameMsg(GMDD.data.NEED_FACE_TARGET, ())
                return False
    if hasattr(target, 'canBeUsedSkill') and not target.canBeUsedSkill(p, skillInfo):
        return False
    else:
        return True


def checkSelfRequest(skillInfo, showMsg = True, needBlockMsg = False):
    p = BigWorld.player()
    hpNeed = skillInfo.getSkillData('hpNeed', 0)
    if p.hp - hpNeed <= 0:
        if showMsg:
            if not needBlockMsg:
                p.showGameMsg(GMDD.data.HP_LESS, ())
        return False
    mpNeed = skillInfo.getSkillData('mpNeed', 0)
    if p.inNoCostAndCDSkillState():
        mpNeed = 0
    if mpNeed > p.mp:
        now = time.time()
        timeInterval = now - p.lastRegenTime
        delta = p.regenSpeed[2] + p.regenRatioSpeed[2] * p.mmp
        if not p.inCombat:
            delta += p.regenSpeed[3] + p.regenRatioSpeed[3] * p.mmp
        mpRegen = delta * timeInterval
        if p.mp + mpRegen < mpNeed:
            if showMsg:
                p.showGameMsg(GMDD.data.MP_LESS, ())
            return False
    if skillInfo.hasSkillData('wsNeed1') and not p.inNoCostAndCDSkillState():
        wsNeedA = skillInfo.getSkillData('wsNeed1')
        wsReduce = p.wsReduce[0]
        if wsReduce:
            wsNeedA = int(round((1 - wsReduce) * wsNeedA))
        if p.ws[0] < wsNeedA and not p.gmMode:
            if showMsg:
                if not needBlockMsg:
                    p.showGameMsg(GMDD.data.WS_LESS, ())
            return False
        skillInfo.reduceWsA = wsNeedA
    if skillInfo.hasSkillData('wsNeed2') and not p.inNoCostAndCDSkillState():
        wsNeedB = skillInfo.getSkillData('wsNeed2')
        wsReduce = p.wsReduce[1]
        if wsReduce:
            wsNeedB = int(round((1 - wsReduce) * wsNeedB))
        if p.ws[1] < wsNeedB and not p.gmMode:
            if showMsg:
                if not needBlockMsg:
                    p.showGameMsg(GMDD.data.WS_LESS, ())
            return False
        skillInfo.reduceWsB = wsNeedB
    equipments = skillInfo.getSkillData('equipmentId', [])
    if equipments:
        equDict = {}
        for equ in p.equipment:
            if equ == const.CONT_EMPTY_VAL:
                continue
            if not equDict.has_key(equ.id):
                equDict[equ.id] = equ.cwrap
            else:
                equDict[equ.id] += equ.cwrap

        for equipId in equipments:
            if not equDict.has_key(equipId):
                if showMsg and ID.data.has_key(equipId):
                    equipName = ID.data.get(equipId).get('name')
                    if not needBlockMsg:
                        p.showGameMsg(GMDD.data.NO_ITEM, (equipName,))
                return False

    props = skillInfo.getSkillData('propId', [])
    if props:
        propDict = {}
        for pg in xrange(p.inv.pageCount):
            for ps in xrange(p.inv.posCount):
                it = p.inv.getQuickVal(pg, ps)
                if it == const.CONT_EMPTY_VAL:
                    continue
                if not propDict.has_key(it.id):
                    propDict[it.id] = it.cwrap
                else:
                    propDict[it.id] += it.cwrap

        for propId in props:
            if not propDict.has_key(propId):
                if showMsg and ID.data.has_key(propId):
                    propName = ID.data.get(propId).get('name')
                    if not needBlockMsg:
                        p.showGameMsg(GMDD.data.NO_ITEM, (propName,))
                return False

    if skillInfo.hasSkillData('selfStates') or skillInfo.hasSkillData('selfNoStates'):
        curSelfStates = p.getStates().keys()
        selfStates = skillInfo.getSkillData('selfStates', [])
        if selfStates != []:
            checkFlag = selfStates[0]
            temStates = selfStates[1:]
            index = 1
            if checkFlag == 0:
                flag = True
                for i, s in enumerate(temStates):
                    if s not in curSelfStates:
                        flag = False
                        index = i
                        break

            elif checkFlag == 1:
                flag = False
                for i, s in enumerate(temStates):
                    if s in curSelfStates:
                        flag = True
                        break

            if not flag:
                if SD.data.has_key(selfStates[index]):
                    stateName = SD.data.get(selfStates[index]).get('name')
                    if not needBlockMsg:
                        p.showGameMsg(GMDD.data.SKILL_FORBIDDEN_NEED_STATE, (stateName,))
                return False
        selfNoStates = skillInfo.getSkillData('selfNoStates', [])
        for s in selfNoStates:
            if s in curSelfStates:
                if showMsg and STD.data.has_key(s):
                    stateName = STD.data.get(s).get('name')
                    if not needBlockMsg:
                        p.showGameMsg(GMDD.data.SKILL_FORBIDDEN_IN_STATE, (stateName,))
                return False

    if skillInfo.hasSkillData('selfHpLessPct'):
        selfHpLessPct = skillInfo.getSkillData('selfHpLessPct')
        if p.hp > selfHpLessPct * p.mhp / 100.0:
            if showMsg:
                if not needBlockMsg:
                    p.showGameMsg(GMDD.data.SKILL_FORBIDDEN_NEED_STATE, (selfHpLessPct,))
            return False
    if skillInfo.hasSkillData('selfHpMorePct'):
        selfHpMorePct = skillInfo.getSkillData('selfHpMorePct')
        if p.hp < selfHpMorePct * p.mhp / 100.0:
            if showMsg:
                if not needBlockMsg:
                    p.showGameMsg(GMDD.data.SKILL_FORBIDDEN_HP_LOWER, (selfHpMorePct,))
            return False
    if skillInfo.hasSkillData('preAmmoType'):
        preAmmoTypeList = skillInfo.getSkillData('preAmmoType')
        ammoNeed = skillInfo.getSkillData('ammoNeed', 1)
        if p.ammoNum < ammoNeed or p.ammoType not in preAmmoTypeList:
            if not needBlockMsg:
                showMsg and p.showGameMsg(utils.getAmmoMsgID(p.realSchool), ())
            return False
    if skillInfo.num == SCFD.data.get('pullOtherSkillId', 2103):
        if not p.groupNUID or len(p.members) <= 1:
            if not needBlockMsg:
                showMsg and p.showGameMsg(GMDD.data.SKILL_CAN_NOT_PULL_OTHER, ())
            return False
    return True


def checkSkillRequest(skillInfo, showMsg = True, tgt = None, needBlockMsg = False):
    p = BigWorld.player()
    if not p:
        gamelog.debug(gameStrings.TEXT_SKILLDATAINFO_874)
        return False
    elif p.life != gametypes.LIFE_ALIVE:
        if not needBlockMsg:
            p.showGameMsg(GMDD.data.DIE, ())
        return False
    else:
        wpSkillTypes = skillInfo.getSkillData('wpSkillType', None)
        if wpSkillTypes and not p.isInPUBG():
            weaponSkillTypes = (p.weaponTypes['leftWeapon'], p.weaponTypes['rightWeapon'])
            for item in weaponSkillTypes:
                if item not in wpSkillTypes:
                    if not needBlockMsg:
                        p.showGameMsg(GMDD.data.NO_CORRESPONDING_WEAPON, ())
                    return False

        if hasattr(p, 'getOperationMode') and p.getOperationMode() == gameglobal.ACTION_MODE:
            optionTarget = p.getOptionalTargetLocked(skillInfo)
            if optionTarget:
                tgt = optionTarget
        noTarget = skillInfo.getSkillData('noTgt', 0)
        needChooseCursor = isSkillNeedChooseCursor(skillInfo)
        if not noTarget and not needChooseCursor and not checkTargetRequest(skillInfo, target=tgt, needBlockMsg=needBlockMsg):
            gamelog.debug(gameStrings.TEXT_SKILLDATAINFO_899)
            return False
        elif not checkSelfRequest(skillInfo, needBlockMsg=needBlockMsg):
            gamelog.debug('checkSelfRequest Faild')
            return False
        if not noTarget:
            targetLocked = None == tgt and p.targetLocked or tgt
            if skillInfo.getSkillData('tgtPos', 0):
                return True
            if targetLocked != None and hasattr(targetLocked, 'getBodySize'):
                bodySize = targetLocked.getBodySize()
                rangeMin = skillInfo.getSkillData('rangeMin', 0)
                rangeMax = skillInfo.getSkillData('rangeMax', 10000)
                rangeMax = max(rangeMin, (rangeMax + p.skillAdd[2]) * (1 + p.skillAdd[3]))
                rangeMax += bodySize
                if rangeMin != 0:
                    rangeMin += bodySize
                dist = p.position.distTo(targetLocked.position)
                if dist < rangeMin:
                    if not needBlockMsg:
                        p.showGameMsg(GMDD.data.DIST_TOO_CLOSE, ())
                    return False
                if dist > rangeMax:
                    enableSkillDistAutoOpt = gameglobal.rds.configData.get('enableSkillDistAutoOpt', False)
                    if enableSkillDistAutoOpt:
                        p.chaseEntity(targetLocked, rangeMax - 0.5, callback=Functor(useSkillAfterChase, skillInfo))
                    elif not needBlockMsg:
                        p.showGameMsg(GMDD.data.DIST_TOO_FAR, ())
                    return False
            else:
                if skillInfo.getSkillData('tgtDir', 0):
                    return True
                if needChooseCursor:
                    pass
                else:
                    if not needBlockMsg:
                        p.showGameMsg(GMDD.data.NEED_LOCK_TARGET, ())
                    return False
        return True


def useSkillAfterChase(skillInfo):
    if skillInfo:
        BigWorld.player().useSkillByKeyDown(True, skillInfo)


def needBreakSelfSpell(oldSkillid, skillInfo):
    return oldSkillid in skillInfo.getSkillData('breakSpellSkillId', [])


def ignoreForceMove(skillInfo):
    return skillInfo.getSkillData('ignoreForceMove', False)


def checkCollide(skillInfo):
    p = BigWorld.player()
    collideHeight = skillInfo.getSkillData('collideHeight', None)
    if collideHeight:
        target = p.targetLocked
        if hasattr(p, 'getOperationMode') and p.getOperationMode() == gameglobal.ACTION_MODE:
            optionTarget = p.getOptionalTargetLocked(skillInfo)
            if optionTarget:
                target = optionTarget
        if target and not target.IsFragileObject and not getattr(target, 'IsWingWorldCarrier', False) and not getattr(target, 'IsWingCityWarBuilding', False):
            thrustPos = flyEffect.getMyThrustPoint(p.position, target.position, collideHeight, gameglobal.TREEMATTERKINDS)
            if not thrustPos:
                return False
    return True


def needFlyDestGround(clientSkillInfo):
    return clientSkillInfo.getSkillData('flyDestGround', 0)


def isSingleFlyResult(clientSkillInfo):
    return clientSkillInfo.getSkillData('singleFlyResult', 0)


def isSkillneedCircle(skillInfo):
    return skillInfo.getSkillData('tgtPos', 0)


def getChangSkillType(skillInfo, owner):
    skillType = getSkillType(skillInfo)
    changSkillType = skillInfo.getSkillData('changeSkillType', ())
    if changSkillType:
        for stateId, skType in changSkillType:
            if stateId in owner.statesServerAndOwn.keys():
                return skType

    return skillType


def isSkillNeedChooseCursor(skillInfo):
    skillType = getChangSkillType(skillInfo, BigWorld.player())
    if BigWorld.player().getOperationMode() == gameglobal.ACTION_MODE and gameglobal.NEED_CHOOSE_EFFECT:
        if skillType == 3 or skillType == 4:
            if isNeedTarget(skillInfo):
                if BigWorld.player().ap.lockAim and BigWorld.player().isFriend(BigWorld.player().targetLocked):
                    return False
                else:
                    return True
    return False


def isAvatarModelEx(modelID):
    return gameglobal.isAvatarModel(modelID)


def getSelfStates(clientSkillInfo):
    return clientSkillInfo.getSkillData('selfStates', None)


def getSelfSkillFlags(clientSkillInfo):
    return clientSkillInfo.getSkillData('selfSkillFlags', None)


def getSelfAmmoTypes(clientSkillInfo):
    return clientSkillInfo.getSkillData('selfAmmoTypes', None)


def getSkillEffects(sd, stage = gameglobal.S_HIT, getByStateNo = -1, isHeal = False):
    effectData = None
    if sd:
        if stage == gameglobal.S_SPELLSTART:
            effectData = sd.getSkillData('spellStartEff', None)
        elif stage == gameglobal.S_SPELL:
            effectData = sd.getSkillData('spellEff', None)
        elif stage == gameglobal.S_CAST:
            effectData = sd.getSkillData('castEff', None)
        elif stage == gameglobal.S_CASTSTOP:
            effectData = sd.getSkillData('castStopEff', None)
        elif stage == gameglobal.S_FLY:
            effectData = sd.getSkillData('flyEff', None)
        elif stage == gameglobal.S_HIT:
            if not isHeal:
                effectData = sd.getSkillData('hitEff1', None)
                if effectData:
                    if getByStateNo >= 0 and len(effectData) > getByStateNo:
                        if type(effectData[getByStateNo]) is list or type(effectData[getByStateNo]) is tuple:
                            effectData = effectData[getByStateNo]
            else:
                effectData = sd.getSkillData('hitHealEff', None)
                if effectData:
                    if getByStateNo >= 0 and len(effectData) > getByStateNo:
                        if type(effectData[getByStateNo]) is list or type(effectData[getByStateNo]) is tuple:
                            effectData = effectData[getByStateNo]
        elif stage == gameglobal.S_KEEP:
            effectData = sd.getSkillData('keepSelfBuff', None)
        elif stage == gameglobal.S_MOVE:
            effectData = sd.getSkillData('movingEff', None)
        elif stage == gameglobal.S_MOVE_LEFT:
            effectData = sd.getSkillData('movingEffLeft', None)
        elif stage == gameglobal.S_MOVE_RIGHT:
            effectData = sd.getSkillData('movingEffRight', None)
        elif stage == gameglobal.S_MOVE_BACK:
            effectData = sd.getSkillData('movingEffBack', None)
        elif stage == gameglobal.S_MOVESTOP:
            effectData = sd.getSkillData('movingStopEff', None)
        elif stage == gameglobal.S_MOVESTOP_LEFT:
            effectData = sd.getSkillData('movingStopEffLeft', None)
        elif stage == gameglobal.S_MOVESTOP_RIGHT:
            effectData = sd.getSkillData('movingStopEffRight', None)
        elif stage == gameglobal.S_MOVESTOP_BACK:
            effectData = sd.getSkillData('movingStopEffBack', None)
        elif stage == gameglobal.S_AFTERMOVE:
            effectData = sd.getSkillData('afterMoveEff', None)
        elif stage == gameglobal.S_AFTERMOVESTOP:
            effectData = sd.getSkillData('afterMoveStopEff', None)
        elif stage == gameglobal.S_FLYDEST:
            effectData = sd.getSkillData('flyDestEff', None)
        elif stage == gameglobal.S_GUIDE_STOP:
            effectData = sd.getSkillData('guideStopEff', None)
        elif stage == gameglobal.S_FLYDEST_STOP:
            effectData = sd.getSkillData('flyDestStopEff', None)
        elif stage == gameglobal.S_HOVER:
            effectData = sd.getSkillData('hoverEff', None)
        elif stage == gameglobal.S_WEAPON_ACTION:
            effectData = sd.getSkillData('weaponEff', None)
    if stage in [gameglobal.S_FLYDEST] and effectData and (type(effectData) is list or type(effectData) is tuple):
        effectData = list(effectData)
        effectData.pop(0)
        return [random.choice(effectData)]
    else:
        if stage in [gameglobal.S_HIT] and effectData and (type(effectData) is list or type(effectData) is tuple):
            effectData = list(effectData)
            playType = effectData.pop(0)
            if playType == 0:
                return [random.choice(effectData)]
            else:
                return effectData
        else:
            return effectData
        return


def getFlyDestShakeCameras(sd):
    if sd:
        return sd.getSkillData('flyDestShakeCameras', ())
    else:
        return ()


def getBeCastedEffect(sd):
    if sd:
        return sd.getSkillData('beCastedEffect', ())
    else:
        return ()


def getSkillTintEffect(sd, stage = gameglobal.S_SPELLSTART):
    tintData = None
    if sd:
        if stage == gameglobal.S_SPELLSTART:
            tintData = sd.getSkillData('spellStartTint', None)
        elif stage == gameglobal.S_SPELL:
            tintData = sd.getSkillData('spellTint', None)
        elif stage == gameglobal.S_CAST:
            tintData = sd.getSkillData('castTint', None)
        elif stage == gameglobal.S_CASTSTOP:
            tintData = sd.getSkillData('castStopTint', None)
        elif stage == gameglobal.S_FLY:
            tintData = sd.getSkillData('flyTint', None)
        elif stage == gameglobal.S_MOVE:
            tintData = sd.getSkillData('movingTint', None)
        elif stage == gameglobal.S_MOVESTOP:
            tintData = sd.getSkillData('movingStopTint', None)
        elif stage == gameglobal.S_AFTERMOVE:
            tintData = sd.getSkillData('afterMoveTint', None)
        elif stage == gameglobal.S_AFTERMOVESTOP:
            tintData = sd.getSkillData('afterMoveStopTint', None)
        elif stage == gameglobal.S_FLYDEST:
            tintData = sd.getSkillData('flyDestTint', None)
    return tintData


def getHitTintId(tgt, skillInfo, clientSkillInfo, dmtype, host):
    tintFx = None
    if dmtype == gametypes.DMGPOWER_CRIT:
        tintFx = clientSkillInfo.getSkillData('critHitTint', None)
    else:
        tintFx = clientSkillInfo.getSkillData('hitTint', None)
    if not tintFx:
        if hasattr(tgt, 'monsterInstance'):
            md = MMCD.data.get(tgt.charType, {})
            tintFx = md.get('hitTint', None)
            if not tintFx:
                tintFx = (gameglobal.HIGHLIGHT_DEFAULT_TINT, (1, 2, 3))
        elif utils.instanceof(host, 'PlayerAvatar'):
            zaijuId = getattr(tgt, 'bianshen', (0, 0))[1]
            if zaijuId:
                tintFx = ZD.data.get(zaijuId, {}).get('hitTint', (gameglobal.HIGHLIGHT_DEFAULT_TINT, (1, 2, 3)))
    return tintFx


def getHitWeaponType(skillInfo):
    sd = ClientSkillInfo(skillInfo.num, skillInfo.lv)
    gamelog.debug('lihang@getHitWeaponType', sd.getSkillData('hitWeaponType', None), skillInfo.num, skillInfo.lv)
    return sd.getSkillData('hitWeaponType', None)


def getFlyDestEffect(clientSkillInfo):
    return clientSkillInfo.getSkillData('flyDestEff', None)


def getCastEffectTime(clientSkillInfo):
    return clientSkillInfo.getSkillData('castEffectTime', None)


def getSkillWeapon(clientSkillInfo):
    return clientSkillInfo.getSkillData('weapon', gametypes.WEAPON_DOUBLEATTACH)


def getSkillEndWeapon(clientSkillInfo):
    return clientSkillInfo.getSkillData('endWeapon', gametypes.WEAPON_DOUBLEATTACH)


def getMoveType(stage, skillInfo):
    sd = ClientSkillInfo(skillInfo.num, skillInfo.lv)
    if sd:
        if stage == gameglobal.S_CAST:
            return sd.getSkillData('castActType', 0)
        if stage == gameglobal.S_MOVE:
            return sd.getSkillData('movingActType', 0)
        if stage == gameglobal.S_AFTERMOVE:
            return sd.getSkillData('afterMoveActType', 0)
        if stage == gameglobal.S_MOVESTOP:
            return sd.getSkillData('moveStopType', 0)


def getSkillActionName(sd, stage, getByStateNo = -1):
    actData = None
    if sd:
        if stage == gameglobal.S_SPELLSTART:
            actData = sd.getSkillData('spellStartAct', None)
        elif stage == gameglobal.S_SPELL:
            actData = sd.getSkillData('spellAct', None)
        elif stage == gameglobal.S_CAST:
            actData = sd.getSkillData('castAct', None)
        elif stage == gameglobal.S_CASTSTOP:
            actData = sd.getSkillData('castStopAct', None)
        elif stage == gameglobal.S_MOVE:
            actData = sd.getSkillData('movingAct', None)
        elif stage == gameglobal.S_MOVE_LEFT:
            actData = sd.getSkillData('movingActLeft', None)
        elif stage == gameglobal.S_MOVE_RIGHT:
            actData = sd.getSkillData('movingActRight', None)
        elif stage == gameglobal.S_MOVE_BACK:
            actData = sd.getSkillData('movingActBack', None)
        elif stage == gameglobal.S_MOVESTOP:
            actData = sd.getSkillData('movingActStop', None)
        elif stage == gameglobal.S_MOVESTOP_LEFT:
            actData = sd.getSkillData('movingActStopLeft', None)
        elif stage == gameglobal.S_MOVESTOP_RIGHT:
            actData = sd.getSkillData('movingActStopRight', None)
        elif stage == gameglobal.S_MOVESTOP_BACK:
            actData = sd.getSkillData('movingActStopBack', None)
        elif stage == gameglobal.S_AFTERMOVE:
            actData = sd.getSkillData('afterMoveAct', None)
        elif stage == gameglobal.S_AFTERMOVESTOP:
            actData = sd.getSkillData('afterMoveActStop', None)
        elif stage == gameglobal.S_WEAPON_ACTION:
            actData = sd.getSkillData('weaponAction', None)
    return actData


def getSkillcollideHeight(skillInfo):
    return skillInfo.getSkillData('collideHeight', None)


def isSpellActLoop(skillInfo):
    return not skillInfo.getSkillData('spellNoLoop', False)


def getCastType(skillInfo):
    return skillInfo.getSkillData('castType', 0)


def getChargeStgs(skillInfo):
    return skillInfo.getSkillData('chargeStgs', [])


def getGuideHpNeed(skillInfo):
    return skillInfo.getSkillData('guidehpNeed', 0)


def getSkillCategory(skillInfo):
    return skillInfo.getSkillData('skillCategory', 0)


def isPreSpellSkill(skillInfo):
    return skillInfo.getSkillData('preSpell', None)


def hideSpellBar(skillInfo):
    return skillInfo.getSkillData('hideSpellBar', None)


def isSpellSkillCanMove(skillInfo):
    return skillInfo.getSkillData('spellMoveable', None)


def getGuideMpNeed(skillInfo):
    return skillInfo.getSkillData('guidempNeed', 0)


def getCastLoop(skillInfo):
    return skillInfo.getSkillData('castLoop', 0)


def isHideCastBar(skillInfo):
    return skillInfo.getSkillData('hideCastBar', None)


def isMovingSkill(skillInfo):
    return skillInfo.getSkillData('moveid', 0)


def isTgtNeedSpellBar(clientSkillInfo):
    return clientSkillInfo.getSkillData('tgtNeedSpellBar', False)


def getSpellWarnEffect(clientSkillInfo):
    effectData = clientSkillInfo.getSkillData('spellWarnEff', None)
    if effectData:
        effectData = list(effectData)
        num = effectData.pop(0)
        if num == 0:
            return [random.choice(effectData)]
        else:
            return effectData
    else:
        return


def getSpellConnector(clientSkillInfo):
    data = clientSkillInfo.getSkillData('spellConnector', ())
    if not data or len(data) < 3:
        return (None, None, None)
    else:
        startNode = data[0]
        endNode = data[1]
        effect = data[2]
        return (startNode, endNode, effect)


def getSpellWarnEffectDisplayType(clientSkillInfo):
    return clientSkillInfo.getSkillData('spellWarnEffDislayType', None)


def isNeedDestEffDelay(clientSkillInfo):
    return clientSkillInfo.getSkillData('destEffDelay', None)


def hasState(owner, stateId):
    return stateId in owner.getStates()


def getCastDelay(owner, skillInfo):
    d = skillInfo.getSkillData('castDelay', 0)
    if isinstance(d, tuple):
        defalutVal = 0
        for stateId, t in d:
            if stateId == 0:
                defalutVal = t
                continue
            if hasState(owner, stateId):
                return t

        return defalutVal
    else:
        return d


def getSkillKit(clientSkillInfo):
    actName = ('spellStartAct', 'spellAct', 'castAct', 'castStopAct', 'movingAct', 'movingActStop', 'afterMoveAct', 'afterMoveActStop')
    kit = 0
    l = 100
    for key in actName:
        value = clientSkillInfo.skillData.get(key, [])
        if value and value[0] == 0:
            l = min(l, len(value) - 1)

    if l != 100:
        kit = random.randint(0, l - 1)
    return kit


def getSkillAction(clientSkillInfo):
    skillActionList = []
    actName = ('spellStartAct', 'spellAct', 'castAct', 'castStopAct', 'movingAct', 'movingActStop', 'afterMoveAct', 'afterMoveActStop')
    for key in actName:
        value = clientSkillInfo.skillData.get(key, [])
        if value:
            value = list(value)
            skillActionList.extend(value[1:])

    return skillActionList


def getSkillEffect(clientSkillInfo):
    effectList = []
    effectName = ('spellEff', 'castEff', 'flyEff', 'movingEff', 'afterMoveEff')
    for key in effectName:
        value = clientSkillInfo.skillData.get(key, [])
        if value:
            value = list(value)
            effectList.extend(value[1:])

    return effectList


def getGuideType(clientSkillInfo):
    return clientSkillInfo.getSkillData('guideType', 0)


def getScreenEffect(clientSkillInfo):
    return clientSkillInfo.getSkillData('castScreenEff', 0)


def getSpellScreenEffect(clientSkillInfo):
    return clientSkillInfo.getSkillData('spellScreenEff', None)


class SkillInfoVal(SkillEnhanceCommon):

    def __init__(self, skillId, level, enable = False):
        self.skillId = skillId
        self.level = level
        self.enable = enable
        self.isWsSkill = False
        self.wsType = 1
        self.isSocialSkill = False
        self.enhanceData = {}


class QingGongSkillInfoVal(object):

    def __init__(self, skillId, level, enable = False):
        self.skillId = skillId
        self.level = level
        self.enable = enable


class PSkillSubDict(dict):

    def removePSkill(self, pskId, subSrc):
        self.pop(subSrc, None)


class PSkillVal(object):

    def __init__(self, pskId, level, enable = False):
        self.id = pskId
        self.level = level
        self.enable = enable
        self.pData = {}
        self.nextTriggerTime = 0
        self.triggerInvalidTime = 0


def getBuffAppearanceSkillInfo(owner, stateId):
    skillId = SCD.data.get(stateId, {}).get('sid', -1)
    if skillId == -1:
        return ClientSkillInfo(stateId, 1, 1)
    appearanceId = getStateSourceAppearanceId(owner, stateId)
    if appearanceId == -1:
        return ClientSkillInfo(stateId, 1, 1)
    return AppearanceSkillInfo(stateId, appearanceId, AppearanceSkillInfo.SKILL_TYPE_BUFF)


def getStateSourceAppearanceId(owner, stateId):
    newestStateId = -1
    newestSrcId = -1
    states = owner.getStates()
    if stateId in states:
        for stateInfo in states[stateId]:
            if newestStateId < stateInfo[1]:
                newestStateId = stateInfo[1]
                newestSrcId = stateInfo[3]

    if newestStateId == -1 and stateId in owner.statesOld:
        states = owner.statesOld
        for stateInfo in states[stateId]:
            if newestStateId < stateInfo[1]:
                newestStateId = stateInfo[1]
                newestSrcId = stateInfo[3]

    if newestStateId == -1:
        return -1
    skillId = SCD.data.get(stateId, {}).get('sid', -1)
    srcEnt = BigWorld.entities.get(newestSrcId)
    if not srcEnt:
        if hasattr(owner, 'otherSkillAppearanceCache') and stateId in owner.otherSkillAppearanceCache:
            return owner.otherSkillAppearanceCache[stateId]
    elif hasattr(srcEnt, 'skillAppearancesDetail'):
        return srcEnt.skillAppearancesDetail.getCurrentAppearance(skillId)
    return -1
