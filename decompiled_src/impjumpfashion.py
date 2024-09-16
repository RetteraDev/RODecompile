#Embedded file name: /WORKSPACE/data/entities/client/helpers/impjumpfashion.o
import math
import random
import BigWorld
import const
import gameglobal
import gametypes
import action
import keys
import gamelog
from helpers import cellCmd
from data import physics_config_data as PCD
from data import ride_together_data as RTD
NOT_IN_JUMP = -1
JUMP_UP_PHASE = 0
JUMP_DOWN_PHASE = 1
AUTO_JUMP_DIST = 10.0

class JumpActionManager(object):

    def __init__(self, owner):
        self.owner = owner
        self.jumpEndTime = 0.0
        self.jumpPhase = NOT_IN_JUMP

    def jumpStart(self, isClimbing = False):
        owner = BigWorld.entity(self.owner)
        if owner == None or not hasattr(owner, 'fashion') or owner.fashion == None:
            return 0.0
        if owner.fashion.doingActionType() == action.DASH_START_ACTION:
            owner.fashion.stopAllActions()
        self.jumpPhase = JUMP_UP_PHASE
        jumpStartActionName = owner.fashion.getJumpStartActionName()
        if jumpStartActionName == None:
            return 0.0
        models = [owner.model]
        if owner.inRidingHorse() and hasattr(owner.model, 'ride') and owner.model.ride:
            models.append(owner.model.ride)
        rtModels = []
        if owner.inRidingHorse() and hasattr(owner, 'tride') and owner.tride.inRide():
            for key in owner.tride.keys():
                idx = owner.tride.get(key)
                driveActions = RTD.data.get(owner.bianshen[1], {}).get('seatActions', ((11101, 0),))
                driveAction = driveActions[idx - 1]
                if driveAction[1]:
                    model = owner.modelServer.getRideTogetherModelByIdx(idx)
                    if model:
                        rtModels.append((idx, model))

        startAct = None
        for m in models:
            try:
                if getattr(m, 'dummyModel', False):
                    continue
                startAct = m.action(jumpStartActionName)
                linker = startAct()
                jumpActionName = owner.fashion.getJumpActionName()
                if jumpActionName:
                    linker = getattr(linker, jumpActionName)()
                    jumpUpActionName = owner.fashion.getJumpUpActionName()
                    if jumpUpActionName:
                        linker = getattr(linker, jumpUpActionName)()
                        fallFlyActionName = owner.fashion.getFallFlyActionName()
                        if fallFlyActionName:
                            linker = getattr(linker, fallFlyActionName)()
                    if owner.jumpState != gametypes.DASH_TWICE_JUMP:
                        fallActionName = owner.fashion.getFallActionName()
                    else:
                        fallActionName = None
                    if fallActionName:
                        getattr(linker, fallActionName)()
            except:
                pass

        try:
            for idx, m in rtModels:
                if getattr(m, 'dummyModel', False):
                    continue
                startAct = m.action(owner.getRideTogetherActionName(jumpStartActionName, idx))
                linker = startAct()
                jumpActionName = owner.fashion.getJumpActionName()
                if jumpActionName:
                    linker = getattr(linker, owner.getRideTogetherActionName(jumpActionName, idx))()
                    jumpUpActionName = owner.fashion.getJumpUpActionName()
                    if jumpUpActionName:
                        linker = getattr(linker, owner.getRideTogetherActionName(jumpUpActionName, idx))()
                        fallFlyActionName = owner.fashion.getFallFlyActionName()
                        if fallFlyActionName:
                            linker = getattr(linker, owner.getRideTogetherActionName(fallFlyActionName, idx))()
                    if owner.jumpState != gametypes.DASH_TWICE_JUMP:
                        fallActionName = owner.fashion.getFallActionName()
                    else:
                        fallActionName = None
                    if fallActionName:
                        getattr(linker, owner.getRideTogetherActionName(fallActionName, idx))()

        except:
            pass

        owner.fashion.setDoingActionType(action.JUMP_ACTION)
        return getattr(startAct, 'duration', 0)

    def setUpSpeed(self, upSpeed):
        owner = BigWorld.entity(self.owner)
        owner.ap.upSpeedMultiplier = upSpeed

    def jumpEnd(self):
        if self.jumpPhase == NOT_IN_JUMP:
            return
        owner = BigWorld.entity(self.owner)
        self.jumpPhase = NOT_IN_JUMP
        owner.delayCancelWeaponTimerAndHangUpWeapon()
        if owner == None or not hasattr(owner, 'fashion') or owner.fashion == None or owner.fashion.doingActionType() == action.GUIDE_ACTION:
            return
        if owner.inSwim:
            fallendActionName = None
        else:
            fallendActionName = owner.fashion.getFallEndActionName()
        owner.rideTogetherDownHorse = False
        if fallendActionName:
            if owner.life != gametypes.LIFE_DEAD:
                owner.fashion.fallEndAction = fallendActionName
                if owner.fashion.doingActionType() != action.GUIDE_ACTION:
                    owner.fashion.playSingleAction(fallendActionName, action.FALLEND_ACTION)
                elif fallendActionName in self.getActionNameList():
                    owner.model.action(fallendActionName)()
                if owner.inRidingHorse():
                    if hasattr(owner.model, 'ride') and owner.model.ride and fallendActionName in owner.model.ride.actionNameList():
                        owner.model.ride.action(fallendActionName)()
                owner.playRideTogetherAction(fallendActionName)
                if hasattr(owner, 'ap'):
                    owner.ap.upwardMagnitude = 0
                    owner.updateActionKeyState()
            else:
                owner.clientControl = True
        elif owner.fashion.doingActionType() != action.DEAD_ACTION:
            actQueue = owner.model.queue
            for i in actQueue:
                owner.model.action(i).stop()

            if owner.inRidingHorse():
                if getattr(owner.model, 'ride', None):
                    actQueue = owner.model.ride.queue
                    for i in actQueue:
                        owner.model.ride.action(i).stop()

                if hasattr(owner, 'tride') and owner.tride.inRide():
                    for key in owner.tride.keys():
                        idx = owner.tride.get(key)
                        model = owner.modelServer.getRideTogetherModelByIdx(idx)
                        if model:
                            actQueue = model.queue
                            for i in actQueue:
                                model.action(i).stop()

        owner.jumpState = gametypes.DEFAULT_JUMP

    def breakJump(self):
        if self.jumpPhase != NOT_IN_JUMP:
            self.jumpEnd()

    def isJumpingPhase(self):
        return self.jumpPhase != NOT_IN_JUMP


