#Embedded file name: /WORKSPACE/data/entities/common/commnewserveractivity.o
import BigWorld
import utils
from data import new_server_activity_data as NSAD
from data import lottery_data as LD

def isNewServerActivityOpen(activityId):
    if BigWorld.component in ('base', 'cell'):
        import gameconfig
        activityListStr = gameconfig.enableNewServerActivity()
    else:
        import gameglobal
        activityListStr = gameglobal.rds.configData.get('enableNewServerActivity', '')
    activityList = activityListStr.split(',')
    return str(activityId) in activityList


def checkNSJingSuInActivityTime(fbNo):
    jingSuFubens = NSAD.data.get('jingSuFubens', {})
    if not jingSuFubens:
        return False
    if not jingSuFubens.has_key(fbNo):
        return False
    jingSuFb = jingSuFubens[fbNo]
    msId, activityOpenDay, _ = jingSuFb
    if msId:
        if BigWorld.component in ('base', 'cell'):
            import serverProgress
            import gameconst
            msFinished = serverProgress.isMileStoneFinished(msId)
            if not msFinished:
                return False
            tMsFinish = serverProgress.getProgressStatus(gameconst.SP_PROP_MILE_STONE, msId)
        else:
            p = BigWorld.player()
            msFinished = p.isServerProgressFinished(msId)
            if not msFinished:
                return False
            tMsFinish = p.getServerProgressFinishTime(msId)
        openDay = utils.getDaysByTime(tMsFinish)
    else:
        openDay = utils.getServerOpenDays()
    if openDay + 1 > activityOpenDay:
        return False
    return True


def checkNSJingSuInDisPlayTime(fbNo):
    jingSuFubens = NSAD.data.get('jingSuFubens', {})
    if not jingSuFubens:
        return False
    if not jingSuFubens.has_key(fbNo):
        return False
    jingSuFb = jingSuFubens[fbNo]
    msId, activityOpenDay, _ = jingSuFb
    if msId:
        if BigWorld.component in ('base', 'cell'):
            import serverProgress
            import gameconst
            msFinished = serverProgress.isMileStoneFinished(msId)
            if not msFinished:
                return False
            tMsFinish = serverProgress.getProgressStatus(gameconst.SP_PROP_MILE_STONE, msId)
        else:
            p = BigWorld.player()
            msFinished = p.isServerProgressFinished(msId)
            if not msFinished:
                return False
            tMsFinish = p.getServerProgressFinishTime(msId)
        openDay = utils.getDaysByTime(tMsFinish)
    else:
        openDay = utils.getServerOpenDays()
    jingSuRewardOpenDay = NSAD.data.get('jingSuRewardOpenDay', 0)
    if openDay + 1 > activityOpenDay + jingSuRewardOpenDay:
        return False
    return True


def checkNSFirstKillInActivityTime():
    openDay = utils.getServerOpenDays()
    firstKillActivityOpenDay = NSAD.data.get('firstKillActivityOpenDay', 60)
    if openDay + 1 > firstKillActivityOpenDay:
        return False
    return True


def checkNSFirstKillInDisplayTime(firstKillEndFbs):
    firstKillFubens = NSAD.data.get('firstKillFubens', ())
    if not firstKillFubens:
        return False
    isAllFinish = True
    tAllFinish = 0
    for fbNo in firstKillFubens:
        if not firstKillEndFbs.has_key(fbNo):
            isAllFinish = False
            break
        tAllFinish = firstKillEndFbs[fbNo][0] if firstKillEndFbs[fbNo][0] > tAllFinish else tAllFinish

    if isAllFinish and tAllFinish:
        firstKillRewardOpenDay = NSAD.data.get('firstKillRewardOpenDay', 7)
        openDay = utils.getDaysByTime(tAllFinish)
        if openDay + 1 > firstKillRewardOpenDay:
            return False
    else:
        firstKillActivityOpenDay = NSAD.data.get('firstKillActivityOpenDay', 60)
        openDay = utils.getServerOpenDays()
        if openDay + 1 > firstKillActivityOpenDay:
            return False
    return True


