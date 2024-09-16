#Embedded file name: I:/bag/tmp/tw2/res/entities\client\helpers/keyboardPhysics.o
import BigWorld
import C_ui
import utils
import gameglobal
import gametypes
import keys
import avatarPhysics
from guis import cursor
from guis import hotkey as HK
from cdata import game_msg_def_data as GMDD

class KeyboardPhysics(avatarPhysics.AvatarPhysics):

    def __init__(self):
        super(KeyboardPhysics, self).__init__()
        self.downTarget = None
        self._mlDowntime = 0
        self._mrDowntime = 0
        self.isDashing = False
        self.headTracking = False
        self.trackModel = None
        self.oldSeekPosition = None
        self.player = BigWorld.player()
        self.headTracking = False
        self.trackModel = None
        self.tracker = BigWorld.Tracker()
        self.entityDirProvider = BigWorld.EntityDirProvider(self.player, 1, 0)
        self.disableTracker = False

    def updateVelocity(self):
        vel = super(KeyboardPhysics, self).updateVelocity()
        if vel != None:
            if abs(vel.x) > 0.01:
                if not self.headTracking:
                    self.beginHeadTracker()
            elif self.headTracking:
                self.stopHeadTracker()

    def initTrackerNode(self):
        return
        if not self.player.firstFetchFinished:
            return
        if self.player.bsState:
            return
        playerModel = self.player.model
        if self.trackModel and self.trackModel != playerModel:
            self.trackModel.tracker = None
        self.trackModel = playerModel
        self.headNodeInfo = BigWorld.TrackerNodeInfo(playerModel, 'biped Head', [('biped Neck', -0.2), ('biped Spine', 0.5), ('biped Spine1', 0.4)], 'None', -0.0, 0.0, -40.0, 40.0, 3600.0)
        playerModel.tracker = self.tracker

    def beginHeadTracker(self):
        return
        if not self.player.firstFetchFinished:
            return
        if self.player.bsState:
            return
        if self.player.fashion.headTracking:
            return
        if self.disableTracker or not self.player.inCombat or self.player.bianshen[0] or self.player.weaponInHandState() or self.player.inSwim or self.player.inFly or self.player.life == gametypes.LIFE_DEAD or gameglobal.rds.isSinglePlayer:
            return
        if self.player.model != self.trackModel:
            self.initTrackerNode()
        self.tracker.directionProvider = self.entityDirProvider
        self.tracker.nodeInfo = self.headNodeInfo
        self.headTracking = True

    def stopHeadTracker(self):
        return None
        self.tracker.directionProvider = None
        self.tracker.nodeInfo = None
        self.headTracking = False

    def detachHeadTracker(self):
        return
        if self.trackModel != None:
            self.trackModel.tracker = None
            self.trackModel = None
            self.headTracking = False

    def reload(self):
        self.downKeyBindings = [([HK.HKM[HK.KEY_FORWARD]], self._key_w_down),
         ([HK.HKM[HK.KEY_BACKWARD]], self._key_s_down),
         ([HK.HKM[HK.KEY_RIGHTTURN]], self._key_d_down),
         ([HK.HKM[HK.KEY_LEFTTURN]], self._key_a_down),
         ([HK.HKM[HK.KEY_MOVELEFT]], self._key_q_down),
         ([HK.HKM[HK.KEY_MOVERIGHT]], self._key_e_down),
         ([HK.HKM[keys.KEY_MOUSE0]], self._key_ml_down),
         ([HK.HKM[keys.KEY_MOUSE1]], self._key_mr_down),
         ([HK.HKM[HK.KEY_RESETCAM]], self._key_mm_down),
         ([HK.HKM[keys.KEY_SPACE]], self._key_space_down),
         ([HK.HKM[HK.KEY_LEFT_DODGE]], self.leftDodge),
         ([HK.HKM[HK.KEY_RIGHT_DODGE]], self.rightDodge),
         ([HK.HKM[HK.KEY_FORWARD_DODGE]], self.forwardDodge),
         ([HK.HKM[HK.KEY_BACK_DODGE]], self.backDodge),
         ([HK.HKM[HK.KEY_UP_DODGE]], self.upDodge),
         ([HK.HKM[HK.KEY_DOWN_DODGE]], self.downDodge),
         ([HK.HKM[HK.KEY_DOWN]], self._key_x_down),
         ([HK.HKM[HK.KEY_WINGFLYUP]], self.landWingFlyUp),
         ([HK.HKM[HK.KEY_WING_SPRINT]], self.wingSlideSprint),
         ([HK.HKM[HK.KEY_LOCK_TARGETS_TARGET]], self.lockTargetsTarget)]
        self.keyBindings = keys.buildBindList(self.downKeyBindings)
        self.ccamera.isBindToDirCursor = True
        self.ccamera.canResetYaw = False

    def stopChasing(self):
        if self.isChasing:
            self.isChasing = False
            self.chasingEntity = None
            self.ccamera.allResetYaw = False
            self.forwardMagnitude = 0
        self.stopSeek()

    def intoForceMove(self):
        self.forceMoveCamera(self._msleft or self._msright)

    def leaveForceMove(self):
        if self._msright:
            self.ccamera.canResetCamera = True
        if self._msleft:
            self.ccamera.canResetCamera = False

    def forceMoveCamera(self, isDown):
        if isDown:
            if self._msleft or self._msright:
                if self.player.needLockCameraAndDc():
                    self.ccamera.canRotate = False
                else:
                    self.ccamera.canRotate = True
            else:
                self.ccamera.canRotate = False
            if not cursor.oldCursorPos:
                cursor.setOutAndSaveOldPos()
        elif not self._msleft and not self._msright:
            cursor.setInAndRestoreOldPos()
            self.ccamera.canRotate = False
        if getattr(self.player, 'inDanDao', False):
            if getattr(self.player, 'danDaoUseDir', False):
                self.dcursor.canRotate = True
                self.ccamera.canRotate = False

    def _key_ml_down(self, isDown):
        self._msleft = isDown
        if self.player.inForceMove:
            self.forceMoveCamera(isDown)
            return
        if isDown:
            BigWorld.player().circleEffect.clipCursorPos = BigWorld.getCursorPosInClip()
            if not self._msright:
                self._mlDowntime = BigWorld.time()
                isAltDown = self.isAltKeyDown()
                if isAltDown:
                    if self.checkLockMoveActionWing():
                        return
                    self.autoSeekPath()
                    return
                cursor.setOutAndSaveOldPos()
                self._mlDowntime = BigWorld.time()
        else:
            BigWorld.player().circleEffect.clipCursorPos = None
            if not self._msright:
                cursor.setInAndRestoreOldPos()
                BigWorld.target.reTarget()
                p = BigWorld.player()
                tg = BigWorld.time() - self._mlDowntime
                if tg < 0.2:
                    if p.target:
                        if not p.circleEffect.isShowingEffect:
                            p.lockTarget(p.target)
                    else:
                        self.getItemSelect(1)
                self._mlDowntime = 0
                result = BigWorld.getCursorPosInWorld(self.player.spaceID, 1000, False, (gameglobal.TREEMATTERKINDS, gameglobal.GLASSMATTERKINDS))
                if self.groupMapMarkCircle.isInGroupMapMarkStatus() and not gameglobal.rds.ui.isMouseInUI():
                    self.groupMapMarkCircle.markMapDone(result[0])
        self.moveControl('_msleft', isDown)
        p = BigWorld.player()
        if not isDown and p.circleEffect.isShowingEffect:
            skillInfo = p.getSkillInfo(p.skillId, p.skillLevel)
            if p.checkSkill(skillInfo):
                p.circleEffect.run()
        self.leftMouseFunction(isDown)

    def _key_mm_down(self, isDown):
        if isDown:
            self.ccamera.canResetYaw = True

    def _key_mr_down(self, isDown):
        if not self.player.rightMouseAble:
            return
        super(KeyboardPhysics, self)._key_mr_down(isDown)
        self._msright = isDown
        if self.player.inForceMove or self.player.inDaZuo():
            self.forceMoveCamera(isDown)
            return
        if self.player.fashion.headTracking:
            self.player.fashion.headCtrlStop()
        if self.player.isPathfinding or self.player.isLockYaw or self.player.inForceNavigate:
            self._msright = 0
            self._key_ml_down(isDown)
            return
        self.moveControl('_msright', isDown)
        if isDown:
            if not self._msleft:
                if self.player and self.player.target:
                    self.downTarget = self.player.target
                else:
                    self.setItemSelect()
                    self.downTarget = None
                cursor.setOutAndSaveOldPos()
                if self.player.clientControl:
                    self.stopChasing()
                self._mrDowntime = BigWorld.time()
            if self.isForbidRotateDCursor():
                self.ccamera.canResetCamera = False
            else:
                self.ccamera.canResetCamera = True
        elif not self._msleft:
            cursor.setInAndRestoreOldPos()
            BigWorld.target.reTarget()
            if self._mrDowntime != 0:
                tg = BigWorld.time() - self._mrDowntime
                if tg < 0.2:
                    if self.player.target and self.player.target.inWorld and self.downTarget == self.player.target:
                        if not utils.instanceof(self.player.target, 'DroppedItem') and self.player.targetLocked != self.player.target:
                            self.player.lockTarget(self.player.target)
                        self.player.startKeyModeFlow(self.player.target)
            self._mrDowntime = 0
        self.rightMouseFunction(isDown)

    def setItemSelect(self):
        pass

    def getItemSelect(self, ctype):
        pass

    def moveControl(self, desc, isDown):
        if not self.player.clientControl:
            return
        performAction = False
        turningAction = False
        if desc in ('_w', '_s') and self.isAutoMoving and isDown:
            self.stopAutoMove()
        if desc in ('_msleft', '_msright'):
            if self._msleft and self._msright:
                self._timeAutoMove()
            else:
                self._enterAutoMove()
        if desc == '_msleft' and self._msright or desc == '_msright' and self._msleft or desc == '_w':
            if self._w or self._msleft and self._msright:
                self._forward = True
                performAction = True
            else:
                self._forward = False
            self.moveForward(self._forward)
        if desc == '_s':
            if self._s:
                self._backward = True
                performAction = True
            else:
                self._backward = False
            self.moveBackward(self._backward)
        if desc == '_q' or desc == '_a' and self._msright or desc == '_msright' and self._a:
            if self._q or self._a and self._msright:
                self._moveleft = True
                performAction = True
            else:
                self._moveleft = False
            self.moveLeft(self._moveleft)
        if desc == '_e' or desc == '_d' and self._msright or desc == '_msright' and self._d:
            if self._e or self._d and self._msright:
                self._moveright = True
                performAction = True
            else:
                self._moveright = False
            self.moveRight(self._moveright)
        if desc not in ('_msleft', '_msright') or not self.player.inFly:
            self._combinationKey()
        if desc == '_a' or desc == '_d' or desc == '_msright':
            if self._a and not self._msright:
                self._turnleft = True
            else:
                self._turnleft = False
            if self._d and not self._msright:
                self._turnright = True
            else:
                self._turnright = False
            if self._turnright == self._turnleft:
                self._turnright = self._turnleft = False
                self.turnLeft(False)
            elif self._turnleft:
                self.turnLeft(self._turnleft)
                turningAction = self._turnleft
            elif self._turnright:
                self.turnRight(self._turnright)
                turningAction = self._turnright
        if self._msleft and not self._msright:
            if self.player.needLockCameraAndDc():
                self.ccamera.canRotate = False
            else:
                self.ccamera.canRotate = True
        else:
            self.ccamera.canRotate = False
        if self._msright:
            if self.isForbidRotateDCursor():
                self.ccamera.canRotate = True
                self.dcursor.canRotate = False
            elif self.player.needLockCameraAndDc():
                self.dcursor.canRotate = False
            else:
                self.dcursor.canRotate = True
        else:
            self.dcursor.canRotate = False
        if performAction and (self.player.isPathfinding or self.player.physics.seeking):
            if not (getattr(self.player, 'inChaoFeng', False) or getattr(self.player, 'inMeiHuo', False)):
                self.stopChasing()
        elif turningAction and (self.player.isPathfinding or self.player.physics.seeking):
            if not (getattr(self.player, 'inChaoFeng', False) or getattr(self.player, 'inMeiHuo', False)):
                self.stopChasing()
        super(KeyboardPhysics, self).moveControl(desc, isDown)

    def isMovingActionKeyControl(self):
        l = (self._s,
         self._w,
         self._q,
         self._e,
         self._msleft and self._msright,
         self._d and self._msright,
         self._a and self._msright,
         self._a and self._msleft,
         self._d and self._msleft,
         self.isAutoMoving)
        for k in l:
            if k:
                return True

        return False

    def restoreJumpState(self, collide = False, afterBigJump = False):
        super(KeyboardPhysics, self).restoreJumpState(collide, afterBigJump)
        if not self._w and not (self._msright and self._msleft):
            self.player.isDashing = False
            self.player.isRunning = True
            self.forwardMagnitude = 0

    def forceAllKeysUp(self):
        super(KeyboardPhysics, self).forceAllKeysUp()
        self._mlDowntime = 0
        self._mrDowntime = 0
        self.downTarget = None

    def _doJump(self):
        super(KeyboardPhysics, self)._doJump()

    def afterJumpEnd(self, collide = False, afterBigJump = False):
        super(KeyboardPhysics, self).afterJumpEnd(collide, afterBigJump)

    def stopMoveExceptAuto(self):
        self.forwardMagnitude = 0
        self.backwardMagnitude = 0
        self.leftwardMagnitude = 0
        self.rightwardMagnitude = 0
        dc = BigWorld.dcursor()
        dc.deltaYaw = 0
        self.isChasing = False
        self.chasingEntity = None
        self.ccamera.allResetYaw = False
        self.updateVelocity()

    def isAltKeyDown(self):
        return BigWorld.getKeyDownState(keys.KEY_RALT, 0) or BigWorld.getKeyDownState(keys.KEY_LALT, 0)

    def autoSeekPath(self):
        if self.player.qinggongState != gametypes.QINGGONG_STATE_DEFAULT:
            return
        if self.player.isForceMove:
            return
        result = BigWorld.getCursorPosInWorld(self.player.spaceID, 1000, False, (gameglobal.TREEMATTERKINDS, gameglobal.GLASSMATTERKINDS))
        vehicleID = 0
        if result[0] != None and self.oldSeekPosition != result[0]:
            if self.player.stateMachine.checkMove():
                self.oldSeekPosition = result[0]
                self.seekPath(result[0], self._autoSeekApproach, vehicleID)
                self.navigation.start(result[0], result[3] == 256, vehicleID, False)

    def _autoSeekApproach(self, success):
        self.forwardMagnitude = 0
        self.navigation.stop()

    def resetControl(self):
        if not self.isChasing:
            if self._w or self._msleft and self._msright or self.isAutoMoving:
                self._forward = True
            else:
                self._forward = False
            self.moveForward(self._forward)
            if self._s:
                self._backward = True
            else:
                self._backward = False
            self.moveBackward(self._backward)
            if self._space:
                self._moveUp = True
            else:
                self._moveUp = False
            if self._x:
                self._moveDown = True
            else:
                self._moveDown = False
            self.moveUp(self._moveUp, self._moveDown)
            if self._q or self._a and self._msright:
                self._moveleft = True
            else:
                self._moveleft = False
            self.moveLeft(self._moveleft)
            if self._e or self._d and self._msright:
                self._moveright = True
            else:
                self._moveright = False
            self.moveRight(self._moveright)
            if self._a and not self._msright:
                self._turnleft = True
            else:
                self._turnleft = False
            if self._d and not self._msright:
                self._turnright = True
            else:
                self._turnright = False
            if self._turnright == self._turnleft:
                self._turnright = self._turnleft = False
                self.turnLeft(False)
            elif self._turnleft:
                self.turnLeft(self._turnleft)
            elif self._turnright:
                self.turnRight(self._turnright)
            self._leftForward = self._moveleft and self._forward
            self._rightForward = self._moveright and self._forward
            self._leftBackward = self._moveleft and self._backward
            self._rightBackward = self._moveright and self._backward
            self.moveLeftForward(self._leftForward)
            self.moveRightForward(self._rightForward)
            self.moveLeftBackward(self._leftBackward)
            self.moveRightBackward(self._rightBackward)
        if self._msleft and not self._msright:
            if self.player.needLockCameraAndDc():
                self.ccamera.canRotate = False
            else:
                self.ccamera.canRotate = True
        else:
            self.ccamera.canRotate = False
        if self._msright:
            if self.isForbidRotateDCursor():
                self.ccamera.canRotate = True
                self.dcursor.canRotate = False
            elif self.player.needLockCameraAndDc():
                self.dcursor.canRotate = False
            else:
                self.dcursor.canRotate = True
        else:
            self.dcursor.canRotate = False
        self.updateVelocity()
        if self.player.canFly() and not self.player.lockHotKey and self.isAnyDirKeyDown():
            self.moveVerticalWard()

    def updateMoveControl(self):
        if self.player.confusionalState:
            self.updateConfusionalMoveState()
            return
        if self.player.life == gametypes.LIFE_DEAD:
            return
        self.forceAllKeysUp()
        if self.player.lockHotKey:
            return
        _w = HK.HKM[HK.KEY_FORWARD].isAnyDown() or HK.HKM[HK.KEY_FORWARD_DODGE].isAnyDown()
        _q = HK.HKM[HK.KEY_MOVELEFT].isAnyDown() or HK.HKM[HK.KEY_LEFT_DODGE].isAnyDown()
        _e = HK.HKM[HK.KEY_MOVERIGHT].isAnyDown() or HK.HKM[HK.KEY_RIGHT_DODGE].isAnyDown()
        _s = HK.HKM[HK.KEY_BACKWARD].isAnyDown() or HK.HKM[HK.KEY_BACK_DODGE].isAnyDown()
        _d = HK.HKM[HK.KEY_RIGHTTURN].isAnyDown()
        _a = HK.HKM[HK.KEY_LEFTTURN].isAnyDown()
        _ml = HK.HKM[keys.KEY_MOUSE0].isAnyDown()
        _mr = HK.HKM[keys.KEY_MOUSE1].isAnyDown()
        _space = HK.HKM[keys.KEY_SPACE].isAnyDown() or HK.HKM[HK.KEY_UP_DODGE].isAnyDown()
        _x = HK.HKM[HK.KEY_DOWN].isAnyDown() or HK.HKM[HK.KEY_DOWN_DODGE].isAnyDown()
        self._w = _w
        self._q = _q
        self._e = _e
        self._s = _s
        self._d = _d
        self._a = _a
        self._space = _space
        self._x = _x
        if not gameglobal.rds.ui.isMouseInUI() and not self.player.circleEffect.isShowingEffect:
            self._msleft = _ml
            self._msright = _mr
        if self.player.isPathfinding or self.player.isLockYaw:
            self._msleft = self._msright
            self._msright = 0
        self.resetControl()

    def forwardDodge(self, isDown):
        if not self.player.checkTempGroupFollow():
            return
        super(KeyboardPhysics, self).forwardDodge(isDown)
        if isDown:
            self._w = isDown
            self._qKeyTime = 0.0
            self._eKeyTime = 0.0
            self._sKeyTime = 0.0
            self._xKeyTime = 0.0
            self._spaceKeyTime = 0.0
            self.realKeyUpTime = 0.0
            self.moveControl('_w', isDown)
        else:
            self.updateMoveControl()
