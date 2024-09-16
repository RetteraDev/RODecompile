#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/welfareProxy.o
from gamestrings import gameStrings
import BigWorld
import copy
import gameglobal
import uiUtils
import uiConst
import utils
import ui
from asObject import ASObject
from guis.ui import unicode2gbk
from uiProxy import UIProxy
from callbackHelper import Functor
from guis import events
from gamestrings import gameStrings
from data import push_data as PMD
from data import sys_config_data as SCD
from data import activity_signin_type_data as ASTD
from cdata import activity_achieve_score_bonus_data as AASBD
from data import login_time_reward_data as LTRD
from data import activity_achieve_score_config_data as AASCD
SIGN_IN_TYPE_NORNAL = 0
SIGN_IN_TYPE_FENWEI = 1

class WelfareProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(WelfareProxy, self).__init__(uiAdapter)
        self.modelMap = {'close': self.onClose,
         'changeTabIndex': self.onChangeTabIndex,
         'initTabInfo': self.onInitTabInfo,
         'updateAddParam': self.onUpdateAddParam,
         'initRewardRecovery': self.onInitRewardRecovery,
         'unRegistrRewardRecovery': self.onUnRegisterRewardRecovery,
         'initSignIn': self.onInitSignIn,
         'unRegistSignIn': self.onUnRegistSignIn,
         'initLottery': self.onInitLottery,
         'unRegistLottery': self.onUnRegistLottery,
         'initAppVip': self.onInitAppVip,
         'unRegistAppVip': self.onUnRegistAppVip,
         'initRewardCatchUp': self.onInitRewardCatchUp,
         'unRegistRewardCatchUp': self.onUnRegistRewardCatchUp}
        self.mediator = None
        self.tabIdx = uiConst.WELFARE_TAB_SEVENDAY_LOGIN
        self.cnt = 0
        self.addParams = {}
        self.addEvent(events.EVENT_ROLE_SET_LV, self.refreshInfo, isGlobal=True)
        uiAdapter.registerEscFunc(uiConst.WIDGET_WELFARE, self.checkAndHide)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_WELFARE:
            self.mediator = mediator
            self.isNeedRefreshItemUseData = True

    def clearWidget(self):
        self.mediator = None
        self.isNeedRefreshItemUseData = False
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_WELFARE)
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()

    def clearAll(self):
        self.cnt = 0

    def reset(self):
        self.tabIdx = uiConst.WELFARE_TAB_SEVENDAY_LOGIN
        self.addParams = {}

    def show(self, tabIdx, addParams = {}):
        self.tabIdx = tabIdx
        self.addParams.update(addParams)
        if self.mediator:
            self.refreshInfo()
        else:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_WELFARE)

    def onClose(self, *arg):
        self.checkAndHide()

    def checkAndHide(self):
        self.hide()

    def onChangeTabIndex(self, *arg):
        self.tabIdx = int(arg[3][0].GetNumber())

    def onUpdateAddParam(self, *arg):
        key = unicode2gbk(arg[3][0].GetString())
        value = int(arg[3][1].GetNumber())
        self.addParams[key] = value

    def onInitTabInfo(self, *arg):
        self.refreshInfo()

    def onInitRewardRecovery(self, *args):
        self.uiAdapter.welfareRewardRecovery.initRewardRecovery(ASObject(args[3][0]))

    def onUnRegisterRewardRecovery(self, *args):
        self.uiAdapter.welfareRewardRecovery.unRegisterRewardRecovery()

    def onInitSignIn(self, *args):
        self.uiAdapter.welfareSignIn.initSignIn(args[3][0], args[3][1])

    def onUnRegistSignIn(self, *args):
        self.uiAdapter.welfareSignIn.unRegistSignIn()

    def onInitLottery(self, *args):
        self.uiAdapter.welfareLottery.initLottery(args[3][0])

    def onUnRegistLottery(self, *args):
        self.uiAdapter.welfareLottery.unRegistLottery()

    def onInitAppVip(self, *args):
        self.uiAdapter.welfareAppVip.initAppVip(args[3][0])

    def onUnRegistAppVip(self, *args):
        self.uiAdapter.welfareAppVip.unRegistAppVip()

    def onInitRewardCatchUp(self, *args):
        self.uiAdapter.welfareRewardCatchUp.initRewardCatchUp(args[3][0])

    def onUnRegistRewardCatchUp(self, *args):
        self.uiAdapter.welfareRewardCatchUp.unRegistRewardCatchUp()

    @ui.callInCD(0.5)
    def refreshInfo(self):
        tabList = self.createTabList()
        labelTabList = self.createLabelTabList()
        if self.mediator:
            info = {}
            info['tabIdx'] = self.tabIdx
            info['tabList'] = tabList
            info['labelTabList'] = labelTabList
            info['addParams'] = copy.deepcopy(self.addParams)
            self.mediator.Invoke('refreshInfo', uiUtils.dict2GfxDict(info, True))
        cnt = 0
        showIdx = -1
        for tabInfo in tabList:
            if not tabInfo.get('redFlagVisible', False):
                continue
            if tabInfo['tabIdx'] == uiConst.WELFARE_TAB_REWARD_RECOVERY:
                continue
            cnt += 1
            if showIdx == -1:
                showIdx = tabInfo['tabIdx']

        for tabInfo in labelTabList:
            if not tabInfo.get('redFlagVisible', False):
                continue
            cnt += 1

        pushMsg = gameglobal.rds.ui.pushMessage
        if cnt == 0:
            pushMsg.removePushMsg(uiConst.MESSAGE_TYPE_WELFARE)
        oldFlag = self.checkRedFlag()
        self.cnt = cnt
        newFlag = self.checkRedFlag()
        if oldFlag != newFlag:
            gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()

    def createTabList(self):
        tabList = []
        self.addSevenDayLoginTab(tabList)
        self.addOnlineRewardTab(tabList)
        self.addSummerTab(tabList)
        self.addMergeServerTab(tabList)
        self.addEveryDayRewardTab(tabList)
        self.addRewardHallTab(tabList)
        self.addFudanTabs(tabList)
        self.addAccumulatedSignInTab(tabList)
        self.addRewardRecoveryTab(tabList)
        self.addSignInTab(tabList)
        self.addLotteryTab(tabList)
        self.addNeteaseAppVipTab(tabList)
        self.addRewardCatchUpTab(tabList)
        return tabList

    def createLabelTabList(self):
        labelTabList = []
        self.addGuideGoalTab(labelTabList)
        self.addNewbieGuideTab(labelTabList)
        return labelTabList

    def checkRedFlag(self):
        return self.cnt != 0

    def addAccumulatedSignInTab(self, tabList):
        if gameglobal.rds.configData.get('enableNoviceCheckInReward', False) and gameglobal.rds.ui.welfareAccumulatedSignIn.isTimeAvaliable():
            tabInfo = {}
            tabInfo['label'] = SCD.data.get('welfareSignInTitle', '')
            tabInfo['newFlagVisible'] = False
            tabInfo['tabIdx'] = uiConst.WELFARE_TAB_ACCUMULATED_SIGN_IN
            tabInfo['redFlagVisible'] = gameglobal.rds.ui.welfareAccumulatedSignIn.isHasReward()
            tabList.append(tabInfo)

    def addFudanTabs(self, tabList):
        if gameglobal.rds.configData.get('enableLoginReward', False):
            p = BigWorld.player()
            for key in p.fudanDict.keys():
                _data = LTRD.data.get(key, {})
                if _data.get('bonus', []):
                    name = _data.get('title', gameStrings.TEXT_MONSTERCLANWARACTIVITYPROXY_348)
                    tabInfo = {}
                    tabInfo['label'] = name
                    tabInfo['tabIdx'] = uiConst.WELFARE_TAB_FUDAN_REWARD
                    tabInfo['newFlagVisible'] = False
                    tabInfo['redFlagVisible'] = gameglobal.rds.ui.welfareFudanReward.isHasRewardById(key)
                    tabInfo['fudanActId'] = key
                    tabList.append(tabInfo)

    def addGuideGoalTab(self, tabList):
        if not gameglobal.rds.ui.topBar.checkGudeGoal():
            return
        tabInfo = {}
        tabInfo['label'] = uiUtils.toHtml(gameStrings.TEXT_WELFAREPROXY_236, linkEventTxt='uiShow:guideGoal.show()')
        tabInfo['redFlagVisible'] = gameglobal.rds.ui.guideGoal.canGainAward()
        tabList.append(tabInfo)

    def addNewbieGuideTab(self, tabList):
        if not gameglobal.rds.ui.newbieGuide.iconMediator:
            return
        tabInfo = {}
        tabInfo['label'] = uiUtils.toHtml(gameStrings.TEXT_WELFAREPROXY_245, linkEventTxt='uiShow:newbieGuide.showLvGuide()')
        tabInfo['redFlagVisible'] = gameglobal.rds.ui.newbieGuide.canGainAward()
        tabList.append(tabInfo)

    def addEveryDayRewardTab(self, tabList):
        p = BigWorld.player()
        tabInfo = {}
        tabInfo['label'] = gameStrings.TEXT_WELFAREPROXY_252
        tabInfo['tabIdx'] = uiConst.WELFARE_TAB_EVERYDAY_REWARD
        tabInfo['newFlagVisible'] = False
        if p.signInApplied >= 1:
            tabInfo['redFlagVisible'] = False
        else:
            tabInfo['redFlagVisible'] = True
        tabList.append(tabInfo)

    def addSevenDayLoginTab(self, tabList):
        if not gameglobal.rds.configData.get('enableNoviceCheckInRewardOld', False):
            return
        p = BigWorld.player()
        dayCnt = int(utils.calcDaysAfterEnterWorld(p))
        if dayCnt > uiConst.DAILY_SIGNIN_MAX_DAY or dayCnt < 0 or not self.checkDailySignInStartTime():
            return
        tabInfo = {}
        tabInfo['label'] = gameStrings.TEXT_WELFAREPROXY_270
        tabInfo['tabIdx'] = uiConst.WELFARE_TAB_SEVENDAY_LOGIN
        tabInfo['newFlagVisible'] = False
        tabInfo['redFlagVisible'] = not bool(1 << dayCnt & p.noviceSignInBM)
        tabList.append(tabInfo)

    def addOnlineRewardTab(self, tabList):
        p = BigWorld.player()
        dayCnt = int(utils.calcDaysAfterEnterWorld(p))
        if dayCnt > uiConst.DAILY_SIGNIN_MAX_DAY or dayCnt < 0 or not self.checkDailySignInStartTime() or gameglobal.rds.ui.welfareOnlineReward.getIsComplete():
            return
        tabInfo = {}
        tabInfo['label'] = gameStrings.TEXT_REWARDGIFTACTIVITYICONSPROXY_564
        tabInfo['tabIdx'] = uiConst.WELFARE_TAB_ONLINE_REWARD
        tabInfo['newFlagVisible'] = False
        tabInfo['redFlagVisible'] = gameglobal.rds.ui.welfareOnlineReward.isHasReward()
        tabList.append(tabInfo)

    def checkDailySignInStartTime(self):
        dailySignInStartTime = SCD.data.get('dailySignInStartTime', {})
        startTime = utils.getTimeSecondFromStr(dailySignInStartTime)
        return BigWorld.player().enterWorldTime >= startTime

    def addSummerTab(self, tabList):
        p = BigWorld.player()
        if not hasattr(p, 'newSignInInfo'):
            return
        for signId, newSignInInfo in p.newSignInInfo.iteritems():
            data = ASTD.data.get(signId, {})
            if data and data.get('activityType') == SIGN_IN_TYPE_NORNAL:
                tabInfo = {}
                tabInfo['label'] = ASTD.data.get(signId, {}).get('title', '')
                tabInfo['tabIdx'] = uiConst.WELFARE_TAB_SUMMER
                tabInfo['newFlagVisible'] = False
                if newSignInInfo:
                    tabInfo['redFlagVisible'] = not newSignInInfo.hasSignedToday()
                else:
                    tabInfo['redFlagVisible'] = False
                tabInfo['signId'] = signId
                tabList.append(tabInfo)

    def addMergeServerTab(self, tabList):
        activityScoreId = uiUtils.getActivityScoreId()
        if activityScoreId == 0:
            return
        tabInfo = {}
        tabInfo['label'] = AASCD.data.get(activityScoreId, {}).get('topic', '')
        tabInfo['tabIdx'] = uiConst.WELFARE_TAB_MERGE_SERVER
        tabInfo['newFlagVisible'] = False
        tabInfo['redFlagVisible'] = self.canMergeServer()
        tabList.append(tabInfo)

    def canMergeServer(self):
        p = BigWorld.player()
        rewardedActivityTypes = p.rewardedActivityTypes
        keys = AASBD.data.keys()
        activityScoreId = uiUtils.getActivityScoreId()
        achieveScores = getattr(p, 'activityAchieveScore', {}).get(activityScoreId, {})
        totalScore = achieveScores.get('val', 0)
        for key in keys:
            if key[0] != activityScoreId:
                continue
            if AASBD.data[key].get('score', 0) <= totalScore:
                if key not in rewardedActivityTypes:
                    return True

        return False

    def addRewardHallTab(self, tabList):
        p = BigWorld.player()
        tabInfo = {}
        tabInfo['label'] = gameStrings.TEXT_WELFAREPROXY_345
        tabInfo['tabIdx'] = uiConst.WELFARE_TAB_REWARD_HALL
        tabInfo['newFlagVisible'] = False
        tabInfo['redFlagVisible'] = p.checkNeedPushMsg()
        tabList.append(tabInfo)

    def addRewardRecoveryTab(self, tabList):
        if gameglobal.rds.configData.get('enableRewardRecoveryClient', False) and BigWorld.player().lv >= SCD.data.get('welfareRewardRecoveryTabLv', 20):
            tabInfo = {}
            tabInfo['label'] = gameStrings.WELFARE_REWARD_RECOVERY
            tabInfo['tabIdx'] = uiConst.WELFARE_TAB_REWARD_RECOVERY
            tabInfo['newFlagVisible'] = False
            tabInfo['redFlagVisible'] = self.uiAdapter.welfareRewardRecovery.getRedFlagVisible()
            tabList.append(tabInfo)

    def addSignInTab(self, tabList):
        if not gameglobal.rds.configData.get('enableNewActivitySignin', False):
            return
        p = BigWorld.player()
        if not hasattr(p, 'newSignInInfo'):
            return
        for signId, newSignInInfo in p.newSignInInfo.iteritems():
            data = ASTD.data.get(signId, {})
            if data and data.get('activityType') == SIGN_IN_TYPE_FENWEI:
                tabInfo = {}
                tabInfo['label'] = ASTD.data.get(signId, {}).get('title', '')
                tabInfo['tabIdx'] = uiConst.WELFARE_TAB_SIGN_IN
                tabInfo['newFlagVisible'] = False
                if newSignInInfo:
                    tabInfo['redFlagVisible'] = not newSignInInfo.hasSignedToday()
                else:
                    tabInfo['redFlagVisible'] = False
                tabInfo['signId'] = signId
                tabList.append(tabInfo)

    def addLotteryTab(self, tabList):
        if gameglobal.rds.ui.welfareLottery.isOpen():
            tabInfo = {}
            tabInfo['label'] = self.uiAdapter.welfareLottery.getLotteryLabel()
            tabInfo['tabIdx'] = uiConst.WELFARE_TAB_LOTTERY
            tabInfo['newFlagVisible'] = False
            tabInfo['redFlagVisible'] = self.uiAdapter.welfareLottery.getRedFlagVisible()
            tabList.append(tabInfo)

    def addNeteaseAppVipTab(self, tabList):
        if gameglobal.rds.ui.welfareAppVip.isOpen():
            tabInfo = {}
            tabInfo['label'] = gameglobal.rds.ui.welfareAppVip.getAppVipLabel()
            tabInfo['tabIdx'] = uiConst.WELFARE_TAB_NETEASE_APP_VIP
            tabInfo['newFlagVisible'] = False
            tabInfo['redFlagVisible'] = gameglobal.rds.ui.welfareAppVip.getRedFlagVisible()
            tabList.append(tabInfo)

    def addRewardCatchUpTab(self, tabList):
        if gameglobal.rds.ui.welfareRewardCatchUp.isOpen():
            tabInfo = {}
            tabInfo['label'] = SCD.data.get('reward_catch_up_title', gameStrings.WELFARE_REWARD_CATCH_UP)
            tabInfo['tabIdx'] = uiConst.WELFARE_TAB_REWARD_CATCH_UP
            tabInfo['newFlagVisible'] = False
            tabInfo['redFlagVisible'] = gameglobal.rds.ui.welfareRewardCatchUp.getRedFlagVisible()
            tabList.append(tabInfo)
