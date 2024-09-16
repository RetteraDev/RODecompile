#Embedded file name: /WORKSPACE/data/entities/client/helpers/actionphysics.o
import BigWorld
import C_ui
import avatarPhysics
import gametypes
import gamelog
import gameglobal
import keys
import utils
import formula
from iNpc import INpc
from guis import hotkey as HK
from guis import cursor
from guis import uiConst
from guis import aimCross
from guis import menuManager
from helpers import action as ACT
from helpers import outlineHelper
from data import sys_config_data as SYSCD
from data import couple_emote_basic_data as CEBD
from cdata import game_msg_def_data as GMDD

class ActionPhysics(avatarPhysics.AvatarPhysics):
    AIM_POINT_OFFSET = 25
    AIM_DISTANCE = 50
    TARGET_FADE_TIME = 2
    SELECT_DIS_LIMIT = 70
    OFFSETY_BOUNDS = 1000.0

    def __init__(self):
        super(ActionPhysics, self).__init__()
        self.aimCross = aimCross.AimCross()
        self.lockTargetTime = 0
        self.player = BigWorld.player()
        self._mrDowntime = 0
        self.targetFadeTimer = 0
        self.lockAim = False
        self.showCursor = False
        self.backupTarget = None
        self.oldTarget = None
        self.selectAngle = SYSCD.data.get('tabTargetYaw', 120.0)

    def restore(self, needResetPos = True):
        self.showCursor = True
        self.aimCross.hide()
        self.ccamera.canRotate = False
        self.dcursor.canRotate = False
        C_ui.cursor_show(True)
        BigWorld.targeting.fixCenterOffset(False, 0, 0)
        BigWorld.targeting.offsetXBounds(0.0)
        BigWorld.targeting.offsetYBounds(0.0)
        BigWorld.targeting.offsetZBounds(0.0)
        BigWorld.target.skeletonCheckEnabled = False
        gameglobal.rds.ui.pushMessage.setHitTestDisable(False)
        self.refreshUIEnabled()
        self.backupTarget = None
        gameglobal.rds.ui.hideAimCross(True, isGray=True)
        gameglobal.rds.ui.hideTargetDir()

    def refreshUIEnabled(self):
        needShowCursor = self.needShowCursor()
        if not needShowCursor:
            gameglobal.rds.ui.setUIHitEnabled(False)
        elif self.inMouseSelectSkillPos:
            gameglobal.rds.ui.setUIHitEnabled(False)
        else:
            gameglobal.rds.ui.setUIHitEnabled(True)

    def restoreOldTarget(self):
        if self.oldTarget and self.oldTarget.inWorld:
            self.player.lockTarget(self.oldTarget)
            self.oldTarget = None

    def needShowCursor(self):
        emoteLockDC = False
        if self.player.coupleEmote:
            emoteLockDC = CEBD.data.get(self.player.coupleEmote[0], {}).get('lockDC', None)
        danDaoLockDC = self.player.inDanDao and not self.player.danDaoUseDir
        return self.showCursor or gameglobal.isWidgetNeedShowCursor or self.player.inForceNavigate or gameglobal.rds.ui.chat.isInputAreaVisible or self.player.isInApprenticeTrain() or self.player.isInApprenticeBeTrain() or self.player.inMeiHuo or self.player.inFear or self.player.inChaoFeng or emoteLockDC or danDaoLockDC or self.player.isLockYaw

    def _setCursorAimState(self):
        if self.needShowCursor() or self.inLoadingProgress or gameglobal.rds.GameState == gametypes.GS_LOADING:
            return
        self.aimCross.turnToAimState()

    def _setCursorAimedState(self, start):
        if self.needShowCursor() or self.inLoadingProgress or gameglobal.rds.GameState == gametypes.GS_LOADING:
            return
        self.aimCross.turnToAimedState(start)

    def reset(self):
        if self.needShowCursor() or self.inLoadingProgress or gameglobal.rds.GameState != gametypes.GS_PLAYGAME or gameglobal.SCENARIO_PLAYING == gameglobal.SCENARIO_PLAYING_TRACK_CAMERA or gameglobal.rds.ui.chat.isInputAreaVisible or gameglobal.rds.ui.recharge.getRechargeState():
            C_ui.cursor_show(True)
            self.backupTarget = None
            gameglobal.rds.ui.hideAimCross(True, isGray=True)
            return
        if BigWorld.player().circleEffect.isShowingEffect:
            return
        if BigWorld.player().chooseEffect.isShowingEffect:
            return
        self._resetCamAndDc()
        if BigWorld.player().targetLocked and BigWorld.player().targetLocked.inWorld:
            visible = gameglobal.rds.ui.getAimVisible()
            self._setCursorAimedState(not visible)
        else:
            self._setCursorAimState()
        cord = self.getAimCord()
        cursor.ignoreCursorPos = True
        cursor.setOutAndSaveOldPos(cord)
        C_ui.cursor_show(False)
        yOffset = self.aimCross.cursorAim.position.y
        offsetPlus = SYSCD.data.get('actionPhysicsYOffsetPlus', 0)
        boundsY = SYSCD.data.get('actionPhysicsYOffsetBounds', 1)
        boundsX = SYSCD.data.get('actionPhysicsXOffsetBounds', 0.3) / 2
        boundsZ = SYSCD.data.get('actionPhysicsZOffsetBounds', 0.3) / 2
        BigWorld.targeting.fixCenterOffset(True, 0, yOffset + offsetPlus)
        BigWorld.targeting.offsetXBounds(boundsX)
        BigWorld.targeting.offsetYBounds(boundsY)
        BigWorld.targeting.offsetZBounds(boundsZ)
        BigWorld.target.skeletonCheckEnabled = True
        gameglobal.rds.ui.actionbar.showMouseIcon(True)
        gameglobal.rds.ui.target.hideRightMenu()
        self.resetMouseIndicator()

    def backToCamera(self):
        if self.showCursor:
            return
        self.ccamera.canRotate = False
        self.dcursor.canRotate = True
        self.ccamera.canResetCamera = True

    def reload(self):
        self.downKeyBindings = [([HK.HKM[HK.KEY_FORWARD]], self._key_w_down),
         ([HK.HKM[HK.KEY_BACKWARD]], self._key_s_down),
         ([HK.HKM[HK.KEY_RIGHTTURN]], self._key_d_down),
         ([HK.HKM[HK.KEY_LEFTTURN]], self._key_a_down),
         ([HK.HKM[HK.KEY_MOVELEFT]], self._key_q_down),
         ([HK.HKM[HK.KEY_MOVERIGHT]], self._key_e_down),
         ([HK.HKM[keys.KEY_MOUSE0]], self._key_ml_down),
         ([HK.HKM[keys.KEY_MOUSE1]], self._key_mr_down),
         ([HK.HKM[keys.KEY_SPACE]], self._key_space_down),
         ([HK.HKM[HK.KEY_RESETCAM]], self._key_mm_down),
         ([HK.HKM[HK.KEY_CHANGE_CURSOR]], self._changeCursor),
         ([HK.HKM[HK.KEY_SWITCH_LAST]], self._switchToLastTarget),
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

    def _isAimForbid(self):
        p = BigWorld.player()
        if self.lockAim or p.fashion.doingActionType() in [ACT.SPELL_ACTION, ACT.GUIDE_ACTION, ACT.CHARGE_ACTION]:
            return True

    def _switchToLastTarget(self, isDown):
        if isDown:
            if self.player.lastTargetLocked and self.player.lastTargetLocked.inWorld:
                self.player.targetFocus(self.player.lastTargetLocked)

    def _key_mr_down(self, isDown):
        utils.recusionLog(6)
        self._msright = isDown
        if self.player.inForceMove:
            return
        super(ActionPhysics, self)._key_mr_down(isDown)
        p = BigWorld.player()
        if isDown and p.circleEffect.isShowingEffect:
            p.circleEffect.cancel()
            return
        if isDown and p.chooseEffect.isShowingEffect:
            p.chooseEffect.cancel()
            return
        if self.player.isPathfinding or self.player.isLockYaw or self.player.inForceNavigate:
            self._msright = 0
            self._key_ml_down(isDown)
            return
        if self.needShowCursor():
            self.testRotate()
        if isDown:
            self._mrDowntime = BigWorld.time()
        if self.needShowCursor():
            if not isDown:
                cursor.setInAndRestoreOldPos()
                BigWorld.target.reTarget()
                if self._mrDowntime != 0:
                    tg = BigWorld.time() - self._mrDowntime
                    if tg < 0.2 and self.player.target:
                        self.player.startKeyModeFlow(self.player.target)
        else:
            useSkillDown = isDown
            if formula.inDotaBattleField(getattr(p, 'mapID', 0)):
                p.useSkillByKeyInDota(2, useSkillDown)
            else:
                p.useSkillByKey(11, useSkillDown)
        if isDown:
            if not self._msleft:
                cursor.setOutAndSaveOldPos()
                if self.isForbidRotateDCursor():
                    self.ccamera.canResetCamera = False
                else:
                    self.ccamera.canResetCamera = True
        elif not self._msleft:
            cursor.setInAndRestoreOldPos()

    def _key_ml_down(self, isDown):
        utils.recusionLog(5)
        self._msleft = isDown
        if self.player.inForceMove:
            return
        p = BigWorld.player()
        if self.needShowCursor():
            self.testRotate()
        if isDown:
            if p.circleEffect.isShowingEffect:
                skillInfo = BigWorld.player().getSkillInfo(p.circleEffect.skillID, p.circleEffect.skillLevel)
                if p.checkSkill(skillInfo):
                    p.circleEffect.run()
                    return
            if not self._msright:
                cursor.setOutAndSaveOldPos()
        else:
            if not self._msright:
                cursor.setInAndRestoreOldPos()
            result = BigWorld.getCursorPosInWorld(self.player.spaceID, 1000, False, (gameglobal.TREEMATTERKINDS, gameglobal.GLASSMATTERKINDS))
            if self.groupMapMarkCircle.isInGroupMapMarkStatus() and not gameglobal.rds.ui.isMouseInUI():
                self.groupMapMarkCircle.markMapDone(result[0])
        if not self.needShowCursor() or not isDown:
            useSkillDown = isDown
            if formula.inDotaBattleField(getattr(p, 'mapID', 0)):
                p.useSkillByKeyInDota(0, useSkillDown)
            else:
                BigWorld.player().useSkillByKey(10, useSkillDown)

    def _key_mm_down(self, isDown):
        p = BigWorld.player()
        if p.circleEffect.isShowingEffect:
            p.circleEffect.cancel()
            return
        if p.chooseEffect.isShowingEffect:
            p.chooseEffect.cancel()
            return
        if self.showCursor:
            if isDown:
                self.ccamera.canResetYaw = True
            return
        if isDown:
            self.ccamera.canRotate = True
            self.dcursor.canRotate = False
            cursor.setOutAndSaveOldPos()

    def _changeCursor(self, isDown):
        if not isDown and not gameglobal.isWidgetNeedShowCursor and not self.player.isInApprenticeTrain() and not self.player.isInApprenticeBeTrain():
            if BigWorld.player().chooseEffect.isShowingEffect:
                BigWorld.player().chooseEffect.cancel()
            if BigWorld.player().circleEffect.isShowingEffect:
                BigWorld.player().circleEffect.cancel()
            if self.showCursor:
                self.showCursor = False
            else:
                self.showCursor = True
            if self.showCursor:
                self._resumeCursor(True)
            else:
                self._leaveCursor(True)

    def resetMouseIndicator(self):
        operationMode = self.player.getSavedOperationMode()
        plus = gameglobal.rds.ui.controlSettingV2.getModePlus(operationMode)
        key = self.player.operation[plus].get(gameglobal.PLUS_SHOW_CURSOR_KEY, 0)
        gameglobal.rds.ui.systemButton.setActionModeIndicator(True, key)

    def _resumeCursor(self, isDown, setMid = True):
        if isDown:
            gameglobal.rds.ui.pushMessage.setHitTestDisable(False)
            self.refreshUIEnabled()
            self.ccamera.canRotate = False
            self.dcursor.canRotate = False
            self.aimCross.hide()
            C_ui.cursor_show(True)
            self.backupTarget = None
            gameglobal.rds.ui.hideAimCross(True, isGray=True)
            if setMid:
                cord = self.getAimCord()
                C_ui.set_cursor_pos(cord[0], cord[1])
            else:
                cursor.setInAndRestoreOldPos()
            BigWorld.targeting.fixCenterOffset(False, 0, 0)
            BigWorld.targeting.offsetXBounds(0.0)
            BigWorld.targeting.offsetYBounds(0.0)
            BigWorld.targeting.offsetZBounds(0.0)
            BigWorld.target.skeletonCheckEnabled = False
            self.resetMouseIndicator()

    def getAimCord(self):
        innerScreenSize = 1.0
        if hasattr(BigWorld, 'getInnerScreenSize'):
            innerScreenSize = BigWorld.getInnerScreenSize()
        offset = (1 - self.aimCross.cursorAim.position[1]) / 2
        height = int(BigWorld.screenHeight() / innerScreenSize * offset)
        return (int(BigWorld.screenWidth() / innerScreenSize / 2), height)

    def _leaveCursor(self, isDown):
        needCursor = gameglobal.isWidgetNeedShowCursor
        if C_ui.cursor_in_clientRect() and not needCursor:
            self.reset()
        else:
            self._resumeCursor(1, False)

    def resetControl(self):
        if not self.isChasing:
            if self._w or self.isAutoMoving:
                self._forward = True
            else:
                self._forward = False
            self.moveForward(self._forward)
            if self._s:
                self._backward = True
            else:
                self._backward = False
            self.moveBackward(self._backward)
            if self._q:
                self._moveleft = True
            else:
                self._moveleft = False
            self.moveLeft(self._moveleft)
            if self._e:
                self._moveright = True
            else:
                self._moveright = False
            self.moveRight(self._moveright)
            if self._space:
                self._moveUp = True
            else:
                self._moveUp = False
            if self._x:
                self._moveDown = True
            else:
                self._moveDown = False
            self.moveUp(self._moveUp, self._moveDown)
            if self._a:
                self._turnleft = True
            else:
                self._turnleft = False
            if self._d:
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
            self.resetCameraAndDcursorRotate()
        self.updateVelocity()

    def resetCameraAndDcursorRotate(self):
        super(ActionPhysics, self).resetCameraAndDcursorRotate()
        if not self.showCursor and not gameglobal.isWidgetNeedShowCursor:
            self._resetCamAndDc()

    def _resetCamAndDc(self):
        if self.isForbidRotateDCursor():
            self.ccamera.canRotate = True
            self.dcursor.canRotate = False
        elif self.player.needLockCameraAndDc():
            self.dcursor.canRotate = False
        elif self.player.isPathfinding:
            self.dcursor.canRotate = False
            self.ccamera.canRotate = True
        else:
            self.dcursor.canRotate = True
            self.ccamera.canRotate = False
        if not self.player.forbidChangeYaw():
            self.ccamera.canResetCamera = True

    def updateMoveControl(self):
        utils.recusionLog(3)
        if self.player.confusionalState:
            self.updateConfusionalMoveState()
            return
        if self.player.life == gametypes.LIFE_DEAD:
            return
        self.forceAllKeysUp()
        if self.player.lockHotKey:
            return
        self._w = HK.HKM[HK.KEY_FORWARD].isAnyDown()
        self._q = HK.HKM[HK.KEY_MOVELEFT].isAnyDown()
        self._e = HK.HKM[HK.KEY_MOVERIGHT].isAnyDown()
        self._s = HK.HKM[HK.KEY_BACKWARD].isAnyDown()
        self._d = HK.HKM[HK.KEY_RIGHTTURN].isAnyDown()
        self._a = HK.HKM[HK.KEY_LEFTTURN].isAnyDown()
        self._space = HK.HKM[keys.KEY_SPACE].isAnyDown()
        self._x = HK.HKM[HK.KEY_DOWN].isAnyDown()
        self.resetControl()

    def hideWidget(self):
        try:
            if gameglobal.rds.ui.roleInfo.isShow:
                gameglobal.rds.ui.roleInfo.hide()
            if gameglobal.rds.ui.skill.lifeMediator:
                gameglobal.rds.ui.skill.closeLifeSkill()
            if gameglobal.rds.ui.skill.generalMediator and not gameglobal.rds.ui.cameraTable.isShow:
                gameglobal.rds.ui.skill.closeGeneralSkill()
            if gameglobal.rds.ui.skill.detailMediator:
                gameglobal.rds.ui.skill.closeDetailpanel()
            if gameglobal.rds.ui.skill.enhanceMediator:
                gameglobal.rds.ui.skill.closeEnhancePanel()
            if gameglobal.rds.ui.skill.daoHangDirMediator:
                gameglobal.rds.ui.skill.closeDaohangDirPanel()
            if gameglobal.rds.ui.skill.isShow and not gameglobal.rds.ui.skill.hasSkillPointChange():
                gameglobal.rds.ui.skill.clearWidget()
            if gameglobal.rds.ui.mail.isShow():
                gameglobal.rds.ui.mail.clearWidget()
            if gameglobal.rds.ui.inventory.mediator:
                gameglobal.rds.ui.inventory.closeInventory()
            if gameglobal.rds.ui.questLog.isShow:
                gameglobal.rds.ui.questLog.hide()
            if gameglobal.rds.ui.team.mediator:
                gameglobal.rds.ui.team.close()
            if gameglobal.rds.ui.ranking.mediator:
                gameglobal.rds.ui.ranking.hide()
            if gameglobal.rds.ui.systemSettingV2.isShow():
                gameglobal.rds.ui.systemSettingV2.close()
            if gameglobal.rds.ui.quest.isShow:
                gameglobal.rds.ui.quest.close()
            if gameglobal.rds.ui.npcV2.isShow:
                gameglobal.rds.ui.npcV2.leaveStage()
            if gameglobal.rds.ui.friend.isShow:
                gameglobal.rds.ui.friend.clearWidget()
            if gameglobal.rds.ui.soundSettingV2.widget:
                gameglobal.rds.ui.gameSetting.hide(True)
            if gameglobal.rds.ui.videoSetting.widget:
                gameglobal.rds.ui.gameSetting.hide(True)
            if gameglobal.rds.ui.surfaceSettingV2.widget:
                gameglobal.rds.ui.gameSetting.hide(True)
            if gameglobal.rds.ui.controlSettingV2.widget:
                gameglobal.rds.ui.controlSettingV2.handleCancelBtnClick()
            if gameglobal.rds.ui.keySettingV2.widget:
                gameglobal.rds.ui.keySettingV2.handleCancelBtnClick()
            if gameglobal.rds.ui.consign.isShow():
                gameglobal.rds.ui.consign.clearWidget()
            if gameglobal.rds.ui.baoDian.isShow():
                gameglobal.rds.ui.baoDian.hide()
            menuTarget = menuManager.getInstance().menuTarget
            if getattr(menuTarget, 'menuId', 0) in (uiConst.MENU_ENTITY, uiConst.MENU_TARGET):
                gameglobal.rds.ui.hideAllMenu()
        except:
            pass

    def moveControl(self, desc, isDown):
        if self.player.inMeiHuo:
            return
        if not BigWorld.player().circleEffect.isShowingEffect and not BigWorld.player().chooseEffect.isShowingEffect:
            if not gameglobal.rds.ui.chat.isInputAreaVisible and isDown:
                self.showCursor = False
                self.reset()
                self.hideWidget()
        if not self.player.clientControl:
            return
        performAction = False
        turningAction = False
        if desc in ('_w', '_s') and isDown and not self.player.inForceNavigate:
            if not (getattr(self.player, 'inChaoFeng', False) or getattr(self.player, 'inMeiHuo', False)):
                self.stopAutoMove()
        if desc == '_w':
            if self._w:
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
        if desc == '_q':
            if self._q:
                self._moveleft = True
                performAction = True
            else:
                self._moveleft = False
            self.moveLeft(self._moveleft)
        if desc == '_e':
            if self._e:
                self._moveright = True
                performAction = True
            else:
                self._moveright = False
            self.moveRight(self._moveright)
        self._combinationKey()
        if desc == '_a' or desc == '_d':
            if self._a:
                self._turnleft = True
            else:
                self._turnleft = False
            if self._d:
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
        if desc in ('_msleft', '_msright'):
            self.testRotate()
        if performAction and (self.player.isPathfinding or self.player.physics.seeking):
            if not (getattr(self.player, 'inChaoFeng', False) or getattr(self.player, 'inMeiHuo', False)):
                self.stopChasing()
        elif turningAction and (self.player.isPathfinding or self.player.physics.seeking):
            if not (getattr(self.player, 'inChaoFeng', False) or getattr(self.player, 'inMeiHuo', False)):
                self.stopChasing()
        super(ActionPhysics, self).moveControl(desc, isDown)

    def testRotate(self):
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

    def isMovingActionKeyControl(self):
        l = (self._s,
         self._w,
         self._q,
         self._e,
         self.isAutoMoving)
        for k in l:
            if k:
                return True

        return False

    def onTargetFocus(self, entity, lockAim):
        if self.targetFadeTimer:
            BigWorld.cancelCallback(self.targetFadeTimer)
            self.targetFadeTimer = 0
        if entity and entity.inWorld:
            length = (self.player.position - entity.position).length
            if length <= ActionPhysics.SELECT_DIS_LIMIT and self.lockAim and self.needSelect(entity):
                if entity != self.player and entity != self.player.targetLocked:
                    self.backupTarget = entity
                    self.aimCross.showBackupTargetAimCross()
                    return
            if self._isAimForbid():
                gamelog.debug('@actionPhysics._isAimForbid return')
                return
            self.changeCursorState(entity, lockAim)

    def changeCursorState(self, entity, lockAim, quickLock = False):
        if not entity or not entity.inWorld:
            return
        if not self.player or not self.player.inWorld:
            return
        length = (self.player.position - entity.position).length
        if length <= ActionPhysics.SELECT_DIS_LIMIT and not self.player.circleEffect.isShowingEffect and self.needSelect(entity, quickLock):
            if self.player.targetLocked != entity:
                self.player.lockTarget(entity)
                return
            if lockAim:
                self.lockAim = True
                outlineHelper.setLockedTarget()
            self.lockOptionalTarget()
            self._setCursorAimedState(True)
            color = self.aimCross.getAimCrossColor(BigWorld.player().targetLocked)
            gameglobal.rds.ui.playAimLock(True, 'normal', lockAim)

    def lockOptionalTarget(self, needShowOptionalAim = False):
        if gameglobal.OPTIONAL_TARGET:
            if self.player.targetLocked:
                isEnemy = self.player.isEnemy(self.player.targetLocked)
                entities = BigWorld.inCameraEntity(80)
                if not entities:
                    entities = []
                length = 1000
                retEnt = None
                for ent in entities:
                    if not hasattr(ent, 'IsCombatUnit') or not ent.IsCombatUnit:
                        continue
                    if ent == self:
                        continue
                    if getattr(ent, 'noSelected', None):
                        continue
                    if not getattr(ent, 'fashion', None):
                        continue
                    if getattr(ent, 'life', None) == gametypes.LIFE_DEAD:
                        continue
                    if self.player.targetLocked == ent or self.player == ent:
                        continue
                    if isEnemy:
                        if self.player.isEnemy(ent):
                            continue
                    elif not self.player.isEnemy(ent):
                        continue
                    if keys.CAP_CAN_USE not in ent.targetCaps:
                        continue
                    le = (ent.position - self.player.targetLocked.position).length
                    if le < length:
                        length = le
                        retEnt = ent

                self.player.optionalTargetLocked = retEnt
                if retEnt == None:
                    gameglobal.rds.ui.subTarget.hideSubTargetUnitFrame()
                else:
                    gameglobal.rds.ui.subTarget.showSubTargetUnitFrame()
                if needShowOptionalAim:
                    self.aimCross.showOptionalTargetAimCross()

    def needSelect(self, entity, quickLock = False):
        if entity == BigWorld.player():
            return True
        if getattr(entity, 'noSelected', None):
            return False
        if not getattr(entity, 'fashion', None):
            return False
        if entity:
            angle = self.player.getTgtAngle(entity)
            if angle >= self.selectAngle or angle < -self.selectAngle:
                return False
            className = entity.__class__.__name__
            blackList = SYSCD.data.get('apSelectBlackList', [])
            if className in blackList:
                return False
            whiteList = SYSCD.data.get('apSelectINpcWhiteList', [])
            if isinstance(entity, INpc) and className not in whiteList:
                return False
            if hasattr(entity, 'life') and entity.life == gametypes.LIFE_DEAD and not self.showCursor:
                return False
            if not gameglobal.CAN_LOCK_TARGET_NPC:
                if BigWorld.player().isFriend(entity) and not quickLock:
                    return False
            return True
        return False

    def onTargetBlur(self, entity):
        if self.targetFadeTimer:
            BigWorld.cancelCallback(self.targetFadeTimer)
            self.targetFadeTimer = 0
        self.backupTarget = None
        gameglobal.rds.ui.hideAimCross(True, isGray=True)
        if not self.lockAim:
            if self.targetFadeTimer:
                BigWorld.cancelCallback(self.targetFadeTimer)
            fadeTime = SYSCD.data.get('apLockFadeTime', ActionPhysics.TARGET_FADE_TIME)
            self.targetFadeTimer = BigWorld.callback(fadeTime, self._unLockTarget)

    def refreshTargetFadeTimer(self):
        if self.lockAim:
            return
        if self.targetFadeTimer:
            BigWorld.cancelCallback(self.targetFadeTimer)
            self.targetFadeTimer = 0
        fadeTime = SYSCD.data.get('apLockFadeExtendTime', 1)
        self.targetFadeTimer = BigWorld.callback(fadeTime, self._unLockTarget)

    def _unLockTarget(self):
        if not self.player or not self.player.inWorld:
            return
        BigWorld.player().unlockTarget()
        self._setCursorAimState()

    def resetAimCrossPos(self, currentScrollNum):
        currentScrollNum = min(currentScrollNum, gameglobal.ACTION_PHYSICS_Y_OFFSET_MAX_STEP)
        yOffset = self.player.getPhysicsYOffset()[currentScrollNum + 1]
        self.aimCross.setAimCrossOffset(yOffset)
        offsetPlus = SYSCD.data.get('actionPhysicsYOffsetPlus', 0)
        boundsY = SYSCD.data.get('actionPhysicsYOffsetBounds', 1)
        boundsX = SYSCD.data.get('actionPhysicsXOffsetBounds', 0.3) / 2
        boundsZ = SYSCD.data.get('actionPhysicsZOffsetBounds', 0.3) / 2
        BigWorld.targeting.fixCenterOffset(True, 0, yOffset + offsetPlus)
        BigWorld.targeting.offsetXBounds(boundsX)
        BigWorld.targeting.offsetYBounds(boundsY)
        BigWorld.targeting.offsetZBounds(boundsZ)
        BigWorld.target.skeletonCheckEnabled = True

    def release(self):
        self.restore()
        self.aimCross.release()

    def stopChasing(self):
        if self.isChasing:
            self.isChasing = False
            self.chasingEntity = None
            self.ccamera.allResetYaw = False
            self.forwardMagnitude = 0
        self.stopSeek()

    def forwardDodge(self, isDown):
        if not self.player.checkTempGroupFollow():
            return
        super(ActionPhysics, self).forwardDodge(isDown)
        if self.player.qinggongState in gametypes.QINGGONG_STATE_DASH_SET or isDown:
            if not self.player.isJumping:
                self._key_w_down(isDown)
            return
        if not isDown:
            self._key_w_down(isDown)
