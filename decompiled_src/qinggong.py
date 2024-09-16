#Embedded file name: /WORKSPACE/data/entities/client/helpers/qinggong.o
import math
import time
import BigWorld
import Sound
import Math
import const
import gameglobal
import gametypes
import commcalc
import formula
import gamelog
import action
import keys
import logicInfo
import utils
from sfx import keyboardEffect
from callbackHelper import Functor
import cellCmd
import wingWorldUtils
from gamestrings import gameStrings
from data import qinggong_cost_data as QCD
from cdata import game_msg_def_data as GMDD
from data import zaiju_data as ZJD
from data import sys_config_data as SYSCD
from data import physics_config_data as PCD
from data import ride_together_data as RTD
STATE_IDLE = 1
STATE_JUMPING = 2
STATE_DASH = 3
STATE_DASH_JUMPING = 4
STATE_TWICE_JUMPING = 5
STATE_DASH_TWICE_JUMPING = 6
STATE_SLIDE_DASH = 7
STATE_SLIDE_SLOW_FALLING = 8
STATE_SLIDE_FAST_FALLING = 9
STATE_COLLIDE_FALLING = 10
STATE_DASH_BIG_JUMPING = 401
STATE_RUSH_DOWN = 402
STATE_AUTO_JUMP = 403
STATE_DASH_AUTO_JUMP = 404
STATE_RUSH_DOWN_WEAPON_IN_HAND = 405
STATE_SLIDE_DASH_WEAPON_IN_HAND = 406
STATE_WINGFLY_IDLE = 11
STATE_WINGFLY_UP = 12
STATE_WINGFLY_DOWN = 13
STATE_WINGFLY_DASH = 14
STATE_WINGFLY_FAST_FALLING = 15
STATE_WINGFLY_LEFT = 16
STATE_WINGFLY_RIGHT = 17
STATE_WINGFLY_BACK = 18
STATE_IN_COMBAT_IDLE = 19
GO_DEFAULT = 0
DASH = 101
RUN_JUMP = 2
RUN_TWICE_JUMP = 3
DASH_JUMP = 4
GO_LEFT = 5
GO_RIGHT = 6
GO_BACK = 7
GO_FORWARD = 8
DASH_TWICE_JUMP = 9
SLIDE_DASH = 10
SLIDE_SLOW_FALL = 11
SLIDE_FAST_FALL = 12
AUTO_JUMP = 13
GO_WINGFLY_LANDUP = 14
DASH_BIG_JUMP = 202
DASH_AUTO_JUMP = 203
SLIDE_DASH_NORMAL = 110
SLIDE_DASH_WEAPON_IN_HAND = 111
GO_UP = 112
GO_DOWN = 113
GO_MOUSE = 114
GO_WINGFLY_UP = 15
GO_WINGFLY_DOWN = 16
GO_WINGFLY_LEFT = 17
GO_WINGFLY_RIGHT = 18
GO_WINGFLY_BACK = 19
GO_WINGFLY_DASH = 20
GO_WINGFLY_LANDDOWN = 21
EventStateMap = {GO_DEFAULT: STATE_IDLE,
 GO_LEFT: STATE_IDLE,
 GO_RIGHT: STATE_IDLE,
 GO_BACK: STATE_IDLE,
 GO_FORWARD: STATE_IDLE,
 DASH: STATE_DASH,
 RUN_JUMP: STATE_JUMPING,
 RUN_TWICE_JUMP: STATE_TWICE_JUMPING,
 DASH_JUMP: STATE_DASH_JUMPING,
 DASH_TWICE_JUMP: STATE_DASH_TWICE_JUMPING,
 SLIDE_DASH: STATE_SLIDE_DASH,
 SLIDE_SLOW_FALL: STATE_SLIDE_SLOW_FALLING,
 SLIDE_FAST_FALL: STATE_SLIDE_FAST_FALLING,
 GO_WINGFLY_UP: STATE_WINGFLY_UP,
 GO_WINGFLY_DOWN: STATE_WINGFLY_DOWN,
 GO_WINGFLY_LEFT: STATE_WINGFLY_LEFT,
 GO_WINGFLY_RIGHT: STATE_WINGFLY_RIGHT,
 GO_WINGFLY_BACK: STATE_WINGFLY_BACK,
 GO_WINGFLY_DASH: STATE_WINGFLY_DASH,
 GO_WINGFLY_LANDDOWN: STATE_WINGFLY_FAST_FALLING}
dirDict = {GO_WINGFLY_LEFT: GO_LEFT,
 GO_WINGFLY_RIGHT: GO_RIGHT,
 GO_WINGFLY_BACK: GO_BACK}
DO_QINGGONG_BY_STATE = {STATE_IDLE: (GO_LEFT,
              GO_RIGHT,
              GO_BACK,
              GO_FORWARD,
              DASH,
              RUN_JUMP,
              GO_MOUSE),
 STATE_DASH: (DASH_JUMP,
              GO_DEFAULT,
              GO_LEFT,
              GO_RIGHT,
              GO_BACK),
 STATE_JUMPING: (RUN_TWICE_JUMP,),
 STATE_DASH_JUMPING: (DASH_BIG_JUMP,),
 STATE_DASH_BIG_JUMPING: (DASH_TWICE_JUMP,),
 STATE_DASH_TWICE_JUMPING: (SLIDE_DASH, SLIDE_FAST_FALL, STATE_DASH_TWICE_JUMPING),
 STATE_SLIDE_SLOW_FALLING: (DASH_TWICE_JUMP,),
 STATE_WINGFLY_IDLE: (GO_WINGFLY_UP,
                      GO_WINGFLY_DOWN,
                      GO_WINGFLY_LEFT,
                      GO_WINGFLY_RIGHT,
                      GO_WINGFLY_BACK,
                      GO_WINGFLY_DASH,
                      GO_LEFT,
                      GO_RIGHT,
                      GO_BACK,
                      GO_FORWARD,
                      GO_WINGFLY_LANDDOWN,
                      GO_MOUSE),
 STATE_IN_COMBAT_IDLE: (GO_LEFT,
                        GO_RIGHT,
                        GO_BACK,
                        GO_FORWARD,
                        GO_UP,
                        GO_DOWN,
                        GO_MOUSE)}
EVENT_DEFAULT = 0
EVENT_SPACE_DOWN = 1
EVENT_S_DOWN = 2
EVENT_LEFT_DOWN = 3
EVENT_RIGHT_DOWN = 4
EVENT_BACK_DOWN = 5
EVENT_FORWARD_DOWN = 6
EVENT_FORWARD_UP = 7
EVENT_NONE = 8
EVENT_WINGFLY_UP = 9
EVENT_WINGFLY_DOWN = 10
EVENT_WINGFLY_LEFT = 11
EVENT_WINGFLY_RIGHT = 12
EVENT_WINGFLY_BACK = 13
EVENT_WINGFLY_DASH = 14
EVENT_WINGFLY_LANDUP = 15
EVENT_WINGFLY_LANDDOWN = 16
EVENT_DODGE_FORWARD_DOWN = 17
EVENT_WEAPON_FORWARD_DOWN = 18
EVENT_DODGE_MOUSE_DOWN = 19
clientFirstActions = {GO_LEFT: gametypes.QINGGONG_ROLL_LEFT,
 GO_RIGHT: gametypes.QINGGONG_ROLL_RIGHT,
 GO_BACK: gametypes.QINGGONG_ROLL_BACK,
 GO_FORWARD: gametypes.QINGGONG_ROLL_FORWARD,
 GO_UP: gametypes.QINGGONG_ROLL_UP,
 GO_DOWN: gametypes.QINGGONG_ROLL_DOWN,
 GO_MOUSE: gametypes.QINGGONG_ROLL_FORWARD}
QINGGONG_ACTION_TYPE = 1
QINGGONG_STATE_TYPE = 2

def switchToDodgeOrDash(jumpType, qinggongMgr):
    p = BigWorld.player()
    if p.getOperationMode() == gameglobal.MOUSE_MODE:
        enterDash(jumpType)
    else:
        switchToDodge(jumpType, qinggongMgr)


def switchToDodge(jumpType, qinggongMgr):
    player = BigWorld.player()
    if BigWorld.player().qinggongMgr.dismissManDown():
        if qinggongMgr._checkCandodge(jumpType):
            qinggongMgr._startJump(jumpType)
        else:
            player.updateActionKeyState()


def playDashStartAction(player):
    dashStartAction = player.fashion.getDashStartAction()
    if dashStartAction:
        player.fashion.stopAllActions()
        playSeq = []
        playSeq.append((dashStartAction,
         [],
         action.DASH_START_ACTION,
         1,
         1.0,
         None))
        player.physics.needPromotionVelY = False
        player.fashion.playActionWithFx(playSeq, action.DASH_START_ACTION, None, False, 0, 0)
        if player.inRidingHorse() and getattr(player.model, 'ride', None) and dashStartAction in player.model.ride.actionNameList():
            player.model.ride.action(dashStartAction)()
            player.playRideTogetherAction(dashStartAction)
        BigWorld.callback(player.fashion.getActionTime(dashStartAction) - 0.1, Functor(player.qinggongMgr._setmatcherCoupled, player, True))


def switchToDash(player, initDash = False, afterBigJump = False, dirType = GO_FORWARD, shieldPathFinding = False):
    if player.getOperationMode() == gameglobal.MOUSE_MODE and not player.isPathfinding:
        player.ap.updateDashYaw(dirType)
    if player.qinggongMgr._checkCanDash():
        player.qinggongMgr.jumpDashFlag = True
        if not player.inSwim and not afterBigJump:
            playDashStartAction(player)
        inRiding = hasattr(player, 'inRiding') and player.inRiding()
        qinggongState = inRiding and gametypes.QINGGONG_STATE_MOUNT_DASH or gametypes.QINGGONG_STATE_FAST_RUN
        lv = player.getQingGongSkillLv(qinggongState)
        gcd = QCD.data.get((qinggongState, lv)).get('gcd', 0)
        now = BigWorld.time()
        commonTotal = gcd
        commonTotal = max(0.0, commonTotal)
        commonCooldown = (commonTotal + now, commonTotal, qinggongState)
        logicInfo.commonCooldownWeaponSkill = commonCooldown
        player.qinggongState = qinggongState
        player.cancelWeaponTimerAndHangUpWeapon()
        if initDash:
            player.dashingInitTime = time.time()
        cellCmd.startQinggongState(qinggongState, player.position)
        player.isDashing = True
        if player.qinggongMgr.checkCanDashOnWater() and not player.inSwim and not inRiding:
            player.enterWaterHeight = 0
        player.ap.setUpSpeedMultiplier()
        if not getattr(player, 'isInsideWater'):
            player.setGravity(SYSCD.data.get('dashGravity', gametypes.DASH_GRAVITY))
        if player.qinggongMgr.dashStartFlag:
            gameglobal.rds.cam.enterDashFov()
        else:
            player.qinggongMgr.dashStartFlag = True
        if hasattr(player, 'inHiding') and player.inHiding():
            pass
        else:
            player.qinggongMgr.playThunderSound()
            player.qinggongMgr.playWindSound()
        player.spriteChangeToFollow(source=gametypes.SPRITE_MOVE_CHANGE_TO_FOLLOW_TYPE_DASH)
    else:
        player.ap.switchToRun()
    if not player.isPathfinding:
        player.updateActionKeyState()
    _isPathfinding = player.isPathfinding
    if player.isPathfinding and shieldPathFinding:
        player.isPathfinding = False
    result = player.stateMachine.checkMove()
    player.isPathfinding = _isPathfinding
    if result:
        player.ap.forwardMagnitude = 1.0
        if hasattr(player.am, 'applyRunRoll'):
            if player.enableApplyModelRoll():
                player.am.maxModelRoll = gameglobal.MAX_DASH_MODEL_ROLL
                player.am.rollRunHalfLife = gameglobal.ROLL_DASH_HALFLIFE
        player.ap.updateVelocity()


def switchToSlide(jumpType, qinggongMgr):
    owner = BigWorld.entity(qinggongMgr.ownerID)
    qinggongMgr.currJumpNum = jumpType
    cellCmd.startQinggongState(gametypes.QINGGONG_STATE_SLIDING, owner.position)


def completeDashStartAction(player, oldActionType):
    player.fashion.setDoingActionType(oldActionType)


def leaveDash(jumpType, qinggongMgr):
    owner = BigWorld.entity(qinggongMgr.ownerID)
    if owner.fashion.isPlayer:
        owner.ap.upwardMagnitude = 0
        if getattr(owner, 'isInsideWater', False):
            if not owner.inSwim and owner.qinggongMgr.getDistanceFromWater():
                if owner.qinggongMgr.getDistanceFromGround() - owner.qinggongMgr.getDistanceFromWater() > owner.getEnterWaterHeight():
                    owner.intoWater(True, owner.qinggongMgr.getDistanceFromWater())
        owner.enterWaterHeight = owner.getEnterWaterHeight()
    qinggongMgr._startJump(jumpType)


def stopDashAction(qinggongMgr):
    qinggongMgr.stopDashAction()


def enterRunJumpStatus(jumpType, qinggongMgr):
    if qinggongMgr._checkCanJumpUp(jumpType):
        qinggongMgr._startJump(jumpType)


def enterFallJumpStatus(jumpType, qinggongMgr):
    if qinggongMgr._checkCanFallJump(jumpType):
        qinggongMgr._startJump(jumpType)


def enterRunTwiceJumpStatus(jumpType, qinggongMgr):
    if qinggongMgr._checkCanRunTwiceJump():
        qinggongMgr._startJump(jumpType)


def enterDashJumpStatus(jumpType, qinggongMgr):
    if qinggongMgr._checkCanDashJump():
        owner = BigWorld.entity(qinggongMgr.ownerID)
        owner.dashingJumpStartTime = time.time()
        if owner.fashion.isPlayer and owner.isQuickDashJump():
            jumpType = DASH_BIG_JUMP
        qinggongMgr._startJump(jumpType)


def enterDashBigJumpStatus(jumpType, qinggongMgr):
    if qinggongMgr._checkCanJumpUp(jumpType):
        if qinggongMgr._checkCanDashBigJump():
            qinggongMgr._startJump(jumpType)


