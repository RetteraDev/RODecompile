#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impGroupPurchase.o
import copy
import BigWorld
import gametypes
import gamelog
import gameglobal
from cdata import game_msg_def_data as GMDD

class ImpGroupPurchase(object):

    def onSyncPreOrderActivity(self):
        gamelog.info('@zmm onSyncPreOrderActivity')
        gameglobal.rds.ui.activitySaleGroupBuy.pushPreOrderMessage()

    def onSyncGroupPurchaseActivity(self):
        gamelog.info('@zmm onSyncGroupPurchaseActivity')
        gameglobal.rds.ui.activitySaleGroupBuy.pushGroupBuyMessage()

    def onPreOrderItem(self, ret):
        gamelog.info('@zmm onGetBackActivityReward', ret)
        if ret == gametypes.PRE_ORDER_ITEM_SUC:
            self.showGameMsg(GMDD.data.PRE_ORDER_ITEM_SUCCESS, ())
            if gameglobal.rds.ui.activitySaleGroupBuy.widget:
                gameglobal.rds.ui.activitySaleGroupBuy.refreshPanel()
            gameglobal.rds.ui.activitySaleGroupBuyConfirm.hide()
        elif ret == gametypes.PRE_ORDER_ITEM_FAIL_BY_INV_LOCK:
            self.showGameMsg(GMDD.data.ITEM_INV_LOCKED, ())
        elif ret == gametypes.PRE_ORDER_ITEM_FAIL_BY_NOT_INVALID_TIME:
            self.showGameMsg(GMDD.data.PRE_ORDER_ITEM_FAILED_BY_NOT_INVALID_TIME, ())
        elif ret == gametypes.GROUP_PURCHASE_ITEM_FAIL_BY_MAX:
            self.showGameMsg(GMDD.data.PRE_ORDER_ITEM_NUMS_LIMIT, ())
        else:
            self.showGameMsg(GMDD.data.PRE_ORDER_ITEM_FAILED, ())

    def onGroupPurchaseItem(self, ret):
        gamelog.info('@zmm onGetBackActivityReward', ret)
        if ret == gametypes.GROUP_PURCHASE_ITEM_SUC:
            self.showGameMsg(GMDD.data.GROUP_PURCHASE_ITEM_SUCCESS, ())
            if gameglobal.rds.ui.activitySaleGroupBuy.widget:
                gameglobal.rds.ui.activitySaleGroupBuy.refreshPanel()
            gameglobal.rds.ui.activitySaleGroupBuyConfirm.hide()
        elif ret == gametypes.GROUP_PURCHASE_ITEM_FAIL_BY_INV_LOCK:
            self.showGameMsg(GMDD.data.ITEM_INV_LOCKED, ())
        elif ret == gametypes.PRE_ORDER_ITEM_FAIL_BY_NOT_INVALID_TIME:
            self.showGameMsg(GMDD.data.GROUP_PURCHASE_ITEM_FAILED_BY_NOT_INVALID_TIME, ())
        elif ret == gametypes.GROUP_PURCHASE_ITEM_FAIL_BY_INV_FULL:
            self.showGameMsg(GMDD.data.ITEM_GET_BAG_FULL, ())
        elif ret == gametypes.GROUP_PURCHASE_ITEM_FAIL_BY_MAX:
            self.showGameMsg(GMDD.data.GROUP_PURCHASE_ITEM_NUMS_LIMIT, ())
        else:
            self.showGameMsg(GMDD.data.GROUP_PURCHASE_ITEM_FAILED, ())

    def set_preOrderInfo(self, old):
        if gameglobal.rds.ui.activitySaleGroupBuy.widget:
            gameglobal.rds.ui.activitySaleGroupBuy.refreshPanel()
