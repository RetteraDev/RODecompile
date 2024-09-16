#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/activitySalePointsRewardProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiUtils
import const
import uiConst
import utils
from uiProxy import UIProxy
from Scaleform import GfxValue
from gameclass import ClientMallVal as cmv
from data import mall_item_data as MID
from data import sys_config_data as SCD
from data import consumable_item_data as CID
from data import bonus_set_data as BSD
from data import mall_config_data as MCFD

class ActivitySalePointsRewardProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ActivitySalePointsRewardProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerMc': self.onRegisterMc,
         'unRegisterMc': self.onUnRegisterMc,
         'getScoreLimitArray': self.onGetScoreLimitArray,
         'getCurPoint': self.onGetCurPoint,
         'setRewardIndex': self.onSetRewardIndex,
         'openChargeWindow': self.onOpenChargeWindow,
         'getCurCoin': self.onGetCurCoin}
        self.panelMc = None
        self.scoreLimit = []
        self.scoreLimitArr = []
        self.mallIdArr = SCD.data.get('isActivitySaleMallId', [20023,
         20024,
         20025,
         20026])

    def onRegisterMc(self, *arg):
        self.panelMc = arg[3][0]
        self.panelMc.Invoke('loadBgImage', uiUtils.array2GfxAarry(self._getBgImagePath(), True))
        self.refreshItems()

    def onUnRegisterMc(self, *arg):
        self.panelMc = None
        self.scoreLimitArr = []

    def _getItemData(self):
        p = BigWorld.player()
        ret = []
        for mallId in self.mallIdArr:
            scoreLimit = MID.data.get(mallId, {}).get('mallScoreLimit', 0)
            slotArray = self._getBonusItems(mallId)
            slotArr = []
            for slot in slotArray:
                slotArr.append(uiUtils.getGfxItemById(slot))

            dic = {}
            canTup = self.hasLimited(mallId)
            dic['can'] = canTup[0]
            dic['btnEnable'] = canTup[1]
            dic['btnDesc'] = canTup[2]
            dic['itemDesc'] = SCD.data.get('activitySaleLimitPoints', gameStrings.TEXT_ACTIVITYSALEPOINTSREWARDPROXY_61) % scoreLimit
            dic['slotArray'] = slotArr
            self.scoreLimitArr.append(scoreLimit)
            ret.append(dic)

        return ret

    def _getBonusItems(self, mallId):
        ret = []
        itemId = MID.data.get(mallId, {}).get('itemId', 0)
        setId = CID.data.get(itemId, {}).get('itemSetInfo', ())[0]
        for i in BSD.data.get(setId, []):
            ret.append(i.get('bonusId', 0))

        return ret

    def onGetScoreLimitArray(self, *arg):
        ret = []
        for mallId in self.mallIdArr:
            scoreLimit = MID.data.get(mallId, {}).get('mallScoreLimit', 0)
            ret.append(scoreLimit)

        return uiUtils.array2GfxAarry(ret)

    def onGetCurPoint(self, *arg):
        p = BigWorld.player()
        return GfxValue(p.totalMallScore)

    def onSetRewardIndex(self, *arg):
        p = BigWorld.player()
        index = int(arg[3][0].GetNumber())
        gameglobal.rds.ui.activitySaleBuy.show(self.mallIdArr[index], 'limit', 1)

    def _getBgImagePath(self):
        if gameglobal.rds.configData.get('enableNewPlayerActivity', False):
            return (uiConst.ACTIVITY_SALE_POINT_BG_V1, uiConst.ACTIVITY_SALE_POINT_BG_LOOP)
        else:
            return (uiConst.ACTIVITY_SALE_POINT_BG, uiConst.ACTIVITY_SALE_POINT_BG_LOOP)

    def hasLimited(self, mallId):
        p = BigWorld.player()
        totalLimit = MID.data.get(mallId, {}).get('totalLimit', 0)
        scoreLimit = MID.data.get(mallId, {}).get('mallScoreLimit', 0)
        leftNum = totalLimit - p.mallInfo.get(mallId, cmv()).nTotal
        if leftNum:
            if p.totalMallScore - scoreLimit >= 0:
                return (True, True, gameStrings.TEXT_ACTIVITYSALELEVELBONUSPROXY_192)
            else:
                return (False, False, gameStrings.TEXT_ACTIVITYSALEPOINTSREWARDPROXY_106)
        else:
            return (True, False, gameStrings.TEXT_ACTIVITYSALELEVELBONUSPROXY_187)

    def refreshItems(self):
        if self.panelMc:
            self.panelMc.Invoke('updataRewardItem', uiUtils.array2GfxAarry(self._getItemData(), True))

    def onOpenChargeWindow(self, *arg):
        BigWorld.player().openRechargeFunc()

    def onGetCurCoin(self, *arg):
        p = BigWorld.player()
        tianbi = p.unbindCoin + p.bindCoin + p.freeCoin
        return GfxValue(tianbi)

    def refreshPanel(self):
        self.refreshItems()
        if self.panelMc:
            self.panelMc.Invoke('refreshPanel')
        gameglobal.rds.ui.activitySale.refreshInfo()

    def canGained(self):
        for mallid in self.mallIdArr:
            if not (self.hasLimited(mallid)[0] == True and self.hasLimited(mallid)[1] == False):
                return True

        return False

    def canGetReward(self):
        for mallid in self.mallIdArr:
            if self.hasLimited(mallid)[1]:
                return True

        return False

    def canOpenTab(self):
        p = BigWorld.player()
        canGained = self.canGained()
        duration = MCFD.data.get('pointsRewardDuration', 60) * const.TIME_INTERVAL_DAY
        if not gameglobal.rds.configData.get('enableNewPlayerActivity', False):
            offset = utils.getNow() - utils.getServerOpenTime()
        else:
            offset = utils.getNow() - p.firstEnterWorldTimeOfCell
        if offset < duration and canGained:
            if gameglobal.rds.configData.get('enableNewPlayerActivity', False):
                if utils.isActivitySaleNewPlayer():
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False
