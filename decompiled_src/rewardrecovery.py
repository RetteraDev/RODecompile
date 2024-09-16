#Embedded file name: /WORKSPACE/data/entities/common/rewardrecovery.o
import BigWorld
import const
import gametypes
import utils
import copy
import gamelog
from userDictType import UserDictType
from userSoleType import UserSoleType
from data import sys_config_data as SCD
from data import reward_getback_data as RGD
from cdata import qumo_junjie_reward_getback_data as QJRGD
from cdata import qumo_junjie_reward_price_data as QJRPD
if BigWorld.component in ('base', 'cell'):
    import gameconfig
    import gameengine
    import gamebonus
    from data import formula_server_data as FMD
elif BigWorld.component in ('client',):
    import gameglobal
    if not getattr(BigWorld, 'isBot', False):
        from data import formula_client_data as FMD

class RewardRecoveryActivity(UserDictType):

    def _lateReload(self):
        super(RewardRecoveryActivity, self)._lateReload()
        for v in self.itervalues():
            v.reloadScript()

    def isActivityTypeValid(self, activityType):
        activityTypes = [ v.get('activityType') for k, v in RGD.data.iteritems() ]
        if activityType not in activityTypes:
            return False
        return True

    def onGetActivity(self, activityType):
        v = None
        if activityType in [gametypes.REWARD_RECOVER_ACTIVITY_TYPE_SCHOOL_DAILY,
         gametypes.REWARD_RECOVER_ACTIVITY_TYPE_HAI_ZEI_HUO_WU,
         gametypes.REWARD_RECOVER_ACTIVITY_TYPE_HAI_YAO_HUN_PO,
         gametypes.REWARD_RECOVER_ACTIVITY_TYPE_XI_CHEN,
         gametypes.REWARD_RECOVER_ACTIVITY_TYPE_GUILD_DAILY]:
            v = CommonDailyRewardRecovery(activityType=activityType)
        elif activityType == gametypes.REWARD_RECOVER_ACTIVITY_TYPE_AN_YING_XIN_MO:
            v = AnYingXinMoRewardRecovery(activityType=activityType)
        elif activityType in [gametypes.REWARD_RECOVER_ACTIVITY_TYPE_XIE_SHOU_TONG_YOU_SU_LAN, gametypes.REWARD_RECOVER_ACTIVITY_TYPE_PO_MO_LING, gametypes.REWARD_RECOVER_ACTIVITY_TYPE_QING_LIN_WAR]:
            v = CommonWeeklyActivityRewardRecovery(activityType=activityType)
        elif activityType in [gametypes.REWARD_RECOVER_ACTIVITY_TYPE_XUAN_SHANG_SHOU_LIE, gametypes.REWARD_RECOVER_ACTIVITY_TYPE_SHI_KONG_HUAN_JING]:
            v = RestCountWeeklyActivityRewardRecovery(activityType=activityType)
        elif activityType in [gametypes.REWARD_RECOVER_ACTIVITY_TYPE_QU_MO, gametypes.REWARD_RECOVER_ACTIVITY_TYPE_JUN_JIE]:
            v = ExpandTabWeeklyActivityRewardRecovery(activityType=activityType)
        elif activityType == gametypes.REWARD_RECOVER_ACTIVITY_TYPE_ZHENG_ZHAN_LING:
            v = ZhengZhanLingRewardRecovery(activityType=activityType)
        elif activityType in [gametypes.REWARD_RECOVER_ACTIVITY_TYPE_FISHING,
         gametypes.REWARD_RECOVER_ACTIVITY_TYPE_SHENG_SI_CHANG,
         gametypes.REWARD_RECOVER_ACTIVITY_TYPE_GOBLIN_TRAVEL,
         gametypes.REWARD_RECOVER_ACTIVITY_TYPE_SHEN_YU_ZHI_SHI,
         gametypes.REWARD_RECOVER_ACTIVITY_TYPE_SUI_XING_YU,
         gametypes.REWARD_RECOVER_ACTIVITY_TYPE_TIAN_YU_YAN_WU,
         gametypes.REWARD_RECOVER_ACTIVITY_TYPE_LUN_ZHAN_YUN_DIAN]:
            v = CommonTimingActivityRewardRecovery(activityType=activityType)
        elif activityType in [gametypes.REWARD_RECOVER_ACTIVITY_TYPE_SI_FANG_ZHI_LUAN]:
            v = CompareTotalTimingActivityRewardRecovery(activityType=activityType)
        elif activityType in [gametypes.REWARD_RECOVER_ACTIVITY_TYPE_SHEN_YU_XIN_MO_LU,
         gametypes.REWARD_RECOVER_ACTIVITY_TYPE_KE_JU,
         gametypes.REWARD_RECOVER_ACTIVITY_TYPE_LING_ZUN_TIAO_ZHAN,
         gametypes.REWARD_RECOVER_ACTIVITY_TYPE_YU_MU_FENG_WAR,
         gametypes.REWARD_RECOVER_ACTIVITY_TYPE_NEW_FLAG_SKY]:
            v = RotateTimingActivityRewardRecovery(activityType=activityType)
        return v

    def getActivity(self, activityType = 0):
        if not activityType or not self.isActivityTypeValid(activityType):
            return None
        v = self.get(activityType)
        if not v:
            v = self.onGetActivity(activityType)
            self[activityType] = v
        return v

    def onActivityCompleted(self, owner, activityId, args):
        rgdVal = RGD.data.get(activityId, {})
        if not rgdVal:
            return
        v = self.getActivity(rgdVal.get('activityType', 0))
        v.activityId = activityId
        if activityId == gametypes.REWARD_RECOVER_ACTIVITY_ID_FOR_TIAN_YU_YAN_WU:
            v.onActivityCompletedForSkyWing(owner, args)
            return
        v.onActivityCompleted(owner, args)

    def refresh(self, owner):
        for activityId, val in RGD.data.iteritems():
            if activityId == gametypes.REWARD_RECOVER_ACTIVITY_ID_FOR_XUN_LING:
                continue
            activityType = val.get('activityType', 0)
            school = val.get('school', 0)
            import itemToolTipUtils
            ownerSchool = itemToolTipUtils.getSchoolFromBase(owner.id)
            if school and ownerSchool != school:
                continue
            if val.get('parentId', 0):
                continue
            v = self.getActivity(activityType)
            v.activityId = activityId

        for activityType, val in self.iteritems():
            if activityType in [gametypes.REWARD_RECOVER_ACTIVITY_TYPE_GUILD_DAILY, gametypes.REWARD_RECOVER_ACTIVITY_TYPE_SUI_XING_YU] or activityType == gametypes.REWARD_RECOVER_ACTIVITY_TYPE_XUN_LING:
                continue
            val.refresh(owner)

    def guildDailyRefresh(self, owner, guildBox):
        activityTypes = [gametypes.REWARD_RECOVER_ACTIVITY_TYPE_GUILD_DAILY, gametypes.REWARD_RECOVER_ACTIVITY_TYPE_SUI_XING_YU]
        for activityType in activityTypes:
            activity = self.get(activityType)
            if not activity:
                activity = self.getActivity(activityType)
            if guildBox:
                activity.refresh(owner)
            else:
                activity.guildDailyRefresh(owner)

    def transfer(self, owner):
        if not gameconfig.enableRewardRecovery():
            return
        owner.transProxyData(const.PROXY_KEY_REWARD_RECOVERY, self.getDTO())

    def getDTO(self):
        return [ (activityType, x.getDTO()) for activityType, x in self.iteritems() ]

    def fromDTO(self, dto):
        if not dto:
            self.clear()
            return self
        for activityType, d in dto:
            v = self.onGetActivity(activityType)
            if not v:
                continue
            self[activityType] = v.fromDTO(d)

        return self

    def refreshExtraLv(self, owner, activityId, extraLv, tWhen):
        aType = RGD.data.get(activityId, {}).get('activityType', 0)
        if not aType:
            return
        if aType not in [gametypes.REWARD_RECOVER_ACTIVITY_TYPE_QU_MO, gametypes.REWARD_RECOVER_ACTIVITY_TYPE_JUN_JIE]:
            return
        v = self.getActivity(aType)
        v.refreshExtraLv(owner, extraLv, tWhen)


