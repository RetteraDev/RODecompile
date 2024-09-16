#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impMultiCarrier.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import gamelog
from guis import uiUtils
from data import sys_config_data as SYSCD

class ImpMultiCarrier(object):

    def beInviteCheckCarrierReady(self):
        multiCarrierLeaderInviteReadyConfirmMsg = SYSCD.data.get('multiCarrierLeaderInviteReadyConfirmMsg', gameStrings.TEXT_IMPMULTICARRIER_13)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(multiCarrierLeaderInviteReadyConfirmMsg, self._comfirmInviteCheckCarrierReady)

    def onUpdateEnterCarrier(self):
        pass

    def beApplyExchangeCarrierSeat(self, fRoleName):
        multiCarrierMemberExchagneSeatConfirmMsg = SYSCD.data.get('multiCarrierMemberExchagneSeatConfirmMsg', gameStrings.TEXT_IMPMULTICARRIER_20) % fRoleName
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(multiCarrierMemberExchagneSeatConfirmMsg, yesCallback=self._approveApplyExchangeCarrier, noCallback=self._disapproveApplyExchangeCarrier)

    def beApplyCreateCarrierByNpc(self, carrierNo):
        multiCarrierReadyConfirmMsg = SYSCD.data.get('multiCarrierReadyConfirmMsg', gameStrings.TEXT_IMPMULTICARRIER_24)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(multiCarrierReadyConfirmMsg, yesCallback=lambda : BigWorld.player().cell.applyCreateCarrierByNpc(carrierNo, False))

    def _comfirmInviteCheckCarrierReady(self):
        BigWorld.player().cell.comfirmCheckCarrierReady()

    def _approveApplyExchangeCarrier(self):
        BigWorld.player().cell.approveApplyExchangeCarrierSeat()

    def _disapproveApplyExchangeCarrier(self):
        BigWorld.player().cell.disapproveApplyExchangeCarrierSeat()

    def onReqCarrierPosition(self, spaceNo, position):
        gamelog.debug('cgy#onReqCarrierPosition: ', spaceNo, position)
        if not gameglobal.rds.ui.questTrack.needRestartFindPath(spaceNo, position):
            return
        uiUtils.findPosByPos(spaceNo, position)

    def beApplyEnterCarrierMajor(self):
        multiCarrierApplyEnterMajorMsg = SYSCD.data.get('multiCarrierApplyEnterMajorMsg', gameStrings.TEXT_IMPMULTICARRIER_44)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(multiCarrierApplyEnterMajorMsg, yesCallback=BigWorld.player().cell.applyEnterCarrierMajor)

    def beReqEnterCarrierMajor(self, gbId, roleName):
        multiCarrierReqEnterMajorMsg = SYSCD.data.get('multiCarrierReqEnterMajorMsg', gameStrings.TEXT_IMPMULTICARRIER_49) % roleName
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(multiCarrierReqEnterMajorMsg, yesCallback=lambda : BigWorld.player().cell.approveReqEnterCarrierMajor(gbId), noCallback=lambda : BigWorld.player().cell.refuseReqEnterCarrierMajor(gbId))

    def inMultiCarrier(self):
        return self.carrier and self.id in self.carrier
