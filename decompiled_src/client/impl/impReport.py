#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impReport.o
import gamelog
import gameglobal
import BigWorld
from guis import uiUtils
from cdata import game_msg_def_data as GMDD

class ImpReport(object):

    def onEvalFeedback(self, urs, aid):
        gamelog.debug('@hjx eval#onEvalFeedback:', self.id, urs, aid)
        gameglobal.rds.ui.inGameEvaluation.show(urs, aid)

    def onSubmitProblemSucc(self):
        gameglobal.rds.ui.customerServiceVip.hide()
        text = uiUtils.getTextFromGMD(GMDD.data.VIP_MSG_SEND_SUCCESS, '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(text)

    def onSubmitProblemFailed(self, errCode, errMsg):
        text = uiUtils.getTextFromGMD(GMDD.data.COMMON_MSG, '%s')
        text = text % errMsg
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(text)