class ActivityDayVal(UserSoleType):

    def __init__(self, lv = 0, cnt = 0, extra = {}):
        self.lv = lv
        self.cnt = cnt
        self.extra = copy.deepcopy(extra)

    def update(self, lv, num, extra):
        self.lv = lv
        self.cnt += num
        self.extra = copy.deepcopy(extra)
        if extra.has_key('time'):
            return
        self.extra['time'] = utils.getNow()


class IRewardRecoveryCommon(UserSoleType):

    def __init__(self, activityType = 0):
        self.getBackRewardTime = 0
        self.activityId = 0
        self.daysVal = {}

    def _lateReload(self):
        super(IRewardRecoveryCommon, self)._lateReload()

    def getActivityId(self):
        return self.activityId

    def getActivityDayVal(self, dateKey):
        if self.daysVal.has_key(dateKey):
            return self.daysVal[dateKey]

    def onUpdateGetBackRewardTime(self, tWhen):
        self.getBackRewardTime = tWhen

    def refresh(self, owner):
        if not owner:
            return
        self.refreshDaily(owner)

    def refreshDaily(self, owner):
        tWhen = utils.getDaySecond()
        day = self.calcGetBackDays(RGD.data.get(self.activityId, {}))
        for index in xrange(day + 1):
            if not self.getActivityDayVal(tWhen):
                c = ActivityDayVal()
                self.daysVal[tWhen] = c
                val = self.daysVal[tWhen]
                val.lv = owner.lv
                val.extra['time'] = tWhen + 1
            tWhen -= const.SECONDS_PER_DAY

        keys = self.daysVal.keys()
        for key in keys:
            if key <= tWhen:
                self.daysVal.pop(key)

        self.transfer(owner)

    def getDTO(self):
        return (self.activityId, self.getBackRewardTime, [ (tWhen,
          x.lv,
          x.cnt,
          x.extra) for tWhen, x in self.daysVal.iteritems() ])

    def fromDTO(self, dto):
        self.activityId, self.getBackRewardTime, vals = dto
        self.daysVal.clear()
        for d in vals:
            tWhen, lv, cnt, extra = d
            val = ActivityDayVal(lv=lv, cnt=cnt, extra=extra)
            self[tWhen] = val

        return self

    def transfer(self, owner):
        owner.client.onSendRewardRecoveryActivity([(self.activityId, self.getDTO())])

    def isActivityInCloseTime(self, dayVal, rgd):
        closeStartime = rgd.get('closeStartTime', None)
        closeEndtime = rgd.get('closeEndtime', None)
        tWhen = dayVal.extra.get('time', 0)
        if closeStartime and closeEndtime and utils.getDisposableCronTabTimeStamp(closeStartime) <= tWhen <= utils.getDisposableCronTabTimeStamp(closeEndtime):
            return True
        return False

    def isItemGetBackInValidTime(self, data):
        flag = False
        if BigWorld.component in ('base', 'cell'):
            if not gameconfig.enableRewardRecovery():
                return flag
        elif not gameglobal.rds.configData.get('enableRewardRecovery', False):
            return flag
        beginTime = data.get('consumeItemStartTime')
        endTime = data.get('consumeItemEndTime')
        if beginTime and endTime and utils.inTimeTupleRange(beginTime[0], endTime[0], utils.getNow()):
            flag = True
        return flag

    def getEnableRewardRecovery(self):
        if BigWorld.component == 'client':
            import gameglobal
            enableRewardRecovery = gameglobal.rds.configData.get('enableRewardRecovery', 0)
        else:
            enableRewardRecovery = gameconfig.enableRewardRecovery()
        return enableRewardRecovery

    def getHolidayIncNum(self, rgd, holidayGetBackNum):
        beginTime = rgd.get('consumeItemStartTime')
        endTime = rgd.get('consumeItemEndTime')
        tNow = utils.getNow()
        if self.getEnableRewardRecovery() and holidayGetBackNum and beginTime and endTime and utils.inTimeTupleRange(beginTime[0], endTime[0], tNow):
            internalSecond = 0
            baset = utils.getMonthSecond()
            i = 0
            while internalSecond <= 0:
                baset -= i * const.TIME_INTERVAL_DAY
                baset = utils.getMonthSecond(baset)
                internalSecond = utils.getDaySecond() - (utils.nextByTimeTuple(beginTime[0], baset) + baset)
                i += 1

            if 365 <= int(round(internalSecond / const.TIME_INTERVAL_DAY)) <= 366:
                return 0
            return min(int(round(internalSecond / const.TIME_INTERVAL_DAY)), holidayGetBackNum)
        else:
            return 0

    def calcGetBackDays(self, data):
        day = data.get('day', 0)
        holidayGetBackDay = data.get('holidayGetBackDay', 0)
        if self.isItemGetBackInValidTime(data):
            holidayIncDay = self.getHolidayIncNum(data, holidayGetBackDay)
            day += holidayIncDay
        return day

    def calcMaxGetBackCount(self, data):
        count = data.get('count', 0)
        holidayGetBackCount = data.get('holidayGetBackCount', 0)
        if self.isItemGetBackInValidTime(data):
            holidayIncCount = self.getHolidayIncNum(data, holidayGetBackCount)
            count += holidayIncCount
        return count

    def calcHistoryGetBackNum(self, extraInfo = None):
        rgd = RGD.data.get(self.activityId, {})
        activityType = rgd.get('activityType', 0)
        maxGetBackCount = self.calcMaxGetBackCount(rgd)
        tWhen = utils.getDaySecond()
        getBackNum = 0
        rewardRecoveryServerOpTime = utils.getRewardRecoveryServerOpTime()
        if rewardRecoveryServerOpTime >= tWhen:
            return getBackNum
        activityCanGetbackStartTime = 0
        if rgd.get('activityCanGetbackStartTime', ''):
            activityCanGetbackStartTime = utils.getDisposableCronTabTimeStamp(rgd.get('activityCanGetbackStartTime', ''))
            if activityCanGetbackStartTime > tWhen:
                return getBackNum
        if activityType in gametypes.REWARD_RECOVER_ACTIVITY_DAILY_TYPE + gametypes.REWARD_RECOVER_ACTIVITY_TIMER_TYPE:
            for i in xrange(self.calcGetBackDays(rgd)):
                timeKey = tWhen - (i + 1) * const.SECONDS_PER_DAY
                if self.getBackRewardTime > timeKey or rewardRecoveryServerOpTime > timeKey or activityCanGetbackStartTime > timeKey:
                    continue
                if getBackNum >= maxGetBackCount:
                    break
                dayVal = self.daysVal.get(timeKey, None)
                if dayVal:
                    if self.isConditionValCanGetBack(dayVal, rgd):
                        getBackNum += 1

        elif activityType in gametypes.REWARD_RECOVER_ACTIVITY_WEEKLY_TYPE:
            thisWeekSecond = utils.getWeekSecond()
            lastWeekSecond = thisWeekSecond - const.TIME_INTERVAL_WEEK
            for i in xrange(maxGetBackCount):
                getBackFlag = True
                startTime = lastWeekSecond - i * const.TIME_INTERVAL_WEEK
                endTime = thisWeekSecond - i * const.TIME_INTERVAL_WEEK
                if utils.getWeekSecond(self.getBackRewardTime) > endTime - 1 or utils.getWeekSecond(rewardRecoveryServerOpTime) >= endTime or utils.getWeekSecond(activityCanGetbackStartTime) > endTime:
                    continue
                for timeKey in self.daysVal.iterkeys():
                    if utils.getWeekSecond(self.getBackRewardTime) > timeKey:
                        continue
                    if getBackNum >= maxGetBackCount:
                        break
                    if startTime <= timeKey < endTime:
                        dayVal = self.daysVal[timeKey]
                        if dayVal:
                            if not self.isConditionValCanGetBack(dayVal, rgd):
                                getBackFlag = False

                if getBackFlag:
                    getBackNum += 1

        return getBackNum

    def getHistoryRewardAndConsume(self, tp, canBackExpFormula, canBackBonus, getBackConsume, getBackConsumeCoinOriginal, dayVal, restCount = 1):
        exp = 0
        bonusIds = []
        consumeCoin = 0
        consumeCoinOriginal = 0
        consumeFames = {}
        if not dayVal:
            return (exp,
             bonusIds,
             consumeCoin,
             consumeFames)
        if canBackExpFormula:
            exp += canBackExpFormula({'lv': dayVal.lv,
             'restCount': restCount})
        if canBackBonus:
            for key in canBackBonus.keys():
                if key[0] <= dayVal.lv <= key[1]:
                    bonusId = canBackBonus.get(key, 0)
                    if bonusId:
                        for i in xrange(restCount):
                            bonusIds.append(bonusId)

        if getBackConsume:
            if tp == gametypes.ACTIVITY_REWARD_RECOVERY_TYPE_COIN:
                consumeCoin += getBackConsume({'lv': dayVal.lv,
                 'restCount': restCount})
                if getBackConsumeCoinOriginal:
                    consumeCoinOriginal += getBackConsumeCoinOriginal({'lv': dayVal.lv,
                     'restCount': restCount})
            elif tp in gametypes.ACTIVITY_REWARD_RECOVERY_TYPE_FAME:
                idx = tp - gametypes.ACTIVITY_REWARD_RECOVERY_TYPE_FAME1
                fameId, fameFormula = getBackConsume[idx]
                if fameFormula:
                    if consumeFames.has_key(fameId):
                        consumeFames[fameId] += fameFormula({'lv': dayVal.lv,
                         'restCount': restCount})
                    else:
                        consumeFames[fameId] = fameFormula({'lv': dayVal.lv,
                         'restCount': restCount})
        return (exp,
         bonusIds,
         consumeCoin,
         consumeFames,
         consumeCoinOriginal)

    def onCalcHistoryRewardAndConsume(self, tp, canBackExpFormula, canBackBonus, getBackConsume, getBackConsumeCoinOriginal, canBackFame, extraInfo = None):
        rgd = RGD.data.get(self.activityId, {})
        day = rgd.get('day', 0)
        activityType = rgd.get('activityType', 0)
        conditionLv = rgd.get('conditionLv', 0)
        maxGetBackCount = self.calcMaxGetBackCount(rgd)
        tWhen = utils.getDaySecond()
        exp = 0
        bonusIds = []
        consumeCoin = 0
        consumeCoinOriginal = 0
        rewardFames = {}
        consumeFames = {}
        getBackNum = 0
        rewardRecoveryServerOpTime = utils.getRewardRecoveryServerOpTime()
        activityCanGetbackStartTime = 0
        if rgd.get('activityCanGetbackStartTime', ''):
            activityCanGetbackStartTime = utils.getDisposableCronTabTimeStamp(rgd.get('activityCanGetbackStartTime', ''))
            if activityCanGetbackStartTime > tWhen:
                return {}
        if activityType in gametypes.REWARD_RECOVER_ACTIVITY_DAILY_TYPE + gametypes.REWARD_RECOVER_ACTIVITY_TIMER_TYPE:
            for i in xrange(self.calcGetBackDays(rgd)):
                if getBackNum >= maxGetBackCount:
                    break
                timeKey = tWhen - (i + 1) * const.SECONDS_PER_DAY
                if self.getBackRewardTime > timeKey or rewardRecoveryServerOpTime > timeKey or activityCanGetbackStartTime > timeKey:
                    continue
                dayVal = self.daysVal.get(timeKey, None)
                if dayVal:
                    if self.isConditionValCanGetBack(dayVal, rgd):
                        expDay, bonusIdsDay, consumeCoinDay, consumeFamesDay, consumeCoinOriginalDay = self.getHistoryRewardAndConsume(tp, canBackExpFormula, canBackBonus, getBackConsume, getBackConsumeCoinOriginal, dayVal)
                        exp += expDay
                        bonusIds += bonusIdsDay
                        consumeCoin += consumeCoinDay
                        consumeCoinOriginal += consumeCoinOriginalDay
                        for fame in canBackFame:
                            fameId = fame[0]
                            fameVal = fame[1]
                            if rewardFames.has_key(fameId):
                                rewardFames[fameId] += fameVal
                            else:
                                rewardFames[fameId] = fameVal

                        for fameId, fameVal in consumeFamesDay.items():
                            if consumeFames.has_key(fameId):
                                consumeFames[fameId] += fameVal
                            else:
                                consumeFames[fameId] = fameVal

                        getBackNum += 1

        if activityType in gametypes.REWARD_RECOVER_ACTIVITY_WEEKLY_TYPE:
            thisWeekSecond = utils.getWeekSecond()
            lastWeekSecond = thisWeekSecond - const.TIME_INTERVAL_WEEK
            for i in xrange(maxGetBackCount):
                getBackFlag = True
                startTime = lastWeekSecond - i * const.TIME_INTERVAL_WEEK
                endTime = thisWeekSecond - i * const.TIME_INTERVAL_WEEK
                if utils.getWeekSecond(self.getBackRewardTime) >= endTime or utils.getWeekSecond(rewardRecoveryServerOpTime) >= endTime or utils.getWeekSecond(activityCanGetbackStartTime) >= endTime:
                    continue
                for key in self.daysVal.iterkeys():
                    if utils.getWeekSecond(self.getBackRewardTime) >= key:
                        continue
                    if startTime <= key < endTime:
                        dayVal = self.daysVal[key]
                        if dayVal:
                            if not self.isConditionValCanGetBack(dayVal, rgd):
                                getBackFlag = False
                                break

                if getBackFlag:
                    dayVal = self.daysVal.get(endTime)
                    if not dayVal:
                        continue
                    expDay, bonusIdsDay, consumeCoinDay, consumeFamesDay, consumeCoinOriginalDay = self.getHistoryRewardAndConsume(tp, canBackExpFormula, canBackBonus, getBackConsume, getBackConsumeCoinOriginal, dayVal)
                    exp += expDay
                    bonusIds += bonusIdsDay
                    consumeCoin += consumeCoinDay
                    consumeCoinOriginal += consumeCoinOriginalDay
                    for fame in canBackFame:
                        fameId = fame[0]
                        fameVal = fame[1]
                        if rewardFames.has_key(fameId):
                            rewardFames[fameId] += fameVal
                        else:
                            rewardFames[fameId] = fameVal

                    for fameId, fameVal in consumeFamesDay.items():
                        if consumeFames.has_key(fameId):
                            consumeFames[fameId] += fameVal
                        else:
                            consumeFames[fameId] = fameVal

        return {'exp': exp,
         'bonusIds': bonusIds,
         'consumeCoin': consumeCoin,
         'consumeFames': [ (fameId, int(cnt)) for fameId, cnt in consumeFames.iteritems() ],
         'consumeCoinOriginal': consumeCoinOriginal,
         'rewardFames': rewardFames}

    def calcHistoryRewardAndConsume(self, owner, tp, extraInfo = None):
        rewardAndConsumeInfo = {}
        subId = extraInfo.get('subId', 0) if extraInfo else 0
        rgd = RGD.data.get(subId, {}) if subId else RGD.data.get(self.activityId, {})
        if not rgd:
            return rewardAndConsumeInfo
        getBackConsumeCoinOriginal = None
        if tp == gametypes.ACTIVITY_REWARD_RECOVERY_TYPE_COIN:
            canBackExpFormula = rgd.get('addExpByCoin')
            canBackBonus = rgd.get('bonusIdByCoin', {})
            canBackFame = rgd.get('addFameByCoin', ())
            getBackConsume = self.calcRewardGetBackConsumeCoin(rgd)
            getBackConsumeCoinOriginal = self.getConsumeCoinOriginal(rgd)
        elif tp in gametypes.ACTIVITY_REWARD_RECOVERY_TYPE_FAME:
            canBackExpFormula = rgd.get('addExpByFame')
            canBackBonus = rgd.get('bonusIdByFame', {})
            canBackFame = rgd.get('addFameByFame', ())
            getBackConsume = rgd.get('rewardGetBackConsumeFame', {})
        rewardAndConsumeInfo = self.onCalcHistoryRewardAndConsume(tp, canBackExpFormula, canBackBonus, getBackConsume, getBackConsumeCoinOriginal, canBackFame, extraInfo)
        return rewardAndConsumeInfo

    def getConsumeCoinOriginal(self, rgd):
        if BigWorld.component in ('base', 'cell'):
            if gameconfig.enableRewardRecoveryNew():
                return rgd.get('rewardGetBackConsumeCoin1', None)
            return None
        elif gameglobal.rds.configData.get('enableRewardRecoveryNew', False):
            return rgd.get('rewardGetBackConsumeCoin1', None)
        else:
            return None

    def calcRewardGetBackConsumeCoin(self, rgd):
        if BigWorld.component in ('base', 'cell'):
            if not gameconfig.enableRewardRecoveryNew():
                return rgd.get('rewardGetBackConsumeCoin', None)
        elif not gameglobal.rds.configData.get('enableRewardRecoveryNew', False):
            return rgd.get('rewardGetBackConsumeCoin', None)
        serverOpenTime = utils.getServerOpenTime()
        from data import sys_config_data as SCD
        rewardGetbackHostGroupByDays = SCD.data.get('rewardGetbackHostGroupByDays', None)
        if not rewardGetbackHostGroupByDays:
            return rgd.get('rewardGetBackConsumeCoin', None)
        flag = False
        groupId = 0
        for i in xrange(len(rewardGetbackHostGroupByDays)):
            if rewardGetbackHostGroupByDays[i][0] * const.SECONDS_PER_DAY <= utils.getNow() - serverOpenTime <= rewardGetbackHostGroupByDays[i][1] * const.SECONDS_PER_DAY:
                flag = True
                groupId = i + 1

        costCoinStr = 'rewardGetBackConsumeCoin'
        if flag:
            costCoinStr += str(groupId)
        return rgd.get(costCoinStr, None)

    def onActivityCompletedByType(self, owner, type, args = ()):
        if not owner:
            return
        if type == gametypes.REWARD_RECOVER_ACTIVITY_COMPLETE_TYPE_FINISH_INC:
            tWhen = utils.getDaySecond()
            if not self.getActivityDayVal(tWhen):
                c = ActivityDayVal()
                self.daysVal[tWhen] = c
            val = self.daysVal[tWhen]
            extra = {}
            val.update(owner.lv, 1, extra)


