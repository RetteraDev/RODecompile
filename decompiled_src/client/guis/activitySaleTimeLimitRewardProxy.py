#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/activitySaleTimeLimitRewardProxy.o
import BigWorld
import time
import gameglobal
import utils
import clientUtils
import uiConst
from Scaleform import GfxValue
from guis import uiUtils
from uiProxy import UIProxy
from ui import gbk2unicode
from gameStrings import gameStrings
from data import limit_time_feedback_data as LTFD
BONUS_DEFAULT = 0
BONUS_RECEIVED = 1
BONUS_CAN_RECEIVE = 2
DAY_REFRESH = 1
WEEK_REFRESH = 2

class ActivitySaleTimeLimitRewardProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ActivitySaleTimeLimitRewardProxy, self).__init__(uiAdapter)
        self.modelMap = {'registerMc': self.onRegisterMc,
         'unRegisterMc': self.onUnRegisterMc,
         'getInfo': self.onGetInfo,
         'getBonus': self.onGetBonus,
         'openMall': self.onOpenMall}
        self.panelMc = {}
        self.itemDatas = []

    def onRegisterMc(self, *arg):
        if not self.panelMc:
            self.getData()
        idx = int(arg[3][1].GetNumber()) - uiConst.ACTIVITY_SALE_TIME_LIMIT_REWARD_1
        self.panelMc[idx] = arg[3][0]

    def onUnRegisterMc(self, *arg):
        self.itemDatas = []
        idx = int(arg[3][0].GetNumber()) - uiConst.ACTIVITY_SALE_TIME_LIMIT_REWARD_1
        self.panelMc[idx] = None

    def onGetBonus(self, *args):
        idx = int(args[3][0].GetNumber()) - uiConst.ACTIVITY_SALE_TIME_LIMIT_REWARD_1
        data = self.itemDatas[idx]
        targetItemId = self.getTargetItemId(data)
        BigWorld.player().cell.receiveItemUseFeedbackReward(targetItemId)

    def onOpenMall(self, *args):
        idx = int(args[3][0].GetNumber()) - uiConst.ACTIVITY_SALE_TIME_LIMIT_REWARD_1
        data = self.itemDatas[idx]
        searchWords = data.get('searchWords', '')
        gameglobal.rds.ui.tianyuMall.show(keyWord=searchWords)

    def getData(self):
        p = BigWorld.player()
        p.cell.getItemUseData()
        p.cell.getItemUseRewardsData()

    def isHasReward(self, data):
        return self.isBaseRewardAvaliable(data) or self.isLoopRewardAvaliable(data)

    def refreshPanel(self):
        for k, v in self.panelMc.iteritems():
            if v:
                v.Invoke('initPanel', GfxValue(k + uiConst.ACTIVITY_SALE_TIME_LIMIT_REWARD_1))

    def onGetInfo(self, *arg):
        idx = int(arg[3][0].GetNumber()) - uiConst.ACTIVITY_SALE_TIME_LIMIT_REWARD_1
        ret = {}
        if idx >= len(self.itemDatas) or idx < 0:
            return
        data = self.itemDatas[idx]
        useTimes = self.getUseTimes(data)
        ret['useTimes'] = useTimes
        baseBonusIds = data.get('baseBonusIds', [])
        loopBonusId = data.get('loopBonusId', 0)
        ret['baseBonusDatas'] = []
        for bonusId in baseBonusIds:
            itemData = self.getItemInfoFromBonusId(bonusId)
            ret['baseBonusDatas'].append(itemData)

        ret['loopBonusData'] = self.getItemInfoFromBonusId(loopBonusId)
        self.getBaseMargins(ret, data)
        self.getBaseBonusStates(ret, data)
        self.getLoopInfo(ret, data)
        self.getEndTime(ret, data)
        self.getRefreshType(ret, data)
        ret['baseProgressTip'] = data.get('baseProgressTip', '{0}')
        ret['loopProgressTip'] = data.get('loopProgressTip', '{0}')
        ret['alreadyUseTimesTxt'] = gameStrings.TIME_LIMIT_REWARD_ITEM_ALREADY_USE_TXT % useTimes
        ret['titleName'] = data.get('titleName', '')
        ret['iconPath'] = data.get('iconPath', '')
        ret['isRewardAvaliable'] = self.isBaseRewardAvaliable(data) or self.isLoopRewardAvaliable(data)
        ret['loopTip'] = data.get('loopTip', '')
        ret['loopTxt'] = data.get('loopTxt', '')
        return uiUtils.dict2GfxDict(ret, True)

    def getRefreshType(self, ret, data):
        refreshType = data.get('refreshType', 0)
        ret['refreshTxt'] = ''
        if refreshType == DAY_REFRESH:
            ret['refreshTxt'] = gameStrings.TIME_LIMIT_REWARD_DAY_REFRESH_TXT
        elif refreshType == WEEK_REFRESH:
            ret['refreshTxt'] = gameStrings.TIME_LIMIT_REWARD_WEEK_REFRESH_TXT

    def getEndTime(self, ret, data):
        endTime = data.get('crontabEnd', ())[0]
        timeStamp = utils.nextByTimeTuple(endTime, utils.getNow()) + utils.getNow()
        timeData = time.localtime(timeStamp)
        ret['endTimeTxt'] = gameStrings.TIME_LIMIT_REWARD_END_TIME_TXT % (timeData.tm_mon, timeData.tm_mday, timeData.tm_hour)

    def getUseTimes(self, data):
        p = BigWorld.player()
        targetItemId = self.getTargetItemId(data)
        if hasattr(p, 'paybackItemInfo'):
            return p.paybackItemInfo.get(targetItemId, 0)
        return 0

    def getBaseMargins(self, ret, data):
        ret['baseMargins'] = data.get('baseMargins', [])

    def getBaseBonusStates(self, ret, data):
        p = BigWorld.player()
        baseMargins = data.get('baseMargins', [])
        targetItemId = self.getTargetItemId(data)
        useTimes = self.getUseTimes(data)
        ret['baseBonusStates'] = []
        for i in xrange(0, len(baseMargins)):
            if hasattr(p, 'paybackItemUseReward'):
                if p.paybackItemUseReward.get(targetItemId, {}).get(baseMargins[i]):
                    ret['baseBonusStates'].append(BONUS_RECEIVED)
                    continue
            if useTimes >= ret['baseMargins'][i]:
                ret['baseBonusStates'].append(BONUS_CAN_RECEIVE)
                continue
            ret['baseBonusStates'].append(BONUS_DEFAULT)

    def isBaseRewardAvaliable(self, data):
        ret = {}
        self.getBaseMargins(ret, data)
        self.getBaseBonusStates(ret, data)
        baseBonusStates = ret.get('baseBonusStates', [])
        if not baseBonusStates:
            return False
        for state in baseBonusStates:
            if state == BONUS_CAN_RECEIVE:
                return True

        return False

    def isLoopRewardAvaliable(self, data):
        ret = {}
        self.getLoopInfo(ret, data)
        if ret['loopAvaliable'] and ret['loopCurrentValue'] >= ret['loopMaxValue']:
            return True
        return False

    def getItemInfoFromBonusId(self, bonusId):
        if not bonusId:
            return None
        else:
            itemBonus = clientUtils.genItemBonus(bonusId)
            return uiUtils.getGfxItemById(itemBonus[0][0], itemBonus[0][1])

    def getLoopInfo(self, ret, data):
        p = BigWorld.player()
        targetItemId = self.getTargetItemId(data)
        useTimes = self.getUseTimes(data)
        loopMargin = data.get('loopMargin', 0)
        ret['loopAvaliable'] = False
        baseMargins = data.get('baseMargins', [])
        if data.get('loopOp', False) and useTimes >= baseMargins[len(baseMargins) - 1]:
            ret['loopAvaliable'] = True
        if not ret['loopAvaliable']:
            return
        finishRewardLoopMargin = baseMargins[len(baseMargins) - 1]
        if hasattr(p, 'paybackItemUseReward') and p.paybackItemUseReward.get(targetItemId, {}).get('finishRewardLoopMargin', 0):
            finishRewardLoopMargin = p.paybackItemUseReward.get(targetItemId, {}).get('finishRewardLoopMargin', 0)
        ret['loopCurrentValue'] = useTimes - finishRewardLoopMargin
        ret['loopMaxValue'] = loopMargin

    def isTimeAvaliable(self, data):
        if not data:
            return False
        beginTime = data.get('crontabStart')[0]
        endTime = data.get('crontabEnd')[0]
        if beginTime and endTime and utils.inTimeTupleRange(beginTime, endTime, utils.getNow()):
            return True
        return False

    def getFeedBackData(self):
        feedbackItems = []
        for k, v in LTFD.data.iteritems():
            if v.get('openOp', False) and self.isTimeAvaliable(v):
                feedbackItems.append(v)

        self.itemDatas = feedbackItems
        return feedbackItems

    def getTargetItemId(self, data):
        return data.get('itemId', ())[0]
