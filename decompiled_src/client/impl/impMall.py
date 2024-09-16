#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impMall.o
import cPickle
import zlib
import BigWorld
import const
import gameglobal
import utils
from gameclass import ClientMallVal
from crontab import CronTab
from guis import events
from data import mall_item_data as MID
from data import item_data as ID
from data import hobby_presale_config_data as HPCD
from cdata import font_config_data as FCD
from cdata import game_msg_def_data as GMDD

class ImpMall(object):

    def onQueryMallGlobalLimit(self, mIds, currNums):
        mdd = MID.data
        left = {}
        if len(mIds) != len(currNums):
            return False
        for i in range(0, len(mIds)):
            md = mdd.get(mIds[i])
            if not md:
                return False
            if not md.has_key('globalLimit'):
                return False
            left[mIds[i]] = md['globalLimit'] - currNums[i]

        gameglobal.rds.ui.tianyuMall.onQueryMallGlobalLimitDone(left)
        return True

    def updateMallInfo(self, data):
        self._updateMallInfo(data)

    def _updateMallInfo(self, data):
        for mid, d in data.iteritems():
            nDay, nWeek, nTotal, tLast, nMonth = d
            self.mallInfo[mid] = ClientMallVal(nDay, nWeek, nTotal, tLast, nMonth)
            if MID.data.get(mid, {}).get('showRedPot', 0):
                gameglobal.rds.ui.tianyuMall.refreshMainTabs()

    def checkCanBuyMallItem(self, mid, many):
        md = MID.data.get(mid)
        if not md:
            return False
        if not self.mallInfo.has_key(mid):
            self.mallInfo[mid] = ClientMallVal()
        name = ID.data.get(md['itemId'], {}).get('name', '')
        if md.has_key('dayLimit'):
            if self.mallInfo[mid].nDay + md['many'] * many > md['dayLimit'] * md['many']:
                self.showGameMsg(GMDD.data.MALL_BUY_FAILD_DAY_LIMIT, (name, md['dayLimit']))
                return False
        if md.has_key('weekLimit'):
            if self.mallInfo[mid].nWeek + md['many'] * many > md['weekLimit'] * md['many']:
                self.showGameMsg(GMDD.data.MALL_BUY_FAILD_WEEK_LIMIT, (name, md['weekLimit']))
                return False
        if md.has_key('totalLimit'):
            if self.mallInfo[mid].nTotal + md['many'] * many > md['totalLimit'] * md['many']:
                self.showGameMsg(GMDD.data.MALL_BUY_FAILD_TOTAL_LIMIT, (name, md['totalLimit']))
                return False
        if md.has_key('beginTime') and md.has_key('endTime'):
            beginTime = md.get('beginTime')
            endTime = md.get('endTime')
            beginCT = CronTab(beginTime)
            endCT = CronTab(endTime)
            now = utils.getNow()
            if beginCT.next(now) < endCT.next(now):
                self.showGameMsg(GMDD.data.MALL_BUY_FAILD_WRONG_TIME, (name,))
                return False
        return True

    def onTryBuyMallItem(self, mId, canBuy):
        pass

    def sendCoin(self, unbindCoin, bindCoin, freeCoin):
        oldCoinAll = self.unbindCoin + self.bindCoin + self.freeCoin
        newCoinAll = unbindCoin + bindCoin + freeCoin
        if newCoinAll > oldCoinAll:
            gameglobal.rds.ui.showRewardLabel(newCoinAll - oldCoinAll, const.REWARD_LABEL_TIANBI)
        self.unbindCoin = unbindCoin
        self.bindCoin = bindCoin
        self.freeCoin = freeCoin
        gameglobal.rds.ui.tianyuMall.onSendMoneyCallback()
        gameglobal.rds.ui.inventory.updataMoney()
        self.dispatchEvent(const.EVENT_UPDATE_COIN, unbindCoin, bindCoin, freeCoin)
        gameglobal.rds.ui.dispatchEvent(events.EVENT_TIANBI_COIN_CHANGED)

    def sendMallCash(self, mallCash):
        if mallCash > self.mallCash:
            gameglobal.rds.ui.showRewardLabel(mallCash - self.mallCash, const.REWARD_LABEL_YUBI)
        self.mallCash = mallCash
        gameglobal.rds.ui.tianyuMall.onSendMoneyCallback()

    def sendMallScore(self, mallScore, totalMallScore):
        self.mallScore = mallScore
        self.totalMallScore = totalMallScore
        gameglobal.rds.ui.tianyuMall.onSendMoneyCallback()
        gameglobal.rds.tutorial.onGetMallScore(mallScore)

    def givePayMallSucc(self):
        gameglobal.rds.ui.tianyuMall.onConfirmGiveSuccess()
        self.showGameMsg(GMDD.data.MALL_GIVE_PAY_SUCC, ())

    def sendMallHistory(self, historyData):
        try:
            history = cPickle.loads(zlib.decompress(historyData))
        except:
            history = []

        self.mallHistory = history
        gameglobal.rds.ui.tianyuMall.onGetMallHistoryDone()

    def onBuyItemSucc(self, buyItems):
        gameglobal.rds.ui.tianyuMall.onConfirmBuySuccess()
        gameglobal.rds.ui.activitySalePointsReward.refreshPanel()
        gameglobal.rds.ui.activitySaleGiftBag.refreshPanel()
        gameglobal.rds.ui.activitySaleBuy.onConfirmBuySuccess()
        gameglobal.rds.ui.backflowDiscount.updateRechargeBuy()
        gameglobal.rds.ui.welfareAppVip.refreshContent()
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
        itemId = buyItems[0][0][0]
        time = buyItems[0][0][1]
        name = ID.data.get(itemId, {}).get('name', '')
        quality = ID.data.get(itemId, {}).get('quality', 1)
        color = FCD.data.get(('item', quality), {}).get('color', 'nothing')
        if len(buyItems) == 1:
            self.showGameMsg(GMDD.data.MALL_BUY_SUCCESS, (color,
             itemId,
             time,
             name))
        else:
            self.showGameMsg(GMDD.data.MALL_BUY_SUCCESS_MORE, ())

    def getCoinAll(self):
        p = BigWorld.player()
        unBindCoin = getattr(p, 'unbindCoin', 0)
        bindCoin = getattr(p, 'bindCoin', 0) + getattr(p, 'freeCoin', 0)
        return unBindCoin + bindCoin

    def onQueryExternalMallData(self, opType, data):
        print '@zs onQueryExternalMallData', opType, data
        if opType == 1 and not gameglobal.rds.ui.hobbyPreSaleShop.widget:
            gameglobal.rds.ui.hobbyPreSaleShop.show(data)
        if opType == 2 and not gameglobal.rds.ui.hobbyPreSaleCheck.widget:
            if not data:
                msg = HPCD.data.get('nonReserve', 0)
                gameglobal.rds.ui.messageBox.showMsgBox(msg)
            else:
                gameglobal.rds.ui.hobbyPreSaleCheck.show(data)
        if opType == 3:
            if data:
                data = gameglobal.rds.ui.hobbyPreSaleCheck.changeCoding(data)
                itemIdList = []
                codeList = []
                for info in data:
                    codeList.append(info.get('code', ''))
                    itemIdList.append(int(info.get('itemId', 0)))

                p = BigWorld.player()
                p.cell.getExternalMallRefund(itemIdList, codeList)
            else:
                msg = HPCD.data.get('nonReserveDeposit', '')
                gameglobal.rds.ui.messageBox.showMsgBox(msg)

    def onApplyExternalMallCode(self, ok, itemId, code, rc, errCode):
        print '@zs onApplyExternalMallCode', ok, code, rc, errCode
        gameglobal.rds.ui.hobbyPreSaleShop.setResetResveringGoodsCd(itemId)
        gameglobal.rds.ui.hobbyPreSaleSuccess.showHobbyPush(ok, itemId, code, rc, errCode)
