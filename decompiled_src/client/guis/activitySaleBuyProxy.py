#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/activitySaleBuyProxy.o
from gamestrings import gameStrings
import BigWorld
import uiConst
import uiUtils
import gameglobal
from uiProxy import UIProxy
from guis import ui
from data import mall_config_data as MCD
from data import mall_item_data as MID
from data import sys_config_data as SCD
from cdata import game_msg_def_data as GMDD

class ActivitySaleBuyProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ActivitySaleBuyProxy, self).__init__(uiAdapter)
        self.modelMap = {'closeBuyConfirm': self.onCloseBuyConfirm,
         'confirmBuy': self.onConfirmBuy,
         'openChargeWindow': self.onOpenChargeWindow}
        self.mediator = None
        self.initData = {}
        self.mallIdArr = SCD.data.get('isActivitySaleMallId', [20023,
         20024,
         20025,
         20026])

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_ACTIVITY_SALE_BUY:
            self.mediator = mediator
            return uiUtils.dict2GfxDict(self.initData, True)

    def show(self, mallId, itemLabel, buyNumber):
        p = BigWorld.player()
        mallItemData = MID.data.get(mallId, {})
        itemId = mallItemData.get('itemId', 0)
        self.initData['itemLabel'] = itemLabel
        self.initData['buyNumber'] = buyNumber
        self.initData['itemName'] = mallItemData.get('itemName', 0)
        self.initData['priceValue'] = mallItemData.get('priceVal', 0)
        self.initData['priceType'] = mallItemData.get('priceType', 0)
        self.initData['limitStr'] = gameStrings.TEXT_ACTIVITYSALEBUYPROXY_45 + str(mallItemData.get('mallScoreLimit', 0))
        self.initData['limit'] = mallItemData.get('mallScoreLimit', 0)
        self.initData['slotInfo'] = uiUtils.getGfxItemById(itemId)
        self.initData['mallId'] = mallId
        self.initData['confirmBtnTip'] = ''
        if self.initData['priceType'] == uiConst.MONEY_TYPE_TIANBI:
            tianbi = p.unbindCoin + p.bindCoin + p.freeCoin
            self.initData['enableConfirmBtn'] = tianbi >= buyNumber * self.initData['priceValue']
            self.initData['confirmBtnTip'] = gameStrings.TEXT_ACTIVITYSALEBUYPROXY_53
        else:
            self.initData['enableConfirmBtn'] = True
        self.uiAdapter.loadWidget(uiConst.WIDGET_ACTIVITY_SALE_BUY)

    def clearWidget(self):
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_ACTIVITY_SALE_BUY)

    def reset(self):
        self.mediator = None
        self.initData = {}

    def onCloseBuyConfirm(self, *arg):
        self.clearWidget()

    @ui.checkInventoryLock()
    def onConfirmBuy(self, *arg):
        mallId = int(arg[3][0].GetNumber())
        p = BigWorld.player()
        if mallId == MCD.data.get('chargeLvReardMallId', 15024):
            p.base.buyChargeLvReward()
            self.onCloseBuyConfirm()
        else:
            mData = MID.data.get(mallId, {})
            minLv = mData.get('minLv', 0)
            maxLv = mData.get('maxLv', 0)
            if minLv > 0 and p.lv < minLv:
                p.showGameMsg(GMDD.data.MALL_BUY_MIN_LV, (minLv,))
                return
            if maxLv > 0 and p.lv > maxLv:
                p.showGameMsg(GMDD.data.MALL_BUY_MAX_LV, (maxLv,))
                return
            p.base.buyMallItems([mallId], [1], BigWorld.player().cipherOfPerson, 0, [False])

    def onOpenChargeWindow(self, *arg):
        BigWorld.player().openRechargeFunc()

    def onConfirmBuySuccess(self):
        if self.mediator:
            self.mediator.Invoke('showBuySuccessAnim')
        if gameglobal.rds.ui.inventory.tempBagMediator is None:
            gameglobal.rds.ui.inventory.show(tempPanel='mall')