class CommonDailyRewardRecovery(IRewardRecoveryCommon):

    def guildDailyRefresh(self, owner):
        tWhen = utils.getDaySecond()
        day = self.calcGetBackDays(RGD.data.get(self.activityId, {}))
        for index in xrange(day + 1):
            if not self.getActivityDayVal(tWhen):
                c = ActivityDayVal()
                self.daysVal[tWhen] = c
                val = self.daysVal[tWhen]
                val.lv = owner.lv
                val.extra['time'] = tWhen + 1
                val.cnt = 1
            tWhen -= const.SECONDS_PER_DAY

        keys = self.daysVal.keys()
        for key in keys:
            if key <= tWhen:
                self.daysVal.pop(key)

        self.transfer(owner)

    def onActivityCompleted(self, owner, args = ()):
        self.onActivityCompletedByType(owner, gametypes.REWARD_RECOVER_ACTIVITY_COMPLETE_TYPE_FINISH_INC, args)

    def isConditionValCanGetBack(self, dayVal, rgd):
        flag = False
        if self.isActivityInCloseTime(dayVal, rgd):
            return flag
        conditionLv = rgd.get('conditionLv', 0)
        if dayVal.lv >= conditionLv and dayVal.cnt == 0:
            flag = True
        return flag


class ZhengZhanLingRewardRecovery(IRewardRecoveryCommon):

    def onActivityCompleted(self, owner, args = ()):
        self.onActivityCompletedByType(owner, gametypes.REWARD_RECOVER_ACTIVITY_COMPLETE_TYPE_FINISH_INC, args)

    def onActivityCompletedByType(self, owner, type, args = ()):
        if not owner:
            return
        if type == gametypes.REWARD_RECOVER_ACTIVITY_COMPLETE_TYPE_FINISH_INC:
            tWhen = utils.getWeekSecond()
            if not self.getActivityDayVal(tWhen):
                c = ActivityDayVal()
                self.daysVal[tWhen] = c
            val = self.daysVal[tWhen]
            extra = {}
            val.update(owner.lv, 1, extra)
        self.transfer(owner)

    def isConditionValCanGetBack(self, dayVal, rgd):
        gamelog.info('ZZL isConditionValCanGetBack', dayVal)
        flag = False
        if self.isActivityInCloseTime(dayVal, rgd):
            return flag
        conditionLv = rgd.get('conditionLv', 0)
        conditionVal = rgd.get('conditionVal', ())
        canGetBackMaxNum = conditionVal[1] if len(conditionVal) >= 2 else 0
        if dayVal.lv >= conditionLv and dayVal.cnt < canGetBackMaxNum:
            flag = True
        return flag

    def onCalcHistoryRewardAndConsume(self, tp, canBackExpFormula, canBackBonus, getBackConsume, getBackConsumeCoinOriginal, canBackFame, extraInfo = None):
        gamelog.info('ZZL onCalcHistoryRewardAndConsume', tp, canBackBonus)
        rgd = RGD.data.get(self.activityId, {})
        day = rgd.get('day', 0)
        activityType = rgd.get('activityType', 0)
        conditionLv = rgd.get('conditionLv', 0)
        conditionVal = rgd.get('conditionVal', ())
        maxGetBackCount = self.calcMaxGetBackCount(rgd)
        tWhen = utils.getDaySecond()
        exp = 0
        bonusIds = []
        consumeCoin = 0
        consumeCoinOriginal = 0
        rewardFames = {}
        consumeFames = {}
        getBackNum = 0
        rewardRecoveryServerOpTime = utils.getRewardRecoveryServerOpTime()
        finishCount = conditionVal[1] if len(conditionVal) >= 2 else 0
        activityCanGetbackStartTime = 0
        if rgd.get('activityCanGetbackStartTime', ''):
            activityCanGetbackStartTime = utils.getDisposableCronTabTimeStamp(rgd.get('activityCanGetbackStartTime', ''))
            if activityCanGetbackStartTime > tWhen:
                return {}
        if activityType in gametypes.REWARD_RECOVER_ACTIVITY_WEEKLY_TYPE:
            thisWeekSecond = utils.getWeekSecond()
            lastWeekSecond = thisWeekSecond - const.TIME_INTERVAL_WEEK
            for i in xrange(maxGetBackCount):
                getBackFlag = True
                startTime = lastWeekSecond - i * const.TIME_INTERVAL_WEEK
                endTime = thisWeekSecond - i * const.TIME_INTERVAL_WEEK
                if utils.getWeekSecond(self.getBackRewardTime) >= endTime or utils.getWeekSecond(rewardRecoveryServerOpTime) >= endTime or utils.getWeekSecond(activityCanGetbackStartTime) >= endTime:
                    continue
                for key in self.daysVal.iterkeys():
                    if utils.getWeekSecond(self.getBackRewardTime) >= key:
                        continue
                    if lastWeekSecond <= key < thisWeekSecond:
                        if not self.isConditionValCanGetBack(self.daysVal[key], rgd):
                            getBackFlag = False
                            break
                    if startTime <= key < endTime:
                        dayVal = self.daysVal[key]
                        if dayVal:
                            if not self.isConditionValCanGetBack(dayVal, rgd):
                                getBackFlag = False
                                break

                if getBackFlag:
                    dayVal = self.daysVal.get(lastWeekSecond)
                    if not dayVal:
                        continue
                    restCount = finishCount - dayVal.cnt if finishCount > dayVal.cnt else 1
                    expDay, bonusIdsDay, consumeCoinDay, consumeFamesDay, consumeCoinOriginalDay = self.getHistoryRewardAndConsume(tp, canBackExpFormula, canBackBonus, getBackConsume, getBackConsumeCoinOriginal, dayVal, restCount)
                    exp += expDay
                    bonusIds += bonusIdsDay
                    consumeCoin += consumeCoinDay
                    consumeCoinOriginal += consumeCoinOriginalDay
                    for fame in canBackFame:
                        fameId = fame[0]
                        fameVal = fame[1]
                        if rewardFames.has_key(fameId):
                            rewardFames[fameId] += fameVal
                        else:
                            rewardFames[fameId] = fameVal

                    for fameId, fameVal in consumeFamesDay.items():
                        if consumeFames.has_key(fameId):
                            consumeFames[fameId] += fameVal
                        else:
                            consumeFames[fameId] = fameVal

        return {'exp': exp,
         'bonusIds': bonusIds,
         'consumeCoin': consumeCoin,
         'consumeFames': [ (fameId, int(cnt)) for fameId, cnt in consumeFames.iteritems() ],
         'consumeCoinOriginal': consumeCoinOriginal,
         'rewardFames': rewardFames}


