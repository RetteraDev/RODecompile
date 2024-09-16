#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impSwim.o
import BigWorld
import gametypes
import const
import gamelog

class ImpSwim(object):

    def insideWater(self, inWater, waterHeight):
        gamelog.debug('zf:@Avatar::insideWater %d' % inWater, waterHeight, self.roleName, self.id)
        self.isInsideWater = inWater

    def resetSwim(self):
        if self.inSwim == const.DEEPWATER:
            self.filter.applyEntityPitch = self.needApplyEntityPitch()
        else:
            self.filter.applyEntityPitch = False
        self.model.straighten()
        self.fashion.autoSetStateCaps()
        self.updateBodySlope()
        self.fashion.resetTurnBodyState()
        self.resetShadowUfo()
        self.modelServer.refreshWeaponState()
        if self.inSwim and self.life == gametypes.LIFE_ALIVE:
            self.fashion.stopAllActions()

    def _resetFreeMode(self, isFree):
        if not self.firstFetchFinished:
            return
        if isFree:
            self.fashion.detachFootTrigger()
            self.fashion.breakJump()
            self.fashion.breakFall()
            self.fashion.stopAllActions()
        else:
            self.fashion.setupFootTrigger()

    def canSwim(self):
        return self.inSwim

    def set_inSwim(self, old):
        if not self.fashion.isPlayer:
            self.resetSwim()
        if self.inFly:
            self.resetFly()
        self.resetFootIK()

    def set_runOnWater(self, old):
        self.fashion.autoSetStateCaps()

    def set_bp(self, old):
        pass

    def getEnterWaterHeight(self):
        if self.bianshen[0] == gametypes.BIANSHEN_RIDING_RB:
            return 5.0 * self.getModelHeight() / 12.0
        return 5.0 * self.getModelHeight() / 7.0

    def getHeightOutOfWater(self):
        res = BigWorld.findWaterFromPoint(self.spaceID, self.position)
        if res is None:
            return
        else:
            height = self.position.y - res[0] + self.model.height
            if height > self.model.height:
                return
            return height

    def set_mbp(self, old):
        pass
