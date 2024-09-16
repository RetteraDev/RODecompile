#Embedded file name: /WORKSPACE/data/entities/client/helpers/avatarphysics.o
import math
import inspect
import BigWorld
import C_ui
import Math
import Pixie
import time
import gameglobal
import gametypes
import keys
import action
import gamelog
import const
import utils
import formula
import clientUtils
from callbackHelper import Functor
from guis import hotkey as HK
from guis import hotkeyProxy
from guis import cursor
from guis import ui
from helpers import qingGong
from helpers import cellCmd
from sfx import sfx
from sfx import keyboardEffect
from sfx import physicsEffect
from Transport import Transport
from Obstacle import Obstacle
from cdata import game_msg_def_data as GMDD
from data import sys_config_data as SYSCD
from data import physics_config_data as PCD
from data import couple_emote_basic_data as CEBD
from data import speed_field_data as SFD
from data import space_collide_msg_data as SCMD
from data import zaiju_data as ZD
from data import duel_config_data as DCD
STOP_DIRECTION_STRAIGHT = 0
STOP_DIRECTION_LEFT = 1
STOP_DIRECTION_RIGHT = 2

class AvatarPhysics(object):
    SEEK_TOLERANCE = 0.2
    SEEK_TIME = 300
    SIN_OF_45 = 0.707107
    VERTICAL_SIN = 0.5774
    DOUBLE_JUMP_TOLERANCE = 0.1
    SPACE_JUMP_TIME_INTERVAL = 0.2
    JUMP_TOP_TIMES = 20
    QINGGONG_SRPINT_INTERVAL = 1.1
    SWIM_SPEED_FACTOR = 0.7
    WATERUNDEREFFECT = 80000
    WATERJUMPEFFECT = 80001
    TARGET_LOCKED_STATE_DEFAULT = 0
    TARGET_LOCKED_STATE_IN = 1
    TARGET_LOCKED_STATE_OUT = 2

    def __init__(self):
        super(AvatarPhysics, self).__init__()
        self.forwardMagnitude = 0.0
        self.backwardMagnitude = 0.0
        self.upwardMagnitude = 0.0
        self.rightwardMagnitude = 0.0
        self.leftwardMagnitude = 0.0
        self.normalWalkSpeed = 0.0
        self.speedMultiplier = 1.0
        self.upSpeedMultiplier = PCD.data.get('runUpSpeed', gametypes.RUNUP_SPEED)
        self.gravity = gametypes.NOMAL_DOWNGRAVITY
        self.isWalking = False
        self.isRunning = True
        self.isTracing = False
        self.traceFailCount = 0
        self.turnSpeed = gameglobal.dcTurnSpeed
        self.ccamera = gameglobal.rds.cam.cc
        self.dcursor = BigWorld.dcursor()
        self.setPhysicsFromModel()
        self.isChasing = False
        self.chasingEntity = None
        self.chaseNum = 0
        self.ccamera.allResetYaw = False
        self.isJumpEnd = False
        self._a = False
        self._d = False
        self._q = False
        self._e = False
        self._w = False
        self._s = False
        self._x = False
        self._space = False
        self._msleft = False
        self._msright = False
        self._forward = False
        self._backward = False
        self._moveleft = False
        self._moveright = False
        self._turnleft = False
        self._turnright = False
        self._moveUp = False
        self._moveDown = False
        self._leftForward = False
        self._rightForward = False
        self._leftBackward = False
        self._rightBackward = False
        self._upWard = False
        self._downWard = False
        self.jumpCnt = 0
        self.realJumpTime = 0.0
        self.realKeyUpTime = 0.0
        self.realSpaceKeyTime = 0.0
        self.realDashTime = 0.0
        self.navigation = sfx.Navigation()
        self.groupMapMarkCircle = sfx.GroupMapMarkCircle()
        self._wKeyTime = 0.0
        self._qKeyTime = 0.0
        self._sKeyTime = 0.0
        self._eKeyTime = 0.0
        self._xKeyTime = 0.0
        self._spaceKeyTime = 0.0
        self.jumpTopCnt = 0
        self.needDoJump = True
        self.disableTracker = False
        self.needForceEndQingGong = False
        self.needKeyInvert = False
        self.forceSeek = False
        self.dcRotateInSeek = False
        self.inLoadingProgress = False
        self._autorunStime = 0
        self.isAutoMoving = False
        self.flyType = gameglobal.DEFAUL_FLY
        self.moveAfterJump = False
        self.autoMoveTimespan = SYSCD.data.get('autoMoveTimespan', 3.0)
        self.targetLockedCallback = None
        self.targetLockEffectUnit = None
        self.targetLockConnector = None
        self.targetLockEffectState = AvatarPhysics.TARGET_LOCKED_STATE_DEFAULT
        self.inMouseSelectSkillPos = False
        self.lockedEffInRange = clientUtils.pixieFetch(sfx.getPath(SYSCD.data.get('targetLockedEffectInRange', 0)))
        self.lockedEffInRange.setAttachMode(0, 1, 0)
        self.lockedEffInRange.force()
        self.lockedEffOutRange = clientUtils.pixieFetch(sfx.getPath(SYSCD.data.get('targetLockedEffectOutRange', 0)))
        self.lockedEffOutRange.setAttachMode(0, 1, 0)
        self.lockedEffOutRange.force()
        self.lastVelocity = None
        self.stopDirection = STOP_DIRECTION_STRAIGHT
        self.displacementSpeed = None

    def reset(self):
        self.ccamera.canRotate = False
        self.dcursor.canRotate = False
        cursor.setInAndRestoreOldPos()
        C_ui.cursor_show(True)
        gameglobal.rds.ui.actionbar.showMouseIcon(False)

    def forceAllKeysUp(self):
        self._a = False
        self._d = False
        self._q = False
        self._e = False
        self._w = False
        self._s = False
        self._space = False
        self._x = False
        self._msleft = False
        self._msright = False
        self._forward = False
        self._backward = False
        self._moveleft = False
        self._moveright = False
        self._turnleft = False
        self._turnright = False
        self._moveUp = False
        self._moveDown = False
        self._wKeyTime = 0.0
        self._qKeyTime = 0.0
        self._sKeyTime = 0.0
        self._eKeyTime = 0.0
        self._xKeyTime = 0.0
        self._spaceKeyTime = 0.0

    def startMarkMap(self, needUpdate = False):
        self.mapMarkingPosition(needUpdate)
        if ui.get_cursor_state() != ui.MARK_MAP_STATE:
            ui.reset_cursor()
            ui.set_cursor_state(ui.MARK_MAP_STATE)
            ui.set_cursor(cursor.mark_map)
            ui.lock_cursor()

    def mapMarkingPosition(self, needUpdate = False):
        if self.player.target == None:
            self.ccamera.allResetYaw = False
            result = BigWorld.getCursorPosInWorld(self.player.spaceID, 1000, False, (gameglobal.TREEMATTERKINDS, gameglobal.GLASSMATTERKINDS))
            process = False
            vehicleID = 0
            if result[1] != None:
                en = BigWorld.entity(result[1])
                if en != None:
                    if hasattr(en, 'itemSelected'):
                        process = en.itemSelected(result, self.on_clicked, 2)
                    if en.model and hasattr(en.model, 'vehicleID') and en.model.vehicleID == en.id:
                        vehicleID = en.id
            if result[0] != None and not process:
                if not self.player.spellingType:
                    if self.player.stateMachine.checkMove():
                        self.groupMapMarkCircle.start(result[0], result[3] == 256, vehicleID, needUpdate)

    def _key_mr_down(self, isDown):
        if self.groupMapMarkCircle.isInGroupMapMarkStatus():
            self.groupMapMarkCircle.stop()

    def setPlayerPhysics(self, player, style):
        if not hasattr(player, 'physics'):
            player.physics = style
        player.physics.velocity = (0.0, 0.0, 0.0)
        player.physics.velocityMouse = 'Direction'
        player.physics.angular = 0
        player.physics.angularMouse = 'MouseX'
        player.physics.collide = True
        player.physics.collisionPush = False
        player.physics.fall = True
        player.physics.jumpTopNotifier = self.jumpTop
        player.physics.jumpEndNotifier = self.jumpEnd
        player.physics.breakJumpNotifier = self.breakJumpCallback
        player.physics.isMovingNotifier = self.physicsMovingNotifier
        player.physics.collideWithPlayerNotifier = self.collideWithPlayerCallback
        player.physics.actionPromoteNotifier = self.actionPromoteCallback
        player.physics.collideNotifier = self.collideCallback
        player.physics.dieNotifier = self.dieCallback
        player.physics.acceleratingEndNotifier = self.acceleratingEndNotifier
        if hasattr(player.physics, 'needPromotionVelY'):
            player.physics.needPromotionVelY = True
        self.player = player
        self.physics = player.physics
        self.apEffectEx = self.player.apEffectEx
        self.apEffectEx.setPlayer(self.player)
        if gameglobal.rds.GameState > gametypes.GS_LOADING:
            self.player.setGravity(gametypes.NOMAL_DOWNGRAVITY, False)

    def physicsMovingNotifier(self, isMoving):
        if hasattr(self.player, 'movingNotifier'):
            self.player.apEffectEx.physicsMovingNotifier(isMoving)

    def collideWithPlayerCallback(self, eid):
        en = BigWorld.entities.get(eid)
        if hasattr(en, 'playCollideAction'):
            en.playCollideAction()
        gamelog.debug('collideWithPlayerCallback:', eid)

    def isMovingActionKeyControl(self):
        return False

    def initTracker(self):
        pass

    def beginHeadTracker(self):
        pass

    def stopHeadTracker(self):
        pass

    def detachHeadTracker(self):
        pass

    def setSpeed(self, speed):
        if speed < 0.1:
            return
        self.runFwdSpeed = speed
        self.runBackSpeed = self.runFwdSpeed * 0.6
        self.updateVelocity()

    def setWalkSpeed(self, speed):
        self.normalWalkSpeed = speed
        self.walkFwdSpeed = speed
        self.walkBackSpeed = self.normalWalkSpeed * SYSCD.data.get('walkBackSpeedFactor', 0.6)
        self.updateVelocity()

    def setUpSpeedMultiplier(self):
        p = self.player
        if p.jumpState == gametypes.DEFAULT_JUMP:
            self.setRunUpSpeed()
        elif p.jumpState == gametypes.DASH_JUMP:
            p = BigWorld.player()
            isInHorse = p.inRiding() and p.bianshen[0] == gametypes.BIANSHEN_RIDING_RB
            if isInHorse:
                self.upSpeedMultiplier = PCD.data.get('horseDashUpSpeed', gametypes.HORSE_DASHUP_SPEED)
                self.physics.upSpeedAttenu = PCD.data.get('horseDashUpSpeedAttenu', gametypes.HORSE_DASHUP_SPEED_ATTENU)
            else:
                self.upSpeedMultiplier = PCD.data.get('dashUpSpeed', gametypes.DASHUP_SPEED)
                self.physics.upSpeedAttenu = PCD.data.get('dashUpSpeedAttenu', gametypes.DASHUP_SPEED_ATTENU)
        elif p.jumpState == gametypes.DASH_BIG_JUMP:
            self.upSpeedMultiplier = PCD.data.get('dashUpSpeed1', gametypes.DASHUP_SPEED1)
            self.physics.upSpeedAttenu = PCD.data.get('dashUpSpeed1Attenu', gametypes.DASHUP_SPEED1_ATTENU)
        elif p.jumpState == gametypes.AUTO_JUMP:
            self.upSpeedMultiplier = SYSCD.data.get('autoJumpUpSpeed', gametypes.AUTO_JUMP_UP_SPEED)
        elif p.jumpState == gametypes.DASH_AUTO_JUMP:
            self.upSpeedMultiplier = SYSCD.data.get('dashAutoJumpUpSpeed', gametypes.DASH_AUTO_JUMP_UP_SPEED)
        elif p.jumpState == gametypes.DEFAULT_TWICE_JUMP:
            self.upSpeedMultiplier = SYSCD.data.get('runUpTwiceSpeed', gametypes.RUNUPTWICE_SPEED)
            self.physics.upSpeedAttenu = PCD.data.get('runUpTwiceSpeedAttenu', gametypes.RUNUPTWICE_SPEED_ATTENU)
        elif p.jumpState == gametypes.DASH_TWICE_JUMP:
            self.upSpeedMultiplier = PCD.data.get('dashUpTwiceSpeed', gametypes.DASHUPTWICE_SPEED)
            self.physics.upSpeedAttenu = PCD.data.get('dashUpTwiceSpeedAttenu', gametypes.DASHUPTWICE_SPEED_ATTENU)
        elif p.inDanDao:
            self.upSpeedMultiplier = PCD.data.get('danDaoFlyUpSpeed', 20)
            self.physics.upSpeedAttenu = PCD.data.get('danDaoUpSpeedAttenu', 1)
        if self.player.isDashing:
            if self.player.inSwim:
                self.setRunUpSpeed()

    def setRunUpSpeed(self):
        p = BigWorld.player()
        isInHorse = p.inRiding() and p.bianshen[0] == gametypes.BIANSHEN_RIDING_RB
        if isInHorse:
            self.upSpeedMultiplier = PCD.data.get('horseRunUpSpeed', gametypes.HORSE_RUNUP_SPEED)
            self.physics.upSpeedAttenu = PCD.data.get('horseRunUpSpeedAttenu', gametypes.HORSE_RUNUP_SPEED_ATTENU)
        else:
            self.upSpeedMultiplier = PCD.data.get('runUpSpeed', gametypes.RUNUP_SPEED)
            self.physics.upSpeedAttenu = PCD.data.get('runUpSpeedAttenu', gametypes.RUNUP_SPEED_ATTENU)

    def setPhysicsFromModel(self, speedData = {}):
        if self.normalWalkSpeed:
            self.walkFwdSpeed = self.normalWalkSpeed * speedData.get('walkFactor', 1.0)
            self.walkBackSpeed = self.normalWalkSpeed * SYSCD.data.get('walkBackSpeedFactor', 0.6) * speedData.get('walkBackFactor', 1.0)
        else:
            self.walkFwdSpeed = self.walkBackSpeed = 0
        self.runFwdSpeed = self.getRunForwardSpeedBase(speedData)
        self.runBackSpeed = self.getRunBackwardSpeedBase(speedData)
        self.dashBackSpeed = self.getDashBackwardSpeed(speedData)
        self.swimWalkFwdSpeed = self.getSwimWalkSpeedBase(speedData)
        self.swimWalkBackSpeed = self.getSwimWalkBackSpeedBase(speedData)
        self.swimRunFwdSpeed = self.getSwimRunSpeedBase(speedData)
        self.swimRunBackSpeed = self.getSwimRunBackSpeedBase(speedData)
        self.swimDashSpeed = self.getSwimDashSpeedBase(speedData)
        self.speedMultiplier = 1.0

    def reload(self):
        pass

    def switchToRun(self, needForce = False):
        if self.realKeyUpTime - self.realSpaceKeyTime < AvatarPhysics.SPACE_JUMP_TIME_INTERVAL and not needForce:
            return
        if self.player.qinggongState in gametypes.QINGGONG_STATE_DASH_SET or self.player.isDashing and not self.player.isJumping:
            self.player.isDashing = False
            self.player.setGravity(gametypes.NOMAL_DOWNGRAVITY)
            self.player.jumpState = gametypes.DEFAULT_JUMP
            self.setUpSpeedMultiplier()
            self.player.qinggongMgr.setState(qingGong.STATE_IDLE)
            self.player.qinggongMgr.stopWindSound()
            gameglobal.rds.cam.leaveDashFov()
            self.updateVelocity()
            cellCmd.endUpQinggongState()

    def switchToWalk(self, isDown):
        if isDown:
            if not self.isWalking:
                self.isWalking = True
                self.isRunning = False
                self.upSpeedMultiplier = gametypes.WALKUP_SPEED
                self.player.showTopMsg('切换成行走状态')
            else:
                self.isWalking = False
                self.isRunning = True
                self.setUpSpeedMultiplier()
                self.player.showTopMsg('切换成跑步状态')
            self.player.restoreGravity()
            if not self.player.qinggongMgr.isJumping():
                self.player.qinggongMgr.setState(qingGong.STATE_IDLE)
            self.updateVelocity()
            cellCmd.endUpQinggongState()

    def isKeyBoardMove(self):
        return False

    def _approach(self, success):
        utils.recusionLog(2)
        gamelog.debug('_approach:', success)
        if self.player.getOperationMode() == gameglobal.MOUSE_MODE and self.isKeyBoardMove():
            pass
        elif not (getattr(self.player, 'inChaoFeng', False) or getattr(self.player, 'inMeiHuo', False)):
            self.forwardMagnitude = 0
        self.player.model.yaw = self.player.yaw
        dc = BigWorld.dcursor()
        dc.canRotate = self.dcRotateInSeek
        if success == 1:
            if self.isChasing and self.chasingEntity and self.chasingEntity.inWorld:
                self.player.reachDesiredDist()
            self.isChasing = False
            self.chasingEntity = None
            self.ccamera.allResetYaw = False
        elif success == -1:
            self.isChasing = False
            self.chasingEntity = None
            self.ccamera.allResetYaw = False
        self.chaseNum = 0
        self.updateMoveControl()
        if not self.navigation.updateFlag:
            self.navigation.stop()

    def beginForceMove(self, point, needCollide = True):
        self.beginForceMoveWithCallback(point, self._endForceMove, needCollide)

    def _endForceMove(self, success):
        p = self.player
        if success != 1:
            gamelog.error('Error....***ForceMove Failed*** ')
        if self.player.isPin:
            self.physics.forbidHorizontalMove = True
        p.isAscending = False
        self.physics.fall = True
        self.forceSeek = False
        self.physics.collide = True
        self._approach(success)
        self.stopMove()
        self._recalcSpeed()
        self.updateVelocity()

    def beginForceMoveWithCallback(self, point, callback, needCollide = True, isHorizonSpeed = False):
        if self.player.isPin:
            self.physics.forbidHorizontalMove = False
        self.forceSeek = True
        self.physics.collide = needCollide
        dc = BigWorld.dcursor()
        self.dcRotateInSeek = dc.canRotate
        dc.canRotate = False
        self.physics.seek((point.x,
         point.y,
         point.z,
         dc.yaw), self.SEEK_TIME, self.SEEK_TOLERANCE, callback)
        vel = point - self.player.position
        vel.normalise()
        yaw = vel.yaw - dc.yaw
        dir = point - self.player.position
        if isHorizonSpeed:
            dir.y = 0
            dir.normalise()
            verticalSpeed = 0
            horizonSpeed = self.runFwdSpeed
        else:
            dir.normalise()
            verticalSpeed = self.runFwdSpeed * dir.y
            horizonSpeed = self.runFwdSpeed * math.sqrt(dir.x * dir.x + dir.z * dir.z)
        self.physics.velocity = Math.Vector3(horizonSpeed * math.sin(yaw), verticalSpeed, horizonSpeed * math.cos(yaw))
        self.physics.maxTopVelocity = Math.Vector3(horizonSpeed * math.sin(yaw), verticalSpeed, horizonSpeed * math.cos(yaw))
        gamelog.debug('jorsef: beginForceMoveWithCallback', self.physics.velocity, point)
        self.player.isAscending = True

    def forceMoveCamera(self, isDown):
        pass

    def intoForceMove(self):
        pass

    def leaveForceMove(self):
        pass

    def handleKeyEvent(self, isDown, key, mods):
        p = BigWorld.player()
        isDown, key, mods, oldKey = hotkeyProxy.filterModsKey(isDown, key, mods)
        if key in (keys.KEY_MOUSE0, keys.KEY_MOUSE1):
            rdfkey = HK.keyDef(key, 1, 0)
        else:
            rdfkey = HK.keyDef(key, 1, mods)
        actionFlag = False
        for downKeys, upKeySets, actionVal in self.keyBindings:
            if self.player.clientControl or not self.player.clientControl and key in (keys.KEY_MOUSE0, keys.KEY_MOUSE1) and not isDown:
                pass
            else:
                return
            if rdfkey in downKeys:
                okayToGo = 1
                for downKey in downKeys:
                    if okayToGo:
                        okayToGo = downKey.isAnyDown() or oldKey and BigWorld.getKeyDownState(oldKey, 0) and BigWorld.getKeyDownState(key, 0)
                    else:
                        break

                if okayToGo:
                    for upKeys in upKeySets:
                        if not upKeys:
                            continue
                        allDown = 1
                        for upKey in upKeys:
                            if allDown:
                                allDown = upKey.isAnyDown()
                            else:
                                break

                        okayToGo = okayToGo and not allDown

                actionFlag = True
                for conflictKey, actions in p.conflictKeyDict.iteritems():
                    if actions[0] != actionVal:
                        if conflictKey.inkeyDef(rdfkey.key, rdfkey.mods) or conflictKey.inkeyDef(rdfkey.key2, rdfkey.mods2):
                            conflictAction = actions[1]
                            arginfo = inspect.getargspec(conflictAction)
                            if len(arginfo.args) > 1:
                                conflictAction(conflictKey, rdfkey)
                            else:
                                conflictAction()

                actionVal(okayToGo)

        self.checkShowCursor()
        if not self.isTracing and actionFlag:
            self.updateVelocity()
        if getattr(gameglobal.rds, 'isFlashWindow', False):
            gameglobal.rds.isFlashWindow = False
            BigWorld.flashWindow(0)

    def checkShowCursor(self):
        opMode = self.player.getOperationMode()
        isInBfDotaChooseHero = getattr(self.player, 'isInBfDotaChooseHero', False)
        if not isInBfDotaChooseHero and (opMode == gameglobal.KEYBOARD_MODE and (self._msleft or self._msright) or opMode == gameglobal.MOUSE_MODE and self._msright or opMode == gameglobal.ACTION_MODE and self.actionNeedHideCursor()):
            C_ui.cursor_show(False)
            if not cursor.oldCursorPosValid():
                if not C_ui.cursor_in_clientRect() and opMode == gameglobal.ACTION_MODE:
                    C_ui.cursor_show(True)
                else:
                    cursor.setOutAndSaveOldPos()
            elif opMode == gameglobal.ACTION_MODE:
                cursor.setOutAndSaveOldPos()
        else:
            cursor.setInAndRestoreOldPos()
            C_ui.cursor_show(True)
            if self.player.chooseEffect.isShowingEffect and getattr(self.player, 'needUpdateChoosePos', False):
                cPos = self.player.chooseEffect.lastCursorPos
                if cPos:
                    C_ui.set_cursor_pos(cPos[0][0], cPos[0][1])
                self.player.needUpdateChoosePos = False

    def actionNeedHideCursor(self):
        p = BigWorld.player()
        isInBfDotaChooseHero = False
        if p:
            isInBfDotaChooseHero = getattr(p, 'isInBfDotaChooseHero', False)
        if isInBfDotaChooseHero:
            return False
        if self.player.isInApprenticeTrain() or self.player.isInApprenticeBeTrain():
            if self._msleft or self._msright:
                return True
            else:
                return False
        if not BigWorld.player().ap.showCursor and not gameglobal.isWidgetNeedShowCursor and gameglobal.rds.GameState == gametypes.GS_PLAYGAME and not gameglobal.rds.ui.chat.isInputAreaVisible:
            return True
        if BigWorld.player().ap.showCursor and (self._msleft or self._msright):
            return True
        if gameglobal.isWidgetNeedShowCursor and (self._msleft or self._msright):
            return True
        return False

    def _combinationKey(self):
        if self.player.inPUBGParachute():
            return
        if self.player.inPUBGPlane():
            return
        if self._leftForward and (self._forward or self.isAutoMoving) and not self._moveleft or self._rightForward and (self._forward or self.isAutoMoving) and not self._moveright:
            self.moveForward(True)
        if self._leftForward and self._moveleft and not (self._forward or self.isAutoMoving) or self._leftBackward and self._moveleft and not (self._forward or self.isAutoMoving):
            self.moveLeft(True)
        if self._rightForward and self._moveright and not (self._forward or self.isAutoMoving) or self._rightBackward and self._moveright and not self._backward:
            self.moveRight(True)
        if self._leftBackward and self._backward and not self._moveleft or self._rightBackward and self._backward and not self._moveright:
            self.moveBackward(True)
        self._leftForward = self._moveleft and (self._forward or self.isAutoMoving)
        self._rightForward = self._moveright and (self._forward or self.isAutoMoving)
        self._leftBackward = self._moveleft and self._backward
        self._rightBackward = self._moveright and self._backward
        self._upWard = self._space
        self._downWard = self._x
        self.moveLeftForward(self._leftForward)
        self.moveRightForward(self._rightForward)
        self.moveLeftBackward(self._leftBackward)
        self.moveRightBackward(self._rightBackward)
        if self.player.canFly() and not self.player.lockHotKey:
            self.moveVerticalWard()

    def moveVerticalWard(self):
        if not self.player.checkTempGroupFollow(False):
            return
        if gameglobal.rds.ui.chat.isInputAreaVisible:
            return
        if gameglobal.rds.ui.bInEdit:
            return
        if not self.player.stateMachine.checkMove():
            return
        if not self.player.stateMachine.checkStatus(const.CT_INIT_MOVE):
            return
        _w = False if self.player.needForbidForwardOp() else HK.HKM[HK.KEY_FORWARD].isAnyDown()
        _q = False if self.player.needForbidSideOp() else HK.HKM[HK.KEY_MOVELEFT].isAnyDown()
        _e = False if self.player.needForbidSideOp() else HK.HKM[HK.KEY_MOVERIGHT].isAnyDown()
        _s = False if self.player.needForbidBackOp() else HK.HKM[HK.KEY_BACKWARD].isAnyDown()
        _space = HK.HKM[keys.KEY_SPACE].isAnyDown()
        _x = HK.HKM[HK.KEY_DOWN].isAnyDown()
        _leftForward = _w and _q
        _rightForward = _w and _e
        _leftBackward = _s and _q
        _rightBackward = _s and _e
        _upWard = _space
        _downWard = _x
        if self.player.qinggongState in gametypes.QINGGONG_WINGFLY_STATES:
            self.player.fashion.stopAction()
            if not self.player.inFlyTypeFlyRide():
                self.player.qinggongMgr.stopWingFlyModelAction()
            else:
                self.player.fashion.stopModelAction(self.player.modelServer.rideModel)
        maxVelocity = utils.getFlyRushMaxSpeed(self.player)
        if _upWard:
            if _leftForward:
                self.leftwardMagnitude = AvatarPhysics.VERTICAL_SIN
                self.forwardMagnitude = AvatarPhysics.VERTICAL_SIN
                self.upwardMagnitude = AvatarPhysics.VERTICAL_SIN
                self.physics.maxTopVelocity = (maxVelocity * AvatarPhysics.VERTICAL_SIN, maxVelocity * AvatarPhysics.VERTICAL_SIN, maxVelocity * AvatarPhysics.VERTICAL_SIN)
            elif _rightForward:
                self.rightwardMagnitude = AvatarPhysics.VERTICAL_SIN
                self.forwardMagnitude = AvatarPhysics.VERTICAL_SIN
                self.upwardMagnitude = AvatarPhysics.VERTICAL_SIN
                self.physics.maxTopVelocity = (maxVelocity * AvatarPhysics.VERTICAL_SIN, maxVelocity * AvatarPhysics.VERTICAL_SIN, maxVelocity * AvatarPhysics.VERTICAL_SIN)
            elif _leftBackward:
                self.leftwardMagnitude = AvatarPhysics.VERTICAL_SIN
                self.backwardMagnitude = AvatarPhysics.VERTICAL_SIN
                self.upwardMagnitude = AvatarPhysics.VERTICAL_SIN
                self.physics.maxTopVelocity = (maxVelocity * AvatarPhysics.VERTICAL_SIN, maxVelocity * AvatarPhysics.VERTICAL_SIN, maxVelocity * AvatarPhysics.VERTICAL_SIN)
            elif _rightBackward:
                self.rightwardMagnitude = AvatarPhysics.VERTICAL_SIN
                self.backwardMagnitude = AvatarPhysics.VERTICAL_SIN
                self.upwardMagnitude = AvatarPhysics.VERTICAL_SIN
                self.physics.maxTopVelocity = (maxVelocity * AvatarPhysics.VERTICAL_SIN, maxVelocity * AvatarPhysics.VERTICAL_SIN, maxVelocity * AvatarPhysics.VERTICAL_SIN)
            elif _w:
                self.forwardMagnitude = AvatarPhysics.SIN_OF_45
                self.upwardMagnitude = AvatarPhysics.SIN_OF_45
                self.physics.maxTopVelocity = (0, maxVelocity * AvatarPhysics.SIN_OF_45, maxVelocity * AvatarPhysics.SIN_OF_45)
            elif _s:
                self.backwardMagnitude = AvatarPhysics.SIN_OF_45
                self.upwardMagnitude = AvatarPhysics.SIN_OF_45
                self.physics.maxTopVelocity = (0, maxVelocity * AvatarPhysics.SIN_OF_45, maxVelocity * AvatarPhysics.SIN_OF_45)
            elif _q:
                self.leftwardMagnitude = AvatarPhysics.SIN_OF_45
                self.upwardMagnitude = AvatarPhysics.SIN_OF_45
                self.physics.maxTopVelocity = (maxVelocity * AvatarPhysics.SIN_OF_45, maxVelocity * AvatarPhysics.SIN_OF_45, 0)
            elif _e:
                self.rightwardMagnitude = AvatarPhysics.SIN_OF_45
                self.upwardMagnitude = AvatarPhysics.SIN_OF_45
                self.physics.maxTopVelocity = (maxVelocity * AvatarPhysics.SIN_OF_45, maxVelocity * AvatarPhysics.SIN_OF_45, 0)
            else:
                self.upwardMagnitude = 1
                self.physics.maxTopVelocity = (0, maxVelocity, 0)
            self.playVerticalAction(_upWard, _downWard)
        elif _downWard:
            if _leftForward:
                self.leftwardMagnitude = AvatarPhysics.VERTICAL_SIN
                self.forwardMagnitude = AvatarPhysics.VERTICAL_SIN
                self.upwardMagnitude = -AvatarPhysics.VERTICAL_SIN
                self.physics.maxTopVelocity = (maxVelocity * AvatarPhysics.VERTICAL_SIN, maxVelocity * AvatarPhysics.VERTICAL_SIN, maxVelocity * AvatarPhysics.VERTICAL_SIN)
            elif _rightForward:
                self.rightwardMagnitude = AvatarPhysics.VERTICAL_SIN
                self.forwardMagnitude = AvatarPhysics.VERTICAL_SIN
                self.upwardMagnitude = -AvatarPhysics.VERTICAL_SIN
                self.physics.maxTopVelocity = (maxVelocity * AvatarPhysics.VERTICAL_SIN, maxVelocity * AvatarPhysics.VERTICAL_SIN, maxVelocity * AvatarPhysics.VERTICAL_SIN)
            elif _leftBackward:
                self.leftwardMagnitude = AvatarPhysics.VERTICAL_SIN
                self.backwardMagnitude = AvatarPhysics.VERTICAL_SIN
                self.upwardMagnitude = -AvatarPhysics.VERTICAL_SIN
                self.physics.maxTopVelocity = (maxVelocity * AvatarPhysics.VERTICAL_SIN, maxVelocity * AvatarPhysics.VERTICAL_SIN, maxVelocity * AvatarPhysics.VERTICAL_SIN)
            elif _rightBackward:
                self.rightwardMagnitude = AvatarPhysics.VERTICAL_SIN
                self.backwardMagnitude = AvatarPhysics.VERTICAL_SIN
                self.upwardMagnitude = -AvatarPhysics.VERTICAL_SIN
                self.physics.maxTopVelocity = (maxVelocity * AvatarPhysics.VERTICAL_SIN, maxVelocity * AvatarPhysics.VERTICAL_SIN, maxVelocity * AvatarPhysics.VERTICAL_SIN)
            elif _w:
                self.forwardMagnitude = AvatarPhysics.SIN_OF_45
                self.upwardMagnitude = -AvatarPhysics.SIN_OF_45
                self.physics.maxTopVelocity = (0, maxVelocity * AvatarPhysics.SIN_OF_45, maxVelocity * AvatarPhysics.SIN_OF_45)
            elif _s:
                self.backwardMagnitude = AvatarPhysics.SIN_OF_45
                self.upwardMagnitude = -AvatarPhysics.SIN_OF_45
                self.physics.maxTopVelocity = (0, maxVelocity * AvatarPhysics.SIN_OF_45, maxVelocity * AvatarPhysics.SIN_OF_45)
            elif _q:
                self.leftwardMagnitude = AvatarPhysics.SIN_OF_45
                self.upwardMagnitude = -AvatarPhysics.SIN_OF_45
                self.physics.maxTopVelocity = (maxVelocity * AvatarPhysics.SIN_OF_45, -maxVelocity * AvatarPhysics.SIN_OF_45, 0)
            elif _e:
                self.rightwardMagnitude = AvatarPhysics.SIN_OF_45
                self.upwardMagnitude = -AvatarPhysics.SIN_OF_45
                self.physics.maxTopVelocity = (maxVelocity * AvatarPhysics.SIN_OF_45, maxVelocity * AvatarPhysics.SIN_OF_45, 0)
            else:
                self.upwardMagnitude = -1
                self.physics.maxTopVelocity = (0, -maxVelocity, 0)
            self.playVerticalAction(_upWard, _downWard)
        elif _leftForward:
            self.leftwardMagnitude = AvatarPhysics.SIN_OF_45
            self.forwardMagnitude = AvatarPhysics.SIN_OF_45
            self.physics.maxTopVelocity = (maxVelocity * AvatarPhysics.SIN_OF_45, 0, maxVelocity * AvatarPhysics.SIN_OF_45)
        elif _rightForward:
            self.rightwardMagnitude = AvatarPhysics.SIN_OF_45
            self.forwardMagnitude = AvatarPhysics.SIN_OF_45
            self.physics.maxTopVelocity = (maxVelocity * AvatarPhysics.SIN_OF_45, 0, maxVelocity * AvatarPhysics.SIN_OF_45)
        elif _leftBackward:
            self.leftwardMagnitude = AvatarPhysics.SIN_OF_45
            self.backwardMagnitude = AvatarPhysics.SIN_OF_45
            self.physics.maxTopVelocity = (-maxVelocity * AvatarPhysics.SIN_OF_45, 0, -maxVelocity * AvatarPhysics.SIN_OF_45)
        elif _rightBackward:
            self.rightwardMagnitude = AvatarPhysics.SIN_OF_45
            self.backwardMagnitude = AvatarPhysics.SIN_OF_45
            self.physics.maxTopVelocity = (maxVelocity * AvatarPhysics.SIN_OF_45, 0, maxVelocity * AvatarPhysics.SIN_OF_45)
        elif _w:
            self.forwardMagnitude = 1
            self.physics.maxTopVelocity = (0, 0, maxVelocity)
        elif _s:
            self.backwardMagnitude = 1
            self.physics.maxTopVelocity = (0, 0, -maxVelocity)
        elif _q:
            self.leftwardMagnitude = 1
            self.physics.maxTopVelocity = (-maxVelocity, 0, 0)
        elif _e:
            self.rightwardMagnitude = 1
            self.physics.maxTopVelocity = (maxVelocity, 0, 0)

    def playVerticalAction(self, up, down):
        if up:
            if self.player.qinggongState in gametypes.QINGGONG_WINGFLY_STATES:
                if self.leftwardMagnitude - self.rightwardMagnitude == 0 and self.backwardMagnitude - self.forwardMagnitude == 0:
                    wingFlyUpStartActName = self.player.fashion.getWingFlyUpStartAction()
                    if wingFlyUpStartActName and wingFlyUpStartActName in self.player.fashion.getActionNameList():
                        try:
                            wingFlyUpStartAct = self.player.model.action(wingFlyUpStartActName)
                            wingFlyUpActName = self.player.fashion.getWingFlyUpAction()
                            wingFlyUpStartAct(0, None, 1).action(wingFlyUpActName)()
                            self.player.model.action(wingFlyUpActName)()
                            self.player.qinggongMgr.playWingFlyModelAction([wingFlyUpActName])
                        except:
                            pass

            else:
                if self.player.fashion.doingActionType() in (action.GUIDE_ACTION,):
                    return
                wingFlyUpActionName = self.player.fashion.getWingFlyNormalUpAction()
                if self.player.isInCoupleRide():
                    actionIds = SYSCD.data.get('wingCoupleFlyUpAction', {}).get(self.player.getCoupleKey())
                    if actionIds:
                        wingFlyUpActionName = actionIds[0]
                        playSeq = [actionIds[1]]
                        self.player.fashion.playActionSequence(self.player.modelServer.coupleModel, playSeq, None)
                self.player.fashion.playSingleAction(wingFlyUpActionName, action.WING_FLY_UP_ACTION)
                self.player.qinggongMgr.playWingFlyModelAction([wingFlyUpActionName])
        if down:
            if self.player.qinggongState in gametypes.QINGGONG_WINGFLY_STATES:
                if self.leftwardMagnitude - self.rightwardMagnitude == 0 and self.backwardMagnitude - self.forwardMagnitude == 0:
                    try:
                        wingFlyDownActName = self.player.fashion.getWingFlyDownAction()
                        self.player.model.action(wingFlyDownActName)()
                        self.player.qinggongMgr.playWingFlyModelAction([wingFlyDownActName])
                    except:
                        pass

            else:
                if self.player.fashion.doingActionType() in (action.GUIDE_ACTION,):
                    return
                wingFlyDownActionName = self.player.fashion.getWingFlyNormalDownAction()
                if self.player.isInCoupleRide():
                    actionIds = SYSCD.data.get('wingCoupleFlyDownAction', {}).get(self.player.getCoupleKey())
                    if actionIds:
                        wingFlyDownActionName = actionIds[0]
                        playSeq = [actionIds[1]]
                        self.player.fashion.playActionSequence(self.player.modelServer.coupleModel, playSeq, None)
                self.player.fashion.playSingleAction(wingFlyDownActionName, action.WING_FLY_DOWN_ACTION)
                self.player.qinggongMgr.playWingFlyModelAction([wingFlyDownActionName])

    def checkLockMoveActionWing(self):
        if self.player.fashion.doingActionType() == action.WING_LAND_ACTION:
            return True
        if self.player.inWingTakeOff:
            return True
        return False

    def isInSpecialDecelarate(self):
        velocityAccelerate = self.physics.velocityAccelerate
        if self.physics.velocity[0] < 0 and velocityAccelerate[0] > 0:
            return True
        if self.physics.velocity[1] < 0 and velocityAccelerate[1] > 0:
            return True
        if self.physics.velocity[2] < 0 and velocityAccelerate[2] > 0:
            return True
        return False

    def _key_w_down(self, isDown):
        if not self.player.checkTempGroupFollow():
            return
        if self.player.inSlowTime and isDown:
            self.player.onSlowTimeActionProcessed(gameglobal.SLOW_TIME_ACTION_FORWARD)
            return
        if self.player.confusionalState in [gameglobal.CONFUSIONAL_FRONT_BACK, gameglobal.CONFUSIONAL_ALL] and not self.needKeyInvert:
            self.needKeyInvert = True
            self._key_s_down(isDown)
            self.needKeyInvert = False
            return
        if isDown and self.player.needForbidForwardOp():
            return
        self._w = isDown
        if self.checkLockMoveActionWing():
            return
        if (self.isInDecelerating() or self.isInSpecialDecelarate()) and isDown:
            self.endFlyAccelerate(isDown)
        if self._w:
            self._qKeyTime = 0.0
            self._eKeyTime = 0.0
            self._sKeyTime = 0.0
            self._xKeyTime = 0.0
            self._spaceKeyTime = 0.0
            self.realKeyUpTime = 0.0
            if self.player.qinggongState == gametypes.QINGGONG_STATE_FAST_DOWN:
                return
            if self._wKeyTime:
                if BigWorld.time() - self._wKeyTime <= gameglobal.DOUBLE_CLICK_INTERVAL:
                    self.realDashTime = BigWorld.time()
                    self._wKeyTime = 0.0
                    if self.player.canFly():
                        self.needForceEndQingGong = True
                        self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_WINGFLY_DASH)
                        self.moveControl('_w', isDown)
                        return
                    if self.player.qinggongMgr.state in (qingGong.STATE_DASH_TWICE_JUMPING,
                     qingGong.STATE_DASH_TWICE_JUMPING,
                     qingGong.STATE_JUMPING,
                     qingGong.STATE_DASH_JUMPING,
                     qingGong.STATE_DASH_BIG_JUMPING,
                     qingGong.STATE_RUSH_DOWN,
                     qingGong.STATE_RUSH_DOWN_WEAPON_IN_HAND,
                     qingGong.STATE_TWICE_JUMPING) or self.player.isFalling or self.player.fashion.doingActionType() in (action.FAST_DOWN_ACTION,):
                        if (self.player.isJumping or self.player.isFalling or self.player.canFly()) and self.player.qinggongMgr.getDistanceFromGround() >= 1.0:
                            if BigWorld.player().weaponInHandState():
                                self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_WEAPON_FORWARD_DOWN)
                            else:
                                wingEquip = BigWorld.player().equipment[gametypes.EQU_PART_WINGFLY]
                                if wingEquip:
                                    if wingEquip.isExpireTTL():
                                        self.player.chatToEventEx('翅膀已过期', const.CHANNEL_COLOR_RED)
                                        self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_DODGE_FORWARD_DOWN)
                                    else:
                                        self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_FORWARD_DOWN)
                                else:
                                    self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_DODGE_FORWARD_DOWN)
                    else:
                        now = time.time()
                        if self.player.lastEpRegenTime == 0.0:
                            epRegen = 0
                        else:
                            timeInterval = now - self.player.lastEpRegenTime
                            if self.player.inCombat:
                                delta = self.player.combatEpRegen
                            else:
                                delta = self.player.nonCombatEpRegenFix
                            if self.player.qinggongState in gametypes.QINGGONG_CNT_COST:
                                _, _, _, cntCost = qingGong.getQinggongData(self.player.qinggongState, self.player.inCombat)
                                delta -= cntCost / 2.0
                            epRegen = delta * timeInterval
                        preMin1, preMax1, fstCost1, _ = qingGong.getQinggongData(gametypes.QINGGONG_ROLL_FORWARD, self.player.inCombat)
                        qinggongState = self.player.inRiding() and gametypes.QINGGONG_STATE_MOUNT_DASH or gametypes.QINGGONG_STATE_FAST_RUN
                        preMin2, preMax2, fstCost2, _ = qingGong.getQinggongData(qinggongState, self.player.inCombat)
                        if (self.player.ep + epRegen < preMax1 or preMax1 == 0) and self.player.ep + epRegen >= preMin1 and self.player.inCombat:
                            self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_FORWARD_DOWN)
                            self.moveControl('_w', isDown)
                            return
                        if self.player.ep + epRegen >= preMin2:
                            if not self.player.isDashing:
                                if BigWorld.player().equipment[gametypes.EQU_PART_WINGFLY] and self.player.qinggongState == gametypes.QINGGONG_STATE_AUTO_JUMP:
                                    self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_FORWARD_DOWN)
                                else:
                                    qingGong.switchToDash(self.player, True)
                        elif not formula.inDotaBattleField(getattr(self.player, 'mapID', 0)):
                            self.player.showGameMsg(GMDD.data.QINGGONG_NOT_ENOUGH, ())
                else:
                    self._wKeyTime = BigWorld.time()
            else:
                self._wKeyTime = BigWorld.time()
        else:
            self.realKeyUpTime = BigWorld.time()
            self.player.enterWaterHeight = self.player.getEnterWaterHeight()
            gamelog.debug('qinggong:dash:松开w', self.player.qinggongState, self.player.isDashing, self.needForceEndQingGong)
            if self.player.qinggongState == gametypes.QINGGONG_STATE_FAST_SLIDING:
                self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_FORWARD_UP)
                self._wKeyTime = 0.0
            elif self.player.qinggongState in gametypes.QINGGONG_WINGFLY_STATES or self.player.qinggongState == 0 and self.needForceEndQingGong:
                self._wKeyTime = 0.0
                if not self.isAnyDirKeyDown():
                    cellCmd.endUpQinggongState()
            elif self.player.qinggongState in gametypes.QINGGONG_STATE_DASH_SET or self.player.isDashing:
                if self.player.qinggongState in gametypes.QINGGONG_STATE_DASH_SET:
                    cellCmd.endUpQinggongState()
                self.switchToRun()
                self.player.physics.velocity = (0, 0, 0)
                if self.player.inRiding() and not self.player.isJumping and not self.isMovingActionKeyControl():
                    actId = self.player.fashion.getHorseSprintStopAction()
                    self.player.fashion.playSingleAction(actId, action.HORSE_DASH_STOP_ACTION, 0, self.dashStopActionCallback, 1)
                    self.player.fashion.setIdleType(gametypes.IDLE_TYPE_SPRINT_STOP)
                    if self.player.inRidingHorse() and getattr(self.player.model, 'ride', None) and actId in self.player.model.ride.actionNameList():
                        self.player.model.ride.action(actId)()
                        self.player.playRideTogetherAction(actId)
        self.moveControl('_w', isDown)

    def dashStopActionCallback(self):
        self.player.fashion.setIdleType(gametypes.IDLE_TYPE_SPRINT_STOP)

    def isAnyDirKeyDown(self):
        _w = HK.HKM[HK.KEY_FORWARD].isAnyDown()
        _q = HK.HKM[HK.KEY_MOVELEFT].isAnyDown()
        _e = HK.HKM[HK.KEY_MOVERIGHT].isAnyDown()
        _s = HK.HKM[HK.KEY_BACKWARD].isAnyDown()
        _space = HK.HKM[keys.KEY_SPACE].isAnyDown()
        _x = HK.HKM[HK.KEY_DOWN].isAnyDown()
        return _w or _q or _e or _s or _space or _x

    def _key_s_down(self, isDown):
        if self.player.inPUBGPlane():
            return
        if self.player.inPUBGParachute():
            return
        if not self.player.checkTempGroupFollow():
            return
        if self.player.inSlowTime and isDown:
            self.player.onSlowTimeActionProcessed(gameglobal.SLOW_TIME_ACTION_BACKWARD)
            return
        if self.player.confusionalState in [gameglobal.CONFUSIONAL_FRONT_BACK, gameglobal.CONFUSIONAL_ALL] and not self.needKeyInvert:
            self.needKeyInvert = True
            self._key_w_down(isDown)
            self.needKeyInvert = False
            return
        if isDown and self.player.needForbidBackOp():
            return
        if self.checkLockMoveActionWing():
            return
        self._s = isDown
        if (self.isInDecelerating() or self.isInSpecialDecelarate()) and isDown:
            self.endFlyAccelerate(isDown)
        if self._s:
            self._qKeyTime = 0.0
            self._eKeyTime = 0.0
            self._wKeyTime = 0.0
            self._xKeyTime = 0.0
            self._spaceKeyTime = 0.0
            if self.player.qinggongState in gametypes.QINGGONG_STATE_DASH_SET:
                cellCmd.endUpQinggongState()
            if self.player.qinggongState in [gametypes.QINGGONG_STATE_SLIDING,
             gametypes.QINGGONG_STATE_FAST_SLIDING,
             gametypes.QINGGONG_STATE_FAST_SLIDING_WEAPON_IN_HAND,
             gametypes.QINGGONG_STATE_FAST_BIG_JUMP,
             gametypes.QINGGONG_STATE_RUSH_DOWN]:
                self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_S_DOWN)
                return
            if self._sKeyTime:
                if BigWorld.time() - self._sKeyTime <= gameglobal.DOUBLE_CLICK_INTERVAL:
                    if self.player.canFly():
                        self.needForceEndQingGong = True
                        self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_WINGFLY_BACK)
                    else:
                        self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_BACK_DOWN)
                        self._sKeyTime = 0.0
                    return
                self._sKeyTime = BigWorld.time()
            else:
                self._sKeyTime = BigWorld.time()
        if self.player.canFly():
            if self.player.qinggongState in gametypes.QINGGONG_WINGFLY_STATES or self.player.qinggongState == 0 and self.needForceEndQingGong:
                if not self.isAnyDirKeyDown():
                    cellCmd.endUpQinggongState()
                    self.endFlyAccelerate(isDown)
        self.moveControl('_s', isDown)

    def _key_d_down(self, isDown):
        if not self.player.checkTempGroupFollow():
            return
        self._d = isDown
        if self.checkLockMoveActionWing():
            return
        if self._d:
            self._wKeyTime = 0.0
            self._qKeyTime = 0.0
            self._sKeyTime = 0.0
            self._eKeyTime = 0.0
            self._xKeyTime = 0.0
            self._spaceKeyTime = 0.0
        self.moveControl('_d', isDown)

    def _key_a_down(self, isDown):
        if not self.player.checkTempGroupFollow():
            return
        self._a = isDown
        if self.checkLockMoveActionWing():
            return
        if self._a:
            self._wKeyTime = 0.0
            self._qKeyTime = 0.0
            self._sKeyTime = 0.0
            self._eKeyTime = 0.0
            self._xKeyTime = 0.0
            self._spaceKeyTime = 0.0
        self.moveControl('_a', isDown)

    def _key_q_down(self, isDown):
        if self.player.inPUBGPlane():
            return
        if not self.player.checkTempGroupFollow():
            return
        if self.player.inSlowTime and isDown:
            self.player.onSlowTimeActionProcessed(gameglobal.SLOW_TIME_ACTION_LEFTWARD)
            return
        if self.player.inSimpleQte and isDown:
            gameglobal.rds.ui.simpleQTE.handleInputKey(gameglobal.QTE_KEY_A)
            return
        if self.player.confusionalState in [gameglobal.CONFUSIONAL_LEFT_RIGHT, gameglobal.CONFUSIONAL_ALL] and not self.needKeyInvert:
            self.needKeyInvert = True
            self._key_e_down(isDown)
            self.needKeyInvert = False
            return
        if self.player.handClimb:
            return
        self._q = isDown
        if self.checkLockMoveActionWing():
            return
        if self.player.qinggongMgr.state in (qingGong.STATE_DASH_TWICE_JUMPING,
         qingGong.STATE_SLIDE_DASH,
         qingGong.STATE_SLIDE_SLOW_FALLING,
         qingGong.STATE_SLIDE_FAST_FALLING,
         qingGong.STATE_COLLIDE_FALLING,
         qingGong.STATE_DASH_AUTO_JUMP) and isDown:
            return
        if (self.isInAccelerating() or self.isInSpecialDecelarate()) and isDown:
            self.endFlyAccelerate(isDown)
        if self._q:
            self._wKeyTime = 0.0
            self._eKeyTime = 0.0
            self._sKeyTime = 0.0
            self._xKeyTime = 0.0
            self._spaceKeyTime = 0.0
            if self._qKeyTime:
                if BigWorld.time() - self._qKeyTime <= gameglobal.DOUBLE_CLICK_INTERVAL:
                    self._qKeyTime = 0.0
                    if self.player.canFly():
                        self.needForceEndQingGong = True
                        self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_WINGFLY_LEFT)
                    else:
                        self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_LEFT_DOWN)
                    return
                self._qKeyTime = BigWorld.time()
            else:
                self._qKeyTime = BigWorld.time()
        elif self.player.canFly():
            if self.player.qinggongState in gametypes.QINGGONG_WINGFLY_STATES or self.player.qinggongState == 0 and self.needForceEndQingGong:
                if not self.isAnyDirKeyDown():
                    cellCmd.endUpQinggongState()
        self.moveControl('_q', isDown)

    def _key_e_down(self, isDown):
        if self.player.inPUBGPlane():
            return
        if not self.player.checkTempGroupFollow():
            return
        if self.player.inSlowTime and isDown:
            self.player.onSlowTimeActionProcessed(gameglobal.SLOW_TIME_ACTION_RIGHTWARD)
            return
        if self.player.inSimpleQte and isDown:
            gameglobal.rds.ui.simpleQTE.handleInputKey(gameglobal.QTE_KEY_D)
            return
        if self.player.confusionalState in [gameglobal.CONFUSIONAL_LEFT_RIGHT, gameglobal.CONFUSIONAL_ALL] and not self.needKeyInvert:
            self.needKeyInvert = True
            self._key_q_down(isDown)
            self.needKeyInvert = False
            return
        if self.player.handClimb:
            return
        self._e = isDown
        if self.checkLockMoveActionWing():
            return
        if self.player.qinggongMgr.state in (qingGong.STATE_DASH_TWICE_JUMPING,
         qingGong.STATE_SLIDE_DASH,
         qingGong.STATE_SLIDE_SLOW_FALLING,
         qingGong.STATE_SLIDE_FAST_FALLING,
         qingGong.STATE_COLLIDE_FALLING,
         qingGong.STATE_DASH_AUTO_JUMP) and isDown:
            return
        if (self.isInDecelerating() or self.isInSpecialDecelarate()) and isDown:
            self.endFlyAccelerate(isDown)
        if self._e:
            self._qKeyTime = 0.0
            self._wKeyTime = 0.0
            self._sKeyTime = 0.0
            self._spaceKeyTime = 0.0
            self._xKeyTime = 0.0
            if self._eKeyTime:
                if BigWorld.time() - self._eKeyTime <= gameglobal.DOUBLE_CLICK_INTERVAL:
                    self._eKeyTime = 0.0
                    if self.player.canFly():
                        self.needForceEndQingGong = True
                        self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_WINGFLY_RIGHT)
                    else:
                        self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_RIGHT_DOWN)
                    return
                self._eKeyTime = BigWorld.time()
            else:
                self._eKeyTime = BigWorld.time()
        elif self.player.canFly():
            if self.player.qinggongState in gametypes.QINGGONG_WINGFLY_STATES or self.player.qinggongState == 0 and self.needForceEndQingGong:
                if not self.isAnyDirKeyDown():
                    cellCmd.endUpQinggongState()
        self.moveControl('_e', isDown)

    def _key_x_down(self, isDown):
        if self.player.inPUBGPlane():
            return
        if not self.player.checkTempGroupFollow():
            return
        self._x = isDown
        if self.checkLockMoveActionWing():
            return
        if (self.isInDecelerating() or self.isInSpecialDecelarate()) and isDown:
            self.endFlyAccelerate(isDown)
        if self.player.canFly():
            if isDown:
                self._qKeyTime = 0.0
                self._wKeyTime = 0.0
                self._sKeyTime = 0.0
                self._eKeyTime = 0.0
                self._spaceKeyTime = 0.0
                if self._xKeyTime:
                    if BigWorld.time() - self._xKeyTime <= gameglobal.DOUBLE_CLICK_INTERVAL:
                        self._xKeyTime = 0.0
                        self.needForceEndQingGong = True
                        self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_WINGFLY_DOWN)
                        return
                    self._xKeyTime = BigWorld.time()
                else:
                    self._xKeyTime = BigWorld.time()
            elif self.player.canFly():
                if self.player.qinggongState in gametypes.QINGGONG_WINGFLY_STATES or self.player.qinggongState == 0 and self.needForceEndQingGong:
                    if not self.isAnyDirKeyDown():
                        cellCmd.endUpQinggongState()
            self.flyDown(isDown)
            self.moveControl('_x', isDown)
            self.player.refreshHorseWingEffect()

    def _key_space_down(self, isDown):
        if self.player.inPUBGPlane():
            return
        if self.player.inPUBGParachute():
            return
        if not self.player.checkTempGroupFollow():
            return
        self._space = isDown
        if self.checkLockMoveActionWing():
            return
        if (self.isInDecelerating() or self.isInSpecialDecelarate()) and isDown:
            self.endFlyAccelerate(isDown)
        if self.player.canFly():
            if isDown:
                self._qKeyTime = 0.0
                self._wKeyTime = 0.0
                self._sKeyTime = 0.0
                self._eKeyTime = 0.0
                self._xKeyTime = 0.0
                if self._spaceKeyTime:
                    if BigWorld.time() - self._spaceKeyTime <= gameglobal.DOUBLE_CLICK_INTERVAL:
                        self._spaceKeyTime = 0.0
                        self.needForceEndQingGong = True
                        self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_WINGFLY_UP)
                        return
                    self._spaceKeyTime = BigWorld.time()
                else:
                    self._spaceKeyTime = BigWorld.time()
            elif self.player.canFly():
                if self.player.qinggongState in gametypes.QINGGONG_WINGFLY_STATES or self.player.qinggongState == 0 and self.needForceEndQingGong:
                    if not self.isAnyDirKeyDown():
                        cellCmd.endUpQinggongState()
            self.flyUp(isDown, True)
            self.moveControl('_space', isDown)
        elif BigWorld.player().qinggongMgr.dismissManDown():
            self.realJumpUp(isDown)
        p = BigWorld.player()
        if hasattr(p, 'getOperationMode') and p.getOperationMode() == gameglobal.ACTION_MODE and not gameglobal.rds.ui.bInEdit:
            if not p.circleEffect.isShowingEffect and not p.chooseEffect.isShowingEffect:
                p.ap.showCursor = False
                p.ap.reset()
                p.ap.hideWidget()

    def isInAccelerating(self):
        return getattr(self.physics, 'isAccelerating', getattr(self.physics, 'acceleratingState', 0)) == 1

    def isInDecelerating(self):
        return getattr(self.physics, 'isAccelerating', getattr(self.physics, 'acceleratingState', 0)) == -1

    def getQingGongTopSpeed(self):
        p = BigWorld.player()
        qinggongSpeed = 0
        if p.qinggongState != gametypes.QINGGONG_STATE_DEFAULT:
            qinggongSpeed = gametypes.QINGGONG_STATE_INFO[p.qinggongState]
            if p.qinggongState == gametypes.QINGGONG_STATE_FAST_RUN:
                qinggongSpeed = self.getDashForwardSpeed()
            elif p.qinggongState == gametypes.QINGGONG_STATE_FAST_JUMP:
                qinggongSpeed = utils.getDashUpForwardSpeed(self.player)
            elif p.qinggongState == gametypes.QINGGONG_STATE_FAST_BIG_JUMP:
                qinggongSpeed = utils.getDashUpForwardSpeed1(self.player)
            elif p.qinggongState == gametypes.QINGGONG_STATE_SLIDING:
                qinggongSpeed = self.getDashFlySpeed()
            elif p.qinggongState in [gametypes.QINGGONG_STATE_FAST_SLIDING,
             gametypes.QINGGONG_STATE_FAST_SLIDING_WEAPON_IN_HAND,
             gametypes.QINGGONG_STATE_WINGFLY_DASH,
             gametypes.QINGGONG_STATE_RUSH_DOWN,
             gametypes.QINGGONG_STATE_RUSH_DOWN_WEAPON_IN_HAND]:
                if self.player.qinggongMgr.rushTop:
                    if self.player.qinggongState == gametypes.QINGGONG_STATE_FAST_SLIDING:
                        qinggongSpeed = utils.getDashRushTopSpeed(self.player)
                    else:
                        qinggongSpeed = utils.getDashRushTopWeaponInHandSpeed(self.player)
                elif self.player.qinggongState in [gametypes.QINGGONG_STATE_FAST_SLIDING, gametypes.QINGGONG_STATE_FAST_SLIDING_WEAPON_IN_HAND]:
                    qinggongSpeed = 0
                else:
                    qinggongSpeed = self.getDashFlySpeed()
            elif p.qinggongState == gametypes.QINGGONG_STATE_MOUNT_DASH:
                qinggongSpeed = utils.getHorseDashUpForwardSpeed(self.player)
            elif p.qinggongState == gametypes.QINGGONG_STATE_AUTO_JUMP:
                qinggongSpeed = utils.getAutoJumpForwardSpeedBase(self.player)
            elif p.qinggongState == gametypes.QINGGONG_STATE_DASH_AUTO_JUMP:
                qinggongSpeed = utils.getDashAutoJumpForwardSpeedBase(self.player)
        if p.inFly:
            qinggongSpeed = self.getFlyTopSpeed()
        return qinggongSpeed

    def getFlyTopSpeed(self):
        p = BigWorld.player()
        if p.qinggongState in gametypes.QINGGONG_STATE_WINGFLY_SET:
            qinggongSpeed = utils.getFlyRushMaxSpeed(self.player)
        else:
            qinggongSpeed = utils.getFlyMaxSpeed(self.player)
        wingFlyMaxSpeed = qinggongSpeed
        if p.qinggongState != gametypes.QINGGONG_STATE_DEFAULT:
            wingFlyMaxSpeed = utils.getFlyRushMaxSpeed(self.player)
        elif self.player.fashion.doingActionType() == action.WING_TAKE_OFF_ACTION:
            wingFlyMaxSpeed = PCD.data.get('wingTakeOffSpeed', gametypes.WING_TAKE_OFF_SPEED)
        else:
            flyMaxSpeed = utils.getFlyMaxSpeed(self.player)
            flyHorizonSpeed = utils.getFlyHorizonSpeed(self.player)
            wingFlyMaxSpeed = max(flyHorizonSpeed, flyMaxSpeed)
            if self.player.gmMode:
                flyHorizonSpeed = PCD.data.get('flyHorizonSpeed', gametypes.WING_TAKE_OFF_SPEED)
                wingFlyMaxSpeed = max(flyHorizonSpeed, flyMaxSpeed, flyHorizonSpeed)
        return max(qinggongSpeed, wingFlyMaxSpeed)

    def resetAvatarTopSpeed(self):
        if gameglobal.rds.isSinglePlayer:
            return
        p = BigWorld.player()
        moveSpeed = max(p.speed[gametypes.SPEED_MOVE] / 60.0, p.ap.runFwdSpeed)
        qinggongSpeed = self.getQingGongTopSpeed()
        speedLimit = max(moveSpeed, qinggongSpeed)
        if not self.player.gmMode:
            equipRide = self.player.equipment.get(gametypes.EQU_PART_RIDE)
            equipWingFly = self.player.equipment.get(gametypes.EQU_PART_WINGFLY)
            if self.player.inFly == gametypes.IN_FLY_TYPE_WING and equipWingFly:
                speedLimit *= equipWingFly.getVelocityDuraFactor() * equipWingFly.getVelocityFactorByVip(p)
            elif self.player.inFly == gametypes.IN_FLY_TYPE_FLY_RIDE and equipRide:
                speedLimit *= equipRide.getVelocityDuraFactor() * equipRide.getVelocityFactorByVip(p)
            elif self.player.bianshen[0] == gametypes.BIANSHEN_RIDING_RB and equipRide:
                speedLimit *= equipRide.getVelocityDuraFactor() * equipRide.getVelocityFactorByVip(p)
        elif self.player.inFlyTypeObserver():
            speedLimit = utils.getFightObserverFlySpeed(self.player)
        if (self.isTracing or self.isChasing) and self.chasingEntity and getattr(self.chasingEntity, 'filter', None):
            entVel = getattr(self.chasingEntity.filter, 'velocity', None)
            if entVel:
                entSpeed = entVel.length
                if entSpeed > 0 and entSpeed < speedLimit:
                    speedLimit = entSpeed
        if self.player.speedField:
            speedLimit = speedLimit + SFD.data.get(self.player.speedField[1], {}).get('speed', 0)
        if self.displacementSpeed:
            speedLimit = self.displacementSpeed
        p.physics.maxVelocity = speedLimit

    def getRunForwardSpeedBase(self, speedData):
        if not getattr(self, 'player', None):
            return 0
        return utils.getMoveSpeedBase(self.player) * speedData.get('runFactor', 1.0)

    def getSwimRunSpeedBase(self, speedData):
        if not getattr(self, 'player', None):
            return 0
        return utils.getMoveSpeedBase(self.player) * speedData.get('swimRunFactor', 1.0)

    def getSwimRunBackSpeedBase(self, speedData):
        if not getattr(self, 'player', None):
            return 0
        return utils.getMoveSpeedBase(self.player) * speedData.get('swimRunBackFactor', 1.0)

    def getSwimWalkSpeedBase(self, speedData):
        if not getattr(self, 'player', None):
            return 0
        return utils.getMoveSpeedBase(self.player) * speedData.get('swimWalkFactor', 1.0)

    def getSwimWalkBackSpeedBase(self, speedData):
        if not getattr(self, 'player', None):
            return 0
        return utils.getMoveSpeedBase(self.player) * speedData.get('swimWalkBackFactor', 1.0)

    def getSwimDashSpeedBase(self, speedData):
        if not getattr(self, 'player', None):
            return 0
        return utils.getRideSwimDashSpeed(self.player)

    def getRunBackwardSpeedBase(self, speedData):
        if not getattr(self, 'player', None):
            return 0
        return utils.getMoveSpeedBase(self.player) * speedData.get('runBackFactor', 1.0) * 0.6

    def getDashForwardSpeed(self):
        p = self.player
        if p.isDashing:
            if p.jumpState == gametypes.DASH_JUMP:
                isInHorse = p.inRiding() and p.bianshen[0] == gametypes.BIANSHEN_RIDING_RB
                if isInHorse:
                    return utils.getHorseDashUpForwardSpeed(self.player)
                else:
                    return utils.getDashUpForwardSpeed(self.player)
            elif p.jumpState == gametypes.DASH_BIG_JUMP:
                return utils.getDashUpForwardSpeed1(self.player)
            else:
                return utils.getDashNormalSpeed(self.player)

        return PCD.data.get('dashForwardSpeed', gametypes.DASHFORWARD_SPEED) * utils.getDashFactor(self.player)

    def getDashBackwardSpeed(self, speedData):
        return PCD.data.get('dashBackSpeed', gametypes.DASHBACKWARD_SPEED) * speedData.get('dashBackFactor', 1.0)

    def getDashFlySpeed(self):
        p = self.player
        if p.qinggongMgr.currJumpNum == qingGong.DASH_TWICE_JUMP or p.jumpState == gametypes.DASH_TWICE_JUMP:
            return utils.getDashFlySpeedLvUp(self.player)
        if p.qinggongMgr.state == qingGong.STATE_RUSH_DOWN:
            return utils.getRushDownFwdSpeed(self.player)
        if p.qinggongMgr.state == qingGong.STATE_RUSH_DOWN_WEAPON_IN_HAND:
            return utils.getRushDownWeaponInHandFwdSpeed(self.player)
        return 0

    def updateVelocity(self):
        if self.player.life == gametypes.LIFE_DEAD:
            self.stopMove()
            return
        if self.player.isAscending:
            self.player.chatToEventEx('正处于位移上升阶段', const.CHANNEL_COLOR_RED)
            return
        if self.player.inDanDao:
            self.player.chatToEventEx('正处于被击飞状态', const.CHANNEL_COLOR_RED)
            return
        if self.player.isForceMove == gameglobal.FORCE_MOVE_CONST_SPEED:
            return
        if self.player.isForceMove == gameglobal.FORCE_MOVE_VARID_SPEED:
            self.player.ap.forwardMagnitude = 1
            self.player.ap.backwardMagnitude = 0
            self.player.ap.leftwardMagnitude = 0
            self.player.ap.rightwardMagnitude = 0
        self._calcSpeedMultiplier()
        if self.player.isPathfinding and not self.upwardMagnitude:
            self.forwardMagnitude = 1
        elif self.isAutoMoving and not self.forwardMagnitude:
            self.forwardMagnitude = 1
        if self.forwardMagnitude > 0 and self.backwardMagnitude > 0:
            forwardSpeed = 0
        else:
            forwardSpeed = self.forwardMagnitude - self.backwardMagnitude
        xSpeed = (self.rightwardMagnitude - self.leftwardMagnitude) * self.speedMultiplier
        ySpeed = self.upwardMagnitude * self.upSpeedMultiplier
        if self.player.canFly():
            if self.player.fashion.doingActionType() == action.WING_TAKE_OFF_ACTION:
                ySpeed = self.upwardMagnitude * PCD.data.get('wingTakeOffSpeed', gametypes.WING_TAKE_OFF_SPEED)
            else:
                ySpeed = self.upwardMagnitude * utils.getFlyVerticalSpeed(self.player)
        zSpeed = forwardSpeed * self.speedMultiplier
        xSpeed, ySpeed, zSpeed, velocity = self.setQingGongVelocity(xSpeed, ySpeed, zSpeed, forwardSpeed)
        if self.player.canSwim():
            if not self.isOnSwimRide():
                ssf = AvatarPhysics.SWIM_SPEED_FACTOR * (1 + self.player.swimSpeedFactor * 1.0 / 100)
                velocity.x *= ssf
                velocity.y *= ssf
                velocity.z *= ssf
        elif self.player.handClimb:
            velocity.x = velocity.z = 0
            velocity.y = zSpeed
        if self.player.qinggongState in gametypes.QINGGONG_WINGFLY_STATES:
            maxVelocity = utils.getFlyRushMaxSpeed(self.player)
            xSpeed = (self.rightwardMagnitude - self.leftwardMagnitude) * maxVelocity
            zSpeed = forwardSpeed * maxVelocity
            ySpeed = self.upwardMagnitude * maxVelocity
            if not (xSpeed == 0 and ySpeed == 0 and zSpeed == 0):
                velocity = Math.Vector3(xSpeed, ySpeed, zSpeed)
            if self.isInAccelerating() or self.isInDecelerating():
                velocityAccelerate = self.physics.velocityAccelerate
                if velocityAccelerate[0] != 0:
                    velocity[0] = xSpeed
                if velocityAccelerate[1] != 0:
                    velocity[1] = ySpeed
                if velocityAccelerate[2] != 0:
                    velocity[2] = zSpeed
        if self.player.inFlyTypeObserver():
            maxVelocity = utils.getFightObserverFlySpeed(self.player)
            xSpeed = (self.rightwardMagnitude - self.leftwardMagnitude) * maxVelocity
            zSpeed = forwardSpeed * maxVelocity
            ySpeed = self.upwardMagnitude * maxVelocity
            if not (xSpeed == 0 and ySpeed == 0 and zSpeed == 0):
                velocity = Math.Vector3(xSpeed, ySpeed, zSpeed)
        velocity = self.updateSpeedFieldVelocity(velocity)
        if self.player.inPUBGParachute():
            pubgParachuteDownSpeed = DCD.data.get('pubgParachuteDownSpeed', 10)
            velocity[1] = -pubgParachuteDownSpeed
            if self.player.pitch > 0:
                velocity[1] -= math.sin(self.player.pitch) * velocity[2]
        if self.player.inFly and velocity[0] == 0 and velocity[1] == 0 and velocity[2] == 0 and getattr(self.physics, 'isAccelerating', getattr(self.physics, 'acceleratingState', 0)) != 0:
            return
        self.physics.velocity = velocity
        self.stopRunToIdle(velocity)
        BigWorld.callback(0, Functor(self.playTurnAction, velocity, self.stopDirection))
        self.adjustModelDir(self.lastVelocity, velocity)
        self.physics.maxTopVelocity = velocity
        self.resetAvatarTopSpeed()
        return velocity

    def updateSpeedFieldVelocity(self, velocity):
        speedField = self.player.speedField
        if speedField:
            sourceEnt = BigWorld.entities.get(speedField[0])
            if sourceEnt and sourceEnt.inWorld:
                velocity = self.getVelocityForSpeedField(sourceEnt, velocity, speedField[1])
        return velocity

    def getVelocityForSpeedField(self, sourceEnt, velocity, speedFieldId):
        speedFieldData = SFD.data.get(speedFieldId, {})
        dirType = speedFieldData.get('dirType', gametypes.SPEED_FIELD_DIR_TYPE_SOURCE)
        shiftType = speedFieldData.get('shiftType', gametypes.SPEED_FIELD_SHIFT_TYPE_PUSH)
        speed = speedFieldData.get('speed', 0)
        if dirType == gametypes.SPEED_FIELD_DIR_TYPE_SOURCE:
            if shiftType == gametypes.SPEED_FIELD_SHIFT_TYPE_PUSH:
                yaw = utils.adjustDir(sourceEnt.yaw - self.player.yaw)
                velocity = Math.Vector3(velocity[0] + speed * math.sin(yaw), velocity[1], velocity[2] + speed * math.cos(yaw))
            else:
                yaw = utils.adjustDir(sourceEnt.yaw - self.player.yaw + math.pi)
                velocity = Math.Vector3(velocity[0] + speed * math.sin(yaw), velocity[1], velocity[2] + speed * math.cos(yaw))
        else:
            direction = sourceEnt.position - self.player.position
            if not direction.length or not speed:
                return Math.Vector3(0, 0, 0)
            ySpeed = (sourceEnt.position.y - self.player.position.y) / direction.length * speed
            if shiftType == gametypes.SPEED_FIELD_SHIFT_TYPE_PUSH:
                yaw = utils.adjustDir(direction.yaw - self.player.yaw + math.pi)
                velocity = Math.Vector3(velocity[0] + speed * math.sin(yaw), velocity[1] + ySpeed, velocity[2] + speed * math.cos(yaw))
            else:
                yaw = utils.adjustDir(direction.yaw - self.player.yaw)
                velocity = Math.Vector3(velocity[0] + speed * math.sin(yaw), velocity[1] + ySpeed, velocity[2] + speed * math.cos(yaw))
        return velocity

    def stopRunToIdle(self, velocity):
        if velocity[2] < 0:
            self.player.backMove = True
        elif abs(velocity[0]) <= 0 and abs(velocity[1]) <= 0 and abs(velocity[2]) <= 0:
            pass
        else:
            self.player.backMove = False
        if abs(velocity[0]) > 0 or abs(velocity[1]) > 0 or abs(velocity[2]) > 0.1:
            for actName in self.player.model.queue:
                runToIdleAction = self.player.fashion.getRunToIdleAction()
                if runToIdleAction == actName:
                    self.player.fashion.stopActionByName(self.player.model, actName)

    def adjustModelDir(self, lastVelocity, velocity):
        if not self.player.inMotorRunStop() or self.player.inMoving():
            return
        if lastVelocity and lastVelocity[0] < 0:
            self.player.model.yaw = self.player.yaw - math.pi / 2
            self.stopDirection = STOP_DIRECTION_LEFT
            self.player.modelServer.poseManager.enableRideIdlePose(True)
        elif lastVelocity and lastVelocity[0] > 0:
            self.player.model.yaw = self.player.yaw + math.pi / 2
            self.stopDirection = STOP_DIRECTION_RIGHT
            self.player.modelServer.poseManager.enableRideIdlePose(True)
        else:
            self.stopDirection = STOP_DIRECTION_STRAIGHT
            self.player.modelServer.poseManager.enableRideIdlePose(False)

    def delayLastVelocity(self):
        velocity = self.physics.velocity
        if abs(velocity[0]) < 0.1 and abs(velocity[1]) < 0.1 and abs(velocity[2]) < 0.1:
            self.lastVelocity = velocity

    def playTurnAction(self, velocity, stopDirection):
        if not self.player:
            return
        if self.player.bianshen[0] != gametypes.BIANSHEN_RIDING_RB:
            return
        if not self.lastVelocity:
            self.lastVelocity = velocity
            if velocity[2] > 1:
                if stopDirection == STOP_DIRECTION_LEFT:
                    self.player.playLeftToStraight()
                elif stopDirection == STOP_DIRECTION_RIGHT:
                    self.player.playRightToStraight()
            elif velocity[0] > 1:
                if stopDirection == STOP_DIRECTION_LEFT:
                    self.player.playLeftToRight()
                else:
                    self.player.playStraightToRight()
            elif velocity[0] < -1:
                if stopDirection == STOP_DIRECTION_RIGHT:
                    self.player.playRightToLeft()
                else:
                    self.player.playStraightToLeft()
            return
        if abs(velocity[0]) < 0.1 and abs(velocity[1]) < 0.1 and abs(velocity[2]) < 0.1:
            BigWorld.callback(0.2, self.delayLastVelocity)
            return
        if self.lastVelocity[2] > 0:
            if velocity[2] <= 0.1:
                if velocity[0] < 0:
                    self.player.playStraightToLeft()
                elif velocity[0] > 0:
                    self.player.playStraightToRight()
            if abs(self.lastVelocity[0]) < 0.1:
                if velocity[0] < -1 and velocity[2] > 1:
                    self.player.playStraightToLeft()
                elif velocity[0] > 1 and velocity[2] > 1:
                    self.player.playStraightToRight()
            if abs(self.lastVelocity[0]) > 0.1:
                if self.lastVelocity[0] < -1 and velocity[2] > 1 and abs(velocity[0]) < 0.1:
                    self.player.playLeftToStraight()
                if self.lastVelocity[0] > 1 and velocity[2] > 1 and abs(velocity[0]) < 0.1:
                    self.player.playRightToStraight()
        elif abs(self.lastVelocity[2]) < 0.1:
            if abs(velocity[2]) <= 0.1:
                if self.lastVelocity[0] < 0 and velocity[0] > 0:
                    self.player.playLeftToRight()
                elif self.lastVelocity[0] > 0 and velocity[0] < 0:
                    self.player.playRightToLeft()
            elif velocity[2] > 1:
                if self.lastVelocity[0] < 0:
                    self.player.playLeftToStraight()
                elif self.lastVelocity[0] > 0:
                    self.player.playRightToStraight()
                elif self.stopDirection == STOP_DIRECTION_LEFT:
                    self.player.playLeftToStraight()
                elif self.stopDirection == STOP_DIRECTION_RIGHT:
                    self.player.playRightToStraight()
        self.lastVelocity = velocity

    def setQingGongVelocity(self, xSpeed, ySpeed, zSpeed, forwardSpeed):
        if self.player.qinggongState in [gametypes.QINGGONG_STATE_FAST_SLIDING,
         gametypes.QINGGONG_STATE_FAST_SLIDING_WEAPON_IN_HAND,
         gametypes.QINGGONG_STATE_WINGFLY_DASH,
         gametypes.QINGGONG_STATE_RUSH_DOWN,
         gametypes.QINGGONG_STATE_RUSH_DOWN_WEAPON_IN_HAND]:
            if self.player.qinggongMgr.rushTop:
                if self.player.qinggongState == gametypes.QINGGONG_STATE_FAST_SLIDING:
                    speed = utils.getDashRushTopSpeed(self.player)
                else:
                    speed = utils.getDashRushTopWeaponInHandSpeed(self.player)
            elif self.player.qinggongState in [gametypes.QINGGONG_STATE_FAST_SLIDING, gametypes.QINGGONG_STATE_FAST_SLIDING_WEAPON_IN_HAND]:
                speed = 0
            else:
                speed = self.getDashFlySpeed()
            speed = speed * self.player.getQingGongData(self.player.qinggongState).get('speedFactor', 1)
            zSpeed = speed
            velocity = Math.Vector3(xSpeed, ySpeed, zSpeed)
        elif self.player.qinggongState == gametypes.QINGGONG_STATE_SLIDING:
            if forwardSpeed:
                xSpeed = (self.rightwardMagnitude - self.leftwardMagnitude) * utils.getDashFlySpeedBase(self.player)
                zSpeed = forwardSpeed * utils.getDashFlySpeedBase(self.player)
            else:
                zSpeed = self.getDashFlySpeed()
            velocity = Math.Vector3(xSpeed, ySpeed, zSpeed)
        else:
            velocity = Math.Vector3(xSpeed, ySpeed, zSpeed)
        return (xSpeed,
         ySpeed,
         zSpeed,
         velocity)

    def _calcSpeedMultiplier(self):
        if self.player.jumpState == gametypes.AUTO_JUMP:
            self.speedMultiplier = utils.getAutoJumpForwardSpeedBase(self.player)
            self.setUpSpeedMultiplier()
        elif self.player.jumpState == gametypes.DASH_AUTO_JUMP:
            self.speedMultiplier = utils.getDashAutoJumpForwardSpeedBase(self.player)
            self.setUpSpeedMultiplier()
        elif self.player.isDashing:
            if self.isOnSwimRide():
                if self.forwardMagnitude > 0:
                    self.speedMultiplier = self.swimDashSpeed
            elif self.backwardMagnitude > 0:
                self.speedMultiplier = self.dashBackSpeed
            else:
                self.speedMultiplier = self.getDashForwardSpeed()
        elif self.isRunning and self.player.weaponState not in (gametypes.WEAR_BACK_ATTACH, gametypes.WEAR_WAIST_ATTACH):
            if self.moveAfterJump:
                jumpMoveSpeed = PCD.data.get('jumpMoveSpeed', 3.0)
                if self.backwardMagnitude > 0:
                    self.speedMultiplier = jumpMoveSpeed * 0.6
                else:
                    self.speedMultiplier = jumpMoveSpeed
            elif self.backwardMagnitude > 0:
                self.speedMultiplier = self.runBackSpeed
            else:
                self.speedMultiplier = self.runFwdSpeed
            if self.player.canFly():
                flyHorizonSpeed = utils.getFlyHorizonSpeed(self.player)
                if self.backwardMagnitude > 0:
                    self.speedMultiplier = flyHorizonSpeed * 0.6
                else:
                    self.speedMultiplier = flyHorizonSpeed
                if self.player.gmMode:
                    flyHorizonSpeed = max(utils.getFlyVerticalSpeed(self.player), flyHorizonSpeed, PCD.data.get('flyHorizonSpeed', gametypes.WING_TAKE_OFF_SPEED))
                    self.speedMultiplier = flyHorizonSpeed
            if self.isOnSwimRide():
                if self.backwardMagnitude > 0:
                    self.speedMultiplier = self.swimRunBackSpeed
                else:
                    self.speedMultiplier = self.swimRunFwdSpeed
        elif self.isWalking or self.player.weaponState in (gametypes.WEAR_BACK_ATTACH, gametypes.WEAR_WAIST_ATTACH):
            if self.isOnSwimRide():
                if self.backwardMagnitude > 0:
                    self.speedMultiplier = self.swimWalkBackSpeed
                else:
                    self.speedMultiplier = self.swimWalkFwdSpeed
            elif self.backwardMagnitude > 0:
                self.speedMultiplier = self.walkBackSpeed
            else:
                self.speedMultiplier = self.walkFwdSpeed
        elif self.backwardMagnitude > 0:
            self.speedMultiplier = self.walkBackSpeed
        else:
            self.speedMultiplier = self.walkFwdSpeed

    def leftMouseFunction(self, isDown):
        if isDown:
            gamelog.debug('zf:leftMouseFunction', isDown)

    def rightMouseFunction(self, isDown):
        if isDown:
            BigWorld.player().circleEffect.cancel()

    def isOnSwimRide(self):
        owner = self.player
        if not owner or not owner.inWorld:
            return False
        if owner.isOnSwimRide() and owner.qinggongMgr.checkCanRideSwim():
            return True
        return False

    def lockTargetsTarget(self, isDown):
        if isDown and self.player.targetLocked:
            lockedId = getattr(self.player.targetLocked, 'lockedId', None)
            if lockedId:
                ent = BigWorld.entities.get(lockedId, None)
                if ent and ent != self.player.targetLocked:
                    self.player.lockTarget(ent, lockAim=True)

    def onTargetFocus(self, entity, lockAim):
        pass

    def changeCursorState(self, entity, lockAim, quickLock = False):
        pass

    def onTargetBlur(self, entity):
        pass

    def _timeAutoMove(self):
        self._autorunStime = BigWorld.time()

    def _enterAutoMove(self):
        if self._autorunStime == 0:
            return False
        timespan = BigWorld.time() - self._autorunStime
        self._autorunStime = 0
        if timespan >= self.autoMoveTimespan and not self.isChasing:
            self.startAutoMove()
        elif timespan > 0:
            self.isAutoMoving = False
        return self.isAutoMoving

    def startAutoMove(self):
        if self.player.stateMachine.checkMove() and self.player.stateMachine.checkStatus(const.CT_AUTO_MOVE):
            if self.isChasing:
                self.stopChasing()
            self.isAutoMoving = True
            self.updateVelocity()
            if self.player.inSwim == const.DEEPWATER:
                self.player.physics.enableSwimJump = True
            else:
                self.player.physics.enableSwimJump = False

    def stopAutoMove(self):
        self.isAutoMoving = False
        self.forwardMagnitude = 0
        self.updateVelocity()

    def stopChasing(self):
        pass

    def breakDashStopAction(self):
        actType = self.player.fashion.doingActionType()
        actId = None
        if actType == action.HORSE_DASH_STOP_ACTION:
            actId = self.player.fashion.getHorseSprintStopAction()
        elif actType == action.DASH_STOP_ACTION:
            actId = self.player.fashion.getDashStopAction()
        if actId:
            self.player.fashion.stopActionByName(self.player.model, actId)
            if self.player.inRidingHorse() and hasattr(self.player.model, 'ride'):
                self.player.fashion.stopActionByName(self.player.model.ride, actId)

    def moveControl(self, desc, isDown):
        if self.isMovingActionKeyControl():
            self.breakDashStopAction()
            if hasattr(self.player, 'tride') and self.player.tride.inRide():
                header = self.player.tride.getHeader()
                if header and header.inRidingHorse():
                    for key in self.player.tride.keys():
                        idx = self.player.tride.get(key)
                        model = self.player.modelServer.getRideTogetherModelByIdx(idx)
                        modelServer = self.player.modelServer
                        if self.player.inFlyTypeFlyRide() and modelServer and modelServer.rideAttached.flyRideIdleAction:
                            pass
                        else:
                            self.player.fashion.stopModelAction(model)

        if self.player.isCombineMove():
            if self.player.fashion.doingActionType() == action.NORMAL_READY_ACTION:
                self.player.fashion.stopAction()

    def setMoveAfterJump(self):
        if self.player.isJumping and self.player.qinggongMgr.getDistanceFromGround() >= 0.5:
            self.moveAfterJump = True
        else:
            self.moveAfterJump = False

    def moveForward(self, isDown):
        if isDown:
            if not self.player.stateMachine.checkMove() or self.player.needForbidForwardOp():
                return
            if not self.player.stateMachine.checkStatus(const.CT_INIT_MOVE):
                return
            if not self.player.checkTempGroupFollow():
                return
            self.forwardMagnitude = 1
            if self.player.inSwim == const.DEEPWATER:
                self.player.physics.enableSwimJump = True
            else:
                self.player.physics.enableSwimJump = False
            self.setMoveAfterJump()
        else:
            self.player.physics.enableSwimJump = False
            if not (getattr(self.player, 'inForceNavigate', False) and self.player.bianshen[0] == gametypes.BIANSHEN_ZAIJU):
                if not (getattr(self.player, 'inChaoFeng', False) or getattr(self.player, 'inMeiHuo', False)):
                    self.forwardMagnitude = 0

    def moveBackward(self, isDown):
        if isDown:
            if not self.player.checkTempGroupFollow():
                return
            if not self.player.stateMachine.checkMove() or self.player.needForbidBackOp():
                return
            if not self.player.stateMachine.checkStatus(const.CT_INIT_MOVE):
                return
            self.backwardMagnitude = 1
            self.setMoveAfterJump()
        else:
            self.backwardMagnitude = 0

    def moveLeft(self, isDown):
        if isDown:
            if not self.player.checkTempGroupFollow():
                return
            if self.player.qinggongMgr.state in (qingGong.STATE_DASH_TWICE_JUMPING,
             qingGong.STATE_SLIDE_DASH,
             qingGong.STATE_SLIDE_SLOW_FALLING,
             qingGong.STATE_SLIDE_FAST_FALLING,
             qingGong.STATE_COLLIDE_FALLING):
                return
            if not self.player.stateMachine.checkMove() or self.player.needForbidSideOp():
                return
            if not self.player.stateMachine.checkStatus(const.CT_INIT_MOVE):
                return
            self.leftwardMagnitude = 1
            self.setMoveAfterJump()
        else:
            self.leftwardMagnitude = 0

    def moveUp(self, moveUp, moveDown):
        if self.player.inPUBGParachute():
            return
        if self.player.inPUBGPlane():
            return
        if not self.player.canFly():
            return
        if moveUp and not moveDown or not moveUp and moveDown:
            if self.player.qinggongMgr.state in (qingGong.STATE_DASH_TWICE_JUMPING,
             qingGong.STATE_SLIDE_DASH,
             qingGong.STATE_SLIDE_SLOW_FALLING,
             qingGong.STATE_SLIDE_FAST_FALLING,
             qingGong.STATE_COLLIDE_FALLING):
                return
            if not self.player.stateMachine.checkMove():
                return
            if not self.player.stateMachine.checkStatus(const.CT_INIT_MOVE):
                return
            if not self.player.checkTempGroupFollow():
                return
            speedData = self.player.getSpeedData()
            if moveUp:
                self.upwardMagnitude = 1.0 * speedData.get('rushUpFactor', 1.0)
            else:
                self.upwardMagnitude = -1.0 * speedData.get('rushUpFactor', 1.0)
        else:
            self.upwardMagnitude = 0

    def moveLeftForward(self, isDown):
        if isDown:
            if not self.player.stateMachine.checkMove() or self.player.needForbidSideOp() or self.player.needForbidForwardOp():
                return
            if not self.player.stateMachine.checkStatus(const.CT_INIT_MOVE):
                return
            if not self.player.checkTempGroupFollow():
                return
            self.leftwardMagnitude = AvatarPhysics.SIN_OF_45
            self.forwardMagnitude = AvatarPhysics.SIN_OF_45
            self.setMoveAfterJump()

    def moveRightForward(self, isDown):
        if isDown:
            if not self.player.stateMachine.checkMove() or self.player.needForbidSideOp() or self.player.needForbidForwardOp():
                return
            if not self.player.stateMachine.checkStatus(const.CT_INIT_MOVE):
                return
            if not self.player.checkTempGroupFollow():
                return
            self.rightwardMagnitude = AvatarPhysics.SIN_OF_45
            self.forwardMagnitude = AvatarPhysics.SIN_OF_45
            self.setMoveAfterJump()

    def moveLeftBackward(self, isDown):
        if isDown:
            if not self.player.stateMachine.checkMove() or self.player.needForbidSideOp() or self.player.needForbidBackOp():
                return
            if not self.player.stateMachine.checkStatus(const.CT_INIT_MOVE):
                return
            if not self.player.checkTempGroupFollow():
                return
            self.leftwardMagnitude = AvatarPhysics.SIN_OF_45
            self.backwardMagnitude = AvatarPhysics.SIN_OF_45
            self.setMoveAfterJump()

    def moveRightBackward(self, isDown):
        if isDown:
            if not self.player.stateMachine.checkMove() or self.player.needForbidSideOp() or self.player.needForbidBackOp():
                return
            if not self.player.stateMachine.checkStatus(const.CT_INIT_MOVE):
                return
            if not self.player.checkTempGroupFollow():
                return
            self.rightwardMagnitude = AvatarPhysics.SIN_OF_45
            self.backwardMagnitude = AvatarPhysics.SIN_OF_45
            self.setMoveAfterJump()

    def moveRight(self, isDown):
        if isDown:
            if self.player.qinggongMgr.state in (qingGong.STATE_DASH_TWICE_JUMPING,
             qingGong.STATE_SLIDE_DASH,
             qingGong.STATE_SLIDE_SLOW_FALLING,
             qingGong.STATE_SLIDE_FAST_FALLING,
             qingGong.STATE_COLLIDE_FALLING):
                return
            if not self.player.stateMachine.checkMove() or self.player.needForbidSideOp():
                return
            if not self.player.stateMachine.checkStatus(const.CT_INIT_MOVE):
                return
            if not self.player.checkTempGroupFollow():
                return
            self.rightwardMagnitude = 1
            self.setMoveAfterJump()
        else:
            self.rightwardMagnitude = 0

    def canTurn(self):
        if self.player.isLockYaw:
            return False
        if gameglobal.rds.ui.homeEditor.isInHomeEditorMode():
            return False
        if self.player.wingWorldCarrier.get(self.player.id) == const.WING_WORLD_CARRIER_MAJOR_IDX and self.player.wingWorldCarrier.isBecomeLadder:
            return False
        return True

    def turnLeft(self, isDown):
        if not self.canTurn():
            return
        dc = BigWorld.dcursor()
        if isDown and not self.player.needLockCameraAndDc() and self.player.rightMouseAble and not self.player.isPathfinding:
            dc.deltaYaw = -self.turnSpeed
            self.updateVelocity()
        else:
            dc.deltaYaw = 0
        self.player.stateMachine.afterTurn()

    def turnRight(self, isDown):
        if not self.canTurn():
            return
        dc = BigWorld.dcursor()
        if isDown and not self.player.needLockCameraAndDc() and self.player.rightMouseAble and not self.player.isPathfinding:
            dc.deltaYaw = self.turnSpeed
            self.updateVelocity()
        else:
            dc.deltaYaw = 0
        self.player.stateMachine.afterTurn()

    def setYaw(self, yaw, forbidCamRotate = False):
        dc = BigWorld.dcursor()
        cc = gameglobal.rds.cam.cc
        if forbidCamRotate:
            cc.canRotate = False
        ccameraYaw = cc.deltaYaw
        ccameraYaw += dc.yaw - yaw
        if ccameraYaw > math.pi:
            ccameraYaw -= math.pi * 2
        if ccameraYaw < -math.pi:
            ccameraYaw += math.pi * 2
        cc.deltaYaw = ccameraYaw
        dc.yaw = yaw

    def setYawAndCamera(self, yaw):
        dc = BigWorld.dcursor()
        cc = gameglobal.rds.cam.cc
        ccameraYaw = cc.deltaYaw
        ccameraYaw += dc.yaw - cc.direction.yaw
        if ccameraYaw > math.pi:
            ccameraYaw -= math.pi * 2
        if ccameraYaw < -math.pi:
            ccameraYaw += math.pi * 2
        cc.deltaYaw = ccameraYaw
        dc.yaw = yaw

    def stopMove(self, down = False):
        if self.player.isAscending:
            return
        self.endFlyAccelerate(True, False)
        self.upwardMagnitude = 0
        self.forwardMagnitude = 0
        self.backwardMagnitude = 0
        self.leftwardMagnitude = 0
        self.rightwardMagnitude = 0
        self.isAutoMoving = False
        self.player.isMoving = False
        cellCmd.endUpQinggongState()
        dc = BigWorld.dcursor()
        dc.deltaYaw = 0
        self.isChasing = False
        self.chasingEntity = None
        self.ccamera.allResetYaw = False
        self.stopSeek()
        self.player.isDashing = False
        self.player.am.matcherCoupled = True
        self.jumpCnt = 0
        if down:
            self.physics.velocity = (0, 0, 0)
        else:
            self.physics.velocity = (0, self.physics.velocity.y, 0)
        self.physics.maxTopVelocity = self.physics.velocity

    def cancelskill(self):
        p = self.player
        if p.spellingType in [action.S_SPELLING]:
            cellCmd.cancelSkill()
            p.stopSpell(False)
        elif p.spellingType in [action.S_SPELLCHARGE]:
            if p.isChargeKeyDown:
                cellCmd.cancelSkill()
        elif p.isGuiding:
            cellCmd.cancelSkill()
        elif p.isDoingAction:
            cellCmd.cancelAction(const.CANCEL_ACT_SKILL)

    def realJumpUp(self, isDown):
        if self.player.inRiding() and not self.isMovingActionKeyControl() and self.player.jumpState == gametypes.DEFAULT_JUMP and not self.player.isPathfinding:
            if isDown:
                if self.player.bianshenStateMgr.canFly():
                    self.player.cell.enterFlyRide()
                else:
                    self.player.horseRoar()
        elif self.player.inSwim:
            if self.player.physics.seeking:
                self.stopSeek()
            if isDown:
                if BigWorld.time() - self.realDashTime < AvatarPhysics.DOUBLE_JUMP_TOLERANCE:
                    self.player.showGameMsg(GMDD.data.OPERATION_FREQUENT, ())
                    return
                item = self.player.equipment[gametypes.EQU_PART_RIDE]
                if not (item and item.canOnlySwim() and self.player.isOnSwimRide()):
                    self.upwardMagnitude = 1.0
                    self.physics.enableSwimJump = True
            else:
                self.upwardMagnitude = 0
                self.player.physics.enableSwimJump = False
            self.updateVelocity()
        elif self._realJump(isDown):
            if self.player.isOnFlyRide():
                if not self.player.canFly():
                    if self.player.bianshenStateMgr.canFly():
                        self.player.cell.enterFlyRide()
                    else:
                        self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_SPACE_DOWN)
            else:
                self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_SPACE_DOWN)
        self.player.clearHoldingSkills()
        return True

    def autoJumpUp(self, isDown):
        if self._realJump(isDown):
            self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_NONE)
        return True

    def landWingFlyUp(self, isDown):
        if isDown:
            if not self.player.checkTempGroupFollow():
                return
            p = BigWorld.player()
            if p.inWingTakeOff:
                return
            if not p.inFly:
                if not p.stateMachine.checkOpenWingFly():
                    return
                if not p.qinggongMgr.checkCanWingFlyLandUp():
                    return
                p.enterWingFly()
        elif self.player.canSwim():
            self.realJumpUp(isDown)
            return

    def landWingFlyDown(self, isDown):
        if isDown:
            self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_WINGFLY_LANDDOWN)

    def flyUp(self, isDown, needStopAction = True):
        needStopAction = self.checkNeedStopActionInFly() and needStopAction
        if isDown:
            if not self.player.stateMachine.checkMove():
                return
            if not self.player.stateMachine.checkStatus(const.CT_INIT_MOVE):
                return
            speedData = self.player.getSpeedData()
            self.upwardMagnitude = 1.0 * speedData.get('rushUpFactor', 1.0)
            self.stopSeek()
            if not (self.isInAccelerating() or self.isInDecelerating()) and needStopAction:
                wingFlyUpActionName = self.player.fashion.getWingFlyNormalUpAction()
                self.player.fashion.playSingleAction(wingFlyUpActionName)
                self.player.qinggongMgr.playWingFlyModelAction([wingFlyUpActionName])
        else:
            self.upwardMagnitude = 0.0
            if needStopAction:
                if self.player.fashion.doingActionType() in (action.ROLL_ACTION, action.ROLLSTOP_ACTION):
                    pass
                elif not self.player.inFlyTypeFlyRide() and not self.player.inFlyTypeFlyZaiju():
                    self.player.fashion.stopAllActions()
                    self.player.qinggongMgr.stopWingFlyModelAction()
                else:
                    rideAttached = self.player.modelServer.rideAttached
                    if rideAttached and not rideAttached.flyRideIdleAction:
                        self.player.fashion.stopAllActions()
                    self.player.fashion.stopAction()
            if self.player.qinggongState in gametypes.QINGGONG_WINGFLY_STATES or self.player.qinggongState == 0 and self.needForceEndQingGong:
                if not self.isAnyDirKeyDown():
                    cellCmd.endUpQinggongState()
        self.updateVelocity()

    def checkNeedStopActionInFly(self):
        p = self.player
        if p.spellingType in [action.S_SPELLING, action.S_SPELLCHARGE] or p.isGuiding or p.isDoingAction:
            return False
        return True

    def flyDown(self, isDown, needStopAction = True):
        needStopAction = self.checkNeedStopActionInFly() and needStopAction
        if isDown:
            if not self.player.isPathfinding and not self.player.stateMachine.checkMove():
                return
            speedData = self.player.getSpeedData()
            self.upwardMagnitude = -1.0 * speedData.get('rushDownFactor', 1.0)
            self.player.setGravity(gametypes.NOMAL_DOWNGRAVITY)
            if not (self.isInAccelerating() or self.isInDecelerating()):
                if self.player.fashion.doingActionType() != action.WING_FLY_DOWN_ACTION and needStopAction:
                    wingFlyDownActionName = self.player.fashion.getWingFlyNormalDownAction()
                    self.player.fashion.playSingleAction(wingFlyDownActionName, action.WING_FLY_DOWN_ACTION)
                    self.player.qinggongMgr.playWingFlyModelAction([wingFlyDownActionName])
        else:
            if not self.player.isPathfinding:
                self.player.setGravity(0.0)
            self.upwardMagnitude = 0.0
            if needStopAction:
                if self.player.fashion.doingActionType() in (action.ROLL_ACTION, action.ROLLSTOP_ACTION):
                    pass
                elif not self.player.inFlyTypeFlyRide() and not self.player.inFlyTypeFlyZaiju():
                    self.player.fashion.stopAllActions()
                    self.player.qinggongMgr.stopWingFlyModelAction()
                else:
                    rideAttached = self.player.modelServer.rideAttached
                    if rideAttached and not rideAttached.flyRideIdleAction:
                        self.player.fashion.stopAllActions()
                    self.player.fashion.stopAction()
            if self.player.qinggongState in gametypes.QINGGONG_WINGFLY_STATES or self.player.qinggongState == 0 and self.needForceEndQingGong:
                if not self.isAnyDirKeyDown():
                    cellCmd.endUpQinggongState()
        self.updateVelocity()

    def getNormalMaxXSpeed(self):
        return self.speedMultiplier

    def getNormalMaxYSpeed(self):
        return self.upSpeedMultiplier

    def getNormalMaxZSpeed(self):
        return self.speedMultiplier

    def startFlyAccelerate(self, flyType):
        if not self.player.canFly():
            return
        if self._forward:
            self.physics.velocity = (0, 0, 0)
        speedData = self.player.getSpeedData()
        if flyType == gameglobal.QUICK_FLY:
            accelerateSpeed = speedData.get('flyRushAccelerateSpeed', 1.0)
            maxVelocity = utils.getFlyRushMaxSpeed(self.player)
            self.physics.maxTopVelocity = (self.getNormalMaxXSpeed(), self.getNormalMaxYSpeed(), maxVelocity)
            self.physics.startAccelerate(0, 0, accelerateSpeed)
        elif flyType == gameglobal.QUICK_FLY_UP:
            accelerateSpeed = speedData.get('flyRushAccelerateSpeed', 5.0)
            maxVelocity = utils.getFlyRushMaxSpeed(self.player)
            self.physics.maxTopVelocity = (self.getNormalMaxXSpeed(), maxVelocity, self.getNormalMaxZSpeed())
            self.physics.startAccelerate(0, accelerateSpeed, 0)
        elif flyType == gameglobal.QUICK_FLY_DOWN:
            accelerateSpeed = speedData.get('flyRushAccelerateSpeed', 5.0)
            maxVelocity = utils.getFlyRushMaxSpeed(self.player)
            self.physics.maxTopVelocity = (self.getNormalMaxXSpeed(), -maxVelocity, self.getNormalMaxZSpeed())
            self.physics.startAccelerate(0, -accelerateSpeed, 0)
        elif flyType == gameglobal.QUICK_FLY_LEFT:
            accelerateSpeed = speedData.get('flyRushAccelerateSpeed', 5.0)
            maxVelocity = utils.getFlyRushMaxSpeed(self.player)
            self.physics.maxTopVelocity = (-maxVelocity, self.getNormalMaxYSpeed(), self.getNormalMaxZSpeed())
            self.physics.startAccelerate(-accelerateSpeed, 0, 0)
        elif flyType == gameglobal.QUICK_FLY_RIGHT:
            accelerateSpeed = speedData.get('flyRushAccelerateSpeed', 5.0)
            maxVelocity = utils.getFlyRushMaxSpeed(self.player)
            self.physics.maxTopVelocity = (maxVelocity, self.getNormalMaxYSpeed(), self.getNormalMaxZSpeed())
            self.physics.startAccelerate(accelerateSpeed, 0, 0)
        elif flyType == gameglobal.QUICK_FLY_BACK:
            accelerateSpeed = speedData.get('flyRushAccelerateSpeed', 5.0)
            maxVelocity = utils.getFlyRushMaxSpeed(self.player)
            self.physics.maxTopVelocity = (self.getNormalMaxXSpeed(), self.getNormalMaxYSpeed(), -maxVelocity)
            self.physics.startAccelerate(0, 0, -accelerateSpeed)
        else:
            if self.flyType == gameglobal.QUICK_FLY_BACK:
                self.physics.endAccelerate()
            self.acceleratingEndNotifier()
            accelerateSpeed = speedData.get('flyAccelerateSpeed', 1.0)
            maxVelocity = utils.getFlyMaxSpeed(self.player)
            self.physics.maxTopVelocity = Math.Vector3(self.getNormalMaxXSpeed(), self.getNormalMaxYSpeed(), maxVelocity)
            self.physics.startAccelerate(0, 0, accelerateSpeed)
        self.resetAvatarTopSpeed()
        self.flyType = flyType

    def startFlyDecelerate(self, flyType):
        if not self.player.canFly():
            return
        if not getattr(self.physics, 'isAccelerating', getattr(self.physics, 'acceleratingState', 0)):
            return
        if flyType != self.flyType:
            return
        self.endFlyAccelerate(True)

    def endFlyAccelerate(self, isDown, needAction = True):
        if isDown and self.physics.maxTopVelocity:
            self.physics.endAccelerate()
            self.flyType = gameglobal.DEFAUL_FLY
            self.physics.maxTopVelocity = Math.Vector3(0, 0, 0)
            if self.player.fashion.doingActionType() in (action.JUMP_ACTION, action.JIDAO_START_ACTION, action.DEAD_ACTION):
                return
            if not self.player.inFlyTypeFlyRide() and not self.player.inFlyTypeFlyZaiju():
                self.player.fashion.stopAllActions()
                self.player.qinggongMgr.stopWingFlyModelAction()
            self.resetAvatarTopSpeed()
            if self.player.canFly() and not self.player.inMoving() and needAction:
                flyStopActionName = self.player.fashion.getWingFlyStopAction()
                self.player.fashion.playSingleAction(flyStopActionName)
                self.player.qinggongMgr.playWingFlyModelAction([flyStopActionName])

    def acceleratingEndNotifier(self):
        if not self.player.inFlyTypeFlyRide() and not self.player.inFlyTypeFlyZaiju():
            self.player.fashion.stopAllActions()
            self.player.qinggongMgr.stopWingFlyModelAction()
        self.player.updateActionKeyState()
        if not (self.flyType == gameglobal.SLOW_FLY and HK.HKM[HK.KEY_FORWARD].isAnyDown()):
            self.flyType = gameglobal.DEFAUL_FLY

    def _realJump(self, isDown):
        self.player.physics.dcControlPitch = not isDown or self.player.needDcControlPitch()
        if not isDown:
            return False
        currentTime = BigWorld.time()
        if currentTime - self.realSpaceKeyTime < AvatarPhysics.SPACE_JUMP_TIME_INTERVAL:
            self.switchToRun(True)
            return False
        if self.player._isOnZaiju() and self.player.needForbidJump():
            return False
        if self.player.qinggongMgr.state in (qingGong.STATE_SLIDE_DASH,):
            return False
        if self.player.fashion.doingActionType() in (action.DASH_START_ACTION,):
            self.player.fashion.stopActionByName(self.player.model, action.DASH_START_ACTION)
        if self.isJumpEnd:
            return False
        if self.player.qinggongMgr.getDistanceFromGround() <= 2.0 and self.player.qinggongMgr.state not in (qingGong.STATE_JUMPING,
         qingGong.STATE_DASH,
         qingGong.STATE_IDLE,
         qingGong.STATE_IN_COMBAT_IDLE):
            return False
        if self.player.qinggongMgr.state == qingGong.STATE_JUMPING:
            if self.player.qinggongMgr.getDistanceFromGround() <= PCD.data.get('twiceJumpHighLimit', 0.6):
                return False
        if not self.player.stateMachine.checkJump():
            return False
        self.jumpCnt += 1
        if self.player.qinggongMgr.jumpDashFlag and self.jumpCnt <= 2:
            self.switchToRun()
            self.player.qinggongMgr.jumpDashFlag = False
            self.player.showGameMsg(GMDD.data.OPERATION_FREQUENT, ())
            return False
        if self.player.qinggongMgr.state not in (qingGong.STATE_TWICE_JUMPING, qingGong.STATE_DASH_TWICE_JUMPING, qingGong.STATE_SLIDE_DASH):
            self.realJumpTime = BigWorld.time()
        elif self.player.qinggongMgr.state in (qingGong.STATE_IDLE, qingGong.STATE_IN_COMBAT_IDLE):
            self.realJumpTime = -1.0
        self.realSpaceKeyTime = currentTime
        self.jumpTopCnt = 0
        self.needDoJump = True
        return True

    def traceEntity(self, entity, desireDist):
        self.isTracing = True
        self.beginChase(entity, desireDist)

    def isUnderWater(self):
        res = self.player.getHeightOutOfWater()
        if res and res < 0 and getattr(self.player, 'isInsideWater', False):
            return True
        else:
            return False

    def _enterSlideStatus(self):
        self.physics.keepJumpVelocity = False
        self.forwardMagnitude = 1
        self.player.am.applyFlyRoll = True
        self.updateVelocity()

    def _doJump(self):
        if not self.needDoJump:
            return
        gamelog.debug('_doJump')
        p = self.player
        fashion = p.fashion
        if p.life == gametypes.LIFE_DEAD:
            fashion.breakJump()
            return
        self.physics.fall = True
        if self.player.qinggongState == gametypes.QINGGONG_STATE_FAST_BIG_JUMP:
            self._enterSlideStatus()
        if self.player.jumpState in [gametypes.DEFAULT_JUMP,
         gametypes.DEFAULT_TWICE_JUMP,
         gametypes.DASH_TWICE_JUMP,
         gametypes.AUTO_JUMP]:
            self.physics.keepJumpVelocity = False
        else:
            self.physics.keepJumpVelocity = True
        self.physics.jump(True, self.player.isJumping or self.physics.jumping)
        self.setJumpStartEnergy()
        self.upwardMagnitude = 1
        self.updateVelocity()

    def jumpEnd(self, end):
        p = self.player
        self.isJumpEnd = True
        self.jumpTopCnt = 0
        self.needDoJump = True
        self.player.jumpActionMgr.jumpEndTime = BigWorld.time()
        p.ap.physics.upSpeedAttenu = 0
        jumpState = self.player.jumpState
        afterBigJump = jumpState in (gametypes.DASH_BIG_JUMP, gametypes.DASH_TWICE_JUMP)
        p.fashion.jump(0)
        self.afterJumpEnd(False, afterBigJump)
        gameglobal.rds.ui.actionbar.checkAllSkillStat(gameglobal.SKILL_STAT_NO_SKILL)

    def jumpTop(self, top):
        if self.player.inSwim:
            return
        self.jumpTopCnt += 1
        if self.jumpTopCnt >= self.JUMP_TOP_TIMES:
            self.jumpTopCnt = 0
            if self.player.isJumping != self.player.physics.jumping:
                self.jumpEnd(True)

    def breakJumpCallback(self, b):
        gamelog.debug('jump collide breakJumpCallback......................')
        if self.player.inSwim:
            return
        self.afterJumpEnd(True)

    def afterJumpEnd(self, collide = False, afterBigJump = False):
        if self.player.canFly():
            return
        self.restoreJumpState(collide, afterBigJump)
        if self.player.life == gametypes.LIFE_DEAD:
            self.stopMove()

    def restoreJumpState(self, collide = False, afterBigJump = False):
        self.player.qinggongMgr.setState(qingGong.STATE_IDLE)
        self.player.jumpState = gametypes.DEFAULT_JUMP
        if self.player.getOperationMode() == gameglobal.MOUSE_MODE:
            self.player.isDashing = (HK.HKM[HK.KEY_FORWARD].isAnyDown() or HK.HKM[HK.KEY_BACKWARD].isAnyDown() or HK.HKM[HK.KEY_MOVELEFT].isAnyDown() or HK.HKM[HK.KEY_MOVERIGHT].isAnyDown()) and self.player.isDashing
        else:
            self.player.isDashing = HK.HKM[HK.KEY_FORWARD].isAnyDown() and self.player.isDashing
        if self.player.isDashing:
            self.setUpSpeedMultiplier()
            self.player.isDashing = False
            self.player.qinggongMgr.jumpDashFlag = True
            qingGong.switchToDash(self.player, False, afterBigJump)
        else:
            self.player.qinggongMgr.dashStartFlag = True
            self.setUpSpeedMultiplier()
            self.needForceEndQingGong = True
            cellCmd.endUpQinggongState()
            self.player.qinggongState = gametypes.QINGGONG_STATE_DEFAULT
            gameglobal.rds.cam.leaveDashFov()
            self.player.qinggongMgr.stopWindSound()
        self.player.am.matcherCoupled = True
        self.jumpCnt = 0
        self.player.qinggongMgr.rushTop = False
        self.player.am.applyFlyRoll = False
        if not collide:
            if not self.player.isInsideWater:
                self.player.setGravity(gametypes.NOMAL_DOWNGRAVITY)
        self.upwardMagnitude = 0
        self.player.jumpActionMgr.jumpEndTime = -1.0
        self.player.cell.startJumping(False)
        self.isJumpEnd = False
        self.moveAfterJump = False
        self.player.updateUseSkillKeyState()
        self.player.updateActionKeyState()

    def setJumpEnergy(self, isDown = True):
        p = self.player
        if p.jumpState == gametypes.DEFAULT_JUMP:
            self.player.setGravity(SYSCD.data.get('runDownGravity', gametypes.RUN_DOWNGRAVITY))
        elif p.jumpState == gametypes.DASH_JUMP:
            isInHorse = p.inRiding() and p.bianshen[0] == gametypes.BIANSHEN_RIDING_RB
            if isInHorse:
                self.player.setGravity(PCD.data.get('horseDashDownGravity', gametypes.HORSE_DASH_DOWNGRAVITY))
            else:
                self.player.setGravity(PCD.data.get('dashDownGravity', gametypes.DASH_DOWNGRAVITY))
        elif p.jumpState == gametypes.DASH_BIG_JUMP:
            self.player.setGravity(PCD.data.get('dashDownGravity', gametypes.DASH_DOWNGRAVITY))
        elif p.jumpState == gametypes.DEFAULT_TWICE_JUMP:
            self.player.setGravity(SYSCD.data.get('runTwiceGravity', gametypes.RUNTWICE_GRAVITY))
        elif p.jumpState == gametypes.DASH_TWICE_JUMP:
            self.player.setGravity(SYSCD.data.get('dashTwiceGravity', gametypes.DASHTWICE_GRAVITY))
        elif p.jumpState == gametypes.AUTO_JUMP:
            self.player.setGravity(PCD.data.get('autoJumpGravity', gametypes.AUTO_JUMP_GRAVITY))
        elif p.jumpState == gametypes.DASH_AUTO_JUMP:
            self.player.setGravity(PCD.data.get('dashAutoJumpGravity', gametypes.AUTO_JUMP_GRAVITY))

    def setJumpStartEnergy(self):
        self.setJumpEnergy()

    def restore(self, needResetPos = True):
        self.ccamera.canRotate = False
        self.isAutoMoving = False
        self.dcursor.canRotate = False
        self.forwardMagnitude = 0.0
        self.backwardMagnitude = 0.0
        self.upwardMagnitude = 0.0
        self.rightwardMagnitude = 0.0
        self.leftwardMagnitude = 0.0
        if not self.player.isAscending:
            self.physics.velocity = (0, 0, 0)
            self.physics.seek(None, 0, 0, None)

    def release(self):
        pass

    def beginChase(self, entity, desiredDist):
        gamelog.debug('beginChase:', entity.id)
        self.isChasing = True
        self.isAutoMoving = False
        self.chasingEntity = entity
        if not self.player.inGroupFollow:
            self.ccamera.canResetYaw = True
        self.ccamera.allResetYaw = True
        self.endFlyAccelerate(True)
        self.physics.maxTopVelocity = Math.Vector3(0, 0, 0)
        self.chaseEntity(entity, desiredDist)
        self.updateVelocity()

    def clearChaseData(self):
        gamelog.debug('clearChaseData')
        self.isChasing = False
        self.ccamera.allResetYaw = False
        self.forwardMagnitude = 0
        self.chaseNum = 0

    def chaseEntity(self, entity, desireDist):
        if self.player.isForceMove:
            return
        gamelog.debug('chaseEntity:1', entity.id, desireDist, self.isChasing)
        if not entity.inWorld or entity.spaceID != entity.spaceID:
            gamelog.debug('chaseEntity:2', entity.id, entity.spaceID != entity.spaceID, self.isChasing)
            self.isTracing = False
            self.clearChaseData()
            return
        if not self.isChasing or entity != self.chasingEntity:
            gamelog.debug('chaseEntity:3', entity != self.chasingEntity, self.isChasing)
            self.isTracing = False
            self.clearChaseData()
            return
        if self.isTracing and hasattr(entity, 'getOpacityValue') and entity.getOpacityValue()[0] == gameglobal.OPACITY_HIDE:
            self.isTracing = False
            self.clearChaseData()
            return
        dirVector = self.player.position - entity.position
        length = dirVector.length
        horizonVector = dirVector
        horizonVector.y = 0
        horizonLength = horizonVector.length
        distance = 0.1
        if self.isTracing:
            distance = 1
        self.chaseNum = self.chaseNum + 1
        gamelog.debug('chaseEntity:4', length, desireDist, distance, entity.id, horizonLength)
        if self.player.isOnFlyRide():
            if not self.player.canFly():
                if self.player.bianshenStateMgr.canFly():
                    self.player.cell.enterFlyRide()
        if length > desireDist + distance and (horizonLength > distance or self.player.inFly):
            s = desireDist / length
            dirVector.x *= s
            dirVector.y *= s
            dirVector.z *= s
            destPos = entity.position + dirVector
            gamelog.debug('chaseEntity:5', destPos)
            if self.isTracing:
                self.seekPath(destPos, self._traceApproach)
            else:
                self.seekPath(destPos, self._chaseApproach)
            self.updateVelocity()
            BigWorld.callback(0.5, Functor(self.chaseEntity, entity, desireDist))
        elif self.isTracing:
            BigWorld.callback(0.5, Functor(self.chaseEntity, entity, desireDist))
        else:
            self.clearChaseData()
            self.updateVelocity()
            BigWorld.callback(0.01, self.player.reachDesiredDist)

    def _traceApproach(self, su):
        if self.player.inGroupFollow and su == -1 and self.isTracing:
            self.traceFailCount += 1
            if self.traceFailCount >= gameglobal.TRACE_FAIL_COUNT:
                self.player.groupFollowTraceFail()
                self.traceFailCount = 0
        else:
            self.traceFailCount = 0
        self.forwardMagnitude = 0
        self.updateMoveControl()

    def _chaseApproach(self, success):
        gamelog.debug('_chaseApproach:', success)
        if success == -1:
            success = 0
        utils.clearLog()
        utils.recusionLog(1)
        self._approach(success)

    def resetCameraPitchRange(self):
        dc = BigWorld.dcursor()
        if self._needLockPitch():
            dc.minPitch = -1
            dc.maxPitch = 0
        else:
            dc.minPitch = -1.134
            dc.maxPitch = 1.56
        gameglobal.rds.cam.setScrollRange()

    def _needLockPitch(self):
        if self.player.inPUBGParachute():
            return True
        return False

    def dropForBlood(self):
        p = self.player
        if self.player.canFly():
            p.clearDropForBlood()
            return
        if self.player.inSwim:
            p.clearDropForBlood()
            return
        if getattr(self.player, 'vehicle', None):
            p.clearDropForBlood()
            return
        mapID = getattr(self.player, 'mapID', 0)
        if mapID in SYSCD.data.get('notDropBloodForMaps', ()):
            p.clearDropForBlood()
            return
        bloodType = p.dropForBlood[0]
        beginHeight = p.dropForBlood[1]
        heightDiff = beginHeight - p.position.y
        if heightDiff < 0:
            return
        p.cell.selfInjure(gametypes.CLIENT_HURT_FALL, heightDiff, bloodType)
        p.clearDropForBlood()

    def collideCallback(self, entityId, collideType, collideWater, collideTri, dropVel, materialKind = 0):
        p = self.player
        if collideType == const.COLLIDETYPE_DOWN:
            if p.inPUBGParachute():
                p.cell.pubgJumpToGround(True)
        if hasattr(p, 'avatarDanDaoCB') and p.avatarDanDaoCB:
            p.avatarDanDaoCB()
            p.avatarDanDaoCB = None
            p.clearAvatarDanDaoCancelCB()
        if p.touchAirWallProcess == 1:
            p.touchAirWallProcess = 2
            p.set_life(gametypes.LIFE_ALIVE)
            gamelog.debug('jorsef: reset touchAirWall')
        gamelog.debug('bgf:collideType', entityId, collideType, dropVel, p.physics.jumping, p.jumpState, p.fashion.fallEndAction, materialKind)
        if not p.canFly() and collideType and not collideWater:
            if not p.vehicle and not p.inSwim:
                p.suggestSpriteFly(False)
        if p.qinggongState == gametypes.QINGGONG_STATE_RUSH_DOWN:
            cellCmd.endUpQinggongState()
            p.updateActionKeyState()
            p.ap.updateVelocity()
            p.am.applyFlyRoll = False
        self.dropForBlood()
        self.player.sprintCount = 0
        if not collideWater:
            if self.player.qinggongState in [gametypes.QINGGONG_STATE_SLIDING,
             gametypes.QINGGONG_STATE_FAST_SLIDING,
             gametypes.QINGGONG_STATE_FAST_SLIDING_WEAPON_IN_HAND,
             gametypes.QINGGONG_STATE_RUSH_DOWN_WEAPON_IN_HAND,
             gametypes.QINGGONG_STATE_RUSH_DOWN]:
                self.player.am.applyFlyRoll = False
                self.player.fashion.stopAllActions()
                self.physics.velocity = Math.Vector3((0, self.physics.velocity[1], 0))
                self.physics.maxTopVelocity = self.physics.velocity
                cellCmd.endUpQinggongState()
        self.collideTypeCheck(entityId, materialKind)
        if materialKind == 136:
            ent = BigWorld.entities.get(entityId)
            if ent and ent.classname() == 'MovingPlatform':
                ent.doAfterCollideWithPlayer()
            else:
                if p.isInCoupleRide():
                    p.cell.cancelCoupleEmote()
                p.cell.teleportOnReachMapBorder()
        if materialKind == gametypes.MATERIAL_TYPE_SHOW_MSG:
            for k, v in SCMD.data.iteritems():
                spaceID = k[0]
                tmpRange1 = k[1][0]
                tmpRange2 = k[1][1]
                if tmpRange1[0] < p.position[0] < tmpRange2[0] and tmpRange1[1] > p.position[2] > tmpRange2[1] and spaceID == p.spaceNo:
                    p.showGameMsg(int(v.get('msgId', 0)), ())

        if self.player.isOnFlyRide() and self.player.inFlyTypeFlyRide() and collideType != 0 and not collideWater and not self.isTracing:
            self.player.cell.leaveFlyRide()
        if self.player.isOnFlyRide() and collideWater:
            if not self.player.bianshenStateMgr.canFly():
                self.player.cell.leaveRide()
        if self.player.fashion.doingActionType() == action.WING_LAND_ACTION:
            self.upwardMagnitude = 0.0
            p.fashion.stopAllActions()
            p.qinggongMgr.stopWingFlyModelAction()
            p.cell.leaveWingFly()
            p.leaveWingTime = time.time()
        if materialKind == gametypes.MATERIAL_TYPE_LAVA:
            envHurtInterval = SYSCD.data.get('envHurtInterval', 1.0)
            if p.lastEnvHurtTime + envHurtInterval < p.getServerTime():
                p.cell.selfInjure(gametypes.CLIENT_HURT_BY_ENV, 1.0, 0)
                p.lastEnvHurtTime = p.getServerTime()
            if p.envHurtTimerId == 0:
                p.envHurtTimerId = BigWorld.callback(envHurtInterval, p.onEnvHurt)
        elif materialKind == gameglobal.TELEPORT_STATIC:
            p.homeRoomFangKaDian()
        elif p.envHurtTimerId != 0:
            BigWorld.cancelCallback(p.envHurtTimerId)
            p.envHurtTimerId = 0
        if p.isInBfDota() and entityId:
            ent = BigWorld.entities.get(entityId, None)
            if utils.instanceof(ent, 'MovingPlatform'):
                if not p.vehicleId:
                    p.enterVehicle(entityId)

    def collideTypeCheck(self, entityId, materialKind):
        entity = BigWorld.entities.get(entityId)
        if not entity:
            return
        if isinstance(entity, Transport) and getattr(entity, 'clientTrigger', False) and materialKind == 136:
            entity.use()
        elif isinstance(entity, Obstacle):
            entity.doDamage()

    def dieCallback(self, collide):
        p = self.player
        gamelog.debug('----jorsef: dieCallback:', p.touchAirWallProcess, self.player)
        if p.touchAirWallProcess == 0 and p.life == gametypes.LIFE_ALIVE:
            p.touchAirWallProcess = 1
            p.cell.selfInjure(gametypes.CLIENT_HURT_DIE, 1.0, 0)
        if p.touchAirWallProcess == 1 and p.life == gametypes.LIFE_DEAD:
            p.touchAirWallProcess = 2
            p.set_life(gametypes.LIFE_ALIVE)

    def actionPromoteCallback(self, actionPromote):
        p = self.player
        actType = p.fashion.doingActionType()
        if actType in [action.HORSE_DASH_STOP_ACTION, action.DASH_STOP_ACTION]:
            return
        if actionPromote:
            p.am.matcherCoupled = False
        else:
            p.am.matcherCoupled = True

    def updateYaw(self, destPos):
        yaw = (destPos - BigWorld.player().position).yaw
        ccameraYaw = self.ccamera.deltaYaw
        ccameraYaw += self.dcursor.yaw - yaw
        if ccameraYaw > math.pi:
            ccameraYaw -= math.pi * 2
        if ccameraYaw < -math.pi:
            ccameraYaw += math.pi * 2
        self.ccamera.deltaYaw = ccameraYaw
        self.dcursor.yaw = yaw
        return yaw

    def autoSeekTo(self, destPos, callback = None, filterYaw = True):
        yaw = self.updateYaw(destPos)
        if callback == None:
            callback = self.__arrive
        BigWorld.player().physics.seek((destPos.x,
         destPos.y,
         destPos.z,
         yaw), self.SEEK_TIME, self.SEEK_TOLERANCE, callback)
        self.forwardMagnitude = 1.0
        self.updateVelocity()

    def __arrive(self, success):
        self.forwardMagnitude = 0
        self.updateVelocity()
        BigWorld.player().physics.stop()

    def seekPath(self, destPos, callback = None, vehicleID = 0, checkStateMachine = True, destYaw = None, continueMode = False):
        if destYaw == None:
            yaw = (destPos - self.player.position).yaw
            if self.chaseNum == 1:
                self.setYaw(yaw, True)
            else:
                self.setYaw(yaw)
        else:
            yaw = destYaw
        if callback == None:
            callback = self._approach
        self.physics.seek((destPos.x,
         destPos.y,
         destPos.z,
         yaw), self.SEEK_TIME, self.SEEK_TOLERANCE, callback, vehicleID, continueMode)
        self.forwardMagnitude = 1.0
        self.updateVelocity()

    def seekPoints(self, points, callback = None):
        if callback == None:
            callback = self._approach
        self.physics.seek(points, self.SEEK_TIME, self.SEEK_TOLERANCE, callback)
        self.forwardMagnitude = 1.0
        self.updateVelocity()

    def stopSeek(self):
        gamelog.debug('User stop seeking................', self.physics.seeking, self.forceSeek)
        if getattr(self.player, 'inForceNavigate', False) and self.player.bianshen[0] == gametypes.BIANSHEN_ZAIJU:
            return
        if self.physics.seeking and not self.forceSeek:
            self.physics.stopseek()
            self.forwardMagnitude = 0.0

    def checkKeyState(self):
        keyState = ((keys.KEY_A, self._a),
         (keys.KEY_D, self._d),
         (keys.KEY_Q, self._q),
         (keys.KEY_E, self._e),
         (keys.KEY_W, self._w),
         (keys.KEY_S, self._s),
         (keys.KEY_LEFTMOUSE, self._msleft),
         (keys.KEY_RIGHTMOUSE, self._msright))
        for key, state in keyState:
            newState = BigWorld.getKeyDownState(key, 0)
            if state != newState:
                self.handleKeyEvent(newState, key, 0)

    def leftDodge(self, isDown):
        if not self.player.checkTempGroupFollow():
            return
        if self.player.inSlowTime and isDown:
            self.player.onSlowTimeActionProcessed(gameglobal.SLOW_TIME_ACTION_LEFTWARD_SHIFT)
            return
        if isDown:
            self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_LEFT_DOWN)
        elif not gameglobal.rds.ui.bInEdit:
            self.updateMoveControl()
            if self.player.qinggongState in gametypes.QINGGONG_WINGFLY_STATES or self.needForceEndQingGong:
                self._qKeyTime = 0.0
                cellCmd.endUpQinggongState()

    def rightDodge(self, isDown):
        if not self.player.checkTempGroupFollow():
            return
        if self.player.inSlowTime and isDown:
            self.player.onSlowTimeActionProcessed(gameglobal.SLOW_TIME_ACTION_RIGHTWARD_SHIFT)
            return
        if isDown:
            self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_RIGHT_DOWN)
        elif not gameglobal.rds.ui.bInEdit:
            self.updateMoveControl()
            if self.player.qinggongState in gametypes.QINGGONG_WINGFLY_STATES or self.needForceEndQingGong:
                self._eKeyTime = 0.0
                cellCmd.endUpQinggongState()

    def backDodge(self, isDown):
        if not self.player.checkTempGroupFollow():
            return
        if self.player.inSlowTime and isDown:
            self.player.onSlowTimeActionProcessed(gameglobal.SLOW_TIME_ACTION_BACKWARD_SHIFT)
            return
        if isDown:
            self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_BACK_DOWN)
        elif not gameglobal.rds.ui.bInEdit:
            self.updateMoveControl()
            if self.player.qinggongState in gametypes.QINGGONG_WINGFLY_STATES or self.needForceEndQingGong:
                self._sKeyTime = 0.0
                cellCmd.endUpQinggongState()

    def upDodge(self, isDown):
        if not self.player.checkTempGroupFollow():
            return
        if not self.player.inFly:
            return
        if isDown:
            self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_WINGFLY_UP)
        elif not gameglobal.rds.ui.bInEdit:
            self.updateMoveControl()
            if self.player.qinggongState in gametypes.QINGGONG_WINGFLY_STATES or self.needForceEndQingGong:
                self._spaceKeyTime = 0.0
                cellCmd.endUpQinggongState()

    def downDodge(self, isDown):
        if not self.player.checkTempGroupFollow():
            return
        if not self.player.inFly:
            return
        if isDown:
            self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_WINGFLY_DOWN)
        elif not gameglobal.rds.ui.bInEdit:
            self.updateMoveControl()
            if self.player.qinggongState in gametypes.QINGGONG_WINGFLY_STATES or self.needForceEndQingGong:
                self._xKeyTime = 0.0
                cellCmd.endUpQinggongState()

    def forwardDodge(self, isDown):
        if not self.player.checkTempGroupFollow():
            return
        if self.player.inSlowTime and isDown:
            self.player.onSlowTimeActionProcessed(gameglobal.SLOW_TIME_ACTION_FORWARD_SHIFT)
            return
        if isDown:
            if BigWorld.player().weaponInHandState() and (self.player.qinggongMgr.state in (qingGong.STATE_DASH_TWICE_JUMPING,
             qingGong.STATE_JUMPING,
             qingGong.STATE_DASH_JUMPING,
             qingGong.STATE_DASH_BIG_JUMPING,
             qingGong.STATE_TWICE_JUMPING,
             qingGong.STATE_RUSH_DOWN,
             qingGong.STATE_RUSH_DOWN_WEAPON_IN_HAND) or self.player.isFalling):
                self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_WEAPON_FORWARD_DOWN)
            else:
                self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_DODGE_FORWARD_DOWN)
        elif self.player.qinggongState in gametypes.QINGGONG_WINGFLY_STATES or self.player.qinggongState in (gametypes.QINGGONG_STATE_FAST_RUN, gametypes.QINGGONG_STATE_MOUNT_DASH) or self.needForceEndQingGong:
            self._wKeyTime = 0.0
            cellCmd.endUpQinggongState()

    def leftMouseDodge(self, isDown):
        if not self.player.checkTempGroupFollow():
            return
        if self.player.inSlowTime and isDown:
            self.player.onSlowTimeActionProcessed(gameglobal.SLOW_TIME_ACTION_FORWARD_SHIFT)
            return
        if isDown:
            if BigWorld.player().weaponInHandState() and (self.player.qinggongMgr.state in (qingGong.STATE_DASH_TWICE_JUMPING,
             qingGong.STATE_JUMPING,
             qingGong.STATE_DASH_JUMPING,
             qingGong.STATE_DASH_BIG_JUMPING,
             qingGong.STATE_TWICE_JUMPING,
             qingGong.STATE_RUSH_DOWN,
             qingGong.STATE_RUSH_DOWN_WEAPON_IN_HAND) or self.player.isFalling):
                self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_WEAPON_FORWARD_DOWN)
            else:
                self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_DODGE_MOUSE_DOWN)
        elif self.player.qinggongState in gametypes.QINGGONG_WINGFLY_STATES or self.player.qinggongState in (gametypes.QINGGONG_STATE_FAST_RUN, gametypes.QINGGONG_STATE_MOUNT_DASH) or self.needForceEndQingGong:
            cellCmd.endUpQinggongState()

    def wingSlideSprint(self, isDown):
        if isDown:
            if self.player.qinggongMgr.state in (qingGong.STATE_DASH_TWICE_JUMPING,
             qingGong.STATE_JUMPING,
             qingGong.STATE_DASH_JUMPING,
             qingGong.STATE_DASH_BIG_JUMPING,
             qingGong.STATE_TWICE_JUMPING,
             qingGong.STATE_RUSH_DOWN) or self.player.isFalling:
                if (self.player.isJumping or self.player.isFalling or self.player.canFly()) and self.player.qinggongMgr.getDistanceFromGround() >= 1.0:
                    self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_FORWARD_DOWN)
        elif self.player.qinggongState == gametypes.QINGGONG_STATE_WINGFLY_DASH or self.needForceEndQingGong:
            self._wKeyTime = 0.0
            cellCmd.endUpQinggongState()

    def resetAimCrossPos(self, currentScrollNum):
        pass

    def restoreForwardKey(self):
        if not self._w and self.player.qinggongState in [gametypes.QINGGONG_STATE_FAST_SLIDING, gametypes.QINGGONG_STATE_FAST_SLIDING_WEAPON_IN_HAND, gametypes.QINGGONG_STATE_WINGFLY_DASH]:
            self._key_w_down(self._w)
        else:
            self.updateMoveControl()

    def _recalcSpeed(self):
        speedData = self.player.getSpeedData()
        self.setPhysicsFromModel(speedData)

    def recalcSpeed(self):
        self._recalcSpeed()
        self.player.updateActionKeyState()

    def isForbidRotateDCursor(self):
        p = BigWorld.player()
        if p.life == gametypes.LIFE_DEAD:
            return True
        if p.handClimb:
            return True
        if p.inForceNavigate:
            return True
        if getattr(p, 'inMeiHuo', False):
            return False
        if getattr(p, 'inFear', False):
            return False
        if getattr(p, 'inChaoFeng', False):
            return False
        if getattr(p, 'inDanDao', False):
            if getattr(p, 'danDaoUseDir', False):
                return False
        if p.fashion.doingActionType() == action.WA_BAO_ACTION:
            return True
        if p.isInApprenticeTrain() or p.isInApprenticeBeTrain():
            return True
        if p.coupleEmote:
            lockDC = CEBD.data.get(p.coupleEmote[0], {}).get('lockDC', None)
            if lockDC:
                return True
        if gameglobal.rds.ui.simpleQTE.lockCamera:
            return True
        if p._isOnZaijuOrBianyao():
            zNo = p._getZaijuOrBianyaoNo()
            if ZD.data.get(zNo, {}).get('lockTurnDir', None):
                return True
        return False

    def updateConfusionalMoveState(self):
        utils.recusionLog(4)
        if self.player.life == gametypes.LIFE_DEAD:
            return
        self.forceAllKeysUp()
        if self.player.lockHotKey:
            return
        _w = HK.HKM[HK.KEY_FORWARD].isAnyDown()
        _q = HK.HKM[HK.KEY_MOVELEFT].isAnyDown()
        _e = HK.HKM[HK.KEY_MOVERIGHT].isAnyDown()
        _s = HK.HKM[HK.KEY_BACKWARD].isAnyDown()
        _d = HK.HKM[HK.KEY_RIGHTTURN].isAnyDown()
        _a = HK.HKM[HK.KEY_LEFTTURN].isAnyDown()
        _ml = HK.HKM[keys.KEY_MOUSE0].isAnyDown()
        _mr = HK.HKM[keys.KEY_MOUSE1].isAnyDown()
        self._w = _w
        self._q = _q
        self._e = _e
        self._s = _s
        self._d = _d
        self._a = _a
        self._key_w_down(_w)
        self._key_q_down(_q)
        self._key_e_down(_e)
        self._key_s_down(_s)
        self._key_d_down(_d)
        if not gameglobal.rds.ui.isMouseInUI() and not self.player.circleEffect.isShowingEffect and self.player.getOperationMode() != gameglobal.ACTION_MODE:
            self._key_ml_down(_ml)
            self._key_mr_down(_mr)
        self.updateVelocity()

    def showJumpWaterEffect(self, position):
        sfx.attachEffect(gameglobal.ATTACH_EFFECT_NORMAL, (gameglobal.EFFECT_LOW,
         self.player.getBasicEffectPriority(),
         self.player.model,
         AvatarPhysics.WATERJUMPEFFECT,
         sfx.EFFECT_UNLIMIT,
         gameglobal.EFFECT_LAST_TIME,
         position))

    def motionClientPin(self):
        player = self.player
        player.fashion.breakJump()
        player.fashion.breakFall()
        player.fashion.stopAllActions()
        player.isAscending = False
        self.stopMove()
        self.forceAllKeysUp()

    def motionClientUnpin(self):
        player = self.player
        player.isAscending = False
        player.updateActionKeyState()

    def beginHandClimbNotifier(self, materialID, startPos, yaw, canAdsorb):
        if materialID == 141 and not canAdsorb:
            return False
        p = self.player
        p.physics.fall = False
        p.physics.followTarget = p.model.matrix
        p.cm.matchActionOnly = True
        p.am.enable = False
        p.model.footIK.enable = False
        if materialID == 140:
            p.model.position = (startPos.x, startPos.y, startPos.z)
            p.cm.setClimbMode('ladder')
            p.model.yaw = yaw
        elif materialID == 141:
            p.cm.setClimbMode('wall')
        p.ap.updateMoveControl()
        self.checkHandClimb()
        return True

    def endHandClimbNotifier(self, reason):
        p = self.player
        p.physics.fall = True
        p.physics.style = 0
        p.cm.matchActionOnly = False
        p.am.enable = True
        p.model.footIK.enable = True
        p.faceToDir(p.model.yaw)
        p.ap.updateMoveControl()

    def checkHandClimb(self):
        if self.player.handClimb:
            self._checkHandClimb()
            BigWorld.callback(0.2, self.checkHandClimb)

    def _checkHandClimb(self):
        p = self.player
        if p.handClimb:
            height = p.model.height + 0.6
            res = BigWorld.collide(p.spaceID, p.position + Math.Vector3(0, height, 0), p.position + Math.Vector3(math.sin(p.yaw) * 5, height, math.cos(p.yaw) * 5))
            if not res:
                p.cell.leaveHandClimb()

    def getTargetLockedEffectState(self):
        dist = (self.player.targetLocked.position - self.player.position).length
        rangeDist = SYSCD.data.get('targetLockedEffectRange', {}).get(self.player.school, 20)
        if dist < rangeDist:
            return AvatarPhysics.TARGET_LOCKED_STATE_IN
        else:
            return AvatarPhysics.TARGET_LOCKED_STATE_OUT

    def getTargetLockedEffect(self, state):
        if state == AvatarPhysics.TARGET_LOCKED_STATE_IN:
            return self.lockedEffInRange
        if state == AvatarPhysics.TARGET_LOCKED_STATE_OUT:
            return self.lockedEffOutRange

    def releaseTargetLockedEffect(self):
        self.targetLockEffectState = AvatarPhysics.TARGET_LOCKED_STATE_DEFAULT
        self.targetLockEffectUnit = None
        if self.targetLockConnector:
            self.targetLockConnector.release()
            self.targetLockConnector = None

    def getgetTargetLockStartNode(self):
        nodeName = SYSCD.data.get('targetLockedEffStartNodeName', 'Scene Root')
        node = None
        try:
            node = self.player.model.node(nodeName)
            if not node:
                node = self.player.model.node('Scene Root')
        except:
            pass

        return node

    def getTargetLockEndNode(self, target):
        if not target or not target.inWorld:
            return
        nodeName = SYSCD.data.get('targetLockedEffEndNodeName', 'Scene Root')
        node = None
        try:
            if hasattr(target, 'isInCoupleRide') and target.isInCoupleRide():
                if target.isInCoupleRideAsRider():
                    horse = target.getCoupleRideHorse()
                    if horse:
                        node = horse.modelServer.bodyModel.node(nodeName)
                else:
                    node = target.modelServer.bodyModel.node(nodeName)
            elif hasattr(target, 'isRidingTogether') and target.isRidingTogether():
                if target.isRidingTogetherAsMain():
                    node = target.modelServer.bodyModel.node(nodeName)
                else:
                    main = target.getRidingTogetherMain()
                    if main:
                        node = main.modelServer.bodyModel.node(nodeName)
            else:
                node = target.model.node(nodeName)
            if not node:
                node = target.model.node('Scene Root')
        except:
            pass

        return node

    def setTargetLockedEffect(self):
        p = self.player
        state = self.getTargetLockedEffectState()
        startNode = self.getgetTargetLockStartNode()
        endNode = self.getTargetLockEndNode(p.targetLocked)
        if not startNode or not endNode:
            gamelog.debug('m.l: targetLocked effect without node')
            self.releaseTargetLockedEffect()
            return
        if self.targetLockEffectState == AvatarPhysics.TARGET_LOCKED_STATE_DEFAULT:
            self.releaseTargetLockedEffect()
            self.targetLockEffectUnit = self.player.targetLocked
            eff = self.getTargetLockedEffect(state)
            if eff:
                self.targetLockConnector = sfx.attachEffect(gameglobal.ATTACH_CACHED_EFFECT_CONNECTOR, (p.getSkillEffectLv(),
                 startNode,
                 eff,
                 endNode,
                 80,
                 p.getSkillEffectPriority()))
            self.targetLockEffectState = state
        elif state != self.targetLockEffectState:
            self.releaseTargetLockedEffect()
            self.targetLockEffectUnit = self.player.targetLocked
            eff = self.getTargetLockedEffect(state)
            if eff:
                self.targetLockConnector = sfx.attachEffect(gameglobal.ATTACH_CACHED_EFFECT_CONNECTOR, (p.getSkillEffectLv(),
                 startNode,
                 eff,
                 endNode,
                 80,
                 p.getSkillEffectPriority()))
            self.targetLockEffectState = state

    def updateTargetLockedEffect(self):
        if not self.player or not self.player.inWorld:
            return
        target = self.player.targetLocked
        if not target or not target.inWorld:
            return
        if target == self.player:
            return
        if not gameglobal.ENABLE_TARGET_LOCKED_EFFECT:
            return
        if self.player.coupleEmote and target.id in self.player.coupleEmote:
            return
        if self.player.tride and target.id in self.player.tride:
            return
        if getattr(self.player, 'belongToRoundTable', False):
            return
        if getattr(self.player, 'interactiveObjectEntId', False):
            return
        className = target.__class__.__name__
        blackList = SYSCD.data.get('targetLockedEffBlackList', [])
        if className in blackList:
            return False
        if self.targetLockedCallback:
            BigWorld.cancelCallback(self.targetLockedCallback)
        if (target.position - self.player.position).length > 80:
            self.releaseTargetLockedEffect()
        else:
            if self.targetLockEffectUnit and self.targetLockEffectUnit != target:
                self.releaseTargetLockedEffect()
            self.setTargetLockedEffect()

    def cancelTargetLockedEffect(self):
        if self.targetLockedCallback:
            BigWorld.cancelCallback(self.targetLockedCallback)
        self.releaseTargetLockedEffect()

    def resetCameraAndDcursorRotate(self):
        pass