class AnYingXinMoRewardRecovery(IRewardRecoveryCommon):

    def onActivityCompleted(self, owner, args = ()):
        self.onActivityCompletedByType(owner, gametypes.REWARD_RECOVER_ACTIVITY_COMPLETE_TYPE_FINISH_INC, args)

    def isConditionValCanGetBack(self, dayVal, rgd):
        flag = False
        if self.isActivityInCloseTime(dayVal, rgd):
            return flag
        conditionLv = rgd.get('conditionLv', 0)
        conditionVal = rgd.get('conditionVal', ())
        canGetBackMaxNum = conditionVal[1]
        if dayVal.lv >= conditionLv and dayVal.cnt < canGetBackMaxNum:
            flag = True
        return flag

    def onCalcHistoryRewardAndConsume(self, tp, canBackExpFormula, canBackBonus, getBackConsume, getBackConsumeCoinOriginal, canBackFame, extraInfo = None):
        rgd = RGD.data.get(self.activityId, {})
        conditionVal = rgd.get('conditionVal', ())
        maxGetBackCount = self.calcMaxGetBackCount(rgd)
        tWhen = utils.getDaySecond()
        exp = 0
        bonusIds = []
        consumeCoin = 0
        consumeCoinOriginal = 0
        rewardFames = {}
        consumeFames = {}
        getBackNum = 0
        finishCount = conditionVal[1] if len(conditionVal) >= 2 else 0
        activityCanGetbackStartTime = 0
        if rgd.get('activityCanGetbackStartTime', ''):
            activityCanGetbackStartTime = utils.getDisposableCronTabTimeStamp(rgd.get('activityCanGetbackStartTime', ''))
        for i in xrange(self.calcGetBackDays(rgd)):
            if getBackNum >= maxGetBackCount:
                break
            timeKey = tWhen - (i + 1) * const.SECONDS_PER_DAY
            if self.getBackRewardTime > timeKey or utils.getRewardRecoveryServerOpTime() > timeKey or activityCanGetbackStartTime > timeKey:
                continue
            dayVal = self.daysVal.get(timeKey, None)
            if dayVal:
                if self.isConditionValCanGetBack(dayVal, rgd):
                    restCount = finishCount - dayVal.cnt if finishCount > dayVal.cnt else 1
                    expDay, bonusIdsDay, consumeCoinDay, consumeFamesDay, consumeCoinOriginalDay = self.getHistoryRewardAndConsume(tp, canBackExpFormula, canBackBonus, getBackConsume, getBackConsumeCoinOriginal, dayVal, restCount)
                    exp += expDay
                    bonusIds += bonusIdsDay
                    consumeCoin += consumeCoinDay
                    consumeCoinOriginal += consumeCoinOriginalDay
                    for fame in canBackFame:
                        fameId = fame[0]
                        fameVal = fame[1]
                        if rewardFames.has_key(fameId):
                            rewardFames[fameId] += fameVal
                        else:
                            rewardFames[fameId] = fameVal

                    for fameId, fameVal in consumeFamesDay.items():
                        if consumeFames.has_key(fameId):
                            consumeFames[fameId] += fameVal
                        else:
                            consumeFames[fameId] = fameVal

                    getBackNum += 1

        return {'exp': exp,
         'bonusIds': bonusIds,
         'consumeCoin': consumeCoin,
         'consumeFames': [ (fameId, int(cnt)) for fameId, cnt in consumeFames.iteritems() ],
         'consumeCoinOriginal': consumeCoinOriginal,
         'rewardFames': rewardFames}


