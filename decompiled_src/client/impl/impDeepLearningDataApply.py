#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impDeepLearningDataApply.o
import BigWorld
import gametypes
import gameglobal
import gamelog
from cdata import game_msg_def_data as GMDD

class ImpDeepLearningDataApply(object):

    def queryDeepLearningPushInfo(self):
        self.cell.queryDeepLearningPushInfo()

    def OnDeepLearningPushInfo(self, info):
        gamelog.debug('@yj OnDeepLearningPushInfo', info)
        self.deepLearningData = info
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
        gameglobal.rds.ui.deepLearningShop.refreshInfo()
        gameglobal.rds.ui.deepLearningShop.checkTimeDownPush()
        if not getattr(info, 'firstPush', 1):
            gameglobal.rds.ui.deepLearningShop.show()

    def onBuyDeepLearningPushItemFailed(self, result):
        gamelog.debug('@yj onBuyDeepLearningPushItemFailed ', result)
        p = BigWorld.player()
        if result == gametypes.DEEP_LEARNING_DATA_APPLY_BUY_ITEM_FAIL_NO_SHOP:
            p.showGameMsg(GMDD.data.DEEP_LEARNING_BUY_ITEM_FAIL_NO_SHOP, ())
        elif result == gametypes.DEEP_LEARNING_DATA_APPLY_BUY_ITEM_FAIL_NO_ITEM:
            p.showGameMsg(GMDD.data.DEEP_LEARNING_BUY_ITEM_FAIL_NO_ITEM, ())
        elif result == gametypes.DEEP_LEARNING_DATA_APPLY_BUY_ITEM_FAIL_BUY_LIMIT:
            p.showGameMsg(GMDD.data.DEEP_LEARNING_BUY_ITEM_FAIL_BUY_LIMIT, ())