def enterDashTwiceJumpStatus(jumpType, qinggongMgr):
    if qinggongMgr._checkCanJumpUp(jumpType):
        if qinggongMgr._checkCanDashTwiceJump():
            qinggongMgr._startJump(jumpType)


def enterFallStatus(jumpType, qinggongMgr):
    qinggongMgr._startJump(jumpType)


def enterFastFallStatus(jumpType, qinggongMgr):
    qinggongMgr._startJump(jumpType)


def enterSlideSprintOrDash(jumpType, qinggongMgr):
    if qinggongMgr._checkGoDash():
        enterDash(jumpType)
    else:
        enterSlideSprint(jumpType, qinggongMgr)


def enterDash(jumpType):
    p = BigWorld.player()
    if checkDashEP():
        switchToDash(BigWorld.player(), True, dirType=jumpType)
    else:
        if not formula.inDotaBattleField(p.mapID):
            p.showGameMsg(GMDD.data.QINGGONG_NOT_ENOUGH, ())
        return


def checkDashEP():
    p = BigWorld.player()
    now = time.time()
    if p.lastEpRegenTime == 0.0:
        epRegen = 0
    else:
        timeInterval = now - p.lastEpRegenTime
        if p.inCombat:
            delta = p.combatEpRegen
        else:
            delta = p.nonCombatEpRegenFix
        if p.qinggongState in gametypes.QINGGONG_CNT_COST:
            _, _, _, cntCost = getQinggongData(p.qinggongState, p.inCombat)
            delta -= cntCost / 2.0
        epRegen = delta * timeInterval
    qinggongState = p.inRiding() and gametypes.QINGGONG_STATE_MOUNT_DASH or gametypes.QINGGONG_STATE_FAST_RUN
    preMin2, preMax2, fstCost2, _ = getQinggongData(qinggongState, p.inCombat)
    if p.ep + epRegen >= preMin2:
        return True
    return False


def enterSlideSprint(jumpType, qinggongMgr):
    if qinggongMgr._checkCanSlideSprint():
        qinggongMgr._startJump(jumpType)


def enterWeapnSlideSprint(jumpType, qinggongMgr):
    if qinggongMgr._checkCanWeapnSlideSprint():
        qinggongMgr._startJump(jumpType)


def leaveSlideSprint(qinggongMgr):
    qinggongMgr.setState(STATE_DASH_TWICE_JUMPING)
    enterFallStatus(SLIDE_SLOW_FALL, qinggongMgr)
    cellCmd.endUpQinggongState()


def getQinggongData(qstype, inCombat = False):
    p = BigWorld.player()
    lv = p.getQingGongSkillLv(qstype)
    if not lv:
        lv = 1
    qcd = QCD.data.get((qstype, lv))
    if not qcd:
        return None
    if inCombat:
        costData = qcd.get('combatCost', (0, 0))
    else:
        costData = qcd.get('nonCombatCost', (0, 0))
    qstype = p.qinggongState
    if qstype in gametypes.HORSE_QINGGONG:
        equipment = p.equipment.get(gametypes.EQU_PART_RIDE)
        if equipment:
            adjustPer = utils.getHorseQinggongAdjust(equipment)
            costData = (int(costData[0] * adjustPer), int(costData[1] * adjustPer))
    if qstype in gametypes.QINGGONG_WINGFLY_STATES:
        if p.inFlyTypeFlyRide():
            equipment = p.equipment.get(gametypes.EQU_PART_RIDE)
        else:
            equipment = p.equipment.get(gametypes.EQU_PART_WINGFLY)
        if equipment:
            adjustPer = utils.getWingQinggongAdjust(equipment)
            costData = (int(costData[0] * adjustPer), int(costData[1] * adjustPer))
    limit = qcd.get('limit', (0, 0))
    return limit + costData


def enterCollideFall(qinggongMgr):
    owner = BigWorld.entities.get(qinggongMgr.ownerID)
    fallAction = owner.fashion.action.getFallRunDownAction(owner.fashion)
    if fallAction == None:
        return
    if owner.fashion.doingActionType() not in [action.FALLEND_ACTION]:
        if keys.CAPS_GROUND in owner.am.matchCaps:
            owner.fashion.playAction([fallAction], action.FALL_ACTION)


def enterWingFlyUp(jumpType, qinggongMgr):
    if qinggongMgr.checkCanWingFlyUp():
        qinggongMgr._startJump(jumpType)
        return True
    return False


def enterWingFlyLandUp(jumpType, qinggongMgr):
    if qinggongMgr.checkCanWingFlyLandUp():
        qinggongMgr._startJump(jumpType)
        return True
    return False


def enterWingFlyDown(jumpType, qinggongMgr):
    if qinggongMgr.checkCanWingFlyDown():
        gamelog.debug('enterWingFlyDown:', jumpType)
        qinggongMgr._startJump(jumpType)
        return True
    return False


def enterWingFlyLeft(jumpType, qinggongMgr):
    if qinggongMgr.checkCanWingFlyLeft():
        qinggongMgr._startJump(jumpType)
        return True
    return False


def enterWingFlyRight(jumpType, qinggongMgr):
    if qinggongMgr.checkCanWingFlyRight():
        qinggongMgr._startJump(jumpType)
        return True
    return False


def enterWingFlyBack(jumpType, qinggongMgr):
    if qinggongMgr.checkCanWingFlyBack():
        qinggongMgr._startJump(jumpType)
        return True
    return False


def enterWingFlyDash(jumpType, qinggongMgr, shieldPathFinding = False):
    owner = BigWorld.entities.get(qinggongMgr.ownerID)
    if owner and owner.getOperationMode() == gameglobal.MOUSE_MODE:
        dirType = dirDict.get(jumpType, None)
        if dirType:
            owner.ap.updateDashYaw(dirType)
            jumpType = GO_WINGFLY_DASH
    if qinggongMgr.checkCanWingFlyDash(shieldPathFinding=shieldPathFinding):
        gamelog.debug('enterWingFlyDash')
        qinggongMgr._startJump(jumpType)
        return True
    return False


def enterWingFlyFastFall(jumpType, qinggongMgr):
    if qinggongMgr.enterWingFlyFastFall():
        qinggongMgr._startJump(jumpType)
        return True
    return False


eventStateTable = {EVENT_DEFAULT: {STATE_DASH: Functor(leaveDash, GO_DEFAULT)},
 EVENT_LEFT_DOWN: {STATE_IDLE: Functor(switchToDodgeOrDash, GO_LEFT),
                   STATE_IN_COMBAT_IDLE: Functor(switchToDodge, GO_LEFT),
                   STATE_DASH: Functor(switchToDodgeOrDash, GO_LEFT),
                   STATE_WINGFLY_IDLE: Functor(enterWingFlyDash, GO_WINGFLY_LEFT)},
 EVENT_RIGHT_DOWN: {STATE_IDLE: Functor(switchToDodgeOrDash, GO_RIGHT),
                    STATE_IN_COMBAT_IDLE: Functor(switchToDodge, GO_RIGHT),
                    STATE_DASH: Functor(switchToDodgeOrDash, GO_RIGHT),
                    STATE_WINGFLY_IDLE: Functor(enterWingFlyDash, GO_WINGFLY_RIGHT)},
 EVENT_BACK_DOWN: {STATE_IDLE: Functor(switchToDodgeOrDash, GO_BACK),
                   STATE_IN_COMBAT_IDLE: Functor(switchToDodge, GO_BACK),
                   STATE_DASH: Functor(switchToDodgeOrDash, GO_BACK),
                   STATE_WINGFLY_IDLE: Functor(enterWingFlyDash, GO_WINGFLY_BACK)},
 EVENT_FORWARD_DOWN: {STATE_IN_COMBAT_IDLE: Functor(switchToDodge, GO_FORWARD),
                      STATE_WINGFLY_IDLE: Functor(switchToDodge, GO_FORWARD),
                      STATE_DASH_TWICE_JUMPING: Functor(enterSlideSprint, SLIDE_DASH),
                      STATE_JUMPING: Functor(enterSlideSprint, SLIDE_DASH),
                      STATE_DASH_JUMPING: Functor(enterSlideSprint, SLIDE_DASH),
                      STATE_TWICE_JUMPING: Functor(enterSlideSprint, SLIDE_DASH),
                      STATE_IDLE: Functor(enterSlideSprint, SLIDE_DASH),
                      STATE_DASH_BIG_JUMPING: Functor(enterSlideSprint, SLIDE_DASH),
                      STATE_RUSH_DOWN: Functor(enterSlideSprint, SLIDE_DASH),
                      STATE_AUTO_JUMP: Functor(enterSlideSprint, SLIDE_DASH)},
 EVENT_DODGE_FORWARD_DOWN: {STATE_IN_COMBAT_IDLE: Functor(switchToDodge, GO_FORWARD),
                            STATE_DASH_TWICE_JUMPING: Functor(enterSlideSprint, SLIDE_DASH_NORMAL),
                            STATE_JUMPING: Functor(enterSlideSprint, SLIDE_DASH_NORMAL),
                            STATE_DASH_JUMPING: Functor(enterSlideSprint, SLIDE_DASH_NORMAL),
                            STATE_TWICE_JUMPING: Functor(enterSlideSprint, SLIDE_DASH_NORMAL),
                            STATE_IDLE: Functor(enterSlideSprintOrDash, SLIDE_DASH_NORMAL),
                            STATE_DASH_BIG_JUMPING: Functor(enterSlideSprint, SLIDE_DASH_NORMAL),
                            STATE_AUTO_JUMP: Functor(enterSlideSprint, SLIDE_DASH_NORMAL),
                            STATE_RUSH_DOWN: Functor(enterSlideSprint, SLIDE_DASH_NORMAL),
                            STATE_WINGFLY_IDLE: Functor(enterWingFlyDash, GO_WINGFLY_DASH)},
 EVENT_DODGE_MOUSE_DOWN: {STATE_IN_COMBAT_IDLE: Functor(switchToDodge, GO_MOUSE),
                          STATE_DASH_TWICE_JUMPING: Functor(enterSlideSprint, SLIDE_DASH_NORMAL),
                          STATE_JUMPING: Functor(enterSlideSprint, SLIDE_DASH_NORMAL),
                          STATE_DASH_JUMPING: Functor(enterSlideSprint, SLIDE_DASH_NORMAL),
                          STATE_TWICE_JUMPING: Functor(enterSlideSprint, SLIDE_DASH_NORMAL),
                          STATE_IDLE: Functor(enterSlideSprintOrDash, SLIDE_DASH_NORMAL),
                          STATE_DASH_BIG_JUMPING: Functor(enterSlideSprint, SLIDE_DASH_NORMAL),
                          STATE_AUTO_JUMP: Functor(enterSlideSprint, SLIDE_DASH_NORMAL),
                          STATE_RUSH_DOWN: Functor(enterSlideSprint, SLIDE_DASH_NORMAL),
                          STATE_WINGFLY_IDLE: Functor(enterWingFlyDash, GO_WINGFLY_DASH)},
 EVENT_WEAPON_FORWARD_DOWN: {STATE_IN_COMBAT_IDLE: Functor(enterWeapnSlideSprint, SLIDE_DASH_WEAPON_IN_HAND),
                             STATE_IDLE: Functor(enterWeapnSlideSprint, SLIDE_DASH_WEAPON_IN_HAND),
                             STATE_DASH_TWICE_JUMPING: Functor(enterWeapnSlideSprint, SLIDE_DASH_WEAPON_IN_HAND),
                             STATE_JUMPING: Functor(enterWeapnSlideSprint, SLIDE_DASH_WEAPON_IN_HAND),
                             STATE_DASH_JUMPING: Functor(enterWeapnSlideSprint, SLIDE_DASH_WEAPON_IN_HAND),
                             STATE_TWICE_JUMPING: Functor(enterWeapnSlideSprint, SLIDE_DASH_WEAPON_IN_HAND),
                             STATE_DASH_BIG_JUMPING: Functor(enterWeapnSlideSprint, SLIDE_DASH_WEAPON_IN_HAND),
                             STATE_RUSH_DOWN_WEAPON_IN_HAND: Functor(enterWeapnSlideSprint, SLIDE_DASH_WEAPON_IN_HAND)},
 EVENT_SPACE_DOWN: {STATE_IDLE: Functor(enterRunJumpStatus, RUN_JUMP),
                    STATE_IN_COMBAT_IDLE: Functor(enterRunJumpStatus, RUN_JUMP),
                    STATE_DASH: Functor(enterDashJumpStatus, DASH_JUMP),
                    STATE_JUMPING: Functor(enterRunTwiceJumpStatus, RUN_TWICE_JUMP),
                    STATE_DASH_JUMPING: Functor(enterDashBigJumpStatus, DASH_BIG_JUMP),
                    STATE_DASH_BIG_JUMPING: Functor(enterDashTwiceJumpStatus, DASH_TWICE_JUMP),
                    STATE_DASH_TWICE_JUMPING: Functor(enterDashTwiceJumpStatus, DASH_TWICE_JUMP),
                    STATE_SLIDE_DASH: Functor(leaveSlideSprint),
                    STATE_COLLIDE_FALLING: Functor(enterCollideFall),
                    STATE_RUSH_DOWN: Functor(enterDashTwiceJumpStatus, DASH_TWICE_JUMP),
                    STATE_AUTO_JUMP: Functor(enterDashTwiceJumpStatus, DASH_TWICE_JUMP),
                    STATE_DASH_AUTO_JUMP: Functor(enterDashTwiceJumpStatus, DASH_TWICE_JUMP)},
 EVENT_S_DOWN: {STATE_DASH_TWICE_JUMPING: Functor(enterFastFallStatus, SLIDE_FAST_FALL),
                STATE_SLIDE_DASH: Functor(enterFastFallStatus, SLIDE_FAST_FALL),
                STATE_DASH_BIG_JUMPING: Functor(enterFastFallStatus, SLIDE_FAST_FALL),
                STATE_RUSH_DOWN: Functor(enterFastFallStatus, SLIDE_FAST_FALL)},
 EVENT_FORWARD_UP: {},
 EVENT_NONE: {STATE_DASH: Functor(enterFallJumpStatus, DASH_AUTO_JUMP),
              STATE_IDLE: Functor(enterFallJumpStatus, AUTO_JUMP)},
 EVENT_WINGFLY_UP: {STATE_WINGFLY_IDLE: Functor(enterWingFlyUp, GO_WINGFLY_UP),
                    STATE_IN_COMBAT_IDLE: Functor(switchToDodge, GO_UP)},
 EVENT_WINGFLY_DOWN: {STATE_WINGFLY_IDLE: Functor(enterWingFlyDown, GO_WINGFLY_DOWN),
                      STATE_IN_COMBAT_IDLE: Functor(switchToDodge, GO_DOWN)},
 EVENT_WINGFLY_LEFT: {STATE_WINGFLY_IDLE: Functor(enterWingFlyLeft, GO_WINGFLY_LEFT),
                      STATE_IN_COMBAT_IDLE: Functor(switchToDodge, GO_LEFT)},
 EVENT_WINGFLY_RIGHT: {STATE_WINGFLY_IDLE: Functor(enterWingFlyRight, GO_WINGFLY_RIGHT),
                       STATE_IN_COMBAT_IDLE: Functor(switchToDodge, GO_RIGHT)},
 EVENT_WINGFLY_BACK: {STATE_WINGFLY_IDLE: Functor(enterWingFlyBack, GO_WINGFLY_BACK),
                      STATE_IN_COMBAT_IDLE: Functor(switchToDodge, GO_BACK)},
 EVENT_WINGFLY_DASH: {STATE_WINGFLY_IDLE: Functor(enterWingFlyDash, GO_WINGFLY_DASH),
                      STATE_IN_COMBAT_IDLE: Functor(switchToDodge, GO_FORWARD)},
 EVENT_WINGFLY_LANDUP: {STATE_WINGFLY_IDLE: Functor(enterWingFlyLandUp, GO_WINGFLY_LANDUP)},
 EVENT_WINGFLY_LANDDOWN: {STATE_WINGFLY_IDLE: Functor(enterWingFlyFastFall, GO_WINGFLY_LANDDOWN)}}

