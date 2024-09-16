#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\guis/rewardGiftActivityIconsProxy.o
from gamestrings import gameStrings
import BigWorld
from Scaleform import GfxValue
import gameglobal
import zmjCommon
import mapGameCommon
import uiConst
import utils
import uiUtils
import ui
from ui import gbk2unicode
import const
import gametypes
import datetime
import events
from gamestrings import gameStrings
from callbackHelper import Functor
from uiProxy import UIProxy
from data import sys_config_data as SCD
from data import login_time_reward_data as LTRD
from data import private_shop_data as PSD
from cdata import game_msg_def_data as GMDD
from data import hall_of_fame_config_data as HOFCD
from data import cross_guild_tournament_schedule_data as CGTSD
from data import arena_playoffs_group_duel_data as APGDD
from data import arena_score_group_duel_data as ASGDD
from data import arena_5v5_group_duel_data as A5GDD
from data import fame_data as FD
from data import zmj_fuben_config_data as ZFCD
from data import challenge_passport_config_data as CPCD
from data import map_game_config_data as MGCD
TIME_FORMAT_TYPE_1 = 1
TIME_FORMAT_TYPE_2 = 2

class RewardGiftActivityIconsProxy(UIProxy):

    def __init__(self, uiAdapter):
        super(RewardGiftActivityIconsProxy, self).__init__(uiAdapter)
        self.bindType = 'rewardGiftActivityIcons'
        self.modelMap = {'clickIcon': self.onClickIcon}
        self.mediator = None
        self.timer = None
        self.shineMap = {'activitySaleIcon': True,
         'privateShop': False,
         'prettyGirl': True,
         'backflowIcon': True}
        self.updateMap = {}
        self.msgCallBackDict = {}
        self.updateCallBack = None
        self.addEvent(events.EVENT_FAME_UPDATE, self.handleFameUpdate)
        self.addEvent(events.EVENT_ROLE_SET_LV, self.handlePlayerLvChanged)
        self.addEvent(events.EVENT_REWARD_GIFT_ACTIVITY_ICONS_UPDATE, self.updateIconsListener)

    def _registerMediator(self, widgetId, mediator):
        if widgetId == uiConst.WIDGET_REWARD_GIFT_ACTIVITY_ICONS:
            self.mediator = mediator
            self.stopTimer()
            self.updateTime()

    def show(self):
        if not self.mediator:
            gameglobal.rds.ui.loadWidget(uiConst.WIDGET_REWARD_GIFT_ACTIVITY_ICONS)
        else:
            self.updateInfo()
        p = BigWorld.player()
        BigWorld.callback(1, p.getNewServerBothRankData)

    def clearWidget(self):
        self.mediator = None
        self.stopTimer()
        self.cancelUpdateCallBack()
        self.cancelAllCallMsgBack()
        gameglobal.rds.ui.unLoadWidget(uiConst.WIDGET_REWARD_GIFT_ACTIVITY_ICONS)

    def clearAll(self):
        self.shineMap = {'activitySaleIcon': True,
         'backflowIcon': True}

    def stopTimer(self):
        if self.timer:
            BigWorld.cancelCallback(self.timer)
            self.timer = None

    def updateTime(self):
        if self.mediator:
            self.updateInfo()
            self.timer = BigWorld.callback(600, self.updateTime)

    def cancelUpdateCallBack(self):
        if self.updateCallBack:
            BigWorld.cancelCallback(self.updateCallBack)
            self.updateCallBack = None

    def setUpdateCallBack(self, delayTime = 0):
        if self.mediator:
            self.cancelUpdateCallBack()
        if delayTime:
            self.updateCallBack = BigWorld.callback(delayTime, self.updateInfo)

    @ui.callInCD(0.5)
    def updateInfo(self):
        if self.mediator:
            ret = {}
            p = BigWorld.player()
            if gameglobal.rds.configData.get('enableRewardGiftActivityIcons', False) and not p._isSoul() and not p.inFubenTypes(const.FB_TYPE_BATTLE_FIELD):
                self.appendActivitySale(ret)
                self.appendWelfare(ret)
                self.appendGuideGoal(ret)
                self.appendOnlineReward(ret)
                self.appendFudanReward(ret)
                self.appendActivityShop(ret)
                self.appendCelebrityHall(ret)
                self.appendPrettyGirlIcon(ret)
                self.appendFriendIcon(ret)
                self.appendBackflowIcon(ret)
                self.appendDeedLearningShopIcon(ret)
                self.appendDefaultShopIcon(ret)
                self.appendNewServerTopRank(ret)
                self.appendLiveStreamingIcon(ret)
                self.appendZhanmo(ret)
                self.appendHistoryConsumedIcon(ret)
                self.appendNewServeiceActivitiesIcon(ret)
                self.appendChallengePassportIcon(ret)
                self.appendMissTianyuGroup(ret)
                self.appendStraightUp(ret)
                self.setNearlyUpdate()
                self.appendRandomTreasureBagMain(ret)
                self.appendBetIcon(ret)
                self.appendMapGameIcon(ret)
                self.appendMapGameV2Icon(ret)
                self.appendRewardCatchUp(ret)
            self.mediator.Invoke('refreshContent', uiUtils.dict2GfxDict(ret, True))

    def appendFudanReward(self, ret):
        if gameglobal.rds.configData.get('enableLoginReward', False):
            p = BigWorld.player()
            fudanIcons = []
            for key in p.fudanDict.keys():
                _data = LTRD.data.get(key, {})
                if _data.get('bonus', []):
                    iconType = 'fudan' + str(_data.get('icon', 1))
                    hasNewInfo = False
                    isShine = False
                    clickHideShine = False
                    tip = _data.get('title', gameStrings.TEXT_MONSTERCLANWARACTIVITYPROXY_348)
                    timeInfo = {}
                    timeInfo['timeGoal'] = p.fudanDict[key][2]
                    _info = {'iconType': iconType,
                     'hasNewInfo': hasNewInfo,
                     'isShine': isShine,
                     'clickHideShine': clickHideShine,
                     'tip': tip,
                     'timeInfo': timeInfo,
                     'fudanActId': key}
                    fudanIcons.append(_info)

            ret['fudanIcons'] = fudanIcons

    def appendZhanmo(self, ret):
        if gameglobal.rds.configData.get('enableZMJFuben', False):
            p = BigWorld.player()
            minLvNeed = ZFCD.data.get('minLvNeed', 0)
            if zmjCommon.checkinZMJTime() and p.lv >= minLvNeed:
                redPoint = gameglobal.rds.ui.zmjActivityBg.hasNewInfo()
                iconType = 'zhanmo'
                _info = {'iconType': iconType,
                 'hasNewInfo': redPoint,
                 'isShine': redPoint,
                 'clickHideShine': False,
                 'tip': ''}
                ret['zhanmo'] = _info

    def appendLiveStreamingIcon(self, ret):
        if gameglobal.rds.configData.get('enableLiveStreamingIcon', False):
            try:
                state, nextUpdateTime = self.getCurStreamingState()
                if state:
                    iconType = 'sai'
                    tip = SCD.data.get('liveStreamingCrossGuildTimeTips', {}).get(state, '')
                    _info = {'iconType': iconType,
                     'hasNewInfo': False,
                     'isShine': False,
                     'clickHideShine': True,
                     'tip': tip,
                     'liveState': state}
                    ret['liveStreaming'] = _info
                    self.updateMap['liveStreaming'] = nextUpdateTime
            except Exception as e:
                msg = ('appendLiveStreamingIcon error:%s', e.message)
                BigWorld.player().reportClientException(gametypes.CLIENT_EXCEPTION_TYPE_SCRIPT, [msg], 0, {})

    def isPlayOffsOpen(self):
        p = BigWorld.player()
        if p.isBalancePlayoffs():
            return True
        if p.isPlayoffs5V5():
            return True
        if gameglobal.rds.configData.get('enableArenaPlayoffs', False):
            return True
        return False

    def getCurStreamingState(self):
        curState = None
        cronTime = []
        strTime = []
        nearlyUpdateTime = 0
        timeOffset = SCD.data.get('liveStreamingWudaohuiTimeOffset', 0)
        if self.isPlayOffsOpen():
            curArenaState = self.uiAdapter.arenaPlayoffs.getCurrentPlayoffsState()
            p = BigWorld.player()
            data = {}
            if p.isBalancePlayoffs():
                groupSchedule = gameglobal.rds.ui.balanceArenaPlayoffs.getMatchesSchedule()
                finalSchedule = gameglobal.rds.ui.balanceArenaPlayoffs.getArenaFinalSchedule()
                i = 0
                for item in groupSchedule:
                    data[i] = item
                    i += 1

                for item in finalSchedule:
                    data[i] = item
                    i += 1

            elif p.isPlayoffs5V5():
                groupSchedule = gameglobal.rds.ui.pvpPlayoffs5V5.getMatchesSchedule()
                finalSchedule = gameglobal.rds.ui.arenaPlayoffs5v5Final.getArenaFinalSchedule()
                i = 0
                for item in groupSchedule:
                    data[i] = item
                    i += 1

                for item in finalSchedule:
                    data[i] = item
                    i += 1

            else:
                data = APGDD.data
            for key, val in data.iteritems():
                if val.get('type') == curArenaState:
                    timeState = self.uiAdapter.arenaPlayoffs.getTimeState(val.get('startTime'), val.get('endTime'), timeOffset)
                    if timeState == uiConst.ARENA_PLAYOFFS_PRE_STATE:
                        strTime.append(val.get('startTime'))
                    if timeState == uiConst.ARENA_PLAYOFFS_PLAYING_STATE:
                        curState = uiConst.REWARD_ICON_LIVE_STREAM_TYPE_WUDAOHUI
                        strTime.append(val.get('endTime'))

        crossGuildLiveStreamingTime = SCD.data.get('liveStreamingCrossGuildTime', ())
        for startIdx, endIdx in crossGuildLiveStreamingTime:
            sc = CGTSD.data.get(startIdx, {}).get('crontab', '')
            weekNum = CGTSD.data.get(startIdx, {}).get('weekNum', '')
            monthNum = CGTSD.data.get(startIdx, {}).get('monthNum', 0)
            curMonth = utils.getMonthInt()
            curMonthDay = utils.getMonthDayInt()
            curYear = utils.getYearInt()
            curWeek = self.getCurWeekNum(curYear, curMonth, curMonthDay)
            ec = CGTSD.data.get(endIdx, {}).get('crontab', '')
            if curMonth == monthNum:
                cronTime.append((sc, weekNum))
                cronTime.append((ec, weekNum))
                if utils.inCrontabRange(sc, ec) and curWeek == weekNum:
                    curState = uiConst.REWARD_ICON_LIVE_STREAM_TYPE_CROSS_GUILD

        liveStreamingTempTime = SCD.data.get('liveStreamingTempTime', ())
        for startCron, endCron, weekNum in liveStreamingTempTime:
            cronTime.append((startCron, weekNum))
            cronTime.append((endCron, weekNum))
            curMonth = utils.getMonthInt()
            curMonthDay = utils.getMonthDayInt()
            curYear = utils.getYearInt()
            curWeek = self.getCurWeekNum(curYear, curMonth, curMonthDay)
            if utils.inCrontabRange(startCron, endCron) and curWeek == weekNum:
                curState = uiConst.REWARD_ICON_LIVE_STREAM_TYPE_TEMP

        if curState:
            nearlyTimes = [ utils.getTimeSecondFromStr(sTime) - utils.getNow() for sTime in strTime ] + [ utils.getNextCrontabTime(cron) - utils.getNow() for cron, weekNum in cronTime ]
            nearlyUpdateTime = min(nearlyTimes)
        return (curState, nearlyUpdateTime)

    def getCurWeekNum(self, year, month, day):
        end = int(datetime.datetime(year, month, day).strftime('%W'))
        begin = int(datetime.datetime(year, month, 1).strftime('%W'))
        return end - begin

    def appendActivityShop(self, ret):
        if not self.uiAdapter.activityShop.canOpen():
            return
        iconType = 'shang'
        hasNewInfo = gameglobal.rds.ui.activityShop.hasNewInfo()
        isShine = gameglobal.rds.ui.activityShop.getNRefreshTime() <= utils.getNow()
        self.shineMap['privateShop'] = isShine
        clickHideShine = True
        tip = SCD.data.get('activityShopName', '')
        _info = {'iconType': iconType,
         'hasNewInfo': hasNewInfo,
         'isShine': isShine,
         'clickHideShine': clickHideShine,
         'tip': tip}
        ret['activityShopIcon'] = _info

    def appendActivitySale(self, ret):
        if not gameglobal.rds.configData.get('enableActivitySale', False):
            return
        if BigWorld.player().lv < SCD.data.get('activitySaleMinLv', 0):
            return
        if not gameglobal.rds.ui.activitySale.checkPanelVisible():
            return
        iconType = 'hui'
        hasNewInfo = gameglobal.rds.ui.activitySale.checkRedFlag()
        isShine = self.shineMap.get('activitySaleIcon', False)
        clickHideShine = True
        tip = gameStrings.TEXT_REWARDGIFTACTIVITYICONSPROXY_352
        _info = {'iconType': iconType,
         'hasNewInfo': hasNewInfo,
         'isShine': isShine,
         'clickHideShine': clickHideShine,
         'tip': tip}
        ret['activitySaleIcon'] = _info

    def appendRandomTreasureBagMain(self, ret):
        if not gameglobal.rds.configData.get('enableRandomTreasureBagMain', False):
            return
        if not gameglobal.rds.ui.randomTreasureBagMain.checkCanOpenMainProxy():
            return
        iconType = 'baibaodai'
        hasNewInfo = gameglobal.rds.ui.randomTreasureBagMain.checkHaveNewReward()
        isShine = False
        clickHideShine = True
        tip = gameStrings.RANDOM_TREASURE_BAG_REWARD_ICON_HINT
        _info = {'iconType': iconType,
         'hasNewInfo': hasNewInfo,
         'isShine': isShine,
         'clickHideShine': clickHideShine,
         'tip': tip}
        ret['randomTreasureBagMainIcon'] = _info

    def appendWelfare(self, ret):
        iconType = 'fu'
        hasNewInfo = gameglobal.rds.ui.welfare.checkRedFlag()
        isShine = False
        clickHideShine = False
        tip = gameStrings.TEXT_REWARDGIFTACTIVITYICONSPROXY_393
        _info = {'iconType': iconType,
         'hasNewInfo': hasNewInfo,
         'isShine': isShine,
         'clickHideShine': clickHideShine,
         'tip': tip}
        ret['welfareIcon'] = _info

    def appendNewServerTopRank(self, ret):
        if not gameglobal.rds.ui.newServerTopRankMain.checkOpen():
            return
        iconType = 'newServer'
        hasNewInfo = False
        isShine = False
        clickHideShine = False
        tip = gameStrings.NEW_SERVER_TOP_RANK_NAME
        _info = {'iconType': iconType,
         'hasNewInfo': hasNewInfo,
         'isShine': isShine,
         'clickHideShine': clickHideShine,
         'tip': tip}
        ret['newServerTopRankIcon'] = _info

    def appendNewServeiceActivitiesIcon(self, ret):
        if not gameglobal.rds.configData.get('enableNewServerActivity', ''):
            return
        if not gameglobal.rds.ui.newServiceActivities.checkNewServiceActivitiesOpen():
            return
        iconType = 'newService'
        hasNewInfo = gameglobal.rds.ui.newServiceActivities.checkRedFlag()
        isShine = False
        clickHideShine = False
        tip = gameStrings.NEW_SERVICE_ACTIVITIES_NAME
        _info = {'iconType': iconType,
         'hasNewInfo': hasNewInfo,
         'isShine': isShine,
         'clickHideShine': clickHideShine,
         'tip': tip}
        ret['newServeiceActivitiesIcon'] = _info

    def appendChallengePassportIcon(self, ret):
        if not gameglobal.rds.configData.get('enableChallengePassport', ''):
            return
        if not uiUtils.isInChallengePassport():
            return
        p = BigWorld.player()
        if p.lv < CPCD.data.get('challengePassportAvatarLvLimit', 20):
            return
        iconType = 'passport'
        hasNewInfo = gameglobal.rds.ui.challengePassportMain.checkRedPointVisible()
        isShine = hasNewInfo
        clickHideShine = True
        tip = gameStrings.CHALLENGE_PASSPORT_ICON_TIP
        phaseInfo = str(p.challengePassportData.lv)
        _info = {'iconType': iconType,
         'hasNewInfo': hasNewInfo,
         'isShine': isShine,
         'clickHideShine': clickHideShine,
         'tip': tip,
         'phaseInfo': phaseInfo}
        ret['challengePassportIcon'] = _info

    def appendMissTianyuGroup(self, ret):
        if not gameglobal.rds.configData.get('enableNewMissTianyu', ''):
            return
        p = BigWorld.player()
        if not p.isMTInGroupTime() and not p.isMTInPlayoffTime():
            return
        iconType = 'meng'
        hasNewInfo = False
        isShine = hasNewInfo
        clickHideShine = True
        tip = ''
        phaseInfo = ''
        _info = {'iconType': iconType,
         'hasNewInfo': hasNewInfo,
         'isShine': isShine,
         'clickHideShine': clickHideShine,
         'tip': tip,
         'phaseInfo': phaseInfo}
        ret['missTianyuGroup'] = _info

    def appendStraightUp(self, ret):
        if not gameglobal.rds.configData.get('enableStraightLvUpV2', False):
            return
        if not gameglobal.rds.ui.straightUp.isNeedShow():
            return
        iconType = 'zhisheng'
        hasNewInfo = gameglobal.rds.ui.straightUp.checkRedPointVisible()
        isShine = gameglobal.rds.ui.straightUp.checkTaskUnfinished()
        clickHideShine = True
        tip = ''
        _info = {'iconType': iconType,
         'hasNewInfo': hasNewInfo,
         'isShine': isShine,
         'clickHideShine': clickHideShine,
         'tip': tip}
        ret['straightUpIcon'] = _info

    def setNewServerRedPoint(self, topType, value):
        if not hasattr(self, 'newServerRedPoint'):
            self.newServerRedPoint = {}
        self.newServerRedPoint[topType] = value

    def getNewServerRedPoint(self):
        result = False
        if not hasattr(self, 'newServerRedPoint'):
            return result
        for k, v in self.newServerRedPoint.items():
            if isinstance(k, basestring) and gameglobal.rds.ui.newServiceActivities.checkCombatAndLvOpen(int(k.split('/')[0])) and v:
                result = True

        return result

    def appendGuideGoal(self, ret):
        if not gameglobal.rds.ui.topBar.checkGudeGoal():
            return
        iconType = 'xiu'
        hasNewInfo = gameglobal.rds.ui.guideGoal.canGainAward()
        isShine = False
        clickHideShine = False
        guideGoalMinLv = SCD.data.get('guideGoalMinLv', 0)
        if BigWorld.player().lv < guideGoalMinLv:
            tip = gameStrings.TEXT_REWARDGIFTACTIVITYICONSPROXY_542 % guideGoalMinLv
        else:
            tip = gameStrings.TEXT_WELFAREPROXY_236
        _info = {'iconType': iconType,
         'hasNewInfo': hasNewInfo,
         'isShine': isShine,
         'clickHideShine': clickHideShine,
         'tip': tip}
        ret['guideGoalIcon'] = _info

    def appendOnlineReward(self, ret):
        if gameglobal.rds.configData.get('enableNoviceReward', False) and self.isShowOnlineRewardIcon() and self.checkDailySignInStartTime() and not gameglobal.rds.ui.welfareOnlineReward.getIsComplete():
            iconType = 'jiang'
            hasNewInfo = False
            isShine = False
            clickHideShine = False
            tip = gameStrings.TEXT_REWARDGIFTACTIVITYICONSPROXY_564
            timeInfo = {}
            timeInfo['timeGoal'] = gameglobal.rds.ui.welfareOnlineReward.getCurrentRewardTime() + utils.getNow()
            _info = {'iconType': iconType,
             'hasNewInfo': hasNewInfo,
             'isShine': isShine,
             'clickHideShine': clickHideShine,
             'tip': tip,
             'timeInfo': timeInfo}
            ret['onlineRewardIcon'] = _info

    def appendCelebrityHall(self, ret):
        if not gameglobal.rds.ui.celebrityRank.checkMainIconCanShow():
            return
        iconType = 'ming'
        hasNewInfo = False
        isShine = False
        clickHideShine = False
        tip = HOFCD.data.get('activityIconTip', '')
        _info = {'iconType': iconType,
         'hasNewInfo': hasNewInfo,
         'isShine': isShine,
         'clickHideShine': clickHideShine,
         'tip': tip}
        ret['celebrityHallIcon'] = _info

    def appendPrettyGirlIcon(self, ret):
        p = BigWorld.player()
        timeDiff = gameglobal.rds.configData.get('missTianyuEndtime', 0) - utils.getNow()
        if gameglobal.rds.configData.get('enableMissTianyu', False) and timeDiff > 0 and not p.lv < const.PRETTY_GIRL_LV_LIMIT:
            iconType = 'meng'
            hasNewInfo = False
            isShine = self.shineMap.get('prettyGirl', False)
            clickHideShine = True
            tip = gameStrings.PRETTY_GIRL_TIPS
            _info = {'iconType': iconType,
             'hasNewInfo': hasNewInfo,
             'isShine': isShine,
             'clickHideShine': clickHideShine,
             'tip': tip}
            ret['prettyGirl'] = _info
            self.updateMap['prettyGirl'] = timeDiff

    def appendFriendIcon(self, ret):
        if not gameglobal.rds.configData.get('enableIMOptimize', True):
            return
        if not gameglobal.rds.configData.get('enableFriendInviteActivityOp', True):
            return
        iconType = 'friend'
        hasNewInfo = gameglobal.rds.ui.summonFriendBackV2.checkRedFlag()
        isShine = False
        clickHideShine = True
        tip = gameStrings.INVITE_FRIEND_PLAY
        _info = {'iconType': iconType,
         'hasNewInfo': hasNewInfo,
         'isShine': isShine,
         'clickHideShine': clickHideShine,
         'tip': tip}
        ret['friendIcon'] = _info

    def appendBackflowIcon(self, ret):
        if not gameglobal.rds.configData.get('enableFlowbackGroup', False):
            return
        if not gameglobal.rds.ui.backflow.checkBackflow():
            return
        if gameglobal.rds.ui.backflow.checkBackflowTimeEnd():
            return
        iconType = 'huiliu'
        hasNewInfo = gameglobal.rds.ui.backflow.checkRedFlag()
        isShine = self.shineMap.get('backflowIcon', False)
        clickHideShine = True
        tip = SCD.data.get('backflowActivityIconTip', '')
        _info = {'iconType': iconType,
         'hasNewInfo': hasNewInfo,
         'isShine': isShine,
         'clickHideShine': clickHideShine,
         'tip': tip}
        ret['backflowIcon'] = _info

    def appendDeedLearningShopIcon(self, ret):
        if not gameglobal.rds.configData.get('enableDeepLearningDataApply', False):
            return
        p = BigWorld.player()
        if not p.deepLearningData:
            return
        if gameglobal.rds.ui.deepLearningShop.checkTimeEnd():
            return
        iconType = 'huili'
        hasNewInfo = False
        isShine = False
        clickHideShine = True
        tip = SCD.data.get('deepLearningShopIconTip', '')
        _info = {'iconType': iconType,
         'hasNewInfo': hasNewInfo,
         'isShine': isShine,
         'clickHideShine': clickHideShine,
         'tip': tip}
        ret['deepLearningShopIcon'] = _info

    def appendDefaultShopIcon(self, ret):
        iconType = 'defaultShop'
        hasNewInfo = gameglobal.rds.ui.tianyuMall.isHasNewInfo()
        isShine = False
        clickHideShine = True
        tip = gameStrings.DEFAULT_SHOP_ICON_TIP
        _info = {'iconType': iconType,
         'hasNewInfo': hasNewInfo,
         'isShine': isShine,
         'clickHideShine': clickHideShine,
         'tip': tip}
        ret['defaultShopIcon'] = _info

    def appendHistoryConsumedIcon(self, ret):
        if not gameglobal.rds.configData.get('enableHistoryConsumed', False):
            return
        if not gameglobal.rds.ui.historyConsumed.isOpen():
            return
        iconType = 'history'
        hasNewInfo = gameglobal.rds.ui.historyConsumed.checkRedFlag()
        isShine = False
        clickHideShine = True
        tip = gameStrings.HISTORY_CONSUMED_ICON_TIP
        _info = {'iconType': iconType,
         'hasNewInfo': hasNewInfo,
         'isShine': isShine,
         'clickHideShine': clickHideShine,
         'tip': tip}
        ret['historyConsumedIcon'] = _info

    def appendBetIcon(self, ret):
        if not gameglobal.rds.configData.get('enableBet', False):
            return
        if not gameglobal.rds.ui.generalBet.isOpen():
            return
        hasNewInfo = gameglobal.rds.ui.generalBet.hasNewInfo()
        isShine = hasNewInfo
        clickHideShine = False
        iconType = 'jingcai'
        tip = gameStrings.DEFAULT_BET_ICON_TIP
        _info = {'iconType': iconType,
         'hasNewInfo': hasNewInfo,
         'isShine': isShine,
         'clickHideShine': clickHideShine,
         'tip': tip}
        ret['betIcon'] = _info

    def appendMapGameIcon(self, ret):
        if mapGameCommon.checkVersion() != uiConst.MAP_GAME_VERSION_1:
            return
        if not gameglobal.rds.ui.mapGameMap.isOpen():
            return
        iconType = 'mapgame'
        hasNewInfo = gameglobal.rds.ui.mapGameMap.checkRedFlag()
        tip = MGCD.data.get('mapGameIconTip', gameStrings.MAP_GAME_ICON_TIP)
        _info = {'iconType': iconType,
         'hasNewInfo': hasNewInfo,
         'isShine': False,
         'clickHideShine': True,
         'tip': tip}
        ret['mapGameIcon'] = _info

    def appendMapGameV2Icon(self, ret):
        if mapGameCommon.checkVersion() != uiConst.MAP_GAME_VERSION_2:
            return
        if not gameglobal.rds.ui.mapGameMapV2.isOpen():
            return
        iconType = 'mapgame2'
        hasNewInfo = gameglobal.rds.ui.mapGameMapV2.checkRedFlag()
        tip = MGCD.data.get('mapGameIconTip', gameStrings.MAP_GAME_ICON_TIP_V2)
        _info = {'iconType': iconType,
         'hasNewInfo': hasNewInfo,
         'isShine': False,
         'clickHideShine': True,
         'tip': tip}
        ret['mapGameV2Icon'] = _info

    def appendRewardCatchUp(self, ret):
        if not gameglobal.rds.ui.welfareRewardCatchUp.isOpen():
            return
        iconType = 'zhuigan'
        hasNewInfo = gameglobal.rds.ui.welfareRewardCatchUp.getRedFlagVisible()
        tip = gameStrings.WELFARE_REWARD_CATCH_UP_TIP
        _info = {'iconType': iconType,
         'hasNewInfo': hasNewInfo,
         'isShine': False,
         'clickHideShine': True,
         'tip': tip}
        ret['RewardCatchUp'] = _info

    def setNearlyUpdate(self):
        if self.mediator:
            key = None
            value = None
            for k, v in self.updateMap.iteritems():
                if not value or v and v < value:
                    value = v
                    key = k

            if key and value:
                self.setUpdateCallBack(value)
                del self.updateMap[key]

    def isShowOnlineRewardIcon(self):
        p = BigWorld.player()
        dayCnt = int(utils.calcDaysAfterEnterWorld(p))
        if dayCnt > uiConst.DAILY_SIGNIN_MAX_DAY or dayCnt < 0:
            ret = False
        else:
            ret = True
        return ret

    def checkDailySignInStartTime(self):
        p = BigWorld.player()
        dailySignInStartTime = SCD.data.get('dailySignInStartTime', {})
        startTime = utils.getTimeSecondFromStr(dailySignInStartTime)
        return p.enterWorldTime >= startTime

    def onClickIcon(self, *args):
        iconName = args[3][0].GetString()
        p = BigWorld.player()
        if iconName == 'activitySaleIcon':
            self.shineMap['activitySaleIcon'] = False
            gameglobal.rds.ui.activitySale.show(uiConst.ACTIVITY_SALE_TAB_FIRST_PAY)
        elif iconName == 'randomTreasureBagMainIcon':
            gameglobal.rds.ui.randomTreasureBagMain.show(checkHaveNewReward=True, enableScrollToCurBag=True)
        elif iconName == 'welfareIcon':
            gameglobal.rds.ui.welfare.show(uiConst.WELFARE_TAB_SEVENDAY_LOGIN)
        elif iconName == 'guideGoalIcon':
            gameglobal.rds.ui.guideGoal.show()
        elif iconName == 'onlineRewardIcon':
            gameglobal.rds.ui.welfare.show(uiConst.WELFARE_TAB_ONLINE_REWARD)
        elif iconName == 'fudanIcon':
            fudanActId = int(args[3][1].GetNumber())
            addParam = {'fudanActId': fudanActId}
            gameglobal.rds.ui.welfare.show(uiConst.WELFARE_TAB_FUDAN_REWARD, addParam)
        elif iconName == 'activityShopIcon':
            if self.uiAdapter.activityShop.canOpen():
                BigWorld.player().getCurrPrivateShop()
            else:
                BigWorld.player().showGameMsg(GMDD.data.ACTIVITY_SHOP_CLOSED, ())
        elif iconName == 'celebrityHallIcon':
            gameglobal.rds.ui.celebrityRank.show()
        elif iconName == 'prettyGirl':
            self.shineMap['prettyGirl'] = False
            enabled = gameglobal.rds.configData.get('enableMissTianyu', False) and utils.getNow() < gameglobal.rds.configData.get('missTianyuEndtime', 0)
            if enabled:
                ziXunUrl = SCD.data.get('ZiXunUrl', [])
                ziXunIdx = -1
                if 'personalZone' in ziXunUrl:
                    ziXunIdx = ziXunUrl.index('personalZone')
                    if ziXunIdx != -1:
                        self.uiAdapter.ziXunInfo.show(ziXunIdx)
        elif iconName == 'friendIcon':
            gameglobal.rds.ui.friend.onShowSprite()
        elif iconName == 'backflowIcon':
            self.shineMap['backflowIcon'] = False
            if not gameglobal.rds.ui.backflow.checkBackflow():
                BigWorld.player().showGameMsg(GMDD.data.THE_BACK_FLOW_ACTIVITY_END, ())
                return
            gameglobal.rds.ui.backflow.show()
        elif iconName == 'deepLearningShopIcon':
            gameglobal.rds.ui.deepLearningShop.show()
        elif iconName == 'newServerTopRankIcon':
            gameglobal.rds.ui.newServerTopRankMain.show()
        elif iconName == 'defaultShopIcon':
            mall = gameglobal.rds.ui.tianyuMall
            if mall.mallMediator:
                mall.hide()
            mall.show()
        elif iconName == 'liveStreaming':
            liveState = int(args[3][1].GetNumber())
            urlDict = SCD.data.get('liveStreamingCrossGuildTimeUrl', {})
            BigWorld.openUrl(urlDict.get(liveState, ''))
        elif iconName == 'historyConsumedIcon':
            gameglobal.rds.ui.historyConsumed.show()
        elif iconName == 'newServeiceActivitiesIcon':
            tabIndex = gameglobal.rds.ui.newServiceActivities.getTheFirstShowTabIndex()
            gameglobal.rds.ui.newServiceActivities.show(tabIndex)
        elif iconName == 'zhanmo':
            gameglobal.rds.ui.zmjActivityBg.show()
        elif iconName == 'challengePassportIcon':
            gameglobal.rds.ui.challengePassportMain.show()
        elif iconName == 'missTianyuGroup':
            p = BigWorld.player()
            if p.isMTInGroupTime():
                gameglobal.rds.ui.missTianyuGroupTopRank.show(gametypes.TOP_TYPE_MISS_TIANYU_GROUP)
            elif p.isMTInPlayoffTime():
                gameglobal.rds.ui.missTianyuGroupTopRank.show(gametypes.TOP_TYPE_MISS_TIANYU_PLAYOFF)
        elif iconName == 'straightUpIcon':
            gameglobal.rds.ui.straightUp.show()
        elif iconName == 'betIcon':
            gameglobal.rds.ui.generalBet.show()
        elif iconName == 'mapGameIcon':
            gameglobal.rds.ui.mapGameMap.show()
        elif iconName == 'mapGameV2Icon':
            gameglobal.rds.ui.mapGameMapV2.show()
        elif iconName == 'RewardCatchUp':
            gameglobal.rds.ui.welfare.show(uiConst.WELFARE_TAB_REWARD_CATCH_UP)

    def handleFameUpdate(self, e):
        if e.data in (const.ZMJ_ZHANMO_FAME_ID, const.ZMJ_TAOFA_FAME_ID, const.ZMJ_GONGXIAN_FAME_ID):
            self.updateInfo()

    def handlePlayerLvChanged(self, e):
        self.updateInfo()

    def updateIconsListener(self):
        self.updateInfo()

    def popMessage(self, iconName, msg, duration = 0):
        if not self.mediator:
            return
        else:
            if self.msgCallBackDict.get(iconName, None):
                BigWorld.cancelCallback(self.msgCallBackDict[iconName])
                self.msgCallBackDict[iconName] = None
            self.mediator.Invoke('popMessage', (GfxValue(gbk2unicode(iconName)), GfxValue(gbk2unicode(msg))))
            if duration:
                self.msgCallBackDict[iconName] = BigWorld.callback(duration, Functor(self.removeMessage, iconName))
            return

    def cancelAllCallMsgBack(self):
        for iconName in self.msgCallBackDict:
            if self.msgCallBackDict[iconName]:
                BigWorld.cancelCallback(self.msgCallBackDict[iconName])

        self.msgCallBackDict = {}

    def removeMessage(self, iconName):
        if self.mediator:
            self.mediator.Invoke('removeMessage', GfxValue(gbk2unicode(iconName)))
