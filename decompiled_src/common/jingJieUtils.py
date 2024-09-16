#Embedded file name: I:/bag/tmp/tw2/res/entities\common/jingJieUtils.o
import utils
import const
import gamelog
import BigWorld
from data import rune_data as RD
from data import rune_equip_data as RED
from data import skill_general_data as SGD
JINGJIE_CHECK_LV = 1
JINGJIE_CHECK_ACTIVE_SKILL_POINT = 2
JINGJIE_CHECK_SKILL_ENHANCE_POINT = 3
JINGJIE_CHECK_SKILL_ENHANCE = 4
JINGJIE_CHECK_WS = 5
JINGJIE_CHECK_RUNE = 6
JINGJIE_CHECK_AIR_SKILL = 7
SUB_TYPE_SKILL_ENHANCE_MID = 1
SUB_TYPE_SKILL_ENHANCE_HIGH = 2
SUB_TYPE_CHECK_WS_LV = 1
SUB_TYPE_CHECK_WS_MID = 2
SUB_TYPE_CHECK_WS_SLOT = 3
SUB_TYPE_CHECK_RUNE_FULL = 1
SUB_TYPE_CHECK_RUNE_WAKE = 2
RUNE_TYPE_WAKE_TIANLUN = 1
RUNE_TYPE_WAKE_DILUN = 2
RUNE_TYPE_WAKE_ALL = 3
jingJieCondCheckMap = {}

def jingJieCondChecker(source):

    def func(method):
        jingJieCondCheckMap[source] = method.__name__
        return method

    return func


@jingJieCondChecker(JINGJIE_CHECK_LV)
def _checkLv(owner, cond):
    gamelog.info('@hjx jj#_checkLv:', owner.id, cond)
    needLv, = cond
    if owner.lv >= needLv:
        return (True, '')
    else:
        return (False, '(%d/%d)' % (owner.lv, needLv))


@jingJieCondChecker(JINGJIE_CHECK_ACTIVE_SKILL_POINT)
def _checkActiveSkillPoint(owner, cond):
    gamelog.info('@hjx jj#_checkActiveSkillPoint:', owner.id, cond)
    lv, = cond
    maxSkillPoint = utils.getCurSkillPoint(lv)
    if owner.activeSkillPoint >= maxSkillPoint:
        return (True, '')
    else:
        return (False, '(%d/%d)' % (owner.activeSkillPoint, maxSkillPoint))


@jingJieCondChecker(JINGJIE_CHECK_SKILL_ENHANCE_POINT)
def _checkSkillEnhancePoint(owner, cond):
    gamelog.info('@hjx jj#_checkSkillEnhancePoint:', owner.id, cond)
    needSkillEnhancePoint, = cond
    skillEnhancePoint = utils.getTotalSkillEnhancePoint(owner)
    if skillEnhancePoint >= needSkillEnhancePoint:
        return (True, '')
    else:
        return (False, '(%d/%d)' % (skillEnhancePoint, needSkillEnhancePoint))


@jingJieCondChecker(JINGJIE_CHECK_SKILL_ENHANCE)
def _checkSkillEnhance(owner, cond):
    gamelog.info('@hjx jj#_checkSkillEnhance:', owner.id, cond)
    cType, num = cond
    cnt = 0
    if cType == SUB_TYPE_SKILL_ENHANCE_MID:
        for sVal in owner.skills.itervalues():
            for part, val in sVal.enhanceData.iteritems():
                if part / 10 == const.SKILL_ENHANCE_ROW_MID and val.enhancePoint > 0:
                    cnt += 1

        if cnt >= num:
            return (True, '')
    elif cType == SUB_TYPE_SKILL_ENHANCE_HIGH:
        for sVal in owner.skills.itervalues():
            for part, val in sVal.enhanceData.iteritems():
                if part / 10 == const.SKILL_ENHANCE_ROW_MAX and val.enhancePoint > 0:
                    cnt += 1

        if cnt >= num:
            return (True, '')
    return (False, '(%d/%d)' % (cnt, num))


@jingJieCondChecker(JINGJIE_CHECK_WS)
def _checkWSSkill(owner, cond):
    gamelog.info('@hjx jj#_checkWSSkill:', owner.id, cond)
    arg1, arg2, arg3 = cond
    cType = arg1
    if cType == SUB_TYPE_CHECK_WS_LV:
        num = arg2
        needLv = arg3
        cnt = 0
        for sVal in owner.wsSkills.itervalues():
            if sVal.level < needLv:
                continue
            cnt += 1

        if cnt >= num:
            return (True, '')
        else:
            return (False, '(%d/%d)' % (cnt, num))
    elif cType == SUB_TYPE_CHECK_WS_MID:
        num = arg2
        needLvType = arg3
        cnt = 0
        for sKey, sVal in owner.wsSkills.iteritems():
            lvType = SGD.data.get((sKey, sVal.level), {}).get('lvType', 0)
            if lvType < needLvType:
                continue
            cnt += 1

        if cnt >= num:
            return (True, '')
        else:
            return (False, '(%d/%d)' % (cnt, num))
    elif cType == SUB_TYPE_CHECK_WS_SLOT:
        num = arg2
        numSlot = arg3
        cnt = owner.getWSSlotsNumWithJingJie(numSlot)
        if cnt >= num:
            return (True, '')
        else:
            return (False, '(%d/%d)' % (cnt, num))
    return (False, '')