class QingGongMgr(object):

    def __init__(self, ownerID = None):
        self.state = STATE_IDLE
        self.rushTop = False
        self.actionType = gametypes.QINGGONG_ACT_DEFAULT
        if ownerID is None:
            ownerID = BigWorld.player().id
        self.ownerID = ownerID
        self.currJumpNum = 0
        self.lastTimeEventHappen = {GO_LEFT: -999.0,
         GO_RIGHT: -999.0,
         GO_BACK: -999.0,
         GO_FORWARD: -999.0,
         GO_UP: -999.0,
         GO_DOWN: -999.0,
         GO_MOUSE: -999.0}
        self.jumpDashFlag = False
        self.dashStartFlag = True
        self.playWindSoundId = 0
        self.wingFlyUpCallBack = None

    def playWindSound(self):
        path = 'fx/char/Shared/fly_wind'
        owner = BigWorld.entity(self.ownerID)
        if not owner.fashion.isPlayer:
            return
        if self.playWindSoundId:
            Sound.stopFx(self.playWindSoundId)
        self.playWindSoundId = gameglobal.rds.sound.playFx(path, owner.position, True, owner)
        gamelog.debug('playDashSound:', self.playWindSoundId)

    def stopWindSound(self):
        gamelog.debug('stopWindSound:', self.playWindSoundId)
        Sound.stopFx(self.playWindSoundId)
        self.playWindSoundId = 0

    def playThunderSound(self):
        path = 'fx/char/Shared/sprint_ready_a_thunder'
        owner = BigWorld.entity(self.ownerID)
        if not owner.fashion.isPlayer:
            return
        gameglobal.rds.sound.playFx(path, owner.position, False, owner)

    def _checkLimitQinggongInMapConfig(self, qinggongType, actionOrState, showErrorMsg = True):
        p = BigWorld.player()
        if p.gmMode:
            return True
        owner = BigWorld.entity(self.ownerID)
        mapId = formula.getMapId(owner.spaceNo)
        limitDict = dict()
        if actionOrState == 1:
            limitDict = gametypes.FB_QINGGONG_ACTION_LIMIT_DICT
        elif actionOrState == 2:
            limitDict = gametypes.FB_QINGGONG_STATE_LIMIT_DICT
        for lv, limitQinggongTyps in limitDict.iteritems():
            if qinggongType in limitQinggongTyps:
                if formula.mapLimit(formula.LIMIT_QINGONG_LV, mapId, lv):
                    showErrorMsg and p.showGameMsg(GMDD.data.NO_QINGGONG_IN_MAP, ())
                    return False

        return True

    def _checkCandodge(self, qinggongType):
        gamelog.debug('_checkCandodge', qinggongType)
        owner = BigWorld.entity(self.ownerID)
        p = BigWorld.player()
        if p.handClimb:
            return False
        if not self._getFlag(gametypes.QINGGONG_FLAG_ROLL):
            p.chatToEventEx('你没有学会翻滚', const.CHANNEL_COLOR_RED)
            return False
        if p.inSwim:
            p.chatToEventEx('处于游泳不能翻滚', const.CHANNEL_COLOR_RED)
            return False
        if BigWorld.time() - self.lastTimeEventHappen[qinggongType] < gameglobal.DOUBLE_CLICK_INTERVAL:
            p.showGameMsg(GMDD.data.OPERATION_FREQUENT, ())
            return False
        if owner.fashion.doingActionType() in [action.MOVING_ACTION, action.AFTERMOVE_ACTION, action.FAINT_ACTION]:
            return False
        if qinggongType not in DO_QINGGONG_BY_STATE.get(self.state, ()):
            p.chatToEventEx('DO_QINGGONG_BY_STATE返回', const.CHANNEL_COLOR_RED)
            return False
        if logicInfo.isInDodgeCoolDownTime():
            p.chatToEventEx('使用轻功,公共cd中', const.CHANNEL_COLOR_RED)
            return False
        if p.isWaitSkillReturn:
            p.showGameMsg(GMDD.data.OPERATION_FREQUENT, ())
            return False
        tp = clientFirstActions[qinggongType]
        preMin, preMax, fstCost, cntCost = getQinggongData(tp, owner.inCombat)
        now = time.time()
        if owner.lastEpRegenTime == 0.0:
            epRegen = 0
        else:
            timeInterval = now - owner.lastEpRegenTime
            if owner.inCombat:
                delta = owner.combatEpRegen
            else:
                delta = owner.nonCombatEpRegenFix
            if owner.qinggongState in gametypes.QINGGONG_CNT_COST:
                delta -= cntCost / 2.0
            epRegen = delta * timeInterval
        if owner.ep + epRegen < preMin or owner.ep + epRegen > preMax > 0 or owner.ep + epRegen < fstCost:
            if not formula.inDotaBattleField(getattr(p, 'mapID', 0)):
                p.showGameMsg(GMDD.data.QINGGONG_NOT_ENOUGH, ())
            p.updateActionKeyState()
            return False
        if owner.skillPlayer.castLoop:
            p.chatToEventEx('castLoop返回', const.CHANNEL_COLOR_RED)
            return False
        if owner.limitQinggongByBianshen(tp):
            owner.showGameMsg(GMDD.data.ZAIJU_FORBID_DODGE, ZJD.data.get(owner._getZaijuNo(), {}).get('name', ''))
            return False
        if hasattr(owner, 'inRiding') and owner.inRiding():
            return False
        if commcalc.getBitDword(owner.flags, gametypes.FLAG_NO_QINGGONG) > 0:
            p.showGameMsg(GMDD.data.QINGGONG_FORBIDDEN, ())
            return False
        if commcalc.getBitDword(owner.flags, gametypes.FLAG_NO_QINGGONG_BODY):
            p.showGameMsg(GMDD.data.QINGGONG_BODY_FORBIDDEN, ())
            return False
        if commcalc.getBitDword(owner.flags, gametypes.FLAG_NO_QINGGONG_DOUBLE_JUMP) > 0:
            p.showGameMsg(GMDD.data.QINGGONG_FORBIDDEN, ())
            return False
        if not self._checkLimitQinggongInMapConfig(qinggongType, QINGGONG_ACTION_TYPE):
            return False
        if qinggongType in (GO_FORWARD, GO_MOUSE):
            if not owner.inCombat:
                return False
            if not owner.stateMachine.checkStatus(const.CT_ROLL_FORWARD) or not owner.checkTempGroupFollow():
                gamelog.debug('stateMachine_QINGGONG返回')
                return False
        else:
            if not owner.checkTempGroupFollow():
                return False
            if owner.inCombat:
                if not owner.stateMachine.checkStatus(const.CT_ROLL_LEFT_RIGHT_IN_COMBAT):
                    gamelog.debug('stateMachine_QINGGONG返回')
                    return False
            elif not owner.stateMachine.checkStatus(const.CT_ROLL_LEFT_RIGHT_NOT_IN_COMBAT):
                gamelog.debug('stateMachine_QINGGONG返回')
                return False
            if not owner.stateMachine.checkStatus(const.CT_ROLL_LEFT_RIGHT):
                gamelog.debug('stateMachine_QINGGONG返回')
                return False
        if p.inFly:
            if not owner.stateMachine.checkStatus(const.CT_WINGFLY_DODGE):
                gamelog.debug('stateMachine_QINGGONG返回')
                return False
        if p.isChargeKeyDown:
            cellCmd.cancelSkill()
            p.isChargeKeyDown = False
        if owner.inFishing():
            owner.showGameMsg(GMDD.data.FISHING_BREAK, ())
            owner.stopFish()
        if not gameglobal.AUTOSKILL_FLAG:
            p.autoSkill.stop()
        return True

    def _checkCanDash(self):
        owner = BigWorld.entity(self.ownerID)
        qinggongState = hasattr(owner, 'inRiding') and owner.inRiding() and gametypes.QINGGONG_STATE_MOUNT_DASH or gametypes.QINGGONG_STATE_FAST_RUN
        if qinggongState == gametypes.QINGGONG_STATE_MOUNT_DASH:
            if not self._getFlag(gametypes.QINGGONG_FLAG_RIDE_DASH):
                owner.chatToEventEx('你没有学会马儿的疾奔', const.CHANNEL_COLOR_RED)
                return False
            if commcalc.getBitDword(owner.flags, gametypes.FLAG_NO_QINGGONG_MOUNT):
                owner.showGameMsg(GMDD.data.QINGGONG_MOUNT_FORBIDDEN, ())
                return False
        elif not self._getFlag(gametypes.QINGGONG_FLAG_DASH):
            owner.chatToEventEx('你没有学会疾奔', const.CHANNEL_COLOR_RED)
            return False
        actionType = owner.fashion.doingActionType()
        if actionType in [action.CAST_ACTION,
         action.CAST_MOVING_ACTION,
         action.MOVING_ACTION,
         action.AFTERMOVE_ACTION,
         action.FAINT_ACTION]:
            str = ''
            if actionType == action.CAST_ACTION:
                str = gameStrings.STR_CAST_ACTION
            elif actionType == action.CAST_MOVING_ACTION:
                str = gameStrings.STR_CAST_MOVING_ACTION
            elif actionType == action.MOVING_ACTION:
                str = gameStrings.STR_MOVING_ACTION
            elif actionType == action.AFTERMOVE_ACTION:
                str = gameStrings.STR_AFTERMOVE_ACTION
            elif actionType == action.FAINT_ACTION:
                str = gameStrings.STR_FAINT_ACTION
            owner.showGameMsg(GMDD.data.QINGGONG_FORBIDDEN_CURRENT_STATE, (str,))
            return False
        if not logicInfo.isUseableSkill(qinggongState):
            return False
        if owner.inCombat:
            return False
        if owner.handClimb:
            return False
        if owner.limitQinggongByBianshen(qinggongState):
            return False
        if commcalc.getBitDword(owner.flags, gametypes.FLAG_NO_QINGGONG):
            return False
        inRiding = hasattr(owner, 'inRiding') and owner.inRiding()
        if not inRiding and commcalc.getBitDword(owner.flags, gametypes.FLAG_NO_QINGGONG_BODY):
            owner.showGameMsg(GMDD.data.QINGGONG_BODY_FORBIDDEN, ())
            return False
        if commcalc.getBitDword(owner.flags, gametypes.FLAG_NO_QINGGONG_DOUBLE_JUMP) > 0:
            owner.showGameMsg(GMDD.data.QINGGONG_FORBIDDEN, ())
            return False
        if owner.skillPlayer.castLoop:
            owner.showGameMsg(GMDD.data.MOVE_FORBIDDEN_USE_SKILL, ())
            return False
        if hasattr(owner, 'stateMachine') and not owner.stateMachine.checkStatus(const.CT_DASH):
            return False
        if owner.inBoothing():
            return False
        if not self._checkLimitQinggongInMapConfig(gametypes.QINGGONG_STATE_FAST_RUN, QINGGONG_STATE_TYPE):
            return False
        mapId = formula.getMapId(owner.spaceNo)
        if formula.inDotaBattleField(mapId) and getattr(owner, 'isInBfDotaChooseHero', False):
            return False
        return True

    def _getFlag(self, key):
        owner = BigWorld.entity(self.ownerID)
        return owner.isQingGongSkillLearned(key)

    def _startJump(self, jumpNum):
        self._real_startJump(jumpNum)

    def _real_startJump(self, jumpNum):
        owner = BigWorld.entity(self.ownerID)
        self.currJumpNum = jumpNum
        qinggongState = None
        otherActions = {RUN_TWICE_JUMP: gametypes.QINGGONG_DOUBLE_JUMP,
         DASH_JUMP: hasattr(owner, 'inRiding') and owner.inRiding() and gametypes.QINGGONG_MOUNT_JUMP or gametypes.QINGGONG_FAST_RUN_JUMP,
         DASH_BIG_JUMP: hasattr(owner, 'inRiding') and owner.inRiding() and gametypes.QINGGONG_MOUNT_JUMP or gametypes.QINGGONG_FAST_RUN_BIG_JUMP,
         DASH_TWICE_JUMP: gametypes.QINGGONG_FAST_RUN_DOUBLE_JUMP,
         SLIDE_SLOW_FALL: gametypes.QINGGONG_SLOW_DOWN,
         SLIDE_FAST_FALL: gametypes.QINGGONG_FAST_DOWN,
         GO_WINGFLY_LANDDOWN: gametypes.QINGGONG_WINGFLY_FAST_DOWN,
         AUTO_JUMP: gametypes.QINGGONG_AUTO_JUMP,
         DASH_AUTO_JUMP: gametypes.QINGGONG_DASH_AUTO_JUMP}
        if self.currJumpNum in clientFirstActions.keys():
            tp = clientFirstActions[self.currJumpNum]
            lv = owner.getQingGongSkillLv(tp)
            qcd = QCD.data.get((tp, lv))
            gcd = qcd.get('gcd', 0.0)
            time = BigWorld.time()
            commonCooldown = (gcd + time, gcd, tp)
            logicInfo.commonCooldownDodge = commonCooldown
            self.doQinggongPlayerAction(tp)
            self.setQingGongActionType(tp)
            cellCmd.startQinggongAction(tp, owner.position)
        elif self.currJumpNum == DASH:
            if not owner.isDashing:
                owner.isDashing = True
        elif self.currJumpNum == GO_DEFAULT:
            owner.isDashing = False
            if owner.fashion.isPlayer:
                owner.restoreGravity()
                owner.ap.setUpSpeedMultiplier()
                owner.ap.updateVelocity()
                self.stopWindSound()
                owner.jumpState = gametypes.DEFAULT_JUMP
                owner.qinggongState = gametypes.QINGGONG_STATE_DEFAULT
                gameglobal.rds.cam.leaveDashFov()
                owner.qinggongMgr.stopDashAction()
            if not owner.qinggongMgr.isJumping():
                owner.qinggongMgr.setState(STATE_IDLE)
        elif self.currJumpNum == RUN_JUMP:
            if owner.fashion.isPlayer:
                owner.ap.cancelskill()
                if owner.stateMachine.checkStatus(const.CT_JUMP) and owner.checkTempGroupFollow() or owner.isFalling:
                    self.setState(STATE_JUMPING)
                    owner.isStartJumping = True
                    owner.cell.startJumping(True)
                    owner.ap.physics.upSpeedAttenu = PCD.data.get('runUpSpeedAttenu', gametypes.RUNUP_SPEED_ATTENU)
                    owner.fashion.jump(True)
                    owner.begingDropForBlood(gametypes.DROP_FOR_BLOOD_OTHER)
        else:
            if self.currJumpNum in otherActions.keys():
                cellCmd.startQinggongAction(otherActions[self.currJumpNum], owner.position)
                return
            if self.currJumpNum == SLIDE_DASH:
                if BigWorld.player().equipment[gametypes.EQU_PART_WINGFLY]:
                    self.rushTop = False
                    if not self.checkCanWingFlyDash():
                        return
                    if not owner.stateMachine.checkStatus(const.CT_OPEN_WINGFLY_CAST):
                        return
                    BigWorld.player().ap.needForceEndQingGong = True
                    owner.qinggongState = gametypes.QINGGONG_STATE_WINGFLY_DASH
                    qinggongState = gametypes.QINGGONG_STATE_WINGFLY_DASH
                else:
                    return
            elif self.currJumpNum == SLIDE_DASH_NORMAL:
                if owner.qinggongMgr.getDistanceFromGround() < 1.0:
                    return
                qinggongState = gametypes.QINGGONG_STATE_FAST_SLIDING
            elif self.currJumpNum == SLIDE_DASH_WEAPON_IN_HAND:
                if owner.qinggongMgr.getDistanceFromGround() < 1.0:
                    return
                qinggongState = gametypes.QINGGONG_STATE_FAST_SLIDING_WEAPON_IN_HAND
            elif self.currJumpNum == GO_WINGFLY_LANDUP:
                qinggongState = gametypes.QINGGONG_STATE_WINGFLY_LANDUP
            elif self.currJumpNum == GO_WINGFLY_UP:
                qinggongState = gametypes.QINGGONG_STATE_WINGFLY_UP
            elif self.currJumpNum == GO_WINGFLY_DOWN:
                qinggongState = gametypes.QINGGONG_STATE_WINGFLY_DOWN
            elif self.currJumpNum == GO_WINGFLY_LEFT:
                qinggongState = gametypes.QINGGONG_STATE_WINGFLY_LEFT
            elif self.currJumpNum == GO_WINGFLY_RIGHT:
                qinggongState = gametypes.QINGGONG_STATE_WINGFLY_RIGHT
            elif self.currJumpNum == GO_WINGFLY_BACK:
                qinggongState = gametypes.QINGGONG_STATE_WINGFLY_BACK
            elif self.currJumpNum == GO_WINGFLY_DASH:
                self.rushTop = False
                qinggongState = gametypes.QINGGONG_STATE_WINGFLY_DASH
        cellCmd.startQinggongState(qinggongState, owner.position)

    def dismissManDown(self):
        owner = BigWorld.entity(self.ownerID)
        p = BigWorld.player()
        if owner == p and owner.inManDownState():
            if not self._getFlag(gametypes.QINGGONG_FLAG_DISMISS_MAN_DOWN):
                p.chatToEventEx('你没有学会解控起身', const.CHANNEL_COLOR_RED)
                return False
            preMin, preMax, fstCost, cntCost = getQinggongData(gametypes.QINGGONG_STATE_MAN_DOWN, owner.inCombat)
            now = time.time()
            if owner.lastEpRegenTime == 0.0:
                epRegen = 0
            else:
                timeInterval = now - owner.lastEpRegenTime
                if owner.inCombat:
                    delta = owner.combatEpRegen
                else:
                    delta = owner.nonCombatEpRegenFix
                if owner.qinggongState in gametypes.QINGGONG_CNT_COST:
                    delta -= cntCost / 2.0
                epRegen = delta * timeInterval
            if owner.ep + epRegen < preMin or owner.ep + epRegen > preMax > 0 or owner.ep + epRegen < fstCost:
                if not formula.inDotaBattleField(getattr(p, 'mapID', 0)):
                    p.showGameMsg(GMDD.data.QINGGONG_NOT_ENOUGH, ())
            else:
                p.cell.dismissManDown()
            return False
        else:
            return True

    def _setClientControl(self, bControl):
        owner = BigWorld.entity(self.ownerID)
        owner.clientControl = bControl

    def jumpEndCallBack(self, bControl):
        self._setClientControl(bControl)

    def _dodgeCallBack(self, gravity, actionName):
        owner = BigWorld.entity(self.ownerID)
        owner.setGravity(gravity)
        if owner == BigWorld.player():
            BigWorld.player().doQingGongActionState = False
            gameglobal.rds.ui.actionbar.checkAllSkillStat(gameglobal.SKILL_STAT_NO_SKILL)
        if owner.life == gametypes.LIFE_DEAD:
            return
        self.setQingGongActionType(gametypes.QINGGONG_ACT_DEFAULT)
        owner.delayCancelWeaponTimerAndHangUpWeapon()
        if owner.fashion.isPlayer:
            owner.updateUseSkillKeyState()
            owner.fashion.forceUpdateMovingNotifier()
        if owner.inFly:
            self.stopWingFlyModelAction()

    def doFuncByEvent(self, event, timeStamp = 0):
        func = eventStateTable.get(event, {}).get(self.state, None)
        gamelog.debug('bgf:state', event, self.state, getattr(func, 'fn', None))
        if func is not None:
            owner = BigWorld.entity(self.ownerID)
            if owner == BigWorld.player():
                owner.clearHoldingSkills()
            return func(self)
        return False

    def setState(self, state, forceUpdate = False):
        owner = BigWorld.entity(self.ownerID)
        if state in [STATE_IDLE, STATE_WINGFLY_IDLE, STATE_IN_COMBAT_IDLE] and not forceUpdate:
            if owner.canFly():
                if owner.inCombat:
                    self.state = STATE_IN_COMBAT_IDLE
                else:
                    self.state = STATE_WINGFLY_IDLE
            elif owner.inCombat:
                self.state = STATE_IN_COMBAT_IDLE
            else:
                self.state = STATE_IDLE
            return
        self.state = state

    def _checkCanRunTwiceJump(self):
        p = BigWorld.player()
        if not self._getFlag(gametypes.QINGGONG_FLAG_RUN_TWICE_JUMP):
            p.chatToEventEx('你没有学会二段跳', const.CHANNEL_COLOR_RED)
            return False
        if p.inRiding():
            p.chatToEventEx('骑马不能二段跳', const.CHANNEL_COLOR_RED)
            return False
        if not self._checkLimitQinggongInMapConfig(gametypes.QINGGONG_DOUBLE_JUMP, QINGGONG_ACTION_TYPE):
            return False
        return True

    def _checkCanDashBigJump(self):
        p = BigWorld.player()
        if p.inRiding():
            return False
        if p.inSwim:
            return False
        dist = self.getDistanceFromWater()
        if dist and dist < 1.0 and self.isJumping():
            return False
        if not self._getFlag(gametypes.QINGGONG_FLAG_DASH_JUMP):
            p.chatToEventEx('你没有学会疾奔跳', const.CHANNEL_COLOR_RED)
            return False
        if commcalc.getBitDword(p.flags, gametypes.FLAG_NO_QINGGONG_DOUBLE_JUMP) > 0:
            p.showGameMsg(GMDD.data.QINGGONG_FORBIDDEN, ())
            return False
        return True

    def _checkCanDashTwiceJump(self):
        p = BigWorld.player()
        if p.inRiding():
            return False
        if p.inSwim:
            return False
        dist = self.getDistanceFromWater()
        if dist and dist < 1.0 and self.isJumping():
            return False
        if self.state == STATE_DASH_TWICE_JUMPING:
            if not self._getFlag(gametypes.QINGGONG_FLAG_DASH_MULTI_JUMP):
                p.chatToEventEx('你没有学会疾奔多段跳', const.CHANNEL_COLOR_RED)
                return False
        elif not self._getFlag(gametypes.QINGGONG_FLAG_DASH_TWICE_JUMP):
            p.chatToEventEx('你没有学会疾奔二段跳', const.CHANNEL_COLOR_RED)
            return False
        if commcalc.getBitDword(p.flags, gametypes.FLAG_NO_QINGGONG_DOUBLE_JUMP) > 0:
            p.showGameMsg(GMDD.data.QINGGONG_FORBIDDEN, ())
            return False
        return True

    def _checkCanJumpUp(self, qinggongType):
        p = BigWorld.player()
        if getattr(p, 'bufNoJump', False):
            p.showGameMsg(GMDD.data.BUFF_NO_JUMP, ())
            return False
        return True

    def _checkCanFallJump(self, qinggongType):
        p = BigWorld.player()
        if qinggongType in (DASH_AUTO_JUMP, AUTO_JUMP):
            if not self._getFlag(gametypes.QINGGONG_FLAG_AUTO_JUMP):
                return False
        if commcalc.getBitDword(p.flags, gametypes.FLAG_NO_QINGGONG_DOUBLE_JUMP) > 0:
            return False
        if not p.stateMachine.checkStatus(const.CT_AUTO_JUMP):
            return False
        return True

    def _checkCanDashJump(self):
        p = BigWorld.player()
        if p.inRiding():
            if not self._getFlag(gametypes.QINGGONG_FLAG_RIDE_DASH_JUMP):
                p.chatToEventEx('你没有学会马儿的疾奔和跳跃', const.CHANNEL_COLOR_RED)
                return False
            if commcalc.getBitDword(p.flags, gametypes.FLAG_NO_QINGGONG_MOUNT):
                p.showGameMsg(GMDD.data.QINGGONG_MOUNT_FORBIDDEN, ())
                return False
            if commcalc.getBitDword(p.flags, gametypes.FLAG_NO_QINGGONG_DOUBLE_JUMP) > 0:
                p.showGameMsg(GMDD.data.QINGGONG_FORBIDDEN, ())
                return False
        elif not self._getFlag(gametypes.QINGGONG_FLAG_DASH_JUMP):
            p.chatToEventEx('你没有学会疾奔跳', const.CHANNEL_COLOR_RED)
            return False
        if commcalc.getBitDword(p.flags, gametypes.FLAG_NO_QINGGONG_DOUBLE_JUMP) > 0:
            p.showGameMsg(GMDD.data.QINGGONG_FORBIDDEN, ())
            return False
        if p.inSwim:
            return False
        if p.inCombat:
            return False
        return True

    def _checkGoDash(self):
        p = BigWorld.player()
        if p.inSwim:
            return False
        if p.inCombat:
            return False
        if p.isDashing:
            return False
        if p.canFly():
            return False
        if self.getDistanceFromGround() < 0.4:
            return True
        return False

    def _checkCanSlideSprint(self):
        p = BigWorld.player()
        if not self._getFlag(gametypes.QINGGONG_FLAG_SLIDE_DASH):
            p.chatToEventEx('你没有学会冲刺', const.CHANNEL_COLOR_RED)
            return False
        if p.inSwim:
            return False
        if p.inRiding():
            return False
        if p.inCombat:
            return False
        if commcalc.getBitDword(p.flags, gametypes.FLAG_NO_QINGGONG):
            return False
        if commcalc.getBitDword(p.flags, gametypes.FLAG_NO_QINGGONG_BODY):
            p.showGameMsg(GMDD.data.QINGGONG_BODY_FORBIDDEN, ())
            return False
        if commcalc.getBitDword(p.flags, gametypes.FLAG_NO_QINGGONG_DOUBLE_JUMP) > 0:
            p.showGameMsg(GMDD.data.QINGGONG_FORBIDDEN, ())
            return False
        if utils.limitSprintByZaiju(p):
            p.showGameMsg(GMDD.data.QINGGONG_FORBIDDEN, ())
            return False
        distanceFromWater = self.getDistanceFromWater()
        if distanceFromWater and distanceFromWater < 2:
            return False
        distanceFromGround = self.getDistanceFromGround()
        if distanceFromGround and distanceFromGround < 1.5:
            return False
        if not self._checkLimitQinggongInMapConfig(gametypes.QINGGONG_STATE_FAST_SLIDING, QINGGONG_STATE_TYPE):
            return False
        if not p.stateMachine.checkStatus(const.CT_SLIDE_DASH) or not p.checkTempGroupFollow():
            return False
        return True

    def _checkCanWeapnSlideSprint(self):
        p = BigWorld.player()
        if not self._getFlag(gametypes.QINGGONG_FLAG_SLIDE_DASH_IN_WEAPON):
            p.chatToEventEx('你没有学会携带武器冲刺', const.CHANNEL_COLOR_RED)
            return False
        if p.inSwim:
            return False
        if p.inRiding():
            return False
        if commcalc.getBitDword(p.flags, gametypes.FLAG_NO_QINGGONG):
            return False
        if commcalc.getBitDword(p.flags, gametypes.FLAG_NO_QINGGONG_BODY):
            p.showGameMsg(GMDD.data.QINGGONG_BODY_FORBIDDEN, ())
            return False
        if commcalc.getBitDword(p.flags, gametypes.FLAG_NO_QINGGONG_DOUBLE_JUMP) > 0:
            p.showGameMsg(GMDD.data.QINGGONG_FORBIDDEN, ())
            return False
        if utils.limitSprintByZaiju(p):
            p.showGameMsg(GMDD.data.QINGGONG_FORBIDDEN, ())
            return False
        distanceFromWater = self.getDistanceFromWater()
        if distanceFromWater and distanceFromWater < 2:
            return False
        distanceFromGround = self.getDistanceFromGround()
        if distanceFromGround and distanceFromGround < 1.5:
            return False
        fallAction = None
        if p.inRiding():
            fallAction = getattr(p.fashion.action, 'getHorseFallRunDownAction')(p.fashion)
        else:
            fallAction = p.fashion.action.getFallRunDownAction(p.fashion)
        if fallAction and fallAction in p.model.queue:
            return False
        if not self._checkLimitQinggongInMapConfig(gametypes.QINGGONG_STATE_FAST_SLIDING_WEAPON_IN_HAND, QINGGONG_STATE_TYPE):
            return False
        if not p.stateMachine.checkStatus(const.CT_SLIDE_DASH) or not p.checkTempGroupFollow():
            return False
        return True

    def checkCanWingFly(self):
        owner = BigWorld.entity(self.ownerID)
        if not self._checkWingValid():
            return False
        if not self._getFlag(gametypes.QINGGONG_FLAG_FLY):
            owner.chatToEventEx('你没有学会翅膀飞行', const.CHANNEL_COLOR_RED)
            return False
        if not owner.gmMode and formula.mapLimit(formula.LIMIT_WINGFLY, formula.getMapId(owner.spaceNo)) and not owner._checkWWArmyCanFlyRide():
            owner.showGameMsg(GMDD.data.FLY_FORBID_IN_MAP, ())
            return False
        return True

    def checkCanFlyRideUp(self):
        owner = BigWorld.entity(self.ownerID)
        if not owner.equipment.get(gametypes.EQU_PART_RIDE).haveTalent(gametypes.RIDE_TALENT_FLYRIDE):
            owner.showGameMsg(GMDD.data.RIDE_DONT_HAS_TALENT, (const.RIDE_WING_TALENT_FLY_TEXT,))
            return False
        if not owner.gmMode and formula.mapLimit(formula.LIMIT_WINGFLY, formula.getMapId(owner.spaceNo)) and not owner._checkWWArmyCanFlyRide():
            return False
        if commcalc.getBitDword(owner.flags, gametypes.FLAG_NO_QINGGONG_WINFLY):
            owner.showGameMsg(GMDD.data.QINGGONG_WINFLY_FORBIDDEN, ())
            return False
        if commcalc.getBitDword(owner.flags, gametypes.FLAG_NO_QINGGONG_DOUBLE_JUMP) > 0:
            owner.showGameMsg(GMDD.data.QINGGONG_FORBIDDEN, ())
            return False
        return True

    def checkCanRideSwim(self):
        owner = BigWorld.entity(self.ownerID)
        equip = owner.equipment.get(gametypes.EQU_PART_RIDE)
        if not equip:
            return False
        return True

    def _checkWingValid(self):
        owner = BigWorld.entity(self.ownerID)
        if hasattr(owner, 'equipment'):
            wingEquip = owner.equipment.get(gametypes.EQU_PART_WINGFLY)
            if wingEquip == const.CONT_EMPTY_VAL:
                return False
            if wingEquip.isExpireTTL():
                owner.showGameMsg(GMDD.data.USE_ITEM_WING_EXPIRED, ())
                return False
        return True

    def checkCanWingFlyDash(self, shieldPathFinding = False):
        owner = BigWorld.entity(self.ownerID)
        if not owner.canFly() and not self._checkWingValid():
            return False
        if not self._getFlag(gametypes.QINGGONG_FLAG_WINGFLY_DASH):
            owner.chatToEventEx('你没有学会翅膀疾飞', const.CHANNEL_COLOR_RED)
            return False
        if not self._getFlag(gametypes.QINGGONG_FLAG_OPEN_WING_IN_AIR):
            owner.chatToEventEx('你没有学会空中展翅', const.CHANNEL_COLOR_RED)
            return False
        if commcalc.getBitDword(owner.flags, gametypes.FLAG_NO_QINGGONG_WINFLY):
            owner.showGameMsg(GMDD.data.QINGGONG_WINFLY_FORBIDDEN, ())
            return False
        if commcalc.getBitDword(owner.flags, gametypes.FLAG_NO_QINGGONG_DOUBLE_JUMP) > 0:
            owner.showGameMsg(GMDD.data.QINGGONG_FORBIDDEN, ())
            return False
        if not owner.gmMode and formula.mapLimit(formula.LIMIT_WINGFLY, formula.getMapId(owner.spaceNo)) and not owner._checkWWArmyCanFlyRide():
            owner.showGameMsg(GMDD.data.FLY_FORBID_IN_MAP, ())
            return False
        if not self._checkLimitQinggongInMapConfig(gametypes.QINGGONG_STATE_WINGFLY_DASH, QINGGONG_STATE_TYPE):
            return False
        _isPathfinding = None
        if owner and hasattr(owner, 'isPathfinding'):
            _isPathfinding = owner.isPathfinding
            if owner.isPathfinding and shieldPathFinding:
                owner.isPathfinding = False
        result = not owner.gmMode == 1 and not owner.checkWingFlyDash()
        if shieldPathFinding:
            owner.isPathfinding = _isPathfinding
        if result:
            return False
        p = BigWorld.player()
        warCityId = p.getWingWarCityId()
        if warCityId and wingWorldUtils.isInAirDefenseRange(p.position, warCityId) and p.wingWorldMiniMap.airStoneEnergy:
            p.showGameMsg(GMDD.data.FORBIDDEN_FLY_IN_AIR_DEFENCE, ())
            return False
        return True

    def checkCanDashOnWater(self):
        if not self._getFlag(gametypes.QINGGONG_FLAG_DASH_ON_WATER):
            return False
        p = BigWorld.player()
        if commcalc.getBitDword(p.flags, gametypes.FLAG_NO_QINGGONG_DOUBLE_JUMP) > 0:
            p.showGameMsg(GMDD.data.QINGGONG_FORBIDDEN, ())
            return False
        return True

    def enterWingFlyFastFall(self):
        return True

    def checkCanWingFlyUp(self):
        owner = BigWorld.entity(self.ownerID)
        if not self._checkWingValid():
            if owner.canFly():
                pass
            else:
                return False
        if commcalc.getBitDword(owner.flags, gametypes.FLAG_NO_QINGGONG_DOUBLE_JUMP) > 0:
            owner.showGameMsg(GMDD.data.QINGGONG_FORBIDDEN, ())
            return False
        if not owner.checkWingFlyDash():
            return False
        if not self._getFlag(gametypes.QINGGONG_FLAG_WINGFLY_UP):
            owner.chatToEventEx('你没有学会翅膀疾升', const.CHANNEL_COLOR_RED)
            return False
        return True

    def checkCanWingFlyLandUp(self):
        owner = BigWorld.entity(self.ownerID)
        if not owner.gmMode and formula.mapLimit(formula.LIMIT_WINGFLY, formula.getMapId(owner.spaceNo)) and not owner._checkWWArmyCanFlyRide():
            owner.showGameMsg(GMDD.data.FLY_FORBID_IN_MAP, ())
            return False
        if not self._checkWingValid():
            return False
        if not self._getFlag(gametypes.QINGGONG_FLAG_WINGFLY_LANDUP):
            owner.chatToEventEx('你没有学会翅膀展翅疾升', const.CHANNEL_COLOR_RED)
            return False
        if commcalc.getBitDword(owner.flags, gametypes.FLAG_NO_QINGGONG_DOUBLE_JUMP) > 0:
            owner.showGameMsg(GMDD.data.QINGGONG_FORBIDDEN, ())
            return False
        if not owner.stateMachine.checkStatus(const.CT_OPEN_WINGFLY_CAST):
            return False
        return True

    def checkCanQingGongPathFinding(self):
        if not self._getFlag(gametypes.QINGGONG_FLAG_AUTO_PATHFINDING):
            return False
        return True

    def checkCanWingFlyDown(self):
        owner = BigWorld.entity(self.ownerID)
        if not self._checkWingValid():
            if owner.canFly():
                pass
            else:
                return False
        if not self._getFlag(gametypes.QINGGONG_FLAG_WINGFLY_UP):
            owner.chatToEventEx('你没有学会翅膀急升急降', const.CHANNEL_COLOR_RED)
            return False
        if commcalc.getBitDword(owner.flags, gametypes.FLAG_NO_QINGGONG_DOUBLE_JUMP) > 0:
            owner.showGameMsg(GMDD.data.QINGGONG_FORBIDDEN, ())
            return False
        if not owner.checkWingFlyDash():
            return False
        if not owner.gmMode and formula.mapLimit(formula.LIMIT_WINGFLY, formula.getMapId(owner.spaceNo)) and not owner._checkWWArmyCanFlyRide():
            owner.showGameMsg(GMDD.data.FLY_FORBID_IN_MAP, ())
            return False
        return True

    def checkCanWingFlyLeft(self):
        owner = BigWorld.entity(self.ownerID)
        if commcalc.getBitDword(owner.flags, gametypes.FLAG_NO_QINGGONG_DOUBLE_JUMP) > 0:
            owner.showGameMsg(GMDD.data.QINGGONG_FORBIDDEN, ())
            return False
        if not owner.checkWingFlyDash():
            return False
        if not owner.gmMode and formula.mapLimit(formula.LIMIT_WINGFLY, formula.getMapId(owner.spaceNo)) and not owner._checkWWArmyCanFlyRide():
            owner.showGameMsg(GMDD.data.FLY_FORBID_IN_MAP, ())
            return False
        return True

    def checkCanWingFlyRight(self):
        owner = BigWorld.entity(self.ownerID)
        if commcalc.getBitDword(owner.flags, gametypes.FLAG_NO_QINGGONG_DOUBLE_JUMP) > 0:
            owner.showGameMsg(GMDD.data.QINGGONG_FORBIDDEN, ())
            return False
        if not owner.checkWingFlyDash():
            return False
        if not owner.gmMode and formula.mapLimit(formula.LIMIT_WINGFLY, formula.getMapId(owner.spaceNo)) and not owner._checkWWArmyCanFlyRide():
            owner.showGameMsg(GMDD.data.FLY_FORBID_IN_MAP, ())
            return False
        return True

    def checkCanWingFlyBack(self):
        owner = BigWorld.entity(self.ownerID)
        if commcalc.getBitDword(owner.flags, gametypes.FLAG_NO_QINGGONG_DOUBLE_JUMP) > 0:
            owner.showGameMsg(GMDD.data.QINGGONG_FORBIDDEN, ())
            return False
        if not owner.checkWingFlyDash():
            return False
        if not owner.gmMode and formula.mapLimit(formula.LIMIT_WINGFLY, formula.getMapId(owner.spaceNo)) and not owner._checkWWArmyCanFlyRide():
            owner.showGameMsg(GMDD.data.FLY_FORBID_IN_MAP, ())
            return False
        return True

    def isJumping(self):
        owner = BigWorld.entity(self.ownerID)
        return owner.jumpActionMgr.jumpPhase != -1

    def _isFaceToWall(self):
        owner = BigWorld.entity(self.ownerID)
        startPos = (owner.position[0], owner.position[1] + owner.model.height, owner.position[2])
        endPos = startPos + self._getFaceDir() * 1
        if BigWorld.collide(owner.spaceID, startPos, endPos):
            return True
        else:
            return False

    def _getFaceDir(self):
        owner = BigWorld.entity(self.ownerID)
        return Math.Vector3(math.sin(owner.yaw), 0, math.cos(owner.yaw))

    def set_rushTop(self, bRushTop):
        owner = BigWorld.entity(self.ownerID)
        self.rushTop = bRushTop
        soundPath = 'fx/char/'
        modelId = owner.fashion.modelID
        soundPath = soundPath + str(modelId) + '/kongshou/flyjump_rush_go_a'
        gameglobal.rds.sound.playFx(soundPath, owner.position, False, owner)
        owner.ap.updateVelocity()

    def setQingGongActionType(self, actType):
        self.actionType = actType

    def doQinggongPlayerAction(self, actType):
        gamelog.debug('doQinggongPlayerAction', actType)
        owner = BigWorld.entity(self.ownerID)
        owner.model.unlockSpine()
        oldGravity = owner.physics.gravity
        actions = []
        duration = 0.0
        startActionName = None
        stopActionName = None
        owner.setGravity(SYSCD.data.get('dashGravity', gametypes.DASH_GRAVITY))
        fashion = owner.fashion
        if not fashion.action:
            return
        isMoveAct = True
        fourDirRoll = False
        if owner.getOperationMode() == gameglobal.MOUSE_MODE:
            cam = gameglobal.rds.cam.cc
            if actType == gametypes.QINGGONG_ROLL_LEFT:
                owner.ap.setYaw(cam.direction.yaw - math.pi / 2, True)
                self.lastTimeEventHappen[GO_LEFT] = BigWorld.time()
                fourDirRoll = True
            elif actType == gametypes.QINGGONG_ROLL_RIGHT:
                owner.ap.setYaw(cam.direction.yaw + math.pi / 2, True)
                self.lastTimeEventHappen[GO_RIGHT] = BigWorld.time()
                fourDirRoll = True
            elif actType == gametypes.QINGGONG_ROLL_BACK:
                owner.ap.setYaw(cam.direction.yaw - math.pi, True)
                self.lastTimeEventHappen[GO_BACK] = BigWorld.time()
                fourDirRoll = True
            elif actType == gametypes.QINGGONG_ROLL_FORWARD:
                if self.currJumpNum == GO_MOUSE:
                    result = BigWorld.getCursorPosInWorld(owner.spaceID, 1000, False, (gameglobal.TREEMATTERKINDS, gameglobal.GLASSMATTERKINDS))
                    if result[0] != None:
                        direction = result[0] - owner.position
                        owner.ap.setYaw(direction.yaw)
                    self.lastTimeEventHappen[GO_MOUSE] = BigWorld.time()
                else:
                    owner.ap.setYaw(cam.direction.yaw, True)
                    self.lastTimeEventHappen[GO_FORWARD] = BigWorld.time()
                fourDirRoll = True
            elif actType == gametypes.QINGGONG_ROLL_UP:
                owner.ap.setYaw(cam.direction.yaw, True)
                self.lastTimeEventHappen[GO_UP] = BigWorld.time()
            elif actType == gametypes.QINGGONG_ROLL_DOWN:
                owner.ap.setYaw(cam.direction.yaw, True)
                self.lastTimeEventHappen[GO_DOWN] = BigWorld.time()
            startActionName = fashion.getRollFollowStartAction()
            stopActionName = fashion.getRollFollowStopAction()
            if fourDirRoll and owner.realSchool == const.SCHOOL_YECHA:
                isMoveAct = False
                self.doDstQingGongPosition(8.0)
        elif actType == gametypes.QINGGONG_ROLL_LEFT:
            startActionName = fashion.getRollLeftStartAction()
            stopActionName = fashion.getRollLeftStopAction()
            self.lastTimeEventHappen[GO_LEFT] = BigWorld.time()
        elif actType == gametypes.QINGGONG_ROLL_RIGHT:
            startActionName = fashion.getRollRightStartAction()
            stopActionName = fashion.getRollRightStopAction()
            self.lastTimeEventHappen[GO_RIGHT] = BigWorld.time()
        elif actType == gametypes.QINGGONG_ROLL_BACK:
            startActionName = fashion.getRollBackStartAction()
            stopActionName = fashion.getRollBackStopAction()
            self.lastTimeEventHappen[GO_BACK] = BigWorld.time()
        elif actType == gametypes.QINGGONG_ROLL_FORWARD:
            startActionName = fashion.getRollFollowStartAction()
            stopActionName = fashion.getRollFollowStopAction()
            self.lastTimeEventHappen[GO_FORWARD] = BigWorld.time()
            if owner.realSchool == const.SCHOOL_YECHA:
                isMoveAct = False
                self.doDstQingGongPosition(8.0)
        elif actType == gametypes.QINGGONG_ROLL_UP:
            startActionName = fashion.getRollUpStartAction()
            stopActionName = fashion.getRollUpStopAction()
            self.lastTimeEventHappen[GO_FORWARD] = BigWorld.time()
        elif actType == gametypes.QINGGONG_ROLL_DOWN:
            startActionName = fashion.getRollDownStartAction()
            stopActionName = fashion.getRollDownStopAction()
            self.lastTimeEventHappen[GO_FORWARD] = BigWorld.time()
        if startActionName:
            duration = fashion.getActionTime(startActionName)
            actions.append((startActionName,
             None,
             isMoveAct,
             action.ROLL_ACTION))
        if stopActionName:
            actions.append((stopActionName,
             None,
             0,
             action.ROLLSTOP_ACTION))
        if owner.school == const.SCHOOL_YECHA:
            if owner.weaponState in (gametypes.WEAPON_MIDATTACH_WITH_ZHUSHOU, gametypes.WEAPON_MIDATTACH_WITH_ZHUSHOU_LEFT, gametypes.WEAPON_MIDATTACH_WITH_ZHUSHOU_RIGHT):
                if owner.modelServer.rightWeaponModel:
                    owner.modelServer.rightWeaponModel.detachRightToLeft()
                owner.switchWeaponState(gametypes.WEAPON_DOUBLEATTACH, False)
        if getattr(owner, 'castSkillBusy', None):
            owner.castSkillBusy = True
        owner.fashion.stopAllActions()
        self.setQingGongActionType(actType)
        func = Functor(self._dodgeCallBack, oldGravity, stopActionName)
        BigWorld.callback(duration + 0.05, func)
        followMovementHalfLife = SYSCD.data.get('followMovementHalfLife', 0.0)
        BigWorld.callback(followMovementHalfLife + 1.0, Functor(self.setCameraFollowHalfLife, 0.0))
        self.setCameraFollowHalfLife(followMovementHalfLife)
        owner.fashion.playActionSequence2(owner.model, actions, action.ROLL_ACTION)
        self.playWingFlyModelAction([startActionName, stopActionName])
        if owner == BigWorld.player():
            BigWorld.player().doQingGongActionState = True
            gameglobal.rds.ui.actionbar.checkAllSkillStat(gameglobal.SKILL_STAT_NO_SKILL)
            gameglobal.rds.tutorial.onCheckAction(actType)

    def doDstQingGongPosition(self, dist):
        player = BigWorld.player()
        time = 0.5
        if hasattr(player.physics, 'setDisplacement'):
            speed = dist / time
            ap = player.ap
            ap.setSpeed(speed)
            ap.displacementSpeed = speed
            player.physics.setDisplacement(speed, time, self._approachTowardTarget)
            return
        theta = 0
        yaw = BigWorld.dcursor().yaw
        dstPos = utils.getRelativePosition(player.position, yaw, theta, dist)
        dstPos = Math.Vector3(dstPos[0], dstPos[1], dstPos[2])
        speed = dist / time
        ap = player.ap
        ap.setSpeed(speed)
        player.physics.maxVelocity = 0
        ap.beginForceMoveWithCallback(dstPos, self._approachTowardTarget, 1)

    def _approachTowardTarget(ispin, success):
        player = BigWorld.player()
        ap = player.ap
        ap.setSpeed(player.speed[gametypes.SPEED_MOVE] / 60.0)
        ap._endForceMove(success)
        player.updateActionKeyState()
        player.isAscending = False
        ap.displacementSpeed = None

    def setCameraFollowHalfLife(self, halfLife):
        if hasattr(BigWorld.camera(), 'followMovementHalfLife'):
            BigWorld.camera().followMovementHalfLife = halfLife

    def doQinggongAction(self, actType):
        owner = BigWorld.entity(self.ownerID)
        if not owner or not owner.inWorld:
            return
        if not owner.model:
            return
        owner.model.unlockSpine()
        func = None
        gamelog.debug('doQinggongAction', actType)
        actions = []
        if actType in [gametypes.QINGGONG_ROLL_LEFT,
         gametypes.QINGGONG_ROLL_RIGHT,
         gametypes.QINGGONG_ROLL_BACK,
         gametypes.QINGGONG_ROLL_FORWARD]:
            if owner.fashion.isPlayer:
                return
            func = owner.fashion.forceUpdateMovingNotifier
            startActionName = None
            stopActionName = None
            duration = 0.0
            fashion = owner.fashion
            if actType == gametypes.QINGGONG_ROLL_LEFT:
                startActionName = fashion.action.getRollLeftStartAction(fashion)
                stopActionName = fashion.action.getRollLeftStopAction(fashion)
            elif actType == gametypes.QINGGONG_ROLL_RIGHT:
                startActionName = fashion.action.getRollRightStartAction(fashion)
                stopActionName = fashion.action.getRollRightStopAction(fashion)
            elif actType == gametypes.QINGGONG_ROLL_BACK:
                startActionName = fashion.action.getRollBackStartAction(fashion)
                stopActionName = fashion.action.getRollBackStopAction(fashion)
            elif actType == gametypes.QINGGONG_ROLL_FORWARD:
                startActionName = fashion.action.getRollFollowStartAction(fashion)
                stopActionName = fashion.action.getRollFollowStopAction(fashion)
            if startActionName:
                duration = fashion.getActionTime(startActionName)
                actions.append((startActionName,
                 None,
                 1,
                 action.ROLL_ACTION))
            if stopActionName:
                actions.append((stopActionName,
                 None,
                 0,
                 action.ROLLSTOP_ACTION))
            owner.fashion.stopAllActions()
            self._setmatcherCoupled(owner, False)
            self.setQingGongActionType(actType)
            BigWorld.callback(duration + 0.3, func)
            BigWorld.callback(duration + 0.3, Functor(self._setmatcherCoupled, owner, True))
            BigWorld.callback(0.1, Functor(owner.fashion.playActionSequence2, owner.model, actions, action.ROLL_ACTION))
            self.playWingFlyModelAction([startActionName, stopActionName])
        elif actType in [gametypes.QINGGONG_DOUBLE_JUMP,
         gametypes.QINGGONG_FAST_RUN_JUMP,
         gametypes.QINGGONG_FAST_RUN_BIG_JUMP,
         gametypes.QINGGONG_MOUNT_JUMP,
         gametypes.QINGGONG_FAST_RUN_DOUBLE_JUMP,
         gametypes.QINGGONG_AUTO_JUMP,
         gametypes.QINGGONG_DASH_AUTO_JUMP]:
            if owner.canSwim():
                self.setState(STATE_IDLE)
                return
            if actType == gametypes.QINGGONG_DOUBLE_JUMP:
                owner.jumpState = gametypes.DEFAULT_TWICE_JUMP
                self.setState(STATE_TWICE_JUMPING)
                if hasattr(owner, 'ap'):
                    owner.ap.setUpSpeedMultiplier()
                    owner.begingDropForBlood(gametypes.DROP_FOR_BLOOD_OTHER)
            elif actType == gametypes.QINGGONG_FAST_RUN_JUMP:
                self.dashStartFlag = False
                owner.dashNormalJump = True
                owner.jumpState = gametypes.DASH_JUMP
                if hasattr(owner, 'ap'):
                    owner.ap.upwardMagnitude = 1
                    owner.ap.setUpSpeedMultiplier()
                    owner.ap.updateVelocity()
                    owner.begingDropForBlood(gametypes.DROP_FOR_BLOOD_OTHER)
                self.setState(STATE_DASH_JUMPING)
            elif actType == gametypes.QINGGONG_MOUNT_JUMP:
                self.dashStartFlag = False
                owner.dashNormalJump = True
                owner.jumpState = gametypes.DASH_JUMP
                if hasattr(owner, 'ap'):
                    owner.ap.setUpSpeedMultiplier()
                    owner.begingDropForBlood(gametypes.DROP_FOR_BLOOD_OTHER)
                self.setState(STATE_DASH_JUMPING)
            elif actType == gametypes.QINGGONG_FAST_RUN_BIG_JUMP:
                self.dashStartFlag = False
                owner.jumpState = gametypes.DASH_BIG_JUMP
                owner.dashNormalJump = False
                if hasattr(owner, 'ap'):
                    owner.ap.setUpSpeedMultiplier()
                    owner.ap.forwardMagnitude = 1
                    owner.begingDropForBlood(gametypes.DROP_FOR_BLOOD_OTHER)
                self.setState(STATE_DASH_BIG_JUMPING)
            elif actType == gametypes.QINGGONG_AUTO_JUMP:
                if owner.canFly():
                    return
                self.dashStartFlag = False
                owner.jumpState = gametypes.AUTO_JUMP
                self.setState(STATE_AUTO_JUMP)
                if owner.fashion.isPlayer:
                    owner.setGravity(PCD.data.get('autoJumpGravity', gametypes.AUTO_JUMP_GRAVITY))
            elif actType == gametypes.QINGGONG_DASH_AUTO_JUMP:
                self.dashStartFlag = False
                owner.jumpState = gametypes.DASH_AUTO_JUMP
                self.setState(STATE_DASH_AUTO_JUMP)
                if owner.fashion.isPlayer:
                    if owner.isInsideWater and not owner.inSwim:
                        distanceFromWater = owner.qinggongMgr.getDistanceFromWater()
                        if distanceFromWater:
                            owner.intoWater(True, distanceFromWater)
                        owner.fashion.breakJump()
                        switchToDash(owner)
                        return
                    owner.setGravity(PCD.data.get('dashAutoJumpGravity', gametypes.AUTO_JUMP_GRAVITY))
            elif actType == gametypes.QINGGONG_FAST_RUN_DOUBLE_JUMP:
                self.dashStartFlag = False
                owner.jumpState = gametypes.DASH_TWICE_JUMP
                self.setState(STATE_DASH_TWICE_JUMPING)
                if hasattr(owner, 'ap'):
                    owner.begingDropForBlood(gametypes.DROP_FOR_BLOOD_DASH_TWICE_JUMP)
                    owner.ap.setUpSpeedMultiplier()
                    owner.ap.updateVelocity()
            owner.isStartJumping = True
            if owner.fashion.isPlayer:
                owner.cell.startJumping(True)
            owner.fashion.jump(True)
            if owner == BigWorld.player():
                gameglobal.rds.ui.actionbar.checkAllSkillStat(gameglobal.SKILL_STAT_NO_SKILL)
        elif actType == gametypes.QINGGONG_FAST_DOWN:
            self.dashStartFlag = True
            if owner.fashion.isPlayer:
                owner.begingDropForBlood(gametypes.DROP_FOR_BLOOD_FAST_DOWN)
                owner.physics.keepJumpVelocity = False
                owner.ap.upwardMagnitude = 0
                owner.ap.forwardMagnitude = 0
                owner.setGravity(PCD.data.get('dashRushGravity', gametypes.DASHRUSH_GRAVITY))
                owner.ap.needDoJump = False
                gamelog.debug('owner.physics.gravity:', owner.physics.gravity)
                owner.ap.updateVelocity()
            try:
                owner.fashion.stopActions()
            except:
                pass

            fallActionName = owner.fashion.getFastFallActionName()
            if fallActionName:
                try:
                    act = owner.model.action(fallActionName)
                    if act:
                        if owner.isJumping:
                            actions = []
                            actions.append((fallActionName,
                             None,
                             0,
                             action.FAST_DOWN_ACTION))
                            owner.fashion.playActionSequence2(owner.model, actions, action.FAST_DOWN_ACTION)
                except:
                    gamelog.error("qinggong:jump:can\'t find action:", fallActionName)

        elif actType == gametypes.QINGGONG_RUSH_DOWN:
            self.dashStartFlag = True
            self.setState(STATE_RUSH_DOWN)
            if owner.fashion.isPlayer:
                owner.ap._enterSlideStatus()
                owner.physics.keepJumpVelocity = False
                owner.ap.upwardMagnitude = 0
                owner.ap.forwardMagnitude = 1
                owner.setGravity(PCD.data.get('rushDownGravity', gametypes.RUSH_DOWN_GRAVITY))
                self.rushTop = False
                gamelog.debug('owner.physics.gravity:', owner.physics.gravity)
                owner.ap.updateVelocity()
            try:
                owner.fashion.stopActions()
            except:
                pass

            rushEndAction = owner.fashion.getRushEndAction()
            if rushEndAction:
                try:
                    actions = []
                    actions.append((rushEndAction,
                     None,
                     0,
                     action.RUSH_DOWN_ACTION))
                    rushEndDownAction = owner.fashion.getRushEndDownAction()
                    if rushEndDownAction:
                        actions.append((rushEndDownAction,
                         None,
                         0,
                         action.RUSH_DOWN_ACTION))
                    owner.fashion.playActionSequence2(owner.model, actions, action.RUSH_DOWN_ACTION)
                except:
                    gamelog.error("qinggong:jump:can\'t find action:", rushEndAction)

        elif actType == gametypes.QINGGONG_RUSH_DOWN_WEAPON_IN_HAND:
            self.dashStartFlag = True
            self.setState(STATE_RUSH_DOWN_WEAPON_IN_HAND)
            if owner.fashion.isPlayer:
                owner.ap._enterSlideStatus()
                owner.physics.keepJumpVelocity = False
                owner.ap.upwardMagnitude = 0
                owner.ap.forwardMagnitude = 1
                owner.setGravity(PCD.data.get('rushDownWeaponInHandGravity', gametypes.RUSH_DOWN_WEAPON_IN_HAND_GRAVITY))
                self.rushTop = False
                gamelog.debug('owner.physics.gravity:', owner.physics.gravity)
                owner.ap.updateVelocity()
            try:
                owner.fashion.stopActions()
            except:
                pass

            rushEndAction = owner.fashion.getRushEndAction()
            if rushEndAction:
                try:
                    actions = []
                    actions.append((rushEndAction,
                     None,
                     0,
                     action.RUSH_DOWN_ACTION))
                    rushEndDownAction = owner.fashion.getRushEndDownAction()
                    if rushEndDownAction:
                        actions.append((rushEndDownAction,
                         None,
                         0,
                         action.RUSH_DOWN_ACTION))
                    owner.fashion.playActionSequence2(owner.model, actions, action.RUSH_DOWN_ACTION)
                except:
                    gamelog.error("qinggong:jump:can\'t find action:", rushEndAction)

        elif actType == gametypes.QINGGONG_WINGFLY_FAST_DOWN:
            if owner.fashion.isPlayer:
                owner.physics.keepJumpVelocity = False
                owner.physics.swim(0)
                owner.physics.jump(True, True)
                owner.ap.upwardMagnitude = 0
                owner.ap.forwardMagnitude = 0
                owner.setGravity(PCD.data.get('dashRushGravity', gametypes.DASHRUSH_GRAVITY), True)
                owner.ap.needDoJump = False
                owner.ap.updateVelocity()
            try:
                owner.fashion.stopActions()
            except:
                pass

            fallActionName = owner.fashion.getWingFlyFastFallAction()
            if fallActionName:
                try:
                    act = owner.model.action(fallActionName)
                    if act:
                        actions = []
                        actions.append((fallActionName,
                         None,
                         0,
                         action.JUMP_ACTION))
                        owner.fashion.playActionSequence2(owner.model, actions, action.JUMP_ACTION)
                        self.playWingFlyModelAction([fallActionName])
                except:
                    gamelog.error("qinggong:jump:can\'t find action:", fallActionName)

        elif actType == gametypes.QINGGONG_SLOW_DOWN:
            if owner == BigWorld.player():
                owner.updateActionKeyState()
                owner.ap.updateVelocity()
            else:
                if owner.inFlyTypeFlyRide() and owner.modelServer and owner.modelServer.rideAttached and owner.modelServer.rideAttached.flyRideIdleAction:
                    pass
                else:
                    owner.fashion.stopAllActions()
                owner.qinggongMgr.stopWingFlyModelAction()
            self.dashStartFlag = True
            fallFlyActionName = owner.fashion.action.getSlowFallDownAction(owner.fashion)
            gamelog.debug('bgf:fallFlyAction2', fallFlyActionName)
            if fallFlyActionName:
                if hasattr(owner, 'ap'):
                    self.rushTop = False
                    owner.physics.keepJumpVelocity = False
                    owner.ap.dashFlySpeed = 0.5
                    owner.ap.upwardMagnitude = 0
                    owner.ap.needDoJump = False
                    if not owner.inSwim and not owner.inFly:
                        owner.setGravity(self._getSlowFallGravity())
                    owner.ap.updateVelocity()
                try:
                    act = owner.model.action(fallFlyActionName)
                    if act:
                        if owner.isJumping:
                            act()
                except:
                    gamelog.error("qinggong:jump:can\'t find action:1225")

    def _setmatcherCoupled(self, owner, bCoupled):
        if hasattr(owner, 'am'):
            gamelog.debug('qinggong:_setmatcherCoupled:', bCoupled)
            owner.am.matcherCoupled = bCoupled
            if owner.fashion.isPlayer:
                owner.physics.needPromotionVelY = bCoupled

    def _getSlowFallGravity(self, t = 1.0):
        dist = self.getDistanceFromGround()
        if t <= 0:
            g = SYSCD.data.get('runDownGravity', gametypes.RUN_DOWNGRAVITY)
        else:
            g = 2 * dist / t / t
        gamelog.debug('@PGF:_getSlowFallGravity', g)
        return min(max(g, SYSCD.data.get('runDownGravity', gametypes.RUN_DOWNGRAVITY)), gametypes.MAX_DOWNGRAVITY)

    def startState(self, old):
        owner = BigWorld.entity(self.ownerID)
        if not owner or not owner.inWorld:
            return
        if not owner.fashion:
            return
        gamelog.debug('startState', owner.qinggongState)
        if owner.qinggongState in gametypes.QINGGONG_STATE_DASH_SET:
            if self.jumpDashFlag:
                self.jumpDashFlag = False
            self.setState(STATE_DASH)
            if owner.fashion.isPlayer:
                if not owner.isInsideWater:
                    owner.setGravity(SYSCD.data.get('dashGravity', gametypes.DASH_GRAVITY))
                owner.isDashing = True
                owner.ap.updateVelocity()
            if old == gametypes.QINGGONG_STATE_DEFAULT:
                self.doFuncByEvent(EVENT_FORWARD_DOWN)
        elif owner.qinggongState == gametypes.QINGGONG_STATE_AUTO_JUMP:
            if owner.fashion.isPlayer:
                owner.begingDropForBlood(gametypes.DROP_FOR_BLOOD_OTHER)
            self.setState(STATE_AUTO_JUMP)
        elif owner.qinggongState == gametypes.QINGGONG_STATE_DASH_AUTO_JUMP:
            if owner.fashion.isPlayer:
                owner.begingDropForBlood(gametypes.DROP_FOR_BLOOD_OTHER)
            self.setState(STATE_DASH_AUTO_JUMP)
            self.jumpState = gametypes.DASH_AUTO_JUMP
        elif owner.qinggongState == gametypes.QINGGONG_STATE_SLIDING:
            self.setState(STATE_DASH_TWICE_JUMPING)
            if old in (gametypes.QINGGONG_STATE_FAST_SLIDING, gametypes.QINGGONG_STATE_FAST_SLIDING_WEAPON_IN_HAND, gametypes.QINGGONG_STATE_RUSH_DOWN):
                if owner.canFly():
                    self.stopWingFlyModelAction()
                self.doQinggongAction(gametypes.QINGGONG_FAST_RUN_DOUBLE_JUMP)
        elif owner.qinggongState == gametypes.QINGGONG_STATE_RUSH_DOWN:
            self.setState(STATE_RUSH_DOWN)
            if owner.fashion.isPlayer:
                owner.begingDropForBlood(gametypes.DROP_FOR_BLOOD_RUSH_DOWN)
            if old == gametypes.QINGGONG_STATE_FAST_SLIDING:
                if owner.canFly():
                    self.stopWingFlyModelAction()
                self.doQinggongAction(gametypes.QINGGONG_RUSH_DOWN)
            elif old == gametypes.QINGGONG_STATE_SLIDING:
                if owner.canFly():
                    self.stopWingFlyModelAction()
                self.doQinggongAction(gametypes.QINGGONG_RUSH_DOWN)
        elif owner.qinggongState == gametypes.QINGGONG_STATE_RUSH_DOWN_WEAPON_IN_HAND:
            self.setState(STATE_RUSH_DOWN_WEAPON_IN_HAND)
            if owner.fashion.isPlayer:
                owner.begingDropForBlood(gametypes.DROP_FOR_BLOOD_RUSH_DOWN)
            if old in (gametypes.QINGGONG_STATE_FAST_SLIDING_WEAPON_IN_HAND, gametypes.QINGGONG_STATE_SLIDING):
                if owner.canFly():
                    self.stopWingFlyModelAction()
                self.doQinggongAction(gametypes.QINGGONG_RUSH_DOWN_WEAPON_IN_HAND)
        elif owner.qinggongState == gametypes.QINGGONG_STATE_FAST_SLIDING:
            self.setState(STATE_SLIDE_DASH)
            self.startStateAction(SLIDE_DASH_NORMAL)
        elif owner.qinggongState == gametypes.QINGGONG_STATE_FAST_SLIDING_WEAPON_IN_HAND:
            self.setState(STATE_SLIDE_DASH_WEAPON_IN_HAND)
            self.startStateAction(SLIDE_DASH_WEAPON_IN_HAND)
        elif owner.qinggongState == gametypes.QINGGONG_STATE_DEFAULT:
            if owner.fashion.isPlayer:
                self.stopWindSound()
            self.setState(STATE_IDLE)
            if old in gametypes.QINGGONG_STATE_DASH_SET:
                if owner.fashion.isPlayer:
                    owner.isDashing = False
                    owner.ap.updateVelocity()
                self.setState(STATE_DASH)
                self.doFuncByEvent(EVENT_DEFAULT)
            elif old in (gametypes.QINGGONG_STATE_SLIDING,
             gametypes.QINGGONG_STATE_FAST_SLIDING,
             gametypes.QINGGONG_STATE_FAST_SLIDING_WEAPON_IN_HAND,
             gametypes.QINGGONG_STATE_RUSH_DOWN_WEAPON_IN_HAND):
                if owner.inCombat:
                    if owner.fashion.isPlayer:
                        owner.physics.keepJumpVelocity = False
                        owner.physics.velocity = (0, owner.physics.velocity[1], 0)
                        owner.physics.maxTopVelocity = owner.physics.velocity
                        if old in (gametypes.QINGGONG_STATE_FAST_SLIDING_WEAPON_IN_HAND, gametypes.QINGGONG_STATE_RUSH_DOWN_WEAPON_IN_HAND):
                            owner.ap.updateVelocity()
                            owner.restoreGravity()
                            owner.updateActionKeyState()
                else:
                    if owner.fashion.doingActionType() not in (action.FAST_DOWN_ACTION,):
                        owner.fashion.stopAllActions()
                    if owner.fashion.isPlayer:
                        owner.ap.updateVelocity()
                        if old == gametypes.QINGGONG_STATE_FAST_SLIDING_WEAPON_IN_HAND:
                            owner.restoreGravity()
                self.setState(STATE_IDLE)
            elif old in [gametypes.QINGGONG_STATE_WINGFLY_UP, gametypes.QINGGONG_STATE_WINGFLY_LANDUP]:
                self.setState(STATE_WINGFLY_IDLE)
                if owner.fashion.isPlayer:
                    owner.ap.startFlyDecelerate(gameglobal.QUICK_FLY_UP)
                if self.wingFlyUpCallBack:
                    BigWorld.cancelCallback(self.wingFlyUpCallBack)
                    self.wingFlyUpCallBack = None
            elif old == gametypes.QINGGONG_STATE_WINGFLY_DOWN:
                if owner.fashion.isPlayer:
                    owner.ap.startFlyDecelerate(gameglobal.QUICK_FLY_DOWN)
                self.setState(STATE_WINGFLY_IDLE)
            elif old == gametypes.QINGGONG_STATE_WINGFLY_LEFT:
                self.setState(STATE_WINGFLY_IDLE)
                if owner.fashion.isPlayer:
                    owner.ap.startFlyDecelerate(gameglobal.QUICK_FLY_LEFT)
            elif old == gametypes.QINGGONG_STATE_WINGFLY_RIGHT:
                self.setState(STATE_WINGFLY_IDLE)
                if owner.fashion.isPlayer:
                    owner.ap.startFlyDecelerate(gameglobal.QUICK_FLY_RIGHT)
            elif old == gametypes.QINGGONG_STATE_WINGFLY_BACK:
                self.setState(STATE_WINGFLY_IDLE)
                if owner.fashion.isPlayer:
                    owner.ap.startFlyDecelerate(gameglobal.QUICK_FLY_BACK)
            elif old == gametypes.QINGGONG_STATE_WINGFLY_DASH:
                self.setState(STATE_WINGFLY_IDLE)
                if owner.fashion.isPlayer:
                    owner.ap.startFlyDecelerate(gameglobal.QUICK_FLY)
            elif old == gametypes.QINGGONG_STATE_FAST_JUMP:
                if owner.fashion.isPlayer:
                    if owner.inCombat:
                        owner.physics.keepJumpVelocity = False
                        owner.physics.velocity = (0, owner.physics.velocity[1], 0)
                        owner.physics.maxTopVelocity = owner.physics.velocity
            elif old == gametypes.QINGGONG_STATE_RUSH_DOWN:
                if owner.fashion.isPlayer:
                    owner.ap.updateVelocity()
            elif old == gametypes.QINGGONG_STATE_SLOW_DOWN:
                if owner.fashion.isPlayer:
                    owner.ap.updateVelocity()
        elif owner.qinggongState == gametypes.QINGGONG_STATE_WINGFLY_UP:
            self.setState(STATE_WINGFLY_UP)
            self.startStateAction(GO_WINGFLY_UP)
        elif owner.qinggongState == gametypes.QINGGONG_STATE_WINGFLY_LANDUP:
            self.setState(STATE_WINGFLY_UP)
            self.startStateAction(GO_WINGFLY_LANDUP)
        elif owner.qinggongState == gametypes.QINGGONG_STATE_WINGFLY_DOWN:
            self.setState(STATE_WINGFLY_DOWN)
            self.startStateAction(GO_WINGFLY_DOWN)
        elif owner.qinggongState == gametypes.QINGGONG_STATE_WINGFLY_LEFT:
            self.setState(STATE_WINGFLY_LEFT)
            self.startStateAction(GO_WINGFLY_LEFT)
        elif owner.qinggongState == gametypes.QINGGONG_STATE_WINGFLY_RIGHT:
            self.setState(STATE_WINGFLY_RIGHT)
            self.startStateAction(GO_WINGFLY_RIGHT)
        elif owner.qinggongState == gametypes.QINGGONG_STATE_WINGFLY_BACK:
            self.setState(STATE_WINGFLY_BACK)
            self.startStateAction(GO_WINGFLY_BACK)
        elif owner.qinggongState == gametypes.QINGGONG_STATE_WINGFLY_DASH:
            self.setState(STATE_WINGFLY_DASH)
            self.startStateAction(GO_WINGFLY_DASH)

    def startStateAction(self, actType):
        gamelog.debug('startStateAction:1', actType)
        if actType in [SLIDE_DASH_NORMAL, SLIDE_DASH_WEAPON_IN_HAND]:
            self.__playRush()
        elif actType in [GO_WINGFLY_DASH]:
            self.__playWingFlyDashAction()
        elif actType in [GO_WINGFLY_UP, GO_WINGFLY_LANDUP]:
            self.__playWingFlyUpAction()
        elif actType in [GO_WINGFLY_DOWN]:
            self.__playWingFlyDownAction()
        elif actType in [GO_WINGFLY_LEFT]:
            self.__playWingFlyLeftAction()
        elif actType in [GO_WINGFLY_RIGHT]:
            self.__playWingFlyRightAction()
        elif actType in [GO_WINGFLY_BACK]:
            self.__playWingFlyBackAction()

    def __playRush(self):
        owner = BigWorld.entity(self.ownerID)
        if getattr(owner.model, 'dummyModel', False):
            return
        owner.fashion.stopAllActions()
        rushStartActName = owner.fashion.getRushStartAction()
        if rushStartActName and rushStartActName in owner.fashion.getActionNameList():
            try:
                rushStartAct = owner.model.action(rushStartActName)
            except:
                raise Exception('__playRush error', rushStartActName, str(owner.model.sources))

        else:
            rushStartAct = None
        if owner.fashion.isPlayer:
            owner.physics.keepJumpVelocity = False
            if self.rushTop:
                return
            owner.setGravity(0.0)
            owner.ap.upwardMagnitude = 0
            owner.ap.updateVelocity()
            owner.fashion.incrRrushActionIndex()
            durationTime = owner.fashion.getActionTime(rushStartActName)
            BigWorld.callback(durationTime, Functor(self.set_rushTop, True))
        try:
            if rushStartAct:
                rushActName = owner.fashion.getRushAction()
                if owner.fashion.isPlayer:
                    gameglobal.rds.cam.setAdaptiveFov()
                    BigWorld.projection().rampFov(1.0, 0.5)
                    BigWorld.callback(1.0, Functor(gameglobal.rds.cam.restoreCameraFov, 1.5))
                    owner.model.needUpdateUnitRotation = False
                rushStartAct(0, None, 0).action(rushActName)()
        except:
            pass

    def stopDashAction(self):
        owner = BigWorld.entity(self.ownerID)
        if not owner:
            return
        if owner.bufActState:
            return
        dashStopAction = owner.fashion.getDashStopAction()
        if dashStopAction and not owner.inSwim and not owner.inMoving():
            if owner.fashion.doingActionType() in (action.DASH_START_ACTION,):
                owner.fashion.stopActionByName(owner.model, action.DASH_START_ACTION)
            if owner.fashion.doingActionType() == action.PROGRESS_SPELL_ACTION:
                return
            playSeq = []
            playSeq.append((dashStopAction,
             [],
             action.DASH_STOP_ACTION,
             1,
             1.0,
             None))
            owner.fashion.playActionWithFx(playSeq, action.DASH_STOP_ACTION, None, False, 0, 0)

    def __playWingFlyDashAction(self):
        owner = BigWorld.entity(self.ownerID)
        if not owner:
            return
        try:
            rushStartActName = owner.fashion.getWingFlyRushStartAction()
            if rushStartActName and rushStartActName in owner.fashion.getActionNameList():
                rushStartAct = owner.model.action(rushStartActName)
            else:
                rushStartAct = None
            if rushStartAct:
                if hasattr(owner, 'inFlyTypeFlyRide') and owner.inFlyTypeFlyRide():
                    owner.fashion.stopAction()
                else:
                    owner.fashion.stopAllActions()
            rushStartAct(0, None, 0)
            self.playWingFlyModelAction([rushStartActName])
        except:
            pass

        if owner.fashion.isPlayer:
            if self.rushTop:
                return
            owner.physics.keepJumpVelocity = False
            owner.physics.endAccelerate()
            owner.ap.startFlyAccelerate(gameglobal.QUICK_FLY)
            owner.setGravity(0.0)
            owner.ap.upwardMagnitude = 0
            gameglobal.rds.cam.setAdaptiveFov()
            BigWorld.projection().rampFov(1.0, 0.5)
            BigWorld.callback(1.0, Functor(gameglobal.rds.cam.restoreCameraFov, 1.5))
            owner.updateFlyTailEffect(True)

    def __playWingFlyLeftAction(self):
        owner = BigWorld.entity(self.ownerID)
        if not owner:
            return
        wingFlyLeftStartActName = owner.fashion.getWingFlyLeftStartAction()
        if owner.fashion.isPlayer:
            owner.physics.endAccelerate()
            owner.ap.startFlyAccelerate(gameglobal.QUICK_FLY_LEFT)
        try:
            if wingFlyLeftStartActName:
                wingFlyLeftStartAct = owner.model.action(wingFlyLeftStartActName)
                wingFlyLeftStartAct()
                self.playWingFlyModelAction([wingFlyLeftStartActName])
        except:
            pass

    def __playWingFlyRightAction(self):
        owner = BigWorld.entity(self.ownerID)
        if not owner:
            return
        wingFlyRightStartActName = owner.fashion.getWingFlyRightStartAction()
        if owner.fashion.isPlayer:
            owner.physics.endAccelerate()
            owner.ap.startFlyAccelerate(gameglobal.QUICK_FLY_RIGHT)
        try:
            if wingFlyRightStartActName:
                wingFlyRightStartAct = owner.model.action(wingFlyRightStartActName)
                wingFlyRightStartAct()
                self.playWingFlyModelAction([wingFlyRightStartActName])
        except:
            pass

    def __playWingFlyBackAction(self):
        owner = BigWorld.entity(self.ownerID)
        if not owner:
            return
        wingFlyBackStartActName = owner.fashion.getWingFlyBackStartAction()
        if owner.fashion.isPlayer:
            owner.physics.endAccelerate()
            owner.ap.startFlyAccelerate(gameglobal.QUICK_FLY_BACK)
        try:
            if wingFlyBackStartActName and wingFlyBackStartActName in owner.fashion.getActionNameList():
                wingFlyBackStartAct = owner.model.action(wingFlyBackStartActName)
                wingFlyBackStartAct()
                self.playWingFlyModelAction([wingFlyBackStartActName])
        except:
            pass

    def __playWingFlyDownAction(self):
        owner = BigWorld.entity(self.ownerID)
        if not owner:
            return
        wingFlyDownStartActName = owner.fashion.getWingFlyDownStartAction()
        if owner.fashion.isPlayer:
            self._cycleCheckFromGround()
            self._cycleCheckFromWater()
            owner.physics.endAccelerate()
            owner.ap.startFlyAccelerate(gameglobal.QUICK_FLY_DOWN)
        try:
            if wingFlyDownStartActName:
                wingFlyDownStartAct = owner.model.action(wingFlyDownStartActName)
                wingFlyDownActName = owner.fashion.getWingFlyDownAction()
                wingFlyDownStartAct(0, None, 0).action(wingFlyDownActName)()
                self.playWingFlyModelAction([wingFlyDownActName])
        except:
            pass

    def __playWingFlyUpAction(self):
        owner = BigWorld.entity(self.ownerID)
        if not owner or not owner.inWorld:
            return
        if getattr(owner.model, 'dummyModel', False):
            return
        if owner.inFly:
            wingFlyUpStartActName = owner.fashion.getWingFlyUpStartAction()
        else:
            wingFlyUpStartActName = owner.fashion.action.getWingNoFlyUpStartAction(owner.fashion)
        wingFlyUpStartAct = None
        if wingFlyUpStartActName and wingFlyUpStartActName in owner.fashion.getActionNameList():
            try:
                wingFlyUpStartAct = owner.model.action(wingFlyUpStartActName)
            except:
                pass

        if owner.fashion.isPlayer:
            owner.setGravity(0.0)
            owner.physics.endAccelerate()
            owner.ap.startFlyAccelerate(gameglobal.QUICK_FLY_UP)
        try:
            wingFlyUpActName = owner.fashion.getWingFlyUpAction()
            wingFlyUpStartAct(0, None, 0).action(wingFlyUpActName)()
            self.playWingFlyModelAction([wingFlyUpActName])
        except:
            pass

    def getDistanceFromGround(self):
        owner = BigWorld.entity(self.ownerID)
        if not owner:
            return 0.0
        length = owner.flyHeight
        if BigWorld.player().spaceID:
            dropPoint = BigWorld.findDropPoint(BigWorld.player().spaceID, Math.Vector3(owner.position[0], owner.position[1] + 1.5, owner.position[2]))
            if dropPoint is not None:
                length = (dropPoint[0] - owner.position).length
        return length

    def getReplacedFeiJianModelAction(self, actions):
        replacedActions = []
        feiJianActionDict = SYSCD.data.get('feiJianActionDict', [])
        for act in actions:
            if act in feiJianActionDict:
                replacedActions.append(feiJianActionDict.get(act))
            else:
                replacedActions.append(act)

        return replacedActions

    def getReplacedBodyActions(self, owner, actions):
        newActions = []
        if not owner.tride.inRide() or not RTD.data.get(owner.bianshen[1], {}).get('useTrideActPostfix', False):
            return actions
        else:
            for act in actions:
                newActions.append(owner.getRideTogetherActionName(act, 0))

            return newActions

    def playReplacedBodyModelFlyAction(self, actions, rateScale = 1.0):
        owner = BigWorld.entity(self.ownerID)
        isInHorse = owner.inRiding() and owner.bianshen[0] == gametypes.BIANSHEN_RIDING_RB
        if not isInHorse:
            return
        rideAttached = owner.modelServer.rideAttached
        if rideAttached and (rideAttached.flyRideIdleAction or rideAttached.chairIdleAction):
            return
        actions = self.getReplacedFeiJianModelAction(actions)
        owner.fashion.playActionSequence(owner.modelServer.bodyModel, self.getReplacedBodyActions(owner, actions), None, rateScale, 0)

    def playReplacedWingFlyModelAction(self, actions, rateScale = 1.0):
        owner = BigWorld.entity(self.ownerID)
        if not owner.canFly():
            return
        if owner.modelServer.wingFlyModel:
            model = owner.modelServer.wingFlyModel.model
            if not model or not model.inWorld:
                return
            actions = self.getReplacedWingFlyModelAction(actions)
            owner.fashion.playActionSequence(model, actions, None, rateScale, 0)

    def playWingFlyModelAction(self, actions, rateScale = 1.0):
        owner = BigWorld.entity(self.ownerID)
        if not owner or not owner.inWorld:
            return
        gamelog.debug('playWingFlyModelAction', actions, owner.modelServer.wingFlyModel.model)
        self.playReplacedBodyModelFlyAction(actions, rateScale)
        self.playReplacedWingFlyModelAction(actions, rateScale)
        if actions:
            owner.playRideTogetherAction(actions[0])

    def getReplacedWingFlyModelAction(self, actions):
        replacedActions = []
        flyCarryActionDict = SYSCD.data.get('flyCarryActionDict', [])
        for act in actions:
            if act in flyCarryActionDict:
                replacedActions.append(flyCarryActionDict.get(act))
            else:
                replacedActions.append(act)

        return replacedActions

    def stopWingFlyModelAction(self):
        gamelog.debug('stopWingFlyModelAction')
        owner = BigWorld.entity(self.ownerID)
        model = owner.modelServer.wingFlyModel.model
        if not model or not model.inWorld:
            return
        actionList = owner.fashion.wingFlyActionList
        for i in actionList:
            try:
                aq = model.action(i)
                playAq = owner.model.action(i)
                if model.freezeTime <= 0:
                    aq.stop()
                if owner.model.freezeTime <= 0:
                    playAq.stop()
            except:
                pass

    def _cycleCheckFromGround(self):
        owner = BigWorld.entity(self.ownerID)
        if not owner.inWorld:
            return
        gamelog.debug('_cycleCheckFromGround', self.getDistanceFromGround())
        if self.getDistanceFromGround() < gameglobal.FROMGROUNDDIST:
            owner.ap.landWingFlyUp(False)
        elif owner.qinggongState == gametypes.QINGGONG_STATE_WINGFLY_DOWN:
            BigWorld.callback(0.5, self._cycleCheckFromGround)

    def _cycleCheckFromWater(self):
        owner = BigWorld.entity(self.ownerID)
        if not owner.inWorld:
            return
        waterDist = self.getDistanceFromWater()
        if waterDist and waterDist < gameglobal.FROMWATERDIST:
            owner.ap.landWingFlyUp(False)
        elif owner.qinggongState == gametypes.QINGGONG_STATE_WINGFLY_DOWN:
            BigWorld.callback(0.5, self._cycleCheckFromWater)

    def getDistanceFromWater(self):
        owner = BigWorld.entity(self.ownerID)
        if owner is None:
            return
        res = BigWorld.findWaterFromPoint(owner.spaceID, owner.position)
        if not res:
            return
        return owner.position.y - res[0]