def checkNSExpBonusInActivityTime():
    openDay = utils.getServerOpenDays()
    expBonusOpenDay = NSAD.data.get('expBonusOpenDay', 30)
    if openDay + 1 > expBonusOpenDay:
        return False
    return True


def checkGlobalExpBonusInActivityTime():
    globalExpBonusStartTimes = NSAD.data.get('globalExpBonusStartTimes', ())
    globalExpBonusEndTimes = NSAD.data.get('globalExpBonusEndTimes', ())
    return utils.inCrontabsRange(globalExpBonusStartTimes, globalExpBonusEndTimes)


def checkNSDailyGiftInActivityTime():
    openDay = utils.getServerOpenDays()
    dailyGiftOpenDay = NSAD.data.get('dailyGiftOpenDay', 7)
    if openDay + 1 > dailyGiftOpenDay:
        return False
    return True


def checkNSLotteryInDisplayTime(lotteryId):
    ld = LD.data.get(lotteryId)
    if not ld:
        return False
    lotteryStartTime = ld.get('lotteryStartTime', '')
    if not lotteryStartTime:
        return False
    lotteryEndTime = ld.get('lotteryEndTime', '')
    if not lotteryEndTime:
        return False
    lotteryStartTime = utils.getTimeSecondFromStr(lotteryStartTime)
    lotteryDisplayEndTime = utils.getDayEndSecondFromStr(lotteryEndTime)
    now = utils.getNow()
    if now < lotteryStartTime or now >= lotteryDisplayEndTime:
        return False
    return True


def checkNSLotteryInAddTime(lotteryId):
    ld = LD.data.get(lotteryId)
    if not ld:
        return False
    lotteryStartTime = ld.get('lotteryStartTime', '')
    if not lotteryStartTime:
        return False
    lotteryEndTime = ld.get('lotteryEndTime', '')
    if not lotteryEndTime:
        return False
    lotteryStartTime = utils.getTimeSecondFromStr(lotteryStartTime)
    lotteryEndTime = utils.getTimeSecondFromStr(lotteryEndTime)
    now = utils.getNow()
    if now < lotteryStartTime or now >= lotteryEndTime:
        return False
    return True


def getNSLotteryNextTime(lotteryId):
    ld = LD.data.get(lotteryId)
    if not ld:
        return 0
    now = utils.getNow()
    lotteryTime = ld.get('lotteryTime', '')
    if not lotteryTime:
        return 0
    lotteryInterval = ld.get('lotteryInterval', 0)
    if not lotteryInterval:
        return 0
    lotteryTime = utils.getTimeSecondFromStr(lotteryTime)
    nextTime = utils.getLotteryNextTime(now, lotteryTime, lotteryInterval)
    if nextTime == now:
        nextTime += lotteryInterval
    lotteryEndTime = ld.get('lotteryEndTime', '')
    lotteryEndTime = utils.getTimeSecondFromStr(lotteryEndTime)
    if nextTime > lotteryEndTime:
        nextTime = lotteryEndTime
    return nextTime


def getLotteryIndexByNextTime(nextTime, lotteryTime, lotteryInterval):
    if nextTime < lotteryTime:
        return 0
    return (nextTime - lotteryTime) / lotteryInterval


def getLotteryTodayIssueTime(lotteryId):
    ld = LD.data.get(lotteryId)
    if not ld:
        return 0
    lotteryInterval = ld.get('lotteryInterval', 0)
    if not lotteryInterval:
        return 0
    nextIssueTime = getNSLotteryNextTime(lotteryId)
    if utils.isSameDay(utils.getNow(), nextIssueTime):
        return nextIssueTime
    return nextIssueTime - lotteryInterval


def checkLotteryInServerConfigList(lotteryId):
    ld = LD.data.get(lotteryId)
    if not ld:
        return False
    serverConfigId = ld.get('serverConfigId')
    if not serverConfigId:
        return True
    if not utils.checkInCorrectServer(serverConfigId):
        return False
    return True


def checkNSAchieveInActivityTime():
    openDay = utils.getServerOpenDays()
    achieveOpenDay = NSAD.data.get('achieveOpenDay', 15)
    if openDay + 1 > achieveOpenDay:
        return False
    return True
