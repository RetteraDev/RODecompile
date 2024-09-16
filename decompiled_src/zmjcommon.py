#Embedded file name: /WORKSPACE/data/entities/common/zmjcommon.o
import BigWorld
import const
import utils
import formula
from checkResult import CheckResult
from data import zmj_fuben_config_data as ZFCD
from cdata import game_msg_def_data as GMDD

def onZMJStart():
    if BigWorld.component in ('base', 'cell'):
        import Netease
        Netease.zmjIsOpen = True


def onZMJEnd():
    if BigWorld.component in ('base', 'cell'):
        import Netease
        Netease.zmjIsOpen = False


def checkinZMJTime(timeStamp = 0, useCache = True):
    if BigWorld.component in ('base', 'cell') and useCache:
        import Netease
        return Netease.zmjIsOpen
    timeStamp = timeStamp or utils.getNow()
    startCrontab, endTimeCrontab = ZFCD.data.get('startCrontab'), ZFCD.data.get('endCrontab')
    if not startCrontab or not endTimeCrontab:
        return False
    else:
        return utils.inCrontabRangeWithYear(startCrontab, endTimeCrontab, timeStamp)


def checkInZMJFbPermitTime(timeStamp = 0):
    timeStamp = timeStamp or utils.getNow()
    fbStartTimeInDay, fbEndTimeInDay = ZFCD.data.get('fbStartTimeInDay'), ZFCD.data.get('fbEndTimeInDay')
    if not fbStartTimeInDay or not fbEndTimeInDay:
        return False
    startTimeInDay = utils.getDayTimeSecondsFromHMS(fbStartTimeInDay)
    endTimeInDay = utils.getDayTimeSecondsFromHMS(fbEndTimeInDay)
    return checkinZMJTime(timeStamp) and startTimeInDay <= timeStamp <= endTimeInDay


def getDaysFromZMJStart():
    cur = utils.getNow()
    if not checkinZMJTime(cur):
        return 0
    startCrontab = ZFCD.data.get('startCrontab')
    if not startCrontab:
        return 0
    startTimeStamp = utils.getPreCrontabTime(startCrontab)
    if startTimeStamp > 0:
        return utils.getIntervalDay(cur, startTimeStamp)
    else:
        return 0


def getZMJPreStartTime():
    cur = utils.getNow()
    if not checkinZMJTime(cur):
        return 0
    startCrontab = ZFCD.data.get('startCrontab')
    if not startCrontab:
        return 0
    return utils.getPreCrontabTime(startCrontab)


def getZMJRangeAward(dmg, rank, thresholdDmg, dmgRoles = None):
    if dmgRoles is None:
        highFbTotalMaxDmgRewardsNotInTop = ZFCD.data.get('highFbTotalMaxDmgRewardsNotInTop', [])
        schoolDmgRoles = []
        for ratio, lowRank, highRank, dmgFix, mailId, mailStr in highFbTotalMaxDmgRewardsNotInTop:
            needDmg = min(max(0, int(ratio * thresholdDmg)), dmgFix)
            schoolDmgRoles.append(((needDmg,
              lowRank,
              highRank,
              dmgFix), (mailId, mailStr)))

    else:
        schoolDmgRoles = dmgRoles
    for idx, info in enumerate(schoolDmgRoles):
        (needDmg, lowRank, highRank, dmgFix), v = info
        if dmg >= dmgFix or dmg >= needDmg and rank <= lowRank or rank <= highRank:
            return (idx, v)

    return (-1, None)


def calcZMJLowCost(isBoost = False):
    cost = ZFCD.data.get('lowFubenCost', 0)
    if isBoost:
        cost *= ZFCD.data.get('boostCostCoef', 0)
    return int(cost)


