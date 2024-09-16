#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impItemUseFeedback.o
import gamelog
import gametypes
import gameglobal
from callbackHelper import Functor
from guis import uiConst
from data import limit_time_feedback_data as LTFD
from cdata import game_msg_def_data as GMDD

class ImpItemUseFeedback(object):

    def onReceiveItemUseFeedbackReward(self, ret):
        gamelog.info('@zmm onReceiveItemUseFeedbackReward', ret)
        if ret == gametypes.ITEM_USE_FEEDBACK_AWARD_REC_SUC:
            self.showGameMsg(GMDD.data.RECEIVE_ITEM_USE_FEEDBACK_REWARD_SUC, ())
            self.cell.getItemUseData()
            self.cell.getItemUseRewardsData()
        elif ret == gametypes.ITEM_USE_FEEDBACK_FAIL_BY_INV_LOCK:
            self.showGameMsg(GMDD.data.ITEM_INV_LOCKED, ())
        elif ret == gametypes.ITEM_USE_FEEDBACK_FAIL_BY_INV_FULL:
            self.showGameMsg(GMDD.data.GET_ITEM_USE_FEEDBACK_BONUS_BY_MAILE, ())
        else:
            self.showGameMsg(GMDD.data.RECEIVE_ITEM_USE_FEEDBACK_REWARD_FAIL, ())

    def onGetItemUseInfo(self, data):
        self.paybackItemInfo = data
        gameglobal.rds.ui.activitySaleTimeLimitReward.refreshPanel()
        gameglobal.rds.ui.activitySale.refreshInfo()

    def onGetItemUseRewardsData(self, data):
        self.paybackItemUseReward = data
        gameglobal.rds.ui.activitySaleTimeLimitReward.refreshPanel()
        gameglobal.rds.ui.activitySale.refreshInfo()

    def onSendItemUsePushFlag(self, needPushFlags):
        """
        \xe9\x99\x90\xe6\x97\xb6\xe5\x9b\x9e\xe9\xa6\x88\xe6\xb4\xbb\xe5\x8a\xa8\xe9\xa6\x96\xe6\xac\xa1\xe5\xbc\x80\xe5\x90\xaf\xe6\x97\xb6\xef\xbc\x8c\xe4\xbc\x9a\xe5\x90\x91\xe7\x8e\xa9\xe5\xae\xb6\xe6\x8e\xa8\xe9\x80\x81\xe6\xb6\x88\xe6\x81\xaf\xef\xbc\x8c\xe8\xaf\xa5\xe5\x87\xbd\xe6\x95\xb0\xe7\x94\xa8\xe4\xba\x8e\xe6\x8d\x95\xe8\x8e\xb7\xe9\x99\x90\xe6\x97\xb6\xe5\x9b\x9e\xe9\xa6\x88\xe9\x9c\x80\xe8\xa6\x81\xe6\x8e\xa8\xe9\x80\x81\xe7\x9a\x84\xe6\xb4\xbb\xe5\x8a\xa8id\xe5\x88\x97\xe8\xa1\xa8
        :param needPushFlags: \xe9\x9c\x80\xe8\xa6\x81\xe6\x8e\xa8\xe9\x80\x81\xe9\x99\x90\xe6\x97\xb6\xe5\x9b\x9e\xe9\xa6\x88\xe6\xb4\xbb\xe5\x8a\xa8\xe7\x9a\x84id\xe5\x88\x97\xe8\xa1\xa8\xef\xbc\x8ceg\xe3\x80\x82[1, 2
        :return:
        """
        if not needPushFlags:
            return
        if not gameglobal.rds.configData.get('enableItemUseFeedback', False):
            return
        for activityId in needPushFlags:
            pushId = LTFD.data.get(activityId, {}).get('pushId', 0)
            gameglobal.rds.ui.pushMessage.addPushMsg(pushId)
            gameglobal.rds.ui.pushMessage.setCallBack(pushId, {'click': Functor(self.onClickPushItemUsePanel, pushId)})

    def onClickPushItemUsePanel(self, pushId):
        gameglobal.rds.ui.activitySale.show(uiConst.ACTIVITY_SALE_TIME_LIMIT_REWARD_1)
        gameglobal.rds.ui.pushMessage.removePushMsg(pushId)
