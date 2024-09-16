#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impPlayerSwim.o
import BigWorld
from Math import Vector3
import gameglobal
import gamelog
import gametypes
import keys
import const
from sfx import screenEffect
from helpers import cellCmd
from helpers import qingGong
from guis import hotkey as HK
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD

class ImpPlayerSwim(object):
    ENTER_RUNONWATER_HEIGHT = -1.0

    def insideWater(self, inWater, waterHeight):
        gamelog.debug('PlayerAvatar::insideWater %d' % inWater, waterHeight, self.roleName, self.id)
        if inWater == const.SHOALWATER and not self.stateMachine.checkStatus(const.CT_SHOAL_WATER):
            return
        super(self.__class__, self).insideWater(inWater, waterHeight)
        if self.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
            equ = self.equipment.get(gametypes.EQU_PART_RIDE)
            if equ.haveTalent(gametypes.RIDE_TALENT_SWIM):
                pass
            else:
                if self.bianshenStateMgr.canFly():
                    self.cell.enterFlyRide()
                    return
                self.cell.leaveRide()
        if self.qinggongMgr.checkCanDashOnWater():
            if inWater == const.SHOALWATER and self.qinggongMgr.getDistanceFromWater() > -3:
                if self.qinggongState == gametypes.QINGGONG_STATE_FAST_RUN and self.ap.physics.velocity[2] > 0:
                    if self.inSwim == const.DEEPWATER:
                        return
                    self.enterWaterHeight = 0
                    height = abs(self.qinggongMgr.getDistanceFromWater()) if self.qinggongMgr.getDistanceFromWater() < -0.5 else 0.0
                    self.cell.enterRunOnWater(1, height)
                    self.loseGravity()
                    return
                dirDown = False
                if self.getOperationMode() == gameglobal.MOUSE_MODE:
                    dirDown = HK.HKM[HK.KEY_FORWARD].isAnyDown() or HK.HKM[HK.KEY_BACKWARD].isAnyDown() or HK.HKM[HK.KEY_MOVELEFT].isAnyDown() or HK.HKM[HK.KEY_MOVERIGHT].isAnyDown()
                else:
                    dirDown = HK.HKM[HK.KEY_FORWARD].isAnyDown()
                if self.isDashing and dirDown and inWater and self.ap.physics.velocity[2] > 0 and self.qinggongState != gametypes.QINGGONG_STATE_MOUNT_DASH:
                    height = abs(self.qinggongMgr.getDistanceFromWater()) if self.qinggongMgr.getDistanceFromWater() < -0.5 else 0.0
                    self.cell.enterRunOnWater(1, height)
                    self.enterWaterHeight = 0
                    self.loseGravity()
                    self.ap.upwardMagnitude = 0
                    self.ap.updateVelocity()
                    self.fashion.breakJump()
                    return
        self.intoWater(inWater, waterHeight)

    def resetInWaterUpwardMagnitude(self):
        self.ap.upwardMagnitude = 0.0

    def intoWater(self, inWater, waterHeight):
        oldSwim = self.inSwim
        self.cell.leaveRunOnWater()
        self.inSwim = inWater
        if inWater:
            if inWater == const.SHOALWATER and oldSwim == const.DEEPWATER:
                self.resetInWaterUpwardMagnitude()
                BigWorld.dcursor().pitch = -0.2
                if HK.HKM[HK.KEY_FORWARD].isAnyDown() or self.ap.isAutoMoving:
                    self.physics.enableSwimJump = False
                screenEffectId = SCD.data.get('swim_screenEffect', None)
                if screenEffectId:
                    screenEffect.startEffects(gameglobal.EFFECT_TAG_SWIM, [screenEffectId], False, BigWorld.player())
                if self.isGuiding in (const.GUIDE_TYPE_NO_MOVE, const.GUIDE_TYPE_MOVE):
                    cellCmd.cancelSkill()
            elif inWater == const.DEEPWATER and oldSwim == const.SHOALWATER or inWater == const.DEEPWATER and oldSwim == const.NOWATER:
                self.loseGravity()
                if HK.HKM[HK.KEY_FORWARD].isAnyDown() or self.ap.isAutoMoving:
                    self.physics.enableSwimJump = True
                if self.isGuiding in (const.GUIDE_TYPE_NO_MOVE, const.GUIDE_TYPE_MOVE):
                    cellCmd.cancelSkill()
            elif inWater == const.SHOALWATER and oldSwim == const.NOWATER:
                position = Vector3(self.position[0], self.position[1] + abs(waterHeight if waterHeight != None else 0), self.position[2])
                self.ap.showJumpWaterEffect(position)
                if self.isGuiding in (const.GUIDE_TYPE_NO_MOVE, const.GUIDE_TYPE_MOVE):
                    cellCmd.cancelSkill()
            self.physics.keepJumpVelocity = False
            self.enterWaterHeight = self.getEnterWaterHeight()
            self.cell.enterSwim(inWater)
        else:
            self.cell.leaveSwim()
        self.waterHeight = waterHeight
        if oldSwim == const.NOWATER and inWater in (const.SHOALWATER, const.DEEPWATER) and self.life != gametypes.LIFE_DEAD or inWater == const.NOWATER:
            self._resetFreeMode(inWater)
        if inWater == const.DEEPWATER:
            self.resetSwim()
        if not inWater and self.physics.enableSwimJump:
            if HK.HKM[HK.KEY_WINGFLYUP].isAnyDown():
                if not self.canFly() and self.qinggongMgr.checkCanWingFlyLandUp():
                    self.qinggongMgr.setState(qingGong.STATE_WINGFLY_IDLE, True)
                    self.qinggongMgr.doFuncByEvent(qingGong.EVENT_WINGFLY_LANDUP)
            elif HK.HKM[keys.KEY_SPACE].isAnyDown():
                position = Vector3(self.position[0], self.position[1] + abs(waterHeight), self.position[2])
                self.ap.showJumpWaterEffect(position)
                self.ap.upwardMagnitude = 0.0
                if self.ap._realJump(True):
                    if self.isOnSwimRide():
                        pass
                    else:
                        self.qinggongMgr.doFuncByEvent(qingGong.EVENT_SPACE_DOWN)
        self.ap.updateVelocity()
        if oldSwim == const.NOWATER and self.inSwim:
            self.suggestSpriteFly(True, False)
        elif self.inSwim == const.NOWATER and oldSwim:
            self.delaySuggestSpriteFly(False, False)

    def _resetFreeMode(self, isFree):
        super(self.__class__, self)._resetFreeMode(isFree)
        if isFree:
            try:
                self.physics.swim(1, self.waterHeight)
            except:
                raise Exception('_resetFreeMode', type(self.waterHeight), self.waterHeight)

            cellCmd.endUpQinggongState()
            self.loseGravity()
        else:
            self.physics.swim(0)
            self.restoreGravity()
        self.resetSwim()

    def resetSwim(self):
        if not self.inWorld:
            return
        super(self.__class__, self).resetSwim()
        if self.inSwim:
            self.castSkillBusy = False
        self.physics.dcControlPitch = self.needDcControlPitch()
        self.ap.updateVelocity()
        self.qinggongMgr.jumpDashFlag = False

    def set_inSwim(self, old):
        super(self.__class__, self).set_inSwim(old)
        if self.bp == self._getmbp() and self.inSwim == const.DEEPWATER or self.bp == 0 and self.inSwim != const.DEEPWATER:
            gameglobal.rds.ui.breathbar.setBreathbar(self.bp, False)
        if self.inSwim and self.inFishingReady():
            self.showGameMsg(GMDD.data.FISHING_BREAK, ())
            self.stopFish()

    def set_runOnWater(self, old):
        super(self.__class__, self).set_runOnWater(old)
        if self.runOnWater:
            self.suggestSpriteFly(True, False)

    def set_bp(self, old):
        super(self.__class__, self).set_bp(old)
        if self.bp == self._getmbp() and self.inSwim != const.DEEPWATER:
            if gameglobal.rds.ui.breathbar.mediator:
                gameglobal.rds.ui.breathbar.mc.SetVisible(False)
            return
        gameglobal.rds.ui.breathbar.setBreathbar(self.bp)

    def set_mbp(self, old):
        pass

    def _getmbp(self):
        return self.mbp or SCD.data.get('mbp', 180)
