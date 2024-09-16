#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impActivityCollect.o
import gamelog
import gametypes
import gameglobal
from callbackHelper import Functor
from guis import uiConst
from guis import uiUtils
from cdata import game_msg_def_data as GMDD
MAX_CHOOSE_NUM = 8

class ImpActivityCollect(object):

    def onSyncActivityCollect(self):
        """
        \xe9\x9b\x86\xe7\xbb\x93\xe6\xb4\xbb\xe5\x8a\xa8\xe6\xaf\x8f\xe6\x97\xa5\xe7\xac\xac\xe4\xb8\x80\xe6\xac\xa1\xe7\x99\xbb\xe5\xbd\x95\xe6\x8e\xa8\xe9\x80\x81\xe5\x87\xbd\xe6\x95\xb0
        :return:
        """
        gameglobal.rds.ui.activitySaleCollect.pushCollectMessage()

    def onReceiveActivityCollectReward(self, ret):
        """
        \xe9\xa2\x86\xe5\x8f\x96\xe9\x9b\x86\xe7\xbb\x93\xe6\xb4\xbb\xe5\x8a\xa8\xe5\xa5\x96\xe5\x8a\xb1\xe8\xbf\x94\xe5\x9b\x9e\xe5\x87\xbd\xe6\x95\xb0
        :param ret:
        :return:
        """
        gamelog.info('@zmm onReceiveActivityCollectReward', ret)
        if ret == gametypes.ACTIVITY_COLLECT_PROGRESS_REWARD_FAIL_BY_TIME_INVALID:
            self.showGameMsg(GMDD.data.ACTIVITY_COLLECT_PROGRESS_REWARD_FAILED_BY_TIME_INVALID, ())
        elif ret == gametypes.ACTIVITY_COLLECT_PROGRESS_REWARD_FAIL:
            self.showGameMsg(GMDD.data.ACTIVITY_COLLECT_PROGRESS_REWARD_FAILED, ())
        elif ret == gametypes.ACTIVITY_COLLECT_PROGRESS_REWARD_FAIL_BY_INV_FULL:
            self.showGameMsg(GMDD.data.ACTIVITY_COLLECT_PROGRESS_REWARD_FAILED_BY_INV_FULL, ())
        elif ret == gametypes.ACTIVITY_COLLECT_PROGRESS_REWARD_SUC:
            self.showGameMsg(GMDD.data.ACTIVITY_COLLECT_PROGRESS_REWARD_SUCCESS, ())
            gameglobal.rds.ui.activitySaleCollect.refreshBonusInfo()
            return
