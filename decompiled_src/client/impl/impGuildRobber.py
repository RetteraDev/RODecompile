#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impGuildRobber.o
from gamestrings import gameStrings
import gameglobal
from callbackHelper import Functor

class ImpGuildRobber(object):

    def ApplyRobberChallengeConfirm(self, notMatchList, npcEntId):
        if len(notMatchList) <= 0:
            return
        msg = gameStrings.TEXT_IMPGUILDROBBER_10 % len(notMatchList)
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self.cell.onApplyRobberChallengeConfirmed, npcEntId), yesBtnText=gameStrings.TEXT_AVATAR_6426, noBtnText=gameStrings.TEXT_PLAYRECOMMPROXY_494_1, isModal=False, msgType='pushLoop', textAlign='center')
