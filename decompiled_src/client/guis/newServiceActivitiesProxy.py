#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/newServiceActivitiesProxy.o
import time
import BigWorld
import gameglobal
import uiConst
import gametypes
import utils
import const
import commNewServerActivity
import appSetting
import keys
from uiTabProxy import UITabProxy
from asObject import RedPotManager
from Scaleform import GfxValue
from data import ns_honor_rank_act_data as NHRAD
from data import new_server_activity_data as NSAD
from cdata import ns_property_rank_act_data as NPRAD
SECONDS_PER_DAY = 86400
TAB_BTN_MAX_CNT = 12
PRIVIEGE_DAY_TO_SECOND = 86400

class NewServiceActivitiesProxy(UITabProxy):

    def __init__(self, uiAdapter):
        super(NewServiceActivitiesProxy, self).__init__(uiAdapter)
        self.reset()
        uiAdapter.registerEscFunc(uiConst.WIDGET_NEW_SERVICE_ACTIVITIES, self.hide)

    def reset(self):
        super(NewServiceActivitiesProxy, self).reset()

    def _registerASWidget(self, widgetId, widget):
        if widgetId == uiConst.WIDGET_NEW_SERVICE_ACTIVITIES:
            self.widget = widget
            self.initUI()
            self.widget.setTabIndex(self.showTabIndex)
            self.reflowTabBtns()

    def clearWidget(self):
        super(NewServiceActivitiesProxy, self).clearWidget()
        self.widget = None
        self.uiAdapter.unLoadWidget(uiConst.WIDGET_NEW_SERVICE_ACTIVITIES)

    def appendTab(self, tabList, view, proxy, tabName = '', visible = True):
        tabLen = len(tabList)
        tabList.append({'tabIdx': tabLen,
         'tabName': 'tabBtn%d' % tabLen,
         'view': view,
         'proxy': proxy,
         'visible': visible})

    def _getTabList(self):
        tabList = []
        self.appendTab(tabList, 'NewServiceCelebrateWidget', 'newServiceCelebrate', '', self.isShowTabCelebrate())
        self.appendTab(tabList, 'NewServiceWelfareWidget', 'newServiceWelfare', '', self.isShowTabBtnWelfare())
        self.appendTab(tabList, 'NewServiceMallBoxWidget', 'newServiceMallBox', '', self.isShowTabBtnBox())
        self.appendTab(tabList, 'NewServerTopRankTab0Widget', 'newServerTopRankGuild', '', self.isShowTabBtnGuild())
        self.appendTab(tabList, 'NewServerTopRankTab1Widget', 'newServerTopRankCombatScoreAndLv', '', self.isShowTabBtnCombat())
        self.appendTab(tabList, 'NewServerTopRankTab1Widget', 'newServerTopRankCombatScoreAndLv', '', self.isShowTabBtnLevel())
        self.appendTab(tabList, 'NewServerTopRankTab3Widget', 'newServerTopRankHonor', '', self.isShowTabBtnHonor())
        self.appendTab(tabList, 'NewServiceFubenRaceWidget', 'newServiceFubenRace', '', self.isShowTabBtnRace())
        self.appendTab(tabList, 'NewServiceFirstKillWidget', 'newServiceFirstKill', '', self.isShowTabFirstKill())
        self.appendTab(tabList, 'NewServiceSecretMerchantWidget', 'newServiceSecretMerchant', '', self.isShowTabBtnDailyGift())
        self.appendTab(tabList, 'NewServiceLotteryWidget', 'newServiceLottery', '', self.isShowTabLottery())
        self.appendTab(tabList, 'NewServiceFinalGuideWidget', 'newServiceFinalGuide', '', self.isShowTabFinalGuide())
        return tabList

    def isShowTabCelebrate(self):
        canOpen = gameglobal.rds.ui.newServiceCelebrate.canOpenTab()
        return canOpen

    def isShowTabBtnWelfare(self):
        canOpen = gameglobal.rds.ui.newServiceWelfare.canOpenTab()
        return canOpen

    def isShowTabBtnBox(self):
        canOpen = gameglobal.rds.ui.newServiceMallBox.canOpenTab()
        return canOpen

    def isShowTabBtnGuild(self):
        if not commNewServerActivity.isNewServerActivityOpen(const.NEW_SERVICE_TOP_RANK_GUILD):
            return False
        return self.checkGuildTab()

    def isShowTabBtnCombat(self):
        if not commNewServerActivity.isNewServerActivityOpen(const.NEW_SERVICE_TOP_RANK_COMBAT_SCORE):
            return False
        return self.checkCombatAndLvTab(gametypes.TOP_TYPE_COMBAT_SCORE)

    def isShowTabBtnLevel(self):
        if not commNewServerActivity.isNewServerActivityOpen(const.NEW_SERVICE_TOP_RANK_COMBAT_LV):
            return False
        return self.checkCombatAndLvTab(gametypes.TOP_TYPE_LEVEL)

    def isShowTabBtnHonor(self):
        if not commNewServerActivity.isNewServerActivityOpen(const.NEW_SERVICE_TOP_RANK_HONOR):
            return False
        return self.checkHonorTab()

    def isShowTabBtnRace(self):
        return gameglobal.rds.ui.newServiceFubenRace.canOpenTab()

    def isShowTabFirstKill(self):
        return gameglobal.rds.ui.newServiceFirstKill.canOpenTab()

    def isShowTabLottery(self):
        if not commNewServerActivity.isNewServerActivityOpen(const.NEW_SERVICE_LOTTERY):
            return False
        lotteryId = NSAD.data.get('lotteryId', 0)
        if not lotteryId:
            return False
        if not commNewServerActivity.checkNSLotteryInDisplayTime(lotteryId):
            return False
        if not commNewServerActivity.checkLotteryInServerConfigList(lotteryId):
            return False
        return True

    def isShowTabFinalGuide(self):
        if not commNewServerActivity.isNewServerActivityOpen(const.NEW_SERVICE_FINAL_GUIDE):
            return False
        canOpen = gameglobal.rds.ui.newServiceFinalGuide.canOpenTab()
        return canOpen

    def isShowTabBtnDailyGift(self):
        canOpen = gameglobal.rds.ui.newServiceSecretMerchant.canOpenTab()
        return canOpen and commNewServerActivity.isNewServerActivityOpen(const.NEW_SERVICE_SECRET_MERCHANT)

    def reflowTabBtns(self):
        if not self.widget:
            return
        tabLen = len(self.tabList)
        posY = 139
        for tabIdx in xrange(TAB_BTN_MAX_CNT):
            tabBtn = getattr(self.widget, 'tabBtn%d' % tabIdx)
            if tabIdx < tabLen:
                tabBtn.visible = self.tabList[tabIdx]['visible']
                if tabBtn.visible:
                    tabBtn.y = posY
                    posY += 41
            else:
                tabBtn.visible = False

        RedPotManager.addRedPot(self.widget.tabBtn1, uiConst.NEW_SERVICE_ACTIVITIES_TAB_WELFARE_REDPOT, (137, 0), self.visiblePotFunTabWelfare)
        RedPotManager.addRedPot(self.widget.tabBtn4, uiConst.NEW_SERVICE_ACTIVITIES_TAB_COMBAT_REDPOT, (137, 0), self.visiblePotFunTabCombat)
        RedPotManager.addRedPot(self.widget.tabBtn5, uiConst.NEW_SERVICE_ACTIVITIES_TAB_LEVEL_REDPOT, (137, 0), self.visiblePotFunTabLevel)
        RedPotManager.addRedPot(self.widget.tabBtn9, uiConst.NEW_SERVICE_ACTIVITIES_TAB_GIFT_REDPOT, (137, 0), self.visiblePotFunTabGift)
        RedPotManager.addRedPot(self.widget.tabBtn11, uiConst.NEW_SERVICE_ACTIVITIES_TAB_FINAL_REDPOT, (137, 0), self.visiblePotFunTabFinal)

    def refreshAllRedPoint(self):
        self.updateActiviesTabWelfareRedPot()
        self.updateActiviesTabCombatRedPot()
        self.updateActiviesTabLevelRedPot()
        self.updateActiviesTabGiftRedPot()
        self.updateFinalReportRedPot()

    def updateFinalReportRedPot(self):
        if not self.widget:
            return
        if self.widget.tabBtn11.visible:
            RedPotManager.updateRedPot(uiConst.NEW_SERVICE_ACTIVITIES_TAB_FINAL_REDPOT)

    def visiblePotFunTabWelfare(self, *args):
        hasReward = gameglobal.rds.ui.newServiceWelfare.isShowWelfareRedPoint()
        return GfxValue(hasReward)

    def updateActiviesTabWelfareRedPot(self):
        if not self.widget:
            return
        if self.widget.tabBtn1.visible:
            RedPotManager.updateRedPot(uiConst.NEW_SERVICE_ACTIVITIES_TAB_WELFARE_REDPOT)

    def visiblePotFunTabGift(self, *args):
        return GfxValue(self.isDailyGiftRedPoint())

    def visiblePotFunTabFinal(self, *args):
        return GfxValue(self.isFinalGuideRedPoint())

    def isFinalGuideRedPoint(self):
        return self.isShowTabFinalGuide() and gameglobal.rds.ui.newServiceFinalGuide.isShowCompleteRedPoint()

    def isDailyGiftRedPoint(self):
        lastTime = appSetting.Obj.get(keys.SET_NEW_SERVICE_AVTIVITY_DAILY_GIFT_PUSH % BigWorld.player().gbId, 0)
        thisTime = utils.getNow()
        lastTimeTuple = time.localtime(lastTime)
        thisTimeTuple = time.localtime(thisTime)
        if thisTime > utils.getServerOpenTime() / SECONDS_PER_DAY * SECONDS_PER_DAY + NSAD.data.get('dailyGiftOpenDay', 7) * SECONDS_PER_DAY:
            return False
        elif lastTimeTuple.tm_year == thisTimeTuple.tm_year and lastTimeTuple.tm_mon == thisTimeTuple.tm_mon and lastTimeTuple.tm_mday == thisTimeTuple.tm_mday:
            return False
        else:
            return self.isShowTabBtnDailyGift()

    def visiblePotFunTabCombat(self, *args):
        if not self.widget:
            return
        return GfxValue(self.isShowCombatSocreRetPoint())

    def updateActiviesTabCombatRedPot(self):
        if not self.widget:
            return
        if self.widget.tabBtn4.visible:
            RedPotManager.updateRedPot(uiConst.NEW_SERVICE_ACTIVITIES_TAB_COMBAT_REDPOT)

    def visiblePotFunTabLevel(self, *args):
        if not self.widget:
            return
        return GfxValue(self.isShowLevelRetPoint())

    def updateActiviesTabLevelRedPot(self):
        if not self.widget:
            return
        if self.widget.tabBtn5.visible:
            RedPotManager.updateRedPot(uiConst.NEW_SERVICE_ACTIVITIES_TAB_LEVEL_REDPOT)

    def updateActiviesTabGiftRedPot(self):
        if not self.widget:
            return
        if self.widget.tabBtn9.visible:
            RedPotManager.updateRedPot(uiConst.NEW_SERVICE_ACTIVITIES_TAB_GIFT_REDPOT)

    def isShowCombatSocreRetPoint(self):
        if not commNewServerActivity.isNewServerActivityOpen(const.NEW_SERVICE_TOP_RANK_COMBAT_SCORE):
            return False
        return self.getPropertyRankRedPoint(gametypes.TOP_TYPE_COMBAT_SCORE)

    def isShowLevelRetPoint(self):
        if not commNewServerActivity.isNewServerActivityOpen(const.NEW_SERVICE_TOP_RANK_COMBAT_LV):
            return False
        return self.getPropertyRankRedPoint(gametypes.TOP_TYPE_LEVEL)

    def getPropertyRankRedPoint(self, topType):
        redPoint = False
        if not self.checkCombatAndLvOpen(topType):
            return redPoint
        else:
            newServerRedPoint = getattr(gameglobal.rds.ui.rewardGiftActivityIcons, 'newServerRedPoint', None)
            if not newServerRedPoint:
                return redPoint
            for i in utils.getEnableNewServerPropertyRankActStages(topType):
                if newServerRedPoint.get(str(topType) + '/' + str(i), False) == True:
                    redPoint = True
                    break

            return redPoint

    def show(self, showTabIndex = 0):
        if not self.checkNewServiceActivitiesOpen():
            return
        self.showTabIndex = showTabIndex
        if self.widget:
            self.widget.setTabIndex(self.showTabIndex)
        else:
            self.uiAdapter.loadWidget(uiConst.WIDGET_NEW_SERVICE_ACTIVITIES)

    def initUI(self):
        self.widget.defaultCloseBtn = self.widget.closeBtn
        self.initTabUI()

    def onTabChanged(self, *args):
        super(NewServiceActivitiesProxy, self).onTabChanged(*args)
        self.refreshInfo()
        currentTabIndex = int(args[3][0].GetNumber())
        if currentTabIndex == const.NEW_SERVICE_TOP_RANK_COMBAT_SCORE or currentTabIndex == const.NEW_SERVICE_TOP_RANK_COMBAT_LV:
            proxy = self.getCurrentProxy()
            if proxy and hasattr(proxy, 'setType'):
                proxy.setType(currentTabIndex)

    def refreshInfo(self):
        if not self.widget:
            return
        self.updateActiviesTabWelfareRedPot()
        self.updateActiviesTabCombatRedPot()
        self.updateActiviesTabLevelRedPot()
        proxy = self.getCurrentProxy()
        if proxy and hasattr(proxy, 'refreshInfo'):
            proxy.refreshInfo()

    def checkCombatAndLvOpen(self, topType):
        if not gameglobal.rds.configData.get('enableNewServerTopRankAct', False):
            return False
        p = BigWorld.player()
        if topType == gametypes.TOP_TYPE_COMBAT_SCORE:
            stage = utils.getNewServerPropertyRankActStage(topType, p.combatScoreList[const.COMBAT_SCORE])
        elif topType == gametypes.TOP_TYPE_LEVEL:
            stage = utils.getNewServerPropertyRankActStage(topType, (p.lv, utils.getTotalSkillEnhancePoint(p)))
        configData = utils.getNSPropertyRankActData(topType)
        if stage > len(configData) - 1:
            return False
        elif not configData:
            return False
        if stage < 0:
            stage = 0
        enableTime = configData[stage].get('enableTime', None)
        if not enableTime:
            return False
        periodType, nWeeksOffset, nLastWeeks = enableTime
        tStart, tEnd = utils.calcTimeDuration(periodType, utils.getServerOpenTime(), nWeeksOffset, nLastWeeks)
        if tStart <= utils.getNow() <= tEnd:
            return True
        else:
            return False

    def checkGuildTab(self):
        if not gameglobal.rds.configData.get('enableNewServerGuildPrestige', False):
            return False
        configData = utils.getNSPrestigeActivityConfigData()
        if configData.get('fromMergeTime', 0) == 0:
            serverOpenTime = gameglobal.rds.configData.get('serverLatestMergeTime', 0) or utils.getServerOpenTime()
            stage = utils.getGuildPrestigeEnableStageAndOneDay(serverOpenTime)
            enableTime = configData.get('enableTime%s' % stage)
            if not enableTime:
                return False
            periodType, nWeeksOffset, nLastWeeks = enableTime
            tStart, tEnd = utils.calcTimeDuration(periodType, serverOpenTime, nWeeksOffset, nLastWeeks)
            if tStart <= utils.getNow() <= tEnd + PRIVIEGE_DAY_TO_SECOND:
                return True
            else:
                return False
        return False

    def checkCombatAndLvTab(self, topType):
        if not gameglobal.rds.configData.get('enableNewServerTopRankAct', False):
            return False
        result = utils.getEnableNewServerPropertyRankActStages(topType)
        if result:
            stage = max(result)
        else:
            stage = -1
        configData = utils.getNSPropertyRankActData(topType)
        if stage > len(configData) - 1:
            return False
        if stage < 0:
            stage = 0
        enableTime = configData[stage].get('enableTime', None)
        if not enableTime:
            return False
        periodType, nWeeksOffset, nLastWeeks = enableTime
        tStart, tEnd = utils.calcTimeDuration(periodType, utils.getServerOpenTime(), nWeeksOffset, nLastWeeks)
        if tStart <= utils.getNow() <= tEnd + PRIVIEGE_DAY_TO_SECOND:
            return True
        else:
            return False

    def checkHonorTab(self):
        configData = NHRAD.data.values()[0]
        if not gameglobal.rds.configData.get('enableNewServerTopRankAct', False):
            return False
        enableTime = configData.get('newServerHonorRankEanbleTime', None)
        if not enableTime:
            return False
        periodType, nWeeksOffset, nLastWeeks = enableTime
        tStart, tEnd = utils.calcTimeDuration(periodType, utils.getServerOpenTime(), nWeeksOffset, nLastWeeks)
        if tStart <= utils.getNow() <= tEnd + PRIVIEGE_DAY_TO_SECOND:
            return True
        else:
            return False

    def checkNewServiceActivitiesOpen(self):
        if self.isShowTabBtnWelfare() or self.isShowTabBtnBox() or self.isShowTabBtnGuild() or self.isShowTabBtnCombat() or self.isShowTabBtnLevel() or self.isShowTabBtnHonor() or self.isShowTabBtnRace() or self.isShowTabFirstKill() or self.isShowTabLottery() or self.isShowTabFinalGuide() or self.isShowTabBtnDailyGift() or self.isShowTabCelebrate():
            return True
        else:
            return False

    def checkRedFlag(self):
        isRedPot = self.isShowCombatSocreRetPoint() or self.isShowLevelRetPoint() or self.isDailyGiftRedPoint() or gameglobal.rds.ui.newServiceWelfare.isShowWelfareRedPoint() or self.isFinalGuideRedPoint()
        return isRedPot

    def getTheFirstShowTabIndex(self):
        if self.isShowTabCelebrate():
            return const.NEW_SERVICE_EXP_BONUS
        if self.isShowTabBtnWelfare():
            return const.NEW_SERVICE_WELFARE
        if self.isShowTabBtnBox():
            return const.NEW_SERVICE_MALL_BOX
        if self.isShowTabBtnGuild():
            return const.NEW_SERVICE_TOP_RANK_GUILD
        if self.isShowTabBtnCombat():
            return const.NEW_SERVICE_TOP_RANK_COMBAT_SCORE
        if self.isShowTabBtnLevel():
            return const.NEW_SERVICE_TOP_RANK_COMBAT_LV
        if self.isShowTabBtnHonor():
            return const.NEW_SERVICE_TOP_RANK_HONOR
        if self.isShowTabBtnRace():
            return const.NEW_SERVICE_FUBEN_RACE
        if self.isShowTabFirstKill():
            return const.NEW_SERVICE_FIRST_KILL
        if self.isShowTabBtnDailyGift():
            appSetting.Obj[keys.SET_NEW_SERVICE_AVTIVITY_DAILY_GIFT_PUSH % BigWorld.player().gbId] = utils.getNow()
            return const.NEW_SERVICE_SECRET_MERCHANT
        if self.isShowTabLottery():
            return const.NEW_SERVICE_LOTTERY
        if self.isShowTabFinalGuide():
            return const.NEW_SERVICE_FINAL_GUIDE