class CommonWeeklyActivityRewardRecovery(IRewardRecoveryCommon):

    def onActivityCompleted(self, owner, args = ()):
        self.onActivityCompletedByType(owner, gametypes.REWARD_RECOVER_ACTIVITY_COMPLETE_TYPE_FINISH_INC, args)

    def isConditionValCanGetBack(self, dayVal, rgd):
        flag = False
        if self.isActivityInCloseTime(dayVal, rgd):
            return flag
        conditionLv = rgd.get('conditionLv', 0)
        if dayVal.lv >= conditionLv and dayVal.cnt == 0:
            flag = True
        return flag


class RestCountWeeklyActivityRewardRecovery(IRewardRecoveryCommon):

    def onActivityCompleted(self, owner, args = ()):
        self.onActivityCompletedByType(owner, gametypes.REWARD_RECOVER_ACTIVITY_COMPLETE_TYPE_FINISH_INC, args)

    def calcHistoryGetBackNum(self, extraInfo = None):
        getBackNum = 0
        rgd = RGD.data.get(self.activityId, {})
        conditionLv = rgd.get('conditionLv', 0)
        conditionVal = rgd.get('conditionVal', ())
        if not conditionVal or len(conditionVal) < 2:
            return getBackNum
        activityCanGetbackStartTime = 0
        if rgd.get('activityCanGetbackStartTime', ''):
            activityCanGetbackStartTime = utils.getDisposableCronTabTimeStamp(rgd.get('activityCanGetbackStartTime', ''))
        maxGetBackCount = self.calcMaxGetBackCount(rgd)
        thisWeekSecond = utils.getWeekSecond()
        lastWeekSecond = thisWeekSecond - const.TIME_INTERVAL_WEEK
        for i in xrange(maxGetBackCount):
            finishCount = 0
            startTime = lastWeekSecond - i * const.TIME_INTERVAL_WEEK
            endTime = thisWeekSecond - i * const.TIME_INTERVAL_WEEK
            if utils.getWeekSecond(self.getBackRewardTime) > endTime - 1 or utils.getWeekSecond(utils.getRewardRecoveryServerOpTime()) >= endTime or utils.getWeekSecond(activityCanGetbackStartTime) >= endTime:
                continue
            canGetBackFlag = False
            for timeKey in self.daysVal.iterkeys():
                if utils.getWeekSecond(self.getBackRewardTime) > timeKey:
                    continue
                if getBackNum >= maxGetBackCount:
                    break
                if startTime <= timeKey < endTime:
                    dayVal = self.daysVal[timeKey]
                    if dayVal:
                        if dayVal.lv >= conditionLv:
                            canGetBackFlag = True
                        if dayVal.lv >= conditionLv and dayVal.cnt > 0:
                            finishCount += dayVal.cnt

            if canGetBackFlag and finishCount < conditionVal[1]:
                getBackNum += 1

        return getBackNum

    def onCalcHistoryRewardAndConsume(self, tp, canBackExpFormula, canBackBonus, getBackConsume, getBackConsumeCoinOriginal, canBackFame, extraInfo = None):
        rgd = RGD.data.get(self.activityId, {})
        conditionLv = rgd.get('conditionLv', 0)
        maxGetBackCount = self.calcMaxGetBackCount(rgd)
        conditionVal = rgd.get('conditionVal', ())
        exp = 0
        bonusIds = []
        consumeCoin = 0
        consumeCoinOriginal = 0
        rewardFames = {}
        consumeFames = {}
        if not conditionVal or len(conditionVal) < 2:
            return {'exp': exp,
             'bonusIds': bonusIds,
             'consumeCoin': consumeCoin,
             'consumeFames': [ (fameId, int(cnt)) for fameId, cnt in consumeFames.iteritems() ]}
        activityCanGetbackStartTime = 0
        if rgd.get('activityCanGetbackStartTime', ''):
            activityCanGetbackStartTime = utils.getDisposableCronTabTimeStamp(rgd.get('activityCanGetbackStartTime', ''))
        finishCount = conditionVal[1]
        totalCount = 0
        restCount = 0
        thisWeekSecond = utils.getWeekSecond()
        lastWeekSecond = thisWeekSecond - const.TIME_INTERVAL_WEEK
        for i in xrange(maxGetBackCount):
            getBackFlag = True
            startTime = lastWeekSecond - i * const.TIME_INTERVAL_WEEK
            endTime = thisWeekSecond - i * const.TIME_INTERVAL_WEEK
            if utils.getWeekSecond(self.getBackRewardTime) >= endTime or utils.getWeekSecond(utils.getRewardRecoveryServerOpTime()) >= endTime or utils.getWeekSecond(activityCanGetbackStartTime) >= endTime:
                continue
            for timeKey in self.daysVal.iterkeys():
                if utils.getWeekSecond(self.getBackRewardTime) >= timeKey:
                    continue
                if startTime <= timeKey < endTime:
                    dayVal = self.daysVal[timeKey]
                    if dayVal:
                        if dayVal.lv >= conditionLv and dayVal.cnt > 0:
                            totalCount += dayVal.cnt

            if totalCount < finishCount:
                restCount += finishCount - totalCount
                dayVal = self.daysVal.get(endTime)
                if not dayVal:
                    continue
                expDay, bonusIdsDay, consumeCoinDay, consumeFamesDay, consumeCoinOriginalDay = self.getHistoryRewardAndConsume(tp, canBackExpFormula, canBackBonus, getBackConsume, getBackConsumeCoinOriginal, dayVal, restCount)
                exp += expDay
                bonusIds += bonusIdsDay
                consumeCoin += consumeCoinDay
                consumeCoinOriginal += consumeCoinOriginalDay
                for fame in canBackFame:
                    fameId = fame[0]
                    fameVal = fame[1]
                    if rewardFames.has_key(fameId):
                        rewardFames[fameId] += fameVal
                    else:
                        rewardFames[fameId] = fameVal

                for fameId, fameVal in consumeFamesDay.items():
                    if consumeFames.has_key(fameId):
                        consumeFames[fameId] += fameVal
                    else:
                        consumeFames[fameId] = fameVal

        return {'exp': exp,
         'bonusIds': bonusIds,
         'consumeCoin': consumeCoin,
         'consumeFames': [ (fameId, int(cnt)) for fameId, cnt in consumeFames.iteritems() ],
         'consumeCoinOriginal': consumeCoinOriginal,
         'rewardFames': rewardFames}


