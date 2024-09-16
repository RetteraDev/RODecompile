#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impPlayerRideFly.o
from gamestrings import gameStrings
import time
import BigWorld
import Math
import gameglobal
import gamelog
import gametypes
import const
import formula
import utils
import clientUtils
from helpers import cellCmd
from helpers import navigator
from data import equip_data as ED
NORMAL_SPEED = 5
HIGH_SPEED = 40
LAND_MOUNT_SPEED = 12
SKY_MOUNT_SPEED = 15
FLOATING_HEIGHT = 500
FLY_MODE = 0
RIDE_MODE = 0
TX2_ROLE_MODEL = None
TX2_ROLE_MODEL_PATH = ('char/1001/base.model', 'char/1001/dummy.model')
SWAP_MODEL = None

class ImpPlayerRideFly(object):

    def startFly(self, isDown):
        global FLY_MODE
        if isDown:
            return
        FLY_MODE = (FLY_MODE + 1) % 3
        self.inFly = FLY_MODE >= 1
        if FLY_MODE == 2:
            pos = self.position
            self.physics.teleport(Math.Vector3(pos[0], FLOATING_HEIGHT, pos[2]))
        self.set_inFly(self.inFly)
        self.flySwitch(self.inFly)

    def needDcControlPitch(self):
        if self.inSwim:
            if self.isOnSwimRide():
                return False
        return self.inFly or self.inSwim

    def resetCollideWithWater(self):
        self.physics.collideWithWater = self.isCollideWithWater()

    def isCollideWithWater(self):
        if self.inFly > 0:
            return self.inFly
        if self.bianshen[1]:
            if self.bianshen[0] == gametypes.BIANSHEN_RIDING_RB and formula.mapLimit(formula.LIMIT_WINGFLY, formula.getMapId(self.spaceNo)):
                return False
            else:
                return ED.data.get(self.bianshen[1], {}).get('flyRide', False)
        return False

    def resetFly(self, showEffect = True):
        super(self.__class__, self).resetFly(showEffect)
        self.physics.dcControlPitch = self.needDcControlPitch()
        self.physics.collideWithWater = self.isCollideWithWater()
        self.enterWaterHeight = self.getEnterWaterHeight()
        if self.inFly:
            gamelog.debug('resetFly:', self.physics.jumping, self.isJumping)
            self.physics.swim(1, self.flyHeight)
            self.loseGravity()
        else:
            self.ap.endFlyAccelerate(True)
            if not self.inSwim:
                self.physics.swim(0)
            self.restoreGravity()
        if self.ap:
            self.ap.recalcSpeed()
        self.resetCamera()

    def startDash(self, isDown):
        if isDown:
            return
        if not gameglobal.rds.isSinglePlayer:
            return
        self.ap.isWalking = not self.ap.isWalking
        self.ap.isRunning = not self.ap.isRunning
        if self.ap.isWalking:
            self.ap.dashFwdSpeed = HIGH_SPEED
            self.ap.dashBackSpeed = HIGH_SPEED * 0.6
            self.ap.walkFwdSpeed = HIGH_SPEED
            self.ap.walkBackSpeed = HIGH_SPEED * 0.6
            self.ap.updateVelocity()
        else:
            self.ap.dashFwdSpeed = LAND_MOUNT_SPEED
            self.ap.dashBackSpeed = LAND_MOUNT_SPEED * 0.6
            self.ap.walkFwdSpeed = NORMAL_SPEED
            self.ap.walkBackSpeed = NORMAL_SPEED * 0.6
            self.ap.updateVelocity()

    def changeMount(self, isDown):
        global RIDE_MODE
        global SWAP_MODEL
        global TX2_ROLE_MODEL_PATH
        global TX2_ROLE_MODEL
        if isDown:
            return
        RIDE_MODE = (RIDE_MODE + 1) % 3
        if RIDE_MODE:
            if not TX2_ROLE_MODEL:
                TX2_ROLE_MODEL = clientUtils.model(*TX2_ROLE_MODEL_PATH)
                SWAP_MODEL = self.model
            if RIDE_MODE == 1:
                self.fashion.setupModel(TX2_ROLE_MODEL)
                self.modelServer.bodyModel = TX2_ROLE_MODEL
            self.modelServer.enterRideHB(RIDE_MODE)
        else:
            self.modelServer.leaveRideHB()
            self.fashion.setupModel(SWAP_MODEL)
            self.modelServer.bodyModel = SWAP_MODEL
        if RIDE_MODE == 1:
            self.ap.runFwdSpeed = LAND_MOUNT_SPEED
        elif RIDE_MODE == 2:
            self.ap.runFwdSpeed = SKY_MOUNT_SPEED
        else:
            self.ap.runFwdSpeed = NORMAL_SPEED
        self.ap.updateVelocity()

    def startSlowDown(self, down):
        if down:
            self.physics.velocity = (0, -10, 0)
            self.physics.maxTopVelocity = self.physics.velocity
        else:
            self.physics.velocity = (0, 0, 0)

    def flySwitch(self, b):
        if b:
            self.fashion.playSingleAction('14011')
        else:
            self.fashion.playSingleAction('14011')

    def flyUp(self, isDown):
        if isDown:
            self.ap.upwardMagnitude = 1
        else:
            self.ap.upwardMagnitude = 0

    def enterRide(self):
        if not self.stateMachine.checkMount():
            return False
        if not self.gmMode and formula.mapLimit(formula.LIMIT_RIDE, formula.getMapId(self.spaceNo)):
            self.chatToEventEx(gameStrings.TEXT_IMPPLAYERRIDEFLY_166, const.CHANNEL_COLOR_RED)
            return False
        if self._isSchoolSwitch():
            self.chatToEventEx(gameStrings.TEXT_IMPPLAYERRIDEFLY_169, const.CHANNEL_COLOR_RED)
            return False
        self.cancelWeaponTimerAndHangUpWeapon()
        self.cell.enterRide()
        return True

    def leaveRide(self):
        if self.stateMachine.checkDismount():
            if self.checkPathfinding():
                self.cancelPathfinding()
            self.cell.leaveRide()
            return True
        return False

    def horseRoar(self):
        if self.inRiding():
            actId = self.fashion.getHorseRoarJumpAction()
            if actId:
                self.cell.horseRoar()

    def enterWingFly(self):
        if not self.stateMachine.checkOpenWingFly():
            return
        self.ap.stopMove()
        self.fashion.stopAllActions()
        self.fashion.stopModelAction(self.modelServer.wingFlyModel.model)
        self.ap.updateVelocity()
        if self.isPathfinding:
            navigator.getNav().stopPathFinding()
        cellCmd.enterWingFly(False)
        self.inWingTakeOff = True
        if getattr(self, 'cancelWingTakeOffTimer', 0):
            BigWorld.cancelCallback(self.cancelWingTakeOffTimer)
        self.cancelWingTakeOffTimer = BigWorld.callback(2, self.cancelWingTakeOff)
        self.takeOffActionPlayed = False

    def cancelWingTakeOff(self):
        self.inWingTakeOff = False
        self.cancelWingTakeOffTimer = False

    def leaveWingFly(self):
        if not self.stateMachine.checkCloseWingFly():
            return
        self.inWingTakeOff = False
        self.ap.endFlyAccelerate(True)
        self.ap.stopMove()
        self.cell.leaveWingFly()
        if self.checkPathfinding():
            self.cancelPathfinding()
        self.leaveWingTime = time.time()

    def getWingFlyNormalSpeedForNav(self):
        resSpeed = 0
        if len(self.speed) > 3:
            resSpeed = self.speed[gametypes.SPEED_FLY] / 60.0
        else:
            resSpeed = gametypes.FLY_H_SPEED_BASE
        equipWingFly = self.equipment.get(gametypes.EQU_PART_WINGFLY)
        if equipWingFly:
            resSpeed = resSpeed * equipWingFly.getVelocityDuraFactor() * equipWingFly.getVelocityFactorByVip(self)
            return resSpeed * utils.getWingSpeedData(self).get('flyHorizonFactor', gametypes.FLY_HORIZON_SPEED_FACTOR)
        else:
            return 0

    def getHorseNormalSpeedForNav(self):
        resSpeed = 0
        if len(self.speed) > 5:
            resSpeed = self.speed[gametypes.SPEED_RIDE] / 60.0
        else:
            resSpeed = gametypes.HORSE_H_SPEED_BASE
        equipRide = self.equipment.get(gametypes.EQU_PART_RIDE)
        if equipRide:
            resSpeed = resSpeed * equipRide.getVelocityDuraFactor() * equipRide.getVelocityFactorByVip(self)
            return resSpeed * utils.getHorseSpeedData(self).get('runFactor', 1.0)
        else:
            return 0
