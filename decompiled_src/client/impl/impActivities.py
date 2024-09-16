#Embedded file name: C:/Users/user/Documents/WORK/roB/build/tmp/tw2/res/entities\client\impl/impActivities.o
import BigWorld
import Account
import gameglobal
import gametypes
import gamelog
import commActivity
import utils
import datetime
import npcConst
import const
from guis import events
from guis import uiConst
from statsTargets import StatsTarget
from callbackHelper import Functor
from crontab import CronTab
from commActivity import GroupLuckJoyVal, GroupLuckJoyMemberVal
from data import special_award_data as SAD
from data import stats_target_data as STD
from data import fishing_top_reward_data as FTRD
from data import activity_basic_data as ABD
from cdata import game_msg_def_data as GMDD
from cdata import activity_reverse_data as ARD
from data import activity_state_config_data as ASCD
from data import world_war_config_data as WWCD
from data import monster_clan_war_config_data as MCWCD
from cdata import update_bonus_data as UBD
from data import login_time_reward_data as LTRD

class ImpActivities(object):

    def getActivityStats(self):
        self.base.dispatchActivityStats()

    def dispatchClientStats(self, statsInfo, statsTargets):
        gamelog.debug('nqb: schedule#dispatchClientStats:', statsInfo, statsTargets)
        self.statsInfo = statsInfo
        self.statsTargets = statsTargets
        dataList = tuple(gameglobal.rds.ui.pushMessage.getDataList(uiConst.MESSAGE_TYPE_GET_REWARD))
        for item in dataList:
            if item['data'][0] == uiConst.ACT_STAT and not (self.statsTargets.has_key(item['data'][1]) and self.statsTargets[item['data'][1]].done):
                if gameglobal.rds.ui.activityPush.erefType == item['data'][0] and gameglobal.rds.ui.activityPush.detailId == item['data'][1]:
                    gameglobal.rds.ui.activityPush.hide()
                gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_GET_REWARD, item)

        for statsTargetId in self.statsTargets:
            std = STD.data.get(statsTargetId, None)
            if std is None:
                continue
            if self._canPushStatsAward(statsTargetId):
                gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GET_REWARD, {'data': (uiConst.ACT_STAT, statsTargetId)})

        gameglobal.rds.ui.achvmentOverview.updateActivityStats(statsInfo)

    def _canPushStatsAward(self, statsTargetId):
        hasActivity = ARD.data[uiConst.ACT_STAT].get(statsTargetId, None)
        if hasActivity is None:
            return False
        elif not self.statsTargets[statsTargetId].done:
            return False
        elif self.statsTargets[statsTargetId].rewardApplied:
            return False
        elif gameglobal.rds.ui.activityPush.isInMsg((uiConst.ACT_STAT, statsTargetId)):
            return False
        elif STD.data.get(statsTargetId, {}).get('bonusId', 0) == 0:
            return False
        else:
            return True

    def resetWeekly(self):
        self.resetWeeklySig = True

    def onResetWeekly(self):
        if self.resetWeeklySig:
            level = gameglobal.rds.ui.accountBind.getLevel(False)
            if level == 0:
                gameglobal.rds.ui.accountBind.addWeeklyPushMsg()
            self.resetWeeklySig = False

    def showScheduleWindow(self, statsInfo, statsTargets):
        gamelog.debug('zt: showScheduleWindow', statsInfo, statsTargets)
        self.statsInfo = statsInfo
        self.statsTargets = statsTargets
        gameglobal.rds.ui.achvmentOverview.updateActivityStats(statsInfo)

    def onStatsChanged(self, key, val, oldVal):
        if hasattr(self, 'statsInfo'):
            self.statsInfo[key] = val
        self.updateTianYuMallVipPrivilegeInfo()

    def onManyStatsChanged(self, statsInfo):
        if hasattr(self, 'statsInfo'):
            self.statsInfo = statsInfo

    def refreshStatsOfFbInfo(self, statsInfo):
        if hasattr(self, 'statsInfo'):
            needToRemove = []
            for key, value in self.statsInfo.iteritems():
                if -1 != key.find('_fbEnterTimes') and not statsInfo.has_key(key):
                    needToRemove.append(key)
                elif -1 != key.find('_fbConquerTimes') and not statsInfo.has_key(key):
                    needToRemove.append(key)

            for key in needToRemove:
                self.statsInfo.pop(key, None)

            self.statsInfo.update(statsInfo)

    def getLoginHourOfToday(self):
        if self.enterTimeOfDay:
            return (self.getServerTime() - self.enterTimeOfDay + self.loginTimeOfDay) / 3600
        else:
            return 0

    def getLoginSecondOfToday(self):
        if self.enterTimeOfDay:
            return self.getServerTime() - self.enterTimeOfDay + self.loginTimeOfDay
        else:
            return 0

    def getDeltaTime(self):
        return self.seqLoginDays

    def notifyLoginTimeReward(self, loginTimeOfReward, loginActivityId):
        gamelog.debug('@hjx notifyLoginTimeReward:', loginTimeOfReward, loginActivityId)
        gameglobal.rds.ui.activityPush.showLoginPush(loginTimeOfReward)

    def syncLoginTimeLeft(self, loginActivityId, loginTimeOfReward, canApplyReward):
        gamelog.debug('@zq: syncLoginTimeLeft', loginActivityId, loginTimeOfReward, canApplyReward)
        startTime = LTRD.data.get(loginActivityId, {}).get('startTime', [None])[0]
        endTime = LTRD.data.get(loginActivityId, {}).get('endTime', [None])[0]
        if startTime and endTime and utils.inTimeTupleRange(startTime, endTime, weekSet=0):
            curFudanLevel = self.calcFudanLevel(loginActivityId, loginTimeOfReward, canApplyReward)
            if curFudanLevel >= len(LTRD.data.get(loginActivityId, {}).get('bonus', [])):
                self.freshInvalidFudanUI(loginActivityId)
                return
            waitTime = LTRD.data.get(loginActivityId, {}).get('bonus', [])[curFudanLevel][0] - loginTimeOfReward
            bHas = True
            if self.fudanDict.get(loginActivityId, -1) == -1:
                delay = int(utils.nextByTimeTuple(endTime, self.getServerTime(), weekSet=0))
                BigWorld.callback(delay, Functor(self.freshInvalidFudanUI, loginActivityId))
                bHas = False
            self.fudanDict[loginActivityId] = [loginTimeOfReward, canApplyReward, utils.getNow() + waitTime * 60]
            if gameglobal.rds.ui.welfare.mediator:
                gameglobal.rds.ui.welfare.refreshInfo()
            if gameglobal.rds.ui.welfareFudanReward.panelMc:
                gameglobal.rds.ui.welfareFudanReward.refreshInfo()
            gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()
        else:
            gamelog.debug('@zq syncLoginTimeLeft TimeOut ')
            self.freshInvalidFudanUI(loginActivityId)

    def freshInvalidFudanUI(self, _id = -1):
        if self != BigWorld.player():
            return
        if self.fudanDict.get(_id, False):
            del self.fudanDict[_id]
            if gameglobal.rds.ui.welfare.mediator:
                _tabIdx = gameglobal.rds.ui.welfare.tabIdx
                gameglobal.rds.ui.welfare.hide()
                gameglobal.rds.ui.welfare.show(_tabIdx)
        gameglobal.rds.ui.rewardGiftActivityIcons.updateInfo()

    def calcFudanLevel(self, actId, time, canApplyReward):
        if time == -1:
            return -1
        _dataArr = LTRD.data.get(actId, {}).get('bonus', [])
        for i in xrange(len(_dataArr)):
            if time == _dataArr[i][0]:
                if canApplyReward:
                    return i
                else:
                    return i + 1
            if i == 0:
                if time < _dataArr[i][0]:
                    return i
            if i == len(_dataArr) - 1:
                return i
            if time > _dataArr[i][0] and time < _dataArr[i + 1][0]:
                return i + 1

        return -1

    def fudanIsNeedDisplay(self, actId, time, canApplyReward, level):
        _dataArr = LTRD.data.get(actId, {}).get('bonus', [])
        if level == len(_dataArr) or self._isSoul():
            return False
        else:
            return True

    def loginTimeRewardApplySucc(self, loginActivityId):
        gameglobal.rds.ui.pushMessage.removePushMsg(uiConst.MESSAGE_TYPE_LOGIN_AWARD_PUSH)

    def loginTimeRewardReset(self, loginActivityId, loginTimeOfReward, canApplyReward):
        gamelog.debug('jorsef: loginTimeRewardReset', loginActivityId, loginTimeOfReward, canApplyReward)
        self.syncLoginTimeLeft(loginActivityId, loginTimeOfReward, canApplyReward)

    def loginTimeRewardSetInvalid(self, loginActivityId):
        gamelog.debug('jorsef: loginTimeRewardSetInvalid', loginActivityId)
        self.freshInvalidFudanUI(loginActivityId)

    def isSpAwdFinish(self, specialAwardId):
        if not SAD.data.has_key(specialAwardId):
            return False
        sad = SAD.data[specialAwardId]
        awardType = sad['type']
        value = sad.get('value', -1)
        if sad.has_key('needLv') and (self.lv < sad['needLv'][0] or self.lv > sad['needLv'][1]):
            return False
        if awardType == gametypes.SPECIAL_AWARD_DAILYTIME:
            if self.getLoginSecondOfToday() < value * 60:
                gamelog.debug('hjx debug spAwd isSpAwdFinish getLoginTimeOfDay fail', self.getLoginSecondOfToday(), value * 3600)
                return False
        elif awardType == gametypes.SPECIAL_AWARD_SEQLOGIN:
            if self.seqLoginDays < value:
                gamelog.debug('hjx debug spAwd seqLoginDays is not enough', self.seqLoginDays, value)
                return False
        elif awardType == gametypes.SPECIAL_AWARD_ACTIVE:
            if self.activePoints < value:
                gamelog.debug('hjx debug spAwd activePoints is not enough', self.activePoints, value)
                return False
        elif awardType == gametypes.SPECIAL_AWARD_ACHIEVE:
            if not self._hasSpecialAwardAchieve(specialAwardId):
                return False
        else:
            return False
        return True

    def isSpAwdRewarded(self, specialAwardId):
        if not SAD.data.has_key(specialAwardId):
            return False
        sad = SAD.data[specialAwardId]
        awardType = sad['type']
        gamelog.debug('hjx debug schedule#isSpAwdFinish:', self.specialRewardInfo)
        if self.specialRewardInfo.has_key(awardType) and specialAwardId in self.specialRewardInfo[awardType]:
            return True
        else:
            return False

    def hasSpecialReward(self):
        for key in SAD.data.keys():
            if self.isSpAwdFinish(key) and not self.isSpAwdRewarded(key):
                return True

        return False

    def isStatsFinish(self, actId, statsId):
        if not self.inWorld:
            return False
        if not hasattr(self, 'statsInfo'):
            return False
        item = STD.data.get(statsId, {})
        prop = item.get('property', '')
        if not self.statsInfo.has_key(prop):
            return False
        if not self.statsTargets.has_key(statsId):
            return False
        if not self.statsTargets[statsId].done:
            return False
        return True

    def isStatsAwarded(self, statsId):
        if not self.statsTargets.has_key(statsId):
            return False
        if not self.statsTargets[statsId].rewardApplied:
            return False
        return True

    def onGetSpecialAward(self, awardType, specialAwardId):
        gamelog.debug('hjx debug onGetSpecialAward', awardType)
        if gameglobal.rds.ui.activityPush.erefType == uiConst.ACT_SPECIAL_AWD and gameglobal.rds.ui.activityPush.detailId == specialAwardId:
            gameglobal.rds.ui.activityPush.hide()
        gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_GET_REWARD, {'data': (uiConst.ACT_SPECIAL_AWD, specialAwardId)})

    def onGetStatsReward(self, statsTargetId):
        if not self.statsTargets.has_key(statsTargetId):
            self.statsTargets[statsTargetId] = StatsTarget(statsTargetId)
        self.statsTargets[statsTargetId].rewardApplied = True
        if gameglobal.rds.ui.activityPush.erefType == uiConst.ACT_STAT and gameglobal.rds.ui.activityPush.detailId == statsTargetId:
            gameglobal.rds.ui.activityPush.hide()
        gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_GET_REWARD, {'data': (uiConst.ACT_STAT, statsTargetId)})

    def checkOnlineTime(self):
        gamelog.debug('@hjx act#checkOnlineTime')
        onlineMin = []
        p = BigWorld.player()
        if isinstance(p, Account.PlayerAccount):
            return
        if hasattr(self, 'onlineAwdId') and hasattr(gameglobal.rds, 'tutorial'):
            actId = commActivity.getActivityIdByRef(self.onlineAwdId, gametypes.ACTIVITY_REF_BONUS)
            if actId:
                gamelog.debug('@hjx act#onlineAwdId:', actId)
                gameglobal.rds.tutorial.onFinishActivity(actId)
        for key, value in SAD.data.items():
            if value.get('type', -1) == gametypes.SPECIAL_AWARD_DAILYTIME:
                onlineMin.append((key, value.get('value', 0)))

        onlineMin = sorted(onlineMin, key=lambda item: item[1])
        gamelog.debug('@hjx act#_checkTime:', onlineMin, p.getLoginSecondOfToday())
        for id, min in onlineMin:
            offset = int(min * 60 - p.getLoginSecondOfToday()) + 2
            gamelog.debug('@hjx act#offset:', id, offset)
            if offset > 0:
                self.onlineAwdId = id
                if hasattr(self, 'scheduleCallback') and self.scheduleCallback != 0:
                    BigWorld.cancelCallback(self.scheduleCallback)
                    self.scheduleCallback = 0
                self.scheduleCallback = BigWorld.callback(offset, self.checkOnlineTime)
                break

    def cancelActCallback(self):
        if hasattr(self, 'scheduleCallback') and self.scheduleCallback != 0:
            BigWorld.cancelCallback(self.scheduleCallback)
            self.scheduleCallback = 0

    def onFinishActivity(self, actId):
        gamelog.debug('hjx debug tutor onFinishActivity:', actId)
        gameglobal.rds.tutorial.onFinishActivity(actId)

    def getFishAwardDetial(self, awardType, awardTime, rank, rewardData):
        ret = {}
        ret['awardType'] = awardType
        ret['awardTime'] = awardTime
        ret['name'] = rewardData['title'] + '(%d.%d.%d)' % (utils.getYearInt(awardTime), utils.getMonthInt(awardTime), utils.getMonthDayInt(awardTime))
        ret['prizeChat'] = rewardData['prizeChat']
        if awardType == gametypes.GLOBAL_AWARD_TYPE_SINGLE_FISHING_RANK:
            ret['questDesc'] = rewardData['desc1'] % rank
            rewardType = 'ranks'
            rewardDataType = 'rankBonus'
        else:
            ret['questDesc'] = rewardData['desc2'] % rank
            rewardType = 'scores'
            rewardDataType = 'scoreBonus'
        idx = utils.getRangeIndex(rank, rewardData[rewardType])
        if idx >= 0:
            rankBonus = rewardData[rewardDataType][idx]
            if rankBonus:
                ret['bonus'] = rankBonus
        return ret

    def getFishAward(self):
        ret = []
        if self.globalAwardCache:
            for key, value in self.globalAwardCache.iteritems():
                awardType, awardTime = key
                if awardType == gametypes.GLOBAL_AWARD_TYPE_SINGLE_FISHING_RANK:
                    questId, rank = value.awardVal
                    if not FTRD.data.has_key(questId):
                        continue
                    rewardData = FTRD.data[questId]
                    ret.append(self.getFishAwardDetial(awardType, awardTime, rank, rewardData))
                elif awardType == gametypes.GLOBAL_AWARD_TYPE_SINGLE_FISHING_SCORE:
                    questId, score = value.awardVal
                    if not FTRD.data.has_key(questId):
                        continue
                    rewardData = FTRD.data[questId]
                    ret.append(self.getFishAwardDetial(awardType, awardTime, score, rewardData))

        return ret

    def hasFishAward(self):
        if self.globalAwardCache:
            for key in self.globalAwardCache:
                if key[0] in (gametypes.GLOBAL_AWARD_TYPE_SINGLE_FISHING_RANK, gametypes.GLOBAL_AWARD_TYPE_SINGLE_FISHING_SCORE):
                    return True

        return False

    def notifyActivity(self, activityId, duration, index):
        activityData = ABD.data.get(activityId)
        if not activityData:
            return
        if not self.inWorld:
            return
        if activityData.get('minLv', 0) > self.lv or activityData.get('maxLv', self.lv) < self.lv:
            return
        if activityId in self.finishedActivity:
            return
        if self.checkActivityOverTime(activityData, index):
            return
        if activityId in WWCD.data.get('scheduleBlackList', ()) and gameglobal.rds.configData.get('enableWorldWar') and self.worldWar.state != gametypes.WORLD_WAR_STATE_CLOSE:
            return
        BigWorld.callback(duration, Functor(self.closeActivityPushMsg, activityId))

    def closeActivityPushMsg(self, activityId):
        pushType = ABD.data.get(activityId, {}).get('pushId', None)
        if not pushType:
            return
        else:
            gameglobal.rds.ui.pushMessage.removeData(pushType, {'data': activityId})
            return

    def checkActivityOverTime(self, aData, index):
        overTime = aData.get('overTime', ())
        if len(overTime) == 0:
            return False
        elif index >= len(overTime) or index < 0:
            return False
        overTime = overTime[index].split('.')
        if len(overTime) != 3:
            gamelog.error('checkActivityOverTime format is error:%s' % overTime)
            return
        year, month, day = [ int(item) for item in overTime ]
        beCheckDate = datetime.date(year, month, day)
        currDate = datetime.date.fromtimestamp(self.getServerTime())
        if currDate >= beCheckDate:
            return True
        else:
            return False

    def setupActivityNotify(self, actIds = (), includeWorldWarActs = False):
        actIds = actIds or ABD.data.keys()
        for activityId in actIds:
            activityData = ABD.data[activityId]
            if activityData.get('includeServer', ()) and gameglobal.rds.g_serverid not in activityData['includeServer']:
                continue
            if activityData.get('excludeServer', ()) and gameglobal.rds.g_serverid in activityData['excludeServer']:
                continue
            if activityData.get('isHideInNoviceServer', 0) and gameglobal.rds.loginManager.serverMode() == gametypes.SERVER_MODE_NOVICE:
                continue
            if activityId in WWCD.data.get('scheduleBlackList', ()) and not includeWorldWarActs:
                continue
            if utils.getEnableCheckServerConfig():
                serverConfigId = activityData.get('serverConfigId', 0)
                if serverConfigId and not utils.checkInCorrectServer(serverConfigId):
                    continue
            weekSet = activityData.get('weekSet', 0)
            if activityData.has_key('startTimes') and activityData.has_key('endTimes') and activityData.has_key('pushId'):
                startCrons = activityData['startTimes']
                endCrons = activityData['endTimes']
                if activityData.has_key('startNotifyTimes'):
                    startCrons = activityData['startNotifyTimes']
                if activityData.has_key('endNotifyTimes'):
                    endCrons = activityData['endNotifyTimes']
                for i in xrange(len(startCrons)):
                    if startCrons[i].startswith('* *'):
                        continue
                    if self.checkActivityOverTime(activityData, i):
                        continue
                    if utils.inCrontabRange(startCrons[i], endCrons[i], weekSet=weekSet):
                        endCT = CronTab(endCrons[i])
                        duration = utils.calcCrontabNextEx(endCT, self.getServerTime(), weekSet=weekSet)
                        if activityId not in gameglobal.rds.notifiedActs:
                            self.notifyActivity(activityId, duration, i)
                            gamelog.debug('zt: showActivity Notify', activityId, duration)
                    else:
                        startCT = CronTab(startCrons[i])
                        endCT = CronTab(endCrons[i])
                        delay = utils.calcCrontabNextEx(startCT, self.getServerTime(), weekSet=weekSet)
                        duration = utils.calcCrontabNextEx(endCT, self.getServerTime(), weekSet=weekSet) - delay
                        BigWorld.callback(delay, Functor(self.notifyActivity, activityId, duration, i))
                        gamelog.debug('zt: showActivity Notify2', activityId, duration, delay)

    def cancelFestivalReward(self, actId, itemBonus):
        gameglobal.rds.ui.pushMessage.removeData(uiConst.MESSAGE_TYPE_GET_FESTIVAL_REWARD, {'data': (actId, itemBonus)})

    def pushFestivalReward(self, actId, itemBonus):
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_GET_FESTIVAL_REWARD, {'data': (actId, itemBonus)})

    def fishingActivityDataSend(self, fishingActivityData):
        self.fishingActivityData = fishingActivityData
        gameglobal.rds.ui.playRecommLvUp.refreshInfo()
        BigWorld.player().showGameMsg(GMDD.data.JOIN_FISH_ACTIVITY_SUCCESS, ())
        gameglobal.rds.ui.fishingGame.checkNeedLoadByNotice()
        if not self.fishingActivityData:
            gameglobal.rds.ui.fishingGame.clearAndHide()

    def onQueryImportantPlayRecommendInfo(self, remoteInfo):
        self.importantPlayRecommendInfo = remoteInfo
        gameglobal.rds.ui.dispatchEvent(events.EVENT_IPRD_UPDATE)

    def onUpdateImportantPlayRecommendInfo(self, remoteInfo):
        self.importantPlayRecommendInfo.update(remoteInfo)
        gameglobal.rds.ui.dispatchEvent(events.EVENT_IPRD_UPDATE)

    def onAddActivityState(self, actId):
        p = BigWorld.player()
        data = ASCD.data.get(actId, {})
        minLv, maxLv = data.get('lvLimit', (None, None))
        if minLv and maxLv and not minLv <= p.lv <= maxLv:
            return None
        else:
            stateId = data.get('stateId', 0)
            if stateId:
                self.activityStateIds.append(stateId)
            if gameglobal.rds.configData.get('enableActivityStateBonus', False):
                if stateId:
                    p.addFakeState(stateId)
            self.setActivityId(actId)
            return None

    def onRemoveActivityState(self, actId):
        p = BigWorld.player()
        data = ASCD.data.get(actId, {})
        minLv, maxLv = data.get('lvLimit', (None, None))
        if minLv and maxLv and not minLv <= p.lv <= maxLv:
            return None
        else:
            stateId = data.get('stateId', 0)
            if stateId and stateId in self.activityStateIds:
                self.activityStateIds.remove(stateId)
            if gameglobal.rds.configData.get('enableActivityStateBonus', False):
                if stateId:
                    p.quitFakeState(stateId)
            self.setActivityId(actId, True)
            return None

    def setActivityId(self, actId, reset = False):
        data = ASCD.data.get(actId, {})
        pointsToFame = data.get('pointsToFame')
        if pointsToFame:
            if not reset:
                self.qumoActivityId = actId
            else:
                self.qumoActivityId = 0
            gameglobal.rds.ui.roleInfo.refreshQumoPanel()
            gameglobal.rds.ui.roleInformationQumo.initWeekReward()
            self.updateRewardHallInfo(uiConst.REWARD_QUMO)
        rewardZXInfo = data.get('rewardZXInfo')
        if rewardZXInfo:
            if not reset:
                self.zxActivityId = actId
            else:
                self.zxActivityId = 0
            gameglobal.rds.ui.roleInfo.refreshJunjiePanel()
            self.updateRewardHallInfo(uiConst.REWARD_JUNJIE)

    def onAddAllActivityState(self, actIds):
        p = BigWorld.player()
        for actId in actIds:
            data = ASCD.data.get(actId, {})
            minLv, maxLv = data.get('lvLimit', (None, None))
            if minLv and maxLv and not minLv <= p.lv <= maxLv:
                continue
            stateId = data.get('stateId', 0)
            if stateId:
                self.activityStateIds.append(stateId)
            self.setActivityId(actId)

        p.setActivityState()

    def showNewYearUI(self, actId):
        data = ABD.data.get(actId, {})
        pathUI = 'widgets/%s.swf' % data.get('showCountDwonUI', 'NewYearCountDownWidget')
        stopFrame = data.get('uiStopFrame', 470)
        gameglobal.rds.ui.showScreenUI(pathUI, stopFrame)

    def pushReceiveFallMsg(self, actId, subId):
        activityData = ABD.data.get(actId, {})
        if not activityData:
            return
        remainTime = min((CronTab(x).next(utils.getNow()) for x in activityData['endTimes']))
        if gameglobal.rds.configData.get('enableNewYearAni', True):
            BigWorld.callback(remainTime - 10, Functor(self.showNewYearUI, actId))
        data = {'startTime': utils.getNow(),
         'totalTime': remainTime,
         'data': []}
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_TIANJIANG, data)
        self.showGameMsg(GMDD.data.RECEIVE_FALL_MSG, ())

    def pushFallBonusItem(self, bonusId):
        pass

    def removeFallBonusBox(self, subId):
        pass

    def onEndPinjiu(self, state, npcId):
        gameglobal.rds.ui.pinJiu.show(state, npcId)

    def monsterClanWarActivityStart(self, activityTime):
        if self.lv < MCWCD.data.get('minLv', 40):
            return
        if self._isSoul():
            return
        self.monsterClanWarStarted = True
        gameglobal.rds.ui.zhanJu.updateStartTime(activityTime)
        gameglobal.rds.ui.monsterClanWarActivity.updateStartTime(activityTime)
        gameglobal.rds.ui.monsterClanWarActivity.startMonsterClanActivity()

    def setPurchaseKaolaHistory(self, info):
        self.purchaseKaolaHistory = info

    def monsterClanWarActivityEnd(self):
        if self.lv < MCWCD.data.get('minLv', 40):
            return
        if not getattr(self, 'monsterClanWarStarted', False):
            return
        if self._isSoul():
            return
        self.monsterClanWarStarted = False
        gameglobal.rds.ui.monsterClanWarActivity.endMonsterClanActivity()
        gameglobal.rds.ui.zhanJu.updateEndTime()

    def monsterClanWarActivityPrepare(self, prepareTime):
        if self.lv < MCWCD.data.get('minLv', 40):
            return
        if self._isSoul():
            return
        gameglobal.rds.ui.monsterClanWarActivity.cacheData = {}
        gameglobal.rds.ui.monsterClanWarActivity.updatePrepareTime(prepareTime)
        gameglobal.rds.ui.zhanJu.updatePrepareTime(prepareTime)

    def notifyActivityRewardInfo(self, rewardTypeList):
        gamelog.debug('@hjx notifyActivityRewardInfo:', rewardTypeList)
        if rewardTypeList:
            gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_PUSH_BONUS, {'rewardList': rewardTypeList})

    def getUpdateBonus(self):
        ret = []
        if not gameglobal.rds.configData.get('enableUpdateBonus', False):
            return ret
        now = utils.getNow()
        for key, value in UBD.data.iteritems():
            if value.has_key('tStartApply'):
                tStartApply = int(value['tStartApply'])
                tEndApply = int(value['tEndApply'])
            elif value.has_key('startCron') and utils.inCrontabRange(value['startCron'], value['endCron']):
                tStartApply = int(utils.getPreCrontabTime(value['startCron']))
                tEndApply = int(utils.getNextCrontabTime(value['endCron']) + 1)
            else:
                continue
            if now < tStartApply:
                continue
            if now > tEndApply:
                continue
            if self.updateBonusFlag.has_key(tStartApply):
                continue
            ret.append(key)

        return ret

    def sendGlobalMonsters(self, data):
        for charType, entId in data:
            self.globalMonsters[charType] = entId

        if self.globalMonsters:
            gameglobal.rds.ui.questTrack.refreshNews(True)

    def sendGlobalMonster(self, charType, entId):
        self.globalMonsters[charType] = entId
        if self.globalMonsters:
            gameglobal.rds.ui.questTrack.refreshNews(True)

    def removeGlobalMonster(self, charType):
        self.globalMonsters.pop(charType, None)
        if self.globalMonsters is None:
            gameglobal.rds.ui.questTrack.refreshNews(False)

    def onGroupLuckJoyStart(self, nuid, aid):
        """
        \xe7\xbb\x84\xe9\x98\x9f\xe7\xbf\xbb\xe7\x89\x8c\xe5\xbc\x80\xe5\xa7\x8b
        Args:
            nuid: \xe7\xbf\xbb\xe7\x89\x8cNUID
            aid: \xe7\xbf\xbb\xe7\x89\x8cID
        """
        self.groupLuckJoy = GroupLuckJoyVal(nuid=nuid, aid=aid)
        self.groupLuckJoy.genInitSlots()
        gameglobal.rds.ui.findBeastLuckJoy.show()

    def onGroupLuckJoyAddMember(self, aid, gbId, name, readOnly):
        """
        \xe6\xb7\xbb\xe5\x8a\xa0\xe7\xbf\xbb\xe7\x89\x8c\xe6\x88\x90\xe5\x91\x98
        Args:
            aid: \xe7\xbf\xbb\xe7\x89\x8cID
            gbId: gbId
            name: \xe8\xa7\x92\xe8\x89\xb2\xe5\x90\x8d
            readOnly: \xe6\x98\xaf\xe5\x90\xa6\xe5\x8f\xaa\xe7\x9c\x8b\xe4\xb8\x8d\xe7\xbf\xbb\xe7\x89\x8c
        """
        self.groupLuckJoy.members[gbId] = GroupLuckJoyMemberVal(name=name, readOnly=readOnly)

    def onGroupLuckJoySlotResult(self, aid, idx, name, detail):
        """
        \xe7\xbb\x84\xe9\x98\x9f\xe7\xbf\xbb\xe7\x89\x8c\xe5\x8d\x95\xe4\xb8\xaaslot\xe7\xbb\x93\xe6\x9e\x9c
        Args:
            aid: \xe7\xbf\xbb\xe7\x89\x8cID
            idx: \xe4\xbd\x8d\xe7\xbd\xae
            name: \xe8\xa7\x92\xe8\x89\xb2\xe5\x90\x8d
            detail: type, gbId, itemId, cnt
        """
        slot = self.groupLuckJoy.slots[idx]
        slot.fromDTO(detail)
        if slot.gbId:
            self.groupLuckJoy.getMember(slot.gbId).name = name
        gameglobal.rds.ui.findBeastLuckJoy.refreshLeafSlot(slot, idx, name)

    def onGroupLuckJoyResult(self, aid, dtos):
        """
        \xe7\xbb\x84\xe9\x98\x9f\xe7\xbf\xbb\xe7\x89\x8c\xe5\x89\xa9\xe4\xbd\x99\xe7\x9a\x84\xe6\x9c\x80\xe5\x90\x8e\xe7\xbb\x93\xe6\x9e\x9c
        Args:
            aid: \xe7\xbf\xbb\xe7\x89\x8cID
            dtos: array of (idx, name, detail) \xe5\x8f\x82\xe8\xa7\x81onGroupLuckJoySlotResult
        
        """
        restSlotInfos = []
        for idx, name, detail in dtos:
            slot = self.groupLuckJoy.slots[idx]
            slot.fromDTO(detail)
            if slot.gbId:
                self.groupLuckJoy.getMember(slot.gbId).name = name
            slotInfo = {'slot': slot,
             'idx': idx,
             'name': name}
            restSlotInfos.append(slotInfo)

        gameglobal.rds.ui.findBeastLuckJoy.openEnd(restSlotInfos)

    def onGroupLuckJoyEnd(self, aid):
        """
        \xe7\xbb\x84\xe9\x98\x9f\xe7\xbf\xbb\xe7\x89\x8c\xe7\xbb\x93\xe6\x9d\x9f
        Args:
            aid: \xe7\xbf\xbb\xe7\x89\x8cID
        """
        pass

    def onListFlowbackBonusClient(self, bonusInfo):
        self.gmFlowbackBonus = bonusInfo
        if gameglobal.rds.ui.funcNpc.lastFuncType == npcConst.NPC_FUNC_GM_AWARD:
            gameglobal.rds.ui.openQuestWindow(uiConst.NPC_AWARD)

    def setHofFinishedActivities(self, hofFinishActivities):
        """
        \xe5\x90\x8c\xe6\xad\xa5\xe5\x90\x8d\xe4\xba\xba\xe5\xa0\x82\xe6\xb4\xbb\xe5\x8a\xa8\xe5\xae\x8c\xe6\x88\x90\xe6\x83\x85\xe5\x86\xb5\xef\xbc\x88\xe4\xb8\x8a\xe7\xba\xbf\xe6\x97\xb6\xe3\x80\x81\xe6\x9c\x89\xe5\x8f\x98\xe5\x8a\xa8\xe6\x97\xb6\xef\xbc\x89
        :param hofFinishActivities:\xe6\x95\xb4\xe4\xb8\xaalist\xef\xbc\x8c\xe5\x8c\x85\xe5\x90\xab\xe8\x8b\xa5\xe5\xb9\xb2\xe4\xb8\xaa\xe5\x85\x83\xe7\xb4\xa0 
        """
        gamelog.debug('@xzh setHofFinishedActivities', hofFinishActivities)
        gameglobal.rds.ui.playRecommActivation.setPlayRecHofFinishedActivities(hofFinishActivities)

    def onUpdateDailyWelfareBuyInfo(self, info):
        """
        \xe6\x95\xb0\xe6\x8d\xae\xe7\xbb\x93\xe6\x9e\x84\xe5\xa6\x82\xe4\xb8\x8b
        //\xe5\x8d\x95\xe8\xb4\xad\xe4\xb9\xb0\xe6\x95\xb0\xe6\x8d\xae 1: {welfareId: buyTime, }
        \xe5\x8d\x95\xe8\xb4\xad\xe4\xb9\xb0\xe6\x95\xb0\xe6\x8d\xae 1: {welfareId: buyTime, lastBuyItemIds: itemId}
        \xe4\xb8\x80\xe9\x94\xae\xe8\xb4\xad\xe4\xb9\xb0\xe6\x95\xb0\xe6\x8d\xae 2 \xef\xbc\x9a buyTime
        \xe4\xb8\x83\xe6\x97\xa5\xe8\xb4\xad\xe4\xb9\xb0\xe6\x95\xb0\xe6\x8d\xae 3 : {'beginTime': xxx, 'duration': 7, 'got': 0}
        \xe4\xb8\x8a\xe6\xac\xa1\xe8\xb4\xad\xe4\xb9\xb0\xe6\x95\xb0\xe6\x8d\xae\xe8\xae\xb0\xe5\xbd\x95 4 : {welfareId: itemId,}
        :param info:
        :return:
        """
        self.dailyGiftInfo = info
        gameglobal.rds.ui.activitySaleDailyGift.refreshInfo()

    def getActivitiesWeeklyAwardInfo(self):
        self.base.syncActivitiesWeeklyAwardInfoToClient()

    def updateActivitiesWeeklyAwardInfo(self, info, version):
        gameglobal.rds.ui.achvmentOverview.updateActivitiesWeeklyAwardInfo(info, version)

    def remindActivitiesWeeklyAward(self, rewardInfo):
        gamelog.debug('@hqx_client_remindActivitiesWeeklyAward', rewardInfo)
        gameglobal.rds.ui.pushMessage.addPushMsg(uiConst.MESSAGE_TYPE_ACHVEMENT_WEEK_AWARD)
        if gameglobal.rds.ui.achvment.widget:
            self.getActivitiesWeeklyAwardInfo()

    def recvNSActPropertyRank(self, topType, stage, topLen, rankData):
        newRankData = []
        for k, v in rankData.items():
            value = list(v)
            value.append(k)
            newRankData.append(value)

        if gameglobal.rds.ui.newServerTopRankCombatScoreAndLv.widget:
            gameglobal.rds.ui.newServerTopRankCombatScoreAndLv.setDataAndRefresh(topType, topLen, newRankData)
        redPoint = self.checkReward(rankData)
        rewardGiftActivityIcons = gameglobal.rds.ui.rewardGiftActivityIcons
        rewardGiftActivityIcons.setNewServerRedPoint(str(topType) + '/' + str(stage), redPoint)
        rewardGiftActivityIcons.updateInfo()
        if rewardGiftActivityIcons.getNewServerRedPoint():
            rewardGiftActivityIcons.uiAdapter.pushMessage.addPushMsg(uiConst.MESSAGE_NEW_SERVER_REWARD_PUSH)
        else:
            rewardGiftActivityIcons.uiAdapter.pushMessage.removePushMsg(uiConst.MESSAGE_NEW_SERVER_REWARD_PUSH)
        gameglobal.rds.ui.newServiceActivities.refreshAllRedPoint()

    def checkReward(self, rankData):
        result = False
        myAvatarInfo = None
        for gbId, avatarInfo in rankData.items():
            if gbId == self.gbId and avatarInfo[0] != 0:
                myAvatarInfo = avatarInfo

        if myAvatarInfo and myAvatarInfo[2] == False:
            result = True
        return result

    def recvNSGuildPrestigeRank(self, rankData):
        if gameglobal.rds.ui.newServerTopRankGuild.widget:
            gameglobal.rds.ui.newServerTopRankGuild.setDataAndRefresh(rankData.values())

    def recvNSHonorRankData(self, rankData):
        if gameglobal.rds.ui.newServerTopRankHonor.widget:
            gameglobal.rds.ui.newServerTopRankHonor.setDataAndRefresh(rankData)

    def onNSPropertyRankAchieveTarget(self, topType, stage, rank):
        rewardGiftActivityIcons = gameglobal.rds.ui.rewardGiftActivityIcons
        rewardGiftActivityIcons.setNewServerRedPoint(str(topType) + '/' + str(stage), True)
        rewardGiftActivityIcons.updateInfo()
        if rewardGiftActivityIcons.getNewServerRedPoint():
            rewardGiftActivityIcons.uiAdapter.pushMessage.addPushMsg(uiConst.MESSAGE_NEW_SERVER_REWARD_PUSH)
        else:
            rewardGiftActivityIcons.uiAdapter.pushMessage.removePushMsg(uiConst.MESSAGE_NEW_SERVER_REWARD_PUSH)

    def exchangeMysteryAnimalSuccess(self):
        if gameglobal.rds.ui.mysteryAnimal.widget:
            gameglobal.rds.ui.mysteryAnimal.refreshPanel()

    def getNewServerBothRankData(self):
        if not self.inWorld:
            return
        self.getNewServerRankData(gametypes.TOP_TYPE_COMBAT_SCORE)
        self.getNewServerRankData(gametypes.TOP_TYPE_LEVEL)

    def getNewServerRankData(self, topType):
        if topType == gametypes.TOP_TYPE_COMBAT_SCORE:
            stage = utils.getNewServerPropertyRankActStage(topType, self.combatScoreList[const.COMBAT_SCORE])
            if stage <= 0:
                stage = 0
            self.base.getNSCombatScorePropertyRank(stage)
        elif topType == gametypes.TOP_TYPE_LEVEL:
            stage = utils.getNewServerPropertyRankActStage(topType, (self.lv, self.skillEnhancePoint))
            if stage <= 0:
                stage = 0
            self.base.getNSLevelPropertyRank(stage)