class ExpandTabWeeklyActivityRewardRecovery(IRewardRecoveryCommon):
    ARGS_LENGTH = 2
    ONE_WEEK_DAYS = 7
    COIN_MODE_DEFAULT = 'coin1'

    def onActivityCompleted(self, owner, args = ()):
        if not owner:
            return
        if len(args) != self.ARGS_LENGTH:
            return
        tWhen = utils.getWeekSecond()
        if not self.getActivityDayVal(tWhen):
            self.daysVal[tWhen] = ActivityDayVal()
        val = self.daysVal[tWhen]
        val.lv = owner.lv
        val.cnt += 1
        val.extra['bonusCnt'], val.extra['extraLv'] = args
        val.extra['time'] = utils.getNow()

    def isConditionValCanGetBack(self, dayVal, rgd):
        if self.isActivityInCloseTime(dayVal, rgd):
            return False
        else:
            activityType, conditionLv, conditionVal = rgd.get('activityType', 0), rgd.get('conditionLv', 0), rgd.get('conditionVal', [])
            extraLv = dayVal.extra.get('extraLv', 0)
            qjrgd = QJRGD.data.get((extraLv, activityType), {})
            enableWingWorld = gameglobal.rds.configData.get('enableWingWorld') if BigWorld.component == 'client' else gameconfig.enableWingWorld()
            rgdBonus = qjrgd.get('wingWorldbonusId', []) if enableWingWorld else qjrgd.get('bonusId', [])
            gamelog.debug('@hqx_get_isConditionValCanGetBack', dayVal, conditionVal)
            if dayVal.lv < conditionLv:
                return False
            if not conditionVal:
                return False
            bonusCnt = dayVal.extra.get('bonusCnt', [])
            if rgd.get('parentId', 0) == self.activityId:
                for val in conditionVal:
                    if val in bonusCnt:
                        return False
                    if val > len(rgdBonus):
                        return False
                    if not rgdBonus[val - 1]:
                        return False

                return True
            flag = False
            for val in conditionVal:
                if val in bonusCnt:
                    continue
                if val > len(rgdBonus):
                    continue
                if not rgdBonus[val - 1]:
                    continue
                flag = True
                break

            return flag

    def refreshDaily(self, owner):
        tWhen = utils.getWeekSecond()
        week = self.calcGetBackDays(RGD.data.get(self.activityId, {})) / self.ONE_WEEK_DAYS
        for index in xrange(week):
            if tWhen in self.daysVal:
                modifyTime = self.daysVal[tWhen].extra.get('time', 0)
                if utils.getWeekSecond(modifyTime) == tWhen:
                    owner.cell.refreshRewardRecoverActivityExtraLv(tWhen, self.activityId)
            else:
                val = ActivityDayVal()
                val.lv = owner.lv
                val.extra['time'] = tWhen + 1
                self.daysVal[tWhen] = val
                owner.cell.refreshRewardRecoverActivityExtraLv(tWhen, self.activityId)
            tWhen -= const.SECONDS_PER_WEEK

        keys = self.daysVal.keys()
        for key in keys:
            if key <= tWhen:
                self.daysVal.pop(key)

        self.transfer(owner)

    def refreshExtraLv(self, owner, extraLv, tWhen):
        self.daysVal[tWhen].extra['time'] = utils.getNow()
        self.daysVal[tWhen].extra['extraLv'] = extraLv
        self.transfer(owner)

    def calcHistoryGetBackNum(self, extraInfo = None):
        subId = extraInfo.get('subId', 0) if extraInfo else 0
        rgd = RGD.data.get(subId, {}) if subId else RGD.data.get(self.activityId, {})
        getBackNum = 0
        tWhen = utils.getDaySecond()
        if subId and subId != self.activityId and RGD.data.get(subId, {}).get('parentId', 0) != self.activityId:
            return getBackNum
        tp = extraInfo.get('tp', 0) if extraInfo else 0
        if tp != gametypes.ACTIVITY_REWARD_RECOVERY_TYPE_COIN:
            return getBackNum
        rewardRecoveryServerOpTime = utils.getRewardRecoveryServerOpTime()
        if rewardRecoveryServerOpTime >= tWhen:
            return getBackNum
        activityCanGetbackStartTime = 0
        if rgd.get('activityCanGetbackStartTime', ''):
            activityCanGetbackStartTime = utils.getDisposableCronTabTimeStamp(rgd.get('activityCanGetbackStartTime', ''))
            if activityCanGetbackStartTime > tWhen:
                return getBackNum
        thisWeekSecond = utils.getWeekSecond()
        lastWeekSecond = thisWeekSecond - const.TIME_INTERVAL_WEEK
        maxGetBackCount = self.calcMaxGetBackCount(rgd)
        for i in xrange(maxGetBackCount):
            startTime = lastWeekSecond - i * const.TIME_INTERVAL_WEEK
            endTime = thisWeekSecond - i * const.TIME_INTERVAL_WEEK
            if utils.getWeekSecond(rewardRecoveryServerOpTime) >= endTime or utils.getWeekSecond(activityCanGetbackStartTime) > endTime:
                continue
            dayVal = self.daysVal.get(startTime)
            if dayVal and self.isConditionValCanGetBack(dayVal, rgd):
                getBackNum += 1

        gamelog.debug('@hqx_get_calcHistoryGetBackNum', getBackNum)
        return getBackNum

    def onCalcHistoryRewardAndConsume(self, tp, canBackExpFormula, canBackBonus, getBackConsume, getBackConsumeCoinOriginal, canBackFame, extraInfo = None):
        subId = extraInfo.get('subId', 0) if extraInfo else 0
        rgd = RGD.data.get(subId, {}) if subId else RGD.data.get(self.activityId, {})
        activityType, conditionVal = rgd.get('activityType', 0), rgd.get('conditionVal', [])
        rewardRecoveryServerOpTime = utils.getRewardRecoveryServerOpTime()
        if tp != gametypes.ACTIVITY_REWARD_RECOVERY_TYPE_COIN:
            return {}
        tWhen = utils.getDaySecond()
        activityCanGetbackStartTime = 0
        if rgd.get('activityCanGetbackStartTime', ''):
            activityCanGetbackStartTime = utils.getDisposableCronTabTimeStamp(rgd.get('activityCanGetbackStartTime', ''))
            if activityCanGetbackStartTime > tWhen:
                return {}
        thisWeekSecond = utils.getWeekSecond()
        lastWeekSecond = thisWeekSecond - const.TIME_INTERVAL_WEEK
        maxGetBackCount = self.calcMaxGetBackCount(rgd)
        bonusIds = []
        consumeCoin = 0
        consumeCoinOriginal = 0
        rgdBonus = None
        for i in xrange(maxGetBackCount):
            startTime = lastWeekSecond - i * const.TIME_INTERVAL_WEEK
            endTime = thisWeekSecond - i * const.TIME_INTERVAL_WEEK
            if utils.getWeekSecond(rewardRecoveryServerOpTime) >= endTime or utils.getWeekSecond(activityCanGetbackStartTime) > endTime:
                continue
            dayVal = self.daysVal.get(startTime)
            if not dayVal or not self.isConditionValCanGetBack(dayVal, rgd):
                continue
            bonusCnt, extraLv = dayVal.extra.get('bonusCnt', []), dayVal.extra.get('extraLv', 0)
            qjrgd = QJRGD.data.get((extraLv, activityType), {})
            enableWingWorld = gameglobal.rds.configData.get('enableWingWorld') if BigWorld.component == 'client' else gameconfig.enableWingWorld()
            rgdBonus = qjrgd.get('wingWorldbonusId', []) if enableWingWorld else qjrgd.get('bonusId', [])
            for val in conditionVal:
                if val > len(rgdBonus):
                    continue
                if val in bonusCnt:
                    continue
                if rgdBonus[val - 1]:
                    bonusIds.append(rgdBonus[val - 1])

            coinMode = self.calcBonusCoinMode()
            for bonusId in bonusIds:
                consumeCoin += QJRPD.data.get(bonusId, {}).get(coinMode, 0)
                consumeCoinOriginal += QJRPD.data.get(bonusId, {}).get(self.COIN_MODE_DEFAULT, 0)

        gamelog.debug('@hqx_onCalcHistoryRewardAndConsume', bonusIds, rgdBonus, conditionVal)
        return {'bonusIds': bonusIds,
         'consumeCoin': consumeCoin,
         'consumeCoinOriginal': consumeCoinOriginal}

    def calcBonusCoinMode(self):
        import gameconfigCommon
        if not gameconfigCommon.enableRewardRecoveryNew():
            return self.COIN_MODE_DEFAULT
        serverOpenTime = utils.getServerOpenTime()
        rewardGetbackHostGroupByDays = SCD.data.get('rewardGetbackHostGroupByDays', None)
        if not rewardGetbackHostGroupByDays:
            return self.COIN_MODE_DEFAULT
        flag = False
        groupId = 0
        for i in xrange(len(rewardGetbackHostGroupByDays)):
            if rewardGetbackHostGroupByDays[i][0] * const.SECONDS_PER_DAY <= utils.getNow() - serverOpenTime <= rewardGetbackHostGroupByDays[i][1] * const.SECONDS_PER_DAY:
                flag = True
                groupId = i + 1

        if flag:
            return 'coin' + str(groupId)
        return self.COIN_MODE_DEFAULT

    def markBonusCnt(self, owner, subId):
        rgd = RGD.data.get(subId, {})
        maxGetBackCount = self.calcMaxGetBackCount(rgd)
        thisWeekSecond = utils.getWeekSecond()
        lastWeekSecond = thisWeekSecond - const.TIME_INTERVAL_WEEK
        activityType, conditionVal = rgd.get('activityType', 0), rgd.get('conditionVal', [])
        rewardRecoveryServerOpTime = utils.getRewardRecoveryServerOpTime()
        activityCanGetbackStartTime = utils.getDisposableCronTabTimeStamp(rgd.get('activityCanGetbackStartTime', '0 0 6 5 * 2019'))
        for i in xrange(maxGetBackCount):
            startTime = lastWeekSecond - i * const.TIME_INTERVAL_WEEK
            endTime = thisWeekSecond - i * const.TIME_INTERVAL_WEEK
            if utils.getWeekSecond(rewardRecoveryServerOpTime) >= endTime or utils.getWeekSecond(activityCanGetbackStartTime) > endTime:
                continue
            dayVal = self.daysVal.get(startTime)
            if not dayVal or not self.isConditionValCanGetBack(dayVal, rgd):
                continue
            bonusCnt, extraLv = dayVal.extra.get('bonusCnt', []), dayVal.extra.get('extraLv', 0)
            tmpCnt = []
            qjrgd = QJRGD.data.get((extraLv, activityType), {})
            enableWingWorld = gameglobal.rds.configData.get('enableWingWorld') if BigWorld.component == 'client' else gameconfig.enableWingWorld()
            rgdBonus = qjrgd.get('wingWorldbonusId', []) if enableWingWorld else qjrgd.get('bonusId', [])
            for val in conditionVal:
                if val > len(rgdBonus):
                    continue
                if val in bonusCnt:
                    continue
                if rgdBonus[val - 1]:
                    tmpCnt.append(val)

            bonusCnt += tmpCnt
            dayVal.extra['bonusCnt'] = bonusCnt
            gamelog.debug('@hqx_get_markBonusCnt', dayVal)

        self.transfer(owner)