class ImpJumpFashion(object):

    def jump(self, jumping, isClimbing = False):
        owner = BigWorld.entity(self.owner)
        if hasattr(owner, 'life') and owner.life == gametypes.LIFE_DEAD or not hasattr(owner, 'life'):
            return
        if hasattr(owner, 'avatarInstance'):
            if owner.canFly():
                if self.isPlayer:
                    owner.ap.isJumpEnd = False
                    owner.isJumping = False
                    owner.physics.jump(False)
                    owner.cell.leaveWingFly()
                return
            if jumping:
                if not owner.isStartJumping:
                    return
                if self.isPlayer:
                    if owner.ap.isJumpEnd:
                        return
                if not owner.isJumping:
                    owner.isJumping = True
                    owner.resetShadowUfo()
                self.isStartJump = True
                owner.jumpActionEnableAlpha()
                owner.resetFootIK()
                if hasattr(owner, 'jumpState') and owner.jumpState in (gametypes.DEFAULT_TWICE_JUMP,):
                    self.actRandom = random.randint(2, 3)
                else:
                    self.actRandom = random.randint(1, 2)
                if hasattr(owner, 'jumpState') and owner.jumpState in (gametypes.DEFAULT_JUMP,):
                    owner.apEffectEx.jumpUp()
                delayTime = owner.jumpActionMgr.jumpStart(isClimbing)
                if hasattr(owner, 'breakBeHitAction'):
                    owner.breakBeHitAction()
                if getattr(owner, 'ap', None):
                    delayTime = 0.0
                    if delayTime > 0.0:
                        BigWorld.callback(delayTime, owner.ap._doJump)
                    else:
                        owner.ap._doJump()
            else:
                if not self.isStartJump:
                    return
                self.isStartJump = False
                owner.jumpActionMgr.jumpEnd()
                owner.apEffectEx.fallToLand()
                owner.resetFootIK()
                self.__cancelJumpState()

    def __cancelJumpState(self):
        owner = BigWorld.entity(self.owner)
        owner.isJumping = False
        owner.resetShadowUfo()
        owner.model.needUpdateUnitRotation = True

    def breakJump(self):
        owner = BigWorld.entity(self.owner)
        if owner.isJumping:
            owner.jumpActionMgr.breakJump()
            self.__cancelJumpState()
            if self.isPlayer:
                owner.physics.jump(False)
                owner.ap.afterJumpEnd()

    def fall(self, falling):
        owner = BigWorld.entity(self.owner)
        gamelog.debug('jorsef: fall1', falling)
        if hasattr(owner, 'avatarInstance'):
            if owner.life == gametypes.LIFE_DEAD and not (self.isPlayer and hasattr(owner, 'touchAirWallProcess') and owner.touchAirWallProcess == 1):
                gamelog.debug('jorsef: in fall, dead, ')
                owner.isFalling = False
                return
            if self.isPlayer and owner.isJumping or owner.canSwim():
                owner.isFalling = False
                return
            if owner == BigWorld.player() and BigWorld.player().isSkillAttachOther():
                owner.isFalling = False
                return
            if not falling and not owner.isFalling and hasattr(owner, 'SMachine') and not owner.SMachine.checkStatus(const.CT_FALL):
                gamelog.debug('bgf@impJumpFashion fall failed', falling, owner.isFalling)
                return
            if falling:
                if self.isPlayer:
                    if owner.getOperationMode() == gameglobal.MOUSE_MODE:
                        owner.ap.stopAutoMove()
            if self.doingActionType() in [action.MOVING_ACTION,
             action.AFTERMOVE_ACTION,
             action.FAST_DOWN_ACTION,
             action.FALLEND_ACTION,
             action.SPELL_ACTION,
             action.MOVINGSTOP_ACTION]:
                owner.isFalling = falling
                gamelog.debug('bgf@impJumpFashion fall failed', self.doingActionType())
                return
            if falling:
                if not owner.canFly():
                    owner.isFalling = True
                if owner.inRiding():
                    fallAction = getattr(self.action, 'getHorseFallRunDownAction')(self)
                else:
                    fallAction = self.action.getFallRunDownAction(self)
                gamelog.debug('bgf@impJumpFashion fall', owner.am.matchCaps, falling, fallAction)
                if fallAction == None:
                    if self.isInZaiju(owner) and self.isPlayer:
                        owner.begingDropForBlood(gametypes.DROP_FOR_BLOOD_OTHER)
                    return
                if owner.fashion.doingActionType() == action.GUIDE_ACTION or getattr(owner, 'inDanDao', False):
                    return
                dis = owner.qinggongMgr.getDistanceFromGround()
                if self.isPlayer and dis > 1 and not owner.canFly():
                    if owner.isInCoupleRide():
                        owner.cell.cancelCoupleEmote()
                if keys.CAPS_GROUND in owner.am.matchCaps or keys.CAPS_RIDE in owner.am.matchCaps:
                    if self.isPlayer and dis > PCD.data.get('autoJumpHeight', 1) and owner.ap.isMovingActionKeyControl():
                        if owner.bianshenStateMgr.canFly():
                            owner.cell.enterFlyRide()
                        else:
                            self.fallAutoJumpActRandom = random.randint(0, 1)
                            owner.ap.autoJumpUp(True)
                        return
                    if self.doingActionType() not in [action.CAST_MOVING_ACTION, action.CASTSTOP_ACTION]:
                        if fallAction in owner.fashion.getActionNameList():
                            owner.model.action(fallAction)()
                        if owner.inRidingHorse() and getattr(owner.model, 'ride', None) and fallAction in owner.model.ride.actionNameList():
                            owner.model.ride.action(fallAction)()
                        owner.playRideTogetherAction(fallAction)
                if self.isPlayer:
                    owner.begingDropForBlood(gametypes.DROP_FOR_BLOOD_OTHER)
            else:
                owner.isFalling = False
                fallEnd = None
                if owner.inRiding():
                    fallEnd = getattr(self.action, 'getHorseFallRunEndRunAction')(self)
                elif getattr(owner, 'isMoving', False):
                    fallEnd = self.getFallRunEndRunAction()
                else:
                    fallEnd = getattr(self.action, 'getFallRunEndIdleAction')(self)
                if not owner.canFly():
                    owner.am.applyFlyRoll = False
                    if self.isPlayer:
                        if not owner.isInsideWater:
                            if owner.qinggongState not in (gametypes.QINGGONG_STATE_WINGFLY_DASH,
                             gametypes.QINGGONG_STATE_RUSH_DOWN_WEAPON_IN_HAND,
                             gametypes.QINGGONG_STATE_RUSH_DOWN,
                             gametypes.QINGGONG_STATE_FAST_SLIDING,
                             gametypes.QINGGONG_STATE_FAST_SLIDING_WEAPON_IN_HAND,
                             gametypes.QINGGONG_STATE_MOUNT_DASH):
                                cellCmd.endUpQinggongState()
                if owner.life != gametypes.LIFE_DEAD:
                    if keys.CAPS_GROUND in owner.am.matchCaps or keys.CAPS_RIDE in owner.am.matchCaps:
                        if fallEnd:
                            owner.fashion.fallEndAction = fallEnd
                            if owner.fashion.doingActionType() != action.GUIDE_ACTION:
                                if owner.qinggongState not in (gametypes.QINGGONG_STATE_FAST_SLIDING_WEAPON_IN_HAND, gametypes.QINGGONG_STATE_FAST_SLIDING):
                                    if not getattr(owner, 'bufActState', None):
                                        self.playSingleAction(fallEnd, action.FALLEND_ACTION)
                                        leaveHorseEndAction = self.getLeaveHorseEndAction()
                                        if leaveHorseEndAction:
                                            try:
                                                owner.model.action(leaveHorseEndAction)()
                                            except:
                                                pass

                                    else:
                                        owner.fashion.stopAllActions()
                                if owner.qinggongState in (gametypes.QINGGONG_STATE_RUSH_DOWN_WEAPON_IN_HAND, gametypes.QINGGONG_STATE_RUSH_DOWN):
                                    if self.isPlayer:
                                        cellCmd.endUpQinggongState()
                                        owner.ap.forwardMagnitude = 0
                                        owner.ap.updateVelocity()
                            try:
                                if owner.inRidingHorse() and owner.model.ride:
                                    owner.model.ride.action(fallEnd)()
                                owner.playRideTogetherAction(fallEnd)
                            except:
                                pass

                        if self.isPlayer:
                            if not owner.inPUBGParachute():
                                owner.updateActionKeyState()

    def breakFall(self):
        owner = BigWorld.entity(self.owner)
        if owner.isFalling:
            self.stopAction()
            owner.isFalling = False

    def getJumpStartActionName(self):
        owner = BigWorld.entity(self.owner)
        name = None
        if owner.jumpState == gametypes.DEFAULT_JUMP:
            if owner.inRiding():
                name = getattr(self.action, 'getHorseJumpRunStartAction')(self)
            else:
                name = getattr(self.action, 'getJumpRunStartAction')(self)
        elif owner.jumpState == gametypes.DASH_BIG_JUMP:
            if owner.inRiding():
                name = getattr(self.action, 'getHorseJumpDashStartAction')(self)
            else:
                name = self.action.getJumpDashStart1Action(self)
        elif owner.jumpState == gametypes.DASH_JUMP:
            if owner.inRiding():
                name = getattr(self.action, 'getHorseJumpDashStartAction')(self)
            else:
                name = self.action.getJumpDashStartAction(self)
        elif owner.jumpState == gametypes.AUTO_JUMP:
            if owner.inRiding():
                name = getattr(self.action, 'getHorseJumpRunAction')(self)
            else:
                name = getattr(self.action, 'getJumpRunAction')(self)
        elif owner.jumpState == gametypes.DASH_AUTO_JUMP:
            if self.fallAutoJumpActRandom == 0:
                if owner.inRiding():
                    name = getattr(self.action, 'getHorseJumpDashAction')(self)
                else:
                    name = self.action.getJumpDashAction(self)
            elif owner.inRiding():
                name = getattr(self.action, 'getHorseJumpDashAction')(self)
            else:
                name = self.action.getJumpDash1Action(self)
        elif owner.jumpState == gametypes.DEFAULT_TWICE_JUMP:
            acttionName = 'getJumpRunTwiceStart' + str(self.actRandom) + 'Action'
            name = getattr(self.action, acttionName)(self)
        elif owner.jumpState == gametypes.DASH_TWICE_JUMP:
            acttionName = 'getJumpDashTwiceStart' + str(self.actRandom) + 'Action'
            name = getattr(self.action, acttionName)(self)
        if not name:
            name = getattr(self.action, 'getJumpRunStartAction')(self)
        gamelog.debug('zfjump:1', name, owner.jumpState)
        return name

    def getJumpActionName(self):
        owner = BigWorld.entity(self.owner)
        name = None
        if owner.jumpState == gametypes.DEFAULT_JUMP:
            if owner.inRiding():
                name = getattr(self.action, 'getHorseJumpRunAction')(self)
            else:
                name = getattr(self.action, 'getJumpRunAction')(self)
        elif owner.jumpState == gametypes.DASH_JUMP:
            if owner.inRiding():
                name = getattr(self.action, 'getHorseJumpDashAction')(self)
            else:
                name = self.action.getJumpDashAction(self)
        elif owner.jumpState == gametypes.AUTO_JUMP:
            if owner.inRiding():
                name = getattr(self.action, 'getHorseJumpRunUpAction')(self)
            else:
                name = getattr(self.action, 'getJumpRunUpAction')(self)
        elif owner.jumpState == gametypes.DASH_AUTO_JUMP:
            if self.fallAutoJumpActRandom == 0:
                if owner.inRiding():
                    name = getattr(self.action, 'getHorseJumpDashUpAction')(self)
                else:
                    name = getattr(self.action, 'getJumpDashUpAction')(self)
            elif owner.inRiding():
                name = getattr(self.action, 'getHorseJumpDashUpAction')(self)
            else:
                name = getattr(self.action, 'getJumpDashUp1Action')(self)
        elif owner.jumpState == gametypes.DASH_BIG_JUMP:
            if owner.inRiding():
                name = getattr(self.action, 'getHorseJumpDashAction')(self)
            else:
                name = self.action.getJumpDash1Action(self)
        elif owner.jumpState == gametypes.DEFAULT_TWICE_JUMP:
            acttionName = 'getJumpRunTwice' + str(self.actRandom) + 'Action'
            name = getattr(self.action, acttionName)(self)
        elif owner.jumpState == gametypes.DASH_TWICE_JUMP:
            acttionName = 'getJumpDashTwice' + str(self.actRandom) + 'Action'
            name = getattr(self.action, acttionName)(self)
        if not name:
            name = getattr(self.action, 'getJumpRunAction')(self)
        gamelog.debug('zfjump:2', name, owner.jumpState)
        return name

    def getJumpUpActionName(self):
        owner = BigWorld.entity(self.owner)
        name = None
        if owner.jumpState == gametypes.DEFAULT_JUMP:
            if owner.inRiding():
                name = getattr(self.action, 'getHorseJumpRunUpAction')(self)
            else:
                name = getattr(self.action, 'getJumpRunUpAction')(self)
        elif owner.jumpState == gametypes.DASH_JUMP:
            if owner.inRiding():
                name = getattr(self.action, 'getHorseJumpDashUpAction')(self)
            else:
                name = getattr(self.action, 'getJumpDashUpAction')(self)
        elif owner.jumpState == gametypes.AUTO_JUMP:
            if owner.inRiding():
                name = getattr(self.action, 'getHorseFallRunFlyAction')(self)
            else:
                name = self.action.getFallRunFlyAction(self)
        elif owner.jumpState == gametypes.DASH_AUTO_JUMP:
            if self.fallAutoJumpActRandom == 0:
                if owner.inRiding():
                    name = getattr(self.action, 'getHorseFallDashFlyAction')(self)
                else:
                    name = self.action.getFallDashFlyAction(self)
            elif owner.inRiding():
                name = getattr(self.action, 'getHorseFallDashFlyAction')(self)
            else:
                name = self.action.getFallDashFly1Action(self)
        elif owner.jumpState == gametypes.DASH_BIG_JUMP:
            if owner.inRiding():
                name = getattr(self.action, 'getHorseJumpDashUpAction')(self)
            else:
                name = getattr(self.action, 'getJumpDashUp1Action')(self)
        elif owner.jumpState == gametypes.DEFAULT_TWICE_JUMP:
            acttionName = 'getJumpRunTwiceUp' + str(self.actRandom) + 'Action'
            name = getattr(self.action, acttionName)(self)
        elif owner.jumpState == gametypes.DASH_TWICE_JUMP:
            acttionName = 'getJumpDashTwiceUp' + str(self.actRandom) + 'Action'
            name = getattr(self.action, acttionName)(self)
        if not name:
            name = getattr(self.action, 'getJumpRunUpAction')(self)
        gamelog.debug('zfjump:3', name, owner.jumpState)
        return name

    def getFallFlyActionName(self):
        owner = BigWorld.entity(self.owner)
        name = None
        if owner.jumpState == gametypes.DEFAULT_JUMP:
            if owner.inRiding():
                name = getattr(self.action, 'getHorseFallRunFlyAction')(self)
            else:
                name = self.action.getFallRunFlyAction(self)
        elif owner.jumpState == gametypes.DASH_JUMP:
            if owner.inRiding():
                name = getattr(self.action, 'getHorseFallDashFlyAction')(self)
            else:
                name = self.action.getFallDashFlyAction(self)
        elif owner.jumpState == gametypes.AUTO_JUMP:
            if owner.inRiding():
                name = getattr(self.action, 'getHorseFallRunDownAction')(self)
            else:
                name = self.action.getFallRunDownAction(self)
        elif owner.jumpState == gametypes.DASH_AUTO_JUMP:
            if self.fallAutoJumpActRandom == 0:
                if owner.inRiding():
                    name = getattr(self.action, 'getHorseFallDashDownAction')(self)
                else:
                    name = self.action.getFallDashDownAction(self)
            elif owner.inRiding():
                name = getattr(self.action, 'getHorseFallDashDownAction')(self)
            else:
                name = self.action.getFallDashDown1Action(self)
        elif owner.jumpState == gametypes.DASH_BIG_JUMP:
            if owner.inRiding():
                name = getattr(self.action, 'getHorseFallDashFlyAction')(self)
            else:
                name = self.action.getFallDashFly1Action(self)
        elif owner.jumpState == gametypes.DEFAULT_TWICE_JUMP:
            acttionName = 'getFallRunTwiceFly' + str(self.actRandom) + 'Action'
            name = getattr(self.action, acttionName)(self)
        elif owner.jumpState == gametypes.DASH_TWICE_JUMP:
            acttionName = 'getFallDashTwiceFly' + str(self.actRandom) + 'Action'
            name = getattr(self.action, acttionName)(self)
        if not name:
            name = self.action.getFallRunFlyAction(self)
        gamelog.debug('zfjump:4', name, owner.jumpState)
        return name

    def getFallActionName(self):
        owner = BigWorld.entity(self.owner)
        name = None
        if self.isPlayer:
            jumpback = owner.ap.backwardMagnitude > 0
        else:
            yaw = owner.yaw
            jumpback = owner.velocity.dot((math.sin(yaw), 0, math.cos(yaw))) < 0
        if owner.jumpState == gametypes.DEFAULT_JUMP:
            if owner.inRiding():
                name = getattr(self.action, 'getHorseFallRunDownAction')(self)
            else:
                name = self.action.getFallRunDownAction(self)
        elif owner.jumpState == gametypes.DASH_JUMP:
            if owner.inRiding():
                name = getattr(self.action, 'getHorseFallDashDownAction')(self)
            else:
                name = self.action.getFallDashDownAction(self)
        elif owner.jumpState in (gametypes.AUTO_JUMP, gametypes.DASH_AUTO_JUMP):
            pass
        elif owner.jumpState == gametypes.DASH_BIG_JUMP:
            if owner.inRiding():
                name = getattr(self.action, 'getHorseFallDashDownAction')(self)
            else:
                name = self.action.getFallDashDown1Action(self)
        elif owner.jumpState == gametypes.DEFAULT_TWICE_JUMP:
            acttionName = 'getFallRunTwiceDown' + str(self.actRandom) + 'Action'
            name = getattr(self.action, acttionName)(self)
            if not name:
                name = self.action.getFallRunDownAction(self)
        elif owner.jumpState == gametypes.DASH_TWICE_JUMP:
            acttionName = 'getFallDashTwiceDown' + str(self.actRandom) + 'Action'
            name = None
        gamelog.debug('zfjump:5', name, owner.jumpState, jumpback)
        return name

    def getFastFallActionName(self):
        acttionName = 'getFallDashTwiceDown1Action'
        name = getattr(self.action, acttionName)(self)
        return name

    def getFallEndActionName(self):
        owner = BigWorld.entity(self.owner)
        name = None
        isMoving = owner.inMoving()
        if self.isPlayer:
            if owner.getOperationMode() == gameglobal.MOUSE_MODE:
                jumpback = False
            else:
                jumpback = owner.ap._s
            isMoving = owner.ap.isMovingActionKeyControl() or owner.isPathfinding or owner.ap.isChasing
            if owner.qinggongState != gametypes.QINGGONG_STATE_FAST_DOWN:
                isMoving = isMoving or owner.ap._s
        else:
            yaw = owner.yaw
            jumpback = owner.velocity.dot((math.sin(yaw), 0, math.cos(yaw))) < 0
        if isMoving:
            if jumpback:
                if owner.inRiding():
                    name = getattr(self.action, 'getHorseFallRunBackEndAction')(self)
                else:
                    name = self.action.getFallRunBackEndAction(self)
            elif owner.jumpState in (gametypes.DEFAULT_JUMP, gametypes.AUTO_JUMP):
                if owner.inRiding():
                    name = getattr(self.action, 'getHorseFallRunEndRunAction')(self)
                elif not gameglobal.gDisablePlayStartAction and owner.jumpState == gametypes.DEFAULT_JUMP:
                    if self.isPlayer and not owner.ap.forwardMagnitude:
                        if owner.ap.rightwardMagnitude:
                            name = self.action.getFallRightRunEndRunAction(self)
                        elif owner.ap.leftwardMagnitude:
                            name = self.action.getFallLeftRunEndRunAction(self)
                        else:
                            name = self.getFallRunEndRunAction()
                    else:
                        name = self.getFallRunEndRunAction()
                else:
                    name = self.getFallRunEndRunAction()
            elif owner.jumpState in (gametypes.DASH_JUMP,
             gametypes.DASH_BIG_JUMP,
             gametypes.DASH_TWICE_JUMP,
             gametypes.DASH_AUTO_JUMP):
                if owner.inRiding():
                    name = getattr(self.action, 'getHorseFallDashEndDashAction')(self)
                elif owner.qinggongMgr.getDistanceFromWater():
                    name = self.getFallRunEndRunAction()
                else:
                    name = self.action.getFallDashEndDashAction(self)
            elif owner.jumpState == gametypes.DEFAULT_TWICE_JUMP:
                acttionName = 'getFallRunTwiceEndRun' + str(self.actRandom) + 'Action'
                name = getattr(self.action, acttionName)(self)
                if not gameglobal.gDisablePlayStartAction:
                    if self.isPlayer and not owner.ap.forwardMagnitude:
                        if owner.ap.rightwardMagnitude:
                            name = self.action.getFallRightRunEndRunAction(self)
                        elif owner.ap.leftwardMagnitude:
                            name = self.action.getFallLeftRunEndRunAction(self)
            elif owner.jumpState == gametypes.DASH_TWICE_JUMP:
                acttionName = 'getFallDashTwiceEndDash' + str(self.actRandom) + 'Action'
                name = getattr(self.action, acttionName)(self)
        elif owner.jumpState in (gametypes.DEFAULT_JUMP, gametypes.AUTO_JUMP):
            if owner.inRiding():
                name = getattr(self.action, 'getHorseFallRunEndIdleAction')(self)
            else:
                name = self.action.getFallRunEndIdleAction(self)
        elif owner.jumpState in (gametypes.DASH_JUMP, gametypes.DASH_AUTO_JUMP):
            if owner.inRiding():
                name = getattr(self.action, 'getHorseFallDashEndIdleAction')(self)
            else:
                name = self.action.getFallDashEndIdleAction(self)
        elif owner.jumpState == gametypes.DASH_BIG_JUMP:
            if owner.inRiding():
                name = getattr(self.action, 'getHorseFallDashEndIdleAction')(self)
            else:
                name = self.action.getFallDashEndIdle1Action(self)
        elif owner.jumpState == gametypes.DEFAULT_TWICE_JUMP:
            acttionName = 'getFallRunTwiceEndIdle' + str(self.actRandom) + 'Action'
            name = getattr(self.action, acttionName)(self)
        elif owner.jumpState == gametypes.DASH_TWICE_JUMP:
            acttionName = 'getFallDashTwiceEndIdle' + str(self.actRandom) + 'Action'
            name = getattr(self.action, acttionName)(self)
        gamelog.debug('zfjump:6', name, owner.jumpState, isMoving)
        return name

    def getFallRunEndRunAction(self):
        return getattr(self.action, 'getFallRunEndRunAction')(self)

    def getLeaveHorseEndAction(self):
        owner = BigWorld.entity(self.owner)
        if getattr(owner, 'rideTogetherDownHorse', False):
            owner.rideTogetherDownHorse = False
            return self.action.getLeaveHorseEndAction(self)

    def getHorseSprintStopAction(self):
        owner = BigWorld.entity(self.owner)
        if getattr(owner, 'sprintSpeeding', False):
            return self.action.getHorseSprintStop1Action(self)
        else:
            return self.action.getHorseSprintStopAction(self)

    def getHorseRoarJumpAction(self):
        return self.action.getHorseRoarJumpAction(self)

    def getDashStartAction(self):
        owner = BigWorld.entity(self.owner)
        if owner.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
            return self.action.getSprintHorseForwardStartAction(self)
        return self.action.getDashStartAction(self)

    def getDashStopAction(self):
        return self.action.getDashStopAction(self)

    def isInZaiju(self, ent):
        if not ent:
            return False
        return getattr(ent, 'isOnWingWorldCarrier', False)
