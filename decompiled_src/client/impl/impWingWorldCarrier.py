#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impWingWorldCarrier.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
from callbackHelper import Functor
from data import sys_config_data as SYSCD

class ImpWingWorldCarrier(object):

    def beExchangeWingWorldCarrierSeat(self, operateNUID, applyPlayerName):
        multiCarrierMemberExchagneSeatConfirmMsg = SYSCD.data.get('multiCarrierMemberExchagneSeatConfirmMsg', gameStrings.TEXT_IMPMULTICARRIER_20) % applyPlayerName
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(multiCarrierMemberExchagneSeatConfirmMsg, yesCallback=Functor(self._approveApplyExchangeWingWorldCarrier, operateNUID), noCallback=Functor(self._disapproveApplyExchangeWingWorldCarrier, operateNUID))

    def _approveApplyExchangeWingWorldCarrier(self, operateNUID):
        BigWorld.player().cell.agreeExchangeWingWorldCarrierSeat(operateNUID)

    def _disapproveApplyExchangeWingWorldCarrier(self, operateNUID):
        BigWorld.player().cell.refuseExchangeWingWorldCarrierSeat(operateNUID)
