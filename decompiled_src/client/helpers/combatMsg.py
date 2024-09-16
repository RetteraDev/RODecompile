#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\helpers/combatMsg.o
import BigWorld
import gametypes
import const
import utils
from utils import quote
from gameclass import SkillInfo
from data import skill_general_template_data as SGTD
from data import state_data as SD
from cdata import game_msg_def_data as GMDD

def ignoreExcept(func):

    def silence(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            import traceback, sys
            traceback.print_exception(*sys.exc_info())

    return silence


def _getSkillName(src, skillId, skillLv):
    return SGTD.data.get(skillId).get('name')


@ignoreExcept
def useSkill(src, tgt, skillId, skillLv):
    if not tgt:
        return
    p = BigWorld.player()
    skillName = _getSkillName(src, skillId, skillLv)
    skillInfo = SkillInfo(skillId, skillLv)
    if skillInfo.getSkillData('noTgt', 0):
        if p.id == src.id:
            p.showGameMsg(GMDD.data.COMBAT_MSG_USE_SKILL_POS, (const.YOU, skillName))
        return
    if p.id == src.id:
        skillName and p.showGameMsg(GMDD.data.COMBAT_MSG_USE_SKILL, (const.YOU, src.id == tgt.id and const.YOU or quote(utils.roleName2SSCName(tgt)), skillName))
    elif src.id != tgt.id and p.id == tgt.id:
        skillName and p.showGameMsg(GMDD.data.COMBAT_MSG_USE_SKILL, (quote(utils.roleName2SSCName(src)), const.YOU, skillName))


@ignoreExcept
def useSkillPos(src, skillId, skillLv):
    p = BigWorld.player()
    if p.id == src.id:
        skillName = _getSkillName(src, skillId, skillLv)
        skillName and p.showGameMsg(GMDD.data.COMBAT_MSG_USE_SKILL_POS, (const.YOU, skillName))


@ignoreExcept
def singleStateCEEffect(stateSrc, stateTgt, stateId, hp, mp, oneTime = False):
    p = BigWorld.player()
    src = BigWorld.entities.get(stateSrc)
    tgt = BigWorld.entities.get(stateTgt)
    if not src or not tgt:
        return
    stateName = SD.data.get(stateId, {}).get('name', '')
    dotDmgType = SD.data.get(stateId, {}).get('dotDmgType', 0)
    if dotDmgType == gametypes.SKILL_EFFECT_PHYSICS:
        dmgTypeName = const.COMBAT_MSG_PHY
    elif dotDmgType == gametypes.SKILL_EFFECT_MAGIC:
        dmgTypeName = const.COMBAT_MSG_MAG
    else:
        dmgTypeName = const.COMBAT_MSG_NORMAL
    powerDesc = const.COMBAT_MSG_NORMAL
    bMsg = False
    if hp < 0:
        value = -hp
        if tgt.id == p.id or tgt.IsSummoned and tgt.ownerId == p.id or tgt.IsWingWorldCarrier and tgt.id == p.wingWorldCarrier.carrierEntId:
            srcRole = src.id == p.id and const.YOU or quote(utils.roleName2SSCName(src))
            if tgt.id == p.id or tgt.IsWingWorldCarrier and tgt.id == p.wingWorldCarrier.carrierEntId:
                tgtRole = const.YOU
            else:
                tgtRole = quote(utils.roleName2SSCName(tgt))
            if src.IsSummonedBeast:
                owner = BigWorld.entities.get(src.ownerId)
                if owner:
                    p.showGameMsg(GMDD.data.COMBAT_MSG_DMG_SB, (src.ownerId == p.id and const.YOU or quote(utils.roleName2SSCName(owner)),
                     srcRole,
                     stateName,
                     tgtRole,
                     value,
                     dmgTypeName,
                     powerDesc))
                    bMsg = True
            elif src.IsSummonedSprite:
                owner = BigWorld.entities.get(src.ownerId)
                if owner:
                    p.showGameMsg(GMDD.data.COMBAT_MSG_SPRITE_DO_DMG, (src.ownerId == p.id and const.YOU or quote(utils.roleName2SSCName(owner)),
                     srcRole,
                     stateName,
                     tgtRole,
                     value,
                     dmgTypeName,
                     powerDesc))
                    bMsg = True
            else:
                if not oneTime:
                    if srcRole == p.roleName:
                        p.showGameMsg(GMDD.data.COMBAT_MSG_DO_DMG, (const.YOU,
                         stateName,
                         tgtRole,
                         value,
                         dmgTypeName,
                         powerDesc))
                    elif tgtRole == p.roleName:
                        p.showGameMsg(GMDD.data.COMBAT_MSG_BE_DMG, (srcRole,
                         stateName,
                         const.YOU,
                         value,
                         dmgTypeName,
                         powerDesc))
                    else:
                        p.showGameMsg(GMDD.data.COMBAT_MSG_DMG, (srcRole,
                         stateName,
                         tgtRole,
                         value,
                         dmgTypeName,
                         powerDesc))
                else:
                    p.showGameMsg(GMDD.data.COMBAT_MSG_CALC_STATE_DMG_ONETIME, (srcRole,
                     stateName,
                     tgtRole,
                     value,
                     dmgTypeName))
                bMsg = True
        if src and not bMsg:
            tgtRole = tgt.id == p.id and const.YOU or quote(utils.roleName2SSCName(tgt))
            if src.id == p.id:
                if not oneTime:
                    p.showGameMsg(GMDD.data.COMBAT_MSG_DO_DMG, (const.YOU,
                     stateName,
                     tgtRole,
                     value,
                     dmgTypeName,
                     powerDesc))
                else:
                    p.showGameMsg(GMDD.data.COMBAT_MSG_CALC_STATE_DMG_ONETIME, (const.YOU,
                     stateName,
                     tgtRole,
                     value,
                     dmgTypeName))
            elif src.IsSummoned and src.ownerId == p.id:
                if src.IsSummonedBeast:
                    p.showGameMsg(GMDD.data.COMBAT_MSG_DMG_SB, (const.YOU,
                     utils.roleName2SSCName(src),
                     stateName,
                     tgtRole,
                     value,
                     dmgTypeName,
                     powerDesc))
                elif src.IsSummonedSprite:
                    p.showGameMsg(GMDD.data.COMBAT_MSG_SPRITE_DO_DMG, (const.YOU,
                     utils.roleName2SSCName(src),
                     stateName,
                     tgtRole,
                     value,
                     dmgTypeName,
                     powerDesc))
    bMsg = False
    if hp > 0 or mp > 0:
        if hp > 0:
            value = hp
            valueTypeName = const.COMBAT_MSG_HP
        else:
            value = mp
            if not tgt.IsSummonedSprite:
                valueTypeName = const.COMBAT_MSG_MP
            else:
                valueTypeName = const.COMBAT_MSG_SPRITE_MP
        if tgt.id == p.id or tgt.IsSummoned and tgt.ownerId == p.id or tgt.IsWingWorldCarrier and tgt.id == p.wingWorldCarrier.carrierEntId:
            srcRole = src.id == p.id and const.YOU or quote(utils.roleName2SSCName(src))
            if tgt.id == src.id:
                tgtRole = const.SELF
            elif tgt.id == p.id or tgt.IsWingWorldCarrier and tgt.id == p.wingWorldCarrier.carrierEntId:
                tgtRole = const.YOU
            else:
                tgtRole = quote(utils.roleName2SSCName(tgt))
            if src.IsSummoned:
                owner = BigWorld.entities.get(src.ownerId)
                if owner:
                    if src.IsSummonedSprite:
                        msgId = GMDD.data.COMBAT_MSG_SPRITE_DO_HEAL
                    else:
                        msgId = GMDD.data.COMBAT_MSG_HEAL_SB
                    p.showGameMsg(msgId, (quote(utils.roleName2SSCName(owner)),
                     utils.roleName2SSCName(src),
                     stateName,
                     tgtRole,
                     value,
                     valueTypeName,
                     gametypes.DMGPOWER_DESC[gametypes.DMGPOWER_NORMAL]))
                    bMsg = True
            else:
                if not oneTime:
                    p.showGameMsg(GMDD.data.COMBAT_MSG_HEAL, (srcRole,
                     stateName,
                     tgtRole,
                     value,
                     valueTypeName,
                     gametypes.DMGPOWER_DESC[gametypes.DMGPOWER_NORMAL]))
                else:
                    p.showGameMsg(GMDD.data.COMBAT_MSG_CALC_STATE_HEAL_ONETIME, (srcRole,
                     stateName,
                     tgtRole,
                     value,
                     valueTypeName))
                bMsg = True
        if src and not bMsg:
            tgtRole = tgt.id == p.id and const.SELF or quote(utils.roleName2SSCName(tgt))
            if src.id == p.id:
                if not oneTime:
                    p.showGameMsg(GMDD.data.COMBAT_MSG_HEAL, (const.YOU,
                     stateName,
                     tgtRole,
                     value,
                     valueTypeName,
                     gametypes.DMGPOWER_DESC[gametypes.DMGPOWER_NORMAL]))
                else:
                    p.showGameMsg(GMDD.data.COMBAT_MSG_CALC_STATE_HEAL_ONETIME, (const.YOU,
                     stateName,
                     tgtRole,
                     value,
                     valueTypeName))
            elif src.IsSummoned and src.ownerId == p.id:
                if src.IsSummonedSprite:
                    msgId = GMDD.data.COMBAT_MSG_SPRITE_DO_HEAL
                else:
                    msgId = GMDD.data.COMBAT_MSG_HEAL_SB
                p.showGameMsg(msgId, (const.YOU,
                 utils.roleName2SSCName(src),
                 stateName,
                 tgtRole,
                 value,
                 valueTypeName,
                 gametypes.DMGPOWER_DESC[gametypes.DMGPOWER_NORMAL]))
    if mp < 0:
        if not tgt.IsSummonedSprite:
            valueTypeName = const.COMBAT_MSG_MP
        else:
            valueTypeName = const.COMBAT_MSG_SPRITE_MP
        if tgt.id == p.id:
            p.showGameMsg(GMDD.data.COMBAT_MSG_STATE_CE_DEC, (stateName,
             const.YOU,
             -mp,
             valueTypeName))
        else:
            p.showGameMsg(GMDD.data.COMBAT_MSG_STATE_CE_DEC, (stateName,
             utils.roleName2SSCName(tgt),
             -mp,
             valueTypeName))
