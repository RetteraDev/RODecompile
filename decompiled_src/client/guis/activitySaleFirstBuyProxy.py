#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/activitySaleFirstBuyProxy.o
import BigWorld
import gameglobal
import uiUtils
import const
import gametypes
import utils
from data import vip_package_data as VPD
from data import vip_service_data as VSD
from data import bonus_data as BD
from data import mall_config_data as MCFD
from data import mall_item_data as MID
from uiProxy import UIProxy
from guis import tianyuMallProxy as MALL
from guis import events

class ActivitySaleFirstBuyProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ActivitySaleFirstBuyProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerMc': self.onRegisterMc,
         'unRegisterMc': self.onUnRegisterMc,
         'openVipBasicPackageConfirm': self.onOpenVipBasicPackageConfirm,
         'gotoMall': self.onGotoMall,
         'gotoRecharge': self.onGotoRecharge}
        self.panelMc = None

    def onRegisterMc(self, *arg):
        self.panelMc = arg[3][0]
        self.getFrameInfo()
        self.addEvent(events.EVENT_VIP_INFO_UPDATE, self.getFrameInfo, isGlobal=True)
        self.addEvent(events.EVENT_VIP_INFO_UPDATE, self.refreshActivitySale, isGlobal=True)
        self.addEvent(events.EVENT_CASH_CHANGED, self.getFrameInfo, isGlobal=True)

    def onUnRegisterMc(self, *arg):
        self.panelMc = None

    def refreshActivitySale(self):
        gameglobal.rds.ui.activitySale.refreshInfo()

    def getFrameInfo(self):
        if not self.panelMc:
            return
        info = {}
        p = BigWorld.player()
        tianBi = p.unbindCoin + p.bindCoin + p.freeCoin
        info['tianBi'] = tianBi
        mallList = []
        firstBuy = False
        if not p.vipBasicPackage and MCFD.data.get('vipFirstBuyDaysList', {}) and MCFD.data.get('vipFirstBuyBasicPackage', 0):
            mid0 = MCFD.data.get('vipFirstBuyBasicPackage', -1)
            mallList.append(mid0)
            value = MCFD.data.get('vipValues', {}).get('value', ())
            firstBuy = True
            if len(value) > 0:
                mid1 = value[0][0]
                mallList.append(mid1)
        else:
            mid0 = self.confirmBuyMallId = MCFD.data.get('vipBasicPackage', -1)
            mallList.append(mid0)
        info['itemList'] = self.getItemList(mallList)
        isVIP, gainedAll = self.canGained(p)
        info['isVIP'] = isVIP
        info['gainedAll'] = gainedAll
        info['iconPath'] = 'activitySale/ActivitySaleFirstBuy.dds'
        info['firstBuy'] = firstBuy
        self.panelMc.Invoke('refreshFrame', uiUtils.dict2GfxDict(info))

    def getItemList(self, mallList):
        itemList = []
        for mallId in mallList:
            itemList.extend(self.getMallItems(mallId))

        return itemList

    def getMallItems(self, mallId):
        itemList = []
        mallData = MID.data.get(mallId, {})
        packageId = mallData.get('packageID', 0)
        serviceList = VPD.data.get(packageId, {}).get('serviceList', ())
        for sid in serviceList:
            svsData = VSD.data.get(sid, {})
            if svsData.get('serviceType', 1) != 2:
                continue
            if svsData.get('invalid', 0) == 1:
                continue
            bonusId = svsData.get('bonusId', 0)
            if bonusId == 0:
                continue
            bonusData = BD.data.get(bonusId, {})
            fixedBonus = bonusData.get('fixedBonus', ())
            if len(fixedBonus) <= 0:
                continue
            bonusType, bonusItemId, bonusNum = fixedBonus[0]
            if bonusType != gametypes.BONUS_TYPE_ITEM:
                continue
            itemInfo = uiUtils.getGfxItemById(bonusItemId)
            itemList.append(itemInfo)

        return itemList

    def canGained(self, p):
        gainedCount = 0
        svcList = p.vipDailyBonus
        now = p.getServerTime()
        itemList = []
        isVIP = False
        gainedAll = False
        serViceCount = 0
        for s in svcList:
            sid, expire, taken = s
            if expire <= now:
                continue
            svsData = VSD.data.get(sid, {})
            if svsData.get('serviceType', 1) != 2:
                continue
            if svsData.get('invalid', 0) == 1:
                continue
            bonusId = svsData.get('bonusId', 0)
            if bonusId == 0:
                continue
            bonusData = BD.data.get(bonusId, {})
            fixedBonus = bonusData.get('fixedBonus', ())
            if len(fixedBonus) <= 0:
                continue
            bonusType, bonusItemId, bonusNum = fixedBonus[0]
            serViceCount += 1
            if bonusType != gametypes.BONUS_TYPE_ITEM:
                continue
            if taken:
                gainedCount += 1
            itemInfo = uiUtils.getGfxItemById(bonusItemId)
            itemList.append(itemInfo)

        isVIP = serViceCount > 0
        gainedAll = gainedCount == len(itemList)
        return (isVIP, gainedAll)

    def onOpenVipBasicPackageConfirm(self, *arg):
        gameglobal.rds.ui.tianyuMall.onOpenVipBasicPackageConfirm()

    def onGotoMall(self, *args):
        gameglobal.rds.ui.tianyuMall.show(tab=MALL.MAIN_TAB_VIP)

    def onGotoRecharge(self, *args):
        BigWorld.player().openRechargeFunc()

    def canOpenTab(self):
        canOpen = False
        hasReward = False
        if not gameglobal.rds.configData.get('enableNewPlayerActivity', False):
            offset = utils.getNow() - utils.getServerOpenTime()
        else:
            p = BigWorld.player()
            offset = utils.getNow() - p.firstEnterWorldTimeOfCell
        duration = MCFD.data.get('firstBuyDuration', 30) * const.TIME_INTERVAL_DAY
        if offset < duration:
            if gameglobal.rds.configData.get('enableNewPlayerActivity', False):
                if utils.isActivitySaleNewPlayer():
                    canOpen = True
            else:
                canOpen = True
        isVIP, gainedAll = self.canGained(BigWorld.player())
        if isVIP and not gainedAll:
            hasReward = True
        return (canOpen, hasReward)