def calcZMJAward(curStar, maxStar, thisStarTotalSucc, isBoost = False, isLucky = False):
    lowFbFameFormulaId = ZFCD.data.get('lowFbFameFormulaId')
    fameVal = 0
    if lowFbFameFormulaId:
        fameVal = int(formula.calcFormulaById(lowFbFameFormulaId, {'star': float(curStar),
         'isBoost': float(isBoost),
         'isLucky': float(isLucky)}))
        if thisStarTotalSucc > ZFCD.data.get('lowFbFameDiscountAfterCnt', const.MAX_UINT32):
            lowFbFameDiscountFormulaId = ZFCD.data.get('lowFbFameDiscountFormulaId')
            if lowFbFameDiscountFormulaId:
                fameVal = int(fameVal * formula.calcFormulaById(lowFbFameDiscountFormulaId, {'curStar': float(curStar),
                 'maxStar': float(maxStar),
                 'isBoost': float(isBoost),
                 'isLucky': float(isLucky)}))
                return fameVal
    return fameVal


def calcZMJAssistAward(star):
    lowFbAssistFameFormulaId = ZFCD.data.get('lowFbAssistFameFormulaId')
    return formula.calcFormulaById(lowFbAssistFameFormulaId, {'star': star})


def getZJMExpireTime():
    return ZFCD.data.get('starBossExpireTime', 0) + ZFCD.data.get('starBossFbFailRecordTime', 0)


def checkShareStarBoss(mVal, src, tar):
    if not mVal:
        return CheckResult(False, (GMDD.data.ZMJ_STAR_BOSS_NONE, ()))
    if mVal.founderGbId != src:
        return CheckResult(False, (GMDD.data.ZMJ_STAR_BOSS_SHARE_NOT_FOUNDER, ()))
    if mVal.star < ZFCD.data.get('starBossShareLevel', 0):
        return CheckResult(False, (GMDD.data.ZMJ_STAR_BOSS_SHARE_UNDER_STAR, ()))
    if utils.getNow() >= mVal.tValid:
        return CheckResult(False, (GMDD.data.ZMJ_STAR_BOSS_INVALID, ()))
    if mVal.killer:
        return CheckResult(False, (GMDD.data.ZMJ_STAR_BOSS_KILLED, ()))
    if len(mVal.candidates) >= ZFCD.data.get('starBossShareLimit', 0):
        return CheckResult(False, (GMDD.data.ZMJ_STAR_BOSS_SHARE_UP_LIMIT, ()))
    if tar in mVal.candidates:
        return CheckResult(False, (GMDD.data.ZMJ_STAR_BOSS_SHARE_ALREADY, ()))
    return CheckResult(True, 0)


def checkApplyStarBoss(mVal, gbId):
    if not mVal:
        return CheckResult(False, (GMDD.data.ZMJ_STAR_BOSS_NONE, ()))
    if gbId not in mVal.allMembers:
        return CheckResult(False, (GMDD.data.ZMJ_STAR_BOSS_OCCUPY_PRIORITY, ()))
    if utils.getNow() >= mVal.tValid:
        return CheckResult(False, (GMDD.data.ZMJ_STAR_BOSS_INVALID, ()))
    if mVal.killer:
        return CheckResult(False, (GMDD.data.ZMJ_STAR_BOSS_KILLED, ()))
    if mVal.ownerGbId:
        return CheckResult(False, (GMDD.data.ZMJ_STAR_BOSS_OCCUPY_OWNER, ()))
    return CheckResult(True, 0)


def checkApplyObserveStarBoss(mVal, src):
    if not mVal:
        return CheckResult(False, (GMDD.data.ZMJ_STAR_BOSS_NONE, ()))
    if utils.getNow() >= mVal.tExpired:
        return CheckResult(False, (GMDD.data.ZMJ_STAR_BOSS_EXPIRED, ()))
    if src not in mVal.allMembers:
        return CheckResult(False, (GMDD.data.ZMJ_STAR_BOSS_OBSERVE_PRIORITY, ()))
    if not mVal.ownerGbId:
        return CheckResult(False, (GMDD.data.ZMJ_STAR_BOSS_OBSERVE_NO_OWNER, ()))
    if mVal.ownerGbId == src:
        return CheckResult(False, (GMDD.data.ZMJ_STAR_BOSS_OBSERVE_INVALID, ()))
    return CheckResult(True, 0)
