#Embedded file name: /WORKSPACE/data/entities/client/helpers/mousephysics.o
import time
import BigWorld
import C_ui
import gameglobal
import gametypes
import const
import keys
import avatarPhysics
import action
import gamelog
import formula
from guis import cursor
from guis import hotkey as HK
from helpers import qingGong
from helpers import cellCmd
from cdata import game_msg_def_data as GMDD

class MousePhysics(avatarPhysics.AvatarPhysics):
    VALUE_PI = 3.1415926

    def __init__(self):
        super(MousePhysics, self).__init__()
        self.downTarget = None
        self._mrDowntime = 0.0
        self._mlDowntime = 0.0
        self.keyDownTimes = {'_w': 0.0,
         '_s': 0.0,
         '_a': 0.0,
         '_d': 0.0}
        self.oldSeekPosition = None
        self.isAutoTurnYaw = False
        self.freeRotateCam = False

    def updateVelocity(self):
        super(MousePhysics, self).updateVelocity()

    def beginChase(self, entity, desiredDist):
        gamelog.debug('beginChase:', entity.id)
        self.isChasing = True
        self.isAutoMoving = False
        self.chasingEntity = entity
        self.ccamera.canResetYaw = False
        self.ccamera.allResetYaw = False
        self.chaseEntity(entity, desiredDist)
        self.updateVelocity()

    def reload(self):
        self.downKeyBindings = [([HK.HKM[HK.KEY_FORWARD]], self._key_w_down),
         ([HK.HKM[HK.KEY_BACKWARD]], self._key_s_down),
         ([HK.HKM[HK.KEY_MOVELEFT]], self._key_a_down),
         ([HK.HKM[HK.KEY_MOVERIGHT]], self._key_d_down),
         ([HK.HKM[keys.KEY_MOUSE0]], self.leftMouseFunction),
         ([HK.HKM[keys.KEY_MOUSE1]], self._key_mr_down),
         ([HK.HKM[keys.KEY_SPACE]], self._key_space_down),
         ([HK.HKM[HK.KEY_DOWN]], self._key_x_down),
         ([HK.HKM[HK.KEY_LEFT_DODGE]], self.leftDodge),
         ([HK.HKM[HK.KEY_RIGHT_DODGE]], self.rightDodge),
         ([HK.HKM[HK.KEY_FORWARD_DODGE]], self.forwardDodge),
         ([HK.HKM[HK.KEY_BACK_DODGE]], self.backDodge),
         ([HK.HKM[HK.KEY_UP_DODGE]], self.upDodge),
         ([HK.HKM[HK.KEY_DOWN_DODGE]], self.downDodge),
         ([HK.HKM[HK.KEY_WINGFLYUP]], self.landWingFlyUp),
         ([HK.HKM[HK.KEY_WING_SPRINT]], self.wingSlideSprint),
         ([HK.HKM[HK.KEY_RESUME_FREE_ROTATE]], self.freeRotate),
         ([HK.HKM[HK.KEY_LEAVE_LOCK_ROTATE]], self.lockRotate),
         ([HK.HKM[HK.KEY_LOCK_TARGETS_TARGET]], self.lockTargetsTarget)]
        self.keyBindings = keys.buildBindList(self.downKeyBindings)
        self.ccamera.isBindToDirCursor = True
        self.ccamera.canResetYaw = False

    def stopChasing(self):
        gamelog.debug('stopChasing')
        if self.isChasing:
            self.isChasing = False
            self.chasingEntity = None
            self.ccamera.allResetYaw = False
            self.forwardMagnitude = 0
        self.stopSeek()

    def __realMove(self, isDown, desc):
        if isDown:
            self.stopAutoMove()
            if self.player.qinggongState == gametypes.QINGGONG_STATE_FAST_DOWN:
                return
            if self.keyDownTimes[desc]:
                if BigWorld.time() - self.keyDownTimes[desc] <= gameglobal.DOUBLE_CLICK_INTERVAL:
                    self.keyDownTimes[desc] = 0.0
                    if self.player.canFly():
                        self.needForceEndQingGong = True
                        self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_WINGFLY_DASH)
                    elif self.player.qinggongMgr.state in (qingGong.STATE_DASH_TWICE_JUMPING,
                     qingGong.STATE_JUMPING,
                     qingGong.STATE_DASH_JUMPING,
                     qingGong.STATE_DASH_BIG_JUMPING,
                     qingGong.STATE_RUSH_DOWN,
                     qingGong.STATE_RUSH_DOWN_WEAPON_IN_HAND,
                     qingGong.STATE_TWICE_JUMPING) or self.player.isFalling:
                        if (self.player.isJumping or self.player.isFalling or self.player.canFly()) and self.player.qinggongMgr.getDistanceFromGround() >= 1.0:
                            if BigWorld.player().weaponInHandState():
                                self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_WEAPON_FORWARD_DOWN)
                            elif BigWorld.player().equipment[gametypes.EQU_PART_WINGFLY]:
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
                            epRegen = delta * timeInterval
                        preMin1, preMax1, fstCost1, _ = qingGong.getQinggongData(gametypes.QINGGONG_ROLL_FORWARD)
                        qinggongState = self.player.inRiding() and gametypes.QINGGONG_STATE_MOUNT_DASH or gametypes.QINGGONG_STATE_FAST_RUN
                        preMin2, preMax2, fstCost2, _ = qingGong.getQinggongData(qinggongState)
                        if (self.player.ep + epRegen < preMax1 or preMax1 == 0) and self.player.ep + epRegen >= preMin1 and self.player.inCombat:
                            if desc == '_w':
                                self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_FORWARD_DOWN)
                            elif desc == '_s':
                                self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_BACK_DOWN)
                            elif desc == '_a':
                                self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_LEFT_DOWN)
                            elif desc == '_d':
                                self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_RIGHT_DOWN)
                            self.moveControl(desc, isDown)
                            return
                        if self.player.ep + epRegen >= preMin2:
                            if not self.player.isDashing:
                                qingGong.switchToDash(self.player)
                        elif not formula.inDotaBattleField(getattr(self.player, 'mapID', 0)):
                            self.player.showGameMsg(GMDD.data.QINGGONG_NOT_ENOUGH, ())
                else:
                    self.keyDownTimes[desc] = BigWorld.time()
            else:
                self.keyDownTimes[desc] = BigWorld.time()
        elif not self.isKeyBoardMove() or self.player.isDashing:
            if self.player.qinggongState in (gametypes.QINGGONG_STATE_FAST_SLIDING, gametypes.QINGGONG_STATE_FAST_SLIDING_WEAPON_IN_HAND):
                self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_FORWARD_UP)
            elif self.player.isDashing:
                if not self.isAnyDirKeyDown():
                    self.switchToRun(True)
            elif self.player.qinggongState == gametypes.QINGGONG_STATE_WINGFLY_DASH or self.needForceEndQingGong:
                cellCmd.endUpQinggongState()
        self.moveControl(desc, isDown)

    def forceMoveCamera(self, isDown):
        if isDown:
            if self._msright:
                if self.player.needLockCameraAndDc():
                    self.ccamera.canRotate = False
                else:
                    self.ccamera.canRotate = True
            else:
                self.ccamera.canRotate = False
            cursor.setOutAndSaveOldPos()
        elif not self._msright:
            cursor.setInAndRestoreOldPos()
            self.ccamera.canRotate = False
        if getattr(self.player, 'inDanDao', False):
            if getattr(self.player, 'danDaoUseDir', False):
                self.dcursor.canRotate = True
                self.ccamera.canRotate = False

    def leaveForceMove(self):
        if self._msright:
            self.ccamera.canResetCamera = False

    def setYaw(self, yaw, forbidCamRotate = False):
        if self.player.needLockCameraAndDc():
            return
        super(self.__class__, self).setYaw(yaw, forbidCamRotate=False)

    def _key_w_down(self, isDown):
        if self.player.inPUBGPlane():
            return
        if not self.player.checkTempGroupFollow():
            return
        self._w = isDown
        if isDown:
            self.keyDownTimes['_s'] = 0.0
            self.keyDownTimes['_a'] = 0.0
            self.keyDownTimes['_d'] = 0.0
            if self.player.stateMachine.checkSetYaw() and not self.player.forbidChangeYaw():
                if self._s:
                    self._s = False
                if self._a:
                    self.setYaw(self.ccamera.direction.yaw - MousePhysics.VALUE_PI / 4)
                elif self._d:
                    self.setYaw(self.ccamera.direction.yaw + MousePhysics.VALUE_PI / 4)
                else:
                    self.setYaw(self.ccamera.direction.yaw)
        self.__realMove(self._w, '_w')
        if not isDown:
            self.updateKeyState('_w')

    def _key_a_down(self, isDown):
        if self.player.inPUBGPlane():
            return
        if not self.player.checkTempGroupFollow():
            return
        if self.player.handClimb:
            return
        if self.player.inSimpleQte and isDown:
            gameglobal.rds.ui.simpleQTE.handleInputKey(gameglobal.QTE_KEY_A)
            return
        self._a = isDown
        if isDown:
            self.keyDownTimes['_s'] = 0.0
            self.keyDownTimes['_w'] = 0.0
            self.keyDownTimes['_d'] = 0.0
            if self.player.stateMachine.checkSetYaw() and not self.player.forbidChangeYaw():
                if self._d:
                    self._d = False
                if self._w:
                    self.setYaw(self.ccamera.direction.yaw - MousePhysics.VALUE_PI / 4)
                elif self._s:
                    self.setYaw(self.ccamera.direction.yaw - 3 * MousePhysics.VALUE_PI / 4)
                else:
                    self.setYaw(self.ccamera.direction.yaw - MousePhysics.VALUE_PI / 2)
        self.__realMove(self._a, '_a')
        if not isDown:
            self.updateKeyState('_a')

    def _key_d_down(self, isDown):
        if self.player.inPUBGPlane():
            return
        if not self.player.checkTempGroupFollow():
            return
        if self.player.handClimb:
            return
        if self.player.inSimpleQte and isDown:
            gameglobal.rds.ui.simpleQTE.handleInputKey(gameglobal.QTE_KEY_D)
            return
        self._d = isDown
        if isDown:
            self.keyDownTimes['_s'] = 0.0
            self.keyDownTimes['_a'] = 0.0
            self.keyDownTimes['_w'] = 0.0
            if self.player.stateMachine.checkSetYaw() and not self.player.forbidChangeYaw():
                if self._a:
                    self._a = False
                if self._s:
                    self.setYaw(self.ccamera.direction.yaw + 3 * MousePhysics.VALUE_PI / 4)
                elif self._w:
                    self.setYaw(self.ccamera.direction.yaw + MousePhysics.VALUE_PI / 4)
                else:
                    self.setYaw(self.ccamera.direction.yaw + MousePhysics.VALUE_PI / 2)
        self.__realMove(self._d, '_d')
        if not isDown:
            self.updateKeyState('_d')

    def _key_s_down(self, isDown):
        if self.player.inPUBGPlane():
            return
        if not self.player.checkTempGroupFollow():
            return
        self._s = isDown
        if isDown:
            self.keyDownTimes['_w'] = 0.0
            self.keyDownTimes['_a'] = 0.0
            self.keyDownTimes['_d'] = 0.0
            if self.player.stateMachine.checkSetYaw() and not self.player.forbidChangeYaw():
                if self._w:
                    self._w = False
                if self._a:
                    self.setYaw(self.ccamera.direction.yaw - 3 * MousePhysics.VALUE_PI / 4)
                elif self._d:
                    self.setYaw(self.ccamera.direction.yaw + 3 * MousePhysics.VALUE_PI / 4)
                else:
                    self.setYaw(self.ccamera.direction.yaw + MousePhysics.VALUE_PI)
        self.__realMove(self._s, '_s')
        if not isDown:
            self.updateKeyState('_s')

    def _key_x_down(self, isDown):
        if self.player.inPUBGPlane():
            return
        if not self.player.checkTempGroupFollow():
            return
        self._x = isDown
        if isDown:
            self._qKeyTime = 0.0
            self._wKeyTime = 0.0
            self._sKeyTime = 0.0
            self._eKeyTime = 0.0
            self._spaceKeyTime = 0.0
            self.stopSeek()
            if self.player.qinggongState in [gametypes.QINGGONG_STATE_SLIDING, gametypes.QINGGONG_STATE_FAST_SLIDING, gametypes.QINGGONG_STATE_FAST_SLIDING_WEAPON_IN_HAND]:
                self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_S_DOWN)
            elif self.player.canFly():
                if self._xKeyTime:
                    if BigWorld.time() - self._xKeyTime <= gameglobal.DOUBLE_CLICK_INTERVAL:
                        self._xKeyTime = 0.0
                        self.player.qinggongMgr.doFuncByEvent(qingGong.EVENT_WINGFLY_DOWN)
                    else:
                        self._xKeyTime = BigWorld.time()
                else:
                    self._xKeyTime = BigWorld.time()
                self.flyDown(isDown)
        elif self.player.canFly():
            self.flyDown(isDown)

    def updateKeyState(self, desc):
        if gameglobal.rds.ui.bInEdit:
            return
        if desc == '_s':
            if HK.HKM[HK.KEY_FORWARD].isAnyDown():
                self.keyDownTimes['_w'] = 0.0
                self._key_w_down(True)
            elif HK.HKM[HK.KEY_MOVELEFT].isAnyDown():
                self.keyDownTimes['_a'] = 0.0
                self._key_a_down(True)
            elif HK.HKM[HK.KEY_MOVERIGHT].isAnyDown():
                self.keyDownTimes['_d'] = 0.0
                self._key_d_down(True)
        elif desc == '_w':
            if HK.HKM[HK.KEY_BACKWARD].isAnyDown():
                self.keyDownTimes['_s'] = 0.0
                self._key_s_down(True)
            elif HK.HKM[HK.KEY_MOVELEFT].isAnyDown():
                self.keyDownTimes['_a'] = 0.0
                self._key_a_down(True)
            elif HK.HKM[HK.KEY_MOVERIGHT].isAnyDown():
                self.keyDownTimes['_d'] = 0.0
                self._key_d_down(True)
        elif desc == '_a':
            if HK.HKM[HK.KEY_BACKWARD].isAnyDown():
                self.keyDownTimes['_s'] = 0.0
                self._key_s_down(True)
            elif HK.HKM[HK.KEY_FORWARD].isAnyDown():
                self.keyDownTimes['_w'] = 0.0
                self._key_w_down(True)
            elif HK.HKM[HK.KEY_MOVERIGHT].isAnyDown():
                self.keyDownTimes['_d'] = 0.0
                self._key_d_down(True)
        elif desc == '_d':
            if HK.HKM[HK.KEY_BACKWARD].isAnyDown():
                self.keyDownTimes['_s'] = 0.0
                self._key_s_down(True)
            elif HK.HKM[HK.KEY_MOVELEFT].isAnyDown():
                self.keyDownTimes['_a'] = 0.0
                self._key_a_down(True)
            elif HK.HKM[HK.KEY_FORWARD].isAnyDown():
                self.keyDownTimes['_w'] = 0.0
                self._key_w_down(True)

    def startAutoMove(self):
        if self.player.stateMachine.checkMove() and self.player.stateMachine.checkStatus(const.CT_AUTO_MOVE):
            self.isAutoMoving = True
            if self.navigation.isShowingEffect:
                self.stopSeek()
            self.updateMousePosition(True)

    def stopAutoMove(self):
        if self.isAutoMoving:
            self.isAutoMoving = False
            self.stopMove()
            if self.navigation.isShowingEffect:
                self.navigation.stop()
                self.oldSeekPosition = None

    def leftMouseFunction(self, isDown):
        if self.player.inPUBGPlane():
            return
        if not self.player.checkTempGroupFollow():
            return
        self._msleft = isDown
        if self.player.inForceMove:
            return
        if self.checkLockMoveActionWing():
            return
        super(MousePhysics, self).leftMouseFunction(isDown)
        p = BigWorld.player()
        if isDown:
            gamelog.debug('leftMouseFunction')
            if self.groupMapMarkCircle.isInGroupMapMarkStatus():
                return
            if self.isChasing and not self.player.target:
                self.clearChaseData()
                self.updateVelocity()
            if not p.circleEffect.isShowingEffect:
                if p.isGuiding and p.isGuiding == const.GUIDE_TYPE_NO_MOVE:
                    self.isAutoTurnYaw = True
                    self.updateYawByMouse()
                elif self._msleft and not self._msright:
                    self._timeAutoMove()
                    self.updateMousePosition(True)
                    if BigWorld.isKeyDown(keys.KEY_LSHIFT) or BigWorld.isKeyDown(keys.KEY_RSHIFT):
                        self.leftMouseDodge(isDown)
        else:
            if self.navigation.isShowingEffect and not self._enterAutoMove():
                self.navigation.stopUpdateEffect()
            if self.isKeyBoardMove():
                self.navigation.stop()
            if p.circleEffect.isShowingEffect:
                p = BigWorld.player()
                skillInfo = BigWorld.player().getSkillInfo(p.skillId, p.skillLevel)
                if p.checkSkill(skillInfo):
                    p.circleEffect.run()
            elif self.isAutoTurnYaw:
                self.isAutoTurnYaw = False
            result = BigWorld.getCursorPosInWorld(self.player.spaceID, 1000, False, (gameglobal.TREEMATTERKINDS, gameglobal.GLASSMATTERKINDS))
            if self.groupMapMarkCircle.isInGroupMapMarkStatus() and not gameglobal.rds.ui.isMouseInUI():
                self.groupMapMarkCircle.markMapDone(result[0])

    def updateMousePosition(self, needUpdate = False):
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
            if result[0] != None and not process and self.oldSeekPosition != result[0]:
                if not self.player.spellingType and not self.player.isForceMove:
                    if self.player.stateMachine.checkMove():
                        if not self.isKeyBoardMove():
                            self.oldSeekPosition = result[0]
                            self.seekPath(result[0], None, vehicleID)
                            self.destination = result[0]
                        self.navigation.start(result[0], result[3] == 256, vehicleID, needUpdate)
                    elif self.player.isGuiding and not self.player.skillPlayer.targetPos:
                        direction = result[0] - self.player.position
                        self.setYaw(direction.yaw)

    def _approach(self, success):
        super(MousePhysics, self)._approach(success)
        if success == 1 and (self.player.qinggongState in gametypes.QINGGONG_STATE_DASH_SET or self.player.isDashing):
            cellCmd.endUpQinggongState()

    def continueSeekPath(self):
        if self.oldSeekPosition:
            self.seekPath(self.oldSeekPosition, None, 0)
            self.navigation.stop()
            self.navigation.start(self.oldSeekPosition, False, 0, False)
            self.navigation.stopUpdateEffect()

    def isKeyBoardMove(self):
        return self._w or self._s or self._a or self._d or self.player.canFly() and (self._x or self._space)

    def _key_ml_down(self, isDown):
        pass

    def _key_mr_down(self, isDown):
        if not self.player.rightMouseAble:
            return
        super(MousePhysics, self)._key_mr_down(isDown)
        self._msright = isDown
        if self.player.inForceMove or self.player.inDaZuo():
            self.forceMoveCamera(isDown)
            return
        if self.isAutoTurnYaw and self.player.isGuiding:
            return
        if isDown:
            if not self._msleft and not self.isAutoMoving:
                cursor.setOutAndSaveOldPos()
                self._mrDowntime = BigWorld.time()
        else:
            if not self._msright:
                cursor.setInAndRestoreOldPos()
                BigWorld.target.reTarget()
                p = BigWorld.player()
                tg = BigWorld.time() - self._mrDowntime
                if tg < 0.2:
                    if p.target and p.target.inWorld:
                        if not p.circleEffect.isShowingEffect:
                            p.lockTarget(p.target)
                            p.startMouseModeFlow(p.target)
                    else:
                        self.getItemSelect(1)
                self._mrDowntime = 0
            p.circleEffect.cancel()
        self.moveControl('_msright', isDown)

    def setItemSelect(self):
        pass

    def getItemSelect(self, ctype):
        pass

    def _doJump(self):
        super(MousePhysics, self)._doJump()

    def afterJumpEnd(self, collide = False, afterBigJump = False):
        super(MousePhysics, self).afterJumpEnd(collide, afterBigJump)

    def moveControl(self, desc, isDown):
        gamelog.debug('bgf:moveControl', desc, isDown, self._msright, self._msleft)
        if not self.player.clientControl:
            return
        performAction = False
        turningAction = False
        if self._msright and not self._msleft and not self.isAutoMoving:
            if (self.isKeyBoardMove() or self.player.isDashing and not self.player.isPathfinding) and self.player.life == gametypes.LIFE_ALIVE:
                if self.player.needLockCameraAndDc():
                    self.dcursor.canRotate = False
                else:
                    self.dcursor.canRotate = True
                    self.ccamera.canRotate = False
            else:
                self.ccamera.canRotate = True
                self.dcursor.canRotate = False
        else:
            self.dcursor.canRotate = False
            self.ccamera.canRotate = False
        gamelog.debug('dcursor, camera', self.dcursor.canRotate, self.ccamera.canRotate)
        if desc in ('_w', '_s', '_a', '_d'):
            if self._w or self._s or self._a or self._d:
                self._forward = True
                performAction = True
            else:
                self._forward = False
        if performAction:
            self.stopChasing()
        elif turningAction:
            self.stopChasing()
        if desc != '_msright':
            self.moveForward(self._forward)
        if self.isMovingActionKeyControl():
            actType = self.player.fashion.doingActionType()
            gamelog.debug('moveForward:isStopActionKeyControl', self._forward, desc, actType)
            if actType in [action.MOVINGSTOP_ACTION, action.AFTERMOVESTOP_ACTION, action.ROLLSTOP_ACTION]:
                self.player.fashion.movingNotifier(True)
        super(MousePhysics, self).moveControl(desc, isDown)

    def isMovingActionKeyControl(self):
        l = (self._s,
         self._w,
         self._a,
         self._d,
         self.isAutoMoving,
         self.physics.seeking)
        for k in l:
            if k:
                return True

        return False

    def updateMoveControl(self):
        if self.player.life == gametypes.LIFE_DEAD:
            return
        self.forceAllKeysUp()
        self._w = HK.HKM[HK.KEY_FORWARD].isAnyDown()
        self._a = HK.HKM[HK.KEY_MOVELEFT].isAnyDown()
        self._d = HK.HKM[HK.KEY_MOVERIGHT].isAnyDown()
        self._s = HK.HKM[HK.KEY_BACKWARD].isAnyDown()
        self._msleft = HK.HKM[keys.KEY_MOUSE0].isAnyDown()
        self._msright = HK.HKM[keys.KEY_MOUSE1].isAnyDown()
        if self._w and self._s:
            self._s = False
        if self._a and self._d:
            self._d = False
        l = (self._w,
         self._a,
         self._s,
         self._d)
        angle = (0,
         -self.VALUE_PI / 2,
         self.VALUE_PI,
         self.VALUE_PI / 2)
        dirYaw = 0
        num = 0
        for i in xrange(0, 4):
            if l[i]:
                dirYaw += angle[i]
                num += 1

        if num:
            dirYaw = dirYaw / num + self.ccamera.direction.yaw
            if self._a and self._s:
                dirYaw = -self.VALUE_PI + dirYaw
            if self.player.stateMachine.checkSetYaw():
                self.setYaw(dirYaw)
        self.moveControl('_w', self._w)
        self.moveControl('_a', self._a)
        self.moveControl('_s', self._s)
        self.moveControl('_d', self._d)
        self.updateVelocity()

    def resetControl(self):
        pass

    def updateYawByMouse(self):
        if not self.isAutoTurnYaw or not self.player.isGuiding:
            return
        result = BigWorld.getCursorPosInWorld(self.player.spaceID, 1000, False, (gameglobal.TREEMATTERKINDS, gameglobal.GLASSMATTERKINDS))
        if result[0] != None:
            direction = result[0] - self.player.position
            self.setYaw(direction.yaw)
            BigWorld.callback(0.1, self.updateYawByMouse)

    def restoreJumpState(self, collide = False, afterBigJump = False):
        gamelog.debug('restoreJumpState')
        if not self._w and not self._a and not self._d and not self._s:
            self.player.isDashing = False
            self.player.isRunning = True
            self.forwardMagnitude = 0
        super(MousePhysics, self).restoreJumpState(collide, afterBigJump)
        if not self.isAutoMoving and self.oldSeekPosition and self.navigation.isShowingEffect:
            BigWorld.callback(0, self.continueSeekPath)

    def resetCameraPitchRange(self):
        super(MousePhysics, self).resetCameraPitchRange()
        gameglobal.rds.cam.setScrollRange()

    def freeRotate(self, isDown):
        if isDown:
            self.freeRotateCam = True
            gameglobal.rds.cam.resetDcursorPitch()

    def lockRotate(self, isDown):
        self.freeRotateCam = False
        gameglobal.rds.cam.mouseModePitch = BigWorld.dcursor().pitch
        gameglobal.rds.cam.resetDcursorPitch()

    def dodgeToRun(self):
        if self.player.qinggongState in gametypes.QINGGONG_STATE_DASH_SET or self.player.isDashing:
            cellCmd.endUpQinggongState()
            self.switchToRun()

    def endDash(self):
        if self.player.qinggongState in gametypes.QINGGONG_STATE_DASH_SET or self.player.isDashing:
            cellCmd.endUpQinggongState()

    def forwardDodge(self, isDown):
        if not self.player.checkTempGroupFollow():
            return
        super(MousePhysics, self).forwardDodge(isDown)
        if not isDown:
            self._key_w_down(isDown)
            self.dodgeToRun()

    def leftDodge(self, isDown):
        if not self.player.checkTempGroupFollow():
            return
        super(MousePhysics, self).leftDodge(isDown)
        if not isDown:
            self._key_a_down(isDown)
            if self.player.qinggongState in gametypes.QINGGONG_STATE_DASH_SET or self.player.isDashing:
                cellCmd.endUpQinggongState()
                self.forwardMagnitude = 0

    def rightDodge(self, isDown):
        if not self.player.checkTempGroupFollow():
            return
        super(MousePhysics, self).rightDodge(isDown)
        if not isDown:
            self._key_d_down(isDown)
            if self.player.qinggongState in gametypes.QINGGONG_STATE_DASH_SET or self.player.isDashing:
                cellCmd.endUpQinggongState()
                self.forwardMagnitude = 0

    def backDodge(self, isDown):
        if not self.player.checkTempGroupFollow():
            return
        super(MousePhysics, self).backDodge(isDown)
        if not isDown:
            self._key_s_down(isDown)
            if self.player.qinggongState in gametypes.QINGGONG_STATE_DASH_SET or self.player.isDashing:
                cellCmd.endUpQinggongState()
                self.forwardMagnitude = 0

    def updateDashYaw(self, dirType):
        if dirType == qingGong.GO_FORWARD:
            self.setYaw(self.ccamera.direction.yaw)
        elif dirType == qingGong.SLIDE_DASH_NORMAL:
            self.setYaw(self.ccamera.direction.yaw)
        elif dirType == qingGong.GO_LEFT:
            self.setYaw(self.ccamera.direction.yaw - MousePhysics.VALUE_PI / 2)
        elif dirType == qingGong.GO_RIGHT:
            self.setYaw(self.ccamera.direction.yaw + MousePhysics.VALUE_PI / 2)
        elif dirType == qingGong.GO_BACK:
            self.setYaw(self.ccamera.direction.yaw + MousePhysics.VALUE_PI)