class CommonTimingActivityRewardRecovery(IRewardRecoveryCommon):

    def guildDailyRefresh(self, owner):
        tWhen = utils.getDaySecond()
        day = self.calcGetBackDays(RGD.data.get(self.activityId, {}))
        for index in xrange(day + 1):
            if not self.getActivityDayVal(tWhen):
                c = ActivityDayVal()
                self.daysVal[tWhen] = c
                val = self.daysVal[tWhen]
                val.lv = owner.lv
                val.extra['time'] = tWhen + 1
                val.cnt = 1
            tWhen -= const.SECONDS_PER_DAY

        keys = self.daysVal.keys()
        for key in keys:
            if key <= tWhen:
                self.daysVal.pop(key)

        self.transfer(owner)

    def onActivityCompleted(self, owner, args = ()):
        self.onActivityCompletedByType(owner, gametypes.REWARD_RECOVER_ACTIVITY_COMPLETE_TYPE_FINISH_INC, args)

    def onActivityCompletedByType(self, owner, type, args = ()):
        if not owner:
            return
        if type == gametypes.REWARD_RECOVER_ACTIVITY_COMPLETE_TYPE_FINISH_INC:
            tWhen = utils.getDaySecond()
            if not self.getActivityDayVal(tWhen):
                c = ActivityDayVal()
                self.daysVal[tWhen] = c
            val = self.daysVal[tWhen]
            extra = {}
            if not val.cnt:
                val.update(owner.lv, 1, extra)

    def onActivityCompletedForSkyWing(self, owner, args = ()):
        self.onActivityCompletedBySkyWing(owner, args)

    def onActivityCompletedBySkyWing(self, owner, args = ()):
        if not owner:
            return
        completeTime, = args
        tWhen = utils.getDaySecond(completeTime)
        if not self.getActivityDayVal(tWhen):
            c = ActivityDayVal()
            self.daysVal[tWhen] = c
        val = self.daysVal[tWhen]
        extra = {'time': completeTime}
        if not val.cnt:
            val.update(owner.lv, 1, extra)

    def isConditionValCanGetBack(self, dayVal, rgd):
        flag = False
        if self.isActivityInCloseTime(dayVal, rgd):
            return flag
        conditionLv = rgd.get('conditionLv', 0)
        newStartTime = rgd.get('newStartTime', None)
        tWhen = utils.getNow()
        if newStartTime and utils.getDisposableCronTabTimeStamp(newStartTime) <= tWhen:
            startCrontab = rgd.get('newStartTimes')
            endCrontab = rgd.get('newEndTimes')
        else:
            startCrontab = rgd.get('startTimes')
            endCrontab = rgd.get('endTimes')
        completeTime = dayVal.extra.get('time', 0)
        if startCrontab and endCrontab and utils.inDateRange(startCrontab[0], endCrontab[0], completeTime):
            if dayVal.lv >= conditionLv:
                if dayVal.cnt == 0:
                    flag = True
                elif not utils.inCrontabRange(startCrontab[0], endCrontab[0], completeTime):
                    flag = True
        return flag


