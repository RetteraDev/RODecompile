#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/activitySaleProxy.o
from gamestrings import gameStrings
import BigWorld
import gameglobal
import uiUtils
import uiConst
import ui
import gametypes
import utils
import gamelog
from uiProxy import UIProxy
from callbackHelper import Functor
from guis import events
from guis.asObject import ASObject
from gameStrings import gameStrings
from data import push_data as PMD
from data import preferential_activities_detail_data as PADD
from data import sys_config_data as SCD
from data import random_lottery_data as RLD
from data import random_turn_over_card_data as RTOCD
from data import random_card_draw_data as RCDD
from data import random_lucky_lottery_data as RLLD
MALL_BOX_TAB_MAX_CNT = 3
TIME_LIMIT_TAB_MAX_CNT = 3

class ActivitySaleProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(ActivitySaleProxy, self).__init__(uiAdapter)
        self.modelMap = {'initPanel': self.onInitPanel,
         'unRegisterPanel': self.onUnRegisterPanel,
         'close': self.onClose,
         'changeTabIndex': self.onChangeTabIndex,
         'initTabInfo': self.onInitTabInfo,
         'initSubPanel': self.onInitSubPanel,
         'unRegisterSubPanel': self.onUnRegisterSubPanel}
        self.mediator = None
        self.tabIdx = uiConst.ACTIVITY_SALE_TAB_FIRST_PAY
        self.cnt = 0
        self.isNeedRefreshItemUseData = False
        self.addEvent(events.EVENT_ROLE_SET_LV, self.refreshInfo, isGlobal=True)
        uiAdapter.registerEscFunc(uiConst.WIDGET_ACTIVITY_SALE, self.checkAndHide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_ACTIVITY_SALE:
            self.mediator = mediator

    def clearWidget(self):
        self.mediator = None
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_ACTIVITY_SALE)
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()

    def clearAll(self):
        self.cnt = 0
        gameglobal.rds.ui.activitySaleFirstPay.clearAll()
        gameglobal.rds.ui.activitySaleNewbiePay.clearAll()
        gameglobal.rds.ui.activitySaleGroupBuy.clearAll()
        gameglobal.rds.ui.activitySaleLuckyLottery.clearAll()

    def reset(self):
        self.tabIdx = uiConst.ACTIVITY_SALE_TAB_FIRST_PAY

    def show(self, tabIdx):
        if not gameglobal.rds.configData.get('enableActivitySale', False):
            gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_ACTIVITY_SALE)
            return
        self.tabIdx = tabIdx
        if self.mediator:
            self.refreshInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_ACTIVITY_SALE)

    def onClose(self, *arg):
        self.checkAndHide()

    def checkAndHide(self):
        if gameglobal.rds.ui.activitySaleRandomCardDraw.isShowingResult == True:
            return
        self.uiAdapter.activitySaleGroupBuy.clearAll()
        self.uiAdapter.activitySaleLuckyLottery.checkAndHide()
        self.hide()

    def onChangeTabIndex(self, *arg):
        self.tabIdx = int(arg[3][0].GetNumber())

    def onInitTabInfo(self, *arg):
        self.refreshInfo()

    def checkCurTabIdxValid(self, tabList):
        firstTabIdx = -1
        isNoTabData = True
        for tabInfo in tabList:
            if tabInfo['visible'] and firstTabIdx == -1:
                firstTabIdx = tabInfo.get('tabIdx', -1)
            if tabInfo['tabIdx'] == self.tabIdx:
                isNoTabData = False
                if not tabInfo['visible']:
                    self.tabIdx = -1

        if (isNoTabData or self.tabIdx == -1) and firstTabIdx != -1:
            self.tabIdx = firstTabIdx
        if self.tabIdx != -1:
            return True
        return False

    @ui.callInCD(0.5)
    def refreshInfo(self):
        if not gameglobal.rds.configData.get('enableActivitySale', False):
            return
        tabList = self.createTabList()
        if self.mediator:
            if not self.checkCurTabIdxValid(tabList):
                self.checkAndHide()
                return
            info = dict()
            info['tabIdx'] = self.tabIdx
            info['tabList'] = tabList
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))
        cnt = 0
        ignoreCnt = 0
        showIdx = -1
        for tabInfo in tabList:
            if not tabInfo['visible'] or not tabInfo['redFlagVisible']:
                continue
            if tabInfo['tabIdx'] == uiConst.ACTIVITY_SALE_TAB_NEWBIE_PAY:
                ignoreCnt += 1
            cnt += 1
            if showIdx == -1:
                showIdx = tabInfo['tabIdx']

        pushMsg = gameglobal.rds.ui.pushMessage
        if cnt <= ignoreCnt:
            pushMsg.removePushMsg(uiConst.MESSAGE_TYPE_ACTIVITY_SALE)
        else:
            callBackDict = {'click': Functor(self.show, showIdx)}
            pushMsg.setCallBack(uiConst.MESSAGE_TYPE_ACTIVITY_SALE, callBackDict)
            pmd = PMD.data.get(uiConst.MESSAGE_TYPE_ACTIVITY_SALE, {})
            msgInfo = {'iconId': pmd.get('iconId', 0),
             'tooltip': pmd.get('tooltip', '%s') % (cnt - ignoreCnt)}
            pushMsg.addPushMsg(uiConst.MESSAGE_TYPE_ACTIVITY_SALE, msgInfo=msgInfo)
        oldFlag = self.checkRedFlag()
        self.cnt = cnt
        newFlag = self.checkRedFlag()
        if oldFlag != newFlag:
            gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()

    def createTabList(self):
        tabList = []
        self.addLuckyLotteryTabs(tabList)
        self.addLoopChargeTab(tabList)
        self.addTurnOverCardTab(tabList)
        self.addLotteryTab(tabList)
        self.addMultiMallBoxTabs(tabList)
        self.addRandomCardDrawTab(tabList)
        self.addTimeLimitRewardTabs(tabList)
        self.addGroupBuyTab(tabList)
        self.addFirstPayTab(tabList)
        self.addFirstBuyTab(tabList)
        self.addLevelBonusTab(tabList)
        self.addGiftBagTab(tabList)
        self.addPointsRewardTab(tabList)
        self.addNewbiePayTab(tabList)
        self.addDailyGiftTab(tabList)
        self.addWeekActivationTab(tabList)
        self.addCollectTab(tabList)
        return tabList

    def checkRedFlag(self):
        return self.cnt != 0

    def checkPanelVisible(self):
        tabList = self.createTabList()
        for tabInfo in tabList:
            if tabInfo['visible']:
                return True

        return False

    def checkTabIdxValid(self, tabIdx):
        tabList = self.createTabList()
        for tabData in tabList:
            tempTabIdx = tabData.get('tabIdx', 0)
            tabVisible = tabData.get('visible', False)
            if tabIdx == tempTabIdx and tabVisible:
                return True

        return False

    def onInitPanel(self, *args):
        proxyName = args[3][0].GetString()
        widget = ASObject(args[3][1])
        proxy = getattr(self.uiAdapter, proxyName, None)
        if proxy and hasattr(proxy, 'initPanel'):
            proxy.initPanel(widget)

    def onUnRegisterPanel(self, *args):
        proxyName = args[3][0].GetString()
        proxy = getattr(self.uiAdapter, proxyName, None)
        if proxy and hasattr(proxy, 'unRegisterPanel'):
            proxy.unRegisterPanel()

    def addFirstPayTab(self, tabList):
        tabInfo = {}
        tabInfo['tabIdx'] = uiConst.ACTIVITY_SALE_TAB_FIRST_PAY
        tabInfo['visible'], tabInfo['redFlagVisible'] = gameglobal.rds.ui.activitySaleFirstPay.canOpenTab()
        tabInfo['label'] = gameStrings.ACTIVITY_SALE_TAB_FIRST_PAY_LABEL
        tabList.append(tabInfo)

    def addFirstBuyTab(self, tabList):
        tabInfo = {}
        tabInfo['tabIdx'] = uiConst.ACTIVITY_SALE_TAB_FIRST_BUY
        tabInfo['visible'], tabInfo['redFlagVisible'] = gameglobal.rds.ui.activitySaleFirstBuy.canOpenTab()
        tabInfo['label'] = gameStrings.ACTIVITY_SALE_TAB_FIRST_BUY_LABEL
        tabList.append(tabInfo)

    def addLevelBonusTab(self, tabList):
        tabInfo = {}
        tabInfo['tabIdx'] = uiConst.ACTIVITY_SALE_TAB_LEVEL_BONUS
        tabInfo['visible'], tabInfo['redFlagVisible'] = gameglobal.rds.ui.activitySaleLevelBonus.canOpenTab()
        tabInfo['label'] = gameStrings.ACTIVITY_SALE_TAB_LEVEL_BONUS_LABEL
        if gameglobal.rds.configData.get('enableNewPlayerActivity', False):
            tabInfo['label'] = gameStrings.NEW_PLAYER_LEVEL_BONUS_LABEL
        tabList.append(tabInfo)

    def addGiftBagTab(self, tabList):
        tabInfo = {}
        tabInfo['tabIdx'] = uiConst.ACTIVITY_SALE_TAB_GIFT_BAG
        tabInfo['visible'] = gameglobal.rds.ui.activitySaleGiftBag.canOpenTab()
        tabInfo['redFlagVisible'] = False
        tabInfo['label'] = gameStrings.ACTIVITY_SALE_TAB_GIFT_BAG_LABEL
        tabList.append(tabInfo)

    def addPointsRewardTab(self, tabList):
        tabInfo = {}
        tabInfo['tabIdx'] = uiConst.ACTIVITY_SALE_TAB_POINTS_REWARD
        tabInfo['visible'] = gameglobal.rds.ui.activitySalePointsReward.canOpenTab()
        tabInfo['redFlagVisible'] = gameglobal.rds.ui.activitySalePointsReward.canGetReward()
        tabInfo['label'] = gameStrings.ACTIVITY_SALE_TAB_POINTS_REWARD_LABEL
        tabList.append(tabInfo)

    def addNewbiePayTab(self, tabList):
        tabInfo = {}
        tabInfo['tabIdx'] = uiConst.ACTIVITY_SALE_TAB_NEWBIE_PAY
        tabInfo['visible'], tabInfo['redFlagVisible'] = gameglobal.rds.ui.activitySaleNewbiePay.canOpenTab()
        tabInfo['label'] = gameStrings.ACTIVITY_SALE_TAB_NEWBIE_PAY_LABEL
        tabList.append(tabInfo)

    def addWeekActivationTab(self, tabList):
        visible = True
        if not gameglobal.rds.configData.get('enableWeekActivation', False):
            visible = False
        if not gameglobal.rds.ui.activitySaleWeekActivation.isShowWeekActTabBtn():
            visible = False
        tabInfo = {}
        tabInfo['label'] = gameStrings.TEXT_ACTIVITYSALEPROXY_280
        tabInfo['tabIdx'] = uiConst.ACTIVITY_SALE_TAB_WEEK_ACTIVATION
        tabInfo['newFlagVisible'] = False
        tabInfo['redFlagVisible'] = gameglobal.rds.ui.activitySaleWeekActivation.isRedFlagVisible()
        tabInfo['visible'] = visible
        tabList.append(tabInfo)

    def addMultiMallBoxTabs(self, tabList):
        preferentialActivityList = SCD.data.get('preferentialActivityList', ())
        activityTabInfoList = []
        self.uiAdapter.activitySaleMallBox.visibleActivityIdList = []
        for activityId in preferentialActivityList:
            visible = True
            activityData = PADD.data.get(activityId, {})
            tabInfo = {}
            tabInfo['label'] = activityData.get('activityName', '')
            tabInfo['newFlagVisible'] = False
            tabInfo['redFlagVisible'] = False
            tabInfo['activityId'] = activityId
            showType = activityData.get('showTimeType', 0)
            if not gameglobal.rds.configData.get('enablePreferentialActivity', False):
                visible = False
            elif showType == gametypes.PREFERENTIAL_ACTIVITY_SHOW_TIME_TYPE_START_END:
                visible = utils.getTimeSecondFromStr(activityData.get('startTime', '')) <= utils.getNow() and utils.getTimeSecondFromStr(activityData.get('endTime', '')) >= utils.getNow()
            elif showType == gametypes.PREFERENTIAL_ACTIVITY_SHOW_TIME_TYPE_DURATION:
                visible = utils.getServerOpenDays() <= activityData.get('durationTime')
            else:
                visible = False
            if activityData.get('isShowNewServiceActivities', False):
                visible = False
            tabInfo['visible'] = visible
            if visible:
                self.uiAdapter.activitySaleMallBox.visibleActivityIdList.append(activityId)
                activityTabInfoList.append(tabInfo)

        for i in xrange(MALL_BOX_TAB_MAX_CNT):
            if i < len(activityTabInfoList):
                tabInfo = activityTabInfoList[i]
            else:
                tabInfo = {}
                tabInfo['label'] = activityData.get('activityName', '')
                tabInfo['newFlagVisible'] = False
                tabInfo['redFlagVisible'] = False
                tabInfo['visible'] = False
            tabInfo['tabIdx'] = uiConst.ACTIVITY_SALE_TAB_MALL_BOX_1 + i
            tabList.append(tabInfo)

    def addDailyGiftTab(self, tabList):
        tabInfo = {}
        tabInfo['tabIdx'] = uiConst.ACTIVITY_SALE_TAB_DAILY_GIFT
        tabInfo['label'] = SCD.data.get('dailyWelfareBuyData', {}).get('tabName', '')
        tabInfo['newFlagVisible'] = False
        tabInfo['redFlagVisible'] = self.uiAdapter.activitySaleDailyGift.getRedPointVisible()
        tabInfo['visible'] = gameglobal.rds.configData.get('enableDailyWelfareActivity', False) or gameglobal.rds.configData.get('enableDailyWelfareActivityOptimize', False)
        tabList.append(tabInfo)

    def addTimeLimitRewardTabs(self, tabList):
        enableItemUseFeedback = gameglobal.rds.configData.get('enableItemUseFeedback', False)
        if enableItemUseFeedback:
            data = gameglobal.rds.ui.activitySaleTimeLimitReward.getFeedBackData()
        else:
            data = []
        for i in xrange(0, TIME_LIMIT_TAB_MAX_CNT):
            tabInfo = {}
            if i >= len(data):
                tabInfo['label'] = ''
                tabInfo['newFlagVisible'] = False
                tabInfo['redFlagVisible'] = False
                tabInfo['visible'] = False
            else:
                tabInfo['label'] = data[i].get('titleName', '')
                tabInfo['newFlagVisible'] = False
                tabInfo['redFlagVisible'] = gameglobal.rds.ui.activitySaleTimeLimitReward.isHasReward(data[i])
                tabInfo['visible'] = True
            tabInfo['tabIdx'] = uiConst.ACTIVITY_SALE_TIME_LIMIT_REWARD_1 + i
            tabList.append(tabInfo)

        p = BigWorld.player()
        if self.isNeedRefreshItemUseData and enableItemUseFeedback:
            p.cell.getItemUseData()
            p.cell.getItemUseRewardsData()
            self.isNeedRefreshItemUseData = False

    def addLoopChargeTab(self, tabList):
        tabInfo = {}
        tabInfo['tabIdx'] = uiConst.ACTIVITY_SALE_TAB_LOOP_CHARGE
        rewardKeyVal = self.uiAdapter.activitySaleLoopCharge.getRewardKeyVal()
        if rewardKeyVal:
            tabInfo['label'] = self.uiAdapter.activitySaleLoopCharge.getRewardKeyVal()[1].get('chargeRewardName', '')
        else:
            tabInfo['label'] = ''
        tabInfo['newFlagVisible'] = False
        tabInfo['redFlagVisible'] = self.uiAdapter.activitySaleLoopCharge.getRedPointVisible()
        tabInfo['visible'] = self.uiAdapter.activitySaleLoopCharge.canOpen()
        tabList.append(tabInfo)

    def addGroupBuyTab(self, tabList):
        groupPurchaseDataList = self.uiAdapter.activitySaleGroupBuy.getValidGroupBuyBasicData()
        tabIdx = uiConst.ACTIVITY_SALE_TAB_GROUP_BUY
        for idx, gpData in enumerate(groupPurchaseDataList):
            tabInfo = dict()
            self.uiAdapter.activitySaleGroupBuy.tabSubIdxToGBData[tabIdx] = gpData
            tabInfo['tabIdx'] = tabIdx
            tabIdx = uiConst.ACTIVITY_SALE_TAB_GROUP_BUY * uiConst.ACTIVITY_SALE_TAB_SUB_OFFSET + idx + 1
            tabInfo['label'] = gpData.get('name', ' ')
            tabInfo['newFlagVisible'] = False
            tabInfo['redFlagVisible'] = self.uiAdapter.activitySaleGroupBuy.getRedPointVisible(gpData.get('idList', []))
            tabInfo['visible'] = True
            tabList.append(tabInfo)

    def addLotteryTab(self, tabList):
        tabInfo = {}
        tabInfo['tabIdx'] = uiConst.ACTIVITY_SALE_TAB_LOTTERY
        data = RLD.data.get(SCD.data.get('randomLotteryActivityId', gametypes.RANDOM_LOTTERY_SYSCONFIG_ID), {})
        tabInfo['label'] = data.get('tabLabel', gameStrings.RANDOM_LOTTERY_TAB_LABEL)
        tabInfo['newFlagVisible'] = False
        tabInfo['redFlagVisible'] = False
        tabInfo['visible'] = self.uiAdapter.activitySaleLottery.canOpen()
        tabList.append(tabInfo)

    def addTurnOverCardTab(self, tabList):
        tabInfo = {}
        tabInfo['tabIdx'] = uiConst.ACTIVITY_SALE_TAB_TURN_OVER_CARD
        data = RTOCD.data.get(SCD.data.get('randomTurnOverCardActivityId', 1), {})
        tabInfo['label'] = data.get('tabLabel', gameStrings.TURN_OVER_CARD_LABEL)
        tabInfo['newFlagVisible'] = False
        tabInfo['redFlagVisible'] = self.uiAdapter.activitySaleTurnOverCard.getRedPointVisible()
        tabInfo['visible'] = self.uiAdapter.activitySaleTurnOverCard.canOpen()
        tabList.append(tabInfo)

    def addRandomCardDrawTab(self, tabList):
        tabInfo = {}
        tabInfo['tabIdx'] = uiConst.ACTIVITY_SALE_TAB_RANDOM_CARD_DRAW
        data = RCDD.data.get(SCD.data.get('randomCardDrawActivityId', 1), {})
        tabInfo['label'] = data.get('tabLabel', gameStrings.RANDOM_CARD_DRAW_LABEL)
        tabInfo['newFlagVisible'] = False
        tabInfo['redFlagVisible'] = self.uiAdapter.activitySaleRandomCardDraw.getRedPointVisible()
        tabInfo['visible'] = self.uiAdapter.activitySaleRandomCardDraw.canOpen()
        tabList.append(tabInfo)

    def addCollectTab(self, tabList):
        activityData = gameglobal.rds.ui.activitySaleCollect.getActivityData()
        tabInfo = {}
        tabInfo['tabIdx'] = uiConst.ACTIVITY_SALE_TAB_COLLECT
        tabInfo['label'] = activityData.get('tabName')
        tabInfo['newFlagVisible'] = False
        tabInfo['redFlagVisible'] = self.uiAdapter.activitySaleCollect.getRedPointVisible()
        tabInfo['visible'] = self.uiAdapter.activitySaleCollect.canOpen()
        tabList.append(tabInfo)

    def addLuckyLotteryTabs(self, tabList):
        RLLDIds = RLLD.data.keys()
        tabIdx = uiConst.ACTIVITY_SALE_TAB_LUCKY_LOTTERY
        for idx, RLLDId in enumerate(RLLDIds):
            self.uiAdapter.activitySaleLuckyLottery.tabSubIdxToRLLDId[tabIdx] = RLLDId
            tabInfo = dict()
            tabInfo['tabIdx'] = tabIdx
            tabIdx = uiConst.ACTIVITY_SALE_TAB_LUCKY_LOTTERY * uiConst.ACTIVITY_SALE_TAB_SUB_OFFSET + idx + 1
            tabInfo['label'] = RLLD.data.get(RLLDId, {}).get('name', '')
            tabInfo['newFlagVisible'] = False
            tabInfo['redFlagVisible'] = self.uiAdapter.activitySaleLuckyLottery.getRedPointVisible(RLLDId)
            tabInfo['visible'] = self.uiAdapter.activitySaleLuckyLottery.checkCanOpen(RLLDId)
            tabList.append(tabInfo)

    def onInitSubPanel(self, *args):
        realCurrentTabIdx = int(args[3][0].GetNumber())
        currentTabIdx = int(args[3][1].GetNumber())
        currentView = ASObject(args[3][2])
        if realCurrentTabIdx == uiConst.ACTIVITY_SALE_TAB_LUCKY_LOTTERY:
            self.uiAdapter.activitySaleLuckyLottery.initPanel(currentTabIdx, currentView)
        elif realCurrentTabIdx == uiConst.ACTIVITY_SALE_TAB_COLLECT:
            self.uiAdapter.activitySaleCollect.initCollect(currentView)
        elif realCurrentTabIdx == uiConst.ACTIVITY_SALE_TAB_RANDOM_CARD_DRAW:
            self.uiAdapter.activitySaleRandomCardDraw.initRandomCardDraw(currentView)
        elif realCurrentTabIdx == uiConst.ACTIVITY_SALE_TAB_TURN_OVER_CARD:
            self.uiAdapter.activitySaleTurnOverCard.initTurnOverCard(currentView)
        elif realCurrentTabIdx == uiConst.ACTIVITY_SALE_TAB_LOTTERY:
            panel = self.uiAdapter.activitySaleLottery.getCurrentPanel()
            self.uiAdapter.activitySaleLottery.initLottery(currentView, panel)
        elif realCurrentTabIdx == uiConst.ACTIVITY_SALE_TAB_GROUP_BUY:
            self.uiAdapter.activitySaleGroupBuy.initGroupBuy(currentTabIdx, currentView)
        elif realCurrentTabIdx == uiConst.ACTIVITY_SALE_TAB_LOOP_CHARGE:
            self.uiAdapter.activitySaleLoopCharge.initLoopCharge(currentView)
        elif realCurrentTabIdx == uiConst.ACTIVITY_SALE_TAB_DAILY_GIFT:
            self.uiAdapter.activitySaleDailyGift.initPanel(currentView)
        elif realCurrentTabIdx in (uiConst.ACTIVITY_SALE_TAB_MALL_BOX_1, uiConst.ACTIVITY_SALE_TAB_MALL_BOX_2, uiConst.ACTIVITY_SALE_TAB_MALL_BOX_3):
            self.uiAdapter.activitySaleMallBox.initPanel(realCurrentTabIdx, currentView)
        elif realCurrentTabIdx == uiConst.ACTIVITY_SALE_TAB_WEEK_ACTIVATION:
            gameglobal.rds.ui.activitySaleWeekActivation.initPanel(currentView)

    def onUnRegisterSubPanel(self, *args):
        realCurrentTabIdx = int(args[3][0].GetNumber())
        currentTabIdx = int(args[3][1].GetNumber())
        currentView = ASObject(args[3][2])
        if realCurrentTabIdx == uiConst.ACTIVITY_SALE_TAB_LUCKY_LOTTERY:
            self.uiAdapter.activitySaleLuckyLottery.unRegister()
        elif realCurrentTabIdx == uiConst.ACTIVITY_SALE_TAB_COLLECT:
            self.uiAdapter.activitySaleCollect.unRegisterCollect()
        elif realCurrentTabIdx == uiConst.ACTIVITY_SALE_TAB_RANDOM_CARD_DRAW:
            self.uiAdapter.activitySaleRandomCardDraw.unRegisterRandomCardDraw()
        elif realCurrentTabIdx == uiConst.ACTIVITY_SALE_TAB_TURN_OVER_CARD:
            self.uiAdapter.activitySaleTurnOverCard.unRegisterTurnOverCard()
        elif realCurrentTabIdx == uiConst.ACTIVITY_SALE_TAB_LOTTERY:
            self.uiAdapter.activitySaleLottery.unRegisterLottery()
        elif realCurrentTabIdx == uiConst.ACTIVITY_SALE_TAB_GROUP_BUY:
            self.uiAdapter.activitySaleGroupBuy.unRegisterGroupBuy()
        elif realCurrentTabIdx == uiConst.ACTIVITY_SALE_TAB_LOOP_CHARGE:
            self.uiAdapter.activitySaleLoopCharge.unRegisterLoopCharge()
        elif realCurrentTabIdx == uiConst.ACTIVITY_SALE_TAB_DAILY_GIFT:
            self.uiAdapter.activitySaleDailyGift.unRegisterDailyGift()
        elif realCurrentTabIdx in (uiConst.ACTIVITY_SALE_TAB_MALL_BOX_1, uiConst.ACTIVITY_SALE_TAB_MALL_BOX_2, uiConst.ACTIVITY_SALE_TAB_MALL_BOX_3):
            self.uiAdapter.activitySaleMallBox.unRegisterMallBox(realCurrentTabIdx)
        elif realCurrentTabIdx == uiConst.ACTIVITY_SALE_TAB_WEEK_ACTIVATION:
            gameglobal.rds.ui.activitySaleWeekActivation.unRegisterPanel()
