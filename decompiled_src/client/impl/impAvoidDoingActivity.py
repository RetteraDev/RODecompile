#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impAvoidDoingActivity.o
import gamelog
import gametypes
import gameglobal
from avoidDoingActivity import AvoidDoingActivity
from callbackHelper import Functor
from guis import uiConst
from guis import uiUtils
from cdata import game_msg_def_data as GMDD
from data import avoid_doing_activity_data as ADAD
from data import sys_config_data as SCD

class ImpAvoidDoingActivity(object):

    def onSendAvoidDoingActivity(self, dto):
        gamelog.debug('@zmm onSendAvoidDoingActivity', dto)
        if not hasattr(self, 'avoidDoingActivity'):
            self.avoidDoingActivity = AvoidDoingActivity()
        for activityType, detailInfo in dto:
            activity = self.avoidDoingActivity.getActivity(activityType)
            if not activity:
                gamelog.error('@ljb: activity None', activityType)
                continue
            activityKey, avoidDoneCount = detailInfo
            activity.activityKey = activityKey
            activity.avoidDoneCount = avoidDoneCount

        gameglobal.rds.ui.avoidDoingActivity.initUI()

    def onAvoidDoingActivityRequest(self, ret):
        gamelog.debug('@zmm onAvoidDoingActivityRequest', ret)
        gamelog.info('@zmm onAvoidDoingActivityRequest', ret)
        if ret == gametypes.AVOID_DOING_ACTIVITY_SUC:
            self.showGameMsg(GMDD.data.AVOID_DOING_ACTIVITY_SUCCSESS, ())
        elif ret == gametypes.AVOID_DOING_ACTIVITY_FAIL_BY_INV_LOCK:
            self.showGameMsg(GMDD.data.ITEM_INV_LOCKED, ())
        elif ret == gametypes.AVOID_DOING_ACTIVITY_FAIL_BY_INV_FULL:
            self.showGameMsg(GMDD.data.ITEM_GET_BAG_FULL, ())
        elif ret == gametypes.AVOID_DOING_ACTIVITY_FAIL_BY_NOT_ENOUGH_COMBAT_SCORE:
            self.showGameMsg(GMDD.data.AVOID_DOING_ACTIVITY_FAILED_BY_NOT_ENOUGH_COMBAT_SCORE, ())
        elif ret == gametypes.AVOID_DOING_ACTIVITY_FAIL_BY_NOT_ENOUGH_FREE_CREDITS:
            self.showGameMsg(GMDD.data.AVOID_DOING_ACTIVITY_FAILED_BY_NOT_ENOUGH_FREE_CREDITS, ())
