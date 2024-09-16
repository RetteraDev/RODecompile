#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/activitySaleFirstPayProxy.o
import BigWorld
import gameglobal
import uiUtils
import const
import utils
import clientUtils
from uiProxy import UIProxy
from data import mall_config_data as MCD
from cdata import game_msg_def_data as GMDD

class ActivitySaleFirstPayProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ActivitySaleFirstPayProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerMc': self.onRegisterMc,
         'unRegisterMc': self.onUnRegisterMc,
         'openRecharge': self.onOpenRecharge,
         'gain': self.onGain}
        self.panelMc = None
        self.stat = 0
        self.firstEnterGameTime = 0
        self.canOpen = False
        self.hasReward = False

    def onRegisterMc(self, *arg):
        self.panelMc = arg[3][0]
        self.refreshFrame()

    def onUnRegisterMc(self, *arg):
        self.panelMc = None
        self.canOpen = False
        self.hasReward = False

    def clearAll(self):
        self.stat = 0
        self.firstEnterGameTime = 0

    def getRechargeInfo(self):
        p = BigWorld.player()
        if p:
            p.base.getFirstChargeRewardStat()

    def updateFrameInfo(self, stat, firstEnterGameTime):
        self.stat = stat
        self.firstEnterGameTime = firstEnterGameTime
        self.refreshFrame()

    def refreshFrame(self):
        if self.panelMc:
            start, end, duration = self.getActivityTime()
            now = utils.getNow()
            passed = now - self.firstEnterGameTime
            durationOff = duration - passed
            endOff = end - now
            remainTime = min(durationOff, endOff)
            frameInfo = {}
            frameInfo['itemList'] = self.getItemList()
            frameInfo['canGain'] = self.stat == const.COIN_FIRSET_CHARGE_REWARD_STAT_PENDING
            frameInfo['time'] = remainTime
            frameInfo['iconPath'] = 'activitySale/ActivitySaleFirstPay.dds'
            self.panelMc.Invoke('refreshFrame', uiUtils.dict2GfxDict(frameInfo))

    def updateStat(self, newStat):
        self.updateFrameInfo(newStat, self.firstEnterGameTime)
        gameglobal.rds.ui.activitySale.refreshInfo()

    def getItemList(self):
        bId = MCD.data.get('firstChargeRewardBonusId', 0)
        itemList = clientUtils.genItemBonus(bId)
        list = []
        for itemId in itemList:
            list.append(uiUtils.getGfxItemById(itemId[0]))

        return list

    def getActivityTime(self):
        startTime = utils.getServerOpenTime()
        endTime = startTime + MCD.data.get('firstChargeRewardServerDuration') * const.TIME_INTERVAL_DAY
        duration = MCD.data.get('firstChargeRewardDuration', 0)
        return (startTime, endTime, duration)

    def onOpenRecharge(self, *args):
        p = BigWorld.player()
        if not self.checkTime():
            p.showGameMsg(GMDD.data.ACTIVITY_SALE_EXPIRE, ())
            return
        BigWorld.player().openRechargeFunc()

    def onGain(self, *args):
        p = BigWorld.player()
        p.cell.getFirstChargeReward()

    def checkTime(self):
        start, end, duration = self.getActivityTime()
        now = utils.getNow()
        if now > self.firstEnterGameTime + duration:
            return False
        if gameglobal.rds.configData.get('enableNewPlayerActivity', False):
            if utils.isActivitySaleNewPlayer():
                return True
            else:
                return False
        if now < start or now > end:
            return False
        return True

    def canOpenTab(self):
        if not gameglobal.rds.configData.get('enableFirstChargeReward', False):
            return (False, False)
        if not self.checkTime():
            return (False, False)
        lv = BigWorld.player().lv
        minLv = MCD.data.get('firstChargeRewardMinLv', 1)
        if lv < minLv:
            return (False, False)
        if self.stat == const.COIN_FIRSET_CHARGE_REWARD_STAT_NONE:
            self.canOpen = True
            self.hasReward = False
        elif self.stat == const.COIN_FIRSET_CHARGE_REWARD_STAT_DONE:
            if self.canOpen and gameglobal.rds.ui.activitySale.mediator:
                self.hasReward = False
            else:
                self.canOpen = False
                self.hasReward = False
        else:
            self.canOpen = True
            self.hasReward = True
        return (self.canOpen, self.hasReward)
