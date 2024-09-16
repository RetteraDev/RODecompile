#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/activitySaleLevelBonusProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiUtils
import const
import utils
import time
import uiConst
from uiProxy import UIProxy
from gamestrings import gameStrings
from data import sys_config_data as SCD
from data import mall_config_data as MCD
from cdata import game_msg_def_data as GMDD

class ActivitySaleLevelBonusProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ActivitySaleLevelBonusProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerMc': self.onRegisterMc,
         'unRegisterMc': self.onUnRegisterMc,
         'getLevelBonusInfo': self.onGetLevelBonusInfo,
         'openChargeWindow': self.onOpenChargeWindow,
         'openPurchaseWindow': self.onOpenPurchaseWindow,
         'claimBonus': self.onClaimBonus,
         'clickConfirmBuyBtn': self.onClickConfirmBuyBtn,
         'clickMallBtn': self.onClickMallBtn}
        self.panelMc = None
        self.chargeLvReward = const.COIN_CHARGE_LV_REWARD_STAT_NONE
        self.chargeLvRewardData = {}
        self.isOpen = False

    def onRegisterMc(self, *arg):
        self.panelMc = arg[3][0]
        self.isOpen = True

    def onUnRegisterMc(self, *arg):
        self.panelMc = None
        self.isOpen = False

    def onGetLevelBonusInfo(self, *arg):
        bgPath = self.getBgPath()
        textInfo, leftTime = self.getTextInfo()
        tianBi = self.getTianBi()
        bonusList = self.getBonusList()
        buyBtnEnable = self.chargeLvReward == const.COIN_CHARGE_LV_REWARD_STAT_NONE
        data = {'timeStr': gameStrings.LEFT_TIME_HEAD,
         'timeFmt': gameStrings.TEXT_ACTIVITYSALELEVELBONUSPROXY_52,
         'bgPath': bgPath,
         'textInfo': textInfo,
         'leftTime': leftTime,
         'bonusList': bonusList,
         'buyBtnEnable': buyBtnEnable,
         'tianBi': tianBi,
         'yunChuiTips': MCD.data.get('levelBonusYunChuiTips', 'YunChuiTips'),
         'bindCashTips': MCD.data.get('levelBonusBindCashTips', 'BindCashTips'),
         'btnTips': MCD.data.get('levelBonusBtnTips', 'BtnTips')}
        return uiUtils.dict2GfxDict(data, True)

    def onOpenChargeWindow(self, *arg):
        BigWorld.player().openRechargeFunc()

    def onOpenPurchaseWindow(self, *arg):
        p = BigWorld.player()
        if self.isExpired():
            p.showGameMsg(GMDD.data.ACTIVITY_SALE_EXPIRE, ())
            return
        coinNeed = MCD.data.get('chargeLvRewardCoinNeed', 1000)
        msg = MCD.data.get('activitySaleLevelBonusConfirm', '%d') % coinNeed
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, p.base.buyChargeLvReward)

    def onClaimBonus(self, *arg):
        lv = int(arg[3][0].GetNumber())
        BigWorld.player().cell.getChargeLvReward(lv)

    def isExpired(self):
        p = BigWorld.player()
        if gameglobal.rds.configData.get('enableNewPlayerActivity', False):
            if not utils.isActivitySaleNewPlayer():
                return True
        lastTime = MCD.data.get('chargeLvRewardServerDuration', 0) * const.TIME_INTERVAL_DAY
        if not gameglobal.rds.configData.get('enableNewPlayerActivity', False):
            endTime = utils.getDaySecond(int(utils.getServerOpenTime())) + lastTime
        else:
            firstEnterWorldTime = p.firstEnterWorldTimeOfCell
            endTime = firstEnterWorldTime + lastTime
        leftTime = endTime - utils.getNow()
        if leftTime <= 0:
            return True
        return False

    def canClaim(self):
        p = BigWorld.player()
        rd = MCD.data.get('chargeLvRewardDict', {})
        keys = rd.keys()
        for lv in keys:
            if p.lv >= lv and not self.chargeLvRewardData.has_key(lv):
                return True

        return False

    def remainClaim(self):
        rd = MCD.data.get('chargeLvRewardDict', {})
        keys = rd.keys()
        for lv in keys:
            if lv > 0 and not self.chargeLvRewardData.has_key(lv):
                return True

        return False

    def canOpenTab(self):
        if not gameglobal.rds.configData.get('enableChargeLvReward', False):
            return (False, False)
        canOpen = True
        canClaim = False
        if self.chargeLvReward == const.COIN_CHARGE_LV_REWARD_STAT_NONE:
            if not self.isOpen:
                canOpen = not self.isExpired()
        else:
            canClaim = self.canClaim()
            if not self.isOpen:
                canOpen = self.remainClaim()
        return (canOpen, canClaim)

    def refreshView(self):
        if self.panelMc:
            self.panelMc.Invoke('refresh', self.onGetLevelBonusInfo())

    def getBgPath(self):
        return [uiConst.ACTIVITY_SALE_LEVEL_BONUS_BG, uiConst.ACTIVITY_SALE_LEVEL_BONUS_BG_LOOP]

    def getTextInfo(self):
        if not gameglobal.rds.configData.get('enableNewPlayerActivity', False):
            startTime = utils.getDaySecond(int(utils.getServerOpenTime()))
        else:
            startTime = BigWorld.player().firstEnterWorldTimeOfCell
        lastTime = MCD.data.get('chargeLvRewardServerDuration', 0) * const.TIME_INTERVAL_DAY
        endTime = startTime + lastTime
        leftTime = endTime - utils.getNow()
        startTime = time.strftime(gameStrings.TEXT_TARGETROLEINFOPROXY_159_1, time.localtime(startTime)) + gameStrings.TEXT_PLAYRECOMMPROXY_848_6
        endTime = time.strftime(gameStrings.TEXT_TARGETROLEINFOPROXY_159_1, time.localtime(endTime)) + gameStrings.TEXT_PLAYRECOMMPROXY_848_6
        textInfo = {'time': {'title': gameStrings.TEXT_ACTIVITYSALELEVELBONUSPROXY_148,
                  'content': gameStrings.TEXT_ACTIVITYSALELEVELBONUSPROXY_148_1 % (startTime, endTime)},
         'desc': {'title': gameStrings.TEXT_ACTIVITYSALELEVELBONUSPROXY_149,
                  'content': SCD.data.get('activitySaleLevelBonusDesc', '')},
         'help': {'title': gameStrings.TEXT_ACTIVITYSALELEVELBONUSPROXY_150,
                  'content': SCD.data.get('activitySaleLevelBonusHelp', '')}}
        return (textInfo, leftTime)

    def getTianBi(self):
        p = BigWorld.player()
        return getattr(p, 'unbindCoin', 0) + getattr(p, 'bindCoin', 0) + getattr(p, 'freeCoin', 0)

    def getBonusList(self):
        bonusList = []
        p = BigWorld.player()
        rd = MCD.data.get('chargeLvRewardDict', {})
        keys = rd.keys()
        keys.sort()
        for lv in keys:
            content = gameStrings.TEXT_ACTIVITYSALELEVELBONUSPROXY_165 % lv if lv >= 20 else gameStrings.TEXT_ACTIVITYSALELEVELBONUSPROXY_165_1
            items = self.getBonusItems(rd[lv])
            btnInfo = self.getBtnInfo(lv, lv == keys[0])
            bonusDetail = {'lv': lv,
             'condition': p.lv >= lv,
             'btnInfo': btnInfo,
             'content': content,
             'items': items}
            bonusList.append(bonusDetail)

        return bonusList

    def getBtnInfo(self, lv, firstRow):
        p = BigWorld.player()
        enabled = False
        if self.chargeLvReward == const.COIN_CHARGE_LV_REWARD_STAT_NONE:
            label = gameStrings.TEXT_ACTIVITYSALELEVELBONUSPROXY_183
        elif p.lv < lv:
            label = gameStrings.TEXT_ACTIVITYSALELEVELBONUSPROXY_185
        elif self.chargeLvRewardData.has_key(lv):
            label = gameStrings.TEXT_ACTIVITYSALELEVELBONUSPROXY_187
        elif firstRow:
            label = gameStrings.TEXT_ACTIVITYSALELEVELBONUSPROXY_189
            enabled = True
        else:
            label = gameStrings.TEXT_ACTIVITYSALELEVELBONUSPROXY_192
            enabled = True
        btnInfo = {'label': label,
         'enabled': enabled}
        return btnInfo

    def getBonusItems(self, data):
        items = []
        for bonusItemId, bonusNum in data:
            if bonusNum >= 10000:
                if bonusNum % 10000 == 0:
                    bonusNum = str(bonusNum / 10000) + gameStrings.TEXT_CBGMAINPROXY_273
                else:
                    bonusNum = str(round(bonusNum * 1.0 / 10000, 1)) + gameStrings.TEXT_CBGMAINPROXY_273
            items.append(uiUtils.getGfxItemById(bonusItemId, bonusNum))

        return items

    def updatePlayerInfo(self, stat, data):
        self.chargeLvReward = stat
        self.chargeLvRewardData = data
        gameglobal.rds.ui.activitySale.refreshInfo()
        self.refreshView()

    def onClickConfirmBuyBtn(self, *arg):
        p = BigWorld.player()
        if self.isExpired():
            p.showGameMsg(GMDD.data.ACTIVITY_SALE_EXPIRE, ())
            return
        coinNeed = MCD.data.get('chargeLvRewardCoinNeed', 1000)
        msg = MCD.data.get('activitySaleLevelBonusConfirm', '%d') % coinNeed
        gameglobal.rds.ui.messageBox.showYesNoMsgBox(msg, p.base.buyChargeLvReward)

    def onClickMallBtn(self, *arg):
        BigWorld.player().getPrivateCompositeShop()
