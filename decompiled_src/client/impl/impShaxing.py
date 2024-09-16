#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impShaxing.o
import BigWorld
import gameglobal
from cdata import game_msg_def_data as GMDD

class ImpShaxing(object):

    def pushShaXingResult(self, result):
        gameglobal.rds.ui.shaXing.showShaXingResult(result)

    def shaxingSignupSucc(self, delayTime):
        self.showGameMsg(GMDD.data.SHAXING_SIGNUP_SUCC, ())
        if self == BigWorld.player():
            self.showShaXingWaitMsgBox(delayTime)

    def shaxingChooseGroupFail(self):
        self.showGameMsg(GMDD.data.SHAXING_CHOOSE_GROUP_FAIL, ())
        if self == BigWorld.player():
            self.hideShaXingWaitMsgBox()
            self.showChooseGroupFailMsgBox()
