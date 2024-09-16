#Embedded file name: I:/bag/tmp/tw2/res/entities\common/socialSkillCommon.o
import BigWorld
import gamelog
from data import social_school_skill_data as SSSD
from cdata import game_msg_def_data as GMDD

def socialSkillLvUpCheck(owner, skillId, nLevel, bMsg = True):
    if not owner.socialSchool:
        gamelog.debug('zt: level up fail: invalid school', owner.roleName)
        return False
    schoolSkillsData = SSSD.data.get(owner.socialSchool, {})
    skillData = schoolSkillsData.get(skillId)
    if not skillData:
        gamelog.error('zt: cannot get skillData', owner.socialSchool, skillId)
        return False
    skillVal = owner.mySkills().get(skillId)
    if not skillVal:
        gamelog.error('zt: cannot get skillVal', owner.socialSchool, skillId)
        return False
    maxLevel = len(skillData.get('socialLvNeed', ())) or len(skillData.get('socialExpReduce', ())) or len(skillData.get('cashReduce', ()))
    if skillVal.level + nLevel > maxLevel:
        gamelog.debug('zt: level up fail: reach max level', maxLevel, skillVal.level)
        return False
    preSkillPoint = getPreSkillPoint(owner, schoolSkillsData)
    if skillData.has_key('preSkillPointNeed') and skillData['preSkillPointNeed']:
        if preSkillPoint < skillData['preSkillPointNeed']:
            gamelog.debug('zt: need preSkillPoint', owner.socialSchool, skillId, preSkillPoint, skillData['preSkillPointNeed'])
            return False
    if skillData.has_key('socialLvNeed'):
        if owner.socLv < skillData['socialLvNeed'][skillVal.level + nLevel - 1]:
            gamelog.debug('zt: need social lv', skillId, skillVal.level, skillData['socialLvNeed'], owner.socLv)
            return False
    if skillData.has_key('preSkillLvNeed'):
        skillLvNeed = zip(skillData['preSkillNeed'], skillData['preSkillLvNeed'])
        for sid, slv in skillLvNeed:
            sVal = owner.mySkills().get(sid)
            if not sVal or sVal.level < slv:
                gamelog.debug('zt: need social skill lv', skillId, sid, slv)
                return False

    return True


def socialSkillLvUpCostCheck(owner, skillId, nLevel, bMsg = True):
    if BigWorld.component in ('cell',):
        channel = owner.client
    elif BigWorld.component in ('client',):
        channel = owner
    if nLevel <= 0:
        return True
    if not owner.socialSchool:
        gamelog.debug('zt: level up fail: invalid school', owner.roleName)
        return False
    skillVal = owner.mySkills().get(skillId)
    if not skillVal:
        gamelog.error('zt: cannot get skillVal', owner.socialSchool, skillId)
        return False
    schoolSkillsData = SSSD.data.get(owner.socialSchool, {})
    skillData = schoolSkillsData.get(skillId)
    if not skillData:
        gamelog.error('zt: cannot get skillData', owner.socialSchool, skillId)
        return False
    if skillData.has_key('socialExpReduce'):
        socExpNeed = 0
        for lv in range(skillVal.level, skillVal.level + nLevel):
            socExpNeed += skillData['socialExpReduce'][lv]

        if owner.socExp < socExpNeed:
            gamelog.debug('zt: social skill lv up need socialExp', skillData['socialExpReduce'])
            bMsg and channel.showGameMsg(GMDD.data.SOCIAL_SKILL_LV_UP_FAIL_EXP, ())
            return False
    if skillData.has_key('cashReduce'):
        cashNeed = 0
        for lv in range(skillVal.level, skillVal.level + nLevel):
            cashNeed += skillData['cashReduce'][lv]

        if cashNeed and owner.inv.isRefuse():
            bMsg and channel.showGameMsg(GMDD.data.ITEM_INV_LOCKED, ())
            return False
        if not owner._canPay(cashNeed):
            gamelog.debug('zt: social skill lv up need cash', skillData['cashReduce'])
            bMsg and channel.showGameMsg(GMDD.data.SOCIAL_SKILL_LV_UP_FAIL_CASH, ())
            return False
    return True


def getPreSkillPoint(owner, schoolSkillsData):
    preSkillPoint = 0
    for sid, _ in schoolSkillsData.iteritems():
        sVal = owner.mySkills().get(sid)
        if sVal:
            preSkillPoint += sVal.level

    return preSkillPoint