class CompareTotalTimingActivityRewardRecovery(CommonTimingActivityRewardRecovery):

    def onActivityCompleted(self, owner, args = ()):
        conditionVal = RGD.data.get(self.activityId, {}).get('conditionVal', ())
        contributeScore = args[0]
        limitContributeScore = conditionVal[0]
        if contributeScore >= limitContributeScore:
            self.onActivityCompletedByType(owner, gametypes.REWARD_RECOVER_ACTIVITY_COMPLETE_TYPE_FINISH_INC, args)


class RotateTimingActivityRewardRecovery(CommonTimingActivityRewardRecovery):

    def isConditionValCanGetBack(self, dayVal, rgd):
        flag = False
        if self.isActivityInCloseTime(dayVal, rgd):
            return flag
        conditionLv = rgd.get('conditionLv', 0)
        newStartTime = rgd.get('newStartTime', None)
        tWhen = utils.getNow()
        if newStartTime and utils.getDisposableCronTabTimeStamp(newStartTime) <= tWhen:
            startCrontab = rgd.get('newStartTimes')
            endCrontab = rgd.get('newEndTimes')
        else:
            startCrontab = rgd.get('startTimes')
            endCrontab = rgd.get('endTimes')
        completeTime = dayVal.extra.get('time', 0)
        weekSet = rgd.get('weekSet', 0)
        if startCrontab and endCrontab and not utils.isInvalidWeek(weekSet, completeTime) and utils.inDateRange(startCrontab[0], endCrontab[0], completeTime):
            if dayVal.lv >= conditionLv:
                if dayVal.cnt == 0:
                    flag = True
                elif not utils.inCrontabRange(startCrontab[0], endCrontab[0], completeTime):
                    flag = True
        return flag
