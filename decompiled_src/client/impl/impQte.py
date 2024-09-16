#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impQte.o
import BigWorld
import gameglobal
from sMath import limit
from helpers import action
from data import qte_data as QTED
OP_LIST = set()

class ImpQte(object):
    QTE_OP_ACTION = 1
    QTE_OP_ROLL_LEFT = 2
    QTE_OP_ROLL_RIGHT = 3
    QTE_OP_JUMP = 4

    def _isInQTE(self):
        return self.qteId > 0

    def enterQTE(self, qteId, tgtId):
        global OP_LIST
        data = QTED.data.get(qteId, None)
        if not data:
            return
        else:
            if self.fashion != None and self.touchAirWallProcess != 1:
                self.fashion.breakJump()
                self.fashion.breakFall()
            if self.autoSkill:
                self.autoSkill.switchToKeyboardMode()
                self.autoSkill.stop()
            if self.ap != None:
                self.ap.stopMove()
                self.ap.stopAutoMove()
            scrollRange = data.get('scrollRange', 0)
            if scrollRange:
                scrollRange = limit(scrollRange, gameglobal.rds.cam.MIN_DIS, gameglobal.rds.cam.MAX_DIS)
                self.oldScrollNum = gameglobal.rds.cam.currentScrollNum
                gameglobal.rds.cam.setScrollRange((scrollRange, scrollRange))
            faceToTgt = data.get('faceToTgt', 0)
            tgt = BigWorld.entities.get(tgtId)
            if faceToTgt and tgt:
                self.faceToDirWidthCamera((tgt.position - self.position).yaw)
            qteAction = data.get('qteAct', None)
            if qteAction:
                self.fashion.playAction([qteAction], action.UNKNOWN_ACTION)
            gameglobal.rds.ui.enterQTE(qteId)
            OP_LIST.add(qteId)
            return

    def endQTE(self, qteId, succ):
        gameglobal.rds.ui.endQTE(qteId)
        self.resetCamera()
        if hasattr(self, 'oldScrollNum'):
            gameglobal.rds.cam.scrollToNum(self.oldScrollNum)
        if qteId in OP_LIST:
            self.onQTEResult(qteId, succ)

    def uploadQTEInfo(self, qteId, succ):
        self.cell.uploadQTEInfo(qteId, succ)

    def onQTEResult(self, qteId, succ):
        data = QTED.data.get(qteId, None)
        if not data:
            return
        else:
            if succ:
                op, opArgs = data.get('opSucc', (0, ()))
            else:
                op, opArgs = data.get('opFail', (0, ()))
            if op == ImpQte.QTE_OP_ACTION:
                actName = opArgs[0]
                if actName:
                    self.fashion.playAction([actName], action.UNKNOWN_ACTION)
            elif op == ImpQte.QTE_OP_ROLL_LEFT:
                self.ap.leftDodge(True)
            elif op == ImpQte.QTE_OP_ROLL_RIGHT:
                self.ap.rightDodge(True)
            elif op == ImpQte.QTE_OP_JUMP:
                self.ap.realJumpUp(True)
            OP_LIST.discard(qteId)
            return
