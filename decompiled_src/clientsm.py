#Embedded file name: /WORKSPACE/data/entities/client/helpers/clientsm.o
import math
import BigWorld
import gametypes
import gameglobal
import commcalc
import formula
import const
import logicInfo
import gamelog
import keys
import wingWorldUtils
from helpers import aspectHelper
from helpers import action
from helpers import qingGong
from helpers import cellCmd
from data import guild_config_data as GCD
from data import ride_together_data as RTD
from data import state_check_common_data as SCD
from data import sys_config_data as SYSCD
from data import item_data as ID
from data import fb_data as FD
from cdata import game_msg_def_data as GMDD

class StateMachine(object):

    def __init__(self, ownerId):
        super(StateMachine, self).__init__()
        self.player = BigWorld.entity(ownerId)
        self.failedCode = None

    def checkStatus(self, event, exclude = (), bMsg = True):
        if self.checkStatus_check(event, exclude, bMsg):
            self.checkStatus_cancel(event, exclude)
            gamelog.debug('zf: checkStatusTrue', event)
            return True
        else:
            gamelog.debug('zf: checkStatusFalse', event)
            return False

    def checkStatus_check(self, event, exclude = (), bMsg = True):
        table = SCD.data.get(event)
        if table == None:
            return True
        block = table.get('block', [])
        for stat in block:
            if stat in exclude:
                continue
            name = self.getCheckMethod(stat)
            if name:
                func = getattr(self, name, None)
            else:
                func = None
            if func != None:
                if func():
                    try:
                        eventName, eShow = SCD.data['CMD_NAME_DICT'][event]
                        stateName, sShow = SCD.data['STATE_NAME_DICT'][stat]
                        if eShow and sShow:
                            if bMsg:
                                self.player.showGameMsg(GMDD.data.CHECK_STATUS_FAIL, (stateName, eventName))
                    except:
                        pass

                    gamelog.debug('状态检测没过:', event, func, name)
                    return False

        return True

    def getCheckMethod(self, stName):
        return '_check_' + stName

    def getCancelMethod(self, stName):
        return '_cancel_' + stName

    def checkStatus_cancel(self, event, exclude = ()):
        table = SCD.data.get(event)
        if table == None:
            return
        cancel = table.get('cancel', [])
        for stat in cancel:
            if stat in exclude:
                continue
            name = self.getCancelMethod(stat)
            if name:
                func = getattr(self, name, None)
            else:
                func = None
            if func:
                func()

    def afterTurn(self):
        if self.player.inFishing():
            buoyPos = self.player.buoyPos
            if not buoyPos:
                return
            byaw = (buoyPos - self.player.position).yaw
            pyaw = self.player.yaw
            byaw = byaw + 2 * math.pi if byaw < 0 else byaw
            pyaw = pyaw + 2 * math.pi if pyaw < 0 else pyaw
            if abs(byaw - pyaw) > math.pi / 2:
                self.player.showGameMsg(GMDD.data.FISHING_BREAK_NO_FACING_WATER, ())
                self.player.stopFish()

    def checkStartMeeting(self, tableType):
        if tableType == gametypes.ROUND_TABLE_TYPE_FUBEN:
            if not self.player.inFuben():
                self.player.showGameMsg(GMDD.data.ROUND_TABLE_LIMIT_FUBEN, ())
                return False
            return True
        xRange = GCD.data.get('roundTableXRange', None)
        yRange = GCD.data.get('roundTableYRange', None)
        if not xRange or not yRange:
            self.player.showGameMsg(GMDD.data.GUILD_MEETING_OUT_OF_RANGE, ())
            return False
        if self.player.position[0] < xRange[0] or self.player.position[0] > xRange[1]:
            self.player.showGameMsg(GMDD.data.GUILD_MEETING_OUT_OF_RANGE, ())
            return False
        if self.player.position[2] < yRange[0] or self.player.position[2] > yRange[1]:
            self.player.showGameMsg(GMDD.data.GUILD_MEETING_OUT_OF_RANGE, ())
            return False
        dist = GCD.data.get('roundTableDistLimit', 4)
        ents = self.player.entitiesInRange(dist)
        if ents:
            for ent in ents:
                if ent.__class__.__name__ == 'RoundTable':
                    self.player.showGameMsg(GMDD.data.GUILD_MEETING_OTHER_TABLE, ())
                    return False

        return True

    def checkMove(self):
        canMove = True
        if getattr(self.player, 'isInBfDotaChooseHero', False):
            return False
        if self.player.isGuiding == const.GUIDE_TYPE_NO_MOVE:
            if gameglobal.MOVE_STOP_GUIDE:
                pass
            else:
                self.player.chatToEventEx('正在使用无法移动的引导技能', const.CHANNEL_COLOR_RED)
                return False
        if self.player.fashion.doingActionType() in [action.ROLL_ACTION,
         action.ZAIJU_ON_ACTION,
         action.SHOW_WEAR_ACTION,
         action.OPEN_WEAR_ACTION]:
            self.player.chatToEventEx('动作中，操作太频繁', const.CHANNEL_COLOR_RED)
            return False
        if self.player.attachSkillData[0] != 0:
            return False
        if self.player.castSkillBusy and self.player.fashion.doingActionType() == action.UNKNOWN_ACTION:
            self.player.castSkillBusy = False
        if self.player.castSkillBusy and not self.player.skillPlayer.castLoop or self._check_SkillCast():
            if gameglobal.MOVE_STOP_GUIDE and self.player.fashion.doingActionType() in [action.GUIDE_ACTION]:
                pass
            else:
                self.player.showGameMsg(GMDD.data.MOVE_FORBIDDEN_USE_SKILL, ())
                return False
        if not self.checkStatus(const.CT_MOVE):
            return False
        if not self.player.clientControl:
            self.player.showGameMsg(GMDD.data.SKILL_FORBIDDEN_NOW, ())
            return False
        if self.player.isFalling and not self.player.canFly():
            self.player.showGameMsg(GMDD.data.MOVE_FORBIDDEN_FALLING, ())
            return False
        if commcalc.getBitDword(self.player.flags, gametypes.FLAG_DUEL_WAITING):
            self.player.showGameMsg(GMDD.data.MOVE_FORBIDDEN_IN_STATE, 'PVP准备')
            return False
        if commcalc.getBitDword(self.player.flags, gametypes.FLAG_NO_SHAXING_WAITING):
            self.player.showGameMsg(GMDD.data.MOVE_FORBIDDEN_IN_STATE, '等待')
            return False
        if self._check_UNCONTROL_ST():
            self.player.showGameMsg(GMDD.data.MOVE_FORBIDDEN_IN_STATE, '晕眩')
            return False
        if self._check_MAN_DOWN_ST():
            self.player.showGameMsg(GMDD.data.MOVE_FORBIDDEN_IN_STATE, '倒地')
            return False
        if hasattr(self.player, 'publicFlags') and commcalc.getBitDword(self.player.publicFlags, gametypes.FLAG_NOT_MOVABLE):
            self.player.showGameMsg(GMDD.data.MOVE_FORBIDDEN_IN_STATE, '定身')
            return False
        if self.player.spellingType == action.S_PRESPELLING:
            self.player.showGameMsg(GMDD.data.MOVE_FORBIDDEN_IN_STATE, '前摇')
            return False
        if getattr(self.player, 'inForceNavigate', False) and self.player.bianshen[0] == gametypes.BIANSHEN_ZAIJU:
            self.player.showGameMsg(GMDD.data.MOVE_FORBIDDEN_IN_STATE, '系统寻路')
            return False
        if hasattr(self.player, 'inForceNavigate'):
            self.player.inForceNavigate = False
        if self._check_AUTO_PATHFINDING_ST():
            self._cancel_AUTO_PATHFINDING_ST()
        if self.player.isDoingAction:
            cellCmd.cancelAction(const.CANCEL_ACT_MOVE)
        if self.player.spellingType == action.S_SPELLING:
            cellCmd.cancelSkill()
        if not gameglobal.AUTOSKILL_FLAG:
            self.player.autoSkill.stop()
        if self.player.isGuildSitInChair():
            self.player.guildLeaveChair()
        return canMove

    def checkJump(self):
        if self.player.handClimb:
            return False
        if self.player.inSwim:
            return False
        if self.player.needForbidJump():
            self.player.chatToEventEx('载具下禁止跳跃', const.CHANNEL_COLOR_RED)
            return False
        if self.player.qinggongMgr.actionType != gametypes.QINGGONG_ACT_DEFAULT:
            self.player.chatToEventEx('正在使用轻功动作', const.CHANNEL_COLOR_RED)
            return False
        if not self.player.clientControl:
            self.player.chatToEventEx('客户端失去控制', const.CHANNEL_COLOR_RED)
            return False
        dist = self.player.qinggongMgr.getDistanceFromWater()
        if dist and dist < 0.0 and self.player.qinggongMgr.isJumping():
            return False
        if self.player.castSkillBusy and not self.player.isGuiding:
            self.player.chatToEventEx('正在施放技能', const.CHANNEL_COLOR_RED)
            return False
        if self.player.skillPlayer.castLoop:
            self.player.showGameMsg(GMDD.data.MOVE_FORBIDDEN_USE_SKILL, ())
            return False
        if hasattr(self.player, 'flags') and commcalc.getBitDword(self.player.flags, gametypes.FLAG_SKILL_PIN):
            self.player.showGameMsg(GMDD.data.MOVE_FORBIDDEN_IN_STATE, '技能定身')
            return False
        if commcalc.getBitDword(self.player.flags, gametypes.FLAG_DUEL_WAITING):
            self.player.showGameMsg(GMDD.data.MOVE_FORBIDDEN_IN_STATE, 'PVP准备')
            return False
        if commcalc.getBitDword(self.player.flags, gametypes.FLAG_NO_SHAXING_WAITING):
            self.player.showGameMsg(GMDD.data.MOVE_FORBIDDEN_IN_STATE, '等待')
            return False
        if self._check_UNCONTROL_ST() and self.player.qteId <= 0:
            self.player.showGameMsg(GMDD.data.MOVE_FORBIDDEN_IN_STATE, '晕眩')
            return False
        if commcalc.getBitDword(self.player.publicFlags, gametypes.FLAG_NOT_MOVABLE):
            self.player.showGameMsg(GMDD.data.MOVE_FORBIDDEN_IN_STATE, '定身')
            return False
        if getattr(self.player, 'bufNoJump', False):
            self.player.showGameMsg(GMDD.data.BUFF_NO_JUMP, ())
            return False
        if self.player.physics.forbidHorizontalMove:
            gamelog.debug('motionPin中')
            return False
        if self.player.isWaitSkillReturn:
            gamelog.debug('等待服务器返回技能')
            return False
        if self.player.spellingType == action.S_SPELLING:
            cellCmd.cancelSkill()
        if self.player.spellingType == action.S_PRESPELLING:
            return False
        if self.player.fashion.doingActionType() in [action.MOVING_ACTION]:
            gamelog.debug('正在位移中')
            return False
        if self.player.isDoingAction:
            cellCmd.cancelAction(const.CANCEL_ACT_JUMP)
        if not gameglobal.AUTOSKILL_FLAG:
            self.player.autoSkill.stop()
        return True

    def checkSetYaw(self):
        if self.player.life == gametypes.LIFE_DEAD:
            return False
        if self.player.ap.forceSeek:
            return False
        return True

    def checkMount(self):
        p = self.player
        if not p.isQingGongSkillLearned(gametypes.QINGGONG_FLAG_RIDE):
            self.player.showGameMsg(GMDD.data.QINGGONG_RIDE_NO_SKILL, ())
            return False
        item = p.equipment[gametypes.EQU_PART_RIDE]
        if not item:
            self.player.showGameMsg(GMDD.data.QINGGONG_RIDE_NO_HORSE, ())
            return False
        if not p.gmMode and formula.mapLimit(formula.LIMIT_RIDE, formula.getMapId(p.spaceNo)):
            p.showGameMsg(GMDD.data.RIDE_FORBID_IN_MAP, ())
            return False
        if p.inSwim and not item.canSwim():
            return False
        if item.canOnlySwim() and not p.inSwim:
            name = ID.data.get(item.id, {}).get('name', '')
            p.showGameMsg(GMDD.data.RIDE_FORBID_ONLY_SWIM, name)
            return False
        if not self.checkStatus(const.CT_RIDE_HORSE):
            return False
        if item.isSwimRide():
            if not self.checkStatus(const.CT_SWIM_RIDE_HORSE):
                return False
        elif not self.checkStatus(const.CT_NORMAL_RIDE_HORSE):
            return False
        return True

    def checkDismount(self):
        if not self.checkStatus(const.CT_DOWN_RIDE_HORSE):
            self.player.showGameMsg(GMDD.data.QINGGONG_RIDE_STATE_DISMOUNT, ())
            return False
        return True

    def checkOpenWingFly(self):
        p = self.player
        if not p.isQingGongSkillLearned(gametypes.QINGGONG_FLAG_FLY):
            p.showGameMsg(GMDD.data.QINGGONG_FLY_NO_SKILL, ())
            return False
        equip = p.equipment[gametypes.EQU_PART_WINGFLY]
        if not equip:
            self.player.showGameMsg(GMDD.data.QINGGONG_FLY_NO_WING, ())
            return False
        if p.qinggongMgr.getDistanceFromGround() >= gameglobal.FROMGROUNDDIST:
            waterDist = p.qinggongMgr.getDistanceFromWater()
            if waterDist and waterDist >= -3:
                pass
            else:
                return False
        if not p.qinggongMgr.checkCanWingFly():
            return False
        if commcalc.getBitDword(self.player.flags, gametypes.FLAG_NO_QINGGONG_WINFLY):
            p.showGameMsg(GMDD.data.QINGGONG_WINFLY_FORBIDDEN, ())
            return False
        if p.coupleEmote and gametypes.RIDE_TALENT_HUG not in getattr(equip, 'talents', []):
            p.showGameMsg(GMDD.data.WING_DONT_HAS_TALENT, (const.RIDE_WING_TALENT_MULTI_FLY_TEXT,))
            return False
        if not self.checkStatus(const.CT_OPEN_WINGFLY_SPELL):
            return False
        warCityId = p.getWingWarCityId()
        if warCityId and wingWorldUtils.isInAirDefenseRange(p.position, warCityId) and p.wingWorldMiniMap.airStoneEnergy:
            p.showGameMsg(GMDD.data.FORBIDDEN_FLY_IN_AIR_DEFENCE, ())
            return False
        return True

    def checkCloseWingFly(self):
        if not self.checkStatus(const.CT_CLOSE_WINGFLY):
            return False
        return True

    def checkDaZuo(self):
        if not self.checkStatus(const.CT_DA_ZUO):
            return False
        return True

    def checkCoupleEmote(self, emoteId, targetId):
        target = BigWorld.entities.get(targetId)
        if not target:
            self.player.showGameMsg(GMDD.data.NO_COUPLE_EMOTE_TARGET, ())
            return False
        if not (hasattr(target, 'IsAvatar') and target.IsAvatar):
            self.player.showGameMsg(GMDD.data.COUPLE_EMOTE_ONYL_HUG_AVATAR, ())
            return False
        if emoteId == gametypes.COUPLE_EMOTE_TYPE_JUGAOGAO:
            physique = target.physique
            sex = physique.sex
            bodyType = physique.bodyType
            if sex != const.SEX_FEMALE or bodyType != const.BODY_TYPE_2:
                self.player.showGameMsg(GMDD.data.COUPLE_EMOTE_JUGAOGAO_ONLY_FEAMLE2, ())
                return False
        p = self.player
        if p.coupleEmote:
            self.player.showGameMsg(GMDD.data.ALREADY_COUPLE_EMOTE, ())
            return False
        if (p.position - target.position).length > SYSCD.data.get('coupleEmoteDist', const.APPLY_COUPLE_EMOTE_DIST):
            self.player.showGameMsg(GMDD.data.COUPLE_EMOTE_DIST_LIMIT, ())
            return False
        if not self.checkStatus(const.CT_COUPLE_EMOTE_HUG):
            return False
        if not p.isFriend(target):
            self.player.showGameMsg(GMDD.data.CAN_NOT_COUPLE_EMOTE_WITH_ENEMY, ())
            return False
        return True

    def checkRideTogetherMajor(self, targetId):
        target = BigWorld.entities.get(targetId)
        if not target:
            return False
        if not (hasattr(target, 'IsAvatar') and target.IsAvatar):
            return False
        p = self.player
        if (p.position - target.position).length > SYSCD.data.get('rideTogetherDist', 5):
            self.player.showGameMsg(GMDD.data.RIDE_TOGETHER_TOO_FAR, ())
            return False
        if p.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
            canRideTogether = RTD.data.get(p.bianshen[1], {}).get('canRideTogether', False)
            if canRideTogether:
                seatNum = RTD.data.get(p.bianshen[1], {}).get('seatNum', 0)
                if seatNum <= len(p.tride.keys()):
                    self.player.showGameMsg(GMDD.data.CAN_NOT_RIDE_TOGETHER_NO_SEAT, ())
                    return False
            else:
                self.player.showGameMsg(GMDD.data.CAN_NOT_RIDE_TOGETHER_FORBIDE, ())
                return False
        else:
            self.player.showGameMsg(GMDD.data.CAN_NOT_RIDE_TOGETHER_NOT_IN_RIDE, ())
            return False
        seatNum = RTD.data.get(p.bianshen[1], {}).get('seatNum', 0)
        if seatNum <= len(p.tride.keys()):
            self.player.showGameMsg(GMDD.data.RIDE_TOGETHER_SEAT_FULL, ())
            return
        if not self.checkStatus(const.CT_MAJOR_RIDE):
            return False
        if not p.isFriend(target):
            self.player.showGameMsg(GMDD.data.CAN_NOT_RIDE_TOGETHER_WITH_ENEMY, ())
            return False
        return True

    def checkRideTogetherMinor(self, targetId):
        target = BigWorld.entities.get(targetId)
        if not target:
            return False
        if not (hasattr(target, 'IsAvatar') and target.IsAvatar):
            return False
        p = self.player
        if (p.position - target.position).length > SYSCD.data.get('rideTogetherDist', 5):
            self.player.showGameMsg(GMDD.data.RIDE_TOGETHER_TOO_FAR, ())
            return False
        if target.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
            canRideTogether = RTD.data.get(target.bianshen[1], {}).get('canRideTogether', False)
            if canRideTogether:
                seatNum = RTD.data.get(target.bianshen[1], {}).get('seatNum', 0)
                if seatNum <= len(target.tride.keys()):
                    self.player.showGameMsg(GMDD.data.CAN_NOT_RIDE_TOGETHER_NO_SEAT, ())
                    return False
            else:
                self.player.showGameMsg(GMDD.data.CAN_NOT_RIDE_TOGETHER_FORBIDE, ())
                return False
        else:
            self.player.showGameMsg(GMDD.data.CAN_NOT_RIDE_TOGETHER_NOT_IN_RIDE, ())
            return False
        if not self.checkStatus(const.CT_MINOR_RIDE):
            return False
        if not p.isFriend(target):
            return False
        return True

    def checkShowBackWear(self):
        p = self.player
        backwear = p.modelServer.backwear
        if p.fashion.doingActionType() == action.HORSE_WHISTLE_ACTION:
            return False
        if backwear and (backwear.isHangUped() or backwear.isAttached()):
            if backwear.isActionWear() or backwear.isActionJustSkillWear():
                if self.checkStatus(const.CT_SHOW_BACK_WEAR):
                    return True
            else:
                p.showGameMsg(GMDD.data.NOT_SHOW_WEAR, ())
        else:
            p.showGameMsg(GMDD.data.NO_SHOW_WEAR_EQUIP, ())
        return False

    def checkShowWaistWear(self):
        p = self.player
        waistwear = p.modelServer.waistwear
        if p.fashion.doingActionType() == action.HORSE_WHISTLE_ACTION:
            return False
        if waistwear and (waistwear.isHangUped() or waistwear.isAttached()):
            if waistwear.isActionWear() or waistwear.isActionJustSkillWear():
                if self.checkStatus(const.CT_SHOW_WAIST_WEAR):
                    return True
            else:
                p.showGameMsg(GMDD.data.NOT_SHOW_WEAR, ())
        else:
            p.showGameMsg(GMDD.data.NO_SHOW_WEAR_EQUIP, ())
        return False

    def checkShowWearActions(self):
        p = self.player
        if p.weaponInHandState() in (gametypes.WEAR_BACK_ATTACH, gametypes.WEAR_WAIST_ATTACH):
            if self.checkStatus(const.CT_SHOW_WEAR_ACTION):
                return True
        return False

    def _check_FOLLOW_TARGET_ST(self):
        return self.player.ap.isTracing

    def _check_COMBAT_ST(self):
        return self.player.inCombat

    def _check_IN_WABAO(self):
        return self.player.inWabaoStatus

    def _check_MOVE_ST(self):
        return self.player.inMoving()

    def _check_MAN_DOWN_UP_ST(self):
        return self.player.fashion.doingActionType() == action.MAN_DOWN_START_ACTION

    def _check_ACTION_SPELL_ST(self):
        return self.player.isDoingAction

    def _check_WEAPON7_CAPS_ST(self):
        return keys.CAPS_WEAPON7 in self.player.am.matchCaps and keys.CAPS_WEAR not in self.player.am.matchCaps

    def _check_WEAPON8_CAPS_ST(self):
        return keys.CAPS_WEAPON8 in self.player.am.matchCaps and keys.CAPS_WEAR not in self.player.am.matchCaps

    def _check_BUF_ACT_CAPS_ST(self):
        return keys.CAPS_BUF_ACT in self.player.am.matchCaps

    def _check_AUTO_PATHFINDING_ST(self):
        return self.player.checkPathfinding()

    def _check_SkillCast(self):
        return self.player.fashion.doingActionType() in [action.CAST_ACTION,
         action.MOVING_ACTION,
         action.AFTERMOVE_ACTION,
         action.ROLL_ACTION,
         action.CHARGE_ACTION,
         action.ZAIJU_ON_ACTION]

    def _check_AttackAction(self):
        return self.player.fashion.doingActionType() == action.ATTACK_ACTION

    def _check_IN_GROUP_FOLLOW(self):
        return self.player.inGroupFollow

    def _check_IN_MARRIAGE_MULTICARRIER(self):
        return self.player.marriageStage == gametypes.MARRIAGE_STAGE_PARADE

    def _check_IN_MARRIAGE_MULTICARRIER_RUNNING(self):
        return self.player.marriageStage == gametypes.MARRIAGE_STAGE_PARADE and self.player.carrier.isMarriageMultiCarrier() and self.player.carrier.isRunningState() and self.player.isOnCarrier()

    def _check_JUMP_ST(self):
        return self.player.isJumping and self.player.physics.jumping

    def _check_CHAT_ACTION_ST(self):
        return self.player.fashion.doingActionType() == action.CHAT_ACTION

    def _check_PICK_ITEM_ST(self):
        return self.player.fashion.doingActionType() == action.PICK_ITEM_ACTION and not self.player.isInPUBG()

    def _check_FALL_ST(self):
        return self.player.isFalling

    def _check_DEEP_WATER_ST(self):
        return self.player.inSwim == const.DEEPWATER

    def _check_SHOAL_WATER_ST(self):
        return self.player.inSwim == const.SHOALWATER

    def _check_NOT_IN_WATER_ST(self):
        return self.player.inSwim == const.NOWATER

    def _check_BIANSHEN_ST(self):
        return self.player.bsState

    def _check_SCHOOL_SWITCH_ST(self):
        return self.player._isSchoolSwitch()

    def _check_SIT(self):
        return self.player.isSitting()

    def _check_UNCONTROL_ST(self):
        return commcalc.getBitDword(self.player.publicFlags, gametypes.FLAG_NOT_CONTROLLABLE)

    def _check_MAN_DOWN_ST(self):
        return commcalc.getBitDword(self.player.flags, gametypes.FLAG_MAN_DOWN)

    def _check_SLOWSPEED_ST(self):
        return commcalc.getBitDword(self.player.flags, gametypes.FLAG_SLOW_DOWN)

    def _check_UNMOVE_ST(self):
        return self.player.physics.forbidHorizontalMove

    def _check_DASH_ST(self):
        return self.player.qinggongMgr.state == qingGong.STATE_DASH

    def _check_DASH_JUMP_ST(self):
        return self.player.jumpState == gametypes.DASH_JUMP

    def _check_AUTO_JUMP_ST(self):
        return self.player.jumpState == gametypes.AUTO_JUMP or self.player.jumpState == gametypes.DASH_AUTO_JUMP

    def _check_DASH_BIG_JUMP_ST(self):
        return self.player.jumpState == gametypes.DASH_BIG_JUMP

    def _check_ROLL_ST(self):
        if self.player.model.freezeTime > 0:
            return False
        return self.player.fashion.doingActionType() == action.ROLL_ACTION

    def _check_SLIDE_ST(self):
        return self.player.qinggongMgr.state == qingGong.STATE_DASH_TWICE_JUMPING

    def _check_RUSH_DOWN_ST(self):
        return self.player.qinggongMgr.state == qingGong.STATE_RUSH_DOWN

    def _check_RUSH_DOWN_WEAPON_IN_HAND_ST(self):
        return self.player.qinggongMgr.state == qingGong.STATE_RUSH_DOWN_WEAPON_IN_HAND

    def _check_WEAPON_IN_HAND_ST(self):
        return self.player.weaponInHandState() != gametypes.WEAPON_HANDFREE

    def _check_SLIDE_DASH_ST(self):
        return self.player.qinggongMgr.state == qingGong.STATE_SLIDE_DASH

    def _check_SLIDE_DASH_WEAPON_IN_HAND_ST(self):
        return self.player.qinggongMgr.state == qingGong.STATE_SLIDE_DASH_WEAPON_IN_HAND

    def _check_SPELL_ST(self):
        return self.player.spellingType

    def _check_MOVE_SPELL_ST(self):
        return self.player.spellingType == action.S_SPELLING_CAN_MOVE

    def _check_WEN_QUAN_ST(self):
        return getattr(self.player, 'inWenQuanState', False)

    def _check_GUIDE_ST(self):
        return self.player.isGuiding == const.GUIDE_TYPE_NO_MOVE

    def _check_MOVE_GUIDE_ST(self):
        return self.player.isGuiding == const.GUIDE_TYPE_MOVE

    def _check_SILENCE_ST(self):
        return commcalc.getBitDword(self.player.publicFlags, gametypes.FLAG_NO_SKILL) and not self.player.gmMode

    def _check_DEAD_ST(self):
        return self.player.life == gametypes.LIFE_DEAD

    def _check_ZAIJU_ST(self):
        return self.player._isOnZaijuOrBianyao()

    def _check_QUEST_ZAIJU_ST(self):
        return self._isOnZaijuOrBianyao() and self.isQuestZaiju

    def _check_FISHING_ST(self):
        return self.player.inFishing()

    def _check_FISHING_START_ST(self):
        return self.player.inFishingReady() or self.player.inFishingHold()

    def _check_CHARGE_ST(self):
        return self.player.isChargeKeyDown

    def _check_EMOTE_ST(self):
        return self.player.fashion.doingActionType() == action.EMOTE_ACTION

    def _check_SIT_DOWN_ST(self):
        return False

    def _check_FORCE_MOVE_ST(self):
        return self.player.isForceMove

    def _check_IN_GCD_ST(self):
        return logicInfo.isInSkillCommonTime()

    def _check_RIDE_ST(self):
        return self.player.bianshen[0] == gametypes.BIANSHEN_RIDING_RB and not self.player.isOnFlyRide() and not self.player.isOnSwimRide()

    def _check_FLY_RIDE_ST(self):
        return self.player.bianshen[0] == gametypes.BIANSHEN_RIDING_RB and self.player.isOnFlyRide()

    def _check_SWIM_RIDE_ST(self):
        return self.player.bianshen[0] == gametypes.BIANSHEN_RIDING_RB and self.player.isOnSwimRide()

    def _check_SWIM_RIDE_IN_WATER_ST(self):
        return self._check_SWIM_RIDE_ST() and self.player.inSwim

    def _check_WINGFLY_ST(self):
        return self.player.inFly == gametypes.IN_FLY_TYPE_WING and not self.player.inCombat

    def _check_WINGFLY_AND_COMBAT_ST(self):
        return self.player.inFly == gametypes.IN_FLY_TYPE_WING and self.player.inCombat

    def _check_WINGFLY_FLYRIDE_ST(self):
        if self.player.checkInAutoQuest():
            return False
        return self.player.inFly == gametypes.IN_FLY_TYPE_FLY_RIDE

    def _check_ISSLIDING_ST(self):
        return self.player.physics.isSliding

    def _check_BOOTH_ST(self):
        return self.player.inBoothing()

    def _check_CHATROOM_ST(self):
        return bool(self.player.chatRoomNUID)

    def _check_DA_ZUO_ST(self):
        return self.player.inDaZuo()

    def _check_AUTO_MOVE_ST(self):
        return self.player.ap.isAutoMoving

    def _check_HAND_CLIMB_ST(self):
        return self.player.handClimb

    def _check_MAJOR_RIDE_ST(self):
        return self.player.isRidingTogetherAsMain()

    def _check_MINOR_RIDE_ST(self):
        return self.player.isRidingTogetherAsVice()

    def _check_COUPLE_EMOTE_HUG_ST(self):
        if self.player.coupleEmote and self.player.coupleEmote[1] == self.player.id:
            return True
        return False

    def _check_COUPLE_EMOTE_BE_HUG_ST(self):
        if self.player.coupleEmote and self.player.coupleEmote[2] == self.player.id:
            return True
        return False

    def _check_COUPLE_EMOTE_NOT_HUG_ST(self):
        if self.player.coupleEmote:
            if self.player.coupleEmote[0] not in gametypes.COUPLE_EMOTE_TYPE_SPECIAL:
                return True
        return False

    def _check_AUTO_QUEST_ST(self):
        return self.player.checkInAutoQuest()

    def _check_CARROUSEL_ST(self):
        if self.player.inCarrousel():
            return True
        return False

    def _check_USING_LIFE_SKILL_ST(self):
        return self.usingLifeSkill

    def _check_PK_PUNISH_ST(self):
        return self.player.pkPunishTime > 0

    def _check_OBSERVER_FLY_ST(self):
        return self.player.inFlyTypeObserver()

    def _check_PK_ST(self):
        return self.player.pkMode != const.PK_MODE_PEACE

    def _check_HOSTILE_ST(self):
        return self.player.pkMode == const.PK_MODE_HOSTILE

    def _check_WALK_ST(self):
        return self.player.ap.isWalking

    def _check_SOCIAL_ACTION_ST(self):
        return self.player.fashion.doingActionType() == action.SOCIAL_ACTION

    def _check_SHOW_BACK_WEAR_ST(self):
        return self.player.weaponInHandState() == gametypes.WEAR_BACK_ATTACH

    def _check_SHOW_WAIST_WEAR_ST(self):
        return self.player.weaponInHandState() == gametypes.WEAR_WAIST_ATTACH

    def _check_SHOW_WEAR_ACTION_ST(self):
        return self.player.fashion.doingActionType() == action.SHOW_WEAR_ACTION

    def _check_IN_DUEL(self):
        return self.player.inDuelZone() and not self.player.isInPUBG()

    def _check_IN_FUBEN(self):
        return self.player.inFuben()

    def _check_HIDING_POWER_ST(self):
        return self.player.hidingPower > 0

    def _check_WING_TAKE_OFF_ST(self):
        return self.player.inWingTakeOff

    def _check_OPEN_WEAR_ST(self):
        return self.player.fashion.doingActionType() == action.OPEN_WEAR_ACTION

    def _check_CLOSE_WEAR_ST(self):
        return self.player.fashion.doingActionType() == action.CLOSE_WEAR_ACTION

    def _check_WINGFLY_DASH_ST(self):
        return self.player.qinggongState in (gametypes.QINGGONG_STATE_WINGFLY_UP,
         gametypes.QINGGONG_STATE_WINGFLY_DOWN,
         gametypes.QINGGONG_STATE_WINGFLY_DASH,
         gametypes.QINGGONG_STATE_WINGFLY_LANDUP,
         gametypes.QINGGONG_STATE_WINGFLY_LEFT,
         gametypes.QINGGONG_STATE_WINGFLY_RIGHT,
         gametypes.QINGGONG_STATE_WINGFLY_BACK)

    def _check_NORMAL_ST(self):
        return True

    def _check_ON_VEHICLE_ST(self):
        if not self.player.vehicle:
            return False
        if hasattr(self.player.vehicle, 'canUseSkill'):
            return not self.player.vehicle.canUseSkill()
        return True

    def _check_RUN_ON_WATER_ST(self):
        return self.player.runOnWater > 0

    def _check_LOOKAT_ST(self):
        if self.player.model and hasattr(self.player.model, 'poser'):
            return getattr(self.player.model.poser, 'enableLookAt', False)
        return False

    def _check_BATCH_USE_ITEM_ST(self):
        if self.player and hasattr(self.player, 'batchUseItemData'):
            return self.player.batchUseItemData != None
        return False

    def _check_ISOLATE_MODE(self):
        return self.player.isolateType != gametypes.ISOLATE_TYPE_NONE

    def _check_WAIT_RIDE_TOGETHER_TELEPORT_OK_ST(self):
        return self.player.isWaitingRideTogether

    def _check_IN_DAN_DAO_ST(self):
        return self.player.inDanDao

    def _check_APPRENTICE_TRAIN_ST(self):
        if gameglobal.rds.configData.get('enableNewApprentice', False):
            if self.player.apprenticeTrainInfoEx and self.player.apprenticeTrainInfoEx[0] == self.player.id:
                return True
        elif self.player.apprenticeTrainInfo and self.player.apprenticeTrainInfo[0] == self.player.id:
            return True
        return False

    def _check_APPRENTICE_BE_TRAIN_ST(self):
        if gameglobal.rds.configData.get('enableNewApprentice', False):
            if self.player.apprenticeTrainInfoEx and self.player.apprenticeTrainInfoEx[1] == self.player.gbId:
                return True
        elif self.player.apprenticeTrainInfo and self.player.apprenticeTrainInfo[1] == self.player.gbId:
            return True
        return False

    def _check_SHUANGXIU_ST(self):
        if self.player.shuangxiuInfo:
            return True
        return False

    def _check_IN_PHASE_FB_ST(self):
        if not self.player.fbStatusList:
            return False
        for fbNo in self.player.fbStatusList:
            if FD.data.get(fbNo, {}).get('isPhaseFb', False):
                return True

        return False

    def _check_ATTACH_OTHER_ST(self):
        return self.player.isSkillAttachOther()

    def _check_BE_ATTACHED_ST(self):
        return self.player.isSkillBeAttached()

    def _check_FIGHT_OBSERVE_ST(self):
        return self.player.inFightObserve()

    def _check_TELEPORT_SPELL_ST(self):
        return self.player.teleportSpell

    def _check_TELEPORT_ACTION(self):
        return self.player.fashion.doingActionType() == action.TELEPORT_SPELL_ACTION

    def _check_IN_INTERACTIVE(self):
        return self.player.interactiveObjectEntId

    def _check_IN_BUF_NO_JUMP(self):
        return self.player.bufNoJump

    def _check_IN_MEI_HUO_ST(self):
        return self.player.inMeiHuo

    def _check_IN_FEAR_ST(self):
        return self.player.inFear

    def _check_IN_CHAO_FENG_ST(self):
        return self.player.inChaoFeng

    def _check_IN_FORBIDRIDEFLY_ST(self):
        return self.player.isForbidRideFly()

    def _check_IN_PUBG(self):
        return self.player.isInPUBG()

    def _check_IN_TEAM_SCENARIO_IN_FUBEN(self):
        if self.player.inFuben() and self.player.isTeammateInPlayScenarioWithGroupSingleEsc():
            return True
        return False

    def _cancel_IN_INTERACTIVE(self):
        if self._check_IN_INTERACTIVE():
            self.player.cell.quitInteractive()

    def _cancel_TELEPORT_SPELL_ST(self):
        if self._check_TELEPORT_SPELL_ST():
            if self.player.teleportCB:
                BigWorld.cancelCallback(self.player.teleportCB)
            if self.player.fashion._doingActionType in (action.TELEPORT_SPELL_ACTION,):
                self.player.fashion.stopAction()
            self.player.cancelTeleportSpell()
            self.player.showGameMsg(GMDD.data.TELEPORT_SPELL_CANCELED, ())

    def _cancel_WAIT_RIDE_TOGETHER_TELEPORT_OK_ST(self):
        if self._check_WAIT_RIDE_TOGETHER_TELEPORT_OK_ST():
            self.player.cell.enableCycleRideTogetherCheck(True)

    def _cancel_BATCH_USE_ITEM_ST(self):
        if self._check_BATCH_USE_ITEM_ST():
            self.player.cell.cancelBatchUseItem()

    def _cancel_JUMP_ST(self):
        if self._check_JUMP_ST():
            self.player.fashion.breakJump()

    def _cancel_FALL_ST(self):
        if self._check_FALL_ST():
            self.player.fashion.breakFall()

    def _cancel_DASH_ST(self):
        if self._check_DASH_ST():
            self.player.ap.switchToRun()

    def _cancel_SPELL_ST(self):
        if self.player.spellingType in [action.S_SPELLING]:
            self.player.cell.cancelSkill()

    def _cancel_MOVE_SPELL_ST(self):
        if self.player.spellingType in [action.S_SPELLING_CAN_MOVE]:
            self.player.cell.cancelSkill()

    def _cancel_GUIDE_ST(self):
        if self.player.isGuiding == const.GUIDE_TYPE_NO_MOVE:
            self.player.cell.cancelSkill()

    def _cancel_MOVE_GUIDE_ST(self):
        if self.player.isGuiding == const.GUIDE_TYPE_MOVE:
            self.player.cell.cancelSkill()

    def _cancel_ACTION_SPELL_ST(self):
        if self._check_ACTION_SPELL_ST():
            cellCmd.cancelAction()

    def _cancel_AUTO_PATHFINDING_ST(self):
        if self.player.checkPathfinding():
            self.player.cancelPathfinding()

    def _cancel_CHARGE_ST(self):
        pass

    def _cancel_IN_GROUP_FOLLOW(self):
        if self._check_IN_GROUP_FOLLOW():
            self.player.cell.cancelGroupFollow()

    def _cancel_RIDE_ST(self):
        if self._check_RIDE_ST():
            self.player.modelServer.leaveRideHB()
            self.player.cell.leaveRide()

    def _cancel_FLY_RIDE_ST(self):
        if self._check_FLY_RIDE_ST():
            self.player.cell.leaveRide()

    def _cancel_SWIM_RIDE_ST(self):
        if self._check_SWIM_RIDE_ST():
            self.player.modelServer.leaveRideHB()
            self.player.cell.leaveRide()

    def _cancel_WINGFLY_ST(self):
        if self._check_WINGFLY_ST():
            return self.player.cell.leaveWingFly()

    def _cancel_WINGFLY_AND_COMBAT_ST(self):
        if self._check_WINGFLY_AND_COMBAT_ST():
            return self.player.cell.leaveWingFly()

    def _cancel_WINGFLY_FLYRIDE_ST(self):
        if self._check_WINGFLY_FLYRIDE_ST():
            self.player.modelServer.leaveRideHB()
            self.player.cell.leaveRide()

    def _cancel_FISHING_ST(self):
        if self.player.inFishing() or self.player.inFishingReady() and gameglobal.rds.ui.fishing.isAuto:
            self.player.showGameMsg(GMDD.data.FISHING_BREAK, ())
            self.player.stopFish()

    def _cancel_FISHING_START_ST(self):
        if self.player.inFishingReady():
            self.player.showGameMsg(GMDD.data.FISHING_BREAK, ())
            self.player.stopFish()

    def _cancel_FOLLOW_TARGET_ST(self):
        if self._check_FOLLOW_TARGET_ST():
            self.player.ap.stopChasing()

    def _cancel_DA_ZUO_ST(self):
        if self._check_DA_ZUO_ST():
            self.player.cell.leaveDaZuo(False)

    def _cancel_AUTO_MOVE_ST(self):
        if self._check_AUTO_MOVE_ST():
            self.player.ap.stopAutoMove()

    def _cancel_HAND_CLIMB_ST(self):
        if self._check_HAND_CLIMB_ST():
            self.player.ap.endHandClimbNotifier('clientSM')

    def _cancel_WEAPON_IN_HAND_ST(self):
        if self._check_WEAPON_IN_HAND_ST():
            self.player.switchWeaponState(gametypes.WEAPON_HANDFREE, False)
            self.player.skillPlayer.endWeaponState = 0

    def _cancel_MAJOR_RIDE_ST(self):
        if self._check_MAJOR_RIDE_ST():
            self.player.cancelRideTogether()

    def _cancel_MINOR_RIDE_ST(self):
        if self._check_MINOR_RIDE_ST():
            self.player.cell.cancelRideTogether()

    def _cancel_COUPLE_EMOTE_HUG_ST(self):
        if self._check_COUPLE_EMOTE_HUG_ST():
            self.player.cell.cancelCoupleEmote()

    def _cancel_COUPLE_EMOTE_BE_HUG_ST(self):
        if self._check_COUPLE_EMOTE_BE_HUG_ST():
            self.player.cell.cancelCoupleEmote()

    def _cancel_COUPLE_EMOTE_APPLY_ST(self):
        self.player.cell.cancelCoupleEmoteApply()

    def _cancel_CARROUSEL_ST(self):
        if self._check_CARROUSEL_ST():
            self.player.cell.leaveCarrousel()

    def _cancel_WALK_ST(self):
        if self._check_WALK_ST():
            self.player.ap.switchToWalk(True)

    def _cancel_SOCIAL_ACTION_ST(self):
        if self._check_SOCIAL_ACTION_ST():
            if hasattr(self.player, 'fashion'):
                self.player.fashion.stopAction()
            if hasattr(self.player, 'emoteActionDone'):
                self.player.emoteActionCancel()

    def _cancel_SHOW_BACK_WEAR_ST(self):
        if self._check_SHOW_BACK_WEAR_ST():
            self.player.innerUpdateBackWear(True, False, False)

    def _cancel_SHOW_WAIST_WEAR_ST(self):
        if self._check_SHOW_WAIST_WEAR_ST():
            self.player.innerUpdateWaistWear(True, False, False)

    def _cancel_SHOW_WEAR_ACTION_ST(self):
        if self._check_SHOW_WEAR_ACTION_ST():
            self.player.fashion.stopActions()

    def _cancel_WINGFLY_DASH_ST(self):
        if self._check_WINGFLY_DASH_ST():
            cellCmd.endUpQinggongState()

    def _cancel_LOOKAT_ST(self):
        if self._check_LOOKAT_ST():
            self.player.modelServer.poseManager.stopPoseModel()

    def _cancel_OPEN_WEAR_ST(self):
        if self._check_OPEN_WEAR_ST():
            modelServer = self.player.modelServer
            modelServer.stopWearAction(True, modelServer.backwear)
            modelServer.stopWearAction(True, modelServer.waistwear)

    def _cancel_CLOSE_WEAR_ST(self):
        if self._check_CLOSE_WEAR_ST():
            modelServer = self.player.modelServer
            modelServer.stopWearAction(False, modelServer.backwear)
            modelServer.stopWearAction(False, modelServer.waistwear)

    def _cancel_APPRENTICE_TRAIN_ST(self):
        if self._check_APPRENTICE_TRAIN_ST():
            self.player.cancelApprenticeTraining()

    def _cancel_APPRENTICE_BE_TRAIN_ST(self):
        if self._check_APPRENTICE_BE_TRAIN_ST():
            self.player.cancelApprenticeTraining()

    def _cancel_SHUANGXIU_ST(self):
        if self._check_SHUANGXIU_ST():
            self.player.cancelShuangxiu()

    def _check_ROUND_TABLE_ST(self):
        return self.player.belongToRoundTable != 0

    def _cancel_ROUND_TABLE_ST(self):
        if self._check_ROUND_TABLE_ST():
            self.player.cell.leaveRoundTable()

    def _check_GUILD_SIT_ST(self):
        return self.player.isGuildSitInChair()

    def _cancel_GUILD_SIT_ST(self):
        if self.player.isGuildSitInChair():
            self.player.guildLeaveChair()

    def _check_OPEN_FULL_SCREEN_FITTING_ROOM_ST(self):
        if gameglobal.rds.ui.fullscreenFittingRoom.mediator or gameglobal.rds.ui.tuZhuang.med:
            return True
        return False

    def _cancel_OPEN_FULL_SCREEN_FITTING_ROOM_ST(self):
        if gameglobal.rds.ui.fullscreenFittingRoom.mediator:
            gameglobal.rds.ui.fullscreenFittingRoom.hide()
        if gameglobal.rds.ui.tuZhuang.med:
            gameglobal.rds.ui.tuZhuang.hide()

    def _check_WORLD_WAR_ST(self):
        return self.player.inWorldWarEx()

    def _check_FORCE_NAVIGATE_ST(self):
        return getattr(self.player, 'inForceNavigate', False)

    def _cancel_FORCE_NAVIGATE_ST(self):
        if self._check_FORCE_NAVIGATE_ST():
            self.player.inForceNavigate = False
            self.player.physics.fall = True

    def _check_FACE_EMOTE_ST(self):
        return self.player.curFaceEmoteId == 0 and getattr(self.player, 'faceEmoteXmlInfo', {}).get('faceEmotionAction', None)

    def _cancel_FACE_EMOTE_ST(self):
        if self._check_FACE_EMOTE_ST():
            self.player.endFaceEmote()

    def _check_PHOTO_ACTION_ST(self):
        return self.player.fashion.doingActionType() == action.PHOTO_ACTION

    def _cancel_PHOTO_ACTION_ST(self):
        if self._check_PHOTO_ACTION_ST():
            self.player.emoteActionCancel()

    def _check_EQUIP_FACE_EMOTE_ST(self):
        return self.player.curFaceEmoteId

    def _check_USING_PET_SKILL_ST(self):
        pet = self.player._getPet()
        if not pet:
            return False
        return pet.petSkillState in (gametypes.PET_SKILL_USING, gametypes.PET_SKILL_MOVING)

    def _cancel_EQUIP_FACE_EMOTE_ST(self):
        if self._check_EQUIP_FACE_EMOTE_ST():
            self.player.cell.resetCurFaceEmote()

    def _check_MULTICARRIER_READY_ST(self):
        return self.player.carrier.isReadyState() and self.player.carrier.has_key(self.player.id)

    def _check_MULTICARRIER_RUNNING_ST(self):
        return self.player.carrier.isRunningState() and self.player.carrier.has_key(self.player.id)

    def _cancel_MULTICARRIER_READY_ST(self):
        if self._check_MULTICARRIER_READY_ST():
            pass

    def _cancel_MULTICARRIER_RUNNING_ST(self):
        if self._check_MULTICARRIER_RUNNING_ST():
            pass

    def _cancel_AUTO_QUEST_ST(self):
        self.player.stopAutoQuest()
        self.player.autoSkill.stopSkillMacro()

    def _check_WING_WORLD_CARRIER(self):
        return self.player.isOnWingWorldCarrier()

    def _cancel_WING_WORLD_CARRIER(self):
        pass

    def _check_TRIAL_CLOTH_ST(self):
        return aspectHelper.getInstance().isInTrialState()

    def _cancel_TRIAL_CLOTH_ST(self):
        pass

    def _check_CQZZ_FLAG_PICKED_ST(self):
        p = BigWorld.player()
        from data import duel_config_data as DCD
        buffIds = DCD.data.get('cqzzFlagBuffID', {}).values()
        for buffId in buffIds:
            if p.statesServerAndOwn.has_key(buffId):
                return True

        return False
