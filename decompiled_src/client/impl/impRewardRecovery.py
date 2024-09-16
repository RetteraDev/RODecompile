#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impRewardRecovery.o
from gamestrings import gameStrings
import copy
import BigWorld
import gametypes
import gamelog
import gameglobal
from guis import uiUtils
from callbackHelper import Functor
from rewardRecovery import RewardRecoveryActivity, ActivityDayVal
from data import reward_getback_data as RGD
from cdata import game_msg_def_data as GMDD

class ImpRewardRecovery(object):

    def onSendRewardRecoveryActivity(self, dto):
        if not hasattr(self, 'rewardRecoveryActivity'):
            self.rewardRecoveryActivity = RewardRecoveryActivity()
        for activityId, detailInfo in dto:
            activityType = RGD.data.get(activityId, {}).get('activityType', 0)
            activity = self.rewardRecoveryActivity.getActivity(activityType)
            if not activity:
                gamelog.error('@jbx: activity None', activityType)
                continue
            activityId, getBackRewardTime, subChildList = detailInfo
            activity.activityId = activityId
            activity.getBackRewardTime = getBackRewardTime
            oldVal = activity.daysVal
            activity.daysVal = {}
            for subChild in subChildList:
                tWhen, lv, cnt, extra = subChild
                if tWhen in oldVal and extra.get('time', 0) < oldVal[tWhen].extra.get('time', 0):
                    activity.daysVal[tWhen] = ActivityDayVal(oldVal[tWhen].lv, oldVal[tWhen].cnt, oldVal[tWhen].extra)
                else:
                    c = ActivityDayVal()
                    activity.daysVal[tWhen] = c
                    c.extra = copy.deepcopy(extra)
                    c.lv = lv
                    c.cnt = cnt

        gameglobal.rds.ui.welfare.refreshInfo()
        gameglobal.rds.ui.welfareRewardRecovery.refreshInfo()

    def onProxySendRewardRecoveryActivity(self, dto):
        if not hasattr(self, 'rewardRecoveryActivity'):
            self.rewardRecoveryActivity = RewardRecoveryActivity()
        for activityType, detailInfo in dto:
            activity = self.rewardRecoveryActivity.getActivity(activityType)
            if not activity:
                gamelog.error('@jbx: activity None', activityType)
                continue
            activityId, getBackRewardTime, subChildList = detailInfo
            activity.activityId = activityId
            activity.getBackRewardTime = getBackRewardTime
            activity.daysVal = {}
            for subChild in subChildList:
                tWhen, lv, cnt, extra = subChild
                c = ActivityDayVal()
                activity.daysVal[tWhen] = c
                c.extra = copy.deepcopy(extra)
                c.lv = lv
                c.cnt = cnt

        gameglobal.rds.ui.welfare.refreshInfo()
        gameglobal.rds.ui.welfareRewardRecovery.refreshInfo()
        gameglobal.rds.ui.welfareRewardRecovery.addPushIcon()

    def onGetBackActivityReward(self, ret):
        gamelog.info('@zmm onGetBackActivityReward', ret)
        if ret == gametypes.GET_BACK_ACTIVITY_REWARD_SUC:
            self.showGameMsg(GMDD.data.GET_BACK_ACTIVITY_REWARD_SUCCESS, ())
        elif ret == gametypes.GET_BACK_ACTIVITY_REWARD_FAIL_BY_NO_EXIST:
            self.showGameMsg(GMDD.data.GET_BACK_REWARD_NOT_EXIST, ())
        elif ret == gametypes.GET_BACK_ACTIVITY_REWARD_FAIL_BY_EXP_FULL:
            self.showGameMsg(GMDD.data.QUEST_LOOP_CHAIN_GET_BACK_EXP_FULL, ())
        elif ret == gametypes.GET_BACK_ACTIVITY_REWARD_FAIL_BY_INV_LOCK:
            self.showGameMsg(GMDD.data.ITEM_INV_LOCKED, ())
        elif ret == gametypes.GET_BACK_ACTIVITY_REWARD_FAIL_BY_INV_FULL:
            self.showGameMsg(GMDD.data.ITEM_GET_BAG_FULL, ())
        elif ret == gametypes.GET_BACK_ACTIVITY_REWARD_FAIL_BY_NOT_ENOUGH_FAME1:
            self.showGameMsg(GMDD.data.QUEST_LOOP_CHAIN_GET_BACK_EXP_NOT_ENOUGH_FAME1, ())
        elif ret == gametypes.GET_BACK_ACTIVITY_REWARD_FAIL_BY_NOT_ENOUGH_FAME2:
            self.showGameMsg(GMDD.data.QUEST_LOOP_CHAIN_GET_BACK_EXP_NOT_ENOUGH_FAME2, ())
        elif ret == gametypes.GET_BACK_ACTIVITY_REWARD_FAIL_BY_NOT_IN_VALID_TIME:
            self.showGameMsg(GMDD.data.GET_BACK_REWARD_NOT_IN_VALID_TIME, ())
        else:
            self.showGameMsg(GMDD.data.GET_BACK_ACTIVITY_REWARD_FAILED, ())

    def confirmGetBackActivityReward(self, tp, activityId):
        gamelog.debug('@zmm confirmGetBackActivityReward')
        msg = uiUtils.getTextFromGMD(GMDD.data.REWARD_GET_BACK_EXP_CHECK, '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self._doConfirmGetBackActivityReward, tp, activityId), yesBtnText=gameStrings.TEXT_AVOIDDOINGACTIVITYTIPPROXY_128, noBtnText=gameStrings.TEXT_PLAYRECOMMPROXY_494_1)

    def _doConfirmGetBackActivityReward(self, tp, activityId):
        gamelog.debug('@zmm _doConfirmGetBackActivityReward')
        self.base.getBackActivityRewardWithoutExpCheck(tp, activityId, gametypes.GET_BACK_ACTIVITY_REWARD_WITHOUT_EXP_CHECK)

    def confirmGetCatchUpActivityReward(self, activityId, catchUpNum, type):
        gamelog.debug('@zmm confirmGetCatchUpActivityReward')
        if type == gametypes.GET_BACK_ACTIVITY_REWARD_EXP_CHECK:
            msg = uiUtils.getTextFromGMD(GMDD.data.REWARD_GET_BACK_EXP_CHECK, '')
        else:
            msg = uiUtils.getTextFromGMD(GMDD.data.REWARD_GET_BACK_FAME_CHECK, '')
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, Functor(self._doConfirmGetCatchUpActivityReward, activityId, catchUpNum, type), yesBtnText=gameStrings.TEXT_AVOIDDOINGACTIVITYTIPPROXY_128, noBtnText=gameStrings.TEXT_PLAYRECOMMPROXY_494_1)

    def _doConfirmGetCatchUpActivityReward(self, activityId, catchUpNum, type):
        gamelog.debug('@zmm _doConfirmGetCatchUpActivityReward')
        if type == gametypes.GET_BACK_ACTIVITY_REWARD_EXP_CHECK:
            self.cell.getCatchUpActivityReward(activityId, catchUpNum, gametypes.GET_BACK_ACTIVITY_REWARD_WITHOUT_EXP_CHECK, gametypes.GET_BACK_ACTIVITY_REWARD_WITH_FAME_CHECK)
        else:
            self.cell.getCatchUpActivityReward(activityId, catchUpNum, gametypes.GET_BACK_ACTIVITY_REWARD_WITHOUT_EXP_CHECK, gametypes.GET_BACK_ACTIVITY_REWARD_WITHOUT_FAME_CHECK)

    def onGetCatchUpActivityReward(self, ret):
        """
        \xe9\xa2\x86\xe5\x8f\x96\xe8\x90\xbd\xe6\x88\xb7\xe6\x9c\x8d\xe5\xa5\x96\xe5\x8a\xb1\xe8\xbf\xbd\xe8\xb5\xb6\xe5\xa5\x96\xe5\x8a\xb1\xe8\xbf\x94\xe5\x9b\x9e\xe5\x87\xbd\xe6\x95\xb0
        :param ret:
        :return:
        """
        gamelog.debug('@zmm onGetCatchUpActivityReward')
        gameglobal.rds.ui.welfareRewardCatchUp.refreshInfo()
        gameglobal.rds.ui.catchUpDetail.refreshInfo()
        gameglobal.rds.ui.catchUpDetail.hide()

    def onSyncRewardCatchUp(self):
        gamelog.debug('@zmm onSyncRewardCatchUp')
        gameglobal.rds.ui.welfareRewardCatchUp.addPushIcon()