@jingJieCondChecker(JINGJIE_CHECK_RUNE)
def _checkRune(owner, cond):
    gamelog.info('@hjx jj#_checkRune:', owner.id, cond)
    arg1, arg2, arg3 = cond
    cType = arg1
    if BigWorld.component == 'client':
        return (False, '')
    import gameconfig
    if not gameconfig.enableHierogramOrRune():
        return (False, '')
    from data import hiero_equip_data as HED
    if cType == SUB_TYPE_CHECK_RUNE_FULL:
        runeEquipLv = arg2
        runeLv = arg3
        if gameconfig.enableHierogram():
            if not hasattr(owner, 'hierogram'):
                return (False, '')
            hieroEquip = owner.hierogram.hieroEquip
            if hieroEquip is None:
                return (False, '')
            lv = HED.data.get(hieroEquip.id, {}).get('order', 0)
            if lv < runeEquipLv:
                return (False, '')
            slotsOpened = owner.getHieroSlotOpenCache()
            fullCnt = 0
            for i in xrange(3):
                fullCnt += slotsOpened[owner.lv][i]

            crystalCnt = 0
            for c in owner.iterAllCrystalItems(ignoreSwitch=False):
                crystalCnt += 1
                lv = RD.data.get(c.id, {}).get('lv', 0)
                if lv < runeLv:
                    return (False, '')

            if crystalCnt < fullCnt:
                return (False, '')
        else:
            if not owner.runeBoard.runeEquip:
                return (False, '')
            itemId = owner.runeBoard.runeEquip.id
            lv = RED.data.get(itemId, {}).get('order', 0)
            if lv < runeEquipLv:
                return (False, '')
            fullCnt = utils.getRuneFullCnt(owner)
            if fullCnt != len(owner.runeBoard.runeEquip.runeData):
                return (False, '')
            for rune in owner.runeBoard.runeEquip.runeData:
                itemId = rune.item.id
                lv = RD.data.get(itemId, {}).get('lv', 0)
                if lv < runeLv:
                    return (False, '')

        return (True, '')
    if cType == SUB_TYPE_CHECK_RUNE_WAKE:
        runeEquipLv = arg2
        runeWakeType = arg3
        if gameconfig.enableHierogram():
            if not hasattr(owner, 'hierogram'):
                return (False, '')
            hieroEquip = owner.hierogram.hieroEquip
            if hieroEquip is None:
                return (False, '')
            lv = HED.data.get(hieroEquip.id, {}).get('order', 0)
            if lv < runeEquipLv:
                return (False, '')
            if runeWakeType == RUNE_TYPE_WAKE_TIANLUN:
                return owner.hierogram.hieroAwakes[const.RUNE_TYPE_TIANLUN]
            if runeWakeType == RUNE_TYPE_WAKE_DILUN:
                return owner.hierogram.hieroAwakes[const.RUNE_TYPE_DILUN]
            if runeWakeType == RUNE_TYPE_WAKE_ALL:
                return owner.hierogram.hieroAwakes[const.RUNE_TYPE_TIANLUN] and owner.hierogram.hieroAwakes[const.RUNE_TYPE_DILUN]
        else:
            if not owner.runeBoard.runeEquip:
                return (False, '')
            itemId = owner.runeBoard.runeEquip.id
            lv = RED.data.get(itemId, {}).get('order', 0)
            if lv < runeEquipLv:
                return (False, '')
            if runeWakeType == RUNE_TYPE_WAKE_TIANLUN:
                return (owner.runeBoard.awakeDict[const.RUNE_TYPE_TIANLUN], '')
            if runeWakeType == RUNE_TYPE_WAKE_DILUN:
                return (owner.runeBoard.awakeDict[const.RUNE_TYPE_DILUN], '')
            if runeWakeType == RUNE_TYPE_WAKE_ALL:
                return (owner.runeBoard.awakeDict[const.RUNE_TYPE_TIANLUN] and owner.runeBoard.awakeDict[const.RUNE_TYPE_DILUN], '')
    return (False, '')


@jingJieCondChecker(JINGJIE_CHECK_AIR_SKILL)
def _checkAirSkill(owner, cond):
    gamelog.info('@hjx jj#_checkAirSkill:', owner.id, cond)
    num, needLvType = cond
    cnt = 0
    for sKey, sVal in owner.airSkills.iteritems():
        lvType = SGD.data.get((sKey, sVal.level), {}).get('lvType', 0)
        if lvType < needLvType:
            continue
        cnt += 1

    if cnt >= num:
        return (True, '')
    else:
        return (False, '(%d/%d)' % (cnt, num))
