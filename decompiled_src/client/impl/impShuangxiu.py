#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impShuangxiu.o
from gamestrings import gameStrings
import BigWorld
import Math
import utils
import gameglobal
import const
from callbackHelper import Functor
from helpers import action
from guis import uiUtils
from data import shuangxiu_config_data as SCD
from cdata import game_msg_def_data as GMDD

class ImpShuangxiu(object):

    def onApplyShuangxiu(self, srcId):
        ent = BigWorld.entities.get(srcId)
        if ent:
            msg = uiUtils.getTextFromGMD(GMDD.data.SHUANGXIU_APPLY_CONFIRM_MSG, gameStrings.TEXT_IMPSHUANGXIU_21) % ent.roleName
            gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, yesCallback=Functor(self.applyShuangxiuConfirmed, srcId, True), yesBtnText=gameStrings.TEXT_IMPSHUANGXIU_24, noCallback=Functor(self.applyShuangxiuConfirmed, srcId, False), noBtnText=gameStrings.TEXT_IMPSHUANGXIU_26)

    def isInShuangxiu(self):
        if not self.shuangxiuInfo:
            return False
        if self.id == self.shuangxiuInfo[0]:
            return True
        return False

    def isInBeShuangxiu(self):
        if not self.shuangxiuInfo:
            return False
        if self.gbId == self.shuangxiuInfo[3]:
            return True
        return False

    def getShuangxiuStartAction(self):
        if self.isInShuangxiu():
            return SCD.data.get('shuangxiuStartAction', '75501')
        else:
            return SCD.data.get('beShuangxiuStartAction', '76501')

    def getShuangxiuLoopAction(self):
        if self.isInShuangxiu():
            return SCD.data.get('shuangxiuLoopAction', '75502')
        else:
            return SCD.data.get('beShuangxiuLoopAction', '76502')

    def getShuangxiuEndAction(self):
        if self.isInShuangxiu():
            return SCD.data.get('shuangxiuEndAction', '75503')
        else:
            return SCD.data.get('beShuangxiuEndAction', '76503')

    def getShuangxiuLoopEffect(self):
        if self.isInShuangxiu():
            return SCD.data.get('shuangxiuLoopEffect', (30410,))
        else:
            return SCD.data.get('beShuangxiuLoopEffect', (30411,))

    def playShuangxiuStart(self):
        shuangxiuStartAction = self.getShuangxiuStartAction()
        shuangxiuLoopAction = self.getShuangxiuLoopAction()
        shuangxiuLoopEffect = self.getShuangxiuLoopEffect()
        blend = True
        keep = True
        playSeq = []
        playSeq.append((shuangxiuStartAction,
         None,
         action.SHUANGXIU_ACTION,
         0,
         1.0,
         None))
        playSeq.append((shuangxiuLoopAction,
         shuangxiuLoopEffect,
         action.SHUANGXIU_ACTION,
         0,
         1.0,
         None))
        self.fashion.playActionWithFx(playSeq, action.SHUANGXIU_ACTION, None, blend, None, keep, priority=self.getSkillEffectPriority())

    def playShuangxiuEnd(self):
        self.fashion.stopAllActions()
        shuangxiuEndAction = self.getShuangxiuEndAction()
        if not self.inMoving():
            blend = True
            keep = True
            playSeq = []
            playSeq.append((shuangxiuEndAction,
             None,
             action.SHUANGXIU_END_ACTION,
             0,
             1.0,
             None))
            self.fashion.playActionWithFx(playSeq, action.SHUANGXIU_END_ACTION, None, blend, None, keep, priority=self.getSkillEffectPriority())

    def shuangxiuGotoRightPosition(self):
        if self == BigWorld.player():
            src = BigWorld.entities.get(self.shuangxiuInfo[0])
            if src:
                dist = SCD.data.get('relativeShuangxiuDist', 1)
                destPos = Math.Vector3(utils.getRelativePosition(src.position, src.yaw, 0, dist))
                BigWorld.player().ap.seekPath(destPos, Functor(self.shuangxiuArriveRightPosition, src))

    def shuangxiuArriveRightPosition(self, src, suc):
        if not src or not src.inWorld:
            return
        dist = SCD.data.get('relativeShuangxiuDist', 1)
        destPos = Math.Vector3(utils.getRelativePosition(src.position, src.yaw, 0, dist))
        BigWorld.player().ap.seekPath(destPos, Functor(self.shuangxiuArriveCallback, src))
        self.shuangxiuArriveCallback(src, True)

    def shuangxiuArriveCallback(self, src, ret):
        self.ap.forwardMagnitude = 0
        self.ap.updateMoveControl()
        BigWorld.callback(0.1, Functor(self.shuangxiuFaceSrc, src))

    def shuangxiuFaceSrc(self, src):
        self.faceTo(src)
        self.ap.restore()

    def set_shuangxiuInfo(self, old):
        if self.shuangxiuInfo:
            if self == BigWorld.player():
                if hasattr(self, 'getOperationMode') and self.getOperationMode() == gameglobal.ACTION_MODE:
                    self.ap.stopMove()
                    self.ap.restore(False)
        if self.isInShuangxiu() or self.isInBeShuangxiu():
            self.playShuangxiuStart()
            if self.isInBeShuangxiu():
                self.shuangxiuGotoRightPosition()
        if old and (not self.isInShuangxiu() or not self.isInBeShuangxiu()):
            self.playShuangxiuEnd()
            if self == BigWorld.player():
                self.ap.reset()

    def cancelShuangxiu(self):
        if self.isInShuangxiu() or self.isInBeShuangxiu():
            self.cell.cancelShuangxiu()

    def applyShuangxiu(self, tgtId):
        if not self.stateMachine.checkStatus(const.CT_SHUANGXIU):
            return
        self.cell.applyShuangxiu(tgtId)

    def useShuangxiuSkill(self):
        if not gameglobal.rds.configData.get('enableShuangxiu', False):
            return
        if not self.targetLocked or not self.targetLocked.IsAvatar or self.targetLocked == self:
            self.showGameMsg(GMDD.data.NO_SHUANGXIU_TARGET, ())
            return
        self.applyShuangxiu(self.targetLocked.id)

    def applyShuangxiuConfirmed(self, srcId, accept):
        if not self.stateMachine.checkStatus(const.CT_SHUANGXIU):
            return
        self.cell.onApplyShuangxiuConfirmed(srcId, accept)
