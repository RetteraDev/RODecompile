#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impPlayerCheck.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import formula
import const

class ImpPlayerCheck(object):

    def checkPhaseAreaState(self):
        if not self.phaseBounds:
            return
        minX = self.phaseBounds[0]
        minZ = self.phaseBounds[1]
        maxX = self.phaseBounds[2]
        maxZ = self.phaseBounds[3]
        if self.position[0] < minX or self.position[0] > maxX or self.position[2] < minZ or self.position[2] > maxZ:
            if not self.confirmBtn:
                self.confirmBtn = gameglobal.rds.ui.messageBox.showYesNoMsgBox(gameStrings.TEXT_IMPPLAYERCHECK_16, self._onConfirmBackBigWorld, noCallback=self._onCancelBackBigWorld)
            if self.fashion:
                self.fashion.breakJump()
                self.fashion.breakFall()
                self.fashion.stopAllActions()
            if self.ap:
                self.ap.stopMove()
        else:
            self.checkPhaseAreaCallback = BigWorld.callback(0.5, self.checkPhaseAreaState)

    def _onConfirmBackBigWorld(self):
        self.confirmBtn = None
        if formula.spaceInMultiLine(self.spaceNo):
            BigWorld.player().cell.exitLine()
        elif formula.spaceInFuben(self.spaceNo):
            fbNo = formula.getFubenNo(self.spaceNo)
            fbType = formula.whatFubenType(fbNo)
            if fbType in (const.FB_TYPE_GROUP,):
                BigWorld.player().cell.exitFuben()
            elif fbType in const.FB_TYPE_SINGLE_SET:
                BigWorld.player().cell.exitSingleFuben()
        else:
            self.cell.teleportOutPhaseByIcon(const.SPACE_NO_BIG_WORLD)
        self.faceToDir(-3.02)

    def _onCancelBackBigWorld(self):
        self.confirmBtn = None
        self.checkPhaseAreaCallback = BigWorld.callback(3.0, self.checkPhaseAreaState)
