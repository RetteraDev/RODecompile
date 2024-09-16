#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impActivation.o
import gamelog
import gametypes
import gameglobal
from cdata import game_msg_def_data as GMDD

class ImpActivation(object):

    def onReceiveActivationReward(self, ret):
        gamelog.info('@szh onReceiveActivationReward', ret)
        if ret == gametypes.ACTIVATION_REC_SUC:
            self.showGameMsg(GMDD.data.RECEIVE_ACTIVATION_REWARD_SUC, ())
            gameglobal.rds.ui.playRecommActivation.refreshDailyActivation()
        elif ret == gametypes.ACTIVATION_REC_FAIL_BY_INV_LOCK:
            self.showGameMsg(GMDD.data.ITEM_INV_LOCKED, ())
        elif ret == gametypes.ACTIVATION_REC_FAIL_BY_INV_FULL:
            self.showGameMsg(GMDD.data.GET_ACTIVITY_BONUS_BY_MAIL, ())
        else:
            self.showGameMsg(GMDD.data.RECEIVE_ACTIVATION_REWARD_FAIL, ())

    def onReceiveWeekActivationReward(self, ret):
        if ret == gametypes.WEEK_ACTIVATION_REC_SUC:
            self.showGameMsg(GMDD.data.RECEIVE_WEEK_ACTIVATION_REWARD_SUC, ())
            gameglobal.rds.ui.playRecommActivation.refreshWeekActivation()
        elif ret == gametypes.WEEK_ACTIVATION_REC_FAIL_BY_INV_LOCK:
            self.showGameMsg(GMDD.data.ITEM_INV_LOCKED, ())
        elif ret == gametypes.WEEK_ACTIVATION_REC_FAIL_BY_INV_FULL:
            self.showGameMsg(GMDD.data.RECEIVE_WEEK_ACTIVATION_REC_FAIL_BY_INV_FULL, ())
        else:
            self.showGameMsg(GMDD.data.RECEIVE_WEEK_ACTIVATION_REWARD_FAIL, ())

    def onUpdateWeekPrivilegeBuyInfo(self, info):
        self.weekPrivilegeBuyInfo = info
        gameglobal.rds.ui.activitySale.refreshInfo()
        gameglobal.rds.ui.activitySaleWeekActivation.updateAfterTrunCardMc()

    def onUpdateOperationActivityInfo(self, info):
        self.weekOperationActivityInfo = info
        gameglobal.rds.ui.playRecommActivation.updateWeekActivationPushMsg()
        gameglobal.rds.ui.activitySale.refreshInfo()
        gameglobal.rds.ui.playRecommActivation.refreshOperatonRecommItems()
