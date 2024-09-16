#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/activitySaleGiftBagProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiUtils
import const
import utils
from uiProxy import UIProxy
from Scaleform import GfxValue
from gameclass import ClientMallVal as cmv
from data import mall_item_data as MID
from data import sys_config_data as SCD
from data import consumable_item_data as CID
from data import bonus_set_data as BSD
from data import mall_config_data as MCFD

class ActivitySaleGiftBagProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ActivitySaleGiftBagProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerMc': self.onRegisterMc,
         'unRegisterMc': self.onUnRegisterMc,
         'getRewardData': self.onGetRewardData,
         'setRewardIndex': self.onSetRewardIndex,
         'openChargeWindow': self.onOpenChargeWindow,
         'getCurCoin': self.onGetCurCoin}
        self.panelMc = None
        self.mallIdArr = SCD.data.get('isGiftBagMallId', [20045,
         20035,
         20046,
         20036])

    def onRegisterMc(self, *arg):
        self.panelMc = arg[3][0]

    def onUnRegisterMc(self, *arg):
        self.panelMc = None

    def _getItemData(self, mallId):
        p = BigWorld.player()
        ret = {}
        itemId = MID.data.get(mallId, {}).get('itemId', 0)
        ret['itemSlot'] = uiUtils.getGfxItemById(itemId)
        ret['itemName'] = MID.data.get(mallId, {}).get('itemName', '')
        ret['itemPrice'] = MID.data.get(mallId, {}).get('originalPrice', 0)
        ret['itemPriceSale'] = MID.data.get(mallId, {}).get('priceVal', 0)
        ret['itemPriceStr'] = gameStrings.TEXT_ACTIVITYSALEGIFTBAGPROXY_47 + str(MID.data.get(mallId, {}).get('originalPrice', 0))
        ret['itemPriceSaleStr'] = gameStrings.TEXT_ACTIVITYSALEGIFTBAGPROXY_48 + str(MID.data.get(mallId, {}).get('priceVal', 0))
        ret['itemLimitDesc'] = gameStrings.TEXT_ACTIVITYSALEGIFTBAGPROXY_49 % MID.data.get(mallId, {}).get('totalLimit', 0)
        ret['slotArray'] = self._getSlotArray(MID.data.get(mallId, {}).get('showItems', []))
        ret['buyBtnEnable'] = self.hasLimited(mallId)
        ret['discountLabelText'] = self._getDiscountLabelText(ret['itemPriceSale'], ret['itemPrice'])
        if ret['buyBtnEnable']:
            ret['buyBtnText'] = gameStrings.TEXT_ACTIVITYSALEGIFTBAGPROXY_54
        else:
            ret['buyBtnText'] = gameStrings.TEXT_ACTIVITYSALEGIFTBAGPROXY_56
        return ret

    def _getDiscountLabelText(self, itemPriceSale, itemPrice):
        rate = int(round(itemPriceSale * 100 / float(itemPrice)))
        mainRate = int(rate / 10.0)
        mainText = str(mainRate)
        subRate = int(rate - mainRate * 10.0)
        if subRate > 0:
            subText = '.' + str(subRate) + gameStrings.TEXT_ACTIVITYSALEGIFTBAGPROXY_65
        else:
            subText = gameStrings.TEXT_ACTIVITYSALEGIFTBAGPROXY_65
        return (mainText, subText)

    def _getSlotArray(self, itemArray):
        ret = []
        for itemId in itemArray:
            ret.append(uiUtils.getGfxItemById(itemId))

        return ret

    def _getBonusItems(self, mallId):
        ret = []
        itemId = MID.data.get(mallId, {}).get('itemId', 0)
        setId = CID.data.get(itemId, {}).get('itemSetInfo', ())[0]
        for i in BSD.data.get(setId, []):
            ret.append(i.get('bonusId', 0))

        return ret

    def onGetRewardData(self, *arg):
        ret = []
        for mallId in self.mallIdArr:
            ret.append(self._getItemData(mallId))

        return uiUtils.array2GfxAarry(ret, True)

    def onSetRewardIndex(self, *arg):
        p = BigWorld.player()
        index = int(arg[3][0].GetNumber())
        gameglobal.rds.ui.activitySaleBuy.show(self.mallIdArr[index], 'limit', 1)

    def hasLimited(self, mallId):
        p = BigWorld.player()
        totalLimit = MID.data.get(mallId, {}).get('totalLimit', 0)
        leftNum = totalLimit - p.mallInfo.get(mallId, cmv()).nTotal
        if leftNum:
            return True
        else:
            return False

    def onOpenChargeWindow(self, *arg):
        BigWorld.player().openRechargeFunc()

    def onGetCurCoin(self, *arg):
        p = BigWorld.player()
        tianbi = p.unbindCoin + p.bindCoin + p.freeCoin
        return GfxValue(tianbi)

    def refreshPanel(self):
        if self.panelMc:
            self.panelMc.Invoke('refreshPanel')
        gameglobal.rds.ui.activitySale.refreshInfo()

    def canGained(self):
        p = BigWorld.player()
        for mallid in self.mallIdArr:
            if mallid == 20045:
                if p.lv < 40 and self.hasLimited(mallid):
                    return True
            elif self.hasLimited(mallid):
                return True

        return False

    def canOpenTab(self):
        duration = MCFD.data.get('giftBagDuration', 60) * const.TIME_INTERVAL_DAY
        if not gameglobal.rds.configData.get('enableNewPlayerActivity', False):
            offset = utils.getNow() - utils.getServerOpenTime()
        else:
            p = BigWorld.player()
            offset = utils.getNow() - p.firstEnterWorldTimeOfCell
        if offset < duration and self.canGained():
            if gameglobal.rds.configData.get('enableNewPlayerActivity', False):
                if utils.isActivitySaleNewPlayer():
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False
